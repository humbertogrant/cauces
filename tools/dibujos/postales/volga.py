# -*- coding: utf-8 -*-
"""Las postales del Volga, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar:

- el nacimiento, en las colinas de Valdái: el pantano entre abetos y abedules, con charcos y juncos, y el Volga que sale como un
  arroyito de la capillita de madera que está sobre el manantial, con su pasarela;
- Tver: «el Volga todavía cabe bajo un puente corto»: el río angosto que viene hacia nosotros y pasa bajo un puente de un solo arco,
  entre casas de madera y una iglesia de cúpulas de cebolla;
- Yaroslavl: el oso de su escudo, de pie, con el hacha dorada al hombro (la leyenda del príncipe que mató al oso con un hacha), en la
  orilla, y enfrente las iglesias de la ciudad;
- Nizhni Nóvgorod: la gran feria donde Oriente y Occidente regateaban: una balanza gigante pesa un cajón de té contra un fardo de
  pieles, en la lengua de tierra donde el Oká entra al Volga, y enfrente, sobre la colina, el Kremlin de ladrillo con sus torres;
- Kazán: un caldero (kazan, en tártaro) hirviendo sobre el fuego delante del Kremlin blanco, donde la mezquita Kul Sharif, con sus
  minaretes, y la catedral de cúpulas de cebolla comparten el recinto;
- Samara: «un anzuelo gigante»: visto desde arriba, el río rodea las montañas boscosas de Zhiguli y casi vuelve sobre sí mismo, como
  un anzuelo colgado de su sedal, entre campos;
- Volgogrado: la Madre Patria de Mamáyev Kurgán, una mujer de piedra que alza una espada y llama con la otra mano, en lo alto de su
  colina sobre el río;
- Astracán: un mercader con su gorro de astracán, de piel de rizos apretados, que muestra una lata de caviar abierta; la tapa, con su
  esturión, en el muelle del delta, donde el río se deshace en brazos entre juncales; lejos, las cúpulas del Kremlin;
- el mar: la lodia de los mercaderes del Volga, la barca del juego, que sale al Caspio, un mar cerrado, entre juncos y lotos en flor.

Desde el 2026-10-25 siguen la regla del protagonista: la imagen para recordar va grande y al medio, y es lo único dorado; sin sol.
"""
import math

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, abedul, abeto, agua, ave, cebolla, cielo, cinta, iglesia, juncos, loto, nube, orilla, pasto,  # noqa: F401
                     prado, reflejo, rio)
from pintor import forma, ovalo, tubo


def casa_madera(l, x, base, w=6.0, h=4.0, techo='lejos'):
    """una izba: la casa de troncos con su techo a dos aguas y sus ventanas con marco claro"""
    c = l.masa(box(x - w / 2, base - h, x + w / 2, base).buffer(.1), material='vientre', alto=.25, brillo=.05, vientre=0, hondo=0,
               linea=.35, escalon=.2)
    l.mancha(box(x - w / 2, base - h, x + w / 2, base), 'E8B952', .3, dentro=c)
    for k in np.arange(base - h + .7, base, .8):                     # los troncos
        l.trazo([(x - w / 2, k), (x + w / 2, k)], .08, color='6B4E10', alfa=.5, dentro=c)
    for dx in (-w * .22, w * .22):
        l.mancha(box(x + dx - .6, base - h * .72, x + dx + .6, base - h * .3), 'F0F6F4', .95, dentro=c)
        l.mancha(box(x + dx - .38, base - h * .66, x + dx + .38, base - h * .36), '164F46', .85, dentro=c)
    l.masa(Polygon([(x - w / 2 - .6, base - h), (x, base - h - w * .42), (x + w / 2 + .6, base - h)]).buffer(.1), material=techo, alto=.25,
           brillo=.1, vientre=0, hondo=0, linea=.35)


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(2)
    cielo(l, sol=None)
    nube(l, 30, 6, 16, .7)
    nube(l, 92, 4.4, 11, .55)
    # las colinas de Valdái, bajas y redondas, con su bosque de abetos
    l.masa(forma([(-2, 22), (10, 18.4), (26, 17.2), (40, 19), (56, 16.6), (72, 18.2), (90, 16.2), (108, 18.4), (122, 17.4), (122, 26),
                  (-2, 26)], 3), material='lejos', alto=.2, brillo=.05, vientre=0, hondo=0, linea=.35, contraluz=.25)
    for x in np.arange(1, 121, 2.8):
        abeto(l, x + rng.uniform(-.8, .8), 22.6 + rng.uniform(-1.2, .4), rng.uniform(5, 7.6), rng.uniform(2.6, 3.4))
    # el pantano: una pradera chata y húmeda, con manchas de musgo, charcos y matas de pasto
    t = prado(l, 22.4, 41, .3)
    for _ in range(70):
        x, y = rng.uniform(-2, 122), rng.uniform(23.4, 41)
        l.mancha(ovalo(x, y, rng.uniform(1.6, 4.4), rng.uniform(.35, .8)), str(rng.choice(['3D9582', 'E8B952'])), .18, dentro=t,
                 difuso=.3)
    for x, y, rx, ry in ((14, 27, 7, 1.1), (30, 32.6, 8, 1.3), (90, 28.4, 8, 1.2), (102, 34.4, 10, 1.6), (12, 37.6, 8, 1.5)):
        agua(l, ovalo(x, y, rx, ry), ondas=1, semilla=int(x), linea=.2)
    pasto(l, 0, 120, 24, 40, 30, semilla=3)
    # el manantial, bajo la capillita, y el Volga que sale de él como un arroyito, hacia nosotros
    cx, pie, e = 60, 28, 1.3
    agua(l, ovalo(cx, pie - .6, 6.4, 1.4), ondas=1, linea=.2)
    agua(l, cinta([(cx - .6, pie), (cx - 3.4, 31.4), (cx + 1.6, 34.4), (cx - 3, 37.8), (cx - .6, 41.5)], [1, 1.6, 2.4, 3.2, 4.2]), ondas=3,
         semilla=4, linea=.25)
    # la capillita de madera sobre pilotes, protagonista, con su cúpula dorada, y la pasarela de tablas que llega hasta ella
    P = lambda pts: [(cx + u * e, pie + v * e) for u, v in pts]
    for u in np.arange(-19, -2, 2.4):
        l.masa(Polygon(P([(u - .15, -2.4), (u + .15, -2.4), (u + .15, -.6), (u - .15, -.6)])), material='lejos', alto=.2, brillo=.1,
               vientre=0, hondo=0, linea=.2, arroja=False)
    pa = l.masa(Polygon(P([(-20, -3.2), (-2, -3.2), (-2, -2.4), (-20, -2.4)])), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0,
                linea=.3)
    for u in np.arange(-19.4, -2, 1.1):
        l.trazo(P([(u, -3.1), (u, -2.5)]), .07, color='0C3A33', alfa=.6, dentro=pa)
    l.masa([Polygon(P([(x - .25, -10), (x + .25, -10), (x + .25, 0), (x - .25, 0)])) for x in (-2.4, 2.4)], material='lejos', alto=.2,
           brillo=.1, vientre=0, hondo=0, linea=.25)
    cap = l.masa(Polygon(P([(-3.4, -10.2), (3.4, -10.2), (3.4, -4), (-3.4, -4)])).buffer(.1), material='vientre', alto=.25, brillo=.05,
                 vientre=0, hondo=0, linea=.35)
    l.mancha(Polygon(P([(-4, -11), (4, -11), (4, -3.6), (-4, -3.6)])), 'E8B952', .35, dentro=cap)
    for v in np.arange(-9.5, -4, .75):
        l.trazo(P([(-3.4, v), (3.4, v)]), .07, color='6B4E10', alfa=.5, dentro=cap)
    l.mancha(forma(P([(-.9, -4), (-.9, -7.4), (0, -8.2), (.9, -7.4), (.9, -4)]), 1), '164F46', .85, dentro=cap)
    l.masa(Polygon(P([(-4.6, -10), (0, -14), (4.6, -10)])).buffer(.1), material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.masa(Polygon(P([(-.8, -15.8), (.8, -15.8), (.8, -13.6), (-.8, -13.6)])), material='vientre', alto=.2, brillo=.05, vientre=0, hondo=0,
           linea=.3)
    l.masa(cebolla(cx, pie - 15.8 * e, 1.2 * e), material='acento', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.3, contraluz=.3)
    tope = pie - (15.8 + 1.2 * 3.05) * e
    l.trazo([(cx, tope + .1), (cx, tope - 2)], .18, alfa=.9)
    l.trazo([(cx - .7, tope - 1.2), (cx + .7, tope - 1.2)], .16, alfa=.9)
    for x, y, h in ((6, 30, 10), (12, 28.4, 8.4), (96, 29, 9), (110, 31, 11), (116, 27.6, 8)):
        abedul(l, x, y, h, 2.2, semilla=int(x))
    juncos(l, 72, 92, 34.6, 4.4, 30, semilla=5)
    juncos(l, 22, 40, 39.6, 5, 30, semilla=6)


# ------------------------------------------------------------------------------------------------ Tver
def tver(l):
    cielo(l, sol=None)
    nube(l, 26, 6, 14, .6)
    nube(l, 98, 4.4, 10, .45)
    prado(l, 19, 41)
    # el río angosto, que viene de lejos hacia nosotros y se ensancha
    w = lambda y: 3 + (y - 19) / 22.5 * 53
    lecho = Polygon([(60 - w(19) / 2, 19), (60 + w(19) / 2, 19), (60 + w(41.5) / 2, 41.5), (60 - w(41.5) / 2, 41.5)])
    agua(l, lecho, linea=.3)
    for k in range(6):                                                # las ondas, más grandes adelante
        y = 32 + k * 1.6
        s_ = (y - 19) / 22.5
        for dx in (-.28, .18):
            x = 60 + dx * w(y) + (k % 2) * 3 * s_
            l.trazo([(x - 2.4 * s_, y), (x, y - .25 * s_), (x + 2.4 * s_, y)], .1 + .12 * s_, color='D2F2DA', alfa=.8)
    # la línea de árboles lejos, que tapa de dónde viene el río, y en las orillas, las casas de madera y la iglesia
    for x in np.arange(-1, 121, 3.2):
        l.masa(ovalo(x, 18.6, 1.9, 1.3), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.22, arroja=False)
    for x, b, w_ in ((6, 22.4, 6), (15, 22, 7), (24.4, 22.6, 6)):
        casa_madera(l, x, b, w_, 4.2)
    iglesia(l, 105, 22.6, 12, 7, cupulas=((0, 1.1), (-4, .66), (4, .66)), dorada=None)
    for x, h in ((92, 8.6), (118, 7.6)):
        abedul(l, x, 23.4, h, 2, semilla=int(x))
    # el puente corto, protagonista: de piedra, de un solo arco, que cruza el río de orilla a orilla
    agua_y, yt = 29, 17
    r = w(agua_y) / 2
    x0, x1 = 60 - r - 11, 60 + r + 11
    arco = ovalo(60, agua_y, r + .4, 8)
    pte = box(x0, yt, x1, agua_y + .8).difference(arco).difference(box(60 - r - .4, agua_y, 60 + r + .4, agua_y + 2))
    l.mancha(arco.intersection(box(40, agua_y - 2.6, 80, agua_y)), '0C3A33', .35)          # la sombra bajo el arco
    espejo = affinity.scale(pte, 1, -1, origin=(0, agua_y)).intersection(lecho)
    for k in np.arange(agua_y + .2, 39, .9):                            # su reflejo, que cierra el ojo del arco
        l.mancha(espejo.intersection(box(-2, k, 122, k + .5)), 'D2F2DA', .55 * max(0, 1 - (k - agua_y) / 9))
    p = l.masa(pte, material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.5, escalon=.2, contraluz=.3)
    l.mancha(box(x0, yt, x1, yt + 1.6), 'CFE0DA', .8, dentro=p)
    for a in range(10, 175, 11):                                        # las dovelas del arco
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        l.trazo([(60 + (r + .4) * c, agua_y - 8 * s_), (60 + (r + 2.6) * c, agua_y - 10.2 * s_)], .14, color='8EB5AA', alfa=.9, dentro=p)
    for x in np.arange(x0 + 1, x1, 2.2):                                # la baranda
        l.trazo([(x, yt - 1.6), (x, yt)], .2, alfa=.8)
    l.trazo([(x0 - .3, yt - 1.7), (x1 + .3, yt - 1.7)], .3, alfa=.9)
    # las orillas de adelante, con pasto y juncos
    for x, s_ in ((4, 1), (116, -1)):
        orilla(l, forma([(x - 12 * s_, 41.5), (x - 12 * s_, 33), (x, 33.6), (x + 12 * s_, 36.4), (x + 18 * s_, 41.5)], 2))
    juncos(l, 4, 16, 40.8, 4.4, 20, semilla=7)
    juncos(l, 104, 116, 40.8, 4.4, 20, semilla=8)


# ------------------------------------------------------------------------------------------------ Yaroslavl
def hacha(l, bajo, alto_):
    """el hacha del escudo: el asta de madera y, arriba, la hoja dorada que se abre hacia afuera en media luna, con su barba"""
    p0, p1 = np.array(bajo, float), np.array(alto_, float)
    d = (p1 - p0) / np.hypot(*(p1 - p0))
    n = np.array([-d[1], d[0]])
    if n[0] < 0:
        n = -n
    l.masa(tubo([p0, p1 + d * .6], [.42, .36], 6), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    c = p1 - d * 2.6
    P = lambda u, v: tuple(c + d * u + n * v)
    hoja = forma([P(1.6, -.2), P(2.8, 1.8), P(5.6, 5.4), P(3.6, 6.6), P(.8, 7.2), P(-2.6, 6.8), P(-5.2, 5.8), P(-6.6, 4.4), P(-3.8, 3.4),
                  P(-2.2, 1.6), P(-1.6, -.2)], 2)
    h = l.masa(hoja, material='acento', alto=.35, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo([P(4.8, 5.6), P(3.2, 6.3), P(.8, 6.8), P(-2.6, 6.4), P(-5, 5.5), P(-6, 4.6)], [.1, .3, .36, .36, .3, .1], color='FBEFCB', alfa=.9,
            dentro=h)                                                   # el filo
    l.mancha(Polygon([P(1.5, 0), P(1.5, 1), P(-1.5, 1), P(-1.5, 0)]).buffer(.1), '6B4E10', .6, dentro=h)    # el ojo, donde entra el asta


def oso(l, x, base):
    """el oso del escudo de Yaroslavl, de pie, de perfil y mirando a la izquierda, con el hacha dorada al hombro"""
    patas = [tubo([(x + 2.6, base - 10.4), (x + 2.8, base - 6), (x + 3.2, base - 1.6)], [2.8, 2.3, 1.9]),
             tubo([(x + .4, base - 10), (x - .8, base - 5.6), (x - 1, base - 1.6)], [3.1, 2.5, 2])]
    pies = [ovalo(x + 1.8, base - .9, 2.6, 1), ovalo(x - 2.6, base - .9, 2.8, 1.1)]
    cuerpo = forma([(x - 3.4, base - 8.4), (x - 4.4, base - 13), (x - 4.6, base - 17.4), (x - 3.8, base - 20.6), (x - 1.8, base - 22.8),
                    (x + 1, base - 24), (x + 3.4, base - 23.4), (x + 4.8, base - 21), (x + 5.4, base - 16), (x + 5.6, base - 11),
                    (x + 4.4, base - 7.4), (x + 1, base - 6.4), (x - 2, base - 6.8)], 3)
    cabeza = forma([(x + 1.4, base - 22.4), (x + 1.6, base - 25.6), (x + .2, base - 27.6), (x - 2, base - 28.2), (x - 3.6, base - 27.2),
                    (x - 5, base - 26.4), (x - 7.2, base - 26), (x - 7.8, base - 25), (x - 7.2, base - 24.1), (x - 4.8, base - 23.6),
                    (x - 3, base - 22.2), (x - 1, base - 21.6)], 2)
    orejas = [ovalo(x - .6, base - 28.3, 1.1, 1.1), ovalo(x + 1, base - 27.8, .9, .9)]
    lejano = tubo([(x + 1.6, base - 21.4), (x + 2.2, base - 19.6), (x + .6, base - 18.4)], [1.6, 1.4, 1.2])    # el brazo de atrás
    b = l.masa(patas + pies + [cuerpo, cabeza] + orejas + [lejano], material='lejos', alto=.5, brillo=.12, vientre=.1, hondo=.1,
               linea=.5, escalon=.2, contraluz=.35, bultos=[(ovalo(x + .6, base - 15, 4.4, 6), .25)])
    l.pelaje(b, densidad=2.4, largo=1.1, ancho=.16, alfa=.35, semilla=9, claro=.3, flujo=100)
    l.mancha(forma([(x - 4.8, base - 25.2), (x - 7.4, base - 25.6), (x - 7.6, base - 24.6), (x - 5, base - 23.8)], 1), '8BD0B9', .6,
             dentro=b, difuso=.2)                                   # el hocico, más claro
    l.mancha(ovalo(x - 7.5, base - 25.3, .55, .45), '05201C', .95, dentro=b)       # la nariz
    l.trazo([(x - 7.2, base - 24.4), (x - 5.4, base - 24.1)], .1, color='05201C', alfa=.8, dentro=b)
    l.mancha(ovalo(x - 3.3, base - 25.9, .38, .38), '05201C', .95, dentro=b)       # el ojo
    l.mancha(ovalo(x - 3.4, base - 26, .13, .13), 'F0F6F4', 1, dentro=b)
    l.mancha(ovalo(x - .6, base - 28.3, .5, .5), '05201C', .6, dentro=b)           # la oreja por dentro
    # el hacha, apoyada en el hombro, y el brazo de adelante, que la agarra
    hacha(l, (x - 5.2, base - 9.2), (x + 7.4, base - 30.4))
    cerca = tubo([(x - .4, base - 21.4), (x - 2.4, base - 17.2), (x - 3.2, base - 13.8)], [1.9, 1.6, 1.4])
    br = l.masa(cerca, material='lejos', alto=.45, brillo=.15, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.pelaje(br, densidad=2.4, largo=1, ancho=.15, alfa=.35, semilla=10, claro=.3, flujo=110)
    for px, py in ((x - 3.2, base - 13.6), (x + .5, base - 18.4)):            # las garras, sobre el asta
        for k in (-.45, 0, .45):
            l.trazo([(px - 1 + k * .3, py - .5 + k), (px - 1.6 + k * .3, py - .2 + k)], .13, color='F0F6F4', alfa=.9)


def yaroslavl(l):
    cielo(l, sol=None)
    nube(l, 22, 6, 12, .55)
    nube(l, 96, 4.4, 10, .45)
    # la otra orilla, con las iglesias de la ciudad
    prado(l, 21.6, 26)
    for x in np.arange(-1, 121, 3.2):
        if 6 < x < 26 or 90 < x < 114:
            continue
        l.masa(ovalo(x, 22.2, 2, 1.5), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.25, arroja=False)
    iglesia(l, 16, 23, 12, 7, cupulas=((0, 1.1), (-4, .65), (4, .65)), dorada=None)
    iglesia(l, 102, 23, 13, 7.6, cupulas=((0, 1.2), (-4.2, .7), (4.2, .7), (-2, .55), (2, .55)), dorada=None)
    # el río, y la orilla de adelante, donde está el oso
    rio(l, 24.6)
    m = orilla(l, forma([(-2, 41.5), (-2, 33.4), (14, 32.2), (34, 31.2), (60, 30.8), (86, 31.4), (106, 32.6), (122, 33.6),
                         (122, 41.5)], 2))
    pasto(l, 0, 120, 33, 40.6, 34, semilla=11, dentro=m)
    oso(l, 60, 38.8)


# ------------------------------------------------------------------------------------------------ Nizhni Nóvgorod
def torre_kremlin(l, x, base, w=4.0, h=10.0):
    """una torre del Kremlin de ladrillo: el cuerpo con sus hileras y el techo en carpa, verde, con su veleta"""
    t = l.masa(box(x - w / 2, base - h, x + w / 2, base).buffer(.1), material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.4,
               escalon=.2, contraluz=.25)
    l.mancha(box(x - w, base - h - 1, x + w, base), 'E8B952', .28, dentro=t)
    for k in np.arange(base - h + 1, base, 1.1):
        l.trazo([(x - w / 2, k), (x + w / 2, k)], .06, color='6B4E10', alfa=.45, dentro=t)
    l.mancha(box(x - .4, base - h * .6, x + .4, base - h * .45), '0C3A33', .8, dentro=t)
    l.masa(Polygon([(x - w / 2 - .5, base - h), (x, base - h - w * 1.4), (x + w / 2 + .5, base - h)]).buffer(.1), material='cuerpo', alto=.3,
           brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.trazo([(x, base - h - w * 1.4), (x, base - h - w * 1.4 - 1.2)], .14, alfa=.9)


def tienda(l, x, base, w=9.0, h=5.6, banderin='cuerpo'):
    """una caseta de la feria: el mostrador con su sombra adentro y el toldo a rayas"""
    c = l.masa(box(x - w / 2, base - h * .6, x + w / 2, base).buffer(.1), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0,
               linea=.35)
    l.mancha(box(x - w / 2 + .8, base - h * .48, x + w / 2 - .8, base - h * .1), '164F46', .7, dentro=c)
    toldo = Polygon([(x - w / 2 - .9, base - h * .55), (x, base - h), (x + w / 2 + .9, base - h * .55)]).buffer(.1)
    t = l.masa(toldo, material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    xs = np.linspace(x - w / 2 - 1, x + w / 2 + 1, 9)
    for a, b in zip(xs[0::2], xs[1::2]):
        l.mancha(Polygon([(a, base - h * .5), (b, base - h * .5), (x, base - h - .2)]), '4AA189', .9, dentro=t)
    l.trazo([(x, base - h), (x, base - h - 1.6)], .12, alfa=.9)
    l.masa(Polygon([(x, base - h - 1.6), (x + 1.4, base - h - 1.2), (x, base - h - .8)]), material=banderin, alto=.2, brillo=.2,
           vientre=0, hondo=0, linea=.15, arroja=False)                # el banderín


def caja_te(l, x, base, w=5.4, h=4.2):
    """un cajón de té: la madera clara con sus flejes y el sello del té, una hoja"""
    c = l.masa(box(x - w / 2, base - h, x + w / 2, base).buffer(.08), material='vientre', alto=.25, brillo=.12, vientre=0, hondo=0,
               linea=.35)
    l.mancha(box(x - w / 2, base - h, x + w / 2, base), 'E8B952', .45, dentro=c)
    for yy in (base - h + .45, base - .45):
        l.trazo([(x - w / 2, yy), (x + w / 2, yy)], .14, color='6B4E10', alfa=.7, dentro=c)
    m = base - h / 2
    l.mancha(forma([(x - 1.3, m + .7), (x - .5, m - .6), (x + .8, m - 1.1), (x + 1.4, m - 1.2), (x + .9, m), (x - .2, m + .6)], 2), '2F8A74',
             .95, dentro=c)
    l.trazo([(x - 1.3, m + .7), (x + 1.1, m - 1)], .08, color='0C3A33', alfa=.7, dentro=c)


def piel(x, y, largo=6.0, giro=0.0):
    """una piel de marta colgada de la nariz: la cabeza arriba con sus orejitas, el cuerpo que se ensancha, las patitas y la cola
    peluda abajo"""
    L = largo
    cuerpo = forma([(x, y), (x - .55, y + .7), (x - .8, y + 1.6), (x - 1.05, y + L * .5), (x - .85, y + L * .85), (x - .4, y + L),
                    (x + .4, y + L), (x + .85, y + L * .85), (x + 1.05, y + L * .5), (x + .8, y + 1.6), (x + .55, y + .7)], 2)
    orejas = [Polygon([(x - .7, y + 1.1), (x - 1.1, y + .4), (x - .3, y + .9)]), Polygon([(x + .7, y + 1.1), (x + 1.1, y + .4), (x + .3, y + .9)])]
    patas = [Polygon([(x - .8, y + 1.8), (x - 1.8, y + 2.6), (x - .9, y + 2.5)]), Polygon([(x + .8, y + 1.8), (x + 1.8, y + 2.6), (x + .9, y + 2.5)]),
             Polygon([(x - .8, y + L * .8), (x - 1.7, y + L * .95), (x - .7, y + L * .92)]),
             Polygon([(x + .8, y + L * .8), (x + 1.7, y + L * .95), (x + .7, y + L * .92)])]
    cola = tubo([(x, y + L - .2), (x + .25, y + L + 1.4), (x - .1, y + L + 3)], [.5, .75, .4], 6)
    return affinity.rotate(unary_union([cuerpo, cola] + orejas + patas).buffer(.03), giro, origin=(x, y))


def pieles(l, puntos, largo=6.0, semilla=0):
    """unas pieles colgadas, cada una de su punto (x, y, giro), peludas, con el pelo que cae"""
    f = l.masa([piel(x, y, largo, g) for x, y, g in puntos], material='lejos', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.3,
               contraluz=.3)
    l.pelaje(f, densidad=9, largo=.5, ancho=.11, alfa=.55, semilla=semilla, claro=.4, flujo=90)
    for x, y, g in puntos:                                              # el ojito
        l.mancha(affinity.rotate(ovalo(x - .35, y + 1.2, .14, .14), g, origin=(x, y)), '05201C', .9, dentro=f)
        l.mancha(affinity.rotate(ovalo(x + .35, y + 1.2, .14, .14), g, origin=(x, y)), '05201C', .9, dentro=f)


def balanza(l, x, base, alto_=20.0, brazo=11.0, lado=1):
    """la gran balanza de la feria: de un lado, un platillo colgado de cadenas (a la izquierda; a la derecha con `lado` -1); del otro,
    un gancho; da dónde asienta el platillo y dónde está el gancho"""
    tope = base - alto_
    l.masa([box(x - .45, tope, x + .45, base - .8), forma([(x - 3.6, base), (x - 2.4, base - 1.4), (x + 2.4, base - 1.4), (x + 3.6, base)], 1)],
           material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.35, contraluz=.3)
    xp, yp = x - lado * (brazo - .4), tope + 7
    for dx in (-2.8, 2.8):
        l.trazo([(xp, tope + .3), (xp + dx, yp)], .1, alfa=.85)
    xg, yg = x + lado * (brazo - .4), tope + 3.4
    l.trazo([(xg, tope + .3), (xg, yg - .6)], .14, alfa=.9)
    l.masa([box(x - brazo, tope - .35, x + brazo, tope + .35).buffer(.1), ovalo(x, tope - .7, .9, .9)], material='oscuro', alto=.3,
           brillo=.35, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.masa(forma([(x - .7, tope - 1.4), (x, tope - 3.4), (x + .7, tope - 1.4)], 1), material='acento', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.3)                                           # el fiel
    l.masa(forma([(xp - 3.4, yp), (xp + 3.4, yp), (xp + 2.4, yp + 1.2), (xp - 2.4, yp + 1.2)], 1), material='acento', alto=.3, brillo=.3,
           vientre=0, hondo=0, linea=.35, contraluz=.3)
    return (xp, yp), (xg, yg)


def gancho(l, x, y):
    """el gancho de donde cuelgan las pieles, con su cuerda dorada"""
    l.masa(ovalo(x, y, .8, .7).difference(ovalo(x, y, .4, .35)), material='oscuro', alto=.2, brillo=.35, vientre=0, hondo=0, linea=.25)


def nizhni(l):
    cielo(l, sol=None)
    nube(l, 30, 5, 12, .5)
    # la otra orilla del Volga, baja y lejos, a la izquierda
    prado(l, 21.4, 24.4)
    for x in np.arange(-1, 56, 3.2):
        l.masa(ovalo(x, 21.6, 1.8, 1.3), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.22, arroja=False)
    agua(l, box(-2, 23.4, 122, 41.5), ondas=10, semilla=4, linea=0)     # donde el Oká entra al Volga
    # la colina alta, a la derecha, con el Kremlin de ladrillo, cuyas murallas suben por la ladera
    colina = forma([(48, 29.6), (56, 26), (64, 21), (74, 15.4), (88, 12.6), (122, 11.8), (122, 30), (48, 30)], 2)
    l.masa(colina, material='cuerpo', alto=.35, brillo=.08, vientre=0, hondo=.1, linea=.4, contraluz=.3)
    for x, y in ((62, 24.6), (70, 20.8), (84, 15.6), (104, 14.6), (116, 16.6), (92, 26), (108, 27)):
        l.masa([ovalo(x + dx, y + dy, 1.8, 1.5) for dx, dy in ((0, 0), (-1.4, .6), (1.4, .5))], material='lejos', alto=.3, brillo=.05,
               vientre=0, hondo=0, linea=.25)
    muro_pts = [(54, 28), (63, 23), (72, 18.4), (84, 15), (100, 13.8), (122, 13.4)]
    muro = []
    for (xa, ya), (xb, yb) in zip(muro_pts[:-1], muro_pts[1:]):
        muro.append(Polygon([(xa, ya), (xb, yb), (xb, yb - 3.4), (xa, ya - 3.4)]))
        for u in np.linspace(0, 1, int(abs(xb - xa) / 1.5) + 1)[:-1]:   # las almenas en cola de golondrina
            xm, ym = xa + (xb - xa) * u, ya + (yb - ya) * u - 3.4
            muro.append(Polygon([(xm, ym + .1), (xm, ym - 1), (xm + .35, ym - .7), (xm + .7, ym - 1), (xm + .7, ym + .1)]))
    m = l.masa(unary_union(muro), material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, escalon=.2, contraluz=.25)
    l.mancha(box(40, 0, 122, 31), 'E8B952', .2, dentro=m)
    for (x, y), h in zip(muro_pts[:-1], (8, 8.6, 9.6, 8.4, 9)):
        torre_kremlin(l, x, y + .4, 3.6, h)
    # la lengua de tierra, adelante, con la feria: una caseta y un puesto de pieles colgadas
    s_ = orilla(l, forma([(-2, 41.5), (-2, 30), (20, 29.6), (44, 30.2), (70, 31.8), (92, 34), (114, 35.2), (122, 35.6), (122, 41.5)], 2))
    pasto(l, 0, 120, 33, 40.6, 18, semilla=12, dentro=s_)
    tienda(l, 10, 34.4, 12, 7.4)
    l.masa([box(97.2, 30.6, 98, 38.6), box(116, 31.6, 116.8, 39.2), tubo([(96.6, 31.2), (117.4, 32.2)], [.3, .3], 4)], material='lejos',
           alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    pieles(l, [(100 + k * 3.6, 31.6 + k * .18, (-1) ** k * 4) for k in range(5)], 4.6, semilla=13)
    # la balanza gigante, protagonista, al medio: un atado de pieles, contra el cielo, y un cajón de té, contra la colina
    (xa, ya), (xg, yg) = balanza(l, 60, 39.4, 26, 17, lado=-1)
    caja_te(l, xa, ya, 6.6, 5)
    pieles(l, [(xg - 2.2, yg + .3, 14), (xg, yg + .7, 0), (xg + 2.2, yg + .3, -14)], 7, semilla=15)
    gancho(l, xg, yg)


# ------------------------------------------------------------------------------------------------ Kazán
def minarete(l, x, base, h=18.0, r=.9):
    """un minarete de la Kul Sharif: la torre fina, sus dos balcones y la punta cónica"""
    t = [box(x - r, base - h, x + r, base)]
    for f in (.45, .78):
        y = base - h * f
        t.append(box(x - r - .7, y - .5, x + r + .7, y + .3))
    l.masa(unary_union(t), material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.masa(Polygon([(x - r - .2, base - h), (x, base - h - 4.2), (x + r + .2, base - h)]).buffer(.05), material='cuerpo', alto=.3,
           brillo=.3, vientre=0, hondo=0, linea=.3)


def llama(x, y, w, h, lado=1):
    """una lengua de fuego que sube desde (x, y) y se tuerce un poco hacia `lado`"""
    return forma([(x - w / 2, y), (x - w * .45, y - h * .4), (x - w * .1 * lado, y - h * .75), (x + w * .15 * lado, y - h),
                  (x + w * .2 * lado, y - h * .7), (x + w * .45, y - h * .35), (x + w / 2, y)], 2)


def burbuja(l, x, y, r):
    """una burbuja: clara, con su brillo y su borde"""
    l.mancha(ovalo(x, y, r, r * .8), 'D2F2DA', .95)
    l.mancha(ovalo(x - r * .3, y - r * .3, r * .3, r * .25), 'FFFFFF', 1)
    t = np.linspace(0, 2 * math.pi, 16)
    l.trazo([(x + r * math.cos(a), y + r * .8 * math.sin(a)) for a in t], .09, color='3E7A6D', alfa=.8)


def muralla(l, arriba, abajo, torres, alto_torre, ancho_torre=5.2, techo=4.8, linea=.4):
    """un lienzo de la muralla blanca del Kremlin, de `arriba` a `abajo`, con sus almenas y sus torres de techo en carpa"""
    muro = box(-2, arriba, 122, abajo)
    for x in np.arange(-1.4, 122, 2.2):
        muro = muro.union(box(x, arriba - 1, x + 1.1, arriba + .2))
    a = ancho_torre / 2
    for x in torres:
        muro = muro.union(forma([(x - a, abajo), (x - a, alto_torre + .8), (x - a + 1, alto_torre), (x + a - 1, alto_torre),
                                 (x + a, alto_torre + .8), (x + a, abajo)], 1))
    m = l.masa(muro, material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=linea, escalon=.2, contraluz=.25)
    for x in torres:
        l.masa(Polygon([(x - a - .4, alto_torre + .4), (x, alto_torre - techo), (x + a + .4, alto_torre + .4)]).buffer(.1),
               material='cuerpo', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.35)
        l.mancha(box(x - .35, alto_torre + 2.6, x + .35, alto_torre + 4.4), '0C3A33', .75, dentro=m)
    return m


def kazan(l):
    cielo(l, sol=None)
    nube(l, 84, 5, 12, .45)
    prado(l, 20, 41)
    # el fondo del Kremlin: el lienzo de muralla de atrás, lejos
    muralla(l, 18.8, 21.4, (4, 118), 15.6, 4, 3.6, linea=.3)
    # la mezquita Kul Sharif, a la izquierda: el cuerpo blanco con sus arcos, la cúpula turquesa y los cuatro minaretes
    mx = 28
    minarete(l, mx - 11, 21.4, 15, .75)
    minarete(l, mx + 11, 21.4, 15, .75)
    cuerpo = l.masa(box(mx - 9, 11.4, mx + 9, 22).buffer(.2), material='claro', alto=.3, brillo=.12, vientre=0, hondo=0, linea=.4,
                    escalon=.2, contraluz=.3)
    for x in np.arange(mx - 7, mx + 7, 3):
        l.mancha(forma([(x, 21), (x, 15.4), (x + .9, 14.2), (x + 1.8, 15.4), (x + 1.8, 21)], 1), '164F46', .75, dentro=cuerpo)
    l.masa(forma([(mx - 6, 11.8), (mx - 5.4, 8), (mx - 2.4, 4.6), (mx, 3.6), (mx + 2.4, 4.6), (mx + 5.4, 8), (mx + 6, 11.8)], 2),
           material='cuerpo', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo([(mx, 3.8), (mx, 1.4)], .18, alfa=.9)
    minarete(l, mx - 13, 25, 17, .9)
    minarete(l, mx + 13, 25, 17, .9)
    # la catedral, a la derecha, de cúpulas de cebolla, en el mismo recinto
    iglesia(l, 104, 24.2, 11, 7, cupulas=((0, 1.05), (-3.6, .62), (3.6, .62), (-1.8, .5), (1.8, .5)), dorada=None)
    # el caldero, protagonista, al medio, hirviendo sobre el fuego en el patio del Kremlin
    cx, ry = 60, 24
    l.mancha(ovalo(cx, 34.6, 15, 3.6), 'F2D48A', .5, difuso=1.4)      # el resplandor del fuego
    for dx, y, w, h, s_ in ((-12.4, 36, 3.6, 8.8, -1), (-8.6, 36.6, 3.2, 6.8, 1), (8.6, 36.6, 3.2, 6.8, -1), (12.4, 36, 3.6, 8.8, 1)):
        f = l.masa(llama(cx + dx, y, w, h, s_), material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3, contraluz=.3)
        l.mancha(llama(cx + dx, y - .2, w * .5, h * .6, s_), 'FBEFCB', .9, dentro=f)
    caldero = forma([(cx - 13, ry), (cx + 13, ry), (cx + 12.4, ry + 3.8), (cx + 9.6, ry + 7.8), (cx + 4, ry + 9.8), (cx - 4, ry + 9.8),
                     (cx - 9.6, ry + 7.8), (cx - 12.4, ry + 3.8)], 3)
    l.masa(caldero, material='oscuro', alto=.6, brillo=.5, vientre=0, hondo=0, linea=.5, contraluz=.4)
    for x in (cx - 13.2, cx + 13.2):                                    # las asas
        l.masa(ovalo(x, ry + 1.6, 1.5, 1.1).difference(ovalo(x, ry + 1.6, .75, .5)), material='oscuro', alto=.3, brillo=.4, vientre=0,
               hondo=0, linea=.3)
    l.masa(ovalo(cx, ry, 13.3, 1.8), material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.45)          # el borde
    l.mancha(ovalo(cx, ry + .1, 12, 1.25), '6FA497', 1)                 # lo que hierve adentro
    for dx, y, r in ((-6, 23.8, .7), (-1.4, 23.6, .9), (3, 24.1, .6), (6.6, 23.8, .8), (-9.6, 24, .5), (1, 22.4, .45), (-4, 21.4, .35)):
        burbuja(l, cx + dx, y, r)
    for k, dx in enumerate((-5.6, 0, 5.6)):                              # el vapor, que sube en eses
        pts = [(cx + dx + 1.1 * math.sin(t * 1.25 + k * 1.7), 21.2 - t * 1.75) for t in range(9)]
        l.trazo(pts, [.3, .7, .9, .9, .8, .7, .5, .35, .15], color='8BD0B9', alfa=.9)
        l.trazo(pts, [.1, .4, .55, .55, .5, .4, .3, .2, .05], color='FFFFFF', alfa=1)
    for dx, h, s_ in ((-5.6, 4.4, 1), (-.4, 5, -1), (5, 4.2, 1)):        # las llamas de abajo, que lamen el fondo del caldero
        f = l.masa(llama(cx + dx, 37, 3.2, h, s_), material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3, contraluz=.3)
        l.mancha(llama(cx + dx, 36.8, 1.6, h * .6, s_), 'FBEFCB', .95, dentro=f)
    # adelante, el lienzo de muralla blanca con sus almenas y dos torres: el caldero hierve dentro del Kremlin
    muralla(l, 35.4, 41.5, (10, 110), 28.4, 6, 5.4)


# ------------------------------------------------------------------------------------------------ Samara
def samara(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 44, 2.4, 12, .5)
    nube(l, 98, 2, 10, .45)
    t = prado(l, 5.6, 41, .2)
    l.mancha(box(-2, 5.6, 122, 9.4), 'D2F2DA', .5, dentro=t, difuso=1)
    # los campos, vistos desde arriba: parcelas en filas, más chicas lejos
    colores = ['9ED6BE', 'C9DDB0', 'B8E0C8', 'D8D9A6', '8BD0B9']
    y, fila = 6.2, 0
    while y < 41:
        h = .9 + fila * .5
        x = -2 - rng.uniform(0, 3)
        while x < 122:
            w = (4 + fila * 1.6) * rng.uniform(.8, 1.4)
            l.mancha(Polygon([(x, y), (x + w, y), (x + w + .3, y + h), (x + .3, y + h)]), str(rng.choice(colores)), rng.uniform(.45, .8),
                     dentro=t)
            x += w + .16
        y += h + .14
        fila += 1
    # las montañas de Zhiguli: una sierra boscosa, con crestas y valles, que llena la curva y sale por la boca del anzuelo hasta el
    # horizonte (en lomas sueltas y redondas, adentro de la curva, parecían la carga de un bote)
    for x0, x1, base, picos, material in ((30, 92, 16, ((36, 11.4), (44, 8.2), (51, 11), (59, 7.4), (67, 10.6), (76, 8.6), (85, 12)), 'vientre'),
                                         (26, 78, 25.4, ((31, 19.6), (38, 15.4), (45, 18.8), (52, 14.2), (60, 18), (68, 15.8), (74, 20)), 'cuerpo'),
                                         (30, 66, 34, ((35, 28.6), (42, 24.2), (49, 27.4), (55, 23.6), (61, 27.8)), 'lejos')):
        g = Polygon([(x0, base)] + list(picos) + [(x1, base)]).buffer(.6).buffer(-.6)
        mz = l.masa(g, material=material, alto=.4, brillo=.1, vientre=0, hondo=.1, linea=.3, escalon=.25, contraluz=.35)
        xs_, ys_ = rng.uniform(x0, x1, 260), rng.uniform(base - 10, base, 260)
        dentro_ = shapely.contains_xy(g.buffer(-.5), xs_, ys_)
        for px, py in zip(xs_[dentro_], ys_[dentro_]):                   # las copas del bosque
            l.mancha(ovalo(px, py, .55, .42), str(rng.choice(['1C6659', '246E61', '4EB196'])), .6, dentro=mz)
        l.trazo(list(picos), .14, color='D2F2DA', alfa=.7, dentro=mz)    # la línea de las crestas
    # el río, en forma de anzuelo: la caña que baja, la curva abajo y la punta que sube, con su barba
    eje = [(22, 6.6), (22.3, 13), (22.6, 20), (23.6, 27), (28.6, 33.4), (38, 37.4), (50, 37.6), (60, 34.4), (66, 28.6), (68, 22.4),
           (67.8, 17.4)]
    anchos = [2.2, 2.8, 3.4, 4.4, 5.2, 5.8, 5.8, 5.4, 4.6, 3.2, .3]
    barba = Polygon([(66.9, 19), (62.2, 24.4), (66.6, 22.8)]).buffer(.2)
    agua(l, cinta(eje, anchos, 12).union(barba), ondas=14, semilla=5, linea=.35)
    # la ciudad, del otro lado de la curva: casitas con sus techos
    paredes, techos = [], []
    for f, yy in enumerate((22.4, 25, 27.8, 30.8, 34)):
        for k in range(4 + f):
            x = 88.6 + k * 2.7 + (f % 2) * 1.3 + rng.uniform(-.3, .3)
            e = .8 + f * .12
            paredes.append(box(x - .9 * e, yy - 1.1 * e, x + .9 * e, yy))
            techos.append(Polygon([(x - 1.1 * e, yy - 1.1 * e), (x, yy - 2 * e), (x + 1.1 * e, yy - 1.1 * e)]))
    l.masa(paredes, material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    l.masa(techos, material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2, arroja=False)
    # el sedal dorado que baja del cielo hasta el ojo del anzuelo, también dorado
    l.trazo([(20.6, -1), (21.8, 3)], .3, color='93701A', alfa=1)
    l.trazo([(20.6, -1), (21.8, 3)], .16, color='F2D48A', alfa=1)
    l.masa(ovalo(22, 4.4, 1.9, 1.6).difference(ovalo(22, 4.4, .9, .7)), material='acento', alto=.3, brillo=.4, vientre=0, hondo=0,
           linea=.3)


# ------------------------------------------------------------------------------------------------ Volgogrado
def madre_patria(l, x, base, s=1.0):
    """la Madre Patria, de perfil, mirando a la izquierda: da un paso adelante, llama con la mano izquierda extendida hacia adelante y
    alza la espada con la derecha, hacia arriba y atrás; el vestido y el manto vuelan detrás"""
    X = lambda u: x + u * s
    Y = lambda v: base + v * s
    P = lambda pts: [(X(u), Y(v)) for u, v in pts]
    pies = [ovalo(X(-4.7), Y(-.45), 1.1 * s, .45 * s), ovalo(X(4.8), Y(-.5), 1 * s, .45 * s, -20)]
    piernas = [tubo(P([(-.6, -9), (-2.8, -5), (-4.3, -.8)]), [1.2 * s, .9 * s, .6 * s], 6),
               tubo(P([(1, -9), (2.9, -4.8), (4.6, -.8)]), [1.1 * s, .85 * s, .55 * s], 6)]
    vestido = forma(P([(-1.8, -10.6), (-2.7, -7.6), (-3.9, -4), (-4.9, -1.7), (-3.3, -1.9), (-1.3, -3.9), (.6, -4.7), (2.6, -3.7),
                       (4.2, -2.1), (6.4, -2.5), (9, -3.9), (7.4, -5.7), (4.6, -8), (2.2, -10.6)]), 2)
    torso = forma(P([(-1.8, -10.4), (-2.3, -13), (-2.5, -15.2), (-1.6, -16.3), (.6, -16.5), (1.7, -15.4), (1.7, -12.6), (1.9, -10.4)]), 2)
    cabeza = [ovalo(X(-1.3), Y(-17.9), 1.2 * s, 1.35 * s), box(X(-1.6), Y(-17), X(-.4), Y(-16))]
    pelo = forma(P([(-.4, -19), (1.4, -18.9), (3.2, -18), (1.4, -17.3), (-.2, -17.4)]), 2)
    adelante = tubo(P([(-1.8, -15.5), (-5.2, -16.5), (-8.4, -17.7)]), [.75 * s, .65 * s, .55 * s], 8)
    mano = ovalo(X(-9), Y(-17.9), .85 * s, .55 * s, -15)
    arriba = tubo(P([(.8, -15.6), (2.2, -18.8), (3, -21.8)]), [.75 * s, .65 * s, .6 * s], 8)
    manto = cinta(P([(.6, -15.8), (3.8, -16.9), (7.2, -16.2), (10.4, -14.6), (13.6, -13.8)]), [1.2 * s, 1.7 * s, 1.6 * s, 1.2 * s, .5 * s])
    d = np.array([.42, -.91])
    puno = np.array([X(3.1), Y(-22.2)])
    nrm = np.array([-d[1], d[0]])
    punta = puno + d * 11 * s
    espada = [Polygon([tuple(puno - d * .6 * s + nrm * .45 * s), tuple(punta - d * 1.4 * s + nrm * .35 * s), tuple(punta),
                       tuple(punta - d * 1.4 * s - nrm * .35 * s), tuple(puno - d * .6 * s - nrm * .45 * s)]),
              tubo([tuple(puno - nrm * 1.3 * s), tuple(puno + nrm * 1.3 * s)], [.28 * s, .28 * s], 4)]
    l.masa(manto, material='claro', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
    e = l.masa(espada, material='claro', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.trazo([tuple(puno + d * .8 * s), tuple(punta - d * 1.2 * s)], .12 * s, color='8EB5AA', alfa=.8, dentro=e)
    partes = pies + piernas + [vestido, torso, pelo, adelante, mano, arriba] + cabeza
    f = l.masa(partes, material='claro', alto=.45, brillo=.2, vientre=0, hondo=.1, linea=.45, escalon=.25, contraluz=.35,
               bultos=[(ovalo(X(-.2), Y(-13.4), 2 * s, 2.6 * s), .2)])
    for k in range(3):                                                   # los pliegues del vestido, que vuela hacia atrás
        l.trazo(P([(.4 + k * .9, -9.4), (2.2 + k * 1.3, -6.4), (4.4 + k * 1.6, -3.6)]), [.06, .2 * s, .08], color='8EB5AA', alfa=.8, dentro=f)
    l.trazo(P([(-1.6, -9.4), (-2.6, -5.6), (-3.8, -2.4)]), [.06, .18 * s, .06], color='8EB5AA', alfa=.7, dentro=f)    # la pierna de adelante
    l.trazo(P([(.2, -8.6), (.5, -6.4), (.6, -4.8)]), [.06, .16 * s, .06], color='8EB5AA', alfa=.7, dentro=f)
    l.trazo(P([(-2.1, -12.4), (-.4, -12.8), (1.2, -12)]), [.06, .14 * s, .06], color='8EB5AA', alfa=.7, dentro=f)     # el cinturón
    return unary_union(partes + espada + [manto])


def volgogrado(l):
    cielo(l, sol=None)
    nube(l, 92, 6, 14, .6)
    nube(l, 22, 4.6, 10, .45)
    # la otra orilla, baja, y el Volga ancho detrás de la colina
    prado(l, 21.6, 24.2)
    for x in np.arange(-1, 121, 3.4):
        l.masa(ovalo(x, 21.8, 1.8, 1.2), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.22, arroja=False)
    rio(l, 24)
    # la colina de Mamáyev Kurgán, con el pedestal y la estatua
    c = orilla(l, forma([(-2, 41.5), (-2, 39.6), (14, 38), (30, 36), (46, 34.2), (60, 33.8), (74, 34.2), (90, 36.4), (106, 38.6),
                         (122, 39.6), (122, 41.5)], 3))
    pasto(l, 0, 120, 36, 40.8, 24, semilla=13, dentro=c)
    l.masa(box(55.4, 32.4, 64.6, 34.6).buffer(.1), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    madre_patria(l, 60, 32.6, 1.0)


# ------------------------------------------------------------------------------------------------ Astracán
def juncal(l, bases, horizonte, semilla=0):
    """un juncal que se aleja: tallos que nacen de `bases`, más chicos cuanto más lejos, con algunas espadañas"""
    rng = np.random.default_rng(semilla)
    tallos, cabezas = [], []
    for x, y in bases:
        e = .18 + (y - horizonte) / (41 - horizonte)
        h = 4.6 * e * rng.uniform(.6, 1.1)
        a = rng.uniform(-.7, .7) * e
        tallos.append(tubo([(x, y), (x + a * .4, y - h * .6), (x + a, y - h)], [.2 * e + .04, .15 * e + .03, .03], 4))
        if rng.random() < .22 and e > .35:
            cabezas.append(ovalo(x + a * .72, y - h * .74, .3 * e + .05, .9 * e, -a * 12))
    l.masa(tallos, material='cuerpo', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.16, arroja=False)
    if cabezas:
        l.masa(cabezas, material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.18, arroja=False)


def gorro(l, x, base, w=10.0, h=7.6, giro=-8.0, semilla=0):
    """un gorro de astracán, puesto en la punta de un palo: alto y redondo, de piel gris de rizos apretados, con la copa de paño y su
    cruz de galón dorado; (x, base) es el medio de su borde de abajo, y el gorro va inclinado `giro` grados"""
    rng = np.random.default_rng(semilla)
    R = lambda g: affinity.rotate(g, giro, origin=(x, base))
    rp = lambda pts: [R(Point(p)).coords[0] for p in pts]
    cuerpo = [forma([(x - w / 2 + .4, base), (x - w / 2 - .1, base - h * .55), (x - w / 2, base - h), (x + w / 2, base - h),
                     (x + w / 2 + .1, base - h * .55), (x + w / 2 - .4, base)], 1), ovalo(x, base, w / 2 - .4, 1.2)]
    for t in np.linspace(0, 1, 13):                                      # el borde rizado de los costados
        for sx in (-1, 1):
            cuerpo.append(ovalo(x + sx * (w / 2 - .4 + .35 * t), base - h * t, .55, .5))
    for a in np.linspace(0, 2 * math.pi, 22)[:-1]:                       # y el de arriba, alrededor de la copa
        cuerpo.append(ovalo(x + w / 2 * math.cos(a), base - h + 1.5 * math.sin(a), .55, .5))
    g = l.masa(R(unary_union(cuerpo)), material='claro', alto=.6, brillo=.25, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    l.mancha(R(unary_union(cuerpo)), '8EB5AA', .55, dentro=g)
    for _ in range(300):                                                 # los rizos apretados
        cx, cy = rng.uniform(x - w / 2 - .4, x + w / 2 + .4), rng.uniform(base - h - 1, base + 1.2)
        a0, r = rng.uniform(0, 2 * math.pi), rng.uniform(.22, .34)
        pts = [(cx + r * math.cos(a0 + t), cy + r * .85 * math.sin(a0 + t)) for t in np.linspace(0, 5, 8)]
        l.trazo(rp(pts), .12, color=str(rng.choice(['3E7A6D', '3E7A6D', 'F0F6F4'])), alfa=.9, dentro=g)
    c = l.masa(R(ovalo(x, base - h + .2, w / 2 - .7, 1.05)), material='lejos', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.trazo(rp([(x - w / 2 + 1.2, base - h + .2), (x + w / 2 - 1.2, base - h + .2)]), .3, color='E8B952', alfa=.95, dentro=c)
    l.trazo(rp([(x - .7, base - h + 1.1), (x + .7, base - h - .7)]), .3, color='E8B952', alfa=.95, dentro=c)


def esturion(x, y, s=1.0):
    """la silueta de un esturión, mirando a la izquierda: el hocico en punta, el lomo largo y la cola de lóbulo largo arriba"""
    X = lambda u: x + u * s
    Y = lambda v: y + v * s
    cuerpo = forma([(X(-4.8), Y(.3)), (X(-3.4), Y(-.5)), (X(-1), Y(-.9)), (X(1.6), Y(-.8)), (X(3.2), Y(-.4)), (X(3.4), Y(.4)),
                    (X(1.4), Y(.8)), (X(-1.4), Y(.9)), (X(-3.6), Y(.7))], 2)
    cola = Polygon([(X(3), Y(-.3)), (X(5.2), Y(-2)), (X(4.5), Y(.2)), (X(4.9), Y(1.1)), (X(3.2), Y(.45))])
    aletas = [Polygon([(X(-2.4), Y(.7)), (X(-1.6), Y(1.8)), (X(-1.2), Y(.8))]), Polygon([(X(1), Y(.7)), (X(1.8), Y(1.6)), (X(2), Y(.6))]),
              Polygon([(X(.4), Y(-.8)), (X(1.4), Y(-1.7)), (X(1.8), Y(-.7))])]
    return unary_union([cuerpo, cola] + aletas).buffer(.02)


def tapa_caviar(l, x, y, s=1.0, giro=-8):
    """la tapa de la lata de caviar, azul, con su aro y su esturión dorados; (x, y) es su centro"""
    tp = l.masa(ovalo(x, y, 4.8 * s, 5.2 * s, giro), material='lejos', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
    t = np.linspace(0, 2 * math.pi, 40)
    l.trazo([(x + 4.1 * s * math.cos(a), y + 4.5 * s * math.sin(a)) for a in t], .22 * s, color='E8B952', alfa=.9, dentro=tp)
    l.mancha(affinity.rotate(esturion(x, y, .78 * s), giro, origin=(x, y)), 'E8B952', 1, dentro=tp)


def mercader(l, x, y, semilla=0):
    """un mercader de Astracán, de frente y de la cintura para arriba: el caftán oscuro, la barba gris, el gorro de astracán, alto y
    rizado, y en las manos la lata de caviar abierta; (x, y) es el medio de la cara"""
    PIEL_ = '93701A'
    caftan = forma([(x - 6.4, y + 4.6), (x - 9.4, y + 11), (x - 10.6, y + 23), (x + 10.6, y + 23), (x + 9.4, y + 11), (x + 6.4, y + 4.6),
                    (x + 2.6, y + 3.6), (x - 2.6, y + 3.6)], 2)
    brazos = [tubo([(x + sx * 7, y + 5.8), (x + sx * 10.4, y + 9.6), (x + sx * 9.2, y + 12.6)], [1.7, 1.5, 1.3], 8) for sx in (-1, 1)]
    c = l.masa([caftan] + brazos, material='lejos', alto=.4, brillo=.15, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.3)
    l.trazo([(x, y + 4), (x + .3, y + 23)], .16, color='05201C', alfa=.7, dentro=c)          # el cruce del caftán
    for k in range(4):                                                   # sus botones
        l.mancha(ovalo(x + 1.2, y + 6 + k * 2.2, .3, .3), '0C3A33', .9, dentro=c)
    # la cabeza, con la barba gris y los bigotes
    h = l.masa([ovalo(x, y, 3.1, 3.5), ovalo(x - 3, y + .2, .6, .9), ovalo(x + 3, y + .2, .6, .9)], material='vientre', alto=.45, brillo=.15,
               vientre=0, hondo=0, linea=.4, contraluz=.25)
    l.mancha(box(x - 4, y - 4, x + 4, y + 4), PIEL_, .45, dentro=h)
    for dx in (-1.2, 1.2):
        l.mancha(ovalo(x + dx, y - .7, .3, .32), '05201C', 1, dentro=h)        # los ojos
        l.trazo([(x + dx - .6, y - 1.6), (x + dx + .6, y - 1.7)], .2, color='3E7A6D', alfa=.9, dentro=h)    # las cejas
    l.trazo([(x, y - .6), (x - .3, y + .6), (x + .3, y + .8)], .14, color='6B4E10', alfa=.8, dentro=h)
    barba = forma([(x - 3, y + .8), (x - 3.4, y + 3.4), (x - 2.2, y + 6.4), (x, y + 7.6), (x + 2.2, y + 6.4), (x + 3.4, y + 3.4), (x + 3, y + .8),
                   (x + 1.6, y + 1.8), (x, y + 2.2), (x - 1.6, y + 1.8)], 2)
    b = l.masa(barba, material='claro', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(barba, '8EB5AA', .45, dentro=b)
    rng = np.random.default_rng(semilla)
    for _ in range(14):                                                  # los pelos de la barba
        u = rng.uniform(-2.6, 2.6)
        l.trazo([(x + u, y + 2.2), (x + u * .8, y + 6)], .08, color='6FA497', alfa=.8, dentro=b)
    l.masa(forma([(x - 2.8, y + 1.6), (x - 1.4, y + 1), (x, y + 1.4), (x + 1.4, y + 1), (x + 2.8, y + 1.6), (x + 1.2, y + 2), (x, y + 1.8),
                  (x - 1.2, y + 2)], 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)     # los bigotes
    # el gorro de astracán, en la cabeza
    gorro(l, x, y - 2.2, 8.6, 7.6, 0, semilla=semilla + 1)
    # la lata de caviar abierta, en las manos
    lata_caviar(l, x, y + 14.6, 1.05, semilla=semilla + 2, tapa=False)
    for sx in (-1, 1):
        m_ = l.masa(ovalo(x + sx * 8.8, y + 12.8, 1.4, 1.1), material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35)
        l.mancha(ovalo(x + sx * 8.8, y + 12.8, 1.6, 1.3), PIEL_, .45, dentro=m_)


def lata_caviar(l, x, base, s=1.0, semilla=0, tapa=True):
    """una lata de caviar abierta, llena de huevas negras que brillan, y su tapa azul con el esturión dorado, apoyada detrás"""
    rng = np.random.default_rng(semilla)
    O = lambda u, v, rx, ry, ang=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, ang)
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    if tapa:
        tapa_caviar(l, x + 11 * s, base - 5.4 * s, s)
    lado = Polygon(P([(-8, -2.6), (8, -2.6), (8, -.6), (-8, -.6)])).union(O(0, -.6, 8, 2.2))
    lt = l.masa(lado, material='lejos', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.trazo(P([(-8, -1.6), (-4, -.1), (0, .3), (4, -.1), (8, -1.6)]), .2 * s, color='E8B952', alfa=.8, dentro=lt)
    borde = l.masa(O(0, -2.6, 8, 2.3), material='claro', alto=.25, brillo=.4, vientre=0, hondo=0, linea=.35)
    l.mancha(O(0, -2.5, 7.2, 1.8), '05201C', 1, dentro=borde)
    for _ in range(int(150 * s)):
        a, rr = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1))
        u, v = 6.8 * rr * math.cos(a), -2.5 + 1.6 * rr * math.sin(a)
        l.mancha(O(u, v, .34, .27), '1E4A42', .9)
        l.mancha(O(u - .1, v - .1, .11, .09), 'D2F2DA', .9)


def astracan(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .5)
    horizonte = 15.4
    prado(l, horizonte, 41, .3)
    # lejos, en el horizonte, el Kremlin blanco con las cúpulas de su catedral
    l.masa(box(84, 12.6, 108, 15.8).buffer(.1), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    iglesia(l, 96, 12.8, 7, 4, cupulas=((0, .7), (-2.3, .42), (2.3, .42)), dorada=None, ventanas=2)
    # el delta: el río que se deshace en brazos, más y más anchos a medida que se acercan
    ramas = [([(58, 15.6), (57.4, 17.4), (56.6, 19.2)], [.9, 1.2, 1.5]),
             ([(56.6, 19), (50, 21.6), (41, 25.6)], [1.4, 1.9, 2.4]),
             ([(56.6, 19), (64, 21.6), (73, 25.6)], [1.4, 1.9, 2.4]),
             ([(41, 25.4), (28, 29.6), (14, 34), (-2, 37.6)], [2.2, 2.8, 3.4, 4]),
             ([(41, 25.4), (40, 31), (37, 41.5)], [2, 2.8, 4]),
             ([(73, 25.4), (80, 32), (86, 41.5)], [2, 2.8, 4.2]),
             ([(73, 25.4), (92, 29), (122, 32.4)], [2.2, 2.8, 3.6]),
             ([(92, 29), (100, 35), (106, 41.5)], [1.6, 2.4, 3.4]),
             ([(20, 32), (18, 37), (16, 41.5)], [1.4, 2.2, 3]),
             ([(58, 15.6), (40, 16.6), (18, 17.8), (-2, 19.2)], [.6, .8, 1, 1.2]),
             ([(58.4, 15.8), (80, 16.8), (104, 18), (122, 19)], [.6, .8, 1, 1.2])]
    canales = unary_union([cinta(p, a, 8) for p, a in ramas])
    agua(l, canales, ondas=0, linea=.22)
    xs, ys = rng.uniform(-2, 122, 900), horizonte + (41 - horizonte) * rng.uniform(0, 1, 900) ** 1.3
    libre = ~shapely.contains_xy(canales.buffer(.4), xs, ys)
    juncal(l, sorted(zip(xs[libre], ys[libre]), key=lambda p: p[1]), horizonte, semilla=8)
    # el muelle, adelante, con los dos protagonistas, grandes: un mercader con su gorro de astracán, que muestra la lata de caviar
    # abierta (el gorro solo, en un poste, parecía un letrero), y la tapa con el esturión
    mu = l.masa(Polygon([(12, 30.4), (108, 30.4), (114, 41.5), (6, 41.5)]).buffer(.1), material='vientre', alto=.12, brillo=.1, vientre=0,
                hondo=0, linea=.4)
    l.mancha(box(4, 30, 116, 42), 'E8B952', .25, dentro=mu)
    for k in np.linspace(32, 40.6, 6):
        l.trazo([(12 - (k - 30.4) * .55, k), (108 + (k - 30.4) * .55, k)], .1, color='6B4E10', alfa=.5, dentro=mu)
    mercader(l, 58, 18.6, semilla=9)
    tapa_caviar(l, 86, 36.4, 1.15, giro=-14)


# ------------------------------------------------------------------------------------------------ el mar
def lodia(l, x, y, s=1.0):
    """la lodia de los mercaderes del Volga, mirando a la derecha: el casco de tablones, alto en las dos puntas, la vela cuadrada en su
    palo, con su verga, y los remos; (x, y) es la línea del agua bajo el medio. El casco es dorado: es la barca del juego, que llega al
    mar"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([tubo(P([(u, -1.4), (u - 2.6, 1.6)]), [.18 * s, .12 * s], 4) for u in (-5.4, -2.2, 1, 4.2)], material='lejos', alto=.2,
           brillo=.2, vientre=0, hondo=0, linea=.2)                     # los remos
    l.masa([tubo(P([(0, -1.4), (0, -15.4)]), [.32 * s, .24 * s], 6), tubo(P([(-6, -13.8), (6, -13.8)]), [.22 * s, .22 * s], 4)],
           material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    vela = forma(P([(-5.6, -13.6), (5.6, -13.6), (6.2, -8.6), (5.4, -3.6), (-5.4, -3.6), (-6.2, -8.6)]), 1)
    v = l.masa(vela, material='claro', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.4, escalon=.15, contraluz=.3)
    for u in (-3.4, -1.1, 1.1, 3.4):                                     # los paños de la vela
        l.trazo(P([(u, -13.4), (u * 1.08, -8.6), (u, -3.8)]), [.05, .12, .05], color='8EB5AA', alfa=.7, dentro=v)
    casco = forma(P([(-9.6, -3.8), (-8.2, -1.2), (-5.2, .9), (5.2, .9), (8.2, -1.2), (9.8, -4), (8.6, -2.6), (6.2, -1.8), (-6.2, -1.8),
                     (-8.6, -2.6)]), 1)
    c = l.masa(casco, material='acento', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    for v_ in (-.9, .1):                                                 # los tablones
        l.trazo(P([(-8, v_ - 1.2), (-4, v_), (4, v_), (8, v_ - 1.2)]), [.05, .12, .12, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco.union(vela)


def mar(l):
    cielo(l, sol=None)
    nube(l, 30, 8, 16, .55)
    nube(l, 96, 6, 12, .45)
    horizonte = 22.4
    m = l.masa(box(-2, horizonte, 122, 41), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 3), '64C8AA', .55, dentro=m, difuso=.8)
    rng = np.random.default_rng(8)
    for _ in range(22):
        x, y = rng.uniform(2, 116), rng.uniform(horizonte + 2, 39)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # las aves que vuelan sobre el delta
    for x, y, s in ((22, 12, 1.2), (28, 10.4, .9), (34, 13, 1), (86, 8.6, .8), (92, 10, .7), (40, 6.6, .7)):
        ave(l, x, y, s)
    # los últimos juncales del delta, a los costados, que salen del agua, y los lotos en flor
    for x0, x1, y, h, n in ((-2, 24, 31, 6, 46), (96, 122, 32, 6, 46), (-2, 16, 39.4, 7, 34), (104, 122, 40, 7, 34)):
        l.mancha(Polygon([(x0, y - .6), (x1, y - .6), (x1 - 2, y + 1.6), (x0, y + 1.6)]), '0C3A33', .25, difuso=.6)
        juncos(l, x0, x1, y, h, n, semilla=int(x0 + y))
    for x, y, s in ((26, 36.6, 1.2), (36, 39.2, 1.3), (84, 38.8, 1.3), (94, 36.4, 1.1)):
        loto(l, x, y, s)
    # la lodia, la barca del juego, que sale al Caspio
    g = lodia(l, 60, 33.6, 1.3)
    reflejo(l, g, 33.8, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Tver', dibujar=tver), dict(clave='Yaroslavl', dibujar=yaroslavl),
            dict(clave='Nizhni Nóvgorod', dibujar=nizhni), dict(clave='Kazán', dibujar=kazan), dict(clave='Samara', dibujar=samara),
            dict(clave='Volgogrado', dibujar=volgogrado), dict(clave='Astracán', dibujar=astracan), dict(clave='mar', dibujar=mar)]
LISTO = True
