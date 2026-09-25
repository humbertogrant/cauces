# -*- coding: utf-8 -*-
"""El mokoro del Zambeze, de memoria: una canoa de un solo tronco, tallada en madera de mukwa, baja y angosta, que en la llanura
inundada se empuja con una pértiga larga (la ngashi) y en el río hondo se rema (NAVES.zambeze). Alrededor, los juncos y un nenúfar.
"""
from _barcas import agua, olas_fondo, palo, poli
from _canoas import canoa, contorno
from pintor import forma, ovalo, tubo

VISTA = (0, 26, 120, 52)
AGUA_Y = 72.0


def dibujar(l):
    for x, h, a in ((96, 16, 4), (100, 22, -3), (104, 18, 6), (108, 24, -2), (112, 15, 5), (6, 14, -5), (10, 19, 3)):   # los juncos
        l.masa(tubo([(x, 73), (x + a * .5, 73 - h * .6), (x + a, 73 - h)], [.4, .3, .15]), material='lejos', alto=.2, brillo=.1,
               vientre=0, hondo=0, linea=.3, arroja=False)
    borda, quilla = canoa(16, 102, 66.6, 5.8, sube_popa=1.2, sube_proa=2.4, panza=1.6)
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    l.trazo([(x, y + .9) for x, y in borda[1:-1]], [.1, .6, .6, .6, .6, .6, .1], color='93701A', alfa=.5, dentro=c, difuso=.15)
    for k in range(2):
        l.trazo([(24 + k * 4, 69.2 + k * 1.5), (60, 70.2 + k * 1.5), (96 - k * 4, 69 + k * 1.4)], [.05, .14, .05], color='93701A',
                alfa=.45, dentro=c)
    # la ngashi, la pértiga larga, que entra al agua
    palo(l, (40, 30.4), (62, 78), .5, .45)
    agua(l, AGUA_Y, sombra=poli([(18, 72), (98, 72), (94, 75), (22, 75)], .5))
    # un nenúfar, con su flor
    l.masa(ovalo(108, 73.4, 5.2, 1.4).difference(forma([(108, 73.4), (113.6, 72.6), (113.6, 74.2)], 0)), material='cuerpo', alto=.15,
           brillo=.2, vientre=0, hondo=0, linea=.35, arroja=False)
    l.masa(forma([(106.6, 72.6), (107.2, 70), (108, 71.6), (108.8, 69.8), (109.4, 72.6)], 1), material='claro', alto=.3, brillo=.2,
           vientre=0, hondo=0, linea=.3, arroja=False)


FONDO = olas_fondo(AGUA_Y)
LISTO = True
