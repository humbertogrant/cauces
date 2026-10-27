# -*- coding: utf-8 -*-
"""Las postales del Térraba, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: el río nace como río General al pie del Chirripó, la montaña más alta del país: un general de uniforme dorado que
  saluda al pie de la montaña, entre las nubes, con el río que le sale de las botas;
- San Isidro: «un santo labrador con un cerro gigante de sombrero»: San Isidro, de túnica dorada, con su azada y su aureola, y de
  sombrero un cerro entero, como el Chirripó; atrás, el valle con sus cafetales y la iglesia;
- Volcán: «un volcán que en vez de lava escupe piñas»: las piñas doradas que salen volando del cráter y caen en los piñales;
- Paso Real: «dos ríos se dan la mano bajo un puente y un rey los bautiza»: el rey dorado, con su corona, que desde el puente echa el
  agua de su jarra sobre las dos manos de agua, la del General y la del Coto Brus, que se aprietan abajo;
- Rey Curré: «un rey con máscara de diablito baila junto al río»: el rey, con su corona y su capa, que baila con la máscara de diablo
  boruca, dorada, de cuernos y dientes, a la orilla del río;
- Palmar: «palmeras en fila y esferas de piedra rodando entre bananos»: las esferas doradas que ruedan entre las matas de banano, con
  la fila de palmeras atrás;
- Ciudad Cortés: «una ciudad con nombre de conquistador se pone botas de hule»: el conquistador, con su morrión y su coraza, metido en
  la inundación hasta las rodillas con unas botas de hule doradas, frente a las casas con el agua en la puerta;
- el mar: la lancha de Puerto Cortés, la barca del juego, de casco dorado y cargada de piñas, que sale al Pacífico entre los manglares
  de Térraba-Sierpe, con las garzas; en una raíz, Pinzas, el cangrejo, que se queda.
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


def cara(l, x, y, s=1.0, bigote=False):
    """los ojos de punto, el bigote si lo lleva y la sonrisa de una cara de frente; (x, y) es el centro de la cabeza"""
    for dx in (-.85, .85):
        l.mancha(ovalo(x + dx * s, y - .4 * s, .26 * s, .3 * s), '05201C', 1)
    if bigote:
        l.trazo([(x - 1.4 * s, y + .75 * s), (x - .7 * s, y + 1.05 * s), (x, y + .95 * s), (x + .7 * s, y + 1.05 * s), (x + 1.4 * s, y + .75 * s)],
                [.1 * s, .32 * s, .3 * s, .32 * s, .1 * s], color='3A2A0A', alfa=.9)
    l.trazo([(x - .75 * s, y + 1.55 * s), (x, y + 1.9 * s), (x + .75 * s, y + 1.55 * s)], .16 * s, color='3A2A0A', alfa=.85)


def casa(l, x, base, w, h):
    """una casita de pueblo, blanca, de techo de zinc"""
    c = l.masa(box(x, base - h, x + w, base).buffer(.04), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25, arroja=False)
    l.mancha(box(x + w * .42, base - h * .62, x + w * .58, base), '164F46', .8, dentro=c)
    t = Polygon([(x - .5, base - h + .2), (x + w / 2, base - h - w * .34), (x + w + .5, base - h + .2)])
    tm = l.masa(t, material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25, arroja=False)
    l.mancha(t.buffer(.4), GRIS, .55, dentro=tm)


def banano(l, x, base, h, semilla=0, racimo=False):
    """una mata de banano: el falso tallo, las hojas anchas que se abren y caen, con su nervio, y si se pide, el racimo verde"""
    rng = np.random.default_rng(semilla)
    l.masa(tubo([(x, base), (x + .3, base - h * .55)], [.9, .7], 3), material='cuerpo', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.25)
    hojas, nervios = [], []
    for a in (-162, -128, -92, -56, -20):
        r = math.radians(a + rng.uniform(-8, 8))
        p0 = np.array([x + .3, base - h * .55])
        d = np.array([math.cos(r), math.sin(r)])
        p1 = p0 + d * h * .3 + np.array([0, -h * .1])
        p2 = p0 + d * h * .56 + np.array([0, h * .14])
        hojas.append(tubo([p0, p1, p2], [.25, h * .12, .2], 8))
        nervios.append([p0, p1, p2])
    m = l.masa(hojas, material='cuerpo', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.25, contraluz=.25)
    for n in nervios:
        l.trazo(n, .12, color='164F46', alfa=.6, dentro=m)
    if racimo:
        l.masa(forma([(x + .6, base - h * .5), (x + 2.6, base - h * .46), (x + 2.4, base - h * .3), (x + 1, base - h * .26)], 1), material='cuerpo', alto=.4,
               brillo=.2, vientre=0, hondo=0, linea=.25)


# ------------------------------------------------------------------------------------------------ el nacimiento
def general(l, x, base, s=1.0):
    """un general de frente, firme, que saluda: las botas, el pantalón con su franja, la casaca dorada con charreteras, botones y
    medallas, la mano en la sien y el bicornio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([forma(P([(-3.4, 0), (-3.2, -4.4), (-.8, -4.6), (-.5, 0)]), 1), forma(P([(.5, 0), (.8, -4.6), (3.2, -4.4), (3.4, 0)]), 1)],
           material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.25)                        # las botas altas
    pant = l.masa([tubo(P([(-1.6, -11), (-1.8, -7), (-1.9, -4)]), [1.4 * s, 1.2 * s, 1.1 * s], 5), tubo(P([(1.6, -11), (1.8, -7), (1.9, -4)]), [1.4 * s, 1.2 * s, 1.1 * s], 5)],
                  material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    for dx in (-2.8, 2.8):
        l.trazo(P([(dx, -10.6), (dx * 1.05, -4.4)]), .3 * s, color='6B4E10', alfa=.7, dentro=pant)
    casaca = [forma(P([(-4, -19.4), (4, -19.4), (4.4, -14), (4, -9.4), (-4, -9.4), (-4.4, -14)]), 1),
              tubo(P([(3.6, -18.6), (6.2, -20.6), (3.6, -22.8)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(-3.6, -18.6), (-4.8, -14.6), (-4.4, -10.8)]), [1.1 * s, 1 * s, .9 * s], 5)]
    m = l.masa(casaca, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    for v in np.arange(-18, -10, 1.6):                                   # los botones
        l.mancha(O(0, v, .32, .32), 'FBEFCB', .95, dentro=m)
    l.trazo(P([(0, -19), (0, -9.6)]), .1 * s, color='6B4E10', alfa=.5, dentro=m)
    for dx in (-1, 1):                                                   # las charreteras, con sus flecos
        l.masa(O(dx * 4.4, -19.4, 1.8, .8), material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.3)
        for k in range(4):
            l.trazo(P([(dx * (3.2 + k * .8), -19), (dx * (3.2 + k * .8), -17.8)]), .14 * s, color='6B4E10', alfa=.7)
    for u in (-2.4, -1.4):                                               # las medallas
        l.mancha(O(u, -16, .4, .45), 'FBEFCB', .95)
        l.trazo(P([(u, -17.2), (u, -16.4)]), .25 * s, color='C8584A', alfa=.9)
    l.mancha(Polygon(P([(-4, -10.8), (4, -10.8), (4, -9.8), (-4, -9.8)])), '3A2A0A', .85)          # el cinturón
    piel(l, [O(3.6, -23.2, .9, .9), O(-4.3, -10.4, .9, .9), O(0, -22, 2.2, 2.5), box(x - .7 * s, base - 20.4 * s, x + .7 * s, base - 19.2 * s)])
    cara(l, x, base - 22 * s, s, bigote=True)
    l.masa([forma(P([(-5.6, -24), (-3, -26.6), (0, -27.4), (3, -26.6), (5.6, -24), (3, -24.4), (0, -24), (-3, -24.4)]), 2)], material='oscuro', alto=.35,
           brillo=.35, vientre=0, hondo=0, linea=.3)                     # el bicornio
    l.mancha(O(0, -25.4, .7, .7), 'FBEFCB', .95)


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    # el Chirripó, enorme y de roca, con sus crestas, por encima de las nubes
    cordillera(l, [(-2, 20), (10, 15), (22, 12), (34, 7), (44, 3.4), (50, 1.6), (54, 2.6), (58, 1.2), (64, 3.6), (74, 7.4), (86, 10), (98, 9),
                   (108, 12), (122, 14)], material='lejos')
    for _ in range(40):
        x, y = rng.uniform(20, 100), rng.uniform(3, 18)
        l.trazo([(x, y), (x + rng.uniform(-1, 1), y + rng.uniform(1, 2.4))], .14, color='05201C', alfa=.35)
    for x, y, w in ((16, 14, 20), (40, 15.6, 18), (82, 15, 22), (108, 13, 16)):
        nube(l, x, y, w, .8)
    cordillera(l, [(-2, 26), (18, 21), (40, 23), (60, 20.4), (82, 22.6), (104, 20.6), (122, 23)], material='cuerpo', linea=.3)
    prado(l, 28, 41.6, .26)
    # el río General que nace a sus pies y baja hacia nosotros
    agua(l, cinta([(62, 31), (60, 34), (63, 37.6), (61, 41.8)], [2, 3.4, 5, 7], 10), ondas=3, semilla=2, linea=.3)
    for x in (30, 44, 80, 94, 12, 108):
        arbol(l, x, 30 + (x % 4), 2.4, material='lejos', semilla=x)
    # el general dorado, protagonista, que saluda al pie del Chirripó
    l.mancha(ovalo(60, 31.2, 7, .9), '0C3A33', .3, difuso=.4)
    general(l, 60, 31, 1.08)


# ------------------------------------------------------------------------------------------------ San Isidro
def labrador(l, x, base, s=1.0):
    """San Isidro labrador, de frente: la túnica dorada con su cinto, las sandalias, la azada al hombro, la aureola, y de sombrero un
    cerro entero, de roca, como el Chirripó"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    piel(l, [O(-1.8, -.5, 1.3, .5), O(1.8, -.5, 1.3, .5)])
    tunica = [forma(P([(-3.4, -17.6), (3.4, -17.6), (4, -12), (5, -1), (-5, -1), (-4, -12)]), 2),
              tubo(P([(3, -16.8), (5.2, -13.6), (5.6, -10.6)]), [1 * s, .9 * s, .8 * s], 5), tubo(P([(-3, -16.8), (-5.4, -14.4), (-6.4, -12)]), [1 * s, .9 * s, .8 * s], 5)]
    m = l.masa(tunica, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    for u in (-2.4, 0, 2.4):
        l.trazo(P([(u * .5, -10), (u, -1.6)]), [.05, .16, .05], color='6B4E10', alfa=.45, dentro=m)
    l.mancha(Polygon(P([(-4, -11.4), (4, -11.4), (4, -10.4), (-4, -10.4)])), MADERA, .7, dentro=m)   # el cinto de cuerda
    # la azada: el cabo largo y la hoja
    l.trazo(P([(-9, -24), (-5.6, -11)]), .35 * s, color=MADERA, alfa=.95)
    l.masa(forma(P([(-10.4, -24.6), (-7.6, -25.2), (-7.4, -23), (-10, -22.4)]), 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    piel(l, [O(5.6, -10.4, .9, .9), O(-6.6, -12, .9, .9), O(0, -20.2, 2.2, 2.5), box(x - .7 * s, base - 18.6 * s, x + .7 * s, base - 17.4 * s)], .45)
    l.masa(forma(P([(-2.2, -20), (-1.8, -18.2), (0, -17.4), (1.8, -18.2), (2.2, -20), (1, -19.2), (0, -19.6), (-1, -19.2)]), 1), material='oscuro', alto=.3,
           brillo=.3, vientre=0, hondo=0, linea=.25)                     # la barba
    for dx in (-.85, .85):
        l.mancha(O(dx, -20.8, .26, .3), '05201C', 1)
    l.masa(forma(P([(-2.4, -20.4), (-2.2, -22.4), (0, -23), (2.2, -22.4), (2.4, -20.4), (1.6, -21.4), (-1.6, -21.4)]), 1), material='oscuro', alto=.35,
           brillo=.3, vientre=0, hondo=0, linea=.25)                     # el pelo
    halo = O(0, -22.8, 3.6, 3.6).difference(O(0, -22.8, 2.8, 2.8))
    l.masa(halo, material='acento', alto=.3, brillo=.6, vientre=0, hondo=0, linea=.25)
    # el sombrero: un cerro de roca con su ala de bosque
    cerro = Polygon(P([(-8, -23.2), (-5.6, -26.6), (-4.4, -26), (-2.6, -30.4), (-1.4, -29.6), (.4, -34.6), (2, -31.6), (3.2, -32.2), (5.4, -27.4),
                       (8, -23.2), (0, -22.6)]))
    c = l.masa(cerro, material='claro', alto=.4, brillo=.15, vientre=0, hondo=.1, linea=.4, escalon=.3, contraluz=.35)
    l.mancha(cerro.buffer(1), GRIS, .55, dentro=c)
    for u in (-3, 0, 2.6):
        l.trazo(P([(u, -32), (u * 1.6, -26)]), .16 * s, color='3A4A47', alfa=.5, dentro=c)
    for u, v in ((-4, -27.4), (3.6, -28.4), (-1, -25.6)):              # las matas de páramo
        l.mancha(O(u, v, 1, .6), '2F8A74', .7, dentro=c)
    for dx, dy, r in ((-3.4, -32, 1.6), (-1.6, -32.8, 1.8), (.6, -32.4, 1.5)):   # la nube de la cumbre
        l.mancha(O(dx, dy, r * 1.4, r * .8), 'FFFFFF', .85, difuso=.3)
    l.masa(O(0, -23.4, 8.6, .9), material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)      # el ala, de bosque


def san_isidro(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 104, 3.6, 10, .4)
    # el valle del General, con sus cafetales, y la iglesia
    cordillera(l, [(-2, 14), (24, 10), (48, 12.4), (74, 9.6), (100, 12), (122, 10)], material='lejos')
    m = l.masa(Polygon([(-2, 41.6), (-2, 19), (30, 17.4), (60, 18.6), (90, 17), (122, 18.6), (122, 41.6)]), material='cuerpo', alto=.2, brillo=.05, vientre=0,
               hondo=0, linea=.3)
    for dy in (2.4, 5, 7.6):
        for x in np.arange(0, 122, 1.6):
            l.mancha(ovalo(x, 18 + dy + .6 * math.sin(x / 7), .8, .55), '164F46', .55, dentro=m)
    prado(l, 27, 41.6, .28)
    ig = l.masa([box(86, 14, 104, 27), box(92, 7, 98, 14.2)], material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(91.4, 7.2), (95, 3.6), (98.6, 7.2)]), material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(forma([(93.6, 27), (93.6, 21.6), (95, 20.4), (96.4, 21.6), (96.4, 27)], 1), '164F46', .85, dentro=ig)
    for x in (8, 16, 24):
        casa(l, x, 27.6, 6, 4)
    # San Isidro, protagonista, con su cerro de sombrero
    l.mancha(ovalo(60, 39.6, 8, .9), '0C3A33', .3, difuso=.4)
    labrador(l, 60, 39.6, 1.06)


# ------------------------------------------------------------------------------------------------ Volcán
def pina(l, x, y, s=1.0, giro=0.0):
    """una piña dorada: el cuerpo ovalado con su red de escamas y la corona de hojas verdes, en punta; `giro` la inclina"""
    G = lambda g: affinity.rotate(g, giro, origin=(x, y))
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    hojas = [Polygon(P([(-.4, -2), (u, -2 - h), (.4, -2)])) for u, h in ((-1.6, 2.2), (-.8, 3), (0, 3.6), (.8, 3), (1.6, 2.2))]
    l.masa([G(g) for g in hojas], material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    cuerpo = G(ovalo(x, y, 1.6 * s, 2.3 * s))
    m = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for k in range(-3, 4):                                               # la red de escamas
        for lado in (-1, 1):
            a, b = G(Polygon(P([(k * .9 - 2, -2.4), (k * .9 + 2, 2.4), (k * .9 + 2.1, 2.4)]))).exterior.coords[:2] if lado > 0 else \
                G(Polygon(P([(k * .9 + 2, -2.4), (k * .9 - 2, 2.4), (k * .9 - 2.1, 2.4)]))).exterior.coords[:2]
            l.trazo([a, b], .1 * s, color='6B4E10', alfa=.5, dentro=m)


def volcan(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 18, 4, 12, .45)
    nube(l, 106, 3.6, 10, .4)
    # el volcán, al medio, con su cráter, y los piñales en hileras alrededor
    cordillera(l, [(-2, 22), (20, 19), (40, 20.6)], material='lejos')
    cordillera(l, [(80, 20.6), (100, 18.6), (122, 21)], material='lejos')
    v = l.masa(Polygon([(26, 30), (50, 14), (54, 12.6), (66, 12.6), (70, 14), (94, 30)]), material='lejos', alto=.4, brillo=.12, vientre=0, hondo=.1, linea=.4,
               escalon=.3, contraluz=.35)
    l.mancha(Polygon([(26, 31), (50, 14), (54, 12.6), (66, 12.6), (70, 14), (94, 31)]), MADERA, .35, dentro=v)
    l.mancha(ovalo(60, 12.8, 6, 1.2), '3A2A0A', .8)                      # el cráter
    for u in (-14, -6, 4, 12):
        l.trazo([(60 + u * .3, 14), (60 + u, 28)], .16, color='3A2A0A', alfa=.35, dentro=v)
    prado(l, 28, 41.6, .3)
    for y in np.arange(29.6, 41, 2.2):                                   # las hileras de piña
        for x in np.arange(-1 + (y * 1.7) % 2.6, 122, 2.6):
            l.trazo([(x - .8, y), (x, y - 1.2 - (y - 29) * .06), (x + .8, y)], .16 + (y - 29) * .006, color='2F8A74', alfa=.85)
    # las piñas doradas, protagonistas, que el volcán escupe en vez de lava
    for k, (u, v_, s, g) in enumerate(((60, 4.6, 1.15, 0), (46, 6.6, 1.05, -30), (74, 6.2, 1.05, 30), (36, 14, 1.1, -55), (84, 13, 1.1, 50), (52, 1.8, .9, -15),
                                      (68, 2, .9, 20))):
        pina(l, u, v_, s, g)
    for t in np.linspace(.15, .85, 5):                                   # los arcos del vuelo
        for lado in (-1, 1):
            x0 = 60 + lado * t * 26
            l.trazo([(x0, 10 - 8 * math.sin(t * math.pi) + 2), (x0 + lado * 1.4, 10.6 - 8 * math.sin((t + .05) * math.pi) + 2)], .2, color='0C3A33', alfa=.4)
    for x, s, g in ((20, 1.2, -15), (100, 1.2, 12), (10, 1, 8), (110, 1, -8)):   # las que ya cayeron en el piñal
        pina(l, x, 33 + (x % 3), s, g)


# ------------------------------------------------------------------------------------------------ Paso Real
def rey(l, x, base, s=1.0):
    """un rey dorado, de pie y de frente, con su corona, su manto con cuello de armiño y la jarra con la que bautiza"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    manto = [forma(P([(-5, 0), (-5.6, -6), (-5, -12), (-3.6, -16.6), (3.6, -16.6), (5, -12), (5.6, -6), (5, 0)]), 2),
             tubo(P([(3.4, -15.6), (6.4, -14), (8.6, -13.4)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(-3.4, -15.6), (-5.2, -12), (-4.4, -9.6)]), [1.1 * s, 1 * s, .9 * s], 5)]
    m = l.masa(manto, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for u in (-3, -1, 1, 3):
        l.trazo(P([(u * .7, -13), (u * 1.3, -1)]), [.05, .18, .05], color='6B4E10', alfa=.5, dentro=m)
    arm = l.masa(forma(P([(-4, -16.6), (-3, -13.4), (0, -12.4), (3, -13.4), (4, -16.6), (0, -15.4)]), 1), material='claro', alto=.4, brillo=.3, vientre=0,
                 hondo=0, linea=.3)
    for u, v in ((-2.2, -14.6), (0, -13.4), (2.2, -14.6)):
        l.mancha(O(u, v, .28, .36), '0C3A33', .9, dentro=arm)
    piel(l, [O(0, -19, 2.2, 2.5), O(-4.4, -9.4, .9, .9), O(8.8, -13.6, .9, .9)])
    l.masa(forma(P([(-2.2, -18.4), (-1.8, -16.4), (0, -15.8), (1.8, -16.4), (2.2, -18.4), (0, -17.4)]), 1), material='claro', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.25)                                           # la barba
    for dx in (-.8, .8):
        l.mancha(O(dx, -19.6, .26, .3), '05201C', 1)
    corona = forma(P([(-2.6, -21), (-3, -24.4), (-1.6, -22.8), (-.8, -25.6), (0, -23), (.8, -25.6), (1.6, -22.8), (3, -24.4), (2.6, -21)]), 0)
    l.masa(corona, material='acento', alto=.5, brillo=.6, vientre=0, hondo=0, linea=.3, contraluz=.4)
    jarra = forma(P([(8.4, -13.8), (10.6, -12.6), (12.4, -12.8), (12.6, -14.6), (11.4, -16.6), (9.4, -16.4)]), 2)
    l.masa(jarra, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.35)
    return P([(12.6, -13.2)])[0]


def mano_agua(l, x0, y0, x1, y1, lado=1):
    """un brazo de agua que sale del río y termina en una mano que aprieta la otra"""
    g = unary_union([cinta([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 1.4), (x1, y1)], [3.4, 2.4, 1.8], 8), ovalo(x1 + lado * 1, y1, 2.2, 1.7)])
    m = l.masa(g, material='lejos', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.mancha(g, '64C8AA', .45, dentro=m)
    for k in range(3):
        l.trazo([(x1 + lado * (.2 + k * .8), y1 - 1.4), (x1 + lado * (.4 + k * .8), y1 + .6)], .12, color='0C3A33', alfa=.5, dentro=m)
    return m


def paso_real(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 104, 3.6, 10, .4)
    cordillera(l, [(-2, 16), (22, 12), (46, 14.4), (70, 11.4), (96, 14), (122, 12)], material='lejos')
    prado(l, 18, 41.6, .3)
    # los dos ríos que llegan, el General por la izquierda y el Coto Brus por la derecha, y se juntan abajo en el Térraba
    agua(l, unary_union([cinta([(-2, 28), (20, 31), (44, 34.6), (60, 37)], [4, 5, 6, 7], 8), cinta([(122, 27), (100, 30.6), (76, 34.6), (60, 37)], [4, 5, 6, 7], 8),
                         cinta([(60, 37), (60, 41.8)], [10, 13], 3)]), ondas=10, semilla=6, linea=.35)
    # el puente de la Interamericana, con su baranda
    for x in (20, 100):
        l.masa(box(x - 2, 21, x + 2, 32), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.masa(box(-2, 20.2, 122, 22.4), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.trazo([(-2, 17.8), (122, 17.8)], .3, color='8EB5AA', alfa=.95)
    for x in np.arange(0, 122, 4):
        l.trazo([(x, 17.8), (x, 20.4)], .25, color='8EB5AA', alfa=.95)
    # las dos manos de agua que se dan la mano bajo el puente
    mano_agua(l, 44, 35, 57.4, 28.6, 1)
    mano_agua(l, 76, 35, 62.6, 28.6, -1)
    # el rey dorado, protagonista, que los bautiza con su jarra desde el puente
    pico = rey(l, 48, 20.4, .76)
    for k in range(4):                                                   # el agua del bautizo, que cae sobre las manos
        l.trazo([(pico[0] + k * .5, pico[1] + .4), (pico[0] + 1.6 + k * .6, pico[1] + 6), (pico[0] + 1.4 + k * .5, pico[1] + 15)], .3, color='9BDDBD', alfa=.9)
    for x, y in ((58, 26.4), (62, 26), (60, 25)):
        l.mancha(ovalo(x, y, .5, .7), 'D2F2DA', .95)


# ------------------------------------------------------------------------------------------------ Rey Curré
def diablito(l, x, base, s=1.0):
    """el rey que baila, de frente, con la máscara de diablito boruca, dorada: los cuernos, los ojos grandes, la nariz y los dientes;
    la corona encima, la capa y el traje de gangoche, un brazo arriba y una pierna levantada"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    capa = forma(P([(-3.8, -17.4), (-5.6, -12), (-6.4, -5), (-5.4, -3.4), (5.4, -3.4), (6.4, -5), (5.6, -12), (3.8, -17.4)]), 2)
    l.masa(capa, material='lejos', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    traje = [forma(P([(-3.6, -17), (3.6, -17), (4, -11), (3.6, -6), (-3.6, -6), (-4, -11)]), 1),
             tubo(P([(-1.6, -6.4), (-2.2, -3), (-2.6, 0)]), [1.2 * s, 1 * s, .9 * s], 5), tubo(P([(1.6, -6.4), (4.2, -5.4), (5.4, -2.6)]), [1.2 * s, 1 * s, .9 * s], 5),
             tubo(P([(3.4, -16.4), (6.4, -18.4), (7.4, -21.4)]), [1 * s, .9 * s, .8 * s], 5), tubo(P([(-3.4, -16.4), (-6.4, -15), (-8.4, -16.4)]), [1 * s, .9 * s, .8 * s], 5)]
    m = l.masa(traje, material='vientre', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.mancha(unary_union(traje).buffer(1), '8A6A3A', .55, dentro=m)
    for k in range(6):                                                   # los flecos de gangoche y de hojas
        l.trazo(P([(-3.4 + k * 1.4, -7), (-3.6 + k * 1.4, -4.6)]), .2 * s, color='3A2A0A', alfa=.5)
    l.masa([O(-2.8, 0, 1.4, .6), O(5.8, -2.2, 1.3, .6, -30)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    piel(l, [O(7.6, -22, .9, .9), O(-9, -16.6, .9, .9)])
    # la máscara de diablito, dorada, con sus cuernos
    mascara = unary_union([forma(P([(-3.6, -26), (-3.8, -21.4), (-2, -18.4), (2, -18.4), (3.8, -21.4), (3.6, -26), (0, -27.2)]), 2),
                           tubo(P([(-3, -26.4), (-5.4, -29), (-5, -32)]), [.9 * s, .6 * s, .2 * s], 6), tubo(P([(3, -26.4), (5.4, -29), (5, -32)]), [.9 * s, .6 * s, .2 * s], 6)])
    mm = l.masa(mascara, material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for dx in (-1.6, 1.6):                                               # los ojos grandes, pintados
        l.mancha(O(dx, -23.6, 1.1, .9), 'FFFFFF', .95, dentro=mm)
        l.mancha(O(dx, -23.5, .5, .55), '05201C', 1, dentro=mm)
        l.trazo(P([(dx * .4, -25.4), (dx * 1.6, -26), (dx * 2.8, -25.4)]), .3 * s, color='3A2A0A', alfa=.9, dentro=mm)
    l.mancha(forma(P([(-.6, -23), (0, -21.4), (.6, -23)]), 1), '6B4E10', .6, dentro=mm)
    l.mancha(forma(P([(-2.4, -20.4), (2.4, -20.4), (1.6, -19), (-1.6, -19)]), 1), '3A2A0A', .9, dentro=mm)          # la boca
    for u in (-1.6, -.5, .6, 1.6):
        l.mancha(Polygon(P([(u - .4, -20.4), (u + .4, -20.4), (u, -19.5)])), 'FFFFFF', .95)
    corona = forma(P([(-2.2, -26.6), (-2.6, -29), (-1.2, -27.8), (0, -30), (1.2, -27.8), (2.6, -29), (2.2, -26.6)]), 0)
    c = l.masa(corona, material='claro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)
    l.mancha(corona.buffer(1), GRIS, .4, dentro=c)


def rey_curre(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 104, 3.6, 10, .4)
    cordillera(l, [(-2, 15), (24, 11), (50, 13.6), (76, 10.6), (100, 13), (122, 11)], material='lejos')
    prado(l, 17, 41.6, .3)
    for x, w, h in ((84, 6, 3.6), (91, 5.6, 3.2), (98, 6.4, 3.8), (6, 6, 3.6)):
        casa(l, x, 20.6, w, h)
    rio(l, 22.4)
    orilla(l, forma([(-2, 41.6), (-2, 32), (40, 30.4), (80, 30.6), (122, 32), (122, 41.6)], 2), tinte=.32)
    for x, h in ((12, 12), (108, 13)):
        banano(l, x, 38, h, semilla=x)
    # el rey dorado de máscara de diablito, protagonista, que baila a la orilla
    l.mancha(ovalo(60, 38.6, 8, .9), '0C3A33', .3, difuso=.4)
    diablito(l, 60, 38.4, 1.08)
    for x, y in ((46, 20), (74, 18), (44, 30), (78, 28)):                # el baile
        l.trazo([(x - 1, y), (x, y - 1), (x + 1, y)], .25, color='0C3A33', alfa=.55)


# ------------------------------------------------------------------------------------------------ Palmar
def esfera(l, x, y, r, rueda=True):
    """una esfera de piedra dorada, perfecta, con su sombra y, si rueda, las rayas del movimiento"""
    l.mancha(ovalo(x + r * .2, y + r * .95, r * 1.1, r * .2), '0C3A33', .35, difuso=.4)
    m = l.masa(ovalo(x, y, r, r), material='acento', alto=.7, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    rng = np.random.default_rng(int(x * 7))
    for _ in range(int(r * 3)):                                          # el grano de la piedra
        a, d = rng.uniform(0, 2 * math.pi), rng.uniform(0, r * .85)
        l.mancha(ovalo(x + math.cos(a) * d, y + math.sin(a) * d, .25, .2), '6B4E10', .3, dentro=m)
    if rueda:
        for k in range(3):
            l.trazo([(x - r * 1.3 - k * 1.6, y - r * .4 + k * r * .4), (x - r * 2.4 - k * 2.4, y - r * .4 + k * r * .4)], .3, color='0C3A33', alfa=.45)


def palmar(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    nube(l, 96, 3.6, 10, .4)
    cordillera(l, [(-2, 14), (24, 10.6), (48, 12.6), (74, 9.4), (100, 12), (122, 10.6)], material='lejos')
    prado(l, 18, 41.6, .3)
    # la fila de palmeras, atrás, y los bananos
    for x in np.arange(4, 122, 9):
        palmera(l, x, 20, 9, 1, datiles=False)
    for x, h in ((10, 13), (30, 11), (90, 12), (110, 13.6), (100, 10)):
        banano(l, x, 33, h, semilla=x, racimo=True)
    # las esferas de piedra doradas, protagonistas, que ruedan entre los bananos
    esfera(l, 70, 25.4, 3.2)
    esfera(l, 44, 27, 4)
    esfera(l, 62, 30.4, 9.4)


# ------------------------------------------------------------------------------------------------ Ciudad Cortés
def conquistador(l, x, base, s=1.0):
    """un conquistador de frente, con el morrión de cresta y la coraza de acero, las calzas abombadas, la espada al cinto y unas
    botas de hule doradas hasta las rodillas; (x, base) es donde pisa, bajo el agua"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    botas = [forma(P([(-5.4, 0), (-5.2, -11.8), (-.8, -12), (-.6, -1.2), (-.4, 0)]), 1), forma(P([(.4, 0), (.6, -1.2), (.8, -12), (5.2, -11.8), (5.4, 0)]), 1)]
    b = l.masa(botas, material='acento', alto=.55, brillo=.55, vientre=0, hondo=.1, linea=.45, contraluz=.45)
    for dx in (-3, 3):
        l.trazo(P([(dx - 2.2, -10.8), (dx + 2.2, -10.8)]), .5 * s, color='6B4E10', alfa=.6, dentro=b)        # el borde de arriba
        l.trazo(P([(dx - 2.4, -.7), (dx + 2.4, -.7)]), .6 * s, color='3A2A0A', alfa=.75, dentro=b)          # la suela
        l.trazo(P([(dx - 1, -9.8), (dx - .8, -2.4)]), [.05, .45, .05], color='FBEFCB', alfa=.9, dentro=b)   # el brillo del hule
    base -= 2.8 * s                                                      # lo de arriba, encima de las botas altas
    calzas = [O(-2.4, -11, 2.4, 2.4), O(2.4, -11, 2.4, 2.4)]
    cm = l.masa(calzas, material='claro', alto=.45, brillo=.3, vientre=0, hondo=0, linea=.35)
    l.mancha(unary_union(calzas).buffer(1), 'C8584A', .38, dentro=cm)
    for u in (-3, -1.6, 1.6, 3):
        l.trazo(P([(u, -13), (u, -9)]), .14 * s, color='3A2A0A', alfa=.4, dentro=cm)
    coraza = [forma(P([(-4.4, -21), (4.4, -21), (4.6, -16), (3.6, -12.4), (-3.6, -12.4), (-4.6, -16)]), 2),
              tubo(P([(4, -20.4), (6, -17), (6.4, -13.4)]), [1.2 * s, 1.1 * s, 1 * s], 5), tubo(P([(-4, -20.4), (-6, -17), (-6.4, -13.4)]), [1.2 * s, 1.1 * s, 1 * s], 5)]
    a = l.masa(coraza, material='claro', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.3, contraluz=.4)
    l.mancha(unary_union(coraza).buffer(1), GRIS, .4, dentro=a)
    l.trazo(P([(0, -20.6), (0, -13)]), [.05, .3, .05], color='FFFFFF', alfa=.8, dentro=a)
    l.trazo(P([(-4.4, -13.4), (4.4, -13.4)]), .4 * s, color='3A2A0A', alfa=.8)                     # el cinto
    l.trazo(P([(-4.4, -13.2), (-8.4, -4.6)]), .4 * s, color='6E7E7B', alfa=.95)                    # la espada
    l.trazo(P([(-5.2, -14.6), (-3.6, -12)]), .4 * s, color='3A2A0A', alfa=.9)
    piel(l, [O(6.4, -12.6, .9, .9), O(-6.4, -12.6, .9, .9), O(0, -23.2, 2.2, 2.5), box(x - .7 * s, base - 21.6 * s, x + .7 * s, base - 20.6 * s)])
    l.masa(forma(P([(-1.8, -22.4), (-1.4, -20.8), (0, -20.2), (1.4, -20.8), (1.8, -22.4), (0, -21.6)]), 1), material='oscuro', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.25)                                           # la barba
    for dx in (-.85, .85):
        l.mancha(O(dx, -23.6, .26, .3), '05201C', 1)
    morrion = [forma(P([(-5.6, -24.6), (-3, -25.6), (-2.6, -27.8), (0, -28.6), (2.6, -27.8), (3, -25.6), (5.6, -24.6), (3.4, -24.8), (0, -25),
                       (-3.4, -24.8)]), 2), forma(P([(-2, -28), (0, -30.2), (2, -28)]), 1)]
    mo = l.masa(morrion, material='claro', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.mancha(unary_union(morrion).buffer(1), GRIS, .45, dentro=mo)


def ciudad_cortes(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    for x, y, w in ((22, 4, 16), (60, 3.4, 20), (100, 4.4, 16)):
        nube(l, x, y, w, .7)
    for _ in range(26):                                                  # la lluvia
        x, y = rng.uniform(0, 120), rng.uniform(6, 16)
        l.trazo([(x, y), (x - .6, y + 2)], .1, color='8EB5AA', alfa=.6)
    # las casas del pueblo, con el agua hasta la puerta, y las matas de banano
    prado(l, 16, 24, .26)
    for x, w, h in ((-1, 7, 6), (7, 6.4, 5.2), (14.4, 7.4, 6.4), (88, 7, 6), (96, 6.4, 5.4), (103.4, 7.4, 6.2), (111.6, 7, 5.6)):
        casa(l, x, 24, w, h)
    for x, h in ((26, 11), (80, 10)):
        banano(l, x, 24, h, semilla=x)
    agua(l, box(-2, 22.6, 122, 41.6), ondas=16, semilla=11, linea=0)
    l.mancha(box(-2, 22.6, 122, 41.6), '8A6A3A', .3)                     # el agua café de la crecida
    # el conquistador, protagonista, con sus botas de hule doradas metidas en la inundación
    conquistador(l, 60, 38.8, 1.08)
    for dx in (-3.2, 3.2):                                               # el agua en los tobillos, con sus ondas
        cx = 60 + dx * 1.08
        l.mancha(ovalo(cx, 38.6, 4.4, .9), '7FA79A', .7)
        for k in range(2):
            l.trazo([(cx - 4.6 - k * 1.6, 38.8 + k * .7), (cx, 39.4 + k * .7), (cx + 4.6 + k * 1.6, 38.8 + k * .7)], .22, color='E6F3EE', alfa=.85)


# ------------------------------------------------------------------------------------------------ el mar
def lancha_pinas(l, x, y, s=1.0):
    """la lancha de Puerto Cortés, la barca del juego, mirando a la derecha: larga y baja, de casco dorado, con el motor fuera de borda
    y la carga de piñas y sacos; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([forma(P([(-19, -5), (-16.4, -5.2), (-16.2, -2.2), (-18.8, -2.2)]), 1), box(x - 18.2 * s, y - 2.4 * s, x - 17.4 * s, y + 1.6 * s)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    for u, w in ((-9, 4.4), (-4, 4)):                                    # los sacos
        f = l.masa(forma(P([(u - w / 2, -1.4), (u - w / 2, -4.2), (u + w / 2, -4.4), (u + w / 2, -1.4)]), 2), material='vientre', alto=.4, brillo=.2,
                   vientre=0, hondo=0, linea=.25)
        l.mancha(forma(P([(u - w, 0), (u + w, 0), (u + w, -6), (u - w, -6)]), 0), 'BF9129', .3, dentro=f)
    for k in range(5):                                                   # las piñas, con su corona
        u = 1 + k * 2.4
        l.masa([Polygon(P([(u - .5, -3.6), (u - .9, -5.6), (u, -4.2), (u + .9, -5.6), (u + .5, -3.6)]))], material='cuerpo', alto=.3, brillo=.2, vientre=0,
               hondo=0, linea=.2)
        m = l.masa(ovalo(x + u * s, y - 2.4 * s, .9 * s, 1.3 * s), material='vientre', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.22)
        l.mancha(ovalo(x + u * s, y - 2.4 * s, 1.2 * s, 1.6 * s), 'BF9129', .55, dentro=m)
    casco = forma(P([(-17, -2.6), (-15, -1.2), (15, -1.2), (18.4, -3.2), (16.6, .6), (11, 1.4), (-13, 1.4), (-16.6, .6)]), 2)
    c = l.masa(casco, material='acento', alto=.45, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-16.4, -1.8), (0, -.9), (17.4, -2.4)]), [.05, .4, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco


def cangrejo(l, x, y, s=1.0):
    """Pinzas, el cangrejo del manglar, rojo, de frente, con sus pinzas levantadas"""
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, y + v * s, rx * s, ry * s, a)
    g = [O(0, 0, 1.8, 1.2), O(-2.4, -1.6, .8, .6, -30), O(2.4, -1.6, .8, .6, 30)] + \
        [tubo([(x + d * 1.4 * s, y + .4 * s), (x + d * 2.6 * s, y + 1.4 * s)], [.2 * s, .15 * s], 2) for d in (-1, 1)] + \
        [tubo([(x + d * 1.2 * s, y - .6 * s), (x + d * 2 * s, y - 1.2 * s)], [.3 * s, .3 * s], 2) for d in (-1, 1)]
    m = l.masa(g, material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.25)
    l.mancha(unary_union(g).buffer(1), 'C8423A', .85, dentro=m)
    for dx in (-.5, .5):
        l.mancha(O(dx, -1.4, .25, .25), '05201C', 1)


def mar(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 40, 5, 14, .5)
    nube(l, 100, 4, 12, .45)
    horizonte = 17
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2), '64C8AA', .5, dentro=m, difuso=.8)
    for y in (19.4, 22):                                                 # el oleaje del Pacífico, afuera
        for x in np.arange(30, 92, 8):
            l.trazo([(x, y + .4), (x + 3, y - .4), (x + 6, y + .4)], .3, color='FFFFFF', alfa=.6)
    for _ in range(14):
        x, y = rng.uniform(30, 90), rng.uniform(24, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # los manglares de Térraba-Sierpe, apretados, a los dos lados, y las garzas que vuelan
    for x0, x1 in ((-2, 30), (90, 122)):
        orilla(l, forma([(x0, 41.6), (x0, 22), (x1, 23), (x1 + (2 if x0 < 0 else -2), 41.6)], 1), tinte=.25, linea=.25)
        for k, x in enumerate(np.arange(x0 + 3, x1, 6.4)):
            mangle(l, x, 30 + (k % 2) * 7, 12 + (k % 3), semilla=int(x))
    for x, y, s in ((40, 7, .7), (46, 5.4, .6), (52, 7.4, .65), (76, 6, .6), (82, 8, .55)):
        ave(l, x, y, s)
    cangrejo(l, 101, 33.6, 1)
    # la lancha de Puerto Cortés, la barca del juego, protagonista, que sale al Pacífico
    g = lancha_pinas(l, 60, 32.4, 1.4)
    reflejo(l, g, 32.8, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='San Isidro', dibujar=san_isidro), dict(clave='Volcán', dibujar=volcan),
            dict(clave='Paso Real', dibujar=paso_real), dict(clave='Rey Curré', dibujar=rey_curre), dict(clave='Palmar', dibujar=palmar),
            dict(clave='Ciudad Cortés', dibujar=ciudad_cortes), dict(clave='mar', dibujar=mar)]
LISTO = True
