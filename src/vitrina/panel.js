/* Bitácora de la vitrina del Nilo (rol Bitácora): las plantillas del panel de Bajar (CAPA.descender) y las acciones de su
   pie (CAPA.pie). Se carga antes que el motor: en el nivel superior solo define funciones y se registra en CAPA; todo lo
   del motor (S, P, esc, num, km, globo, postal, sello, mas, botones…) se usa dentro de ellas, que corren después.
   Los textos salen de los datos y del motor tal cual; los rótulos nuevos de interfaz están juntos en ROT. */
(function(){
  if(typeof CAPA==='undefined'||!CAPA)return;
  const ROT={marca:'Cauces',nave:'Nave',companero:'Compañero',paradas:'Paradas',proxima:'próxima',perfil:'Perfil del río',
    mar:'Llegaste al mar',ganancia:'Ganancia',antes:'La vez pasada',mercader:'El mercader',tesoro:'Tu tesoro',zarpar:'Zarpar'};
  let ultima='';/* momento y paso del último panel: la hoja solo entra con movimiento cuando cambian */
  const momento=()=>typeof CAPA.momento==='function'?CAPA.momento():'otro';
  const sinTilde=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase();
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
  /* el perfil del motor en un contenedor propio; sin los <title> de cada punto, que nombran paradas futuras */
  function perfil(r){if(!r.perfil||typeof perfilSVG!=='function')return '';const A=r.perfil;
    return `<div class="v-perfil"><div class="v-perfil-cab"><span class="v-rotulo">${ROT.perfil}</span><span class="v-nota">de ${num(km(A[0][1])+' m')} en la fuente a ${num(km(A[A.length-1][1])+' m')} en el mar</span></div><div class="v-perfil-svg">${perfilSVG(r).replace(/<title>[^<]*<\/title>/g,'')}</div></div>`}
  const pintada=(r,i,pictos)=>(typeof postal==='function'&&postal(r.id,i))||(typeof escena==='function'&&pictos?escena(pictos):'');
  /* la cita con que abre el texto de la primera capa de contexto («…», escribió Fulano: …); si no abre así, no hay cita */
  function cita(r){const t=r.contexto&&r.contexto[0]&&r.contexto[0].texto,m=t&&/^«([^»]+)»,\s*escribió\s+([^:.,;]+)/.exec(t);return m?{texto:m[1],autor:m[2].trim()}:null}

  function portada(r,entra){const V=r.vocab,n=r.paradas.length,g=globo(r,S.dicho||(r.companero&&r.companero.hola)),q=cita(r);
    return `<div class="v-portada"><div class="v-marca">${ROT.marca}</div><h2 class="v-rio">${esc(r.nombre)}</h2><p class="v-cab">${V.cabecera(r)}</p>${q?`<blockquote class="v-cita"><p>«${esc(q.texto)}»</p><cite>${esc(q.autor)}</cite></blockquote>`:''}</div>
<div class="v-hoja${entra}" data-v="portada">${g}${g?'':botonVoz()}<dl class="v-datos">${r.vehiculo?`<div class="v-dato"><dt>${ROT.nave}</dt><dd>${esc(r.vehiculo.nombre)}</dd></div>`:''}${r.companero?`<div class="v-dato"><dt>${ROT.companero}</dt><dd>${esc(r.companero.nombre)}</dd></div>`:''}<div class="v-dato"><dt>${ROT.paradas}</dt><dd>${n}</dd></div></dl></div>`}

  function navega(r,entra){const V=r.vocab,a=S.paso,g0=S.guias&&S.guias[a],primera=!S.zarpo&&a===0;
    /* antes de responder, Hipo pregunta; después, dice lo que el motor le hace decir. En la primera bajada, saluda */
    const g=globo(r,primera?(S.dicho||(r.companero&&r.companero.hola)):(g0&&g0.resp!=null&&S.dicho)||V.proxima);
    const arriba=primera?bloqueFrase(r,true):`<div class="v-avance"><div class="v-frase">${fraseHasta(r,a)}</div><div class="v-rotulo">${botonVoz()}${cuenta(r,a)}</div></div>${fichas(r,a,true,!!entra)}`;
    /* al zarpar de la fuente, lo que el motor dice en «Tu embarcación»: con qué zarpás y a quién hay que ganarle */
    const zarpe=a===0&&r.vehiculo?`<p class="v-zarpe">${S.eco?V.zarpas+rival(V,S.eco):esc(r.vehiculo.zarpe)}</p>`:'';
    return `<div class="v-hoja${entra}" data-v="navega">${arriba}${g}${zarpe}${perfil(r)}</div>`}

  function parada(r,entra){const V=r.vocab,n=r.paradas.length,p=S.paso,c=r.paradas[p-1],prev=p>1?r.paradas[p-2]:null,k=claveSello(r,p-1);
    const g=globo(r,S.dicho||((S.selloNuevo===k?`¡Sello de ${c.nombre}! `:'')+(r.companero?r.companero.paradas[p-1]:'')));
    const ns=renderSello(r,p-1),nota=(/<\/svg><div>([\s\S]*)<\/div><\/div>\s*$/.exec(ns)||[])[1]||'';
    return `<div class="v-hoja${entra}" data-v="parada"><div class="v-cabeza"><div><p class="kicker">${botonVoz()}${V.kickerParada(r,p,n,c)}</p><h2 class="v-ciudad">${esc(c.nombre)}</h2><div class="pais">${esc(c.pais)} · ${V.tramo(r,c,prev)}${textoAltura(r,p-1)}</div></div>${sello(r,p-1,S.selloNuevo===k?' nuevo':'')}</div>${g}${S.hoyListo?`<p class="aviso-hoy">${ico('ok')} ¡Dos ${V.Parada.toLowerCase()}s nuevas! ${r.tipo==='rio'?'Si querés, la barca se queda anclada aquí hasta mañana.':'Si querés, mañana seguimos desde aquí.'}</p>`:''}${S.anclada?`<p class="aviso-hoy"><button class="enlace" onclick="abrirRio('${r.id}',1)">Empezar de nuevo desde ${V.entreInicio}</button></p>`:''}<div class="ficha recuerdo v-recuerdo">${pintada(r,p,c.escena)}<div class="cuerpo"><div class="imagen"><div class="fkicker">Imagen para recordar</div>${esc(c.imagen)}</div></div></div>${mas('Contame más',`<p>${esc(c.dato)}</p>`)}${nota?`<p class="v-sello-nota">${nota}</p>`:''}${!S.eco&&c.puerto?`<div class="puerto"><div class="fkicker">${V.enPuerto}</div><p>${esc(c.puerto)}</p><div class="bodega">${V.llevaba}: ${esc(c.carga)}</div></div>`:''}${renderMercado(r,p-1)}</div>`}

  function mar(r,entra){const V=r.vocab,n=r.paradas.length,f=S.eco&&S.eco.final,g=globo(r,S.dicho||(r.companero&&r.companero.fin),'','dormido');
    const cifra=(t,v)=>`<div class="v-cifra"><dt>${t}</dt><dd>${v}</dd></div>`;
    const cuentas=f?`<div class="v-cuentas"><div class="fkicker">Cuentas del viaje</div><dl class="v-cifras">${f.gan>0?cifra(ROT.ganancia,'+'+f.gan):''}${S.eco.antes!=null?cifra(ROT.antes,S.eco.antes):''}${S.eco.fantasma!=null?cifra(ROT.mercader,S.eco.fantasma):''}${cifra(ROT.tesoro,km(P.tesoro||0))}</dl><p class="v-cuenta">${V.cuentas} ${f.fin}.${f.vend.length?` ${V.sobrante} ${esc(r.paradas[n-1].nombre)}: ${esc(f.vend.join(', '))}.`:''}${f.gan>0?'':' Sin ganancia esta vez.'}</p><div class="bolsa">${ico('moneda')} ${rango(P.tesoro||0)}</div></div>`:'';
    return `<div class="v-hoja${entra}" data-v="mar"><p class="kicker">${botonVoz()}${ROT.mar} · ${cuenta(r,n)}</p><h2 class="v-titulo">${marcarFrase(r.frase)}</h2>${fichas(r,n,false,false)}${g}${r.vehiculo?`<p class="v-llegada">${esc(r.vehiculo.llegada)}</p>`:''}${cuentas}<div class="ficha recuerdo v-recuerdo">${pintada(r,n+1,r.fin.escena)}<div class="cuerpo"><p>${esc(V.llegada(r))}</p></div></div>${r.contexto&&r.contexto[1]?mas(V.contame(r.contexto[1]),`<p>${esc(r.contexto[1].texto)}</p>`,r.contexto[1].titulo):''}</div>`}

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

  /* las acciones del pie: «Zarpar» lleva a la guía (CAPA.navegar); en lo demás, lo del motor */
  CAPA.pie=function(r,porDefecto){const m=momento();if(!r||!r.paradas||typeof S==='undefined')return porDefecto;
    const n=r.paradas.length,p=S.paso,z=`<button class="btn v-zarpar" onclick="CAPA.navegar()">${ROT.zarpar}</button>`;
    try{if(m==='portada'&&p===0)return botones('',z);
      if(m==='parada'&&p>=1&&p<n)return botones(`<button class="enlace" onclick="paso(-1)">‹ Atrás</button>`,z)}
    catch(e){}
    return porDefecto};

  /* al final de cada render (evento «dibujado»): en la píldora, el kilómetro del rótulo del motor en lugar de la cabecera
     larga, y un nombre accesible para el botón de sonido. Con el DOM simulado de las pruebas no hace nada */
  function dibujado(){if(typeof document==='undefined'||!document.getElementById||typeof S==='undefined')return;
    const cab=document.getElementById('cab');if(!cab||typeof cab.querySelector!=='function')return;
    const son=cab.querySelector('.son');if(son&&son.setAttribute&&typeof VJ==='function')son.setAttribute('aria-label',VJ().sonido);
    const m=momento();if(m!=='navega'&&m!=='parada'&&m!=='mar'&&m!=='evento')return;/* en un evento queda el kilómetro de la parada de donde se zarpó */
    const r=typeof rioPor==='function'&&rioPor(S.rio),sub=cab.querySelector('.sub');if(!r||!r.paradas||!sub)return;
    const V=r.vocab,n=r.paradas.length,p=S.paso,k=String(p>n?V.kickerFin(r):p>=1?V.kickerParada(r,p,n,r.paradas[p-1]):V.kickerInicio(r)),i=k.indexOf(' · ');
    if(i>=0)sub.innerHTML=k.slice(i+3)}
  if(typeof CAPA.oir==='function')CAPA.oir('dibujado',function(){try{dibujado()}catch(e){}});
})();
