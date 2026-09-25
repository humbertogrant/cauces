# -*- coding: utf-8 -*-
"""La balsa de pieles de oveja del río Amarillo (yangpi fazi), de memoria: trece pieles de oveja enteras, infladas, amarradas bajo un
enrejado de palos de madera; se ven en fila, redondas y claras, con los muñones de las patas atados, y el enrejado encima; un remo
largo para gobernarla. Bajaba desde Lanzhou con mercancía y pasajeros; al final del viaje se vendía la madera y las pieles volvían
por tierra (NAVES.huanghe).
"""
import numpy as np

from _barcas import agua, fardo, olas_fondo, palo, poli
from pintor import ovalo, tubo

VISTA = (4, 47, 112, 33)
AGUA_Y = 70.0


def piel(l, x, y, r=4.2, material='claro'):
    """una piel de oveja inflada: el cuerpo redondo y alargado, el cuello atado y los cuatro muñones de las patas"""
    cuerpo = ovalo(x, y, r * 1.2, r * .85)
    cuello = tubo([(x + r * 1.1, y - r * .1), (x + r * 1.55, y - r * .3)], [.9, .6], 5)
    patas = [tubo([(x + dx, y + r * .6), (x + dx * 1.1, y + r * 1.05)], [.7, .5], 5) for dx in (-r * .75, -r * .3, r * .3, r * .75)]
    p = l.masa([cuerpo, cuello] + patas, material=material, alto=.75, brillo=.25, vientre=0, hondo=0, linea=.45, contraluz=.2)
    l.pelaje(p, densidad=2.4, largo=.9, ancho=.16, alfa=.28, semilla=int(x), claro=.3, curva=20, desvio=40, flujo=0)
    return p


def dibujar(l):
    for x in np.arange(24, 96, 11):                                 # la fila de atrás, más oscura
        piel(l, x + 5.5, 64.4, 3.8, material='lejos')
    for x in np.arange(20, 100, 11.4):
        piel(l, x, 66.6, 4.2)
    # el enrejado de palos, encima: los largueros y los travesaños que se cruzan
    marco = [tubo([(14, 59.4), (104, 59.4)], [.7, .7]), tubo([(14, 62.4), (104, 62.4)], [.6, .6])]
    for x in np.arange(16, 104, 6.2):
        marco.append(tubo([(x, 58.2), (x + 2.2, 63.6)], [.45, .45], 4))
    l.masa(marco, material='acento', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4, arroja=False)
    for x in np.arange(16, 104, 6.2):                               # las ataduras
        l.mancha(ovalo(x + .2, 59.4, .6, .7), '0C3A33', .7)
    fardo(l, 42, 53.6, 8, 5.4, material='vientre')
    fardo(l, 51, 54.2, 7, 4.8, material='claro')
    fardo(l, 72, 53.8, 7.6, 5.2, material='lejos')
    # el remo largo de gobierno, en la popa
    palo(l, (18, 58.6), (18, 52.6), .4, .35)
    palo(l, (24, 51), (6.4, 68), .5, .45)
    l.masa(poli([(8.4, 66.2), (5.4, 65.8), (4.6, 70.4), (8, 70.6)], .3), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.4)
    agua(l, AGUA_Y, x0=6, x1=114, sombra=poli([(14, 70), (104, 70), (100, 73), (18, 73)], .5))


FONDO = olas_fondo(AGUA_Y, x0=6, x1=114)
LISTO = True
