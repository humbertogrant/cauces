# -*- coding: utf-8 -*-
"""Las postales del Tárcoles, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el de Tárcoles, donde los cocodrilos lo toman.

- el nacimiento: el Valle Central entre sus volcanes, lleno de casas, y los dos ríos dorados que recogen su agua: el Grande, que viene
  de San Ramón por la izquierda, y el Virilla, que baja de Coronado entre San José y Heredia, y se van a juntar abajo;
- Heredia: «una ciudad de flores con un fortín de ladrillo que mira el río desde arriba»: el Fortín dorado, con sus troneras que miran
  hacia abajo, entre las flores, sobre el cañón del Virilla;
- Belén: «un portal de Belén con mulas cruzando un puente de piedra y un chip de computadora de estrella»: el chip dorado, con sus
  patitas como rayos, que brilla de estrella sobre el portal, y las mulas que cruzan el puente de piedra;
- Balsa: «una balsa de troncos cruza el río justo donde dos ríos se abrazan»: la balsa dorada, con el balsero y una mula, en el
  abrazo del Virilla y el Grande, donde nace el Tárcoles;
- Orotina: «una oreja enorme escucha pasar el tren cargado de mangos y sandías»: la oreja dorada, parada junto a la vía, y el tren
  con sus vagones de frutas; a la orilla, los puestos de fruta;
- Tárcoles: «docenas de cocodrilos toman el sol bajo un puente lleno de turistas con celular»: los cocodrilos dorados en los bancos
  de barro, bajo el puente con los turistas que les toman fotos, y un sol pálido;
- el mar: la lancha de Tárcoles, la barca del juego, de casco dorado, con su techo de lona y su salvavidas, que sale al golfo de
  Nicoya entre los manglares; en el almendro de la playa, Ara, la lapa roja, con su pareja.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import forma, ovalo, tubo

PIEL = 'A2683A'            # el tono de la piel: un café tibio sobre el pálido de `vientre`
MADERA = '5A3E1E'
TEJA = 'B0603A'
LADRILLO = '9A4A30'


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


def casa(l, x, base, w, h, techo=TEJA):
    """una casita blanca de techo de teja, con su puerta y su ventana"""
    c = l.masa(box(x, base - h, x + w, base).buffer(.04), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    l.mancha(box(x + w * .42, base - h * .6, x + w * .58, base), '164F46', .8, dentro=c)
    t = Polygon([(x - .5, base - h + .2), (x + w / 2, base - h - w * .38), (x + w + .5, base - h + .2)])
    tm = l.masa(t, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    l.mancha(t.buffer(.4), techo, .75, dentro=tm)


def rio_dorado(l, g, ondas):
    """un río dorado, protagonista, con su agua: las ondas claras en `ondas` [(x, y)…]"""
    m = l.masa(g, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.4, escalon=.1, contraluz=.3)
    for x, y in ondas:
        l.trazo([(x - 1.4, y), (x, y - .3), (x + 1.4, y)], .16, color='FBEFCB', alfa=.9, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 60, 3.4, 14, .45)
    # los volcanes que cierran el valle: el Poás, el Barva y el Irazú, y los cerros de los lados
    cordillera(l, [(-2, 12), (10, 8), (18, 5.4), (22, 5.4), (32, 9), (44, 7), (52, 8.4), (62, 10.4), (80, 9), (92, 5), (98, 4.6), (108, 8), (122, 9.4)],
               material='lejos')
    prado(l, 13, 41.6, .26)
    # la ciudad del Valle Central, apretada entre los dos ríos
    for y, n, h in ((15.4, 14, 2), (18.4, 12, 2.4), (21.6, 10, 2.8), (25, 8, 3.2), (28.6, 6, 3.6), (32.4, 4, 4)):
        ancho = (n * 4.4)
        for k in range(n):
            x = 60 - ancho / 2 + k * 4.4 + rng.uniform(-.6, .6)
            casa(l, x, y, 3 + (y - 15) * .08, h * rng.uniform(.8, 1.1), techo=TEJA if rng.random() < .6 else '6E7E7B')
    l.masa([box(57.4, 9.4, 62.6, 15.6), box(58.6, 6.4, 61.4, 9.6)], material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.25)   # la catedral
    for x in np.arange(2, 30, 5):
        arbol(l, x, 30 + (x % 3), 2, material='lejos', semilla=int(x))
    for x in np.arange(92, 120, 5):
        arbol(l, x, 30 + (x % 3), 2, material='lejos', semilla=int(x))
    # los dos ríos dorados, protagonistas, que recogen el agua del valle y bajan a juntarse: el Grande y el Virilla
    grande = cinta([(4, 15.6), (14, 20), (26, 24.4), (40, 30), (52, 36.6), (59, 42)], [1, 1.6, 2.4, 3.2, 4, 4.6], 10)
    virilla = cinta([(116, 15), (104, 19.4), (92, 24.4), (80, 30), (68, 36.6), (61, 42)], [1, 1.6, 2.4, 3.2, 4, 4.6], 10)
    rio_dorado(l, unary_union([grande, virilla]), [(14, 20), (26, 24.4), (38, 29), (50, 35.4), (104, 19.4), (92, 24.4), (80, 30), (68, 36.4)])


# ------------------------------------------------------------------------------------------------ Heredia
def flores(l, x0, x1, y0, y1, n, semilla=0):
    """matas con flores de colores: rosadas, blancas, moradas y rojas"""
    rng = np.random.default_rng(semilla)
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        l.masa([ovalo(x + dx, y + .6, 1, .6, a) for dx, a in ((-1.2, -30), (0, 0), (1.2, 30))], material='cuerpo', alto=.3, brillo=.15, vientre=0, hondo=0,
               linea=.22, arroja=False)
        color = str(rng.choice(['E8A0B0', 'FFFFFF', 'B08AC8', 'C8584A', 'F0C0D0']))
        for k in range(3):
            fx, fy = x + (k - 1) * 1.3 + rng.uniform(-.3, .3), y - .6 - (k % 2) * .8
            for j in range(5):
                a = math.radians(j * 72)
                l.mancha(ovalo(fx + math.cos(a) * .45, fy + math.sin(a) * .45, .42, .42), color, .95)
            l.mancha(ovalo(fx, fy, .22, .22), 'E8B952', .9)


def fortin(l, x, base, s=1.0):
    """el Fortín de Heredia, dorado: la torre redonda de ladrillo, el anillo de arriba, la cupulita, y dos troneras que miran hacia
    abajo, al río, como ojos"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry: ovalo(x + u * s, base + v * s, rx * s, ry * s)
    torre = forma(P([(-7.4, 0), (-6.8, -17), (6.8, -17), (7.4, 0)]), 0)
    anillo = forma(P([(-8, -16.6), (-8, -19.6), (8, -19.6), (8, -16.6)]), 0)
    cupula = forma(P([(-4.6, -19.4), (-4.2, -22), (-2, -24), (2, -24), (4.2, -22), (4.6, -19.4)]), 2)
    m = l.masa([torre, anillo, cupula, O(0, -24.6, .6, 1)], material='acento', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.45, escalon=.2,
               contraluz=.4)
    for v in np.arange(-15.6, -.6, 1.6):                                 # las hiladas de ladrillo
        l.trazo(P([(-7, v), (7, v)]), .1 * s, color='6B4E10', alfa=.4, dentro=m)
        for u in np.arange(-6 + (v * 1.3) % 2.4, 7, 2.4):
            l.trazo(P([(u, v), (u, v + 1.6)]), .08 * s, color='6B4E10', alfa=.3, dentro=m)
    l.trazo(P([(-8, -16.8), (8, -16.8)]), .2 * s, color='6B4E10', alfa=.6, dentro=m)
    for dx in (-2.8, 2.8):                                               # las troneras, que miran al río
        l.masa(O(dx, -11, 1.4, 1.6), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(O(dx + .2, -10.2, .7, .75), '05201C', 1)
    l.trazo(P([(-1.4, -5.8), (0, -5.2), (1.4, -5.8)]), .25 * s, color='3A2A0A', alfa=.75)
    l.mancha(forma(P([(-1.6, 0), (-1.6, -3.4), (0, -4.4), (1.6, -3.4), (1.6, 0)]), 1), '3A2A0A', .8)   # la puerta


def heredia(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # el volcán Barva, atrás, la ciudad con su iglesia, y el cañón del Virilla abajo
    cordillera(l, [(-2, 14), (20, 10), (40, 6.6), (56, 7.6), (76, 11), (100, 9.6), (122, 12)], material='lejos')
    prado(l, 15, 41.6, .28)
    for x, w, h in ((-1, 6, 4), (6, 5.6, 3.4), (12.4, 6, 4.2), (90, 6, 4), (97, 5.6, 3.4), (103.4, 6, 4.2), (110, 6, 3.8)):
        casa(l, x, 19, w, h)
    ig = l.masa([box(20, 9, 34, 19.4), box(21.4, 4.6, 25.6, 9.2)], material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(box(19, 4, 36, 20), 'BF9129', .2, dentro=ig)
    l.mancha(forma([(25.6, 19.4), (25.6, 15), (27, 13.6), (28.4, 15), (28.4, 19.4)], 1), '164F46', .8, dentro=ig)
    l.masa(Polygon([(20.8, 4.8), (23.5, 2.4), (26.2, 4.8)]), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # el cañón, con el río al fondo
    for pts in ([(-2, 41.6), (-2, 31), (24, 31.6), (38, 34), (42, 41.6)], [(122, 41.6), (122, 31), (96, 31.6), (82, 34), (78, 41.6)]):
        orilla(l, forma(pts, 1), tinte=.3)
    agua(l, forma([(42, 41.6), (44, 36.4), (60, 35.6), (76, 36.4), (78, 41.6)], 1), ondas=3, semilla=2, linea=.3)
    flores(l, 2, 118, 22, 30, 26, semilla=3)
    # el Fortín dorado, protagonista, que mira el río desde arriba, entre las flores
    fortin(l, 60, 33, 1.16)
    flores(l, 44, 76, 31.4, 34, 7, semilla=4)


# ------------------------------------------------------------------------------------------------ Belén
def chip(l, x, y, r):
    """un chip de computadora dorado, de estrella: el cuadro con su marca redonda y las patitas que salen por los cuatro lados como
    rayos, más los rayos finos de la estrella entre ellas"""
    for k in range(4):                                                   # los rayos finos de la estrella
        a = math.radians(45 + k * 90)
        l.trazo([(x + math.cos(a) * r * 1.1, y + math.sin(a) * r * 1.1), (x + math.cos(a) * r * 2.3, y + math.sin(a) * r * 2.3)], [.5, .05],
                color='F2D48A', alfa=.95)
    patas = []
    for lado in range(4):
        for k in range(5):
            t = -.64 + k * .32
            if lado == 0:
                patas.append(box(x + t * r - .28, y - r * 1.75, x + t * r + .28, y - r))
            elif lado == 1:
                patas.append(box(x + t * r - .28, y + r, x + t * r + .28, y + r * 1.75))
            elif lado == 2:
                patas.append(box(x - r * 1.75, y + t * r - .28, x - r, y + t * r + .28))
            else:
                patas.append(box(x + r, y + t * r - .28, x + r * 1.75, y + t * r + .28))
    cuerpo = box(x - r, y - r, x + r, y + r)
    m = l.masa(patas + [cuerpo], material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.4)
    l.mancha(box(x - r * .78, y - r * .78, x + r * .78, y + r * .78), '6B4E10', .25, dentro=m)
    l.mancha(ovalo(x - r * .5, y - r * .5, r * .14, r * .14), '6B4E10', .6, dentro=m)
    for k in range(3):                                                   # las pistas grabadas
        l.trazo([(x - r * .5, y - r * .1 + k * r * .3), (x + r * .55, y - r * .1 + k * r * .3)], .12, color='FBEFCB', alfa=.7, dentro=m)


def mula_chica(l, x, base, s=1.0, lado=1):
    """una mula chica, gris, de perfil, con sus orejas largas"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    g = [ovalo(x, base - 4.4 * s, 3.6 * s, 1.8 * s), tubo(P([(2.8, -5), (4.2, -6.6)]), [.9 * s, .7 * s], 3), ovalo(x + lado * 5 * s, base - 6.6 * s, 1.4 * s, .8 * s),
         Polygon(P([(4, -7.2), (3.4, -9.6), (4.6, -7.4)])), Polygon(P([(4.6, -7.2), (4.6, -9.8), (5.4, -7.4)]))]
    g += [tubo(P([(u, -3.4), (u, 0)]), [.4 * s, .35 * s], 2) for u in (-2.6, -1.6, 1.8, 2.8)]
    m = l.masa(g, material='claro', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(g).buffer(1), '6E7E7B', .55, dentro=m)


def belen(l):
    cielo(l, sol=None)
    l.mancha(box(0, 0, 120, 14), 'C9E4DA', .5, difuso=4)                 # el cielo de la noche buena, un poco más hondo arriba
    # la fábrica, lejos, a la derecha, y el portal de Belén al medio, con su techo de paja
    prado(l, 18, 41.6, .26)
    f = l.masa([box(92, 12, 118, 18.4), box(98, 9.6, 112, 12.2)], material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(94, 117, 3):
        l.mancha(box(x, 14, x + 1.6, 15.6), '164F46', .7, dentro=f)
    for x in (4, 12, 22):
        casa(l, x, 18.6, 6, 4)
    portal = [box(46, 17.4, 47.4, 24), box(72.6, 17.4, 74, 24), box(59.3, 16, 60.7, 24)]
    madera(l, portal, .6)
    l.mancha(box(47.4, 18.4, 72.6, 24), '3A2A0A', .55)
    techo = forma([(42, 18.4), (48, 14.4), (72, 14.4), (78, 18.4)], 1)
    t = l.masa(techo, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(techo.buffer(1), 'BF9129', .45, dentro=t)
    for x in np.arange(44, 77, 1.6):
        l.trazo([(x, 15), (x - .6, 18.2)], .1, color='6B4E10', alfa=.45, dentro=t)
    madera(l, [forma([(54, 24), (55, 20.6), (65, 20.6), (66, 24)], 1)], .5)           # el pesebre
    l.mancha(ovalo(60, 20.6, 4.4, 1), 'F2D48A', .7)                       # la paja con su luz
    # el río y el puente de piedra en arcos, con las mulas que lo cruzan
    rio(l, 30)
    p = l.masa(Polygon([(-2, 26), (122, 26), (122, 29.4), (-2, 29.4)]), material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(box(-2, 25, 122, 31), 'BF9129', .35, dentro=p)
    for x0 in np.arange(-2, 122, 20):
        arco = forma([(x0 + 3, 34), (x0 + 3, 31), (x0 + 6, 28.4), (x0 + 10, 28), (x0 + 14, 28.4), (x0 + 17, 31), (x0 + 17, 34)], 2)
        l.mancha(box(x0, 29.4, x0 + 20, 34), 'BF9129', .0)
        pm = l.masa([box(x0 - 1, 29.2, x0 + 3, 36), box(x0 + 17, 29.2, x0 + 21, 36)], material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
        l.mancha(box(x0 - 2, 29, x0 + 22, 36.4), 'BF9129', .35, dentro=pm)
    for x in np.arange(0, 122, 2.4):
        l.trazo([(x, 26), (x, 29.4)], .08, color='6B4E10', alfa=.35)
    for x, s in ((26, 1.1), (38, 1.15), (88, 1.1)):
        mula_chica(l, x, 26.2, s, 1 if x < 60 else -1)
    # el chip dorado, protagonista, que brilla de estrella sobre el portal
    l.mancha(ovalo(60, 7, 14, 6), 'FBEFCB', .45, difuso=2)
    chip(l, 60, 7.2, 3.9)


# ------------------------------------------------------------------------------------------------ Balsa
def balsa_troncos(l, x, y, s=1.0):
    """una balsa de troncos dorada, vista un poco desde arriba: los troncos amarrados, con el balsero que la empuja con la vara y una
    mula encima"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    troncos = [tubo(P([(-12, -4 + k * 1.6), (12, -4.6 + k * 1.6)]), [.8 * s, .8 * s], 2) for k in range(6)]
    m = l.masa(troncos, material='acento', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for k in range(6):
        l.mancha(ovalo(x - 12 * s, y + (-4 + k * 1.6) * s, .5 * s, .6 * s), '6B4E10', .6, dentro=m)          # los cortes
    for u in (-8, 8):                                                    # los amarres
        l.trazo(P([(u, -5), (u + .4, 4.6)]), .25 * s, color='5A3E1E', alfa=.9)
    # el balsero con su vara, y la mula
    piel(l, [ovalo(x + 7 * s, y - 13.4 * s, 1.1 * s, 1.2 * s), ovalo(x + 9.4 * s, y - 9.6 * s, .6 * s, .6 * s)])
    l.masa([forma(P([(5.4, -3), (5.6, -11.6), (8.4, -11.6), (8.6, -3)]), 1), tubo(P([(8, -11), (9.4, -9.6)]), [.5 * s, .45 * s], 2)], material='claro', alto=.3,
           brillo=.2, vientre=0, hondo=0, linea=.3)
    l.masa([ovalo(x + 7 * s, y - 14.6 * s, 2.4 * s, .5 * s), forma(P([(5.8, -14.6), (6, -16), (8, -16), (8.2, -14.6)]), 1)], material='vientre', alto=.3,
           brillo=.2, vientre=0, hondo=0, linea=.25)
    l.trazo(P([(12, -18), (6.6, 6)]), .3 * s, color='3A2A0A', alfa=.95)
    mula_chica(l, x - 4 * s, y - 2.6 * s, 1.15 * s, 1)


def balsa(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # los cerros secos de Atenas, y los dos ríos que se juntan, vistos un poco desde arriba: el Grande, que viene de la izquierda, y el
    # Virilla, de la derecha; abajo, el Tárcoles
    cordillera(l, [(-2, 12), (20, 8.6), (42, 11), (64, 8), (86, 10.6), (104, 8.4), (122, 11)], material='lejos')
    prado(l, 13, 41.6, .32)
    for x in np.arange(4, 118, 9):
        arbol(l, x, 16.6 + (x % 4) * .4, 2, material='lejos', semilla=int(x))
    agua(l, unary_union([cinta([(-2, 19), (16, 21.4), (34, 24.6), (50, 27.4), (60, 29)], [3.4, 4, 5, 6, 7], 8),
                         cinta([(122, 18.4), (104, 21), (86, 24.4), (70, 27.4), (60, 29)], [3.4, 4, 5, 6, 7], 8),
                         cinta([(60, 29), (58, 34), (61, 38), (60, 41.8)], [10, 12, 13, 14], 8)]), ondas=12, semilla=5, linea=.35)
    for x, y in ((40, 25.2), (80, 25.2), (52, 27.4), (68, 27.4)):        # las ondas del abrazo
        l.trazo([(x - 1.6, y + .6), (x, y), (x + 1.6, y + .6)], .2, color='D2F2DA', alfa=.85)
    # la balsa de troncos dorada, protagonista, que cruza en el abrazo
    l.mancha(ovalo(60, 33.6, 14, 1.6), '0C3A33', .25, difuso=.6)
    balsa_troncos(l, 60, 32.4, 1.12)


# ------------------------------------------------------------------------------------------------ Orotina
def oreja(l, x, base, s=1.0):
    """una oreja enorme, dorada, parada en el suelo, de perfil: el pabellón, el borde enrollado, el hueco y el lóbulo"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    g = forma(P([(-2, 0), (-5.4, -3), (-7.4, -8), (-8.4, -14), (-7.4, -20), (-4, -24.6), (1, -26), (5.4, -24.4), (8, -20), (8.4, -14), (6.6, -9.4),
                 (3, -6.6), (1.4, -3.6), (2.4, -.4)]), 3)
    m = l.masa(g, material='acento', alto=.55, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.trazo(P([(-5.6, -8), (-6.6, -14), (-5.4, -20), (-2, -23.4), (2, -23.6), (5, -21), (6, -16), (4.6, -11.6), (1.6, -9.6)]), [.1, .5, .6, .6, .6, .5, .4, .3, .1],
            color='6B4E10', alfa=.55, dentro=m)                          # el borde enrollado
    hueco = forma(P([(-2.6, -10.4), (-3.4, -14.4), (-1.6, -17.4), (1.6, -17.6), (2.4, -14.6), (.6, -12.4), (.4, -10)]), 2)
    l.mancha(hueco, '6B4E10', .7, dentro=m)
    l.trazo(P([(-3.6, -19.4), (0, -21), (3.4, -19)]), [.05, .3, .05], color='FBEFCB', alfa=.85, dentro=m)
    return g


def vagon(l, x, y, w, carga, semilla=0):
    """un vagón de tren abierto, cargado de mangos o de sandías"""
    rng = np.random.default_rng(semilla)
    madera(l, [box(x, y - 4, x + w, y)], .55)
    for u in (x + 2, x + w - 2):
        l.masa(ovalo(u, y + .6, 1.2, 1.2), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    for k in range(int(w // 2.4) * 2):
        cx, cy = x + 1.4 + (k % int(w // 2.4)) * 2.4 + rng.uniform(-.3, .3), y - 4.4 - (k // int(w // 2.4)) * 1.4
        if carga == 'sandia':
            m = l.masa(ovalo(cx, cy, 1.4, 1), material='cuerpo', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
            l.trazo([(cx - 1.2, cy), (cx + 1.2, cy)], .14, color='164F46', alfa=.7, dentro=m)
        else:
            m = l.masa(ovalo(cx, cy, 1, .8, 20), material='vientre', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
            l.mancha(ovalo(cx, cy, 1.4, 1.2), 'D88A3A', .75, dentro=m)
            l.mancha(ovalo(cx + .4, cy - .3, .5, .4), '7AA84A', .7, dentro=m)


def orotina(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    nube(l, 104, 3.6, 10, .4)
    cordillera(l, [(-2, 15), (24, 11), (50, 13.6), (76, 10.4), (100, 12.6), (122, 11)], material='lejos')
    prado(l, 16, 41.6, .3)
    for x in (8, 20, 102, 114):                                          # los palos de mango
        arbol(l, x, 18, 3.6, material='cuerpo', semilla=x)
    # los puestos de fruta de la orilla del camino
    for x in (2, 30):
        madera(l, [box(x, 26, x + 1, 32), box(x + 13, 26, x + 14, 32)], .6)
        t = l.masa(forma([(x - 1.6, 26.4), (x + 7, 23.6), (x + 15.6, 26.4)], 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(Polygon([(x - 1, 25.4), (x + 7, 22.6), (x + 15, 25.4), (x + 15, 27), (x - 1, 27)]), '5A8EC8', .35, dentro=t)
        madera(l, [box(x, 29.6, x + 14, 31.4)], .5)
        for k in range(6):
            cx = x + 1.4 + k * 2.2
            m = l.masa(ovalo(cx, 28.6, 1, .9), material='vientre', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.22)
            l.mancha(ovalo(cx, 28.6, 1.4, 1.2), ('D88A3A', '7AA84A', 'C8584A')[k % 3], .7, dentro=m)
    # la vía y el tren de las frutas, que pasa
    for y in (36.4, 38.4):
        l.trazo([(-2, y), (122, y)], .35, color='6E7E7B', alfa=.95)
    for x in np.arange(0, 122, 3):
        l.trazo([(x, 35.8), (x - .6, 39.2)], .5, color=MADERA, alfa=.6)
    l.masa([box(72, 26.6, 88, 35), box(82, 22, 88, 27), box(74, 23.4, 76, 26.8)], material='lejos', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    l.mancha(box(83.2, 23, 86.8, 25.4), CIELO, .9)                       # la ventana de la cabina, atrás
    for u in (75, 79.6, 84.4):
        l.masa(ovalo(u, 35.6, 1.6, 1.6), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    for k in range(3):
        l.mancha(ovalo(76 + k * 3, 21.4 - k * 1.4, 1.4 + k * .5, 1 + k * .3), 'FFFFFF', .8 - k * .15, difuso=.4)
    vagon(l, 89, 35, 15, 'mango', semilla=1)
    vagon(l, 106, 35, 15, 'sandia', semilla=2)
    # la oreja dorada, protagonista, que escucha pasar el tren, y el ruido que le llega
    oreja(l, 54, 35.6, 1.3)
    for k in range(3):
        r = 4 + k * 2.2
        l.trazo([(69 - r * .4 * math.cos(t), 24 + r * math.sin(t)) for t in np.linspace(-.9, .9, 7)], .24, color='0C3A33', alfa=.6)


# ------------------------------------------------------------------------------------------------ Tárcoles
def cocodrilo(l, x, base, s=1.0, lado=1, material='acento'):
    """un cocodrilo echado en el barro, de perfil, mirando a `lado`, con la boca abierta al sol: el hocico largo con sus dientes, el
    ojo alto, las patas cortas, el lomo de escamas y la cola larga"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    g = [forma(P([(-8, -1.2), (-6, -4.4), (0, -5.2), (6, -4.8), (9, -5), (12.4, -7.6), (17, -8.6), (17.6, -7.6), (13, -5.6), (17.4, -4.4), (17, -3.4),
                  (12, -2.8), (8, -1), (-6, -.6)]), 2),
         tubo(P([(-7.6, -2.2), (-13, -1.6), (-18, -.8), (-21, -.2)]), [2.4 * s, 1.6 * s, .9 * s, .2 * s], 8),
         tubo(P([(4.6, -1.6), (5.6, 0)]), [1.1 * s, .9 * s], 4), tubo(P([(-4, -1.6), (-5, 0)]), [1.1 * s, .9 * s], 4)]
    c = l.masa(g, material=material, alto=.45, brillo=.4, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    for u in np.arange(-16, 8, 1.8):
        v = -4.8 if u > -6 else -2.8 + (u + 6) * .12
        l.trazo(P([(u, v), (u + .9, v - .6), (u + 1.8, v)]), .13 * s, color='6B4E10', alfa=.6, dentro=c)
    for u in np.arange(13.4, 17, 1.1):                                   # los dientes
        l.trazo(P([(u, -5.6), (u + .2, -6.2)]), .16 * s, color='FFFFFF', alfa=.95)
        l.trazo(P([(u, -4.6), (u + .2, -4)]), .16 * s, color='FFFFFF', alfa=.95)
    l.masa(ovalo(x + lado * 10.6 * s, base - 6.4 * s, 1.2 * s, 1 * s), material=material, alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(x + lado * 10.8 * s, base - 6.5 * s, .45 * s, .4 * s), '05201C', 1)
    return c


def turista(l, x, base, s=1.0, semilla=0):
    """un turista en la baranda, de espaldas a nosotros no: de frente, con el celular levantado para la foto"""
    rng = np.random.default_rng(semilla)
    camisa = str(rng.choice(['FFFFFF', '5A8EC8', 'E8A0B0', '7AA84A']))
    m = l.masa(forma([(x - 1.4 * s, base), (x - 1.6 * s, base - 3.6 * s), (x + 1.6 * s, base - 3.6 * s), (x + 1.4 * s, base)], 1), material='claro', alto=.3, brillo=.2,
               vientre=0, hondo=0, linea=.22)
    l.mancha(box(x - 2 * s, base - 4 * s, x + 2 * s, base), camisa, .55, dentro=m)
    piel(l, [ovalo(x, base - 4.6 * s, .9 * s, 1 * s), tubo([(x + 1.2 * s, base - 3.2 * s), (x + 1.8 * s, base - 5.6 * s)], [.35 * s, .3 * s], 3)], .55)
    l.masa(box(x + 1.4 * s, base - 7.2 * s, x + 2.4 * s, base - 5.6 * s), material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.15)   # el celular
    if rng.random() < .5:
        l.mancha(ovalo(x + 1.9 * s, base - 6.8 * s, .25 * s, .25 * s), 'FFFFFF', .95)


def tarcoles(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    l.mancha(ovalo(108, 7, 9, 6), 'FBEFCB', .45, difuso=2)               # el sol pálido que toman
    l.mancha(ovalo(108, 7.2, 3.2, 3.2), 'F2D48A', .55)
    # el puente con su baranda y los turistas que toman fotos
    for x in (16, 104):
        l.masa(box(x - 2.4, 15, x + 2.4, 30), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    for k in range(13):
        turista(l, 6 + k * 9.2 + rng.uniform(-1, 1), 12.6, .95, semilla=k)
    l.masa(box(-2, 12.4, 122, 15.4), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.trazo([(-2, 9.6), (122, 9.6)], .3, color='8EB5AA', alfa=.95)
    for x in np.arange(0, 122, 3):
        l.trazo([(x, 9.6), (x, 12.4)], .2, color='8EB5AA', alfa=.9)
    # el río, abajo, con los bancos de barro y los cocodrilos dorados, protagonistas, que toman el sol
    agua(l, box(-2, 15.4, 122, 41.6), ondas=10, semilla=10, linea=0)
    for pts in ([(-2, 34), (20, 30.6), (50, 30), (80, 31), (110, 30.4), (122, 31), (122, 38), (-2, 39)], [(30, 22), (50, 20.6), (76, 21), (90, 22.6), (70, 24),
                                                                                                        (40, 24)]):
        b = l.masa(forma(pts, 2), material='vientre', alto=.1, brillo=.05, vientre=0, hondo=0, linea=.3)
        l.mancha(forma(pts, 2).buffer(1), '8A6A3A', .5, dentro=b)
    for x, y, s, lado in ((44, 22.6, .5, 1), (62, 22, .45, -1), (78, 22.8, .5, -1), (12, 32.2, .6, 1), (100, 31.8, .62, -1), (110, 34, .6, -1)):
        cocodrilo(l, x, y, s, lado)
    cocodrilo(l, 56, 35.4, 1.25, 1)


# ------------------------------------------------------------------------------------------------ el mar
def lancha_toldo(l, x, y, s=1.0):
    """la lancha de Tárcoles, la barca del juego, mirando a la derecha: el casco de madera, dorado; el techo de lona sobre postes, las
    bancas, el salvavidas colgado y el motor fuera de borda; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([forma(P([(-16.6, -5.4), (-14, -5.6), (-13.8, -2.4), (-16.4, -2.4)]), 1), box(x - 15.8 * s, y - 2.6 * s, x - 15 * s, y + 1.6 * s)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)                         # el motor
    for u in (-10, -2, 6):                                               # los postes
        l.trazo(P([(u, -1.6), (u, -9.4)]), .25 * s, color='3A2A0A', alfa=.9)
    for u in (-8, 0):                                                    # las bancas
        madera(l, [box(x + (u - 1.4) * s, y - 3.4 * s, x + (u + 1.4) * s, y - 2.2 * s)], .6, linea=.2)
    lona = forma(P([(-12, -9), (-11.4, -10.6), (8, -10.6), (8.6, -9), (-12, -9)]), 1)
    t = l.masa(lona, material='claro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.mancha(lona.buffer(1), '5A8EC8', .4, dentro=t)
    sv = ovalo(x + 3 * s, y - 5.4 * s, 1.6 * s, 1.6 * s).difference(ovalo(x + 3 * s, y - 5.4 * s, .8 * s, .8 * s))     # el salvavidas
    m = l.masa(sv, material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
    for a in (0, 90, 180, 270):
        l.mancha(Polygon([(x + 3 * s, y - 5.4 * s), (x + 3 * s + 2 * s * math.cos(math.radians(a - 20)), y - 5.4 * s + 2 * s * math.sin(math.radians(a - 20))),
                          (x + 3 * s + 2 * s * math.cos(math.radians(a + 20)), y - 5.4 * s + 2 * s * math.sin(math.radians(a + 20)))]), 'C8584A', .8, dentro=m)
    casco = forma(P([(-15, -2.6), (-13, -1.4), (13, -1.4), (16.4, -3.6), (14.6, .6), (9, 1.4), (-11, 1.4), (-14.6, .6)]), 2)
    c = l.masa(casco, material='acento', alto=.45, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-14.4, -1.8), (0, -.9), (15.4, -2.8)]), [.05, .4, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco


def lapa(l, x, y, s=1.0, lado=1):
    """una lapa roja posada, de perfil: el cuerpo rojo, el ala con su azul, la cola larga, la cara blanca y el pico curvo"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    g = [ovalo(x, y, 1.2 * s, 1.9 * s), ovalo(x + lado * .5 * s, y - 2 * s, .9 * s, .9 * s), tubo(P([(-.4, 1.4), (-1, 4), (-1.4, 6.4)]), [.5 * s, .35 * s, .15 * s], 5)]
    m = l.masa(g, material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.25)
    l.mancha(unary_union(g).buffer(1), 'C8423A', .85, dentro=m)
    l.mancha(ovalo(x - lado * .4 * s, y + .8 * s, .8 * s, 1.2 * s), '3A5AA8', .85, dentro=m)
    l.mancha(ovalo(x + lado * .8 * s, y - 2 * s, .45 * s, .4 * s), 'FFFFFF', .95, dentro=m)
    l.masa(Polygon(P([(1.2, -2.6), (2.2, -2), (1.4, -1.4)])), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)


def mar(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 40, 5, 14, .5)
    nube(l, 100, 4, 12, .45)
    horizonte = 18
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(30, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa(forma([(70, horizonte + .4), (84, horizonte - 2.6), (100, horizonte - 3.4), (114, horizonte - 1.4), (122, horizonte + .4)], 1), material='lejos',
           alto=.2, brillo=.08, vientre=0, hondo=0, linea=.3)            # la península, lejos
    # los manglares de la boca, a la derecha, y la playa con el almendro y las lapas, a la izquierda
    orilla(l, forma([(122, 41.6), (122, 26), (108, 27.4), (98, 33), (96, 41.6)], 2), tinte=.3)
    for x, y, h in ((118, 30, 11), (108, 33, 12), (114, 39, 13)):
        mangle(l, x, y, h, semilla=x)
    orilla(l, forma([(-2, 41.6), (-2, 24), (16, 25), (28, 30), (32, 41.6)], 2), tinte=.5)
    for x, y, h in ((24, 32, 12), (30, 36, 10)):
        palmera(l, x, y, h, -1, datiles=False)
    madera(l, [tubo([(8, 34), (9, 26), (10, 18)], [1, .8, .6], 6), tubo([(9.4, 24), (14, 20), (18, 19)], [.5, .4, .3], 5)], .5)
    l.masa([ovalo(10, 15, 8, 3), ovalo(4, 17, 5, 2.4), ovalo(16, 16.6, 5, 2.4)], material='cuerpo', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.3)   # el almendro
    lapa(l, 14, 19, 1.1, 1)
    lapa(l, 5, 19.6, 1, -1)
    # la lancha de Tárcoles, la barca del juego, protagonista, que sale al golfo
    g = lancha_toldo(l, 62, 33, 1.45)
    reflejo(l, g, 33.4, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Heredia', dibujar=heredia), dict(clave='Belén', dibujar=belen),
            dict(clave='Balsa', dibujar=balsa), dict(clave='Orotina', dibujar=orotina), dict(clave='Tárcoles', dibujar=tarcoles),
            dict(clave='mar', dibujar=mar)]
LISTO = True
