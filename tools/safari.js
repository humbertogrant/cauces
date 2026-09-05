// Prueba en el motor de Safari (WebKit, vía Playwright): abre los dos juegos con pantalla de iPhone, por http (servidor local en
// el puerto 8765) y por file://, ejercita un río o viaje y reporta errores de página y de consola, más una captura por caso.
// Uso (una sola vez, en una carpeta aparte para no meter dependencias al proyecto):
//   mkdir wk && cd wk && npm init -y && npm i playwright && npx playwright install webkit && node ../cauces-proyecto/tools/safari.js
// Resultado esperado: errores [] y consola [] en los cuatro casos. No sustituye la prueba en un iPhone de verdad.
const {webkit,devices}=require(require('path').resolve(process.cwd(),'node_modules','playwright'));
const fs=require('fs'),path=require('path');
const DIST='C:/Users/humbe/proyectos/geo/cauces-proyecto/dist';
(async()=>{
  const browser=await webkit.launch();
  const casos=[];
  for(const juego of ['cauces','exploradores']){
    for(const modo of ['http','file']){
      const url=modo==='http'?`http://localhost:8765/${juego}.html?wk=1`:'file:///'+DIST+'/'+juego+'.html';
      const ctx=await browser.newContext({...devices['iPhone 13'],locale:'es-CR'});
      const page=await ctx.newPage();
      const errores=[],consola=[];
      page.on('pageerror',e=>errores.push(String(e.message||e)));
      page.on('console',m=>{if(m.type()==='error'||m.type()==='warning')consola.push(m.type()+': '+m.text().slice(0,200))});
      let carga='ok';
      try{await page.goto(url,{waitUntil:'load',timeout:60000})}catch(e){carga='FALLA: '+String(e.message).slice(0,120)}
      await page.waitForTimeout(1500);
      const estado=await page.evaluate(()=>{try{return{panel:document.getElementById('panel').innerHTML.length,cab:document.getElementById('cab').textContent.trim().slice(0,40),rutas:typeof RUTAS!=='undefined'?RUTAS.length:null,tierra:(document.getElementById('tierra').getAttribute('d')||'').length,ls:(()=>{try{return Object.keys(localStorage).length}catch(e){return 'ERR '+e.name}})()}}catch(e){return{error:String(e)}}}).catch(e=>({evalError:String(e)}));
      let flujo=null;
      if(estado.rutas){
        flujo=await page.evaluate(async()=>{try{const r=RUTAS[0];abrirRio(r.id);await new Promise(x=>setTimeout(x,300));const g=S.guias[0];if(g)responderGuia(g.objetivo);paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}await new Promise(x=>setTimeout(x,300));return{pantalla:S.pantalla,paso:S.paso,kicker:document.querySelector('.kicker').textContent,capa:document.getElementById('capa').innerHTML.length,perfil:document.getElementById('perfil').innerHTML.length,barcaT:document.getElementById('barca')&&document.getElementById('barca').getAttribute('transform')}}catch(e){return{error:String(e)}}}).catch(e=>({evalError:String(e)}));
        await page.screenshot({path:path.join(__dirname,`wk-${juego}-${modo}.png`)});
      }
      casos.push({juego,modo,carga,errores,consola:consola.slice(0,6),estado,flujo});
      await ctx.close();
    }
  }
  await browser.close();
  console.log(JSON.stringify(casos,null,1));
})().catch(e=>{console.error('ERROR',e);process.exit(1)});
