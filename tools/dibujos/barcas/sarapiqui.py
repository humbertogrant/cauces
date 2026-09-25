# -*- coding: utf-8 -*-
"""El bote de Sarapiquí, de memoria: un bote largo y angosto, de tablas de madera y la borda pintada, que hoy lleva motor fuera de borda
y antes iba a remo y pértiga río abajo hasta el San Juan (NAVES.sarapiqui): el motor en la popa, las bancas, y la pértiga y un remo
a bordo.
"""
import numpy as np

from _barcas import agua, caja, motor_fuera, olas_fondo, palo, poli, tablas
from _canoas import canoa, contorno
from pintor import forma

VISTA = (0, 48, 120, 32)
AGUA_Y = 72.0


def dibujar(l):
    borda, quilla = canoa(14, 112, 65, 7, sube_popa=.6, sube_proa=5.6, panza=1.2)
    palo(l, (8, 64.2), (117.4, 61.2), .42, .4)                     # la pértiga, a lo largo, dentro del bote: asoma por las puntas
    for x in np.arange(34, 100, 16):                                # las bancas, que asoman por la borda
        l.masa(caja(x, 62.6, x + 5, 64.4, .15), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.45, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, borda[1:-1], quilla[1:-1], n=3)
    l.mancha(forma(borda[:-1] + [(x, y + 1.6) for x, y in borda[-2::-1]], 1), '2F8A74', .8, dentro=c)       # la borda pintada
    l.trazo([(x, y + 1.9) for x, y in borda[1:-1]], .2, color='F0F6F4', alfa=.85, dentro=c)
    motor_fuera(l, 14.4, 60.4, alto_=10.4)
    agua(l, AGUA_Y, sombra=poli([(16, 72), (108, 72), (102, 75.4), (20, 75.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
