// Prueba de humo del HTML ya ensamblado: carga los <script> de dist/<juego><sufijo>.html en el DOM simulado y juega un poco.
// Comprueba que el recorte del motor (vocabularios, animales, pictogramas y glifos que el juego no usa) no rompió nada, y que
// cada edición dice lo que es (meta, JUEGO.edicion, título, línea en «¿Cómo se juega?») y no arrastra marcas de edición.
// Uso: node test/dist.js [cauces|exploradores] [economica|amplia]. Termina con "DIST OK".
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar}=require('./arnes'),{JUEGOS,EDICIONES,cortarEdicion}=require('../build.js');
const juego=process.argv[2]||'cauces',edicion=process.argv[3]||'economica';
if(!JUEGOS[juego]||!EDICIONES[edicion])throw 'uso: node test/dist.js [cauces|exploradores] [economica|amplia]';
const E=EDICIONES[edicion],archivo=juego+E.sufijo+'.html';
/* el corte por edición: la económica quita los bloques marcados, la amplia solo las marcas, y una marca sin cierre es un error */
if(cortarEdicion('a,/*@amplia*/b,/*@fin:amplia*/c;/*@amplia*/d/*@fin:amplia*/','economica')!=='a,c;')throw 'corte económico';
if(cortarEdicion('a,/*@amplia*/b,/*@fin:amplia*/c','amplia')!=='a,b,c')throw 'corte amplio';
{let fallo=false;try{cortarEdicion('/*@amplia*/x','economica')}catch(e){fallo=true}if(!fallo)throw 'una marca sin cierre debía fallar'}
montar([]);
const html=fs.readFileSync(path.join(__dirname,'..','dist',archivo),'utf8');
if(html.includes('/*@amplia*/')||html.includes('/*@fin:amplia*/')||html.includes('__EDICION__')||html.includes('__PESO__'))throw 'marcas de edición en dist/'+archivo;
if(!html.includes(`<meta name="edicion" content="${E.nombre}">`))throw 'sin meta de edición en dist/'+archivo;
const titulo=JUEGOS[juego].titulo+(E.sufijo?' · edición '+E.nombre:'');if(!html.includes(`<title>${titulo}</title>`))throw 'título de la edición en dist/'+archivo;
const scripts=[...html.matchAll(/<script>\n([\s\S]*?)<\/script>/g)].map(m=>m[1]);if(scripts.length<5)throw 'pocos scripts en dist/'+archivo;
scripts.forEach((s,i)=>vm.runInThisContext(s,{filename:archivo+'-script-'+i}));
setTimeout(()=>{
  if(JUEGO.id!==juego)throw 'juego '+JUEGO.id;
  if(juego==='cauces'&&(edicion==='amplia')!==!!rutaPor('orinoco'))throw 'ríos de la amplia en la edición '+edicion;
  if((edicion==='amplia')!==(typeof RETRATOS!=='undefined'))throw 'RETRATOS en la edición '+edicion;if(edicion==='amplia'&&juego==='cauces'&&!(RETRATOS.hipo&&RETRATOS.hipo.o&&RETRATOS.hipo.s&&RETRATOS.hipo.c))throw 'sin retrato completo del hipopótamo';if((edicion==='amplia')!==(typeof personaje==='function'))throw 'personaje en la edición '+edicion;
  if(edicion==='amplia')for(const k of Object.keys(RETRATOS))if(!RUTAS.some(r=>r.companero.glifo===k))throw 'retrato sin animal en este juego: '+k;
  const kb=Math.round(html.length/1024);if(!JUEGO.edicion||JUEGO.edicion.nombre!==E.nombre||JUEGO.edicion.kb!==kb)throw 'JUEGO.edicion '+JSON.stringify(JUEGO.edicion)+' en un archivo de '+kb+' KB';
  for(const t of Object.keys(VOCAB))if(!(t==='rio'?juego==='cauces':juego==='exploradores'))throw 'VOCAB.'+t+' sobra en '+juego;
  for(const r of RUTAS){if(!r.vocab||!r.vocab.inicio)throw 'ruta sin vocabulario '+r.id;if(!ANIMALES[r.companero.glifo])throw 'animal recortado de más: '+r.companero.glifo;
    for(const c of r.paradas)for(const e of c.escena)if(!picto(e))throw 'pictograma recortado de más: '+e+' en '+c.nombre;
    for(const e of r.inicio.escena.concat(r.fin.escena))if(!picto(e))throw 'pictograma recortado de más: '+e;
    if(r.vehiculo&&glifo(r.vehiculo.tipo)===glifo('zzz')&&r.vehiculo.tipo!=='cuadrada')throw 'glifo recortado de más: '+r.vehiculo.tipo}
  crearPerfil('Dist');
  {const p=document.querySelector('#panel').innerHTML;if(p.indexOf('Edición '+E.nombre)<0||p.indexOf(kb+' KB')<0)throw 'la portada no dice la edición'}
  const r=RUTAS[0];abrirRio(r.id);
  const bajar=k=>{for(let i=0;i<k;i++){const g=S.guias[S.paso];if(g&&g.resp==null)responderGuia(g.objetivo);paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}};
  bajar(r.paradas.length+1);if(!P.vistos[r.id])throw 'no llegó al final';
  const panel=document.querySelector('#panel').innerHTML;if(panel.indexOf(r.vocab.fin)<0)throw 'final sin vocabulario';
  setTab('ordenar');for(let i=0;i<r.paradas.length;i++)tocarChip(i);if(!S.orden.listo)throw 'orden';
  setTab('preguntar');for(let i=0;i<6;i++){responder(S.quiz.qs[S.quiz.i].correcta);siguiente()}
  irInicio();iniciarReto();for(let i=0;i<10;i++){responder(S.quiz.qs[S.quiz.i].correcta);siguiente()}
  if(document.querySelector('#capa').innerHTML.length<500)throw 'mapa vacío';
  console.log('DIST OK',juego,E.nombre,kb,'KB')
},50);
