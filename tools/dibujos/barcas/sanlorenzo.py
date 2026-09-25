# -*- coding: utf-8 -*-
"""La canoa de corteza de abedul del San Lorenzo, de memoria: la corteza clara cosida con raíces de abeto en paños, con las costuras
selladas con resina oscura; la borda de madera; las puntas altas, que suben y se curvan hacia atrás; tan liviana que se carga al
hombro en los rápidos y tan grande que llevaba toneladas de pieles: en el medio, los fardos de pieles de castor, y los remos de pala
larga (NAVES.sanlorenzo).
"""
import numpy as np

from _barcas import agua, fardo, olas_fondo, poli, remo
from _canoas import canoa, contorno
from pintor import forma

VISTA = (0, 46, 120, 34)
AGUA_Y = 72.0


def dibujar(l):
    borda, quilla = canoa(10, 112, 64.4, 7.6, sube_popa=8.6, sube_proa=8.6, panza=1.2)
    for x, y, w, h in ((34, 57.4, 8, 7.2), (43, 58.4, 7, 6.2), (51, 57, 8.4, 7.6), (60.4, 58.2, 7.4, 6.4), (69, 57.6, 8, 7)):
        fardo(l, x, y, w, h, material='lejos', ataduras=2)
    remo(l, (82, 63.4), 116, 16, material='lejos')
    c = l.masa(forma(contorno(borda, quilla), 1), material='claro', alto=.45, brillo=.2, vientre=0, hondo=0, contraluz=.25)
    # los paños de corteza, las costuras con resina y las lenticelas oscuras de la corteza de abedul
    for x in (24, 38, 52, 66, 80, 94):
        l.trazo([(x, 64.2), (x + .4, 68), (x, 71.4)], [.3, .45, .3], alfa=.8, dentro=c)
    rng = np.random.default_rng(4)
    for _ in range(46):
        x, y = rng.uniform(14, 108), rng.uniform(64.8, 71)
        l.trazo([(x - rng.uniform(.6, 1.4), y), (x + rng.uniform(.6, 1.4), y)], .16, color='3E7A6D', alfa=.5, dentro=c)
    # las puntas altas, que suben y se curvan hacia adentro, cosidas y selladas
    for s, (x, y) in ((1, borda[0]), (-1, borda[-1])):
        punta = forma([(x, y + 1.2), (x - s * 1.4, y - 2.2), (x - s * .4, y - 5.6), (x + s * 2.4, y - 6.8), (x + s * 4.4, y - 5.2),
                       (x + s * 3.4, y - 3.8), (x + s * 1.6, y - 4.4), (x + s * 1, y - 2.2), (x + s * 3.2, y + 1.6)], 2)
        pm = l.masa(punta, material='claro', alto=.35, brillo=.2, vientre=0, hondo=0, contraluz=.25, linea=.6)
        l.trazo([(x + s * .6, y), (x - s * .2, y - 3.2), (x + s * 1.6, y - 5.4)], [.3, .4, .2], alfa=.7, dentro=pm)
    # la borda de madera, que sigue la curva hasta las puntas
    l.masa(forma([(x, y - .1) for x, y in borda] + [(x, y + 1.3) for x, y in borda[::-1]], 1), material='acento', alto=.2, brillo=.2,
           vientre=0, hondo=0, linea=.4, arroja=False)
    remo(l, (30, 64.2), 118, 16)
    remo(l, (88, 64.2), 116, 16)
    agua(l, AGUA_Y, sombra=poli([(14, 72), (108, 72), (102, 75.6), (18, 75.6)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
