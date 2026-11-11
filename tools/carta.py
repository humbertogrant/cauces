# -*- coding: utf-8 -*-
"""Carta de la vitrina del Nilo: relieve sombreado, cauce fino, costas de la región y rótulos de atlas → src/vitrina/carta-datos.js

    python tools/carta.py

- Relieve (CARTA.luz): ETOPO1 (NOAA NCEI, dominio público), el mismo ráster que usa tools/relieve.py (tools/ne/etopo1_mundo_…tif,
  ≈ 0,18°). Se recorta la ventana del Nilo, se exagera lo bajo (para que el valle y las tierras altas de Etiopía se lean), se
  sombrea con luz del noroeste en dos escalas y se guarda como UN WebP con transparencia ya en la paleta: sombras hacia #174A3F,
  luces hacia #2B6E5E y un poco más, con el alfa proporcional a la fuerza. Así entra sobre la tierra #215A4F sin modo de mezcla.
- Relieve fino (CARTA.luz2): el corredor del río con el mosaico DEM de NOAA NCEI que tools/relieve.py bajó para el perfil del Nilo
  (tools/ne/dem_rio_nilo_…tif, 0,015°), ya pintado sobre el color de la tierra y desvanecido en los bordes; carta.js lo muestra al
  acercarse.
- Cauce fino (CARTA.curso, CARTA.brazos): Natural Earth 10 m (dominio público), encadenado con las funciones de tools/cauces.py (se
  leen sin correr su parte principal: no toca rios.js), simplificado a la tolerancia de pantalla y con un vértice en la proyección
  de cada parada. Las cifras del juego no cambian: las fija src/juegos/nilo.js.
- Costas, lagos y fronteras de la región (CARTA.tierra, CARTA.lagos, CARTA.bordes): Natural Earth 10 m, finos cerca del río y cada
  vez más gruesos lejos, en la proyección del motor (x=(lon+180)/360·1000, y=(90−lat)/180·500).
- Rótulos, líneas e hitos: posiciones fijas elegidas a mano (geografía, no datos del juego). carta.js decide cuáles caben.
No baja nada de la red. Deja vistas previas en la carpeta temporal del sistema (fuera del repositorio).
"""
import os,io,json,base64,tempfile,subprocess,glob
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import shapely
from shapely.geometry import LineString,Point,shape
Image.MAX_IMAGE_PIXELS=None
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI)
TIF=os.path.join(AQUI,'ne','etopo1_mundo_ETOPO1_ice_surface.tif')
SALIDA=os.path.join(RAIZ,'src','vitrina','carta-datos.js')
BB=(-180,-60,180,84)                 # lon O, lat S, lon E, lat N del ráster (ver BB_MUNDO en relieve.py)
LATN,LONO,LATS,LONE=36,18,-6,46      # la ventana del Nilo
ANCHO=400; ALTO=int(round(ANCHO*(LATN-LATS)/(LONE-LONO)))
TOPE=150000                          # caracteres de base64 entre los dos relieves
TOPE_LEJOS=70000                     # … de los cuales, el lejano
BASE=(0x21,0x5A,0x4F); BAJA=(0x17,0x4A,0x3F); BAJA2=(0x11,0x3E,0x35); ALTA=(0x2B,0x6E,0x5E); ALTA2=(0x45,0x94,0x7E)
REGION=(-20,-25,75,50)               # lon O, lat S, lon E, lat N de las costas de la carta

def fuerza(z,escalas,z0=0):
    """Sombreado con luz del noroeste a 45° (−1 sombra … +1 luz) de una altura z; escalas: [(peso, suavizado en px, k)].
    z0 (metros) amansa la exageración junto al nivel del mar: sin él, en el DEM fino el delta, que es plano, sale lleno de ruido."""
    zc=(np.power(np.clip(z,0,None)+z0,0.6)-z0**0.6)*8   # exagera lo bajo: 100 m → 127, 1 000 m → 505, 3 000 m → 975
    e=0
    for peso,sig,k in escalas:
        s=ndi.gaussian_filter(zc,sig); gy,gx=np.gradient(s)   # gy crece hacia el sur, gx hacia el este
        if k<0: k=max(float(np.percentile(np.hypot(gx,gy)[z>1],-k)),1e-3)   # k negativo: el percentil de la pendiente que hace de «45°»
        v=(.5*gx+.5*gy+.7071*k)/np.sqrt(gx*gx+gy*gy+k*k)-.7071
        e=e+peso*np.where(v>0,v/.2929,v/.55)
    e=np.sign(e)*np.power(np.clip(np.abs(e),0,1),.8)
    e=e+.30*np.clip((z-700)/2000,0,1)-.10*np.clip(1-z/250,0,1)   # las tierras altas, más claras; el valle y la costa, más oscuros
    return np.clip(e,-1,1)
def color(e):
    f=np.abs(e)[...,None]; t=np.clip((f-.55)/.45,0,1)
    mez=lambda c1,c2: np.array(c1,np.float32)*(1-t)+np.array(c2,np.float32)*t
    return np.where(e[...,None]>0,mez(ALTA,ALTA2),mez(BAJA,BAJA2))
def borde(alto,ancho,b):
    y=np.minimum(np.arange(alto),np.arange(alto)[::-1])/b; x=np.minimum(np.arange(ancho),np.arange(ancho)[::-1])/b
    m=np.clip(np.minimum.outer(y,x),0,1); return m*m*(3-2*m)
def etopo(latn,lono,lats,lone,ancho,alto):
    a=np.array(Image.open(TIF),dtype=np.float32); a[~np.isfinite(a)|(np.abs(a)>12000)]=0
    H,W=a.shape
    lat=latn-(np.arange(alto)+.5)*(latn-lats)/alto; lon=lono+(np.arange(ancho)+.5)*(lone-lono)/ancho
    F,C=np.meshgrid((BB[3]-lat)/(BB[3]-BB[1])*H-.5,(lon-BB[0])/(BB[2]-BB[0])*W-.5,indexing='ij')
    return np.clip(ndi.map_coordinates(a,[F,C],order=3,mode='nearest'),0,None)
def relieve():
    z=etopo(LATN,LONO,LATS,LONE,ANCHO,ALTO); k=ANCHO/400
    e=fuerza(z,[(.6,1.3*k,34/k),(.45,5*k,15/k)])
    a=np.clip(np.abs(e)*.9,0,1)[...,None]; rgb=np.array(BASE,np.float32)*(1-a)+color(e)*a   # ya pintado sobre el color de la tierra: el alfa solo desvanece los bordes de la ventana (y así el WebP pesa la mitad)
    return np.dstack([np.clip(rgb,0,255),borde(ALTO,ANCHO,22*k)[...,None]*255]).round().astype(np.uint8),z
def webp(img,tope,calidades=(86,82,78,74,70,64,58,50,42,34),alfa=None):
    for q in calidades:
        buf=io.BytesIO(); img.save(buf,'WEBP',quality=q,alpha_quality=min(q+6,90) if alfa is None else alfa,method=6); b=base64.b64encode(buf.getvalue()).decode()
        if len(b)<=tope: return b,q
    raise SystemExit('el relieve no entra en %d caracteres de base64'%tope)

# ---------- el cauce fino ----------
NOMBRES=['Victoria Nile','Albert Nile','Bahr el Jebel','El Bahr el Abyad','Nile','Rosetta Branch']
DESDE,HASTA=[0.43,33.19],[31.44,30.40]   # Jinja, donde el Nilo sale del lago Victoria, y la boca de Rosetta
BRAZOS=[('Nilo Azul',['Abay','El Bahr el Azraq'],[12.0,37.3],[15.63,32.49]),
        ('Atbara',['Atbara'],[14.62,35.9],[17.67,33.98]),
        ('Sobat',['Sobat'],[7.92,33.21],[9.38,31.54]),
        ('Bahr el Zeraf',['Bahr el  Zeraf'],[7.77,30.55],[9.43,31.14]),
        ('brazo de Damieta',['Damietta Branch'],[30.18,31.1],[31.53,31.84])]
def cauces_py():
    """Las funciones de tools/cauces.py (camino, proyectar, redondear…) sin correr su parte principal, que reescribe rios.js."""
    f=os.path.join(AQUI,'cauces.py'); src=open(f,encoding='utf8').read(); ns={'__file__':f,'__name__':'cauces_sin_principal'}
    exec(compile(src[:src.index('\nruta_rios=')],f,'exec'),ns); return ns
def nilo_de_cauces():
    texto=open(os.path.join(RAIZ,'src','data','rios.js'),encoding='utf8').read()
    r=subprocess.run(['node'],input=texto+";const r=RIVERS.find(r=>r.id==='nilo');console.log(JSON.stringify({curso:r.curso,ciudades:r.ciudades.map(c=>[c.nombre,c.pos]),imagenes:r.ciudades.map(c=>c.imagen)}))",capture_output=True,text=True,encoding='utf8')
    return json.loads(r.stdout)
def renglones(hoy):
    """Los renglones de RENGLONES que de verdad están, letra por letra, en los datos del juego."""
    naves=open(os.path.join(RAIZ,'src','data','naves.js'),encoding='utf8').read()
    puertos=json.loads(subprocess.run(['node'],input=naves+";console.log(JSON.stringify(NAVES.nilo.puertos.map(p=>p[0])))",capture_output=True,text=True,encoding='utf8').stdout)
    out={}
    for i,(texto,donde) in RENGLONES.items():
        fuente=(hoy['imagenes'] if donde=='imagen' else puertos)[i]
        if texto in fuente: out[str(i)]=texto
        else: print('  aviso: «%s» ya no está en los datos de %s: el renglón no sale'%(texto,hoy['ciudades'][i][0]))
    return out
def cauce():
    C=cauces_py(); hoy=nilo_de_cauces(); d=lambda a,b:((a[0]-b[0])**2+(a[1]-b[1])**2)**.5
    pts=C['camino'](NOMBRES,DESDE,HASTA,'ne10'); crudo=len(pts)
    for tol in (0.002,0.003,0.004,0.005,0.006,0.008,0.01,0.015):
        s=list(LineString(pts).simplify(tol,preserve_topology=False).coords)
        if len(s)<=660: break
    curso=C['redondear'](C['proyectar'](s,hoy['ciudades']),3)
    for extremo,viejo in ((0,hoy['curso'][0]),(-1,hoy['curso'][-1])):   # el mismo primer y último punto que el curso de hoy (0,05°)
        if d(curso[extremo],viejo)>0.05: curso.insert(0,viejo) if extremo==0 else curso.append(viejo)
    ult=0; lejos=[]
    for nombre,pos in hoy['ciudades']:   # la regla del motor: el vértice más cercano, sin retroceder
        i=min(range(ult,len(curso)),key=lambda k:d(curso[k],pos)); lejos.append('%s %d (%.3f°)'%(nombre,i,d(curso[i],pos)))
        if i<ult or (ult and i==ult): raise SystemExit('las paradas no quedan en orden sobre el cauce fino: '+nombre)
        ult=i
    print('cauce: %d vértices de Natural Earth 10 m → %d (tolerancia %.3f°); extremos a %.3f° y %.3f° de los de hoy'%(crudo,len(curso),tol,d(curso[0],hoy['curso'][0]),d(curso[-1],hoy['curso'][-1])))
    print('  paradas (vértice, distancia): '+' · '.join(lejos))
    eje=LineString([(p[1],p[0]) for p in curso]); brazos=[]
    for nombre,nombres,desde,hasta in BRAZOS:
        try: b=C['camino'](nombres,desde,hasta,'ne10')
        except SystemExit as e: print('  sin brazo',nombre,':',e); continue
        b=list(LineString(b).simplify(0.006,preserve_topology=False).coords)
        for k in (0,-1):   # el extremo que toca el cauce se pega a él
            q=eje.interpolate(eje.project(Point(b[k])))
            if q.distance(Point(b[k]))<0.12:
                if k==0: b.insert(0,(q.x,q.y))
                else: b.append((q.x,q.y))
        brazos.append(C['redondear'](b,3)); print('  brazo %s: %d vértices'%(nombre,len(brazos[-1])))
    return curso,brazos,hoy

# ---------- el relieve fino del corredor ----------
FINO=dict(lleno=0.9,nada=2.4,orilla=0.35)   # grados desde el cauce: hasta dónde el relieve fino va entero y dónde ya no queda nada; y el margen en que se apaga contra el borde del DEM
def relieve_fino(curso_hoy,curso):
    """El corredor del río con el mosaico DEM de NOAA NCEI que tools/relieve.py bajó para el perfil (0,015°): su caja es la del
    curso de Cauces más 0,3°. Sale ya pintado sobre el color de la tierra y con el alfa según la distancia al cauce: entero junto
    al río y desvanecido hacia los costados, donde vuelve a verse el relieve lejano (así no queda una franja con el corte a la vista)."""
    import hashlib
    la=[p[0] for p in curso_hoy]; lo=[p[1] for p in curso_hoy]; bb=(min(lo)-.3,min(la)-.3,max(lo)+.3,max(la)+.3)
    W=min(int((bb[2]-bb[0])/0.015),6000); H=max(int(W*(bb[3]-bb[1])/(bb[2]-bb[0])),8)
    f=os.path.join(AQUI,'ne','dem_rio_nilo_DEM_global_mosaic_%s.tif'%hashlib.md5(('%r%r'%(tuple(round(v,4) for v in bb),(W,H))).encode()).hexdigest()[:6])
    if not os.path.exists(f): print('sin relieve fino: falta',f,'(lo baja python tools/relieve.py cauces amplia)'); return None
    d=np.array(Image.open(f),dtype=np.float32); d[~np.isfinite(d)|(np.abs(d)>12000)]=0; d=ndi.gaussian_filter(np.clip(d,0,None),.7)
    alto,ancho=d.shape; px=(bb[2]-bb[0])/ancho; py=(bb[3]-bb[1])/alto
    e=fuerza(d,[(.55,1.3,-80),(.35,6.5,-82),(.3,23,-86)],z0=80); a=(np.abs(e)*.82)[...,None]
    rgb=np.array(BASE,np.float32)*(1-a)+color(e)*a
    lejos=np.ones((alto,ancho),bool)   # el cauce fino, pintado en la grilla, para medir la distancia a él
    for (la0,lo0),(la1,lo1) in zip(curso,curso[1:]):
        for t in np.linspace(0,1,int(max(abs(la1-la0)/py,abs(lo1-lo0)/px))+2):
            i=int((bb[3]-(la0+(la1-la0)*t))/py); j=int((lo0+(lo1-lo0)*t-bb[0])/px)
            if 0<=i<alto and 0<=j<ancho: lejos[i,j]=False
    suave=lambda t:(lambda u:u*u*(3-2*u))(np.clip(t,0,1))
    w=1-suave((ndi.distance_transform_edt(lejos,sampling=(py,px))-FINO['lleno'])/(FINO['nada']-FINO['lleno']))
    w=w*suave(np.minimum.outer(np.minimum(np.arange(alto),np.arange(alto)[::-1])*py,np.minimum(np.arange(ancho),np.arange(ancho)[::-1])*px)/FINO['orilla'])
    im=np.dstack([np.clip(rgb,0,255),w[...,None]*255]).round().astype(np.uint8)
    return im,[bb[3],bb[0],bb[1],bb[2]],d.shape

# ---------- costas, lagos y fronteras de la región ----------
def ne(nombre): return [shape(f['geometry']) for f in json.load(open(os.path.join(AQUI,'ne',nombre+'.geojson'),encoding='utf8'))['features'] if f['geometry']]
def partes(g,tipo):
    if g.is_empty: return []
    if g.geom_type==tipo: return [g]
    return [x for h in getattr(g,'geoms',[]) for x in partes(h,tipo)]
TOL=(0.008,0.05,0.22)        # tolerancia (grados) cerca del río, a media distancia y lejos
TOL_B=(0.02,0.12,0.5)        # lo mismo para las fronteras
CERCA,MEDIO=5.0,13.0         # grados desde el cauce
def mapa(curso):
    eje=LineString([(p[1],p[0]) for p in curso]); zc=eje.buffer(CERCA); zm=eje.buffer(MEDIO); shapely.prepare(zc); shapely.prepare(zm)
    def clase(xy): xy=np.asarray(xy); c=shapely.contains_xy(zc,xy[:,0],xy[:,1]); m=shapely.contains_xy(zm,xy[:,0],xy[:,1]); return np.where(c,0,np.where(m,1,2))
    def texto(xy,cierra):
        cl=clase(xy); out=[]
        for (x,y),c in zip(xy,cl):
            X,Y=(x+180)/360*1000,(90-y)/180*500
            out.append(('%.1f %.1f' if c==2 else '%.2f %.2f')%(X,Y))
        return 'M'+'L'.join(out)+('Z' if cierra else '')
    def anillo(coords):
        """Simplifica un anillo con la tolerancia de cada tramo (cerca, medio, lejos), sin mover los vértices donde cambia."""
        xy=list(coords)[:-1]; n=len(xy)
        if n<3: return None
        cl=clase(xy); cambios=[i for i in range(n) if cl[i]!=cl[i-1]]
        if not cambios: out=list(LineString(xy+[xy[0]]).simplify(TOL[cl[0]],preserve_topology=False).coords)[:-1]
        else:
            orden=list(range(cambios[0],n))+list(range(cambios[0])); out=[]; i=0
            while i<n:
                c=cl[orden[i]]; j=i
                while j<n and cl[orden[j]]==c: j+=1
                t=[xy[orden[k]] for k in range(i,j)]+[xy[orden[j%n]]]
                if len(t)>2: t=list(LineString(t).simplify(TOL[c],preserve_topology=False).coords)
                out+=t[:-1]; i=j
        return out if len(out)>=3 else None
    def poligonos(gs,minimo):
        out=[]; nv=0
        for g in gs:
            for p in partes(shapely.clip_by_rect(g,*REGION),'Polygon'):
                c=0 if p.intersects(zc) else 1 if p.intersects(zm) else 2
                if p.area<minimo[c]: continue
                for r in [p.exterior]+list(p.interiors):
                    a=anillo(r.coords)
                    if a: out.append(texto(a,True)); nv+=len(a)
        return ''.join(out),nv
    tierra,nt=poligonos(ne('ne_10m_land'),(0.0008,0.02,0.25))
    lagos10=[g for g in ne('ne_10m_lakes') if g.intersects(zm)]; lagos50=[g for g in ne('ne_50m_lakes') if not g.intersects(zm)]
    l1,n1=poligonos(lagos10,(0.002,0.05,9)); l2,n2=poligonos(lagos50,(9,9,0.3))
    lineas=[]; nb=0
    # Natural Earth trae cada frontera en muchos pedacitos: primero se unen en líneas largas y después se cortan por zona
    g=shapely.line_merge(shapely.unary_union([shapely.clip_by_rect(x,*REGION) for x in ne('ne_10m_admin_0_boundary_lines_land')]))
    for zona,t in ((g.intersection(zc),TOL_B[0]),(g.intersection(zm).difference(zc),TOL_B[1]),(g.difference(zm),TOL_B[2])):   # las fronteras son líneas punteadas y tenues: aguantan más simplificación que la costa
        if zona.geom_type!='LineString' and not zona.is_empty: zona=shapely.line_merge(shapely.unary_union(partes(zona,'LineString')))
        for l in partes(zona,'LineString'):
            if l.length<t*1.5: continue
            s=list(l.simplify(t,preserve_topology=False).coords)
            if len(s)>=2: lineas.append(texto(s,False)); nb+=len(s)
    bordes=''.join(lineas)
    print('mapa: costa %d vértices, %.1f KB · lagos %d vértices, %.1f KB · fronteras %d vértices, %.1f KB · total %.1f KB'%(nt,len(tierra)/1024,n1+n2,len(l1+l2)/1024,nb,len(bordes)/1024,(len(tierra)+len(l1+l2)+len(bordes))/1024))
    return tierra,l1+l2,bordes

# Rótulos: t (| parte en renglones), p [lat, lon] del ancla, a (start|middle|end), c (clase: agua, pais, rio-n), g (giro),
# max y min: ancho de vista (en unidades del SVG, llevado a un teléfono de 390 px) a partir del cual se oculta o se muestra;
# tras: índice de la parada que tiene que estar alcanzada para que salga.
# De cada nombre sale una sola versión por vista: la primera de la lista que cabe.
ROTULOS=[
 dict(t='MAR MEDITERRÁNEO',p=[32.75,28.6],a='middle',c='agua',max=130,min=14),
 dict(t='MAR MEDITERRÁNEO',p=[31.85,31.95],a='middle',c='agua',max=14),
 dict(t='MAR ROJO',p=[20.0,38.3],a='middle',c='agua',g=59,max=130,min=40),
 dict(t='MAR|ROJO',p=[23.2,36.95],a='middle',c='agua',max=40),
 dict(t='LAGO VICTORIA',p=[-2.2,33.0],a='middle',c='agua',max=130,min=40),
 dict(t='LAGO VICTORIA',p=[-1.3,33.0],a='middle',c='agua',max=40),
 dict(t='LAGO NASSER',p=[23.0,31.75],a='end',c='agua',max=60),
 dict(t='Nilo Blanco',p=[11.1,31.7],a='end',c='rio-n',max=130,min=40),
 dict(t='Nilo Blanco',p=[14.2,31.9],a='end',c='rio-n',max=40),
 dict(t='Nilo Azul',p=[13.9,34.3],a='start',c='rio-n',max=130,min=40),
 dict(t='Nilo Azul',p=[14.45,33.9],a='start',c='rio-n',max=40),
 dict(t='SUDD',p=[7.75,29.75],a='end',c='pais',max=130),
 dict(t='SUDD',p=[6.9,31.9],a='start',c='pais',max=130),
 dict(t='EGIPTO',p=[22.3,27.9],a='start',c='pais',max=60),
 dict(t='EGIPTO',p=[26.6,28.0],a='middle',c='pais',max=60),
 dict(t='EGIPTO',p=[28.0,29.3],a='start',c='pais',max=20),
 dict(t='SUDÁN',p=[21.5,27.9],a='start',c='pais',max=60),
 dict(t='SUDÁN',p=[12.2,27.6],a='start',c='pais',max=60),
 dict(t='SUDÁN DEL SUR',p=[6.3,29.6],a='end',c='pais',max=60),
 dict(t='UGANDA',p=[0.8,32.2],a='end',c='pais',max=60),
 dict(t='ETIOPÍA',p=[8.9,37.1],a='end',c='pais',max=60),
 dict(t='DESIERTO|DE NUBIA',p=[20.9,34.9],a='middle',c='pais',max=60),
 # el delta, rotulado: solo cuando El Cairo ya se alcanzó (tras=5), junto a cada brazo
 dict(t='brazo de Rosetta',p=[30.72,30.6],a='end',c='rio-n',max=30,tras=5),
 dict(t='brazo de Damieta',p=[30.72,31.55],a='start',c='rio-n',max=30,tras=5),
]
# La boca del río: el rótulo va pegado al último punto del cauce (carta.js prueba varios lados, según dónde esté la barca)
BOCA=dict(t='desembocadura',max=30,tras=5)
# Un renglón en cursiva bajo el nombre de la parada donde está la barca, solo donde los datos del juego lo dan tal cual:
# índice de la parada → (texto, dónde tiene que estar: la imagen de la ciudad en rios.js o el puerto de NAVES). Si no está, no sale.
RENGLONES={3:('primera catarata','imagen'),5:('puerto de Bulaq','nave')}
# Hitos: ninguno es una parada del juego. m: marca (cuadro | tri); l: de qué lado va el nombre (izq | der);
# tras: índice de la parada que tiene que estar alcanzada para que el hito aparezca (Guiza queda pegada a El Cairo: memoria primero).
HITOS=[
 dict(t='Abu Simbel',p=[22.34,31.63],m='cuadro',l='izq',max=45),
 dict(t='Pirámides de Meroe',p=[16.94,33.75],m='tri',l='der',max=45),
 dict(t='Pirámides de Guiza',p=[29.98,31.13],m='tri',l='izq',max=45,tras=5),
 dict(t='Alejandría',p=[31.20,29.92],m='cuadro',l='izq',max=45),
 dict(t='Port Said',p=[31.26,32.30],m='cuadro',l='der',max=30,tras=5),
 dict(t='Suez',p=[29.97,32.55],m='cuadro',l='der',max=30,tras=5),
]
# Paralelos con nombre: rio = longitud donde el Nilo (o su lago) los cruza, para que el rótulo se vaya al otro lado
LINEAS=[dict(t='ECUADOR',lat=0,rio=33.2,portada='izq'),dict(t='TRÓPICO DE CÁNCER',lat=23.44,rio=32.9,portada='der')]
RETICULA=dict(paso=5,lat=[-10,40],lon=[10,55])

def main():
    im,z=relieve(); img=Image.fromarray(im,'RGBA'); b64,q=webp(img,TOPE_LEJOS)
    datos=dict(luz=dict(src='data:image/webp;base64,'+b64,caja=[LATN,LONO,LATS,LONE],px=[ANCHO,ALTO]),reticula=RETICULA,lineas=LINEAS,rotulos=ROTULOS,hitos=HITOS)
    a=im[...,3]; print('relieve %d×%d, calidad %d: %d caracteres de base64; alfa medio %.2f, máximo %d; altura máxima %.0f m'%(ANCHO,ALTO,q,len(b64),a.mean()/255,a.max(),z.max()))
    fondo=Image.new('RGBA',img.size,BASE+(255,)); fondo.alpha_composite(img); vista=os.path.join(tempfile.gettempdir(),'carta-relieve-vista.png'); fondo.convert('RGB').save(vista)
    curso,brazos,hoy=cauce(); datos['curso']=curso; datos['brazos']=brazos
    datos['boca']=BOCA; datos['renglones']=renglones(hoy); print('renglones:',datos['renglones'])
    datos['tierra'],datos['lagos'],datos['bordes']=mapa(curso)
    F=relieve_fino(hoy['curso'],curso)
    if F:
        im2,caja2,forma=F; img2=Image.fromarray(im2,'RGBA'); b2,q2=webp(img2,TOPE-len(b64),alfa=35)   # el alfa es un degradado suave: con poca calidad pesa la quinta parte y no se nota
        datos['luz2']=dict(src='data:image/webp;base64,'+b2,caja=caja2,px=[im2.shape[1],im2.shape[0]],max=36)   # max: ancho de vista (llevado a 390 px) hasta el que se muestra
        print('relieve fino %d×%d, calidad %d: %d caracteres de base64; los dos relieves, %d (tope %d)'%(im2.shape[1],im2.shape[0],q2,len(b2),len(b2)+len(b64),TOPE))
        tmp=tempfile.gettempdir(); f2=Image.new('RGBA',img2.size,BASE+(255,)); f2.alpha_composite(img2); f2.convert('RGB').save(os.path.join(tmp,'carta-relieve-fino-vista.png'))
        f0=int((caja2[0]-27.2)/((caja2[0]-caja2[2])/im2.shape[0])); f2.convert('RGB').crop((0,f0,im2.shape[1],f0+275)).resize((im2.shape[1]*2,550),Image.LANCZOS).save(os.path.join(tmp,'carta-relieve-fino-recorte.png'))   # de Asuán a Luxor, al doble
    cab='// Generado por tools/carta.py: no editar a mano. Relieve de ETOPO1 y del mosaico DEM de NOAA NCEI (dominio público); cauce, costas, lagos y fronteras de Natural Earth 10 m (dominio público); rótulos de geografía puestos a mano.\n'
    open(SALIDA,'w',encoding='utf-8',newline='\n').write(cab+'const CARTA='+json.dumps(datos,ensure_ascii=False,separators=(',',':'))+';\n')
    print('datos:',SALIDA,'(%.1f KB)'%(os.path.getsize(SALIDA)/1024)); print('vista previa:',vista)
if __name__=='__main__': main()
