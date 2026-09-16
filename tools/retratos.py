"""Retratos «grabado» de los animales para la edición amplia: src/data/retratos.js a partir de láminas de dominio público.

Uso: python tools/retratos.py [glifos]   (sin glifos, todos los de tools/retratos/fuentes.json; requiere: pip install pillow numpy
shapely matplotlib). Cada entrada de fuentes.json dice de dónde sale la lámina (url de Wikimedia Commons, título, autor, año y
licencia, que va al pie de la ficha), cómo prepararla (recorte en fracciones [x0,y0,x1,y1], voltear para que mire a la derecha,
ancho de trabajo en píxeles) y los dos umbrales de oscuridad (medio y oscuro, de 0 a 1). Las láminas originales se guardan en
tools/retratos/orig/ (no se versionan: se bajan de la url si faltan).

Cómo se traza: la imagen en gris se recorta, se voltea si hace falta, se reduce al ancho de trabajo con un poco de desenfoque,
se estira el contraste para que el papel quede blanco y se convierte en dos capas de «oscuridad ≥ umbral» con contornos rellenos
(matplotlib, como las franjas de relieve): la capa media (verde medio) y la oscura (verde tinta). Cada capa se simplifica
(shapely) y sale como un path SVG con fill-rule evenodd (los huecos se respetan solos). Resultado por animal: 10-30 KB.
El motor la dibuja con retrato(m) en el globo (modo Adulto) y en la ficha «Conocé a …» al empezar el río.
"""
import json,os,sys,io,urllib.request
import numpy as np
from PIL import Image,ImageFilter,ImageOps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,MultiPolygon
from shapely import make_valid
from shapely.ops import unary_union

RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR=os.path.join(RAIZ,'tools','retratos');ORIG=os.path.join(DIR,'orig');os.makedirs(ORIG,exist_ok=True)
UA={'User-Agent':'cauces-juego/1.0 (juego educativo de un solo archivo) retratos de animales'}
FUENTES=json.load(open(os.path.join(DIR,'fuentes.json'),encoding='utf8'))
SALIDA=os.path.join(RAIZ,'src','data','retratos.js')

def bajar(f):
    ruta=os.path.join(ORIG,f['archivo'])
    if not os.path.exists(ruta):
        print('  bajando',f['url']);open(ruta,'wb').write(urllib.request.urlopen(urllib.request.Request(f['url'],headers=UA),timeout=300).read())
    return ruta

def preparar(f):
    im=Image.open(bajar(f)).convert('L')
    if f.get('recorte'):
        x0,y0,x1,y1=f['recorte'];W,H=im.size;im=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
    if f.get('voltear'): im=ImageOps.mirror(im)
    W=f.get('ancho',300);H=max(int(im.size[1]*W/im.size[0]),8)
    im=im.resize((W,H),Image.LANCZOS).filter(ImageFilter.GaussianBlur(f.get('desenfoque',0.7)))
    a=np.asarray(im,dtype=np.float32)/255.0
    lo,hi=np.percentile(a,f.get('negro',1.0)),np.percentile(a,f.get('blanco',92.0))   # el papel queda blanco, la tinta más oscura queda negra
    a=np.clip((a-lo)/max(hi-lo,1e-3),0,1)
    return 1.0-a   # oscuridad: 0 papel, 1 tinta

def capa(osc,umbral):
    """Polígonos (px, y hacia abajo) donde la oscuridad es ≥ umbral, con contornos rellenos; los huecos los resuelve evenodd."""
    H,W=osc.shape;X=np.arange(W);Y=np.arange(H)
    fig=plt.figure();cs=plt.contourf(X,Y,osc,levels=[umbral,1e9]);plt.close(fig)
    anillos=[]
    for path in cs.get_paths():
        for poly in path.to_polygons(closed_only=True):
            if len(poly)>=4:
                p=Polygon(poly)
                if p.area>=2.0: anillos.append(p)
    return anillos

def simplificar(anillos,tol,area_min):
    out=[]
    for p in anillos:
        q=p.simplify(tol,preserve_topology=True)
        if q.is_empty or q.area<area_min: continue
        out.append(q)
    return out

def path(anillos,dec=1):
    d=[]
    for p in anillos:
        pts=list(p.exterior.coords)[:-1]
        d.append('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in pts)+'Z')
    return ''.join(d)

def recortar_al_cuerpo(medio,oscuro,halo,parte):
    """Deja solo lo que está cerca del animal: el cuerpo es el polígono mayor de la capa media (con sus huecos rellenos, más los
    otros polígonos grandes, como una cola separada), dilatado `halo` píxeles; el pasto y los fondos lejanos del grabado se van."""
    if not medio: return medio,oscuro
    grandes=sorted(medio,key=lambda p:-p.area);mayor=grandes[0].area
    cuerpo=unary_union([Polygon(p.exterior) for p in grandes if p.area>=parte*mayor]).buffer(halo)
    def dentro(ps):
        out=[]
        for p in ps:
            q=p.intersection(cuerpo)
            if q.is_empty: continue
            for g in (q.geoms if hasattr(q,'geoms') else [q]):
                if g.geom_type=='Polygon' and g.area>=2: out.append(g)
        return out
    return dentro(medio),dentro(oscuro)

def silueta(medio,parte,cierre,apertura):
    """La forma del animal: los polígonos grandes de la capa media con los huecos rellenos, unidos, con los huecos entre partes
    cerrados (buffer de ida y vuelta) y sin las salientes delgadas, pasto y briznas pegadas al lomo (apertura: buffer de vuelta e
    ida). Es la base del personaje: se rellena plano, como un glifo, y encima va la cara."""
    if not medio: return []
    grandes=sorted(medio,key=lambda p:-p.area);mayor=grandes[0].area
    g=unary_union([Polygon(p.exterior) for p in grandes if p.area>=parte*mayor]).buffer(cierre).buffer(-cierre)
    if apertura>0: g=g.buffer(-apertura).buffer(apertura)
    g=g.simplify(0.9,preserve_topology=True)
    return [p for p in (g.geoms if hasattr(g,'geoms') else [g]) if p.geom_type=='Polygon' and p.area>=20]

def trazar(f):
    osc=preparar(f);H,W=osc.shape
    tol=f.get('tolerancia',0.6);am=f.get('area_min',6.0)
    medio=capa(osc,f.get('medio',0.32));oscuro=capa(osc,f.get('oscuro',0.62))
    sil=silueta(medio,f.get('parte_silueta',0.5),f.get('cierre',3.0),f.get('apertura',4.0))
    if f.get('halo',8)>0: medio,oscuro=recortar_al_cuerpo(medio,oscuro,f.get('halo',8),f.get('parte',0.3))
    medio=simplificar(medio,tol,am);oscuro=simplificar(oscuro,tol,am)
    r=dict(v=f'0 0 {W} {H}',m=path(medio),o=path(oscuro),s=path(sil))
    if f.get('cara'): r['c']=f['cara']   # ojo [x,y], boca [x,y] y tamaño k en píxeles del retrato: dónde va la cara dibujada del personaje
    return r

def js(s): return json.dumps(s,ensure_ascii=False)
if __name__=='__main__':
    quiero=set(sys.argv[1:])
    lineas=[]
    for f in FUENTES:
        if quiero and f['glifo'] not in quiero: continue
        r=trazar(f);cred=f.get('credito') or f"{f.get('autor','Grabado')}, {f.get('anio','siglo XIX')} · {f.get('licencia','dominio público')} · Wikimedia Commons"
        cara=(',c:'+js(r['c'])) if r.get('c') else ''
        lineas.append(f"{f['glifo']}:{{v:'{r['v']}',m:'{r['m']}',o:'{r['o']}',s:'{r['s']}'{cara},f:{js(cred)}}}")
        print(f"  {f['glifo']:13} {r['v']:14} medio {len(r['m'])//1024} KB · oscuro {len(r['o'])//1024} KB · silueta {len(r['s'])//1024} KB")
    if quiero:   # con glifos como argumentos, se conservan los demás retratos ya generados
        viejo=open(SALIDA,encoding='utf8').read() if os.path.exists(SALIDA) else ''
        for l in viejo.split('\n'):
            k=l.split(':',1)[0]
            if k and k.replace('/*@amplia*/','').strip() not in quiero and '{v:' in l: lineas.append(l.rstrip(',').rstrip('};').replace('/*@amplia*/','').replace('/*@fin:amplia*/',''))
    cab='// Generado por tools/retratos.py: no editar a mano. Retratos «grabado» de los animales (dos capas: medio y oscuro), solo en la edición amplia.\n'
    cuerpo='/*@amplia*/\nconst RETRATOS={\n'+''.join(l+',\n' for l in sorted(set(lineas)))+'};\n/*@fin:amplia*/\n'   # una entrada por línea: build.js recorta las que el juego no usa
    open(SALIDA,'w',encoding='utf8',newline='\n').write(cab+cuerpo)
    print('retratos.js:',len(cuerpo)//1024,'KB,',len(lineas),'retratos')
