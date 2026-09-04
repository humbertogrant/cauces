// Ensambla dist/cauces.html a partir de src/. Uso: node build.js
const fs=require('fs'),path=require('path');
const src=p=>fs.readFileSync(path.join(__dirname,'src',p),'utf8');
const orden=['data/mapa.js','data/rios.js','data/naves.js','data/mascotas.js','data/mercados.js','data/eventos.js','data/relieve.js','motor.js'];
const html=src('cabeza.html')+orden.map(f=>'<script>\n'+src(f)+'</script>\n').join('')+src('cola.html');
fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'dist','cauces.html'),html);
console.log('dist/cauces.html',(html.length/1024).toFixed(0),'KB');if(html.length>500*1024)console.warn('AVISO: dist/cauces.html pasa de 500 KB');
