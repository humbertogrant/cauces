# -*- coding: utf-8 -*-
"""Las postales del Murray, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo la naranja que hace de sol en Mildura.

- el nacimiento: los Alpes Australianos, nevados, con sus eucaliptos de la nieve, y un canguro dorado que salta en la nieve junto al
  río recién nacido: Alpes, pero australianos;
- Albury: «en un albergue al pie de la montaña, un ornitorrinco pide la cama de arriba y una manta de lana»: el ornitorrinco dorado, en
  la cama de arriba de la cucheta, tapado con su manta; abajo, el río que ya separa dos estados;
- Echuca: «un eco repite el silbato de los vapores contra un muelle de madera altísimo»: el vapor de ruedas silba y el eco dorado rebota
  contra el muelle de tres pisos, cada vez más chico;
- Swan Hill: «una colina llena de cisnes negros que graznan toda la noche»: de noche, con la luna llena, la colina llena de cisnes
  negros, con un filo de luna, que graznan con sus graznidos dorados, y la carpa de lona de Mitchell, con su farol, que no lo dejan
  dormir;
- Mildura: «una naranja gigante hace de sol sobre un desierto verde»: la naranja dorada, en el cielo, sobre los naranjales y las viñas
  regados en la tierra roja;
- Renmark: «un marinero renombra cada uva de la parra»: el marinero, con su gorra, le pone etiqueta a cada uva dorada del racimo, en la
  parra junto al río;
- Murray Bridge: «un puente de hierro le hace cosquillas al río con los pies»: el puente dorado, cuyas pilas terminan en pies que le
  hacen cosquillas al agua, que se ríe; arriba pasa el tren;
- Goolwa: «una gaviota cierra unas compuertas enormes»: la gaviota empuja la última de las compuertas doradas de la barrera, entre el
  lago dulce y el mar salado;
- el mar: la boca del Murray, angosta entre las dunas, y la draga dorada que la mantiene abierta, con su caño que tira la arena; los
  pelícanos en el banco (el vapor se queda ante las barreras).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, cordillera, nube, orilla, palmera, pasto, piedra, prado,  # noqa: F401
                     reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'
ROJA = '9A5446'            # la tierra roja de Mildura


def piel(l, piezas, tono=.45):
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def eucalipto(l, x, base, h, semilla=0, material='claro'):
    """un eucalipto de la nieve: el tronco blanco y torcido, con sus ramas, y la copa rala"""
    rng = np.random.default_rng(semilla)
    pts = [(x, base), (x + rng.uniform(-1, 1), base - h * .4), (x + rng.uniform(-1.4, 1.4), base - h * .75)]
    t = l.masa([tubo(pts, [h * .06, h * .045, h * .03], 5), tubo([pts[1], (pts[1][0] + h * .2, pts[1][1] - h * .3)], [h * .03, h * .015], 3),
                tubo([pts[1], (pts[1][0] - h * .18, pts[1][1] - h * .34)], [h * .03, h * .015], 3)], material=material, alto=.3, brillo=.2, vientre=0,
               hondo=0, linea=.25)
    l.masa([ovalo(pts[2][0] + dx * h, pts[2][1] + dy * h, h * .16, h * .09) for dx, dy in ((0, 0), (-.18, .1), (.18, .06), (.1, -.08))],
           material='lejos', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.22)


# ------------------------------------------------------------------------------------------------ el nacimiento
def canguro(l, x, base, s=1.0):
    """un canguro dorado en pleno salto, de perfil, mirando a la derecha: las patas largas estiradas, la cola larga, los bracitos y las
    orejas paradas; (x, base) es el suelo bajo el medio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = [O(0, -11, 4.6, 6.4, 30), O(4.4, -17.6, 2.2, 1.9), forma(P([(5.6, -18.6), (8.4, -17.6), (8.6, -16.6), (5.8, -16.4)]), 1),
              Polygon(P([(3.4, -19), (3.6, -23.6), (4.6, -19.4)])), Polygon(P([(4.8, -19), (5.6, -23.4), (6, -18.8)])),
              tubo(P([(-3, -8), (-8.6, -5.4), (-14, -4.6), (-18, -5.4)]), [2.2 * s, 1.4 * s, .9 * s, .4 * s], 8),
              tubo(P([(-1, -7), (-3.6, -4), (-1, -2.4), (5.4, -1.6)]), [2.4 * s, 1.6 * s, 1 * s, .8 * s], 8),
              tubo(P([(2.6, -14.4), (4.6, -12.4), (5.4, -11.4)]), [.7 * s, .6 * s, .5 * s], 5)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.mancha(O(1.6, -10, 2, 3.6, 30), 'FBEFCB', .6, dentro=c)
    l.mancha(O(5.2, -18, .38, .38), '05201C', 1)
    l.mancha(O(8.2, -17.4, .35, .3), '05201C', .9)
    return c


def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 24, 4.4, 12, .5)
    nube(l, 98, 4, 12, .45)
    cordillera(l, [(-2, 16), (10, 9.4), (22, 12), (34, 6.6), (46, 10.6), (58, 14)], nieve=12)
    cordillera(l, [(54, 14), (66, 8), (78, 5.4), (90, 9), (104, 6.6), (122, 11)], nieve=11)
    # la nieve del suelo, el río recién nacido y los eucaliptos de la nieve
    nieve = l.masa(box(-2, 15.4, 122, 41.6), material='claro', alto=.1, brillo=.05, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    for _ in range(18):
        x, y = rng.uniform(0, 120), rng.uniform(17, 40)
        l.trazo([(x - 3, y), (x, y - .3), (x + 3, y)], .2, color='B6CEC6', alfa=.7)
    agua(l, cinta([(86, 16), (80, 20), (88, 25), (76, 31), (84, 36), (74, 41.6)], [1.4, 2, 2.8, 3.6, 4.4, 5.4], 8), ondas=4, semilla=2, linea=.3)
    for x, y, h in ((8, 30, 14), (18, 36, 16), (102, 30, 14), (112, 37, 17), (30, 22, 8), (96, 21, 8)):
        eucalipto(l, x, y, h, semilla=int(x))
    # el canguro dorado, protagonista, que salta en la nieve, con sus huellas
    for k in range(4):
        x0 = 22 + k * 7
        for dx in (0, 1.4):
            l.mancha(ovalo(x0 + dx, 34 + k * .6, .5, 1.1, 20), '9DB9B0', .8)
    l.mancha(ovalo(56, 37.6, 8, 1), '9DB9B0', .5, difuso=.5)
    canguro(l, 56, 33, 1.12)


# ------------------------------------------------------------------------------------------------ Albury
def ornitorrinco(l, x, y, s=1.0):
    """el ornitorrinco dorado, acostado de lado y tapado, con la cabeza en la almohada: el pico de pato oscuro y los ojitos"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, y + v * s, rx * s, ry * s, a)
    c = l.masa([O(0, 0, 4, 2.6), forma(P([(-4, -.6), (-8, -.2), (-10.4, .8), (-8, 1.8), (-4, 1.4)]), 1)], material='acento', alto=.5, brillo=.45,
               vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.masa(forma(P([(3, -1.2), (6.6, -1.4), (8.4, -.6), (8, .6), (6, 1), (3.2, 1)]), 2), material='oscuro', alto=.4, brillo=.35, vientre=0, hondo=0,
           linea=.35)                                                    # el pico
    l.mancha(O(1.6, -.8, .4, .4), '05201C', 1)
    l.trazo(P([(.4, .8), (1.4, 1.2), (2.4, .8)]), .12 * s, color='6B4E10', alfa=.8)
    return c


def albury(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.6, 10, .4)
    # las montañas, la represa de Hume, y el río que separa dos estados (la línea punteada)
    cordillera(l, [(-2, 20), (10, 12), (24, 14.6), (38, 9), (54, 15), (66, 20)], material='cuerpo')
    cordillera(l, [(60, 20), (74, 13), (90, 15.6), (104, 10), (122, 14)], material='cuerpo')
    piedra(l, box(70, 16.4, 108, 20), .1, .35)
    prado(l, 19.6, 41, .24)
    a = rio(l, 28.6)
    l.trazo([(x, 34) for x in np.arange(-2, 122, .1)][::1], .1, color='FFFFFF', alfa=0)
    for x in np.arange(-2, 122, 4):
        l.trazo([(x, 34.4), (x + 2, 34.4)], .3, color='FFFFFF', alfa=.85, dentro=a)
    casitas(l, -1, 30, 22.4, 3, semilla=2)
    casitas(l, 90, 122, 22.4, 3, semilla=3)
    # la cucheta del albergue, en la orilla, y el ornitorrinco dorado, protagonista, en la cama de arriba
    marco = [box(40, 6, 42, 30), box(78, 6, 80, 30), box(40, 15.4, 80, 16.8), box(40, 25.4, 80, 26.8), box(66, 6, 67.2, 15.6), box(68.6, 6, 69.8, 15.6)]
    for k in range(4):
        marco.append(box(66, 8 + k * 2, 69.8, 8.6 + k * 2))
    m = l.masa(marco, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(unary_union(marco).buffer(1), '8A6A3A', .55, dentro=m)
    for y in (15.4, 25.4):
        l.masa(box(42, y - 1.4, 78, y + .2), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)       # los colchones
    l.masa(ovalo(46.6, 23.6, 3.6, 1.4), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)              # la cama de abajo, vacía
    l.masa(ovalo(46.6, 13.4, 3.6, 1.4), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)              # la almohada de arriba
    ornitorrinco(l, 53, 12.2, 1.05)
    manta = forma([(55.6, 15.2), (55.4, 11), (60, 9.6), (66, 10.4), (66.4, 15.2)], 1)
    mm = l.masa(manta, material='claro', alto=.35, brillo=.25, vientre=0, hondo=0, linea=.35)
    for x in np.arange(56.6, 66, 2.2):                                   # las rayas de la manta de lana
        l.trazo([(x, 10.4), (x + .2, 15)], .5, color='2F8A74', alfa=.6, dentro=mm)
    for k, (x, y, s) in enumerate(((60, 6.6, .9), (64, 4.2, 1.2))):     # el sueño
        l.trazo([(x, y), (x + 1.4 * s, y), (x, y + 1.4 * s), (x + 1.4 * s, y + 1.4 * s)], .26 * s, color='0C3A33', alfa=.7)


# ------------------------------------------------------------------------------------------------ Echuca
def vapor_ruedas(l, x, y, s=1.0, lado=1):
    """un vapor de ruedas del Murray, de madera (no dorado: lo dorado es el eco), con su rueda al costado, las dos cubiertas, la chimenea
    y el silbato que suelta su vapor; devuelve dónde está el silbato"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    c = l.masa(forma(P([(-12, -2), (11, -2), (13, -3.2), (12, .6), (-11, .6)]), 1), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0,
               linea=.35)
    l.mancha(Polygon(P([(-13, -4), (14, -4), (14, 2), (-13, 2)])), '9A5446', .5, dentro=c)
    cub = l.masa([Polygon(P([(-10, -2), (8, -2), (8, -5.6), (-10, -5.6)])), Polygon(P([(-6, -5.6), (4, -5.6), (4, -8.6), (-6, -8.6)]))], material='claro',
                 alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    for u in np.arange(-9, 8, 1.8):
        l.trazo(P([(u, -4.6), (u, -3)]), .3 * s, color='164F46', alfa=.7, dentro=cub)
    rueda = l.masa(ovalo(x + lado * -1 * s, y - 2.4 * s, 3.6 * s, 3.6 * s), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(ovalo(x + lado * -1 * s, y - 2.4 * s, 4 * s, 4 * s), '8A6A3A', .5, dentro=rueda)
    for a in range(0, 180, 30):
        r = math.radians(a)
        l.trazo([(x + lado * (-1 + 3.4 * math.cos(r)) * s, y + (-2.4 + 3.4 * math.sin(r)) * s), (x + lado * (-1 - 3.4 * math.cos(r)) * s, y + (-2.4 - 3.4 * math.sin(r)) * s)],
                .14 * s, color='3A2A0A', alfa=.7, dentro=rueda)
    l.masa(Polygon(P([(1, -8.6), (2.4, -8.6), (2.4, -16), (1, -16)])), material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    for k in range(3):
        l.mancha(ovalo(x + lado * (2 - k * 2.4) * s, y + (-17.6 - k * 1.2) * s, (1.3 + k * .5) * s, (1 + k * .3) * s), 'FFFFFF', .7 - k * .15, difuso=.4)
    l.masa(Polygon(P([(-1.6, -8.6), (-.8, -8.6), (-.8, -11), (-1.6, -11)])), material='claro', alto=.3, brillo=.4, vientre=0, hondo=0, linea=.25)
    return (x + lado * -1.2 * s, y - 11.4 * s)


def echuca(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # el muelle de madera altísimo, de tres pisos, a la izquierda; el río y el vapor que silba
    prado(l, 14, 20, .22)
    for x in (100, 112):
        arbol(l, x, 16, 2.4, semilla=x)
    rio(l, 19)
    postes = []
    for x in np.arange(2, 40, 3.4):
        postes.append(box(x - .5, 6, x + .5, 30))
    for y in (6, 14, 22):
        postes.append(box(0, y, 41, y + 1.4))
    for x in np.arange(2, 40, 6.8):
        postes += [tubo([(x, y + 1.4), (x + 3.4, y + 8)], [.3, .3], 2) for y in (6, 14, 22)]
    m = l.masa(postes, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(postes).buffer(1), '8A6A3A', .65, dentro=m)
    sx, sy = vapor_ruedas(l, 70, 30.6, 1.15, -1)
    # el eco, protagonista: el silbido dorado que sale del vapor, rebota en el muelle y vuelve, cada vez más chico
    for k, r in enumerate((6, 10, 14, 18, 22)):
        arco = cinta([(sx - r * math.cos(t), sy - r * .7 * math.sin(t)) for t in np.linspace(-.9, .9, 16)], [1.4 - k * .16] * 16, 3)
        l.masa(arco, material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.3, contraluz=.35)
    for k, r in enumerate((4, 7, 10)):                                   # el eco que vuelve del muelle, más chico
        arco = cinta([(42 + r * math.cos(t), sy + 2 - r * .7 * math.sin(t)) for t in np.linspace(-.8, .8, 14)], [1 - k * .2] * 14, 3)
        l.masa(arco, material='acento', alto=.3, brillo=.45, vientre=0, hondo=0, linea=.25, contraluz=.3)


# ------------------------------------------------------------------------------------------------ Swan Hill
def cisne_negro(l, x, y, s=1.0, lado=1, cuac=False):
    """un cisne negro echado, de perfil: el cuerpo de barca con la cola alzada y las plumas rizadas del lomo, las puntas blancas de las
    alas, el cuello largo en S, el ojo claro y el pico dorado, grande; con un filo pálido de luna alrededor, para que no se pierda en la
    noche (chicos y sin filo, parecían culebras o caballitos de mar); con `cuac`, abre el pico y grazna: el graznido, dorado, en tres
    arcos que salen del pico (lo que no dejó dormir a Mitchell)"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    cuerpo = forma(P([(-4.8, -4.6), (-3.8, -2.2), (-2.6, -.6), (0, .1), (2.6, -.1), (3.8, -1.4), (3.4, -3.2), (1, -3.9), (-2.2, -4),
                      (-3.8, -5.2)]), 2)
    cuello = tubo(P([(2.4, -2.8), (3.8, -5.2), (2.9, -7.4), (3.5, -9.2)]), [.95 * s, .72 * s, .6 * s, .6 * s], 8)
    cabeza = ovalo(x + lado * 4.1 * s, y - 9.5 * s, .95 * s, .75 * s)
    silueta = unary_union([cuerpo, cuello, cabeza])
    l.mancha(silueta.buffer(.5 * s), '8EB5AA', .45, difuso=.3 * s)      # el filo de luna
    c = l.masa([cuerpo, cuello, cabeza], material='oscuro', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.3, contraluz=.5)
    for k in range(4):                                                   # las plumas rizadas del lomo
        u0 = -2.8 + k * 1.3
        l.trazo(P([(u0, -3.4), (u0 + .5, -4.4), (u0 + 1.1, -3.8), (u0 + .8, -3.3)]), .14 * s, color='6FA497', alfa=.8, dentro=c)
    l.mancha(Polygon(P([(-4.6, -2.6), (-2.4, -2), (-1.8, -1), (-3.6, -1.4)])), 'FFFFFF', .85, dentro=c)    # las puntas blancas
    l.mancha(ovalo(x + lado * 4.4 * s, y - 9.7 * s, .22 * s, .22 * s), 'D2F2DA', 1, dentro=c)           # el ojo
    pico = Polygon(P([(4.4, -9.8), (7.6, -9.2), (4.6, -8.6)])) if not cuac else unary_union([Polygon(P([(4.4, -9.8), (7.6, -10.9), (4.8, -9.2)])),
                                                                                           Polygon(P([(4.4, -9), (7.4, -7.8), (4.8, -8.5)]))])
    l.masa(pico, material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.22)
    if cuac:
        for k in range(3):                                               # el graznido: tres arcos dorados que se abren
            r = 1.2 + k * 1.1
            a = np.linspace(-.7, .7, 7)
            l.trazo([(x + lado * (7.4 + r * math.cos(t)) * s, y + (-9.3 + r * math.sin(t)) * s) for t in a], .28 * s, color='E8B952',
                    alfa=.95 - k * .15)


def swan_hill(l):
    rng = np.random.default_rng(5)
    # de noche: el cielo oscuro, las estrellas y la luna
    l.mancha(box(0, 0, 120, 40), '0C3A33', 1)
    l.mancha(box(0, 16, 120, 30), '245E53', .55, difuso=3)
    for _ in range(36):
        x, y = rng.uniform(0, 120), rng.uniform(0, 16)
        l.mancha(ovalo(x, y, .18, .18), 'FFFFFF', rng.uniform(.5, 1))
    l.mancha(ovalo(16, 6, 6.4, 6.4), 'FBEFCB', .2, difuso=1.6)          # la luna llena, con su halo (en cuarto, con las estrellas,
    l.mancha(ovalo(16, 6, 3.2, 3.2), 'FBEFCB', .9)                       # parecía la media luna y la estrella de una bandera)
    for dx, dy, r in ((-1, -.8, .7), (.9, .6, .5), (-.4, 1.2, .4)):
        l.mancha(ovalo(16 + dx, 6 + dy, r, r), 'D9D2B8', .6)
    # la colina, llena de cisnes negros que graznan
    colina = forma([(-2, 34), (14, 24), (34, 18), (56, 16.6), (78, 19), (98, 26), (122, 32), (122, 41.6), (-2, 41.6)], 2)
    c = l.masa(colina, material='lejos', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(colina, '0C3A33', .15, dentro=c)
    l.mancha(box(-2, 14, 122, 26), '8EB5AA', .3, dentro=c, difuso=3)     # la luz de la luna en la colina, para que se vean los cisnes
    agua(l, forma([(-2, 37), (40, 36), (80, 37.4), (122, 36), (122, 41.6), (-2, 41.6)], 2), linea=.3)
    puestos = [(30, 22.6, .7), (41, 19.6, .72), (53, 17.8, .72), (66, 18.2, .72), (79, 20.6, .7),                     # en la cresta
               (22, 28.6, 1.02), (45, 25.6, 1.08), (69, 26, 1.08), (90, 29.4, 1),                                       # en la ladera
               (33, 35.6, 1.45), (60, 34.4, 1.55), (86, 36.4, 1.4)]                                                     # adelante, grandes
    for k, (x, y, e) in enumerate(puestos):
        cisne_negro(l, x, y, e, 1 if k % 2 else -1, cuac=k % 3 != 1)
    # la carpa de lona de Mitchell, con la luz de su farol adentro (clara: lo dorado son los graznidos), vista de frente y de costado,
    # con su palo y sus vientos (un triángulo solo, con la cabeza de Mitchell adentro, parecía un ojo en una pirámide)
    l.mancha(ovalo(106, 18, 11, 6), 'FBEFCB', .18, difuso=2)
    for a, b in (((102.4, 13.2), (96.2, 22.8)), ((112.6, 12), (119.4, 21.6))):      # los vientos
        l.trazo([a, b], .1, color='D2F2DA', alfa=.7)
    costado = Polygon([(102.4, 13.4), (112.6, 12.2), (117.4, 21.2), (107.2, 22.4)])
    c = l.masa(costado, material='claro', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(costado, '8EB5AA', .45, dentro=c)
    frente = Polygon([(97.6, 22.4), (102.4, 13.4), (107.2, 22.4)])
    f = l.masa(frente, material='claro', alto=.25, brillo=.35, vientre=0, hondo=0, linea=.35)
    l.mancha(frente, 'FBEFCB', .4, dentro=f)
    l.mancha(Polygon([(100.4, 22.4), (102.4, 16.8), (104.4, 22.4)]), 'FFF6DE', .95, dentro=f)       # la puerta abierta, con la luz
    l.trazo([(102.4, 16.8), (102.4, 22.4)], .12, color='8EB5AA', alfa=.7, dentro=f)
    l.trazo([(102.4, 13.6), (102.4, 11.8)], .2, alfa=.9)                                            # la punta del palo


# ------------------------------------------------------------------------------------------------ Mildura
def mildura(l):
    rng = np.random.default_rng(6)
    cielo(l, sol=None, tarde=.25)
    # la naranja gigante, dorada, protagonista, que hace de sol
    l.mancha(ovalo(60, 11, 14, 11), 'F2D48A', .35, difuso=3)
    n = l.masa(ovalo(60, 11, 8.6, 8.2), material='acento', alto=.6, brillo=.55, vientre=0, hondo=0, linea=.45, contraluz=.45)
    for _ in range(50):                                                  # los poros de la cáscara
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 7.6)
        l.mancha(ovalo(60 + r * math.cos(a), 11 + r * math.sin(a), .22, .22), '6B4E10', .35, dentro=n)
    l.trazo([(55, 7.6), (54.4, 10.4)], [.05, .5, .05], color='FBEFCB', alfa=.85, dentro=n)
    l.masa([tubo([(60, 3), (60.4, 1.4)], [.4, .3], 3), ovalo(63, 1.8, 3, 1.2, -15)], material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    # el desierto verde: la tierra roja con las hileras de naranjos y viñas regadas por los canales, hasta el horizonte
    tierra(l, 20, 41, desierto=.4)
    l.mancha(box(-2, 20, 122, 41.6), ROJA, .35)
    for k in range(9):                                                   # las hileras, en perspectiva hacia el horizonte
        x0 = -40 + k * 25
        for t in np.linspace(.02, 1, 14):
            x = 60 + (x0 - 60) * t
            y = 20.4 + 21 * t
            r = .6 + 1.8 * t
            l.masa(ovalo(x, y - r * .6, r, r * .8), material='cuerpo', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.15 + .15 * t, arroja=False)
    for k in range(4):                                                   # los canales
        x0 = -16 + k * 50
        l.trazo([(60, 20.6), (x0, 41.6)], .4, color='64C8AA', alfa=.8)
    for x0, w, h in ((-6, 30, 3), (90, 34, 3.6)):                         # las dunas, lejos
        l.mancha(ovalo(x0 + w / 2, 20.6, w / 2, h), 'BF9129', .4, difuso=1)


# ------------------------------------------------------------------------------------------------ Renmark
def marinero(l, x, base, s=1.0):
    """un marinero de perfil, mirando a la derecha, con la camiseta a rayas y la gorra, que estira el brazo para poner una etiqueta"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    l.masa([tubo(P([(-.8, -8), (-1.2, -4), (-1.4, -.4)]), [1.1 * s, 1 * s, .9 * s], 5), tubo(P([(.8, -8), (1.2, -4), (1.6, -.4)]), [1.1 * s, 1 * s, .9 * s], 5),
            O(-1.2, -.2, 1.2, .5), O(2, -.2, 1.2, .5)], material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    c = l.masa(forma(P([(-2.4, -15.4), (2.4, -15.4), (2.8, -12), (2.4, -7.6), (-2.4, -7.6), (-2.8, -12)]), 1), material='claro', alto=.35, brillo=.25,
               vientre=0, hondo=0, linea=.35)
    for v in np.arange(-14.6, -8, 1.4):                                  # las rayas de la camiseta
        l.trazo(P([(-2.8, v), (2.8, v)]), .5 * s, color='164F46', alfa=.8, dentro=c)
    piel(l, [O(.6, -17.8, 2, 2.2), tubo(P([(1.8, -14.4), (5, -15.6), (8, -17.4)]), [.7 * s, .6 * s, .55 * s], 5)])
    l.masa([forma(P([(-1.6, -19.2), (-1.4, -20.6), (1, -21), (2.6, -20.2), (2.6, -19.2)]), 1), O(3, -19.4, 1.4, .4)], material='oscuro', alto=.3, brillo=.3,
           vientre=0, hondo=0, linea=.25)                                # la gorra
    l.mancha(O(1.6, -18, .26, .3), '05201C', 1)


def renmark(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # el río con un barco-casa, y los viñedos de la Riverland en hileras
    prado(l, 15, 41, .3)
    rio(l, 16.4)
    prado(l, 21, 41, .3)
    l.masa([forma([(84, 19.8), (104, 19.8), (105.4, 18.4), (83.4, 18.4)], 1), box(86, 16, 100, 18.5)], material='claro', alto=.2, brillo=.15, vientre=0,
           hondo=0, linea=.25)
    for y in np.arange(22.6, 30, 2.2):
        l.trazo([(-2, y), (122, y)], .7, color='2F8A74', alfa=.75)
    # la parra en su emparrado, con el racimo de uvas doradas, protagonista, y las etiquetas; el marinero que las renombra
    em = l.masa([box(36, 14, 37.4, 38), box(84, 14, 85.4, 38), box(34, 13.4, 88, 15)], material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0,
                linea=.3)
    l.mancha(box(33, 12, 89, 39), '5A3E1E', .55, dentro=em)
    for x in np.arange(38, 84, 4.6):                                     # las hojas de la parra
        l.masa(ovalo(x + rng.uniform(-1, 1), 16 + rng.uniform(-.6, .6), 2.6, 1.8), material='cuerpo', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.25)
    uvas = []
    for fila, (n, y) in enumerate(((7, 18.4), (6, 20.6), (5, 22.8), (4, 25), (3, 27.2), (2, 29.4), (1, 31.6))):
        for k in range(n):
            uvas.append((60 - (n - 1) * 1.15 + k * 2.3, y))
    for x, y in uvas:
        l.masa(ovalo(x, y, 1.2, 1.15), material='acento', alto=.6, brillo=.55, vientre=0, hondo=0, linea=.25, contraluz=.4)
    for (x, y) in uvas[::3]:                                             # las etiquetas con su nombre
        l.trazo([(x, y), (x + .8, y + 1.4)], .08, color='0C3A33', alfa=.8)
        l.masa(box(x + .4, y + 1.4, x + 2.4, y + 2.4), material='claro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.15)
        l.trazo([(x + .7, y + 1.9), (x + 2.1, y + 1.9)], .08, color='0C3A33', alfa=.7)
    marinero(l, 44, 39, 1.2)


# ------------------------------------------------------------------------------------------------ Murray Bridge
def murray_bridge(l):
    cielo(l, sol=None)
    nube(l, 26, 4, 12, .45)
    nube(l, 100, 3.6, 10, .4)
    prado(l, 18, 22, .24)
    casitas(l, -1, 122, 19.6, 3, semilla=8)
    a = rio(l, 22)
    # el puente de hierro dorado, protagonista: las cerchas, y las pilas que terminan en pies que le hacen cosquillas al agua
    tablero = box(-2, 15, 122, 16.6)
    cerchas = []
    for x0 in np.arange(-2, 122, 24):
        cerchas.append(cinta([(x0 + 24 * t, 15 - 5 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 13)], [.7] * 13, 3))
    m = l.masa([tablero] + cerchas, material='acento', alto=.35, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for x0 in np.arange(-2, 122, 24):
        for t in np.linspace(.1, .9, 8):
            x = x0 + 24 * t
            l.trazo([(x, 15 - 5 * math.sin(math.pi * t)), (x, 15)], .14, color='BF9129', alfa=.9)
    for x in np.arange(22, 122, 24):                                     # las pilas, con sus pies descalzos que se meten al agua
        l.masa([box(x - 1.6, 16.4, x + 1.6, 28), ovalo(x + 1.6, 28.4, 3, 1.3), ovalo(x + 4.4, 27.8, .7, .6), ovalo(x + 4.6, 28.8, .6, .5)],
               material='acento', alto=.4, brillo=.4, vientre=0, hondo=0, linea=.35, contraluz=.3)
        for k in range(3):                                               # el agua que se ríe con las cosquillas
            l.trazo([(x + 2 + (2.6 + k * 1.4) * math.cos(t), 29.4 + (.8 + k * .4) * math.sin(t)) for t in np.linspace(0, math.pi, 10)], .16,
                    color='FFFFFF', alfa=.8 - k * .2)
    # el tren que pasa por arriba
    for k in range(4):
        l.masa(box(30 + k * 7, 11.4, 36.4 + k * 7, 14.8), material='lejos' if k else 'oscuro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # la cara del río, que se ríe, abajo
    l.trazo([(46, 34), (60, 37.6), (74, 34)], .5, color='FFFFFF', alfa=.85, dentro=a)
    for dx in (-8, 8):
        l.trazo([(60 + dx - 1.4, 31), (60 + dx, 30.2), (60 + dx + 1.4, 31)], .4, color='FFFFFF', alfa=.85, dentro=a)


# ------------------------------------------------------------------------------------------------ Goolwa
def gaviota(l, x, y, s=1.0):
    """una gaviota que empuja con las alas abiertas, de perfil, mirando a la derecha: el cuerpo blanco, las alas grises de punta negra,
    el pico y las patas amarillas"""
    P = lambda pts: [(x + u * s, y + v * s) for u, v in pts]
    l.masa([forma(P([(-1, -3), (-5, -9), (-9.6, -11.4), (-8, -8), (-4, -2.6)]), 2), forma(P([(1, -3), (2.6, -9.6), (5.6, -12.4), (5, -8.4), (3, -2.6)]), 2)],
           material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(Polygon(P([(-9.6, -11.4), (-7.4, -11), (-8, -8.6)])), '0C3A33', .9)
    l.mancha(Polygon(P([(5.6, -12.4), (4.6, -11.6), (5.2, -10)])), '0C3A33', .9)
    l.masa([ovalo(x, y - 2 * s, 4 * s, 2 * s), ovalo(x + 3.8 * s, y - 4 * s, 1.6 * s, 1.4 * s)], material='claro', alto=.45, brillo=.3, vientre=0, hondo=0,
           linea=.35)
    l.masa(Polygon(P([(5.2, -4.4), (7.8, -3.8), (5.4, -3.4)])), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    l.mancha(Polygon(P([(5.2, -4.4), (7.8, -3.8), (5.4, -3.4)])), 'E8DDBE', .9)
    l.mancha(ovalo(x + 4.2 * s, y - 4.4 * s, .3 * s, .3 * s), '05201C', 1)


def goolwa(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .45)
    # a la izquierda, el lago dulce; a la derecha, el mar salado, con más olas; y la barrera de compuertas en medio
    agua(l, box(-2, 16, 122, 41.6), ondas=0, linea=0)
    l.mancha(box(-2, 16, 60, 41.6), '64C8AA', .25)
    rng = np.random.default_rng(9)
    for _ in range(18):
        x, y = rng.uniform(64, 120), rng.uniform(18, 40)
        l.trazo([(x, y), (x + 1.5, y - .4), (x + 3, y)], .2, color='D2F2DA', alfa=.85)
    prado(l, 14, 16.6, .3)
    fr = l.masa([forma([(108.4, 15), (108.8, 6.4), (111, 6.4), (111.4, 15)], 0), box(108, 5.2, 111.8, 6.6)], material='claro', alto=.3, brillo=.2,
                vientre=0, hondo=0, linea=.3)
    l.mancha(box(107, 9, 113, 10.6), '2F8A74', .85, dentro=fr)
    # las compuertas doradas, protagonistas, una al lado de la otra, y la gaviota que empuja la última para cerrarla
    l.masa(box(-2, 14, 122, 16.4), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)          # la pasarela de la barrera
    for k, x in enumerate(np.arange(30, 90, 8)):
        abierta = x > 80
        g = Polygon([(x, 16.4), (x + 7, 16.4), (x + 7, 36), (x, 36)]) if not abierta else Polygon([(x, 16.4), (x + 2.4, 17.6), (x + 2.4, 37.2), (x, 36)])
        m = l.masa(g, material='acento', alto=.35, brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
        for y in (21, 26, 31):
            l.trazo([(x, y), (x + (7 if not abierta else 2.4), y + (0 if not abierta else .8))], .18, color='6B4E10', alfa=.6, dentro=m)
    gaviota(l, 92, 30, 1.25)


# ------------------------------------------------------------------------------------------------ el mar
def pelicano(l, x, y, s=1.0, lado=1):
    """un pelícano australiano, blanco con las alas negras, parado en la arena: el pico largo y claro con su bolsa"""
    P = lambda pts: [(x + lado * u * s, y + v * s) for u, v in pts]
    l.masa([tubo(P([(-.6, 0), (-.7, -2.4)]), [.25 * s, .2 * s], 3), tubo(P([(.6, 0), (.5, -2.4)]), [.25 * s, .2 * s], 3)], material='oscuro', alto=.2,
           brillo=.2, vientre=0, hondo=0, linea=.15)
    c = l.masa([ovalo(x, y - 4 * s, 3 * s, 2 * s), tubo(P([(1.6, -5), (2.4, -7.4), (1.8, -9)]), [.9 * s, .7 * s, .7 * s], 6), ovalo(x + lado * 2 * s, y - 9.4 * s, .9 * s, .8 * s)],
               material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(x - lado * 1 * s, y - 4.4 * s, 2.4 * s, 1.2 * s), '0C3A33', .85, dentro=c)
    l.masa(forma(P([(2.6, -9.8), (7.6, -8), (7.4, -7.2), (4, -6.6), (2.6, -8.6)]), 1), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.2)
    l.mancha(forma(P([(3, -8.6), (7, -7.6), (4, -6.8)]), 1), 'E8DDBE', .9)


def mar(l):
    rng = np.random.default_rng(11)
    cielo(l, sol=None)
    nube(l, 30, 5, 16, .5)
    nube(l, 96, 4, 12, .45)
    # el océano Austral, con sus olas, al fondo; las dunas de la costa y la boca angosta del río entre ellas
    horizonte = 15
    m = l.masa(box(-2, horizonte, 122, 25), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    for _ in range(20):
        x, y = rng.uniform(-2, 118), rng.uniform(horizonte + 1, 24)
        l.trazo([(x, y), (x + 1.6, y - .4), (x + 3.2, y)], .2, color='D2F2DA', alfa=.85)
    for g in (forma([(-2, 41.6), (-2, 23), (20, 22), (40, 23.4), (52, 26), (50, 41.6)], 2), forma([(70, 41.6), (68, 26), (80, 23.4), (100, 22), (122, 23),
                                                                                                     (122, 41.6)], 2)):
        orilla(l, g, tinte=.45)
    for x, y in ((8, 26), (30, 26.4), (96, 26.4), (112, 26)):
        pasto(l, x - 4, x + 4, y, y + 2, 4, semilla=x)
    boca = forma([(52, 25), (68, 25), (66, 30), (62, 41.6), (54, 41.6), (54, 30)], 2)
    agua(l, boca, ondas=4, semilla=12, linea=.35)
    # la draga dorada, protagonista, en la boca, con su caño que tira la arena hacia la duna
    d = l.masa([forma([(46, 34.6), (66, 34.6), (68, 32.4), (45, 32.6)], 1), box(50, 28.6, 58, 32.8), box(52.6, 26, 54, 28.8)], material='acento', alto=.4,
               brillo=.45, vientre=0, hondo=0, linea=.4, contraluz=.35)
    l.mancha(box(51, 29.6, 57, 31), '6B4E10', .6, dentro=d)
    cano = tubo([(58, 30), (68, 27), (78, 25.6), (86, 26)], [.8, .7, .7, .7], 6)
    l.masa(cano, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35)
    for k in range(9):                                                   # la arena que sale del caño
        l.mancha(ovalo(87 + k * .9, 26.4 + (k % 3) * .5 - k * .2, .6 + k * .1, .4), 'D8C49A', .9)
    l.trazo([(46, 34), (30, 36), (14, 39)], .2, color='0C3A33', alfa=.5)  # el ancla
    # los pelícanos en la arena
    for x, y, lado in ((20, 34, 1), (28, 36.4, -1), (96, 34.6, -1), (106, 37, 1)):
        pelicano(l, x, y, 1, lado)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Albury', dibujar=albury), dict(clave='Echuca', dibujar=echuca),
            dict(clave='Swan Hill', dibujar=swan_hill), dict(clave='Mildura', dibujar=mildura), dict(clave='Renmark', dibujar=renmark),
            dict(clave='Murray Bridge', dibujar=murray_bridge), dict(clave='Goolwa', dibujar=goolwa), dict(clave='mar', dibujar=mar)]
LISTO = True
