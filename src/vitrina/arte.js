// Trazo: los dibujos a mano de la vitrina del Nilo (docs/vitrina/contrato.md, «CAPA.arte»): la falúa con la carga a la vista,
// cada carga sola e Hipo nadando junto a la barca. SVG plano, sin degradados; 1 unidad = 1 px de pantalla (la falúa mide 52 px
// de ancho; Hipo, 22). Los colores van por clases en arte.css. Se carga antes que el motor: aquí solo se define CAPA.arte; lo
// del motor (S) se usa dentro de cargasDe, que corre después. Nada de DOM.
(function(){
  if(typeof CAPA==='undefined')return;/* sin la capa no hay dónde colgar el arte: el juego sigue como siempre */
  const pth=(c,d)=>`<path class="${c}" d="${d}"/>`,cir=(c,x,y,r)=>`<circle class="${c}" cx="${x}" cy="${y}" r="${r}"/>`;

  /* ---------- las cargas: caja de 12 × 12, origen en el centro del suelo (x −6…6, y −12…0). Cada una tiene silueta propia,
     porque a este tamaño el detalle de adentro no se lee: saco panzón con su nudo, arco de colmillos, cuenco con montón, racimo,
     rollo con su tela tendida, gavilla de tres espigas y dos peces colgados de una vara. El obelisco es el único largo: acostado, x −16…15, punta a proa. ---------- */
  const DATILES=[[-2.6,-7.4],[0,-7.4],[2.6,-7.4],[-1.3,-5.1],[1.3,-5.1],[0,-2.9]];
  const r1=v=>+v.toFixed(1),pez=x=>pth('v-carga v-claro',`M${x} -9.4Q${r1(x-3.9)} -6.8 ${x} -3.8L${r1(x-2)} -.7L${r1(x+2)} -.7L${x} -3.8Q${r1(x+3.9)} -6.8 ${x} -9.4Z`)+cir('v-tinta',x,-7.4,.6);
  const CARGAS={
    /* un saco atado: panzón, de hombros redondos, con el cuello fruncido arriba, a un lado, y la boca abierta en abanico */
    cafe:pth('v-carga','M-3.4 -.6Q-5.2 -.8 -5 -3.4Q-4.8 -6.6 -2 -7.2L1.3 -7L1 -10.4L5.7 -9.7L3.9 -6.5Q5.2 -5 5 -3.2Q5.2 -.8 3.4 -.6Z')+pth('v-linea','M1.3 -7.1L3.9 -6.6'),
    /* dos colmillos curvos, parados y enfrentados: las puntas se buscan arriba */
    marfil:pth('v-carga v-crema','M-4.7 -.7Q-6.2 -7.6 -.9 -10.7Q-2 -6 -1.1 -.7Z')+pth('v-carga v-crema','M4.7 -.7Q6.2 -7.6 .9 -10.7Q2 -6 1.1 -.7Z'),
    /* un cuenco con trozos de goma arábiga: el borde del cuenco va delante de los trozos de abajo */
    goma:cir('v-carga v-calido',-2.1,-5.6,1.8)+cir('v-carga v-calido',2.1,-5.6,1.8)+cir('v-carga v-calido',0,-7.9,1.8)+pth('v-carga v-t2','M-4.5 -4.4L4.5 -4.4Q4.2 -.6 0 -.6Q-4.2 -.6 -4.5 -4.4Z'),
    /* un racimo: los dátiles en una sola masa (borde oscuro detrás, frutos sin línea encima) y el tallo en gancho */
    datiles:pth('v-tallo','M0 -8.8Q-.4 -11 -3.4 -10.8')+DATILES.map(p=>cir('v-borde',p[0],p[1],1.55)).join('')+DATILES.map(p=>cir('v-carga v-calido v-sin',p[0],p[1],1.55)).join(''),
    /* el obelisco de Asuán, de granito rosado, acostado: a popa el zócalo, más ancho; el fuste se angosta hasta la punta, y una
       línea lo separa del piramidión, que mira a proa. (Las cuñas de madera no caben: el fuste queda a 1 px del suelo.) */
    obelisco:pth('v-carga v-calido','M-12.4 -1.1L10 -2.2L10 -5.4L-12.4 -6.5Z')+pth('v-carga v-calido','M10 -2.2L13.9 -3.8L10 -5.4Z')+pth('v-carga v-calido','M-15 -.6L-12.4 -.6L-12.4 -7.2L-15 -7.2Z'),
    /* un rollo de tela que se desenrolla: la tela tendida en el suelo, a popa, y el rollo de canto, con su espiral */
    lino:pth('v-carga','M2 -.6L-5.3 -.6L-5.3 -4L0 -4Z')+cir('v-carga v-t2',2.2,-3.9,3.3)+pth('v-linea v-fina','M2.2 -3.9A.7 .7 0 0 1 3.6 -3.9A1.5 1.5 0 0 1 .6 -3.9'),
    /* una gavilla atada: los tallos abiertos abajo, la cintura atada y tres espigas en abanico */
    trigo:pth('v-carga v-crema','M-3 -.6L3 -.6L1.5 -3.8L2.1 -5.2Q5.2 -6.2 4.6 -10Q2.3 -9 1.6 -7Q1.6 -9.6 0 -11.3Q-1.6 -9.6 -1.6 -7Q-2.3 -9 -4.6 -10Q-5.2 -6.2 -2.1 -5.2L-1.5 -3.8Z')+pth('v-linea','M-1.7 -4.4L1.7 -4.4'),
    /* dos pescados secos colgados de una vara, la cola abajo */
    pescado:pth('v-palo','M-4.6 -10.2L4.6 -10.2')+pez(-2.3)+pez(2.3)};
  const CLAVES=['cafe','marfil','goma','datiles','obelisco','lino','trigo','pescado'];
  function carga(clave){return CARGAS[clave]||''}

  /* ---------- la falúa: de perfil, proa a la derecha; origen en el centro del casco sobre la línea de flotación; caja x −26…26,
     y −34…10. La entena larga sube de la proa hacia popa y la vela cuelga de ella con el pujamen alto: debajo queda la cubierta
     libre, entre el palo y la popa, para la carga, que se ve contra el agua. El obelisco va acostado sobre la borda y lo demás, encima.
     Trazo de 1,3 px (1,5 en palos y agua; 1,0 a 1,1 solo en detalles de adentro: la espiral del lino, la zeta, el blanco del ojo). */
  const SITIOS={1:[-7],2:[-12,-2.5],3:[-15.8,-6.6,2.6]},SOBRE={1:[-9],2:[-14,-4.5]};
  function falua(cargas){
    const cs=[];for(const c of (cargas||[]))if(CARGAS[c]&&cs.length<3&&!(c==='obelisco'&&cs.indexOf(c)>=0))cs.push(c);/* la bodega puede traer dos del mismo bien: van los dos; obelisco hay uno solo */
    const ob=cs.indexOf('obelisco')>=0,otras=cs.filter(c=>c!=='obelisco'),xs=(ob?SOBRE:SITIOS)[otras.length]||[],y=ob?-11.2:-5.6;
    return pth('v-casco','M-23.2 -1.5L-25.8 -.8L-25.6 6.2L-22.6 4Z')/* la pala del timón, bajo la popa */
      +pth('v-palo','M10 -6L13 -19.5')/* el palo corto, caído hacia proa */
      +pth('v-vela','M23.5 -12.6L-10 -32.8Q-17.5 -28.5 -20 -21.5Q2 -19.5 23.5 -12.6Z')
      +pth('v-palo','M25.6 -11.2L-12 -33.9')/* la entena */
      +pth('v-palo v-cabo','M-20 -21.5L-22.4 -8.4')/* la escota, a popa */
      +otras.map((c,i)=>`<g transform="translate(${xs[i]} ${y})">${CARGAS[c]}</g>`).join('')
      +pth('v-casco v-panza','M-22.6 0Q-21.5 4 -15 5.2Q0 6.6 13 5.2Q19 4 21.2 0Z')
      +pth('v-casco','M-24.4 -8.6Q-12 -5.6 0 -5.6Q14 -5.6 25.6 -10.6Q24.6 -4 21.2 0L-22.6 0Q-23.8 -4 -24.4 -8.6Z')
      +(ob?`<g transform="translate(-7 -5.4)">${CARGAS.obelisco}</g>`:'')}

  /* ---------- Hipo nadando: solo la cabeza asomada del agua, de frente; origen en su centro, caja x −11…11, y −8…6. Lo que dice
     «hipopótamo» a 22 px: las orejitas redondas, chicas y bien separadas, arriba; los ojos en dos bultos que sobresalen
     arriba; el hocico ancho, más ancho que la frente, con sus dos ollares; y una sola línea de agua, larga, de lado a lado (corta
     y al medio era una boca). La cabeza es una sola masa: el borde oscuro va detrás y el verde encima, sin línea, porque a este
     tamaño cada pieza con su trazo se volvía pura tinta (las orejas y los bultos eran aros oscuros: unas gafas). ---------- */
  const cabeza=c=>cir(c,-6.8,-6.1,1.35)+cir(c,6.8,-6.1,1.35)+cir(c,-3.1,-4.4,2.3)+cir(c,3.1,-4.4,2.3)+pth(c,'M-5 -4.4L5 -4.4L5 0L-5 0Z')+pth(c,'M-9 3.8L-9.2 1Q-9 -2.4 -5.6 -2.4L5.6 -2.4Q9 -2.4 9.2 1L9 3.8Z');
  const OJOS={
    normal:cir('v-tinta',-3.1,-4.5,1.1)+cir('v-tinta',3.1,-4.5,1.1),
    alegre:pth('v-linea','M-4.3 -3.8Q-3.1 -6 -1.9 -3.8')+pth('v-linea','M1.9 -3.8Q3.1 -6 4.3 -3.8'),
    pensativo:pth('v-linea','M-4.3 -4.3L-1.9 -4.3')+cir('v-tinta',3.1,-4,1.1)+pth('v-linea','M1.7 -6.1L4.6 -5.4'),/* un ojo entornado y la ceja del otro, levantada */
    sorpresa:cir('v-ojo',-3.1,-4.5,1.9)+cir('v-ojo',3.1,-4.5,1.9)+cir('v-tinta',-3.1,-4.5,.8)+cir('v-tinta',3.1,-4.5,.8),
    dormido:pth('v-linea','M-4.3 -4.9Q-3.1 -3.1 -1.9 -4.9')+pth('v-linea','M1.9 -4.9Q3.1 -3.1 4.3 -4.9')};
  /* la «z» del que duerme; `espejo`: dibujada al revés, para cuando el grupo que la lleva va en espejo (la barca rumbo al oeste) */
  const zeta=espejo=>pth('v-palo v-fina',espejo?'M11 -8L8.9 -8L11 -5.6L8.9 -5.6':'M8.9 -8L11 -8L8.9 -5.6L11 -5.6');
  const ollar=x=>`<ellipse class="v-tinta" cx="${x}" cy=".4" rx="1.3" ry=".9" transform="rotate(${x<0?24:-24} ${x} .4)"/>`;
  function hipoNada(animo,espejo){
    return cabeza('v-borde')+cabeza('v-hipo v-sin')
      +(OJOS[animo]||OJOS.normal)+(animo==='dormido'?zeta(espejo):'')
      +ollar(-3.8)+ollar(3.8)
      +pth('v-agua','M-10.4 4.4Q-9.1 3.1 -7.8 4.4T-5.2 4.4T-2.6 4.4T0 4.4T2.6 4.4T5.2 4.4T7.8 4.4T10.4 4.4')}

  /* ---------- qué lleva la barca ahora. Niño: la bodega del mercader (S.eco.bodega, índices de r.carga). Adulto: la carga
     narrativa del último puerto (r.paradas[S.paso-1].carga), buscando palabras. El obelisco va siempre y primero; a lo sumo
     tres, y si el texto nombra más (Luxor: goma, dátiles, lino y trigo), las tres últimas: lo recién cargado es lo que cuenta
     la parada. Vacío en el nacimiento, al llegar al mar y con «vendida». ---------- */
  const PALABRAS=[['cafe',/caf[eé]/],['marfil',/marfil/],['goma',/goma/],['datiles',/d[aá]til/],['obelisco',/obelisco/],['lino',/lino/],['trigo',/trigo/],['pescado',/pescado/]];
  function claveDe(nombre){const t=String(nombre||'').toLowerCase();for(const p of PALABRAS)if(p[1].test(t))return p[0];return null}
  function cargasDe(r){
    if(typeof S==='undefined'||!S||!r||!r.paradas)return [];
    const n=r.paradas.length,p=S.paso;if(!(p>=1&&p<=n))return [];
    let cs=[];
    if(S.eco&&S.eco.bodega){for(const gi of S.eco.bodega){const g=(r.carga||[])[gi],c=g&&claveDe(g.n);if(c)cs.push(c)}}
    else{const t=String(r.paradas[p-1].carga||'').toLowerCase();if(/vendid/.test(t))return [];
      cs=PALABRAS.map(q=>[q[0],t.search(q[1])]).filter(q=>q[1]>=0).sort((a,b)=>a[1]-b[1]).map(q=>q[0])}
    const ob=cs.indexOf('obelisco')>=0,resto=cs.filter(c=>c!=='obelisco'),cabe=ob?2:3;
    return (ob?['obelisco']:[]).concat(resto.slice(Math.max(0,resto.length-cabe)))}

  /* ---------- la hoja de contacto: todo a tamaño real y a 4×, con su nombre, sobre el verde del mar ---------- */
  const NOMBRES={cafe:'café',marfil:'marfil',goma:'goma arábiga',datiles:'dátiles',obelisco:'obelisco',lino:'lino',trigo:'trigo',pescado:'pescado seco'};
  const FALUAS=[[[],'vacía'],[['cafe'],'Jinja: café'],[['marfil'],'Juba: marfil'],[['goma'],'Jartum: goma'],[['obelisco','goma','datiles'],'Asuán: obelisco, goma y dátiles'],[['datiles','lino','trigo'],'Luxor: dátiles, lino y trigo'],
    [['cafe','pescado'],'Niño: café y pescado'],[['cafe','pescado','goma'],'Niño: café, pescado y goma'],[['goma','datiles','trigo'],'Niño: goma, dátiles y trigo'],[['pescado','pescado','trigo'],'Niño: dos pescados y trigo'],[['obelisco'],'solo el obelisco'],[['obelisco','lino'],'obelisco y lino'],[['marfil','lino'],'marfil y lino']];
  const ANIMOS=['normal','alegre','pensativo','sorpresa','dormido'];
  function hoja(){
    const svg=(g,x,y,w,h,k)=>`<svg class="v-arte" width="${w*k}" height="${h*k}" viewBox="${x} ${y} ${w} ${h}" aria-hidden="true">${g}</svg>`;
    const celda=(g,x,y,w,h,nombre)=>`<figure class="v-h-celda"><div class="v-h-duo"><span class="v-h-real">${svg(g,x,y,w,h,1)}</span>${svg(g,x,y,w,h,4)}</div><figcaption>${nombre}</figcaption></figure>`;
    const fila=(titulo,celdas)=>`<h3>${titulo}</h3><div class="v-h-fila">${celdas.join('')}</div>`;
    const escena=k=>`<svg class="v-arte" width="${170*k}" height="${48*k}" viewBox="-60 -44 170 48" aria-hidden="true"><rect class="v-h-tierra" x="-60" y="-44" width="170" height="48"/><path class="v-h-rio" d="M-60 -2Q-20 4 6 -2T70 -4T110 -8"/><g transform="translate(0 -6)">${falua(['obelisco','goma','datiles'])}</g><g transform="translate(-40 -2)">${hipoNada('normal')}</g><g transform="translate(72 -8)">${falua(['cafe','pescado','goma'])}</g><g transform="translate(46 -14)">${hipoNada('alegre')}</g></svg>`;
    return `<div class="v-hoja">${
      fila('La falúa del Nilo (52 px) · tamaño real y 4×',FALUAS.map(f=>celda(falua(f[0]),-26,-34,52,44,f[1])))}${
      fila('Las cargas (12 px) · tamaño real y 4×',CLAVES.map(c=>c==='obelisco'?celda(carga(c),-16,-12,32,12,NOMBRES[c]):celda(carga(c),-6,-12,12,12,NOMBRES[c])))}${
      fila('Hipo nadando (22 px) · tamaño real y 4×',ANIMOS.map(a=>celda(hipoNada(a),-11,-8,22,14,a)))}${
      fila('En su lugar: sobre la tierra y el río recorrido',[`<figure class="v-h-celda">${escena(1)}<figcaption>tamaño real</figcaption></figure>`,`<figure class="v-h-celda">${escena(2)}<figcaption>a 2×</figcaption></figure>`])}</div>`}

  CAPA.arte={falua,hipoNada,carga,cargasDe,hoja,claves:CLAVES};
})();
