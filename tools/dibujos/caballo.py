# -*- coding: utf-8 -*-
"""Bucéfalo, Rabona y Ceniza: el caballo (Equus caballus), de memoria, parado y atento, con proporciones de caballo: la altura en
la cruz casi igual al largo del cuerpo (de la punta del hombro a la punta de la nalga), la cabeza de unos dos quintos de esa
altura, el cuello grueso y arqueado, la grupa redonda y poderosa; las patas de adelante con el codo pegado al pecho, el antebrazo
musculoso, la «rodilla» (que es la muñeca), la caña fina, el menudillo, la cuartilla inclinada y el casco; las de atrás con la
babilla junto a la panza, la pierna que baja hacia atrás hasta el corvejón (el talón, en punta hacia atrás) y la caña recta; la
crin cae hacia un lado del cuello, el copete sobre la frente, las orejas en punta hacia adelante, ollares grandes; la cola larga.
"""

from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 0, 120, 90)
SUELO = 85.0


def cuerpo():
    """el tronco, el cuello y la cabeza, en una sola pieza, con la quijada ancha y el hocico lleno"""
    return forma([(25.5, 47), (27, 43.5), (31, 41.2), (36, 40.6), (42, 41.8), (48, 42.6), (54, 42.4), (59, 41), (62.5, 39.5),
                  (66, 35.5), (70.5, 29.5), (75, 24.5), (79, 21.2), (81.4, 20.4), (83.6, 21.2), (85.6, 23.2), (88.4, 27.2),
                  (91.4, 31.2), (93.6, 34), (95, 36.4), (95, 38.6), (93.6, 40), (91.4, 40.6), (89.6, 39.6), (87.4, 39.4),
                  (84.8, 38.4), (82.6, 36), (82, 33), (80.6, 36), (78.4, 41), (76, 46.4), (73.8, 51), (72, 55.4), (69.5, 60.2),
                  (64, 62.8), (56, 63.6), (48, 63.4), (42.5, 62.4), (38.5, 61.2), (33.5, 61.4), (29.2, 59.2), (26.2, 55),
                  (25, 51)], 3)


def mano(x0, a=0.0):
    """la pata de adelante: el antebrazo musculoso desde el codo, la rodilla, la caña, el menudillo, la cuartilla y el casco"""
    antebrazo = tubo([(x0, 56.5), (x0 + .5 + a * .3, 63), (x0 + .9 + a * .5, 69.8)], [3.3, 2.7, 1.95])
    rodilla = ovalo(x0 + 1 + a * .5, 70.4, 2.1, 1.7)
    cana = tubo([(x0 + 1 + a * .5, 71), (x0 + 1.2 + a * .6, 78.6)], [1.5, 1.4])
    menudillo = ovalo(x0 + 1.4 + a * .6, 79.4, 1.8, 1.6)
    cuartilla = tubo([(x0 + 1.5 + a * .6, 79.8), (x0 + 3.2 + a * .7, 82.4)], [1.45, 1.3])
    return [antebrazo, rodilla, cana, menudillo, cuartilla], casco(x0 + 3.8 + a * .7)


def pata(x0, a=0.0):
    """la de atrás: la pierna, en cuña desde el muslo hasta el corvejón (el talón, en punta hacia atrás); la caña recta"""
    pierna = forma([(x0 + 1, 59.5), (x0 - .3, 64.5), (x0 - 2.1, 68.2), (x0 - 2.6 + a, 70.4), (x0 - 5.3 + a, 70.8),
                    (x0 - 6.5 + a, 69.4), (x0 - 8.3, 65.2), (x0 - 10.5, 60.6), (x0 - 11.8, 56.5), (x0 - 6, 57)], 2)
    cana = tubo([(x0 - 4 + a, 70.6), (x0 - 3.7 + a, 78.6)], [1.55, 1.42])
    menudillo = ovalo(x0 - 3.4 + a, 79.4, 1.8, 1.6)
    cuartilla = tubo([(x0 - 3.3 + a, 79.8), (x0 - 1.7 + a, 82.4)], [1.45, 1.3])
    return [pierna, cana, menudillo, cuartilla], casco(x0 - 1.1 + a)


def casco(x):
    return forma([(x - 2.1, SUELO - 3), (x + 1.2, SUELO - 3), (x + 2.6, SUELO - .1), (x - 2.3, SUELO - .1)], 1)


def cola():
    return forma([(28.2, 43), (25, 45.5), (22.4, 51), (21.2, 58.5), (21.4, 66), (22.8, 72.5), (25, 76.2), (26.2, 74.2), (25.4, 68),
                  (25.6, 60), (26.6, 52.5), (28.8, 47)], 3)


def crin():
    """la crin cae hacia este lado del cuello, en mechones"""
    borde = [(80.6, 20.2), (77.4, 22.2), (73.4, 25.8), (69.4, 30.6), (65.6, 35.6), (62.6, 39.2)]
    abajo = [(64.4, 41.2), (67.6, 38.8), (68.6, 36.8), (71.2, 34.4), (72.4, 31.6), (75.2, 29.6), (76.4, 26.6), (79.2, 25),
             (80.6, 22.6), (82.2, 21.6)]
    return forma(borde + abajo, 2)


def copete():
    return forma([(81.8, 19.6), (84, 19.8), (85.6, 21.6), (86, 24.2), (84.6, 23.4), (83.2, 21.8)], 2)


def dibujar(l):
    mano_l, casco_ml = mano(63.4, -1.2)
    pata_l, casco_pl = pata(45.2, 1.2)
    for partes, c in ((mano_l, casco_ml), (pata_l, casco_pl)):
        l.masa(partes, material='lejos', alto=.6, brillo=.05, vientre=0, linea=.7, hondo=0)
        l.masa(c, material='oscuro', alto=.3, brillo=.15, vientre=0, linea=.5, hondo=0)
    t = l.masa(cola(), material='lejos', alto=.35, brillo=.2, vientre=0, linea=.75, hondo=0)
    l.pelaje(t, densidad=3, largo=4.5, ancho=.28, flujo=lambda x, y: 95 + (y - 60) * .9, alfa=.35, semilla=3, curva=6)
    manos, casco_m = mano(68.4, 1.4)
    patas, casco_p = pata(39.5, 0)
    c = l.masa([cuerpo()] + manos + patas, alto=.85, brillo=.28, vientre=.4,
               bultos=[(ovalo(33, 48.5, 9, 9.5), .22), (forma([(61, 40), (67, 40), (74, 48.5), (70, 55), (64, 50)], 3), .18),
                       (ovalo(86, 34.8, 4.2, 3.4), .5), (ovalo(69.8, 60.5, 3, 4), .18), (ovalo(84.6, 24.4, 2.6, 2.2), .25)])
    l.pelaje(c, densidad=1.1, largo=1.3, ancho=.16, flujo=lambda x, y: 195 + (y - 50) * .6, alfa=.12, semilla=4)
    # la línea del hombro, la de la quijada, la del codo y la de la babilla; las venas de la cara
    for p in (((63, 41.5), (67.5, 46.5), (71.5, 51)), ((83, 32.4), (85.6, 37.2), (89.4, 39.4)), ((70.6, 57.4), (68.6, 60)),
              ((40.8, 58.6), (38.6, 61.4)), ((86.8, 28.6), (89.4, 32.6))):
        l.trazo(list(p), [.12, .3, .12], alfa=.3, dentro=c, difuso=.05)
    l.trazo([(78.4, 41), (75.6, 44.6), (73.8, 48.4)], [.1, .26, .1], alfa=.22, dentro=c, difuso=.1)   # el surco de la yugular
    for m_ in (casco_m, casco_p):
        l.masa(m_, material='oscuro', alto=.3, brillo=.15, vientre=0, linea=.5, hondo=0)
    l.mancha(forma([(92.2, 33.2), (93.6, 33.6), (93.8, 35.4), (92.8, 35.8), (92.3, 34.6)], 2), '0C3A33', .8, dentro=c)   # el ollar
    l.trazo([(92.2, 38.8), (93.9, 38.4)], .25, alfa=.5, dentro=c)
    m = l.masa(crin(), material='lejos', alto=.35, brillo=.2, vientre=0, linea=.6, hondo=0)
    l.pelaje(m, densidad=4, largo=3.2, ancho=.24, flujo=lambda x, y: 118 - (x - 62) * .3, alfa=.4, semilla=5, curva=10)
    l.masa(forma([(81.2, 20.6), (82.4, 15.2), (84.2, 20.4)], 2), material='lejos', alto=.4, brillo=.05, vientre=0, linea=.5, hondo=0)
    l.masa(forma([(82.6, 20.8), (84.4, 15), (85.6, 20.8)], 2), alto=.4, brillo=.1, vientre=0, linea=.55, hondo=0)      # las orejas
    cp = l.masa(copete(), material='lejos', alto=.3, brillo=.15, vientre=0, linea=.5, hondo=0)
    l.pelaje(cp, densidad=6, largo=2, ancho=.2, flujo=60, alfa=.35, semilla=6)
    l.mancha(ovalo(87.4, 26.6, .9, .7, 30), 'D6F3E4', .5, dentro=c, difuso=.2)    # la estrella de la frente


CARA = dict(ojo=[85.9, 25.4], k=1.3, boca=[92.2, 38.6], kb=1.3, giro=18, pb=.7, wb=.6)
CARA['marco'] = [72.0, 12.0, 30, 30]
FONDO = ('<ellipse class="sombra" cx="52" cy="%.1f" rx="38" ry="4.2" style="opacity:.28"/>' % (SUELO + .4)
         + '<path d="M8 88q.3-2.8-1-4.6M10.5 88.4q.2-3 1.4-4.6M104 88q-.3-3 1.2-5M106.4 88.4q0-2.8 1.6-4.4"' + AGUA + '/>')
LISTO = True
