// Pruebas de un juego: node test/pruebas.js [cauces|exploradores] [amplia|economica]. Ejercita datos, preguntas, flujo completo, economía, guía,
// recitar, mapa y todo lo demás (test/casos.js para Cauces, test/casos-exploradores.js para Exploradores). Termina con "TODO OK".
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar,archivosDe,EDICIONES,JUEGOS}=require('./arnes');
const juego=process.argv[2]||'cauces',edicion=process.argv[3]||'amplia';if(!JUEGOS[juego]||!EDICIONES[edicion])throw 'uso: node test/pruebas.js [cauces|exploradores] [amplia|economica]';
global.LS=montar(archivosDe(juego,edicion),edicion);
const casos=juego==='cauces'?'casos.js':'casos-'+juego+'.js';
vm.runInThisContext(fs.readFileSync(path.join(__dirname,casos),'utf8'),{filename:casos});
