# -*- coding: utf-8 -*-
"""Las postales del Níger, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol. El río es un bumerán de 4 200 km (naceNota y frase): el bumerán dorado
sale en el nacimiento, es la punta en Gao y vuelve en el mar.

- el nacimiento: las tierras altas de Guinea, verdes, con el Atlántico a la izquierda, a solo 240 km; el río joven le da la espalda y
  se va tierra adentro, y un bumerán dorado sale volando hacia el Sáhara;
- Bamako: «tres cocodrilos custodian el río»: tres cocodrilos dorados, como los del escudo, en la orilla del río ancho y lento;
  atrás, el puente y la ciudad;
- Mopti: «una Venecia de barro»: la ciudad de barro dorado, con la mezquita de torres y palos salientes, reflejada en los canales del
  delta interior, y las piraguas que hacen de taxi;
- Tombuctú: «sal del norte, oro del sur, libros en el medio»: el camello con sus barras de sal blanca, el cesto de oro y, al medio, el
  libro abierto de un manuscrito, de cantos dorados; atrás, la mezquita de Sankoré y las dunas;
- Gao: «la punta del bumerán»: visto desde arriba, el río que sube hacia el desierto y en Gao dobla al sureste, con un bumerán dorado
  echado sobre la curva; en la punta, la tumba de los Askia, la pirámide de barro;
- Niamey: «un país que se llama como el río»: un poste dorado con dos flechas que dicen lo mismo, NÍGER: una señala el río y la otra
  el país; al lado, una jirafa, de las últimas de África occidental;
- Lokoja: «un cruce loco: entra el Benue y el río duplica su tamaño»: un policía de tránsito, de uniforme dorado, dirige con su
  silbato el cruce de los dos ríos, que se arremolinan; abajo, el río juntado, el doble de ancho; atrás, el monte Patti;
- Port Harcourt: «torres de petróleo entre manglares y llamas de gas de noche»: de noche, las torres de petróleo oscuras entre los
  manglares y las llamas de gas, doradas, que se reflejan en el río;
- el mar: el golfo de Guinea, con los manglares, una plataforma de petróleo y un barco; el bumerán dorado vuelve a la costa, a 240 km
  de donde salió (la pinaza no sale al golfo).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, piedra, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
BARRO = '8A6A3A'           # el barro de las casas, cuando no es lo que hay que recordar


def piel(l, piezas, tono=.55):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    l.mancha(unary_union(piezas).buffer(1), '5A3E1E', .25, dentro=m)
    return m


def bumeran(x, y, largo, abre=118.0, giro=0.0, ancho=.18):
    """un bumerán: dos brazos curvos que se juntan en el codo, con las puntas redondeadas; (x, y) es el codo"""
    brazos = []
    for lado in (-1, 1):
        a = math.radians(giro + lado * abre / 2 - 90)
        pts = [(x + largo * t * math.cos(a) + lado * largo * .12 * math.sin(math.pi * t) * math.sin(a),
                y + largo * t * math.sin(a) - lado * largo * .12 * math.sin(math.pi * t) * math.cos(a)) for t in np.linspace(0, 1, 9)]
        brazos.append(tubo(pts, [largo * ancho * .55] + [largo * ancho * .5] * 7 + [largo * ancho * .42], 6))
    return unary_union(brazos + [ovalo(x, y, largo * ancho * .55, largo * ancho * .55)])


def pinta_bumeran(l, g):
    m = l.masa(g, material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    c = g.centroid
    for k in range(3):                                                   # las rayas pintadas, como en los de verdad
        l.trazo([(c.x - 4 + k * 4, c.y - 6), (c.x - 2 + k * 4, c.y + 6)], .3, color='6B4E10', alfa=.5, dentro=m)
    return m


def adobe(l, x0, x1, base, alto_, material='acento', tono=0.0, torres=3, puerta=True):
    """una casa o una mezquita de barro, al estilo del Sahel: muros gruesos, torres con pináculos redondeados y los palos de madera que
    salen del muro (para el andamio del reenlucido anual)"""
    w = x1 - x0
    piezas = [box(x0, base - alto_, x1, base).buffer(.4)]
    for k in range(torres):
        tx = x0 + w * (k + .5) / torres
        piezas.append(forma([(tx - 1.4, base - alto_ + .4), (tx - 1.2, base - alto_ - 3.6), (tx - .6, base - alto_ - 5.4), (tx, base - alto_ - 6),
                             (tx + .6, base - alto_ - 5.4), (tx + 1.2, base - alto_ - 3.6), (tx + 1.4, base - alto_ + .4)], 1))
    for k in range(int(w // 2.4) + 1):                                   # los pináculos chicos del borde
        px = x0 + .6 + k * 2.4
        if px < x1 - .4:
            piezas.append(forma([(px - .5, base - alto_ + .3), (px - .3, base - alto_ - 1.4), (px, base - alto_ - 1.8), (px + .3, base - alto_ - 1.4),
                                 (px + .5, base - alto_ + .3)], 1))
    m = l.masa(piezas, material=material, alto=.4, brillo=.3, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.35)
    if tono:
        l.mancha(unary_union(piezas).buffer(1), BARRO, tono, dentro=m)
    for y in np.arange(base - alto_ + 1.6, base - 1, 2.6):              # los palos que salen
        for x in np.arange(x0 + 1, x1 - .6, 2.4):
            l.trazo([(x - .2, y), (x + .7, y + .1)], .26, color='5A3E1E', alfa=.85)
    if puerta:
        cx = (x0 + x1) / 2
        l.mancha(forma([(cx - 1.3, base), (cx - 1.3, base - 3), (cx, base - 4), (cx + 1.3, base - 3), (cx + 1.3, base)], 1), '0C3A33', .8, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    cielo(l, sol=None)
    nube(l, 30, 5, 12, .5)
    nube(l, 100, 4, 12, .45)
    # a la izquierda, lejos, el Atlántico, a solo 240 km; las tierras altas de Guinea, verdes, con su selva
    m = l.masa(box(-2, 15.6, 30, 19), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 15.6, 30, 16.8), '64C8AA', .5, dentro=m)
    cordillera(l, [(18, 22), (30, 14), (44, 10.4), (58, 12.6), (72, 9.4), (88, 12), (104, 10), (122, 14)], material='cuerpo')
    selva(l, 20, 122, 21, 5, semilla=2, emergentes=4)
    prado(l, 20.6, 41, .2)
    # el río joven, que le da la espalda al mar y se va tierra adentro, hacia la derecha y hacia el fondo
    agua(l, cinta([(30, 41.6), (40, 36), (60, 33), (80, 29), (96, 25.6), (112, 23.4), (124, 22.6)], [7, 6, 5, 4, 3, 2.2, 1.6], 8), ondas=6, semilla=3,
         linea=.3)
    for x, y, r in ((8, 34, 2.8), (16, 39, 3), (108, 34, 3), (116, 39.4, 3.4), (96, 38.6, 2.4)):
        arbol(l, x, y, r, semilla=int(x))
    pasto(l, 0, 120, 26, 40.6, 20, semilla=4)
    # el bumerán dorado, protagonista, que sale volando hacia el Sáhara, con la estela de su vuelta
    c = curva([(30, 30), (40, 18), (54, 12.6)], 10)
    for k in range(0, len(c) - 1, 2):
        l.trazo([tuple(c[k]), tuple(c[k + 1])], .35, color='FFFFFF', alfa=.9)
    pinta_bumeran(l, bumeran(66, 13.4, 13, 116, 30))


# ------------------------------------------------------------------------------------------------ Bamako
def cocodrilo(l, x, base, s=1.0, lado=1):
    """un cocodrilo dorado, echado de perfil, mirando a `lado`, con la cabeza levantada: el hocico largo con sus dientes, el ojo alto,
    las patas cortas, el lomo de escamas y la cola larga; (x, base) es el suelo bajo el medio"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    cuerpo = [forma(P([(-8, -1.4), (-6, -5.2), (0, -6.4), (6, -6), (9.4, -6.2), (12.6, -7.4), (17.6, -6.8), (19.4, -5.8), (17, -4.8), (12.4, -4),
                       (9, -2), (6, -1), (-6, -.8)]), 2),
              tubo(P([(-7.6, -2.6), (-13, -2), (-18, -1), (-22, -.4)]), [3.2 * s, 2.2 * s, 1.2 * s, .3 * s], 8),
              tubo(P([(4.6, -2), (5.8, 0)]), [1.4 * s, 1.1 * s], 4), tubo(P([(-4, -2), (-5.2, 0)]), [1.4 * s, 1.1 * s], 4)]
    c = l.masa(cuerpo, material='acento', alto=.45, brillo=.4, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    for u in np.arange(-18, 8, 1.6):                                     # las escamas del lomo
        v = -6 if u > -6 else -3.6 + (u + 6) * .14
        l.trazo(P([(u, v), (u + .8, v - .7), (u + 1.6, v)]), .14 * s, color='6B4E10', alfa=.7, dentro=c)
    for u in np.arange(13, 18.4, 1.2):                                   # los dientes
        l.trazo(P([(u, -4.8), (u + .3, -4)]), .18 * s, color='FFFFFF', alfa=.95)
    l.masa(ovalo(x + lado * 11 * s, base - 7.6 * s, 1.4 * s, 1.2 * s), material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(x + lado * 11.2 * s, base - 7.7 * s, .5 * s, .45 * s), '05201C', 1)
    return c


def bamako(l):
    cielo(l, sol=None)
    nube(l, 24, 4.4, 12, .5)
    nube(l, 98, 4, 12, .45)
    # enfrente, la ciudad baja y el puente largo sobre el río ancho y lento
    prado(l, 15, 20, .3)
    for x in np.arange(0, 122, 3.8):
        h = 2.6 + (x * 7 % 3)
        l.masa(box(x, 18.2 - h, x + 3.2, 18.4), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    rio(l, 19.4)
    l.masa(box(-2, 18.2, 122, 19.2), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    for x in np.arange(4, 122, 7):
        l.masa(box(x - .6, 19, x + .6, 22.4), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)
    # la orilla de arena de adelante y los tres cocodrilos, protagonistas, que custodian el río
    m = orilla(l, forma([(-2, 41.5), (-2, 30.4), (30, 28.6), (60, 28.2), (90, 28.6), (122, 30.4), (122, 41.5)], 2), tinte=.36)
    pasto(l, 0, 120, 31, 40.6, 12, semilla=5, dentro=m)
    for x, y, s, lado in ((36, 32.6, .9, 1), (82, 33.2, .9, -1), (60, 39, 1.12, 1)):
        l.mancha(ovalo(x, y + .2, 14 * s, 1), '0C3A33', .2, difuso=.5)
        cocodrilo(l, x, y, s, lado)


# ------------------------------------------------------------------------------------------------ Mopti
def piragua(l, x, y, s=1.0, lado=1, techo=True):
    """una piragua de madera, larga y de puntas altas, con su techo de esteras y su barquero con la pértiga: el taxi del río"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    if techo:
        l.masa(forma(P([(-3.4, -1.4), (-3, -4.2), (0, -5.2), (3, -4.2), (3.4, -1.4)]), 1), material='claro', alto=.25, brillo=.15, vientre=0,
               hondo=0, linea=.3)
    c = l.masa(forma(P([(-11, -3.2), (-9, -1.4), (9, -1.4), (11, -3.2), (10.4, -.6), (8, .6), (-8, .6), (-10.4, -.6)]), 1), material='vientre',
               alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(Polygon(P([(-12, -4), (12, -4), (12, 1), (-12, 1)])), '5A3E1E', .55, dentro=c)
    for u in (-6, -2, 2, 6):                                             # las bandas pintadas
        l.trazo(P([(u, -1.2), (u + .2, .4)]), .4 * s, color='FFFFFF', alfa=.6, dentro=c)
    px, py = x + lado * 7 * s, y - 1.4 * s                               # el barquero y la pértiga
    piel(l, [ovalo(px, py - 4.4 * s, .8 * s, .9 * s)], .55)
    l.masa(forma([(px - .9 * s, py), (px - 1 * s, py - 3.2 * s), (px + 1 * s, py - 3.2 * s), (px + .9 * s, py)], 1), material='claro', alto=.3,
           brillo=.2, vientre=0, hondo=0, linea=.25)
    l.trazo([(px - lado * 2 * s, py + 2 * s), (px + lado * 2.4 * s, py - 8 * s)], .2 * s, color='5A3E1E', alfa=.9)
    return c


def mopti(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    # el delta interior: el agua por todas partes, y la ciudad de barro dorado que se mira en ella, con su mezquita
    prado(l, 17, 21, .3)
    a = rio(l, 20.4)
    for x0, x1, h, torres in ((-1, 16, 6, 1), (16, 30, 8, 2), (86, 100, 7.4, 2), (100, 121, 6, 1)):
        g = adobe(l, x0, x1, 21, h, torres=torres)
    mez = adobe(l, 38, 82, 21, 11.4, torres=3)
    reflejo(l, box(-2, 2, 122, 21), 21, .3, 'F2D48A')
    # los canales en primer plano, con sus orillas, y las piraguas taxi
    for g in (forma([(-2, 41.5), (-2, 30), (14, 29.4), (24, 31), (18, 41.5)], 2), forma([(98, 41.5), (104, 31), (112, 29.2), (122, 29.6), (122, 41.5)], 2)):
        orilla(l, g, tinte=.34)
    piragua(l, 44, 30.6, 1.1, 1)
    piragua(l, 78, 36.4, 1.25, -1)
    piragua(l, 28, 37.6, .9, 1, techo=False)


# ------------------------------------------------------------------------------------------------ Tombuctú
def camello(l, x, base, s=1.0, lado=1):
    """un dromedario de perfil, mirando a `lado`, cargado con barras de sal blanca a los lados de la joroba"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    patas = [tubo(P([(u, -6.6), (u + d, -3.4), (u, 0)]), [1 * s, .7 * s, .6 * s], 5) for u, d in ((-5, -.6), (-3.4, .4), (3.4, -.4), (5, .5))]
    cuerpo = [forma(P([(-6.4, -6), (-6.6, -9), (-4, -11), (-1.6, -14.4), (1.4, -14.6), (3.6, -11.4), (6, -10.4), (6.8, -7.6), (5.6, -6)]), 2),
              tubo(P([(5.6, -9.6), (8.6, -12), (9.6, -16), (11.4, -17.4)]), [2 * s, 1.4 * s, 1.2 * s, 1.1 * s], 8), ovalo(x + lado * 12 * s, base - 17 * s, 2 * s, 1.3 * s),
              tubo(P([(-6.4, -9), (-7.6, -6.6), (-7.2, -4.6)]), [.4 * s, .3 * s, .3 * s], 4)]
    c = l.masa(patas + cuerpo, material='vientre', alto=.45, brillo=.2, vientre=0, hondo=.1, linea=.4, contraluz=.3)
    l.mancha(unary_union(patas + cuerpo).buffer(1), BARRO, .45, dentro=c)
    l.mancha(ovalo(x + lado * 12.4 * s, base - 17.6 * s, .35 * s, .35 * s), '05201C', 1)
    sal = [Polygon(P([(-5.4, -10.6), (-1, -12.6), (-.6, -9), (-5, -7.4)])), Polygon(P([(1, -12.6), (5.4, -10.6), (5, -7.4), (.6, -9)]))]
    sl = l.masa(sal, material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.35)
    l.mancha(unary_union(sal).buffer(.5), '9DB9B0', .45, dentro=sl)      # la sal, gris, en losas, atadas con sogas (blancas y lisas,
    for g in sal:                                                       # parecían libros)
        c0, c1, c2, c3 = [np.array(q) for q in g.exterior.coords[:4]]
        for f in (.3, .7):
            l.trazo([tuple(c0 + (c1 - c0) * f), tuple(c3 + (c2 - c3) * f)], .2 * s, color='5A3E1E', alfa=.85)
        l.trazo([tuple(c0 + (c3 - c0) * .5), tuple(c1 + (c2 - c1) * .5)], .08 * s, color='6FA497', alfa=.8)
    return c


def libro_abierto(l, x, y, w, h):
    """un manuscrito abierto sobre su atril: las tapas de cuero dorado, anchas, las dos páginas de pergamino, con sus renglones de
    letra y la orla y el título dorados de cada página (con las tapas finas, lo dorado del cuadro era el oro del cesto)"""
    at = [tubo([(x - w * .36, y + .4), (x + w * .3, y + h * .62)], [1, .9], 3), tubo([(x + w * .36, y + .4), (x - w * .3, y + h * .62)], [1, .9], 3)]
    a = l.masa(at, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)               # el atril de madera, en X
    l.mancha(unary_union(at).buffer(1), '5A3E1E', .6, dentro=a)
    tapa = Polygon([(x - w / 2 - 1.6, y + 1.2), (x, y + 2.4), (x + w / 2 + 1.6, y + 1.2), (x + w / 2 + 1.6, y - h - .4), (x, y - h + .8),
                    (x - w / 2 - 1.6, y - h - .4)])
    l.masa(tapa, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for lado in (-1, 1):
        pg = Polygon([(x, y + .6), (x + lado * w / 2, y - .4), (x + lado * w / 2, y - h), (x, y - h + 1.2)])
        p = l.masa(pg, material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
        l.mancha(pg.buffer(1), 'FBEFCB', .5, dentro=p)
        for k in range(2, 9):                                            # los renglones, en curva como la página
            f = k / 9.6
            a0 = (x + lado * w * .08, y - h + 1.2 + (h - 1.2) * f + .3)
            a1 = (x + lado * w * .46, y - h + .2 + (h - .8) * f)
            l.trazo([a0, a1], .16, color='0C3A33', alfa=.65, dentro=p)
        f = 1 / 9.6                                                      # el título, dorado
        l.trazo([(x + lado * w * .1, y - h + 1.2 + (h - 1.2) * f + .3), (x + lado * w * .34, y - h + .3 + (h - .8) * f)], .5, color='E8B952',
                alfa=.95, dentro=p)
        l.trazo([(x + lado * w * .04, y - .1), (x + lado * w * .47, y - .9), (x + lado * w * .47, y - h + .1), (x + lado * w * .04, y - h + 1.5)],
                .22, color='E8B952', alfa=.9, dentro=p)                 # la orla


def tombuctu(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    # atrás, las dunas y la mezquita de Sankoré, con su torre de barro en pirámide y sus palos
    tierra(l, 14, 41, desierto=.5)
    for x0, w, h in ((-6, 40, 6), (24, 50, 4.4), (78, 48, 6.4)):
        l.mancha(ovalo(x0 + w / 2, 18, w / 2, h), 'BF9129', .3, difuso=1)
    m = l.masa([box(78, 15.6, 110, 21.4), forma([(86, 15.8), (87.4, 8.6), (89, 5.4), (91, 4.6), (93, 5.4), (94.6, 8.6), (96, 15.8)], 1)], material='vientre',
               alto=.35, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(box(76, 4, 112, 22), BARRO, .55, dentro=m)
    for y in np.arange(7, 15.6, 2.2):
        for x in np.arange(87.6, 95, 1.8):
            l.trazo([(x, y), (x + .5, y + .1)], .22, color='5A3E1E', alfa=.85)
    # al norte, a la izquierda, el camello con la sal; al sur, a la derecha, el cesto con el oro; y al medio, el libro, protagonista
    camello(l, 22, 37, 1.1, 1)
    cesto = forma([(92, 37.4), (90.6, 31.4), (106.4, 31.4), (105, 37.4)], 1)
    c = l.masa(cesto, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(cesto.buffer(1), '8A6A3A', .55, dentro=c)
    for y in (33, 35.2):
        l.trazo([(91, y), (106, y)], .14, color='5A3E1E', alfa=.6, dentro=c)
    pepitas = [ovalo(92 + k * 1.6 + rng.uniform(-.3, .3), 31 - (k % 3) * .9 - rng.uniform(0, .6), 1, .8) for k in range(9)]
    l.masa(pepitas, material='acento', alto=.6, brillo=.6, vientre=0, hondo=0, linea=.3, contraluz=.4)
    libro_abierto(l, 60, 31, 28, 15)


# ------------------------------------------------------------------------------------------------ Gao
def gao(l):
    rng = np.random.default_rng(8)
    cielo(l, sol=None)
    nube(l, 92, 3, 12, .4)
    # visto desde arriba: el desierto con sus dunas, y el río que sube hacia el Sáhara y en Gao dobla hacia el sureste
    tierra(l, 5, 41, desierto=.48)
    for _ in range(14):
        x, y = rng.uniform(0, 120), rng.uniform(7, 40)
        l.trazo([(x - 4, y + .6), (x, y - .6), (x + 4, y + .6)], .5, color='BF9129', alfa=.45)
    rio_ = cinta([(-2, 38), (16, 31), (34, 22), (50, 15), (60, 12.4), (70, 15), (86, 22), (104, 31), (124, 38.6)], [5, 5.2, 5.4, 5.6, 5.8, 6, 6.2, 6.4,
                                                                                                                 6.6], 8)
    agua(l, rio_, ondas=10, semilla=9, linea=.35)
    for g in (forma([(-2, 41.5), (-2, 39.6), (14, 33.4), (32, 24.6), (48, 18), (60, 15.6), (72, 18), (88, 24.6), (106, 33.4), (122, 40.4), (122, 41.5)], 2),):
        l.mancha(g.difference(rio_.buffer(.2)), '2F8A74', .14)            # la franja verde de las orillas
    # el bumerán dorado, protagonista, echado sobre la curva del río: la punta, en Gao
    pinta_bumeran(l, bumeran(60, 13.4, 30, 136, 180, .13))
    # la tumba de los Askia, la pirámide de barro con sus palos, en la punta
    t = l.masa(forma([(54.4, 11.6), (56, 6.4), (58, 4), (60, 3.2), (62, 4), (64, 6.4), (65.6, 11.6)], 1), material='vientre', alto=.35, brillo=.2,
               vientre=0, hondo=0, linea=.35)
    l.mancha(box(52, 2, 68, 12), BARRO, .6, dentro=t)
    for y in np.arange(5, 11, 1.6):
        for x in np.arange(56.6, 63.6, 1.6):
            l.trazo([(x, y), (x + .4, y + .1)], .2, color='5A3E1E', alfa=.85)


# ------------------------------------------------------------------------------------------------ Niamey
def letra(ch, x, y, h):
    """una letra de cartel, de palo, de alto `h`, con su pie izquierdo en (x, y); devuelve (polígono, ancho)"""
    g = .22 * h
    if ch == 'N':
        w = .66 * h
        return unary_union([box(x, y - h, x + g, y), box(x + w - g, y - h, x + w, y), Polygon([(x, y - h), (x + g * 1.2, y - h), (x + w, y),
                                                                                               (x + w - g * 1.2, y)])]), w
    if ch == 'Í':
        return unary_union([box(x, y - h, x + g, y), Polygon([(x + g * .2, y - h * 1.16), (x + g * 1.4, y - h * 1.42), (x + g * 1.6, y - h * 1.3),
                                                              (x + g * .5, y - h * 1.08)])]), g
    if ch == 'G':
        w = .66 * h
        aro = ovalo(x + w / 2, y - h / 2, w / 2, h / 2).difference(ovalo(x + w / 2, y - h / 2, w / 2 - g, h / 2 - g))
        aro = aro.difference(box(x + w / 2, y - h * .78, x + w + 1, y - h * .44))
        return unary_union([aro, box(x + w * .5, y - h * .5, x + w, y - h * .5 + g), box(x + w - g, y - h * .5, x + w, y - h * .14)]), w
    if ch == 'E':
        w = .56 * h
        return unary_union([box(x, y - h, x + g, y), box(x, y - h, x + w, y - h + g), box(x, y - h / 2 - g / 2, x + w * .82, y - h / 2 + g / 2),
                            box(x, y - g, x + w, y)]), w
    if ch == 'R':
        w = .62 * h
        lazo = ovalo(x + w * .45, y - h * .72, w * .5, h * .28).difference(ovalo(x + w * .45, y - h * .72, w * .5 - g, h * .28 - g))
        return unary_union([box(x, y - h, x + g, y), lazo.difference(box(x - 1, y - h, x + w * .45, y)), box(x, y - h, x + w * .45, y - h + g),
                            box(x, y - h * .44 - g, x + w * .45, y - h * .44),
                            Polygon([(x + w * .3, y - h * .46), (x + w * .3 + g * 1.1, y - h * .46), (x + w, y), (x + w - g * 1.2, y)])]), w
    raise ValueError(ch)


def palabra(texto, x, y, h, esp=.16):
    """las letras de una palabra, una al lado de la otra, desde (x, y); devuelve (polígono, ancho)"""
    piezas, x0 = [], x
    for ch in texto:
        g, w = letra(ch, x0, y, h)
        piezas.append(g)
        x0 += w + esp * h
    return unary_union(piezas), x0 - x - esp * h


def flecha(l, x0, x1, y, alto_, texto):
    """una flecha de madera del poste, dorada, de x0 a x1 (la punta en x1), con su texto en letras oscuras"""
    lado = 1 if x1 > x0 else -1
    f = Polygon([(x0, y - alto_ / 2), (x1 - lado * alto_ * .6, y - alto_ / 2), (x1, y), (x1 - lado * alto_ * .6, y + alto_ / 2), (x0, y + alto_ / 2)])
    m = l.masa(f, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.45, contraluz=.35)
    g, w = palabra(texto, 0, 0, alto_ * .58)
    cx = (x0 + x1 - lado * alto_ * .3) / 2
    l.mancha(affinity.translate(g, cx - w / 2, y + alto_ * .29), '3A2A0A', .95, dentro=m)
    return m


def jirafa(l, x, base, s=1.0, lado=1):
    """una jirafa de perfil, mirando a `lado`: las patas largas, el cuello largo, la cabeza con sus cuernitos y sus manchas"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    patas = [tubo(P([(u, -10), (u + .2, -5), (u, 0)]), [.7 * s, .5 * s, .45 * s], 4) for u in (-3.4, -2.2, 2.6, 3.8)]
    cuerpo = [forma(P([(-4.4, -10), (-4.6, -12.6), (-2, -14.2), (3.6, -15.6), (5, -13), (4.4, -10)]), 2),
              tubo(P([(3.4, -13.6), (5.4, -19.6), (7, -25)]), [1.6 * s, 1.1 * s, .8 * s], 6), forma(P([(6, -24.6), (7, -26.6), (9.6, -25.8), (10, -24.4), (7.4, -23.6)]), 1),
              tubo(P([(6.8, -26.2), (6.6, -27.8)]), [.25 * s, .2 * s], 3), tubo(P([(7.6, -26.4), (7.6, -28)]), [.25 * s, .2 * s], 3),
              tubo(P([(-4.4, -12.6), (-5.6, -9.6), (-5.4, -7.4)]), [.3 * s, .25 * s, .2 * s], 4)]
    c = l.masa(patas + cuerpo, material='vientre', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.mancha(unary_union(patas + cuerpo).buffer(1), 'D8C49A', .55, dentro=c)
    rng = np.random.default_rng(3)
    for _ in range(26):                                                  # las manchas
        u, v = rng.uniform(-4, 6.4), rng.uniform(-24, -10.6)
        if v < -15 and abs(u - (3.6 + (-15 - v) * .3)) > 1:
            continue
        l.mancha(ovalo(x + lado * u * s, base + v * s, .6 * s, .5 * s, rng.uniform(0, 90)), '8A6A3A', .8, dentro=c)
    l.mancha(ovalo(x + lado * 8 * s, base - 25.6 * s, .3 * s, .3 * s), '05201C', 1)
    return c


def niamey(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 104, 3.6, 10, .4)
    # el río a la izquierda, y a la derecha la ciudad: la gran avenida junto al agua, con sus árboles
    prado(l, 16, 41, .32)
    agua(l, forma([(-2, 16.6), (40, 16.6), (46, 24), (40, 32), (30, 41.6), (-2, 41.6)], 2), ondas=10, semilla=10, linea=.35)
    avenida = Polygon([(52, 16.8), (122, 16.8), (122, 22.6), (60, 19)])
    l.masa(avenida, material='claro', alto=.1, brillo=.05, vientre=0, hondo=0, linea=.3)
    for x in np.arange(56, 122, 6):
        arbol(l, x, 16.4 - (x - 56) * .01, 1.4, material='cuerpo', semilla=int(x))
    for x in np.arange(60, 122, 7.6):
        h = 3 + (x * 3 % 4)
        l.masa(box(x, 14.4 - h, x + 5, 14.6), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.22, arroja=False)
    # una jirafa, de las últimas de África occidental, y el poste dorado, protagonista: las dos flechas dicen lo mismo
    jirafa(l, 98, 38.4, .82, -1)
    l.masa(box(59.2, 6, 60.8, 39), material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    flecha(l, 61, 30, 13.4, 7.4, 'NÍGER')
    flecha(l, 59, 92, 24, 7.4, 'NÍGER')
    l.mancha(ovalo(60, 39.2, 4, .8), '0C3A33', .25, difuso=.4)


# ------------------------------------------------------------------------------------------------ Lokoja
def policia(l, x, base, s=1.0):
    """un policía de tránsito, de frente, con el uniforme y la gorra dorados, que abre los brazos con los guantes blancos y toca el
    silbato; (x, base) es el pie"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-1.7, -.3, 1.2, .55), O(1.7, -.3, 1.2, .55)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    uni = [tubo(P([(-1.3, -8), (-1.5, -4), (-1.7, -.6)]), [1.2 * s, 1.1 * s, 1 * s], 5), tubo(P([(1.3, -8), (1.5, -4), (1.7, -.6)]), [1.2 * s, 1.1 * s, 1 * s], 5),
           forma(P([(-2.8, -15.6), (2.8, -15.6), (3.2, -12.4), (2.9, -7.6), (-2.9, -7.6), (-3.2, -12.4)]), 1),
           tubo(P([(-2.6, -14.8), (-5.6, -15.4), (-8.8, -16.6)]), [.9 * s, .8 * s, .7 * s], 6), tubo(P([(2.6, -14.8), (5.6, -16.6), (8.4, -19.4)]), [.9 * s, .8 * s, .7 * s], 6)]
    u = l.masa(uni, material='acento', alto=.45, brillo=.4, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.trazo(P([(0, -15.4), (0, -7.8)]), .14 * s, color='6B4E10', alfa=.6, dentro=u)
    l.trazo(P([(-2.9, -8.4), (2.9, -8.4)]), .5 * s, color='5A3E1E', alfa=.85, dentro=u)     # el cinturón
    l.masa([O(-9.6, -16.8, 1.1, 1), O(9.2, -19.8, 1.1, 1)], material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)   # los guantes
    piel(l, [O(0, -18.4, 2.3, 2.5), box(x - .7 * s, base - 16.4 * s, x + .7 * s, base - 15.4 * s)], .6)
    l.masa([forma(P([(-2.6, -20), (-2.4, -21.6), (0, -22.4), (2.4, -21.6), (2.6, -20)]), 1), O(0, -19.9, 3, .55)], material='acento', alto=.4, brillo=.4,
           vientre=0, hondo=0, linea=.35)                                # la gorra con su visera
    for dx in (-.9, .9):
        l.mancha(O(dx, -18.8, .28, .3), '05201C', 1)
    l.masa([O(.9, -16.9, .8, .45), box(x + 1.4 * s, base - 17.2 * s, x + 2.4 * s, base - 16.6 * s)], material='claro', alto=.3, brillo=.4, vientre=0,
           hondo=0, linea=.2)                                           # el silbato
    for k in range(3):                                                   # el pitido
        l.trazo(P([(3 + k * .9, -17.8 - k * .6), (3.6 + k * 1, -18.6 - k * .7)]), .14 * s, color='FFFFFF', alfa=.9)
    return u


def lokoja(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 24, 3.6, 12, .45)
    # atrás, el monte Patti, de cima chata; visto desde arriba, el Níger que llega por la izquierda y el Benue por la derecha
    l.masa(forma([(30, 12), (36, 6), (48, 4.6), (62, 5), (70, 9), (74, 12)], 2), material='cuerpo', alto=.3, brillo=.08, vientre=0, hondo=0,
           linea=.35)
    tierra(l, 10, 41, desierto=.22)
    niger_ = cinta([(-2, 14), (20, 16), (40, 20.4), (56, 24)], [7, 7.4, 7.6, 7.8], 8)
    benue = cinta([(122, 14), (100, 16), (80, 20.4), (64, 24)], [7, 7.4, 7.6, 7.8], 8)
    junto = cinta([(60, 22), (60, 30), (60, 41.6)], [12, 15, 17], 6)      # el río juntado, el doble de ancho
    a = agua(l, unary_union([niger_, benue, junto]).buffer(.3).buffer(-.3), ondas=0, linea=.35)
    l.mancha(benue, 'C6B98A', .4, dentro=a, difuso=1)
    for k in range(4):                                                   # el remolino del cruce loco
        r = 2 + k * 1.8
        l.trazo([(60 + r * math.cos(t), 26 + r * .5 * math.sin(t)) for t in np.linspace(k, k + 4.6, 20)], .22, color='FFFFFF', alfa=.85)
    for x, y, lado in ((26, 17.6, 1), (94, 17.4, -1), (52, 36, 1), (70, 38.6, -1)):      # las barcas, que van para todos lados
        l.masa(forma([(x - 3 * lado, y - .5), (x + 3 * lado, y - .5), (x + 2.2 * lado, y + .7), (x - 2.2 * lado, y + .7)], 1), material='vientre',
               alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        l.trazo([(x - 3.6 * lado, y), (x - 6 * lado, y + .4)], .16, color='FFFFFF', alfa=.7)
    # el policía de tránsito, protagonista, en su tarima en medio del cruce
    piedra(l, ovalo(60, 27, 6, 1.6), .2, .35)
    policia(l, 60, 26.6, 1.12)


# ------------------------------------------------------------------------------------------------ Port Harcourt
def llama(l, x, y, h, s=1.0):
    """una llama de gas, dorada, en la punta de su chimenea, con su resplandor"""
    l.mancha(ovalo(x, y - h * .4, h * .9, h * .8), 'F2D48A', .3, difuso=2)
    g = forma([(x - 1.6 * s, y), (x - 2 * s, y - h * .4), (x - .8 * s, y - h * .7), (x - .4 * s, y - h * .5), (x, y - h), (x + .8 * s, y - h * .6),
               (x + 1.4 * s, y - h * .7), (x + 2 * s, y - h * .3), (x + 1.4 * s, y)], 2)
    m = l.masa(g, material='acento', alto=.4, brillo=.6, vientre=0, hondo=0, linea=.3, contraluz=.4)
    l.mancha(forma([(x - .7 * s, y), (x - .5 * s, y - h * .4), (x, y - h * .6), (x + .5 * s, y - h * .4), (x + .7 * s, y)], 1), 'FBEFCB', .9, dentro=m)
    return g


def torre_petroleo(l, x, base, h, w):
    """una torre de petróleo de celosía, oscura contra la noche"""
    l.trazo([(x - w / 2, base), (x, base - h)], .3, color='05201C', alfa=.95)
    l.trazo([(x + w / 2, base), (x, base - h)], .3, color='05201C', alfa=.95)
    for k in range(1, 6):
        f = k / 6
        y = base - h * f
        wf = w / 2 * (1 - f)
        l.trazo([(x - wf, y), (x + wf, y)], .16, color='05201C', alfa=.9)
        if k < 5:
            y2 = base - h * (k + 1) / 6
            wf2 = w / 2 * (1 - (k + 1) / 6)
            l.trazo([(x - wf, y), (x + wf2, y2)], .12, color='05201C', alfa=.8)


def port_harcourt(l):
    rng = np.random.default_rng(14)
    # de noche: el cielo oscuro con sus estrellas
    l.mancha(box(0, 0, 120, 40), '0C3A33', 1)
    l.mancha(box(0, 14, 120, 24), '245E53', .6, difuso=3)
    for _ in range(40):
        x, y = rng.uniform(0, 120), rng.uniform(0, 14)
        l.mancha(ovalo(x, y, .18, .18), 'FFFFFF', rng.uniform(.5, 1))
    # los manglares, negros, y el río que refleja las llamas
    m = l.masa(box(-2, 23, 122, 41.5), material='oscuro', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 23, 122, 41.5), '154A41', .6, dentro=m)
    for x0, x1, y in ((-2, 44, 23.4), (78, 122, 23.4), (-2, 18, 34), (104, 122, 33)):
        for x in np.arange(x0 + 2, x1 - 1, 4.4):
            h = rng.uniform(6, 9)
            l.masa([tubo([(x + d * .5, y - h * .4), (x + d, y + .4)], [.18, .1], 4) for d in (-2.4, -1, 1, 2.4)] +
                   [ovalo(x, y - h * .8, h * .4, h * .26)], material='oscuro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25, arroja=False)
    # las torres de petróleo, oscuras, y las llamas de gas, doradas, protagonistas, con su reflejo en el río
    for x, h in ((30, 15), (92, 13)):
        torre_petroleo(l, x, 23.6, h, 6)
    llamas = []
    for x, y, h in ((48, 12.6, 9), (60, 9, 12.4), (72, 12.6, 9)):
        l.masa(box(x - .8, y, x + .8, 23.8), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
        l.mancha(box(x - .9, y - .2, x + .9, 23.8), '245E53', .5)
        llamas.append(llama(l, x, y, h, 1.2))
    for g in llamas:
        reflejo(l, affinity.translate(g, 0, 23.8 - g.bounds[3]), 23.8, .45, 'F2D48A')


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    rng = np.random.default_rng(16)
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .5)
    nube(l, 98, 4, 12, .45)
    # el golfo de Guinea, con una plataforma de petróleo y un barco
    horizonte = 18
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 1.8), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    pl = l.masa([box(84, horizonte - 3.4, 98, horizonte - 2.4), box(85, horizonte - 2.6, 86, horizonte + .4), box(96, horizonte - 2.6, 97, horizonte + .4),
                 box(88, horizonte - 6, 92, horizonte - 3.2)], material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    l.trazo([(93.4, horizonte - 3.4), (95, horizonte - 11)], .2, color='0C3A33', alfa=.9)
    l.trazo([(96.6, horizonte - 3.4), (95, horizonte - 11)], .2, color='0C3A33', alfa=.9)
    l.masa([forma([(14, horizonte - .4), (32, horizonte - .4), (33.4, horizonte - 1.8), (13.4, horizonte - 1.8)], 1), box(15, horizonte - 3.6, 19, horizonte - 1.7)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # los manglares del delta, a los costados
    for x0, x1, y in ((-2, 26, 30), (-2, 14, 39), (98, 122, 29), (108, 122, 39.6)):
        for x in np.arange(x0 + 2, x1 - 1, 5.4):
            mangle(l, x + rng.uniform(-1, 1), y, rng.uniform(7, 9.6), semilla=int(x * 5))
    # la playa de adelante, adonde vuelve el bumerán
    playa = forma([(20, 41.6), (28, 35.6), (50, 33.6), (70, 33.6), (92, 35.6), (100, 41.6)], 2)
    orilla(l, playa, tinte=.4)
    l.trazo([(26, 36.4), (50, 34.4), (70, 34.4), (94, 36.4)], .2, color='FFFFFF', alfa=.7)
    # el bumerán dorado, protagonista, que vuelve: la estela de su vuelta enorme y él, llegando a la costa, con su sombra en la arena
    c = curva([(118, 4), (100, 1.6), (80, 5), (68, 12)], 12)
    for k in range(0, len(c) - 1, 2):
        l.trazo([tuple(c[k]), tuple(c[k + 1])], .35, color='FFFFFF', alfa=.9)
    l.mancha(ovalo(58, 37.6, 12, 1.6), '0C3A33', .22, difuso=.6)
    pinta_bumeran(l, bumeran(58, 22, 17, 116, 205, .17))


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Bamako', dibujar=bamako), dict(clave='Mopti', dibujar=mopti),
            dict(clave='Tombuctú', dibujar=tombuctu), dict(clave='Gao', dibujar=gao), dict(clave='Niamey', dibujar=niamey),
            dict(clave='Lokoja', dibujar=lokoja), dict(clave='Port Harcourt', dibujar=port_harcourt), dict(clave='mar', dibujar=mar)]
LISTO = True
