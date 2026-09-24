# -*- coding: utf-8 -*-
"""Valsa, el cisne vulgar (Cygnus olor), de memoria, nadando: todo blanco, con las alas arqueadas sobre el lomo como velas (la
postura con que el macho defiende su territorio), las plumas en capas (las chicas arriba, en escamas, y las largas del borde, que
terminan en festón), el cuello grueso y largo en forma de S y la cabeza con el pico hacia abajo; el pico anaranjado (dorado) con una
protuberancia negra en la base y la piel negra entre el ojo y el pico; la cola corta y en punta, un poco levantada.
"""
import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

from pintor import AGUA, curva, forma, ovalo, tubo

VISTA = (0, 6, 120, 82)
AGUA_Y = 79.5


def cuerpo():
    return forma([(13, 69.6), (19.4, 66.8), (28, 66.4), (40, 67.4), (55, 68), (68, 67.2), (78, 66), (84.6, 67.6), (88.6, 71.4),
                  (88.2, 76), (83, AGUA_Y), (60, AGUA_Y + .4), (35, AGUA_Y + .4), (20, AGUA_Y), (15, 75.4)], 3)


def cola():
    return forma([(16.4, 70.6), (10.6, 66.4), (7.4, 65.2), (8.6, 67.8), (11.4, 71.4), (14.6, 73.8)], 2)


BORDE_ALA = [(79.4, 66.4), (77.2, 60), (73, 53), (67, 46.6), (60, 41.6), (52, 38.6), (44, 38.4), (37, 40.6), (31, 45), (26.4, 51),
             (22.4, 58), (19, 64), (16.4, 68.8)]
ATRAS_ALA = [(16.4, 68.8), (24, 70.4), (36, 71.2), (50, 71), (64, 70), (74, 68.4), (79.4, 66.4)]


def ala():
    """las alas arqueadas; el borde de atrás, en festón: las puntas redondas de las plumas largas, que caen sobre el lomo"""
    base = forma(BORDE_ALA + ATRAS_ALA[1:-1], 3)
    borde = LineString(curva([(21, 67.6), (30, 68.8), (40, 69.2), (50, 69), (60, 68.2), (69, 66.8), (75.4, 65.2)], 12))
    puntas = [np.array(borde.interpolate(t).coords[0]) for t in np.linspace(0, borde.length, 12)]
    festones = [Point(*q).buffer(2.5, 24) for q in puntas]
    return unary_union([base] + festones), puntas


def cuello():
    return tubo([(80.4, 69), (80.2, 60), (77.8, 51.4), (77.6, 43.4), (80.2, 36.2), (84.6, 30), (87.4, 24.6), (88.4, 20)],
                [6.2, 5.2, 4.5, 4.1, 3.8, 3.6, 3.5, 3.6])


def cabeza():
    return forma([(84.6, 18), (87, 14.6), (91.4, 13.8), (95, 15.8), (96.6, 19), (95.2, 22.2), (91, 23.4), (87, 22.6)], 3)


def pico():
    return forma([(93.8, 17), (96.8, 18.6), (99.8, 21.6), (102.6, 25.6), (103.2, 27.6), (101.6, 27.8), (98.4, 25.2), (95.6, 23.2),
                  (93.6, 21.8)], 2)


def dibujar(l):
    c = l.masa([cuerpo(), cuello(), cabeza(), cola()], material='claro', brillo=.25, contraluz=.2,
               bultos=[(ovalo(90, 18.4, 4.6, 3.8), .4), (ovalo(83, 70.6, 6.4, 5.4), .35)])
    for k in range(4):                                                   # las plumas del pecho y del cuello, apenas
        l.trazo([(84 - k * .6, 57 - k * 7.4), (81.6 - k * .4, 58.8 - k * 7.4), (79.6 - k * .4, 58 - k * 7.4)], [.06, .18, .06],
                color='8EB5AA', alfa=.35, dentro=c, difuso=.1)
    ala_, puntas = ala()
    # el ala de allá asoma arriba de la de acá: las dos levantadas, como velas
    from shapely import affinity
    l.masa(affinity.translate(forma(BORDE_ALA + ATRAS_ALA[1:-1], 3), 3.6, -2.4).difference(cuello().buffer(.6)), material='claro',
           alto=.5, brillo=.1, linea=.7, contraluz=.2, hondo=0)
    a = l.masa(ala_, material='claro', alto=.55, brillo=.25, linea=.75, contraluz=.3, hondo=.12)
    # las plumas largas: una línea entre cada dos, que sube desde el festón hacia el ala
    for q0, q1 in zip(puntas[:-1], puntas[1:]):
        p = (q0 + q1) / 2 + np.array([0, 1.4])
        d = p - np.array([54, 40])
        d = d / np.linalg.norm(d)
        l.trazo([p, p - d * 4.6, p - d * 9.6], [.2, .16, .04], color='5F8F83', alfa=.42, dentro=a, difuso=.06)
        l.mancha(ovalo(*(p - d * 3), 1, 3.6, np.degrees(np.arctan2(d[1], d[0])) + 90), '8EB5AA', .16, dentro=a, difuso=.8)
    # las plumas chicas de arriba, en escamas: filas de arcos con la punta hacia atrás y abajo, que siguen el borde del ala
    t = np.array([-.45, 1.0])
    t = t / np.linalg.norm(t)
    e = np.array([-t[1], t[0]])
    for fila_, (off, n) in enumerate(((3.6, 12), (7.4, 11), (11.2, 9), (15, 7))):
        borde = LineString(curva(BORDE_ALA[1:-1], 10)).parallel_offset(off, 'right')
        if borde.is_empty:
            continue
        if borde.geom_type != 'LineString':
            borde = max(borde.geoms, key=lambda g: g.length)
        for s_ in np.linspace(.1, .9, n) + (fila_ % 2) * .4 / n:
            q = np.array(borde.interpolate(min(s_, 1) * borde.length).coords[0])
            l.trazo([q + e * 1.8 - t * .5, q + e * 1.2 + t * .6, q + t * 1, q - e * 1.2 + t * .6, q - e * 1.8 - t * .5],
                    [.05, .14, .2, .14, .05], color='5F8F83', alfa=.3, dentro=a, difuso=.06)
            l.mancha(ovalo(*(q + t * 1.9), 1.7, .7, np.degrees(np.arctan2(e[1], e[0]))), '8EB5AA', .16, dentro=a, difuso=.5)
    b = l.masa(pico(), material='acento', alto=.35, brillo=.3, vientre=0, linea=.55, hondo=0)
    l.masa(ovalo(94.6, 16.8, 1.8, 1.5, 30), material='oscuro', alto=.5, brillo=.3, vientre=0, linea=.35, hondo=0)   # la protuberancia
    l.mancha(forma([(90.8, 17.6), (94, 17.2), (95.4, 20.4), (93.6, 22.2), (91.2, 20.4)], 2), '0C3A33', .9, dentro=c)   # la piel negra
    l.mancha(ovalo(99.6, 21.6, .5, .28, 48), '0C3A33', .7, dentro=b)                                                    # la narina
    l.trazo([(94.4, 22.6), (97.6, 24.4), (100.6, 26.4), (102.8, 27.4)], [.15, .25, .2, .1], alfa=.5, dentro=b)          # la comisura


CARA = dict(ojo=[90.8, 18], k=1.1)
CARA['marco'] = [76.0, 6.0, 30, 30]
FONDO = ('<path d="M0 %.1fq4.5-2.4 9 0t9 0M104 %.1fq4.5-2.4 9 0t9 0M10 %.1fq4.5-2.2 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0"' % (AGUA_Y + 1, AGUA_Y + 1.5, AGUA_Y + 5.5)
         + AGUA + '/>')
LISTO = True
