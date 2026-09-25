# -*- coding: utf-8 -*-
"""La falúa del Nilo, de memoria: casco bajo de madera, con la proa alta y afilada y el timón con su caña en la popa; un palo corto,
plantado cerca de la proa e inclinado hacia adelante, y una sola vela latina, triangular y enorme: la verga, larga, cuelga del tope del
palo con la punta de adelante baja, amarrada junto a la proa, y la de atrás muy alta sobre la popa; abajo, la botavara a lo largo del
pie de la vela. La misma silueta navega el Nilo desde los faraones (el dato está en NAVES.nilo).
"""
import math

import numpy as np

from _barcas import agua, cabo, casco, olas_fondo, palo, tablas, vela
from pintor import forma

VISTA = (0, 0, 120, 88)
AGUA_Y = 75.0

ARRIBA = [(25.4, 64.8), (34, 67), (48, 68), (62, 68.2), (76, 67.4), (88, 65.4), (97, 61.6)]
ABAJO = [(26.6, 71.4), (33, 76.2), (48, 78.2), (62, 78.4), (76, 77.4), (86, 74.6), (94, 67)]
TOPE = np.array([80.4, 42.4])                       # el tope del palo, de donde cuelga la verga
DIR = np.array([-math.cos(math.radians(41)), -math.sin(math.radians(41))])
PICO = TOPE + DIR * 58                              # la punta alta de la verga, sobre la popa
PUNO = TOPE - DIR * 17                              # la punta baja, amarrada junto a la proa
ESCOTA = np.array([30.6, 60.6])                     # el puño de atrás, al final de la botavara


def dibujar(l):
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA, ABAJO, n=4)
    # la borda pintada: una franja verde y un filete claro, como las falúas de colores
    l.mancha(forma(ARRIBA + [(96, 63.6), (88, 67.4), (76, 69.4), (62, 70.2), (48, 70), (34, 69), (25.8, 66.8)], 1), '2F8A74', .75,
             dentro=c)
    l.trazo([(26, 66.9), (34, 69.1), (48, 70.1), (62, 70.3), (76, 69.5), (88, 67.5), (95.6, 64)], [.1, .3, .3, .3, .3, .3, .1],
            color='F0F6F4', alfa=.85, dentro=c)
    # el timón y su caña, en la popa
    palo(l, (26.2, 63.4), (35.6, 62.2), .5, .4)
    l.masa(forma([(24.4, 63.2), (27.4, 63.6), (27.8, 74.6), (25.6, 77.4), (22.6, 76.4), (23.2, 68)], 1), material='acento',
           alto=.3, brillo=.2, vientre=0, hondo=0, linea=.6)
    # el palo, corto e inclinado hacia adelante
    palo(l, (78.8, 67.6), tuple(TOPE + [.3, -1]), .85, .6)
    # la vela: el triángulo entre la verga, la botavara y la baluma; los paños van a lo largo, de la botavara a la verga
    baluma = [tuple(PICO), (34.4, 22), (31.8, 38), (30.8, 50), tuple(ESCOTA)]
    pie = [tuple(ESCOTA), (48, 60.2), (66, 59), (82, 57.6), tuple(PUNO)]
    borde = [tuple(PUNO)] + [tuple(PUNO + (PICO - PUNO) * f) for f in (.25, .5, .75)] + baluma + pie[1:-1]
    costuras = []
    for f in np.linspace(.1, .9, 8):
        a = np.array(PUNO + (PICO - PUNO) * f)
        b = np.array(ESCOTA + (PUNO - ESCOTA) * (1 - f) * .98)
        costuras.append((tuple(a), tuple(b)))
    vela(l, borde, costuras, veces=2)
    # la verga y la botavara, largas y finas, y las drizas y las escotas
    palo(l, tuple(PUNO + DIR * -1.2), tuple(PICO + DIR * 1.6), .75, .45)
    palo(l, tuple(ESCOTA + [-1, .2]), tuple(PUNO + [0, 2]), .5, .45)
    cabo(l, [tuple(PUNO + [0, 1]), (93.4, 62.4)])
    cabo(l, [tuple(ESCOTA), (34.4, 63.6)])
    cabo(l, [tuple(TOPE), (76.6, 66.8)], alfa=.5)
    sombra = forma([(26, 75), (94, 75), (90, 79.6), (30, 79.6)], 1)
    agua(l, AGUA_Y, sombra=sombra)


FONDO = olas_fondo(AGUA_Y)
LISTO = True
