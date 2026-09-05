# De Cauces a rutas: diagnóstico y propuesta (fase 1)

> **Estado (2026-09-04, noche): fases 2 y 3 hechas.** Decisiones de Humberto: viajeros y conquista, para niños y adultos;
> repositorio git abierto; los nombres internos (`rioPor`, `abrirRio`) quedan como alias; relieve en Exploradores desde
> el principio; cámara por tramo para los viajes largos. Lo hecho: `RUTAS`, `desdeRio`, `normalizar`, `VOCAB`
> (rio e itinerario), `JUEGO` por juego, `voces.js`, `build.js` con dos objetivos, instantánea de 200 pantallas,
> `itinerarios.js` con Ibn Battuta (9 etapas), `tools/rutas.py`, `tools/itinerarios.py`, mapa y relieve por juego,
> preguntas `fin`/`fecha`/`orden`, línea de tiempo, cámara por tramo, glifos de caravana y caminante, viento,
> `casos-exploradores.js` y `verificacion.md` con el itinerario. Después entraron Marco Polo, Alejandro Magno, Hernán Cortés
> y Zheng He (tipo `travesia`, la «derrota» de este documento), con lo que volvieron las preguntas de viaje, frase y contexto.
> Pendiente: cortes en la animación, antimeridiano (sección 4.4). CLAUDE.md es la referencia viva; este documento queda como
> diseño y memoria.

Estado de partida (2026-09-04): `npm test` termina en TODO OK y `npm run build` deja `dist/cauces.html` en 460 KB.
Este documento es solo lectura del código: no se tocó el motor. Responde a `instruccion-itinerarios.md` con tres
salvedades, porque son decisiones ya tomadas que la instrucción no conocía:

- El tope por archivo es **500 KB**, no 400 (subido hoy para el relieve). Un `exploradores.html` cabría igual con 400.
- Son **19 rutas**, no 13: trece ríos del mundo y seis de Costa Rica con `zona:'cr'`, vista propia y costa de 10 m.
- **No hay repositorio git** en `cauces-proyecto`. Donde la instrucción dice «commits», acá hay «pasos», cada uno
  cerrado con `npm test` en TODO OK. Si querés historial, el primer paso de la fase 2 puede ser `git init`.

Y hay subsistemas nuevos que la instrucción no menciona y que también asumen «río»: pasaporte y sellos, Hoy
(cola diaria), escenas, luz y clima, barcas con glifos, animales SVG, voz, perfiles de jugador, relieve y perfil
de altura. Todos están en el inventario.

## 1. Inventario: todo lo que hoy asume que la ruta es un río

### 1.1 Campos de datos

| Dónde | Campo | Qué asume |
|---|---|---|
| `rios.js` RIVERS | `curso` | Una sola polilínea continua de la fuente al mar, sin cruzar el antimeridiano; 40+ vértices (20 en zona); generada por `tools/cauces.py` con un vértice frente a cada ciudad. |
| | `brazos` | Afluentes: solo se dibujan (`.rio.brazo`); el test exige que empalmen al cauce (≤ 0,02°). |
| | `mar`, `marEn` | El final es un mar con artículo («el mar Negro»). Pregunta `mar` y cabecera «km hasta». |
| | `nace`, `naceNota`, `escenaNace`, `escenaMar` | Inicio = nacimiento; fin = desembocadura. |
| | `antigua`, `moderna`, `pistaAntigua`, `pistaModerna` | Dos capas de contexto con nombre fijo «Ruta antigua / Ruta moderna» y sus preguntas. |
| | `longitud` | Km oficiales; escala `c.km` (`acum/kmPoly*longitud`), kicker «km ≈», fila del inicio, cabecera, nota de la pregunta `mar`. |
| | `continente` | Etiqueta de región en la fila y la cabecera. |
| | `zona` | Vista de zona, costa fina de 10 m, distractores por zona (`otrosRios`, mares), grupo en la lista. |
| | `ciudades[]` | `nombre, pais, pos, imagen, dato, escena`; el motor les cuelga `idx`, `km`, `puerto`, `carga`. |
| `naves.js` NAVES[id] | `tipo` | Uno de los siete glifos náuticos de `glifo()`. `puertos[i]` = [texto, carga] por ciudad (modo Historia). |
| `mascotas.js` MASCOTAS[id] | `hola`, `mar`, `paradas[]` | La frase del final se llama `mar`. `VOCES` genéricas hablan de río y capitán. |
| `mercados.js` MERCADOS[id] | `o`, `d`, `m` | Puerto de origen, puertos hasta pudrirse, puerto donde se paga doble. `RANGOS` son grados navales. |
| `eventos.js` EVENTOS[id] | `tramo`, `reto` | Retos `imagen, ruta, pais, frase, mar`; «mar» es el destino final. |
| `relieve.js` | `ALTURAS[id]`, `NOMBRES_RELIEVE[].v[id]`, `RELIEVE[vista]` | Perfil de altura por río; etiquetas ancladas por id de río; franjas recortadas a las vistas de los ríos. |
| Índices | `NAVES`, `MASCOTAS`, `MERCADOS`, `EVENTOS`, `ALTURAS` | Todo indexado por id de río y pegado al cargar (`r.nave`, `r.masc`, `r.mercado`, `r.fantasma`). |

### 1.2 Vocabulario en el motor (textos visibles y de voz)

Todas las cadenas donde aparece río, fuente, mar, desembocadura, puerto, bodega, barca, cauce, km, zarpar,
descender, capitán o mercader, con la función donde viven. La sección 5 dice a qué clave de `VOCAB` va cada una.

| Función | Texto |
|---|---|
| `cabecera` | «‹ Ríos», aria «Volver a los ríos», title «Sonido del agua» |
| `render` | «Cauces» / «Los grandes ríos, ciudad por ciudad»; «N ríos completos»; «Europa · 2 850 km hasta el mar Negro»; «Diez preguntas de todos los ríos» |
| `tabs` | «Descender» |
| `renderInicio` | «Tocá un río en el mapa o en la lista.», «Los grandes ríos», «Podio por longitud» (No Ames Ya Más), «Ríos de Costa Rica» + nota, «¿Cómo se juega?» (río, fuente, mar, embarcación, bodega, puerto), notas de Ajustes («precios que suben río abajo», «puerto por puerto»), fila «N ciudades / paradas» |
| `renderDescender` | «Nacimiento · km 0 de N · N m sobre el mar», «Tu embarcación», «Zarpás con diez monedas y la bodega vacía», «El mercader de la ruta suele llegar con N», «Contame más: la ruta antigua/moderna», «Parada p de n · km ≈», «N km desde X / desde la fuente / en la fuente misma», «el río pasa a N m sobre el mar», «En el puerto», «El mercader llevaba:», «Llegar al mar ›», «Desembocadura · km N», «Después de N km, el X llega a Y», «Cuentas del viaje», «Zarpaste con 10 monedas», «Lo que quedaba en la bodega se vendió en» |
| `botonZarpar` | «Zarpar a X ›» |
| `renderMercado` | «Mercado de X», «Cerrado: ya llegaste al mar con esta barca», «bodega N de 3», «se pasa en N puertos», «se paga mejor en», «vale más río abajo», «Se vende aquí», «aquí solo podés vender», «vendé si te conviene» |
| `renderEvento` | «Entre la fuente y X», «el mar» |
| `renderOrden`, `renderRecitar` | extremos «Fuente» y «Mar», «Tocá las N ciudades en orden, de la fuente al mar», «el cauce ya es tuyo», «volvé a bajar el río con la frase en mano» |
| `renderQuiz`, `MSG_QUIZ` | «Ya dominás este cauce», «Volvé a bajar el río con calma» |
| `renderPasaporte` | grupos de ríos, «Un río completo / N ríos completos», «llegando a una ciudad», «Los ríos completos se pintan de dorado», «Volver a los ríos» |
| `renderHoy`, `iniciarRepaso` | «Bajá un río o jugá un reto», «Bajá un río hasta el mar» |
| `lectura` | «Nacimiento: X.», «Parada p de n: X, país.», «Desembocadura: X. Después de N kilómetros, el Y llega a Z.», «de la fuente al mar», «El río pasa a N metros» |
| `preguntaTipo` | «¿Junto a qué río está X?», «más cerca de la desembocadura del X», «De la fuente al mar: …», «Ruta antigua: «…» ¿De qué río se trata?», «¿Dónde desemboca el X?», «N km hasta …», «En el X, ¿qué parada sigue…?», relleno «La desembocadura», «¿De qué ciudad del X es esta imagen?», «¿En cuál de estas paradas del X pasa el río más alto…?», «¿Qué frase guarda el orden de las ciudades del X?» |
| `perfilSVG`, `textoAltura`, `fraseAltura` | «Altura del cauce», «Perfil de altura del X: de N m en la fuente a 0 m en el mar», «el río pasa a / ya va al nivel del mar / bajo el nivel del océano» |
| `VOCES` (mascotas.js) | «el río ya está en tu cabeza», «Volvamos a bajar el río juntos», «¡Ese es mi río!», «¡Sos capitán de este río!», «Un par de viajes más y sos capitán», «Bajemos el río otra vez» |
| `VOCES` de economía (mercados.js) | «¡Esa! Zarpamos hacia {c}», «Rumbo a {c}», «en ese puerto no vas a poder comprar», «mercader de la ruta» (×3), «El río nos puso una prueba», «El río nos deja pasar» |
| `RANGOS` | Grumete, Marinero, Capitán, Almirante, Señor de los Cauces |
| `cabeza.html` | `<title>Cauces: los grandes ríos, ciudad por ciudad</title>`; el resto de las etiquetas del esqueleto es neutro |

Los textos de contenido (naves, mascotas, eventos, datos de ciudades) hablan de ríos porque son ríos: se quedan.

### 1.3 Preguntas y tarjetas

- Tipos: `ciudad` (¿junto a qué río?), `imagen`, `cerca` (más cerca de la desembocadura), `siguiente`, `frase`,
  `antigua`, `moderna`, `mar`, `pais`, `altura`. Los distractores de `ciudad`, `frase`, `antigua`, `moderna` y `mar`
  salen de **otras rutas** (`otrosRios`), primero de la misma zona: con menos de cuatro rutas en un juego esas
  preguntas no se pueden armar.
- Tarjetas Leitner: `rio:ID:orden|antigua|moderna|mar` y `ciudad:ID:i` (`idsDe`, `preguntaDeCard`, `selloOro`,
  `colaHoy` agrupa por el segundo trozo de la clave). El prefijo `rio:` está guardado en el progreso de la gente.
- `iniciarQuiz` arma seis preguntas fijas; `iniciarReto` sortea diez de todos los tipos; los eventos mapean
  `reto` → tipo (`ruta` → `siguiente`, `mar` → `mar`).

### 1.4 Funciones e identificadores con «río» adentro

`rioPor`, `otrosRios`, `abrirRio`, `S.rio`, `focoRio`, `renderDescender`, `botonZarpar`, `kmParada`, `idxParada`,
`renderMercado`, `fantasma`, `cerrarEco`, `animarBarca`, `#barca`/`.barca`, `estacionada`, `S.viaje`, `audio.remar`,
`ambiente` («amanecer en la fuente, atardecer en el mar»), `ZONAS` (dentro de motor.js), `store.clave`
(`cauces:progreso:<perfil>`, `cauces:perfiles`), `progresoJSON` (`app:'cauces'`). Ninguno necesita cambiar de
nombre para generalizar: son nombres internos. Propongo conservarlos (las pruebas los usan) y documentar que
«rio» en un identificador significa «ruta»; renombrar sería churn sin valor para la memoria.

### 1.5 Mapa y herramientas

- `renderMapa` dibuja `curso` como un solo `<path>` y `brazos` aparte; la barca avanza por `curso.slice(de,a)`;
  `puntoMedio` interpola sobre `acum` (km reales de la polilínea). Vista: `vbPara` sobre todos los puntos de la
  ruta, ancho mínimo 20 unidades (3 en zona), aspecto de la pantalla. Una ruta que dé media vuelta al mundo
  cabría, pero como una línea en un hemisferio, y una que cruce 180° se rompería (x salta de 1000 a 0).
- `tools/mapa.py`: costa 110 m en el mundo, 50 m dentro de los rectángulos de vista de cada río (aspectos 1.0 y
  2.4), 10 m dentro de los de zona. `tools/relieve.py`: franjas recortadas a esos mismos rectángulos (aspectos
  1.0 a 4.0) y etiquetas con ancla por id de río. Los dos leen `RIVERS` de `rios.js`. `tools/cauces.py` solo
  sirve para ríos (grafo de tramos de Natural Earth). `tools/verificacion.py` lee `RIVERS`, `NAVES`, `MASCOTAS`,
  `EVENTOS` y `ALTURAS`.
- `test/casos.js`: exige por ruta 40 vértices (20 en zona), cada ciudad a ≤ 0,25° de su vértice (Tombuctú y
  Karachi 1°), brazos empalmados, saltos ≤ 230 km, cuatro ciudades mínimo, acróstico, naves y mascotas con
  tantas entradas como ciudades, y recorre todas las rutas en los dos modos («animal siempre presente»).

## 2. Esquema `RUTA`

Una ruta es lo que el motor recibe; los archivos de datos pueden seguir en su forma actual. Los ríos se
convierten al cargar con `desdeRio(r)`; los datos nuevos (itinerarios, derrotas) se escriben ya en este esquema y
pasan por `normalizar(ruta)`, que calcula lo derivado y aplica el vocabulario.

```js
{
  id:'danubio', tipo:'rio',                    // 'rio' | 'derrota' | 'itinerario'
  nombre:'Danubio', region:'Europa', zona:null, // region = hoy `continente`; zona = vista propia ('cr')
  longitud:2850,                               // km oficiales; opcional (sin él, el progreso va por etapas)
  inicio:{nombre:'Selva Negra', nota:'Nace en Donaueschingen…', escena:['montaña','arbol','casas']},
  fin:{nombre:'Mar Negro', en:'el mar Negro', escena:['delta','aves','barco']},
  contexto:[                                   // dos capas con nombre neutro; hoy antigua/moderna
    {clave:'antigua', titulo:'Ruta antigua', texto:'…', pista:'…sin nombres propios…'},
    {clave:'moderna', titulo:'Ruta moderna', texto:'…', pista:'…'}],
  frase:'[U]n [R]ey…', fraseNota:'…',
  trazo:[[[47.95,8.5],…]],                     // lista de segmentos [lat,lon]; el río tiene uno (= curso)
  ramas:[[[…]]],                               // hoy brazos: solo se dibujan
  paradas:[{nombre:'Ulm', pais:'Alemania', pos:[48.4,9.99], imagen:'…', dato:'…', escena:[…],
            fecha:null,                        // itinerarios: '1326' o 'hacia 1330'; va donde hoy va el km
            puerto:'…', carga:'…'}],           // hoy vienen de NAVES.puertos[i]
  vehiculo:{nombre:'…', tipo:'vapor', desc:'…', zarpe:'…', llegada:'…'},   // hoy NAVES[id]; tipos + caravana, pie
  companero:{nombre:'Valsa', especie:'cisne', emoji:'🦢', glifo:'cisne', hola:'…', fin:'…', paradas:['…']}, // MASCOTAS
  carga:[{n:'…', e:'🍇', o:0, b:3, d:2, m:4}], // hoy MERCADOS[id]; en itinerarios es el morral
  eventos:[{tramo:3, icono:'🌫️', titulo:'…', reto:'imagen', texto:'…', bien:'…', mal:'…'}],
  perfil:[[0,724],[0.12,482],…],               // hoy ALTURAS[id]; opcional
  camara:'toda',                               // 'toda' (hoy) | 'tramo' (la vista sigue al viajero)
  lon0:null,                                   // meridiano central si la ruta cruza 180° (ver 4.4)
  origenCausal:null, puerta:null,              // {nombre, pos, nota}: cordillera de origen, estrecho o garganta de salida
  vocab:{}                                     // sobreescrituras puntuales de VOCAB[tipo]
  // calculados por normalizar(): acum, kmPoly, paradas[].idx y .km, fantasma, vocab efectivo
}
```

Ejemplo de itinerario (dos etapas de las ocho a diez de Ibn Battuta, como forma, no como contenido verificado):

```js
{ id:'ibnbattuta', tipo:'itinerario', nombre:'Ibn Battuta', region:'c. 1325-1354',
  inicio:{nombre:'Tánger', nota:'Sale a los 21 años hacia La Meca…', escena:['casas','mezquita','barco']},
  fin:{nombre:'Tánger, de regreso', en:'Tánger, de regreso', escena:['casas','mezquita','camello']},
  contexto:[{clave:'entonces', titulo:'El mundo que vio', texto:'…', pista:'…'},
            {clave:'hoy', titulo:'Lo que queda', texto:'…', pista:'…'}],
  frase:'[E]l [M]…', trazo:[[[35.78,-5.81],[36.8,3.06],[30.05,31.24],…]],
  paradas:[{nombre:'El Cairo', pais:'Egipto', pos:[30.05,31.24], fecha:'1326', imagen:'…', dato:'…', escena:[…]},
           {nombre:'La Meca', pais:'Arabia Saudita', pos:[21.42,39.83], fecha:'1326', …}],
  vehiculo:{nombre:'La caravana del hach', tipo:'caravana', …}, companero:{…especie:'dromedario'…},
  carga:[{n:'Dátiles', e:'🌴', o:0, b:2, d:2}, …], camara:'tramo' }
```

## 3. `VOCAB` por tipo

Una tabla `VOCAB[tipo]`; cada ruta puede sobreescribir claves con `vocab`. Para `rio` las palabras son las de hoy,
letra por letra: ningún texto de Cauces cambia. Las columnas `derrota` e `itinerario` son propuesta.

| Clave | rio (hoy) | derrota | itinerario |
|---|---|---|---|
| `tipo` / `tipos` | río / ríos | derrota / derrotas | viaje / viajes |
| `inicio` / `fin` | Nacimiento / Desembocadura | Puerto de salida / Puerto de llegada | Partida / Regreso |
| `extremoInicio` / `extremoFin` | Fuente / Mar | Salida / Llegada | Partida / Regreso |
| `deInicioAFin` | de la fuente al mar | de la salida a la llegada | de la partida al regreso |
| `desdeInicio`, `enInicio` | desde la fuente, en la fuente misma | desde la salida, en el puerto de salida | desde la partida, en la partida misma |
| `llegarFin` | Llegar al mar | Llegar a puerto | Volver a casa |
| `hastaFin` | «N km hasta {fin.en}» | «N km hasta {fin.en}» | «{region} · de {inicio} a {fin}» |
| `parada` / `paradas` / `paradaCorta` | ciudad / ciudades / parada | puerto / puertos / escala | etapa / etapas / etapa |
| `puerto`, `enPuerto`, `llevaba` | puerto, En el puerto, El mercader llevaba | puerto, En el puerto, La nave llevaba | alto, En el camino, El viajero llevaba |
| `vehiculo`, `tuVehiculo` | embarcación, Tu embarcación | nave, Tu nave | caravana, Tu caravana |
| `carga`, `mercado`, `seVende` | bodega, Mercado de, Se vende aquí | bodega, Mercado de, Se vende aquí | morral, Trueque en, Se cambia aquí |
| `mercader` | mercader de la ruta | mercader de la ruta | viajero de la ruta |
| `avanzar`, `bajar`, `bajarVerbo` | Zarpar a, Descender, bajar | Zarpar a, Navegar, navegar | Seguir a, Viajar, viajar |
| `recorre` | Bajá un río | Navegá una derrota | Recorré un viaje |
| `progreso` | km (`c.km` de `longitud`) | km | fecha (`parada.fecha`) |
| `sonido` | Sonido del agua | Sonido del mar | Sonido del camino |
| `volver`, `lista`, `toca` | Volver a los ríos, Ríos, Tocá un río en el mapa o en la lista | …derrotas… | Volver a los viajes, Viajes, Tocá un viaje… |
| `completo`, `completos` | río completo, ríos completos | derrota completa… | viaje completo, viajes completos |
| `dominas`, `conCalma` | Ya dominás este cauce. / Volvé a bajar el río con calma | …esta derrota… | Ya dominás este viaje. / Volvé a recorrer el viaje con calma |
| `entreInicio`, `entreFin` | la fuente, el mar | la salida, la llegada | la partida, el regreso |
| `preguntas.*` | ver sección 4.1 | | |
| `voces` | las de hoy (VOCES + economía) | variantes | variantes («¡Ese es mi viaje!», «Seguimos hacia {c}») |
| `rangos` | Grumete… Señor de los Cauces | Grumete… Almirante | Aprendiz, Peregrino, Caravanero, Gran Viajero, Señor de los Caminos |

Las frases hechas del animal (`VOCES`) que hoy nombran el río pasan a `VOCAB[tipo].voces` con las mismas
cadenas para `rio`. Todo lo que no está en la tabla es neutro y no cambia.

## 4. Mecánicas por tipo

### 4.1 Preguntas

| Tipo | rio | derrota | itinerario |
|---|---|---|---|
| `ciudad` («¿junto a qué río está X?») | sí | sí («¿en qué derrota…?») | solo con ≥ 4 viajes en el juego («¿en qué viaje…?») |
| `imagen` | sí | sí | sí |
| `cerca` | «más cerca de la desembocadura» | «más cerca de la llegada» | «más cerca del final del viaje» |
| `siguiente` | sí | sí | sí |
| `frase` | sí | sí | con ≥ 4 viajes; si no, `orden` |
| `contexto` (hoy `antigua`/`moderna`) | sí | sí | con ≥ 4 viajes |
| `fin` (hoy `mar`) | «¿Dónde desemboca…?» | «¿Dónde llega…?» | «¿Dónde termina el viaje?»; distractores: etapas del mismo viaje si hay pocas rutas |
| `pais` | sí | sí | sí («país actual») |
| `altura` | si hay `perfil` | no | no |
| `fecha` (nuevo) | no | si hay fechas | «¿En qué año llegó a Delhi?» con los años de otras etapas como distractores |
| `orden` (nuevo) | no | no | «¿Cuál es el orden correcto?»: cuatro secuencias de cuatro etapas, una verdadera; marca la tarjeta `orden` |

`iniciarQuiz` deja de tener seis tipos fijos: toma seis de los disponibles para el tipo y el juego, con la misma
composición que hoy cuando la ruta es un río (ciudad/imagen, siguiente, cerca/altura, contexto, fin, frase). Los
retos de los eventos ya mapean `reto` → tipo; `mar` pasa a leerse como `fin`.

### 4.2 Progreso sin kilómetros

`frac = paso/(n+1)` ya gobierna luz, sonido y perfil, y no depende de km: se queda. `c.km` se sigue calculando
sobre la polilínea (`acum`), pero se muestra solo si la ruta tiene `longitud`. Con `progreso:'fecha'` el kicker dice
«Etapa 3 de 9 · hacia 1330» y la línea de país «desde El Cairo, 1326». `puntoMedio` de los eventos usa `acum`:
funciona con cualquier trazo. El mercader fantasma y los precios cuentan «paradas pasadas», no km.

### 4.3 Morral

Misma economía (10 monedas, tres espacios, `precio` con `o`, `b`, `d`, `m`) con otras palabras: «Trueque en
Delhi», «Se cambia aquí», «se pasa en dos altos» (dátiles), «se paga mejor en D____» (oculta), «vale más adelante».
El «viajero de la ruta» es el fantasma. En Historia, `parada.carga` es lo que el viajero llevaba según el relato.
Memoria primero: comprar sigue exigiendo acertar la próxima etapa (`S.llaves`).

### 4.4 Mapa

- **Trazo por segmentos.** `renderMapa` dibuja un `<path>` por segmento; los índices de parada son globales sobre
  la concatenación. `animarBarca` recibe sub-polilíneas por segmento: al cruzar un corte, el vehículo desaparece al
  final de uno y aparece al inicio del siguiente (sin línea a través del mapa).
- **Antimeridiano.** Ruta con `lon0`: los puntos con longitud «al otro lado» se proyectan con x + 1000 y la tierra se
  duplica con `<use href="#tierra" x="1000">` (y lagos, fronteras, relieve), sin datos extra. Solo se activa en rutas
  que lo necesiten (Magallanes); Ibn Battuta no lo cruza.
- **Cámara.** `camara:'toda'` es lo de hoy. `camara:'tramo'` (para rutas de medio mundo): en Descender la vista es
  el rectángulo de [etapa anterior, actual, siguiente] con ancho mínimo 20; en Ordenar, Recitar y Preguntar, la
  ruta entera. Los ríos siguen en `toda`: cero cambio.
- **Costa y relieve finos por parada.** Para rutas cuya vista entera pase de 60 unidades, `mapa.py` y `relieve.py`
  usan como «cuenca» la unión de círculos de radio 8 unidades (≈ 3°) alrededor de cada parada más un corredor de
  2,5 unidades a lo largo del trazo, en vez del rectángulo de vista. Es lo que se ve cuando la cámara sigue el tramo;
  el resto del hemisferio queda en 110 m. Las etiquetas de relieve se anclan por ruta con esas mismas vistas.
- **Zonas** (`ZONAS`) salen de motor.js y pasan a la configuración del juego.

### 4.5 Franja bajo el mapa

`#perfil` se generaliza a «franja»: para rutas con `perfil`, la altura (hoy); para rutas con fechas, una **línea de
tiempo** con los años y el marcador en la etapa actual. Memoria: la cronología es a un viaje lo que la altura a un
río.

### 4.6 Vehículo, luz, clima, sonido

`glifo()` suma `caravana` (dromedario cargado, vista lateral, hacia la derecha) y `pie` (caminante con bordón).
Los náuticos conservan `.mece`; los terrestres usan `.anda` (balanceo corto); la estela pasa a huellas (mismo
`#estela`, guiones más cortos) y el salpicón a polvo (color tierra). Luz y clima van por `frac` y por icono: iguales.
El sonido es el mismo ruido rosa con otro filtro (`sonido:'viento'`), sin archivos.

### 4.7 Pasaporte, Hoy, Leitner, perfiles

Sellos por parada: iguales (río y país en el aro; en un viaje, viaje y país). Tarjetas: las rutas de tipo `rio`
conservan el prefijo `rio:` (progreso guardado); las demás usan `ruta:`; `preguntaDeCard` entiende los dos.
Almacenamiento con prefijo por juego (`JUEGO.clave`: `cauces:` / `exploradores:`), porque en `file://` los dos
archivos comparten `localStorage`; `progresoJSON.app` lleva el id del juego y la importación lo comprueba.

## 5. Migración campo a campo

| Hoy | `RUTA` | Cómo |
|---|---|---|
| `RIVERS[i]` | `RUTAS[i]` (mismo objeto, ampliado) | `desdeRio` agrega los campos nuevos sobre el objeto; los viejos quedan como alias para datos y pruebas |
| `continente` | `region` | alias |
| `nace`, `naceNota`, `escenaNace` | `inicio.{nombre, nota, escena}` | |
| `mar`, `marEn`, `escenaMar` | `fin.{nombre, en, escena}` | |
| `antigua`, `pistaAntigua` | `contexto[0].{texto, pista}`, `titulo:'Ruta antigua'`, `clave:'antigua'` | la clave conserva el id de tarjeta |
| `moderna`, `pistaModerna` | `contexto[1]` | ídem |
| `curso` | `trazo[0]` | el mismo arreglo |
| `brazos` | `ramas` | alias |
| `ciudades` | `paradas` | el mismo arreglo (comparten `idx`, `km`, `puerto`, `carga`) |
| `NAVES[id]` | `vehiculo` + `paradas[i].puerto/carga` | hoy ya se reparte al cargar |
| `MASCOTAS[id]` (`mar`) | `companero` (`fin`) | alias `masc` |
| `MERCADOS[id]` | `carga` | alias `mercado` |
| `EVENTOS[id]` | `eventos` | |
| `ALTURAS[id]` | `perfil` | |
| `VOCES`, economía, `RANGOS` | `src/data/voces.js` compartido; frases con río en `VOCAB.rio.voces` | mismas cadenas |
| `ZONAS`, título, grupos del inicio, podio, «¿Cómo se juega?» | `src/juegos/cauces.js` (`JUEGO`) | un archivo por juego |

## 6. Riesgos

1. **Dos nombres para lo mismo** durante la migración (`ciudades`/`paradas`). Se acepta a propósito: el motor lee
   solo los nuevos al terminar la fase 2; los viejos quedan para `rios.js` y `test/casos.js`, y CLAUDE.md lo dice.
2. **Que un texto de Cauces cambie sin querer.** Se cubre con una prueba de instantánea (sección 7, paso 0): antes
   de tocar nada se guarda el HTML de un recorrido determinista de dos ríos en los dos modos, y cada paso lo compara.
3. **Preguntas con pocas rutas.** Exploradores nace con un viaje: sin `fecha` y `orden`, el reto del río tendría
   solo cuatro tipos. Por eso entran en la fase 3, no después.
4. **Mapa de medio mundo.** La cámara por tramo y las cuencas por parada son nuevas; se prueban con Ibn Battuta
   antes de cualquier derrota. El antimeridiano queda diseñado pero se implementa cuando haga falta.
5. **Contenido.** La Rihla es discutida en China y en parte de Asia oriental; el dato lo dice y va marcado en
   `docs/verificacion.md`. Fechas «hacia», nunca exactas si no las hay.
6. **Peso.** Motor +5 KB (VOCAB, adaptador, glifos nuevos). `exploradores.html` ≈ 250-300 KB: cabeza 22, motor 92,
   voces 6, mapa propio 60-80, relieve propio (opcional) hasta 60, datos ≈ 25. Muy por debajo de 500.
7. **Progreso guardado.** Prefijo `rio:` y claves `cauces:` intactos: nadie pierde sellos ni tarjetas.

## 7. Plan de pasos

Cada paso termina con `npm test` en TODO OK y `node build.js`; si se abre git, cada paso es un commit en español.

**Fase 2 (sin cambio de comportamiento)**

0. Prueba de instantánea: `test/instantanea.js` recorre Danubio y Sarapiquí en Niño y Adulto con `Math.random`
   sembrado, guarda `#cab`, `#panel`, `#capa` y `#perfil` en `test/instantanea.json`; desde aquí, cualquier
   diferencia de texto es un fallo.
1. `src/data/voces.js`: VOCES, voces de economía y RANGOS salen de mascotas.js y mercados.js. Sin cambio de texto.
2. `VOCAB`, `desdeRio`, `normalizar`, `RUTAS` y `rutaPor` (alias de `rioPor`) al inicio de motor.js.
3. Motor por pantallas, leyendo `paradas/inicio/fin/contexto/vehiculo/companero/carga/trazo` y `VOCAB`:
   a) cabecera, inicio, Hoy, pasaporte; b) Descender, guía, mercado, eventos; c) Ordenar, Recitar, Preguntar y
   `lectura`; d) `preguntaTipo` (tipo `fin` con alias `mar`, `contexto` con alias `antigua/moderna`);
   e) mapa (trazo por segmentos, cámara), relieve y franja.
4. `src/juegos/cauces.js` (JUEGO: nombre, subtítulo, clave, grupos, podio, ZONAS, rangos) y `build.js` con dos
   objetivos y una lista de archivos por juego. `dist/cauces.html` idéntico en textos.
5. CLAUDE.md: esquema RUTA, VOCAB, JUEGO, alias, receta de datos nuevos.

**Fase 3 (Exploradores)**

6. Glifos `caravana` y `pie`, `.anda`, huellas y polvo, sonido de viento.
7. Preguntas `fecha` y `orden`; `fin` con distractores de la misma ruta; `iniciarQuiz` por disponibilidad.
8. Línea de tiempo en la franja; cámara por tramo; cuencas por parada en `mapa.py` y `relieve.py` (con el juego
   como argumento: `python tools/mapa.py exploradores`).
9. `src/data/itinerarios.js`: Ibn Battuta, 8-10 etapas verificadas (Tánger, El Cairo, La Meca, Bagdad o Tabriz,
   Kilwa, Delhi, Maldivas, China «según su relato», Malí de regreso), acróstico, imágenes, datos, dos contextos,
   caravana, compañero, morral, eventos; `tools/itinerarios.py` densifica el trazo entre puntos de paso a mano
   (geodésicas; se declara ilustrativo en docs).
10. `test/casos.js` corre también contra Exploradores (mismos chequeos que los ríos, más los suyos);
    `tools/verificacion.py` lee itinerarios; README y CLAUDE.md con la receta.

## 8. Decisiones que te pido antes de la fase 2

1. **Viajeros o conquista.** La instrucción dice «ningún itinerario de conquista; viajeros, no generales»; tu mensaje
   de hoy dice «rutas de exploración y conquista». Propongo Exploradores para viajeros (Ibn Battuta, Marco Polo,
   Zheng He, Elcano como derrota, Humboldt) y, si querés conquista, rutas marcadas `solo:'historia'` que el modo
   Niño no lista. El esquema lo soporta; el contenido lo decidís vos.
2. **git.** ¿Abrimos repositorio antes de la fase 2? Recomiendo que sí: la migración se lee mejor paso a paso.
3. **Nombres internos.** Conservar `rioPor`, `abrirRio`, `S.rio` como alias (recomendado) o renombrar todo.
4. **Relieve en Exploradores.** Con cuencas por parada (recomendado, ≈ 40-60 KB) o sin franjas al principio.
5. **Cámara por tramo** para Ibn Battuta (recomendado) o vista entera del viaje.
