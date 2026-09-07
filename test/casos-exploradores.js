// Pruebas de Exploradores: datos de cada ruta (itinerarios y travesías), vocabulario por tipo (nada de río en pantalla),
// flujo completo de todas las rutas en los dos modos, carga, preguntas propias (fin, orden, fecha) y las que vuelven con
// cuatro rutas o más (viaje, frase, contexto), línea de tiempo (con años antes de Cristo), cámara por tramo, vehículo
// terrestre o flota en el mapa, grupos de viajeros y conquistadores, guardado con prefijo propio y relieve en la vista.
const bajar=k=>{for(let i=0;i<k;i++){paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}};
const sinNum=h=>h.replace(new RegExp('<span class="num">([^<]*)</span>','g'),'$1'),panel=()=>sinNum(document.querySelector('#panel').innerHTML+document.getElementById('pie').innerHTML),capa=()=>document.querySelector('#capa').innerHTML;
if(JUEGO.id!=='exploradores')throw 'juego equivocado';
if(RUTAS.length<4)throw 'con menos de cuatro rutas no vuelven las preguntas de viaje, frase y contexto';
const nombresParada=new Map();
for(const r of RUTAS){
  if(!['itinerario','travesia'].includes(r.tipo))throw r.id+' tipo raro '+r.tipo;
  for(const k of ['id','nombre','region','inicio','fin','contexto','frase','trazo','paradas','vehiculo','companero','carga'])if(r[k]==null)throw r.id+' falta '+k;
  if(r.contexto.length!==2||r.contexto.some(c=>!c.clave||!c.titulo||!c.texto||!c.pista))throw r.id+' contexto incompleto';
  if(r.paradas.length<4)throw r.id+' pocas etapas';
  const ini=[...r.frase.matchAll(/\[([^\]]+)\]/g)].map(m=>m[1].toUpperCase()),cini=r.paradas.map(c=>c.nombre[0].toUpperCase());if(ini.join('')!==cini.join(''))throw 'acróstico '+r.id+' '+ini.join('')+' vs '+cini.join('');
  const pictoOk=e=>!!PICTOS[e]||(e.startsWith('animal:')&&!!ANIMALES[e.slice(7)]);
  {const rs=r.paradas.map(c=>c.rumbo);if(rs.some(x=>!x)||new Set(rs).size!==rs.length)throw r.id+' rumbos: cada etapa lleva uno, todos distintos'}
  for(const c of r.paradas){for(const k of ['nombre','pais','pos','imagen','dato','escena','fecha','rumbo'])if(c[k]==null)throw r.id+' '+c.nombre+' falta '+k;if(c.imagen.length>260)console.log('imagen larga',c.nombre,c.imagen.length);for(const e of c.escena)if(!pictoOk(e))throw 'pictograma '+e+' en '+c.nombre;
    if(nombresParada.has(c.nombre)&&nombresParada.get(c.nombre)!==r.id)throw 'la parada '+c.nombre+' está en dos rutas: la pregunta «¿en qué viaje está…?» sería ambigua';nombresParada.set(c.nombre,r.id)}
  for(const e of r.inicio.escena.concat(r.fin.escena))if(!pictoOk(e))throw 'pictograma '+e;
  if(r.curso.length<40)throw r.id+' trazo demasiado simple';
  r.paradas.forEach((c,i)=>{const d=Math.hypot(r.curso[c.idx][0]-c.pos[0],r.curso[c.idx][1]-c.pos[1]);if(d>0.25)throw r.id+' '+c.nombre+' a '+d.toFixed(2)+'° del trazo';if(i&&c.idx<=r.paradas[i-1].idx)throw r.id+' '+c.nombre+' fuera de orden'});
  for(let i=1;i<r.curso.length;i++)if(hav(r.curso[i-1],r.curso[i])>230)throw r.id+' salto de '+Math.round(hav(r.curso[i-1],r.curso[i]))+' km';
  if(r.companero.paradas.length!==r.paradas.length)throw 'compañero '+r.id;if(!ANIMALES[r.companero.glifo])throw 'glifo del compañero '+r.companero.glifo;
  if(r.vehiculo.puertos.length!==r.paradas.length||r.paradas[r.paradas.length-1].carga!=='vendida')throw 'vehículo '+r.id;
  if(glifo(r.vehiculo.tipo)===glifo('otro-que-no-existe')&&r.vehiculo.tipo!=='cuadrada')throw 'vehículo sin glifo '+r.vehiculo.tipo;
  const n=r.paradas.length;for(let j=0;j<n-1;j++)if(!r.carga.some(g=>g.o===j))throw r.id+' etapa '+j+' sin nada que cambiar';
  for(const g of r.carga){if(g.o>=n-1)throw r.id+' bien ofrecido en la última etapa: '+g.n;if(g.m!=null&&g.m<=g.o)throw r.id+' bien que se paga mejor antes de comprarlo: '+g.n}
  for(const e of r.eventos){if(!(e.tramo>=1&&e.tramo<=n+1))throw 'tramo '+r.id;if(e.reto==='ruta'&&e.tramo>n-1)throw 'ruta tarde '+r.id;if(e.reto==='imagen'&&e.tramo<2)throw 'imagen temprano '+r.id}
  const T=tiposDisponibles(r);for(const t of ['imagen','pais','fin','orden','ciudad','frase','cruza',...r.contexto.map(c=>c.clave)])if(!T.includes(t))throw r.id+' sin el tipo '+t;if((masLejana(r)!=null)!==T.includes('lejos'))throw r.id+' lejos mal ofrecido';if(T.includes('cerca')||T.includes('siguiente'))throw r.id+' con preguntas de secuencia fina';
  if(r.tramos){const U=unidades(r);if(U[U.length-1].hasta!==r.paradas.length-1||U.some((u,i)=>u.desde>u.hasta||(i&&u.desde!==U[i-1].hasta+1)))throw r.id+' tramos mal cortados';const qo=preguntaTipo('orden',r);if(!qo.opciones[qo.correcta].split(' → ').every(nm=>r.tramos.some(t=>esc(t.nombre)===nm)))throw r.id+' orden por tramos: '+qo.opciones[qo.correcta]}
  for(const t of T){const q=preguntaTipo(t,r);const esp=q.tipo==='cerca'?3:4;if(q.opciones.length!==esp||new Set(q.opciones).size!==esp||q.correcta<0)throw 'pregunta mala '+t+' en '+r.id+' '+JSON.stringify(q.opciones)}
  const qc=preguntaTipo('ciudad',r);if(qc.opciones[qc.correcta]!==esc(r.nombre)||!qc.opciones.every(o=>RUTAS.some(x=>esc(x.nombre)===o)))throw 'pregunta de viaje '+qc.texto;
  const qf=preguntaTipo('fin',r);if(qf.opciones[qf.correcta]!==esc(r.fin.nombre))throw 'pregunta de fin '+qf.texto;
  const qo=preguntaTipo('orden',r);if(!qo.opciones.every(o=>o.split(' → ').length===4))throw 'pregunta de orden '+JSON.stringify(qo.opciones);
  {if(T.includes('lejos')){const ql=preguntaTipo('lejos',r);if(!r.paradas.some(c=>esc(c.nombre)===ql.opciones[ql.correcta]))throw 'lejos '+r.id}const qc=preguntaTipo('cruza',r);if(!r.cruza.includes(sinHtml(qc.opciones[qc.correcta]))||qc.opciones.filter(o=>r.cruza.includes(sinHtml(o))).length!==1)throw 'cruza '+r.id+' '+JSON.stringify(qc.opciones)}
  const qx=preguntaTipo(r.contexto[0].clave,r);if(qx.opciones[qx.correcta]!==esc(r.nombre)||qx.texto.indexOf(r.contexto[0].titulo)<0)throw 'pregunta de contexto '+qx.texto;
}
{const qd=preguntaTipo('fecha',rioPor('alejandro'));if(qd.tipo!=='fecha'||!/a\. C\./.test(qd.opciones[qd.correcta])||new Set(qd.opciones.map(anio)).size!==4)throw 'fecha antes de Cristo: '+JSON.stringify(qd.opciones);
 const qz=preguntaTipo('fecha',rioPor('zhenghe'));if(qz.tipo!=='fecha'||new Set(qz.opciones.map(anio)).size!==4)throw 'fechas repetidas por año: '+JSON.stringify(qz.opciones);
 if(preguntaTipo('fecha',rioPor('cortes')).tipo!=='cerca')throw 'Cortés tiene tres años: la pregunta de fecha debía caer a cerca';
 if(anio('334 a. C.')!==-334||anio('hacia 1332')!==1332||txtAnio(-323)!=='323 a. C.')throw 'años';
 const qd2=preguntaTipo('duracion',rioPor('ibnbattuta'));if(qd2.opciones[qd2.correcta]!=='29 años'||new Set(qd2.opciones).size!==4)throw 'duración de Ibn Battuta: '+JSON.stringify(qd2.opciones);
 const qp=preguntaTipo('primero',rioPor('marcopolo')),ini=nm=>anio(RUTAS.find(x=>esc(x.nombre)===nm).inicio.fecha),vals=qp.opciones.map(ini),esp=/último/.test(qp.texto)?Math.max(...vals):Math.min(...vals);if(ini(qp.opciones[qp.correcta])!==esp)throw 'primero: '+qp.texto+' '+JSON.stringify(qp.opciones);
 if(tiposDisponibles(rioPor('odiseo')).includes('duracion')||tiposDisponibles(rioPor('odiseo')).includes('primero'))throw 'Odiseo no tiene años: sin duración ni primero';
 if(!idsDe(rioPor('alejandro')).includes('ruta:alejandro:escala'))throw 'sin tarjeta de escala';
 if(!RUTAS.some(r=>r.conquista)||!RUTAS.some(r=>!r.conquista))throw 'grupos de viajeros y conquistadores'}
console.log('rutas',RUTAS.length,'etapas',RUTAS.reduce((a,r)=>a+r.paradas.length,0),'preguntas OK');
setTimeout(()=>{
const RIO=['Nacimiento','Desembocadura','Llegar al mar','Descender','el río pasa','próxima parada','Mercado de','la bodega','Zarpar a'];
const sinRio=(r,donde)=>{const t=panel(),lista=r.tipo==='travesia'?RIO.slice(0,6):RIO;for(const w of lista)if(t.indexOf(w)>=0)throw 'vocabulario de río en '+donde+': '+w};
for(const modo of ['mercader','historia']){crearPerfil('Prueba '+modo);setModo(modo);
  for(const r of RUTAS){const n=r.paradas.length,V=r.vocab,k=r.id+' '+modo;
    abrirRio(r.id);let ph=panel();if(ph.indexOf(V.inicio)<0||ph.indexOf(V.tuVehiculo)<0||ph.indexOf(esc(r.inicio.nombre))<0)throw k+': inicio sin vocabulario ('+V.inicio+', '+V.tuVehiculo+')';sinRio(r,'inicio '+k);
    if(audio.modo!==(V.sonidoTipo||'agua'))throw k+' sonido: '+audio.modo;
    const pf=document.getElementById('perfil'),conAnios=r.paradas.some(c=>anio(c.fecha)!=null);if(conAnios&&(pf.hidden||pf.innerHTML.indexOf('Línea de tiempo')<0))throw k+' sin línea de tiempo';if(!conAnios&&!pf.hidden)throw k+' franja sin años';if(r.id==='alejandro'&&pf.innerHTML.indexOf('334 a. C.')<0)throw 'línea de tiempo sin años antes de Cristo';
    let cp=capa();const tierra=!!TERRESTRES[r.vehiculo.tipo];if(tierra&&(cp.indexOf('class="barca tierra"')<0||cp.indexOf('class="anda"')<0||cp.indexOf('estela huellas')<0))throw k+' sin vehículo terrestre en el mapa';if(!tierra&&(cp.indexOf('class="barca"')<0||cp.indexOf('huellas')>=0))throw k+' sin flota en el mapa';if(cp.indexOf('class="animal"')<0)throw k+' sin animal';
    if(r.camara==='tramo'){const vbTramo=vbPara(ventana(r),20,1.3),vbToda=vbPara(r.curso.concat(r.paradas.map(c=>c.pos)),20,1.3);if(!(vbTramo.w<vbToda.w*0.7))throw k+' la cámara por tramo no acerca: '+vbTramo.w+' vs '+vbToda.w}
    const g0=S.guias[0];if(!g0)throw k+' sin guía';if(panel().indexOf(V.proxima)<0)throw k+' guía sin vocabulario';if(document.getElementById('pie').innerHTML.indexOf('>'+esc(r.paradas[g0.objetivo].rumbo)+'</button>')<0)throw k+' la guía debe mostrar rumbos';if(!lectura().some(x=>x.indexOf(r.paradas[g0.objetivo].rumbo)>=0))throw k+' la voz debe leer los rumbos';responderGuia(g0.objetivo);if(panel().indexOf(V.avanzar+' ')<0)throw k+' sin botón '+V.avanzar;
    let eventos=0;for(let p=0;p<=n;p++){paso(1);if(S.evento){eventos++;responderEvento(S.evento.q.correcta);continuarEvento()}
      ph=panel();if(S.paso<=n){const c=r.paradas[S.paso-1];if(sinHtml(ph).indexOf(`${V.Parada} ${S.paso} de ${n}`)<0||ph.indexOf(esc(c.fecha))<0)throw k+': kicker de la parada '+S.paso;sinRio(r,'parada '+S.paso+' '+k);
        if(modo==='mercader'&&S.paso<n&&ph.indexOf(V.mercado)<0)throw k+' sin '+V.mercado+' en '+c.nombre;if(modo==='historia'&&ph.indexOf(V.llevaba)<0)throw k+' sin carga en Historia '+c.nombre;
        if(modo==='mercader'&&S.paso===1){const gi=r.carga.findIndex(g=>g.o===0);comprar(gi);if(S.eco.bodega.length!==1||panel().indexOf(`${V.carga} 1 de 3`)<0)throw k+' compra'}
        const g=S.guias[S.paso];if(g)responderGuia(g.objetivo)}
      else{if(ph.indexOf(V.fin)<0||ph.indexOf('vuelve a '+esc(r.fin.en))<0&&ph.indexOf('termina en '+esc(r.fin.en))<0)throw k+': final mal: '+ph.slice(0,300)}}
    if(eventos!==r.eventos.length)throw k+' eventos vistos '+eventos+' de '+r.eventos.length;if(!P.vistos[r.id])throw k+' no visto';
    if(modo==='mercader'&&(!S.eco.cerrado||!S.eco.final))throw k+' sin cuentas finales';
    setTab('ordenar');const U=unidades(r);if(panel().indexOf(V.extremoInicio+'</span>')<0||panel().indexOf(V.extremoFin+'</span>')<0||panel().indexOf(r.tramos?V.tocaTramos(U.length):V.tocaEnOrden(n))<0)throw k+' ordenar sin vocabulario';if(r.tramos&&panel().indexOf(esc(r.tramos[0].nombre))<0)throw k+' ordenar sin tramos';for(let i=0;i<U.length;i++)tocarChip(i);if(!S.orden.listo||panel().indexOf(V.ordenBien)<0)throw k+' orden no listo';
    setTab('trazar');{const pie=document.getElementById('pie').innerHTML;if(pie.indexOf('>Trazar<')<0||pie.indexOf('Recitar')>=0)throw k+' el riel de un viaje lleva Trazar';if(capa().indexOf('trazarEn(')<0||capa().indexOf('class="rio activo resto"')>=0)throw k+' el mapa de Trazar debe tener etapas tocables y esconder el resto del camino';
      if(panel().indexOf(V.trazaPregunta(1,n,r.inicio.nombre))<0)throw k+' trazar sin pregunta';trazarEn(1);if(S.tra.errores!==1||panel().indexOf(V.trazaNo)<0)throw k+' error de trazar no contado';for(let i=0;i<n;i++)trazarEn(i);if(!S.tra.listo||panel().indexOf(V.trazaFin(n-1,n))<0)throw k+' trazar: '+sinHtml(panel()).slice(0,200);if(!etapasHechas(r).trazar)throw k+' trazar no marcado como hecho';
      if(document.getElementById('pie').innerHTML.indexOf('Preguntar ›')<0)throw k+' sin Preguntar tras trazar'}
    setTab('preguntar');if(S.quiz.qs.length!==6)throw k+' quiz de '+S.quiz.qs.length;for(let i=0;i<6;i++){const q=S.quiz.qs[S.quiz.i];responder(q.correcta);siguiente()}if(panel().indexOf('6 de 6')<0||panel().indexOf(V.dominas)<0)throw k+' resultado';
    if(!lectura().length)throw k+' sin lectura';
    verPasaporte();if(sellosDe(r)<n-2)throw k+' pocos sellos '+sellosDe(r);irInicio()}
  const ph=panel();if(ph.indexOf('Viajeros')<0||ph.indexOf('Conquistadores')<0||ph.indexOf('Tocá un viaje')<0)throw modo+' inicio sin grupos';if(ph.indexOf('Los viajes, en escala')<0||ph.indexOf('29 años')<0)throw modo+' inicio sin la comparación de viajes';
  iniciarReto();const tipos=new Set();for(let i=0;i<10;i++){const q=S.quiz.qs[S.quiz.i];tipos.add(q.tipo);responder(q.correcta);siguiente()}
  irInicio();const pend=colaHoy().length;iniciarRepaso();if(pend&&S.pantalla!=='quiz')throw 'repaso vacío con '+pend+' pendientes';if(S.pantalla==='quiz')for(const q of S.quiz.qs)if(!q)throw 'pregunta nula en el repaso';irInicio()}
// tarjetas y guardado propios del juego
const r=RUTAS[0],ids=idsDe(r);if(!ids.includes('ruta:'+r.id+':orden')||!ids.includes('ruta:'+r.id+':entonces')||!ids.includes('ruta:'+r.id+':fin'))throw 'tarjetas '+ids.join(',');
if(!Object.keys(LS).some(k=>k.startsWith('exploradores:')))throw 'guardado sin prefijo del juego';
if(progresoJSON().indexOf('"app":"exploradores"')<0)throw 'exportación sin el juego';
if(rango(300)!=='Gran Viajero')throw 'rangos del juego: '+rango(300);
// relieve y nombres en las vistas
for(const r of RUTAS){abrirRio(r.id);const rel=document.getElementById('relieve');if(!rel.innerHTML||rel.innerHTML.indexOf('<path')<0)throw r.id+' sin franjas de relieve';if(!NOMBRES_RELIEVE.some(L=>L.v&&L.v[r.id]))throw r.id+' sin nombres de relieve'}
irInicio();
console.log('TODO OK');
},50);
