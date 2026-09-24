# -*- coding: utf-8 -*-
"""Tembo, el elefante africano de sabana (Loxodonta africana), de memoria, caminando: el punto más alto en el hombro y el lomo
hundido detrás; la cabeza grande con la frente inclinada; la oreja enorme, con la forma de África, que tapa el cuello y el hombro;
la trompa larga, colgando casi hasta el suelo, con arrugas en anillo y dos «dedos» en la punta; los colmillos que salen junto a
la base de la trompa y se curvan hacia adelante; el ojo chico entre la oreja y la trompa; patas como columnas, con los pies
redondos y sus uñas; la cola fina con un penacho. Piel gruesa y arrugada.
"""
import numpy as np

from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 0, 120, 90)
SUELO = 83.0


def cuerpo():
    return forma([(19.5, 50), (21, 38), (25.5, 29), (33, 23.5), (44, 21.5), (53.5, 24), (62, 21), (70, 20.5), (77, 17.5), (83, 16),
                  (88.5, 18.5), (92.5, 24), (95.5, 31), (97.5, 40), (98.8, 52), (98.6, 64), (99.4, 73.5), (101.5, 78.5),
                  (104, 79.6), (103, 81.6), (99.8, 81.8), (97, 78), (95.4, 68), (95, 56), (93.8, 46.5), (90.5, 47.5),
                  (86.5, 46.5), (82, 52), (74, 58.5), (60, 62.5), (46, 62), (36, 58.5), (25, 55.5)], 3)


def pata(arriba, abajo, ancho):
    (x0, y0), (x1, y1) = arriba, abajo
    col = tubo([(x0, y0), ((x0 * .55 + x1 * .45), (y0 * .55 + y1 * .45)), (x1, y1 - 2.6)], [ancho, ancho * .86, ancho * .8])
    return col.union(ovalo(x1 + .3, y1 - 2.3, ancho * .95, 2.5))


PATAS_CERCA = [((74, 52), (80.5, SUELO), 6.4), ((35, 50), (27.5, SUELO), 7.2)]
PATAS_LEJOS = [((67, 56), (65.5, SUELO - .6), 5.8), ((43, 55), (47, SUELO - .6), 6.2)]


def oreja():
    """la oreja con la forma de África: ancha arriba, con el borde de arriba casi recto y enrollado, el bulto de atrás, y abajo se
    angosta hasta la punta que cuelga; el borde de adelante, pegado a la cabeza detrás del ojo"""
    return forma([(81.6, 17.6), (77, 14.2), (70, 13), (63.4, 14), (58.6, 17.2), (55.8, 22.6), (54.8, 29), (55.6, 34.6),
                  (58.2, 38.6), (61.4, 42), (63.4, 46.2), (65, 51), (67.4, 57), (69.6, 55.6), (71.6, 51), (74.8, 47),
                  (78.8, 43), (81.8, 37.2), (83.4, 30.4), (83.2, 23)], 3)


def colmillo():
    return tubo([(91.5, 45.5), (95.5, 48.4), (100.5, 49.2), (105.2, 47.2)], [1.55, 1.4, 1.05, .45])


def dibujar(l):
    for arriba, abajo, a in PATAS_LEJOS:
        l.masa(pata(arriba, abajo, a), material='lejos', alto=.7, brillo=.05, vientre=0, linea=.8, hondo=0)
    cola = tubo([(20.5, 38), (18.8, 46), (18.4, 55)], [.8, .6, .45])
    l.masa([cola, ovalo(18.3, 57.2, 1.1, 2.4, 8)], alto=.4, brillo=.05, vientre=0, linea=.6, hondo=0)
    patas = [pata(*p) for p in PATAS_CERCA]
    c = l.masa([cuerpo()] + patas, brillo=.2, vientre=.45,
               bultos=[(ovalo(86, 22, 7, 6), .5), (ovalo(30, 36, 11, 13), .2), (ovalo(96.5, 38, 2.6, 6), .3)])
    l.grietas(c, densidad=.3, ancho=.13, alfa=.13, semilla=3)                              # la piel gruesa, agrietada
    # la piel arrugada: anillos en la trompa, arrugas en las patas y en el costado
    for y in np.arange(40, 78, 2.6):
        x = float(np.interp(y, [40, 52, 64, 74], [96.2, 97, 97, 97.8]))
        l.trazo([(x - 1.9, y - .3), (x, y + .35), (x + 2.2, y - .2)], [.12, .3, .12], alfa=.35, dentro=c)
    for (x0, y0), (x1, y1), a in PATAS_CERCA:
        for t in np.linspace(.45, .88, 5):
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            l.trazo([(x - a * .7, y), (x, y + .6), (x + a * .7, y + .1)], [.1, .28, .1], alfa=.28, dentro=c)
        for f in (-.4, .05, .5):
            l.masa(ovalo(x1 + a * f, SUELO - 1.2, .95, .8), material='claro', alto=.15, brillo=0, vientre=0, linea=.25, arroja=False, hondo=0)
    for p in (((40, 40), (44, 44), (46, 50)), ((48, 36), (53, 42)), ((30, 44), (33, 49))):
        l.trazo(list(p), [.15, .35, .15], alfa=.2, dentro=c, difuso=.1)
    l.trazo([(87, 27.5), (84.5, 30.5), (84.8, 33)], [.15, .32, .12], alfa=.35, dentro=c)     # la arruga bajo el ojo
    l.trazo([(92.4, 45.8), (90.3, 48.2), (88.2, 47.6)], [.2, .45, .2], alfa=.5, dentro=c)   # el labio de abajo
    l.mancha(forma([(101.2, 80.6), (103.4, 79.8), (104.2, 81.4)], 1), '0C3A33', .55)          # los «dedos» de la punta
    o = l.masa(oreja(), alto=.3, brillo=.12, vientre=0, linea=.85, hondo=0, contraluz=.2)
    l.grietas(o, densidad=.35, ancho=.12, alfa=.11, semilla=4)
    # el borde de arriba, enrollado: una franja más clara con su pliegue debajo
    l.mancha(forma([(81, 16.8), (76.6, 14.4), (70, 13.6), (63.6, 14.6), (58.8, 17.8), (57.6, 20.6), (60.4, 18.8), (64.4, 17.4),
                    (70, 16.6), (76, 17.4), (80.2, 19.6)], 2), 'D2F2DA', .35, dentro=o, difuso=.3)
    l.trazo([(58.2, 21.4), (61.4, 19.4), (66, 18), (71, 17.6), (76, 18.4), (80.6, 20.6)], [.1, .3, .35, .35, .3, .1], alfa=.35,
            dentro=o, difuso=.1)
    # las venas, que se abren desde donde la oreja se pega a la cabeza
    for p in (((81, 27), (74, 26.4), (66.4, 25.4), (60, 27)), ((80.6, 33), (73.4, 34.2), (66.4, 36.6), (61.4, 39.6)),
              ((79.6, 39), (74, 42.4), (69.6, 47.6), (67.8, 53)), ((73.6, 34.2), (70.4, 30.6), (64.4, 30.8)),
              ((70, 45), (66.6, 44.4), (63.6, 44))):
        l.trazo(list(p), [.28, .2, .14, .05], color='11443F', alfa=.3, dentro=o, difuso=.12)
    # el borde de atrás, un poco ondulado y gastado
    for k, (x, y) in enumerate(((56, 25.6), (55.4, 31), (56.8, 36), (60, 40.4), (63, 44.2), (64.6, 49.4))):
        l.trazo([(x + .6, y - .8), (x - .2, y), (x + .6, y + .8)], [.1, .22, .1], alfa=.3, dentro=o, difuso=.05)
    l.mancha(oreja().boundary.buffer(1.8), '0C3A33', .1, dentro=o, difuso=.6)
    l.masa(colmillo(), material='claro', alto=.5, brillo=.3, vientre=0, linea=.6, hondo=0)


CARA = dict(ojo=[87.6, 29.6], k=1.6)
CARA['marco'] = [71.0, 12.0, 38, 38]
FONDO = ('<ellipse class="sombra" cx="58" cy="%.1f" rx="54" ry="6" style="opacity:.28"/>' % (SUELO + .5)
         + '<path d="M2.5 86q.3-2.8-1-4.6M5 86.4q.2-3 1.4-4.6M29 87.6q.3-3-1-5M31.4 88q.2-3.2 1.4-5M116 85q-.3-3 1.2-5"' + AGUA + '/>')
LISTO = True
