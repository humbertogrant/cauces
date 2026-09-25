// Pruebas de un juego: node test/pruebas.js [cauces|exploradores] [amplia|economica]. Ejercita datos, preguntas, flujo completo, economía, guía,
// recitar, mapa y todo lo demás (test/casos.js para Cauces, test/casos-exploradores.js para Exploradores). Termina con "TODO OK".
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar,archivosDe,EDICIONES,JUEGOS}=require('./arnes');
const juego=process.argv[2]||'cauces',edicion=process.argv[3]||'amplia';if(!JUEGOS[juego]||!EDICIONES[edicion])throw 'uso: node test/pruebas.js [cauces|exploradores] [amplia|economica]';
global.LS=montar(archivosDe(juego,edicion),edicion);
// procedencia de las ilustraciones (edición amplia): una pintada (`i`) tiene su dibujo de memoria en tools/dibujos/<clave>.py; una de
// vectores (`d`), su contorno en tools/ilustraciones/, anotado en fuentes.json, de dominio público o CC0
if(edicion==='amplia'){const raiz=path.join(__dirname,'..'),dir=path.join(raiz,'tools','ilustraciones'),fu=JSON.parse(fs.readFileSync(path.join(dir,'fuentes.json'),'utf8')),datos=fs.readFileSync(path.join(dir,'ilustraciones_datos.py'),'utf8');
  let pintadas=0,contornos=0;for(const l of fs.readFileSync(path.join(raiz,'src','data','ilustraciones.js'),'utf8').split('\n')){const k=(l.match(/^([a-zñ]+):\{v:/)||[])[1];if(!k)continue;
    if(/i:'data:image\/webp;base64,/.test(l)){if(!fs.existsSync(path.join(raiz,'tools','dibujos',k+'.py')))throw 'ilustración pintada sin su dibujo: '+k;pintadas++;continue}
    const f=(datos.match(new RegExp("'"+k+"': dict\\(\\s*fuente='([^']+)'"))||[])[1],x=f&&fu[f];if(!x||!fs.existsSync(path.join(dir,f))||!/^(CC0|Dominio público)/.test(x.licencia)||!x.autor||!x.pagina)throw 'contorno sin procedencia libre: '+k;contornos++}
  if(!pintadas&&!contornos)throw 'ilustraciones vacías';console.log('ilustraciones: '+pintadas+' dibujadas de memoria (tools/dibujos), '+contornos+' sobre contornos de PhyloPic');
  // y las barcas y las mercancías pintadas: cada una con su dibujo en tools/dibujos/barcas/ o tools/dibujos/bienes/
  let barcas=0,bienes=0;
  for(const [archivo,carpeta] of [['barcas.js','barcas'],['bienes.js','bienes']])for(const l of fs.readFileSync(path.join(raiz,'src','data',archivo),'utf8').split('\n')){const k=(l.match(/^([a-z]+):[{[]/)||[])[1];if(!k)continue;
    if(!fs.existsSync(path.join(raiz,'tools','dibujos',carpeta,k+'.py')))throw 'pintada sin su dibujo: '+carpeta+'/'+k;if(carpeta==='barcas')barcas++;else bienes+=(l.match(/data:image\/webp/g)||[]).length}
  console.log('barcas: '+barcas+' pintadas · mercancías: '+bienes+' pintadas')}
const casos=juego==='cauces'?'casos.js':'casos-'+juego+'.js';
vm.runInThisContext(fs.readFileSync(path.join(__dirname,casos),'utf8'),{filename:casos});
