# -*- coding: utf-8 -*-
"""El bongo guanacasteco, de memoria: una canoa grande de un solo tronco, con los costados gruesos y las puntas que suben un poco, que
bajaba el Tempisque cargada y cruzaba el golfo hasta Puntarenas: remos y, cuando el viento ayudaba, una vela en un palo corto
(NAVES.tempisque). A bordo, la carga del río: cueros doblados y sacos de maíz (MERCADOS.tempisque).
"""
from _barcas import agua, cabo, casco, fardo, olas_fondo, palo, remo, vela
from pintor import forma

VISTA = (0, 22, 120, 62)
AGUA_Y = 74.0

ARRIBA = [(10.4, 61.4), (20, 65), (40, 67), (60, 67.4), (80, 66.8), (98, 64.4), (108.4, 60.8)]
ABAJO = [(13.6, 66.6), (24, 72.8), (40, 76), (60, 76.8), (80, 76), (96, 72.8), (106, 66.4)]


def dibujar(l):
    remo(l, (30, 64.6), 118, 18, material='lejos')
    # el palo corto, la vela y su botavara
    palo(l, (72, 67), (72.4, 26.4), .8, .6)
    vela(l, [(73.2, 27.8), (95.4, 33.6), (92.4, 48), (90, 60.4), (73.6, 60.8)],
         [((73.6, 27.8 + k * 6.6), (93.6 - k * .4, 33.6 + k * 5.4)) for k in range(1, 5)])
    palo(l, (72.6, 60.8), (91.4, 60.4), .45, .4)
    palo(l, (72.6, 28.6), (95.6, 33.8), .45, .4)
    cabo(l, [(90.6, 60.6), (100, 64)])
    # la carga: cueros doblados y sacos de maíz
    fardo(l, 36, 60.6, 8.6, 6, material='lejos')
    fardo(l, 44, 61.4, 7, 5.4)
    fardo(l, 51.6, 60.2, 7.6, 6.6)
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.55, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    # el tronco vaciado: el borde grueso y la madera, con sus vetas
    l.trazo([(12, 63.4), (20, 66.8), (40, 68.8), (60, 69.2), (80, 68.6), (98, 66.2), (106.6, 62.8)], [.1, .5, .5, .5, .5, .5, .1],
            color='93701A', alfa=.5, dentro=c, difuso=.15)
    for k in range(3):
        y = 70.6 + k * 1.8
        l.trazo([(18 + k * 3, y), (40, y + .8), (60, y + 1), (80, y + .8), (100 - k * 3, y - .6)], [.05, .14, .14, .14, .05],
                color='93701A', alfa=.45, dentro=c)
    remo(l, (26, 66.6), 116, 18)
    remo(l, (14.6, 62.2), 104, 20, pala=4.4, ancho=1.8)
    agua(l, AGUA_Y, sombra=forma([(12, 74), (106, 74), (100, 78.6), (18, 78.6)], 1))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
