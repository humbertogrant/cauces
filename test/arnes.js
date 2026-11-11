// Arnés compartido: simula un DOM mínimo y carga los archivos de un juego en este mismo contexto, en una edición:
// la amplia (por defecto) es la fuente entera con sus archivos generados finos; la económica recorta los bloques
// /*@amplia*/ … /*@fin:amplia*/ como build.js y carga los archivos generados económicos. La edición queda en EDICION.
// Uso: const {montar,archivosDe}=require('./arnes'); montar(archivosDe('cauces','amplia'),'amplia')
// También trae finesDeLinea(juego, edicion): comprueba que build.js arma el mismo HTML con los fuentes en CRLF que en LF.
const fs=require('fs'),path=require('path'),vm=require('vm');
const {EDICIONES,archivosDe,cortarEdicion,ensamblar}=require('../build.js');
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
/* build.js no depende de los fines de línea: con todos los fuentes en CRLF arma el mismo HTML, byte a byte, que con LF. No toca
   el disco: build.js lee src/ con fs.readFileSync y, mientras arma, aquí se le entrega el mismo texto con \r\n en cada renglón.
   Devuelve '' si todo va bien, o el texto del problema (cada prueba lo lanza a su manera) */
function finesDeLinea(id,edicion){const real=fs.readFileSync,raiz=path.join(__dirname,'..','src')+path.sep,lf=ensamblar(id,edicion).html;let n=0,crlf;
  fs.readFileSync=function(p,...mas){const t=real.call(fs,p,...mas);if(typeof t!=='string'||!path.resolve(String(p)).startsWith(raiz))return t;n++;return t.replace(/\r?\n/g,'\r\n')};
  try{crlf=ensamblar(id,edicion).html}catch(e){return 'con los fuentes en CRLF, build.js no logra armar '+id+' '+edicion+': '+(e&&e.message||e)}finally{fs.readFileSync=real}
  if(!n)return 'finesDeLinea no probó nada: build.js no leyó ningún fuente con fs.readFileSync';
  return crlf===lf?'':'con los fuentes en CRLF, build.js arma otro HTML de '+id+' '+edicion+' ('+crlf.length+' caracteres frente a '+lf.length+')'}
const CAUCES=archivosDe('cauces','amplia'),EXPLORADORES=archivosDe('exploradores','amplia');
module.exports={montar,finesDeLinea,archivosDe,EDICIONES,CAUCES,EXPLORADORES,JUEGOS:{cauces:CAUCES,exploradores:EXPLORADORES}};
