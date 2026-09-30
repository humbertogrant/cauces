# -*- coding: utf-8 -*-
"""Piezas comunes de las postales pintadas de tools/dibujos/postales/: una caja de 120 × 40 (la postal del juego mide 240 × 80), con el
cielo pálido, el sol dorado, la tierra y el río abajo, como la postal de pictogramas, pero pintados; y lo que se repite de una postal a
otra: el reflejo en el agua, las palmeras datileras, los árboles, las montañas y las nubes.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box

from pintor import forma, ovalo, tubo

VISTA = (0, 0, 120, 40)
CIELO = 'E6F3EE'


def cielo(l, sol=(106, 7.4), tarde=0.0):
    """el cielo pálido, un poco más claro arriba, y el sol dorado con su halo; `tarde` lo entibia hacia el horizonte (el atardecer)"""
    l.mancha(box(0, 0, 120, 40), CIELO, 1)
    l.mancha(box(0, 0, 120, 14), 'D2F2DA', .5, difuso=6)
    if tarde:
        l.mancha(box(0, 16, 120, 34), 'F2D48A', tarde, difuso=5)
    if sol:
        l.mancha(ovalo(sol[0], sol[1], 7, 7), 'F2D48A', .35, difuso=2.4)
        l.masa(ovalo(sol[0], sol[1], 3, 3), material='acento', alto=.4, brillo=.3, vientre=0, hondo=0, tinta=False, contraluz=0)


def tierra(l, suelo=31.0, hasta=34.5, desierto=0.0):
    """la franja de tierra; `desierto` la tiñe de dorado"""
    t = l.masa(box(-2, suelo, 122, hasta), material='vientre', alto=.08, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0,
               contraluz=0, arroja=False)
    if desierto:
        l.mancha(box(-2, suelo, 122, hasta), 'E8B952', desierto, dentro=t)
    return t


def fondo(l, suelo=31.0, rio=34.0, sol=(106, 7.4), desierto=0.0):
    """el cielo, el sol y la tierra, hasta donde empieza el río"""
    cielo(l, sol)
    return tierra(l, suelo, rio + .5, desierto)


def rio(l, y=34.0, color='lejos', brillo='64C8AA', ondas='A4DCC4', semilla=1):
    """el río, abajo: verde hondo, con el brillo del cielo arriba y unas ondas claras"""
    agua = Polygon([(x, y + .25 * math.sin(x / 2.6)) for x in np.arange(-2, 122.1, 1)] + [(122, 41), (-2, 41)]).buffer(0)
    a = l.masa(agua, material=color, alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, y, 122, y + 1.4), brillo, .55, dentro=a, difuso=.5)
    rng = np.random.default_rng(semilla)
    for _ in range(16 if y + 2.4 < 39 else 0):                     # una franja angosta no lleva ondas
        x, yy = rng.uniform(2, 116), rng.uniform(y + 1.6, 39)
        l.trazo([(x, yy), (x + 3, yy - .25), (x + 6, yy)], .18, color=ondas, alfa=.7)
    return a


def reflejo(l, g, y, alfa=.3, color='A4DCC4'):
    """el reflejo de una pieza en el agua: su silueta espejada bajo la línea del agua, pálida y cortada en franjas"""
    r = affinity.scale(g, 1, -1, origin=(0, y)).intersection(box(-2, y, 122, 41))
    if r.is_empty:
        return
    for k in np.arange(y + .4, 41, .9):
        l.mancha(r.intersection(box(-2, k, 122, k + .5)), color, alfa * max(0, 1 - (k - y) / 7))


def palmera(l, x, y, alto_=8.0, lado=1, material='cuerpo', datiles=True):
    """una palmera datilera: el tronco con sus anillos, que se curva un poco, y la copa de hojas largas que suben y caen en arco"""
    tope = (x + lado * 1.2, y - alto_)
    t = l.masa(tubo([(x, y), (x + lado * .4, y - alto_ * .5), tope], [.55, .45, .38]), material='lejos', alto=.3, brillo=.1, vientre=0,
               hondo=0, linea=.3)
    for k in np.arange(.1, .95, .12):
        yy = y - alto_ * k
        l.trazo([(x + lado * .4 * k - .5, yy), (x + lado * .4 * k + .5, yy - .2)], .1, alfa=.5, dentro=t)
    hojas = []
    for a in (-170, -145, -118, -62, -35, -10, 20, 160):
        r = math.radians(a)
        d = np.array([math.cos(r), math.sin(r)])
        p0 = np.array(tope)
        p1 = p0 + d * 2.6 + np.array([0, -1.1])
        p2 = p0 + d * 4.8 + np.array([0, .4 + abs(math.cos(r)) * 1.4])
        hojas.append(tubo([p0, p1, p2], [.34, .3, .05], 6))
    l.masa(hojas, material=material, alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3, contraluz=.2)
    if datiles:
        for dx in (-.4, .4):
            l.masa(ovalo(tope[0] + dx, tope[1] + .9, .45, .6), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.2,
                   arroja=False)


def arbol(l, x, y, r=2.6, material='cuerpo', semilla=0):
    """un árbol de copa redonda: el tronco y la copa de tres o cuatro bollos"""
    l.masa(tubo([(x, y - r * .2), (x, y + r * 1.1)], [.35, .3]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25,
           arroja=False)
    copa = [ovalo(x + dx * r, y + dy * r - r * .6, r * rr, r * rr * .9) for dx, dy, rr in ((0, -.2, .62), (-.45, .15, .5), (.45, .12, .52),
                                                                                          (0, .25, .5))]
    return l.masa(copa, material=material, alto=.35, brillo=.12, vientre=0, hondo=.1, linea=.3, contraluz=.25)


def cordillera(l, puntos, material='lejos', nieve=None, linea=.4, alto=.35):
    """una cordillera: el perfil de los picos (de izquierda a derecha, cerrado abajo) y, si se pide, la nieve en las cumbres por
    encima de la altura `nieve`"""
    pts = [(puntos[0][0], 41)] + puntos + [(puntos[-1][0], 41)]
    g = Polygon(pts).buffer(0)
    m = l.masa(g, material=material, alto=alto, brillo=.08, vientre=0, hondo=.1, linea=linea, escalon=.3, contraluz=.3)
    if nieve is not None:
        # la nieve: lo que queda arriba de la línea de nieve, con el borde de abajo quebrado
        limite = Polygon([(-5, -5), (125, -5)] + [(x, nieve + 1.2 * math.sin(x * 1.7) + .8 * math.sin(x * .6)) for x in np.arange(125, -5.1, -.8)])
        n = g.intersection(limite.buffer(0))
        if not n.is_empty:
            l.masa(n, material='claro', alto=.25, brillo=.3, vientre=0, hondo=0, tinta=False, contraluz=.3, arroja=False)
    return m


def nube(l, x, y, w=10.0, alfa=.8):
    """una nube: bollos claros, sin línea"""
    for dx, dy, r in ((-.3, .2, .28), (0, -.1, .34), (.3, .15, .26), (.12, .3, .3), (-.15, .32, .26)):
        l.mancha(ovalo(x + dx * w, y + dy * w * .4, r * w * .7, r * w * .45), 'FFFFFF', alfa, difuso=.3)


def abedul(l, x, y, alto_=9.0, r=2.2, semilla=0):
    """un abedul: el tronco blanco con sus marcas negras y la copa liviana, de hojas chicas"""
    rng = np.random.default_rng(semilla)
    t = l.masa(tubo([(x, y), (x + .3, y - alto_ * .6), (x + .1, y - alto_)], [.42, .34, .2]), material='claro', alto=.3, brillo=.1,
               vientre=0, hondo=0, linea=.3)
    for k in np.arange(.08, .9, .11):
        yy = y - alto_ * k
        l.trazo([(x - .35, yy), (x + rng.uniform(-.1, .35), yy - .15)], .14, alfa=.8, dentro=t)
    copa = [ovalo(x + dx * r, y - alto_ * .74 + dy * r, r * rr, r * rr * 1.3) for dx, dy, rr in ((0, -.5, .62), (-.42, .15, .5),
                                                                                                    (.42, .1, .5), (0, .6, .46))]
    l.masa(copa, material='cuerpo', alto=.3, brillo=.12, vientre=0, hondo=.1, linea=.25, contraluz=.25)


def abeto(l, x, y, alto_=10.0, ancho=4.0, material='lejos'):
    """un abeto: capas de ramas en triángulo, más anchas abajo, sobre un tronco corto"""
    capas = [box(x - .3, y - alto_ * .2, x + .3, y)]
    for k in range(4):
        f = k / 4
        yb = y - alto_ * (.15 + .78 * f)
        w = ancho * (1 - .68 * f) / 2
        capas.append(Polygon([(x - w, yb), (x, yb - alto_ * .36), (x + w, yb)]))
    l.masa(capas, material=material, alto=.3, brillo=.08, vientre=0, hondo=0, linea=.3, contraluz=.2)


def cebolla(x, y, r):
    """una cúpula de cebolla vista de frente: bulbosa, más ancha abajo, y con la punta afilada; (x, y) es donde asienta sobre su
    tambor, `r` su medio ancho"""
    pts = [(x - r * .62, y), (x - r * .98, y - r * .55), (x - r, y - r * 1.05), (x - r * .78, y - r * 1.55), (x - r * .38, y - r * 2),
           (x - r * .12, y - r * 2.45), (x, y - r * 2.8), (x + r * .12, y - r * 2.45), (x + r * .38, y - r * 2), (x + r * .78, y - r * 1.55),
           (x + r, y - r * 1.05), (x + r * .98, y - r * .55), (x + r * .62, y)]
    return forma(pts, 2).union(Polygon([(x - r * .08, y - r * 2.5), (x, y - r * 3.05), (x + r * .08, y - r * 2.5)]))


def iglesia(l, x, base, ancho=9.0, alto_=7.0, cupulas=((0, 1.0),), dorada=0, material='claro', ventanas=3):
    """una iglesia ortodoxa: el cuerpo blanco con sus ventanas en arco, el techo, y los tambores con sus cúpulas de cebolla y su
    cruz; `cupulas`: (corrimiento, escala) de cada una; la de índice `dorada` va dorada y las demás verdes"""
    c = l.masa(box(x - ancho / 2, base - alto_, x + ancho / 2, base).buffer(.15), material=material, alto=.3, brillo=.1, vientre=0,
               hondo=0, linea=.4, escalon=.2, contraluz=.25)
    for k in range(ventanas):
        wx = x - ancho / 2 + ancho * (k + .5) / ventanas
        l.mancha(forma([(wx - .45, base - alto_ * .3), (wx - .45, base - alto_ * .6), (wx, base - alto_ * .72), (wx + .45, base - alto_ * .6),
                        (wx + .45, base - alto_ * .3)], 1), '164F46', .85, dentro=c)
    top = base - alto_
    l.masa(Polygon([(x - ancho / 2 - .5, top), (x - ancho / 2 + 1, top - 1.4), (x + ancho / 2 - 1, top - 1.4), (x + ancho / 2 + .5, top)]).buffer(.1),
           material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    for i, (dx, e) in enumerate(cupulas):
        cx, t = x + dx, top - 1.2
        l.masa(box(cx - 1.1 * e, t - 2.4 * e, cx + 1.1 * e, t + .2).buffer(.08), material=material, alto=.3, brillo=.1, vientre=0, hondo=0,
               linea=.35)
        l.mancha(box(cx - .25 * e, t - 1.9 * e, cx + .25 * e, t - .6 * e), '164F46', .8)
        l.masa(cebolla(cx, t - 2.3 * e, 1.5 * e), material='acento' if i == dorada else 'cuerpo', alto=.5, brillo=.4, vientre=0, hondo=0,
               linea=.35, contraluz=.3)
        tip = t - 2.3 * e - 1.5 * e * 3.05
        l.trazo([(cx, tip + .1), (cx, tip - 1.8 * e)], .12 * e + .08, alfa=.9)
        l.trazo([(cx - .6 * e, tip - 1.15 * e), (cx + .6 * e, tip - 1.15 * e)], .1 * e + .07, alfa=.9)
    return c


def juncos(l, x0, x1, y, alto_=5.0, n=40, semilla=0, espadanas=True, material='cuerpo'):
    """un juncal: tallos finos que se abren un poco, y algunas espadañas con su cabeza oscura"""
    rng = np.random.default_rng(semilla)
    tallos, cabezas = [], []
    for _ in range(n):
        x = rng.uniform(x0, x1)
        h = alto_ * rng.uniform(.5, 1.1)
        a = rng.uniform(-.9, .9)
        tallos.append(tubo([(x, y), (x + a * .4, y - h * .6), (x + a, y - h)], [.2, .15, .05], 4))
        if espadanas and rng.random() < .28:
            cabezas.append(ovalo(x + a * .72, y - h * .74, .32, .95, -a * 10))
    l.masa(tallos, material=material, alto=.15, brillo=.1, vientre=0, hondo=0, linea=.18, arroja=False)
    if cabezas:
        l.masa(cabezas, material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.2, arroja=False)


def ave(l, x, y, s=1.0, alfa=.85):
    """un ave que vuela lejos: dos alas en arco"""
    l.trazo([(x - 2 * s, y + .4 * s), (x - 1 * s, y - .5 * s), (x, y), (x + 1 * s, y - .5 * s), (x + 2 * s, y + .4 * s)],
            [.08 * s, .26 * s, .3 * s, .26 * s, .08 * s], alfa=alfa)


def loto(l, x, y, s=1.0):
    """un loto sobre su hoja redonda y chata, en el agua: los pétalos que se abren hacia arriba y el centro dorado"""
    l.masa(ovalo(x - 1.4 * s, y + .5 * s, 2.6 * s, .7 * s), material='cuerpo', alto=.12, brillo=.2, vientre=0, hondo=0, linea=.3,
           arroja=False)
    petalos = []
    for a in (-60, -30, 0, 30, 60):
        r = math.radians(a - 90)
        d = np.array([math.cos(r), math.sin(r)])
        e = np.array([-d[1], d[0]])
        b = np.array([x, y])
        petalos.append(Polygon([b + e * .5 * s, b + d * 1.5 * s + e * .55 * s, b + d * 2.6 * s, b + d * 1.5 * s - e * .55 * s,
                                b - e * .5 * s]).buffer(.05))
    l.masa(petalos, material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.25, contraluz=.3, arroja=False)
    l.masa(ovalo(x, y - .5 * s, .7 * s, .45 * s), material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2, arroja=False)
