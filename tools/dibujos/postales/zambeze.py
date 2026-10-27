# -*- coding: utf-8 -*-
"""Las postales del Zambeze, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el de Tete, que hace hervir la pava.

- el nacimiento: las colinas de Mwinilunga, con su bosque de miombo de copas chatas, y el claro donde nace el río: una gota dorada, la
  primera, sobre el manantial;
- Mongu: «un mono con corona rema en una llanura inundada»: el mono dorado, con su corona, rema en la barca real a rayas blancas y
  negras, con los remeros, sobre la llanura que el río inunda cada año;
- Katima Mulilo: «una gata mima a un mulito mientras apagan juntos un fuego con agua del río»: la gata dorada abraza al mulito, que
  echa el balde de agua sobre la fogata;
- Livingstone: «un león de piedra se moja la melena bajo una catarata que truena»: el león dorado, sentado en su roca al pie de las
  cataratas Victoria, con la melena mojada; la cortina de agua, el humo que truena y el puente;
- Kariba: «una caja enorme guarda el río entero»: la caja dorada, llena de agua, que es la presa con su lago, y los botes que rescatan
  a los animales de las islas;
- Tete: «una tetera hierve sola al sol sobre un puente colgante»: la pava dorada que hierve en el tablero del puente, bajo el sol
  pálido que calienta, con el carbón debajo de la tierra;
- Chinde: «un chinchorro colgado entre dos manglares mece a un capitán inglés con sombrero»: el chinchorro dorado y el capitán de
  blanco con su casco, que se mece; atrás, un vapor que sube el río;
- el mar: el delta, con sus manglares y sus palmeras, y un cartel con una mano dorada que apunta con el dedo índice al Índico, adonde
  van los barcos (el mokoro se queda entre los manglares).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, piedra, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '5A3E1E'
PIEL_CLARA = '93701A'


def piel(l, piezas, tono=.62, color=PIEL):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), color, tono, dentro=m)
    return m


def miombo(l, x, base, h, semilla=0, material='lejos'):
    """un árbol de miombo: el tronco y la copa ancha y chata, como una sombrilla"""
    rng = np.random.default_rng(semilla)
    l.masa(tubo([(x, base), (x + rng.uniform(-.6, .6), base - h * .7)], [h * .05, h * .035], 3), material='vientre', alto=.2, brillo=.1, vientre=0,
           hondo=0, linea=.22)
    l.masa([ovalo(x + dx * h, base - h * .78 + dy * h, h * .34, h * .12) for dx, dy in ((0, 0), (-.22, .05), (.22, .04))], material=material, alto=.3,
           brillo=.15, vientre=0, hondo=0, linea=.25)


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 24, 4.4, 12, .45)
    nube(l, 100, 4, 10, .4)
    # las colinas de Mwinilunga, suaves, cubiertas de miombo
    for pts, mat in (([(-2, 16), (20, 11), (44, 13), (66, 10), (90, 12.6), (122, 10)], 'lejos'), ([(-2, 20), (30, 16), (60, 18), (90, 15), (122, 18)], 'cuerpo')):
        l.masa(Polygon([(-2, 41)] + pts + [(122, 41)]), material=mat, alto=.3, brillo=.06, vientre=0, hondo=0, linea=.3)
        for x in np.arange(0, 122, 4.4):
            y = np.interp(x, [p[0] for p in pts], [p[1] for p in pts])
            miombo(l, x + rng.uniform(-1, 1), y + 1.6, rng.uniform(4, 6), semilla=int(x * 3), material='lejos' if mat == 'cuerpo' else 'oscuro')
    # el claro, el manantial y el río que empieza, angosto, y baja hacia nosotros
    prado(l, 22, 41, .3)
    for x, y, h in ((8, 32, 11), (20, 38, 13), (102, 33, 11), (114, 39, 13), (32, 27, 8), (90, 27, 8)):
        miombo(l, x, y, h, semilla=int(x))
    agua(l, ovalo(60, 27.4, 6, 1.8), ondas=2, semilla=2, linea=.3)
    agua(l, cinta([(61, 28.6), (58.6, 32), (62, 36), (59, 41.6)], [1.4, 2.2, 3.2, 4.4], 8), ondas=3, semilla=3, linea=.3)
    for k in range(3):
        l.trazo([(60 + (1.6 + k * 1.6) * math.cos(t), 27.4 + (.5 + k * .4) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 22)], .14, color='FFFFFF',
                alfa=.7)
    # la primera gota, dorada, protagonista, que cae al manantial
    gota = forma([(60, 6), (61.4, 9.6), (64.6, 15.6), (65.4, 19), (63.6, 22.6), (60, 23.8), (56.4, 22.6), (54.6, 19), (55.4, 15.6), (58.6, 9.6)], 2)
    l.mancha(ovalo(60, 27.2, 4, .8), 'F2D48A', .4, difuso=.6)
    g = l.masa(gota, material='acento', alto=.6, brillo=.6, vientre=0, hondo=0, linea=.45, contraluz=.45)
    l.trazo([(57.4, 15), (56.8, 19), (58.4, 21.6)], [.06, .5, .06], color='FBEFCB', alfa=.9, dentro=g)


# ------------------------------------------------------------------------------------------------ Mongu
def mono_rey(l, x, base, s=1.0):
    """un mono dorado, sentado, de perfil, mirando a la derecha, con su corona, que rema con un remo largo"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = [O(0, -4.6, 3.4, 4.2), O(1.4, -10.6, 2.6, 2.4), O(3.6, -10, 1.4, 1.1), O(-.4, -11.4, .9, .9),
              tubo(P([(1.6, -7), (4.4, -5.4), (6, -4)]), [.8 * s, .7 * s, .6 * s], 5), tubo(P([(-2.6, -2.6), (-6, -2.4), (-8, -5), (-6.4, -7)]), [.6 * s, .5 * s, .4 * s, .3 * s], 8)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.4)
    l.mancha(O(3.4, -10.2, 1.2, .9), 'FBEFCB', .7, dentro=c)
    l.mancha(O(2.6, -11.2, .3, .3), '05201C', 1)
    l.masa(forma(P([(-.6, -12.6), (-1, -15), (.2, -13.8), (1.2, -15.6), (2.2, -13.8), (3.4, -15), (3, -12.6)]), 0), material='acento', alto=.4,
           brillo=.6, vientre=0, hondo=0, linea=.3)                      # la corona
    l.trazo(P([(9, -12), (2, 3.6)]), .4 * s, color='5A3E1E', alfa=.95)    # el remo
    l.masa(O(1.2, 4.6, .8, 2, 25), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    return c


def mongu(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 12, .4)
    # la llanura del alto Zambeze, inundada hasta el horizonte, con matas de pasto que asoman y unos árboles en sus islotes
    agua(l, box(-2, 15, 122, 41.6), ondas=14, semilla=4, linea=0)
    for _ in range(30):
        x, y = rng.uniform(0, 120), rng.uniform(16, 40)
        l.trazo([(x - .6, y), (x, y - 1.2), (x + .6, y)], .16, color='2F8A74', alfa=.8)
    for x in (10, 30, 92, 112):
        l.masa(ovalo(x, 16.6, 5, .9), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        miombo(l, x, 16.4, 5, semilla=x)
    # la barca real, a rayas blancas y negras, con los remeros, y el mono rey dorado, protagonista, que rema adelante
    barca = forma([(22, 30), (96, 30), (102, 27.4), (98, 33.4), (92, 34.6), (26, 34.6), (20, 33), (16, 27.6)], 1)
    b = l.masa(barca, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)
    for x in np.arange(20, 102, 4):
        l.mancha(box(x, 26, x + 2, 35), '0C3A33', .9, dentro=b)
    for x in (30, 40, 50, 80, 90):                                       # los remeros
        piel(l, [ovalo(x, 25, 1.1, 1.2)])
        l.masa(forma([(x - 1.4, 30), (x - 1.5, 26.4), (x + 1.5, 26.4), (x + 1.4, 30)], 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
        l.trazo([(x + 2.4, 24), (x - 1.6, 34)], .3, color='5A3E1E', alfa=.9)
    l.masa([forma([(54, 30), (54, 22), (70, 22), (70, 30)], 0), forma([(52, 22.4), (62, 18.6), (72, 22.4)], 1)], material='claro', alto=.3, brillo=.2,
           vientre=0, hondo=0, linea=.35)                                # el toldo del rey
    mono_rey(l, 62, 28.6, 1.2)


# ------------------------------------------------------------------------------------------------ Katima Mulilo
def katima(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # el río ancho, atrás, con palmeras en la orilla
    prado(l, 14, 20, .26)
    rio(l, 19)
    for x, h, lado in ((8, 10, 1), (100, 12, -1), (112, 9, 1)):
        palmera(l, x, 20.4, h, lado, datiles=False)
    m = orilla(l, forma([(-2, 41.6), (-2, 25), (40, 24), (80, 24), (122, 25), (122, 41.6)], 2), tinte=.3)
    pasto(l, 0, 120, 27, 40.6, 14, semilla=5, dentro=m)
    # la fogata que apagan, con su humo blanco
    l.masa([tubo([(80, 37), (88, 35.6)], [.5, .5], 2), tubo([(80, 35.6), (88, 37)], [.5, .5], 2)], material='vientre', alto=.3, brillo=.1, vientre=0,
           hondo=0, linea=.25)
    l.mancha(ovalo(84, 34, 3, 2), 'FBEFCB', .6, difuso=.6)
    for k in range(5):
        l.mancha(ovalo(84 + k * 1.2, 30 - k * 3, 2 + k * .6, 1.6 + k * .4), 'FFFFFF', .8 - k * .12, difuso=.5)
    # el mulito gris que echa el balde de agua, y la gata dorada, protagonista, que lo mima
    x, b = 64, 38.6
    mula = [ovalo(x, b - 8, 6, 3.2), tubo([(x + 4.4, b - 9.4), (x + 7, b - 13), (x + 8.6, b - 14)], [1.6, 1.3, 1.1], 5), ovalo(x + 9.6, b - 13.4, 2.2, 1.6, -20),
            Polygon([(x + 7.6, b - 15), (x + 7, b - 19.4), (x + 8.8, b - 15.4)]), Polygon([(x + 8.6, b - 15), (x + 9, b - 19.6), (x + 9.8, b - 15.2)])]
    for u in (-4, -2, 2.4, 4.2):
        mula.append(tubo([(x + u, b - 6), (x + u, b)], [.8, .6], 3))
    mm = l.masa(mula, material='claro', alto=.45, brillo=.25, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.mancha(unary_union(mula).buffer(1), '6E7E7B', .5, dentro=mm)
    l.mancha(ovalo(x + 10, b - 14, .35, .35), '05201C', 1)
    l.masa([forma([(x + 12.6, b - 12.4), (x + 15.4, b - 11), (x + 14.6, b - 8.4), (x + 12.2, b - 9.4)], 1)], material='claro', alto=.3, brillo=.25,
           vientre=0, hondo=0, linea=.3)                                 # el balde, en la boca del mulito
    l.trazo([(x + 15, b - 9), (x + 17, b - 6), (x + 18.6, b - 4)], [.5, .6, .4], color='9BDDBD', alfa=.9)
    gata = [ovalo(x - 9, b - 6, 3.4, 4.6), ovalo(x - 8.4, b - 12.6, 2.6, 2.4), Polygon([(x - 10.6, b - 14), (x - 10.4, b - 16.6), (x - 9, b - 14.6)]),
            Polygon([(x - 7.8, b - 14.6), (x - 6.4, b - 16.6), (x - 6.2, b - 14)]),
            tubo([(x - 7, b - 9), (x - 4, b - 9.4), (x - 1.6, b - 8.6)], [.9, .8, .7], 5), tubo([(x - 11.6, b - 2.4), (x - 15, b - 4), (x - 14, b - 8)], [.6, .5, .4], 6)]
    g = l.masa(gata, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.4)
    for v in (-4, -6, -8):                                               # las rayas atigradas
        l.trazo([(x - 11.6, b + v), (x - 9.4, b + v - .4)], .3, color='6B4E10', alfa=.6, dentro=g)
    for dx in (-1, 1):
        l.mancha(ovalo(x - 8.4 + dx, b - 13, .3, .4), '05201C', 1)
    l.trazo([(x - 9.2, b - 11.6), (x - 8.4, b - 11.2), (x - 7.6, b - 11.6)], .16, color='0C3A33', alfa=.8)
    l.masa(ovalo(x - 4.6, b - 13.6, 1.2, 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)        # el corazón del mimo
    l.mancha(ovalo(x - 4.6, b - 13.6, 1, .8), 'E8A090', .7)


# ------------------------------------------------------------------------------------------------ Livingstone
def livingstone(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    # la cortina de agua de las cataratas Victoria, larga, y el humo que truena, que sube
    selva(l, -2, 122, 11, 4, semilla=8, emergentes=2)
    borde = box(-2, 11, 122, 13)
    l.masa(borde, material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(0, 122, 1.4):
        l.trazo([(x, 12.4), (x + .3, 20), (x - .2, 30)], [1, 1.2, .6], color='FFFFFF', alfa=.85)
    for k in range(9):
        l.mancha(ovalo(8 + k * 13, 8 - (k % 2) * 2.4, 6, 3.6), 'FFFFFF', .7, difuso=1)
    for x, y in ((24, 3), (70, 2.4), (100, 4)):                          # el trueno: rayitas
        l.trazo([(x, y), (x + 1.4, y + 1.4), (x, y + 2), (x + 1.6, y + 3.6)], .24, color='0C3A33', alfa=.6)
    # la garganta, abajo, con el agua revuelta, y el puente de arco a la derecha
    agua(l, box(-2, 29, 122, 41.6), ondas=12, semilla=9, linea=0)
    l.mancha(box(-2, 28, 122, 32), 'FFFFFF', .6, difuso=1.2)
    l.masa(cinta([(86 + 30 * t, 26 - 9 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 15)], [.9] * 15, 3), material='claro', alto=.2, brillo=.2,
           vientre=0, hondo=0, linea=.3)
    l.masa(box(84, 16.4, 122, 17.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    for t in np.linspace(.1, .9, 7):
        x = 86 + 30 * t
        l.trazo([(x, 26 - 9 * math.sin(math.pi * t)), (x, 17.4)], .14, color='8EB5AA', alfa=.9)
    # la roca y el león de piedra dorado, protagonista, sentado bajo el agua, con la melena mojada
    l.masa(forma([(36, 41.6), (38, 34), (50, 31.4), (70, 31.4), (82, 34), (84, 41.6)], 2), material='lejos', alto=.35, brillo=.1, vientre=0, hondo=0,
           linea=.4)
    x, b = 60, 31.6
    cuerpo = [forma([(x - 7, b), (x - 7.6, b - 6), (x - 4.4, b - 10), (x + 3, b - 10.4), (x + 6, b - 7), (x + 6.4, b)], 2),
              tubo([(x + 6, b - 1), (x + 10, b - 1.6), (x + 11.6, b - 4)], [.8, .6, .5], 5), ovalo(x + 12, b - 4.6, 1, .9)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    melena = [ovalo(x - 3.6 + 4.4 * math.cos(math.radians(a)), b - 13.4 + 4.6 * math.sin(math.radians(a)), 2.2, 2) for a in range(0, 360, 30)]
    l.masa(melena + [ovalo(x - 3.6, b - 13.4, 5.2, 5.6)], material='acento', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.45, contraluz=.35)
    l.masa([ovalo(x - 3.6, b - 13, 3.2, 3.4), ovalo(x - 3.6, b - 11, 2, 1.6)], material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4,
           contraluz=.4)
    for dx in (-1.2, 1.2):                                               # los ojos cerrados, contento bajo el agua
        l.trazo([(x - 3.6 + dx - .7, b - 14), (x - 3.6 + dx, b - 13.6), (x - 3.6 + dx + .7, b - 14)], .2, color='3A2A0A', alfa=.9)
    l.mancha(ovalo(x - 3.6, b - 11.6, .7, .5), '5A3E1E', .9)
    for k in range(10):                                                  # las gotas sobre la melena
        a = math.radians(200 + k * 14)
        l.mancha(ovalo(x - 3.6 + 7 * math.cos(a), b - 13.4 + 7 * math.sin(a), .35, .6), 'FFFFFF', .9)


# ------------------------------------------------------------------------------------------------ Kariba
def kariba(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # el río que llega desde atrás y el agua que subió, con las copas de los árboles ahogados y las islas
    prado(l, 14, 18, .26)
    agua(l, box(-2, 17, 122, 41.6), ondas=10, semilla=11, linea=0)
    for x in (10, 22, 100, 112):
        l.masa(ovalo(x, 22, 3, .8), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.trazo([(x - 1, 22), (x - 2, 19.4)], .2, color='5A3E1E', alfa=.8)
    # la caja dorada, protagonista: enorme, llena de agua, que guarda el río entero
    frente = Polygon([(36, 20), (84, 20), (84, 36), (36, 36)])
    tapa = Polygon([(36, 20), (44, 14), (92, 14), (84, 20)])
    lado = Polygon([(84, 20), (92, 14), (92, 30), (84, 36)])
    for g, br in ((lado, .2), (frente, .45)):
        m = l.masa(g, material='acento', alto=.3, brillo=br, vientre=0, hondo=0, linea=.45, contraluz=.35)
        for k in range(1, 4):                                            # las tablas de la caja
            y = 20 + k * 4
            l.trazo([(36, y), (84, y)] if g is frente else [(84, y), (92, y - 6)], .2, color='6B4E10', alfa=.55, dentro=m)
    agua(l, tapa, ondas=6, semilla=12, linea=.35)                         # el agua que la llena hasta el borde
    l.trazo([(36, 20), (84, 20)], .5, color='BF9129', alfa=.95)
    l.trazo([(84, 20), (92, 14)], .5, color='BF9129', alfa=.95)
    agua(l, cinta([(64, 4), (66, 9), (66, 14.4)], [1.4, 2.4, 3.4], 6), linea=.3)       # el río que entra a la caja
    # los botes que rescatan a los animales
    for x, y, animal in ((16, 33, 'antilope'), (104, 34, 'mono')):
        l.masa(forma([(x - 7, y - .6), (x + 7, y - .6), (x + 5.6, y + 1.2), (x - 5.6, y + 1.2)], 1), material='vientre', alto=.3, brillo=.2, vientre=0,
               hondo=0, linea=.3)
        if animal == 'antilope':
            l.masa([ovalo(x, y - 3, 3.4, 1.8), tubo([(x + 2.4, y - 3.6), (x + 3.6, y - 6.4)], [.7, .6], 3), ovalo(x + 4, y - 6.8, 1.2, .8),
                    tubo([(x + 3.6, y - 7.4), (x + 3, y - 10)], [.2, .1], 3), tubo([(x + 4.4, y - 7.4), (x + 4.6, y - 10)], [.2, .1], 3)] +
                   [tubo([(x + u, y - 2), (x + u, y - .6)], [.3, .25], 2) for u in (-2, 2)], material='vientre', alto=.4, brillo=.2, vientre=0, hondo=0,
                   linea=.3)
        else:
            l.masa([ovalo(x, y - 3, 2, 2.2), ovalo(x + .6, y - 6.6, 1.6, 1.5), tubo([(x - 1.6, y - 2), (x - 4, y - 3), (x - 4, y - 5.6)], [.3, .25, .2], 5)],
                   material='lejos', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.3)
        persona_x = x - 4
        piel(l, [ovalo(persona_x, y - 5.6, .9, 1)])
        l.masa(forma([(persona_x - 1.2, y - .6), (persona_x - 1.3, y - 4.4), (persona_x + 1.3, y - 4.4), (persona_x + 1.2, y - .6)], 1), material='claro',
               alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)


# ------------------------------------------------------------------------------------------------ Tete
def pava(l, x, base, s=1.0):
    """una pava dorada, de las de la cocina, que hierve sola: el cuerpo ancho, el asa arriba, el pico y el vapor que silba"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    g = unary_union([forma(P([(-5.6, 0), (-6.4, -3), (-5, -6.6), (-2.6, -8), (2.6, -8), (5, -6.6), (6.4, -3), (5.6, 0)]), 2),
                     tubo(P([(-3.4, -8), (-3, -11.6), (3, -11.6), (3.4, -8)]), [.6 * s] * 4, 8),
                     tubo(P([(5.4, -3), (8.4, -5.4), (10.6, -8.6)]), [1 * s, .8 * s, .6 * s], 5), ovalo(x, base - 8.4 * s, 1 * s, .6 * s)])
    l.mancha(ovalo(x + 1, base + .4, 7, .9), '0C3A33', .3, difuso=.4)
    m = l.masa(g, material='acento', alto=.55, brillo=.55, vientre=0, hondo=0, linea=.45, contraluz=.45)
    l.trazo(P([(-4.4, -2), (-4.6, -5)]), [.06, .45, .06], color='FBEFCB', alfa=.9, dentro=m)
    for k in range(4):                                                   # el vapor, que sale del pico
        l.mancha(ovalo(x + (11.6 + k * 1.6) * s, base + (-10 - k * 2) * s, (1.2 + k * .5) * s, (.9 + k * .3) * s), 'FFFFFF', .85 - k * .15, difuso=.4)
    for k in range(3):                                                   # las burbujas del hervor
        l.mancha(ovalo(x + (-2 + k * 2) * s, base - 9.4 * s, .5 * s, .5 * s), 'FFFFFF', .8)


def tete(l):
    rng = np.random.default_rng(13)
    cielo(l, sol=None, tarde=.3)
    # el sol pálido que calienta, con el aire que tiembla
    l.mancha(ovalo(96, 7, 9, 6), 'FBEFCB', .45, difuso=2)
    l.mancha(ovalo(96, 7.4, 3.2, 3.2), 'F2D48A', .6)
    for k in range(4):
        l.trazo([(80 + k * 4 + .5 * math.sin(t * 3), 14 - t * 4) for t in np.linspace(0, 1, 8)], .16, color='FFFFFF', alfa=.6)
    # las orillas, con el carbón por debajo, y el río
    prado(l, 20, 41, .34)
    rio(l, 24)
    for x0, x1 in ((-2, 34), (86, 122)):
        tierra_ = Polygon([(x0, 22), (x1, 22), (x1, 41.6), (x0, 41.6)])
        t = l.masa(tierra_, material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.35)
        l.mancha(tierra_, 'BF9129', .45, dentro=t)
        for _ in range(16):                                              # el carbón, abajo
            x, y = rng.uniform(x0 + 2, x1 - 2), rng.uniform(31, 40)
            l.masa(ovalo(x, y, rng.uniform(.8, 1.6), rng.uniform(.5, 1)), material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.2)
        l.trazo([(x0, 30), (x1, 30)], .2, color='6B4E10', alfa=.5, dentro=t)
    # el puente colgante, con sus torres y sus cables, y la pava dorada, protagonista, que hierve sola en el tablero
    for x in (24, 96):
        l.masa(box(x - 1, 8, x + 1, 24), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.trazo([(-2, 20), (24, 8.4), (60, 19), (96, 8.4), (122, 20)], .3, color='E2EDE9', alfa=.95)
    for x in np.arange(28, 94, 4):
        y = 8.4 + 10.6 * (1 - abs(x - 60) / 36) ** 1.6
        l.trazo([(x, y), (x, 21)], .1, color='8EB5AA', alfa=.9)
    l.masa(box(-2, 21, 122, 22.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    pava(l, 58, 21, 1.15)


# ------------------------------------------------------------------------------------------------ Chinde
def chinde(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # el brazo del delta, con un vapor que sube el río, atrás
    prado(l, 12, 16, .26)
    rio(l, 15.6)
    l.masa([forma([(78, 20.6), (100, 20.6), (102, 19), (77, 19)], 1), box(82, 15.4, 96, 19.2), box(88, 11, 89.6, 15.6), ovalo(86, 19, 2.4, 2.4)],
           material='vientre', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    for k in range(3):
        l.mancha(ovalo(88.8 - k * 2.2, 9.4 - k * 1.2, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .7 - k * .15, difuso=.4)
    # el banco de barro de adelante, donde están los dos manglares grandes
    banco = forma([(-2, 41.6), (-2, 30), (30, 28.6), (60, 28.2), (90, 28.6), (122, 30), (122, 41.6)], 2)
    b = l.masa(banco, material='vientre', alto=.1, brillo=.05, vientre=0, hondo=0, linea=.35)
    l.mancha(banco, '8A6A3A', .4, dentro=b)
    for x in (16, 104):
        mangle(l, x, 38.6, 30, semilla=x)
    # el chinchorro dorado, protagonista, colgado de los troncos, y el capitán inglés que se mece en él
    l.trazo([(17, 19), (31, 21.4)], .35, color='5A3E1E', alfa=.95)
    l.trazo([(103, 19), (89, 21.4)], .35, color='5A3E1E', alfa=.95)
    hamaca = forma([(31, 21.4), (44, 27.4), (60, 29.2), (76, 27.4), (89, 21.4), (76, 24.6), (60, 26.2), (44, 24.6)], 2)
    l.mancha(ovalo(60, 36, 22, 1.6), '0C3A33', .25, difuso=.8)                                     # la sombra en el barro
    piel(l, [ovalo(41.4, 20.4, 2, 2.2), tubo([(73, 22.6), (79, 21.4)], [.7, .6], 3)], .5, PIEL_CLARA)
    l.masa(forma([(43, 21.4), (50, 22.6), (70, 23.4), (74, 22.4), (73, 24.8), (50, 25.4), (44, 24.6)], 2), material='claro', alto=.4, brillo=.3, vientre=0,
           hondo=0, linea=.35)                                           # el traje blanco del capitán, acostado
    l.masa([ovalo(40.6, 18, 3, 1.2), forma([(38.6, 18.2), (39, 15.6), (42.4, 15.2), (43.2, 18)], 1)], material='claro', alto=.4, brillo=.3, vientre=0,
           hondo=0, linea=.3)                                            # el casco de explorador
    l.mancha(ovalo(42.4, 20, .3, .34), '05201C', 1)
    l.trazo([(41.6, 21.6), (43.6, 21.8)], .3, color='3A2A0A', alfa=.85)  # el bigote
    for u in (79.6, 80.4):                                               # los zapatos
        l.mancha(ovalo(u, 21.2, .6, .5), '0C3A33', .9)
    m = l.masa(hamaca, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for k in range(10):                                                  # el tejido del chinchorro
        x = 36 + k * 5.2
        l.trazo([(x, 22.6), (x + 1.6, 29)], .16, color='6B4E10', alfa=.5, dentro=m)
    for k in range(3):                                                   # el vaivén
        l.trazo([(56 + k * 2.6, 31.6 + k * .5), (61 + k * 2.6, 31.6 + k * .5)], .2, color='0C3A33', alfa=.45)


# ------------------------------------------------------------------------------------------------ el mar
def mano_indice(x, y, s=1.0):
    """una mano que apunta con el índice hacia la derecha, como en los carteles viejos: el puño, el índice estirado y el puño de la
    camisa"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    return unary_union([forma(P([(-4, -3.4), (-1.6, -4), (1.6, -3.6), (2.6, -2), (2.4, 2.6), (0, 3.6), (-4, 3)]), 1),
                        forma(P([(1.6, -3.6), (9, -3.4), (10, -2.4), (9, -1.6), (2.4, -1.6)]), 1),
                        ovalo(x + 2 * s, y + 0 * s, 1.4 * s, .9 * s), ovalo(x + 1.8 * s, y + 1.6 * s, 1.2 * s, .8 * s), ovalo(x + 1.2 * s, y + 3 * s, 1 * s, .7 * s),
                        box(x - 6.6 * s, y - 3 * s, x - 3.6 * s, y + 3.2 * s)])


def mar(l):
    rng = np.random.default_rng(15)
    cielo(l, sol=None)
    nube(l, 24, 5, 14, .5)
    nube(l, 96, 4, 12, .45)
    # el Índico, a la derecha, con los barcos; el delta, a la izquierda, con manglares y palmeras
    horizonte = 17
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(16):
        x, y = rng.uniform(40, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    for x, y, s in ((90, 17, .9), (110, 19.4, .7)):
        l.masa([forma([(x - 8 * s, y), (x + 8 * s, y), (x + 9 * s, y - 1.6 * s), (x - 8.4 * s, y - 1.6 * s)], 1), box(x - 5 * s, y - 4 * s, x, y - 1.5 * s)],
               material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    costa = forma([(-2, 41.6), (-2, 20), (20, 21), (34, 25), (40, 32), (36, 41.6)], 2)
    orilla(l, costa, tinte=.36)
    for x, y, h in ((6, 24, 12), (16, 27, 14), (28, 30, 10)):
        palmera(l, x, y, h, 1, datiles=False)
    for x in (8, 22, 34):
        mangle(l, x, 39.6, 9, semilla=x)
    # el cartel con la mano dorada, protagonista, que apunta con el índice al Índico
    l.masa(box(57, 18, 59, 38), material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(box(56, 17, 60, 39), '5A3E1E', .6)
    tabla = box(46, 15, 82, 27)
    t = l.masa(tabla, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.4)
    l.mancha(tabla.buffer(1), '8A6A3A', .55, dentro=t)
    for y in (18, 21, 24):
        l.trazo([(46, y), (82, y)], .1, color='3A2A0A', alfa=.4, dentro=t)
    mano = mano_indice(62, 21, 1.55)
    mm = l.masa(mano, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([(65, 16.4), (75, 16.6)], [.05, .3, .05], color='FBEFCB', alfa=.8, dentro=mm)
    l.mancha(box(51.4, 16.4, 56.4, 26), 'FFFFFF', .9, dentro=mm)          # el puño blanco de la camisa


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Mongu', dibujar=mongu), dict(clave='Katima Mulilo', dibujar=katima),
            dict(clave='Livingstone', dibujar=livingstone), dict(clave='Kariba', dibujar=kariba), dict(clave='Tete', dibujar=tete),
            dict(clave='Chinde', dibujar=chinde), dict(clave='mar', dibujar=mar)]
LISTO = True
