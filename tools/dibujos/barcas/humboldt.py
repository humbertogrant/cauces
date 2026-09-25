# -*- coding: utf-8 -*-
"""La canoa de Humboldt y Bonpland en el Orinoco, de memoria: una canoa larga, un tronco vaciado, con un toldo bajo de hojas de palma a
popa, donde viajaban apretados con sus cosas; a bordo, los baúles de los instrumentos (llevaban unos cuarenta) y los atados de plantas
secas entre papeles, que al final del viaje eran unas 60 000 (el vehículo de la ruta en ITINERARIOS); los canaletes de los remeros.
"""
import numpy as np

from _barcas import agua, caja, olas_fondo, paja, poli, remo
from _canoas import canoa, contorno
from pintor import forma, ovalo

VISTA = (0, 47, 120, 35)
AGUA_Y = 72.0


def baul(l, x, y, w, h):
    """un baúl de instrumentos: la caja, la tapa con su canto, los herrajes"""
    b = l.masa(caja(x, y, x + w, y + h, .3), material='lejos', alto=.35, brillo=.15, vientre=0, hondo=0, linea=.4, arroja=False)
    l.trazo([(x + .3, y + h * .3), (x + w - .3, y + h * .3)], .2, color='0D3530', alfa=.8, dentro=b)
    for xx in (x + w * .25, x + w * .75):
        l.mancha(caja(xx - .4, y + .2, xx + .4, y + h - .2, .1), 'E8B952', .85, dentro=b)
    return b


def dibujar(l):
    borda, quilla = canoa(10, 114, 65, 7.2, sube_popa=2.4, sube_proa=4.8, panza=1.4)
    # el toldo de hojas de palma, a popa, bajo y abovedado
    t = paja(l, [(16, 64.4), (16.6, 57.6), (19.4, 53.4), (24, 51.4), (30, 50.6), (40, 50.6), (46, 51.4), (50.4, 53.6), (52.4, 57.6),
                 (52.8, 64.4)], flujo=100, veces=1, densidad=3)
    l.mancha(poli([(46.4, 64.4), (46.6, 57.6), (48.4, 54.8), (50.6, 55.4), (51.6, 58.4), (51.8, 64.4)], .3), '0D3530', .85, dentro=t)
    for x in (24, 32, 40):                                          # los aros de la armazón
        l.trazo([(x, 51.2 + abs(x - 34) * .05), (x - .2, 64.2)], [.25, .3, .25], color='164F46', alfa=.55, dentro=t)
    for x in np.arange(18, 51, 2.4):                                # las hojas de palma, que caen en capas
        for y in (54.4, 58.4, 62.2):
            l.trazo([(x, y), (x + .6, y + 1.8)], [.12, .04], color='E6EEEA', alfa=.45, dentro=t)
    # los baúles de los instrumentos y los atados de plantas secas entre papeles
    for x, y, w, h in ((55, 58.4, 7.4, 6.2), (63, 59.6, 6, 5), (70.4, 58.8, 7, 5.8)):
        baul(l, x, y, w, h)
    for x, y in ((79, 59.6), (85.4, 60.2)):
        a = l.masa(caja(x, y, x + 5.6, y + 4.8, .3), material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.35, arroja=False)
        for k in range(4):
            l.trazo([(x + .3, y + .9 + k * 1.1), (x + 5.3, y + .9 + k * 1.1)], .1, color='8EB5AA', alfa=.8, dentro=a)
        l.trazo([(x + 2.8, y + .1), (x + 2.8, y + 4.7)], .2, color='0C3A33', alfa=.6, dentro=a)
        for dx, dy in ((1, -1.2), (2.4, -1.8), (4, -1.4)):
            l.masa(ovalo(x + dx, y + dy + .6, .9, .45, -30), material='cuerpo', alto=.2, brillo=.1, vientre=0, hondo=0, linea=.2,
                   arroja=False)                                     # las hojas que asoman
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.5, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    l.trazo([(x, y + .9) for x, y in borda[1:-1]], [.1] + [.6] * 13 + [.1], color='93701A', alfa=.5, dentro=c, difuso=.15)
    for k in range(2):
        l.trazo([(20 + k * 4, 68.2 + k * 1.6), (60, 69.4 + k * 1.6), (104 - k * 4, 68 + k * 1.4)], [.05, .14, .05], color='93701A',
                alfa=.45, dentro=c)
    for x in (58, 74, 92):                                          # los canaletes de los remeros
        remo(l, (x, 64.2), 110, 15, pala=4, ancho=1.8)
    agua(l, AGUA_Y, sombra=poli([(12, 72), (108, 72), (102, 75.4), (18, 75.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
