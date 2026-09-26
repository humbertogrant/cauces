# -*- coding: utf-8 -*-
"""Las postales del Tigris, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), que es lo que el jugador tiene que retener, con lo que dice el dato del lugar:

- el nacimiento, en los montes Tauro: las montañas nevadas, los campos y dos ríos jóvenes que bajan juntos, el Tigris y el Éufrates,
  «su gemelo», que nace a pocos kilómetros;
- Diyarbakır: las murallas negras de basalto sobre su meseta, los huertos junto al río y el puente de los Diez Ojos (1065);
- Mosul: un toro alado de Nínive (un lamassu, con cabeza de hombre barbado y tiara de cuernos) cubierto con una tela de muselina,
  que se llama así por Mosul, y al fondo las ruinas de la muralla de Nínive;
- Tikrit: «un tic-tac de 800 años»: el sol es un reloj sobre la ciudadela, en lo alto del barranco sobre el río;
- Samarra: la Malwiya, el minarete en espiral de la Gran Mezquita, y el muro de la mezquita con sus torres redondas;
- Bagdad: la ciudad redonda, con la muralla y sus puertas, una biblioteca gigante en el centro y el río teñido de tinta, con libros
  que flotan (762 y 1258);
- Basora: el barco de Simbad que zarpa donde los dos ríos ya son uno, entre palmerales datileros;
- el mar: el Shatt al-Arab que se abre al golfo Pérsico al atardecer, con palmeras, un faro y un barco.
"""
import math

import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import VISTA, arbol, cielo, cordillera, fondo, nube, palmera, reflejo, rio, tierra
from pintor import curva, forma, ovalo, tubo


def cinta(pts, anchos):
    """una cinta de ancho variable a lo largo de una curva: un río que baja"""
    c = curva(pts, 10)
    a = np.interp(np.linspace(0, 1, len(c)), np.linspace(0, 1, len(anchos)), anchos)
    izq, der = [], []
    for i in range(len(c)):
        d = c[min(i + 1, len(c) - 1)] - c[max(i - 1, 0)]
        d = d / (np.hypot(*d) or 1)
        n = np.array([-d[1], d[0]])
        izq.append(c[i] + n * a[i] / 2)
        der.append(c[i] - n * a[i] / 2)
    return Polygon(izq + der[::-1]).buffer(0)


def rio_joven(l, pts, anchos):
    """un río que baja de la montaña: la cinta de agua verde clara, con su brillo"""
    g = cinta(pts, anchos)
    m = l.masa(g, material='vientre', alto=.05, brillo=0, vientre=0, hondo=0, linea=.3, escalon=0, contraluz=0, arroja=False)
    l.mancha(g, '64C8AA', .9, dentro=m)
    c = curva(pts, 10)
    l.trazo([tuple(p + np.array([-.25, 0])) for p in c[::3]], [.1] + [.3] * (len(c[::3]) - 2) + [.1], color='F4FBF7', alfa=.8, dentro=m)
    return g


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    cielo(l, sol=(104, 7))
    nube(l, 28, 6.4, 14, .75)
    nube(l, 66, 4.6, 10, .6)
    cordillera(l, [(-2, 17), (6, 10.6), (12, 14.2), (20, 7.6), (28, 13.2), (36, 9.8), (44, 15.6), (52, 8.4), (60, 12.6), (68, 7),
                   (78, 13.8), (86, 9.6), (96, 15.2), (104, 11), (112, 14.4), (122, 11.4)], material='vientre', nieve=11.8, linea=.3,
               alto=.3)
    cordillera(l, [(-2, 22.4), (8, 16.6), (18, 21.2), (28, 14.8), (38, 20.8), (46, 18.2), (56, 23.2), (64, 17), (74, 22.6), (84, 16),
                   (94, 21.2), (104, 17.8), (114, 22.2), (122, 19.2)], material='lejos', nieve=18.6, linea=.4)
    cordillera(l, [(-2, 27.4), (14, 23.8), (30, 26.8), (48, 24.4), (62, 27.6), (80, 24), (98, 27), (122, 24.4)], material='cuerpo',
               linea=.35, alto=.25)
    # los campos: franjas de parcelas en perspectiva, con sus surcos
    rng = np.random.default_rng(4)
    for fila, (y0, y1) in enumerate(((27.6, 30.4), (30.4, 33.8), (33.8, 37.4), (37.4, 41))):
        x = -2 - fila * 3.4
        while x < 122:
            w = rng.uniform(12, 22) * (1 + fila * .25)
            g = Polygon([(x, y0), (x + w, y0), (x + w + (fila + 1) * .8, y1), (x + (fila + 1) * .8, y1)])
            m = l.masa(g, material=['vientre', 'cuerpo', 'claro'][rng.integers(0, 3)] if fila else 'vientre', alto=.06, brillo=0,
                       vientre=0, hondo=0, linea=.25, escalon=0, contraluz=0, arroja=False)
            for k in np.arange(y0 + .7, y1, .9 + fila * .15):
                l.trazo([(x + .6, k), (x + w - .4, k)], .1, color='2F8A74', alfa=.45, dentro=m)
            x += w
    for x, y in ((8, 29.2), (26, 28.6), (96, 29), (112, 28.4)):
        arbol(l, x, y, 1.8)
    # los dos ríos jóvenes que bajan juntos: el Tigris, a la izquierda, y el Éufrates, su gemelo
    rio_joven(l, [(46, 23.4), (43, 26.4), (47.4, 30.4), (42, 35), (46, 41)], [.8, 1.4, 2.2, 3.2, 4.4])
    rio_joven(l, [(66, 24), (69.6, 27.2), (65.4, 31), (71, 35.4), (67, 41)], [.8, 1.4, 2.2, 3.2, 4.4])


# ------------------------------------------------------------------------------------------------ Diyarbakır
def diyarbakir(l):
    fondo(l, suelo=29.6, rio=33.0)
    l.masa(forma([(-2, 34), (-2, 18.6), (20, 18.2), (40, 18.6), (50, 21.4), (56, 26.6), (60, 30.4), (62, 34)], 2), material='vientre',
           alto=.25, brillo=.05, vientre=0, hondo=0, linea=.45, contraluz=.2)
    for x, w, h in ((6, 5, 3.4), (12, 6, 4.2), (24, 5, 3.6), (31, 6.4, 4.6), (39, 5, 3.2)):
        l.masa(box(x, 13.6 - h + 4, x + w, 14.2), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35, arroja=False)
    l.masa(box(19, 3.4, 22.4, 14.2), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.4)
    l.masa(forma([(18.4, 3.6), (20.7, 1.2), (23, 3.6)], 0), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    l.mancha(box(20.2, 5.2, 21.2, 7), '0C3A33', .7)
    # la muralla de basalto negro, con almenas y torres
    muro = [box(-2, 11.8, 50, 19)]
    for x in np.arange(-1, 50, 1.9):
        muro.append(box(x, 10.8, x + 1, 11.9))
    for x in (4, 16, 28, 40):
        muro.append(forma([(x - 2.4, 19), (x - 2.4, 9.4), (x - 1.6, 8.8), (x + 1.6, 8.8), (x + 2.4, 9.4), (x + 2.4, 19)], 1))
        for dx in (-2, -.6, .8):
            muro.append(box(x + dx, 7.8, x + dx + .9, 8.9))
    m = l.masa(muro, material='oscuro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.35)
    rng = np.random.default_rng(3)
    for _ in range(120):                                          # los sillares de basalto
        x, y = rng.uniform(-1, 50), rng.uniform(9, 18.6)
        l.trazo([(x, y), (x + rng.uniform(1, 2), y)], .08, color='3E7A6D', alfa=.55, dentro=m)
    for x in (4, 16, 28, 40):
        l.mancha(box(x - .35, 12.4, x + .35, 14.4), '05201C', .8, dentro=m)
    # los huertos de Hevsel, entre la muralla y el río
    for x, y, r in ((4, 28.4, 2.6), (9.6, 29.6, 2.2), (15, 28.2, 2.8), (21, 29.8, 2.3), (26.4, 28.6, 2.7), (32, 29.8, 2.2),
                    (37.4, 28.8, 2.6), (43, 30, 2.2), (48.6, 29.2, 2.4)):
        arbol(l, x, y, r)
    # el puente de los Diez Ojos: el tablero y sus diez arcos
    x0, x1, yt, ya = 54, 120, 25.4, 33.2
    puente = box(x0, yt, x1, ya)
    luz = (x1 - x0) / 10
    for k in range(10):
        c = x0 + luz * (k + .5)
        r = luz * .36 * (1.12 if k in (4, 5) else 1)
        puente = puente.difference(ovalo(c, ya, r, r * 1.35).union(box(c - r, ya, c + r, ya + 2)))
    p = l.masa(puente, material='lejos', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.3)
    l.trazo([(x0, yt + .9), (x1, yt + .9)], .18, color='0C3A33', alfa=.6, dentro=p)
    for k in range(10):
        c = x0 + luz * (k + .5)
        l.trazo([(c - luz * .36, ya - .2), (c - luz * .3, ya - luz * .32), (c, ya - luz * .5), (c + luz * .3, ya - luz * .32),
                 (c + luz * .36, ya - .2)], .12, color='A4DCC4', alfa=.45, dentro=p)
    rio(l, 33.2)
    reflejo(l, puente, 33.2, .35)


# ------------------------------------------------------------------------------------------------ Mosul
def lamassu(l):
    """el toro alado de Nínive, de perfil, mirando a la derecha: cuerpo de toro, el ala que nace del hombro y se abre hacia atrás y
    hacia arriba en filas de plumas, la cabeza de hombre con barba rizada y tiara de cuernos; sobre su plinto. De piedra: verde claro"""
    l.masa(box(8.4, 29.2, 56.4, 31.4).buffer(.2), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.45)     # el plinto
    patas = [box(15.2, 21, 18.6, 29.4), box(21.4, 21, 24.6, 29.4), box(42.4, 20, 45.6, 29.4), box(47, 20, 50.2, 29.4)]
    for x in (15.2, 21.4, 42.4, 47):                               # las pezuñas
        patas.append(forma([(x - .3, 29.4), (x - .2, 27.8), (x + 3.4, 27.8), (x + 3.6, 29.4)], 1))
    cuerpo = forma([(13, 13.6), (22, 12.6), (34, 12.6), (44, 12.2), (48.6, 11.4), (51.2, 13.4), (51.6, 18.4), (50.4, 22.2), (44, 22.6),
                    (30, 23), (18, 22.8), (13.4, 21), (12.4, 17)], 2)
    cola = tubo([(13, 15), (10.6, 18), (10.2, 23.4)], [.7, .6, .5])
    borla = ovalo(10.2, 24.6, 1.1, 1.8)
    c = l.masa([cuerpo, cola, borla] + patas, material='cuerpo', alto=.4, brillo=.15, vientre=.2, hondo=.1, linea=.5, escalon=.2,
               contraluz=.3, bultos=[(ovalo(46, 17, 5, 5), .2), (ovalo(18, 18, 5, 5), .15)])
    for x in (16.8, 23, 44, 48.6):                                 # los músculos de las patas, tallados
        l.trazo([(x - 1, 22.6), (x, 24.4), (x - .6, 26.4)], [.08, .2, .08], alfa=.45, dentro=c)
    for k in range(5):                                             # el pelo rizado del vientre, en hileras
        l.trazo([(20 + k * 5, 22.2), (21 + k * 5, 21.2), (22 + k * 5, 22.2)], .14, alfa=.45, dentro=c)
    # el ala: nace angosta en el hombro y se abre hacia atrás y hacia arriba; arriba, las plumas chicas en escamas; abajo, las
    # largas, que terminan en punta atrás
    arriba_ = [(48, 12.6), (45, 9.8), (39, 7.2), (31, 5.2), (22, 4), (14, 3.8), (8.6, 4.6)]
    abajo = [(47, 13), (42, 12.8), (34, 12), (26, 10.6), (18, 9.2), (12, 8.2), (8.2, 7.2)]
    puntas = [(8.6, 4.6), (7, 5.2), (8.6, 5.8), (7.2, 6.4), (8.2, 7.2)]
    ala = Polygon(arriba_ + puntas[1:-1] + abajo[::-1]).buffer(.2).buffer(-.1)
    a = l.masa(ala, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.3)
    A, B = np.array(arriba_), np.array(abajo)
    for f in (.12, .28):                                           # las plumas chicas, en escamas
        fila = A + (B - A) * f
        for i in range(len(fila) - 1):
            for u in np.linspace(0, 1, 4)[:-1]:
                q = fila[i] + (fila[i + 1] - fila[i]) * u
                l.trazo([tuple(q + [-.5, -.1]), tuple(q + [0, .5]), tuple(q + [.5, -.1])], [.05, .12, .05], alfa=.5, dentro=a)
    for f in (.45, .6, .75, .9):                                   # las plumas largas, a lo largo, hacia la punta
        fila = A + (B - A) * f
        l.trazo([tuple(q) for q in fila[1:]], [.16, .14, .12, .1, .08, .04], alfa=.45, dentro=a)
    # la cabeza de hombre: la cara, la barba rizada en hileras y la tiara con sus cuernos
    cara = forma([(48.8, 11.6), (48.6, 7), (50.4, 5), (53, 5.2), (53.8, 7), (54.6, 8.4), (53.8, 9.2), (54, 10.6), (52.6, 11.4)], 2)
    barba = forma([(48.8, 10.2), (53.4, 10.6), (54, 13.4), (53.4, 17.4), (49.4, 17.6), (48.4, 14)], 1)
    tiara = forma([(49.4, 5.6), (49.2, 1.4), (53.8, 1.4), (53.6, 5.6)], 1)
    h = l.masa([cara, barba, tiara], material='cuerpo', alto=.35, brillo=.15, vientre=0, hondo=.1, linea=.45, escalon=.2, contraluz=.3)
    for y in np.arange(11.6, 17.4, 1.3):                            # los rizos de la barba
        for x in np.arange(49.2, 53.6, 1.2):
            dx = .6 if int(y) % 2 else 0
            l.mancha(ovalo(x + dx, y, .42, .42), '2F8A74', .9, dentro=h)
            l.mancha(ovalo(x + dx + .1, y + .1, .18, .18), '0C3A33', .6, dentro=h)
    for y in (2.4, 3.6, 4.8):                                       # los cuernos de la tiara
        l.trazo([(49.6, y), (51.4, y - .5), (53.4, y)], [.1, .2, .1], alfa=.6, dentro=h)
    l.trazo([(49.2, 1.6), (53.8, 1.6)], [.2, .3, .2], color='E8B952', alfa=.9, dentro=h)
    l.mancha(ovalo(52.2, 6.8, .6, .36), '0C3A33', .9, dentro=h)       # el ojo grande, tallado
    l.trazo([(51.2, 6), (52.8, 5.8)], .16, alfa=.7, dentro=h)
    l.trazo([(52.6, 10.2), (53.6, 10.4)], .14, alfa=.6, dentro=h)
    return unary_union([cuerpo, ala, cara, barba, tiara] + patas)


def mosul(l):
    fondo(l, desierto=.35)
    # al fondo, las ruinas de la muralla de Nínive: un tramo de adobe con su puerta, gastado, sobre lomas de ruinas
    l.masa(forma([(56, 31.2), (60, 27.6), (70, 26.4), (84, 27.8), (96, 26.2), (112, 27.4), (122, 26.8), (122, 31.6), (56, 31.6)], 2),
           material='vientre', alto=.15, brillo=0, vientre=0, hondo=0, linea=.35, contraluz=.2, arroja=False)
    puerta = forma([(84, 28.4), (84, 22.4), (86, 20.2), (89, 20.2), (91, 22.4), (91, 28.4)], 1)
    muro = box(66, 17.4, 112, 28)
    for x in np.arange(66, 112, 2.4):
        muro = muro.union(box(x, 16.2, x + 1.3, 17.6))
    muro = muro.union(box(80, 15, 95, 28)).difference(forma([(100, 15), (103, 19.6), (108, 18.4), (112.4, 21.4), (113, 14)], 1))
    m = l.masa(muro.difference(puerta), material='vientre', alto=.25, brillo=.05, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.2)
    l.mancha(box(-2, 14, 122, 29), 'E8B952', .28, dentro=m)
    for y in np.arange(18.6, 28, 1.5):                               # las hileras de adobe
        l.trazo([(66.4, y), (111.6, y)], .07, color='6B4E10', alfa=.3, dentro=m)
    l.mancha(forma([(84.2, 28.4), (84.2, 22.4), (86, 20.4), (89, 20.4), (90.8, 22.4), (90.8, 28.4)], 1), 'CFE0DA', .6)
    g = lamassu(l)
    # la tela de muselina, blanca, fina y transparente, echada sobre el lomo: cae por el costado en pliegues, con el borde en flecos
    tela = forma([(15.6, 9.6), (22, 7.4), (31, 7.2), (39, 8.6), (45.4, 11.4), (47.6, 15), (46.4, 22), (43, 20.2), (40, 24), (36, 21.6),
                  (32, 24.4), (28, 21.8), (24, 24.2), (20.6, 21.2), (17.8, 23.2), (15.6, 16)], 2)
    t = l.masa(tela, material='claro', alto=.3, brillo=.25, vientre=0, hondo=0, linea=.35, escalon=.15, contraluz=.35, arroja=False)
    # la transparencia: dejo ver el toro por debajo, a través de la tela, con un velo del color del cuerpo
    l.mancha(tela.intersection(g), '6CC8A8', .28, dentro=t)
    for x0, x1 in ((20.4, 19.4), (25.6, 25), (31, 30.6), (36.6, 36.2), (41.6, 41.6)):
        l.trazo([(x0 + 1.4, 8.4), (x0 + .4, 14), (x1, 22.4)], [.06, .3, .12], color='FFFFFF', alfa=.95, dentro=t)
        l.trazo([(x0 + 2.2, 8.8), (x0 + 1.2, 14.4), (x1 + .8, 22.8)], [.04, .16, .06], color='8EB5AA', alfa=.8, dentro=t)
    borde = [(15.6, 16), (17.8, 23.2), (20.6, 21.2), (24, 24.2), (28, 21.8), (32, 24.4), (36, 21.6), (40, 24), (43, 20.2), (46.4, 22)]
    for (x0, y0), (x1, y1) in zip(borde[1:-1], borde[2:]):          # los flecos
        for u in np.linspace(0, 1, 4)[:-1]:
            x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            l.trazo([(x, y), (x, y + 1)], .09, color='8EB5AA', alfa=.8)
    rio(l)
    reflejo(l, g, 34, .3)


# ------------------------------------------------------------------------------------------------ Tikrit
def reloj(l, x, y, r):
    """el sol es un reloj: la esfera dorada, el aro, las doce marcas y las agujas; unas rayitas que dicen «tic, tac»"""
    l.mancha(ovalo(x, y, r * 2.2, r * 2.2), 'F2D48A', .35, difuso=2.4)
    e = l.masa(ovalo(x, y, r, r), material='acento', alto=.4, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=0)
    l.mancha(ovalo(x, y, r * .82, r * .82), 'FBEFCB', .55, dentro=e)
    for k in range(12):
        a = math.radians(k * 30)
        d = np.array([math.sin(a), -math.cos(a)])
        l.trazo([(x + d[0] * r * .66, y + d[1] * r * .66), (x + d[0] * r * .8, y + d[1] * r * .8)], .3 if k % 3 == 0 else .16,
                alfa=.9, dentro=e)
    for grados, largo, ancho in ((300, .46, .38), (60, .66, .24)):     # las diez y diez
        a = math.radians(grados)
        l.trazo([(x, y), (x + math.sin(a) * r * largo, y - math.cos(a) * r * largo)], [ancho, ancho * .6], alfa=.95, dentro=e)
    l.mancha(ovalo(x, y, .4, .4), '0C3A33', 1, dentro=e)
    for s in (-1, 1):                                                 # tic, tac
        for k in (1, 2):
            rr = r + 1 + k * 1.1
            l.trazo([(x + s * rr * math.cos(math.radians(a_)), y - rr * math.sin(math.radians(a_))) for a_ in (-25, 0, 25)],
                    .16, color='93701A', alfa=.8)


def tikrit(l):
    cielo(l, sol=None)
    reloj(l, 98, 10.4, 5.6)
    tierra(l, 30.4, 34.5, desierto=.35)
    # el barranco sobre el río, con sus capas de tierra, y la ciudadela en lo alto
    barranco = forma([(-2, 34.4), (-2, 17.6), (10, 16.4), (26, 16.8), (40, 17.6), (46, 19.8), (49, 24), (52, 28.6), (56, 32), (60, 34.4)], 2)
    b = l.masa(barranco, material='vientre', alto=.3, brillo=.05, vientre=0, hondo=.1, linea=.45, escalon=.25, contraluz=.25)
    l.mancha(barranco, 'E8B952', .35, dentro=b)
    for k, y in enumerate((20.4, 23.4, 26.4, 29.4)):
        l.trazo([(-2, y), (20, y + .3), (36 + k * 3, y + .2), (46 + k * 2.4, y + 1.6)], [.08, .2, .2, .08], color='93701A', alfa=.5,
                dentro=b)
    muro = [box(4, 11.2, 40, 17)]
    for x in (6, 16, 28, 38):
        muro.append(box(x - 2, 8.6, x + 2, 17))
    muro = unary_union(muro)
    for x, y in ((12, 10.4), (24, 9.6), (33, 10.8)):                  # las partes gastadas: la ciudadela es una ruina
        muro = muro.difference(ovalo(x, y, 2.6, 1.8))
    for x in np.arange(4.4, 40, 1.8):
        if muro.contains(box(x, 11, x + .9, 11.4)):
            muro = muro.difference(box(x, 10.2, x + .9, 11.4))
    m = l.masa(muro, material='lejos', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
    l.mancha(box(-2, 8, 122, 18), 'E8B952', .18, dentro=m)
    for x in (6, 16, 28, 38):
        l.mancha(box(x - .35, 12, x + .35, 13.8), '0C3A33', .7, dentro=m)
    for xp, h, lado in ((70, 8, 1), (76, 9.4, -1), (112, 8.2, 1)):
        palmera(l, xp, 31, h, lado)
    rio(l)
    reflejo(l, barranco, 34, .3)


# ------------------------------------------------------------------------------------------------ Samarra
def malwiya(x, base, alto_=25.0, ancho=15.6, vueltas=5):
    """la silueta de la Malwiya: la base cuadrada y el cono que se angosta en escalones; cada vuelta de la rampa asoma como un
    escalón en los dos bordes"""
    y0 = base - 1.8
    izq, der = [], []
    for k in range(vueltas):
        f0, f1 = k / vueltas, (k + 1) / vueltas
        w0, w1 = ancho * (1 - .7 * f0) / 2, ancho * (1 - .7 * f1) / 2
        ya, yb = y0 - (alto_ - 4) * f0, y0 - (alto_ - 4) * f1
        der += [(x + w0, ya + .6 * (k > 0)), (x + w0 - .3, yb + 1.4), (x + w1 + .2, yb + 1.4)]
        izq += [(x - w0, ya), (x - w0 + .3, yb + .4), (x - w1 - .2, yb + .4)]
    wt, yt = ancho * .3 / 2, y0 - (alto_ - 4)
    return Polygon([(x - ancho / 2 - 1.2, base), (x + ancho / 2 + 1.2, base), (x + ancho / 2 + 1.2, y0)] + der + [(x + wt, yt), (x - wt, yt)]
                   + izq[::-1] + [(x - ancho / 2 - 1.2, y0)]).buffer(.1)


def samarra(l):
    fondo(l, desierto=.3)
    l.masa(forma([(-2, 31.2), (14, 29.4), (30, 30.4), (52, 29.2), (80, 30.6), (104, 29.4), (122, 30.2), (122, 31.6), (-2, 31.6)], 2),
           material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.35, contraluz=.2, arroja=False)
    muro = [box(50, 25.4, 106, 31.2)]
    for x in np.arange(52, 106, 4.4):
        muro.append(forma([(x - 1.3, 31.2), (x - 1.3, 24.8), (x - .8, 24.2), (x + .8, 24.2), (x + 1.3, 24.8), (x + 1.3, 31.2)], 1))
    m = l.masa(muro, material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.4, escalon=.2)
    for x in np.arange(54.2, 104, 4.4):
        l.mancha(box(x - .35, 26.6, x + .35, 28.2), '0C3A33', .5, dentro=m)
    x, base = 34, 31.2
    s = malwiya(x, base)
    t = l.masa(s, material='cuerpo', alto=.45, brillo=.12, vientre=0, hondo=.1, linea=.5, escalon=.25, contraluz=.25,
               bultos=[(ovalo(x - 1, 20, 5, 11), .25)])
    for k in range(5):                                             # la rampa: una franja clara que sube en diagonal en cada vuelta
        f0, f1 = k / 5, (k + 1) / 5
        y0, y1 = base - 1.8 - 21 * f0, base - 1.8 - 21 * f1
        w0, w1 = 7.8 * (1 - .72 * f0), 7.8 * (1 - .72 * f1)
        l.trazo([(x - w0, y0 - .5), (x + w1 * .3, y0 - 1.9 - (y0 - y1) * .3), (x + w0 * .96, y1 + .2)], [.25, .6, .25], color='D2F2DA',
                alfa=.8, dentro=t, difuso=.08)
        l.trazo([(x - w0, y0 + .1), (x + w1 * .3, y0 - 1.3 - (y0 - y1) * .3), (x + w0 * .96, y1 + .8)], [.1, .22, .1], color='0C3A33',
                alfa=.5, dentro=t)
    l.masa(box(x - 2.2, base - 25.8, x + 2.2, base - 23.2).buffer(.2), material='cuerpo', alto=.3, brillo=.1, vientre=0, hondo=0,
           linea=.4)
    for dx in (-1.1, .2):
        l.mancha(forma([(x + dx, base - 23.4), (x + dx, base - 24.8), (x + dx + .45, base - 25.3), (x + dx + .9, base - 24.8),
                        (x + dx + .9, base - 23.4)], 1), '0C3A33', .75)
    for xp, h, lado in ((10, 8.6, 1), (15, 7, -1), (110, 9, -1), (116, 7.4, 1)):
        palmera(l, xp, 31.4, h, lado)
    rio(l)
    reflejo(l, s, 34, .35)


# ------------------------------------------------------------------------------------------------ Bagdad
def libro(l, x, y, w=2.8):
    """un libro abierto que flota en el río de tinta: las dos mitades como una V muy abierta, con el lomo en el agua, y la mancha de
    tinta que suelta alrededor"""
    l.mancha(ovalo(x, y + .5, w * 1.7, 1), '05201C', .6, difuso=.4)
    hojas = [Polygon([(x, y + .2), (x - w, y - 1.3), (x - w - .3, y - .6), (x - .2, y + .7)]),
             Polygon([(x, y + .2), (x + w, y - 1.3), (x + w + .3, y - .6), (x + .2, y + .7)])]
    b = l.masa([h.buffer(.12) for h in hojas], material='claro', alto=.2, brillo=.3, vientre=0, hondo=0, linea=.3, arroja=False)
    for s in (-1, 1):
        for k in (.35, .6, .85):
            l.trazo([(x + s * w * k * .3, y - .1 - w * k * .12), (x + s * w * k, y - 1.1 * k)], .07, color='8EB5AA', alfa=.9, dentro=b)
    l.trazo([(x, y - .1), (x, y + .6)], .2, color='0C3A33', alfa=.8, dentro=b)


def bagdad(l):
    """la ciudad redonda vista desde arriba: la muralla en anillo con sus torres y sus cuatro puertas, las cuatro avenidas que llegan al
    centro, las casas en anillos, y en el centro la biblioteca gigante con su cúpula verde; abajo, el río teñido de tinta"""
    from shapely import affinity
    fondo(l, suelo=24, rio=34, desierto=.28)
    cx, cy, rx, ry, h = 60, 21.6, 46, 10.4, 2.4
    l.mancha(ovalo(cx, cy, rx - 1, ry - .8), 'F0F6F4', .6)             # el suelo de la ciudad, claro
    # las cuatro avenidas, de las puertas al centro, y la plaza
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        x1, y1 = cx + (rx - 1.4) * math.cos(a), cy + (ry - 1) * math.sin(a)
        l.trazo([(x1, y1), (cx, cy)], [1.6, 1], color='D2F2DA', alfa=.95)
    l.mancha(ovalo(cx, cy + .6, 15, 3.8), 'D2F2DA', .9)
    # la muralla: el anillo con su alto; la mitad de atrás, antes de las casas, y la de adelante, después
    anillo = ovalo(cx, cy, rx, ry).difference(ovalo(cx, cy, rx - 2.2, ry - 1.5))
    solido = unary_union([affinity.translate(anillo, 0, -t) for t in np.linspace(0, h, 7)])
    torres = []
    for a in np.linspace(0, 2 * math.pi, 29)[:-1]:
        x, y = cx + (rx - 1.1) * math.cos(a), cy + (ry - .75) * math.sin(a) - h
        torres.append((y, box(x - .7, y - 1.2, x + .7, y + .6)))
    tope = affinity.translate(anillo, 0, -h)

    def muro(parte, ts):
        m = l.masa(unary_union([parte] + ts), material='lejos', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.35, escalon=.2,
                   contraluz=.25)
        l.mancha(box(-2, -2, 122, 41), 'E8B952', .2, dentro=m)
        l.mancha(tope.intersection(parte), 'D2F2DA', .5, dentro=m)          # el camino de ronda, arriba
        return m

    corte = cy - h / 2
    muro(solido.intersection(box(-2, -2, 122, corte)), [t for y, t in torres if y < corte - 1])
    # las casas, en anillos: de techo plano, claras; las de atrás, de afuera hacia adentro; las de adelante, de adentro hacia afuera
    anillos = (.42, .54, .66, .78, .9)

    def casas(r, adelante):
        bloques, techos = [], []
        paso = 3.4 / (rx * r)
        for a in np.arange(paso / 2, 2 * math.pi, paso):
            if (math.sin(a) >= 0) != adelante:
                continue
            if min(abs(math.sin(a)), abs(math.cos(a))) < .16:          # las avenidas
                continue
            x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a) + .6
            w = 2.2 + .5 * abs(math.cos(a))
            bloques.append(box(x - w / 2, y - 2.1, x + w / 2, y))
            techos.append(box(x - w / 2, y - 2.1, x + w / 2, y - 1.3))
        if bloques:
            m = l.masa(bloques, material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.28, escalon=.2, contraluz=.2)
            l.mancha(unary_union(techos), 'CFE0DA', .9, dentro=m)
    for r in anillos[::-1]:
        casas(r, False)
    # la biblioteca gigante, en el centro, con sus arcos llenos de libros y la cúpula verde
    rng = np.random.default_rng(5)
    b = l.masa(box(cx - 8, 12.4, cx + 8, 24.6).buffer(.2), material='claro', alto=.3, brillo=.12, vientre=0, hondo=0, linea=.45,
               escalon=.2, contraluz=.3)
    for k in range(3):
        x0 = cx - 6.8 + k * 5
        arco = forma([(x0, 24.2), (x0, 16.6), (x0 + .4, 15.2), (x0 + 1.9, 14.3), (x0 + 3.4, 15.2), (x0 + 3.8, 16.6), (x0 + 3.8, 24.2)], 1)
        l.mancha(arco, '164F46', .9, dentro=b)
        for y0 in (16.6, 19.2, 21.8):
            xx = x0 + .25
            while xx < x0 + 3.5:
                wl = rng.uniform(.32, .55)
                l.mancha(box(xx, y0 + rng.uniform(0, .5), xx + wl, y0 + 2.3), ['E8B952', 'D2F2DA', '6CC8A8', 'F0F6F4'][rng.integers(0, 4)],
                         .95, dentro=b)
                xx += wl + .08
            l.mancha(box(x0 + .2, y0 + 2.3, x0 + 3.6, y0 + 2.6), '0C3A33', .7, dentro=b)
    l.masa(forma([(cx - 7.2, 12.6), (cx - 6.6, 8.6), (cx - 3.8, 5.4), (cx, 4.4), (cx + 3.8, 5.4), (cx + 6.6, 8.6), (cx + 7.2, 12.6)], 2),
           material='cuerpo', alto=.5, brillo=.35, vientre=0, hondo=0, linea=.45, contraluz=.3)
    l.masa(tubo([(cx, 4.6), (cx, 2.2)], [.25, .2]), material='acento', alto=.3, brillo=.3, vientre=0, hondo=0, linea=.25)
    for r in anillos:
        casas(r, True)
    muro(solido.intersection(box(-2, corte, 122, 41)), [t for y, t in torres if y >= corte - 1])
    # las cuatro puertas: casas de guardia sobre la muralla, con su arco oscuro
    for a in (0, math.pi / 2, math.pi):
        x, y = cx + (rx - 1.1) * math.cos(a), cy + (ry - .75) * math.sin(a)
        w = 4.6 if a == math.pi / 2 else 2.8
        g = l.masa(box(x - w / 2, y - h - 3, x + w / 2, y + .6).buffer(.2), material='lejos', alto=.3, brillo=.12, vientre=0, hondo=0,
                   linea=.4, escalon=.2)
        l.mancha(box(-2, -2, 122, 41), 'E8B952', .2, dentro=g)
        l.mancha(forma([(x - w * .22, y + .6), (x - w * .22, y - 1.2), (x, y - 2), (x + w * .22, y - 1.2), (x + w * .22, y + .6)], 1),
                 '0C3A33', .85, dentro=g)
    # el río teñido de tinta, con remolinos de tinta y los libros que flotan
    a = rio(l, 34, color='oscuro', brillo='3E7A6D', ondas='6FA497', semilla=3)
    for k in range(7):
        y = 35 + k * .8
        l.trazo([(rng.uniform(-2, 30), y), (rng.uniform(40, 70), y + .4), (rng.uniform(80, 122), y - .2)], [.3, .9, .3], color='05201C',
                alfa=.6, dentro=a, difuso=.2)
    for x, y in ((12, 36.6), (33, 38.6), (55, 36.2), (78, 38.2), (99, 36.4), (114, 38.8)):
        libro(l, x, y)


# ------------------------------------------------------------------------------------------------ Basora
def dhow(l, x, y, s=1.0):
    """el barco de Simbad: un dhow, de proa larga que sale hacia adelante y popa alta, con una gran vela latina hinchada"""
    X = lambda u: x + u * s
    Y = lambda v: y + v * s
    casco = forma([(X(-13), Y(-4.6)), (X(-10), Y(-2.6)), (X(4), Y(-2.2)), (X(11), Y(-3.4)), (X(16), Y(-6.4)), (X(13), Y(-1.4)),
                   (X(8), Y(1.6)), (X(-8), Y(1.8)), (X(-12.6), Y(.4))], 1)
    v = l.masa(forma([(X(-9), Y(-3.6)), (X(-2), Y(-13)), (X(8), Y(-21)), (X(12), Y(-22.4)), (X(11), Y(-15)), (X(9), Y(-7)),
                      (X(6), Y(-3.4))], 2), material='claro', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.45, escalon=.15, contraluz=.2)
    for k in range(4):
        l.trazo([(X(-7 + k * 3.4), Y(-4.4 - k * 1.2)), (X(1 + k * 2.6), Y(-14 - k * 1.6))], [.06, .14, .06], color='8EB5AA', alfa=.6,
                dentro=v)
    l.masa(tubo([(X(-11.6), Y(-2.2)), (X(12.6), Y(-23.4))], [.35, .25], 6), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0,
           linea=.3)                                                     # la entena
    l.masa(tubo([(X(1), Y(-2)), (X(2), Y(-15))], [.4, .3], 6), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)
    c = l.masa(casco, material='acento', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.45, contraluz=.25)
    for k in range(2):
        l.trazo([(X(-12 + k), Y(-1.4 + k * 1.3)), (X(4), Y(-.6 + k * 1.3)), (X(12 - k * 2), Y(-2 + k * 1.2))], [.06, .16, .06], alfa=.4,
                dentro=c)
    l.trazo([(X(-12), Y(-3.2)), (X(4), Y(-2)), (X(14), Y(-5))], [.1, .3, .1], color='0C3A33', alfa=.6, dentro=c)
    # Simbad, en la proa: el turbante con su joya, la cara, el traje largo y el brazo que señala el mar
    cuerpo = forma([(X(8), Y(-2.4)), (X(10.4), Y(-2.4)), (X(10), Y(-5.8)), (X(8.4), Y(-5.8))], 1)
    brazo = tubo([(X(9.8), Y(-5.2)), (X(11.6), Y(-6.6)), (X(13.2), Y(-7.8))], [.32, .28, .24], 6)
    l.masa([cuerpo, brazo], material='lejos', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.masa(ovalo(X(9.2), Y(-6.6), .75, .8), material='vientre', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.masa(forma([(X(8.2), Y(-6.9)), (X(8.4), Y(-7.9)), (X(9.2), Y(-8.4)), (X(10.1), Y(-7.9)), (X(10.3), Y(-6.9))], 2), material='claro',
           alto=.4, brillo=.3, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(X(9.3), Y(-7.5), .22, .22), 'E8B952', 1)
    return casco


def basora(l):
    cielo(l, sol=(104, 7.4))
    # dos ríos que se juntan: el de atrás baja entre palmerales y se une al de adelante, que sigue ancho hacia el mar
    lejos = Polygon([(-2, 25.2), (122, 25.2), (122, 28.6), (-2, 28.6)])
    a1 = l.masa(lejos, material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0, arroja=False)
    l.mancha(box(-2, 25.2, 122, 26), '64C8AA', .5, dentro=a1, difuso=.4)
    l.masa(forma([(-2, 25.4), (10, 24.4), (26, 24.8), (40, 24.4), (48, 25.2), (122, 25.2), (122, 23.6), (-2, 23.6)], 1), material='vientre',
           alto=.08, brillo=0, vientre=0, hondo=0, linea=.3, contraluz=.2, arroja=False)
    for x in np.arange(2, 120, 5.6):                                    # el palmeral de la otra orilla, lejos
        palmera(l, x, 24.8, 4.2, 1 if int(x) % 2 else -1, material='lejos', datiles=False)
    lengua = forma([(-2, 28.4), (8, 27.6), (22, 27.8), (34, 28.6), (42, 30), (36, 31.4), (20, 31.6), (-2, 31.8)], 2)   # la punta de tierra
    l.masa(lengua, material='vientre', alto=.15, brillo=0, vientre=0, hondo=0, linea=.35, contraluz=.2, arroja=False)
    for x, h, lado in ((4, 7.6, 1), (10, 8.6, -1), (17, 7.2, 1), (24, 8, -1), (31, 6.4, 1)):
        palmera(l, x, 30, h, lado)
    rio(l, 31.4)
    g = dhow(l, 76, 33.2, 1.0)
    reflejo(l, g, 33.4, .3)
    for x, h, lado in ((112, 9.4, -1), (118, 8, 1)):
        palmera(l, x, 31, h, lado)


# ------------------------------------------------------------------------------------------------ el mar
def mar(l):
    cielo(l, sol=(84, 22.6), tarde=.45)
    nube(l, 34, 8, 16, .55)
    # el golfo: el mar hasta el horizonte, con el camino de luz del sol que se pone
    horizonte = 24.4
    m = l.masa(box(-2, horizonte, 122, 41), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0,
               contraluz=0, arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 3), '64C8AA', .55, dentro=m, difuso=.8)
    rng = np.random.default_rng(6)
    for k in range(26):                                                # el reflejo dorado del sol, en rayitas
        y = horizonte + .6 + k * .6
        w = 1.2 + k * .35
        x = 84 + rng.uniform(-1.4, 1.4) * (1 + k * .08)
        l.trazo([(x - w, y), (x + w, y)], .26, color='F2D48A', alfa=.85 - k * .02)
    for _ in range(18):
        x, y = rng.uniform(2, 116), rng.uniform(horizonte + 2, 39)
        if abs(x - 84) < 8:
            continue
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    # un petrolero en el horizonte: el casco largo y bajo, el puente y la chimenea a popa
    l.masa([forma([(38, horizonte + .4), (57.4, horizonte + .4), (58.4, horizonte - .9), (38.6, horizonte - .7)], 0),
            box(38.8, horizonte - 2.8, 41.6, horizonte - .6), box(39.6, horizonte - 3.8, 40.6, horizonte - 2.6)], material='lejos',
           alto=.15, brillo=0, vientre=0, hondo=0, linea=.25, arroja=False)
    # la última orilla del Shatt al-Arab, con sus palmeras, a la izquierda
    orilla = forma([(-2, 22.8), (8, 22.4), (18, 23.4), (26, 25), (30, 27.8), (24, 30.2), (10, 31.2), (-2, 31.6)], 2)
    l.masa(orilla, material='vientre', alto=.15, brillo=0, vientre=0, hondo=0, linea=.35, contraluz=.25)
    for x, h, lado in ((2, 9.4, 1), (8, 11, -1), (14, 8.6, 1), (20, 9.8, -1), (25, 7.4, 1)):
        palmera(l, x, 28.4 - (x > 22) * 1.6, h, lado)
    # el faro, en la punta de la escollera, a la derecha
    l.masa(forma([(96, horizonte + 1.2), (104, horizonte - 1), (118, horizonte - .4), (122, horizonte + .8), (122, horizonte + 2.4),
                  (96, horizonte + 2.2)], 1), material='lejos', alto=.2, brillo=.05, vientre=0, hondo=0, linea=.35)
    torre = forma([(106.4, horizonte - .6), (107.4, 9.6), (110.6, 9.6), (111.6, horizonte - .6)], 0)
    t = l.masa(torre, material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, linea=.4, escalon=.2, contraluz=.3)
    for y in (13, 17.6):
        l.mancha(box(100, y, 118, y + 2.2), '2F8A74', .85, dentro=t)
    l.masa(box(106.6, 8.4, 111.4, 9.8).buffer(.15), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.masa(box(107.4, 5.6, 110.6, 8.4).buffer(.1), material='acento', alto=.3, brillo=.5, vientre=0, hondo=0, linea=.3)
    l.masa(forma([(106.8, 5.8), (109, 3.4), (111.2, 5.8)], 0), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(ovalo(109, 7, 6, 3.4), 'F2D48A', .35, difuso=1.4)            # la luz del faro
    reflejo(l, torre, horizonte + .2, .25, color='F2D48A')


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Diyarbakır', dibujar=diyarbakir), dict(clave='Mosul', dibujar=mosul),
            dict(clave='Tikrit', dibujar=tikrit), dict(clave='Samarra', dibujar=samarra), dict(clave='Bagdad', dibujar=bagdad),
            dict(clave='Basora', dibujar=basora), dict(clave='mar', dibujar=mar)]
LISTO = True
