# -*- coding: utf-8 -*-
"""La lodia del Volga, de memoria: casco de tablones solapados (las tracas montan una sobre otra, como en los barcos de los varegos),
con la roda y el codaste que suben en curva; un palo con una vela cuadrada de paños a franjas y remos por la borda; y la sirga: en los
tramos sin viento, los burlaki la arrastraban río arriba desde la orilla, tirando de una cuerda atada al palo, como en el cuadro de
Repin (NAVES.volga).
"""
import numpy as np

from _barcas import agua, cabo, casco, olas_fondo, palo, remo, vela_cuadrada
from pintor import forma, ovalo

VISTA = (0, 10, 120, 74)
AGUA_Y = 75.0

ARRIBA = [(16, 55.4), (26, 63.6), (40, 66.6), (60, 67.4), (80, 66.6), (94, 63.4), (104, 55.2)]
ABAJO = [(19.4, 64), (28, 72.4), (42, 76.8), (60, 77.6), (80, 76.8), (93, 72.2), (101.4, 63.6)]


def dibujar(l):
    for x in (46, 56, 76, 86):                                      # los remos del otro lado
        remo(l, (x + 1.4, 64.6), 116, 17, material='lejos')
    palo(l, (60, 67.2), (60.6, 14.4), .9, .6)
    v = vela_cuadrada(l, 60.4, 19.4, 34, 34, comba=1.6, paños=7)
    for k in (1, 3, 5):                                             # los paños a franjas
        x0 = 60.4 - 17 + 34 * k / 7
        l.mancha(forma([(x0, 19.6), (x0 + 34 / 7, 19.6), (x0 + 34 / 7 + .2, 53.6), (x0 + .1, 53.6)], 0), '6CC8A8', .45, dentro=v)
    palo(l, (41.6, 19.4), (79.2, 19.4), .55, .5)
    cabo(l, [(44, 53.2), (40.4, 66)])
    cabo(l, [(77, 53.4), (82, 66)])
    # la sirga, que va del palo a los burlaki, adelante en la orilla
    cabo(l, [(60.4, 24), (90, 40), (120, 50.4)], ancho=.18, alfa=.8)
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    # las tracas solapadas: cada una con su borde de abajo marcado y su sombrita
    for f in np.linspace(.12, .86, 5):
        pts = [tuple(np.array(a) + (np.array(b) - np.array(a)) * f) for a, b in zip(ARRIBA, ABAJO)]
        l.trazo(pts, [.08, .3, .3, .3, .3, .3, .08], alfa=.4, dentro=c)
        l.trazo([(x, y + .5) for x, y in pts], [.06, .5, .5, .5, .5, .5, .06], color='93701A', alfa=.35, dentro=c, difuso=.2)
    for x, y in ((26, 64.6), (100, 58.4)):                           # los clavos de la roda y del codaste
        l.mancha(ovalo(x, y, .3, .3), '0C3A33', .7, dentro=c)
    for x in (42, 52, 72, 82):                                      # los remos de este lado
        remo(l, (x, 66.4), 114, 17)
    agua(l, AGUA_Y, sombra=forma([(18, 75), (102, 75), (98, 79.6), (22, 79.6)], 1))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
