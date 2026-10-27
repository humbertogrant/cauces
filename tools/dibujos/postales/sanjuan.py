# -*- coding: utf-8 -*-
"""Las postales del San Juan, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: el lago de Nicaragua, enorme, con los dos volcanes de Ometepe, y el río dorado que sale de él hacia el Caribe;
- San Carlos: «un lago gigante se vacía por una pajilla»: la pajilla dorada, de las que se doblan, metida en el lago, que pasa por
  encima del cerro del fuerte y echa el agua en el río;
- Sábalos: «un sábalo, un pez plateado enorme, salta por encima del bote y saluda»: el sábalo de plata, con las aletas y la cola
  doradas, que salta en arco sobre el bote del pescador y saluda con la aleta;
- El Castillo: «un castillo de piedra sobre un raudal y una muchacha de 19 años disparando el cañón»: la fortaleza en su cerro, y
  Rafaela, de vestido dorado, que dispara el cañón desde la muralla; abajo, el raudal;
- Boca San Carlos: «una boca abierta se toma un río entero de un trago»: la boca dorada, abierta, que se toma el río San Carlos, que
  llega de Costa Rica; enfrente, la selva;
- Delta: «una letra griega Δ partida en dos por un cuchillo»: la Δ dorada partida por el cuchillo, sobre el río que se parte: el brazo
  ancho, el Colorado, hacia Costa Rica, y el flaco, el San Juan;
- San Juan de Nicaragua: «un pueblo gris junto a un canal que nunca se terminó de cavar»: las casas grises bajo el cielo gris, la zanja
  del canal que se acaba de golpe en un montón de tierra y la pala dorada clavada ahí, abandonada; a un lado, los manglares;
- el mar: el vapor del Tránsito, la barca del juego, de casco dorado, con su toldo, su chimenea y su rueda a popa, que sale al Caribe
  por la bahía, entre los manglares y el faro; en el agua, la aleta de Tiburcio, el tiburón toro, que va y viene.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = 'A2683A'            # el tono de la piel: un café tibio sobre el pálido de `vientre`
MADERA = '5A3E1E'
GRIS = '7E8C89'


def piel(l, piezas, tono=.6):
    """piezas de piel: el pálido de `vientre` teñido de café"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def madera(l, piezas, tono=.55, linea=.3):
    """piezas de madera: el pálido de `vientre` teñido de café"""
    m = l.masa(piezas, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=linea)
    l.mancha(unary_union(piezas).buffer(1), MADERA, tono, dentro=m)
    return m


def piedra_gris(l, piezas, tono=.45, linea=.35):
    """piezas de piedra gris"""
    m = l.masa(piezas, material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=linea, escalon=.2, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), GRIS, tono, dentro=m)
    return m


def lancha(l, x, y, s=1.0):
    """una lancha de madera, de perfil, mirando a la derecha, con su motor"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa(box(x - 8.6 * s, y - 3 * s, x - 7.4 * s, y + .8 * s), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    c = madera(l, [forma(P([(-8, -1.6), (-7, -.6), (7, -.6), (9, -2), (8, .6), (5, 1.2), (-6, 1.2), (-7.6, .6)]), 2)], .5, linea=.35)
    l.trazo(P([(-7.6, -1), (0, -.6), (8.4, -1.6)]), [.05, .3, .05], color='164F46', alfa=.6, dentro=c)


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 60, 4, 14, .45)
    nube(l, 104, 5, 10, .4)
    # el lago, enorme, hasta el horizonte, con los dos volcanes de Ometepe en su isla: el Concepción, un cono perfecto, y el Maderas
    lago = l.masa(box(-2, 14, 122, 41.6), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 14, 122, 16), '64C8AA', .5, dentro=lago, difuso=.8)
    for _ in range(22):
        x, y = rng.uniform(0, 116), rng.uniform(16, 28)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa(Polygon([(8, 14.6), (15, 9.6), (19.4, 4.6), (21.6, 4.6), (26, 9.6), (31, 12.4), (36, 11), (40, 10.6), (45, 12.2), (50, 14.6)]),
           material='lejos', alto=.35, brillo=.08, vientre=0, hondo=.1, linea=.35, escalon=.3, contraluz=.3)
    nube(l, 20.6, 3.6, 7, .5)
    lancha(l, 86, 22, .9)
    # la orilla de acá, con sus casas, y el río dorado, protagonista, que sale del lago y baja hacia nosotros
    rio_ = Polygon([(46, 26.4), (74, 26.4), (70, 30), (72, 35), (80, 41.8), (40, 41.8), (48, 35), (50, 30)]).buffer(1.2).buffer(-1.2)
    m = l.masa(rio_, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=0, escalon=.1, contraluz=.3)
    l.mancha(box(40, 25, 80, 28.4), '64C8AA', .45, dentro=m, difuso=1.4)    # el agua del lago que entra al río
    for x, y, w in ((60, 29.4, 2.4), (55.6, 31.6, 2.8), (64.4, 32.6, 2.8), (59.4, 35, 3.2), (52.6, 37.6, 3.4), (66.6, 38, 3.4), (60, 40.2, 3.6)):
        l.trazo([(x - w, y + .3), (x - w / 2, y - .2), (x, y + .2), (x + w / 2, y - .2), (x + w, y + .3)], .24, color='FFFFFF', alfa=.85, dentro=m)
    for pts in ([(-2, 41.6), (-2, 27.6), (20, 26.8), (36, 26.6), (47, 27), (51, 30), (49, 35), (41, 41.6)],
                [(122, 41.6), (122, 27.4), (100, 26.6), (84, 26.6), (73, 27), (69, 30), (71, 35), (79, 41.6)]):
        b = orilla(l, forma(pts, 2), tinte=.3)
    for x in (44, 47, 50, 70, 73, 76):                                    # los juncos de la boca
        y = 27.6 + abs(x - 60) * .02
        for dx in (-.6, 0, .6):
            l.trazo([(x + dx, y + .4), (x + dx * 1.6, y - 2.2)], .14, color='2F8A74', alfa=.85)
    for x, w, h in ((14, 5, 3.2), (20.6, 4.6, 2.8), (26.6, 5, 3.4), (90, 4.6, 3), (96, 5, 3.4)):
        c = l.masa(box(x, 30.6 - h, x + w, 30.6), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.masa(Polygon([(x - .4, 30.6 - h), (x + w / 2, 30.6 - h - 1.6), (x + w + .4, 30.6 - h)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0,
               linea=.25)
    for x, y, s in ((30, 8, .6), (36, 6.6, .5), (80, 8, .6)):
        ave(l, x, y, s)


# ------------------------------------------------------------------------------------------------ San Carlos
def san_carlos(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 96, 4, 12, .45)
    # el lago, a la izquierda, el cerro del fuerte al medio y el río que sale a la derecha
    lago = l.masa(box(-2, 16, 46, 41.6), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 16, 46, 18), '64C8AA', .5, dentro=lago, difuso=.8)
    for _ in range(12):
        x, y = rng.uniform(0, 40), rng.uniform(18, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    orilla(l, forma([(70, 41.6), (74, 24.4), (96, 23.4), (122, 23), (122, 41.6)], 1), tinte=.26)
    agua(l, forma([(84, 41.6), (88, 30), (100, 27), (122, 26), (122, 41.6)], 2), ondas=8, semilla=4, linea=.35)
    l.masa(forma([(30, 41.6), (36, 26), (48, 19.6), (62, 18.4), (76, 21), (86, 28), (90, 41.6)], 2), material='cuerpo', alto=.3, brillo=.06, vientre=0,
           hondo=0, linea=.4, escalon=.2, contraluz=.3)
    f = piedra_gris(l, [box(50, 13.6, 70, 19.6), box(50, 11.6, 54, 13.8), box(66, 11.6, 70, 13.8)], .35)
    for x in np.arange(55, 66, 2):
        l.mancha(box(x, 13, x + 1, 13.8), CIELO, 1)
    l.mancha(forma([(58.6, 19.6), (58.6, 16.6), (60, 15.4), (61.4, 16.6), (61.4, 19.6)], 1), '164F46', .85, dentro=f)
    for x, y in ((96, 33), (104, 31)):
        lancha(l, x, y, .9)
    # la pajilla dorada, protagonista, de las que se doblan: entra al lago, pasa por encima del fuerte y echa el agua en el río
    eje = [(18, 38), (18, 14), (24, 6.4), (40, 4), (76, 4.6), (94, 7.4), (100, 14), (100, 22)]
    paja = tubo(eje, [1.5] * len(eje), 10)
    m = l.masa(paja, material='acento', alto=.55, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    c = curva(eje, 10)
    largo = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(c, axis=0).T))])
    for k, d in enumerate(np.arange(2, largo[-1], 3.2)):                 # las rayas en espiral, y el codo de acordeón, de rayas juntas
        i = int(np.searchsorted(largo, d))
        p0, p1 = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        t = (p1 - p0) / (np.hypot(*(p1 - p0)) or 1)
        nrm = np.array([-t[1], t[0]])
        a, b = c[i] + nrm * 1.6 + t * .8, c[i] - nrm * 1.6 - t * .8
        l.trazo([tuple(a), tuple(b)], .5, color='FBEFCB', alfa=.7, dentro=m)
    for d in np.arange(26, 36, 1.1):
        i = int(np.searchsorted(largo, d))
        p0, p1 = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        t = (p1 - p0) / (np.hypot(*(p1 - p0)) or 1)
        nrm = np.array([-t[1], t[0]])
        l.trazo([tuple(c[i] + nrm * 1.6), tuple(c[i] - nrm * 1.6)], .16, color='6B4E10', alfa=.7, dentro=m)
    l.mancha(ovalo(18, 38, 4, 1), 'FFFFFF', .7, difuso=.4)                # el remolino donde chupa
    for k in range(4):                                                   # el chorro que sale
        l.trazo([(99 + k * .7, 23.4), (99.6 + k * .7, 28), (99 + k * .7, 31)], .5, color='9BDDBD', alfa=.9)
    l.mancha(ovalo(100.4, 31, 4, 1.2), 'FFFFFF', .8, difuso=.4)


# ------------------------------------------------------------------------------------------------ Sábalos
def sabalo(l, x, y, s=1.0, giro=-28):
    """el sábalo real, de plata, saltando en arco: el cuerpo largo y alto, las escamas grandes, la boca hacia arriba, el ojo grande, y
    las aletas y la cola horquillada doradas; una aleta de pecho levantada, que saluda"""
    G = lambda g: affinity.rotate(g, giro, origin=(x, y))
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, y + v * s, rx * s, ry * s, a)
    aletas = [Polygon(P([(-13, 0), (-19, -6), (-17, 0), (-19, 6)])), Polygon(P([(-2, -4.4), (-6, -8.4), (-4.6, -4)])), Polygon(P([(-4, 4), (-8, 7.4), (-6.4, 3.8)])),
              forma(P([(3, 1.6), (4, 6), (6.4, 7.4), (5.6, 2.4)]), 1)]
    l.masa([G(g) for g in aletas], material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.35)
    cuerpo = G(forma(P([(-14, 0), (-8, -4.6), (0, -5.6), (8, -4.4), (13, -1.6), (14.6, .2), (13, 1.6), (8, 3.6), (0, 4.8), (-8, 4), (-14, 0)]), 2))
    c = l.masa(cuerpo, material='claro', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.mancha(G(Polygon(P([(-14, -6), (15, -6), (15, -1.6), (-14, -1.6)]))), '8EB5AA', .45, dentro=c)
    for k in range(6):                                                   # las escamas grandes
        for j in range(3):
            l.trazo([(px, py) for px, py in [tuple(G(Polygon(P([(-9 + k * 3.4 + j * .4, -3 + j * 2.6), (-8 + k * 3.4 + j * .4, -2 + j * 2.6),
                                                                   (-9 + k * 3.4 + j * .4, -1 + j * 2.6)]))).exterior.coords)[i] for i in range(3)]],
                    .1, color='6E7E7B', alfa=.6, dentro=c)
    l.masa(G(O(10, -1, 1.5, 1.5)), material='claro', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.25)
    l.mancha(G(O(10.2, -1, .8, .8)), '05201C', 1)
    l.trazo([tuple(c_) for c_ in G(Polygon(P([(13.4, 1), (11, 1.6), (12, 2.6)]))).exterior.coords][:3], .2, color='3A2A0A', alfa=.8)
    l.masa(G(forma(P([(5.4, -3), (7.6, -9.4), (9.6, -10), (8.6, -6), (6.6, -2.4)]), 1)), material='acento', alto=.4, brillo=.5, vientre=0, hondo=0,
           linea=.35)                                                    # la aleta que saluda


def sabalos(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 102, 3.6, 10, .4)
    selva(l, -2, 122, 21, 9, semilla=5, emergentes=4)
    agua(l, box(-2, 21, 122, 41.6), ondas=14, semilla=6, linea=0)
    # el bote del pescador, con la caña doblada y el sedal, y el sábalo de plata, protagonista, que salta por encima y saluda
    madera(l, [forma([(44, 31.4), (46, 32.8), (74, 32.8), (78, 30.6), (76, 34.6), (70, 35.6), (48, 35.6), (45, 34.6)], 2)], .55, linea=.4)
    piel(l, [ovalo(52, 26.8, 1.2, 1.3)])
    l.masa(forma([(50.4, 32.6), (50.2, 28.4), (53.8, 28.4), (53.6, 32.6)], 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.masa([ovalo(52, 25.6, 2.6, .6), forma([(50.8, 25.6), (51, 24), (53, 24), (53.2, 25.6)], 1)], material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.25)
    l.trazo([(54, 29), (60, 22), (66, 20), (70, 20.6)], .25, color='3A2A0A', alfa=.9)    # la caña, doblada
    l.trazo([(70, 20.6), (74, 15)], .08, color='3A2A0A', alfa=.7)                       # el sedal
    sabalo(l, 62, 13, 1.25, giro=-22)
    for x, y in ((34, 30), (38, 27), (88, 29), (92, 26), (86, 24)):      # las gotas del salto
        l.mancha(ovalo(x, y, .5, .8), 'D2F2DA', .95)
    for x in (36, 88):
        l.mancha(ovalo(x, 33, 5, 1), 'FFFFFF', .7, difuso=.4)


# ------------------------------------------------------------------------------------------------ El Castillo
def rafaela(l, x, base, s=1.0):
    """Rafaela, de frente, de pie en la muralla: el vestido dorado, largo, el pelo recogido, y el brazo con la mecha encendida que
    toca el cañón"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    vestido = [forma(P([(-2.6, -15.4), (2.6, -15.4), (3, -11.6), (5.4, 0), (-5.4, 0), (-3, -11.6)]), 2),
               tubo(P([(2.4, -14.6), (5.4, -12.4), (8.4, -11.6)]), [.9 * s, .8 * s, .7 * s], 5), tubo(P([(-2.4, -14.6), (-4, -11.6), (-2.6, -9.6)]), [.9 * s, .8 * s, .7 * s], 5)]
    m = l.masa(vestido, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    for u in (-2.4, 0, 2.4):
        l.trazo(P([(u * .5, -10), (u, -.6)]), [.05, .16, .05], color='6B4E10', alfa=.45, dentro=m)
    l.mancha(Polygon(P([(-3, -11.8), (3, -11.8), (3, -11), (-3, -11)])), '6B4E10', .5, dentro=m)
    piel(l, [O(8.8, -11.6, .8, .8), O(-2.4, -9.4, .8, .8), O(0, -17.6, 2, 2.3), box(x - .6 * s, base - 16 * s, x + .6 * s, base - 15 * s)])
    l.masa([forma(P([(-2.2, -17.8), (-2, -19.8), (0, -20.4), (2, -19.8), (2.2, -17.8), (1.4, -18.8), (-1.4, -18.8)]), 1), O(0, -20.8, 1.2, 1)],
           material='oscuro', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.25)                # el pelo con su moño
    for dx in (-.7, .7):
        l.mancha(O(dx, -17.8, .22, .26), '05201C', 1)
    l.trazo(P([(-.6, -16.4), (0, -16.1), (.6, -16.4)]), .14 * s, color='3A2A0A', alfa=.85)
    l.trazo(P([(8.8, -11.6), (11.6, -9)]), .3 * s, color=MADERA, alfa=.95)                   # el botafuego
    l.mancha(O(11.8, -8.8, .5, .6), 'FBEFCB', .95)


def el_castillo(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 100, 4, 12, .45)
    # la selva y el cerro, la fortaleza de piedra arriba y el raudal abajo
    selva(l, -2, 122, 22, 8, semilla=8, emergentes=3)
    l.masa(forma([(-2, 41.6), (-2, 20), (10, 16), (30, 13.4), (56, 14), (74, 18), (84, 26), (88, 41.6)], 2), material='cuerpo', alto=.3, brillo=.06,
           vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.3)
    piedra_gris(l, [box(4, 6, 50, 17), box(10, 2.6, 22, 6.2), box(4, 4.4, 8, 6.2), box(46, 4.4, 50, 6.2)], .45)
    for x in np.arange(10.4, 22, 2.2):
        l.mancha(box(x, 2.6, x + 1.1, 3.4), CIELO, 1)
    for x in (26, 34, 42):
        l.mancha(box(x, 9, x + 1.6, 12), '164F46', .8)
    agua(l, forma([(84, 41.6), (82, 30), (90, 24), (122, 23), (122, 41.6)], 2), ondas=4, semilla=9, linea=.35)
    for _ in range(30):                                                  # el raudal
        x, y = rng.uniform(86, 120), rng.uniform(25, 40)
        l.trazo([(x, y), (x + 2, y - .5), (x + 4, y)], .5, color='FFFFFF', alfa=.75)
    for x, y in ((94, 31), (104, 28), (112, 35)):
        l.masa(ovalo(x, y, 2.6, 1.1), material='lejos', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.3)
    # la muralla de adelante, el cañón que dispara al río, y Rafaela, de vestido dorado, protagonista
    piedra_gris(l, [box(24, 27, 82, 41.6), box(24, 24.6, 30, 27.2), box(36, 24.6, 42, 27.2), box(76, 24.6, 82, 27.2)], .5)
    for y in (31, 35, 39):
        l.trazo([(24, y), (82, y)], .12, color='3A2A0A', alfa=.35)
    l.masa([forma([(60, 26.4), (61, 23.4), (78, 21.2), (79, 23.4), (64, 27)], 1), ovalo(60.6, 25, 2.2, 2.2)], material='oscuro', alto=.4, brillo=.4, vientre=0,
           hondo=0, linea=.3)                                            # el cañón
    madera(l, [box(56, 26, 66, 27.4), ovalo(58.4, 27.4, 1.6, 1.6), ovalo(64, 27.4, 1.6, 1.6)], .6)
    for k in range(5):                                                   # el fogonazo y el humo
        l.mancha(ovalo(84 + k * 3.4, 20.4 - k * 1.4, 2 + k * .8, 1.6 + k * .5), 'FFFFFF', .85 - k * .1, difuso=.5)
    l.mancha(ovalo(81, 21.6, 2, 1.4), 'FBEFCB', .95)
    l.masa(ovalo(104, 13, 1.2, 1.2), material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.2)     # la bala
    for k in range(3):
        l.trazo([(100 - k * 3, 13.8 + k * .8), (102 - k * 3, 13.4 + k * .8)], .2, color='0C3A33', alfa=.5)
    rafaela(l, 47, 27, 1.15)


# ------------------------------------------------------------------------------------------------ Boca San Carlos
def boca_san_carlos(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # enfrente, la selva de Nicaragua y el San Juan, ancho; el río San Carlos llega desde acá, de Costa Rica
    selva(l, -2, 122, 17, 7, semilla=10, emergentes=3)
    agua(l, box(-2, 17, 122, 26), ondas=8, semilla=11, linea=0)
    prado(l, 26, 41.6, .3)
    for x, w, h in ((8, 6, 3.6), (15, 5.6, 3.2), (22, 6.4, 3.8)):
        c = l.masa(box(x, 31 - h, x + w, 31), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.masa(Polygon([(x - .4, 31 - h), (x + w / 2, 31 - h - 1.8), (x + w + .4, 31 - h)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0,
               linea=.25)
    agua(l, cinta([(124, 40), (104, 37.4), (86, 33.6), (72, 30), (64, 27.6)], [9, 8, 6.6, 5.2, 4.4], 10), ondas=6, semilla=12, linea=.35)
    # la boca dorada, protagonista, abierta, que se toma el río San Carlos de un trago
    labios = unary_union([forma([(34, 21), (40, 15.4), (46, 13.6), (50, 15), (54, 13.6), (60, 15.4), (66, 21), (60, 19.4), (50, 18.4), (40, 19.4)], 2),
                          forma([(34, 21), (40, 27.6), (50, 30.4), (60, 27.6), (66, 21), (60, 23.6), (50, 24.8), (40, 23.6)], 2)])
    adentro = forma([(35, 21), (40, 19.4), (50, 18.4), (60, 19.4), (65, 21), (60, 23.6), (50, 24.8), (40, 23.6)], 2)
    l.mancha(adentro, '3A1A12', 1)
    l.masa(forma([(41, 19.6), (50, 18.6), (59, 19.6), (58, 20.8), (50, 20.4), (42, 20.8)], 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.25)                                                    # los dientes de arriba
    l.mancha(forma([(43, 23.6), (50, 21.6), (57, 23.6), (50, 24.6)], 2), 'C86A6A', .9)                    # la lengua
    agua(l, cinta([(64, 27.6), (60, 25), (56, 22.6), (52, 21.6)], [4.4, 3.6, 2.8, 2], 6), linea=0)        # el río que entra en la boca
    m = l.masa(labios, material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.trazo([(42, 16.4), (46, 15.2), (49, 16)], [.05, .3, .05], color='FBEFCB', alfa=.9, dentro=m)
    l.trazo([(42, 27.4), (50, 29.2), (56, 28.6)], [.05, .35, .05], color='FBEFCB', alfa=.8, dentro=m)
    for k in range(3):                                                   # el trago: «glu»
        l.trazo([(70 + k * 2.4, 12 - k * 1.8), (71.4 + k * 2.4, 11 - k * 1.8), (72.8 + k * 2.4, 12 - k * 1.8)], .3, color='0C3A33', alfa=.7)


# ------------------------------------------------------------------------------------------------ Delta
def delta(l):
    rng = np.random.default_rng(13)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    # la selva y el pantano, y el río que se parte: el San Juan, flaco, hacia la izquierda, y el Colorado, ancho, hacia acá
    selva(l, -2, 122, 18, 7, semilla=14, emergentes=3)
    prado(l, 18, 41.6, .3)
    for _ in range(40):
        x, y = rng.uniform(0, 120), rng.uniform(20, 41)
        l.trazo([(x - .6, y), (x, y - 1.6), (x + .6, y)], .14, color='2F8A74', alfa=.7)
    agua(l, unary_union([cinta([(80, 17.4), (70, 21), (62, 24)], [4, 5, 6], 6), cinta([(62, 24), (40, 26), (20, 27), (-2, 26.6)], [3.4, 2.4, 1.8, 1.6], 8),
                         cinta([(62, 24), (74, 30), (88, 35), (104, 39), (124, 41)], [7, 9, 11, 13, 15], 8)]), ondas=10, semilla=15, linea=.35)
    # la Δ dorada, protagonista, partida en dos por el cuchillo
    izq = Polygon([(36, 33), (55, 4.6), (57.4, 8.6), (46.6, 33)])
    der = Polygon([(51, 33), (59.4, 12), (63, 5.2), (82, 33)])
    hueco_izq = Polygon([(44.6, 28.4), (55.6, 12), (56.8, 14), (48.6, 28.4)])
    hueco_der = Polygon([(54.6, 28.4), (60.2, 16.6), (61.4, 14.6), (73.4, 28.4)])
    for g, h in ((izq, hueco_izq), (der, hueco_der)):
        m = l.masa(g.difference(h), material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.45, contraluz=.35)
    l.mancha(ovalo(59, 34.2, 22, 1.4), '0C3A33', .25, difuso=.6)
    # el cuchillo, clavado entre las dos mitades
    hoja = Polygon([(55.6, 0), (58.4, -.6), (60.6, 24), (57.6, 30), (57.4, 24)])
    hm = l.masa(hoja, material='claro', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.35)
    l.mancha(hoja.buffer(1), '8EB5AA', .4, dentro=hm)
    l.trazo([(56.6, 1), (58.4, 23)], [.05, .25, .05], color='FFFFFF', alfa=.85, dentro=hm)


# ------------------------------------------------------------------------------------------------ San Juan de Nicaragua
def pala(l, x, base, s=1.0, giro=12):
    """una pala dorada clavada en la tierra, un poco inclinada: el mango largo con su agarradera y la hoja enterrada a medias"""
    G = lambda g: affinity.rotate(g, giro, origin=(x, base))
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    g = [box(x - .55 * s, base - 22 * s, x + .55 * s, base - 3 * s), forma(P([(-3.4, -3.4), (3.4, -3.4), (3.6, 1.6), (0, 3.4), (-3.6, 1.6)]), 1),
         tubo(P([(-2.2, -24.6), (0, -25.4), (2.2, -24.6)]), [.5 * s] * 3, 4), tubo(P([(-2, -24.6), (-.6, -22)]), [.45 * s, .45 * s], 2),
         tubo(P([(2, -24.6), (.6, -22)]), [.45 * s, .45 * s], 2)]
    m = l.masa([G(p) for p in g], material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([tuple(c) for c in G(Polygon(P([(-.2, -21), (-.2, -4), (.2, -4)]))).exterior.coords][:2], [.05, .25], color='FBEFCB', alfa=.85, dentro=m)
    return m


def greytown(l):
    rng = np.random.default_rng(16)
    l.mancha(box(0, 0, 120, 40), 'C9D2D0', 1)                            # el cielo gris
    for x, y, w in ((20, 5, 18), (60, 4, 22), (100, 5.4, 18)):
        for dx, dy, r in ((-.3, .2, .28), (0, -.1, .34), (.3, .15, .26)):
            l.mancha(ovalo(x + dx * w, y + dy * w * .4, r * w * .7, r * w * .45), '9AA6A3', .8, difuso=.6)
    for _ in range(20):                                                  # la llovizna
        x, y = rng.uniform(0, 120), rng.uniform(8, 18)
        l.trazo([(x, y), (x - .6, y + 2)], .1, color='8A9A97', alfa=.6)
    # el pueblo gris, a la izquierda, sobre sus pilotes, y los manglares a la derecha
    prado(l, 20, 41.6, .2)
    l.mancha(box(-2, 20, 122, 41.6), GRIS, .3)
    for x, w, h in ((-1, 7, 5.6), (7, 6.4, 4.6), (14.6, 7.4, 5.8), (23, 6, 4.4)):
        c = l.masa(box(x, 24 - h, x + w, 24), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
        l.mancha(box(x - 1, 24 - h - 2, x + w + 1, 24), GRIS, .55, dentro=c)
        l.mancha(box(x + w * .4, 24 - h * .6, x + w * .6, 24), '3A4A47', .8, dentro=c)
        t = l.masa(Polygon([(x - .5, 24 - h), (x + w / 2, 24 - h - 2), (x + w + .5, 24 - h)]), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.mancha(Polygon([(x - 1, 24 - h + .2), (x + w / 2, 24 - h - 2.4), (x + w + 1, 24 - h + .2)]), '5E6A68', .7, dentro=t)
        for u in (x + .6, x + w - .6):
            l.trazo([(u, 24), (u, 27.4)], .3, color='3A4A47', alfa=.9)
    for x in (98, 108, 117):
        mangle(l, x, 31, 13, semilla=x)
    # la zanja del canal que nunca se terminó: el agua quieta que se acaba en el montón de tierra, y la pala dorada, protagonista
    zanja = Polygon([(-2, 31), (66, 29.6), (66, 34.4), (-2, 37.6)])
    agua(l, zanja, ondas=4, semilla=17, linea=.35)
    monton = forma([(60, 36), (64, 29), (70, 26.4), (80, 26.8), (86, 31), (88, 36.4)], 2)
    t = l.masa(monton, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.4)
    l.mancha(monton.buffer(1), '8A6A3A', .55, dentro=t)
    for _ in range(14):
        x, y = rng.uniform(64, 84), rng.uniform(28, 35)
        l.mancha(ovalo(x, y, .5, .35), '5A3E1E', .5, dentro=t)
    lancha(l, 30, 34, .9)
    pala(l, 76, 30.4, 1.08, giro=10)


# ------------------------------------------------------------------------------------------------ el mar
def vapor(l, x, y, s=1.0):
    """el vapor del Tránsito, la barca del juego, mirando a la derecha: el casco bajo y chato, dorado; la cubierta con su toldo de lona
    de borde festoneado sobre postes, la timonera chica encima, la chimenea alta y fina adelante, los baúles y la rueda de paletas a
    popa; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, r: ovalo(x + u * s, y + v * s, r * s, r * s)
    rueda = l.masa(O(-15.4, -3.4, 4.2), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    for k in range(10):
        a = math.radians(k * 36)
        l.trazo([(x + (-15.4 + 1 * math.cos(a)) * s, y + (-3.4 + 1 * math.sin(a)) * s), (x + (-15.4 + 4.2 * math.cos(a)) * s, y + (-3.4 + 4.2 * math.sin(a)) * s)],
                .22 * s, color='0C3A33', alfa=.9, dentro=rueda)
    for u in np.arange(-10, 11, 4):                                      # los postes del toldo
        l.trazo(P([(u, -2), (u, -8.4)]), .25 * s, color='3A2A0A', alfa=.9)
    for u, w in ((-6, 3), (-1.6, 2.6), (3, 3.2)):                        # los baúles
        madera(l, [forma(P([(u - w / 2, -2), (u - w / 2, -4.4), (u + w / 2, -4.4), (u + w / 2, -2)]), 1)], .65, linea=.25)
    toldo = forma(P([(-11.6, -8), (-11, -9.6), (11, -9.6), (11.6, -8), (10, -7.6), (8.4, -8), (6.6, -7.6), (5, -8), (3.2, -7.6), (1.6, -8), (0, -7.6), (-1.6, -8),
                     (-3.2, -7.6), (-5, -8), (-6.6, -7.6), (-8.4, -8), (-10, -7.6)]), 1)
    l.masa(toldo, material='claro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.masa(box(x - 3.4 * s, y - 13 * s, x + 1.4 * s, y - 9.4 * s), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)       # la timonera
    l.mancha(box(x - 2.6 * s, y - 12.2 * s, x + .6 * s, y - 10.8 * s), '164F46', .8)
    l.masa([box(x + 7 * s, y - 20 * s, x + 8.2 * s, y - 9.4 * s), forma(P([(6.2, -20.6), (7, -20), (8.2, -20), (9, -20.6), (8.6, -21.6), (6.6, -21.6)]), 1)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)       # la chimenea
    for k in range(4):
        l.mancha(ovalo(x + (6 - k * 2.6) * s, y + (-23 - k * 1.2) * s, (1.3 + k * .5) * s, (1 + k * .3) * s), 'FFFFFF', .8 - k * .15, difuso=.4)
    casco = forma(P([(-14.6, -2.4), (-14, .6), (13, .6), (16, -2.6), (13, -1.8), (-11, -1.8)]), 1)
    c = l.masa(casco, material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-13.6, -.8), (0, -.4), (14, -1.2)]), [.05, .12, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco.union(toldo)


def mar(l):
    rng = np.random.default_rng(18)
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .5)
    nube(l, 90, 4, 12, .45)
    horizonte = 19
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(30, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # los manglares de la bahía, a la izquierda, y el faro en su punta, a la derecha
    orilla(l, forma([(-2, 41.6), (-2, 22), (14, 23), (24, 28), (28, 41.6)], 2), tinte=.3)
    for x, y, h in ((4, 26, 11), (14, 29, 12), (6, 38.6, 13), (22, 37, 11)):
        mangle(l, x, y, h, semilla=x)
    orilla(l, forma([(96, horizonte + .6), (104, horizonte - 1.2), (122, horizonte - 1.4), (122, horizonte + .6)], 1), tinte=.4, linea=.25)
    f = l.masa(forma([(107.6, horizonte - .8), (108.2, 8.6), (110.2, 8.6), (110.8, horizonte - .8)], 0), material='claro', alto=.3, brillo=.2, vientre=0,
               hondo=0, linea=.3)
    l.mancha(box(106, 12.4, 112, 13.8), '2F8A74', .85, dentro=f)
    l.masa(Polygon([(107.6, 8.8), (109.2, 6.8), (110.8, 8.8)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # la aleta de Tiburcio, el tiburón toro, que va y viene
    l.masa(Polygon([(86, 33.4), (89.4, 28.6), (90.4, 33.4)]), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.trazo([(82, 33.8), (86, 33.4), (92, 33.6), (95, 34.2)], .2, color='FFFFFF', alfa=.6)
    # el vapor del Tránsito, la barca del juego, protagonista, que sale al Caribe
    g = vapor(l, 58, 33, 1.3)
    reflejo(l, g, 33.4, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='San Carlos', dibujar=san_carlos), dict(clave='Sábalos', dibujar=sabalos),
            dict(clave='El Castillo', dibujar=el_castillo), dict(clave='Boca San Carlos', dibujar=boca_san_carlos), dict(clave='Delta', dibujar=delta),
            dict(clave='San Juan de Nicaragua', dibujar=greytown), dict(clave='mar', dibujar=mar)]
LISTO = True
