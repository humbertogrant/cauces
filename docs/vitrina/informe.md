# Informe de la corrida: vitrina del Nilo

Corrida autónoma del 2026-11-11, de 07:31 a 08:22 (51 de los 60 minutos del presupuesto), según `instruccion-un-rio.md`.

1. `dist/nilo.html` (647 KB; el tope era 900) baja el Nilo entero en Niño y en Adulto con clics reales y sin errores de consola:
   carta de noche con relieve sombreado real y un solo hilo de oro, bitácora en papel con las fichas del acróstico, portada,
   pruebas entre puertos y llegada al mar, y seis efectos de sonido sintetizados.
2. Cauces y Exploradores no cambiaron: sus cuatro HTML salen byte a byte iguales y `npm test` pasa 9 de 9 (los 8 de siempre más
   «VITRINA OK»).
3. Hubo tres vueltas del ciclo de mirar y corregir, con cuatro subagentes. Los hallazgos graves están corregidos; lo que queda es
   menor y está en `hallazgos.md`.
4. La corrida se apartó de la instrucción en cuatro cosas, todas anotadas en `diario.md`: usó lo ya pintado (Hipo, la falúa, las
   mercancías, las postales) en lugar de dibujar en línea; respetó «enseñar antes de preguntar»; dejó el curso de Natural Earth
   50 m; y no embebió fuentes.
5. Nadie oyó el sonido ni lo jugó en un teléfono de verdad: está medido, no probado con un jugador.

## Tiempo y consumo

| Tramo | Plan de la instrucción | Lo que pasó |
|---|---|---|
| Leer y planear | 10 % (6 min) | 07:31 – 07:47, 16 min (27 %): el repositorio había cambiado mucho desde setiembre y hubo que reconciliar la instrucción con él |
| Construir | 55 % (33 min) | 07:47 – 08:04, unos 17 min (28 %), en paralelo: ganchos y build (Dirección) y cuatro subagentes |
| Mirar y corregir | 25 % (15 min) | 07:56 – 08:20, unos 24 min, solapado con el final de la construcción y con el informe |
| Informe | 10 % (6 min) | 08:12 – 08:22, a ratos, mientras corría la vuelta final de verificación |

Sobraron unos 9 minutos del presupuesto: cerré ahí en vez de abrir otra vuelta que no iba a alcanzar a verificar.

- **Subagentes:** Verificación ≈ 441 mil tokens, Carta ≈ 357 mil, Bitácora ≈ 347 mil y Sonido ≈ 264 mil: unos 1,41 millones
  entre los cuatro.
- **Dirección:** la sesión cerró con ≈ 675 mil tokens en su ventana (incluye lo que la conversación ya traía antes de la corrida).
- **Plan:** al cierre el plan marca 22 % del límite semanal (24 % en el modelo de la corrida). No tomé la lectura al empezar, así
  que no sé cuánto de eso es de esta hora. El entorno no muestra el costo en dinero.

## Vueltas del ciclo

| Vuelta | Hora | Qué se miró | Qué salió |
|---|---|---|---|
| 0 | 07:54 | El «antes»: el Nilo de `dist/cauces.html` en cuatro momentos | Punto de partida, en `capturas/antes-*.png` |
| 1 | 07:56 | Primer recorrido completo de la vitrina (27 capturas) | 9 hallazgos (3 graves): dorado en un afluente, datos de la portada cortados, anillo de la próxima parada tapado; y que los eventos volvían al diseño viejo |
| 2 | 08:04 | Segundo recorrido, y uno en Adulto | Corregido lo anterior. Un grave nuevo: tras un evento la página se ensanchaba (el sello nuevo se salía 72 px). Corregido y vuelto a medir a las 08:10 |
| Final | 08:11 – 08:15 | Recorridos en los dos modos (54 pantallas), doce capturas de después en tres tamaños, mediciones | Los graves, confirmados corregidos; 8 hallazgos menores nuevos |

**Hallazgos** (`hallazgos.md` tiene cada uno con su captura): 25 en total. Al cerrar ese documento, a las 08:15, había 12
corregidos (los 4 graves y los 7 medios, más uno menor), uno cerrado por ser a propósito (en la portada el río va entero en
dorado) y 12 menores. Un último retoque de tres minutos, de 08:16 a 08:18, corrigió tres de esos menores (el rótulo repetido en
pantalla ancha, el rótulo que asomaba bajo el botón de volver y el «‹ Atrás» con dos formas) y achicó el papel en blanco de la
portada del teléfono; lo comprobé con capturas, pero `hallazgos.md` no lo recoge. **Quedan 9 menores.** Los que conviene que
mirés: en el teléfono el riel Bajar · Ordenar · Recitar · Preguntar no se ve durante la bajada (se llega a Ordenar desde el mar);
a 1440 px la hoja de la portada queda casi vacía; y, en Adulto, la carga de Juba nombra a Jartum (es un texto de los datos de
siempre: «…el comercio que hizo rica a Jartum…»).

## Cada pieza de la lista de prioridad

| # | Pieza | Estado | Detalle |
|---|---|---|---|
| 1 | La carta | Terminada, con dos reservas | Relieve sombreado real de ETOPO1 dentro del mismo SVG, recortado por la tierra; lagos, fronteras punteadas, retícula, ecuador y trópico; rótulos con jerarquía de atlas que no pisan el cauce; cinco encuadres (río entero, tramo, parada, delta y evento). Reservas: de cerca (parada, delta) el relieve se ve en manchas suaves, porque el ráster es de baja resolución; y el curso sigue siendo el de Natural Earth 50 m, que ya era real: el de 10 m no se tocó |
| 2 | El hilo de oro y las paradas | Terminada | Lo recorrido en dorado con resplandor, lo que falta en crema, los afluentes finos en verde claro; paradas visitadas con punto y nombre; la próxima, anillo punteado con signo de pregunta; las demás, sin nombre. Una prueba vigila que la carta no nombre paradas futuras |
| 3 | La bitácora | Terminada, con una reserva | Hoja de papel sobre el mapa fijo, rótulo, ciudad, país y distancia, globo de Hipo, tarjeta de la imagen, dato, bodega y mercado, botón de zarpar. Reserva: el sello es el del motor (su forma cambia por parada y lleva letras de 8 px), no uno circular propio |
| 4 | La falúa e Hipo | A medias | Hipo pintado con sus cinco ánimos en el globo, y las mercancías pintadas, ya existían y se usan; en la vitrina no queda ningún emoji (lo prueba el test). No se hizo: la barca con la carga a la vista (el obelisco de Asuán) ni Hipo nadando al lado: en la carta siguen el glifo de la falúa, con la vela dorada, e Hipo encima |
| 5 | Portada y llegada al mar | Terminadas | Portada con el río entero en dorado, el nombre, la distancia, la cita de Heródoto y el saludo de Hipo; llegada con el delta, el texto de la falúa y las cuentas del viaje |
| 6 | El acróstico como progreso | Terminada | Seis fichas que se llenan con cada parada y la frase que se completa; en el mar, la frase entera es el título |
| 7 | Imágenes para recordar | Terminada con lo que había | Las ocho postales pintadas del Nilo (octubre); `encargos-ilustracion.md` las deja descritas |
| 8 | Perfil del río | Terminada | El perfil del motor (datos reales, nunca sube), dentro de la hoja, en «navegando» |
| 9 | Sonido | Terminada sin oír | Viento, puerto, moneda, sello, mar y acierto, sobre el agua del motor; arranca tras el primer toque, recuerda el silencio y pasa por un compresor. Medido, no escuchado |
| — | Pantallas de 820 px o más | Terminada | La carta a la izquierda y la bitácora en columna a la derecha |

Fuera de alcance, como pedía la instrucción: Ordenar, Recitar y Preguntar heredan papel, tipografía y colores, y nada más.

## Mediciones

Sobre el build final, con el Edge del sistema emulando 390 × 844 (`capturas/medicion.json`):

- **Movimiento**, con la CPU frenada 4×, tramo Jinja → Juba: 59,9 cuadros por segundo de mediana y cuadro más largo de 16,9 ms
  (pedido: 50 o más, y ninguno de más de 100 ms). La barca va a 0,12 px del curso como máximo, en 85 cuadros, y a menos de 0,1 px
  en cinco capturas de otro viaje.
- **Sonido**, cada efecto renderizado con `OfflineAudioContext` (no se oyó): ninguna muestra inválida y todos por debajo de
  −3 dBFS.

  | Efecto | Duración | Pico | Pico a la salida |
  |---|---|---|---|
  | viento | 5,2 s | −9,4 dBFS | −12,5 dBFS |
  | puerto | 1,1 s | −9,8 dBFS | −13,7 dBFS |
  | moneda | 0,3 s | −9,0 dBFS | −11,2 dBFS |
  | sello | 0,36 s | −8,5 dBFS | −12,3 dBFS |
  | mar | 6,4 s | −7,9 dBFS | −11,5 dBFS |
  | acierto | 0,18 s | −13,8 dBFS | −17,0 dBFS |

- **Peso:** `dist/nilo.html`, 647 KB (tope 900); el relieve embebido, 95 KB (tope 150). `dist/cauces.html` sigue en 459 KB y los
  otros tres, igual que antes, byte a byte.
- **Cauces, sin cambios de comportamiento:** los cuatro HTML de siempre son byte a byte los de antes de la corrida (git no los ve
  cambiados), así que juegan igual por construcción; además, el recorrido del «antes» sobre `dist/cauces.html` (Niño, 20
  pantallas) llegó al mar sin errores, y la instantánea de 200 pantallas sigue igual.
- **Recorrido automático** con clics reales (Edge del sistema): 27 pantallas por modo, unos 45 segundos cada uno, los dos llegan
  al mar sin errores de consola, sin botones tapados y con la página en 390 px de ancho en las 54 pantallas.
- **Pruebas:** `npm test` pasa 9 de 9. `test/vitrina.js` comprueba en los dos modos que los ganchos salen en orden, que las fichas
  del acróstico corresponden a las paradas alcanzadas, que la carta no nombra paradas futuras, que en el panel solo aparecen como
  fichas de la guía (o en la lista de la primera bajada, o dentro de textos de los datos), que no hay emojis y que el archivo pesa
  menos de 900 KB.

## Lo que no pude verificar

- **Cómo suena.** Cada efecto cumple duración, pico y validez, pero nadie lo oyó: no sé si el viento cansa, si la moneda suena a
  moneda ni si algo suena a máquina.
- **Cómo lo juega un niño.** Ningún jugador lo tocó.
- **Un teléfono de verdad.** Todo se vio en el Edge de escritorio emulando 390 × 844: no en Safari ni con el dedo.
- **Las fuentes sin red.** No se embebieron: sin conexión, Oswald y Source Sans 3 caen a las del sistema y la carta pierde parte
  de su carácter.
- **Coordenadas de los cuatro hitos** (Abu Simbel, Meroe, Guiza, Alejandría): puestas de memoria; están marcadas en
  `docs/verificacion.md`.

Tres cosas concretas para probar con un jugador de verdad:

1. **Las dos pantallas por parada.** Dale el teléfono a un niño sin explicarle nada: ¿entiende que ZARPAR lleva a la pregunta y
   no al viaje? ¿Mira las fichas del acróstico para responder, o las ignora?
2. **El sonido, con el teléfono en la mano.** Bajá el río entero con sonido: ¿el viento molesta en los tramos largos? ¿Se
   distinguen la moneda, el sello y el golpe de acierto? Después apagalo, cerrá y volvé: tiene que seguir apagado.
3. **La carta a la luz del día, en iPhone.** ¿Se leen los rótulos en crema sobre verde? ¿El dedo sobre el mapa desplaza la hoja?
   ¿La barra de Safari tapa el botón?

## Propuesta para la siguiente hora, por impacto

1. **La falúa con la carga a la vista e Hipo nadando al lado** (lo que faltó de la pieza 4): es lo que más se aleja de la
   referencia y lo que más quiere un niño.
2. **Relieve fino de cerca y curso de 10 m**: los modelos de elevación finos del Nilo ya están en caché; con dos niveles de
   relieve, la parada y el delta dejan de verse en manchas.
3. **Vestir Ordenar, Recitar y Preguntar** con la misma hoja: hoy, al salir de Bajar, la vitrina vuelve al diseño de siempre.
4. **Sello propio de la bitácora**, circular y sin letras de menos de 11 px.
5. **Fuentes embebidas en subconjunto**, para que se vea igual sin red (pide bajar las fuentes).
6. **Una tarde en el iPhone** con lo anterior, y decidir si esta capa pasa a los demás ríos: por río cuesta unos 95 KB de relieve
   y sus rótulos puestos a mano.

## Qué queda y dónde

- Rama `vitrina-nilo`, en `C:\Users\humbe\proyectos\geo\cauces-vitrina`, sin push y sin mezclar. Para verla: abrir
  `dist/nilo.html`.
- En `cauces-proyecto` sigue sin commit el trabajo de la voz; no se tocó. Los ganchos de la vitrina quedaron lejos de sus líneas
  para que la mezcla salga sola.
- `docs/vitrina/`: `plan.md`, `contrato.md`, `diario.md`, `hallazgos.md`, `textos-nuevos.md`, `encargos-ilustracion.md`,
  `capturas/` y este informe.
