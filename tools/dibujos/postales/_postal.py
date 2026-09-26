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
    for _ in range(16):
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
