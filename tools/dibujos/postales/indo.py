# -*- coding: utf-8 -*-
"""Las postales del Indo, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: el Kailash, el monte sagrado, dorado, con sus franjas de roca y su grieta de nieve en la cara, reflejado en el lago
  Manasarovar; los peregrinos que lo rodean y el río joven que sale;
- Leh: «un hilo verde en un desierto de altura»: la franja de álamos a lo largo del río, entre montañas ocres, es un hilo verde que
  una aguja dorada va cosiendo; arriba, el palacio de Leh y las estupas blancas;
- Skardu: «una K de K2»: una K dorada, enorme, como una puerta, delante de la pirámide nevada del K2;
- Attock: «un puente de barcas y un fuerte mogol»: el puente de barcas, dorado, que cruza el río donde entra el Kabul, con un jinete
  que lo pasa; en el cerro, el fuerte de Akbar;
- Sukkur: «sesenta y seis compuertas reparten el río como una regadera»: una regadera dorada que riega los campos de Sind, delante de
  la presa de muchos arcos;
- Hyderabad: «ventiladores de viento en los techos»: los techos de la ciudad llenos de torres de viento, doradas, que miran al río y
  atrapan la brisa;
- Karachi: «veinte millones en la boca de un río que ya casi no llega»: el río, seco, termina en una llave de agua dorada que apenas
  gotea; detrás, la ciudad enorme;
- el mar: el mar Arábigo, con los números arábigos, dorados, que flotan: 1, 2, 3; las dunas, los manglares del delta y un barco (la
  barca se queda en el delta: al mar casi no llega ni el agua).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, piedra,  # noqa: F401
                     prado, reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
OCRE = 'BF9129'            # las montañas peladas del desierto de altura


def piel(l, piezas, tono=.5):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def montes_ocres(l, puntos, tono=.5, material='vientre', nieve=None):
    """una cordillera pelada, ocre, de desierto de altura"""
    m = cordillera(l, puntos, material=material, nieve=nieve)
    l.mancha(Polygon([(puntos[0][0], 41)] + puntos + [(puntos[-1][0], 41)]).buffer(0), OCRE, tono, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 20, 5, 12, .5)
    nube(l, 102, 4, 12, .45)
    cordillera(l, [(-2, 17), (8, 11), (18, 13.4), (28, 9.6), (38, 14.6)], nieve=12)
    cordillera(l, [(82, 14.6), (92, 10), (102, 12.6), (112, 9), (122, 13)], nieve=11.6)
    # el Kailash, dorado: la cúpula en pirámide, con sus franjas de roca y la grieta de nieve que baja por la cara
    k = forma([(38, 20), (46, 13), (52, 6.6), (56, 3), (60, 1.8), (64, 3), (68, 6.6), (74, 13), (82, 20)], 2)
    m = l.masa(k, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, escalon=.3, contraluz=.4)
    l.mancha(forma([(55, 3.6), (58, 2), (62, 2), (65, 3.6), (62.6, 4.4), (60, 3.6), (57.4, 4.4)], 1), 'FBEFCB', .9, dentro=m)   # la nieve de la cumbre
    for y in (6.4, 9.6, 12.8, 16):                                       # las franjas de roca, en gradas
        w = 3.6 + (y - 1.8) * 1.15
        l.trazo([(60 - w, y + .3), (60 - w * .4, y - .1), (60 + w * .3, y + .2), (60 + w, y - .1)], .3, color='6B4E10', alfa=.5, dentro=m)
    rng_k = np.random.default_rng(5)
    for _ in range(9):                                                   # las vetas de nieve que bajan por la cara, desparejas
        x0, y0 = rng_k.uniform(52, 68), rng_k.uniform(4.6, 12)
        largo = rng_k.uniform(2.4, 5)
        l.trazo([(x0, y0), (x0 + rng_k.uniform(-.6, .6), y0 + largo * .5), (x0 + rng_k.uniform(-.8, .8), y0 + largo)], [.5, .35, .1], color='FBEFCB',
                alfa=.85, dentro=m)
    # el lago Manasarovar, con el monte reflejado, y la orilla con los peregrinos que dan la vuelta
    prado(l, 19.6, 41, .36)
    lago = forma([(14, 20.4), (106, 20.4), (110, 25), (98, 30.4), (60, 32), (22, 30.4), (10, 25)], 2)
    agua(l, lago, ondas=6, semilla=2, linea=.35)
    reflejo(l, k, 20.4, .45, 'F2D48A')
    agua(l, cinta([(62, 31.6), (58.6, 35), (62, 38.4), (59, 41.6)], [2, 3, 4, 5], 6), linea=.3)       # el río que sale
    for k_ in range(14):
        a = math.radians(200 + k_ * 10.5)
        x, y = 60 + 54 * math.cos(a), 30.6 - 10 * math.sin(a) + 4.4
        if y < 31 or y > 40:
            continue
        l.masa([ovalo(x, y - 2.4, .6, .7), forma([(x - .8, y), (x - .9, y - 1.8), (x + .9, y - 1.8), (x + .8, y)], 1)], material='claro' if k_ % 2 else 'lejos',
               alto=.2, brillo=.15, vientre=0, hondo=0, linea=.2)


# ------------------------------------------------------------------------------------------------ Leh
def leh(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # las montañas ocres del desierto de altura, con nieve arriba, y el palacio de Leh en su cerro, con las estupas
    montes_ocres(l, [(-2, 14), (10, 6.6), (22, 9), (34, 5), (46, 9.4), (58, 12)], .55, nieve=7.6)
    montes_ocres(l, [(56, 12), (70, 7), (84, 9.4), (98, 4.6), (110, 8.4), (122, 6)], .55, nieve=7)
    montes_ocres(l, [(-2, 24), (14, 17), (30, 14.4), (44, 18), (60, 22)], .45)
    p = l.masa([box(18, 9.4, 30, 15), box(20, 7.6, 28, 9.6), box(22.4, 6, 25.6, 7.8)], material='claro', alto=.25, brillo=.15, vientre=0, hondo=0,
               linea=.3)
    l.mancha(box(16, 5, 32, 16), OCRE, .3, dentro=p)
    for y in (11, 13):
        for x in np.arange(19.4, 29, 1.8):
            l.mancha(box(x, y, x + .8, y + 1), '164F46', .75, dentro=p)
    for x in (36, 40, 44):
        l.masa([box(x - 1, 16.6, x + 1, 18), ovalo(x, 16.2, 1.1, .9), Polygon([(x - .3, 15.6), (x, 13.6), (x + .3, 15.6)])], material='claro', alto=.3,
               brillo=.2, vientre=0, hondo=0, linea=.25)
    tierra(l, 22, 41, desierto=.5)
    # el río y el hilo verde de álamos a lo largo, que la aguja dorada va cosiendo
    hilo = [(-2, 33), (14, 31.4), (30, 32.6), (46, 30.4), (62, 31.4), (76, 29.6)]
    agua(l, cinta(hilo, [3, 3.2, 3.4, 3.6, 3.8, 4], 8), ondas=4, semilla=4, linea=.3)
    c = curva(hilo, 10)
    for k in range(0, len(c), 2):                                        # los álamos, finos y altos, en fila a lo largo del río
        x, y = c[k]
        for dy in (-2.6, 2.6):
            l.masa([ovalo(x + rng.uniform(-.4, .4), y + dy - 3.4, .9, 3), box(x - .15, y + dy - 1, x + .15, y + dy)], material='cuerpo', alto=.3,
                   brillo=.2, vientre=0, hondo=0, linea=.22, arroja=False)
    l.trazo([(76, 29.6), (80, 28.6), (82, 28)], .6, color='2F8A74', alfa=.95)                     # el hilo que va a la aguja
    aguja = Polygon([(80.4, 30.4), (82, 28.6), (113, 13.4), (115.6, 13.6), (116, 16.4), (82.6, 31.2)]).buffer(.4)
    ojo = ovalo(112.4, 15.4, 2.2, .75, -26)
    m = l.masa(aguja.difference(ojo), material='acento', alto=.5, brillo=.6, vientre=0, hondo=0, linea=.45, contraluz=.45)
    l.trazo([(82, 28), (96, 21.4), (106, 17.4), (112.4, 15.4), (116.6, 16.6), (118, 21), (116, 25.6)], .55, color='2F8A74', alfa=.95)
    l.trazo([(84, 29.6), (108, 18)], [.05, .3, .05], color='FBEFCB', alfa=.85, dentro=m)


# ------------------------------------------------------------------------------------------------ Skardu
def letra_k(x, y, h):
    """la letra K, de palo grueso, con su pie izquierdo en (x, y)"""
    g = .26 * h
    w = .7 * h
    return unary_union([box(x, y - h, x + g, y), Polygon([(x + g * .8, y - h * .44), (x + w - g * .2, y - h), (x + w + g * .9, y - h),
                                                          (x + g * 1.6, y - h * .38)]),
                        Polygon([(x + g * 1.2, y - h * .56), (x + w + g * .9, y), (x + w - g * .2, y), (x + g * .8, y - h * .44)])])


def skardu(l):
    cielo(l, sol=None)
    nube(l, 18, 4, 12, .45)
    nube(l, 104, 3.4, 10, .4)
    # el Karakórum: las montañas altísimas, y al fondo, en el medio, la pirámide nevada del K2
    cordillera(l, [(-2, 18), (10, 9), (22, 12.6), (34, 7), (44, 13), (52, 18)], nieve=11)
    cordillera(l, [(68, 18), (78, 12), (90, 6.6), (102, 11), (112, 7.6), (122, 12)], nieve=10)
    cordillera(l, [(36, 22), (48, 12), (56, 4), (60, 1.6), (65, 5), (72, 12.6), (84, 22)], nieve=12.6)
    montes_ocres(l, [(-2, 24), (16, 19), (32, 22.4), (40, 26)], .45)
    montes_ocres(l, [(80, 26), (92, 21), (108, 19), (122, 23)], .45)
    tierra(l, 24.6, 41, desierto=.45)
    agua(l, cinta([(-2, 32), (30, 33.4), (60, 34), (90, 33.4), (124, 32)], [5, 6, 6.6, 6, 5], 8), ondas=8, semilla=5, linea=.3)
    # la K dorada, protagonista, enorme como una puerta, delante del K2
    k = letra_k(47, 33.4, 26)
    l.mancha(affinity.translate(k, 1.2, 1), '0C3A33', .3, difuso=.6)
    m = l.masa(k.buffer(.3), material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([(48.2, 32.6), (48.2, 8.6)], [.06, .3, .06], color='FBEFCB', alfa=.8, dentro=m)
    reflejo(l, k, 33.6, .25)


# ------------------------------------------------------------------------------------------------ Attock
def attock(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.6, 10, .4)
    # el cerro del fuerte, a la derecha, con sus murallas mogolas, y los cerros pelados
    montes_ocres(l, [(-2, 20), (12, 12), (26, 14.6), (40, 18), (52, 20)], .4)
    cerro = forma([(62, 22), (74, 12), (90, 9.6), (110, 10.4), (122, 13), (122, 22)], 2)
    l.masa(cerro, material='vientre', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(cerro, OCRE, .45)
    muro = [Polygon([(70, 17), (76, 10.6), (118, 9.6), (122, 12.6), (122, 17)])]
    for x in (78, 90, 102, 114):
        muro.append(ovalo(x, 10.6, 2.4, 2))
        muro.append(box(x - 2.4, 10.6, x + 2.4, 15))
    f = piedra(l, muro, .6, .45)
    l.mancha(unary_union(muro).buffer(1), '8A6A3A', .3, dentro=f)
    for x in np.arange(77, 121, 1.6):                                    # las almenas de la muralla
        l.mancha(box(x, 10, x + .8, 11), CIELO, 1, dentro=f)
    for x in (78, 90, 102, 114):
        for dx in (-1.6, -.4, .8):
            l.mancha(box(x + dx, 8.4, x + dx + .7, 9.4), CIELO, 1, dentro=f)
        l.mancha(box(x - .4, 12, x + .4, 13.6), '164F46', .75, dentro=f)
    l.mancha(forma([(94.6, 17), (94.6, 13.6), (96, 12.4), (97.4, 13.6), (97.4, 17)], 1), '164F46', .85, dentro=f)
    tierra(l, 21, 41, desierto=.4)
    # el Indo, ancho, y el Kabul, que entra por la izquierda, de otro color
    a = agua(l, unary_union([box(-2, 24, 122, 36), cinta([(-2, 21.4), (14, 23), (26, 26)], [4, 5, 6], 6)]).buffer(.3).buffer(-.3), ondas=12, semilla=6,
             linea=.35)
    l.mancha(cinta([(-2, 21.4), (14, 23), (26, 26), (40, 28)], [4, 5, 6, 4], 6), 'C6B98A', .45, dentro=a, difuso=1)
    # el puente de barcas, protagonista, dorado: las barcas en fila con el tablero encima, y un jinete que lo cruza
    barcas = [forma([(x - 2.6, 30.4), (x + 2.6, 30.4), (x + 2, 32.6), (x - 2, 32.6)], 1) for x in np.arange(12, 112, 6)]
    l.masa(barcas, material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.35, contraluz=.3)
    tablero = box(4, 28.6, 116, 30.6)
    t = l.masa(tablero, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for x in np.arange(5, 116, 1.4):
        l.trazo([(x, 28.8), (x, 30.4)], .1, color='6B4E10', alfa=.5, dentro=t)
    for x in np.arange(6, 116, 3):                                       # la baranda
        l.trazo([(x, 28.8), (x, 26.6)], .14, color='6B4E10', alfa=.7)
    l.trazo([(4, 26.6), (116, 26.6)], .16, color='6B4E10', alfa=.7)
    reflejo(l, unary_union(barcas + [tablero]), 32.6, .25, 'F2D48A')
    # un jinete que cruza: los conquistadores pasaron todos por aquí
    x, b = 66, 28.6
    l.masa([ovalo(x, b - 4.6, 3.4, 1.8), tubo([(x - 2.6, b - 5), (x - 4.4, b - 7.4), (x - 5.6, b - 8)], [1.2, 1, .8], 5),
            forma([(x - 5.2, b - 8.8), (x - 7.4, b - 7.2), (x - 7, b - 6.4), (x - 5, b - 7)], 1)] +
           [tubo([(x + u, b - 4), (x + u + d, b - 2), (x + u, b)], [.6, .45, .4], 4) for u, d in ((-2.4, -.6), (-1.4, .4), (1.6, -.4), (2.6, .5))],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    l.masa([forma([(x - .8, b - 6), (x - 1, b - 9.6), (x + 1, b - 9.6), (x + .8, b - 6)], 1), ovalo(x, b - 10.6, .9, 1),
            Polygon([(x - .7, b - 11.2), (x, b - 13), (x + .7, b - 11.2)])], material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.25)
    l.trazo([(x + 1, b - 9), (x + 2.6, b - 14)], .2, color='0C3A33', alfa=.9)                      # la lanza


# ------------------------------------------------------------------------------------------------ Sukkur
def regadera(l, x, y, s=1.0):
    """una regadera dorada, inclinada, con su asa, el pico largo y la flor llena de agujeros que reparte el chorro"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    cuerpo = forma(P([(-7, 3.6), (-7.6, -4), (-6, -6), (5, -6), (6.6, -4), (6, 3.6), (4, 5.4), (-5, 5.4)]), 1)
    asa = tubo(P([(-5.6, -5.8), (-4, -10.4), (2.4, -10.4), (4.4, -5.8)]), [.9 * s] * 4, 8)
    pico = tubo(P([(5.6, 1.6), (12, -3.2), (16.6, -6.4)]), [1.4 * s, 1 * s, .8 * s], 4)
    flor = ovalo(x + 17.4 * s, y - 7 * s, 1.4 * s, 2.4 * s, 35)
    g = unary_union([cuerpo, asa, pico, flor])
    gg = affinity.rotate(g, 14, origin=(x, y))
    m = l.masa(gg, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([tuple(affinity.rotate(Polygon(P([(-6, -3), (-6, -2.9), (-5.9, -3)])), 14, origin=(x, y)).exterior.coords[0]),
             tuple(affinity.rotate(Polygon(P([(4, -3), (4, -2.9), (4.1, -3)])), 14, origin=(x, y)).exterior.coords[0])], .2, color='6B4E10', alfa=.6, dentro=m)
    fx, fy = affinity.rotate(flor, 14, origin=(x, y)).centroid.coords[0]
    return fx, fy


def sukkur(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .45)
    nube(l, 96, 3.6, 10, .4)
    # la presa de muchos arcos, que cruza el río al fondo, con sus compuertas
    prado(l, 14, 20, .24)
    agua(l, box(-2, 17.6, 122, 21.6), linea=0)
    p = piedra(l, box(-2, 12.6, 122, 18.4), .2, .35)
    for x in np.arange(-1, 122, 2.2):                                    # las compuertas, una al lado de la otra
        l.mancha(forma([(x, 18.4), (x, 15.4), (x + .9, 14.4), (x + 1.8, 15.4), (x + 1.8, 18.4)], 1), '0C3A33', .55, dentro=p)
        l.trazo([(x + .9, 18.4), (x + .9, 21)], .5, color='FFFFFF', alfa=.6)
    l.trazo([(-2, 13.4), (122, 13.4)], .2, color='6B4E10', alfa=.5, dentro=p)
    for x in (12, 108):
        palmera(l, x, 21.6, 8, 1 if x < 60 else -1, datiles=False)
    # los campos de Sind, verdes, con sus canales, adelante
    prado(l, 21.6, 41, .2)
    for k in range(6):
        y = 23.6 + k * 3
        l.trazo([(-2, y), (122, y + .4)], .5, color='64C8AA', alfa=.7)
    for _ in range(40):
        x, y = rng.uniform(0, 120), rng.uniform(23, 40)
        l.trazo([(x - .5, y), (x, y - .9), (x + .5, y)], .14, color='2F8A74', alfa=.6)
    # la regadera dorada, protagonista, que riega los campos con el río
    fx, fy = regadera(l, 50, 22, 1.25)
    rng = np.random.default_rng(9)
    for k in range(16):                                                  # el chorro, en gotitas que se abren
        a = math.radians(rng.uniform(10, 80))
        d = rng.uniform(3, 14)
        x, y = fx + d * math.cos(a), fy + d * math.sin(a) + d * d * .04
        l.mancha(ovalo(x, y, .35, .5), 'FFFFFF', .95)
        l.trazo([(fx + (d - 2) * math.cos(a), fy + (d - 2) * math.sin(a)), (x, y - .4)], .14, color='FFFFFF', alfa=.6)


# ------------------------------------------------------------------------------------------------ Hyderabad
def hyderabad(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .4)
    # el río, lejos, a la izquierda, de donde viene la brisa
    prado(l, 16, 20, .3)
    agua(l, forma([(-2, 16.4), (30, 16.4), (24, 20), (-2, 21)], 2), linea=.3)
    for k in range(4):                                                   # la brisa, que viene del río
        y = 6 + k * 3.2
        l.trazo([(2 + k * 3, y + 1), (14 + k * 3, y), (26 + k * 3, y + .6), (36 + k * 3, y - .2)], .3, color='FFFFFF', alfa=.85)
    # los techos de la ciudad, en filas que bajan hacia nosotros, cada uno con su torre de viento dorada que mira a la brisa
    fila = [(19, 36, 108, .62), (26, 22, 118, .8), (34, 8, 122, 1)]
    for base, x0, x1, s in fila:
        x = x0
        while x < x1:
            w, h = rng.uniform(7, 10) * s, rng.uniform(5, 7) * s
            c = l.masa(box(x, base - h, x + w, base + 6), material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.3)
            l.mancha(box(x - 1, base - h - 1, x + w + 1, base + 7), 'D8C49A', .35, dentro=c)
            for k in range(int(w // (2.6 * s))):
                l.mancha(box(x + (1 + k * 2.6) * s, base - h + 1.6 * s, x + (2.2 + k * 2.6) * s, base - h + 3.4 * s), '164F46', .7, dentro=c)
            tx = x + w * .55                                             # la torre de viento: la caja con la boca abierta hacia la brisa
            torre = Polygon([(tx - 1.4 * s, base - h), (tx - 1.4 * s, base - h - 4 * s), (tx + 1.6 * s, base - h - 5.4 * s), (tx + 1.6 * s, base - h)])
            m = l.masa(torre, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
            l.mancha(Polygon([(tx - 1.2 * s, base - h - 3.8 * s), (tx - 1.2 * s, base - h - 1.6 * s), (tx - .4 * s, base - h - 1.8 * s),
                              (tx - .4 * s, base - h - 4.2 * s)]), '6B4E10', .8, dentro=m)
            x += w + rng.uniform(.6, 2)


# ------------------------------------------------------------------------------------------------ Karachi
def karachi(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .45)
    # la ciudad enorme, detrás: los edificios altos, apretados, hasta los costados
    prado(l, 20, 24, .3)
    for x in np.arange(-1, 122, 4.2):
        h = rng.uniform(6, 16)
        e = l.masa(box(x, 21 - h, x + 3.8, 21.2), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.22, arroja=False)
        for y in np.arange(21 - h + .8, 21, 1.2):
            l.trazo([(x + .4, y), (x + 3.4, y)], .08, color='8EB5AA', alfa=.8, dentro=e)
    for x in (8, 112):                                                   # las grúas del puerto
        l.masa([box(x - .3, 8, x + .3, 21), Polygon([(x, 8), (x + 5, 7.2), (x + 5, 7.6), (x, 8.8)])], material='lejos', alto=.2, brillo=.1, vientre=0,
               hondo=0, linea=.2)
    # el cauce seco, de arena y grietas, que llega hasta la llave, y el mar detrás de todo, a los lados
    tierra(l, 21, 41, desierto=.5)
    cauce = forma([(40, 41.6), (46, 30), (52, 24), (68, 24), (74, 30), (80, 41.6)], 2)
    c = l.masa(cauce, material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.35)
    l.mancha(cauce, 'BF9129', .45, dentro=c)
    for _ in range(14):                                                  # las grietas del barro seco
        x, y = rng.uniform(46, 74), rng.uniform(27, 40)
        l.trazo([(x, y), (x + rng.uniform(-2, 2), y + rng.uniform(.6, 1.6)), (x + rng.uniform(-2, 2), y + rng.uniform(1.6, 2.6))], .14, color='6B4E10', alfa=.5,
                dentro=c)
    # la llave de agua dorada, protagonista, donde termina el río, que apenas gotea
    llave = [box(52, 22.4, 68, 26.6).buffer(.6), tubo([(62, 24.6), (66, 26), (67.4, 29.4), (67.4, 31.6)], [3.6, 3.4, 3, 3], 6),
             box(57.4, 18.4, 60.6, 22.6), ovalo(59, 17.6, 5, 1.4)]
    m = l.masa(llave, material='acento', alto=.5, brillo=.55, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([(53, 23.2), (66, 23.2)], [.06, .3, .06], color='FBEFCB', alfa=.85, dentro=m)
    l.masa(forma([(66.2, 33.4), (67.4, 31.6), (68.6, 33.4), (68.2, 34.6), (66.6, 34.6)], 2), material='claro', alto=.6, brillo=.6, vientre=0, hondo=0,
           linea=.3)                                                     # la gota
    l.mancha(ovalo(67.4, 39.6, 2.6, .6), '6BB9A0', .7)                    # el charquito


# ------------------------------------------------------------------------------------------------ el mar
def digito(ch, x, y, h):
    """un número arábigo, de trazo grueso, con su pie en (x, y) a la izquierda"""
    g = .2 * h
    w = .6 * h
    if ch == '1':
        return unary_union([box(x + w * .45, y - h, x + w * .45 + g, y), Polygon([(x + w * .45, y - h), (x + w * .45 + g, y - h), (x + w * .05, y - h * .66),
                                                                                (x - g * .1, y - h * .76)]), box(x + w * .15, y - g, x + w * .9, y)])
    if ch == '2':
        pts = [(x + w * .05, y - h * .74), (x + w * .3, y - h * .97), (x + w * .75, y - h * .95), (x + w * .95, y - h * .72), (x + w * .8, y - h * .45),
               (x + w * .3, y - h * .18), (x + w * .02, y - g * .5)]
        return unary_union([tubo(pts, [g] * 7, 6), box(x, y - g, x + w, y)])
    if ch == '3':
        g = .17 * h
        arriba = [(x + w * .1, y - h * .84), (x + w * .45, y - h * .99), (x + w * .88, y - h * .84), (x + w * .84, y - h * .6), (x + w * .5, y - h * .53)]
        abajo = [(x + w * .5, y - h * .53), (x + w * .95, y - h * .4), (x + w * .92, y - h * .12), (x + w * .5, y - g * .4), (x + w * .06, y - h * .14)]
        return unary_union([tubo(arriba, [g] * 5, 6), tubo(abajo, [g] * 5, 6)])
    raise ValueError(ch)


def mar(l):
    rng = np.random.default_rng(14)
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .5)
    nube(l, 98, 4, 12, .45)
    # el mar Arábigo, con un barco lejos; a la izquierda, las dunas de la costa; a la derecha, los manglares del delta
    horizonte = 17.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(20):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa([forma([(76, horizonte - .4), (98, horizonte - .4), (100, horizonte - 2), (75, horizonte - 2)], 1), box(78, horizonte - 4.4, 83, horizonte - 1.9)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    dunas = forma([(-2, 41.6), (-2, 22), (8, 19.6), (18, 22.6), (26, 26), (22, 34), (12, 41.6)], 2)
    orilla(l, dunas, tinte=.5)
    for y in (24, 28, 32):
        l.trazo([(0, y), (8, y - 1.4), (16, y)], .3, color='BF9129', alfa=.5)
    for x0, x1, y in ((96, 122, 28), (104, 122, 39)):
        for x in np.arange(x0 + 2, x1 - 1, 5.4):
            mangle(l, x + rng.uniform(-1, 1), y, rng.uniform(7, 9.4), semilla=int(x * 7))
    # los números arábigos, dorados, protagonistas, que flotan en el mar Arábigo
    for ch, x, y, h, giro in (('1', 34, 34.6, 15, -6), ('2', 52, 36.6, 16, 5), ('3', 74, 34.8, 15, -4)):
        g = affinity.rotate(digito(ch, x, y, h), giro, origin=(x + h * .3, y))
        l.mancha(ovalo(x + h * .3, y + .4, h * .45, 1), 'FFFFFF', .55, difuso=.4)
        l.masa(g.buffer(.2), material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
        reflejo(l, g, y + .4, .25, 'F2D48A')


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Leh', dibujar=leh), dict(clave='Skardu', dibujar=skardu),
            dict(clave='Attock', dibujar=attock), dict(clave='Sukkur', dibujar=sukkur), dict(clave='Hyderabad', dibujar=hyderabad),
            dict(clave='Karachi', dibujar=karachi), dict(clave='mar', dibujar=mar)]
LISTO = True
