# -*- coding: utf-8 -*-
"""La lancha de Tárcoles, de memoria: una lancha de madera con motor fuera de borda, como las que llevan turistas a ver los cocodrilos
del río y pescadores hasta la boca (NAVES.tarcoles): el casco pintado, el techo de lona sobre postes para el sol, las bancas y un
salvavidas colgado.
"""
import numpy as np

from _barcas import agua, caja, motor_fuera, olas_fondo, palo, poli, tablas
from _canoas import canoa, contorno
from pintor import forma, ovalo

VISTA = (0, 43, 120, 37)
AGUA_Y = 72.0


def dibujar(l):
    borda, quilla = canoa(12, 110, 63.6, 8.4, sube_popa=.4, sube_proa=5.4, panza=1.1)
    for x in np.arange(26, 90, 12):                                 # los postes del techo
        palo(l, (x, 64), (x, 47.4), .35, .32, material='claro')
    for x in np.arange(30, 94, 12):                                 # las bancas
        l.masa(caja(x, 61.8, x + 6, 63.4, .15), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.45, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, borda[1:-1], quilla[1:-1], n=3)
    l.mancha(forma([(x, y + 1.8) for x, y in borda[:-1]] + [(x, y + 3.6) for x, y in borda[-2::-1]], 1), '2F8A74', .8, dentro=c)
    # el techo de lona, con el borde en festón
    borde = [(x, 48.6 + (1 if k % 2 else .2)) for k, x in enumerate(np.arange(22.4, 92, 1.8))]
    t = l.masa(poli([(21, 46.6), (93.6, 46.6), (93.6, 48.6)] + borde[::-1], .2), material='claro', alto=.3, brillo=.12, vientre=0,
               hondo=0, linea=.45)
    for x in np.arange(30, 92, 12):
        l.mancha(caja(x, 46.8, x + 6, 48.4, .1), '6CC8A8', .6, dentro=t)
    # el salvavidas colgado de un poste
    s = l.masa(ovalo(50, 56, 2.4, 2.4).difference(ovalo(50, 56, 1.1, 1.1)), material='claro', alto=.4, brillo=.2, vientre=0, hondo=0,
               linea=.35)
    for a in (40, 130, 220, 310):
        l.mancha(ovalo(50 + 1.8 * np.cos(np.radians(a)), 56 + 1.8 * np.sin(np.radians(a)), .7, .45, a + 90), 'E8B952', .9, dentro=s)
    motor_fuera(l, 12.2, 58.8, alto_=11.4)
    agua(l, AGUA_Y, sombra=poli([(14, 72), (106, 72), (100, 75.4), (18, 75.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
