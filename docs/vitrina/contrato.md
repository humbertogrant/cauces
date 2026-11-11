# Contrato de la vitrina del Nilo

Árbol de trabajo: `C:\Users\humbe\proyectos\geo\cauces-vitrina` (rama `vitrina-nilo`). Solo Dirección hace commits. Nadie edita un
archivo ajeno: si hace falta un cambio, se le pide a Dirección en el informe final. `src/motor.js`, `build.js`, `src/cabeza.html`,
`src/data/*` y `test/casos*.js` no se tocan.

Dirección de arte, en una frase: **carta náutica de noche con un solo hilo de oro, que es el río; abajo, la bitácora en papel cálido.**

## Dueños

| Rol | Archivos |
|---|---|
| Dirección | `build.js`, ganchos en `src/motor.js`, `src/juegos/nilo.js`, `src/vitrina/capa.js`, `src/vitrina/capa.css`, `docs/vitrina/*.md` (menos hallazgos), `CLAUDE.md` |
| Carta | `tools/carta.py`, `src/vitrina/carta-datos.js` (generado), `src/vitrina/carta.js`, `src/vitrina/carta.css` |
| Bitácora | `src/vitrina/panel.js`, `src/vitrina/panel.css` |
| Sonido | `src/vitrina/sonido.js` |
| Verificación | `tools/captura.js`, `test/vitrina.js`, `docs/vitrina/hallazgos.md`, `docs/vitrina/capturas/` |

## Cómo se arma `dist/nilo.html` (`node build.js`)

Un solo archivo, sin red. Orden de los `<script>`: datos del Nilo (los mismos globales de Cauces amplia, pero solo con el Nilo:
`LAND`, `LAGOS`, `BORDES`, `RIVERS`, `NAVES`, `MASCOTAS`, `ILUSTRACIONES`, `BARCAS`, `BIENES`, `POSTALES`, `MERCADOS`, `EVENTOS`,
`VOCES`, `RELIEVE`, `NOMBRES_RELIEVE`, `ALTURAS`) → `src/juegos/nilo.js` (`JUEGO`) → `src/vitrina/capa.js` → `carta-datos.js` →
`carta.js` → `panel.js` → `sonido.js` → `src/motor.js`. El CSS de `capa.css`, `carta.css` y `panel.css` va, en ese orden, después
del de `cabeza.html`, dentro de un `<style>` propio. Un archivo de módulo que no exista se salta (el build no falla).

Los módulos se cargan **antes** que el motor: en el nivel superior solo definen cosas y se registran en `CAPA`. Lo del motor (`S`,
`P`, `esc`, `num`, `km`, `proj`, `globo`, `postal`, `rioPor`…) se usa solo dentro de funciones, que corren después. Las pruebas
cargan todo con un DOM simulado (`test/arnes.js`): nada de DOM ni de APIs del navegador al cargar, y dentro de las funciones todo
acceso al DOM va con guardas (`if(!el||!el.setAttribute)return`). Si `CAPA` no está, el motor se comporta como hoy: en
`dist/cauces.html` y `dist/exploradores.html` los ganchos ni siquiera viajan (el build los recorta; quedan byte a byte iguales).

## `CAPA` (lo define `src/vitrina/capa.js`)

```js
const CAPA={rio:'nilo',fase:'parada',          // fase: 'parada' (lo que hay en la parada) | 'navega' (la guía antes de zarpar)
  oir(nombre,fn){…}, emitir(nombre,datos){…},   // eventos; un oyente que falla no rompe el juego
  navegar(){CAPA.fase='navega';render(false)},  // lo llama el botón ZARPAR de la bitácora
  momento(){…}};                                // 'portada' | 'navega' | 'parada' | 'mar' | 'otro'
```

Cada módulo agrega lo suyo con asignaciones (`CAPA.mapa=function(…){…}`):

- **Bitácora**: `CAPA.descender = r => string|null` (HTML de `#panel` en Bajar; `null` deja el del motor) y
  `CAPA.pie = (r, porDefecto) => string|null` (el bloque de acciones del pie en Bajar; `porDefecto` es el HTML del motor).
- **Carta**: `CAPA.mapa = (foco, vb, px) => void` (después de que el motor dibujó el mapa) y
  `CAPA.vista = (r, foco) => ({pts:[[lat,lon],…], minW:número, margen:número}) | null` (el encuadre).
- **Sonido**: se suscribe con `CAPA.oir`.

## Ganchos del motor

1. `render()`: antes de dibujar, `document.body` recibe `data-momento="…"` con `CAPA.momento()` y la clase `vitrina`.
2. `renderDescender(r)`, sin evento activo: si `CAPA.descender(r)` devuelve un string, ese es el panel.
3. `renderPie()`, en Bajar y sin evento: `acto = CAPA.pie(r, acto) ?? acto`.
4. `renderMapa(foco)`, con `foco.modo==='rio'`: el encuadre sale de `CAPA.vista(r, foco)` si devuelve algo; al final,
   `CAPA.mapa(foco, vb, px)`.
5. Eventos (`CAPA.emitir`): `zarpar {r, de, a}` al salir hacia la parada `a` (1…n+1, n+1 es el mar); `avanza {k, x, y}` en cada
   cuadro del viaje de la barca (`k` de 0 a 1; `x`, `y` en unidades del SVG); `parada {r, i}` al llegar a la parada `i` (0…n−1);
   `mar {r}` al llegar al mar; `moneda {}` al comprar o vender; `sello {r, i}` al ganar un sello; `toque {}` en el primer toque
   o tecla del jugador (para arrancar el sonido); `dibujado {}` al final de cada `render()` (para retocar lo que el motor acaba de
   poner, como el subtítulo del encabezado).
6. Durante una prueba entre puertos (`S.evento`), `CAPA.momento()` devuelve `'evento'`: el panel y el pie son los del motor
   (`renderEvento`), dentro de la misma hoja; `CAPA.descender` y `CAPA.pie` no se llaman.

Las fases: al llegar a una parada, `CAPA.fase='parada'` (la bitácora muestra la parada y un botón ZARPAR que llama
`CAPA.navegar()`); en `'navega'` la bitácora muestra las fichas del acróstico, la pregunta de Hipo y el perfil, y el pie es el del
motor (la guía «¿Cuál es la próxima parada?» y, al responder, «Zarpar a …», que es `paso(1)`). `paso()` devuelve la fase a
`'parada'`. En la portada (`S.paso===0`), ZARPAR también llama `CAPA.navegar()`; en la primera bajada el motor muestra ahí la
frase con la lista y su «Zarpar ›» (`zarpar()`), y después la guía: eso se respeta (enseñar antes de preguntar).

## Lo que el motor ya da (leer `src/motor.js` antes de escribir)

- Estado: `S.pantalla` ('inicio'|'rio'|'quiz'|'pasaporte'), `S.tab` ('descender'|…), `S.paso` (0 = nacimiento, 1…n = paradas,
  n+1 = mar), `S.evento`, `S.zarpo`, `S.guias[p]` (`{opciones, objetivo, resp, ok}`), `S.llaves`, `S.eco` (Mercader: `{monedas,
  bodega, final…}`; `null` en Historia), `S.selloNuevo`, `P` (lo guardado), `esNino()`, `modo()`.
- Ruta: `r=rioPor('nilo')`: `r.nombre`, `r.longitud`, `r.frase` («Tres [J]otas y un [A][L][E]»), `r.paradas[i] {nombre, pais, pos,
  imagen, dato, km, idx}`, `r.curso` ([lat,lon]…), `r.ramas`, `r.inicio`, `r.fin`, `r.vehiculo`, `r.companero`, `r.carga`,
  `r.perfil`, `r.vocab` (textos: `kickerInicio(r)`, `kickerParada(r,p,n,c)`, `kickerFin(r)`, `tramo(r,c,prev)`, `cabecera(r)`,
  `llegada(r)`, `proxima`, `avanzar`, `llegarFin`…).
- Plantillas y ayudas: `esc`, `num`, `km`, `globo(r, texto, extra, animo)` (ánimos: normal, alegre, pensativo, sorpresa,
  dormido), `postal(rid, i, cls)` (la postal pintada: 0 nacimiento, 1…n paradas, n+1 mar), `renderSello(r, i)`, `sello(r, i)`,
  `renderMercado(r, j)`, `renderGuia(r)`, `bloqueFrase(r, conLista)`, `mas(titulo, html)`, `laminaNave(r)`, `fichaAnimal(r)`,
  `bienPintado(r, gi)`, `perfilSVG(r)`, `textoAltura(r, i)`, `rival(V, e)`, `rango(n)`, `ico(clave)`, `botonVoz()`, `botones(a, b)`.
  El panel de hoy está en `renderDescender` (motor.js ≈ línea 624): tomar de ahí cada texto, sin cambiarlo.
- Mapa: SVG `#svg` con `#tierra`, `#relieve`, `#lagos`, `#fronteras`, `#capa` (lo que el motor redibuja en cada render), y encima
  los `div` `#luz`, `#clima`, `#olas`. `proj([lat,lon]) → [x,y]` con `x=(lon+180)/360*1000`, `y=(90−lat)/180*500`. `px` = unidades
  del SVG por píxel de pantalla: un tamaño constante en pantalla es `(n*px).toFixed(2)`. Clases que ya dibuja el motor: `.rio.activo`
  (lo recorrido), `.rio.activo.resto` (lo que falta), `.rio.brazo` (afluentes), `.ciudad` y `.ciudad.on` (paradas), `.halo`, `.etq`
  (nombres: solo los de paradas ya alcanzadas, `foco.etiquetas`), `.etq.relieve`, `#barca` (`.casco`, `.vela`, `.palo`, `.linea`,
  `.fig`), `#masc` (Hipo sobre la barca), `#estela`. `foco`: `{modo:'rio', rio, etiquetas:Set, actual, halo, corte, barca, frac}`.
- Sonido de hoy: `audio` (motor.js ≈ línea 227): ruido rosa filtrado con Web Audio, `audio.ping()` para la moneda, arranca con el
  botón «≈ sonido».

## CSS compartido (`src/vitrina/capa.css`)

Todo selector de la vitrina empieza por `body.vitrina`. Variables:

```
--v-mar:#0C3A33; --v-tierra:#215A4F; --v-tierra-baja:#174A3F; --v-tierra-alta:#2B6E5E; --v-oro:#E8B952; --v-crema:#FBF8F2;
--v-claro:#64C8AA; --v-tinta:#0F423A; --v-cuerpo:#2D2D2D; --v-sec:#6B6B6B; --v-tinte1:#E9F5F0; --v-tinte2:#B7E3D3;
--v-calido:#D89B85; --v-teja:#A6472E; --v-filete:rgba(15,66,58,.2); --v-tit:'Oswald','Arial Narrow',sans-serif;
--v-txt:'Source Sans 3','Source Sans Pro',-apple-system,'Segoe UI',sans-serif
```

Reglas de arte que valen para todos: el dorado es solo el río recorrido y la vela de la barca, y no entra en la bitácora (las
postales pintadas traen su protagonista dorada: son imagen, se quedan). Nada por debajo de 11 px. Todo lo tocable, 44 px o más.
Un solo título dominante por pantalla. Salidas de 200 a 350 ms; con `prefers-reduced-motion`, solo fundidos. Ningún emoji.
Memoria primero: fuera de las fichas de la guía y de la lista de la primera bajada, ningún nombre de parada futura aparece ni en la
carta ni en la bitácora.

## Herramienta de capturas (`tools/captura.js`, de Verificación; sin dependencias: Edge o Chrome del sistema por CDP)

```
node tools/captura.js foto <archivo.html> <salida.png> [390x844] ["js a evaluar antes de la foto"]
node tools/captura.js recorrido <archivo.html> <carpeta> [390x844] [mercader|historia]
```
