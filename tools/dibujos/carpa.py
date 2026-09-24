# -*- coding: utf-8 -*-
"""Li, la carpa común (Cyprinus carpio), de memoria: cuerpo alto con el lomo arqueado, escamas grandes y marcadas, aleta dorsal
larga (de la mitad del lomo casi hasta la cola) con una espina aserrada adelante, dos pares de barbillas en la boca (las de la
comisura, más largas), boca que se estira hacia abajo para buscar en el fondo, y la cola ahorquillada. La aleta dorsal, dorada:
el único detalle de ese color, como en la ilustración de antes.
"""
import numpy as np
from shapely.geometry import Polygon

from _perfil import Perfil
from pintor import AGUA, tubo

VISTA = (0, 8, 120, 76)
S = [0.000, 0.020, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 0.800]
ARRIBA = [0.032, 0.050, 0.075, 0.108, 0.135, 0.157, 0.172, 0.180, 0.182, 0.178, 0.168, 0.152, 0.132, 0.110, 0.088, 0.070, 0.058, 0.054]
ABAJO = [0.028, 0.042, 0.060, 0.084, 0.104, 0.120, 0.132, 0.140, 0.144, 0.143, 0.136, 0.124, 0.108, 0.090, 0.073, 0.060, 0.052, 0.050]
F = Perfil(S, ARRIBA, ABAJO, 96, giros=((0, -4), (.5, -2), (1, 2)))


def a(s):
    return float(F.arriba(s))


def b(s):
    return float(F.abajo(s))


def dorsal():
    s = np.linspace(.35, .66, 14)
    alto = np.interp(s, [.35, .37, .42, .5, .6, .66], [.0, .1, .085, .06, .045, .03])
    return F.pieza([(0.345, a(.345) - .01)] + list(zip(s, [a(v) + h for v, h in zip(s, alto)])) + [(0.67, a(.67) - .012)], 1)


def cola():
    return F.pieza([(0.79, 0.05), (0.85, 0.08), (0.92, 0.118), (0.975, 0.148), (0.995, 0.155), (0.99, 0.13), (0.965, 0.085),
                    (0.935, 0.035), (0.915, 0.004), (0.935, -0.03), (0.962, -0.08), (0.985, -0.125), (0.99, -0.15), (0.972, -0.145),
                    (0.92, -0.112), (0.85, -0.075), (0.79, -0.047)], 1)


def anal():
    return F.pieza([(0.615, -b(.615) + .01), (0.63, -b(.63) - .045), (0.64, -b(.64) - .07), (0.652, -b(.652) - .066),
                    (0.666, -b(.666) - .032), (0.68, -b(.68) + .006)], 1)


def pelvica():
    return F.pieza([(0.43, -b(.43) + .012), (0.46, -b(.46) - .03), (0.485, -b(.485) - .05), (0.49, -b(.49) - .036),
                    (0.475, -b(.475) + .004)], 1)


def pectoral():
    return F.pieza([(0.215, -0.095), (0.26, -0.118), (0.3, -0.142), (0.31, -0.155), (0.29, -0.155), (0.255, -0.138),
                    (0.228, -0.116)], 2)


def barbillas():
    """dos pares: el de la comisura, más largo; el del labio de arriba, cortito"""
    return [tubo(F.linea([(0.042, -0.026), (0.05, -0.05), (0.046, -0.07)]), [.55, .45, .32]),
            tubo(F.linea([(0.012, -0.012), (0.012, -0.03), (0.006, -0.04)]), [.45, .38, .3])]


def todo():
    return [F.cuerpo(), dorsal(), cola(), anal(), pelvica(), pectoral()] + barbillas()


F.encuadrar(todo, (8, 22, 112, 80))


def escamas(l, cuerpo):
    """escamas grandes: arcos abiertos hacia la cabeza, en filas corridas, más marcadas a media altura"""
    for i, s in enumerate(np.arange(.24, .8, .034)):
        y0 = -b(s) + .03
        y1 = a(s) - .03
        for y in np.arange(y0 + (.016 if i % 2 else 0), y1, .032):
            p = [(s - .006, y + .014), (s + .008, y + .006), (s + .011, y - .002), (s + .006, y - .012), (s - .006, y - .016)]
            l.trazo(F.linea(p), [.12, .24, .26, .2, .1], alfa=.28, dentro=cuerpo)


def dibujar(l):
    fin = dict(alto=.3, brillo=.12, vientre=0, linea=.7, hondo=0)
    l.masa(dorsal(), material='acento', alto=.3, brillo=.12, vientre=0, linea=.7, hondo=0)
    l.trazo(F.linea([(0.352, a(.352)), (0.358, a(.358) + .05), (0.368, a(.368) + .1)]), .45, alfa=.55)     # la espina aserrada
    l.masa(anal(), **fin)
    l.masa(cola(), **fin)
    corte = Polygon(F.linea([(0.8, 0.25), (0.84, 0.25), (0.84, -0.25), (0.8, -0.25)]))
    cuerpo = l.masa(F.cuerpo(), brillo=.3, vientre=.7, sin_tinta=corte,
                    bultos=[(F.pieza([(0.01, .02), (0.08, .09), (0.18, .11), (0.2, -.06), (0.1, -.07), (0.02, -.02)]), .25)])
    escamas(l, cuerpo)
    l.trazo(F.linea([(0.176, 0.12), (0.2, 0.07), (0.212, 0.01), (0.205, -0.05), (0.19, -0.09)]), [.2, .5, .6, .5, .2],
            alfa=.55, dentro=cuerpo)                 # el borde del opérculo
    l.trazo(F.linea([(0.22, 0.03), (0.4, 0.024), (0.6, 0.014), (0.8, 0.006)]), .22, alfa=.25, dentro=cuerpo, difuso=.05)
    for bb in barbillas():
        l.masa(bb, alto=.3, brillo=0, vientre=0, linea=.45, hondo=0)
    l.masa(pelvica(), **dict(fin, raices=[(*F.P(.45, -b(.45)), .9, 2.4)]))
    l.masa(pectoral(), alto=.3, brillo=.1, vientre=0, linea=.7, raices=[(*F.P(.22, -.1), 1.0, 2.8)], hondo=0)


CARA = dict(ojo=F.p(.088, .036), k=1.5, boca=F.p(.018, -.012), kb=1.5, giro=round(-F.grados(.02)) + 28, pb=.7, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 16, 1), round(CARA['ojo'][1] - 15, 1), 32, 32]
_mx, _my = F.P(-.01, 0)
FONDO = ('<path d="M4 14q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M58 18.5q4.5-2.2 9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1.1"%s/><circle cx="%.1f" cy="%.1f" r=".75"%s/>' % (_mx + 2.5, _my - 5, AGUA, _mx + 4.3, _my - 9.5, AGUA))
LISTO = True
