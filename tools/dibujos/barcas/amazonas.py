# -*- coding: utf-8 -*-
"""El regatão del Amazonas, de memoria: la barca del vendedor ambulante de la Amazonía, de casco de madera con la borda pintada, un
techo de tablas sobre postes que cubre casi toda la cubierta, las hamacas colgadas debajo, la timonera adelante y una bodega que se
llena y se vacía en cada caserío: compra caucho, castaña y pescado, y vende sal, jabón y baterías (NAVES.amazonas). En la proa,
sacos de castaña, el caucho en bolas y cajas de lo que vende.
"""
import numpy as np

from _barcas import agua, caja, cabina, casco, fardo, olas_fondo, poli, tablas
from pintor import forma, ovalo, tubo

VISTA = (0, 35, 120, 47)
AGUA_Y = 74.0

ARRIBA = [(8.6, 61.8), (20, 64.4), (40, 65.6), (60, 65.8), (80, 65.2), (96, 63.4), (110.4, 58.2)]
ABAJO = [(12, 69), (22, 73.6), (40, 76), (60, 76.4), (80, 75.8), (96, 73.6), (107.4, 66.6)]


def hamaca(l, x0, x1, y, caida, material):
    """una hamaca colgada: la tela que cae en curva entre dos cuerdas"""
    pts = [(x0, y), (x0 + (x1 - x0) * .25, y + caida * .8), (x0 + (x1 - x0) * .5, y + caida), (x0 + (x1 - x0) * .75, y + caida * .8),
           (x1, y)]
    abajo = [(x, yy + 1.3) for x, yy in pts[::-1]][1:-1]
    h = l.masa(forma(pts + abajo, 2), material=material, alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35, arroja=False)
    for k in (1, 2):
        l.trazo([(x0 + .6, y + .4), (x0 + (x1 - x0) * .5, y + caida + .4 * k), (x1 - .6, y + .4)], .1, color='0C3A33', alfa=.3, dentro=h)
    return h


def dibujar(l):
    # el techo de tablas y sus postes
    for x in np.arange(14, 92, 9.6):
        l.masa(caja(x - .4, 49.6, x + .4, 64, .1), material='acento', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x0, x1, y, caida, mat in ((15.4, 27.6, 51.4, 6.4, 'vientre'), (28.6, 40.6, 51.4, 5.4, 'claro'), (43.2, 55.4, 51.4, 6.6, 'cuerpo'),
                                   (56.4, 68.4, 51.4, 5.6, 'vientre'), (70.6, 82.6, 51.4, 6, 'claro')):
        hamaca(l, x0, x1, y, caida, mat)
    # la carga en la proa: sacos de castaña, el caucho en bolas y las cajas de lo que vende
    fardo(l, 86.4, 60.6, 5.2, 5, material='vientre')
    fardo(l, 91, 59.4, 5.6, 6, material='claro')
    for x, y in ((98.4, 61.6), (100.8, 61.4), (99.6, 59.6)):
        l.masa(ovalo(x, y, 1.5, 1.4), material='oscuro', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.3, arroja=False)
    for x, y, w, h in ((76.6, 60.8, 4.4, 3.4), (77.2, 57.6, 3.8, 3.2), (81.4, 61.4, 3.6, 2.8)):     # cajas de jabón y de baterías
        cj = l.masa(caja(x, y, x + w, y + h, .2), material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35, arroja=False)
        l.trazo([(x + .5, y + h * .5), (x + w - .5, y + h * .5)], .12, color='2F8A74', alfa=.7, dentro=cj)
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA, ABAJO, n=3)
    # la borda pintada: una franja verde con un filete claro, como las barcas de la Amazonía
    l.mancha(forma(ARRIBA + [(109.6, 60.8), (96, 65.8), (80, 67.6), (60, 68.2), (40, 68), (20, 66.8), (9.4, 64.2)], 1), '2F8A74', .8,
             dentro=c)
    l.trazo([(9.4, 64.4), (20, 67), (40, 68.2), (60, 68.4), (80, 67.8), (96, 66), (109.4, 61)], [.1, .3, .3, .3, .3, .3, .1],
            color='F0F6F4', alfa=.85, dentro=c)
    # el techo de tablas, encima de todo, y la timonera adelante
    t = l.masa(poli([(10.6, 48.6), (96.4, 48.6), (98.4, 50.4), (10.6, 50.4)], .2), material='acento', alto=.25, brillo=.15, vientre=0,
               hondo=0, linea=.5)
    for x in np.arange(16, 96, 5.2):
        l.trazo([(x, 48.8), (x, 50.2)], .1, alfa=.35, dentro=t)
    cabina(l, 84, 40.4, 96, 48.6, ventanas=[(85.6, 42.2, 3.8, 3.2), (90.6, 42.2, 3.8, 3.2)], techo=.8)
    l.masa(tubo([(13.6, 50.4), (13.8, 41.4)], [.5, .45]), material='oscuro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)   # el escape
    agua(l, AGUA_Y, sombra=poli([(10, 74), (108, 74), (104, 78), (14, 78)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
