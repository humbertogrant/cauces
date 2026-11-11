# Textos nuevos de la vitrina, para revisión de Humberto

Ningún dato, cifra ni fecha nueva entró al juego: todo lo que se lee sobre el Nilo sale de `src/data/` tal como estaba. Lo que
sigue son los textos de interfaz (rótulos y botones) y los rótulos geográficos de la carta que la vitrina agrega.

## Del juego `nilo` (Dirección)

| Dónde | Texto |
|---|---|
| Título del archivo (`<title>`) | Cauces · Nilo: la vitrina de un río |
| Subtítulo en el inicio | El Nilo, ciudad por ciudad |
| Título del grupo en el inicio | El Nilo |

## De la bitácora (`src/vitrina/panel.js`)

| Dónde | Texto |
|---|---|
| Portada, sobre el mapa | Cauces (rótulo de marca) |
| Portada, tres datos | Nave · Compañero · Paradas |
| Botón del pie en la portada y en cada parada | Zarpar |
| Navegando, ficha de la parada que sigue | próxima |
| Navegando y llegada, contador | «3 de 6 paradas» (con la palabra «Parada» del motor) |
| Navegando, rótulo del perfil | Perfil del río |
| Navegando, bajo el perfil | «de 1 149 m en la fuente a 0 m en el mar» (las palabras que el motor ya usa en la descripción del perfil) |
| Llegada al mar, rótulo | Llegaste al mar |
| Llegada al mar, tarjeta de cifras | Ganancia · La vez pasada · El mercader · Tu tesoro |

## De la carta (`src/vitrina/carta.js` y `carta-datos.js`)

Son nombres de geografía, puestos a mano sobre la carta; ninguno es una parada del juego. También están listados, con ⚠, al final
de `docs/verificacion.md`.

| Clase | Rótulos |
|---|---|
| Mares y lagos (cursiva espaciada) | Mar Mediterráneo · Mar Rojo · Lago Victoria · Lago Nasser |
| Cauces (cursiva) | Nilo Blanco · Nilo Azul |
| Países y regiones (mayúsculas espaciadas) | Egipto · Sudán · Sudán del Sur · Uganda · Etiopía · Desierto de Nubia · Sudd |
| Líneas | Ecuador · Trópico de Cáncer |
| Hitos (11 px, con coordenadas puestas de memoria) | Abu Simbel (22,34° N, 31,63° E) · Pirámides de Meroe (16,94° N, 33,75° E) · Pirámides de Guiza (29,98° N, 31,13° E; solo aparece cuando El Cairo ya se alcanzó, porque al lado del anillo delataba la parada) · Alejandría (31,20° N, 29,92° E) |
| Signo | «?» en el anillo de la próxima parada |

Abu Simbel, Meroe, Guiza y Alejandría ya están nombrados en los textos del juego (datos de Asuán, Jartum y El Cairo, y la llegada
de la falúa); lo nuevo son sus posiciones en la carta.

## Fuente del relieve

ETOPO1 Global Relief Model, de NOAA NCEI (Amante y Eakins, 2009), dominio público: el mismo ráster que ya usa `tools/relieve.py`.
`python tools/carta.py` lo recorta a la ventana lat −6…36, lon 18…46, lo sombrea con luz del noroeste y lo guarda como una imagen
WebP de 400 × 600 dentro de `src/vitrina/carta-datos.js` (95 KB). No se bajó nada en la corrida.
