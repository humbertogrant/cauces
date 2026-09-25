# -*- coding: utf-8 -*-
"""La barca de cola larga del Mekong, de memoria: casco estrecho y largo de madera, con la proa que sube en una punta alta y curva, y
en la popa un motor de camión montado sobre un pivote, con la hélice al final de un tubo de tres metros: el barquero lo gobierna con
una caña larga y lo levanta en los rápidos y en los bajíos (NAVES.mekong).
"""
from _barcas import agua, caja, olas_fondo, poli, tablas
from _canoas import canoa, contorno
from pintor import forma, tubo

VISTA = (0, 49, 120, 33)
AGUA_Y = 72.0


def dibujar(l):
    borda, quilla = canoa(22, 112, 66.4, 8.2, sube_popa=1.4, sube_proa=10.4, panza=1.4)
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.45, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, borda[1:-2], quilla[1:-2], n=3)
    l.mancha(forma(borda[:-1] + [(x, y + 1.8) for x, y in borda[-2::-1]], 1), '2F8A74', .75, dentro=c)      # la borda pintada
    # el pivote, el motor de camión y su radiador; la caña; el tubo largo con la hélice, que entra al agua
    tubo_ = l.masa(tubo([(26, 60.8), (14, 67.4), (2.4, 74)], [.5, .48, .45]), material='oscuro', alto=.35, brillo=.35, vientre=0,
                   hondo=0, linea=.35)
    l.masa(forma([(1, 72.8), (3.4, 71.4), (4.4, 74), (3, 77), (.6, 76.4)], 1), material='oscuro', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.3)
    l.masa(poli([(23.4, 63.4), (27, 63.4), (27, 66), (23.4, 66)], .2), material='oscuro', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.35)
    motor = l.masa(poli([(24.6, 63.4), (24.6, 56.4), (27, 54.4), (35.8, 54.4), (36.4, 57.2), (36.4, 63.4)], .4), material='oscuro',
                   alto=.4, brillo=.35, vientre=0, hondo=0, linea=.45)
    for y in (57, 58.8, 60.6):
        l.trazo([(29, y), (35.6, y)], .16, color='6FA497', alfa=.8, dentro=motor)
    l.masa(caja(27.4, 52.4, 30.2, 54.6, .2), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.35)
    l.masa(tubo([(35.6, 57.4), (46, 57.8), (50.4, 58.8)], [.4, .35, .3]), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.35)
    agua(l, AGUA_Y, sombra=poli([(20, 72), (106, 72), (100, 75.6), (24, 75.6)], .5))
    l.mancha(forma([(3, 72.4), (14, 70.6), (12, 73.4), (4, 75.2)], 1), 'F4FBF7', .5, difuso=.4)                       # la espuma de la hélice


FONDO = olas_fondo(AGUA_Y)
LISTO = True
