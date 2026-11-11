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
/* los fuentes se leen siempre con fines de línea LF, estén como estén en el disco: el recorte trabaja por renglones (limpiar, bloque,
   cortarEdicion, cortarVitrina) y con CRLF armaba otro HTML (renglones vacíos de más; con el motor en CRLF, un objeto sin cerrar),
   que la CI, que arma con LF, rechaza en «dist al día» aunque las pruebas pasen acá. finesDeLinea, en test/arnes.js, lo comprueba */
const src=p=>fs.readFileSync(path.join(__dirname,'src',p),'utf8').replace(/\r\n?/g,'\n');
const JUEGOS={
  cauces:{titulo:'Cauces: los grandes ríos, ciudad por ciudad',vocab:['rio'],archivos:['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/ilustraciones.js','data/mercados.js','data/eventos.js','data/voces.js','data/relieve.js','juegos/cauces.js','motor.js'],amplia:{'data/mapa.js':'data/mapa-amplia.js','data/relieve.js':'data/relieve-amplia.js'},soloAmplia:['data/barcas.js','data/bienes.js','data/postales.js']},
  nilo:{titulo:'Cauces · Nilo: la vitrina de un río',salida:'nilo.html',ediciones:['amplia'],tope:900,vitrina:true,soloRutas:['nilo'],estilos:['vitrina/capa.css','vitrina/arte.css','vitrina/carta.css','vitrina/panel.css'],vocab:['rio'],archivos:['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/ilustraciones.js','data/mercados.js','data/eventos.js','data/voces.js','data/relieve.js','juegos/nilo.js','vitrina/capa.js','vitrina/arte.js','vitrina/carta-datos.js','vitrina/mapa-carta.js','vitrina/carta.js','vitrina/panel.js','vitrina/sonido.js','motor.js'],amplia:{'data/mapa.js':'data/mapa-amplia.js','data/relieve.js':'data/relieve-amplia.js'},soloAmplia:['data/barcas.js','data/bienes.js','data/postales.js']},/* la vitrina (docs/vitrina/contrato.md): un solo río, una sola edición y la capa de src/vitrina/ antes del motor */
  exploradores:{titulo:'Exploradores: los grandes viajes, etapa por etapa',vocab:['itinerario','travesia'],archivos:['data/mapa-exploradores.js','data/itinerarios.js','data/ilustraciones.js','data/voces.js','data/relieve-exploradores.js','juegos/exploradores.js','motor.js'],soloAmplia:['data/barcas.js','data/bienes.js','data/postales.js']}
};
const EDICIONES={economica:{nombre:'económica',sufijo:'',tope:500},amplia:{nombre:'amplia',sufijo:'-amplia',tope:0}};
function archivosDe(id,edicion){const j=JUEGOS[id],rep=(edicion==='amplia'&&j.amplia)||{},mas=edicion==='amplia'&&j.soloAmplia||[];
  /* la vitrina: si su carta trae costas, lagos y fronteras propios (CARTA.tierra…), vitrina/mapa-carta.js los entrega como LAND, LAGOS y BORDES y el mapa del mundo no viaja */
  const mapaPropio=!!j.vitrina&&(()=>{try{return /["']?tierra["']?:\s*["'`]M/.test(src('vitrina/carta-datos.js'))}catch(e){return false}})();
  return j.archivos.filter(f=>!f.startsWith('vitrina/')||fs.existsSync(path.join(__dirname,'src',f))).filter(f=>mapaPropio?!/^data\/mapa/.test(f):f!=='vitrina/mapa-carta.js').flatMap(f=>[rep[f]||f].concat(f==='data/ilustraciones.js'?mas:[]))}// archivos del juego en una edición; `soloAmplia` (barcas y mercancías pintadas) entra tras las ilustraciones
const ABRE='/*@amplia*/',CIERRA='/*@fin:amplia*/';
/* la vitrina: los ganchos del motor van entre /*@vitrina*\/ y /*@fin:vitrina*\/; un juego con `vitrina` conserva el código y pierde las marcas, y los
   demás pierden el bloque entero (y su salto de línea, si el bloque ocupa renglones propios): quedan byte a byte como antes de los ganchos */
const VABRE='/*@'+'vitrina*/',VCIERRA='/*@fin:'+'vitrina*/';
function cortarVitrina(t,conservar){for(;;){const a=t.indexOf(VABRE);if(a<0)break;const b=t.indexOf(VCIERRA,a);if(b<0)throw 'marca '+VABRE+' sin cierre';const fin=b+VCIERRA.length;
    t=conservar?t.slice(0,a)+t.slice(a+VABRE.length,b)+t.slice(fin):t.slice(0,a)+t.slice(t[fin]==='\n'&&(a===0||t[a-1]==='\n')?fin+1:fin)}return t}
/* un juego con `soloRutas` se lleva de los datos solo sus rutas: dentro de RIVERS, NAVES, MASCOTAS, MERCADOS y EVENTOS, una entrada empieza en la
   línea que abre con el id de una ruta y llega hasta la siguiente */
function filtrarRutas(t,ids,todas){let dentro=false,deja=true;return t.split('\n').filter(l=>{if(/^const (RIVERS|NAVES|MASCOTAS|MERCADOS|EVENTOS)\b/.test(l)){dentro=true;deja=true;return true}
    if(!dentro)return true;if(/^[\]}];\s*$/.test(l)){dentro=false;return true}const k=l.match(/^\{id:"([a-z]+)"/)||l.match(/^([a-z]+):[\[{]/);if(k&&todas.has(k[1]))deja=ids.has(k[1]);return deja}).join('\n')}
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
  const il=new Set();for(const m of datos.matchAll(/glifo:["']([a-zñ]+)["'][^\n]*?(?:ilus:["']([a-zñ]+)["']|$)/gm))il.add(m[2]||m[1]);/* ilustraciones: la de cada compañero, su `ilus` si lo trae (en la misma línea) y si no su glifo; no las de animales de escena. Boto y Bulán tienen el glifo «delfin» pero su propia ilustración: la «delfin» es la de Nerea, en Exploradores */
  const ru=new Set();for(const m of datos.matchAll(/\bid:["']([a-z]+)["']/g))ru.add(m[1]);/* las rutas del juego: sus barcas y sus mercancías pintadas */
  return{glifos:g,pictos:p,tipos:t,iconos:i,ilus:il,rutas:ru}}
/* sin comentarios ni sangría: src los conserva; en dist pesan unos 9 KB en el motor y 1,4 KB en los datos (bloques y líneas de
   comentario, comentarios al final de línea y la sangría, que dentro de las plantillas HTML solo es espacio en blanco) */
const limpiar=m=>m.replace(/^[ \t]*\/\*[\s\S]*?\*\/[ \t]*\n?/gm,'').replace(/^[ \t]*\/\/[^\n]*\n/gm,'').replace(/[ \t]*\/\*[^\n]*?\*\/[ \t]*$/gm,'').replace(/^[ \t]+/gm,'').replace(/\n{2,}/g,'\n');
/* los trazos del mapa y del relieve (cadenas "M… L… Z") van en coordenadas absolutas en src, donde se leen y se comparan; en dist, en
   relativas: «l» con las diferencias, sin espacio antes de un negativo ni el cero de «0.5». Las diferencias salen de los valores ya
   redondeados, así que el dibujo es el mismo, y se comprueba al armar, punto por punto; quita un 39 % del peso de los trazos (≈ 60 KB en
   la económica de Cauces) */
function relativo(d){const t=d.match(/[MLZz]|-?\d*\.?\d+/g);if(!t||t.join('')!==d.replace(/[\s,]/g,''))return d;
  let dec=0;for(const s of t){const k=s.indexOf('.');if(k>=0)dec=Math.max(dec,s.length-k-1)}
  const F=10**dec,ent=s=>Math.round(parseFloat(s)*F),num=v=>{let s=(v/F).toFixed(dec);if(dec)s=s.replace(/\.?0+$/,'');return s.replace(/^(-?)0\./,'$1.')};
  let o='',x=0,y=0,sx=0,sy=0,c='',u='';const pts=[],pega=s=>{o+=(/[\d.]$/.test(o)&&/^[\d.]/.test(s)?' ':'')+s};
  for(let i=0;i<t.length;){const s=t[i];if(s==='M'||s==='L'){c=s;i++;continue}if(s==='Z'||s==='z'){o+='z';u='z';x=sx;y=sy;i++;continue}
    const X=ent(t[i]),Y=ent(t[i+1]);i+=2;pts.push(X,Y);if(c==='M'){o+='M';pega(num(X));pega(num(Y));u='';c='L';sx=X;sy=Y}else{if(u!=='l'){o+='l';u='l'}pega(num(X-x));pega(num(Y-y))}x=X;y=Y}
  const q=o.match(/[Mlz]|-?\d*\.?\d+/g),de=[];let a=0,b=0,ax=0,ay=0,k='';/* la prueba: el trazo relativo, leído de vuelta, da los mismos puntos */
  for(let i=0;i<q.length;){const s=q[i];if(s==='M'||s==='l'){k=s;i++;continue}if(s==='z'){a=ax;b=ay;i++;continue}
    const X=ent(q[i]),Y=ent(q[i+1]);i+=2;if(k==='M'){a=X;b=Y;ax=a;ay=b;k='l'}else{a+=X;b+=Y}de.push(a,b)}
  if(de.length!==pts.length||de.some((v,i)=>v!==pts[i]))throw 'un trazo relativo no reproduce el original: '+d.slice(0,60);
  return o}
const trazos=m=>m.replace(/"(M-?[\d.][\d. MLZz-]*)"/g,(x,d)=>'"'+relativo(d)+'"');
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
  const j=JUEGOS[id],e=EDICIONES[edicion],archivos=archivosDe(id,edicion),todas=j.soloRutas&&new Set([...src('data/rios.js').matchAll(/^\{id:"([a-z]+)"/gm)].map(m=>m[1]));
  const leer=f=>{let t=cortarVitrina(cortarEdicion(src(f),edicion),!!j.vitrina);if(j.soloRutas&&/^data\/(rios|naves|mascotas|mercados|eventos)\.js$/.test(f))t=filtrarRutas(t,new Set(j.soloRutas),todas);
    if(j.vitrina&&/^data\/relieve/.test(f))t=t.replace(/^const RELIEVE=.*$/m,'const RELIEVE={};');/* la vitrina trae su relieve sombreado: las franjas no viajan */return t};
  const datos=archivos.filter(f=>f!=='motor.js').map(leer).join('\n'),u=usados(datos),{motor,quitado}=recortar(leer('motor.js'),j,u);
  const titulo=j.titulo+(e.sufijo&&!j.salida?' · edición '+e.nombre:'');
  const estilos=(j.estilos||[]).filter(f=>fs.existsSync(path.join(__dirname,'src',f))).map(src).join('\n');/* el CSS de la capa, después del de cabeza.html */
  const ilustraciones=t=>t.split('\n').filter(l=>{const k=l.match(/^([a-zñ]+):\{v:/);if(!k||u.ilus.has(k[1]))return true;quitado.ilustraciones=(quitado.ilustraciones||0)+1;return false}).join('\n');/* ilustraciones (data/ilustraciones.js): solo las de los animales del juego */
  const porRuta=t=>t.split('\n').filter(l=>{const k=l.match(/^([a-z]+):[{[]/);return !k||u.rutas.has(k[1])}).join('\n');/* barcas, mercancías y postales: solo las de las rutas del juego */
  const guion=f=>f==='motor.js'?motor:f.startsWith('juegos/')?limpiar(leer(f))+`\nJUEGO.edicion={nombre:'${e.nombre}',kb:__PESO__};`:f==='data/ilustraciones.js'?ilustraciones(limpiar(leer(f))):f==='data/barcas.js'||f==='data/bienes.js'||f==='data/postales.js'?porRuta(limpiar(leer(f))):/^data\/(mapa|relieve)/.test(f)||f==='vitrina/carta-datos.js'?trazos(limpiar(leer(f))):limpiar(leer(f));
  const base=leer('cabeza.html').replace('<title>__TITULO__</title>',`<title>${titulo}</title>`).replace('content="__EDICION__"',`content="${e.nombre}"`).replace('</head>',()=>(estilos?'<style>\n'+estilos+'</style>\n':'')+'</head>')+archivos.map(f=>'<script>\n'+guion(f)+'</script>\n').join('')+leer('cola.html');
  /* el archivo dice cuánto pesa; el número entra en el mismo archivo, así que se comprueba después de escribirlo */
  let kb=Math.round(base.length/1024),html=base.replace('__PESO__',kb);const kb2=Math.round(html.length/1024);if(kb2!==kb){kb=kb2;html=base.replace('__PESO__',kb)}
  return{archivo:j.salida||id+e.sufijo+'.html',html,kb,quitado,tope:j.tope||e.tope}}
function construir(){
  fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
  const solo=process.argv[2];if(solo&&!JUEGOS[solo])throw 'uso: node build.js [juego]: '+Object.keys(JUEGOS).join(' | ');/* con un juego, solo ese: `node build.js nilo` */
  for(const id of Object.keys(JUEGOS).filter(k=>!solo||k===solo))for(const ed of JUEGOS[id].ediciones||Object.keys(EDICIONES)){const {archivo,html,kb,quitado,tope}=ensamblar(id,ed);
    fs.writeFileSync(path.join(__dirname,'dist',archivo),html);
    console.log(`dist/${archivo}`,kb,'KB','· recortado del motor:',`${quitado.vocab} vocabularios, ${quitado.animales} animales, ${quitado.pictos} pictogramas, ${quitado.glifos} glifos, ${quitado.iconos} iconos`);
    if(tope&&html.length>tope*1024)console.warn(`AVISO: dist/${archivo} pasa de ${tope} KB`)}}
module.exports={JUEGOS,EDICIONES,archivosDe,ensamblar,cortarEdicion,cortarVitrina};
if(require.main===module)construir();
