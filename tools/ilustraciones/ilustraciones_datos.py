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
    # --- lote del 2026-09-18
    # Boto, el delfín rosado (Inia geoffrensis). La clave es «inia» y no el glifo «delfin», que comparte con Bulán (delfín del Indo,
    # sin silueta libre) y con la delfín de Odiseo: mascotas.js le pone ilus:"inia" y los otros dos siguen con el glifo.
    'inia': dict(
        fuente='delfin-inia.svg', espejo=True, apoyo='centro', liso=0.5, vista=(0, 4, 120, 70),
        cara=dict(ojo=[92.6, 36.9], k=1.4, boca=[103.6, 37.8], kb=6.8, giro=-6, pb=0.25, wb=0.7, marco=[78, 18, 38, 38]),
        zonas={'lejos@.5': [[(56.5, 53.2), (60, 51.2), (65.5, 50.8), (66, 62), (56, 62)]]},                      # la aleta
        lineas='<ellipse class="oscuro" cx="87.8" cy="33.1" rx=".9" ry=".35"/>',                                 # el espiráculo
        fondo=('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M30 16.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
               '<circle cx="90" cy="25.5" r="1.1"' + AGUA + '/><circle cx="92.4" cy="21.2" r=".75"' + AGUA + '/>'),
    ),
    # Tami (caimán del Orinoco, Crocodylus intermedius) y Lalo (cocodrilo americano, C. acutus): la silueta es de C. acutus, la especie
    # exacta del Tempisque y un congénere del del Orinoco. Toma el sol en el banco de arena con la cola en el agua.
    'cocodrilo': dict(
        fuente='cocodrilo-reinke.svg', espejo=True, luz=0.5, vista=(0, 40, 120, 50),
        cara=dict(ojo=[95.4, 61.5], k=1.3, boca=[101.8, 65.2], kb=8, giro=-6, pb=0.3, wb=0.7, marco=[84, 45, 34, 34]),
        lineas='<circle class="oscuro" cx="110.2" cy="62.7" r=".5"/>',                                           # la nariz
        fondo=('<ellipse class="sombra" cx="72" cy="77.5" rx="43" ry="5.5" style="opacity:.28"/>'
               '<path d="M2 85.5q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0M16 88.8q4.5-2.2 9 0t9 0t9 0t9 0"' + AGUA + '/>'),
    ),
    # Tembo, el elefante africano de sabana (Loxodonta africana). La silueta no trae colmillo a la vista: no se inventa.
    'elefante': dict(
        fuente='elefante-traver.svg', espejo=True, liso=0.35,
        cara=dict(ojo=[90.5, 33], k=1.7, marco=[66, 8, 48, 48]),
        zonas={
            'lejos': [[(6, 66), (11, 62), (16, 60), (21, 60.5), (23.5, 63), (22, 83), (6, 83)],              # pata trasera lejana
                      [(61.5, 68.8), (70.2, 68.8), (70.6, 74.5), (68.8, 79.5), (61.5, 80)]],                 # pata delantera lejana
            'lejos@.5': [[(86, 20), (77, 21), (70.5, 27), (68.5, 35), (71.5, 43.5), (75.5, 47), (81.5, 42), (85, 34), (86.8, 27)]],   # la oreja
        },
        lineas=('<path class="bigote" d="M97.6 52q2 .9 4.2.4M98.4 58q2 .9 4.2.5M99.6 64q2 .9 4 .7M101.6 69.6q1.8 1 3.8 1"' + TENUE + '/>'
                '<path class="bigote" d="M72 82v-1.6M75 82.2v-1.6M78 82v-1.6M42.5 80.6v-1.6M45.5 80.8v-1.6M48.5 80.4v-1.6" style="stroke-width:.7;opacity:.75"/>'),
        fondo=('<ellipse class="sombra" cx="58" cy="81.5" rx="54" ry="6" style="opacity:.28"/>'
               '<path d="M2.5 85q.3-2.8-1-4.6M5 85.4q.2-3 1.4-4.6M29 86.6q.3-3-1-5M31.4 87q.2-3.2 1.4-5M116 84q-.3-3 1.2-5"' + AGUA + '/>'),
    ),
    # Valsa, el cisne vulgar (Cygnus olor): nada, así que el contorno termina en la línea del agua.
    'cisne': dict(
        fuente='cisne-wilson.svg', apoyo='centro', vista=(0, 8, 120, 82),
        cara=dict(ojo=[101.2, 24.4], k=1.4, marco=[82, 8, 36, 36]),
        zonas={
            'acento': [[(105.6, 25.4), (104.2, 29.8), (116, 37), (116, 24)]],                                   # el pico
            'oscuro': [[(102.8, 21), (108.8, 21), (108.9, 25.6), (105.6, 25.4), (104.2, 29.6), (102.6, 28.4)]],   # la protuberancia y el antifaz
        },
        lineas='<path class="bigote" d="M34 63.5Q54 73.5 80 65.5"' + TENUE + '/>',                              # el borde del ala plegada
        fondo=('<path d="M0 80.5q4.5-2.4 9 0t9 0M104 81q4.5-2.4 9 0t9 0M10 85q4.5-2.2 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0"' + AGUA + '/>'),
    ),
    # Lobi (lobito de río) y Nuria (nutria de río): las dos son la nutria neotropical, Lontra longicaudis, la especie de la silueta.
    'nutria': dict(
        fuente='nutria-michaud.svg', vista=(0, 30, 120, 60),
        cara=dict(ojo=[105, 59.5], k=1.5, boca=[107.8, 66.2], kb=2.6, giro=-13, pb=0.8, wb=0.7, marco=[82, 40, 36, 36]),
        lineas=('<ellipse class="oscuro" cx="110.2" cy="62.3" rx="1.1" ry=".9"/>'
                '<path class="bigote" d="M108.6 63.6l5.4-1.4M108.8 64.5l5.6.5M108.6 65.3l4.8 2.2" style="stroke-width:.45;opacity:.7"/>'
                '<path class="bigote" d="M98 57.8q1-1.9 2.5-.6"' + TENUE + '/>'),
        fondo=('<ellipse class="sombra" cx="68" cy="81.5" rx="46" ry="5" style="opacity:.28"/>'
               '<path d="M4 86.5q4.5-2.4 9 0t9 0t9 0M3.5 84q.3-2.8-1-4.6M6 84.4q.2-3 1.4-4.6"' + AGUA + '/>'),
    ),
    # --- lote 3 del 2026-09-18
    # Bíber, el castor del Rin (Castor fiber). La silueta es de su congénere americano (C. canadensis), casi idéntico por fuera, porque
    # la única libre de C. fiber muestra la cola de canto y no se lee. Los incisivos anaranjados son el detalle dorado.
    'castor': dict(
        fuente='castor-canadensis.svg',
        cara=dict(ojo=[103.4, 40.6], k=1.5, boca=[107.6, 47], kb=2, giro=8, pb=0.7, wb=0.7, marco=[84, 22, 36, 36]),
        zonas={'lejos': [[(0, 68), (33, 68), (36.2, 72), (35.4, 75.5), (33, 78.6), (30, 86), (0, 86)]]},         # la cola
        tramas=[dict(pol=[(0, 68), (32.5, 68), (35.4, 72), (34.8, 75.5), (32.4, 78.6), (29.5, 86), (0, 86)], paso=2.4, angulos=(28, -38))],
        lineas=('<path class="acento" d="M107.3 47.2h1.7v1.9h-1.7Z" style="stroke-width:.35"/>'                         # el incisivo anaranjado, bajo el labio
                '<ellipse class="oscuro" cx="110.7" cy="41.9" rx="1" ry=".8"/>'
                '<path class="bigote" d="M108 44.2l5.6-.8M108.2 45l5.6.8" style="stroke-width:.45;opacity:.7"/>'
                '<path class="bigote" d="M94.6 36.4q1-1.8 2.4-.4"' + TENUE + '/>'
                '<path class="bigote" d="M58 34q3-1.6 6-1.6M70 31q3-.6 6 .2M82 35q3 .6 5.6 2M52 44q2.6-2 5.6-2.4M64 42q3-.8 6-.2M78 44q3 .4 5.6 1.6M50 56q2.4-1.6 5.2-2M62 54q3-.6 6 0"' + TENUE + '/>'),
        fondo=('<ellipse class="sombra" cx="66" cy="80.5" rx="50" ry="5.5" style="opacity:.28"/>'
               '<path d="M2 86.5q4.5-2.4 9 0t9 0t9 0t9 0M114 84q.3-3-1-5M116.4 84.4q.2-3.2 1.4-5"' + AGUA + '/>'),
    ),
    # Tun, la marsopa sin aleta del Yangtsé (Neophocaena asiaeorientalis): sin aleta en el lomo y con su «sonrisa».
    'marsopa': dict(
        fuente='marsopa-neophocaena.svg', apoyo='centro', luz=0.7, vista=(0, 12, 120, 64),
        cara=dict(ojo=[104.5, 37.2], k=1.3, boca=[108.4, 39.9], kb=2.6, giro=-4, pb=0.6, wb=0.7, marco=[84, 18, 36, 36]),
        zonas={'lejos@.5': [[(85.5, 50.5), (90, 47), (96.5, 45.8), (97.5, 57), (84.5, 57)]]},                    # la aleta
        lineas='<ellipse class="oscuro" cx="100.4" cy="33.5" rx=".9" ry=".35"/>',
        fondo=('<path d="M4 18q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M40 22.5q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'
               '<circle cx="103" cy="27" r="1.1"' + AGUA + '/><circle cx="105.2" cy="23" r=".75"' + AGUA + '/>'),
    ),
    # Gavi, el gavial (Gavialis gangeticus): hocico finísimo con la «ghara» en la punta (viene en el contorno). Toma el sol en un banco de arena.
    'gavial': dict(
        fuente='gavial-jfd.svg', espejo=True, luz=0.3, borde=0.7, vista=(0, 54, 120, 36),
        cara=dict(ojo=[97.2, 69.4], k=0.9, marco=[92, 58, 24, 24]),
        fondo=('<ellipse class="sombra" cx="62" cy="82" rx="52" ry="3.6" style="opacity:.28"/>'
               '<path d="M4 87q4.5-2.2 9 0t9 0t9 0t9 0M84 87.4q4.5-2.2 9 0t9 0t9 0"' + AGUA + '/>'),
    ),
    # Belu, el esturión beluga (Huso huso): placas de hueso en filas, aleta del lomo muy atrás y cola de tiburón.
    'esturion': dict(
        fuente='esturion-cada.svg', espejo=True, apoyo='centro', luz=0.6, vista=(0, 26, 120, 44),
        cara=dict(ojo=[101.5, 46.8], k=1.1, marco=[84, 30, 34, 34]),
        lineas=('<path class="bigote" d="M48 47.6Q75 45.4 98 46.6" style="stroke-width:.9;stroke-dasharray:1.1 2.3;opacity:.5"/>'
                '<path class="bigote" d="M96.6 43.8q-2 3.6-.4 7.6M103.9 52.2l.4 2.2M102.4 52l.2 2"' + TENUE + '/>'),
        fondo=('<path class="sombra" d="M0 64Q30 61 60 63.5T120 62V70H0Z" style="opacity:.22"/>'
               '<ellipse class="sombra" cx="26" cy="66" rx="4" ry="1.4" style="opacity:.3"/><ellipse class="sombra" cx="88" cy="66.4" rx="5" ry="1.6" style="opacity:.3"/>'),
    ),
    # Mana, el manatí africano (Trichechus senegalensis): flota con la cola de paleta hacia abajo, junto a las plantas que come.
    'manati': dict(
        fuente='manati-traver.svg', espejo=True, apoyo='centro',
        cara=dict(ojo=[103, 29], k=1.2, boca=[107.6, 39.4], kb=2, giro=15, pb=0.6, wb=0.7, marco=[80, 8, 38, 38]),
        zonas={'lejos': [[(55, 53.5), (61, 52), (70.5, 50), (71, 72), (54, 72)]]},                               # la aleta lejana
        lineas=('<path class="bigote" d="M94 20q-2.6 8 .4 17M89.5 19q-2.4 8 .2 16"' + TENUE + '/>'
                '<circle class="oscuro" cx="108.6" cy="35.2" r=".4"/><circle class="oscuro" cx="110" cy="36.6" r=".4"/><circle class="oscuro" cx="108.4" cy="37.4" r=".4"/>'),
        fondo=('<path d="M4 6q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0"' + AGUA + '/>'
               '<path d="M100 89q-2-12 2-22M104.5 89q1-10-1.5-17M109 89q-1-13 3-25M113.5 89q1.5-9 0-15" style="fill:none;stroke:var(--verde-medio);stroke-width:1.6;stroke-linecap:round;opacity:.5"/>'),
    ),
    # Lola, la bonobo (Pan paniscus): camina sobre los nudillos y mira al suelo; el retrato gira para enderezarle la cara.
    'bonobo': dict(
        fuente='bonobo-keesey.svg', espejo=True, liso=0.2, brillo=0.3,      # brillo solo en el lomo, no en brazos ni piernas
        cara=dict(ojo=[89.3, 28.4], k=1.3, boca=[83.6, 36.9], kb=1.8, giro=55, pb=0.8, wb=0.7, marco=[68, 8, 40, 40], inclina=-50),
        zonas={'lejos': [[(45.5, 38), (53.5, 37), (58, 50), (61, 62), (62.5, 68), (60.5, 72.5), (52, 72.5), (47, 60)]],   # la pierna lejana
               'lejos@.55~': [[(89.5, 20.5), (86.8, 23.5), (85.4, 27), (85.2, 30.2), (83, 32.2), (81, 34.5), (80.2, 38), (84, 41), (90, 38), (94, 32), (94.5, 24), (92, 20)]]},   # la cara sin pelo
        lineas='<path class="bigote" d="M83.2 26.6q-1.6-2.2.4-3.8q1.8.8 1.4 3.4"' + TENUE + '/>',                  # la oreja
        fondo=('<ellipse class="sombra" cx="58" cy="81.5" rx="44" ry="5.5" style="opacity:.28"/>'
               '<path d="M6 85q.3-2.8-1-4.6M8.5 85.4q.2-3 1.4-4.6M108 86q-.3-3 1.2-5M110.4 86.4q0-2.8 1.6-4.4"' + AGUA + '/>'),
    ),
    # Bela, la beluga (Delphinapterus leucas): blanca de verdad (todo el cuerpo en `claro`), sin aleta en el lomo y con la frente abombada.
    'beluga': dict(
        fuente='beluga-traver.svg', espejo=True, apoyo='centro', vista=(0, 6, 120, 78),
        cara=dict(ojo=[103.8, 35.8], k=1.3, boca=[108.2, 38.7], kb=2.8, giro=0, pb=0.6, wb=0.7, marco=[80, 14, 38, 38]),
        zonas={'claro': [[(0, 0), (120, 0), (120, 90), (0, 90)]],
               'lejos@.45': [[(75, 45), (82.5, 44.5), (82.5, 51), (75, 51)]]},                                   # la aleta lejana
        lineas='<ellipse class="oscuro" cx="101" cy="28.8" rx=".9" ry=".35"/>',
        fondo=('<path d="M4 12q4.5-2.4 9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0t9 0M14 16.5q4.5-2.2 9 0t9 0"' + AGUA + '/>'
               '<circle cx="106" cy="22" r="1.1"' + AGUA + '/><circle cx="108.4" cy="17.6" r=".75"' + AGUA + '/>'),
    ),
}
