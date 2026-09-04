"""Regenera src/data/relieve.js: franjas de altura del mapa, nombres de relieve y perfil de altura de cada recorrido.

Uso: python tools/relieve.py [juego]   (juego: cauces, por defecto, o exploradores; requiere: pip install shapely numpy pillow matplotlib;
descarga a tools/ne/ la primera vez). Para otro juego escribe src/data/relieve-<juego>.js; las rutas y sus vistas las da tools/rutas.py.

Fuentes (todas públicas y citables):
- Alturas del mundo: ETOPO1 (NOAA NCEI, 1 minuto de arco ≈ 1,8 km), servido por recortes desde el ImageServer de NCEI.
- Alturas de los perfiles (mundo y Costa Rica): mosaico DEM global de NCEI (DEM_global_mosaic), mismo servicio; ETOPO1 trae la
  batimetría de los lagos grandes (en Jinja daría el fondo del lago Victoria), por eso no sirve para los perfiles.
- Franjas de Costa Rica: mosaico DEM de NCEI (DEM_all), más fino, mismo servicio.
- Nombres de relieve del mundo: Natural Earth 50 m, regiones físicas (cordilleras, mesetas, desiertos, llanuras, cuencas), con
  su nombre en español (NAME_ES). Natural Earth no trae nada a la escala de Costa Rica: esas etiquetas van en CR_NOMBRES,
  y los volcanes y cerros se ubican con OpenStreetMap (Overpass); la altura que se muestra es la publicada (PICOS_ALTURA), y
  si la de OpenStreetMap difiere se avisa al generar, para revisarla.

Qué produce:
- RELIEVE: por vista ('mundo' y cada zona), franjas «≥ tantos metros» como trazos SVG en las unidades del mapa (viewBox
  1000x500, proyección equirectangular: x=(lon+180)/360*1000, y=(90-lat)/180*500), recortadas a los rectángulos de vista de
  los ríos (los que calcula vbPara en motor.js, para aspectos de pantalla de 1.0 a 4.0), así nunca se ve un borde.
  Mundo: ≥500 m y ≥2 000 m con un decimal; Costa Rica: ≥500 m y ≥1 500 m con tres decimales.
- NOMBRES_RELIEVE: etiquetas {n, t (cordillera | llano | desierto | pico), z (vista)} con posición [lat, lon] y giro en grados;
  las del mundo llevan una posición por río (v: {rio: [lat, lon, giro]}) porque el ancla se calcula dentro de la vista de
  cada río (y, si se puede, en la parte que se ve con cualquier aspecto de pantalla), y solo se muestran las de rango 1-2 o las que quedan cerca del cauce (hasta 14 por vista).
- ALTURAS: por río, puntos [f, alt] del perfil del cauce: f = fracción del largo del cauce (0 fuente, 1 mar), alt en metros,
  muestreado en cada vértice del curso (mínimo de una ventana de 3x3 celdas, para caer al fondo del valle), forzado a no
  subir río abajo y simplificado; los vértices de las paradas siempre se conservan, así altura(r, parada) es exacta.
"""
import json,os,urllib.request,urllib.parse,hashlib,time,math,sys
import rutas as RUTAS
import numpy as np
from PIL import Image
from shapely.geometry import shape,box,Polygon,MultiPolygon,LineString,Point
from shapely.ops import unary_union
from shapely import make_valid,affinity
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE=os.path.join(RAIZ,'tools','ne'); os.makedirs(NE,exist_ok=True)
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
IMG='https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/%s/ImageServer/exportImage?bbox=%s&bboxSR=4326&size=%d,%d&imageSR=4326&format=tiff&pixelType=F32&f=image'
UA={'User-Agent':'cauces (juego educativo de un solo archivo)'}

NIVELES={'mundo':[500,2000],'cr':[500,1500]}
DEC={'mundo':1,'cr':3}
SIMPL={'mundo':(0.6,3),'cr':(0.016,0.012)}          # (tolerancia, área mínima) en unidades del mapa
RES_MUNDO=(2000,800); BB_MUNDO=(-180,-60,180,84)   # ETOPO1 a ~0,18° para las franjas del mundo
RES_CR=0.003                                        # grados por celda para las franjas de Costa Rica (~330 m)
RES_PERFIL={'mundo':0.03,'cr':0.0007}               # grados por celda para muestrear los perfiles
CLASES={'Range/mtn':'cordillera','Plateau':'llano','Plain':'llano','Basin':'llano','Valley':'llano','Lowland':'llano','Tundra':'llano','Wetlands':'llano','Foothills':'llano','Desert':'desierto'}
RANGO_MAX={'cordillera':4,'llano':2,'desierto':3}   # scalerank de Natural Earth admitido por tipo (las cordilleras de rango 4 solo pegadas al cauce)
BAJO_MAR={'volga':-28}                              # ríos que terminan bajo el nivel del océano (Caspio); los demás no bajan de 0
EXCLUIR={'Punyab','península ibérica','SELVAS','LES LAURENTIDES','Meandro de Ordos','Superior Upland','Campos Sertão','Escudo Canadiense','TIERRAS BAJAS DE VYCHEGDA'}
TOPE_POR_VISTA=14
ASPECTOS=(1.0,2.4,4.0)   # aspectos de pantalla cubiertos (teléfono vertical … monitor ancho); el núcleo es lo que se ve con todos
# Etiquetas de Costa Rica (Natural Earth no las tiene): posición aproximada del rótulo y giro en grados (sentido horario)
CR_NOMBRES=[('Cordillera de Guanacaste','cordillera',[10.84,-85.27],33),('Cordillera de Tilarán','cordillera',[10.38,-84.8],32),
 ('Cordillera Volcánica Central','cordillera',[10.13,-84.05],24),('Cordillera de Talamanca','cordillera',[9.42,-83.45],34),
 ('Llanuras del Norte','llano',[10.62,-84.45],0),('Llanuras del Caribe','llano',[10.43,-83.78],0),('Valle Central','llano',[9.87,-84.05],0),('Valle del General','llano',[9.3,-83.63],30)]
PICOS_CR=['Irazú','Turrialba','Poás','Barva','Arenal','Rincón de la Vieja','Orosí','Miravalles','Tenorio','Chirripó']
# Alturas publicadas (revisar en docs/verificacion.md) y posición de respaldo si Overpass no responde
PICOS_ALTURA={'Irazú':([9.979,-83.852],3432),'Turrialba':([10.025,-83.767],3340),'Poás':([10.198,-84.233],2708),'Barva':([10.135,-84.1],2906),
 'Arenal':([10.463,-84.703],1670),'Rincón de la Vieja':([10.83,-85.324],1916),'Orosí':([10.98,-85.473],1659),'Miravalles':([10.748,-85.153],2028),
 'Tenorio':([10.673,-85.015],1916),'Chirripó':([9.484,-83.489],3820)}
OSM_Q='''[out:json][timeout:120];
(node["natural"~"^(volcano|peak)$"]["name"](8.9,-86.0,11.3,-82.5););
out body;'''

import unicodedata
def llano(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def px(lat,lon): return (lon+180)/360*1000,(90-lat)/180*500
def proj(g): return affinity.affine_transform(g,[1000/360,0,0,-500/180,500,250])
def ne(nombre):
    f=os.path.join(NE,nombre+'.geojson')
    if not os.path.exists(f): urllib.request.urlretrieve(URL+nombre+'.geojson',f)
    return json.load(open(f,encoding='utf8'))['features']
def hav(a,b):  # km entre dos [lat,lon]
    R=6371;la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]));q=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(q))

def dem(servicio,bbox,size,nombre):
    """Recorte del DEM como matriz float32 (filas de norte a sur), guardado en tools/ne/<nombre>_<servicio>_<hash>.tif (el hash cambia con el recorte)."""
    f=os.path.join(NE,'%s_%s_%s.tif'%(nombre,servicio,hashlib.md5(('%r%r'%(tuple(round(v,4) for v in bbox),tuple(size))).encode()).hexdigest()[:6]))
    if not os.path.exists(f):
        u=IMG%(servicio,','.join('%.4f'%v for v in bbox),size[0],size[1])
        for i in range(4):
            try:
                b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=300).read()
                if b[:2] in(b'II',b'MM'): open(f,'wb').write(b);break
                print('  el servidor devolvió algo que no es TIFF:',b[:100]); time.sleep(5)
            except Exception as e: print('  reintento',i+1,'de',nombre,':',e); time.sleep(5)
        else: raise SystemExit('no se pudo bajar '+nombre+' de NOAA NCEI; probá de nuevo en un rato')
    a=np.array(Image.open(f),dtype=np.float32)
    malos=~np.isfinite(a)|(np.abs(a)>12000);a[malos]=0   # sin dato → 0
    if malos.mean()>0.05 or (a==0).mean()>0.6: print('  aviso: %s trae %.0f%% de celdas sin dato y %.0f%% en cero'%(nombre,malos.mean()*100,(a==0).mean()*100))
    return a
def muestra(a,bbox,lat,lon):
    """Altura en un punto: mínimo de la ventana 3x3 alrededor de la celda (para caer al cauce y no a la ladera)."""
    h,w=a.shape;xmin,ymin,xmax,ymax=bbox
    j=int((lon-xmin)/(xmax-xmin)*(w-1));i=int((ymax-lat)/(ymax-ymin)*(h-1));i=max(0,min(h-1,i));j=max(0,min(w-1,j))
    return float(a[max(i-1,0):i+2,max(j-1,0):j+2].min())

# ---- ríos y rectángulos de vista (mismos que mapa.py / vbPara)
JUEGO=sys.argv[1] if len(sys.argv)>1 else 'cauces'
RIOS=RUTAS.cargar(JUEGO)
for r in RIOS: r['ciudades']=[{'n':n,'pos':p} for n,p in zip(r['nombres'],r['paradas'])]
def rect_vista(pts,minW,margen,asp,extra):
    xs=[px(*p)[0] for p in pts];ys=[px(*p)[1] for p in pts]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys);cx,cy=(x0+x1)/2,(y0+y1)/2
    w=max((x1-x0)*margen,minW);h=max((y1-y0)*margen,minW/asp)
    if w/h<asp: w=h*asp
    else: h=w/asp
    return box(cx-w/2-extra,cy-h/2-extra,cx+w/2+extra,cy+h/2+extra)
VISTA={};NUCLEO={}   # por ruta: unión de sus rectángulos de vista (todos los aspectos) y núcleo (lo que se ve con cualquier aspecto); con cámara por tramo, una ventana por parada
for r in RIOS:
    rr=[];nn=[]
    for pts in RUTAS.vistas(r):
        rv=[rect_vista(pts,3 if r['zona'] else 20,1.3,asp,0.5 if r['zona'] else 3) for asp in ASPECTOS]
        rr+=rv;nn.append(rv[0].intersection(rv[-1]))
    VISTA[r['id']]=unary_union(rr);NUCLEO[r['id']]=unary_union(nn)
ZONAS=sorted({r['zona'] for r in RIOS if r['zona']})
UNION={'mundo':unary_union([VISTA[r['id']] for r in RIOS if not r['zona']])}
for z in ZONAS:
    pts=[p for r in RIOS if r['zona']==z for p in r['curso']+[c['pos'] for c in r['ciudades']]]
    UNION[z]=unary_union([VISTA[r['id']] for r in RIOS if r['zona']==z]+[rect_vista(pts,3,1.25,asp,0.5) for asp in ASPECTOS])

# ---- franjas
def polys(g):
    if g.geom_type=='Polygon': return [g]
    return [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
def franja(a,bbox,umbral):
    """Polígonos (unidades del mapa) donde la altura es ≥ umbral, por contornos rellenos; los huecos se restan por paridad."""
    h,w=a.shape;xmin,ymin,xmax,ymax=bbox
    X=(np.linspace(xmin,xmax,w)+180)/360*1000;Y=(90-np.linspace(ymax,ymin,h))/180*500
    fig=plt.figure();cs=plt.contourf(X,Y,a,levels=[umbral,1e9]);plt.close(fig)
    anillos=[]
    for path in cs.get_paths():
        for poly in path.to_polygons(closed_only=True):
            if len(poly)>=4:
                p=make_valid(Polygon(poly))
                if p.area>0: anillos.append(p)
    anillos.sort(key=lambda p:-p.area)
    niveles={}
    for i,p in enumerate(anillos):
        pt=p.representative_point();d=sum(1 for q in anillos[:i] if q.contains(pt))
        niveles.setdefault(d,[]).append(p)
    g=None
    for d in sorted(niveles):
        u=unary_union(niveles[d]);g=u if g is None else (g.union(u) if d%2==0 else g.difference(u))
    return g if g is not None else MultiPolygon()
def limpiar(g,tol,area_min):
    g=g.simplify(tol,preserve_topology=True);out=[]
    for p in polys(g):
        if p.area<area_min: continue
        out.append(Polygon(p.exterior,[i for i in p.interiors if Polygon(i).area>=area_min]))
    return MultiPolygon(out)
def path_pol(g,dec):
    out=[]
    for p in polys(g):
        out.append('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in p.exterior.coords[:-1])+'Z')
        for i in p.interiors: out.append('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in i.coords[:-1])+'Z')
    return ''.join(out)
def bbox_de(g):
    x0,y0,x1,y1=g.bounds;return (x0*0.36-180,90-y1*0.36,x1*0.36-180,90-y0*0.36)  # unidades del mapa → grados

RELIEVE={}
print('franjas del mundo (ETOPO1)…')
A=dem('ETOPO1_ice_surface',BB_MUNDO,RES_MUNDO,'etopo1_mundo')
RELIEVE['mundo']=[]
for u in NIVELES['mundo']:
    g=limpiar(franja(A,BB_MUNDO,u).intersection(UNION['mundo']),*SIMPL['mundo']);RELIEVE['mundo'].append((u,path_pol(g,DEC['mundo'])))
for z in ZONAS:
    print('franjas de la zona',z,'(mosaico NCEI)…')
    bb=bbox_de(UNION[z]);W=int((bb[2]-bb[0])/RES_CR);H=int((bb[3]-bb[1])/RES_CR)
    B=dem('DEM_all',bb,(W,H),'dem_'+z)
    RELIEVE[z]=[]
    for u in NIVELES[z]:
        g=limpiar(franja(B,bb,u).intersection(UNION[z]),*SIMPL[z]);RELIEVE[z].append((u,path_pol(g,DEC[z])))

# ---- nombres del mundo (Natural Earth 50 m)
def titulo(n):
    n=n.strip()
    if n.isupper():
        chicas={'de','del','la','las','los','y','el','en'};n=' '.join(w.lower() if w.lower() in chicas else w.capitalize() for w in n.lower().split())
    return n[0].upper()+n[1:]
def giro(g):
    """Giro del rótulo (grados, sentido horario, entre -90 y 90) si la forma es alargada; 0 si no."""
    r=g.minimum_rotated_rectangle
    if r.geom_type!='Polygon': return 0
    c=list(r.exterior.coords);lados=[(math.hypot(c[i+1][0]-c[i][0],c[i+1][1]-c[i][1]),c[i],c[i+1]) for i in range(4)]
    largo,(x0,y0),(x1,y1)=max(lados);corto=min(l[0] for l in lados)
    if corto==0 or largo/corto<1.8: return 0
    a=math.degrees(math.atan2(y1-y0,x1-x0))
    if a>90: a-=180
    if a<-90: a+=180
    return int(round(a)) if abs(a)<=60 else 0   # un rótulo casi vertical no se lee: mejor derecho
print('nombres de relieve (Natural Earth 50 m)…')
regiones=[]
for ft in ne('ne_50m_geography_regions_polys'):
    p=ft['properties'];t=CLASES.get(p['FEATURECLA'])
    if not t or not ft['geometry'] or p['SCALERANK']>RANGO_MAX[t]: continue
    nombre=p.get('NAME_ES') or p['NAME']
    if nombre in EXCLUIR or p['NAME'] in EXCLUIR: continue
    regiones.append({'n':titulo(nombre),'t':t,'s':p['SCALERANK'],'g':proj(make_valid(shape(ft['geometry'])))})
NOMBRES=[]
for reg in regiones:
    v={}
    for r in RIOS:
        if r['zona']: continue
        vista=VISTA[r['id']]
        if not reg['g'].intersects(vista): continue
        c=reg['g'].intersection(vista)
        if c.is_empty or c.area<1.5: continue
        curso=LineString([px(*p) for p in r['curso']]);w=vista.bounds[2]-vista.bounds[0]
        if (reg['s']>2 or r['camara']=='tramo') and c.distance(curso)>(0.04 if reg['s']>3 else 0.12)*w: continue   # con cámara por tramo, solo lo que queda cerca del camino
        cn=reg['g'].intersection(NUCLEO[r['id']])   # el ancla va en la parte visible con cualquier aspecto de pantalla, si la hay
        pt=(cn if cn.area>=1 else c).representative_point();v[r['id']]=(pt,c.area,giro(cn if cn.area>=1 else c))
    if v: NOMBRES.append({'n':reg['n'],'t':reg['t'],'s':reg['s'],'v':v})
# tope por vista y sin nombres repetidos en la misma vista (p. ej. dos «Meseta Brasileña»)
for r in RIOS:
    if r['zona']: continue
    cands=[x for x in NOMBRES if r['id'] in x['v']];cands.sort(key=lambda x:(x['s'],-x['v'][r['id']][1]))
    vistos=set();quedan=[]
    for x in cands:
        if x['n'] in vistos or len(quedan)>=TOPE_POR_VISTA: x['v'].pop(r['id']);continue
        vistos.add(x['n']);quedan.append(x)
NOMBRES=[x for x in NOMBRES if x['v']]
def latlon(pt): return [round(90-pt.y*0.36,2),round(pt.x*0.36-180,2)]
salida_nombres=[{'n':x['n'],'t':x['t'],'z':'mundo','v':{rid:latlon(pt)+([a] if a else []) for rid,(pt,area,a) in x['v'].items()}} for x in NOMBRES]

# ---- nombres y picos de Costa Rica
def picos_osm():
    f=os.path.join(NE,'osm_picos_'+hashlib.md5(OSM_Q.encode('utf8')).hexdigest()[:8]+'.json')
    if not os.path.exists(f):
        for url in ('https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter'):
            try:
                req=urllib.request.Request(url,data=urllib.parse.urlencode({'data':OSM_Q}).encode(),headers=UA)
                raw=urllib.request.urlopen(req,timeout=300).read()
                if raw.lstrip().startswith(b'{'): open(f,'wb').write(raw);break
                print('  Overpass devolvió algo que no es JSON desde',url); time.sleep(5)
            except Exception as e: print('  Overpass falló en',url,':',e); time.sleep(5)
        else: return None
    out={}
    for e in json.load(open(f,encoding='utf8'))['elements']:
        t=e.get('tags',{});n=llano(t.get('name',''));ele=t.get('ele','').replace(',','.')
        for p in PICOS_CR:
            if n in (llano(p),'volcan '+llano(p),'cerro '+llano(p)) and ele.replace('.','',1).isdigit():
                if p not in out or int(float(ele))>out[p][1]: out[p]=([round(e['lat'],3),round(e['lon'],3)],int(float(ele)))
    return out
picos=(picos_osm() if 'cr' in ZONAS else None) or {}
faltan=[p for p in PICOS_CR if p not in picos]
if faltan and 'cr' in ZONAS: print('  picos sin nodo en OpenStreetMap, con posición de respaldo:',faltan)
for p in (PICOS_CR if 'cr' in ZONAS else []):
    pos=(picos.get(p) or PICOS_ALTURA[p])[0];ele=PICOS_ALTURA[p][1]
    if p in picos and abs(picos[p][1]-ele)>25: print('  aviso: %s mide %d m en OpenStreetMap y %d m en la altura publicada que usa el juego'%(p,picos[p][1],ele))
    salida_nombres.append({'n':p,'t':'pico','z':'cr','p':pos,'e':ele})
for n,t,pos,a in (CR_NOMBRES if 'cr' in ZONAS else []): salida_nombres.append({'n':n,'t':t,'z':'cr','p':pos,**({'a':a} if a else {})})

# ---- perfiles de altura
def dp(pts,tol):  # Douglas-Peucker sobre [(x,y)] normalizados
    if len(pts)<3: return pts
    (x0,y0),(x1,y1)=pts[0],pts[-1];dx,dy=x1-x0,y1-y0;L=math.hypot(dx,dy) or 1
    d=[abs(dy*(x-x0)-dx*(y-y0))/L for x,y in pts];i=max(range(1,len(pts)-1),key=lambda k:d[k])
    if d[i]>tol: return dp(pts[:i+1],tol)[:-1]+dp(pts[i:],tol)
    return [pts[0],pts[-1]]
ALTURAS={};PARADAS={}
print('perfiles…')
for r in RIOS:
    if r['tipo']!='rio': continue   # el perfil de altura es de los ríos; los viajes llevan línea de tiempo
    z=r['zona'] or 'mundo';pts=r['curso'];m=0.05 if r['zona'] else 0.3
    la=[p[0] for p in pts];lo=[p[1] for p in pts];bb=(min(lo)-m,min(la)-m,max(lo)+m,max(la)+m)
    res=RES_PERFIL[z];W=min(int((bb[2]-bb[0])/res),6000);H=max(int(W*(bb[3]-bb[1])/(bb[2]-bb[0])),8)
    a=dem('DEM_global_mosaic',bb,(W,H),'dem_rio_'+r['id'])
    acum=[0.0]
    for i in range(1,len(pts)): acum.append(acum[-1]+hav(pts[i-1],pts[i]))
    total=acum[-1];alts=[muestra(a,bb,*p) for p in pts]
    piso=BAJO_MAR.get(r['id'],0);alts=[max(x,piso) for x in alts]
    for i in range(1,len(alts)): alts[i]=min(alts[i],alts[i-1])       # el río no sube
    alts[-1]=piso                                                     # el último vértice está en el mar
    # vértice de cada parada, igual que motor.js: el más cercano, sin retroceder
    idx=[];ult=0
    for c in r['ciudades']:
        best=ult;bd=1e9
        for i in range(ult,len(pts)):
            d=(pts[i][0]-c['pos'][0])**2+(pts[i][1]-c['pos'][1])**2
            if d<bd: bd=d;best=i
        idx.append(best);ult=best
    top=max(alts[0],1);norm=[(acum[i]/total,alts[i]/top) for i in range(len(pts))]
    tol=0.012;simp=dp(norm,tol)
    while len(simp)>40: tol*=1.5;simp=dp(norm,tol)
    quedan=sorted(set([norm.index(p) for p in simp]+idx+[0,len(pts)-1]))
    ALTURAS[r['id']]=[[round(acum[i]/total,3),int(round(alts[i]))] for i in quedan]
    PARADAS[r['id']]=[(c['n'],int(round(alts[k]))) for c,k in zip(r['ciudades'],idx)]
    print('  %-11s fuente %5d m → %s → mar %d m  (%d puntos)'%(r['id'],alts[0],' · '.join('%s %d'%x for x in PARADAS[r['id']]),alts[-1],len(quedan)))

# ---- salida
def js(v): return json.dumps(v,ensure_ascii=False,separators=(',',':'))
cab='// Generado por tools/relieve.py: no editar a mano. Alturas de ETOPO1 y del mosaico DEM de NOAA NCEI; nombres de Natural Earth 50 m y OpenStreetMap.\n'
rel='const RELIEVE={'+','.join(f'{z}:['+','.join(f'[{u},"{d}"]' for u,d in RELIEVE[z])+']' for z in RELIEVE)+'};\n'
nom='const NOMBRES_RELIEVE='+js(salida_nombres)+';\n'
per='const ALTURAS={'+','.join(f'{k}:'+js(v) for k,v in ALTURAS.items())+'};\n'
open(os.path.join(RAIZ,'src','data','relieve'+RUTAS.sufijo(JUEGO)+'.js'),'w',encoding='utf8').write(cab+rel+nom+per)
print('relieve'+RUTAS.sufijo(JUEGO)+'.js: franjas %d KB (%s), nombres %d KB (%d etiquetas), perfiles %d KB'%(len(rel)//1024,', '.join('%s %d KB'%(z,sum(len(d) for u,d in RELIEVE[z])//1024) for z in RELIEVE),len(nom)//1024,len(salida_nombres),len(per)//1024))
for r in RIOS:
    if not r['zona']: print('  %-10s %2d nombres: %s'%(r['id'],sum(1 for x in salida_nombres if x.get('v') and r['id'] in x['v']),', '.join(x['n'] for x in salida_nombres if x.get('v') and r['id'] in x['v'])))
