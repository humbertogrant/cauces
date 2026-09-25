# -*- coding: utf-8 -*-
"""El junco del Yangtsé, de memoria: casco de proa chata y cuadrada, sin roda, que sube en una popa alta con el castillo de popa y
su techo curvo; el timón grande colgado de la popa, que se sube en los bajíos; dos palos con velas de estera reforzadas con listones
de bambú (los listones dan las líneas horizontales y hacen que la vela se pliegue como un abanico), con las escotas que bajan de
cada listón; un toldo de esteras sobre la bodega. El casco dividido en compartimentos estancos no se ve desde afuera (está en
NAVES.yangtse).
"""
from _barcas import agua, cabo, esteras, olas_fondo, palo, poli, tablas
from pintor import forma

VISTA = (0, 8, 120, 76)
AGUA_Y = 75.0

ARRIBA = [(13.4, 50.2), (22, 54.6), (34, 62.4), (50, 66.4), (70, 66.8), (88, 64.6), (103.4, 59.6)]
ABAJO = [(19.6, 70.6), (26, 74.6), (36, 77.4), (50, 78.4), (70, 78.4), (88, 76.4), (102.4, 70.4)]


def vela_junco(l, x_palo, y_top, ancho_popa, ancho_proa, alto, listones=7):
    """una vela de junco: casi un trapecio, más ancha abajo, con la verga arriba y los listones de bambú que la cruzan"""
    x0, x1 = x_palo - ancho_popa, x_palo + ancho_proa
    pts = [(x0 + 3, y_top + 1.4), (x1 - 1.6, y_top - 1.6), (x1 + .6, y_top + alto * .5), (x1 + 1.4, y_top + alto),
           (x0 - 1.4, y_top + alto + 1.2), (x0 - .4, y_top + alto * .45)]
    v = l.masa(forma(pts, 1), material='vientre', alto=.22, brillo=.08, vientre=0, hondo=0, escalon=.15, contraluz=.15, linea=.6)
    esteras(l, v, paso=1.6, alfa=.25)
    for k in range(listones + 1):
        f = k / listones
        a = (x0 + 3 + (x0 - 1.4 - x0 - 3) * f, y_top + 1.4 + (alto + 1.2 - 1.4) * f)
        b = (x1 - 1.6 + (x1 + 1.4 - x1 + 1.6) * f, y_top - 1.6 + (alto + 1.6) * f)
        l.masa(forma([(a[0] - .4, a[1] - .35), (b[0] + .4, b[1] - .35), (b[0] + .4, b[1] + .35), (a[0] - .4, a[1] + .35)], 0),
               material='acento', alto=.2, brillo=.15, vientre=0, hondo=0, linea=.3, arroja=False)
        if 0 < k < listones:
            cabo(l, [(a[0] - .2, a[1]), (x0 - 6 + f * 3, y_top + alto + 6)], ancho=.1, alfa=.45)     # las escotas de cada listón
    return v


def dibujar(l):
    # el palo de popa y su vela, detrás; el de proa, más alto, adelante
    palo(l, (46, 67.4), (47.4, 20.4), .8, .55)
    vela_junco(l, 47, 24, 20, 8, 34, listones=6)
    palo(l, (80, 67.2), (81.2, 12), .9, .6)
    vela_junco(l, 81, 15.4, 22, 9, 44, listones=8)
    # el castillo de popa, sobre la popa alta, con su techo curvo y sus ventanas (detrás del casco, que lo tapa abajo)
    popa = l.masa(poli([(14.4, 44.2), (31, 46.6), (31.4, 60), (16, 56)], .4), material='acento', alto=.35, brillo=.2, vientre=0,
                  hondo=0, linea=.6)
    for x in (18.6, 23.2, 27.6):
        l.mancha(poli([(x, 48.6), (x + 2.6, 49), (x + 2.6, 51.8), (x, 51.4)], .15), '0C3A33', .7, dentro=popa)
    l.masa(forma([(11.2, 44), (15.4, 41.8), (24, 42.6), (33, 45), (32.8, 46.8), (22.6, 45.2), (14.4, 45.6)], 2), material='lejos',
           alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    # el casco, de una pieza: la popa alta y la proa chata, un espejo casi derecho sin roda
    c = l.masa(poli(ARRIBA + [(104.2, 62.4), (103.4, 67.6)] + ABAJO[::-1], .5), material='acento', alto=.5, brillo=.3, vientre=0,
               hondo=0, contraluz=.25)
    tablas(l, c, ARRIBA[1:], ABAJO[1:], n=4)
    l.trazo([(101.4, 60.6), (101.6, 70)], [.12, .3, .12], alfa=.35, dentro=c)          # el canto del espejo de proa
    l.trazo([(15.6, 51.4), (20.6, 70)], [.12, .3, .12], alfa=.35, dentro=c)            # y el de popa
    # el timón grande, colgado de la popa
    l.masa(poli([(15.2, 58.6), (18.6, 60), (21.4, 74.2), (19, 79), (12.6, 78.4), (14, 68)], .5), material='acento', alto=.3,
           brillo=.15, vientre=0, hondo=0, linea=.6)
    # el toldo de esteras sobre la bodega: una bóveda baja, con sus aros
    t = l.masa(forma([(53.6, 66.8), (53.6, 61.8), (56, 59.4), (60, 58.4), (70, 58.4), (74, 59.4), (76.4, 61.8), (76.4, 66.8)], 1),
               material='vientre', alto=.35, brillo=.05, vientre=0, hondo=0, linea=.5)
    esteras(l, t, paso=1.2, alfa=.3)
    for x in (58, 65, 72):
        l.trazo([(x, 58.8), (x, 66.6)], [.2, .28, .2], color='164F46', alfa=.45, dentro=t)
    agua(l, AGUA_Y, sombra=forma([(16, 75), (100, 75), (96, 79.6), (22, 79.6)], 1))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
