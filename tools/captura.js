#!/usr/bin/env node
// Capturas y medidas del juego con el Edge o el Chrome del sistema, sin pantalla y sin dependencias: se le habla por el
// protocolo DevTools (CDP) con el WebSocket y el fetch que trae Node (22 o más). Es de Verificación (ver docs/vitrina/contrato.md).
//
//   node tools/captura.js foto <archivo.html> <salida.png> [390x844] ["js a evaluar antes de la foto"]
//   node tools/captura.js recorrido <archivo.html> <carpeta> [390x844] [mercader|historia]
//   node tools/captura.js medir <archivo.html> [390x844] [carpeta para las cinco capturas del viaje]
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
    const foto=async salida=>{const r=await cdp.send('Page.captureScreenshot',{format:'png'});fs.mkdirSync(path.dirname(path.resolve(salida)),{recursive:true});fs.writeFileSync(salida,Buffer.from(r.data,'base64'))};
    return {cdp,ev,cargar,recargar,clic,foto,errores,avisos,url,navegador:nav.exe,cerrar:async()=>{cdp.cerrar();await nav.cerrar()}}
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

async function main(){
  const [cmd,...resto]=process.argv.slice(2);let tam={w:390,h:844},modo='mercader';const libres=[];
  for(const a of resto){const m=/^(\d+)x(\d+)(?:@(\d(?:\.\d+)?))?$/.exec(a);if(m)tam={w:+m[1],h:+m[2],k:m[3]?+m[3]:2};else   /* 1440x900@1: escala 1 en vez de 2 */ if(a==='mercader'||a==='historia')modo=a;else libres.push(a)}
  if(cmd==='foto'&&libres.length>=2)return cmdFoto(libres[0],libres[1],tam,libres[2]);
  if(cmd==='recorrido'&&libres.length>=2)return cmdRecorrido(libres[0],libres[1],tam,modo);
  if(cmd==='medir'&&libres.length>=1)return cmdMedir(libres[0],tam,libres[1]);
  console.error('uso:\n  node tools/captura.js foto <archivo.html> <salida.png> [390x844] ["js a evaluar antes de la foto"]\n  node tools/captura.js recorrido <archivo.html> <carpeta> [390x844] [mercader|historia]\n  node tools/captura.js medir <archivo.html> [390x844] [carpeta para las capturas del viaje]');return 2}
main().then(c=>{process.exitCode=c},e=>{console.error('captura: '+(e&&e.message||e));process.exitCode=1});
