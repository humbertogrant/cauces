# -*- coding: utf-8 -*-
"""Piezas para las barcas de tools/dibujos/barcas/, en unidades de la caja (0 0 120 90, y hacia abajo, proa a la derecha).

Como en el glifo del mapa, el casco va dorado (`acento`: la barca es lo tuyo, lo que dice «estás aquí»), las velas y lo pintado de
blanco van claros (`claro`), los techos, toldos y lo que no es madera van en los verdes, y lo de metal (chimeneas, motores) en tinta
(`oscuro`). Cada barca flota en una franja de agua pintada (`agua`): lo que queda bajo la línea de flotación se ve a través del
agua, y el reflejo y la sombra del casco se pintan encima.
"""
import math

import numpy as np
from shapely.geometry import Polygon

from pintor import forma, ovalo, tubo

RIO = '64C8AA'           # el verde claro de los ríos del mapa
ESPUMA = 'F4FBF7'


def casco(pts, veces=2):
    """un casco: pocas pasadas de redondeo, para que las esquinas de la madera no se vuelvan globos"""
    return forma(pts, veces)


def caja(x0, y0, x1, y1, r=.3):
    """una pieza recta (una cabina, un fardo, una ventana), con las esquinas apenas redondeadas"""
    from shapely.geometry import box
    return box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)).buffer(-r).buffer(r)


def poli(pts, r=.25):
    """un polígono recto, con las esquinas apenas redondeadas"""
    return Polygon(pts).buffer(0).buffer(-r).buffer(r)


def entre(borde_a, borde_b, f):
    """un punto de cada par entre dos bordes (listas de puntos del mismo largo), a la fracción `f` del primero al segundo"""
    a, b = np.asarray(borde_a, float), np.asarray(borde_b, float)
    return [tuple(p) for p in a + (b - a) * f]


def tablas(l, masa, arriba, abajo, n=4, ancho=.16, alfa=.32, desde=.12, hasta=.88):
    """las tablas del casco: `n` líneas entre la borda (`arriba`) y la quilla (`abajo`), que siguen la curva del casco"""
    for k in range(n):
        f = desde + (hasta - desde) * (k + .5) / n
        l.trazo(entre(arriba, abajo, f), [ancho * .6, ancho, ancho, ancho * .6], alfa=alfa, dentro=masa, difuso=.04)


def cuaderna(l, masa, p0, p1, ancho=.14, alfa=.25):
    """una junta vertical entre tablas, o el canto de una cuaderna"""
    l.trazo([p0, p1], [ancho, ancho], alfa=alfa, dentro=masa, difuso=.04)


def palo(l, p0, p1, r0=.7, r1=.5, material='acento', **kw):
    """un palo, una verga o un remo: un tubo fino de madera"""
    kw.setdefault('linea', .5)
    return l.masa(tubo([p0, p1], [r0, r1], 8), material=material, alto=.4, brillo=.2, vientre=0, hondo=0, contraluz=.2, **kw)


def cabo(l, pts, ancho=.14, alfa=.7):
    """un cabo o una cuerda: una línea de tinta fina"""
    l.trazo(pts, ancho, alfa=alfa, difuso=.02)


def vela(l, pts, costuras=(), veces=2, alfa_costura=.3, **kw):
    """una vela: chata, blanca, con sus costuras (listas de pares de puntos)"""
    kw.setdefault('alto', .22)
    kw.setdefault('linea', .6)
    v = l.masa(forma(pts, veces), material='claro', brillo=.15, vientre=0, hondo=0, escalon=.1, contraluz=.15, **kw)
    for a, b in costuras:
        l.trazo([a, b], [.08, .16, .08], color='8EB5AA', alfa=alfa_costura, dentro=v, difuso=.05)
    return v


def vela_cuadrada(l, x, y, ancho, alto, comba=.6, paños=5, material='claro', inflado=.3, **kw):
    """una vela cuadrada vista de costado, colgada de su verga (arriba, en `y`) y centrada en `x`: el pie se curva un poco con el
    viento y los paños van de arriba abajo"""
    x0, x1, y1 = x - ancho / 2, x + ancho / 2, y + alto
    t = np.linspace(0, 1, 9)[1:-1]
    derecha = [(x1 + comba * .5 * math.sin(math.pi * u), y + alto * u) for u in t]
    pie = [(x1 - ancho * u, y1 + comba * math.sin(math.pi * u)) for u in np.linspace(0, 1, 9)]
    izquierda = [(x0 - comba * .5 * math.sin(math.pi * u), y1 - alto * u) for u in t]
    pts = [(x0, y), (x1, y)] + derecha + pie + izquierda
    kw.setdefault('linea', .6)
    v = l.masa(poli(pts, .35), material=material, alto=inflado, brillo=.15, vientre=0, hondo=0, escalon=.1, contraluz=.15, **kw)
    for k in range(1, paños):
        xs = x0 + ancho * k / paños
        l.trazo([(xs, y + .3), (xs + comba * .1, y + alto * .5), (xs, y1 + comba * .8)], [.06, .14, .06], color='8EB5AA', alfa=.4,
                dentro=v, difuso=.05)
    return v


def remo(l, escalamo, grados, largo, pala=3.2, ancho=1.1, material='acento', **kw):
    """un remo que sale del escálamo hacia afuera y abajo (`grados` en la caja: 90 es derecho hacia abajo); la pala al final"""
    a = math.radians(grados)
    d = np.array([math.cos(a), math.sin(a)])
    e = np.array([-d[1], d[0]])
    p0 = np.asarray(escalamo, float) - d * largo * .28
    p1 = p0 + d * largo
    caña = tubo([p0, p1 - d * pala * .8], [.34, .3], 6)
    hoja = forma([p1 - d * pala + e * ancho * .3, p1 - d * pala * .4 + e * ancho * .55, p1 + e * ancho * .45, p1 + d * .3,
                  p1 - e * ancho * .45, p1 - d * pala * .4 - e * ancho * .55, p1 - d * pala - e * ancho * .3], 2)
    kw.setdefault('linea', .4)
    return l.masa([caña, hoja], material=material, alto=.3, brillo=.2, vientre=0, hondo=0, contraluz=.15, **kw)


def paja(l, pts, flujo=100, material='vientre', densidad=5, veces=2, **kw):
    """un techo de paja o de hojas de palma: una masa chata con muchas hebras que caen"""
    kw.setdefault('linea', .6)
    t = l.masa(forma(pts, veces), material=material, alto=.35, brillo=.05, vientre=0, hondo=.1, escalon=.2, contraluz=.2, **kw)
    l.pelaje(t, densidad=densidad, largo=2.2, ancho=.2, alfa=.5, semilla=int(pts[0][0] * 7) % 97, claro=.35, curva=6, desvio=8,
             mechon=2, separa=.3, flujo=flujo)
    return t


def esteras(l, masa, paso=1.4, alfa=.35, color='3D9582'):
    """el tejido de una estera: una trama fina en diagonal, cruzada"""
    x0, y0, x1, y1 = masa.g.bounds
    L = (x1 - x0) + (y1 - y0)
    for k in np.arange(-L, L, paso):
        l.trazo([(x0 + k, y0), (x0 + k + (y1 - y0), y1)], .09, color=color, alfa=alfa, dentro=masa)
        l.trazo([(x0 + k + (y1 - y0), y0), (x0 + k, y1)], .09, color=color, alfa=alfa * .7, dentro=masa)


def cabina(l, x0, y0, x1, y1, ventanas=(), material='claro', techo=None, **kw):
    """una cabina recta con sus ventanas (x, y, ancho, alto) y, si se pide, un techo (`techo`: lo que sobresale a cada lado)"""
    kw.setdefault('linea', .5)
    c = l.masa(caja(x0, y0, x1, y1, .2), material=material, alto=.25, brillo=.1, vientre=0, hondo=0, contraluz=.15, **kw)
    for vx, vy, vw, vh in ventanas:
        l.mancha(caja(vx, vy, vx + vw, vy + vh, .12), '2F8A74', .75, dentro=c)
        l.mancha(caja(vx + vw * .1, vy + vh * .1, vx + vw * .45, vy + vh * .4, .08), 'DAF5D8', .5, dentro=c, difuso=.1)
    if techo is not None:
        l.masa(caja(x0 - techo, y0 - 1.2, x1 + techo, y0 + .2, .2), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0,
               linea=.45)
    return c


def fardo(l, x, y, w, h, material='vientre', ataduras=2, **kw):
    """un fardo o un saco: una pieza redondeada con sus ataduras"""
    kw.setdefault('linea', .4)
    f = l.masa(caja(x, y, x + w, y + h, min(w, h) * .3), material=material, alto=.45, brillo=.08, vientre=0, hondo=0, arroja=False,
               **kw)
    for k in range(ataduras):
        xx = x + w * (k + 1) / (ataduras + 1)
        l.trazo([(xx, y + .2), (xx + .1, y + h - .2)], .14, alfa=.4, dentro=f)
    return f


def rueda(l, cx, cy, r, n=14, material='acento', lejos=False):
    """una rueda de paletas vista de lado: dos aros, los rayos y las paletas anchas, de tablas, que asoman afuera del aro"""
    piezas = [ovalo(cx, cy, r * .98, r * .98).difference(ovalo(cx, cy, r * .98 - .7, r * .98 - .7)),
              ovalo(cx, cy, r * .55, r * .55).difference(ovalo(cx, cy, r * .55 - .6, r * .55 - .6)), ovalo(cx, cy, 1.2, 1.2)]
    for k in range(n):
        a = 2 * math.pi * (k + .5) / n
        d = np.array([math.cos(a), math.sin(a)])
        piezas.append(tubo([(cx, cy), (cx + d[0] * r * .98, cy + d[1] * r * .98)], [.26, .26], 4))
        e = np.array([-d[1], d[0]])
        c = np.array([cx, cy]) + d * r
        piezas.append(Polygon([c + e * .55 - d * r * .42, c + e * .55 + d * .5, c - e * .55 + d * .5, c - e * .55 - d * r * .42]))
    return l.masa(piezas, material='lejos' if lejos else material, alto=.3, brillo=.15, vientre=0, hondo=0, linea=.42)


def chimenea(l, x, y0, y1, r=1.4, corona=True):
    """una chimenea de vapor: un tubo de metal con su corona en la boca"""
    piezas = [tubo([(x, y0), (x, y1)], [r, r], 6)]
    if corona:
        piezas.append(forma([(x - r * 1.7, y1 - .2), (x - r * 1.3, y1 - 1.8), (x + r * 1.3, y1 - 1.8), (x + r * 1.7, y1 - .2),
                             (x + r * .9, y1 + 1.2), (x - r * .9, y1 + 1.2)], 1))
    return l.masa(piezas, material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.5)


def humo(l, x, y, n=4, deriva=(-5, -3.4), r=2.2):
    """el humo que sale de una chimenea y se va con el viento: bocanadas claras que se deshacen"""
    for k in range(n):
        cx, cy = x + deriva[0] * k * .9, y + deriva[1] * k
        l.mancha(ovalo(cx, cy, r * (1 + .35 * k), r * (.8 + .3 * k)), 'B6CEC6', max(.2, .8 - .14 * k), difuso=.3 + .16 * k)
        l.mancha(ovalo(cx - r * .2, cy - r * .25, r * (.7 + .3 * k), r * (.5 + .25 * k)), 'F0F6F4', max(.25, .8 - .14 * k),
                 difuso=.3 + .16 * k)


def motor_fuera(l, x, y, alto_=7, espejo=False):
    """un motor fuera de borda colgado del espejo de popa: la carcasa, la pata y la hélice bajo el agua"""
    s = -1 if espejo else 1
    carcasa = forma([(x - 1.6 * s, y - 1.2), (x + 1.4 * s, y - 1.6), (x + 2.2 * s, y + 1.4), (x + 1.2 * s, y + 3.4),
                     (x - 1.8 * s, y + 3)], 1)
    pata = tubo([(x - .2 * s, y + 3), (x - .6 * s, y + alto_)], [.7, .6], 6)
    helice = forma([(x - 2.2 * s, y + alto_ - .6), (x - .4 * s, y + alto_ - 1.2), (x + .6 * s, y + alto_), (x - .4 * s, y + alto_ + 1),
                    (x - 2 * s, y + alto_ + .8)], 1)
    return l.masa([carcasa, pata, helice], material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.5)


def agua(l, y, x0=2, x1=118, alto_=7, sombra=None):
    """la franja de agua donde flota la barca: tiñe lo que queda bajo la línea de flotación, con la sombra del casco (`sombra`:
    un polígono) y los reflejos de la superficie; se desvanece hacia los costados y hacia abajo"""
    ondas = [(x, y + .35 * math.sin(x / 3.1)) for x in np.arange(x0, x1 + .1, 1)]
    banda = Polygon(ondas + [(x1, y + alto_), (x0, y + alto_)]).buffer(0)
    medio = (x0 + x1) / 2
    l.mancha(banda.intersection(ovalo(medio, y + alto_ * .2, (x1 - x0) * .47, alto_ * 1.05)), RIO, .44, difuso=1.5)
    if sombra is not None:
        l.mancha(sombra, '0C3A33', .22, difuso=.8)
    for k, (a, b, dy) in enumerate(((x0 + 6, medio - 18, .6), (medio + 14, x1 - 8, 1), (medio - 30, medio + 6, 2.6), (x0 + 16, x0 + 34, 3.4),
                                   (x1 - 30, x1 - 12, 4.2))):
        pts = [(x, y + dy + .3 * math.sin(x / 2.2 + k)) for x in np.linspace(a, b, 12)]
        l.trazo(pts, [.06, .26, .26, .06], color=ESPUMA, alfa=.85, difuso=.05)


def olas_fondo(y, x0=2, x1=118):
    """ondas de vectores detrás de la barca, para el FONDO"""
    return ('<path d="M%g %gq4.5-2.4 9 0t9 0t9 0M%g %gq4.5-2.4 9 0t9 0" style="fill:none;stroke:var(--verde-medio);stroke-width:1;'
            'opacity:.45"/>' % (x0, y + 5.2, x1 - 27, y + 6.4))
