# Cauces

Juego de un solo archivo para aprender los grandes ríos del mundo: se baja cada río de la fuente al mar,
ciudad por ciudad, con acrósticos, imágenes mnemónicas, una barca sobre el cauce real, un animal guía que habla,
un mercado, eventos entre puertos y repaso espaciado.

- Dos juegos con el mismo motor: `dist/cauces.html` (los grandes ríos) y `dist/exploradores.html` (los grandes viajes,
  etapa por etapa: Ibn Battuta, Marco Polo, Zheng He, Odiseo, Alejandro Magno y Hernán Cortés, cada uno con su caravana,
  flota o ejército, un animal de guía, una carga de trueque y una línea de tiempo bajo el mapa). En los viajes la memoria es
  la del viaje entero: cada etapa dice cuántos kilómetros y años lleva, la guía pregunta hacia dónde sigue, Ordenar va por
  tramos, Trazar reconstruye la forma del viaje tocando el mapa y las preguntas miden la magnitud: cuánto duró, hasta dónde
  llegó, qué mares y desiertos cruzó, cuál viaje fue primero. Cada juego guarda su progreso aparte; cada archivo pesa menos de medio megabyte y lleva solo lo que su juego usa.
- En línea: <https://humbertogrant.github.io/cauces/> (Cauces en `cauces.html`, Exploradores en `exploradores.html`). Es la misma
  carpeta `dist`, publicada por GitHub Pages con cada cambio de `main`; desde ahí abre también en iPhone.
- Jugar: abrir `dist/cauces.html` (o `dist/exploradores.html`) en cualquier navegador. Basta un doble clic: no necesita servidor, instalación
  ni red (solo baja las fuentes de Google la primera vez; sin red usa las del sistema) y no llama a ningún
  servicio. En Android basta copiar el archivo al aparato y abrirlo con el navegador. En iPhone, no: la app Archivos (y el
  adjunto de correo o WhatsApp) solo muestra una vista previa sin JavaScript, y se ve el fondo vacío; en iPhone se abre la dirección
  de arriba en Safari (o cualquier otro hosting estático, o una app que sirva HTML local).
- Ríos: quince grandes ríos del mundo, con el Congo y el Huang He recién llegados, y un paquete de Costa Rica (Tempisque, Reventazón, Sarapiquí, San Juan,
  Tárcoles y Térraba) con su historia económica; en el mapa mundial, el punto dorado sobre Costa Rica abre esa zona.
- Escenas: cada ciudad, cada fuente y cada desembocadura tienen su postal, compuesta con pictogramas de lo que
  hay ahí (presa, templo, puente, manglar…); en el reto de imagen la postal sirve de pista.
- Barcas, animales e iconos: dibujados en SVG propio (una barca por tipo, un animal por río y un juego de iconos de
  línea para los bienes, los eventos y los controles), sin depender de los emojis del aparato.
- Navegación: la pregunta de la próxima parada y el botón de zarpar viven en una barra fija al pie, siempre al alcance
  del pulgar, con el riel Bajar · Ordenar · Recitar · Preguntar que marca lo ya hecho; la portada empieza por «Hoy» y
  muestra los ríos en tarjetas por continente. Panel de papel cálido, mapa oscuro, dos tipos de bloque (la voz del
  animal y la ficha) y dorado solo para «estás aquí».
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
