# -*- coding: utf-8 -*-
"""La balsa de rafting del Reventazón, de memoria: una balsa inflable de goma, corta y ancha, de tubos gordos que se levantan en la
proa y en la popa, con la cuerda de seguridad alrededor, sujeta a las argollas, y los travesaños inflados por dentro; los remos de
mango en T y los cascos. Baja por un rápido, entre piedras y espuma: el Reventazón es uno de los ríos de rafting más famosos de
América y fue sede del mundial de 1998 (NAVES.reventazon).
"""
import numpy as np

from _barcas import ESPUMA, olas_fondo, poli
from pintor import forma, ovalo, tubo

VISTA = (4, 42, 112, 38)
AGUA_Y = 70.0


def remo_t(l, p0, p1, material='oscuro'):
    """un remo de rafting: la caña, el mango en T y la pala ancha"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    e = np.array([-d[1], d[0]])
    cana = tubo([p0, p1 - d * 4], [.34, .32], 6)
    t = tubo([p0 - e * 1.4, p0 + e * 1.4], [.42, .42], 4)
    pala = forma([p1 - d * 5 + e * .5, p1 - d * 3.2 + e * 1.4, p1 + e * 1.2, p1 + d * .3, p1 - e * 1.2, p1 - d * 3.2 - e * 1.4,
                  p1 - d * 5 - e * .5], 2)
    return l.masa([cana, t, pala], material=material, alto=.3, brillo=.3, vientre=0, hondo=0, linea=.35)


def dibujar(l):
    # la piedra del rápido, detrás, con el agua que la rompe
    l.masa(forma([(88, 70.4), (91, 62.4), (98, 58.6), (106, 59.8), (111.6, 64.6), (113, 70.6)], 2), material='lejos', alto=.7,
           brillo=.15, vientre=0, hondo=0, linea=.55)
    # el tubo de allá asoma por encima; los travesaños y los cascos, por dentro
    l.masa(forma([(22, 55.4), (30, 54.4), (58, 54.6), (80, 54), (90, 52.8), (92, 55.4), (90, 58), (24, 58)], 2), material='acento',
           alto=.4, brillo=.2, vientre=0, hondo=0, linea=.5)
    for x in (42, 58, 74):
        l.masa(ovalo(x, 58, 2.8, 2), material='acento', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.4, arroja=False)
    for x in (35, 50, 66, 81):
        l.masa(ovalo(x, 57.6, 2.8, 2).intersection(poli([(x - 3, 54.6), (x + 3, 54.6), (x + 3, 58), (x - 3, 58)], 0)), material='claro',
               alto=.6, brillo=.4, vientre=0, hondo=0, linea=.35, arroja=False)
    remo_t(l, (44, 48.4), (70, 60))
    # el tubo de este lado, gordo, con las puntas que se levantan
    t = l.masa([tubo([(15.6, 54.2), (20, 60), (34, 63.2), (58, 64), (82, 63.2), (94, 59.8), (98.4, 53.4)], [3.6, 4.1, 4.3, 4.3, 4.3, 4.1, 3.5])],
               material='acento', alto=.85, brillo=.35, vientre=0, hondo=0, contraluz=.25, linea=.7)
    argollas = [(17.6, 57.4), (26, 61.6), (38, 63), (50, 63.4), (62, 63.4), (74, 63), (86, 61.6), (95.6, 57.2)]
    for (x0, y0), (x1, y1) in zip(argollas[:-1], argollas[1:]):
        l.trazo([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 1.6), (x1, y1)], .24, color='F0F6F4', alfa=.9, dentro=t)
    for x, y in argollas:
        l.mancha(ovalo(x, y, .65, .65), '0C3A33', .85, dentro=t)
    l.trazo([(22, 65), (58, 66.8), (92, 64.6)], [.1, .3, .1], color='93701A', alfa=.4, dentro=t, difuso=.2)
    remo_t(l, (74, 47.4), (92, 68.4))
    # el agua blanca del rápido: la ola que levanta la proa, la espuma alrededor y las salpicaduras
    for x, y, rx, ry in ((10, 68.4, 8, 3), (22, 70, 10, 2.4), (46, 70.4, 13, 2), (72, 70.2, 11, 2.4), (98, 68.8, 9, 3.6),
                         (104, 63.4, 4, 2.2), (112, 69.6, 6, 2.8), (100, 58.6, 2.4, 1.4)):
        l.mancha(ovalo(x, y, rx, ry), ESPUMA, .95, difuso=.4)
    for x, y, r in ((100, 50.4, 1), (103.4, 53, .8), (97, 48.6, .7), (106, 56.4, .9), (11, 60.6, .8), (7, 63, 1), (14, 58, .6)):
        l.mancha(ovalo(x, y, r, r), ESPUMA, .95, difuso=.12)
        l.trazo([(x - r * .8, y + r * .2), (x, y + r * 1.1), (x + r * .8, y + r * .2)], .12, color='64C8AA', alfa=.6)
    rng = np.random.default_rng(3)
    for _ in range(16):
        x = rng.uniform(6, 114)
        l.trazo([(x, 72 + rng.uniform(-.6, .6)), (x + 3, 71.3), (x + 6, 72)], .22, color='64C8AA', alfa=.75, difuso=.05)


FONDO = olas_fondo(AGUA_Y, x0=6, x1=114)
LISTO = True
