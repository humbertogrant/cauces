# -*- coding: utf-8 -*-
"""Las postales del Rin, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: los Alpes suizos, con la nieve dorada del pico de donde baja el Rin; el río joven cruza el lago de Constanza y salta las
  cataratas de Schaffhausen, las más caudalosas de Europa, con su roca en medio;
- Basilea: «el río dobla en un codo de 90°»: visto desde arriba, el Rin viene por abajo y dobla hacia el norte, y en el codo, una escuadra
  dorada, de las de la escuela, marca el ángulo recto; la catedral de piedra roja en la orilla de afuera y, al fondo, el puerto;
- Estrasburgo: «una ciudad de calles, hoy sede del Parlamento Europeo»: la catedral de arenisca rosada, con su única aguja, dentro del
  círculo de estrellas doradas de Europa; las casas de entramado en las calles, y el Parlamento redondo junto al río;
- Maguncia: «letras de plomo flotando en el río»: los tipos de imprenta de Gutenberg, con sus letras doradas, flotan y dicen BIBLIA;
  atrás, la catedral de piedra roja;
- Coblenza: «la Esquina Alemana, donde el Mosela entra al Rin bajo una estatua ecuestre»: el jinete dorado en su pedestal, en la punta
  donde se juntan los dos ríos; enfrente, la fortaleza de Ehrenbreitstein en su cerro;
- Colonia: «dos torres góticas y un frasco de perfume»: la catedral oscura de dos torres y, delante, el frasco dorado del agua de colonia
  que rocía el río; a la izquierda, el puente de los arcos con su tren;
- Duisburgo: «un garaje de grúas»: un galpón abierto con una grúa dorada estacionada en cada lugar, como autos en un garaje, junto al
  muelle de las barcazas; atrás, las chimeneas del Ruhr;
- Rotterdam: «el río se rinde al mar en un puerto de 40 km»: una bandera blanca, en su asta dorada, clavada en el río; a los lados, las
  grúas del puerto que se pierden en el horizonte, y el puente Erasmus;
- el mar: el mar del Norte, frío y gris; en el dique, una veleta dorada con la N grande del norte; lejos, un buque que sale, un faro y
  las grúas. La barcaza del Rin no ve el mar: en Rotterdam se queda.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cebolla_baja, cielo, cinta, cordillera, nube, orilla, pasto,  # noqa: F401
                     piedra, prado, reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

ROJA = '9A5446'            # la arenisca roja de Basilea y de Maguncia
ROSA = 'D98A7C'            # la arenisca rosada de Estrasburgo
PLOMO = '6E7E7B'           # el gris del plomo y del acero
GRIS = '8FA19D'            # el gris frío del mar del Norte


def arenisca(l, piezas, color, tono=.45, linea=.35):
    """piedra de un color: el pálido de `vientre` teñido"""
    m = l.masa(piezas, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=linea, escalon=.2, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), color, tono, dentro=m)
    return m


def gotico(l, m, x, y, w=.9, h=3.2, alfa=.8):
    """una ventana gótica, en punta, dentro de la masa `m`"""
    l.mancha(forma([(x - w / 2, y), (x - w / 2, y - h * .7), (x, y - h), (x + w / 2, y - h * .7), (x + w / 2, y)], 1), '0C3A33', alfa, dentro=m)


def barcaza(l, x, y, s=1.0, carga='contenedores', lado=1):
    """una barcaza del Rin, chica, de casco de acero gris (no es la protagonista): la carga en la bodega y la casa a popa"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    c = l.masa(Polygon(P([(-12, -1.6), (11, -1.6), (12.4, -2.6), (11.6, .4), (-12, .4)])), material='claro', alto=.25, brillo=.15, vientre=0,
               hondo=0, linea=.3)
    l.mancha(Polygon(P([(-13, -3), (13, -3), (13, 1), (-13, 1)])), PLOMO, .55, dentro=c)
    if carga == 'contenedores':
        for k in range(6):
            u0 = -6.6 + k * 2.9
            l.masa(Polygon(P([(u0, -1.6), (u0 + 2.7, -1.6), (u0 + 2.7, -3.6), (u0, -3.6)])), material=('cuerpo', 'lejos', 'claro')[k % 3], alto=.2,
                   brillo=.15, vientre=0, hondo=0, linea=.2)
    l.masa([Polygon(P([(-11.4, -1.6), (-7.6, -1.6), (-7.6, -4), (-11.4, -4)])), Polygon(P([(-10.4, -4), (-8.4, -4), (-8.4, -5.4), (-10.4, -5.4)]))],
           material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    return c


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    cielo(l, sol=None)
    nube(l, 18, 4.4, 12, .5)
    nube(l, 104, 4, 12, .45)
    # los Alpes de los Grisones, nevados, y al medio el pico de donde baja el Rin, con la nieve dorada
    cordillera(l, [(-2, 17), (6, 10.6), (14, 13), (24, 6.6), (32, 11.4), (40, 9), (48, 15.6)], nieve=11.6)
    cordillera(l, [(72, 15.6), (80, 9.4), (88, 12), (98, 6), (106, 10.8), (114, 8.6), (122, 13)], nieve=11.4)
    pico = Polygon([(30, 25), (44, 15.4), (52, 8.4), (57, 4), (60, 1.6), (63.6, 4.6), (68, 8.6), (76, 15.4), (90, 25)])
    l.masa(pico, material='lejos', alto=.4, brillo=.1, vientre=0, hondo=.1, linea=.4, escalon=.3, contraluz=.3)
    l.trazo([(60, 1.8), (58.4, 8), (56, 14), (52, 20)], [.1, .3, .4, .2], color='0C3A33', alfa=.35)       # la arista
    linea_nieve = Polygon([(20, -5), (100, -5)] + [(x, 10.6 + 1.6 * math.sin(x * 1.3) + .9 * math.sin(x * .5)) for x in np.arange(100, 19.9, -.8)])
    nieve = pico.intersection(linea_nieve.buffer(0))
    n = l.masa(nieve, material='acento', alto=.35, brillo=.45, vientre=0, hondo=0, linea=.3, contraluz=.4)
    l.trazo([(60, 2), (58.6, 6), (57, 9.4)], [.05, .2, .1], color='FBEFCB', alfa=.8, dentro=n)
    # el lago de Constanza, ancho, al pie de los Alpes, y el río joven que baja del pico hasta él
    prado(l, 22, 41, .24)
    agua(l, forma([(-2, 23.4), (30, 22.6), (60, 22.8), (90, 22.6), (122, 23.4), (122, 27.4), (90, 28.2), (60, 28.6), (30, 28.2), (-2, 27.6)], 2), ondas=8,
         semilla=2, linea=.3)
    agua(l, cinta([(60.6, 12), (60, 16.4), (61, 20), (60.4, 23.4)], [.9, 1.3, 1.8, 2.4], 6), linea=.25)
    # las cataratas de Schaffhausen, adelante: el escalón de roca, el agua blanca que cae y la espuma; la roca en medio
    agua(l, forma([(36, 28), (48, 28.4), (72, 28.4), (84, 28), (90, 30.6), (30, 30.6)], 2), linea=.3)
    roca = forma([(26, 41.5), (28, 33.4), (34, 30.4), (86, 30.4), (92, 33.4), (94, 41.5)], 1)
    l.masa(roca, material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35)
    for x in np.arange(30, 91, 1.6):                                     # los chorros
        l.trazo([(x, 30.4), (x + .4, 34), (x - .2, 38.4)], [1.1, 1.3, .6], color='FFFFFF', alfa=.85)
    l.mancha(ovalo(60, 39.6, 36, 2.6), 'FFFFFF', .75, difuso=.8)
    l.masa(forma([(56.6, 39.4), (57.4, 33.4), (59, 29.4), (61.4, 29), (62.6, 33.6), (63.4, 39.4)], 1), material='oscuro', alto=.35, brillo=.2, vientre=0,
           hondo=0, linea=.35)                                           # la roca en medio de la catarata
    for x0, x1 in ((-2, 30), (90, 122)):                                 # las orillas con sus árboles
        for k in range(5):
            arbol(l, x0 + (x1 - x0) * (k + .5) / 5, 33 + (k % 2) * 3, 2.6, semilla=k + int(x0))
    l.masa([box(99, 27.4, 111, 31.6), box(102.6, 23.4, 106.2, 27.6)], material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.3)  # el castillo
    l.masa([Polygon([(98.4, 27.6), (105, 24.8), (111.6, 27.6)]), Polygon([(102.2, 23.6), (104.4, 20.6), (106.6, 23.6)])], material='lejos', alto=.2,
           brillo=.1, vientre=0, hondo=0, linea=.25)


# ------------------------------------------------------------------------------------------------ Basilea
def escuadra(l, x, y, ancho, alto_):
    """una escuadra de la escuela, dorada, acostada: el ángulo recto en (x, y), un cateto hacia la derecha y otro hacia arriba, con su
    hueco en triángulo y las rayitas de la regla"""
    t = Polygon([(x, y), (x + ancho, y), (x, y - alto_)])
    hueco = Polygon([(x + ancho * .2, y - alto_ * .14), (x + ancho * .62, y - alto_ * .14), (x + ancho * .2, y - alto_ * .62)])
    g = t.difference(hueco)
    l.mancha(affinity.translate(g, 1.2, 1), '0C3A33', .3, difuso=.6)
    m = l.masa(g, material='acento', alto=.25, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for k in np.arange(2, ancho - 2, 2):                                 # las rayitas de la regla, en los dos catetos
        l.trazo([(x + k, y - .2), (x + k, y - (1.4 if k % 10 < 1 else .8))], .1, color='6B4E10', alfa=.8, dentro=m)
    for k in np.arange(1.4, alto_ - 1.4, 1.4):
        l.trazo([(x + .2, y - k), (x + (1.6 if round(k / 1.4) % 5 == 0 else 1), y - k)], .1, color='6B4E10', alfa=.8, dentro=m)
    l.trazo([(x + 2.4, y - .1), (x + 2.4, y - 2.4), (x + .1, y - 2.4)], .16, color='6B4E10', alfa=.9, dentro=m)      # la marca del ángulo recto
    return g


def basilea(l):
    rng = np.random.default_rng(2)
    cielo(l, sol=None)
    nube(l, 92, 3, 12, .4)
    # visto desde arriba: la tierra, y el Rin que viene por abajo desde la derecha y en el codo dobla hacia el norte, al fondo
    tierra(l, 5, 41, desierto=.24)
    rin = cinta([(124, 33.6), (96, 33.2), (70, 32.6), (52, 32), (45.4, 30.6), (43, 26.6), (42.4, 20), (42.2, 13), (42, 5.4)],
                [10, 9.8, 9.6, 9.4, 9, 7.6, 5.8, 4.2, 2.6], 4)
    agua(l, rin, ondas=12, semilla=3, linea=.35)
    # el puerto, al fondo, río abajo: las grúas y los tanques
    for x, h in ((34, 6), (37.6, 5), (48, 5.6), (51.4, 6.4)):
        l.masa([box(x - .3, 7.4 - h, x + .3, 7.4), Polygon([(x - .2, 7.4 - h), (x + 2.6, 7.4 - h - .6), (x + 2.6, 7.4 - h - .2), (x, 7.4 - h + .6)])],
               material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)
    # la Basilea de la orilla de afuera, abajo a la izquierda, con la catedral de piedra roja y sus dos torres
    for _ in range(30):
        x, y = rng.uniform(1, 38), rng.uniform(14, 41)
        if rin.buffer(1).intersects(box(x - 1.4, y - 2, x + 1.4, y)) or (8 < x < 30 and y > 31):
            continue
        l.masa(box(x - 1.2, y - 1.6, x + 1.2, y), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
        l.masa(Polygon([(x - 1.4, y - 1.6), (x, y - 2.8), (x + 1.4, y - 1.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2,
               arroja=False)
    cat = arenisca(l, [box(10, 34.6, 28, 40.6), box(10.4, 28.6, 14.4, 35), box(23.6, 28.6, 27.6, 35), Polygon([(10.2, 28.8), (12.4, 24.4), (14.6, 28.8)]),
                       Polygon([(23.4, 28.8), (25.6, 24.4), (27.8, 28.8)])], ROJA, .55)
    for x in (12.4, 25.6):
        gotico(l, cat, x, 33.4, .9, 3)
    for x in np.arange(15.6, 23, 2.2):
        gotico(l, cat, x, 39.6, .9, 3.4)
    # la otra orilla, adentro del codo, con sus casas, y la escuadra dorada, protagonista, que marca el ángulo recto
    for _ in range(36):
        x, y = rng.uniform(48, 120), rng.uniform(8, 27)
        if rin.buffer(1).intersects(box(x - 1.4, y - 2, x + 1.4, y)) or (Polygon([(46, 28.6), (94, 28.6), (46, 5)]).buffer(1).intersects(box(x - 1.4, y - 2, x + 1.4, y))):
            continue
        l.masa(box(x - 1.2, y - 1.6, x + 1.2, y), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2, arroja=False)
        l.masa(Polygon([(x - 1.4, y - 1.6), (x, y - 2.8), (x + 1.4, y - 1.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2,
               arroja=False)
    escuadra(l, 48.4, 27.4, 44, 22)
    barcaza(l, 92, 34.6, .7, lado=-1)


# ------------------------------------------------------------------------------------------------ Estrasburgo
def estrella(l, x, y, r):
    """una estrella dorada de cinco puntas"""
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * .42
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return l.masa(Polygon(pts), material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.3, contraluz=.35)


def entramado(l, x, base, w=5.0, h=6.0, semilla=0):
    """una casa de entramado: las paredes blancas con las vigas oscuras en cruz y el techo empinado"""
    rng = np.random.default_rng(semilla)
    c = l.masa(box(x, base - h, x + w, base).buffer(.05), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for y in np.arange(base - h, base, h / 3):                           # los pisos
        l.trazo([(x, y), (x + w, y)], .22, color='5A3E1E', alfa=.85, dentro=c)
        for k in range(int(w // 1.7)):
            x0 = x + .3 + k * 1.7
            if rng.random() < .5:
                l.trazo([(x0, y + .1), (x0 + 1.3, y + h / 3 - .1)], .16, color='5A3E1E', alfa=.8, dentro=c)
            else:
                l.trazo([(x0 + .6, y), (x0 + .6, y + h / 3)], .16, color='5A3E1E', alfa=.8, dentro=c)
    l.masa(Polygon([(x - .4, base - h), (x + w / 2, base - h - w * .8), (x + w + .4, base - h)]), material='lejos', alto=.25, brillo=.12,
           vientre=0, hondo=0, linea=.3)


def estrasburgo(l):
    cielo(l, sol=None)
    nube(l, 16, 4, 12, .45)
    nube(l, 104, 3.6, 12, .4)
    prado(l, 22, 41, .22)
    # a la derecha, el Parlamento Europeo: la torre redonda de vidrio junto al río
    p = l.masa([box(92, 12.4, 112, 24.4), ovalo(102, 12.6, 10, 2.4)], material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    for y in np.arange(14, 24, 1.3):
        l.trazo([(92.4, y), (111.6, y)], .14, color='8EB5AA', alfa=.8, dentro=p)
    # la catedral de arenisca rosada, al medio: la fachada con su rosetón, la nave, y una sola aguja, la del norte
    cat = arenisca(l, [box(48, 14.4, 72, 27), box(72, 18.4, 90, 27), Polygon([(71.6, 18.6), (81, 14.4), (90.4, 18.6)]), box(48.6, 9.4, 56.6, 14.6),
                       box(63.4, 10.6, 71.4, 14.6), box(50, 4.4, 55.2, 9.6), Polygon([(50.2, 4.6), (52.6, -1.4), (55, 4.6)])], ROSA, .55, .4)
    l.mancha(ovalo(60, 17.6, 2.6, 2.6), '0C3A33', .7, dentro=cat)        # el rosetón
    for a in range(0, 360, 45):
        l.trazo([(60, 17.6), (60 + 2.4 * math.cos(math.radians(a)), 17.6 + 2.4 * math.sin(math.radians(a)))], .12, color=ROSA, alfa=.9, dentro=cat)
    for x in (52.6, 67.4):
        gotico(l, cat, x, 13.6, 1, 3.4)
        gotico(l, cat, x, 25, 1.4, 5)
    gotico(l, cat, 60, 26.4, 2.6, 5.2, .85)                              # el portal
    for x in np.arange(74.6, 89, 2.8):
        gotico(l, cat, x, 25.6, .9, 4)
    for y in np.arange(0, 4.4, 1.1):                                     # la aguja calada
        l.trazo([(52.6 - (4.6 - y) * .5, y + .3), (52.6 + (4.6 - y) * .5, y + .3)], .1, color='6B4E10', alfa=.5, dentro=cat)
    # las calles de casas de entramado, adelante, y el río
    for k, x in enumerate((-1, 5.6, 12, 18.6, 25)):
        entramado(l, x, 29.4, 5.6, 6.4 + (k % 2) * 1.4, semilla=k)
    for k, x in enumerate((95, 101.6, 108, 114.6)):
        entramado(l, x, 29.4, 5.6, 5.6 + (k % 2) * 1.6, semilla=k + 5)
    rio(l, 30)
    # el círculo de estrellas de Europa alrededor de la catedral, protagonista
    for k in range(12):
        a = math.radians(-90 + k * 30)
        estrella(l, 64 + 21.6 * math.cos(a), 14.2 + 12 * math.sin(a), 2.4)


# ------------------------------------------------------------------------------------------------ Maguncia
def letra(ch, x, y, h):
    """una letra de imprenta, con remates, de alto `h`, con su pie izquierdo en (x, y); devuelve (polígono, ancho)"""
    g = .2 * h                                                           # el grosor del trazo
    if ch == 'I':
        return unary_union([box(x + .1 * h, y - h, x + .1 * h + g, y), box(x, y - h, x + .4 * h, y - h + .1 * h), box(x, y - .1 * h, x + .4 * h, y)]), .4 * h
    if ch == 'L':
        return unary_union([box(x + .08 * h, y - h, x + .08 * h + g, y), box(x, y - h, x + .38 * h, y - h + .1 * h), box(x, y - g * .9, x + .58 * h, y),
                            box(x + .5 * h, y - .3 * h, x + .58 * h, y)]), .58 * h
    if ch == 'B':
        fuera = unary_union([box(x, y - h, x + .32 * h, y), ovalo(x + .3 * h, y - .74 * h, .27 * h, .26 * h), ovalo(x + .33 * h, y - .26 * h, .3 * h, .26 * h)])
        hueco = unary_union([ovalo(x + .3 * h, y - .74 * h, .11 * h, .1 * h).union(box(x + g, y - .84 * h, x + .3 * h, y - .64 * h)),
                             ovalo(x + .33 * h, y - .26 * h, .13 * h, .1 * h).union(box(x + g, y - .36 * h, x + .33 * h, y - .16 * h))])
        return fuera.difference(hueco), .63 * h
    if ch == 'A':
        fuera = Polygon([(x, y), (x + .3 * h, y - h), (x + .44 * h, y - h), (x + .74 * h, y)])
        hueco = Polygon([(x + .29 * h, y - .36 * h), (x + .37 * h, y - .66 * h), (x + .45 * h, y - .36 * h)])
        pie = Polygon([(x + .2 * h, y + .1), (x + .37 * h, y - .22 * h), (x + .54 * h, y + .1)])
        return fuera.difference(hueco).difference(pie), .74 * h
    raise ValueError(ch)


def maguncia(l):
    rng = np.random.default_rng(4)
    cielo(l, sol=None)
    nube(l, 22, 4.4, 12, .5)
    nube(l, 100, 4, 12, .45)
    # la ciudad, enfrente, con la catedral de piedra roja y su torre de corona
    prado(l, 16, 22, .2)
    casitas(l, -1, 40, 18.4, 4, semilla=11)
    casitas(l, 82, 122, 18.4, 4, semilla=12)
    cat = arenisca(l, [box(44, 9.4, 80, 18.6), box(54, 2.4, 62, 9.6), box(46, 5.4, 50.6, 9.6), box(74, 5.4, 78.6, 9.6),
                       Polygon([(53.6, 2.6), (58, -1.4), (62.4, 2.6)]), Polygon([(45.8, 5.6), (48.3, 2.6), (50.8, 5.6)]),
                       Polygon([(73.8, 5.6), (76.3, 2.6), (78.8, 5.6)])], ROJA, .55)
    for x in np.arange(46.6, 79, 3):
        gotico(l, cat, x, 16.6, 1, 4)
    gotico(l, cat, 58, 8, 1.2, 3.6)
    rio(l, 19.4)
    # los tipos de imprenta que flotan, protagonistas: cada uno, un bloque de plomo con su letra dorada encima; dicen BIBLIA
    x = 21.6
    for k, ch in enumerate('BIBLIA'):
        h = 13
        g, w = letra(ch, 0, 0, h)
        giro = rng.uniform(-7, 7)
        y = 31.4 + rng.uniform(-1.2, 1.2) + (k % 2) * 1.6
        bloque = box(-.9, 0, w + .9, 4.4)
        pieza = affinity.translate(affinity.rotate(unary_union([g, bloque]), giro, origin=(w / 2, 0)), x, y)
        l.mancha(ovalo(x + w / 2, y + 3.6, w * .9, 1.2), 'FFFFFF', .5, difuso=.4)            # el agua que se abre alrededor
        b = l.masa(affinity.translate(affinity.rotate(bloque, giro, origin=(w / 2, 0)), x, y), material='claro', alto=.25, brillo=.3, vientre=0,
                   hondo=0, linea=.35)
        l.mancha(affinity.translate(affinity.rotate(bloque, giro, origin=(w / 2, 0)), x, y).buffer(.5), PLOMO, .55, dentro=b)
        l.masa(affinity.translate(affinity.rotate(g, giro, origin=(w / 2, 0)), x, y), material='acento', alto=.4, brillo=.45, vientre=0, hondo=0,
               linea=.4, contraluz=.35)
        reflejo(l, pieza, y + 4.6, .2)
        x += w + 4.2


# ------------------------------------------------------------------------------------------------ Coblenza
def jinete_estatua(l, x, base, s=1.0):
    """la estatua ecuestre, dorada: el caballo que avanza al paso, mirando a la izquierda, con una mano levantada, y el jinete erguido,
    con su capa y su casco; (x, base) es donde pisan las patas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    lejos = [tubo(P([(4.6, -8), (5.4, -4), (5, 0)]), [1.2 * s, .9 * s, .7 * s], 5), tubo(P([(-4.4, -8.4), (-4.8, -4.2), (-4.6, 0)]), [1.1 * s, .8 * s, .7 * s], 5)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.3), '6B4E10', .35)
    caballo = [O(0, -10, 7, 3.6), tubo(P([(-4.4, -11.2), (-6.6, -14.4), (-8.2, -16.2)]), [3.4 * s, 2.8 * s, 2.2 * s], 6),
               forma(P([(-7.2, -17.6), (-9, -18), (-11, -16.6), (-13.4, -13.6), (-13.4, -12.4), (-12, -12.2), (-9.4, -14), (-7.4, -15.4)]), 1),
               Polygon(P([(-7.8, -17.4), (-7.4, -19.4), (-6.8, -17.4)])),
               tubo(P([(6, -11), (8.6, -9), (9.4, -4.4)]), [1.4 * s, 1.1 * s, .6 * s], 6),
               tubo(P([(5.8, -8.6), (6.6, -4.4), (6.4, 0)]), [1.4 * s, 1 * s, .8 * s], 5), tubo(P([(-5.4, -8.6), (-5.8, -4.2), (-5.6, 0)]), [1.3 * s, 1 * s, .8 * s], 5),
               tubo(P([(-3.4, -8.6), (-5.4, -6.2), (-7.6, -6.6)]), [1.2 * s, 1 * s, .8 * s], 5)]       # la mano levantada
    c = l.masa(caballo, material='acento', alto=.55, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.trazo(P([(-7.2, -17.6), (-5.6, -15.4), (-3.8, -12.6)]), [.3, .5, .2], color='6B4E10', alfa=.5, dentro=c)     # la crin
    l.mancha(O(-9.6, -16, .3, .3), '05201C', .9)
    jinete = [forma(P([(-1.6, -12.6), (1.8, -12.6), (2.2, -17), (1.4, -21.6), (-1.4, -21.6), (-2.2, -17)]), 1), O(0, -23.4, 1.5, 1.6),
              Polygon(P([(-.4, -25), (0, -27.2), (.4, -25)])), tubo(P([(-1.4, -20.6), (-3.6, -18), (-5.6, -17.2)]), [.7 * s, .6 * s, .5 * s], 5),
              forma(P([(1.2, -21.4), (4.6, -18), (6.6, -12), (2.4, -13.4)]), 1), tubo(P([(.6, -13), (-.6, -10.4), (.6, -8.2)]), [1 * s, .8 * s, .6 * s], 5)]
    l.masa(jinete, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.4)
    return c


def coblenza(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .5)
    # los cerros de viñedos, enfrente: a la derecha, el de Ehrenbreitstein con su fortaleza larga
    for pts in ([(64, 24), (70, 13), (82, 9.4), (104, 9), (118, 12), (124, 24)], [(-2, 24), (-2, 13), (14, 11.4), (30, 13.6), (44, 18.4), (54, 24)]):
        orilla(l, forma(pts, 2), tinte=.34)
    f = piedra(l, [box(74, 7.4, 116, 11.6), box(78, 5.4, 82, 7.6), box(108, 5.4, 112, 7.6)], .3)
    for x in np.arange(75, 115, 1.8):
        l.mancha(box(x, 8.6, x + .7, 9.8), '164F46', .7, dentro=f)
    for x0, x1, y0, y1 in ((68, 122, 14, 22), (0, 46, 15, 22)):          # las hileras de las viñas
        for y in np.arange(y0, y1, 1.6):
            l.trazo([(x0 + (y - y0) * .6, y), (x1 - (y - y0) * .4, y)], .22, color='2F8A74', alfa=.55)
    # los dos ríos: el Mosela, que baja por la izquierda, y el Rin, ancho, por la derecha; se juntan delante de la punta
    mosela = cinta([(-2, 23.4), (16, 25.4), (32, 29), (46, 34.4)], [5, 6, 7.4, 9], 6)
    rin_ = cinta([(124, 23.4), (100, 25.6), (80, 30), (66, 35)], [9, 10, 11, 12], 6)
    a = agua(l, unary_union([mosela, rin_, box(-2, 32.6, 122, 41.5)]).buffer(.3).buffer(-.3), ondas=14, semilla=6, linea=.35)
    l.mancha(mosela, '9BDDBD', .3, dentro=a, difuso=1.2)
    # la Esquina Alemana: la punta de piedra entre los dos ríos, el pedestal y el jinete dorado, protagonista
    punta = forma([(30, 24), (90, 24), (82, 28), (70, 33), (62, 36.4), (58, 36.4), (50, 33), (38, 28)], 1)
    piedra(l, punta, .3, .4)
    for x in np.arange(34, 88, 2.2):
        l.trazo([(x, 24.6), (x + .4, 25.4)], .1, color='6B4E10', alfa=.4)
    ped = piedra(l, [box(51, 26, 69, 32.4), box(54, 23, 66, 26.4), box(56, 21.2, 64, 23.2)], .35, .45)
    for x in np.arange(52, 69, 3):
        l.trazo([(x, 27.4), (x, 32)], .3, color='6B4E10', alfa=.35, dentro=ped)
    l.mancha(forma([(58.4, 32.4), (58.4, 29), (60, 27.6), (61.6, 29), (61.6, 32.4)], 1), '0C3A33', .75, dentro=ped)
    jinete_estatua(l, 60.4, 21.4, .76)
    reflejo(l, punta, 36.6, .2)


# ------------------------------------------------------------------------------------------------ Colonia
def frasco(l, x, base, s=1.0):
    """el frasco del agua de colonia, dorado: el cuerpo redondeado, el cuello, la tapa con su pera de goma para rociar y la nube de
    perfume que sale; (x, base) es el pie del frasco"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = forma(P([(-5.2, 0), (-6, -3), (-6, -9), (-4.6, -11.4), (-1.6, -12.2), (1.6, -12.2), (4.6, -11.4), (6, -9), (6, -3), (5.2, 0)]), 2)
    c = l.masa([cuerpo, box(x - 1.6 * s, base - 14.6 * s, x + 1.6 * s, base - 11.8 * s)], material='acento', alto=.6, brillo=.6, vientre=0, hondo=0,
               linea=.45, contraluz=.45)
    l.trazo(P([(-4.4, -2), (-4.8, -6), (-4, -9.6)]), [.1, .5, .1], color='FBEFCB', alfa=.85, dentro=c)          # el brillo del vidrio
    l.mancha(Polygon(P([(-3.4, -4), (3.4, -4), (3.4, -8.4), (-3.4, -8.4)])), 'FBEFCB', .7, dentro=c)          # la etiqueta
    for v in (-5.4, -6.4, -7.4):
        l.trazo(P([(-2.4, v), (2.4, v)]), .14 * s, color='6B4E10', alfa=.7, dentro=c)
    l.masa([box(x - 1.2 * s, base - 16.6 * s, x + 1.2 * s, base - 14.4 * s), tubo(P([(1.2, -15.6), (4, -16.4), (6.4, -15.4)]), [.4 * s, .35 * s, .3 * s], 6),
            O(7.8, -15, 1.8, 1.5)], material='acento', alto=.45, brillo=.4, vientre=0, hondo=0, linea=.35)
    for k in range(5):                                                   # la nube de perfume, que sale de la tapa
        l.mancha(O(-3.6 - k * 2.4, -16.4 - k * .9, 1 + k * .45, .8 + k * .3), 'FFFFFF', .85 - k * .12, difuso=.5)
    return c


def colonia(l):
    cielo(l, sol=None)
    nube(l, 22, 4.4, 12, .45)
    nube(l, 104, 4, 10, .4)
    prado(l, 19, 24, .2)
    casitas(l, -1, 30, 21.4, 4, semilla=13)
    casitas(l, 90, 122, 21.4, 4, semilla=14)
    # la catedral, oscura y enorme, con sus dos torres caladas hasta la punta
    torres = []
    for x in (50.4, 69.6):
        torres += [box(x - 3.4, 11, x + 3.4, 23), Polygon([(x - 3.6, 11.2), (x, .8), (x + 3.6, 11.2)])]
        for y in np.arange(2.6, 11, 1.8):                                # los ganchos de la aguja
            w = (y - .8) / 10.4 * 3.6
            torres += [Polygon([(x - w, y), (x - w - .7, y - .5), (x - w + .2, y - .9)]), Polygon([(x + w, y), (x + w + .7, y - .5), (x + w - .2, y - .9)])]
    cat = l.masa([box(53.6, 14.6, 66.4, 23), box(73, 16.4, 90, 23), Polygon([(72.6, 16.6), (81.4, 12), (90.4, 16.6)])] + torres, material='lejos', alto=.3,
                 brillo=.1, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.25)
    l.mancha(box(40, -3, 92, 23.4), PLOMO, .45, dentro=cat)
    for x in (50.4, 69.6):
        gotico(l, cat, x, 21, 2.2, 7, .85)
        gotico(l, cat, x, 13.4, 1.2, 2.4, .7)
        for y in np.arange(3.4, 11, 1.6):                                # las agujas caladas
            w = (y - .8) / 10.4 * 3.6
            l.trazo([(x - w * .7, y), (x + w * .7, y)], .1, color='05201C', alfa=.55, dentro=cat)
    gotico(l, cat, 60, 21.4, 3, 5.6, .85)
    for x in np.arange(75, 89, 2.6):
        gotico(l, cat, x, 21.6, .9, 4)
    # el puente de los arcos, a la izquierda, con el tren
    rio(l, 23)
    for x0 in (-2, 12, 26):
        l.masa(cinta([(x0 + 14 * k / 12, 22.4 - 5.4 * math.sin(math.pi * k / 12)) for k in range(13)], [.7] * 13, 3), material='lejos', alto=.2,
               brillo=.2, vientre=0, hondo=0, linea=.3)
    l.masa(box(-2, 22, 41, 23.4), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.masa([box(4, 19.6, 13, 22), box(13.6, 19.6, 22.6, 22), box(23.2, 19.6, 32.2, 22)], material='claro', alto=.25, brillo=.2, vientre=0, hondo=0,
           linea=.25)
    # la orilla de adelante y el frasco de perfume, protagonista, delante de la catedral
    m = orilla(l, forma([(-2, 41.5), (-2, 33), (30, 31.6), (60, 31.4), (90, 31.6), (122, 33), (122, 41.5)], 2), tinte=.24)
    pasto(l, 0, 120, 33, 40.6, 18, semilla=15, dentro=m)
    l.mancha(ovalo(61, 37.4, 8, 1.2), '0C3A33', .25, difuso=.6)
    frasco(l, 60, 37.4, 1.2)


# ------------------------------------------------------------------------------------------------ Duisburgo
def grua(l, x, base, s=1.0, giro=40):
    """una grúa de puerto, dorada: el pórtico de cuatro patas, la cabina, el contrapeso y la pluma levantada hacia la derecha"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    a = math.radians(giro)
    punta = (x + (2 + 14 * math.cos(a)) * s, base + (-9.4 - 14 * math.sin(a)) * s)
    piezas = [Polygon(P([(-3, 0), (-2.2, 0), (-.6, -6), (-1.6, -6)])), Polygon(P([(3, 0), (2.2, 0), (.6, -6), (1.6, -6)])),
              box(x - 2 * s, base - 6.6 * s, x + 2 * s, base - 5.8 * s), box(x - 1.6 * s, base - 9.6 * s, x + 1.8 * s, base - 6.4 * s),
              box(x - 3.6 * s, base - 9 * s, x - 1.4 * s, base - 7 * s), Polygon(P([(-.4, -9.4), (.4, -9.4), (0, -13)])),
              tubo([(x + 1.6 * s, base - 9 * s), punta], [.7 * s, .4 * s], 4)]
    m = l.masa(piezas, material='acento', alto=.35, brillo=.4, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.trazo([(x, base - 13 * s), punta], .1 * s, color='6B4E10', alfa=.9)                    # el tensor
    l.trazo([punta, (punta[0], punta[1] + 5 * s)], .08 * s, color='0C3A33', alfa=.9)          # el cable y el gancho
    l.mancha(box(x - .4 * s, base - 8.8 * s, x + 1 * s, base - 7.4 * s), '164F46', .85, dentro=m)
    return m


def duisburgo(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 98, 3.6, 12, .4)
    # atrás, las chimeneas del Ruhr con su humo
    prado(l, 10, 24, .16)
    for x, h in ((6, 9), (12, 12), (110, 10), (116, 13)):
        l.masa(box(x - .8, 12 - h, x + .8, 12.2), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
        for k in range(3):
            l.mancha(ovalo(x + 1.6 + k * 2.2, 12 - h - 1.4 - k * 1.1, 1.3 + k * .5, 1 + k * .3), 'FFFFFF', .7 - k * .15, difuso=.4)
    # el garaje: un galpón largo y abierto, de techo de chapa sobre columnas, con un lugar numerado para cada grúa
    piso = box(14, 27.4, 106, 29)
    l.masa(piso, material='vientre', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.3)
    fondo_ = l.masa(box(14, 7.4, 106, 27.6), material='lejos', alto=.1, brillo=.05, vientre=0, hondo=0, linea=.3)
    l.mancha(box(14, 7.4, 106, 27.6), '0C3A33', .35, dentro=fondo_)
    for k in range(4):                                                   # las grúas, una en cada lugar
        grua(l, 25.6 + k * 23, 27.4, 1, 46)
    for x in (14, 37, 60, 83, 106):                                      # las columnas
        l.masa(box(x - .9, 7.6, x + .9, 28), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    techo = Polygon([(10.6, 7.8), (16, 3.4), (104, 3.4), (109.4, 7.8)])
    t = l.masa(techo, material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)
    for x in np.arange(17, 104, 2):
        l.trazo([(x, 3.6), (x + (x - 60) * .06, 7.6)], .12, color='8EB5AA', alfa=.8, dentro=t)
    for k in range(4):                                                   # las rayas del piso de cada lugar
        x0 = 15.4 + k * 23
        l.trazo([(x0 + 2, 28.2), (x0 + 19, 28.2)], .2, color='FFFFFF', alfa=.85)
    # el muelle y el río, con una barcaza cargada de contenedores
    rio(l, 30.4)
    barcaza(l, 62, 36.4, 1.2)


# ------------------------------------------------------------------------------------------------ Rotterdam
def bandera(l, x, base, alto_, s=1.0):
    """la bandera blanca de la rendición, flameando, en su asta dorada clavada en el agua"""
    a = l.masa([box(x - .5 * s, base - alto_, x + .5 * s, base), ovalo(x, base - alto_ - .3, 1 * s, 1 * s)], material='acento', alto=.4, brillo=.5,
               vientre=0, hondo=0, linea=.35, contraluz=.35)
    y0 = base - alto_ + 1
    ola = lambda t: 1.1 * math.sin(t * math.pi * 1.6)
    arriba = [(x + .5 + 18 * t * s, y0 + ola(t) * s) for t in np.linspace(0, 1, 16)]
    abajo = [(x + .5 + 18 * t * s, y0 + 11 * s + ola(t + .12) * s + t * .6) for t in np.linspace(1, 0, 16)]
    f = l.masa(Polygon(arriba + abajo).buffer(.1), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for t in (.3, .62):                                                  # los pliegues
        l.trazo([(x + .5 + 18 * t * s, y0 + ola(t) * s + .4), (x + .5 + 18 * (t + .04) * s, y0 + 10.6 * s + ola(t + .12) * s)], [.1, .4, .1],
                color='9DB9B0', alfa=.7, dentro=f)
    return a


def rotterdam(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .45)
    # el puerto que se pierde en el horizonte: las grúas de las dos orillas, cada vez más chicas
    prado(l, 14.6, 16.4, .14)
    for lado in (-1, 1):
        for k in range(8):
            f = (k / 7) ** .8
            x = 60 + lado * (57 - 49 * f)
            y = 30.6 - 15 * f
            h = 11 * (1 - f * .8)
            for j in range(3):                                           # los contenedores apilados en el muelle
                c = box(x + lado * h * .25, y - h * .14 * (j + 1), x + lado * h * .65, y - h * .14 * j)
                l.masa(c if lado > 0 else affinity.scale(c, 1, 1), material=('cuerpo', 'claro', 'lejos')[(k + j) % 3], alto=.15, brillo=.1, vientre=0,
                       hondo=0, linea=.12 + .1 * (1 - f), arroja=False)
            l.masa([Polygon([(x - h * .16, y), (x - h * .05, y - h * .62), (x + h * .05, y - h * .62), (x + h * .16, y)]), box(x - h * .1, y - h * .8, x + h * .1, y - h * .6),
                    Polygon([(x, y - h * .74), (x - lado * h * .95, y - h * 1.02), (x - lado * h * .95, y - h * .94), (x, y - h * .62)])], material='lejos',
                   alto=.2, brillo=.1, vientre=0, hondo=0, linea=.16 + .12 * (1 - f), arroja=False)
    agua(l, Polygon([(-2, 41.5), (-2, 30), (54, 15.6), (66, 15.6), (122, 30), (122, 41.5)]), ondas=14, semilla=8, linea=.3)
    for lado in (-1, 1):                                                 # los muelles de las dos orillas
        l.masa(Polygon([(60 + lado * 62, 41.5), (60 + lado * 62, 30.2), (60 + lado * 6, 15.6), (60 + lado * 7.6, 15.6), (60 + lado * 64, 31.4),
                         (60 + lado * 64, 41.5)]).buffer(0), material='vientre', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.3)
    # el puente Erasmus, blanco, con su pilón doblado y sus tirantes, a lo lejos
    l.masa(box(40, 18.6, 80, 19.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.masa(Polygon([(49, 18.8), (50.4, 18.8), (53, 8.6), (52, 6.4), (51.2, 6.6), (51.8, 8.6)]), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.3)
    for k in range(7):
        l.trazo([(52.2, 7.4 + k * .9), (54 + k * 3.6, 18.8)], .08, color='8EB5AA', alfa=.9)
        l.trazo([(51.6, 8 + k * .9), (48 - k * 1.2, 18.8)], .08, color='8EB5AA', alfa=.9)
    for x, h in ((70, 8), (74, 11), (78, 7), (86, 9), (34, 7), (30, 10)):         # los edificios de vidrio
        e = l.masa(box(x - 1.6, 16.4 - h, x + 1.6, 16.6), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25, arroja=False)
        for y in np.arange(16.4 - h + .8, 16.2, 1):
            l.trazo([(x - 1.2, y), (x + 1.2, y)], .08, color='8EB5AA', alfa=.8, dentro=e)
    barcaza(l, 30, 36.4, .9)
    # la bandera blanca, protagonista: el río se rinde al mar
    for k in range(3):
        l.trazo([(58.4 + (2.4 + k * 2.2) * math.cos(t), 37.6 + (.6 + k * .4) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 25)], .14,
                color='D2F2DA', alfa=.75 - k * .15)
    a = bandera(l, 58.4, 37.4, 31.4, 1.05)
    reflejo(l, a.g, 37.6, .25)


# ------------------------------------------------------------------------------------------------ el mar
def letra_veleta(ch, x, y, h):
    """las letras de los puntos cardinales de la veleta: N, S, E, O, centradas en (x, y)"""
    w, g = h * .7, h * .2
    x0, y0 = x - w / 2, y + h / 2
    if ch == 'N':
        return unary_union([box(x0, y0 - h, x0 + g, y0), box(x0 + w - g, y0 - h, x0 + w, y0),
                            Polygon([(x0, y0 - h), (x0 + g * 1.3, y0 - h), (x0 + w, y0), (x0 + w - g * 1.3, y0)])])
    if ch == 'E':
        return unary_union([box(x0, y0 - h, x0 + g, y0), box(x0, y0 - h, x0 + w, y0 - h + g), box(x0, y0 - h / 2 - g / 2, x0 + w * .8, y0 - h / 2 + g / 2),
                            box(x0, y0 - g, x0 + w, y0)])
    if ch == 'O':
        return ovalo(x, y, w / 2 + g * .2, h / 2).difference(ovalo(x, y, w / 2 - g * .8, h / 2 - g))
    if ch == 'S':
        pts = [(x0 + w, y0 - h + g), (x0 + w * .5, y0 - h + g * .5), (x0 + g * .5, y0 - h * .76), (x0 + w * .5, y0 - h * .5),
               (x0 + w - g * .5, y0 - h * .24), (x0 + w * .5, y0 - g * .5), (x0, y0 - g)]
        return tubo(pts, [g] * 7, 6)
    raise ValueError(ch)


def veleta(l, x, base, s=1.0):
    """la veleta dorada del dique: el poste, la cruz de los puntos cardinales con sus letras (la N grande, hacia el mar) y la flecha arriba;
    (x, base) es el pie del poste"""
    l.masa(box(x - .5 * s, base - 22 * s, x + .5 * s, base), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    cy = base - 15 * s
    brazos = [box(x - 10 * s, cy - .3 * s, x + 10 * s, cy + .3 * s), Polygon([(x - .3 * s, cy + .3 * s), (x + 6.6 * s, cy - 5.6 * s),
                                                                          (x + 7 * s, cy - 5.2 * s), (x + .3 * s, cy + .7 * s)]),
              Polygon([(x - .3 * s, cy - .3 * s), (x - 5.8 * s, cy + 4.6 * s), (x - 5.4 * s, cy + 5 * s), (x + .3 * s, cy + .1 * s)])]
    letras = [letra_veleta('N', x + 8.6 * s, cy - 7.4 * s, 4.4 * s), letra_veleta('S', x - 7.2 * s, cy + 6.2 * s, 2.6 * s),
              letra_veleta('E', x + 12.4 * s, cy, 2.6 * s), letra_veleta('O', x - 12.4 * s, cy, 2.6 * s)]
    flecha = [box(x - 9 * s, base - 22.6 * s, x + 7 * s, base - 21.8 * s), Polygon([(x + 6.6 * s, base - 24 * s), (x + 10.4 * s, base - 22.2 * s),
                                                                                 (x + 6.6 * s, base - 20.4 * s)]),
              Polygon([(x - 9.4 * s, base - 24.6 * s), (x - 6.6 * s, base - 22.6 * s), (x - 6.6 * s, base - 21.8 * s), (x - 9.4 * s, base - 19.8 * s),
                       (x - 7.8 * s, base - 22.2 * s)]), ovalo(x, base - 22.2 * s, .9 * s, .9 * s)]
    return l.masa(brazos + letras + flecha, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)


def mar(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    l.mancha(box(-2, -2, 122, 22), GRIS, .3, difuso=4)                   # el cielo gris del norte
    nube(l, 24, 6, 18, .6)
    nube(l, 90, 4.6, 14, .55)
    # el mar del Norte, frío y gris, con mucho oleaje
    horizonte = 19.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, 41.5), GRIS, .45, dentro=m)
    for _ in range(46):
        x, y = rng.uniform(-2, 118), rng.uniform(horizonte + 1, 34)
        l.trazo([(x, y), (x + 1.5, y - .35), (x + 3, y)], .16, color='E2EDE9', alfa=.75)
    # lejos: las grúas del puerto a la izquierda, un buque que sale y un faro a la derecha
    for x, h in ((2.4, 6), (6.4, 7.4), (10.6, 6.4)):
        l.masa([box(x - .3, horizonte - h, x + .3, horizonte), Polygon([(x, horizonte - h), (x + 3, horizonte - h - .6), (x + 3, horizonte - h - .2), (x, horizonte - h + .6)])],
               material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)
    l.masa(forma([(14, horizonte + .4), (18, horizonte - .6), (26, horizonte - .4), (29, horizonte + .6)], 1), material='vientre', alto=.15,
           brillo=0, vientre=0, hondo=0, linea=.25)
    fr = l.masa([forma([(20.4, horizonte - .4), (20.8, 10.4), (23, 10.4), (23.4, horizonte - .4)], 0), box(20, 9.2, 23.8, 10.6)], material='claro',
                alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(box(18, 13, 26, 14.6), '2F8A74', .85, dentro=fr)
    l.masa(Polygon([(85, horizonte + .4), (111, horizonte + .4), (113.4, horizonte - 1.6), (84, horizonte - 1.6)]), material='oscuro', alto=.2,
           brillo=.15, vientre=0, hondo=0, linea=.25)
    for k in range(8):
        l.masa(box(89 + k * 2.6, horizonte - 3.4, 91.4 + k * 2.6, horizonte - 1.5), material=('cuerpo', 'claro', 'lejos')[k % 3], alto=.15,
               brillo=.1, vientre=0, hondo=0, linea=.18)
    l.masa(box(85.6, horizonte - 5.4, 88.6, horizonte - 1.5), material='claro', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.2)
    # el dique de adelante, con su pasto de duna, y la veleta dorada, protagonista: la N del norte
    d = orilla(l, forma([(-2, 41.5), (-2, 33.4), (30, 32), (60, 31.6), (90, 32), (122, 33.4), (122, 41.5)], 2), tinte=.3)
    pasto(l, 0, 120, 33, 40.6, 26, semilla=16, dentro=d)
    veleta(l, 58, 37.6, 1.25)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Basilea', dibujar=basilea), dict(clave='Estrasburgo', dibujar=estrasburgo),
            dict(clave='Maguncia', dibujar=maguncia), dict(clave='Coblenza', dibujar=coblenza), dict(clave='Colonia', dibujar=colonia),
            dict(clave='Duisburgo', dibujar=duisburgo), dict(clave='Rotterdam', dibujar=rotterdam), dict(clave='mar', dibujar=mar)]
LISTO = True
