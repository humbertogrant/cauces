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
