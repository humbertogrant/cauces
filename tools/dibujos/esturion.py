# -*- coding: utf-8 -*-
"""Belu, el esturión beluga (Huso huso), de memoria: cuerpo largo sin escamas pero con filas de placas de hueso (una en el lomo,
una a cada lado a media altura y otra cerca de la panza), hocico corto y puntiagudo, cuatro barbillas aplanadas debajo del hocico,
delante de una boca grande en media luna, aleta dorsal muy atrás, cerca de la cola, y la cola como la de un tiburón, con el lóbulo
de arriba más largo, por donde siguen las placas. Lomo oscuro, panza clara. Nada sobre el fondo del río.
"""
import numpy as np
from shapely.geometry import Polygon

from _perfil import Perfil
from pintor import tubo

VISTA = (0, 26, 120, 44)
S = [0.000, 0.020, 0.050, 0.090, 0.130, 0.180, 0.230, 0.300, 0.380, 0.460, 0.540, 0.620, 0.700, 0.760, 0.790]
ARRIBA = [0.008, 0.019, 0.033, 0.050, 0.065, 0.078, 0.087, 0.094, 0.096, 0.093, 0.084, 0.070, 0.053, 0.042, 0.037]
ABAJO = [0.007, 0.014, 0.024, 0.037, 0.050, 0.061, 0.070, 0.078, 0.082, 0.080, 0.072, 0.059, 0.044, 0.033, 0.029]
F = Perfil(S, ARRIBA, ABAJO, 100, giros=((0, 2), (.5, 0), (1, -2)))


def a(s):
    return float(F.arriba(s))


def b(s):
    return float(F.abajo(s))


def placas_lomo(s):
    """la fila de placas del lomo asoma en el contorno como dientes de sierra romos"""
    s = np.asarray(s, float)
    m = (s > .19) & (s < .64)
    fase = np.clip((s - .19) / .041, 0, None) % 1
    return np.where(m, .007 * np.clip(1 - np.abs(fase - .5) * 2.4, 0, 1), 0)


def dorsal():
    return F.pieza([(0.635, a(.635) - .01), (0.655, a(.655) + .04), (0.672, a(.672) + .05), (0.69, a(.69) + .036),
                    (0.715, a(.715) + .012), (0.735, a(.735) - .006)], 1)


def anal():
    return F.pieza([(0.655, -b(.655) + .008), (0.672, -b(.672) - .03), (0.69, -b(.69) - .036), (0.705, -b(.705) - .024),
                    (0.725, -b(.725) - .004), (0.735, -b(.735) + .006)], 1)


def cola():
    return F.pieza([(0.77, 0.036), (0.84, 0.052), (0.91, 0.072), (0.97, 0.09), (1.005, 0.103), (0.99, 0.086), (0.95, 0.064),
                    (0.91, 0.04), (0.885, 0.012), (0.89, -0.02), (0.905, -0.055), (0.905, -0.078), (0.88, -0.07),
                    (0.84, -0.048), (0.8, -0.032), (0.77, -0.028)], 1)


def pectoral():
    return F.pieza([(0.19, -0.046), (0.24, -0.066), (0.285, -0.09), (0.296, -0.1), (0.275, -0.1), (0.24, -0.088),
                    (0.21, -0.07)], 2)


def pelvica():
    return F.pieza([(0.54, -b(.54) + .008), (0.565, -b(.565) - .02), (0.585, -b(.585) - .03), (0.588, -b(.588) - .018),
                    (0.575, -b(.575) + .004)], 1)


def barbillas():
    """dos de las cuatro se ven: cortas, colgando delante de la boca"""
    return [tubo(F.linea([(s, -b(s) + .003), (s - .006, -b(s) - .012), (s - .009, -b(s) - .02)]), [.38, .32, .22])
            for s in (.05, .068)]


def todo():
    return [F.cuerpo(joroba=placas_lomo), dorsal(), anal(), cola(), pectoral(), pelvica()] + barbillas()


F.encuadrar(todo, (8, 30, 112, 61))


def dibujar(l):
    fin = dict(alto=.3, brillo=.12, vientre=0, linea=.7, hondo=0)
    l.masa(barbillas()[0], material='lejos', alto=.3, brillo=0, vientre=0, linea=.4, hondo=0)      # la del otro lado, detrás
    l.masa(dorsal(), **fin)
    l.masa(anal(), **fin)
    l.masa(cola(), **fin)
    corte = Polygon(F.linea([(0.78, 0.2), (0.82, 0.2), (0.82, -0.2), (0.78, -0.2)]))
    cuerpo = l.masa(F.cuerpo(joroba=placas_lomo), brillo=.22, vientre=.85, sin_tinta=corte)
    # las placas: la fila de un costado a media altura y la de la panza, como rombos claros con borde oscuro
    for fila, (s0, s1, n, y) in enumerate(((.22, .79, 26, lambda s: float(F.medio(s)) + .008),
                                           (.26, .6, 9, lambda s: -b(s) + .016))):
        for s in np.linspace(s0, s1, n):
            t = .0085 if fila == 0 else .008
            h = .0075 if fila == 0 else .006
            rombo = F.pieza([(s - t, y(s)), (s, y(s) + h), (s + t, y(s)), (s, y(s) - h)], 1)
            l.mancha(rombo, 'CDEFE3', .7, dentro=cuerpo)
            l.mancha(rombo.boundary.buffer(.12), '0C3A33', .35, dentro=cuerpo)
    for s in np.arange(.8, .98, .03):                # las placas siguen por el lóbulo de arriba de la cola
        y = .04 + (s - .8) * .33
        l.mancha(F.pieza([(s - .007, y), (s, y + .006), (s + .007, y), (s, y - .006)], 1), 'CDEFE3', .5)
    l.trazo(F.linea([(0.17, 0.07), (0.188, 0.035), (0.194, -0.005), (0.188, -0.04), (0.176, -0.06)]), [.2, .45, .5, .4, .2],
            alfa=.5, dentro=cuerpo)                   # el borde del opérculo
    l.masa(barbillas()[1], alto=.3, brillo=0, vientre=0, linea=.4, hondo=0)
    l.masa(pelvica(), **dict(fin, raices=[(*F.P(.56, -b(.56)), .8, 2.2)]))
    l.masa(pectoral(), alto=.3, brillo=.1, vientre=0, linea=.7, raices=[(*F.P(.195, -.052), 1.0, 2.8)], hondo=0)


CARA = dict(ojo=F.p(.082, .024), k=1.05, boca=F.p(.1, -.052), kb=1.8, giro=round(-F.grados(.1)) + 8, pb=.6, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 15, 1), round(CARA['ojo'][1] - 15, 1), 30, 30]
FONDO = ('<path class="sombra" d="M0 64Q30 61 60 63.5T120 62V70H0Z" style="opacity:.22"/>'
         '<ellipse class="sombra" cx="26" cy="66" rx="4" ry="1.4" style="opacity:.3"/><ellipse class="sombra" cx="88" cy="66.4" rx="5" ry="1.6" style="opacity:.3"/>')
LISTO = True
