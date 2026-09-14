"""Rutas de un juego para las herramientas de Python (mapa.py, relieve.py, verificacion.py).

cargar(juego, edicion) devuelve, por ruta (la edición amplia, por defecto, es la fuente entera; la económica recorta lo
envuelto en /*@amplia*/ … /*@fin:amplia*/ igual que build.js; sufijo(juego, edicion) nombra los archivos generados): id, tipo, zona, camara, curso (trazo concatenado, [lat, lon]), paradas ([lat, lon]) e
idx (vértice de cada parada, como lo calcula motor.js: el más cercano sin retroceder). vistas(r) devuelve los conjuntos
de puntos que el motor puede mostrar de esa ruta: la ruta entera, o, con camara 'tramo', una ventana por parada (del
vértice de la parada anterior al de la siguiente), que es lo que vbPara encuadra en Descender.
"""
import json,os,re,subprocess
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGOS={'cauces':('rios.js',"RIVERS.map(r=>({id:r.id,nombre:r.nombre,tipo:'rio',zona:r.zona||null,camara:'toda',curso:r.curso,paradas:r.ciudades.map(c=>c.pos),nombres:r.ciudades.map(c=>c.nombre)}))"),
        'exploradores':('itinerarios.js',"ITINERARIOS.map(r=>({id:r.id,nombre:r.nombre,tipo:r.tipo,zona:r.zona||null,camara:r.camara||'toda',curso:[].concat(...r.trazo),paradas:r.paradas.map(c=>c.pos),nombres:r.paradas.map(c=>c.nombre)}))")}
DATOS={'cauces':'rios.js','exploradores':'itinerarios.js'}
MARCA=re.compile(r'/\*@amplia\*/.*?/\*@fin:amplia\*/\n?',re.S)
def cortar(js,edicion='amplia'):
    """Lo envuelto en /*@amplia*/ … /*@fin:amplia*/ solo va en la edición amplia (el mismo corte que hace build.js)."""
    return re.sub(r'/\*@(?:fin:)?amplia\*/\n?','',js) if edicion=='amplia' else MARCA.sub('',js)
def sufijo(juego,edicion='economica'): return ('' if juego=='cauces' else '-'+juego)+('-amplia' if edicion=='amplia' else '')
def cargar(juego='cauces',edicion='amplia'):
    archivo,expr=JUEGOS[juego]
    js=cortar(open(os.path.join(RAIZ,'src','data',archivo),encoding='utf8').read(),edicion)+';console.log(JSON.stringify('+expr+'))'
    rutas=json.loads(subprocess.run(['node'],input=js,capture_output=True,text=True,encoding='utf8').stdout)  # por stdin: en Windows el argumento sería demasiado largo
    for r in rutas:
        idx=[];ult=0
        for c in r['paradas']:
            best=ult;bd=1e9
            for i in range(ult,len(r['curso'])):
                d=(r['curso'][i][0]-c[0])**2+(r['curso'][i][1]-c[1])**2
                if d<bd: bd=d;best=i
            idx.append(best);ult=best
        r['idx']=idx
    return rutas
def partir(pts):
    """Una vista que cruza el antimeridiano (más de 180° de ancho) se parte en su lado oeste y su lado este."""
    lons=[p[1] for p in pts]
    if not pts or max(lons)-min(lons)<=180: return [pts]
    return [[p for p in pts if p[1]<0],[p for p in pts if p[1]>=0]]
def vistas(r):
    if r['camara']!='tramo': return partir(r['curso']+r['paradas'])
    n=len(r['paradas']);ult=len(r['curso'])-1
    def idx(p): return 0 if p<=0 else ult if p>n else r['idx'][p-1]
    return [v for p in range(0,n+2) for v in partir(r['curso'][idx(p-1):idx(p+1)+1])]
