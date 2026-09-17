// Pruebas de un juego: node test/pruebas.js [cauces|exploradores] [amplia|economica]. Ejercita datos, preguntas, flujo completo, economía, guía,
// recitar, mapa y todo lo demás (test/casos.js para Cauces, test/casos-exploradores.js para Exploradores). Termina con "TODO OK".
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar,archivosDe,EDICIONES,JUEGOS}=require('./arnes');
const juego=process.argv[2]||'cauces',edicion=process.argv[3]||'amplia';if(!JUEGOS[juego]||!EDICIONES[edicion])throw 'uso: node test/pruebas.js [cauces|exploradores] [amplia|economica]';
global.LS=montar(archivosDe(juego,edicion),edicion);
// procedencia de las ilustraciones (edición amplia): cada contorno es un archivo de tools/ilustraciones/ anotado en fuentes.json, de dominio público o CC0
if(edicion==='amplia'){const dir=path.join(__dirname,'..','tools','ilustraciones'),fu=JSON.parse(fs.readFileSync(path.join(dir,'fuentes.json'),'utf8')),usados=[...fs.readFileSync(path.join(dir,'ilustraciones_datos.py'),'utf8').matchAll(/fuente='([^']+)'/g)].map(m=>m[1]);
  if(!usados.length)throw 'ilustraciones sin contornos';for(const f of usados){const x=fu[f];if(!fs.existsSync(path.join(dir,f))||!x||!/^(CC0|Dominio público)/.test(x.licencia)||!x.autor||!x.pagina)throw 'contorno sin procedencia libre: '+f}
  console.log('ilustraciones: '+usados.length+' contornos con procedencia')}
const casos=juego==='cauces'?'casos.js':'casos-'+juego+'.js';
vm.runInThisContext(fs.readFileSync(path.join(__dirname,casos),'utf8'),{filename:casos});
