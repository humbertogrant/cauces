// Instantánea de Cauces: recorre dos ríos en los dos modos con azar y fecha fijos y compara el texto visible, la
// lectura en voz alta y el marcado de cada pantalla con test/instantanea.json.gz. Cualquier diferencia es un fallo:
// la migración a rutas no debe cambiar nada de lo que se ve o se oye en Cauces.
// Uso: node test/instantanea.js            compara (termina en "INSTANTÁNEA OK")
//      node test/instantanea.js --guardar  vuelve a tomar la instantánea (solo cuando el cambio es a propósito)
const fs=require('fs'),path=require('path'),zlib=require('zlib'),crypto=require('crypto');
const {montar,CAUCES}=require('./arnes');
const ARCHIVO=path.join(__dirname,'instantanea.json.gz'),GUARDAR=process.argv.includes('--guardar');
// azar y fecha fijos, antes de cargar el motor
let semilla=20260904;Math.random=()=>{semilla|=0;semilla=semilla+0x6D2B79F5|0;let t=Math.imul(semilla^semilla>>>15,1|semilla);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const FIJO=Date.UTC(2026,8,4,18,0,0),RealDate=Date;
global.Date=class extends RealDate{constructor(...a){super(...(a.length?a:[FIJO]))}static now(){return FIJO}};
montar(CAUCES);
const foto={},sha=s=>crypto.createHash('sha1').update(s).digest('hex').slice(0,16);
const texto=h=>String(h).replace(/<[^>]+>/g,' ').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/\s+/g,' ').trim();
function tomar(clave){const cab=document.querySelector('#cab').innerHTML,panel=document.querySelector('#panel').innerHTML,capa=document.querySelector('#capa').innerHTML,pf=document.getElementById('perfil'),perfil=pf.hidden?'':pf.innerHTML,pe=document.getElementById('pie'),pie=pe.hidden?'':pe.innerHTML;
  const voz=(S.pantalla==='inicio'||S.pantalla==='pasaporte')?[]:lectura();
  if(foto[clave])throw 'clave repetida '+clave;
  foto[clave]={h:sha(cab+'\n'+panel+'\n'+capa+pie+'\n'+perfil),t:texto(cab+' | '+panel+' | '+pie+' | '+perfil),v:voz.map(x=>String(x))}}
setTimeout(()=>{
  for(const modo of ['mercader','historia']){
    crearPerfil('Foto '+modo);setModo(modo);irInicio();tomar(modo+'/inicio');
    for(const id of ['danubio','sarapiqui']){
      const r=rioPor(id),n=r.ciudades.length,k=modo+'/'+id;
      abrirRio(id);tomar(k+'/descender/0');
      for(let p=0;p<=n;p++){
        const g=S.guias[S.paso];if(g&&g.resp==null){responderGuia(p%3===1?g.opciones.find(i=>i!==g.objetivo):g.objetivo);tomar(k+'/guia/'+p)}
        if(S.eco&&!S.eco.cerrado&&p>0){const of=r.mercado.map((x,gi)=>gi).filter(gi=>r.mercado[gi].o===p-1);if(of.length&&S.llaves[p-1]!==false){comprar(of[0]);tomar(k+'/compra/'+p)}if(S.eco.bodega.length&&p%2===0){vender(0);tomar(k+'/venta/'+p)}}
        paso(1);
        if(S.evento){tomar(k+'/evento/'+S.evento.tramo);responderEvento(p%2?S.evento.q.correcta:(S.evento.q.correcta+1)%S.evento.q.opciones.length);tomar(k+'/evento/'+S.evento.tramo+'/resp');continuarEvento()}
        tomar(k+'/descender/'+S.paso)}
      paso(-1);tomar(k+'/atras');paso(1);
      setTab('ordenar');tomar(k+'/ordenar/0');tocarChip(S.orden.pool[S.orden.pool.length-1]);tomar(k+'/ordenar/fallo');for(let i=0;i<n;i++)tocarChip(i);tomar(k+'/ordenar/fin');
      setTab('recitar');tomar(k+'/recitar/0');setPista('iniciales');revelar();tomar(k+'/recitar/rev');recordada(true);for(let i=1;i<n;i++){revelar();recordada(i%2===0)}tomar(k+'/recitar/fin');
      setTab('preguntar');for(let i=0;i<6;i++){tomar(k+'/preguntar/'+i);const q=S.quiz.qs[S.quiz.i];responder(i%2?q.correcta:(q.correcta+1)%q.opciones.length);tomar(k+'/preguntar/'+i+'/resp');siguiente()}tomar(k+'/preguntar/fin');
      verPasaporte();tomar(k+'/pasaporte')}
    irInicio();tomar(modo+'/inicio/2');iniciarReto();for(let i=0;i<3;i++){tomar(modo+'/reto/'+i);responder(S.quiz.qs[S.quiz.i].correcta);tomar(modo+'/reto/'+i+'/resp');siguiente()}
    irInicio();iniciarRepaso();tomar(modo+'/repaso');if(S.quiz){responder(S.quiz.qs[0].correcta);tomar(modo+'/repaso/resp')}
    irInicio();verZona('cr');tomar(modo+'/zona');verZona(null)}
  if(GUARDAR){fs.writeFileSync(ARCHIVO,zlib.gzipSync(JSON.stringify(foto)));console.log('instantánea guardada:',Object.keys(foto).length,'pantallas,',(fs.statSync(ARCHIVO).size/1024).toFixed(0),'KB');return}
  if(!fs.existsSync(ARCHIVO))throw 'no hay instantánea: node test/instantanea.js --guardar';
  const vieja=JSON.parse(zlib.gunzipSync(fs.readFileSync(ARCHIVO)));const claves=Object.keys(vieja);let marcado=0;
  if(claves.length!==Object.keys(foto).length)throw `la instantánea tenía ${claves.length} pantallas y ahora hay ${Object.keys(foto).length}`;
  for(const c of claves){const a=vieja[c],b=foto[c];if(!b)throw 'falta la pantalla '+c;
    if(a.t!==b.t){let i=0;while(i<a.t.length&&a.t[i]===b.t[i])i++;throw `texto distinto en ${c} cerca de «…${a.t.slice(Math.max(0,i-60),i+80)}» → «…${b.t.slice(Math.max(0,i-60),i+80)}»`}
    if(JSON.stringify(a.v)!==JSON.stringify(b.v))throw `lectura distinta en ${c}: ${JSON.stringify(a.v)} → ${JSON.stringify(b.v)}`;
    if(a.h!==b.h)marcado++}
  if(marcado)throw `el texto es igual pero el marcado cambió en ${marcado} pantalla(s); si es a propósito: node test/instantanea.js --guardar`;
  console.log('INSTANTÁNEA OK:',claves.length,'pantallas iguales')
},50);
