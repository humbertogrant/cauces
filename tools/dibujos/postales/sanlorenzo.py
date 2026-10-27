# -*- coding: utf-8 -*-
"""Las postales del San Lorenzo, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta
la «imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: el lago Ontario, el último de los Grandes Lagos, ancho como un mar, que se vacía por un embudo dorado: de su punta sale
  el río, entre las Mil Islas, con sus pinos, sus casitas y un faro;
- Kingston: «un rey con corona de hielo se sienta en la boca del lago y deja salir el río entre mil islas»: el rey, de manto dorado y
  corona de hielo, sentado en su trono sobre la boca del lago; enfrente, el fuerte Henry;
- Cornwall: «una vaca de Cornualles empuja la puerta de una esclusa gigante»: la vaca dorada empuja la compuerta, y el barco de mar sube
  la escalera de agua hacia los Grandes Lagos;
- Montreal: «un monte real con sombrero de nieve mira cómo los rápidos hacen saltar las canoas»: el monte Royal, con su sombrero de
  nieve y su corona dorada, mira los rápidos de Lachine, donde saltan las canoas de corteza; a su pie, la ciudad;
- Trois-Rivières: «tres ríos se dan la mano en un puerto de papel»: visto desde arriba, el Saint-Maurice partido en tres brazos por dos
  islas llega al San Lorenzo, y en el medio flota un barco de papel de diario, dorado; la papelera y los troncos;
- Quebec: «un diamante enorme aprieta el río hasta dejarlo angosto»: un diamante dorado, enorme, metido en el río al pie del cabo
  Diamant, lo deja angosto; arriba, el Château Frontenac y la muralla;
- Tadoussac: «una ballena blanca toca un tambor en la boca del fiordo»: la beluga toca su tambor dorado donde el agua dulce, oscura, se
  vuelve salada, al pie de los acantilados del Saguenay;
- el mar: el golfo de San Lorenzo, con témpanos, gaviotas, un faro y un barco grande, y la cola dorada de una ballena que se hunde (la
  canoa de corteza se queda en el Saguenay: el golfo es de las ballenas y de los barcos grandes).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, abeto, agua, arbol, ave, casitas, cielo, cinta, cordillera, nube, orilla, pasto, piedra, prado, reflejo,  # noqa: F401
                     rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'
HIELO = 'C6EEDC'


def piel(l, piezas, tono=.45):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def islita(l, x, y, w, semilla=0):
    """una de las Mil Islas: una roca con pinos y, a veces, una casita"""
    rng = np.random.default_rng(semilla)
    l.masa(forma([(x - w, y), (x - w * .6, y - 1.2), (x + w * .6, y - 1.2), (x + w, y)], 1), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0,
           linea=.3)
    for k in range(max(1, int(w // 1.6))):
        abeto(l, x - w * .6 + k * 1.6 + rng.uniform(-.3, .3), y - .8, rng.uniform(3, 4.6), 1.6, material='lejos')
    if w > 4 and rng.random() < .6:
        l.masa([box(x + w * .2, y - 2.6, x + w * .2 + 2, y - 1), Polygon([(x + w * .2 - .3, y - 2.6), (x + w * .2 + 1, y - 3.6), (x + w * .2 + 2.3, y - 2.6)])],
               material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # el lago Ontario, ancho como un mar, hasta el horizonte
    m = l.masa(box(-2, 12, 122, 24), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 12, 122, 13.6), '64C8AA', .5, dentro=m)
    rng = np.random.default_rng(1)
    for _ in range(14):
        x, y = rng.uniform(2, 118), rng.uniform(14, 23)
        l.trazo([(x, y), (x + 3, y - .2), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # la orilla de adelante, con las Mil Islas y el río que sale del embudo
    prado(l, 24, 41, .24)
    agua(l, cinta([(60, 35), (58.6, 37.4), (61.4, 39.6), (59.6, 41.6)], [3.4, 5, 7, 9], 8), ondas=3, semilla=2, linea=.3)
    for x, y, w in ((12, 33, 6), (26, 38, 5), (94, 34, 6), (108, 38.6, 5), (40, 40, 3), (82, 40.4, 3)):
        agua(l, ovalo(x, y - .4, w + 2.4, 1.4), linea=.2)
        islita(l, x, y, w, semilla=int(x))
    fr = l.masa([forma([(113, 30), (113.4, 22.4), (115.6, 22.4), (116, 30)], 0), box(112.6, 21.2, 116.4, 22.6)], material='claro', alto=.3, brillo=.2,
                vientre=0, hondo=0, linea=.3)
    l.mancha(box(112, 25, 117, 26.6), '2F8A74', .85, dentro=fr)
    # el embudo dorado, protagonista: el lago entra por arriba y el río sale por la punta
    boca = ovalo(60, 21.4, 22, 3.6)
    cono = Polygon([(38, 21.4), (82, 21.4), (62, 30), (61.6, 35.4), (58.4, 35.4), (58, 30)])
    e = l.masa(cono.union(boca), material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([(42, 22.6), (58.6, 30), (59, 34.6)], [.06, .4, .06], color='FBEFCB', alfa=.85, dentro=e)
    agua(l, ovalo(60, 21.2, 20.4, 2.8), linea=.25)                       # el agua del lago, que entra al embudo
    for k in range(3):
        l.trazo([(60 + (6 + k * 5) * math.cos(t), 21.2 + (.8 + k * .6) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 25)], .16, color='FFFFFF',
                alfa=.7)


# ------------------------------------------------------------------------------------------------ Kingston
def rey(l, x, base, s=1.0):
    """un rey sentado en su trono, de frente: el manto dorado con su cuello de armiño, la cara con barba, la corona de hielo y el cetro"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    t = l.masa([box(x - 8 * s, base - 22 * s, x + 8 * s, base), forma(P([(-8, -22), (-6, -26), (0, -27.6), (6, -26), (8, -22)]), 1)], material='lejos',
               alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)                                # el trono
    manto = forma(P([(-7, 0), (-7.4, -8), (-5.6, -16), (-3, -18.6), (3, -18.6), (5.6, -16), (7.4, -8), (7, 0)]), 2)
    m = l.masa(manto, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for u in (-4, -1.4, 1.4, 4):
        l.trazo(P([(u, -16), (u * 1.3, -1)]), [.06, .2, .06], color='6B4E10', alfa=.5, dentro=m)
    arm = l.masa(forma(P([(-4.6, -18.6), (-3.4, -14), (0, -12.6), (3.4, -14), (4.6, -18.6), (0, -17)]), 1), material='claro', alto=.4, brillo=.3, vientre=0,
                 hondo=0, linea=.3)                                      # el cuello de armiño
    for u, v in ((-2.6, -16.4), (0, -14.4), (2.6, -16.4)):
        l.mancha(O(u, v, .3, .4), '0C3A33', .9, dentro=arm)
    piel(l, [O(0, -21.6, 2.6, 2.8), O(-7.4, -6, 1.2, 1.1), O(7.4, -6, 1.2, 1.1)], .58)
    l.masa(forma(P([(-2.4, -21), (-2, -18.6), (0, -17.8), (2, -18.6), (2.4, -21), (0, -20)]), 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.25)                                                    # la barba
    for dx in (-.9, .9):
        l.mancha(O(dx, -22.2, .28, .32), '05201C', 1)
    corona = forma(P([(-2.8, -23.6), (-3.2, -27), (-1.8, -25.4), (-1, -28.4), (0, -25.6), (1, -28.4), (1.8, -25.4), (3.2, -27), (2.8, -23.6)]), 0)
    c = l.masa(corona, material='claro', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.3, contraluz=.4)
    l.mancha(corona.buffer(1), HIELO, .6, dentro=c)
    for u in (-1, 1):
        l.trazo(P([(u, -24.4), (u * .6, -27.4)]), .14 * s, color='FFFFFF', alfa=.9, dentro=c)
    l.trazo(P([(7.4, -6), (9.4, -18)]), .45 * s, color='BF9129', alfa=.95)                          # el cetro
    l.masa(O(9.6, -18.6, .9, .9), material='claro', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.25)


def kingston(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # el lago, atrás, y el fuerte Henry en su cerro, a la derecha
    m = l.masa(box(-2, 14, 122, 22), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.masa(forma([(84, 22), (90, 15.4), (110, 14.6), (122, 16), (122, 22)], 2), material='cuerpo', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35)
    f = piedra(l, [box(92, 10.4, 114, 15.6), box(94, 8.6, 98, 10.6), box(108, 8.6, 112, 10.6)], .3)
    for x in np.arange(93, 114, 1.8):
        l.mancha(box(x, 10, x + .8, 11), CIELO, 1, dentro=f)
    # el río que sale por debajo del trono, entre las Mil Islas
    prado(l, 22, 41, .24)
    agua(l, forma([(-2, 22), (122, 22), (122, 41.6), (-2, 41.6)], 0), ondas=10, semilla=3, linea=0)
    for x, y, w in ((10, 30, 5), (22, 37, 6), (100, 31, 5), (112, 38, 6), (36, 26, 3), (84, 27, 3)):
        islita(l, x, y, w, semilla=int(x * 3))
    # el rey, protagonista, sentado sobre la boca del lago
    l.masa(forma([(46, 34.6), (48, 31.6), (72, 31.6), (74, 34.6)], 1), material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    rey(l, 60, 31.8, 1)


# ------------------------------------------------------------------------------------------------ Cornwall
def vaca_empuja(l, x, base, s=1.0, lado=1):
    """una vaca dorada que empuja con la cabeza y los hombros, de perfil, mirando a `lado`: las patas de atrás estiradas, haciendo
    fuerza, los cuernos, la cola"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + lado * u * s, base + v * s, rx * s, ry * s, a * lado)
    lejos = [tubo(P([(4, -6), (5.4, -3), (6.4, 0)]), [1.2 * s, 1 * s, .9 * s], 4), tubo(P([(-5, -6.4), (-7.4, -3), (-9, 0)]), [1.2 * s, 1 * s, .9 * s], 4)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.3), '6B4E10', .4)
    cuerpo = [O(-1, -8.4, 7.4, 4), O(7, -9.4, 3.2, 2.6), tubo(P([(5.4, -6.4), (6.6, -3), (7.6, 0)]), [1.3 * s, 1.1 * s, 1 * s], 4),
              tubo(P([(-6, -6.6), (-8.4, -3.2), (-10.4, 0)]), [1.3 * s, 1.1 * s, 1 * s], 4),
              tubo(P([(-8, -10), (-10.4, -10.6), (-11.6, -8)]), [.5 * s, .4 * s, .3 * s], 5)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for u, v, r in ((-3, -10, 1.8), (2, -7, 1.4)):
        l.mancha(O(u, v, r, r * .7), '6B4E10', .45, dentro=c)
    l.masa([tubo(P([(7, -11.4), (6, -13.4), (4.6, -13.6)]), [.5 * s, .4 * s, .2 * s], 4), tubo(P([(8.4, -11.6), (9.4, -13.6), (10.8, -13.8)]), [.5 * s, .4 * s, .2 * s], 4)],
           material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.mancha(O(8.4, -10, .4, .4), '05201C', 1)
    for k in range(3):                                                   # la fuerza
        l.trazo(P([(-12 - k * 1.4, -9 + k * 1.6), (-14 - k * 1.4, -9 + k * 1.6)]), .2 * s, color='0C3A33', alfa=.6)


def cornwall(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # la esclusa: el escalón de agua, alto atrás y bajo adelante, con el barco de mar que sube; la compuerta gigante
    prado(l, 12, 41, .22)
    alta = box(-2, 15, 122, 19.6)
    agua(l, alta, linea=.3)
    piedra(l, box(-2, 19.6, 122, 22), .15, .35)
    agua(l, box(-2, 22, 122, 34), ondas=8, semilla=5, linea=.3)
    l.masa([forma([(14, 30), (52, 30), (54.4, 27.4), (13, 27.6)], 1), box(16, 23.4, 24, 27.7), box(18.6, 21, 20.4, 23.6)], material='lejos', alto=.2,
           brillo=.15, vientre=0, hondo=0, linea=.3)                    # el barco de mar, en la esclusa
    for k in range(5):
        l.masa(box(26 + k * 5, 25.2, 30.4 + k * 5, 27.7), material=('cuerpo', 'claro', 'lejos')[k % 3], alto=.15, brillo=.1, vientre=0, hondo=0, linea=.18)
    puerta = Polygon([(62, 14), (76, 14), (76, 34), (62, 34)])
    p = l.masa(puerta, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(puerta.buffer(1), '6E7E7B', .55, dentro=p)
    for y in (18, 22.6, 27.2, 31.6):
        l.trazo([(62, y), (76, y)], .3, color='3E4E4B', alfa=.7, dentro=p)
    l.trazo([(62, 14), (76, 34)], .3, color='3E4E4B', alfa=.6, dentro=p)
    orilla(l, forma([(-2, 41.6), (-2, 34), (122, 34), (122, 41.6)], 0), tinte=.3)
    # la vaca dorada, protagonista, que empuja la compuerta
    vaca_empuja(l, 90, 38.6, 1.2, -1)


# ------------------------------------------------------------------------------------------------ Montreal
def montreal(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 104, 3.4, 10, .4)
    # el monte Royal, con su sombrero de nieve, su corona dorada y su cara, que mira los rápidos; la ciudad a su pie
    monte = forma([(16, 28), (24, 16), (36, 10), (48, 8.6), (60, 10), (70, 16), (78, 28)], 2)
    l.masa(monte, material='cuerpo', alto=.4, brillo=.1, vientre=0, hondo=.1, linea=.4, contraluz=.3)
    for _ in range(26):
        x, y = rng.uniform(22, 72), rng.uniform(14, 27)
        if monte.buffer(-1.4).contains(ovalo(x, y, 1, .8)):
            l.mancha(ovalo(x, y, 1.2, .9), '164F46', .5)
    sombrero = forma([(30, 13.4), (36, 8), (48, 6.4), (60, 8), (66, 13.4), (56, 11.4), (40, 11.4)], 2)
    l.masa(sombrero, material='claro', alto=.45, brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.3)
    corona = forma([(41, 6.8), (40.6, 2.4), (43.4, 4.6), (46, 1), (48.6, 4.6), (51.4, 1), (54, 4.6), (56.8, 2.4), (56.4, 6.8)], 0)
    l.masa(corona, material='acento', alto=.5, brillo=.55, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for x in (46, 51.4):                                                 # los ojos del monte, que miran los rápidos, a la derecha
        l.mancha(ovalo(x, 16.6, 1.6, 1.3), 'FFFFFF', .95)
        l.mancha(ovalo(x + .7, 16.8, .7, .7), '05201C', 1)
    l.trazo([(45, 21), (49, 22.4), (53, 21)], .3, color='0C3A33', alfa=.7)
    for x in np.arange(10, 86, 3.6):                                     # la ciudad al pie del monte
        h = rng.uniform(3, 7)
        l.masa(box(x, 28.6 - h, x + 3, 28.8), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.22, arroja=False)
    # el río y los rápidos de Lachine, a la derecha, con las canoas de corteza que saltan
    agua(l, box(-2, 28.6, 122, 41.6), ondas=8, semilla=8, linea=0)
    for _ in range(40):
        x, y = rng.uniform(78, 120), rng.uniform(22, 40)
        l.trazo([(x, y), (x + 1.4, y - 1.2), (x + 2.8, y)], .5, color='FFFFFF', alfa=.85)
    prado(l, 18, 22, .2) if False else None
    for x, y, g in ((88, 30, -18), (104, 36, 14), (96, 24, -8)):         # las canoas de corteza, en el aire
        c = affinity.rotate(forma([(x - 6, y - 1.4), (x - 4.4, y), (x + 4.4, y), (x + 6, y - 1.4), (x + 4.6, y + 1), (x - 4.6, y + 1)], 1), g, origin=(x, y))
        cm = l.masa(c, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(c.buffer(1), 'D8C49A', .5, dentro=cm)
        for k in range(4):
            l.trazo([tuple(affinity.rotate(Polygon([(x - 3 + k * 2, y - .6), (x - 3 + k * 2 + .01, y - .6), (x - 3 + k * 2, y - .59)]), g, origin=(x, y)).exterior.coords[0]),
                     tuple(affinity.rotate(Polygon([(x - 3 + k * 2, y + .8), (x - 3 + k * 2 + .01, y + .8), (x - 3 + k * 2, y + .81)]), g, origin=(x, y)).exterior.coords[0])],
                    .14, color='3A2A0A', alfa=.7, dentro=cm)


# ------------------------------------------------------------------------------------------------ Trois-Rivières
def trois_rivieres(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 30, 3, 12, .4)
    # visto desde arriba: el bosque, el Saint-Maurice que baja y se parte en tres brazos por dos islas, y el San Lorenzo, ancho, abajo
    tierra(l, 5, 41, desierto=.12)
    for _ in range(80):
        x, y = rng.uniform(-2, 122), rng.uniform(6, 26)
        l.mancha(ovalo(x, y, rng.uniform(1.2, 2.2), rng.uniform(1, 1.6)), str(rng.choice(['2F8A74', '164F46'])), .6)
    sl = box(-2, 30, 122, 41.6)
    brazos = [cinta([(56, 4), (55, 12), (50, 20), (42, 26), (36, 31)], [4, 4, 3, 2.8, 3], 8), cinta([(56, 4), (56, 14), (58, 22), (60, 31)], [4, 4, 3, 3],
                                                                                                       8),
              cinta([(56, 4), (57, 12), (64, 20), (74, 26), (82, 31)], [4, 4, 3, 2.8, 3], 8)]
    agua(l, unary_union(brazos + [sl]).buffer(.3).buffer(-.3), ondas=10, semilla=9, linea=.35)
    for x0, y0 in ((52, 13), (60, 22), (66, 13)):                        # los troncos que bajan por el río
        l.masa(tubo([(x0, y0), (x0 + 2.4, y0 + .4)], [.5, .5], 2), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.2)
    # la papelera, con sus chimeneas, y el barco de papel de diario, dorado, protagonista, donde se juntan los tres
    for x, h in ((96, 8), (102, 10)):
        l.masa(box(x - .8, 26 - h, x + .8, 26.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        for k in range(3):
            l.mancha(ovalo(x + 1.4 + k * 2, 26 - h - 1.4 - k, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .6 - k * .12, difuso=.4)
    l.masa(box(88, 20.6, 110, 26.2), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.25)
    barco = [Polygon([(46, 33), (74, 33), (68, 39.4), (52, 39.4)]), Polygon([(50, 33), (60, 20.6), (70, 33)])]
    m = l.masa(barco, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    for k in range(6):                                                   # las letras del diario
        y = 25 + k * 1.6
        w = (y - 20.6) / 12.4 * 9
        l.trazo([(60 - w * .7, y), (60 + w * .7, y)], .2, color='6B4E10', alfa=.55, dentro=m)
    for k in range(3):
        l.trazo([(50 + k, 35 + k * 1.4), (70 - k, 35 + k * 1.4)], .2, color='6B4E10', alfa=.55, dentro=m)
    l.trazo([(60, 20.8), (60, 33)], .25, color='6B4E10', alfa=.7, dentro=m)


# ------------------------------------------------------------------------------------------------ Quebec
def quebec(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # el cabo Diamant, el acantilado, con la muralla y el Château Frontenac de techos verdes, a la izquierda
    prado(l, 13, 41, .24)
    cabo = forma([(-2, 41.6), (-2, 12), (20, 11.6), (40, 13), (46, 22), (50, 41.6)], 1)
    c = l.masa(cabo, material='lejos', alto=.35, brillo=.1, vientre=0, hondo=0, linea=.4)
    l.mancha(cabo, '8FA19D', .3, dentro=c)
    ch = l.masa([box(10, 5, 32, 12), box(18, 1.4, 24, 5.2), box(10.4, 2.6, 13.6, 5.2), box(28.4, 2.6, 31.6, 5.2)], material='claro', alto=.3, brillo=.15,
                vientre=0, hondo=0, linea=.35)
    l.mancha(box(8, 0, 34, 13), 'BF9129', .25, dentro=ch)
    for x in np.arange(11, 32, 1.8):
        for y in (7, 9.4):
            l.mancha(box(x, y, x + .8, y + 1.2), '164F46', .75, dentro=ch)
    l.masa([Polygon([(17.4, 1.6), (21, -2.4), (24.6, 1.6)]), Polygon([(10, 2.8), (12, .4), (14, 2.8)]), Polygon([(28, 2.8), (30, .4), (32, 2.8)])],
           material='cuerpo', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.3)                # los techos verdes de cobre
    piedra(l, box(30, 10.6, 44, 13), .25, .3)
    # el río que se angosta entre el cabo y el diamante
    agua(l, forma([(44, 41.6), (44, 24), (52, 16), (70, 16), (64, 26), (60, 41.6)], 1), ondas=6, semilla=10, linea=.35)
    agua(l, forma([(70, 16), (122, 16), (122, 22), (80, 22)], 1), linea=.3)
    # el diamante enorme, dorado, protagonista, metido en el río, que lo deja angosto
    x, y = 84, 24
    corona_ = Polygon([(x - 18, y), (x - 13, y - 6), (x + 13, y - 6), (x + 18, y)])
    pabellon = Polygon([(x - 18, y), (x + 18, y), (x, y + 16)])
    l.mancha(ovalo(x + 2, y + 16, 10, 1.4), '0C3A33', .3, difuso=.6)
    d = l.masa([corona_, pabellon], material='acento', alto=.4, brillo=.6, vientre=0, hondo=0, linea=.45, contraluz=.45)
    for u in (-13, -6, 0, 6, 13):                                        # las facetas
        l.trazo([(x + u, y - 6), (x + u * .6, y)], .18, color='6B4E10', alfa=.6, dentro=d)
        l.trazo([(x + u * 1.3, y), (x, y + 16)], .18, color='6B4E10', alfa=.5, dentro=d)
    l.trazo([(x - 18, y), (x + 18, y)], .22, color='6B4E10', alfa=.6, dentro=d)
    l.mancha(Polygon([(x - 12, y - 5), (x - 6, y - 5), (x - 8, y - 1)]), 'FBEFCB', .85, dentro=d)
    for k, (dx, dy) in enumerate(((-22, -10), (22, -12), (26, 2))):      # los destellos
        l.trazo([(x + dx - 1.6, y + dy), (x + dx + 1.6, y + dy)], .3, color='FFFFFF', alfa=.9)
        l.trazo([(x + dx, y + dy - 1.6), (x + dx, y + dy + 1.6)], .3, color='FFFFFF', alfa=.9)


# ------------------------------------------------------------------------------------------------ Tadoussac
def beluga(l, x, y, s=1.0):
    """la beluga, blanca, de frente oblicua, con su frente abombada y su sonrisa, que asoma del agua y toca el tambor con la aleta"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, y + v * s, rx * s, ry * s, a)
    c = l.masa([forma(P([(-9, 0), (-8, -6), (-4, -10.4), (2, -12), (6.4, -10.6), (8.4, -7.6), (8.6, -4), (7, 0)]), 2),
                forma(P([(-6, -3), (-10.6, -6.6), (-11.6, -4.6), (-7.4, -1.4)]), 1)], material='claro', alto=.5, brillo=.3, vientre=0, hondo=.1, linea=.4,
               contraluz=.35)
    l.mancha(O(5.4, -9, .55, .55), '05201C', 1)
    l.trazo(P([(4.6, -5.6), (6.6, -5), (8.2, -5.8)]), .2 * s, color='0C3A33', alfa=.8)
    l.mancha(O(6.6, -6.6, 1, .5), 'E8A090', .3)
    return c


def tadoussac(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # los acantilados del fiordo del Saguenay, oscuros, y el pueblo con su hotel blanco
    for pts in ([(-2, 30), (-2, 8), (10, 6), (22, 10), (30, 18), (34, 30)], [(84, 30), (90, 16), (100, 9), (112, 7), (122, 8.6), (122, 30)]):
        g = Polygon(pts).buffer(0)
        m = l.masa(g, material='lejos', alto=.35, brillo=.08, vientre=0, hondo=0, linea=.35)
        l.mancha(g, '0C3A33', .3, dentro=m)
        for _ in range(10):
            xx = rng.uniform(pts[1][0], pts[-2][0])
            abeto(l, xx, rng.uniform(12, 24), rng.uniform(3, 5), 1.6, material='lejos')
    h = l.masa([box(96, 10.4, 110, 15), Polygon([(95, 10.6), (103, 7.4), (111, 10.6)])], material='claro', alto=.25, brillo=.15, vientre=0, hondo=0,
               linea=.3)
    # el agua dulce, oscura, del fiordo, que se vuelve salada, verde, en el estuario
    agua(l, box(-2, 22, 122, 41.6), ondas=10, semilla=13, linea=0)
    l.mancha(Polygon([(-2, 22), (40, 22), (24, 41.6), (-2, 41.6)]), '0C3A33', .55, difuso=2)
    l.trazo([(40, 22), (36, 28), (30, 34), (24, 41.6)], .3, color='D2F2DA', alfa=.7)
    # la beluga, que toca su tambor dorado, protagonista, y las notas
    beluga(l, 54, 36, 1.3)
    t = l.masa([box(64, 25.4, 78, 33.6), ovalo(71, 25.4, 7, 1.8)], material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for x in np.arange(65, 78, 2.4):                                     # las cuerdas del tambor
        l.trazo([(x, 26.6), (x + 1.2, 33.4)], .16, color='6B4E10', alfa=.7, dentro=t)
    l.mancha(ovalo(71, 25.2, 6.2, 1.3), 'FBEFCB', .8)
    l.trazo([(60.4, 30), (66, 25)], .4, color='9DB9B0', alfa=.9)         # el palillo, en la aleta
    for x, y in ((80, 16), (86, 22), (44, 18)):
        l.masa([ovalo(x, y, .9, .7, -20), box(x + .7, y - 4, x + 1, y)], material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.2)


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    rng = np.random.default_rng(14)
    cielo(l, sol=None)
    nube(l, 24, 5, 14, .5)
    nube(l, 96, 4, 12, .45)
    horizonte = 16
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # el faro en su roca, a la izquierda, un barco grande lejos, y los témpanos
    l.masa(forma([(-2, 24), (6, 19.4), (18, 19), (24, 24)], 1), material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.3)
    fr = l.masa([forma([(9.6, 19.4), (10, 8.6), (12.2, 8.6), (12.6, 19.4)], 0), box(9.2, 7.4, 13, 8.8)], material='claro', alto=.3, brillo=.2, vientre=0,
                hondo=0, linea=.3)
    l.mancha(box(8, 12, 14, 13.6), '2F8A74', .85, dentro=fr)
    l.masa([forma([(84, horizonte - .4), (108, horizonte - .4), (110, horizonte - 2), (83, horizonte - 2)], 1), box(86, horizonte - 4.4, 92, horizonte - 1.9)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    for x, y, w in ((30, 30, 6), (96, 26, 7), (104, 36, 5), (16, 37, 5), (80, 34, 4)):
        l.masa(forma([(x - w, y), (x - w * .6, y - 1.6), (x + w * .4, y - 1.8), (x + w, y)], 1), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0,
               linea=.3)
        l.mancha(forma([(x - w, y), (x + w, y), (x + w * .9, y + .8), (x - w * .9, y + .8)], 1), HIELO, .7)
    for x, y, s in ((40, 8, .8), (52, 6, .6), (70, 9, .7)):
        ave(l, x, y, s)
    # la cola dorada de la ballena, protagonista, que se hunde, con el agua que chorrea
    cola = unary_union([tubo([(60, 34), (60.4, 28), (60, 24)], [3.4, 2.4, 1.6], 4),
                        forma([(60, 24), (54, 20.6), (46, 17), (42, 17.6), (46, 21), (52, 24.6), (58, 25.6)], 2),
                        forma([(60, 24), (66, 20.6), (74, 17), (78, 17.6), (74, 21), (68, 24.6), (62, 25.6)], 2)])
    l.mancha(ovalo(60, 34.6, 9, 1.6), 'FFFFFF', .7, difuso=.5)
    c = l.masa(cola, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    for x in (44, 48, 72, 76):                                           # el agua que chorrea de la cola
        l.trazo([(x, 19), (x + .2, 23)], .3, color='FFFFFF', alfa=.85)
    reflejo(l, cola, 34.6, .25, 'F2D48A')


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Kingston', dibujar=kingston), dict(clave='Cornwall', dibujar=cornwall),
            dict(clave='Montreal', dibujar=montreal), dict(clave='Trois-Rivières', dibujar=trois_rivieres), dict(clave='Quebec', dibujar=quebec),
            dict(clave='Tadoussac', dibujar=tadoussac), dict(clave='mar', dibujar=mar)]
LISTO = True
