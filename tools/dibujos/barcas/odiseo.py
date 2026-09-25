# -*- coding: utf-8 -*-
"""Una de las doce naves de Odiseo, de memoria: una galera negra, como las «naves negras» del poema, larga y baja, de un solo mástil,
con vela cuadrada y una fila de remeros por banda (se ven los remos, en fila, entrando al agua); la proa baja con el espolón y un ojo
pintado a cada lado; la popa que sube en una curva alta y se enrosca; el remo de gobierno en la popa (el vehículo de la ruta en
ITINERARIOS). El casco va negro, como dice el poema, y el ojo y los adornos en dorado.
"""
import numpy as np

from _barcas import agua, cabo, olas_fondo, palo, poli, remo, vela_cuadrada
from pintor import forma, ovalo

VISTA = (0, 12, 120, 72)
AGUA_Y = 75.0

ARRIBA = [(14.4, 57.2), (22, 64.4), (40, 66.6), (60, 67), (80, 66.6), (96, 64.8), (106, 63.4)]
ABAJO = [(17, 69.4), (26, 74), (40, 76.4), (60, 77), (80, 76.4), (96, 73.8), (108.4, 70.4)]


def dibujar(l):
    for x in np.arange(34, 94, 5.6):                                # los remos de la otra banda
        remo(l, (x + 1.4, 65.6), 122, 17, pala=2.8, ancho=.9, material='lejos')
    palo(l, (62, 67), (62.6, 16), .9, .6)
    vela_cuadrada(l, 62.4, 21, 38, 34, comba=1.6, paños=8)
    palo(l, (41.6, 21.2), (83.4, 21.2), .6, .55)
    cabo(l, [(62.6, 17), (104.6, 63)], alfa=.55)
    cabo(l, [(62.6, 17), (18.4, 61)], alfa=.55)
    cabo(l, [(44, 55.6), (40, 66.4)])
    cabo(l, [(81, 55.4), (86, 66)])
    # el casco negro: la popa que sube y se enrosca, la proa baja con el espolón
    c = l.masa(poli(ARRIBA + [(111.6, 66), (116.4, 69), (111, 70.4)] + ABAJO[::-1], .5), material='oscuro', alto=.5, brillo=.35,
               vientre=0, hondo=0, contraluz=.3)
    popa = forma([(14.4, 57.2), (11.4, 50.6), (10.4, 44), (12.4, 39.4), (16.6, 38), (19.4, 40.6), (17.6, 43.6), (15.4, 42.2),
                  (14.6, 45.6), (16.4, 51.6), (20.4, 58.6), (22, 64.4)], 2)
    l.masa(popa, material='oscuro', alto=.4, brillo=.35, vientre=0, hondo=0, contraluz=.3, linea=.6)
    l.trazo([(15.4, 42.2), (14.6, 45.6), (16.4, 51.6), (20.4, 58.6)], [.1, .3, .3, .1], color='E8B952', alfa=.8)
    # la franja dorada de la borda, el ojo pintado en la proa y las portas de los remos
    l.trazo([(20, 65.8), (40, 68.2), (60, 68.6), (80, 68.2), (96, 66.4), (108, 65.4)], [.1, .45, .45, .45, .45, .1], color='E8B952',
            alfa=.85, dentro=c)
    ojo = forma([(98.4, 69.4), (100.6, 67.8), (103.4, 67.6), (105.4, 69), (103, 70.6), (100.4, 70.6)], 2)
    l.mancha(ojo, 'E8B952', .95, dentro=c)
    l.mancha(ovalo(101.8, 69.2, .9, .9), '05201C', 1, dentro=c)
    for x in np.arange(30, 92, 5.6):
        l.mancha(ovalo(x, 70.4, .55, .5), 'E8B952', .6, dentro=c)
    for x in np.arange(30, 92, 5.6):                                # los remos de esta banda, en fila
        remo(l, (x, 70.4), 118, 16, pala=3, ancho=1)
    remo(l, (19.2, 61.4), 100, 22, pala=5.6, ancho=2.2)              # el remo de gobierno
    agua(l, AGUA_Y, sombra=poli([(16, 75), (110, 75), (104, 79.2), (22, 79.2)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
