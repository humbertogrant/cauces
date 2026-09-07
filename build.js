// Ensambla un HTML por juego a partir de src/. Uso: node build.js
// Cada juego lleva sus datos, su archivo src/juegos/<id>.js (JUEGO) y el mismo motor; cabeza.html lleva el título como __TITULO__.
// Para conservar peso, del motor se recorta lo que el juego no usa: los bloques de VOCAB de otros tipos de ruta (marcados
// con /*@vocab:tipo*/ … /*@fin:tipo*/), los animales, los pictogramas y los glifos de vehículo que no aparecen en sus datos.
// Las pruebas cargan src/ entero; test/dist.js comprueba que el HTML recortado sigue jugando.
const fs=require('fs'),path=require('path');
const src=p=>fs.readFileSync(path.join(__dirname,'src',p),'utf8');
const JUEGOS={
  cauces:{titulo:'Cauces: los grandes ríos, ciudad por ciudad',vocab:['rio'],archivos:['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/mercados.js','data/eventos.js','data/voces.js','data/relieve.js','juegos/cauces.js','motor.js']},
  exploradores:{titulo:'Exploradores: los grandes viajes, etapa por etapa',vocab:['itinerario','travesia'],archivos:['data/mapa-exploradores.js','data/itinerarios.js','data/voces.js','data/relieve-exploradores.js','juegos/exploradores.js','motor.js']}
};
function usados(datos){/* claves que usan los datos del juego: glifos de animal, pictogramas de escena y tipos de vehículo */
  const g=new Set(),p=new Set(),t=new Set(['cuadrada']);
  for(const m of datos.matchAll(/glifo:["']([a-zñ]+)["']/g))g.add(m[1]);
  for(const m of datos.matchAll(/escena(?:Nace|Mar)?:\[([^\]]*)\]/g))for(const k of m[1].split(',')){const c=k.replace(/["' ]/g,'');if(!c)continue;if(c.startsWith('animal:'))g.add(c.slice(7));else p.add(c)}
  for(const m of datos.matchAll(/tipo:["']([a-z]+)["']/g))t.add(m[1]);
  const i=new Set();for(const m of datos.matchAll(/\b(?:i|icono):["']([a-z]+)["']/g))i.add(m[1]);/* iconos de bienes y eventos */
  for(const m of datos.matchAll(/icono:["']animal:([a-z]+)["']/g))g.add(m[1]);for(const m of datos.matchAll(/icono:["']barca:([a-z]+)["']/g))t.add(m[1]);
  return{glifos:g,pictos:p,tipos:t,iconos:i}}
function recortar(motor,j,u){
  let m=motor,quitado={vocab:0,animales:0,pictos:0,glifos:0,iconos:0};
  for(const tipo of ['rio','itinerario','travesia']){if(j.vocab.includes(tipo))continue;const a=m.indexOf(`/*@vocab:${tipo}*/`),b=m.indexOf(`/*@fin:${tipo}*/`);if(a<0||b<0)throw 'sin marcas de VOCAB.'+tipo;m=m.slice(0,a)+m.slice(b+`/*@fin:${tipo}*/`.length);quitado.vocab++}
  const bloque=(ini,fin,conservar,que)=>{const a=m.indexOf(ini),b=m.indexOf(fin,a);if(a<0||b<0)throw 'sin bloque '+ini;const lineas=m.slice(a,b).split('\n');
    const out=lineas.map(l=>{const k=l.match(/^([a-zñ]+):'/);if(!k||conservar.has(k[1]))return l;quitado[que]++;return l.endsWith('};')?'};':null}).filter(l=>l!==null);/* la última entrada cierra el objeto en su misma línea */m=m.slice(0,a)+out.join('\n')+m.slice(b)};
  const enMotor=new Set([...motor.matchAll(/picto\('([a-zñ]+)'\)/g)].map(x=>x[1]));/* pictogramas que el motor pide por nombre */
  bloque('const ANIMALES={','function animal(',u.glifos,'animales');
  bloque('const PICTOS={','function picto(',new Set([...u.pictos,...enMotor]),'pictos');
  const icoMotor=new Set([...motor.matchAll(/ico\('([a-z]+)'\)/g)].map(x=>x[1]));bloque('const ICONOS={','function ico(',new Set([...u.iconos,...icoMotor]),'iconos');
  {const a=m.indexOf('function glifo('),b=m.indexOf('let animB',a);const lineas=m.slice(a,b).split('\n');
    const out=lineas.filter(l=>{const k=l.match(/^\s*case '([a-z]+)':/);if(!k||u.tipos.has(k[1]))return true;quitado.glifos++;return false});m=m.slice(0,a)+out.join('\n')+m.slice(b)}
  return{motor:m,quitado}}
fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
for(const [id,j] of Object.entries(JUEGOS)){
  const datos=j.archivos.filter(f=>f!=='motor.js').map(src).join('\n'),u=usados(datos),{motor,quitado}=recortar(src('motor.js'),j,u);
  const html=src('cabeza.html').replace('<title>__TITULO__</title>',`<title>${j.titulo}</title>`)+j.archivos.map(f=>'<script>\n'+(f==='motor.js'?motor:src(f))+'</script>\n').join('')+src('cola.html');
  fs.writeFileSync(path.join(__dirname,'dist',id+'.html'),html);
  console.log(`dist/${id}.html`,(html.length/1024).toFixed(0),'KB','· recortado del motor:',`${quitado.vocab} vocabularios, ${quitado.animales} animales, ${quitado.pictos} pictogramas, ${quitado.glifos} glifos, ${quitado.iconos} iconos`);if(html.length>500*1024)console.warn(`AVISO: dist/${id}.html pasa de 500 KB`)}
