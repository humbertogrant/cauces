# -*- coding: utf-8 -*-
"""Bela, la beluga (Delphinapterus leucas), de memoria: toda blanca, cabeza chica con un melón muy redondo sobre un pico corto,
cuello que se dobla (se le marca detrás de la cabeza), sin aleta dorsal (una cresta baja en el lomo), aletas pectorales anchas
en paleta y la cola horizontal. Nada arqueada, la cola abajo a la izquierda.
"""
import numpy as np

from _perfil import Perfil
from pintor import AGUA, ovalo

VISTA = (0, 6, 120, 78)
S = [0.000, 0.020, 0.040, 0.060, 0.080, 0.100, 0.120, 0.150, 0.180, 0.210, 0.240, 0.280, 0.330, 0.400, 0.500, 0.600, 0.700,
     0.800, 0.880, 0.930]
ARRIBA = [0.020, 0.026, 0.036, 0.058, 0.084, 0.104, 0.118, 0.126, 0.126, 0.118, 0.110, 0.110, 0.118, 0.128, 0.130, 0.120, 0.098,
          0.070, 0.048, 0.040]
ABAJO = [0.018, 0.026, 0.034, 0.042, 0.050, 0.058, 0.066, 0.078, 0.088, 0.096, 0.104, 0.114, 0.124, 0.132, 0.130, 0.114, 0.088,
         0.058, 0.034, 0.024]
F = Perfil(S, ARRIBA, ABAJO, 86, giros=((0, -12), (.35, 4), (.7, 16), (1, 30)))


def cresta(s):
    s = np.asarray(s, float)
    return np.where((s > .42) & (s < .78), .006 * np.sin(np.clip((s - .42) / .36, 0, 1) * np.pi), 0)


def aleta():
    return F.paleta((.245, -.07), -42, .13, [.018, .020, .024, .028, .030, .030, .024], [.016, .016, .022, .028, .032, .032, .026],
                    abombe=.014)


def todo():
    return [F.cuerpo(joroba=cresta, roma=.8), F.cola_horizontal(.915, .14, .10, .085), aleta()[0]]


F.encuadrar(todo, (8, 24, 112, 80))


def dibujar(l):
    cuerpo = l.masa([F.cuerpo(joroba=cresta, roma=.8), F.cola_horizontal(.915, .14, .10, .085)], material='claro', brillo=.25,
                    bultos=[(F.pieza([(0.05, .03), (0.09, .11), (0.16, .12), (0.21, .08), (0.2, .0), (0.12, -.03), (0.06, -.02)]), .45)])
    # el pliegue del cuello, suave
    l.trazo(F.linea([(0.262, 0.1), (0.258, 0.05), (0.268, 0.0)]), [.5, .35, .1], color='5F8F83', alfa=.35, dentro=cuerpo, difuso=.35)
    ap, d, e = aleta()
    raiz = F.P(.245, -.07)
    l.masa(ap, material='claro', alto=.4, brillo=.1, raices=[(raiz[0], raiz[1], 2.2, 5.2)], linea=.72)
    l.mancha(ovalo(*F.P(.2, float(F.arriba(.2)) - .008), .9, .3, -F.grados(.2)), '0C3A33', .8)      # el espiráculo


CARA = dict(ojo=F.p(.105, .02), k=1.3, boca=F.p(.036, -.011), kb=2.3, giro=round(-F.grados(.04)) + 4, pb=.6, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 15, 1), round(CARA['ojo'][1] - 18, 1), 36, 36]
_bx, _by = F.P(.2, float(F.arriba(.2)))
FONDO = ('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M14 16.5q4.5-2.2 9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1.1"%s/><circle cx="%.1f" cy="%.1f" r=".75"%s/>' % (_bx + 1.5, _by - 6, AGUA, _bx + 3.8, _by - 10, AGUA))
LISTO = True
