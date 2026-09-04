// Pruebas de Exploradores: datos del itinerario, vocabulario de viaje (nada de río en pantalla), flujo completo en los dos
// modos, morral, preguntas propias de un juego con una sola ruta (fin, orden, fecha), línea de tiempo, cámara por tramo,
// caravana en el mapa, guardado con prefijo propio y relieve en la vista del viaje.
const bajar=k=>{for(let i=0;i<k;i++){paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}};
const panel=()=>document.querySelector('#panel').innerHTML,capa=()=>document.querySelector('#capa').innerHTML;
if(JUEGO.id!=='exploradores')throw 'juego equivocado';
if(!RUTAS.length)throw 'sin rutas';
for(const r of RUTAS){
  if(r.tipo!=='itinerario')throw r.id+' no es itinerario';
  for(const k of ['id','nombre','region','inicio','fin','contexto','frase','trazo','paradas','vehiculo','companero','carga'])if(r[k]==null)throw r.id+' falta '+k;
  if(r.contexto.length!==2||r.contexto.some(c=>!c.clave||!c.titulo||!c.texto||!c.pista))throw r.id+' contexto incompleto';
  if(r.paradas.length<4)throw r.id+' pocas etapas';
  const ini=[...r.frase.matchAll(/\[([^\]]+)\]/g)].map(m=>m[1].toUpperCase()),cini=r.paradas.map(c=>c.nombre[0].toUpperCase());if(ini.join('')!==cini.join(''))throw 'acróstico '+r.id+' '+ini.join('')+' vs '+cini.join('');
  const pictoOk=e=>!!PICTOS[e]||e.startsWith('animal:');
  for(const c of r.paradas){for(const k of ['nombre','pais','pos','imagen','dato','escena','fecha'])if(c[k]==null)throw r.id+' '+c.nombre+' falta '+k;if(c.imagen.length>260)console.log('imagen larga',c.nombre,c.imagen.length);for(const e of c.escena)if(!pictoOk(e))throw 'pictograma '+e}
  for(const e of r.inicio.escena.concat(r.fin.escena))if(!pictoOk(e))throw 'pictograma '+e;
  if(r.curso.length<40)throw r.id+' trazo demasiado simple';
  r.paradas.forEach((c,i)=>{const d=Math.hypot(r.curso[c.idx][0]-c.pos[0],r.curso[c.idx][1]-c.pos[1]);if(d>0.25)throw r.id+' '+c.nombre+' a '+d.toFixed(2)+'° del trazo';if(i&&c.idx<=r.paradas[i-1].idx)throw r.id+' '+c.nombre+' fuera de orden'});
  for(let i=1;i<r.curso.length;i++)if(hav(r.curso[i-1],r.curso[i])>230)throw r.id+' salto de '+Math.round(hav(r.curso[i-1],r.curso[i]))+' km';
  if(r.companero.paradas.length!==r.paradas.length)throw 'compañero '+r.id;if(!ANIMALES[r.companero.glifo])throw 'glifo del compañero '+r.companero.glifo;
  if(r.vehiculo.puertos.length!==r.paradas.length||r.paradas[r.paradas.length-1].carga!=='vendida')throw 'vehículo '+r.id;
  const n=r.paradas.length;for(let j=0;j<n-1;j++)if(!r.carga.some(g=>g.o===j))throw r.id+' etapa '+j+' sin nada que cambiar';
  for(const e of r.eventos){if(!(e.tramo>=1&&e.tramo<=n+1))throw 'tramo '+r.id;if(e.reto==='ruta'&&e.tramo>n-1)throw 'ruta tarde '+r.id}
}
console.log('itinerarios',RUTAS.length,'etapas',RUTAS.reduce((a,r)=>a+r.paradas.length,0));
// preguntas propias de un juego con una sola ruta
for(const r of RUTAS){const T=tiposDisponibles(r);for(const t of ['ciudad','frase','entonces','hoy'])if(T.includes(t))throw 'tipo sin distractores ofrecido: '+t;
  for(const t of ['imagen','siguiente','cerca','pais','fin','orden','fecha']){if(!T.includes(t))throw 'falta el tipo '+t;const q=preguntaTipo(t,r);const esp=q.tipo==='cerca'?3:4;if(q.opciones.length!==esp||new Set(q.opciones).size!==esp||q.correcta<0)throw 'pregunta mala '+t+' '+JSON.stringify(q.opciones)}
  const qf=preguntaTipo('fin',r);if(qf.opciones[qf.correcta]!==esc(r.fin.nombre)||qf.texto.indexOf('termina el viaje')<0)throw 'pregunta de fin '+qf.texto;
  const qo=preguntaTipo('orden',r);if(!qo.opciones.every(o=>o.split(' → ').length===4))throw 'pregunta de orden '+JSON.stringify(qo.opciones);
  const qd=preguntaTipo('fecha',r);if(!/\d{4}/.test(qd.opciones[qd.correcta])||qd.texto.indexOf('¿En qué año')<0)throw 'pregunta de fecha '+qd.texto;
  const qc=preguntaTipo('cerca',r);if(qc.texto.indexOf('final del viaje')<0)throw 'cerca sin vocabulario de viaje: '+qc.texto}
console.log('preguntas OK');
setTimeout(()=>{
const RIO=['Nacimiento','Desembocadura','Zarpar a','Llegar al mar','Mercado de','la bodega','Descender','el río pasa','próxima parada'];
const sinRio=donde=>{const t=panel();for(const w of RIO)if(t.indexOf(w)>=0)throw 'vocabulario de río en '+donde+': '+w};
const r=RUTAS[0],n=r.paradas.length;
for(const modo of ['mercader','historia']){crearPerfil('Prueba '+modo);setModo(modo);
  abrirRio(r.id);let ph=panel();if(ph.indexOf('Partida')<0||ph.indexOf('Tu caravana')<0||ph.indexOf(esc(r.inicio.nombre))<0)throw modo+': partida sin vocabulario de viaje';sinRio('partida '+modo);
  if(audio.modo!=='viento')throw 'sonido: '+audio.modo;
  const pf=document.getElementById('perfil');if(pf.hidden||pf.innerHTML.indexOf('Línea de tiempo')<0)throw 'sin línea de tiempo';
  let cp=capa();if(cp.indexOf('class="barca tierra"')<0||cp.indexOf('class="anda"')<0||cp.indexOf('estela huellas')<0)throw 'sin caravana en el mapa';if(cp.indexOf('class="animal"')<0)throw 'sin animal sobre la caravana';
  const vbTramo=vbPara(ventana(r),20,1.3),vbToda=vbPara(r.curso.concat(r.paradas.map(c=>c.pos)),20,1.3);if(!(vbTramo.w<vbToda.w*0.6))throw 'la cámara por tramo no acerca: '+vbTramo.w+' vs '+vbToda.w;
  const g0=S.guias[0];if(!g0)throw 'sin guía en la partida';if(panel().indexOf('próxima etapa')<0)throw 'guía sin vocabulario de viaje';responderGuia(g0.objetivo);if(panel().indexOf('Seguir a ')<0)throw 'sin botón Seguir a';
  if(!/Salimos hacia|Rumbo a|Yo también me acordaba/.test(S.dicho))throw 'voz de guía sin viaje: '+S.dicho;
  let eventos=0;for(let p=0;p<=n;p++){paso(1);if(S.evento){eventos++;const E=S.evento;if(!E.def.titulo)throw 'evento sin título';responderEvento(E.q.correcta);continuarEvento()}
    ph=panel();if(S.paso<=n){const c=r.paradas[S.paso-1];if(ph.indexOf(`Etapa ${S.paso} de ${n}`)<0||ph.indexOf(esc(c.fecha))<0)throw modo+': kicker de etapa '+S.paso;sinRio('etapa '+S.paso+' '+modo);
      if(modo==='mercader'&&S.paso<n&&ph.indexOf('Trueque en')<0)throw 'sin trueque en '+c.nombre;if(modo==='historia'&&ph.indexOf('El viajero llevaba')<0)throw 'sin carga en Historia '+c.nombre;
      if(modo==='mercader'&&S.paso===1){const gi=r.carga.findIndex(g=>g.o===0);comprar(gi);if(S.eco.bodega.length!==1||panel().indexOf('morral 1 de 3')<0)throw 'compra en el morral'}
      const g=S.guias[S.paso];if(g)responderGuia(g.objetivo)}
    else{if(ph.indexOf('Regreso')<0||ph.indexOf('vuelve a Fez')<0)throw modo+': regreso mal: '+ph.slice(0,300)}}
  if(eventos!==r.eventos.length)throw 'eventos vistos '+eventos+' de '+r.eventos.length;if(!P.vistos[r.id])throw 'no visto';
  if(modo==='mercader'&&(!S.eco.cerrado||!S.eco.final))throw 'morral sin cuentas finales';
  setTab('ordenar');if(panel().indexOf('Partida</span>')<0||panel().indexOf('Regreso</span>')<0||panel().indexOf('etapas en orden, de la partida al regreso')<0)throw 'ordenar sin vocabulario';for(let i=0;i<n;i++)tocarChip(i);if(!S.orden.listo||panel().indexOf('el camino ya es tuyo')<0)throw 'orden no listo';
  setTab('recitar');if(panel().indexOf('Etapa 1 de')<0)throw 'recitar sin vocabulario';for(let i=0;i<n;i++){revelar();recordada(true)}if(panel().indexOf(`${n} de ${n} recordadas`)<0)throw 'recitar';
  setTab('preguntar');if(S.quiz.qs.length!==6)throw 'quiz de '+S.quiz.qs.length;for(const q of S.quiz.qs)if(['ciudad','frase','entonces','hoy'].includes(q.tipo))throw 'tipo sin distractores en el quiz: '+q.tipo;
  for(let i=0;i<6;i++){const q=S.quiz.qs[S.quiz.i];responder(q.correcta);siguiente()}if(panel().indexOf('6 de 6')<0||panel().indexOf('Ya dominás este viaje')<0)throw 'resultado';
  if(!lectura().length)throw 'sin lectura';
  verPasaporte();if(panel().indexOf('viaje completo')<0&&panel().indexOf('viajes completos')<0)throw 'pasaporte sin vocabulario';if(sellosDe(r)<n-2)throw 'pocos sellos '+sellosDe(r);
  irInicio();if(panel().indexOf('Los grandes viajes')<0||panel().indexOf('Tocá un viaje')<0)throw 'inicio sin vocabulario';
  iniciarReto();for(let i=0;i<10;i++){const q=S.quiz.qs[S.quiz.i];if(['ciudad','frase','entonces','hoy'].includes(q.tipo))throw 'reto con tipo sin distractores '+q.tipo;responder(q.correcta);siguiente()}
  irInicio();iniciarRepaso();if(S.pantalla!=='quiz')throw 'repaso vacío';for(const q of S.quiz.qs)if(!q)throw 'pregunta nula en el repaso';
  irInicio()}
// tarjetas y guardado propios del juego
const ids=idsDe(r);if(!ids.includes('ruta:'+r.id+':orden')||!ids.includes('ruta:'+r.id+':entonces')||!ids.includes('ruta:'+r.id+':fin'))throw 'tarjetas '+ids.join(',');
if(!Object.keys(LS).some(k=>k.startsWith('exploradores:')))throw 'guardado sin prefijo del juego';
if(progresoJSON().indexOf('"app":"exploradores"')<0)throw 'exportación sin el juego';
if(rango(300)!=='Gran Viajero')throw 'rangos del juego: '+rango(300);
// relieve y nombres en la vista del viaje
abrirRio(r.id);const rel=document.getElementById('relieve');if(!rel.innerHTML||rel.innerHTML.indexOf('<path')<0)throw 'sin franjas de relieve';if((capa().match(/class="etq relieve/g)||[]).length<1)throw 'sin nombres de relieve';
irInicio();
console.log('TODO OK');
},50);
