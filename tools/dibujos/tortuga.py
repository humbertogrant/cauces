# -*- coding: utf-8 -*-
"""Marea, la tortuga verde (Chelonia mydas), de memoria, nadando de perfil: caparazón bajo y liso, en forma de lágrima, con escudos
grandes que no se montan (cuatro a cada costado) y una fila de escudos chicos en el borde; cabeza redonda y chica para su cuerpo, con
escamas y un pico corto y romo (la mandíbula de abajo, aserrada); aletas delanteras largas como alas, con una uña, y las de atrás
cortas y redondas. Vuela bajo el agua: la aleta cercana baja y la lejana sube.
"""
import numpy as np

from pintor import AGUA, forma, ovalo, tubo

VISTA = (0, 6, 120, 78)


def caparazon():
    return forma([(88, 44.5), (84, 37.5), (76, 32), (64, 29), (51, 29.5), (40, 32.5), (31, 38.5), (25.5, 45), (24, 49.5),
                  (30, 52), (44, 53.5), (60, 54), (75, 53), (86, 50.5)], 3)


def plastron():
    return forma([(30, 51), (44, 53.2), (60, 53.8), (75, 52.8), (86, 50.3), (84, 55.5), (74, 58.5), (60, 59.5), (45, 59),
                  (34, 56.5)], 2)


def cabeza():
    cuello = tubo([(82, 50), (89, 48.5), (94, 47.2)], [4.6, 4.2, 3.9])
    craneo = forma([(92, 42.5), (97.5, 40.2), (103, 40.8), (107, 43.2), (109, 46.4), (108.6, 49), (105.5, 50.6), (100, 51.2),
                    (94, 50.4), (90.5, 47.5)], 3)
    return cuello, craneo


def aleta_cerca():
    return forma([(84, 49.5), (80, 54), (73, 60.5), (64, 67.5), (55, 73.5), (48.5, 77), (47, 76.2), (51, 71.5), (58, 64.5),
                  (66, 57.5), (73, 52.5), (79, 49)], 3)


def aleta_lejos():
    return forma([(83, 41), (78, 36), (71, 29), (63, 22), (56, 16.5), (53, 15.5), (55, 18.5), (61, 26), (68, 33.5), (75, 40),
                  (80, 43.5)], 3)


def dibujar(l):
    l.masa(aleta_lejos(), material='lejos', alto=.3, brillo=.1, vientre=0, linea=.75, hondo=0)
    l.masa(forma([(33, 51), (27, 54), (20.5, 57.5), (19, 59.5), (23, 60), (29.5, 58), (35, 55.5)], 3), material='lejos', alto=.3,
           brillo=.05, vientre=0, linea=.7, hondo=0)                                    # la aleta de atrás, del otro lado
    cuello, craneo = cabeza()
    ca = l.masa([cuello, craneo], brillo=.3, vientre=.4, linea=.8, bultos=[(ovalo(101, 45, 5, 3.6), .4)])
    # las escamas de la cabeza: placas grandes, con bordes oscuros
    for trazo_ in (((96.5, 41.5), (98.5, 45.5), (96.5, 49.5)), ((102, 41.2), (103.2, 43.6)), ((99, 46.8), (104.5, 47.6)),
                   ((92.5, 44), (95, 45.5))):
        l.trazo(list(trazo_), .22, alfa=.35, dentro=ca)
    l.trazo([(104.8, 49.3), (106.2, 49.8), (107.4, 49.4), (108.3, 48.6)], .3, alfa=.6, dentro=ca)     # la mandíbula aserrada
    l.masa(plastron(), material='claro', alto=.3, brillo=.1, vientre=0, linea=.75, hondo=0)
    cap = l.masa(caparazon(), alto=.6, brillo=.3, vientre=.35, linea=.85, escalon=.1, contraluz=.3, bultos=[(ovalo(58, 40, 24, 10), .1)])
    # los escudos: la fila del lomo arriba, cuatro grandes a este costado y los chicos del borde; cada escudo grande con sus rayos,
    # que salen de donde empezó a crecer (el dibujo de sol de la tortuga verde)
    A = [(31, 40.4), (43, 36), (56, 34.4), (69.4, 35.2), (81.6, 39.6)]            # entre la fila del lomo y la de los costados
    B = [(27.4, 48.4), (41.4, 50), (55.6, 50.8), (70, 50.4), (84.6, 47.8)]        # entre los costados y el borde
    l.trazo(A, [.3, .4, .4, .4, .3], alfa=.55, dentro=cap, difuso=.05)
    l.trazo(B, [.3, .4, .4, .4, .3], alfa=.55, dentro=cap, difuso=.05)
    rng = np.random.default_rng(12)
    for i in range(4):
        a0, a1, b0, b1 = np.array(A[i]), np.array(A[i + 1]), np.array(B[i]), np.array(B[i + 1])
        if i:
            l.trazo([a0, (a0 + b0) / 2 + [.6, 0], b0], [.4, .4, .35], alfa=.55, dentro=cap, difuso=.05)
        centro = a0 * .5 + a1 * .2 + b0 * .3 + rng.uniform(-.6, .6, 2)
        l.mancha(forma([a0, a1, b1, b0], 1).buffer(-.6), 'D2F2DA', .16, dentro=cap, difuso=1.2)
        for f in np.linspace(.08, .92, 7):
            q = b0 + (b1 - b0) * f if f < .6 else a1 + (b1 - a1) * (f - .3)
            l.trazo([centro, centro + (q - centro) * rng.uniform(.75, .92)], [.06, .16], color='11443F', alfa=.2, dentro=cap, difuso=.12)
    for x in (37, 49.6, 62.6, 75.4):                                            # la fila del lomo
        y = float(np.interp(x, [a[0] for a in A], [a[1] for a in A]))
        l.trazo([(x - .6, y - 5.4), (x, y)], [.1, .35], alfa=.45, dentro=cap, difuso=.05)
    for x in np.arange(29.6, 86, 3.3):                                           # los escudos chicos del borde
        y = float(np.interp(x, [b[0] for b in B], [b[1] for b in B]))
        l.trazo([(x, y), (x + .3, y + 3.2)], [.3, .12], alfa=.45, dentro=cap)
    l.masa(forma([(35, 52.5), (29, 57.5), (24.5, 61), (24, 63), (28.5, 62.5), (34, 59), (37.5, 55.5)], 3), alto=.3, brillo=.1,
           vientre=0, linea=.72, hondo=0)                                              # la aleta de atrás, de este lado
    ap = l.masa(aleta_cerca(), alto=.3, brillo=.2, vientre=0, linea=.8, hondo=0, raices=[(82.5, 50.5, 1.5, 4.5)], funde=False)
    for k in range(9):                                                                # las escamas del borde de adelante
        f = .12 + k * .085
        q = np.array([83 - 34 * f, 50 + 26.4 * f])
        l.trazo([q + [-.4, -1.2], q + [.9, .2], q + [-.2, 1.4]], [.08, .2, .08], alfa=.3, dentro=ap, difuso=.05)
    l.mancha(forma([(60.6, 65), (62, 66.2), (60.4, 67.2)], 1), '0C3A33', .8)            # la uña


CARA = dict(ojo=[101.8, 44.4], k=1.35, boca=[104.6, 48.6], kb=2.4, giro=10, pb=.5, wb=.7)
CARA['marco'] = [83.0, 28.0, 32, 32]
FONDO = ('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M20 16.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
         '<circle cx="111" cy="36" r="1.1"' + AGUA + '/><circle cx="113" cy="31.5" r=".75"' + AGUA + '/>')
LISTO = True
