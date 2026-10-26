# -*- coding: utf-8 -*-
"""Piezas comunes de las postales pintadas de tools/dibujos/postales/: una caja de 120 × 40 (la postal del juego mide 240 × 80), con el
cielo pálido, el sol dorado, la tierra y el río abajo, como la postal de pictogramas, pero pintados; y lo que se repite de una postal a
otra: el reflejo en el agua, las palmeras datileras, los árboles, las montañas y las nubes.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from pintor import curva, forma, ovalo, tubo

VISTA = (0, 0, 120, 40)
CIELO = 'E6F3EE'
PIEDRA = 'BF9129'          # la piedra arenisca: el pálido de `vientre` teñido de ocre


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


def cinta(pts, anchos, n=10):
    """una cinta de ancho variable a lo largo de una curva (un río que serpentea, un brazo del delta, un chorro de agua)"""
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
    """la tierra verde: un prado, más amarillo que el agua para que no se confundan"""
    return tierra(l, suelo, hasta, desierto=tinte)


def orilla(l, g, tinte=.24, linea=.35):
    """una orilla de pasto (con más `tinte`, de arena), con su línea"""
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
    """un espejo de agua (un charco, un lago, un brazo de río) con su brillo y unas ondas claras"""
    m = l.masa(g, material=material, alto=.05, brillo=0, vientre=0, hondo=0, linea=linea, tinta=linea > 0, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(g, brillo, .6, dentro=m, difuso=.6)
    rng = np.random.default_rng(semilla)
    x0, y0, x1, y1 = g.bounds
    for _ in range(ondas):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        l.trazo([(x, y), (x + 2, y - .2), (x + 4, y)], .16, color='D2F2DA', alfa=.8, dentro=m)
    return m


def papiro(l, x, y, alto_=6.0, n=7, semilla=0, material='cuerpo'):
    """una mata de papiro: tallos finos que se abren en abanico desde el agua, cada uno con su penacho de hilos, redondo y liviano"""
    rng = np.random.default_rng(semilla)
    tallos, penachos = [], []
    for k in range(n):
        a = ((k + .5) / n - .5) * 1.1 + rng.uniform(-.08, .08)
        h = alto_ * rng.uniform(.75, 1.05)
        tope = (x + math.sin(a) * h * .7, y - math.cos(a) * h)
        tallos.append(tubo([(x + a * .4, y), (x + math.sin(a) * h * .3, y - math.cos(a) * h * .5), tope], [.13, .1, .07], 4))
        penachos.append((tope, a))
    l.masa(tallos, material=material, alto=.15, brillo=.1, vientre=0, hondo=0, linea=.16, arroja=False)
    r = alto_ * .2
    for (px, py), a in penachos:                                         # el penacho: un abanico de hilos finos, sin masa, que se abre
        l.mancha(ovalo(px, py - r * .4, r * .9, r * .55), '6CC8A8', .4, difuso=.2)
        for t in np.linspace(-1.4, 1.4, 11):
            ang = a * .5 + t - math.pi / 2
            fin = (px + math.cos(ang) * r * 1.15, py + math.sin(ang) * r * .9)
            l.trazo([(px, py), ((px + fin[0]) / 2, (py + fin[1]) / 2 - r * .12), fin], [.09, .07, .04], color='1C6659', alfa=.9)


def selva(l, x0, x1, y, alto_=7.0, semilla=0, material='lejos', emergentes=2):
    """la selva: una franja de copas redondas y apretadas que sube y baja, y algunos árboles altos que sobresalen con su copa en
    sombrilla; `y` es el pie de la franja"""
    rng = np.random.default_rng(semilla)
    for _ in range(emergentes):
        ex, h = rng.uniform(x0 + 3, x1 - 3), alto_ * rng.uniform(1.45, 1.8)
        tronco = tubo([(ex, y - alto_ * .4), (ex + .3, y - h + .6)], [.32, .22], 4)
        copa = [ovalo(ex + dx, y - h + dy, rx, ry) for dx, dy, rx, ry in ((0, 0, 2.8, 1.1), (-1.8, .5, 1.7, .9), (1.9, .4, 1.7, .9))]
        l.masa([tronco] + copa, material=material, alto=.3, brillo=.12, vientre=0, hondo=0, linea=.3, contraluz=.3)
    copas, x = [Polygon([(x0, y), (x0 + 1, y - alto_ * .3), (x1 - 1, y - alto_ * .3), (x1, y)])], x0 + alto_ * .3
    while x < x1 - alto_ * .2:                                           # las copas, redondas y grandes, que se tocan
        r = alto_ * rng.uniform(.3, .5)
        copas.append(ovalo(x, y - r * rng.uniform(.6, 1.1), r * 1.15, r))
        x += r * rng.uniform(.9, 1.4)
    g = unary_union(copas)
    m = l.masa(g, material=material, alto=.3, brillo=.08, vientre=0, hondo=0, linea=.3, contraluz=.3)
    for _ in range(int((x1 - x0) * alto_ * .3)):                         # el follaje: manchas más oscuras y más claras
        px, py = rng.uniform(x0, x1), rng.uniform(y - alto_, y)
        l.mancha(ovalo(px, py, rng.uniform(.6, 1.2), rng.uniform(.5, .9)), str(rng.choice(['164F46', '4AA189'])), .35, dentro=m)
    return m


def piramide(l, x, base, ancho, alto_, luz=-1):
    """una pirámide vista un poco de costado: la cara del sol (a la izquierda con `luz` -1), clara, y la de la sombra, más oscura, con
    sus hiladas de piedra"""
    arista = x - luz * ancho * .12                                       # la arista corre hacia el lado de la sombra
    izq = Polygon([(x - ancho / 2, base), (x, base - alto_), (arista, base)])
    der = Polygon([(arista, base), (x, base - alto_), (x + ancho / 2, base)])
    for k, cara in enumerate((izq, der) if luz < 0 else (der, izq)):   # primero la cara del sol, después la de la sombra
        m = l.masa(cara.buffer(.05), material='vientre', alto=.15, brillo=.1 if k == 0 else 0, vientre=0, hondo=0, linea=.35, escalon=0,
                   contraluz=.2 if k == 0 else 0)
        l.mancha(cara, ('E8B952', 'BF9129')[k], (.5, .6)[k], dentro=m)
        for f in np.arange(.12, 1, .12):                                 # las hiladas
            l.trazo([(x - ancho / 2 * (1 - f), base - alto_ * f), (x + ancho / 2 * (1 - f), base - alto_ * f)], .07, color='6B4E10', alfa=.4,
                    dentro=m)
    return izq.union(der)


def obelisco(l, x, base, alto_=10.0, ancho=1.3, punta='acento'):
    """un obelisco: el fuste que se angosta, de piedra clara con sus jeroglíficos, y la punta en pirámide (dorada, si no se pide otro
    `punta`)"""
    w, t = ancho / 2, base - alto_ * .9
    fuste = Polygon([(x - w, base), (x - w * .7, t), (x + w * .7, t), (x + w, base)])
    f = l.masa(fuste.buffer(.05), material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(fuste, 'E8B952', .4, dentro=f)
    for k in np.arange(t + 1.2, base - .6, 1.5):
        l.trazo([(x - .15, k), (x + .15, k + .3)], .1, color='6B4E10', alfa=.5, dentro=f)
    l.masa(Polygon([(x - w * .75, t), (x, base - alto_), (x + w * .75, t)]).buffer(.04), material=punta, alto=.3, brillo=.5, vientre=0,
           hondo=0, linea=.3)
    return fuste


class corrido:
    """un lienzo corrido: lo que se dibuja en él cae `dx`, `dy` más allá; sirve para mover una pieza ya dibujada (el toro alado, las
    ruinas) sin tocar sus números"""

    def __init__(self, l, dx=0.0, dy=0.0):
        self.l, self.dx, self.dy = l, dx, dy

    def _g(self, g):
        if isinstance(g, (list, tuple)):
            return [self._g(p) for p in g]
        return affinity.translate(g, self.dx, self.dy) if hasattr(g, 'geom_type') else g

    def _dentro(self, kw):
        if hasattr(kw.get('dentro'), 'geom_type'):
            kw['dentro'] = self._g(kw['dentro'])
        return kw

    def masa(self, piezas, **kw):
        if kw.get('bultos'):
            kw['bultos'] = [(self._g(b), h) for b, h in kw['bultos']]
        if kw.get('sin_tinta') is not None:
            kw['sin_tinta'] = self._g(kw['sin_tinta'])
        return self.l.masa(self._g(piezas), **kw)

    def trazo(self, pts, anchos, **kw):
        return self.l.trazo([(x + self.dx, y + self.dy) for x, y in pts], anchos, **self._dentro(kw))

    def mancha(self, g, color, alfa=1.0, **kw):
        return self.l.mancha(self._g(g), color, alfa, **self._dentro(kw))

    def pelaje(self, masa, **kw):
        if kw.get('zona') is not None:
            kw['zona'] = self._g(kw['zona'])
        return self.l.pelaje(masa, **kw)


def piedra(l, piezas, tono=.3, linea=.35, alto=.25):
    """piezas de piedra clara, un poco ocre"""
    m = l.masa(piezas, material='vientre', alto=alto, brillo=.1, vientre=0, hondo=0, linea=linea, escalon=.2, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEDRA, tono, dentro=m)
    return m


def casitas(l, x0, x1, base, alto_=4.0, semilla=0, material='claro'):
    """una fila de casas de pueblo, de techo a dos aguas, con sus ventanas"""
    rng = np.random.default_rng(semilla)
    x = x0
    while x < x1:
        w, h = rng.uniform(3, 4.6), alto_ * rng.uniform(.7, 1.1)
        c = l.masa(box(x, base - h, x + w, base).buffer(.05), material=material, alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25,
                   arroja=False)
        for k in range(int(w // 1.4)):
            l.mancha(box(x + .5 + k * 1.4, base - h + 1, x + 1.1 + k * 1.4, base - h + 1.9), '164F46', .75, dentro=c)
        l.masa(Polygon([(x - .3, base - h), (x + w / 2, base - h - w * .45), (x + w + .3, base - h)]), material='lejos', alto=.2, brillo=.15,
               vientre=0, hondo=0, linea=.25, arroja=False)
        x += w + rng.uniform(.2, 1.2)


def cebolla_baja(x, y, r):
    """el chapitel barroco de una torre de pueblo: una cebolla chica con su aguja"""
    pts = [(x - r, y), (x - r * 1.05, y - r * .7), (x - r * .5, y - r * 1.4), (x - r * .2, y - r * 1.9), (x, y - r * 2.6),
           (x + r * .2, y - r * 1.9), (x + r * .5, y - r * 1.4), (x + r * 1.05, y - r * .7), (x + r, y)]
    return forma(pts, 1)
