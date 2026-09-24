# -*- coding: utf-8 -*-
"""Ara, la lapa roja (Ara macao), de memoria, parada en una rama: cuerpo erguido y un poco inclinado hacia adelante, la cabeza
redonda con la cara blanca y sin plumas alrededor del ojo, el pico grande y ganchudo (claro arriba, oscuro abajo), el ala doblada
con su franja amarilla (dorada: el único detalle de ese color) y las plumas largas de la punta; la cola larguísima, en punta, que
cuelga por debajo de la rama; las patas cortas con dos dedos adelante y dos atrás, agarrando la rama.
"""
import numpy as np
from shapely.geometry import Point

from pintor import forma, ovalo, tubo

VISTA = (20, 6, 80, 82)


def cuerpo():
    return forma([(64.5, 12.5), (70, 10), (75, 11.5), (77.5, 15), (77.2, 20), (74.5, 25), (72, 30.5), (70.4, 37.5), (68.5, 44),
                  (65, 49), (60.5, 51.2), (56, 50), (53.5, 45), (53.8, 38), (56, 31), (59.5, 24.5), (62, 18.5)], 3)


def cola():
    return forma([(58.5, 47.5), (54, 56), (48.5, 66), (42, 76.5), (36.5, 85), (34.8, 87.2), (37.4, 86.6), (44, 79.5),
                  (51.5, 69.5), (57.5, 59.5), (61.5, 51)], 3)


def ala():
    return forma([(66, 23.5), (69.5, 28), (70, 35), (67.5, 42), (63, 49), (57.5, 56.5), (52.5, 62.5), (50.2, 61), (51.5, 54),
                  (53.5, 45), (56.5, 35.5), (60.5, 27.5)], 3)


def pico():
    arriba = forma([(76.4, 14), (79.8, 14.4), (82.4, 17), (83.4, 21), (82.6, 25.2), (81, 27.4), (80.6, 24.6), (79, 22.2),
                    (76.4, 21.2)], 2)
    abajo = forma([(76.2, 21.4), (79.2, 22.6), (80.4, 25), (79.6, 27), (77, 27.2), (75.2, 24.8)], 2)
    return arriba, abajo


def cara():
    return forma([(68.5, 13.5), (72.5, 12.2), (76.2, 13.6), (77, 17), (76.6, 21.4), (74.5, 23.5), (71, 22.6), (68.6, 19.5)], 3)


def escamas(l, masa, zona, filas, t=(-.2, 1.0), ancho=1.3, alfa=.3, color='5F8F83', sombra='8EB5AA'):
    """plumitas en escamas: filas de arcos con la punta hacia `t` (hacia donde cae la pluma), sobre `zona`"""
    t = np.array(t) / np.hypot(*t)
    e = np.array([-t[1], t[0]])
    x0, y0, x1, y1 = zona.bounds
    for k, y in enumerate(np.arange(y0 + ancho, y1, ancho * 1.25)):
        for x in np.arange(x0 + (k % 2) * ancho, x1, ancho * 2):
            q = np.array([x, y])
            if not zona.contains(Point(*q)):
                continue
            l.trazo([q + e * ancho - t * .35 * ancho, q + e * ancho * .6 + t * .4 * ancho, q + t * .55 * ancho,
                     q - e * ancho * .6 + t * .4 * ancho, q - e * ancho - t * .35 * ancho], [.04, .1, .14, .1, .04], color=color,
                    alfa=alfa, dentro=masa, difuso=.05)


def dibujar(l):
    t = l.masa(cola(), alto=.3, brillo=.15, vientre=0, linea=.75, hondo=0, contraluz=.2)
    l.mancha(forma([(46, 70), (51.6, 69.4), (44, 79.5), (37.4, 86.6), (34.8, 87.2), (36.5, 85), (42, 76.5)], 2), '164F46', .45,
             dentro=t, difuso=1.2)                                                  # la punta de la cola, más oscura
    for f in (.3, .55, .8):                                                         # las plumas de la cola, en largo
        l.trazo([(59.5 - f * 4, 49.5 + f), (47 - f * 3, 72 + f * 2), (37.5, 85.5)], [.18, .22, .05], alfa=.3, dentro=t)
    c = l.masa(cuerpo(), brillo=.2, vientre=.35, contraluz=.3, bultos=[(ovalo(70.5, 16, 6, 5.5), .5), (ovalo(66, 36, 6, 9), .25)])
    # las plumitas del pecho y de la nuca, en escamas
    escamas(l, c, cuerpo().difference(ala().buffer(.3)).difference(cara().buffer(.6)).buffer(-.5), 0, t=(-.15, 1), ancho=1.25,
            alfa=.32, color='11443F')
    cf = l.masa(cara(), material='claro', alto=.3, brillo=.1, vientre=0, linea=.4, hondo=0, contraluz=0)
    for x, y in ((70.2, 15.4), (70.6, 19.6), (74.6, 21.6)):                        # apenas unas plumitas rojas en la cara blanca
        l.mancha(ovalo(x, y, .22, .16), '2F8A74', .6, dentro=cf)
    a = l.masa(ala(), alto=.35, brillo=.18, vientre=0, linea=.8, hondo=0, contraluz=.25)
    # el ala: las plumas largas de la punta (azules: más oscuras), la franja amarilla de las cubiertas con sus puntas verdes
    punta = ala().difference(forma([(60, 20), (75, 20), (70, 41), (60, 45.4), (52, 44)], 1))
    l.mancha(punta, '164F46', .62, dentro=a, difuso=.6)
    for k, (x0, y0) in enumerate(((66.5, 39.5), (63.5, 44), (60.5, 48.5), (57.5, 53))):
        l.trazo([(x0 + 2, y0 - 2.5), (x0, y0 + 2), (x0 - 4 + k * .3, y0 + 8 - k * .6)], [.15, .28, .1], alfa=.45, dentro=a)
    banda = forma([(66, 23.5), (69.5, 28), (69.6, 33), (66.8, 38.4), (62, 41.6), (58.2, 38.6), (60.5, 31), (63, 26)], 3)
    l.mancha(banda, 'E8B952', .92, dentro=a)                                        # la franja amarilla del ala
    escamas(l, a, banda.buffer(-.6), 0, t=(-.5, 1), ancho=1.9, alfa=.25, color='93701A')
    for x0, y0 in ((66.8, 38.6), (64.2, 40.4), (61.4, 41.4), (59, 39.6)):           # las puntas verdes de las cubiertas
        l.mancha(ovalo(x0, y0, 1.5, .9, -30), '2F8A74', .75, dentro=a, difuso=.15)
    l.mancha(banda.boundary.buffer(.2), '0C3A33', .3, dentro=a)
    arriba, abajo = pico()
    l.masa(abajo, material='oscuro', alto=.4, brillo=.2, vientre=0, linea=.55, hondo=0)
    l.masa(arriba, material='claro', alto=.5, brillo=.3, vientre=0, linea=.6, hondo=0)
    l.mancha(forma([(76.4, 14), (77.6, 14.2), (77.2, 21.2), (76.4, 21.2)], 1), '0C3A33', .6, difuso=.3)   # la base oscura del pico
    l.trazo([(78.5, 15.2), (80.8, 18), (81.5, 21.5)], [.1, .25, .1], alfa=.3)
    # las patas: dos dedos adelante y dos atrás, agarrando la rama
    for x in (60, 64.4):
        l.masa([tubo([(x, 48.5), (x + .3, 51.2)], [1.2, 1.0]), tubo([(x + .3, 51.4), (x + 2.8, 52.4)], [.65, .5]),
                tubo([(x + .3, 51.4), (x + 2.4, 53.6)], [.6, .45]), tubo([(x + .2, 51.4), (x - 2.4, 52.8)], [.6, .45])],
               material='lejos', alto=.4, brillo=.05, vientre=0, linea=.45, hondo=0)


CARA = dict(ojo=[72.4, 16.8], k=1.2)
CARA['marco'] = [57.0, 5.0, 30, 30]
FONDO = ('<path d="M22 53.5Q52 49 98 52.2" style="fill:none;stroke:var(--verde-medio);stroke-width:3;stroke-linecap:round;opacity:.6"/>'
         '<path class="sombra" d="M84 51q4-7 11-6q-2 6-11 6Z" style="opacity:.5"/><path class="sombra" d="M30 53.4q-1-7 5-10q3 6-5 10Z" style="opacity:.5"/>')
LISTO = True
