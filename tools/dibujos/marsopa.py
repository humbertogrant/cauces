# -*- coding: utf-8 -*-
"""Tun, la marsopa sin aleta del Yangtsé (Neophocaena asiaeorientalis), de memoria: cabeza redonda sin pico, boca corta que sube
un poco en la comisura (parece que sonríe), cuerpo rechoncho adelante que se afina hacia la cola, sin aleta dorsal: en su lugar,
a lo largo del lomo, una cresta baja cubierta de tubérculos; aletas pectorales medianas y puntiagudas, cola horizontal.
"""
import numpy as np

from _perfil import Perfil
from pintor import AGUA

VISTA = (0, 12, 120, 64)
S = [0.000, 0.020, 0.050, 0.100, 0.150, 0.200, 0.300, 0.400, 0.500, 0.600, 0.700, 0.800, 0.880, 0.930]
ARRIBA = [0.036, 0.058, 0.082, 0.106, 0.121, 0.130, 0.139, 0.140, 0.133, 0.117, 0.093, 0.066, 0.047, 0.040]
ABAJO = [0.030, 0.048, 0.066, 0.085, 0.098, 0.107, 0.118, 0.120, 0.112, 0.095, 0.072, 0.047, 0.029, 0.021]
F = Perfil(S, ARRIBA, ABAJO, 90, giros=((0, 16), (.45, 12), (1, 3)))


def cresta(s):
    """los tubérculos de la cresta del lomo: una ondulación finita sobre el contorno"""
    s = np.asarray(s, float)
    m = (s > .42) & (s < .8)
    return np.where(m, .0014 * np.abs(np.sin((s - .42) * np.pi / .019)) * np.sin(np.clip((s - .42) / .38, 0, 1) * np.pi), 0)


def todo():
    return [F.cuerpo(joroba=cresta, roma=.9), F.cola_horizontal(.915, .13, .10, .075), aleta()[0]]


def aleta():
    return F.paleta((.2, -.052), -35, .14, [.014, .016, .019, .021, .020, .015, .008], [.012, .012, .016, .020, .020, .015, .009])


F.encuadrar(todo, (8, 27, 112, 73))


def dibujar(l):
    cuerpo = l.masa([F.cuerpo(joroba=cresta, roma=.9), F.cola_horizontal(.915, .13, .10, .075)], brillo=.3, vientre=.6,
                    bultos=[(F.pieza([(0.0, .02), (0.06, .09), (0.14, .1), (0.16, .02), (0.1, -.06), (0.02, -.04)]), .2)])
    for s in np.arange(.43, .79, .018):              # la fila de tubérculos, apenas por debajo del borde
        y = float(F.arriba(s)) - .006
        l.mancha(F.pieza([(s - .004, y - .002), (s, y + .002), (s + .004, y - .002)], 1), '0C3A33', .25, dentro=cuerpo, difuso=.05)
    ap, d, e = aleta()
    raiz = F.P(.2, -.052)
    l.masa(ap, alto=.4, brillo=.12, vientre=0, raices=[(raiz[0], raiz[1], 2.0, 4.8)], linea=.72)
    th = F.grados(.14)
    from pintor import ovalo
    l.mancha(ovalo(*F.P(.14, float(F.arriba(.14)) - .008), .8, .28, -th), '0C3A33', .8)      # el espiráculo


CARA = dict(ojo=F.p(.106, .004), k=1.3, boca=F.p(.042, -.021), kb=2.6, giro=round(-F.grados(.04)) + 3, pb=.6, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 16, 1), round(CARA['ojo'][1] - 17, 1), 34, 34]
_bx, _by = F.P(.14, float(F.arriba(.14)))
FONDO = ('<path d="M4 18q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M40 22.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1.1"%s/><circle cx="%.1f" cy="%.1f" r=".75"%s/>' % (_bx + 1.5, _by - 6.5, AGUA, _bx + 3.7, _by - 10.5, AGUA))
LISTO = True
