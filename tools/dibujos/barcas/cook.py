# -*- coding: utf-8 -*-
"""El Endeavour de Cook, de memoria: un barco carbonero de Whitby, de unos 30 metros, robusto, de proa redonda y llena, fondo chato y
poco calado, con la popa cuadrada y sus ventanas; aparejo de corbeta: tres palos, el trinquete y el mayor con velas cuadradas (la
mayor, la gavia y el juanete), el de mesana con su cangreja y una gavia, y los foques en el bauprés. En cubierta, la cabra, que ya
había dado la vuelta al mundo en otro barco (el vehículo de la ruta en ITINERARIOS).
"""
import numpy as np

from _barcas import agua, cabo, olas_fondo, palo, poli, tablas, vela, vela_cuadrada
from pintor import forma, tubo

VISTA = (0, 0, 120, 84)
AGUA_Y = 76.0

ARRIBA = [(12.6, 54.4), (20, 58.4), (40, 61.2), (60, 61.8), (80, 61.2), (94, 59.4), (104, 56)]
ABAJO = [(15.6, 72.4), (24, 76.6), (40, 78.8), (60, 79.2), (80, 78.6), (94, 76.2), (103.4, 68.4)]


def aparejo(l, x, y0, velas, alto_palo):
    """un palo con sus velas cuadradas, de abajo arriba: (ancho, alto) de cada una; devuelve el tope"""
    palo(l, (x, y0), (x + .8, y0 - alto_palo), .95, .45)
    y = y0 - 8
    for ancho, alto_ in velas:
        y_top = y - alto_
        vela_cuadrada(l, x + .3, y_top, ancho, alto_, comba=1, paños=4, inflado=.22)
        palo(l, (x - ancho / 2 - 1, y_top), (x + ancho / 2 + 1.6, y_top), .45, .4)
        y = y_top - 1.4
    return y


def dibujar(l):
    # los foques en el bauprés
    palo(l, (98, 58.4), (119, 50.4), .7, .45)
    vela(l, [(118.4, 51.2), (93.4, 22.8), (108.6, 50.2)], [], veces=1, alto=.2)
    vela(l, [(110.4, 53.4), (88.6, 26.4), (101.6, 54)], [], veces=1, alto=.2)
    # el palo de mesana: la cangreja y la gavia
    palo(l, (27, 58.6), (27.6, 20), .8, .45)
    vela(l, [(27.6, 32.2), (13.2, 36.4), (7.4, 53.6), (27.4, 53.4)], [((27.4, 40), (10.8, 43)), ((27.4, 47), (9, 48.8))], veces=0)
    palo(l, (27.6, 32.2), (12.4, 36.6), .4, .35)                    # el pico de la cangreja
    palo(l, (27.6, 53.8), (6, 54.2), .45, .4)                       # la botavara
    vela_cuadrada(l, 27.8, 23.6, 13, 8, comba=.8, paños=3, inflado=.22)
    palo(l, (20.2, 23.6), (35.4, 23.6), .4, .35)
    # el mayor y el trinquete, con sus tres velas cuadradas
    aparejo(l, 56, 60, [(34, 14), (29, 11.6), (22, 8.6)], 58)
    aparejo(l, 83, 59.6, [(30, 13), (26, 10.8), (19, 8)], 53)
    for p0, p1 in (((56.8, 3.4), (27.6, 20)), ((56.8, 3.4), (83.8, 7.4)), ((83.8, 7.4), (118.6, 50.8)), ((27.6, 20), (12, 55))):
        cabo(l, [p0, p1], ancho=.12, alfa=.55)
    for x in (44, 50, 62, 68, 76, 90):                              # los obenques
        cabo(l, [(x, 60.6), (56.4 if x < 70 else 83.4, 40)], ancho=.1, alfa=.4)
    # el casco: la proa redonda y llena, la popa cuadrada con su espejo y sus ventanas
    c = l.masa(poli(ARRIBA + [(106.8, 58.4), (106.6, 63.6)] + ABAJO[::-1] + [(12.4, 65)], .6), material='acento', alto=.5, brillo=.3,
               vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA[1:], ABAJO[1:], n=5)
    l.trazo([(13.6, 62.4), (40, 67.6), (60, 68.2), (80, 67.4), (100, 64.4), (105.6, 60.6)], [.2, .7, .7, .7, .6, .2], color='0C3A33',
            alfa=.75, dentro=c)                                      # la cinta, la franja oscura del costado
    for x in np.arange(24, 100, 7.2):                                # las portas
        l.mancha(poli([(x, 63.2), (x + 2, 63.4), (x + 2, 65.2), (x, 65)], .12), '0C3A33', .6, dentro=c)
    for x in (15.4, 19.4):                                          # las ventanas de la cámara, en la aleta de popa
        l.mancha(poli([(x, 57.2), (x + 2.6, 57.6), (x + 2.6, 60), (x, 59.6)], .12), '0C3A33', .7, dentro=c)
    l.trazo([(13, 55.2), (22, 58.8)], [.1, .3, .1], color='E8B952', alfa=.9, dentro=c)
    # la cabra, en cubierta, junto al palo mayor
    cabra = [forma([(66, 60.8), (66.6, 58.4), (70.4, 58), (71.6, 56.2), (72.8, 55.8), (73.4, 57), (72.2, 58.6), (71.4, 60.8)], 2)]
    cabra += [tubo([(x, 60.2), (x, 61.8)], [.28, .24], 4) for x in (66.6, 67.6, 70, 71)]
    l.masa(cabra, material='claro', alto=.35, brillo=.1, vientre=0, hondo=0, linea=.3, arroja=False)
    l.trazo([(72.6, 55.8), (72, 54.6), (71.2, 54.4)], [.18, .12, .04], alfa=.9)
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(12, 76), (104, 76), (100, 80.4), (18, 80.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
