# -*- coding: utf-8 -*-
"""La caja de Ulm (Ulmer Schachtel) del Danubio, de memoria: una barcaza plana de tablas de pino, como un cajón, de costados bajos y
puntas chatas que suben en rampa; una casita en cubierta, pintada a franjas blancas y negras, con techo a dos aguas; los remos largos
de gobierno en la proa y en la popa, apoyados en su horquilla; barriles y cajones de carga. Solo navega río abajo: al llegar se
desarma y se vende como leña, y el barquero vuelve a pie (NAVES.danubio).
"""
import numpy as np

from _barcas import agua, caja, fardo, olas_fondo, palo, poli

VISTA = (0, 43, 120, 39)
AGUA_Y = 72.0


def barril(l, x, y, r=2.2, h=4.6):
    b = l.masa(poli([(x - r, y), (x - r - .3, y - h / 2), (x - r, y - h), (x + r, y - h), (x + r + .3, y - h / 2), (x + r, y)], .4),
               material='acento', alto=.5, brillo=.2, vientre=0, hondo=0, linea=.35, arroja=False)
    for f in (.22, .78):
        l.trazo([(x - r - .2, y - h * f), (x + r + .2, y - h * f)], .3, color='0C3A33', alfa=.7, dentro=b)
    return b


def dibujar(l):
    # los remos de gobierno, con su horquilla, de proa y de popa
    for x0, x1, y1 in ((20, 2, 70.6), (98, 118, 70.2)):
        palo(l, (x0, 60.4), (x0, 55.4), .45, .4)
        palo(l, (x0 + (x1 - x0) * -.25, 54.8), (x1, y1), .5, .45)
        l.masa(poli([(x1 - 3 * np.sign(x1 - x0), y1 - 1.6), (x1, y1 - 1.8), (x1 + 1.2 * np.sign(x1 - x0), y1 + 2.2),
                     (x1 - 3.6 * np.sign(x1 - x0), y1 + 1.8)], .3), material='acento', alto=.3, brillo=.2, vientre=0, hondo=0,
               linea=.4)
    # la casita a franjas, con su techo a dos aguas y su puerta
    casa = l.masa(caja(42, 51.4, 72, 62, .2), material='claro', alto=.25, brillo=.1, vientre=0, hondo=0, linea=.5)
    for k, y in enumerate(np.arange(51.4, 62, 1.5)):                 # las franjas blancas y negras, a lo largo de la casa
        if k % 2:
            l.mancha(caja(42, y, 72, y + 1.5, 0), '0C3A33', .9, dentro=casa)
    l.mancha(caja(54.6, 55.2, 59.4, 62, .15), '164F46', 1, dentro=casa)
    l.mancha(caja(45, 53.4, 49, 56.6, .15), 'DAF5D8', .95, dentro=casa)
    l.mancha(caja(65, 53.4, 69, 56.6, .15), 'DAF5D8', .95, dentro=casa)
    l.masa(poli([(39.6, 52), (57, 46.4), (74.4, 52), (74.4, 53.4), (39.6, 53.4)], .25), material='lejos', alto=.3, brillo=.12,
           vientre=0, hondo=0, linea=.5)
    for x in (24, 29, 76.6, 88):                                    # la carga: barriles y cajones
        barril(l, x, 62)
    fardo(l, 81, 57.4, 5.6, 4.6, material='acento', ataduras=1)
    fardo(l, 33, 57.2, 6, 4.8, material='acento', ataduras=1)
    # el cajón: costados bajos de tablas, puntas chatas que suben en rampa
    c = l.masa(poli([(8.4, 58.4), (18, 62), (100, 62), (110.6, 58.2), (106.4, 67.4), (100, 70.4), (18, 70.4), (12, 67.6)], .4),
               material='acento', alto=.35, brillo=.25, vientre=0, hondo=0, contraluz=.2)
    for y in (64.6, 67.4):
        l.trazo([(14, y), (18, y + .4), (100, y + .4), (104, y)], [.08, .2, .2, .08], alfa=.35, dentro=c)
    for x in np.arange(22, 100, 6.4):
        l.trazo([(x, 62.4), (x, 70)], .1, alfa=.25, dentro=c)
    l.trazo([(18, 62.4), (18, 70)], [.2, .3], alfa=.4, dentro=c)
    l.trazo([(100, 62.4), (100, 70)], [.2, .3], alfa=.4, dentro=c)
    agua(l, AGUA_Y, sombra=poli([(12, 72), (106, 72), (102, 75.4), (16, 75.4)], .5))


FONDO = olas_fondo(AGUA_Y)
LISTO = True
