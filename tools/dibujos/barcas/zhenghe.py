# -*- coding: utf-8 -*-
"""La flota del tesoro de Zheng He, de memoria: un junco enorme, un barco del tesoro, con muchos mástiles (aquí se ven cinco) y velas de
estera con listones de bambú, la proa chata y alta, la popa todavía más alta con su castillo de varios pisos y sus ventanas, el timón
grande colgado de la popa; y en el costado, una fila de portas. Las crónicas cuentan unas 300 naves y 27 000 hombres en el primer
viaje; el tamaño exacto de los barcos grandes se discute (el vehículo de la ruta en ITINERARIOS).
"""
import numpy as np

from _barcas import agua, cabo, esteras, olas_fondo, palo, poli, tablas
from pintor import forma

VISTA = (0, 4, 120, 80)
AGUA_Y = 76.0


def vela_junco(l, x_palo, y_top, ancho_popa, ancho_proa, alto, listones=7, material='vientre'):
    x0, x1 = x_palo - ancho_popa, x_palo + ancho_proa
    pts = [(x0 + 2.4, y_top + 1.2), (x1 - 1.2, y_top - 1.4), (x1 + .5, y_top + alto * .5), (x1 + 1.2, y_top + alto),
           (x0 - 1.2, y_top + alto + 1), (x0 - .3, y_top + alto * .45)]
    v = l.masa(forma(pts, 1), material=material, alto=.22, brillo=.08, vientre=0, hondo=0, escalon=.15,
               contraluz=.15, linea=.55)
    esteras(l, v, paso=1.6, alfa=.22)
    for k in range(listones + 1):
        f = k / listones
        a = (x0 + 2.4 + (x0 - 1.2 - x0 - 2.4) * f, y_top + 1.2 + (alto + 1 - 1.2) * f)
        b = (x1 - 1.2 + (x1 + 1.2 - x1 + 1.2) * f, y_top - 1.4 + (alto + 1.4) * f)
        l.masa(forma([(a[0] - .3, a[1] - .3), (b[0] + .3, b[1] - .3), (b[0] + .3, b[1] + .3), (a[0] - .3, a[1] + .3)], 0),
               material='acento', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25, arroja=False)
    return v


def dibujar(l):
    # los cinco palos del barco del tesoro, de popa a proa, con sus velas
    for x, h, ap, apr, alto_, n in ((30, 36, 10, 4, 24, 5), (44, 50, 15, 6, 36, 7), (60, 58, 17, 7, 44, 8), (75, 50, 15, 6, 36, 7),
                                     (87, 34, 9, 4, 22, 5)):
        palo(l, (x, 66), (x + .6, 66 - h), .8, .55)
        vela_junco(l, x + .3, 66 - h + 3, ap, apr, alto_, listones=n)
        cabo(l, [(x - ap + 2, 66 - h + 3 + alto_), (x - ap - 3, 64)], ancho=.12, alfa=.5)
    # el castillo de popa, de varios pisos, con sus ventanas
    popa = l.masa(poli([(8.6, 38.6), (26, 41.4), (27, 60), (12, 56)], .4), material='acento', alto=.35, brillo=.2, vientre=0, hondo=0,
                  linea=.6)
    for fila, y in enumerate((43, 48.4)):
        for x in np.arange(12.4 + fila * .8, 25, 3.6):
            l.mancha(poli([(x, y), (x + 2.2, y + .3), (x + 2.2, y + 3.2), (x, y + 2.9)], .15), '0C3A33', .7, dentro=popa)
    l.trazo([(10, 46.8), (26.4, 47.6)], .2, alfa=.5, dentro=popa)
    l.masa(forma([(5.6, 38.4), (9.4, 35.8), (18, 36.4), (28, 38.8), (28, 40.8), (17.6, 39.2), (8.4, 39.8)], 2), material='lejos',
           alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    # el casco, enorme: la popa alta y la proa chata
    ARRIBA = [(8.4, 44), (16, 50), (30, 60.2), (50, 64.6), (70, 64.8), (88, 62.6), (102, 57.2), (108.6, 52.6)]
    ABAJO = [(14.4, 70.4), (22, 75), (34, 78.2), (50, 79.2), (70, 79.2), (88, 77.4), (100, 72.6), (106.8, 66)]
    c = l.masa(poli(ARRIBA + [(109.6, 55.4), (108.6, 61.4)] + ABAJO[::-1], .5), material='acento', alto=.5, brillo=.3, vientre=0,
               hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA[1:], ABAJO[1:], n=5)
    l.trazo([(106, 53.6), (105.4, 66)], [.12, .3, .12], alfa=.35, dentro=c)
    for x in np.arange(36, 100, 8):                                  # las portas de la cubierta de abajo
        l.mancha(poli([(x, 66.6), (x + 2.4, 66.8), (x + 2.4, 68.8), (x, 68.6)], .15), '0C3A33', .55, dentro=c)
    l.masa(poli([(9.4, 56), (13, 58), (16, 74), (13.6, 79.4), (6.4, 78.4), (7.6, 66)], .5), material='acento', alto=.3, brillo=.15,
           vientre=0, hondo=0, linea=.6)                              # el timón
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(10, 76), (106, 76), (100, 80.4), (16, 80.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
