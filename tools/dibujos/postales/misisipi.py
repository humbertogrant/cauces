# -*- coding: utf-8 -*-
"""Las postales del Misisipi, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el de San Luis, que se pone en el Oeste.

- el nacimiento: el río sale del lago Itasca tan chico que se cruza a pie por unas piedras: un niño, con su gorra y su camiseta
  doradas, cruza de piedra en piedra con los brazos abiertos, entre pinos;
- Mineápolis: «un muñeco de masa amasa junto a una catarata»: el muñeco de masa, dorado como una galleta de jengibre, con sus botones y
  sus zigzags de azúcar y su gorro de cocinero, amasa en su mesa al lado de las cataratas de San Antonio, con panes ya horneados;
  atrás, el molino de harina y el puente de piedra en arcos (blanco y redondo, parecía un muñeco de nieve);
- San Luis: «un arco de 192 m como puerta»: el Gateway Arch, de acero, en la orilla, que enmarca el sol que se pone en el Oeste, hacia
  donde salían Lewis y Clark; a la izquierda, el Misuri que entra al Misisipi;
- Memphis: «Elvis toca una guitarra hecha de algodón»: un cantante de rock con su copete y su traje dorado, que toca una guitarra cuyo
  cuerpo es un capullo de algodón, en la orilla, con las matas de algodón y, atrás, el puente en M sobre el río;
- Baton Rouge: «un bastón rojo clavado en la orilla»: el bastón que marcaba el límite de las tierras de caza, dorado como lo que hay que
  recordar, con sus plumas; enfrente, las chimeneas de las plantas y un barco;
- Nueva Orleans: «una trompeta sale del agua en una media luna»: el río que se curva en media luna alrededor de la ciudad, con sus casas
  de balcones detrás del dique, y la trompeta dorada que sale del agua;
- el mar: el vapor no sale al golfo (en Nueva Orleans la carga pasa a los barcos de altura): el delta del Misisipi, la «pata de
  pájaro», visto desde arriba como una pata de gallina dorada echada en el golfo de México: la caña con sus escamas, que viene de
  tierra, los tres dedos, que son los pasos del río entre sus diques de barro, con sus almohadillas y sus uñas, y el dedo de atrás.
"""
import math

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, abeto, agua, arbol, ave, cielo, cinta, juncos, nube, orilla, pasto, prado, reflejo, rio,  # noqa: F401
                     tierra)
from pintor import forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`


def piel(l, piezas, tono=.45):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nino(l, x, base, s=1.0):
    """un niño que cruza el río de piedra en piedra, de perfil, mirando a la derecha: da un paso largo con los brazos abiertos para no
    caerse; la gorra y la camiseta, doradas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    piel(l, [tubo(P([(-.3, -6), (-1.6, -3.2), (-2.6, -.6)]), [.6 * s, .5 * s, .45 * s], 6),
             tubo(P([(.4, -6), (1.8, -3.4), (2.6, -.6)]), [.6 * s, .5 * s, .45 * s], 6),
             tubo(P([(-1, -11.6), (-3.4, -12.4), (-5.8, -12.8)]), [.5 * s, .45 * s, .4 * s], 6), O(-6.1, -12.8, .6, .55),
             tubo(P([(1, -11.6), (3.4, -12.6), (5.8, -13.4)]), [.5 * s, .45 * s, .4 * s], 6), O(6.1, -13.5, .6, .55),
             O(.2, -14.4, 1.7, 1.75), O(-1.3, -14.4, .5, .6)])
    l.masa([O(-2.9, -.3, 1.1, .5), O(3, -.3, 1.1, .5)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.masa(forma(P([(-1.5, -7.8), (1.5, -7.8), (2.2, -5.2), (-2, -5.2)]), 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.3)                                                     # el pantalón corto
    l.masa(forma(P([(-1.4, -12.6), (1.4, -12.6), (2, -11.4), (1.6, -7.6), (-1.6, -7.6), (-2, -11.4)]), 1), material='acento', alto=.35,
           brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.3)      # la camiseta
    l.masa(forma(P([(-1.6, -15), (-1.3, -16.3), (.4, -16.6), (1.6, -15.9), (3.2, -15.3), (1.6, -15)]), 1), material='acento', alto=.3,
           brillo=.3, vientre=0, hondo=0, linea=.3)                      # la gorra, con la visera adelante
    l.mancha(O(1, -14.5, .2, .2), '05201C', 1)
    l.trazo(P([(.9, -13.5), (1.4, -13.3), (1.8, -13.6)]), .1 * s, color='0C3A33', alfa=.9)


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 28, 5, 14, .6)
    nube(l, 96, 4, 10, .45)
    # el lago Itasca, al fondo, con su orilla de pinos
    prado(l, 15, 41, .24)
    agua(l, forma([(-2, 15.4), (122, 15.4), (122, 21.6), (86, 23), (70, 24.6), (50, 24.6), (34, 23), (-2, 21.6)], 2), ondas=8, semilla=1,
         linea=.25)
    for x in np.arange(-1, 122, 2.6):
        abeto(l, x + rng.uniform(-.6, .6), 15.6 + rng.uniform(-.4, .4), rng.uniform(4, 6), rng.uniform(2, 2.8))
    # el río que nace, tan chico, que baja hacia nosotros, y las piedras que lo cruzan
    agua(l, cinta([(60, 24), (58.4, 28), (61.6, 33), (58.6, 37.6), (60, 41.5)], [5, 6, 7, 8.4, 9.6], 8), ondas=4, semilla=2, linea=.3)
    piedras = [ovalo(x, y, rx, ry) for x, y, rx, ry in ((47.6, 30.6, 2.4, 1), (52.4, 30.2, 2.2, .95), (57, 30.4, 2.3, 1), (61.8, 30.1, 2.2, .95),
                                                        (66.4, 30.4, 2.3, 1), (71.2, 30.6, 2.3, 1))]
    l.masa(piedras, material='vientre', alto=.5, brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for x, y in ((47.6, 30.6), (52.4, 30.2), (57, 30.4), (61.8, 30.1), (66.4, 30.4), (71.2, 30.6)):
        l.trazo([(x - 1.8, y + .9), (x, y + 1.3), (x + 1.8, y + .9)], .16, color='D2F2DA', alfa=.8)   # el agua que pasa entre las piedras
    # las orillas, con sus pinos y su pasto
    for x, y, h in ((8, 34, 9), (16, 36.6, 11), (26, 33, 7.6), (96, 33.6, 8.4), (106, 36, 11), (114, 33, 8)):
        abeto(l, x, y, h, h * .45, material='cuerpo')
    pasto(l, 2, 40, 27, 40.6, 14, semilla=3)
    pasto(l, 80, 118, 27, 40.6, 14, semilla=4)
    # el niño que cruza a pie, de piedra en piedra, protagonista
    nino(l, 59.6, 30.2, 1.15)


# ------------------------------------------------------------------------------------------------ Mineápolis
def muneco(l, x, base, s=1.0):
    """un muñeco de masa, dorado como una galleta de jengibre, con sus botones y sus zigzags de azúcar y su gorro de cocinero, que amasa
    detrás de su mesa: la bola de masa cruda entre las manos y, en la punta de la mesa, los panes ya horneados"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = l.masa([O(0, -9, 5.6, 6.2), O(-3.4, -.8, 1.6, 1.2), O(3.4, -.8, 1.6, 1.2)], material='acento', alto=.6, brillo=.4, vientre=0,
                    hondo=.1, linea=.45, contraluz=.35)
    for k in range(3):                                                   # los botones de azúcar
        l.mancha(O(0, -12.6 + k * 2.2, .55, .55), 'FFFFFF', .95, dentro=cuerpo)
    for sx in (-1, 1):                                                   # el zigzag de azúcar de los pies
        l.trazo(P([(sx * 2.4, -1.2), (sx * 2.9, -.5), (sx * 3.4, -1.2), (sx * 3.9, -.5), (sx * 4.4, -1.2)]), .16 * s, color='FFFFFF',
                alfa=.95, dentro=cuerpo)
    cab = l.masa(O(0, -18.2, 4.2, 3.8), material='acento', alto=.6, brillo=.4, vientre=0, hondo=.1, linea=.45, contraluz=.35)
    for dx in (-1.5, 1.5):
        l.mancha(O(dx, -18.8, .4, .5), '05201C', 1, dentro=cab)
        l.mancha(O(dx * 1.6, -17.2, .8, .45), 'C86A6A', .4, dentro=cab)   # los cachetes
    l.trazo(P([(-1.4, -16.8), (0, -16.1), (1.4, -16.8)]), .18 * s, color='0C3A33', alfa=.9, dentro=cab)
    l.masa([O(0, -24.6, 3.4, 2.6), O(-2.4, -23.8, 2, 1.8), O(2.4, -23.8, 2, 1.8), Polygon(P([(-3.2, -21.4), (3.2, -21.4), (3, -23.4), (-3, -23.4)]))],
           material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.4)        # el gorro de cocinero
    # la mesa, la bola de masa entre las manos y los panes
    l.masa([Polygon(P([(-11, -6.2), (13, -6.2), (13, -5), (-11, -5)])), box(x - 10 * s, base - 5, x - 9 * s, base),
            box(x + 11.6 * s, base - 5, x + 12.6 * s, base)], material='lejos', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.masa([O(0, -7.6, 3.4, 1.6), O(-1.6, -8.2, 1.4, 1)], material='claro', alto=.5, brillo=.2, vientre=0, hondo=0, linea=.35)  # la masa cruda
    for sx in (-1, 1):                                                   # los brazos que amasan
        b = l.masa([tubo(P([(sx * 4.6, -11), (sx * 4.4, -8.8), (sx * 2.4, -7.8)]), [1.2 * s, 1.1 * s, 1 * s], 6), O(sx * 2.2, -7.8, 1.3, 1)],
                   material='acento', alto=.5, brillo=.35, vientre=0, hondo=0, linea=.35)
        l.trazo(P([(sx * 3.6, -10.4), (sx * 4.6, -10.1), (sx * 5.3, -10.5)]), .14 * s, color='FFFFFF', alfa=.9, dentro=b)
    panes = l.masa([O(7.4, -7.4, 2.4, 1.3), O(10.6, -7.2, 2, 1.1)], material='vientre', alto=.6, brillo=.3, vientre=0, hondo=0, linea=.35,
                   contraluz=.3)
    l.mancha(O(9, -7.3, 5, 2), 'A2683A', .6, dentro=panes)              # los panes, café: lo dorado es el muñeco
    for u in (6.4, 7.6, 8.8):
        l.trazo(P([(u - .4, -7.9), (u + .4, -7)]), .14 * s, color='FBEFCB', alfa=.9, dentro=panes)


def mineapolis(l):
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .55)
    # atrás, el molino de harina con sus silos y su chimenea, y el puente de piedra en arcos
    prado(l, 15, 22, .2)
    mol = l.masa([box(76, 6, 96, 16.4), box(98, 4.4, 106, 16.4), box(106.4, 4.4, 114.4, 16.4)], material='vientre', alto=.25, brillo=.1,
                 vientre=0, hondo=0, linea=.35)
    l.mancha(box(74, 3, 116, 17), 'E8B952', .2, dentro=mol)
    for x in np.arange(78, 95, 2.4):
        for y in (8.6, 11.6):
            l.mancha(box(x, y, x + 1.2, y + 1.6), '164F46', .8, dentro=mol)
    l.masa(box(116.2, 1.4, 118.4, 16.4), material='lejos', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)    # la chimenea (detrás
    # del muñeco le salía del gorro como una antena)
    puente = box(-2, 14.4, 122, 17.4)
    for x in np.arange(2, 122, 7):
        puente = puente.difference(ovalo(x, 17.6, 2.6, 2.2))
    p = l.masa(puente, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(box(-2, 14, 122, 18), 'E8B952', .22, dentro=p)
    rio(l, 17.6)
    # las cataratas de San Antonio, a la izquierda, con su escalón de piedra y el agua blanca
    l.masa(Polygon([(-2, 21.4), (44, 21.4), (44, 24.4), (-2, 24.4)]), material='vientre', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(0, 44, 2.6):
        l.trazo([(x, 21.6), (x + .3, 26.4), (x - .2, 30.4)], [.9, 1.1, .4], color='FFFFFF', alfa=.85)
    l.mancha(ovalo(22, 30.4, 24, 2.2), 'FFFFFF', .6, difuso=.8)
    # la orilla de adelante, y el muñeco de masa que amasa, protagonista
    orilla(l, forma([(30, 41.5), (36, 33.6), (54, 32.2), (90, 32.6), (122, 31.6), (122, 41.5)], 2), tinte=.24)
    muneco(l, 70, 37.4, 1.05)


# ------------------------------------------------------------------------------------------------ San Luis
def san_luis(l):
    cielo(l, sol=None, tarde=.4)
    # el sol que se pone en el Oeste, enmarcado por el arco, el único dorado
    l.mancha(ovalo(60, 21, 13, 13), 'F2D48A', .4, difuso=3)
    l.masa(ovalo(60, 21.6, 5.2, 5.2), material='acento', alto=.4, brillo=.3, vientre=0, hondo=0, tinta=False, contraluz=0)
    # la ciudad baja, al pie del arco, y el río; a la izquierda, el Misuri que entra
    prado(l, 26.4, 31, .2)
    for x, w, h in ((8, 4, 6), (14, 3.6, 9), (20, 4.4, 7), (96, 4, 8), (102, 3.4, 11), (108, 4.4, 7.4), (114, 3.6, 9.6)):
        e = l.masa(box(x - w / 2, 27.2 - h, x + w / 2, 27.4).buffer(.06), material='claro', alto=.25, brillo=.12, vientre=0, hondo=0,
                   linea=.3)
        for yy in np.arange(27.2 - h + .8, 27, 1):
            l.trazo([(x - w / 2 + .3, yy), (x + w / 2 - .3, yy)], .08, color='8EB5AA', alfa=.8, dentro=e)
    agua(l, cinta([(-2, 26.8), (12, 27.6), (24, 29.2), (34, 31.4)], [2, 2.8, 3.6, 4.8], 8), linea=.25)   # el Misuri, que entra
    rio(l, 30)
    # el Gateway Arch, protagonista: la catenaria de acero, más gruesa abajo, que enmarca el sol
    base, a = 30.6, 11.3
    pts = [(x, base - 29 + a * (math.cosh((x - 60) / a) - 1)) for x in np.linspace(38.2, 81.8, 41)]
    anchos = [3.2 - 1.8 * (1 - abs(x - 60) / 21.8) for x, _ in pts]
    arco = cinta(pts, anchos, 4)
    m = l.masa(arco, material='claro', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo([(x - .4, y + .2) for x, y in pts[2:-2]], .16, color='FFFFFF', alfa=.8, dentro=m)
    reflejo(l, arco, 30.2, .3)
    l.masa([forma([(68, 34.6), (82, 34.6), (83.4, 33.2), (67, 33.2)], 1), box(71, 31.4, 78, 33.3), box(72.4, 29.4, 73.4, 31.5)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)       # un barco en el río


# ------------------------------------------------------------------------------------------------ Memphis
def cantante(l, x, base, s=1.0):
    """un cantante de rock, de frente: el copete negro, las patillas, el traje dorado, una pierna doblada al bailar, y la guitarra
    cuyo cuerpo es un capullo de algodón, con su mástil"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-2.6, -.4, 1.5, .6), O(3.4, -.5, 1.5, .6)], material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.25)
    traje = [tubo(P([(-1.4, -11), (-2, -6), (-2.6, -.8)]), [1.3 * s, 1.1 * s, 1 * s], 6),
             tubo(P([(1.4, -11), (3.6, -6.4), (3.4, -.8)]), [1.3 * s, 1.1 * s, 1 * s], 6),
             forma(P([(-3.4, -20.4), (3.4, -20.4), (4, -16), (3, -10.6), (-3, -10.6), (-4, -16)]), 1),
             tubo(P([(3, -19.4), (5, -15.6), (3.2, -13)]), [1 * s, .9 * s, .8 * s], 6),
             tubo(P([(-3, -19.4), (-5.6, -17.4), (-7.8, -17.8)]), [1 * s, .9 * s, .8 * s], 6)]
    t = l.masa(traje, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.35)
    for k in range(4):                                                   # el brillo del lamé
        l.trazo(P([(-2.6 + k * 1.6, -19.6), (-2 + k * 1.4, -12)]), [.05, .14, .05], color='FBEFCB', alfa=.8, dentro=t)
    l.masa(forma(P([(-1.4, -20.4), (0, -18.2), (1.4, -20.4), (2.4, -21.6), (0, -21), (-2.4, -21.6)]), 1), material='claro', alto=.3,
           brillo=.2, vientre=0, hondo=0, linea=.3)                      # el cuello alto
    # la guitarra: el mástil y las clavijas, y el cuerpo, un capullo de algodón con sus hojitas secas
    l.masa([tubo(P([(.6, -12.4), (-6, -18.4), (-9.4, -21.4)]), [.45 * s, .4 * s, .4 * s], 6),
            forma(P([(-9, -20.6), (-10.6, -22.4), (-11.4, -21.6), (-10, -20)]), 1)], material='lejos', alto=.3, brillo=.25, vientre=0,
           hondo=0, linea=.3)
    for k in range(5):
        u = -1 - k * 1.5
        l.trazo(P([(u - .3, -13.4 - k * 1.3), (u + .3, -12.9 - k * 1.4)]), .08 * s, color='FBEFCB', alfa=.8)
    l.masa([Polygon(P([(1.6, -10.6), (5, -8.4), (3.6, -11.6)])), Polygon(P([(-1.6, -10.6), (-5, -8.6), (-3.6, -11.8)])),
            Polygon(P([(0, -9.2), (1.6, -6), (-1.6, -6)]))], material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    algodon = [O(-1.8, -11.4, 2.4, 2.1), O(1.8, -11.6, 2.3, 2.1), O(0, -9.4, 2.4, 2), O(0, -13.2, 2, 1.8)]
    l.masa(algodon, material='claro', alto=.6, brillo=.3, vientre=0, hondo=.1, linea=.35, contraluz=.35)
    piel(l, [O(3.4, -12.6, .9, .8), O(-8, -17.8, .9, .8), O(0, -23.4, 2.3, 2.6), Polygon(P([(-.8, -21.2), (.8, -21.2), (.8, -20.2), (-.8, -20.2)]))],
         .5)
    # la cabeza: el copete, las patillas, los ojos y la sonrisa torcida
    l.masa([forma(P([(-2.4, -24.6), (-2.6, -26.4), (-1.2, -27.8), (1.4, -28.4), (3.4, -27.6), (2.6, -26.6), (2.2, -25.4), (0, -25.8)]), 2),
            Polygon(P([(-2.4, -24.8), (-2.2, -22.4), (-1.7, -22.4), (-1.6, -24.6)])),
            Polygon(P([(2.4, -24.8), (2.2, -22.4), (1.7, -22.4), (1.6, -24.6)]))], material='oscuro', alto=.4, brillo=.35, vientre=0, hondo=0,
           linea=.3)
    for dx in (-.8, .8):
        l.mancha(O(dx, -23.8, .25, .28), '05201C', 1)
    l.trazo(P([(-.6, -22.4), (.2, -22.1), (.9, -22.6)]), .16 * s, color='0C3A33', alfa=.9)


def memphis(l):
    rng = np.random.default_rng(4)
    cielo(l, sol=None)
    nube(l, 22, 5, 12, .5)
    nube(l, 100, 4, 10, .45)
    # atrás, el río y el puente en M, con sus dos arcos
    prado(l, 18, 41, .24)
    rio(l, 20)
    for cx in (40, 80):
        arco = cinta([(cx + 18 * math.cos(t), 21 - 12 * math.sin(t)) for t in np.linspace(0, math.pi, 25)], [.8] * 25, 3)
        l.masa(arco, material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
        for t in np.linspace(.2, math.pi - .2, 9):                      # los tirantes
            xx = cx + 18 * math.cos(t)
            l.trazo([(xx, 21 - 12 * math.sin(t)), (xx, 20.6)], .1, color='8EB5AA', alfa=.9)
    l.masa(box(10, 20.2, 110, 21.2), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    # la orilla de adelante, con matas de algodón, y el cantante, protagonista
    m = orilla(l, forma([(-2, 41.5), (-2, 27.4), (30, 26.2), (60, 26), (92, 26.4), (122, 27.2), (122, 41.5)], 2), tinte=.26)
    for x0 in (4, 12, 20, 98, 106, 114):                                 # las matas de algodón
        y0 = 33 + rng.uniform(-1, 1)
        l.masa([tubo([(x0, y0 + 4), (x0 + dx, y0)], [.2, .14], 4) for dx in (-1.4, 0, 1.4)], material='lejos', alto=.2, brillo=.1, vientre=0,
               hondo=0, linea=.2)
        l.masa([ovalo(x0 + dx, y0 + dy, .9, .8) for dx, dy in ((-1.4, 0), (0, -.6), (1.4, .1))], material='claro', alto=.5, brillo=.3, vientre=0,
               hondo=0, linea=.25)
    l.masa(box(44, 37.4, 76, 39.2).buffer(.15), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)    # el escenario
    for x, y in ((40, 14), (78, 12), (84, 17)):                          # las notas
        l.masa([ovalo(x, y, .9, .7, -20), box(x + .7, y - 4, x + 1, y)], material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.2)
    cantante(l, 60, 37.4, 1.3)


# ------------------------------------------------------------------------------------------------ Baton Rouge
def baton_rouge(l):
    cielo(l, sol=None)
    nube(l, 30, 4, 12, .5)
    # enfrente, las plantas, con sus chimeneas a rayas, sus tanques y el humo
    prado(l, 18, 23, .2)
    for x, h in ((70, 14), (78, 10), (92, 16), (104, 12), (112, 9)):
        c = l.masa(box(x - .9, 19 - h, x + .9, 19.4), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        for y in np.arange(19 - h, 19, 2.4):
            l.mancha(box(x - 1, y, x + 1, y + 1.2), '3E7A6D', .85, dentro=c)
        for k in range(3):
            l.mancha(ovalo(x - 1.6 - k * 2.2, 19 - h - 1.6 - k * 1.2, 1.4 + k * .5, 1 + k * .3), 'FFFFFF', .7 - k * .15, difuso=.4)
    l.masa([ovalo(x, 18.4, 3, 1).union(box(x - 3, 15.4, x + 3, 18.4)).union(ovalo(x, 15.4, 3, 1)) for x in (84, 98)], material='claro',
           alto=.35, brillo=.2, vientre=0, hondo=0, linea=.3)            # los tanques
    rio(l, 22)
    l.masa([forma([(10, 25.6), (44, 25.6), (46.4, 23.6), (11, 23.8)], 1), box(12, 21, 18, 23.8), box(13.4, 19.4, 15, 21.2)], material='lejos',
           alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)            # un barco grande
    # la orilla de adelante, con el bastón clavado, protagonista, y sus plumas
    m = orilla(l, forma([(-2, 41.5), (-2, 31), (26, 29.6), (60, 29.4), (94, 30), (122, 31.2), (122, 41.5)], 2), tinte=.26)
    pasto(l, 0, 120, 31, 40.6, 26, semilla=5, dentro=m)
    l.mancha(ovalo(61, 37.6, 6, 1.2), '0C3A33', .25, difuso=.6)
    b = l.masa(tubo([(60.4, 38.4), (60, 20), (59.6, 4.4)], [1.1, .95, .8], 6), material='acento', alto=.45, brillo=.4, vientre=0, hondo=0,
               linea=.45, contraluz=.35)
    for y in (8, 12, 16, 30):                                            # las bandas pintadas
        l.trazo([(58.8, y), (61, y - .3)], .5, color='6B4E10', alfa=.7, dentro=b)
    for k, (dx, dy, a) in enumerate(((-2.4, 6.2, -40), (2.6, 6.6, 40), (-2, 7.8, -20))):  # las plumas atadas arriba
        l.masa(ovalo(59.8 + dx, 4.4 + dy, .7, 2.6, a), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.trazo([(59.8 + dx * .4, 4.4 + dy - 2.2), (59.8 + dx, 4.4 + dy + 1.8)], .08, color='8EB5AA', alfa=.9)
    l.trazo([(58.6, 9.2), (61.2, 8.6)], .3, color='0C3A33', alfa=.8)        # la atadura


# ------------------------------------------------------------------------------------------------ Nueva Orleans
def trompeta(l, x, y, s=1.0, giro=-35):
    """una trompeta dorada que sale del agua con la campana arriba: la campana, el tubo, las tres válvulas y la boquilla"""
    from shapely import affinity
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    R = lambda g: affinity.rotate(g, giro, origin=(x, y))
    campana = forma(P([(-1, -12), (-3.6, -15.4), (-4.4, -17), (4.4, -17), (3.6, -15.4), (1, -12)]), 2)
    tubo_ = tubo(P([(0, -12), (0, -2), (0, 3)]), [.8 * s, .7 * s, .7 * s], 6)
    vuelta = tubo(P([(.3, -4), (2.4, -4.6), (3, -7), (2.2, -9), (.4, -9.6)]), [.6 * s, .6 * s, .6 * s, .6 * s, .6 * s], 8)
    valvulas = [Polygon(P([(1.2 + dy * 0, -7.6 + dy), (3.4, -7.6 + dy), (3.4, -6.8 + dy), (1.2, -6.8 + dy)])) for dy in (0, 1.4, 2.8)]
    botones = [ovalo(x + 3.9 * s, y + (-7.2 + dy) * s, .5 * s, .5 * s) for dy in (0, 1.4, 2.8)]
    t = l.masa([R(g) for g in [campana, tubo_, vuelta] + valvulas + botones], material='acento', alto=.5, brillo=.6, vientre=0, hondo=0, linea=.45,
               contraluz=.4)
    l.mancha(R(ovalo(x, y - 17 * s, 4.2 * s, .9 * s)), '6B4E10', .8, dentro=t)   # la boca de la campana
    l.trazo([tuple(R(Polygon(P([(-.3, v), (-.29, v), (-.3, v + .01)]))).exterior.coords[0]) for v in (-11, -6, -1)], .2 * s, color='FBEFCB',
            alfa=.8, dentro=t)
    return t


def nueva_orleans(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 98, 3.4, 10, .45)
    # visto un poco desde arriba: el río que se curva en media luna, y la ciudad adentro, detrás del dique
    tierra(l, 8, 41, desierto=.2)
    pts = [(60 + 50 * math.cos(t), 6 + 30 * math.sin(t)) for t in np.linspace(math.radians(10), math.radians(170), 40)]
    media_luna = cinta(pts, [3 + 6 * math.sin(math.radians(10 + 160 * k / 39)) for k in range(40)], 3)
    agua(l, media_luna, ondas=10, semilla=1, linea=.35)
    adentro = Polygon([(60 + 46 * math.cos(t), 6 + 26 * math.sin(t)) for t in np.linspace(math.radians(14), math.radians(166), 30)] + [(60, 6)])
    l.mancha(adentro, 'E8B952', .12)
    dique = cinta([(60 + 46.6 * math.cos(t), 6 + 26.4 * math.sin(t)) for t in np.linspace(math.radians(16), math.radians(164), 30)], [.8] * 30, 3)
    l.masa(dique, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    for _ in range(46):                                                  # las casas de balcones, con sus techos empinados
        a = rng.uniform(math.radians(25), math.radians(155))
        r = rng.uniform(.3, .82)
        cx, cy = 60 + 44 * r * math.cos(a), 6 + 24 * r * math.sin(a)
        if cy < 12:
            continue
        w = 2 + r * 1.2
        c = l.masa(box(cx - w / 2, cy - 1.6 - r, cx + w / 2, cy), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22,
                   arroja=False)
        l.trazo([(cx - w / 2, cy - .9), (cx + w / 2, cy - .9)], .14, color='164F46', alfa=.8, dentro=c)
        l.masa(Polygon([(cx - w / 2 - .2, cy - 1.6 - r), (cx, cy - 2.8 - r * 1.4), (cx + w / 2 + .2, cy - 1.6 - r)]), material='lejos', alto=.2,
               brillo=.15, vientre=0, hondo=0, linea=.2, arroja=False)
    # la trompeta, protagonista, que sale del agua en la media luna
    l.mancha(ovalo(60, 36.6, 6, 1.2), 'FFFFFF', .7, difuso=.4)
    trompeta(l, 60, 36.4, 1.15, -28)
    for k in range(3):                                                   # las ondas alrededor
        l.trazo([(60 + (5 + k * 2.4) * math.cos(t), 36.8 + (1 + k * .5) * math.sin(t)) for t in np.linspace(math.radians(200), math.radians(340), 9)],
                .16, color='D2F2DA', alfa=.8)


# ------------------------------------------------------------------------------------------------ el mar
def vapor(l, x, y, s=1.0):
    """el vapor de rueda, la barca del juego, mirando a la derecha: el casco chato y dorado, las dos cubiertas blancas con su baranda, la
    casilla del piloto, las dos chimeneas altas con su corona y la rueda de paletas atrás; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, r: ovalo(x + u * s, y + v * s, r * s, r * s)
    rueda = l.masa(O(-13.2, -3.4, 4), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    for k in range(10):                                                  # las paletas
        a = math.radians(k * 36)
        l.trazo([(x + (-13.2 + 1 * math.cos(a)) * s, y + (-3.4 + 1 * math.sin(a)) * s), (x + (-13.2 + 4 * math.cos(a)) * s, y + (-3.4 + 4 * math.sin(a)) * s)],
                .2 * s, color='0C3A33', alfa=.9, dentro=rueda)
    cub = l.masa([Polygon(P([(-10, -6.4), (10, -6.4), (10, -2), (-10, -2)])), Polygon(P([(-7, -10.4), (6, -10.4), (6, -6.2), (-7, -6.2)])),
                  Polygon(P([(-2, -13.4), (2.4, -13.4), (2.4, -10.2), (-2, -10.2)]))], material='claro', alto=.3, brillo=.15, vientre=0, hondo=0,
                 linea=.4)
    for v0, u0, u1 in ((-6.4, -10, 10), (-10.4, -7, 6)):                # las barandas y las ventanas
        l.trazo(P([(u0, v0 + 1), (u1, v0 + 1)]), .12 * s, color='0C3A33', alfa=.6, dentro=cub)
        for u in np.arange(u0 + 1, u1, 1.6):
            l.trazo(P([(u, v0 + 1.6), (u, v0 + 3.4)]), .3 * s, color='164F46', alfa=.7, dentro=cub)
    for u in (3.4, 6.4):                                                 # las chimeneas, con su corona
        l.masa([Polygon(P([(u - .7, -6.2), (u + .7, -6.2), (u + .7, -19), (u - .7, -19)])), forma(P([(u - 1.4, -19.6), (u - .8, -18.6),
                (u + .8, -18.6), (u + 1.4, -19.6), (u + .9, -20.4), (u, -19.8), (u - .9, -20.4)]), 1)], material='oscuro', alto=.3, brillo=.3,
               vientre=0, hondo=0, linea=.3)
        for k in range(3):                                               # el humo
            l.mancha(ovalo(x + (u - 2 - k * 2.4) * s, y + (-21.6 - k * 1.2) * s, (1.3 + k * .5) * s, (1 + k * .3) * s), 'FFFFFF', .75 - k * .15,
                     difuso=.4)
    casco = forma(P([(-13.6, -2.4), (-13, .6), (12, .6), (14.6, -2.6), (12, -1.8), (-10, -1.8)]), 1)
    c = l.masa(casco, material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-12.6, -.8), (0, -.4), (13, -1.2)]), [.05, .12, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco.union(Polygon(P([(-10, -6.4), (10, -6.4), (10, -2), (-10, -2)])))


def pelicano(l, x, y, s=1.0):
    """un pelícano pardo que vuela de costado, mirando a la derecha: las alas anchas en M, el cuerpo, la cabeza recogida y el pico largo
    con su bolsa, que es lo que lo distingue"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    alas = [tubo(P([(-.6, 0), (-3, -2.2), (-6.4, -1)]), [.7 * s, .55 * s, .2 * s], 6), tubo(P([(.6, 0), (3, -2.4), (6.2, -1.4)]), [.7 * s, .55 * s, .2 * s], 6)]
    cuerpo = ovalo(x, y + .2 * s, 2.2 * s, .9 * s)
    cabeza = ovalo(x + 2.4 * s, y - .4 * s, .8 * s, .7 * s)
    pico = Polygon(P([(2.8, -.8), (7, .3), (6.6, .9), (2.8, .2)]))
    l.masa(alas + [cuerpo, cabeza, pico], material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.mancha(Polygon(P([(3.2, .1), (6.6, .6), (5.4, 1.2), (3.4, .7)])), 'A4DCC4', .6)    # la bolsa del pico


def pata_de_pajaro(l):
    """el delta del Misisipi, la «pata de pájaro», dorada, vista desde arriba como una pata de gallina echada en el golfo: la caña, con
    sus escamas, que viene de tierra (el cauce principal), los tres dedos, que son los pasos del río entre sus diques de barro, con sus
    almohadillas y sus uñas, y el dedo de atrás, corto (con el cielo atrás y los dedos lisos, parecía una horqueta o un tridente parado
    en el mar)"""
    J = (60, 24.6)
    cana = ([(60.6, 42.6), (60.3, 33), J], [6.4, 5.8, 5.4])
    dedos = [([J, (54.4, 18.8), (48.6, 13.6), (43.4, 9.4)], [4.8, 4, 3.2, 2.5]),
             ([J, (60, 17.6), (60.2, 11), (60.4, 5.4)], [4.8, 4, 3.2, 2.5]),
             ([J, (65.6, 18.8), (71.4, 13.6), (76.6, 9.4)], [4.8, 4, 3.2, 2.5]),
             ([J, (64.6, 28.6), (68, 31.6)], [3.6, 2.8, 2.2])]          # el dedo de atrás
    almohadillas = [ovalo(x, y, w * .68, w * .6) for p_, a_ in dedos for (x, y), w in zip(p_[1:-1], a_[1:-1])]
    puntas = [ovalo(p_[-1][0], p_[-1][1], a_[-1] * .56, a_[-1] * .5) for p_, a_ in dedos]
    pata = unary_union([cinta(*cana, 8)] + [cinta(p_, a_, 8) for p_, a_ in dedos] + almohadillas + puntas +
                       [ovalo(J[0], J[1], 4, 3.6)]).buffer(.5).buffer(-.5)
    for p_, a_ in dedos:                                                 # las uñas, oscuras, que siguen la dirección del dedo
        (xa, ya), (xb, yb) = p_[-2], p_[-1]
        d = np.array([xb - xa, yb - ya]) / math.hypot(xb - xa, yb - ya)
        n_ = np.array([-d[1], d[0]])
        b0 = np.array([xb, yb]) + d * a_[-1] * .25
        una = Polygon([tuple(b0 + n_ * a_[-1] * .42), tuple(b0 + d * a_[-1] * 1.6 + n_ * a_[-1] * .12), tuple(b0 - n_ * a_[-1] * .42)])
        l.masa(una.buffer(.1), material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3)
    t = l.masa(pata, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.5, escalon=.1, contraluz=.35)
    canales = unary_union([cinta(cana[0], [w * .2 for w in cana[1]], 8)] + [cinta(p_, [w * .2 for w in a_], 8) for p_, a_ in dedos[:3]])
    l.mancha(canales, '2F8A74', .8, dentro=t)                            # el río, que corre por adentro de cada dedo
    for y in np.arange(28.4, 42, 1.5):                                   # las escamas de la caña
        l.trazo([(57.4, y + .35), (60.4, y - .45), (63.4, y + .35)], .16, color='6B4E10', alfa=.6, dentro=t)
    for p_, a_ in dedos[:3]:                                             # los pliegues entre las almohadillas
        for (xa, ya), (xb, yb), w in zip(p_[1:-1], p_[2:], a_[2:]):
            xm, ym = (xa + xb) / 2, (ya + yb) / 2
            d = np.array([xb - xa, yb - ya]) / math.hypot(xb - xa, yb - ya)
            n_ = np.array([-d[1], d[0]])
            l.trazo([(xm + n_[0] * w * .5, ym + n_[1] * w * .5), (xm - n_[0] * w * .5, ym - n_[1] * w * .5)], .14, color='6B4E10', alfa=.55,
                    dentro=t)
    return pata


def mar(l):
    # visto desde arriba, sin cielo: el golfo de México, con el agua más clara y baja alrededor del delta, y la pata de pájaro dorada,
    # protagonista, echada en él
    m = l.masa(box(-2, -2, 122, 42), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    rng = np.random.default_rng(9)
    for _ in range(46):
        x, y = rng.uniform(-2, 116), rng.uniform(0, 40)
        l.trazo([(x, y), (x + 1.6, y - .3), (x + 3.2, y)], .16, color='A4DCC4', alfa=.6, dentro=m)
    sombra = Polygon([(60.6, 42.6), (54, 24), (40, 6), (60, 1), (80, 6), (70, 30), (61, 42.6)]).buffer(5)
    l.mancha(sombra, '64C8AA', .45, dentro=m, difuso=2.4)                # el agua baja del delta
    pata_de_pajaro(l)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Mineápolis', dibujar=mineapolis), dict(clave='San Luis', dibujar=san_luis),
            dict(clave='Memphis', dibujar=memphis), dict(clave='Baton Rouge', dibujar=baton_rouge),
            dict(clave='Nueva Orleans', dibujar=nueva_orleans), dict(clave='mar', dibujar=mar)]
LISTO = True
