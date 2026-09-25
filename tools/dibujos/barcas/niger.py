# -*- coding: utf-8 -*-
"""La pinaza del Níger, de memoria: una canoa larga de tablas cosidas y calafateadas, de hasta 30 metros, con las puntas que suben
y se afinan; techos de esteras en arco sobre la carga y la gente, y un motor fuera de borda que a veces funciona. Es el camión del
Níger: en la crecida lleva de todo (NAVES.niger).
"""
import numpy as np

from _barcas import agua, esteras, fardo, motor_fuera, olas_fondo, poli, tablas
from _canoas import canoa, contorno
from pintor import forma, ovalo

VISTA = (0, 47, 120, 35)
AGUA_Y = 72.0


def boveda(l, x0, x1, y_base, alto_):
    """un techo de esteras en arco, sobre aros, con su tejido y los aros marcados"""
    pts = [(x0, y_base)] + [(x0 + (x1 - x0) * u, y_base - alto_ * np.sin(np.pi * u) ** .6) for u in np.linspace(.05, .95, 10)] + [(x1, y_base)]
    t = l.masa(poli(pts, .3), material='vientre', alto=.4, brillo=.06, vientre=0, hondo=0, linea=.5)
    esteras(l, t, paso=1.1, alfa=.32)
    for u in np.linspace(.15, .85, 4):
        x = x0 + (x1 - x0) * u
        l.trazo([(x, y_base - alto_ * np.sin(np.pi * u) ** .6 + .3), (x, y_base)], [.22, .3, .22], color='164F46', alfa=.5, dentro=t)
    return t


def dibujar(l):
    borda, quilla = canoa(8, 114, 64.6, 7.6, sube_popa=7.4, sube_proa=9.6, panza=1.3)
    boveda(l, 24, 56, 63, 11.4)
    boveda(l, 58, 88, 63, 12.4)
    for x, y, w, h, m in ((30, 51.6, 6, 4.4, 'claro'), (37, 52.4, 5, 3.6, 'lejos'), (64, 51.4, 7, 4.6, 'claro'), (72, 50.8, 5.6, 5.2, 'vientre')):
        fardo(l, x, y + 1.4, w, h, material=m)                     # los bultos, arriba de los techos
    fardo(l, 90, 58.6, 7, 5.8, material='claro')
    fardo(l, 97, 59.6, 5.4, 4.8, material='lejos')
    fardo(l, 15, 59.6, 7, 5, material='claro')
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.45, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, borda[1:-1], quilla[1:-1], n=3)
    for x in np.arange(18, 106, 3.2):                               # las costuras de las tablas, cosidas
        l.trazo([(x, 66.6), (x + .6, 67.4)], .14, alfa=.45, dentro=c)
    for x, y in ((9.4, 57.8), (112.6, 55.6)):                       # las puntas, pintadas
        l.mancha(ovalo(x, y + 1.6, 2, 1.4), '2F8A74', .8, dentro=c)
    motor_fuera(l, 8.6, 61.6, alto_=10)
    agua(l, AGUA_Y, sombra=poli([(12, 72), (108, 72), (102, 75.6), (16, 75.6)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
