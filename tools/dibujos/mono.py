# -*- coding: utf-8 -*-
"""Bruno, el mono congo (Alouatta palliata, el aullador de manto), de memoria, sentado en una rama comiendo hojas, con la cola
prensil enrollada en la rama como una quinta mano (dos vueltas, como una cuerda): cuerpo robusto y encorvado, de pelo negro y largo,
con un fleco largo y dorado en los costados (el manto que le da nombre: el único detalle de ese color); la cabeza chica, la cara
negra y sin pelo, de hocico corto, y debajo la mandíbula honda y la garganta abultada, con barba, donde está el hueso que hace
resonar su aullido; las manos y los pies agarran la rama; con una mano sostiene una ramita con hojas.
"""
import math

import numpy as np

from _patas import peludo
from pintor import forma, ovalo, tubo

VISTA = (16, 12, 100, 60)


def eje_rama(x):
    return 63 - .0635 * (x + 3)


def rama():
    return tubo([(-3, eje_rama(-3)), (40, eje_rama(40)), (85, eje_rama(85)), (123, eje_rama(123))], [3.0, 2.8, 2.6, 2.4])


def ramita():
    return tubo([(96, eje_rama(96) - 1), (104, 47.5), (111, 41), (116, 37.5)], [1.3, 1.0, .8, .6])


def hoja(x, y, largo, ang, ancho=.42):
    """una hoja: punta aguda, base redonda, girada `ang` grados"""
    a = math.radians(ang)
    d, e = np.array([math.cos(a), math.sin(a)]), np.array([-math.sin(a), math.cos(a)])
    p = np.array([x, y])
    pts = [p, p + d * largo * .3 + e * largo * ancho * .9, p + d * largo * .7 + e * largo * ancho * .6, p + d * largo,
           p + d * largo * .7 - e * largo * ancho * .6, p + d * largo * .3 - e * largo * ancho * .9]
    return forma(pts, 3), [p, p + d * largo * .92]


def cola():
    """La cola: sale de la base del lomo, va hacia atrás sobre la rama y se enrolla dos vueltas; devuelve los tramos de adelante
    (que se pintan después de la rama) y los de atrás (antes), y la punta."""
    base = [(44, 55.2), (40.5, 56.4), (37, 57.2)]
    x0, paso, R = 36.2, 6.4, 3.9
    xs = np.arange(x0, 21.9, -.2)
    th = 2 * math.pi * (x0 - xs) / paso
    pts = np.column_stack([xs, [eje_rama(x) - R * math.cos(t) for x, t in zip(xs, th)]])
    delante, atras = [], []
    frente = np.sin(th) >= 0
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and frente[j + 1] == frente[i]:
            j += 1
        seg = pts[max(i - 1, 0):min(j + 2, len(xs))]
        eje = seg[::3].tolist() + ([seg[-1].tolist()] if (len(seg) - 1) % 3 else [])
        radios = [1.25 - .35 * (x0 - p[0]) / (x0 - 22) for p in eje]
        (delante if frente[i] else atras).append(tubo(eje, radios, 8))
        i = j + 1
    delante.insert(0, tubo(base + [tuple(pts[0])], [1.5, 1.4, 1.3, 1.25], 10))      # sobre la rama, a la vista
    ult = pts[-1]
    punta = tubo([tuple(ult), (ult[0] - 1.8, ult[1] + 2.6), (ult[0] - 1.6, ult[1] + 5), (ult[0] + .2, ult[1] + 6)], [.9, .8, .65, .45])
    return delante, atras, punta


def torso():
    t = forma([(44, 57.6), (40.2, 54.5), (38.4, 47), (39.6, 38.5), (43.8, 30.5), (50.5, 25), (57.5, 22.6), (64, 23.2), (67.4, 27),
               (68.2, 33), (68.6, 38.5), (66.8, 45), (63.8, 51.5), (58.5, 56.4), (51, 58.2)], 3)
    return peludo(t, largo=2.2, paso=1.5, donde=lambda x, y, nx, ny: nx < -.15 and y < 55, semilla=3, flujo=100, mezcla=.72)


def cabeza():
    """la cabeza chica y la garganta abultada con su barba"""
    c = forma([(64.5, 26), (65.4, 21.6), (68.6, 18.8), (72.6, 18.6), (75.8, 20.4), (77.6, 23.4), (78.8, 26.2), (80.8, 29.2),
               (81.8, 31.2), (81.2, 33.4), (79, 35.4), (77.6, 38.6), (75.2, 41.6), (71.4, 43), (67.4, 41.8), (65.2, 36)], 3)
    return peludo(c, largo=1.6, paso=1.2, donde=lambda x, y, nx, ny: (ny > .3 and y > 37) or (ny < -.4 and x < 74), semilla=4,
                  flujo=lambda x, y: 98 if y > 30 else 150, mezcla=.66)


def cara():
    return forma([(72.6, 21.8), (76.2, 22.8), (78.3, 25.4), (77.9, 27.4), (79.6, 28.9), (81.7, 30.9), (81.5, 32.9), (79.6, 34.2),
                  (78.3, 35.6), (75.4, 36.2), (72.6, 34.2), (71.6, 29.8), (71.8, 25.4)], 3)


def manto():
    """el fleco dorado del costado, del hombro a la cadera"""
    return forma([(42.6, 41), (46, 38.4), (50.4, 42.4), (54.6, 49), (57.4, 55.6), (52.6, 57.4), (46.4, 55.2), (42.4, 49.6)], 3)


def brazo_lejos():
    return [tubo([(62, 31), (64.6, 43), (68.4, 53)], [3.4, 2.8, 2.3]),
            forma([(66.4, 52), (70.2, 52.2), (72.2, 54.4), (71.8, 57.4), (69.8, 56.2), (67.6, 57.2), (66, 55.6)], 3)]


def pierna():
    muslo = tubo([(47.5, 51.5), (54, 48.6), (59.4, 46.8)], [4.4, 3.9, 3.2])
    canilla = tubo([(59.6, 47), (60.8, 51.6), (61, 55.4)], [3.0, 2.6, 2.2])
    pie = forma([(58, 55.2), (62.6, 54.6), (65.4, 56), (65.2, 58.6), (63, 57.6), (60.4, 58.4), (58, 57.6)], 3)
    return [muslo, canilla, pie]


def brazo():
    """el brazo de este lado sostiene la ramita con hojas delante del pecho"""
    arriba_ = tubo([(58, 30.5), (58.6, 38.5), (60.4, 45.6)], [3.8, 3.3, 2.9])
    antebrazo = tubo([(60.4, 45.6), (66, 45.4), (72, 43.6)], [2.8, 2.5, 2.1])
    mano = forma([(71, 41.4), (74.4, 41), (76.6, 42.6), (76.4, 45.6), (73.6, 46.8), (71, 46)], 3)
    return [arriba_, antebrazo, mano]


def ramillete():
    """la ramita que sostiene, con tres hojas tiernas"""
    tallo = tubo([(72.5, 45.6), (80, 43.4), (86, 42.6)], [.45, .4, .32])
    hojas = [hoja(85.6, 42.6, 7.2, -28), hoja(85.2, 42.8, 6.4, 18), hoja(81, 43.2, 5.2, -70)]
    return tallo, hojas


def dibujar(l):
    delante, atras, punta = cola()
    for h, nervio in (hoja(104.5, 47.2, 8, -80), hoja(110.8, 41.2, 7.4, -20), hoja(107, 44.2, 6.8, 40), hoja(115.4, 37.8, 6, 10)):
        m = l.masa(h, material='lejos', alto=.25, brillo=.2, vientre=0, linea=.55, hondo=0, contraluz=.2)
        l.trazo(nervio, [.18, .06], alfa=.4, dentro=m)
    l.masa(ramita(), material='lejos', alto=.5, brillo=.1, vientre=0, linea=.6, hondo=0)
    l.masa(brazo_lejos(), material='lejos', alto=.6, brillo=.04, vientre=0, linea=.75, hondo=0)
    ca = l.masa(atras, alto=.55, brillo=.08, vientre=0, linea=.7, hondo=0, raices=[(44, 55.2, 1.5, 4)])
    l.pelaje(ca, densidad=2, largo=1.2, ancho=.18, alfa=.3, semilla=31, claro=.35, flujo=180, mechon=2, separa=.25)
    r = l.masa(rama(), material='lejos', alto=.6, brillo=.1, vientre=0, linea=.8, hondo=0)
    for x in (4, 16, 50, 88, 101):                             # la corteza
        l.trazo([(x, eje_rama(x) - .6), (x + 5, eje_rama(x + 5) - .9)], .2, alfa=.3, dentro=r)
        l.trazo([(x + 2, eje_rama(x) + 1.2), (x + 6, eje_rama(x + 6) + 1)], .16, alfa=.22, dentro=r)
    cd = l.masa(delante + [punta], alto=.55, brillo=.08, vientre=0, linea=.7, hondo=0)
    l.pelaje(cd, densidad=2, largo=1.2, ancho=.18, alfa=.3, semilla=32, claro=.35, flujo=110, mechon=2, separa=.25)
    pu = punta.intersection(ovalo(punta.centroid.x + 1, punta.centroid.y + 1.5, 1.8, 2.6))
    l.mancha(pu, 'A6BDB6', .45, dentro=cd, difuso=.25)                                     # la punta pelada, que agarra
    c = l.masa([torso(), cabeza()], brillo=.06, vientre=.2, contraluz=.35, linea=.8,
               bultos=[(ovalo(52, 36, 11, 10), .3), (ovalo(71, 38.6, 4.6, 3.6), .35), (ovalo(68.6, 24.6, 5, 4.4), .35)])
    l.pelaje(c, densidad=1.3, largo=2.6, ancho=.24, alfa=.42, semilla=11, curva=6, desvio=6, claro=.35, mechon=3,
             flujo=lambda x, y: 150 if y < 27 and x > 60 else (95 if x > 62 else 100 + (46 - x) * 1.5))
    mt = manto()
    l.mancha(mt, 'E8B952', .3, dentro=c, difuso=1.4)                                       # el manto: un fleco largo y dorado
    l.pelaje(c, densidad=2.2, largo=4.2, ancho=.26, alfa=.55, semilla=12, curva=5, desvio=5, claro=.55, mechon=2,
             zona=mt.buffer(.8), oscuro='93701A', clarito='F2D48A', flujo=lambda x, y: 96 - (x - 48) * 1.2)
    # la cara negra, con la barba de la garganta que baja desde la mandíbula
    f = l.masa(cara(), material='oscuro', alto=.5, brillo=.3, vientre=0, linea=.8, hondo=.2, contraluz=.25, arroja=False,
               sin_tinta=cabeza().buffer(-.55), bultos=[(ovalo(79.2, 31.4, 3.2, 3), .15), (ovalo(75.8, 25, 3, 1.4, -15), .1)])
    l.pelaje(c, densidad=4, largo=2.2, ancho=.22, alfa=.55, semilla=13, curva=5, desvio=6, claro=.3, mechon=2,
             zona=ovalo(74, 39, 5, 3.2, -20), flujo=105)                                   # la barba
    l.mancha(ovalo(81, 30.6, .5, .34, 30), '05201C', .8, dentro=f)                          # la narina
    l.mancha(forma([(79, 33.4), (81.2, 32.8), (80.8, 34.2), (79.2, 35)], 2), 'A6BDB6', .4, dentro=f, difuso=.25)
    pr = l.masa(pierna(), alto=.6, brillo=.06, vientre=.2, linea=.8, hondo=0, raices=[(47.5, 51.5, 3, 8)])
    l.pelaje(pr, densidad=1.3, largo=2, ancho=.22, alfa=.36, semilla=14, claro=.35, mechon=2, curva=6, desvio=6,
             flujo=lambda x, y: 195 if y < 50 else 95)
    for p in (((61.2, 56.4), (63.4, 56.8), (64.4, 58.2)), ((59.6, 56.8), (61.4, 57.6), (61.8, 58.6))):
        l.trazo(list(p), .2, alfa=.4, dentro=pr)                                           # los dedos del pie, que agarran
    tallo, hojas_ = ramillete()
    l.masa(tallo, material='lejos', alto=.4, brillo=.1, vientre=0, linea=.45, hondo=0)
    for h, nervio in hojas_:
        m = l.masa(h, alto=.25, brillo=.25, vientre=0, linea=.55, hondo=0, contraluz=.25)
        l.trazo(nervio, [.18, .06], alfa=.4, dentro=m)
    b = l.masa([peludo(u, largo=1.4, paso=1.2, donde=lambda x, y, nx, ny: ny > .3 or nx < -.4, semilla=15,
                       flujo=lambda x, y: 95 if x < 60 else 175) if i < 2 else u for i, u in enumerate(brazo())],
               alto=.6, brillo=.06, vientre=.2, linea=.8, hondo=0, raices=[(58, 30.5, 2.5, 7)])
    l.pelaje(b, densidad=1.3, largo=2, ancho=.22, alfa=.36, semilla=16, claro=.35, mechon=2, curva=6, desvio=6,
             flujo=lambda x, y: 95 if x < 60 else 180)
    for p in (((73.6, 42.2), (75.6, 43), (75.8, 44.8)), ((72.6, 43.6), (74.6, 44.8), (74.4, 46.2))):
        l.trazo(list(p), .2, alfa=.45, dentro=b)                                            # los dedos que sostienen la ramita


CARA = dict(ojo=[75.7, 27.2], k=1.15, boca=[79.9, 33.6], kb=1.3, giro=18, pb=.7, wb=.6)
CARA['marco'] = [58.0, 14.0, 30, 30]
FONDO = ''
LISTO = True
