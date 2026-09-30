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
- Astracán: un gorro de astracán, de piel de rizos apretados, y una lata de caviar abierta, con su esturión en la tapa, en un muelle
  del delta, donde el río se deshace en brazos entre juncales; lejos, las cúpulas del Kremlin;
- el mar: el delta que se abre al Caspio, un mar cerrado: juncos, lotos en flor, aves y un barco pesquero.
"""
import math

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

from _postal import VISTA, abedul, abeto, ave, cebolla, cielo, iglesia, juncos, loto, nube, rio, tierra  # noqa: F401
from pintor import curva, forma, ovalo, tubo


def cinta(pts, anchos, n=10):
    """una cinta de ancho variable a lo largo de una curva (un río que serpentea, un brazo del delta)"""
    c = curva(pts, n)
    a = np.interp(np.linspace(0, 1, len(c)), np.linspace(0, 1, len(anchos)), anchos)
    izq, der = [], []
    for i in range(len(c)):
        d = c[min(i + 1, len(c) - 1)] - c[max(i - 1, 0)]
        d = d / (np.hypot(*d) or 1)
        nrm = np.array([-d[1], d[0]])
        izq.append(c[i] + nrm * a[i] / 2)
        der.append(c[i] - nrm * a[i] / 2)
    return Polygon(izq + der[::-1]).buffer(0)


def prado(l, suelo, hasta=41.0, tinte=.24):
    """la tierra verde del Volga: un prado, más amarillo que el agua para que no se confundan"""
    return tierra(l, suelo, hasta, desierto=tinte)


def orilla(l, g, tinte=.24, linea=.35):
    """una orilla de pasto, del mismo verde amarillo del prado, con su línea"""
    m = l.masa(g, material='vientre', alto=.12, brillo=.04, vientre=0, hondo=0, linea=linea, escalon=.1, contraluz=.2)
    l.mancha(g, 'E8B952', tinte, dentro=m)
    return m


def pasto(l, x0, x1, y0, y1, n, semilla=0, dentro=None):
    """matas de pasto: tres hojitas que salen de un punto, más grandes adelante"""
    rng = np.random.default_rng(semilla)
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = .6 + (y - y0) / max(y1 - y0, 1) * .6
        for dx, h in ((-.7, 1.1), (0, 1.5), (.7, 1.1)):
            l.trazo([(x + dx * s * .4, y), (x + dx * s, y - h * s)], .12 * s + .04, color='2F8A74', alfa=.8, dentro=dentro)


def agua(l, g, material='lejos', brillo='64C8AA', ondas=0, semilla=0, linea=.3):
    """un espejo de agua con su brillo y unas ondas claras"""
    m = l.masa(g, material=material, alto=.05, brillo=0, vientre=0, hondo=0, linea=linea, tinta=linea > 0, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(g, brillo, .6, dentro=m, difuso=.6)
    rng = np.random.default_rng(semilla)
    x0, y0, x1, y1 = g.bounds
    for _ in range(ondas):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        l.trazo([(x, y), (x + 2, y - .2), (x + 4, y)], .16, color='D2F2DA', alfa=.8, dentro=m)
    return m


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
    cielo(l, sol=(102, 7))
    nube(l, 30, 6, 16, .7)
    nube(l, 72, 4.4, 11, .55)
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
    for x, y, rx, ry in ((18, 27, 7, 1.1), (36, 31.6, 9, 1.4), (84, 28.4, 8, 1.2), (102, 33.4, 10, 1.6), (14, 36.6, 8, 1.5),
                         (46, 25.4, 5, .8)):
        agua(l, ovalo(x, y, rx, ry), ondas=1, semilla=int(x), linea=.2)
    pasto(l, 0, 120, 24, 40, 30, semilla=3)
    # el manantial, bajo la capillita, y el Volga que sale de él como un arroyito, hacia nosotros
    agua(l, ovalo(62, 25.8, 5.4, 1.2), ondas=1, linea=.2)
    agua(l, cinta([(61, 26.4), (57.6, 29.4), (62.4, 32.6), (57, 36.4), (60, 41.4)], [.8, 1.3, 2, 2.8, 3.8]), ondas=3, semilla=4, linea=.25)
    # la pasarela de tablas y la capillita de madera sobre pilotes, con su cúpula
    for x in np.arange(40, 62, 3):
        l.masa(box(x - .2, 25, x + .2, 27), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
    p = l.masa(box(38, 24.2, 60.4, 25.2), material='acento', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    for x in np.arange(39, 60, 1.4):
        l.trazo([(x, 24.3), (x, 25.1)], .08, color='6B4E10', alfa=.6, dentro=p)
    for x in (59.6, 64.4):
        l.masa(box(x - .25, 22.4, x + .25, 27), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    cap = l.masa(box(58.6, 17.2, 65.4, 23.4).buffer(.1), material='vientre', alto=.25, brillo=.05, vientre=0, hondo=0, linea=.35)
    l.mancha(box(58, 16, 66, 24), 'E8B952', .35, dentro=cap)
    for k in np.arange(17.9, 23.4, .75):
        l.trazo([(58.6, k), (65.4, k)], .07, color='6B4E10', alfa=.5, dentro=cap)
    l.mancha(forma([(61.1, 23.4), (61.1, 20), (62, 19.2), (62.9, 20), (62.9, 23.4)], 1), '164F46', .85, dentro=cap)
    l.masa(Polygon([(57.4, 17.4), (62, 13.4), (66.6, 17.4)]).buffer(.1), material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0,
           linea=.35)
    l.masa(box(61.2, 11.6, 62.8, 13.8), material='vientre', alto=.2, brillo=.05, vientre=0, hondo=0, linea=.3)
    l.masa(cebolla(62, 11.6, 1.2), material='cuerpo', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.3, contraluz=.3)
    l.trazo([(62, 7.9), (62, 6.2)], .16, alfa=.9)
    l.trazo([(61.4, 6.9), (62.6, 6.9)], .14, alfa=.9)
    for x, y, h in ((6, 30, 10), (12, 28.4, 8.4), (96, 29, 9), (110, 31, 11), (116, 27.6, 8)):
        abedul(l, x, y, h, 2.2, semilla=int(x))
    juncos(l, 70, 92, 33.6, 4.4, 30, semilla=5)
    juncos(l, 22, 40, 39.6, 5, 30, semilla=6)


# ------------------------------------------------------------------------------------------------ Tver
def tver(l):
    cielo(l, sol=(104, 7))
    nube(l, 26, 7, 14, .6)
    prado(l, 16.4, 41)
    # el río angosto, que viene de lejos hacia nosotros y se ensancha
    lecho = Polygon([(58, 17), (62, 17), (87, 41.5), (33, 41.5)])
    agua(l, lecho, linea=.3)
    for k in range(9):                                                # las ondas, más grandes adelante
        y = 25 + k * 1.8
        s = (y - 17) / 24
        for dx in (-.3, .2):
            x = 60 + dx * (4 + s * 50) + (k % 2) * 3 * s
            l.trazo([(x - 2.4 * s, y), (x, y - .25 * s), (x + 2.4 * s, y)], .1 + .12 * s, color='D2F2DA', alfa=.8)
    # la línea de árboles lejos, que tapa de dónde viene el río
    for x in np.arange(-1, 121, 3.2):
        l.masa(ovalo(x, 16.2, 1.9, 1.3), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.22, arroja=False)
    # la orilla izquierda, con sus casas de madera; la derecha, con la iglesia y los abedules
    for x, b, w in ((7, 22.6, 6), (16, 22.2, 7), (26, 22.8, 6), (35.4, 23, 5.4)):
        casa_madera(l, x, b, w, 4.2)
    iglesia(l, 95, 23, 13, 7.4, cupulas=((0, 1.15), (-4.4, .7), (4.4, .7)), dorada=0)
    for x, h in ((81, 8.6), (110, 9.4), (116, 7.6)):
        abedul(l, x, 23.4, h, 2, semilla=int(x))
    # el puente corto, de piedra y de un solo arco, que cruza el río de orilla a orilla
    agua_y, x0, x1, yt = 23.2, 43, 77, 17.4
    arco = ovalo(60, agua_y, 8.8, 4.6)
    pte = box(x0, yt, x1, agua_y + .8).difference(arco).difference(box(51.2, agua_y, 68.8, agua_y + 2))
    l.mancha(arco.intersection(box(50, agua_y - 1.8, 70, agua_y)), '0C3A33', .35)          # la sombra bajo el arco
    espejo = affinity.scale(pte, 1, -1, origin=(0, agua_y)).intersection(lecho)
    for k in np.arange(agua_y + .2, 31, .8):                            # su reflejo, que cierra el ojo del arco
        l.mancha(espejo.intersection(box(-2, k, 122, k + .45)), 'D2F2DA', .55 * max(0, 1 - (k - agua_y) / 7.5))
    p = l.masa(pte, material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.3)
    l.mancha(box(x0, yt, x1, yt + 1), 'CFE0DA', .8, dentro=p)
    for a in range(15, 170, 15):                                        # las dovelas del arco
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        l.trazo([(60 + 8.8 * c, agua_y - 4.6 * s), (60 + 10.4 * c, agua_y - 6 * s)], .1, color='8EB5AA', alfa=.9, dentro=p)
    for x in np.arange(x0 + .8, x1, 1.7):                               # la baranda
        l.trazo([(x, yt - 1), (x, yt)], .14, alfa=.8)
    l.trazo([(x0 - .2, yt - 1.1), (x1 + .2, yt - 1.1)], .22, alfa=.9)
    # las orillas de adelante, con pasto y juncos
    for x, s in ((6, 1), (114, -1)):
        orilla(l, forma([(x - 12 * s, 41.5), (x - 12 * s, 31), (x, 31.6), (x + 16 * s, 34.4), (x + 26 * s, 41.5)], 2))
    juncos(l, 20, 32, 40.8, 4.4, 20, semilla=7)
    juncos(l, 88, 100, 40.8, 4.4, 20, semilla=8)


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
    cielo(l, sol=(104, 7))
    nube(l, 22, 6, 12, .55)
    # la otra orilla, con las iglesias de la ciudad
    prado(l, 21.6, 26)
    for x in np.arange(-1, 121, 3.2):
        if 6 < x < 26 or 90 < x < 114:
            continue
        l.masa(ovalo(x, 22.2, 2, 1.5), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.25, arroja=False)
    iglesia(l, 16, 23, 12, 7, cupulas=((0, 1.1), (-4, .65), (4, .65)), dorada=None)
    iglesia(l, 102, 23, 13, 7.6, cupulas=((0, 1.2), (-4.2, .7), (4.2, .7), (-2, .55), (2, .55)), dorada=0)
    # el río, y la orilla de adelante, donde está el oso
    rio(l, 24.6)
    m = orilla(l, forma([(-2, 41.5), (-2, 33.4), (14, 32.2), (34, 31.2), (60, 30.8), (86, 31.4), (106, 32.6), (122, 33.6),
                         (122, 41.5)], 2))
    pasto(l, 0, 120, 33, 40.6, 34, semilla=11, dentro=m)
    oso(l, 58, 38.8)


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


def tienda(l, x, base, w=9.0, h=5.6):
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
    l.masa(Polygon([(x, base - h - 1.6), (x + 1.4, base - h - 1.2), (x, base - h - .8)]), material='acento', alto=.2, brillo=.2,
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


def balanza(l, x, base, alto_=20.0, brazo=11.0):
    """la gran balanza de la feria: a la izquierda, un platillo colgado de cadenas; a la derecha, un gancho; da dónde asienta el
    platillo y dónde está el gancho"""
    tope = base - alto_
    l.masa([box(x - .45, tope, x + .45, base - .8), forma([(x - 3.6, base), (x - 2.4, base - 1.4), (x + 2.4, base - 1.4), (x + 3.6, base)], 1)],
           material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.35, contraluz=.3)
    xp, yp = x - brazo + .4, tope + 7
    for dx in (-2.8, 2.8):
        l.trazo([(xp, tope + .3), (xp + dx, yp)], .1, alfa=.85)
    xg, yg = x + brazo - .4, tope + 3.4
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
    cielo(l, sol=(16, 6.6))
    nube(l, 44, 5, 12, .5)
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
    l.mancha(box(40, 0, 122, 31), 'E8B952', .28, dentro=m)
    for (x, y), h in zip(muro_pts[:-1], (8, 8.6, 9.6, 8.4, 9)):
        torre_kremlin(l, x, y + .4, 3.6, h)
    # la lengua de tierra, adelante, con la feria
    s = orilla(l, forma([(-2, 41.5), (-2, 30), (20, 29.6), (44, 30.2), (70, 31.8), (92, 34), (102, 35.8), (92, 37.2), (72, 39), (56, 41.5)],
                        2))
    pasto(l, 0, 96, 32, 40, 18, semilla=12, dentro=s)
    tienda(l, 7, 33.4, 10, 6)
    tienda(l, 66, 35, 9, 5.6)
    for x, b in ((14.6, 38.4), (20.4, 38.4), (17.5, 34.2)):             # los cajones de té, apilados
        caja_te(l, x, b)
    # el puesto de pieles: dos palos, una vara y las pieles colgadas
    l.masa([box(75.2, 30.6, 76, 38.6), box(90, 31.6, 90.8, 39.2), tubo([(74.6, 31.2), (91.4, 32.2)], [.3, .3], 4)], material='lejos',
           alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    pieles(l, [(78 + k * 3, 31.6 + k * .18, (-1) ** k * 4) for k in range(5)], 4.2, semilla=13)
    # la balanza gigante: un cajón de té contra un atado de pieles
    (xa, ya), (xg, yg) = balanza(l, 42, 38.8, 20, 11.4)
    caja_te(l, xa, ya, 5.8, 4.4)
    pieles(l, [(xg - 1.7, yg + .2, 14), (xg, yg + .5, 0), (xg + 1.7, yg + .2, -14)], 5.4, semilla=15)
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
    cielo(l, sol=(110, 6.4))
    prado(l, 20, 41)
    # el fondo del Kremlin: el lienzo de muralla de atrás, lejos
    muralla(l, 18.8, 21.4, (4, 118), 15.6, 4, 3.6, linea=.3)
    # la mezquita Kul Sharif: el cuerpo blanco con sus arcos, la cúpula turquesa y los cuatro minaretes
    mx = 40
    minarete(l, mx - 11, 21.4, 15, .75)
    minarete(l, mx + 11, 21.4, 15, .75)
    cuerpo = l.masa(box(mx - 9, 11.4, mx + 9, 22).buffer(.2), material='claro', alto=.3, brillo=.12, vientre=0, hondo=0, linea=.4,
                    escalon=.2, contraluz=.3)
    for x in np.arange(mx - 7, mx + 7, 3):
        l.mancha(forma([(x, 21), (x, 15.4), (x + .9, 14.2), (x + 1.8, 15.4), (x + 1.8, 21)], 1), '164F46', .75, dentro=cuerpo)
    l.masa(forma([(mx - 6, 11.8), (mx - 5.4, 8), (mx - 2.4, 4.6), (mx, 3.6), (mx + 2.4, 4.6), (mx + 5.4, 8), (mx + 6, 11.8)], 2),
           material='cuerpo', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo([(mx, 3.8), (mx, 1.4)], .18, color='93701A', alfa=.9)
    l.mancha(ovalo(mx, 1.6, .5, .5), 'E8B952', 1)
    minarete(l, mx - 13, 25, 17, .9)
    minarete(l, mx + 13, 25, 17, .9)
    # la catedral, de cúpulas de cebolla, en el mismo recinto
    iglesia(l, 102, 24.2, 11, 7, cupulas=((0, 1.05), (-3.6, .62), (3.6, .62), (-1.8, .5), (1.8, .5)), dorada=0)
    # el caldero, grande, hirviendo sobre el fuego en el patio del Kremlin
    cx, ry = 76, 24
    l.mancha(ovalo(cx, 34.6, 15, 3.6), 'F2D48A', .5, difuso=1.4)      # el resplandor del fuego
    for x, y, w, h, s in ((63.6, 36, 3.6, 8.8, -1), (67.4, 36.6, 3.2, 6.8, 1), (84.6, 36.6, 3.2, 6.8, -1), (88.4, 36, 3.6, 8.8, 1)):
        f = l.masa(llama(x, y, w, h, s), material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3, contraluz=.3)
        l.mancha(llama(x, y - .2, w * .5, h * .6, s), 'FBEFCB', .9, dentro=f)
    caldero = forma([(cx - 13, ry), (cx + 13, ry), (cx + 12.4, ry + 3.8), (cx + 9.6, ry + 7.8), (cx + 4, ry + 9.8), (cx - 4, ry + 9.8),
                     (cx - 9.6, ry + 7.8), (cx - 12.4, ry + 3.8)], 3)
    l.masa(caldero, material='oscuro', alto=.6, brillo=.5, vientre=0, hondo=0, linea=.5, contraluz=.4)
    for x in (cx - 13.2, cx + 13.2):                                    # las asas
        l.masa(ovalo(x, ry + 1.6, 1.5, 1.1).difference(ovalo(x, ry + 1.6, .75, .5)), material='oscuro', alto=.3, brillo=.4, vientre=0,
               hondo=0, linea=.3)
    l.masa(ovalo(cx, ry, 13.3, 1.8), material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.45)          # el borde
    l.mancha(ovalo(cx, ry + .1, 12, 1.25), '6FA497', 1)                 # lo que hierve adentro
    for x, y, r in ((70, 23.8, .7), (74.6, 23.6, .9), (79, 24.1, .6), (82.6, 23.8, .8), (66.4, 24, .5), (77, 22.4, .45), (72, 21.4, .35)):
        burbuja(l, x, y, r)
    for k, x0 in enumerate((70.4, 76, 81.6)):                            # el vapor, que sube en eses
        pts = [(x0 + 1.1 * math.sin(t * 1.25 + k * 1.7), 21.2 - t * 1.75) for t in range(9)]
        l.trazo(pts, [.3, .7, .9, .9, .8, .7, .5, .35, .15], color='8BD0B9', alfa=.9)
        l.trazo(pts, [.1, .4, .55, .55, .5, .4, .3, .2, .05], color='FFFFFF', alfa=1)
    for x, h, s in ((70.4, 4.4, 1), (75.6, 5, -1), (81, 4.2, 1)):      # las llamas de abajo, que lamen el fondo del caldero
        f = l.masa(llama(x, 37, 3.2, h, s), material='acento', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3, contraluz=.3)
        l.mancha(llama(x, 36.8, 1.6, h * .6, s), 'FBEFCB', .95, dentro=f)
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
    # las montañas de Zhiguli, cubiertas de bosque, que el río rodea: lomas redondas, de atrás hacia adelante
    for x, yb, w, h in ((34, 17, 20, 7), (52, 16, 22, 8.4), (67, 18.4, 14, 6.4), (29, 24.6, 14, 7), (45, 25, 20, 8.6), (61, 25.4, 18, 7.6),
                        (72, 25, 9, 5.6), (37, 32, 20, 7.4), (55, 32.6, 22, 8), (68, 30.6, 10, 5.4)):
        g = forma([(x - w / 2, yb), (x - w / 3, yb - h * .7), (x - w / 8, yb - h), (x + w / 6, yb - h * .9), (x + w / 2.6, yb - h * .5),
                   (x + w / 2, yb)], 3)
        mz = l.masa(g, material='cuerpo', alto=.5, brillo=.1, vientre=0, hondo=.1, linea=.3, escalon=.2, contraluz=.35)
        xs_, ys_ = rng.uniform(x - w / 2, x + w / 2, 90), rng.uniform(yb - h, yb, 90)
        for px, py in zip(xs_[shapely.contains_xy(g, xs_, ys_)], ys_[shapely.contains_xy(g, xs_, ys_)]):   # las copas del bosque
            l.mancha(ovalo(px, py, .7, .55), str(rng.choice(['1C6659', '246E61', '4EB196'])), .7, dentro=mz)
    # el río, en forma de anzuelo: la caña que baja, la curva abajo y la punta que sube, con su barba
    eje = [(16, 6.4), (16.4, 14), (18, 22.4), (23, 30.4), (33, 35.8), (48, 37.8), (63, 35.6), (74, 29.4), (80, 21), (82, 13.6), (82.2, 8.4)]
    anchos = [1.8, 2.6, 3.8, 4.8, 5.6, 5.8, 5.4, 4.6, 3.6, 2.2, .2]
    barba = Polygon([(80.9, 11), (76.4, 17.2), (80.6, 15.4)]).buffer(.15)
    agua(l, cinta(eje, anchos, 12).union(barba), ondas=14, semilla=5, linea=.35)
    # la ciudad, del otro lado de la curva: casitas con sus techos
    paredes, techos = [], []
    for f, yy in enumerate((22.4, 25, 27.8, 30.8, 34)):
        for k in range(4 + f):
            x = 88.6 + k * 2.7 + (f % 2) * 1.3 + rng.uniform(-.3, .3)
            s = .8 + f * .12
            paredes.append(box(x - .9 * s, yy - 1.1 * s, x + .9 * s, yy))
            techos.append(Polygon([(x - 1.1 * s, yy - 1.1 * s), (x, yy - 2 * s), (x + 1.1 * s, yy - 1.1 * s)]))
    l.masa(paredes, material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    l.masa(techos, material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.2, arroja=False)
    # el sedal que baja del cielo hasta el ojo del anzuelo
    l.trazo([(15.2, -1), (15.8, 4.2)], .16, alfa=.9)
    l.masa(ovalo(16, 5.2, 1.3, 1.1).difference(ovalo(16, 5.2, .65, .5)), material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0,
           linea=.25)


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
    cielo(l, sol=(104, 8))
    nube(l, 80, 6, 14, .6)
    # la otra orilla, baja, y el Volga ancho detrás de la colina
    prado(l, 21.6, 24.2)
    for x in np.arange(-1, 121, 3.4):
        l.masa(ovalo(x, 21.8, 1.8, 1.2), material='lejos', alto=.3, brillo=.05, vientre=0, hondo=0, linea=.22, arroja=False)
    rio(l, 24)
    # la colina de Mamáyev Kurgán, con el pedestal y la estatua
    c = orilla(l, forma([(-2, 41.5), (-2, 39), (10, 37), (24, 35), (36, 34), (52, 34), (64, 35.2), (80, 37.6), (96, 39.4), (122, 40),
                         (122, 41.5)], 3))
    pasto(l, 0, 110, 36, 40.8, 24, semilla=13, dentro=c)
    l.masa(box(39.4, 32.4, 48.6, 34.6).buffer(.1), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    madre_patria(l, 44, 32.6, 1.0)


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


def lata_caviar(l, x, base, semilla=0):
    """una lata de caviar abierta, llena de huevas negras que brillan, y su tapa azul con el esturión dorado, apoyada detrás"""
    rng = np.random.default_rng(semilla)
    tapa = ovalo(x + 11, base - 5.4, 4.8, 5.2, -8)
    tp = l.masa(tapa, material='lejos', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
    t = np.linspace(0, 2 * math.pi, 40)
    l.trazo([(x + 11 + 4.1 * math.cos(a), base - 5.4 + 4.5 * math.sin(a)) for a in t], .22, color='E8B952', alfa=.9, dentro=tp)
    l.mancha(affinity.rotate(esturion(x + 11, base - 5.4, .78), -8, origin=(x + 11, base - 5.4)), 'E8B952', 1, dentro=tp)
    lado = box(x - 8, base - 2.6, x + 8, base - .6).union(ovalo(x, base - .6, 8, 2.2))
    lt = l.masa(lado, material='lejos', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.trazo([(x - 8, base - 1.6), (x - 4, base - .1), (x, base + .3), (x + 4, base - .1), (x + 8, base - 1.6)], .2, color='E8B952', alfa=.8,
            dentro=lt)
    borde = l.masa(ovalo(x, base - 2.6, 8, 2.3), material='claro', alto=.25, brillo=.4, vientre=0, hondo=0, linea=.35)
    l.mancha(ovalo(x, base - 2.5, 7.2, 1.8), '05201C', 1, dentro=borde)
    for _ in range(150):
        a, rr = rng.uniform(0, 2 * math.pi), math.sqrt(rng.uniform(0, 1))
        hx_, hy_ = x + 6.8 * rr * math.cos(a), base - 2.5 + 1.6 * rr * math.sin(a)
        l.mancha(ovalo(hx_, hy_, .34, .27), '1E4A42', .9)
        l.mancha(ovalo(hx_ - .1, hy_ - .1, .11, .09), 'D2F2DA', .9)


def astracan(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=(104, 6.6))
    horizonte = 15.4
    prado(l, horizonte, 41, .3)
    # lejos, en el horizonte, el Kremlin blanco con las cúpulas de su catedral
    l.masa(box(80, 12.6, 104, 15.8).buffer(.1), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    iglesia(l, 92, 12.8, 7, 4, cupulas=((0, .7), (-2.3, .42), (2.3, .42)), dorada=0, ventanas=2)
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
    # el muelle, adelante, con el gorro y la lata
    mu = l.masa(Polygon([(2, 33.2), (60, 33.2), (64, 41.5), (-2, 41.5)]).buffer(.1), material='vientre', alto=.12, brillo=.1, vientre=0,
                hondo=0, linea=.4)
    l.mancha(box(-2, 33, 66, 42), 'E8B952', .4, dentro=mu)
    for k in np.linspace(34.6, 40.4, 5):
        l.trazo([(2 - (k - 33.2) * .5, k), (60 + (k - 33.2) * .5, k)], .1, color='6B4E10', alfa=.55, dentro=mu)
    l.masa(box(57.7, 30, 59.1, 33.8), material='lejos', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    p = l.masa(tubo([(15, 39.4), (15.2, 27)], [.95, .85], 4), material='lejos', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(box(13, 26, 17.4, 40), 'E8B952', .3, dentro=p)             # el poste del muelle, de madera
    for k in (33.6, 35.4):
        l.trazo([(14.2, k), (16, k - .2)], .16, color='E8B952', alfa=.8, dentro=p)
    gorro(l, 15.3, 27.4, 10, 7.6, -8, semilla=9)
    lata_caviar(l, 38.4, 39.2, semilla=10)


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    cielo(l, sol=(92, 20.6), tarde=.35)
    nube(l, 30, 8, 16, .55)
    horizonte = 22.4
    m = l.masa(box(-2, horizonte, 122, 41), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 3), '64C8AA', .55, dentro=m, difuso=.8)
    rng = np.random.default_rng(8)
    for k in range(24):                                                # el reflejo del sol
        y = horizonte + .6 + k * .6
        w = 1 + k * .3
        x = 92 + rng.uniform(-1.2, 1.2) * (1 + k * .08)
        l.trazo([(x - w, y), (x + w, y)], .24, color='F2D48A', alfa=.8 - k * .02)
    for _ in range(16):
        x, y = rng.uniform(2, 116), rng.uniform(horizonte + 2, 39)
        if abs(x - 92) < 7:
            continue
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # un barco pesquero en el mar: el casco con la proa alta, la cabina atrás y el palo con su pluma
    y0 = horizonte + 2.2
    l.masa([forma([(49.6, y0 - 1.6), (51.4, y0 + 1), (62, y0 + 1), (64.6, y0 - 2.4), (62.6, y0 - 1.4), (51, y0 - 1.2)], 1),
            box(51.6, y0 - 3.6, 55.4, y0 - 1.2), tubo([(59.4, y0 - 1.2), (59.4, y0 - 7)], [.2, .16], 4),
            tubo([(59.4, y0 - 6.4), (63.4, y0 - 3.2)], [.12, .1], 4)], material='lejos', alto=.15, brillo=0, vientre=0, hondo=0, linea=.3,
           arroja=False)
    # las aves que vuelan sobre el delta
    for x, y, s in ((24, 12, 1.2), (30, 10.4, .9), (36, 13, 1), (70, 8.6, .8), (76, 10, .7), (44, 6.6, .7)):
        ave(l, x, y, s)
    # los últimos juncales del delta, a los costados, que salen del agua, y los lotos en flor adelante
    for x0, x1, y, h, n in ((-2, 24, 31, 6, 46), (96, 122, 32, 6, 46), (-2, 16, 39.4, 7, 34), (104, 122, 40, 7, 34)):
        l.mancha(Polygon([(x0, y - .6), (x1, y - .6), (x1 - 2, y + 1.6), (x0, y + 1.6)]), '0C3A33', .25, difuso=.6)
        juncos(l, x0, x1, y, h, n, semilla=int(x0 + y))
    for x, y, s in ((34, 36.6, 1.2), (46, 38.6, 1.4), (58, 35.8, 1), (72, 38.2, 1.3), (86, 36.4, 1.1)):
        loto(l, x, y, s)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Tver', dibujar=tver), dict(clave='Yaroslavl', dibujar=yaroslavl),
            dict(clave='Nizhni Nóvgorod', dibujar=nizhni), dict(clave='Kazán', dibujar=kazan), dict(clave='Samara', dibujar=samara),
            dict(clave='Volgogrado', dibujar=volgogrado), dict(clave='Astracán', dibujar=astracan), dict(clave='mar', dibujar=mar)]
LISTO = True
