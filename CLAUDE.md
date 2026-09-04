# Cauces

Juego HTML de un solo archivo para aprender los grandes ríos del mundo: cada río es un palacio de la memoria
que se baja de la fuente al mar, ciudad por ciudad, con un acróstico, imágenes mnemónicas, una barca, un animal
guía, un mercado de trueque y repaso espaciado (Leitner). Dos audiencias, con un interruptor Niño/Adulto: sus
hijos (Niño, por defecto: mercader, textos plegados, voz que lee sola) y Humberto (Adulto: historia completa y carga
fija). El animal acompaña igual en los dos modos. Idioma: español de Costa Rica, voseo, sin jerga sin explicar.

## Principios (no negociables)

1. **Memoria primero.** Nada divertido ocurre sin recordar algo. Cada capa nueva (eventos, voz, sellos) tiene que
   pagar en la moneda de la memoria: pedir una ciudad, un orden, una ruta. Si una función se puede ganar sin saber
   nada del río, está mal diseñada.
2. **Un solo archivo, sin dependencias.** `dist/cauces.html` corre en cualquier navegador sin red. Nada de
   frameworks, bundlers ni npm en producción. Solo Google Fonts (sin red, caen a las del sistema). Nada llama a
   ningún servicio, ni a Claude ni a otra API: tiene que correr igual desde un doble clic en el archivo.
3. **Nada inventado.** Cada dato numérico, fecha o superlativo tiene que ser verificable. Si una cifra es
   aproximada, se marca (≈, "hacia", "unos"). Si no hay certeza, se quita. `docs/verificacion.md` lista las
   afirmaciones a revisar; se regenera con `npm run verificacion`.
4. **Prototipo primero.** "Funciona feo pero funciona" es un resultado válido. Pulir después.
5. **Identidad visual de La Ruta.** Paleta: verde oscuro #0F423A, verde claro #64C8AA, dorado #E8B952 (solo el
   río activo, la barca y acentos), gris #2D2D2D/#6B6B6B, rojo teja #A6472E para errores. Mar #0C3A33 con patrón
   seigaiha, tierra #215A4F. Tipografías Oswald (títulos) y Source Sans 3 (cuerpo). No cambiar sin pedirlo.

## Estructura

```
src/cabeza.html      DOCTYPE, <head>, CSS completo y esqueleto del body (cabecera + mapa SVG + panel)
src/cola.html        cierre
src/data/mapa.js     LAND, LAGOS, BORDES: paths SVG (Natural Earth 110 m fuera de las cuencas, 50 m dentro)
src/data/rios.js     RIVERS: 19 ríos, 13 del mundo y 6 de Costa Rica (zona 'cr'); curso y brazos los genera tools/cauces.py
src/data/naves.js    NAVES: embarcación, zarpe, llegada y carga narrativa por puerto (modo Historia)
src/data/mascotas.js MASCOTAS (animal guía por río) y VOCES (frases genéricas)
src/data/mercados.js MERCADOS (bienes por río), RANGOS y voces de la economía
src/data/eventos.js  EVENTOS: pruebas entre puertos por río (tramo, reto, textos)
src/data/relieve.js  RELIEVE (franjas de altura por vista), NOMBRES_RELIEVE (cordilleras, mesetas, desiertos, volcanes) y ALTURAS
                     (perfil de altura de cada cauce); lo genera tools/relieve.py
src/motor.js         todo el motor: estado, perfiles y guardado, Leitner, preguntas, render, mapa, audio, economía, eventos, voz
build.js             ensambla dist/cauces.html en el orden de arriba
test/pruebas.js      arnés con DOM simulado; test/casos.js son los casos. `npm test` debe terminar en "TODO OK"
tools/cauces.py      genera curso y brazos de rios.js desde Natural Earth (50 m; 10 m global y Norteamérica) u OpenStreetMap
tools/mapa.py        regenera src/data/mapa.js desde Natural Earth (110/50 m; 10 m en las cuencas de zona; shapely)
tools/relieve.py     regenera src/data/relieve.js: alturas de NOAA NCEI (ETOPO1 y mosaico DEM), nombres de Natural Earth 50 m y OpenStreetMap
tools/verificacion.py genera docs/verificacion.md
```

Comandos: `npm run build`, `npm test`, `npm run verificacion`, `npm run mapa`, `npm run cauces`, `npm run relieve` (los de Python
descargan Natural Earth a `tools/ne/` la primera vez; en Windows no hay `python3`: correrlos como
`python tools/….py`). Antes de dar por terminado un
cambio: `npm test` y `npm run build`, y abrir `dist/cauces.html` en un navegador (o `python3 -m http.server`).

## Cómo está hecho el motor

- Estado en dos objetos: `S` (sesión: pantalla, río, pestaña, paso, orden, quiz, eco, guías, recitar, evento) y `P`
  (persistente: `cards` Leitner, `vistos`, `tesoro`, `modo`, `voz`, `sellos`). `P` se guarda con `guardar()` en `localStorage`
  bajo `cauces:progreso:<perfil>` (memoria si no hay o falla). `PERFILES` (`cauces:perfiles`: lista y activo) da
  un `P` por persona; "¿Quién juega?" en el inicio los elige o crea (`elegirPerfil`, `crearPerfil`,
  `quitarPerfil`); `cargarPerfiles()` migra el guardado viejo (`cauces:progreso`) al perfil Capitán. Copia y
  traslado: `progresoJSON()`/`exportar()` bajan un `.json` y `importarTexto()` lo carga (crea o reemplaza el
  perfil que trae el archivo, preguntando antes de pisar progreso).
- Todo se dibuja con `render()`: cabecera, panel (`renderInicio`, `renderDescender`, `renderOrden`,
  `renderRecitar`, `renderQuiz`) y mapa (`renderMapa(foco)`), a partir de `S`. Los manejadores son funciones
  globales llamadas desde `onclick` en el HTML generado. No hay componentes ni eventos delegados.
- Mapa: SVG con proyección equirectangular (`proj`), viewBox animado (`setVB`), tamaños en píxeles constantes
  (`px = vb.w / ancho del contenedor`). La barca se anima con `animarBarca` sobre la polilínea del río entre
  paradas; la mascota va en `#masc` y se contrarrota para quedar derecha. Fuera de Descender (Ordenar, Recitar, el
  reto del río) la barca queda estacionada en la parada actual (`estacionada(r)`) para que no desaparezca; en reto
  mundial y repaso, antes de responder, hay un globo neutro «Cauces» (`globoNeutro`) para no delatar el río sin
  dejar la pantalla sin globo. La barca es un glifo SVG propio
  por tipo (`glifo()`: latina, junco, vapor, balsa, canoa, barcaza, cuadrada; vista lateral, proa a la derecha,
  partes `casco` dorado, `vela` blanca, `linea` color mar solo sobre vela o casco, `palo` dorado para mástiles,
  chimeneas y remos contra el agua, `fig` blanca, `humo`), envuelto en `.mece` (balanceo CSS); al avanzar, `animarBarca`
  dibuja la estela `#estela` detrás y al llegar suelta un salpicón (`.salpicon`, se quita solo); si la guía salió
  mal, `S.bamboleo` añade la clase `duda` una vez. El mismo glifo va en el bloque «Tu embarcación» (`.barca.mini`).
  El animal (`ANIMALES[m.glifo]`) va en `#masc` sobre la barca, derecho y mirando hacia adelante
  (`rotate(-ang·sx)`: se anula el giro pero no el espejo), y en el globo del evento salta una vez (`.globo.salta`).
- Escenas (`PICTOS`, `escena(items)`): un vocabulario de pictogramas SVG (caja 40×40, suelo en y=40; clases `p`
  verde, `d` dorado, `b` blanco, `l` línea, `w` línea clara, `a` agua) y `animal:<glifo>` para los animales. Cada
  ciudad lleva `escena` con 3-4 claves y cada río `escenaNace`/`escenaMar`; se dibuja como postal (cielo, sol,
  suelo, río) sobre la imagen para recordar, en la fuente y en el mar; el reto de imagen la muestra sin nombre como
  pista (`q.escena`), y el sello del pasaporte lleva el primer pictograma (`.escena.pic`). Componer con lo que dice
  el dato de la ciudad (presa, templo, puente, manglar…), nunca al azar.
  Todo respeta `prefers-reduced-motion`. Los cauces son de Natural Earth
  50 m (`tools/cauces.py`), con un vértice propio frente a cada ciudad para que `c.idx` la ancle justo ahí.
- Relieve (`src/data/relieve.js`, de `tools/relieve.py`; alturas de NOAA NCEI: ETOPO1 para las franjas del mundo,
  el mosaico DEM fino para Costa Rica y el mosaico global para los perfiles, porque ETOPO1 trae el fondo de los lagos):
  · Franjas (`RELIEVE[vista]`: mundo ≥500 y ≥2 000 m, cr ≥500 y ≥1 500 m) en el grupo `#relieve` entre la tierra y
    los lagos, dos tonos de tierra (`--relieve1`, `--relieve2`) con trazo redondeado. Están recortadas a las vistas
    de los ríos (aspectos de pantalla 1.0 a 4.0), así que solo se dibujan en las vistas de zona y de río; en el
    mundo el grupo queda vacío. `renderMapa` las vuelve a poner solo cuando cambia la vista (`rel._z`).
  · Nombres (`NOMBRES_RELIEVE`: `t` cordillera | llano | desierto | pico): en el mundo salen de Natural Earth 50 m
    (regiones físicas con nombre en español, rango 1-2 siempre y rango 3-4 solo pegadas al cauce, hasta 14 por vista),
    con una posición por río (`v[id] = [lat, lon, giro]`) calculada dentro de lo que se ve con cualquier aspecto;
    en Costa Rica van a mano (`CR_NOMBRES`) y los volcanes y cerros (`PICOS_CR`) con posición de OpenStreetMap y
    altura publicada (`PICOS_ALTURA`; si OpenStreetMap difiere, el generador avisa). Se dibujan como `.etq.relieve`
    (cordilleras y desiertos en versalitas espaciadas, llanos en cursiva, picos con triángulo dorado y metros; los
    picos solo en la vista de un río), giradas según la forma, y ocupan lugar en `puestos` para que las etiquetas
    de ciudad las esquiven (`colocar`).
  · Perfil de altura (`ALTURAS[id]`: puntos `[fracción del cauce, metros]`, el río nunca sube, vértices de las
    paradas incluidos): `#perfil`, una franja SVG bajo el mapa en la pantalla de río (`perfilSVG`, oculta en las demás
    y con el mapa plegado), con el cauce en tierra, un punto por parada y el marcador dorado donde va la barca
    (`fracActual`); `alturaParada(r,i)` interpola la altura en la parada, `textoAltura` la pone en la línea de país
    («el río pasa a 161 m sobre el mar») y `fraseAltura` en la lectura de Adulto. Es la altura del cauce, no la del
    pueblo (Juan Viñas está a 1 160 m y el Reventazón pasa a 860): se dice «el río pasa a».
- Zonas (`ZONAS`; hoy solo `cr`, Costa Rica): los ríos con `zona:'cr'` no se tocan en el mapa mundial, donde un
  marcador dorado abre la vista de zona (`verZona`, `S.zona`) con sus ríos tocables y etiquetados y el botón
  ‹ Mundo; el ancho mínimo de vista es 3 unidades para ríos de zona (20 para los del mundo), y dentro de sus cuencas
  la costa, los lagos y las fronteras vienen de Natural Earth 10 m con tres decimales. Los distractores de las
  preguntas se toman primero de la misma zona (`otrosRios` y los mares). En la lista del inicio van en su propio
  grupo, «Ríos de Costa Rica». `continente` hace de etiqueta de región («Guanacaste», «Frontera con Nicaragua»).
- Pasaporte (`P.sellos[río:i] = fecha`): al llegar a una ciudad (`paso`), el sello se gana solo si la guía «¿cuál
  es la próxima parada?» se acertó al zarpar (`S.llaves[i] === true`, la misma llave del mercado); si no, la página
  lo dice sin regañar y se puede volver a bajar el río a ganarlo. Es dorado (`selloOro`) cuando la tarjeta
  `ciudad:ID:i` está en caja ≥ 3. `completo(r)` = todos los sellos → el río va en dorado en el mapa mundial y en la
  zona (clase `hecho`) y la fila del inicio dice «completo». Pantalla `pasaporte` (`verPasaporte`,
  `renderPasaporte`): resumen, y por río sus sellos y los huecos vacíos. Va en el JSON de exportación como el
  resto de `P`. Cada sello (`sello(r,i)`) es un SVG con carácter propio y estable: un hash de `río:parada` elige
  la forma (`FORMAS`: círculo, óvalo, cuadrado, hexágono, octógono, escudo), la inclinación (`--rot`), el desgaste
  del aro interior (`DESGASTES`) y la tinta (verde o verde medio; ocre con estrellas si es de oro); lleva el río y
  el país en el aro (`textPath`), el primer pictograma de la ciudad en tinta, el nombre y la fecha. El hueco vacío
  conserva la forma en punteado gris.
- Leitner: cajas 0-5, intervalos [0,1,3,7,14,30] días. Tarjetas por río: `rio:ID:orden|antigua|moderna|mar`
  y `ciudad:ID:i`. Entran al repaso al terminar un descenso (`sembrar`, que las marca `nuevo`) o al jugar (`marcar`).
- Hoy (`colaHoy`, bloque «Hoy» en el inicio con `renderHoy`): las vencidas ya repasadas entran todas; las nuevas
  (sembradas y nunca respondidas) entran de a `NUEVAS_POR_DIA` (10) por día: `P.dia = {fecha, nuevas}` cuenta las
  que estrenaron hoy (`marcar` quita la marca `nuevo` y suma) y `diaHoy()` reinicia al cambiar la fecha. La cola
  intercala ríos (una tarjeta por río y ronda) y el repaso toma las primeras 10 en ese orden. El bloque dice
  cuántas, unos minutos (15 s por tarjeta), qué ríos, y cuántas nuevas esperan turno (`nuevasEnEspera`).
- Interruptor Niño/Adulto (`P.modo`: `mercader` = Niño, `historia` = Adulto; `esNino()`): gobierna la economía
  (mercado o carga fija), la densidad del texto (en Niño la ruta antigua, la moderna y el dato de cada ciudad van
  plegados en `<details class="mas">` «Contame más» vía `mas()`) y la voz (`P.voz`: `auto` lee sola en Niño,
  `boton` solo a pedido; en Adulto nunca lee sola). El animal acompaña igual en los dos modos: en el globo con sus
  líneas de hola, parada y mar, y sobre la barca. Se probó callarlo en Adulto y el resultado era que aparecía y
  desaparecía; la prueba «animal siempre presente» recorre todos los ríos en ambos modos y falla si falta.
- Economía (modo Mercader): 10 monedas y bodega de 3 por descenso; precio = base × (1 + 0,5 × puertos bajados),
  ×2 en el puerto `m` ("se paga mejor en"), ×1,25 en el último puerto, 0 si `d` puertos ya pasaron (se pudre).
  El mercado de un puerto solo permite comprar si se acertó "¿cuál es la próxima parada?" al zarpar
  (`S.llaves`). Ganancia → `P.tesoro`; rangos en `RANGOS`. `fantasma(r)` simula un mercader que vende todo al
  final e ignora los mejores puertos: es el número a batir.
- Preguntas (`preguntaTipo`): ciudad (¿junto a qué río?), imagen (la mnemónica con el nombre tapado por
  `sinNombre` → ¿qué ciudad?), cerca, siguiente, frase (las tres marcan la tarjeta `orden`), antigua, moderna, mar
  y pais (sin tarjeta), y altura (¿en cuál de estas paradas pasa el río más alto?: cuatro paradas con la más alta
  al menos 25 m y un 15 % por encima de la segunda; si no hay diferencia clara, cae a `cerca`; sin tarjeta; entra
  al reto mundial y alterna con `cerca` en el reto del río). El repaso alterna ciudad/imagen para la misma tarjeta `ciudad:ID:i`.
- Eventos entre puertos (ambos modos): al zarpar hacia la parada `tramo` (`paso(1)`) salta el evento de
  `EVENTOS[id]` si no se vio en este descenso (`S.eventosVistos`); la barca se detiene a mitad del tramo
  (`S.evento.medio = puntoMedio(...)`: `{k, pt}`, el punto interpolado sobre `curso` a mitad de los km del tramo, para
  que no caiga sobre la parada cuando dos paradas son vértices consecutivos) y el panel muestra `renderEvento`. Se
  resuelve con una pregunta de
  `preguntaTipo` según `reto`: imagen → una ciudad ya vista al azar, ruta → 'siguiente' tras la próxima parada,
  pais → país de la próxima, frase, mar. Marca la tarjeta Leitner que corresponda y, en Mercader, +2 monedas al
  acertar y −2 al fallar (nunca por debajo de 0). `continuarEvento()` completa el tramo desde el punto medio
  (`S.viaje.medio`). Sin temporizador a propósito: la prisa castigaría al que lee despacio, no al que no recuerda.
  El mercader fantasma no enfrenta eventos: acertarlos es la ventaja de quien recuerda.
- Luz y clima (`ambiente(foco)` al final de `renderMapa`): dos capas sobre el mapa, `#luz` y `#clima`, sin
  eventos de puntero. La luz va por `foco.frac`: `data-luz="amanecer"` (dorado, se apaga hacia el 40 % del río),
  nada en medio, `data-luz="atardecer"` (teja y dorado desde el 60 % hasta el mar); `data-mar="vivo"` en `#mapa`
  mece el patrón del mar cerca de la boca. El clima sale del icono del evento activo (`CLIMA_ICONO`: 🌫️ niebla,
  🌪️ arena, 🌧️ lluvia, 🌊 y 🌬️ oleaje) o de `clima` explícito en el evento, y dura hasta «Seguir». Todo CSS;
  con `prefers-reduced-motion` no hay animación. En el inicio y el pasaporte `#arriba.portada` hace el mapa más alto.
- Audio: ruido rosa filtrado (Web Audio), sin archivos; `audio.ping` para monedas. Solo arranca con un gesto del
  usuario (botón ≈).
- Voz (`voz`, botón 🔊 en el globo del animal, para quien todavía no lee): `lectura()` arma por pantalla la lista de
  frases a leer desde `S` (la frase del animal, nombre y país de la parada, la imagen, la pregunta y las opciones
  numeradas «primera, segunda…» para tocar por posición; en Historia también el dato), `paraVoz` limpia el texto
  para el sintetizador (HTML, «6 650 km» → «6650 kilómetros», siglos en romanos, «a. C.», el «___» de la imagen) y
  `voz.leer()` habla con `speechSynthesis` del navegador, una `SpeechSynthesisUtterance` por frase, prefiriendo
  es-CR y luego es-MX, es-US, es-419 (sin red evita las voces «en línea»). Tocar de nuevo calla; cada `render()`
  calla; el agua baja de volumen mientras habla (`audio.duck`). Sin archivos de audio: no pesa. El botón está en el
  globo y, si no hay globo (Adulto, reto, repaso), en la línea de encabezado (`botonVoz()`, con la marca `GLOBO`
  que `render()` reinicia). Con `leeSola()` (Niño + `P.voz` ≠ `boton`), `render()` lee toda la pantalla al
  cambiar de pantalla (`voz.decir(lectura())`) y solo la reacción del animal (`dichoActual()`) al responder.

## Esquema de datos

RIVERS[]: `id, nombre, continente (o región, en los ríos de zona), zona? ('cr'), longitud (km), mar (etiqueta), marEn (con artículo), nace, naceNota, antigua,
moderna, pistaAntigua (sin nombres propios), pistaModerna, frase ("[M]i [S]obrino…": corchetes = iniciales),
fraseNota?, curso [[lat,lon]…] de la fuente al mar, brazos? [[[lat,lon]…]], ciudades [{nombre, pais, pos:[lat,lon],
imagen (mnemónica absurda ≤35 palabras), dato, escena [3-4 pictogramas]}]`, más `escenaNace` y `escenaMar` por río. Cada ciudad debe caer cerca de un vértice de `curso` y en
orden: `c.idx` y `c.km` se calculan al cargar. Mínimo 4 ciudades; 5-7 es lo cómodo. `curso` y `brazos` salen de
Natural Earth por `tools/cauces.py` (no editarlos a mano): cauce de la fuente al mar, 60-250 vértices con dos
decimales y un vértice proyectado frente a cada ciudad; los brazos son afluentes reales o, donde Natural Earth
50 m no los trae (Mosela, Meno, Tonlé Sap), listas de puntos a mano dentro de `CAUCES`.

NAVES[id]: `nombre, tipo (latina|junco|vapor|balsa|canoa|barcaza|cuadrada → glifo en el mapa), desc, zarpe,
llegada, puertos [[texto, carga]] (uno por ciudad, en orden; la última carga es "vendida")`.

MASCOTAS[id]: `nombre, especie, emoji, glifo, hola, mar, paradas[]` (una frase por ciudad, tono para niño, ≤25 palabras).
`glifo` es la clave en `ANIMALES` (motor.js): un SVG por especie (viewBox -14 -14 28 28, mirando a la derecha; partes
`cuerpo` verde claro, `claro`, `oscuro`, `acento` dorado, `bigote`, `dientes`, `rabo`, `pata`); `animal(m)` lo
dibuja en el globo, la lista, el pasaporte y la barca; el emoji queda de respaldo si no hay glifo.

MERCADOS[id]: `[{n: nombre, e: emoji, o: puerto de origen (índice), b: precio base, d?: puertos antes de
pudrirse, m?: puerto donde se paga doble}]`. Cada puerto salvo el último debería ofrecer algo.

EVENTOS[id]: `[{tramo (parada de llegada, 1..n+1; n+1 es el mar), icono (emoji), titulo, texto (la situación, con
un hecho real del tramo), reto (imagen, tramo ≥ 2 | ruta, tramo ≤ n-1 | pais, tramo ≤ n | frase | mar), bien, mal
(desenlace corto, amable; sin mencionar monedas: se agregan solas)}]`. Uno o dos por río, un tramo por evento,
anclados a algo verificable del lugar (cataratas, frontera, niebla, hielo) y con un animal que no sea la mascota.

### Para agregar un río

1. Objeto en `rios.js` con 5-7 ciudades y coordenadas verificadas y un `curso` provisional de unos pocos vértices;
   luego el río en `CAUCES` de `tools/cauces.py` (nombres de los tramos de Natural Earth, `desde`/`hasta`, y
   `cabeza`/`cola` a mano donde el dato no llega) y `npm run cauces`: en su salida, cada ciudad debe quedar a
   ≤ 0,25° del cauce (el test lo exige). Si Natural Earth 50 m no lo trae, `capa:'ne10na'` (Norteamérica),
   `'ne10'` (global) u `'osm'` (OpenStreetMap; ampliar `OSM_Q`), con `dec:3`, `simpl` y `tol`/`puente` finos como
   en los ríos ticos; un río chico lleva `zona` para que el mapa se acerque y la costa sea de 10 m (`npm run mapa`).
2. Frase acróstica con las iniciales entre corchetes; imagen mnemónica y `escena` (3-4 claves de `PICTOS` o
   `animal:`) por ciudad, `escenaNace`/`escenaMar`; `pistaAntigua` y
   `pistaModerna` sin nombres que delaten el río.
3. NAVES, MASCOTAS (animal real del río) y MERCADOS con el mismo número de puertos que ciudades; uno o dos
   EVENTOS anclados a un tramo real, respetando los límites de `tramo` por reto.
4. `npm test` (valida conteos, acrósticos, preguntas), `npm run mapa` si el río cae fuera de las cuencas ya
   cubiertas por la costa fina, `npm run relieve` (franjas, nombres y perfil del río nuevo; revisar las alturas
   que imprime), `npm run verificacion` y revisar las líneas nuevas.

## Pendientes, en orden de valor

1. Inmersión, lo que queda de la evaluación del 2026-09-04: retos sobre el mapa («tocá dónde queda…», que pagan
   memoria espacial) y paisaje sonoro por tramo sintetizado. (La bitácora imprimible se descartó.)
2. Más ríos de Costa Rica: Pacuare y Sixaola están en Natural Earth 10 m Norteamérica (`capa:'ne10na'`) pero casi
   no tienen pueblos a la orilla (Tres Equis y la barra; Suretka, Bribri y Sixaola): habría que armar paradas con
   sitios (rápidos, reservas, puentes) y verificarlos. Los demás ríos saldrían de OpenStreetMap ampliando `OSM_Q`.
3. Más eventos: hoy hay 40, dos por río salvo el Danubio y el Níger (tres). Cada uno con un hecho real detrás.


## Reglas de trabajo

- Cambios pequeños y probados. Si tocás datos, corré `npm run verificacion` y leé lo que cambió.
- No agregar dependencias de ejecución. Herramientas de desarrollo (shapely, node) sí.
- Mantener `dist/cauces.html` por debajo de ~500 KB (tope subido de 400 a 500 el 2026-09-04 para el relieve; hoy ≈ 460 KB).
- Textos para niño: frases cortas, concretas, sin sarcasmo; el animal nunca regaña.
- Accesibilidad mínima: botones reales, `aria-label` en iconos, `prefers-reduced-motion` respetado.
