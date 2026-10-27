# -*- coding: utf-8 -*-
"""Las postales del Huang He, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: los montes Bayan Har, nevados, y los dos lagos, Gyaring y Ngoring; entre ellos y después, el río que ya nace dorado
  de barro: el río Amarillo;
- Lanzhou: «un lanchón que cruza el río lleno de fideos»: el lanchón, cargado de fideos dorados estirados a mano que cuelgan por la
  borda; atrás, el primer puente de hierro sobre el Amarillo, con sus arcos;
- Yinchuan: «un yin y un yang de arroz en medio del desierto»: visto desde arriba, el arrozal redondo con su mitad dorada y su mitad
  verde, regado por canales, entre las dunas;
- Baotou: «un bao de acero al vapor en lo alto de la curva»: el bao dorado, con sus pliegues y su vapor, en el vértice de la gran
  vuelta del río; las acerías y las dunas alrededor;
- Zhengzhou: «un zapato de bronce gigante marca el kilómetro cero»: el zapato dorado en su pedestal con el cero, entre las vías del
  tren y las murallas de tierra de la capital Shang;
- Kaifeng: «un río que pasa por arriba, a diez metros sobre los techos»: el río dorado de barro corre entre sus diques más alto que la
  ciudad, con su pagoda de hierro, y la gente mira hacia arriba; abajo, las ciudades enterradas;
- Jinan: «un genio sale de un manantial y no del río»: el genio dorado brota de la fuente de Baotu, con sus tres chorros, entre sauces;
  el río pasa de largo, lejos, al norte;
- Dongying: «un dong de campana suena en un delta nuevo cada año»: la campana dorada que suena sobre el delta de barro, con los pozos
  de petróleo que cabecean y las gaviotas;
- el mar: el golfo de Bohai y el barro nuevo: el penacho dorado del río Amarillo que se abre en el agua salada; el faro, las gaviotas
  y, lejos, una fábrica (la balsa se deshace en el delta: la madera se vende y las pieles vuelven en camello).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, cordillera, nube, orilla, palmera, pasto, piedra, prado,  # noqa: F401
                     reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'
BARRO = 'C6A866'           # el loes, la tierra amarilla


def piel(l, piezas, tono=.45):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def rio_dorado(l, g, ondas=8, semilla=0):
    """el río Amarillo, dorado de barro, con sus remolinos claros: es lo que hay que recordar"""
    m = l.masa(g, material='acento', alto=.1, brillo=.2, vientre=0, hondo=0, linea=.35, escalon=0, contraluz=.2, arroja=False)
    rng = np.random.default_rng(semilla)
    x0, y0, x1, y1 = g.bounds
    for _ in range(ondas):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        l.trazo([(x, y), (x + 1.4, y - .25), (x + 2.8, y)], .16, color='FBEFCB', alfa=.8, dentro=m)
    return m


def rio_barroso(l, y, semilla=1):
    """el río de fondo, turbio de barro (no dorado: lo dorado es la imagen)"""
    a = rio(l, y, semilla=semilla)
    l.mancha(box(-2, y - 1, 122, 41.6), BARRO, .5, dentro=a)
    return a


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .5)
    nube(l, 100, 4, 12, .45)
    cordillera(l, [(-2, 15), (8, 9), (18, 11.4), (28, 6.6), (40, 10.4), (52, 8), (62, 12), (70, 15)], nieve=10.6)
    cordillera(l, [(60, 15), (72, 10), (84, 6.4), (96, 10), (108, 7.4), (122, 11)], nieve=10)
    prado(l, 14.6, 41, .38)
    # los dos lagos, Gyaring y Ngoring, y el río dorado que los une y después baja hacia nosotros
    for g in (forma([(6, 18), (28, 16.6), (40, 18.4), (30, 22), (10, 22)], 2), forma([(78, 17.4), (100, 16.4), (116, 18.4), (104, 22.4), (82, 22)], 2)):
        agua(l, g, ondas=4, semilla=2, linea=.3)
    rio_ = unary_union([cinta([(38, 19.6), (50, 20.6), (62, 19.6), (80, 19.6)], [1.4, 1.8, 2, 2.2], 8),
                        cinta([(98, 21.6), (92, 25), (76, 27), (58, 28.6), (44, 32), (52, 37), (64, 41.6)], [2.4, 3, 3.6, 4.4, 5.4, 6.6, 8], 10)])
    rio_dorado(l, rio_, 14, 3)
    for _ in range(16):
        x, y = rng.uniform(0, 120), rng.uniform(24, 40)
        l.trazo([(x - .6, y), (x, y - .9), (x + .6, y)], .14, color='2F8A74', alfa=.6)


# ------------------------------------------------------------------------------------------------ Lanzhou
def lanzhou(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # los cerros de loes, la ciudad y el puente de hierro de arcos
    for pts in ([(-2, 18), (12, 10), (28, 12.6), (40, 18)], [(84, 18), (96, 11), (110, 9.6), (122, 13), (122, 18)]):
        g = Polygon(pts + [(pts[-1][0], 19), (pts[0][0], 19)]).buffer(0)
        m = l.masa(g, material='vientre', alto=.3, brillo=.08, vientre=0, hondo=0, linea=.35)
        l.mancha(g, BARRO, .55, dentro=m)
    casitas(l, -1, 122, 19.4, 3.4, semilla=4)
    rio_barroso(l, 20)
    l.masa(box(-2, 18.6, 122, 19.6), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x0 in np.arange(4, 118, 22.8):                                   # los arcos de hierro
        arco = cinta([(x0 + 22 * t, 18.6 - 5.4 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 15)], [.6] * 15, 3)
        l.masa(arco, material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
        for t in np.linspace(.1, .9, 7):
            l.trazo([(x0 + 22 * t, 18.6 - 5.4 * math.sin(math.pi * t)), (x0 + 22 * t, 18.6)], .1, color='164F46', alfa=.85)
    # el lanchón cargado de fideos dorados, protagonista, que cruza el río
    l.mancha(ovalo(60, 35.4, 30, 1.4), 'FFFFFF', .45, difuso=.5)
    casco = forma([(28, 27.6), (92, 27.6), (96, 26), (93, 33), (88, 35.4), (32, 35.4), (27, 33), (24, 26)], 1)
    c = l.masa(casco, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(casco.buffer(1), '5A3E1E', .6, dentro=c)
    for y in (30, 32.6):
        l.trazo([(27, y), (93, y)], .12, color='3A2A0A', alfa=.5, dentro=c)
    monte = forma([(30, 27.8), (36, 18.6), (48, 15.6), (60, 15), (72, 15.6), (84, 18.6), (90, 27.8)], 2)
    l.mancha(monte, '93701A', .9)                                        # el fondo del montón, a la sombra
    hebras = []
    for k in range(70):                                                  # los fideos, hebra por hebra, en ondas y rulos
        y0 = rng.uniform(17, 27)
        x0 = rng.uniform(32, 88)
        largo = rng.uniform(8, 16)
        pts = [(x0 + t - largo / 2, y0 + 1.1 * math.sin(t * 1.3 + k)) for t in np.linspace(0, largo, 9)]
        pts = [(x, y) for x, y in pts if monte.buffer(-.4).contains(box(x - .1, y - .1, x + .1, y + .1))]
        if len(pts) > 3:
            hebras.append(tubo(pts, [.42] * len(pts), 4))
    l.masa(hebras, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.18, contraluz=.35)
    for x0 in (30, 40, 52, 66, 78, 88):                                  # los que cuelgan por la borda
        largo = rng.uniform(4, 7)
        pts = [(x0, 27.6), (x0 + rng.uniform(-1, 1), 27.6 + largo * .5), (x0 + rng.uniform(-1.4, 1.4), 27.6 + largo)]
        l.masa(tubo(pts, [.4, .35, .3], 6), material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.25)
    for k in range(3):                                                   # el vapor de los fideos recién hechos
        l.mancha(ovalo(50 + k * 9, 11.6 - k * .6, 2.4, 1.6), 'FFFFFF', .7, difuso=.6)


# ------------------------------------------------------------------------------------------------ Yinchuan
def yinchuan(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 28, 3, 12, .4)
    # visto desde arriba: el desierto con sus dunas, el río que pasa y los canales que llevan el agua
    tierra(l, 6, 41, desierto=.55)
    for _ in range(18):
        x, y = rng.uniform(0, 120), rng.uniform(8, 40)
        if 28 < x < 92 and 12 < y < 38:
            continue
        l.trazo([(x - 4, y + .6), (x, y - .6), (x + 4, y + .6)], .5, color='BF9129', alfa=.45)
    rio_barroso_g = cinta([(-2, 9), (40, 10.4), (80, 9.6), (124, 11)], [4, 4.4, 4.4, 4], 8)
    a = agua(l, rio_barroso_g, linea=.3)
    l.mancha(rio_barroso_g, BARRO, .5, dentro=a)
    for x0, x1 in ((40, 44), (80, 76)):                                  # los canales de dos mil años
        agua(l, cinta([(x0, 11), (x0 + (x1 - x0) * .5, 16), (x1, 21)], [1, 1, 1], 4), linea=.2)
    # el yin y el yang de arroz, protagonista: la mitad dorada (el arroz maduro) y la verde (el arroz nuevo), con sus dos puntos
    cx, cy, rx, ry = 60, 27, 26, 11.4
    disco = ovalo(cx, cy, rx, ry)
    mitad = Polygon([(cx - rx - 1, cy - ry - 1), (cx, cy - ry - 1), (cx, cy + ry + 1), (cx - rx - 1, cy + ry + 1)])
    yin = mitad.intersection(disco).union(ovalo(cx, cy - ry / 2, rx / 2, ry / 2)).difference(ovalo(cx, cy + ry / 2, rx / 2, ry / 2))
    yang = disco.difference(yin)
    l.mancha(ovalo(cx + 1, cy + 1.4, rx, ry), '0C3A33', .25, difuso=.8)
    v = l.masa(yang, material='cuerpo', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.45, contraluz=.3)
    o = l.masa(yin, material='acento', alto=.35, brillo=.45, vientre=0, hondo=0, linea=.45, contraluz=.35)
    for k in range(12):                                                  # las hileras de las matas de arroz
        y = cy - ry + 1 + k * (2 * ry - 2) / 11
        l.trazo([(cx - rx, y), (cx + rx, y)], .14, color='164F46', alfa=.45, dentro=v)
        l.trazo([(cx - rx, y), (cx + rx, y)], .14, color='6B4E10', alfa=.45, dentro=o)
    l.masa(ovalo(cx, cy - ry / 2, 3, 1.6), material='cuerpo', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35)
    l.masa(ovalo(cx, cy + ry / 2, 3, 1.6), material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35)


# ------------------------------------------------------------------------------------------------ Baotou
def bao(l, x, base, r):
    """un bao, el pan al vapor, dorado como de acero: redondo, con los pliegues que se juntan arriba y el vapor"""
    g = forma([(x - r, base), (x - r * 1.05, base - r * .5), (x - r * .7, base - r * 1.05), (x, base - r * 1.32), (x + r * .7, base - r * 1.05),
               (x + r * 1.05, base - r * .5), (x + r, base)], 2)
    l.mancha(ovalo(x + 1, base + .4, r * 1.1, r * .2), '0C3A33', .3, difuso=.5)
    m = l.masa(g, material='acento', alto=.6, brillo=.6, vientre=0, hondo=.1, linea=.45, contraluz=.45)
    for k in range(-4, 5):                                               # los pliegues, que suben al nudo de arriba
        l.trazo([(x + k * r * .22, base - r * .25), (x + k * r * .08, base - r * .9), (x, base - r * 1.24)], [.06, .25, .06], color='6B4E10', alfa=.55,
                dentro=m)
    l.trazo([(x - r * .7, base - r * .4), (x - r * .4, base - r * .9)], [.05, .35, .05], color='FBEFCB', alfa=.85, dentro=m)
    for k in range(3):
        l.mancha(ovalo(x - 3 + k * 3, base - r * 1.5 - k * 1.6, 1.6 + k * .5, 1.2 + k * .3), 'FFFFFF', .7 - k * .12, difuso=.4)
        l.trazo([(x - 3 + k * 3, base - r * 1.4), (x - 2 + k * 3, base - r * 1.7 - k)], .2, color='FFFFFF', alfa=.6)
    return g


def baotou(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 22, 3, 12, .4)
    # visto desde arriba: las dunas de Ordos, y el río que sube, da la gran vuelta arriba, en Baotou, y vuelve a bajar
    tierra(l, 5, 41, desierto=.5)
    for _ in range(16):
        x, y = rng.uniform(0, 120), rng.uniform(16, 40)
        l.trazo([(x - 4, y + .6), (x, y - .6), (x + 4, y + .6)], .5, color='BF9129', alfa=.45)
    curva_ = cinta([(8, 41.6), (14, 34), (26, 27.4), (42, 24.4), (60, 23.4), (78, 24.4), (94, 27.4), (106, 34), (112, 41.6)],
                   [4, 4.4, 4.8, 5, 5.2, 5, 4.8, 4.4, 4], 10)
    a = agua(l, curva_, ondas=10, semilla=7, linea=.35)
    l.mancha(curva_, BARRO, .5, dentro=a)
    # las acerías de Baotou, junto al vértice, con sus chimeneas y su humo
    for x, h in ((22, 7), (28, 9), (92, 8), (98, 10)):
        l.masa(box(x - .8, 21 - h, x + .8, 21.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        for k in range(3):
            l.mancha(ovalo(x + 1.4 + k * 2, 21 - h - 1.4 - k * 1, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .6 - k * .12, difuso=.4)
    l.masa([box(12, 16.6, 26, 21.4), box(88, 16, 104, 21.4)], material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.25)
    # el bao de acero dorado, protagonista, en lo alto de la curva
    bao(l, 60, 22.6, 11)


# ------------------------------------------------------------------------------------------------ Zhengzhou
def zapato(x, base, s=1.0):
    """un zapato de bronce, de perfil, con la punta a la derecha, levantada como en los zapatos antiguos"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    return forma(P([(-12, 0), (-12.6, -5), (-11, -9.6), (-6, -10.4), (-4.4, -6), (2, -5), (8.6, -4.2), (12.4, -3.6), (14.6, -5.6), (15, -2.4), (12.6, 0)]), 2)


def zhengzhou(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # atrás, las murallas de tierra de la capital Shang; los campos, el río lejos y las vías del tren que se cruzan
    prado(l, 15, 41, .3)
    rio_barroso(l, 14.2)
    prado(l, 17.6, 41, .3)
    mu = l.masa(forma([(-2, 21), (-2, 17.4), (40, 17), (44, 19.6), (-2, 21.6)], 1).union(forma([(76, 19.6), (80, 17), (122, 17.4), (122, 21.6)], 1)),
                material='vientre', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(box(-2, 16, 122, 22), BARRO, .6, dentro=mu)
    for x in np.arange(-2, 122, 1.4):
        l.trazo([(x, 17.6), (x, 21)], .08, color='6B4E10', alfa=.3, dentro=mu)
    for (a, b) in (((-2, 36), (124, 26)), ((-2, 26), (124, 37))):        # las vías que se cruzan: el cruce de trenes de China
        for d in (-.8, .8):
            l.trazo([(a[0], a[1] + d), (b[0], b[1] + d)], .22, color='5A3E1E', alfa=.85)
        for t in np.linspace(0, 1, 40):
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            l.trazo([(x, y - 1.3), (x, y + 1.3)], .3, color='8A6A3A', alfa=.6)
    l.masa([box(4, 30.6, 22, 34), box(22.6, 30.6, 36, 34)], material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)      # un tren
    # el pedestal con el cero, y el zapato de bronce dorado, protagonista, que marca el kilómetro cero
    pd = piedra(l, box(46, 26.6, 74, 33.4), .2, .4)
    cero = ovalo(60, 30, 2, 2.4).difference(ovalo(60, 30, 1.1, 1.5))
    l.mancha(cero, '3A2A0A', .9, dentro=pd)
    z = zapato(59, 26.6, 1.3)
    l.mancha(affinity.translate(z, 1, .6), '0C3A33', .3, difuso=.5)
    m = l.masa(z, material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.trazo([(48, 19.4), (60, 20.2), (72, 21.4)], [.06, .3, .06], color='FBEFCB', alfa=.8, dentro=m)
    for x in np.arange(46, 58, 1.8):                                     # las costuras
        l.trazo([(x, 25.6), (x + .6, 25.4)], .12, color='6B4E10', alfa=.6, dentro=m)


# ------------------------------------------------------------------------------------------------ Kaifeng
def kaifeng(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    nube(l, 22, 3, 12, .4)
    nube(l, 100, 3, 10, .35)
    # en corte: los diques, altos, y entre ellos el río dorado de barro, más arriba que la ciudad
    dique = forma([(-2, 22), (-2, 7.6), (6, 7.2), (18, 14.6), (102, 14.6), (114, 7.2), (122, 7.6), (122, 22)], 1)
    d = l.masa(dique, material='vientre', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.4)
    l.mancha(dique, BARRO, .6, dentro=d)
    for x in (6, 114):
        arbol(l, x, 7, 1.6, semilla=x)
    rio_dorado(l, forma([(10, 8), (110, 8), (102, 14.6), (18, 14.6)], 0), 18, 11)
    l.trazo([(12, 8), (108, 8)], .2, color='FBEFCB', alfa=.8)
    # la ciudad, abajo del río: las casas de techos curvos, la pagoda de hierro y la gente que mira hacia arriba
    suelo = l.masa(box(-2, 22, 122, 28), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 22, 122, 28), BARRO, .35, dentro=suelo)
    for x in np.arange(2, 120, 9.6):
        if 52 < x < 68:
            continue
        c = l.masa(box(x, 18.6, x + 7, 22.4), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
        l.mancha(box(x + 2.6, 20, x + 4.4, 22.4), '164F46', .75, dentro=c)
        l.masa(forma([(x - 1.4, 18.8), (x + 1, 17.2), (x + 6, 17.2), (x + 8.4, 18.8)], 1), material='lejos', alto=.25, brillo=.15, vientre=0, hondo=0,
               linea=.3)
    pg = []
    for k in range(7):                                                   # la pagoda de hierro, de pisos con aleros
        y = 22.4 - k * 2.2
        w = 4 - k * .36
        pg += [box(60 - w * .7, y - 2.2, 60 + w * .7, y), forma([(60 - w - .6, y - 1.8), (60, y - 2.6), (60 + w + .6, y - 1.8)], 0)]
    pg.append(Polygon([(59.4, 7), (60, 4.4), (60.6, 7)]))
    p = l.masa(pg, material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(pg).buffer(1), '5A3E1E', .45, dentro=p)
    for x in (30, 88):                                                   # la gente, que mira el río allá arriba
        piel(l, [ovalo(x, 23.4, .9, 1)], .45)
        l.masa(forma([(x - 1, 27.6), (x - 1.1, 24.4), (x + 1.1, 24.4), (x + 1, 27.6)], 1), material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0,
               linea=.25)
        l.trazo([(x + .6, 24.8), (x + 2.6, 21.4)], .3, color='93701A', alfa=.9)
    # abajo, enterradas en el barro, las ciudades de antes, una debajo de otra
    for k, y0 in enumerate((28, 32.6, 37.2)):
        capa = box(-2, y0, 122, y0 + 4.6)
        cm = l.masa(capa, material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.25, escalon=0, contraluz=0, arroja=False)
        l.mancha(capa, '8A6A3A', .35 + k * .12, dentro=cm)
        for x in np.arange(6 + k * 4, 118, 16):
            l.trazo([(x, y0 + 4), (x, y0 + 2), (x + 2.4, y0 + 1), (x + 4.8, y0 + 2), (x + 4.8, y0 + 4)], .16, color='3A2A0A', alfa=.4)


# ------------------------------------------------------------------------------------------------ Jinan
def genio(l, x, base, s=1.0):
    """un genio dorado que sale del agua del manantial: la cola en remolino, el torso, los brazos cruzados, el turbante y la sonrisa"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cola = tubo(P([(0, 0), (-2.6, -2.4), (1.6, -5), (-1.6, -8), (0, -11)]), [.8 * s, 1.4 * s, 2 * s, 2.6 * s, 3 * s], 10)
    torso = forma(P([(-3.4, -10.4), (-4, -14), (-3, -17.6), (3, -17.6), (4, -14), (3.4, -10.4)]), 2)
    brazos = [tubo(P([(-3.4, -16.4), (-5.4, -14), (2, -13.4)]), [1.2 * s, 1.1 * s, 1 * s], 6), tubo(P([(3.4, -16.4), (5.4, -14), (-2, -12.6)]), [1.2 * s, 1.1 * s, 1 * s], 6)]
    cabeza = O(0, -20.2, 2.4, 2.6)
    m = l.masa([cola, torso] + brazos + [cabeza], material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.masa([forma(P([(-2.8, -21.4), (-2.6, -23.6), (0, -24.6), (2.6, -23.6), (2.8, -21.4)]), 2), O(0, -25, .7, .7)], material='claro', alto=.45,
           brillo=.3, vientre=0, hondo=0, linea=.35)                                            # el turbante
    for dx in (-.9, .9):
        l.mancha(O(dx, -20.4, .28, .32), '05201C', 1)
    l.trazo(P([(-.9, -19), (0, -18.6), (.9, -19)]), .16 * s, color='0C3A33', alfa=.9)
    l.trazo(P([(-1, -17.8), (-1.6, -17.4)]), .2 * s, color='6B4E10', alfa=.8)                    # el bigote fino
    l.trazo(P([(1, -17.8), (1.6, -17.4)]), .2 * s, color='6B4E10', alfa=.8)
    return m


def jinan(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # lejos, al norte, el río Amarillo que pasa de largo; la ciudad con sus techos y sus sauces
    prado(l, 12, 20, .26)
    rio_barroso(l, 12.6)
    prado(l, 15, 41, .26)
    for x in np.arange(2, 120, 9):
        l.masa([box(x, 16.6, x + 6, 20), forma([(x - 1, 16.8), (x + 1, 15.4), (x + 5, 15.4), (x + 7, 16.8)], 1)], material='claro', alto=.2, brillo=.1,
               vientre=0, hondo=0, linea=.25, arroja=False)
    for x in (10, 22, 98, 110):                                          # los sauces llorones: el tronco y las ramas largas que caen
        l.masa(tubo([(x, 36), (x + .3, 28), (x - .4, 22)], [.7, .55, .4], 4), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        for k in range(15):
            dx = (k - 7) * .7
            l.trazo([(x + dx * .3, 21.6), (x + dx * .9, 21), (x + dx * 1.4, 24 + abs(dx) * .3), (x + dx * 1.5, 31 - abs(dx) * .6)],
                    [.12, .3, .3, .1], color=('2F8A74', '4EB196')[k % 2], alfa=.9)
    # la fuente de Baotu: el estanque con su baranda de piedra y los tres chorros que brotan del suelo
    estanque = forma([(26, 34), (34, 28.4), (86, 28.4), (94, 34), (86, 39.6), (34, 39.6)], 2)
    piedra(l, estanque.buffer(1.4).difference(estanque), .25, .35)
    agua(l, estanque, ondas=8, semilla=12, linea=.3)
    for x in (44, 76):
        l.mancha(ovalo(x, 33.2, 3, .9), 'FFFFFF', .85)
        for k in range(3):
            l.trazo([(x - 1 + k, 33), (x - 1.4 + k * 1.4, 30.4)], .5, color='FFFFFF', alfa=.85)
    # el genio dorado, protagonista, que sale del chorro del medio
    l.mancha(ovalo(60, 33.6, 4, 1.2), 'FFFFFF', .9)
    genio(l, 60, 33.4, 1.18)


# ------------------------------------------------------------------------------------------------ Dongying
def campana(l, x, y, h):
    """una campana dorada que suena, colgada de su travesaño, con su badajo y las ondas del dong"""
    l.masa(box(x - h * .55, y - h * .08, x + h * .55, y + h * .02), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    g = forma([(x - h * .16, y), (x - h * .22, y + h * .2), (x - h * .28, y + h * .55), (x - h * .5, y + h * .9), (x + h * .5, y + h * .9),
               (x + h * .28, y + h * .55), (x + h * .22, y + h * .2), (x + h * .16, y)], 2)
    g = affinity.rotate(g, -12, origin=(x, y))
    m = l.masa(g, material='acento', alto=.55, brillo=.55, vientre=0, hondo=0, linea=.45, contraluz=.45)
    for v in (.3, .76):
        a = affinity.rotate(Polygon([(x - h * .4, y + h * v), (x + h * .4, y + h * v), (x, y + h * v + .01)]), -12, origin=(x, y))
        l.trazo([tuple(a.exterior.coords[0]), tuple(a.exterior.coords[1])], .2, color='6B4E10', alfa=.6, dentro=m)
    bx, by = affinity.rotate(Polygon([(x + h * .08, y + h), (x + h * .09, y + h), (x + h * .08, y + h + .01)]), -12, origin=(x, y)).exterior.coords[0]
    l.masa(ovalo(bx, by, h * .07, h * .07), material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)
    for k in range(3):                                                   # las ondas del sonido
        r = h * (.75 + k * .22)
        for lado in (-1, 1):
            l.trazo([(x + lado * r * math.cos(t), y + h * .5 - r * .6 * math.sin(t)) for t in np.linspace(-.5, .5, 8)], .3, color='FFFFFF', alfa=.9 - k * .2)
    return g


def cabeceo(l, x, base, s=1.0):
    """un pozo de petróleo que cabecea: el caballete, el balancín con su cabeza de caballo y el contrapeso, oscuros"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    l.masa([Polygon(P([(-3, 0), (-2.4, 0), (0, -6), (-.6, -6)])), Polygon(P([(2.4, 0), (3, 0), (.6, -6), (0, -6)])),
            Polygon(P([(-7, -6.6), (6, -7.8), (6.2, -7), (-7, -5.8)])), forma(P([(5.6, -9), (8, -8.4), (8.2, -5.6), (6.4, -6.6)]), 1),
            box(x - 7.6 * s, base - 5.6 * s, x - 5.6 * s, base - 3 * s), box(x + 7 * s, base - 5.6 * s, x + 7.4 * s, base)], material='oscuro', alto=.25,
           brillo=.3, vientre=0, hondo=0, linea=.25)


def dongying(l):
    rng = np.random.default_rng(14)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    # el delta nuevo, de barro, que gana tierra al mar, con sus canales; el mar a la derecha
    horizonte = 18
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.6), '64C8AA', .5, dentro=m, difuso=.6)
    delta = forma([(-2, 18.4), (40, 19), (64, 22), (80, 28), (88, 34), (84, 41.6), (-2, 41.6)], 2)
    d = l.masa(delta, material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.35)
    l.mancha(delta, BARRO, .55, dentro=d)
    for pts in ([(-2, 24), (30, 26), (60, 30), (84, 36)], [(-2, 32), (24, 33), (50, 36.4), (70, 41.6)]):
        a = agua(l, cinta(pts, [1.4, 1.8, 2.2, 2.6], 6), linea=.25)
        l.mancha(cinta(pts, [1.4, 1.8, 2.2, 2.6], 6), BARRO, .4, dentro=a)
    for x, y in ((14, 30.6), (34, 23.4), (66, 26.6), (40, 39.6)):
        cabeceo(l, x, y, .9)
    for x, y, s in ((84, 8, .8), (94, 12, .6), (104, 7, .7), (20, 12, .6)):
        ave(l, x, y, s)
    # la campana dorada, protagonista, que suena sobre el delta nuevo
    campana(l, 60, 4, 17)


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    rng = np.random.default_rng(16)
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .5)
    nube(l, 96, 4, 12, .45)
    # el golfo de Bohai, el faro en su punta y, lejos, una fábrica
    horizonte = 16
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa([box(96, horizonte - 4, 110, horizonte), box(104, horizonte - 9, 105.6, horizonte - 3.8)], material='claro', alto=.2, brillo=.12, vientre=0,
           hondo=0, linea=.25)
    for k in range(3):
        l.mancha(ovalo(106 - k * 2.2, horizonte - 10.4 - k * 1, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .6 - k * .12, difuso=.4)
    # la tierra nueva de barro, abajo a la izquierda, con el faro, y el río que llega
    costa = forma([(-2, 41.6), (-2, 24), (14, 24.6), (26, 28), (34, 34), (30, 41.6)], 2)
    c = l.masa(costa, material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.35)
    l.mancha(costa, BARRO, .55, dentro=c)
    fr = l.masa([forma([(10.4, 26), (10.8, 13.6), (13, 13.6), (13.4, 26)], 0), box(10, 12.4, 13.8, 13.8)], material='claro', alto=.3, brillo=.2, vientre=0,
                hondo=0, linea=.3)
    l.mancha(box(9, 17, 15, 18.6), '2F8A74', .85, dentro=fr)
    l.masa(Polygon([(10.2, 12.6), (11.9, 10.6), (13.6, 12.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # el penacho dorado del río Amarillo, protagonista, que se abre en el agua salada
    a = agua(l, cinta([(-2, 36), (12, 35.6), (26, 35)], [3, 3.6, 4.4], 6), linea=.3)                   # la boca del río
    penacho = forma([(24, 33), (34, 26.6), (48, 24), (66, 22.6), (86, 24), (100, 28.6), (104, 34), (96, 39), (76, 41.6), (40, 41.6), (28, 38)], 3)
    for k, (enc, alfa) in enumerate(((0, .45), (3, .5), (6, .6), (9, .65))):  # de afuera hacia adentro, cada vez más dorado
        g = penacho.buffer(-enc)
        if not g.is_empty:
            l.mancha(g, 'E8B952', alfa, difuso=2.4)
    l.mancha(cinta([(-2, 36), (12, 35.6), (26, 35)], [3, 3.6, 4.4], 6), 'E8B952', .8)
    for k in range(8):                                                   # los remolinos de barro, que se abren en abanico desde la boca
        r = 8 + k * 2.6
        l.trazo([(26 + r * math.cos(t), 35 - r * .5 * math.sin(t)) for t in np.linspace(-.6, 1.2, 14)], .22, color='FBEFCB', alfa=.75)
    for x, y, s in ((60, 8, .8), (72, 11, .6), (40, 10, .7)):
        ave(l, x, y, s)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Lanzhou', dibujar=lanzhou), dict(clave='Yinchuan', dibujar=yinchuan),
            dict(clave='Baotou', dibujar=baotou), dict(clave='Zhengzhou', dibujar=zhengzhou), dict(clave='Kaifeng', dibujar=kaifeng),
            dict(clave='Jinan', dibujar=jinan), dict(clave='Dongying', dibujar=dongying), dict(clave='mar', dibujar=mar)]
LISTO = True
