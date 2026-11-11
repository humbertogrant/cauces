# -*- coding: utf-8 -*-
"""Carta de la vitrina del Nilo: relieve sombreado y rótulos de atlas → src/vitrina/carta-datos.js

    python tools/carta.py

- Relieve: ETOPO1 (NOAA NCEI, dominio público), el mismo ráster que usa tools/relieve.py (tools/ne/etopo1_mundo_…tif, ≈ 0,18°).
  Se recorta la ventana del Nilo, se exagera lo bajo (para que el valle y las tierras altas de Etiopía se lean), se sombrea con
  luz del noroeste en dos escalas y se guarda como UN WebP con transparencia ya en la paleta: sombras hacia #174A3F, luces hacia
  #2B6E5E y un poco más, con el alfa proporcional a la fuerza. Así entra sobre la tierra #215A4F sin ningún modo de mezcla.
- Rótulos, líneas e hitos: posiciones fijas elegidas a mano (geografía, no datos del juego). carta.js decide cuáles caben.
No baja nada de la red. Deja una vista previa en la carpeta temporal del sistema (fuera del repositorio).
"""
import os,io,json,base64,tempfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS=None
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI)
TIF=os.path.join(AQUI,'ne','etopo1_mundo_ETOPO1_ice_surface.tif')
SALIDA=os.path.join(RAIZ,'src','vitrina','carta-datos.js')
BB=(-180,-60,180,84)                 # lon O, lat S, lon E, lat N del ráster (ver BB_MUNDO en relieve.py)
LATN,LONO,LATS,LONE=36,18,-6,46      # la ventana del Nilo
ANCHO=400; ALTO=int(round(ANCHO*(LATN-LATS)/(LONE-LONO)))
TOPE=150000                          # caracteres de base64
BASE=(0x21,0x5A,0x4F); BAJA=(0x17,0x4A,0x3F); BAJA2=(0x11,0x3E,0x35); ALTA=(0x2B,0x6E,0x5E); ALTA2=(0x45,0x94,0x7E)

def relieve():
    a=np.array(Image.open(TIF),dtype=np.float32); a[~np.isfinite(a)|(np.abs(a)>12000)]=0
    H,W=a.shape
    lat=LATN-(np.arange(ALTO)+.5)*(LATN-LATS)/ALTO; lon=LONO+(np.arange(ANCHO)+.5)*(LONE-LONO)/ANCHO
    fila=(BB[3]-lat)/(BB[3]-BB[1])*H-.5; col=(lon-BB[0])/(BB[2]-BB[0])*W-.5
    F,C=np.meshgrid(fila,col,indexing='ij')
    z=np.clip(ndi.map_coordinates(a,[F,C],order=3,mode='nearest'),0,None)
    zc=np.power(z,0.6)*8             # exagera lo bajo: 100 m → 127, 1 000 m → 505, 3 000 m → 975
    def sombra(sig,k):               # luz del noroeste, a 45°: positiva en las laderas que miran al noroeste
        s=ndi.gaussian_filter(zc,sig); gy,gx=np.gradient(s)   # gy crece hacia el sur, gx hacia el este
        v=(.5*gx+.5*gy+.7071*k)/np.sqrt(gx*gx+gy*gy+k*k)-.7071
        return np.where(v>0,v/.2929,v/.55)
    e=.6*sombra(1.3,34)+.45*sombra(5,15)
    e=np.sign(e)*np.power(np.clip(np.abs(e),0,1),.8)
    e=e+.30*np.clip((z-700)/2000,0,1)-.10*np.clip(1-z/250,0,1)   # las tierras altas, más claras; el valle y la costa, más oscuros
    e=np.clip(e,-1,1); f=np.abs(e)[...,None]
    def mez(c1,c2,t): return np.array(c1,np.float32)*(1-t)+np.array(c2,np.float32)*t
    t=np.clip((f-.55)/.45,0,1)
    rgb=np.where(e[...,None]>0,mez(ALTA,ALTA2,t),mez(BAJA,BAJA2,t))
    alfa=np.clip(np.abs(e)*.9,0,1)
    b=22; y=np.minimum(np.arange(ALTO),np.arange(ALTO)[::-1])/b; x=np.minimum(np.arange(ANCHO),np.arange(ANCHO)[::-1])/b
    borde=np.clip(np.minimum.outer(y,x),0,1); borde=borde*borde*(3-2*borde)   # se desvanece hacia los bordes de la ventana
    alfa=alfa*borde
    return np.dstack([np.clip(rgb,0,255),alfa[...,None]*255]).round().astype(np.uint8),z

# Rótulos: t (| parte en renglones), p [lat, lon] del ancla, a (start|middle|end), c (clase: agua, pais, rio-n), g (giro),
# max y min: ancho de vista (en unidades del SVG, llevado a un teléfono de 390 px) a partir del cual se oculta o se muestra.
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
 dict(t='EGIPTO',p=[22.3,27.9],a='start',c='pais',max=60),
 dict(t='EGIPTO',p=[28.0,29.3],a='start',c='pais',max=20),
 dict(t='SUDÁN',p=[21.5,27.9],a='start',c='pais',max=60),
 dict(t='SUDÁN',p=[12.2,27.6],a='start',c='pais',max=60),
 dict(t='SUDÁN DEL SUR',p=[6.3,29.6],a='end',c='pais',max=60),
 dict(t='UGANDA',p=[0.8,32.2],a='end',c='pais',max=60),
 dict(t='ETIOPÍA',p=[8.9,37.1],a='end',c='pais',max=60),
 dict(t='DESIERTO|DE NUBIA',p=[20.9,34.9],a='middle',c='pais',max=60),
]
# Hitos: ninguno es una parada del juego. m: marca (cuadro | tri); l: de qué lado va el nombre (izq | der);
# tras: índice de la parada que tiene que estar alcanzada para que el hito aparezca (Guiza queda pegada a El Cairo: memoria primero).
HITOS=[
 dict(t='Abu Simbel',p=[22.34,31.63],m='cuadro',l='izq',max=45),
 dict(t='Pirámides de Meroe',p=[16.94,33.75],m='tri',l='der',max=45),
 dict(t='Pirámides de Guiza',p=[29.98,31.13],m='tri',l='izq',max=45,tras=5),
 dict(t='Alejandría',p=[31.20,29.92],m='cuadro',l='izq',max=45),
]
# Paralelos con nombre: rio = longitud donde el Nilo (o su lago) los cruza, para que el rótulo se vaya al otro lado
LINEAS=[dict(t='ECUADOR',lat=0,rio=33.2,portada='izq'),dict(t='TRÓPICO DE CÁNCER',lat=23.44,rio=32.9,portada='der')]
RETICULA=dict(paso=5,lat=[-10,40],lon=[10,55])

def main():
    im,z=relieve(); img=Image.fromarray(im,'RGBA'); b64=None
    for q in (86,82,78,74,70,64,58,50,42):
        buf=io.BytesIO(); img.save(buf,'WEBP',quality=q,alpha_quality=min(q+6,90),method=6); b64=base64.b64encode(buf.getvalue()).decode()
        if len(b64)<=TOPE: break
    else: raise SystemExit('el relieve no entra en %d caracteres de base64'%TOPE)
    datos=dict(luz=dict(src='data:image/webp;base64,'+b64,caja=[LATN,LONO,LATS,LONE],px=[ANCHO,ALTO]),reticula=RETICULA,lineas=LINEAS,rotulos=ROTULOS,hitos=HITOS)
    cab='// Generado por tools/carta.py: no editar a mano. Relieve sombreado de ETOPO1 (NOAA NCEI, dominio público); rótulos de geografía puestos a mano.\n'
    open(SALIDA,'w',encoding='utf-8',newline='\n').write(cab+'const CARTA='+json.dumps(datos,ensure_ascii=False,separators=(',',':'))+';\n')
    fondo=Image.new('RGBA',img.size,BASE+(255,)); fondo.alpha_composite(img); vista=os.path.join(tempfile.gettempdir(),'carta-relieve-vista.png'); fondo.convert('RGB').save(vista)
    a=im[...,3]; print('relieve %d×%d, calidad %d: %d caracteres de base64 (tope %d); alfa medio %.2f, máximo %d; altura máxima %.0f m'%(ANCHO,ALTO,q,len(b64),TOPE,a.mean()/255,a.max(),z.max()))
    print('datos:',SALIDA,'(%.1f KB)'%(os.path.getsize(SALIDA)/1024)); print('vista previa:',vista)
if __name__=='__main__': main()
