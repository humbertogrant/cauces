# -*- coding: utf-8 -*-
"""El lanchón de la hidrovía del Paraná, de memoria: barcazas planas, de acero, que viajan en convoy, amarradas unas a otras (hasta
veinte), empujadas por un remolcador: el empujador, de proa chata con los topes para empujar, alto y cuadrado, con la timonera arriba
de todo para ver por encima de la carga; las barcazas, bajas y largas, llenas de soja hasta el borde. Cada convoy carga tanto como
mil camiones (NAVES.parana).
"""
import numpy as np

from _barcas import agua, caja, cabina, olas_fondo, palo, poli
from pintor import forma, ovalo

VISTA = (0, 26, 120, 56)
AGUA_Y = 74.0


def barcaza(l, x0, x1):
    b = l.masa(poli([(x0, 64.8), (x1, 64.8), (x1 + 1.6, 66.4), (x1, 75.2), (x0, 75.2)], .3), material='acento', alto=.3, brillo=.25,
               vientre=0, hondo=0, contraluz=.2)
    l.trazo([(x0 + .4, 67.4), (x1 + .6, 67.4)], [.2, .4, .2], color='0C3A33', alfa=.5, dentro=b)
    for x in np.arange(x0 + 6, x1, 6.4):
        l.trazo([(x, 67.8), (x, 74.8)], .1, alfa=.2, dentro=b)
    # la soja, a granel, que asoma en un lomo sobre la borda
    s = l.masa(forma([(x0 + 1.2, 65), (x0 + 4, 61.8), (x0 + 12, 60.4), (x1 - 12, 60.4), (x1 - 4, 61.8), (x1 - 1.2, 65)], 2),
               material='acento', alto=.25, brillo=.08, vientre=0, hondo=0, linea=.45, arroja=False)
    rng = np.random.default_rng(int(x0))
    for _ in range(int((x1 - x0) * 4)):
        x, y = rng.uniform(x0 + 2, x1 - 2), rng.uniform(61.2, 64.8)
        l.mancha(ovalo(x, y, .28, .22), '93701A', .5, dentro=s)
    return b


def dibujar(l):
    barcaza(l, 70, 116)
    barcaza(l, 30.4, 69.6)
    for x in (30.6, 69.6):                                          # las amarras entre barcazas
        l.trazo([(x - .8, 66.2), (x + .8, 65.2)], .3, alfa=.8)
    # el empujador: casco cuadrado, los topes de proa, la casa y la timonera alta
    c = l.masa(poli([(3.4, 63.2), (28.4, 63.2), (29.4, 64.6), (29.4, 75.4), (6, 75.4), (3, 71)], .4), material='acento', alto=.35,
               brillo=.25, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(3.8, 66.6), (29, 66.6)], [.2, .4, .2], color='0C3A33', alfa=.5, dentro=c)
    for y in (64.6, 70):
        l.masa(caja(28.6, y, 31, y + 3.2, .3), material='oscuro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    cabina(l, 6, 54.8, 25.4, 63.2, ventanas=[(8, 56.8, 3.2, 3), (13, 56.8, 3.2, 3), (18, 56.8, 3.2, 3)], techo=.8)
    cabina(l, 9, 46.4, 23, 53.8, ventanas=[(10, 48.2, 12, 3)], techo=.6)
    cabina(l, 10.4, 36.8, 22, 45.4, ventanas=[(11.4, 38.4, 9.6, 3.6)], techo=1.4)
    for y in (45.4, 53.8):
        l.masa(caja(12, y, 20, y + .8, .1), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    palo(l, (7.6, 54), (7.6, 30.4), .5, .4, material='oscuro')                 # el mástil de las luces
    l.masa(caja(5.8, 31, 9.4, 32, .2), material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(4, 74), (116, 74), (112, 78), (8, 78)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
