# -*- coding: utf-8 -*-
"""Bulán, el delfín del Indo (Platanista minor), de memoria: pico largo y fino con los dientes a la vista aunque cierre la boca,
frente que sube de golpe hasta un melón redondo, ojo diminuto (casi no ve: sus ojos no tienen cristalino) justo encima de la
comisura, cuello que se dobla (una leve hondonada detrás de la cabeza), aletas pectorales grandes y anchas como paletas, y la
aleta dorsal reducida a una joroba baja a dos tercios del cuerpo. La cola, horizontal, vista un poco desde arriba para que se
lea su forma de media luna.

El cuerpo se arma con tablas de proporciones (fracciones del largo L, del pico a la muesca de la cola) a lo largo de un eje apenas
curvo, la cabeza un poco arriba y la cola también.
"""
import math
import numpy as np
from scipy.interpolate import PchipInterpolator
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pintor import AGUA, chaikin, ovalo

VISTA = (0, 4, 120, 70)
L = 95.0                                            # el largo, en unidades de la caja


def _pchip(x, y):
    return PchipInterpolator(np.asarray(x, float), np.asarray(y, float), extrapolate=True)


# y medido desde el eje del pico: arriba, lo que sube el lomo; abajo, lo que baja la panza
S_T = [0.000, 0.006, 0.020, 0.045, 0.080, 0.120, 0.160, 0.185, 0.200, 0.210, 0.220, 0.235, 0.250, 0.270, 0.290, 0.310, 0.330,
       0.360, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.760, 0.820, 0.870, 0.910, 0.940, 0.965]
ARRIBA_T = [0.0085, 0.0092, 0.0105, 0.0092, 0.0086, 0.0094, 0.0118, 0.0165, 0.0310, 0.0580, 0.0820, 0.1010, 0.1120, 0.1175,
            0.1150, 0.1085, 0.1060, 0.1085, 0.1140, 0.1180, 0.1175, 0.1135, 0.1070, 0.0985, 0.0890, 0.0770, 0.0650, 0.0560,
            0.0490, 0.0450, 0.0430]
ABAJO_T = [0.0085, 0.0092, 0.0105, 0.0092, 0.0086, 0.0092, 0.0112, 0.0135, 0.0175, 0.0210, 0.0250, 0.0320, 0.0400, 0.0500,
           0.0600, 0.0680, 0.0740, 0.0820, 0.0880, 0.0900, 0.0870, 0.0800, 0.0700, 0.0580, 0.0450, 0.0310, 0.0200, 0.0120,
           0.0080, 0.0060, 0.0050]
_ROBUSTO = np.interp(S_T, [0, .3, .36, .75, .9, 1], [1, 1, 1.08, 1.08, 1, 1])
_ARR, _ABA = _pchip(S_T, np.array(ARRIBA_T) * _ROBUSTO), _pchip(S_T, np.array(ABAJO_T) * _ROBUSTO)
FIN_S = .965


def arriba(s):
    return _ARR(np.clip(s, 0, FIN_S))


def abajo(s):
    return _ABA(np.clip(s, 0, FIN_S))


_DORSAL = _pchip([0.600, 0.630, 0.660, 0.680, 0.692, 0.702, 0.712, 0.722, 0.732], [0, .25, .62, .92, 1, .88, .55, .2, 0])


def dorsal(s):
    s = np.asarray(s, float)
    return np.where((s > .6) & (s < .732), .024 * np.clip(_DORSAL(np.clip(s, .6, .732)), 0, 1), 0.)


# el eje: la cabeza apenas arriba, la cola también; la punta del pico en (111,6; 43,6)
_sg = np.linspace(-0.1, 1.2, 4000)
_th = _pchip([0, .25, .5, .75, 1.0, 1.1], np.radians([9, 6, 1, -4, -9, -10]))(np.clip(_sg, 0, 1.1))
_ds = np.diff(_sg)
_BX = np.concatenate([[0], np.cumsum(-(np.cos(_th[1:]) + np.cos(_th[:-1])) / 2 * _ds)]) * L
_BY = np.concatenate([[0], np.cumsum(-(np.sin(_th[1:]) + np.sin(_th[:-1])) / 2 * _ds)]) * L
_BX -= np.interp(0, _sg, _BX)
_BY -= np.interp(0, _sg, _BY)
OX, OY = 111.6, 43.6


def P(s, y):
    """(s, y) del cuerpo -> punto de la caja"""
    s, y = np.asarray(s, float), np.asarray(y, float)
    X, Y, t = np.interp(s, _sg, _BX), np.interp(s, _sg, _BY), np.interp(s, _sg, _th)
    return np.stack([X - y * L * np.sin(t) + OX, -(Y + y * L * np.cos(t)) + OY], -1)


def cuerpo():
    s = np.concatenate([np.linspace(0, .3, 400), np.linspace(.3, FIN_S, 400)[1:]])
    lomo = np.stack([s, arriba(s) + dorsal(s)], -1)
    panza = np.stack([s[::-1], -abajo(s[::-1])], -1)
    r0 = float(arriba(0))
    phi = np.linspace(-np.pi / 2, np.pi / 2, 30)[1:-1]
    punta = np.stack([-r0 * np.cos(phi), r0 * np.sin(phi)], -1)
    return Polygon(P(*np.vstack([lomo, panza, punta]).T)).buffer(0)


# la cola es horizontal: su planta vista desde arriba, proyectada como la vería alguien un poco por encima del animal
COLA_INS, COLA_B, COLA_EPS, COLA_PUNTA, COLA_MUESCA = .950, .130, math.radians(50), .120, .088


def cola():
    b = np.concatenate([-np.linspace(1, 0, 60)[:-1], np.linspace(0, 1, 60)])
    f = np.abs(b)
    ataque = np.stack([COLA_PUNTA * f ** 1.4, b], -1)
    fuga = np.stack([COLA_MUESCA + (COLA_PUNTA - COLA_MUESCA) * f ** 2.5 - .012 * np.clip(1 - f / .10, 0, 1), b], -1)[::-1]
    planta = np.vstack([ataque, fuga[1:-1]])
    a, bb = planta[:, 0], planta[:, 1] * COLA_B * np.where(planta[:, 1] > 0, 1.07, .93)
    eje = float((arriba(COLA_INS) - abajo(COLA_INS)) / 2)
    return Polygon(P(COLA_INS + a, eje - bb * math.sin(COLA_EPS))).buffer(0)


ALETA_RAIZ = np.array([.335, -.036])


def aleta():
    """la aleta pectoral: grande, ancha y en paleta, con la punta festoneada por los huesos de los dedos"""
    R, ang = ALETA_RAIZ, math.radians(-36)
    d = np.array([math.cos(ang), math.sin(ang)])
    e = np.array([d[1], -d[0]])
    LF, U = .160, np.linspace(0, 1, 80)
    WL = _pchip([0, .15, .35, .55, .75, .9, 1], [.016, .018, .021, .025, .029, .031, .026])(U)
    WT = _pchip([0, .15, .35, .55, .75, .9, 1], [.014, .014, .019, .027, .036, .042, .040])(U)
    ataque = R + (U[:, None] * LF) * d + WL[:, None] * e
    fuga = R + (U[:, None] * LF) * d - WT[:, None] * e
    phi = np.linspace(0, np.pi, 60)[1:-1]
    c0, rad = R + LF * d + (WL[-1] - WT[-1]) / 2 * e, (WL[-1] + WT[-1]) / 2
    abombe = .010 * np.sin(phi) + .0032 * np.abs(np.sin(2.5 * phi)) * (phi > .8)
    punta = c0 + (np.cos(phi)[:, None] * rad) * e + abombe[:, None] * d
    return Polygon(P(*chaikin(np.vstack([ataque, punta, fuga[::-1]]), 2).T)).buffer(0), d, e, LF


def dientes():
    """largos adelante, trabados arriba y abajo, a la vista con la boca cerrada"""
    ds = []
    for j, sd in enumerate(np.arange(.020, .150, .0092)):
        largo = float(np.interp(sd, [.02, .09, .15], [.0125, .0085, .0045]))
        signo = -1 if j % 2 == 0 else 1
        ds.append(Polygon([P(sd - .0022, 0), P(sd - .0035, signo * largo), P(sd + .0022, 0)]))
    return unary_union(ds)


def _encuadrar():
    """centrado a lo ancho y, a lo alto, entre la superficie del agua (y 25,5) y el borde de abajo"""
    global OX, OY
    OX = OY = 0.0
    x0, y0, x1, y1 = unary_union([cuerpo(), cola(), aleta()[0]]).bounds
    OX, OY = (120 - (x1 - x0)) / 2 - x0, 25.5 + (44.5 - (y1 - y0)) / 2 - y0


_encuadrar()


def dibujar(l):
    raiz = P(*ALETA_RAIZ)
    l.masa([cuerpo(), cola()], bultos=[(ovalo(*P(.258, .06), 6.5, 5.5), .18)], brillo=.3, vientre=.55)
    ap, d, e, LF = aleta()
    l.masa(ap, alto=.4, brillo=.12, vientre=0, raices=[(raiz[0], raiz[1], 2.2, 5.2)], linea=.72)
    for f in (-.62, -.2, .22):                       # los huesos de los dedos, apenas marcados
        uu = np.linspace(.40, .95, 8)
        pts = ALETA_RAIZ + uu[:, None] * LF * d + (f * .03 * (.7 + .55 * uu))[:, None] * e
        l.trazo(P(*pts.T), .22, alfa=.16, difuso=.08)
    l.masa(dientes(), material='claro', alto=.15, linea=.14, vientre=0, brillo=0, arroja=False, hondo=0)
    th = math.degrees(float(np.interp(.29, _sg, _th)))           # el espiráculo: una ranura a lo largo, arriba de la cabeza
    l.mancha(ovalo(*P(.29, float(arriba(.29)) - .007), .9, .3, -th), '0C3A33', .85)


_punta, _comisura = P(.004, 0), P(.226, 0)
CARA = dict(ojo=[round(float(v), 1) for v in P(.241, .030)], k=1.0,
            boca=[round(float(v), 1) for v in (_punta + _comisura) / 2], kb=round(float(np.hypot(*(_punta - _comisura))) / 2.4, 1),
            giro=round(math.degrees(math.atan2(_punta[1] - _comisura[1], _punta[0] - _comisura[0]))), pb=.12, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 12, 1), round(CARA['ojo'][1] - 18, 1), 30, 30]
_bx, _by = P(.29, float(arriba(.29)))
FONDO = ('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M30 16.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1.1"%s/><circle cx="%.1f" cy="%.1f" r=".75"%s/>' % (_bx + 1, _by - 7, AGUA, _bx + 3.4, _by - 11.3, AGUA))
LISTO = True
