# -*- coding: utf-8 -*-
"""Lobi y Nuria, la nutria neotropical (Lontra longicaudis), de memoria, caminando por la orilla con el lomo arqueado, como caminan
las nutrias en tierra: cabeza ancha y chata, orejas chicas y redondas puestas bajas a los costados, los ojos arriba y adelante (para
mirar con la cabeza casi hundida), la nariz desnuda, bigotes largos y gruesos (con ellos siente a los peces en el agua turbia); el
cuello casi tan ancho como la cabeza; la garganta y el pecho más claros; el cuerpo largo; patas cortas y fuertes, con membrana entre
los cinco dedos; la cola larga, gruesa y musculosa en la base, que se afina en punta. Pelo corto, denso y lustroso.
"""
import numpy as np

from _patas import dedos
from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 30, 120, 60)
SUELO = 81.5


def cuerpo():
    return forma([(41, 64.5), (46, 59.5), (53, 56.4), (61, 56.4), (69, 58.2), (76, 60), (82, 59.2), (87, 57), (92, 55.2), (96, 54),
                  (101, 53.8), (105.5, 55.2), (109, 57.4), (111.8, 60), (111.8, 62.4), (109.2, 64.2), (104, 65.8), (98, 67.4),
                  (92, 69.6), (86, 72.2), (78, 74.2), (68, 75), (58, 74.8), (50, 74), (45, 71.8), (42, 68.6)], 3)


def cola():
    return tubo([(43, 66.8), (33, 68.2), (23, 68.2), (14, 66.6), (6.5, 63.4)], [4.4, 3.6, 2.6, 1.6, .5])


def pata_delante(lejos=False):
    d = np.array([-5.5, -1.2]) if lejos else np.zeros(2)
    brazo = tubo([(84, 66) + d, (85.2, 72.5) + d, (86.8, 78.6) + d], [3.4, 2.6, 2.0])
    ds, _ = dedos((87.6, 80.2) + d, 8, [1.6, 1.9, 2.0, 1.8, 1.4], abanico=46, grueso=(.62, .38), curva=6)
    return [brazo] + ds


def pata_atras(lejos=False):
    d = np.array([5.5, -1.2]) if lejos else np.zeros(2)
    muslo = tubo([(51, 66) + d, (55.5, 72.2) + d], [4.6, 3.2])
    pierna = tubo([(55.5, 72.2) + d, (52.6, 78) + d], [2.9, 2.0])
    pie = tubo([(52.4, 79.6) + d, (56, 80.4) + d, (58.4, 80.6) + d], [1.8, 1.5, 1.2])
    ds, _ = dedos((58.2, 80.6) + d, 4, [1.8, 2.2, 2.4, 2.2, 1.7], abanico=34, grueso=(.62, .38), curva=4)
    return [muslo, pierna, pie] + ds


def dibujar(l):
    l.masa(pata_atras(True), material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
    l.masa(pata_delante(True), material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
    t = l.masa(cola(), brillo=.3, vientre=.4, linea=.8, hondo=0, raices=[(44, 66.5, 1, 4)], funde=False)
    l.pelaje(t, densidad=1.6, largo=1.6, ancho=.15, flujo=lambda x, y: 185 + (x - 25) * .15, alfa=.16, semilla=21)
    c = l.masa(cuerpo(), brillo=.35, vientre=.6, alto=.9,
               bultos=[(ovalo(102, 59, 7.8, 5.2), .3), (ovalo(109.2, 61, 3.4, 2.6), .35), (ovalo(55, 64, 11, 8), .15)])
    # la garganta y el pecho, claros; el pelo lustroso, que corre hacia atrás
    l.mancha(forma([(95, 66.2), (106.5, 64.4), (102, 67.6), (94, 70.4), (87.5, 73.4), (89, 70.4)], 2), 'DDF6EC', .6, dentro=c, difuso=.7)
    l.pelaje(c, densidad=1.5, largo=1.7, ancho=.15, flujo=lambda x, y: 186 + (y - 62) * .5, alfa=.16, semilla=22)
    # la oreja chica y baja, la nariz desnuda, los bigotes largos y sus raíces
    l.masa(ovalo(95.8, 55.2, 1.8, 1.5, -20), alto=.4, brillo=.1, vientre=0, linea=.5, hondo=0)
    l.mancha(ovalo(96, 55.5, .8, .65), '0C3A33', .35)
    l.mancha(forma([(110.8, 58.6), (112.5, 59.9), (112.4, 61.9), (110.8, 61.6)], 2), '0C3A33', .85)
    for dx, dy in ((-2.5, -5), (-.6, -2.2), (1.2, .4), (-1.4, 2.8), (.2, 4.4)):
        l.trazo([(108.6, 62.2), (111.2 + dx * .6, 61.8 + dy * .5), (115.2 + dx, 61.4 + dy)], [.22, .14, .05], alfa=.8)
    for dx, dy in ((-1, -3.5), (1, -.8), (-.5, 2.2), (.6, 3.6)):
        l.mancha(ovalo(108.2 + dx * .15, 62.4 + dy * .2, .2, .2), '0C3A33', .5, dentro=c)
    pc = l.masa(pata_delante(), alto=.6, brillo=.15, vientre=.2, linea=.75, hondo=0, raices=[(84, 65.5, 2, 6)])
    ph = l.masa(pata_atras(), alto=.6, brillo=.15, vientre=.2, linea=.75, hondo=0, raices=[(51, 65, 2.5, 7.5)])
    for m in (pc, ph):
        l.pelaje(m, densidad=1.5, largo=1.1, ancho=.13, flujo=100, alfa=.14, semilla=23)
    l.mancha(forma([(52.8, 80.2), (58.8, 79.4), (60.4, 80.8), (53.4, 81.2)], 2), 'A9E1CF', .3)          # la membrana del pie


CARA = dict(ojo=[102.8, 57.2], k=1.4, boca=[108.6, 63.8], kb=2.2, giro=-12, pb=.8, wb=.7)
CARA['marco'] = [86.0, 42.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="64" cy="%.1f" rx="48" ry="4.6" style="opacity:.28"/>' % (SUELO + .6)
         + '<path d="M4 87.5q4.5-2.4 9 0t9 0t9 0M3.5 85q.3-2.8-1-4.6M6 85.4q.2-3 1.4-4.6"' + AGUA + '/>')
LISTO = True
