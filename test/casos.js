// datos
const bajar=k=>{for(let i=0;i<k;i++){paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}}; // avanza k tramos resolviendo eventos
const ids=new Set();
for(const r of RIVERS){
  if(ids.has(r.id))throw 'id repetido '+r.id; ids.add(r.id);
  for(const k of ['id','nombre','continente','longitud','mar','marEn','nace','naceNota','antigua','moderna','pistaAntigua','pistaModerna','frase','curso','ciudades'])if(r[k]==null)throw r.id+' falta '+k;
  if(r.ciudades.length<4)throw r.id+' pocas ciudades';
  const ini=[...r.frase.matchAll(/\[([^\]]+)\]/g)].map(m=>m[1].toUpperCase());
  const cini=r.ciudades.map(c=>c.nombre[0].toUpperCase());
  if(ini.join('')!==cini.join(''))console.log('AVISO acróstico',r.id,ini.join(''),'vs',cini.join(''));
  for(const c of r.ciudades){for(const k of ['nombre','pais','pos','imagen','dato'])if(c[k]==null)throw r.id+' '+c.nombre+' falta '+k;
    if(c.imagen.length>260)console.log('imagen larga',r.id,c.nombre,c.imagen.length)}
  for(const p of r.curso)if(Math.abs(p[0])>90||Math.abs(p[1])>180)throw 'coord '+r.id;
  if(r.curso.length<(r.zona?20:40))throw r.id+' cauce demasiado simple: '+r.curso.length+' vértices';
  // cada ciudad cae cerca de su vértice (en grados); Tombuctú y Karachi están lejos del cauce de verdad
  r.ciudades.forEach((c,i)=>{const d=Math.hypot(r.curso[c.idx][0]-c.pos[0],r.curso[c.idx][1]-c.pos[1]),lim=['Tombuctú','Karachi'].includes(c.nombre)?1:0.25;if(d>lim)throw r.id+' '+c.nombre+' a '+d.toFixed(2)+'° del cauce';
    if(i&&c.idx<=r.ciudades[i-1].idx)throw r.id+' '+c.nombre+' comparte vértice con la parada anterior'});
  // brazos empalmados al cauce (o a otro brazo del río) y sin saltos absurdos entre vértices seguidos
  const dSeg=(p,a,b)=>{const t=Math.max(0,Math.min(1,((p[0]-a[0])*(b[0]-a[0])+(p[1]-a[1])*(b[1]-a[1]))/(((b[0]-a[0])**2+(b[1]-a[1])**2)||1)));return Math.hypot(p[0]-a[0]-t*(b[0]-a[0]),p[1]-a[1]-t*(b[1]-a[1]))};
  const dLin=(p,L)=>Math.min(...L.slice(1).map((b,i)=>dSeg(p,L[i],b)));
  (r.brazos||[]).forEach((b,k)=>{const otros=[r.curso].concat((r.brazos||[]).filter((x,j)=>j!==k)),d=Math.min(...otros.map(L=>Math.min(dLin(b[0],L),dLin(b[b.length-1],L))));if(d>0.02)throw r.id+' brazo '+k+' suelto: '+d.toFixed(3)+'°'});
  for(let i=1;i<r.curso.length;i++)if(hav(r.curso[i-1],r.curso[i])>230)throw r.id+' salto de '+Math.round(hav(r.curso[i-1],r.curso[i]))+' km en el vértice '+i;
}
console.log('ríos',RIVERS.length,'ciudades',RIVERS.reduce((a,r)=>a+r.ciudades.length,0));
// preguntas
for(const r of RIVERS)for(const t of ['ciudad','cerca','siguiente','antigua','moderna','mar','frase','imagen','pais','altura']){const q=preguntaTipo(t,r);const esp=q.tipo==='cerca'?3:4;if(q.opciones.length!==esp||q.correcta<0)throw 'pregunta mala '+t+' '+r.id;if(new Set(q.opciones).size!==esp)throw 'opciones repetidas '+t+' '+r.id}
// flujo completo
setTimeout(()=>{
for(const r of RIVERS){
  abrirRio(r.id);
  bajar(r.ciudades.length+1);
  if(!P.vistos[r.id])throw 'no visto '+r.id;
  setTab('ordenar');
  tocarChip(S.orden.pool[0]);            // probablemente error
  for(let i=0;i<r.ciudades.length;i++)tocarChip(i);
  if(!S.orden.listo)throw 'orden no listo '+r.id;
  setTab('preguntar');
  for(let i=0;i<6;i++){const q=S.quiz.qs[S.quiz.i];responder(q.correcta);siguiente()}
  if(document.querySelector('#panel').innerHTML.indexOf('de 6')<0)throw 'sin resultado '+r.id;
}
irInicio();
iniciarReto();for(let i=0;i<10;i++){responder(0);siguiente()}
irInicio();
iniciarRepaso();console.log('repaso qs',S.quiz.qs.length,'pendientes',pendientes().length);
const svg=document.querySelector('#capa').innerHTML;console.log('capa ok',svg.length>1000, 'dominio nilo',dominio(rioPor('nilo')).toFixed(2));
abrirRio('danubio');bajar(7);
console.log(document.querySelector('#capa').innerHTML.match(/<text[^>]*>[^<]*<\/text>/g));

for(const r of RIVERS){const n=NAVES[r.id];if(!n)throw 'sin nave '+r.id;if(n.puertos.length!==r.ciudades.length)throw 'puertos '+r.id+' '+n.puertos.length+' vs '+r.ciudades.length;
  for(const c of r.ciudades)if(!c.puerto||!c.carga)throw 'puerto vacío '+r.id+' '+c.nombre;
  for(const k of ['nombre','tipo','desc','zarpe','llegada'])if(!n[k])throw 'nave '+r.id+' falta '+k;
  if(r.ciudades[r.ciudades.length-1].carga!=='vendida')throw 'no vendida '+r.id}
abrirRio('tigris');let ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="nave"')<0)throw 'sin bloque nave';
paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="mercado"')<0)throw 'sin mercado tigris';
if(document.querySelector('#capa').innerHTML.indexOf('<g id="barca" class="barca"><g class="mece"><g transform="scale(')<0)throw 'sin glifo';
bajar(6);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('odres vuelven a Mosul')<0)throw 'sin llegada';
console.log('naves OK', document.getElementById('barca')._transform);

for(const r of RIVERS){const m=MASCOTAS[r.id];if(!m)throw 'sin mascota '+r.id;if(m.paradas.length!==r.ciudades.length)throw 'paradas mascota '+r.id+' '+m.paradas.length+' vs '+r.ciudades.length;
  for(const k of ['nombre','especie','emoji','hola','mar'])if(!m[k])throw 'mascota '+r.id+' falta '+k}
abrirRio('volga');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')<0||ph.indexOf('Soy Belu')<0)throw 'sin globo hola';
paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('tan angosto')<0)throw 'sin globo parada';
if(document.querySelector('#capa').innerHTML.indexOf('id="masc"')<0)throw 'sin mascota en mapa';
console.log('masc transform',document.getElementById('masc')._transform);
setTab('ordenar');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')<0)throw 'sin globo orden';
tocarChip(S.orden.pool.find(i=>i!==0));if(!VOCES.ordenMal.includes(S.orden.dicho))throw 'voz mal';
setTab('preguntar');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')<0)throw 'sin globo quiz';
responder(S.quiz.qs[0].correcta);if(!VOCES.quizBien.includes(S.quiz.dicho))throw 'voz bien';
irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="emo"')<0)throw 'sin emoji lista';
iniciarReto();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')>=0)throw 'globo antes de responder en reto';
responder(0);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')<0)throw 'sin globo tras responder en reto';
console.log('mascotas OK');

// economía: cada bien tiene origen válido; simulación de la mejor estrategia simple
for(const r of RIVERS){const M=MERCADOS[r.id];if(!M||!M.length)throw 'sin mercado '+r.id;
  for(const g of M){if(g.o<0||g.o>=r.ciudades.length-1)throw 'origen raro '+r.id+' '+g.n;if(g.m!=null&&(g.m<=g.o||g.m>=r.ciudades.length))throw 'mejor raro '+r.id+' '+g.n;
    const pf=precio(r,g,r.ciudades.length-1);if(pf==null)throw 'precio null '+r.id+' '+g.n}
  // oferta en cada puerto salvo el último
  for(let j=0;j<r.ciudades.length-1;j++)if(!M.some(g=>g.o===j))console.log('AVISO sin oferta',r.id,r.ciudades[j].nombre)}
abrirRio('niger');paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="mercado"')<0||ph.indexOf('comprar · 5')<0)throw 'sin mercado';
comprar(0);comprar(0);if(S.eco.monedas!==0||S.eco.bodega.length!==2)throw 'compra mal '+S.eco.monedas;
comprar(0);if(!VOCES.sinMonedas.includes(S.dicho))throw 'voz sin monedas';
bajar(2);/* Tombuctú (el harmatán salta en el tramo 3 y bajar lo resuelve) */ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('vender · 20')<0)throw 'precio oro Tombuctú: '+ph.match(/vender · \d+/g);
const m0=S.eco.monedas;vender(0);vender(0);if(S.eco.monedas!==m0+40)throw 'venta mal '+S.eco.monedas;
comprar(2);comprar(3);comprar(3);if(S.eco.bodega.length!==3||S.eco.monedas!==m0+40-3-8)throw 'compra 2 mal';
bajar(4);/* Port Harcourt */ph=document.querySelector('#panel').innerHTML;console.log('precios PH',ph.match(/vender · \d+/g));
paso(1);/* mar */if(!S.eco.cerrado)throw 'no cerrado';console.log('final',S.eco.final,'tesoro',P.tesoro,rango(P.tesoro));
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Cuentas del viaje')<0)throw 'sin cuentas';
paso(-1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Cerrado: ya llegaste')<0)throw 'mercado no cerrado al volver';
const tAntes=P.tesoro;paso(1);if(P.tesoro!==tAntes)throw 'doble tesoro';
// perecedero
abrirRio('tigris');paso(1);comprar(0);bajar(3);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('podrido · tirar')<0)throw 'sandía no se pudrió';vender(0);if(!VOCES.podrido.includes(S.dicho.replace('Sandías','{g}')))console.log('voz podrido',S.dicho);
irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Tesoro:')<0)throw 'sin tesoro en inicio';
console.log('economía OK');

// interruptor
irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="tabs modo"')<0||ph.indexOf('Tesoro:')<0)throw 'sin interruptor';
abrirRio('nilo');paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="mercado"')<0||ph.indexOf('class="puerto"')>=0)throw 'mercader: debe haber mercado y no narración';
irInicio();setModo('historia');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Tesoro:')>=0||ph.indexOf('sin monedas')<0)throw 'historia inicio mal';
abrirRio('nilo');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('bodega vacía')<0||ph.indexOf('Zarpás del lago Victoria')<0)throw 'historia zarpe mal';
paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="mercado"')>=0||ph.indexOf('El mercader llevaba: café')<0)throw 'historia: debe haber narración y no mercado';
if(S.eco!==null)throw 'eco no nulo';
bajar(6);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Cuentas del viaje')>=0||ph.indexOf('falúa no sale al mar')<0)throw 'historia mar mal';
if(JSON.parse(window.localStorage.getItem(store.clave(PERFILES.activo))).modo!=='historia')throw 'modo no persistido';
setModo('mercader');abrirRio('nilo');paso(1);if(!S.eco||S.eco.monedas!==10)throw 'vuelta a mercader mal';
console.log('interruptor OK');

setModo('mercader');
console.log('fantasma',RIVERS.map(r=>r.nombre+' '+r.fantasma).join(' | '));
// guía: respuesta correcta abre el mercado; incorrecta lo cierra a compras
abrirRio('nilo');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('¿Cuál es la próxima parada?')<0||ph.indexOf('Zarpar a')>=0)throw 'guía inicial mal';
if(S.guias[0].opciones.length!==3||!S.guias[0].opciones.includes(0))throw 'opciones guía mal';
responderGuia(0);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Zarpar a Jinja')<0||!VOCES.guiaBien.some(v=>S.dicho.startsWith(v.split('{c}')[0])))throw 'guía bien mal '+S.dicho;
paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Se vende aquí')<0)throw 'mercado no abrió tras acierto';
const mal=S.guias[1].opciones.find(i=>i!==1);responderGuia(mal);if(S.llaves[1]!==false)throw 'llave no cerrada';
paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('solo podés vender')<0||ph.indexOf('Se vende aquí')>=0)throw 'mercado no se cerró';
// pista con hueco
abrirRio('niger');paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('se paga mejor en T_______')<0)throw 'pista sin hueco: '+ph.match(/se paga mejor en [^<]*/);
// ordenar premia
setTab('ordenar');for(let i=0;i<7;i++)tocarChip(i);if(S.orden.premio!==5||!/\+5 monedas/.test(S.orden.dicho))throw 'premio orden mal';
// recitar
setTab('recitar');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Recitar')<0||ph.indexOf('Revelar')<0)throw 'recitar mal';
setPista('nada');for(let i=0;i<7;i++){revelar();recordada(true)}if(S.rec.i!==7||S.rec.premio!==5)throw 'recitar fin mal '+S.rec.premio;
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('7 de 7 recordadas')<0)throw 'sin resumen recitar';
// fantasma en cuentas
abrirRio('niger');bajar(8);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('El mercader de la ruta llegó con')<0)throw 'sin fantasma en cuentas';
if(!/mercader de la ruta/.test(S.dicho))throw 'dicho sin fantasma';
// historia: guía sin mercado
setModo('historia');abrirRio('rin');responderGuia(S.guias[0].opciones.find(i=>i!==0));if(!VOCES.guiaMalH.some(v=>S.dicho.startsWith(v.split('{c}')[0])))throw 'guiaMalH';
setModo('mercader');
console.log('uno y dos OK');

if(document.getElementById('lagos')._d.length<5000||document.getElementById('fronteras')._d.length<5000)throw 'capas vacías';
irInicio();if(document.getElementById('fronteras').style.display!=='none')throw 'fronteras visibles en mundo';
abrirRio('rin');if(document.getElementById('fronteras').style.display!=='')throw 'fronteras ocultas en río';
plegarMapa();
console.log('mapa OK');

// eventos: datos válidos y restricciones por reto
const RETOS=['imagen','ruta','pais','frase','mar'];let nEv=0;
for(const r of RIVERS){const E=EVENTOS[r.id],n=r.ciudades.length;if(!E||!E.length)throw 'sin eventos '+r.id;
  for(const e of E){nEv++;for(const k of ['tramo','icono','titulo','texto','reto','bien','mal'])if(e[k]==null)throw r.id+' evento falta '+k;
    if(e.tramo<1||e.tramo>n+1)throw 'tramo fuera de rango '+r.id;if(!RETOS.includes(e.reto))throw 'reto raro '+r.id+' '+e.reto;
    if(e.reto==='imagen'&&e.tramo<2)throw 'imagen sin ciudades vistas '+r.id;if(e.reto==='ruta'&&e.tramo>n-1)throw 'ruta sin parada siguiente '+r.id;if(e.reto==='pais'&&e.tramo>n)throw 'pais en el mar '+r.id;
    if(/moneda/i.test(e.bien+e.mal))throw 'evento menciona monedas '+r.id;if(e.texto.length>320)console.log('AVISO evento largo',r.id,e.titulo,e.texto.length)}
  if(new Set(E.map(e=>e.tramo)).size!==E.length)throw 'tramos repetidos '+r.id}
for(const id in EVENTOS)if(!rioPor(id))throw 'evento de río inexistente '+id;
console.log('eventos',nEv);
// eventos: flujo en Mercader (Nilo: cocodrilo en el tramo 3, cataratas en el 4)
setModo('mercader');abrirRio('nilo');bajar(2);const mAntes=S.eco.monedas;
paso(1);if(!S.evento||S.paso!==2)throw 'evento no saltó o el paso avanzó';
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="evento"')<0||ph.indexOf('Cocodrilos del Sudd')<0||ph.indexOf('Entre Juba y Jartum')<0||ph.indexOf('Seguir hacia')>=0||ph.indexOf('class="globo')<0)throw 'pantalla de evento';
if(document.querySelector('#capa').innerHTML.indexOf('id="barca"')<0)throw 'evento sin barca';
let q=S.evento.q;if(q.tipo!=='imagen'||q.opciones.length!==4||q.ciudad>1)throw 'pregunta del cocodrilo '+q.tipo+' '+q.ciudad;
responderEvento(q.correcta===0?1:0);if(S.evento.ok!==false||S.eco.monedas!==mAntes-2)throw 'fallo evento: monedas '+S.eco.monedas;
if(P.cards[q.cardId].box!==0)throw 'evento no marcó la tarjeta';
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Seguir hacia Jartum')<0||ph.indexOf('−2 monedas')<0)throw 'sin botón de seguir o sin multa';
responderEvento(q.correcta);if(S.evento.ok!==false)throw 'respondió dos veces';
continuarEvento();if(S.evento||S.paso!==3)throw 'no siguió a Jartum';
paso(-1);paso(1);if(S.evento||S.paso!==3)throw 'evento repetido';
const m2=S.eco.monedas;paso(1);if(!S.evento||S.evento.def.reto!=='ruta')throw 'cataratas no saltaron';q=S.evento.q;
if(q.tipo!=='siguiente'||q.opciones[q.correcta]!=='Luxor')throw 'ruta: debe preguntar qué sigue después de Asuán';
responderEvento(q.correcta);if(S.evento.ok!==true||S.eco.monedas!==m2+2)throw 'premio evento';
if(!P.cards['rio:nilo:orden']||P.cards['rio:nilo:orden'].box<1)throw 'ruta no marcó orden';
continuarEvento();if(S.paso!==4)throw 'no llegó a Asuán';
// eventos: Historia sin monedas; la aduana pregunta el país de la próxima parada
setModo('historia');abrirRio('danubio');bajar(3);paso(1);if(!S.evento||S.evento.def.reto!=='pais')throw 'aduana no saltó';
q=S.evento.q;if(q.texto.indexOf('Linz')<0||q.opciones[q.correcta]!=='Austria'||q.cardId)throw 'pregunta aduana '+q.texto;
{const r=rioPor('danubio'),m=S.evento.medio,a=r.ciudades[2].idx,b=r.ciudades[3].idx;/* el punto medio entre Passau y Linz debe quedar entre ambos, nunca encima de una parada */
  if(m.k<a||m.k>=b||m.pt.join()===r.curso[a].join()||m.pt.join()===r.curso[b].join())throw 'punto medio aduana '+JSON.stringify(m)+' '+a+'-'+b;
  if(document.querySelector('#capa').innerHTML.indexOf('<g id="barca"')<0)throw 'barca del evento'}
responderEvento(q.correcta);if(S.eco!==null||S.evento.delta!==0)throw 'historia con monedas';
ph=document.querySelector('#panel').innerHTML;if(/[+−]2 monedas/.test(ph))throw 'historia menciona monedas';
continuarEvento();if(S.paso!==4)throw 'no llegó a Linz';
// eventos: último tramo (Amazonas: pororoca) llega al mar
abrirRio('amazonas');bajar(5);paso(1);if(!S.evento||S.evento.tramo!==6)throw 'pororoca no saltó';
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Entre Belém y el mar')<0)throw 'kicker del mar';
responderEvento(S.evento.q.correcta);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Seguir hacia el mar')<0)throw 'sin seguir al mar';
continuarEvento();if(S.paso!==6||S.evento)throw 'no llegó al mar';
setModo('mercader');
// preguntas nuevas: la imagen no delata el nombre; el país correcto es el de la ciudad
for(const r of RIVERS){const qi=preguntaTipo('imagen',r,1),nom=r.ciudades[1].nombre;if(qi.texto.toLowerCase().indexOf(nom.toLowerCase())>=0)throw 'imagen delata '+r.id;
  if(qi.opciones[qi.correcta]!==esc(nom)||!qi.opciones.every(o=>r.ciudades.some(c=>esc(c.nombre)===o)))throw 'opciones imagen '+r.id;
  const qp=preguntaTipo('pais',r,0);if(qp.opciones[qp.correcta]!==esc(r.ciudades[0].pais))throw 'pais correcta '+r.id}
console.log('eventos OK');

// voz: limpieza del texto para el sintetizador
{const t=paraVoz('<b>M</b>i [S]obrino &amp; 6 650 km, siglo XV, siglos I-VI, c. 1550 a. C., 161 m, 11 km³, (___ suena a jinete) «hola»'),e='Mi Sobrino & 6650 kilómetros, siglo 15, siglos 1-6, hacia 1550 antes de Cristo, 161 metros, 11 kilómetros cúbicos, (esta ciudad suena a jinete) hola';if(t!==e)throw 'paraVoz: '+t}
// voz: botón en el globo y lectura por pantalla
const ss=window.speechSynthesis;setModo('mercader');setVoz('boton');abrirRio('nilo');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="voz"')<0)throw 'sin botón de voz';
let lec=lectura();if(!/^¡Soy Hipo!/.test(lec[0])||lec[1]!=='Nacimiento: Lago Victoria y lago Tana.'||lec[2]!=='¿Cuál es la próxima parada?'||!/^primera: /.test(lec[3])||lec.length!==6)throw 'lectura fuente '+JSON.stringify(lec);
voz.leer();if(!voz.hablando||ss.cola.length!==6||ss.cola[0].voice.lang!=='es-CR'||ss.cola[0].text!==paraVoz(lec[0]))throw 'voz.leer '+ss.cola.length;
voz.leer();if(voz.hablando||ss.cola.length)throw 'la voz no se calla';
paso(1);lec=lectura();if(lec[1]!=='Parada 1 de 6: Jinja, Uganda.'||!/^Imagen para recordar: Un jinete/.test(lec[2])||lec.some(t=>/Ripon/.test(t)))throw 'lectura parada '+JSON.stringify(lec);
setModo('historia');abrirRio('nilo');paso(1);if(!lectura().some(t=>/Ripon/.test(t)))throw 'Historia debe leer el dato';setModo('mercader');
// voz: evento, ordenar y quiz leen las opciones numeradas
abrirRio('nilo');bajar(2);paso(1);lec=lectura();if(!/^Cocodrilos del Sudd\. En el pantano/.test(lec[1])||!/^¿De qué ciudad del Nilo/.test(lec[2])||!/^cuarta: /.test(lec[6])||lec.length!==7)throw 'lectura evento '+JSON.stringify(lec);
responderEvento(S.evento.q.correcta);lec=lectura();if(lec.length!==4||!/ Ganás 2 monedas\.$/.test(lec[3]))throw 'lectura evento resuelto '+JSON.stringify(lec);
setTab('ordenar');lec=lectura();if(lec.length!==8||!/^Tocá las 6 ciudades/.test(lec[1]))throw 'lectura ordenar '+JSON.stringify(lec);
setTab('preguntar');lec=lectura();if(lec.length!==2+S.quiz.qs[0].opciones.length||!/^primera: /.test(lec[2]))throw 'lectura quiz '+JSON.stringify(lec);
voz.leer();irInicio();if(voz.hablando||ss.cola.length)throw 'la voz sigue al cambiar de pantalla';
console.log('voz OK');

// fuera de Claude: sin llamadas a ningún servicio, progreso por perfil en localStorage, copia en JSON
if(typeof otraImagen!=='undefined')throw 'otraImagen sigue existiendo';
abrirRio('nilo');paso(1);ph=document.querySelector('#panel').innerHTML;if(/Claude|otraImagen|class="ia"/.test(ph))throw 'quedó un resto de Claude en la parada';
irInicio();ph=document.querySelector('#panel').innerHTML;if(/dentro de Claude/.test(ph)||ph.indexOf('¿Quién juega?')<0||ph.indexOf('>Capitán<')<0||ph.indexOf('guardar en un archivo')<0||ph.indexOf('type="file"')<0)throw 'inicio sin perfiles o con restos de Claude';
const cardsCap=Object.keys(P.cards).length;if(!cardsCap||PERFILES.activo!=='Capitán')throw 'Capitán sin progreso';
crearPerfil('  Ana  ');if(PERFILES.activo!=='Ana'||Object.keys(P.cards).length)throw 'perfil nuevo mal';
if(!JSON.parse(window.localStorage.getItem('cauces:perfiles')).lista.includes('Ana'))throw 'perfiles no persistidos';
marcar('prueba:ana',true);if(!JSON.parse(window.localStorage.getItem(store.clave('Ana'))).cards['prueba:ana'])throw 'Ana no guarda';
crearPerfil('ana');if(PERFILES.activo!=='Ana'||PERFILES.lista.length!==2)throw 'nombre repetido debe elegir, no duplicar';
elegirPerfil(0);if(PERFILES.activo!=='Capitán'||Object.keys(P.cards).length!==cardsCap||P.cards['prueba:ana'])throw 'volver a Capitán mal';
ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="chip bien" onclick="elegirPerfil(0)"')<0)throw 'chip activo mal';
const d=JSON.parse(progresoJSON());if(d.app!=='cauces'||d.perfil!=='Capitán'||Object.keys(d.progreso.cards).length!==cardsCap)throw 'progresoJSON mal';
d.perfil='Beto';d.progreso.tesoro=999;if(!importarTexto(JSON.stringify(d))||PERFILES.activo!=='Beto'||P.tesoro!==999||PERFILES.lista.length!==3||!/Beto cargado/.test(S.aviso))throw 'importar mal';
if(importarTexto('esto no es json')||!/no tiene un progreso/.test(S.aviso))throw 'importar basura';
quitarPerfil();if(PERFILES.lista.includes('Beto')||window.localStorage.getItem(store.clave('Beto'))||PERFILES.activo!=='Capitán')throw 'quitar mal';
// migración del guardado viejo (cauces:progreso sin perfiles)
store.borrar('cauces:perfiles');store.escribir('cauces:progreso',{cards:{viejo:{box:2,due:0}},vistos:{}});cargarPerfiles();
if(PERFILES.activo!=='Capitán'||!P.cards.viejo||window.localStorage.getItem('cauces:progreso')||!window.localStorage.getItem('cauces:perfiles'))throw 'migración mal';
console.log('perfiles OK');

// Costa Rica: zona propia (distractores de la misma zona), grupo en la lista, marcador en el mundo y mapa de zona
{const cr=RIVERS.filter(r=>r.zona==='cr');if(cr.length!==6)throw 'faltan ríos de Costa Rica';
 const t=rioPor('tempisque');if(otrosRios(t,3).some(x=>x.zona!=='cr'))throw 'distractores fuera de Costa Rica';if(otrosRios(rioPor('nilo'),3).some(x=>x.zona))throw 'distractores del mundo con Costa Rica';
 const qm=preguntaTipo('mar',t);if(qm.opciones.length!==4||!qm.opciones.includes('Golfo de Nicoya'))throw 'mar tempisque '+qm.opciones;
 irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Ríos de Costa Rica')<0||ph.indexOf('Tempisque')<0||ph.indexOf('5 paradas')<0)throw 'lista sin Costa Rica';
 let capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('class="zona"')<0||capa.indexOf('Costa Rica')<0||capa.indexOf("abrirRio('tempisque')")>=0||capa.indexOf("abrirRio('nilo')")<0)throw 'mundo: marcador de zona o ríos tocables mal';
 verZona('cr');capa=document.querySelector('#capa').innerHTML;if(capa.indexOf("abrirRio('tempisque')")<0||capa.indexOf("abrirRio('nilo')")>=0||capa.indexOf('>Sarapiquí<')<0)throw 'zona: ríos tocables o etiquetas mal';
 if(document.querySelector('.mundo').hidden!==false)throw 'botón Mundo oculto en zona';
 abrirRio('sanjuan');bajar(3);paso(1);if(!S.evento||S.evento.def.reto!=='pais'||S.evento.q.opciones[S.evento.q.correcta]!=='Costa Rica')throw 'frontera del San Juan';
 responderEvento(S.evento.q.correcta);continuarEvento();if(document.querySelector('.mundo').hidden!==true)throw 'botón Mundo visible en un río';
 irInicio();if(S.zona!=='cr')throw 'volver debe conservar la zona';verZona(null);if(document.querySelector('.mundo').hidden!==true)throw 'botón Mundo visible en el mundo';
 console.log('Costa Rica OK')}
// pasaporte: el sello se gana llegando con la guía acertada; dorado con caja ≥ 3; el río completo se pinta en el mapa
{setModo('mercader');abrirRio('rin');const r=rioPor('rin'),n=r.ciudades.length;
 for(let i=0;i<n;i++){responderGuia(i);paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}
 if(sellosDe(r)!==n||!completo(r))throw 'sellos del Rin '+sellosDe(r);
 ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="sello-nuevo"')<0||ph.indexOf('Sello de Rotterdam')<0)throw 'sin aviso de sello nuevo';
 if(!JSON.parse(window.localStorage.getItem(store.clave(PERFILES.activo))).sellos['rin:0'])throw 'sello no persistido';
 if(!lectura().some(t=>/Sello de Rotterdam/.test(t)))throw 'la voz no lee el sello';
 abrirRio('volga');responderGuia(S.guias[0].opciones.find(i=>i!==0));paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}
 if(sellosDe(rioPor('volga'))!==0)throw 'sello sin acertar la guía';ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Sin sello esta vez')<0)throw 'sin nota de sello perdido';
 paso(-1);paso(1);if(sellosDe(rioPor('volga'))!==0)throw 'sello al ir y volver';
 irInicio();ph=document.querySelector('#panel').innerHTML;if(!/Pasaporte \(\d+\)/.test(ph)||ph.indexOf('· completo')<0)throw 'inicio sin pasaporte';
 let capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('class="rio hecho"')<0||(capa.match(/class="rio hecho"/g)||[]).length!==1)throw 'mapa sin el río dorado (o con más de uno)';
 verPasaporte();ph=document.querySelector('#panel').innerHTML;if(S.pantalla!=='pasaporte'||ph.indexOf('Rotterdam')<0||ph.indexOf(`${n} de ${n} sellos`)<0||ph.indexOf('class="sello vacio"')<0||ph.indexOf('Pasaporte de Capitán')<0)throw 'pantalla de pasaporte';
 for(let k=0;k<3;k++)marcar('ciudad:rin:0',true);verPasaporte();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="sello oro"')<0)throw 'sin sello dorado';
 const d=JSON.parse(progresoJSON());if(!d.progreso.sellos['rin:0'])throw 'sellos fuera del json';d.perfil='Zoe';importarTexto(JSON.stringify(d));if(!P.sellos['rin:0']||PERFILES.activo!=='Zoe')throw 'sellos no importados';quitarPerfil();
 irInicio();console.log('pasaporte OK')}
// interruptor Niño/Adulto: el niño ve textos plegados, animal y lectura automática; el adulto, todo el texto, animal solo para reaccionar, sin lectura sola
{setModo('mercader');setVoz('auto');irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('>Niño<')<0||ph.indexOf('>Adulto<')<0||ph.indexOf('Lee sola')<0)throw 'sin interruptor Niño/Adulto';
 const ss=window.speechSynthesis;abrirRio('nilo');if(!voz.hablando||!ss.cola.length||!/Soy Hipo/.test(ss.cola[0].text))throw 'niño: no leyó sola al abrir el río';
 ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<details class="mas">')<0||ph.indexOf('Contame más')<0||ph.indexOf('<h3>Ruta antigua</h3>')>=0)throw 'niño: ruta antigua sin plegar';
 const antes=ss.cola.length;responderGuia(0);if(!(ss.cola.length>0&&ss.cola.length<antes)||!/Zarpamos|acordaba|Rumbo/.test(ss.cola[0].text))throw 'niño: no leyó la reacción de la guía '+ss.cola.length;
 paso(1);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<details class="mas">')<0||document.querySelector('#capa').innerHTML.indexOf('id="masc"')<0)throw 'niño: dato sin plegar o sin mascota en la barca';
 setVoz('boton');abrirRio('nilo');if(voz.hablando)throw 'con el botón no debe leer sola';
 setModo('historia');setVoz('auto');abrirRio('nilo');ph=document.querySelector('#panel').innerHTML;if(voz.hablando||ph.indexOf('class="globo"')<0||ph.indexOf('<details')>=0||ph.indexOf('<h3>Ruta antigua</h3>')<0||(ph.match(/class="voz/g)||[]).length!==1)throw 'adulto: leyó sola, escondió al animal, plegó texto o no tiene un solo botón de voz';
 responderGuia(0);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="globo"')<0)throw 'adulto: la reacción de la guía debe verse';
 paso(1);if(document.querySelector('#capa').innerHTML.indexOf('id="masc"')<0)throw 'adulto: el animal debe ir en la barca también';
 if(!lectura().some(t=>/Ripon/.test(t)))throw 'adulto: la voz debe leer el dato';
 irInicio();iniciarReto();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="voz"')<0||ph.indexOf('class="globo"')>=0)throw 'reto sin botón de voz';
 iniciarRepaso();if(S.pantalla==='quiz'){ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="voz"')<0)throw 'repaso sin botón de voz'}
 const d=JSON.parse(progresoJSON());if(d.progreso.voz!=='auto')throw 'voz fuera del json';
 setModo('mercader');setVoz('boton');irInicio();console.log('interruptor Niño/Adulto OK')}
// Hoy: las nuevas entran con tope diario e intercalando ríos; las vencidas ya repasadas entran siempre; el día reinicia el tope
{crearPerfil('Hoy');abrirRio('nilo');bajar(7);abrirRio('rin');bajar(8);irInicio();
 const nuevas=Object.keys(P.cards).filter(id=>P.cards[id].nuevo).length;if(nuevas<15)throw 'sembrar no marca nuevas '+nuevas;
 const cola=colaHoy();if(cola.length!==NUEVAS_POR_DIA)throw 'tope diario '+cola.length;
 if(cola[0].split(':')[1]===cola[1].split(':')[1])throw 'no intercala ríos '+cola.slice(0,2);
 ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('class="hoy"')<0||ph.indexOf('10 tarjetas por repasar')<0||ph.indexOf('unos 3 min')<0||ph.indexOf('esperando turno')<0||ph.indexOf('intercalados')<0)throw 'bloque Hoy: '+(ph.match(/class="hoy".{0,260}/)||[''])[0];
 iniciarRepaso();if(S.quiz.qs.length!==10)throw 'repaso de hoy '+S.quiz.qs.length;for(let i=0;i<10;i++){responder(S.quiz.qs[S.quiz.i].correcta);siguiente()}
 if(P.dia.nuevas!==10||colaHoy().length!==0)throw 'tope no se agota '+P.dia.nuevas+' '+colaHoy().length;
 const espera=nuevasEnEspera();if(espera<5)throw 'nuevas en espera '+espera;
 irInicio();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('Nada pendiente hoy')<0||!/mañana entran \d+ más/.test(ph))throw 'Hoy sin nada: '+(ph.match(/class="hoy".{0,300}/)||[''])[0];
 P.cards['rio:nilo:mar']={box:1,due:0};if(colaHoy().length!==1)throw 'la vencida repasada no entra';
 const espera2=nuevasEnEspera();P.dia.fecha='2000-01-01';if(colaHoy().length!==1+Math.min(espera2,NUEVAS_POR_DIA))throw 'no reinicia el día '+colaHoy().length+' vs '+(1+Math.min(espera2,NUEVAS_POR_DIA));
 const d=JSON.parse(progresoJSON());if(!d.progreso.dia)throw 'día fuera del json';
 quitarPerfil();console.log('Hoy OK')}
// luz y clima: amanecer en la fuente, atardecer y oleaje en el mar; el clima sale del icono del evento y dura hasta continuar; inicio liviano
{setModo('mercader');abrirRio('misisipi');const luz=document.getElementById('luz'),cl=document.getElementById('clima'),mapa=document.getElementById('mapa');
 if(luz['_data-luz']!=='amanecer'||!(parseFloat(luz.style.opacity)>0.3))throw 'sin amanecer en la fuente '+luz['_data-luz']+' '+luz.style.opacity;
 bajar(2);paso(1);if(!S.evento||cl['_data-clima']!=='niebla')throw 'la niebla del Misisipi no se ve: '+cl['_data-clima'];
 responderEvento(S.evento.q.correcta);if(cl['_data-clima']!=='niebla')throw 'el clima debe quedarse hasta continuar';continuarEvento();if(cl['_data-clima']!=='')throw 'el clima no se fue';
 if(luz['_data-luz']!=='')throw 'a mitad del río no hay luz especial: '+luz['_data-luz'];
 bajar(3);if(luz['_data-luz']!=='atardecer'||!(parseFloat(luz.style.opacity)>0.3)||mapa['_data-mar']!=='vivo')throw 'sin atardecer ni oleaje en el mar '+luz['_data-luz']+' '+mapa['_data-mar'];
 irInicio();if(luz['_data-luz']!==''||cl['_data-clima']!==''||mapa['_data-mar']!=='')throw 'el inicio debe quedar sin luz ni clima';
 ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<details class="mas ajustes"><summary>Ajustes')<0||ph.indexOf('¿Cómo se juega?')<0||ph.indexOf('¿Quién juega?')>ph.indexOf('class="hoy"')||ph.indexOf('Un palacio de la memoria por río')>=0||ph.indexOf('class="tabs modo"')<0)throw 'inicio no está liviano';
 console.log('luz y clima OK')}
// barcas: glifos propios por tipo, barca viva (mece, estela, bamboleo) y la barca dibujada en el bloque de la embarcación
{const tipos=['latina','junco','vapor','balsa','canoa','barcaza','cuadrada'],gl=tipos.map(glifo);
 if(new Set(gl).size!==7||gl.some(g=>g.indexOf('class="casco"')<0)||gl.some(g=>g.length>760)||glifo('otro')!==glifo('cuadrada'))throw 'glifos: '+gl.map(g=>g.length);
 if(glifo('vapor').indexOf('class="humo"')<0||glifo('junco').indexOf('class="vela"')<0||glifo('canoa').indexOf('class="fig"')<0)throw 'glifos sin sus partes';
 setModo('mercader');abrirRio('misisipi');let capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('<g id="barca" class="barca"><g class="mece">')<0||capa.indexOf('<path id="estela"')<0)throw 'barca sin mece o sin estela';
 ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="barca mini"')<0||ph.indexOf('class="humo"')<0)throw 'sin la barca en el bloque de la embarcación';
 responderGuia(S.guias[0].opciones.find(i=>i!==0));capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('class="barca duda"')<0||S.bamboleo)throw 'sin bamboleo tras errar la guía';
 paso(1);capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('class="barca duda"')>=0)throw 'el bamboleo no debe repetirse';
 bajar(5);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="barca mini"')<0)throw 'sin la barca al llegar al mar';
 console.log('barcas OK')}
// animales: un glifo SVG por especie, en el globo, la lista, el pasaporte y la barca; salto en el evento
{if(Object.keys(ANIMALES).length<17)throw 'faltan glifos de animales';
 for(const r of RIVERS){const m=MASCOTAS[r.id];if(!m.glifo||!ANIMALES[m.glifo])throw 'mascota sin glifo '+r.id;const g=ANIMALES[m.glifo];if(g.length>560||(g.indexOf('class="cuerpo"')<0&&g.indexOf('class="claro"')<0))throw 'glifo raro '+m.glifo+' '+g.length}
 if(animal({emoji:'x'})!=='x')throw 'sin glifo debe caer al emoji';
 setModo('mercader');abrirRio('nilo');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<div class="globo"><span class="emo" aria-hidden="true"><svg class="animal"')<0)throw 'globo sin animal';
 let capa=document.querySelector('#capa').innerHTML;if(capa.indexOf('<g id="masc"><g class="animal" transform="translate(-9 -9) scale(.6)">')<0)throw 'barca sin animal';
 bajar(2);paso(1);ph=document.querySelector('#panel').innerHTML;if(!S.evento||ph.indexOf('<div class="globo salta">')<0)throw 'el animal no salta en el evento';
 irInicio();ph=document.querySelector('#panel').innerHTML;if((ph.match(/<svg class="animal"/g)||[]).length<RIVERS.length)throw 'lista sin animales';
 verPasaporte();ph=document.querySelector('#panel').innerHTML;if((ph.match(/<svg class="animal"/g)||[]).length<RIVERS.length)throw 'pasaporte sin animales';
 setModo('historia');abrirRio('nilo');if(document.querySelector('#capa').innerHTML.indexOf('id="masc"')<0)throw 'adulto: sin animal en la barca';setModo('mercader');
 irInicio();console.log('animales OK')}
// escenas: todas las ciudades y extremos con pictogramas válidos; postal en la parada, la fuente y el mar; pista en el reto de imagen; sello con pictograma
{if(Object.keys(PICTOS).length<36)throw 'faltan pictogramas';
 for(const r of RIVERS){for(const k of ['escenaNace','escenaMar'])if(!r[k]||r[k].length<3||r[k].some(x=>!picto(x)))throw r.id+' '+k+' inválida';
   r.ciudades.forEach(c=>{if(!c.escena||c.escena.length<3||c.escena.length>4||c.escena.some(x=>!picto(x)))throw r.id+' '+c.nombre+' escena inválida'})}
 for(const k in PICTOS)if(PICTOS[k].length>620)throw 'pictograma pesado '+k+' '+PICTOS[k].length;
 setModo('mercader');abrirRio('terraba');ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="escena"')<0)throw 'fuente sin postal';
 bajar(4);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="escena"')<0||ph.indexOf(PICTOS.mascara)<0)throw 'Rey Curré sin su máscara';
 bajar(3);ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="escena"')<0)throw 'mar sin postal';
 const q=preguntaTipo('imagen',rioPor('tarcoles'),4);if(!q.escena||q.escena.indexOf('animal:cocodrilo')<0)throw 'reto de imagen sin escena';
 S.pantalla='rio';S.rio='tarcoles';setTab('preguntar');S.quiz.qs=[q];S.quiz.i=0;render();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="escena quiz"')<0||ph.indexOf('<g class="animal"')<0)throw 'el reto no muestra la escena';
 abrirRio('tarcoles');responderGuia(0);paso(1);verPasaporte();ph=document.querySelector('#panel').innerHTML;if(ph.indexOf('<svg class="escena pic"')<0)throw 'sello sin pictograma';
 irInicio();console.log('escenas OK')}
// sellos con carácter: forma, inclinación y aro propios por ciudad, estables, y el vacío con su forma
{crearPerfil('Sellos');const r=rioPor('rin'),n=r.ciudades.length;setModo('mercader');abrirRio('rin');for(let i=0;i<n;i++){responderGuia(i);paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}
 const s=r.ciudades.map((c,i)=>sello(r,i));if(s.some(x=>x.indexOf('<svg class="sello')<0||x.indexOf('<textPath')<0||x.indexOf('RIN · ')<0))throw 'sello sin aro o sin svg';
 const formas=new Set(s.map(x=>(x.match(/<g class="forma">(<\w+)/)||[])[1])),rots=new Set(s.map(x=>(x.match(/--rot:(-?\d+)deg/)||[])[1]));
 if(formas.size<3||rots.size<4)throw 'sellos demasiado iguales: formas '+formas.size+' giros '+rots.size;
 if(sello(r,0)!==sello(r,0))throw 'el sello no es estable';
 if(sello(rioPor('nilo'),0).indexOf('class="sello vacio"')<0||sello(rioPor('nilo'),0).indexOf('class="forma"')<0)throw 'vacío sin forma';
 for(let k=0;k<3;k++)marcar('ciudad:rin:1',true);if(sello(r,1).indexOf('class="sello oro"')<0||sello(r,1).indexOf('★')<0)throw 'oro sin estrellas';
 sellos()['sanjuan:5']=Date.now();if(sello(rioPor('sanjuan'),5).indexOf('textLength="78"')<0||sello(rioPor('sanjuan'),5).indexOf('SAN JUAN · NICARAGUA')<0)throw 'nombre largo sin ajuste o aro sin país';delete sellos()['sanjuan:5'];
 quitarPerfil();console.log('sellos OK')}
// auditoría permanente: el animal nunca desaparece durante la ruta, en ningún modo, ni del globo ni de la barca (cuando el mapa muestra el río)
{const faltas=[];const panel=()=>document.querySelector('#panel').innerHTML,capa=()=>document.querySelector('#capa').innerHTML;
 const revisa=(modo,rio,donde)=>{if(panel().indexOf('class="globo')<0)faltas.push(modo+' '+rio+' '+donde+': globo');if(S.pantalla==='rio'&&capa().indexOf('rio activo')>=0&&capa().indexOf('id="masc"')<0)faltas.push(modo+' '+rio+' '+donde+': barca')};
 crearPerfil('Auditoría');setVoz('boton');
 for(const modo of ['mercader','historia']){setModo(modo);
  for(const r of RIVERS){abrirRio(r.id);const n=r.ciudades.length;revisa(modo,r.id,'fuente');
   for(let p=0;p<=n;p++){responderGuia(S.guias[p]?S.guias[p].objetivo:0);revisa(modo,r.id,'guía '+p);paso(1);
    if(S.evento){revisa(modo,r.id,'evento '+S.evento.tramo);responderEvento(S.evento.q.correcta);revisa(modo,r.id,'evento resuelto');continuarEvento()}
    revisa(modo,r.id,S.paso<=n?'parada '+S.paso:'mar')}
   setTab('ordenar');revisa(modo,r.id,'ordenar');setTab('recitar');revisa(modo,r.id,'recitar');revelar();revisa(modo,r.id,'recitar revelada');
   setTab('preguntar');revisa(modo,r.id,'preguntar');responder(S.quiz.qs[0].correcta);revisa(modo,r.id,'preguntar respondida')}
  irInicio();iniciarReto();revisa(modo,'reto','antes');if(panel().indexOf('class="globo neutro"')<0)faltas.push(modo+' reto sin globo neutro');responder(0);revisa(modo,'reto','después')}
 quitarPerfil();setModo('mercader');irInicio();if(faltas.length)throw 'el animal desaparece en '+faltas.length+' momentos, p. ej. '+faltas.slice(0,5).join(' | ');
 console.log('animal siempre presente OK')}
// relieve: franjas por vista, nombres de relieve, perfil de altura del cauce (nunca sube) y pregunta de altura
{for(const z of ['mundo','cr']){if(!RELIEVE[z]||RELIEVE[z].length<2)throw 'relieve sin franjas '+z;let prev=0;for(const [a,d] of RELIEVE[z]){if(a<=prev||d.length<500||d[0]!=='M')throw 'franja mala '+z+' '+a;prev=a}}
 for(const r of RIVERS){const P=ALTURAS[r.id];if(!P||P.length<6)throw 'sin perfil '+r.id;if(P[0][0]!==0||P[P.length-1][0]!==1)throw 'perfil sin extremos '+r.id;
   for(let i=1;i<P.length;i++){if(P[i][0]<=P[i-1][0])throw 'perfil desordenado '+r.id;if(P[i][1]>P[i-1][1])throw 'el río sube '+r.id}
   if(P[P.length-1][1]>0||P[P.length-1][1]<-30)throw 'mar raro '+r.id+' '+P[P.length-1][1];
   const alts=r.ciudades.map((c,i)=>alturaParada(r,i));for(let i=1;i<alts.length;i++)if(alts[i]>alts[i-1])throw 'paradas que suben '+r.id;if(alts[0]>P[0][1])throw 'parada sobre la fuente '+r.id}
 const vistas={};for(const L of NOMBRES_RELIEVE){if(!L.n||!L.t||!L.z)throw 'etiqueta mala '+JSON.stringify(L);
   if(L.z==='mundo'){if(!L.v||!Object.keys(L.v).length)throw 'etiqueta sin vistas '+L.n;for(const k in L.v){if(!rioPor(k))throw 'vista de río inexistente '+k;vistas[k]=(vistas[k]||0)+1}}
   else{if(!L.p)throw 'etiqueta sin posición '+L.n;if(L.t==='pico'&&!(L.e>0))throw 'pico sin altura '+L.n;vistas[L.z]=(vistas[L.z]||0)+1}}
 for(const r of RIVERS)if(!r.zona&&!(vistas[r.id]>=3&&vistas[r.id]<=14))throw 'nombres de relieve en '+r.id+': '+vistas[r.id];if(!(vistas.cr>=10))throw 'pocos nombres en cr';
 abrirRio('indo');let cp=document.querySelector('#capa').innerHTML;if((cp.match(/class="etq relieve/g)||[]).length<4)throw 'sin nombres de relieve en el mapa del Indo';if(cp.indexOf('Himalaya')<0)throw 'sin Himalaya';
 const rel=document.getElementById('relieve');if(!rel.innerHTML||rel.innerHTML.indexOf('class="a2000"')<0)throw 'sin franjas en la vista del río';
 const pf=document.getElementById('perfil');if(pf.hidden||pf.innerHTML.indexOf('<svg')<0||pf.innerHTML.indexOf('class="perfil-aqui"')<0)throw 'sin perfil';
 const xa=()=>+pf.innerHTML.match(/class="perfil-aqui" cx="([\d.]+)"/)[1];const xa0=xa();bajar(2);if(!(xa()>xa0))throw 'el marcador del perfil no avanza';
 if(document.querySelector('#panel').innerHTML.indexOf('m sobre el mar')<0)throw 'sin altura en la parada';
 abrirRio('sarapiqui');cp=document.querySelector('#capa').innerHTML;if(cp.indexOf('class="pico"')<0||cp.indexOf('Poás')<0)throw 'sin volcanes en la vista del Sarapiquí';if(rel.innerHTML.indexOf('class="a1500"')<0)throw 'sin franjas de cr';
 irInicio();if(rel.innerHTML!=='')throw 'franjas en el mundo';if(!pf.hidden)throw 'perfil visible en el inicio';
 verZona('cr');cp=document.querySelector('#capa').innerHTML;if(cp.indexOf('Talamanca')<0)throw 'sin cordilleras en la zona';verZona(null);
 let conAltura=0;for(const r of RIVERS){const q=preguntaTipo('altura',r);if(q.tipo!=='altura')continue;conAltura++;if(q.opciones.length!==4||new Set(q.opciones).size!==4||q.correcta<0)throw 'pregunta altura mala '+r.id;
   const alts=r.ciudades.map((c,i)=>alturaParada(r,i)),top=r.ciudades.findIndex(c=>esc(c.nombre)===q.opciones[q.correcta]);for(const o of q.opciones){const j=r.ciudades.findIndex(c=>esc(c.nombre)===o);if(j<0||(j!==top&&alts[j]>=alts[top]))throw 'altura: la respuesta no es la más alta '+r.id}}
 if(conAltura<RIVERS.length-3)throw 'pocas preguntas de altura: '+conAltura;
 console.log('relieve OK: nombres por vista',JSON.stringify(vistas),'preguntas de altura',conAltura)}
console.log('TODO OK');
},50);
