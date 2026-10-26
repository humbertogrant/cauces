# -*- coding: utf-8 -*-
"""Las postales del Danubio, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: la fuente del Danubio en Donaueschingen, un estanque redondo con su baranda dorada, de donde sale el río joven, entre
  los abetos oscuros de la Selva Negra, que se ve negra de verdad;
- Ulm: «una U con un campanario dentro»: una U dorada, enorme, y adentro la torre de la catedral, la más alta del mundo durante más de
  un siglo, que la pasa; en el río, una caja de Ulm, la barcaza de un solo viaje;
- Ratisbona: «una rata cruza un puente de piedra medieval»: la rata, dorada, sobre el Puente de Piedra de muchos arcos, con las dos
  torres de la catedral detrás;
- Passau: «tres ríos se hacen un pase»: visto desde arriba, el Inn verde (el más ancho, porque trae más agua), el Ilz negro y el Danubio
  azul se juntan en la punta de la ciudad, y una pelota dorada vuela entre ellos;
- Linz: «una tarta Linzer con enrejado de masa»: la tarta, dorada, en la orilla, con su enrejado sobre la mermelada; atrás, los puentes;
- Viena: «un vals sobre el agua, aunque en Viena el río es café»: una pareja que baila el vals sobre el río café, ella con su vestido de
  baile dorado, entre notas; atrás, la catedral de San Esteban y la noria del Prater;
- Bratislava: «dos hermanos a 60 km»: dos hermanos abrazados, con camisetas doradas, que señalan cada uno su capital: Viena, lejos río
  arriba, y el castillo blanco de Bratislava, con el puente del platillo volador;
- Budapest: «Buda arriba, Pest abajo y el río en medio»: el Puente de las Cadenas, con sus dos torres de piedra y las cadenas doradas,
  entre el castillo en la colina de Buda y el Parlamento en el llano de Pest;
- Belgrado: «la ciudad blanca donde el Sava entra»: la fortaleza blanca de Kalemegdan sobre la punta donde se juntan los dos ríos, y en
  su borde el Vencedor, dorado en su columna, que vigila la confluencia;
- el mar: el mar Negro, oscuro como su nombre, con los pelícanos blancos del delta (Valsa se queda con ellos), de bolsa dorada; la caja
  de Ulm no llega: al final del viaje se vende como leña.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, abeto, agua, arbol, ave, casitas, cebolla_baja, cielo, cinta, juncos, nube, orilla, pasto,  # noqa: F401
                     piedra, prado, reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
AZUL = '3F6F9F'            # el Danubio azul de Passau
CAFE = '8A6A3A'            # el río café de Viena
MERMELADA = '4A2418'       # la mermelada de grosellas de la tarta Linzer: casi negra


def piel(l, piezas, tono=.45):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 26, 4.4, 14, .55)
    nube(l, 98, 3.6, 10, .45)
    # la Selva Negra: lomas cubiertas de abetos oscuros, casi negros, una detrás de otra
    for (pts, mat) in (([(-2, 7), (14, 3), (34, 5.4), (52, 2.4), (74, 5), (96, 2), (122, 5.4)], 'lejos'),
                       ([(-2, 11.4), (20, 7.4), (44, 10.4), (64, 8), (88, 11), (122, 7.6)], 'oscuro')):
        g = Polygon([(-2, 41)] + pts + [(122, 41)])
        l.masa(g, material=mat, alto=.3, brillo=.05, vientre=0, hondo=0, linea=.35, escalon=.3, contraluz=.25)
        for dy in (1.8, 4.8, 7.8, 10.8, 13.8):
            for x in np.arange(-1 + dy * .4, 122, 2.2):
                y = np.interp(x, [p[0] for p in pts], [p[1] for p in pts]) + dy
                if y < 22.4:
                    abeto(l, x + rng.uniform(-.6, .6), y + rng.uniform(0, .8), rng.uniform(4.2, 5.8), rng.uniform(2, 2.8), material='oscuro')
    # el pueblo de Donaueschingen, al pie, con su iglesia de dos torres
    prado(l, 19.4, 41, .24)
    casitas(l, 6, 40, 21, 3.4, semilla=2)
    casitas(l, 82, 116, 21, 3.4, semilla=3)
    for x in (21, 28.4):
        l.masa([box(x - 1.6, 12, x + 1.6, 21.6), cebolla_baja(x, 12.2, 1.7)], material='claro', alto=.3, brillo=.12, vientre=0, hondo=0,
               linea=.3)
        l.mancha(forma([(x - .5, 16.6), (x - .5, 14.6), (x, 14), (x + .5, 14.6), (x + .5, 16.6)], 1), '164F46', .8)
    l.masa(box(21, 15, 28.4, 21.6), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(forma([(23.6, 21.4), (23.6, 18.6), (24.7, 17.6), (25.8, 18.6), (25.8, 21.4)], 1), '164F46', .85)
    # los abetos oscuros de adelante, a los costados
    for x, y, h in ((5, 36, 14), (13, 39.6, 17), (2, 41, 10), (107, 37, 15), (116, 40.4, 17), (98, 40, 10)):
        abeto(l, x, y, h, h * .42, material='oscuro')
    # la fuente: el estanque redondo con su baranda dorada, protagonista, y el río joven que sale de él hacia nosotros
    agua(l, cinta([(60, 33), (57, 36.4), (61, 39), (59, 41.6)], [6, 7.4, 8.6, 9.6], 8), ondas=3, semilla=4, linea=.3)
    cx, cy, rx, ry, muro = 60, 26.4, 19, 6.4, 3.6
    frente = Polygon([(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, math.pi, 40)] +
                     [(cx + rx * math.cos(t), cy + muro + ry * math.sin(t)) for t in np.linspace(math.pi, 0, 40)])
    l.masa(frente, material='acento', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.45, contraluz=.3)       # el muro del estanque
    for t in np.linspace(.12, math.pi - .12, 15):                       # los balaustres del frente
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        l.trazo([(x, y + .5), (x, y + muro - .4)], .32, color='6B4E10', alfa=.55)
    agua(l, ovalo(cx, cy, rx - 1.4, ry - .9), ondas=5, semilla=5, linea=.25)                                  # el agua de la fuente
    l.mancha(ovalo(cx, cy - .6, rx - 5, ry - 3), 'D2F2DA', .45, difuso=.8)
    for k in range(3):                                                  # las ondas del manantial
        l.trazo([(cx + (3 + k * 3) * math.cos(t), cy + (1 + k) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 25)], .14, color='FFFFFF',
                alfa=.6)
    borde = ovalo(cx, cy, rx, ry).difference(ovalo(cx, cy, rx - 1.4, ry - .9))
    l.masa(borde, material='acento', alto=.4, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.35)        # la baranda
    l.masa(box(cx - 2.6, cy + ry - .4, cx + 2.6, cy + ry + muro + .2), material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.4)
    agua(l, cinta([(cx, cy + ry - .2), (cx, cy + ry + muro + 1)], [3.6, 4.4], 4), linea=.25)                  # el desagüe, por donde sale


# ------------------------------------------------------------------------------------------------ Ulm
def caja_ulm(l, x, y, s=1.0):
    """la caja de Ulm, chica, mirando a la derecha: el cajón de tablas de madera con las puntas en rampa y la casita a franjas blancas y
    negras; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    casa = l.masa(Polygon(P([(-4, -1.6), (3, -1.6), (3, -4.4), (-4, -4.4)])), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0,
                  linea=.3)
    for k in range(3):
        l.mancha(Polygon(P([(-4, -2.2 - k * .9), (3, -2.2 - k * .9), (3, -2.6 - k * .9), (-4, -2.6 - k * .9)])), '0C3A33', .9, dentro=casa)
    l.masa(Polygon(P([(-4.6, -4.2), (-.5, -6), (3.6, -4.2)])), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    c = l.masa(Polygon(P([(-9.6, -2.4), (-7.4, -1.4), (7.4, -1.4), (9.6, -2.4), (8.4, .4), (-8.4, .4)])), material='vientre', alto=.3, brillo=.2,
               vientre=0, hondo=0, linea=.35)
    l.mancha(Polygon(P([(-10, -3), (10, -3), (10, 1), (-10, 1)])), '8A6A3A', .6, dentro=c)        # las tablas de pino
    return c


def ulm(l):
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .55)
    nube(l, 100, 4, 12, .5)
    # la ciudad vieja, en la orilla de enfrente, y el río
    prado(l, 25, 41, .22)
    casitas(l, -1, 40, 29.6, 5, semilla=1)
    casitas(l, 80, 122, 29.6, 5, semilla=2)
    rio(l, 30.4)
    caja_ulm(l, 22, 36.4, 1.1)
    # la nave de la catedral, detrás de la torre
    piedra(l, [box(66, 18.4, 92, 29), Polygon([(65.4, 18.6), (79, 13.4), (92.6, 18.6)])], .25)
    for x in np.arange(68.4, 91, 3.2):
        l.mancha(forma([(x - .6, 27), (x - .6, 21.4), (x, 20.2), (x + .6, 21.4), (x + .6, 27)], 1), '164F46', .7)
    # la torre de la catedral, la más alta del mundo durante más de un siglo: el cuerpo, la parte octogonal y la aguja calada
    t = piedra(l, [box(54.4, 14.4, 65.6, 29.6), box(55.8, 8.4, 64.2, 14.6), Polygon([(56.6, 8.6), (60, -2), (63.4, 8.6)])], .3, .4)
    l.mancha(forma([(58, 29), (58, 23.4), (60, 21.4), (62, 23.4), (62, 29)], 1), '0C3A33', .85, dentro=t)        # el portal
    for x in (56.4, 63.6):                                              # los contrafuertes
        l.trazo([(x, 29.4), (x, 14.6)], .3, color='6B4E10', alfa=.45, dentro=t)
    for y in (14.6, 8.6):
        l.trazo([(54, y), (66, y)], .3, color='6B4E10', alfa=.5, dentro=t)
    for x in (57.6, 60, 62.4):                                          # las ventanas altas y la aguja calada
        l.mancha(forma([(x - .45, 17.8), (x - .45, 12.2), (x, 11.4), (x + .45, 12.2), (x + .45, 17.8)], 1), '164F46', .8, dentro=t)
    for y in np.arange(.8, 8, 1.6):
        w = (8.6 - y) / 10.6 * 3.4
        l.trazo([(60 - w * .9, y + .4), (60 + w * .9, y + .4)], .12, color='6B4E10', alfa=.6, dentro=t)
    l.trazo([(60, -2.2), (60, 8.4)], .12, color='6B4E10', alfa=.5, dentro=t)
    # la U dorada, protagonista: la torre está adentro
    u = cinta([(47.4, 4.4), (47.4, 21), (49.4, 27.4), (54, 30.6), (60, 31.4), (66, 30.6), (70.6, 27.4), (72.6, 21), (72.6, 4.4)], [4.4] * 9, 6)
    m = l.masa(u, material='acento', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.5, contraluz=.4)
    l.trazo([(46.2, 5), (46.2, 21), (48, 27), (52, 30.2), (56, 31.6)], [.08, .2, .2, .1, .05], color='FBEFCB', alfa=.7, dentro=m)
    for x0 in (45.2, 70.4):                                             # las puntas, cortadas derecho, con su remate
        l.masa(box(x0, 3.4, x0 + 4.4, 5), material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4)
    reflejo(l, u, 30.6, .22)


# ------------------------------------------------------------------------------------------------ Ratisbona
def rata(l, x, base, s=1.0):
    """una rata que camina, de perfil, mirando a la derecha: el cuerpo en pera, el hocico puntudo con sus bigotes, las orejas redondas,
    las patitas y la cola larga y fina que se curva atrás; (x, base) es donde pisan las patas de adelante"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cola = tubo(P([(-12, -3.6), (-17, -2.6), (-21, -4.8), (-23.6, -9), (-22.4, -12.4)]), [.9 * s, .7 * s, .5 * s, .35 * s, .2 * s], 8)
    l.masa(cola, material='acento', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    patas = [tubo(P([(-9.4, -3.4), (-10.4, -1.4), (-9.6, 0)]), [1.3 * s, 1 * s, .7 * s], 5), tubo(P([(-.6, -3), (.2, -1.2), (.6, 0)]), [1 * s, .8 * s, .6 * s], 5)]
    lejos = [tubo(P([(-6.8, -3), (-7, -1), (-6.2, 0)]), [1.1 * s, .9 * s, .6 * s], 5), tubo(P([(1.6, -3.2), (2.6, -1.2), (3, 0)]), [.9 * s, .7 * s, .5 * s], 5)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.2), '6B4E10', .35)
    cuerpo = [O(-6, -6.4, 7.2, 4.6), O(1.6, -6.4, 4, 3.4), forma(P([(3.4, -9), (6.6, -8), (9.6, -6.6), (10.4, -6), (9.6, -5.4), (5.6, -4.2), (3, -4)]), 2)]
    c = l.masa(cuerpo + patas, material='acento', alto=.6, brillo=.4, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.pelaje(c, densidad=.6, largo=1.2, ancho=.14, alfa=.18, semilla=3)
    l.masa([O(3.4, -10.2, 1.8, 1.9), O(.8, -10.4, 1.5, 1.7)], material='acento', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35)   # las orejas
    l.mancha(O(3.4, -10.1, 1, 1.1), 'E8A090', .45)
    l.mancha(O(10.2, -6, .5, .45), '05201C', 1)                            # la nariz
    l.mancha(O(6.2, -7.6, .55, .55), '05201C', 1)                          # el ojo
    l.mancha(O(6.35, -7.75, .16, .16), 'FFFFFF', .9)
    for dy in (-.8, 0, .8):                                              # los bigotes
        l.trazo(P([(9.4, -5.8), (12.6, -5.8 + dy * 1.4)]), .08 * s, color='0C3A33', alfa=.7)


def ratisbona(l):
    cielo(l, sol=None)
    nube(l, 20, 4.6, 12, .5)
    nube(l, 92, 4, 12, .5)
    # la ciudad vieja enfrente, con la catedral de dos torres
    prado(l, 18, 24, .22)
    casitas(l, -1, 46, 20.4, 4.6, semilla=4)
    casitas(l, 84, 122, 20.4, 4.6, semilla=5)
    d = piedra(l, [box(62, 11.6, 82, 20.6), box(63, 3.4, 67.4, 12), box(76.6, 3.4, 81, 12), Polygon([(62.6, 3.6), (65.2, -2.6), (67.8, 3.6)]),
                   Polygon([(76.2, 3.6), (78.8, -2.6), (81.4, 3.6)])], .2)
    for x in (65.2, 78.8):
        l.mancha(forma([(x - .6, 10.6), (x - .6, 6.4), (x, 5.6), (x + .6, 6.4), (x + .6, 10.6)], 1), '164F46', .8, dentro=d)
    l.mancha(forma([(70.4, 19.6), (70.4, 15), (72, 13.4), (73.6, 15), (73.6, 19.6)], 1), '164F46', .8, dentro=d)
    rio(l, 23.6)
    # el Puente de Piedra: largo y bajo, con muchos arcos y un lomo suave al medio
    lomo = lambda x: 21.4 - 1.4 * math.exp(-((x - 60) / 34) ** 2)
    tablero = Polygon([(x, lomo(x)) for x in np.arange(-2, 122.1, 2)] + [(122, 31.6), (-2, 31.6)])
    for x in np.arange(-1, 122, 11.4):
        tablero = tablero.difference(forma([(x + 1.6, 33), (x + 1.6, 28.6), (x + 5.7, 25.2), (x + 9.8, 28.6), (x + 9.8, 33)], 2))
    p = piedra(l, tablero, .35, .4)
    for x in np.arange(-1, 122, 11.4):                                   # los tajamares, que cortan la corriente
        l.masa(Polygon([(x - 1.4, 31.6), (x, 29.4), (x + 1.4, 31.6)]), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(0, 122, 2.2):                                     # las piedras del pretil
        l.trazo([(x, lomo(x) + .3), (x, lomo(x) + 1.6)], .08, color='6B4E10', alfa=.4, dentro=p)
    l.trazo([(x, lomo(x) + 1.8) for x in np.arange(-2, 122.1, 4)], .14, color='6B4E10', alfa=.5, dentro=p)
    l.mancha(box(-2, 31.4, 122, 40), '0C3A33', .15, difuso=1)
    # la rata, protagonista, que cruza el puente
    rata(l, 70, lomo(70) + .4, 1.22)


# ------------------------------------------------------------------------------------------------ Passau
def pelota(l, x, y, r):
    """una pelota de fútbol dorada, con sus pentágonos oscuros, y las rayas del pase"""
    p = l.masa(ovalo(x, y, r, r), material='acento', alto=.8, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.mancha(Polygon([(x + r * .32 * math.cos(math.radians(a)), y + r * .32 * math.sin(math.radians(a))) for a in range(-90, 270, 72)]),
             '6B4E10', .85, dentro=p)
    for a in range(-54, 306, 72):
        cx, cy = x + r * .86 * math.cos(math.radians(a)), y + r * .86 * math.sin(math.radians(a))
        l.mancha(ovalo(cx, cy, r * .26, r * .26), '6B4E10', .75, dentro=p)
        l.trazo([(x + r * .32 * math.cos(math.radians(a)), y + r * .32 * math.sin(math.radians(a))), (cx, cy)], .12, color='6B4E10', alfa=.6,
                dentro=p)


def passau(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 30, 2.6, 12, .45)
    # visto desde arriba: el prado, y enfrente el cerro con su bosque y la Veste, la fortaleza de arriba
    prado(l, 5, 41, .3)
    cerro = forma([(46, 13.4), (50, 8), (56, 3), (60, -2), (124, -2), (124, 11.4), (104, 12.6), (84, 12.4), (66, 14.4)], 2)
    l.masa(cerro, material='cuerpo', alto=.3, brillo=.08, vientre=0, hondo=0, linea=.3)
    for _ in range(60):
        x, y = rng.uniform(50, 120), rng.uniform(1, 12.4)
        if cerro.buffer(-.6).contains(ovalo(x, y, .6, .5)) and not (66 < x < 92 and y < 7.4):
            l.masa(ovalo(x, y, 1.1, .9), material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
    v = l.masa([box(68, 3.4, 90, 6.8), box(71, 1.2, 75, 6.8), box(83.6, 1.2, 87.6, 6.8), box(77.4, -.6, 80.6, 4)], material='claro', alto=.25,
               brillo=.15, vientre=0, hondo=0, linea=.3)
    for x in np.arange(68.6, 90, 1.4):
        l.mancha(box(x, 3.3, x + .6, 3.9), CIELO, 1, dentro=v)
    # los tres ríos: el Danubio azul por arriba, el Inn verde y ancho por abajo, el Ilz negro y angosto que baja del cerro; juntos siguen
    # a la derecha un buen trecho con sus tres colores lado a lado
    danubio = cinta([(-2, 12.6), (20, 13.6), (40, 16), (56, 18.6), (68, 20.6)], [6, 6.4, 6.8, 7, 7.2], 8)
    inn = cinta([(-2, 35.4), (20, 34.6), (40, 31.6), (56, 27.6), (68, 25.2)], [10.4, 10.8, 11, 10.8, 10.4], 8)
    ilz = cinta([(126, 12.6), (112, 14.4), (100, 13.6), (88, 15.6), (78, 16.4), (70, 20)], [3.4, 3.8, 4, 4.2, 4.4, 4.6], 8)
    junto = cinta([(58, 22.4), (70, 23), (84, 24.6), (102, 27.2), (124, 30.6)], [12.6, 13.4, 14, 15, 16], 8)
    agua_toda = unary_union([danubio, inn, ilz, junto]).buffer(.3).buffer(-.3)
    j = agua(l, agua_toda, material='lejos', ondas=0, linea=.35)
    l.mancha(junto, '4EB196', .55, dentro=j, difuso=1.4)
    l.mancha(cinta([(64, 20.6), (84, 21.8), (102, 24), (124, 26.8)], [5.4, 6, 6, 5.4], 8), AZUL, .7, dentro=j, difuso=.5)
    l.mancha(cinta([(66, 19), (84, 19.4), (100, 21.2), (124, 24.2)], [2.4, 2.4, 2, 1.4], 8), '05201C', .75, dentro=j, difuso=.3)
    for g, color, alfa in ((danubio, AZUL, .7), (inn, '2F8A74', .6), (ilz, '05201C', .74)):
        l.mancha(g, color, alfa, dentro=j, difuso=1.4)
    for g, n, color in ((danubio, 10, 'A4C4DC'), (inn, 14, 'C6EEDC'), (ilz, 9, '6FA497'), (junto, 14, 'D2F2DA')):   # las ondas, a lo largo
        x0, y0, x1, y1 = g.bounds
        for _ in range(n):
            for _ in range(40):
                x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
                if g.buffer(-.4).contains(box(x, y - .25, x + 2.4, y + .25)):
                    l.trazo([(x, y), (x + 1.2, y - .2), (x + 2.4, y)], .14, color=color, alfa=.85)
                    break
    # la ciudad vieja en la punta, entre el Danubio y el Inn, con la catedral blanca de cúpulas verdes
    punta = forma([(-2, 17.6), (20, 18.4), (40, 21), (54, 23), (63, 23.4), (54, 24.4), (40, 26), (20, 28.6), (-2, 29.6)], 2)
    orilla(l, punta, tinte=.26)
    for _ in range(70):
        x, y = rng.uniform(1, 58), rng.uniform(18.6, 29.4)
        c = box(x - 1.1, y - 1.3, x + 1.1, y)
        if not punta.buffer(-.5).contains(c) or (24 < x < 42 and y < 25.4):
            continue
        l.masa(c, material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
        l.masa(Polygon([(x - 1.3, y - 1.3), (x, y - 2.4), (x + 1.3, y - 1.3)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2,
               arroja=False)
    cat = l.masa([box(26, 18.6, 40, 24.6), box(26.4, 14.2, 29.8, 19), box(36.2, 14.2, 39.6, 19)], material='claro', alto=.3, brillo=.15, vientre=0,
                 hondo=0, linea=.35)
    for x in (28.1, 37.9):
        l.mancha(forma([(x - .5, 18), (x - .5, 16), (x, 15.4), (x + .5, 16), (x + .5, 18)], 1), '164F46', .8, dentro=cat)
    l.masa([cebolla_baja(28.1, 14.4, 1.7), cebolla_baja(37.9, 14.4, 1.7), cebolla_baja(33, 18.8, 2.6)], material='cuerpo', alto=.4, brillo=.3,
           vientre=0, hondo=0, linea=.3)
    # el pase: la pelota dorada, protagonista, que vuela sobre la confluencia, y su recorrido de un río a otro
    for pts in ([(36, 14.4), (46, 6.6), (57, 9.4)], [(82, 12.6), (78, 6.4), (68, 8.8)], [(50, 29), (52, 20), (58, 15.2)]):
        c = curva(pts, 10)
        for k in range(0, len(c) - 1, 2):
            l.trazo([tuple(c[k]), tuple(c[k + 1])], .42, color='FFFFFF', alfa=.95)
    pelota(l, 62.4, 11.4, 4.8)


# ------------------------------------------------------------------------------------------------ Linz
def tarta(l, x, y, rx, ry, alto_):
    """la tarta Linzer, vista un poco desde arriba: el borde de masa dorada, la mermelada oscura y el enrejado de tiras de masa
    cruzadas; (x, y) es el centro de la tapa"""
    lado = Polygon([(x + rx * math.cos(t), y + ry * math.sin(t)) for t in np.linspace(0, math.pi, 40)] +
                   [(x + rx * math.cos(t), y + alto_ + ry * math.sin(t)) for t in np.linspace(math.pi, 0, 40)])
    l.mancha(ovalo(x, y + alto_ + ry * .6, rx * 1.15, ry * .7), '0C3A33', .3, difuso=1)
    l.masa(ovalo(x, y + alto_ + .8, rx + 3, ry + 1.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.35)   # el plato
    m = l.masa(lado, material='acento', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.45, contraluz=.3)
    for t in np.linspace(.15, math.pi - .15, 26):                       # el borde ondulado, marcado con el tenedor
        px, py = x + rx * math.cos(t), y + ry * math.sin(t)
        l.trazo([(px, py + .6), (px, py + alto_ - .4)], .14, color='6B4E10', alfa=.45, dentro=m)
    tapa = ovalo(x, y, rx, ry)
    l.masa(tapa, material='acento', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.4)
    dentro = ovalo(x, y, rx - 2.2, ry - 1)
    l.mancha(dentro, MERMELADA, .92)
    l.mancha(ovalo(x - rx * .25, y - ry * .3, rx * .35, ry * .3), 'E8A090', .25, difuso=.8)
    tiras = []
    for k in np.arange(-rx, rx + .1, rx / 3.4):                          # el enrejado: tiras en diagonal, cruzadas
        for sgn in (-1, 1):
            tiras.append(Polygon([(x + k - .8 + sgn * ry * 1.4, y - ry * 1.1), (x + k + .8 + sgn * ry * 1.4, y - ry * 1.1),
                                  (x + k + .8 - sgn * ry * 1.4, y + ry * 1.1), (x + k - .8 - sgn * ry * 1.4, y + ry * 1.1)]))
    rejilla = unary_union(tiras).intersection(dentro)
    l.masa(rejilla, material='acento', alto=.35, brillo=.35, vientre=0, hondo=0, linea=.3, contraluz=.3)
    borde = tapa.difference(ovalo(x, y, rx - 2.2, ry - 1))
    l.masa(borde, material='acento', alto=.45, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for t in np.linspace(0, 2 * math.pi, 34)[:-1]:                       # las marcas del borde
        px, py = x + (rx - 1.1) * math.cos(t), y + (ry - .5) * math.sin(t)
        l.trazo([(px - .3, py), (px + .3, py)], .12, color='6B4E10', alfa=.5)


def linz(l):
    cielo(l, sol=None)
    nube(l, 26, 4.4, 14, .55)
    nube(l, 100, 4, 10, .45)
    # atrás: el cerro con la basílica de dos torres, la ciudad, el río y sus puentes
    l.masa(forma([(-2, 18), (6, 12), (14, 8.6), (22, 8.2), (30, 11.4), (40, 17), (-2, 19)], 2), material='lejos', alto=.3, brillo=.06, vientre=0,
           hondo=0, linea=.35)
    l.masa([box(15.4, 4.4, 20.8, 9), box(15.6, 2.2, 17, 5), box(19.2, 2.2, 20.6, 5), cebolla_baja(16.3, 2.4, .8), cebolla_baja(19.9, 2.4, .8)],
           material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.3)
    prado(l, 16, 22, .2)
    casitas(l, 30, 74, 18, 4, semilla=6)
    l.masa(Polygon([(84, 18.2), (86, 11.4), (100, 11.4), (102, 18.2)]), material='claro', alto=.25, brillo=.3, vientre=0, hondo=0, linea=.3)
    for y in np.arange(12.6, 18, 1.3):                                   # el cubo de vidrio a orillas del río
        l.trazo([(85.6, y), (100.6, y)], .14, color='8EB5AA', alfa=.8)
    rio(l, 21)
    for x0, x1, y in ((-2, 122, 21.4),):                                 # el puente largo y chato, de acero
        l.masa(box(x0, y - .2, x1, y + 1), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
        for x in np.arange(6, 120, 14):
            l.masa(box(x - .5, y + .8, x + .5, y + 3.4), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # la orilla de adelante, con la tarta, protagonista, en su plato
    m = orilla(l, forma([(-2, 41.5), (-2, 28.6), (30, 27.6), (60, 27.2), (90, 27.6), (122, 28.6), (122, 41.5)], 2), tinte=.24)
    pasto(l, 0, 120, 29, 40.6, 22, semilla=7, dentro=m)
    tarta(l, 60, 27, 25, 7.2, 4.4)


# ------------------------------------------------------------------------------------------------ Viena
def pareja(l, x, base, s=1.0):
    """una pareja que baila el vals: él, de frac oscuro, la toma de la cintura; ella, con el vestido de baile dorado que se abre al
    girar; las manos juntas, en alto, del lado de ella; (x, base) es el pie del vestido"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    # él, a la izquierda, mirando a la derecha: las piernas, el frac con sus faldones, el brazo que la abraza
    l.masa([tubo(P([(-5.4, -9), (-5.8, -4.6), (-6.4, -.2)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(-3.6, -9), (-3.2, -4.6), (-2.8, -.2)]), [1.1 * s, 1 * s, .9 * s], 5),
            O(-6.8, -.1, 1.3, .55), O(-2.4, -.1, 1.3, .55)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    frac = l.masa([forma(P([(-7.2, -19.6), (-2.6, -19.6), (-2.2, -13), (-2.8, -8.4), (-7, -8.4), (-7.6, -13)]), 1),
                   Polygon(P([(-7, -10), (-8.4, -5.6), (-6.4, -7.6)])),
                   tubo(P([(-3.4, -18.6), (0, -16.2), (3.4, -14.4)]), [1 * s, .9 * s, .8 * s], 6)], material='oscuro', alto=.4, brillo=.35,
                  vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.masa(Polygon(P([(-5.6, -19.6), (-4.2, -15.6), (-3, -19.6)])), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)   # la pechera
    l.trazo(P([(-5, -19.4), (-4.2, -18.6), (-3.4, -19.4)]), .3 * s, color='05201C', alfa=.9)                                           # la corbata de moño
    piel(l, [O(-4.6, -22.4, 2.2, 2.4), box(x - 5.2 * s, base - 20.6 * s, x - 4 * s, base - 19.4 * s)], .5)
    l.masa(forma(P([(-6.8, -22.6), (-6.4, -24.6), (-4.4, -25.2), (-2.6, -24.4), (-2.4, -23)]), 1), material='oscuro', alto=.3, brillo=.3,
           vientre=0, hondo=0, linea=.25)                                # el pelo
    l.mancha(O(-3.6, -22.8, .24, .28), '05201C', 1)
    l.trazo(P([(-3.6, -21.2), (-2.9, -21), (-2.6, -21.4)]), .14 * s, color='0C3A33', alfa=.9)
    # ella, a la derecha, mirando a la izquierda: el vestido dorado, ancho, que gira; el talle, los brazos y la cabeza con su moño
    v = l.masa(forma(P([(1.6, -15.6), (5.6, -15.6), (6.4, -12.6), (12.4, -3.4), (13, .2), (6, 1), (-1, .6), (-2.2, -2.6), (1.2, -12.6)]), 2),
               material='acento', alto=.5, brillo=.4, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.4)
    for u0, u1 in ((3, 1.6), (4.6, 5.4), (6, 9.4), (7.2, 12)):           # los pliegues del vuelo
        l.trazo(P([(u0, -11.6), (u1, -.6)]), [.06, .2, .1], color='6B4E10', alfa=.45, dentro=v)
    l.trazo(P([(-1.6, -1.4), (3, .2), (8, .2), (12.6, -1)]), [.1, .24, .24, .1], color='FBEFCB', alfa=.7, dentro=v)
    l.masa(forma(P([(1.4, -21), (5.4, -21), (5.8, -15.4), (1.6, -15.4)]), 1), material='acento', alto=.4, brillo=.35, vientre=0, hondo=0,
           linea=.35)                                                    # el corpiño
    piel(l, [O(3.8, -23.6, 2, 2.2), box(x + 3.2 * s, base - 21.8 * s, x + 4.4 * s, base - 20.8 * s),
             tubo(P([(1.8, -20.4), (-.6, -21.6), (-2.6, -22.6)]), [.6 * s, .55 * s, .5 * s], 6),
             tubo(P([(5.4, -20.4), (7.4, -24), (6.4, -27.4)]), [.6 * s, .55 * s, .5 * s], 6), O(6.2, -27.8, .7, .7)], .4)
    l.masa(tubo(P([(-7, -19), (-7.6, -23.4), (-2.4, -27.8), (5.6, -28)]), [.9 * s, .8 * s, .7 * s, .6 * s], 8), material='oscuro', alto=.3,
           brillo=.3, vientre=0, hondo=0, linea=.3)                      # el brazo de él, que sube hasta la mano de ella
    l.masa([forma(P([(1.6, -23.4), (1.8, -25.4), (3.6, -26.2), (5.6, -25.4), (5.8, -23.2), (4.6, -24.4), (2.8, -24.6)]), 2), O(5.6, -25.8, 1.2, 1.1)],
           material='oscuro', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.3)       # el pelo recogido
    l.mancha(O(2.8, -23.6, .24, .28), '05201C', 1)
    l.trazo(P([(2.2, -22.2), (2.8, -21.9), (3.4, -22.2)]), .14 * s, color='0C3A33', alfa=.9)
    return v


def nota(l, x, y, s=1.0, doble=False):
    """una nota musical: la cabeza redonda y la plica, y una o dos corcheas"""
    piezas = [ovalo(x, y, 1 * s, .75 * s, -20), box(x + .75 * s, y - 5 * s, x + 1.1 * s, y)]
    if doble:
        piezas += [ovalo(x + 4 * s, y - .6 * s, 1 * s, .75 * s, -20), box(x + 4.75 * s, y - 5.6 * s, x + 5.1 * s, y - .6 * s),
                   Polygon([(x + .75 * s, y - 5 * s), (x + 5.1 * s, y - 5.6 * s), (x + 5.1 * s, y - 4.6 * s), (x + .75 * s, y - 4 * s)])]
    else:
        piezas.append(tubo([(x + 1, y - 5 * s), (x + 2.6 * s, y - 3.4 * s), (x + 2.4 * s, y - 1.6 * s)], [.4 * s, .3 * s, .1 * s], 5))
    l.masa(piezas, material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.2)


def viena(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 30, 4.4, 14, .5)
    # atrás: la ciudad, con la catedral de San Esteban (la torre alta y el techo de tejas a rombos) y la noria del Prater
    prado(l, 18, 24, .2)
    casitas(l, -1, 122, 20, 4.4, semilla=8)
    d = piedra(l, [box(14, 10.4, 34, 19.6), Polygon([(13.4, 10.6), (24, 4.6), (34.6, 10.6)]), box(8, 6.4, 12.4, 19.6),
                   Polygon([(7.8, 6.6), (10.2, -3.4), (12.6, 6.6)])], .2)
    for k in range(5):                                                   # los rombos del techo de tejas
        for j in range(3):
            cx, cy = 16.4 + k * 3.8 + (j % 2) * 1.9, 9.4 - j * 1.4 + abs(k - 2) * .4
            l.mancha(Polygon([(cx, cy - .6), (cx + .9, cy), (cx, cy + .6), (cx - .9, cy)]), '1C6659', .7, dentro=d)
    n0 = (96, 9.6)
    r = 8.4
    l.masa(ovalo(*n0, r, r).difference(ovalo(*n0, r - .6, r - .6)), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    for a in range(0, 360, 30):                                          # los rayos y las cabinas de la noria
        px, py = n0[0] + r * math.cos(math.radians(a)), n0[1] + r * math.sin(math.radians(a))
        l.trazo([n0, (px, py)], .12, color='8EB5AA', alfa=.9)
        l.masa(box(px - .7, py - .4, px + .7, py + .8), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2, arroja=False)
    l.masa([Polygon([(n0[0] - 5, 19.6), (n0[0], n0[1]), (n0[0] + 5, 19.6), (n0[0] + 4, 19.6), (n0[0], n0[1] + 1.4), (n0[0] - 4, 19.6)])],
           material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    # el río café, ancho, adelante
    a = rio(l, 22.6)
    l.mancha(box(-2, 22, 122, 41), CAFE, .62, dentro=a)
    for _ in range(14):
        x, y = rng.uniform(2, 116), rng.uniform(25, 39)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='D8C49A', alfa=.6)
    # la pareja que baila el vals sobre el agua, protagonista, con sus ondas, su reflejo y las notas
    for k in range(3):
        l.trazo([(61 + (8 + k * 3) * math.cos(t), 35.4 + (1.2 + k * .6) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 31)], .16, color='E8DDBE',
                alfa=.7 - k * .15)
    v = pareja(l, 60, 35, 1.12)
    reflejo(l, v.g, 35.6, .3, "E8DDBE")
    for x, y, s, doble in ((34, 18, .9, False), (82, 14.6, .9, True), (90, 26, .8, False), (28, 28, .8, True)):
        nota(l, x, y, s, doble)


# ------------------------------------------------------------------------------------------------ Bratislava
def hermano(l, x, base, alto_, brazo, pelo, semilla=0):
    """un hermano de frente, contento, con la camiseta dorada; `brazo` es la mano que señala (la otra le abraza el hombro al hermano)"""
    s = alto_ / 20
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-1.8, -.3, 1.3, .6), O(1.8, -.3, 1.3, .6)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.masa([tubo(P([(-1.3, -8), (-1.5, -4), (-1.8, -.6)]), [1.2 * s, 1.1 * s, 1 * s], 5), tubo(P([(1.3, -8), (1.5, -4), (1.8, -.6)]), [1.2 * s, 1.1 * s, 1 * s], 5)],
           material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)              # el pantalón
    hx, hy = brazo
    piel(l, [tubo([(x + (2.6 if hx > x else -2.6) * s, base - 14.4 * s), ((x + hx) / 2, (base - 14.4 * s + hy) / 2 - 1), (hx, hy)], [.8 * s, .7 * s, .6 * s], 6),
             ovalo(hx, hy, .85 * s, .8 * s), O(0, -19, 2.8, 3), box(x - .8 * s, base - 16.6 * s, x + .8 * s, base - 15 * s)], .45)
    c = l.masa(forma(P([(-2.8, -15.6), (2.8, -15.6), (3.4, -12.4), (3, -7.6), (-3, -7.6), (-3.4, -12.4)]), 1), material='acento', alto=.4,
               brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo(P([(-1, -15.4), (0, -14.4), (1, -15.4)]), .18 * s, color='6B4E10', alfa=.6, dentro=c)
    for dx in (-1, 1):
        l.mancha(O(dx, -19.4, .32, .36), '05201C', 1)
    l.trazo(P([(-1.2, -17.6), (0, -16.9), (1.2, -17.6)]), .2 * s, color='0C3A33', alfa=.9)
    if pelo == 'liso':
        l.masa(forma(P([(-2.9, -19.4), (-2.8, -21.6), (-1.2, -22.6), (1.4, -22.6), (2.9, -21.4), (2.9, -19.4), (1.6, -21.2), (-1.4, -21)]), 2),
               material='oscuro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.3)
    else:
        l.masa([O(dx, -21.6 + dy, 1.1, 1) for dx, dy in ((-2.2, .8), (-1.2, -.4), (0, -.8), (1.2, -.4), (2.2, .8))], material='oscuro', alto=.4,
               brillo=.25, vientre=0, hondo=0, linea=.3)
    return c


def bratislava(l):
    cielo(l, sol=None)
    nube(l, 40, 4, 12, .5)
    # río arriba, lejos a la izquierda, Viena con su torre; a la derecha, en su colina, el castillo blanco de cuatro torres y el puente
    # del platillo volador; el río en medio
    prado(l, 17, 26, .2)
    l.masa(forma([(64, 18), (72, 13.4), (84, 11.6), (96, 12.4), (106, 15.6), (112, 18)], 2), material='cuerpo', alto=.3, brillo=.1, vientre=0,
           hondo=0, linea=.3)
    cas = l.masa([box(80, 6.4, 98, 12.6), box(79.4, 3.6, 82.4, 12.6), box(95.6, 3.6, 98.6, 12.6)], material='claro', alto=.3, brillo=.2, vientre=0,
                 hondo=0, linea=.35)
    for x0 in (79, 95.2):
        l.masa(Polygon([(x0, 3.8), (x0 + 1.9, 1.6), (x0 + 3.8, 3.8)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    l.masa(Polygon([(82, 6.6), (89, 4.2), (96, 6.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    for x in np.arange(83.6, 95, 2.2):
        l.mancha(box(x, 8.4, x + .9, 10), '164F46', .75, dentro=cas)
    casitas(l, 22, 64, 18.4, 3.4, semilla=9)
    l.masa([box(6.6, 9.4, 9.4, 18.4), Polygon([(6.4, 9.6), (8, 3.4), (9.6, 9.6)])], material='claro', alto=.25, brillo=.1, vientre=0, hondo=0,
           linea=.3)                                                     # la torre de San Esteban, en Viena, lejos
    casitas(l, -1, 20, 18.4, 2.6, semilla=10)
    rio(l, 19.4)
    l.masa(box(98, 18.6, 122, 19.8), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)   # el puente
    l.masa([Polygon([(104, 19.2), (106.4, 9.6), (107.6, 9.6), (106.4, 19.2)]), ovalo(107.4, 9, 2.8, 1)], material='claro', alto=.3, brillo=.2,
           vientre=0, hondo=0, linea=.3)                                 # el pilón y el platillo
    for k in range(5):
        l.trazo([(106.6, 11 + k * 1.6), (100 + k * 4.4, 18.8)], .1, color='8EB5AA', alfa=.9)
    # la orilla de adelante y los dos hermanos abrazados, protagonistas: el mayor señala a Viena, el menor al castillo
    m = orilla(l, forma([(-2, 41.5), (-2, 27.6), (40, 26.6), (80, 26.6), (122, 27.6), (122, 41.5)], 2), tinte=.24)
    pasto(l, 0, 120, 28, 40.6, 22, semilla=11, dentro=m)
    hermano(l, 52.6, 38.6, 26, (41.4, 13), 'liso')
    hermano(l, 67.4, 38.6, 22, (79.6, 15.4), 'rizos')
    piel(l, [tubo([(55.8, 20.4), (60.4, 20.6), (64, 22.2)], [1, .9, .8], 6), ovalo(64.4, 22.6, .95, .9)], .45)   # el brazo del mayor en el hombro del menor


# ------------------------------------------------------------------------------------------------ Budapest
def budapest(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 52, 4, 12, .45)
    # Buda, a la izquierda, arriba en su colina, con el castillo de cúpula
    l.masa(forma([(-2, 8), (10, 6.6), (24, 8), (34, 12.6), (42, 20.4), (46, 25), (-2, 25)], 2), material='cuerpo', alto=.35, brillo=.1, vientre=0,
           hondo=0, linea=.35)
    cas = piedra(l, [box(2, 3.6, 30, 8.6), box(12.6, 1.4, 19.4, 4), ovalo(16, 1.6, 3, 2.4)], .2)
    for x in np.arange(3.4, 29, 2.2):
        l.mancha(box(x, 5, x + .9, 7), '164F46', .7, dentro=cas)
    for _ in range(18):                                                  # las casas de la ladera
        x = rng.uniform(2, 40)
        y = 10 + (x - 2) * .34 + rng.uniform(0, 6)
        if y > 23:
            continue
        l.masa(box(x - 1, y - 1.4, x + 1, y), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
    # Pest, a la derecha, abajo en el llano, con el Parlamento de torres finas y cúpula
    prado(l, 19, 25, .2)
    par = l.masa([box(78, 14.6, 122, 20.6), box(95, 9.6, 105, 15), ovalo(100, 9.8, 4, 3.4)], material='claro', alto=.3, brillo=.15, vientre=0,
                 hondo=0, linea=.35)
    for x in np.arange(79, 121, 1.6):
        l.trazo([(x, 16), (x, 19.6)], .3, color='8EB5AA', alfa=.8, dentro=par)
    for x in list(np.arange(80, 94, 3.4)) + list(np.arange(107, 121, 3.4)) + [100]:
        y0 = 14.8 if x != 100 else 6.6
        l.masa(Polygon([(x - .5, y0), (x, y0 - 3.4), (x + .5, y0)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)
    # el río en medio
    rio(l, 21.6)
    # el Puente de las Cadenas, protagonista: el tablero, las dos torres de piedra en arco y las cadenas doradas, que cuelgan entre las
    # torres y bajan de cada torre a su orilla
    def cadena(x):
        if 38 <= x <= 82:
            return 25.6 - 12 * ((x - 60) / 22) ** 2
        return 13.6 + 12.4 * (abs(x - (38 if x < 38 else 82)) / 40) ** .7
    tablero = box(-2, 27, 122, 28.6)
    torres = []
    for cx in (38, 82):
        t = box(cx - 4.6, 12.4, cx + 4.6, 31.6).difference(forma([(cx - 2.4, 31.8), (cx - 2.4, 21), (cx, 18.4), (cx + 2.4, 21), (cx + 2.4, 31.8)], 2))
        torres.append(t)
    piedra(l, tablero, .25, .35)
    for x in np.arange(-2, 122, 3):                                      # los tirantes
        if any(abs(x - cx) < 5 for cx in (38, 82)):
            continue
        l.trazo([(x, cadena(x)), (x, 27)], .14, color='6B4E10', alfa=.8)
    for cx in (38, 82):
        piedra(l, [torres[(cx > 60) * 1], box(cx - 5.4, 11.6, cx + 5.4, 13.2)], .35, .45, .3)
    cadenas = [cinta([(x, cadena(x)) for x in np.linspace(a, b, 30)], [1.1] * 30, 4) for a, b in ((38, 82), (38, -2), (82, 122))]
    c = l.masa(cadenas, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for g in cadenas:                                                    # los eslabones
        x0, y0, x1, y1 = g.bounds
        for x in np.arange(x0, x1, 1.6):
            l.trazo([(x, y0 - 2), (x, y1 + 2)], .12, color='6B4E10', alfa=.55, dentro=c)
    reflejo(l, unary_union(torres), 31.4, .25)
    l.mancha(box(-2, 28.6, 122, 41), '0C3A33', .08)


# ------------------------------------------------------------------------------------------------ Belgrado
def vencedor(l, x, base, s=1.0, columna=9.0):
    """el Vencedor de Kalemegdan, dorado, en su columna: un hombre de pie que mira a la confluencia, con un halcón en la mano levantada
    y la espada en la otra; (x, base) es el pie de la columna"""
    pie = base - (columna + 1.2) * s
    P = lambda pts: [(x + u * s, pie + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, pie + v * s, rx * s, ry * s, a)
    piedra(l, [box(x - 1.4 * s, base - 1.4 * s, x + 1.4 * s, base), box(x - .9 * s, pie + .9 * s, x + .9 * s, base - 1.2 * s),
               box(x - 1.3 * s, pie, x + 1.3 * s, pie + 1 * s)], .1, .35)
    cuerpo = [tubo(P([(-.6, -4.2), (-.8, -2), (-.7, 0)]), [.6 * s, .55 * s, .5 * s], 4), tubo(P([(.6, -4.2), (.8, -2), (.9, 0)]), [.6 * s, .55 * s, .5 * s], 4),
              forma(P([(-1.3, -8.8), (1.3, -8.8), (1.4, -5.8), (1, -4), (-1, -4), (-1.4, -5.8)]), 1), O(0, -10.1, 1.05, 1.15),
              tubo(P([(1.2, -8.4), (2.8, -9.8), (3.6, -11.4)]), [.45 * s, .4 * s, .35 * s], 5),
              tubo(P([(-1.2, -8.4), (-2.1, -6.4), (-2.3, -5)]), [.45 * s, .4 * s, .35 * s], 5),
              Polygon(P([(-2.5, -5.2), (-2.1, -5.2), (-2.7, -.8), (-3, -.8)])),
              O(3.8, -12.2, 1, .7), Polygon(P([(3.2, -12.4), (2.2, -14.2), (5, -12.8)]))]
    return l.masa(cuerpo, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)


def belgrado(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.6, 12, .45)
    # la tierra, y la ciudad blanca detrás, de los dos lados del Sava
    prado(l, 12, 41, .22)
    for _ in range(70):
        x, h = rng.uniform(-1, 121), rng.uniform(3, 9)
        if 50 < x < 64 and rng.random() < .7:
            continue
        l.masa(box(x - 1.6, 16.4 - h, x + 1.6, 16.6), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.22, arroja=False)
    # los dos ríos: el Sava, que baja en diagonal desde atrás a la izquierda, y el Danubio, ancho, que corre adelante; se juntan al pie
    # de la punta
    sava = cinta([(-2, 17.4), (14, 19.6), (30, 23.4), (44, 27.4), (56, 30.6)], [5, 6, 7, 8.4, 10], 8)
    danubio = cinta([(-2, 34.6), (30, 34.4), (60, 34.8), (90, 35.4), (124, 36)], [11, 11.4, 11.8, 12, 12], 8)
    a = agua(l, unary_union([sava, danubio]).buffer(.3).buffer(-.3), ondas=14, semilla=3, linea=.35)
    l.mancha(sava, '9BDDBD', .3, dentro=a, difuso=1.2)
    l.mancha(danubio, AZUL, .25, dentro=a, difuso=1.2)
    # la punta de Kalemegdan, entre los dos ríos: la colina verde con sus árboles
    colina = forma([(50, 29.2), (54, 25.6), (62, 21.4), (76, 18.2), (96, 16.8), (124, 16.4), (124, 29.6), (90, 29.4), (66, 29.6)], 2)
    l.masa(colina, material='cuerpo', alto=.35, brillo=.1, vientre=0, hondo=.1, linea=.4, contraluz=.3)
    for _ in range(18):
        x, y = rng.uniform(60, 120), rng.uniform(24.6, 28.6)
        if colina.buffer(-1).contains(ovalo(x, y, 1, .8)):
            arbol(l, x, y - .6, 1.2, material='lejos', semilla=int(x))
    # la fortaleza blanca, sobre la colina: la muralla con sus torres almenadas y su puerta
    muro = [Polygon([(64, 25.4), (68, 20.4), (116, 19.4), (118, 24.6)])]
    torres = (69, 80, 91, 102, 113)
    for x in torres:
        muro.append(box(x - 2.2, 15.6, x + 2.2, 24))
    f = l.masa(muro, material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
    for x in torres:                                                     # las almenas y las troneras
        for dx in (-1.5, 0, 1.5):
            l.mancha(box(x + dx - .4, 15.5, x + dx + .4, 16.4), CIELO, 1, dentro=f)
        l.mancha(box(x - .3, 18, x + .3, 19.6), '164F46', .7, dentro=f)
    for x in np.arange(70.6, 116, 2.2):
        l.mancha(box(x, 19.3, x + 1, 20.2), CIELO, 1, dentro=f)
    l.mancha(forma([(84.4, 24.4), (84.4, 21.2), (86, 19.8), (87.6, 21.2), (87.6, 24.4)], 1), '164F46', .85, dentro=f)   # la puerta
    reflejo(l, colina, 29.6, .16)
    # el Vencedor, dorado, en su columna en la punta, protagonista: mira a la confluencia, donde el Sava entra al Danubio
    vencedor(l, 60, 27.4, 1.1, 4.4)



# ------------------------------------------------------------------------------------------------ el mar
def pelicano_blanco(l, x, y, s=1.0, lado=1, alas=False):
    """un pelícano blanco que nada, de perfil: el cuerpo grande y blanco, el cuello grueso y corto, la cabeza chica y el pico enorme, largo
    y chato, con la bolsa dorada colgando debajo, que es lo que lo distingue; con `alas`, las abre; (x, y) es la línea del agua"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + lado * u * s, y + v * s, rx * s, ry * s, a * lado)
    if alas:
        l.masa([forma(P([(-1, -3.6), (-5, -9.4), (-10.6, -11), (-9, -7.4), (-5, -3.8)]), 2), forma(P([(.6, -4), (1, -9.6), (4, -12.4), (4, -8.4), (2.6, -4)]), 2)],
               material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(Polygon(P([(-10.6, -11), (-8, -10.6), (-9, -7.4)])), '0C3A33', .8)
    c = l.masa([O(-1.4, -2.4, 5.8, 2.8), tubo(P([(2.8, -3.6), (3.8, -5.6), (3.4, -7.4), (3.9, -8.6)]), [1.9 * s, 1.5 * s, 1.3 * s, 1.3 * s], 8),
                O(4.1, -9, 1.6, 1.4)], material='claro', alto=.45, brillo=.25, vientre=0, hondo=.1, linea=.35, contraluz=.3)
    l.mancha(O(-5, -2.8, 1.8, 1), '9DB9B0', .5, dentro=c)
    l.masa(forma(P([(3, -10.2), (1.2, -10), (2.6, -9.4)]), 1), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2)   # el copete
    pico = [forma(P([(5, -9.8), (14.6, -6.8), (15.2, -6.1), (14.4, -5.8), (5.2, -8)]), 1), forma(P([(5.2, -8), (14.2, -5.9), (12, -3.8), (8.6, -3), (6, -5)]), 2)]
    b = l.masa(pico, material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.trazo(P([(5.2, -8), (14.2, -5.9)]), .14 * s, color='6B4E10', alfa=.75, dentro=b)
    l.mancha(O(4.6, -9.4, .32, .32), '05201C', 1)
    return c


def mar(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    nube(l, 28, 6, 16, .5)
    nube(l, 92, 5, 12, .4)
    # el mar Negro: oscuro como su nombre, hasta el horizonte
    horizonte = 19
    m = l.masa(box(-2, horizonte, 122, 41.5), material='oscuro', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, 41.5), '05201C', .55, dentro=m)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.6), '3E7A6D', .5, dentro=m, difuso=.6)
    for _ in range(22):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='3E7A6D', alfa=.8)
    # el viejo faro de Sulina, lejos, en la boca del brazo del medio
    l.masa(forma([(2, horizonte + .4), (8, horizonte - .6), (20, horizonte - .4), (24, horizonte + .6)], 1), material='cuerpo', alto=.15, brillo=0,
           vientre=0, hondo=0, linea=.3)
    l.masa([forma([(11.4, horizonte - .4), (11.8, 10.6), (14.2, 10.6), (14.6, horizonte - .4)], 0), box(11, 9.4, 15, 10.8)], material='claro',
           alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(11.4, 9.6), (13, 7.8), (14.6, 9.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # los juncales del delta, a los costados, el mayor juncal del mundo
    for x0, x1, y in ((-2, 30, 34), (-2, 16, 40.6), (94, 122, 31), (104, 122, 40)):
        juncos(l, x0, x1, y, 6, int((x1 - x0) * 1.8), semilla=int(x0 + y))
    for x, y, s in ((40, 8, .8), (52, 6, .6), (84, 9, .7)):
        ave(l, x, y, s)
    # los pelícanos blancos, protagonistas, que nadan juntos en el agua negra
    for x, y, s, lado, alas in ((18, 30.6, .95, 1, False), (36, 36.8, 1.15, 1, False), (56, 31, 1, 1, False), (84, 36.6, 1.15, -1, False),
                                (102, 30.8, .95, -1, False)):
        g = pelicano_blanco(l, x, y, s, lado, alas)
        reflejo(l, g.g, y + .2, .35, "FFFFFF")


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Ulm', dibujar=ulm), dict(clave='Ratisbona', dibujar=ratisbona),
            dict(clave='Passau', dibujar=passau), dict(clave='Linz', dibujar=linz), dict(clave='Viena', dibujar=viena),
            dict(clave='Bratislava', dibujar=bratislava), dict(clave='Budapest', dibujar=budapest), dict(clave='Belgrado', dibujar=belgrado),
            dict(clave='mar', dibujar=mar)]
LISTO = True
