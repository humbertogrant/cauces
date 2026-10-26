# -*- coding: utf-8 -*-
"""Las postales del Amazonas, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol.

- el nacimiento: en los Andes del Perú, el nevado Mismi, donde suele ponerse su fuente más lejana: el glaciar del que sale un arroyito
  que pasa por una laguna y baja hacia nosotros por la puna, con alpacas, y un cóndor que planea;
- Iquitos: «un taxi flotante»: a Iquitos no llega ninguna carretera; un taxi dorado flota en el río, frente a las casas que flotan, un
  delfín rosado salta a su lado y una avioneta pasa en el cielo, porque solo se entra por río o por aire;
- Leticia: «tres vecinas se dan la mano en una esquina»: Leticia, Tabatinga y Santa Rosa, en la triple frontera: tres mujeres que se
  toman de la mano a la orilla del río;
- Manaos: «dos manos que no se juntan»: el Río Negro, oscuro, y el Solimões, café con leche, que corren lado a lado sin mezclarse, y
  dos manos, una de cada color, que se buscan sin tocarse; enfrente, la ciudad con la cúpula del Teatro Amazonas;
- Santarém: «un santo con un camión lleno de soya»: el camión, con la caja llena de soya dorada y un santo de aureola al volante, que
  va al puerto, donde los silos cargan los barcos;
- Belém: «Belén, el nacimiento»: la estrella de Belén, dorada, sobre el estuario donde el río nace al mar; en la orilla, el mercado
  Ver-o-Peso con sus torrecitas y los barcos, y las palmeras de asaí;
- el mar: el regatão, la barca del juego, que sale al Atlántico entre manglares, donde el agua café del río empuja al mar azul.
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, agua, ave, cielo, cinta, cordillera, mangle, nube, orilla, palmera, pasto, prado, reflejo, rio, selva,  # noqa: F401
                     tierra)
from pintor import forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
CAFE = 'BF9129'            # el café con leche del Solimões y del agua del río, sobre el pálido de `vientre`


# ------------------------------------------------------------------------------------------------ el nacimiento
def alpaca(l, x, base, s=1.0, lado=1, material='claro', semilla=0):
    """una alpaca de pie, de perfil, mirando a la derecha (o a la izquierda con `lado` -1): el cuerpo lanudo, el cuello largo, la
    cabeza chica con sus orejas paradas y las patas finas"""
    P = lambda pts: [(x + u * s * lado, base + v * s) for u, v in pts]
    cuerpo = ovalo(x, base - 4.6 * s, 4 * s, 2.5 * s)
    cuello = tubo(P([(2.4, -5.6), (3.3, -8), (3.6, -10.2)]), [1.35 * s, 1.1 * s, .95 * s], 6)
    cabeza = forma(P([(2.9, -10), (3.1, -11.4), (4.1, -11.9), (5.5, -11.3), (5.9, -10.4), (5.1, -9.9)]), 1)
    orejas = [Polygon(P([(3.1, -11.3), (3, -12.9), (3.7, -11.6)])), Polygon(P([(3.8, -11.6), (3.9, -13.1), (4.4, -11.7)]))]
    patas = [tubo(P([(u, -3.4), (u, -.3)]), [.75 * s, .5 * s], 4) for u in (-2.6, -1.3, 1.5, 2.7)]
    m = l.masa([cuerpo, cuello, cabeza] + orejas + patas, material=material, alto=.45, brillo=.15, vientre=.1, hondo=0, linea=.35,
               contraluz=.3)
    l.pelaje(m, densidad=7, largo=.45, ancho=.11, alfa=.4, semilla=semilla, claro=.45, flujo=90, mechon=2)
    l.mancha(ovalo(x + 4.8 * s * lado, base - 10.9 * s, .22 * s, .22 * s), '05201C', 1, dentro=m)


def condor(l, x, y, s=1.0):
    """un cóndor que planea: las alas largas y anchas, con las plumas de la punta abiertas como dedos y la franja blanca, el collar
    blanco y la cabeza chica"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    alas = forma(P([(-12, -.6), (-9, -1.8), (-4, -1.6), (-1.4, -.8), (1.4, -.8), (4, -1.6), (9, -1.8), (12, -.6), (9.6, .4), (4, .6),
                    (1.4, 1.2), (-1.4, 1.2), (-4, .6), (-9.6, .4)]), 1)
    dedos = [tubo(P([(sx * 11, -.8 + k * .45), (sx * 13.6, -1.5 + k * .75)]), [.32 * s, .1 * s], 4) for sx in (-1, 1) for k in range(4)]
    cola = Polygon(P([(-1, 1), (1, 1), (.8, 3), (-.8, 3)]))
    m = l.masa([alas, cola, ovalo(x, y + .5 * s, 1.6 * s, 1 * s)] + dedos, material='oscuro', alto=.3, brillo=.25, vientre=0, hondo=0,
               linea=.3, contraluz=.3)
    for sx in (-1, 1):
        l.trazo(P([(sx * 2.6, -.3), (sx * 6, -.6), (sx * 9, -.4)]), [.1, .45 * s, .2], color='CFE0DA', alfa=.75, dentro=m)
    l.masa(ovalo(x, y - .8 * s, 1.1 * s, .6 * s), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.masa(ovalo(x, y - 1.7 * s, .6 * s, .55 * s), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)


def nace(l):
    cielo(l, sol=None)
    nube(l, 22, 6, 14, .6)
    nube(l, 100, 5, 10, .45)
    # los Andes: el nevado Mismi, al medio, más alto, y cerros más bajos a los lados, con nieve en las cumbres
    cordillera(l, [(-2, 20), (8, 14), (18, 16.4), (28, 11.4), (38, 15), (48, 9), (60, 2.4), (72, 9.4), (82, 14.6), (92, 10.8), (104, 15.4),
                   (114, 12), (122, 15)], material='lejos', nieve=10.6, linea=.4)
    # el glaciar que baja del Mismi: sale de la nieve de la cumbre, sin borde arriba, y se angosta valle abajo
    lengua = cinta([(60, 7.6), (59.4, 11), (60.4, 14), (60.1, 16.8)], [3.4, 2.8, 2.4, 2.2], 8)
    g = l.masa(lengua, material='claro', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    for y0 in (11.4, 13, 14.6):                                          # las grietas del hielo
        l.trazo([(58.8, y0), (60, y0 + .4), (61.2, y0)], .1, color='8EB5AA', alfa=.8, dentro=g)
    l.trazo([(58, 9), (58.2, 11), (59, 14), (59, 16.6), (60.1, 17.8)], [.06, .16, .16, .16, .06], color='8EB5AA', alfa=.8)
    l.trazo([(62, 9), (61.6, 11), (61.6, 14), (61.2, 16.6), (60.1, 17.8)], [.06, .12, .12, .12, .06], color='8EB5AA', alfa=.6)
    # la puna: el pasto alto y amarillento de la altura
    puna = forma([(-2, 23), (14, 21.6), (30, 22.8), (46, 21), (60, 20.2), (76, 21.4), (92, 22.6), (108, 21.2), (122, 22.4), (122, 41.5),
                  (-2, 41.5)], 2)
    p = l.masa(puna, material='vientre', alto=.1, brillo=.04, vientre=0, hondo=0, linea=.3, escalon=.1, contraluz=.2)
    l.mancha(puna, 'E8B952', .34, dentro=p)
    # el arroyito que sale del glaciar, la laguna, y el río recién nacido que baja hacia nosotros
    agua(l, cinta([(60.4, 17), (59.6, 19.6), (58.4, 22.4)], [.6, .9, 1.2], 6), linea=.2)
    agua(l, ovalo(56, 24.6, 9.6, 2), ondas=2, semilla=1, linea=.25)
    agua(l, cinta([(52, 26), (49, 30), (53.4, 34.6), (48.6, 38.4), (51, 41.5)], [1.2, 2, 3, 4, 5.2], 10), ondas=3, semilla=2, linea=.25)
    pasto(l, 2, 118, 25, 40.6, 34, semilla=3)
    # las alpacas, y el cóndor
    alpaca(l, 24, 34.4, 1.1, 1, 'claro', semilla=4)
    alpaca(l, 34, 37.4, .95, -1, 'vientre', semilla=5)
    alpaca(l, 90, 36.6, 1.2, -1, 'claro', semilla=6)
    condor(l, 92, 9, 1.1)


# ------------------------------------------------------------------------------------------------ Iquitos
def taxi(l, x, y, s=1.0):
    """un taxi que flota en el río, de costado, mirando a la derecha: la carrocería dorada con su franja a cuadros, las ventanas, el
    letrero en el techo y las ruedas medio hundidas; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, r: ovalo(x + u * s, y + v * s, r * s, r * s)
    ruedas = [O(u, -.6, 2.3) for u in (-8.6, 8.8)]
    l.masa(ruedas, material='oscuro', alto=.4, brillo=.35, vientre=0, hondo=0, linea=.35)
    l.masa([O(u, -.6, .9) for u in (-8.6, 8.8)], material='claro', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.25)
    cuerpo = forma(P([(-14.6, -1.6), (-14.9, -4.6), (-13.2, -5.6), (-7, -6), (-4.6, -10.4), (5.4, -10.4), (8.6, -6.2), (13.4, -5.6),
                      (14.9, -4.2), (14.7, -1.6)]), 1)
    cuerpo = cuerpo.difference(O(-8.6, -.6, 2.9)).difference(O(8.8, -.6, 2.9))
    c = l.masa(cuerpo, material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.35)
    for ventana in (P([(-4, -9.8), (.2, -9.8), (.2, -6.4), (-6.2, -6.4)]), P([(1, -9.8), (5, -9.8), (7.8, -6.4), (1, -6.4)])):
        l.mancha(Polygon(ventana).buffer(.1 * s), '164F46', .9, dentro=c)
        l.mancha(Polygon(ventana).buffer(-.25 * s), 'A4DCC4', .9, dentro=c)
    for k, u in enumerate(np.arange(-14, 14.4, 1.4)):                   # la franja a cuadros
        l.mancha(Polygon(P([(u, -5 + .7 * (k % 2)), (u + .7, -5 + .7 * (k % 2)), (u + .7, -4.3 + .7 * (k % 2)), (u, -4.3 + .7 * (k % 2))])),
                 '0C3A33', .95, dentro=c)
        l.mancha(Polygon(P([(u + .7, -5 + .7 * ((k + 1) % 2)), (u + 1.4, -5 + .7 * ((k + 1) % 2)), (u + 1.4, -4.3 + .7 * ((k + 1) % 2)),
                            (u + .7, -4.3 + .7 * ((k + 1) % 2))])), '0C3A33', .95, dentro=c)
    l.trazo(P([(.6, -6.2), (.6, -1.8)]), .12 * s, color='6B4E10', alfa=.7, dentro=c)        # la puerta
    l.mancha(O(14, -4.6, .6), 'FBEFCB', 1, dentro=c)                     # el farol
    letrero = l.masa(Polygon(P([(-2.6, -12.2), (2.6, -12.2), (2.6, -10.4), (-2.6, -10.4)])).buffer(.15 * s), material='claro', alto=.25,
                     brillo=.3, vientre=0, hondo=0, linea=.3)
    l.mancha(Polygon(P([(-2, -11.7), (2, -11.7), (2, -10.9), (-2, -10.9)])), '0C3A33', .85, dentro=letrero)
    return cuerpo.union(unary_union(ruedas))


def boto(l, x, y, s=1.0):
    """un delfín rosado del Amazonas que salta en arco, mirando a la derecha: el pico largo, la frente redonda, la cresta baja del lomo y
    las aletas grandes; (x, y) es el agua bajo el medio del salto"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    cuerpo = tubo(P([(-6.4, .4), (-3.6, -3), (0, -4.4), (3.6, -3.4), (6, -1.2)]), [.5 * s, 1.4 * s, 1.8 * s, 1.5 * s, 1 * s], 10)
    cabeza = ovalo(x + 5.6 * s, y - 1.8 * s, 1.4 * s, 1.2 * s)
    pico = tubo(P([(6.4, -1.2), (8.6, .4)]), [.5 * s, .3 * s], 4)
    cola = Polygon(P([(-6.4, .4), (-8.2, -.6), (-7.2, .8), (-8, 2), (-6, 1)]))
    aleta = Polygon(P([(2, -2.6), (3.6, -.6), (1.2, -1.4)]))
    m = l.masa([cuerpo, cabeza, pico, cola, aleta], material='claro', alto=.45, brillo=.25, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.mancha(ovalo(x + 5.4 * s, y - 2.3 * s, .2 * s, .2 * s), '05201C', 1, dentro=m)
    for dx in (-6, 6.6):                                                 # las salpicaduras de donde sale y adonde cae
        for k in range(4):
            a = math.radians(-150 + k * 40)
            l.mancha(ovalo(x + dx * s + 1.6 * s * math.cos(a), y + 1 * s * math.sin(a), .3 * s, .3 * s), 'FFFFFF', .9)


def avioneta(l, x, y, s=1.0):
    """una avioneta que pasa lejos, de costado: el fuselaje, el ala, la cola y la hélice"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([forma(P([(-5, -.4), (3.6, -.8), (5, 0), (3.6, .8), (-5, .4)]), 1), Polygon(P([(-1.4, -.2), (1.6, -.2), (.2, 2.6), (-.8, 2.6)])),
            Polygon(P([(-5, -.4), (-5.8, -2.6), (-4.4, -2.6), (-3.6, -.4)]))], material='claro', alto=.25, brillo=.3, vientre=0, hondo=0,
           linea=.25)
    l.trazo(P([(5.2, -1.4), (5.2, 1.4)]), .14 * s, alfa=.8)


def iquitos(l):
    rng = np.random.default_rng(2)
    cielo(l, sol=None)
    nube(l, 30, 5, 14, .55)
    nube(l, 84, 4, 10, .45)
    avioneta(l, 102, 8, 1.2)
    rio(l, 21.6)
    selva(l, -2, 122, 21.8, 5.6, semilla=2, emergentes=3)
    # a la izquierda, las casas que flotan en el río, sobre sus balsas
    for x, w in ((6, 8), (17, 7), (27.4, 7.6)):
        l.masa(box(x - w / 2 - .6, 26.6, x + w / 2 + .6, 27.8).buffer(.1), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
        c = l.masa(box(x - w / 2, 22.6, x + w / 2, 26.8).buffer(.1), material='vientre', alto=.25, brillo=.05, vientre=0, hondo=0, linea=.35)
        l.mancha(box(x - .7, 24.2, x + .7, 26.8), '164F46', .8, dentro=c)
        t = l.masa(Polygon([(x - w / 2 - 1, 22.8), (x, 19.6), (x + w / 2 + 1, 22.8)]).buffer(.1), material='lejos', alto=.25, brillo=.1,
                   vientre=0, hondo=0, linea=.35)
        for k in np.arange(x - w / 2, x + w / 2, .7):                   # la paja del techo
            l.trazo([(x, 19.8), (k, 22.7)], .06, color='0C3A33', alfa=.4, dentro=t)
    # el taxi que flota, protagonista, al medio, con el agua que le moja las ruedas
    g = taxi(l, 60, 32.4, 1.15)
    l.mancha(box(40, 32.4, 80, 35.4).intersection(g), '246E61', .55)
    for k in range(7):                                                   # la espuma alrededor
        x0 = 42 + k * 5.6 + rng.uniform(-.6, .6)
        l.trazo([(x0, 32.6), (x0 + 1.6, 32.3), (x0 + 3.2, 32.6)], .22, color='FFFFFF', alfa=.85)
    reflejo(l, g, 32.6, .22)
    boto(l, 94, 33.6, 1.2)


# ------------------------------------------------------------------------------------------------ Leticia
def vecina(l, x, base, vestido, tono, pelo, manos, semilla=0):
    """una vecina de frente, contenta: el vestido, la cara con sus ojos y su sonrisa, el pelo (`moño`, `largo` o `rizos`) y los brazos
    hasta sus `manos` (dos puntos, la izquierda y la derecha)"""
    hombros = [(x - 2.1, base - 13.8), (x + 2.1, base - 13.8)]
    piel = []
    if pelo == 'largo':                                                  # el pelo largo cae detrás de los hombros
        l.masa(forma([(x - 2.6, base - 18.6), (x - 3.2, base - 15), (x - 3.4, base - 11.6), (x + 3.4, base - 11.6), (x + 3.2, base - 15),
                      (x + 2.6, base - 18.6), (x, base - 19.8)], 2), material='oscuro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.3)
    for (hx, hy), (mx, my) in zip(hombros, manos):                       # los brazos
        piel.append(tubo([(hx, hy), ((hx + mx) / 2, (hy + my) / 2 + .4), (mx, my)], [.7, .6, .55], 6))
        piel.append(ovalo(mx, my, .85, .8))
    piel += [tubo([(x - 1.4, base - 5), (x - 1.6, base - .6)], [.6, .5], 4), tubo([(x + 1.4, base - 5), (x + 1.6, base - .6)], [.6, .5], 4),
             box(x - .7, base - 16.4, x + .7, base - 14)]
    p = l.masa(piel, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(box(x - 30, base - 30, x + 30, base + 2), PIEL, tono, dentro=p)
    l.masa([ovalo(x - 1.8, base - .3, 1.2, .55), ovalo(x + 1.8, base - .3, 1.2, .55)], material='oscuro', alto=.3, brillo=.3, vientre=0,
           hondo=0, linea=.25)                                           # los zapatos
    v = l.masa(forma([(x - 2.2, base - 14.6), (x + 2.2, base - 14.6), (x + 2.6, base - 11.4), (x + 5, base - 4.4), (x - 5, base - 4.4),
                      (x - 2.6, base - 11.4)], 1), material=vestido, alto=.4, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for k in (-1, 1):                                                    # los pliegues de la falda
        l.trazo([(x + k * 1.2, base - 10.4), (x + k * 2.6, base - 4.8)], [.06, .16, .06], color='0C3A33', alfa=.35, dentro=v)
    h = l.masa(ovalo(x, base - 17.6, 2.2, 2.4), material='vientre', alto=.45, brillo=.15, vientre=0, hondo=0, linea=.4, contraluz=.25)
    l.mancha(ovalo(x, base - 17.6, 2.6, 2.8), PIEL, tono, dentro=h)
    for dx in (-.8, .8):
        l.mancha(ovalo(x + dx, base - 17.9, .26, .3), '05201C', 1, dentro=h)
    l.trazo([(x - .8, base - 16.6), (x, base - 16.2), (x + .8, base - 16.6)], .16, color='0C3A33', alfa=.9, dentro=h)    # la sonrisa
    if pelo == 'moño':
        l.masa([forma([(x - 2.3, base - 17.4), (x - 2.2, base - 19.2), (x - 1, base - 20.2), (x + 1, base - 20.2), (x + 2.2, base - 19.2),
                       (x + 2.3, base - 17.4), (x + 1.4, base - 19), (x - 1.4, base - 19)], 2), ovalo(x, base - 21, 1.2, 1)], material='oscuro',
               alto=.35, brillo=.25, vientre=0, hondo=0, linea=.3)
    elif pelo == 'largo':
        l.masa(forma([(x - 2.4, base - 17), (x - 2.3, base - 19.2), (x - 1, base - 20.2), (x + 1, base - 20.2), (x + 2.3, base - 19.2),
                      (x + 2.4, base - 17), (x + 1, base - 19.2), (x - 1.2, base - 19)], 2), material='oscuro', alto=.35, brillo=.25, vientre=0,
               hondo=0, linea=.3)
    else:
        l.masa([ovalo(x + dx, base - 19.4 + dy, .95, .9) for dx, dy in ((-2, .8), (-1.4, -.4), (0, -.9), (1.4, -.4), (2, .8), (-2.4, 2), (2.4, 2))],
               material='oscuro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.3)


def leticia(l):
    cielo(l, sol=None)
    nube(l, 22, 5, 14, .55)
    nube(l, 96, 4, 10, .45)
    rio(l, 19.6)
    selva(l, -2, 122, 19.8, 5, semilla=3, emergentes=3)
    # la esquina, adelante: el pasto de la orilla y las tres vecinas que se dan la mano: Leticia, Tabatinga y Santa Rosa
    m = orilla(l, forma([(-2, 41.5), (-2, 29.4), (20, 28.2), (44, 27.6), (76, 27.6), (100, 28.4), (122, 29.6), (122, 41.5)], 2), tinte=.2)
    pasto(l, 0, 120, 30, 40.8, 30, semilla=4, dentro=m)
    base = 39
    vecina(l, 40, base, 'acento', .5, 'moño', [(34.6, base - 19.4), (50, base - 9.4)], semilla=5)
    vecina(l, 60, base, 'claro', .3, 'largo', [(50, base - 9.4), (70, base - 9.4)], semilla=6)
    vecina(l, 80, base, 'cuerpo', .65, 'rizos', [(70, base - 9.4), (85.4, base - 19.4)], semilla=7)


# ------------------------------------------------------------------------------------------------ Manaos
def mano(l, x0, y0, x1, y1, lado=1, material='oscuro', tinte=None):
    """un antebrazo que sale del agua en (x0, y0) y la mano que apunta con el índice, la palma hacia abajo, hasta la punta (x1, y1); mira
    a la derecha (o a la izquierda con `lado` -1)"""
    xw, yw = x1 - 9.4 * lado, y1 + 1.8
    brazo = tubo([(x0, y0), ((x0 + xw) / 2, (y0 + yw) / 2 + 1), (xw, yw)], [2.4, 1.9, 1.5], 10)
    palma = forma([(xw - .4 * lado, yw - 1.4), (xw + 3 * lado, yw - 2.4), (x1 - 3.4 * lado, y1 - .8), (x1 - 3 * lado, y1 + 1.4),
                   (xw + 3 * lado, yw + 1.6), (xw, yw + 1.4)], 2)
    indice = tubo([(x1 - 4 * lado, y1 - .2), (x1 - 1.6 * lado, y1 - .1), (x1, y1)], [.62, .55, .48], 6)
    pulgar = tubo([(xw + 1.6 * lado, yw - 1.2), (xw + 3.4 * lado, yw - 2.6), (xw + 4.8 * lado, yw - 2.4)], [.6, .55, .45], 6)
    dedos = [ovalo(x1 - (3.6 + k * 1.3) * lado, y1 + 1.8, .7, .65) for k in range(3)]
    m = l.masa([brazo, palma, indice, pulgar] + dedos, material=material, alto=.5, brillo=.2, vientre=0, hondo=.1, linea=.45, escalon=.2,
               contraluz=.35)
    if tinte:
        l.mancha(box(min(x0, x1) - 6, min(y0, y1) - 6, max(x0, x1) + 6, max(y0, y1) + 6), tinte, .5, dentro=m)
    for k in range(3):                                                   # las uñas y los nudillos
        l.trazo([(x1 - (3.4 + k * 1.3) * lado, y1 + 1.2), (x1 - (3.9 + k * 1.3) * lado, y1 + 1.6)], .1, color='0C3A33', alfa=.4, dentro=m)
    return unary_union([brazo, palma, indice])


def manaos(l):
    rng = np.random.default_rng(4)
    cielo(l, sol=None)
    nube(l, 60, 4, 14, .5)
    # enfrente, la ciudad, con la cúpula del Teatro Amazonas, y la selva
    prado(l, 15, 19.4, .2)
    for x, w, h in ((4, 3, 7), (8.4, 3.4, 9.4), (12.6, 2.6, 6), (36, 3, 8), (40.4, 3.4, 10.6), (45, 2.8, 7)):
        t = l.masa(box(x - w / 2, 19 - h, x + w / 2, 19).buffer(.06), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.25)
        for yy in np.arange(19 - h + .8, 18.6, 1):
            l.trazo([(x - w / 2 + .3, yy), (x + w / 2 - .3, yy)], .07, color='8EB5AA', alfa=.8, dentro=t)
    l.masa(box(17.6, 14.4, 30.4, 19.2).buffer(.1), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.3)
    cup = l.masa(forma([(19.6, 14.6), (20.2, 12), (22.4, 10.2), (24, 9.6), (25.6, 10.2), (27.8, 12), (28.4, 14.6)], 2), material='cuerpo',
                 alto=.5, brillo=.4, vientre=0, hondo=0, linea=.3)
    for k in range(4):                                                   # las tejas de la cúpula
        l.trazo([(20.4 + k * 2.2, 14.4), (24, 9.8)], .08, color='164F46', alfa=.5, dentro=cup)
    selva(l, 50, 122, 19.4, 4.4, semilla=5, emergentes=2)
    # el encuentro de las aguas: el Río Negro, oscuro, y el Solimões, café con leche, lado a lado, sin mezclarse
    medio = [(60 + 1.4 * math.sin(k * .8), 19.4 + k * 2.2) for k in range(11)]
    negro = Polygon([(-2, 19.4)] + medio + [(-2, 41.5)]).buffer(0)
    solimoes = Polygon(medio + [(122, 41.5), (122, 19.4)]).buffer(0)
    n = l.masa(negro, material='oscuro', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 19.4, 122, 21), '3E7A6D', .5, dentro=n)
    so = l.masa(solimoes, material='vientre', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(solimoes, CAFE, .55, dentro=so)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(22, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='6FA497' if x < 60 else 'FBEFCB', alfa=.6)
    for k in range(5):                                                   # los remolinos de la línea donde se encuentran
        x, y = medio[2 + k * 2]
        l.trazo([(x - 1.6, y), (x - .4, y - .8), (x + .8, y), (x - .2, y + .6)], .14, color='E2EDE9', alfa=.6)
    # las dos manos, protagonistas: una de cada agua, que se buscan sin tocarse
    mano(l, 24, 42, 56.2, 24.4, 1, 'oscuro')
    mano(l, 96, 42, 63.8, 24.4, -1, 'vientre', CAFE)


# ------------------------------------------------------------------------------------------------ Santarém
def camion(l, x, y, s=1.0, semilla=0):
    """un camión de carga, de costado, mirando a la derecha, con la caja llena de soya, un montón de granos dorados; en la cabina, un
    santo con su aureola dorada al volante; (x, y) es el suelo bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry: ovalo(x + u * s, y + v * s, rx * s, ry * s)
    rng = np.random.default_rng(semilla)
    # la soya, en un montón que asoma de la caja
    soya = forma(P([(-17.6, -11.6), (-15, -15.4), (-10.6, -17.6), (-5.4, -17), (-1.4, -14.6), (.6, -11.6)]), 2)
    so = l.masa(soya, material='acento', alto=.45, brillo=.35, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    for _ in range(int(170 * s)):
        u, v = rng.uniform(-17.4, .4), rng.uniform(-17.6, -11.8)
        l.mancha(O(u, v, .34, .3), str(rng.choice(['F2D48A', 'BF9129', 'FBEFCB'])), .9, dentro=so)
    # la caja, de tablas, el chasis y las ruedas
    caja = l.masa(Polygon(P([(-18.4, -12.4), (1.2, -12.4), (1.2, -5.6), (-18.4, -5.6)])).buffer(.1 * s), material='lejos', alto=.25,
                  brillo=.15, vientre=0, hondo=0, linea=.4)
    for v in (-10.4, -8.2):
        l.trazo(P([(-18.2, v), (1, v)]), .12 * s, color='0C3A33', alfa=.5, dentro=caja)
    for u in np.arange(-15.4, 0, 4):
        l.trazo(P([(u, -12.2), (u, -5.8)]), .12 * s, color='0C3A33', alfa=.5, dentro=caja)
    l.masa(Polygon(P([(-18.6, -5.8), (16, -5.8), (16, -4), (-18.6, -4)])), material='oscuro', alto=.2, brillo=.3, vientre=0, hondo=0,
           linea=.3)
    ruedas = [O(u, -3, 3, 3) for u in (-12, -6, 9.4)]
    l.masa(ruedas, material='oscuro', alto=.45, brillo=.35, vientre=0, hondo=0, linea=.35)
    l.masa([O(u, -3, 1.2, 1.2) for u in (-12, -6, 9.4)], material='claro', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.25)
    # la cabina, blanca, con su ventana, y el santo adentro, con su aureola
    cab = forma(P([(1.6, -5.8), (1.6, -15.2), (3, -16.6), (9.6, -16.6), (13.4, -11.8), (15.8, -10.6), (16.2, -5.8)]), 1)
    c = l.masa(cab, material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.3)
    ventana = Polygon(P([(3.4, -15.2), (9, -15.2), (12, -11.6), (3.4, -11.6)]))
    l.mancha(ventana.buffer(.15 * s), '164F46', .9, dentro=c)
    l.mancha(ventana, 'A4DCC4', .85, dentro=c)
    l.masa(Polygon(P([(4, -11.6), (9.6, -11.6), (9, -13), (4.6, -13)])).buffer(.1 * s), material='lejos', alto=.2, brillo=.15, vientre=0,
           hondo=0, linea=.25)                                           # el manto, en los hombros
    h = l.masa(O(6.8, -13.6, 1.4, 1.5), material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(O(6.8, -13.6, 1.6, 1.7), PIEL, .4, dentro=h)
    l.masa(forma(P([(5.6, -13.4), (8, -13.4), (7.6, -11.8), (6.8, -11.2), (6, -11.8)]), 1), material='claro', alto=.3, brillo=.2, vientre=0,
           hondo=0, linea=.2)                                            # la barba
    l.mancha(O(7.5, -14, .17, .17), '05201C', 1, dentro=h)
    l.masa(O(6.8, -15.8, 2, .75).difference(O(6.8, -15.8, 1.4, .4)), material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.25)
    l.mancha(O(6.8, -15.8, 3, 1.4), 'F2D48A', .35, difuso=.6 * s)        # el resplandor de la aureola
    l.mancha(O(15.4, -8.4, .7, .6), 'FBEFCB', 1, dentro=c)              # el farol
    l.trazo(P([(8.2, -11.2), (8.2, -6.2)]), .12 * s, color='8EB5AA', alfa=.8, dentro=c)    # la puerta
    return unary_union([cab, soya] + ruedas)


def santarem(l):
    cielo(l, sol=None)
    nube(l, 30, 5, 12, .5)
    # atrás, el río donde el Tapajós, verde, se junta con el Amazonas, café; el puerto con sus silos y un barco que carga
    tierra(l, 17, 22, desierto=.2)
    selva(l, -2, 70, 17.6, 4, semilla=6, emergentes=2)
    rio_ = Polygon([(-2, 21.6), (122, 21.6), (122, 27), (-2, 27)])
    r = l.masa(rio_, material='vientre', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 21.6, 70, 27), CAFE, .45, dentro=r)
    l.mancha(box(70, 21.6, 122, 27), '4AA189', .55, dentro=r, difuso=2)
    for x in (88, 95, 102):                                              # los silos
        si = l.masa([box(x - 2.8, 12.4, x + 2.8, 21.8), ovalo(x, 12.4, 2.8, 1)], material='claro', alto=.35, brillo=.2, vientre=0, hondo=0,
                    linea=.35, contraluz=.3)
        for yy in np.arange(13.6, 21.6, 1.6):
            l.trazo([(x - 2.8, yy), (x + 2.8, yy)], .07, color='8EB5AA', alfa=.8, dentro=si)
    l.masa(tubo([(86, 14), (76, 21.4)], [.4, .4], 4), material='lejos', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)   # la cinta
    l.masa([forma([(60, 22.6), (84, 22.6), (85.4, 24.8), (61, 24.8)], 0), box(80, 19.6, 84, 22.8)], material='lejos', alto=.2, brillo=.1,
           vientre=0, hondo=0, linea=.3)                                 # el barco de la soya
    # el camino de tierra, adelante, y el camión con el santo, protagonista, que va al puerto
    camino = l.masa(forma([(-2, 27), (122, 27), (122, 41.5), (-2, 41.5)], 0), material='vientre', alto=.08, brillo=0, vientre=0, hondo=0,
                    linea=.3, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 27, 122, 42), 'E8B952', .3, dentro=camino)
    for y in (30.4, 35):
        l.trazo([(-2, y), (122, y + .4)], .14, color='93701A', alfa=.35, dentro=camino)
    camion(l, 58, 38.6, 1.3, semilla=7)
    pasto(l, 0, 24, 29, 31, 6, semilla=8)
    pasto(l, 96, 120, 29, 31, 6, semilla=9)


# ------------------------------------------------------------------------------------------------ Belém
def estrella(l, x, y, r, hasta=30.0):
    """la estrella de Belén: ocho puntas, cuatro largas y cuatro cortas, dorada, con su resplandor y su cola de luz que baja"""
    l.mancha(Polygon([(x - r * .25, y), (x + r * .25, y), (x + r * .9, hasta), (x - r * .9, hasta)]), 'F2D48A', .3, difuso=1)
    l.mancha(ovalo(x, y, r * 2.4, r * 2.4), 'F2D48A', .4, difuso=2)
    puntas = []
    for k in range(16):
        a = math.radians(k * 22.5 - 90)
        rr = r if k % 4 == 0 else (r * .55 if k % 2 == 0 else r * .2)
        puntas.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    e = l.masa(Polygon(puntas), material='acento', alto=.4, brillo=.55, vientre=0, hondo=0, linea=.35, contraluz=.35)
    l.mancha(ovalo(x, y, r * .25, r * .25), 'FBEFCB', .95, dentro=e)
    return e


def asai(l, x, y, h, lado=1):
    """una palmera de asaí: el tronco fino y largo y la copa chica de hojas que cuelgan"""
    tope = (x + lado * .6, y - h)
    l.masa(tubo([(x, y), (x + lado * .3, y - h * .5), tope], [.28, .24, .2], 6), material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0,
           linea=.25)
    hojas = []
    for a in (-160, -130, -100, -70, -40, -15, 200):
        d = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))])
        p0 = np.array(tope)
        hojas.append(tubo([p0, p0 + d * 1.6 + np.array([0, -.5]), p0 + d * 3 + np.array([0, 1.4])], [.22, .18, .04], 6))
    l.masa(hojas, material='cuerpo', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.25, contraluz=.2)


def belem(l):
    cielo(l, sol=None, tarde=.15)
    nube(l, 22, 6, 12, .45)
    nube(l, 104, 5, 10, .4)
    # el estuario, ancho, que se abre al mar hasta el horizonte
    horizonte = 20.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2.6), '64C8AA', .55, dentro=m, difuso=.8)
    # la estrella de Belén, protagonista, sobre el río que nace al mar
    estrella(l, 62, 9.6, 8.4, hasta=33)
    rng = np.random.default_rng(5)
    for _ in range(20):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # la orilla de Belém, a la izquierda: el mercado Ver-o-Peso con sus cuatro torrecitas y los barcos en el muelle
    orilla(l, forma([(-2, 17.4), (12, 17), (30, 17.6), (42, 19.2), (46, 23.6), (40, 28.4), (20, 29.6), (-2, 30)], 2), tinte=.24)
    mer = l.masa(box(4, 19.4, 38, 26.2).buffer(.1), material='claro', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.4, escalon=.2)
    for x in np.arange(6.4, 37, 2.6):
        l.mancha(forma([(x, 26), (x, 22.4), (x + .7, 21.6), (x + 1.4, 22.4), (x + 1.4, 26)], 1), '164F46', .8, dentro=mer)
    l.masa(Polygon([(3, 19.6), (39, 19.6), (37, 18), (5, 18)]).buffer(.1), material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    for x in (5, 15.6, 26.4, 37):                                        # las torrecitas de hierro
        l.masa(box(x - 1.2, 15, x + 1.2, 18.4), material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
        l.masa(Polygon([(x - 1.6, 15.2), (x, 12.4), (x + 1.6, 15.2)]), material='lejos', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)
    for x, y, s in ((10, 30.6, 1), (22, 31.6, .9), (33, 30.8, 1)):       # los barcos del muelle
        l.masa(forma([(x - 4 * s, y - .8 * s), (x + 4 * s, y - .8 * s), (x + 3 * s, y + .6 * s), (x - 3 * s, y + .6 * s)], 1), material='lejos',
               alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
        l.masa(box(x - 1.6 * s, y - 2.6 * s, x + 1.2 * s, y - .8 * s), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    for x, h, lado in ((-1, 10.4, 1), (2.6, 8.4, -1), (40, 9, 1)):
        asai(l, x, 22.4 if x > 30 else 19, h, lado)
    # la otra orilla, a la derecha, baja, con sus palmeras de asaí
    orilla(l, forma([(96, 22.6), (104, 21.2), (122, 20.8), (122, 24.4), (100, 24.2)], 1), tinte=.24)
    for x, h, lado in ((104, 7.4, 1), (108, 8.6, -1), (113, 7, 1), (118, 8.2, -1)):
        asai(l, x, 22.4, h, lado)


# ------------------------------------------------------------------------------------------------ el mar
def regatao(l, x, y, s=1.0):
    """el regatão, la barca del vendedor de la Amazonía, mirando a la derecha: el casco largo de canoa, dorado (es la barca del juego),
    el techo de tablas sobre sus postes, las hamacas colgadas y los sacos de la bodega; (x, y) es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([tubo(P([(u, -2), (u, -9.6)]), [.22 * s, .22 * s], 4) for u in (-9, -3, 3, 9)], material='lejos', alto=.2, brillo=.15, vientre=0,
           hondo=0, linea=.25)
    for u0, u1, mat in ((-8.6, -3.4, 'claro'), (3.4, 8.6, 'cuerpo')):     # las hamacas
        l.masa(forma(P([(u0, -8.8), ((u0 + u1) / 2, -6), (u1, -8.8), ((u0 + u1) / 2, -6.8)]), 1), material=mat, alto=.3, brillo=.2,
               vientre=0, hondo=0, linea=.25)
    l.masa([ovalo(x + u * s, y - 2.8 * s, 1.3 * s, 1 * s) for u in (-1.4, 1, -.2)], material='vientre', alto=.4, brillo=.15, vientre=0,
           hondo=0, linea=.3)                                            # los sacos
    techo = Polygon(P([(-11.6, -9.6), (11.6, -9.6), (10.6, -11.4), (-10.6, -11.4)])).buffer(.1 * s)
    t = l.masa(techo, material='lejos', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.35)
    for u in np.arange(-10, 11, 1.6):
        l.trazo(P([(u, -11.3), (u + .2, -9.7)]), .08, color='0C3A33', alfa=.5, dentro=t)
    casco = forma(P([(-15, -3.4), (-13, -1), (-8, .9), (8, .9), (13.4, -1.2), (15.8, -3.8), (13.6, -2.6), (8, -1.8), (-8, -1.8), (-13.2, -2.4)]), 1)
    c = l.masa(casco, material='acento', alto=.35, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.trazo(P([(-12.6, -1.4), (0, -.4), (12.6, -1.6)]), [.05, .14, .05], color='6B4E10', alfa=.6, dentro=c)
    return casco.union(techo)


def mar(l):
    cielo(l, sol=None)
    nube(l, 30, 7, 16, .55)
    nube(l, 92, 5, 12, .45)
    horizonte = 21
    # el mar azul, al fondo, y el agua café del río, adelante, que lo empuja
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2.6), '64C8AA', .55, dentro=m, difuso=.8)
    cafe = Polygon([(-2, 29)] + [(x, 28.6 + .8 * math.sin(x / 7)) for x in np.arange(0, 122.1, 4)] + [(122, 41.5), (-2, 41.5)])
    l.mancha(cafe, CAFE, .5, dentro=m, difuso=1.2)
    l.mancha(cafe, 'E2EDE9', .18, dentro=m, difuso=1.2)
    rng = np.random.default_rng(9)
    for _ in range(22):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4' if y < 29 else 'FBEFCB', alfa=.65)
    # un faro, lejos, en una punta de tierra
    l.masa(forma([(96, horizonte + .6), (106, horizonte - .6), (122, horizonte - .4), (122, horizonte + 1.4), (96, horizonte + 1.4)], 1),
           material='vientre', alto=.15, brillo=0, vientre=0, hondo=0, linea=.3)
    f = l.masa(forma([(110.4, horizonte - .4), (111, 12.4), (113, 12.4), (113.6, horizonte - .4)], 0), material='claro', alto=.3, brillo=.2,
               vientre=0, hondo=0, linea=.3)
    l.mancha(box(108, 15, 116, 16.4), '2F8A74', .85, dentro=f)
    l.masa(box(110.6, 10.4, 113.4, 12.6).buffer(.1), material='claro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(110.4, 10.6), (112, 9), (113.6, 10.6)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    # los manglares, a los costados, parados en el agua sobre sus raíces
    for x, y, h in ((4, 31, 10), (12, 33.4, 11), (20, 30.4, 8.4), (102, 32.4, 9), (110, 34.6, 11), (118, 31.6, 9.6)):
        mangle(l, x, y, h, semilla=int(x))
    for x, y, s in ((36, 8, 1), (42, 6.4, .8), (78, 9.4, .9)):
        ave(l, x, y, s)
    # el regatão, la barca del juego, protagonista, que sale al Atlántico
    g = regatao(l, 60, 34.6, 1.25)
    reflejo(l, g, 34.8, .22)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Iquitos', dibujar=iquitos), dict(clave='Leticia', dibujar=leticia),
            dict(clave='Manaos', dibujar=manaos), dict(clave='Santarém', dibujar=santarem), dict(clave='Belém', dibujar=belem),
            dict(clave='mar', dibujar=mar)]
LISTO = True
