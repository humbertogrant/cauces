// Arnés compartido: simula un DOM mínimo y carga los archivos de un juego en este mismo contexto, en una edición:
// la amplia (por defecto) es la fuente entera con sus archivos generados finos; la económica recorta los bloques
// /*@amplia*/ … /*@fin:amplia*/ como build.js y carga los archivos generados económicos. La edición queda en EDICION.
// Uso: const {montar,archivosDe}=require('./arnes'); montar(archivosDe('cauces','amplia'),'amplia')
const fs=require('fs'),path=require('path'),vm=require('vm');
const {EDICIONES,archivosDe,cortarEdicion}=require('../build.js');
function montar(archivos,edicion='amplia'){
  global.nodo=()=>({innerHTML:'',textContent:'',clientWidth:380,clientHeight:300,style:{},setAttribute(k,v){this['_'+k]=v},classList:{toggle(){return true},contains(){return true}}});
  global.nodos={};
  global.document={querySelectorAll:()=>[],querySelector:s=>nodos[s]||(nodos[s]=nodo()),getElementById:s=>nodos['#'+s]||(nodos['#'+s]=nodo())};
  const LS={};
  global.window={matchMedia:()=>({matches:false}),scrollTo(){},addEventListener(){},
    localStorage:{getItem:k=>Object.prototype.hasOwnProperty.call(LS,k)?LS[k]:null,setItem(k,v){LS[k]=String(v)},removeItem(k){delete LS[k]}},
    speechSynthesis:{cola:[],cancel(){this.cola.length=0},speak(u){this.cola.push(u)},getVoices(){return[{lang:'en-US',name:'Zira'},{lang:'es-MX',name:'Sabina'},{lang:'es-CR',name:'María'}]}}};
  global.SpeechSynthesisUtterance=function(t){this.text=t};
  global.requestAnimationFrame=f=>0;global.cancelAnimationFrame=()=>{};
  global.EDICION=edicion;
  for(const f of archivos)vm.runInThisContext(cortarEdicion(fs.readFileSync(path.join(__dirname,'..','src',f),'utf8'),edicion),{filename:f});
  return LS}
const CAUCES=archivosDe('cauces','amplia'),EXPLORADORES=archivosDe('exploradores','amplia');
module.exports={montar,archivosDe,EDICIONES,CAUCES,EXPLORADORES,JUEGOS:{cauces:CAUCES,exploradores:EXPLORADORES}};
