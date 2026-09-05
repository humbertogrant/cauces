// Prueba de humo del HTML ya ensamblado: carga los <script> de dist/<juego>.html en el DOM simulado y juega un poco.
// Comprueba que el recorte del motor (vocabularios, animales, pictogramas y glifos que el juego no usa) no rompió nada.
// Uso: node test/dist.js [cauces|exploradores]. Termina con "DIST OK".
const fs=require('fs'),path=require('path'),vm=require('vm');
const {montar}=require('./arnes');
const juego=process.argv[2]||'cauces';
montar([]);
const html=fs.readFileSync(path.join(__dirname,'..','dist',juego+'.html'),'utf8');
const scripts=[...html.matchAll(/<script>\n([\s\S]*?)<\/script>/g)].map(m=>m[1]);if(scripts.length<5)throw 'pocos scripts en dist/'+juego+'.html';
scripts.forEach((s,i)=>vm.runInThisContext(s,{filename:juego+'-script-'+i}));
setTimeout(()=>{
  if(JUEGO.id!==juego)throw 'juego '+JUEGO.id;
  for(const t of Object.keys(VOCAB))if(!(t==='rio'?juego==='cauces':juego==='exploradores'))throw 'VOCAB.'+t+' sobra en '+juego;
  for(const r of RUTAS){if(!r.vocab||!r.vocab.inicio)throw 'ruta sin vocabulario '+r.id;if(!ANIMALES[r.companero.glifo])throw 'animal recortado de más: '+r.companero.glifo;
    for(const c of r.paradas)for(const e of c.escena)if(!picto(e))throw 'pictograma recortado de más: '+e+' en '+c.nombre;
    for(const e of r.inicio.escena.concat(r.fin.escena))if(!picto(e))throw 'pictograma recortado de más: '+e;
    if(r.vehiculo&&glifo(r.vehiculo.tipo)===glifo('zzz')&&r.vehiculo.tipo!=='cuadrada')throw 'glifo recortado de más: '+r.vehiculo.tipo}
  crearPerfil('Dist');const r=RUTAS[0];abrirRio(r.id);
  const bajar=k=>{for(let i=0;i<k;i++){const g=S.guias[S.paso];if(g&&g.resp==null)responderGuia(g.objetivo);paso(1);if(S.evento){responderEvento(S.evento.q.correcta);continuarEvento()}}};
  bajar(r.paradas.length+1);if(!P.vistos[r.id])throw 'no llegó al final';
  const panel=document.querySelector('#panel').innerHTML;if(panel.indexOf(r.vocab.fin)<0)throw 'final sin vocabulario';
  setTab('ordenar');for(let i=0;i<r.paradas.length;i++)tocarChip(i);if(!S.orden.listo)throw 'orden';
  setTab('preguntar');for(let i=0;i<6;i++){responder(S.quiz.qs[S.quiz.i].correcta);siguiente()}
  irInicio();iniciarReto();for(let i=0;i<10;i++){responder(S.quiz.qs[S.quiz.i].correcta);siguiente()}
  if(document.querySelector('#capa').innerHTML.length<500)throw 'mapa vacío';
  console.log('DIST OK',juego,(html.length/1024).toFixed(0),'KB')
},50);
