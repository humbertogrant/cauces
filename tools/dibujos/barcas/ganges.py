# -*- coding: utf-8 -*-
"""La barca del Ganges, la que los ingleses llamaban «budgerow», de memoria: casco de madera ancho y sin quilla, con la popa alta y
curva; un techo de paja a popa, sobre la cámara de los pasajeros; un palo con una vela cuadrada, que se usa cuando sopla del sur, y
remos largos para bajar con la corriente; el remo de gobierno grande, en la popa (NAVES.ganges).
"""
from _barcas import agua, cabo, caja, casco, olas_fondo, palo, paja, remo, tablas, vela_cuadrada
from pintor import forma

VISTA = (0, 12, 120, 72)
AGUA_Y = 75.0

ARRIBA = [(14.6, 52.4), (22, 58.4), (32, 64.2), (50, 67), (70, 67.2), (86, 65.6), (97, 62.6), (104.6, 58.6)]
ABAJO = [(20.4, 66.4), (27, 73), (38, 77), (50, 78.2), (70, 78.2), (86, 76.4), (96, 72.4), (102.8, 64.6)]


def dibujar(l):
    # los remos del otro lado, detrás
    for x in (60, 70, 80):
        remo(l, (x + 1.6, 64.6), 118, 20, material='lejos')
    # el palo y la vela cuadrada, con su verga
    palo(l, (70, 67), (70.8, 16.6), .9, .6)
    vela_cuadrada(l, 70.6, 21.4, 30, 36, comba=1.4, paños=6)
    palo(l, (54.2, 21.6), (87.4, 20.8), .55, .5)
    cabo(l, [(55, 57.6), (58.6, 65.4)])
    cabo(l, [(85.8, 57.2), (95, 63.2)])
    cabo(l, [(70.8, 17), (102.6, 58.8)], alfa=.5)
    # la cámara de popa con su techo de paja
    l.masa(caja(24, 49.6, 46, 66, .3), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    paja(l, [(18.6, 52.4), (20.4, 47.4), (24.4, 43.4), (30, 41.2), (35, 40.6), (40, 41.2), (45.6, 43.4), (49.6, 47.4), (51.4, 52.4),
             (35, 50.6)], flujo=95, veces=1)
    c = l.masa(casco(ARRIBA + ABAJO[::-1]), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA, ABAJO, n=4)
    # el remo de gobierno, grande, en la popa, y los remos de este lado
    remo(l, (19, 57.2), 100, 26, pala=6.4, ancho=2.6)
    for x in (56, 66, 76):
        remo(l, (x, 66), 116, 20)
    agua(l, AGUA_Y, sombra=forma([(18, 75), (102, 75), (98, 79.6), (22, 79.6)], 1))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
