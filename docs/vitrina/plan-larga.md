# Plan de la corrida larga

Segunda corrida sobre la vitrina del Nilo, pedida por Humberto el 2026-11-11 («vamos con la corrida larga»). No dio un número:
**Decisión:** 180 minutos, de 08:27 a 11:27, dicho al empezar. Misma rama (`vitrina-nilo`), mismo alcance (solo el Nilo, solo
Bajar), mismas reglas; lo que sube es el acabado. Parte del commit 5ee97ff, el cierre de la corrida de 60 minutos.

## Qué le faltaba a cada pieza para el «nivel final»

| # | Pieza | Lo que faltaba | Quién |
|---|---|---|---|
| 1 | La carta | De cerca, el relieve se ve en manchas, la costa y los lagos son gruesos y el río es una poligonal; falta el halo de la costa | Carta |
| 1 | Curso real | Es el de Natural Earth 50 m; la instrucción pide el de 10 m, sin romper la barca ni los índices de parada | Carta (datos) y Dirección (enganche, con las cifras fijas) |
| 2 | Hilo de oro y paradas | Nada grave; revisar con la barca nueva | Carta |
| 3 | La bitácora | Sello circular propio; el riel de etapas no se ve en el teléfono; estados sin mirar (guía fallada, sello pendiente, bodega llena, anclada, Adulto) | Bitácora |
| 4 | La falúa e Hipo | La carga a la vista (el obelisco de Asuán) e Hipo nadando al lado | Trazo (dibujo) y Carta (colocación) |
| 5 | Portada y llegada | La hoja casi vacía en pantalla ancha | Bitácora |
| 6-8 | Acróstico, imágenes, perfil | Nada pendiente | — |
| 9 | Sonido | Sigue sin oírse; no se toca salvo que algo falle | Sonido |
| — | Verificación | Auditoría automática (letra de menos de 11 px, toques de menos de 44 px, contraste, ancho de página), catálogo de estados con captura, otros tamaños, prueba de cifras fijas | Verificación |

Fuera de alcance, como en la instrucción: Ordenar, Recitar y Preguntar (heredan papel y tipografía), mecánicas nuevas, datos del
juego. Sin descargas: no se embeben fuentes.

## Reparto del reloj

| Tramo | Hora | Qué |
|---|---|---|
| Planear | 08:27 – 08:35 | Plan, contrato ampliado, lanzar la vuelta A |
| Construir (vuelta A) | 08:35 – 09:20 | Trazo, Carta, Bitácora y Verificación en paralelo; Dirección: enganche del cauce fino, build |
| Mirar y corregir | 09:20 – 10:55 | Tres o cuatro vueltas: build, pruebas, recorridos, auditoría, mirar capturas, corregir lo más grave |
| Verificación final | 10:55 – 11:15 | Recorridos en los dos modos, capturas en tres tamaños, mediciones |
| Informe | 11:15 – 11:27 | Informe de la corrida larga, CLAUDE.md, commits |

## La regla nueva más delicada: el cauce fino no puede cambiar ninguna cifra

Con otro dibujo del río cambiarían los kilómetros de cada parada y la altura que se lee en cada una. `src/juegos/nilo.js`
(`cauceFino`) calcula los kilómetros con el curso de Cauces y los deja fijos, y pasa el perfil de altura al cauce nuevo corriendo
sus fracciones entre parada y parada. Probado antes de tener el cauce de verdad, con un curso torcido a propósito (405 vértices y
5 202 km de dibujo contra 203 y 4 944): kilómetros 0, 1 006, 3 014, 5 297, 5 566 y 6 394 y alturas 1 149, 457, 373, 106, 75 y 21 m,
iguales en los dos.
