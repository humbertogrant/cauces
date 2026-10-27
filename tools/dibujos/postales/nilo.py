# -*- coding: utf-8 -*-
"""Las postales del Nilo, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar. La imagen para recordar es la protagonista: grande, al
medio, y lo único dorado de la postal; no hay sol, salvo el que se pone en Luxor, que es parte de la imagen.

- el nacimiento: los dos ríos que nacen y bajan hacia nosotros, grandes: el Nilo Blanco, claro, que sale del lago Victoria, a la
  izquierda, y el Nilo Azul, oscuro, que sale del lago Tana, al pie de las tierras altas de Etiopía, y cae por su catarata; en cada
  lago, parada en el agua, su inicial dorada, la V de Victoria y la T de Tana;
- Jinja: «un jinete salta a caballo desde el lago Victoria»: el caballo dorado en el aire, sobre el agua donde nace el Nilo Blanco,
  con la corona de agua que dejó al saltar; río abajo, la represa de Owen Falls, que tapó las cataratas Ripon;
- Juba: «un país recién nacido con chupón»: un bebé grande, con su chupón y su banderita de estrella, en una canasta que flota en el
  río, frente al muelle de Juba y sus casas de techos de lata; río abajo, el Sudd, el pantano de papiros;
- Jartum: «dos jarras, una de agua blanca y otra azul, se vacían en el mismo cauce»: el Nilo Blanco y el Nilo Azul se juntan y corren
  un trecho lado a lado, cada uno de su color; enfrente, Omdurmán, con la cúpula del Mahdi;
- Asuán: «una aduana en el río»: una barrera a rayas que cruza el río de orilla a orilla, con su caseta, y una falúa que espera; al
  fondo, la Presa Alta, la aduana del agua, que la deja salir por sus compuertas, y las rocas de granito de la primera catarata;
- Luxor: «lujo de faraones»: en la orilla de los muertos, donde se pone el sol, los cerros del Valle de los Reyes y una máscara de oro
  de faraón; en la de los vivos, las columnas de Karnak, un obelisco y un pilono;
- El Cairo: «el río cae en un abanico»: visto desde arriba y desde el mar, el Nilo baja del horizonte y en la punta, donde está la
  ciudad, se abre en el delta, un triángulo dorado como la letra Δ, hasta el mar; junto a la ciudad, las pirámides de Guiza;
- el mar: la falúa no sale al mar (en el delta la carga sigue en gabarra hasta Alejandría): el faro de Alejandría, dorado, en su isla,
  con la gabarra cargada que va hacia él, y la falúa, de madera, que da la vuelta en el último brazo del delta, entre palmeras.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, agua, ave, cielo, cinta, cordillera, nube, obelisco, orilla, palmera, papiro, pasto,  # noqa: F401
                     piramide, prado, reflejo, rio, selva, tierra)
from pintor import forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`


def nilo_blanco(l, g, ondas=0, semilla=0):
    """el agua del Nilo Blanco: clara, casi blanca"""
    return agua(l, g, material='vientre', brillo='C6EEDC', ondas=ondas, semilla=semilla, linea=.3)


def nilo_azul(l, g, ondas=0, semilla=0):
    """el agua del Nilo Azul: honda y oscura"""
    return agua(l, g, material='lejos', brillo='246E61', ondas=ondas, semilla=semilla, linea=.3)


def faluca(l, x, y, s=1.0, lado=1, casco='lejos'):
    """una falúa del Nilo: el casco bajo, el palo corto y la gran vela latina, triangular, colgada de su entena larga e inclinada; mira a
    la derecha (con `lado` -1, a la izquierda); (x, y) es la línea del agua bajo el medio del casco. El casco es de madera; dorado solo
    cuando la falúa es la protagonista"""
    P = lambda pts: [(x + u * s * lado, y + v * s) for u, v in pts]
    vela = Polygon(P([(-5.8, -1.6), (6.4, -13.8), (3.2, -1.4)]))
    v = l.masa(vela.buffer(.15 * s), material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.4, escalon=.15, contraluz=.25)
    for k in range(3):
        l.trazo(P([(-3.6 + k * 2.2, -2.2 - k * 1.6), (3.6 + k * .4, -2)]), [.05, .12, .05], color='8EB5AA', alfa=.6, dentro=v)
    l.masa([tubo(P([(-6.6, -1), (7.2, -14.6)]), [.22 * s, .16 * s], 6), tubo(P([(1.6, -.8), (1.8, -7.4)]), [.3 * s, .24 * s], 6)],
           material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    casco_ = forma(P([(-7, -1.2), (-6, .7), (5, .9), (7.6, -1.8), (5.6, -.8), (-5.6, -.5)]), 1)
    c = l.masa(casco_, material=casco, alto=.35, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.25)
    l.trazo(P([(-6.4, -.3), (0, .1), (6.8, -.9)]), [.06, .14, .06], alfa=.4, dentro=c)
    return casco_.union(vela)


# ------------------------------------------------------------------------------------------------ el nacimiento
def inicial(l, pts, x, base, s=1.0):
    """una letra grande y dorada, parada en el agua de su lago, con sus ondas al pie; `pts`, su contorno, con la base en 0"""
    g = Polygon([(x + u * s, base + v * s) for u, v in pts]).buffer(.15 * s)
    l.masa(g, material='acento', alto=.45, brillo=.45, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.35)
    x0, _, x1, _ = g.bounds
    for k, w in enumerate((1, 1.5)):
        cx, rx = (x0 + x1) / 2, (x1 - x0) / 2 * w * .6
        t = np.linspace(.15, math.pi - .15, 12)
        l.trazo([(cx + rx * math.cos(a), base + .3 + k * .5 + .5 * math.sin(a)) for a in t], .14, color='FFFFFF', alfa=.85 - k * .25)
    return g


# las letras van con remates, como de imprenta: la T de palo seco parecía una cruz
LETRA_V = [(-6, -13), (-1.2, -13), (-1.2, -11.8), (-2.2, -11.8), (0, -4.6), (2.2, -11.8), (1.2, -11.8), (1.2, -13), (6, -13), (6, -11.8),
           (5, -11.8), (1.4, 0), (-1.4, 0), (-5, -11.8), (-6, -11.8)]
LETRA_T = [(-6, -13), (6, -13), (6, -9.2), (5, -9.2), (4.6, -10.4), (1.6, -10.4), (1.6, -1.2), (3, -1.2), (3, 0), (-3, 0), (-3, -1.2),
           (-1.6, -1.2), (-1.6, -10.4), (-4.6, -10.4), (-5, -9.2), (-6, -9.2)]


def nace(l):
    cielo(l, sol=None)
    nube(l, 30, 5.4, 14, .6)
    nube(l, 62, 4, 10, .5)
    # a la derecha, lejos, las tierras altas de Etiopía
    cordillera(l, [(56, 18), (64, 11.4), (72, 7.6), (80, 10.2), (88, 6.2), (96, 9.4), (104, 5.8), (112, 8.6), (122, 7.4)], material='lejos',
               alto=.35)
    cordillera(l, [(62, 19), (70, 14.6), (80, 15.6), (90, 12.8), (100, 14.8), (110, 12.4), (122, 14)], material='cuerpo', alto=.3, linea=.35)
    # la tierra, que tapa el pie de las montañas; llana a la izquierda, hasta el horizonte
    suelo = Polygon([(-2, 15.4), (54, 15.4), (64, 17.6), (80, 18.4), (100, 18.2), (122, 18.6), (122, 41.5), (-2, 41.5)])
    t = l.masa(suelo, material='vientre', alto=.08, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(suelo, 'E8B952', .3, dentro=t)
    # lejos, a la izquierda, el lago Victoria, que se pierde en el horizonte, con la selva en su orilla; a la derecha, el lago Tana
    agua(l, forma([(-2, 15.6), (44, 15.6), (52, 16.6), (46, 18.8), (26, 19.6), (-2, 19.4)], 2), ondas=6, semilla=1, linea=.25)
    selva(l, 44, 62, 17.6, 2.8, semilla=2, emergentes=1)
    agua(l, ovalo(94, 19.8, 12, 1.5), ondas=2, semilla=3, linea=.25)
    # los dos ríos que nacen y bajan hacia nosotros: el Nilo Blanco, claro, y el Nilo Azul, oscuro, que cae por su catarata
    nilo_blanco(l, cinta([(40, 19.2), (35.6, 22.6), (39, 27.4), (47, 33.4), (53, 41.5)], [1.4, 2.6, 4.4, 6.6, 9]), ondas=7, semilla=4)
    nilo_azul(l, cinta([(84, 20.6), (84.6, 23.2), (79, 28.4), (72, 34.4), (67.6, 41.5)], [1.2, 2.2, 4.2, 6.4, 9]), ondas=7, semilla=5)
    for k in range(4):                                                   # la catarata del Nilo Azul: la espuma blanca
        l.trazo([(83.4 + k * .5, 21.6), (83.6 + k * .5, 23.2), (83.2 + k * .5, 24.6)], [.3, .26, .12], color='FFFFFF', alfa=.9)
    l.mancha(ovalo(84, 24.8, 2.6, .8), 'FFFFFF', .7, difuso=.3)
    for x, y, h in ((30, 25.4, 4.6), (27, 32.4, 6), (16, 36.6, 6.6), (50, 27.6, 4.4), (56, 33.2, 5.4)):
        papiro(l, x, y, h, 7, semilla=int(x * 3))
    pasto(l, 2, 120, 24, 40.6, 30, semilla=6)
    # las protagonistas: la inicial de cada lago, dorada y parada en su agua: la V de Victoria y la T de Tana
    inicial(l, LETRA_V, 20, 18.4, 1.0)
    inicial(l, LETRA_T, 97, 20.6, .95)


# ------------------------------------------------------------------------------------------------ Jinja
def jinete(l, cx, cy):
    """un jinete que salta a caballo, mirando a la derecha: el caballo, dorado, estirado en el aire, con las manos dobladas debajo del
    pecho, las patas de atrás estiradas y la cola y la crin oscuras que vuelan; el jinete inclinado hacia adelante, con su sombrero"""
    T = lambda pts: [(cx + u, cy + v) for u, v in pts]
    lejanas = [tubo(T([(5, 1.8), (8.2, 3.8), (6.4, 5.8)]), [1, .75, .5], 6), tubo(T([(-7, 1.4), (-10.6, 4.6), (-14.4, 6.4)]), [1.4, .8, .5], 6)]
    lejanas += [ovalo(cx + 6.1, cy + 6.2, .7, .45, 30), ovalo(cx - 14.9, cy + 6.6, .75, .45, 20)]
    lj = l.masa(lejanas, material='acento', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.2)
    l.mancha(unary_union(lejanas), '6B4E10', .4, dentro=lj)             # las patas del otro lado, en sombra
    l.masa(tubo(T([(-8, -1.4), (-11.8, -2.8), (-15.6, -1.2), (-18, -.2)]), [.9, 1.15, .8, .3], 8), material='oscuro', alto=.3, brillo=.25,
           vientre=0, hondo=0, linea=.3)                                # la cola, que vuela
    torso = forma(T([(-8.4, -.6), (-7, -2.8), (-2, -3.4), (4, -3.2), (7.6, -2), (8.6, .4), (7, 2.6), (2, 3), (-3, 3), (-7, 2.4)]), 3)
    cuello = tubo(T([(6, -1.4), (9, -5.4), (10.6, -8)]), [2.3, 1.7, 1.3], 8)
    cabeza = forma(T([(10, -8.6), (11, -10), (12.6, -9.8), (15.2, -7.6), (16, -6.6), (15.4, -5.8), (12.6, -6.4), (10.6, -6.6)]), 2)
    oreja = Polygon(T([(10.9, -9.7), (11.2, -11.6), (12, -9.9)]))
    manos = [tubo(T([(6.2, 1.4), (9.4, 3), (7.8, 5.2)]), [1.1, .8, .55], 6)]
    patas = [tubo(T([(-6, .8), (-9.8, 3.4), (-13.8, 4.6)]), [1.7, .9, .6], 6)]
    cascos = [ovalo(cx + 7.5, cy + 5.6, .75, .5, 30), ovalo(cx - 14.3, cy + 4.9, .8, .5, 15)]
    c = l.masa([torso, cuello, cabeza, oreja] + manos + patas, material='acento', alto=.45, brillo=.35, vientre=0, hondo=.1, linea=.45,
               escalon=.2, contraluz=.35, bultos=[(ovalo(cx - 5, cy - .4, 3, 2.4), .2), (ovalo(cx + 4.6, cy - .6, 2.6, 2.2), .2)])
    l.masa(cascos, material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.25)
    l.masa(tubo(T([(6.6, -3.2), (8.4, -6.2), (10, -9.4)]), [.75, .65, .55], 6), material='oscuro', alto=.3, brillo=.25, vientre=0, hondo=0,
           linea=.25)                                                    # la crin
    l.mancha(ovalo(cx + 13.2, cy - 8.4, .3, .3), '05201C', 1, dentro=c)    # el ojo
    l.mancha(ovalo(cx + 15.2, cy - 6.6, .3, .25), '05201C', .8, dentro=c)  # el ollar
    # el jinete: la pierna en el costado, el cuerpo inclinado, el brazo que lleva las riendas, la cabeza con su sombrero
    l.masa([tubo(T([(.6, -3.2), (3.4, -1.4), (2.4, 1.6)]), [.95, .8, .6], 6), ovalo(cx + 2.6, cy + 2, .95, .6)], material='oscuro', alto=.3,
           brillo=.25, vientre=0, hondo=0, linea=.3)
    j = l.masa(forma(T([(-.6, -3.2), (-.4, -5.6), (1.4, -8.2), (3.2, -8.8), (4.4, -7.6), (3.2, -5), (2, -3.2)]), 2), material='claro',
               alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.trazo(T([(2.6, -8.2), (1.4, -5.6), (1, -3.6)]), [.05, .12, .05], color='8EB5AA', alfa=.7, dentro=j)
    l.masa(tubo(T([(3.4, -7.8), (5.8, -6.8), (8.2, -6.4)]), [.6, .55, .45], 6), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.35)
    l.trazo(T([(8.4, -6.4), (11.6, -6.2), (14.6, -6.4)]), .1, alfa=.9)      # las riendas
    h = l.masa(ovalo(cx + 4.4, cy - 9.9, 1.25, 1.35), material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(ovalo(cx + 4.4, cy - 9.9, 1.4, 1.5), 'A2683A', .6, dentro=h)
    l.mancha(ovalo(cx + 5.1, cy - 10, .18, .18), '05201C', 1, dentro=h)
    l.masa(forma(T([(2.2, -10.4), (3.2, -12.2), (5.2, -12.4), (5.8, -10.9), (7, -10.5), (6.6, -10.1), (1.8, -10.1)]), 1), material='acento',
           alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)              # el sombrero
    return unary_union([torso, cuello, cabeza] + manos + patas)


def jinja(l):
    cielo(l, sol=None)
    nube(l, 28, 5, 12, .55)
    nube(l, 96, 4.4, 10, .45)
    prado(l, 18, 41, .14)
    # el lago Victoria, que se pierde en el horizonte, y el Nilo Blanco que sale de él hacia la derecha
    lago = forma([(-2, 18), (64, 18), (70, 20.2), (66, 23.6), (52, 26.8), (30, 28.4), (8, 28.6), (-2, 28.4)], 2)
    agua(l, lago, ondas=10, semilla=1)
    selva(l, 62, 122, 19.6, 4, semilla=2, emergentes=2)
    nilo_blanco(l, cinta([(58, 23), (72, 26.4), (86, 29.6), (100, 33.4), (122, 37)], [5, 6, 7, 8, 9]), ondas=6, semilla=3)
    # río abajo, la represa de Owen Falls, que tapó las cataratas Ripon: el muro con sus compuertas y el agua blanca
    p = l.masa(box(96, 27.6, 112, 31.4).buffer(.15), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.4, escalon=.2,
               contraluz=.25)
    for x in np.arange(98, 111, 3):
        l.mancha(box(x, 29.4, x + 1.6, 31.4), '0C3A33', .7, dentro=p)
        l.trazo([(x + .8, 31.6), (x + .6, 33.6), (x + 1.2, 35.4)], [.5, .6, .2], color='FFFFFF', alfa=.85)
    l.mancha(ovalo(104, 35.6, 8, 1.4), 'FFFFFF', .6, difuso=.5)
    # la orilla de adelante, con papiros y pasto
    m = orilla(l, forma([(-2, 41.5), (-2, 32.4), (16, 31), (36, 31.6), (54, 33.6), (70, 37.4), (78, 41.5)], 2), tinte=.16)
    pasto(l, 0, 70, 33, 40.6, 18, semilla=4, dentro=m)
    for x, y, h in ((6, 32.6, 6), (22, 32, 5.4)):
        papiro(l, x, y, h, 7, semilla=int(x))
    # el salto: la corona de agua donde el caballo dejó el lago, con sus gotas, y el jinete en el aire sobre el río que nace
    sx, sy = 40, 26.4
    corona = [ovalo(sx, sy, 3.4, .9)]
    for k, a in enumerate(np.linspace(196, 344, 9)):
        r, ang = (3.6 if k % 2 == 0 else 2.4), math.radians(a)
        corona.append(Polygon([(sx + 1.5 * math.cos(ang - .3), sy + .5 * math.sin(ang - .3)), (sx + r * math.cos(ang), sy + r * .95 * math.sin(ang)),
                               (sx + 1.5 * math.cos(ang + .3), sy + .5 * math.sin(ang + .3))]))
    l.masa(unary_union(corona).buffer(.1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25, arroja=False)
    l.masa([ovalo(x, y, r, r * 1.15) for x, y, r in ((35.4, 21.6, .45), (38.4, 20.6, .4), (42.4, 21, .45), (45, 22.6, .4), (33.6, 23.6, .35))],
           material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2, arroja=False)
    g = jinete(l, 59, 17.4)
    reflejo(l, g, 27, .2)


# ------------------------------------------------------------------------------------------------ Juba
def bebe(l, x, y, s=1.0):
    """el país recién nacido: un bebé con su chupón, dormido y contento, envuelto en su manta dentro de una canasta que flota, con una
    banderita de estrella dorada en la mano; (x, y) es el centro de la cara, `s` la escala"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, ang=0: ovalo(x + u * s, y + v * s, rx * s, ry * s, ang)
    canasta = forma(P([(-8.2, 3.6), (8.2, 3.6), (7.4, 6.4), (5, 8), (-5, 8), (-7.4, 6.4)]), 2)
    l.mancha(O(0, 8.2, 10, 1.4), '0C3A33', .25, difuso=.6 * s)            # la sombra en el agua
    # la banderita: el asta y la tela con su estrella
    l.masa(tubo(P([(5.4, 3.4), (6.6, -9)]), [.22 * s, .18 * s], 4), material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    b = l.masa(Polygon(P([(6.5, -9), (12.4, -7.4), (6.3, -5.6)])).buffer(.1 * s), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0,
               linea=.3)
    est = P([(8.2 + .95 * math.sin(math.radians(a)) * (1 if k % 2 == 0 else .42), -7.4 - .95 * math.cos(math.radians(a)) * (1 if k % 2 == 0 else .42))
             for k, a in enumerate(range(0, 360, 36))])
    l.mancha(Polygon(est), 'E8B952', 1, dentro=b)
    # la manta, la mano que agarra el asta, la cabeza
    manta = forma(P([(-6.4, 4), (-5.6, 1.2), (-3, 2.6), (0, 3.2), (3, 2.4), (5.8, 1.4), (6.6, 4)]), 2)
    m = l.masa(manta, material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    for k in range(3):
        l.trazo(P([(-5 + k * 3.6, 2.2), (-4 + k * 3.6, 3.8)]), [.05, .14 * s, .05], color='8EB5AA', alfa=.7, dentro=m)
    cara, orejas, mano = O(0, 0, 3.5, 3.3), [O(-3.4, .2, .6, .8), O(3.4, .2, .6, .8)], O(5.6, 2.6, .9, .75)
    c = l.masa([cara] + orejas + [mano], material='vientre', alto=.5, brillo=.15, vientre=0, hondo=0, linea=.4, contraluz=.25)
    l.mancha(box(x - 5 * s, y - 5 * s, x + 7 * s, y + 4 * s), PIEL, .45, dentro=c)
    for dx in (-2, 2):                                                   # los cachetes
        l.mancha(O(dx, 1, .9, .55), 'E8B952', .35, dentro=c)
    for dx in (-1.4, 1.4):                                               # los ojos cerrados, contentos
        l.trazo(P([(dx - .6, -.7), (dx, -1.1), (dx + .6, -.7)]), .16 * s, alfa=.9, dentro=c)
    l.trazo(P([(-.2, -3.2), (.4, -4), (1.2, -3.6), (.8, -3)]), .2 * s, color='0C3A33', alfa=.9)    # el rulo
    # el chupón: el escudo claro sobre la boca, el botón y el aro dorado
    l.masa(O(0, 1.3, 1.5, .85), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25, arroja=False)
    l.masa(O(0, 2, .9, .75).difference(O(0, 2, .5, .4)), material='acento', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.2)
    # la canasta tejida, que flota
    k_ = l.masa(canasta, material='acento', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for v in np.arange(4.4, 8, .9):
        l.trazo(P([(-8, v), (8, v)]), .1 * s, color='6B4E10', alfa=.5, dentro=k_)
    for u in np.arange(-7.4, 8, 1.4):
        l.trazo(P([(u, 3.6), (u + .3, 8)]), .07 * s, color='93701A', alfa=.45, dentro=k_)
    l.trazo(P([(-8.2, 3.7), (8.2, 3.7)]), .3 * s, color='6B4E10', alfa=.6, dentro=k_)
    return canasta.union(cara)


def juba(l):
    rng = np.random.default_rng(2)
    cielo(l, sol=None)
    nube(l, 32, 5, 14, .55)
    nube(l, 92, 4, 10, .45)
    prado(l, 18.6, 41, .2)
    # río abajo, a la derecha, el Sudd: el pantano de papiros que se pierde en el horizonte, con sus brazos de agua
    for x0, x1, y in ((60, 122, 21.4), (70, 122, 19.8)):
        agua(l, Polygon([(x0, y), (x1, y - .4), (x1, y + .9), (x0 + 4, y + 1)]), linea=.15)
    for x in np.arange(62, 122, 3.2):
        papiro(l, x + rng.uniform(-.6, .6), 20.6 + rng.uniform(-.4, .6), rng.uniform(2.2, 3), 5, semilla=int(x * 10))
    # la orilla de Juba, a la izquierda: las casas de techo de lata y unos árboles de mango
    for x, w in ((6, 7), (15, 6), (24, 7.4), (34, 6)):
        c = l.masa(box(x - w / 2, 17, x + w / 2, 21.6).buffer(.1), material='vientre', alto=.25, brillo=.05, vientre=0, hondo=0, linea=.35)
        l.mancha(box(x - w / 2, 17, x + w / 2, 21.6), 'E8B952', .25, dentro=c)
        l.mancha(box(x - .6, 18.8, x + .6, 21.6), '164F46', .8, dentro=c)
        t = l.masa(Polygon([(x - w / 2 - .6, 17.4), (x - w / 2 + .6, 15.4), (x + w / 2 + .6, 15.4), (x + w / 2 + .6, 17.4)]).buffer(.08),
                   material='claro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.35)
        for k in np.arange(x - w / 2, x + w / 2 + .6, .7):              # la lata ondulada
            l.trazo([(k, 15.5), (k - .5, 17.3)], .08, color='8EB5AA', alfa=.8, dentro=t)
    for x in (42, 50):
        l.masa([ovalo(x + dx, 16.4 + dy, 2.6, 2) for dx, dy in ((0, 0), (-1.8, 1), (1.8, .9))] + [tubo([(x, 22), (x, 18.4)], [.35, .3], 4)],
               material='lejos', alto=.3, brillo=.08, vientre=0, hondo=0, linea=.3)
    # el río, y el muelle de Juba con su barco de carga
    rio(l, 22.8)
    l.masa([box(2, 22.4, 36, 23.6)] + [box(x, 23.4, x + .5, 25.4) for x in np.arange(3, 36, 4)], material='lejos', alto=.2, brillo=.15,
           vientre=0, hondo=0, linea=.3)
    l.masa(forma([(4, 26), (26, 26), (29, 24.2), (3, 24.4)], 1), material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    cab = l.masa(box(7, 21.6, 15, 24.4).buffer(.1), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    for x in (8.4, 11, 13.6):
        l.mancha(box(x - .5, 22.4, x + .5, 23.4), '164F46', .8, dentro=cab)
    # la orilla de adelante, con papiros
    m = orilla(l, forma([(-2, 41.5), (-2, 36.6), (12, 35.4), (26, 36.8), (34, 41.5)], 2), tinte=.2)
    pasto(l, 0, 30, 37, 40.6, 8, semilla=3, dentro=m)
    papiro(l, 8, 37, 6, 7, semilla=4)
    papiro(l, 112, 38.6, 6.4, 7, semilla=5)
    papiro(l, 104, 39.6, 5, 6, semilla=6)
    # el país recién nacido, grande, en su canasta, que flota en medio del río
    g = bebe(l, 60, 21.6, 1.62)
    reflejo(l, g, 34.6, .2)


# ------------------------------------------------------------------------------------------------ Jartum
def jarra(l, x, y, s=1.0, giro=105.0, espejo=False):
    """una jarra de barro, de panza ancha, con su asa y su pico, volcada para vaciarse (con `espejo`, hacia la izquierda); (x, y) es el
    medio de la panza; da la punta del pico, por donde sale el chorro"""
    sx = -1 if espejo else 1
    P = lambda pts: [(x + u * s * sx, y + v * s) for u, v in pts]
    R = lambda g: affinity.rotate(g, giro * sx, origin=(x, y))
    punto = lambda p: R(Point(p)).coords[0]
    cuerpo = forma(P([(-2.4, 5), (-3.6, 2.6), (-3.8, .4), (-3.2, -1.6), (-2, -3.4), (-2.6, -4.8), (2.4, -4.8), (4.4, -5.8), (3.2, -4.4),
                      (2, -3.4), (3.2, -1.6), (3.8, .4), (3.6, 2.6), (2.4, 5)]), 2)
    asa = tubo(P([(-2.2, -3.2), (-5, -2.4), (-5.2, .6), (-3.6, 1.4)]), [.5 * s] * 4, 8)
    m = l.masa([R(cuerpo), R(asa)], material='acento', alto=.45, brillo=.3, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.35)
    for v in (-1.4, 2.2):                                                # las franjas pintadas de la jarra
        l.trazo([punto(p) for p in P([(-3.9, v), (0, v + .5), (3.9, v)])], .35 * s, color='6B4E10', alfa=.7, dentro=m)
    l.mancha(R(ovalo(x, y - 4.8 * s, 2.2 * s, .5 * s)), '05201C', .8)    # la boca, oscura por dentro
    return punto(P([(4.4, -5.8)])[0])


def jartum(l):
    cielo(l, sol=None)
    nube(l, 60, 3.4, 12, .45)
    tierra(l, 18.2, 41, desierto=.34)
    # enfrente, Omdurmán: las casas bajas, la cúpula del Mahdi y un minarete, con palmeras
    for x, w, h in ((34, 7, 3.4), (42, 6, 2.8), (50, 6, 3.6), (72, 7, 3), (80, 6.4, 3.6), (88, 6, 2.8)):
        c = l.masa(box(x - w / 2, 19.4 - h, x + w / 2, 19.6).buffer(.1), material='vientre', alto=.2, brillo=.05, vientre=0, hondo=0,
                   linea=.3)
        l.mancha(box(x - w / 2, 15, x + w / 2, 19.6), 'E8B952', .3, dentro=c)
        l.mancha(box(x - .5, 17.6, x + .5, 19.6), '164F46', .75, dentro=c)
    l.masa(box(55.6, 13.4, 64.4, 19.6).buffer(.1), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.masa(forma([(55, 13.6), (55.6, 11), (57.6, 8.4), (60, 6.6), (62.4, 8.4), (64.4, 11), (65, 13.6)], 2), material='claro', alto=.5,
           brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)          # la cúpula del Mahdi, plateada
    l.trazo([(60, 6.8), (60, 4.4)], .16, alfa=.9)
    l.masa([box(67.6, 9.6, 69.2, 19.6), box(67, 12.4, 69.8, 13.2)], material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(67.4, 9.8), (68.4, 7), (69.4, 9.8)]), material='cuerpo', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    for x, h, lado in ((8, 6, 1), (112, 6.6, -1), (117, 5.4, 1)):
        palmera(l, x, 19.8, h, lado, datiles=False)
    # el Nilo Blanco viene de la izquierda y el Nilo Azul de la derecha; se juntan y bajan lado a lado, cada uno de su color
    blanco = cinta([(-2, 23), (24, 24.4), (46, 26.4), (58, 28.6)], [5, 5.4, 6, 6.4])
    azul = cinta([(122, 22.4), (96, 23.8), (74, 26.2), (62, 28.6)], [4, 4.6, 5.2, 6])
    junto = Polygon([(54, 27.4), (66, 27.4), (76, 41.5), (44, 41.5)])
    medio = [(60 + .8 * math.sin(k * .9), 27.4 + k * 1.4) for k in range(11)]
    lado_b = Polygon([(54, 27.4)] + medio + [(44, 41.5)]).buffer(0)
    lado_a = Polygon(medio + [(76, 41.5), (66, 27.4)]).buffer(0)
    nilo_blanco(l, blanco.union(lado_b.intersection(junto)), ondas=8, semilla=1)
    nilo_azul(l, azul.union(lado_a.intersection(junto)), ondas=8, semilla=2)
    # las dos jarras, grandes, que vacían cada una su agua en su río: la de agua blanca en el Nilo Blanco, la de agua azul en el Azul
    for jx, esp, hasta, material, color_ in ((22, False, 24.8, 'vientre', 'C6EEDC'), (98, True, 24.4, 'lejos', '246E61')):
        px, py = jarra(l, jx, 9, 1.62, 105, esp)
        d = -1 if esp else 1
        ch = cinta([(px, py), (px + d * 1.2, py + (hasta - py) * .5), (px + d * 1.8, hasta)], [2.3, 2.1, 2.6], 8)
        c = l.masa(ch, material=material, alto=.15, brillo=.2, vientre=0, hondo=0, linea=.3, arroja=False)
        l.mancha(ch, color_, .75, dentro=c)
        l.trazo([(px - d * .2, py + .6), (px + d * .8, py + (hasta - py) * .5), (px + d * 1.3, hasta - 1)], [.1, .26, .1], color='FFFFFF',
                alfa=.85, dentro=c)
        for k in range(5):                                               # la salpicadura
            a = math.radians(-160 + k * 35)
            l.mancha(ovalo(px + d * 1.8 + 2.6 * math.cos(a), hasta - .4 + 1.2 * math.sin(a), .42, .36), 'FFFFFF', .9)
    pasto(l, 2, 40, 34, 40.6, 8, semilla=5)
    pasto(l, 82, 118, 34, 40.6, 8, semilla=6)


# ------------------------------------------------------------------------------------------------ Asuán
def asuan(l):
    rng = np.random.default_rng(4)
    cielo(l, sol=None)
    nube(l, 30, 4.6, 14, .5)
    nube(l, 92, 3.6, 10, .4)
    # al fondo, la Presa Alta de orilla a orilla, entre cerros de desierto, con el agua blanca que sale por sus compuertas
    tierra(l, 15, 41, desierto=.4)
    for pts in (((-2, 13.4), (6, 9.4), (16, 10.4), (26, 12.6)), ((94, 12.6), (104, 9.2), (114, 10.4), (122, 9.4))):
        l.masa(forma([(pts[0][0], 14)] + list(pts) + [(pts[-1][0], 14)], 2), material='vientre', alto=.3, brillo=.05, vientre=0, hondo=0,
               linea=.35, contraluz=.2)
    dique = Polygon([(-2, 12.6), (122, 12.6), (122, 17.8), (-2, 17.8)])
    d = l.masa(dique, material='vientre', alto=.2, brillo=.05, vientre=0, hondo=0, linea=.4, escalon=.15, contraluz=.25)
    l.mancha(dique, 'E8B952', .3, dentro=d)
    for _ in range(110):                                                 # las piedras del terraplén
        x, y = rng.uniform(-2, 122), rng.uniform(13.8, 17.6)
        l.mancha(ovalo(x, y, rng.uniform(.4, .9), rng.uniform(.2, .45)), '93701A', .3, dentro=d)
    l.trazo([(-2, 13.4), (122, 13.4)], .2, color='6B4E10', alfa=.5, dentro=d)
    comp = l.masa(box(50, 13.6, 70, 18.4).buffer(.12), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, escalon=.2)
    for x in (53, 58, 63, 68):
        l.mancha(forma([(x - 1.5, 18.4), (x - 1.5, 16), (x, 15), (x + 1.5, 16), (x + 1.5, 18.4)], 1), '0C3A33', .85, dentro=comp)
    # el río que baja de la presa hacia nosotros, con las rocas de granito de la primera catarata
    lecho = Polygon([(48, 18), (72, 18), (106, 41.5), (14, 41.5)])
    agua(l, lecho, ondas=10, semilla=3)
    for x in (53, 58, 63, 68):                                           # el agua blanca que sale de cada compuerta
        l.trazo([(x, 18.4), (x + (x - 60.5) * .1, 20), (x + (x - 60.5) * .18, 21.4)], [1, 1.2, .5], color='FFFFFF', alfa=.85)
    l.mancha(ovalo(60.5, 21.4, 11, 1.3), 'FFFFFF', .5, difuso=.5)
    rocas = [ovalo(x, y, r * 1.3, r) for x, y, r in ((38, 30.4, 1.4), (34, 33.6, 1.8), (84, 30.6, 1.5), (88.6, 34, 2), (44, 22.4, .8),
                                                    (77, 22.6, .9))]
    r = l.masa(rocas, material='oscuro', alto=.6, brillo=.4, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.mancha(box(20, 18, 100, 42), '3E7A6D', .2, dentro=r)
    for x, h, lado in ((6, 7.4, 1), (12, 6.2, -1), (110, 6.8, -1), (116, 8, 1)):
        palmera(l, x, 24.4, h, lado, datiles=False)
    # la aduana: la caseta en la orilla izquierda, y la barrera a rayas que cruza el río de orilla a orilla, sobre sus dos postes
    cas = l.masa(box(2.6, 20.4, 15.4, 30.6).buffer(.15), material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.4,
                 escalon=.2, contraluz=.25)
    l.mancha(box(4.4, 22.4, 13.6, 26), '164F46', .85, dentro=cas)          # la ventanilla
    l.mancha(box(4.4, 24.6, 13.6, 25.2), 'CFE0DA', .9, dentro=cas)          # su mostrador
    l.masa(Polygon([(1.4, 20.8), (9, 17.6), (16.6, 20.8)]).buffer(.12), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.trazo([(13.6, 18.6), (13.6, 12.6)], .16, alfa=.9)                    # el asta y su bandera
    l.masa(Polygon([(13.6, 12.6), (17.8, 13.6), (13.6, 14.8)]).buffer(.08), material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0,
           linea=.25)
    l.masa([box(16.8, 22.6, 19.4, 32.6).buffer(.1), box(100.6, 22.6, 103.2, 32.6).buffer(.1)], material='lejos', alto=.3, brillo=.2,
           vientre=0, hondo=0, linea=.35)
    barrera = box(18, 23.6, 102, 26.8).buffer(.2)
    b = l.masa(barrera, material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.3)
    for x0 in np.arange(19.4, 101, 5.2):                                 # las rayas de la barrera
        l.mancha(Polygon([(x0, 22), (x0 + 2.6, 22), (x0 + 1.6, 28.4), (x0 - 1, 28.4)]), 'E8B952', .95, dentro=b)
    l.masa(ovalo(18.1, 25.2, 1.8, 1.8), material='oscuro', alto=.3, brillo=.35, vientre=0, hondo=0, linea=.3)   # el eje
    # la falúa que espera que levanten la barrera
    g = faluca(l, 62, 37.4, 1.05, lado=-1)
    reflejo(l, g, 37.6, .2)


# ------------------------------------------------------------------------------------------------ Luxor
def mascara(l, x, y, s=1.0):
    """la máscara de oro de un faraón, de frente: el tocado a rayas que cae sobre los hombros, la cara de oro, los ojos pintados, la
    barba trenzada, la cobra en la frente y el collar ancho; (x, y) es el medio de la cara"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    tocado = forma(P([(-4.2, -7.4), (4.2, -7.4), (5.4, -5.4), (6.6, 0), (7.6, 4.4), (5, 5), (4.6, 9.4), (2.6, 9.4), (2.6, 3), (-2.6, 3),
                      (-2.6, 9.4), (-4.6, 9.4), (-5, 5), (-7.6, 4.4), (-6.6, 0), (-5.4, -5.4)]), 1)
    t = l.masa(tocado, material='acento', alto=.4, brillo=.35, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.35)
    for v in np.arange(-6.4, 9.6, 1.25):                                 # las rayas del tocado
        l.trazo(P([(-8, v), (8, v + .2)]), .5 * s, color='164F46', alfa=.85, dentro=t)
    collar = Polygon(P([(-7.2, 4.6), (7.2, 4.6), (6, 8.2), (2.6, 9.6), (-2.6, 9.6), (-6, 8.2)])).buffer(.1)
    c = l.masa(collar, material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.25)
    for k, tono in enumerate(('164F46', 'FBEFCB', '164F46', 'FBEFCB')):  # las vueltas del collar
        r = 6.2 - k * 1.1
        l.trazo(P([(-r, 4.8 + k * .9), (-r * .55, 6.4 + k * 1.1), (0, 6.9 + k * 1.1), (r * .55, 6.4 + k * 1.1), (r, 4.8 + k * .9)]),
                .4 * s, color=tono, alfa=.8, dentro=c)
    cara = forma(P([(-3.4, -5.4), (3.4, -5.4), (3.6, -1.6), (3, 1.6), (1.6, 3.4), (-1.6, 3.4), (-3, 1.6), (-3.6, -1.6)]), 2)
    f = l.masa(cara, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.3,
               bultos=[(ovalo(x, y + .2 * s, 1 * s, 2 * s), .2)])
    l.mancha(cara, 'FBEFCB', .2, dentro=f)
    for sx in (-1, 1):                                                   # los ojos pintados y las cejas
        l.mancha(forma(P([(sx * .6, -2), (sx * 1.6, -2.6), (sx * 2.7, -2.1), (sx * 3.4, -2), (sx * 2.6, -1.4), (sx * 1.6, -1.3)]), 1), 'FFFFFF',
                 .9, dentro=f)
        l.mancha(ovalo(x + sx * 1.6 * s, y - 1.9 * s, .38 * s, .4 * s), '05201C', 1, dentro=f)
        l.trazo(P([(sx * .5, -2), (sx * 1.6, -2.7), (sx * 2.8, -2.2), (sx * 3.6, -1.8)]), .18 * s, color='164F46', alfa=.95, dentro=f)
        l.trazo(P([(sx * .6, -3.2), (sx * 1.8, -3.7), (sx * 3.2, -3.2)]), .3 * s, color='164F46', alfa=.9, dentro=f)
    l.trazo(P([(0, -1.6), (-.2, .4), (.5, .6)]), .12 * s, color='93701A', alfa=.8, dentro=f)
    l.trazo(P([(-1, 1.6), (0, 1.9), (1, 1.6)]), .2 * s, color='93701A', alfa=.8, dentro=f)
    barba = forma(P([(-.7, 3.2), (.7, 3.2), (.8, 7), (.4, 7.6), (-.4, 7.6), (-.8, 7)]), 1)
    b = l.masa(barba, material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.35)
    for v in np.arange(3.9, 7.4, .7):
        l.trazo(P([(-.8, v), (.8, v + .2)]), .22 * s, color='164F46', alfa=.8, dentro=b)
    l.masa(forma(P([(-.6, -5.2), (-.5, -7), (0, -8), (.5, -7), (.6, -5.2)]), 1), material='acento', alto=.4, brillo=.5, vientre=0,
           hondo=0, linea=.3)                                            # la cobra de la frente
    return tocado.union(collar)


def luxor(l):
    cielo(l, sol=None, tarde=.4)
    # el sol que se pone detrás de los cerros de la orilla oeste: pálido, medio tapado
    l.mancha(ovalo(22, 15.6, 9, 9), 'F2D48A', .35, difuso=2.4)
    l.mancha(ovalo(22, 15.6, 4.2, 4.2), 'F2D48A', .8)
    # la orilla de los muertos, al oeste: los cerros del Valle de los Reyes, con las puertas de las tumbas, y la máscara de oro
    cerros = forma([(-2, 22), (10, 17.4), (22, 15.4), (32, 13.6), (40, 8.6), (46, 12.4), (58, 11), (74, 12.6), (86, 10.4), (98, 13.4),
                    (110, 12), (122, 14.6), (122, 25), (-2, 25)], 2)
    c = l.masa(cerros, material='vientre', alto=.35, brillo=.05, vientre=0, hondo=.1, linea=.4, escalon=.2, contraluz=.3)
    l.mancha(cerros, 'E8B952', .34, dentro=c)
    for x, y in ((14, 19.4), (28, 18.4), (86, 17), (100, 18.6), (110, 17.6)):
        l.mancha(forma([(x - .8, y + 1.6), (x - .8, y), (x, y - .6), (x + .8, y), (x + .8, y + 1.6)], 1), '0C3A33', .8, dentro=c)
    mascara(l, 60, 12.2, 1.28)
    # el río en medio, con una falúa
    rio(l, 24.8)
    f = faluca(l, 90, 29.4, .7)
    reflejo(l, f, 29.6, .2)
    # la orilla de los vivos, al este: las columnas de Karnak, con sus capiteles de papiro, un obelisco y el pilono, entre palmeras
    orilla(l, forma([(-2, 41.5), (-2, 32.4), (20, 31.6), (50, 32.2), (80, 33), (122, 32.4), (122, 41.5)], 2), tinte=.3)
    for x in np.arange(4, 46, 7):
        col = [box(x - 1.3, 28, x + 1.3, 38), forma([(x - 2.4, 28.2), (x - 2.6, 26.8), (x - 1.6, 25.8), (x + 1.6, 25.8), (x + 2.6, 26.8),
                                                     (x + 2.4, 28.2)], 1), box(x - 2, 24.8, x + 2, 26), box(x - 1.8, 37.8, x + 1.8, 38.8)]
        k = l.masa(col, material='vientre', alto=.4, brillo=.12, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
        l.mancha(box(x - 3, 24, x + 3, 40), 'E8B952', .3, dentro=k)
        for yy in (30, 32.8, 35.6):                                      # los relieves de las columnas
            l.trazo([(x - 1.1, yy), (x + 1.1, yy + .2)], .12, color='6B4E10', alfa=.5, dentro=k)
            l.trazo([(x - .5, yy + .7), (x + .4, yy + 1.2)], .1, color='6B4E10', alfa=.4, dentro=k)
    l.masa(box(1, 23.8, 46, 25).buffer(.1), material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.4)
    obelisco(l, 52, 38.6, 16, 1.7, punta='vientre')
    for x, h, lado in ((70, 8.4, 1), (77, 9.6, -1), (115, 8.8, -1)):
        palmera(l, x, 38, h, lado, datiles=False)
    py = [forma([(84, 38.6), (85.4, 28), (95, 28), (96.4, 38.6)], 0), forma([(100, 38.6), (101.4, 28), (111, 28), (112.4, 38.6)], 0),
          box(95, 31, 101, 38.6)]
    p = l.masa(unary_union(py).difference(box(96.6, 33.4, 99.4, 38.8)), material='vientre', alto=.3, brillo=.1, vientre=0, hondo=0,
               linea=.4, escalon=.2, contraluz=.3)
    l.mancha(box(82, 27, 114, 40), 'E8B952', .3, dentro=p)
    for x0 in (87, 103):
        l.trazo([(x0, 31), (x0 + 2.4, 31)], .14, color='6B4E10', alfa=.5, dentro=p)
        l.trazo([(x0 + 1.2, 32), (x0 + 1.2, 35.6)], .14, color='6B4E10', alfa=.45, dentro=p)


# ------------------------------------------------------------------------------------------------ El Cairo
def cairo(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None)
    # visto desde muy arriba y desde el mar, mirando al sur: el Nilo baja del horizonte y en la punta, donde está la ciudad, se abre en
    # abanico hasta el mar, que queda adelante; el delta, protagonista, es un triángulo dorado, como la letra Δ (con el triángulo
    # marcado solo por una línea punteada, no se veía)
    tierra(l, 6, 41, desierto=.3)
    agua(l, box(-2, 34.4, 122, 41.5), ondas=10, semilla=1, linea=0)
    apice = (60, 15)
    costa = [(2, 35), (12, 35.8), (22, 35), (32, 35.8), (42, 35), (52, 35.8), (62, 35), (72, 35.8), (82, 35), (92, 35.8), (102, 35),
             (112, 35.8), (118, 35.2)]
    delta = Polygon([apice] + costa).buffer(.3)
    d = l.masa(delta, material='acento', alto=.15, brillo=.35, vientre=0, hondo=0, linea=.6, escalon=.1, contraluz=.25)
    for _ in range(90):                                                  # los campos del delta
        x, y = rng.uniform(4, 116), rng.uniform(16, 35)
        l.mancha(ovalo(x, y, rng.uniform(.8, 2.2), rng.uniform(.3, .8)), str(rng.choice(['6B4E10', 'FBEFCB'])), .16, dentro=d)
    # los brazos del río, como las varillas del abanico, más anchos adelante, y el Nilo que baja derecho del horizonte hasta la punta
    brazos = [cinta([apice, (apice[0] + (bx - apice[0]) * .5, 25.4), (bx, 35.6)], [a * .6, a, a * 1.7], 8)
              for bx, a in ((8, 1.5), (22, .9), (38, 1), (60, .9), (82, 1), (98, .9), (112, 1.5))]
    nilo = Polygon([(59.7, 6), (60.3, 6), (60.8, apice[1] + .6), (59.2, apice[1] + .6)])
    agua(l, unary_union(brazos + [nilo]), ondas=4, semilla=2, linea=.25)
    # la ciudad en la punta del delta: torres, minaretes y una cúpula; y del lado oeste, a la derecha, las pirámides de Guiza
    for x, w, h in ((51, 1.8, 4.4), (53.4, 1.6, 3), (66, 1.8, 3.6), (68.2, 1.6, 5)):
        t = l.masa(box(x - w / 2, 15.6 - h, x + w / 2, 15.6).buffer(.06), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0,
                   linea=.25)
        for yy in np.arange(15.6 - h + .6, 15.2, .8):
            l.trazo([(x - w / 2 + .25, yy), (x + w / 2 - .25, yy)], .07, color='8EB5AA', alfa=.8, dentro=t)
    for x, h in ((56, 5.4), (63.6, 4.6)):
        l.masa([box(x - .3, 15.6 - h, x + .3, 15.6), box(x - .55, 15.6 - h * .6, x + .55, 15.6 - h * .6 + .3)], material='claro', alto=.25,
               brillo=.15, vientre=0, hondo=0, linea=.2)
        l.masa(Polygon([(x - .35, 15.6 - h), (x, 15.6 - h - 1.1), (x + .35, 15.6 - h)]), material='cuerpo', alto=.3, brillo=.3, vientre=0,
               hondo=0, linea=.15)
    l.masa(box(57.4, 13.4, 62.4, 15.8).buffer(.06), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    l.masa(forma([(57.8, 13.6), (58.4, 12.2), (59.9, 11.2), (61.4, 12.2), (62, 13.6)], 2), material='cuerpo', alto=.45, brillo=.4, vientre=0,
           hondo=0, linea=.25)
    for x, b, w, h in ((74, 16.4, 6.4, 4.8), (81, 16.6, 5.6, 4.2), (86.4, 16.8, 3.4, 2.6)):
        piramide(l, x, b, w, h, luz=-1)


# ------------------------------------------------------------------------------------------------ el mar
def faro(l, x, base, s=1.0):
    """el faro de Alejandría, como lo cuentan las descripciones antiguas: tres cuerpos, uno sobre otro (el de abajo, cuadrado y alto,
    con sus ventanas; el del medio, octogonal; el de arriba, redondo, con el fuego) sobre su zócalo; dorado, porque la carga sigue
    hasta Alejandría"""
    P = lambda pts: Polygon([(x + u * s, base + v * s) for u, v in pts])
    cuerpos = [P([(-7.6, 0), (7.6, 0), (7.6, -1.8), (-7.6, -1.8)]), P([(-5.4, -1.8), (5.4, -1.8), (4.6, -12.4), (-4.6, -12.4)]),
               P([(-5.4, -12.4), (5.4, -12.4), (5.4, -13.3), (-5.4, -13.3)]), P([(-3.4, -13.3), (3.4, -13.3), (3, -19.4), (-3, -19.4)]),
               P([(-3.7, -19.4), (3.7, -19.4), (3.7, -20.1), (-3.7, -20.1)]), P([(-2, -20.1), (2, -20.1), (1.8, -23.4), (-1.8, -23.4)]),
               forma([(x - 2.2 * s, base - 23.4 * s), (x - 1.6 * s, base - 24.8 * s), (x, base - 25.6 * s), (x + 1.6 * s, base - 24.8 * s),
                      (x + 2.2 * s, base - 23.4 * s)], 2)]
    m = l.masa(cuerpos, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.35)
    for v in (-4.6, -8.4):                                               # las ventanas
        for u in (-2.6, 0, 2.6):
            l.mancha(box(x + (u - .45) * s, base + (v - 1.2) * s, x + (u + .45) * s, base + v * s), '6B4E10', .75, dentro=m)
    for u in (-1.4, 1.4):
        l.mancha(box(x + (u - .35) * s, base - 17.4 * s, x + (u + .35) * s, base - 15.8 * s), '6B4E10', .75, dentro=m)
    l.mancha(box(x - .9 * s, base - 22.8 * s, x + .9 * s, base - 21 * s), 'FFFFFF', .9, dentro=m)       # el fuego
    return unary_union(cuerpos)


def gabarra(l, x, y, s=1.0):
    """una gabarra, mirando a la derecha: el casco largo y chato, de madera, cargado de sacos, con su timón atrás y un palo con su vela
    cuadrada chica; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa(Polygon(P([(-1, -2), (-.6, -2), (-.6, -10), (-1, -10)])), material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
    v = l.masa(Polygon(P([(-4, -9.6), (2.4, -9.6), (2.8, -4.4), (-3.6, -4.4)])).buffer(.1 * s), material='claro', alto=.3, brillo=.15,
               vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.trazo(P([(-3.8, -7), (2.6, -7)]), .08, color='8EB5AA', alfa=.7, dentro=v)
    sacos = [ovalo(x + u * s, y + v_ * s, 1.6 * s, .9 * s) for u, v_ in ((-5.6, -2.4), (-2.4, -2.4), (.8, -2.4), (4, -2.4), (-4, -3.8),
                                                                           (-.8, -3.8), (2.4, -3.8))]
    sc = l.masa(sacos, material='claro', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.3, contraluz=.25)
    l.mancha(unary_union(sacos), 'B08A6A', .35, dentro=sc)
    casco = forma(P([(-8.6, -1.8), (8.4, -1.8), (9.6, -2.6), (8.2, .6), (-7.8, .6), (-9, -2.4)]), 1)
    c = l.masa(casco, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.25)
    l.mancha(casco, 'A2683A', .55, dentro=c)
    l.trazo(P([(-8.2, -.6), (8.6, -.6)]), .1, color='6B4E10', alfa=.6, dentro=c)
    l.trazo(P([(-8.6, -1.6), (-10.4, .8)]), .3, alfa=.85)              # el timón
    return casco


def mar(l):
    cielo(l, sol=None)
    nube(l, 40, 7, 16, .55)
    nube(l, 98, 5, 12, .45)
    horizonte = 21.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0,
               contraluz=0, arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 3), '64C8AA', .55, dentro=m, difuso=.8)
    rng = np.random.default_rng(8)
    for _ in range(22):
        x, y = rng.uniform(30, 116), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # a la derecha, en su isla, el faro de Alejandría, dorado, protagonista
    l.masa(forma([(78, horizonte + 3.6), (82, horizonte + .4), (106, horizonte + .4), (112, horizonte + 3.6)], 1), material='lejos',
           alto=.2, brillo=.05, vientre=0, hondo=0, linea=.35)
    fr = faro(l, 94, horizonte + 1.6, .82)
    reflejo(l, fr.intersection(box(-2, 0, 122, horizonte + 1.6)), horizonte + 3.6, .22)
    # la última orilla del delta, a la izquierda, partida por el brazo del Nilo, que se abre al mar
    canal = cinta([(-2, 27), (14, 27.4), (28, 27), (40, 26.2), (52, 25.4)], [2.4, 3, 3.8, 5.6, 9], 8)
    tierra_ = forma([(-2, 20.6), (12, 20.4), (26, 21.2), (38, 22.4), (46, 25.4), (40, 29.6), (24, 31.6), (8, 32.4), (-2, 32.8)], 2)
    orilla(l, tierra_.difference(canal), tinte=.36)
    for x, y, h, lado in ((6, 23.6, 8.6, 1), (13, 23.8, 7, -1), (24, 24.2, 7.8, 1), (10, 31.2, 9, -1), (20, 30.4, 7.4, 1)):
        palmera(l, x, y, h, lado, datiles=False)
    # la gabarra, cargada, que sigue hacia Alejandría, y la falúa, la barca del Nilo, de madera, que da la vuelta hacia el sur
    g = gabarra(l, 64, 29.6, 1.1)
    reflejo(l, g, 29.8, .2)
    g = faluca(l, 40, 36.4, 1.2, lado=-1)
    reflejo(l, g, 36.6, .2)
    for x, y, s in ((30, 9, 1), (36, 7.4, .8), (100, 8.6, .7)):
        ave(l, x, y, s)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Jinja', dibujar=jinja), dict(clave='Juba', dibujar=juba),
            dict(clave='Jartum', dibujar=jartum), dict(clave='Asuán', dibujar=asuan), dict(clave='Luxor', dibujar=luxor),
            dict(clave='El Cairo', dibujar=cairo), dict(clave='mar', dibujar=mar)]
LISTO = True
