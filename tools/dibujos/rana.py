# -*- coding: utf-8 -*-
"""Croac, la rana toro (Lithobates catesbeianus), de memoria: sentada, el lomo que baja de la cabeza a la grupa, cabeza ancha con
los ojos saltones arriba; detrás de cada ojo, un tímpano redondo y grande (su oído; en el macho, más grande que el ojo), rodeado
por un pliegue de piel que baja hacia el hombro (no tiene los pliegues largos del lomo de otras ranas); boca muy ancha; las patas de
adelante cortas y derechas, con cuatro dedos; las de atrás plegadas: el muslo hacia adelante, la pierna hacia atrás y el pie largo
sobre el suelo, con cinco dedos unidos por membrana. Piel lisa con manchas.
"""
import numpy as np

from _patas import dedos, miembro
from pintor import ovalo, forma, tubo

VISTA = (0, 0, 120, 90)
SUELO = 81.0


def torso():
    return forma([(101.5, 49.5), (100, 44.5), (95, 40.5), (89, 36.5), (84, 33), (78, 34.5), (71, 38), (62, 42), (52, 48.5),
                  (43, 56), (35.5, 64), (33, 71), (36.5, 77), (46, 79.5), (58, 79), (70, 75.5), (80, 69), (88, 62), (95, 57),
                  (100, 53)], 3)


def pierna(lejos=False):
    d = np.array([5.0, -2.0]) if lejos else np.zeros(2)
    muslo = tubo([(40, 65) + d, (48, 70) + d, (57, 73.5) + d], [7.2, 6.2, 4.6])
    pierna_ = tubo([(58, 74) + d, (50, 77.5) + d, (41.5, 78.5) + d], [4.0, 3.2, 2.4])
    pie = tubo([(41, 79.2) + d, (49, 80) + d, (56, 80.2) + d], [2.2, 1.7, 1.2])
    ds, puntas = dedos((55.5, 80.2) + d, 4, [4.8, 6.2, 7.4, 6.4, 4.6], abanico=26, grueso=(.75, .45), curva=-4)
    return [muslo, pierna_, pie] + ds, puntas


def brazo(lejos=False):
    d = np.array([-4.5, -1.0]) if lejos else np.zeros(2)
    b = miembro([(77, 62) + d, (75, 69) + d, (79, 76) + d, (82, 79.5) + d], [3.8, 3.0, 2.2, 1.7])
    ds, puntas = dedos((82.5, 80) + d, 8, [3.2, 4.0, 3.6, 2.8], abanico=70, grueso=(.75, .5), curva=-10)
    return [b] + ds, puntas


def membrana(puntas, base):
    """la membrana entre los dedos del pie: un abanico claro que llega hasta la mitad de cada dedo"""
    pts = [base] + [tuple(np.asarray(base) * .35 + np.asarray(p) * .65) for p, _ in puntas]
    from shapely.geometry import Polygon
    return Polygon(pts).convex_hull.buffer(.3)


def dibujar(l):
    pl, _ = pierna(True)
    l.masa(pl, material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
    bl, _ = brazo(True)
    l.masa(bl, material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
    cuerpo = l.masa(torso(), brillo=.35, vientre=.75,
                    bultos=[(ovalo(84.5, 37.5, 5.5, 5), .9), (ovalo(92, 50, 9, 6), .25), (ovalo(55, 58, 16, 14), .3)])
    # manchas de la piel, más en el lomo
    rng = np.random.default_rng(9)
    for x, y, r in ((62, 47, 2.4), (52, 54, 2.8), (70, 43, 1.8), (45, 62, 2.2), (58, 62, 1.6), (40, 70, 1.8), (76, 50, 1.5)):
        l.mancha(ovalo(x + rng.uniform(-.5, .5), y, r, r * .8, rng.uniform(0, 90)), '0C3A33', .22, dentro=cuerpo, difuso=.25)
    # el tímpano: un disco grande detrás del ojo, con su borde, y el pliegue de piel que lo rodea y baja al hombro
    l.mancha(ovalo(74.5, 45, 4.1, 4.0), '1F6D5A', .55, dentro=cuerpo)
    l.mancha(ovalo(74.5, 45, 4.1, 4.0).boundary.buffer(.28), '0C3A33', .55, dentro=cuerpo)
    l.mancha(ovalo(73.6, 44.2, 1.3, 1.2), 'CFF4E7', .35, dentro=cuerpo, difuso=.3)
    l.trazo([(80.5, 37.5), (76, 39.4), (71, 41.2), (68.6, 45), (69.4, 50), (72, 54.5)], [.2, .45, .55, .5, .35, .15], alfa=.45, dentro=cuerpo)
    l.mancha(ovalo(99.2, 45.6, .5, .38), '0C3A33', .8)                   # la narina
    pc, pts_pie = pierna()
    l.masa(pc, alto=.6, brillo=.2, vientre=.3, linea=.75, hondo=0, raices=[(40, 64, 3, 8)])
    l.mancha(membrana(pts_pie, (55.5, 80.2)), 'A9E1CF', .35)
    for x, y, r in ((49, 70, 1.8), (53, 73.5, 1.3)):
        l.mancha(ovalo(x, y, r, r * .8), '0C3A33', .2, difuso=.2)
    bc, _ = brazo()
    l.masa(bc, alto=.6, brillo=.2, vientre=.3, linea=.72, hondo=0, raices=[(77, 61, 2.5, 6)])


CARA = dict(ojo=[84.5, 36.8], k=3.0, boca=[88.6, 52.2], kb=7.2, giro=-14, pb=.35, wb=.8)
CARA['marco'] = [62.0, 12.0, 44, 44]
FONDO = ('<ellipse class="sombra" cx="62" cy="%.1f" rx="44" ry="5" style="opacity:.28"/>' % (SUELO + .5)
         + '<path d="M2 87q4.5-2.4 9 0t9 0t9 0M108 84q-.3-3.4 1.2-6M110.6 84.4q0-3 1.7-5" style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.55"/>')
LISTO = True
