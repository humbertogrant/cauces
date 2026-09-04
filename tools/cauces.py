"""Genera los cauces reales de src/data/rios.js (curso y brazos) a partir de Natural Earth ne_50m_rivers_lake_centerlines.

Uso: python tools/cauces.py            (requiere: pip install shapely; descarga el GeoJSON a tools/ne/ la primera vez)
Por río, CAUCES dice de qué capa salen los tramos (capa: ne50 por defecto, ne10, ne10na u osm) y cuáles forman el cauce
(nombres, se comparan con name, name_en y name_alt; en osm con el name del way; un nombre con prefijo, 'ne10:Tuotuo',
sale de otra capa), con dec decimales, simpl grados de
simplificación y, para capas finas, tol (extremos que son el mismo nudo) y puente (hueco máximo que se puentea) más chicos,
dónde empieza y termina (desde, hasta, en [lat,lon]) y, donde Natural Earth no llega, una cabeza o una cola dibujadas
a mano (fuentes, estuarios, deltas). Los tramos (ríos y las "lake centerlines" de lagos y embalses) se enlazan en un
grafo por sus extremos; los huecos menores de PUENTE grados se puentean con una recta penalizada, y el cauce es el
camino más corto de desde a hasta, simplificado a SIMPL grados y redondeado a dos decimales. Los brazos son otros
caminos del mismo grafo o listas de puntos a mano. Reescribe solo las líneas curso:[...] y brazos:[...] de cada río.
Los brazos se empalman solos al cauce o a otro brazo si quedan a menos de 0,2° (empalmar). Imprime por río los vértices,
los km de la polilínea, el salto máximo entre vértices, a cuántos grados queda cada brazo y la distancia de cada ciudad
al vértice más cercano (en grados).
"""
import json,os,math,heapq,subprocess,urllib.request,hashlib
from shapely.geometry import LineString,Point

RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE=os.path.join(RAIZ,'tools','ne'); os.makedirs(NE,exist_ok=True)
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
TOL=0.02      # grados: extremos más cerca que esto son el mismo nudo
PUENTE=1.2    # grados: huecos menores se puentean con una recta (peso ×8)
SIMPL=0.02    # grados: tolerancia de simplificación (Douglas-Peucker)

CAUCES={
 'nilo':{'nombres':['Victoria Nile','Albert Nile','Mountain Nile','White Nile','Nile','Rosetta Branch'],'desde':[0.42,33.2],'hasta':[31.45,30.4],
   'brazos':[{'nombres':['Blue Nile'],'desde':[12.0,37.3],'hasta':[15.63,32.49]}]},
 'amazonas':{'nombres':['Ucayali','Amazonas'],'desde':[-15.5,-71.9],'hasta':[-1.55,-52.66],'cola':[[-1.4,-51.6],[-1.7,-50.5],[-1.81,-49.79],[-1.46,-48.5],[-0.9,-48.2]],
   'brazos':[{'nombres':['Negro'],'desde':[2.06,-70.34],'hasta':[-3.13,-59.9]},{'nombres':['Madeira'],'desde':[-10.39,-65.4],'hasta':[-3.34,-58.69]},[[-1.4,-51.6],[0.03,-51.07],[0.7,-50.0]]]},
 'yangtse':{'nombres':['ne10:Tuotuo','Tongtian','Jinsha','Chang Jiang','Yangtze'],'desde':[34.2,90.8],'hasta':[31.96,120.07],'cola':[[31.8,120.9],[31.23,121.47],[31.4,122.0]],
   'brazos':[{'nombres':['Han'],'desde':[33.1,107.0],'hasta':[30.58,114.28]}]},
 'misisipi':{'nombres':['Mississippi'],'desde':[47.16,-95.03],'hasta':[28.98,-89.38],'cabeza':[[47.2,-95.2]],
   'brazos':[{'nombres':['Missouri'],'desde':[46.66,-111.7],'hasta':[38.82,-90.13]},{'nombres':['Ohio'],'desde':[40.45,-79.99],'hasta':[36.99,-89.15]}]},
 'danubio':{'nombres':['Danube'],'desde':[47.95,8.5],'hasta':[45.23,28.76],'cola':[[45.2,29.7]],
   'brazos':[{'nombres':['Drava'],'desde':[47.09,13.82],'hasta':[45.56,18.95]},{'nombres':['Tisza'],'desde':[48.1,24.2],'hasta':[45.15,20.3],'cola':[[47.93,21.05],[47.62,20.76],[47.17,20.18],[46.71,20.14],[46.25,20.15],[45.93,20.09],[45.2,20.3]]}]},
 'rin':{'nombres':['Rhein','Rhin','Rhine','Lek','Nieuwe Maas','Noord','Waal','Merwede','Nieuwe Waterweg'],'desde':[46.6,8.7],'hasta':[51.92,4.48],'cola':[[51.98,4.05]],
   'brazos':[[[48.2,6.3],[49.1,6.2],[49.75,6.6],[50.36,7.6]],[[50.1,10.0],[50.1,8.8],[50.0,8.27]]]},
 'ganges':{'nombres':['Ganges'],'desde':[30.15,78.6],'hasta':[21.9,88.1],'cabeza':[[30.99,78.94],[30.73,78.44],[30.38,78.48]],'cola':[[21.9,88.1]],
   'brazos':[{'nombres':['Ganges'],'desde':[24.83,87.92],'hasta':[22.75,90.44]},{'nombres':['Brahmaputra'],'desde':[28.0,95.4],'hasta':[23.85,89.75]}]},
 'volga':{'nombres':['Volga'],'desde':[57.25,32.5],'hasta':[45.8,47.9],
   'brazos':[{'nombres':['Kama'],'desde':[58.21,53.69],'hasta':[55.11,49.25]}]},
 'tigris':{'nombres':['Dicle','Tigris','Shatt al Arab'],'desde':[38.4,40.0],'hasta':[29.95,48.55],
   'brazos':[{'nombres':['Firat','Fırat','Euphrates','Al Furat','Furat'],'desde':[38.8,39.7],'hasta':[30.97,47.47]}]},
 'mekong':{'nombres':['ne10:Za','Lancang','Mekong'],'desde':[33.2,94.1],'hasta':[10.0,105.83],'cola':[[9.6,106.5]],
   'brazos':[{'nombres':['Mekong'],'desde':[11.59,104.95],'hasta':[10.22,106.14]},[[13.0,103.9],[12.3,104.3],[11.56,104.92]]]},
 'niger':{'nombres':['Niger'],'desde':[9.1,-10.7],'hasta':[5.36,6.45],'cola':[[4.9,6.7],[4.82,7.05],[4.4,7.15]],
   'brazos':[{'nombres':['Benue'],'desde':[9.49,11.92],'hasta':[7.79,6.78]}]},
 'parana':{'nombres':['Paraná'],'desde':[-20.1,-51.0],'hasta':[-33.99,-58.43],'cola':[[-34.6,-58.38],[-34.9,-56.16],[-35.4,-55.5]],
   'brazos':[{'nombres':['Paraná'],'desde':[-16.0,-57.7],'hasta':[-27.31,-58.6]}]},
 'indo':{'nombres':['ne10:Shiquan','Indus'],'desde':[31.4,81.6],'hasta':[24.04,67.45],'brazos':[]},
 # Costa Rica (zona 'cr'): Natural Earth 50 m no los trae. Reventazón: NE 10 m Norteamérica; San Juan: NE 10 m global;
 # Tempisque y Sarapiquí (y los afluentes): OpenStreetMap. Tres decimales y simplificación de 0,003° porque el mapa se acerca mucho.
 'tempisque':{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Tempisque'],'desde':[10.73,-85.5],'hasta':[10.18,-85.24],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Liberia'],'desde':[10.78,-85.33],'hasta':[10.47,-85.55],'dec':3,'simpl':0.003},{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Bebedero'],'desde':[10.37,-85.19],'hasta':[10.25,-85.25],'dec':3,'simpl':0.003}]},
 'reventazon':{'capa':'ne10na','tol':0.002,'puente':0.1,'nombres':['Reventazón'],'desde':[9.68,-83.8],'hasta':[10.3,-83.33],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Parismina'],'desde':[10.06,-83.72],'hasta':[10.31,-83.38],'dec':3,'simpl':0.003}]},
 'sarapiqui':{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Sarapiquí'],'desde':[10.17,-84.17],'hasta':[10.716,-83.9375],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Rio Puerto Viejo','Río Puerto Viejo'],'desde':[10.21,-84.06],'hasta':[10.4541,-84.0083],'dec':3,'simpl':0.003}]},
 'sanjuan':{'capa':'ne10','tol':0.002,'puente':0.1,'nombres':['San Juan'],'desde':[11.1231,-84.7783],'hasta':[10.93,-83.69],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Colorado'],'desde':[10.735,-83.7385],'hasta':[10.7713,-83.5964],'dec':3,'simpl':0.003},{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río San Carlos'],'desde':[10.37,-84.54],'hasta':[10.7815,-84.1987],'dec':3,'simpl':0.003}]},
 # Tárcoles: el cauce sigue el Virilla (Coronado → Heredia → Belén) y desde Balsa el Grande de Tárcoles; el río Grande es afluente.
 'tarcoles':{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Virilla','Río Grande de Tárcoles'],'desde':[9.98,-84.0],'hasta':[9.78,-84.64],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río Grande'],'desde':[10.1,-84.44],'hasta':[9.943,-84.379],'dec':3,'simpl':0.003}]},
 # Térraba: río General desde el valle de Pérez Zeledón y, desde Paso Real, Grande de Térraba; el Coto Brus es afluente.
 'terraba':{'capa':'osm','tol':0.0005,'puente':0.03,'nombres':['Río General','Río Grande de Térraba'],'desde':[9.45,-83.75],'hasta':[8.93,-83.6],'dec':3,'simpl':0.003,
   'brazos':[{'capa':'osm','tol':0.0005,'puente':0.15,'nombres':['Río Coto Brus'],'desde':[8.95,-82.99],'hasta':[9.0058,-83.225],'dec':3,'simpl':0.003}]},  # los tramos del Coto Brus en OSM tienen huecos: puente más largo
}

def ne(nombre):
    f=os.path.join(NE,nombre+'.geojson')
    if not os.path.exists(f): urllib.request.urlretrieve(URL+nombre+'.geojson',f)
    return json.load(open(f,encoding='utf8'))['features']
CAPAS={'ne50':'ne_50m_rivers_lake_centerlines','ne10':'ne_10m_rivers_lake_centerlines','ne10na':'ne_10m_rivers_north_america'}
_cache={}
OSM_Q='''[out:json][timeout:180];
(
  way["waterway"="river"]["name"~"Tempisque|Sarapiqu|Bebedero|Parismina|Grande de Orosi|Macho$|Colorado$|San Carlos$|Liberia$|Puerto Viejo$|Grande de T.rcoles|Virilla|^R.o Grande$|Grande de T.rraba|^R.o General$|Coto Brus"](8.7,-86.0,11.3,-83.0);
);
out geom;'''
def osm():
    """Ríos y pueblos de Costa Rica desde OpenStreetMap (Overpass), guardados en tools/ne/osm_cr.json."""
    f=os.path.join(NE,'osm_cr_'+hashlib.md5(OSM_Q.encode('utf8')).hexdigest()[:8]+'.json')  # cambia si cambia la consulta
    if not os.path.exists(f):
        import urllib.parse,time
        for url in ('https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter'):
            try:
                req=urllib.request.Request(url,data=urllib.parse.urlencode({'data':OSM_Q}).encode(),headers={'User-Agent':'cauces (juego educativo de un solo archivo)'})
                raw=urllib.request.urlopen(req,timeout=300).read()
                if raw.lstrip().startswith(b'{'): open(f,'wb').write(raw); break
                print('  Overpass devolvió algo que no es JSON desde',url,'; reintento en otro servidor'); time.sleep(5)
            except Exception as e: print('  Overpass falló en',url,':',e); time.sleep(5)
        else: raise SystemExit('no se pudo bajar OpenStreetMap (Overpass); probá de nuevo en un rato')
    return json.load(open(f,encoding='utf8'))['elements']
def partes_de(nombres,capa='ne50'):
    """Tramos de los nombres dados; un nombre puede llevar prefijo de capa ('ne10:Tuotuo') para mezclar fuentes."""
    grupos={}
    for n in nombres:
        c,nom=(n.split(':',1) if ':' in n and n.split(':',1)[0] in CAPAS or n.startswith('osm:') else (capa,n))
        grupos.setdefault(c,[]).append(nom)
    out=[]
    for c,noms in grupos.items(): out+=_partes(noms,c)
    return out
def _partes(nombres,capa):
    out=[]
    if capa=='osm':
        for e in osm():
            if e['type']=='way' and e.get('tags',{}).get('name') in nombres and e.get('geometry'):
                out.append([(p['lon'],p['lat']) for p in e['geometry']])
        return [p for p in out if len(p)>=2]
    if capa not in _cache: _cache[capa]=ne(CAPAS[capa])
    for ft in _cache[capa]:
        p=ft['properties']; g=ft['geometry']
        if g and any(p.get(k) in nombres for k in ('name','name_en','name_alt')):
            cs=[g['coordinates']] if g['type']=='LineString' else g['coordinates']
            out+= [[tuple(c) for c in cc] for cc in cs if len(cc)>=2]
    return out
def hav(a,b):  # km entre dos (lon,lat)
    R=6371; la1,la2=math.radians(a[1]),math.radians(b[1]); dl=math.radians(b[0]-a[0]); dn=la2-la1
    q=math.sin(dn/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(q))
dist=lambda a,b:math.hypot(a[0]-b[0],a[1]-b[1])
largo=lambda p:sum(hav(p[i-1],p[i]) for i in range(1,len(p)))

def camino(nombres,desde,hasta,capa='ne50',tol=TOL,puente=PUENTE):
    """Camino más corto por los tramos de la capa entre desde y hasta ([lat,lon]); devuelve [(lon,lat),...]."""
    partes=partes_de(nombres,capa)
    if not partes: raise SystemExit('sin tramos para '+', '.join(nombres))
    objetivos=[(desde[1],desde[0]),(hasta[1],hasta[0])]
    for o in objetivos:  # el vértice más cercano a cada extremo pasa a ser un nudo
        pi,vi=min(((k,i) for k,p in enumerate(partes) for i in range(len(p))),key=lambda kv:dist(partes[kv[0]][kv[1]],o))
        if 0<vi<len(partes[pi])-1: p=partes[pi]; partes[pi]=p[:vi+1]; partes.append(p[vi:])
    cambio=True  # donde el extremo de un tramo toca el interior de otro, se parte el otro
    while cambio:
        cambio=False; extremos=[p[0] for p in partes]+[p[-1] for p in partes]
        for k,p in enumerate(partes):
            for vi in range(1,len(p)-1):
                if any(dist(p[vi],e)<tol for e in extremos): partes[k]=p[:vi+1]; partes.append(p[vi:]); cambio=True; break
            if cambio: break
    nudos=[]
    def nudo(pt):
        for i,n in enumerate(nudos):
            if dist(pt,n)<tol: return i
        nudos.append(pt); return len(nudos)-1
    aristas={}
    for p in partes:
        a,b=nudo(p[0]),nudo(p[-1])
        if a==b: continue
        w=largo(p)
        for x,y,c in ((a,b,p),(b,a,p[::-1])):
            if (x,y) not in aristas or aristas[(x,y)][0]>w: aristas[(x,y)]=(w,c)
    puentes=set()
    for i in range(len(nudos)):
        for j in range(i+1,len(nudos)):
            if (i,j) not in aristas and dist(nudos[i],nudos[j])<puente:
                w=hav(nudos[i],nudos[j])*8; aristas[(i,j)]=(w,[nudos[i],nudos[j]]); aristas[(j,i)]=(w,[nudos[j],nudos[i]]); puentes.add((i,j)); puentes.add((j,i))
    ini=min(range(len(nudos)),key=lambda i:dist(nudos[i],objetivos[0])); fin=min(range(len(nudos)),key=lambda i:dist(nudos[i],objetivos[1]))
    ady={}
    for (a,b),(w,c) in aristas.items(): ady.setdefault(a,[]).append((b,w))
    costo={ini:0}; previo={}; cola=[(0,ini)]
    while cola:
        d,u=heapq.heappop(cola)
        if u==fin: break
        if d>costo.get(u,1e18): continue
        for v,w in ady.get(u,[]):
            if d+w<costo.get(v,1e18): costo[v]=d+w; previo[v]=u; heapq.heappush(cola,(d+w,v))
    if fin not in costo: raise SystemExit(f'sin camino entre {desde} y {hasta} por {nombres}')
    ruta=[fin]
    while ruta[-1]!=ini: ruta.append(previo[ruta[-1]])
    ruta.reverse(); pts=[]; kmp=0; np=0
    for a,b in zip(ruta,ruta[1:]):
        c=aristas[(a,b)][1]; pts+= c if not pts else c[1:]
        if (a,b) in puentes: np+=1; kmp+=hav(c[0],c[-1])
    if np: print(f"          aviso: {np} puente{'s' if np>1 else ''} en recta ({kmp:.0f} km) entre {nombres}")
    return pts

def redondear(pts,dec=2):  # [(lon,lat)] → [[lat,lon]] con dec decimales y sin repetidos
    out=[]
    for x,y in pts:
        q=[round(y,dec)+0.0,round(x,dec)+0.0]
        if not out or out[-1]!=q: out.append(q)
    return out
def proyectar(pts,ciudades):
    """Inserta en la polilínea el punto más cercano a cada ciudad: la simplificación deja tramos rectos con vértices a
    40-50 km, y motor.js ancla cada parada a un vértice, así que cada ciudad necesita el suyo justo enfrente."""
    line=LineString(pts); acum=[0.0]
    for i in range(1,len(pts)): acum.append(acum[-1]+dist(pts[i-1],pts[i]))
    extra=[]
    for nombre,pos in ciudades:
        d=line.project(Point(pos[1],pos[0])); q=line.interpolate(d); extra.append((d,(q.x,q.y)))
    out=[]
    for a,p in sorted(list(zip(acum,pts))+extra,key=lambda t:t[0]):
        if not out or dist(out[-1],p)>1e-6: out.append(p)
    return out
def linea(spec,ciudades=()):
    if isinstance(spec,list): return [[float(a),float(b)] for a,b in spec]  # a mano, tal cual
    pts=camino(spec['nombres'],spec['desde'],spec['hasta'],spec.get('capa','ne50'),spec.get('tol',TOL),spec.get('puente',PUENTE))
    pts=list(LineString(pts).simplify(spec.get('simpl',SIMPL),preserve_topology=False).coords)
    if ciudades: pts=proyectar(pts,ciudades)
    return [[float(a),float(b)] for a,b in spec.get('cabeza',[])]+redondear(pts,spec.get('dec',2))+[[float(a),float(b)] for a,b in spec.get('cola',[])]
def empalmar(brazos,curso):
    """Une el extremo más cercano de cada brazo al cauce (o a otro brazo del mismo río) si queda a menos de 0,1°:
    las fuentes difieren (50 m, 10 m, OSM) y los afluentes quedaban a unos km del cauce."""
    out=[]
    for i,b in enumerate(brazos):
        otros=[L for j,L in enumerate([curso]+brazos) if j!=i+1 and len(L)>=2]
        lineas=[LineString([(p[1],p[0]) for p in L]) for L in otros]
        def cerca(pt):
            P=Point(pt[1],pt[0]); mejor=None
            for L in lineas:
                d=L.distance(P)
                if mejor is None or d<mejor[0]: q=L.interpolate(L.project(P)); mejor=(d,[round(q.y,3),round(q.x,3)])
            return mejor
        c0,c1=cerca(b[0]),cerca(b[-1])
        if c0 and c1:
            if c1[0]<=c0[0]:
                if 0.0005<c1[0]<0.2: b=b+[c1[1]]
            elif 0.0005<c0[0]<0.2: b=[c0[1]]+b
        out.append(b)
    return out
def suelto(b,curso,brazos):  # distancia (grados) del brazo al cauce o a otro brazo, por su extremo más cercano
    lineas=[LineString([(p[1],p[0]) for p in L]) for L in [curso]+[x for x in brazos if x is not b] if len(L)>=2]
    return min(min(L.distance(Point(p[1],p[0])) for L in lineas) for p in (b[0],b[-1]))
def fmt_pt(p): return '['+','.join(('%.3f'%v).rstrip('0').rstrip('.') if v%1 else str(int(v)) for v in p)+']'
def fmt(pts): return '['+','.join(fmt_pt(p) for p in pts)+']'

ruta_rios=os.path.join(RAIZ,'src','data','rios.js')
texto=open(ruta_rios,encoding='utf8',newline='').read()
dump=subprocess.run(['node'],input=texto+";console.log(JSON.stringify(RIVERS.map(r=>({id:r.id,longitud:r.longitud,ciudades:r.ciudades.map(c=>[c.nombre,c.pos])}))))",capture_output=True,text=True,encoding='utf8').stdout
rios={r['id']:r for r in json.loads(dump)}
total=0
for rid,spec in CAUCES.items():
    r=rios[rid]; curso=linea(spec,r['ciudades']); brazos=empalmar([linea(b) for b in spec.get('brazos',[])],curso)
    km=largo([(p[1],p[0]) for p in curso]); salto=max(hav((a[1],a[0]),(b[1],b[0])) for a,b in zip(curso,curso[1:]))
    empalmes=', '.join(f'{suelto(b,curso,brazos):.3f}°' for b in brazos)
    ult=0; dists=[]
    for nombre,pos in r['ciudades']:  # misma regla que motor.js: vértice más cercano, sin retroceder
        best=min(range(ult,len(curso)),key=lambda i:dist(curso[i],pos)); ult=best; dists.append(f"{nombre} {dist(curso[best],pos):.2f}")
    ctxt,btxt=fmt(curso),('['+','.join(fmt(b) for b in brazos)+']' if brazos else '')
    total+=len(ctxt)+len(btxt)
    print(f"{rid:9} {len(curso):4} vértices, {km:5.0f} km de polilínea ({r['longitud']} km reales), salto máx {salto:.0f} km, brazos {[len(b) for b in brazos]} a {empalmes or '—'}, {(len(ctxt)+len(btxt))//1024} KB")
    print('          '+' · '.join(dists))
    i=texto.index('{id:"%s"'%rid); j=texto.find('\n{id:"',i+1); j=len(texto) if j<0 else j
    bloque=texto[i:j]; a=bloque.index('\ncurso:['); b=bloque.index('\n',a+1); resto=bloque[b:]
    if resto.startswith('\nbrazos:['): resto=resto[resto.index('\n',1):]
    texto=texto[:i]+bloque[:a]+'\ncurso:'+ctxt+','+('\nbrazos:'+btxt+',' if btxt else '')+resto+texto[j:]
cab='// curso y brazos los genera tools/cauces.py a partir de Natural Earth (50 m); no editarlos a mano.\n'
if not texto.startswith('//'): texto=cab+texto
open(ruta_rios,'w',encoding='utf8',newline='').write(texto)
print(f'cursos y brazos: {total//1024} KB en total; rios.js {len(texto.encode("utf8"))//1024} KB')
