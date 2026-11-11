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
