# -*- coding: utf-8 -*-
"""Cascos largos de canoa para tools/dibujos/barcas/: la borda y la quilla como dos curvas que se juntan en las puntas (la popa a la
izquierda, la proa a la derecha), con la quilla redonda que sube hasta cada punta y las puntas que suben tanto como se pida."""
import numpy as np


def canoa(x0, x1, y, alto, sube_popa=2.0, sube_proa=3.0, panza=1.0, n=17, lleno=.55):
    """La borda y la quilla de una canoa de `x0` (popa) a `x1` (proa), con la borda en `y` al medio y `alto` de puntal. Las puntas
    suben `sube_popa` y `sube_proa`; `lleno` (0 a 1) dice cuán llena es la quilla (más, más plana abajo y más rápida la subida en las
    puntas); `panza` > 1 la hace más honda. Devuelve (borda, quilla), de popa a proa, con los mismos puntos en las puntas."""
    t = np.linspace(0, 1, n)
    xs = x0 + (x1 - x0) * t
    tip_popa, tip_proa = y - sube_popa, y - sube_proa
    # la borda: casi recta al medio, sube en curva hacia las puntas
    borda = y - sube_popa * np.clip(1 - t / .38, 0, 1) ** 2 - sube_proa * np.clip((t - .6) / .4, 0, 1) ** 2
    borda[0], borda[-1] = tip_popa, tip_proa
    # la quilla: redonda, del fondo sube hasta encontrar la borda en cada punta
    base = tip_popa + (tip_proa - tip_popa) * t
    k = .35 + .3 * (1 - lleno)
    fondo = base + (y + alto * panza - base) * np.sin(np.pi * t) ** k
    return [(float(a), float(b)) for a, b in zip(xs, borda)], [(float(a), float(b)) for a, b in zip(xs, fondo)]


def contorno(borda, quilla):
    """el polígono del casco: la borda de popa a proa y la quilla de vuelta, sin repetir las puntas"""
    return borda + quilla[-2:0:-1]
