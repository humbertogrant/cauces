# -*- coding: utf-8 -*-
"""Qilin, la jirafa (Giraffa), de memoria: el cuello larguísimo (con siete vértebras, como el nuestro, pero enormes) y una crin
corta y tiesa; el lomo que baja de la cruz a la grupa porque las patas de adelante son más largas; en la cabeza, dos osiconos
(cuernos de hueso cubiertos de piel, con un mechón oscuro en la punta) y orejas hacia los lados; la cara larga; el pelaje con
manchas grandes separadas por líneas claras; la cola larga con un penacho oscuro; cascos partidos.
"""
import numpy as np
from shapely.geometry import MultiPoint
from shapely.ops import voronoi_diagram

from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 0, 120, 90)
SUELO = 86.0


def cuerpo():
    return forma([(37.5, 45), (38.5, 39.5), (42, 36.5), (50, 33.5), (57, 30.5), (61.5, 26.5), (65.5, 20), (69.5, 13.5), (72.5, 9.5),
                  (75.5, 7.2), (79, 7.5), (82.6, 10.2), (86, 13.6), (88.4, 16.4), (88.2, 18.6), (85.8, 19.4), (82.2, 18.4),
                  (79, 17.4), (76.8, 18.8), (73.8, 24), (70.5, 30.5), (67, 37.5), (64, 43.5), (62, 48.5), (58, 51), (51, 50.5),
                  (45.5, 50), (42, 49), (39, 47.5)], 3)


def mano(x0, a=0.0):
    """la pata de adelante, larga: el antebrazo, la rodilla (la muñeca), la caña larga, el menudillo y el casco"""
    antebrazo = tubo([(x0, 47.4), (x0 + .4 + a * .3, 56), (x0 + .8 + a * .5, 64.8)], [3.1, 2.4, 1.75])
    rodilla = ovalo(x0 + .9 + a * .5, 65.6, 1.85, 1.6)
    cana = tubo([(x0 + .9 + a * .5, 66.4), (x0 + 1.2 + a * .6, 80)], [1.35, 1.25])
    menudillo = ovalo(x0 + 1.3 + a * .6, 80.6, 1.5, 1.35)
    cuartilla = tubo([(x0 + 1.4 + a * .6, 81), (x0 + 2.6 + a * .7, 83.4)], [1.25, 1.2])
    return [antebrazo, rodilla, cana, menudillo, cuartilla], casco(x0 + 3 + a * .7)


def pata(x0, a=0.0):
    """la de atrás: el muslo y la pierna en cuña hasta el corvejón, en punta hacia atrás; la caña larga"""
    pierna = forma([(x0 - 3.6, 41), (x0 + 2.6, 46.6), (x0 + 4.4, 52.4), (x0 + 3.4, 57), (x0 + 1.4, 62.4), (x0 + .8 + a, 66.2),
                    (x0 - 2.2 + a, 67.4), (x0 - 3.2, 64.4), (x0 - 4.4, 58.4), (x0 - 6.6, 52), (x0 - 7.6, 46)], 3)
    cana = tubo([(x0 - .6 + a, 66.8), (x0 - .3 + a, 80)], [1.4, 1.25])
    menudillo = ovalo(x0 - .2 + a, 80.6, 1.5, 1.35)
    cuartilla = tubo([(x0 - .1 + a, 81), (x0 + 1.1 + a, 83.4)], [1.25, 1.2])
    return [pierna, cana, menudillo, cuartilla], casco(x0 + 1.5 + a)


def casco(x):
    return forma([(x - 1.9, SUELO - 2.6), (x + 1, SUELO - 2.6), (x + 2.3, SUELO - .1), (x - 2.1, SUELO - .1)], 1)


def manchas(masa_poligono):
    """las manchas: celdas de Voronoi sobre el cuerpo, achicadas para que quede la red de líneas claras entre ellas"""
    rng = np.random.default_rng(17)
    x0, y0, x1, y1 = masa_poligono.bounds
    pts = []
    while len(pts) < 70:
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if masa_poligono.buffer(-1).contains(MultiPoint([(x, y)]).geoms[0]):
            pts.append((x, y))
    celdas = voronoi_diagram(MultiPoint(pts), envelope=masa_poligono.buffer(5))
    return [c.buffer(-.42, join_style=2) for c in celdas.geoms]


def dibujar(l):
    for partes, pie in (mano(57, -1), pata(50, 1.2)):
        m = l.masa(partes, material='lejos', alto=.55, brillo=.05, vientre=0, linea=.65, hondo=0)
        l.masa(pie, material='oscuro', alto=.3, brillo=.1, vientre=0, linea=.45, hondo=0)
    cola = tubo([(38.5, 41), (36.6, 50), (35.4, 60)], [.7, .55, .4])
    l.masa([cola], alto=.4, brillo=.05, vientre=0, linea=.5, hondo=0)
    l.masa(forma([(34.6, 59), (36.8, 59.2), (37.2, 64), (35.6, 67.5), (33.8, 64)], 2), material='oscuro', alto=.3, brillo=.1,
           vientre=0, linea=.45, hondo=0)                                                        # el penacho
    manos, casco_m = mano(61)
    patas, casco_p = pata(44.6)
    silueta = [cuerpo()] + manos + patas
    c = l.masa(silueta, brillo=.18, vientre=.4, contraluz=.3, bultos=[(ovalo(81, 12.5, 4.5, 3.5), .35), (ovalo(58, 38, 6, 8), .2)])
    l.pelaje(c, densidad=1, largo=1.1, ancho=.15, alfa=.18, semilla=21, claro=.4, flujo=lambda x, y: 100 if y > 48 else 150)
    from shapely.ops import unary_union
    # las manchas grandes y oscuras, separadas por una red de líneas claras; en las patas se achican y se apagan hacia abajo
    arriba = unary_union([cuerpo()] + [p.intersection(forma([(0, 0), (120, 0), (120, 64), (0, 64)], 1)) for p in manos[:1] + patas[:1]])
    cara = ovalo(82, 13, 8, 6.4, 35)
    for celda in manchas(arriba):
        cy = celda.centroid.y
        l.mancha(celda.difference(cara), '1C6659', .62 if cy < 50 else .45, dentro=c, difuso=.08)
    for m_ in (casco_m, casco_p):
        l.masa(m_, material='oscuro', alto=.3, brillo=.1, vientre=0, linea=.45, hondo=0)
    # la crin corta y tiesa, a lo largo de la nuca
    cr = l.masa(forma([(57.5, 30), (61, 26), (65, 19.5), (69, 13), (72.5, 9), (73.8, 10.6), (70.5, 15.5), (66.6, 22), (62.8, 28.2),
                       (59.4, 31.8)], 2), material='lejos', alto=.3, brillo=.1, vientre=0, linea=.5, hondo=0)
    for f in np.linspace(.05, .95, 12):
        x, y = 58.5 + f * 14.5, 30.5 - f * 21
        l.trazo([(x + .6, y + .6), (x - .6, y - .9)], .16, alfa=.4, dentro=cr)
    # los osiconos con su mechón, las orejas hacia los lados, el ollar y la boca
    for x0, lejos in ((74.4, True), (76.6, False)):
        l.masa([tubo([(x0, 8), (x0 - .4, 3.6)], [.9, .75]), ovalo(x0 - .45, 3.2, 1.1, 1.0)],
               material='lejos' if lejos else 'cuerpo', alto=.4, brillo=.1, vientre=0, linea=.45, hondo=0)
        l.mancha(ovalo(x0 - .45, 3.0, .9, .8), '0C3A33', .75)
    l.masa(forma([(73.2, 10), (69, 8.6), (67.2, 9.8), (69.5, 11.2), (73, 11.6)], 2), alto=.35, brillo=.05, vientre=0, linea=.5, hondo=0)
    l.mancha(ovalo(86.6, 15.4, .75, .4, 35), '0C3A33', .7, dentro=c)
    l.trazo([(85.2, 18.8), (87.6, 18.4)], .22, alfa=.5, dentro=c)


CARA = dict(ojo=[80.6, 11.4], k=1.3, boca=[86.2, 18.6], kb=1.3, giro=10, pb=.7, wb=.6)
CARA['marco'] = [66.0, 1.0, 26, 26]
FONDO = ('<ellipse class="sombra" cx="52" cy="%.1f" rx="28" ry="3.6" style="opacity:.28"/>' % (SUELO + .4)
         + '<path d="M16 88q.3-2.8-1-4.6M18.5 88.4q.2-3 1.4-4.6M92 88q-.3-3 1.2-5M94.4 88.4q0-2.8 1.6-4.4"' + AGUA + '/>')
LISTO = True
