# -*- coding: utf-8 -*-
"""El vapor de ruedas del Murray, de memoria: un vapor de ruedas laterales, de madera de eucalipto rojo: casco bajo, la rueda de
paletas al costado, tapada por su caja de medio círculo con los listones en abanico; una chimenea alta; la timonera arriba, adelante;
la leña apilada en cubierta, porque quemaba leña; y a remolque una barcaza cargada de fardos de lana, como las que unían las
estancias del interior con los trenes de la costa entre 1860 y 1900 (NAVES.murray).
"""
import numpy as np

from _barcas import agua, caja, cabina, cabo, chimenea, fardo, humo, olas_fondo, poli
from pintor import forma, ovalo

VISTA = (0, 10, 120, 74)
AGUA_Y = 74.0


def dibujar(l):
    # la barcaza de lana, a remolque
    b = l.masa(poli([(2.6, 67.4), (36.6, 67.4), (38.4, 69.4), (36, 75.2), (4, 75.2), (1.6, 70.6)], .4), material='acento', alto=.35,
               brillo=.2, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(3, 71), (36.6, 71)], .14, alfa=.3, dentro=b)
    for fila, y in enumerate((61.4, 55.6)):
        for x in np.arange(5 + fila * 2.4, 34 - fila * 2, 5.2):
            fardo(l, x, y, 4.8, 5.8 + (fila == 0) * .2, material='claro', ataduras=2)
    cabo(l, [(38.4, 68.2), (46, 70.4), (53.4, 68.4)], ancho=.2)
    # el vapor: el casco bajo, la cubierta con su cabina, la timonera, la chimenea y la leña
    c = l.masa(poli([(52.4, 66.8), (108, 66.8), (116, 64.4), (112.6, 70.8), (104, 74.6), (56, 74.6), (52.2, 71.4)], .4),
               material='acento', alto=.4, brillo=.25, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(53, 70.4), (106, 70.4), (113.4, 67.6)], .14, alfa=.3, dentro=c)
    cabina(l, 56, 58.6, 100, 66.8, ventanas=[(x, 60.4, 2.6, 3.2) for x in np.arange(58.4, 99, 4.6)], techo=1.4)
    cabina(l, 88, 50.6, 99.6, 57.2, ventanas=[(89.6, 52, 3, 3.2), (94.4, 52, 3, 3.2)], techo=1)
    for k, x in enumerate(np.arange(58, 74, 2.1)):                  # la leña apilada sobre el techo de la cabina
        for j in range(2):
            l.masa(ovalo(x + j * 1.05, 56.4 - j * 1.6, 1.05, .95), material='acento', alto=.4, brillo=.15, vientre=0, hondo=0,
                   linea=.3, arroja=False)
            l.mancha(ovalo(x + j * 1.05, 56.4 - j * 1.6, .45, .4), '93701A', .7)
    chimenea(l, 80.6, 58, 26, r=1.7)
    humo(l, 79.4, 22.4, n=5, deriva=(-5.4, -.9), r=2.6)
    # la caja de la rueda: medio círculo con los listones en abanico, sobre la rueda
    cx, cy, r = 77.4, 66.6, 11.4
    caja_rueda = forma([(cx - r, cy)] + [(cx - r * np.cos(a), cy - r * np.sin(a)) for a in np.linspace(0, np.pi, 24)] + [(cx + r, cy)], 0)
    k_ = l.masa(caja_rueda.union(caja(cx - r, cy - .4, cx + r, cy + 3.4, .2)), material='claro', alto=.35, brillo=.15, vientre=0,
                hondo=0, linea=.6)
    for a in np.linspace(.18, np.pi - .18, 9):
        l.trazo([(cx - 2.6 * np.cos(a), cy - 2.6 * np.sin(a)), (cx - (r - .8) * np.cos(a), cy - (r - .8) * np.sin(a))], [.3, .3],
                color='2F8A74', alfa=.6, dentro=k_)
    l.masa(ovalo(cx, cy, 2.8, 2.8).intersection(caja(cx - 3, cy - 3, cx + 3, cy)), material='acento', alto=.3, brillo=.2, vientre=0,
           hondo=0, linea=.4)
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(4, 74), (114, 74), (110, 78), (6, 78)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
