# -*- coding: utf-8 -*-
"""El convoy de barcazas del Congo, de memoria: un remolcador viejo empuja cinco o seis barcazas amarradas, y sobre ellas va un pueblo
flotante que tarda semanas entre Kisangani y Kinshasa (NAVES.congo): techos de lona y de chapa sobre palos, bultos, sacos, canastos de
pescado ahumado, palanganas, bicicletas, las cabras. Se ven dos barcazas delante del remolcador.
"""
import numpy as np

from _barcas import agua, caja, cabina, chimenea, fardo, humo, olas_fondo, palo, poli
from pintor import forma, ovalo

VISTA = (0, 28, 120, 54)
AGUA_Y = 74.0


def cabra(l, x, y, espejo=False):
    """una cabra chica, de perfil: el cuerpo, el cuello, la cabeza con sus cuernos y las patas finas"""
    s = -1 if espejo else 1
    X = lambda v: x + s * v
    cuerpo = forma([(X(-3), y - 3.4), (X(1.6), y - 3.8), (X(2.8), y - 5.4), (X(3.8), y - 6.6), (X(5), y - 6.2), (X(4.8), y - 5),
                    (X(3.6), y - 4.6), (X(3), y - 2.2), (X(2), y - 1.6), (X(-2.6), y - 1.6), (X(-3.4), y - 2.4)], 2)
    patas = [caja(min(X(p), X(p + .5)), y - 2, max(X(p), X(p + .5)), y, .1) for p in (-2.6, -1.6, 1.2, 2.1)]
    m = l.masa([cuerpo] + patas, material='claro', alto=.4, brillo=.1, vientre=0, hondo=0, linea=.35, arroja=False)
    l.trazo([(X(3.6), y - 6.4), (X(3), y - 7.6), (X(2.2), y - 8)], [.2, .15, .05], alfa=.9)                   # los cuernos
    l.mancha(ovalo(X(4.1), y - 5.9, .22, .22), '0C3A33', .9, dentro=m)
    return m


def barcaza(l, x0, x1, semilla):
    rng = np.random.default_rng(semilla)
    b = l.masa(poli([(x0, 66.4), (x1, 66.4), (x1 + 1.4, 67.6), (x1, 75.2), (x0, 75.2)], .3), material='acento', alto=.3, brillo=.2,
               vientre=0, hondo=0, contraluz=.2)
    l.trazo([(x0 + .4, 68.6), (x1 + .4, 68.6)], .16, alfa=.35, dentro=b)
    for k in range(int((x1 - x0) / 7)):                             # los parches de óxido del casco
        x = rng.uniform(x0 + 2, x1 - 2)
        l.mancha(ovalo(x, rng.uniform(70, 74), rng.uniform(1, 2.4), rng.uniform(.6, 1.2)), '93701A', .35, dentro=b, difuso=.4)
    # los techos sobre palos: lona clara y chapa verde, a distintas alturas
    x = x0 + 1
    while x < x1 - 8:
        w = rng.uniform(7, 11)
        h = rng.uniform(55, 58.6)
        for px in (x + .6, x + w - .6):
            palo(l, (px, 66.4), (px, h + .8), .25, .22, material='lejos')
        chapa = rng.random() < .5
        l.masa(poli([(x - .6, h + 1.2), (x + w * .5, h - .6), (x + w + .6, h + 1.2), (x + w + .6, h + 2), (x - .6, h + 2)], .2),
               material='lejos' if chapa else 'claro', alto=.2, brillo=.12, vientre=0, hondo=0, linea=.4)
        x += w + rng.uniform(1.2, 3)
    # los bultos, los sacos, los canastos de pescado ahumado y las palanganas
    x = x0 + 1.2
    while x < x1 - 4:
        k = rng.integers(0, 3)
        w = rng.uniform(3.2, 5.4)
        if k == 0:
            fardo(l, x, 66.4 - rng.uniform(3, 4.6), w, rng.uniform(3, 4.4), material=['vientre', 'claro', 'lejos'][rng.integers(0, 3)])
        elif k == 1:
            c = l.masa(forma([(x, 62.4), (x + w, 62.4), (x + w - .6, 66.4), (x + .6, 66.4)], 1), material='acento', alto=.3, brillo=.1,
                       vientre=0, hondo=0, linea=.35, arroja=False)
            for j in range(3):
                l.trazo([(x + .4, 63.4 + j * 1.1), (x + w - .4, 63.4 + j * 1.1)], .12, color='6B4E10', alfa=.6, dentro=c)
            l.masa(ovalo(x + w / 2, 62.2, w * .42, .9), material='oscuro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
        else:
            l.masa(forma([(x, 64.2), (x + w, 64.2), (x + w - .8, 66.4), (x + .8, 66.4)], 1), material='cuerpo', alto=.2, brillo=.3,
                   vientre=0, hondo=0, linea=.35, arroja=False)
        x += w + rng.uniform(.2, 1.4)
    return b


def dibujar(l):
    barcaza(l, 72.4, 116.4, 7)
    barcaza(l, 32.2, 71.6, 3)
    cabra(l, 60.8, 66.4)
    cabra(l, 100, 66.4, espejo=True)
    # el remolcador, viejo: la casa, la timonera, la chimenea con su humo
    c = l.masa(poli([(3.6, 63.2), (30.4, 63.2), (31.4, 64.6), (31.4, 75.4), (6.4, 75.4), (3, 71)], .4), material='acento', alto=.35,
               brillo=.25, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(4, 66.6), (31, 66.6)], [.2, .4, .2], color='0C3A33', alfa=.5, dentro=c)
    for x in (8, 17, 25):
        l.mancha(ovalo(x, 71.4, 2, 1.1), '93701A', .35, dentro=c, difuso=.4)
    cabina(l, 6, 55, 27, 63.2, ventanas=[(8, 57, 3, 3), (12.6, 57, 3, 3), (17.2, 57, 3, 3), (21.8, 57, 3, 3)], techo=.8)
    cabina(l, 10.4, 46.6, 22.4, 54, ventanas=[(11.6, 48.2, 9.6, 3)], techo=1)
    chimenea(l, 25.4, 55, 42.4, r=1.3, corona=False)
    humo(l, 24.6, 39.6, n=4, deriva=(-4.8, -1.2), r=2)
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(4, 74), (116, 74), (112, 78), (8, 78)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
