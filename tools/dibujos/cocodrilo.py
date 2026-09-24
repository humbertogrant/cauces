# -*- coding: utf-8 -*-
"""Lalo y Tami, el cocodrilo americano (Crocodylus acutus) y el del Orinoco (C. intermedius), de memoria: hocico largo y más bien
angosto, con los dientes a la vista aunque cierre la boca (el cuarto de abajo encaja por fuera, en una muesca de la mandíbula de
arriba), la nariz en una almohadilla en la punta, los ojos arriba de la cabeza, sobre dos bultos; el lomo con filas de placas de
hueso y la cola con una cresta doble de escamas en sierra; las patas cortas, con cinco dedos adelante y cuatro atrás. Toma el sol
echado en un banco de arena, con la punta de la cola en el agua.
"""
import numpy as np

from _patas import dedos, garra, miembro
from _perfil import Perfil
from pintor import AGUA, ovalo

VISTA = (0, 40, 120, 50)
S = [0.000, 0.015, 0.030, 0.060, 0.090, 0.110, 0.125, 0.140, 0.160, 0.190, 0.230, 0.280, 0.330, 0.380, 0.430, 0.480, 0.550,
     0.650, 0.750, 0.850, 0.950, 1.000]
ARRIBA = [0.013, 0.019, 0.017, 0.018, 0.022, 0.029, 0.037, 0.040, 0.038, 0.043, 0.053, 0.061, 0.065, 0.064, 0.060, 0.052,
          0.043, 0.033, 0.024, 0.016, 0.009, 0.004]
ABAJO = [0.011, 0.013, 0.013, 0.014, 0.016, 0.019, 0.023, 0.027, 0.032, 0.038, 0.045, 0.050, 0.051, 0.050, 0.045, 0.037,
         0.029, 0.022, 0.016, 0.011, 0.006, 0.003]
F = Perfil(S, ARRIBA, ABAJO, 102, giros=((0, 1), (.5, 0), (.7, 3), (.85, 22), (1, 52)))


def escamas(s):
    """las placas del lomo asoman como bultos; en la cola, la cresta doble en sierra"""
    s = np.asarray(s, float)
    lomo = np.where((s > .17) & (s < .5), .0028 * np.abs(np.sin((s - .17) * np.pi / .022)), 0)
    fase = np.clip((s - .5) / .028, 0, None) % 1
    sierra = np.where((s >= .5) & (s < .97), np.interp(s, [.5, .97], [.0065, .0025]) * np.clip(1 - np.abs(fase - .5) * 2.2, 0, 1), 0)
    return lomo + sierra


def pata_delante(lejos=False):
    d = -.006 if lejos else 0
    brazo = miembro(F.linea([(0.212 + d, 0.004), (0.232 + d, -0.02), (0.258 + d, -0.036), (0.238 + d, -0.052)]), [2.3, 1.9, 1.4, 1.05])
    ds, puntas = dedos(F.P(0.232 + d, -0.055), 6, [1.5, 2.1, 2.4, 2.1, 1.4], abanico=55, grueso=(.55, .32), curva=6)
    return brazo, ds, puntas


def pata_atras(lejos=False):
    d = .03 if lejos else 0
    pierna = miembro(F.linea([(0.44 + d, 0.006), (0.415 + d, -0.018), (0.398 + d, -0.034), (0.452 + d, -0.05)]), [3.2, 2.6, 1.9, 1.15])
    ds, puntas = dedos(F.P(0.446 + d, -0.055), 3, [2.1, 2.9, 3.1, 2.6], abanico=40, grueso=(.6, .34), curva=5)
    return pierna, ds, puntas


def muslos():
    """el brazo y el muslo de este lado, hasta el codo y la rodilla: van en el mismo volumen que el cuerpo"""
    return [miembro(F.linea([(0.212, 0.004), (0.232, -0.02), (0.256, -0.035)]), [2.4, 2.0, 1.55]),
            miembro(F.linea([(0.44, 0.006), (0.415, -0.018), (0.4, -0.033)]), [3.3, 2.8, 2.1])]


def bajos():
    """de la rodilla y del codo para abajo, con los dedos"""
    out = []
    for eje, radios, base, g, largos, ab in (([(0.256, -0.035), (0.238, -0.052)], [1.45, 1.05], (0.232, -0.055), 6,
                                               [1.5, 2.1, 2.4, 2.1, 1.4], 55),
                                              ([(0.4, -0.033), (0.452, -0.05)], [1.95, 1.15], (0.446, -0.055), 3,
                                               [2.1, 2.9, 3.1, 2.6], 40)):
        ds, puntas = dedos(F.P(*base), g, largos, abanico=ab, grueso=(.6, .34), curva=5)
        out.append((miembro(F.linea(eje), radios), ds, puntas, F.P(*eje[0])))
    return out


def todo():
    return [F.cuerpo(joroba=escamas, roma=.8), pata_delante()[0], pata_atras()[0]]


F.encuadrar(todo, (6, 51, 114, 82))
SUELO = float(F.P(.33, -float(F.abajo(.33)))[1])


def dientes():
    """de arriba bajan, de abajo suben, trabados a lo largo de la boca; el cuarto de abajo, más grande, adelante"""
    out = []
    for j, s in enumerate(np.arange(.012, .132, .0105)):
        largo = .0075 if j % 2 else -.0075
        out.append(F.pieza([(s - .0028, -.003), (s - .001, -.003 + largo), (s + .0028, -.003)], 0))
    out.append(F.pieza([(0.028, -.004), (0.03, .011), (0.034, -.004)], 0))
    return out


def dibujar(l):
    for parte, lejos in ((pata_delante, True), (pata_atras, True)):
        m, ds, puntas = parte(lejos)
        l.masa([m] + ds, material='lejos', alto=.5, brillo=.05, vientre=0, linea=.6, hondo=0)
    cuerpo = l.masa([F.cuerpo(joroba=escamas, roma=.8)] + muslos(), brillo=.18, vientre=.7, linea=.75,
                    bultos=[(ovalo(*F.P(.13, .026), 1.8, 1.4), .6), (ovalo(*F.P(.015, .012), 1.2, 1.0), .4),
                            (ovalo(*F.P(.418, -.014), 3.4, 3), .3), (ovalo(*F.P(.232, -.016), 2.4, 2.2), .25)])
    # escamas rectangulares del costado y de la cola, en filas
    for y0 in (.012, -.008, -.026):
        l.trazo(F.linea([(s, y0 * (1 - max(0, s - .45) * 1.4)) for s in np.linspace(.18, .9, 30)]), .18, alfa=.22, dentro=cuerpo, difuso=.04)
    for s in np.arange(.19, .92, .018):
        y1 = float(F.arriba(s)) - .004
        y0 = -float(F.abajo(s)) + .006
        l.trazo(F.linea([(s, y1), (s + .002, (y1 + y0) / 2), (s, y0)]), .14, alfa=.14, dentro=cuerpo, difuso=.03)
    for dnt in dientes():
        l.masa(dnt, material='claro', alto=.15, brillo=0, vientre=0, linea=.14, arroja=False, hondo=0)
    l.mancha(ovalo(*F.P(.01, .013), .35, .22), '0C3A33', .8)          # la nariz
    for m, ds, puntas, (x, y) in bajos():
        l.masa([m] + ds, alto=.5, brillo=.1, vientre=0, linea=.65, hondo=0, raices=[(x, y, .6, 2.6)])
        for p, g in puntas[:3]:
            l.masa(garra(p, g, .7, .28), material='oscuro', alto=.1, brillo=0, vientre=0, linea=0, tinta=False, arroja=False, hondo=0)


CARA = dict(ojo=F.p(.128, .029), k=1.3, boca=F.p(.072, -.003), kb=6.2, giro=round(-F.grados(.07)), pb=.3, wb=.7)
CARA['marco'] = [round(CARA['ojo'][0] - 16, 1), round(CARA['ojo'][1] - 14, 1), 30, 30]
_cola = F.P(1.0, 0)
FONDO = ('<ellipse class="sombra" cx="66" cy="%.1f" rx="46" ry="4.5" style="opacity:.28"/>' % (SUELO + 1)
         + '<path d="M2 %.1fq4.5-2.4 9 0t9 0t9 0t9 0M8 %.1fq4.5-2.2 9 0t9 0t9 0"' % (_cola[1] + 1.5, _cola[1] + 5) + AGUA + '/>')
LISTO = True
