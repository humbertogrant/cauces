#!/usr/bin/env node
// Capturas y medidas del juego con el Edge o el Chrome del sistema, sin pantalla y sin dependencias: se le habla por el
// protocolo DevTools (CDP) con el WebSocket y el fetch que trae Node (22 o más). Es de Verificación (ver docs/vitrina/contrato.md).
//
//   node tools/captura.js foto <archivo.html> <salida.png> [390x844] ["js a evaluar antes de la foto"]
//   node tools/captura.js recorrido <archivo.html> <carpeta> [390x844] [mercader|historia]
//   node tools/captura.js medir <archivo.html> [390x844] [carpeta para las cinco capturas del viaje]
//   node tools/captura.js auditar <archivo.html> [390x844] [salida.json] [solo=estado,estado]
//   node tools/captura.js estados <archivo.html> <carpeta> [390x844] [solo=estado,estado]
//
// auditar: arma cada estado del catálogo (CATALOGO, más abajo: la portada, navegar, la guía sin responder, bien y mal, la parada con
//   el sello nuevo y con el sello pendiente, el mercado lleno, el evento, la barca anclada, el mar, en Niño y en Adulto) con funciones
//   del motor y mide en cada uno: el texto más chico y los de menos de 11 px (en píxeles de pantalla, también los del SVG), lo
//   tocable de menos de 44 px, el contraste de cada texto HTML contra su fondo (menos de 4,5 a 1; lo que va sobre el mapa o una imagen
//   se cuenta aparte), si la página es más ancha que la ventana, nombres de paradas futuras en la carta, emojis, textos cortados por
//   el borde, por el pie o por su caja, y rótulos de la carta tapados o encimados. Imprime un resumen y deja el JSON en
//   docs/vitrina/capturas/auditoria.json (auditoria-<ancho>x<alto>.json con otro tamaño). Sale con código 1 si hay página ancha,
//   nombres futuros, emojis, errores de consola o un estado que no se pudo armar.
// estados: una captura por estado del mismo catálogo (NN-estado.png) y un estados.json.
// El tamaño admite la escala: 1440x900@1 (si no, escala 2).
//
// foto: emula el tamaño (escala 2; móvil si el ancho es < 760), carga, espera al juego, evalúa el JS, espera ≈ 1,2 s y guarda.
// recorrido: perfil limpio, el modo pedido y baja el Nilo entero con clics de verdad (Input.dispatchMouseEvent en el centro del
//   botón); una captura numerada por pantalla y un recorrido.json con los pasos, los tiempos y los errores de consola.
// medir: con la CPU frenada 4×, los cuadros de un viaje de la barca (mediana de cuadros por segundo y cuadro más largo), cinco
//   capturas a lo largo del viaje, la barca contra el curso del río y, si existe, CAPA.sonido.probar(). Imprime un JSON.
// Los tres salen con código 1 si hubo errores de consola o excepciones (recorrido, también si no llegó al mar).
// El navegador: msedge.exe o chrome.exe en sus carpetas de siempre, o el que diga la variable CAPTURA_NAVEGADOR.
'use strict';
const fs=require('fs'),os=require('os'),path=require('path'),{spawn,spawnSync}=require('child_process'),{pathToFileURL}=require('url');
const NAVEGADORES=['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe','C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe','C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'];
const dormir=ms=>new Promise(r=>setTimeout(r,ms));

/* ---------- el navegador ---------- */
class CDP{
  constructor(url){this.ws=new WebSocket(url);this.id=0;this.pend=new Map();this.oyentes=[];
    this.listo=new Promise((ok,no)=>{this.ws.addEventListener('open',()=>ok());this.ws.addEventListener('error',e=>no(new Error('WebSocket: '+((e&&e.message)||'no conectó'))))});
    this.ws.addEventListener('message',ev=>{const m=JSON.parse(typeof ev.data==='string'?ev.data:Buffer.from(ev.data).toString());
      if(m.id&&this.pend.has(m.id)){const {ok,no,metodo}=this.pend.get(m.id);this.pend.delete(m.id);m.error?no(new Error(metodo+': '+m.error.message)):ok(m.result)}
      else if(m.method)for(const f of this.oyentes.slice())f(m.method,m.params)});
    this.ws.addEventListener('close',()=>{for(const {no,metodo} of this.pend.values())no(new Error(metodo+': se cerró la conexión'));this.pend.clear()})}
  send(metodo,params={}){const id=++this.id;return new Promise((ok,no)=>{this.pend.set(id,{ok,no,metodo});this.ws.send(JSON.stringify({id,method:metodo,params}))})}
  on(f){this.oyentes.push(f)}
  una(metodo,ms=30000){return new Promise((ok,no)=>{const quitar=()=>{clearTimeout(t);this.oyentes=this.oyentes.filter(x=>x!==f)},f=(m,p)=>{if(m===metodo){quitar();ok(p)}},t=setTimeout(()=>{quitar();no(new Error('no llegó '+metodo+' en '+ms+' ms'))},ms);this.oyentes.push(f)})}
  cerrar(){try{this.ws.close()}catch(e){}}}

async function lanzar(){
  const pedido=process.env.CAPTURA_NAVEGADOR,exe=pedido&&fs.existsSync(pedido)?pedido:NAVEGADORES.find(p=>fs.existsSync(p));
  if(!exe)throw new Error('no encontré msedge.exe ni chrome.exe (se puede dar la ruta en CAPTURA_NAVEGADOR)');
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'captura-'));
  const proc=spawn(exe,['--headless=new','--remote-debugging-port=0','--remote-allow-origins=*','--user-data-dir='+dir,'--hide-scrollbars','--mute-audio','--no-first-run','--no-default-browser-check','--disable-extensions','about:blank'],{stdio:'ignore',windowsHide:true});
  let salio=false;proc.on('exit',()=>{salio=true});
  const fPuerto=path.join(dir,'DevToolsActivePort');let puerto=null,wsNav=null;
  for(let i=0;i<200&&!puerto&&!salio;i++){await dormir(100);try{const t=fs.readFileSync(fPuerto,'utf8').split(/\r?\n/);if(+t[0]&&t[1]){puerto=+t[0];wsNav=t[1]}}catch(e){}}
  const cerrar=async()=>{
    if(puerto&&!salio)try{const b=new CDP(`ws://127.0.0.1:${puerto}${wsNav}`);await Promise.race([b.listo.then(()=>b.send('Browser.close')).catch(()=>{}),dormir(2000)]);b.cerrar()}catch(e){}
    for(let i=0;i<30&&!salio;i++)await dormir(100);
    if(!salio){try{spawnSync('taskkill',['/PID',String(proc.pid),'/T','/F'],{stdio:'ignore'})}catch(e){}try{proc.kill()}catch(e){}await dormir(300)}
    for(let i=0;i<20;i++){try{fs.rmSync(dir,{recursive:true,force:true});if(!fs.existsSync(dir))break}catch(e){}await dormir(250)}};
  if(!puerto){await cerrar();throw new Error('el navegador no abrió el puerto de DevTools: '+exe)}
  return {exe,dir,puerto,cerrar}}

/* la página: carga un archivo local, evalúa, hace clic, saca fotos y junta los errores de consola */
const LISTO=`typeof S!=='undefined'&&typeof render==='function'&&!!document.querySelector('#panel')&&document.querySelector('#panel').innerHTML.length>40`;
async function abrir(archivo,tam){
  const ruta=path.resolve(archivo);if(!fs.existsSync(ruta))throw new Error('no existe '+ruta);
  const nav=await lanzar();
  try{
    let pag=null;for(let i=0;i<50&&!pag;i++){try{pag=(await (await fetch(`http://127.0.0.1:${nav.puerto}/json/list`)).json()).find(t=>t.type==='page')}catch(e){}if(!pag)await dormir(100)}
    if(!pag)throw new Error('el navegador no tiene ninguna página');
    const cdp=new CDP(pag.webSocketDebuggerUrl);await cdp.listo;
    const errores=[],avisos=[];
    cdp.on((m,p)=>{
      if(m==='Runtime.exceptionThrown'){const d=p.exceptionDetails;errores.push({tipo:'excepción',texto:(d.exception&&d.exception.description)||d.text,url:d.url||'',linea:d.lineNumber})}
      else if(m==='Log.entryAdded'&&p.entry.level==='error'){const e=p.entry,o={tipo:'log:'+e.source,texto:e.text,url:e.url||''};
        (e.source==='network'&&/fonts\.(googleapis|gstatic)\.com/.test(o.url+' '+o.texto)?avisos:errores).push(o)}   /* sin red, las fuentes de Google no cargan: es un aviso, no un error del juego */
      else if(m==='Runtime.consoleAPICalled'&&p.type==='error')errores.push({tipo:'console.error',texto:p.args.map(a=>a.value!==undefined?String(a.value):(a.description||'')).join(' ')})});
    await cdp.send('Page.enable');await cdp.send('Runtime.enable');await cdp.send('Log.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride',{width:tam.w,height:tam.h,deviceScaleFactor:tam.k||2,mobile:tam.w<760});
    const ev=async(expr,espera)=>{const r=await cdp.send('Runtime.evaluate',{expression:expr,returnByValue:true,awaitPromise:!!espera,userGesture:true});
      if(r.exceptionDetails)throw new Error('al evaluar «'+expr.slice(0,80)+'»: '+((r.exceptionDetails.exception&&r.exceptionDetails.exception.description)||r.exceptionDetails.text));return r.result.value};
    const listo=async()=>{let ok=false;for(let i=0;i<150&&!ok;i++){ok=await ev(LISTO).catch(()=>false);if(!ok)await dormir(100)}
      if(!ok)throw new Error('el juego no arrancó en 15 s (no hay S, render o #panel)');
      await Promise.race([ev(`document.fonts?document.fonts.ready.then(()=>true):true`,true).catch(()=>{}),dormir(2500)]);await dormir(250)};
    const url=pathToFileURL(ruta).href;
    const cargar=async()=>{const p=cdp.una('Page.loadEventFired');await cdp.send('Page.navigate',{url});await p;await listo()};
    const recargar=async()=>{const p=cdp.una('Page.loadEventFired');await cdp.send('Page.reload');await p;await listo()};
    const clic=async(x,y)=>{await cdp.send('Input.dispatchMouseEvent',{type:'mouseMoved',x,y});await cdp.send('Input.dispatchMouseEvent',{type:'mousePressed',x,y,button:'left',clickCount:1});await cdp.send('Input.dispatchMouseEvent',{type:'mouseReleased',x,y,button:'left',clickCount:1})};
    const captura=async()=>Buffer.from((await cdp.send('Page.captureScreenshot',{format:'png'})).data,'base64');
    const foto=async salida=>{const b=await captura();fs.mkdirSync(path.dirname(path.resolve(salida)),{recursive:true});fs.writeFileSync(salida,b)};
    return {cdp,ev,cargar,recargar,clic,foto,captura,escala:tam.k||2,errores,avisos,url,navegador:nav.exe,cerrar:async()=>{cdp.cerrar();await nav.cerrar()}}
  }catch(e){await nav.cerrar();throw e}}

/* ---------- lo que se le pregunta a la página ---------- */
const ESTADO=`(()=>{try{const r=S.rio?rioPor(S.rio):null,g=S.guias&&S.guias[S.paso],E=S.evento,pie=document.getElementById('pie'),hayCapa=typeof CAPA!=='undefined';
  return {pantalla:S.pantalla,tab:S.tab,rio:S.rio,paso:S.paso,n:r?r.paradas.length:null,parada:r&&S.paso>=1&&S.paso<=r.paradas.length?r.paradas[S.paso-1].nombre:null,zarpo:!!S.zarpo,
    evento:E?{tramo:E.tramo,resp:E.resp==null?null:E.resp,correcta:E.q.correcta}:null,guia:g?{objetivo:g.objetivo,resp:g.resp==null?null:g.resp,ok:g.ok}:null,
    fase:hayCapa?CAPA.fase:null,momento:hayCapa&&CAPA.momento?CAPA.momento():null,modo:P.modo,monedas:S.eco?S.eco.monedas:null,
    ventana:innerWidth+'x'+innerHeight,anchoPagina:document.documentElement.scrollWidth,scrollY:Math.round(window.scrollY),escala:window.visualViewport?Math.round(visualViewport.scale*1000)/1000:1,pie:pie&&!pie.hidden?(pie.innerText||'').replace(/\\s+/g,' ').trim().slice(0,160):''}}catch(e){return {error:String(e)}}})()`;
/* qué tocar ahora: en la portada, lo que abre el Nilo; en un evento, la opción correcta; si no, un botón del pie que empiece por
   «Zarpar a», «Llegar al mar», «Seguir hacia» o «Zarpar», o la ficha correcta de la guía; después, lo mismo en el panel */
const BUSCAR=`(()=>{const vis=b=>{if(!b||b.disabled)return false;const q=b.getBoundingClientRect(),c=getComputedStyle(b);return q.width>0&&q.height>0&&c.visibility!=='hidden'&&c.display!=='none'};
  const txt=b=>(b.innerText||b.textContent||'').replace(/\\s+/g,' ').trim(),oc=b=>b.getAttribute('onclick')||'';
  const todos=s=>[...document.querySelectorAll(s)].filter(vis),con=(s,p)=>todos(s).find(b=>txt(b).toLowerCase().indexOf(p.toLowerCase())===0);
  const E=S.evento,g=S.guias&&S.guias[S.paso],PREF=['Zarpar a','Llegar al mar','Seguir hacia','Zarpar'];let el=null,motivo='';
  if(S.pantalla==='inicio'){el=todos('#panel button,#panel [onclick],#pie button').find(b=>/abrirRio\\('nilo'/.test(oc(b)));motivo='abre el Nilo desde la portada'}
  else if(E&&E.resp==null){el=todos('#panel .opciones button')[E.q.correcta];motivo='opción correcta del evento'}
  else{for(const s of ['#pie','#panel']){
      for(const p of PREF){el=con(s+' button',p);if(el){motivo=s+': «'+p+'»';break}}
      if(!el&&g&&g.resp==null&&S.paso<rioPor(S.rio).paradas.length){const r=rioPor(S.rio),nom=r.paradas[g.objetivo].nombre;
        el=todos(s+' .chip').find(b=>new RegExp('responderGuia\\\\('+g.objetivo+'\\\\)').test(oc(b)))||todos(s+' .chip').find(b=>txt(b)===nom);if(el)motivo=s+': ficha correcta de la guía'}
      if(el)break}
    if(!el){el=con('#pie button','Siguiente');if(el)motivo='#pie: «Siguiente»'}}
  if(!el)return null;
  /* como haría una persona: la página solo se mueve si el botón no está entero a la vista */
  {const q0=el.getBoundingClientRect();if(q0.top<0||q0.left<0||q0.bottom>innerHeight||q0.right>innerWidth)el.scrollIntoView({block:'center',inline:'center',behavior:'instant'})}
  const q=el.getBoundingClientRect(),x=q.left+q.width/2,y=q.top+q.height/2,enc=document.elementFromPoint(x,y),libre=!!enc&&(enc===el||el.contains(enc));
  /* el clic va en píxeles de pantalla: si la página no cabe a lo ancho, el navegador la achica (visualViewport.scale < 1) y hay que convertir */
  const vv=window.visualViewport,kv=vv?vv.scale:1,ox=vv?vv.offsetLeft:0,oy=vv?vv.offsetTop:0;
  return {x:Math.round((x-ox)*kv*10)/10,y:Math.round((y-oy)*kv*10)/10,ancho:Math.round(q.width),alto:Math.round(q.height),texto:txt(el).slice(0,60),motivo,tapado:!libre,escala:Math.round(kv*1000)/1000,
    encima:libre||!enc?null:(enc.tagName.toLowerCase()+(enc.id?'#'+enc.id:'')+(typeof enc.className==='string'&&enc.className.trim()?'.'+enc.className.trim().replace(/\\s+/g,'.'):''))}})()`;
function etiqueta(e){
  if(!e||e.error)return 'error';
  if(e.pantalla==='inicio')return 'portada';
  if(e.pantalla!=='rio')return e.pantalla;
  if(e.tab!=='descender')return e.tab;
  if(e.evento)return 'evento-tramo-'+e.evento.tramo+(e.evento.resp==null?'':'-resuelto');
  if(e.paso>e.n)return 'mar';
  const resp=!!e.guia&&e.guia.resp!=null,nav=e.fase?e.fase==='navega':(e.zarpo&&!!e.guia&&!resp);
  if(e.paso===0)return resp?'navega-respondida':nav?'navega':'inicio';
  return 'parada-'+e.paso+(resp?'-respondida':e.fase&&nav?'-navega':'')}

/* ---------- los subcomandos ---------- */
function decir(s){console.log(s)}
function listar(errores,avisos){
  if(avisos.length)decir('avisos ('+avisos.length+'): '+avisos.map(a=>a.texto+(a.url?' ['+a.url.slice(0,70)+']':'')).join(' | '));
  if(errores.length){decir('ERRORES DE CONSOLA ('+errores.length+'):');for(const e of errores)decir('  · '+e.tipo+': '+String(e.texto).split('\n').slice(0,3).join(' // ')+(e.url?' ['+e.url.slice(-60)+(e.linea!=null?':'+e.linea:'')+']':''))}
  else decir('sin errores de consola')}

async function cmdFoto(archivo,salida,tam,js){
  const s=await abrir(archivo,tam);
  try{await s.cargar();if(js){const valor=await s.ev(js,true);if(valor!==undefined)decir('js → '+JSON.stringify(valor))}await dormir(1200);await s.foto(salida);
    decir('foto: '+salida+' ('+tam.w+'x'+tam.h+', escala 2, '+path.basename(s.navegador)+')');listar(s.errores,s.avisos);return s.errores.length?1:0}
  finally{await s.cerrar()}}

async function cmdRecorrido(archivo,carpeta,tam,modo){
  const s=await abrir(archivo,tam),t0=Date.now(),pasos=[];let llego=false,fallo=null,k=0;
  try{
    await s.cargar();await s.ev('localStorage.clear()');await s.recargar();
    /* el modo se guarda y se recarga: la vitrina abre el río al arrancar, y cambiar el modo después dejaría la bajada a medias
       entre los dos (la economía de Niño ya iniciada, con los textos de Adulto) */
    await s.ev(`setModo(${JSON.stringify(modo)})`);await s.recargar();await dormir(500);
    fs.mkdirSync(carpeta,{recursive:true});for(const f of fs.readdirSync(carpeta))if(/^\d\d-.*\.png$/.test(f)||f==='recorrido.json')fs.unlinkSync(path.join(carpeta,f));
    const guardar=async(e,extra)=>{k++;const captura=String(k).padStart(2,'0')+'-'+etiqueta(e)+'.png';await s.foto(path.join(carpeta,captura));pasos.push(Object.assign({n:k,captura,t:Date.now()-t0},extra,{estado:e}));return captura};
    let e=await s.ev(ESTADO);await guardar(e,{accion:'perfil limpio, modo '+modo});
    let atascos=0;
    for(let i=0;i<150;i++){
      e=await s.ev(ESTADO);if(e.error){fallo='estado: '+e.error;break}
      if(e.pantalla==='rio'&&e.n!=null&&e.paso===e.n+1){llego=true;break}
      const b=await s.ev(BUSCAR);if(!b){fallo='no encontré qué tocar en «'+etiqueta(e)+'» (pie: '+e.pie+')';break}
      await dormir(60);const antes=JSON.stringify(e),tc=Date.now();await s.clic(b.x,b.y);
      let d=e,cambio=false;for(let j=0;j<70&&!cambio;j++){await dormir(60);d=await s.ev(ESTADO);cambio=JSON.stringify(d)!==antes}
      const ms=Date.now()-tc,viaje=cambio&&(d.paso!==e.paso||(!!d.evento)!==(!!e.evento)),mar=d.n!=null&&d.paso===d.n+1;
      await dormir(mar?3200:viaje?1800:cambio?550:200);
      const extra={accion:'clic en «'+b.texto+'»',motivo:b.motivo,x:b.x,y:b.y,boton:b.ancho+'x'+b.alto,ms};if(b.tapado){extra.tapado=true;extra.encima=b.encima}
      if(!cambio){atascos++;extra.sinCambio=true;await guardar(d,extra);if(atascos>=3){fallo='tres clics seguidos sin cambio en «'+etiqueta(d)+'» (el último, en «'+b.texto+'»'+(b.tapado?', tapado por '+b.encima:'')+')';break}}
      else{atascos=0;await guardar(await s.ev(ESTADO),extra)}}
    if(!llego&&!fallo)fallo='demasiados pasos sin llegar al mar';
  }catch(err){fallo=String(err&&err.message||err)}
  finally{
    const informe={archivo:path.relative(process.cwd(),path.resolve(archivo)).replace(/\\/g,'/'),tam:tam.w+'x'+tam.h,modo,navegador:path.basename(s.navegador),fecha:new Date().toISOString(),duracionMs:Date.now()-t0,llegoAlMar:llego,fallo,capturas:pasos.length,errores:s.errores,avisos:s.avisos,pasos};
    try{fs.mkdirSync(carpeta,{recursive:true});fs.writeFileSync(path.join(carpeta,'recorrido.json'),JSON.stringify(informe,null,1))}catch(e){}
    await s.cerrar();
    decir('recorrido: '+informe.archivo+' · '+modo+' · '+informe.tam+' · '+pasos.length+' capturas en '+carpeta+' · '+(informe.duracionMs/1000).toFixed(1)+' s · '+(llego?'llegó al mar':'NO LLEGÓ AL MAR: '+fallo));
    const tap=pasos.filter(p=>p.tapado);if(tap.length)decir('botones tapados al tocarlos: '+tap.map(p=>p.captura+' ('+p.encima+')').join(', '));
    listar(s.errores,s.avisos)}
  return s.errores.length||!llego?1:0}

async function cmdMedir(archivo,tam,carpeta){
  const s=await abrir(archivo,tam),res={archivo:path.relative(process.cwd(),path.resolve(archivo)).replace(/\\/g,'/'),tam:tam.w+'x'+tam.h,cpu:'4x',navegador:path.basename(s.navegador)};
  const GRABAR=`(()=>{const m=window.__m={t:[],pos:[],on:true};(function f(now){if(!m.on)return;m.t.push(now);const b=document.getElementById('barca'),q=b&&/translate\\(\\s*([-\\d.]+)[ ,]+([-\\d.]+)/.exec(b.getAttribute('transform')||'');m.pos.push(q?[+q[1],+q[2]]:null);requestAnimationFrame(f)})(performance.now());return true})()`;
  /* la distancia de un punto del SVG al curso del río (la polilínea de rioPor('nilo').curso proyectada con proj) y los píxeles por unidad */
  const CURSO=`const poly=rioPor('nilo').curso.map(p=>proj(p)),ctm=document.getElementById('svg').getScreenCTM(),esc=ctm?Math.hypot(ctm.a,ctm.b):1,
    dist=p=>{let best=1e9;for(let i=1;i<poly.length;i++){const a=poly[i-1],b=poly[i],dx=b[0]-a[0],dy=b[1]-a[1],L=dx*dx+dy*dy,u=L?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/L)):0;best=Math.min(best,Math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))}return best};`;
  const DESVIO=`(()=>{const b=document.getElementById('barca'),q=b&&/translate\\(\\s*([-\\d.]+)[ ,]+([-\\d.]+)/.exec(b.getAttribute('transform')||'');if(!q)return null;${CURSO}return Math.round(dist([+q[1],+q[2]])*esc*100)/100})()`;
  /* la ventana del viaje: del cuadro anterior al primer movimiento de la barca al último cuadro en que se movió (lo quieto de después no cuenta) */
  const LEER=`(()=>{const m=window.__m;m.on=false;${CURSO}
    const mov=[];for(let i=1;i<m.pos.length;i++){const p=m.pos[i],q=m.pos[i-1];if(p&&q&&(p[0]!==q[0]||p[1]!==q[1]))mov.push(i)}
    const a=mov.length?mov[0]-1:0,b=mov.length?mov[mov.length-1]:-1,ts=m.t.slice(a,b+1),d=[];for(let i=1;i<ts.length;i++)d.push(ts[i]-ts[i-1]);
    const ord=d.slice().sort((x,y)=>x-y),med=ord.length?ord[ord.length>>1]:null,ds=m.pos.slice(a,b+1).filter(p=>p).map(dist);
    return {cuadros:ts.length,duracionMs:ts.length?Math.round(ts[ts.length-1]-ts[0]):0,fpsMediana:med?Math.round(10000/med)/10:null,cuadroMasLargoMs:ord.length?Math.round(ord[ord.length-1]*10)/10:null,cuadrosDeMasDe50ms:d.filter(x=>x>50).length,
      desvioMaxSVG:ds.length?Math.round(Math.max(...ds)*1000)/1000:null,desvioMaxPx:ds.length?Math.round(Math.max(...ds)*esc*100)/100:null,pxPorUnidad:Math.round(esc*100)/100,muestras:ds.length}})()`;
  const AVANZAR=`(()=>{if(!S.zarpo)zarpar();if(typeof CAPA!=='undefined'&&CAPA.navegar&&CAPA.fase!=='navega')CAPA.navegar();const g=S.guias[S.paso];if(g&&g.resp==null)responderGuia(g.objetivo);return S.paso})()`;
  try{
    await s.cargar();await s.ev('localStorage.clear()');await s.recargar();await s.ev(`setModo('historia');abrirRio('nilo',1)`);await dormir(900);
    await s.cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
    /* un viaje entero sin evento, sin capturas en el medio, para los cuadros y la posición de la barca */
    const n=await s.ev(`rioPor('nilo').paradas.length`);let medido=null;
    for(let i=0;i<n&&!medido;i++){await s.ev(AVANZAR);await dormir(500);await s.ev(GRABAR);await dormir(120);await s.ev('paso(1)');
      const hayEvento=await s.ev('!!S.evento');await dormir(2400);const m=await s.ev(LEER);
      if(hayEvento){await s.ev('responderEvento(S.evento.q.correcta);continuarEvento()');await dormir(2400)}else if(m.cuadros>5)medido=Object.assign({tramo:'de '+i+' a '+(i+1)},m)}   /* la fuente y la primera parada pueden ser el mismo punto (Jinja): ese tramo no mueve la barca y no sirve para medir */
    res.viaje=medido;if(medido)res.barcaSobreElCurso=medido.desvioMaxPx!=null&&medido.desvioMaxPx<=3;
    /* otro viaje, con cinco capturas a lo largo */
    if(carpeta){fs.mkdirSync(carpeta,{recursive:true});res.capturas=[];
      await s.ev(`(()=>{window.__k=null;if(typeof CAPA!=='undefined'&&CAPA.oir)CAPA.oir('avanza',d=>{window.__k=d&&d.k});return true})()`);   /* el avance del viaje (0 a 1), si la capa lo emite */
      for(let i=0;i<4;i++){const p=await s.ev(AVANZAR);await dormir(500);await s.ev(`window.__t0=performance.now();paso(1)`);
        if(await s.ev('!!S.evento')){await dormir(2400);await s.ev('responderEvento(S.evento.q.correcta);continuarEvento()');await dormir(2400);continue}
        for(let j=0;j<5;j++){const meta=120+j*300;while(await s.ev('performance.now()-window.__t0')<meta)await dormir(15);
          const f='viaje-'+(j+1)+'.png';await s.foto(path.join(carpeta,f));res.capturas.push({captura:f,ms:Math.round(await s.ev('performance.now()-window.__t0')),desde:p,desvioPx:await s.ev(DESVIO),avance:await s.ev('window.__k==null?null:Math.round(window.__k*100)/100')})}
        break}
      res.barcaSobreElCursoEnLasCinco=res.capturas.length===5&&res.capturas.every(c=>c.desvioPx!=null&&c.desvioPx<=3)}
    await s.cdp.send('Emulation.setCPUThrottlingRate',{rate:1});
    res.sonido=await s.ev(`(async()=>{if(typeof CAPA==='undefined'||!CAPA.sonido||!CAPA.sonido.probar)return 'no hay CAPA.sonido.probar';try{return await CAPA.sonido.probar()}catch(e){return 'falló: '+e}})()`,true);
  }catch(err){res.fallo=String(err&&err.message||err)}
  finally{res.errores=s.errores;res.avisos=s.avisos;await s.cerrar()}
  decir(JSON.stringify(res,null,1));return res.errores.length||res.fallo?1:0}

/* ---------- el catálogo de estados (auditar y estados) ---------- */
/* Lo que se instala en la página para armar cada estado con funciones del motor. Corre en el navegador, no en Node: se manda
   con toString(). En Cauces la portada es otra pantalla, así que primero se abre el Nilo desde la fuente. */
function ayudaEnPagina(){
  const espera=ms=>new Promise(r=>setTimeout(r,ms)),hayCapa=typeof CAPA!=='undefined'&&!!CAPA;
  if(S.pantalla!=='rio')abrirRio('nilo',1);
  const navegar=()=>{if(hayCapa&&CAPA.navegar&&CAPA.fase!=='navega'&&S.paso<rioPor(S.rio).paradas.length)CAPA.navegar()};
  const guia=mal=>{if(!S.zarpo)zarpar();const g=S.guias[S.paso];if(g&&g.resp==null)responderGuia(mal?g.opciones.find(i=>i!==g.objetivo):g.objetivo)};
  /* hasta la parada k (n+1 es el mar), acertando la guía y los eventos; con {fallar:p}, la guía del paso p se responde mal */
  const ir=async(k,o)=>{o=o||{};for(let v=0;S.paso<k&&v<90;v++){if(S.evento){if(S.evento.resp==null)responderEvento(S.evento.q.correcta);continuarEvento();continue}guia(o.fallar===S.paso);paso(1)}await espera(1800);return S.paso};
  const alEvento=async()=>{const n=rioPor(S.rio).paradas.length;for(let v=0;!S.evento&&S.paso<=n&&v<90;v++){guia(false);paso(1)}await espera(1800);return !!S.evento};
  /* baja comprando lo que se ofrece en cada puerto hasta llenar la bodega */
  const llenar=async()=>{const r=rioPor(S.rio),n=r.paradas.length;for(let v=0;v<n&&S.eco&&S.eco.bodega.length<3&&S.paso<n;v++){await ir(S.paso+1);const j=S.paso-1;for(let t=0;t<3;t++)r.carga.forEach((g,gi)=>{if(g.o===j&&S.eco.bodega.length<3&&S.eco.monedas>=g.b)comprar(gi)})}await espera(300);return S.eco?S.eco.bodega.length:null};
  return {espera,navegar,guia,ir,alEvento,llenar}}
/* cada estado: un nombre, el modo (Niño si no se dice) y el JS que lo arma; `c` es la ayuda de arriba y `n`, el número de paradas */
const CATALOGO=[
  {id:'portada',nota:'la portada del río, con el perfil limpio'},
  {id:'navegar-primera',nota:'navegar en la primera bajada: la frase con la lista, antes de zarpar',js:`c.navegar()`},
  {id:'guia-sin-responder',nota:'navegar en Juba, con la guía sin responder',js:`await c.ir(2);c.navegar()`},
  {id:'guia-bien',nota:'la guía respondida bien',js:`await c.ir(2);c.navegar();c.guia(false);await c.espera(500)`},
  {id:'guia-mal',nota:'la guía respondida mal',js:`await c.ir(2);c.navegar();c.guia(true);await c.espera(500)`},
  {id:'parada-sello-nuevo',nota:'Juba recién llegada, con el sello nuevo',js:`await c.ir(2)`},
  {id:'parada-sello-pendiente',nota:'Juba tras fallar la guía: el sello queda pendiente',js:`await c.ir(2,{fallar:1})`},
  {id:'mercado-lleno',nota:'el mercado con la bodega llena (la página baja hasta el mercado)',js:`await c.llenar();const m=document.querySelector('#panel .mercado');if(m)m.scrollIntoView({block:'center',behavior:'instant'});await c.espera(300)`},
  {id:'evento',nota:'una prueba entre puertos, sin responder',js:`await c.alEvento()`},
  {id:'evento-bien',nota:'la prueba respondida bien',js:`await c.alEvento();responderEvento(S.evento.q.correcta);await c.espera(700)`},
  {id:'evento-mal',nota:'la prueba respondida mal',js:`await c.alEvento();responderEvento((S.evento.q.correcta+1)%S.evento.q.opciones.length);await c.espera(700)`},
  {id:'parada-adulto',modo:'historia',nota:'Juba en Adulto',js:`await c.ir(2)`},
  {id:'anclada',nota:'la barca anclada: el río se reabre en Juba',js:`await c.ir(2);abrirRio('nilo');await c.espera(500)`},
  {id:'parada-ultima',nota:'El Cairo, la última parada',js:`await c.ir(n)`},
  {id:'mar-nino',nota:'la llegada al mar en Niño',js:`await c.ir(n+1);await c.espera(3000)`},
  {id:'mar-adulto',modo:'historia',nota:'la llegada al mar en Adulto',js:`await c.ir(n+1);await c.espera(3000)`}];

/* La auditoría de una pantalla. Corre en el navegador (se manda con toString()) y devuelve lo medido:
   (a) los textos pintados y su tamaño en píxeles de pantalla; (b) lo tocable de menos de 44 px; (c) el contraste de cada texto
   HTML contra su fondo; (d) si la página es más ancha que la ventana; (e) nombres de paradas futuras en la carta; (f) emojis;
   (g) textos cortados por el borde o por el pie, cajas que recortan su texto, rótulos de la carta tapados o encimados. */
function auditarEnPagina(){
  const W=innerWidth,H=innerHeight,SVGNS='http://www.w3.org/2000/svg',de=document.documentElement,r1=v=>Math.round(v*10)/10;
  const limpio=t=>String(t||'').replace(/\s+/g,' ').trim();
  const zonaDe=el=>{for(let a=el;a&&a.nodeType===1;a=a.parentElement){const i=a.id;if(i==='panel'||i==='pie'||i==='cab'||i==='perfil')return i;if(i==='mapa'||i==='svg')return 'mapa';if(i==='rielArriba')return 'riel'}return 'otro'};
  const sel=el=>{const c=typeof el.className==='string'?el.className:(el.className&&el.className.baseVal)||'';return el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(c.trim()?'.'+c.trim().split(/\s+/).slice(0,3).join('.'):'')};
  const rotulo=el=>(limpio(el.textContent)||limpio(el.getAttribute&&el.getAttribute('aria-label'))||limpio(el.getAttribute&&el.getAttribute('title'))).slice(0,60);
  const opacidad=el=>{let o=1;for(let a=el;a&&a.nodeType===1;a=a.parentElement){o*=parseFloat(getComputedStyle(a).opacity);if(!(o>0.01))return 0}return o};
  const escalaCSS=el=>{let k=1;for(let a=el;a&&a.nodeType===1;a=a.parentElement){const t=getComputedStyle(a).transform;if(t&&t!=='none'){try{const m=new DOMMatrix(t);k*=Math.hypot(m.a,m.b)}catch(e){}}}return k};
  /* la caja que deja ver a un elemento: el cruce de sus ancestros con overflow (c.l…c.b, cualquiera que no sea visible) y, aparte,
     el de los que recortan sin dejar desplazar (hidden o clip: c.dl…c.db, con quién recorta cada lado) */
  const clips=new Map(),clipDe=el=>{if(clips.has(el))return clips.get(el);const c={l:-1e9,t:-1e9,r:1e9,b:1e9,dl:-1e9,dt:-1e9,dr:1e9,db:1e9,ql:null,qt:null,qr:null,qb:null};
    for(let a=el;a&&a.nodeType===1&&a!==document.body&&a!==de;a=a.parentElement){const cs=getComputedStyle(a),ox=cs.overflowX,oy=cs.overflowY;if(ox==='visible'&&oy==='visible')continue;const q=a.getBoundingClientRect();
      if(ox!=='visible'){c.l=Math.max(c.l,q.left);c.r=Math.min(c.r,q.right);if(/hidden|clip/.test(ox)){if(q.left>c.dl){c.dl=q.left;c.ql=a}if(q.right<c.dr){c.dr=q.right;c.qr=a}}}
      if(oy!=='visible'){c.t=Math.max(c.t,q.top);c.b=Math.min(c.b,q.bottom);if(/hidden|clip/.test(oy)){if(q.top>c.dt){c.dt=q.top;c.qt=a}if(q.bottom<c.db){c.db=q.bottom;c.qb=a}}}}
    clips.set(el,c);return c};
  /* (a) los textos pintados, agrupados por su elemento */
  const grupos=new Map(),rango=document.createRange(),tw=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  for(let nd=tw.nextNode();nd;nd=tw.nextNode()){
    const t=limpio(nd.nodeValue);if(!t)continue;const p=nd.parentElement;if(!p||p.closest('script,style,noscript,template,defs,title,desc,symbol'))continue;
    const svg=p.namespaceURI===SVGNS;rango.selectNodeContents(nd);let rs=[...rango.getClientRects()].filter(q=>q.width>0.5&&q.height>0.5);
    if(!rs.length&&svg){const q=(p.closest('text')||p).getBoundingClientRect();if(q.width>0.5&&q.height>0.5)rs=[q]}
    if(!rs.length||getComputedStyle(p).visibility!=='visible')continue;const op=opacidad(p);if(op<=0.01)continue;
    /* lo que deja ver cada caja con overflow: un texto recortado del todo no se pinta (un rótulo solo para lectores de pantalla);
       recortado en parte por un overflow hidden o clip, queda anotado con lo que le falta */
    let px;if(svg){const te=p.closest('text')||p,m=te.getScreenCTM?te.getScreenCTM():null;px=parseFloat(getComputedStyle(p).fontSize)*(m?Math.hypot(m.a,m.b):1)}else px=parseFloat(getComputedStyle(p).fontSize)*escalaCSS(p);
    /* a lo alto, la caja de un renglón es más alta que sus letras: un corte de menos de 0,3 del cuerpo no toca la letra y no cuenta */
    const cl=clipDe(p),partes=[],holgura=0.3*(px||0);let corte=0,quien=null;
    for(const q of rs){const l=Math.max(q.left,cl.l),t2=Math.max(q.top,cl.t),r2=Math.min(q.right,cl.r),b2=Math.min(q.bottom,cl.b);if(r2-l>=3&&b2-t2>=3)partes.push({l,t:t2,r:r2,b:b2});
      for(const [d,a] of [[Math.min(q.width,cl.dl-q.left),cl.ql],[Math.min(q.width,q.right-cl.dr),cl.qr],[Math.min(q.height,cl.dt-q.top)-holgura,cl.qt],[Math.min(q.height,q.bottom-cl.db)-holgura,cl.qb]])if(d>corte){corte=d;quien=a}}
    if(!partes.length)continue;
    let g=grupos.get(p);
    if(!g){g={el:p,svg,px,op,texto:'',l:1e9,t:1e9,r:-1e9,b:-1e9,corte:0,quien:null};grupos.set(p,g)}
    g.texto=limpio(g.texto+' '+t);if(corte>g.corte){g.corte=corte;g.quien=quien}
    for(const q of partes){g.l=Math.min(g.l,q.l);g.t=Math.min(g.t,q.t);g.r=Math.max(g.r,q.r);g.b=Math.max(g.b,q.b)}}
  const T=[...grupos.values()].filter(g=>g.px>0).map(g=>Object.assign(g,{zona:zonaDe(g.el),sel:sel(g.el),enPantalla:g.r>0&&g.l<W&&g.b>0&&g.t<H,decorativo:!!g.el.closest('[aria-hidden="true"]')}));
  const item=g=>({texto:g.texto.slice(0,60),px:r1(g.px),zona:g.zona,sel:g.sel,svg:g.svg,enPantalla:g.enPantalla,decorativo:g.decorativo});
  const orden=T.slice().sort((a,b)=>a.px-b.px),html=orden.filter(g=>!g.svg);
  /* (b) lo tocable */
  const toques=[...document.querySelectorAll('button,a[href],[onclick],summary,[role="button"],input,select,textarea')].filter(el=>{if(el.disabled)return false;const q=el.getBoundingClientRect(),cs=getComputedStyle(el);return q.width>0&&q.height>0&&cs.visibility==='visible'&&cs.pointerEvents!=='none'&&opacidad(el)>0.01});
  const toquesChicos=toques.map(el=>({el,q:el.getBoundingClientRect()})).filter(o=>o.q.width<43.5||o.q.height<43.5).map(o=>({texto:rotulo(o.el),ancho:r1(o.q.width),alto:r1(o.q.height),zona:zonaDe(o.el),sel:sel(o.el),enPantalla:o.q.right>0&&o.q.left<W&&o.q.bottom>0&&o.q.top<H}));
  /* (c) el contraste de cada texto HTML contra su fondo: se baja por lo que hay debajo del texto hasta un color opaco; lo que
     queda sobre el mapa, una imagen o un degradado se cuenta aparte */
  const color=s=>{const m=/rgba?\(([^)]+)\)/.exec(s||'');if(!m)return null;const v=m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat);return v.length<3||v.some(isNaN)?null:{r:v[0],g:v[1],b:v[2],a:v.length>3?v[3]:1}};
  const hex=c=>'#'+[c.r,c.g,c.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join('');
  const sobre=(f,b)=>({r:f.r*f.a+b.r*(1-f.a),g:f.g*f.a+b.g*(1-f.a),b:f.b*f.a+b.b*(1-f.a),a:1});
  const lum=c=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b)};
  const razon=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
  const esFoto=x=>/^(img|canvas|video|picture)$/i.test(x.tagName)||(x.namespaceURI===SVGNS);
  const fondoDe=g=>{const el=g.el,capas=[];let aparte=null;
    const mirar=x=>{if(/^(img|canvas|video|picture)$/i.test(x.tagName)){aparte='imagen';return true}
      if(x.namespaceURI===SVGNS){aparte=x.closest('#mapa')?'mapa':'dibujo';return true}
      const cs=getComputedStyle(x),o=parseFloat(cs.opacity);if(!(o>0.01))return false;
      if(cs.backgroundImage&&cs.backgroundImage!=='none'){aparte=(x.id==='mapa'||x.closest('#mapa'))?'mapa':'imagen o degradado';return true}
      const c=color(cs.backgroundColor);if(c&&c.a>0){c.a*=o;capas.push(c);if(c.a>=0.99)return true}return false};
    const cx=(g.l+g.r)/2,cy=(g.t+g.b)/2;let listo=false;
    if(cx>=0&&cx<W&&cy>=0&&cy<H){const pila=document.elementsFromPoint(cx,cy);let a=el,propio=pila.indexOf(el)>=0;
      while(a&&pila.indexOf(a)<0){if(mirar(a)){listo=true;break}a=a.parentElement}
      if(!listo){const i=a?pila.indexOf(a):0,k0=propio||!pila.slice(0,i).some(esFoto)?i:0;   /* un texto que no recibe toques y tiene el mapa o una imagen en la pila: están debajo */
        for(let k=k0;k<pila.length;k++){const x=pila[k];if(x!==el&&el.contains(x))continue;if(mirar(x))break}}}
    else for(let a=el;a&&a.nodeType===1;a=a.parentElement)if(mirar(a))break;
    if(aparte)return {aparte};
    let base={r:255,g:255,b:255,a:1};for(let k=capas.length-1;k>=0;k--)base=sobre(capas[k],base);return {color:base}};
  const opTexto=el=>{let o=1;for(let a=el;a&&a.nodeType===1;a=a.parentElement){const cs=getComputedStyle(a);o*=parseFloat(cs.opacity);const c=color(cs.backgroundColor);if((c&&c.a>0)||(cs.backgroundImage&&cs.backgroundImage!=='none'))break}return o};
  const contrastesBajos=[],aparte={mapa:0,imagen:0,dibujo:0,ejemplos:[]},enCaptura=[];let sinMedir=0,medidos=0;
  /* lo que va sobre el mapa o una imagen se mide después, en la captura: aquí se anota su caja y su color */
  const tapadoEn=(g,x,y)=>{if(x<0||y<0||x>=W||y>=H)return true;const e=document.elementFromPoint(x,y);if(!e||e===g.el||g.el.contains(e)||e.contains(g.el))return false;return !(g.zona==='mapa'&&e.closest('#mapa'))};
  const paraCaptura=(g,c,sobreQue,grande)=>{if(!g.enPantalla||!c||c.a<=0.05||enCaptura.length>=80)return;
    for(const x of [g.l+1.5,(g.l+g.r)/2,g.r-1.5])for(const y of [g.t+1.5,(g.t+g.b)/2,g.b-1.5])if(tapadoEn(g,x,y))return;   /* tapado en todo o en parte por otra cosa (la hoja, la píldora): no se mide */
    enCaptura.push({texto:g.texto.slice(0,40),sel:g.sel,zona:g.zona,px:r1(g.px),sobre:sobreQue,grande,color:{r:c.r,g:c.g,b:c.b,a:Math.min(1,c.a*g.op)},l:g.l,t:g.t,r:g.r,b:g.b})};
  /* mientras se mira qué hay debajo de cada texto, todo recibe toques: así elementsFromPoint da la pila entera, en el orden en que se
     pinta (el mapa de la vitrina y los rótulos de adorno llevan pointer-events:none y, si no, no saldrían) */
  const forzar=document.createElement('style');forzar.textContent='*{pointer-events:auto!important}';document.head.appendChild(forzar);
  for(const g of T){const cs=getComputedStyle(g.el),esGrande=g.px>=24||(g.px>=18.66&&parseInt(cs.fontWeight,10)>=700);
    if(g.svg){aparte[g.zona==='mapa'?'mapa':'dibujo']++;if(g.zona==='mapa'){const cf=color(cs.fill);if(cf){cf.a*=parseFloat(cs.fillOpacity||1);paraCaptura(g,cf,'mapa',esGrande)}}continue}
    const c=color(cs.color);if(!c){sinMedir++;continue}
    const f=fondoDe(g);if(f.aparte){aparte[f.aparte==='mapa'?'mapa':f.aparte==='dibujo'?'dibujo':'imagen']++;if(aparte.ejemplos.length<10)aparte.ejemplos.push({texto:g.texto.slice(0,40),sobre:f.aparte,zona:g.zona,sel:g.sel,color:hex(c),px:r1(g.px)});paraCaptura(g,c,f.aparte,esGrande);continue}
    medidos++;const tinta=sobre({r:c.r,g:c.g,b:c.b,a:c.a*opTexto(g.el)},f.color),rz=razon(tinta,f.color),grande=g.px>=24||(g.px>=18.66&&parseInt(cs.fontWeight,10)>=700);
    if(rz<4.5)contrastesBajos.push(Object.assign(item(g),{color:hex(tinta),fondo:hex(f.color),razon:Math.round(rz*100)/100,grande,pasaComoGrande:grande&&rz>=3}))}
  forzar.remove();
  /* (d) el ancho de la página */
  const pagina={ventana:W,ancho:Math.max(de.scrollWidth,document.body?document.body.scrollWidth:0),alto:de.scrollHeight,scrollY:Math.round(window.scrollY)};pagina.desborda=pagina.ancho>W+1;
  if(pagina.desborda)pagina.culpables=[...document.querySelectorAll('body *')].filter(x=>x.namespaceURI!==SVGNS).map(x=>({x,q:x.getBoundingClientRect()})).filter(o=>o.q.width>0&&o.q.right>W+1).sort((a,b)=>b.q.right-a.q.right).slice(0,6).map(o=>({sel:sel(o.x),derecha:r1(o.q.right),ancho:r1(o.q.width)}));
  /* (e) nombres de paradas futuras en la carta (con la guía ya respondida, la que sigue ya se dijo) */
  const r=typeof S!=='undefined'&&S.pantalla==='rio'&&S.rio?rioPor(S.rio):null,p=r?S.paso:0,gq=r&&S.guias?S.guias[p]:null,resp=!!gq&&gq.resp!=null;
  const futuras=r?r.paradas.map(c=>c.nombre).slice(p+(resp?1:0)):[],mapa=document.getElementById('mapa');
  const tm=mapa?(limpio(mapa.textContent)+' | '+[...mapa.querySelectorAll('[aria-label],[title]')].map(x=>(x.getAttribute('aria-label')||'')+' '+(x.getAttribute('title')||'')).join(' ')).toLowerCase():'';
  const nombresFuturos=futuras.filter(nm=>tm.indexOf(nm.toLowerCase())>=0);
  /* (f) emojis: en los textos pintados, en aria-label, title y alt, y en lo que el CSS agrega con ::before y ::after */
  const EMOJI=/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|️|⃣/gu,esEmoji=ch=>!/[©®™]/.test(ch);
  const fuentes=T.map(g=>({t:g.texto,d:g.sel})).concat([...document.querySelectorAll('[aria-label],[title],[alt]')].filter(x=>x.getClientRects().length).map(x=>({t:(x.getAttribute('aria-label')||'')+' '+(x.getAttribute('title')||'')+' '+(x.getAttribute('alt')||''),d:sel(x)+' (atributo)'})));
  for(const x of document.querySelectorAll('#panel *,#pie *,#cab *'))for(const ps of ['::before','::after']){const ct=getComputedStyle(x,ps).content;if(ct&&ct!=='none'&&ct!=='normal')fuentes.push({t:ct,d:sel(x)+ps})}
  const emojis=[];for(const f of fuentes)for(const ch of (f.t.match(EMOJI)||[]).filter(esEmoji))if(!emojis.some(e=>e.car===ch&&e.donde===f.d))emojis.push({car:ch,codigo:'U+'+ch.codePointAt(0).toString(16).toUpperCase(),donde:f.d});
  /* (g) cortes: por el borde de la ventana, por el pie fijo, por la propia caja; rótulos de la carta tapados, bajo la barca o encimados */
  const pie=document.getElementById('pie'),qp=pie&&!pie.hidden?pie.getBoundingClientRect():null,pieFijo=!!qp&&qp.height>0&&/fixed|sticky/.test(getComputedStyle(pie).position),tope=pieFijo?qp.top:H,maxS=Math.max(0,de.scrollHeight-H),sy=window.scrollY;
  const cortados=[];
  for(const g of T){if(!g.enPantalla)continue;
    if(g.l<-1||g.r>W+1)cortados.push(Object.assign(item(g),{por:'el borde de la ventana',firme:true,fuera:r1(Math.max(-g.l,g.r-W))}));
    else if(pieFijo&&g.zona!=='pie'&&g.t<tope-1&&g.b>tope+2&&g.r>qp.left+1&&g.l<qp.right-1){   /* cruza el borde de arriba del pie, y en su misma columna */const firme=(g.b+sy)-maxS>tope+2;   /* ¿sigue tapado con la página bajada del todo? */
      cortados.push(Object.assign(item(g),{por:firme?'el pie, también con la página bajada del todo':'el pie (asoma a medias; se destapa al bajar)',firme}))}}
  /* textos a los que su propia caja (o la de un ancestro con overflow hidden) les corta 2 px o más; en la carta, el borde del mapa */
  const recortados=T.filter(g=>g.enPantalla&&g.corte>=2).map(g=>({texto:g.texto.slice(0,60),sel:g.sel,zona:g.zona,falta:r1(g.corte),por:g.quien?sel(g.quien):'',px:r1(g.px)}));
  /* rótulos de la carta con algo de fuera del mapa encima (la píldora, un botón, la hoja): nueve puntos por rótulo; tapado entero no
     se ve y no estorba (se cuenta aparte), tapado a medias sí */
  const etqs=T.filter(g=>g.svg&&g.zona==='mapa'&&g.enPantalla),rotulosTapados=[],barcaSobreRotulos=[],rotulosEncimados=[];let rotulosOcultos=0;
  const encima=(x,y)=>{if(x<0||y<0||x>=W||y>=H)return null;const e=document.elementFromPoint(x,y);return !e||e===document.body||e===de||e.closest('#mapa')||(mapa&&e.contains(mapa))?null:e};
  for(const g of etqs){const xs=[g.l+1.5,(g.l+g.r)/2,g.r-1.5],ys=[g.t+1.5,(g.t+g.b)/2,g.b-1.5],enc=[];for(const x of xs)for(const y of ys){const e=encima(x,y);if(e)enc.push(e)}
    if(enc.length>=9)rotulosOcultos++;else if(enc.length)rotulosTapados.push({texto:g.texto.slice(0,40),por:sel(enc[0]),puntos:enc.length+' de 9',px:r1(g.px)})}
  /* la barca que se ve: el casco, la vela y el animal (la caja del grupo entero incluye el halo, que no tapa nada) */
  const eb=document.getElementById('barca'),pb=[...document.querySelectorAll('#barca .casco,#barca .vela,#barca .fig,#masc *')].map(x=>x.getBoundingClientRect()).filter(q=>q.width>0&&q.height>0);
  const qb=pb.length?{left:Math.min(...pb.map(q=>q.left)),right:Math.max(...pb.map(q=>q.right)),top:Math.min(...pb.map(q=>q.top)),bottom:Math.max(...pb.map(q=>q.bottom)),width:1}:eb?eb.getBoundingClientRect():null;
  if(qb&&qb.width>0)for(const g of etqs){const w=Math.min(g.r,qb.right)-Math.max(g.l,qb.left),h=Math.min(g.b,qb.bottom)-Math.max(g.t,qb.top);if(w>4&&h>4)barcaSobreRotulos.push({texto:g.texto.slice(0,40),solape:r1(w)+' × '+r1(h)+' px'})}
  for(let i=0;i<etqs.length;i++)for(let j=i+1;j<etqs.length;j++){const a=etqs[i],b=etqs[j];if((a.el.closest('text')||a.el)===(b.el.closest('text')||b.el)||a.texto===b.texto)continue;const w=Math.min(a.r,b.r)-Math.max(a.l,b.l),h=Math.min(a.b,b.b)-Math.max(a.t,b.t);if(w>3&&h>3)rotulosEncimados.push({a:a.texto.slice(0,30),b:b.texto.slice(0,30),solape:r1(w)+' × '+r1(h)+' px'})}
  return {ventana:W+'x'+H,momento:typeof CAPA!=='undefined'&&CAPA.momento?CAPA.momento():null,paso:p,
    cuenta:{textos:T.length,enPantalla:T.filter(g=>g.enPantalla).length,toques:toques.length,contrastesMedidos:medidos,sinMedir},
    textoMinimo:orden.length?item(orden[0]):null,textoMinimoHTML:html.length?item(html[0]):null,textosChicos:orden.filter(g=>g.px<10.95).map(item),
    toquesChicos,contrastesBajos,aparte,enCaptura,pagina,nombresFuturos,emojis,cortados,recortados,rotulosTapados,rotulosOcultos,barcaSobreRotulos,rotulosEncimados}}

/* Un PNG de 8 bits (RGB o RGBA, sin entrelazar: lo que da Page.captureScreenshot) a píxeles, sin dependencias. */
function leerPNG(buf){let p=8,w=0,h=0,tipo=0,bits=0;const idat=[];
  while(p<buf.length){const n=buf.readUInt32BE(p),t=buf.toString('latin1',p+4,p+8),d=buf.subarray(p+8,p+8+n);
    if(t==='IHDR'){w=d.readUInt32BE(0);h=d.readUInt32BE(4);bits=d[8];tipo=d[9]}else if(t==='IDAT')idat.push(d);else if(t==='IEND')break;p+=12+n}
  if(bits!==8||(tipo!==6&&tipo!==2))throw new Error('PNG de un tipo que no leo: color '+tipo+', '+bits+' bits');
  const c=tipo===6?4:3,raw=require('zlib').inflateSync(Buffer.concat(idat)),fila=w*c,px=Buffer.alloc(h*fila);
  for(let y=0;y<h;y++){const f=raw[y*(fila+1)],o=y*(fila+1)+1,q=y*fila;
    for(let x=0;x<fila;x++){const a=x>=c?px[q+x-c]:0,b=y?px[q-fila+x]:0,d=x>=c&&y?px[q-fila+x-c]:0;let v=raw[o+x];
      if(f===1)v+=a;else if(f===2)v+=b;else if(f===3)v+=(a+b)>>1;else if(f===4){const e=a+b-d,pa=Math.abs(e-a),pb=Math.abs(e-b),pc=Math.abs(e-d);v+=pa<=pb&&pa<=pc?a:pb<=pc?b:d}
      px[q+x]=v&255}}
  return {w,h,c,px}}
/* El contraste de un texto contra lo que de verdad tiene alrededor en la captura: los píxeles de un anillo pegado a su caja (por
   fuera, a 2 px). Devuelve la mediana y el más bajo de cada veinte (percentil 5). Sirve para lo que va sobre el mapa o una imagen. */
function contrasteEnCaptura(img,k,t){
  const lum=(r,g,b)=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)};
  const l=Math.max(0,Math.round(t.l*k)-2),r=Math.min(img.w-1,Math.round(t.r*k)+2),a=Math.max(0,Math.round(t.t*k)-2),b=Math.min(img.h-1,Math.round(t.b*k)+2),rz=[];
  const uno=(x,y)=>{const i=(y*img.w+x)*img.c,R=img.px[i],G=img.px[i+1],B=img.px[i+2],al=t.color.a,lt=lum(t.color.r*al+R*(1-al),t.color.g*al+G*(1-al),t.color.b*al+B*(1-al)),lf=lum(R,G,B);rz.push((Math.max(lt,lf)+0.05)/(Math.min(lt,lf)+0.05))};
  for(let x=l;x<=r;x++){uno(x,a);uno(x,b)}for(let y=a+1;y<b;y++){uno(l,y);uno(r,y)}
  if(!rz.length)return null;rz.sort((x,y)=>x-y);return {mediana:Math.round(rz[rz.length>>1]*100)/100,bajo:Math.round(rz[Math.floor(rz.length*0.05)]*100)/100}}

/* arma cada estado del catálogo en una misma sesión (perfil limpio, el modo, recarga, la ayuda y el JS del estado) y le pasa la
   página a `cadaUno` */
async function porEstado(archivo,tam,cadaUno,solo){
  const s=await abrir(archivo,tam),hechos=[];
  try{await s.cargar();
    for(const e of CATALOGO){if(solo&&solo.indexOf(e.id)<0)continue;const t0=Date.now(),e0=s.errores.length;let fallo=null,dato=null;
      try{await s.ev('localStorage.clear()');await s.recargar();await s.ev(`setModo(${JSON.stringify(e.modo||'mercader')})`);await s.recargar();
        await s.ev(`window.__c=(${ayudaEnPagina.toString()})();true`);
        if(e.js)await s.ev(`(async()=>{const c=window.__c,n=rioPor('nilo').paradas.length;${e.js};return true})()`,true);
        await dormir(900);dato=await cadaUno(s,e,CATALOGO.indexOf(e)+1)}   /* el número es el del catálogo, también con solo= */
      catch(err){fallo=String(err&&err.message||err)}
      hechos.push({id:e.id,modo:e.modo||'mercader',nota:e.nota,ms:Date.now()-t0,fallo,erroresDeConsola:s.errores.slice(e0),estado:await s.ev(ESTADO).catch(()=>null),dato})}
    return {archivo:path.relative(process.cwd(),path.resolve(archivo)).replace(/\\/g,'/'),tam:tam.w+'x'+tam.h+(tam.k&&tam.k!==2?'@'+tam.k:''),navegador:path.basename(s.navegador),fecha:new Date().toISOString(),estados:hechos,errores:s.errores,avisos:s.avisos}}
  finally{await s.cerrar()}}

async function cmdEstados(archivo,carpeta,tam,solo){
  fs.mkdirSync(carpeta,{recursive:true});
  const R=await porEstado(archivo,tam,async(s,e,k)=>{const captura=String(k).padStart(2,'0')+'-'+e.id+'.png';await s.foto(path.join(carpeta,captura));return {captura}},solo);
  /* con solo=, lo que ya había de los otros estados se conserva */
  const fj=path.join(carpeta,'estados.json');let guardar=R;
  if(solo&&fs.existsSync(fj))try{const antes=JSON.parse(fs.readFileSync(fj,'utf8'));if(antes&&Array.isArray(antes.estados)&&antes.tam===R.tam){const m=new Map(R.estados.map(h=>[h.id,h]));guardar=Object.assign({},R,{estados:CATALOGO.map(e=>m.get(e.id)||antes.estados.find(h=>h.id===e.id)).filter(Boolean)})}}catch(e){}
  fs.writeFileSync(fj,JSON.stringify(guardar,null,1));
  decir('estados: '+R.archivo+' · '+R.tam+' · '+R.estados.length+' capturas en '+carpeta);
  for(const h of R.estados)decir('  '+(h.dato?h.dato.captura:'(sin captura) '+h.id).padEnd(34)+' '+h.nota+(h.estado?' · paso '+h.estado.paso+(h.estado.momento?' · '+h.estado.momento:'')+(h.estado.anchoPagina>+R.tam.split('x')[0]?' · PÁGINA DE '+h.estado.anchoPagina+' px':''):'')+(h.fallo?' · FALLÓ: '+h.fallo:''));
  listar(R.errores,R.avisos);return R.errores.length||R.estados.some(h=>h.fallo)?1:0}

async function cmdAuditar(archivo,tam,salida,solo){
  const R=await porEstado(archivo,tam,async s=>{const d=await s.ev(`(${auditarEnPagina.toString()})()`);
    /* lo que va sobre el mapa o una imagen: su contraste contra los píxeles de la captura (aparte: no hace fallar) */
    d.sobreElMapa=[];try{if(d.enCaptura.length){const img=leerPNG(await s.captura());for(const t of d.enCaptura){const m=contrasteEnCaptura(img,s.escala,t);if(m)d.sobreElMapa.push({texto:t.texto,sel:t.sel,zona:t.zona,px:t.px,sobre:t.sobre,grande:t.grande,mediana:m.mediana,bajo:m.bajo})}}}catch(e){d.sobreElMapaFallo=String(e&&e.message||e)}
    delete d.enCaptura;return d},solo),n=v=>String(v).replace('.',',');
  const destino=salida||path.join(__dirname,'..','docs','vitrina','capturas',tam.w===390&&tam.h===844?'auditoria.json':'auditoria-'+tam.w+'x'+tam.h+'.json');
  /* el resumen: una línea por estado y, debajo, cada cosa una sola vez con los estados donde aparece */
  const junta=(campo,clave,filtro)=>{const m=new Map();for(const h of R.estados)for(const x of (h.dato&&h.dato[campo])||[]){if(filtro&&!filtro(x))continue;const k=clave(x);if(!m.has(k))m.set(k,{x,en:[]});m.get(k).en.push(h.id)}return [...m.values()]};
  const todos=R.estados.length,donde=en=>en.length===todos?'todos':en.length>4?en.length+' estados':en.join(', ');
  decir('auditoría: '+R.archivo+' · '+R.tam+' · '+todos+' estados · '+R.navegador);
  decir('  '+'estado'.padEnd(24)+'texto mín.  <11 px  toques<44  contraste<4,5  ancho     futuros emojis cortados  rótulos tapados');
  let graves=0;
  for(const h of R.estados){const d=h.dato;if(!d){decir('  '+h.id.padEnd(24)+'FALLÓ: '+h.fallo);graves++;continue}
    const firmes=d.cortados.filter(c=>c.firme).length+d.recortados.length;if(d.pagina.desborda||d.nombresFuturos.length||d.emojis.length)graves++;
    decir('  '+h.id.padEnd(24)+(n(d.textoMinimo?d.textoMinimo.px:'-')+' px').padEnd(12)+String(d.textosChicos.length).padEnd(8)+String(d.toquesChicos.length).padEnd(11)+(d.contrastesBajos.filter(c=>!c.pasaComoGrande).length+(d.contrastesBajos.some(c=>c.pasaComoGrande)?' (+'+d.contrastesBajos.filter(c=>c.pasaComoGrande).length+' grandes)':'')).padEnd(15)+(d.pagina.ancho+'/'+d.pagina.ventana+(d.pagina.desborda?' !':'')).padEnd(10)+String(d.nombresFuturos.length?d.nombresFuturos.join('+'):0).padEnd(8)+String(d.emojis.length).padEnd(7)+(firmes+' (+'+(d.cortados.length-d.cortados.filter(c=>c.firme).length)+' a medias)').padEnd(10)+' '+d.rotulosTapados.length)}
  const bloque=(titulo,filas)=>{if(filas.length){decir('\n'+titulo+' ('+filas.length+'):');for(const f of filas)decir('  · '+f)}};
  bloque('Textos de menos de 11 px',junta('textosChicos',x=>x.sel+'|'+x.texto).sort((a,b)=>a.x.px-b.x.px).map(o=>n(o.x.px)+' px · «'+o.x.texto+'» · '+o.x.zona+(o.x.svg?' (SVG)':'')+(o.x.decorativo?' (aria-hidden)':'')+' · '+o.x.sel+' · '+donde(o.en)));
  bloque('Tocables de menos de 44 px',junta('toquesChicos',x=>x.sel+'|'+x.texto+'|'+Math.round(x.ancho)+'x'+Math.round(x.alto)).sort((a,b)=>Math.min(a.x.ancho,a.x.alto)-Math.min(b.x.ancho,b.x.alto)).map(o=>n(o.x.ancho)+' × '+n(o.x.alto)+' px · «'+o.x.texto+'» · '+o.x.zona+' · '+o.x.sel+' · '+donde(o.en)));
  bloque('Contraste por debajo de 4,5 a 1',junta('contrastesBajos',x=>x.sel+'|'+x.texto+'|'+x.color+x.fondo).sort((a,b)=>a.x.razon-b.x.razon).map(o=>n(o.x.razon)+' a 1 · «'+o.x.texto+'» · '+o.x.color+' sobre '+o.x.fondo+' · '+n(o.x.px)+' px'+(o.x.pasaComoGrande?' (texto grande: pasa con 3 a 1)':'')+' · '+o.x.zona+' · '+o.x.sel+' · '+donde(o.en)));
  bloque('Página más ancha que la ventana',R.estados.filter(h=>h.dato&&h.dato.pagina.desborda).map(h=>h.id+': '+h.dato.pagina.ancho+' de '+h.dato.pagina.ventana+' px'+((h.dato.pagina.culpables||[]).length?' · sobresalen: '+h.dato.pagina.culpables.map(c=>c.sel+' (hasta '+n(c.derecha)+')').join(', '):'')));
  bloque('Nombres de paradas futuras en la carta',R.estados.filter(h=>h.dato&&h.dato.nombresFuturos.length).map(h=>h.id+': '+h.dato.nombresFuturos.join(', ')));
  bloque('Emojis',junta('emojis',x=>x.car+'|'+x.donde).map(o=>'«'+o.x.car+'» '+o.x.codigo+' · '+o.x.donde+' · '+donde(o.en)));
  bloque('Textos cortados',junta('cortados',x=>x.sel+'|'+x.texto+'|'+x.por,x=>x.firme).map(o=>'«'+o.x.texto+'» · por '+o.x.por+' · '+o.x.zona+' · '+o.x.sel+' · '+donde(o.en)));
  bloque('Textos recortados por su caja (o por el borde de la carta)',junta('recortados',x=>x.sel+'|'+x.texto).map(o=>'«'+o.x.texto+'» · le faltan '+n(o.x.falta)+' px · recorta '+o.x.por+' · '+o.x.zona+' · '+o.x.sel+' · '+donde(o.en)));
  bloque('Textos que asoman a medias sobre el pie (se destapan al bajar)',junta('cortados',x=>x.sel+'|'+x.texto,x=>!x.firme).map(o=>'«'+o.x.texto+'» · '+o.x.zona+' · '+donde(o.en)));
  bloque('Rótulos de la carta tapados por algo de encima',junta('rotulosTapados',x=>x.texto+'|'+x.por).map(o=>'«'+o.x.texto+'» · por '+o.x.por+' ('+o.x.puntos+' puntos) · '+donde(o.en)));
  bloque('Rótulos de la carta bajo la caja de la barca',junta('barcaSobreRotulos',x=>x.texto).map(o=>'«'+o.x.texto+'» · '+o.x.solape+' · '+donde(o.en)));
  bloque('Rótulos de la carta encimados (por sus cajas)',junta('rotulosEncimados',x=>x.a+'|'+x.b).map(o=>'«'+o.x.a+'» con «'+o.x.b+'» · '+o.x.solape+' · '+donde(o.en)));
  const ap=R.estados.reduce((a,h)=>{if(h.dato)for(const k of ['mapa','imagen','dibujo'])a[k]+=h.dato.aparte[k];return a},{mapa:0,imagen:0,dibujo:0});
  decir('\nAparte (no hace fallar): '+ap.mapa+' textos sobre el mapa, '+ap.imagen+' sobre una imagen o un degradado y '+ap.dibujo+' dentro de un dibujo (sello, perfil), sumando los estados.');
  const sm=junta('sobreElMapa',x=>x.sel+'|'+x.texto,x=>x.mediana<(x.grande?3:4.5));
  for(const o of sm){let peor=o.x;for(const h of R.estados)for(const x of (h.dato&&h.dato.sobreElMapa)||[])if(x.sel===o.x.sel&&x.texto===o.x.texto&&x.mediana<peor.mediana)peor=x;o.x=peor}
  bloque('Sobre el mapa o una imagen, contraste medido en la captura por debajo de 4,5 a 1 (3 a 1 si el texto es grande); el peor estado de cada uno',sm.sort((a,b)=>a.x.mediana-b.x.mediana).map(o=>n(o.x.mediana)+' a 1 de mediana ('+n(o.x.bajo)+' en lo más claro) · «'+o.x.texto+'» · '+n(o.x.px)+' px · '+o.x.zona+' · '+o.x.sel+' · '+donde(o.en)));
  const tot=R.estados.reduce((a,h)=>a+((h.dato&&h.dato.sobreElMapa)||[]).length,0);if(tot)decir('  (medidos en la captura: '+tot+' textos sobre el mapa o una imagen, sumando los estados)');
  fs.mkdirSync(path.dirname(destino),{recursive:true});fs.writeFileSync(destino,JSON.stringify(R,null,1));decir('JSON: '+destino);
  listar(R.errores,R.avisos);
  const fallos=R.estados.filter(h=>h.fallo);if(fallos.length)decir('ESTADOS QUE NO SE PUDIERON ARMAR: '+fallos.map(h=>h.id+' ('+h.fallo+')').join('; '));
  decir(graves?'FALLA: hay '+graves+' estados con la página ancha, nombres futuros en la carta, emojis o sin armar':'sin página ancha, nombres futuros ni emojis');
  return graves||R.errores.length?1:0}

async function main(){
  const [cmd,...resto]=process.argv.slice(2);let tam={w:390,h:844},modo='mercader',solo=null;const libres=[];
  for(const a of resto){const m=/^(\d+)x(\d+)(?:@(\d(?:\.\d+)?))?$/.exec(a);if(m)tam={w:+m[1],h:+m[2],k:m[3]?+m[3]:2};   /* 1440x900@1: escala 1 en vez de 2 */
    else if(a==='mercader'||a==='historia')modo=a;else if(/^solo=/.test(a))solo=a.slice(5).split(',').filter(Boolean);else libres.push(a)}
  if(cmd==='auditar'&&libres.length>=1)return cmdAuditar(libres[0],tam,libres[1],solo);
  if(cmd==='estados'&&libres.length>=2)return cmdEstados(libres[0],libres[1],tam,solo);
  if(cmd==='foto'&&libres.length>=2)return cmdFoto(libres[0],libres[1],tam,libres[2]);
  if(cmd==='recorrido'&&libres.length>=2)return cmdRecorrido(libres[0],libres[1],tam,modo);
  if(cmd==='medir'&&libres.length>=1)return cmdMedir(libres[0],tam,libres[1]);
  console.error('uso:\n  node tools/captura.js auditar <archivo.html> [390x844] [salida.json] [solo=estado,estado]\n  node tools/captura.js estados <archivo.html> <carpeta> [390x844] [solo=estado,estado]\n  node tools/captura.js foto <archivo.html> <salida.png> [390x844] ["js a evaluar antes de la foto"]\n  node tools/captura.js recorrido <archivo.html> <carpeta> [390x844] [mercader|historia]\n  node tools/captura.js medir <archivo.html> [390x844] [carpeta para las capturas del viaje]');return 2}
main().then(c=>{process.exitCode=c},e=>{console.error('captura: '+(e&&e.message||e));process.exitCode=1});
