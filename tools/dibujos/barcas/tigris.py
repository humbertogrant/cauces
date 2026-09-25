# -*- coding: utf-8 -*-
"""El kelek del Tigris, de memoria: una balsa de troncos de álamo atados en enrejado, que flota sobre docenas de odres de piel de
cabra inflados, amarrados debajo (se ven asomar redondos, con los muñones de las patas atados); sin proa ni popa: dos remos largos,
uno en cada punta, sobre su horquilla; la carga encima. Solo baja: en Bagdad se vende la madera, se desinflan los odres y vuelven a
Mosul a lomo de burro (NAVES.tigris).
"""
import numpy as np

from _barcas import agua, fardo, olas_fondo, palo, poli
from pintor import forma, ovalo, tubo

VISTA = (0, 48, 120, 32)
AGUA_Y = 70.0


def odre(l, x, y, r=3.2, material='lejos'):
    """un odre de piel de cabra inflado: casi una bola, con los muñones de las patas atados"""
    cuerpo = ovalo(x, y, r * 1.12, r * .9)
    patas = [tubo([(x + dx, y + dy), (x + dx * 1.45, y + dy * 1.4)], [.5, .38], 5) for dx, dy in ((-r * .8, -r * .45), (r * .8, -r * .45),
                                                                                                    (-r * .55, r * .7), (r * .55, r * .7))]
    o = l.masa([cuerpo] + patas, material=material, alto=.7, brillo=.25, vientre=0, hondo=0, linea=.4, contraluz=.2)
    l.trazo([(x - r * .5, y - r * .1), (x, y + r * .15), (x + r * .5, y - r * .1)], [.08, .16, .08], color='0C3A33', alfa=.35, dentro=o)
    return o


def dibujar(l):
    rng = np.random.default_rng(2)
    for x in np.arange(18, 104, 6.2):                               # los odres de atrás, más oscuros
        odre(l, x + 3.1, 66.2 + rng.uniform(-.4, .4), 3, material='lejos')
    for x in np.arange(15, 106, 6.8):                               # los de adelante
        odre(l, x, 68.2 + rng.uniform(-.4, .4), 3.3, material='vientre')
    # la carga: sacos, cerámica y papel de Mosul
    for x, y, w, h, m in ((34, 55.4, 7, 5, 'claro'), (41.6, 56.4, 6, 4, 'vientre'), (62, 55, 7.6, 5.4, 'claro'), (70.4, 56, 6.2, 4.4, 'lejos')):
        fardo(l, x, y, w, h, material=m)
    for x in (50.6, 55.4):
        v = l.masa(forma([(x - 1.4, 60.4), (x - 2.2, 57.6), (x - 1.4, 55.4), (x - .6, 54.6), (x + .6, 54.6), (x + 1.4, 55.4),
                          (x + 2.2, 57.6), (x + 1.4, 60.4)], 2), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.35,
                   arroja=False)
    # la plataforma de troncos, con las puntas de los troncos y las ataduras
    p = l.masa(poli([(10.6, 60.4), (108.6, 60.4), (110, 62), (108.6, 64), (10.6, 64), (9.4, 62)], .4), material='acento', alto=.35,
               brillo=.2, vientre=0, hondo=0, contraluz=.2)
    for x in np.arange(12, 108, 7.4):
        l.masa(ovalo(x, 62.2, 1.6, 1.6), material='acento', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.35, arroja=False)
        l.mancha(ovalo(x, 62.2, .9, .9), '93701A', .6)
        l.mancha(ovalo(x, 62.2, .3, .3), '6B4E10', .8)
    for x in np.arange(15.6, 106, 7.4):
        l.trazo([(x, 60.6), (x + .4, 63.8)], .3, color='0C3A33', alfa=.55, dentro=p)
    # los dos remos largos, uno en cada punta, con su horquilla
    for x0, x1, s in ((14, -2, -1), (104, 120, 1)):
        palo(l, (x0, 60.4), (x0, 54.4), .45, .4)
        palo(l, (x0 - s * 5, 52.6), (x1, 68.6), .5, .45)
        l.masa(poli([(x1 - s * 3, 67), (x1, 66.8), (x1 + s * 1, 70.8), (x1 - s * 3.6, 70.4)], .3), material='acento', alto=.3,
               brillo=.2, vientre=0, hondo=0, linea=.4)
    agua(l, AGUA_Y, sombra=poli([(10, 70), (110, 70), (106, 73.4), (14, 73.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
