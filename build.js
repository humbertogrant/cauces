// Ensambla un HTML por juego y por edición a partir de src/. Uso: node build.js
// Cada juego lleva sus datos, su archivo src/juegos/<id>.js (JUEGO) y el mismo motor; cabeza.html lleva el título como __TITULO__
// y la edición como __EDICION__ (una <meta name="edicion">). Hay dos ediciones del mismo código: la económica (dist/<id>.html,
// 500 KB o menos, la que se comparte) y la amplia (dist/<id>-amplia.html, sin tope). Lo que solo va en la amplia se envuelve en src
// con /*@amplia*/ … /*@fin:amplia*/ (JS o CSS: datos, juego, motor o cabeza); la económica recorta esos bloques y la amplia solo
// quita las marcas. Los archivos generados (mapa, relieve) no llevan marcas: la amplia tiene los suyos, más finos, y `amplia`
// en JUEGOS dice qué archivo reemplaza a cuál (archivosDe). Cada HTML dice qué es: la <meta name="edicion">, JUEGO.edicion
// {nombre, kb} (escrito tras src/juegos/<id>.js; en src no existe) y, en la amplia, el título con « · edición amplia».
// Para conservar peso, del motor se recorta lo que el juego no usa: los bloques de VOCAB de otros tipos de ruta (marcados
// con /*@vocab:tipo*/ … /*@fin:tipo*/), los animales, los pictogramas y los glifos de vehículo que no aparecen en sus datos.
// Las pruebas cargan src/ entero (es decir, la edición amplia); test/dist.js [juego] [edicion] comprueba que cada HTML recortado
// sigue jugando. Como módulo exporta JUEGOS, EDICIONES, ensamblar y cortarEdicion; construye solo si se corre directo.
const fs=require('fs'),path=require('path');
const src=p=>fs.readFileSync(path.join(__dirname,'src',p),'utf8');
const JUEGOS={
  cauces:{titulo:'Cauces: los grandes ríos, ciudad por ciudad',vocab:['rio'],archivos:['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/retratos.js','data/mercados.js','data/eventos.js','data/voces.js','data/relieve.js','juegos/cauces.js','motor.js'],amplia:{'data/mapa.js':'data/mapa-amplia.js','data/relieve.js':'data/relieve-amplia.js'}},
  exploradores:{titulo:'Exploradores: los grandes viajes, etapa por etapa',vocab:['itinerario','travesia'],archivos:['data/mapa-exploradores.js','data/itinerarios.js','data/retratos.js','data/voces.js','data/relieve-exploradores.js','juegos/exploradores.js','motor.js']}
};
const EDICIONES={economica:{nombre:'económica',sufijo:'',tope:500},amplia:{nombre:'amplia',sufijo:'-amplia',tope:0}};
function archivosDe(id,edicion){const j=JUEGOS[id],rep=(edicion==='amplia'&&j.amplia)||{};return j.archivos.map(f=>rep[f]||f)}// archivos del juego en una edición
const ABRE='/*@amplia*/',CIERRA='/*@fin:amplia*/';
function cortarEdicion(texto,edicion){// la económica quita los bloques marcados; la amplia, solo las marcas (y el salto de línea que las sigue)
  const tras=(t,i)=>t[i]==='\n'?i+1:i;
  if(edicion==='amplia'){let t=texto;for(const m of [ABRE,CIERRA])for(;;){const a=t.indexOf(m);if(a<0)break;t=t.slice(0,a)+t.slice(tras(t,a+m.length))}return t}
  let t=texto;for(;;){const a=t.indexOf(ABRE);if(a<0)break;const b=t.indexOf(CIERRA,a);if(b<0)throw 'marca '+ABRE+' sin cierre';t=t.slice(0,a)+t.slice(tras(t,b+CIERRA.length))}
  if(t.includes(CIERRA))throw 'marca '+CIERRA+' sin apertura';return t}
function usados(datos){/* claves que usan los datos del juego: glifos de animal, pictogramas de escena y tipos de vehículo */
  const g=new Set(),p=new Set(),t=new Set(['cuadrada']);
  for(const m of datos.matchAll(/glifo:["']([a-zñ]+)["']/g))g.add(m[1]);
  for(const m of datos.matchAll(/escena(?:Nace|Mar)?:\[([^\]]*)\]/g))for(const k of m[1].split(',')){const c=k.replace(/["' ]/g,'');if(!c)continue;if(c.startsWith('animal:'))g.add(c.slice(7));else p.add(c)}
  for(const m of datos.matchAll(/tipo:["']([a-z]+)["']/g))t.add(m[1]);
  const i=new Set();for(const m of datos.matchAll(/\b(?:i|icono):["']([a-z]+)["']/g))i.add(m[1]);/* iconos de bienes y eventos */
  for(const m of datos.matchAll(/icono:["']animal:([a-z]+)["']/g))g.add(m[1]);for(const m of datos.matchAll(/icono:["']barca:([a-z]+)["']/g))t.add(m[1]);
  return{glifos:g,pictos:p,tipos:t,iconos:i}}
/* sin comentarios ni sangría: src los conserva; en dist pesan unos 9 KB en el motor y 1,4 KB en los datos (bloques y líneas de
   comentario, comentarios al final de línea y la sangría, que dentro de las plantillas HTML solo es espacio en blanco) */
const limpiar=m=>m.replace(/^[ \t]*\/\*[\s\S]*?\*\/[ \t]*\n?/gm,'').replace(/^[ \t]*\/\/[^\n]*\n/gm,'').replace(/[ \t]*\/\*[^\n]*?\*\/[ \t]*$/gm,'').replace(/^[ \t]+/gm,'').replace(/\n{2,}/g,'\n');
function recortar(motor,j,u){
  let m=motor,quitado={vocab:0,animales:0,pictos:0,glifos:0,iconos:0};
  for(const tipo of ['rio','itinerario','travesia']){if(j.vocab.includes(tipo))continue;let hubo=false;for(;;){const a=m.indexOf(`/*@vocab:${tipo}*/`);if(a<0)break;const b=m.indexOf(`/*@fin:${tipo}*/`,a);if(b<0)throw 'sin cierre de VOCAB.'+tipo;m=m.slice(0,a)+m.slice(b+`/*@fin:${tipo}*/`.length);hubo=true}if(!hubo)throw 'sin marcas de VOCAB.'+tipo;quitado.vocab++}/* puede haber varios bloques por tipo: el vocabulario y las funciones propias de ese tipo de ruta */
  const bloque=(ini,fin,conservar,que)=>{const a=m.indexOf(ini),b=m.indexOf(fin,a);if(a<0||b<0)throw 'sin bloque '+ini;const lineas=m.slice(a,b).split('\n');
    const out=lineas.map(l=>{const k=l.match(/^([a-zñ]+):'/);if(!k||conservar.has(k[1]))return l;quitado[que]++;return l.endsWith('};')?'};':null}).filter(l=>l!==null);/* la última entrada cierra el objeto en su misma línea */m=m.slice(0,a)+out.join('\n')+m.slice(b)};
  const enMotor=new Set([...motor.matchAll(/picto\('([a-zñ]+)'\)/g)].map(x=>x[1]));/* pictogramas que el motor pide por nombre */
  bloque('const ANIMALES={','function animal(',u.glifos,'animales');
  bloque('const PICTOS={','function picto(',new Set([...u.pictos,...enMotor]),'pictos');
  const icoMotor=new Set([...motor.matchAll(/ico\('([a-z]+)'\)/g)].map(x=>x[1]));bloque('const ICONOS={','function ico(',new Set([...u.iconos,...icoMotor]),'iconos');
  m=limpiar(m);
  {const a=m.indexOf('function glifo('),b=m.indexOf('let animB',a);const lineas=m.slice(a,b).split('\n');
    const out=lineas.filter(l=>{const k=l.match(/^\s*case '([a-z]+)':/);if(!k||u.tipos.has(k[1]))return true;quitado.glifos++;return false});m=m.slice(0,a)+out.join('\n')+m.slice(b)}
  return{motor:m,quitado}}
function ensamblar(id,edicion){
  const j=JUEGOS[id],e=EDICIONES[edicion],archivos=archivosDe(id,edicion),leer=f=>cortarEdicion(src(f),edicion);
  const datos=archivos.filter(f=>f!=='motor.js').map(leer).join('\n'),u=usados(datos),{motor,quitado}=recortar(leer('motor.js'),j,u);
  const titulo=j.titulo+(e.sufijo?' · edición '+e.nombre:'');
  const retratos=t=>t.split('\n').filter(l=>{const k=l.match(/^([a-zñ]+):\{v:/);if(!k||u.glifos.has(k[1]))return true;quitado.retratos=(quitado.retratos||0)+1;return false}).join('\n');/* retratos «grabado» (data/retratos.js): solo los de los animales del juego */
  const guion=f=>f==='motor.js'?motor:f.startsWith('juegos/')?limpiar(leer(f))+`\nJUEGO.edicion={nombre:'${e.nombre}',kb:__PESO__};`:f==='data/retratos.js'?retratos(limpiar(leer(f))):limpiar(leer(f));
  const base=leer('cabeza.html').replace('<title>__TITULO__</title>',`<title>${titulo}</title>`).replace('content="__EDICION__"',`content="${e.nombre}"`)+archivos.map(f=>'<script>\n'+guion(f)+'</script>\n').join('')+leer('cola.html');
  /* el archivo dice cuánto pesa; el número entra en el mismo archivo, así que se comprueba después de escribirlo */
  let kb=Math.round(base.length/1024),html=base.replace('__PESO__',kb);const kb2=Math.round(html.length/1024);if(kb2!==kb){kb=kb2;html=base.replace('__PESO__',kb)}
  return{archivo:id+e.sufijo+'.html',html,kb,quitado,tope:e.tope}}
function construir(){
  fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
  for(const id of Object.keys(JUEGOS))for(const ed of Object.keys(EDICIONES)){const {archivo,html,kb,quitado,tope}=ensamblar(id,ed);
    fs.writeFileSync(path.join(__dirname,'dist',archivo),html);
    console.log(`dist/${archivo}`,kb,'KB','· recortado del motor:',`${quitado.vocab} vocabularios, ${quitado.animales} animales, ${quitado.pictos} pictogramas, ${quitado.glifos} glifos, ${quitado.iconos} iconos`);
    if(tope&&html.length>tope*1024)console.warn(`AVISO: dist/${archivo} pasa de ${tope} KB`)}}
module.exports={JUEGOS,EDICIONES,archivosDe,ensamblar,cortarEdicion};
if(require.main===module)construir();
