"""Regenera src/data/mapa.js (costa, lagos y fronteras) a partir de Natural Earth.

Uso: python3 tools/mapa.py            (requiere: pip install shapely; descarga los GeoJSON a tools/ne/ la primera vez)
Costa: 110 m fuera de las cuencas de los ríos, 50 m dentro, y 10 m en las cuencas de los ríos de una zona (Costa Rica),
donde el mapa se acerca mucho más; lagos y fronteras 50 m dentro de las cuencas y 10 m en las zonas.
Proyección equirectangular al viewBox 1000x500: x=(lon+180)/360*1000, y=(90-lat)/180*500.
Las "cuencas" son los rectángulos de vista de cada río (los mismos que calcula vbPara en motor.js: ancho mínimo 20
unidades, 3 en los ríos de zona) para aspectos 1.0 y 2.4, así la costa fina cubre lo que se ve al abrir un río en
teléfono o en pantalla ancha. Las piezas de 10 m se escriben aparte y con tres decimales (0,001 unidad ≈ 40 m).
"""
import json,os,subprocess,urllib.request
from shapely.geometry import shape,box,MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE=os.path.join(RAIZ,'tools','ne'); os.makedirs(NE,exist_ok=True)
URL='https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/'
def ne(nombre):
    f=os.path.join(NE,nombre+'.geojson')
    if not os.path.exists(f): urllib.request.urlretrieve(URL+nombre+'.geojson',f)
    return [shape(ft['geometry']) for ft in json.load(open(f,encoding='utf8'))['features'] if ft['geometry']]
def proj(g): return affinity.affine_transform(g,[1000/360,0,0,-500/180,500,250])

rios_js=open(os.path.join(RAIZ,'src','data','rios.js'),encoding='utf8').read()
dump=subprocess.run(['node'],input=rios_js+";console.log(JSON.stringify(RIVERS.map(r=>({zona:r.zona||null,curso:r.curso,ciudades:r.ciudades.map(c=>c.pos)}))))",capture_output=True,text=True,encoding='utf8').stdout  # por stdin: en Windows el argumento sería demasiado largo
rects={'fino':[],'zona':[]}
for r in json.loads(dump):
    pts=r['curso']+r['ciudades']
    xs=[(p[1]+180)/360*1000 for p in pts]; ys=[(90-p[0])/180*500 for p in pts]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys); cx,cy=(x0+x1)/2,(y0+y1)/2
    minW,margen=(3,0.5) if r['zona'] else (20,3)
    for asp in (1.0,2.4):
        w=max((x1-x0)*1.3,minW); h=max((y1-y0)*1.35,minW/asp)
        if w/h<asp: w=h*asp
        else: h=w/asp
        rects['zona' if r['zona'] else 'fino'].append(box(cx-w/2-margen,cy-h/2-margen,cx+w/2+margen,cy+h/2+margen))
fino=unary_union(rects['fino']); zona=unary_union(rects['zona']) if rects['zona'] else box(-10,-10,-9,-9)

def polys(g):
    if g.geom_type=='Polygon': return [g]
    if g.geom_type=='MultiPolygon': return list(g.geoms)
    return [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
def lineas(g):
    if g.geom_type=='LineString': return [g]
    return [l for x in getattr(g,'geoms',[]) for l in lineas(x)]
def dentro(nombre):  # piezas de Natural Earth 10 m que tocan la zona, ya proyectadas
    return [g for g in (proj(x) for x in ne(nombre)) if g.intersects(zona)]

land110=unary_union([proj(g) for g in ne('ne_110m_land')]).buffer(0)
land50=unary_union([proj(g) for g in ne('ne_50m_land')]).buffer(0)
mundo=box(0,0,1000,470)  # sin Antártida
grueso=land110.intersection(mundo).difference(fino).difference(zona).simplify(1.4,preserve_topology=True)
finoLand=land50.intersection(fino).difference(zona).simplify(0.3,preserve_topology=True)
land=unary_union([grueso,finoLand]).buffer(0)
land=MultiPolygon([p for p in polys(land) if p.area>=(2 if fino.intersects(p) else 12)])
land10=unary_union(dentro('ne_10m_land')).buffer(0).intersection(zona).simplify(0.015,preserve_topology=True)
land10=MultiPolygon([p for p in polys(land10) if p.area>=0.002])
lagos=unary_union([proj(g) for g in ne('ne_50m_lakes')]).intersection(fino).difference(zona).simplify(0.3,preserve_topology=True)
lagos=MultiPolygon([p for p in polys(lagos) if p.area>=0.6])
lagos10=unary_union(dentro('ne_10m_lakes')).intersection(zona).simplify(0.015,preserve_topology=True)
lagos10=MultiPolygon([p for p in polys(lagos10) if p.area>=0.001])
bordes=unary_union([proj(g) for g in ne('ne_50m_admin_0_boundary_lines_land')]).intersection(fino).difference(zona).simplify(0.3,preserve_topology=True)
bordes10=unary_union(dentro('ne_10m_admin_0_boundary_lines_land')).intersection(zona).simplify(0.015,preserve_topology=True)

def path_pol(g,dec=1):
    out=[]
    for p in polys(g):
        out.append('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in p.exterior.coords[:-1])+'Z')
        for i in p.interiors: out.append('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in i.coords[:-1])+'Z')
    return ''.join(out)
def path_lin(g,dec=1):
    return ''.join('M'+'L'.join(f'{x:.{dec}f} {y:.{dec}f}' for x,y in l.coords) for l in lineas(g))
LAND=path_pol(land)+path_pol(land10,3); LAGOS=path_pol(lagos)+path_pol(lagos10,3); BORDES=path_lin(bordes)+path_lin(bordes10,3)
open(os.path.join(RAIZ,'src','data','mapa.js'),'w',encoding='utf8').write(f'const LAND="{LAND}";const LAGOS="{LAGOS}";const BORDES="{BORDES}";\n')
print(f'costa {len(LAND)//1024} KB (10 m: {len(path_pol(land10,3))//1024} KB), lagos {len(LAGOS)//1024} KB, fronteras {len(BORDES)//1024} KB')
