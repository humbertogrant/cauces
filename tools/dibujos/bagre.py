# -*- coding: utf-8 -*-
"""Buk, el bagre gigante del Mekong (Pangasianodon gigas), de memoria: cuerpo largo y robusto, cabeza ancha de hocico romo y boca
ancha, sin barbas de adulto (las tienen solo de cría), el ojo bajo, a la altura de la comisura; aleta dorsal alta y triangular con
una espina adelante, lejos atrás una aleta adiposa chica y carnosa, la anal de base larga, las pectorales con espina detrás de la
cabeza y la cola muy ahorquillada. Lomo oscuro y panza clara. Nada cerca del fondo del río.
"""
import numpy as np
from shapely.geometry import Polygon

from _perfil import Perfil
from pintor import AGUA

VISTA = (0, 14, 120, 66)
S = [0.000, 0.015, 0.040, 0.080, 0.120, 0.160, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700,
     0.750, 0.800, 0.850, 0.870]
ARRIBA = [0.037, 0.047, 0.060, 0.078, 0.093, 0.105, 0.114, 0.121, 0.125, 0.126, 0.124, 0.119, 0.112, 0.103, 0.093, 0.082,
          0.071, 0.061, 0.053, 0.047, 0.046]
ABAJO = [0.033, 0.042, 0.052, 0.064, 0.076, 0.087, 0.096, 0.104, 0.109, 0.111, 0.110, 0.106, 0.099, 0.090, 0.079, 0.068,
         0.058, 0.048, 0.041, 0.036, 0.036]
F = Perfil(S, ARRIBA, ABAJO, 100, giros=((0, 3), (.5, 0), (1, -4)))


def a(s):
    return float(F.arriba(s))


def b(s):
    return float(F.abajo(s))


def cola():
    return F.pieza([(0.855, 0.046), (0.90, 0.07), (0.95, 0.105), (0.985, 0.133), (1.008, 0.150), (0.992, 0.12), (0.968, 0.075),
                    (0.945, 0.032), (0.934, 0.008), (0.944, -0.018), (0.964, -0.062), (0.986, -0.106), (1.003, -0.137),
                    (0.982, -0.121), (0.948, -0.09), (0.905, -0.058), (0.855, -0.035)], 1)


def dorsal():
    return F.pieza([(0.292, a(.292) - .012), (0.302, a(.302) + .07), (0.314, a(.314) + .124), (0.322, a(.322) + .118),
                    (0.338, a(.338) + .088), (0.356, a(.356) + .052), (0.378, a(.378) + .022), (0.402, a(.402) - .012)], 1)


def adiposa():
    return F.pieza([(0.728, a(.728) - .008), (0.742, a(.742) + .016), (0.766, a(.766) + .021), (0.788, a(.788) + .01),
                    (0.80, a(.80) - .008)], 2)


def anal():
    s = np.linspace(.585, .815, 12)
    hondo = np.interp(s, [.585, .6, .7, .815], [.02, .046, .04, .026])
    return F.pieza(list(zip(s, [-b(v) + .012 for v in s])) + list(zip(s[::-1], [-b(v) - h for v, h in zip(s[::-1], hondo[::-1])])), 2)


def pectoral():
    return F.pieza([(0.196, -0.056), (0.26, -0.083), (0.31, -0.108), (0.328, -0.124), (0.302, -0.126), (0.262, -0.114),
                    (0.226, -0.096), (0.203, -0.076)], 2)


def pelvica():
    return F.pieza([(0.452, -b(.452) + .014), (0.50, -0.116), (0.527, -0.132), (0.505, -0.134), (0.474, -0.12),
                    (0.452, -b(.452) + .002)], 2)


def todo():
    return [F.cuerpo(roma=.55), cola(), dorsal(), adiposa(), anal(), pectoral(), pelvica()]


F.encuadrar(todo, (8, 27, 112, 67))


def radios(l, masa, base, punta, n, alfa=.14):
    """los radios de una aleta: pinceladas finas que van de la base hacia el borde"""
    for t in np.linspace(0, 1, n):
        p0 = np.asarray(base[0]) * (1 - t) + np.asarray(base[1]) * t
        p1 = np.asarray(punta[0]) * (1 - t) + np.asarray(punta[1]) * t
        l.trazo(F.linea([p0, p0 * .45 + p1 * .55, p1]), .2, alfa=alfa, dentro=masa, difuso=.05)


def dibujar(l):
    fin = dict(alto=.25, brillo=.1, vientre=0, linea=.7, hondo=0)
    d = l.masa(dorsal(), **fin)
    radios(l, d, [(0.30, a(.3)), (0.39, a(.39))], [(0.316, a(.316) + .12), (0.40, a(.40) + .004)], 7)
    l.masa(adiposa(), **fin)
    an = l.masa(anal(), **fin)
    radios(l, an, [(0.60, -b(.6)), (0.80, -b(.8))], [(0.60, -b(.6) - .044), (0.81, -b(.81) - .026)], 9)
    c = l.masa(cola(), **fin)
    radios(l, c, [(0.87, 0.03), (0.87, 0.0)], [(1.0, 0.14), (0.99, 0.02)], 6)
    radios(l, c, [(0.87, 0.0), (0.87, -0.025)], [(0.94, -0.02), (0.995, -0.13)], 6)
    corte = Polygon(F.linea([(0.862, 0.2), (0.9, 0.2), (0.9, -0.2), (0.862, -0.2)]))       # sin tinta donde el pedúnculo entra en la cola
    cuerpo = l.masa(F.cuerpo(roma=.55), brillo=.28, vientre=.85, sin_tinta=corte,
                    bultos=[(F.pieza([(0.02, .02), (0.1, .07), (0.19, .07), (0.19, -.05), (0.1, -.05), (0.02, -.015)]), .15)])
    l.trazo(F.linea([(0.866, 0.042), (0.874, 0.02), (0.876, -0.004), (0.872, -0.03)]), .3, alfa=.35, difuso=.06)   # la base de la cola
    # el borde del opérculo (curvo, siguiendo la nuca), la línea lateral y la comisura, que sigue la boca hacia atrás
    l.trazo(F.linea([(0.172, 0.082), (0.196, 0.05), (0.208, 0.01), (0.207, -0.03), (0.196, -0.066)]), [.2, .45, .55, .45, .2],
            alfa=.5, dentro=cuerpo)
    l.trazo(F.linea([(0.225, 0.028), (0.4, 0.022), (0.6, 0.014), (0.8, 0.008), (0.86, 0.006)]), .22, alfa=.22, dentro=cuerpo,
            difuso=.05)
    pe = l.masa(pectoral(), alto=.3, brillo=.1, vientre=0, linea=.7, raices=[(*F.P(.2, -.064), 1.2, 3.2)], hondo=0)
    radios(l, pe, [(0.205, -0.062), (0.206, -0.078)], [(0.325, -0.123), (0.3, -0.125)], 5)
    l.trazo(F.linea([(0.198, -0.058), (0.262, -0.082), (0.326, -0.123)]), .38, alfa=.5, dentro=pe)      # la espina
    l.masa(pelvica(), alto=.28, brillo=.1, vientre=0, linea=.7, raices=[(*F.P(.455, -b(.455) + .008), 1.0, 2.6)], hondo=0)


CARA = dict(ojo=F.p(.082, .0), k=1.25, boca=F.p(.036, -.015), kb=2.9, giro=round(-F.grados(.03)) + 4, pb=.5, wb=.75)
CARA['marco'] = [round(CARA['ojo'][0] - 13, 1), round(CARA['ojo'][1] - 16, 1), 32, 32]
FONDO = ('<path d="M4 20q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M64 24.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
         '<path class="sombra" d="M0 74Q30 71 60 73.5T120 72V80H0Z" style="opacity:.22"/>'
         '<ellipse class="sombra" cx="30" cy="76" rx="4" ry="1.4" style="opacity:.3"/><ellipse class="sombra" cx="96" cy="76.4" rx="5" ry="1.6" style="opacity:.3"/>')
LISTO = True
