# -*- coding: utf-8 -*-
"""Las postales del Congo, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: la meseta de Katanga, alta y llana, con sus pantanos y lagunas, donde nace el Lualaba; al medio, la cruz de cobre de
  Katanga, la moneda antigua de la región del cobre, dorada, enorme, como un monumento;
- Bukama: «una vaca dormida en una cama flotante entre papiros»: la vaca dorada que duerme en su cama, que flota entre los papiros de
  los lagos y pantanos; lejos, el tren que sube al cobre;
- Kindu: «un kínder de barcazas aprende a subirse al tren»: barcazas chiquitas, doradas, con su carita, en fila, y la primera que sube
  por la rampa al vagón del tren;
- Kisangani: «un pescador le tira un beso a la catarata mientras cuelga trampas de madera»: el pescador wagenia, de ropa dorada, en su
  andamio de palos sobre el torrente de las cataratas Boyoma, con las nasas cónicas colgando y un corazón dorado que vuela;
- Mbandaka: «una banda con un pie en cada hemisferio»: una banda de música, de uniforme dorado, parada con un pie a cada lado de la
  línea del ecuador; atrás, el río ancho como un mar, con sus islas;
- Kinshasa: «dos capitales frente a frente y un boxeador con corona que cruza en balsa»: el boxeador, con su corona y sus guantes
  dorados, de pie en la balsa en medio del río, entre Kinshasa y Brazzaville;
- Matadi: «una mata de piedras con un puente colgante encima»: una mata cuya copa son piedras doradas, en la orilla, debajo del puente
  colgante, y el barco de mar que no puede subir más;
- Boma: «un baobab con bigote de capitán»: el baobab dorado, con su gorra de capitán y su bigote, que mira pasar los barcos hacia el
  mar;
- el mar: el Congo entra al Atlántico en Banana: la lengua de arena de Banana es un plátano gigante, dorado, con su faro; los
  manglares y los barcos (el convoy se queda en Boma).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, mangle, nube, orilla, palmera, papiro, pasto, piedra, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '5A3E1E'            # la piel oscura: el pálido de `vientre` teñido de marrón


def piel(l, piezas, tono=.7):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def cara(l, x, y, s=1.0, ojos=True, boca='sonrisa'):
    """los ojos de punto y la boca de una carita"""
    if ojos:
        for dx in (-.8, .8):
            l.mancha(ovalo(x + dx * s, y, .28 * s, .32 * s), '05201C', 1)
    if boca == 'sonrisa':
        l.trazo([(x - .8 * s, y + 1.2 * s), (x, y + 1.6 * s), (x + .8 * s, y + 1.2 * s)], .16 * s, color='0C3A33', alfa=.9)


def tren(l, x0, y, n=4, s=1.0):
    """un tren chico de perfil: la locomotora a la derecha y los vagones"""
    for k in range(n):
        x = x0 + k * 7.4 * s
        l.masa(box(x, y - 3.4 * s, x + 6.8 * s, y - .6 * s), material='lejos' if k else 'oscuro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.22)
        for dx in (1.4, 5.4):
            l.masa(ovalo(x + dx * s, y - .5 * s, .7 * s, .7 * s), material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.18)
    l.masa(box(x0 + (n - 1) * 7.4 * s + 1, y - 5.4 * s, x0 + (n - 1) * 7.4 * s + 2.4 * s, y - 3.2 * s), material='oscuro', alto=.2, brillo=.2,
           vientre=0, hondo=0, linea=.18)


# ------------------------------------------------------------------------------------------------ el nacimiento
def cruz_katanga(x, y, r):
    """la cruz de Katanga: el lingote de cobre en forma de X, de brazos que se ensanchan en la punta, con el nudo al medio"""
    brazos = []
    for a in (45, 135, 225, 315):
        d = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))])
        e = np.array([-d[1], d[0]])
        c = np.array([x, y])
        brazos.append(Polygon([tuple(c + e * r * .16), tuple(c + d * r * .82 + e * r * .2), tuple(c + d * r + e * r * .34), tuple(c + d * r * 1.06),
                               tuple(c + d * r - e * r * .34), tuple(c + d * r * .82 - e * r * .2), tuple(c - e * r * .16)]))
    return unary_union(brazos + [ovalo(x, y, r * .28, r * .28)])


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .5)
    nube(l, 100, 4, 12, .45)
    # la meseta, llana hasta el horizonte, con sus árboles sueltos de sabana, sus pantanos y sus lagunas
    prado(l, 15, 41, .34)
    for x in (6, 22, 40, 82, 98, 114):
        arbol(l, x, 14.6, 1.6, material='lejos', semilla=x)
    for g in (forma([(4, 22), (24, 20.6), (32, 23.4), (18, 25.4)], 2), forma([(86, 21.4), (106, 20.4), (116, 23), (98, 24.6)], 2)):
        agua(l, g, ondas=3, semilla=2, linea=.3)
    agua(l, cinta([(86, 20), (80, 25), (88, 30), (76, 35.4), (82, 41.6)], [1.4, 2.4, 3.4, 4.6, 6], 8), ondas=4, semilla=3, linea=.3)
    for x, y in ((40, 24), (96, 27.6), (36, 33), (100, 36), (24, 40)):
        papiro(l, x, y, 4.6, 7, semilla=int(x))
    pasto(l, 0, 120, 18, 40.6, 26, semilla=4)
    # la cruz de cobre de Katanga, dorada, protagonista, parada como un monumento
    l.masa(box(50, 30.6, 70, 33.6), material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    c = cruz_katanga(60, 18, 12)
    l.mancha(affinity.translate(c, 1.4, 1.2), '0C3A33', .3, difuso=.6)
    m = l.masa(c, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.mancha(c.buffer(1), 'B86B3A', .3, dentro=m)                        # el tono del cobre
    for a in (45, 135, 225, 315):
        d = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        l.trazo([(60 + d[0] * 4, 18 + d[1] * 4), (60 + d[0] * 9, 18 + d[1] * 9)], [.06, .3, .06], color='FBEFCB', alfa=.7, dentro=m)


# ------------------------------------------------------------------------------------------------ Bukama
def vaca(l, x, base, s=1.0):
    """una vaca dorada echada y dormida, de perfil, mirando a la derecha: las patas dobladas, la cabeza apoyada, los ojos cerrados, los
    cuernos y la cola; (x, base) es donde apoya"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = [forma(P([(-8, 0), (-8.6, -4.6), (-5, -7.4), (3, -7.2), (7, -5), (7.6, 0)]), 2), O(9.6, -2.4, 3, 2.2), O(12.2, -1.6, 1.6, 1.3),
              tubo(P([(-7.6, -5), (-9.6, -3), (-10, 0)]), [.5 * s, .4 * s, .3 * s], 5), O(-10, .2, .7, .5),
              tubo(P([(-2, -1), (1.6, -.4), (3.8, 0)]), [1.2 * s, 1 * s, .8 * s], 5)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for u, v, r in ((-4, -4.4, 1.6), (1.6, -5.2, 1.2), (-6.4, -2, 1)):     # las manchas
        l.mancha(O(u, v, r, r * .7), '6B4E10', .45, dentro=c)
    l.masa([tubo(P([(8.4, -4), (7.4, -6), (6, -6.4)]), [.5 * s, .4 * s, .2 * s], 5), tubo(P([(10, -4.4), (11.2, -6.4), (12.6, -6.6)]), [.5 * s, .4 * s, .2 * s], 5)],
           material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)                    # los cuernos
    l.masa(O(8, -3.6, 1.2, .6, -20), material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)   # la oreja
    l.trazo(P([(9.6, -2.8), (10.4, -2.4), (11.2, -2.8)]), .16 * s, color='0C3A33', alfa=.9)   # el ojo cerrado
    l.mancha(O(13, -1.4, .3, .25), '05201C', .9)
    return c


def bukama(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.6, 10, .4)
    # lejos, el terraplén con el tren que sube al cobre; los lagos y pantanos con sus papiros
    prado(l, 15, 19, .28)
    tren(l, 60, 15.6, 5, .8)
    agua(l, box(-2, 18.6, 122, 41.6), ondas=10, semilla=4, linea=0)
    for x, y, h in ((6, 26, 7), (16, 30, 8), (100, 26.4, 7), (112, 31, 8), (30, 38, 7), (90, 39, 7.6), (44, 21.6, 5), (78, 21.6, 5)):
        papiro(l, x, y, h, 9, semilla=int(x))
    # la cama flotante, con la vaca dorada que duerme, protagonista
    l.mancha(ovalo(60, 33.4, 24, 1.6), 'FFFFFF', .5, difuso=.5)
    cama = l.masa([box(38, 28.4, 84, 32.4), box(36.6, 20, 39.4, 33.4), box(82.6, 23.6, 85.4, 33.4)], material='vientre', alto=.3, brillo=.2, vientre=0,
                  hondo=0, linea=.4)
    l.mancha(box(35, 19, 87, 34), '8A6A3A', .55, dentro=cama)
    l.masa(box(39.4, 26, 82.6, 28.6).buffer(.4), material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.35)          # el colchón
    l.masa(ovalo(76.6, 24.8, 4.4, 1.8), material='claro', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.35)                    # la almohada
    vaca(l, 60, 26.4, 1.25)
    m = l.masa(forma([(40, 26.4), (40.4, 22.4), (50, 21.6), (58, 22.6), (60, 26.4)], 1), material='cuerpo', alto=.35, brillo=.25, vientre=0, hondo=0,
               linea=.35)                                                                         # la frazada
    for k in range(4):
        l.trazo([(41 + k * 4.4, 22.4), (42 + k * 4.4, 26.2)], .3, color='FFFFFF', alfa=.5, dentro=m)
    for k, (x, y, s) in enumerate(((78, 18, 1), (82, 14.6, 1.3), (87, 10.6, 1.6))):                # el sueño: zetas
        l.trazo([(x, y), (x + 1.6 * s, y), (x, y + 1.6 * s), (x + 1.6 * s, y + 1.6 * s)], .3 * s, color='0C3A33', alfa=.75)


# ------------------------------------------------------------------------------------------------ Kindu
def barcacita(l, x, y, s=1.0, giro=0.0):
    """una barcaza chiquita, dorada, de casco chato, con su carita y una gorrita de escuela"""
    g = forma([(x - 5 * s, y - 2.6 * s), (x + 5 * s, y - 2.6 * s), (x + 5.6 * s, y - 1.6 * s), (x + 4.6 * s, y + .4 * s), (x - 4.6 * s, y + .4 * s),
               (x - 5.6 * s, y - 1.6 * s)], 1)
    g = affinity.rotate(g, giro, origin=(x, y))
    m = l.masa(g, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    cx, cy = affinity.rotate(Polygon([(x + 2.2 * s, y - 1.4 * s), (x + 2.3 * s, y - 1.4 * s), (x + 2.2 * s, y - 1.3 * s)]), giro, origin=(x, y)).exterior.coords[0]
    for dx in (-.7, .7):
        l.mancha(ovalo(cx + dx * s, cy - .2 * s, .28 * s, .32 * s), '05201C', 1)
    l.trazo([(cx - .6 * s, cy + .5 * s), (cx, cy + .8 * s), (cx + .6 * s, cy + .5 * s)], .14 * s, color='0C3A33', alfa=.9)
    gorra = affinity.rotate(Polygon([(x - 1.6 * s, y - 2.6 * s), (x - 1.2 * s, y - 4.2 * s), (x + 1.2 * s, y - 4.2 * s), (x + 1.6 * s, y - 2.6 * s)]),
                            giro, origin=(x, y))
    l.masa(gorra, material='lejos', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    return g


def kindu(l):
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .5)
    # atrás, la selva; el terraplén del tren y el tren con su vagón chato, en la orilla
    selva(l, -2, 122, 14, 6, semilla=5, emergentes=3)
    prado(l, 13.6, 24, .26)
    l.masa(box(-2, 19.6, 122, 21), material='vientre', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(-2, 122, 2):
        l.trazo([(x, 19.8), (x, 20.8)], .2, color='5A3E1E', alfa=.6)
    tren(l, 62, 19.6, 6, 1.1)
    l.masa(box(40, 16.4, 60, 18.6), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)      # el vagón chato
    for dx in (43, 57):
        l.masa(ovalo(dx, 18.8, .9, .9), material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2)
    # el río y la rampa de tablas que sube al vagón
    rio(l, 24.4)
    rampa = Polygon([(18, 33), (40, 18.6), (44, 18.6), (24, 33.6)])
    r = l.masa(rampa, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(rampa.buffer(1), '8A6A3A', .55, dentro=r)
    for k in range(1, 12):
        f = k / 12
        l.trazo([(18 + 22 * f, 33 - 14.4 * f), (24 + 20 * f, 33.6 - 15 * f)], .12, color='3A2A0A', alfa=.5, dentro=r)
    # el kínder de barcazas, protagonistas: en fila en el agua, y la primera que sube
    barcacita(l, 34, 23.4, 1, -33)
    for k, (x, y) in enumerate(((30, 35.4), (46, 36.6), (62, 35.8), (78, 37), (94, 36))):
        barcacita(l, x, y, 1.15 - k * .03)
    l.masa([forma([(100, 31.4), (112, 31.4), (113, 30), (99.4, 30)], 1), box(102, 27, 107, 30.2), box(103.6, 25, 105, 27.2)], material='lejos', alto=.2,
           brillo=.15, vientre=0, hondo=0, linea=.3)                    # el remolcador, la maestra


# ------------------------------------------------------------------------------------------------ Kisangani
def kisangani(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # la selva de las orillas y las cataratas Boyoma: el escalón de roca y el agua blanca que corre
    selva(l, -2, 122, 16, 7, semilla=7, emergentes=3)
    prado(l, 15.6, 18, .2)
    agua(l, box(-2, 17.6, 122, 41.6), ondas=0, semilla=8, linea=0)
    for y0 in (19, 24, 29.6):                                            # los escalones de los saltos, con su espuma
        l.trazo([(x, y0 + .5 * math.sin(x / 4)) for x in np.arange(-2, 122, 2)], .5, color='0C3A33', alfa=.35)
        for x in np.arange(-1, 122, 1.6):
            l.trazo([(x, y0 + .5 * math.sin(x / 4)), (x + .4, y0 + 2.4)], [.9, .4], color='FFFFFF', alfa=.85)
    for _ in range(26):
        x, y = rng.uniform(0, 120), rng.uniform(20, 40)
        l.trazo([(x, y), (x + 2.4, y - .3), (x + 4.8, y)], .3, color='FFFFFF', alfa=.75)
    # el andamio de palos de los wagenia, sobre el torrente, con las nasas cónicas que cuelgan
    palos = []
    for x in (30, 46, 74, 90):
        palos += [tubo([(x - 3, 38), (x, 12)], [.5, .4], 3), tubo([(x + 3, 38), (x, 12)], [.5, .4], 3)]
    palos += [tubo([(26, 13.4), (94, 13.4)], [.5, .5], 3), tubo([(27, 22), (93, 22)], [.4, .4], 3)]
    p = l.masa(palos, material='vientre', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(palos).buffer(1), '5A3E1E', .7, dentro=p)
    for x in (36, 52, 68, 84):                                           # las nasas: conos de varas que cuelgan hasta el agua
        l.trazo([(x, 13.6), (x, 24)], .12, color='3A2A0A', alfa=.8)
        n = Polygon([(x - 2.4, 24), (x + 2.4, 24), (x + .4, 33), (x - .4, 33)])
        nm = l.masa(n, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(n.buffer(1), '8A6A3A', .6, dentro=nm)
        for k in range(4):
            l.trazo([(x - 2.2 + k * 1.4, 24.2), (x - .3 + k * .2, 32.8)], .1, color='3A2A0A', alfa=.5, dentro=nm)
    # el pescador, protagonista, de ropa dorada, parado en el andamio, que le tira un beso a la catarata
    x, b = 60, 22
    piel(l, [tubo([(x - 1, b - 6), (x - 1.4, b - 3), (x - 1.8, b)], [.8, .7, .6], 5), tubo([(x + 1, b - 6), (x + 1.6, b - 3), (x + 2, b)], [.8, .7, .6], 5),
             ovalo(x, b - 13.4, 1.9, 2.1), tubo([(x - 1.8, b - 10.6), (x - 3.6, b - 8), (x - 5, b - 9)], [.6, .55, .5], 5),
             tubo([(x + 1.8, b - 10.6), (x + 3.4, b - 12.4), (x + 2.4, b - 13.6)], [.6, .55, .5], 5)], .75)
    l.masa([forma([(x - 2.2, b - 11.4), (x + 2.2, b - 11.4), (x + 2.6, b - 5.6), (x - 2.6, b - 5.6)], 1)], material='acento', alto=.45, brillo=.45,
           vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.masa(forma([(x - 2, b - 6), (x + 2.2, b - 6), (x + 2.4, b - 3.6), (x - 2.4, b - 3.6)], 1), material='acento', alto=.4, brillo=.4, vientre=0, hondo=0,
           linea=.35)
    l.mancha(ovalo(x - .6, b - 13.8, .25, .28), '05201C', 1)
    l.mancha(ovalo(x + 1.6, b - 12.8, .45, .35), 'E8A090', .9)                                     # los labios del beso
    corazon = unary_union([ovalo(x + 7.4, b - 15.6, 1.3, 1.3), ovalo(x + 9.6, b - 15.6, 1.3, 1.3),
                           Polygon([(x + 6.2, b - 15.2), (x + 10.8, b - 15.2), (x + 8.5, b - 12)])])
    l.masa(corazon, material='acento', alto=.5, brillo=.55, vientre=0, hondo=0, linea=.35, contraluz=.4)
    for k in range(3):
        l.trazo([(x + 3.6 + k * 1.1, b - 13.6 - k * .5), (x + 4.2 + k * 1.1, b - 14 - k * .5)], .16, color='FFFFFF', alfa=.85)


# ------------------------------------------------------------------------------------------------ Mbandaka
def musico(l, x, base, s=1.0, instrumento='tambor'):
    """un músico de la banda, de frente, con el uniforme y la gorra dorados, las piernas abiertas (un pie a cada lado del ecuador) y su
    instrumento"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-2.4, -3.5, 1.1, .5), O(3.2, -.3, 1.2, .55)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)   # el pie de atrás, más alto
    uni = [tubo(P([(-1.2, -8), (-1.8, -5.6), (-2.2, -3.8)]), [1.2 * s, 1.1 * s, 1 * s], 5), tubo(P([(1.2, -8), (2.2, -4), (3, -.6)]), [1.2 * s, 1.1 * s, 1 * s], 5),
           forma(P([(-2.8, -15.6), (2.8, -15.6), (3.2, -12.4), (2.9, -7.6), (-2.9, -7.6), (-3.2, -12.4)]), 1)]
    u = l.masa(uni, material='acento', alto=.45, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for v in (-14, -12, -10):                                            # los botones y los cordones
        l.mancha(O(0, v, .3, .3), 'FBEFCB', .95, dentro=u)
    piel(l, [O(0, -18.4, 2.2, 2.4), box(x - .7 * s, base - 16.4 * s, x + .7 * s, base - 15.4 * s)], .72)
    l.masa([box(x - 2.2 * s, base - 22.6 * s, x + 2.2 * s, base - 20 * s), O(0, -20, 2.8, .5)], material='acento', alto=.4, brillo=.4, vientre=0, hondo=0,
           linea=.35)                                                    # la gorra alta
    l.mancha(O(0, -21.4, .5, .5), 'FBEFCB', .9)
    for dx in (-.8, .8):
        l.mancha(O(dx, -18.6, .26, .3), '05201C', 1)
    if instrumento == 'tambor':
        piel(l, [tubo(P([(-2.6, -14.6), (-3.6, -11.6), (-2.4, -10.4)]), [.6 * s] * 3, 5), tubo(P([(2.6, -14.6), (3.6, -11.6), (2.4, -10.4)]), [.6 * s] * 3, 5)], .72)
        t = l.masa([box(x - 3.2 * s, base - 10.6 * s, x + 3.2 * s, base - 6.4 * s), O(0, -10.6, 3.2, .8)], material='claro', alto=.4, brillo=.3, vientre=0,
                   hondo=0, linea=.35)
        for k in range(5):
            l.trazo(P([(-3 + k * 1.5, -10.2), (-2.2 + k * 1.5, -6.6)]), .12 * s, color='0C3A33', alfa=.6, dentro=t)
    elif instrumento == 'trompeta':
        piel(l, [tubo(P([(2.6, -14.6), (3.4, -16), (1.4, -17.2)]), [.6 * s] * 3, 5)], .72)
        l.masa([tubo(P([(.6, -17.4), (5, -18.6), (8.6, -19.6)]), [.4 * s, .4 * s, .5 * s], 3), forma(P([(8, -18.4), (10.4, -21), (10.8, -17.6)]), 1)],
               material='claro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)
    else:                                                                # la tuba
        t = l.masa([tubo(P([(-1, -9), (-3.6, -12), (-3.4, -16), (-1.4, -19.6), (1.6, -22)]), [1.2 * s, 1.4 * s, 1.6 * s, 1.8 * s, 2.2 * s], 8),
                    forma(P([(-.4, -23.4), (3.6, -23.4), (4.4, -20.6), (.2, -20.4)]), 1)], material='claro', alto=.45, brillo=.4, vientre=0, hondo=0,
                   linea=.35)


def mbandaka(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .5)
    nube(l, 100, 3.6, 12, .45)
    # el río, ancho como un mar, con sus islas de selva
    agua(l, box(-2, 14, 122, 26), ondas=10, semilla=10, linea=0)
    for x0, x1, y in ((8, 30, 18), (44, 64, 16.4), (84, 108, 19)):
        selva(l, x0, x1, y, 3.4, semilla=int(x0), emergentes=1)
    # la orilla de acá, y la línea del ecuador que la cruza
    orilla(l, forma([(-2, 41.5), (-2, 25.6), (30, 24.6), (60, 24.4), (90, 24.6), (122, 25.6), (122, 41.5)], 2), tinte=.3)
    ecuador = cinta([(-2, 34.6), (40, 34.2), (80, 34.2), (124, 34.6)], [.8] * 4, 4)
    l.mancha(ecuador, 'FFFFFF', .95)
    # la banda, protagonista: tres músicos que dan el paso con un pie a cada lado del ecuador
    musico(l, 40, 36.6, 1, 'trompeta')
    musico(l, 60, 37, 1.08, 'tambor')
    musico(l, 80, 36.6, 1, 'tuba')
    for x, y in ((28, 14), (92, 12)):                                    # las notas
        l.masa([ovalo(x, y, .9, .7, -20), box(x + .7, y - 4, x + 1, y)], material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.2)


# ------------------------------------------------------------------------------------------------ Kinshasa
def boxeador(l, x, base, s=1.0):
    """un boxeador de pie, de frente, con los guantes dorados levantados, el calzón dorado y una corona dorada"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-2.4, -.3, 1.3, .55), O(2.4, -.3, 1.3, .55)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    piel(l, [tubo(P([(-1.4, -7), (-1.8, -3.6), (-2.2, -.6)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(1.4, -7), (1.8, -3.6), (2.2, -.6)]), [1.1 * s, 1 * s, .9 * s], 5),
             forma(P([(-3.2, -16), (3.2, -16), (2.8, -10), (2.2, -8.4), (-2.2, -8.4), (-2.8, -10)]), 1),
             tubo(P([(-3, -15.4), (-5.4, -12.6), (-4, -16.6)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(3, -15.4), (5.4, -12.6), (4, -16.6)]), [1.1 * s, 1 * s, .9 * s], 5),
             O(0, -18.6, 2.2, 2.4), box(x - .8 * s, base - 16.8 * s, x + .8 * s, base - 15.6 * s)], .72)
    l.masa([forma(P([(-2.6, -8.8), (2.6, -8.8), (3, -5.4), (.4, -5.4), (0, -6.4), (-.4, -5.4), (-3, -5.4)]), 1),
            O(-4.2, -17.2, 1.7, 1.9), O(4.2, -17.2, 1.7, 1.9),
            forma(P([(-2.2, -20.4), (-2.6, -23.4), (-1.2, -22), (0, -24), (1.2, -22), (2.6, -23.4), (2.2, -20.4)]), 1)],
           material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for dx in (-.8, .8):
        l.mancha(O(dx, -18.8, .26, .3), '05201C', 1)
    l.trazo(P([(-.8, -17.4), (0, -17.1), (.8, -17.4)]), .16 * s, color='0C3A33', alfa=.9)


def kinshasa(l):
    rng = np.random.default_rng(11)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    nube(l, 92, 3.4, 10, .4)
    # las dos capitales, frente a frente: Kinshasa a la izquierda, con sus edificios, y Brazzaville a la derecha, con su torre
    prado(l, 18, 22, .26)
    for x0, x1, top in ((-2, 46, 7), (74, 122, 10)):
        for x in np.arange(x0, x1, 3.6):
            h = rng.uniform(4, 22 - top)
            e = l.masa(box(x, 20.6 - h, x + 3.2, 20.8), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.22, arroja=False)
            for y in np.arange(20.6 - h + .8, 20.4, 1.2):
                l.trazo([(x + .4, y), (x + 2.8, y)], .08, color='8EB5AA', alfa=.8, dentro=e)
    t = l.masa([box(98, 2.6, 102.6, 20.8), ovalo(100.3, 2.8, 2.3, 1.2)], material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)   # la torre
    for y in np.arange(3.6, 20, 1):
        l.trazo([(98.4, y), (102.2, y)], .08, color='8EB5AA', alfa=.8, dentro=t)
    # el río entre las dos, ancho, y la balsa con el boxeador, protagonista
    rio(l, 21.4)
    for k in range(3):
        l.trazo([(60 + (9 + k * 2.6) * math.cos(a), 36.8 + (1.2 + k * .5) * math.sin(a)) for a in np.linspace(0, math.pi, 20)], .16, color='D2F2DA',
                alfa=.75 - k * .15)
    balsa = [tubo([(46, 35.6 + k * .7), (74, 35.6 + k * .7)], [.7, .7], 3) for k in range(3)]
    b = l.masa(balsa, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(balsa).buffer(1), '8A6A3A', .6, dentro=b)
    boxeador(l, 60, 35.2, 1.2)


# ------------------------------------------------------------------------------------------------ Matadi
def matadi(l):
    rng = np.random.default_rng(13)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # los cerros de piedra, el puente colgante blanco encima, de torre a torre, y el río angosto y hondo
    for pts in ([(-2, 30), (-2, 12), (10, 10.6), (22, 14), (30, 22), (34, 30)], [(86, 30), (90, 20), (100, 13), (112, 10.4), (122, 12), (122, 30)]):
        g = Polygon(pts).buffer(0)
        m = l.masa(g, material='lejos', alto=.3, brillo=.08, vientre=0, hondo=0, linea=.35)
        l.mancha(g, '8FA19D', .35, dentro=m)
    agua(l, box(-2, 26, 122, 41.6), ondas=10, semilla=13, linea=0)
    for x in (24, 96):
        l.masa(box(x - 1.2, 3, x + 1.2, 18.6), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.masa(box(-2, 17.4, 122, 18.6), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    for tramo, (a, b) in ((0, (-2, 24)), (1, (24, 96)), (2, (96, 122))):     # los cables, de torre a torre
        if tramo == 1:
            pts = [(x, 3.4 + 12.6 * (1 - ((x - 60) / 36) ** 2) * 0 + 3.4 + 10.2 * ((x - 60) / 36) ** 2 * 0) for x in np.linspace(a, b, 2)]
            pts = [(x, 3.4 + (14 - 10.6 * ((x - 60) / 36) ** 2)) for x in np.linspace(a, b, 30)]
        else:
            x0 = 24 if tramo == 0 else 96
            pts = [(x, 3.4 + abs(x - x0) / 26 * 12) for x in np.linspace(a, b, 10)]
        l.trazo(pts, .3, color='DAE5E1', alfa=.95)
        for x, y in pts[1:-1:2]:
            l.trazo([(x, y), (x, 17.6)], .08, color='8EB5AA', alfa=.9)
    # el barco de mar que no puede subir más, y la mata de piedras doradas, protagonista, en la orilla de adelante
    l.masa([forma([(64, 31.6), (98, 31.6), (101, 29), (63, 29.2)], 1), box(66, 25.4, 74, 29.3), box(68.6, 23, 70.6, 25.6)], material='lejos', alto=.2,
           brillo=.15, vientre=0, hondo=0, linea=.3)
    orilla(l, forma([(-2, 41.6), (-2, 33), (24, 32), (50, 33.6), (66, 36.4), (60, 41.6)], 2), tinte=.2)
    l.masa(tubo([(48, 39.6), (48.6, 33), (48, 29)], [1.8, 1.4, 1.2], 4), material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(box(45, 28, 51, 40.4), '5A3E1E', .6)
    for k in range(5):                                                   # las ramas, que sostienen las piedras
        a = math.radians(-150 + k * 30)
        l.trazo([(48.3, 29.6), (48.3 + 6 * math.cos(a), 29.6 + 4.4 * math.sin(a))], .4, color='5A3E1E', alfa=.85)
    puestos = []
    for _ in range(80):                                                  # las piedras, una por una, que arman la copa redonda
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 1) ** .6
        cx, cy = 48.3 + 11 * r * math.cos(a), 21 + 7.4 * r * math.sin(a)
        rx, ry = rng.uniform(1.7, 2.6), rng.uniform(1.3, 1.9)
        if all(math.hypot((cx - px) / (rx + prx), (cy - py) / (ry + pry)) > .8 for px, py, prx, pry in puestos):
            puestos.append((cx, cy, rx, ry))
    for cx, cy, rx, ry in sorted(puestos, key=lambda p: p[1]):
        g = ovalo(cx, cy, rx, ry, rng.uniform(-30, 30))
        l.masa(g, material='acento', alto=.6, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.4)
        l.trazo([(cx - rx * .4, cy - ry * .3), (cx + rx * .2, cy - ry * .55)], .12, color='FBEFCB', alfa=.7)


# ------------------------------------------------------------------------------------------------ Boma
def boma(l):
    rng = np.random.default_rng(15)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # el estuario, ancho, con los barcos que bajan hacia el mar, y la orilla del puerto viejo
    prado(l, 15, 18, .26)
    rio(l, 17.6)
    for x, y, s in ((84, 24, .9), (104, 21.4, .7)):
        l.masa([forma([(x - 8 * s, y), (x + 8 * s, y), (x + 9 * s, y - 1.6 * s), (x - 8.4 * s, y - 1.6 * s)], 1), box(x - 5 * s, y - 4 * s, x, y - 1.5 * s),
                box(x - 3 * s, y - 6 * s, x - 1.8 * s, y - 3.9 * s)], material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        l.trazo([(x + 8 * s, y - .6 * s), (x + 12 * s, y - .2 * s)], .16, color='FFFFFF', alfa=.7)
    m = orilla(l, forma([(-2, 41.5), (-2, 28), (30, 26.6), (60, 27), (80, 30), (92, 41.5)], 2), tinte=.3)
    pasto(l, 0, 90, 29, 40.6, 16, semilla=16, dentro=m)
    casitas(l, 2, 22, 28.4, 3.4, semilla=17)
    # el baobab dorado, protagonista, con su gorra de capitán y su bigote, que mira pasar los barcos
    tronco = forma([(38, 38), (36.4, 30), (37, 22), (39.6, 14.6), (42, 12), (54, 12), (56.4, 14.6), (59, 22), (59.6, 30), (58, 38)], 2)
    ramas = [tubo([(41, 13), (37, 8), (32, 6.6)], [1.6, 1, .5], 5), tubo([(44, 12.4), (42, 6), (39, 3.4)], [1.6, 1, .5], 5),
             tubo([(52, 12.4), (54, 6), (57, 3.6)], [1.6, 1, .5], 5), tubo([(55, 13), (60, 8.6), (64, 7.4)], [1.6, 1, .5], 5)]
    for p in ((31.6, 6.4), (38.6, 3), (57.6, 3.2), (64.4, 7)):            # las hojas, ralas
        l.masa([ovalo(p[0] + dx, p[1] + dy, 2.2, 1.3) for dx, dy in ((0, 0), (-1.6, .8), (1.6, .6))], material='cuerpo', alto=.3, brillo=.2, vientre=0,
               hondo=0, linea=.25)
    t = l.masa([tronco] + ramas, material='acento', alto=.5, brillo=.4, vientre=0, hondo=.1, linea=.45, contraluz=.35)
    for x in np.arange(39, 58, 2.6):                                     # la corteza
        l.trazo([(x, 37), (x + rng.uniform(-.6, .6), 26), (x + rng.uniform(-.6, .6), 16)], [.1, .2, .1], color='6B4E10', alfa=.45, dentro=t)
    for dx in (-2.6, 2.6):                                               # la cara: los ojos, el bigote de capitán y la boca
        l.mancha(ovalo(48 + dx, 20.6, .9, 1), 'FFFFFF', .95, dentro=t)
        l.mancha(ovalo(48 + dx + .3, 20.8, .45, .5), '05201C', 1, dentro=t)
    bigote = unary_union([tubo([(48, 24.4), (45, 23.6), (42.6, 24.6), (41.4, 23)], [.9, .8, .6, .3], 6), tubo([(48, 24.4), (51, 23.6), (53.4, 24.6), (54.6, 23)],
                                                                                                          [.9, .8, .6, .3], 6)])
    l.masa(bigote, material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)
    l.trazo([(46.6, 26.6), (48, 27.2), (49.4, 26.6)], .2, color='3A2A0A', alfa=.8)
    gorra = [forma([(40.6, 13.6), (41, 9.4), (48, 8.2), (55, 9.4), (55.4, 13.6)], 1), forma([(40, 13.4), (56, 13.4), (57.4, 15), (38.6, 15)], 1)]
    g = l.masa(gorra[0], material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.4)
    l.masa(gorra[1], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.35)
    l.mancha(box(40, 11.6, 56, 13), '0C3A33', .85, dentro=g)
    l.mancha(ovalo(48, 10.6, 1.2, 1), 'E8B952', 1, dentro=g)            # el escudo de la gorra


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    rng = np.random.default_rng(17)
    cielo(l, sol=None)
    nube(l, 30, 5, 16, .5)
    nube(l, 96, 4, 12, .45)
    # el Atlántico, al fondo, y el río que llega por la derecha; un barco lejos
    horizonte = 17
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    l.mancha(Polygon([(60, 41.6), (80, 26), (122, 22), (122, 41.6)]), '8A6A3A', .3, dentro=m, difuso=3)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa([forma([(14, horizonte - .4), (34, horizonte - .4), (35.6, horizonte - 2), (13.4, horizonte - 2)], 1), box(16, horizonte - 4.4, 21, horizonte - 1.9)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # los manglares de la otra orilla del estuario, a la derecha
    for x in np.arange(98, 122, 5):
        mangle(l, x + rng.uniform(-1, 1), 24 + rng.uniform(-1, 1), rng.uniform(7, 9), semilla=int(x * 3))
    # la lengua de arena de Banana, protagonista: un plátano gigante, dorado, con su faro y sus casitas
    pts = [(16, 30), (30, 34.6), (50, 36.6), (70, 35.6), (86, 31.6), (96, 26.6)]
    banana = cinta(pts, [2, 6, 8.4, 8.4, 6.4, 2.6], 10)
    l.mancha(affinity.translate(banana, .8, 1.4), '0C3A33', .3, difuso=.6)
    b = l.masa(banana, material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.trazo([(22, 31.6), (44, 34.6), (66, 34.4), (86, 30)], [.05, .3, .3, .05], color='FBEFCB', alfa=.75, dentro=b)
    for x, y in ((38, 36.4), (56, 38), (74, 36.6)):                       # las pecas del plátano
        l.mancha(ovalo(x, y, .7, .45), '6B4E10', .6, dentro=b)
    l.masa(forma([(95, 27.4), (96.4, 25.6), (99.4, 24), (100, 25), (97.6, 27.4)], 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)  # el cabo
    fr = l.masa([forma([(57.6, 32.6), (58, 23.6), (60.2, 23.6), (60.6, 32.6)], 0), box(57.2, 22.4, 61, 23.8)], material='claro', alto=.3, brillo=.2,
                vientre=0, hondo=0, linea=.3)
    l.mancha(box(56, 26.6, 62, 28), '2F8A74', .85, dentro=fr)
    l.masa(Polygon([(57.4, 22.6), (59.1, 20.6), (60.8, 22.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    for x in (44, 50, 68, 74):
        l.masa([box(x - 1.2, 30.6, x + 1.2, 32.6), Polygon([(x - 1.5, 30.8), (x, 29.6), (x + 1.5, 30.8)])], material='claro', alto=.2, brillo=.1, vientre=0,
               hondo=0, linea=.2)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Bukama', dibujar=bukama), dict(clave='Kindu', dibujar=kindu),
            dict(clave='Kisangani', dibujar=kisangani), dict(clave='Mbandaka', dibujar=mbandaka), dict(clave='Kinshasa', dibujar=kinshasa),
            dict(clave='Matadi', dibujar=matadi), dict(clave='Boma', dibujar=boma), dict(clave='mar', dibujar=mar)]
LISTO = True
