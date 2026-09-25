# -*- coding: utf-8 -*-
"""El vapor de rueda del Misisipi, de memoria: casco largo y tan plano que casi no se ve bajo la cubierta; la cubierta principal,
abierta y cargada de fardos de algodón; encima, la cubierta de los pasajeros, blanca, con su galería de arcos y barandas; más arriba,
la cabina del piloto, con ventanas a los cuatro lados; adelante, dos chimeneas altas con la corona recortada y el humo que se va
hacia atrás; la gran rueda de paletas en la popa. El piloto «se sabe de memoria cada banco de arena», como Mark Twain (NAVES).
"""
import numpy as np

from _barcas import agua, caja, chimenea, humo, olas_fondo, palo, poli, rueda

VISTA = (0, 6, 120, 78)
AGUA_Y = 74.0


def dibujar(l):
    # la rueda de popa, detrás de todo, con las vigas que la sostienen
    for y in (62.2, 66.4):
        palo(l, (10.6, y), (24, y + 1.4), .45, .45)
    rueda(l, 15.4, 67, 8.8)
    # el casco, bajo y chato
    c = l.masa(poli([(18.6, 69.2), (101, 69.2), (109.6, 67.4), (106.8, 72.4), (98.6, 75.2), (21.4, 75.2), (19, 73.2)], .4),
               material='acento', alto=.35, brillo=.25, vientre=0, hondo=0, contraluz=.2)
    for y in (71.4, 73.4):
        l.trazo([(21, y), (101, y), (106.4, y - 1.4)], .14, alfa=.3, dentro=c)
    # los fardos de algodón en la cubierta principal, con sus flejes
    for k, x in enumerate(np.arange(29, 92, 5.2)):
        f = l.masa(caja(x, 64.4 - (k % 2) * .4, x + 4.8, 69), material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.4,
                   arroja=False)
        for dx in (1.4, 3.4):
            l.trazo([(x + dx, 64.6), (x + dx, 68.8)], .14, alfa=.35, dentro=f)
    # la cubierta de los pasajeros: el piso, los postes, la cabina con su galería de arcos y la baranda, y el techo
    l.masa(caja(19.6, 58.4, 106, 60.2, .2), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.45)
    for x in np.arange(24, 104, 4):
        l.masa(caja(x - .35, 60.2, x + .35, 64.4, .1), material='claro', alto=.15, brillo=0, vientre=0, hondo=0, linea=.3, arroja=False)
    cabina = l.masa(caja(24, 50.4, 98, 58.4, .2), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    for x in np.arange(26.6, 96.4, 3.6):
        l.mancha(poli([(x, 58), (x, 53.2), (x + .5, 52), (x + 1.1, 51.6), (x + 1.7, 52), (x + 2.2, 53.2), (x + 2.2, 58)], .1), '2F8A74',
                 .5, dentro=cabina)
    l.trazo([(24, 55.6), (98, 55.6)], .2, alfa=.55, dentro=cabina)
    for x in np.arange(26, 98, 1.2):
        l.trazo([(x, 55.6), (x, 58.2)], .08, alfa=.35, dentro=cabina)
    l.masa(caja(20.6, 48.8, 102, 50.4, .2), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.45)
    # la cubierta de arriba y la cabina del piloto
    l.masa(caja(50, 44.2, 82, 48.8, .2), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    piloto = l.masa(caja(60, 36.8, 71.4, 44.2, .2), material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.5)
    for x in (61.4, 64.8, 68.2):
        l.mancha(caja(x, 38.4, x + 2.2, 41.8, .15), '2F8A74', .7, dentro=piloto)
    l.masa(poli([(58, 36.8), (73.4, 36.8), (71.2, 34.4), (60.2, 34.4)], .2), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0,
           linea=.45)
    # las dos chimeneas, altas, con su corona, y el humo que se va hacia atrás
    for x in (86, 92.6):
        chimenea(l, x, 50, 18.4, r=1.5)
    humo(l, 85.4, 14.6, n=5, deriva=(-5.2, -1.3), r=2.4)
    palo(l, (106.4, 67.6), (106.8, 58.2), .3, .25)                            # el asta de proa
    agua(l, AGUA_Y, sombra=poli([(10, 74), (108, 74), (104, 77.6), (14, 77.6)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
