# Hallazgos de Verificación: vitrina del Nilo

Verificación mide, captura, mira y anota; no corrige código de otros. Todo a 390 × 844 (escala 2, móvil) con Edge sin pantalla,
salvo que se diga otra cosa. Las capturas salen de `node tools/captura.js` (ver el encabezado de `tools/captura.js`).

## Antes (`dist/cauces.html`, modo Niño / mercader, 2026-11-11)

Recorrido completo con clics de verdad: 20 capturas en `docs/vitrina/capturas/antes/` (`01-portada.png` … `20-mar.png`, más
`recorrido.json` con cada paso, su botón y sus tiempos). Llegó al mar en 30,4 s, sin errores de consola. Los cuatro momentos:

1. **Inicio del río** · `docs/vitrina/capturas/antes/antes-1-inicio.png`: cabecera crema («‹ Ríos», Nilo, «≈ sonido»), el mapa
   ocupa un tercio con el río entero apagado, cinco rótulos de relieve y la barca en la fuente; debajo, el perfil de altura, el
   riel de cuatro pasos, el globo de Hipo, «Lago Victoria y lago Tana» y la ficha de la frase con la lista; al pie, «Zarpar ›».
2. **Navegando (la guía a la vista)** · `docs/vitrina/capturas/antes/antes-2-navegando.png` (Juba, parada 2): la misma pantalla
   de la parada hace de guía: «¿Cuál es la próxima parada?» y tres fichas en el pie, que tapa la postal; el mapa no cambia de
   encuadre y la barca queda encima del nombre de Juba.
3. **Parada 4, Asuán** · `docs/vitrina/capturas/antes/antes-3-parada-4.png`: el tramo recorrido en dorado con cuatro nombres, la
   barca sobre el rótulo de Asuán, el globo con el sello, kicker, nombre, país y altura; de la postal solo asoma el borde de
   arriba, cortado por el pie con la guía.
4. **Llegada al mar** · `docs/vitrina/capturas/antes/antes-4-mar.png`: el río entero en dorado con los seis nombres, «Mar
   Mediterráneo», la postal de pictogramas (edición económica) y «Ordenar de memoria ›»; a los 3,2 s del clic la barrida de olas
   doradas todavía tapa la cabecera (la captura cae a media animación).

## Cómo se anota cada hallazgo

Un hallazgo por fila, numerado por vuelta (`V1-01`…). Gravedad: **grave** (impide jugar, rompe el contrato o se ve roto),
**media** (se nota y estorba), **menor** (pulido). «Captura» es la ruta dentro de `docs/vitrina/capturas/`. «Qué se ve» dice lo
que se ve o se midió, no la causa ni el arreglo; si hay un número (píxeles, ms, dBFS), va. «Visto por» dice quién lo miró.

## Vuelta 1 (2026-11-11)

### Medidas (`dist/nilo.html`, build de las 07:59, 640 KB)

- **Prueba**: `node test/vitrina.js` termina en `VITRINA OK` en los dos modos, dos bajadas por modo (la última corrida, sobre un
  build de 646 KB). Comprueba el arranque con solo el Nilo, el orden de los ganchos, `dibujado`, los momentos (incluido `evento`),
  las fichas del acróstico, los nombres de paradas futuras, el peso (< 900 KB) y que no haya emojis en `#panel`, `#pie` y `#cab`.
- **Cuadros** (`docs/vitrina/capturas/medicion.json`; CPU frenada 4×, tramo Jinja → Juba): 80 cuadros en 1 400 ms, mediana de
  59,9 cuadros por segundo, cuadro más largo de 50 ms, ninguno de más de 50 ms.
- **Barca sobre el curso**: desvío máximo de 0,13 px en los 80 cuadros del viaje; en las cinco capturas de otro viaje (Asuán →
  Luxor, `vuelta1-viaje/viaje-1.png` … `viaje-5.png`), 0,10 · 0,04 · 0,02 · 0,03 · 0,03 px. Tolerancia: 3 px. Las cinco capturas
  cayeron a los 590, 894, 1 194, 1 488 y 1 779 ms del zarpe (con la CPU frenada la primera sale tarde y la última, ya llegada).
- **Sonido** (`CAPA.sonido.probar()`), ninguna muestra inválida en ningún efecto:

  | Efecto | Duración | Pico | Pico a la salida |
  |---|---|---|---|
  | viento | 5,2 s | −9,4 dBFS | −12,5 dBFS |
  | puerto | 1,1 s | −9,8 dBFS | −13,7 dBFS |
  | moneda | 0,3 s | −9,0 dBFS | −11,2 dBFS |
  | sello | 0,36 s | −8,5 dBFS | −12,3 dBFS |
  | mar | 6,4 s | −7,9 dBFS | −11,5 dBFS |

- **Recorrido en Adulto** (`vuelta1-historia/`, 27 capturas, build de las 08:03, sin monedas de principio a fin): llegó al mar
  sin errores de consola, ningún botón tapado y ningún clic sin efecto. Botones del pie: 277 a 366 × 52 px; fichas de la guía,
  111 × 52; opciones de los eventos, 354 × 48. Miradas una por una: portada, Juba, Jartum, Asuán y el mar.
- **Ojo con la herramienta**: `recorrido` centra cada botón en la pantalla antes de tocarlo; en los eventos eso desplaza la
  página (ver V1-13). El modo se pone y se recarga antes de empezar: la vitrina abre el río al arrancar, y cambiar a Adulto con
  el río ya abierto deja la bajada con las monedas de Niño (así salió la primera corrida, ya reemplazada).

### Hallazgos

| N.º | Gravedad | Pantalla | Captura | Qué se ve | Visto por |
|---|---|---|---|---|---|
| V1-01 | grave | portada | `v0-nilo/01-inicio.png` | El Nilo Azul (un afluente) sale con resplandor dorado: el dorado es solo del río recorrido. | Dirección |
| V1-02 | grave | portada | `v0-nilo/01-inicio.png` | La fila NAVE / COMPAÑERO / PARADAS queda cortada por el pie. | Dirección |
| V1-03 | grave | navegando y parada | `v0-nilo/14-parada-3-navega.png`, `v0-nilo/18-parada-4.png` | El anillo «?» de la próxima parada queda debajo de la píldora del encabezado. | Dirección |
| V1-04 | media | portada | `v0-nilo/01-inicio.png` | El título NILO y la línea «África · 6 650 km…» pisan el río. | Dirección |
| V1-05 | media | navegando y parada | `v0-nilo/14-parada-3-navega.png` | La barca tapa la J de JARTUM. En el build de las 07:59 pasaba también en parada, con JUBA y ASUÁN (esa corrida se reemplazó; sin captura guardada). | Dirección; Verificación |
| V1-06 | media | navegando | `v0-nilo/14-parada-3-navega.png` | La pregunta sale dos veces (globo de Hipo y rótulo del pie) y el perfil queda cortado por el pie. | Dirección |
| V1-07 | media | todas | `v0-nilo/18-parada-4.png` | El subtítulo de la píldora se corta («…hasta el Mediterr…»). | Dirección |
| V1-08 | media | portada y mar | `v0-nilo/01-inicio.png`, `v0-nilo/27-mar.png` | La luz del amanecer y del atardecer del motor tiñe la carta de dorado y de teja. En el build de las 07:59 el mar seguía con una mancha parda abajo de la carta (esa corrida se reemplazó; sin captura guardada). | Dirección; Verificación |
| V1-09 | menor | parada | `v0-nilo/18-parada-4.png` | El sello no es circular (es el del motor, con forma por parada): escudo en Juba, Jartum y Asuán (`vuelta1-historia/08-parada-2.png`, `13-parada-3.png`, `18-parada-4.png`). | Dirección; Verificación |
| V1-10 | menor, para Humberto | parada 2 (Juba), Adulto | `vuelta1-historia/08-parada-2.png` (el texto queda más abajo en el panel) | En Adulto, la carga de Juba nombra a Jartum («…el comercio que hizo rica a Jartum…»): es un texto de `NAVES.nilo.puertos` del juego de siempre. La prueba ya no lo cuenta: quita del panel los textos que vienen tal cual de los datos. | Verificación (prueba) |
| V1-11 | menor | parada 4 (Asuán) | `vuelta1-historia/18-parada-4.png` | A los lados del río, al sur de Asuán, hay cinco o seis marcas triangulares oscuras, como puntas de flecha, que no se entiende qué son. | Verificación |
| V1-12 | menor | evento resuelto | `vuelta1-historia/12-evento-tramo-3-resuelto.png` | En el build de las 07:59 el botón «Seguir hacia …» medía 42 px de alto (171 a 182 × 42; el contrato pide 44); en el de las 08:03 ya mide 354 × 52. | Verificación (medido) |
| V1-13 | grave | parada a la que se llega tras un evento (Jartum, Asuán) | `vuelta1-historia/13-parada-3.png`, `vuelta1-historia/18-parada-4.png` | La pantalla llega desplazada hacia abajo (unos 155 px en Jartum, 95 en Asuán): no se ven la píldora ni los botones redondos, la carta queda cortada y en Asuán el borde de arriba corta el anillo «?»; en Asuán, a 1,8 s del clic, del pie con ZARPAR solo asoma un filo. En `dist/cauces.html` la misma llegada vuelve arriba (`antes/15-parada-4.png`). La herramienta centró la opción del evento antes de tocarla, así que parte del desplazamiento puede ser suyo; lo que se ve es que al llegar no vuelve arriba. | Verificación |
| V1-14 | media | parada a la que se llega tras un evento | `vuelta1-historia/13-parada-3.png` | El botón ZARPAR mide 366 px de ancho (294 en las demás paradas) y el borde derecho de la pantalla lo corta. | Verificación (visto y medido) |
| V1-15 | media | portada | `vuelta1-historia/01-inicio.png` | El título NILO tapa el rótulo TRÓPICO DE CÁNCER (se leen letras sueltas entre las del título) y la barca, en la fuente, queda medio tapada por el borde de arriba de la bitácora. | Verificación |
| V1-16 | menor | portada | `vuelta1-historia/01-inicio.png` | El río entero va en dorado antes de recorrer nada; el contrato dice que el dorado es solo el río recorrido. A confirmar si en la portada es a propósito. | Verificación |
| V1-17 | menor | parada 2 (Juba) | `vuelta1-historia/08-parada-2.png` | El rótulo SUDD queda pegado al botón de volver, arriba a la izquierda. | Verificación |

**Cómo están, en el build de las 08:03 (capturas de `vuelta1-historia/`), los que anotó Dirección sobre `v0-nilo/`**: V1-01, el Nilo
Azul ya es una línea fina y clara, sin resplandor; V1-02, la fila NAVE / COMPAÑERO / PARADAS se ve entera; V1-04, ni el título ni
la línea tocan el río; V1-05, JUBA, JARTUM y ASUÁN ya van separados de la barca en parada; V1-07, la píldora dice «km ≈1 006 de
6 650», sin cortes; V1-08, ni la portada ni el mar muestran tinte dorado o pardo. Siguen: V1-03 (en Juba no se ve ningún anillo:
el curso que falta se mete bajo la píldora), V1-09 (sellos en escudo en Juba, Jartum y Asuán) y V1-11. V1-06 (navegando) no la
volví a mirar.

## Vuelta 2 (2026-11-11, build final: `dist/nilo.html` de 647 KB)

### Medidas

- **Prueba**: `node test/vitrina.js` → `VITRINA OK 647 KB (tope 900)`.
- **Recorridos con clics de verdad**, 390 × 844: Niño (`vuelta2-mercader/`), 27 capturas en 44,6 s; Adulto (`vuelta2-historia/`),
  27 capturas en 45,7 s. Los dos llegaron al mar, sin errores de consola, sin botones tapados ni clics sin efecto. En las 54
  pantallas la página mide 390 px de ancho. Las tres paradas que siguen a un evento (Jartum, Asuán, El Cairo) llegan sin
  desplazamiento, con la píldora y los botones a la vista, y ZARPAR mide 294 × 52 como en las demás (354 × 52 en la portada).
  La herramienta ya solo mueve la página si el botón no está entero a la vista, y anota el desplazamiento en cada paso.
- **Cuadros** (`medicion.json`; CPU frenada 4×, tramo Jinja → Juba): 85 cuadros en 1 400 ms, mediana de 59,9 cuadros por segundo,
  cuadro más largo de 16,9 ms.
- **Barca sobre el curso**: desvío máximo de 0,12 px en los 85 cuadros; en las cinco capturas de otro viaje (`vuelta2-viaje/`, al
  21, 55, 84, 99 y 100 % del avance): 0,08 · 0,02 · 0,06 · 0,05 · 0,02 px. Tolerancia: 3 px.
- **Sonido** (`CAPA.sonido.probar()`), seis efectos y ninguna muestra inválida:

  | Efecto | Duración | Pico | Pico a la salida |
  |---|---|---|---|
  | viento | 5,2 s | −9,4 dBFS | −12,5 dBFS |
  | puerto | 1,1 s | −9,8 dBFS | −13,7 dBFS |
  | moneda | 0,3 s | −9,0 dBFS | −11,2 dBFS |
  | sello | 0,36 s | −8,5 dBFS | −12,3 dBFS |
  | mar | 6,4 s | −7,9 dBFS | −11,5 dBFS |
  | acierto | 0,18 s | −13,8 dBFS | −17,0 dBFS |

### Capturas que se versionan (sueltas en `docs/vitrina/capturas/`)

`antes-1-inicio.png`, `antes-2-navegando.png`, `antes-3-parada-4.png`, `antes-4-mar.png` y el «después» de los mismos cuatro
momentos (portada, navegando en Jartum, Asuán y el mar) en tres tamaños: `despues-390-…` (390 × 844, escala 2), `despues-820-…`
(820 × 1180) y `despues-1440-…` (1440 × 900); las anchas van a escala 1 para que pesen como las del teléfono (0,5 a 0,8 MB cada
una). Las doce salieron sin errores de consola y con la página del ancho de la ventana. Miradas: las cuatro de 390,
`despues-820-2-navegando.png`, `despues-1440-1-portada.png` y `despues-1440-3-parada-4.png`.

### Hallazgos nuevos (todos menores)

| N.º | Gravedad | Pantalla | Captura | Qué se ve |
|---|---|---|---|---|
| V2-01 | menor | parada (bitácora) | `despues-390-3-parada-4.png` | El sello del motor lleva en el aro letras de unos 8 px (decorativas), por debajo de los 11 px del contrato. |
| V2-02 | menor | parada y delta | `despues-390-3-parada-4.png`, `despues-390-4-mar.png`, `despues-1440-3-parada-4.png` | En las vistas cercanas el relieve se ve en manchas suaves, sin forma. |
| V2-03 | menor | portada a 1440 | `despues-1440-1-portada.png` | El rótulo SUDÁN sale dos veces (bajo el lago Nasser y en el centro del país) y EGIPTO no aparece. |
| V2-04 | menor | portada | `despues-1440-1-portada.png`, `despues-390-1-portada.png` | La bitácora de la portada queda casi vacía: el globo de Hipo y la fila NAVE / COMPAÑERO / PARADAS; a 1440 hay unos 580 px de papel en blanco hasta ZARPAR. |
| V2-05 | menor | bajada a 390 | `despues-390-2-navegando.png` | A 390 no se ve el riel Bajar · Ordenar · Recitar · Preguntar; a 820 y 1440 va en el pie. A confirmar si es a propósito. |
| V2-06 | menor | parada 6 (El Cairo) | `vuelta2-mercader/26-parada-6.png` | La barca queda pegada al pictograma de las pirámides de Guiza. |
| V2-07 | menor | paradas y mar | `despues-390-3-parada-4.png`, `despues-390-4-mar.png` | El control de volver cambia de forma: enlace «‹ Atrás» en las paradas y botón con borde «‹ ATRÁS» en El Cairo y en el mar. |
| V2-08 | menor | mar | `despues-390-4-mar.png` | Hipo sale dormido («z z») mientras dice «Ganaste 6 monedas. La próxima, más.». A confirmar si es el ánimo que se quiere. |

## Estado final de cada hallazgo

| N.º | Gravedad | Estado |
|---|---|---|
| V1-01 | grave | corregido en la vuelta 1 (el Nilo Azul es una línea fina, sin resplandor) |
| V1-02 | grave | corregido en la vuelta 1 |
| V1-03 | grave | corregido en la vuelta 2: en navegando (Jartum) y en la parada de Asuán el anillo «?» se ve entero, debajo de la píldora |
| V1-04 | media | corregido en la vuelta 1 |
| V1-05 | media | corregido en la vuelta 1 (JARTUM y ASUÁN van separados de la barca) |
| V1-06 | media | corregido en la vuelta 2: la pregunta sale una vez, en el globo de Hipo, y el perfil se ve entero |
| V1-07 | media | corregido en la vuelta 1 |
| V1-08 | media | corregido en la vuelta 1 |
| V1-09 | menor | queda: es el sello del motor (escudo en Juba, Jartum y Asuán; círculo en El Cairo) |
| V1-10 | menor, para Humberto | queda: texto de `NAVES.nilo.puertos` del juego de siempre |
| V1-11 | menor | queda: las marcas oscuras junto al río parecen ser las ensenadas del lago Nasser; a 820 y 1440 se ven más (`despues-1440-3-parada-4.png`) |
| V1-12 | menor | corregido en la vuelta 1 |
| V1-13 | grave | corregido en la vuelta 2 (medido: ancho de página 390 y desplazamiento 0 en las paradas que siguen a un evento, en los dos modos) |
| V1-14 | media | corregido en la vuelta 2 (ZARPAR mide 294 × 52 en todas las paradas) |
| V1-15 | media | corregido en la vuelta 2 (TRÓPICO DE CÁNCER va a la derecha y la barca se ve entera) |
| V1-16 | menor | cerrado: es a propósito (en la portada, el hilo de oro es el río entero) |
| V1-17 | menor | queda: a 390 no lo volví a mirar; a 820, en navegando, un rótulo asoma detrás del botón de volver (`despues-820-2-navegando.png`) |
| V2-01 a V2-08 | menor | quedan |

**Pendientes graves: ninguno. Medias: ninguna. Quedan 12 menores** (V1-09, V1-10, V1-11, V1-17 y V2-01 a V2-08); tres de ellos
son preguntas a confirmar (V2-05, V2-08 y el origen de V1-11).

## Corrida larga, vuelta A (2026-11-11, de 08:27 a 09:15)

### Lo que hay de nuevo para medir

- **`node tools/captura.js auditar <archivo.html> [390x844]`**: arma 16 estados con funciones del motor (la portada; navegar en la
  primera bajada; la guía sin responder, bien y mal; la parada con el sello nuevo y con el sello pendiente; el mercado con la
  bodega llena; el evento sin responder, bien y mal; la parada en Adulto; la barca anclada; la última parada; el mar en Niño y
  en Adulto) y mide en cada uno el texto más chico (en píxeles de pantalla, también el del SVG), lo tocable de menos de 44 px,
  el contraste de cada texto HTML contra lo que tiene debajo, el ancho de la página, nombres de paradas futuras en la carta,
  emojis, textos cortados y rótulos de la carta tapados o encimados. Deja `auditoria.json` (y `auditoria-360x640.json`,
  `auditoria-844x390.json`) en `docs/vitrina/capturas/`. Sale con código 1 si hay página ancha, nombres futuros o emojis.
- **`node tools/captura.js estados <archivo.html> <carpeta> [390x844]`**: una captura por estado. Corridas: `estados-390/`,
  `estados-360/` (360 × 640) y `estados-acostado/` (844 × 390), 16 capturas cada una, sin errores de consola. Miradas 17: de
  390, la portada, navegar-primera, guía mal, sello pendiente, mercado lleno, evento mal, anclada y El Cairo; de 360, la portada,
  la guía sin responder y la parada; de acostado, la portada, la guía sin responder, la parada y el mar.
- **`test/vitrina.js`, cifras fijas**: los kilómetros y la altura de cada parada, la longitud, los nombres en su orden y lo que se
  lee (kicker, tramo y altura) se comparan con los de Cauces, sacados de `dist/cauces-amplia.html` en un proceso hijo; cada
  parada cae a 0,25° o menos del curso y sus `idx` crecen. Pasa: `VITRINA OK 609 KB`.

- **Regresión sobre el build de las 08:54 (609 KB, ya con la falúa nueva e Hipo nadando)**: dos recorridos con clics de verdad a
  390 × 844 (`vueltaA-mercader/` y `vueltaA-historia/`), 27 capturas y 41,9 s cada uno, los dos al mar, sin errores de consola,
  sin botones tapados y con la página de 390 px en las 54 pantallas. `medir` (`medicion-vueltaA.json`; CPU 4×, Jinja → Juba):
  84 cuadros en 1 383 ms, mediana de 59,9 cuadros por segundo, cuadro más largo de 16,9 ms; la barca, a 0,12 px del curso como
  máximo (en cinco capturas: 0,05 · 0 · 0,08 · 0,05 · 0,11); los seis efectos de sonido, sin muestras inválidas y con los mismos
  picos que en la vuelta 2.

### Auditoría automática (repetida sobre los builds de las 08:47, las 08:52 y las 08:58, de 609 a 610 KB, con los mismos números)

| Tamaño | Texto más chico | Textos de menos de 11 px | Tocables de menos de 44 px | Contraste de menos de 4,5 | Página ancha | Nombres futuros en la carta | Emojis |
|---|---|---|---|---|---|---|---|
| 390 × 844 | 10,2 px | 3 (rótulos del perfil), en 4 estados | 0 | 0 | no | 0 | 0 |
| 360 × 640 | 9,4 px | 3 (los mismos), en 4 estados | 0 | 0 | no | 0 | 0 |
| 844 × 390 | 9,8 px | 3 (los mismos) y 3 rótulos de la carta a 10,9 px | 0 | 0 | no | 0 | 0 |

Por estado, a 390 × 844 (en los 16, cero tocables chicos, cero contrastes bajos, página de 390 px, sin nombres futuros ni emojis):

| Estado | Texto más chico | Textos de menos de 11 px | Asoman a medias sobre el pie |
|---|---|---|---|
| portada | 11 px | 0 | 0 |
| navegar-primera | 10,2 px | 2 | 0 |
| guia-sin-responder, guia-bien, guia-mal | 10,2 px | 3 | 0 |
| parada-sello-nuevo, parada-adulto, anclada | 11 px | 0 | 1 (el texto de la postal) |
| parada-sello-pendiente | 11,9 px | 0 | 1 |
| mercado-lleno, evento, evento-bien, evento-mal | 11 px | 0 | 0 |
| parada-ultima | 11 px | 0 | 1 |
| mar-nino, mar-adulto | 11 px | 0 | 0 |

Por estado se midió el contraste de 13 a 37 textos HTML y hay de 4 a 10 tocables. Lo que va sobre el mapa se mide aparte y no
hace fallar: su contraste sale de la captura, contra los píxeles que rodean cada texto (107 textos a 390 × 844, sumando los
estados; los tapados por la hoja o la píldora no se miden). Los títulos, la píldora y los nombres de las paradas pasan de 4,5 a 1;
los rótulos secundarios de la carta, no (A-12). Lo que va dentro de un dibujo (el sello y el perfil, 21 textos) no se mide.

### Hallazgos nuevos

| N.º | Gravedad | Pantalla | Captura | Qué se ve | Visto por |
|---|---|---|---|---|---|
| A-01 | media | navegando y parada, a 360 × 640 | `estados-360/03-guia-sin-responder.png`, `estados-360/06-parada-sello-nuevo.png` | La píldora tapa en parte lo que la carta pone debajo: el anillo «?» de la próxima parada (3 de 9 puntos en navegar y con la guía sin responder; 6 de 9 con la guía bien y en el evento), el rótulo SUDD en las paradas (6 de 9) y «Nilo Azul» con la guía mal (3 a 4 de 9); con la guía mal, además, la hoja tapa una punta del rótulo JUBA (3 de 9). Sigue igual en el build de las 08:58. A 390 × 844 y acostado, nada. | auditoría y a ojo |
| A-02 | media | navegar en la primera bajada, antes de zarpar | `estados-390/02-navegar-primera.png` | Hipo ya pregunta «¿Cuál es la próxima parada?» con la lista de las seis a la vista y sin fichas para responder; el pie dice «Zarpar ›». | a ojo |
| A-03 | media | navegando, a 360 × 640 y acostado | `estados-360/03-guia-sin-responder.png`, `estados-acostado/03-guia-sin-responder.png` | El perfil queda bajo el pie: a 360 asoma su encabezado cortado por la mitad («Perfil del río», «de 1 149 m en la fuente a 0 m en el…»); acostado, solo «1 149 m». Se destapa al bajar. En el build de las 08:55 ya no se ve: el pie lleva «‹ Atrás» y las fichas en un renglón y el perfil entra entero, a 360 y acostado. | auditoría y a ojo |
| A-04 | menor | navegando | `estados-390/05-guia-mal.png` | Los rótulos del perfil («1 149 m», «457 m», «Altura del cauce») miden 10,2 px (9,4 a 360 × 640; 9,8 acostado): por debajo de 11. | auditoría |
| A-05 | menor | navegando | `estados-390/02-navegar-primera.png` | En el perfil, «1 149 m» queda pisado por la línea que baja de la fuente. | a ojo |
| A-06 | menor | parada y navegando | `estados-390/07-parada-sello-pendiente.png`, `estados-390/05-guia-mal.png` | La barca llega a la parada girada con el rumbo del tramo (casi vertical) y al pasar a navegar, o al reabrir el río, queda horizontal: cambia de postura entre dos pantallas de la misma parada. En el build de las 08:54, con la falúa nueva, llega horizontal y ya no se ve (`vueltaA-mercader/08-parada-2.png`). | a ojo |
| A-07 | menor | parada 1 (Jinja) | `estados-390/extra-jinja-sello.png` | El sello de Jinja dice «0° N». | a ojo |
| A-08 | menor | portada, a 360 × 640 | `estados-360/01-portada.png` | Sobre el pie asoma una raya suelta: es el filete de lo que sigue (el riel), que queda debajo del pie. En el build de las 08:55 ya no se ve: el riel entra entero sobre ZARPAR. | a ojo |
| A-09 | menor | navegar en la primera bajada, acostado | `estados-acostado/02-navegar-primera.png` | Tres rótulos de la carta (ECUADOR, LAGO VICTORIA, UGANDA) miden 10,9 px: al límite de los 11. | auditoría |
| A-10 | menor | parada, a 360 × 640 | `estados-360/06-parada-sello-nuevo.png` | El kicker se parte en dos renglones entre «KM» y «≈1 006 DE 6 650». En el build de las 08:55 el kicker dice solo «PARADA 2 DE 6» y ya no se parte. | a ojo |
| A-11 | menor, para Humberto | mercado (Niño) | `estados-390/08-mercado-lleno.png` | Con una moneda dice «1 monedas · bodega 3 de 3»: es el texto del motor de siempre (`renderMercado`). | a ojo |
| A-12 | menor (aparte: sobre el mapa, a decidir) | la carta, en casi todos los estados | `estados-390/01-portada.png`, `estados-390/03-guia-sin-responder.png` | Nueve rótulos secundarios de 11 px quedan por debajo de 4,5 a 1 contra lo que tienen alrededor, medido en la captura a 390 × 844 (mediana): ECUADOR 2,65; Nilo Azul 3,21; LAGO VICTORIA 3,26; ETIOPÍA 3,43; Nilo Blanco 3,48; UGANDA 3,69; SUDD 3,80; SUDÁN 3,80; SUDÁN DEL SUR 3,84. Acostado, también EGIPTO, 3,96. Los nombres de las paradas y el mar Mediterráneo pasan. | auditoría (captura) |
| A-13 | menor | portada, con la falúa nueva (build de las 08:54) | `vueltaA-mercader/01-inicio.png` | La falúa nueva, más grande, queda pegada por abajo al rótulo LAGO VICTORIA: su sombra parece pisar las letras del medio. | a ojo |

### Abiertos de la primera corrida

| N.º | Gravedad | Qué era | Cómo se ve en la vuelta A (build de las 08:44 a 08:47) |
|---|---|---|---|
| V1-09 | menor | el sello no es circular | abierto en la lista; en este build el sello ya es circular (`estados-390/13-anclada.png`) |
| V1-10 | menor, para Humberto | la carga de Juba nombra a Jartum | abierto |
| V1-11 | menor | marcas oscuras junto al río, al sur de Asuán | abierto; no se volvió a mirar |
| V2-01 | menor | letras de 8 px en el sello | abierto en la lista; en este build el sello lleva «JUBA» a 13 px y «5° N» a 11 px |
| V2-02 | menor | relieve en manchas suaves en las vistas cercanas | abierto; en Juba y en El Cairo ya se ve relieve con detalle, con zonas borrosas (`estados-390/14-parada-ultima.png`) |
| V2-04 | menor | la bitácora de la portada queda casi vacía | abierto en la lista; en este build trae el riel bajo la fila (`estados-390/01-portada.png`) |
| V2-05 | menor | a 390 no se ve el riel | abierto en la lista; el riel está en la portada, y en parada y navegando sigue sin verse a 390 |
| V2-06 | menor | en El Cairo la barca queda pegada al pictograma de Guiza | abierto en la lista; a las 08:44 seguía encima de los triángulos y en el build de las 08:55 el pictograma ya no sale bajo la barca (`estados-390/14-parada-ultima.png`) |
| V2-08 | menor | en el mar Hipo sale dormido mientras habla | abierto: sigue («z z» en `estados-acostado/15-mar-nino.png`) |
| V1-17 | menor | un rótulo asoma detrás del botón de volver | corregido en el retoque de las 08:18 (lo comprobó Dirección); SUDD queda separado del botón en `estados-acostado/06-parada-sello-nuevo.png` |
| V2-03 | menor | SUDÁN dos veces y sin EGIPTO a 1440 | corregido en el retoque de las 08:18 (lo comprobó Dirección) |
| V2-07 | menor | «‹ Atrás» cambia de forma | corregido en el retoque de las 08:18: enlace también en El Cairo (`estados-390/14-parada-ultima.png`) |

**Vuelta A: ningún hallazgo grave. De las 3 medias nuevas siguen dos (A-01, la píldora sobre el anillo a 360 × 640, y A-02, la
pregunta de Hipo antes de zarpar); A-03 ya no se ve en el build de las 08:55. De las 10 menores nuevas (A-04 a A-13) ya no se ven
tres (A-06, A-08 y A-10) y siguen siete. De las 9 menores abiertas de la primera corrida, cinco ya no se ven en los builds de la
vuelta A (V1-09, V2-01, V2-04, V2-06 y, en la portada, V2-05) y cuatro siguen (V1-10, V1-11, V2-02 y V2-08). Las capturas de
`estados-390/`, `estados-360/` y `estados-acostado/` son las del build de las 08:55.**

## Corrida larga, vuelta B (2026-11-11, de 09:11 a 09:21; build de las 09:11, 610 KB)

Capturas en `docs/vitrina/capturas/vueltaB/` (fuera de git), con hojas de contacto `hoja-estados-390.png`, `hoja-estados-360.png`,
`hoja-estados-1440.png`, `hoja-recorrido-historia-a.png` y `-b.png` (las arma `hojas.py`, en la misma carpeta).

- **Recorridos a 390 × 844** (`mercader/` y `historia/`): 27 capturas cada uno, 40,8 y 40,9 s, los dos llegaron al mar, sin errores
  de consola.
- **Estados** a 390 × 844, 360 × 640 y 1440 × 900 @1 (`estados-390/`, `estados-360/`, `estados-1440/`): 16 cada uno, sin errores de
  consola.
- **Auditoría** (`aud-390.json`, `aud-360.json`): en los 16 estados y en los dos tamaños, texto más chico 11 px, 0 textos de menos de
  11 px (el perfil ya no baja de 11: A-04 no aparece), 0 tocables de menos de 44 px, 0 contrastes HTML de menos de 4,5, página sin
  ensanchar, sin nombres futuros ni emojis. Textos cortados: solo los que asoman bajo el pie (la imagen para recordar en 5 estados a 390;
  el texto de la llegada en el mar a 360). Rótulos tapados, solo a 360 × 640: el anillo «?» por la píldora (navegar-primera 6 de 9,
  guía sin responder 3 de 9, guía bien 6 de 9, evento 6 de 9), SUDD por la píldora (cuatro estados de parada, 6 de 9) y JUBA por la
  hoja con la guía mal (3 de 9). Sobre el mapa, contraste medido en la captura por debajo de 4,5 a 1 (aparte, no hace fallar): a 360,
  8 rótulos (ECUADOR 2,73; brazo de Damieta 3,13; brazo de Rosetta 3,24; Nilo Blanco 3,52; la N del norte 3,6; UGANDA 3,66; SUDD 3,8;
  «250 km» 4,47); a 390, los mismos más LAGO VICTORIA 3,26, Nilo Azul 3,26, ETIOPÍA 3,43, SUDÁN 3,8, SUDÁN DEL SUR 3,84 y «200 km» 4,4.

| N.º | Gravedad | Pantalla y tamaño | Captura | Qué se ve |
|---|---|---|---|---|
| B-01 | media | evento entre Jartum y Asuán, resuelto (Adulto), 390 × 844 | `historia/17-evento-tramo-4-resuelto.png` | La nota del acierto dice el orden entero, «Jinja → Juba → Jartum → Asuán → Luxor → El Cairo», con Luxor y El Cairo todavía por llegar: nombres de paradas futuras fuera de las fichas de la guía y de la lista de la primera bajada. Lo mismo en el evento de Luxor a El Cairo (`historia/25-evento-tramo-6-resuelto.png`), donde falta solo El Cairo. |
| B-02 | media | guía mal, 360 × 640 | `estados-360/05-guia-mal.png` | La hoja corta por la mitad la falúa, a Hipo y el rótulo JUBA; no se ven ni el anillo «?» ni el hilo de oro: el mapa queda sin lo que importa. (Es A-01 en su peor caso; la auditoría lo da como JUBA tapado 3 de 9.) |
| B-03 | media | navegar y evento, 360 × 640 | `estados-360/09-evento.png`, `estados-360/02-navegar-primera.png` | El anillo «?» de la próxima parada queda bajo la píldora NILO (6 de 9 puntos); en las paradas, SUDD también (`estados-360/06-parada-sello-nuevo.png`). Sigue A-01. |
| B-04 | media | llegada al mar, 390 × 844 y 360 × 640 | `estados-390/15-mar-nino.png` | La falúa queda dibujada en la desembocadura, sobre la costa del Mediterráneo, mientras el texto de abajo dice «La falúa no sale al mar: en el delta la carga sigue en gabarra hasta Alejandría». El hilo de oro también llega hasta la costa. |
| B-05 | menor | evento entre Luxor y El Cairo, 390 × 844 | `historia/24-evento-tramo-6.png`, `historia/25-evento-tramo-6-resuelto.png` | El rótulo «Alejandría» queda cortado por la píldora NILO («Alejandr…»). |
| B-06 | menor | portada, 390 × 844 | `estados-390/01-portada.png` | Sigue A-13: la falúa e Hipo quedan encima del rótulo LAGO VICTORIA; la sombra de la barca pisa «VICTORIA». |
| B-07 | menor | parada y navegar, 390 × 844 | `estados-390/06-parada-sello-nuevo.png`, `estados-390/05-guia-mal.png` | Hipo nadando queda pegado al rótulo de la parada (JUBA empieza a 4-5 px de su hocico): no lo tapa, pero se leen como una sola pieza. |
| B-08 | menor | navegar con la guía mal, 390 × 844 | `estados-390/05-guia-mal.png` | El rótulo «Nilo Azul» va encima del trazo del afluente (la «l» final cruza la línea). |
| B-09 | menor | navegar (Adulto), 390 × 844 | `historia/19-parada-4-navega.png` | La escala gráfica «200 km» va a la derecha, sobre la línea punteada de la frontera de los 22° N; en las demás pantallas va a la izquierda: salta de lado entre pantallas seguidas (`historia/18-parada-4.png` la tiene a la derecha, `historia/21-parada-5.png` a la izquierda). |
| B-10 | menor | navegar al empezar (Adulto), 390 × 844 | `historia/03-navega.png`, `historia/04-navega-respondida.png` | Antes de la primera parada, la cabecera de las fichas no tiene título: solo «0 DE 6 PARADAS» a la derecha y un hueco a la izquierda, donde en las demás va «Tres Jotas…». |
| B-11 | menor | todos los estados, 1440 × 900 | `estados-1440/04-guia-bien.png` | En el ancho, la falúa e Hipo miden unos 50 y 20 px y quedan pegados al borde de abajo del mapa (guía, evento); la columna de papel deja más de la mitad vacía bajo el perfil. La píldora NILO tapa el trazo blanco del río en la parte de arriba. |
| B-12 | menor | evento, 390 × 844 | `estados-390/09-evento.png` | La cabecera dice «km ≈1 006» (Juba) mientras la falúa está ya a mitad del tramo, pasado el Sudd. |
| B-13 | menor | perfil, todos los tamaños | `estados-390/02-navegar-primera.png` | Sigue A-05: «1 149 m» pisado por la línea que baja de la fuente. |
| B-14 | menor | mar en Niño, 390 y 360 | `estados-390/15-mar-nino.png` | Sigue V2-08: Hipo dormido («z z») en el retrato mientras habla. |
| B-15 | menor, para Humberto | mercado (Niño), 390 × 844 | `estados-390/08-mercado-lleno.png` | Sigue A-11: «1 monedas». |

Revisado y sin hallazgo: el río (hilo de oro) y la vela de la falúa son lo único dorado en la carta en las 16 + 27 pantallas (el oro de las
postales queda en su ficha); un solo título dominante por pantalla (nombre de la parada, «Tres Jotas…» o NILO en la portada); sin
emojis ni dibujos de otro trazo (el cocodrilo del evento es un icono de línea del motor, como los demás); márgenes de 18 px y
separaciones parejas en la hoja a 390 y 360; la falúa con su carga (en Adulto, la carga se ve en cubierta) e Hipo se leen a 390 y 360;
la flecha del norte, siempre arriba a la derecha bajo el botón de sonido, sin pisar nada.

**Ya no se ven de la vuelta A:** A-04 (la auditoría no encuentra textos de menos de 11 px, a 390 ni a 360), A-03, A-06, A-08 y A-10
(como ya se había anotado). Siguen: A-01 (B-02, B-03), A-05 (B-13), A-11 (B-15), A-12 (los contrastes de arriba), A-13 (B-06) y
V2-08 (B-14); A-02 cambió: en la primera bajada el pie dice «Zarpar ›» con la lista a la vista y la pregunta de Hipo ya está en el globo
(`estados-390/02-navegar-primera.png`), igual que en la vuelta A. A-07 y A-09 no se volvieron a mirar (Jinja y acostado no se
capturaron en esta vuelta).

## Corrida larga, verificación final (2026-11-11, de 09:30 a 09:45; `dist/nilo.html` de 617 KB, sin reconstruir)

Capturas en `docs/vitrina/capturas/final/` (fuera de git): `mercader/`, `historia/`, `estados-390/`, `estados-360/`, `estados-acostado/`,
`estados-1440/`, `auditoria-*.json`, `medir/` y las hojas `hoja-estados-390.png`, `-360`, `-acostado` y `-1440` (las arma `hojas.py`).
Versionadas: las doce `despues-*.png` (rehechas con este build), las cuatro `intermedio-390-*.png` (las `despues-390` de la corrida de
60 minutos, sacadas de HEAD), `comparacion-390.png` (antes · 60 minutos · corrida larga) y `medicion.json`.

- **Recorridos a 390 × 844**: mercader e historia, 27 capturas cada uno, 41,7 y 41,2 s, los dos llegaron al mar, sin errores de consola.
- **Estados**: 16 por tamaño (390 × 844, 360 × 640, 844 × 390 y 1440 × 900 @1), sin errores de consola.
- **Auditoría**, en los cuatro tamaños: texto más chico 11 px, 0 textos de menos de 11 px, 0 toques de menos de 44 px, 0 contrastes HTML
  de menos de 4,5, página sin ensanchar, 0 nombres futuros, 0 emojis, 0 rótulos tapados en la carta. Contraste bajo sobre la carta, medido
  en la captura: ninguno a 390, 360 ni acostado; a 1440, solo ECUADOR (3,48 de mediana). Cortados: a 360, «Jinja» recortado 9 px por el
  borde de la carta en los tres estados del evento; a 1440, en el mar en Niño, el párrafo de la ruta moderna queda bajo el pie aun con la
  página bajada del todo. A medias sobre el pie (se destapan al bajar): 2 textos a 390, 2 a 360, 5 acostado, 2 a 1440.
- **`medir`** (`medicion.json`; CPU 4×, Jinja → Juba, 390 × 844): 80 cuadros en 1 407 ms, mediana de 55,6 cuadros por segundo, cuadro más
  largo de 18,7 ms, ninguno de más de 50 ms; la barca a 0,09 px del curso como máximo (cinco capturas: 0 · 0,01 · 0,04 · 0,02 · 0,07); los
  seis efectos (viento, puerto, moneda, sello, mar, acierto) sin muestras inválidas, picos de 0,20 a 0,40 (−13,8 a −7,9 dBFS), sin errores.

| N.º | Gravedad | Pantalla y tamaño | Captura | Qué se ve |
|---|---|---|---|---|
| F-01 | media | llegada al mar, 390 × 844, 360 × 640 y 1440 × 900 | `despues-390-4-mar.png`, `final/estados-360/15-mar-nino.png` | Sigue B-04: la falúa con Hipo está dibujada en la desembocadura, sobre la costa, y el hilo de oro llega hasta el mar, mientras el texto dice «La falúa no sale al mar». |
| F-02 | menor | evento, 360 × 640 | `final/estados-360/09-evento.png` | El rótulo «Jinja» queda recortado 9 px por el borde de la carta (auditoría), en los tres estados del evento. |
| F-03 | menor | mar en Niño, 1440 × 900 | `final/estados-1440/15-mar-nino.png` | El párrafo de la ruta moderna («La Presa Alta de Asuán (1970)…») queda bajo el pie aun con la columna bajada del todo (auditoría). |
| F-04 | menor | carta, 1440 × 900 | `final/estados-1440/08-mercado-lleno.png` | ECUADOR, a 3,48 a 1 de contraste contra el relieve (queda A-12 solo en el ancho). |
| F-05 | menor | todos los estados, 1440 × 900 | `final/hoja-estados-1440.png` | Sigue B-11: la falúa e Hipo chicos (≈ 50 y 20 px) en una carta muy ancha; la columna de papel deja mucho vacío bajo el contenido. |
| F-06 | menor, para Humberto | mercado (Niño) | `final/estados-360/08-mercado-lleno.png` | Sigue B-15: «1 monedas». |

Revisado y sin hallazgo: el río (hilo de oro) y la vela y la carga de la falúa son lo único dorado de la carta en las hojas y la comparación;
un solo título dominante por pantalla (NILO en la portada, la ciudad en la parada, «Tres Jotas…» navegando y en el mar); a 360 × 640 la
píldora NILO ya no tapa el anillo «?» ni SUDD, y con la guía mal la carta muestra la falúa, Hipo, JUBA y el anillo enteros
(`final/estados-360/05-guia-mal.png`); sin emojis; márgenes parejos en el papel; la falúa con su carga e Hipo nadando se leen a 390 y 360 y
no tapan nombres (JUBA, JARTUM, ASUÁN y EL CAIRO quedan a su derecha); la escala abajo a la izquierda y el norte arriba a la derecha, bajo
el botón de sonido, en todas las pantallas de 390 y 360. La comparación muestra el salto: de la pantalla del motor (mapa chico, lista y
riel) a la carta con relieve y la bitácora de papel; entre «60 minutos» y «corrida larga» cambian la falúa (con carga) e Hipo nadando, el
sello circular, el riel en la portada, la escala y el norte, y la carta de 10 m con el delta rotulado.

### Estado de cada hallazgo de la corrida larga

| N.º | Estado |
|---|---|
| A-01 | corregido: a 360 × 640 la auditoría no da rótulos tapados y la píldora deja ver el anillo y SUDD |
| A-02 | queda como diseño: la pregunta de Hipo llega con la lista a la vista y «Zarpar ›» (enseñar antes de preguntar); no se volvió a cambiar |
| A-03 | corregido (desde el build de las 08:55) |
| A-04 | corregido: 0 textos de menos de 11 px en los cuatro tamaños |
| A-05 | queda: «1 149 m» sigue junto a la línea de la fuente en el perfil (`final/estados-360/03-guia-sin-responder.png`) |
| A-06 | corregido |
| A-07 | queda sin mirar (el sello de Jinja no se capturó) |
| A-08 | corregido |
| A-09 | corregido: acostado, 0 textos de menos de 11 px |
| A-10 | corregido |
| A-11 | del motor de Cauces (`renderMercado`): queda, «1 monedas» (F-06) |
| A-12 | corregido a 390, 360 y acostado; queda ECUADOR a 1440 (F-04) |
| A-13 | corregido: en la portada la falúa queda sobre el lago, bajo LAGO VICTORIA, sin pisar letras |
| B-01 | queda sin confirmar: la auditoría (que no arma los eventos de Adulto con la nota del acierto) da 0 nombres futuros; no se miró `historia/17` ni `25` |
| B-02 | corregido |
| B-03 | corregido |
| B-04 | queda (F-01) |
| B-05 | queda sin mirar (`final/historia/24-…` no se revisó a tamaño completo) |
| B-06 | corregido (es A-13) |
| B-07 | corregido: Hipo nada detrás de la falúa y el rótulo de la parada queda separado |
| B-08 | queda sin mirar |
| B-09 | queda sin mirar (la escala está a la izquierda en todas las de las hojas) |
| B-10 | queda sin mirar |
| B-11 | queda (F-05) |
| B-12 | queda: en el evento la cabecera sigue diciendo «km ≈1 006» con la falúa a mitad del tramo (`final/estados-360/09-evento.png`) |
| B-13 | queda (es A-05) |
| B-14 | queda sin mirar (Hipo en el retrato del mar, a tamaño completo) |
| B-15 | del motor de Cauces: queda (A-11, F-06) |

**Quedan abiertos: 0 graves, 2 medios (B-04 / F-01, la falúa en el mar, y B-01, nombres futuros en la nota del evento de Adulto, sin
confirmar) y 13 menores (A-05/B-13, A-07, A-11/B-15, A-12 en el ancho / F-04, B-05, B-08, B-09, B-10, B-11/F-05, B-12, B-14, F-02, F-03);
A-02 queda como diseño. Los que no se volvieron a mirar no se dan por corregidos.**
