/* Carta de la vitrina del Nilo: relieve sombreado, retícula, rótulos de atlas, la próxima parada y los encuadres.
   Se carga antes que el motor: acá arriba solo se definen funciones y se registran en CAPA. Todo acceso al DOM va con guardas
   (las pruebas usan un DOM simulado sin createElementNS ni insertAdjacentHTML): si algo falta, la carta del motor queda como está. */
(function(){
if(typeof CAPA==='undefined'||typeof CARTA==='undefined')return;
const NS='http://www.w3.org/2000/svg';
const pr=p=>[(p[1]+180)/360*1000,(90-p[0])/180*500];           /* la proyección del motor */
const txt=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const ANCHO_LETRA={agua:8.2,pais:10.2,'rio-n':6.2,linea:9.2,hito:5.9};   /* px por letra a 11 px, con su espaciado */
const paso=()=>typeof S!=='undefined'&&S?S.paso|0:0;
const idx=(r,p)=>{const n=r.paradas.length;return p<=0?0:p>n?r.curso.length-1:r.paradas[p-1].idx};

/* el relieve: una sola vez, después de #relieve y antes de #lagos, recortado por la tierra */
function fondo(){const svg=document.getElementById('svg'),lagos=document.getElementById('lagos');
  if(!svg||!lagos||!svg.insertBefore||!document.createElementNS||lagos.parentNode!==svg||document.getElementById('v-fondo'))return;
  const L=CARTA.luz,a=pr([L.caja[0],L.caja[1]]),b=pr([L.caja[2],L.caja[3]]),g=document.createElementNS(NS,'g');
  g.setAttribute('id','v-fondo');g.setAttribute('aria-hidden','true');
  g.innerHTML=`<clipPath id="v-recorte"><use href="#tierra" clip-rule="evenodd"/></clipPath><image href="${L.src}" x="${a[0].toFixed(2)}" y="${a[1].toFixed(2)}" width="${(b[0]-a[0]).toFixed(2)}" height="${(b[1]-a[1]).toFixed(2)}" preserveAspectRatio="none" clip-path="url(#v-recorte)"/>`;
  svg.insertBefore(g,lagos)}

/* un grupo dentro de #capa (el motor la vuelve a escribir en cada render, así que se vuelve a poner cada vez) */
function grupo(capa,id,html,antes){const g=document.createElementNS(NS,'g');g.setAttribute('id',id);g.setAttribute('aria-hidden','true');g.innerHTML=html;capa.insertBefore(g,antes||null)}

function dibujar(foco,vb,px){const capa=document.getElementById('capa');
  if(!capa||!capa.insertBefore||!capa.querySelector||!document.createElementNS||!foco||foco.modo!=='rio'||!foco.rio||foco.rio.id!==CAPA.rio)return;
  const r=foco.rio,f=v=>(v*px).toFixed(2),n=r.paradas.length,ancho=px*390,M=4*px,momento=typeof CAPA.momento==='function'?CAPA.momento():'';
  const dentro=q=>q[0]>vb.x&&q[0]<vb.x+vb.w&&q[1]>vb.y&&q[1]<vb.y+vb.h;

  /* el resplandor del hilo de oro: dos copias anchas y transparentes debajo de lo recorrido */
  if(capa.querySelectorAll)capa.querySelectorAll('path.rio.activo').forEach(p=>{if(!p.classList||p.classList.contains('brazo')||(p.classList.contains('resto')&&momento!=='portada')||!p.cloneNode||!p.parentNode)return;/* los afluentes nunca; lo que falta, solo en la portada, donde el río entero es el hilo de oro */
    ['a','b'].forEach(c=>{const k=p.cloneNode(false);k.setAttribute('class','v-brillo '+c);k.removeAttribute('stroke-width');p.parentNode.insertBefore(k,p)})});

  /* líneas de fondo: retícula cada 5°, ecuador y trópico */
  const R=CARTA.reticula,a=pr([R.lat[1],R.lon[0]]),b=pr([R.lat[0],R.lon[1]]);let L='';
  for(let la=R.lat[0];la<=R.lat[1];la+=R.paso)if(!CARTA.lineas.some(l=>l.lat===la))L+=`<path class="v-ret" d="M${a[0].toFixed(2)} ${pr([la,0])[1].toFixed(2)}H${b[0].toFixed(2)}"/>`;
  for(let lo=R.lon[0];lo<=R.lon[1];lo+=R.paso)L+=`<path class="v-ret" d="M${pr([0,lo])[0].toFixed(2)} ${a[1].toFixed(2)}V${b[1].toFixed(2)}"/>`;
  CARTA.lineas.forEach(l=>{L+=`<path class="v-par" d="M${a[0].toFixed(2)} ${pr([l.lat,0])[1].toFixed(2)}H${b[0].toFixed(2)}"/>`});
  grupo(capa,'v-lineas',L,capa.firstChild);

  /* lo que un rótulo no puede pisar: el río (muestras cada 3 px del cauce a la vista), las paradas y sus nombres, la barca */
  const rio=[],puestos=[{x0:vb.x,x1:vb.x+64*px,y0:vb.y,y1:vb.y+64*px},{x0:vb.x+vb.w-64*px,x1:vb.x+vb.w,y0:vb.y,y1:vb.y+64*px}];/* las esquinas de arriba (64 × 64 px) son de los botones redondos: volver y sonido */
  for(let i=0;i+1<r.curso.length;i++){const p=pr(r.curso[i]),q=pr(r.curso[i+1]);
    if(Math.max(p[0],q[0])<vb.x-vb.w*.2||Math.min(p[0],q[0])>vb.x+vb.w*1.2||Math.max(p[1],q[1])<vb.y-vb.h*.2||Math.min(p[1],q[1])>vb.y+vb.h*1.2)continue;
    const m=Math.min(400,Math.max(1,Math.ceil(Math.hypot(q[0]-p[0],q[1]-p[1])/(3*px))));for(let k=0;k<=m;k++)rio.push([p[0]+(q[0]-p[0])*k/m,p[1]+(q[1]-p[1])*k/m])}
  const prox=typeof S!=='undefined'&&S&&S.pantalla==='rio'&&S.tab==='descender'&&momento!=='portada'&&paso()<n?paso():-1;/* en la portada no hay pregunta todavía */
  /* la barca tapa la primera letra del nombre de la parada donde está: ese nombre se corre hacia afuera */
  const B=foco.barca,qb=B?pr(B.poly?B.poly[B.t1>=B.t0?B.poly.length-1:0]:r.curso[B.a]):null;
  if(qb&&capa.querySelectorAll)r.paradas.forEach((c,i)=>{const q=pr(c.pos);if(!foco.etiquetas||!foco.etiquetas.has(i)||Math.hypot(q[0]-qb[0],q[1]-qb[1])>10*px)return;
    capa.querySelectorAll('text.etq').forEach(t=>{if(!t.getAttribute||!t.classList||t.classList.contains('relieve')||t.textContent!==c.nombre)return;const x=parseFloat(t.getAttribute('x')),fin=t.getAttribute('text-anchor')==='end';if(isFinite(x))t.setAttribute('x',(x+(fin?-16:14)*px).toFixed(2))})});
  r.paradas.forEach((c,i)=>{const q=pr(c.pos),d=(i===prox?15:7)*px;puestos.push({x0:q[0]-d,x1:q[0]+d,y0:q[1]-d,y1:q[1]+d})});
  /* los nombres que puso el motor (las paradas alcanzadas), cada uno con su caja de verdad */
  if(capa.querySelectorAll)capa.querySelectorAll('text.etq').forEach(t=>{if(!t.getAttribute||!t.classList||t.classList.contains('relieve'))return;
    const x=parseFloat(t.getAttribute('x')),y=parseFloat(t.getAttribute('y')),w=((t.textContent||'').length*9.2+4)*px,an=t.getAttribute('text-anchor');if(!isFinite(x)||!isFinite(y))return;
    const x0=an==='end'?x-w:an==='middle'?x-w/2:x;puestos.push({x0,x1:x0+w,y0:y-13*px,y1:y+4*px})});
  if(qb)puestos.push({x0:qb[0]-24*px,x1:qb[0]+22*px,y0:qb[1]-32*px,y1:qb[1]+14*px});
  const libre=c=>c.x0>vb.x+M&&c.x1<vb.x+vb.w-M&&c.y0>vb.y+M&&c.y1<vb.y+vb.h-26*px&&!puestos.some(o=>c.x0<o.x1+M&&c.x1>o.x0-M&&c.y0<o.y1+M&&c.y1>o.y0-M)&&!rio.some(p=>p[0]>c.x0-M&&p[0]<c.x1+M&&p[1]>c.y0-M&&p[1]<c.y1+M);
  /* la caja de un rótulo de 11 px (renglones partidos con |), con su ancla y su giro */
  const caja=(t,x,y,anc,cls,giro)=>{const rs=t.split('|'),w=Math.max.apply(null,rs.map(s=>s.length))*ANCHO_LETRA[cls]*px,h=(13+(rs.length-1)*15)*px;
    if(giro){const g=giro*Math.PI/180,c=Math.abs(Math.cos(g)),s=Math.abs(Math.sin(g)),bw=c*w+s*h,bh=s*w+c*h;return{x0:x-bw/2,x1:x+bw/2,y0:y-bh/2,y1:y+bh/2}}
    const x0=anc==='end'?x-w:anc==='middle'?x-w/2:x;return{x0,x1:x0+w,y0:y-10*px,y1:y-10*px+h}};
  const texto=(t,x,y,anc,cls,giro)=>{const rs=t.split('|'),X=x.toFixed(2),Y=y.toFixed(2);
    return`<text class="v-rot ${cls}" x="${X}" y="${Y}" font-size="${f(11)}" text-anchor="${anc}"${giro?` transform="rotate(${giro} ${X} ${Y})"`:''}>${rs.length>1?rs.map((s,i)=>`<tspan x="${X}" dy="${i?f(15):0}">${txt(s)}</tspan>`).join(''):txt(t)}</text>`};
  let H='';

  /* la próxima parada: anillo punteado con un signo de pregunta, sin nombre (memoria primero) */
  if(prox>=0){const p0=pr(r.paradas[prox].pos);let q=p0;
    /* si la parada queda a menos de 24 px de la barca (Jinja, a un paso del nacimiento), el anillo se corre río abajo y un hilo fino lo une a su punto */
    if(qb){const dx=p0[0]-qb[0],dy=p0[1]-qb[1],d=Math.hypot(dx,dy);if(d<24*px){const s=pr(r.curso[Math.min(r.curso.length-1,(r.paradas[prox].idx|0)+1)]),ux=d>px?dx:s[0]-p0[0],uy=d>px?dy:s[1]-p0[1],nu=Math.hypot(ux,uy)||1;
      q=[qb[0]+ux/nu*38*px,qb[1]+uy/nu*38*px];puestos.push({x0:q[0]-15*px,x1:q[0]+15*px,y0:q[1]-15*px,y1:q[1]+15*px});H+=`<path class="v-guia" d="M${p0[0].toFixed(2)} ${p0[1].toFixed(2)}L${q[0].toFixed(2)} ${q[1].toFixed(2)}" stroke-width="${f(1)}"/>`}}
    H+=`<circle class="v-prox" cx="${q[0].toFixed(2)}" cy="${q[1].toFixed(2)}" r="${f(11)}" stroke-width="${f(1.6)}" stroke-dasharray="${f(2.2)} ${f(3.4)}"/><text class="v-prox-t" x="${q[0].toFixed(2)}" y="${(q[1]+5*px).toFixed(2)}" font-size="${f(14)}" text-anchor="middle">?</text>`}

  /* paralelos con nombre: el rótulo va pegado a un borde de la vista, del lado donde no pisa el río */
  CARTA.lineas.forEach(l=>{const y=pr([l.lat,0])[1]-5*px;if(y<vb.y+16*px||y>vb.y+vb.h-6*px)return;
    /* en la portada el título va arriba a la izquierda: el trópico solo sale a la derecha, en dos renglones si entero no cabe */
    const der=momento==='portada'&&l.portada==='der',t2=l.t.replace(' ','|'),ops=der?[[l.t,'end'],[t2,'end']]:[[l.t,'start'],[l.t,'end'],[t2,'start'],[t2,'end']];
    for(const [t,anc] of ops){const x=anc==='start'?vb.x+12*px:vb.x+vb.w-12*px,yy=t.indexOf('|')>=0?y-15*px:y,c=caja(t,x,yy,anc,'linea');if(libre(c)){puestos.push(c);H+=texto(t,x,yy,anc,'linea');break}}});

  /* rótulos de atlas, en orden de jerarquía: el que no cabe entero, pisa el río o pisa a otro, no sale */
  const vistos={};/* de cada nombre, una sola versión por vista: la primera que cabe */
  CARTA.rotulos.forEach(o=>{const nom=o.t.replace('|',' ');if(vistos[nom]||ancho>o.max||(o.min&&ancho<=o.min))return;const q=pr(o.p),c=caja(o.t,q[0],q[1],o.a,o.c,o.g);if(!libre(c))return;vistos[nom]=1;puestos.push(c);H+=texto(o.t,q[0],q[1],o.a,o.c,o.g)});

  /* hitos: una marca (cuadrito o dos triángulos) y su nombre a 11 px; ninguno es una parada */
  CARTA.hitos.forEach(o=>{if(ancho>o.max||(o.tras!=null&&!(foco.etiquetas&&foco.etiquetas.has(o.tras))))return;const q=pr(o.p);if(!dentro(q))return;
    const tri=o.m==='tri',izq=o.l==='izq',mx=tri?(izq?q[0]-21*px:q[0]+4*px):q[0]-2.5*px,x=izq?(tri?mx-5*px:q[0]-8*px):(tri?mx+22*px:q[0]+8*px),y=q[1]+4*px,anc=izq?'end':'start',c=caja(o.t,x,y,anc,'hito');
    if(!libre(c))return;puestos.push(c,{x0:mx-2*px,x1:mx+19*px,y0:q[1]-6*px,y1:q[1]+6*px});
    H+=(tri?`<path class="v-marca" stroke-width="${f(1.1)}" d="M${mx.toFixed(2)} ${(q[1]+4*px).toFixed(2)}l${f(4.5)} ${f(-8)}l${f(4.5)} ${f(8)}zm${f(8)} 0l${f(4.5)} ${f(-8)}l${f(4.5)} ${f(8)}z"/>`:`<path class="v-marca" stroke-width="${f(1.1)}" d="M${mx.toFixed(2)} ${(q[1]-2.5*px).toFixed(2)}h${f(5)}v${f(5)}h${f(-5)}z"/>`)+texto(o.t,x,y,anc,'hito')});

  grupo(capa,'v-rotulos',H,capa.querySelector('#estela')||capa.querySelector('rect.hitz'))}

/* después de que el motor dibujó el mapa */
CAPA.mapa=function(foco,vb,px){try{fondo();dibujar(foco,vb,px)}catch(e){if(typeof console!=='undefined'&&console.warn)console.warn('carta:',e)}};

/* el encuadre de cada momento: {pts, minW, margen} para vbPara del motor (minW en unidades del SVG: 1 unidad = 0,36°) */
CAPA.vista=function(r,foco){if(!r||r.id!==CAPA.rio||typeof CAPA.momento!=='function'||!r.curso||!r.paradas)return null;
  const m=CAPA.momento(),n=r.paradas.length,p=Math.max(0,Math.min(n+1,paso()));
  if(m==='portada')return{pts:r.curso.concat(r.paradas.map(c=>c.pos),[[33.4,31.2],[16.9,21.0],[-3.6,33.2]]),minW:20,margen:1.1};   /* el río entero, con un poco de mar arriba para su rótulo, aire al oeste (el título va arriba a la izquierda y el río pasa por los dos tercios del ancho) y aire al sur del nacimiento: la barca, Hipo y la orilla norte del lago Victoria quedan enteros por encima del borde de la hoja */
  if(m==='navega'||m==='evento'){/* en un evento la barca está detenida a mitad del tramo: el mismo encuadre, de la parada anterior a la de llegada (S.evento.tramo, 1…n+1) */
    const ev=m==='evento'&&typeof S!=='undefined'&&S&&S.evento&&S.evento.tramo?Math.max(1,Math.min(n+1,S.evento.tramo|0)):0,de=idx(r,ev?ev-1:p),a=idx(r,ev||Math.min(n+1,p+1));const t=r.curso.slice(Math.min(de,a),Math.max(de,a)+1);let alto=t[0];t.forEach(q=>{if(q[0]>alto[0])alto=q});const bajo=Math.min.apply(null,t.map(q=>q[0]));
    return{pts:t.concat([[alto[0]+Math.max(.5,(alto[0]-bajo)*.14),alto[1]]]),minW:17,margen:1.42}}/* un punto más al norte: arriba va la cabecera de la vitrina y no tiene que tapar la próxima parada */   /* de la parada actual a la próxima, con aire */
  if(m==='parada'){const c=p>=1&&p<=n?r.paradas[p-1].pos:r.curso[idx(r,p)];return{pts:[[c[0]-2.6,c[1]],[c[0]+3.6,c[1]]],minW:9,margen:1}}   /* la parada, cerca (unos 6° de alto) y un poco abajo del centro: arriba va la cabecera */
  if(m==='mar')return{pts:[[29.6,29.5],[32.6,32.6]],minW:8,margen:1.15};                                     /* el delta, de El Cairo a la costa, con mar arriba para la cabecera */
  return null};
})();
