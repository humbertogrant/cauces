# -*- coding: utf-8 -*-
"""Lola, la bonobo (Pan paniscus), de memoria, sentada en el suelo con las rodillas arriba y un brazo apoyado en la rodilla:
más esbelta que un chimpancé, de brazos y piernas largos, con el pelo negro y largo; en la cabeza, redonda, el pelo se abre con una
raya al medio y cae hacia los lados y hacia atrás, con mechones sobre las mejillas; la cara negra y sin pelo hasta la frente (en los
bonobos es negra también de jóvenes), la frente más alta y el arco de las cejas más suave que en el chimpancé, el hocico corto y los
labios claros; las orejas chicas y negras, casi tapadas por el pelo; las manos de dedos largos y los pies como manos, con el dedo
gordo separado.
"""
import numpy as np

from _patas import peludo
from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 0, 120, 90)
SUELO = 82.0


def abajo_atras(x, y):
    """cómo cae el pelo: hacia abajo en el lomo, un poco hacia atrás en la nuca y en la cabeza"""
    return 105 if y > 34 else 125


def torso():
    t = forma([(31, 80.5), (27.8, 72), (27.8, 60), (30, 49), (34, 40.5), (38.5, 34.5), (42.5, 29.5), (49, 28.5), (55, 31),
               (57.5, 36), (58.2, 41), (58.4, 48), (58.4, 56), (56.5, 65), (52, 73), (44, 79.5), (37, 81.5)], 3)
    # el pelo largo del lomo y de los hombros cae hacia abajo: dientes de sierra en el contorno
    return peludo(t, largo=2.1, paso=1.5, donde=lambda x, y, nx, ny: nx < -.2 and y < 75, semilla=1, flujo=abajo_atras, mezcla=.7)


def craneo():
    """la cabeza con su pelo: redonda, el pelo que baja de la raya y cae hacia atrás; los mechones de la mejilla bajo la oreja"""
    c = forma([(44.5, 33), (42.2, 27.5), (42.2, 21), (44.6, 16), (48.6, 13), (53, 12.2), (57, 13.4), (59.6, 16), (59.4, 20),
               (57.8, 24.5), (57.4, 29.5), (57.8, 33.8), (55.6, 36.4), (51.4, 36.8), (47.6, 35.4)], 3)
    return peludo(c, largo=1.7, paso=1.25, donde=lambda x, y, nx, ny: (nx < .1 and y < 36) or (ny < -.3 and x < 56), semilla=2,
                  flujo=abajo_atras, mezcla=.62)


def cara():
    """la cara negra y sin pelo, de la línea del pelo al mentón: la frente, el arco de las cejas, el hocico corto y los labios"""
    return forma([(56.2, 15.6), (59.6, 16.4), (61.6, 18.8), (62.4, 21.2), (61.8, 23.2), (62.2, 25), (63.9, 26.9), (65.4, 29.4),
                  (65.5, 31.6), (64.6, 33.6), (62.8, 35.3), (60, 36.4), (57.6, 36.2), (55.6, 34.2), (55.2, 30.2), (55.6, 25.6),
                  (55.4, 21), (55.4, 17.4)], 3)


def pierna(lejos=False):
    d = np.array([8.5, -1.5]) if lejos else np.zeros(2)
    muslo = tubo([(40, 73) + d, (52, 62) + d, (63.5, 51.5) + d], [6.2, 5.4, 4.2])
    canilla = tubo([(64, 51.5) + d, (66.2, 63.5) + d, (66.8, 75.8) + d], [4.0, 3.4, 2.7])
    # el pie como una mano: el talón, la planta larga y los dedos doblados sobre el suelo; el dedo gordo, aparte y hacia adentro
    pie = forma([(63.6, 75.4) + d, (69.2, 76.2) + d, (74.4, 77.8) + d, (78.2, 79.6) + d, (79.4, 81.6) + d, (76.6, 82.4) + d,
                 (66, 82.4) + d, (62.8, 80.4) + d], 3)
    if not lejos:
        return [muslo, canilla, pie]
    # del pie de allá se ve el lado de adentro: el dedo gordo, separado como un pulgar, sale del empeine hacia adelante
    dedo_gordo = tubo([(70.4, 79.6) + d, (73.6, 81.2) + d, (75.6, 81.6) + d], [1.2, 1.0, .8])
    return [muslo, canilla, pie, dedo_gordo]


def brazo(lejos=False):
    d = np.array([-7, 3]) if lejos else np.zeros(2)
    arriba_ = tubo([(47, 40) + d, (49, 50) + d, (51.5, 58.5) + d], [4.2, 3.6, 3.1])
    antebrazo = tubo([(51.5, 58.5) + d, (59, 53.5) + d, (66.5, 48.5) + d], [3.0, 2.7, 2.3])
    mano = forma([(65.5, 46.2) + d, (70.5, 47) + d, (73.5, 50) + d, (74, 55) + d, (71.8, 56.2) + d, (70.5, 52.8) + d,
                  (67.5, 51.5) + d, (64.8, 50.5) + d], 3)
    return [arriba_, antebrazo, mano]


def dibujar(l):
    for m in (l.masa(pierna(True), material='lejos', alto=.6, brillo=.04, vientre=0, linea=.75, hondo=0),
              l.masa(brazo(True), material='lejos', alto=.6, brillo=.04, vientre=0, linea=.75, hondo=0)):
        l.pelaje(m, densidad=1, largo=1.8, ancho=.2, alfa=.3, semilla=18, claro=.35, mechon=2, curva=6, desvio=6,
                 flujo=lambda x, y: 88 if x > 66 else -40)
    cr = craneo()
    c = l.masa([torso(), cr], brillo=.06, vientre=.2, contraluz=.35, linea=.8,
               bultos=[(ovalo(49, 22.5, 8, 7), .5), (ovalo(44, 44, 10, 9), .3), (ovalo(36, 64, 9, 12), .3)])
    # el pelo largo: en la cabeza baja desde la raya (arriba) y cae hacia atrás; en el lomo, hacia abajo; en mechones
    l.pelaje(c, densidad=1.3, largo=2.6, ancho=.24, alfa=.42, semilla=11, curva=6, desvio=5, claro=.4, mechon=3,
             flujo=lambda x, y: (100 + (x - 52) * -2.2) if y < 36 else 100 + (x - 40) * .5)
    # la cara negra; la línea solo donde la cara es el borde del dibujo (adentro se junta con el pelo sin línea); el borde del pelo
    # sobre la cara, irregular: el pelo de la sien y de la mejilla cae hacia atrás
    pelo = cr.difference(cara())
    entra = peludo(pelo, largo=.9, paso=1.3, donde=lambda x, y, nx, ny: nx > .3 and y > 16.5, semilla=5, flujo=120,
                   mezcla=.55).difference(pelo)
    f = l.masa(cara().difference(entra), material='oscuro', alto=.5, brillo=.3, vientre=0, linea=.8, hondo=.2, contraluz=.25,
               arroja=False, sin_tinta=cr.buffer(-.55),
               bultos=[(ovalo(63.2, 30.6, 3.6, 4), .28), (ovalo(59.6, 20.4, 3.6, 2, -12), .15)])
    l.mancha(forma([(62.2, 31.6), (64.2, 30.7), (65.5, 31.1), (65.3, 32.6), (64.3, 34), (62.8, 34.9), (63.6, 33.2), (63.4, 32.2)], 2),
             'A6BDB6', .75, dentro=f, difuso=.3)                                               # los labios, claros
    l.mancha(ovalo(64.2, 28.2, .55, .36, 25), '05201C', .8, dentro=f)                          # la narina
    # la oreja chica, en forma de C, medio tapada por el pelo que cae de la cabeza
    oreja = forma([(51.4, 22.6), (52.6, 23.4), (53, 25.4), (52.4, 27.6), (51, 28.4), (50, 27.2), (50.2, 24.4)], 3)
    o = l.masa(oreja, material='lejos', alto=.35, brillo=.05, vientre=0, tinta=False, hondo=0, arroja=False, contraluz=0)
    l.trazo([(52.3, 23.2), (50.6, 23.9), (50.2, 26), (51.2, 28)], [.1, .36, .3, .1], alfa=.75, difuso=.08)   # el borde de la oreja
    l.trazo([(51.9, 24.6), (51.3, 25.4), (51.5, 26.6)], [.1, .22, .1], alfa=.5, dentro=o, difuso=.1)          # su pliegue
    l.pelaje(c, densidad=3.5, largo=2, ancho=.24, alfa=.6, semilla=17, claro=.25, mechon=2, curva=5, desvio=5,
             zona=ovalo(50.6, 22.6, 2.8, 1.6, -20), flujo=112)                                   # el pelo tapa la oreja arriba
    pr = l.masa(pierna(), alto=.6, brillo=.06, vientre=.2, linea=.8, hondo=0, raices=[(40, 72, 3, 9)])
    l.pelaje(pr, densidad=1.1, largo=2, ancho=.22, alfa=.36, semilla=13, claro=.4, mechon=2, curva=6, desvio=6,
             flujo=lambda x, y: -40 if y < 62 and x < 62 else (85 if y < 76 else 0))
    b = l.masa([peludo(u, largo=1.4, paso=1.2, donde=lambda x, y, nx, ny: ny > .25 or nx < -.4, semilla=14,
                       flujo=lambda x, y: 100 if x < 52 else 170) if i < 2 else u for i, u in enumerate(brazo())],
               alto=.6, brillo=.06, vientre=.2, linea=.8, hondo=0, raices=[(47, 40, 2.5, 7)])
    l.pelaje(b, densidad=1.2, largo=2, ancho=.22, alfa=.36, semilla=15, claro=.4, mechon=2, curva=6, desvio=6,
             flujo=lambda x, y: 95 if x < 52 else (175 if x < 66 else 60))
    for p in (((68, 48.5), (71.5, 49.2), (72.8, 52)), ((67.2, 50.2), (70, 51.8), (70.8, 54.6))):
        l.trazo(list(p), .22, alfa=.4, dentro=b)                                              # los dedos largos, doblados
    for p in (((76.4, 79.4), (78.4, 80.4), (78.8, 82)), ((73.8, 78.8), (75.6, 80.4), (75.8, 82.2))):
        l.trazo(list(p), .2, alfa=.35, dentro=pr)                                             # los dedos del pie, doblados al suelo


CARA = dict(ojo=[59.3, 24.4], k=1.2, boca=[63.2, 33.1], kb=1.6, giro=6, pb=.7, wb=.6)
CARA['marco'] = [43.0, 9.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="55" cy="%.1f" rx="38" ry="4.6" style="opacity:.28"/>' % (SUELO + .6)
         + '<path d="M6 86q.3-2.8-1-4.6M8.5 86.4q.2-3 1.4-4.6M108 87q-.3-3 1.2-5M110.4 87.4q0-2.8 1.6-4.4"' + AGUA + '/>')
LISTO = True
