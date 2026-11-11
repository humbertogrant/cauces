# Informe de la corrida larga: vitrina del Nilo

Segunda corrida autónoma del 2026-11-11, de 08:27 a 09:47 (80 de los 180 minutos que tomé como presupuesto), sobre la misma
rama y con el mismo alcance que la de 60 minutos (su informe quedó en `informe-60-min.md`).

1. `dist/nilo.html` (617 KB; tope 900) subió de nivel en lo que había quedado a medias: la falúa lleva la carga a la vista (el
   obelisco de Asuán, acostado en la cubierta) e Hipo nada a popa; de cerca la carta tiene relieve nítido, el río con su forma real
   y el delta con sus dos brazos; la bitácora tiene sello circular propio y el riel de etapas vuelve a estar a mano en el teléfono.
2. Ninguna cifra del juego cambió con el cauce nuevo: los kilómetros y las alturas de las seis paradas son los de Cauces, y una
   prueba lo compara contra `dist/cauces-amplia.html`. Cauces y Exploradores siguen byte a byte iguales; `npm test`, 9 de 9.
3. Hubo cuatro vueltas (construir, dos de arreglos y la verificación final) y una auditoría automática nueva sobre 16 estados:
   ninguna letra de menos de 11 px, ningún toque de menos de 44 px, ningún contraste bajo, la página nunca se ensancha.
4. Cerré a los 80 minutos y no a los 180: ya solo quedaban hallazgos menores, que es la condición de parada de la instrucción, y
   el consumo iba más rápido de lo que supuse (ver «Tiempo y consumo»).
5. Sigue sin verificarse lo mismo que antes: cómo suena y cómo lo juega un niño en un teléfono de verdad.

## Tiempo y consumo

| Tramo | Hora | Qué |
|---|---|---|
| Planear | 08:27 – 08:33 | Plan, contrato ampliado, enganche del cauce fino con las cifras fijas |
| Vuelta A (construir) | 08:30 – 09:11 | Trazo, Carta (dos pasadas), Bitácora y Verificación, en paralelo |
| Vuelta B (arreglar) | 09:11 – 09:22 | Verificación integrada con hojas de contacto, y los arreglos de bitácora y carta |
| Vuelta C (retocar) | 09:22 – 09:30 | Retoques de carta y de hoja |
| Verificación final e informe | 09:30 – 09:47 | Recorridos, auditoría en cuatro tamaños, mediciones, capturas, este informe |

- **Plan de consumo** (lo que marca la cuenta): el límite semanal del modelo de la corrida pasó de 27 % a 45 % (18 puntos) y el
  general, de 24 % a 33 % (9 puntos), medido al empezar y a las 09:31; falta sumar la verificación final y el cierre.
- **Dónde se fue:** en los primeros 35 minutos se gastaron 15 de esos 18 puntos, porque retomé a los cuatro subagentes de la primera
  corrida, que ya cargaban entre 380 y 680 mil tokens de contexto, y cada llamada suya lo relee. Desde las 09:11 usé agentes nuevos,
  de contexto chico y con encargos angostos: las dos vueltas siguientes costaron 3 puntos en 29 minutos.
- **Subagentes:** cuatro de contexto grande (Verificación ≈ 680 mil tokens al cerrar, Carta ≈ 656 mil, Bitácora ≈ 535 mil y Trazo,
  nuevo, ≈ 383 mil) y seis nuevos (entre 100 y 190 mil cada uno).
- El entorno no muestra el costo en dinero.

## Vueltas del ciclo

| Vuelta | Qué se miró | Qué salió |
|---|---|---|
| A | La hoja de contacto de Trazo; la carta nueva en Asuán y en el delta; 16 estados auditados en tres tamaños | 2 hallazgos medios y 7 menores; el obelisco parecía una flauta e Hipo una rana (corregidos en la misma vuelta) |
| B | Recorridos en los dos modos; hoja de contacto de los 16 estados a 390, 360 y 1440 | Ningún grave; 4 medios y 11 menores. Corregidos: el anillo tapado por el encabezado en teléfonos chicos, el contraste de los rótulos de la carta, Hipo que preguntaba antes de zarpar, el perfil con letra chica |
| C | Capturas de cada retoque | La «N» con contraste, Hipo separado del nombre de la parada, la escala fija, el mapa mínimo en teléfonos chicos |
| Final | Recorridos, auditoría en cuatro tamaños, mediciones, comparación de antes y después | Ver «Mediciones» y `hallazgos.md` |

## Cada pieza, después de la corrida larga

| # | Pieza | Estado | Qué cambió |
|---|---|---|---|
| 1 | La carta | Terminada | Costas, lagos y fronteras de la región con detalle (en lugar del mapa del mundo), halo de costa, un segundo relieve fino para las vistas cercanas, escala gráfica y norte, el delta rotulado. El curso es ahora el de Natural Earth 10 m (635 vértices, con cinco afluentes), sin que cambie ninguna cifra |
| 2 | El hilo de oro y las paradas | Terminada | El anillo de la próxima parada ya no queda bajo el encabezado en ningún tamaño; los rótulos dan 4,5 a 1 o más |
| 3 | La bitácora | Terminada | Sello circular propio (pictograma, nombre y latitud, sin letra de menos de 11 px); el riel de etapas en la portada y en el mar del teléfono; el mapa conserva un mínimo visible; todos los estados mirados (guía fallada, sello pendiente, bodega llena, barca anclada, Adulto) |
| 4 | La falúa e Hipo | Terminada, con una reserva | La falúa de perfil con vela latina dorada y hasta tres cargas a la vista; Hipo nada a popa, con cinco ánimos. Reserva: son dibujos de línea hechos a mano, chicos; se leen, pero conviene que los mirés vos (el rollo de lino es el más flojo) |
| 5 | Portada y llegada | Terminadas | En pantalla ancha la portada lleva «Tu embarcación» y «Conocé a Hipo» |
| 6-8 | Acróstico, imágenes, perfil | Terminadas | El perfil, con rótulos de 12 px que la línea ya no tacha |
| 9 | Sonido | Terminada sin oír | Sin cambios; vuelto a medir |

Sigue fuera de alcance: Ordenar, Recitar y Preguntar (heredan papel y tipografía). No se embebieron fuentes (pide descarga).

## Mediciones

Las cifras de la verificación final están en `capturas/medicion.json` y al final de `hallazgos.md`.

- **Cifras fijas:** kilómetros 0, 1 006, 3 014, 5 297, 5 566 y 6 394 y alturas 1 149, 457, 373, 106, 75 y 21 m, iguales a los de
  Cauces, con el cauce fino puesto.
- **Movimiento** (CPU frenada 4×, verificación final): 55,6 cuadros por segundo de mediana (pedido: 50 o más), cuadro más largo
  de 18,7 ms (pedido: ninguno de más de 100), la barca a 0,09 px del curso como máximo.
- **Auditoría** (16 estados, en 390 × 844, 360 × 640, 844 × 390 y 1440 × 900): letra más chica, 11 px; ningún toque de menos de
  44 px; ningún contraste de menos de 4,5 a 1 en la bitácora; la página nunca se ensancha; ningún nombre de parada futura; ningún
  emoji; ningún rótulo de la carta tapado. En la carta, un solo rótulo queda por debajo de 4,5 a 1: ECUADOR, a 1440 px (3,48).
- **Recorridos** con clics reales: 27 pantallas por modo, unos 41 segundos, los dos al mar sin errores de consola.
- **Hallazgos al cierre** (`hallazgos.md`): ningún grave. Dos medios, los dos del motor de Cauces y sin tocar (la nota del evento
  con el orden entero y la barca dibujada en la boca del río). Trece menores: siete a la vista (entre ellos, «1 monedas», la falúa
  chica en pantalla ancha y «Jinja» recortado 9 px en teléfonos de 360 px durante un evento) y seis que la verificación final no
  volvió a mirar, aunque sus dueños los dieron por corregidos.
- **Sonido:** seis efectos, sin muestras inválidas, todos por debajo de −3 dBFS (el más alto, el mar, −7,9).
- **Peso:** `dist/nilo.html`, 617 KB (era 647): el mapa de la región pesa menos que el del mundo que reemplaza. Los dos relieves
  suman 71 KB (tope 150).

## Lo que conviene que mirés vos

- **Los dos dibujos nuevos** (la falúa con su carga e Hipo nadando): en `capturas/despues-390-3-parada-4.png` se ven en Asuán.
- **Un texto nuevo dicho por Hipo:** «Mirá la frase: así van las paradas, en orden.», antes de zarpar en la primera bajada. Está
  en `textos-nuevos.md`, con los rótulos nuevos de la carta.
- **Tres cosas que son del motor de Cauces, no de la vitrina, y que no toqué:** el mercado dice «1 monedas»; al resolver un evento
  de frase, la nota muestra el orden entero, con paradas que todavía no se alcanzaron; y al llegar al mar la barca se dibuja en la
  boca del río mientras el texto dice que la falúa no sale al mar.
- **Las fuentes de los datos nuevos** quedaron al final de `docs/verificacion.md`; el mosaico de elevación fino es el mismo que ya
  usa el perfil de altura, pero no revisé sus términos de uso en esta corrida.

## Lo que no pude verificar

Igual que en la corrida de 60 minutos: nadie oyó el sonido, ningún jugador lo tocó y todo se vio en el Edge de escritorio emulando
teléfonos, no en un iPhone. Las tres pruebas con un jugador de verdad que propuse entonces siguen en pie (las dos pantallas por
parada, el sonido con el teléfono en la mano, la carta a la luz del día); sumo una: **¿se entiende la barca?** Preguntale a un niño
qué lleva la falúa en Asuán y quién nada al lado.

## Propuesta para lo que sigue, por impacto

1. **Probarlo con tus hijos en el iPhone** antes de invertir más: es lo único que falta para saber si este nivel sirve.
2. **Fuentes embebidas en subconjunto** (hay que bajarlas): sin red, la carta pierde su tipografía.
3. **Vestir Ordenar, Recitar y Preguntar** con la misma hoja: hoy, al salir de Bajar, se vuelve al diseño de siempre.
4. **Decidir si esta capa pasa a los demás ríos.** Por río cuesta: unos 170 KB de carta (costas de la región, cauce fino y dos
   relieves), los rótulos puestos a mano y la barca dibujada. La bitácora, el sonido y las pruebas ya sirven para todos.
5. **Achicar las capturas versionadas** (unos 9 MB de PNG, más 3,7 MB de las referencias) antes de mezclar la rama.

## Qué queda y dónde

- Rama `vitrina-nilo`, en `C:\Users\humbe\proyectos\geo\cauces-vitrina`, sin push y sin mezclar. Para verla: `dist/nilo.html`.
- `docs/vitrina/`: `plan-larga.md`, `contrato.md` (con la sección de la corrida larga), `diario.md`, `hallazgos.md`,
  `textos-nuevos.md`, `capturas/` (con `comparacion-390.png`: antes, 60 minutos y corrida larga) y este informe.
- En `cauces-proyecto` sigue sin commit el trabajo de la voz; no se tocó.
