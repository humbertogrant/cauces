// Prueba de la vitrina del Nilo: carga los <script> de dist/nilo.html en el DOM simulado (como test/dist.js) y baja el río con
// las funciones del motor, en los dos modos. Comprueba lo que promete docs/vitrina/contrato.md:
//  (a) el juego arranca y RUTAS trae solo el Nilo;
//  (b) los ganchos se emiten en orden: por cada tramo, `zarpar` antes de `parada`, y `mar` una sola vez, al final;
//  (c) en la fase 'navega', las fichas del acróstico del panel son las paradas alcanzadas (.v-ficha.llena = S.paso; a lo sumo
//      una .v-ficha.proxima);
//  (d) memoria primero: la carta (#capa y lo que agregue la capa) no nombra ninguna parada futura, y el panel y el pie solo las
//      nombran en las fichas de la guía (botones .chip) o en la lista de la primera bajada, antes de zarpar();
//      Los textos que salen tal cual de los datos del juego de siempre (la imagen y el dato de cada parada, su puerto y su carga,
//      las frases del compañero, la embarcación y el contexto) no cuentan: son contenido de Cauces y la regla vale para lo que
//      agrega la vitrina; se quitan del texto comparando contra los datos, no contra clases de CSS;
//  (e) en Niño (mercader) y en Adulto (historia) se llega al mar sin excepciones;
//  (f) dist/nilo.html pesa menos de 900 KB;
//  (g) ningún emoji en lo que se dibuja en Bajar (#panel, #pie y #cab de cada pantalla del recorrido);
//  (h) las cifras fijas: los kilómetros y la altura de cada parada, la longitud del río, el orden y los nombres de las paradas y
//      lo que se lee de ellas son los mismos que en Cauces (dist/cauces-amplia.html, cargado en un proceso hijo con el mismo DOM
//      simulado); cada parada cae a 0,25° o menos del curso y sus idx crecen.
// Uso: node test/vitrina.js. Termina con "VITRINA OK" o lanza un error que dice qué falta. Es de Verificación.
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar}=require('./arnes');
const archivo=path.join(__dirname,'..','dist','nilo.html');
const falla=m=>{throw new Error('vitrina: '+m)};
/* las cifras fijas del Nilo en un HTML ensamblado, las que ve el jugador y las que las sostienen: nombres y orden de las paradas,
   kilómetros, alturas, longitud, lo que se lee (kicker, tramo y altura) y cómo cae cada parada sobre el curso. Se sacan con la misma
   función de dist/nilo.html y de dist/cauces-amplia.html; nada va escrito a mano */
function cifrasDe(){const r=rioPor('nilo'),V=r.vocab,n=r.paradas.length,sinTags=t=>String(t).replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();
  const alCurso=pos=>{let m=1e9;for(let i=1;i<r.curso.length;i++){const a=r.curso[i-1],b=r.curso[i],dx=b[1]-a[1],dy=b[0]-a[0],L=dx*dx+dy*dy,u=L?Math.max(0,Math.min(1,((pos[1]-a[1])*dx+(pos[0]-a[0])*dy)/L)):0;m=Math.min(m,Math.hypot(pos[1]-a[1]-u*dx,pos[0]-a[0]-u*dy))}return m};
  return {longitud:r.longitud,vertices:r.curso.length,paradas:r.paradas.map((c,i)=>({nombre:c.nombre,km:c.km,idx:c.idx,altura:alturaParada(r,i),
    kicker:sinTags(V.kickerParada(r,i+1,n,c)),tramo:sinTags(V.tramo(r,c,i?r.paradas[i-1]:null)),textoAltura:sinTags(textoAltura(r,i)),alCurso:alCurso(c.pos)}))}}
if(process.argv[2]==='--cifras'){   /* proceso hijo: las cifras de otro HTML ensamblado (el de Cauces), por la salida */
  montar([]);const h=fs.readFileSync(path.resolve(process.argv[3]),'utf8');[...h.matchAll(/<script>\n([\s\S]*?)<\/script>/g)].forEach((m,i)=>vm.runInThisContext(m[1],{filename:'cifras-script-'+i}));
  setTimeout(()=>process.stdout.write('@@CIFRAS@@'+JSON.stringify(cifrasDe())+'@@FIN@@'),50);return}
if(!fs.existsSync(archivo))falla('falta dist/nilo.html (lo arma `node build.js`)');
montar([]);
/* aquí las animaciones corren hasta el final (ver `drenar`), así que el nodo simulado necesita lo que el motor toca al terminar un
   viaje: classList.add/remove (las olas del mar), insertAdjacentHTML y querySelector (el salpicón) */
{const base=global.nodo;global.nodo=()=>{const x=base();Object.assign(x.classList,{add(){},remove(){}});x.insertAdjacentHTML=function(_,h){this.innerHTML+=h};x.querySelector=()=>null;x.remove=()=>{};x.offsetWidth=380;return x}}
/* los cuadros de animación: el arnés los descarta; aquí se guardan y `drenar` los corre con el reloj adelantado, para que cada
   viaje de la barca termine (y la capa anuncie la llegada) antes de seguir */
let cola=[];global.requestAnimationFrame=f=>{cola.push(f);return cola.length};global.cancelAnimationFrame=()=>{};
const drenar=()=>{for(let i=0;i<400&&cola.length;i++){const c=cola;cola=[];for(const f of c)f(performance.now()+60000)}if(cola.length)falla('una animación no termina nunca (400 cuadros con el reloj un minuto adelante)')};
const html=fs.readFileSync(archivo,'utf8'),TOPE_KB=900,kb=Math.round(fs.statSync(archivo).size/1024);
if(kb>=TOPE_KB)falla('dist/nilo.html pesa '+kb+' KB: pasa del tope de '+TOPE_KB+' KB');
const scripts=[...html.matchAll(/<script>\n([\s\S]*?)<\/script>/g)].map(m=>m[1]);if(scripts.length<5)falla('pocos <script> en dist/nilo.html ('+scripts.length+')');
scripts.forEach((s,i)=>vm.runInThisContext(s,{filename:'nilo.html-script-'+i}));
setTimeout(()=>{
  /* (a) arranca, y solo con el Nilo */
  if(typeof JUEGO==='undefined'||typeof RUTAS==='undefined'||typeof S==='undefined')falla('el juego no arrancó (faltan JUEGO, RUTAS o S)');
  if(RUTAS.length!==1||RUTAS[0].id!=='nilo')falla('RUTAS debía traer solo el Nilo y trae: '+RUTAS.map(r=>r.id).join(', '));
  if(typeof CAPA==='undefined')falla('falta CAPA (src/vitrina/capa.js no viaja en dist/nilo.html)');
  for(const f of ['oir','emitir','navegar','momento'])if(typeof CAPA[f]!=='function')falla('falta CAPA.'+f+' (contrato, «CAPA»)');
  drenar();
  const r=rioPor('nilo'),n=r.paradas.length,nodoDe=s=>document.querySelector(s).innerHTML||'';
  /* (h) las cifras fijas: las mismas que en Cauces (dist/cauces-amplia.html, cargado en un proceso hijo), y las paradas sobre el curso */
  {const otro=path.join(__dirname,'..','dist','cauces-amplia.html');if(!fs.existsSync(otro))falla('falta dist/cauces-amplia.html para comparar las cifras (lo arma `node build.js`)');
    let salida;try{salida=require('child_process').execFileSync(process.execPath,[__filename,'--cifras',otro],{encoding:'utf8',maxBuffer:1<<26})}catch(e){falla('no pude sacar las cifras de Cauces: '+(e&&e.message||e))}
    const m=/@@CIFRAS@@([\s\S]*)@@FIN@@/.exec(salida);if(!m)falla('el proceso hijo no devolvió las cifras de Cauces');
    const A=JSON.parse(m[1]),B=cifrasDe(),nombres=X=>X.paradas.map(c=>c.nombre).join(' · ');
    if(B.longitud!==A.longitud)falla('la longitud del Nilo es '+B.longitud+' km y en Cauces es '+A.longitud);
    if(nombres(B)!==nombres(A))falla('las paradas no son las de Cauces, en su orden: '+nombres(B)+' (en Cauces: '+nombres(A)+')');
    B.paradas.forEach((c,i)=>{const a=A.paradas[i],de=' de '+c.nombre+': ';
      if(Math.round(c.km)!==Math.round(a.km))falla('el kilómetro'+de+Math.round(c.km)+', y en Cauces es '+Math.round(a.km));
      if(c.altura!==a.altura)falla('la altura'+de+c.altura+' m, y en Cauces es '+a.altura+' m');
      for(const k of ['kicker','tramo','textoAltura'])if(c[k]!==a[k])falla('lo que se lee ('+k+')'+de+'«'+c[k]+'», y en Cauces es «'+a[k]+'»');
      if(!(c.alCurso<=0.25))falla(c.nombre+' cae a '+c.alCurso.toFixed(3)+'° del curso (el tope es 0,25°)');
      if(!(c.idx>=0&&c.idx<B.vertices))falla('el idx de '+c.nombre+' cae fuera del curso: '+c.idx+' de '+B.vertices+' vértices');
      if(i&&!(c.idx>B.paradas[i-1].idx))falla('los idx de las paradas no crecen: '+B.paradas.map(x=>x.nombre+' '+x.idx).join(', '))})}
  /* (b) los ganchos, en orden */
  const oidos=[];for(const k of ['zarpar','parada','mar'])CAPA.oir(k,d=>oidos.push({k,de:d&&d.de,a:d&&d.a,i:d&&d.i}));
  let dibujados=0;CAPA.oir('dibujado',()=>{dibujados++});   /* al final de cada render() */
  const ganchos=donde=>{
    if(!dibujados)falla('el motor no emitió ningún `dibujado` '+donde+' (contrato, «Ganchos del motor», punto 5: al final de cada render())');dibujados=0;
    const txt=oidos.map(o=>o.k==='zarpar'?'zarpar→'+o.a:o.k==='parada'?'parada '+o.i:'mar').join(' · ')||'(ninguno)';
    if(!oidos.some(o=>o.k==='zarpar'))falla('el motor no emitió ningún `zarpar` '+donde+': faltan los ganchos de eventos en src/motor.js (contrato, «Ganchos del motor», punto 5). Se oyó: '+txt);
    let esperada=0,mares=0;const zarpes={};
    oidos.forEach((o,j)=>{
      if(o.k==='zarpar'){if(!(o.a>=1&&o.a<=n+1))falla('`zarpar` con a='+o.a+' '+donde+' (debía ir de 1 a '+(n+1)+')');zarpes[o.a]=true}
      else if(o.k==='parada'){if(o.i!==esperada)falla('`parada` fuera de orden '+donde+': llegó la '+o.i+' y tocaba la '+esperada+'. Se oyó: '+txt);if(!zarpes[o.i+1])falla('`parada` '+o.i+' sin un `zarpar` hacia ella antes, '+donde+'. Se oyó: '+txt);esperada++}
      else{mares++;if(j!==oidos.length-1)falla('`mar` no fue lo último '+donde+'. Se oyó: '+txt);if(!zarpes[n+1])falla('`mar` sin un `zarpar` hacia el mar antes, '+donde+'. Se oyó: '+txt)}});
    if(esperada!==n)falla('se oyeron '+esperada+' `parada` de '+n+' '+donde+'. Se oyó: '+txt);
    if(mares!==1)falla('`mar` se oyó '+mares+' veces '+donde+' (debía ser una, al final). Se oyó: '+txt);
    oidos.length=0};
  /* (c) y (d): lo que se ve en cada momento */
  const sinDatos=h=>h.replace(/(src|href)="data:[^"]*"/g,''),sinFichas=h=>h.replace(/<button[^>]*class="[^"]*\bchip\b[^"]*"[^>]*>[\s\S]*?<\/button>/g,'');
  /* el texto que se lee o se oye: sin etiquetas (los números van envueltos en <span class="num">), más aria-label, title y alt */
  const plano=t=>String(t).replace(/\s+/g,' ').trim(),ent={'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#39;':"'",'&nbsp;':' '};
  const aTexto=h=>plano((h.replace(/<style\b[\s\S]*?<\/style>/g,' ').replace(/<[^>]*>/g,'')+' | '+[...h.matchAll(/\s(?:aria-label|title|alt)="([^"]*)"/g)].map(m=>m[1]).join(' | ')).replace(/&(?:amp|lt|gt|quot|#39|nbsp);/g,m=>ent[m]));
  /* lo que viene literalmente de los datos del juego de siempre: se quita antes de buscar nombres (de la cadena más larga a la más corta) */
  const cadenas=o=>typeof o==='string'?[o]:Array.isArray(o)?o.flatMap(cadenas):o&&typeof o==='object'?Object.values(o).flatMap(cadenas):[];
  const DATOS=[...new Set([...r.paradas.flatMap(c=>[c.imagen,c.dato,c.puerto,c.carga]),...cadenas(r.companero&&r.companero.paradas),...cadenas(r.vehiculo),...(r.contexto||[]).map(x=>x&&x.texto)]
    .filter(t=>typeof t==='string').map(plano).filter(t=>t.length>=12))].sort((a,b)=>b.length-a.length);
  const sinTextosDeDatos=t=>{for(const d of DATOS)if(t.includes(d))t=t.split(d).join(' ');return t};
  /* emojis: los pictogramas de Unicode (menos ©, ® y ™), las banderas, el selector de presentación de emoji y la tecla */
  const EMOJI=/\p{Extended_Pictographic}|[\u{1F1E6}-\u{1F1FF}]|️|⃣/gu,emojis=h=>[...new Set((h.match(EMOJI)||[]).filter(c=>!/[©®™]/.test(c)))];
  const cerca=(h,nom)=>{const i=h.indexOf(nom);return '…'+h.slice(Math.max(0,i-90),i+nom.length+40).replace(/\s+/g,' ')+'…'};
  const mirar=(etapa,donde)=>{const p=S.paso,g=S.guias[p],respondida=!!g&&g.resp!=null,aqui=donde+', paso '+p+' ('+etapa+')';
    if(etapa==='navega'){
      if(CAPA.fase!=='navega')falla('CAPA.navegar() no dejó la fase en navega, '+aqui);
      const fichas=[...nodoDe('#panel').matchAll(/class="([^"]*)"/g)].map(m=>m[1].split(/\s+/)).filter(c=>c.includes('v-ficha'));
      if(!fichas.length)falla('en la fase navega el panel no trae las fichas del acróstico (.v-ficha): falta src/vitrina/panel.js (CAPA.descender) o todavía no las dibuja; '+aqui);
      const llenas=fichas.filter(c=>c.includes('llena')).length,prox=fichas.filter(c=>c.includes('proxima')).length;
      if(fichas.length!==n)falla('el acróstico trae '+fichas.length+' fichas y el Nilo tiene '+n+' paradas; '+aqui);
      if(llenas!==p)falla('fichas llenas del acróstico: '+llenas+', y las paradas alcanzadas son '+p+'; '+aqui);
      if(prox>1)falla('hay '+prox+' fichas .proxima en el acróstico (a lo sumo una); '+aqui)}
    /* paradas futuras: de la que sigue en adelante; con la guía ya respondida, la que sigue ya se dijo («Zarpar a …») */
    const futuras=r.paradas.map(c=>c.nombre).slice(p+(respondida?1:0));
    for(const [k,nd] of Object.entries(nodos)){if(k!=='#capa'&&!/v-|carta|vitrina/i.test(k))continue;const h=sinDatos(String(nd.innerHTML||''));
      const hm=h.toLowerCase();   /* en la carta los rótulos pueden ir escritos en mayúsculas: se compara sin distinguirlas */
      for(const nom of futuras){const i=hm.indexOf(nom.toLowerCase());if(i>=0)falla('la carta ('+k+') nombra una parada futura, '+nom+'; '+aqui+': '+cerca(h,h.substr(i,nom.length)))}}
    for(const k of ['#panel','#pie','#cab']){const e=emojis(sinDatos(String((nodos[k]||{}).innerHTML||'')));
      if(e.length)falla('hay emojis en '+k+': '+e.map(c=>'«'+c+'» U+'+c.codePointAt(0).toString(16).toUpperCase()).join(', ')+'; '+aqui)}
    if(S.evento||(p===0&&!S.zarpo))return;   /* un evento pregunta con opciones; la primera bajada enseña la lista antes de zarpar */
    for(const k of ['#panel','#pie']){const h=sinTextosDeDatos(aTexto(sinFichas(sinDatos(nodoDe(k)))));
      for(const nom of futuras)if(h.includes(nom))falla((k==='#panel'?'el panel':'el pie')+' nombra una parada futura fuera de las fichas de la guía y de los textos de datos del juego, '+nom+'; '+aqui+': '+cerca(h,nom))}};
  /* (e) la bajada entera, con las funciones del motor */
  const bajar=donde=>{abrirRio('nilo',1);drenar();oidos.length=0;
    if(S.pantalla!=='rio'||S.paso!==0)falla('abrirRio no dejó la barca en la fuente, '+donde);
    if(CAPA.momento()!=='portada')falla('CAPA.momento() en la fuente dio «'+CAPA.momento()+'» y debía dar «portada», '+donde);
    mirar('portada',donde);
    for(let v=0;S.paso<n+1;v++){if(v>80)falla('la bajada no termina, '+donde+' (paso '+S.paso+')');
      if(S.evento){if(CAPA.momento()!=='evento')falla('CAPA.momento() durante una prueba entre puertos dio «'+CAPA.momento()+'» y debía dar «evento» (contrato, «Ganchos del motor», punto 6), '+donde+', paso '+S.paso);
        mirar('evento',donde);if(S.evento.resp==null)responderEvento(S.evento.q.correcta);mirar('evento resuelto',donde);continuarEvento();drenar();mirar('tras el evento',donde);continue}
      const p=S.paso;
      if(p<n){if(!S.zarpo){zarpar();drenar()}
        if(CAPA.fase!=='navega'){CAPA.navegar();drenar()}
        if(CAPA.momento()!=='navega')falla('CAPA.momento() con la guía a la vista dio «'+CAPA.momento()+'», '+donde+', paso '+p);
        mirar('navega',donde);
        const g=S.guias[p];if(!g)falla('no hay guía en el paso '+p+', '+donde);
        if(g.resp==null)responderGuia(g.objetivo);drenar();mirar('guía respondida',donde)}
      paso(1);drenar();
      if(!S.evento){if(S.paso!==p+1)falla('paso(1) no avanzó desde '+p+', '+donde);
        if(S.paso<=n&&CAPA.fase!=='parada')falla('paso() no devolvió la fase a parada (quedó en «'+CAPA.fase+'»), '+donde+', paso '+S.paso);
        mirar(S.paso>n?'mar':'parada',donde)}}
    if(CAPA.momento()!=='mar')falla('CAPA.momento() al final dio «'+CAPA.momento()+'» y debía dar «mar», '+donde);
    if(!P.vistos.nilo)falla('la bajada no quedó anotada (P.vistos), '+donde);
    ganchos(donde)};
  for(const [modo,nombre] of [['mercader','Niño'],['historia','Adulto']]){
    crearPerfil('Vitrina '+nombre);setModo(modo);drenar();
    try{bajar('en '+nombre+', primera bajada');bajar('en '+nombre+', segunda bajada')}
    catch(e){if(/^vitrina: /.test(e&&e.message))throw e;const x=new Error('vitrina: una excepción bajando el Nilo en '+nombre+' (paso '+S.paso+'): '+(e&&e.stack||e));throw x}}
  console.log('VITRINA OK',kb,'KB (tope '+TOPE_KB+')')
},50);
