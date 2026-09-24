# -*- coding: utf-8 -*-
"""Gavi, el gavial (Gavialis gangeticus), de memoria: el hocico más fino de los cocodrilos, larguísimo y derecho, que se ensancha
de golpe en la cabeza, con muchos dientes finos trabados a la vista; el macho adulto lleva en la punta la ghara, un bulto redondo
alrededor de la nariz; ojos arriba de la cabeza; cuerpo más delgado que el de un cocodrilo y patas débiles; la cola con cresta en
sierra. Echado en la orilla arenosa.
"""
import numpy as np

from _patas import dedos, garra, miembro
from _perfil import Perfil
from pintor import AGUA, ovalo

VISTA = (0, 54, 120, 36)
S = [0.000, 0.012, 0.025, 0.045, 0.080, 0.110, 0.130, 0.145, 0.160, 0.180, 0.200, 0.240, 0.290, 0.340, 0.390, 0.440, 0.490,
     0.560, 0.660, 0.760, 0.860, 0.950, 1.000]
ARRIBA = [0.013, 0.014, 0.0095, 0.0068, 0.0068, 0.0072, 0.0092, 0.016, 0.024, 0.026, 0.028, 0.036, 0.044, 0.048, 0.048, 0.045,
          0.039, 0.032, 0.025, 0.019, 0.013, 0.007, 0.003]
ABAJO = [0.009, 0.010, 0.0072, 0.0056, 0.0058, 0.0062, 0.0080, 0.012, 0.016, 0.020, 0.024, 0.030, 0.036, 0.039, 0.038, 0.034,
         0.028, 0.023, 0.018, 0.013, 0.009, 0.005, 0.003]
F = Perfil(S, ARRIBA, ABAJO, 104, giros=((0, 1), (.5, 0), (.8, -2), (1, -4)))


def escamas(s):
    s = np.asarray(s, float)
    lomo = np.where((s > .19) & (s < .52), .0024 * np.abs(np.sin((s - .19) * np.pi / .02)), 0)
    fase = np.clip((s - .52) / .026, 0, None) % 1
    sierra = np.where((s >= .52) & (s < .98), np.interp(s, [.52, .98], [.0055, .002]) * np.clip(1 - np.abs(fase - .5) * 2.2, 0, 1), 0)
    return lomo + sierra


def pata_delante(lejos=False):
    d = -.006 if lejos else 0
    brazo = miembro(F.linea([(0.205 + d, 0.002), (0.222 + d, -0.016), (0.244 + d, -0.028), (0.228 + d, -0.041)]), [1.8, 1.5, 1.1, .85])
    ds, puntas = dedos(F.P(0.223 + d, -0.044), 6, [1.2, 1.7, 1.9, 1.7, 1.1], abanico=55, grueso=(.45, .26), curva=6)
    return brazo, ds, puntas


def pata_atras(lejos=False):
    d = .03 if lejos else 0
    pierna = miembro(F.linea([(0.425 + d, 0.004), (0.402 + d, -0.014), (0.388 + d, -0.027), (0.436 + d, -0.04)]), [2.6, 2.1, 1.5, .95])
    ds, puntas = dedos(F.P(0.43 + d, -0.044), 3, [1.7, 2.3, 2.5, 2.1], abanico=40, grueso=(.5, .28), curva=5)
    return pierna, ds, puntas


def todo():
    return [F.cuerpo(joroba=escamas, roma=.9), pata_delante()[0], pata_atras()[0]]


F.encuadrar(todo, (6, 64, 114, 84))
SUELO = float(F.P(.34, -float(F.abajo(.34)))[1])


def dientes():
    """muchos, finos como agujas, trabados arriba y abajo a lo largo del hocico"""
    out = []
    for j, s in enumerate(np.arange(.03, .15, .0072)):
        largo = .0062 if j % 2 else -.0062
        out.append(F.pieza([(s - .0018, -.001), (s - .0012, -.001 + largo), (s + .0018, -.001)], 0))
    return out


def dibujar(l):
    for parte in (pata_delante, pata_atras):
        m, ds, puntas = parte(True)
        l.masa([m] + ds, material='lejos', alto=.5, brillo=.05, vientre=0, linea=.55, hondo=0)
    cuerpo = l.masa(F.cuerpo(joroba=escamas, roma=.9), brillo=.18, vientre=.7, linea=.7,
                    bultos=[(ovalo(*F.P(.155, .02), 1.5, 1.2), .6), (ovalo(*F.P(.008, .009), 1.3, 1.1), .6)])
    for y0 in (.01, -.008, -.022):
        l.trazo(F.linea([(s, y0 * (1 - max(0, s - .45) * 1.4)) for s in np.linspace(.19, .92, 30)]), .16, alfa=.2, dentro=cuerpo, difuso=.04)
    for s in np.arange(.2, .94, .017):
        y1 = float(F.arriba(s)) - .004
        y0 = -float(F.abajo(s)) + .005
        l.trazo(F.linea([(s, y1), (s + .002, (y1 + y0) / 2), (s, y0)]), .13, alfa=.13, dentro=cuerpo, difuso=.03)
    for dnt in dientes():
        l.masa(dnt, material='claro', alto=.12, brillo=0, vientre=0, linea=.12, arroja=False, hondo=0)
    l.mancha(ovalo(*F.P(.006, .016), .38, .24), '0C3A33', .8)          # la nariz, en la ghara
    for parte in (pata_atras, pata_delante):
        m, ds, puntas = parte()
        l.masa([m] + ds, alto=.5, brillo=.1, vientre=0, linea=.6, hondo=0,
               raices=[(*F.linea([(0.425 if parte is pata_atras else .205, .004)])[0], 1.4, 3.8)])
        for p, g in puntas[:3]:
            l.masa(garra(p, g, .6, .24), material='oscuro', alto=.1, brillo=0, vientre=0, linea=0, tinta=False, arroja=False, hondo=0)


CARA = dict(ojo=F.p(.155, .022), k=.95)
CARA['marco'] = [round(CARA['ojo'][0] - 11, 1), round(CARA['ojo'][1] - 12, 1), 24, 24]
FONDO = ('<ellipse class="sombra" cx="62" cy="%.1f" rx="52" ry="3.6" style="opacity:.28"/>' % (SUELO + 1)
         + '<path d="M4 87q4.5-2.2 9 0t9 0t9 0t9 0M84 87.4q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>')
LISTO = True
