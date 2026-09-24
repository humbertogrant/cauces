# -*- coding: utf-8 -*-
"""Nerea, la delfín de Odiseo: un delfín listado (Stenella coeruleoalba), el más común del Mediterráneo, de memoria: esbelto, con
un pico corto y marcado, oscuro, aleta dorsal alta y curvada hacia atrás, aletas pectorales finas y la cola horizontal. Su marca:
el lomo oscuro como una capa; una franja oscura y nítida que va del ojo a lo largo del costado y baja hasta atrás, con una rama más
corta debajo; otra franja del ojo hacia la aleta; una llamarada clara que sube del costado hacia la aleta dorsal, y la panza blanca.
Salta fuera del agua, en arco.
"""
import numpy as np

from _perfil import Perfil
from pintor import AGUA, ovalo

VISTA = (0, 0, 120, 90)
S = [0.000, 0.010, 0.030, 0.060, 0.080, 0.100, 0.120, 0.150, 0.200, 0.260, 0.330, 0.420, 0.500, 0.580, 0.660, 0.740, 0.820,
     0.880, 0.930]
ARRIBA = [0.010, 0.012, 0.013, 0.016, 0.024, 0.040, 0.058, 0.072, 0.082, 0.090, 0.098, 0.104, 0.103, 0.095, 0.080, 0.062,
          0.046, 0.036, 0.032]
ABAJO = [0.010, 0.011, 0.012, 0.015, 0.019, 0.026, 0.034, 0.045, 0.060, 0.074, 0.086, 0.094, 0.090, 0.080, 0.064, 0.046,
         0.030, 0.020, 0.016]
F = Perfil(S, ARRIBA, ABAJO, 90, giros=((0, -44), (.5, 6), (1, 52)))


def a(s):
    return float(F.arriba(s))


def b(s):
    return float(F.abajo(s))


def dorsal():
    return F.pieza([(0.40, a(.40) - .01), (0.43, a(.43) + .03), (0.46, a(.46) + .07), (0.49, a(.49) + .1), (0.52, a(.52) + .118),
                    (0.545, a(.545) + .12), (0.54, a(.54) + .1), (0.535, a(.535) + .07), (0.545, a(.545) + .035),
                    (0.565, a(.565) + .008), (0.58, a(.58) - .01)], 2)


def aleta():
    return F.paleta((.22, -.06), -38, .12, [.012, .013, .014, .014, .012, .009, .005], [.010, .010, .012, .013, .012, .009, .005])


def todo():
    return [F.cuerpo(), dorsal(), F.cola_horizontal(.915, .12, .10, .035), aleta()[0]]


F.encuadrar(todo, (12, 8, 108, 70))


def dibujar(l):
    l.masa(dorsal(), alto=.35, brillo=.18, vientre=0, linea=.75)
    cuerpo = l.masa([F.cuerpo(), F.cola_horizontal(.915, .12, .10, .035)], brillo=.35, vientre=.9, contraluz=.3,
                    bultos=[(ovalo(*F.P(.13, .03), 4.5, 4), .15)])
    # la capa: el lomo más oscuro, del melón a la cola
    capa = F.pieza([(0.1, 0.05), (0.2, 0.065), (0.32, 0.066), (0.45, 0.07), (0.58, 0.058), (0.7, 0.03), (0.82, 0.012), (0.95, 0.01),
                    (0.95, 0.2), (0.1, 0.2)], 2)
    l.mancha(capa, '11443F', .5, dentro=cuerpo, difuso=.9)
    # la panza blanca, debajo de la franja
    l.mancha(F.pieza([(0.03, -0.012), (0.12, -0.016), (0.2, -0.018), (0.3, -0.032), (0.42, -0.046), (0.54, -0.056), (0.64, -0.058),
                      (0.72, -0.05), (0.78, -0.04), (0.78, -0.2), (0.03, -0.2)], 2), 'EAF9EC', .72, dentro=cuerpo, difuso=.25)
    # la llamarada clara que sube del costado hacia la aleta dorsal
    l.mancha(F.pieza([(0.28, -0.012), (0.34, 0.012), (0.42, 0.046), (0.5, 0.074), (0.53, 0.082), (0.47, 0.05), (0.4, 0.016),
                      (0.33, -0.018)], 2), 'D2F2DA', .7, dentro=cuerpo, difuso=.3)
    # la franja del ojo a lo largo del costado, que baja hasta atrás; su rama corta; la del ojo a la aleta
    l.trazo(F.linea([(0.108, 0.01), (0.18, -0.006), (0.28, -0.022), (0.4, -0.036), (0.52, -0.046), (0.62, -0.05), (0.7, -0.044),
                     (0.76, -0.034)]), [.4, .85, 1.0, .95, .85, .65, .4, .1], color='0C3A33', alfa=.85, dentro=cuerpo, difuso=.05)
    l.trazo(F.linea([(0.33, -0.032), (0.38, -0.05), (0.44, -0.068)]), [.4, .35, .08], color='0C3A33', alfa=.7, dentro=cuerpo,
            difuso=.05)
    l.trazo(F.linea([(0.115, 0.0), (0.16, -0.022), (0.212, -0.048)]), [.35, .5, .15], color='0C3A33', alfa=.75, dentro=cuerpo,
            difuso=.05)
    l.mancha(F.pieza([(0.0, -0.012), (0.03, -0.014), (0.07, -0.004), (0.085, 0.02), (0.06, 0.02), (0.02, 0.013), (0.0, 0.012)], 2),
             '11443F', .5, dentro=cuerpo, difuso=.3)                                              # el pico, oscuro
    ap, d, e = aleta()
    raiz = F.P(.22, -.06)
    l.masa(ap, alto=.4, brillo=.12, vientre=0, raices=[(raiz[0], raiz[1], 1.8, 4.2)], linea=.7)
    l.mancha(ovalo(*F.P(.16, a(.16) - .006), .8, .28, -F.grados(.16)), '0C3A33', .85)      # el espiráculo


_punta, _comisura = np.array(F.P(.004, -.002)), np.array(F.P(.1, -.01))
CARA = dict(ojo=F.p(.112, .014), k=1.2, boca=[round(float(v), 1) for v in (_punta + _comisura) / 2],
            kb=round(float(np.hypot(*(_punta - _comisura))) / 2.4, 1),
            giro=round(float(np.degrees(np.arctan2(_punta[1] - _comisura[1], _punta[0] - _comisura[0])))), pb=.3, wb=.7,
            inclina=round(F.grados(.1)))
CARA['marco'] = [round(CARA['ojo'][0] - 15, 1), round(CARA['ojo'][1] - 15, 1), 30, 30]
_pies = F.P(.95, 0)
FONDO = ('<path d="M4 80q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M20 85q4.5-2.2 9 0t9 0t9 0M76 85q4.5-2.2 9 0t9 0"' + AGUA + '/>'
         '<circle cx="%.1f" cy="%.1f" r="1"%s/><circle cx="%.1f" cy="%.1f" r=".7"%s/><circle cx="%.1f" cy="%.1f" r=".8"%s/>'
         % (_pies[0] - 3, 74, AGUA, _pies[0] + 2, 71, AGUA, _pies[0] - 6, 70.5, AGUA))
LISTO = True
