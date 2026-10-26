# -*- coding: utf-8 -*-
"""Las postales del Mekong, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el de Luang Prabang, que sale pálido.

- el nacimiento: la meseta tibetana, alta y plana, con sus montes nevados; un chorten blanco de punta dorada con las banderas de
  oración, y el río que nace al lado (en China se llama Lancang);
- Jinghong: «elefantes y té pu'er en la orilla»: un elefante dorado que levanta con la trompa una torta redonda de té pu'er, envuelta
  en papel; atrás, las terrazas de té, las palmeras y la represa con que China lo ataja;
- Luang Prabang: «una fila de monjes naranja al amanecer»: los monjes, con sus túnicas doradas y sus cuencos, caminan en fila y en
  orden, y la gente arrodillada les da arroz; atrás, los techos del templo y el monte Phousi;
- Vientián: «viento manso sobre el río»: la estupa dorada del Pha That Luang, el símbolo de Laos, y el viento suave que ondula sobre el
  río tranquilo y lleva una cometa; enfrente, Tailandia;
- Phnom Penh: «un pulmón que inhala en monzón y exhala en seca»: visto desde arriba, el lago Tonlé Sap con forma de pulmón, de borde
  dorado, y el río que lo une al Mekong, con una flecha dorada de ida y vuelta: en lluvias el agua va al lago y en seca vuelve;
- Can Tho: «un mercado flotante con sombreros cónicos»: las barcas apretadas, con ojos pintados en la proa y cargadas de frutas, los
  sombreros cónicos dorados y las varas altas donde cuelgan lo que venden;
- el mar: los nueve dragones (Cửu Long): de cada brazo del delta, entre los arrozales, sale al mar un dragón dorado; la cola larga se
  queda en el delta.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, agua, arbol, ave, casitas, cebolla_baja, cielo, cinta, cordillera, mangle, nube, orilla, palmera,  # noqa: F401
                     pasto, piedra, prado, reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
PAPEL = 'D8C49A'           # el papel de la torta de té


# ------------------------------------------------------------------------------------------------ el nacimiento
def chorten(l, x, base, s=1.0):
    """un chorten tibetano: las gradas, el cuerpo redondo blanco, el pináculo de anillos y la punta dorada con su sol y su luna"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    blanco = [box(x - 7 * s, base - 2.2 * s, x + 7 * s, base), box(x - 5.6 * s, base - 4.2 * s, x + 5.6 * s, base - 2), box(x - 4.4 * s, base - 6 * s, x + 4.4 * s, base - 4),
              forma(P([(-4.4, -6), (-5, -8.6), (-4.2, -11.6), (-2, -13.2), (2, -13.2), (4.2, -11.6), (5, -8.6), (4.4, -6)]), 2),
              box(x - 2.4 * s, base - 14.6 * s, x + 2.4 * s, base - 13)]
    b = l.masa(blanco, material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
    l.mancha(forma(P([(-1.4, -8), (-1.4, -10.4), (0, -11.4), (1.4, -10.4), (1.4, -8)]), 1), '164F46', .7, dentro=b)   # el nicho
    oro = [Polygon(P([(-1.8, -14.6), (-.5, -24), (.5, -24), (1.8, -14.6)])), ovalo(x, base - 25 * s, 1.4 * s, .7 * s),
           forma(P([(-1.6, -26.4), (0, -25.6), (1.6, -26.4), (1, -25.2), (-1, -25.2)]), 1), ovalo(x, base - 27.4 * s, .7 * s, .7 * s)]
    m = l.masa(oro, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.4)
    for k in range(9):                                                   # los trece anillos (nueve se ven)
        y = base - (15.4 + k * .95) * s
        w = (1.7 - k * .13) * s
        l.trazo([(x - w, y), (x + w, y)], .14 * s, color='6B4E10', alfa=.7, dentro=m)
    return b


def banderas(l, a, b, caida=2.0, n=14, semilla=0):
    """una cuerda de banderas de oración entre los puntos `a` y `b`, que cae en curva; las banderas cuadradas, de colores claros"""
    colores = ('FFFFFF', '9BDDBD', '2F8A74', 'FBEFCB', '164F46')
    pts = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + caida * 4 * t * (1 - t)) for t in np.linspace(0, 1, 30)]
    l.trazo(pts, .1, color='0C3A33', alfa=.8)
    for k in range(n):
        t = (k + .5) / n
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + caida * 4 * t * (1 - t)
        l.mancha(Polygon([(x - .7, y), (x + .7, y), (x + .8, y + 1.7), (x - .6, y + 1.8)]), colores[(k + semilla) % 5], .95)


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 24, 5, 14, .5)
    nube(l, 98, 4, 12, .45)
    # los montes nevados, lejos, al borde de la meseta
    cordillera(l, [(-2, 16), (8, 10), (16, 12.4), (26, 7), (36, 11.4), (44, 9.6), (54, 15)], nieve=12)
    cordillera(l, [(66, 15), (76, 9.4), (84, 11.6), (94, 6.6), (104, 10.4), (114, 8.6), (122, 12)], nieve=11.6)
    # la meseta: alta, plana y amarilla de pasto ralo, y el río que nace en ella y baja serpenteando hacia nosotros
    prado(l, 15.4, 41, .42)
    agua(l, cinta([(80, 17), (74, 20), (82, 24), (72, 29), (82, 34), (70, 41.6)], [1, 1.8, 2.6, 3.6, 5, 7], 8), ondas=4, semilla=2, linea=.3)
    for _ in range(20):                                                  # las matas de pasto ralo
        x, y = rng.uniform(0, 120), rng.uniform(18, 40)
        l.trazo([(x - .6, y), (x, y - .9), (x + .6, y)], .12, color='2F8A74', alfa=.6)
    # el chorten, protagonista, y las cuerdas de banderas que bajan de su punta a los postes
    for x, y in ((22, 31), (104, 30.4)):
        l.masa(box(x - .35, y - 11, x + .35, y), material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2)
    chorten(l, 58, 34, 1.08)
    banderas(l, (58, 5.4), (22, 20.2), 1.8, 16, 0)
    banderas(l, (58, 5.4), (104, 19.6), 2.2, 20, 2)


# ------------------------------------------------------------------------------------------------ Jinghong
def elefante(l, x, base, s=1.0):
    """un elefante asiático dorado, de perfil, mirando a la derecha: el lomo alto, la cabeza en cúpula, la oreja chica, los colmillos
    cortos y la trompa levantada que sostiene la torta de té; (x, base) es el suelo bajo el medio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    lejos = [tubo(P([(-6, -6), (-6.4, -3), (-6.2, 0)]), [2.6 * s, 2.4 * s, 2.4 * s], 4), tubo(P([(5, -6), (5.4, -3), (5.2, 0)]), [2.6 * s, 2.4 * s, 2.4 * s], 4)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(unary_union(lejos).buffer(.3), '6B4E10', .4)
    cuerpo = [forma(P([(-10, -6), (-10.4, -10), (-8, -14.6), (-3, -16.4), (3, -16), (7.6, -13.6), (9, -9), (8.4, -5.4), (-8, -5)]), 2),
              tubo(P([(-8.4, -7), (-8.6, -3), (-8.4, 0)]), [2.8 * s, 2.6 * s, 2.6 * s], 4), tubo(P([(3, -7), (3.2, -3), (3, 0)]), [2.8 * s, 2.6 * s, 2.6 * s], 4),
              O(10.6, -12.4, 4.6, 4.6), O(9.6, -15.6, 3, 2.4),
              tubo(P([(13.6, -10.6), (15.6, -8.4), (17, -11), (17.4, -16), (16.4, -20.4)]), [2.4 * s, 1.9 * s, 1.5 * s, 1.2 * s, 1 * s], 10),
              tubo(P([(-9.8, -11.4), (-11.6, -8.6), (-11.8, -5.6)]), [.5 * s, .4 * s, .3 * s], 6)]
    c = l.masa(cuerpo, material='acento', alto=.55, brillo=.4, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for v in np.arange(-11, -18.4, -1.4):                                # las arrugas de la trompa
        l.trazo(P([(16.4, v), (17.8, v + .2)]), .1 * s, color='6B4E10', alfa=.6, dentro=c)
    l.masa(O(8, -12, 2.6, 3.4, -10), material='acento', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.35)      # la oreja
    l.mancha(O(11.6, -13.6, .55, .45), '05201C', 1)                      # el ojo
    l.masa(tubo(P([(13, -8.6), (14.6, -7.4), (15.8, -7.8)]), [.7 * s, .5 * s, .2 * s], 5), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.25)                                                    # el colmillo
    # la torta de té pu'er, redonda y chata, envuelta en papel con su sello, en la punta de la trompa
    t = l.masa(O(16.6, -23, 3.6, 2.6), material='claro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.35)
    l.mancha(O(16.6, -23, 4, 3), PAPEL, .6, dentro=t)
    l.mancha(O(16.6, -23, 1.6, 1.1), '5A3E1E', .5, dentro=t)
    l.trazo(P([(13.4, -23.4), (19.8, -23.4)]), .1 * s, color='5A3E1E', alfa=.6, dentro=t)
    return c


def jinghong(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .5)
    nube(l, 96, 3.6, 12, .45)
    # atrás, los cerros con las terrazas de té y, en el río, la represa
    cordillera(l, [(-2, 20), (10, 10), (24, 7.6), (38, 11), (50, 16), (60, 19)], material='cuerpo')
    cordillera(l, [(56, 19), (70, 12), (86, 9), (100, 11.6), (112, 8.4), (122, 13)], material='cuerpo')
    for y in np.arange(11, 20, 1.4):                                     # las hileras de té
        l.trazo([(x, y + .4 * math.sin(x / 3)) for x in np.arange(2, 50, 2)], .3, color='164F46', alfa=.45)
        l.trazo([(x, y + .4 * math.sin(x / 3)) for x in np.arange(66, 120, 2)], .3, color='164F46', alfa=.45)
    prado(l, 19, 41, .24)
    a = rio(l, 21)
    pr = piedra(l, [box(40, 17.6, 80, 22), box(48, 15.6, 72, 18)], .1, .35)                     # la represa
    for x in np.arange(50, 71, 3.4):
        l.mancha(box(x, 18.6, x + 1.6, 22), '0C3A33', .6, dentro=pr)
        l.trazo([(x + .8, 22), (x + .8, 24.6)], .8, color='FFFFFF', alfa=.7)
    # la orilla de adelante, con palmeras y una pagoda dai, y el elefante, protagonista
    m = orilla(l, forma([(-2, 41.5), (-2, 28.6), (30, 27.6), (60, 27.4), (90, 27.6), (122, 28.6), (122, 41.5)], 2), tinte=.24)
    pasto(l, 0, 120, 29, 40.6, 18, semilla=4, dentro=m)
    for x, h, lado in ((8, 13, 1), (16, 10, -1), (104, 12, -1), (113, 14, 1)):
        palmera(l, x, 36.4, h, lado, datiles=False)
    pg = l.masa([box(84, 26.4, 96, 32.6), Polygon([(82.6, 26.6), (90, 21.4), (97.4, 26.6)]), Polygon([(85.4, 21.6), (90, 16.4), (94.6, 21.6)])],
                material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(forma([(88.8, 32.6), (88.8, 29.6), (90, 28.6), (91.2, 29.6), (91.2, 32.6)], 1), '164F46', .8, dentro=pg)
    l.mancha(ovalo(56, 38.2, 13, 1.3), '0C3A33', .22, difuso=.6)
    elefante(l, 52, 38.2, 1.12)


# ------------------------------------------------------------------------------------------------ Luang Prabang
def monje(l, x, base, s=1.0):
    """un monje que camina hacia la derecha, de perfil: la cabeza rapada, la túnica dorada que le cruza un hombro y llega a los
    tobillos, y el cuenco de las limosnas en las manos, con su tapa"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    piel(l, [O(.6, -17.6, 1.7, 1.9), box(x - .3 * s, base - 16 * s, x + 1.3 * s, base - 14.6 * s), O(-.6, -.4, 1.1, .5), O(1.8, -.4, 1.1, .5),
             tubo(P([(.4, -13), (2.4, -10.4), (3.6, -9.4)]), [.7 * s, .6 * s, .5 * s], 5)], .45)
    t = l.masa(forma(P([(-2.2, -14.8), (2.4, -15), (3, -12), (2.8, -6), (3.4, -1.2), (-2.6, -1.2), (-2.4, -6), (-2.8, -12)]), 1), material='acento',
               alto=.45, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for u0, u1 in ((-1.6, -1.8), (.2, .6), (1.8, 2.4)):                  # los pliegues
        l.trazo(P([(u0, -12), (u1, -1.6)]), [.06, .18, .06], color='6B4E10', alfa=.5, dentro=t)
    l.trazo(P([(-2.2, -14.6), (2.6, -9.6)]), .2 * s, color='6B4E10', alfa=.55, dentro=t)     # el borde que cruza el pecho
    l.masa([O(3.8, -9, 1.9, 1.5), O(3.8, -10.4, 1.4, .5)], material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)   # el cuenco
    l.mancha(O(1.4, -18.2, .26, .26), '05201C', 1)
    return t


def piel(l, piezas, tono=.45):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def arrodillada(l, x, base, s=1.0):
    """una persona arrodillada que da arroz, mirando a la izquierda: la canasta de arroz glutinoso a su lado"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([forma(P([(-2.4, 0), (-2.6, -4), (-1.8, -8.4), (1.6, -8.4), (2.6, -4), (4.4, -1), (4.4, 0)]), 1)], material='claro', alto=.3, brillo=.2,
           vientre=0, hondo=0, linea=.35)
    piel(l, [O(0, -10.2, 1.6, 1.8), tubo(P([(-1, -7.4), (-3, -5.4), (-4.2, -5.8)]), [.6 * s, .5 * s, .45 * s], 5)], .5)
    l.masa(forma(P([(-1.6, -10.4), (-1.4, -12), (1, -12.2), (1.8, -11), (1.6, -9.6)]), 1), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.25)
    c = l.masa([O(6.6, -1.6, 2, 1.6), box(x + 4.8 * s, base - 1.6 * s, x + 8.4 * s, base)], material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0,
               linea=.3)
    l.mancha(O(6.6, -1.6, 2.4, 2.4), '8A6A3A', .5, dentro=c)
    for k in range(4):
        l.trazo(P([(4.8, -.4 - k * .6), (8.4, -.4 - k * .6)]), .08 * s, color='5A3E1E', alfa=.5, dentro=c)


def luang_prabang(l):
    cielo(l, sol=None, tarde=.3)
    l.mancha(ovalo(22, 12, 7, 5), 'FBEFCB', .5, difuso=2)                # el sol que sale, pálido, detrás del monte
    l.mancha(ovalo(22, 12.6, 2.8, 2.8), 'F2D48A', .55)
    # el monte Phousi con su estupa, el río y los techos bajos del templo, de aleros que casi tocan el suelo
    l.masa(forma([(2, 22), (12, 12.4), (24, 9.4), (36, 12), (48, 20), (50, 22)], 2), material='cuerpo', alto=.3, brillo=.1, vientre=0, hondo=0,
           linea=.35)
    l.masa([box(22.6, 6.4, 25.4, 9.6), Polygon([(22.4, 6.6), (24, 3.4), (25.6, 6.6)])], material='claro', alto=.2, brillo=.15, vientre=0, hondo=0,
           linea=.25)
    rio(l, 21)
    prado(l, 21.6, 41, .2)
    for x0, w in ((60, 34), (96, 22)):
        for k, (dy, dw) in enumerate(((0, 0), (-3.4, -6), (-6.4, -13))):  # los tres aleros superpuestos
            l.masa(Polygon([(x0 - 2 + dw / -2 + (-dw / 2 if False else 0), 26 + dy), (x0 + 4 - dw * .1, 21 + dy), (x0 + w - 4 + dw * .1, 21 + dy),
                            (x0 + w + 2 + dw / 2, 26 + dy)]), material='oscuro' if k % 2 == 0 else 'lejos', alto=.25, brillo=.15, vientre=0, hondo=0,
                   linea=.3)
        tm = l.masa(box(x0 + 2, 26, x0 + w - 2, 30.4), material='claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.3)
        for x in np.arange(x0 + 4, x0 + w - 3, 3.2):
            l.mancha(box(x, 27, x + 1.4, 30.4), '164F46', .7, dentro=tm)
    # la calle, y los monjes en fila, protagonistas, con la gente arrodillada que les da arroz
    calle = l.masa(box(-2, 31, 122, 41.5), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 31, 122, 41.5), 'D8C49A', .35, dentro=calle)
    for k in range(6):
        monje(l, 22 + k * 11.4, 38.6, 1.05 - k * .02)
    for x in (100, 110.6):
        arrodillada(l, x, 39.4, 1)


# ------------------------------------------------------------------------------------------------ Vientián
def that_luang(l, x, base, s=1.0):
    """la estupa del Pha That Luang, dorada: la base cuadrada con su escalinata, la corona de agujitas alrededor, el cuerpo en
    campana y la aguja alta en forma de pimpollo de loto"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    piezas = [box(x - 16 * s, base - 3 * s, x + 16 * s, base), box(x - 12.4 * s, base - 6 * s, x + 12.4 * s, base - 2.8 * s),
              forma(P([(-9, -6), (-9.6, -9.6), (-7.4, -13), (-3.6, -15), (3.6, -15), (7.4, -13), (9.6, -9.6), (9, -6)]), 2),
              forma(P([(-3.4, -14.8), (-2.6, -19), (-1.4, -24.4), (-.5, -29.6), (0, -31.6), (.5, -29.6), (1.4, -24.4), (2.6, -19), (3.4, -14.8)]), 2)]
    for u in np.arange(-14.6, 15, 2.7):                                  # las agujitas alrededor
        piezas.append(forma(P([(u - .8, -2.8), (u - .5, -5.4), (u, -7.6), (u + .5, -5.4), (u + .8, -2.8)]), 1))
    m = l.masa(piezas, material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.4)
    for v in (-9.6, -12.4, -17.6, -21, -24.4):                           # los anillos y molduras
        w = 9 if v > -14 else (3.6 + (v + 31.6) * .1)
        l.trazo(P([(-w * .9, v), (w * .9, v)]), .16 * s, color='6B4E10', alfa=.55, dentro=m)
    for u in (-6, -3, 0, 3, 6):                                          # los pétalos de loto del cuerpo
        l.trazo(P([(u - 1, -6.4), (u, -8.4), (u + 1, -6.4)]), .14 * s, color='6B4E10', alfa=.5, dentro=m)
    return m


def vientian(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .4)
    # enfrente, Tailandia, baja y lejana; el río tranquilo, sin olas
    prado(l, 17.4, 19, .2)
    for x in np.arange(2, 120, 4.6):
        arbol(l, x, 17.6, .9, material='lejos', semilla=int(x))
    a = rio(l, 18.6, semilla=3)
    # la orilla de acá, con la estupa dorada, protagonista
    orilla(l, forma([(-2, 33), (30, 31.4), (60, 31), (90, 31.4), (122, 33), (122, 41.5), (-2, 41.5)], 2), tinte=.24)
    piedra(l, box(28, 30, 92, 33.4), .15, .35)
    for x in np.arange(29, 92, 2.8):                                     # el claustro
        l.mancha(forma([(x, 33.2), (x, 31.4), (x + .7, 30.8), (x + 1.4, 31.4), (x + 1.4, 33.2)], 1), '164F46', .6)
    st = that_luang(l, 60, 30.4, .92)
    for x in (12, 108):
        palmera(l, x, 38, 13, 1 if x < 60 else -1, datiles=False)
    # el viento manso: ondas suaves que cruzan el cielo y el río, y una cometa que lleva
    for x0, y0, largo in ((4, 8, 30), (70, 5.4, 34), (10, 21, 26), (82, 23.6, 30), (38, 2.6, 22)):
        pts = [(x0 + t, y0 + 1 * math.sin(t / 4.6)) for t in np.arange(0, largo, 1)]
        l.trazo(pts, [.06] + [.3] * (len(pts) - 2) + [.06], color='FFFFFF', alfa=.9)
        cx, cy = pts[-1]
        l.trazo([(cx + 1.6 * math.cos(t), cy - 1.6 + 1.6 * math.sin(t)) for t in np.linspace(math.pi / 2, math.pi * 2.2, 14)], .3, color='FFFFFF',
                alfa=.9)
    k = Polygon([(98, 9), (101.4, 12.6), (98, 17.4), (94.6, 12.6)])     # la cometa
    l.masa(k, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.trazo([(98, 9.2), (98, 17.2)], .1, color='0C3A33', alfa=.6)
    l.trazo([(94.8, 12.6), (101.2, 12.6)], .1, color='0C3A33', alfa=.6)
    l.trazo([(98, 17.4), (96.6, 19.4), (98.4, 21.2), (96.8, 23)], .12, color='0C3A33', alfa=.7)
    l.trazo([(98, 17.4), (90, 26), (84, 32)], .06, color='0C3A33', alfa=.6)   # el hilo
    reflejo(l, st.g, 31.4, .15)


# ------------------------------------------------------------------------------------------------ Phnom Penh
def pulmon(x, y, s=1.0):
    """el contorno de un pulmón: redondeado afuera, con su lado de adentro hundido donde entra el bronquio, y el lóbulo de abajo"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    return forma(P([(4, -12), (0, -11), (-4.6, -7), (-7.6, -1), (-8.6, 5), (-7.6, 10), (-3, 12.4), (3, 12.4), (6.6, 11), (7.6, 8),
                    (5.4, 5), (4.4, 1), (5.6, -2), (6, -7)]), 3)


def phnom_penh(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 64, 2.6, 12, .4)
    # visto desde arriba: la tierra, el Mekong que baja por la derecha y el lago con forma de pulmón arriba a la izquierda
    tierra(l, 5, 41, desierto=.24)
    mekong = cinta([(110, 4), (104, 12), (96, 20), (90, 28), (86, 36), (84, 42)], [9, 10, 11, 12, 12, 12], 8)
    bassac = cinta([(88, 27), (78, 33), (72, 38), (68, 42)], [4, 5, 5.6, 6], 8)
    rio_ts = cinta([(36, 20.4), (48, 22.6), (62, 24.6), (76, 25.6), (89, 26)], [3.6, 4, 4.4, 4.8, 5.2], 8)
    lago = pulmon(24, 18, 1.35)
    agua(l, unary_union([mekong, bassac, rio_ts, lago.buffer(-.8)]).buffer(.3).buffer(-.3), ondas=12, semilla=6, linea=.35)
    def rama(x, y, ang, largo, ancho, nivel):                          # los bronquios: un árbol de canales claros, que se abre desde la entrada
        x1, y1 = x + largo * math.cos(math.radians(ang)), y + largo * math.sin(math.radians(ang))
        l.trazo([(x, y), (x1, y1)], [ancho, ancho * .75], color='C6EEDC', alfa=.85)
        if nivel:
            for d in (-32, 30):
                rama(x1, y1, ang + d, largo * .66, ancho * .7, nivel - 1)
    rama(32, 20.6, 200, 6.4, 1.4, 3)
    rama(32, 20.6, 135, 6, 1.2, 2)
    rama(32, 20.6, 250, 5.6, 1.2, 2)
    # el borde dorado del pulmón, protagonista
    l.masa(lago.difference(lago.buffer(-1.4)), material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
    # la ciudad en la confluencia, con los techos del Palacio Real
    for _ in range(26):
        x, y = rng.uniform(64, 84), rng.uniform(28, 40)
        g = box(x - 1.2, y - 1.4, x + 1.2, y)
        if g.intersects(unary_union([mekong, bassac, rio_ts]).buffer(.6)):
            continue
        l.masa(g, material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
        l.masa(Polygon([(x - 1.5, y - 1.4), (x, y - 2.6), (x + 1.5, y - 1.4)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2,
               arroja=False)
    l.masa([Polygon([(66, 33.6), (68, 30.6), (76, 30.6), (78, 33.6)]), Polygon([(69, 30.8), (72, 26.4), (75, 30.8)]), box(71.6, 24, 72.4, 26.8)],
           material='cuerpo', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    # la flecha dorada de ida y vuelta, sobre el río que une el lago con el Mekong: en lluvias entra al lago, en seca vuelve
    pts = [(38, 17.2), (50, 18.6), (62, 20.6), (76, 21.6), (86, 22)]
    c = curva(pts, 10)
    flecha = [cinta([tuple(p) for p in c], [1.1] * len(c), 2)]
    for (p0, p1) in ((c[1], c[0]), (c[-2], c[-1])):                      # las dos puntas
        d = np.array(p1) - np.array(p0)
        d = d / np.hypot(*d)
        n_ = np.array([-d[1], d[0]])
        q = np.array(p1)
        flecha.append(Polygon([tuple(q + d * 2.6), tuple(q + n_ * 2), tuple(q - n_ * 2)]))
    l.masa(flecha, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.4)


# ------------------------------------------------------------------------------------------------ Can Tho
def sombrero(l, x, y, r=2.2):
    """un sombrero cónico, dorado, visto un poco de costado: el cono chato con su ala"""
    return l.masa(forma([(x - r, y), (x - r * .4, y - r * .5), (x, y - r * .9), (x + r * .4, y - r * .5), (x + r, y), (x, y + r * .22)], 1),
                  material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.3, contraluz=.4)


def barca_mercado(l, x, y, s=1.0, carga=0, semilla=0, lado=1):
    """una barca del mercado flotante: el casco de madera con el ojo pintado en la proa, la carga de frutas y su gente con sombreros"""
    rng = np.random.default_rng(semilla)
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    c = l.masa(forma(P([(-9, -2.4), (8.4, -2.6), (10.4, -3.6), (9.6, -.6), (8, .8), (-8, .8), (-9.4, -.4)]), 1), material='vientre', alto=.3,
               brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(Polygon(P([(-10, -4), (11, -4), (11, 1), (-10, 1)])), '8A6A3A', .55, dentro=c)
    ox, oy = x + lado * 7.6 * s, y - 1.2 * s                              # el ojo de la proa
    l.mancha(ovalo(ox, oy, .9 * s, .55 * s), 'FFFFFF', .95, dentro=c)
    l.mancha(ovalo(ox + lado * .2 * s, oy, .4 * s, .4 * s), '05201C', 1, dentro=c)
    frutas = []
    for k in range(9):                                                   # la carga: sandías, piñas y racimos
        u = -6 + k * 1.5
        if carga == 0:
            frutas.append(ovalo(x + lado * u * s, y - 3 * s - (k % 2) * .9 * s, 1.1 * s, .8 * s))
        else:
            frutas.append(ovalo(x + lado * u * s, y - 3.2 * s - (k % 2) * .8 * s, .7 * s, 1 * s))
    f = l.masa(frutas, material='cuerpo' if carga == 0 else 'claro', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.25, arroja=False)
    if carga == 0:
        for k in range(9):
            u = -6 + k * 1.5
            l.trazo([(x + lado * (u - .8) * s, y - 3 * s - (k % 2) * .9 * s), (x + lado * (u + .8) * s, y - 3 * s - (k % 2) * .9 * s)], .1 * s,
                    color='164F46', alfa=.7, dentro=f)
    for k, u in enumerate((-7.4, 6)):                                    # la gente, con sus sombreros cónicos
        px = x + lado * u * s
        piel(l, [ovalo(px, y - 6 * s, .9 * s, 1 * s)], .5)
        l.masa(forma([(px - 1.1 * s, y - 2.4 * s), (px - 1.2 * s, y - 4.4 * s), (px + 1.2 * s, y - 4.4 * s), (px + 1.1 * s, y - 2.4 * s)], 1),
               material=('claro', 'lejos')[k], alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
        sombrero(l, px, y - 6.6 * s, 2.4 * s)
    return c


def can_tho(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 24, 4.4, 12, .5)
    nube(l, 98, 4, 10, .45)
    # atrás, la orilla con sus casas de palafito y sus palmeras, y el puente de tirantes, lejos
    prado(l, 14, 18, .22)
    l.masa(box(60, 11.4, 122, 12.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.2)
    for x in (76, 104):
        l.masa(box(x - .6, 3.4, x + .6, 12), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.2)
        for k in range(6):
            l.trazo([(x, 4 + k * 1.2), (x - 12 + k * 1.6, 11.6)], .06, color='8EB5AA', alfa=.9)
            l.trazo([(x, 4 + k * 1.2), (x + 12 - k * 1.6, 11.6)], .06, color='8EB5AA', alfa=.9)
    for x in np.arange(2, 120, 9):
        c = l.masa(box(x, 12.6, x + 6, 16.6), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        l.masa(Polygon([(x - .6, 12.8), (x + 3, 10.4), (x + 6.6, 12.8)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
        for xx in (x + 1, x + 5):
            l.trazo([(xx, 16.6), (xx, 18.6)], .2, color='5A3E1E', alfa=.8)
    for x in (8, 46, 92):
        palmera(l, x, 15.6, 7, 1, datiles=False)
    rio(l, 17.6, semilla=4)
    # las varas altas donde cuelgan lo que vende cada barca
    for x, cosa in ((30, 0), (52, 1), (78, 0), (98, 1)):
        l.trazo([(x, 34), (x, 9)], .3, color='5A3E1E', alfa=.9)
        if cosa == 0:
            l.masa([ovalo(x, 9.8, 1.4, 1), ovalo(x - .4, 11.6, 1.2, .9)], material='cuerpo', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.25)
        else:
            l.masa([ovalo(x + dx, 10 + dy, .6, 1.1) for dx, dy in ((-.8, 0), (0, .4), (.8, 0))], material='claro', alto=.4, brillo=.3, vientre=0,
                   hondo=0, linea=.2)
    # el mercado flotante, protagonista: las barcas apretadas como en una calle, con su gente de sombrero cónico
    for x, y, s, carga, lado in ((24, 24.4, .72, 1, 1), (60, 23.8, .72, 0, -1), (96, 24.4, .72, 1, -1), (38, 30.6, 1.05, 0, 1), (84, 30.4, 1.05, 1, -1),
                                 (16, 39.4, 1.5, 1, 1), (62, 40, 1.55, 0, 1), (106, 39.6, 1.5, 0, -1)):
        barca_mercado(l, x, y, s, carga, semilla=int(x), lado=lado)


# ------------------------------------------------------------------------------------------------ el mar
def dragon(l, x, base, alto_, lado=1, semilla=0):
    """un dragón dorado que sale del agua: el cuello en S con su cresta de púas, la cabeza larga con los cuernos, el bigote y la boca
    abierta; (x, base) es donde sale del agua"""
    s = alto_ / 14
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    control = P([(0, 1), (-1.6, -4), (1.4, -8), (0, -11.6)])
    eje = curva(control, 8)
    cuello = tubo(control, [2.4 * s, 2 * s, 1.7 * s, 1.5 * s], 8)
    cabeza = forma(P([(-1.2, -10.6), (-.6, -13.6), (2, -14.6), (5.6, -13.4), (6.6, -12.2), (4.6, -11.4), (6.4, -10.6), (5, -9.6), (1.4, -9.6)]), 1)
    cuernos = [tubo(P([(0, -13.6), (-1.6, -16), (-2.8, -16.6)]), [.5 * s, .35 * s, .15 * s], 5), tubo(P([(1, -14.2), (.4, -16.6), (-.6, -17.6)]), [.45 * s, .3 * s, .12 * s], 5)]
    puas = [Polygon([tuple(eje[k]), (eje[k][0] - lado * 1.4 * s, eje[k][1] - .6 * s), tuple(eje[k + 1])]) for k in range(0, len(eje) - 3, 3)]
    m = l.masa([cuello, cabeza] + cuernos + puas, material='acento', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.mancha(ovalo(x + lado * 2.4 * s, base - 12.4 * s, .45 * s, .45 * s), '05201C', 1)                  # el ojo
    l.trazo(P([(5.6, -11.2), (8.4, -10.4), (9.6, -11.8)]), .14 * s, color='6B4E10', alfa=.9)              # el bigote
    for k in range(1, len(eje) - 1, 2):                                  # las escamas
        l.trazo([(eje[k][0] - .6 * s, eje[k][1]), (eje[k][0] + .6 * s, eje[k][1] + .3 * s)], .12 * s, color='6B4E10', alfa=.6, dentro=m)
    return m


def mar(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    nube(l, 30, 4, 14, .45)
    nube(l, 96, 3.4, 12, .4)
    # atrás, el delta: los arrozales en franjas, con sus diques, y los nueve brazos que bajan al mar
    prado(l, 9, 24, .3)
    for y in np.arange(10.4, 23, 1.6):
        l.trazo([(-2, y), (122, y + .4)], .12, color='2F8A74', alfa=.45)
    for k in range(9):
        x = 6.6 + k * 13.4
        agua(l, cinta([(x + (k - 4) * -1.2, 9.6), (x + (k - 4) * -.4, 16), (x, 24)], [.8, 1.6, 3], 6), linea=.25)
    for x in (2, 118):
        mangle(l, x, 24, 8, semilla=x)
    # el mar, adelante, y un barco lejos
    horizonte = 23.6
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.6), '64C8AA', .5, dentro=m, difuso=.6)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # los nueve dragones, protagonistas: uno sale al mar de cada brazo
    for k in range(9):
        x = 6.6 + k * 13.4
        alto_ = 15 if k in (3, 4, 5) else (13 if k in (2, 6) else 11.4)
        lado = -1 if k < 4 else 1
        l.mancha(ovalo(x, horizonte + 3.6, 3.2, .8), 'FFFFFF', .6, difuso=.4)
        dragon(l, x, horizonte + 3.4, alto_, lado, semilla=k)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Jinghong', dibujar=jinghong), dict(clave='Luang Prabang', dibujar=luang_prabang),
            dict(clave='Vientián', dibujar=vientian), dict(clave='Phnom Penh', dibujar=phnom_penh), dict(clave='Can Tho', dibujar=can_tho),
            dict(clave='mar', dibujar=mar)]
LISTO = True
