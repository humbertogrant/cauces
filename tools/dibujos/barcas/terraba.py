# -*- coding: utf-8 -*-
"""La lancha de Puerto Cortés, de memoria: una lancha larga y baja de madera, con la borda pintada y motor fuera de borda, de las que
suben por el Térraba y recorren los canales del manglar de Sierpe (NAVES.terraba); a bordo, de la carga del río (MERCADOS.terraba):
piñas y sacos.
"""
from _barcas import agua, fardo, motor_fuera, olas_fondo, poli, tablas
from _canoas import canoa, contorno
from pintor import forma, ovalo, tubo

VISTA = (0, 48, 120, 32)
AGUA_Y = 72.0


def pina(l, x, y):
    """una piña: el cuerpo con sus escamas en rombos y la corona de hojas"""
    p = l.masa(ovalo(x, y, 2.4, 3.2), material='acento', alto=.5, brillo=.2, vientre=0, hondo=0, linea=.35, arroja=False)
    for k in range(-3, 4):
        l.trazo([(x - 2 + k * .8, y - 2.6), (x + 2 + k * .8, y + 2.8)], .1, color='6B4E10', alfa=.6, dentro=p)
        l.trazo([(x + 2 + k * .8, y - 2.6), (x - 2 + k * .8, y + 2.8)], .1, color='6B4E10', alfa=.6, dentro=p)
    l.masa([tubo([(x, y - 3), (x + dx, y - 3 - abs(dx) * .3 - 3.4)], [.4, .1], 4) for dx in (-2.2, -1, 0, 1, 2.2)], material='cuerpo',
           alto=.2, brillo=.1, vientre=0, hondo=0, linea=.25, arroja=False)


def dibujar(l):
    borda, quilla = canoa(10, 114, 65.4, 6.8, sube_popa=.6, sube_proa=5.4, panza=1.2)
    for x in (64, 69.6, 75.2):
        pina(l, x, 61.6)
    fardo(l, 40, 60.4, 7, 4.4, material='claro')
    fardo(l, 48, 61, 6, 3.8, material='vientre')
    c = l.masa(forma(contorno(borda, quilla), 1), material='acento', alto=.45, brillo=.3, vientre=0, hondo=0, contraluz=.25)
    tablas(l, c, borda[1:-1], quilla[1:-1], n=3)
    l.mancha(forma(borda[:-1] + [(x, y + 1.6) for x, y in borda[-2::-1]], 1), 'E6EEEA', .85, dentro=c)       # la borda pintada
    l.trazo([(x, y + 1.9) for x, y in borda[1:-1]], .22, color='2F8A74', alfa=.85, dentro=c)
    motor_fuera(l, 10.6, 60.8, alto_=10.2)
    agua(l, AGUA_Y, sombra=poli([(12, 72), (108, 72), (102, 75.4), (16, 75.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
