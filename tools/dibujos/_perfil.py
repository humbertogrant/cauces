# -*- coding: utf-8 -*-
"""Cuerpos alargados de perfil (peces, delfines, cocodrilos) para los dibujos de tools/dibujos/.

Un cuerpo es un eje apenas curvo y dos tablas: lo que sube el lomo y lo que baja la panza en cada punto del largo. Las piezas
(aletas, patas, la cola) se dan en esas mismas coordenadas: `s` va de 0 en la punta del hocico a 1 al final del cuerpo, `y`
hacia el lomo, las dos en fracciones del largo `L` (en unidades de la caja). `P(s, y)` las lleva a la caja del juego.
"""
import math

import numpy as np
from scipy.interpolate import PchipInterpolator
from shapely.geometry import Polygon
from shapely.ops import unary_union

from pintor import chaikin


def pchip(x, y):
    return PchipInterpolator(np.asarray(x, float), np.asarray(y, float), extrapolate=True)


class Perfil:
    def __init__(self, s, arriba, abajo, largo, giros=((0, 0), (1, 0)), punta=(100.0, 45.0)):
        """`giros`: (s, grados) del eje: positivo, la cabeza apunta hacia arriba; `punta`: dónde queda el hocico en la caja."""
        self.s0, self.s1 = float(s[0]), float(s[-1])
        self._a, self._b = pchip(s, arriba), pchip(s, abajo)
        self.L = float(largo)
        gs, gd = zip(*giros)
        self._sg = np.linspace(-0.4, 1.6, 4000)
        self._th = pchip(gs, np.radians(gd))(np.clip(self._sg, min(gs), max(gs)))
        ds = np.diff(self._sg)
        bx = np.concatenate([[0], np.cumsum(-(np.cos(self._th[1:]) + np.cos(self._th[:-1])) / 2 * ds)]) * self.L
        by = np.concatenate([[0], np.cumsum(-(np.sin(self._th[1:]) + np.sin(self._th[:-1])) / 2 * ds)]) * self.L
        self._bx, self._by = bx - np.interp(0, self._sg, bx), by - np.interp(0, self._sg, by)
        self.ox, self.oy = punta

    def arriba(self, s):
        return self._a(np.clip(s, self.s0, self.s1))

    def abajo(self, s):
        return self._b(np.clip(s, self.s0, self.s1))

    def medio(self, s):
        return (self.arriba(s) - self.abajo(s)) / 2

    def grados(self, s):
        """hacia dónde apunta la cabeza en ese punto del eje, en grados de la caja (positivo: arriba)"""
        return math.degrees(float(np.interp(s, self._sg, self._th)))

    def P(self, s, y):
        s, y = np.asarray(s, float), np.asarray(y, float)
        X, Y, t = np.interp(s, self._sg, self._bx), np.interp(s, self._sg, self._by), np.interp(s, self._sg, self._th)
        return np.stack([X - y * self.L * np.sin(t) + self.ox, -(Y + y * self.L * np.cos(t)) + self.oy], -1)

    def p(self, s, y):
        """un punto como lista redondeada, para la cara"""
        return [round(float(v), 1) for v in self.P(s, y)]

    def cuerpo(self, s1=None, joroba=None, n=500, roma=1.0):
        """el contorno de la punta del hocico (redondeada) hasta `s1`; `joroba(s)` suma al lomo; `roma` < 1 achata la punta"""
        s1 = self.s1 if s1 is None else s1
        s = np.linspace(self.s0, s1, n)
        lomo = np.stack([s, self.arriba(s) + (joroba(s) if joroba else 0)], -1)
        panza = np.stack([s[::-1], -self.abajo(s[::-1])], -1)
        a0, b0 = float(self.arriba(self.s0)), float(self.abajo(self.s0))
        r, c = (a0 + b0) / 2, (a0 - b0) / 2
        phi = np.linspace(-np.pi / 2, np.pi / 2, 30)[1:-1]
        punta = np.stack([self.s0 - roma * r * np.cos(phi), c + r * np.sin(phi)], -1)
        return Polygon(self.P(*np.vstack([lomo, panza, punta]).T)).buffer(0)

    def pieza(self, pts, veces=2):
        """un polígono dado en coordenadas del cuerpo, redondeado"""
        return Polygon(self.P(*chaikin(np.asarray(pts, float), veces).T)).buffer(0)

    def linea(self, pts):
        """una polilínea en coordenadas del cuerpo, llevada a la caja"""
        return self.P(*np.asarray(pts, float).T)

    def cola_horizontal(self, ins, envergadura, punta, muesca, elev=50, cerca=1.07):
        """La cola de un cetáceo, que es horizontal: su planta vista desde arriba (media luna con muesca al centro), proyectada
        como la vería alguien un poco por encima del animal (`elev` grados): la mitad cercana baja, la lejana sube."""
        b = np.concatenate([-np.linspace(1, 0, 60)[:-1], np.linspace(0, 1, 60)])
        f = np.abs(b)
        ataque = np.stack([punta * f ** 1.4, b], -1)
        fuga = np.stack([muesca + (punta - muesca) * f ** 2.5 - .012 * np.clip(1 - f / .10, 0, 1), b], -1)[::-1]
        planta = np.vstack([ataque, fuga[1:-1]])
        a, bb = planta[:, 0], planta[:, 1] * envergadura * np.where(planta[:, 1] > 0, cerca, 2 - cerca)
        eje = float(self.medio(ins))
        return Polygon(self.P(ins + a, eje - bb * math.sin(math.radians(elev)))).buffer(0)

    def paleta(self, raiz, grados, largo, ataque, fuga, festón=0.0, abombe=.01):
        """Una aleta pectoral en paleta que nace en `raiz` (s, y) y apunta `grados` (negativo: hacia atrás y abajo); `ataque` y
        `fuga`: medio ancho del borde de adelante y del de atrás en 0, .15, .35, .55, .75, .9 y 1 del largo. Devuelve el
        polígono y sus ejes (d: a lo largo; e: hacia el borde de ataque), para dibujarle los dedos."""
        R, ang = np.asarray(raiz, float), math.radians(grados)
        d = np.array([math.cos(ang), math.sin(ang)])
        e = np.array([d[1], -d[0]])
        U = np.linspace(0, 1, 80)
        WL, WT = pchip([0, .15, .35, .55, .75, .9, 1], ataque)(U), pchip([0, .15, .35, .55, .75, .9, 1], fuga)(U)
        lado_a = R + (U[:, None] * largo) * d + WL[:, None] * e
        lado_f = R + (U[:, None] * largo) * d - WT[:, None] * e
        phi = np.linspace(0, np.pi, 60)[1:-1]
        c0, rad = R + largo * d + (WL[-1] - WT[-1]) / 2 * e, (WL[-1] + WT[-1]) / 2
        bomba = abombe * np.sin(phi) + festón * np.abs(np.sin(2.5 * phi)) * (phi > .8)
        punta = c0 + (np.cos(phi)[:, None] * rad) * e + bomba[:, None] * d
        return Polygon(self.P(*chaikin(np.vstack([lado_a, punta, lado_f[::-1]]), 2).T)).buffer(0), d, e

    def encuadrar(self, piezas, caja):
        """mueve el animal para que la unión de `piezas()` quede centrada en la caja (x0, y0, x1, y1)"""
        self.ox = self.oy = 0.0
        x0, y0, x1, y1 = unary_union(piezas()).bounds
        self.ox = (caja[0] + caja[2]) / 2 - (x0 + x1) / 2
        self.oy = (caja[1] + caja[3]) / 2 - (y0 + y1) / 2
