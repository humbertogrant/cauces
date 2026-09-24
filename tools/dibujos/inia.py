# -*- coding: utf-8 -*-
"""Boto, el delfín rosado del Amazonas (Inia geoffrensis), de memoria: pico largo y delgado con pelitos duros (bigotes sensibles)
a lo largo, melón abultado, ojos chicos, cuello muy flexible, sin aleta dorsal de verdad sino una joroba larga y baja como una
quilla, aletas pectorales enormes y anchas, y la cola horizontal y ancha. Nada subiendo en diagonal.
"""
import numpy as np

from _perfil import Perfil
from pintor import AGUA, ovalo

VISTA = (0, 4, 120, 70)
S = [0.000, 0.010, 0.040, 0.080, 0.120, 0.160, 0.180, 0.195, 0.210, 0.230, 0.250, 0.280, 0.320, 0.380, 0.450, 0.520, 0.600,
     0.680, 0.760, 0.840, 0.900, 0.940]
ARRIBA = [0.012, 0.014, 0.014, 0.015, 0.017, 0.021, 0.028, 0.045, 0.066, 0.084, 0.094, 0.098, 0.096, 0.100, 0.108, 0.114,
          0.112, 0.100, 0.080, 0.058, 0.044, 0.038]
ABAJO = [0.012, 0.013, 0.013, 0.014, 0.016, 0.020, 0.024, 0.030, 0.037, 0.046, 0.056, 0.068, 0.080, 0.092, 0.100, 0.104,
         0.098, 0.082, 0.060, 0.038, 0.025, 0.020]
F = Perfil(S, ARRIBA, ABAJO, 92, giros=((0, 12), (.5, 14), (1, 18)))


def quilla(s):
    """la joroba larga y baja del lomo, en lugar de aleta dorsal"""
    s = np.asarray(s, float)
    return np.where((s > .48) & (s < .8), .016 * np.sin(np.clip((s - .48) / .32, 0, 1) * np.pi) ** 1.5, 0)


def aleta():
    return F.paleta((.3, -.058), -38, .17, [.018, .020, .025, .030, .034, .034, .026], [.016, .016, .024, .034, .042, .046, .040],
                    festón=.003, abombe=.012)


def todo():
    return [F.cuerpo(joroba=quilla), F.cola_horizontal(.925, .14, .11, .08), aleta()[0]]


F.encuadrar(todo, (8, 22, 112, 70))


def dibujar(l):
    cuerpo = l.masa([F.cuerpo(joroba=quilla), F.cola_horizontal(.925, .14, .11, .08)], brillo=.3, vientre=.55,
                    bultos=[(ovalo(*F.P(.25, .06), 5.5, 5), .2)])
    for s in np.arange(.02, .16, .012):              # los pelitos del pico
        l.mancha(ovalo(*F.P(s, float(F.arriba(s)) - .004), .16, .16), '0C3A33', .45, dentro=cuerpo)
    ap, d, e = aleta()
    raiz = F.P(.3, -.058)
    l.masa(ap, alto=.4, brillo=.12, vientre=0, raices=[(raiz[0], raiz[1], 2.2, 5.4)], linea=.72)
    for f in (-.62, -.2, .22):                       # los huesos de los dedos, apenas marcados
        uu = np.linspace(.40, .95, 8)
        pts = np.array([.3, -.058]) + uu[:, None] * .17 * d + (f * .03 * (.7 + .55 * uu))[:, None] * e
        l.trazo(F.P(*pts.T), .22, alfa=.16, difuso=.08)
    l.mancha(ovalo(*F.P(.27, float(F.arriba(.27)) - .007), .9, .3, -F.grados(.27)), '0C3A33', .85)      # el espiráculo


_punta, _comisura = np.array(F.P(.004, 0)), np.array(F.P(.2, -.004))
CARA = dict(ojo=F.p(.215, .016), k=1.3, boca=[round(float(v), 1) for v in (_punta + _comisura) / 2],
            kb=round(float(np.hypot(*(_punta - _comisura))) / 2.4, 1),
            giro=round(float(np.degrees(np.arctan2(_punta[1] - _comisura[1], _punta[0] - _comisura[0])))), pb=.15, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 13, 1), round(CARA['ojo'][1] - 17, 1), 32, 32]
_bx, _by = F.P(.27, float(F.arriba(.27)))
FONDO = ('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M30 16.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1.1"%s/><circle cx="%.1f" cy="%.1f" r=".75"%s/>' % (_bx + 1, _by - 6, AGUA, _bx + 3.4, _by - 10, AGUA))
LISTO = True
