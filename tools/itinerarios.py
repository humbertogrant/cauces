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
PASO_RUTA={'napoleon':45}  # rutas cortas: vértices más seguidos para que el trazo tenga cuerpo (el test pide 40 o más)
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
  [16.27,-0.04],[17.5,6.8],[31.28,-4.28],('Fez',[34.03,-5.0])],
 'marcopolo':[
  ('Venecia',[45.44,12.33]),[42.0,18.0],[35.1,25.5],('Acre',[32.93,35.08]),[36.8,35.8],[39.9,41.3],[38.08,46.3],[32.0,51.7],[30.28,57.08],('Ormuz',[27.15,57.08]),
  [30.28,57.08],[34.3,58.7],[36.75,66.9],[37.0,71.5],[38.5,74.0],('Kashgar',[39.47,75.99]),[37.1,79.9],[39.5,88.5],[40.14,94.66],[38.9,100.4],[41.0,111.0],('Shangdu',[42.36,116.18]),
  ('Pekín',[39.9,116.4]),[34.7,113.6],[32.06,118.8],('Hangzhou',[30.25,120.17]),[24.87,118.68],[13.8,109.2],[10.8,106.7],[1.3,103.8],('Sumatra',[5.1,97.2]),[8.5,93.0],('Ceilán',[7.0,80.5]),
  [11.25,75.78],[19.0,72.8],[24.5,63.0],[27.15,57.08],[30.28,57.08],[32.0,51.7],[38.08,46.3],[39.9,41.3],('Trebisonda',[41.0,39.72]),[41.01,28.98],[40.6,22.9],[42.0,18.0],('Venecia',[45.44,12.33])],
 'alejandro':[
  ('Pela',[40.76,22.52]),[40.2,26.4],[39.96,26.24],[40.3,27.3],[38.49,28.04],[37.94,27.34],[37.04,27.42],[38.4,30.5],('Gordio',[39.65,31.99]),[36.92,34.9],('Issos',[36.83,36.2]),
  [35.2,35.9],[34.45,35.85],('Tiro',[33.27,35.2]),[31.5,34.47],[30.6,32.3],[29.85,31.25],[29.2,25.52],('Alejandría',[31.2,29.92]),[29.85,31.25],[31.5,34.47],[33.51,36.29],[36.2,37.15],[36.5,40.7],('Gaugamela',[36.36,43.25]),
  [34.4,44.3],[32.54,44.42],[32.19,48.26],[30.5,50.5],('Persépolis',[29.93,52.89]),[32.4,51.7],[34.8,48.5],[36.3,54.0],[36.2,58.0],[35.4,62.0],[36.75,66.9],[37.5,67.3],('Samarcanda',[39.65,66.97]),
  [36.75,66.9],[34.5,69.2],[34.0,71.5],[33.74,72.79],('Hidaspes',[32.93,73.73]),[31.3,74.9],[30.2,71.5],[27.5,68.4],[24.9,67.0],[25.3,60.6],[27.2,57.0],[30.5,50.5],[32.19,48.26],('Babilonia',[32.54,44.42])],
 'cortes':[
  ('Santiago de Cuba',[20.02,-75.82]),[21.8,-80.0],[22.4,-83.6],('Cozumel',[20.51,-86.95]),[19.6,-88.0],('Tabasco',[18.53,-92.65]),[18.7,-94.5],('Veracruz',[19.19,-96.14]),('Cempoala',[19.44,-96.4]),[19.53,-96.92],[19.45,-97.5],('Tlaxcala',[19.32,-98.24]),
  ('Cholula',[19.06,-98.3]),[19.15,-98.75],('Tenochtitlan',[19.43,-99.13]),[19.6,-98.95],('Otumba',[19.7,-98.75]),[19.32,-98.24],('Texcoco',[19.51,-98.88]),('Tenochtitlan',[19.43,-99.13])],
 'odiseo':[
  ('Troya',[39.96,26.24]),[39.9,25.9],[40.3,25.3],('Ísmaro',[40.87,25.52]),[40.3,25.0],[39.0,24.5],[37.5,24.0],[36.4,23.2],[35.6,20.5],[34.6,15.5],[34.0,12.0],('Yerba',[33.8,10.85]),
  [34.3,11.6],[35.6,12.8],[36.7,14.0],[37.1,15.4],('Etna',[37.6,15.17]),[38.0,15.45],[38.25,15.63],[38.4,15.4],('Lípari',[38.47,14.95]),[39.3,14.3],[40.3,13.4],[41.0,12.9],('Circeo',[41.23,13.05]),
  [40.9,13.6],[40.7,14.2],('Sirenas',[40.58,14.43]),[40.0,15.0],[39.3,15.4],[38.6,15.7],('Mesina',[38.25,15.63]),[37.6,15.5],[36.9,15.4],[36.4,14.9],('Gozo',[36.05,14.25]),
  [36.0,15.5],[36.8,18.0],[38.4,19.6],('Corfú',[39.62,19.92]),[39.0,20.4],[38.6,20.6],('Ítaca',[38.37,20.72])],
 'napoleon':[
  ('Kaunas',[54.9,23.9]),[54.8,24.6],('Vilna',[54.69,25.28]),[54.95,26.4],[55.1,27.7],[55.15,29.0],('Vítebsk',[55.19,30.2]),[54.95,31.1],('Smolensk',[54.78,32.05]),[54.95,33.3],[55.2,34.3],[55.55,35.0],('Borodinó',[55.52,35.83]),
  [55.5,36.6],('Moscú',[55.75,37.62]),[55.45,37.3],('Maloyaroslávets',[55.02,36.46]),[55.35,35.95],[55.55,35.0],[55.2,34.3],[54.95,33.3],[54.78,32.05],('Krasny',[54.57,31.45]),[54.5,30.4],[54.4,29.4],('Berézina',[54.3,28.48]),
  [54.35,27.4],[54.48,26.4],('Vilna',[54.69,25.28])],
 'zhenghe':[
  ('Nankín',[32.06,118.8]),[31.45,121.1],[26.0,120.5],[19.5,113.0],('Champa',[13.78,109.22]),[6.0,109.0],[-3.0,110.5],('Java',[-7.25,112.75]),[-6.1,106.8],[1.3,103.8],('Malaca',[2.19,102.25]),[5.1,97.2],[6.03,80.22],('Calicut',[11.25,75.78]),
  [6.03,80.22],[5.1,97.2],[1.3,103.8],('Palembang',[-2.99,104.76]),[1.3,103.8],[2.19,102.25],[5.1,97.2],[6.03,80.22],[11.25,75.78],[15.5,60.0],[13.5,50.5],('Adén',[12.8,45.03]),[11.5,45.5],[9.5,50.9],('Mogadiscio',[2.05,45.34]),[-1.0,42.5],('Malindi',[-3.22,40.12]),
  [2.05,45.34],[11.25,75.78],[6.03,80.22],[5.1,97.2],[2.19,102.25],[1.3,103.8],[13.78,109.22],[19.5,113.0],[26.0,120.5],[31.45,121.1],('Nankín',[32.06,118.8])]}

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
def trazo(puntos,paso=PASO):
    pts=[p[1] if isinstance(p,tuple) else p for p in puntos];out=[pts[0]]
    for a,b in zip(pts,pts[1:]):
        n=int(hav(a,b)//paso);out+=geodesica(a,b,n)+[b]
    return out

p=os.path.join(RAIZ,'src','data','itinerarios.js');s=open(p,encoding='utf8').read()
for rid,puntos in PUNTOS.items():
    t=trazo(puntos,PASO_RUTA.get(rid,PASO));nombres=[x[0] for x in puntos if isinstance(x,tuple)]
    txt='['+','.join('[%s,%s]'%(('%.2f'%la).rstrip('0').rstrip('.'),('%.2f'%lo).rstrip('0').rstrip('.')) for la,lo in t)+']'
    pat=re.compile(r"(\{id:'%s',.*?\n trazo:)\[\[.*?\]\]\]"%rid,re.S);m=pat.search(s);assert m,rid
    s=s[:m.start()]+m.group(1)+'['+txt+']'+s[m.end():]
    saltos=max(hav(a,b) for a,b in zip(t,t[1:]));km=sum(hav(a,b) for a,b in zip(t,t[1:]))
    print('%s: %d vértices, salto máximo %.0f km, largo del dibujo %.0f km, pasa por %s'%(rid,len(t),saltos,km,', '.join(nombres)))
open(p,'w',encoding='utf8',newline='\n').write(s)
