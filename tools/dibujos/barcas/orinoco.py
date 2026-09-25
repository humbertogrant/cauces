# -*- coding: utf-8 -*-
"""La curiara del Orinoco, de memoria: la canoa del Orinoco, un tronco vaciado largo y angosto, de costados gruesos, que hoy lleva
motor fuera de borda y antes se movía a canalete, el remo corto de pala en punta; es el bote de los waraos, «la gente de la curiara»
(NAVES.orinoco).
"""
from _barcas import agua, motor_fuera, olas_fondo, poli
from _canoas import canoa, contorno
from pintor import forma, tubo

VISTA = (0, 48, 120, 32)
AGUA_Y = 72.0


def dibujar(l):
    borda, quilla = canoa(12, 112, 65.4, 6.6, sube_popa=1.6, sube_proa=4.4, panza=1.5)
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    # el tronco vaciado: el borde grueso, la madera por dentro en las puntas y las vetas
    l.trazo([(x, y + .9) for x, y in borda[1:-1]], [.1, .6, .6, .6, .6, .6, .1], color='93701A', alfa=.5, dentro=c, difuso=.15)
    for k in range(3):
        l.trazo([(20 + k * 4, 67.4 + k * 1.3), (50, 68.6 + k * 1.4), (80, 68.6 + k * 1.4), (104 - k * 4, 67 + k * 1.2)],
                [.05, .14, .14, .05], color='93701A', alfa=.45, dentro=c)
    # el canalete, apoyado de través
    l.masa([tubo([(44, 57.2), (61, 66.8)], [.35, .35]), forma([(60, 65.6), (63.6, 66.4), (68.6, 70.4), (63.4, 69.8), (59.6, 67.4)], 2)],
           material='acento', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)
    motor_fuera(l, 12.6, 61.4, alto_=10)
    agua(l, AGUA_Y, sombra=poli([(14, 72), (108, 72), (102, 75.2), (18, 75.2)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
