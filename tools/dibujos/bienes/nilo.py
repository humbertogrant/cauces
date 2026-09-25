# -*- coding: utf-8 -*-
"""Las mercancías del Nilo (MERCADOS.nilo, en su orden), de memoria, cada una como un bodegón chico en una caja de 40 × 40:

- café, de Jinja (Uganda, uno de los grandes productores de café de África): un saco de yute abierto, lleno de granos tostados, cada
  uno con su surco al medio, y unos granos sueltos delante;
- pescado seco, de Juba: dos pescados abiertos y secados al sol, planos y tiesos, colgados por la boca de un cordel;
- goma arábiga, de Jartum (Sudán es el que más produce): las «lágrimas» de resina que la acacia suelta por la corteza, trozos duros,
  irregulares y translúcidos como vidrio, color ámbar, amontonados en un cuenco de barro;
- dátiles, de Asuán: un racimo colgando de su tallo anaranjado, con las ramitas que se abren y caen, y los dátiles apretados, lisos
  y brillantes;
- trigo, de Luxor: una gavilla de espigas atada con un cordel, abierta en abanico arriba y abajo, con sus barbas largas.

El dorado va en lo que es dorado de verdad: la goma, el trigo y el tallo de los dátiles.
"""
import math

import numpy as np

from pintor import curva, forma, ovalo, tubo

VISTA = (0, 0, 40, 40)


def grano_cafe(l, x, y, ang, r=1.7):
    """un grano de café tostado: un óvalo oscuro y brillante con el surco en ese al medio"""
    g = l.masa(ovalo(x, y, r, r * .72, ang), material='oscuro', alto=.5, brillo=.45, vientre=0, hondo=0, linea=.35, contraluz=.2,
               arroja=False)
    a = math.radians(ang)
    d, e = np.array([math.cos(a), math.sin(a)]), np.array([-math.sin(a), math.cos(a)])
    p = np.array([x, y])
    l.trazo([p - d * r * .8, p - d * r * .3 + e * .18, p + d * r * .3 - e * .18, p + d * r * .8], [.05, .2, .2, .05], color='05201C',
            alfa=.9, dentro=g)
    return g


def cafe(l):
    rng = np.random.default_rng(3)
    saco = forma([(9.6, 36), (7.6, 30), (8, 22), (9.6, 16.6), (8.2, 13.4), (11.4, 12.2), (15.6, 13.6), (20, 12.4), (24.4, 13.8),
                  (28.8, 12.4), (31.6, 13.8), (30.2, 17), (32, 23), (32.4, 30), (30.4, 36), (20, 37.2)], 2)
    s = l.masa(saco, material='vientre', alto=.8, brillo=.08, vientre=0, contraluz=.2, linea=.9,
               bultos=[(ovalo(20, 29, 10, 7), .3)])
    for k in range(9):                                               # la trama del yute
        y = 17 + k * 2.2
        l.trazo([(9, y), (20, y + .5), (31.4, y)], .1, color='3D9582', alfa=.35, dentro=s)
    for k in range(10):
        x = 10 + k * 2.3
        l.trazo([(x, 16), (x + .2, 36)], .1, color='3D9582', alfa=.3, dentro=s)
    boca = forma([(10.2, 15.6), (14, 13.6), (20, 14.4), (26, 13.4), (30, 15.4), (26.4, 18.4), (20, 19), (13.6, 18.4)], 2)
    l.masa(boca, material='lejos', alto=.2, brillo=0, vientre=0, hondo=0, linea=.5, arroja=False)
    for k in range(20):                                             # los granos que asoman por la boca
        x, y = rng.uniform(12, 28.4), rng.uniform(13.6, 17.6)
        grano_cafe(l, x, y, rng.uniform(0, 180), r=1.35)
    for x, y, a in ((7.4, 37.4, 20), (33.6, 36.4, -30), (30.2, 38.6, 70)):
        grano_cafe(l, x, y, a, r=1.6)


def pescado_seco(l):
    """dos pescados abiertos y secos, tiesos, colgados por la boca de un cordel"""
    for dx, dy, ang in ((-4.6, 1.4, 84), (4.6, -.4, 96)):
        c = np.array([20 + dx, 22 + dy])
        a = math.radians(ang)
        d, e = np.array([math.cos(a), math.sin(a)]), np.array([-math.sin(a), math.cos(a)])

        def P(u, v):
            return tuple(c + d * u + e * v)
        cuerpo = forma([P(-12.6, 0), P(-10.8, -3.4), P(-5, -4.8), P(3, -4.6), P(9.4, -3), P(12.2, -.8), P(12.2, 1), P(9.4, 3.2),
                        P(3, 4.8), P(-5, 5), P(-10.8, 3.4)], 2)
        cola = forma([P(11, 0), P(15.4, -4.2), P(16.6, -3.6), P(14.6, 0), P(16.6, 3.6), P(15.4, 4.2)], 1)
        m = l.masa([cuerpo, cola], material='lejos', alto=.18, brillo=.2, vientre=0, hondo=0, contraluz=.2, escalon=.12)
        l.mancha(forma([P(-9.6, -1.6), P(-4, -2.8), P(4, -2.6), P(9, -1.4), P(9, 1.4), P(4, 2.6), P(-4, 2.8), P(-9.6, 1.6)], 2),
                 'A9E0CB', .55, dentro=m, difuso=.3)                # la carne abierta, clara
        for u in np.arange(-7.4, 8.6, 1.6):                         # las espinas y las arrugas del secado
            l.trazo([P(u, -2.4), P(u + .6, 0), P(u, 2.4)], [.05, .12, .05], color='164F46', alfa=.55, dentro=m)
        l.trazo([P(-8.8, -3.4), P(-9.8, 0), P(-8.8, 3.4)], [.1, .26, .1], alfa=.55, dentro=m)          # el borde de la agalla
        l.mancha(ovalo(*P(-10.6, -1.4), .5, .5), '05201C', .85, dentro=m)                            # el ojo seco
    # el cordel que pasa por las bocas y sube a un lazo
    cordel = [tubo([(15.8, 10.8), (17.2, 6.6), (20, 5), (22.8, 6.4), (24, 10.2)], [.35, .35, .35, .35, .35]),
              tubo([(14.4, 11.6), (20, 9.4), (25.6, 11.2)], [.35, .32, .35])]
    l.masa(cordel, material='claro', alto=.3, brillo=.1, vientre=0, hondo=0, linea=.3)


def goma(l):
    """las lágrimas de goma arábiga: trozos irregulares, duros y translúcidos, amontonados en un cuenco de barro"""
    # la boca del cuenco, por dentro (los trozos de abajo se hunden en ella; el cuenco se pinta después, delante)
    l.masa(ovalo(20, 25.6, 15.4, 2.6), material='oscuro', alto=.2, brillo=0, vientre=0, hondo=0, linea=.6, arroja=False)
    rng = np.random.default_rng(8)

    def trozo(x, y, r):
        pts = []
        for k in range(7):
            a = 2 * math.pi * k / 7 + rng.uniform(-.25, .25)
            rr = r * rng.uniform(.62, 1.15)
            pts.append((x + rr * math.cos(a) * 1.1, y + rr * math.sin(a) * .9))
        return forma(pts, 2)

    def lagrima(t, x, y, r):
        g = l.masa(t, material='acento', alto=.55, brillo=.7, vientre=0, hondo=0, linea=.35, contraluz=.4, escalon=.1)
        l.mancha(ovalo(x - r * .35, y - r * .4, r * .38, r * .2, -25), 'FFFFFF', .85, dentro=g, difuso=.06)   # el brillo del vidrio
        l.mancha(ovalo(x + r * .25, y + r * .35, r * .55, r * .35, 10), 'FBEFCB', .45, dentro=g, difuso=.25)  # la luz que pasa
    pila = []                                                     # un montón apretado: los trozos se tocan y se tapan
    for fila, y in enumerate(np.arange(26, 12, -2.7)):
        ancho = 13.6 * math.sqrt(max(0, 1 - ((26 - y) / 14.6) ** 2))
        for x in np.arange(20 - ancho + (fila % 2) * 1.6, 20 + ancho + .1, 3.3):
            pila.append((x + rng.uniform(-.5, .5), y + rng.uniform(-.5, .5), rng.uniform(1.8, 2.5)))
    for x, y, r in sorted(pila, key=lambda t: t[1]):
        lagrima(trozo(x, y, r), x, y, r)
    cuenco = forma([(4.4, 26), (10, 27.6), (20, 28.2), (30, 27.6), (35.6, 26), (34, 30.8), (29.4, 34.6), (20, 36.4), (10.6, 34.6),
                    (6, 30.8)], 2)
    c = l.masa(cuenco, material='lejos', alto=.6, brillo=.12, vientre=0, contraluz=.2, linea=.85)
    l.trazo([(6.6, 30.4), (20, 31.8), (33.4, 30.4)], [.1, .22, .1], color='A4DCC4', alfa=.5, dentro=c)
    for x, y, r in ((36.2, 34.4, 1.6), (4.6, 36.6, 1.4), (33, 37.8, 1.1)):                       # unas sueltas, sobre la mesa
        lagrima(trozo(x, y, r), x, y, r)


def datiles(l):
    """un racimo de dátiles colgando: el tallo grueso y anaranjado, las ramitas que se abren y caen, y los dátiles apretados en
    ellas, lisos y brillantes"""
    tallo = tubo([(19, 1.6), (19.8, 6), (20.2, 9.6)], [1.3, 1.1, 1])
    ejes = []
    for k in range(7):
        f = k / 6 - .5
        ejes.append([(20.2, 9.4), (20.2 + f * 16, 12.4 + abs(f) * 2), (20.2 + f * 22, 22 + abs(f) * 4),
                     (20.2 + f * 22.6, 34 - abs(f) * 6)])
    l.masa([tallo] + [tubo(e, [.4, .34, .3, .26]) for e in ejes], material='acento', alto=.3, brillo=.15, vientre=0, hondo=0,
           linea=.35)
    rng = np.random.default_rng(5)
    puestos = []
    for e in ejes:
        c = curva(e, 10)
        largo = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(c, axis=0).T))])
        for t in np.arange(4.2, largo[-1], 2.3):
            x, y = c[min(int(np.searchsorted(largo, t)), len(c) - 1)]
            puestos.append((x + rng.uniform(-.8, .8), y + rng.uniform(-.2, .4), rng.uniform(-18, 18)))
    for x, y, a in sorted(puestos, key=lambda t: t[1]):
        d = l.masa(ovalo(x, y + 1.5, 1.45, 2.35, a), material='oscuro', alto=.7, brillo=.55, vientre=0, hondo=0, linea=.35,
                   contraluz=.3)
        l.mancha(ovalo(x - .45, y + .8, .3, .85, a), '9DB9B0', .7, dentro=d, difuso=.12)       # el brillo de la piel
        l.mancha(ovalo(x, y - .7, .6, .3, a), '93701A', .9, dentro=d)                           # el cáliz, chiquito


def trigo(l):
    """una gavilla: las espigas se abren en abanico arriba, los tallos se cruzan en el atado y se abren otra vez abajo"""
    n = 9
    tallos = []
    for k in range(n):
        f = k / (n - 1) - .5
        tallos.append(tubo([(20 - f * 10, 38.6), (20 + f * 1.4, 27.6), (20 + f * 15, 13.4)], [.34, .3, .28]))
    l.masa(tallos, material='acento', alto=.25, brillo=.2, vientre=0, hondo=0, linea=.3)
    for k in range(n):
        f = k / (n - 1) - .5
        base = np.array([20 + f * 15, 13.4])
        ang = -90 + f * 62
        a = math.radians(ang)
        d, e = np.array([math.cos(a), math.sin(a)]), np.array([-math.sin(a), math.cos(a)])
        granos = []
        for j in range(6):
            c = base + d * (j * 1.15 + .4)
            for s_ in (-1, 1):
                granos.append(ovalo(*(c + e * s_ * .5), .62, 1.05, ang + 90 + s_ * 28))
        granos.append(ovalo(*(base + d * 7.4), .5, .8, ang + 90))
        l.masa(granos, material='acento', alto=.6, brillo=.35, vientre=0, hondo=0, linea=.28, contraluz=.25)
        for j in range(5):                                            # las barbas largas
            lado = 1 if j % 2 else -1
            p0 = base + d * (1.2 + j * 1.3) + e * lado * .7
            l.trazo([tuple(p0), tuple(p0 + d * 6 + e * lado * 1.2)], [.1, .03], color='6B4E10', alfa=.6)
    l.masa(tubo([(16, 28.4), (20, 29.2), (24, 28.4)], [.75, .75, .75]), material='lejos', alto=.4, brillo=.15, vientre=0, hondo=0,
           linea=.4)                                                  # el cordel del atado


BIENES = [dict(clave='café', vista=VISTA, dibujar=cafe), dict(clave='pescado seco', vista=VISTA, dibujar=pescado_seco),
          dict(clave='goma arábiga', vista=VISTA, dibujar=goma), dict(clave='dátiles', vista=VISTA, dibujar=datiles),
          dict(clave='trigo', vista=VISTA, dibujar=trigo)]
LISTO = True
