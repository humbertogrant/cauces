// El mapa de la vitrina: cuando la carta trae sus propias costas, lagos y fronteras de la región (CARTA.tierra, CARTA.lagos y
// CARTA.bordes, de tools/carta.py: finos cerca del río, gruesos lejos), son los del juego, y el mapa del mundo de Cauces no viaja.
// build.js carga este archivo solo en ese caso, después de carta-datos.js y antes del motor.
const LAND=CARTA.tierra,LAGOS=CARTA.lagos||'',BORDES=CARTA.bordes||'';
