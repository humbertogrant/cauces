# -*- coding: utf-8 -*-
"""Pico, el ornitorrinco (Ornithorhynchus anatinus), de memoria y visto desde arriba, nadando: así se reconoce, porque de perfil el
pico y la cola, que son anchos y chatos, se ven finos. El cuerpo chato y ancho, de pelo denso y lustroso, con la cabeza que sigue al
cuerpo sin cuello marcado, apenas doblado al nadar; el pico ancho y chato, de goma, más ancho hacia la punta, que es redonda, como el
de un pato (dorado, como en la ilustración de antes), con un escudo de piel en la base que se monta sobre la frente, las dos narinas
juntas arriba, cerca de la punta, y los poros finos con que siente la electricidad de sus presas; los ojos chicos, uno a cada lado,
en un surco justo detrás del pico donde también está el oído, sin orejas por fuera; las patas de adelante, cortas, salen a los
costados y reman con una membrana ancha que pasa más allá de las uñas (una se estira hacia adelante y la otra empuja hacia atrás);
las de atrás, con uñas y la membrana a medias, van hacia atrás junto a la cola, de timón; la cola ancha y chata, como la de un
castor pero peluda, donde guarda grasa. Desde arriba se le ven los dos ojos.
"""
import math

import numpy as np
from shapely.ops import transform

from _patas import garra
from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 10, 120, 72)
EJE = 45.8                                  # la línea del lomo, antes de doblarlo


def doblar_y(x, y):
    """el cuerpo, apenas doblado en ese de lado a lado, como cuando nada: la cola baja un poco y la cabeza sube"""
    return y + 2.2 * np.sin(np.pi * (np.asarray(x) - 62) / 110) * -1


def D(pts):
    return [(x, float(doblar_y(x, y))) for x, y in pts]


def G(g):
    return transform(lambda x, y, z=None: (x, doblar_y(x, y)), g)


def cuerpo():
    """la cabeza, el cuerpo y la cola: la cola es una paleta ancha, con una cintura apenas marcada"""
    return G(forma([(96.6, 41.2), (93, 40.2), (89, 39.6), (85, 38.8), (80, 37.6), (72, 35.8), (64, 34.8), (56, 34.4), (49, 34.6),
                    (43.4, 36), (39, 39.4), (35.4, 39.6), (30, 38.4), (24.4, 38.2), (19.6, 39.4), (16.6, 42.4), (16, 46.2),
                    (16.8, 49.6), (19.8, 52.4), (24.6, 53.6), (30, 53.4), (35.4, 52.2), (39, 52.4), (43.4, 55.8), (49, 57.2),
                    (56, 57.4), (64, 57), (72, 56), (80, 54.2), (85, 52.8), (89, 52), (93, 51.4), (96.6, 50.4)], 3))


def pala():
    """el pico: ancho y chato, más ancho hacia la punta"""
    return G(forma([(96.4, 41), (100.2, 40.2), (104.4, 39.6), (108.2, 39.8), (110.8, 41.4), (111.8, 44), (111.9, 45.8),
                    (111.8, 47.6), (110.8, 50.2), (108.2, 51.8), (104.4, 52), (100.2, 51.4), (96.4, 50.6)], 3))


def escudo():
    """el escudo de piel de la base del pico, que se monta sobre la frente"""
    return G(forma([(93.8, 41.8), (95.2, 39.8), (97.4, 39.8), (97.8, 45.8), (97.4, 51.8), (95.2, 51.8), (93.8, 49.8), (94.6, 45.8)], 3))


def pata_palmeada(muneca, grados, largo, abanico, n=5, fuera=1.2):
    """una mano o un pie de nadador: los dedos se abren en abanico desde la muñeca y la membrana los une (el borde, en festón
    entre las puntas); `fuera`: cuánto pasa la membrana más allá de la punta de los dedos. Devuelve la membrana y las puntas."""
    m = np.asarray(muneca, float)
    g = math.radians(grados)
    eje = np.array([math.cos(g), math.sin(g)])
    borde, puntas = [], []
    for k in range(n):
        f = k / (n - 1) - .5
        a = math.radians(grados + abanico * f)
        d = np.array([math.cos(a), math.sin(a)])
        L = largo * (1 - .2 * abs(f) * 2)
        if k:
            am = math.radians(grados + abanico * (f - .5 / (n - 1)))
            borde.append(m + np.array([math.cos(am), math.sin(am)]) * L * fuera * .84)
        borde.append(m + d * L * fuera)
        puntas.append((m + d * L, math.degrees(a)))
    a0, a1 = math.radians(grados - abanico / 2 - 25), math.radians(grados + abanico / 2 + 25)
    antes = m + np.array([math.cos(a0), math.sin(a0)]) * largo * .32
    despues = m + np.array([math.cos(a1), math.sin(a1)]) * largo * .32
    return forma([m - eje * .9, antes] + borde + [despues], 2), puntas


# las patas: hombro o cadera, muñeca o tobillo, hacia dónde abren los dedos, largo de los dedos y abanico (antes de doblar el cuerpo)
MANOS = [((80.4, 39.4), (82.2, 34.4), -58, 7.4, 92), ((78.4, 52.6), (76.2, 57.6), 124, 7.4, 92)]
PIES = [((44.4, 38.8), (41.6, 34.2), -156, 5.8, 60), ((44.4, 53.2), (41.6, 57.8), 156, 5.8, 60)]


def dibujar(l):
    # las patas van debajo del cuerpo: salen de los costados
    for (h, w, g, largo, ab), fuera, radios, sem in ([(p, 1.22, (2.4, 1.8), 3) for p in MANOS] +
                                                     [(p, .9, (2.5, 1.7), 4) for p in PIES]):
        h, w = D([h, w])
        brazo = tubo([h, ((h[0] + w[0]) / 2, (h[1] + w[1]) / 2), w], [radios[0], (radios[0] + radios[1]) / 2, radios[1]])
        palma, puntas = pata_palmeada(w, g, largo, ab, fuera=fuera)
        m = l.masa([brazo, palma], alto=.4, brillo=.12, vientre=0, linea=.7, hondo=0, contraluz=.2)
        l.pelaje(m, densidad=2, largo=1.2, ancho=.15, alfa=.22, semilla=sem, claro=.35,
                 zona=brazo, flujo=math.degrees(math.atan2(w[1] - h[1], w[0] - h[0])))
        for q, gg in puntas:
            l.trazo([w, q], [.32, .14], alfa=.22, dentro=m, difuso=.12)                       # los dedos bajo la membrana
            l.masa(garra(q, gg, .8 if fuera > 1 else .75, .26), material='oscuro', alto=.1, brillo=0, vientre=0, linea=0,
                   tinta=False, arroja=False, hondo=0)
        l.mancha(palma.difference(ovalo(w[0], w[1], largo * .8, largo * .8)), 'D2F2DA', .3, dentro=m, difuso=.3)  # la membrana
    c = l.masa(cuerpo(), alto=.6, brillo=.2, vientre=0, contraluz=.25,
               bultos=[(G(ovalo(88, EJE, 6.6, 5.4)), .3), (G(ovalo(56, EJE, 20, 9.4)), .2)])
    # el pelo denso y lustroso, alisado por el agua hacia atrás; en la cola, más corto y áspero
    l.pelaje(c, densidad=2.2, largo=1.9, ancho=.17, alfa=.28, semilla=6, claro=.4, curva=5, desvio=5, zona=G(ovalo(68, EJE, 30, 14)),
             flujo=lambda x, y: 180 + (y - doblar_y(x, EJE)) * 1.6)
    l.pelaje(c, densidad=3, largo=1.1, ancho=.17, alfa=.3, semilla=7, claro=.35, curva=4, desvio=12,
             zona=forma([(38, 30), (8, 30), (8, 62), (38, 62)], 1), flujo=lambda x, y: 180 + (y - doblar_y(x, EJE)) * 2.4)
    # los surcos de la cara, donde están los ojos y los oídos
    for s in (-1, 1):
        l.trazo(D([(93.8, EJE + s * 4.6), (90.6, EJE + s * 4.3), (87.4, EJE + s * 4.6), (84.8, EJE + s * 5.2)]), [.1, .32, .28, .06],
                alfa=.5, dentro=c, difuso=.1)
        l.mancha(G(ovalo(86.2, EJE + s * 4.9, .7, .28, s * 8)), '0C3A33', .55, dentro=c)            # el oído, una ranura
    e = l.masa(escudo(), material='acento', alto=.3, brillo=.25, vientre=0, linea=.7, hondo=0, contraluz=.2)
    b = l.masa(pala(), material='acento', alto=.25, brillo=.4, vientre=0, linea=.8, hondo=0, contraluz=.25,
               sin_tinta=escudo().buffer(-.5))
    # el borde del pico de arriba, que monta sobre el de abajo; las narinas juntas cerca de la punta; los poros finos
    l.mancha(pala().difference(pala().buffer(-1)), '93701A', .3, dentro=b, difuso=.4)
    for s in (-1, 1):
        l.mancha(G(ovalo(108, EJE + s * 1.1, .55, .2, s * 14)), '0C3A33', .6, dentro=b)
    rng = np.random.default_rng(9)
    for _ in range(40):
        x, y = rng.uniform(99, 110), rng.uniform(40.6, 51)
        if ((x - 104.6) / 6.4) ** 2 + ((y - EJE) / 5.2) ** 2 < 1:
            l.mancha(G(ovalo(x, y, .16, .16)), '93701A', .4, dentro=b)


_o = D([(91, 49.8), (91, 41.8)])
CARA = dict(ojo=[round(_o[0][0], 1), round(_o[0][1], 1)], ojo2=[round(_o[1][0], 1), round(_o[1][1], 1)], k=1.3, vista='arriba')
CARA['marco'] = [79.0, 29.0, 30, 30]
FONDO = ('<path d="M6 18q4.5-2.4 9 0t9 0t9 0M40 14q4.5-2.4 9 0t9 0t9 0M96 20q4.5-2.4 9 0t9 0M4 70q4.5-2.4 9 0t9 0t9 0t9 0'
         'M58 74q4.5-2.2 9 0t9 0t9 0M100 68q4.5-2.2 9 0t9 0"' + AGUA + '/>'
         '<circle cx="115" cy="37" r="1.2"' + AGUA + '/><circle cx="117.4" cy="33.4" r=".8"' + AGUA + '/>')
LISTO = True
