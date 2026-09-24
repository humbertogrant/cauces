# -*- coding: utf-8 -*-
"""Patas, dedos y garras para los dibujos de tools/dibujos/, en unidades de la caja.

Una pata es un tubo que pasa suave por sus articulaciones (hombro, codo, muñeca…), con un radio en cada una; los dedos, tubos
cortos que salen en abanico desde un punto, cada uno con su largo; las garras, triangulitos en la punta de cada dedo.
"""
import math

import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from pintor import tubo


def miembro(articulaciones, radios, n=12):
    return tubo(articulaciones, radios, n)


def dedos(base, grados, largos, abanico=40, grueso=(.45, .3), curva=0.0):
    """Dedos en abanico desde `base`, hacia `grados` (0: adelante, a la derecha; 90: abajo en la caja), abiertos `abanico`
    grados de punta a punta; `curva` los dobla (grados, hacia abajo si es positivo). Devuelve los tubos y sus puntas."""
    b = np.asarray(base, float)
    tubos, puntas = [], []
    k = len(largos)
    for i, L in enumerate(largos):
        a = math.radians(grados + (abanico * (i / (k - 1) - .5) if k > 1 else 0))
        c = math.radians(grados + (abanico * (i / (k - 1) - .5) if k > 1 else 0) + curva)
        m = b + np.array([math.cos(a), math.sin(a)]) * L * .55
        p = m + np.array([math.cos(c), math.sin(c)]) * L * .45
        tubos.append(tubo([b, m, p], [grueso[0], (grueso[0] + grueso[1]) / 2, grueso[1]], 6))
        puntas.append((p, c))
    return tubos, puntas


def garra(punta, grados, largo=.9, ancho=.35):
    """una uña: un triangulito curvo que sigue al dedo"""
    p = np.asarray(punta, float)
    a = math.radians(grados)
    d = np.array([math.cos(a), math.sin(a)])
    e = np.array([-d[1], d[0]])
    return Polygon([p + e * ancho, p + d * largo + e * .05 * largo, p - e * ancho * .6]).buffer(.05)


def peludo(g, largo=1.2, paso=.9, donde=None, semilla=0, hacia=0.0, flujo=None, mezcla=.65):
    """Un contorno con mechones: triangulitos que salen del borde. Sin `flujo` salen derechos hacia afuera, girados `hacia` grados
    (en el sentido del reloj en la caja: en el lomo de un animal que mira a la derecha, positivo levanta el mechón); con `flujo`
    (grados en la caja, 0 a la derecha y 90 hacia abajo, o una función (x, y) -> grados) se acuestan en la dirección en que cae el
    pelo, `mezcla` de cuánto: donde el pelo cae a lo largo del borde quedan dientes de sierra, y donde cae hacia afuera, mechones
    largos. `donde(x, y, nx, ny)` elige en qué partes del borde (nx, ny: la normal hacia afuera); sin él, en todo el borde."""
    rng = np.random.default_rng(semilla)
    borde = g.exterior if g.geom_type == 'Polygon' else max(g.geoms, key=lambda p: p.area).exterior
    L = borde.length
    ext = []
    t = rng.uniform(0, paso)
    while t < L:
        p = np.asarray(borde.interpolate(t).coords[0])
        q = np.asarray(borde.interpolate(min(t + .2, L)).coords[0])
        d = q - p
        if np.hypot(*d) > 0:
            d = d / np.hypot(*d)
            n = np.array([d[1], -d[0]])                     # hacia afuera, si el borde va en sentido antihorario en la caja
            if g.contains(Point(*(p + n * .3))):
                n = -n
            if donde is None or donde(p[0], p[1], n[0], n[1]):
                a = math.radians(hacia)
                nb = np.array([n[0] * math.cos(a) - n[1] * math.sin(a), n[0] * math.sin(a) + n[1] * math.cos(a)])
                if flujo is not None:
                    f = math.radians((flujo(*p) if callable(flujo) else flujo) + rng.normal(0, 8))
                    nb = nb * (1 - mezcla) + np.array([math.cos(f), math.sin(f)]) * mezcla
                    if nb @ n < .12:                           # el pelo que cae hacia adentro no asoma
                        nb = nb + n * (.12 - nb @ n)
                    nb = nb / np.hypot(*nb)
                largo_ = largo * rng.uniform(.6, 1.25)
                ext.append(Polygon([p - d * paso * .55, p + nb * largo_ + d * rng.uniform(-.2, .2), p + d * paso * .55]).buffer(0))
        t += paso * rng.uniform(.7, 1.2)
    return unary_union([g] + ext)


def union(*gs):
    return unary_union([g for g in gs if g is not None and not g.is_empty])


def pata_ungulado(articulaciones, radios, suelo, pie, lejos=False):
    """Una pata de ungulado de articulación en articulación (codo, rodilla, menudillo o babilla, corvejón, menudillo) hasta el
    suelo, y su pie: `pie` es 'casco' (caballo) o 'almohadilla' (camello: dos dedos sobre una almohadilla ancha)."""
    pts = [np.asarray(p, float) for p in articulaciones]
    tramos = [tubo([pts[i], pts[i + 1]], [radios[i], radios[i + 1]], 6) for i in range(len(pts) - 1)]
    x = pts[-1][0] + (1.6 if pie == 'casco' else 1.2)
    y = suelo - (.4 if lejos else 0)
    tramos.append(tubo([pts[-1], (x - .4, y - 2.6)], [radios[-1], radios[-1] * .9], 6))
    if pie == 'casco':
        a = radios[-1] * 1.9
        p = Polygon([(x - a * .5, y - 2.6), (x + a * .45, y - 2.6), (x + a * .75, y), (x - a * .6, y)]).buffer(.15)
    else:
        a = radios[-1] * 2.4
        p = Polygon([(x - a * .55, y - 2.2), (x + a * .5, y - 2.4), (x + a * .9, y - .6), (x + a * .7, y), (x - a * .7, y),
                     (x - a * .8, y - 1)]).buffer(.4).buffer(-.2)
    return tramos, p
