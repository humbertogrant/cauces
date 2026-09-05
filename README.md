# Cauces

Juego de un solo archivo para aprender los grandes ríos del mundo: se baja cada río de la fuente al mar,
ciudad por ciudad, con acrósticos, imágenes mnemónicas, una barca sobre el cauce real, un animal guía que habla,
un mercado, eventos entre puertos y repaso espaciado.

- Dos juegos con el mismo motor: `dist/cauces.html` (los grandes ríos) y `dist/exploradores.html` (los grandes viajes,
  etapa por etapa: Ibn Battuta, Marco Polo, Zheng He, Alejandro Magno y Hernán Cortés, cada uno con su caravana, flota o
  ejército, un animal de guía, una carga de trueque y una línea de tiempo bajo el mapa). Cada juego guarda su progreso aparte.
- Jugar: abrir `dist/cauces.html` (o `dist/exploradores.html`) en cualquier navegador. Basta un doble clic: no necesita servidor, instalación
  ni red (solo baja las fuentes de Google la primera vez; sin red usa las del sistema) y no llama a ningún
  servicio. Para el teléfono, copiar ese único archivo al aparato o subirlo a cualquier hosting estático.
- Ríos: trece grandes ríos del mundo y un paquete de Costa Rica (Tempisque, Reventazón, Sarapiquí, San Juan,
  Tárcoles y Térraba) con su historia económica; en el mapa mundial, el punto dorado sobre Costa Rica abre esa zona.
- Escenas: cada ciudad, cada fuente y cada desembocadura tienen su postal, compuesta con pictogramas de lo que
  hay ahí (presa, templo, puente, manglar…); en el reto de imagen la postal sirve de pista.
- Barcas y animales: dibujados en SVG propio (una barca por tipo, un animal por río), sin depender de los emojis
  del aparato.
- Relieve: al acercarse a un río, el mapa muestra las tierras altas en dos tonos (más de 500 y de 2 000 m; en Costa
  Rica, 500 y 1 500) con los nombres de cordilleras, mesetas, desiertos y llanuras, y en los ríos ticos los volcanes
  con su altura. Bajo el mapa, un perfil del cauce de la fuente al mar marca a qué altura va la barca, y cada parada
  dice a cuántos metros pasa el río. Alturas de NOAA (ETOPO1 y el mosaico DEM de NCEI), nombres de Natural Earth y
  OpenStreetMap. El reto pregunta en cuál parada pasa el río más alto.
- Luz y clima: el mapa amanece en la fuente y atardece en el mar, y los eventos traen su niebla, su lluvia o su
  tormenta de arena.
- Hoy: al abrir, el inicio dice cuántas tarjetas tocan repasar y cuántos minutos; las nuevas entran de a diez por
  día y el repaso intercala ríos.
- Niño o Adulto: un interruptor en el inicio. Niño (por defecto): mercado con monedas, el animal acompaña, los
  textos largos quedan plegados y la voz puede leer sola cada pantalla. Adulto: la historia completa y la carga
  fija de la ruta; el animal acompaña igual.
- Pasaporte: cada ciudad da un sello si se llega sabiendo adónde se iba (dorado cuando además se recuerda en el
  repaso); los ríos con todos sus sellos se pintan de dorado en el mapa.
- Progreso: se guarda en el navegador (`localStorage`), un progreso por perfil ("¿Quién juega?" en el inicio).
  En "Progreso" se puede guardar en un archivo `.json` y cargarlo en otro aparato o navegador.
- Desarrollar: editar `src/`, luego `npm test` y `npm run build`. Ver `CLAUDE.md` para todo lo demás.
