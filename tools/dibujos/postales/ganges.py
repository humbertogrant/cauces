# -*- coding: utf-8 -*-
"""Las postales del Ganges, de memoria: una por parada, y la del nacimiento y la del mar, en el orden de POSTALES. Cada una pinta la
«imagen para recordar» de su ciudad (rios.js), con lo que dice el dato del lugar, y sigue la regla del protagonista: la imagen para
recordar va grande y al medio, y es lo único dorado; sin sol, salvo el de Benarés, que sale pálido al amanecer.

- el nacimiento: Gaumukh, «boca de vaca»: la punta del glaciar Gangotri hecha una cara de vaca de hielo, con los cuernos dorados, y el
  río que sale de su boca, la cueva; atrás, el Himalaya;
- Haridwar: «una puerta en la montaña»: una puerta dorada, de columnas y cúpulas, por donde el Ganges sale de los cerros a la llanura;
  los peregrinos en las escaleras y las lámparas que flotan en el río;
- Kanpur: «un perro con zapatos de cuero»: un perro callejero que camina orgulloso con sus cuatro zapatos de cuero, dorados; atrás, las
  curtidurías que tiñen el río y el puente;
- Prayagraj: «tres trenzas de agua»: visto desde arriba, el Ganges claro y el Yamuna oscuro se juntan y se trenzan con el Saraswati,
  que no se ve (solo su borde), y una cinta dorada ata la trenza; en los arenales, la multitud y las carpas del Kumbh Mela;
- Benarés: «escaleras que bajan al agua y fuego al amanecer»: los ghats con sus sombrillas y sus templos, y al pie, en la orilla, el
  fuego dorado en su lámpara; el sol sale pálido detrás de la otra orilla;
- Patna: «Ashoka planta su pata»: el león de Ashoka, dorado, el de su columna, planta la pata frente a la empalizada de madera de
  Pataliputra; atrás, el río ancho y el puente largo;
- Calcuta: «la última puerta antes del mar»: el puente Howrah, de acero, dorado, con sus dos torres como una puerta sobre el Hooghly;
  atrás, el monumento blanco a Victoria, del Raj, y las grúas;
- el mar: la bahía de Bengala y el tigre de Bengala, dorado, en los manglares de los Sundarbans; un barco que pasa (la barca se queda en
  el Hooghly, y Gavi dice que no te bajés del barco).
"""
import math

import numpy as np
from shapely import affinity
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from _postal import (VISTA, agua, arbol, ave, casitas, cebolla_baja, cielo, cinta, cordillera, mangle, nube, orilla, palmera,  # noqa: F401
                     pasto, piedra, prado, reflejo, rio, tierra)
from pintor import curva, forma, ovalo, tubo

PIEL = '93701A'            # el tono de la piel: dorado oscuro sobre el pálido de `vientre`
HIELO = 'A4DCC4'           # el azul verdoso del hielo
CLARO_RIO = 'C6B98A'       # el Ganges claro, de agua turbia
OSCURO_RIO = '1C6659'      # el Yamuna, más verde y oscuro


def persona(l, x, base, s=1.0, ropa='claro', semilla=0):
    """una persona chica, de pie, de frente: el cuerpo con su ropa, la cabeza y el pelo oscuro"""
    rng = np.random.default_rng(semilla)
    m = l.masa([forma([(x - .9 * s, base), (x - 1.1 * s, base - 2.6 * s), (x - .7 * s, base - 4.2 * s), (x + .7 * s, base - 4.2 * s),
                       (x + 1.1 * s, base - 2.6 * s), (x + .9 * s, base)], 1)], material=ropa, alto=.3, brillo=.2, vientre=0, hondo=0, linea=.22,
               arroja=False)
    c = l.masa(ovalo(x, base - 5 * s, .75 * s, .8 * s), material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.2, arroja=False)
    l.mancha(ovalo(x, base - 5 * s, 1 * s, 1 * s), PIEL, .45, dentro=c)
    l.mancha(ovalo(x + rng.uniform(-.1, .1), base - 5.5 * s, .78 * s, .4 * s), '05201C', .9, dentro=c)
    return m


# ------------------------------------------------------------------------------------------------ el nacimiento
def nace(l):
    cielo(l, sol=None)
    nube(l, 22, 5, 12, .5)
    nube(l, 104, 4.4, 10, .45)
    # el Himalaya: las tres Bhagirathi a la izquierda y el Shivling, la pirámide afilada, a la derecha
    cordillera(l, [(-2, 16), (6, 6.4), (12, 9.4), (18, 4.4), (24, 8.6), (30, 5.6), (38, 12), (46, 16)], nieve=10)
    cordillera(l, [(70, 16), (80, 9), (88, 1.2), (96, 9.6), (104, 7.4), (114, 10.6), (122, 9)], nieve=9.6)
    # el suelo de la morena, de piedra suelta, y el glaciar: la lengua de hielo sucio de piedras que baja hasta adelante
    suelo = l.masa(box(-2, 26, 122, 41.5), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
                   arroja=False)
    l.mancha(box(-2, 26, 122, 41.5), '8FA19D', .55, dentro=suelo)
    hielo = forma([(-2, 13.6), (30, 12.4), (90, 12.4), (122, 13.6), (122, 31), (90, 30.4), (60, 33), (30, 30.4), (-2, 31)], 2)
    h = l.masa(hielo, material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35, escalon=.3, contraluz=.3)
    l.mancha(hielo, HIELO, .35, dentro=h)
    rng = np.random.default_rng(2)
    for _ in range(26):                                                 # las grietas
        x, y = rng.uniform(0, 120), rng.uniform(15, 29)
        if 38 < x < 82:
            continue
        l.trazo([(x, y), (x + rng.uniform(1.6, 3), y + rng.uniform(-.5, .5))], .16, color='6BB9A0', alfa=.7, dentro=h)
    for y0 in (17.4, 22.6, 27.4):                                       # las franjas de morena, de piedra suelta
        l.trazo([(x, y0 + 1.2 * math.sin(x / 9)) for x in np.arange(-2, 122, 4)], .5, color='8FA19D', alfa=.45, dentro=h)
    # la cara de vaca de hielo, protagonista: la frente, las orejas, los cuernos dorados, los ojos, el hocico y la boca, que es la cueva
    orejas = [ovalo(40.2, 15.4, 5, 2.2, -18), ovalo(79.8, 15.4, 5, 2.2, 18)]
    o = l.masa(orejas, material='claro', alto=.4, brillo=.2, vientre=0, hondo=0, linea=.4, contraluz=.3)
    l.mancha(unary_union(orejas).buffer(1), HIELO, .45, dentro=o)
    cara = forma([(45, 31), (44.4, 21), (46.4, 14.6), (52, 11.2), (60, 10.4), (68, 11.2), (73.6, 14.6), (75.6, 21), (75, 31)], 2)
    c = l.masa(cara, material='claro', alto=.5, brillo=.25, vientre=0, hondo=.1, linea=.45, escalon=.3, contraluz=.35)
    l.mancha(cara, HIELO, .3, dentro=c)
    for x0, x1 in ((48.6, 40.6), (71.4, 79.4)):                         # los cuernos, dorados, que suben en curva
        l.masa(tubo([(x0, 12.6), ((x0 + x1) / 2 + (x1 - x0) * .1, 7.4), (x1, 3.2)], [1.9, 1.3, .35], 8), material='acento', alto=.5, brillo=.5,
               vientre=0, hondo=0, linea=.4, contraluz=.4)
    for dx in (-7, 7):                                                  # los ojos
        l.mancha(ovalo(60 + dx, 18.6, 1.6, 1.3), '05201C', .95, dentro=c)
        l.mancha(ovalo(60 + dx + .5, 18.2, .45, .4), 'FFFFFF', .9, dentro=c)
    hocico = ovalo(60, 26.6, 11.6, 4.8)
    l.masa(hocico, material='claro', alto=.4, brillo=.3, vientre=0, hondo=0, linea=.35, contraluz=.3)
    for dx in (-4.6, 4.6):                                              # las narinas
        l.mancha(ovalo(60 + dx, 25.4, 1.3, .9, -dx * 3), '0C3A33', .85)
    boca = ovalo(60, 30.4, 6.6, 2.4)
    l.mancha(boca, '05201C', .95)
    l.mancha(ovalo(60, 29.6, 5, 1.2), '164F46', .8)
    # el río que sale de la boca, hacia nosotros, entre las piedras de la morena
    agua(l, cinta([(60, 31), (58.6, 34.4), (61.4, 38), (59.4, 41.6)], [9, 11, 13, 15], 8), ondas=6, semilla=3, linea=.3)
    l.mancha(ovalo(60, 32.6, 7, 1.6), 'FFFFFF', .7, difuso=.4)
    piedras = [ovalo(x, y, r * 1.4, r) for x, y, r in ((10, 35, 2), (22, 38, 2.6), (34, 36, 1.6), (88, 36.4, 1.8), (100, 38.4, 2.6), (112, 35.4, 2),
                                                      (4, 40, 2.4), (116, 40.6, 2.4))]
    l.masa(piedras, material='claro', alto=.5, brillo=.2, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(piedras).buffer(1), '8FA19D', .5)


# ------------------------------------------------------------------------------------------------ Haridwar
def puerta(l, x0, x1, base, alto_):
    """la puerta dorada de Haridwar: dos columnas, el arco lobulado entre ellas, las cúpulas encima y la del medio, más grande"""
    cx = (x0 + x1) / 2
    top = base - alto_
    cols = [box(x0 - 3, top + 6, x0 + 3, base), box(x1 - 3, top + 6, x1 + 3, base)]
    dintel = box(x0 - 3, top + 3, x1 + 3, top + 9)
    arco = dintel.union(box(x0, top + 9, x1, top + 13)).difference(ovalo(cx, top + 15, (x1 - x0) / 2 - .2, 7))
    for k in range(-3, 4):                                              # los lóbulos del arco
        a = math.radians(90 + k * 22)
        arco = arco.difference(ovalo(cx + ((x1 - x0) / 2 - .4) * math.cos(a), top + 15 - 7 * math.sin(a), 1.3, 1.3))
    cupulas = [cebolla_baja(cx, top + 3.2, 3.6), cebolla_baja(x0, top + 3.2, 2.2), cebolla_baja(x1, top + 3.2, 2.2)]
    for x in (x0 + 10, x1 - 10):
        cupulas.append(cebolla_baja(x, top + 3.2, 1.4))
    m = l.masa(cols + [arco] + cupulas, material='acento', alto=.45, brillo=.45, vientre=0, hondo=0, linea=.45, escalon=.2, contraluz=.4)
    for x in (x0, x1):                                                  # las bandas y los nichos de las columnas
        for y in np.arange(top + 11, base - 2, 3.6):
            l.trazo([(x - 3, y), (x + 3, y)], .2, color='6B4E10', alfa=.6, dentro=m)
            l.mancha(forma([(x - .8, y + 2.6), (x - .8, y + 1.2), (x, y + .6), (x + .8, y + 1.2), (x + .8, y + 2.6)], 1), '6B4E10', .55, dentro=m)
    for x in np.arange(x0 + 4, x1 - 3, 3):                              # los arquitos del dintel
        l.mancha(forma([(x - .7, top + 8.2), (x - .7, top + 6.2), (x, top + 5.4), (x + .7, top + 6.2), (x + .7, top + 8.2)], 1), '6B4E10', .5, dentro=m)
    return unary_union(cols + [arco])


def lampara(l, x, y, s=1.0):
    """una lámpara de hoja que flota en el río, con su llamita clara (no dorada: lo dorado es la puerta)"""
    l.masa(ovalo(x, y, 1.2 * s, .45 * s), material='cuerpo', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.18, arroja=False)
    l.mancha(ovalo(x, y - 1 * s, 1.6 * s, 1.4 * s), 'FBEFCB', .45, difuso=.5)
    l.mancha(forma([(x - .3 * s, y - .3 * s), (x, y - 1.6 * s), (x + .3 * s, y - .3 * s)], 1), 'FFFFFF', .95)


def haridwar(l):
    rng = np.random.default_rng(3)
    cielo(l, sol=None)
    nube(l, 24, 4.4, 12, .5)
    nube(l, 100, 4, 10, .45)
    # los cerros del Himalaya que se abren, y el río que sale de entre ellos a la llanura
    cordillera(l, [(-2, 22), (6, 9), (16, 6), (28, 9.4), (40, 13.4), (52, 18), (58, 22)], material='cuerpo')
    cordillera(l, [(62, 22), (68, 18), (80, 13), (92, 8.6), (104, 5.6), (114, 8.4), (122, 20)], material='cuerpo')
    for _ in range(40):
        x = rng.uniform(0, 120)
        y = rng.uniform(10, 21)
        arbol(l, x, y, 1, material='lejos', semilla=int(x * 7))
    prado(l, 21.6, 41, .2)
    agua(l, cinta([(60, 18), (60, 24), (59, 32), (60, 41.6)], [3, 10, 26, 46], 8), ondas=14, semilla=4, linea=.35)
    # las escaleras de los ghats en las dos orillas, con los peregrinos
    for lado in (-1, 1):
        g = Polygon([(60 + lado * 12, 26), (60 + lado * 64, 26), (60 + lado * 64, 41.5), (60 + lado * 25, 41.5)])
        p = piedra(l, g, .3, .35)
        for y in np.arange(27, 41.5, 1.2):
            l.trazo([(60 + lado * (12 + (y - 26) * .85), y), (60 + lado * 64, y)], .1, color='6B4E10', alfa=.45, dentro=p)
        for k in range(9):
            x = 60 + lado * rng.uniform(20, 56)
            y = rng.uniform(29, 40)
            if lado * (x - 60) < 12 + (y - 26) * .85 + 2:
                continue
            persona(l, x, y, rng.uniform(.8, 1.1), ('claro', 'cuerpo', 'lejos')[k % 3], semilla=k)
    # la puerta dorada, protagonista, por donde el río sale de la montaña
    puerta(l, 38, 82, 31.4, 27.4)
    for x, y in ((50, 33), (58, 36.4), (67, 34.4), (73, 38), (46, 38.6), (62, 39.8)):
        lampara(l, x, y, 1)


# ------------------------------------------------------------------------------------------------ Kanpur
def zapato(x, y, s=1.0, lado=1):
    """un zapato de cuero visto de costado, con la punta hacia `lado`"""
    return forma([(x - lado * 1.2 * s, y - 1.6 * s), (x + lado * .6 * s, y - 1.6 * s), (x + lado * .9 * s, y - .9 * s), (x + lado * 2.4 * s, y - .6 * s),
                  (x + lado * 2.6 * s, y), (x - lado * 1.4 * s, y), (x - lado * 1.5 * s, y - .8 * s)], 1)


def perro(l, x, base, s=1.0):
    """un perro callejero, flaco y orgulloso, que camina de perfil hacia la derecha con sus cuatro zapatos de cuero dorados: las orejas
    paradas, el hocico largo y la cola enroscada arriba; (x, base) es el suelo bajo el medio del cuerpo"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    pies = ((-6.6, 0), (-3.6, 0), (4, 0), (7, 0))
    lejos = [tubo(P([(-5.4, -7.6), (-4.6, -4), (-3.6, -1.6)]), [1.4 * s, .9 * s, .7 * s], 5), tubo(P([(5, -7.4), (6.6, -4), (7, -1.6)]), [1.2 * s, .8 * s, .7 * s], 5)]
    l.masa(lejos, material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.3), '9DB9B0', .5)
    cuerpo = [O(0, -9.6, 7.4, 3.2), O(6, -10, 3, 3.2), tubo(P([(-6.6, -9), (-7.2, -4), (-6.6, -1.6)]), [1.6 * s, 1 * s, .8 * s], 5),
              tubo(P([(4, -8.4), (4.2, -4), (4, -1.6)]), [1.4 * s, .9 * s, .8 * s], 5),
              tubo(P([(7.6, -11.4), (9.6, -14.6), (10.8, -16)]), [2.2 * s, 1.8 * s, 1.6 * s], 6), O(11.4, -16.6, 2.3, 1.9),
              forma(P([(12.4, -17.6), (16.6, -16.2), (16.8, -15), (12.8, -14.6)]), 1),
              Polygon(P([(9.8, -17.4), (10.4, -21.4), (11.8, -18)])), Polygon(P([(11.4, -18), (12.8, -21.6), (13.4, -17.8)])),
              tubo(P([(-7, -10.4), (-9.6, -13.4), (-8.6, -16.4), (-6.4, -16.2), (-6.4, -14.4)]), [1.2 * s, 1 * s, .9 * s, .7 * s, .4 * s], 8)]
    c = l.masa(cuerpo, material='claro', alto=.5, brillo=.25, vientre=0, hondo=.1, linea=.4, contraluz=.35)
    l.mancha(unary_union(cuerpo).buffer(1), 'E8B952', .14, dentro=c)
    l.mancha(O(12.4, -17.4, .45, .45), '05201C', 1)                     # el ojo
    l.mancha(O(16.6, -15.6, .6, .5), '05201C', 1)                       # la nariz
    l.trazo(P([(13.4, -14.8), (15, -14.6)]), .12 * s, color='0C3A33', alfa=.8)
    # los cuatro zapatos de cuero, dorados, con sus cordones
    zs = [zapato(x + u * s, base + v * s, s, 1) for u, v in pies]
    z = l.masa(zs, material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.35, contraluz=.35)
    for u, v in pies:
        l.trazo([(x + (u - .6) * s, base - 1.4 * s), (x + (u + .5) * s, base - 1.1 * s)], .12 * s, color='6B4E10', alfa=.9, dentro=z)
        l.trazo([(x + (u - 1.3) * s, base - .25 * s), (x + (u + 2.5) * s, base - .25 * s)], .12 * s, color='6B4E10', alfa=.7, dentro=z)
    return c


def kanpur(l):
    rng = np.random.default_rng(5)
    cielo(l, sol=None)
    nube(l, 30, 4.4, 12, .45)
    # enfrente, las curtidurías con sus chimeneas, sus caños y el puente de hierro
    prado(l, 15, 22, .18)
    for x, w, h in ((4, 10, 5), (18, 12, 6), (86, 12, 5.4), (102, 14, 6)):
        f = l.masa(box(x, 18.4 - h, x + w, 18.6), material='claro', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)
        for k in range(int(w // 2.4)):
            l.mancha(box(x + .8 + k * 2.4, 18.4 - h + 1.2, x + 1.8 + k * 2.4, 18.4 - h + 2.4), '164F46', .7, dentro=f)
        l.masa(box(x + w - 2, 18.4 - h - 6, x + w - .8, 18.4 - h), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
        for k in range(3):
            l.mancha(ovalo(x + w - 1.4 - k * 2, 18.4 - h - 7.4 - k * 1.2, 1.2 + k * .4, .9 + k * .3), 'FFFFFF', .6 - k * .12, difuso=.4)
    l.masa(box(30, 16.6, 84, 17.6), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.3)       # el puente
    for x in np.arange(30, 84, 4.5):
        l.trazo([(x, 16.8), (x + 2.25, 13.6), (x + 4.5, 16.8)], .2, color='164F46', alfa=.85)
    l.trazo([(30, 13.6), (84, 13.6)], .22, color='164F46', alfa=.85)
    a = rio(l, 18.6)
    for x0 in (8, 24, 92, 108):                                          # lo que tiñe el río: manchas que salen de los caños
        l.mancha(forma([(x0, 18.6), (x0 + 3, 21), (x0 + 6, 25), (x0 + 2, 26.6), (x0 - 2, 22)], 2), '5A3E1E', .45, dentro=a, difuso=1)
        l.mancha(forma([(x0 + 2, 19.4), (x0 + 5, 22.6), (x0 + 9, 24.4), (x0 + 6, 25.6), (x0 + 1, 22)], 2), '3F3A5A', .35, dentro=a, difuso=1)
    # la orilla de adelante y el perro con zapatos de cuero, protagonista
    m = orilla(l, forma([(-2, 41.5), (-2, 28.4), (30, 27.4), (60, 27.2), (90, 27.4), (122, 28.4), (122, 41.5)], 2), tinte=.26)
    pasto(l, 0, 120, 29, 40.6, 22, semilla=6, dentro=m)
    l.mancha(ovalo(61, 37.8, 12, 1.2), '0C3A33', .22, difuso=.6)
    perro(l, 58, 37.8, 1.12)


# ------------------------------------------------------------------------------------------------ Prayagraj
def trenza(l, x, y0, y1, ancho):
    """una trenza de tres hebras de agua, como una trenza de pelo: gajos que se cruzan de un lado al otro; la del Ganges, clara, la del
    Yamuna, oscura, y la del Saraswati, que no se ve: solo su borde de puntos"""
    paso = (y1 - y0) / 8
    for k in range(9):
        y = y0 + k * paso
        lado = 1 if k % 2 else -1
        g = ovalo(x + lado * ancho * .2, y, ancho * .42, paso * .78, lado * -34)
        cual = k % 3
        if cual == 2:                                                    # el Saraswati, invisible: solo el borde, punteado
            c = np.array(g.exterior.coords)
            for i in range(0, len(c) - 4, 6):
                l.trazo([tuple(c[i]), tuple(c[i + 3])], .32, color='FFFFFF', alfa=.95)
            continue
        m = l.masa(g, material='lejos', alto=.45, brillo=.35, vientre=0, hondo=0, linea=.4, contraluz=.3)
        l.mancha(g.buffer(.5), (CLARO_RIO, OSCURO_RIO)[cual], .72, dentro=m)
        l.trazo([(x + lado * ancho * .05, y - paso * .3), (x + lado * ancho * .32, y + paso * .2)], [.08, .22, .08], color='FFFFFF', alfa=.6, dentro=m)


def prayagraj(l):
    rng = np.random.default_rng(7)
    cielo(l, sol=None)
    nube(l, 30, 3, 12, .45)
    # visto desde arriba: los arenales, el Ganges claro que llega por la izquierda y el Yamuna oscuro por la derecha
    tierra(l, 6, 41, desierto=.34)
    ganga = cinta([(-2, 9), (18, 10.4), (36, 12.4), (50, 13.4), (57, 13.6)], [7, 7.6, 8, 8, 7], 8)
    yamuna = cinta([(122, 9), (102, 10.4), (84, 12.4), (70, 13.4), (63, 13.6)], [7, 7.6, 8, 8, 7], 8)
    for g, color in ((ganga, CLARO_RIO), (yamuna, OSCURO_RIO)):
        m = agua(l, g, material='lejos', ondas=6, semilla=8, linea=.3)
        l.mancha(g, color, .7, dentro=m)
    # la cola de la trenza, abajo: el río juntado que sigue, ya mezclado
    cola = forma([(56.4, 33.6), (63.6, 33.6), (70, 37.6), (76, 41.6), (44, 41.6), (50, 37.6)], 2)
    c = agua(l, cola, ondas=4, semilla=9, linea=.35)
    l.mancha(cola, CLARO_RIO, .35, dentro=c)
    # la trenza de tres aguas, y la gomita dorada que la ata, protagonista
    trenza(l, 60, 13.6, 31.4, 14)
    l.masa([box(53.6, 31.4, 66.4, 34.4).buffer(.6), ovalo(60, 32.9, 7.4, 2.2)], material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.45,
           contraluz=.4)
    l.trazo([(54, 32.2), (66, 32.2)], [.06, .2, .06], color='FBEFCB', alfa=.85)
    # la multitud del Kumbh Mela en los arenales: filas de carpas y gente, muchísima
    for _ in range(70):
        x, y = rng.uniform(1, 119), rng.uniform(19, 40)
        if 40 < x < 80:
            continue
        if rng.random() < .3:
            l.masa(Polygon([(x - 1.6, y), (x, y - 2.2), (x + 1.6, y)]), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.2,
                   arroja=False)
        else:
            for k in range(4):
                xx, yy = x + rng.uniform(-2, 2), y + rng.uniform(-1, 1)
                l.mancha(ovalo(xx, yy, .5, .5), ('0C3A33', '2F8A74', 'FFFFFF', '5A3E1E')[k], .85)
    for x, y in ((30, 11.6), (90, 11.6)):                                # las barcas de los peregrinos
        l.masa(forma([(x - 3, y - .4), (x + 3, y - .4), (x + 2.2, y + .8), (x - 2.2, y + .8)], 1), material='vientre', alto=.2, brillo=.15,
               vientre=0, hondo=0, linea=.25)


# ------------------------------------------------------------------------------------------------ Benarés
def sombrilla(l, x, y, r=3.0):
    """una sombrilla de los ghats, de hoja de palma, en su palo"""
    l.trazo([(x, y), (x, y + 4)], .25, color='5A3E1E', alfa=.9)
    l.masa(forma([(x - r, y + .4), (x, y - r * .5), (x + r, y + .4), (x, y)], 1), material='claro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.3)


def fuego(l, x, base, s=1.0):
    """el fuego dorado en su lámpara de bronce: el cuenco en su pie y las llamas altas"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    l.mancha(ovalo(x, base - 9 * s, 9 * s, 9 * s), 'F2D48A', .35, difuso=2.4)
    pie = [forma(P([(-2.4, 0), (-1, -1), (-.6, -4), (.6, -4), (1, -1), (2.4, 0)]), 1), forma(P([(-4.6, -4), (4.6, -4), (3.6, -6.6), (-3.6, -6.6)]), 1)]
    llamas = [forma(P([(-4, -6.4), (-4.6, -9), (-3, -13), (-2.4, -10.6), (-1.4, -15), (0, -19.6), (1.2, -14.6), (2.6, -16.4), (2.8, -12),
                       (4.4, -10.4), (4.2, -6.4)]), 2)]
    m = l.masa(pie + llamas, material='acento', alto=.4, brillo=.5, vientre=0, hondo=0, linea=.4, contraluz=.4)
    l.mancha(forma(P([(-2, -6.6), (-1.6, -10), (0, -14.4), (1.4, -10.4), (2, -6.6)]), 2), 'FBEFCB', .9, dentro=m)    # el centro claro
    return m


def benares(l):
    rng = np.random.default_rng(9)
    cielo(l, sol=None, tarde=.35)
    # el sol que sale, pálido, detrás de la otra orilla
    l.mancha(ovalo(102, 15.4, 8, 6), 'FBEFCB', .45, difuso=2)
    l.mancha(ovalo(102, 16, 3.4, 3.4), 'F2D48A', .6)
    l.masa(forma([(70, 17.4), (122, 16.8), (122, 18.6), (70, 18.6)], 1), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0, linea=.25)
    a = rio(l, 18.4)
    l.mancha(cinta([(102, 18.6), (101, 26), (103, 34), (101, 41)], [3, 4, 5, 6], 6), 'FBEFCB', .35, dentro=a, difuso=.8)   # el brillo del sol
    # los ghats: las escaleras de piedra que bajan al agua, con los templos y los palacios arriba
    tierra_g = Polygon([(-2, 6), (66, 14), (82, 31), (88, 41.5), (-2, 41.5)])
    p = piedra(l, tierra_g, .32, .4)
    for y in np.arange(16, 41.5, 1.1):                                   # los escalones
        x1 = 66 + (y - 14) * (16 / 17) if y < 31 else 82 + (y - 31) * .6
        l.trazo([(-2, y), (x1, y)], .1, color='6B4E10', alfa=.45, dentro=p)
    for x, w, h, torre in ((2, 10, 9, True), (13, 9, 7, False), (23, 11, 10, True), (35, 9, 7, False), (45, 10, 8, True)):
        y0 = 8 + x * .1
        e = piedra(l, [box(x, y0 - h + 6, x + w, y0 + 6)], .25, .35)
        for k in range(int(w // 2.2)):
            l.mancha(forma([(x + 1 + k * 2.2, y0 + 4), (x + 1 + k * 2.2, y0 + 2.4), (x + 1.5 + k * 2.2, y0 + 1.8), (x + 2 + k * 2.2, y0 + 2.4),
                            (x + 2 + k * 2.2, y0 + 4)], 1), '0C3A33', .65, dentro=e)
        if torre:                                                        # el shikhara del templo, la torre en punta
            piedra(l, forma([(x + w * .3, y0 - h + 6.2), (x + w * .38, y0 - h + 2), (x + w / 2, y0 - h - 1.6), (x + w * .62, y0 - h + 2),
                             (x + w * .7, y0 - h + 6.2)], 1), .3, .3)
    for x, y in ((12, 22), (28, 25), (44, 21), (20, 32), (38, 33.4)):
        sombrilla(l, x, y, 3.2)
    for k in range(14):
        x, y = rng.uniform(4, 64), rng.uniform(24, 40)
        persona(l, x, y, rng.uniform(.8, 1.05), ('claro', 'cuerpo', 'acento' if False else 'lejos')[k % 3], semilla=k)
    for x, y in ((92, 30), (106, 36)):                                   # las barcas de los peregrinos
        l.masa([forma([(x - 5, y - .6), (x + 5, y - .6), (x + 4, y + .8), (x - 4, y + .8)], 1), box(x - 2.4, y - 2.6, x + 2.4, y - .5)],
               material='vientre', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # el fuego dorado al amanecer, protagonista, en su plataforma al pie de los ghats
    piedra(l, box(52, 33, 74, 36.4), .35, .4)
    fuego(l, 63, 33.2, 1.25)


# ------------------------------------------------------------------------------------------------ Patna
def leon(l, x, base, s=1.0):
    """el león de la columna de Ashoka, dorado, que camina hacia la izquierda y planta la pata de adelante: la melena en rulos, la cara,
    la cola con su borla; (x, base) es el suelo bajo el medio del cuerpo"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    lejos = [tubo(P([(-5, -8), (-6.4, -4), (-6.2, 0)]), [1.8 * s, 1.3 * s, 1.2 * s], 5), tubo(P([(6, -8), (6.6, -4), (6.2, 0)]), [1.8 * s, 1.3 * s, 1.2 * s], 5)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.3), '6B4E10', .35)
    cuerpo = [O(1.6, -9.4, 8.6, 3.8), tubo(P([(-4.4, -8.4), (-8.4, -4.2), (-9.4, 0)]), [2 * s, 1.6 * s, 1.5 * s], 5),
              tubo(P([(7.6, -8.6), (8.6, -4.4), (8.4, 0)]), [2 * s, 1.5 * s, 1.4 * s], 5),
              tubo(P([(9.6, -10), (13.4, -12.6), (15.4, -10.4), (16.6, -12.6)]), [.8 * s, .6 * s, .5 * s, .4 * s], 8), O(17, -13, 1.2, 1.1)]
    c = l.masa(cuerpo, material='acento', alto=.55, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    melena = [O(-5.6 + 2.6 * math.cos(math.radians(a)), -13 + 3.4 * math.sin(math.radians(a)), 1.6, 1.4) for a in range(0, 360, 30)]
    m = l.masa(melena + [O(-5.6, -13, 4, 4.4)], material='acento', alto=.5, brillo=.4, vientre=0, hondo=0, linea=.45, contraluz=.35)
    for a in range(0, 360, 30):                                          # los rulos de la melena
        cx, cy = x + (-5.6 + 2.6 * math.cos(math.radians(a))) * s, base + (-13 + 3.4 * math.sin(math.radians(a))) * s
        l.trazo([(cx - .5 * s, cy), (cx, cy - .5 * s), (cx + .5 * s, cy)], .14 * s, color='6B4E10', alfa=.7, dentro=m)
    cara = l.masa([O(-8.6, -12.6, 2.6, 2.4), O(-10.4, -11.2, 1.6, 1.3)], material='acento', alto=.5, brillo=.5, vientre=0, hondo=0, linea=.4,
                  contraluz=.4)
    l.mancha(O(-9.2, -13.6, .45, .38), '05201C', 1)
    l.mancha(O(-11.6, -11.6, .5, .4), '5A3E1E', .9)
    l.trazo(P([(-11.6, -10.4), (-10, -10), (-9, -10.6)]), .14 * s, color='5A3E1E', alfa=.8, dentro=cara)
    for dx in (-1.2, 0, 1.2):                                            # las garras de la pata plantada
        l.trazo(P([(-9.4 + dx * .5, -.2), (-9.6 + dx * .6, .4)]), .14 * s, color='6B4E10', alfa=.9)
    return c


def patna(l):
    rng = np.random.default_rng(11)
    cielo(l, sol=None)
    nube(l, 22, 4.4, 12, .5)
    nube(l, 100, 3.6, 10, .4)
    # atrás, el río ancho, los campos de la otra orilla y el puente largo
    prado(l, 12, 16, .3)
    a = rio(l, 15.4)
    l.masa(box(-2, 13.6, 122, 14.8), material='vientre', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25)
    for x in np.arange(2, 122, 5.2):
        l.masa(box(x - .5, 14.6, x + .5, 17.6), material='vientre', alto=.15, brillo=.1, vientre=0, hondo=0, linea=.2)
    # la empalizada de madera de Pataliputra, con sus torres y su puerta
    m = orilla(l, forma([(-2, 41.5), (-2, 22.6), (60, 21.6), (122, 22.6), (122, 41.5)], 2), tinte=.3)
    troncos = []
    for x in np.arange(-1, 122, 1.5):
        if 54 < x < 66:
            continue
        troncos.append(Polygon([(x - .7, 27.6), (x - .7, 19.8), (x, 18.8), (x + .7, 19.8), (x + .7, 27.6)]))
    for x in (8, 32, 88, 112):
        troncos += [box(x - 2.6, 15.6, x + 2.6, 27.6), Polygon([(x - 3.4, 15.8), (x, 12.6), (x + 3.4, 15.8)])]
    for x in (54.6, 65.4):
        troncos += [box(x - 2, 14.6, x + 2, 27.6), Polygon([(x - 2.8, 14.8), (x, 11.6), (x + 2.8, 14.8)])]
    t = l.masa(troncos, material='vientre', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.35)
    l.mancha(box(-2, 11, 122, 28), '8A6A3A', .5, dentro=t)
    for y in (21.4, 25.4):
        l.trazo([(-2, y), (122, y)], .3, color='5A3E1E', alfa=.6, dentro=t)
    pasto(l, 0, 120, 29, 40.6, 18, semilla=12, dentro=m)
    # la huella y el polvo donde planta la pata
    for k in range(5):
        l.mancha(ovalo(48 - k * 2.6, 36.6 - k * .5, 1.6 + k * .3, .8 + k * .2), 'FFFFFF', .55 - k * .08, difuso=.4)
    l.mancha(ovalo(54.4, 37.8, 4.4, 1), '0C3A33', .25, difuso=.5)
    for a in (-160, -130, -50, -20):
        r = math.radians(a)
        l.trazo([(54.6 + 3 * math.cos(r), 37.6 + 1 * math.sin(r)), (54.6 + 5.4 * math.cos(r), 37.6 + 1.8 * math.sin(r))], .2, color='6B4E10', alfa=.6)
    # el león de Ashoka, protagonista, que planta la pata frente a la puerta
    leon(l, 63.6, 37.8, 1.25)


# ------------------------------------------------------------------------------------------------ Calcuta
def howrah(l, base, alto_):
    """el puente Howrah, dorado: dos torres de acero y las cerchas en voladizo que se juntan al medio, con el tablero colgado"""
    torres = (30, 90)
    tope = base - alto_
    def cordon(x):                                                       # la cuerda de arriba de las cerchas
        t = min(abs(x - c) for c in torres)
        if 30 <= x <= 90:
            return tope + 1.6 + (t / 30) ** 1.4 * 9.6
        return tope + 1.6 + (t / 32) ** 1.2 * 10.6
    piezas = []
    for c in torres:
        piezas += [box(c - 2.6, tope, c - 1, base + 4), box(c + 1, tope, c + 2.6, base + 4), box(c - 2.6, tope, c + 2.6, tope + 1.6),
                   box(c - 2.6, tope + 9, c + 2.6, tope + 10)]
    xs = np.arange(-2, 122.1, 1)
    piezas.append(cinta([(x, cordon(x)) for x in xs], [1.1] * len(xs), 2))
    piezas.append(box(-2, base - 1.2, 122, base))                        # el tablero
    m = l.masa(piezas, material='acento', alto=.4, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.35)
    paso = 3
    for x in np.arange(-2, 122, paso):                                   # los montantes y las diagonales
        y0, y1 = cordon(x), cordon(x + paso)
        l.trazo([(x, y0), (x, base - 1)], .3, color='BF9129', alfa=.95)
        l.trazo([(x, y0), (x + paso, base - 1)], .22, color='BF9129', alfa=.9)
        l.trazo([(x, y0 + .2), (x + paso, y1 + .2)], .2, color='6B4E10', alfa=.6)
    return m


def calcuta(l):
    rng = np.random.default_rng(13)
    cielo(l, sol=None)
    nube(l, 20, 4, 12, .45)
    nube(l, 104, 3.4, 10, .4)
    # atrás, la ciudad: el monumento a Victoria, de mármol blanco, los edificios altos y las grúas del puerto
    prado(l, 17, 24, .2)
    v = l.masa([box(4, 12.6, 24, 18.6), ovalo(14, 12.8, 4.6, 4), box(4.4, 10.6, 7.4, 12.8), box(20.6, 10.6, 23.6, 12.8)], material='claro', alto=.35,
               brillo=.3, vientre=0, hondo=0, linea=.3)
    l.masa(Polygon([(13.4, 9), (14, 6.6), (14.6, 9)]), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2)
    for x, h in ((36, 8), (42, 11), (48, 7), (72, 9), (78, 12), (84, 8)):
        e = l.masa(box(x - 2, 18.6 - h, x + 2, 18.8), material='claro', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25, arroja=False)
        for y in np.arange(18.6 - h + .8, 18.4, 1.1):
            l.trazo([(x - 1.6, y), (x + 1.6, y)], .08, color='8EB5AA', alfa=.8, dentro=e)
    for x in (98, 104, 110):
        l.masa([box(x - .3, 10, x + .3, 18.8), Polygon([(x, 10), (x + 4, 9.2), (x + 4, 9.6), (x, 10.8)])], material='lejos', alto=.2, brillo=.1,
               vientre=0, hondo=0, linea=.2)
    a = rio(l, 19.6)
    for x, y in ((14, 32), (100, 34.6)):                                 # las barcas del Hooghly
        l.masa([forma([(x - 5, y - .8), (x + 5, y - .8), (x + 4, y + .8), (x - 4, y + .8)], 1), box(x - 1.4, y - 2.8, x + 2, y - .7)],
               material='vientre', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # el puente Howrah, protagonista: la última puerta antes del mar
    g = howrah(l, 26.6, 22)
    reflejo(l, box(-2, 4.6, 122, 26.6).intersection(unary_union([box(27.4, 4.6, 32.6, 30), box(87.4, 4.6, 92.6, 30)])), 30.4, .2)


# ------------------------------------------------------------------------------------------------ el mar
def tigre(l, x, base, s=1.0):
    """el tigre de Bengala, dorado con sus rayas oscuras, de perfil, que camina hacia la izquierda por el barro del manglar: la cabeza
    grande con sus mejillas blancas, las patas fuertes y la cola larga; (x, base) es el suelo bajo el medio"""
    P = lambda pts: [(x + u * s, base + v * s) for u, v in pts]
    O = lambda u, v, rx, ry, a=0: ovalo(x + u * s, base + v * s, rx * s, ry * s, a)
    lejos = [tubo(P([(-6, -7.6), (-7.4, -3.6), (-7, 0)]), [2 * s, 1.5 * s, 1.4 * s], 5), tubo(P([(6.4, -8), (7.6, -4), (7.4, 0)]), [2 * s, 1.5 * s, 1.4 * s], 5)]
    l.masa(lejos, material='acento', alto=.3, brillo=.15, vientre=0, hondo=0, linea=.3)
    l.mancha(unary_union(lejos).buffer(.3), '6B4E10', .4)
    cuerpo = [O(1, -9, 9.6, 4.2), tubo(P([(-5.2, -8.4), (-9.6, -4.2), (-10.4, 0)]), [2.2 * s, 1.8 * s, 1.7 * s], 5),
              tubo(P([(8.4, -8.6), (9.2, -4.4), (9, 0)]), [2.2 * s, 1.7 * s, 1.6 * s], 5),
              tubo(P([(10.4, -10.4), (15, -11.6), (19, -9.4), (21.4, -10.6)]), [1.1 * s, .9 * s, .8 * s, .7 * s], 8),
              O(-10.4, -12.6, 3.8, 3.4), O(-13.2, -11.2, 2, 1.6), O(-8.6, -15.6, 1, 1)]
    c = l.masa(cuerpo, material='acento', alto=.55, brillo=.45, vientre=0, hondo=.1, linea=.45, contraluz=.4)
    l.mancha(O(-2, -6.4, 9, 1.6), 'FBEFCB', .7, dentro=c)               # la panza clara
    l.mancha(O(-11.4, -10.8, 2.6, 1.6), 'FFFFFF', .85, dentro=c)        # las mejillas blancas
    l.mancha(O(-12.6, -14, .9, .6), 'FFFFFF', .6, dentro=c)
    rng = np.random.default_rng(3)
    for u in np.arange(-6, 10, 1.9):                                     # las rayas
        l.trazo(P([(u, -13), (u + rng.uniform(-.8, .8), -10.4), (u + rng.uniform(-.4, .4), -7.6)]), [.2, .5, .1], color='05201C', alfa=.85, dentro=c)
    for u in np.arange(12, 21, 2):
        l.trazo(P([(u, -12.4), (u + .2, -9.4)]), .4, color='05201C', alfa=.85, dentro=c)
    for v in (-15, -13.6):
        l.trazo(P([(-10.4, v), (-8.4, v + .4)]), [.1, .3], color='05201C', alfa=.8, dentro=c)
    l.mancha(O(-11.6, -13.4, .5, .4), '05201C', 1)                      # el ojo
    l.mancha(O(-15, -11.6, .6, .45), '5A3E1E', 1)                       # la nariz
    return c


def mar(l):
    rng = np.random.default_rng(15)
    cielo(l, sol=None)
    nube(l, 26, 6, 16, .5)
    nube(l, 94, 5, 12, .45)
    # la bahía de Bengala, al fondo, con un barco que pasa
    horizonte = 17.4
    m = l.masa(box(-2, horizonte, 122, 41.5), material='lejos', alto=.05, brillo=0, vientre=0, hondo=0, tinta=False, escalon=0, contraluz=0,
               arroja=False)
    l.mancha(box(-2, horizonte, 122, horizonte + 2), '64C8AA', .5, dentro=m, difuso=.8)
    for _ in range(18):
        x, y = rng.uniform(2, 118), rng.uniform(horizonte + 2, 40)
        l.trazo([(x, y), (x + 3, y - .25), (x + 6, y)], .16, color='A4DCC4', alfa=.7)
    l.masa([forma([(84, horizonte - .4), (106, horizonte - .4), (108, horizonte - 2), (83, horizonte - 2)], 1), box(86, horizonte - 4.6, 92, horizonte - 1.9),
            box(88, horizonte - 6.6, 89.4, horizonte - 4.4)], material='lejos', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.25)
    # los Sundarbans: los islotes de barro con sus manglares, a los costados y atrás
    for x0, x1, y in ((-2, 34, 24), (86, 122, 23), (-2, 22, 34), (100, 122, 33)):
        l.masa(forma([(x0, y + .8), (x0 + 2, y - .6), (x1 - 2, y - .6), (x1, y + .8)], 1), material='vientre', alto=.1, brillo=0, vientre=0, hondo=0,
               linea=.25)
        for x in np.arange(x0 + 3, x1 - 2, 5.4):
            mangle(l, x + rng.uniform(-1, 1), y, rng.uniform(7, 10), semilla=int(x * 3))
    # el banco de barro del medio, y el tigre de Bengala, protagonista
    banco = forma([(30, 37.6), (40, 33.4), (80, 33), (92, 37.4), (80, 39.4), (40, 39.6)], 2)
    b = l.masa(banco, material='vientre', alto=.15, brillo=.05, vientre=0, hondo=0, linea=.3)
    l.mancha(banco, '8A6A3A', .35, dentro=b)
    for x in (36, 86):
        mangle(l, x, 36.6, 9.6, semilla=x)
    t = tigre(l, 62, 36.6, 1.12)
    reflejo(l, t.g, 37, .25)


POSTALES = [dict(clave='nace', dibujar=nace), dict(clave='Haridwar', dibujar=haridwar), dict(clave='Kanpur', dibujar=kanpur),
            dict(clave='Prayagraj', dibujar=prayagraj), dict(clave='Benarés', dibujar=benares), dict(clave='Patna', dibujar=patna),
            dict(clave='Calcuta', dibujar=calcuta), dict(clave='mar', dibujar=mar)]
LISTO = True
