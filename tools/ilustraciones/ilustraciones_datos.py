# -*- coding: utf-8 -*-
"""Lo que tools/ilustraciones.py necesita saber de cada animal y no está en el contorno. Coordenadas en la caja 0 0 120 90,
leídas sobre la cuadrícula (python tools/ilustraciones.py --crudo y la hoja con --grid).

Por animal: `fuente` (archivo de tools/ilustraciones/, ver fuentes.json), `espejo` (si la silueta mira a la izquierda), `giro`
(grados, para nivelar las patas), `apoyo` ('suelo' o 'centro'), `cara` (lo que recibe caraDe en motor.js: ojo, k, boca, kb, giro,
marco), `zonas` (clase → polígonos toscos que el contorno recorta: `lejos` para patas y partes lejanas, `acento` para el único
detalle dorado), `lineas` (detalles a mano, encima) y `fondo` (el indicio del lugar donde vive, detrás)."""

TENUE = ' style="stroke-width:.7;opacity:.5"'
AGUA = ' style="fill:none;stroke:var(--verde-medio);stroke-width:1;opacity:.55"'

# el picabueyes (dorado) posado en el lomo del hipopótamo; patas en y = 21.4 antes de moverlo
PICABUEYES = ('<g transform="translate(-7 3.7)"><path class="acento" d="M45.5 17.5l-3.5-2.4l1.2 3.2Z"/><ellipse class="acento" cx="50" cy="17.2" rx="4.4" ry="2.7"/>'
              '<circle class="acento" cx="54.6" cy="14.8" r="2"/><path class="oscuro" d="M56.4 14.8l2.8.7l-2.8.9Z"/><circle class="oscuro" cx="55" cy="14.3" r=".45"/>'
              '<path class="bigote" d="M48.6 19.8v1.6M51.4 19.8v1.6" style="stroke-width:.8"/></g>')

ANIMALES = {
    'hipo': dict(
        fuente='hipo-traver.svg', espejo=True, giro=-5,
        cara=dict(ojo=[105.4, 54.5], k=2.2, boca=[99.2, 72.6], kb=7.6, giro=61, marco=[76, 38, 50, 50], inclina=-40),
        zonas={'lejos': [
            [(8, 61), (12, 58.5), (17, 58), (20.2, 60.5), (21.2, 63.5), (23, 81), (8, 81)],          # pata trasera lejana
            [(59, 65), (66.5, 65.5), (67.4, 72.6), (66, 75), (68.5, 81), (59, 81)],                   # pata delantera lejana
        ]},
        lineas=('<path class="bigote" d="M92.5 47.5q-3.6 6.2-2 13.5M87.6 46q-3 5.4-2.2 11M71.2 50.5q-2.6 8 .6 14.5M37 68q-3.5-7-2.5-15"' + TENUE + '/>'
                '<ellipse class="oscuro" cx="109.7" cy="75.3" rx="1.1" ry=".55" transform="rotate(68 109.7 75.3)"/>'
                '<path class="bigote" d="M74 81v-1.7M77 81.2v-1.7M80 81v-1.7M41.2 77.4l.4-1.6M43.2 76.6l.3-1.5" style="stroke-width:.7;opacity:.75"/>'
                + PICABUEYES),
        fondo=('<ellipse class="sombra" cx="60" cy="81" rx="56" ry="6.5" style="opacity:.28"/>'
               '<path d="M93.5 85q.4-3.2-1.2-5.4M96 85.4q.2-3.6 1.4-5.6M115 84.6q-.3-3.2 1.3-5.2M117.4 85q0-2.8 1.7-4.2M4.5 84q.3-2.8-1-4.6M7 84.4q.2-3 1.4-4.6"' + AGUA + '/>'),
    ),
    'ornitorrinco': dict(
        fuente='ornitorrinco-michaud.svg', espejo=True, apoyo='centro',
        cara=dict(ojo=[89.2, 29.4], k=1.8, marco=[75, 11, 38, 38]),
        zonas={
            'acento': [[(91.2, 24.2), (93, 28), (95.2, 31.4), (97.8, 34.6), (100.6, 37.4), (118, 38), (118, 10), (91.2, 10)]],   # el pico
            'lejos': [[(0, 28), (31.2, 28), (31.2, 39.6), (33, 46), (31.6, 52), (30.2, 56.5), (0, 60)]],                       # la cola
        },
        lineas=('<circle class="oscuro" cx="106.8" cy="23.2" r=".55"/><circle class="oscuro" cx="108.8" cy="25" r=".55"/>'
                '<path class="bigote" d="M40 41q2.5-1.3 5-.9M50 38.5q2.5-1.3 5-.9M60 37q2.5-1.3 5-.9M70 35q2.5-1.3 5-.9M79 32.5q2.5-1.3 5-.9'
                'M46 46q2.5-1.3 5-.9M57 44q2.5-1.3 5-.9M68 42q2.5-1.3 5-.9M78 39.5q2.5-1.3 5-.9"' + TENUE + '/>'
                '<path class="bigote" d="M87.5 57.2L96.5 59.6M87.8 58.4L97.2 62.2M88.5 59.8L95.5 63.6"' + TENUE + '/>'),
        fondo=('<path d="M4 8q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M22 12.5q4.5-2.2 9 0t9 0t9 0M76 12.5q4.5-2.2 9 0t9 0"' + AGUA + '/>'
               '<circle cx="115" cy="19" r="1.2"' + AGUA + '/><circle cx="113.2" cy="15.2" r=".8"' + AGUA + '/>'
               '<path class="sombra" d="M0 84Q30 79 60 83T120 81V90H0Z" style="opacity:.22"/>'
               '<ellipse class="sombra" cx="24" cy="85.6" rx="4" ry="1.6" style="opacity:.3"/><ellipse class="sombra" cx="92" cy="86" rx="5" ry="1.8" style="opacity:.3"/>'),
    ),
}
