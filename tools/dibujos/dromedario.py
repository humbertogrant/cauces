# -*- coding: utf-8 -*-
"""Zahra, la dromedaria (Camelus dromedarius), de memoria, parada: una sola joroba alta en medio del lomo (grasa, no agua), el
cuello largo que baja desde los hombros y sube en curva hasta la cabeza, con un poco de pelo más largo en la garganta y en la joroba;
la cabeza con la cara larga, los párpados pesados y las pestañas largas contra la arena, orejas chicas y redondas echadas atrás,
ollares que puede cerrar y el labio de arriba partido; las patas largas: adelante, el codo separado del pecho, el antebrazo, la
rodilla con su callo, la caña y el menudillo; atrás, el muslo largo que baja hasta la babilla, bajo la panza, y la pierna que vuelve
hacia atrás hasta el corvejón; callos en las rodillas y en el pecho (donde se apoya al echarse), y los pies anchos: dos dedos sobre
una almohadilla blanda, para no hundirse en la arena; la cola fina con un mechón.
"""
from _patas import peludo
from pintor import forma, ovalo, tubo

VISTA = (0, 4, 120, 84)
SUELO = 85.0


def cuerpo():
    c = forma([(29, 39.6), (32.6, 35.6), (37.4, 33), (42.4, 27), (47.4, 21.6), (52.6, 19.6), (58, 21.2), (63, 26.6), (67.4, 31.6),
               (72, 34.2), (77, 36.6), (82, 35.6), (86.4, 31.6), (89.4, 26.6), (92, 23.6), (96.4, 22.6), (101, 23.8), (104.6, 26.2),
               (107, 29), (106.8, 31.8), (104.4, 33.4), (100.2, 33.2), (96.2, 32), (93, 33), (89.4, 36.8), (85.4, 42.2),
               (80.6, 46.6), (75, 49.6), (70.4, 51.6), (64, 53.2), (56, 53.4), (48.4, 52.8), (42, 51), (35.8, 50.2), (30.4, 48),
               (28.2, 44)], 3)
    # el pelo un poco más largo arriba de la joroba y en la garganta
    return peludo(c, largo=1.3, paso=1.3, semilla=4, flujo=lambda x, y: 150 if x < 60 else 110, mezcla=.7,
                  donde=lambda x, y, nx, ny: (ny < -.5 and 45 < x < 60) or (ny > .3 and 80 < x < 92))


def mano(x0, a=0.0):
    """la pata de adelante: el antebrazo desde el codo, la rodilla con su callo, la caña, el menudillo, la cuartilla y el pie"""
    antebrazo = tubo([(x0, 50.4), (x0 + .5 + a * .3, 58), (x0 + 1 + a * .5, 65.6)], [3.5, 2.9, 2.2])
    rodilla = ovalo(x0 + 1.1 + a * .5, 66.6, 2.4, 2.1)
    cana = tubo([(x0 + 1.1 + a * .5, 67.4), (x0 + 1.4 + a * .6, 77.8)], [1.75, 1.6])
    menudillo = ovalo(x0 + 1.5 + a * .6, 78.6, 1.9, 1.7)
    cuartilla = tubo([(x0 + 1.6 + a * .6, 79), (x0 + 3 + a * .7, 82.4)], [1.6, 1.5])
    return [antebrazo, rodilla, cana, menudillo, cuartilla], pie(x0 + 3.6 + a * .7)


def pata(x0, a=0.0):
    """la de atrás: el muslo largo hasta la babilla, bajo la panza, y la pierna que vuelve atrás hasta el corvejón"""
    pierna = forma([(x0 - 2, 42), (x0 + 3.6, 47.4), (x0 + 6, 53.4), (x0 + 5.6, 57.6), (x0 + 3, 61.6), (x0 + 1.8 + a, 66.4),
                    (x0 + 1.8 + a, 69), (x0 - 1.6 + a, 69.6), (x0 - 2.6, 66.4), (x0 - 3.4, 61), (x0 - 4.6, 55.4), (x0 - 6.6, 49.4)], 3)
    cana = tubo([(x0 + .2 + a, 68.8), (x0 + .4 + a, 77.8)], [1.75, 1.6])
    menudillo = ovalo(x0 + .5 + a, 78.6, 1.9, 1.7)
    cuartilla = tubo([(x0 + .6 + a, 79), (x0 + 2 + a, 82.4)], [1.6, 1.5])
    return [pierna, cana, menudillo, cuartilla], pie(x0 + 2.6 + a)


def pie(x):
    """el pie ancho y blando: la almohadilla y los dos dedos con sus uñas chicas"""
    return forma([(x - 2.6, SUELO - 3), (x + 1.4, SUELO - 3.2), (x + 3.6, SUELO - 1.6), (x + 4.4, SUELO - .2), (x - 3.4, SUELO - .2),
                  (x - 3.8, SUELO - 1.6)], 2)


def dibujar(l):
    mano_l, pie_ml = mano(62.6, -1)
    pata_l, pie_pl = pata(44.6, 1.4)
    for partes, p in ((mano_l, pie_ml), (pata_l, pie_pl)):
        m = l.masa(partes + [p], material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
        l.pelaje(m, densidad=1.2, largo=1.2, ancho=.16, alfa=.2, semilla=31, claro=.3, flujo=95)
    t = l.masa([tubo([(29.4, 40.4), (27.4, 47.4), (26.6, 55)], [.75, .6, .5]), forma([(26.4, 54), (27.8, 57), (27.2, 60.4),
                                                                                       (25.8, 60.8), (25, 57.4)], 2)],
               alto=.4, brillo=.05, vientre=0, linea=.55, hondo=0)                        # la cola con su mechón
    l.pelaje(t, densidad=8, largo=1.8, ancho=.16, alfa=.4, semilla=32, claro=.3, flujo=95, zona=ovalo(26.4, 57.6, 2, 3.4))
    manos, pie_m = mano(67)
    patas, pie_p = pata(39.4)
    c = l.masa([cuerpo()] + manos + patas + [pie_m, pie_p], brillo=.14, vientre=.35, contraluz=.3,
               bultos=[(ovalo(52.4, 28, 14, 10), .14), (ovalo(98.6, 28, 5, 3.6), .3), (ovalo(36, 44, 8, 7), .1),
                       (ovalo(68.4, 44.4, 5, 6), .15)])
    l.pelaje(c, densidad=1.1, largo=1.5, ancho=.18, alfa=.26, semilla=33, claro=.35, curva=8,
             flujo=lambda x, y: 100 if y > 50 else (160 if x < 62 else (70 if x < 88 else 190)))
    l.pelaje(c, densidad=3, largo=2.4, ancho=.2, alfa=.34, semilla=34, claro=.15, mechon=2,
             zona=forma([(80.6, 36.6), (86, 32), (90, 34.4), (87.4, 40), (82.4, 44.4)], 2), flujo=100)   # la garganta
    # los callos de las rodillas y del pecho, un poco más oscuros; las líneas del codo y de la babilla
    for x, y, rx, ry in ((68.1, 66.6, 1.7, 1.9), (69.4, 51.8, 3.2, 1.5)):
        l.mancha(ovalo(x, y, rx, ry), '1F6D5A', .5, dentro=c, difuso=.2)
    for p in (((64.8, 47.4), (65.4, 51.6)), ((44.4, 53.4), (45.4, 57.8)), ((36.6, 64.4), (37.8, 68.4))):
        l.trazo(list(p), [.1, .26, .1], alfa=.3, dentro=c, difuso=.08)
    # los dos dedos de cada pie
    for x in (70.6, 42):
        l.trazo([(x + .8, SUELO - 2.8), (x + 1.1, SUELO - .3)], .22, alfa=.45, dentro=c)
    # la papada, el labio partido, el ollar, la oreja chica echada atrás y las pestañas largas
    l.trazo([(96, 31.8), (99.5, 32.9), (103, 33.2)], [.1, .3, .1], alfa=.3, dentro=c)
    l.trazo([(106.2, 29.4), (105.1, 30.8), (105.4, 32)], .22, alfa=.55, dentro=c)
    l.mancha(ovalo(104.5, 27.4, .9, .35, 30), '0C3A33', .75, dentro=c)
    l.masa(forma([(90.2, 24.6), (88.6, 22.6), (89, 21), (90.8, 21.4), (92, 23.4)], 2), alto=.4, brillo=.05, vientre=0, linea=.5,
           hondo=0)
    for dx in (-.8, .4, 1.6):
        l.trazo([(96.2 + dx, 24.4), (96 + dx * 1.4, 23)], .16, alfa=.6)


CARA = dict(ojo=[96.6, 26.2], k=1.3, boca=[104.4, 32.4], kb=1.4, giro=12, pb=.7, wb=.6)
CARA['marco'] = [81.0, 12.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="54" cy="%.1f" rx="42" ry="4.4" style="opacity:.28"/>' % (SUELO + .4)
         + '<path d="M2 88q10-4 22-1.5t24-1M78 87.5q12-3.5 22-1t18-1.5" style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.45"/>')
LISTO = True
