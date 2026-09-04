// Arnés de pruebas de Cauces: simula un DOM mínimo y ejercita datos, preguntas, flujo completo, economía, guía, recitar y mapa.
// Uso: node test/pruebas.js  (o npm test). Termina con "TODO OK" o lanza el primer fallo.
const fs=require('fs'),path=require('path'),vm=require('vm');
global.nodo=()=>({innerHTML:'',textContent:'',clientWidth:380,clientHeight:300,style:{},setAttribute(k,v){this['_'+k]=v},classList:{toggle(){return true},contains(){return true}}});
global.nodos={};
global.document={querySelectorAll:()=>[],querySelector:s=>nodos[s]||(nodos[s]=nodo()),getElementById:s=>nodos['#'+s]||(nodos['#'+s]=nodo())};
const LS={};
global.window={matchMedia:()=>({matches:false}),scrollTo(){},addEventListener(){},
  localStorage:{getItem:k=>Object.prototype.hasOwnProperty.call(LS,k)?LS[k]:null,setItem(k,v){LS[k]=String(v)},removeItem(k){delete LS[k]}},
  speechSynthesis:{cola:[],cancel(){this.cola.length=0},speak(u){this.cola.push(u)},getVoices(){return[{lang:'en-US',name:'Zira'},{lang:'es-MX',name:'Sabina'},{lang:'es-CR',name:'María'}]}}};
global.SpeechSynthesisUtterance=function(t){this.text=t};
global.requestAnimationFrame=f=>0;global.cancelAnimationFrame=()=>{};

for(const f of ['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/mercados.js','data/eventos.js','data/relieve.js','motor.js']){
  vm.runInThisContext(fs.readFileSync(path.join(__dirname,'..','src',f),'utf8'),{filename:f});
}
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'casos.js'),'utf8'),{filename:'casos.js'});
