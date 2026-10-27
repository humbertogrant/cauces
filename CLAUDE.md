# Cauces

Juego HTML de un solo archivo para aprender los grandes ríos del mundo: cada río es un palacio de la memoria
que se baja de la fuente al mar, ciudad por ciudad, con un acróstico, imágenes mnemónicas, una barca, un animal
guía, un mercado de trueque y repaso espaciado (Leitner). Dos audiencias, con un interruptor Niño/Adulto: sus
hijos (Niño, por defecto: mercader, textos plegados, voz que lee sola) y Humberto (Adulto: historia completa y carga
fija). El animal acompaña igual en los dos modos. Idioma: español de Costa Rica, voseo, sin jerga sin explicar.

Desde el 2026-09-04 el motor juega **rutas** de paradas (tipo `rio`, `derrota` o `itinerario`; ver `docs/itinerarios.md`)
y hay un segundo juego con el mismo motor y la misma identidad: **Exploradores** (`dist/exploradores.html`), viajes de
exploradores y conquistadores etapa por etapa, para niños y adultos. El primer itinerario es Ibn Battuta (1325-1354).
Los ríos se convierten al esquema de ruta al cargar (`desdeRio`); ningún texto de Cauces cambió con la migración y una
instantánea de 200 pantallas (`test/instantanea.js`) lo vigila. Exploradores trae nueve rutas: Ibn Battuta, Marco Polo,
Alejandro Magno y Hernán Cortés (itinerarios, los dos últimos con `conquista:true`) y Zheng He (tipo `travesia`, la ruta
marítima que el diseño llamaba «derrota»; se evitó esa palabra porque para un niño es «perder») y Odiseo (travesía de mito: nueve escalas de Troya a Ítaca según
la tradición que ubica el poema; sin años, con «año 1 del regreso» en el kicker). Desde el 2026-09-07 los viajes juegan
con otra unidad de memoria que los ríos: no la parada en orden fino, sino el tramo, el rumbo y la escala (ver «Viajes»). El 2026-09-07 entraron también Napoleón (la campaña de Rusia de 1812,
conquista; todo en un año, con fechas con mes), Humboldt (1799-1804, en canoa) y James Cook (1768-1771, travesía que da la
vuelta al mundo y cruza el antimeridiano: `antimeridiano:true`).

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
5. **Identidad visual de La Ruta** (rediseñada el 2026-09-06 a pedido de Humberto). El verde oscuro #0F423A es tinta,
   no fondo: títulos, botones y énfasis. El panel es papel cálido #FAF7F1 y el mapa (mar #0C3A33 con patrón seigaiha,
   tierra #215A4F) la única superficie oscura: ese contraste es la firma. Dos tipos de bloque en todo el juego: la voz
   (burbuja del animal, fondo #E9F3EE, siempre igual) y la ficha (tarjeta blanca con un solo filete #E4DFD3). El dorado
   #E8B952 solo dice «estás aquí»: río activo, barca, parada actual, paso actual; como texto sobre papel se usa el oro
   tinta #8A6A1A (iniciales de la frase). Verde claro #64C8AA para los ríos; gris #2D2D2D/#6B6B6B; rojo teja #A6472E solo
   para errores. Oswald solo en nombres de lugar y números (río en la cabecera, ciudad, kilómetros, monedas); Source
   Sans 3 para todo lo demás, dos puntos más grande en Niño (`body.nino`, 19 px). Movimiento: la barca y sus efectos, el
   oleaje lento del mar (`marea`) y una barrida de olas doradas al llegar al mar (`olear`); la luz, el clima, el salto del
   animal y el sello que cae se conservan. No cambiar sin pedirlo.

## Estructura

```
src/cabeza.html      DOCTYPE, <head>, CSS completo y esqueleto del body (cabecera + mapa SVG + panel)
src/cola.html        cierre
src/data/mapa.js     LAND, LAGOS, BORDES: paths SVG (Natural Earth 110 m fuera de las cuencas, 50 m dentro); mapa-amplia.js, lo mismo
                     con todas las rutas y tres veces más fino, para la edición amplia (python tools/mapa.py cauces amplia)
src/data/rios.js     RIVERS: 25 ríos: 15 del mundo y 6 de Costa Rica (zona 'cr') en las dos ediciones, y 4 solo en la amplia (bloque
                     /*@amplia*/: Orinoco, Murray, San Lorenzo, Zambeze); curso y brazos los genera tools/cauces.py [ids]
src/data/naves.js    NAVES: embarcación, zarpe, llegada y carga narrativa por puerto (modo Historia)
src/data/mascotas.js MASCOTAS (animal guía por río) y VOCES (frases genéricas)
src/data/ilustraciones.js ILUSTRACIONES: los animales dibujados de memoria y pintados (WebP en base64), para la ficha y el globo (solo
                     edición amplia; GENERADO por tools/ilustraciones.py, no editar a mano; ver «Ilustraciones»)
src/data/barcas.js, bienes.js, postales.js  BARCAS (la embarcación de cada ruta, pintada, para «Tu embarcación»), BIENES (las mercancías
                     pintadas de una ruta, en el orden de su carga) y POSTALES (las de un río: el nacimiento, una por ciudad y el mar); solo
                     en la edición amplia; GENERADOS por tools/pintados.py (ver «Barcas y mercancías» y «Postales»)
src/data/mercados.js MERCADOS (bienes por río), RANGOS y voces de la economía
src/data/eventos.js  EVENTOS: pruebas entre puertos por río (tramo, reto, textos)
src/data/voces.js    VOCES (frases genéricas del compañero), RANGOS y voces de la economía: compartidos por los dos juegos
src/data/itinerarios.js  ITINERARIOS: rutas de Exploradores ya en el esquema RUTA; el trazo lo genera tools/itinerarios.py
src/data/mapa-exploradores.js, relieve-exploradores.js  mapa y relieve de Exploradores (mapa.py y relieve.py con el juego como argumento)
src/juegos/cauces.js, src/juegos/exploradores.js  JUEGO: nombre, subtítulo, tipo de ruta, clave de guardado, zonas, grupos de la lista, portada, rangos
src/data/relieve.js  RELIEVE (franjas de altura por vista), NOMBRES_RELIEVE (cordilleras, mesetas, desiertos, volcanes) y ALTURAS
                     (perfil de altura de cada cauce); lo genera tools/relieve.py; relieve-amplia.js, con todas las rutas y franjas
                     más finas, para la edición amplia (python tools/relieve.py cauces amplia)
src/motor.js         todo el motor: estado, perfiles y guardado, Leitner, preguntas, render, mapa, audio, economía, eventos, voz
build.js             ensambla un HTML por juego (JUEGOS: cauces y exploradores) y por edición (EDICIONES: económica y amplia; ver
                     «Ediciones»), cada uno con sus datos, su src/juegos/<id>.js y el motor; recorta del motor lo que el juego no usa:
                     los VOCAB de otros tipos (marcas /*@vocab:tipo*/ … /*@fin:tipo*/), y los animales, pictogramas y glifos de
                     vehículo que no aparecen en sus datos; exporta JUEGOS, EDICIONES, ensamblar y cortarEdicion para las pruebas
test/arnes.js        DOM simulado y carga de los archivos de un juego en una edición (amplia por defecto; la económica recorta como
                     build.js y carga sus generados; EDICION global); test/pruebas.js [juego] [edicion] corre test/casos.js (Cauces) o
                     test/casos-exploradores.js; test/instantanea.js compara 200 pantallas de Cauces con test/instantanea.json.gz.
                     test/dist.js [juego] [edicion] carga los <script> del HTML ensamblado y juega un poco (vigila el recorte,
                     que cada edición diga lo que es y que la amplia no pase de 5 MB; dice cuánto le queda). `npm test` corre todo: "TODO OK" tres veces (Cauces amplia y económica, Exploradores), "INSTANTÁNEA OK" y "DIST OK" cuatro veces
tools/cauces.py      genera curso y brazos de rios.js desde Natural Earth (50 m; 10 m global y Norteamérica) u OpenStreetMap; con ids
                     como argumentos, solo esos ríos
tools/mapa.py        regenera src/data/mapa.js (o mapa-<juego>.js; con «amplia» de segundo argumento, mapa-amplia.js) desde Natural Earth
                     (110/50 m; 10 m en las cuencas de zona; shapely)
tools/rutas.py       rutas y vistas de un juego para las herramientas (ruta entera o ventana por parada con cámara por tramo;
                     las vistas que cruzan el antimeridiano se parten en su lado oeste y su lado este)
tools/safari.js      prueba en WebKit (motor de Safari) con Playwright, por http y file://; ver el encabezado del archivo
tools/itinerarios.py regenera el trazo de cada itinerario a partir de puntos de paso a mano (geodésicas cada 80 km, o el paso de PASO_RUTA)
tools/relieve.py     regenera src/data/relieve.js (o relieve-<juego>.js; con «amplia», relieve-amplia.js): alturas de NOAA NCEI (ETOPO1 y
                     mosaico DEM), nombres de Natural Earth 50 m y OpenStreetMap
tools/verificacion.py genera docs/verificacion.md
tools/pintor.py      pinta cada dibujo de tools/dibujos/<clave>.py (numpy, scipy, shapely, Pillow) en un WebP de tools/dibujos/salida/;
                     `barcas [ruta…]`, `bienes [ruta…]` y `postales [ruta [i…]]` pintan las de tools/dibujos/barcas/, bienes/ y postales/
tools/pintados.py    genera src/data/barcas.js, bienes.js y postales.js con lo pintado (tools/ilustraciones.py la llama al final)
tools/peso_postales.py cuánto pesan las postales y cuánto pesaría la amplia de Cauces con todas, con cada ancho y calidad (tope: 5 MB)
tools/ilustraciones.py genera src/data/ilustraciones.js con los dibujos pintados; todavía sabe armar las de vectores de antes, desde las
                     siluetas de PhyloPic de tools/ilustraciones/ (dominio público o CC0, con autor y licencia en fuentes.json)
```

Comandos: `npm run build`, `npm test`, `npm run instantanea` (vuelve a tomar la instantánea; solo cuando un cambio de texto de Cauces es
a propósito), `npm run verificacion`, `npm run mapa`, `npm run cauces`, `npm run relieve`, `npm run itinerarios`; para la edición amplia,
`python tools/mapa.py cauces amplia` y `python tools/relieve.py cauces amplia`; para Exploradores,
`python tools/mapa.py exploradores` y `python tools/relieve.py exploradores` (los de Python
descargan Natural Earth a `tools/ne/` la primera vez; en Windows no hay `python3`: correrlos como
`python tools/….py`). Antes de dar por terminado un
cambio: `npm test` y `npm run build`, y abrir `dist/cauces.html` en un navegador (o `python3 -m http.server`).

## Ediciones

Desde el 2026-09-13 cada juego sale en dos ediciones del mismo código, y no son ramas ni forks: build.js ensambla las cuatro
salidas de la misma fuente. La **económica** (`dist/cauces.html`, `dist/exploradores.html`) pesa 500 KB o menos, es la que se
comparte y la que juega bien en cualquier teléfono; la **amplia** (`dist/cauces-amplia.html`, `dist/exploradores-amplia.html`)
tiene un tope más holgado: 5 MB (desde el 2026-10-26; Humberto: «hasta 5MB estamos bien de peso total»). Lo que solo va en la amplia se envuelve en `/*@amplia*/ … /*@fin:amplia*/` (JS o CSS, en datos, juego,
motor o cabeza; en un array la marca abarca el elemento con su coma): la económica recorta el bloque y la amplia solo quita las
marcas. Los archivos generados no llevan marcas: la amplia tiene los suyos, `mapa-amplia.js` y `relieve-amplia.js` (todas las rutas;
costas, lagos, fronteras y franjas del mundo unas tres veces más finas), y `JUEGOS.cauces.amplia` en build.js dice qué archivo
reemplaza a cuál; `python tools/mapa.py cauces amplia` y `python tools/relieve.py cauces amplia` los regeneran, y las herramientas
sin segundo argumento hacen la económica (tools/rutas.py recorta las marcas igual que build.js). Cada archivo dice qué es: `<meta name="edicion">`, `JUEGO.edicion {nombre, kb}` (lo escribe build.js tras
src/juegos/<id>.js; en src no existe, así que la instantánea no lo ve) y una línea al final de «¿Cómo se juega?»; el título de
la amplia termina en « · edición amplia». Las pruebas cargan la amplia por defecto, y `node test/pruebas.js cauces economica`
recorta la fuente como el build y carga los generados económicos (`EDICION` global para los casos que dependen de la edición);
`test/dist.js [juego] [edicion]` juega cada HTML. El pasaporte es compartido: las dos ediciones guardan bajo la misma clave (`cauces:progreso:<perfil>`) y el motor
ignora en Hoy las tarjetas de rutas que la edición abierta no trae (`colaHoy`, `nuevasEnEspera`), así que quien pasa de una a
otra conserva sellos y cajas, y el JSON exportado lleva todo. Desde el 2026-09-13 la amplia trae, además de las
costas y el relieve finos, cuatro ríos que no caben en la económica: Orinoco (caimán del Orinoco, curiara), Murray (ornitorrinco, vapor
de ruedas; estrena Oceanía en la portada), San Lorenzo (beluga, canoa de corteza; Natural Earth solo trae un tramo corto, así que la
cabeza y la cola van a mano en CAUCES) y Zambeze (elefante, mokoro). Cada uno va dentro del bloque `/*@amplia*/ … /*@fin:amplia*/`
de rios.js, mascotas.js, naves.js, mercados.js y eventos.js; sus glifos (ornitorrinco, beluga, elefante) viven en ANIMALES y build.js
los recorta de la económica. Las pruebas exigen que la económica siga con 21 ríos y que la amplia tenga el Orinoco; docs/verificacion.md
marca «solo en la edición amplia» en su título.
Un cambio que engorde la amplia dice su peso en el commit. Para congelar una versión, etiqueta de git y Release en GitHub con los
dos HTML económicos adjuntos: `economica-1` (2026-09-13) es la primera.

## Ilustraciones (edición amplia)

Desde el 2026-09-15 cada animal guía tiene, además del glifo chico, una **ilustración** (`src/data/ilustraciones.js`,
`ILUSTRACIONES[clave] = {v, c, f, i}`; caja 0 0 120 90, mirando a la derecha; `v` es el encuadre de la lámina) para la ficha «Conocé a …»
al empezar la ruta y para el globo, donde va un retrato (primer plano de la cabeza, `c.marco`) en los dos modos. El glifo sigue en el
mapa, la lista, los sellos y los iconos. Solo van en la amplia, en los dos juegos: el archivo está entero dentro de `/*@amplia*/ …
/*@fin:amplia*/` y build.js recorta las entradas de animales que el juego no usa (una por línea). La clave es el `ilus` del compañero o,
si no lo trae, su `glifo`: Boto lleva `ilus:"inia"`, Bulán `ilus:"platanista"` y Rafi `ilus:"tortugablanda"`, porque «delfin» y
«tortuga» son las de Nerea y Marea en Exploradores (`usados()` en build.js toma, línea por línea, el `ilus` si está y si no el glifo).
- **Dibujadas de memoria y pintadas pixel por pixel** (desde el 2026-09-23: Humberto vio a Bulán pintado así y pidió «dibujá de
  memoria todo el set»). Reemplazan a las de vectores sobre siluetas de PhyloPic, que quedan en `tools/ilustraciones/` sin uso (la
  herramienta todavía sabe armarlas). Son 29 dibujos: los 23 de Cauces (Buk y Bulán estrenan ilustración) y 6 de Exploradores
  (dromedario, camello, caballo, jirafa, delfín listado y tortuga verde; la lapa es la misma de Cauces). Cada animal es un archivo de
  `tools/dibujos/<clave>.py` que arma el cuerpo con piezas en la caja del juego (formas de puntos, `tubo` con radio a lo largo de un
  eje, `ovalo`) y `tools/pintor.py` lo pinta: cada masa se infla como un globo (ecuación de Poisson sobre su contorno; los `bultos`
  suben suave, para esculpir frente, mejillas o músculos), la luz sale de sus normales (arriba, adelante y de frente, como la sombra de
  antes) llevada a una rampa por material de la paleta (`cuerpo` verde claro, `vientre` más pálido, `lejos` más oscuro para lo del otro
  lado, `claro` blanco, `oscuro` tinta, `acento` dorado: un solo detalle dorado por animal), las masas de adelante echan sombra sobre
  las de atrás y cada una lleva su línea de tinta, más gruesa del lado de la sombra, que se desvanece en `raices` (donde nace una pata o
  una aleta; en las piezas delgadas también se funde el color, `funde`) y se quita con `sin_tinta` (el corte del pedúnculo sobre la cola
  de un pez). Desde la segunda pasada (2026-09-24) la luz es más de pintura: las rampas corren la sombra hacia el azul y la luz hacia el
  amarillo, un `escalon` suave separa sombra, medio tono y luz, y un filo de `contraluz` aclara los bordes de arriba; `pelaje` pinta el
  pelo con pinceladas finas que siguen su flujo (en mechones de dos o tres pelos para el pelo largo) y oscurecen o aclaran el color que
  ya está pintado; `grietas`, la red fina de la piel gruesa del elefante; y cada ojo de `CARA` lleva una `cuenca` suave. Ayudantes:
  `_perfil.py` (cuerpos largos de perfil con dos tablas, lo que sube el lomo y lo que baja la panza a lo largo de
  un eje curvo; la cola horizontal de un cetáceo, proyectada un poco desde arriba, y las aletas en paleta) y `_patas.py` (miembros,
  dedos en abanico, garras, patas de ungulado con casco o almohadilla y `peludo`: mechones en el contorno, que se acuestan hacia donde
  cae el pelo). Salida: un WebP de 680 px de ancho (la ficha mide 340) con
  transparencia en `tools/dibujos/salida/` (fuera de git) y dos vistas previas, grande y con rejilla (el ojo y la boca de caraDe y el
  marco); `python tools/pintor.py [clave…]`. `python tools/ilustraciones.py` arma el archivo de datos con las pintadas que tienen
  `LISTO = True` (las repinta si el dibujo o el pintor cambiaron) y, si faltara alguna, con la de vectores.
- **La cara no se pinta**: el ojo y la boca los dibuja caraDe (motor.js) encima de la imagen, según el ánimo, con el `CARA` del dibujo
  (ojo, k, boca, kb, giro, pb, wb, marco, inclina). De perfil, un solo ojo (lo que Humberto rechazó el 2026-09-17 fueron animales de lado
  con los dos ojos del mismo lado); de frente (el cangrejo) o desde arriba (la tortuga de caparazón blando y el ornitorrinco), dos, y la ilustración lo
  declara con `vista:'frente'|'arriba'` y `ojo2` (la prueba rechaza uno sin el otro). En el retrato, la imagen lleva el filtro SVG
  `#aro` (que viene en la misma ilustración: dilata la silueta y la pinta de verde claro por debajo) para despegarse del círculo oscuro.
  Ánimos: normal (parpadea cada 5,5 s, `.parpado`), alegre, pensativo, sorpresa y dormido, como antes (ver «Cómo está hecho el motor»).
- Cada dibujo dice en su encabezado qué rasgos de la especie dibuja, para revisarlos contra una foto. Las poses siguen las de antes
  donde calzaban con la ficha y el fondo, o cuentan lo que dice la ficha: Hipo pasta con la cabeza baja y el picabueyes en el lomo,
  Bruno come hojas sentado en su rama con la cola prensil enrollada dos vueltas en ella, Bíber roe la corteza de una rama, la lapa
  está en su rama, Valsa arquea las alas como velas, Rafi y Pico se ven desde arriba (de perfil, el pico y la cola del ornitorrinco,
  que son anchos y chatos, se veían finos y parecía un lagarto) y el cangrejo de frente. Nerea salta fuera del agua.
- Lecciones (2026-09-23): un animal macizo (hipopótamo, elefante, caballo, camélidos, jirafa) lleva las patas de este lado dentro del
  mismo volumen que el cuerpo; separadas parecen salchichas pegadas. El cuello tiene que salir del cuerpo (la bonobo tuvo la cabeza
  flotando). Un bulto que sube de golpe dibuja un disco. La cola de un cetáceo es horizontal: se dibuja su planta proyectada, no una
  cola de pez. Las patas de un cangrejo de frente se abren en abanico; paralelas parecen un peine. Una cola prensil se enrolla en la
  rama: el tramo de atrás se pinta antes que la rama y la vuelta de adelante, después.
- Lecciones de la segunda pasada (2026-09-24): el pelo pintado con un color fijo deja rayas blancas en la sombra; las pinceladas tienen
  que tomar el color de abajo. Una pieza aparte con su propio volumen y su línea se lee como un objeto pegado: la oreja de la bonobo
  parecía un segundo ojo y la «manga» del camello, una almohada; el pelo largo (barba, manga, joroba) va en el mismo volumen que el
  cuerpo, con un tono más oscuro y mechones en el contorno. Donde una aleta se funde con el cuerpo, su sombra también tiene que
  desvanecerse (si no, queda una mancha en la raíz); una pata gruesa no se funde: el muslo va en el volumen del cuerpo y de la
  rodilla para abajo, una pieza aparte (el cocodrilo). Las patas de un ungulado van por articulaciones (codo, rodilla, caña,
  menudillo, cuartilla; atrás, el muslo en cuña hasta el corvejón): rectas parecen palos. Una cara oscura (bonobo, mono congo) no
  lleva línea donde se junta con el pelo, solo donde es el borde del dibujo (`sin_tinta` con la cabeza achicada). La cola ancha del
  castor y la paleta del manatí se ven un poco desde arriba; la del manatí va en el mismo volumen que el cuerpo, más chata.
- Fichas: la `ficha` de cada compañero (un hecho de la especie, verificable) va dentro de `/*@amplia*/` en mascotas.js y en
  itinerarios.js; tools/verificacion.py lista y marca ⚠ cada frase, en Cauces y en Exploradores.
- Pesos (2026-09-24, tras la segunda pasada): cada WebP pesa de 10 a 36 KB (el pelo y las texturas suman: el cangrejo, el mono y el
  elefante son los más pesados); Cauces amplia ≈ 1 297 KB y Exploradores amplia ≈ 658 KB (antes de la pasada, 1 246 y 642). Se probó
  bajar la calidad de 84 a 80: ahorraba 44 KB entre los 29, poco para lo que se pierde. Para comparar una pasada con la anterior:
  guardar los WebP de `tools/dibujos/salida/` antes de repintar y ponerlos lado a lado (scratchpad `antes-despues.py`).
- Hojas de revisión en scratchpad/webkit: `pintados.js [--grid] [--x2] [claves]` (cada animal grande con su fondo y su cara, a tamaño
  de ficha y los cinco retratos) y `pintados-contacto.js [--x2] [claves]` (todos a 280 px con su globo), con el motor y el CSS del
  juego; `ficha-lote.js río…` y `ficha-lote-exp.js ruta…` (ficha y globo dentro del juego armado, y dicen si cada globo lleva retrato).
- **Barcas y mercancías** (desde el 2026-09-25, a pedido de Humberto: «un trabajo similar dibujando las barcas, y para una ruta, como
  prueba, las mercancías»). Cada ruta con barca tiene su embarcación dibujada de memoria según su descripción (NAVES o el vehículo del
  viaje) en `tools/dibujos/barcas/<ruta>.py`: las 25 de Cauces (la falúa del Nilo, el junco del Yangtsé, la caja de Ulm del Danubio, el
  kelek del Tigris, la balsa de pieles del Huang He, la de rafting del Reventazón…) y las 4 de Exploradores que son barcos (la flota del
  tesoro, la galera de Odiseo, la canoa de Humboldt y el Endeavour); las caravanas y los jinetes siguen con su glifo. Van de perfil, con
  la proa a la derecha, como el glifo del mapa: el casco dorado (la barca es lo tuyo), las velas claras, el metal en tinta; flotan en una
  franja de agua pintada (`agua`, en `_barcas.py`, que también trae velas, remos, cabinas, techos de paja, esteras, ruedas de paletas,
  chimeneas y humo; `_canoas.py` da cascos largos de canoa). El motor las pone arriba del bloque «Tu embarcación» (`laminaNave`, en una
  lámina blanca como la de «Conocé a …») y, si una ruta no tiene, queda el glifo chico. Las mercancías: `tools/dibujos/bienes/<ruta>.py`
  trae `BIENES`, un bodegón de 40 × 40 por cada bien de MERCADOS[ruta], en su orden y con su nombre en `clave` (tools/pintados.py lo
  exige); el mercado y la bodega los muestran a 52 px en lugar del icono de línea (`bienPintado`). Por ahora solo el Nilo: café de Jinja,
  pescado seco de Juba, goma arábiga de Jartum, dátiles de Asuán y trigo de Luxor. Todo va dentro de `/*@amplia*/` y build.js deja en
  cada juego solo las de sus rutas. Pesos: una barca, de 17 a 52 KB de WebP (la vela, el aparejo y el agua pesan; 907 KB las 29) y un
  bien, de 4 a 8 KB; con ellas, Cauces amplia pasó de ≈ 1 297 a ≈ 2 321 KB y Exploradores amplia de ≈ 658 a ≈ 892 KB (2026-09-25). La
  económica no cambia ni un byte: en la plantilla del motor, las marcas `/*@amplia*/` rodean todo lo agregado.
- Lecciones de las barcas (2026-09-25): una pieza recta (una cabina, un fardo, una vela cuadrada) se redondea con `caja` o `poli`, no con
  `forma`: el redondeo de Chaikin vuelve octógonos los rectángulos y globos las velas. Un casco de canoa necesita la quilla redonda que
  sube hasta cada punta (`_canoas.canoa`): con fondo chato y las puntas cortadas parece una cuña. Una carga chica (un racimo de bananos,
  unos plátanos) no se lee a este tamaño: mejor lo que tiene silueta propia (una piña, un saco, un barril). Un montón (la goma arábiga)
  va apretado y dentro de su cuenco: el borde del cuenco se pinta después, delante de los trozos de abajo.
- **Postales** (desde el 2026-09-25, a pedido de Humberto, con el Tigris como prueba: «dale, hacé el Tigris completo»). La postal de cada
  parada deja de ser una fila de pictogramas genéricos y pinta la imagen para recordar de la ciudad, que es lo que el jugador tiene que
  retener, con lo que dice su dato: en el Tigris, los montes Tauro con dos ríos jóvenes (el Tigris y el Éufrates, su gemelo), las
  murallas negras de Diyarbakır y el puente de los Diez Ojos, un toro alado de Nínive bajo una tela de muselina en Mosul, el sol hecho
  reloj sobre la ciudadela de Tikrit («un tic-tac de 800 años»), la Malwiya de Samarra, la ciudad redonda de Bagdad con la biblioteca
  en el centro y el río de tinta con libros flotando, el barco de Simbad en Basora y el golfo al atardecer con un petrolero y un faro.
  El 2026-09-26 siguió el Volga («hagamos las postales del volga»): el pantano de Valdái con la capillita de madera sobre el manantial
  (de memoria: revisar contra una foto), el río angosto bajo un puente de un solo arco en Tver, el oso del escudo de Yaroslavl de pie
  con el hacha dorada al hombro (la leyenda del príncipe que lo mata se cuenta con el escudo, no con la pelea), una balanza gigante de
  la feria de Nizhni Nóvgorod que pesa un cajón de té contra un atado de pieles frente al Kremlin de ladrillo, el caldero que hierve
  dentro del Kremlin de Kazán con la mezquita Kul Sharif y la catedral, el río hecho anzuelo alrededor de las montañas de Zhiguli en
  Samara, la Madre Patria con su espada sobre la colina de Volgogrado, el gorro de astracán y la lata de caviar en un muelle del delta, y
  el Caspio con juncos, lotos y un pesquero. El 2026-10-25 entró el Nilo, ya con la regla del protagonista (ver abajo): el Nilo Blanco,
  claro, y el Nilo Azul, oscuro, que nacen de sus lagos y bajan hacia nosotros; el jinete que salta a caballo desde el lago Victoria en
  Jinja; el bebé con chupón y banderita de estrella en su canasta, frente al muelle de Juba; las dos jarras que vacían agua blanca y
  azul en el mismo cauce en Jartum; la barrera a rayas de la aduana que cruza el río en Asuán, con la Presa Alta al fondo; la máscara de
  oro en la orilla de las tumbas de Luxor, con el sol que se pone, y Karnak en la de los templos; el delta de El Cairo abierto en
  abanico, con la letra Δ en dorado; y la falúa que sale al Mediterráneo. Ese mismo día, a pedido de Humberto («reparemos las
  existentes y dale con el amazonas»), el Tigris y el Volga pasaron a la regla (en Diyarbakır la muralla negra se curva alrededor del
  río; la Malwiya es dorada, como un cono de helado; el reloj de Tikrit, el toro alado, el barco de Simbad y el faro, al medio; los libros
  de Bagdad, abiertos y echados en el agua; el puente de Tver, la balanza de Nizhni y la Madre Patria, grandes; el anzuelo de Samara, en
  J; en Astracán, un mercader con su gorro de astracán que muestra la lata de caviar) y entró el Amazonas: el nevado Mismi con su
  glaciar, alpacas y un cóndor; el taxi dorado que flota en Iquitos, con un delfín rosado y una avioneta; las tres vecinas que se dan la
  mano en Leticia; las dos manos, oscura y café con leche, que se buscan sin tocarse sobre el encuentro de las aguas en Manaos; el santo
  de aureola que maneja un camión de soya en Santarém; la estrella de Belén sobre el estuario y el mercado Ver-o-Peso; y el regatão que
  sale al Atlántico entre manglares. En los mares, la protagonista es la barca del juego, con su casco dorado (la falúa del Nilo, la
  lodia del Volga, el regatão del Amazonas), salvo en el Tigris, cuyo kelek se desarma en Bagdad: su mar tiene el faro. El 2026-10-26
  siguieron el Yangtsé y el Misisipi («sigamos»): el Jinsha, «arenas doradas», trenzado sobre su banco de arena dorada, con yaks; la
  ciudad vertical de Chongqing en su cerro, con el tren dorado que atraviesa un edificio, la niebla y una olla de hotpot; el río que
  choca contra la presa de las Tres Gargantas en Yichang y hace «¡chan!», con un estallido dorado de historieta; el puente de Wuhan con
  su W de acero dorada; la puerta Ming de Nankín con su techo dorado, reflejada entera en el río como en un espejo, y una rosa de los
  vientos con el sur lleno; los rascacielos de Shanghái «sobre el mar», con las esferas doradas de la Perla Oriental; el junco que sale
  al mar entre grúas. En el Misisipi: un niño de gorra dorada que cruza el río recién nacido por las piedras del lago Itasca; el muñeco
  de masa que amasa junto a las cataratas de Mineápolis, con panes dorados; el Gateway Arch de San Luis, que enmarca el sol que se pone
  en el Oeste; un cantante de copete y traje dorado con una guitarra hecha de un capullo de algodón, frente al puente en M de Memphis;
  el bastón clavado en la orilla de Baton Rouge (dorado, como todo lo que hay que recordar, aunque la frase lo diga rojo: el rojo del
  juego es solo para los errores), con las chimeneas de las plantas enfrente; la trompeta dorada que sale del agua en la media luna de
  Nueva Orleans; y el vapor de rueda que sale al golfo de México, con pelícanos. Ese mismo día siguieron el Danubio y el Rin («sigamos
  con el Danubio y el Rin»): la fuente del Danubio en Donaueschingen, un estanque redondo de baranda dorada, entre los abetos negros de la
  Selva Negra; una U dorada con la torre de la catedral de Ulm adentro, y una caja de Ulm en el río; una rata dorada que cruza el Puente
  de Piedra de Ratisbona; el Inn verde, el Ilz negro y el Danubio azul que se juntan en Passau, vistos desde arriba, con una pelota
  dorada que se pasan; la tarta Linzer con su enrejado, en la orilla de Linz; una pareja que baila el vals sobre el río café de Viena,
  ella de vestido dorado; dos hermanos de camiseta dorada que señalan Viena y el castillo de Bratislava; las cadenas doradas del Puente
  de las Cadenas entre Buda y Pest; el Vencedor dorado en su columna, en la punta de Belgrado donde el Sava entra al Danubio, con la
  fortaleza blanca; y los pelícanos blancos de bolsa dorada en el mar Negro, oscuro como su nombre (la caja de Ulm no llega al mar: se
  vende como leña). En el Rin: los Alpes suizos con la nieve dorada del pico de donde baja el río, el lago de Constanza y las cataratas
  de Schaffhausen con su roca; una escuadra dorada en el codo de 90° de Basilea; la catedral rosada de Estrasburgo dentro del círculo de
  estrellas doradas de Europa; los tipos de imprenta que flotan en Maguncia y dicen BIBLIA; el jinete dorado de la Esquina Alemana, en
  Coblenza; el frasco del agua de colonia, dorado, delante de las dos torres de la catedral de Colonia; un garaje con una grúa dorada en
  cada lugar, en Duisburgo; una bandera blanca en su asta dorada, clavada en el río, en Rotterdam; y una veleta dorada con la N del norte
  en el dique del mar del Norte, frío y gris (la barcaza del Rin no ve el mar). Siguieron el Ganges y el Mekong («sigamos con el Ganges
  y el Mekong»): Gaumukh, «boca de vaca», hecha una cara de vaca de hielo con los cuernos dorados, que escupe el río por la boca de la
  cueva; la puerta dorada de Haridwar por donde el río sale de la montaña, con las lámparas que flotan; un perro con cuatro zapatos de
  cuero dorados frente a las curtidurías de Kanpur; la trenza de tres aguas de Prayagraj (el Saraswati, invisible, es solo un borde de
  puntos), atada con una gomita dorada, entre la multitud del Kumbh Mela; el fuego dorado al pie de los ghats de Benarés, con el sol
  pálido del amanecer; el león de Ashoka, dorado, que planta la pata frente a la empalizada de Pataliputra en Patna; el puente Howrah,
  dorado, la última puerta de Calcuta; y el tigre de Bengala, dorado, en los manglares de los Sundarbans (la barca se queda en el
  Hooghly). En el Mekong: un chorten de punta dorada con sus banderas de oración en la meseta tibetana; un elefante dorado con una torta
  de té pu'er en la trompa, en Jinghong; la fila de monjes de túnica dorada que reciben arroz al amanecer en Luang Prabang; la estupa
  dorada del Pha That Luang con el viento manso y una cometa en Vientián; el lago Tonlé Sap con forma de pulmón, con sus bronquios y una
  flecha dorada de ida y vuelta, en Phnom Penh; el mercado flotante de Can Tho con sus sombreros cónicos dorados; y los nueve dragones
  dorados que salen al mar de los nueve brazos del delta (la cola larga se queda en el delta). Siguieron el Níger y el Paraná («sigamos
  con el Níger y el Paraná»). El Níger es un bumerán (naceNota y frase) y su bumerán dorado atraviesa la serie: sale volando de las
  tierras altas de Guinea, de espaldas al Atlántico; es la punta, echado sobre la curva del río, en Gao, junto a la tumba de los Askia;
  y vuelve a la costa en el mar (la pinaza no sale al golfo). En el medio: tres cocodrilos dorados en la orilla de Bamako; la ciudad de
  barro dorado de Mopti, con su mezquita, reflejada en los canales, y las piraguas taxi; en Tombuctú, el camello con la sal, el cesto de
  oro y, al medio, el manuscrito abierto de cantos dorados; en Niamey, un poste dorado con dos flechas que dicen lo mismo, NÍGER (el
  país y el río), y una jirafa; en Lokoja, un policía de tránsito de uniforme dorado que dirige el cruce loco del Benue, con el río
  juntado el doble de ancho; y en Port Harcourt, de noche, las llamas de gas doradas entre los manglares y las torres de petróleo. En el
  Paraná: la suma dorada del nacimiento (Paranaíba + Grande = Paraná, con sus represas y sus campos); las cataratas del Iguazú y la
  represa de Itaipú lado a lado, con un arcoíris dorado entre los dos muros, en Foz do Iguaçu; las ruinas de piedra roja de la misión
  de Trinidad, con su campana dorada, frente a Yacyretá, en Encarnación; un acordeón dorado de chamamé donde se juntan las dos
  corrientes, en Corrientes; la bandera argentina, con su sol de mayo dorado, sobre los silos de soya de Rosario; un león dorado echado
  en el río color de león, frente al Obelisco de Buenos Aires; el vigía de camisa y catalejo dorados, en la cofa, que ve el Cerro de
  Montevideo; y un cofre de plata, de herrajes dorados, que flota en la boca del Río de la Plata (el lanchón no llega al mar).
  Siguieron el Indo y el Congo («sigamos con el Indo y el Congo»). En el Indo: el Kailash dorado, con sus gradas de roca y sus vetas de
  nieve, reflejado en el lago Manasarovar; en Leh, el hilo verde de álamos a lo largo del río, entre montañas ocres, que una aguja
  dorada va cosiendo; en Skardu, una K dorada delante del K2; en Attock, el puente de barcas dorado con un jinete que lo cruza y el
  fuerte de Akbar; en Sukkur, una regadera dorada delante de la presa de muchas compuertas; en Hyderabad, los techos llenos de torres
  de viento doradas; en Karachi, el río seco que termina en una llave de agua dorada que apenas gotea, con la ciudad enorme atrás; y en
  el mar Arábigo, los números arábigos dorados (1, 2, 3) que flotan (la barca se queda en el delta). En el Congo, juegos de sílabas: la
  cruz de cobre de Katanga, dorada, en la meseta donde nace el Lualaba; la vaca (Bu-kama) dormida en su cama flotante entre papiros; el
  kínder (Kin-du) de barcacitas doradas que suben al tren; el pescador wagenia que le tira un beso (Kis-angani) a la catarata desde su
  andamio de nasas; la banda (M-banda-ka) de uniforme dorado que da el paso sobre la línea del ecuador; el boxeador con corona
  (Kin-shasa) que cruza en balsa entre Kinshasa y Brazzaville; la mata de piedras doradas (Mata-di) debajo del puente colgante; el
  baobab dorado con gorra y bigote de capitán (Bo-ma); y la lengua de arena de Banana, donde el Congo entra al Atlántico, hecha un
  plátano gigante dorado con su faro (el convoy se queda en Boma). Siguieron el Huang He y el Orinoco («huang he y orinoco»). En el
  Huang He: el río que nace ya dorado de barro entre los lagos Gyaring y Ngoring, el río Amarillo; el lanchón cargado de fideos dorados
  de Lanzhou, hebra por hebra, bajo el puente de hierro; el yin y el yang de arroz, mitad dorada y mitad verde, en el desierto de
  Yinchuan; el bao de acero dorado en lo alto de la curva de Baotou; el zapato de bronce del kilómetro cero de Zhengzhou, entre las vías;
  el río dorado que pasa por arriba de los techos de Kaifeng, entre diques, sobre las ciudades enterradas; el genio dorado que sale del
  manantial de Jinan; la campana dorada que suena sobre el delta nuevo de Dongying, entre los pozos que cabecean; y el penacho dorado de
  barro que se abre en el golfo de Bohai (la balsa de pieles se deshace en el delta). En el Orinoco, el primero de los ríos que solo están
  en la amplia: el Casiquiare dorado, el canal por donde el Orinoco le presta agua al río Negro y al Amazonas; Fernando, que sirve té
  negro de una tetera dorada en tazas de arena blanca, en San Fernando de Atabapo; los raudales que gritan ¡AY! y las curiaras doradas
  que se bajan a caminar en Puerto Ayacucho; el carro dorado con su carreta y la meta a cuadros pintada atrás, en Puerto Carreño; el
  caimán dorado que dobla el río con la cola en Caicara; Bolívar, de casaca dorada, que aprieta el río bajo el puente de Angostura, con
  la botella de amargo; la guayaba de acero dorada en el muelle de Ciudad Guayana, junto a los dos ríos que no se mezclan; y el delta
  abierto como un abanico dorado de caños hacia el Atlántico (la curiara se queda en los caños). Después, los otros tres ríos de la
  amplia («murray san lorenzo y zambeze»), con lo que quedan pintados los diecinueve del mundo. En el Murray: un canguro dorado que salta
  en la nieve de los Alpes Australianos; el ornitorrinco dorado en la cama de arriba de la cucheta del albergue (Albury); el eco dorado
  del silbato del vapor que rebota contra el muelle altísimo de Echuca; de noche, la colina de cisnes negros de pico dorado y la carpa de
  Mitchell, que no lo dejan dormir (Swan Hill); la naranja dorada que hace de sol sobre los naranjales de Mildura; el marinero que le
  pone etiqueta a cada uva dorada en Renmark; el puente dorado que le hace cosquillas al río con los pies en Murray Bridge; la gaviota
  que cierra la última compuerta dorada de Goolwa; y la draga dorada que mantiene abierta la boca, entre las dunas y los pelícanos (el
  vapor se queda ante las barreras). En el San Lorenzo: el embudo dorado por donde se vacía el lago Ontario; el rey de manto dorado y
  corona de hielo en la boca del lago (Kingston); la vaca dorada que empuja la compuerta de la esclusa (Cornwall); el monte Royal con su
  sombrero de nieve y su corona dorada que mira saltar las canoas en los rápidos (Montreal); el barco de papel de diario, dorado, donde
  se juntan los tres brazos (Trois-Rivières); el diamante dorado que angosta el río bajo el cabo y el Château Frontenac (Quebec); la beluga
  que toca un tambor dorado en la boca del Saguenay (Tadoussac); y la cola dorada de una ballena entre los témpanos del golfo (la canoa
  se queda en el Saguenay). En el Zambeze: la primera gota, dorada, sobre el manantial del bosque de miombo; el mono rey dorado que rema
  en la barca a rayas sobre la llanura inundada (Mongu); la gata dorada que mima al mulito que apaga el fuego (Katima Mulilo); el león
  dorado bajo el humo que truena (Livingstone); la caja dorada que guarda el río, con los botes que rescatan animales (Kariba); la pava
  dorada que hierve sola sobre el puente colgante, con el carbón debajo (Tete); el chinchorro dorado del capitán inglés entre dos
  manglares (Chinde); y la mano dorada de un cartel que apunta con el índice al Índico (el mokoro se queda entre los manglares).
  Por último, los seis ríos de Costa Rica («vamos con los ríos ticos»), con lo que quedan pintadas las 201 postales de Cauces. En el
  Tempisque: el árbol de guanacaste dorado, el que le da nombre a la provincia, en el llano seco al pie del volcán Orosí; un sabanero de
  camisa blanca y una vaca cebú, los dos con su sombrero dorado, frente a las casas blancas de Liberia; el guardia de uniforme dorado,
  con el machete al hombro, que cuida el puente (Guardia); el queso crema gigante, de papel dorado y con su cuchillo de untar, que flota
  con sombrero de paja entre los arrozales (Filadelfia); el bolsón dorado lleno de mazorcas que pasa del muelle al bongo (Bolsón); las
  ollas doradas de arroz cuyo humo tapa el muelle, frente a las garzas y las espátulas de Palo Verde (Puerto Humo); y el bongo de casco
  dorado que entra al golfo de Nicoya, con Puntarenas enfrente. En el Reventazón: los ríos de agua que bajan de Talamanca y del valle de
  Cartago y se juntan en el Reventazón dorado; el oso dorado que reza de rodillas en la iglesia de Orosi; la cara dorada de cachetes
  inflados que tapa el cañón y aguanta el embalse (Cachí); don Juan Viñas, de saco dorado, con su café en la banca de la estación; la
  bola de béisbol dorada, con su volcancito de sombrero, que rema en la balsa (Turrialba); el SÍ dorado que chirría sobre el cruce de
  las vías, con la represa atrás (Siquirres); la tortuga dorada con boina y paraguas que desova en la playa (Parismina); y la balsa de
  rafting de tubos dorados que sale a la barra, frente a las olas del Caribe. En el Sarapiquí: las cataratas doradas entre el Poás y el
  Barva; el arcángel dorado que se baña bajo la catarata con su paraguas (San Miguel); la virgen de yeso con el chaleco salvavidas
  dorado, que se sube a la balsa bajo el puente colgante (La Virgen); los mates dorados que cuelgan del higuerón (Chilamate); las mulas
  cansadas, doradas, que pasan del muelle al bote (Puerto Viejo); los tres botes dorados que se dan la mano entre las banderas de Costa
  Rica y de Nicaragua (Trinidad); y el bote de casco dorado que entra al San Juan, con Bruno, el mono congo, que grita en la orilla. En el
  San Juan: el río dorado que sale del lago de Nicaragua, con Ometepe en el horizonte; la pajilla dorada que vacía el lago por encima del
  fuerte (San Carlos); el sábalo de plata, de aletas doradas, que salta sobre el bote y saluda (Sábalos); Rafaela, de vestido dorado, que
  dispara el cañón desde la muralla (El Castillo); la boca dorada que se toma el río San Carlos (Boca San Carlos); la Δ dorada partida por
  el cuchillo, sobre el río que se parte (Delta); la pala dorada clavada al final del canal sin terminar, junto al pueblo gris (San Juan
  de Nicaragua); y el vapor del Tránsito, de casco dorado, que sale al Caribe, con la aleta de Tiburcio. En el Tárcoles: el Grande y el
  Virilla, dorados, que recogen el agua del Valle Central a los dos lados de la ciudad; el Fortín dorado que mira el río entre las flores
  (Heredia); el chip dorado que brilla de estrella sobre el portal, con las mulas en el puente de piedra (Belén); la balsa de troncos
  dorada en el abrazo de los dos ríos (Balsa); la oreja dorada que escucha el tren de los mangos y las sandías (Orotina); los cocodrilos
  dorados bajo el puente de los turistas (Tárcoles); y la lancha de casco dorado que sale al golfo, con Ara y otra lapa en el almendro.
  En el Térraba: el general de uniforme dorado que saluda al pie del Chirripó, porque el río nace como río General; San Isidro, de
  túnica dorada, con un cerro de sombrero; las piñas doradas que escupe el volcán (Volcán); el rey dorado que bautiza desde el puente las
  dos manos de agua (Paso Real); el rey que baila con la máscara de diablito dorada (Rey Curré); las esferas doradas que ruedan entre los
  bananos (Palmar); el conquistador con botas de hule doradas en la inundación (Ciudad Cortés); y la lancha de casco dorado, cargada de
  piñas, que sale al Pacífico entre los manglares de Sierpe. En los seis mares la barca del juego llega, según su propio dato.
  `tools/dibujos/postales/<ruta>.py` trae `POSTALES` en el orden del recorrido (clave 'nace', el nombre de cada ciudad y 'mar';
  tools/pintados.py exige que calcen con rios.js), en una caja de 120 × 40 (la postal mide 240 × 80), con los ayudantes de
  `_postal.py` (cielo, sol, tierra, río, reflejo, palmeras, árboles, cordilleras con nieve y nubes; desde el Volga, abedules, abetos,
  iglesias de cúpulas de cebolla, juncos, aves y lotos; desde el Nilo, cintas y espejos de agua, prados, orillas, pasto, papiros, selva,
  pirámides y obeliscos, y `corrido`, un lienzo que corre lo que se dibuja en él, para mover una pieza sin tocar sus números; desde el
  Danubio, `casitas` de pueblo, `piedra` arenisca y `cebolla_baja`, el chapitel de una torre barroca; desde el Ganges, `mangle`); se
  guardan en WebP sin transparencia de 600 px de ancho y calidad 75 (hasta el 2026-10-26, de 744 px y calidad 84: ver abajo). El motor
  las pone con `postal(rid, i, cls)` (i = 0 el nacimiento, 1…n cada parada, n+1 el mar) en
  la ficha del nacimiento, de cada parada y del mar, y de pista en el reto de imagen; donde un río no tiene, queda la de pictogramas,
  y el sello del pasaporte sigue con su pictograma. Pesan de 4 a 18 KB cada una (en el archivo de datos, 99 KB las ocho del Tigris,
  130 KB las nueve del Volga, 97 KB las ocho del Nilo, 73 KB las siete del Amazonas, 77 KB las siete del Yangtsé, 81 KB las siete
  del Misisipi, 143 KB las diez del Danubio, 111 KB las nueve del Rin, 112 KB las ocho del Ganges, 99 KB las siete del Mekong, 93 KB
  las nueve del Níger, 75 KB las ocho del Paraná, 93 KB las ocho del Indo, 101 KB las nueve del Congo, 91 KB las nueve del Huang He,
  71 KB las ocho del Orinoco, 100 KB las nueve del Murray, 63 KB las ocho del San Lorenzo, 83 KB las ocho del Zambeze, 78 KB las
  siete del Tempisque, 102 KB las ocho del Reventazón, 87 KB las siete del Sarapiquí, 79 KB las ocho del San Juan, 98 KB las siete del
  Tárcoles y 107 KB las ocho del Térraba; el
  delta de Astracán, con sus juncos, es la más pesada, y la Selva Negra la sigue): Cauces amplia pasó de ≈ 2 321 a ≈ 2 491 KB con el
  Tigris, a ≈ 2 734 KB con el Volga, a ≈ 2 903 KB con el Nilo, a ≈ 3 017 KB con el Amazonas y a ≈ 3 289 KB con el Yangtsé y el
  Misisipi, bajó a ≈ 2 878 KB al pasar las postales a 600 px y calidad 75 y subió a ≈ 3 132 KB con el Danubio y el Rin, a ≈ 3 343 KB
  con el Ganges y el Mekong, a ≈ 3 510 KB con el Níger y el Paraná, a ≈ 3 705 KB con el Indo y el Congo, a ≈ 3 867 KB con el Huang He
  y el Orinoco, a ≈ 4 113 KB con el Murray, el San Lorenzo y el Zambeze y a ≈ 4 663 KB con los seis ríos de Costa Rica, con lo que
  están las 201.
  **El tope de la amplia es 5 MB** (Humberto, 2026-10-26) y las postales son lo que más la engorda: todo Cauces lleva 201. Con 744 px y
  calidad 84 la amplia habría llegado a ≈ 6,4 MB; a 600 px y calidad 75 pesan un 42 % menos y con las 201, todas pintadas desde el
  2026-10-26, queda en ≈ 4 663 KB, con ≈ 457 KB de sobra (la proyección sobre las 156 primeras daba ≈ 500 KB: las ticas, con más figuras,
  salieron un poco más pesadas; el margen sube y baja con el detalle de cada serie: con 80 dejaba 240 KB, y las
  series más sencillas, del Níger en adelante, lo agrandaron; `python tools/peso_postales.py` mide las que hay, proyecta el total recodificando las
  vistas grandes como lo haría el pintor y prueba otras combinaciones: `560/75` dejaría ≈ 540 KB). Humberto comparó las dos a ciegas en el teléfono, en ocho postales difíciles (los
  juncos de Astracán, los renglones de Bagdad, el cielo de Luxor, las caras de Leticia…), y eligió la liviana: «no vale la pena la
  diferencia». Cambiar otra vez es tocar `ANCHO_POSTAL` y `CALIDAD_POSTAL` en tools/pintor.py y correr `python tools/pintados.py`,
  que repinta todas. test/dist.js falla si la amplia pasa de 5 MB y dice cuánto le queda. Las mercancías de los demás ríos (hoy solo
  las cinco del Nilo, 41 KB en el archivo de datos) sumarían ≈ 1 MB más: con todas las postales no cabrían sin achicarlas también. El
  AVIF pesaría lo mismo con 744 px (≈ 9,6 KB por postal a calidad 60), pero Safari lo lee desde iOS 16 y el WebP desde iOS 14: un
  iPad viejo se quedaría sin postales.
- Lecciones de las postales (2026-09-25): la postal pinta la imagen absurda de la ciudad, no un monumento cualquiera; donde coinciden
  (la Malwiya), mejor. Lo que se ve de costado se aplana: la ciudad redonda, vista casi de perfil, parecía un barco, y hay que verla desde
  arriba, con el anillo de la muralla, las cuatro puertas y las avenidas que llegan al centro. Blanco sobre blanco no se ve: la muselina
  es transparente sobre una piedra verde, con pliegues claros y flecos. Un barco chico en el horizonte con una torre al medio parece un
  submarino: el petrolero lleva el puente y la chimenea a popa.
- Lecciones del Volga (2026-09-26): un prado y un río del mismo verde se confunden; la tierra va teñida de amarillo (`prado` y `orilla`
  en volga.py) y el agua queda verde azul. Lo que la frase dice que pasa dentro se pinta dentro: con la muralla detrás, el caldero de
  Kazán quedaba fuera del Kremlin; va en el patio, con un lienzo de muralla adelante. Una cosa chica sin silueta propia no se lee: un
  fardo de pieles parecía un arbusto y, colgadas con su cabecita, sus patas y su cola, son pieles; un gorro de piel suelto parecía una
  maceta o una pantalla de lámpara y, puesto en un poste con el borde rizado, es un gorro. Una hoja de hacha en abanico parece una
  bandera: va en media luna, con sus dos puntas. Una figura alta con los brazos arriba (la Madre Patria y su espada) se dibuja con
  escala para que quepa entera; cortada, no se entiende.
- La regla del protagonista (2026-10-25, propuesta tras revisar las 25 postales al tamaño del teléfono y aprobada por Humberto: «dale,
  aplicá 1, 2 y 3 al Nilo»): la imagen para recordar es la protagonista; ocupa al menos un tercio del alto, va al medio y es lo único
  dorado de la postal (en la postal el dorado dice «esto es lo que hay que recordar», como en el juego dice «estás aquí»). No hay sol,
  salvo cuando es parte de la imagen (el reloj de Tikrit; el atardecer de Luxor, pálido y medio tapado por los cerros); las palmeras van
  sin dátiles dorados (`datiles=False`), el obelisco sin punta dorada (`punta`) y las falúas con casco de madera, salvo cuando la barca
  es la protagonista (la del mar del Nilo). Se revisa a 360 px, el ancho de la ficha en el teléfono: así se vio que el bebé de Juba, la
  barrera de Asuán, la balanza de Nizhni y el gorro y la lata de Astracán quedaban chicos, que Samara parece un bote lleno de melones y
  que los cuatro mares eran casi la misma postal. Desde el 2026-10-25 la cumplen todas las series.
- Lecciones de la reparación (2026-10-25): una U con algo adentro parece un bote (Samara, con las montañas como carga): el anzuelo es
  una J, con la caña larga y recta, el ojo y el sedal arriba, y la punta corta con su barba, y las montañas salen por la boca hacia el
  horizonte. Un gorro solo, en un poste, parece un letrero o una lámpara: en la cabeza de alguien es un gorro. Unos libros abiertos de
  costado, en V, parecen gaviotas: echados en el agua, con sus dos páginas y sus renglones, son libros. Un glaciar con volumen propio
  parece un cono colgado: va plano, como una lengua de hielo con grietas que sale de la nieve de la cumbre. Lo oscuro sobre lo oscuro se
  pierde: las pieles van contra el cielo y el cajón de té contra la colina. Para que la barca del mar sea la del juego, tiene que poder
  llegar al mar según su propio dato (el kelek no). Una figura de frente se arma igual que un animal: piernas, vestido o caftán, brazos
  en tubo hasta las manos, cabeza con ojos de punto y una sonrisa; las tres vecinas de Leticia llevan cada una su peinado (moño, pelo
  largo, rizos) para distinguirse.
- Lecciones del Yangtsé y del Misisipi (2026-10-26): una ciudad vertical se lee por su cerro: los edificios van escalonados sobre la
  pendiente, de atrás hacia adelante; sueltos, flotan. Un reflejo que tiene que decir «espejo» va entero y fuerte, aunque haya que achicar
  lo reflejado (la puerta de Nankín, para que su techo dorado entre en el agua). Una onomatopeya se pinta como el estallido de una
  historieta. Un afluente que entra se pinta antes que el río, para que se junten sin borde; si no, parece una rampa (el Misuri). Un
  pelícano se reconoce por el pico largo con su bolsa; las alas solas parecen un cocodrilo que vuela.
- Lecciones del Danubio y del Rin (2026-10-26): ríos que se juntan, vistos desde arriba, van en una sola masa de agua teñida por zonas, con
  los tintes difusos; en piezas separadas quedan costuras, y la punta cortada de un río angosto y oscuro parece un tablón (el Ilz de
  Passau). Un río que entra a la postal sale de un borde o de detrás de algo; si nace encima de un cerro, parece apoyado en él. Una punta
  entre dos ríos se lee si está pegada a la tierra de atrás; sola en el agua es una isla o un barco (Belgrado). Un pelícano es su pico:
  largo, chato y con la bolsa colgando; con el pico corto y el cuello largo, parece un cisne. Un caballo lleva el cuello arqueado hacia
  adelante y la cabeza larga; con el cuello recto hacia arriba, parece una llama. Una aguja gótica tiene que entrar entera en la postal:
  cortada por el borde de arriba, la torre parece un bloque. Las letras se leen enteras a 360 px si miden al menos un tercio del alto
  (BIBLIA en Maguncia); las de una veleta, más chicas, se leen por su forma y por la N, más grande.
- Lecciones del Ganges y del Mekong (2026-10-26): un paisaje se vuelve cara con poco (Gaumukh: la frente del glaciar, dos orejas, los
  cuernos, los ojos, el hocico, y la cueva por boca). Una trenza se lee si es grande y sus gajos se cruzan de un lado al otro en
  zigzag; una columna chica de óvalos no. Un pulmón se lee por su árbol de bronquios; el contorno solo parece una hoja o una gota. Cuando
  la protagonista son muchas cosas chicas (los sombreros de Can Tho), las de adelante van grandes. Las cordilleras llegan hasta abajo:
  una postal sin suelo adelante muestra una franja oscura. Dos cabezas enfrentadas parecen besarse: los dragones del medio miran afuera.
- Lecciones del Níger y del Paraná (2026-10-26): una figura que recorre la serie de un río la ata (el bumerán del Níger: sale, dobla
  y vuelve). Una forma echada sobre un río sigue su dirección: el bumerán de Gao, pintado en V sobre un río en Λ, no decía nada. Un
  cartel se lee a 360 px si sus letras miden un décimo del alto (NÍGER). Una figura en lo alto de un mástil, chica y en una esquina, se
  pierde: se la pinta de cerca (el vigía de Montevideo). De noche, la protagonista es la luz (las llamas de Port Harcourt). Un arcoíris
  de una sola banda dorada es un arco: lleva sus bandas pálidas.
- Lecciones del Indo y del Congo (2026-10-26): un dibujo puede leerse como un símbolo que no se buscó: una cúpula dorada con una veta
  vertical y dos franjas blancas era una iglesia con su cruz (el Kailash); hay que buscar cruces, letras y banderas que no se
  pidieron. Los juegos de sílabas del Congo (Bu-kama, Kin-du, M-banda-ka) se pintan tal cual, con la escena absurda entera. De frente,
  un pie a cada lado de una línea es un paso: un pie más arriba, detrás, y el otro adelante. Una «mata de piedras» lleva las piedras
  sueltas, cada una con su borde; juntas en una sola masa son una nube o un árbol.
- Lecciones del Huang He y del Orinoco (2026-10-26): lo que está hecho de muchas hebras (los fideos de Lanzhou) se pinta hebra por hebra;
  en una sola masa es un pan. Un penacho de barro en el mar es una mancha sin borde que se esfuma; con línea es una isla. Un sauce llorón
  lleva las ramas largas que caen desde una copa chica; con un sombrero macizo y flecos parece una medusa. Lo que la frase pone «en lo
  alto de la curva» va en el vértice, no adentro (el bao de Baotou). La piel muy clara sobre el `vientre` verde pálido sale verde: va el
  tono dorado oscuro, a la mitad (Bolívar). Un río visto desde arriba, teñido de pardo sobre un llano amarillo, se confunde con un
  camino: lleva su agua y sus ondas.
- Lecciones del Murray, del San Lorenzo y del Zambeze (2026-10-26): una hamaca colgada bajo, sobre el agua, es una canoa: va alta, entre
  los troncos, con tierra debajo y su sombra. Un embudo lleva el pico largo y angosto; con el pico corto es una copa. Quien empuja mira a
  lo que empuja (la vaca de Cornwall, primero de espaldas a la compuerta). El suelo que se pinta después tapa lo de atrás: el acantilado
  de Quebec se pinta encima de la otra orilla. Una mancha que tiñe una pieza va `dentro=` de esa pieza; suelta, tiñe toda su caja (el
  emparrado de Renmark pintó el fondo de café). Cuando la imagen es un juego de palabras con el nombre del mar (Bengala, Arábigo, Banana,
  Índico), la protagonista del mar sale del juego: el tigre, los números, el plátano, la mano que apunta con el índice.
- Lecciones de los ríos de Costa Rica (2026-10-26): `cordillera` cierra su polígono abajo, en el borde de la postal: un volcán en el
  horizonte de un lago (Ometepe) va en su propio polígono, cerrado en la línea del agua, o tapa el lago entero. Varios ríos dorados que
  se juntan, angostos, parecen varillas o cuernos de venado: los afluentes van de agua y lo dorado es el río que forman, largo y en una
  curva suave; corto y con curvas cerradas parece un chorizo o una media. Una barra blanca en el agua con un papel dorado y una punta
  doblada es un barco: el queso crema se lee por su crema, el papel arrugado y el cuchillo de untar. Una bolsa dorada con hojas verdes
  arriba es una piña: las mazorcas llevan tusas pálidas y la bolsa su borde enrollado. La piel teñida con el dorado oscuro sobre
  `vientre` sale verde oliva: va un café tibio (`A2683A`) a .6; la paja de un sombrero teñida de ocre se ve dorada: va pálida
  (`D2B070`). Un bigote con las puntas hacia abajo es una cara de enojo; con las puntas hacia arriba y una sonrisa, la cara es amable.
  Una mula que baja un escalón va inclinada entera (`affinity.rotate`), no con las patas estiradas. Una estatua de yeso lleva la cara de
  yeso. Una locomotora lleva la chimenea adelante y la cabina atrás. Con todas las postales pintadas, test/casos.js les quita un momento
  las suyas al Térraba y al Tárcoles para probar las de pictogramas, que son las de la económica.
- Hojas de revisión de postales: scratchpad `hoja-postales.py río` (las postales grandes, una debajo de otra, y otra hoja a 360 px, el
  tamaño del teléfono; el scratchpad se limpia solo y en octubre de 2026 se llevó dos veces estos scripts y dejó rota la instalación de
  Playwright: conviene pasarlos a tools/) y scratchpad/webkit
  `postales.js río` (cada ficha dentro del juego armado, bajando el río) y `reto-imagen.js río índice` (el reto de imagen con su pista).
- Hojas de revisión de barcas y mercancías: scratchpad `hoja-barcas.py ruta…` (las barcas grandes, de a dos) y `hoja-bienes.py ruta` (cada
  bien grande y a 52 y 78 px), y scratchpad/webkit `barcas-hoja.js [ruta…]` (el bloque «Tu embarcación» con el CSS del juego) y
  `barca-mercado.js [--exp] ruta…` (la barca y el mercado dentro del juego armado, comprando para que se vea la bodega).
- Descartado: el 2026-09-15, retratos trazados de grabados del siglo XIX y un «personaje» hecho con su silueta más una cara dibujada
  (commits b0715a6 y c69a359); el 2026-09-17, dibujos vectoriales a mano por coordenadas, con cabeza a tres cuartos sobre un cuerpo de
  perfil (commits f10c428 y 7959341); del 2026-09-17 al 2026-09-23, las ilustraciones de vectores sobre siluetas de PhyloPic (sombra por
  corrimiento del contorno, filo de brillo y zonas de color; `tools/ilustraciones.py` y `tools/ilustraciones/`).

## Cómo está hecho el motor

- Rutas: el motor no sabe de ríos, sabe de rutas (`RUTAS`, `rutaPor`; `rioPor`, `abrirRio`, `S.rio`, `focoRio` son alias:
  «rio» en un identificador quiere decir «ruta»). `JUEGO.rutas()` entrega las rutas: en Cauces, `RIVERS.map(desdeRio)`,
  que sobre el mismo objeto del río agrega `region`, `inicio {nombre, nota, escena}`, `fin {nombre, en, escena}`,
  `contexto [{clave, titulo, texto, pista}]`, `trazo [[…]]`, `ramas`, `paradas` (= `ciudades`), `vehiculo` (= NAVES),
  `companero` (= MASCOTAS, con `fin` = `mar`), `carga` (= MERCADOS), `eventos`, `perfil` (= ALTURAS); los nombres
  viejos quedan como alias para rios.js y las pruebas. `normalizar(r)` calcula `acum`, `kmPoly`, `idx` y `km` de cada
  parada, `cortes` (dónde empieza cada segmento del trazo), el mercader fantasma, el vocabulario efectivo y `pref`
  (prefijo de tarjetas: `rio:` para ríos, por el progreso guardado; `ruta:` para lo demás).
- Vocabulario: `VOCAB[tipo]` (rio | itinerario | travesia) tiene todas las palabras y frases que cambian con el
  tipo de ruta (inicio/fin, parada/etapa, bodega/morral, Zarpar/Seguir, Descender/Viajar, kickers, preguntas, cabeceras,
  voces del compañero que nombran el río) y cada ruta puede sobreescribir claves con `vocab`. `r.vocab` es el efectivo;
  `VJ()` da el del juego para pantallas sin ruta; `VZ()` da las voces del compañero de la ruta abierta (`VOCES` más
  `vocab.voces`). Las cadenas de `VOCAB.rio` son, letra por letra, las que Cauces tenía antes.
- Juego (`JUEGO`, de src/juegos/<id>.js, cargado antes del motor): `id`, `nombre`, `sub`, `tipo` (vocabulario por
  defecto), `clave` (prefijo de localStorage: en `file://` los dos juegos comparten el almacenamiento), `zonas`,
  `rutas()`, `grupos` de la lista y del pasaporte (`titulo`, `filtro`, `nota`, `antes`, `clase`), `rangos` y
  `comoSeJuega`. `progresoJSON.app` lleva el id del juego.
- Preguntas por tipo: `tiposDisponibles(r)`; con menos de cuatro rutas en el juego no hay distractores de otras rutas,
  así que `ciudad`, `frase` y las de contexto no se ofrecen y entran `orden` (cuatro secuencias, una verdadera) y
  `fecha` (¿en qué año llegó a…?; los años se comparan con `anio`, que entiende «334 a. C.» como -334, y los distractores
  son años distintos, no textos distintos). Con cuatro rutas o más, el reto del río de un viaje reparte cerca/fecha y
  frase/orden; el de un río no cambia. `fin` (alias `mar`) toma etapas del mismo viaje como distractores si hace falta.
  Ninguna parada puede repetirse entre rutas del mismo juego (la pregunta «¿en qué viaje está…?» sería ambigua; el test lo exige).
  Los tipos de contexto se llaman como la `clave` de cada capa (`antigua`/`moderna` en ríos, `entonces`/`hoy` en Ibn
  Battuta) y son a la vez claves de tarjeta.
- Mapa por tipo: `trazoTramo` dibuja el trazo por segmentos (`cortes`); `camara:'tramo'` encuadra en Descender la
  ventana de la parada anterior a la siguiente (`ventana(r)`), pensada para viajes de medio mundo; los vehículos
  terrestres (`TERRESTRES`: caravana, pie, jinete) van sin balanceo, con `.anda`, huellas en vez de estela y polvo en vez de
  salpicón; el sonido pasa a viento (`audio.modo`). La franja bajo el mapa es el perfil de altura si la ruta tiene
  `perfil` y una línea de tiempo (`tiempoSVG`) si tiene fechas. Pendiente: partir la animación del vehículo en los
  cortes y el antimeridiano (`lon0` + `<use>` de la tierra), diseñados en docs/itinerarios.md.
- Viajes (Exploradores; funciones dentro de bloques `/*@vocab:itinerario*/ … /*@fin:itinerario*/` que build.js recorta de
  Cauces): la unidad de memoria es el tramo, el rumbo y la escala, no la parada en orden fino. El kicker suma kilómetros del
  dibujo y años desde la partida (`escalaViaje`) y el final resume la escala (`resumenViaje`). La guía pregunta «¿hacia
  dónde sigue el viaje?» con el `rumbo` de cada etapa (`rotuloGuia`); el nombre aparece al acertar. Sin «cerca» ni
  «siguiente»: `TIPOS_VIAJE` ofrece `lejos` (punto más lejano, si es claro), `cruza` (campo `cruza`), `duracion` y
  `primero` (con años), todas sobre la tarjeta `ruta:ID:escala`. Ordenar y la pregunta de orden usan `unidades(r)`: los
  `tramos` con nombre si el viaje los trae. El riel de un viaje lleva Trazar en vez de Recitar (`iniciarTrazar`,
  `trazarEn`, `renderTrazar`, `focoTrazar`): el mapa muestra solo el camino trazado y todas las etapas como puntos sin
  nombre (`hitz` con `trazarEn(i)`, `ocultarResto`), tocar la siguiente a la primera cuenta como recuerdo con pista
  (`marcar(…, 'recordar', 1)`), hasta dos errores dejan la etapa hecha (`P.etapas[id].trazar`) y en Mercader dan monedas.
  La portada de Exploradores cierra con «Los viajes, en escala» (`renderComparar`): kilómetros y años por viaje.
- Navegación (rediseño del 2026-09-06): en las pantallas de ruta y de reto hay una barra fija al pie, `#pie`, que `render()`
  arma con `renderPie()` a partir de `S`: arriba las acciones del momento (la guía «¿cuál es la próxima parada?» con sus fichas
  y «Zarpar a…», «Llegar al mar», «Seguir hacia…» tras un evento, Revelar / La sabía / No la sabía en Recitar, Otra vez y
  Preguntar al terminar, Siguiente y Ver resultado en las preguntas, Otra ronda y Volver al final) y abajo el riel de viaje
  (`renderRiel`: Bajar · Ordenar · Recitar · Preguntar), que es a la vez menú y mapa del progreso: el paso actual va en
  dorado y los hechos con un check (`P.etapas[id]`, marcados por `hecha()`: bajar = `P.vistos`, ordenar con ≤ 1 error,
  recitar con ≥ n−1 aciertos, preguntar con una ronda del río al 60 % o más). `body.con-pie` acolcha el panel con el alto
  real de la barra (`acomodarPie`) y en teléfono baja el mapa a 28vh. En el inicio y el pasaporte no hay barra.
  La portada empieza por Hoy, sigue «¿Quién juega?», el tesoro y las rutas en tarjetas (`.tarjeta`: animal, nombre,
  `vocab.tarjeta(r)` y barra de dominio; tres columnas en teléfono), agrupadas por región cuando el grupo trae
  `porRegion` (Cauces: por continente, en el orden del río más largo); «Tocá un río…» vive en «¿Cómo se juega?».
  Los números van en Oswald con `num()` (`<span class="num">`): cabecera, kickers, tramos, alturas, monedas y precios;
  las pruebas comparan textos sin esas etiquetas (`sinNum`) y miran `#panel` más `#pie` (`todo()` / `panel()`).
- Estado en dos objetos: `S` (sesión: pantalla, río, pestaña, paso, orden, quiz, eco, guías, recitar, evento) y `P`
  (persistente: `cards` Leitner, `vistos`, `tesoro`, `modo`, `voz`, `sellos`, `etapas`). `P` se guarda con `guardar()` en `localStorage`
  bajo `cauces:progreso:<perfil>` (memoria si no hay o falla). `PERFILES` (`cauces:perfiles`: lista y activo) da
  un `P` por persona; "¿Quién juega?" en el inicio los elige o crea (`elegirPerfil`, `crearPerfil`,
  `quitarPerfil`); `cargarPerfiles()` migra el guardado viejo (`cauces:progreso`) al perfil Capitán. Copia y
  traslado: `progresoJSON()`/`exportar()` bajan un `.json` y `importarTexto()` lo carga (crea o reemplaza el
  perfil que trae el archivo, preguntando antes de pisar progreso).
- Todo se dibuja con `render()`: cabecera, panel (`renderInicio`, `renderDescender`, `renderOrden`,
  `renderRecitar`, `renderQuiz`) y mapa (`renderMapa(foco)`), a partir de `S`. Los manejadores son funciones
  globales llamadas desde `onclick` en el HTML generado. No hay componentes ni eventos delegados.
- Mapa: SVG con proyección equirectangular (`proj`), viewBox animado (`setVB`), tamaños en píxeles constantes
  (`px = vb.w / ancho del contenedor`). El SVG lleva `preserveAspectRatio` slice y `vbPara` ajusta la vista a la proporción
  del mapa desplegado; plegado (▾, `#arriba.compacto`) recorta esa misma vista a la altura chica centrando la barca (misma
  escala, nunca un mapa encogido). Como el alto del CSS cambia con transición, `dimsMapa` mide los dos altos sin transición y
  restaura la animación (FLIP) en cada render; al plegar la caja se anima y al desplegar salta y solo destapa. La barca se anima con `animarBarca` sobre la polilínea del río entre
  paradas; la mascota va en `#masc` y se contrarrota para quedar derecha. Fuera de Descender (Ordenar, Recitar, el
  reto del río) la barca queda estacionada en la parada actual (`estacionada(r)`) para que no desaparezca; en reto
  mundial y repaso, antes de responder, hay un globo neutro «Cauces» (`globoNeutro`) para no delatar el río sin
  dejar la pantalla sin globo. La barca es un glifo SVG propio
  por tipo (`glifo()`: latina, junco, vapor, balsa, canoa, barcaza, cuadrada; vista lateral, proa a la derecha,
  partes `casco` dorado, `vela` blanca, `linea` color mar solo sobre vela o casco, `palo` dorado para mástiles,
  chimeneas y remos contra el agua, `fig` blanca, `humo`; lo alto va del centro a la proa y la popa queda baja porque el
  animal se sienta ahí, en `#masc` con `translate(-9 -9) scale(.6)`), envuelto en `.mece` (balanceo CSS); al avanzar, `animarBarca`
  dibuja la estela `#estela` detrás y al llegar suelta un salpicón (`.salpicon`, se quita solo); si la guía salió
  mal, `S.bamboleo` añade la clase `duda` una vez. El mismo glifo va en el bloque «Tu embarcación» (`.barca.mini`).
  El animal (`ANIMALES[m.glifo]`) va en `#masc` sobre la barca, derecho y mirando hacia adelante
  (`rotate(-ang·sx)`: se anula el giro pero no el espejo), y en el globo del evento salta una vez (`.globo.salta`).
- Escenas (`PICTOS`, `escena(items)`; en la edición amplia, la postal pintada del río si la tiene, `postal(rid, i, cls)`, ver «Postales»): un vocabulario de pictogramas SVG (caja 40×40, suelo en y=40; clases `p`
  verde, `d` dorado, `b` blanco, `l` línea, `w` línea clara, `a` agua) y `animal:<glifo>` para los animales. Cada
  ciudad lleva `escena` con 3-4 claves y cada río `escenaNace`/`escenaMar`; se dibuja como postal (cielo, sol,
  suelo, río) sobre la imagen para recordar, en la fuente y en el mar; el reto de imagen la muestra sin nombre como
  pista (`q.escena`), y el sello del pasaporte lleva el primer pictograma (`.escena.pic`). Componer con lo que dice
  el dato de la ciudad (presa, templo, puente, manglar…), nunca al azar.
  Todo respeta `prefers-reduced-motion`. Los cauces son de Natural Earth
  50 m (`tools/cauces.py`), con un vértice propio frente a cada ciudad para que `c.idx` la ancle justo ahí.
- Iconos (`ICONOS`, `ico(clave)`): un juego propio de iconos de línea (caja 24×24, trazo `currentColor`, clase `.ico`) para los
  bienes del mercado (por categoría, campo `i`), los eventos (campo `icono`, que también decide el clima) y los controles
  (moneda, voz, ok). No hay emojis en la interfaz: se ven distintos en cada teléfono y no son de nadie. build.js recorta los
  que el juego no usa. `animal:<glifo>` y `barca:<tipo>` reutilizan los animales y las barcas.
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
  `ciudad:ID:i` está en caja ≥ 3 y además se recitó de memoria alguna vez (`rec`). `completo(r)` = todos los sellos → el río va en dorado en el mapa mundial y en la
  zona (clase `hecho`) y la fila del inicio dice «completo». Pantalla `pasaporte` (`verPasaporte`,
  `renderPasaporte`): resumen, y por río sus sellos y los huecos vacíos. Va en el JSON de exportación como el
  resto de `P`. Cada sello (`sello(r,i)`) es un SVG con carácter propio y estable: un hash de `río:parada` elige
  la forma (`FORMAS`: círculo, óvalo, cuadrado, hexágono, octógono, escudo), la inclinación (`--rot`), el desgaste
  del aro interior (`DESGASTES`) y la tinta (verde o verde medio; ocre con estrellas si es de oro); lleva el río y
  el país en el aro (`textPath`), el primer pictograma de la ciudad en tinta, el nombre y la fecha. El hueco vacío
  conserva la forma en punteado gris.
- Leitner: cajas 0-5, intervalos [0,1,3,7,14,30] días. Dos clases de evidencia (revisión externa del 2026-09-07):
  reconocer entre opciones (guía, retos, repaso, eventos) sube una tarjeta solo hasta la caja 3; recordar de memoria en
  Recitar (`marcar(id, ok, 'recordar', nivel)`, 1 con pista y 2 sin pista) deja la marca `rec` y abre las cajas 4 y 5. Una
  tarjeta solo sube cuando está vencida: acertarla tres veces la misma tarde cuenta una vez; fallarla la baja a 0 y borra
  `rec`. Así el dominio de un río sin recitar tope en 60 % y nada se muestra consolidado por reconocerlo recién. Tarjetas por río: `rio:ID:orden|antigua|moderna|mar`
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

RUTA (lo que el motor lee; docs/itinerarios.md trae el esquema completo con ejemplo): `id, tipo, nombre, region, zona?,
longitud?, inicio {nombre, nota, escena, fecha?}, fin {nombre, en, escena, fecha?}, contexto [dos capas {clave, titulo,
texto, pista}], frase, fraseNota?, trazo [segmentos de [lat,lon]], ramas?, paradas [{nombre, pais, pos, imagen, dato,
escena, fecha?, rumbo (viajes)}], vehiculo {nombre, tipo, desc, zarpe, llegada, puertos}, companero {nombre, especie, emoji, glifo,
hola, fin, paradas}, carga [bienes], eventos [], perfil?, camara?, vocab?, cruza? [mares, desiertos o montañas que cruzó],
tramos? [{nombre, hasta: índice de la última etapa del tramo}], antimeridiano? (la ruta cruza los 180°)`. Los itinerarios se escriben así directamente
(`itinerarios.js`); los ríos siguen en su esquema de siempre y `desdeRio` los convierte.

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
dibuja en el globo, la lista, el pasaporte y la barca; el emoji queda de respaldo si no hay glifo. Construcción del set
(redibujado el 2026-09-14 para que lea a 26 px): cuerpo redondo y cabeza grande, suelo en y ≈ 8 para los de patas, patas
rellenas con contorno (`cuerpo`, nunca trazos de palo), ojo `oscuro` de radio 1-1.2, boca con `bigote`, un solo detalle
dorado por animal donde el animal lo pide (pico, manta, cresta, pinzas) y `claro` para vientre, cara o dientes. Cada glifo
pesa hasta 800 caracteres (la prueba lo exige); la hoja de contacto scratchpad/webkit/hoja.js los dibuja a los tamaños reales.

MERCADOS[id]: `[{n: nombre, i: icono (clave de ICONOS: grano, fruta, pez, cesta, bebida, frasco, hoja, tela, piel, madera, metal, gema, mineral, vasija, papel, moneda…), o: puerto de origen (índice), b: precio base, d?: puertos antes de
pudrirse, m?: puerto donde se paga doble}]`. Cada puerto salvo el último debería ofrecer algo.

EVENTOS[id]: `[{tramo (parada de llegada, 1..n+1; n+1 es el mar), icono (clave de ICONOS: ola, niebla, viento, lluvia, arena, hielo, piedra, puente, aduana, vela, nudo, tren, espada, castillo, mascara, pez, o `animal:<glifo>` / `barca:<tipo>`; niebla, arena, lluvia, ola y viento traen clima), titulo, texto (la situación, con
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
5. Un río nuevo del mundo va solo en la edición amplia: su objeto y sus entradas entran dentro del bloque `/*@amplia*/ …
   /*@fin:amplia*/` de cada archivo de datos, y las herramientas se corren para la amplia (`python tools/cauces.py <id>`,
   `python tools/relieve.py cauces amplia`, `python tools/mapa.py cauces amplia`); la económica y sus generados no cambian.
   Donde Natural Earth no trae regiones con nombre (Australia), `MUNDO_NOMBRES` en relieve.py lleva rótulos a mano, y
   `PERMITIR` levanta para un río un nombre de `EXCLUIR` (el Escudo Canadiense en el San Lorenzo). La instantánea cambia
   (lista y reto) y se retoma a propósito.

### Para agregar un itinerario (o una derrota)

1. Objeto en `src/data/itinerarios.js` en el esquema RUTA: `tipo:'itinerario'`, `region` (los años), `inicio` y `fin`
   con `fecha`, dos capas de `contexto` con `clave`, `titulo`, `texto` y `pista` sin nombres propios, 8-10 `paradas`
   en orden cronológico con `pos` verificada, `fecha` («hacia 1332» si el relato no la fija), `imagen`, `dato` y
   `escena`; acróstico con las iniciales; `vehiculo` (`tipo` caravana, pie o uno náutico) con `puertos` por etapa;
   `companero` (animal real del viaje, `glifo` en `ANIMALES`); `carga` (el morral: algo que cambiar en cada etapa
   salvo la última); uno o dos `eventos`. `camara:'tramo'` si el viaje es largo. Donde el relato es discutido, el
   dato lo dice («según su relato», «los historiadores dudan»).
2. Puntos de paso en `PUNTOS` de `tools/itinerarios.py` (con las paradas nombradas) y `npm run itinerarios`: cada
   parada debe quedar como vértice y en orden.
3. `python tools/mapa.py exploradores` y `python tools/relieve.py exploradores` (cubren las ventanas de la cámara por
   tramo), `node test/pruebas.js exploradores`, `npm run build`, `npm run verificacion` y revisar las líneas nuevas.
4. Una travesía (ruta marítima) va igual con `tipo:'travesia'` (vocabulario de escalas y flota); si cruza 180°, falta el
   antimeridiano.
5. Campos propios de los viajes: `rumbo` en cada etapa (hacia dónde sigue el viaje para llegar a ella: medio y dirección,
   distinto dentro del viaje; es lo que preguntan las fichas de la guía), `tramos` (tres a cinco tramos con nombre que
   cubren todas las etapas en orden; Ordenar y la pregunta de orden los usan) y `cruza` (mares, desiertos o montañas que
   el viaje cruzó, para la pregunta «¿cuál de estos cruzó…?»). Un viaje sin años (Odiseo) lleva en `fecha` un texto sin
   cifra («año 1 del regreso»): no tiene línea de tiempo ni preguntas de fecha, duración o «cuál fue primero». Cuando el
   lugar es tradición y no dato (los sitios de la Odisea), el `dato` lo dice. Las fechas admiten mes («junio de 1812»):
   `fechaNum` las coloca en la línea de tiempo y `lapso` mide en meses lo que no llega a un año; la pregunta de fecha solo
   se ofrece con cuatro años distintos. Si el viaje cruza los 180° (Cook), `antimeridiano:true`: `desenrollar` vuelve
   continuas las longitudes al cargar, el mapa muestra los mundos vecinos (`#copias`, `data-copias` en `#mapa`) y dibuja la
   ruta también a ±360°, y tools/rutas.py parte en dos las vistas que cruzan la línea para el mapa y el relieve. Una ruta
   corta puede pedir vértices más seguidos en `PASO_RUTA` de tools/itinerarios.py (el test exige 40 vértices o más).

## Pendientes, en orden de valor

Hecho el 2026-09-06: el rediseño estético en tres fases (identidad, navegación con barra al pie y riel, iconos propios).
Queda por sentir en el iPhone de Humberto si la barra al pie deja suficiente contenido a la vista; si no, la salida es plegar
el mapa (▾) al abrir la barra o bajar el perfil de altura a 44 px.

0. Más ríos del mundo (hechos el 2026-09-13 en la edición amplia: Orinoco, Murray, San Lorenzo y Zambeze). Los que sigan pesan
   12-15 KB cada uno y entran marcados `/*@amplia*/`, solo en la edición amplia (ver «Ediciones»), porque la económica de Cauces está
   al tope. Un paquete aparte («Ríos de España»: Tajo, Ebro, Duero, Guadalquivir) iría mejor como cuaderno nuevo con el mismo motor.

1. Exploradores: más viajes (Elcano, Darwin) y de conquista (Gengis Kan), aprobados para niños y adultos. Cada viaje nuevo trae rumbo por etapa, tramos y cruza. Con cada viaje,
   revisar las líneas nuevas de docs/verificacion.md y que ninguna parada se repita entre rutas.
2. Motor de rutas, lo que falta: partir la animación del vehículo en los `cortes`. (El antimeridiano y la línea de tiempo
   con meses quedaron hechos el 2026-09-07 con Cook y Napoleón.)
3. Inmersión, lo que queda de la evaluación del 2026-09-04: retos sobre el mapa («tocá dónde queda…», que pagan
   memoria espacial) y paisaje sonoro por tramo sintetizado. (La bitácora imprimible se descartó.)
4. Más ríos de Costa Rica: Pacuare y Sixaola están en Natural Earth 10 m Norteamérica (`capa:'ne10na'`) pero casi
   no tienen pueblos a la orilla (Tres Equis y la barra; Suretka, Bribri y Sixaola): habría que armar paradas con
   sitios (rápidos, reservas, puentes) y verificarlos. Los demás ríos saldrían de OpenStreetMap ampliando `OSM_Q`.
5. Más eventos (hecho el 2026-09-13 en la edición amplia: un tercer evento, marcado `/*@amplia*/` al final del array del río en
   eventos.js, para los trece ríos del mundo que tenían dos; la económica sigue con 44 y la amplia tiene 69, tres por río del mundo).
   Los que sigan, con un hecho real detrás y un tramo que ningún otro evento del río use.


## Reglas de trabajo

- Cambios pequeños y probados. Si tocás datos, corré `npm run verificacion` y leé lo que cambió.
- No agregar dependencias de ejecución. Herramientas de desarrollo (shapely, node) sí.
- Mantener la edición económica (`dist/cauces.html`, `dist/exploradores.html`) por debajo de ~500 KB (tope subido de 400 a 500 el
  2026-09-04 para el relieve; el 2026-09-14 Cauces ≈ 498 KB y Exploradores ≈ 455 KB; la amplia de Cauces ≈ 4 663 KB y la de Exploradores ≈ 893 KB el 2026-10-26, con los animales, las barcas, las mercancías del Nilo y las postales de los 25 ríos pintados). La edición amplia
  (`-amplia.html`) tiene un tope más holgado, 5 MB (Humberto, 2026-10-26; test/dist.js falla si una lo pasa y dice cuánto queda): lo que
  no cabe en la económica va marcado `/*@amplia*/` (ver «Ediciones»), y lo que más engorda la amplia son las postales (ver «Postales» y
  `python tools/peso_postales.py`). Palancas de peso ya usadas: recorte del motor por juego en build.js;
  comentarios y sangría fuera del motor, de los datos y del archivo del juego en dist (`limpiar` en build.js); en mapa.py, fronteras a 0,5 y lagos
  ≥ 1 unidad², costa fina a 0,3 (Cauces) o 0,45 (Exploradores); en relieve.py, franjas a 0,75/4 en el mundo y 0,02/0,02 en la zona.
  Lo que queda por probar si hace falta: un minificador de desarrollo sobre el motor (terser como herramienta, no como dependencia
  de ejecución; test/dist.js seguiría probando el HTML ensamblado), que es la palanca grande que queda: la económica de Cauces está a 2 KB del tope.
- Ningún texto de Cauces cambia sin querer: `test/instantanea.js` compara 200 pantallas; si un cambio de texto es a propósito,
  `npm run instantanea` y decirlo en el commit. Hay repositorio git desde el 2026-09-04: commits chicos, en español. El remoto es
  github.com/humbertogrant/cauces (público) desde el 2026-09-06; `gh` en esta máquina está autenticado como humbertogrant.
- Publicación: GitHub Pages sirve la carpeta `dist` en https://humbertogrant.github.io/cauces/ (`cauces.html`, `exploradores.html`,
  las ediciones amplias `cauces-amplia.html` y `exploradores-amplia.html`, y una portada `index.html` que build.js no toca). La publica `.github/workflows/pages.yml` con cada push a `main`, solo si `npm test`
  pasa y `node build.js` no cambia `dist`: reconstruir y versionar `dist` antes de subir.
- Textos para niño: frases cortas, concretas, sin sarcasmo; el animal nunca regaña.
- Accesibilidad mínima: botones reales, `aria-label` en iconos, `prefers-reduced-motion` respetado.
- iPhone: un `.html` copiado al aparato se abre en la vista previa de Archivos (Quick Look), que no ejecuta JavaScript y
  muestra solo el fondo; no es un fallo del juego (WebKit lo corre sin errores por http y por file://, `tools/safari.js`).
  En iPhone se abre la dirección de Pages (o cualquier hosting estático, o una app que sirva HTML local).
- Móvil (revisado el 2026-09-04 a 375×812, 360×640 y 812×375): nada desborda a lo ancho, toques de 36 px o más, campo de
  texto de 17 px (sin zoom en iPhone). Reglas en cabeza.html: con ancho ≤ 480 px el mapa baja a 34vh (el bloque pegajoso
  queda en ~55 % del alto); con alto ≤ 520 px (teléfono en horizontal) `#arriba` deja de ser pegajoso; con la barra al pie (`body.con-pie`) y ancho < 760 px el mapa
  baja a 28vh (mínimo 190 px) y el panel se acolcha con el alto de la barra. En el panel de vista
  previa las transiciones CSS no avanzan: para medir alturas hay que poner `transition:none`.
