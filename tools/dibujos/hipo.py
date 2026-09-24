# -*- coding: utf-8 -*-
"""Hipo, el hipopótamo (Hippopotamus amphibius), de memoria: cuerpo de barril sobre patas cortas como columnas, con cuatro dedos
cortos de uñas redondas; cabeza enorme con el hocico ancho y los ojos, las orejas chicas y las narinas arriba (para ver, oír y
respirar con casi todo el cuerpo bajo el agua); piel gruesa y lisa, con pliegues en el cuello; la cola corta y aplanada. Pasta
con la cabeza baja, como en su ficha: sale de noche a comer pasto. En el lomo, un picabueyes (dorado).
"""

from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 0, 120, 90)
SUELO = 82.0


def cuerpo():
    return forma([(17.5, 52), (19.5, 42), (26, 35.5), (36, 32), (48, 30.5), (60, 30.5), (70, 32.5), (78, 36), (85, 40.5),
                  (89, 42.5), (95, 44.5), (99, 46.5), (103, 51.5), (107.5, 57.5), (111, 62), (113, 68), (112.5, 75),
                  (109.5, 79.5), (103, 80.8), (96.5, 78.8), (91.5, 74.5), (86.5, 69.5), (81, 67.2), (75, 68.5), (64, 71.5),
                  (50, 72.5), (38, 71), (28, 67.5), (21, 61.5)], 3)


def pata(x0, y0, x1, ancho, lejos=False):
    """una pata como columna, un poco más ancha arriba, con el pie redondo apoyado"""
    col = tubo([(x0, y0), ((x0 + x1) / 2, (y0 + SUELO) / 2), (x1, SUELO - 2.6)], [ancho, ancho * .82, ancho * .78])
    pie = ovalo(x1 + .6, SUELO - 2.2, ancho * .95, 2.4)
    return col.union(pie)


def unas(x, ancho):
    return [ovalo(x + ancho * f, SUELO - 1.1, .9, .75) for f in (-.35, .05, .45)]


def picabueyes():
    cuerpo_ = ovalo(47.5, 26.2, 3.4, 2.0, -8)
    cabeza_ = ovalo(51.6, 24.2, 1.5, 1.4)
    pico = forma([(52.8, 23.6), (55.4, 24.4), (52.9, 25.0)], 1)
    cola = forma([(44.5, 26.6), (40.8, 28.8), (41.2, 27.2), (44.2, 25.4)], 1)
    patas = [tubo([(x, 27.8), (x - .2, 30.6)], [.28, .24]) for x in (46.8, 48.4)]
    return [cuerpo_, cabeza_, pico, cola], patas


def dibujar(l):
    for x0, y0, x1, a in ((66, 60, 65, 5.4), (38, 60, 40.5, 5.8)):            # las patas del otro lado
        l.masa(pata(x0, y0, x1, a, True), material='lejos', alto=.7, brillo=.05, vientre=0, linea=.8, hondo=0)
    l.masa(tubo([(19, 47), (16.5, 52), (15.2, 57.5)], [1.4, 1.1, .7]), alto=.5, brillo=.1, vientre=0, linea=.7, hondo=0)   # la cola
    patas = [pata(73, 58, 72.5, 5.8), pata(30, 58, 31.5, 6.4)]         # las de este lado salen del mismo volumen
    c = l.masa([cuerpo()] + patas, brillo=.28, vientre=.55,
               bultos=[(ovalo(99.2, 48.4, 3.3, 2.5, 40), .9), (ovalo(108.5, 60, 4.2, 3, 50), .6), (ovalo(106, 71, 8, 6.5, 50), .5),
                       (ovalo(93, 72, 5, 4), .4), (ovalo(70, 50, 11, 13), .18), (ovalo(33, 50, 12, 13), .18)])
    for x0, x1, a in ((73, 72.5, 5.8), (30, 31.5, 6.4)):                  # el borde de adelante de cada pata, apenas
        l.trazo([(x0 + a * .75, 64), (x1 + a * .85, 72), (x1 + a * .8, SUELO - 4)], [.1, .35, .1], alfa=.22, dentro=c, difuso=.25)
        for u in unas(x1, a):
            l.masa(u, material='claro', alto=.15, brillo=0, vientre=0, linea=.25, arroja=False, hondo=0)
        l.trazo([(x1 - a * .6, SUELO - 7), (x1, SUELO - 6.2), (x1 + a * .6, SUELO - 7)], .3, alfa=.22, dentro=c)
    # los pliegues del cuello y de la papada, y la línea de la boca que sigue el hocico hacia atrás
    for p in (((84.5, 43.5), (86.5, 52), (85.2, 60)), ((88.5, 46), (90.8, 54), (90, 62.5)), ((80.5, 42), (81.8, 48))):
        l.trazo(list(p), [.2, .45, .15], alfa=.28, dentro=c, difuso=.12)
    l.trazo([(90.5, 68.5), (93.5, 72.5), (98, 75.5)], [.15, .4, .2], alfa=.3, dentro=c, difuso=.1)
    # las orejas chicas, arriba, detrás de los ojos
    l.masa([ovalo(90.6, 42.2, 1.7, 2.5, -30)], alto=.5, brillo=.1, vientre=0, linea=.6, hondo=0)
    l.mancha(ovalo(90.8, 42.6, .75, 1.35, -30), '0C3A33', .35)
    # las narinas, arriba de la punta del hocico
    l.mancha(ovalo(108.8, 59.4, .7, 1.3, 55), '0C3A33', .8)
    l.mancha(ovalo(111.2, 62.6, .6, 1.1, 55), '0C3A33', .6)
    ave, patas = picabueyes()
    l.masa(ave, material='acento', alto=.6, brillo=.3, vientre=0, linea=.45, hondo=0)
    for pt in patas:
        l.masa(pt, material='oscuro', alto=.1, brillo=0, vientre=0, linea=0, tinta=False, arroja=False, hondo=0)
    l.mancha(ovalo(52.1, 23.8, .35, .35), '0C3A33', 1)


CARA = dict(ojo=[99.3, 49.4], k=2.0, boca=[102.4, 71.6], kb=7.6, giro=33, pb=.6, wb=.8, inclina=-40)
CARA['marco'] = [76.0, 38.0, 46, 46]
FONDO = ('<ellipse class="sombra" cx="62" cy="%.1f" rx="56" ry="6" style="opacity:.28"/>' % (SUELO + .5)
         + '<path d="M93.5 86q.4-3.2-1.2-5.4M96 86.4q.2-3.6 1.4-5.6M115 85.6q-.3-3.2 1.3-5.2M117.4 86q0-2.8 1.7-4.2M4.5 85q.3-2.8-1-4.6M7 85.4q.2-3 1.4-4.6"'
         + AGUA + '/>')
LISTO = True
