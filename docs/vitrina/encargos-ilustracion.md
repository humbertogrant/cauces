# Encargos de ilustración: las imágenes para recordar del Nilo

La instrucción pedía describir las seis imágenes como encargo, por si después se producían pintadas. Ya existen pintadas: son las
postales del Nilo que entraron el 2026-10-25 (`tools/dibujos/postales/nilo.py`, ocho con el nacimiento y el mar; ver «Postales» en
`CLAUDE.md`). La vitrina las usa tal cual en la tarjeta «Imagen para recordar», así que este documento queda como ficha de cada
una: sirve para repintarlas o para encargarlas a otra mano sin perder lo que tienen que decir.

## Lo que vale para todas

- **Qué pinta:** exactamente la imagen mnemónica que está escrita en `src/data/rios.js` (campo `imagen`), sin agregarle ideas.
- **Regla del protagonista** (2026-10-25): la imagen para recordar ocupa al menos un tercio del alto, va al medio y es lo único
  dorado de la postal. Sin sol, salvo que sea parte de la imagen.
- **Tamaño:** caja de dibujo de 120 × 40 (proporción 3 : 1); se entrega en WebP de 600 px de ancho, calidad 75, sin transparencia.
  En el teléfono se ve a 360 px de ancho: lo que no se lea a ese tamaño, no está.
- **Paleta:** la del juego. Verde oscuro `#0F423A` (tinta), verde claro `#64C8AA`, verdes de tierra `#215A4F` a `#2B6E5E`, agua
  verde azul, crema `#FBF8F2`, y un solo dorado, `#E8B952`, para la protagonista. El rojo teja `#A6472E` no se usa: es de los errores.
- **Cómo se revisa:** a 360 px, y con una lectura a ciegas (alguien que ve la postal sin saber el río ni la ciudad dice qué ve).

## Las seis paradas

| # | Parada | Texto mnemónico (del juego) | Protagonista dorada | Lo que hoy está pintado |
|---|---|---|---|---|
| 1 | Jinja (Uganda) | «Un jinete salta a caballo desde el lago Victoria: aquí nace el Nilo Blanco (Jinja suena a jinete).» | El caballo con su jinete, en el salto | El jinete que salta a caballo desde el lago, con el río que nace |
| 2 | Juba (Sudán del Sur) | «Un país recién nacido con chupón: Juba es la capital de Sudán del Sur, el Estado más joven del mundo (2011).» | El bebé con su chupón | El bebé con chupón y banderita de estrella en su canasta, frente al muelle |
| 3 | Jartum (Sudán) | «Dos jarras, una de agua blanca y otra azul, se vacían en el mismo cauce: Jartum es la confluencia del Nilo Blanco y el Nilo Azul.» | Las dos jarras | Las dos jarras de barro que vacían agua blanca y azul en un mismo cauce |
| 4 | Asuán (Egipto) | «Una aduana en el río: Asuán (a-duana) fue la frontera sur de Egipto en la primera catarata, y hoy la presa es la aduana del agua.» | La barrera de la aduana | La barrera a rayas que cruza el río, con la Presa Alta al fondo |
| 5 | Luxor (Egipto) | «Lujo (lux) de faraones: Luxor es la antigua Tebas, con Karnak en la orilla de los vivos y el Valle de los Reyes en la de los muertos.» | La máscara de oro | La máscara de oro en la orilla de las tumbas, con el sol que se pone, y Karnak enfrente |
| 6 | El Cairo (Egipto) | «El río cae (Cai-ro) en un abanico: aquí el Nilo se abre en el delta, la letra griega Δ que dio nombre a todos los deltas.» | El delta y su Δ | El delta abierto en abanico, visto desde el mar, con la Δ |

Las otras dos de la serie: el **nacimiento** (el Nilo Blanco, claro, y el Nilo Azul, oscuro, que nacen de los lagos Victoria y
Tana, con una V y una T doradas) y el **mar** (el faro de Alejandría, dorado, con la gabarra que va hacia él y la falúa de madera
que da la vuelta, porque la falúa no sale al mar).

## El dibujo de línea por defecto

Si una edición no trae las postales pintadas (la económica de Cauces), la tarjeta muestra la escena de pictogramas del motor
(`escena(c.escena)`): ese es el dibujo de línea por defecto. En la vitrina no hace falta: siempre viaja la pintada.
