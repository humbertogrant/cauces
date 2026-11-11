# Plan de la corrida: vitrina del Nilo

Corrida autónoma según `instruccion-un-rio.md`, con el presupuesto por defecto: 60 minutos de reloj, de las 07:31 a las 08:31 del
2026-11-11. Rama `vitrina-nilo`, en un árbol de trabajo aparte (`proyectos/geo/cauces-vitrina`), sin push.

## Qué cambió desde que se escribió la instrucción (setiembre de 2026) y cómo se adapta

| La instrucción supone | El repositorio hoy | Qué se hace |
|---|---|---|
| 13 ríos; `dist/cauces.html` bajo ~400 KB | 25 ríos; económica con tope de 500 KB (≈ 459) y amplia con tope de 5 MB | Se respetan los topes de hoy; `dist/nilo.html` va aparte, bajo 900 KB |
| Curso a mano; «cauces reales» pendiente | El curso del Nilo ya es de Natural Earth 50 m, con un vértice por parada | Se conserva: cambiarlo al de 10 m mueve índices de parada; queda como pendiente |
| Sin relieve | Franjas de altura (≥ 500 y ≥ 2 000 m) y nombres de relieve | La vitrina cambia las franjas por un sombreado continuo de ETOPO1 |
| Sin perfil, sin sellos, sin sonido propio | Perfil de altura con datos reales, sellos con carácter, agua sintetizada | Se visten (perfil y sellos) y se extiende (sonido); no se rehacen |
| Hipo, la falúa, los bienes y las imágenes, por dibujar en línea plana | Hipo pintado con cinco ánimos, la falúa pintada, las cinco mercancías del Nilo y las ocho postales pintadas | Se usa lo pintado (ver «Decisiones») |
| Ningún nombre de parada futura, nunca | «Enseñar antes de preguntar» (lote 1, 2026-10-29): en la primera bajada, la frase con la lista antes de zarpar | Se respeta el lote 1; en todo lo demás, ningún nombre futuro |
| Playwright para las capturas | El scratchpad se limpia solo y Playwright pide descarga | Edge o Chrome del sistema por CDP, sin dependencias |

## Arquitectura

- `build.js` gana un juego, `nilo` (`dist/nilo.html`): los datos de Cauces amplia recortados al Nilo, `src/juegos/nilo.js`, la capa
  `src/vitrina/` y el motor.
- El motor lleva los ganchos entre `/*@vitrina*/ … /*@fin:vitrina*/`; el build los recorta de Cauces y de Exploradores, que quedan
  byte a byte iguales. Los ganchos, las fases y lo que exporta cada módulo están en `contrato.md`.
- Cuatro subagentes, cada uno dueño de sus archivos: Carta, Bitácora, Sonido y Verificación. Dirección integra.

## Orden de trabajo y reparto del reloj

| Tramo | Minutos | Qué |
|---|---|---|
| Leer y planear | 07:31 – 07:47 | Instrucción, referencia, `CLAUDE.md`, motor; rama y árbol; contrato; lanzar los subagentes |
| Construir | 07:47 – 08:08 | Ganchos y build (Dirección); carta, bitácora, sonido, herramienta de capturas y pruebas (subagentes) |
| Mirar y corregir | 08:08 – 08:24 | Integrar, `npm test`, recorrido con capturas, hallazgos, corregir los tres más graves, repetir |
| Informe | 08:24 – 08:31 | `informe.md`, `textos-nuevos.md`, sección en `CLAUDE.md`, commits |

Prioridad si el tiempo no alcanza (la de la instrucción): 1 la carta, 2 el hilo de oro y las paradas, 3 la bitácora, 4 la falúa e
Hipo (ya pintados), 5 portada y llegada, 6 el acróstico como progreso, 7 imágenes para recordar (ya pintadas), 8 perfil, 9 sonido.
Una pieza a medias que estorbe se desactiva antes de cerrar (basta con no cargar su módulo: el build se salta el archivo que falte).
