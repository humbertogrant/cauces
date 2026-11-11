# Diario de la corrida (2026-11-11)

Horas de reloj de la máquina. Lo decidido sin consultar va marcado **Decisión**.

- **07:31** Arranque. Humberto adjuntó `instruccion-un-rio.md` y `referencia-nilo.zip` y pidió «mirá esto y arrancá con la
  propuesta». **Decisión:** lo tomo como la orden de correr la instrucción con el presupuesto por defecto (60 minutos) y lo digo
  al empezar, para que pueda frenarme si solo quería una propuesta escrita.
- **07:32-07:39** Leídas la instrucción, las cuatro imágenes de referencia, la memoria del proyecto y `CLAUDE.md` entero. El
  repositorio cambió mucho desde setiembre (ver la tabla de `plan.md`).
- **07:36** En `cauces-proyecto` hay trabajo sin commit (la elección de la voz, del 2026-10-29) y otra sesión abierta sobre esa
  carpeta. **Decisión:** rama `vitrina-nilo` en un árbol de trabajo aparte (`proyectos/geo/cauces-vitrina`), desde `0c4e965`; no
  toco el árbol principal ni su trabajo pendiente.
- **07:39** Base verificada en la rama nueva: `npm test` pasa (TODO OK × 3, INSTANTÁNEA OK, DIST OK × 4).
- **07:40** **Decisión (arte):** uso lo pintado que ya existe (Hipo y sus cinco ánimos, la falúa, las cinco mercancías, las ocho
  postales del Nilo) en lugar de redibujar en línea plana. Razones: tres rondas de dibujo vectorial por coordenadas se descartaron
  en setiembre; lo pintado es lo que Humberto aprobó y la propia instrucción lo deja previsto («por si después quiero producirlas
  pintadas»). El rol «Trazo» queda sin subagente. Consecuencia: en la bitácora hay dorado dentro de las postales (su
  protagonista); la regla «el dorado no entra en la bitácora» se aplica a la interfaz, no a las imágenes.
- **07:40** **Decisión (memoria):** la instrucción pide que nunca se vea el nombre de una parada futura; el lote 1 del 2026-10-29
  («enseñar antes de preguntar») muestra la frase con la lista en la primera bajada, antes de zarpar. Se respeta el lote 1, que es
  posterior y salió de una revisión con cinco lectores; en todo lo demás, ningún nombre futuro.
- **07:41** **Decisión (datos):** sin descargas. ETOPO1 (NOAA, dominio público) y Natural Earth ya están en `tools/ne` del árbol
  principal; copié al árbol nuevo lo que hace falta (la carpeta está fuera de git). Las capturas van con el Edge o el Chrome del
  sistema por CDP, sin Playwright. No embebo fuentes: `dist/nilo.html` corre sin red con las del sistema, como el juego de hoy.
- **07:41** **Decisión (curso):** el curso del Nilo se queda como está (Natural Earth 50 m, con vértice por parada). Pasarlo al de
  10 m mueve los índices de parada, el perfil y los eventos; queda de pendiente.
- **07:44** `contrato.md`: ganchos, fases y dueños. **Decisión (flujo):** la parada se parte en dos pantallas sin tocar la mecánica:
  lo que hay en la parada (con ZARPAR) y la guía («navegando»: fichas del acróstico, pregunta de Hipo, perfil). La guía, el sello y
  el mercado siguen siendo los del motor.
- **07:47** Lanzados cuatro subagentes en paralelo: Carta, Bitácora, Sonido y Verificación, cada uno con el contrato, la frase de
  arte, su lista de archivos y la prohibición de tocar lo ajeno.
- **07:49** Ganchos en `src/motor.js` (14 puntos, todos entre `/*@vitrina*/ … /*@fin:vitrina*/`) y juego `nilo` en `build.js`.
  `node build.js` genera `dist/nilo.html` (493 KB antes de la carta) y deja `dist/cauces*.html` y `dist/exploradores*.html` byte a
  byte iguales (git no los ve cambiados). **Decisión:** la vitrina guarda aparte (`cauces-nilo`) y abre directo en su río.
- **07:50** Humo en el DOM simulado: solo el Nilo, los dos modos llegan al mar, los eventos salen en orden (zarpar → sello →
  parada … → mar).
- **07:53-07:56** La otra sesión (la del trabajo de la voz, sin commit en `cauces-proyecto`) avisó que cambia la línea de `init` y la
  última de `renderInicio`. **Decisión:** el gancho de arranque va al final de `motor.js` y el de `renderDescender`, una línea más
  abajo: así los dos cambios no quedan pegados y la mezcla futura sale sola.
- **07:56** Primer recorrido completo de `dist/nilo.html` (639 KB) con clics reales en el Edge del sistema: 27 capturas, llegó al
  mar, sin errores de consola. Vuelta 1 de mirar: la portada, navegando en Jartum, Asuán y el mar ya se parecen a la referencia.
  Lo más grave: un afluente con resplandor dorado, los tres datos de la portada cortados por el pie y el anillo de la próxima
  parada tapado por el encabezado. Lista completa en `hallazgos.md`; cada arreglo fue a su dueño.
- **07:57** Gancho nuevo, `dibujado`, al final de `render()`: la bitácora lo usa para acortar el subtítulo del encabezado.
- **07:58** Verificación entregó la vuelta 0: `tools/captura.js` (foto, recorrido, medir), el «antes» y `test/vitrina.js`. La prueba
  falla en Adulto: en Juba, la carga narrativa del juego nombra a Jartum («…el comercio que hizo rica a Jartum…»). **Decisión:**
  ese texto es de los datos de Cauces de siempre y la corrida no toca datos; la regla «ningún nombre futuro» se prueba sobre lo
  que agrega la vitrina, y el caso queda anotado para Humberto.
- **07:58** Sonido entregó: cinco efectos sintetizados, con pico entre −7,9 y −9,8 dBFS, medidos con `OfflineAudioContext` (nadie
  los oyó). **Decisión:** acertar la guía no puede sonar a moneda (en Adulto no hay monedas): pedí un golpe de madera corto para
  los aciertos. El primer toque se escucha ahora en `pointerup`, `click` o `keydown`.
- **07:59** Bitácora entregó la vuelta 1. **Decisiones:** el sello dorado del motor (tinta ocre) se queda en la bitácora; la
  pregunta de la guía va una sola vez (en el globo); el texto de zarpe y el rival, que la portada nueva dejó fuera, vuelven en
  «navegando» antes de la primera parada.
- **08:00** Mirando las pantallas de evento: en mitad de la bajada la prueba entre puertos volvía de golpe al diseño viejo del
  motor. **Decisión:** `CAPA.momento()` devuelve `evento` y la bitácora lo trata como una parada: el panel del motor dentro de la
  misma hoja. No es mecánica nueva; es no dejar una pantalla a medias en el recorrido de Bajar.
- **08:01** Tres roles reconstruyendo a la vez chocaron al escribir `dist/` (un error de Windows al abrir `cauces-amplia.html`).
  `node build.js nilo` arma solo la vitrina.
- **08:03** `test/vitrina.js` pasa en los dos modos y entra en `npm test`: 9 de 9 (TODO OK × 3, INSTANTÁNEA OK, DIST OK × 4,
  VITRINA OK). Medición con la CPU frenada 4×: 59,9 cuadros por segundo de mediana, cuadro más largo de 50 ms, la barca a 0,13 px
  del curso.
- **08:04** Vuelta 2 de mirar (segundo recorrido completo, 27 capturas): entraron los arreglos de Carta y Bitácora (el dorado
  solo en el cauce, la portada con el río entero en dorado y a la derecha del título, el anillo de la próxima parada a la vista,
  la píldora con el kilómetro, la pregunta una sola vez, el perfil entero, los eventos dentro de la hoja). Quedaban dos retoques
  de la portada (el rótulo del trópico detrás del título y la barca cortada por la hoja): hechos a las 08:07.
- **08:06** **Decisión:** las carpetas de recorridos completos (unas 27 capturas cada una) no se versionan; sí los cuatro momentos
  de antes y los de después en tres tamaños, sueltos en `docs/vitrina/capturas/`. `tools/verificacion.py` agrega al final de
  `docs/verificacion.md` la fuente del relieve y los rótulos de la carta, marcados para revisión.
- **08:06** **Decisión (Carta, confirmada):** «Pirámides de Guiza» solo aparece en la carta cuando El Cairo ya se alcanzó: al lado
  del anillo de la próxima parada, la delataba.
- **08:08** Hallazgo grave de Verificación: al llegar a una parada después de un evento, el encabezado desaparecía y ZARPAR salía
  cortado. Lo reproduje y medí: la página pasaba de 390 a 462 px de ancho. Causa: el sello nuevo del motor cae con una animación
  que empieza agrandada 2,4 veces y girada; en la bitácora va pegado al borde derecho y se salía 72 px, y el teléfono agrandaba
  la página entera. Arreglo en `capa.css` (es de Dirección): la página no puede ensancharse y el sello entra con una animación
  corta. Medido otra vez: 390 px y el botón de 294.
- **08:10** Vuelta final de Verificación en marcha: recorridos en los dos modos, las doce capturas de antes y después (390 × 844,
  820 × 1180 y 1440 × 900) y las mediciones sobre el build final.
- **08:13** Build completo y `npm test` sobre el estado final: 9 de 9; los cuatro HTML de Cauces y Exploradores, sin cambios.
  Miré yo las dos pantallas que faltaban: el mercado de Juba con la bodega y las cuentas del viaje en el mar. Bien las dos.
- **08:15** Verificación cerró: dos recorridos de 27 pantallas (mercader e historia), los dos al mar, sin errores de consola y con
  la página en 390 px en las 54 pantallas; 59,9 cuadros por segundo con la CPU frenada 4×, cuadro más largo de 16,9 ms, la barca a
  0,12 px del curso; seis efectos de sonido sin muestras inválidas. Hallazgos: ningún grave ni medio pendiente; quedan 12 menores.
- **08:16** Sobraban unos minutos. **Decisión:** en vez de agregar algo, un último retoque de tres minutos sobre la pantalla más
  débil, la portada: el papel en blanco bajo los tres datos (Bitácora) y, en pantalla ancha, un rótulo repetido y otro bajo el
  botón de volver (Carta). Si no entra limpio, se descarta.
- **08:18** El retoque entró limpio: la portada del teléfono con el mapa a 67svh (menos papel en blanco), «‹ Atrás» igual en todas
  las pantallas, «EGIPTO» y «SUDÁN» una vez cada uno en pantalla ancha y las esquinas de los botones libres de rótulos. Lo miré en
  capturas a 390 × 844, 820 × 1180 y 1440 × 900.
- **08:19** Build completo y `npm test` sobre el estado final: 9 de 9. `dist/nilo.html`, 647 KB. Los otros cuatro HTML, sin cambios.
- **08:20** Retomé las nueve capturas de «después» que cambiaron con el retoque (portada, navegando y mar, en los tres tamaños),
  para que las versionadas sean las del build final. `hallazgos.md` se cerró a las 08:15 y no recoge el retoque: el informe lo dice.
- **08:21** Cierre, con unos 9 minutos del presupuesto sin usar: informe escrito, todo con commit en `vitrina-nilo`, sin push.
  Quedan 9 hallazgos menores y la pieza 4 (la falúa con la carga a la vista e Hipo nadando al lado) a medias. **Decisión:** no abrir
  otra vuelta de arreglos que no se alcanzaría a verificar.

## Corrida larga (2026-11-11, 08:27 → 11:27)

- **08:26** Humberto: «vamos con la corrida larga», sin número. **Decisión:** 180 minutos, de 08:27 a 11:27; se lo dije al empezar,
  con lo que pienso hacer, para que pueda cambiar el presupuesto. Mismo alcance y mismas reglas; plan en `plan-larga.md`. El plan
  de consumo marca 24 % del límite semanal al arrancar (27 % en el modelo de la corrida).
- **08:29** Contrato ampliado (sección «Corrida larga»): rol nuevo, Trazo (`src/vitrina/arte.*`: la falúa con la carga a la vista e
  Hipo nadando), y los datos que la carta puede entregar: cauce fino, costas y lagos de la región, segundo relieve.
  **Decisión (arte):** estos dos dibujos sí van en SVG plano, a mano: son piezas chicas del mapa, del tamaño de los glifos que
  Humberto aprobó en setiembre, no ilustraciones; se miran a tamaño real en una hoja de contacto antes de darlos por buenos.
- **08:30** Lanzada la vuelta A: Trazo (nuevo), Carta, Bitácora y Verificación, hasta las 09:15-09:20.
- **08:32** **Decisión (cifras):** el cauce fino no puede mover ningún número del juego. `cauceFino` en `src/juegos/nilo.js` deja
  fijos los kilómetros de cada parada (calculados con el curso de Cauces) y pasa el perfil de altura al cauce nuevo por tramos.
  Probado con un curso torcido a propósito: kilómetros y alturas de las seis paradas, idénticos. El build aprende `arte.js`,
  `arte.css` y `mapa-carta.js` (si la carta trae sus costas, el mapa del mundo no viaja).
- **08:49** Primera mirada a la hoja de contacto de Trazo: la falúa se lee; pedí tres retoques (el obelisco parecía una flauta, Hipo
  nadando una rana, el saco de café una botella).
- **08:56** Carta entregó la vuelta A antes de tiempo: cauce fino de Natural Earth 10 m (635 vértices, cinco afluentes), costas,
  lagos y fronteras de la región (77 KB, en lugar del mapa del mundo), halo de costa, un segundo relieve fino del corredor para las
  vistas cercanas, y la falúa e Hipo de Trazo colocados. `dist/nilo.html` bajó a 609 KB. **Decisiones de Carta, aprobadas:** la
  falúa va siempre derecha y mira según el rumbo del tramo (girada con el río, un perfil de 52 px quedaba de punta); Guiza solo
  sale cuando El Cairo ya se alcanzó. Le pedí una segunda pasada: escala gráfica y norte, rótulos del delta y un renglón bajo
  Asuán («primera catarata») y El Cairo («puerto de Bulaq»), que están en los datos del juego.
- **09:00** Verificación entregó: `auditar` (16 estados: letra de menos de 11 px, toques de menos de 44 px, contraste, ancho de
  página, nombres futuros, emojis), `estados` (una captura por estado, en tres tamaños) y la prueba de cifras fijas contra
  `dist/cauces-amplia.html`. Auditoría: ningún toque chico, ningún contraste bajo en la bitácora, página nunca ancha; letra más
  chica, 10,2 px (rótulos del perfil). Hallazgos nuevos: 2 medios y 7 menores.
- **09:01** Trazo entregó: la falúa con hasta tres cargas a la vista (el obelisco, acostado en la cubierta, se ve), ocho cargas y la
  cabeza de Hipo asomada del agua en cinco ánimos. Mirado dentro del juego en Asuán: se lee. El gancho del encuadre ahora recibe
  las medidas del mapa.
- **09:02** El consumo va más rápido de lo supuesto: el límite semanal del modelo pasó de 27 % a 42 % en 35 minutos. **Decisión:**
  tope de 75 % para esta corrida, avisado a Humberto; si se alcanza antes de las 11:27, se cierra ahí con commits e informe. Para
  gastar menos: agentes nuevos de contexto chico para las vueltas que siguen, menos llamadas de Dirección y revisión en hojas de
  contacto.
- **09:03** **Decisiones sobre los hallazgos de la vuelta A:** antes de zarpar en la primera bajada Hipo no puede preguntar por la
  próxima parada con la lista a la vista: dirá un texto nuevo y corto que explica la frase (va a `textos-nuevos.md`); los rótulos
  secundarios de la carta suben a 4,5 a 1 de contraste aunque la instrucción los pedía al 60 % (se lee o no se lee); «1 monedas»
  en el mercado es un texto del motor de Cauces y no se toca aquí: queda avisado.
- **09:07-09:10** Carta cerró la segunda pasada (escala gráfica y norte, el delta rotulado, «primera catarata» y «puerto de Bulaq»
  bajo sus paradas, el relieve fino sin franja visible) y Bitácora la vuelta A (riel en la portada y el mar del teléfono, sello
  circular propio con la latitud, el alto del mapa medido, portada ancha con «Tu embarcación» y «Conocé a Hipo»). **Decisiones de
  Bitácora, aprobadas:** «‹ Atrás» en la guía vuelve a la hoja de la parada (antes se llevaba la barca a la parada anterior); el
  rótulo dice «Parada 4 de 6» y el kilómetro queda en la píldora.
- **09:11** Vuelta A integrada: `npm test` 9 de 9, `dist/nilo.html` 610 KB, commit fe8391d.
- **09:14** Vuelta B con tres agentes nuevos de contexto chico (los de la vuelta A cargaban entre 380 y 680 mil tokens y cada
  llamada suya salía cara): uno verifica y arma hojas de contacto; dos aplican los arreglos decididos. **Decisión de orden:** cada
  uno arma su propia copia del juego con `ensamblar('nilo','amplia')`, sin tocar `dist/`, para no pisar las capturas del que mira.
- **09:20** Verificación B, sobre el build de la vuelta A: los dos recorridos al mar sin errores; auditoría sin letra de menos de
  11 px, sin toques chicos y sin contrastes bajos en la bitácora; ningún hallazgo grave, 4 medios y 11 menores. Miré la hoja de
  contacto de los 16 estados a 390 × 844: el conjunto ya se lee como un solo producto. **Decisiones:** la nota del evento que
  muestra el orden entero (B-01) y la falúa dibujada en la boca del río mientras el texto dice que no sale al mar (B-04) son del
  motor de Cauces y se quedan; van anotadas para Humberto junto con «1 monedas».
- **09:21** Vuelta B integrada: Hipo ya no pregunta antes de zarpar (dice el texto nuevo, que va a `textos-nuevos.md`), el perfil
  con rótulos de 12 px que la línea no tacha, el sello de Jinja con «0° 25′ N», Hipo despierto si habla en el mar; la carta
  reserva los 84 px reales de la píldora, todos sus rótulos dan 4,5 a 1 o más (salvo la «N» sobre relieve claro en algunas
  paradas, pendiente) y ninguno baja de 11 px. `npm test` 9 de 9; `dist/nilo.html`, 614 KB.
- **09:24** Vuelta C con dos agentes nuevos. **09:27-09:31** entregaron. Bitácora: en `navega` el mapa conserva un mínimo visible
  (los 84 px de la píldora más 210 de río) y lo que no cabe se ve desplazando la hoja; con cero paradas, la cabecera de las fichas
  lleva el rótulo del motor «Frase para el orden»; en pantalla ancha, navegando, el papel vacío lo ocupa la imagen para recordar de
  la última parada alcanzada (**decisión de Bitácora, aprobada:** no adelanta la siguiente); movimiento reducido y nombres
  accesibles, revisados sin cambios. Carta: la «N» del norte con un disco oscuro detrás (contraste de 3,6 a 8,98); el nombre de la
  parada, separado de Hipo; la escala gráfica, siempre abajo a la izquierda salvo que ahí pase el río o la barca; «Nilo Azul», fuera
  del trazo del afluente; en pantalla ancha, la falúa e Hipo a 1,4 veces; «LAGO VICTORIA» vuelve a la portada, sobre el lago.
- **09:31** Consumo a media corrida: el límite semanal del modelo, en 45 % (había subido 15 puntos en los primeros 35 minutos y
  solo 3 en los 29 siguientes, ya con agentes nuevos). Lejos del tope de 75 %.
- **09:45** Verificación final (agente nuevo): los dos recorridos al mar sin errores; auditoría limpia en cuatro tamaños; 55,6
  cuadros por segundo con la CPU frenada, la barca a 0,09 px del curso; seis efectos de sonido válidos. Ningún hallazgo grave; dos
  medios, los dos del motor de Cauces; trece menores. Miré la hoja de comparación (antes, 60 minutos, corrida larga).
- **09:46** **Decisión de cierre:** paro a los 80 minutos de los 180. Solo quedan hallazgos menores (la condición de parada de la
  instrucción) y la sesión que dirige está por llenar su ventana de contexto; seguir sería gastar cuota en retoques chicos. Informe
  en `informe.md`; el de la primera corrida pasa a `informe-60-min.md`.
