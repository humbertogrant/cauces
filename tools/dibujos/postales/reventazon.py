# -*- coding: utf-8 -*-
"""Las postales del Reventazón, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: la cordillera de Talamanca, con las nubes pegadas, y el valle de cafetales donde los ríos dorados que bajan de la
  montaña, de un lado y del otro, se juntan en uno solo;
- Orosi: «una iglesia chiquita de techo de tejas y un oso que reza adentro»: la iglesia blanca de techo de teja, con su campanario, y
  por la puerta abierta el oso dorado, de rodillas, con las manos juntas;
- Cachí: «un cachete inflado aguanta el agua de todo el valle»: una cara dorada, con los cachetes inflados y los ojos apretados, que
  tapa el cañón entre los cerros y aguanta el embalse; abajo sale el río;
- Juan Viñas: «don Juan Viñas se toma un café con azúcar de su propio ingenio, sentado en la estación del tren»: don Juan, de saco
  dorado, en la banca de la estación, con su taza que humea; atrás, la chimenea del ingenio, los cañales y los cafetales, y el tren;
- Turrialba: «una bola de béisbol con un volcán de sombrero baja el río en balsa»: la bola dorada, con sus costuras, el volcancito
  que humea de sombrero y el remo, en la balsa, entre los rápidos; al fondo, el volcán Turrialba;
- Siquirres: «un sí que chirría como los frenos del tren»: las letras SÍ, doradas, en un carro de tren que frena sobre el cruce de
  las vías, con las chispas; atrás, los bananales y la represa;
- Parismina: «una tortuga con paraguas y boina desova en la playa»: la tortuga dorada, con su boina y su paraguas, y los huevos en
  el hoyo, en la arena de la barra;
- el mar: la balsa de rafting, la barca del juego, de tubos dorados, que sale a la barra de Parismina con sus remeros, frente a las
  olas del Caribe que revientan; en la orilla, Nuria, la nutria, que se queda.
"""
import math

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, prado,  # noqa: F401
                     reflejo, rio, selva, tierra)
from pintor import forma, ovalo, tubo

PIEL = 'A2683A'            # el tono de la piel: un café tibio sobre el pálido de `vientre`
PAJA = 'D2B070'            # la paja de los sombreros
TEJA = 'B0603A'            # el barro cocido de las tejas
MADERA = '5A3E1E'


def piel(l, piezas, tono=.6):
    """piezas de piel: el pálido de `vientre` teñido de café"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def cara(l, x, y, s=1.0, bigote=True):
    """los ojos de punto, el bigote con las puntas para arriba y la sonrisa de una cara de frente; (x, y) es el centro de la cabeza"""
    for dx in (-.85, .85):
        l.mancha(ovalo(x + dx * s, y - .4 * s, .26 * s, .3 * s), '05201C', 1)
    if bigote:
        l.trazo([(x - 1.4 * s, y + .75 * s), (x - .7 * s, y + 1.05 * s), (x, y + .95 * s), (x + .7 * s, y + 1.05 * s), (x + 1.4 * s, y + .75 * s)],
                [.1 * s, .32 * s, .3 * s, .32 * s, .1 * s], color='3A2A0A', alfa=.9)
    l.trazo([(x - .75 * s, y + 1.55 * s), (x, y + 1.9 * s), (x + .75 * s, y + 1.55 * s)], .16 * s, color='3A2A0A', alfa=.85)


def madera(l, piezas, tono=.55, linea=.3):
    """piezas de madera: el pálido de `vientre` teñido de café"""
    m = l.masa(piezas, material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=linea)
    l.mancha(unary_union(piezas).buffer(1), MADERA, tono, dentro=m)
    return m


def cafetal(l, pts, filas, semilla=0, dentro=None):
    """las hileras de un cafetal sobre una ladera: matas oscuras en fila, a lo largo de cada curva de `filas` (corrimientos en y)"""
    rng = np.random.default_rng(semilla)
    pts = sorted(pts)
    xs = [p[0] for p in pts]
    for dy in filas:
        for x in np.arange(min(xs), max(xs), 1.6):
            y = np.interp(x, xs, [p[1] for p in pts]) + dy
            l.mancha(ovalo(x + rng.uniform(-.3, .3), y, .8, .55), '164F46', .55, dentro=dentro)


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    # la cordillera de Talamanca, alta y oscura, con las nubes pegadas a las cumbres
    cordillera(l, [(-2, 9), (10, 6), (24, 8), (40, 4.6), (56, 7), (72, 5), (90, 7.6), (106, 4.4), (122, 7)], material='lejos')
    for x, y, w in ((16, 6.4, 18), (60, 5.6, 20), (104, 6, 16)):
        nube(l, x, y, w, .7)
    # el fondo del valle, y los cerros de cafetales de adelante
    prado(l, 13, 41.6, .28)
    for borde, pie in (([(-2, 26), (10, 24.4), (24, 26.6), (34, 31), (40, 36), (43, 41.6)], [(-2, 41.6)]),
                       ([(90, 41.6), (95, 34), (104, 30.6), (114, 29), (122, 29.6)], [(122, 41.6)])):
        g = Polygon(borde + pie).buffer(0)
        m = l.masa(g, material='cuerpo', alto=.25, brillo=.06, vientre=0, hondo=0, linea=.35, escalon=.2, contraluz=.25)
        cafetal(l, borde, (2.6, 5.4, 8.4, 11.6, 15), semilla=int(borde[0][0]) + 2, dentro=m)
    # los ríos que bajan de Talamanca y del valle de Cartago, con sus cascadas, y se juntan
    for a in ([(1, 15.4), (12, 17.4), (22, 17), (32, 20.4), (41, 22.4)], [(36, 13.6), (37, 16.4), (40, 18.6), (42.2, 21.8)],
              [(72, 13.8), (64, 16.4), (56, 17.2), (48, 20), (43.4, 22.2)]):
        agua(l, cinta(a, np.linspace(.6, 1.8, len(a)), 10), linea=.3)
        x, y = a[0]
        l.mancha(ovalo(x, y + .4, 1.8, 1.1), 'FFFFFF', .85, difuso=.3)   # la cascada donde sale de la montaña
    # el Reventazón dorado, protagonista, que nace donde se juntan y baja hacia nosotros, con sus ondas
    cauce = cinta([(42.2, 22), (54, 24.4), (68, 25.4), (78, 28), (76, 32.6), (66, 36), (64, 41.8)], [2.2, 3, 4, 5, 6.6, 8, 10], 10).buffer(.4).buffer(-.4)
    m = l.masa(cauce, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.4, escalon=.1, contraluz=.3)
    for x, y in ((50, 24), (60, 25.2), (70, 26), (78, 28.6), (77, 32.6), (68, 35.4), (62, 38.4), (68, 40.4), (58, 36.6)):
        l.trazo([(x - 1.4, y), (x, y - .3), (x + 1.4, y)], .16, color='FBEFCB', alfa=.9, dentro=m)
    for x, y in ((8, 21), (26, 23), (60, 20.6), (90, 22), (50, 32), (86, 36)):
        arbol(l, x, y, 2.4, material='lejos', semilla=int(x))


# ------------------------------------------------------------------------------------------------ Orosi
def oso_reza(l, x, base, s=1.0):
    """un oso dorado, de rodillas y de perfil, mirando a la derecha, con las manos juntas delante del hocico y la cabeza un poco
    gacha, que reza con los ojos cerrados"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = [forma(P([(-4.6, -1.6), (-6, -5.6), (-5.4, -10.4), (-3, -13.8), (1, -14.2), (3.2, -11.4), (3.6, -6), (2, -2)]), 2),
              O(-2.4, -1.8, 5.2, 2.1), O(-7.2, -1.2, 1.4, 1.2),
              O(2.4, -16.8, 3.1, 2.8), O(5.2, -15.4, 1.8, 1.2, 30), O(1, -19.4, 1.1, 1.1),
              tubo(P([(1, -11.6), (5, -10.4), (7.4, -10.4)]), [1.1 * s, 1 * s, .9 * s], 5),
              forma(P([(6.6, -9.4), (8.6, -9.6), (9.6, -11.8), (9.4, -14.6), (8.6, -15), (7.4, -12.6)]), 1)]
    m = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    l.mancha(O(6.4, -14.6, .45, .4), '3A2A0A', 1)                     # la nariz
    l.trazo(P([(2.4, -17.6), (3.2, -17.1), (4, -17.4)]), .2 * s, color='3A2A0A', alfa=.9)    # el ojo cerrado
    l.mancha(O(1, -19.4, .5, .5), '6B4E10', .5, dentro=m)
    l.trazo(P([(7.8, -10), (9, -14.4)]), .14 * s, color='6B4E10', alfa=.65, dentro=m)        # las manos juntas


def orosi(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.6, 12, .45)
    # las montañas del valle y los cafetales
    cordillera(l, [(-2, 12), (16, 7.6), (34, 10.4), (52, 8.4), (70, 10), (90, 6.6), (108, 9.4), (122, 8)], material='lejos')
    ladera = [(-2, 20), (20, 17.6), (44, 19.6), (70, 17.4), (96, 19.2), (122, 17)]
    m = l.masa(Polygon([(-2, 41.6)] + ladera + [(122, 41.6)]), material='cuerpo', alto=.25, brillo=.06, vientre=0, hondo=0, linea=.35)
    cafetal(l, ladera, (2, 4.6, 7.4), semilla=3, dentro=m)
    prado(l, 30, 41.6, .3)
    # la iglesia chiquita: la fachada blanca de frontón, el techo de teja, el campanario a un lado y la puerta abierta
    techo = Polygon([(33, 13.6), (60, 4.6), (87, 13.6), (85, 14.6), (60, 6.4), (35, 14.6)])
    fachada = Polygon([(35, 34), (35, 14), (60, 6), (85, 14), (85, 34)])
    f = l.masa(fachada, material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, contraluz=.25)
    t = l.masa(techo, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(techo.buffer(.5), TEJA, .8, dentro=t)
    torre = l.masa(box(18, 9, 32, 34), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, contraluz=.25)
    tt = Polygon([(16.6, 9.4), (25, 3.4), (33.4, 9.4)])
    t2 = l.masa(tt, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(tt.buffer(.5), TEJA, .8, dentro=t2)
    l.mancha(forma([(21.6, 18), (21.6, 13.6), (25, 11), (28.4, 13.6), (28.4, 18)], 2), '164F46', .9, dentro=torre)     # el hueco de la campana
    l.masa(forma([(23.2, 16.4), (23.6, 13.6), (25, 12.8), (26.4, 13.6), (26.8, 16.4)], 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0,
           linea=.25)
    for x in (38.6, 77.4):
        l.mancha(forma([(x, 22), (x, 18), (x + 1.8, 16.4), (x + 3.6, 18), (x + 3.6, 22)], 1), '164F46', .75, dentro=f)
    puerta = forma([(46, 34), (46, 20), (49, 15), (55, 12.6), (60, 12.2), (65, 12.6), (71, 15), (74, 20), (74, 34)], 2)
    l.mancha(puerta, '0C3A33', .95)
    l.mancha(ovalo(60, 22, 9, 9), 'F2D48A', .12, difuso=2, dentro=puerta)            # la luz de las velas, adentro
    for x in (49, 71):                                                   # las velas
        l.masa(box(x - .5, 26, x + .5, 30), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.15)
        l.mancha(ovalo(x, 25.2, .5, .8), 'FBEFCB', .95)
    madera(l, [box(44.6, 20, 46, 34), box(74, 20, 75.4, 34)], .6)       # las hojas abiertas de la puerta
    # el oso dorado, protagonista, que reza de rodillas
    oso_reza(l, 58, 33.6, 1.12)
    l.masa(box(30, 33.6, 90, 35), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)


# ------------------------------------------------------------------------------------------------ Cachí
def cachi(l):
    cielo(l, sol=None)
    nube(l, 24, 3.6, 12, .45)
    nube(l, 100, 3.4, 10, .45)
    cordillera(l, [(-2, 10), (20, 7), (44, 9), (70, 6), (96, 8.4), (122, 6.6)], material='lejos')
    # el embalse, atrás de la cara, que llena el valle
    agua(l, box(-2, 11.6, 122, 24), ondas=8, semilla=2, linea=0)
    # los cerros del cañón, a los dos lados
    for pts in ([(-2, 41.6), (-2, 13), (14, 14), (28, 17), (38, 23), (43, 31), (44, 41.6)], [(122, 41.6), (122, 13), (106, 14), (92, 17), (82, 23), (77, 31),
                                                                                           (76, 41.6)]):
        m = l.masa(Polygon(pts), material='cuerpo', alto=.3, brillo=.06, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.3)
        cafetal(l, pts[1:5] if pts[0][0] < 0 else pts[1:5], (3, 6.4, 10), semilla=int(pts[1][1]), dentro=m)
    # el río que sale por abajo, con su espuma
    agua(l, cinta([(60, 33), (58.6, 36.6), (61, 41.8)], [16, 20, 26], 6), ondas=6, semilla=3, linea=.3)
    for k in range(6):
        l.mancha(ovalo(54 + k * 2.4, 34.4 + (k % 2) * .8, 2.2, .8), 'FFFFFF', .7, difuso=.3)
    # la cara dorada, protagonista: los cachetes inflados que aguantan el agua de todo el valle
    piezas = [ovalo(60, 21, 15, 12.4), ovalo(48.4, 24.6, 8.6, 8.2), ovalo(71.6, 24.6, 8.6, 8.2), ovalo(60, 30, 9, 4)]
    c = l.masa(piezas, material='acento', alto=.6, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for dx in (-1, 1):
        l.mancha(ovalo(60 + dx * 12.6, 26, 3.6, 2.6), 'E8A090', .45, dentro=c)       # el rubor de los cachetes
        l.trazo([(60 + dx * 3, 16.6), (60 + dx * 5, 17.6), (60 + dx * 7.6, 16.8)], .5, color='3A2A0A', alfa=.9)        # los ojos apretados
        l.trazo([(60 + dx * 3, 13.6), (60 + dx * 5.4, 12.6), (60 + dx * 8, 13.4)], .4, color='6B4E10', alfa=.8)         # las cejas
    l.masa(ovalo(60, 27.6, 2, 1.6), material='oscuro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)          # la boca apretada
    l.mancha(ovalo(60, 21.6, 1.3, 1), '6B4E10', .35, dentro=c)          # la nariz
    for x, y in ((45, 12.4), (76, 12.6), (39, 16), (82, 16.4)):           # el agua que empuja
        l.trazo([(x - 1, y + 1), (x, y - .6), (x + 1, y + 1)], .24, color='FFFFFF', alfa=.85)
    l.mancha(ovalo(76.4, 15.4, .7, 1.1), 'D2F2DA', .9)                   # una gota de esfuerzo


# ------------------------------------------------------------------------------------------------ Juan Viñas
def don_juan(l, x, base, s=1.0):
    """don Juan Viñas, sentado de frente en la banca de la estación: los zapatos, el pantalón, el saco dorado con la camisa blanca y
    la corbata, el sombrero, el bigote, la taza de café que se lleva a la boca y el platito en la otra mano"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([O(-2.6, -.4, 1.5, .6), O(2.6, -.4, 1.5, .6)], material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.25)
    l.masa([tubo(P([(-2.4, -7.6), (-2.6, -4), (-2.6, -.8)]), [1.2 * s, 1.1 * s, 1 * s], 5), tubo(P([(2.4, -7.6), (2.6, -4), (2.6, -.8)]), [1.2 * s, 1.1 * s, 1 * s], 5),
            O(-2.4, -7.8, 1.8, 1.4), O(2.4, -7.8, 1.8, 1.4)], material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    saco = [forma(P([(-4.4, -17.4), (4.4, -17.4), (4.8, -12), (4.4, -7.6), (-4.4, -7.6), (-4.8, -12)]), 1),
            tubo(P([(4, -16.6), (6, -13), (3.8, -11.4)]), [1.2 * s, 1.1 * s, 1 * s], 5),
            tubo(P([(-4, -16.6), (-6.2, -13.4), (-5.4, -11)]), [1.2 * s, 1.1 * s, 1 * s], 5)]
    m = l.masa(saco, material='acento', alto=.45, brillo=.45, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.35)
    camisa = Polygon(P([(-1.6, -17.4), (1.6, -17.4), (0, -12.4)]))
    l.masa(camisa, material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.masa(Polygon(P([(-.5, -16.8), (.5, -16.8), (.7, -14), (0, -13), (-.7, -14)])), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.2)                                                     # la corbata
    for dx in (-1, 1):                                                   # las solapas
        l.trazo(P([(dx * 1.6, -17.2), (dx * 2.4, -14.6), (0, -11.6)]), .14 * s, color='6B4E10', alfa=.6, dentro=m)
    for v in (-10.4, -9):
        l.mancha(O(0, v, .3, .3), '6B4E10', .8, dentro=m)
    piel(l, [O(3.4, -11.6, .9, .9), O(-5.2, -10.8, .9, .9), O(0, -19.6, 2.2, 2.5), box(x - .7 * s, base - 18 * s, x + .7 * s, base - 16.8 * s)])
    cara(l, x, base - 19.6 * s, s)
    # la taza que humea, en la mano, y el platito
    l.masa(forma(P([(2.2, -13.2), (2.4, -11), (4.6, -11), (4.8, -13.2)]), 1), material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.25)
    l.mancha(Polygon(P([(2.3, -13.2), (4.7, -13.2), (4.6, -12.6), (2.4, -12.6)])), '5A3E1E', .9)
    for k in range(3):
        l.trazo(P([(3 + k * .7, -13.8), (3.4 + k * .7, -15), (2.8 + k * .7, -16.2), (3.2 + k * .7, -17.4)]), .14 * s, color='FFFFFF', alfa=.85)
    l.masa(O(-5.2, -11.6, 2, .45), material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.2)
    # el sombrero
    l.masa([O(0, -21.4, 4.6, .9), forma(P([(-2.4, -21.4), (-2.2, -23.6), (0, -24.2), (2.2, -23.6), (2.4, -21.4)]), 1)], material='lejos', alto=.35,
           brillo=.3, vientre=0, hondo=0, linea=.3)


def locomotora(l, x, y, s=1.0):
    """una locomotora de vapor chica, de perfil, mirando a la izquierda: la caldera, la chimenea con su humo, la cabina y las ruedas"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry: ovalo(x + u * s, y + v * s, rx * s, ry * s)
    l.masa([box(x - 8 * s, y - 6.4 * s, x + 4 * s, y - 2 * s), box(x + 4 * s, y - 10 * s, x + 10 * s, y - 2 * s), box(x - 6.6 * s, y - 9.6 * s, x - 4.6 * s, y - 6.2 * s),
            Polygon(P([(3.4, -10), (10.6, -10), (10.6, -11), (3.4, -11)]))], material='lejos', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    l.mancha(box(x + 5.4 * s, y - 9 * s, x + 8.6 * s, y - 6.4 * s), CIELO, .9)
    for u in (-5.6, -1.6, 2.4, 7):
        l.masa(O(u, -1.2, 1.4, 1.4), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    for k in range(4):
        l.mancha(O(-5.6 + k * 2.4, -11.6 - k * 1.6, 1.4 + k * .5, 1 + k * .3), 'FFFFFF', .8 - k * .15, difuso=.4)


def juan_vinas(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 30, 3.6, 12, .45)
    # las lomas: los cañales a la izquierda, con la chimenea del ingenio, y los cafetales a la derecha
    cordillera(l, [(-2, 12), (20, 9.4), (44, 11.6), (70, 9), (96, 11), (122, 9.6)], material='lejos')
    loma = [(-2, 17), (24, 15), (50, 16.4), (76, 14.6), (100, 16), (122, 14.8)]
    m = l.masa(Polygon([(-2, 41.6)] + loma + [(122, 41.6)]), material='cuerpo', alto=.25, brillo=.06, vientre=0, hondo=0, linea=.35)
    cafetal(l, loma[2:], (2, 4.4, 6.8), semilla=6, dentro=m)
    for _ in range(90):                                                  # la caña
        x, y = rng.uniform(0, 40), rng.uniform(16, 24)
        l.trazo([(x, y), (x + rng.uniform(-.6, .6), y - 2.4)], .14, color='9BDDBD', alfa=.8, dentro=m)
    ch = l.masa([Polygon([(9.4, 18), (10, 3.4), (12.4, 3.4), (13, 18)]), box(9.4, 2.6, 13, 3.6)], material='claro', alto=.25, brillo=.1, vientre=0,
                hondo=0, linea=.3)                                       # la chimenea del ingenio
    l.mancha(box(9, 2, 14, 18), TEJA, .55, dentro=ch)
    for y in np.arange(5, 18, 1.6):
        l.trazo([(9.6, y), (12.8, y)], .08, color='5A2A1A', alfa=.4, dentro=ch)
    for k in range(5):
        l.mancha(ovalo(13.6 + k * 3.2, 1.8 + k * .3, 1.6 + k * .7, 1.1 + k * .3), 'FFFFFF', .85 - k * .12, difuso=.4)
    # la estación: la pared de tablas, la ventana, el alero sobre sus postes; las vías, y el tren que llega
    prado(l, 25, 41.6, .26)
    pared = box(26, 12, 84, 29)
    madera(l, [pared], .45)
    for x in np.arange(27, 84, 2.2):
        l.trazo([(x, 12.4), (x, 29)], .1, color='3A2A0A', alfa=.35)
    for x in (32, 70):
        l.mancha(box(x, 16, x + 7, 22), '164F46', .85)
        l.trazo([(x + 3.5, 16), (x + 3.5, 22)], .2, color='E2EDE9', alfa=.9)
    alero = Polygon([(22, 12.6), (88, 12.6), (85, 8), (25, 8)])
    a = l.masa(alero, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(alero.buffer(.5), TEJA, .75, dentro=a)
    for x in (27, 83):
        madera(l, [box(x - .5, 12.6, x + .5, 30)], .6)
    l.masa(box(22, 29, 88, 31), material='claro', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.3)          # el andén
    for y in (35.2, 37.6):
        l.trazo([(-2, y), (122, y)], .35, color='6E7E7B', alfa=.95)
    for x in np.arange(0, 122, 3):
        l.trazo([(x, 34.6), (x - .6, 38.4)], .5, color=MADERA, alfa=.6)
    locomotora(l, 106, 35, 1.25)
    # la banca, y don Juan, de saco dorado, protagonista, con su café
    madera(l, [box(42, 22.4, 66, 23.6), box(42, 26.2, 66, 27.4), box(43.4, 27, 44.6, 30.4), box(63.4, 27, 64.6, 30.4)], .65)
    don_juan(l, 54, 30.4, 1.1)


# ------------------------------------------------------------------------------------------------ Turrialba
def bola(l, x, y, r):
    """una bola de béisbol dorada: la esfera con las dos costuras curvas, de puntadas, la cara contenta y el volcancito que humea de
    sombrero"""
    m = l.masa(ovalo(x, y, r, r), material='acento', alto=.6, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for lado in (-1, 1):                                                 # las costuras
        c = [(x + lado * r * (.62 - .3 * math.cos(t)), y + r * .9 * math.sin(t)) for t in np.linspace(-1.25, 1.25, 12)]
        l.trazo(c, .12, color='8A3A22', alfa=.7, dentro=m)
        for k in range(1, len(c) - 1):
            px, py = c[k]
            l.trazo([(px - .6, py - .3), (px, py), (px + .6, py - .3)], .14, color='A0402A', alfa=.9, dentro=m)
    for dx in (-.25, .25):
        l.mancha(ovalo(x + dx * r, y - .1 * r, .1 * r, .13 * r), '05201C', 1)
    l.trazo([(x - .28 * r, y + .25 * r), (x, y + .42 * r), (x + .28 * r, y + .25 * r)], .1 * r, color='3A2A0A', alfa=.85)
    # el volcancito de sombrero, con su cráter y su humo
    v = Polygon([(x - 1.02 * r, y - .66 * r), (x - .62 * r, y - .98 * r), (x - .26 * r, y - 1.42 * r), (x - .12 * r, y - 1.36 * r), (x, y - 1.42 * r),
                 (x + .14 * r, y - 1.35 * r), (x + .28 * r, y - 1.42 * r), (x + .64 * r, y - .98 * r), (x + 1.02 * r, y - .66 * r)])
    vm = l.masa(v, material='lejos', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(v.buffer(1), MADERA, .5, dentro=vm)
    for u in (-.5, -.1, .35):                                            # las quebradas de la falda
        l.trazo([(x + u * r * .5, y - 1.3 * r), (x + u * r, y - .8 * r)], .12, color='3A2A0A', alfa=.45, dentro=vm)
    for k in range(4):
        l.mancha(ovalo(x + k * .26 * r, y - (1.62 + k * .3) * r, (.22 + k * .12) * r, (.14 + k * .06) * r), 'C9D8D2', .9 - k * .12, difuso=.3)
    return m


def balsa(l, x, y, s=1.0, material='claro', tinte='8EB5AA'):
    """una balsa de rafting de perfil: el tubo gordo que se levanta en las puntas, con la cuerda de seguridad en sus argollas; (x, y) es
    la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    tubo_ = forma(P([(-15, -5.6), (-12, -2.4), (12, -2.4), (15, -5.6), (17, -4.6), (15.4, .2), (11, 1.4), (-11, 1.4), (-15.4, .2), (-17, -4.6)]), 3)
    t = l.masa(tubo_, material=material, alto=.6, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.35)
    if tinte:
        l.mancha(tubo_.buffer(1), tinte, .45, dentro=t)
    cuerda = [(x + u * s, y + (-1 + .5 * abs(math.sin(u * .52))) * s) for u in np.linspace(-13, 13, 26)]
    l.trazo(cuerda, .16 * s, color='3A2A0A', alfa=.7, dentro=t)
    return tubo_


def turrialba(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    # el volcán Turrialba, ancho, con su cráter que echa ceniza, y los cerros verdes
    cordillera(l, [(-2, 16), (20, 12), (40, 8), (50, 6.4), (58, 6.4), (70, 9.4), (90, 13), (122, 14)], material='lejos')
    for k in range(5):
        l.mancha(ovalo(56 + k * 3.4, 4.6 - k * 1, 2.2 + k * 1, 1.4 + k * .4), 'C9D8D2', .75 - k * .1, difuso=.6)
    cordillera(l, [(-2, 21), (24, 17.6), (50, 19.6), (80, 17), (122, 19.4)], material='cuerpo', linea=.3)
    # el río, con los rápidos y las piedras
    agua(l, box(-2, 22, 122, 41.6), ondas=10, semilla=8, linea=0)
    for _ in range(30):
        x, y = rng.uniform(0, 120), rng.uniform(23, 40)
        l.trazo([(x, y), (x + 2, y - .5), (x + 4, y)], .5, color='FFFFFF', alfa=.7)
    for x, y, rx in ((14, 30, 4), (100, 27, 3.6), (110, 36, 5), (8, 38, 4)):
        l.masa(ovalo(x, y, rx, rx * .45), material='vientre', alto=.5, brillo=.2, vientre=0, hondo=0, linea=.3)
        l.mancha(ovalo(x - rx * .9, y + .4, rx * .5, .6), 'FFFFFF', .8, difuso=.3)
    # la balsa, y la bola dorada con su volcán de sombrero, protagonista, que rema
    l.trazo([(74, 13), (66, 34)], .45, color='3A2A0A', alfa=.95)        # el remo
    l.masa(forma([(64.6, 33.4), (67.6, 34.6), (66.4, 38.4), (63.6, 37.4)], 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    bola(l, 58, 21, 9.4)
    l.masa([ovalo(68, 21, 1.2, 1.2), tubo([(65.6, 23), (68, 21)], [.6, .6], 2)], material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3)
    g = balsa(l, 58, 32.4, 1.25)
    for k in range(4):
        l.mancha(ovalo(36 - k * 3, 33.6 + k * .4, 3, .9), 'FFFFFF', .7, difuso=.3)


# ------------------------------------------------------------------------------------------------ Siquirres
def letras_si(x, base, s=1.0):
    """las letras SÍ, gruesas: la S como un tubo en curva, la I como una barra y la tilde inclinada; (x, base) es abajo a la izquierda"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    ese = tubo(P([(9, -13.4), (7, -15.6), (3.4, -15.6), (1.2, -13.2), (2, -10.2), (5, -8.4), (8, -6.6), (9, -3.6), (7.2, -.8), (3.6, -.4), (.8, -2.4)]),
               [1.7 * s] * 11, 6)
    i = Polygon(P([(12.8, 0), (12.8, -15.4), (16.2, -15.4), (16.2, 0)]))
    tilde = Polygon(P([(13.8, -16.6), (16.6, -20.4), (19, -19.4), (15.6, -16)]))
    return [ese, i, tilde]


def siquirres(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # los cerros y la represa, con su embalse, y los bananales
    cordillera(l, [(-2, 14), (24, 9.6), (44, 11.6), (60, 8.6), (80, 11), (100, 8.4), (122, 12.6)], material='lejos')
    agua(l, forma([(70, 13.6), (76, 11.2), (98, 11), (104, 13.6)], 1), linea=.25)
    presa = forma([(70, 13.2), (87, 14.2), (104, 13.2), (100, 22.4), (87, 23), (74, 22.4)], 1)
    pm = l.masa(presa, material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(presa.buffer(1), '8EB5AA', .45, dentro=pm)
    for x in np.arange(84.4, 90, 1.2):                                   # el vertedero
        l.trazo([(x, 14.2), (x + .1, 18), (x - .2, 22.6)], .5, color='FFFFFF', alfa=.85)
    l.mancha(ovalo(87, 23, 4.6, 1.2), 'FFFFFF', .8, difuso=.4)
    prado(l, 20, 41.6, .26)
    for x, h in ((4, 13), (16, 11), (30, 12.4), (108, 12), (118, 13.6), (90, 10)):
        banano(l, x, 31, h, semilla=x)
    # las vías que se cruzan: la de acá, de costado, y la otra, que se va hacia el fondo
    for dx in (-5, 5):
        l.trazo([(60 + dx * 2.2, 41.8), (60 + dx * .3, 22)], .3, color='6E7E7B', alfa=.9)
    for t in np.linspace(0, 1, 8) ** 1.6:
        y = 22 + t * 19.8
        w = 1.4 + t * 9.6
        l.trazo([(60 - w, y), (60 + w, y)], .4 + t * .3, color=MADERA, alfa=.55)
    for x in np.arange(0, 122, 3):
        l.trazo([(x, 32.6), (x - .6, 36)], .5, color=MADERA, alfa=.65)
    for y in (33, 35.4):
        l.trazo([(-2, y), (122, y)], .4, color='6E7E7B', alfa=.95)
    # el carro, con las letras SÍ doradas, protagonistas, que chirría al frenar: las chispas y el chillido
    l.masa(box(38, 28.6, 82, 31), material='lejos', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)
    for u in (44, 54, 66, 76):
        l.masa(ovalo(u, 32.2, 1.8, 1.8), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
        for k in range(5):                                               # las chispas
            a = math.radians(190 + k * 14)
            l.trazo([(u - 1.4, 33.6), (u - 1.4 + math.cos(a) * (3 + k % 2 * 1.6), 33.6 + math.sin(a) * (3 + k % 2 * 1.6))], .2, color='FBEFCB', alfa=.95)
    m = l.masa(letras_si(44.6, 28.6, 1.36), material='acento', alto=.55, brillo=.5, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    for x, y in ((36, 22), (34, 26), (88, 21), (90, 25)):                # el chillido
        l.trazo([(x, y), (x + 1, y - 1.2), (x + 2, y), (x + 3, y - 1.2), (x + 4, y)], .3, color='0C3A33', alfa=.7)


def banano(l, x, base, h, semilla=0):
    """una mata de banano: el falso tallo y las hojas largas y anchas, rotas, que se abren y caen"""
    rng = np.random.default_rng(semilla)
    l.masa(tubo([(x, base), (x + .3, base - h * .55)], [.9, .7], 3), material='cuerpo', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.25)
    hojas, nervios = [], []
    for a in (-162, -128, -92, -56, -20):
        r = math.radians(a + rng.uniform(-8, 8))
        p0 = np.array([x + .3, base - h * .55])
        d = np.array([math.cos(r), math.sin(r)])
        p1 = p0 + d * h * .3 + np.array([0, -h * .1])
        p2 = p0 + d * h * .56 + np.array([0, h * .14])
        hojas.append(tubo([p0, p1, p2], [.25, h * .12, .2], 8))
        nervios.append([p0, p1, p2])
    m = l.masa(hojas, material='cuerpo', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.25, contraluz=.25)
    for n in nervios:
        l.trazo(n, .12, color='164F46', alfa=.6, dentro=m)


# ------------------------------------------------------------------------------------------------ Parismina
def tortuga(l, x, base, s=1.0):
    """una tortuga verde dorada en la arena, de perfil, mirando a la derecha: el caparazón con sus placas, la cabeza con la boina, la
    aleta de adelante en la arena y la otra levantada, que sostiene el paraguas abierto"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    # el paraguas, atrás: el mango, la tela en cúpula con su borde de ondas y las varillas
    l.trazo(P([(9.4, -9), (10, -24)]), .3 * s, color='3A2A0A', alfa=.95)
    tela = forma(P([(-2, -22.4), (1, -27.6), (10, -30.4), (19, -27.6), (22, -22.4), (19.4, -23.4), (16, -22.2), (12.6, -23.4), (10, -22.2), (7.4, -23.4),
                    (4, -22.2), (.6, -23.4)]), 2)
    t = l.masa(tela, material='lejos', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for u in (4, 10, 16):
        l.trazo(P([(10, -30.2), (u, -22.6)]), .1 * s, color='0C3A33', alfa=.6, dentro=t)
    for u0, u1 in ((1, 6), (13, 18)):                                    # los gajos claros
        l.mancha(Polygon(P([(10, -30.4), (u0, -22), (u1, -22)])), 'E6F3EE', .55, dentro=t)
    piezas = [forma(P([(-10, -1.4), (-9, -5.6), (-4, -9.6), (2, -10.4), (7, -8.4), (9.6, -4.4), (9.4, -1.4)]), 2),
              O(12.4, -5.6, 2.6, 2.2, -10), tubo(P([(8.6, -4.4), (11, -5)]), [1.4 * s, 1.3 * s], 3),
              forma(P([(5, -2), (9, -1.6), (13, .2), (8, .6), (4, -.4)]), 1),
              tubo(P([(5.6, -6), (8.4, -8.4), (9.6, -10)]), [1 * s, .8 * s, .7 * s], 5),
              forma(P([(-8, -1.4), (-12, .2), (-9.6, .6), (-6.4, -.6)]), 1)]
    m = l.masa(piezas, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    for pts in (((-6, -6.6), (-2, -8.6), (2, -6.4), (-2, -4.4)), ((2, -6.4), (6.4, -6.6), (7.6, -3.6), (3.2, -2.6)), ((-2, -4.4), (3.2, -2.6), (-1, -1.8),
                                                                                                                      (-6.6, -2.6))):
        l.trazo(P(list(pts) + [pts[0]]), .16 * s, color='6B4E10', alfa=.55, dentro=m)               # las placas
    l.mancha(O(13.4, -6.2, .4, .45), '05201C', 1)
    l.trazo(P([(13.6, -4.6), (14.6, -4.4)]), .14 * s, color='3A2A0A', alfa=.8)
    l.masa([O(11.8, -7.8, 3, .9, -12), O(12.8, -8.8, .4, .5)], material='oscuro', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.25)   # la boina


def parismina(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    nube(l, 24, 4, 12, .45)
    nube(l, 98, 3.4, 12, .45)
    # el mar, atrás, con las olas, y la barra donde el río entra
    m = l.masa(box(-2, 15, 122, 26), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 15, 122, 17), '64C8AA', .5, dentro=m, difuso=.6)
    for y in (19, 22.4):
        for x in np.arange(-2, 122, 9):
            l.trazo([(x, y + .4), (x + 3, y - .4), (x + 6, y + .4)], .35, color='FFFFFF', alfa=.7)
    playa = forma([(-2, 41.6), (-2, 23), (40, 24.4), (80, 24), (104, 25), (122, 26.6), (122, 41.6)], 2)
    orilla(l, playa, tinte=.5, linea=.3)
    agua(l, cinta([(122, 30), (112, 28.4), (104, 26.4)], [3.4, 3, 2.4], 6), linea=.3)
    for x, y, h in ((8, 30, 13), (18, 27, 11), (104, 34, 12)):
        palmera(l, x, y, h, 1, datiles=False)
    # el hoyo con los huevos, y la tortuga dorada, protagonista, con su boina y su paraguas
    l.mancha(ovalo(48, 35, 7, 2), '8A6A3A', .55)
    for k in range(9):
        l.masa(ovalo(44.6 + (k % 5) * 1.6, 34.4 + (k // 5) * 1.3, .8, .7), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.2)
    for k in range(6):                                                   # el rastro en la arena
        l.trazo([(100 - k * 2.6, 39.6 - k * .3), (101.4 - k * 2.6, 38.6 - k * .3)], .3, color='8A6A3A', alfa=.5)
    tortuga(l, 64, 37.6, 1.15)


# ------------------------------------------------------------------------------------------------ el mar
def remero(l, x, y, s=1.0, remo=1):
    """un remero de rafting, sentado en el tubo: el chaleco, el casco y el remo de mango en T"""
    l.masa(forma([(x - 1.4 * s, y), (x - 1.6 * s, y - 3.4 * s), (x + 1.6 * s, y - 3.4 * s), (x + 1.4 * s, y)], 1), material='claro', alto=.3, brillo=.2, vientre=0,
           hondo=0, linea=.25)
    piel(l, [ovalo(x, y - 4.6 * s, 1 * s, 1.1 * s)])
    l.masa(forma([(x - 1.2 * s, y - 4.8 * s), (x - 1 * s, y - 5.8 * s), (x, y - 6.2 * s), (x + 1 * s, y - 5.8 * s), (x + 1.2 * s, y - 4.8 * s)], 1), material='lejos',
           alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)                # el casco
    l.trazo([(x + 2.4 * s * remo, y - 6 * s), (x - 1.6 * s * remo, y + 4 * s)], .26 * s, color='3A2A0A', alfa=.95)
    l.masa(forma([(x - 1.6 * s * remo - .6, y + 3.4 * s), (x - 1.2 * s * remo + .6, y + 3.6 * s), (x - 2 * s * remo + .6, y + 6.4 * s),
                  (x - 2.4 * s * remo - .6, y + 6.2 * s)], 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.2)


def nutria(l, x, base, s=1.0):
    """una nutria de río, sentada en la orilla, de frente: el cuerpo largo y café, la cabeza chata con sus bigotes"""
    O = lambda u, v, rx, ry: ovalo(x + u * s, base + v * s, rx * s, ry * s)
    g = [O(0, -3, 2, 3.2), O(0, -7, 1.6, 1.4), O(-1.4, -8.2, .5, .5), O(1.4, -8.2, .5, .5), tubo([(x + 1.6 * s, base - .4 * s), (x + 4 * s, base)], [.7 * s, .4 * s], 3)]
    m = l.masa(g, material='vientre', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(g).buffer(1), MADERA, .65, dentro=m)
    l.mancha(O(0, -6.4, 1, .7), 'C9D8D2', .6, dentro=m)
    for dx in (-.6, .6):
        l.mancha(O(dx, -7.4, .2, .22), '05201C', 1)


def mar(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .5)
    nube(l, 96, 4, 12, .45)
    # el Caribe, atrás, y las olas que revientan en la barra
    m = l.masa(box(-2, 14, 122, 41.6), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 14, 122, 16), '64C8AA', .5, dentro=m, difuso=.6)
    for y, a in ((17.4, .7), (20, .8)):
        for x in np.arange(-2, 122, 8):
            l.trazo([(x, y + .4), (x + 3, y - .4), (x + 6, y + .4)], .35, color='FFFFFF', alfa=a)
    ola = [(x, 23.4 - 1.2 * math.sin(x / 5.4)) for x in np.arange(-2, 122.1, 1)]
    l.mancha(Polygon(ola + [(122, 27.4), (-2, 27.4)]), 'FFFFFF', .85, difuso=.5)          # la espuma de la ola que revienta
    for x in np.arange(0, 122, 4.6):
        l.mancha(ovalo(x + rng.uniform(-1, 1), 22.4 + rng.uniform(-1, .6), 2.4, 1.6), 'FFFFFF', .8, difuso=.4)
    l.mancha(box(-2, 27.4, 122, 41.6), '64C8AA', .25, dentro=m)          # el agua del río, más clara, en la barra
    # las puntas de arena de la barra, con sus palmeras, y Nuria, la nutria, que se queda en la orilla
    for pts in ([(-2, 41.6), (-2, 25), (14, 26.4), (24, 31), (26, 41.6)], [(122, 41.6), (122, 25.6), (108, 27), (98, 32), (96, 41.6)]):
        orilla(l, forma(pts, 2), tinte=.5)
    for x, y, h, lado in ((6, 32, 14, 1), (16, 36, 12, 1), (114, 34, 14, -1)):
        palmera(l, x, y, h, lado, datiles=False)
    nutria(l, 104, 37.6, .9)
    # la balsa de rafting, la barca del juego, de tubos dorados, con sus remeros, protagonista
    for x, k in ((48, 1), (56, -1), (64, 1), (72, -1)):
        remero(l, x, 30.6, 1, k)
    g = balsa(l, 60, 33.6, 1.45, material='acento', tinte=None)
    reflejo(l, g, 34, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Orosi', dibujar=orosi), dict(clave='Cachí', dibujar=cachi),
            dict(clave='Juan Viñas', dibujar=juan_vinas), dict(clave='Turrialba', dibujar=turrialba), dict(clave='Siquirres', dibujar=siquirres),
            dict(clave='Parismina', dibujar=parismina), dict(clave='mar', dibujar=mar)]
LISTO = True
