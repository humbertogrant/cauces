# -*- coding: utf-8 -*-
"""La barcaza del Rin, de memoria: un buque de carga de 110 metros, de casco de acero largo y bajo, con la bodega tapada por las
tapas de las escotillas; a popa, la casa de la familia que vive a bordo y la timonera encima, alta para ver por arriba de la carga;
en cubierta, la bicicleta, y el coche encima de la escotilla, para bajarlo en el puerto; el ancla en la proa. Lleva 3 000 toneladas,
lo mismo que cien camiones (NAVES.rin).
"""
import numpy as np

from _barcas import agua, caja, cabina, olas_fondo, palo, poli
from pintor import forma, ovalo

VISTA = (0, 33, 120, 49)
AGUA_Y = 74.0


def dibujar(l):
    c = l.masa(poli([(4.4, 63.6), (110, 63.6), (116.4, 61.8), (114.6, 67.4), (108.4, 75.6), (8, 75.6), (4.4, 71)], .4),
               material='acento', alto=.35, brillo=.25, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(5, 66.6), (110, 66.6), (115.4, 64.4)], [.2, .5, .2], color='0C3A33', alfa=.6, dentro=c)      # la regala
    for x in np.arange(10, 110, 9.8):                                            # las planchas del casco
        l.trazo([(x, 67), (x, 75.2)], .1, alfa=.22, dentro=c)
    l.mancha(ovalo(112.4, 67, 1.2, 1), '0C3A33', .8, dentro=c)                  # el escobén del ancla
    # la bodega: las tapas de las escotillas, en fila
    for x in np.arange(30, 104, 7.4):
        e = l.masa(caja(x, 58.6, x + 7.2, 63.8, .3), material='lejos', alto=.25, brillo=.12, vientre=0, hondo=0, linea=.4, arroja=False)
        l.trazo([(x + 1, 59.6), (x + 6.2, 59.6)], .12, color='A4DCC4', alfa=.6, dentro=e)
    # el coche encima de la escotilla de popa
    auto = l.masa([forma([(30.6, 58.6), (31, 55.6), (33.4, 55.2), (35.4, 52.6), (41.8, 52.4), (44.4, 55.2), (46.6, 55.8), (46.8, 58.6)], 1)],
                  material='cuerpo', alto=.4, brillo=.35, vientre=.2, hondo=0, linea=.45)
    l.mancha(poli([(35.8, 53.2), (41.4, 53.2), (43.2, 55.4), (34.4, 55.4)], .2), '2F8A74', .8, dentro=auto)
    for x in (34, 43.2):
        l.masa(ovalo(x, 58.6, 1.5, 1.5), material='oscuro', alto=.3, brillo=.2, vientre=0, hondo=0, linea=.35)
    # la casa de la familia, a popa, y la timonera encima
    cabina(l, 7, 55, 28.4, 63.6, ventanas=[(9, 57, 3.4, 3), (14, 57, 3.4, 3), (19, 57, 3.4, 3), (23.6, 57, 3.4, 3)], techo=.8)
    cabina(l, 10.6, 44.6, 25, 53.8, ventanas=[(12, 46.4, 11.6, 3.6)], techo=1.2)
    l.masa(caja(16.6, 53.8, 19.2, 55, .1), material='lejos', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.35)
    palo(l, (21.6, 43.4), (21.8, 37.4), .25, .2, material='oscuro')             # el mástil del radar
    l.masa(caja(18.6, 36.6, 25, 37.6, .2), material='oscuro', alto=.2, brillo=.2, vientre=0, hondo=0, linea=.3)
    palo(l, (5.6, 63), (5.4, 52), .22, .2, material='oscuro')                   # el asta de la bandera de popa
    l.masa(poli([(5.6, 52.4), (11.2, 52.8), (11, 56.2), (5.6, 55.6)], .15), material='claro', alto=.1, brillo=.1, vientre=0, hondo=0,
           linea=.3)
    # la bicicleta en cubierta, junto a la casa
    for x in (29.8, 35.2):
        l.trazo([(x + 1.6 * np.cos(a), 61.2 + 1.6 * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 20)], .2, alfa=.85)
    l.trazo([(29.8, 61.2), (32, 58.8), (35.2, 61.2), (32.6, 61.2), (29.8, 61.2)], .22, alfa=.85)
    l.trazo([(32, 58.8), (31.6, 58), (32.8, 57.8)], .22, alfa=.85)
    l.trazo([(34.2, 58.6), (34.6, 57.8)], .22, alfa=.85)
    agua(l, AGUA_Y, x0=0, x1=120, sombra=poli([(6, 74), (112, 74), (108, 78), (10, 78)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
