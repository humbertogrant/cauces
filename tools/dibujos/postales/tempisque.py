# -*- coding: utf-8 -*-
"""Las postales del Tempisque, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: la cordillera de Guanacaste con el cono del volcán Orosí, el río que baja de su pie y cruza el llano seco, y un árbol
  de guanacaste dorado, el árbol que le da nombre a la provincia, con su copa enorme y chata;
- Liberia: «una ciudad pintada de blanco donde todos usan sombrero de sabanero»: las casas blancas de techo de teja y la iglesia, y
  adelante un sabanero de camisa blanca y una vaca cebú, los dos con su sombrero dorado;
- Guardia: «un guardia con machete y sombrero cuida un puente sobre el río»: el guardia, de uniforme dorado, de pie en el puente, con
  el machete al hombro; abajo, el río de piedras y pozas;
- Filadelfia: «un queso crema gigante flota río abajo con sombrero de paja»: el queso, envuelto en su papel dorado y abierto arriba,
  con su sombrero, que flota en el río crecido entre los arrozales;
- Bolsón: «un bolsón lleno de maíz se sube a un bongo de un solo tronco»: el bolsón dorado, con las mazorcas que asoman, que pasa del
  muelle al bongo;
- Puerto Humo: «un muelle tapado por el humo de los fogones donde hierven las ollas de arroz»: las ollas doradas que hierven sobre sus
  fogones y el humo que tapa el muelle; enfrente, el humedal de Palo Verde con sus garzas y espátulas, y un cocodrilo en el barro;
- el mar: el bongo, la barca del juego, de casco dorado y con su vela, que entra al golfo de Nicoya entre los manglares; enfrente,
  la lengua de arena de Puntarenas, y atrás, lejos, el puente largo cerca de la boca.
"""
import math

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, juncos, mangle, nube, orilla, palmera, pasto, prado,  # noqa: F401
                     reflejo, rio, tierra)
from pintor import forma, ovalo, tubo

PIEL = 'A2683A'            # el tono de la piel: un café tibio sobre el pálido de `vientre` (con el dorado oscuro salía verde oliva)
PAJA = 'D2B070'            # la paja de los sombreros
TEJA = 'B0603A'            # el barro cocido de las tejas
SECO = '8A6A3A'            # el pasto seco del llano


def piel(l, piezas, tono=.5):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def llano(l, pts, tinte=.42):
    """el llano guanacasteco, seco: un prado amarillo, sin línea, que empieza en el perfil `pts`"""
    g = Polygon([(-2, 41.6)] + pts + [(122, 41.6)]).buffer(0)
    m = l.masa(g, material='vientre', alto=.08, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(g, 'E8B952', tinte, dentro=m)
    return m


def pasto_seco(l, x0, x1, y0, y1, n, semilla=0, dentro=None):
    """matas de pasto seco, del color de la paja"""
    rng = np.random.default_rng(semilla)
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        s = .6 + (y - y0) / max(y1 - y0, 1) * .6
        for dx, h in ((-.7, 1.1), (0, 1.5), (.7, 1.1)):
            l.trazo([(x + dx * s * .4, y), (x + dx * s, y - h * s)], .12 * s + .04, color=SECO, alfa=.7, dentro=dentro)


def casa(l, x, base, w, h):
    """una casa de adobe encalada, blanca, con su techo de teja, su puerta y sus ventanas"""
    c = l.masa(box(x, base - h, x + w, base).buffer(.05), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25, arroja=False)
    l.mancha(box(x + w * .42, base - h * .66, x + w * .58, base), '164F46', .8, dentro=c)
    for u in (.12, .72):
        l.mancha(box(x + w * u, base - h * .62, x + w * (u + .16), base - h * .3), '164F46', .7, dentro=c)
    techo = Polygon([(x - .7, base - h + .3), (x + .5, base - h - 1.9), (x + w - .5, base - h - 1.9), (x + w + .7, base - h + .3)])
    t = l.masa(techo, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25, arroja=False)
    l.mancha(techo.buffer(.5), TEJA, .75, dentro=t)
    for k in np.arange(x + .4, x + w, .9):                               # las hileras de tejas
        l.trazo([(k, base - h - 1.7), (k - .3, base - h + .1)], .08, color='5A2A1A', alfa=.35, dentro=t)


def sombrero(l, x, y, s=1.0, material='acento', tono=None):
    """un sombrero de ala ancha, de sabanero: el ala que sube un poco a los lados, la copa con su hundido y la cinta; (x, y) es el
    centro del ala"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    g = [forma(P([(-6.6, -.6), (-5, .6), (0, 1.1), (5, .6), (6.6, -.6), (4.6, -.2), (0, .1), (-4.6, -.2)]), 2),
         forma(P([(-2.8, 0), (-2.7, -2.8), (-1.6, -3.6), (0, -3), (1.6, -3.6), (2.7, -2.8), (2.8, 0)]), 2)]
    m = l.masa(g, material=material, alto=.45, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.4)
    if tono:
        l.mancha(unary_union(g).buffer(1), tono[0], tono[1], dentro=m)
    l.mancha(Polygon(P([(-2.75, -.2), (2.75, -.2), (2.72, -1), (-2.72, -1)])), '3A2A0A', .75, dentro=m)     # la cinta
    return m


def cara(l, x, y, s=1.0, bigote=True):
    """los ojos de punto, el bigote con las puntas para arriba y la sonrisa de una cara de frente; (x, y) es el centro de la cabeza"""
    for dx in (-.85, .85):
        l.mancha(ovalo(x + dx * s, y - .4 * s, .26 * s, .3 * s), '05201C', 1)
    if bigote:
        l.trazo([(x - 1.4 * s, y + .75 * s), (x - .7 * s, y + 1.05 * s), (x, y + .95 * s), (x + .7 * s, y + 1.05 * s), (x + 1.4 * s, y + .75 * s)],
                [.1 * s, .32 * s, .3 * s, .32 * s, .1 * s], color='3A2A0A', alfa=.9)
    l.trazo([(x - .75 * s, y + 1.55 * s), (x, y + 1.9 * s), (x + .75 * s, y + 1.55 * s)], .16 * s, color='3A2A0A', alfa=.85)


# ------------------------------------------------------------------------------------------------ el nacimiento
def guanacaste(l, x, base, s=1.0, material='acento'):
    """un árbol de guanacaste: el tronco corto y grueso que se abre en ramas largas, casi horizontales, y la copa enorme, ancha y
    chata, como una sombrilla; mucho más ancho que alto"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry: ovalo(x + u * s, base + v * s, rx * s, ry * s)
    ramas = [tubo(P([(-.4, 0), (-.6, -5), (-4, -9.6), (-13, -12.6)]), [2.4 * s, 1.9 * s, 1.1 * s, .5 * s], 8),
             tubo(P([(.4, 0), (.8, -5.4), (5, -9.8), (14, -12.8)]), [2.4 * s, 1.8 * s, 1 * s, .5 * s], 8),
             tubo(P([(0, -6), (-.6, -10), (-1.4, -13.4)]), [1.2 * s, .8 * s, .5 * s], 6),
             forma(P([(-4.4, .3), (-2.4, -2.6), (2.4, -2.6), (4.4, .3)]), 1)]
    t = l.masa(ramas, material=material, alto=.4, brillo=.25, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.mancha(unary_union(ramas).buffer(1), '6B4E10', .3, dentro=t)
    copa = [O(0, -17.4, 21, 4.6), O(-11, -16.2, 11, 3.8), O(11.6, -16.4, 11, 3.8), O(-5, -20, 10, 3.4), O(6, -20.2, 10.6, 3.4),
            O(-20, -14.8, 5.4, 2.4), O(20.6, -15, 5.4, 2.4), O(0, -21.4, 7, 2.6)]
    c = l.masa(copa, material=material, alto=.45, brillo=.35, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    rng = np.random.default_rng(7)
    for _ in range(70):                                                  # el follaje menudo
        u, v = rng.uniform(-25, 25), rng.uniform(-23.4, -12.6)
        l.mancha(O(u, v, rng.uniform(.6, 1.3), rng.uniform(.35, .6)), str(rng.choice(['6B4E10', 'FBEFCB'])), .28, dentro=c)
    return c


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 22, 5, 12, .45)
    nube(l, 110, 3.4, 8, .45)
    # la cordillera de Guanacaste, al fondo, con el cono del volcán Orosí, y las lomas de su pie
    cordillera(l, [(-2, 16), (14, 13.6), (30, 15.4), (46, 12.4), (60, 14), (72, 11.6), (82, 10.6), (90, 6), (95, 2.6), (98, 2.6), (103, 6.4),
                   (110, 10.6), (122, 12.4)], material='lejos')
    cordillera(l, [(-2, 21), (16, 18.6), (34, 19.8), (52, 17.8), (70, 19.2), (86, 16.8), (100, 16.2), (112, 18.2), (122, 17.4)], material='cuerpo',
               linea=.3)
    # el llano seco, el río que nace al pie del volcán y lo cruza hacia nosotros, y el bosque seco de la orilla
    m = llano(l, [(-2, 21.4), (30, 20.6), (60, 21.2), (90, 20), (122, 20.8)])
    pasto_seco(l, 0, 120, 23, 40.6, 40, semilla=2, dentro=m)
    agua(l, cinta([(96, 18.6), (92, 22), (99, 27), (93, 33), (101, 41.8)], [.6, 1.4, 2.6, 4.4, 6.8], 10), ondas=4, semilla=3, linea=.3)
    for x, y, r in ((88, 24, 2), (104, 26, 2.2), (86, 32, 2.6), (110, 35, 2.8), (12, 27, 2.2), (24, 30, 2)):
        arbol(l, x, y, r, material='lejos', semilla=int(x))
    # el guanacaste dorado, protagonista, con su sombra en el llano
    l.mancha(ovalo(58, 32.6, 22, 1.8), '0C3A33', .25, difuso=.8)
    guanacaste(l, 58, 32.4)


# ------------------------------------------------------------------------------------------------ Liberia
def sabanero(l, x, base, s=1.0):
    """un sabanero de frente: las botas, el pantalón, la camisa blanca, el pañuelo al cuello, la soga enrollada en la mano y el
    sombrero de ala ancha, dorado"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([forma(P([(-3.4, 0), (-3.4, -2.6), (-1, -2.8), (-.6, 0)]), 1), forma(P([(.6, 0), (1, -2.8), (3.4, -2.6), (3.4, 0)]), 1)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)                         # las botas
    l.masa([tubo(P([(-1.6, -10.6), (-1.8, -6), (-2.1, -2.4)]), [1.4 * s, 1.2 * s, 1.1 * s], 5),
            tubo(P([(1.6, -10.6), (1.8, -6), (2.1, -2.4)]), [1.4 * s, 1.2 * s, 1.1 * s], 5)], material='lejos', alto=.3, brillo=.2, vientre=0,
           hondo=0, linea=.3)                                                                            # el pantalón
    camisa = [forma(P([(-3.8, -18.6), (3.8, -18.6), (4.2, -14), (3.4, -10.2), (-3.4, -10.2), (-4.2, -14)]), 1),
              tubo(P([(3.4, -17.8), (5, -14.4), (5.4, -11.4)]), [1.1 * s, 1 * s, .9 * s], 5),
              tubo(P([(-3.4, -17.8), (-5.8, -15.4), (-6.6, -13)]), [1.1 * s, 1 * s, .9 * s], 5)]
    c = l.masa(camisa, material='claro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.trazo(P([(0, -17.6), (0, -10.6)]), .1 * s, color='8EB5AA', alfa=.8, dentro=c)
    l.mancha(Polygon(P([(-3.4, -10.6), (3.4, -10.6), (3.4, -9.6), (-3.4, -9.6)])), '3A2A0A', .9)        # la faja
    piel(l, [O(5.5, -10.6, .9, .95), O(-6.8, -12.4, .9, .95), O(0, -21.4, 2.2, 2.6), box(x - .8 * s, base - 19.6 * s, x + .8 * s, base - 18.2 * s)],
         .62)
    l.masa(Polygon(P([(-2, -18.8), (2, -18.8), (0, -16.4)])), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)  # el pañuelo
    cara(l, x, base - 21.4 * s, s)
    for k in range(3):                                                   # la soga enrollada
        l.trazo([(x + (-6.8 + 1.6 * math.cos(t)) * s, base + (-10.4 + (1.6 + k * .3) * math.sin(t)) * s) for t in np.linspace(0, 2 * math.pi, 18)],
                .16 * s, color=SECO, alfa=.95)
    sombrero(l, x, base - 23.2 * s, s)


def cebu(l, x, base, s=1.0, lado=-1, con_sombrero=True):
    """una vaca cebú, blanca, de perfil: la joroba, la papada, las orejas caídas, los cuernos cortos y la cola; mira a `lado`"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + lado * u * s, base + v * s, rx * s, ry * s, a * lado)
    patas = [tubo(P([(u, -5), (u + .2, -2.4), (u, 0)]), [.75 * s, .55 * s, .5 * s], 4) for u in (-6, -4.4, 4, 5.6)]
    cuerpo = [forma(P([(-8, -5.6), (-8.4, -9), (-6, -10.4), (0, -10.6), (2.2, -11), (3.4, -13), (5.4, -12.6), (6.4, -10.6), (7.8, -9.4),
                       (8, -6.6), (6.4, -4.6), (-6.6, -4.4)]), 2),
              forma(P([(6.6, -10.4), (9.2, -11), (11.6, -10.4), (12.2, -7.4), (11.2, -6.6), (9.6, -7.6), (7.4, -6.4)]), 2),
              tubo(P([(-8.2, -8.6), (-9.4, -5.6), (-9.6, -2.4)]), [.3 * s, .25 * s, .2 * s], 6)]
    c = l.masa(patas + cuerpo, material='claro', alto=.45, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    l.mancha(O(8.2, -6.4, 1.6, 2.2), 'C9D8D2', .7, dentro=c)            # la papada
    l.mancha(O(-9.6, -2.2, .5, .9), '3A2A0A', .8)                       # la borla de la cola
    l.masa(O(9.6, -10.4, 1.6, .7, 35), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)          # la oreja caída
    l.mancha(O(10.6, -9.4, .32, .36), '05201C', 1)
    l.mancha(O(11.8, -7.4, .6, .5), '3A2A0A', .55)                      # el hocico
    if con_sombrero:
        sombrero(l, x + lado * 10 * s, base - 12.2 * s, .62 * s)


def liberia(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    nube(l, 98, 3.4, 10, .4)
    # la ciudad blanca: casas de adobe encaladas, de techo de teja, y la iglesia blanca con su torre
    prado(l, 25, 41, .32)
    for x, w, h in ((-2, 9, 6.4), (8, 8, 5.6), (17, 10, 6.6), (82, 9, 6), (92, 8.4, 5.4), (101.6, 10, 6.4), (112, 10, 5.8)):
        casa(l, x, 26, w, h)
    ig = l.masa([box(28, 13.6, 40, 26), box(29.6, 6, 35.4, 13.8)], material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(28.8, 6.2), (32.5, 2.6), (36.2, 6.2)]), material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(forma([(31.4, 12), (31.4, 9.2), (32.5, 8.2), (33.6, 9.2), (33.6, 12)], 1), '164F46', .85, dentro=ig)     # el campanario
    l.mancha(forma([(32.4, 26), (32.4, 20.4), (34, 18.8), (35.6, 20.4), (35.6, 26)], 1), '164F46', .85, dentro=ig)    # la puerta
    techo = Polygon([(39.6, 14.6), (40.4, 13.6), (58, 13.6), (59, 14.6)])
    t = l.masa(techo, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    l.mancha(techo.buffer(.5), TEJA, .75, dentro=t)
    nave = l.masa(box(40, 14.6, 58.6, 26), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    for x in (43, 48, 53):
        l.mancha(forma([(x, 22), (x, 18.6), (x + 1, 17.6), (x + 2, 18.6), (x + 2, 22)], 1), '164F46', .7, dentro=nave)
    for x in (61, 70):
        casa(l, x, 26, 8, 5.8)
    # la calle, y adelante el sabanero y la vaca cebú, con sus sombreros dorados, protagonistas
    calle = l.masa(box(-2, 26, 122, 41.6), material='claro', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
                   arroja=False)
    l.mancha(box(-2, 26, 122, 41.6), 'E8B952', .18, dentro=calle)
    l.mancha(ovalo(54, 38.6, 7, .9), '0C3A33', .25, difuso=.4)
    l.mancha(ovalo(77, 38.8, 10, .9), '0C3A33', .25, difuso=.4)
    cebu(l, 77, 38.6, 1.25, lado=-1)
    sabanero(l, 52, 38.6, 1.3)


# ------------------------------------------------------------------------------------------------ Guardia
def guardia(l, x, base, s=1.0):
    """un guardia de frente, firme: las botas, el uniforme dorado con su faja y sus bolsas, el machete al hombro, la otra mano en la
    faja, y el sombrero de ala ancha"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([forma(P([(-3.2, 0), (-3.2, -3.2), (-.8, -3.4), (-.5, 0)]), 1), forma(P([(.5, 0), (.8, -3.4), (3.2, -3.2), (3.2, 0)]), 1)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)                         # las botas
    uniforme = [tubo(P([(-1.6, -10.6), (-1.8, -6.4), (-1.9, -3)]), [1.4 * s, 1.2 * s, 1.1 * s], 5),
                tubo(P([(1.6, -10.6), (1.8, -6.4), (1.9, -3)]), [1.4 * s, 1.2 * s, 1.1 * s], 5),
                forma(P([(-3.8, -18.6), (3.8, -18.6), (4.2, -14), (3.4, -10), (-3.4, -10), (-4.2, -14)]), 1),
                tubo(P([(3.4, -17.8), (5.8, -15.6), (6, -17.6)]), [1.1 * s, 1 * s, .9 * s], 5),
                tubo(P([(-3.4, -17.8), (-5.2, -14.4), (-3.6, -11.4)]), [1.1 * s, 1 * s, .9 * s], 5)]
    u = l.masa(uniforme, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    for v0 in (-17, -13.4):                                              # las bolsas de la camisa
        for dx in (-2.2, 1.2):
            l.trazo(P([(dx, v0), (dx + 1.6, v0)]), .12 * s, color='6B4E10', alfa=.6, dentro=u)
    l.trazo(P([(0, -18.2), (0, -10.6)]), .1 * s, color='6B4E10', alfa=.5, dentro=u)
    l.mancha(Polygon(P([(-3.4, -10.6), (3.4, -10.6), (3.4, -9.4), (-3.4, -9.4)])), '3A2A0A', .9)        # la faja
    # el machete al hombro: el cabo en la mano y la hoja ancha de acero, con la punta sesgada
    l.masa(tubo(P([(5.8, -16.4), (6.4, -19.2)]), [.5 * s, .45 * s], 3), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    hoja = forma(P([(5.6, -19), (7.4, -19), (8.6, -23), (9.2, -26.6), (7.8, -27.2), (6.8, -23.4)]), 1)
    h = l.masa(hoja, material='claro', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.35)
    l.mancha(hoja.buffer(1), '8EB5AA', .45, dentro=h)
    l.trazo(P([(6.6, -19.8), (8, -25.4)]), [.05, .2, .05], color='FFFFFF', alfa=.8, dentro=h)
    piel(l, [O(6.1, -17.2, .9, .9), O(-3.6, -11, .9, .9), O(0, -21.4, 2.2, 2.6), box(x - .8 * s, base - 19.6 * s, x + .8 * s, base - 18.2 * s)],
         .62)
    cara(l, x, base - 21.4 * s, s)
    sombrero(l, x, base - 23.2 * s, s, material='vientre', tono=(PAJA, .6))


def guardia_puente(l):
    rng = np.random.default_rng(4)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 100, 3.4, 10, .4)
    # las lomas con potreros y unas vacas, atrás
    cordillera(l, [(-2, 17), (20, 14.6), (44, 16), (70, 13.6), (96, 15.4), (122, 14)], material='cuerpo', linea=.3)
    llano(l, [(-2, 18.4), (40, 17.8), (80, 18.8), (122, 18)], .3)
    for x, lado in ((14, 1), (24, -1), (98, 1), (108, -1)):
        cebu(l, x, 22.6, .32, lado=lado, con_sombrero=False)
    for x, r in ((34, 2.2), (86, 2.4), (6, 2), (116, 2.2)):
        arbol(l, x, 21.6, r, material='lejos', semilla=x)
    # el río de piedras y pozas, abajo
    agua(l, box(-2, 30, 122, 41.6), ondas=8, semilla=5, linea=0)
    for _ in range(22):
        x, y = rng.uniform(0, 120), rng.uniform(31.6, 40.4)
        l.masa(ovalo(x, y, rng.uniform(1, 2.6), rng.uniform(.6, 1.1)), material='vientre', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.25,
               arroja=False)
    for x0, x1 in ((-2, 14), (104, 122)):
        orilla(l, forma([(x0, 41.6), (x0, 28), (x1, 28.6), (x1 + (8 if x0 < 0 else -8), 41.6)], 1), tinte=.36)
    # el puente, con sus pilas y su baranda, y el guardia dorado, protagonista, que lo cuida
    for x in (30, 90):
        l.masa(box(x - 2, 28, x + 2, 35), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.masa(box(-2, 27, 122, 29.4), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.trazo([(-2, 24.4), (122, 24.4)], .3, color='8EB5AA', alfa=.95)
    for x in np.arange(0, 122, 4):
        l.trazo([(x, 24.4), (x, 27.2)], .25, color='8EB5AA', alfa=.95)
    l.mancha(ovalo(61, 27.6, 6, .6), '0C3A33', .3, difuso=.3)
    guardia(l, 60, 27.4, .95)


# ------------------------------------------------------------------------------------------------ Filadelfia
def queso(l, x, y, s=1.0):
    """un queso crema gigante, de barra: la crema blanca, el papel dorado que la envuelve abajo, abierto y arrugado, el cuchillo de
    untar clavado arriba, la cara y el sombrero de paja; (x, y) es la esquina de abajo a la izquierda del frente, en la línea del
    agua"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    frente = Polygon(P([(0, 0), (0, -12), (26, -12), (26, 0)]))
    lado = Polygon(P([(26, 0), (26, -12), (31, -15.4), (31, -3.4)]))
    tapa = Polygon(P([(0, -12), (5, -15.4), (31, -15.4), (26, -12)]))
    for g, br in ((lado, .12), (frente, .35), (tapa, .3)):
        l.masa(g, material='claro', alto=.3, brillo=br, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.trazo(P([(8, -13.4), (13, -14.4), (19, -13.4), (24, -14.2)]), [.05, .25, .25, .05], color='C9D8D2', alfa=.9)   # la crema untada
    # el papel dorado, abierto: envuelve la mitad de abajo, con el borde de arriba arrugado y una punta doblada hacia afuera
    papel = [Polygon(P([(0, 0), (0, -6.6), (3, -5.8), (6.6, -6.9), (10, -6), (13.4, -7.1), (17, -6.1), (20.4, -7), (23.4, -6), (26, -6.8), (26, 0)])),
             Polygon(P([(26, 0), (26, -6.8), (27.6, -8.4), (29.4, -8.6), (31, -10), (31, -3.4)]))]
    m = l.masa(papel, material='acento', alto=.35, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    for k in range(6):                                                   # las arrugas del papel
        u = 2 + k * 4.4
        l.trazo(P([(u, -6.2), (u + .8, -3.4), (u - .3, -.6)]), [.05, .16, .05], color='6B4E10', alfa=.45, dentro=m)
    # el cuchillo de untar, clavado en la crema
    l.masa(forma(P([(22.6, -13.4), (23.6, -13.8), (26.6, -20.6), (25.6, -21.2)]), 1), material='claro', alto=.3, brillo=.4, vientre=0, hondo=0,
           linea=.3)
    l.masa(tubo(P([(26.2, -20.8), (27.8, -24.6)]), [.6 * s, .55 * s], 3), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    for dx in (9.6, 16.4):                                               # la cara
        l.mancha(ovalo(x + dx * s, y - 10.4 * s, .55 * s, .7 * s), '05201C', 1)
    l.trazo(P([(10.8, -8.8), (13, -8.1), (15.2, -8.8)]), .3 * s, color='3A2A0A', alfa=.9)
    sombrero(l, x + 13.4 * s, y - 15.6 * s, 1.15 * s, material='vientre', tono=(PAJA, .6))


def filadelfia(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .45)
    nube(l, 96, 3.4, 10, .4)
    # el pueblo, lejos, y los arrozales, verdes y anegados, hasta el río crecido
    prado(l, 15, 41, .2)
    for x, w, h in ((40, 6, 3.6), (47, 5, 3), (53, 6.6, 4), (61, 5, 3.2), (67, 6, 3.6)):
        casa(l, x, 16, w, h)
    for y0 in (17, 19.4, 22.4):
        for x in np.arange(-2, 122, 11):
            l.trazo([(x, y0 + .2), (x + 9, y0)], .14, color='A4DCC4', alfa=.6)
    for _ in range(140):                                                 # las matas de arroz, en hileras
        x, y = rng.uniform(0, 120), rng.uniform(16.4, 25)
        l.trazo([(x - .3, y), (x, y - .9 - (y - 16) * .06), (x + .3, y)], .12, color='2F8A74', alfa=.8)
    agua(l, forma([(-2, 41.6), (-2, 25.6), (30, 25), (60, 25.6), (90, 24.8), (122, 25.4), (122, 41.6)], 1), ondas=12, semilla=7, linea=.3)
    # el queso crema dorado, protagonista, que flota río abajo con su sombrero de paja
    l.mancha(ovalo(62, 35.4, 20, 1.6), '0C3A33', .25, difuso=.6)
    queso(l, 45, 35.4, 1.05)
    for k in range(3):                                                   # las ondas que deja
        l.trazo([(40 - k * 3, 36.6 + k * .9), (46 + k * 4, 37.2 + k * .9), (80 + k * 3, 36.6 + k * .9)], .2, color='D2F2DA', alfa=.7)


# ------------------------------------------------------------------------------------------------ Bolsón
def bolson(l, x, base, s=1.0):
    """un bolsón dorado de gangoche, abierto arriba con el borde enrollado y lleno de mazorcas que asoman, con su cara y las dos
    piernas que dan el paso del muelle al bongo"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([tubo(P([(-3, -4), (-5.6, -1.4), (-7.2, 0)]), [.7 * s, .6 * s, .5 * s], 5), tubo(P([(3, -4), (5.4, -2.4), (7.4, 1.6)]), [.7 * s, .6 * s, .5 * s], 5),
            O(-7.8, .2, 1.4, .6), O(8, 1.8, 1.4, .6)], material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    for u, v, a in ((-5.6, -21.4, -28), (-2.6, -23, -12), (.6, -23.6, 2), (3.8, -22.8, 16), (6.6, -21, 30)):   # las mazorcas, con sus tusas
        l.masa([Polygon(P([(u - .8, v + 3.4), (u - 2.8, v - .6), (u - .2, v + 1.6)])), Polygon(P([(u + .8, v + 3.4), (u + 2.6, v - .2), (u + .2, v + 1.6)]))],
               material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.2)
        m = l.masa(O(u, v, 1.3, 3, a), material='acento', alto=.5, brillo=.55, vientre=0, hondo=0, linea=.3)
        for k in range(4):                                               # los granos, en hileras
            for j in range(5):
                l.mancha(O(u + (k - 1.5) * .6 + math.sin(math.radians(a)) * (j - 2) * 1.1, v + (j - 2) * 1.1, .26, .4, a), '6B4E10', .3, dentro=m)
    bolsa = forma(P([(-7.6, -2.6), (-9, -7), (-9.2, -12), (-8.6, -17.4), (8.6, -17.4), (9.2, -12), (9, -7), (7.6, -2.6), (4, -1.8), (-4, -1.8)]), 2)
    b = l.masa(bolsa, material='acento', alto=.5, brillo=.4, vientre=0, hondo=.1, linea=.45, contraluz=.35)
    l.mancha(bolsa.buffer(1), 'BF9129', .35, dentro=b)
    for k in range(9):                                                   # la trama del gangoche
        l.trazo(P([(-8 + k * 2, -16.6), (-7.8 + k * 1.95, -2.6)]), .1 * s, color='6B4E10', alfa=.3, dentro=b)
    for k in range(7):
        l.trazo(P([(-9.2, -15.4 + k * 1.9), (9.2, -15.4 + k * 1.9)]), .1 * s, color='6B4E10', alfa=.25, dentro=b)
    borde = forma(P([(-9.4, -15.6), (9.4, -15.6), (9.6, -18.8), (-9.6, -18.8)]), 1)
    r = l.masa(borde, material='acento', alto=.45, brillo=.4, vientre=0, hondo=0, linea=.4)
    l.mancha(borde.buffer(1), 'BF9129', .35, dentro=r)
    l.trazo(P([(-9.4, -17.2), (9.4, -17.2)]), .14 * s, color='6B4E10', alfa=.5, dentro=r)
    for dx in (-2.8, 2.8):
        l.mancha(O(dx, -10.6, .6, .75), '05201C', 1)
    l.trazo(P([(-2, -7.6), (0, -6.6), (2, -7.6)]), .35 * s, color='3A2A0A', alfa=.9)


def bongo_madera(l, x, y, s=1.0):
    """el bongo amarrado, de madera, sin carga: la canoa grande de un solo tronco, con las puntas que suben"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    c = l.masa(forma(P([(-18, -2.6), (-14, -.6), (14, -.6), (18, -2.8), (16, 1.4), (10, 2.4), (-10, 2.4), (-16, 1.4)]), 2), material='vientre', alto=.4,
               brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(forma(P([(-20, -3), (20, -3), (20, 3), (-20, 3)]), 0), '5A3E1E', .6, dentro=c)
    l.trazo(P([(-16, -1.4), (0, -.2), (16, -1.6)]), [.05, .3, .05], color='3A2A0A', alfa=.5, dentro=c)
    return c


def bolson_puerto(l):
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .45)
    nube(l, 98, 3.4, 10, .4)
    # la otra orilla, con los campos y unas casas, y el río que da la vuelta en su meandro
    m = llano(l, [(-2, 15), (40, 14.6), (80, 15.2), (122, 14.6)], .3)
    for x, w, h in ((80, 6, 3.6), (87, 5.6, 3.2), (94, 6.4, 3.8)):
        casa(l, x, 16.4, w, h)
    for x, r in ((10, 2.4), (20, 2), (64, 2.2), (108, 2.6)):
        arbol(l, x, 15.4, r, material='lejos', semilla=x)
    agua(l, forma([(-2, 41.6), (-2, 19), (30, 18), (70, 18.6), (104, 17.4), (122, 18), (122, 41.6)], 2), ondas=10, semilla=8, linea=.3)
    orilla(l, forma([(84, 41.6), (96, 30), (110, 26), (122, 25.6), (122, 41.6)], 2), tinte=.32)
    # el muelle de tablas, a la izquierda, y el bongo amarrado a su lado
    l.mancha(ovalo(80, 33.4, 18, 1.4), '0C3A33', .22, difuso=.6)
    bongo_madera(l, 80, 32, 1.1)
    for x in (4, 13, 22, 31, 40, 48):
        l.masa(box(x - .6, 30, x + .6, 38.6), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    d = l.masa(box(-2, 29.4, 50, 31.6), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(box(-2, 29.4, 50, 31.6), '5A3E1E', .55, dentro=d)
    for x in np.arange(0, 50, 2.6):
        l.trazo([(x, 29.4), (x, 31.6)], .1, color='3A2A0A', alfa=.5, dentro=d)
    # el bolsón dorado lleno de maíz, protagonista, que pasa del muelle al bongo
    bolson(l, 56, 29.6, 1.0)


# ------------------------------------------------------------------------------------------------ Puerto Humo
def olla(l, x, base, s=1.0):
    """una olla dorada sobre su fogón de tres piedras y leña, con el arroz que hierve y se rebalsa"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([tubo(P([(-7, 0), (6, -1.4)]), [.6 * s, .6 * s], 2), tubo(P([(-6, -1.2), (7, .2)]), [.6 * s, .6 * s], 2)], material='vientre', alto=.3, brillo=.1,
           vientre=0, hondo=0, linea=.25)
    for k in range(3):                                                   # las llamas
        l.mancha(forma(P([(-3 + k * 3, -.6), (-2.4 + k * 3, -3), (-1.4 + k * 3, -4.6), (-1 + k * 3, -2.6), (-.4 + k * 3, -.6)]), 1), 'F2D48A', .85)
    for u in (-5.6, 5.6):                                                # las piedras del fogón
        l.masa(O(u, -1.4, 1.6, 1.3), material='lejos', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.25)
    g = unary_union([forma(P([(-5.4, -2.6), (-6.2, -6), (-5.8, -9.4), (5.8, -9.4), (6.2, -6), (5.4, -2.6)]), 2), O(0, -9.4, 6.4, 1.2),
                     O(-6.6, -8.4, 1.2, .5), O(6.6, -8.4, 1.2, .5)])
    m = l.masa(g, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    l.trazo(P([(-4.4, -4), (-4.6, -7.6)]), [.06, .4, .06], color='FBEFCB', alfa=.9, dentro=m)
    l.masa(forma(P([(-5.6, -9.6), (-4, -11.2), (-1.6, -10.4), (0, -11.6), (2.4, -10.6), (4.4, -11.4), (5.8, -9.6), (5, -8.6), (6, -7), (4.8, -6.4),
                    (4.2, -8.6), (0, -9), (-4.4, -8.6)]), 2), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)   # el arroz rebalsado
    return g


def espatula(l, x, base, s=1.0, lado=1):
    """una espátula rosada en el agua, de perfil: las patas largas, el cuerpo, el cuello y el pico ancho en cuchara"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    g = [tubo(P([(0, 0), (.2, -3.4)]), [.12 * s, .12 * s], 2), tubo(P([(.8, 0), (.6, -3.4)]), [.12 * s, .12 * s], 2), ovalo(x + lado * .2 * s, base - 4.6 * s, 2 * s, 1.2 * s),
         tubo(P([(1.4, -5), (2.2, -7), (2.6, -8.2)]), [.4 * s, .3 * s, .3 * s], 5), forma(P([(2.6, -8.6), (5.2, -8), (5.8, -7.4), (5.2, -7.2), (2.8, -7.8)]), 1)]
    m = l.masa(g, material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.mancha(unary_union(g).buffer(1), 'E8A0B0', .6, dentro=m)


def garza(l, x, base, s=1.0, lado=1):
    """una garza blanca, de pie, con el cuello en S y el pico de lanza"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    l.masa([tubo(P([(0, 0), (.2, -3.6)]), [.12 * s, .12 * s], 2), tubo(P([(.8, 0), (.6, -3.6)]), [.12 * s, .12 * s], 2),
            ovalo(x + lado * .2 * s, base - 5 * s, 2 * s, 1.3 * s), tubo(P([(1.6, -5.4), (1, -7.4), (2, -9.2)]), [.35 * s, .3 * s, .3 * s], 6),
            Polygon(P([(2, -9.6), (4.6, -9), (2, -8.8)]))], material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.25)


def cocodrilo(l, x, base, s=1.0, lado=1):
    """un cocodrilo echado en el barro, de perfil, mirando a `lado`: el hocico largo, el ojo alto, las patas cortas, el lomo de
    escamas y la cola larga"""
    P = lambda pts: [(x + lado * u * s, base + v * s) for u, v in pts]
    g = [forma(P([(-8, -1.2), (-6, -4.2), (0, -5), (6, -4.6), (9, -4.6), (12, -5.4), (16.6, -4.6), (17.6, -3.6), (15, -3), (11.6, -2.6), (8, -1),
                  (-6, -.6)]), 2),
         tubo(P([(-7.6, -2.2), (-13, -1.6), (-18, -.8), (-21, -.2)]), [2.4 * s, 1.6 * s, .9 * s, .2 * s], 8),
         tubo(P([(4.6, -1.6), (5.6, 0)]), [1.1 * s, .9 * s], 4), tubo(P([(-4, -1.6), (-5, 0)]), [1.1 * s, .9 * s], 4)]
    c = l.masa(g, material='lejos', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for u in np.arange(-16, 8, 1.8):
        v = -4.6 if u > -6 else -2.8 + (u + 6) * .12
        l.trazo(P([(u, v), (u + .9, v - .6), (u + 1.8, v)]), .12 * s, color='05201C', alfa=.5, dentro=c)
    l.masa(ovalo(x + lado * 10.6 * s, base - 5.8 * s, 1.1 * s, .9 * s), material='lejos', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.mancha(ovalo(x + lado * 10.8 * s, base - 5.9 * s, .4 * s, .35 * s), 'F2D48A', .9)
    return c


def puerto_humo(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    # enfrente, el humedal de Palo Verde: el juncal, las garzas y las espátulas, los patos que vuelan y un cocodrilo en el barro
    prado(l, 16, 21, .26)
    juncos(l, 40, 122, 20.4, 4, 90, semilla=10, espadanas=False)
    for x, y, s, f in ((84, 21.4, .8, garza), (92, 21, .7, espatula), (100, 21.6, .8, espatula), (110, 21.2, .75, garza), (118, 21.4, .7, espatula)):
        f(l, x, y, s, lado=-1 if x > 100 else 1)
    for x, y, s in ((60, 6, .7), (66, 4.4, .55), (72, 6.6, .6), (90, 8, .6), (96, 6.4, .5)):
        ave(l, x, y, s)
    agua(l, box(-2, 21, 122, 41.6), ondas=10, semilla=11, linea=0)
    l.masa(ovalo(102, 27.6, 14, 1.6), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.25)
    l.mancha(ovalo(102, 27.6, 14, 1.6), '8A6A3A', .5)
    cocodrilo(l, 104, 27.4, .62, lado=-1)
    # la orilla de acá, con el muelle a la izquierda, y las ollas doradas que hierven en sus fogones, protagonistas
    orilla(l, forma([(-2, 41.6), (-2, 30), (30, 30.6), (70, 31), (86, 32.6), (92, 41.6)], 2), tinte=.34)
    for x in (2, 9, 16, 23):
        l.masa(box(x - .6, 24, x + .6, 33), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    d = l.masa(box(-2, 23, 28, 25), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(box(-2, 23, 28, 25), '5A3E1E', .55, dentro=d)
    l.masa(forma([(2, 23), (2, 17), (8, 14.6), (14, 17), (14, 23)], 0), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x, b, s in ((45, 36.4, 1.35), (67, 37.2, 1.5)):
        olla(l, x, b, s)
    # el humo de los fogones, que sube y se va sobre el muelle hasta taparlo
    for k in range(14):
        t = k / 13
        cx = 60 - t * 54 + rng.uniform(-2, 2)
        cy = 19 - math.sin(t * math.pi) * 7 + rng.uniform(-1, 1)
        l.mancha(ovalo(cx, cy, 5 + t * 5, 3.4 + t * 2.6), 'FFFFFF', .62 + .2 * (1 - abs(t - .6)), difuso=1.2)
    for x, y in ((45, 20.6), (67, 19.4)):
        for k in range(3):
            l.mancha(ovalo(x + k * 1.4 - 1, y - k * 3, 2.6 + k, 2 + k * .6), 'FFFFFF', .7, difuso=.6)


# ------------------------------------------------------------------------------------------------ el mar
def bongo(l, x, y, s=1.0):
    """el bongo, la barca del juego, mirando a la derecha: la canoa grande de un solo tronco, de casco dorado, con su palo corto, la
    vela cuadrada entre la botavara y el pico, la carga de cueros y sacos de maíz, y el remero de popa; (x, y) es la línea del agua
    bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.trazo(P([(-16, -5.4), (-20, 1.4)]), .35 * s, color='5A3E1E', alfa=.95)                # el remo de popa
    l.masa(tubo(P([(2, -1.6), (2.4, -22)]), [.4 * s, .3 * s], 3), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)   # el palo
    vela = Polygon(P([(3, -21.2), (15, -18), (13.6, -3.6), (3, -3.6)]))
    v = l.masa(vela, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for k in range(1, 4):
        l.trazo(P([(3, -21.2 + k * 4.4), (15 - k * .35, -18 + k * 3.6)]), .1 * s, color='8EB5AA', alfa=.7, dentro=v)
    l.trazo(P([(2.6, -3.6), (14.4, -3.6)]), .3 * s, color='5A3E1E', alfa=.95)               # la botavara
    l.trazo(P([(2.6, -21.4), (15.4, -18)]), .3 * s, color='5A3E1E', alfa=.95)               # el pico
    for u, w, h, mat in ((-11, 5, 3.4, 'lejos'), (-6, 4.4, 3, 'vientre'), (-1.6, 4.6, 3.6, 'vientre')):   # los cueros y los sacos
        f = l.masa(forma(P([(u - w / 2, -2.4), (u - w / 2, -2.4 - h), (u + w / 2, -2.4 - h), (u + w / 2, -2.4)]), 1), material=mat, alto=.4, brillo=.2,
                   vientre=0, hondo=0, linea=.25)
        if mat == 'vientre':
            l.mancha(forma(P([(u - w, 0), (u + w, 0), (u + w, -7), (u - w, -7)]), 0), 'BF9129', .4, dentro=f)
    piel(l, [ovalo(x - 15.4 * s, y - 8.4 * s, .9 * s, 1 * s)])
    l.masa(forma(P([(-16.6, -2.6), (-16.6, -7.2), (-14.2, -7.2), (-14.2, -2.6)]), 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    casco = forma(P([(-19.6, -4.8), (-15, -2.4), (15, -2.4), (20, -5), (17.6, .6), (10, 2.2), (-10, 2.2), (-17.6, .6)]), 2)
    c = l.masa(casco, material='acento', alto=.5, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-17.6, -3), (0, -1.8), (17.6, -3.2)]), [.05, .4, .05], color='93701A', alfa=.5, dentro=c)
    for k in range(2):                                                   # las vetas del tronco
        l.trazo(P([(-14 + k * 3, -.2 + k * 1.1), (0, .4 + k * 1.1), (14 - k * 3, -.4 + k * 1.1)]), [.05, .14, .05], color='93701A', alfa=.45, dentro=c)
    return casco.union(vela)


def mar(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .5)
    nube(l, 96, 4, 12, .45)
    horizonte = 18
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(30, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # enfrente, la lengua de arena de Puntarenas, larga y angosta, con sus casas y sus palmeras
    lengua = forma([(70, horizonte + .4), (78, horizonte - 1), (122, horizonte - 1.4), (122, horizonte + .4)], 1)
    orilla(l, lengua, tinte=.4, linea=.25)
    for x in np.arange(82, 122, 3.6):
        l.masa(box(x, horizonte - 2.6, x + 2.4, horizonte - .8), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.18, arroja=False)
    for x in (80, 94, 108):
        palmera(l, x, horizonte - .8, 2.6, 1, datiles=False)
    # atrás a la izquierda, lejos, el puente largo cerca de la boca
    l.masa(box(-2, horizonte - 2.4, 30, horizonte - 1.6), material='claro', alto=.1, brillo=.1, vientre=0, hondo=0, linea=.18)
    for x in np.arange(0, 30, 3):
        l.trazo([(x, horizonte - 1.6), (x, horizonte)], .3, color='8EB5AA', alfa=.9)
    # los manglares de la boca, a la izquierda, y el ojo de Lalo, el cocodrilo, que se queda en la orilla
    orilla(l, forma([(-2, 41.6), (-2, 24), (12, 25), (22, 30), (24, 41.6)], 2), tinte=.3)
    for x, y, h in ((4, 27, 11), (14, 31, 12), (6, 38.6, 13)):
        mangle(l, x, y, h, semilla=x)
    l.masa([ovalo(30, 36.6, 3, .7), ovalo(28.4, 35.8, .7, .6), ovalo(31.2, 35.8, .7, .6)], material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.25)
    for dx in (-1.6, 1.2):
        l.mancha(ovalo(29.8 + dx, 35.6, .3, .25), 'F2D48A', .9)
    # el bongo, la barca del juego, protagonista, que entra al golfo
    g = bongo(l, 64, 33, 1.3)
    reflejo(l, g, 33.4, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Liberia', dibujar=liberia), dict(clave='Guardia', dibujar=guardia_puente),
            dict(clave='Filadelfia', dibujar=filadelfia), dict(clave='Bolsón', dibujar=bolson_puerto), dict(clave='Puerto Humo', dibujar=puerto_humo),
            dict(clave='mar', dibujar=mar)]
LISTO = True
