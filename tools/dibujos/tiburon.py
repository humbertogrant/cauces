# -*- coding: utf-8 -*-
"""Tiburcio, el tiburón toro (Carcharhinus leucas), de memoria: cuerpo grueso y pesado, hocico corto, romo y redondeado (más ancho
que largo), ojos chicos, cinco hendiduras branquiales delante de la aleta pectoral, primera aleta dorsal grande y triangular que
nace sobre el final de la pectoral, segunda dorsal chica, pectorales grandes y anchas, la boca debajo en media luna y la cola con
el lóbulo de arriba más largo. Gris arriba y blanco abajo.
"""
import numpy as np
from shapely.geometry import Polygon

from _perfil import Perfil
from pintor import AGUA

VISTA = (0, 16, 120, 62)
S = [0.000, 0.015, 0.040, 0.080, 0.120, 0.160, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.720]
ARRIBA = [0.034, 0.046, 0.062, 0.078, 0.090, 0.099, 0.106, 0.112, 0.114, 0.112, 0.106, 0.097, 0.085, 0.071, 0.056, 0.042, 0.032, 0.030]
ABAJO = [0.028, 0.036, 0.050, 0.064, 0.076, 0.086, 0.094, 0.101, 0.104, 0.103, 0.097, 0.087, 0.074, 0.060, 0.046, 0.034, 0.026, 0.025]
F = Perfil(S, ARRIBA, ABAJO, 100, giros=((0, 2), (.5, 0), (1, -3)))


def a(s):
    return float(F.arriba(s))


def b(s):
    return float(F.abajo(s))


def dorsal1():
    return F.pieza([(0.262, a(.262) - .012), (0.29, a(.29) + .06), (0.318, a(.318) + .112), (0.33, a(.33) + .124),
                    (0.338, a(.338) + .116), (0.346, a(.346) + .085), (0.362, a(.362) + .045), (0.382, a(.382) + .018),
                    (0.405, a(.405) + .004), (0.39, a(.39) - .012)], 1)


def dorsal2():
    return F.pieza([(0.575, a(.575) - .008), (0.59, a(.59) + .026), (0.6, a(.6) + .03), (0.61, a(.61) + .014),
                    (0.635, a(.635) + .004), (0.625, a(.625) - .008)], 1)


def cola():
    return F.pieza([(0.69, 0.034), (0.76, 0.06), (0.84, 0.098), (0.92, 0.138), (0.975, 0.165), (0.99, 0.162), (0.975, 0.138),
                    (0.955, 0.12), (0.945, 0.104), (0.9, 0.06), (0.87, 0.03), (0.86, 0.0), (0.88, -0.04), (0.9, -0.075),
                    (0.905, -0.098), (0.885, -0.095), (0.84, -0.07), (0.79, -0.045), (0.74, -0.03), (0.69, -0.026)], 1)


def pectoral():
    return F.pieza([(0.222, -0.05), (0.262, -0.084), (0.31, -0.124), (0.35, -0.158), (0.374, -0.178), (0.37, -0.162),
                    (0.36, -0.142), (0.345, -0.122), (0.326, -0.104), (0.306, -0.089), (0.29, -0.078), (0.262, -0.062)], 2)


def pelvica():
    return F.pieza([(0.468, -b(.468) + .01), (0.49, -b(.49) - .03), (0.52, -b(.52) - .046), (0.528, -b(.528) - .036),
                    (0.512, -b(.512) - .01), (0.5, -b(.5) + .006)], 1)


def anal():
    return F.pieza([(0.6, -b(.6) + .008), (0.615, -b(.615) - .022), (0.632, -b(.632) - .03), (0.64, -b(.64) - .02),
                    (0.648, -b(.648) + .004)], 1)


def todo():
    return [F.cuerpo(roma=.6), dorsal1(), dorsal2(), cola(), pectoral(), pelvica(), anal()]


F.encuadrar(todo, (8, 27, 112, 75))


def dibujar(l):
    fin = dict(alto=.35, brillo=.14, vientre=.2, linea=.72, hondo=0)
    l.masa(dorsal1(), **fin)
    l.masa(dorsal2(), **fin)
    l.masa(anal(), **fin)
    l.masa(cola(), **fin)
    corte = Polygon(F.linea([(0.705, 0.2), (0.74, 0.2), (0.74, -0.2), (0.705, -0.2)]))
    cuerpo = l.masa(F.cuerpo(roma=.6), brillo=.3, vientre=.9, sin_tinta=corte,
                    bultos=[(F.pieza([(0.01, .02), (0.08, .07), (0.16, .07), (0.16, -.05), (0.07, -.05), (0.01, -.02)]), .2)])
    for i, s in enumerate(np.linspace(.172, .228, 5)):          # las cinco hendiduras branquiales
        l.trazo(F.linea([(s, 0.036 - .002 * i), (s + .004, 0.0), (s + .002, -0.036 + .003 * i)]), [.2, .42, .2], alfa=.55, dentro=cuerpo)
    l.masa(pelvica(), **dict(fin, raices=[(*F.P(.49, -b(.49)), 1.0, 2.6)]))
    l.masa(pectoral(), alto=.4, brillo=.14, vientre=.2, linea=.72, raices=[(*F.P(.235, -.07), 1.4, 3.6)], hondo=0)


CARA = dict(ojo=F.p(.078, .02), k=1.2, boca=F.p(.075, -.05), kb=3.0, giro=round(-F.grados(.075)) + 10, pb=.5, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 16, 1), round(CARA['ojo'][1] - 16, 1), 34, 34]
FONDO = '<path d="M4 22q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M20 26.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
LISTO = True
