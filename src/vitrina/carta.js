/* Carta de la vitrina del Nilo: relieve sombreado, retícula, rótulos de atlas, la próxima parada y los encuadres.
   Se carga antes que el motor: acá arriba solo se definen funciones y se registran en CAPA. Todo acceso al DOM va con guardas
   (las pruebas usan un DOM simulado sin createElementNS ni insertAdjacentHTML): si algo falta, la carta del motor queda como está. */
(function(){
if(typeof CAPA==='undefined'||typeof CARTA==='undefined')return;
const NS='http://www.w3.org/2000/svg';
const pr=p=>[(p[1]+180)/360*1000,(90-p[0])/180*500];           /* la proyección del motor */
const txt=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const T=11.3;/* el cuerpo de los rótulos, en px de pantalla: un pelo más de 11 para que el redondeo del navegador no los deje en 10,9 */
const PILDORA=84;/* alto de la píldora del encabezado que flota arriba del mapa (navega, evento, parada, mar) */
const ANCHO_LETRA={agua:8.2,pais:10.2,'rio-n':6.2,linea:9.2,hito:5.9,bajo:5.7,escala:7.2};   /* px por letra a 11 px, con su espaciado */
/* cuántos px del borde de abajo del mapa tapa la hoja de la bitácora (#panel), para no poner nada debajo; sin medidas, 26 */
function solapa(){const m=document.getElementById('mapa'),p=document.getElementById('panel');if(!m||!p||!m.getBoundingClientRect||!p.getBoundingClientRect)return 26;
  const a=m.getBoundingClientRect(),b=p.getBoundingClientRect();if(!a||!b||!a.height)return 26;
  return b.left<a.right-20&&b.top>a.top+a.height*.5&&b.top<a.bottom?Math.max(8,a.bottom-b.top+6):8}
const paso=()=>typeof S!=='undefined'&&S?S.paso|0:0;
const idx=(r,p)=>{const n=r.paradas.length;return p<=0?0:p>n?r.curso.length-1:r.paradas[p-1].idx};

/* el relieve: una sola vez, después de #relieve y antes de #lagos, recortado por la tierra */
function fondo(){const svg=document.getElementById('svg'),lagos=document.getElementById('lagos'),tierra=document.getElementById('tierra');
  if(!svg||!lagos||!svg.insertBefore||!document.createElementNS||lagos.parentNode!==svg||document.getElementById('v-fondo'))return;
  const img=(L,id)=>{const a=pr([L.caja[0],L.caja[1]]),b=pr([L.caja[2],L.caja[3]]);
    return`<image${id?` id="${id}" style="opacity:0"`:''} href="${L.src}" x="${a[0].toFixed(2)}" y="${a[1].toFixed(2)}" width="${(b[0]-a[0]).toFixed(2)}" height="${(b[1]-a[1]).toFixed(2)}" preserveAspectRatio="none"/>`};
  const g=document.createElementNS(NS,'g');g.setAttribute('id','v-fondo');g.setAttribute('aria-hidden','true');
  /* el relieve lejano y, encima, el fino del corredor del río, que aparece al acercarse (ver cerca) */
  g.innerHTML=`<clipPath id="v-recorte"><use href="#tierra" clip-rule="evenodd"/></clipPath><g clip-path="url(#v-recorte)">${img(CARTA.luz)}${CARTA.luz2?img(CARTA.luz2,'v-luz2'):''}</g>`;
  svg.insertBefore(g,lagos);
  /* el halo de la costa: la misma tierra, debajo de la tierra, con tres trazos verde claro de ancho fijo en pantalla; de cada uno solo se ve la mitad que da al mar */
  if(tierra&&tierra.parentNode===svg){const h=document.createElementNS(NS,'g');h.setAttribute('id','v-halo');h.setAttribute('aria-hidden','true');
    h.innerHTML='<use href="#tierra" class="a"/><use href="#tierra" class="b"/><use href="#tierra" class="c"/>';svg.insertBefore(h,tierra)}}
/* el relieve fino se ve cuando la vista es angosta (parada, evento, delta, navegando): px·390 es el ancho de la vista llevado a un teléfono */
function cerca(px){const l=document.getElementById('v-luz2'),h=document.getElementById('v-halo');if(l&&l.style&&CARTA.luz2)l.style.opacity=px*390<=CARTA.luz2.max?'1':'0';
  /* el ancho del halo, en píxeles de pantalla: 16, 8 y 2,2 (vector-effect no llega a las copias de <use>) */
  if(h&&h.children)[16,8,2.2].forEach((w,i)=>{const u=h.children[i];if(u&&u.setAttribute)u.setAttribute('stroke-width',(w*px).toFixed(3))})}

/* un grupo dentro de #capa (el motor la vuelve a escribir en cada render, así que se vuelve a poner cada vez) */
function grupo(capa,id,html,antes){const g=document.createElementNS(NS,'g');g.setAttribute('id',id);g.setAttribute('aria-hidden','true');g.innerHTML=html;capa.insertBefore(g,antes||null)}

/* La falúa y el Hipo de Trazo (CAPA.arte), si están: la falúa reemplaza al glifo del motor dentro de #barca e Hipo nada a popa,
   no encima. El motor gira #barca con el rumbo y endereza #masc en cada cuadro; la falúa, que es un perfil de 52 px, toma ese
   mismo enderezado (va siempre derecha y solo se da vuelta a la izquierda cuando el río va hacia el oeste). */
let MIRA=1;/* hacia dónde mira la falúa (1 derecha, −1 izquierda): el rumbo del viaje de punta a punta; no cambia con cada recodo ni al volver a dibujar */
function derecha(){const m=document.getElementById('masc'),g=document.getElementById('v-falua'),b=document.getElementById('barca');if(!m||!g||!b||!m.getAttribute||!g.setAttribute)return;
  const t=m.getAttribute('transform');if(!t)return;
  const k=(/scale\(-1 /.test(b.getAttribute('transform')||'')?-1:1)*MIRA,h=document.getElementById('v-hipo');/* el espejo del motor por el espejo que hace falta */
  g.setAttribute('transform',t+(k<0?' scale(-1 1)':''));if(h&&h.setAttribute)h.setAttribute('transform',(k<0?'scale(-1 1) ':'')+'translate(-40 4)')}
function arte(foco,momento){const A=CAPA.arte,b=document.getElementById('barca'),m=document.getElementById('masc'),B=foco.barca;
  if(!A||typeof A.falua!=='function'||typeof A.hipoNada!=='function'||!b||!b.querySelector||!m||!foco.rio||!B)return false;
  const g=b.querySelector('.mece > g');if(!g)return false;
  let P,ida;if(B.poly){P=B.poly;ida=B.t1>=B.t0}else{P=[foco.rio.curso[B.de],foco.rio.curso[B.a]];ida=true}
  if(P&&P.length>1){const dx=(pr(P[P.length-1])[0]-pr(P[0])[0])*(ida?1:-1);if(Math.abs(dx)>1e-6)MIRA=dx<0?-1:1}
  let cargas=[],falua,hipo;try{if(A.cargasDe)cargas=A.cargasDe(foco.rio)||[]}catch(e){}
  try{falua=A.falua(cargas);hipo=A.hipoNada(momento==='evento'?'sorpresa':momento==='mar'?'alegre':'normal')}catch(e){return false}/* si el dibujo falla, queda el glifo del motor */
  if(!falua||!hipo)return false;
  g.innerHTML=falua;g.setAttribute('id','v-falua');
  m.innerHTML=`<g id="v-hipo" transform="translate(-40 4)">${hipo}</g>`;
  derecha();return true}
/* hacia dónde mira la barca al llegar (la regla de animarBarca): 1 a la derecha, −1 a la izquierda */
function mirada(r,B){let P,fin;if(B.poly){P=B.poly;fin=B.t1>=B.t0}else{P=r.curso.slice(Math.min(B.de,B.a),Math.max(B.de,B.a)+1);fin=B.de<=B.a}
  if(!P||P.length<2)return 1;const a=pr(fin?P[P.length-2]:P[0]),b=pr(fin?P[P.length-1]:P[1]);return b[0]-a[0]<0?-1:1}
if(typeof CAPA.oir==='function')CAPA.oir('avanza',derecha);

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
  if(momento!=='portada')puestos.push({x0:vb.x+70*px,x1:vb.x+vb.w-70*px,y0:vb.y,y1:vb.y+PILDORA*px});/* la píldora del encabezado, arriba al centro */
  if(momento==='portada')puestos.push({x0:vb.x,x1:vb.x+220*px,y0:vb.y+64*px,y1:vb.y+352*px});/* y en la portada, arriba a la izquierda, va el título (hasta la firma de la cita) */
  const muestrear=P=>{for(let i=0;i+1<P.length;i++){const p=pr(P[i]),q=pr(P[i+1]);
    if(Math.max(p[0],q[0])<vb.x-vb.w*.2||Math.min(p[0],q[0])>vb.x+vb.w*1.2||Math.max(p[1],q[1])<vb.y-vb.h*.2||Math.min(p[1],q[1])>vb.y+vb.h*1.2)continue;
    const m=Math.min(400,Math.max(1,Math.ceil(Math.hypot(q[0]-p[0],q[1]-p[1])/(3*px))));for(let k=0;k<=m;k++)rio.push([p[0]+(q[0]-p[0])*k/m,p[1]+(q[1]-p[1])*k/m])}};
  muestrear(r.curso);(r.ramas||[]).forEach(muestrear);/* el cauce y también los afluentes: ningún rótulo sobre un río */
  const borde=solapa();/* px del borde de abajo del mapa que tapa la hoja */
  const prox=typeof S!=='undefined'&&S&&S.pantalla==='rio'&&S.tab==='descender'&&momento!=='portada'&&paso()<n?paso():-1;/* en la portada no hay pregunta todavía */
  /* la barca tapa la primera letra del nombre de la parada donde está: ese nombre se corre hacia afuera */
  const B=foco.barca,qb=B?pr(B.poly?B.poly[B.t1>=B.t0?B.poly.length-1:0]:r.curso[B.a]):null;
  let renglon=null;
  const conArte=!!B&&arte(foco,momento),mira=conArte?MIRA:B?mirada(r,B):1;/* con la falúa nueva (52 px, Hipo a popa) todo lo que esquiva a la barca necesita más lugar */
  if(qb&&capa.querySelectorAll)r.paradas.forEach((c,i)=>{const q=pr(c.pos);if(!foco.etiquetas||!foco.etiquetas.has(i)||Math.hypot(q[0]-qb[0],q[1]-qb[1])>10*px)return;
    capa.querySelectorAll('text.etq').forEach(t=>{if(!t.getAttribute||!t.classList||t.classList.contains('relieve')||t.textContent!==c.nombre)return;const x=parseFloat(t.getAttribute('x')),fin=t.getAttribute('text-anchor')==='end';
      const corre=conArte?(fin?(mira>0?-50:-26):(mira>0?26:50)):(fin?-16:14);/* del lado de popa hay que pasar también a Hipo */
      if(!isFinite(x))return;t.setAttribute('x',(x+corre*px).toFixed(2));
      /* y, donde los datos del juego lo dan, un renglón en cursiva debajo (CARTA.renglones): solo en la parada donde está la barca */
      const y=parseFloat(t.getAttribute('y'));if(CARTA.renglones&&CARTA.renglones[i]&&isFinite(y))renglon={t:CARTA.renglones[i],x:x+corre*px,y:y+14*px,anc:fin?'end':'start'}})});
  r.paradas.forEach((c,i)=>{const q=pr(c.pos),d=(i===prox?15:7)*px;puestos.push({x0:q[0]-d,x1:q[0]+d,y0:q[1]-d,y1:q[1]+d})});
  /* los nombres que puso el motor (las paradas alcanzadas), cada uno con su caja de verdad */
  if(capa.querySelectorAll)capa.querySelectorAll('text.etq').forEach(t=>{if(!t.getAttribute||!t.classList||t.classList.contains('relieve'))return;
    const x=parseFloat(t.getAttribute('x')),y=parseFloat(t.getAttribute('y')),w=((t.textContent||'').length*9.2+4)*px,an=t.getAttribute('text-anchor');if(!isFinite(x)||!isFinite(y))return;
    const x0=an==='end'?x-w:an==='middle'?x-w/2:x;puestos.push({x0,x1:x0+w,y0:y-13*px,y1:y+4*px})});
  const qp=qb||(momento==='portada'&&r.curso&&r.curso.length?pr(r.curso[0]):null);
  if(qp)puestos.push(conArte||momento==='portada'?{x0:qp[0]-54*px,x1:qp[0]+54*px,y0:qp[1]-38*px,y1:qp[1]+16*px}:{x0:qp[0]-24*px,x1:qp[0]+22*px,y0:qp[1]-32*px,y1:qp[1]+14*px});
  if(false)puestos.push(conArte?{x0:qb[0]-54*px,x1:qb[0]+54*px,y0:qb[1]-38*px,y1:qb[1]+16*px}:{x0:qb[0]-24*px,x1:qb[0]+22*px,y0:qb[1]-32*px,y1:qb[1]+14*px});
  const libre=c=>c.x0>vb.x+M&&c.x1<vb.x+vb.w-M&&c.y0>vb.y+M&&c.y1<vb.y+vb.h-borde*px&&!puestos.some(o=>c.x0<o.x1+M&&c.x1>o.x0-M&&c.y0<o.y1+M&&c.y1>o.y0-M)&&!rio.some(p=>p[0]>c.x0-M&&p[0]<c.x1+M&&p[1]>c.y0-M&&p[1]<c.y1+M);
  /* la caja de un rótulo de 11 px (renglones partidos con |), con su ancla y su giro */
  const caja=(t,x,y,anc,cls,giro)=>{const rs=t.split('|'),w=Math.max.apply(null,rs.map(s=>s.length))*ANCHO_LETRA[cls]*px,h=(13+(rs.length-1)*15)*px;
    if(giro){const g=giro*Math.PI/180,c=Math.abs(Math.cos(g)),s=Math.abs(Math.sin(g)),bw=c*w+s*h,bh=s*w+c*h;return{x0:x-bw/2,x1:x+bw/2,y0:y-bh/2,y1:y+bh/2}}
    const x0=anc==='end'?x-w:anc==='middle'?x-w/2:x;return{x0,x1:x0+w,y0:y-10*px,y1:y-10*px+h}};
  const texto=(t,x,y,anc,cls,giro)=>{const rs=t.split('|'),X=x.toFixed(2),Y=y.toFixed(2);
    return`<text class="v-rot ${cls}" x="${X}" y="${Y}" font-size="${f(T)}" stroke-width="${f(2.6)}" text-anchor="${anc}"${giro?` transform="rotate(${giro} ${X} ${Y})"`:''}>${rs.length>1?rs.map((s,i)=>`<tspan x="${X}" dy="${i?f(15):0}">${txt(s)}</tspan>`).join(''):txt(t)}</text>`};
  let H='';
  if(renglon){const c=caja(renglon.t,renglon.x,renglon.y,renglon.anc,'bajo');puestos.push(c);H+=texto(renglon.t,renglon.x,renglon.y,renglon.anc,'bajo')}

  /* escala gráfica (abajo a la izquierda, sobre el borde de la hoja) y norte (arriba a la derecha, bajo el botón de sonido); en la
     portada, no. La barra es el número redondo de kilómetros que mide de 70 a 130 px en la latitud del centro de la vista
     (1 unidad del SVG = 0,36° de longitud). Si el río pasa por ahí, la escala prueba a la derecha; si no cabe, no sale. */
  if(momento!=='portada'){const latC=90-(vb.y+vb.h/2)/500*180,kmPx=0.36*111.32*Math.cos(latC*Math.PI/180)*px,
      km=([1000,500,250,200,100,50,25,20,10,5,2,1].map(k=>[k,k/kmPx]).filter(v=>v[1]>=64&&v[1]<=136).sort((u,v)=>Math.abs(u[1]-100)-Math.abs(v[1]-100))[0]||[0])[0];/* 70 a 130 px, con un poco de holgura para que siempre haya un número redondo */
    if(km){const largo=km/kmPx*px,yb=vb.y+vb.h-(borde+14)*px;
      for(const x0 of [vb.x+16*px,vb.x+vb.w-16*px-largo]){const c={x0:x0-3*px,x1:x0+Math.max(largo,56*px)+3*px,y0:yb-24*px,y1:yb+4*px};if(!libre(c))continue;puestos.push(c);
        H+=`<path class="v-escala" stroke-width="${f(1.3)}" d="M${x0.toFixed(2)} ${(yb-5*px).toFixed(2)}V${yb.toFixed(2)}h${largo.toFixed(2)}v${f(-5)}"/><text class="v-rot escala" x="${x0.toFixed(2)}" y="${(yb-10*px).toFixed(2)}" font-size="${f(T)}" stroke-width="${f(2.6)}">${km} km</text>`;break}}
    const xn=vb.x+vb.w-37*px,yn=vb.y+74*px,cn={x0:xn-10*px,x1:xn+10*px,y0:yn-3*px,y1:yn+40*px};
    if(libre(cn)){puestos.push(cn);H+=`<path class="v-escala" stroke-width="${f(1.3)}" d="M${xn.toFixed(2)} ${(yn+22*px).toFixed(2)}V${yn.toFixed(2)}m${f(-4)} ${f(6)}l${f(4)} ${f(-6)}l${f(4)} ${f(6)}"/><text class="v-rot escala" x="${xn.toFixed(2)}" y="${(yn+37*px).toFixed(2)}" font-size="${f(T)}" stroke-width="${f(2.6)}" text-anchor="middle" style="stroke-width:${f(4)}">N</text>`}}

  /* la próxima parada: anillo punteado con un signo de pregunta, sin nombre (memoria primero) */
  if(prox>=0){const p0=pr(r.paradas[prox].pos);let q=p0;
    /* si la parada queda a menos de 24 px de la barca (Jinja, a un paso del nacimiento), el anillo se corre río abajo y un hilo fino lo une a su punto */
    if(qb){const dx=p0[0]-qb[0],dy=p0[1]-qb[1],d=Math.hypot(dx,dy);if(d<(conArte?50:24)*px){const s=pr(r.curso[Math.min(r.curso.length-1,(r.paradas[prox].idx|0)+8)]),ux=d>px?dx:s[0]-p0[0],uy=d>px?dy:s[1]-p0[1],nu=Math.hypot(ux,uy)||1,lejos=(conArte?64:38)*px;
      q=[qb[0]+ux/nu*lejos,qb[1]+uy/nu*lejos];puestos.push({x0:q[0]-15*px,x1:q[0]+15*px,y0:q[1]-15*px,y1:q[1]+15*px});H+=`<path class="v-guia" d="M${p0[0].toFixed(2)} ${p0[1].toFixed(2)}L${q[0].toFixed(2)} ${q[1].toFixed(2)}" stroke-width="${f(1)}"/>`}}
    H+=`<circle class="v-prox" cx="${q[0].toFixed(2)}" cy="${q[1].toFixed(2)}" r="${f(11)}" stroke-width="${f(1.6)}" stroke-dasharray="${f(2.2)} ${f(3.4)}"/><text class="v-prox-t" x="${q[0].toFixed(2)}" y="${(q[1]+5*px).toFixed(2)}" font-size="${f(14)}" text-anchor="middle">?</text>`}

  /* paralelos con nombre: el rótulo va pegado a un borde de la vista, del lado donde no pisa el río */
  CARTA.lineas.forEach(l=>{const y=pr([l.lat,0])[1]-5*px;if(y<vb.y+16*px||y>vb.y+vb.h-6*px)return;
    /* en la portada el título va arriba a la izquierda: el trópico solo sale a la derecha, en dos renglones si entero no cabe */
    const der=momento==='portada'&&l.portada==='der',t2=l.t.replace(' ','|'),ops=der?[[l.t,'end'],[t2,'end']]:[[l.t,'start'],[l.t,'end'],[t2,'start'],[t2,'end']];
    for(const [t,anc] of ops){const x=anc==='start'?vb.x+12*px:vb.x+vb.w-12*px,yy=t.indexOf('|')>=0?y-15*px:y,c=caja(t,x,yy,anc,'linea');if(libre(c)){puestos.push(c);H+=texto(t,x,yy,anc,'linea');break}}});

  /* rótulos de atlas, en orden de jerarquía: el que no cabe entero, pisa el río o pisa a otro, no sale */
  const vistos={};/* de cada nombre, una sola versión por vista: la primera que cabe */
  const alcanzada=i=>i==null||!!(foco.etiquetas&&foco.etiquetas.has(i));/* `tras`: lo que solo sale cuando esa parada ya se alcanzó */
  CARTA.rotulos.forEach(o=>{const nom=o.t.replace('|',' ');if(vistos[nom]||ancho>o.max||(o.min&&ancho<=o.min)||!alcanzada(o.tras))return;const q=pr(o.p),c=caja(o.t,q[0],q[1],o.a,o.c,o.g);if(!libre(c))return;vistos[nom]=1;puestos.push(c);H+=texto(o.t,q[0],q[1],o.a,o.c,o.g)});

  /* la boca del río: su nombre pegado al último punto del cauce, del lado que quede libre (la barca puede estar ahí), y un
     circulito hueco en la boca cuando la barca no la tapa */
  const BO=CARTA.boca;if(BO&&ancho<=BO.max&&alcanzada(BO.tras)){const q=pr(r.curso[r.curso.length-1]);
    if(dentro(q)){if(!qb||Math.hypot(q[0]-qb[0],q[1]-qb[1])>30*px)H+=`<circle class="v-boca" cx="${q[0].toFixed(2)}" cy="${q[1].toFixed(2)}" r="${f(4.5)}" stroke-width="${f(1.6)}"/>`;
      for(const [dx,dy,anc] of [[-12,-7,'end'],[0,-52,'middle'],[-64,-8,'end'],[64,-8,'start'],[0,34,'middle']]){const x=q[0]+dx*px,y=q[1]+dy*px,c=caja(BO.t,x,y,anc,'rio-n');if(libre(c)){puestos.push(c);H+=texto(BO.t,x,y,anc,'rio-n');break}}}}

  /* hitos: una marca (cuadrito o dos triángulos) y su nombre a 11 px; ninguno es una parada. El nombre prueba su lado, el otro y,
     si es largo, lo mismo en dos renglones: el primero que no pise un río, un rótulo ni la barca */
  CARTA.hitos.forEach(o=>{if(ancho>o.max||!alcanzada(o.tras))return;const q=pr(o.p);if(!dentro(q))return;
    const tri=o.m==='tri',otro=o.l==='izq'?'der':'izq',t2=o.t.length>12?o.t.replace(' ','|'):null,ops=[[o.t,o.l],[o.t,otro]];if(t2)ops.push([t2,o.l],[t2,otro]);
    if(!tri)ops.push([o.t,'abajo'],[o.t,'arriba']);/* una marca chica también admite el nombre debajo o encima */
    for(const [t,lado] of ops){const izq=lado==='izq',vert=lado==='abajo'||lado==='arriba',mx=tri?(izq?q[0]-21*px:q[0]+4*px):q[0]-2.5*px,
        x=vert?q[0]:izq?(tri?mx-5*px:q[0]-8*px):(tri?mx+22*px:q[0]+8*px),y=q[1]+(lado==='abajo'?18:lado==='arriba'?-9:t===o.t?4:-3)*px,anc=vert?'middle':izq?'end':'start',c=caja(t,x,y,anc,'hito'),cm={x0:mx-2*px,x1:mx+(tri?19:7)*px,y0:q[1]-6*px,y1:q[1]+6*px};
      if(!libre(c)||puestos.some(p=>cm.x0<p.x1&&cm.x1>p.x0&&cm.y0<p.y1&&cm.y1>p.y0))continue;puestos.push(c,cm);
      H+=(tri?`<path class="v-marca" stroke-width="${f(1.1)}" d="M${mx.toFixed(2)} ${(q[1]+4*px).toFixed(2)}l${f(4.5)} ${f(-8)}l${f(4.5)} ${f(8)}zm${f(8)} 0l${f(4.5)} ${f(-8)}l${f(4.5)} ${f(8)}z"/>`:`<path class="v-marca" stroke-width="${f(1.1)}" d="M${mx.toFixed(2)} ${(q[1]-2.5*px).toFixed(2)}h${f(5)}v${f(5)}h${f(-5)}z"/>`)+texto(t,x,y,anc,'hito');break}});

  /* para revisar la colocación: con CAPA.depurarCarta=1 se ven las cajas ocupadas (rótulos, nombres, barca, esquinas, título) */
  if(CAPA.depurarCarta)H+=puestos.map(o=>`<rect x="${o.x0.toFixed(2)}" y="${o.y0.toFixed(2)}" width="${(o.x1-o.x0).toFixed(2)}" height="${(o.y1-o.y0).toFixed(2)}" fill="none" stroke="#A6472E" stroke-width="${f(1)}"/>`).join('');
  grupo(capa,'v-rotulos',H,capa.querySelector('#estela')||capa.querySelector('rect.hitz'))}

/* después de que el motor dibujó el mapa */
CAPA.mapa=function(foco,vb,px){try{fondo();cerca(px);dibujar(foco,vb,px)}catch(e){if(typeof console!=='undefined'&&console.warn)console.warn('carta:',e)}};

/* el encuadre de cada momento: {pts, minW, margen} para vbPara del motor (minW en unidades del SVG: 1 unidad = 0,36°) */
/* reserva arriba los px reales de la píldora: un punto al norte de lo encuadrado, tal que vbPara (mismo cálculo) deje PILDORA+8 px libres */
function reservar(v,dims,cuida){if(!v||!dims||!dims.ancho)return v;cuida=(cuida||[]).map(c=>pr(c).concat([c[2]||0]));/* [lat, lon, px de más]: en Jinja el anillo se corre unos 64 px de la barca */const an=dims.ancho,des=dims.des||dims.alto||260,asp=an/des,base=v.pts.map(pr);
  const y0=Math.min.apply(null,base.map(q=>q[1]));let extra=null;
  for(let k=0;k<8;k++){const P=extra?base.concat([extra]):base;let x0=1e9,x1=-1e9,ya=1e9,yb=-1e9;P.forEach(q=>{x0=Math.min(x0,q[0]);x1=Math.max(x1,q[0]);ya=Math.min(ya,q[1]);yb=Math.max(yb,q[1])});
    let w=(x1-x0)*v.margen,h=(yb-ya)*v.margen;w=Math.max(w,v.minW);h=Math.max(h,v.minW/asp);if(w/h<asp)w=h*asp;else h=w/asp;
    const top=(ya+yb)/2-h/2,s=w/an,cx=(x0+x1)/2;let falta=(PILDORA+8)*s-(y0-top);
    cuida.forEach(q=>{if(Math.abs(q[0]-cx)<w/2&&q[1]>top&&q[1]<top+h)falta=Math.max(falta,(PILDORA+18+(q[2]||0))*s-(q[1]-top))});/* el anillo de la próxima parada, si cae en la vista */if(falta<=s*.5)break;extra=[(x0+x1)/2,(extra?extra[1]:y0)-falta]}
  if(extra)v.pts=v.pts.concat([[90-extra[1]/500*180,extra[0]/1000*360-180]]);return v}
CAPA.vista=function(r,foco,dims){const v=vista0(r,foco),p=paso(),m=CAPA.momento();
  return v&&m!=='portada'?reservar(v,dims,m!=='mar'&&p>=0&&p<r.paradas.length?[r.paradas[p].pos.concat([p===0?66:0])]:[]):v};
function vista0(r,foco){if(!r||r.id!==CAPA.rio||typeof CAPA.momento!=='function'||!r.curso||!r.paradas)return null;
  const m=CAPA.momento(),n=r.paradas.length,p=Math.max(0,Math.min(n+1,paso()));
  if(m==='portada')return{pts:r.curso.concat(r.paradas.map(c=>c.pos),[[33.4,31.2],[16.9,21.0],[-3.6,33.2]]),minW:20,margen:1.1};   /* el río entero, con un poco de mar arriba para su rótulo, aire al oeste (el título va arriba a la izquierda y el río pasa por los dos tercios del ancho) y aire al sur del nacimiento: la barca, Hipo y la orilla norte del lago Victoria quedan enteros por encima del borde de la hoja */
  if(m==='navega'||m==='evento'){/* en un evento la barca está detenida a mitad del tramo: el mismo encuadre, de la parada anterior a la de llegada (S.evento.tramo, 1…n+1) */
    const ev=m==='evento'&&typeof S!=='undefined'&&S&&S.evento&&S.evento.tramo?Math.max(1,Math.min(n+1,S.evento.tramo|0)):0,de=idx(r,ev?ev-1:p),a=idx(r,ev||Math.min(n+1,p+1));const t=r.curso.slice(Math.min(de,a),Math.max(de,a)+1);let alto=t[0];t.forEach(q=>{if(q[0]>alto[0])alto=q});const bajo=Math.min.apply(null,t.map(q=>q[0]));
    return{pts:t.concat([[alto[0]+Math.max(.5,(alto[0]-bajo)*.14),alto[1]]]),minW:17,margen:1.42}}/* un punto más al norte: arriba va la cabecera de la vitrina y no tiene que tapar la próxima parada */   /* de la parada actual a la próxima, con aire */
  if(m==='parada'){const c=p>=1&&p<=n?r.paradas[p-1].pos:r.curso[idx(r,p)];return{pts:[[c[0]-2.6,c[1]],[c[0]+3.6,c[1]]],minW:9,margen:1}}   /* la parada, cerca (unos 6° de alto) y un poco abajo del centro: arriba va la cabecera */
  if(m==='mar')return{pts:[[29.6,29.5],[32.6,32.6]],minW:8,margen:1.15};                                     /* el delta, de El Cairo a la costa, con mar arriba para la cabecera */
  return null}
})();
