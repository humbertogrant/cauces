# -*- coding: utf-8 -*-
"""Mana, el manatí africano (Trichechus senegalensis), de memoria, nadando despacio hacia las plantas del fondo: cuerpo grande,
redondo y largo, sin cuello marcado (apenas unos pliegues de piel), piel gruesa y arrugada, con pelos sueltos y alguna mancha de
algas en el lomo; la cabeza chica con un hocico grande y cuadrado, vuelto hacia abajo para pastar: el labio de arriba, ancho,
partido al medio y cubierto de cerdas duras, con el que agarra las plantas; las narinas arriba de la punta del hocico, que se
cierran bajo el agua; ojos diminutos; dos aletas delanteras largas, como remos, con uñas en la punta, y ninguna pata de atrás; la
cola, una paleta grande, redonda y horizontal (se ve un poco desde arriba, para que se vea ancha).
"""
import numpy as np

from pintor import AGUA, forma, ovalo

VISTA = (0, 8, 120, 72)


def cuerpo():
    return forma([(26.4, 55.2), (30, 50.4), (38, 43.4), (50, 36.8), (62, 33.6), (74, 33.2), (84, 35), (89.6, 37.4), (95, 38.4),
                  (100.8, 40.4), (104.4, 42.6), (106.6, 45.6), (107.4, 49.4), (106.6, 53), (104, 55.2), (101, 54.4), (99, 55.4),
                  (96.6, 55), (92, 53.8), (84, 55.8), (72, 59.2), (60, 60.8), (48, 59.4), (38, 56.2), (30.8, 56.8)], 3)


def cola():
    """la paleta: ancha y redonda, un poco desde arriba; nace del pedúnculo"""
    return forma([(30.4, 53.2), (26, 50.8), (18.6, 50.4), (10.4, 52.8), (4.6, 57.4), (4, 62.6), (8, 66), (15.6, 66.6),
                  (23.4, 63.8), (28.8, 59.4), (31.6, 57)], 3)


def aleta(lejos=False):
    """la aleta, como un remo: angosta en la raíz, ancha y redonda en la punta"""
    if lejos:
        return forma([(90.6, 53.6), (93.4, 53.4), (94.4, 57.6), (94.4, 62), (92.6, 64), (90.6, 62.4), (90.2, 57.6)], 3)
    return forma([(83.6, 53.4), (88.8, 53.6), (88.8, 56.4), (87.8, 62), (85.8, 67.2), (82.8, 69.4), (79.8, 68.2), (79.6, 64.2),
                  (81.6, 58.6), (83, 55.4)], 3)


def dibujar(l):
    l.masa(aleta(True), material='lejos', alto=.4, brillo=.08, vientre=0, linea=.7, hondo=0)
    # el cuerpo y la paleta, en un solo volumen (la paleta más chata)
    c = l.masa([cuerpo(), cola()], brillo=.12, vientre=.08, contraluz=.3, hondo=.15,
               bultos=[(ovalo(102, 49, 6.2, 5.8), .42), (ovalo(62, 45, 24, 11), .25), (ovalo(95.2, 44.2, 4, 3.6), .15),
                       (ovalo(15, 58.6, 12, 7.6, 18), -.18)])
    for k in range(3):                                                                         # los pliegues de la paleta
        l.trazo([(26 - k * 4.4, 53 + k * .6), (21 - k * 4.4, 58.4 + k * .3), (22 - k * 4.4, 63.6 - k * .6)], [.1, .22, .1],
                alfa=.18, dentro=c, difuso=.1)
    # las manchas de algas en el lomo, suaves
    for x, y, rx, ry in ((58, 37.8, 7, 2.6), (72, 36.4, 5, 2), (46, 42, 4.4, 2.2)):
        l.mancha(ovalo(x, y, rx, ry, -8), '1C6659', .16, dentro=c, difuso=1)
    # la piel arrugada: pliegues en arco en el cuello y arrugas finas en el cuerpo
    for k, x in enumerate((86.4, 89, 91.4)):
        l.trazo([(x - 1.2, 36.4 + k * .4), (x + .4, 44 + k * .2), (x - .8, 52.6)], [.1, .26, .1], alfa=.3 - k * .05, dentro=c,
                difuso=.08)
    rng = np.random.default_rng(4)
    for _ in range(26):
        x, y = rng.uniform(36, 82), rng.uniform(38, 57)
        a = rng.uniform(-.4, .4)
        l.trazo([(x - 1.6, y - .3 + a), (x, y), (x + 1.6, y - .3 - a)], [.06, .16, .06], alfa=.2, dentro=c, difuso=.06)
    for _ in range(46):                                                                        # pelos sueltos
        x, y = rng.uniform(34, 98), rng.uniform(36, 58)
        l.mancha(ovalo(x, y, .13, .13), '0C3A33', .35, dentro=c)
    # el hocico: el labio de arriba partido al medio y con cerdas; las narinas arriba de la punta
    l.trazo([(107, 47.4), (106.2, 51), (104.6, 54.2)], [.1, .34, .1], alfa=.5, dentro=c, difuso=.08)
    for _ in range(40):
        a = rng.uniform(0, 2 * np.pi)
        r = np.sqrt(rng.uniform(0, 1))
        x, y = 103.4 + 3.6 * r * np.cos(a), 50.8 + 3.6 * r * np.sin(a)
        l.mancha(ovalo(x, y, .16, .16), '0C3A33', .55, dentro=c)
    for dx in (0, 1.6):
        l.mancha(forma([(102.6 + dx, 41.6 + dx * .4), (103.8 + dx, 41.2 + dx * .4), (104.4 + dx, 42.2 + dx * .4),
                        (103.2 + dx, 42.2 + dx * .4)], 2), '0C3A33', .75, dentro=c)
    a = l.masa(aleta(), alto=.45, brillo=.1, vientre=0, linea=.75, hondo=0, raices=[(86.2, 53.2, 1.6, 4.2)])
    for k in range(3):                                                                         # las arrugas de la aleta
        l.trazo([(82.2 - k * .8, 56.4 + k * 3.4), (85.2 - k * .9, 56.2 + k * 3.6), (88 - k * 1, 57.2 + k * 3.6)], [.08, .2, .08],
                alfa=.22, dentro=a, difuso=.06)
    for x, y in ((81, 68.8), (83.2, 68.8), (85.2, 67.4)):                                      # las uñas de la punta
        l.masa(ovalo(x, y, .75, .55, -30), material='claro', alto=.2, brillo=0, linea=.3, arroja=False, hondo=0, contraluz=0)


CARA = dict(ojo=[95.6, 42.8], k=1.0, boca=[101.4, 54.4], kb=1.4, giro=-14, pb=.6, wb=.6)
CARA['marco'] = [80.0, 30.0, 30, 30]
FONDO = ('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0"' + AGUA + '/>'
         '<path d="M100 80q-2-10 2-18M104.5 80q1-8-1.5-14M109 80q-1-11 3-21M113.5 80q1.5-8 0-13" style="fill:none;stroke:var(--verde-medio);'
         'stroke-width:1.6;stroke-linecap:round;opacity:.5"/>')
LISTO = True
