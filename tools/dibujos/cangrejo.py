# -*- coding: utf-8 -*-
"""Pinzas, un cangrejo del manglar, de memoria y de frente (un poco desde arriba): el caparazón ancho y abombado, casi cuadrado
de esquinas redondas, con dientecitos en los bordes de adelante y el surco en forma de H en el lomo; los dos ojos arriba de
pedúnculos cortos, que salen de sus cuencas en el borde de adelante; la boca tapada por dos placas, como una puerta; dos tenazas
grandes adelante (doradas, como en la ilustración de antes), con dientes en el borde de los dedos; y cuatro patas para caminar a cada
lado, gruesas, chatas y articuladas (el muslo sube hasta la rodilla y el resto baja al suelo en tres tramos, con la punta en uña y
algunos pelos), que se abren en abanico hacia los costados: por eso camina de lado.
"""
import numpy as np

from pintor import forma, ovalo, tubo

VISTA = (0, 8, 120, 80)
SUELO = 80.0

# las patas del lado izquierdo, de adelante (0) hacia atrás (3): nacimiento, rodilla, tobillo y punta; las del derecho, en espejo
PATAS = [((35, 53.4), (23, 44), (16.4, 62.4), (14.6, 79.4)),
         ((35, 51), (20.4, 40), (11.8, 57.4), (8.8, 76.4)),
         ((35.6, 48.6), (19.6, 36.4), (8.8, 51.4), (4.4, 71.6)),
         ((36.6, 46.2), (25, 35.6), (18.6, 44.8), (15.4, 62.4))]


def espejo(p, lado):
    return p if lado < 0 else (120 - p[0], p[1])


def pata(i, lado):
    b, r, t, p = [np.array(espejo(q, lado)) for q in PATAS[i]]
    k = 1 - .1 * i
    tramos = [tubo([b, (b + r) / 2 + [0, -.8], r], [3.4 * k, 3.3 * k, 2.8 * k], 8),        # el muslo, ancho y chato
              tubo([r, t], [2.6 * k, 2.2 * k], 8),
              tubo([t, t + (p - t) * .5, p], [2.0 * k, 1.5 * k, .35], 8)]                   # la punta, en uña
    return tramos, (r, t, p)


def caparazon():
    return forma([(60, 29.6), (70.6, 30.4), (80, 33.4), (87.4, 38.4), (91.4, 44.4), (91, 50.4), (86.6, 55.4), (76, 58.8), (60, 60),
                  (44, 58.8), (33.4, 55.4), (29, 50.4), (28.6, 44.4), (32.6, 38.4), (40, 33.4), (49.4, 30.4)], 3)


def tenaza(lado):
    s = -1 if lado < 0 else 1
    x = lambda v: 60 + s * v
    brazo = tubo([(x(21), 56), (x(24.4), 62), (x(19.6), 66.6)], [3.2, 3.0, 2.8])
    palma = forma([(x(20.6), 63), (x(15.4), 62.4), (x(10.8), 64), (x(8.4), 67.8), (x(9.6), 72), (x(14), 74.2), (x(19.2), 73),
                   (x(22), 69)], 3)
    fijo = forma([(x(10.6), 69.2), (x(6.4), 70), (x(3.2), 70.8), (x(1.4), 70.4), (x(3), 72.2), (x(7), 73), (x(10.8), 72.8)], 2)
    movil = forma([(x(10.4), 66.2), (x(6.8), 65), (x(3.6), 65.4), (x(1.8), 67), (x(3.8), 67.2), (x(7), 68), (x(10.2), 68.8)], 2)
    return [brazo, palma], [fijo, movil]


def dibujar(l):
    rng = np.random.default_rng(5)
    for i in (3, 2, 1, 0):                              # de atrás hacia adelante: las de atrás, más lejos y más oscuras
        for lado in (-1, 1):
            tramos, (r, t, p) = pata(i, lado)
            m = l.masa(tramos, material='lejos' if i > 1 else 'cuerpo', alto=.5, brillo=.18, vientre=0, linea=.7, hondo=0)
            for q, a in ((r, 2.4), (t, 1.9)):           # las articulaciones: un anillo más oscuro
                l.mancha(ovalo(q[0], q[1], a * (1 - .1 * i), a * .55 * (1 - .1 * i), 90 if q is r else 20), '0C3A33', .22,
                         dentro=m, difuso=.3)
            for _ in range(5):                          # algunos pelos cortos en el borde
                f = rng.uniform(.15, .85)
                q = r + (t - r) * f
                d = (t - r) / np.linalg.norm(t - r)
                n = np.array([d[1], -d[0]]) * (-1 if lado < 0 else 1)
                l.trazo([q + n * 1.2, q + n * 2.4 + d * .6], [.14, .04], alfa=.55)
    cap = l.masa(caparazon() .union(forma([(44, 57), (76, 57), (74, 61.4), (46, 61.4)], 2)), brillo=.3, vientre=.25, linea=.85,
                 bultos=[(ovalo(60, 40, 24, 9), .45), (ovalo(46, 45, 9, 7), .2), (ovalo(74, 45, 9, 7), .2)])
    for lado in (-1, 1):                                                # los dientecitos del borde de adelante, apenas marcados
        for (x, y), (x2, y2) in (((32.6, 38.6), (34.6, 39.6)), ((30, 42.8), (32.2, 43.4)), ((28.8, 47), (31, 47.2))):
            l.trazo([espejo((x, y), lado), espejo((x2, y2), lado)], [.35, .08], alfa=.5, dentro=cap)
    # el surco en forma de H del lomo, los granitos, y el borde de adelante con las cuencas de los ojos
    for p in (((51.4, 33.4), (53.6, 38.4), (52.8, 44.4)), ((68.6, 33.4), (66.4, 38.4), (67.2, 44.4)),
              ((53.4, 38.8), (60, 40), (66.6, 38.8))):
        l.trazo(list(p), [.12, .3, .12], alfa=.3, dentro=cap, difuso=.1)
    for _ in range(60):
        x, y = rng.uniform(34, 86), rng.uniform(33, 55)
        l.mancha(ovalo(x, y, .22, .18), '0C3A33', .18, dentro=cap)
    l.trazo([(38.6, 49.6), (46, 51.6), (60, 52.2), (74, 51.6), (81.4, 49.6)], [.2, .45, .45, .45, .2], alfa=.4, dentro=cap, difuso=.1)
    for x in (47.4, 72.6):
        l.mancha(ovalo(x, 50.2, 3, 1.7), '0C3A33', .45, dentro=cap, difuso=.3)
    # los pedúnculos de los ojos, desde sus cuencas
    for lado in (-1, 1):
        a, b = espejo((47.6, 50), lado), espejo((45.2, 42.6), lado)
        l.masa(tubo([a, b], [1.7, 1.45]), alto=.5, brillo=.25, vientre=0, linea=.6, hondo=0)
    # la boca: dos placas, como una puerta
    l.masa(forma([(54.6, 53.6), (65.4, 53.6), (66, 60.4), (60, 61.6), (54, 60.4)], 2), material='lejos', alto=.2, brillo=.15,
           vientre=0, linea=.55, hondo=0)
    l.trazo([(60, 54), (60, 61.2)], .28, alfa=.55)
    for lado in (-1, 1):
        brazo, dedos_ = tenaza(lado)
        b = l.masa(brazo, material='acento', alto=.55, brillo=.3, vientre=0, linea=.8, hondo=0)
        d = l.masa(dedos_, material='acento', alto=.4, brillo=.25, vientre=0, linea=.7, hondo=0)
        for k in range(4):                                                  # los dientes del borde de los dedos
            x = 60 + lado * (3.4 + k * 1.6)
            l.trazo([(x, 69.6), (x + lado * .3, 70.6)], [.3, .08], alfa=.55, dentro=d)
            l.trazo([(x, 68.4), (x + lado * .3, 67.6)], [.3, .08], alfa=.45, dentro=d)
        for _ in range(8):                                                  # granitos en la palma
            x, y = 60 + lado * rng.uniform(11, 20), rng.uniform(63.6, 72.6)
            l.mancha(ovalo(x, y, .26, .22), '6B4E10', .3, dentro=b)


CARA = dict(ojo=[45.2, 42.2], ojo2=[74.8, 42.2], k=1.25, vista='frente', marco=[36.0, 22.0, 48, 48])
FONDO = ('<ellipse class="sombra" cx="60" cy="%.1f" rx="56" ry="5" style="opacity:.28"/>' % (SUELO)
         + '<path d="M104 86q-2-16 8-28M112 86q0-11 6-18M2 86q4.5-2.4 9 0t9 0" style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.55"/>')
LISTO = True
