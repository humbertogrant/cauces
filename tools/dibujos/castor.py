# -*- coding: utf-8 -*-
"""Bíber, el castor europeo (Castor fiber), de memoria: sentado en la orilla sobre las patas de atrás, royendo la corteza de una
rama que sostiene con las manos: cuerpo grande, pesado y encorvado, de pelo denso; la cabeza ancha y roma, con los cachetes llenos
(los músculos de roer), orejas chicas y redondas, ojos chicos puestos altos y la nariz arriba del hocico, bigotes, y los dos
incisivos grandes y anaranjados a la vista (el esmalte lleva hierro: por eso van dorados, el único detalle de ese color); las manos
chicas, de dedos con uñas, que sostienen la rama; las patas de atrás grandes, con membrana entre los cinco dedos; la cola ancha,
plana, ovalada y cubierta de escamas, apoyada en el suelo (se ve un poco desde arriba, para que se vea ancha).
"""
import numpy as np

from _patas import dedos, garra, peludo
from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 18, 120, 68)
SUELO = 80.0


def cuerpo():
    c = forma([(39, 78.6), (35.2, 71), (34.4, 61), (37.2, 51), (43.6, 42), (52.4, 35.4), (61.6, 31.6), (70, 30.2), (76.2, 29.4),
               (82, 30), (87, 33), (91.6, 37.2), (94.2, 40.4), (94.2, 43.4), (92.2, 46.2), (88.8, 47.8), (85, 49.2), (80.6, 50.8),
               (76.4, 54.4), (73.4, 60), (71.2, 66.6), (68.6, 72.8), (64, 77.6), (55, 80.2), (46, 80.2)], 3)
    return peludo(c, largo=1.3, paso=1.3, donde=lambda x, y, nx, ny: ny < -.3 and x < 74 or (nx < -.5 and y < 72), semilla=3,
                  flujo=lambda x, y: 160 if y < 45 else 120, mezcla=.75)


def cola():
    """la cola, ancha y plana: una paleta ovalada con un pedúnculo corto y carnoso"""
    return forma([(40, 77.2), (33, 76), (25, 74.4), (15.5, 73.8), (7.4, 74.8), (3, 77.6), (5.2, 80.8), (14, 82.6), (24.4, 82.2),
                  (32.6, 80.8), (40, 80.2)], 3)


def mano(lejos=False):
    """el antebrazo corto y la mano chica, con los dedos cerrados sobre la rama (la de allá queda detrás de la rama)"""
    if lejos:
        return [tubo([(76, 44.6), (78.6, 50.8), (86.8, 51.6)], [2.8, 2.2, 1.7]), ovalo(89.4, 51.2, 2, 1.5, -10)], []
    brazo = tubo([(72.6, 49.4), (75, 57.4), (83, 58.8)], [3.1, 2.5, 1.9])
    palma = ovalo(85.6, 58.2, 2, 1.5, -10)
    ds, puntas = [], []
    for k in range(4):                                   # cuatro dedos que abrazan la rama por delante
        y = 56.6 + k * .95
        ds.append(tubo([(86.4, y), (89.2, y - .7), (90.8, y + .3)], [.52, .46, .36], 6))
        puntas.append(((90.8, y + .3), 110))
    return [brazo, palma] + ds, puntas


def rama():
    """la rama que roe, pelada donde ya comió, con dos hojas arriba"""
    return tubo([(83.6, 68.8), (90.2, 56), (96.6, 43.4), (101.2, 34.4)], [1.25, 1.2, 1.1, .95])


def pata():
    """la pata de atrás, grande: el muslo en el cuerpo, el pie largo y plano en el suelo, con sus dedos palmeados"""
    pie = forma([(52.6, 76.6), (60, 76.8), (67.4, 77.6), (72.8, 78.6), (74.6, 80), (72, 80.6), (60, 80.6), (52, 80.4)], 3)
    ds, puntas = dedos((70.4, 79.2), 8, [3.2, 3.8, 4.0, 3.6, 3.0], abanico=40, grueso=(.8, .55), curva=4)
    return [pie] + ds, puntas


def dibujar(l):
    t = l.masa(cola(), material='lejos', alto=.35, brillo=.3, vientre=0, linea=.8, hondo=0, raices=[(40, 78.6, 1, 4)], funde=False)
    # las escamas de la cola, en rombos: dos familias de líneas que se cruzan
    for k in np.arange(-4, 40, 2.3):
        l.trazo([(k, 73.4), (k + 7, 83)], .15, alfa=.32, dentro=t)
        l.trazo([(k + 7, 73.4), (k, 83)], .15, alfa=.32, dentro=t)
    l.mancha(ovalo(20, 76.4, 12, 1.6, -2), 'D2F2DA', .18, dentro=t, difuso=.8)                # el brillo del cuero
    ml, pl = mano(True)
    l.masa(ml, material='lejos', alto=.55, brillo=.05, vientre=0, linea=.7, hondo=0)
    c = l.masa(cuerpo(), brillo=.1, vientre=.35, contraluz=.35,
               bultos=[(ovalo(85, 40.4, 6.4, 5.6), .45), (ovalo(80, 35.6, 5.4, 4.4), .3), (ovalo(91.4, 41.6, 3, 2.6), .25),
                       (ovalo(56, 66, 12, 11), .35), (ovalo(52, 46, 12, 9), .2)])
    l.pelaje(c, densidad=1.8, largo=1.9, ancho=.2, alfa=.34, semilla=8, curva=6, desvio=7, claro=.4, mechon=2, separa=.26,
             flujo=lambda x, y: 185 if x > 78 and y < 46 else (125 if x < 60 else 110))
    # la oreja chica y redonda, la nariz arriba del hocico, los bigotes
    l.masa(ovalo(77.2, 33.2, 2, 1.8, -20), alto=.4, brillo=.1, vientre=0, linea=.55, hondo=0, arroja=False)
    l.mancha(ovalo(77.4, 33.5, .9, .8), '0C3A33', .4)
    l.mancha(forma([(92, 37.6), (93.8, 38.8), (93.9, 40.6), (92.4, 40)], 2), '0C3A33', .85, dentro=c)
    for dx, dy in ((-1.6, -3.6), (0, -1.4), (1, 1), (-1, 3)):
        l.trazo([(91.4, 43.2), (94 + dx * .6, 43 + dy * .5), (97.8 + dx, 42.6 + dy)], [.2, .13, .05], alfa=.7)
    # los incisivos anaranjados, a la vista bajo el labio de arriba
    l.masa([forma([(89.6, 46.2), (92.4, 45.8), (92.6, 49.8), (90.2, 50.2)], 1)], material='acento', alto=.25, brillo=.35,
           vientre=0, linea=.35, hondo=0)
    l.trazo([(91.1, 46.1), (91.4, 50)], .16, alfa=.5)
    r = l.masa(rama(), material='claro', alto=.5, brillo=.2, vientre=0, linea=.6, hondo=0)
    for y0 in (61, 64.4):                                                                       # la corteza que queda abajo
        l.mancha(tubo([(83.6, 68.8), (86, 64), (87.8, y0 - 1)], [1.4, 1.3, 1.3]), '4EB196', .9, dentro=r)
    for p in (((93.4, 49.6), (94.4, 48.2)), ((95, 46.6), (95.6, 45.2)), ((92.4, 52), (93.6, 50.6))):
        l.trazo(list(p), .16, alfa=.35, dentro=r)                                                 # las marcas de los dientes
    for x, y, a in ((100.6, 35.6, -110), (101, 34.8, -40)):
        h = forma([(x, y), (x + 3 * np.cos(np.radians(a + 25)), y + 3 * np.sin(np.radians(a + 25))),
                   (x + 6 * np.cos(np.radians(a)), y + 6 * np.sin(np.radians(a))),
                   (x + 3 * np.cos(np.radians(a - 25)), y + 3 * np.sin(np.radians(a - 25)))], 3)
        l.masa(h, material='lejos', alto=.25, brillo=.2, vientre=0, linea=.5, hondo=0)
    pp, puntas_p = pata()
    p = l.masa(pp, alto=.5, brillo=.1, vientre=.2, linea=.75, hondo=0)
    for q, g in puntas_p:
        l.masa(garra(q, g, .8, .3), material='oscuro', alto=.1, brillo=0, vientre=0, linea=0, tinta=False, arroja=False, hondo=0)
    l.mancha(forma([(70, 78.2), (74.6, 77.4), (75.4, 79.6), (74.2, 81.2), (70.2, 80.4)], 2), 'A9E1CF', .35, dentro=p, difuso=.2)   # la membrana
    mn, puntas_m = mano()
    m = l.masa(mn, alto=.55, brillo=.1, vientre=.2, linea=.75, hondo=0, raices=[(72.4, 47, 2, 6)])
    l.pelaje(m, densidad=2, largo=1.5, ancho=.18, alfa=.3, semilla=9, claro=.35, flujo=150)
    for q, g in puntas_m:
        l.masa(garra(q, g, .6, .22), material='oscuro', alto=.1, brillo=0, vientre=0, linea=0, tinta=False, arroja=False, hondo=0)


CARA = dict(ojo=[85, 36.4], k=1.15, boca=[89, 46.6], kb=1.4, giro=-6, pb=.6, wb=.6)
CARA['marco'] = [72.0, 24.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="52" cy="%.1f" rx="50" ry="4.4" style="opacity:.28"/>' % (SUELO + 1.4)
         + '<path d="M86 84q4.5-2.4 9 0t9 0t9 0M110 79q.3-3-1-5M112.4 79.4q.2-3.2 1.4-5"' + AGUA + '/>')
LISTO = True
