# -*- coding: utf-8 -*-
"""Tarim, el camello bactriano (Camelus bactrianus), de memoria: dos jorobas, una sobre los hombros y otra sobre las caderas,
cuerpo más macizo y patas más cortas que el dromedario, y el pelo largo y más oscuro del invierno de las estepas: una barba que
cuelga bajo el cuello hasta el pecho, mechones arriba de las jorobas y de la cabeza y «mangas» en la parte de arriba de las patas de
adelante; la cabeza con párpados pesados y pestañas largas, ollares que se cierran contra el polvo y el labio partido; las patas
con la rodilla y su callo adelante, el corvejón atrás, y los pies anchos de dos dedos sobre una almohadilla.
"""
from _patas import peludo
from pintor import forma, ovalo, tubo

VISTA = (0, 6, 120, 82)
SUELO = 85.0


def cuerpo():
    c = forma([(26.6, 45), (28.6, 38.6), (33, 33.6), (37.4, 27.4), (42, 24.4), (46.4, 27.8), (50.6, 31.2), (54.6, 27), (59, 23.2),
               (63.6, 25.6), (67, 31.6), (71.6, 35.6), (76.6, 38), (81.6, 37.6), (86, 33.6), (89.4, 28.6), (92, 25.6), (96.4, 24.8),
               (101, 26.2), (104.6, 28.6), (106.8, 31.2), (106.4, 34), (103.6, 35.4), (99.6, 35), (95.6, 33.6), (92.6, 34.6),
               (89, 38.6), (85, 44), (80, 48.6), (74, 52.6), (70, 55.6), (64, 57.6), (56, 57.6), (48, 57), (42, 55.6), (36.6, 53),
               (31, 51.6), (27.6, 49)], 3)
    # el pelo largo arriba de las jorobas y de la cabeza
    return peludo(c, largo=2.2, paso=1.4, semilla=4, flujo=lambda x, y: 150 if x < 50 else (30 if x < 66 else 120), mezcla=.55,
                  donde=lambda x, y, nx, ny: ny < -.35 and (36 < x < 47 or 53 < x < 65 or 89 < x < 95))


def barba():
    """la barba que cuelga del cuello y del pecho, en mechones"""
    b = forma([(93.4, 34.4), (91.4, 39), (88, 44.6), (83.4, 50.4), (78.4, 55.4), (73.2, 59.4), (69.4, 58.4), (71, 54.4), (76, 49.4),
               (81.2, 43.6), (85.6, 37.6), (89.6, 33.6)], 3)
    return peludo(b, largo=2.6, paso=1.1, semilla=5, flujo=95, mezcla=.7, donde=lambda x, y, nx, ny: ny > -.2)


def manga(x0):
    """el pelo largo de la parte de arriba de la pata de adelante"""
    m = forma([(x0 - 4.4, 52.4), (x0 + 4.6, 51.6), (x0 + 4.6, 58), (x0 + 3.6, 65.6), (x0 - 2.8, 66.4), (x0 - 4.8, 60)], 3)
    return peludo(m, largo=2.4, paso=1.1, semilla=6, flujo=95, mezcla=.7, donde=lambda x, y, nx, ny: ny > .2 or abs(nx) > .6)


def mano(x0, a=0.0):
    antebrazo = tubo([(x0, 55.4), (x0 + .5 + a * .3, 62), (x0 + 1 + a * .5, 68.6)], [3.8, 3.1, 2.4])
    rodilla = ovalo(x0 + 1.1 + a * .5, 69.6, 2.6, 2.2)
    cana = tubo([(x0 + 1.1 + a * .5, 70.4), (x0 + 1.4 + a * .6, 78.2)], [1.95, 1.8])
    menudillo = ovalo(x0 + 1.5 + a * .6, 79, 2.1, 1.8)
    cuartilla = tubo([(x0 + 1.6 + a * .6, 79.4), (x0 + 3 + a * .7, 82.4)], [1.75, 1.6])
    return [antebrazo, rodilla, cana, menudillo, cuartilla], pie(x0 + 3.6 + a * .7)


def pata(x0, a=0.0):
    pierna = forma([(x0 - 2, 45), (x0 + 3.8, 50), (x0 + 6.2, 56.4), (x0 + 5.6, 60.6), (x0 + 3, 64.4), (x0 + 2 + a, 68.6),
                    (x0 + 2 + a, 71), (x0 - 1.8 + a, 71.6), (x0 - 2.8, 68.4), (x0 - 3.8, 63.4), (x0 - 5, 57.6), (x0 - 7, 51.4)], 3)
    cana = tubo([(x0 + .2 + a, 70.8), (x0 + .4 + a, 78.2)], [1.95, 1.8])
    menudillo = ovalo(x0 + .5 + a, 79, 2.1, 1.8)
    cuartilla = tubo([(x0 + .6 + a, 79.4), (x0 + 2 + a, 82.4)], [1.75, 1.6])
    return [pierna, cana, menudillo, cuartilla], pie(x0 + 2.6 + a)


def pie(x):
    return forma([(x - 2.8, SUELO - 3), (x + 1.4, SUELO - 3.2), (x + 3.8, SUELO - 1.6), (x + 4.6, SUELO - .2), (x - 3.6, SUELO - .2),
                  (x - 4, SUELO - 1.6)], 2)


def dibujar(l):
    mano_l, pie_ml = mano(62.4, -1)
    pata_l, pie_pl = pata(44.4, 1.4)
    for partes, p in ((mano_l, pie_ml), (pata_l, pie_pl)):
        m = l.masa(partes + [p], material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
        l.pelaje(m, densidad=1.2, largo=1.3, ancho=.16, alfa=.22, semilla=41, claro=.3, flujo=95)
    ml = l.masa(manga(62.8), material='lejos', alto=.4, brillo=.05, vientre=0, linea=.6, hondo=0)
    l.pelaje(ml, densidad=3, largo=2.6, ancho=.22, alfa=.45, semilla=42, claro=.3, mechon=2, flujo=95)
    t = l.masa([tubo([(27.4, 43), (25.6, 50), (24.8, 56.4)], [.8, .62, .5]), forma([(24.6, 55.4), (26.2, 58.6), (25.6, 62.4),
                                                                                     (24, 62.8), (23.2, 59)], 2)],
               alto=.4, brillo=.05, vientre=0, linea=.55, hondo=0)
    l.pelaje(t, densidad=8, largo=1.8, ancho=.16, alfa=.4, semilla=43, claro=.3, flujo=95, zona=ovalo(24.6, 59.4, 2, 3.4))
    manos, pie_m = mano(67)
    patas, pie_p = pata(39.2)
    # la barba y la manga de este lado van en el mismo volumen que el cuerpo: pelo largo, no una pieza aparte
    c = l.masa([cuerpo(), barba(), manga(67.4)] + manos + patas + [pie_m, pie_p], brillo=.12, vientre=.35, contraluz=.3,
               bultos=[(ovalo(42, 29, 6.6, 5.6), .2), (ovalo(58.8, 28, 6.6, 5.6), .2), (ovalo(98.6, 30, 5, 3.6), .3),
                       (ovalo(36, 47, 8, 7), .1)])
    l.pelaje(c, densidad=1.1, largo=1.6, ancho=.18, alfa=.28, semilla=44, claro=.35, curva=8,
             flujo=lambda x, y: 100 if y > 50 else (160 if x < 66 else (70 if x < 88 else 190)))
    # el pelo largo y oscuro arriba de las jorobas y de la cabeza
    for zona in (ovalo(41.6, 25.6, 6.4, 3.4), ovalo(59, 24.6, 6.4, 3.4), ovalo(92.4, 26.8, 2.8, 2)):
        l.mancha(zona, '164F46', .5, dentro=c, difuso=1)
        l.pelaje(c, densidad=4, largo=2.4, ancho=.22, alfa=.5, semilla=45, claro=.25, mechon=2, zona=zona.buffer(1),
                 flujo=lambda x, y: 120 if x > 50 else 60)
    # la barba y la manga: más oscuras, de pelo largo que cae
    for zona, sem in ((barba(), 46), (manga(67.4), 47)):
        l.mancha(zona, '164F46', .55, dentro=c, difuso=.8)
        l.pelaje(c, densidad=3.4, largo=2.8, ancho=.22, alfa=.5, semilla=sem, claro=.3, mechon=2, zona=zona, flujo=97)
    # los callos de las rodillas; las líneas de la babilla y del corvejón; los dos dedos de cada pie
    for x, y, rx, ry in ((68.1, 69.6, 1.8, 2),):
        l.mancha(ovalo(x, y, rx, ry), '1F6D5A', .5, dentro=c, difuso=.2)
    for p in (((44.2, 56.4), (45.2, 60.6)), ((36.4, 66.4), (37.6, 70.4))):
        l.trazo(list(p), [.1, .26, .1], alfa=.3, dentro=c, difuso=.08)
    for x in (70.6, 41.8):
        l.trazo([(x + .8, SUELO - 2.8), (x + 1.1, SUELO - .3)], .22, alfa=.45, dentro=c)
    l.trazo([(106, 31.6), (104.9, 32.8), (105.2, 34)], .22, alfa=.55, dentro=c)
    l.mancha(ovalo(104.3, 29.6, .9, .35, 30), '0C3A33', .75, dentro=c)
    l.masa(forma([(90.2, 26.6), (88.6, 24.6), (89, 23), (90.8, 23.4), (92, 25.4)], 2), alto=.4, brillo=.05, vientre=0, linea=.5,
           hondo=0)
    for dx in (-.8, .4, 1.6):
        l.trazo([(96.2 + dx, 26.4), (96 + dx * 1.4, 25)], .16, alfa=.6)


CARA = dict(ojo=[96.6, 28.2], k=1.3, boca=[104.4, 34.4], kb=1.4, giro=12, pb=.7, wb=.6)
CARA['marco'] = [81.0, 14.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="54" cy="%.1f" rx="42" ry="4.4" style="opacity:.28"/>' % (SUELO + .4)
         + '<path d="M2 88q10-4 22-1.5t24-1M78 87.5q12-3.5 22-1t18-1.5" style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.45"/>')
LISTO = True
