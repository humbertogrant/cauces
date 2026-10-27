# -*- coding: utf-8 -*-
"""Las postales del Orinoco, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: visto desde arriba, el Orinoco que baja de la sierra Parima entre la selva y, al medio, el Casiquiare, dorado, el canal
  natural por donde le presta agua al río Negro y al Amazonas;
- San Fernando de Atabapo: «un pescador llamado Fernando sirve té negro en tazas de arena blanca»: en la playa blanca, el pescador sirve
  el té de una tetera dorada en tazas de arena; atrás, el agua negra del Atabapo que se junta con la parda del Orinoco;
- Puerto Ayacucho: «un puerto lleno de ayes: el agua grita al saltar los raudales y los barcos se bajan a caminar»: los raudales, entre
  las rocas, gritan ¡AY!, y las curiaras doradas se bajan del agua y caminan por la carretera que los rodea;
- Puerto Carreño: «un carro con carreta cruza el río con una meta pintada en la espalda»: el carro dorado, con su carreta, cruza el
  río con la bandera a cuadros de la meta pintada atrás; enfrente, Venezuela;
- Caicara del Orinoco: «un caimán dobla el río hacia el este con la cola y cuenta semillas de sarrapia»: visto desde arriba, el caimán
  dorado, echado en la curva, que la dobla con la cola, con las semillas en la mano y el olor a vainilla;
- Ciudad Bolívar: «Bolívar aprieta el río con las dos manos hasta dejarlo angosto»: Bolívar, de casaca dorada, aprieta el río entre sus
  manos, y por la angostura pasa el puente colgante; en la orilla, la botella de amargo de Angostura;
- Ciudad Guayana: «dos ríos de colores corren juntos sin mezclarse, como café y té, y una guayaba de acero brilla en el muelle»: la
  guayaba dorada, en el muelle, con las grúas y la acería; el Caroní oscuro y el Orinoco pardo, juntos y sin mezclarse;
- el mar: el delta, visto desde arriba, abierto como un abanico dorado cuyos pliegues son los caños, hacia el Atlántico de los barcos
  grandes; una casa de palafito de los waraos (la curiara se queda en los caños).
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
PARDO = 'BF9129'           # el agua parda del Orinoco
NEGRO = '1E1A10'           # el agua negra, color té, del Atabapo y del Caroní


def piel(l, piezas, tono=.6, color=PIEL):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), color, tono, dentro=m)
    return m


def agua_color(l, g, color, alfa, ondas=0, semilla=0):
    m = agua(l, g, ondas=ondas, semilla=semilla, linea=.3)
    l.mancha(g, color, alfa, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 22, 3, 12, .4)
    # visto desde arriba: la selva, y arriba a la derecha la sierra Parima, de donde baja el Orinoco
    tierra(l, 5, 41, desierto=.1)
    l.mancha(box(-2, 5, 122, 41.6), '1C6659', .55)
    for _ in range(160):                                                 # las copas de la selva, vistas desde arriba
        x, y = rng.uniform(-2, 122), rng.uniform(6, 41)
        l.mancha(ovalo(x, y, rng.uniform(1.4, 2.6), rng.uniform(1.1, 2)), str(rng.choice(['2F8A74', '164F46', '4AA189'])), .7)
    for x0 in (90, 104, 114):
        l.masa(forma([(x0 - 8, 12), (x0 - 2, 6), (x0 + 2, 5.4), (x0 + 8, 11), (x0 + 4, 14), (x0 - 4, 14)], 2), material='lejos', alto=.4, brillo=.15,
               vientre=0, hondo=.1, linea=.3)
    # el Orinoco, que baja de la sierra y se va hacia la izquierda; el río Negro, oscuro, abajo, que se va al Amazonas
    orinoco_ = cinta([(102, 13), (86, 15.4), (64, 14), (40, 13.6), (14, 12), (-2, 12.6)], [1.6, 2.6, 3.4, 4, 4.6, 5], 8)
    negro = cinta([(-2, 34), (24, 33), (50, 34.6), (80, 33.4), (124, 34)], [4.4, 5, 5.4, 6, 6.6], 8)
    agua_color(l, orinoco_, PARDO, .5, ondas=4, semilla=2)
    agua_color(l, negro, NEGRO, .55, ondas=4, semilla=3)
    # el Casiquiare, dorado, protagonista: el canal natural que baja del Orinoco al río Negro
    canal = cinta([(44, 14), (48, 19), (58, 22), (66, 26), (70, 31.6), (72, 33.6)], [3.4, 3.4, 3.4, 3.6, 3.8, 4], 8)
    m = l.masa(canal, material='acento', alto=.15, brillo=.35, vientre=0, hondo=0, linea=.45, escalon=0, contraluz=.3, arroja=False)
    for t in np.linspace(.12, .88, 7):                                   # la corriente, que baja hacia el río Negro
        c = curva([(44, 14), (48, 19), (58, 22), (66, 26), (70, 31.6), (72, 33.6)], 10)
        i = int(t * (len(c) - 1))
        x, y = c[i]
        d = c[min(i + 1, len(c) - 1)] - c[i]
        d = d / (np.hypot(*d) or 1)
        l.trazo([(x - d[0] - d[1] * .8, y - d[1] + d[0] * .8), (x + d[0] * .6, y + d[1] * .6), (x - d[0] + d[1] * .8, y - d[1] - d[0] * .8)], .2,
                color='6B4E10', alfa=.8, dentro=m)


# ------------------------------------------------------------------------------------------------ San Fernando de Atabapo
def tetera(l, x, y, s=1.0):
    """una tetera dorada, inclinada para servir: el cuerpo redondo, la tapa, el asa y el pico; devuelve la punta del pico"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    g = unary_union([ovalo(x, y, 4 * s, 3.2 * s), forma(P([(-1.8, -3), (-1.4, -4.2), (1.4, -4.2), (1.8, -3)]), 1), ovalo(x, y - 4.6 * s, .7 * s, .6 * s),
                     tubo(P([(-3.8, -1.6), (-6.4, -2), (-6.6, 1), (-3.8, 1.4)]), [.6 * s] * 4, 6),
                     tubo(P([(3.6, .6), (6, -.6), (8, -2.6)]), [1 * s, .7 * s, .5 * s], 5)])
    g = affinity.rotate(g, 22, origin=(x, y))
    m = l.masa(g, material='acento', alto=.55, brillo=.55, vientre=0, hondo=0, linea=.45, contraluz=.45)
    l.trazo([(x - 2.4 * s, y - 1 * s), (x - 1 * s, y - 2.2 * s)], [.05, .3, .05], color='FBEFCB', alfa=.85, dentro=m)
    p = affinity.rotate(Polygon(P([(8, -2.6), (8.1, -2.6), (8, -2.5)])), 22, origin=(x, y)).exterior.coords[0]
    return p


def san_fernando(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # atrás, la selva de la otra orilla, que ya es Colombia; el agua negra del Atabapo y la parda del Orinoco que se juntan
    selva(l, -2, 122, 15, 5, semilla=4, emergentes=3)
    agua(l, box(-2, 14.6, 122, 28), ondas=0, linea=0)
    l.mancha(Polygon([(-2, 14.6), (64, 14.6), (52, 28), (-2, 28)]), NEGRO, .6, difuso=2)
    l.mancha(Polygon([(64, 14.6), (122, 14.6), (122, 28), (52, 28)]), PARDO, .45, difuso=2)
    # la playa blanca de adelante, las tazas de arena, y el pescador, con la tetera dorada, protagonista
    playa = forma([(-2, 41.6), (-2, 27.4), (30, 26.6), (60, 26.4), (90, 26.6), (122, 27.4), (122, 41.6)], 2)
    l.masa(playa, material='claro', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.35)
    for x in (70, 80, 90):                                               # las tazas de arena blanca, con el té negro adentro
        t = l.masa([forma([(x - 3, 33), (x - 2.4, 37.4), (x + 2.4, 37.4), (x + 3, 33)], 1), ovalo(x, 33, 3, .8)], material='claro', alto=.5, brillo=.3,
                   vientre=0, hondo=0, linea=.35)
        l.mancha(ovalo(x, 33.1, 2.4, .55), NEGRO, .85)
        for k in range(6):
            l.mancha(ovalo(x - 2 + k * .8, 35 + (k % 2) * 1.2, .2, .2), 'D8C49A', .9)       # los granitos de arena
    x, b = 46, 38.6                                                      # el pescador Fernando, con su sombrero
    piel(l, [tubo([(x - 1, b - 7), (x - 1.4, b - 3.6), (x - 1.8, b)], [.8, .7, .6], 5), tubo([(x + 1, b - 7), (x + 1.6, b - 3.6), (x + 2, b)], [.8, .7, .6], 5),
             ovalo(x, b - 15, 2, 2.2), tubo([(x + 2, b - 12.4), (x + 5, b - 13.6), (x + 7.4, b - 15.4)], [.65, .55, .5], 5)])
    l.masa(forma([(x - 2.6, b - 13), (x + 2.6, b - 13), (x + 3, b - 6.4), (x - 3, b - 6.4)], 1), material='claro', alto=.35, brillo=.25, vientre=0,
           hondo=0, linea=.35)
    l.masa(forma([(x - 2.4, b - 7), (x + 2.6, b - 7), (x + 2.8, b - 4), (x - 2.8, b - 4)], 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.3)
    l.masa([ovalo(x, b - 16.6, 4.4, .8), forma([(x - 2.2, b - 16.6), (x - 1.8, b - 18.8), (x + 1.8, b - 18.8), (x + 2.2, b - 16.6)], 1)], material='vientre',
           alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(x + .8, b - 15.2, .26, .3), '05201C', 1)
    px, py = tetera(l, x + 11.4, b - 17, 1.15)
    l.trazo([(px, py), (px + 2, py + 6), (69.6, 32.8)], [.5, .4, .3], color=NEGRO, alfa=.9)        # el chorro de té negro


# ------------------------------------------------------------------------------------------------ Puerto Ayacucho
def letras_ay(l, x, y, h):
    """el grito ¡AY!, en letras blancas con borde"""
    g = .2 * h
    a = Polygon([(x, y), (x + .3 * h, y - h), (x + .44 * h, y - h), (x + .74 * h, y)]).difference(
        Polygon([(x + .29 * h, y - .36 * h), (x + .37 * h, y - .66 * h), (x + .45 * h, y - .36 * h)])).difference(
        Polygon([(x + .2 * h, y + .1), (x + .37 * h, y - .22 * h), (x + .54 * h, y + .1)]))
    x2 = x + .84 * h
    ye = unary_union([Polygon([(x2, y - h), (x2 + g * 1.1, y - h), (x2 + .36 * h, y - .5 * h), (x2 + .36 * h - g * .5, y - .4 * h)]),
                      Polygon([(x2 + .72 * h, y - h), (x2 + .72 * h - g * 1.1, y - h), (x2 + .36 * h, y - .5 * h), (x2 + .36 * h + g * .5, y - .4 * h)]),
                      box(x2 + .36 * h - g / 2, y - .5 * h, x2 + .36 * h + g / 2, y)])
    ex = unary_union([box(x2 + .86 * h, y - h, x2 + .86 * h + g, y - .3 * h), box(x2 + .86 * h, y - .16 * h, x2 + .86 * h + g, y)])
    g_ = unary_union([a, ye, ex])
    l.masa(g_.buffer(.15), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35)
    return g_


def curiara_caminante(l, x, base, s=1.0, paso=0):
    """una curiara dorada que se bajó del agua y camina por la carretera con sus patitas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    for k, u in enumerate((-4, -1.4, 1.4, 4)):                           # las patitas, que van y vienen
        d = (1 if (k + paso) % 2 else -1) * .9
        l.trazo(P([(u, -2.8), (u + d * .5, -1.4), (u + d, 0)]), .35 * s, color='3A2A0A', alfa=.9)
        l.trazo(P([(u + d, 0), (u + d + .7, 0)]), .3 * s, color='3A2A0A', alfa=.9)
    c = l.masa(forma(P([(-8, -5.6), (-6, -3.4), (6, -3.4), (8, -5.6), (7.4, -3), (5.4, -2.2), (-5.4, -2.2), (-7.4, -3)]), 1), material='acento', alto=.45,
               brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.mancha(ovalo(x + 4.6 * s, base - 3.6 * s, .3 * s, .35 * s), '05201C', 1)
    l.trazo(P([(3.4, -2.8), (4.2, -2.5), (5, -2.8)]), .12 * s, color='0C3A33', alfa=.9, dentro=c)
    return c


def puerto_ayacucho(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # los raudales de Atures: el río que salta entre las rocas negras, todo espuma
    selva(l, -2, 122, 13, 5, semilla=6, emergentes=2)
    agua(l, box(-2, 12.6, 122, 26), ondas=0, linea=0)
    for _ in range(26):                                                  # las rocas
        x, y = rng.uniform(0, 120), rng.uniform(14, 25)
        l.masa(ovalo(x, y, rng.uniform(1.6, 3.4), rng.uniform(1, 1.8)), material='oscuro', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.3, arroja=False)
    for _ in range(46):                                                  # la espuma que salta
        x, y = rng.uniform(0, 120), rng.uniform(13, 26)
        l.trazo([(x, y), (x + 1.4, y - 1.2), (x + 2.8, y)], .5, color='FFFFFF', alfa=.85)
    # los gritos: ¡AY!
    for x, y, h in ((14, 10.6, 5), (82, 9.6, 6)):
        globo = forma([(x - 2, y - h - 1.6), (x + h * 2.2, y - h - 1.6), (x + h * 2.2, y + 1.4), (x + 3, y + 1.4), (x + 1, y + 3.6), (x + 1.4, y + 1.4),
                       (x - 2, y + 1.4)], 1)
        l.masa(globo, material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
        letras_ay(l, x, y, h)
    # la carretera que rodea los raudales, y las curiaras doradas, protagonistas, que se bajaron a caminar por ella
    camino = forma([(-2, 41.6), (-2, 29), (40, 27.6), (80, 27.6), (122, 29), (122, 41.6)], 2)
    c = l.masa(camino, material='vientre', alto=.1, brillo=.05, vientre=0, hondo=0, linea=.35)
    l.mancha(camino, 'D8C49A', .45, dentro=c)
    for x in np.arange(4, 120, 9):
        l.trazo([(x, 34.6), (x + 4.6, 34.6)], .5, color='FFFFFF', alfa=.85, dentro=c)
    for k, (x, s) in enumerate(((28, 1.05), (60, 1.25), (92, 1.05))):
        curiara_caminante(l, x, 33.6 + (k % 2) * 1.4, s, k)


# ------------------------------------------------------------------------------------------------ Puerto Carreño
def carro(l, x, base, s=1.0):
    """el carro dorado, antiguo, de perfil, mirando a la izquierda, que tira de su carreta; atrás, la bandera a cuadros de la meta"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, r: ovalo(x + u * s, base + v * s, r * s, r * s)
    cuerpo = [forma(P([(-10, -2.4), (-10.6, -5), (-8, -6), (-5, -6.2), (-3.6, -10), (4, -10.4), (6, -6.4), (10, -6), (10.4, -2.4)]), 1)]
    c = l.masa(cuerpo, material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.mancha(Polygon(P([(-3, -9.4), (3.4, -9.6), (4.8, -6.8), (-4, -6.6)])), 'C6EEDC', .9, dentro=c)       # las ventanas
    l.trazo(P([(.4, -9.6), (.4, -6.6)]), .3 * s, color='6B4E10', alfa=.8, dentro=c)
    for i in range(4):                                                   # la meta pintada atrás: la bandera a cuadros
        for j in range(3):
            if (i + j) % 2 == 0:
                l.mancha(box(x + (6.6 + i * .9) * s, base - (6.1 - j * .9) * s, x + (7.5 + i * .9) * s, base - (5.2 - j * .9) * s), '0C3A33', .95, dentro=c)
            else:
                l.mancha(box(x + (6.6 + i * .9) * s, base - (6.1 - j * .9) * s, x + (7.5 + i * .9) * s, base - (5.2 - j * .9) * s), 'FFFFFF', .95, dentro=c)
    for u in (-6.4, 6.4):
        l.masa(O(u, -2.2, 2.2), material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)
        l.masa(O(u, -2.2, .8), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    # la carreta, atrás, con su lanza enganchada
    l.trazo(P([(10.4, -3.4), (14, -3.4)]), .3 * s, color='5A3E1E', alfa=.9)
    ct = l.masa(box(x + 14 * s, base - 6 * s, x + 22 * s, base - 2.6 * s), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(box(x + 13 * s, base - 7 * s, x + 23 * s, base - 2 * s), '8A6A3A', .6, dentro=ct)
    l.masa(O(18, -2, 2), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(O(18, -2, 2.4), '5A3E1E', .6)
    l.masa([O(16.4, -7.4, 1.6), O(19.6, -7.6, 1.6)], material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)   # los sacos
    return c


def puerto_carreno(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    nube(l, 98, 3.6, 10, .4)
    # enfrente, Venezuela; el río Meta que entra por la izquierda; los Llanos de pasto
    prado(l, 14, 20, .3)
    for x in (12, 30, 90, 108):
        arbol(l, x, 15.4, 1.6, semilla=x)
    agua(l, box(-2, 19.6, 122, 41.6), ondas=10, semilla=7, linea=0)
    l.mancha(cinta([(-2, 22), (20, 24), (40, 27)], [5, 6, 3], 6), PARDO, .45, difuso=1.4)
    # el carro dorado, protagonista, que cruza el río salpicando, con la meta pintada atrás
    for k in range(3):
        l.trazo([(46 + k * 3, 33.4 - k * .6), (40 + k * 2, 31.6 - k * 1.4)], .3, color='FFFFFF', alfa=.85)
    l.mancha(ovalo(58, 33.4, 18, 1.4), 'FFFFFF', .6, difuso=.5)
    carro(l, 54, 33.6, 1.3)
    reflejo(l, box(40, 20, 84, 33.6), 33.8, .15, 'F2D48A')


# ------------------------------------------------------------------------------------------------ Caicara del Orinoco
def caiman(l, s=1.0):
    """el caimán dorado, visto desde arriba, echado en la curva del río: la cabeza a la izquierda, las patas y la cola larga que dobla el
    río hacia el este; con las semillas de sarrapia en la mano"""
    eje = [(30, 22), (38, 21.4), (46, 21), (54, 22.4), (60, 25.6), (63, 30), (68, 33.6), (80, 35), (96, 34.4)]
    anchos = [2.4, 3.6, 4.4, 4.6, 4.2, 3.4, 2.6, 1.6, .4]
    cuerpo = [tubo(eje, anchos, 12), forma([(30, 20), (22, 20.6), (18, 21.6), (22, 23), (30, 24)], 1)]
    for (x, y), d in (((40, 19.4), (-1, -1)), ((40, 23.4), (-1, 1)), ((54, 20.2), (1, -1)), ((53, 25), (-1, 1))):
        cuerpo.append(tubo([(x, y), (x + d[0] * 2, y + d[1] * 2.6), (x + d[0] * 3.4, y + d[1] * 3)], [1, .8, .6], 4))
    m = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for k in range(1, len(eje) - 1):                                     # las escamas del lomo
        x, y = eje[k]
        l.trazo([(x - .8, y), (x + .8, y)], .2, color='6B4E10', alfa=.6, dentro=m)
    for dy in (-1.2, 1.2):
        l.mancha(ovalo(27, 22 + dy, .45, .4), '05201C', 1)
    for k in range(5):                                                   # las semillas de sarrapia, en la mano
        l.mancha(ovalo(34 + k * .9, 27.2 + (k % 2) * .6, .5, .3, 30), '3A2A0A', .95)
    for k in range(3):                                                   # el olor a vainilla
        l.trazo([(36 + k * 1.6, 25.6), (36.6 + k * 1.6, 24), (36 + k * 1.6, 22.4)], .14, color='FFFFFF', alfa=.7)


def caicara(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    nube(l, 30, 3, 12, .4)
    # visto desde arriba: los Llanos y el río que baja y en Caicara dobla hacia el este, siguiendo la cola del caimán
    tierra(l, 5, 41, desierto=.3)
    for _ in range(30):
        x, y = rng.uniform(0, 120), rng.uniform(6, 40)
        l.trazo([(x - .6, y), (x, y - .9), (x + .6, y)], .14, color='2F8A74', alfa=.55)
    rio_ = cinta([(40, 4), (44, 12), (50, 20), (58, 27), (68, 31), (84, 31.4), (124, 30)], [7, 8, 9, 10, 10.4, 10.4, 10.4], 10)
    agua_color(l, rio_, PARDO, .22, ondas=18, semilla=10)
    l.masa([box(96, 22, 116, 26), box(100, 20.4, 104, 22.2)], material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.25)  # el puerto
    caiman(l)


# ------------------------------------------------------------------------------------------------ Ciudad Bolívar
def bolivar(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # las orillas, y el río que se angosta entre las manos de Bolívar: Angostura
    prado(l, 26, 41, .26)
    rio_ = Polygon([(-2, 27), (40, 27.4), (56, 30), (64, 30), (80, 27.4), (122, 27), (122, 41.6), (80, 41.6), (64, 34.4), (56, 34.4), (40, 41.6),
                    (-2, 41.6)]).buffer(0)
    agua_color(l, rio_, PARDO, .2, ondas=12, semilla=11)
    # Bolívar, de casaca dorada, detrás del río, con los brazos que bajan y las manos que aprietan las dos orillas
    x = 60
    piel(l, [ovalo(x, 6.6, 3, 3.4), box(x - 1, 9.4, x + 1, 11.4)], .5, '93701A')
    l.masa(forma([(x - 3.2, 5.4), (x - 3, 3), (x - 1, 2), (x + 2, 2.2), (x + 3.4, 4), (x + 3.2, 6), (x + 2, 4.6), (x - 2, 4.6)], 1), material='oscuro',
           alto=.35, brillo=.3, vientre=0, hondo=0, linea=.3)           # el pelo
    l.masa([forma([(x - 3.2, 5), (x - 3.6, 9.6), (x - 2.6, 9)], 1), forma([(x + 3.2, 5), (x + 3.6, 9.6), (x + 2.6, 9)], 1)], material='oscuro', alto=.3,
           brillo=.3, vientre=0, hondo=0, linea=.25)                     # las patillas
    for dx in (-1.1, 1.1):
        l.mancha(ovalo(x + dx, 6.6, .3, .34), '05201C', 1)
    l.trazo([(x - 1, 8.8), (x, 8.6), (x + 1, 8.8)], .18, color='3A2A0A', alfa=.8)
    casaca = [forma([(x - 7, 26), (x - 7.6, 14), (x - 5, 11), (x + 5, 11), (x + 7.6, 14), (x + 7, 26)], 1),
              tubo([(x - 6.6, 13), (x - 13, 18), (x - 16, 27)], [2.2, 2, 1.8], 6), tubo([(x + 6.6, 13), (x + 13, 18), (x + 16, 27)], [2.2, 2, 1.8], 6)]
    c = l.masa(casaca, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for dx in (-6, 6):                                                   # las charreteras
        l.masa(ovalo(x + dx, 12, 2.2, 1), material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35)
        for k in range(5):
            l.trazo([(x + dx - 1.6 + k * .8, 12.6), (x + dx - 1.6 + k * .8, 14)], .16, color='6B4E10', alfa=.8)
    l.trazo([(x - 5, 12), (x + 5, 24)], .8, color='FBEFCB', alfa=.8, dentro=c)    # la banda
    for v in (15, 18, 21):
        l.mancha(ovalo(x, v, .4, .4), 'FBEFCB', .95, dentro=c)
    piel(l, [ovalo(x - 16.6, 28.4, 2.2, 1.6), ovalo(x + 16.6, 28.4, 2.2, 1.6)], .5, '93701A')     # las manos que aprietan las orillas
    # el puente colgante de Angostura, por la parte angosta
    for xx in (50, 70):
        l.masa(box(xx - .7, 22, xx + .7, 31.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.trazo([(40, 30.4), (50, 22.4), (60, 28), (70, 22.4), (80, 30.4)], .2, color='E2EDE9', alfa=.95)
    l.masa(box(40, 30.2, 80, 31), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    # la botella de amargo, en la orilla, con su etiqueta grande
    b = l.masa([box(96, 31, 101, 39), box(97.6, 28.4, 99.4, 31.2)], material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.35)
    l.mancha(box(95.6, 32.4, 101.4, 37.4), 'FBEFCB', .95, dentro=b)
    l.trazo([(96.4, 34), (100.4, 34)], .14, color='3A2A0A', alfa=.7, dentro=b)


# ------------------------------------------------------------------------------------------------ Ciudad Guayana
def guayana(l):
    rng = np.random.default_rng(13)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # atrás, la acería con sus chimeneas y las grúas del muelle
    prado(l, 15, 19, .24)
    for x, h in ((8, 9), (14, 12), (104, 10), (112, 8)):
        l.masa(box(x - .8, 17 - h, x + .8, 17.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        for k in range(3):
            l.mancha(ovalo(x + 1.4 + k * 2, 17 - h - 1.4 - k, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .6 - k * .12, difuso=.4)
    l.masa([box(18, 11.4, 34, 17.4), box(86, 12, 102, 17.4)], material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.25)
    # los dos ríos que corren juntos sin mezclarse: el Caroní, oscuro como té, y el Orinoco, pardo como café con leche
    agua(l, box(-2, 17.6, 122, 30), ondas=0, linea=0)
    l.mancha(box(-2, 17.6, 122, 23.6), NEGRO, .55)
    l.mancha(box(-2, 23.6, 122, 30), PARDO, .45)
    l.trazo([(x, 23.6 + .3 * math.sin(x / 3)) for x in np.arange(-2, 122, 2)], .3, color='D8C49A', alfa=.6)
    for _ in range(14):
        x, y = rng.uniform(2, 116), rng.uniform(18.6, 29)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='D2F2DA', alfa=.6)
    # el muelle de adelante, con su grúa, y la guayaba de acero dorada, protagonista
    muelle = box(-2, 30, 122, 41.6)
    mm = piedra(l, muelle, .1, .4)
    for x in np.arange(-2, 122, 6):
        l.trazo([(x, 30), (x, 41.6)], .1, color='6B7E7B', alfa=.5, dentro=mm)
    l.masa([box(14, 14, 15.4, 31), Polygon([(14.6, 14), (30, 12.4), (30, 13.4), (14.6, 15.6)])], material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0,
           linea=.3)
    l.trazo([(29, 13.4), (29, 20)], .1, color='0C3A33', alfa=.9)
    g = forma([(60, 16.8), (62.8, 17.8), (64.4, 21), (67.6, 25.4), (68.8, 29.6), (66.4, 33.6), (62, 35.4), (58, 35.4), (53.6, 33.6), (51.2, 29.6),
               (52.4, 25.4), (55.6, 21), (57.2, 17.8)], 2)
    l.mancha(ovalo(61, 35.6, 9, 1.2), '0C3A33', .3, difuso=.5)
    m = l.masa(g, material='acento', alto=.65, brillo=.65, vientre=0, hondo=.1, linea=.45, contraluz=.45)
    l.trazo([(55, 23), (54.6, 27), (56, 31)], [.06, .5, .06], color='FBEFCB', alfa=.9, dentro=m)
    for k in range(5):                                                   # la coronita de abajo, del cáliz
        a = math.radians(-90 + (k - 2) * 26)
        l.trazo([(60, 35), (60 + 1.6 * math.cos(a + math.pi), 35 + 1.2 + .4 * math.sin(a))], .3, color='6B4E10', alfa=.8)
    l.masa(tubo([(60, 17.6), (59.4, 15.4), (60.6, 14)], [.5, .4, .3], 4), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.masa(ovalo(63, 14.4, 2.6, 1.1, -25), material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)          # la hojita


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    rng = np.random.default_rng(15)
    cielo(l, sol=None)
    nube(l, 24, 3, 12, .4)
    # el Atlántico, arriba, con los barcos grandes
    horizonte = 6
    m = l.masa(box(-2, horizonte, 122, 18), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    for _ in range(12):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 1, 16)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    for x, y, s in ((18, 9, .9), (98, 11, .7)):
        l.masa([forma([(x - 8 * s, y), (x + 8 * s, y), (x + 9 * s, y - 1.6 * s), (x - 8.4 * s, y - 1.6 * s)], 1), box(x - 5 * s, y - 4 * s, x, y - 1.5 * s)],
               material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # el delta, visto desde arriba: el río que llega desde abajo y se abre en abanico; los pliegues dorados del abanico y los caños entre ellos
    agua(l, box(-2, 14, 122, 41.6), ondas=0, linea=0)
    pivote = (60, 44)
    n = 8
    for k in range(n):                                                   # los pliegues dorados del abanico
        a0 = math.radians(205 + k * (130 / n) + 1.2)
        a1 = math.radians(205 + (k + 1) * (130 / n) - 1.2)
        r0, r1 = 9, 36
        pliegue = Polygon([(pivote[0] + r0 * math.cos(a0), pivote[1] + r0 * math.sin(a0)), (pivote[0] + r1 * math.cos(a0), pivote[1] + r1 * .78 * math.sin(a0)),
                           (pivote[0] + r1 * math.cos((a0 + a1) / 2), pivote[1] + r1 * .82 * math.sin((a0 + a1) / 2)),
                           (pivote[0] + r1 * math.cos(a1), pivote[1] + r1 * .78 * math.sin(a1)), (pivote[0] + r0 * math.cos(a1), pivote[1] + r0 * math.sin(a1))])
        p = l.masa(pliegue, material='acento', alto=.3, brillo=.4 + (k % 2) * .15, vientre=0, hondo=0, linea=.35, contraluz=.35)
        for _ in range(6):                                               # la selva y los manglares de cada isla
            t, r = rng.uniform(.15, .85), rng.uniform(14, 32)
            a = a0 + (a1 - a0) * t
            l.mancha(ovalo(pivote[0] + r * math.cos(a), pivote[1] + r * .8 * math.sin(a), 1.2, .8), '6B4E10', .45, dentro=p)
    l.masa(ovalo(60, 40, 9, 4.4), material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)    # el mango del abanico
    l.mancha(ovalo(60, 40, 2.4, 1.4), '6B4E10', .8)
    # un palafito de los waraos, en un caño
    l.masa([box(84, 24, 92, 26.6), Polygon([(83, 24.2), (88, 21.4), (93, 24.2)])], material='vientre', alto=.25, brillo=.15, vientre=0, hondo=0,
           linea=.3)
    for x in (85, 88, 91):
        l.trazo([(x, 26.6), (x, 29.4)], .2, color='5A3E1E', alfa=.9)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='San Fernando de Atabapo', dibujar=san_fernando),
            dict(clave='Puerto Ayacucho', dibujar=puerto_ayacucho), dict(clave='Puerto Carreño', dibujar=puerto_carreno),
            dict(clave='Caicara del Orinoco', dibujar=caicara), dict(clave='Ciudad Bolívar', dibujar=bolivar), dict(clave='Ciudad Guayana', dibujar=guayana),
            dict(clave='mar', dibujar=mar)]
LISTO = True
