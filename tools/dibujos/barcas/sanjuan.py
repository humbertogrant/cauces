# -*- coding: utf-8 -*-
"""El vapor del Tránsito, en el río San Juan, de memoria: un vapor chico de rueda y poco calado, como los de la compañía de Vanderbilt
que subían el río con pasajeros rumbo a California entre 1851 y 1857 (NAVES.sanjuan): casco bajo y chato, una sola cubierta con su
toldo de lona de borde festoneado sobre postes, una chimenea alta y fina adelante, la timonera chica encima del toldo y la rueda de
paletas a popa; en cubierta, los baúles de los viajeros.
"""
import numpy as np

from _barcas import agua, caja, cabina, chimenea, humo, olas_fondo, palo, poli, rueda

VISTA = (0, 10, 120, 74)
AGUA_Y = 74.0


def dibujar(l):
    rueda(l, 17.6, 67.4, 7.8, n=12)
    for y in (62.8, 66.4):
        palo(l, (13.2, y), (26, y + 1), .4, .4)
    c = l.masa(poli([(21, 68.4), (98, 68.4), (108.4, 66.2), (104.6, 71.6), (96, 74.8), (24, 74.8), (21.4, 72.6)], .4),
               material='acento', alto=.35, brillo=.25, vientre=0, hondo=0, contraluz=.2)
    l.trazo([(22, 71.2), (98, 71.2), (104.6, 69)], .14, alfa=.3, dentro=c)
    # la cubierta: la baranda, los postes del toldo y los baúles de los viajeros
    for x in np.arange(26, 94, 5.4):
        l.masa(caja(x - .3, 55.4, x + .3, 68.4, .1), material='claro', alto=.15, brillo=0, vientre=0, hondo=0, linea=.3, arroja=False)
    l.trazo([(24, 64.6), (94, 64.6)], .22, alfa=.6)
    for x, y, w, h in ((32, 64, 6, 4.4), (39, 65, 5, 3.4), (58, 64.2, 6.4, 4.2), (66, 65.2, 4.4, 3.2), (78, 64.4, 5.6, 4)):
        f = l.masa(caja(x, y, x + w, y + h, .5), material='lejos', alto=.35, brillo=.12, vientre=0, hondo=0, linea=.35, arroja=False)
        l.trazo([(x + .4, y + h * .45), (x + w - .4, y + h * .45)], .14, color='E8B952', alfa=.8, dentro=f)
    # el toldo de lona, con el borde festoneado
    borde = [(24, 55.4)] + [(x, 55.4 + (1.4 if k % 2 else .2)) for k, x in enumerate(np.arange(25.6, 95, 1.7))] + [(96, 55.4)]
    t = l.masa(poli([(22.4, 53.6), (97.6, 53.6)] + borde[::-1], .15), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0,
               linea=.45)
    for x in np.arange(28, 96, 6.6):
        l.trazo([(x, 53.8), (x, 55.4)], .12, color='8EB5AA', alfa=.6, dentro=t)
    cabina(l, 44, 47.4, 54, 53.6, ventanas=[(45.4, 48.8, 3, 2.8), (49.8, 48.8, 3, 2.8)], techo=.8)
    chimenea(l, 86, 54, 22, r=1.3)
    humo(l, 84.8, 18.4, n=5, deriva=(-5.2, -.8), r=2.2)
    palo(l, (106.4, 66.8), (107, 58.4), .3, .25)
    agua(l, AGUA_Y, sombra=poli([(10, 74), (106, 74), (102, 77.8), (14, 77.8)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
