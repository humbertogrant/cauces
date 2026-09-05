"""Genera docs/verificacion.md: todas las afirmaciones con cifra, fecha o superlativo del contenido, por río.
Uso: python3 tools/verificacion.py. Marca con ⚠ las que contienen las palabras de la lista DUDAS (editable)."""
import json,os,re,subprocess
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=lambda f:open(os.path.join(RAIZ,'src','data',f),encoding='utf8').read()
js=src('rios.js')+src('naves.js')+src('mascotas.js')+src('eventos.js')+";console.log(JSON.stringify({RIVERS,NAVES,MASCOTAS,EVENTOS}))"
d=json.loads(subprocess.run(['node'],input=js,capture_output=True,text=True,encoding='utf8').stdout)  # por stdin: en Windows el argumento sería demasiado largo
R,N,M,E=d['RIVERS'],d['NAVES'],d['MASCOTAS'],d['EVENTOS']
PAT=re.compile(r'\d|siglo|mayor|más grande|más largo|más alto|más ancho|primer|único|más antigu|más transitad|más poblad|más sangrient')
SPLIT=re.compile(r'(?<!\ba\.)(?<!\bc\.)(?<!\bs\.)(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚ¿¡«])')
DUDAS=['Rihla','120 000','madre de ciudades','1258','Abu Said','mejor construidas','Bayalun','Santa Sofía','Tughluq','1341','cauri','Zaitún','juncos','Tagaza','Sulaymán','1355','24 años','Calicut','peste','Niamey','segunda muralla','capitales más cercanas','torre de iglesia','exportador','tamaño de Costa Rica','3 700 km','14 m','cuarto del PIB','60 %','80 %','mercado de algodón','molinos de Budapest','Kamyshin','granero que alimentaba','Inn trae','tejedores','40 castillos','400 millones','Pataliputra','Ilısu','más peligrosa','once presas','mitad del arroz','700 km','90 %','Yacyretá (1994)','3 400 km','tercio de Pakistán','20 millones','66 compuertas','1583','3 500 m','tamaño de Suiza','COP30','2025','Kumbh','más de 100 TWh','1,3 millones','primera gran manufactura','Ver-o-Peso','almacén enorme','tarta más antigua','30 millones','cien camiones','mil camiones','50 kilos','Ergani','lustre','Marajó','144 km','145 km','84 km','192 km','780 m','mundial de 1998','250 m','100 kilos','nueve de cada diez','Cariblanco','años ochenta','más antigua del país','segunda puerta','1833','más lluviosos','miles de patos','Muelle','puerto fluvial','1769','Sardinal','1854','canal que nunca','reconstruido','Solentiname','desde 1942','Guayabo','clase III','4 000 mm','Puente','cacao que sirvió','Ujarrás','Casa del Soñador','Hacienda Juan Viñas','fines de comercio','2015 y 2018','cancelada en 2024','Isla Portillos','1957','70 000','1817','80 km','Kumbh','Repin','Cai Rang','harmatán','sudestada','quinta parte','diez países','111 km','160 km','1958','Intel','1997','Los Tajos','1910','puente de Mulas','balsa','huetares','Fortín','1876','Chirripó','3 820','1979','Del Monte','1938','Finca 6','2014','Diquís','2018','Diablitos','30 de diciembre','esferas','mil años','manglar','siglos IV y XVI','agua grande','primera exportación','más contaminado']
frases=lambda t:[f.strip() for f in SPLIT.split(t) if PAT.search(f)]
out=["# Cauces: lista de verificación de contenido","","Cada línea es una afirmación con cifra, fecha o superlativo tal como aparece en el juego. ⚠ = revisar primero. Se regenera con `python3 tools/verificacion.py`.",""]
for r in R:
    out+= [f"## {r['nombre']} ({r['longitud']:,} km hasta {r['marEn']})".replace(',',' '),""]
    def add(etq,t):
        for f in frases(t): out.append(f"- {etq}: {f}{' ⚠' if any(k in f for k in DUDAS) else ''}")
    add("Nacimiento",r['naceNota']);add("Ruta antigua",r['antigua']);add("Ruta moderna",r['moderna']);add("Pista antigua",r['pistaAntigua']);add("Pista moderna",r['pistaModerna'])
    for c in r['ciudades']:add(f"{c['nombre']} · imagen",c['imagen']);add(f"{c['nombre']} · dato",c['dato'])
    n=N.get(r['id'])
    if n:
        add("Embarcación",n['desc']);add("Zarpe",n['zarpe']);add("Llegada",n['llegada'])
        for c,pu in zip(r['ciudades'],n['puertos']):add(f"{c['nombre']} · puerto (Historia)",pu[0])
    m=M.get(r['id'])
    if m:
        add(f"{m['nombre']} · hola",m['hola']);add(f"{m['nombre']} · mar",m['mar'])
        for c,l in zip(r['ciudades'],m['paradas']):add(f"{m['nombre']} en {c['nombre']}",l)
    for e in E.get(r['id'],[]):
        add(f"Evento · {e['titulo']}",e['texto']);add(f"Evento · {e['titulo']} · bien",e['bien']);add(f"Evento · {e['titulo']} · mal",e['mal'])
    out.append("")
os.makedirs(os.path.join(RAIZ,'docs'),exist_ok=True)
# Exploradores: itinerarios (src/data/itinerarios.js), con vehículo, compañero y eventos dentro de cada ruta
I=json.loads(subprocess.run(['node'],input=src('itinerarios.js')+";console.log(JSON.stringify(ITINERARIOS))",capture_output=True,text=True,encoding='utf8').stdout)
out+=["# Exploradores","","Mismo criterio: cada línea es una afirmación con cifra, fecha o superlativo. El trazo del mapa es ilustrativo (puntos de paso a mano en tools/itinerarios.py); lo verificable son las etapas, sus fechas y los textos.",""]
for r in I:
    out+=[f"## {r['nombre']} ({r['region']}, de {r['inicio']['nombre']} a {r['fin']['en']})",""]
    def add(etq,t):
        for f in frases(t): out.append(f"- {etq}: {f}{' ⚠' if any(k in f for k in DUDAS) else ''}")
    add("Partida",r['inicio']['nota'])
    for cx in r['contexto']: add(cx['titulo'],cx['texto']);add(cx['titulo']+' · pista',cx['pista'])
    for c in r['paradas']: out.append(f"- {c['nombre']} · fecha: {c['fecha']} ⚠");add(f"{c['nombre']} · imagen",c['imagen']);add(f"{c['nombre']} · dato",c['dato'])
    v=r['vehiculo'];add("Vehículo",v['desc']);add("Salida",v['zarpe']);add("Llegada",v['llegada'])
    for c,pu in zip(r['paradas'],v['puertos']): add(f"{c['nombre']} · en el camino (Historia)",pu[0])
    m=r['companero'];add(f"{m['nombre']} · hola",m['hola']);add(f"{m['nombre']} · regreso",m['fin'])
    for c,l in zip(r['paradas'],m['paradas']): add(f"{m['nombre']} en {c['nombre']}",l)
    for e in r.get('eventos',[]): add(f"Evento · {e['titulo']}",e['texto']);add(f"Evento · {e['titulo']} · bien",e['bien']);add(f"Evento · {e['titulo']} · mal",e['mal'])
    out.append("")
# relieve: altura del cauce en cada parada y picos con su altura (src/data/relieve.js, de tools/relieve.py)
js2=src('rios.js')+src('relieve.js')+"""
const hav=(a,b)=>{const R=6371,toR=x=>x*Math.PI/180,dl=toR(b[0]-a[0]),dn=toR(b[1]-a[1]),q=Math.sin(dl/2)**2+Math.cos(toR(a[0]))*Math.cos(toR(b[0]))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(q))};
const alt=(P,f)=>{if(f<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++)if(f<=P[i][0]){const [f0,a0]=P[i-1],[f1,a1]=P[i];return f1>f0?a0+(a1-a0)*(f-f0)/(f1-f0):a1}return P[P.length-1][1]};
const out={};for(const r of RIVERS){const acum=[0];for(let i=1;i<r.curso.length;i++)acum[i]=acum[i-1]+hav(r.curso[i-1],r.curso[i]);const tot=acum[acum.length-1];let ult=0;const P=ALTURAS[r.id];if(!P)continue;
  out[r.id]={fuente:P[0][1],mar:P[P.length-1][1],paradas:r.ciudades.map(c=>{let best=ult,bd=1e9;for(let i=ult;i<r.curso.length;i++){const d=(r.curso[i][0]-c.pos[0])**2+(r.curso[i][1]-c.pos[1])**2;if(d<bd){bd=d;best=i}}ult=best;return [c.nombre,Math.round(alt(P,acum[best]/tot))]})}}
console.log(JSON.stringify({alturas:out,picos:NOMBRES_RELIEVE.filter(x=>x.t==='pico').map(x=>[x.n,x.e])}))"""
rel=json.loads(subprocess.run(['node'],input=js2,capture_output=True,text=True,encoding='utf8').stdout)
out+=["## Relieve: alturas (m) que muestra el juego","","Altura del cauce en cada parada, muestreada del mosaico DEM global de NOAA NCEI sobre el vértice del cauce (no es la altura del pueblo: Juan Viñas está a 1 160 m y el río pasa a 860). Se regenera con `python tools/relieve.py`; contrastar con alturas publicadas. ⚠ = revisar.",""]
for r in R:
    a=rel['alturas'].get(r['id'])
    if a: out.append(f"- {r['nombre']}: fuente {a['fuente']} m → "+" · ".join(f"{n} {m} m" for n,m in a['paradas'])+f" → mar {a['mar']} m ⚠")
out+=["","Volcanes y cerros de Costa Rica (posición de OpenStreetMap; altura publicada, fijada en `PICOS_ALTURA` de tools/relieve.py; OpenStreetMap da 1 440 m para el Orosí y 1 875 m para el Rincón de la Vieja):",""]
out+=[f"- {n}: {e} m ⚠" for n,e in rel['picos']]
out.append("")
open(os.path.join(RAIZ,'docs','verificacion.md'),'w',encoding='utf8',newline='\n').write('\n'.join(out))
print(len(out),'líneas,','\n'.join(out).count('⚠'),'marcadas')
