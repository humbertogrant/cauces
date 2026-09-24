# -*- coding: utf-8 -*-
"""Pintor: los animales de la edición amplia, dibujados de memoria y pixel por pixel (ver «Ilustraciones» en CLAUDE.md).

Cada animal es un archivo de tools/dibujos/ (<clave>.py) que arma el cuerpo con piezas en la caja del juego (0 0 120 90, y hacia
abajo, mirando a la derecha): formas de puntos, tubos a lo largo de un eje con su radio, y óvalos. Las piezas se juntan en masas
que se pintan de atrás hacia adelante (la pata lejana, el cuerpo, la pata cercana), cada una con su línea de tinta, que es más
gruesa del lado de la sombra y se desvanece donde una pata nace del cuerpo. Cada masa se infla como un globo: su altura sale de
la ecuación de Poisson sobre el contorno (un disco da media esfera; una tira larga, medio cilindro), más los bultos que la
esculpen (una mejilla, una rodilla), y la luz, de las normales de esa altura: viene de arriba, adelante y de frente, como la
sombra de las ilustraciones de vectores, y se lleva a la paleta del juego con una rampa por material (verde claro para el
cuerpo, verde medio para lo lejano, blanco, tinta y dorado), con las sombras corridas hacia el azul y las luces hacia el amarillo,
un escalón suave entre sombra, medio tono y luz, y un filo de contraluz en los bordes de arriba. Las masas de adelante echan sombra
sobre las de atrás. Encima van el pelo (`pelaje`: pinceladas finas que siguen su flujo y oscurecen o aclaran lo ya pintado), la piel
agrietada (`grietas`), las manchas y los trazos de cada dibujo, y una cuenca suave donde irá cada ojo.

La cara no se pinta: el ojo y la boca los dibuja caraDe en el motor, encima de la imagen y según el ánimo (normal, alegre,
sorpresa, dormido, pensativo), con los datos de `CARA`. El fondo (`FONDO`, el lugar donde vive) es de vectores, como antes.

python tools/pintor.py [clave …]   pinta y guarda tools/dibujos/salida/<clave>.webp, .json y dos vistas previas (todas sin claves)
"""
import importlib
import io
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import sparse
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.sparse.linalg import spsolve
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

AQUI = os.path.dirname(os.path.abspath(__file__))
DIBUJOS = os.path.join(AQUI, 'dibujos')
SALIDA = os.path.join(DIBUJOS, 'salida')
PX, SS, K = 10, 3, 5          # pixeles por unidad al pintar; sobremuestreo de los bordes; pixeles por unidad de la malla de Poisson
ANCHO_WEBP, CALIDAD = 680, 84  # la ficha mide 340 px de ancho: el doble, para pantallas de alta densidad
LINEA = .85                    # la línea de tinta, en unidades de la caja (la de vectores mide 1,1 de centro a centro)
CORRIDA = (-.26, .3)           # la línea engorda hacia abajo y atrás, del lado de la sombra

# el agua y el trazo tenue de los fondos, como en tools/ilustraciones/ilustraciones_datos.py
AGUA = ' style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.55"'
TENUE = ' style="stroke-width:.7;opacity:.5"'


def hx(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


TINTA = hx('0C3A33')
BLANCO = hx('FFFFFF')
CLARO_PELO = hx('D2F2DA')     # hacia dónde aclara una pincelada clara del pelaje

# rampas de luz por material: de la sombra más honda al brillo
RAMPAS = {
    # las sombras corridas hacia el azul y las luces hacia el amarillo, sin salir del verde: el volumen se lee más rico
    'cuerpo': [(0, '11443F'), (.2, '1C6659'), (.4, '2F8A74'), (.58, '4EB196'), (.74, '6CC8A8'), (.88, '9BDDBD'), (1, 'DAF5D8')],
    'vientre': [(0, '256F66'), (.2, '3D9582'), (.4, '5FB59D'), (.58, '8BD0B9'), (.74, 'A9E0CB'), (.88, 'C6EEDC'), (1, 'EAF9EC')],
    'lejos': [(0, '0D3530'), (.2, '164F46'), (.4, '246E61'), (.58, '368B78'), (.74, '4AA189'), (.88, '6BB9A0'), (1, 'A4DCC4')],
    'claro': [(0, '9DB9B0'), (.2, 'B6CEC6'), (.4, 'CFE0DA'), (.58, 'E2EDE9'), (.74, 'F0F6F4'), (.88, 'FAFCFB'), (1, 'FFFFFF')],
    'oscuro': [(0, '05201C'), (.25, '0A302A'), (.45, '0C3A33'), (.62, '154A41'), (.78, '245E53'), (.9, '3E7A6D'), (1, '6FA497')],
    'acento': [(0, '6B4E10'), (.2, '93701A'), (.4, 'BF9129'), (.58, 'DDAD45'), (.74, 'E8B952'), (.88, 'F2D48A'), (1, 'FBEFCB')],
}
_RAMPAS = {k: (np.array([a for a, _ in v], np.float32), np.array([hx(c) for _, c in v])) for k, v in RAMPAS.items()}

LUZ = np.array([.35, -.8, .5])          # de arriba (y negativa), adelante (x positiva) y de frente
LUZ = LUZ / np.linalg.norm(LUZ)
MEDIA = LUZ + np.array([0, 0, 1.0])
MEDIA = MEDIA / np.linalg.norm(MEDIA)
ARROJA = (-.55, .75)                    # hacia dónde cae la sombra que una masa echa sobre las de atrás
ARRIBA = np.array([-.3, -1.0, 0])       # el contraluz: un filo claro en los bordes de arriba
ARRIBA = ARRIBA / np.linalg.norm(ARRIBA)


def rampa(q, material):
    xs, cs = _RAMPAS[material]
    return np.stack([np.interp(q, xs, cs[:, i]) for i in range(3)], -1).astype(np.float32)


def suave(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------------------------------------ geometría (unidades de la caja)
def chaikin(p, veces=3, cerrado=True):
    """Redondea un polígono de control cortando esquinas; abierto, conserva los extremos."""
    p = np.asarray(p, float)
    for _ in range(veces):
        if cerrado:
            q = np.roll(p, -1, 0)
            n = np.empty((2 * len(p), 2))
            n[0::2] = .75 * p + .25 * q
            n[1::2] = .25 * p + .75 * q
        else:
            a, b = p[:-1], p[1:]
            n = np.empty((2 * len(a), 2))
            n[0::2] = .75 * a + .25 * b
            n[1::2] = .25 * a + .75 * b
            n = np.vstack([p[:1], n, p[-1:]])
        p = n
    return p


def curva(pts, n=14):
    """Curva suave que pasa por todos los puntos (Catmull-Rom centrípeta), abierta."""
    p = np.asarray(pts, float)
    if len(p) == 2:
        return np.linspace(p[0], p[1], n + 1)
    e = np.vstack([2 * p[0] - p[1], p, 2 * p[-1] - p[-2]])
    out = []
    for i in range(1, len(e) - 2):
        p0, p1, p2, p3 = e[i - 1], e[i], e[i + 1], e[i + 2]
        t0 = 0.0
        t1 = t0 + np.linalg.norm(p1 - p0) ** .5 + 1e-6
        t2 = t1 + np.linalg.norm(p2 - p1) ** .5 + 1e-6
        t3 = t2 + np.linalg.norm(p3 - p2) ** .5 + 1e-6
        t = np.linspace(t1, t2, n, endpoint=False)[:, None]
        a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
        b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
        out.append((t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2)
    out.append(p[-1:])
    return np.vstack(out)


def forma(pts, veces=3):
    """Un contorno cerrado a partir de puntos de control, redondeado."""
    return Polygon(chaikin(pts, veces)).buffer(0)


def tubo(eje, radios, n=14):
    """Un tubo a lo largo de una curva suave que pasa por `eje`, con el radio de `radios` (uno por punto) interpolado."""
    e = np.asarray(eje, float)
    c = curva(e, n)
    r = np.interp(np.linspace(0, len(e) - 1, len(c)), np.arange(len(e)), np.asarray(radios, float))
    piezas = [unary_union([Point(c[i]).buffer(r[i], 20), Point(c[i + 1]).buffer(r[i + 1], 20)]).convex_hull for i in range(len(c) - 1)]
    return unary_union(piezas)


def ovalo(cx, cy, rx, ry, ang=0):
    return affinity.rotate(affinity.scale(Point(cx, cy).buffer(1, 48), rx, ry), ang, origin=(cx, cy))


def lazo(pts, anchos, n=10):
    """Un trazo de ancho variable (en unidades) a lo largo de una curva suave: pinceladas de tinta, pliegues, dedos."""
    c = curva(pts, n) if len(pts) > 2 else np.asarray(pts, float)
    a = np.interp(np.linspace(0, 1, len(c)), np.linspace(0, 1, len(np.atleast_1d(anchos))), np.atleast_1d(np.asarray(anchos, float)))
    piezas = [unary_union([Point(c[i]).buffer(a[i] / 2, 10), Point(c[i + 1]).buffer(a[i + 1] / 2, 10)]).convex_hull for i in range(len(c) - 1)]
    return unary_union(piezas)


def anillo(g, ancho=LINEA, corrida=CORRIDA):
    """La línea de tinta de una masa: centrada en el borde y más gruesa del lado de la sombra."""
    fuera = g.buffer(ancho / 2, 16)
    if corrida != (0, 0):
        fuera = unary_union([fuera, affinity.translate(fuera, *corrida)])
    return fuera.difference(g.buffer(-ancho / 2, 16))


def _poligonos(g):
    if g is None or g.is_empty:
        return []
    if g.geom_type == 'Polygon':
        return [g]
    return [p for h in getattr(g, 'geoms', []) for p in _poligonos(h)]


# ------------------------------------------------------------------------------------------------ volumen
def poisson(mascara):
    """u con laplaciano −1 dentro de la máscara y 0 fuera, en pixeles de la malla (la máscara trae un borde vacío)."""
    ny, nx = mascara.shape
    ys, xs = np.nonzero(mascara)
    n = len(ys)
    if not n:
        return np.zeros(mascara.shape)
    idx = -np.ones(mascara.shape, np.int64)
    idx[ys, xs] = np.arange(n)
    filas, cols, vals = [np.arange(n)], [np.arange(n)], [np.full(n, 4.0)]
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = ys + dy, xs + dx
        vec = idx[np.clip(yy, 0, ny - 1), np.clip(xx, 0, nx - 1)]
        vec[(yy < 0) | (yy >= ny) | (xx < 0) | (xx >= nx)] = -1
        m = vec >= 0
        filas.append(np.nonzero(m)[0])
        cols.append(vec[m])
        vals.append(np.full(m.sum(), -1.0))
    A = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(filas), np.concatenate(cols))), shape=(n, n))
    u = np.zeros(mascara.shape)
    u[ys, xs] = spsolve(A.tocsc(), np.ones(n))
    return u


class Masa:
    """Una parte del animal que se pinta de una vez: sus piezas se funden en un solo volumen con una sola línea."""

    def __init__(self, piezas, material='cuerpo', alto=1.0, bultos=(), brillo=.18, vientre=.5, raices=(), linea=LINEA,
                 tinta=True, arroja=True, textura=None, hondo=.35, sin_tinta=None, funde=None, escalon=.3, contraluz=.3):
        """`sin_tinta`: un polígono donde la línea no va (el corte del pedúnculo sobre la aleta de la cola). `funde`: si en las
        `raices` también el color se funde con el cuerpo (una aleta delgada, sí; una pata gruesa, no: por defecto, según `alto`)."""
        self.g = unary_union([p for p in (piezas if isinstance(piezas, (list, tuple)) else [piezas])]).buffer(0)
        self.material, self.alto, self.bultos = material, alto, list(bultos)
        self.brillo, self.vientre, self.raices, self.linea = brillo, vientre, list(raices), linea
        self.tinta, self.arroja, self.textura, self.hondo, self.sin_tinta = tinta, arroja, textura, hondo, sin_tinta
        self.funde = alto <= .45 if funde is None else funde
        self.escalon, self.contraluz = escalon, contraluz       # el escalón suave entre luz y sombra; el filo claro de arriba


class Lienzo:
    def __init__(self, vista):
        self.vx, self.vy, self.vw, self.vh = vista
        self.W, self.H = int(round(self.vw * PX)), int(round(self.vh * PX))
        cols, filas = np.meshgrid(np.arange(self.W), np.arange(self.H))
        self.X = (self.vx + (cols + .5) / PX).astype(np.float32)
        self.Y = (self.vy + (filas + .5) / PX).astype(np.float32)
        self.rgb = np.zeros((self.H, self.W, 3), np.float32)      # color premultiplicado
        self.alfa = np.zeros((self.H, self.W), np.float32)
        self.ops = []

    # ---------------------------------------------------------------- lo que arma un dibujo
    def masa(self, piezas, **kw):
        m = Masa(piezas, **kw)
        self.ops.append(('masa', m))
        return m

    def trazo(self, pts, anchos, color=TINTA, alfa=1.0, dentro=None, difuso=0.0):
        """Una pincelada: `dentro` (una masa o un polígono) la recorta; `difuso` la suaviza (en unidades)."""
        self.ops.append(('forma', lazo(pts, anchos), color, alfa, dentro, difuso))

    def mancha(self, poligono, color, alfa=1.0, dentro=None, difuso=0.0):
        """Un parche de color plano sobre lo ya pintado (una marca del pelaje, la protuberancia del cisne)."""
        self.ops.append(('forma', poligono, color, alfa, dentro, difuso))

    def pelaje(self, masa, densidad=1.0, largo=1.5, ancho=.2, flujo=200.0, alfa=.22, semilla=0, curva=12.0, zona=None, claro=.45,
               oscuro=None, clarito=None, mechon=1, separa=.32, desvio=9.0):
        """El pelo: pinceladas cortas y afinadas que siguen el flujo del pelaje (`flujo`: grados en la caja, 0 a la derecha y 90
        hacia abajo, o una función (x, y) -> grados), unas oscuras y otras claras (`claro`: la fracción de claras), dentro de la
        masa (o de `zona`). `densidad`: mechones por unidad cuadrada; cada mechón tiene `mechon` pelos casi paralelos, separados
        `separa`, para el pelo largo. Sin `oscuro` ni `clarito`, las pinceladas oscurecen o aclaran el color que ya está pintado (el
        pelo de la sombra sigue en la sombra); con un color, lo pintan encima."""
        import shapely
        g = masa.g if zona is None else zona.intersection(masa.g)
        if g.is_empty:
            return
        rng = np.random.default_rng(semilla)
        x0, y0, x1, y1 = g.bounds
        n = max(int(g.area * densidad), 1)
        xs, ys = rng.uniform(x0, x1, n * 4), rng.uniform(y0, y1, n * 4)
        ok = shapely.contains_xy(g, xs, ys)
        osc, cla = [], []
        for x, y in list(zip(xs[ok], ys[ok]))[:n]:
            a0 = (flujo(x, y) if callable(flujo) else flujo) + rng.normal(0, desvio)
            lado = cla if rng.random() < claro else osc
            for j in range(mechon):
                a = math.radians(a0 + rng.normal(0, 3) * (mechon > 1))
                d = np.array([math.cos(a), math.sin(a)])
                e = np.array([-d[1], d[0]])
                L = largo * rng.uniform(.7, 1.3)
                c = rng.normal(0, curva) / 100 * L
                w = ancho * rng.uniform(.8, 1.2)
                p0 = np.array([x, y]) + e * separa * (j - (mechon - 1) / 2) + d * rng.uniform(-.2, .2) * largo
                p1 = p0 + d * L * .5 + e * c
                p2 = p0 + d * L
                lado.append([p0 + e * w / 2, p1 + e * w * .35, p2, p1 - e * w * .35, p0 - e * w / 2])
        self.ops.append(('trazos', osc, oscuro or 'oscurece', alfa, masa))
        self.ops.append(('trazos', cla, clarito or 'aclara', alfa * .8, masa))

    def grietas(self, masa, densidad=.5, ancho=.12, alfa=.3, semilla=0, zona=None):
        """La piel gruesa y agrietada (elefante, hipopótamo): una red fina de líneas entre celdas irregulares, que oscurece lo
        que ya está pintado. `densidad`: celdas por unidad cuadrada."""
        import shapely
        from shapely.geometry import MultiPoint
        from shapely.ops import voronoi_diagram
        g = masa.g if zona is None else zona.intersection(masa.g)
        if g.is_empty:
            return
        rng = np.random.default_rng(semilla)
        x0, y0, x1, y1 = g.bounds
        n = max(int(g.area * densidad), 3)
        xs, ys = rng.uniform(x0, x1, n * 3), rng.uniform(y0, y1, n * 3)
        ok = shapely.contains_xy(g, xs, ys)
        pts = list(zip(xs[ok], ys[ok]))[:n]
        polis = []
        for celda in voronoi_diagram(MultiPoint(pts), envelope=g.buffer(2)).geoms:
            c = np.asarray(celda.exterior.coords)
            for a, b in zip(c[:-1], c[1:]):
                d = b - a
                L = np.hypot(*d)
                if L < 1e-6:
                    continue
                e = np.array([-d[1], d[0]]) / L * ancho * rng.uniform(.6, 1.3) / 2
                polis.append([a + e, b + e, b - e, a - e])
        self.ops.append(('trazos', polis, 'oscurece', alfa, masa))

    def cuenca(self, x, y, k):
        """Una sombra suave alrededor de donde caraDe dibuja el ojo, para que se asiente en la cara."""
        self.ops.append(('cuenca', x, y, k))

    # ---------------------------------------------------------------- raster
    def a_px(self, x, y):
        return (np.asarray(x) - self.vx) * PX, (np.asarray(y) - self.vy) * PX

    def cobertura(self, g):
        """Qué fracción de cada pixel cubre `g` (bordes suaves por sobremuestreo), en todo el lienzo."""
        out = np.zeros((self.H, self.W), np.float32)
        ps = _poligonos(g)
        if not ps:
            return out
        x0, y0, x1, y1 = unary_union(ps).bounds
        c0 = max(int(math.floor((x0 - self.vx) * PX)) - 2, 0)
        r0 = max(int(math.floor((y0 - self.vy) * PX)) - 2, 0)
        c1 = min(int(math.ceil((x1 - self.vx) * PX)) + 2, self.W)
        r1 = min(int(math.ceil((y1 - self.vy) * PX)) + 2, self.H)
        if c1 <= c0 or r1 <= r0:
            return out
        img = Image.new('L', ((c1 - c0) * SS, (r1 - r0) * SS), 0)
        d = ImageDraw.Draw(img)
        for p in ps:
            for k, anillo_ in enumerate([p.exterior] + list(p.interiors)):
                xy = [(((x - self.vx) * PX - c0) * SS, ((y - self.vy) * PX - r0) * SS) for x, y in anillo_.coords]
                d.polygon(xy, fill=0 if k else 255)
        a = np.asarray(img, np.float32).reshape(r1 - r0, SS, c1 - c0, SS).mean(axis=(1, 3)) / 255
        out[r0:r1, c0:c1] = a
        return out

    def cobertura_lista(self, polis):
        """Como `cobertura`, para muchos polígonos chicos a la vez (listas de puntos), sin unirlos."""
        out = np.zeros((self.H, self.W), np.float32)
        if not polis:
            return out
        todos = np.vstack([np.asarray(p, float) for p in polis])
        c0 = max(int(math.floor((todos[:, 0].min() - self.vx) * PX)) - 2, 0)
        r0 = max(int(math.floor((todos[:, 1].min() - self.vy) * PX)) - 2, 0)
        c1 = min(int(math.ceil((todos[:, 0].max() - self.vx) * PX)) + 2, self.W)
        r1 = min(int(math.ceil((todos[:, 1].max() - self.vy) * PX)) + 2, self.H)
        if c1 <= c0 or r1 <= r0:
            return out
        img = Image.new('L', ((c1 - c0) * SS, (r1 - r0) * SS), 0)
        d = ImageDraw.Draw(img)
        for p in polis:
            d.polygon([(((x - self.vx) * PX - c0) * SS, ((y - self.vy) * PX - r0) * SS) for x, y in p], fill=255)
        out[r0:r1, c0:c1] = np.asarray(img, np.float32).reshape(r1 - r0, SS, c1 - c0, SS).mean(axis=(1, 3)) / 255
        return out

    def altura(self, g, alto=1.0, bulto=False):
        """La altura del volumen inflado sobre el contorno `g`, en unidades, en todo el lienzo. Un `bulto` (lo que se suma encima
        para esculpir una mejilla o una rodilla) sube suave desde su borde, sin escalón: si no, dibujaría un disco."""
        out = np.zeros((self.H, self.W), np.float32)
        ps = _poligonos(g)
        if not ps:
            return out
        x0, y0, x1, y1 = unary_union(ps).bounds
        ox, oy = x0 - 1, y0 - 1
        nx, ny = int(math.ceil((x1 - x0 + 2) * K)), int(math.ceil((y1 - y0 + 2) * K))
        img = Image.new('L', (nx, ny), 0)
        d = ImageDraw.Draw(img)
        for p in ps:
            for k, anillo_ in enumerate([p.exterior] + list(p.interiors)):
                d.polygon([((x - ox) * K, (y - oy) * K) for x, y in anillo_.coords], fill=0 if k else 1)
        u = poisson(np.asarray(img) > 0)
        c0 = max(int(math.floor((x0 - self.vx) * PX)) - 2, 0)
        r0 = max(int(math.floor((y0 - self.vy) * PX)) - 2, 0)
        c1 = min(int(math.ceil((x1 - self.vx) * PX)) + 2, self.W)
        r1 = min(int(math.ceil((y1 - self.vy) * PX)) + 2, self.H)
        if c1 <= c0 or r1 <= r0:
            return out
        X, Y = self.X[r0:r1, c0:c1], self.Y[r0:r1, c0:c1]
        uu = np.clip(map_coordinates(u, [(Y - oy) * K - .5, (X - ox) * K - .5], order=3, mode='constant', cval=0), 0, None)
        if bulto:
            t = np.clip(uu / max(u.max(), 1e-9), 0, 1)
            out[r0:r1, c0:c1] = 2 * alto / K * math.sqrt(u.max()) * t * t * (3 - 2 * t)
        else:
            out[r0:r1, c0:c1] = 2 * alto / K * np.sqrt(uu)
        return out

    # ---------------------------------------------------------------- pintar
    def pintar(self, grano=.016):
        masas = [op[1] for op in self.ops if op[0] == 'masa']
        cob = {id(m): self.cobertura(m.g) for m in masas}
        rng = np.random.default_rng(11)
        ruido = gaussian_filter(rng.standard_normal((self.H, self.W)).astype(np.float32), 1.2) * grano
        for i, op in enumerate(self.ops):
            if op[0] == 'masa':
                m = op[1]
                a = cob[id(m)]
                if not a.any():
                    continue
                col = self._sombrear(m, a)
                # la sombra que echan las masas de adelante
                delante = [self._raiz(o[1], cob[id(o[1])]) for o in self.ops[i + 1:] if o[0] == 'masa' and o[1].arroja]
                if delante:
                    s = np.max(delante, axis=0)
                    dx, dy = int(round(ARROJA[0] * PX)), int(round(ARROJA[1] * PX))
                    s = gaussian_filter(np.roll(np.roll(s, dy, 0), dx, 1), .55 * PX)
                    col *= (1 - .3 * s)[..., None]
                col = np.clip(col * (1 + ruido[..., None]), 0, 1)
                for (x, y, d0, d1) in (m.raices if m.funde else ()):      # donde una aleta nace del cuerpo, el color se funde con él
                    a = a * suave(.15 * d1, .85 * d1, np.hypot(self.X - x, self.Y - y))
                self._componer(col, a)
                if m.tinta:
                    r = anillo(m.g, m.linea)
                    t = self.cobertura(r.difference(m.sin_tinta) if m.sin_tinta is not None else r)
                    for (x, y, d0, d1) in m.raices:
                        t *= suave(d0, d1, np.hypot(self.X - x, self.Y - y))
                    self._componer(TINTA, t)
            elif op[0] == 'trazos':
                _, polis, color, alfa, dentro = op
                a = np.clip(self.cobertura_lista(polis) * cob[id(dentro)] * alfa, 0, 1)[..., None]
                if color == 'oscurece':                   # el pelo oscuro: el mismo color de abajo, más hondo
                    self.rgb = self.rgb * (1 - .62 * a)
                elif color == 'aclara':                   # el claro: el de abajo, con más luz (en la sombra, poca)
                    luz = (self.rgb @ np.array([.3, .59, .11], np.float32)) / np.maximum(self.alfa, 1e-4)
                    meta = CLARO_PELO * self.alfa[..., None]
                    self.rgb = self.rgb + (meta - self.rgb) * a * (.15 + .7 * np.clip(luz, 0, 1))[..., None]
                else:
                    self._componer(hx(color), a[..., 0])
            elif op[0] == 'cuenca':
                _, x, y, k = op
                r = np.hypot(self.X - x, self.Y - y) / k
                todo = np.max([cob[id(mm)] for mm in masas], axis=0)
                self._componer(TINTA, .16 * np.exp(-((r - 1.25) / .45) ** 2) * (r > .9) * todo)
            else:
                _, g, color, alfa, dentro, difuso = op
                a = self.cobertura(g)
                if difuso:
                    a = gaussian_filter(a, difuso * PX)
                if dentro is not None:
                    a *= cob[id(dentro)] if isinstance(dentro, Masa) else self.cobertura(dentro)
                self._componer(hx(color) if isinstance(color, str) else np.asarray(color, np.float32), a * alfa)

    def _raiz(self, m, a):
        """La cobertura de una masa con su color fundido en las raíces (como se pinta): así la sombra que echa no oscurece
        el cuerpo justo donde la aleta o la pata se funde con él."""
        for (x, y, d0, d1) in (m.raices if m.funde else ()):
            a = a * suave(.15 * d1, .85 * d1, np.hypot(self.X - x, self.Y - y))
        return a

    def _componer(self, color, a):
        a = np.clip(a, 0, 1)
        self.rgb = self.rgb * (1 - a[..., None]) + np.asarray(color, np.float32) * a[..., None]
        self.alfa = self.alfa + a * (1 - self.alfa)

    def _sombrear(self, m, a):
        h = self.altura(m.g, m.alto)
        for pol, alto in m.bultos:
            h = h + self.altura(pol.intersection(m.g), alto, bulto=True)
        gy, gx = np.gradient(h, 1 / PX)
        n = np.stack([-gx, -gy, np.ones_like(h)], -1)
        n /= np.linalg.norm(n, axis=-1, keepdims=True)
        q = np.clip((n @ LUZ + .32) / 1.32, 0, 1)
        if m.escalon:                                       # tres tonos que se funden: sombra, medio y luz, como un dibujo pintado
            q = q * (1 - m.escalon) + (.42 * suave(.33, .45, q) + .58 * suave(.62, .74, q)) * m.escalon
        col = rampa(q, m.material)
        if m.vientre and m.material == 'cuerpo':           # contrasombreado: lo que mira hacia abajo, más pálido
            w = (m.vientre * suave(.05, .6, n[..., 1]))[..., None]
            col = col * (1 - w) + rampa(q, 'vientre') * w
        if m.brillo:
            col = col + (1 - col) * (m.brillo * np.clip(n @ MEDIA, 0, 1) ** 24)[..., None]
        if m.contraluz:                                     # un filo claro donde el volumen se da vuelta hacia arriba
            filo = np.clip(1 - n[..., 2], 0, 1) ** 1.6 * np.clip(n @ ARRIBA, 0, 1)
            col = col + (1 - col) * (m.contraluz * filo)[..., None]
        if m.hondo:                                         # los hundidos (donde el cuello entra en la cabeza) se oscurecen
            hundido = np.clip((gaussian_filter(h, 1.2 * PX) - h) / 2.5, 0, 1)
            col = col * (1 - m.hondo * hundido)[..., None]
        if m.textura:
            col = m.textura(self, col, h, n)
        return col

    # ---------------------------------------------------------------- salida
    def imagen(self):
        c = np.where(self.alfa[..., None] > 0, self.rgb / np.maximum(self.alfa[..., None], 1e-4), 0)
        rgba = np.dstack([np.clip(c, 0, 1), np.clip(self.alfa, 0, 1)])
        return Image.fromarray((rgba * 255 + .5).astype(np.uint8), 'RGBA')


def _rejilla(img, vista, cara):
    """Vista previa para ubicar piezas: el animal sobre blanco, la rejilla cada 10 unidades y el ojo y la boca de caraDe, aproximados."""
    vx, vy, vw, vh = vista
    fondo = Image.new('RGBA', img.size, (255, 255, 255, 255))
    fondo.alpha_composite(img)
    d = ImageDraw.Draw(fondo)
    for x in range(int(math.ceil(vx / 10)) * 10, int(vx + vw) + 1, 10):
        d.line([((x - vx) * PX, 0), ((x - vx) * PX, img.size[1])], fill=(200, 60, 60, 255), width=1)
        d.text(((x - vx) * PX + 3, 2), str(x), fill=(200, 60, 60, 255))
    for y in range(int(math.ceil(vy / 10)) * 10, int(vy + vh) + 1, 10):
        d.line([(0, (y - vy) * PX), (img.size[0], (y - vy) * PX)], fill=(200, 60, 60, 255), width=1)
        d.text((3, (y - vy) * PX + 2), str(y), fill=(200, 60, 60, 255))
    if cara:
        k = cara.get('k', 2)
        for o in [cara['ojo']] + ([cara['ojo2']] if cara.get('ojo2') else []):
            x, y = (o[0] - vx) * PX, (o[1] - vy) * PX
            d.ellipse([x - 1.15 * k * PX, y - 1.15 * k * PX, x + 1.15 * k * PX, y + 1.15 * k * PX], outline=(220, 30, 30, 255), width=3)
        if cara.get('boca'):
            kb, g = cara.get('kb', 2 * k), math.radians(cara.get('giro', 0))
            bx, by = (cara['boca'][0] - vx) * PX, (cara['boca'][1] - vy) * PX
            d.line([(bx - 1.2 * kb * PX * math.cos(g), by - 1.2 * kb * PX * math.sin(g)),
                    (bx + 1.2 * kb * PX * math.cos(g), by + 1.2 * kb * PX * math.sin(g))], fill=(220, 30, 30, 255), width=3)
        if cara.get('marco'):
            x, y, w, _ = cara['marco']
            d.rectangle([(x - vx) * PX, (y - vy) * PX, (x + w - vx) * PX, (y + w - vy) * PX], outline=(40, 90, 220, 255), width=2)
    return fondo


def pintar_clave(clave, previa=True):
    """Pinta tools/dibujos/<clave>.py y guarda su WebP, su JSON (vista, cara, fondo) y dos vistas previas."""
    if DIBUJOS not in sys.path:
        sys.path.insert(0, DIBUJOS)
    if AQUI not in sys.path:
        sys.path.insert(0, AQUI)
    mod = importlib.reload(importlib.import_module(clave)) if clave in sys.modules else importlib.import_module(clave)
    l = Lienzo(mod.VISTA)
    mod.dibujar(l)
    k = mod.CARA.get('k', 2)
    for o in [mod.CARA['ojo']] + ([mod.CARA['ojo2']] if mod.CARA.get('ojo2') else []):
        l.cuenca(o[0], o[1], k)
    l.pintar()
    img = l.imagen()
    os.makedirs(SALIDA, exist_ok=True)
    chica = img.resize((ANCHO_WEBP, int(round(ANCHO_WEBP * img.size[1] / img.size[0]))), Image.LANCZOS)
    b = io.BytesIO()
    chica.save(b, 'WEBP', quality=CALIDAD, method=6)
    io.open(os.path.join(SALIDA, clave + '.webp'), 'wb').write(b.getvalue())
    datos = dict(v=' '.join('%g' % v for v in mod.VISTA), c=mod.CARA, f=getattr(mod, 'FONDO', ''), listo=bool(getattr(mod, 'LISTO', False)))
    io.open(os.path.join(SALIDA, clave + '.json'), 'w', encoding='utf8', newline='\n').write(json.dumps(datos, ensure_ascii=False, indent=1))
    if previa:
        img.save(os.path.join(SALIDA, clave + '-grande.png'))
        _rejilla(img, mod.VISTA, mod.CARA).save(os.path.join(SALIDA, clave + '-rejilla.png'))
    return len(b.getvalue())


def claves():
    return sorted(f[:-3] for f in os.listdir(DIBUJOS) if f.endswith('.py') and not f.startswith('_'))


if __name__ == '__main__':
    for c in (sys.argv[1:] or claves()):
        print('%-14s %5.1f KB' % (c, pintar_clave(c) / 1024))
