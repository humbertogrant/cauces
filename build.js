// Ensambla un HTML por juego a partir de src/. Uso: node build.js
// Cada juego lleva sus datos, su archivo src/juegos/<id>.js (JUEGO) y el mismo motor; cabeza.html lleva el título como __TITULO__.
const fs=require('fs'),path=require('path');
const src=p=>fs.readFileSync(path.join(__dirname,'src',p),'utf8');
const JUEGOS={
  cauces:{titulo:'Cauces: los grandes ríos, ciudad por ciudad',archivos:['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/mercados.js','data/eventos.js','data/voces.js','data/relieve.js','juegos/cauces.js','motor.js']}
};
fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
for(const [id,j] of Object.entries(JUEGOS)){
  const html=src('cabeza.html').replace('<title>__TITULO__</title>',`<title>${j.titulo}</title>`)+j.archivos.map(f=>'<script>\n'+src(f)+'</script>\n').join('')+src('cola.html');
  fs.writeFileSync(path.join(__dirname,'dist',id+'.html'),html);
  console.log(`dist/${id}.html`,(html.length/1024).toFixed(0),'KB');if(html.length>500*1024)console.warn(`AVISO: dist/${id}.html pasa de 500 KB`)}
