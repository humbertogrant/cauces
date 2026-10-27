# -*- coding: utf-8 -*-
"""Las postales del Yangtsé, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: en la meseta tibetana, bajo los montes Tanggula nevados, el río joven que en su tramo alto se llama Jinsha, «arenas
  doradas»: sus brazos trenzados sobre un ancho banco de arena dorada, con yaks;
- Chongqing: «una ciudad vertical entre niebla y ollas de hotpot»: los edificios que suben por el cerro entre bancos de niebla, las
  escaleras, el tren dorado que atraviesa un edificio y, a la orilla, una olla de hotpot que humea;
- Yichang: «el río choca contra un muro y hace ¡chan!»: el río que se estrella contra el muro de la presa de las Tres Gargantas, entre
  las paredes de la garganta, con la salpicadura y un estallido dorado, como en una historieta;
- Wuhan: «una W gigante de acero cruza el río»: el puente, con su viga de acero en W, dorada, sus pilas en el agua, sus torres en los
  extremos y el tren que pasa por adentro;
- Nankín: «la capital del sur, espejo de Pekín»: la puerta de la muralla Ming, con sus arcos y su torre de techo de tejas doradas, que se
  refleja en el río como en un espejo, y una rosa de los vientos que señala el sur;
- Shanghái: «la ciudad sobre el mar»: los rascacielos de Pudong, que salen del agua, con las esferas doradas de la Torre de la Perla
  Oriental;
- el mar: el junco se queda en el estuario y del Yangtsé al mar salen los portacontenedores; la protagonista sale del nombre del mar,
  «Oriental», donde sale el sol: el sol que nace, dorado, en el horizonte del mar de China Oriental, con su camino de luz en el agua
  (sin rayos en abanico, que dirían otra cosa); a la derecha, las grúas del puerto y un portacontenedores que sale; adelante, el junco,
  de madera.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, agua, ave, cielo, cinta, cordillera, nube, orilla, pasto, prado, reflejo, rio, tierra)  # noqa: F401
from pintor import forma, ovalo, tubo


# ------------------------------------------------------------------------------------------------ el nacimiento
def yak(l, x, base, s=1.0, lado=1, semilla=0):
    """un yak de la meseta, de perfil, mirando a la derecha (o a la izquierda con `lado` -1): la joroba, el pelo largo que le cuelga como
    una falda, la cabeza gacha y los cuernos que se curvan hacia arriba"""
    P = lambda pts: [(x + u * s * lado, base + v * s) for u, v in pts]
    patas = [tubo(P([(u, -2.6), (u, -.2)]), [.6 * s, .5 * s], 4) for u in (-3.6, -2.2, 2.4, 3.8)]
    cuerpo = forma(P([(-5, -4), (-5.4, -6.4), (-4, -8.4), (-1, -8.8), (1.6, -9.8), (3.6, -9.4), (5, -8), (5.6, -6), (5.4, -4.2), (3, -3.2),
                      (-3, -3.2)]), 2)
    falda = forma(P([(-5.2, -5), (5.6, -5), (5.4, -2.8), (4.2, -1.8), (2.8, -2.6), (1.2, -1.8), (-.4, -2.6), (-2, -1.8), (-3.6, -2.6),
                     (-5, -1.8)]), 1)
    cabeza = forma(P([(4.8, -7.4), (6.6, -7.6), (8.2, -6.6), (8.6, -5), (7.8, -4.2), (6.2, -4.6), (5, -5.6)]), 1)
    m = l.masa(patas + [cuerpo, falda, cabeza], material='oscuro', alto=.45, brillo=.25, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    l.pelaje(m, densidad=4, largo=1, ancho=.12, alfa=.4, semilla=semilla, claro=.4, flujo=95, mechon=2)
    l.masa([tubo(P([(6.2, -7.4), (5.4, -9), (6.4, -10.2)]), [.35 * s, .25 * s, .1 * s], 6),
            tubo(P([(7.2, -7.4), (8.2, -8.8), (7.6, -10.2)]), [.35 * s, .25 * s, .1 * s], 6)], material='claro', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.25)
    l.mancha(ovalo(x + 7 * s * lado, base - 6.2 * s, .22 * s, .22 * s), 'D2F2DA', 1, dentro=m)


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 24, 5, 14, .6)
    nube(l, 98, 4, 10, .45)
    cordillera(l, [(-2, 17), (10, 10.6), (20, 13.6), (32, 6.8), (44, 12), (56, 5.8), (68, 11.4), (80, 5.2), (92, 10.6), (104, 7.4), (116, 11.6),
                   (122, 9.6)], material='lejos', nieve=10.8)
    meseta = forma([(-2, 20.6), (20, 19.4), (40, 20.2), (60, 19.2), (80, 20.4), (100, 19.4), (122, 20.2), (122, 41.5), (-2, 41.5)], 2)
    m = l.masa(meseta, material='vientre', alto=.08, brillo=0, vientre=0, hondo=0, linea=.3, escalon=0, contraluz=.15)
    l.mancha(meseta, 'E8B952', .2, dentro=m)
    # el Jinsha, «arenas doradas»: el río joven, trenzado, sobre su banco de arena dorada, protagonista
    arena = forma([(54, 20.4), (66, 20.4), (80, 28), (98, 41.5), (22, 41.5), (40, 28)], 2)
    a = l.masa(arena, material='acento', alto=.12, brillo=.15, vientre=0, hondo=0, linea=.35, escalon=.1, contraluz=.25)
    for _ in range(180):                                                 # los granos de arena
        l.mancha(ovalo(rng.uniform(22, 98), rng.uniform(21, 41), .25, .18), str(rng.choice(['FBEFCB', 'BF9129'])), .7, dentro=a)
    canales = [cinta(pts, w, 8) for pts, w in (([(59, 20.6), (56.4, 24.4), (50.6, 28.6), (46, 34), (40, 41.5)], [.6, 1, 1.5, 2.1, 2.9]),
                                                ([(61, 20.6), (63, 24.6), (58.6, 28.8), (61, 34.4), (58.6, 41.5)], [.6, 1, 1.6, 2.3, 3.1]),
                                                ([(60.4, 21.4), (66, 25.6), (72.4, 30), (70.6, 35.2), (78, 41.5)], [.5, .9, 1.4, 2, 2.9]),
                                                ([(50.6, 28.6), (55, 30.6), (60, 31.6)], [1.2, 1.1, 1.2]),
                                                ([(61, 34.4), (66, 35.6), (70.6, 35.2)], [1.4, 1.2, 1.4]))]
    agua(l, unary_union(canales), ondas=4, semilla=2, linea=.25)
    pasto(l, 2, 24, 23, 40, 8, semilla=5)
    pasto(l, 96, 118, 23, 40, 8, semilla=6)
    yak(l, 14, 31, .95, 1, semilla=3)
    yak(l, 106, 35.6, 1.25, -1, semilla=4)


# ------------------------------------------------------------------------------------------------ Chongqing
def edificio(l, x0, x1, base, alto_, material='claro'):
    """un edificio alto: el bloque y su rejilla de ventanas"""
    e = l.masa(box(x0, base - alto_, x1, base).buffer(.08), material=material, alto=.25, brillo=.12, vientre=0, hondo=0, linea=.3)
    for yy in np.arange(base - alto_ + .9, base - .4, 1.1):
        l.trazo([(x0 + .4, yy), (x1 - .4, yy)], .1, color='8EB5AA', alfa=.85, dentro=e)
    for xx in np.arange(x0 + .9, x1 - .3, 1.2):
        l.trazo([(xx, base - alto_ + .4), (xx, base - .4)], .06, color='8EB5AA', alfa=.6, dentro=e)
    return e


def chongqing(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    # el cerro empinado, que sube de izquierda a derecha, cubierto de edificios en escalones: la ciudad vertical
    pend = lambda x: 36 - (x + 2) / 124 * 22
    cerro = Polygon([(-2, pend(-2))] + [(x, pend(x) + .6 * math.sin(x / 5)) for x in np.arange(0, 122.1, 4)] + [(122, 41.5), (-2, 41.5)])
    l.masa(cerro, material='lejos', alto=.2, brillo=.05, vientre=0, hondo=0, linea=.35)
    edificios = []
    for x in np.arange(118, -4, -4.6):                                  # la fila de arriba
        if 47 < x < 71:
            continue
        edificios.append((x, pend(x) + rng.uniform(1, 2.6), rng.uniform(8, 15), rng.uniform(3.4, 4.2)))
    for x, b, h, w in sorted(edificios, key=lambda e: e[1]):
        edificio(l, x - w / 2, x + w / 2, b, h, material=str(rng.choice(['claro', 'claro', 'vientre'])))
    # la niebla, en bancos entre los edificios de arriba
    for y, a in ((10.4, .7), (16.6, .5)):
        l.mancha(box(-2, y - 1.6, 122, y + 1.6), 'FFFFFF', a, difuso=1.4)
    for x in np.arange(116, -4, -5.4):                                  # la fila de abajo, más cerca
        if 47 < x < 71:
            continue
        b = pend(x) + rng.uniform(5.6, 7.4)
        edificio(l, x - 2, x + 2, b, rng.uniform(5, 9), material=str(rng.choice(['claro', 'vientre'])))
    # una escalera que sube por el cerro, entre los edificios
    pasos = []
    for k in range(9):
        x0, y0 = 30 + k * 1.6, pend(30) + 4.4 - k * 1.2
        pasos += [(x0, y0), (x0 + 1.6, y0)]
    l.trazo(pasos, .3, color='E2EDE9', alfa=.95)
    # la vía del tren, que entra al cerro por un túnel, y el edificio que el tren atraviesa
    l.masa([box(-2, 22, 86, 23.2)] + [box(x - .6, 23, x + .6, pend(x) + 2) for x in (8, 26, 42, 76)], material='vientre', alto=.2, brillo=.1,
           vientre=0, hondo=0, linea=.3)
    l.masa(forma([(84, 23.4), (84, 19.6), (86, 18), (88.6, 18), (90.6, 19.6), (90.6, 23.4)], 1), material='oscuro', alto=.1, brillo=0,
           vientre=0, hondo=0, linea=.35)                                # la boca del túnel
    torre = box(50, 5.6, 68, 34).difference(box(50, 17.8, 68, 22.8))
    e = l.masa(torre.buffer(.08), material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.3)
    for yy in [y for y in np.arange(6.6, 33.6, 1.2) if not 17.2 < y < 23.4]:
        l.trazo([(50.4, yy), (67.6, yy)], .12, color='8EB5AA', alfa=.85, dentro=e)
    for xx in np.arange(51.2, 68, 1.4):
        l.trazo([(xx, 6), (xx, 33.6)], .07, color='8EB5AA', alfa=.6, dentro=e)
    l.mancha(box(50, 17.8, 68, 22.8), '0C3A33', .55)                     # el hueco, en sombra
    l.masa(box(50, 22, 68, 23.2), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    # el tren, protagonista: dos coches dorados, uno adentro del edificio y otro que ya sale hacia el túnel
    coches = [forma([(x0, 21.8), (x0, 19), (x0 + .8, 18.2), (x0 + 12.4, 18.2), (x0 + 13.2, 19), (x0 + 13.2, 21.8)], 1) for x0 in (51.6, 66.2)]
    t = l.masa(coches, material='acento', alto=.35, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for x0 in (51.6, 66.2):
        l.mancha(box(x0 + 1, 19, x0 + 12.2, 20.2), '164F46', .9, dentro=t)
        for xv in np.arange(x0 + 3.6, x0 + 12, 2.6):
            l.trazo([(xv, 19), (xv, 20.2)], .14, color='E8B952', alfa=.9, dentro=t)
    l.masa(forma([(79.4, 21.8), (79.4, 19), (81, 19), (82.2, 20.6), (82.2, 21.8)], 1), material='acento', alto=.3, brillo=.35, vientre=0,
           hondo=0, linea=.35)                                           # la trompa del tren
    # el río, abajo, y la olla de hotpot que humea en la orilla, con su caldo partido en dos
    rio(l, 37.6)
    olla = ovalo(17, 36.6, 8, 2).union(box(9, 36.6, 25, 39.4)).union(ovalo(17, 39.4, 8, 1.8))
    l.masa(olla, material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.mancha(ovalo(17, 36.6, 7.1, 1.4), '6FA497', 1)
    l.mancha(ovalo(14.4, 36.6, 3.6, 1.1), '3E7A6D', 1)                   # un lado del caldo, más oscuro
    l.trazo([(10.2, 36.8), (14, 35.6), (17, 36.8), (20, 37.8), (23.8, 36.6)], .3, color='0C3A33', alfa=.9)
    for k, x0 in enumerate((12.6, 17, 21.4)):                            # el vapor, que sube hacia la niebla
        pts = [(x0 + .9 * math.sin(t * 1.3 + k), 34.6 - t * 1.6) for t in range(7)]
        l.trazo(pts, [.3, .6, .7, .7, .6, .4, .15], color='8BD0B9', alfa=.85)
        l.trazo(pts, [.1, .35, .45, .45, .4, .25, .05], color='FFFFFF', alfa=1)


# ------------------------------------------------------------------------------------------------ Yichang
def estallido(l, x, y, rx, ry, puntas=11, semilla=0):
    """el estallido de una historieta: una estrella de puntas desparejas, dorada, con el centro claro"""
    rng = np.random.default_rng(semilla)
    pts = []
    for k in range(puntas * 2):
        a = 2 * math.pi * k / (puntas * 2)
        r = rng.uniform(.95, 1.15) if k % 2 == 0 else rng.uniform(.5, .62)
        pts.append((x + rx * r * math.cos(a), y + ry * r * math.sin(a)))
    e = l.masa(Polygon(pts), material='acento', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.mancha(Polygon([(x + (px - x) * .5, y + (py - y) * .5) for px, py in pts]), 'FBEFCB', .9, dentro=e)
    return e


def yichang(l):
    cielo(l, sol=None)
    nube(l, 60, 4, 12, .45)
    # las paredes de la garganta, a los dos lados
    for pts in ([(-2, 41.5), (-2, 2), (6, 6), (10, 3.4), (16, 12), (20, 22), (26, 41.5)],
                [(122, 41.5), (122, 3), (114, 6.4), (110, 3.8), (104, 13), (100, 22), (94, 41.5)]):
        g = forma(pts, 2)
        m = l.masa(g, material='lejos', alto=.4, brillo=.1, vientre=0, hondo=.1, linea=.4, escalon=.25, contraluz=.35)
        for k in range(5):                                               # las vetas de la roca
            yy = 8 + k * 6
            l.trazo([(pts[0][0], yy), ((pts[0][0] + pts[-2][0]) / 2, yy + 1.4)], .12, color='164F46', alfa=.5, dentro=m)
    # el muro de la presa, de orilla a orilla de la garganta, con sus compuertas
    muro = Polygon([(14, 13), (106, 13), (104, 24), (16, 24)])
    p = l.masa(muro, material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.3)
    l.mancha(box(14, 13, 106, 14.4), 'CFE0DA', .9, dentro=p)
    for x in np.arange(22, 100, 5.4):                                    # las compuertas
        l.mancha(box(x, 16.4, x + 2.4, 20.4), '164F46', .85, dentro=p)
    for x in (30, 52, 74, 92):                                           # las grúas del coronamiento
        l.masa([box(x - .2, 9.4, x + .2, 13), box(x - 2, 9.2, x + 2, 9.8)], material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2)
    # el río, que viene hacia el muro y choca: «¡chan!»
    lecho = Polygon([(16, 24), (104, 24), (124, 41.5), (-4, 41.5)])
    agua(l, lecho, ondas=14, semilla=3, linea=0)
    for k in range(6):                                                   # la corriente que corre hacia el muro
        x0 = 36 + k * 9
        l.trazo([(x0 + (x0 - 60) * .5, 39), (x0 + (x0 - 60) * .25, 33), (x0, 27)], [.2, .4, .2], color='D2F2DA', alfa=.75)
    estallido(l, 60, 15.6, 16, 9.4, semilla=4)
    salpicadura = [ovalo(60 + dx, 22 + dy, rx, ry) for dx, dy, rx, ry in ((0, 0, 9, 2.4), (-5, -3, 3, 3.4), (5, -3.2, 3.2, 3.6), (0, -5.4, 3.6, 4),
                                                                         (-9, -1, 2.4, 2), (9, -1.4, 2.4, 2.2))]
    l.masa(salpicadura, material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for dx, dy, r in ((-13, -6, .7), (-10, -10, .6), (12.6, -7, .7), (9.6, -11, .55), (-4, -12.4, .6), (4, -13, .5)):
        l.masa(ovalo(60 + dx, 22 + dy, r, r * 1.2), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)


# ------------------------------------------------------------------------------------------------ Wuhan
def wuhan(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .5)
    nube(l, 92, 3.4, 10, .4)
    # enfrente, la ciudad, con sus rascacielos, y a la izquierda la Torre de la Grulla Amarilla sobre su cerro
    prado(l, 20, 25)
    for x in np.arange(30, 104, 5.6):
        h = rng.uniform(6, 13)
        edificio(l, x - 1.8, x + 1.8, 21.4, h, material=str(rng.choice(['claro', 'vientre'])))
    l.masa(forma([(-2, 21), (6, 16.6), (16, 15.4), (26, 18), (30, 21.4)], 2), material='cuerpo', alto=.3, brillo=.05, vientre=0, hondo=0,
           linea=.35)
    for k, (w, y0) in enumerate(((6.4, 15.6), (5.2, 12.8), (4, 10.2))):  # la torre, en pisos con aleros curvos
        l.masa(box(16 - w / 2 + .6, y0 - 2.6, 16 + w / 2 - .6, y0), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
        l.masa(forma([(16 - w / 2 - 1, y0 - 2.4), (16 - w / 2, y0 - 3), (16 + w / 2, y0 - 3), (16 + w / 2 + 1, y0 - 2.4), (16 + w / 2 - .6, y0 - 2.2),
                      (16 - w / 2 + .6, y0 - 2.2)], 1), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.trazo([(16, 7.2), (16, 5.6)], .16, alfa=.9)
    # el río ancho
    rio(l, 24.6)
    # el puente, protagonista: las pilas en el agua, la viga de acero en W, dorada, con el tren adentro, y las torres de los extremos
    sup, inf = 13.6, 19.8
    l.masa([box(x - 1.4, inf, x + 1.4, 27.4).buffer(.1) for x in np.arange(10, 120, 20)], material='vientre', alto=.3, brillo=.1, vientre=0,
           hondo=0, linea=.35)
    for x in np.arange(10, 120, 20):
        l.mancha(ovalo(x, 27.4, 3.2, .5), 'D2F2DA', .7)
    tren = l.masa([box(x0, inf - 2.6, x0 + 9.6, inf - .4).buffer(.1) for x0 in np.arange(24, 84, 10.4)], material='lejos', alto=.25, brillo=.2,
                  vientre=0, hondo=0, linea=.3)
    for x0 in np.arange(24, 84, 10.4):
        l.mancha(box(x0 + .8, inf - 2.2, x0 + 8.8, inf - 1.4), 'A4DCC4', .8, dentro=tren)
    barras = [box(-2, sup - .5, 122, sup + .5), box(-2, inf - .5, 122, inf + .5)]
    for x in np.arange(-2, 122, 8):                                      # la W: diagonales que bajan y suben
        barras.append(tubo([(x, sup), (x + 4, inf), (x + 8, sup)], [.42, .42, .42], 3))
    v = l.masa(barras, material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for x in np.arange(2, 122, 8):                                       # los remaches de los nudos
        l.mancha(ovalo(x, inf, .3, .3), '6B4E10', .9, dentro=v)
    l.masa([box(x0, sup - 1.6, x0 + 2.6, sup - .5).buffer(.08) for x0 in (34, 58, 82)], material='claro', alto=.2, brillo=.2, vientre=0,
           hondo=0, linea=.2)                                            # los autos de arriba
    for x in (4, 116):                                                   # las torres de los extremos, con sus aleros
        l.masa(box(x - 2.4, 6.8, x + 2.4, 24.4).buffer(.1), material='claro', alto=.3, brillo=.12, vientre=0, hondo=0, linea=.4)
        l.masa(forma([(x - 4, 7.4), (x - 2.6, 6.2), (x + 2.6, 6.2), (x + 4, 7.4), (x + 2.6, 7.6), (x - 2.6, 7.6)], 1), material='lejos', alto=.2,
               brillo=.15, vientre=0, hondo=0, linea=.3)


# ------------------------------------------------------------------------------------------------ Nankín
def puerta_ming(l, x, base, s=1.0):
    """la puerta de la muralla Ming de Nankín: el macizo de ladrillo con sus tres arcos y, arriba, la torre de dos pisos con sus techos
    de tejas doradas y los aleros curvos; da su silueta"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    macizo = Polygon(P([(-16, 0), (-15, -13), (15, -13), (16, 0)]))
    for u in (-9, 0, 9):
        macizo = macizo.difference(forma(P([(u - 2.4, 0.2), (u - 2.4, -5), (u - 1.4, -6.8), (u, -7.4), (u + 1.4, -6.8), (u + 2.4, -5), (u + 2.4, .2)]), 1))
    m = l.masa(macizo, material='lejos', alto=.3, brillo=.12, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.3)
    l.mancha(macizo, 'E8B952', .18, dentro=m)
    for v in np.arange(-12, 0, 1.2):                                     # las hiladas de ladrillo
        l.trazo(P([(-16, v), (16, v)]), .07, color='0C3A33', alfa=.35, dentro=m)
    for v0, w, h in ((-13, 11.4, 3.6), (-19.4, 7.6, 3)):                # los dos pisos de la torre, con sus techos dorados
        cuerpo = l.masa(Polygon(P([(-w + 1.4, v0), (w - 1.4, v0), (w - 1.4, v0 - h), (-w + 1.4, v0 - h)])), material='claro', alto=.25,
                        brillo=.1, vientre=0, hondo=0, linea=.35)
        for u in np.arange(-w + 2.6, w - 1.6, 2.4):
            l.trazo(P([(u, v0), (u, v0 - h)]), .3 * s, color='164F46', alfa=.85, dentro=cuerpo)
        techo = forma(P([(-w - 2.2, v0 - h + .2), (-w - 1, v0 - h - .6), (-w + 1.6, v0 - h - 1.4), (w - 1.6, v0 - h - 1.4), (w + 1, v0 - h - .6),
                         (w + 2.2, v0 - h + .2), (w, v0 - h - .2), (-w, v0 - h - .2)]), 1)
        if v0 < -15:
            techo = techo.union(Polygon(P([(-w + 1.6, v0 - h - 1.2), (-w + 3.4, v0 - h - 3.4), (w - 3.4, v0 - h - 3.4), (w - 1.6, v0 - h - 1.2)])))
        t = l.masa(techo, material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.35)
        for u in np.arange(-w, w, .9):                                   # las tejas
            l.trazo(P([(u, v0 - h - .2), (u + .3, v0 - h - 1.3)]), .06 * s, color='6B4E10', alfa=.5, dentro=t)
    return macizo.union(Polygon(P([(-13.6, -13), (13.6, -13), (11, -26), (-11, -26)])))


def rosa(l, x, y, r):
    """una rosa de los vientos: cuatro puntas largas y cuatro cortas, en un aro, con la del sur llena y más larga"""
    l.trazo([(x + r * .62 * math.cos(t), y + r * .62 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)], .16, alfa=.8)
    for k in range(8):
        a = math.radians(k * 45 - 90)
        largo = (1.25 if k == 4 else 1) if k % 2 == 0 else .55
        d = np.array([math.cos(a), math.sin(a)])
        n = np.array([-d[1], d[0]])
        c = np.array([x, y])
        pts = [tuple(c + d * r * largo), tuple(c + n * r * .16), tuple(c - n * r * .16)]
        l.masa(Polygon(pts), material='oscuro' if k == 4 else 'claro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.25)


def nankin(l):
    cielo(l, sol=None)
    nube(l, 92, 5, 12, .5)
    rosa(l, 15, 9, 5.4)
    # la muralla Ming de orilla a orilla, con la puerta al medio, protagonista
    agua_y = 21.4
    muro = [box(-2, 14.6, 122, agua_y)]
    for x in np.arange(-1.4, 122, 2.2):
        muro.append(box(x, 13.6, x + 1.1, 14.8))
    m = l.masa(unary_union(muro), material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.25)
    l.mancha(box(-2, 13, 122, agua_y), 'E8B952', .18, dentro=m)
    for y in np.arange(15.8, agua_y, 1.2):
        l.trazo([(-2, y), (122, y)], .06, color='0C3A33', alfa=.3, dentro=m)
    g = puerta_ming(l, 60, agua_y + .2, .76)
    # el río, y en él la puerta entera, de cabeza, como en un espejo: la capital del sur, espejo de la del norte
    rio(l, agua_y)
    espejo = affinity.scale(g, 1, -1, origin=(0, agua_y + .2))
    techos = affinity.scale(g.intersection(box(-2, -2, 122, agua_y - 9.6)), 1, -1, origin=(0, agua_y + .2))
    for k in np.arange(agua_y + .4, 41.5, .75):                           # el reflejo, en franjas, con el techo dorado abajo
        franja = box(-2, k, 122, k + .5)
        l.mancha(espejo.intersection(franja), '3E7A6D', .6)
        l.mancha(techos.intersection(franja), 'F2D48A', .7)
    for x in (6, 112):                                                   # los sauces de la orilla
        l.masa([ovalo(x + dx, 18.6 + dy, 2.4, 2) for dx, dy in ((0, 0), (-2, 1), (2, .8))], material='cuerpo', alto=.3, brillo=.1, vientre=0,
               hondo=0, linea=.3)


# ------------------------------------------------------------------------------------------------ Shanghái
def perla(l, x, base, s=1.0):
    """la Torre de la Perla Oriental: las patas, la esfera grande, las columnas, la esfera de arriba, la chica y la aguja; las esferas,
    doradas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, r: ovalo(x + u * s, base + v * s, r * s, r * s)
    l.masa([tubo(P([(u, 0), (u * .3, -8)]), [.6 * s, .5 * s], 4) for u in (-4, 0, 4)] +
           [tubo(P([(u, -10), (u, -24.6)]), [.5 * s, .5 * s], 4) for u in (-1.2, 1.2)] + [tubo(P([(0, -28), (0, -33.6)]), [.5 * s, .4 * s], 4)] +
           [tubo(P([(0, -34), (0, -40)]), [.25 * s, .1 * s], 4)], material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    esferas = [O(0, -11, 4.2), O(0, -26.4, 2.8), O(0, -34.6, 1.2)]
    e = l.masa(esferas, material='acento', alto=.6, brillo=.6, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for v, r in ((-11, 4.2), (-26.4, 2.8)):                              # las franjas de las esferas
        l.trazo(P([(-r * .95, v), (0, v + r * .2), (r * .95, v)]), .2 * s, color='6B4E10', alfa=.5, dentro=e)
    return unary_union(esferas)


def shanghai(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 24, 6, 14, .5)
    agua_y = 30
    # los rascacielos de Pudong, que salen del agua: la Torre de Jin Mao, la Torre de Shanghái, la del abridor y otros
    for x in (6, 12, 108, 114, 22, 98):
        edificio(l, x - 2.2, x + 2.2, agua_y, rng.uniform(8, 12), material='vientre')
    jm = [box(30 - 2.6 + k * .5, agua_y - 6 - k * 4, 30 + 2.6 - k * .5, agua_y - k * 4) for k in range(5)]
    j = l.masa(unary_union(jm + [Polygon([(29.2, agua_y - 26), (30, agua_y - 30), (30.8, agua_y - 26)])]), material='claro', alto=.3,
               brillo=.15, vientre=0, hondo=0, linea=.35)
    for k in range(5):
        l.trazo([(30 - 2.4 + k * .5, agua_y - 6 - k * 4 + .3), (30 + 2.4 - k * .5, agua_y - 6 - k * 4 + .3)], .2, color='164F46', alfa=.7, dentro=j)
    st = forma([(81, agua_y), (81.6, agua_y - 20), (83.2, agua_y - 31.6), (85, agua_y - 34), (86.4, agua_y - 31.6), (87.6, agua_y - 20),
                (88.2, agua_y)], 1)
    t = l.masa(st, material='claro', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for k in range(8):                                                   # la torre de Shanghái, que se tuerce
        y0 = agua_y - 2 - k * 4
        l.trazo([(81.4, y0), (84.6, y0 - 1.8), (88, y0 - 3.6)], .14, color='8EB5AA', alfa=.85, dentro=t)
    ab = box(91, agua_y - 30, 96.4, agua_y).difference(Polygon([(92, agua_y - 28.2), (95.4, agua_y - 28.2), (94.6, agua_y - 25.6), (92.8, agua_y - 25.6)]))
    a = l.masa(ab, material='claro', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.4)
    for y in np.arange(agua_y - 24, agua_y - .5, 1.4):
        l.trazo([(91.3, y), (96.1, y)], .08, color='8EB5AA', alfa=.8, dentro=a)
    g = perla(l, 60, agua_y, .98)
    for x, h in ((44, 10), (50, 7), (70, 8), (75, 11)):
        edificio(l, x - 2, x + 2, agua_y, h, material='claro')
    # el agua, abajo, con el reflejo de la ciudad y de las esferas doradas
    rio(l, agua_y)
    reflejo(l, box(4, agua_y - 12, 116, agua_y), agua_y + .2, .3)
    reflejo(l, g, agua_y + .2, .45, color='F2D48A')
    for x in (14, 104):                                                  # dos barcos chicos
        l.masa([forma([(x - 4, 34.2), (x + 4, 34.2), (x + 3, 35.6), (x - 3, 35.6)], 1), box(x - 1.4, 32.6, x + 1.6, 34.3)], material='lejos',
               alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)


# ------------------------------------------------------------------------------------------------ el mar
def junco(l, x, y, s=1.0, dorado=True):
    """el junco del Yangtsé, la barca del juego, mirando a la derecha: el casco de popa alta y proa cuadrada, dorado (de madera, sin
    `dorado`), y las velas de estera con sus listones de bambú, abiertas en abanico; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    palos = [tubo(P([(u, -2), (u, -top)]), [.3 * s, .22 * s], 4) for u, top in ((-7.6, 11.6), (0, 17.6), (7.4, 13.6))]
    l.masa(palos, material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    for u0, top, w in ((-7.6, 11.4, 5.6), (0, 17.2, 8), (7.4, 13.4, 6)):  # las velas de estera, de atrás hacia adelante
        vela = forma(P([(u0 - w * .7, -top + .4), (u0 + w * .25, -top - .6), (u0 + w * .35, -3.6), (u0 - w * .8, -3.2)]), 1)
        v = l.masa(vela, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.4, escalon=.15, contraluz=.3)
        for k in range(1, 6):                                            # los listones de bambú
            f = k / 6
            l.trazo(P([(u0 - w * (.7 + .1 * f), -top + .4 + (top - 3.6) * f), (u0 + w * (.25 + .1 * f), -top - .6 + (top - 3) * f)]), .16 * s,
                    color='3E7A6D', alfa=.9, dentro=v)
    casco = forma(P([(-12.6, -5.8), (-11.6, -1.4), (-7, .9), (8, .9), (11.4, -1.4), (12, -3.6), (9, -2.6), (-6, -2.2), (-9.8, -4.4)]), 1)
    c = l.masa(casco, material='acento' if dorado else 'vientre', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    if not dorado:
        l.mancha(casco.buffer(.3), 'A2683A', .6, dentro=c)
    for v_ in (-1.2, -.2):
        l.trazo(P([(-11, v_ - 1.6), (-4, v_), (8, v_), (11, v_ - 1.4)]), [.05, .12, .12, .05], color='6B4E10', alfa=.6, dentro=c)
    l.mancha(ovalo(x + 10.2 * s, y - 2.4 * s, .45 * s, .45 * s), '05201C', .9, dentro=c)            # el ojo de la proa
    return casco


def mar(l):
    cielo(l, sol=None)
    nube(l, 32, 7, 16, .55)
    nube(l, 80, 5, 12, .45)
    horizonte = 23.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0,
               contraluz=0, arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2.6), '64C8AA', .55, dentro=m, difuso=.8)
    rng = np.random.default_rng(9)
    for _ in range(22):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        if abs(x + 3 - 62) > 8:
            l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # el sol que nace en el mar, dorado, protagonista: medio disco sobre el horizonte, con su resplandor y su camino de luz en el agua
    l.mancha(ovalo(62, horizonte, 17, 11), 'FBEFCB', .5, difuso=2.4)
    sol = ovalo(62, horizonte + .2, 9.6, 9.6).intersection(box(40, 0, 84, horizonte + .2))
    l.masa(sol, material='acento', alto=.35, brillo=.5, vientre=0, hondo=0, linea=.45, escalon=.1, contraluz=.35, arroja=False)
    for k, y in enumerate(np.arange(horizonte + 1, 40, 1.3)):          # el camino de luz, que se angosta y se rompe hacia nosotros
        w = 8.4 - k * .25
        for dx in ((-w * .5, w * .35) if k % 2 else (-w * .15,)):
            l.trazo([(62 + dx - w * .3, y), (62 + dx + w * .3, y)], .4 - k * .008, color='E8B952', alfa=.85 - k * .025)
    # el puerto de contenedores, a la derecha: el muelle, las grúas y un barco cargado
    l.masa(box(84, horizonte - 1.4, 122, horizonte + .8), material='vientre', alto=.15, brillo=.05, vientre=0, hondo=0, linea=.3)
    for x in (90, 100, 110):                                             # las grúas
        l.masa([box(x - .3, 10, x + .3, horizonte - 1.2), box(x + 3, 12, x + 3.6, horizonte - 1.2), box(x - 4, 9.6, x + 8, 10.6),
                Polygon([(x, 10), (x + 1.4, 7.4), (x + 2.8, 10)])], material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    cont = l.masa([forma([(86, horizonte + .4), (112, horizonte + .4), (113.4, horizonte - 1.4), (86.6, horizonte - 1.2)], 0)] +
                  [box(88 + k * 3, horizonte - 3.4 - (k % 2) * 1, 90.8 + k * 3, horizonte - 1.2) for k in range(7)], material='claro', alto=.2,
                  brillo=.15, vientre=0, hondo=0, linea=.25)
    for k in range(7):
        l.mancha(box(88 + k * 3, horizonte - 3.4 - (k % 2), 90.8 + k * 3, horizonte - 1.2), str(['4AA189', '3E7A6D', 'A4DCC4'][k % 3]), .8,
                 dentro=cont)
    # un portacontenedores que sale al mar, a la izquierda del sol
    sale = l.masa([forma([(20, horizonte + .4), (40, horizonte + .4), (41.4, horizonte - 1.4), (20.6, horizonte - 1.2)], 0),
                   box(21, horizonte - 4.2, 23.6, horizonte - 1.2)] + [box(25 + k * 2.4, horizonte - 2.8 - (k % 2) * .8, 27.2 + k * 2.4, horizonte - 1.2)
                                                                         for k in range(6)], material='claro', alto=.2, brillo=.15, vientre=0,
                  hondo=0, linea=.25)
    for k in range(6):
        l.mancha(box(25 + k * 2.4, horizonte - 2.8 - (k % 2) * .8, 27.2 + k * 2.4, horizonte - 1.2), str(['4AA189', '3E7A6D', 'A4DCC4'][k % 3]),
                 .8, dentro=sale)
    l.mancha(box(19, horizonte - .4, 42, horizonte + .6), '164F46', .6, dentro=sale)
    for x, yv, sv in ((28, 8, .9), (34, 6.4, .7)):
        ave(l, x, yv, sv)
    # el junco, de madera, que se queda en el estuario, adelante a la izquierda
    g = junco(l, 22, 37, 1.05, dorado=False)
    reflejo(l, g, 37.2, .2)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Chongqing', dibujar=chongqing), dict(clave='Yichang', dibujar=yichang),
            dict(clave='Wuhan', dibujar=wuhan), dict(clave='Nankín', dibujar=nankin), dict(clave='Shanghái', dibujar=shanghai),
            dict(clave='mar', dibujar=mar)]
LISTO = True
