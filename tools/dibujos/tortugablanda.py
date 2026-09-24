# -*- coding: utf-8 -*-
"""Rafi, una tortuga de caparazón blando (familia Trionychidae), de memoria y vista desde arriba: el caparazón chato y redondo como
una tortilla, sin escudos duros, cubierto de piel como cuero, salpicado de manchitas oscuras y con el borde blando, más claro, que se
dobla; el cuello largo; la cabeza angosta, con una franja clara detrás del ojo, termina en una nariz en tubo que saca del agua para
respirar, como un esnórquel; las cuatro patas anchas, como abanicos, con membrana entre los cinco dedos y uñas solo en los tres de
adentro; la cola, corta. Vista desde arriba se le ven los dos ojos, juntos y adelante.
"""
import math

import numpy as np

from _patas import garra
from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 6, 120, 80)
EJE = math.radians(8)                       # la cabeza apunta a la derecha y un poco hacia abajo
D = np.array([math.cos(EJE), math.sin(EJE)])
N = np.array([-D[1], D[0]])
C = np.array([96.5, 51.6])                 # el centro de la cabeza


def caparazon():
    return forma([(85, 45.4), (84, 37), (79.4, 29.4), (70, 23.6), (56, 21.8), (42, 23.6), (31.4, 29.4), (25.4, 37.6), (24, 47.4),
                  (25.6, 57.4), (31.6, 65.6), (42.4, 71.6), (56, 73.4), (70, 71.4), (79.6, 65.4), (84.2, 57.6), (85.2, 50.2)], 3)


def disco():
    """la parte dura, debajo de la piel: el lomo sube un poco más ahí"""
    return ovalo(55.4, 47.4, 24, 19.4)


def cabeza():
    cuello = tubo([(80, 48.4), (87.4, 49.6), C - D * 3.4], [5.2, 4.8, 4.1])
    craneo = forma([C - D * 5 + N * 3.9, C + D * 3.4 + N * 3.5, C + D * 8.2 + N * 1.9, C + D * 9.8,
                    C + D * 8.2 - N * 1.9, C + D * 3.4 - N * 3.5, C - D * 5 - N * 3.9], 3)
    nariz = tubo([C + D * 8.8, C + D * 13.4], [1.4, 1.0])
    return cuello, craneo, nariz


def pata(base, grados, brazo, mano, ancho, espejo=False):
    """la pata: el brazo sale de abajo del caparazón y la mano se abre en abanico, con la membrana entre los dedos (el borde, en
    arcos entre las puntas) y uñas en los tres dedos de adentro"""
    a = math.radians(grados)
    d = np.array([math.cos(a), math.sin(a)])
    e = np.array([-d[1], d[0]])
    b = np.asarray(base, float)
    m = b + d * brazo
    tramo = tubo([b, b + d * brazo * .5, m], [ancho * .42, ancho * .4, ancho * .36], 10)
    puntas, borde = [], [m - e * ancho * .36 - d * 1, m - e * ancho * .62 + d * mano * .3]
    for k in range(5):
        f = k / 4 - .5
        ang = a + math.radians(78 * f)
        dd = np.array([math.cos(ang), math.sin(ang)])
        largo = mano * (1 - .16 * abs(f) * 2)
        p = m + dd * largo
        if k:
            ang_m = a + math.radians(78 * (f - .125))
            borde.append(m + np.array([math.cos(ang_m), math.sin(ang_m)]) * largo * .86)
        borde.append(p)
        puntas.append((p, math.degrees(ang), f))
    borde += [m + e * ancho * .62 + d * mano * .3, m + e * ancho * .36 - d * 1]
    mano_ = forma(borde, 3)
    dedos = [(p, g) for p, g, f in puntas if (f < .2 if not espejo else f > -.2)]
    return [tramo, mano_], dedos, (m, puntas)


# base, grados, brazo, mano, ancho; las de adelante apuntan adelante y afuera, las de atrás, atrás y afuera
PATAS = [((73, 30.6), -50, 7.6, 10.4, 8.4, True), ((73, 64.4), 50, 7.6, 10.4, 8.4, False),
         ((35, 31.6), -132, 7, 11.2, 8.8, False), ((35, 63.4), 132, 7, 11.2, 8.8, True)]


def dibujar(l):
    for base, g, brazo, mano, ancho, esp in PATAS:
        partes, dedos, (m, puntas) = pata(base, g, brazo, mano, ancho, esp)
        p = l.masa(partes, alto=.35, brillo=.14, vientre=0, linea=.75, hondo=0, contraluz=.2)
        for q, gg, f in puntas:                                                   # los dedos, como costillas bajo la membrana
            l.trazo([m + (q - m) * .25, m + (q - m) * .85], [.35, .18], color='0C3A33', alfa=.2, dentro=p, difuso=.2)
        for q, gg in dedos:
            l.masa(garra(q, gg, 1.5, .42), material='claro', alto=.1, brillo=0, vientre=0, linea=.25, arroja=False, hondo=0,
                   contraluz=0)
    l.masa(tubo([(28, 47.6), (19.6, 48.8), (15.4, 49.4)], [3.0, 2.0, .55]), alto=.35, brillo=.1, vientre=0, linea=.7, hondo=0)
    cuello, craneo, nariz = cabeza()
    h = l.masa([cuello, craneo, nariz], brillo=.25, vientre=0, linea=.75, hondo=.2,
               bultos=[(ovalo(*(C + D * 1.8), 4.6, 3.2, math.degrees(EJE)), .45)])
    for s in (1, -1):                                                              # la franja clara detrás de cada ojo
        l.trazo([C + D * 4 + N * 2.2 * s, C - D * 1 + N * 2.9 * s, C - D * 6 + N * 3.1 * s], [.35, .5, .3], color='D2F2DA',
                alfa=.4, dentro=h, difuso=.25)
    for s in (1, -1):
        l.mancha(ovalo(*(C + D * 13.2 + N * .5 * s), .32, .24), '0C3A33', .8)          # las narinas, en la punta del tubo
    for k in range(4):                                                                  # los pliegues del cuello
        q = np.array([82 + k * 2.6, 48.8 + k * .3])
        l.trazo([q + N * 3.6, q + D * .6, q - N * 3.6], [.08, .2, .08], alfa=.22, dentro=h, difuso=.08)
    cap = l.masa(caparazon(), alto=.24, brillo=.22, vientre=0, linea=.85, hondo=0, contraluz=.25, escalon=.12,
                 bultos=[(disco(), .12), (ovalo(55, 44, 12, 8), .06)])
    # el borde blando, más claro, que se dobla; las manchitas oscuras del cuero; unas arrugas finas a lo largo
    borde = caparazon().difference(disco().buffer(1))
    l.mancha(borde, 'D2F2DA', .32, dentro=cap, difuso=1.2)
    rng = np.random.default_rng(3)
    for _ in range(95):
        x, y = rng.uniform(27, 83), rng.uniform(24, 71)
        r = rng.uniform(.35, .85)
        if ((x - 55) / 28) ** 2 + ((y - 47.4) / 24) ** 2 < .92:
            l.mancha(ovalo(x, y, r, r * rng.uniform(.7, 1), rng.uniform(0, 180)), '14463C', .42, dentro=cap, difuso=.15)
    for k, y in enumerate((39.4, 47.4, 55.4)):
        l.trazo([(34, y + (y - 47.4) * .3), (55, y), (76, y + (y - 47.4) * .2)], [.1, .4, .1], color='0C3A33', alfa=.1, dentro=cap,
                difuso=.5)
    for x in (30.2, 33, 36):                                                             # el borde que se dobla, atrás
        l.trazo([(x, 36 + (x - 30) * -.8), (x - 3.2, 47.4), (x, 58.8 + (x - 30) * .8)], [.08, .2, .08], alfa=.12, dentro=cap, difuso=.2)


_o1, _o2 = C + D * 5.2 + N * 2.1, C + D * 5.2 - N * 2.1
CARA = dict(ojo=[round(float(v), 1) for v in _o2], ojo2=[round(float(v), 1) for v in _o1], k=1.1, vista='arriba',
            marco=[82.0, 35.0, 32, 32])
FONDO = '<path d="M4 16q4.5-2.4 9 0t9 0t9 0M84 80q4.5-2.4 9 0t9 0t9 0M6 78q4.5-2.2 9 0t9 0"' + AGUA + '/>'
LISTO = True
