// Pruebas de Cauces: ejercita datos, preguntas, flujo completo, economía, guía, recitar, mapa y todo lo demás (test/casos.js).
// Uso: node test/pruebas.js  (o npm test, que además corre la instantánea). Termina con "TODO OK" o lanza el primer fallo.
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar,CAUCES}=require('./arnes');
montar(CAUCES);
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'casos.js'),'utf8'),{filename:'casos.js'});
