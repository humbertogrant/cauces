# -*- coding: utf-8 -*-
"""Las postales del Paraná, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el sol de mayo de la bandera de Rosario.

- el nacimiento: la confluencia del Paranaíba y el Grande, vista desde arriba, entre represas y campos: una suma dorada, + entre los
  dos ríos y = sobre el que forman, el Paraná;
- Foz do Iguaçu: «un muro de agua y un muro de concreto lado a lado»: las cataratas del Iguazú, con su garganta y su bruma, y la
  represa de Itaipú, con sus contrafuertes y su vertedero; un arcoíris dorado va de un muro al otro;
- Encarnación: «una misión de piedra roja frente a una represa»: las ruinas de la iglesia jesuítica de Trinidad, de piedra roja, con su
  campanario y la campana dorada; enfrente, la represa de Yacyretá;
- Corrientes: «un acordeón de chamamé donde dos corrientes se juntan»: un acordeón dorado, con el fuelle abierto, donde el río Paraguay
  entra al Paraná; atrás, el puente de tirantes;
- Rosario: «la bandera argentina izada sobre silos de soya»: la bandera celeste y blanca con su sol dorado, en lo alto de los silos del
  puerto, con las grúas y un barco cargando;
- Buenos Aires: «un río color de león, de 220 km de ancho»: el Río de la Plata, leonado hasta el horizonte, con un león dorado echado
  en él; a la izquierda, el Obelisco y los edificios;
- Montevideo: «monte vide eu»: el vigía, en la cofa del palo mayor, ve el Cerro con su catalejo dorado; enfrente, el Cerro con su
  fortaleza y su faro;
- el mar: el Río de la Plata sale al Atlántico: el agua marrón contra la verde del mar, y un cofre de plata, de herrajes dorados, que
  flota en la boca; cargueros, un faro y gaviotas (el lanchón no llega al mar: lo hacen los cargueros).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (CIELO, VISTA, agua, arbol, ave, casitas, cielo, cinta, nube, orilla, palmera, pasto, piedra, prado, reflejo, rio,  # noqa: F401
                     selva, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
ROJA = '9A5446'            # la piedra roja de las misiones
CELESTE = '8CC4E8'         # el celeste de la bandera argentina
LEONADO = 'BF9129'         # el agua color de león del Río de la Plata
MARRON = '8A6A3A'          # el agua marrón del estuario


def piel(l, piezas, tono=.45):
    """piezas de piel: el pálido de `vientre` teñido de dorado oscuro"""
    m = l.masa(piezas, material='vientre', alto=.4, brillo=.15, vientre=0, hondo=0, linea=.35, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), PIEL, tono, dentro=m)
    return m


def arenisca(l, piezas, color, tono=.5, linea=.35):
    """piedra de un color: el pálido de `vientre` teñido"""
    m = l.masa(piezas, material='vientre', alto=.25, brillo=.1, vientre=0, hondo=0, linea=linea, escalon=.2, contraluz=.25)
    l.mancha(unary_union(piezas).buffer(1), color, tono, dentro=m)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    rng = np.random.default_rng(1)
    cielo(l, sol=None)
    nube(l, 30, 3, 12, .45)
    # visto desde arriba: los campos en franjas, el Paranaíba que llega por la izquierda y el Grande por la derecha
    tierra(l, 6, 41, desierto=.3)
    for k in range(9):                                                   # los campos de soya, en franjas
        x0 = -2 + k * 14
        l.mancha(Polygon([(x0, 6), (x0 + 13, 6), (x0 + 10, 41.6), (x0 - 3, 41.6)]), ('2F8A74', '9BDDBD', 'BF9129')[k % 3], .18)
    paranaiba = cinta([(-2, 9), (18, 11), (36, 15), (50, 19.6), (57, 22.4)], [5, 5.4, 6, 6.4, 6.8], 8)
    grande = cinta([(122, 9), (102, 11), (84, 15), (70, 19.6), (63, 22.4)], [5, 5.4, 6, 6.4, 6.8], 8)
    parana = cinta([(60, 21), (60, 30), (60.6, 41.6)], [11, 12, 13], 6)
    agua(l, unary_union([paranaiba, grande, parana]).buffer(.3).buffer(-.3), ondas=12, semilla=2, linea=.35)
    for x0, x1, y in ((20, 32, 12.4), (88, 100, 12.4)):                  # las represas, que cruzan cada río
        piedra(l, box(x0, y - 1.6, x1, y + 1.6), .15, .35)
        for x in np.arange(x0 + 1, x1 - .6, 2):
            l.trazo([(x, y + 1.6), (x, y + 3)], .6, color='FFFFFF', alfa=.7)
    for _ in range(18):
        x, y = rng.uniform(0, 120), rng.uniform(26, 40)
        if 44 < x < 76:
            continue
        arbol(l, x, y, 1.4, semilla=int(x * 3))
    # la suma dorada, protagonista: el más entre los dos ríos y el igual sobre el Paraná
    mas = unary_union([box(55.4, 9.6, 64.6, 12.6), box(58.5, 6.5, 61.5, 15.7)])
    igual = unary_union([box(54.4, 25, 65.6, 27.6), box(54.4, 29.6, 65.6, 32.2)])
    for g in (mas, igual):
        l.mancha(affinity.translate(g, .8, .8), '0C3A33', .3, difuso=.4)
        l.masa(g.buffer(.3), material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)


# ------------------------------------------------------------------------------------------------ Foz do Iguaçu
def foz(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 60, 4, 14, .45)
    # a la izquierda, las cataratas: el borde de la garganta en arco, con la selva arriba, las cortinas de agua y la bruma
    selva(l, -2, 54, 15, 6, semilla=4, emergentes=3)
    borde = forma([(-2, 15), (10, 14.6), (24, 15.6), (38, 15), (54, 15.6), (54, 31), (-2, 31)], 1)
    l.masa(borde, material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    for x in np.arange(0, 54, 1.4):                                      # las cortinas de agua
        y0 = 15.4 + .4 * math.sin(x)
        l.trazo([(x, y0), (x + .3, y0 + 7), (x - .2, 30)], [1, 1.2, .6], color='FFFFFF', alfa=.88)
    l.mancha(ovalo(26, 30, 30, 4), 'FFFFFF', .7, difuso=1.4)            # la bruma
    # a la derecha, la represa de Itaipú: el muro de concreto con sus contrafuertes y el vertedero
    muro = Polygon([(64, 12), (122, 12), (122, 31), (64, 31)])
    m = piedra(l, muro, .08, .4)
    for x in np.arange(66, 122, 4.8):                                    # los contrafuertes
        l.mancha(box(x, 12, x + 2.2, 31), '0C3A33', .18, dentro=m)
        l.trazo([(x, 12), (x, 31)], .14, color='6B7E7B', alfa=.6, dentro=m)
    for x in np.arange(66.6, 80, 2.4):                                   # el vertedero, con su agua blanca
        l.trazo([(x, 13), (x + .2, 22), (x - .1, 31)], [.8, 1, .5], color='FFFFFF', alfa=.85)
    l.masa(box(64, 10.6, 122, 12.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)
    # el río abajo, compartido, y el arcoíris dorado, protagonista, que va de un muro al otro
    agua(l, box(-2, 30.6, 122, 41.6), ondas=12, semilla=5, linea=0)
    l.mancha(box(-2, 30, 122, 33.6), 'FFFFFF', .45, difuso=1.4)
    for k, (color, alfa) in enumerate((('9BDDBD', .6), ('FBEFCB', .8))):
        r = 44 - k * 2.2
        l.trazo([(60 + r * math.cos(t), 33 - r * .62 * math.sin(t)) for t in np.linspace(.05, math.pi - .05, 40)], 1, color=color, alfa=alfa)
    arco = cinta([(60 + 41.8 * math.cos(t), 33 - 41.8 * .62 * math.sin(t)) for t in np.linspace(.05, math.pi - .05, 40)], [1.6] * 40, 3)
    l.masa(arco, material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.25, contraluz=.4)


# ------------------------------------------------------------------------------------------------ Encarnación
def encarnacion(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 100, 3.4, 10, .4)
    # enfrente, la represa de Yacyretá, larga y baja, sobre el río ancho
    prado(l, 15, 19, .2)
    y = piedra(l, box(56, 12.6, 122, 17), .1, .35)
    for x in np.arange(58, 122, 3):
        l.mancha(box(x, 13.6, x + 1.4, 17), '0C3A33', .45, dentro=y)
    rio(l, 17.6)
    # la orilla de acá, con el pasto, y las ruinas de piedra roja de la misión de Trinidad, protagonistas
    m = orilla(l, forma([(-2, 41.5), (-2, 24.6), (30, 23.6), (60, 23.4), (90, 23.6), (122, 24.6), (122, 41.5)], 2), tinte=.24)
    pasto(l, 0, 120, 26, 40.6, 22, semilla=6, dentro=m)
    muros = [box(24, 18, 96, 34)]
    for x in np.arange(29, 92, 9):                                       # los arcos de la nave, abiertos al cielo
        muros[0] = muros[0].difference(forma([(x, 34.4), (x, 25), (x + 3.4, 21.4), (x + 6.8, 25), (x + 6.8, 34.4)], 2))
    fachada = box(52, 10, 68, 34).difference(forma([(57, 34.4), (57, 25), (60, 21.6), (63, 25), (63, 34.4)], 2))
    piezas = muros + [fachada, Polygon([(51, 10.4), (60, 5.4), (69, 10.4)])]
    r = arenisca(l, piezas, ROJA, .6, .4)
    for y in np.arange(19.4, 34, 1.4):                                   # las hiladas de piedra
        l.trazo([(24, y), (96, y)], .08, color='5A3E1E', alfa=.35, dentro=r)
    for x in np.arange(53, 68, 1.8):                                     # el friso
        l.mancha(ovalo(x + .9, 12.8, .6, .9), '5A3E1E', .45, dentro=r)
    # el campanario, a la derecha, de piedra roja, con la campana dorada
    t = arenisca(l, [box(100, 6.4, 110, 34), Polygon([(99, 6.8), (105, 2.4), (111, 6.8)])], ROJA, .6, .4)
    l.mancha(forma([(102.4, 16.4), (102.4, 10.6), (105, 8.6), (107.6, 10.6), (107.6, 16.4)], 2), '0C3A33', .8, dentro=t)
    l.masa([forma([(102.8, 15.6), (103.4, 12.4), (105, 11.2), (106.6, 12.4), (107.2, 15.6)], 1), ovalo(105, 16, .6, .6)], material='acento', alto=.5,
           brillo=.55, vientre=0, hondo=0, linea=.35, contraluz=.4)
    l.trazo([(105, 9.2), (105, 11.4)], .14, color='0C3A33', alfa=.8)


# ------------------------------------------------------------------------------------------------ Corrientes
def acordeon(l, x, y, ancho, alto_):
    """un acordeón dorado de frente, con el fuelle abierto en pliegues, la caja de los teclados a la derecha (las teclas blancas y negras)
    y la de los bajos a la izquierda, con sus botones; (x, y) es el centro"""
    caja = ancho * .2
    izq = box(x - ancho / 2, y - alto_ / 2, x - ancho / 2 + caja, y + alto_ / 2).buffer(.6)
    der = box(x + ancho / 2 - caja, y - alto_ / 2, x + ancho / 2, y + alto_ / 2).buffer(.6)
    fuelle = box(x - ancho / 2 + caja, y - alto_ * .42, x + ancho / 2 - caja, y + alto_ * .42)
    f = l.masa(fuelle, material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.3)
    n = 10
    for k in range(n + 1):                                               # los pliegues del fuelle, en zigzag
        xx = x - ancho / 2 + caja + (ancho - 2 * caja) * k / n
        l.trazo([(xx, y - alto_ * .42), (xx, y + alto_ * .42)], .3 if k % 2 else .16, color='6B4E10', alfa=.75 if k % 2 else .45, dentro=f)
    for v in (-.3, 0, .3):
        l.trazo([(x - ancho / 2 + caja, y + alto_ * v), (x + ancho / 2 - caja, y + alto_ * v)], .1, color='FBEFCB', alfa=.5, dentro=f)
    m = l.masa([izq, der], material='acento', alto=.45, brillo=.5, vientre=0, hondo=0, linea=.45, contraluz=.4)
    for k in range(7):                                                   # las teclas, a la derecha
        ty = y - alto_ / 2 + 1 + k * (alto_ - 2) / 7
        l.mancha(box(x + ancho / 2 - caja + .8, ty, x + ancho / 2 - .6, ty + (alto_ - 2) / 7 - .3), 'FFFFFF', .95, dentro=m)
        if k % 7 not in (2, 6):
            l.mancha(box(x + ancho / 2 - caja + .8, ty + (alto_ - 2) / 7 - .7, x + ancho / 2 - caja * .45, ty + (alto_ - 2) / 7 + .2), '05201C', .95, dentro=m)
    for i in range(3):                                                   # los botones de los bajos, a la izquierda
        for j in range(6):
            l.mancha(ovalo(x - ancho / 2 + 1.6 + i * 1.9, y - alto_ / 2 + 1.8 + j * (alto_ - 3) / 5.4, .55, .55), 'FBEFCB', .95, dentro=m)
    for lado in (-1, 1):                                                 # las correas
        l.trazo([(x + lado * (ancho / 2 - caja * .5), y - alto_ / 2 - .4), (x + lado * (ancho / 2 - caja * .5), y - alto_ / 2 - 2.4)], .4,
                color='5A3E1E', alfa=.85)
    return unary_union([izq, der, fuelle])


def nota(l, x, y, s=1.0):
    l.masa([ovalo(x, y, 1 * s, .75 * s, -20), box(x + .75 * s, y - 5 * s, x + 1.1 * s, y),
            tubo([(x + 1, y - 5 * s), (x + 2.6 * s, y - 3.4 * s), (x + 2.4 * s, y - 1.6 * s)], [.4 * s, .3 * s, .1 * s], 5)], material='oscuro',
           alto=.2, brillo=.3, vientre=0, hondo=0, linea=.2)


def corrientes(l):
    cielo(l, sol=None)
    nube(l, 22, 4, 12, .5)
    nube(l, 98, 3.6, 12, .45)
    # atrás, el puente General Belgrano, de dos torres y tirantes, y la ciudad
    prado(l, 15, 19, .2)
    casitas(l, -1, 122, 16.6, 3, semilla=7)
    l.masa(box(-2, 13.4, 122, 14.4), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    for x in (34, 86):
        l.masa(box(x - .8, 2.6, x + .8, 18), material='claro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.25)
        for k in range(7):
            l.trazo([(x, 3.4 + k * 1.3), (x - 14 + k * 1.8, 13.6)], .06, color='8EB5AA', alfa=.9)
            l.trazo([(x, 3.4 + k * 1.3), (x + 14 - k * 1.8, 13.6)], .06, color='8EB5AA', alfa=.9)
    # las dos corrientes que se juntan: el Paraguay, más oscuro, que llega por la izquierda, y el Paraná, por la derecha
    agua(l, box(-2, 17.6, 122, 41.6), ondas=0, semilla=8, linea=0)
    l.mancha(Polygon([(-2, 17.6), (60, 17.6), (60, 41.6), (-2, 41.6)]), '164F46', .35, difuso=3)
    for lado in (-1, 1):                                                 # las corrientes, que entran a los dos lados del acordeón
        for k in range(5):
            y = 21 + k * 3.8
            x0 = 60 + lado * 62
            l.trazo([(x0, y), (60 + lado * 40, y + .6), (60 + lado * 24, y)], .3, color='D2F2DA', alfa=.75)
            l.trazo([(60 + lado * 25, y), (60 + lado * 27, y - .6)], .3, color='D2F2DA', alfa=.75)
    # el acordeón dorado, protagonista, donde se juntan
    g = acordeon(l, 60, 27.4, 44, 17)
    reflejo(l, g, 36.2, .2)
    for x, y in ((24, 12), (94, 9.6), (100, 22)):
        nota(l, x, y, .9)


# ------------------------------------------------------------------------------------------------ Rosario
def sol_de_mayo(l, x, y, r):
    """el sol de mayo de la bandera: el disco dorado con su cara y sus rayos, rectos y ondulados"""
    rayos = []
    for k in range(16):
        a = math.radians(k * 22.5)
        d = np.array([math.cos(a), math.sin(a)])
        e = np.array([-d[1], d[0]])
        b = np.array([x, y])
        if k % 2 == 0:
            rayos.append(Polygon([tuple(b + d * r * .9 + e * r * .14), tuple(b + d * r * 1.75), tuple(b + d * r * .9 - e * r * .14)]))
        else:
            pts = [tuple(b + d * r * (0.9 + .85 * t) + e * r * .1 * math.sin(t * 9)) for t in np.linspace(0, 1, 8)]
            rayos.append(tubo(pts, [r * .1] * 7 + [r * .02], 4))
    m = l.masa(rayos + [ovalo(x, y, r, r)], material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.25, contraluz=.4)
    for dx in (-.35, .35):
        l.mancha(ovalo(x + dx * r, y - .15 * r, .1 * r, .1 * r), '6B4E10', .9, dentro=m)
    l.trazo([(x - .3 * r, y + .35 * r), (x, y + .45 * r), (x + .3 * r, y + .35 * r)], .1 * r, color='6B4E10', alfa=.8, dentro=m)
    return m


def rosario(l):
    cielo(l, sol=None)
    nube(l, 20, 4.6, 12, .45)
    nube(l, 104, 4, 10, .4)
    # a la izquierda, lejos, el Monumento a la Bandera; los silos de soya del puerto, al medio
    prado(l, 22, 26, .22)
    l.masa([box(4, 14.4, 22, 23), box(9.6, 4, 12.6, 14.6)], material='claro', alto=.25, brillo=.15, vientre=0, hondo=0, linea=.3)
    silos = []
    for x in np.arange(36, 90, 7.2):
        silos += [box(x - 3.2, 14.6, x + 3.2, 25.6), Polygon([(x - 3.2, 14.8), (x, 12.6), (x + 3.2, 14.8)])]
    s = l.masa(silos, material='claro', alto=.4, brillo=.25, vientre=0, hondo=0, linea=.35, escalon=.2, contraluz=.3)
    for x in np.arange(36, 90, 7.2):
        for y in np.arange(16, 25.4, 1.6):
            l.trazo([(x - 3, y), (x + 3, y + .1)], .08, color='8EB5AA', alfa=.6, dentro=s)
    l.masa(box(30, 9.4, 96, 12.6), material='claro', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)    # la galería de cintas, arriba
    for x, h in ((100, 13), (110, 11)):                                  # las grúas
        l.masa([box(x - .4, 25.6 - h, x + .4, 25.8), Polygon([(x, 25.6 - h), (x - 7, 25.6 - h - .8), (x - 7, 25.6 - h - .2), (x, 25.6 - h + .6)])],
               material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    rio(l, 26)
    l.masa([forma([(64, 33), (100, 33), (102.6, 30.6), (63, 30.8)], 1), box(92, 26.8, 99, 30.9), box(94.6, 24.6, 96, 26.9)], material='lejos', alto=.2,
           brillo=.15, vientre=0, hondo=0, linea=.3)                    # el barco que carga
    # la bandera argentina, izada sobre los silos, protagonista: celeste, blanca, celeste, y el sol de mayo dorado
    l.masa(box(61.6, -1, 62.6, 13), material='claro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)
    ola = lambda t: .9 * math.sin(t * math.pi * 1.5)
    franja = lambda f0, f1: Polygon([(62.6 + 26 * t, .6 + 13.2 * f0 + ola(t)) for t in np.linspace(0, 1, 14)] +
                                    [(62.6 + 26 * t, .6 + 13.2 * f1 + ola(t + .1)) for t in np.linspace(1, 0, 14)])
    b = l.masa(franja(0, 1), material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.4, contraluz=.3)
    for f0, f1 in ((0, 1 / 3), (2 / 3, 1)):
        l.mancha(franja(f0, f1), CELESTE, .95, dentro=b)
    sol_de_mayo(l, 75.4, 7.4 + ola(.5), 1.7)


# ------------------------------------------------------------------------------------------------ Buenos Aires
def leon_echado(l, x, base, s=1.0):
    """un león echado como una esfinge, mirando a la izquierda: la melena en rulos, las patas de adelante estiradas, la cola; (x, base)
    es la línea del agua bajo el medio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    cuerpo = [forma(P([(-6, 0), (-7, -4), (-4, -7), (4, -7.4), (10, -6), (13, -3), (13.4, 0)]), 2),
              tubo(P([(-6, -1.4), (-12, -.8), (-17, -.6)]), [2 * s, 1.8 * s, 1.6 * s], 5), tubo(P([(-4.4, -.4), (-10, -.2), (-15.4, 0)]), [1.8 * s, 1.6 * s, 1.5 * s], 5),
              tubo(P([(12.6, -2), (16.6, -3.4), (19.6, -1.6), (21.4, -3)]), [.8 * s, .7 * s, .6 * s, .5 * s], 8), O(21.8, -3.4, 1.2, 1.1)]
    c = l.masa(cuerpo, material='acento', alto=.5, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    melena = [O(-8 + 4.2 * math.cos(math.radians(a)), -9 + 4.6 * math.sin(math.radians(a)), 2.2, 2) for a in range(0, 360, 30)]
    m = l.masa(melena + [O(-8, -9, 5.4, 5.8)], material='acento', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.45, contraluz=.35)
    for a in range(0, 360, 30):                                          # los rulos de la melena, como olas
        cx, cy = x + (-8 + 4.2 * math.cos(math.radians(a))) * s, base + (-9 + 4.6 * math.sin(math.radians(a))) * s
        l.trazo([(cx - .7 * s, cy), (cx, cy - .7 * s), (cx + .7 * s, cy)], .16 * s, color='6B4E10', alfa=.7, dentro=m)
    l.masa([O(-10.2, -8.4, 3.2, 3.2), O(-12.6, -6.6, 2, 1.6)], material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.mancha(O(-11, -9.8, .5, .42), '05201C', 1)
    l.mancha(O(-14.2, -7.2, .6, .45), '5A3E1E', .9)
    l.trazo(P([(-14.2, -5.6), (-12.4, -5.2), (-11.2, -5.8)]), .16 * s, color='5A3E1E', alfa=.8)
    return c


def buenos_aires(l):
    rng = np.random.default_rng(10)
    cielo(l, sol=None)
    nube(l, 40, 4.4, 14, .45)
    nube(l, 104, 3.6, 12, .4)
    # el Río de la Plata, color de león, hasta el horizonte: no se ve la otra orilla
    horizonte = 16
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, 41.5), LEONADO, .55, dentro=m)
    for _ in range(24):
        x, y = rng.uniform(26, 118), rng.uniform(horizonte + 1.6, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='E8DDBE', alfa=.7)
    # a la izquierda, la ciudad: los edificios altos y el Obelisco, en la costanera
    for x, h in ((2, 16), (8, 12), (14, 19), (20, 14), (26, 10)):
        e = l.masa(box(x - 2.4, 30 - h, x + 2.4, 30.2), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25, arroja=False)
        for y in np.arange(30 - h + .8, 30, 1.2):
            l.trazo([(x - 2, y), (x + 2, y)], .08, color='8EB5AA', alfa=.8, dentro=e)
    l.masa([Polygon([(30, 30.4), (30.8, 6.4), (31.8, 4.6), (32.8, 6.4), (33.6, 30.4)])], material='claro', alto=.4, brillo=.3, vientre=0, hondo=0,
           linea=.35)                                                    # el Obelisco
    l.mancha(box(33, 9, 33.2, 30), '9DB9B0', .5)
    orilla(l, forma([(-2, 41.5), (-2, 29.6), (20, 30), (36, 30.6), (40, 34), (34, 41.5)], 2), tinte=.2)
    # el león dorado, protagonista, echado en el río color de león
    for k in range(3):
        l.trazo([(78 + (16 + k * 4) * math.cos(t), 33.6 + (1.4 + k * .6) * math.sin(t)) for t in np.linspace(0, math.pi, 20)], .16, color='E8DDBE',
                alfa=.7 - k * .15)
    g = leon_echado(l, 76, 33.4, 1.25)
    reflejo(l, g.g, 33.6, .3, 'F2D48A')


# ------------------------------------------------------------------------------------------------ Montevideo
def vigia(l, x, base, s=1.0):
    """el vigía en la cofa, visto de cerca: asoma del barril de la cofa con la camisa dorada y mira por el catalejo dorado hacia la
    derecha; (x, base) es el borde de arriba de la cofa, al medio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    camisa = l.masa([forma(P([(-4.2, 1), (-4, -6), (-2.6, -8.4), (2.6, -8.4), (4, -6), (4.2, 1)]), 1),
                     tubo(P([(2.6, -7.6), (5.6, -9), (7.6, -10.8)]), [1.3 * s, 1.1 * s, 1 * s], 6),
                     tubo(P([(-2.4, -7.6), (1.6, -9.6), (5, -11)]), [1.3 * s, 1.1 * s, 1 * s], 6)], material='acento', alto=.45, brillo=.4, vientre=0,
                    hondo=0, linea=.4, contraluz=.35)
    for u in (-1.6, 0, 1.6):
        l.trazo(P([(u, -8), (u - .2, .6)]), [.06, .18, .06], color='6B4E10', alfa=.45, dentro=camisa)
    piel(l, [O(.6, -11.6, 2.6, 2.8), box(x - .6 * s, base - 9 * s, x + 1.6 * s, base - 8 * s), O(7.6, -11, 1.1, 1), O(5.4, -11.4, 1.1, 1)], .5)
    l.masa([forma(P([(-2, -12.6), (-2.2, -14.4), (0, -15.4), (2.6, -15), (3.4, -13.8), (1.4, -14), (-.6, -13)]), 1), O(-1.8, -13, .9, 1.6)],
           material='oscuro', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.3)                # el gorro
    l.mancha(O(1.6, -12.2, .3, .3), '05201C', 1)
    cat = [tubo(P([(3.6, -12.2), (10, -13.8), (17, -15.4)]), [.8 * s, 1 * s, 1.3 * s], 4), O(17.4, -15.5, .5, 1.4, -14)]
    c = l.masa(cat, material='acento', alto=.5, brillo=.55, vientre=0, hondo=0, linea=.4, contraluz=.4)
    for u in (8.6, 12.4):                                                # los tramos del catalejo
        l.trazo(P([(u, -14.4), (u, -12.6)]), .16 * s, color='6B4E10', alfa=.8, dentro=c)
    cofa = forma(P([(-7, 0), (-6.4, 6.6), (6.4, 6.6), (7, 0)]), 1)
    k = l.masa(cofa, material='vientre', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(cofa.buffer(1), '5A3E1E', .6, dentro=k)
    for v in (1.6, 3.6, 5.6):
        l.trazo(P([(-6.8, v), (6.8, v)]), .12 * s, color='3A2A0A', alfa=.45, dentro=k)
    for u in np.arange(-5, 6, 2.5):
        l.trazo(P([(u, .2), (u * .95, 6.4)]), .1 * s, color='3A2A0A', alfa=.35, dentro=k)


def montevideo(l):
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 64, 3, 10, .35)
    # enfrente, al otro lado de la bahía, el Cerro con su fortaleza y su faro
    prado(l, 24, 27, .2)
    cerro = forma([(62, 26), (72, 19), (82, 13), (92, 11.4), (102, 13.6), (112, 19), (122, 23), (122, 27), (62, 27)], 2)
    l.masa(cerro, material='cuerpo', alto=.35, brillo=.1, vientre=0, hondo=0, linea=.35)
    piedra(l, [box(84, 8.4, 100, 11.6), box(86, 6.6, 89, 8.6), box(95, 6.6, 98, 8.6)], .25, .3)
    f = l.masa([box(90.6, 1.8, 92.8, 8.6), box(90.2, .8, 93.2, 2)], material='claro', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.25)
    l.mancha(box(90, 4, 94, 5.2), '2F8A74', .8, dentro=f)
    rio(l, 26.6)
    for k in range(3):                                                   # la mirada del vigía, que va hasta el Cerro
        l.trazo([(68 + k * 6, 9 + k * .1), (71 + k * 6, 9.1 + k * .1)], .3, color='FFFFFF', alfa=.85)
    # el palo mayor, con sus obenques, y la cofa con el vigía, protagonista, que asoma y mira con el catalejo dorado
    l.masa(box(48.6, 22, 51.4, 41.6), material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    l.mancha(box(48, 21, 52, 42), '5A3E1E', .6)
    for x0 in (30, 70):
        l.trazo([(x0, 41.6), (50, 26)], .16, color='0C3A33', alfa=.6)
        l.trazo([(x0 + (50 - x0) * .3, 41.6), (50, 28)], .12, color='0C3A33', alfa=.5)
    l.masa(box(40, 32.6, 60, 33.6), material='vientre', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3)  # la verga
    l.mancha(box(39, 32, 61, 34.2), '5A3E1E', .55)
    vigia(l, 50, 22.4, 1.05)


# ------------------------------------------------------------------------------------------------ el mar
def cofre(l, x, base, s=1.0):
    """un cofre de tesoro abierto, de madera con herrajes dorados, lleno de monedas de plata que se desbordan; (x, base) es la línea del agua"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    tapa = forma(P([(-7.6, -10), (-7, -15.6), (0, -17.6), (7, -15.6), (7.6, -10)]), 1)
    t = l.masa(tapa, material='vientre', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(tapa.buffer(1), '5A3E1E', .6, dentro=t)
    monedas = [ovalo(x + u * s, base + v * s, 1.3 * s, .7 * s) for u, v in ((-5, -10.4), (-2.4, -11), (0, -10.6), (2.6, -11.2), (5, -10.4), (-3.6, -12.2),
                                                                             (-1, -12.6), (1.6, -12.4), (4, -12), (0, -13.6), (-8.6, -6), (9, -5.4))]
    l.masa(monedas, material='claro', alto=.6, brillo=.6, vientre=0, hondo=0, linea=.3, contraluz=.4)
    caja = box(x - 8 * s, base - 10.4 * s, x + 8 * s, base)
    c = l.masa(caja, material='vientre', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.4)
    l.mancha(caja.buffer(1), '5A3E1E', .6, dentro=c)
    for v in (-7, -3.6):
        l.trazo([(x - 8 * s, base + v * s), (x + 8 * s, base + v * s)], .1 * s, color='3A2A0A', alfa=.5, dentro=c)
    herrajes = [box(x - 8.4 * s, base - 10.8 * s, x - 6.6 * s, base), box(x + 6.6 * s, base - 10.8 * s, x + 8.4 * s, base),
                box(x - 8.4 * s, base - 10.8 * s, x + 8.4 * s, base - 9.6 * s), box(x - 1.4 * s, base - 9.8 * s, x + 1.4 * s, base - 6.4 * s),
                Polygon(P([(-7.6, -10), (-7, -15.6), (-6, -15.8), (-6.4, -10)])), Polygon(P([(6.4, -10), (6, -15.8), (7, -15.6), (7.6, -10)]))]
    h = l.masa(herrajes, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.4)
    l.mancha(ovalo(x, base - 7.6 * s, .4 * s, .6 * s), '3A2A0A', .9, dentro=h)          # el ojo de la cerradura
    return caja.union(tapa)


def mar(l):
    rng = np.random.default_rng(12)
    cielo(l, sol=None)
    nube(l, 30, 5, 16, .5)
    nube(l, 92, 4, 12, .45)
    # el Atlántico verde, al fondo, contra el agua marrón del Río de la Plata, adelante
    horizonte = 18
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(Polygon([(-2, 25.4), (30, 24.6), (60, 25.4), (90, 24.4), (122, 25.2), (122, 41.6), (-2, 41.6)]), MARRON, .6, dentro=m, difuso=.8)
    for _ in range(22):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 1.6, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='E8DDBE' if y > 25 else 'A4DCC4', alfa=.7)
    # lejos: un carguero que sale al mar y, en su islote, un faro
    l.masa([forma([(70, horizonte + .2), (98, horizonte + .2), (100.4, horizonte - 1.8), (69, horizonte - 1.8)], 1), box(71, horizonte - 4.2, 75, horizonte - 1.7)],
           material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    for k in range(7):
        l.masa(box(76 + k * 3, horizonte - 3.6, 78.6 + k * 3, horizonte - 1.7), material=('cuerpo', 'claro', 'lejos')[k % 3], alto=.15, brillo=.1,
               vientre=0, hondo=0, linea=.18)
    l.masa(forma([(8, horizonte + .4), (11, horizonte - .6), (19, horizonte - .4), (22, horizonte + .6)], 1), material='vientre', alto=.15, brillo=0,
           vientre=0, hondo=0, linea=.25)
    fr = l.masa([forma([(13.4, horizonte - .4), (13.8, 9.4), (16, 9.4), (16.4, horizonte - .4)], 0), box(13, 8.2, 16.8, 9.6)], material='claro',
                alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(box(12, 12, 18, 13.6), '2F8A74', .85, dentro=fr)
    for x, y, s in ((36, 8, .8), (46, 6, .6), (104, 9, .7)):
        ave(l, x, y, s)
    # el cofre de plata, protagonista, que flota en la boca del río
    for k in range(3):
        l.trazo([(60 + (10 + k * 2.6) * math.cos(t), 34.6 + (1.2 + k * .5) * math.sin(t)) for t in np.linspace(0, math.pi, 20)], .16, color='E8DDBE',
                alfa=.75 - k * .15)
    g = cofre(l, 60, 34.4, 1.15)
    reflejo(l, g, 34.6, .25)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Foz do Iguaçu', dibujar=foz), dict(clave='Encarnación', dibujar=encarnacion),
            dict(clave='Corrientes', dibujar=corrientes), dict(clave='Rosario', dibujar=rosario), dict(clave='Buenos Aires', dibujar=buenos_aires),
            dict(clave='Montevideo', dibujar=montevideo), dict(clave='mar', dibujar=mar)]
LISTO = True
