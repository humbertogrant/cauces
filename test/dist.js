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
  if((edicion==='amplia')!==(typeof ILUSTRACIONES!=='undefined'))throw 'ILUSTRACIONES en la edición '+edicion;if(edicion==='amplia'&&juego==='cauces'&&!(ILUSTRACIONES.hipo&&(ILUSTRACIONES.hipo.d||ILUSTRACIONES.hipo.i)&&ILUSTRACIONES.hipo.c))throw 'sin ilustración del hipopótamo';if((edicion==='amplia')!==(typeof ilustracion==='function'))throw 'ilustracion en la edición '+edicion;
  /* la cara corresponde a la vista: de perfil, un solo ojo; ojo2 solo si la ilustración declara que se ve de frente o desde arriba; y su marco cuadrado para el retrato */
  /* cada ilustración es de vectores (`d`) o pintada (`i`: un WebP en base64, que el retrato envuelve con el filtro #aro) */
  if(edicion==='amplia')for(const [k,r] of Object.entries(ILUSTRACIONES)){if(!r.d===!r.i||(r.i&&!/^data:image\/webp;base64,[A-Za-z0-9+/]+=*$/.test(r.i)))throw 'ilustración sin cuerpo o con dos: '+k;if(r.i&&!/filter="url\(#aro\)"/.test(ilustracion({glifo:k},'normal','cabeza')))throw 'retrato pintado sin filo: '+k;}
  if(edicion==='amplia')for(const [k,r] of Object.entries(ILUSTRACIONES)){if(!r.c||!r.c.ojo||(r.c.ojo2&&!['frente','arriba'].includes(r.c.vista))||(r.c.vista&&!r.c.ojo2)||!r.c.marco||r.c.marco[2]!==r.c.marco[3])throw 'cara de la ilustración '+k;if(ilustracion({glifo:k},'normal','cabeza').indexOf(r.f||'<fondo>')>=0&&r.f)throw 'el retrato no lleva fondo: '+k}
  if(edicion==='amplia')for(const k of Object.keys(ILUSTRACIONES))if(!RUTAS.some(r=>(r.companero.ilus||r.companero.glifo)===k))throw 'ilustración sin animal en este juego: '+k;
  /* las barcas y las mercancías pintadas: solo en la amplia, solo las de las rutas del juego, un WebP cada una; la barca va en la lámina
     de «Tu embarcación» y cada bien, en el orden de la carga de su ruta */
  const webp=/^data:image\/webp;base64,[A-Za-z0-9+/]+=*$/;
  if((edicion==='amplia')!==(typeof BARCAS!=='undefined'&&typeof BIENES!=='undefined'&&typeof laminaNave==='function'))throw 'barcas y mercancías pintadas en la edición '+edicion;
  if(edicion==='amplia'){for(const [k,b] of Object.entries(BARCAS)){const r=rutaPor(k);if(!r||!r.vehiculo)throw 'barca pintada sin su ruta: '+k;if(!webp.test(b.i)||b.v.split(' ').length!==4)throw 'barca pintada sin imagen: '+k;if(!/barca-pintada/.test(laminaNave(r)))throw 'la lámina no lleva la barca: '+k}
    for(const [k,bs] of Object.entries(BIENES)){const r=rutaPor(k);if(!r||bs.length!==r.carga.length)throw 'mercancías pintadas que no calzan con la carga de '+k;bs.forEach((b,i)=>{if(b!==null&&!webp.test(b))throw 'mercancía pintada sin imagen: '+k+' '+i;if(b&&!/img class="bien"/.test(bienPintado(r,i)))throw 'el mercado no muestra la mercancía: '+k+' '+i})}}
  /* las postales pintadas: solo en la amplia; cada lista calza con el recorrido de su río (el nacimiento, las paradas y el mar) */
  if((edicion==='amplia')!==(typeof POSTALES!=='undefined'&&typeof postal==='function'))throw 'postales pintadas en la edición '+edicion;
  if(edicion==='amplia')for(const [k,ps] of Object.entries(POSTALES)){const r=rutaPor(k);if(!r||ps.length!==r.paradas.length+2)throw 'postales que no calzan con el recorrido de '+k;ps.forEach((p,i)=>{if(p!==null&&!webp.test(p))throw 'postal sin imagen: '+k+' '+i})}
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
  /* en el juego: bajando un río con postales pintadas, cada ficha (el nacimiento, cada parada y el mar) muestra la suya en lugar de la
     de pictogramas, y el reto de imagen también la lleva de pista */
  if(edicion==='amplia')for(const [k,ps] of Object.entries(POSTALES)){const rt=rutaPor(k),n=rt.paradas.length;abrirRio(k);
    for(let i=0;i<=n+1;i++){const ph=document.querySelector('#panel').innerHTML,pintada=ph.indexOf('<img class="escena pintada"')>=0;
      if(pintada!==!!ps[i]||pintada===(ph.indexOf('<svg class="escena"')>=0))throw 'postal de '+k+' en el lugar '+i;if(i<=n)bajar(1)}
    const q=preguntaTipo('imagen',rt,1);S.pantalla='rio';S.rio=k;setTab('preguntar');S.quiz.qs=[q];S.quiz.i=0;render();
    if(!!ps[2]!==(document.querySelector('#panel').innerHTML.indexOf('<img class="escena pintada quiz"')>=0))throw 'el reto de imagen de '+k+' sin su postal';irInicio()}
  console.log('DIST OK',juego,E.nombre,kb,'KB')
},50);
