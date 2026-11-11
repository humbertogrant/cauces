/* Bitácora de la vitrina del Nilo (rol Bitácora): las plantillas del panel de Bajar (CAPA.descender) y las acciones de su
   pie (CAPA.pie). Se carga antes que el motor: en el nivel superior solo define funciones y se registra en CAPA; todo lo
   del motor (S, P, esc, num, km, globo, postal, picto, mas, botones…) se usa dentro de ellas, que corren después.
   Los textos salen de los datos y del motor tal cual; los rótulos nuevos de interfaz están juntos en ROT. */
(function(){
  if(typeof CAPA==='undefined'||!CAPA)return;
  const ROT={marca:'Cauces',nave:'Nave',companero:'Compañero',paradas:'Paradas',proxima:'próxima',perfil:'Perfil del río',
    mar:'Llegaste al mar',ganancia:'Ganancia',antes:'La vez pasada',mercader:'El mercader',tesoro:'Tu tesoro',zarpar:'Zarpar',
    norte:'N',sur:'S',miraFrase:'Mirá la frase: así van las paradas, en orden.'};
  let ultima='';/* momento y paso del último panel: la hoja solo entra con movimiento cuando cambian */
  const momento=()=>typeof CAPA.momento==='function'?CAPA.momento():'otro';
  const TILDES=new RegExp('['+String.fromCharCode(0x300)+'-'+String.fromCharCode(0x36f)+']','g');/* los acentos sueltos, tras normalizar */
  const sinTilde=s=>String(s||'').normalize('NFD').replace(TILDES,'').toUpperCase();
  const inicial=c=>String(c.nombre||'').trim().charAt(0).toUpperCase();
  const cuenta=(r,a)=>`${a} de ${r.paradas.length} ${(r.vocab.Parada||'Parada').toLowerCase()}s`;

  /* qué paradas cubre cada inicial de la frase: una por parada, salvo cuando hay menos iniciales que paradas y varias
     seguidas empiezan igual (las «Tres [J]otas» del Nilo valen por Jinja, Juba y Jartum) */
  function cobertura(r){const partes=String(r.frase||'').split(/\[([^\]]+)\]/),nb=(partes.length-1)/2,n=r.paradas.length,cub=[];let i=0;
    for(let b=0;b<nb;b++){const L=sinTilde(partes[2*b+1]).charAt(0),ini=i;if(i<n)i++;
      while(i<n&&(n-i)>(nb-b-1)&&sinTilde(inicial(r.paradas[i]))===L)i++;
      cub.push([ini,i-1])}
    return{partes,cub}}
  /* la frase que se va completando: con a paradas alcanzadas, hasta la palabra de la última inicial ganada */
  function fraseHasta(r,a){const n=r.paradas.length;if(!r.frase||a<=0)return '';if(a>=n)return marcarFrase(r.frase);
    const{partes,cub}=cobertura(r),k=cub.findIndex(c=>a-1>=c[0]&&a-1<=c[1]);if(k<0)return '';
    let h=esc(partes[0]);
    for(let b=0;b<=k;b++){const sig=partes[2*b+2]||'',pal=(sig.match(/^\S*/)||[''])[0];
      h+=`<b>${esc(partes[2*b+1])}</b>${esc(pal)}`;if(b<k||a-1===cub[b][1])h+=esc(sig.slice(pal.length))}
    return h.replace(/\s+$/,'')+'…'}
  /* las fichas del acróstico: llenas las alcanzadas, «?» la que sigue y punteadas las demás (sin nombres futuros) */
  function fichas(r,a,conProxima,nueva){const n=r.paradas.length;let h=`<div class="v-fichas" role="list" aria-label="${esc(cuenta(r,Math.min(a,n)))}">`;
    for(let i=0;i<n;i++){const c=r.paradas[i];
      if(i<a)h+=`<span class="v-ficha llena${nueva&&i===a-1?' nueva':''}" data-i="${i}" role="listitem"><b>${esc(inicial(c))}</b><small>${esc(c.nombre)}</small></span>`;
      else if(i===a&&conProxima)h+=`<span class="v-ficha proxima" data-i="${i}" role="listitem"><b>?</b><small>${ROT.proxima}</small></span>`;
      else h+=`<span class="v-ficha vacia" data-i="${i}" role="listitem" aria-hidden="true"><b></b><small></small></span>`}
    return h+'</div>'}
  /* el perfil del motor en un contenedor propio; sin los <title> de cada punto, que nombran paradas futuras. Los rótulos de
     altura van siempre encima de la línea (la de la fuente y la de «aquí», que el motor ponía debajo cerca de la fuente):
     la línea baja hacia la derecha y los tachaba */
  function perfil(r){if(!r.perfil||typeof perfilSVG!=='function')return '';const A=r.perfil;
    return `<div class="v-perfil"><div class="v-perfil-cab"><span class="v-rotulo">${ROT.perfil}</span><span class="v-nota">de ${num(km(A[0][1])+' m')} en la fuente a ${num(km(A[A.length-1][1])+' m')} en el mar</span></div><div class="v-perfil-svg">${perfilSVG(r).replace(/<title>[^<]*<\/title>/g,'').replace(/(<text class="perfil-txt" x="[0-9.]+") y="[0-9.]+">/,'$1 y="-3">').replace(/(class="perfil-aqui" cx="[0-9.]+" cy="([0-9.]+)"[^>]*>)(<text class="perfil-txt" x="[0-9.]+") y="([0-9.]+)"/,(t,c,cy,tx,y)=>+y>+cy?`${c}${tx} y="${(+cy-8).toFixed(1)}"`:t)}</div></div>`}
  const pintada=(r,i,pictos)=>(typeof postal==='function'&&postal(r.id,i))||(typeof escena==='function'&&pictos?escena(pictos):'');
  /* la cita con que abre el texto de la primera capa de contexto («…», escribió Fulano: …); si no abre así, no hay cita */
  function cita(r){const t=r.contexto&&r.contexto[0]&&r.contexto[0].texto,m=t&&/^«([^»]+)»,\s*escribió\s+([^:.,;]+)/.exec(t);return m?{texto:m[1],autor:m[2].trim()}:null}
  /* el riel de etapas del motor (Bajar · Ordenar · Recitar · Preguntar) dentro de la hoja, solo donde el motor no lo deja en
     el pie: en el teléfono lo manda a #rielArriba, que en Bajar está oculto, y sin él no hay cómo ir a Recitar o a Preguntar */
  const riel=r=>typeof renderRiel==='function'&&typeof telefono==='function'&&telefono()?`<div class="v-riel">${renderRiel(r)}</div>`:'';
  /* cuánto alto piden la hoja y el pie en esta pantalla: se mide la hoja dentro de #panel antes de entregarla (el pie ya
     está dibujado cuando el motor arma el panel, y el mapa se mide después) y va en --v-resto, en body; panel.css le deja
     al mapa lo demás (en la portada y navegando, donde todo tiene que verse sin desplazar). 18 de margen de la hoja, 16 de
     aire sobre el pie y los 22 que la hoja pisa del mapa. Con el DOM simulado no hace nada; devuelve la misma hoja */
  function resto(html){try{if(typeof document==='undefined'||typeof document.createElement!=='function'||!document.getElementById)return html;
      const b=document.body,p=document.getElementById('panel'),pie=document.getElementById('pie');
      if(!b||!b.style||typeof b.style.setProperty!=='function'||!p||typeof p.appendChild!=='function'||typeof p.removeChild!=='function')return html;
      const d=document.createElement('div');if(!d||!d.style)return html;d.style.cssText='visibility:hidden;pointer-events:none';d.innerHTML=html;p.appendChild(d);
      const h=d.offsetHeight||0,hp=pie&&!pie.hidden?(pie.offsetHeight||0):0;p.removeChild(d);
      if(h>0)b.style.setProperty('--v-resto',Math.round(h+hp+18+16-22)+'px')}catch(e){}
    return html}
  /* ¿hay columna con alto de sobra (820 px o más de ancho y no un teléfono acostado)? Ahí la portada puede llevar más */
  const holgada=()=>typeof window!=='undefined'&&typeof window.matchMedia==='function'&&window.matchMedia('(min-width:820px) and (min-height:600px)').matches;
  /* lo que el motor dice en «Tu embarcación» al zarpar: con qué zarpás y a quién hay que ganarle */
  const zarpe=r=>r.vehiculo?`<p class="v-zarpe">${S.eco?r.vocab.zarpas+rival(r.vocab,S.eco):esc(r.vehiculo.zarpe)}</p>`:'';

  /* el sello de la bitácora: circular, con el primer pictograma de la ciudad, su nombre y su latitud redondeada (de c.pos).
     Pendiente: punteado, sin tinta. Ganado: tinta verde. Dorado (selloOro): la tinta ocre del motor. Recién ganado: cae */
  function selloV(r,i,cae){const c=r.paradas[i],ts=sellos()[claveSello(r,i)];
    if(!ts)return `<svg class="v-sello pendiente" viewBox="0 0 84 84" role="img" aria-label="Sin sello"><circle class="aro" cx="42" cy="42" r="38"/></svg>`;
    const oro=selloOro(r,i),pc=c.escena&&typeof picto==='function'&&picto(c.escena[0]),nom=String(c.nombre).toUpperCase(),la=Array.isArray(c.pos)?+c.pos[0]:NaN;
    /* cerca del ecuador los grados redondeados dan 0: ahí van grados y minutos (Jinja, 0,42°: «0° 25′ N») */
    const gr=Math.round(Math.abs(la)),lat=isFinite(la)?`${gr?gr+'°':'0° '+Math.round(Math.abs(la)*60)+'′'} ${la<0?ROT.sur:ROT.norte}`:'',giro=((i*5)%11)-5;
    return `<svg class="v-sello${oro?' oro':''}${cae?' nuevo':''}" viewBox="0 0 84 84" style="--v-giro:${giro}deg" role="img" aria-label="Sello de ${esc(c.nombre)}"><circle class="borde" cx="42" cy="42" r="40"/><circle class="aro" cx="42" cy="42" r="35"/>${pc?`<svg class="pic" x="30" y="10" width="24" height="24" viewBox="${pc.vb}">${pc.svg}</svg>`:''}<text class="nom" x="42" y="50" text-anchor="middle"${nom.length>8?' textLength="60" lengthAdjust="spacingAndGlyphs"':''}>${esc(nom)}</text><line class="raya" x1="27" y1="55.5" x2="57" y2="55.5"/><text class="lat${gr?"":" min"}" x="42" y="69" text-anchor="middle">${lat}</text></svg>`}

  function portada(r,entra){const V=r.vocab,n=r.paradas.length,g=globo(r,S.dicho||(r.companero&&r.companero.hola)),q=cita(r);
    /* donde hay columna holgada, lo que el motor cuenta en el nacimiento sin nombrar paradas: la embarcación (con con qué
       zarpás y a quién hay que ganarle) y la ficha del compañero; en el teléfono acostado, solo la línea de zarpe */
    const ancho=holgada()?`${r.vehiculo?`<div class="nave">${(typeof laminaNave==='function'&&laminaNave(r))||`<svg class="barca mini" viewBox="-15 -15 30 20" aria-hidden="true">${glifo(r.vehiculo.tipo)}</svg>`}<div class="fkicker">${V.tuVehiculo}</div><div class="ntit">${esc(r.vehiculo.nombre)}</div><p>${esc(r.vehiculo.desc)}</p><div class="fnota">${S.eco?V.zarpas+rival(V,S.eco):esc(r.vehiculo.zarpe)}</div></div>`:''}${typeof fichaAnimal==='function'?fichaAnimal(r):''}`:zarpe(r);
    return resto(`<div class="v-portada"><div class="v-marca">${ROT.marca}</div><h2 class="v-rio">${esc(r.nombre)}</h2><p class="v-cab">${V.cabecera(r)}</p>${q?`<blockquote class="v-cita"><p>«${esc(q.texto)}»</p><cite>${esc(q.autor)}</cite></blockquote>`:''}</div>
<div class="v-bit${entra}" data-v="portada">${g}${g?'':botonVoz()}<dl class="v-datos">${r.vehiculo?`<div class="v-dato"><dt>${ROT.nave}</dt><dd>${esc(r.vehiculo.nombre)}</dd></div>`:''}${r.companero?`<div class="v-dato"><dt>${ROT.companero}</dt><dd>${esc(r.companero.nombre)}</dd></div>`:''}<div class="v-dato"><dt>${ROT.paradas}</dt><dd>${n}</dd></div></dl><div class="v-ancho">${ancho}</div>${riel(r)}</div>`)}

  function navega(r,entra){const V=r.vocab,a=S.paso,g0=S.guias&&S.guias[a],primera=!S.zarpo&&a===0;
    /* antes de zarpar en la primera bajada, Hipo señala la frase con la lista (todavía no hay fichas para responder); luego,
       antes de responder, pregunta; después, dice lo que el motor le hace decir (acierto, o «Era …: …») */
    const g=globo(r,primera?ROT.miraFrase:((g0&&g0.resp!=null&&S.dicho)||V.proxima));
    /* en la primera bajada, antes de zarpar, la frase con la lista (enseñar antes de preguntar) en lugar de las fichas */
    const arriba=primera?bloqueFrase(r,true):`<div class="v-avance"><div class="v-frase">${fraseHasta(r,a)}</div><div class="v-rotulo">${botonVoz()}${cuenta(r,a)}</div></div>${fichas(r,a,true,!!entra)}`;
    /* la hoja se mide: con la guía respondida el pie crece y, si salió mal, Hipo explica en varios renglones («Era …: …») */
    return resto(`<div class="v-bit${entra}" data-v="navega">${arriba}${g}${a===0?zarpe(r):''}${perfil(r)}</div>`)}

  function parada(r,entra){const V=r.vocab,n=r.paradas.length,p=S.paso,c=r.paradas[p-1],prev=p>1?r.paradas[p-2]:null,k=claveSello(r,p-1);
    const g=globo(r,S.dicho||((S.selloNuevo===k?`¡Sello de ${c.nombre}! `:'')+(r.companero?r.companero.paradas[p-1]:'')));
    /* el texto del motor sobre el sello (recién ganado, ya en el pasaporte o «te espera»), sin su dibujo */
    const ns=renderSello(r,p-1),nota=(/<\/svg><div>([\s\S]*)<\/div><\/div>\s*$/.exec(ns)||[])[1]||'';
    /* del rótulo del motor («Parada 4 de 6 · km ≈5 297 de 6 650»), aquí la primera parte; el kilómetro va en la píldora */
    const kp=String(V.kickerParada(r,p,n,c)),ik=kp.indexOf(' · '),rotulo=ik>=0?kp.slice(0,ik):kp;
    return `<div class="v-bit${entra}" data-v="parada"><div class="v-cabeza"><div><p class="kicker">${botonVoz()}${rotulo}</p><h2 class="v-ciudad">${esc(c.nombre)}</h2><div class="pais">${esc(c.pais)} · ${V.tramo(r,c,prev)}${textoAltura(r,p-1)}</div></div>${selloV(r,p-1,!!entra&&S.selloNuevo===k)}</div>${g}${S.hoyListo?`<p class="aviso-hoy">${ico('ok')} ¡Dos ${V.Parada.toLowerCase()}s nuevas! ${r.tipo==='rio'?'Si querés, la barca se queda anclada aquí hasta mañana.':'Si querés, mañana seguimos desde aquí.'}</p>`:''}${S.anclada?`<p class="aviso-hoy"><button class="enlace" onclick="abrirRio('${r.id}',1)">Empezar de nuevo desde ${V.entreInicio}</button></p>`:''}<div class="ficha recuerdo v-recuerdo">${pintada(r,p,c.escena)}<div class="cuerpo"><div class="imagen"><div class="fkicker">Imagen para recordar</div>${esc(c.imagen)}</div></div></div>${mas('Contame más',`<p>${esc(c.dato)}</p>`)}${nota?`<p class="v-sello-nota">${nota}</p>`:''}${!S.eco&&c.puerto?`<div class="puerto"><div class="fkicker">${V.enPuerto}</div><p>${esc(c.puerto)}</p><div class="bodega">${V.llevaba}: ${esc(c.carga)}</div></div>`:''}${renderMercado(r,p-1)}</div>`}

  function mar(r,entra){const V=r.vocab,n=r.paradas.length,f=S.eco&&S.eco.final,g=globo(r,S.dicho||(r.companero&&r.companero.fin),'',S.dicho?(S.animo||'alegre'):'dormido');/* dormido solo si no tiene nada que contar de la bajada */
    const cifra=(t,v)=>`<div class="v-cifra"><dt>${t}</dt><dd>${v}</dd></div>`;
    const cuentas=f?`<div class="v-cuentas"><div class="fkicker">Cuentas del viaje</div><dl class="v-cifras">${f.gan>0?cifra(ROT.ganancia,'+'+f.gan):''}${S.eco.antes!=null?cifra(ROT.antes,S.eco.antes):''}${S.eco.fantasma!=null?cifra(ROT.mercader,S.eco.fantasma):''}${cifra(ROT.tesoro,km(P.tesoro||0))}</dl><p class="v-cuenta">${V.cuentas} ${f.fin}.${f.vend.length?` ${V.sobrante} ${esc(r.paradas[n-1].nombre)}: ${esc(f.vend.join(', '))}.`:''}${f.gan>0?'':' Sin ganancia esta vez.'}</p><div class="bolsa">${ico('moneda')} ${rango(P.tesoro||0)}</div></div>`:'';
    return `<div class="v-bit${entra}" data-v="mar"><p class="kicker">${botonVoz()}${ROT.mar} · ${cuenta(r,n)}</p><h2 class="v-titulo">${marcarFrase(r.frase)}</h2>${fichas(r,n,false,false)}${g}${r.vehiculo?`<p class="v-llegada">${esc(r.vehiculo.llegada)}</p>`:''}${cuentas}<div class="ficha recuerdo v-recuerdo">${pintada(r,n+1,r.fin.escena)}<div class="cuerpo"><p>${esc(V.llegada(r))}</p></div></div>${r.contexto&&r.contexto[1]?mas(V.contame(r.contexto[1]),`<p>${esc(r.contexto[1].texto)}</p>`,r.contexto[1].titulo):''}${riel(r)}</div>`}

  /* el panel de Bajar según el momento; null deja el del motor (también si algo falla: la bitácora no rompe el juego) */
  CAPA.descender=function(r){const m=momento();if(!r||!r.paradas||m==='otro'||!m||typeof S==='undefined')return null;
    const n=r.paradas.length,p=S.paso,clave=m+':'+p,entra=clave!==ultima?' v-entra':'';
    try{let h=null;
      if(p>n)h=m==='mar'?mar(r,entra):null;
      else if(m==='navega'&&p<n)h=navega(r,entra);
      else if(m==='portada'&&p===0)h=portada(r,entra);
      else if(m==='parada'&&p>=1)h=parada(r,entra);
      if(h!=null)ultima=clave;return h}
    catch(e){if(typeof console!=='undefined'&&console.warn)console.warn('Bitácora:',e);return null}};

  /* de la guía, de vuelta a la hoja de la misma parada (su mercado, su imagen): el «‹ Atrás» del motor es paso(-1) y se
     llevaba la barca a la parada anterior, sin forma de volver al mercado que se acababa de dejar */
  CAPA.aParada=function(){CAPA.fase='parada';if(typeof render==='function')render(false);if(typeof window!=='undefined'&&typeof window.scrollTo==='function')window.scrollTo(0,0)};

  /* las acciones del pie: «Zarpar» lleva a la guía (CAPA.navegar); en la guía, lo del motor, con su «‹ Atrás» de vuelta
     a la hoja de la parada; en lo demás, lo del motor */
  CAPA.pie=function(r,porDefecto){const m=momento();if(!r||!r.paradas||typeof S==='undefined')return porDefecto;
    const n=r.paradas.length,p=S.paso,z=`<button class="btn v-zarpar" onclick="CAPA.navegar()">${ROT.zarpar}</button>`;
    try{if(m==='portada'&&p===0)return botones('',z);
      if(m==='parada'&&p>=1&&p<n)return botones(`<button class="enlace" onclick="paso(-1)">‹ Atrás</button>`,z);
      if(m==='navega'&&p>=1&&typeof porDefecto==='string')return porDefecto.split('onclick="paso(-1)"').join('onclick="CAPA.aParada()"')}
    catch(e){}
    return porDefecto};

  /* al final de cada render (evento «dibujado»): en la píldora, el kilómetro del rótulo del motor en lugar de la cabecera
     larga, y un nombre accesible para el botón de sonido. Con el DOM simulado de las pruebas no hace nada */
  /* los rótulos del perfil: el dibujo se escala con la hoja (y su ancho de dibujo cambia con la pantalla), así que se mide
     cuánto mide en pantalla y se pasa a --v-pfs la letra que da 12 px de verdad, en cualquier ancho */
  function ajustarPerfil(){try{const p=document.getElementById('panel'),sv=p&&typeof p.querySelector==='function'&&p.querySelector('.v-perfil svg');if(!sv||!sv.viewBox||!sv.viewBox.baseVal)return;
      const w=sv.getBoundingClientRect().width,W=sv.viewBox.baseVal.width;if(w>0&&W>0)sv.style.setProperty('--v-pfs',(12*W/w).toFixed(2)+'px')}catch(e){}}
  function dibujado(){if(typeof document==='undefined'||!document.getElementById||typeof S==='undefined')return;ajustarPerfil();
    const cab=document.getElementById('cab');if(!cab||typeof cab.querySelector!=='function')return;
    const son=cab.querySelector('.son');if(son&&son.setAttribute&&typeof VJ==='function')son.setAttribute('aria-label',VJ().sonido);
    const m=momento();if(m!=='navega'&&m!=='parada'&&m!=='mar'&&m!=='evento')return;/* en un evento queda el kilómetro de la parada de donde se zarpó */
    const r=typeof rioPor==='function'&&rioPor(S.rio),sub=cab.querySelector('.sub');if(!r||!r.paradas||!sub)return;
    const V=r.vocab,n=r.paradas.length,p=S.paso,k=String(p>n?V.kickerFin(r):p>=1?V.kickerParada(r,p,n,r.paradas[p-1]):V.kickerInicio(r)),i=k.indexOf(' · ');
    if(i>=0)sub.innerHTML=k.slice(i+3)}

  /* vuelve a medir la hoja que ya está en pantalla y le pide al motor que reencuadre el mapa: cuando llegan las fuentes
     (la primera pantalla se mide con las del sistema y el texto puede partirse distinto) o cuando cambia el ancho */
  CAPA.remedir=function(){try{const m=momento();if(m!=='portada'&&m!=='navega')return;
      if(typeof document==='undefined'||!document.getElementById)return;ajustarPerfil();
      const b=document.body,p=document.getElementById('panel'),pie=document.getElementById('pie');
      if(!b||!b.style||typeof b.style.setProperty!=='function'||!p||typeof p.querySelector!=='function')return;
      const el=p.querySelector('.v-bit'),h=el?(el.offsetHeight||0):0,hp=pie&&!pie.hidden?(pie.offsetHeight||0):0;if(!h)return;
      b.style.setProperty('--v-resto',Math.round(h+hp+18+16-22)+'px');
      if(typeof renderMapa==='function'&&typeof S!=='undefined'&&S.foco)renderMapa(S.foco,true)}catch(e){}};
  /* se engancha una sola vez, en el primer «dibujado» (al cargar no se toca el navegador) */
  let enganchado=false;
  function enganchar(){if(enganchado||typeof document==='undefined'||typeof window==='undefined')return;enganchado=true;
    try{const f=document.fonts;if(f&&f.ready&&typeof f.ready.then==='function')f.ready.then(function(){CAPA.remedir()})}catch(e){}
    try{if(typeof window.addEventListener==='function'){let ancho=window.innerWidth,t=0;
      window.addEventListener('resize',function(){if(window.innerWidth===ancho)return;ancho=window.innerWidth;clearTimeout(t);t=setTimeout(function(){CAPA.remedir()},180)})}}catch(e){}}
  if(typeof CAPA.oir==='function')CAPA.oir('dibujado',function(){try{enganchar();dibujado()}catch(e){}});
})();
