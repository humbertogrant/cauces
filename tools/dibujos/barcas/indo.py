# -*- coding: utf-8 -*-
"""La barca mohana del Indo, de memoria: fondo plano y casco largo de tablas, con la proa que sube larga y curva; en cubierta, la
casa de los mohana, el pueblo del río en Sind que vive, pesca y comercia a bordo: paredes y techo de esteras de junco sobre una
armazón; un palo con una vela, la que aprovecha el viento, y una pértiga larga para los bajíos (NAVES.indo).
"""
import numpy as np

from _barcas import agua, cabo, caja, casco, esteras, olas_fondo, palo, poli, tablas, vela
from pintor import forma

VISTA = (0, 6, 120, 78)
AGUA_Y = 76.0

ARRIBA = [(12, 58.4), (22, 64.4), (40, 67.6), (60, 68.2), (80, 67.2), (94, 63), (104.8, 54.6), (110.4, 47.4)]
ABAJO = [(16.4, 70.4), (26, 75.4), (40, 78.2), (60, 78.8), (80, 78), (92, 75.4), (100.2, 69.4), (107.6, 50.4)]


def dibujar(l):
    # el palo, la verga y la vela, con la punta de adelante baja
    palo(l, (76, 67.6), (77, 22.4), .85, .6)
    vela(l, [(58.2, 21.2), (79, 14.6), (98, 11.2), (97.4, 25), (92, 42), (84.4, 57.6), (62, 57.2), (60.8, 42), (59.6, 30)],
         [((62 + k * 5.4, 19.6 - k * 1.3), (64 + k * 4.4, 56.8)) for k in range(6)])
    palo(l, (56.4, 22), (100, 10.4), .65, .45)
    palo(l, (61, 57.8), (86.2, 57.8), .5, .45)
    cabo(l, [(99.6, 11), (104.6, 53.2)])
    cabo(l, [(62, 57.8), (58, 67.2)])
    # la casa de esteras: paredes y techo curvo, con su puerta
    casa = l.masa(poli([(22.6, 66), (22.6, 50.4), (52.6, 50.4), (52.6, 67.6)], .3), material='vientre', alto=.3, brillo=.05,
                  vientre=0, hondo=0, linea=.55)
    esteras(l, casa, paso=1.1, alfa=.3)
    l.mancha(caja(40.4, 55.6, 46.2, 67.4, .2), '0C3A33', .7, dentro=casa)
    techo = l.masa(forma([(19.4, 51.8), (21.2, 45.4), (27.6, 41.6), (37.6, 40.4), (47.6, 41.6), (54, 45.4), (55.8, 51.8)], 2),
                   material='lejos', alto=.35, brillo=.08, vientre=0, hondo=0, linea=.55)
    esteras(l, techo, paso=1.3, alfa=.3, color='A4DCC4')
    for x in np.arange(24, 54, 5.6):
        l.trazo([(x, 43.4 - abs(x - 37.6) * .05), (x - .2, 51.2)], [.2, .28, .2], color='0D3530', alfa=.45, dentro=techo)
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA[:-1], ABAJO[:-1], n=4)
    l.mancha(forma([(104.8, 54.6), (110.4, 47.4), (111.4, 48.8), (106.6, 55.8)], 1), '0C3A33', .5, dentro=c, difuso=.2)
    # la pértiga, apoyada en la borda
    palo(l, (6.6, 38.4), (34.4, 82), .45, .45)
    agua(l, AGUA_Y, sombra=forma([(14, 76), (104, 76), (98, 80.6), (20, 80.6)], 1))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
