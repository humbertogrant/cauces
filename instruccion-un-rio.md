# Instrucción para Claude Code: un río al nivel final (vitrina del Nilo)

> Cómo usarla: copiá este archivo a la raíz de `cauces-proyecto`, abrí Claude Code ahí y decile:
> «Leé instruccion-un-rio.md y ejecutala. Presupuesto: 60 minutos». Para la corrida larga, cambiá el número.

Leé `CLAUDE.md` completo antes de hacer nada. Después corré `npm test` y `npm run build` y confirmá que
ambos pasan ("TODO OK" y los `dist/` generados). Si algo falla antes de empezar, parás ahí y lo anotás en
el informe: no construyás sobre una base rota.

Lo que sigue describe el proyecto como estaba en setiembre de 2026. Si el repositorio cambió (por ejemplo,
si el motor ya está estandarizado en itinerarios), manda lo que hay en el repositorio y adaptás los nombres.

## Para qué es esto

Cauces funciona y enseña, pero se ve y se siente como prototipo. Quiero saber cuánto acabado compra una
corrida larga y autónoma tuya cuando el alcance es mínimo. Por eso el encargo es un solo río, el Nilo,
llevado al nivel que tendría el juego terminado: carta con relieve real, el río como hilo de oro, la falúa
e Hipo dibujados, la bitácora en papel, sonido propio y nada a medias. Los otros doce ríos no se tocan.

Es un experimento con dos resultados que me importan por igual: la vitrina y la medición (cuánto tiempo y
consumo tomó, qué quedó bien y qué no). Trabajás sin mí: no voy a estar para contestar preguntas. Cuando
dudés, decidí con los principios de `CLAUDE.md`, anotá la decisión en el diario de la corrida y seguí.

## Presupuesto y cómo gastarlo

- Presupuesto de esta corrida: **60 minutos** de reloj, salvo que yo te haya dado otro número al arrancar.
  Anotá la hora de inicio con `date` y revisala entre etapas.
- Repartilo más o menos así: 10 % leer y planear, 55 % construir, 25 % mirar y corregir, 10 % informe. El
  25 % de mirar y corregir no se recorta: de ahí sale el acabado.
- El alcance es fijo y la calidad solo varía hacia arriba. Si el tiempo no alcanza para todo, hacé menos
  piezas pero terminadas, en el orden de prioridad de más abajo. Tres piezas al nivel final valen más que
  ocho a medias.
- Si terminás antes, no agregués cosas: volvé a las capturas, buscá la pantalla más débil y subila de nivel.
- Al llegar al tope cerrás como esté: todo compilando, pruebas pasando e informe escrito.

## Alcance

Entra:

- Un objetivo de build nuevo, `dist/nilo.html`: el mismo motor, solo el Nilo (id `nilo`), con una capa de
  acabado encima. `build.js` lo genera además de lo que ya genera.
- La capa de acabado vive en `src/vitrina/` y se engancha al motor por pocos puntos explícitos: al zarpar,
  al avanzar la barca, al llegar a una parada, al llegar al mar, y plantillas alternativas para las
  pantallas de Bajar. Si la capa no está cargada, el motor se comporta exactamente como hoy.
- El recorrido completo de Bajar en el Nilo, en modo Mercader y en modo Historia: portada, navegación
  entre paradas con la guía de próxima parada, las seis paradas y la llegada al mar.

No entra:

- Mecánicas nuevas (eventos entre puertos, voz, perfiles, pasaporte), ríos nuevos, cambios al contenido o a
  los datos de los ríos, reescritura del motor.
- Ordenar, Recitar y Preguntar: en la vitrina heredan tipografía y colores de la bitácora, pero no se
  rediseñan en esta corrida.
- Cualquier cambio de comportamiento en `dist/cauces.html` (y en `dist/exploradores.html`, si existe).

## Dirección de arte

Una frase manda sobre todo lo demás: **carta náutica de noche con un solo hilo de oro, que es el río;
abajo, la bitácora en papel cálido.**

Es la identidad de La Ruta que Cauces ya usa, llevada más hondo; no es otra identidad. El principio 5 de
`CLAUDE.md` sigue vigente y esta instrucción es el permiso explícito para profundizarla dentro de la
vitrina. Cuando una decisión visual no esté cubierta aquí, preguntate cuál opción se parece más a esa frase.

| Elemento | Valor |
|---|---|
| Mar | `#0C3A33` con seigaiha tenue (verde claro al ~13 %) y un halo claro pegado a la costa |
| Tierra | `#215A4F` como base; con relieve se mueve entre `#174A3F` y `#2B6E5E` |
| Río recorrido, vela de la barca | dorado `#E8B952`, con un resplandor suave. Nada más es dorado |
| Río por recorrer, afluentes | crema `#FBF8F2` al ~70 % y verde claro `#64C8AA` al ~60 %, líneas finas |
| Bitácora | papel `#FBF8F2` con grano muy leve; tarjetas blancas, borde de 1 px `rgba(15,66,58,.2)` |
| Texto | `#0F423A` títulos y botones, `#2D2D2D` cuerpo, `#6B6B6B` secundario |
| Tintes para ilustración | `#E9F5F0`, `#B7E3D3`, y un único acento cálido `#D89B85` |
| Rojo teja `#A6472E` | solo errores, como hoy |

- El dorado no entra en la bitácora: sobre papel no da contraste y deja de señalar al río.
- Tipografía: Oswald 700 para el nombre del río (≈96 px en la portada) y el de la ciudad (≈42 px); Oswald
  500 en mayúsculas para botones y rótulos; Source Sans 3 400/600 para el cuerpo (15/21) y lo secundario
  (14/20). Un solo título dominante por pantalla. Nada por debajo de 11 px.
- Rótulos de la carta, con jerarquía de atlas: mares y lagos en cursiva espaciada y verde claro; países y
  desiertos en mayúsculas muy espaciadas, crema al ~60 %; ciudades ya visitadas en Oswald mayúsculas;
  hitos (Abu Simbel, Meroe) en 11 px.
- Ilustración: línea de 1,3 a 1,6 px en verde muy oscuro, rellenos con los tintes, sin degradados y sin
  emoji. Hipo, la falúa, los bienes de la bodega y las imágenes para recordar comparten ese trazo.
- Formas: hoja de la bitácora con esquinas superiores de 22 px; tarjetas de 16; botones de 12 a 14;
  botón principal verde oscuro de 52 px de alto; todo lo tocable mide al menos 44 px.
- Movimiento: salidas suaves de 200 a 350 ms; el único movimiento largo es el viaje de la barca. Con
  `prefers-reduced-motion`, fundidos y nada más.
- Sonido: madera, agua y viento. Nada que suene a máquina de juegos.

Referencia visual: si existe `docs/vitrina/referencia/`, ahí hay cuatro imágenes de una maqueta estática
(portada, navegando, parada en Asuán, llegada al mar). Miralas antes de planear. Tomá de ahí composición,
jerarquía y ánimo; no es una especificación al píxel y solo muestra teléfono. Los textos del Nilo en la
maqueta son los del juego. Los precios, las monedas, los km en ruta y la pregunta de Hipo en la guía son
ilustrativos: la verdad está en `src/data/` y en el motor.

## Qué significa "nivel final", en orden de prioridad

1. **La carta.** Relieve sombreado real, generado por una herramienta nueva en `tools/` a partir de datos
   de elevación y dibujado dentro del mismo SVG, recortado por la tierra y en la proyección que ya usa el
   motor. Curso real del Nilo en lugar de la polilínea a mano (es el pendiente de "cauces reales", solo
   para este río): la barca y los índices de parada deben seguir funcionando. Lagos, fronteras punteadas,
   retícula tenue, ecuador y trópico de Cáncer punteados, rótulos con la jerarquía de arriba. Cuatro
   encuadres: el río entero, el tramo en curso, la parada y el delta.
2. **El hilo de oro y las paradas.** Lo recorrido en dorado, lo que falta en claro. Las paradas visitadas
   llevan punto y nombre; la próxima es un anillo punteado con signo de pregunta; las siguientes no llevan
   nombre. Memoria primero: fuera de las alternativas que ofrezca la guía, ningún nombre de parada futura
   aparece en la carta ni en el panel.
3. **La bitácora.** El panel inferior como hoja de papel con el sistema tipográfico de arriba: rótulo de
   parada, nombre de la ciudad, país y distancia, la voz de Hipo en globo, la imagen para recordar en
   tarjeta, el dato, la bodega y el mercado, y el botón de zarpar. Un sello circular por parada.
4. **La falúa e Hipo.** Barca dibujada con vela latina, estela y la carga a la vista (el obelisco de
   Asuán tiene que verse). Hipo dibujado, con tres o cuatro expresiones, en el globo y nadando junto a la
   barca. Iconos dibujados para los bienes del Nilo. En la vitrina no queda ningún emoji.
5. **Portada y llegada al mar.** Portada a pantalla completa con el río entero, el nombre, la distancia y
   el saludo de Hipo. Llegada con el delta, el texto de llegada de la nave y las cuentas del viaje.
6. **El acróstico como progreso.** Seis fichas que se llenan con la inicial de cada parada alcanzada y la
   frase que se va completando («Tres Jotas y un…»). En la llegada al mar la frase entera es el título.
7. **Imágenes para recordar, dibujadas.** Una viñeta por parada que muestre exactamente la imagen
   mnemónica que ya está escrita en los datos, sin agregarle ideas.
8. **Perfil del río.** Una tira con la altitud a lo largo del curso y la posición de la barca, con datos
   reales y forzada a bajar siempre (un río no sube). Si no hay fuente verificable, se omite.
9. **Sonido.** Sintetizado con WebAudio y extendiendo el audio que el motor ya tiene: fondo de agua,
   viento en la vela, llegada a puerto, moneda, sello. Arranca solo después del primer toque, el silencio
   se recuerda y nada satura. Va de último porque es lo único que no podés juzgar vos.

En pantallas de 820 px o más, la carta va a un lado y la bitácora en una columna de 380 a 420 px.

Datos para la carta, verificados al preparar la maqueta:

- Curso: en `ne_10m_rivers_lake_centerlines` de Natural Earth, encadenar los tramos (ríos y ejes de lago)
  llamados Victoria Nile, Albert Nile, Bahr el Jebel, El Bahr el Abyad, Nile y Rosetta Branch, empezando
  en Jinja (0,43° N, 33,19° E) y dejando fuera el eje del lago Victoria que va hacia el Kagera. Salen unos
  1 800 vértices que terminan en 31,44° N, 30,40° E; simplificalos a la tolerancia de pantalla.
- Elevación: la maqueta usó un ráster global de baja resolución y alcanza para un relieve suave a escala
  de teléfono. Para el juego usá una fuente con licencia clara (ETOPO o SRTM, por ejemplo) y anotá fuente
  y licencia en `docs/verificacion.md`. El relieve embebido no debería pasar de unos 150 KB.

## Equipo y propiedad de archivos

Trabajá con subagentes, cada uno dueño de sus archivos. Nadie edita un archivo ajeno: si necesita un
cambio, se lo pide al dueño a través de vos. La razón es práctica: los subagentes no comparten contexto, y
dos manos en el mismo archivo producen estilos que no calzan.

| Rol | Es dueño de | Hace |
|---|---|---|
| Dirección (vos) | `docs/vitrina/`, `build.js`, los ganchos en `src/motor.js`, `CLAUDE.md` | Plan, contrato entre módulos, integración, arbitraje y el informe |
| Carta | `tools/` (lo nuevo), `src/vitrina/carta.*` | Relieve, curso real, encuadres, rótulos, hilo de oro, cámara |
| Bitácora | `src/vitrina/panel.*` | Hoja de papel, tipografía, fichas del acróstico, sellos, portada y llegada |
| Trazo | `src/vitrina/arte.*` | Hipo, falúa y carga, iconos de bienes, viñetas mnemónicas |
| Sonido | `src/vitrina/sonido.*` | Paisaje sonoro y efectos |
| Verificación | `test/` (lo nuevo), `tools/captura.*`, `docs/vitrina/hallazgos.md` | Pruebas, recorrido automático, capturas y mediciones. No corrige código de otros |

Antes de repartir, escribí `docs/vitrina/contrato.md`: los ganchos del motor con sus argumentos, los
nombres de clases y variables CSS compartidas, y qué exporta cada módulo. Cada encargo a un subagente
lleva la frase de dirección de arte, la tabla de valores, su lista de archivos, el contrato y la
prohibición de tocar lo ajeno. Si tu entorno no permite subagentes en paralelo, hacé los mismos roles en
serie y respetá igual la propiedad de archivos.

## El ciclo de mirar y corregir

Esta es la parte que más pesa en el resultado. Ninguna pieza está terminada hasta que la viste.

1. Antes de construir, capturá el Nilo actual desde `dist/cauces.html` en los cuatro momentos (inicio del
   río, navegando, parada 4, llegada al mar). Ese es tu "antes".
2. Montá `tools/captura.*` con Playwright como dependencia de desarrollo (si no se puede instalar, usá el
   Chrome del sistema en modo headless). Tiene que recorrer el río completo con clics reales, no con
   atajos de estado, y guardar capturas en `docs/vitrina/capturas/` a 390×844 en cada vuelta y también a
   820×1180 y 1440×900 al cierre.
3. Después de cada integración: `npm test`, `npm run build`, recorrido, capturas, y abrí las imágenes y
   miralas. Revisá, en este orden:
   - ¿El río es lo único dorado y se lee de un vistazo?
   - ¿Hay un solo título dominante y la jerarquía se sostiene?
   - ¿Algo cortado, encimado, desalineado o con texto de menos de 11 px? ¿Algún rótulo sobre el río?
   - ¿Se ve el nombre de alguna parada futura?
   - ¿Queda algún emoji o un dibujo con otro trazo?
   - ¿El panel respira: márgenes de 18 px y separaciones parejas?
   - ¿Contraste de texto de al menos 4,5 a 1?
4. Anotá lo que veás en `docs/vitrina/hallazgos.md` con la captura al lado, corregí los tres más graves y
   repetí. Parás cuando solo queden hallazgos menores o se acabe el tiempo.
5. Lo que no se ve se mide. Movimiento: con la CPU frenada 4×, la barca viaja a 50 cuadros por segundo o
   más de mediana y ningún cuadro pasa de 100 ms; capturá cinco cuadros del viaje y comprobá que la barca
   va sobre el curso. Sonido: no podés oírlo, así que renderizá cada efecto con `OfflineAudioContext` y
   comprobá duración, pico por debajo de 0 dBFS y ausencia de valores inválidos; decilo así en el informe.

## Reglas que no se negocian

- Memoria primero. Nada de la vitrina puede revelar lo que el juego le pide recordar al niño.
- Nada inventado. Relieve, curso y altitud salen de datos; ningún dato, cifra o fecha nueva entra al
  juego. Los textos nuevos de interfaz (rótulos, botones) van listados en `docs/vitrina/textos-nuevos.md`
  para que yo los revise. Si falta un dato, se deja fuera y se anota.
- Español de Costa Rica con voseo, frases cortas para niño, y el compañero nunca regaña.
- Un solo archivo por juego y sin dependencias de ejecución. `dist/nilo.html` corre sin red (las fuentes
  pueden ir embebidas en subconjunto) y pesa menos de 900 KB. `dist/cauces.html` sigue bajo sus ~400 KB.
- Los 13 ríos de `dist/cauces.html` se comportan idénticos al terminar. Si hay que elegir entre una capa
  elegante y no romper Cauces, no rompés Cauces.
- No cambiés el esquema de datos existente: lo que la vitrina necesite de más (iconos, viñetas, sellos) va
  en `src/vitrina/`, indexado por lo que ya existe.
- El arnés de pruebas usa un DOM simulado: lo que la capa haga al cargar tiene que tolerarlo.
- Accesibilidad: botones reales, `aria-label` en los iconos, `prefers-reduced-motion` respetado, sonido
  apagado hasta el primer toque.
- Git: trabajá en una rama nueva `vitrina-nilo`, con commits pequeños en español. Sin push y sin tocar
  otras ramas.
- Donde esta instrucción y `CLAUDE.md` choquen, manda esta dentro de la vitrina y `CLAUDE.md` fuera de ella.

## Criterios de aceptación

1. `npm test` termina en "TODO OK", con casos nuevos: los ganchos se llaman en orden, las fichas del
   acróstico corresponden a las paradas alcanzadas, la carta no contiene nombres de paradas futuras y en el
   panel solo aparecen como alternativas de la guía.
2. `npm run build` genera `dist/nilo.html` y los demás `dist/` de siempre; `dist/cauces.html` pasa el mismo
   recorrido que antes en ambos modos.
3. El recorrido automático baja el Nilo completo en Mercader y en Historia sin errores de consola.
4. Capturas de antes y después de los cuatro momentos en `docs/vitrina/capturas/`, y `hallazgos.md` sin
   pendientes graves.
5. Mediciones dentro de lo pedido en el ciclo (cuadros por segundo, pico de audio, tamaño de archivo).
6. Cada pieza de la lista de prioridad figura en el informe como terminada, a medias o no tocada. Una
   pieza a medias que estorba se desactiva antes de cerrar.

## Lo que me entregás

- `dist/nilo.html`.
- `docs/vitrina/`: `plan.md`, `contrato.md`, `diario.md` (con hora en cada entrada: qué se intentó, qué
  se decidió sin consultarme y por qué), `hallazgos.md`, `textos-nuevos.md`, `capturas/` e `informe.md`.
- `docs/vitrina/encargos-ilustracion.md`: las seis imágenes para recordar descritas como encargo (texto
  mnemónico, tamaño, paleta), por si después quiero producirlas pintadas en mi propio equipo. Cada viñeta
  queda como un espacio con su dibujo de línea por defecto.
- `informe.md` empieza con cinco líneas de resumen y sigue con: tiempo usado y consumo (tokens o costo, si
  tu entorno lo muestra); cuántas vueltas del ciclo hiciste; qué quedó terminado, a medias y sin tocar;
  mediciones; lo que no pudiste verificar (cómo suena, cómo lo juega un niño) con tres cosas concretas que
  yo debería probar con un jugador de verdad; y la propuesta para la siguiente hora, ordenada por impacto.
- Actualizá `CLAUDE.md` con una sección corta sobre la vitrina: el build nuevo, la capa y sus ganchos.
