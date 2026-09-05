"""Regenera el `trazo` de cada itinerario de src/data/itinerarios.js a partir de puntos de paso escritos a mano.

Uso: python tools/itinerarios.py

El trazo es ilustrativo: une, en orden cronológico, las paradas y los lugares por donde el relato dice que pasó, con
arcos de círculo máximo (geodésicas) partidos cada PASO km, así la caravana avanza a ritmo parejo y ningún salto pasa de
los 230 km que exige el test. Cada parada queda como vértice exacto (la posición de la parada se inserta en el trazo), así
`idx` la ancla justo ahí. Las paradas y fechas verificadas están en itinerarios.js; los puntos de paso de aquí no se
muestran con nombre: son solo el dibujo del camino.
"""
import json,os,re,math
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASO=80  # km entre vértices
# Puntos de paso [lat, lon] en orden; los que coinciden con una parada llevan el nombre para comprobar que el trazo pasa por ella.
PUNTOS={
 'ibnbattuta':[
  ('Tánger',[35.78,-5.81]),[34.88,-1.32],[36.8,10.18],[32.9,13.19],[31.2,29.92],('El Cairo',[30.05,31.24]),
  [31.5,34.47],[33.51,36.29],[24.47,39.61],('La Meca',[21.42,39.83]),
  [24.47,39.61],[32.0,44.33],[30.5,47.8],('Bagdad',[33.34,44.4]),
  [30.5,47.8],[21.42,39.83],[21.5,39.17],[12.8,45.03],[2.05,45.34],[-4.05,39.67],('Kilwa',[-8.96,39.51]),
  [-4.05,39.67],[2.05,45.34],[17.0,54.1],[23.6,58.6],[27.1,56.3],[21.42,39.83],[30.05,31.24],[36.5,32.0],[37.87,32.49],[42.03,35.15],[45.03,35.38],[47.5,46.5],[44.1,28.6],('Constantinopla',[41.01,28.98]),
  [44.1,28.6],[47.5,46.5],[41.55,60.63],[39.77,64.42],[39.65,66.97],[36.75,66.9],[34.53,69.17],[30.2,71.47],('Delhi',[28.65,77.23]),
  [26.9,75.8],[23.0,72.6],[15.5,73.8],[11.25,75.78],('Malé',[4.18,73.51]),
  [6.8,80.5],[22.35,91.8],[5.1,97.2],[1.3,103.8],[10.8,106.7],[16.1,108.2],('Quanzhou',[24.87,118.68]),
  [16.1,108.2],[1.3,103.8],[5.1,97.2],[11.25,75.78],[27.1,56.3],[29.6,52.5],[33.34,44.4],[33.51,36.29],[30.05,31.24],[31.2,29.92],[36.8,10.18],[34.03,-5.0],[37.18,-3.6],[34.03,-5.0],[31.28,-4.28],[23.6,-5.0],[17.3,-7.03],[13.5,-9.5],('Tombuctú',[16.77,-3.01]),
  [16.27,-0.04],[17.5,6.8],[31.28,-4.28],('Fez',[34.03,-5.0])]}

def hav(a,b):
    R=6371;la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]));q=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(q))
def geodesica(a,b,n):
    """n puntos intermedios del círculo máximo entre a y b (lat, lon en grados)."""
    la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]));d=2*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
    out=[]
    if d==0: return out
    for k in range(1,n+1):
        f=k/(n+1);A=math.sin((1-f)*d)/math.sin(d);B=math.sin(f*d)/math.sin(d)
        x=A*math.cos(la1)*math.cos(lo1)+B*math.cos(la2)*math.cos(lo2);y=A*math.cos(la1)*math.sin(lo1)+B*math.cos(la2)*math.sin(lo2);z=A*math.sin(la1)+B*math.sin(la2)
        out.append([round(math.degrees(math.atan2(z,math.hypot(x,y))),2),round(math.degrees(math.atan2(y,x)),2)])
    return out
def trazo(puntos):
    pts=[p[1] if isinstance(p,tuple) else p for p in puntos];out=[pts[0]]
    for a,b in zip(pts,pts[1:]):
        n=int(hav(a,b)//PASO);out+=geodesica(a,b,n)+[b]
    return out

p=os.path.join(RAIZ,'src','data','itinerarios.js');s=open(p,encoding='utf8').read()
for rid,puntos in PUNTOS.items():
    t=trazo(puntos);nombres=[x[0] for x in puntos if isinstance(x,tuple)]
    txt='['+','.join('[%s,%s]'%(('%.2f'%la).rstrip('0').rstrip('.'),('%.2f'%lo).rstrip('0').rstrip('.')) for la,lo in t)+']'
    pat=re.compile(r"(\{id:'%s',.*?\n trazo:)\[\[.*?\]\]\]"%rid,re.S);m=pat.search(s);assert m,rid
    s=s[:m.start()]+m.group(1)+'['+txt+']'+s[m.end():]
    saltos=max(hav(a,b) for a,b in zip(t,t[1:]));km=sum(hav(a,b) for a,b in zip(t,t[1:]))
    print('%s: %d vértices, salto máximo %.0f km, largo del dibujo %.0f km, pasa por %s'%(rid,len(t),saltos,km,', '.join(nombres)))
open(p,'w',encoding='utf8',newline='\n').write(s)
