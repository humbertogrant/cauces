# -*- coding: utf-8 -*-
"""Las postales del Sarapiquí, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: el lado norte de los volcanes Poás y Barva, con su selva, y el río dorado que nace entre ellos y baja de catarata en
  catarata;
- San Miguel: «un arcángel con paraguas se baña bajo una catarata»: el arcángel de alas y aureola doradas y túnica blanca, de pie en
  la poza, y el agua que le cae sobre el paraguas;
- La Virgen: «una virgen de yeso con chaleco salvavidas se sube a una balsa»: la virgen blanca, de yeso, en su pedestal, con su chaleco
  salvavidas dorado, subida a la balsa; atrás, el puente colgante sobre el río y la selva;
- Chilamate: «un higuerón gigante con un mate colgando de cada rama»: el higuerón de la orilla, ancho y de raíces tablares, con los
  mates dorados, cada uno con su bombilla, que cuelgan de las ramas;
- Puerto Viejo: «un muelle viejo con mulas cansadas que se bajan a un bote»: las mulas doradas, con sus alforjas y las orejas caídas,
  que pasan del muelle torcido al bote; en la selva de atrás, un mono;
- Trinidad: «una trinidad de botes se da la mano en la esquina de dos países»: los tres botes dorados, con sus ojos, que se dan la
  mano en la boca del Sarapiquí, con la bandera de Costa Rica de este lado y la de Nicaragua enfrente;
- el mar: el bote del Sarapiquí, la barca del juego, de casco dorado, que entra al San Juan ancho; enfrente, la orilla de Nicaragua,
  y de este lado Bruno, el mono congo, que los despide con un grito.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, nube, orilla, palmera, pasto, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import forma, ovalo, tubo

PIEL = 'A2683A'            # el tono de la piel: un café tibio sobre el pálido de `vientre`
MADERA = '5A3E1E'


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


def bote(l, x, y, s=1.0, material='vientre', tinte=MADERA, motor=True):
    """el bote de Sarapiquí de perfil, mirando a la derecha: largo y angosto, de tablas, con la borda pintada, las bancas y el motor
    fuera de borda en la popa; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    if motor:
        l.masa([forma(P([(-17.6, -5.4), (-15, -5.6), (-14.8, -2.4), (-17.4, -2.4)]), 1), box(x - 16.8 * s, y - 2.6 * s, x - 16 * s, y + 1.6 * s)],
               material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    casco = forma(P([(-16, -2.8), (-14, -1.4), (14, -1.4), (17.4, -3.4), (15.6, .6), (10, 1.4), (-12, 1.4), (-15.6, .6)]), 2)
    c = l.masa(casco, material=material, alto=.45, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    if tinte:
        l.mancha(casco.buffer(1), tinte, .55, dentro=c)
    l.trazo(P([(-15.4, -1.8), (0, -.9), (16.4, -2.6)]), [.05, .45, .05], color='164F46' if tinte else '6B4E10', alfa=.6, dentro=c)   # la borda
    for k in range(2):                                                   # las tablas
        l.trazo(P([(-13 + k * 2, .2 + k * .7), (0, .5 + k * .7), (13 - k * 2, -.2 + k * .7)]), [.05, .12, .05], color='3A2A0A', alfa=.35, dentro=c)
    return casco


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 30, 3.6, 12, .45)
    # el Poás, ancho y chato, con su cráter, y el Barva, redondo, con la selva que les sube por la falda
    cordillera(l, [(-2, 16), (10, 10), (22, 5.4), (28, 4.6), (31, 5.4), (34, 4.6), (42, 6), (54, 11), (66, 9), (78, 5.6), (88, 4.4), (98, 5.6),
                   (110, 10), (122, 13)], material='lejos')
    for x, y, w in ((60, 9.4, 16), (100, 3.4, 12)):
        nube(l, x, y, w, .55)
    selva(l, -2, 122, 22, 8, semilla=2, emergentes=4)
    m = l.masa(Polygon([(-2, 41.6), (-2, 21), (40, 20), (80, 20.4), (122, 21), (122, 41.6)]), material='cuerpo', alto=.2, brillo=.05, vientre=0, hondo=0,
               linea=.3)
    for _ in range(60):
        x, y = rng.uniform(0, 120), rng.uniform(22, 41)
        l.mancha(ovalo(x, y, rng.uniform(.8, 1.6), rng.uniform(.6, 1)), str(rng.choice(['164F46', '4AA189'])), .35, dentro=m)
    # el río dorado, protagonista, que nace entre los dos volcanes y baja de catarata en catarata, con sus pozas
    caidas = ((57, 63, 13, 19.6), (52.4, 61.6, 22.6, 29.4), (55, 67, 32.4, 38.6))
    tramos = [cinta([(60, 10.4), (59.4, 12), (60, 13.4)], [1.2, 2.6, 5], 4), box(57, 13, 63, 19.6), ovalo(59.6, 20.6, 7.6, 2),
              cinta([(59.6, 21), (56, 22.6)], [7, 9], 3), box(52.4, 22.6, 61.6, 29.4), ovalo(57.4, 30.2, 9, 2.2),
              cinta([(57.4, 30.6), (61, 32.4)], [9, 12], 3), box(55, 32.4, 67, 38.6), ovalo(61, 39.4, 11, 2.4), cinta([(61, 40), (60.4, 41.8)], [14, 15], 2)]
    g = unary_union(tramos)
    rio_ = l.masa(g, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.4, escalon=.1, contraluz=.3)
    for x0, x1, y0, y1 in caidas:                                        # los hilos de agua de cada caída
        for x in np.arange(x0 + .6, x1, .9):
            l.trazo([(x, y0 + .4), (x + .1, y1 - .2)], .16, color='FBEFCB', alfa=.85, dentro=rio_)
        l.mancha(ovalo((x0 + x1) / 2, y1 + .4, (x1 - x0) * .9, 1.2), 'FFFFFF', .8, difuso=.5)       # la espuma al pie


# ------------------------------------------------------------------------------------------------ San Miguel
def arcangel(l, x, base, s=1.0):
    """un arcángel de frente, de pie en la poza: las alas doradas abiertas detrás, que suben desde los hombros con sus plumas, la
    túnica blanca con el cinto dorado, la aureola, la cara y el brazo levantado que sostiene el paraguas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    alas = []
    for lado in (-1, 1):
        borde = [(lado * 2, -17.4), (lado * 6, -22), (lado * 11, -24.4), (lado * 15.4, -24.6)]
        for k, (u0, v0) in enumerate(((15.4, -24.6), (14.4, -21.4), (13, -18.6), (11, -16), (8.4, -13.8), (5.6, -12.4))):   # las plumas largas del borde
            borde += [(lado * (u0 - .4), v0 + 1.6), (lado * (u0 - 1.6), v0 + 1.2)]
        borde += [(lado * 3, -12.6)]
        alas.append(Polygon(P(borde)).buffer(.25))
    a = l.masa(alas, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for lado in (-1, 1):                                                 # las hileras de plumas
        for k in range(3):
            l.trazo(P([(lado * (4 + k * 3.2), -20.6 + k * .4), (lado * (6 + k * 2.6), -14.6 + k * .2)]), .14 * s, color='6B4E10', alfa=.5, dentro=a)
    tunica = [forma(P([(-3.4, -17.6), (3.4, -17.6), (4, -12), (5.4, 0), (-5.4, 0), (-4, -12)]), 2),
              tubo(P([(3, -16.8), (5.6, -19.6), (6.6, -23)]), [1 * s, .9 * s, .8 * s], 5), tubo(P([(-3, -16.8), (-4.4, -13), (-2, -10.6)]), [1 * s, .9 * s, .8 * s], 5)]
    t = l.masa(tunica, material='claro', alto=.45, brillo=.3, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    for u in (-2.6, 0, 2.6):                                             # los pliegues
        l.trazo(P([(u * .6, -15), (u, -1)]), [.05, .16, .05], color='8EB5AA', alfa=.6, dentro=t)
    l.masa(Polygon(P([(-4, -11.2), (4, -11.2), (4, -9.8), (-4, -9.8)])), material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.25)   # el cinto
    piel(l, [O(6.7, -23.4, .9, .9), O(-1.8, -10.6, .9, .9), O(0, -20.2, 2.2, 2.5), box(x - .7 * s, base - 18.6 * s, x + .7 * s, base - 17.4 * s)])
    l.masa(forma(P([(-2.4, -20.6), (-2.2, -22.6), (0, -23.2), (2.2, -22.6), (2.4, -20.6), (1.6, -21.6), (-1.6, -21.6)]), 1), material='acento', alto=.4,
           brillo=.4, vientre=0, hondo=0, linea=.3)                      # el pelo
    for dx in (-.8, .8):
        l.mancha(O(dx, -20, .24, .28), '05201C', 1)
    l.trazo(P([(-.7, -18.6), (0, -18.3), (.7, -18.6)]), .15 * s, color='3A2A0A', alfa=.85)
    halo = O(0, -24.8, 3, .9).difference(O(0, -24.8, 2.2, .45))
    l.masa(halo, material='acento', alto=.3, brillo=.6, vientre=0, hondo=0, linea=.25)


def san_miguel(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    # la pared de roca con su selva, la catarata que cae desde arriba y la poza
    selva(l, -2, 122, 14, 7, semilla=4, emergentes=3)
    for pts in ([(-2, 41.6), (-2, 12), (30, 13), (44, 12.4), (48, 30), (40, 41.6)], [(122, 41.6), (122, 12), (90, 13), (76, 12.4), (72, 30), (80, 41.6)]):
        m = l.masa(forma(pts, 1), material='lejos', alto=.3, brillo=.08, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.25)
        for _ in range(30):
            px, py = rng.uniform(min(p[0] for p in pts), max(p[0] for p in pts)), rng.uniform(12, 40)
            l.mancha(ovalo(px, py, rng.uniform(.8, 1.6), rng.uniform(.6, 1)), str(rng.choice(['164F46', '2F8A74'])), .5, dentro=m)
    l.masa(box(44, 10, 76, 13), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    cae = box(48, 12.4, 72, 36)
    agua(l, cae, linea=0)
    for x in np.arange(48.6, 72, 1.1):
        l.trazo([(x, 12.6), (x + rng.uniform(-.3, .3), 24), (x, 36)], [.5, .7, .5], color='FFFFFF', alfa=.75)
    agua(l, forma([(30, 41.6), (34, 33.6), (60, 32), (86, 33.6), (90, 41.6)], 2), ondas=6, semilla=5, linea=.35)
    # el arcángel dorado, protagonista, que se baña bajo la catarata con su paraguas
    arcangel(l, 60, 39.4, 1.02)
    l.trazo([(66.8, 16), (66.8, 6.6)], .35, color='3A2A0A', alfa=.95)              # el mango del paraguas
    tela = forma([(53.2, 9.8), (56, 6.4), (61, 3.6), (66.8, 2.8), (72.6, 3.6), (77.6, 6.4), (80.4, 9.8), (77.8, 9), (75.2, 10), (72.4, 9), (69.6, 10), (66.8, 9),
                  (64, 10), (61.2, 9), (58.4, 10), (55.8, 9)], 1)
    t = l.masa(tela, material='claro', alto=.45, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.mancha(tela.buffer(1), '1E4A8C', .7, dentro=t)
    for u in (55.4, 61, 66.8, 72.6, 78.2):                               # las varillas
        l.trazo([(66.8, 2.8), (u, 9.6)], .14, color='E6F3EE', alfa=.85, dentro=t)
    l.trazo([(66.8, 2.8), (66.8, 1.2)], .3, color='3A2A0A', alfa=.95)
    for lado in (-1, 1):                                                 # el agua que rebota del paraguas
        for k in range(4):
            l.trazo([(66.8 + lado * (13 + k * .6), 9.6), (66.8 + lado * (15.4 + k * 1.4), 11.6 + k * 1.6), (66.8 + lado * (16.2 + k * 1.6), 15 + k * 2)], .3,
                    color='FFFFFF', alfa=.85)
    l.mancha(ovalo(60, 39.2, 12, 1.6), 'FFFFFF', .7, difuso=.6)


# ------------------------------------------------------------------------------------------------ La Virgen
def virgen(l, x, base, s=1.0):
    """una virgen de yeso, de frente: el manto blanco hasta los pies, el velo, la corona, la cara serena y las manos juntas, con el
    chaleco salvavidas dorado puesto encima, con sus correas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    manto = forma(P([(-4.6, 0), (-5, -6), (-4.4, -14), (-3.6, -19), (-2.6, -22.4), (0, -23.6), (2.6, -22.4), (3.6, -19), (4.4, -14), (5, -6), (4.6, 0)]), 2)
    m = l.masa(manto, material='claro', alto=.4, brillo=.25, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.3)
    for u in (-2.6, 0, 2.6):                                             # los pliegues del yeso
        l.trazo(P([(u * .6, -10), (u, -.6)]), [.05, .16, .05], color='8EB5AA', alfa=.6, dentro=m)
    l.mancha(manto.buffer(1), 'C9D8D2', .25, dentro=m)
    cy = l.masa(O(0, -19.6, 1.9, 2.2), material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.3, contraluz=.3)   # la cara, de yeso
    l.mancha(O(0, -19.6, 2.4, 2.6), 'E8D8C8', .35, dentro=cy)
    for dx in (-.7, .7):
        l.trazo(P([(dx - .4, -19.8), (dx, -19.6), (dx + .4, -19.8)]), .14 * s, color='3A2A0A', alfa=.8)   # los ojos bajos
    l.trazo(P([(-.5, -18.2), (0, -18), (.5, -18.2)]), .12 * s, color='3A2A0A', alfa=.75)
    chaleco = [Polygon(P([(-4.6, -10.6), (-4.8, -16.6), (-3.8, -18), (-1.2, -18), (-.5, -16.4), (-.5, -10.6)])),
               Polygon(P([(.5, -10.6), (.5, -16.4), (1.2, -18), (3.8, -18), (4.8, -16.6), (4.6, -10.6)])),
               tubo(P([(-3.2, -18.2), (-1.6, -19.6), (0, -19.9), (1.6, -19.6), (3.2, -18.2)]), [.9 * s] * 5, 6)]
    c = l.masa(chaleco, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    for v in (-15, -12.4):                                               # las correas, con su hebilla
        l.trazo(P([(-4.6, v), (4.6, v)]), .45 * s, color='3A2A0A', alfa=.85)
        l.mancha(Polygon(P([(-.7, v - .5), (.7, v - .5), (.7, v + .5), (-.7, v + .5)])), 'E2EDE9', .95)
    for k in range(3):
        l.trazo(P([(-3.8, -15.4 + k * 2), (-1.8, -15.4 + k * 2)]), .1 * s, color='6B4E10', alfa=.45, dentro=c)
    l.masa(forma(P([(-1.4, -12.6), (0, -15.6), (1.4, -12.6), (0, -11.8)]), 1), material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.25)  # las manos
    l.masa(forma(P([(-2, -23), (-2.4, -25.2), (-1.2, -24.4), (0, -26), (1.2, -24.4), (2.4, -25.2), (2, -23)]), 0), material='claro', alto=.35, brillo=.35,
           vientre=0, hondo=0, linea=.3)                                 # la corona de yeso


def la_virgen(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # la selva de las dos orillas y el puente colgante, largo, sobre el río
    selva(l, -2, 122, 22, 10, semilla=6, emergentes=4)
    l.trazo([(-2, 9.6), (30, 14.6), (60, 16.4), (90, 14.6), (122, 9.6)], .3, color='8EB5AA', alfa=.95)
    l.trazo([(-2, 13.6), (30, 17.8), (60, 19.2), (90, 17.8), (122, 13.6)], .45, color='E2EDE9', alfa=.95)
    for x in np.arange(2, 120, 3):
        yt = np.interp(x, [-2, 30, 60, 90, 122], [9.6, 14.6, 16.4, 14.6, 9.6])
        yb = np.interp(x, [-2, 30, 60, 90, 122], [13.6, 17.8, 19.2, 17.8, 13.6])
        l.trazo([(x, yt), (x, yb)], .1, color='8EB5AA', alfa=.9)
    rio(l, 24)
    orilla(l, forma([(-2, 41.6), (-2, 30), (10, 31), (20, 34.6), (26, 41.6)], 2), tinte=.3)
    orilla(l, forma([(122, 41.6), (122, 30.6), (110, 31.4), (100, 35), (96, 41.6)], 2), tinte=.3)
    # la balsa en el agua y la virgen de yeso, protagonista, con su chaleco salvavidas dorado, que se sube
    g = balsa(l, 66, 36, 1.25)
    reflejo(l, g, 36.4, .2)
    l.mancha(ovalo(58, 37, 6, 1), '0C3A33', .25, difuso=.4)
    l.masa([box(49.4, 34.2, 62.6, 36.6), box(50.6, 33, 61.4, 34.4)], material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)   # el pedestal
    virgen(l, 56, 33.2, 1.04)


def balsa(l, x, y, s=1.0):
    """una balsa de rafting de perfil, gris: el tubo gordo que se levanta en las puntas, con la cuerda de seguridad; (x, y) es la línea
    del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    tubo_ = forma(P([(-15, -5.6), (-12, -2.4), (12, -2.4), (15, -5.6), (17, -4.6), (15.4, .2), (11, 1.4), (-11, 1.4), (-15.4, .2), (-17, -4.6)]), 3)
    t = l.masa(tubo_, material='claro', alto=.6, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.35)
    l.mancha(tubo_.buffer(1), '6E7E7B', .5, dentro=t)
    l.trazo([(x + u * s, y + (-1 + .5 * abs(math.sin(u * .52))) * s) for u in np.linspace(-13, 13, 26)], .16 * s, color='3A2A0A', alfa=.7, dentro=t)
    return tubo_


# ------------------------------------------------------------------------------------------------ Chilamate
def mate(l, x, y, s=1.0, desde=None):
    """un mate dorado colgado de su cordel, que baja de la rama en `desde`: la calabacita panzona, la boca y la bombilla de metal"""
    l.trazo([(x, y - 3.2 * s if desde is None else desde), (x, y - 1.2 * s)], .1, color='3A2A0A', alfa=.8)
    l.trazo([(x + .2 * s, y - 1 * s), (x + 1.2 * s, y - 3 * s)], .16 * s, color='C9D8D2', alfa=.95)        # la bombilla
    g = unary_union([ovalo(x, y + .4 * s, 1.1 * s, 1 * s), ovalo(x, y - .7 * s, .7 * s, .6 * s)])
    m = l.masa(g, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.3, contraluz=.4)
    l.mancha(ovalo(x, y - 1.2 * s, .6 * s, .2 * s), '3A2A0A', .8)
    l.trazo([(x - .6 * s, y - .2 * s), (x + .6 * s, y - .2 * s)], .1 * s, color='6B4E10', alfa=.5, dentro=m)


def higueron(l, x, base, s=1.0):
    """un higuerón gigante: el tronco ancho con sus raíces tablares, las ramas largas y la copa enorme, de verde oscuro, con raíces que
    cuelgan"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry: ovalo(x + u * s, base + v * s, rx * s, ry * s)
    tronco = [forma(P([(-9, 0), (-5, -1.4), (-3.4, -8), (-3, -14), (3, -14), (3.4, -8), (5, -1.4), (9, 0)]), 2),
              tubo(P([(-2, -12), (-8, -17), (-18, -20)]), [1.6 * s, 1.1 * s, .6 * s], 8), tubo(P([(2, -12), (8, -17.4), (19, -20.4)]), [1.6 * s, 1.1 * s, .6 * s], 8),
              tubo(P([(0, -13), (-1, -19), (-3, -23)]), [1.4 * s, 1 * s, .6 * s], 6)]
    t = madera(l, tronco, .45, linea=.4)
    for u in (-6, -3, 3, 6):                                             # las raíces tablares
        l.trazo(P([(u * .4, -6), (u, -.2)]), [.05, .2, .05], color='3A2A0A', alfa=.5, dentro=t)
    copa = [O(0, -26, 20, 5.4), O(-14, -23.6, 11, 4.6), O(14, -23.8, 11, 4.6), O(-7, -29, 10, 4), O(8, -29.4, 10, 4), O(-24, -21.6, 6, 3), O(24, -22, 6, 3)]
    c = l.masa(copa, material='lejos', alto=.45, brillo=.15, vientre=0, hondo=.1, linea=.4, contraluz=.3)
    rng = np.random.default_rng(int(x))
    for _ in range(80):
        u, v = rng.uniform(-28, 28), rng.uniform(-33, -18)
        l.mancha(O(u, v, rng.uniform(.6, 1.3), rng.uniform(.4, .7)), str(rng.choice(['05201C', '4AA189'])), .3, dentro=c)
    for u in (-20, -11, 12, 21):                                         # las raíces que cuelgan
        l.trazo(P([(u, -21), (u + .3, -14)]), .14 * s, color='3A2A0A', alfa=.6)


def chilamate(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 14, 3.4, 10, .45)
    nube(l, 108, 3.4, 10, .45)
    # los piñales y los potreros de atrás, y el río sin rápidos adelante
    prado(l, 18, 30, .3)
    for x in np.arange(0, 122, 2.4):                                     # las hileras de piña
        for y in (19.6, 21.4):
            l.trazo([(x - .6, y), (x, y - 1), (x + .6, y)], .16, color='2F8A74', alfa=.8)
    rio(l, 31)
    orilla(l, forma([(-2, 32), (30, 30.4), (90, 30.4), (122, 32), (122, 26), (-2, 26)], 1), tinte=.3)
    # el higuerón, con los mates dorados, protagonistas, que cuelgan de cada rama
    higueron(l, 60, 30.6, 1.05)
    for u, v, s in ((-24, 14, 1), (-17, 16.4, 1.1), (-9, 15.4, 1.15), (-2, 17, 1.2), (8, 16, 1.2), (16, 16.8, 1.1), (23, 14.6, 1), (-13, 12.4, .9),
                    (12, 12.4, .9)):
        mate(l, 60 + u * 1.05, v + 5.4, s * 1.6, desde=11)


# ------------------------------------------------------------------------------------------------ Puerto Viejo
def mula(l, x, base, s=1.0, lado=1, giro=0.0, material='acento'):
    """una mula cansada, de perfil, mirando a `lado`: la cabeza larga y gacha, las orejas largas y caídas, las alforjas de cuero, la
    cola con su borla y las patas con sus cascos; `giro` la inclina (grados, la cabeza hacia abajo) para que baje un escalón"""
    G = lambda g: affinity.rotate(g, giro * lado, origin=(x, base)) if giro else g
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + lado * u * s, base + v * s, rx * s, ry * s, a * lado)
    patas = [tubo(P([(u, -7), (u + .2, -3.6), (u, -.8)]), [.85 * s, .65 * s, .55 * s], 4) for u in (-6, -4.2, 4.2, 6)]
    cascos = [O(u, -.4, .8, .5) for u in (-6, -4.2, 4.2, 6)]
    cuerpo = [ovalo(x, base - 9 * s, 7.6 * s, 3.8 * s), tubo(P([(5.6, -10), (8.4, -9), (10.2, -6.6)]), [2.2 * s, 1.7 * s, 1.4 * s], 5),
              forma(P([(9.2, -8.4), (11.4, -7.6), (13.4, -3.4), (12.6, -2.2), (11, -2.6), (9, -6.2)]), 2),
              O(6.6, -12.6, .8, 3.6, -30), O(8.4, -12.4, .8, 3.6, 35), tubo(P([(-7.4, -10), (-8.6, -7), (-8.6, -4)]), [.5 * s, .4 * s, .3 * s], 5)]
    m = l.masa([G(g) for g in patas + cuerpo], material=material, alto=.45, brillo=.4, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    l.masa([G(g) for g in cascos + [O(-8.6, -3.6, .7, 1.1)]], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    l.mancha(G(O(12.8, -3, .8, .7)), '6B4E10', .6, dentro=m)            # el hocico
    l.mancha(G(O(10.6, -6.6, .45, .2, -20)), '3A2A0A', .9)              # el ojo, medio cerrado
    alforja = G(forma(P([(-4.4, -12.6), (2.2, -12.6), (2.6, -6.4), (-4.8, -6.4)]), 2))
    a = madera(l, [alforja], .72)
    l.mancha(G(Polygon(P([(-4.6, -10.4), (2.4, -10.4), (2.4, -9.8), (-4.6, -9.8)]))), '3A2A0A', .6, dentro=a)
    for k in range(2):                                                   # las gotas de sudor
        l.mancha(G(O(-2 + k * 3, -15 + k * .4, .4, .6)), 'A4DCC4', .9)


def mono(l, x, y, s=1.0):
    """un mono congo, negro, sentado en una rama: el cuerpo, la cabeza con la barba, la cola enrollada"""
    O = lambda u, v, rx, ry: ovalo(x + u * s, y + v * s, rx * s, ry * s)
    g = [O(0, -2, 1.6, 2.2), O(.4, -4.8, 1.2, 1.1), tubo([(x - 1, y), (x - 2.6, y + 2), (x - 1.8, y + 3.4)], [.3 * s, .25 * s, .2 * s], 6),
         tubo([(x + 1, y - 2.6), (x + 2.6, y - 1.6), (x + 3, y)], [.35 * s, .3 * s, .3 * s], 5)]
    l.masa(g, material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.mancha(O(.9, -4.6, .25, .25), 'C9D8D2', .9)


def puerto_viejo(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # la selva, la confluencia y unas casas en la otra orilla, y el mono en su árbol
    selva(l, -2, 122, 20, 9, semilla=9, emergentes=3)
    for x, w, h in ((86, 6, 3.6), (93, 5.6, 3.2), (100, 6.4, 3.8)):
        c = l.masa(box(x, 21 - h, x + w, 21), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.masa(Polygon([(x - .4, 21 - h), (x + w / 2, 21 - h - 1.8), (x + w + .4, 21 - h)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    l.trazo([(96, 8.4), (106, 9.6)], .5, color='3A2A0A', alfa=.9)
    mono(l, 101, 9, .9)
    rio(l, 21.4)
    # el muelle viejo y torcido, el bote a su lado y las mulas cansadas doradas, protagonistas, que se bajan
    for x, a in ((2, .3), (10, -.4), (18, .5), (26, -.2), (34, .4), (42, -.3)):
        madera(l, [Polygon([(x - .6, 39), (x + a - .6, 27), (x + a + .6, 27), (x + .6, 39)])], .6)
    d = madera(l, [Polygon([(-2, 27.4), (44, 26.4), (44, 28.6), (-2, 29.6)])], .5)
    for x in np.arange(0, 44, 2.6):
        l.trazo([(x, 27.4 - x * .02), (x + .3, 29.5 - x * .02)], .12, color='3A2A0A', alfa=.5, dentro=d)
    l.mancha(ovalo(76, 35.6, 18, 1.4), '0C3A33', .22, difuso=.6)
    bote(l, 76, 34.4, 1.15)
    mula(l, 20, 27, 1.15, 1)
    mula(l, 53, 28.6, 1.25, 1, giro=15)


# ------------------------------------------------------------------------------------------------ Trinidad
def botecito(l, x, y, s=1.0, lado=1):
    """un botecito dorado con ojos, de perfil, mirando a `lado`"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    g = forma(P([(-7, -2.6), (-5, -1.2), (5, -1.2), (7.6, -3.4), (6.4, .6), (3, 1.4), (-4, 1.4), (-6.4, .6)]), 2)
    m = l.masa(g, material='acento', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo(P([(-6.4, -1.6), (0, -.8), (6.6, -2.4)]), [.05, .3, .05], color='6B4E10', alfa=.55, dentro=m)
    l.masa(ovalo(x + lado * 4.4 * s, y - 2 * s, .9 * s, .9 * s), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    l.mancha(ovalo(x + lado * 4.6 * s, y - 2 * s, .4 * s, .45 * s), '05201C', 1)
    l.trazo(P([(3, .2), (4, .5), (5, .1)]), .14 * s, color='3A2A0A', alfa=.85)
    return g


def bandera(l, x, base, alto_, franjas):
    """una bandera en su asta: `franjas`, de arriba abajo, (color, alto relativo)"""
    l.trazo([(x, base), (x, base - alto_)], .3, color='3A2A0A', alfa=.95)
    y, total = base - alto_ + .3, sum(a for _, a in franjas)
    for color, a in franjas:
        h = 4.2 * a / total
        l.mancha(Polygon([(x + .2, y), (x + 6.4, y + .3), (x + 6.4, y + h + .3), (x + .2, y + h)]), color, 1)
        y += h
    l.trazo([(x + .2, base - alto_ + .3), (x + 6.4, base - alto_ + .6), (x + 6.4, base - alto_ + 4.8), (x + .2, base - alto_ + 4.5), (x + .2, base - alto_ + .3)],
            .12, color='3A2A0A', alfa=.6)


def trinidad(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # enfrente, la orilla de Nicaragua, con su selva y su bandera; el San Juan ancho y el Sarapiquí que entra desde acá
    selva(l, -2, 122, 18, 7, semilla=10, emergentes=3)
    bandera(l, 100, 17.6, 9, (('5A8EC8', 1), ('FFFFFF', 1), ('5A8EC8', 1)))
    agua(l, box(-2, 17.6, 122, 41.6), ondas=12, semilla=11, linea=0)
    orilla(l, forma([(-2, 41.6), (-2, 30), (22, 31), (36, 34.4), (40, 41.6)], 2), tinte=.32)
    orilla(l, forma([(122, 41.6), (122, 30), (98, 31), (84, 34.4), (80, 41.6)], 2), tinte=.32)
    agua(l, forma([(40, 41.6), (44, 34), (60, 31.6), (76, 34), (80, 41.6)], 2), ondas=4, semilla=12, linea=0)
    bandera(l, 12, 31, 10, (('1E4A8C', 1), ('FFFFFF', 1), ('B23A2E', 2), ('FFFFFF', 1), ('1E4A8C', 1)))
    for x in (110, 116):
        palmera(l, x, 32, 8, -1, datiles=False)
    # los tres botes dorados, protagonistas, que se dan la mano
    for x0, y0, x1, y1 in ((38, 25, 50, 23.4), (70, 23.4, 82, 25)):
        xm = (x0 + x1) / 2
        l.masa([tubo([(x0, y0), (x0 + 2, y0 - 6), (xm - .6, y0 - 9.6)], [.7, .65, .6], 6), tubo([(x1, y1), (x1 - 2, y1 - 5), (xm + .6, y0 - 9.6)], [.7, .65, .6], 6),
                ovalo(xm, y0 - 10, 1.4, 1.4)], material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35)
    for x, y, lado in ((32, 28.6, 1), (60, 27, 1), (88, 28.6, -1)):
        g = botecito(l, x, y, 1.6, lado)
        reflejo(l, g, y + .5, .2)


# ------------------------------------------------------------------------------------------------ el mar
def congo_grita(l, x, y, s=1.0):
    """Bruno, el mono congo, sentado en su rama de la orilla, con la boca abierta en un grito"""
    O = lambda u, v, rx, ry: ovalo(x + u * s, y + v * s, rx * s, ry * s)
    g = [O(0, -2.4, 2, 2.6), O(.8, -5.6, 1.5, 1.4), tubo([(x - 1.4, y), (x - 3.4, y + 2.4), (x - 2.2, y + 4)], [.4 * s, .3 * s, .25 * s], 6),
         tubo([(x + 1.4, y - 3.2), (x + 3.4, y - 1.8), (x + 3.6, y)], [.45 * s, .4 * s, .35 * s], 5)]
    l.masa(g, material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.mancha(O(1.9, -5.2, .55, .6), '3A2A0A', 1)
    l.mancha(O(1.2, -6.2, .25, .25), 'C9D8D2', .9)
    for k in range(3):                                                   # el grito
        r = 3 + k * 1.6
        l.trazo([(x + (2.4 + r * math.cos(t)) * s, y + (-5.2 + r * math.sin(t)) * s) for t in np.linspace(-.6, .6, 6)], .2 * s, color='0C3A33', alfa=.7)


def mar(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 14, .5)
    nube(l, 96, 3.6, 12, .45)
    # enfrente, la orilla de Nicaragua, con la selva y unas casas, y el San Juan ancho
    selva(l, -2, 122, 17, 7, semilla=13, emergentes=4)
    for x, w, h in ((64, 6, 3.4), (71, 5.6, 3), (77.6, 6.4, 3.6)):
        l.masa(box(x, 17 - h, x + w, 17), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.masa(Polygon([(x - .4, 17 - h), (x + w / 2, 17 - h - 1.8), (x + w + .4, 17 - h)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    agua(l, box(-2, 17, 122, 41.6), ondas=14, semilla=14, linea=0)
    # de este lado, la orilla con su árbol, y Bruno, el mono congo, que los despide con un grito
    orilla(l, forma([(-2, 41.6), (-2, 28), (12, 29.4), (24, 34), (28, 41.6)], 2), tinte=.3)
    madera(l, [tubo([(6, 41), (7, 30), (9, 20), (12, 14)], [1.2, 1, .8, .6], 8), tubo([(9, 21), (16, 18), (24, 18.6)], [.6, .5, .4], 6)], .5)
    l.masa([ovalo(12, 12, 8, 3.4), ovalo(4, 14, 5, 2.6), ovalo(20, 13, 5, 2.4)], material='lejos', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.3)
    congo_grita(l, 19, 18.4, 1)
    # el bote del Sarapiquí, la barca del juego, de casco dorado, protagonista, que entra al San Juan
    g = bote(l, 66, 32, 1.4, material='acento', tinte=None)
    l.masa([box(66 - 8 * 1.4, 32 - 2.6 * 1.4, 66 - 6.8 * 1.4, 32 - 1.4 * 1.4), box(66 + 2 * 1.4, 32 - 2.6 * 1.4, 66 + 3.2 * 1.4, 32 - 1.4 * 1.4)],
           material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)                      # las bancas
    l.trazo([(66 - 10 * 1.4, 32 - 1.8 * 1.4), (66 + 12 * 1.4, 32 - 6 * 1.4)], .3, color='3A2A0A', alfa=.9)   # la pértiga
    reflejo(l, g, 32.4, .22)
    for k in range(4):                                                   # la estela
        l.trazo([(66 - 24 - k * 3, 32.6 + k * .6), (66 - 30 - k * 4, 33.6 + k * .9)], .3, color='FFFFFF', alfa=.6)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='San Miguel', dibujar=san_miguel), dict(clave='La Virgen', dibujar=la_virgen),
            dict(clave='Chilamate', dibujar=chilamate), dict(clave='Puerto Viejo', dibujar=puerto_viejo), dict(clave='Trinidad', dibujar=trinidad),
            dict(clave='mar', dibujar=mar)]
LISTO = True
