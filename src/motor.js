const $=s=>document.querySelector(s);
const azar=a=>a[Math.floor(Math.random()*a.length)];
const mezclar=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const rutaPor=id=>RUTAS.find(r=>r.id===id),rioPor=rutaPor;/* «rio» en un identificador quiere decir «ruta»: el motor juega rutas de paradas (ver docs/itinerarios.md) */
const ZONAS=JUEGO.zonas||{};/* JUEGO viene de src/juegos/<juego>.js, cargado antes del motor */const zonaDe=r=>r.zona||'mundo';
/* interruptor Niño/Adulto: P.modo 'mercader' = Niño (mercado, animal, textos plegados, lee sola), 'historia' = Adulto */
let GLOBO=false;const esNino=()=>modo()==='mercader';const mas=(titulo,html,h3)=>esNino()?`<details class="mas"><summary>${titulo}</summary>${html}</details>`:`${h3?`<h3>${h3}</h3>`:''}${html}`;
const htmlVoz=()=>voz.soporte()?`<button class="voz${voz.hablando?' on':''}" onclick="voz.leer()" aria-pressed="${voz.hablando}" aria-label="Escuchar en voz alta" title="Escuchar">🔊</button>`:'';
const botonVoz=()=>GLOBO?'':htmlVoz();
const leeSola=()=>esNino()&&P.voz!=='boton'&&voz.soporte();
function setVoz(v){P.voz=v;guardar();render(false)}
function dichoActual(){if(S.pantalla==='quiz')return S.quiz&&S.quiz.resp!=null?S.quiz.dicho:null;if(S.pantalla!=='rio')return null;const r=rioPor(S.rio);
  if(S.tab==='descender'){const E=S.evento;if(E)return E.resp!=null?(E.ok?E.def.bien:E.def.mal):E.dicho;return S.dicho}
  if(S.tab==='ordenar')return S.orden&&S.orden.dicho;
  if(S.tab==='recitar'){const R=S.rec;if(!R)return null;return R.revelada&&R.i<r.paradas.length?r.paradas[R.i].nombre:R.dicho}
  return S.quiz&&S.quiz.dicho}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const km=n=>String(n).replace(/\B(?=(\d{3})+(?!\d))/g,' ');
const marcarFrase=f=>esc(f).replace(/\[([^\]]+)\]/g,'<b>$1</b>');
const fraseLimpia=f=>f.replace(/[\[\]]/g,'');
const lista=r=>r.paradas.map(c=>c.nombre).join(' → ');
const oculta=s=>s.split(' ').map(w=>w[0]+'_'.repeat(Math.max(1,w.length-1))).join(' ');
const sinNombre=(t,n)=>t.replace(new RegExp(n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'),'___');
const sinHtml=s=>String(s).replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
Object.assign(VOCES,{
  guiaBien:["¡Esa! Zarpamos hacia {c}.","Sí, {c}. Yo también me acordaba.","¡Exacto! Rumbo a {c}."],
  guiaMal:["Nop, era {c}. Vamos igual, pero ahí solo vas a poder vender.","Casi. La siguiente es {c}; en ese puerto no vas a poder comprar."],
  guiaMalH:["Nop, era {c}. Vamos igual.","Casi: la siguiente es {c}."],
  recitarInicio:["Decí cada parada antes de revelarla. Yo no soplo.","Cerrá los ojos si querés: el río ya está en tu cabeza."],
  recitarBien:["¡Esa sí!","¡Claro que sí!","Ya la tenés."],
  recitarMal:["Esa se nos escapó.","La próxima vez sale.","Mirá la imagen otra vez."],
  recitarFin:["¡Todas! Ya podés bajar con menos pista.","Casi todas. Otra vuelta y sale.","Volvamos a bajar el río juntos."],
  fantasma:["¡Le ganaste al mercader de la ruta!","El mercader de la ruta llegó con {n}; la próxima le ganás.","Empataste con el mercader de la ruta."],
  eventoAviso:["¡Ojo! El río nos puso una prueba.","¡Alto ahí! Esto se pasa recordando.","Tranquilo: esto lo sabemos."],
  eventoBien:["¡Eso era! Seguimos.","¡Bien ahí! El río nos deja pasar.","¡Lo sabías! Adelante."],
  eventoMal:["No pasa nada: ya viste la respuesta y seguimos.","Casi. Guardá la respuesta para la próxima.","Otro día nos sale. ¡A seguir!"]
});
function fantasma(r){const n=r.paradas.length;let monedas=10,bodega=[];
  for(let j=0;j<n;j++){bodega=bodega.filter(gi=>{const g=r.carga[gi],k=j-g.o;if(j===n-1||(g.d&&k>=g.d)){monedas+=precio(r,g,j)||0;return false}return true});
    if(j<n-1){const oferta=r.carga.map((g,gi)=>({g,gi})).filter(x=>x.g.o===j).map(x=>{const g=x.g,jv=g.d?Math.min(n-1,j+g.d):n-1;return{...x,gan:(precio(r,g,jv)||0)-g.b}}).filter(x=>x.gan>0).sort((a,b)=>b.gan-a.gan);
      for(const x of oferta)while(bodega.length<3&&monedas>=x.g.b){monedas-=x.g.b;bodega.push(x.gi)}}}
  return monedas}
document.getElementById('tierra').setAttribute('d',LAND);document.getElementById('lagos').setAttribute('d',LAGOS);document.getElementById('fronteras').setAttribute('d',BORDES);
const hav=(a,b)=>{const R=6371,toR=x=>x*Math.PI/180,dl=toR(b[0]-a[0]),dn=toR(b[1]-a[1]),q=Math.sin(dl/2)**2+Math.cos(toR(a[0]))*Math.cos(toR(b[0]))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(q))};
/* ---------- rutas: el motor juega rutas de paradas (tipo rio | derrota | itinerario). VOCAB da las palabras de cada tipo;
   desdeRio(r) convierte un río de rios.js (más NAVES, MASCOTAS, MERCADOS, EVENTOS, ALTURAS) al esquema RUTA sobre el mismo
   objeto, dejando los campos viejos como alias para los datos y las pruebas; normalizar(r) calcula lo derivado (acum, kmPoly,
   idx y km de cada parada, mercader fantasma, vocabulario efectivo). Esquema y migración: docs/itinerarios.md ---------- */
const cap=t=>t[0].toUpperCase()+t.slice(1);
const VOCAB={
  rio:{tipo:'río',tipos:'ríos',Tipos:'Ríos',
    inicio:'Nacimiento',fin:'Desembocadura',extremoInicio:'Fuente',extremoFin:'Mar',entreInicio:'la fuente',entreFin:'el mar',Parada:'Parada',proxima:'¿Cuál es la próxima parada?',
    llegarFin:'Llegar al mar',avanzar:'Zarpar a',bajar:'Descender',
    parada:'ciudad',paradas:'ciudades',puertoS:'puerto',puertosS:'puertos',enPuerto:'En el puerto',llevaba:'El mercader llevaba',
    tuVehiculo:'Tu embarcación',carga:'bodega',mercado:'Mercado de',seVende:'Se vende aquí',masAdelante:'vale más río abajo',mercader:'mercader de la ruta',
    zarpas:'Zarpás con diez monedas y la bodega vacía.',cerrado:'Cerrado: ya llegaste al mar con esta barca.',cuentas:'Zarpaste con 10 monedas y llegaste con',sobrante:'Lo que quedaba en la bodega se vendió en',
    soloVender:'Llegaste sin saber adónde ibas: aquí solo podés vender.',nadaQueComprar:'Aquí no hay nada que comprar; vendé si te conviene.',
    sonido:'Sonido del agua',volver:'Volver a los ríos',toca:'Tocá un río en el mapa o en la lista.',retoSub:'Diez preguntas de todos los ríos',
    completo:'río completo',completos:'ríos completos',hechoNota:'Los ríos completos se pintan de dorado en el mapa.',
    selloNota:'Cada sello se gana llegando a una ciudad sabiendo adónde ibas; se vuelve dorado cuando además la recordás en el repaso.',
    recorre:'Bajá un río o jugá un reto: lo que hagás vuelve cuando toque.',recorreFin:'No hay nada pendiente todavía. Bajá un río hasta el mar o jugá un reto: lo que hagás entra al repaso y vuelve cuando toque.',
    ajustesNino:'Mercader: diez monedas, tres espacios y precios que suben río abajo. El animal acompaña, los textos largos quedan plegados en «Contame más» y la voz puede leer sola.',
    ajustesAdulto:'Historia: la carga fija de la ruta, puerto por puerto, sin monedas. Todo el texto a la vista y el animal calladito, salvo para reaccionar.',
    dominas:'Ya dominás este cauce.',conCalma:'Volvé a bajar el río con calma; el repaso te lo va a recordar.',
    ordenBien:'Sin errores: el cauce ya es tuyo.',ordenMal:e=>`${e} errores: volvé a bajar el río con la frase en mano.`,tocaEnOrden:n=>`Tocá las ${n} ciudades en orden, de la fuente al mar.`,
    cabecera:r=>`${r.region} · ${km(r.longitud)} km hasta ${r.fin.en}`,fila:r=>`${esc(r.region)} · ${km(r.longitud)} km · ${r.paradas.length} ${r.zona?'paradas':'ciudades'}`,
    kickerInicio:r=>`Nacimiento · km 0 de ${km(r.longitud)}`,kickerParada:(r,p,n,c)=>`Parada ${p} de ${n} · km ≈${km(c.km)} de ${km(r.longitud)}`,kickerFin:r=>`Desembocadura · km ${km(r.longitud)}`,
    tramo:(r,c,prev)=>prev?`${km(c.km-prev.km)} km desde ${esc(prev.nombre)}`:c.km?`${km(c.km)} km desde la fuente`:'en la fuente misma',
    llegada:r=>`Después de ${km(r.longitud)} km, el ${r.nombre} llega a ${r.fin.en}.`,contame:cx=>'Contame más: la '+cx.titulo.toLowerCase(),
    vozInicio:r=>`Nacimiento: ${r.inicio.nombre}.`,vozParada:(p,n,c)=>`Parada ${p} de ${n}: ${c.nombre}, ${c.pais}.`,vozFin:r=>`Desembocadura: ${r.fin.nombre}. Después de ${r.longitud} kilómetros, el ${r.nombre} llega a ${r.fin.en}.`,
    preguntas:{ciudad:(r,c)=>`¿Junto a qué río está ${c.nombre} (${c.pais})?`,cerca:r=>`¿Cuál de estas ciudades está más cerca de la desembocadura del ${r.nombre}?`,orden:r=>'De la fuente al mar: '+lista(r)+'.',
      contexto:(r,cx)=>`Ruta ${cx.clave}: «${cx.pista}» ¿De qué río se trata?`,fin:r=>`¿Dónde desemboca el ${r.nombre}?`,finNota:r=>`${km(r.longitud)} km hasta ${r.fin.en}. ${r.inicio.nota}`,
      siguiente:(r,c)=>`En el ${r.nombre}, ¿qué parada sigue después de ${c.nombre}?`,relleno:'La desembocadura',imagen:(r,c)=>`¿De qué ciudad del ${r.nombre} es esta imagen? «${sinNombre(c.imagen,c.nombre)}»`,
      altura:r=>`¿En cuál de estas paradas del ${r.nombre} pasa el río más alto sobre el mar?`,alturaNota:'El cauce en cada parada: ',frase:r=>`¿Qué frase guarda el orden de las ciudades del ${r.nombre}?`,
      fecha:(r,c)=>`¿En qué año pasó el ${r.nombre} por ${c.nombre}?`,fechaNota:r=>'Parada por parada: '+r.paradas.map(c=>`${c.nombre} ${c.fecha||'?'}`).join(' · ')+'.',ordenPregunta:r=>`¿En qué orden van estas ciudades del ${r.nombre}?`}},
  itinerario:{tipo:'viaje',tipos:'viajes',Tipos:'Viajes',
    inicio:'Partida',fin:'Regreso',extremoInicio:'Partida',extremoFin:'Regreso',entreInicio:'la partida',entreFin:'el regreso',Parada:'Etapa',proxima:'¿Cuál es la próxima etapa?',
    llegarFin:'Volver a casa',avanzar:'Seguir a',bajar:'Viajar',
    parada:'etapa',paradas:'etapas',puertoS:'alto',puertosS:'altos',enPuerto:'En el camino',llevaba:'El viajero llevaba',
    tuVehiculo:'Tu caravana',carga:'morral',mercado:'Trueque en',seVende:'Se cambia aquí',masAdelante:'vale más adelante',mercader:'viajero de la ruta',
    zarpas:'Salís con diez monedas y el morral vacío.',cerrado:'Cerrado: ya volviste a casa con esta caravana.',cuentas:'Saliste con 10 monedas y volviste con',sobrante:'Lo que quedaba en el morral se cambió en',
    soloVender:'Llegaste sin saber adónde ibas: aquí solo podés vender.',nadaQueComprar:'Aquí no hay nada que cambiar; vendé si te conviene.',
    sonido:'Sonido del camino',sonidoTipo:'viento',volver:'Volver a los viajes',toca:'Tocá un viaje en el mapa o en la lista.',retoSub:'Diez preguntas de todos los viajes',
    completo:'viaje completo',completos:'viajes completos',hechoNota:'Los viajes completos se pintan de dorado en el mapa.',
    selloNota:'Cada sello se gana llegando a una etapa sabiendo adónde ibas; se vuelve dorado cuando además la recordás en el repaso.',
    recorre:'Recorré un viaje o jugá un reto: lo que hagás vuelve cuando toque.',recorreFin:'No hay nada pendiente todavía. Recorré un viaje hasta el regreso o jugá un reto: lo que hagás entra al repaso y vuelve cuando toque.',
    ajustesNino:'Mercader: diez monedas, tres espacios y precios que suben etapa a etapa. El animal acompaña, los textos largos quedan plegados en «Contame más» y la voz puede leer sola.',
    ajustesAdulto:'Historia: lo que el viajero llevaba, alto por alto, sin monedas. Todo el texto a la vista y el animal calladito, salvo para reaccionar.',
    dominas:'Ya dominás este viaje.',conCalma:'Volvé a recorrer el viaje con calma; el repaso te lo va a recordar.',
    ordenBien:'Sin errores: el camino ya es tuyo.',ordenMal:e=>`${e} errores: volvé a recorrer el viaje con la frase en mano.`,tocaEnOrden:n=>`Tocá las ${n} etapas en orden, de la partida al regreso.`,
    cabecera:r=>`${r.region} · de ${r.inicio.nombre} a ${r.fin.en}`,fila:r=>`${esc(r.region)} · ${r.paradas.length} etapas`,
    kickerInicio:r=>`Partida${r.inicio.fecha?` · ${r.inicio.fecha}`:''}`,kickerParada:(r,p,n,c)=>`Etapa ${p} de ${n}${c.fecha?` · ${c.fecha}`:''}`,kickerFin:r=>`Regreso${r.fin.fecha?` · ${r.fin.fecha}`:''}`,
    tramo:(r,c,prev)=>prev?`después de ${esc(prev.nombre)}`:`primera etapa desde ${esc(r.inicio.nombre)}`,
    llegada:r=>`Después de ${r.paradas.length} etapas, ${r.nombre} vuelve a ${r.fin.en}.`,contame:cx=>'Contame más: '+cx.titulo[0].toLowerCase()+cx.titulo.slice(1),
    vozInicio:r=>`Partida: ${r.inicio.nombre}${r.inicio.fecha?', '+r.inicio.fecha:''}.`,vozParada:(p,n,c)=>`Etapa ${p} de ${n}: ${c.nombre}, ${c.pais}${c.fecha?', '+c.fecha:''}.`,vozFin:r=>`Regreso: ${r.fin.en}. Después de ${r.paradas.length} etapas, ${r.nombre} vuelve a ${r.fin.en}.`,
    preguntas:{ciudad:(r,c)=>`¿En qué viaje está la etapa ${c.nombre} (${c.pais})?`,cerca:r=>`¿Cuál de estas etapas está más cerca del final del viaje de ${r.nombre}?`,orden:r=>'De la partida al regreso: '+lista(r)+'.',
      contexto:(r,cx)=>`${cx.titulo}: «${cx.pista}» ¿De qué viaje se trata?`,fin:r=>`¿Dónde termina el viaje de ${r.nombre}?`,finNota:r=>`Sale de ${r.inicio.nombre}${r.inicio.fecha?' en '+r.inicio.fecha:''} y vuelve a ${r.fin.en}${r.fin.fecha?' en '+r.fin.fecha:''}. ${r.inicio.nota}`,
      siguiente:(r,c)=>`En el viaje de ${r.nombre}, ¿qué etapa sigue después de ${c.nombre}?`,relleno:'El regreso',imagen:(r,c)=>`¿De qué etapa del viaje de ${r.nombre} es esta imagen? «${sinNombre(c.imagen,c.nombre)}»`,
      altura:r=>`¿En cuál de estas etapas pasa más alto el viaje de ${r.nombre}?`,alturaNota:'La altura en cada etapa: ',frase:r=>`¿Qué frase guarda el orden de las etapas del viaje de ${r.nombre}?`,
      fecha:(r,c)=>`¿En qué año llegó ${r.nombre} a ${c.nombre}?`,fechaNota:r=>'Etapa por etapa: '+r.paradas.map(c=>`${c.nombre} ${c.fecha||'?'}`).join(' · ')+'.',ordenPregunta:r=>`¿En qué orden pasó ${r.nombre} por estas etapas?`},
    voces:{ordenFin:["¡Perfecto! ¡Te lo sabés como yo!","¡Casi perfecto! Uno más y me gano un puñado de dátiles.","Volvamos a recorrer el viaje juntos, con la frase en la mano."],
      quizBien:["¡Sí! ¡Te lo sabías!","¡Eso! Yo estaba segura.","¡Bravo! Otra más.","¡Claro que sí!","¡Ese es mi viaje!"],
      resultado:["¡Sos guía de este viaje!","¡Bien! Un par de vueltas más y sos guía.","Recorramos el viaje otra vez; yo te acompaño."],
      recitarInicio:["Decí cada etapa antes de revelarla. Yo no soplo.","Cerrá los ojos si querés: el camino ya está en tu cabeza."],
      recitarFin:["¡Todas! Ya podés recorrerlo con menos pista.","Casi todas. Otra vuelta y sale.","Volvamos a recorrer el camino juntos."],
      guiaBien:["¡Esa! Salimos hacia {c}.","Sí, {c}. Yo también me acordaba.","¡Exacto! Rumbo a {c}."],
      guiaMal:["Nop, era {c}. Vamos igual, pero ahí solo vas a poder vender.","Casi. La siguiente es {c}; en ese alto no vas a poder cambiar nada."],
      guiaMalH:["Nop, era {c}. Vamos igual.","Casi: la siguiente es {c}."],
      eventoAviso:["¡Ojo! El camino nos puso una prueba.","¡Alto ahí! Esto se pasa recordando.","Tranquilo: esto lo sabemos."],
      eventoBien:["¡Eso era! Seguimos.","¡Bien ahí! El camino nos deja pasar.","¡Lo sabías! Adelante."],
      compra:["{g}: buen cambio.","Cargado. Ahora a cambiarlo más adelante.","{g} en el morral. ¿Cuánto valdrá más adelante?"],
      podrido:["Uy, {g}: se pasó. A la arena.","{g} podrido. Hay que cambiar más rápido."],
      sinMonedas:["No alcanzan las monedas. Vendé algo primero.","Estamos sin plata. ¿Qué tenés en el morral?"],
      sinEspacio:["El morral está lleno. Vendé algo o dejalo.","Solo caben tres cosas. Elegí."],
      fantasma:["¡Le ganaste al viajero de la ruta!","El viajero de la ruta llegó con {n}; la próxima le ganás.","Empataste con el viajero de la ruta."]}},
  travesia:{tipo:'travesía',tipos:'travesías',Tipos:'Viajes',
    inicio:'Zarpe',fin:'Regreso',extremoInicio:'Zarpe',extremoFin:'Regreso',entreInicio:'el zarpe',entreFin:'el regreso',Parada:'Escala',proxima:'¿Cuál es la próxima escala?',
    llegarFin:'Volver a puerto',avanzar:'Zarpar a',bajar:'Navegar',
    parada:'escala',paradas:'escalas',puertoS:'puerto',puertosS:'puertos',enPuerto:'En el puerto',llevaba:'La flota llevaba',
    tuVehiculo:'Tu flota',carga:'bodega',mercado:'Mercado de',seVende:'Se vende aquí',masAdelante:'vale más en la próxima escala',mercader:'mercader de la flota',
    zarpas:'Zarpás con diez monedas y la bodega vacía.',cerrado:'Cerrado: ya volviste a puerto con esta flota.',cuentas:'Zarpaste con 10 monedas y volviste con',sobrante:'Lo que quedaba en la bodega se vendió en',
    soloVender:'Llegaste sin saber adónde ibas: aquí solo podés vender.',nadaQueComprar:'Aquí no hay nada que comprar; vendé si te conviene.',
    sonido:'Sonido del mar',volver:'Volver a los viajes',toca:'Tocá un viaje en el mapa o en la lista.',retoSub:'Diez preguntas de todos los viajes',
    completo:'travesía completa',completos:'travesías completas',hechoNota:'Los viajes completos se pintan de dorado en el mapa.',
    selloNota:'Cada sello se gana llegando a una escala sabiendo adónde ibas; se vuelve dorado cuando además la recordás en el repaso.',
    recorre:'Recorré un viaje o jugá un reto: lo que hagás vuelve cuando toque.',recorreFin:'No hay nada pendiente todavía. Recorré un viaje hasta el regreso o jugá un reto: lo que hagás entra al repaso y vuelve cuando toque.',
    ajustesNino:'Mercader: diez monedas, tres espacios y precios que suben escala a escala. El animal acompaña, los textos largos quedan plegados en «Contame más» y la voz puede leer sola.',
    ajustesAdulto:'Historia: lo que la flota llevaba, puerto por puerto, sin monedas. Todo el texto a la vista y el animal calladito, salvo para reaccionar.',
    dominas:'Ya dominás esta travesía.',conCalma:'Volvé a navegar la travesía con calma; el repaso te lo va a recordar.',
    ordenBien:'Sin errores: la ruta ya es tuya.',ordenMal:e=>`${e} errores: volvé a navegar con la frase en mano.`,tocaEnOrden:n=>`Tocá las ${n} escalas en orden, del zarpe al regreso.`,
    cabecera:r=>`${r.region} · de ${r.inicio.nombre} a ${r.fin.en}`,fila:r=>`${esc(r.region)} · ${r.paradas.length} escalas`,
    kickerInicio:r=>`Zarpe${r.inicio.fecha?` · ${r.inicio.fecha}`:''}`,kickerParada:(r,p,n,c)=>`Escala ${p} de ${n}${c.fecha?` · ${c.fecha}`:''}`,kickerFin:r=>`Regreso${r.fin.fecha?` · ${r.fin.fecha}`:''}`,
    tramo:(r,c,prev)=>prev?`después de ${esc(prev.nombre)}`:`primera escala desde ${esc(r.inicio.nombre)}`,
    llegada:r=>`Después de ${r.paradas.length} escalas, la flota de ${r.nombre} vuelve a ${r.fin.en}.`,contame:cx=>'Contame más: '+cx.titulo[0].toLowerCase()+cx.titulo.slice(1),
    vozInicio:r=>`Zarpe: ${r.inicio.nombre}${r.inicio.fecha?', '+r.inicio.fecha:''}.`,vozParada:(p,n,c)=>`Escala ${p} de ${n}: ${c.nombre}, ${c.pais}${c.fecha?', '+c.fecha:''}.`,vozFin:r=>`Regreso: ${r.fin.en}. Después de ${r.paradas.length} escalas, la flota de ${r.nombre} vuelve a ${r.fin.en}.`,
    preguntas:{ciudad:(r,c)=>`¿En qué viaje está la escala ${c.nombre} (${c.pais})?`,cerca:r=>`¿Cuál de estas escalas está más cerca del final de la travesía de ${r.nombre}?`,orden:r=>'Del zarpe al regreso: '+lista(r)+'.',
      contexto:(r,cx)=>`${cx.titulo}: «${cx.pista}» ¿De qué viaje se trata?`,fin:r=>`¿Dónde termina la travesía de ${r.nombre}?`,finNota:r=>`Zarpa de ${r.inicio.nombre}${r.inicio.fecha?' en '+r.inicio.fecha:''} y vuelve a ${r.fin.en}${r.fin.fecha?' en '+r.fin.fecha:''}. ${r.inicio.nota}`,
      siguiente:(r,c)=>`En la travesía de ${r.nombre}, ¿qué escala sigue después de ${c.nombre}?`,relleno:'El regreso',imagen:(r,c)=>`¿De qué escala de la travesía de ${r.nombre} es esta imagen? «${sinNombre(c.imagen,c.nombre)}»`,
      altura:r=>`¿En cuál de estas escalas pasa más alto la travesía de ${r.nombre}?`,alturaNota:'La altura en cada escala: ',frase:r=>`¿Qué frase guarda el orden de las escalas de la travesía de ${r.nombre}?`,
      fecha:(r,c)=>`¿En qué año llegó la flota de ${r.nombre} a ${c.nombre}?`,fechaNota:r=>'Escala por escala: '+r.paradas.map(c=>`${c.nombre} ${c.fecha||'?'}`).join(' · ')+'.',ordenPregunta:r=>`¿En qué orden pasó la flota de ${r.nombre} por estas escalas?`},
    voces:{ordenFin:["¡Perfecto! ¡Te lo sabés como yo!","¡Casi perfecto! Uno más y me gano un pescado.","Volvamos a navegar la ruta juntos, con la frase en la mano."],
      quizBien:["¡Sí! ¡Te lo sabías!","¡Eso! Yo estaba segura.","¡Bravo! Otra más.","¡Claro que sí!","¡Ese es mi viaje!"],
      resultado:["¡Sos almirante de esta flota!","¡Bien! Un par de viajes más y sos almirante.","Naveguemos la ruta otra vez; yo te acompaño."],
      recitarInicio:["Decí cada escala antes de revelarla. Yo no soplo.","Cerrá los ojos si querés: la ruta ya está en tu cabeza."],
      recitarFin:["¡Todas! Ya podés navegar con menos pista.","Casi todas. Otra vuelta y sale.","Volvamos a navegar la ruta juntos."],
      eventoAviso:["¡Ojo! El mar nos puso una prueba.","¡Alto ahí! Esto se pasa recordando.","Tranquilo: esto lo sabemos."],
      eventoBien:["¡Eso era! Seguimos.","¡Bien ahí! El mar nos deja pasar.","¡Lo sabías! Adelante."],
      compra:["{g}: buena compra.","Cargado. Ahora a venderlo en la próxima escala.","{g} en la bodega. ¿Cuánto valdrá más adelante?"],
      fantasma:["¡Le ganaste al mercader de la flota!","El mercader de la flota llegó con {n}; la próxima le ganás.","Empataste con el mercader de la flota."]}}
};
const VZ=()=>{const r=S.rio&&rutaPor(S.rio);return r?r.vocesEfectivas:VOCES};/* voces del compañero según la ruta abierta */
const VJ=()=>VOCAB[(typeof JUEGO!=='undefined'&&JUEGO.tipo)||'rio'];/* vocabulario del juego, para las pantallas sin ruta */
function desdeRio(r){if(r.tipo)return r;r.tipo='rio';r.region=r.continente;
  r.inicio={nombre:r.nace,nota:r.naceNota,escena:r.escenaNace};r.fin={nombre:r.mar,en:r.marEn,escena:r.escenaMar};
  r.contexto=[{clave:'antigua',titulo:'Ruta antigua',texto:r.antigua,pista:r.pistaAntigua},{clave:'moderna',titulo:'Ruta moderna',texto:r.moderna,pista:r.pistaModerna}];
  r.trazo=[r.curso];r.ramas=r.brazos||[];r.paradas=r.ciudades;
  const m=MASCOTAS[r.id];if(m&&m.fin==null)m.fin=m.mar;r.companero=r.masc=m;
  r.carga=r.mercado=MERCADOS[r.id]||[];r.eventos=EVENTOS[r.id]||[];r.perfil=ALTURAS[r.id]||null;
  const n=NAVES[r.id];if(n){r.vehiculo=r.nave=n;r.paradas.forEach((c,i)=>{if(n.puertos[i]){c.puerto=n.puertos[i][0];c.carga=n.puertos[i][1]}})}
  return r}
function normalizar(r){r.ramas=r.ramas||[];r.carga=r.carga||[];r.eventos=r.eventos||[];r.perfil=r.perfil||null;if(r.vehiculo&&r.vehiculo.puertos)r.paradas.forEach((c,i)=>{const pu=r.vehiculo.puertos[i];if(pu&&c.puerto==null){c.puerto=pu[0];c.carga=pu[1]}});
  r.vocab=Object.assign({},VOCAB[r.tipo]||VOCAB.rio,r.vocab||{});r.vocesEfectivas=Object.assign({},VOCES,r.vocab.voces||{});r.pref=(r.tipo==='rio'?'rio:':'ruta:')+r.id+':';/* prefijo de las tarjetas: rio: se conserva por el progreso guardado */
  r.curso=r.trazo.length===1?r.trazo[0]:[].concat(...r.trazo);r.cortes=[];let k=0;r.trazo.forEach((seg,i)=>{if(i)r.cortes.push(k);k+=seg.length});/* cortes: índice donde empieza cada segmento nuevo */
  r.acum=[0];for(let i=1;i<r.curso.length;i++)r.acum[i]=r.acum[i-1]+hav(r.curso[i-1],r.curso[i]);r.kmPoly=r.acum[r.acum.length-1];
  let ult=0;r.paradas.forEach(c=>{let best=ult,bd=1e9;for(let i=ult;i<r.curso.length;i++){const d=(r.curso[i][0]-c.pos[0])**2+(r.curso[i][1]-c.pos[1])**2;if(d<bd){bd=d;best=i}}c.idx=best;ult=best;c.km=Math.round(r.acum[best]/r.kmPoly*(r.longitud||r.kmPoly))});
  if(r.carga.length)r.fantasma=fantasma(r);return r}
const RUTAS=JUEGO.rutas().map(normalizar);
const idxParada=(r,p)=>p<=0?0:p>r.paradas.length?r.curso.length-1:r.paradas[p-1].idx;
/* ---------- relieve: perfil de altura del cauce (ALTURAS, de tools/relieve.py: puntos [fracción del cauce, metros]) ---------- */
const alturaEn=(r,f)=>{const P=r.perfil;if(!P)return null;if(f<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++)if(f<=P[i][0]){const [f0,a0]=P[i-1],[f1,a1]=P[i];return f1>f0?a0+(a1-a0)*(f-f0)/(f1-f0):a1}return P[P.length-1][1]};
const fracParada=(r,i)=>r.acum[r.paradas[i].idx]/r.kmPoly;
const alturaParada=(r,i)=>{const a=alturaEn(r,fracParada(r,i));return a==null?null:Math.round(a)};
const textoAltura=(r,i)=>{const a=alturaParada(r,i);return a==null?'':a<0?` · el río va ${km(-a)} m bajo el nivel del océano`:a<5?' · el río ya va al nivel del mar':` · el río pasa a ${km(a)} m sobre el mar`};
const fraseAltura=(r,i)=>{const a=alturaParada(r,i);return a==null?'':a<0?`El río va ${-a} metros bajo el nivel del océano.`:a<5?'El río ya va al nivel del mar.':`El río pasa a ${a} metros sobre el mar.`};
function fracActual(r){const n=r.paradas.length,p=S.paso,fp=k=>k<=0?0:k>n?1:fracParada(r,k-1);return S.evento?(fp(p)+fp(p+1))/2:fp(p)}
const anio=f=>{const t=String(f||''),m=t.match(/\d{3,4}/);return m?(/a\.\s?C/.test(t)?-m[0]:+m[0]):null};/* «334 a. C.» → -334 */
const txtAnio=a=>a<0?`${-a} a. C.`:String(a);
const conFranja=r=>!!(r.perfil||(anio(r.inicio.fecha)!=null&&anio(r.fin.fecha)!=null&&r.paradas.some(c=>anio(c.fecha)!=null)));
function tiempoSVG(r){/* línea de tiempo: para las rutas con fechas (itinerarios), lo que el perfil de altura es para los ríos */
  const el=document.getElementById('perfil'),W=Math.max(300,(el&&el.clientWidth)||380),H=56,x0=12,x1=W-12,y=31,a0=anio(r.inicio.fecha),a1=anio(r.fin.fecha),ff=r.paradas.map(c=>anio(c.fecha));if(a0==null||a1==null||a1<=a0)return '';
  const X=a=>x0+(a-a0)/(a1-a0)*(x1-x0),n=r.paradas.length,p=S.paso,ap=k=>k<=0?a0:k>n?a1:(ff[k-1]!=null?ff[k-1]:a0),aa=S.evento?(ap(p)+ap(p+1))/2:ap(p),xa=X(aa);
  let h=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Línea de tiempo del viaje de ${esc(r.nombre)}: de ${txtAnio(a0)} a ${txtAnio(a1)}"><line class="perfil-base" x1="${x0}" y1="${y}" x2="${x1}" y2="${y}"/>`;
  h+=`<text class="perfil-txt" x="${x0}" y="${y-9}">${txtAnio(a0)}</text><text class="perfil-txt" x="${x1}" y="${y-9}" text-anchor="end">${txtAnio(a1)}</text>`;
  r.paradas.forEach((c,i)=>{if(ff[i]==null)return;const x=X(ff[i]);h+=`<circle class="perfil-tick" cx="${x.toFixed(1)}" cy="${y}" r="2.2"><title>${esc(c.nombre)}: ${esc(c.fecha)}</title></circle>${i%2?`<text class="perfil-txt k" x="${x.toFixed(1)}" y="${y+15}" text-anchor="middle">${txtAnio(ff[i])}</text>`:''}`});
  const nom=p<=0?r.inicio.nombre:p>n?r.fin.en:r.paradas[p-1].nombre,fe=p>=1&&p<=n?r.paradas[p-1].fecha:p<=0?r.inicio.fecha:r.fin.fecha;
  h+=`<circle class="perfil-aqui" cx="${xa.toFixed(1)}" cy="${y}" r="4"/><text class="perfil-txt" x="${Math.min(Math.max(xa,60),W-60).toFixed(1)}" y="${H-4}" text-anchor="middle">${esc(nom)}${fe?' · '+esc(fe):''}</text>`;
  return h+'</svg>'}
function perfilSVG(r){const P=r.perfil;if(!P)return tiempoSVG(r);const el=document.getElementById('perfil'),W=Math.max(300,(el&&el.clientWidth)||380),H=56,x0=8,x1=W-8,yb=44,yt=10,top=Math.max(P[0][1],1),piso=Math.min(0,P[P.length-1][1]);
  const X=f=>x0+f*(x1-x0),Y=a=>yb-(Math.max(a,piso)-piso)/(top-piso)*(yb-yt),fa=fracActual(r),aa=Math.round(alturaEn(r,fa)),xa=X(fa),ya=Y(aa);
  let h=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Perfil de altura del ${esc(r.nombre)}: de ${km(P[0][1])} m en la fuente a ${km(P[P.length-1][1])} m en el mar">`;
  h+=`<path class="perfil-tierra" d="M${X(0).toFixed(1)} ${yb}L${P.map(([f,a])=>`${X(f).toFixed(1)} ${Y(a).toFixed(1)}`).join('L')}L${X(1).toFixed(1)} ${yb}Z"/><line class="perfil-base" x1="${x0}" y1="${Y(0).toFixed(1)}" x2="${x1}" y2="${Y(0).toFixed(1)}"/>`;
  r.paradas.forEach((c,i)=>{h+=`<circle class="perfil-tick" cx="${X(fracParada(r,i)).toFixed(1)}" cy="${Y(alturaParada(r,i)).toFixed(1)}" r="2.2"><title>${esc(c.nombre)}: ${km(alturaParada(r,i))} m</title></circle>`});
  h+=`<circle class="perfil-aqui" cx="${xa.toFixed(1)}" cy="${ya.toFixed(1)}" r="4"/>`;
  const izq=fa>0.75;h+=`<text class="perfil-txt" x="${(xa+(izq?-8:8)).toFixed(1)}" y="${(ya<24?ya+14:ya-7).toFixed(1)}" text-anchor="${izq?'end':'start'}">${km(aa)} m</text>`;
  if(fa>0.12)h+=`<text class="perfil-txt" x="${(x0+7).toFixed(1)}" y="${(yt+4).toFixed(1)}">${km(P[0][1])} m</text>`;
  h+=`<text class="perfil-txt k" x="${x1}" y="${H-3}" text-anchor="end">Altura del cauce</text>`;
  return h+'</svg>'}
const kmParada=(r,p)=>p<=0?0:p>r.paradas.length?r.longitud:r.paradas[p-1].km;
function puntoMedio(r,de,a){if(a<=de)return{k:de,pt:r.curso[de]};const s=(r.acum[de]+r.acum[a])/2;let k=de;while(k<a-1&&r.acum[k+1]<=s)k++;
  const p=r.curso[k],q=r.curso[k+1],L=r.acum[k+1]-r.acum[k],u=L?(s-r.acum[k])/L:0;return{k,pt:[p[0]+(q[0]-p[0])*u,p[1]+(q[1]-p[1])*u]}}

/* ---------- sonido de agua (ruido rosa filtrado; rápidos cerca de la fuente, mar al final) ---------- */
const audio={ctx:null,on:false,nivel:0.7,frac:0.4,modo:'agua',
  iniciar(){const C=window.AudioContext||window.webkitAudioContext;if(!C)return false;const ctx=this.ctx=new C();
    const buf=ctx.createBuffer(1,ctx.sampleRate*4,ctx.sampleRate),d=buf.getChannelData(0);let b0=0,b1=0,b2=0;
    for(let i=0;i<d.length;i++){const w=Math.random()*2-1;b0=0.99765*b0+w*0.0990460;b1=0.96300*b1+w*0.2965164;b2=0.57000*b2+w*1.0526913;d[i]=(b0+b1+b2+w*0.1848)*0.15}
    const src=ctx.createBufferSource();src.buffer=buf;src.loop=true;
    const bp=this.bp=ctx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=1000;bp.Q.value=0.8;
    const lp=ctx.createBiquadFilter();lp.type='lowpass';lp.frequency.value=2600;
    const mod=ctx.createGain();mod.gain.value=1;const lfo=this.lfo=ctx.createOscillator();lfo.frequency.value=0.4;const lg=this.lfoG=ctx.createGain();lg.gain.value=0.3;lfo.connect(lg);lg.connect(mod.gain);
    const g=this.g=ctx.createGain();g.gain.value=0;
    src.connect(bp);bp.connect(lp);lp.connect(mod);mod.connect(g);g.connect(ctx.destination);src.start();lfo.start();return true},
  toggle(){if(!this.ctx&&!this.iniciar())return;this.on=!this.on;if(this.on)this.ctx.resume();const t=this.ctx.currentTime;this.g.gain.cancelScheduledValues(t);this.g.gain.setTargetAtTime(this.on?this.nivel:0,t,0.4);this.ajustar(this.frac);
    document.querySelectorAll('.son').forEach(b=>{b.classList.toggle('on',this.on);b.setAttribute('aria-pressed',this.on)})},
  ajustar(frac){this.frac=frac;if(!this.ctx)return;const t=this.ctx.currentTime,v=this.modo==='viento';/* viento: más grave, más lento, sin rápidos */
    this.bp.frequency.setTargetAtTime(v?700-300*frac:1400-1000*frac,t,0.8);this.bp.Q.setTargetAtTime(v?0.5:0.6+0.6*frac,t,0.8);this.lfo.frequency.setTargetAtTime(v?0.15:0.6-0.4*frac,t,0.8);this.lfoG.gain.setTargetAtTime(v?0.5:0.22+0.3*frac,t,0.8)},
  ping(f){if(!this.ctx||!this.on)return;const t=this.ctx.currentTime,o=this.ctx.createOscillator(),g=this.ctx.createGain();o.type='sine';o.frequency.value=f||880;g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.25,t+0.01);g.gain.exponentialRampToValueAtTime(0.0001,t+0.25);o.connect(g);g.connect(this.ctx.destination);o.start(t);o.stop(t+0.3)},
  remar(){if(!this.ctx||!this.on)return;const t=this.ctx.currentTime,g=this.g.gain;g.cancelScheduledValues(t);g.setValueAtTime(g.value,t);g.linearRampToValueAtTime(this.nivel*1.9,t+0.25);g.setTargetAtTime(this.nivel,t+0.3,0.6)},
  duck(on){if(!this.ctx||!this.on)return;const t=this.ctx.currentTime;this.g.gain.cancelScheduledValues(t);this.g.gain.setTargetAtTime(on?this.nivel*0.25:this.nivel,t,0.3)}};

/* ---------- voz del animal: speechSynthesis del navegador, sin archivos de audio ---------- */
const ORD=['primera','segunda','tercera','cuarta','quinta','sexta','sétima','octava'];
const romano=s=>{const V={I:1,V:5,X:10,L:50};let n=0;for(let i=0;i<s.length;i++){const a=V[s[i]],b=V[s[i+1]]||0;n+=a<b?-a:a}return n};
function paraVoz(t){return sinHtml(t).replace(/[\[\]«»]/g,'').replace(/(\d)[    ](?=\d{3}\b)/g,'$1').replace(/km³/g,'kilómetros cúbicos').replace(/\bkm\b/g,'kilómetros').replace(/\ba\. C\./g,'antes de Cristo').replace(/\bc\. (?=\d)/g,'hacia ')
  .replace(/\b(siglos?|dinastía) ([IVXL]+)\b/g,(m,a,b)=>a+' '+romano(b)).replace(/\b[IVXL]{2,}\b/g,romano).replace(/(\d) m\b/g,'$1 metros').replace(/≈/g,'unos ').replace(/ · /g,'. ').replace(/→/g,', luego ').replace(/___/g,'esta ciudad').replace(/\s+/g,' ').trim()}
const MSG_QUIZ=V=>[V.dominas,'Bien; lo que fallaste vuelve en el repaso.',V.conCalma];const vocabQuiz=()=>S.quiz&&S.quiz.modo==='rio'&&S.rio?rioPor(S.rio).vocab:VJ();
const nivelQuiz=Q=>{const p=Q.aciertos/Q.qs.length;return p>=0.9?0:p>=0.6?1:2};
function lectura(){const r=S.pantalla!=='inicio'&&S.pantalla!=='pasaporte'&&S.rio&&rioPor(S.rio);if(!r)return[];const V=r.vocab,n=r.paradas.length,m=r.companero,h=modo()==='historia',L=[];
  const di=(...t)=>t.forEach(x=>{if(x)L.push(String(x))});
  const opciones=(ops,pre)=>{di(pre);ops.forEach((o,i)=>di(`${ORD[i]||(i+1)}: ${sinHtml(o)}`))};
  const quiz=Q=>{const N=Q.qs.length;if(Q.i>=N){const k=nivelQuiz(Q);di(Q.modo==='rio'?VZ().resultado[k]:'',`${Q.aciertos} de ${N}.`,MSG_QUIZ(vocabQuiz())[k]);return}const q=Q.qs[Q.i];if(Q.modo==='rio'||Q.resp!=null)di(Q.dicho);di(q.texto);if(Q.resp==null)opciones(q.opciones);else di(q.nota)};
  if(S.pantalla==='quiz'||S.tab==='preguntar'){if(S.quiz)quiz(S.quiz);return L}
  if(S.tab==='ordenar'){const o=S.orden;di(o.dicho);if(!o.listo)opciones(o.pool.map(i=>r.paradas[i].nombre),V.tocaEnOrden(n));return L}
  if(S.tab==='recitar'){const R=S.rec;di(R.dicho);if(R.i>=n)di(`${R.ok.filter(Boolean).length} de ${n} recordadas.`);else if(!R.revelada)di(`${V.Parada} ${R.i+1} de ${n}: decila en voz alta y después revelá.`);else di(`${r.paradas[R.i].nombre}, ${r.paradas[R.i].pais}. ¿La sabías?`);return L}
  const E=S.evento,p=S.paso;
  if(E){di(E.dicho,E.def.titulo+'. '+E.def.texto,E.q.texto);if(E.resp==null)opciones(E.q.opciones);else di((E.ok?E.def.bien:E.def.mal)+(E.delta?` ${E.delta>0?'Ganás':'Perdés'} ${Math.abs(E.delta)} monedas.`:''),h?E.q.nota:'');return L}
  const guia=()=>{const g=S.guias[p];if(g&&g.resp==null&&p<n)opciones(g.opciones.map(i=>r.paradas[i].nombre),V.proxima)};
  if(p===0){di(S.dicho||(m&&m.hola),V.vozInicio(r),h?r.inicio.nota:'');guia()}
  else if(p<=n){const c=r.paradas[p-1];di(S.dicho||(m&&m.paradas[p-1]),V.vozParada(p,n,c),'Imagen para recordar: '+c.imagen,h?c.dato:'',h?fraseAltura(r,p-1):'',S.selloNuevo===claveSello(r,p-1)?`¡Sello de ${c.nombre} en el pasaporte!`:'');guia()}
  else di(S.dicho||(m&&m.fin),V.vozFin(r));
  return L}
const voz={hablando:false,
  soporte(){return typeof window!=='undefined'&&!!window.speechSynthesis&&typeof SpeechSynthesisUtterance!=='undefined'},
  elegir(){const off=typeof navigator!=='undefined'&&navigator.onLine===false,vs=window.speechSynthesis.getVoices().filter(v=>/^es/i.test(v.lang)&&!(off&&v.localService===false));
    for(const p of ['es-cr','es-mx','es-us','es-419'])for(const v of vs)if(v.lang.replace('_','-').toLowerCase().startsWith(p))return v;return vs[0]||null},
  leer(){if(!this.soporte())return;if(this.hablando){this.callar();return}this.decir(lectura())},
  decir(frases){if(!this.soporte())return;frases=(frases||[]).map(paraVoz).filter(Boolean);const ss=window.speechSynthesis;ss.cancel();if(!frases.length){this.estado(false);return}const v=this.elegir();
    frases.forEach((t,i)=>{const u=new SpeechSynthesisUtterance(t);if(v){u.voice=v;u.lang=v.lang}else u.lang='es-MX';u.rate=0.95;if(i===frases.length-1)u.onend=u.onerror=()=>this.estado(false);ss.speak(u)});this.estado(true)},
  callar(){if(this.hablando&&this.soporte())window.speechSynthesis.cancel();this.estado(false)},
  estado(on){if(on!==this.hablando){this.hablando=on;audio.duck(on)}document.querySelectorAll('.voz').forEach(b=>{b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)})}};

/* ---------- persistencia: localStorage de este navegador, un progreso por perfil; memoria si no hay ---------- */
const store={mem:{},clave:n=>JUEGO.clave+':progreso:'+n,
  leer(k){try{const v=window.localStorage&&window.localStorage.getItem(k);if(v)return JSON.parse(v)}catch(e){}return this.mem[k]||null},
  escribir(k,v){this.mem[k]=v;try{if(window.localStorage)window.localStorage.setItem(k,JSON.stringify(v))}catch(e){}},
  borrar(k){delete this.mem[k];try{if(window.localStorage)window.localStorage.removeItem(k)}catch(e){}}};
let PERFILES={activo:'Capitán',lista:['Capitán']};
const nuevoP=()=>({cards:{},vistos:{},sellos:{}});

/* ---------- pasaporte: un sello por ciudad, ganado al llegar sabiendo adónde ibas; dorado si además está en caja ≥ 3 ---------- */
const sellos=()=>P.sellos||(P.sellos={});
const claveSello=(r,i)=>r.id+':'+i;
const sellosDe=r=>r.paradas.filter((c,i)=>sellos()[claveSello(r,i)]).length;
const completo=r=>sellosDe(r)===r.paradas.length;
const totalSellos=()=>RUTAS.reduce((a,r)=>a+sellosDe(r),0);
const selloOro=(r,i)=>{const c=P.cards['ciudad:'+r.id+':'+i];return !!(c&&c.box>=3)};
function sellar(r,i){const k=claveSello(r,i);if(sellos()[k])return false;sellos()[k]=Date.now();guardar();return true}
const fechaSello=ts=>{try{return new Date(ts).toLocaleDateString('es-CR',{day:'numeric',month:'short'})}catch(e){return ''}};
function verPasaporte(){S.pantalla='pasaporte';S.aviso=null;render()}
/* sellos con carácter: forma, inclinación, desgaste y tinta salen de un hash de río:parada, así cada sello es siempre el mismo */
const FORMAS={circulo:'<circle cx="50" cy="50" r="46"/>',ovalo:'<ellipse cx="50" cy="50" rx="48" ry="41"/>',cuadrado:'<rect x="6" y="6" width="88" height="88" rx="18"/>',hexagono:'<polygon points="50,3 93,26 93,74 50,97 7,74 7,26"/>',octogono:'<polygon points="30,4 70,4 96,30 96,70 70,96 30,96 4,70 4,30"/>',escudo:'<path d="M50 4 L93 14 V52 Q93 82 50 97 Q7 82 7 52 V14 Z"/>'};
const DESGASTES=['','4 2','7 2 2 2','9 3','2 2','6 1 1 1'];
function sello(r,i,extra){const c=r.paradas[i],k=claveSello(r,i),ts=sellos()[k];let h=2166136261;for(const ch of k)h=Math.imul(h^ch.charCodeAt(0),16777619);h=Math.imul(h^(h>>>13),1540483477)>>>0;h=(h^(h>>>15))>>>0;/* FNV-1a con mezcla final: claves vecinas dan sellos distintos */
  const nombres=Object.keys(FORMAS),f=FORMAS[nombres[h%nombres.length]],rot=((h>>>5)%29)-14,desgaste=DESGASTES[(h>>>10)%DESGASTES.length],tinta=(h>>>15)%3===0?' verde2':'';
  if(!ts)return `<svg class="sello vacio" viewBox="0 0 100 100" role="img" aria-label="Sin sello"><g class="forma">${f}</g></svg>`;
  const oro=selloOro(r,i),pc=c.escena&&picto(c.escena[0]),aro=((oro?'★ ':'')+r.nombre+' · '+c.pais+' · ').toUpperCase();let txt=aro;while(txt.length<36)txt+=aro;
  const largo=c.nombre.length>11?' textLength="78" lengthAdjust="spacingAndGlyphs"':'',id='aro'+h.toString(36);
  return `<svg class="sello${oro?' oro':tinta}${extra||''}" viewBox="0 0 100 100" style="--rot:${rot}deg" role="img" aria-label="Sello de ${esc(c.nombre)}"><defs><path id="${id}" d="M50 50 m-37 0 a37 37 0 1 1 74 0 a37 37 0 1 1 -74 0"/></defs><g class="forma">${f}</g><g class="forma2" transform="translate(50 50) scale(.9) translate(-50 -50)"${desgaste?` stroke-dasharray="${desgaste}"`:''}>${f}</g><text class="aro"><textPath href="#${id}">${esc(txt)}</textPath></text>${pc?`<svg class="escena pic" x="34" y="19" width="32" height="32" viewBox="${pc.vb}">${pc.svg}</svg>`:''}<text class="nom" x="50" y="64" text-anchor="middle"${largo}>${esc(c.nombre)}</text><text class="fecha" x="50" y="76" text-anchor="middle">${esc(fechaSello(ts))}</text></svg>`}
function renderSello(r,i){const k=claveSello(r,i),c=r.paradas[i];
  if(S.selloNuevo===k)return `<div class="sello-nuevo">${sello(r,i,' nuevo')}<div><b>¡Sello de ${esc(c.nombre)}!</b> Llegaste sabiendo adónde ibas; ya está en tu pasaporte.</div></div>`;
  if(sellos()[k])return `<div class="sello-nota">${sello(r,i)}<div>Sello en el pasaporte${selloOro(r,i)?', y dorado: la recordás en el repaso':''}.</div></div>`;
  if(S.llaves[i]===false)return `<div class="sello-nota">${sello(r,i)}<div>Sin sello esta vez: llegaste sin saber adónde ibas. En la próxima bajada, si lo sabés, lo ganás.</div></div>`;
  return ''}
function renderPasaporte(){const grupos=JUEGO.grupos.map(g=>[g.titulo,RUTAS.filter(g.filtro)]);
  const total=RUTAS.reduce((a,r)=>a+r.paradas.length,0),hechos=RUTAS.filter(completo).length;
  return `<p class="kicker">Pasaporte de ${esc(PERFILES.activo)}</p><h2>${totalSellos()} de ${total} sellos</h2><p>${hechos===1?'Un '+VJ().completo:hechos+' '+VJ().completos} de ${RUTAS.length}. ${VJ().selloNota} ${VJ().hechoNota}</p>
${grupos.map(([t,rs])=>`<div class="fkicker">${t}</div>`+rs.map(r=>`<div class="pas-rio"><button class="pas-cab" onclick="abrirRio('${r.id}')">${r.companero?`<span class="emo" aria-hidden="true">${animal(r.companero)}</span>`:''}<b>${esc(r.nombre)}</b><span class="fmeta">${sellosDe(r)} de ${r.paradas.length} sellos${completo(r)?' · completo':''}</span></button><div class="sellos">${r.paradas.map((c,i)=>sello(r,i)).join('')}</div></div>`).join('')).join('')}
<div class="acciones"><button class="btn sec" onclick="irInicio()">${VJ().volver}</button></div>`}
const guardarPerfiles=()=>store.escribir(JUEGO.clave+':perfiles',PERFILES);
function cargarPerfiles(){const g=store.leer(JUEGO.clave+':perfiles');
  if(g&&g.lista&&g.lista.length)PERFILES=g;
  else{PERFILES={activo:'Capitán',lista:['Capitán']};const viejo=store.leer(JUEGO.clave+':progreso');if(viejo&&viejo.cards){store.escribir(store.clave('Capitán'),viejo);store.borrar('cauces:progreso')}guardarPerfiles()}
  if(!PERFILES.lista.includes(PERFILES.activo))PERFILES.activo=PERFILES.lista[0];P=store.leer(store.clave(PERFILES.activo))||nuevoP()}
function elegirPerfil(i){const n=PERFILES.lista[i];if(!n)return;PERFILES.activo=n;guardarPerfiles();P=store.leer(store.clave(n))||nuevoP();S.perfilNuevo=false;S.aviso=null;render(false)}
function nuevoPerfil(){S.perfilNuevo=!S.perfilNuevo;render(false);const el=document.getElementById('nombrePerfil');if(S.perfilNuevo&&el&&el.focus)el.focus()}
function crearPerfil(nombre){const el=document.getElementById('nombrePerfil');nombre=String(nombre!=null?nombre:(el&&el.value)||'').trim().slice(0,20);if(!nombre)return;
  const i=PERFILES.lista.findIndex(x=>x.toLowerCase()===nombre.toLowerCase());if(i>=0){elegirPerfil(i);return}
  PERFILES.lista.push(nombre);PERFILES.activo=nombre;guardarPerfiles();P=nuevoP();guardar();S.perfilNuevo=false;S.aviso=null;render(false)}
const preguntar=m=>typeof confirm==='function'?confirm(m):true;
function quitarPerfil(){const n=PERFILES.activo;if(!preguntar(`¿Quitar el perfil ${n} y su progreso de este navegador? Si querés conservarlo, guardalo antes en un archivo.`))return;
  store.borrar(store.clave(n));PERFILES.lista=PERFILES.lista.filter(x=>x!==n);if(!PERFILES.lista.length)PERFILES.lista=['Capitán'];PERFILES.activo=PERFILES.lista[0];guardarPerfiles();P=store.leer(store.clave(PERFILES.activo))||nuevoP();S.aviso=null;render(false)}
const progresoJSON=()=>JSON.stringify({app:JUEGO.id,version:1,perfil:PERFILES.activo,guardado:new Date().toISOString(),progreso:P});
function exportar(){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([progresoJSON()],{type:'application/json'}));a.href=url;a.download='cauces-'+PERFILES.activo.replace(/[^\p{L}\p{N}]+/gu,'-')+'.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
function importarTexto(txt){let d=null;try{d=JSON.parse(txt)}catch(e){}
  const p=d&&d.progreso&&d.progreso.cards?d.progreso:(d&&d.cards?d:null);if(!p){S.aviso='Ese archivo no tiene un progreso de Cauces.';render(false);return false}
  const n=(d.perfil&&String(d.perfil).trim().slice(0,20))||PERFILES.activo,hay=store.leer(store.clave(n));
  if(hay&&Object.keys(hay.cards||{}).length&&!preguntar(`Ya hay progreso de ${n} en este navegador. ¿Reemplazarlo con el del archivo?`))return false;
  if(!PERFILES.lista.includes(n))PERFILES.lista.push(n);PERFILES.activo=n;guardarPerfiles();P={cards:p.cards||{},vistos:p.vistos||{},tesoro:p.tesoro||0,modo:p.modo,voz:p.voz,sellos:p.sellos||{},dia:p.dia};guardar();S.perfilNuevo=false;S.aviso=`Progreso de ${n} cargado.`;render(false);return true}
function importarArchivo(input){const f=input.files&&input.files[0];if(!f)return;const r=new FileReader();r.onload=()=>importarTexto(r.result);r.readAsText(f);input.value=''}
function renderPerfiles(){const on=PERFILES.activo;return `<div class="fkicker">¿Quién juega?</div><div class="chips perfiles">${PERFILES.lista.map((n,i)=>`<button class="chip${n===on?' bien':''}" onclick="elegirPerfil(${i})" aria-pressed="${n===on}">${esc(n)}</button>`).join('')}<button class="chip" onclick="nuevoPerfil()" aria-expanded="${S.perfilNuevo}">＋ Otro</button></div>${S.perfilNuevo?`<form class="acciones" onsubmit="crearPerfil();return false"><input class="campo" id="nombrePerfil" maxlength="20" placeholder="¿Cómo te llamás?" aria-label="Nombre del perfil" autocomplete="off"><button class="btn" type="submit">Listo</button></form>`:''}`}
function renderProgreso(){return `<div class="progreso"><div class="fkicker">Progreso</div><p class="fnota">Se guarda en este navegador, un progreso por perfil. Para tener una copia o llevarlo a otro aparato: <button class="enlace" onclick="exportar()">guardar en un archivo</button> · <label class="enlace">cargar de un archivo<input type="file" accept=".json,application/json" hidden onchange="importarArchivo(this)"></label> · <button class="enlace" onclick="quitarPerfil()">quitar este perfil</button></p></div>`}

/* ---------- Leitner ---------- */
const INTERVALOS=[0,1,3,7,14,30],DIA=86400000,NUEVAS_POR_DIA=10;
let P=nuevoP();
const guardar=()=>store.escribir(store.clave(PERFILES.activo),P);
function marcar(id,ok){const c=P.cards[id]||{box:0,due:0};if(c.nuevo){delete c.nuevo;diaHoy().nuevas++}c.box=ok?Math.min(5,c.box+1):0;c.due=Date.now()+INTERVALOS[c.box]*DIA;P.cards[id]=c;guardar()}
function idsDe(r){const ids=['orden',...r.contexto.map(c=>c.clave),r.tipo==='rio'?'mar':'fin'].map(k=>r.pref+k);r.paradas.forEach((c,i)=>ids.push('ciudad:'+r.id+':'+i));return ids}
function dominio(r){const ids=idsDe(r);let s=0;ids.forEach(id=>{const c=P.cards[id];if(c)s+=c.box});return s/(ids.length*5)}
function sembrar(r){idsDe(r).forEach(id=>{if(!P.cards[id])P.cards[id]={box:0,due:Date.now(),nuevo:true}});guardar()}
/* Hoy: las tarjetas vencidas ya repasadas entran todas; las nuevas (sembradas y nunca respondidas) entran de a NUEVAS_POR_DIA
   por día (P.dia cuenta las que estrenaron hoy); la cola intercala ríos, uno por ronda */
const fechaHoy=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
function diaHoy(){const f=fechaHoy();if(!P.dia||P.dia.fecha!==f)P.dia={fecha:f,nuevas:0};return P.dia}
function colaHoy(){const t=Date.now(),porRio={};Object.keys(P.cards).forEach(id=>{if(P.cards[id].due<=t){const k=id.split(':')[1];(porRio[k]=porRio[k]||[]).push(id)}});
  const listas=mezclar(Object.keys(porRio)).map(k=>mezclar(porRio[k])),mezcla=[];for(let hay=true;hay;){hay=false;for(const l of listas)if(l.length){mezcla.push(l.shift());hay=true}}
  let cupo=NUEVAS_POR_DIA-diaHoy().nuevas;return mezcla.filter(id=>!P.cards[id].nuevo||cupo-->0)}
function nuevasEnEspera(){const t=Date.now(),cola=colaHoy();return Object.keys(P.cards).filter(id=>P.cards[id].nuevo&&P.cards[id].due<=t&&!cola.includes(id)).length}
const pendientes=()=>colaHoy();
function renderHoy(){const cola=colaHoy(),n=cola.length,min=Math.max(1,Math.round(n*15/60)),espera=nuevasEnEspera();
  const rios=[...new Set(cola.map(id=>id.split(':')[1]))].map(rioPor).filter(Boolean).map(r=>r.nombre),cuales=rios.slice(0,3).join(', ')+(rios.length>3?' y más':'');
  return `<div class="hoy"><div class="fkicker">Hoy</div>${n?`<div class="htit">${n} tarjeta${n>1?'s':''} por repasar · unos ${min} min</div><p class="fnota">${esc(cuales)}${rios.length>1?', intercalados':''}.${espera?` Hay ${espera} tarjeta${espera>1?'s':''} nueva${espera>1?'s':''} esperando turno: entran de a ${NUEVAS_POR_DIA} por día.`:''}</p>`:`<div class="htit">Nada pendiente hoy</div><p class="fnota">${espera?`Hay ${espera} tarjeta${espera>1?'s':''} nueva${espera>1?'s':''} esperando turno: mañana entran ${Math.min(espera,NUEVAS_POR_DIA)} más.`:VJ().recorre}</p>`}<div class="acciones"><button class="btn${n?'':' sec'}" onclick="iniciarRepaso()">Repasar${n?` (${n})`:''}</button><button class="btn sec" onclick="iniciarReto()">Reto mundial</button><button class="btn sec" onclick="verPasaporte()">Pasaporte${totalSellos()?` (${totalSellos()})`:''}</button></div></div>`}

/* ---------- preguntas ---------- */
function otrosRios(r,n){const z=zonaDe(r);return mezclar(RUTAS.filter(x=>x.id!==r.id&&zonaDe(x)===z)).concat(mezclar(RUTAS.filter(x=>x.id!==r.id&&zonaDe(x)!==z))).slice(0,n)}
function armar(base,correcta,distractores){const ops=mezclar([correcta,...distractores]);base.opciones=ops;base.correcta=ops.indexOf(correcta);return base}
function preguntaTipo(tipo,r,extra){const V=r.vocab;
  const n=r.paradas.length;
  if(tipo==='ciudad'){const i=extra==null?Math.floor(Math.random()*n):extra,c=r.paradas[i];
    return armar({tipo,rio:r.id,ciudad:i,texto:V.preguntas.ciudad(r,c),nota:c.imagen,cardId:'ciudad:'+r.id+':'+i},esc(r.nombre),otrosRios(r,3).map(x=>esc(x.nombre)))}
  if(tipo==='cerca'){const idx=mezclar(r.paradas.map((c,i)=>i)).slice(0,3),max=Math.max(...idx);
    return armar({tipo,rio:r.id,ciudad:max,texto:V.preguntas.cerca(r),nota:V.preguntas.orden(r),cardId:r.pref+'orden'},esc(r.paradas[max].nombre),idx.filter(i=>i!==max).map(i=>esc(r.paradas[i].nombre)))}
  const cx=r.contexto.find(x=>x.clave===tipo);if(cx){
    return armar({tipo,rio:r.id,ciudad:null,texto:V.preguntas.contexto(r,cx),nota:cx.texto,cardId:r.pref+tipo},esc(r.nombre),otrosRios(r,3).map(x=>esc(x.nombre)))}
  if(tipo==='mar'||tipo==='fin'){const z=zonaDe(r);let fines=[...new Set(mezclar([...new Set(RUTAS.filter(x=>x.fin.nombre!==r.fin.nombre&&zonaDe(x)===z).map(x=>x.fin.nombre))]).concat(mezclar([...new Set(RUTAS.filter(x=>x.fin.nombre!==r.fin.nombre&&zonaDe(x)!==z).map(x=>x.fin.nombre))])))].slice(0,3);
    if(fines.length<3)fines=fines.concat(mezclar(r.paradas.map(c=>c.nombre).filter(nm=>nm!==r.fin.nombre&&!fines.includes(nm))).slice(0,3-fines.length));/* con pocas rutas, etapas del mismo viaje */
    return armar({tipo,rio:r.id,ciudad:null,texto:V.preguntas.fin(r),nota:V.preguntas.finNota(r),cardId:r.pref+(r.tipo==='rio'?'mar':'fin')},esc(r.fin.nombre),fines.map(esc))}
  if(tipo==='siguiente'){const i=extra==null?Math.floor(Math.random()*(n-1)):Math.min(extra,n-2),c=r.paradas[i],sig=i+1;const otras=mezclar(r.paradas.map((x,k)=>k).filter(k=>k!==sig&&k!==i)).slice(0,3).map(k=>esc(r.paradas[k].nombre));
    if(otras.length<3)otras.push(V.preguntas.relleno);/* ríos de cuatro paradas */
    return armar({tipo,rio:r.id,ciudad:sig,texto:V.preguntas.siguiente(r,c),nota:V.preguntas.orden(r),cardId:r.pref+'orden'},esc(r.paradas[sig].nombre),otras)}
  if(tipo==='imagen'){const i=extra==null?Math.floor(Math.random()*n):extra,c=r.paradas[i],otras=mezclar(r.paradas.map((x,k)=>k).filter(k=>k!==i)).slice(0,3);
    return armar({tipo,rio:r.id,ciudad:i,escena:c.escena,texto:V.preguntas.imagen(r,c),nota:c.dato,cardId:'ciudad:'+r.id+':'+i},esc(c.nombre),otras.map(k=>esc(r.paradas[k].nombre)))}
  if(tipo==='pais'){const i=extra==null?Math.floor(Math.random()*n):extra,c=r.paradas[i];
    const dis=[...new Set(mezclar([...new Set(r.paradas.map(x=>x.pais))]).concat(mezclar([...new Set(RUTAS.flatMap(x=>x.paradas.map(y=>y.pais)))])))].filter(p=>p!==c.pais).slice(0,3);
    return armar({tipo,rio:r.id,ciudad:i,texto:`¿En qué país está ${c.nombre}?`,nota:c.dato,cardId:null},esc(c.pais),dis.map(esc))}
  if(tipo==='altura'){const alts=r.paradas.map((c,i)=>alturaParada(r,i));let sel=null;
    for(let k=0;k<8&&!sel&&alts[0]!=null;k++){const g=mezclar(r.paradas.map((c,i)=>i)).slice(0,4),top=g.reduce((m,i)=>alts[i]>alts[m]?i:m,g[0]),seg=Math.max(...g.filter(i=>i!==top).map(i=>alts[i]));if(alts[top]>=seg+25&&alts[top]>=seg*1.15)sel={g,top}}
    if(!sel)return preguntaTipo('cerca',r);/* sin diferencia clara de altura: pregunta de orden */
    return armar({tipo,rio:r.id,ciudad:sel.top,texto:V.preguntas.altura(r),nota:V.preguntas.alturaNota+r.paradas.map((c,i)=>`${c.nombre} ${km(alts[i])} m`).join(' · ')+'.',cardId:null},esc(r.paradas[sel.top].nombre),sel.g.filter(i=>i!==sel.top).map(i=>esc(r.paradas[i].nombre)))}
  if(tipo==='fecha'){const con=r.paradas.map((c,i)=>i).filter(i=>anio(r.paradas[i].fecha)!=null),porAnio={};con.forEach(i=>{const a=anio(r.paradas[i].fecha);if(!(a in porAnio))porAnio[a]=r.paradas[i].fecha});const anos=Object.values(porAnio);if(anos.length<4)return preguntaTipo('cerca',r);
    const i=extra!=null&&r.paradas[extra]&&anio(r.paradas[extra].fecha)!=null?extra:azar(con),c=r.paradas[i],otras=mezclar(anos.filter(a=>anio(a)!==anio(c.fecha))).slice(0,3);
    return armar({tipo,rio:r.id,ciudad:i,texto:V.preguntas.fecha(r,c),nota:V.preguntas.fechaNota(r),cardId:'ciudad:'+r.id+':'+i},esc(c.fecha),otras.map(esc))}
  if(tipo==='orden'){if(n<4)return preguntaTipo('cerca',r);const a=Math.floor(Math.random()*(n-3)),grupo=[a,a+1,a+2,a+3],nombre=g=>g.map(i=>esc(r.paradas[i].nombre)).join(' → '),ok=nombre(grupo),vistos=new Set([ok]),otras=[];let tries=0;
    while(otras.length<3&&tries++<40){const k=nombre(mezclar(grupo));if(!vistos.has(k)){vistos.add(k);otras.push(k)}}
    return armar({tipo,rio:r.id,ciudad:null,texto:V.preguntas.ordenPregunta(r),nota:V.preguntas.orden(r),cardId:r.pref+'orden'},ok,otras)}
  /* frase */
  return armar({tipo:'frase',rio:r.id,ciudad:null,texto:V.preguntas.frase(r),nota:lista(r)+'.',cardId:r.pref+'orden'},marcarFrase(r.frase),otrosRios(r,3).map(x=>marcarFrase(x.frase)))
}
function tiposDisponibles(r){/* tipos de pregunta que se pueden armar para esta ruta en este juego; con menos de cuatro rutas no hay distractores de otras rutas */
  if(RUTAS.length>=4&&r.tipo==='rio')return ['ciudad','imagen','cerca','siguiente','antigua','moderna','mar','frase','pais','altura'];
  const t=['imagen','siguiente','cerca','pais','fin','orden'];if(RUTAS.length>=4)t.push('ciudad','frase',...r.contexto.map(c=>c.clave));if(r.paradas.some(c=>c.fecha))t.push('fecha');if(r.perfil)t.push('altura');return t}
function preguntaDeCard(id){const p=id.split(':'),r=rutaPor(p[1]);if(!r)return null;const T=tiposDisponibles(r);
  if(p[0]==='ciudad')return preguntaTipo(azar(['ciudad','imagen'].filter(t=>T.includes(t)).concat(T.includes('fecha')?['fecha']:[])),r,+p[2]);
  if(p[2]==='orden')return preguntaTipo(azar(['cerca','frase','siguiente'].filter(t=>T.includes(t))),r);
  return preguntaTipo(p[2],r)}
function iniciarQuiz(r){const n=r.paradas.length,a=Math.floor(Math.random()*n);let b=Math.floor(Math.random()*(n-1));if(b>=a)b++;
  const qs=mezclar(RUTAS.length>=4?[preguntaTipo(azar(['ciudad','imagen']),r,a),preguntaTipo('siguiente',r,b),preguntaTipo(azar(['cerca',r.perfil?'altura':'fecha']),r),preguntaTipo(azar(r.contexto.map(c=>c.clave)),r),preguntaTipo(r.tipo==='rio'?'mar':'fin',r),r.tipo==='rio'?preguntaTipo('frase',r):preguntaTipo(azar(['frase','orden']),r)]
    :[preguntaTipo('imagen',r,a),preguntaTipo('siguiente',r,b),preguntaTipo(azar(['cerca','fecha']),r),preguntaTipo('orden',r),preguntaTipo('fin',r),preguntaTipo(azar(['pais','fecha']),r)]);/* con una sola ruta no hay distractores de otras rutas */
  S.quiz={qs,i:0,aciertos:0,resp:null,titulo:r.nombre,modo:'rio',dicho:azar(VZ().pregunta)}}
function iniciarRepaso(){const ids=colaHoy().slice(0,10);
  if(!ids.length){S.pantalla='inicio';S.aviso=VJ().recorreFin;render();return}
  S.pantalla='quiz';S.aviso=null;S.quiz={qs:ids.map(preguntaDeCard).filter(Boolean),i:0,aciertos:0,resp:null,titulo:'Repaso',modo:'repaso'};render()}
function iniciarReto(){const qs=[],claves=new Set();let tries=0;
  while(qs.length<10&&tries++<60){const r=azar(RUTAS),t=azar(tiposDisponibles(r));const q=preguntaTipo(t,r);const k=q.tipo+':'+q.rio+':'+q.ciudad;if(claves.has(k))continue;claves.add(k);qs.push(q)}
  S.pantalla='quiz';S.aviso=null;S.quiz={qs,i:0,aciertos:0,resp:null,titulo:'Reto mundial',modo:'reto'};render()}

/* ---------- estado y navegación ---------- */
const S={pantalla:'inicio',rio:null,tab:'descender',paso:0,orden:null,quiz:null,aviso:null,foco:null,viaje:null,guias:{},llaves:{},dicho:null,rec:null,evento:null,eventosVistos:{},viajeEv:false,perfilNuevo:false,zona:null,selloNuevo:null,dichoLeido:null,bamboleo:false};
function verZona(z){S.zona=z;render(false)}
function abrirRio(id){S.pantalla='rio';S.rio=id;S.tab='descender';S.paso=0;S.aviso=null;S.guias={};S.llaves={};S.dicho=null;S.evento=null;S.eventosVistos={};S.viajeEv=false;iniciarEco();audio.modo=rioPor(id).vocab.sonidoTipo||'agua';prepararGuia(rioPor(id));render()}
function prepararGuia(r){const n=r.paradas.length,p=S.paso;if(p>=n||S.guias[p])return;const otras=mezclar(r.paradas.map((c,i)=>i).filter(i=>i!==p)).slice(0,2);S.guias[p]={objetivo:p,opciones:mezclar([p,...otras]),resp:null,ok:null}}
function responderGuia(i){const r=rioPor(S.rio),g=S.guias[S.paso];if(!g||g.resp!=null)return;g.resp=i;g.ok=i===g.objetivo;S.bamboleo=!g.ok;S.llaves[g.objetivo]=g.ok;marcar('ciudad:'+r.id+':'+g.objetivo,g.ok);
  S.dicho=azar(g.ok?VZ().guiaBien:(S.eco?VZ().guiaMal:VZ().guiaMalH)).replace('{c}',r.paradas[g.objetivo].nombre);if(g.ok)audio.ping(1046);render(false)}
function lanzarEvento(r,def){const p=S.paso,q=def.reto==='imagen'?preguntaTipo('imagen',r,Math.floor(Math.random()*p)):def.reto==='pais'?preguntaTipo('pais',r,def.tramo-1):def.reto==='ruta'?preguntaTipo('siguiente',r,def.tramo-1):preguntaTipo(def.reto,r);
  S.eventosVistos[def.tramo]=true;S.dicho=null;S.viajeEv=true;
  S.evento={def,q,resp:null,ok:null,delta:0,tramo:def.tramo,medio:puntoMedio(r,idxParada(r,p),idxParada(r,def.tramo)),dicho:azar(VZ().eventoAviso)};audio.ping(392);render()}
function responderEvento(i){const E=S.evento;if(!E||E.resp!=null)return;const q=E.q,e=S.eco;E.resp=i;E.ok=i===q.correcta;if(q.cardId)marcar(q.cardId,E.ok);
  if(e&&!e.cerrado){E.delta=E.ok?2:-Math.min(2,e.monedas);e.monedas+=E.delta}
  E.dicho=azar(E.ok?VZ().eventoBien:VZ().eventoMal);if(E.ok)audio.ping(1319);render(false)}
function continuarEvento(){const E=S.evento;if(!E||E.resp==null)return;S.evento=null;paso(1,E)}
const modo=()=>P.modo==='historia'?'historia':'mercader';
function setModo(m){P.modo=m;guardar();render(false)}
function iniciarEco(){S.eco=modo()==='mercader'?{monedas:10,bodega:[],dicho:null,cerrado:false,final:null}:null}
function precio(r,g,j){if(j<g.o)return null;const k=j-g.o;if(g.d&&k>g.d)return 0;let p=g.b*(1+0.5*k);if(g.m===j)p*=2;else if(j===r.paradas.length-1&&k>0)p*=1.25;return Math.round(p)}
function comprar(gi){const r=rioPor(S.rio),g=r.carga[gi],e=S.eco;if(!e||e.cerrado)return;
  if(e.bodega.length>=3)S.dicho=azar(VZ().sinEspacio);else if(e.monedas<g.b)S.dicho=azar(VZ().sinMonedas);else{e.monedas-=g.b;e.bodega.push(gi);S.dicho=azar(VZ().compra).replace('{g}',g.n[0].toUpperCase()+g.n.slice(1));audio.ping(660)}
  render(false)}
function vender(bi){const r=rioPor(S.rio),e=S.eco;if(!e||e.cerrado)return;const g=r.carga[e.bodega[bi]],p=precio(r,g,S.paso-1);e.bodega.splice(bi,1);
  if(p>0){e.monedas+=p;S.dicho=azar(VZ().venta).replace('{n}',p);audio.ping(1046)}else S.dicho=azar(VZ().podrido).replace('{g}',g.n[0].toUpperCase()+g.n.slice(1));
  render(false)}
function cerrarEco(r){const e=S.eco;if(!e||e.cerrado)return;const j=r.paradas.length-1,vend=[];e.bodega.forEach(gi=>{const g=r.carga[gi],p=precio(r,g,j)||0;e.monedas+=p;vend.push(g.n+' · '+p)});e.bodega=[];
  const gan=e.monedas-10;P.tesoro=(P.tesoro||0)+Math.max(0,gan);e.cerrado=true;e.final={fin:e.monedas,gan,vend};S.dicho=VZ().ganancia[gan>=10?0:gan>0?1:2].replace('{n}',gan)+(r.fantasma!=null?' '+(e.monedas>r.fantasma?VZ().fantasma[0]:e.monedas<r.fantasma?VZ().fantasma[1].replace('{n}',r.fantasma):VZ().fantasma[2]):'');guardar()}
function irInicio(){S.pantalla='inicio';S.aviso=null;render()}
function setTab(t){S.tab=t;const r=rioPor(S.rio);if(t==='ordenar')reiniciarOrden(r);if(t==='recitar')iniciarRecitar(r);if(t==='preguntar')iniciarQuiz(r);render()}
function paso(d,tras){const r=rioPor(S.rio),fin=r.paradas.length+1,antes=S.paso;
  if(d>0&&!tras&&!S.evento&&antes<fin){const def=r.eventos.find(e=>e.tramo===antes+1&&!S.eventosVistos[e.tramo]);if(def){lanzarEvento(r,def);return}}
  S.paso=Math.max(0,Math.min(fin,antes+d));S.viaje={de:antes,a:S.paso};if(tras&&tras.medio!=null)S.viaje.medio=tras.medio;audio.remar();S.dicho=null;prepararGuia(r);S.selloNuevo=null;if(d>0&&S.paso>=1&&S.paso<fin&&S.llaves[S.paso-1]===true&&sellar(r,S.paso-1)){S.selloNuevo=claveSello(r,S.paso-1);audio.ping(1318)}if(S.paso===fin){cerrarEco(r);if(!P.vistos[r.id]){P.vistos[r.id]=true;sembrar(r)}}render()}
function reiniciarOrden(r){S.orden={pool:mezclar(r.paradas.map((c,i)=>i)),seq:[],errores:0,listo:false,fallo:null,dicho:azar(VZ().ordenInicio)}}
function tocarChip(i){const o=S.orden,r=rioPor(S.rio);if(o.listo)return;
  if(i===o.seq.length){o.seq.push(i);o.pool=o.pool.filter(x=>x!==i);o.fallo=null;o.dicho=azar(VZ().ordenBien);if(!o.pool.length){o.listo=true;o.dicho=VZ().ordenFin[o.errores===0?0:o.errores===1?1:2];if(S.eco&&o.errores<=1){o.premio=o.errores===0?5:2;P.tesoro=(P.tesoro||0)+o.premio;o.dicho+=` +${o.premio} monedas al tesoro.`}marcar(r.pref+'orden',o.errores<=1)}}
  else{o.errores++;o.fallo=i;o.dicho=azar(VZ().ordenMal);setTimeout(()=>{if(S.orden===o&&o.fallo===i){o.fallo=null;render(false)}},600)}
  render(false)}
function responder(i){const q=S.quiz.qs[S.quiz.i];if(S.quiz.resp!=null)return;S.quiz.resp=i;const ok=i===q.correcta;S.quiz.dicho=azar(ok?VZ().quizBien:VZ().quizMal);if(ok)S.quiz.aciertos++;if(q.cardId)marcar(q.cardId,ok);render(false)}
function siguiente(){S.quiz.i++;S.quiz.resp=null;S.quiz.dicho=azar(VZ().pregunta);render()}
function otraRonda(){if(S.quiz.modo==='rio'){iniciarQuiz(rioPor(S.rio));render()}else if(S.quiz.modo==='repaso')iniciarRepaso();else iniciarReto()}

/* ---------- render ---------- */
function cabecera(t,sub,volver){return `${volver?`<button class="volver" onclick="irInicio()" aria-label="${VJ().volver}">‹ ${VJ().Tipos}</button>`:''}<div><h1>${esc(t)}</h1>${sub?`<div class="sub">${esc(sub)}</div>`:''}</div><button class="son${audio.on?' on':''}" onclick="audio.toggle()" aria-pressed="${audio.on}" title="${VJ().sonido}">≈</button>`}
function globoNeutro(texto){GLOBO=true;return `<div class="globo neutro"><span class="emo" aria-hidden="true"><svg class="barca" viewBox="-15 -16 30 22">${glifo('cuadrada')}</svg></span><div class="dice"><b>Cauces:</b> ${esc(texto||azar(VZ().pregunta))} ${htmlVoz()}</div></div>`}
function globo(r,texto,extra){const m=r&&r.companero;if(!m||!texto)return '';GLOBO=true;return `<div class="globo${extra?' '+extra:''}"><span class="emo" aria-hidden="true">${animal(m)}</span><div class="dice"><b>${esc(m.nombre)}:</b> ${esc(texto)} ${htmlVoz()}</div></div>`}
function bloqueFrase(r,conLista){return `<div class="frase"><div class="fkicker">Frase para el orden</div><div class="ftexto">${marcarFrase(r.frase)}</div>${r.fraseNota?`<div class="fnota">${esc(r.fraseNota)}</div>`:''}${conLista?`<div class="flista">${esc(lista(r))}</div>`:''}</div>`}
function tabs(){return `<div class="tabs">${[['descender',VJ().bajar],['ordenar','Ordenar'],['recitar','Recitar'],['preguntar','Preguntar']].map(([k,t])=>`<button class="${S.tab===k?'on':''}" onclick="setTab('${k}')">${t}</button>`).join('')}</div>`}
function renderInicio(){const n=pendientes().length;
  const fila=r=>`<button class="fila" onclick="abrirRio('${r.id}')"><span class="fnombre">${r.companero?`<span class="emo" aria-hidden="true">${animal(r.companero)}</span>`:''}${esc(r.nombre)}</span><span class="fmeta">${r.vocab.fila(r)}${completo(r)?' · completo':sellosDe(r)?` · ${sellosDe(r)} sello${sellosDe(r)>1?'s':''}`:P.vistos[r.id]?' · recorrido':''}</span><span class="barra"><i style="width:${Math.round(dominio(r)*100)}%"></i></span></button>`;
  const porLargo=(a,b)=>(b.longitud||0)-(a.longitud||0);
  const grupos=JUEGO.grupos.map(g=>`<div class="fkicker${g.clase?' '+g.clase:''}">${g.titulo}</div>${g.nota?`<p class="fnota">${g.nota}</p>`:'\n'}${g.antes?g.antes+'\n':''}<div class="lista">${RUTAS.filter(g.filtro).sort(porLargo).map(fila).join('')}</div>`).join('\n');
  return `${renderPerfiles()}
${renderHoy()}
${S.aviso?`<div class="aviso">${esc(S.aviso)}</div>`:''}
${modo()==='mercader'?`<div class="tesoro">🪙 Tesoro: ${P.tesoro||0} monedas · ${rango(P.tesoro||0)}</div>`:''}
<p class="pie">${VJ().toca}</p>
${grupos}
<details class="mas ajustes"><summary>¿Cómo se juega?</summary>${JUEGO.comoSeJuega}</details>
<details class="mas ajustes"><summary>Ajustes: modo, voz y progreso</summary><div class="fkicker">Modo de juego</div><div class="tabs modo"><button class="${esNino()?'on':''}" onclick="setModo('mercader')">Niño</button><button class="${esNino()?'':'on'}" onclick="setModo('historia')">Adulto</button></div><p class="fnota">${esNino()?VJ().ajustesNino:VJ().ajustesAdulto}</p>${esNino()&&voz.soporte()?`<div class="tabs modo"><button class="${P.voz!=='boton'?'on':''}" onclick="setVoz('auto')">🔊 Lee sola</button><button class="${P.voz==='boton'?'on':''}" onclick="setVoz('boton')">Solo con el botón</button></div><p class="fnota">Con «Lee sola», el animal lee cada pantalla al abrirla y lo que dice al responder.</p>`:''}${renderProgreso()}</details>`}
function renderDescender(r){if(S.evento)return renderEvento(r);const V=r.vocab;const n=r.paradas.length,p=S.paso;
  if(p===0)return `${globo(r,S.dicho||(r.companero&&r.companero.hola))}<p class="kicker">${botonVoz()}${V.kickerInicio(r)}${r.perfil?` · ${km(r.perfil[0][1])} m sobre el mar`:''}</p><h2>${esc(r.inicio.nombre)}</h2>${escena(r.inicio.escena)}<p>${esc(r.inicio.nota)}</p>${r.vehiculo?`<div class="nave"><svg class="barca mini" viewBox="-15 -15 30 20" aria-hidden="true">${glifo(r.vehiculo.tipo)}</svg><div class="fkicker">${V.tuVehiculo}</div><div class="ntit">${esc(r.vehiculo.nombre)}</div><p>${esc(r.vehiculo.desc)}</p><div class="fnota">${S.eco?V.zarpas+(r.fantasma!=null?` El ${V.mercader} suele llegar con ${r.fantasma}; a ver si le ganás.`:''):esc(r.vehiculo.zarpe)}</div></div>`:''}${mas(V.contame(r.contexto[0]),`<p>${esc(r.contexto[0].texto)}</p>`,r.contexto[0].titulo)}${bloqueFrase(r,true)}${renderGuia(r)}<div class="nav"><span></span>${botonZarpar(r)}</div>`;
  if(p<=n){const c=r.paradas[p-1];
    const prev=p>1?r.paradas[p-2]:null;
    return `${globo(r,S.dicho||(r.companero&&r.companero.paradas[p-1]))}<p class="kicker">${botonVoz()}${V.kickerParada(r,p,n,c)}</p><h2>${esc(c.nombre)}</h2><div class="pais">${esc(c.pais)} · ${V.tramo(r,c,prev)}${textoAltura(r,p-1)}</div>${escena(c.escena)}<div class="imagen"><div class="fkicker">Imagen para recordar</div>${esc(c.imagen)}</div>${mas('Contame más',`<p>${esc(c.dato)}</p>`)}${renderSello(r,p-1)}${!S.eco&&c.puerto?`<div class="puerto"><div class="fkicker">${V.enPuerto}</div><p>${esc(c.puerto)}</p><div class="bodega">${V.llevaba}: ${esc(c.carga)}</div></div>`:''}${renderMercado(r,p-1)}${renderGuia(r)}<div class="nav"><button class="btn sec" onclick="paso(-1)">‹ Atrás</button>${p===n?`<button class="btn" onclick="paso(1)">${V.llegarFin} ›</button>`:botonZarpar(r)}</div>`}
  const f=S.eco&&S.eco.final;
  return `${globo(r,S.dicho||(r.companero&&r.companero.fin))}<p class="kicker">${botonVoz()}${V.kickerFin(r)}</p><h2>${esc(r.fin.nombre)}</h2>${escena(r.fin.escena)}<p>${esc(V.llegada(r))}</p>${f?`<div class="mercado"><div class="fkicker">Cuentas del viaje</div><p>${V.cuentas} ${f.fin}.${f.vend.length?` ${V.sobrante} ${esc(r.paradas[r.paradas.length-1].nombre)}: ${esc(f.vend.join(', '))}.`:''} ${f.gan>0?`Ganancia: ${f.gan}.`:'Sin ganancia esta vez.'}${r.fantasma!=null?` El ${V.mercader} llegó con ${r.fantasma}.`:''}</p><div class="bolsa">🪙 Tesoro: ${P.tesoro||0} monedas · ${rango(P.tesoro||0)}</div></div>`:''}${r.vehiculo?`<div class="nave"><svg class="barca mini" viewBox="-15 -15 30 20" aria-hidden="true">${glifo(r.vehiculo.tipo)}</svg><div class="fkicker">${esc(r.vehiculo.nombre)}</div><p>${esc(r.vehiculo.llegada)}</p></div>`:''}${mas(V.contame(r.contexto[1]),`<p>${esc(r.contexto[1].texto)}</p>`,r.contexto[1].titulo)}${bloqueFrase(r,true)}<div class="nav"><button class="btn sec" onclick="paso(-1)">‹ Atrás</button><button class="btn" onclick="setTab('ordenar')">Ordenar de memoria ›</button></div>`}
function renderGuia(r){const g=S.guias[S.paso];if(!g||S.paso>=r.paradas.length)return '';
  const chips=g.opciones.map(i=>{let cls='chip';if(g.resp!=null){if(i===g.objetivo)cls+=' bien';else if(i===g.resp)cls+=' mal'}return `<button class="${cls}" onclick="responderGuia(${i})"${g.resp!=null?' disabled':''}>${esc(r.paradas[i].nombre)}</button>`}).join('');
  return `<div class="guia"><div class="fkicker">${r.vocab.proxima}</div><div class="chips">${chips}</div></div>`}
function renderEvento(r){const E=S.evento,d=E.def,q=E.q,n=r.paradas.length;
  const V=r.vocab,de=S.paso===0?V.entreInicio:r.paradas[S.paso-1].nombre,hacia=E.tramo<=n?r.paradas[E.tramo-1].nombre:V.entreFin;
  const ops=q.opciones.map((o,i)=>{let cls='op';if(E.resp!=null){if(i===q.correcta)cls+=' bien';else if(i===E.resp)cls+=' mal';else cls+=' apagada'}return `<button class="${cls}" onclick="responderEvento(${i})">${o}</button>`}).join('');
  const fin=E.resp==null?'':`<div class="nota${E.ok?'':' no'}">${esc(E.ok?d.bien:d.mal)}${E.delta?` ${E.delta>0?'+':'−'}${Math.abs(E.delta)} monedas.`:''} ${esc(q.nota)}</div><div class="nav"><span></span><button class="btn" onclick="continuarEvento()">Seguir hacia ${esc(hacia)} ›</button></div>`;
  return `${globo(r,E.dicho,'salta')}<p class="kicker">${botonVoz()}Entre ${esc(de)} y ${esc(hacia)}</p><div class="evento"><span class="eicono" aria-hidden="true">${d.icono}</span><div><div class="etit">${esc(d.titulo)}</div><p>${esc(d.texto)}</p></div></div><p class="pregunta">${esc(q.texto)}</p><div class="opciones">${ops}</div>${fin}`}
function botonZarpar(r){const g=S.guias[S.paso];if(!g)return '<button class="btn" onclick="paso(1)">Siguiente ›</button>';if(g.resp==null)return '<span></span>';return `<button class="btn" onclick="paso(1)">${r.vocab.avanzar} ${esc(r.paradas[g.objetivo].nombre)} ›</button>`}
function renderMercado(r,j){const V=r.vocab;const e=S.eco;if(!e||!r.carga.length)return '';const c=r.paradas[j];
  if(e.cerrado)return `<div class="mercado"><div class="fkicker">${V.mercado} ${esc(c.nombre)}</div><p>${V.cerrado}</p></div>`;
  const slots=e.bodega.map((gi,bi)=>{const g=r.carga[gi],p=precio(r,g,j);return `<button class="item" onclick="vender(${bi})"><span class="ie">${g.e}</span>${esc(g.n)}<span class="ip">${p>0?`vender · ${p}`:'podrido · tirar'}</span></button>`}).join('')+Array(Math.max(0,3-e.bodega.length)).fill('<span class="item vacio">—</span>').join('');
  const abierto=S.llaves[j]!==false;
  const oferta=!abierto?'':r.carga.map((g,gi)=>({g,gi})).filter(x=>x.g.o===j).map(({g,gi})=>{const pista=g.d?`se pasa en ${g.d} ${g.d>1?V.puertosS:V.puertoS}`:g.m!=null?`se paga mejor en ${esc(oculta(r.paradas[g.m].nombre))}`:V.masAdelante;const no=e.monedas<g.b||e.bodega.length>=3;return `<button class="item${no?' no':''}" onclick="comprar(${gi})"><span class="ie">${g.e}</span>${esc(g.n)}<span class="ip">comprar · ${g.b}</span><small>${pista}</small></button>`}).join('');
  return `<div class="mercado"><div class="fkicker">${V.mercado} ${esc(c.nombre)}</div><div class="bolsa">🪙 ${e.monedas} monedas · ${V.carga} ${e.bodega.length} de 3</div><div class="slots">${slots}</div>${!abierto?`<small>${V.soloVender}</small>`:oferta?`<div class="fkicker">${V.seVende}</div><div class="slots">${oferta}</div>`:`<small>${V.nadaQueComprar}</small>`}</div>`}
function iniciarRecitar(r){const d=dominio(r);S.rec={i:0,revelada:false,pista:d<0.3?'frase':d<0.7?'iniciales':'nada',ok:[],dicho:azar(VZ().recitarInicio),premio:0}}
function setPista(p){S.rec.pista=p;render(false)}
function revelar(){S.rec.revelada=true;render(false)}
function recordada(ok){const r=rioPor(S.rio),R=S.rec,n=r.paradas.length;if(R.i>=n||!R.revelada)return;marcar('ciudad:'+r.id+':'+R.i,ok);R.ok.push(ok);R.dicho=azar(ok?VZ().recitarBien:VZ().recitarMal);R.i++;R.revelada=false;
  if(R.i>=n){const todas=R.ok.every(Boolean);R.dicho=VZ().recitarFin[todas?0:R.ok.filter(Boolean).length>=n-1?1:2];if(S.eco&&todas){R.premio=R.pista==='nada'?5:R.pista==='iniciales'?3:1;P.tesoro=(P.tesoro||0)+R.premio;R.dicho+=` +${R.premio} monedas al tesoro.`;guardar()}}
  render(false)}
function renderRecitar(r){const V=r.vocab,R=S.rec,n=r.paradas.length;
  const sel=`<div class="tabs modo"><button class="${R.pista==='frase'?'on':''}" onclick="setPista('frase')">Frase</button><button class="${R.pista==='iniciales'?'on':''}" onclick="setPista('iniciales')">Iniciales</button><button class="${R.pista==='nada'?'on':''}" onclick="setPista('nada')">Sin pista</button></div>`;
  const pista=R.pista==='frase'?`<div class="frase"><div class="ftexto">${marcarFrase(r.frase)}</div></div>`:R.pista==='iniciales'?`<div class="frase"><div class="ftexto">${r.paradas.map(c=>esc(c.nombre[0])).join(' · ')}</div></div>`:'';
  const seq=`<div class="secuencia"><span class="extremo">${V.extremoInicio}</span>${r.paradas.map((c,i)=>i<R.i?`<span class="puesto${R.ok[i]?'':' no'}">${esc(c.nombre)}</span>`:i===R.i&&R.revelada?`<span class="puesto actual">${esc(c.nombre)}</span>`:'<span class="hueco">—</span>').join('')}<span class="extremo">${V.extremoFin}</span></div>`;
  let cuerpo;
  if(R.i>=n){const ok=R.ok.filter(Boolean).length;cuerpo=`<div class="nota${ok===n?'':' no'}">${ok} de ${n} recordadas${R.premio?` · +${R.premio} monedas al tesoro`:''}.${ok===n&&R.pista!=='nada'?' Probá con menos pista.':''}</div><div class="acciones"><button class="btn" onclick="setTab('recitar')">Otra vez</button><button class="btn sec" onclick="setTab('preguntar')">Preguntar ›</button></div>`}
  else if(!R.revelada)cuerpo=`<p class="pregunta">${V.Parada} ${R.i+1} de ${n}: decila en voz alta, o en tu cabeza, y después revelá.</p><div class="acciones"><button class="btn" onclick="revelar()">Revelar</button></div>`;
  else cuerpo=`<h2>${esc(r.paradas[R.i].nombre)}</h2><div class="pais">${esc(r.paradas[R.i].pais)}</div><div class="acciones"><button class="btn" onclick="recordada(true)">La sabía</button><button class="btn sec" onclick="recordada(false)">No la sabía</button></div>`;
  return `${globo(r,R.dicho)}<p class="kicker">${botonVoz()}Recitar · el palacio, habitación por habitación</p>${sel}${pista}${seq}${cuerpo}`}
function renderOrden(r){const V=r.vocab,o=S.orden,n=r.paradas.length;
  const seq=`<div class="secuencia"><span class="extremo">${V.extremoInicio}</span>${o.seq.map(i=>`<span class="puesto">${esc(r.paradas[i].nombre)}</span>`).join('')}${o.pool.map(()=>'<span class="hueco">—</span>').join('')}<span class="extremo">${V.extremoFin}</span></div>`;
  const chips=`<div class="chips">${o.pool.map(i=>`<button class="chip${o.fallo===i?' mal':''}" onclick="tocarChip(${i})">${esc(r.paradas[i].nombre)}</button>`).join('')}</div>`;
  const pista=o.errores>=2&&!o.listo?`<div class="pista">${bloqueFrase(r,false)}</div>`:'';
  const fin=o.listo?`<div class="nota${o.errores>1?' no':''}">${o.errores===0?V.ordenBien+(o.premio?` +${o.premio} monedas al tesoro.`:''):o.errores===1?'Un error: cuenta como acierto, pero repasalo.'+(o.premio?` +${o.premio} monedas al tesoro.`:''):V.ordenMal(o.errores)}</div><div class="acciones"><button class="btn" onclick="setTab('preguntar')">Preguntar ›</button><button class="btn sec" onclick="setTab('ordenar')">Otra vez</button></div>`:'';
  return `${globo(r,o.dicho)}<p class="kicker">${botonVoz()}Ordenar</p><p class="pregunta">${V.tocaEnOrden(n)}</p>${seq}${o.listo?'':chips}${pista}${fin}`}
function renderQuiz(){const Q=S.quiz,n=Q.qs.length;
  if(Q.i>=n){const k=nivelQuiz(Q),msg=MSG_QUIZ(vocabQuiz())[k];
    const rm=Q.modo==='rio'?rioPor(S.rio):null;
    return `${rm?globo(rm,VZ().resultado[k]):''}<div class="resultado"><p class="kicker">${botonVoz()}${esc(Q.titulo)}</p><h2>${Q.aciertos} de ${n}</h2><p>${msg}</p><div class="acciones"><button class="btn" onclick="otraRonda()">Otra ronda</button><button class="btn sec" onclick="irInicio()">Volver a los ríos</button></div></div>`}
  const q=Q.qs[Q.i],resp=Q.resp;
  const ops=q.opciones.map((o,i)=>{let cls='op';if(resp!=null){if(i===q.correcta)cls+=' bien';else if(i===resp)cls+=' mal';else cls+=' apagada'}return `<button class="${cls}" onclick="responder(${i})">${o}</button>`}).join('');
  const nota=resp!=null?`<div class="nota${resp===q.correcta?'':' no'}">${esc(q.nota)}</div><div class="nav"><span></span><button class="btn" onclick="siguiente()">${Q.i+1===n?'Ver resultado ›':'Siguiente ›'}</button></div>`:'';
  const rq=Q.modo==='rio'?rioPor(S.rio):(resp!=null?rioPor(q.rio):null);
  return `${rq?globo(rq,Q.dicho):globoNeutro(Q.dicho)}<p class="kicker">${botonVoz()}Pregunta ${Q.i+1} de ${n} · ${esc(Q.titulo)}</p>${q.escena?escena(q.escena,'quiz'):''}<p class="pregunta">${esc(q.texto)}</p><div class="opciones">${ops}</div>${nota}`}
function render(scroll){voz.callar();GLOBO=false;const arriba=document.getElementById('arriba');if(arriba)arriba.classList.toggle('portada',S.pantalla==='inicio'||S.pantalla==='pasaporte');
  const cab=$('#cab'),panel=$('#panel');
  if(S.pantalla==='inicio'){cab.innerHTML=cabecera(JUEGO.nombre,JUEGO.sub);panel.innerHTML=renderInicio();renderMapa(S.zona?{modo:'zona',zona:S.zona,tocar:true}:{modo:'mundo',tocar:true})}
  else if(S.pantalla==='pasaporte'){cab.innerHTML=cabecera('Pasaporte',`${totalSellos()} sellos · ${RUTAS.filter(completo).length} ${VJ().completos}`,true);panel.innerHTML=renderPasaporte();renderMapa(S.zona?{modo:'zona',zona:S.zona,tocar:true}:{modo:'mundo',tocar:true})}
  else if(S.pantalla==='rio'){const r=rioPor(S.rio);cab.innerHTML=cabecera(r.nombre,r.vocab.cabecera(r),true);
    panel.innerHTML=tabs()+(S.tab==='descender'?renderDescender(r):S.tab==='ordenar'?renderOrden(r):S.tab==='recitar'?renderRecitar(r):renderQuiz());renderMapa(focoRio(r))}
  else{cab.innerHTML=cabecera(S.quiz.titulo,S.quiz.modo==='repaso'?'Lo que ya toca volver a ver':VJ().retoSub,true);panel.innerHTML=renderQuiz();renderMapa(focoQuiz(S.quiz.qs[S.quiz.i],null))}
  const pf=document.getElementById('perfil');if(pf){const rp=S.pantalla==='rio'?rioPor(S.rio):null,ok=!!(rp&&conFranja(rp));pf.hidden=!ok;pf.innerHTML=ok?perfilSVG(rp):''}
  if(leeSola()&&S.pantalla!=='inicio'){if(scroll!==false){S.dichoLeido=dichoActual();voz.decir(lectura())}else{const d=dichoActual();if(d&&d!==S.dichoLeido){S.dichoLeido=d;voz.decir([d])}}}
  if(scroll!==false)window.scrollTo(0,0)}

/* ---------- foco del mapa ---------- */
function focoRio(r){const n=r.paradas.length,f={modo:'rio',rio:r,tocar:false,etiquetas:new Set(),actual:null,halo:null};
  if(S.tab==='descender'){
    if(S.evento){for(let i=0;i<S.paso;i++)f.etiquetas.add(i);const m=S.evento.medio,de=idxParada(r,S.paso);f.corte=m.k;f.extra=[r.curso[m.k],m.pt];
      f.barca={poly:r.curso.slice(de,m.k+1).concat([m.pt]),t0:S.viajeEv?0:1,t1:1};S.viajeEv=false;f.frac=(S.paso+0.5)/(n+1);return f}
    if(S.paso===0)f.halo=r.curso[0];else if(S.paso<=n){for(let i=0;i<S.paso;i++)f.etiquetas.add(i);f.actual=S.paso-1}else{for(let i=0;i<n;i++)f.etiquetas.add(i);f.halo=r.curso[r.curso.length-1]}
    const a=idxParada(r,S.paso);let de=a,poly=null;if(S.viaje&&S.viaje.a===S.paso){const m=S.viaje.medio;if(m)poly=[m.pt].concat(r.curso.slice(m.k+1,a+1));else de=idxParada(r,S.viaje.de)}S.viaje=null;f.corte=a;f.barca=poly?{poly,t0:0,t1:1}:{de,a};f.frac=S.paso/(n+1)}
  else if(S.tab==='ordenar'){S.orden.seq.forEach(i=>f.etiquetas.add(i));if(S.orden.listo)for(let i=0;i<n;i++)f.etiquetas.add(i);Object.assign(f,estacionada(r))}
  else if(S.tab==='recitar'){const R=S.rec;for(let i=0;i<Math.min(R.i,n);i++)f.etiquetas.add(i);if(R.i<n&&R.revelada){f.etiquetas.add(R.i);f.actual=R.i}Object.assign(f,estacionada(r))}
  else return focoQuiz(S.quiz.qs[S.quiz.i],r);
  return f}
/* la barca queda estacionada en la parada actual cuando no se está descendiendo, para que el animal no desaparezca del mapa */
const estacionada=r=>{const a=idxParada(r,S.paso);return{corte:a,barca:{de:a,a},frac:S.paso/(r.paradas.length+1)}};
function focoQuiz(q,rDef){
  if(!q){if(rDef){const f={modo:'rio',rio:rDef,tocar:false,etiquetas:new Set(rDef.paradas.map((c,i)=>i)),actual:null,halo:null,...estacionada(rDef)};return f}return{modo:'mundo',tocar:false}}
  const r=rioPor(q.rio);
  const est=rDef&&rDef.id===r.id?estacionada(rDef):{};
  if(S.quiz.resp==null){if(q.tipo==='cerca'||q.tipo==='siguiente'||q.tipo==='imagen'||q.tipo==='pais')return{modo:'rio',rio:r,tocar:false,etiquetas:new Set(),actual:null,halo:null,...est};return{modo:'mundo',tocar:false}}
  return{modo:'rio',rio:r,tocar:false,etiquetas:new Set(r.paradas.map((c,i)=>i)),actual:q.ciudad,halo:null,...est}}

/* ---------- mapa ---------- */
const proj=p=>[(p[1]+180)/360*1000,(90-p[0])/180*500];
const trazo=pts=>pts.map((p,i)=>{const q=proj(p);return (i?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1)}).join('');
const trazoTramo=(r,a,b)=>{let d='';for(let i=a;i<=b;i++){const q=proj(r.curso[i]);d+=(i===a||r.cortes.includes(i)?'M':'L')+q[0].toFixed(1)+' '+q[1].toFixed(1)}return d};/* vértices a..b del trazo; cada segmento nuevo (cortes) empieza con M */
function vbPara(pts,minW,margen){const m=$('#mapa'),asp=(m.clientWidth||380)/(m.clientHeight||260);
  let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;pts.forEach(p=>{const q=proj(p);x0=Math.min(x0,q[0]);y0=Math.min(y0,q[1]);x1=Math.max(x1,q[0]);y1=Math.max(y1,q[1])});
  let w=(x1-x0)*margen,h=(y1-y0)*margen;const cx=(x0+x1)/2,cy=(y0+y1)/2;w=Math.max(w,minW);h=Math.max(h,minW/asp);if(w/h<asp)w=h*asp;else h=w/asp;return{x:cx-w/2,y:cy-h/2,w,h}}
let VB=null,anim=null;
function setVB(t,inmediato){const svg=$('#svg'),fmt=v=>`${v.x.toFixed(2)} ${v.y.toFixed(2)} ${v.w.toFixed(2)} ${v.h.toFixed(2)}`;
  const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;if(anim)cancelAnimationFrame(anim);
  if(inmediato||!VB||reduce){VB=t;svg.setAttribute('viewBox',fmt(t));return}
  const de={...VB},t0=performance.now();
  const step=now=>{let k=Math.min(1,(now-t0)/500);k=1-Math.pow(1-k,3);const v={x:de.x+(t.x-de.x)*k,y:de.y+(t.y-de.y)*k,w:de.w+(t.w-de.w)*k,h:de.h+(t.h-de.h)*k};svg.setAttribute('viewBox',fmt(v));VB=v;if(k<1)anim=requestAnimationFrame(step);else{VB=t;anim=null}};
  anim=requestAnimationFrame(step)}
function colocar(q,nombre,puestos,px){const w=nombre.length*6.6*px,alto=12*px;
  const cands=[[6,4,'start'],[6,-9,'start'],[6,16,'start'],[-6,4,'end'],[-6,-9,'end'],[-6,16,'end']];
  for(const [dx,dy,an] of cands){const x=q[0]+dx*px,y=q[1]+dy*px;const box={x0:an==='end'?x-w:x,x1:an==='end'?x:x+w,y0:y-alto,y1:y+3*px};
    if(!puestos.some(b=>box.x0<b.x1&&box.x1>b.x0&&box.y0<b.y1&&box.y1>b.y0)){puestos.push(box);return[x,y,an]}}
  const x=q[0]+6*px,y=q[1]+4*px;return[x,y,'start']}
const TERRESTRES={caravana:1,pie:1,jinete:1};
function ventana(r){/* cámara por tramo: de la parada anterior a la siguiente, por el trazo */const n=r.paradas.length,p=S.paso,de=idxParada(r,Math.max(0,p-1)),a=idxParada(r,Math.min(n+1,p+1));return r.curso.slice(de,a+1)}
function renderMapa(foco,inmediato){S.foco=foco;const capa=$('#capa'),m=$('#mapa');let pts,vb;
  if(foco.modo==='mundo'){pts=[];RUTAS.forEach(r=>pts.push(...r.curso));vb=vbPara(pts,60,1.08)}
  else if(foco.modo==='zona'){pts=[];RUTAS.filter(r=>r.zona===foco.zona).forEach(r=>pts.push(...r.curso,...r.paradas.map(c=>c.pos)));vb=vbPara(pts,3,1.25)}
  else{const r=foco.rio;pts=r.camara==='tramo'&&S.pantalla==='rio'&&S.tab==='descender'?ventana(r):r.curso.concat(r.paradas.map(c=>c.pos));vb=vbPara(pts,r.zona?3:20,1.3)}
  setVB(vb,inmediato);const px=vb.w/(m.clientWidth||380),f=v=>(v*px).toFixed(2);const activo=foco.rio?foco.rio.id:null,enZona=foco.modo==='zona';let h='';
  const zr=foco.modo==='mundo'?'':enZona?foco.zona:(foco.rio.zona||'mundo'),rel=document.getElementById('relieve');/* franjas de altura: solo al acercarse (están recortadas a las vistas de los ríos) */
  if(rel){if(rel._z!==zr){rel._z=zr;rel.innerHTML=zr&&RELIEVE[zr]?RELIEVE[zr].map(([a,d])=>`<path class="a${a}" d="${d}"/>`).join(''):''}rel.setAttribute('stroke-width',f(1.2))}
  RUTAS.forEach(r=>{const cls=activo?(r.id===activo?' activo':' tenue'):(enZona&&r.zona!==foco.zona?' tenue':'');
    r.ramas.forEach(b=>{h+=`<path class="rio brazo${cls}" d="${trazo(b)}" stroke-width="${f(1.6)}"/>`});
    if(r.id===activo&&foco.corte!=null){h+=`<path class="rio activo resto" d="${trazoTramo(r,foco.corte,r.curso.length-1)}" stroke-width="${f(2.4)}"/>`;if(foco.corte>0)h+=`<path class="rio activo" d="${trazoTramo(r,0,foco.corte)}" stroke-width="${f(3.4)}"/>`;if(foco.extra)h+=`<path class="rio activo" d="${trazo(foco.extra)}" stroke-width="${f(3.4)}"/>`}
    else h+=`<path class="rio${cls}${!activo&&completo(r)?' hecho':''}" d="${trazoTramo(r,0,r.curso.length-1)}" stroke-width="${f(r.id===activo?3:2.2)}"/>`;
    if(foco.tocar&&(enZona?r.zona===foco.zona:!r.zona))h+=`<path class="hit" d="${trazoTramo(r,0,r.curso.length-1)}" stroke-width="${f(18)}" onclick="abrirRio('${r.id}')"/>`});
  const puestos=[];
  if(zr){const rid=foco.rio?foco.rio.id:null;NOMBRES_RELIEVE.forEach(L=>{if(L.z!==zr)return;let p=L.p,a=L.a||0;if(L.v){const v=rid&&L.v[rid];if(!v)return;p=v;a=v[2]||0}
    const q=proj(p);if(q[0]<vb.x-2*px||q[0]>vb.x+vb.w+2*px||q[1]<vb.y||q[1]>vb.y+vb.h)return;
    if(L.t==='pico'){if(!foco.rio)return;/* los picos solo al acercarse a un río; en la zona entera se amontonan */
      const t=`${L.n} ${km(L.e)} m`,[x,y,an]=colocar(q,t,puestos,px);h+=`<path class="pico" d="M${q[0].toFixed(1)} ${(q[1]-4.5*px).toFixed(1)}l${f(3.6)} ${f(6.8)}h${f(-7.2)}z" stroke-width="${f(.8)}"/><text class="etq relieve pico" x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${f(10)}" stroke-width="${f(2.5)}" text-anchor="${an}">${esc(t)}</text>`;return}
    const w=L.n.length*(L.t==='llano'?5.6:7.6)*px,rad=a*Math.PI/180,bw=Math.abs(Math.cos(rad))*w+Math.abs(Math.sin(rad))*12*px,bh=Math.abs(Math.sin(rad))*w+Math.abs(Math.cos(rad))*12*px;
    h+=`<text class="etq relieve ${L.t}" x="${q[0].toFixed(1)}" y="${q[1].toFixed(1)}" font-size="${f(L.t==='llano'?10.5:9.5)}" stroke-width="${f(2.5)}" text-anchor="middle"${a?` transform="rotate(${a} ${q[0].toFixed(1)} ${q[1].toFixed(1)})"`:''}>${esc(L.n)}</text>`;
    puestos.push({x0:q[0]-bw/2,x1:q[0]+bw/2,y0:q[1]-bh/2-4*px,y1:q[1]+bh/2})})}
  if(foco.modo==='mundo')for(const z in ZONAS){const q=proj(ZONAS[z].pos);h+=`<circle class="zona" cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${f(4.5)}" stroke-width="${f(1.5)}"/><text class="etq" x="${(q[0]+7*px).toFixed(1)}" y="${(q[1]+4*px).toFixed(1)}" font-size="${f(12)}" stroke-width="${f(3)}">${esc(ZONAS[z].nombre)}</text>${foco.tocar?`<circle class="hitz" cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${f(18)}" onclick="verZona('${z}')"><title>Ríos de ${esc(ZONAS[z].nombre)}</title></circle>`:''}`}
  if(enZona){RUTAS.filter(r=>r.zona===foco.zona).forEach(r=>{const q=proj(r.curso[Math.floor(r.curso.length/2)]),[x,y,an]=colocar(q,r.nombre,puestos,px);h+=`<text class="etq" x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${f(12)}" stroke-width="${f(3)}" text-anchor="${an}">${esc(r.nombre)}</text>`})}
  if(foco.rio){const r=foco.rio;
    r.paradas.forEach((c,i)=>{const q=proj(c.pos),on=foco.etiquetas.has(i);h+=`<circle class="ciudad${on?' on':''}" cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${f(3.5)}"/>`;
      if(foco.actual===i)h+=`<circle class="halo" cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${f(5)}" stroke-width="${f(1.5)}"/>`});
    if(foco.halo){const q=proj(foco.halo);h+=`<circle class="halo" cx="${q[0].toFixed(1)}" cy="${q[1].toFixed(1)}" r="${f(5)}" stroke-width="${f(1.5)}"/>`}
    r.paradas.forEach((c,i)=>{if(!foco.etiquetas.has(i))return;const q=proj(c.pos),[x,y,an]=colocar(q,c.nombre,puestos,px);h+=`<text class="etq" x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${f(12)}" stroke-width="${f(3)}" text-anchor="${an}">${esc(c.nombre)}</text>`})}
  let barca=null;if(foco.rio&&foco.barca){const b=foco.barca;if(b.poly)barca={poly:b.poly.map(proj),t0:b.t0,t1:b.t1};else{const lo=Math.min(b.de,b.a),hi=Math.max(b.de,b.a);barca={poly:foco.rio.curso.slice(lo,hi+1).map(proj),t0:b.de<=b.a?0:1,t1:b.de<=b.a?1:0}}const tv=foco.rio.vehiculo?foco.rio.vehiculo.tipo:'',tierra=!!TERRESTRES[tv];h+=`<path id="estela" class="estela${tierra?' huellas':''}" d="" stroke-width="${f(1.6)}" stroke-dasharray="${f(2)} ${f(3)}"/><g id="barca" class="barca${tierra?' tierra':''}${S.bamboleo?' duda':''}"><g class="mece"><g transform="scale(${px.toFixed(4)})">${tierra?'<g class="anda">':''}${glifo(tv)}${tierra?'</g>':''}</g></g>${foco.rio.companero?`<g id="masc">${ANIMALES[foco.rio.companero.glifo]?`<g class="animal" transform="translate(-9 -9) scale(.6)">${ANIMALES[foco.rio.companero.glifo]}</g>`:`<text x="-13" y="-9" font-size="13" text-anchor="middle">${foco.rio.companero.emoji}</text>`}</g>`:''}</g>`;S.bamboleo=false}
  const fr=document.getElementById('fronteras');fr.setAttribute('stroke-width',f(1));fr.setAttribute('stroke-dasharray',f(3)+' '+f(3));fr.style.display=foco.modo==='mundo'?'none':'';
  const bm=document.querySelector('.mundo');if(bm)bm.hidden=!enZona;
  capa.innerHTML=h;if(barca)animarBarca(barca.poly,barca.t0,barca.t1,px,!!(foco.rio.vehiculo&&TERRESTRES[foco.rio.vehiculo.tipo]));audio.ajustar(foco.frac!=null?foco.frac:0.45);ambiente(foco)}
/* luz por avance (amanecer en la fuente, atardecer en el mar) y clima por evento (por icono, o `clima` explícito en el evento) */
const CLIMA_ICONO={'🌫️':'niebla','🌪️':'arena','🌧️':'lluvia','🌊':'oleaje','🌬️':'oleaje','❄️':'niebla'};
function ambiente(foco){const luz=document.getElementById('luz'),cl=document.getElementById('clima'),m=document.getElementById('mapa');if(!luz||!cl||!m)return;
  const fr=foco.frac;let etapa='',op=0;
  if(fr!=null){if(fr<0.4){etapa='amanecer';op=0.34*(1-fr/0.4)}else if(fr>0.6){etapa='atardecer';op=0.38*(fr-0.6)/0.4}}
  luz.setAttribute('data-luz',etapa);luz.style.opacity=op.toFixed(2);
  const E=S.pantalla==='rio'&&S.tab==='descender'&&S.evento,c=E?(E.def.clima||CLIMA_ICONO[E.def.icono]||''):'';
  cl.setAttribute('data-clima',c);m.setAttribute('data-mar',c==='oleaje'||(fr!=null&&fr>=0.85)?'vivo':'')}
/* ---------- animales: un glifo SVG por especie (viewBox -14 -14 28 28, mirando a la derecha), en la paleta ---------- */
const ANIMALES={
camello:'<path class="cuerpo" d="M-11 2 Q-11 -3 -7 -4 Q-5 -9 -2 -5 Q0 -9 3 -5 Q6 -5 7 -1 L7 3 L-11 3 Z"/><path class="cuerpo" d="M7 -1 L9 -7 L12 -8 L13 -6 L10 -5 L9 0 Z"/><circle class="oscuro" cx="11" cy="-6.5" r=".6"/><path class="pata" d="M-8 3 L-8 9 M-4 3 L-4 9 M2 3 L2 9 M5 3 L5 9"/><path class="rabo" d="M-11 0 L-13 5"/><path class="acento" d="M-8 -4 L-5 -4 L-5 -2 L-8 -2 Z"/>',
caballo:'<path class="cuerpo" d="M-10 1 Q-10 -4 -5 -4 L4 -4 Q7 -4 7 -1 L7 2 L-10 2 Z"/><path class="cuerpo" d="M6 -3 L9 -10 L12 -11 L14 -9 L11 -8 L10 -3 Z"/><path class="oscuro" d="M6 -4 Q9 -9 8 -12 Q7 -8 5 -5 Z"/><circle class="oscuro" cx="11.5" cy="-9.5" r=".6"/><path class="pata" d="M-8 2 L-9 8 M-4 2 L-4 8 M2 2 L2 8 M5 2 L6 8"/><path class="rabo" d="M-10 -2 L-13 4"/><path class="acento" d="M-3 -4 L2 -4 L2 -1 L-3 -1 Z"/>',
jirafa:'<path class="cuerpo" d="M-9 1 Q-9 -3 -5 -3 L3 -3 Q6 -3 6 0 L6 2 L-9 2 Z"/><path class="cuerpo" d="M4 -3 L6 -12 L9 -13 L11 -11 L8 -10 L7 -2 Z"/><circle class="oscuro" cx="9" cy="-11.5" r=".5"/><path class="pata" d="M-7 2 L-7 9 M-4 2 L-4 9 M1 2 L1 9 M4 2 L4 9"/><path class="rabo" d="M-9 0 L-11 4"/><path class="oscuro" d="M-6 -2h2v2h-2zM-2 -1h2v2h-2zM1 -2h2v2h-2zM-4 0h1v1h-1z"/><path class="acento" d="M7 -13 L7 -15 M9 -13 L9 -15" stroke-width=".8" fill="none"/>',
dromedario:'<path class="cuerpo" d="M-11 2 Q-11 -4 -5 -5 Q-2 -9 2 -5 Q6 -5 7 -1 L7 3 L-11 3 Z"/><path class="cuerpo" d="M7 -1 L9 -8 L12 -9 L13 -7 L10 -6 L9 0 Z"/><circle class="oscuro" cx="11" cy="-7.5" r=".6"/><path class="pata" d="M-8 3 L-8 9 M-4 3 L-4 9 M2 3 L2 9 M5 3 L5 9"/><path class="rabo" d="M-11 0 L-13 5"/><path class="acento" d="M-6 -5 L1 -5 L0 -2 L-6 -2 Z"/>',
hipo:'<ellipse class="cuerpo" cx="-2" cy="1" rx="9" ry="6"/><path class="cuerpo" d="M4 -3 Q12 -4 12 1 Q12 5 5 5 Z"/><circle class="cuerpo" cx="4" cy="-5" r="1.7"/><circle class="cuerpo" cx="8" cy="-5" r="1.7"/><circle class="oscuro" cx="7" cy="-1.5" r=".9"/><circle class="oscuro" cx="10.5" cy=".5" r=".7"/><path class="cuerpo" d="M-8 6h3v3h-3zM1 6h3v3h-3z"/>',
delfin:'<path class="cuerpo" d="M-12 3 Q-8 -2 -2 -4 Q4 -6 12 -2 L9 0 Q4 3 -3 3 Q-7 3 -9 5 Z"/><path class="cuerpo" d="M-12 3 L-11 -1 L-8 2 Z"/><path class="cuerpo" d="M-1 -4 L1 -8 L4 -4 Z"/><circle class="oscuro" cx="6" cy="-2.5" r=".8"/>',
marsopa:'<path class="cuerpo" d="M-12 2 Q-6 -4 0 -4 Q9 -4 12 0 Q9 3 0 3 Q-6 3 -9 5 Z"/><path class="cuerpo" d="M-12 2 L-12 -2 L-8 1 Z"/><path class="claro" d="M-4 3 Q2 4 8 2 Q2 2 -4 3 Z"/><circle class="oscuro" cx="8" cy="-1" r=".8"/>',
rana:'<ellipse class="cuerpo" cx="0" cy="2" rx="9" ry="5.5"/><circle class="cuerpo" cx="-4" cy="-4" r="3"/><circle class="cuerpo" cx="4" cy="-4" r="3"/><circle class="claro" cx="-4" cy="-4.3" r="1.6"/><circle class="claro" cx="4" cy="-4.3" r="1.6"/><circle class="oscuro" cx="-3.5" cy="-4.3" r=".8"/><circle class="oscuro" cx="4.5" cy="-4.3" r=".8"/><path class="oscuro" d="M-5 3 Q0 6 5 3 Q0 4.5 -5 3 Z"/><path class="cuerpo" d="M-10 5 L-7 2 L-6 7 Z M10 5 L7 2 L6 7 Z"/>',
cisne:'<path class="claro" d="M-9 3 Q-4 -2 4 0 L8 3 Q0 7 -9 3 Z"/><path class="oscuro" d="M-9 3 L-12 1 L-10 4 Z"/><path class="claro" d="M2 0 Q4 -6 2 -9 Q1 -12 5 -12 Q9 -12 8 -8 L5 -8 Q7 -5 6 0 Z"/><circle class="oscuro" cx="6" cy="-10.5" r=".7"/><path class="acento" d="M8 -10 L12 -9 L8 -8 Z"/>',
castor:'<path class="oscuro" d="M-7 3 Q-14 2 -12 7 Q-8 8 -7 3 Z"/><ellipse class="cuerpo" cx="1" cy="1" rx="8" ry="6"/><circle class="cuerpo" cx="8" cy="-2" r="4"/><circle class="oscuro" cx="9.5" cy="-3" r=".7"/><circle class="oscuro" cx="11.5" cy="-1.5" r=".8"/><path class="claro" d="M9.5 1 h2 v2 h-2 Z"/><path class="cuerpo" d="M-3 6 h3 v3 h-3 Z M3 6 h3 v3 h-3 Z"/>',
gavial:'<path class="cuerpo" d="M-12 2 Q-6 -1 0 -1 L4 -1 L12 -2.5 L12 -.5 L4 1 Q0 3 -6 3 Q-10 3 -12 2 Z"/><path class="oscuro" d="M-9 -1 l1 -1.5 1 1.5 Z M-6 -1 l1 -1.5 1 1.5 Z M-3 -1 l1 -1.5 1 1.5 Z"/><circle class="oscuro" cx="2" cy="-1.5" r=".8"/><circle class="cuerpo" cx="11" cy="-2" r="1"/><path class="cuerpo" d="M-7 3 h2.5 v2.5 h-2.5 Z M-1 3 h2.5 v2.5 h-2.5 Z"/>',
esturion:'<path class="cuerpo" d="M-12 0 L-12 -4 L-8 -1 Z M-12 0 L-12 4 L-8 1 Z"/><path class="cuerpo" d="M-12 0 Q-6 -3.5 2 -3 Q8 -3 12 -1 Q8 2 2 2.5 Q-6 3 -12 0 Z"/><path class="oscuro" d="M-6 -3 l1.5 -2 1.5 2 Z M-2 -3.2 l1.5 -2 1.5 2 Z M2 -3 l1.5 -2 1.5 2 Z"/><circle class="oscuro" cx="8" cy="-1.5" r=".7"/><path class="bigote" d="M10 0 l1 1.5 M11 0 l1 1.5"/>',
tortuga:'<path class="cuerpo" d="M-8 3 l-2 3 h3 Z M7 3 l2 3 h-3 Z"/><path class="cuerpo" d="M-9 1 Q-8 -7 0 -7 Q8 -7 9 1 Z"/><path class="bigote" d="M-5 -4 L-2 -6 M0 -6.5 L0 -3 M3 -6 L5 -4"/><path class="claro" d="M-10 1 h20 l-1 2 h-18 Z"/><path class="cuerpo" d="M9 0 Q12 -2 12 1 Q12 3 9 2 Z"/><circle class="oscuro" cx="11" cy=".5" r=".6"/>',
bagre:'<path class="cuerpo" d="M-12 1 L-12 -3 L-9 0 Z M-12 1 L-12 5 L-9 2 Z"/><path class="cuerpo" d="M-12 1 Q-6 -4 2 -4 Q9 -4 12 0 Q9 3 2 3.5 Q-6 4 -12 1 Z"/><path class="oscuro" d="M0 -4 l2 -3 2 3 Z"/><circle class="oscuro" cx="8" cy="-1" r=".8"/><path class="bigote" d="M11 0 l3 -3 M11 .5 l3 3"/>',
manati:'<path class="cuerpo" d="M-9 1 Q-13 -1 -12 4 Q-9 5 -7 2 Z"/><path class="cuerpo" d="M-9 1 Q-8 -5 0 -5 Q8 -5 12 -1 Q10 3 4 4 Q-3 5 -9 1 Z"/><path class="cuerpo" d="M3 4 l-1 3 h4 Z"/><circle class="oscuro" cx="9" cy="-1.5" r=".7"/><path class="bigote" d="M11 0 l2 1 M11 1 l2 1.5"/>',
nutria:'<path class="cuerpo" d="M-12 4 Q-8 -1 -2 -2 Q4 -3 9 -1 Q12 0 11 2 Q6 3 -2 3 Q-8 3 -12 6 Z"/><circle class="cuerpo" cx="7" cy="-3.8" r="1.1"/><circle class="cuerpo" cx="10" cy="-4" r="1.1"/><circle class="cuerpo" cx="9" cy="-1" r="3"/><circle class="oscuro" cx="10.3" cy="-2" r=".6"/><circle class="oscuro" cx="12" cy="-.5" r=".7"/><path class="bigote" d="M11 .5 l3 .5 M11 1 l3 1.5"/>',
cocodrilo:'<path class="cuerpo" d="M-12 1 Q-5 -2 1 -2 L12 -2 L12 1 L2 2 Q-5 3 -12 4 Z"/><path class="oscuro" d="M-8 -1.5 l1 -1.5 1 1.5 Z M-5 -2 l1 -1.5 1 1.5 Z M-2 -2 l1 -1.5 1 1.5 Z"/><circle class="cuerpo" cx="3" cy="-3" r="1.4"/><circle class="oscuro" cx="3.4" cy="-3.2" r=".6"/><path class="dientes" d="M6 1 l1 1.5 1 -1.5 1 1.5 1 -1.5 1 1.5 1 -1.5"/><path class="cuerpo" d="M-7 4 h2.5 v2.5 h-2.5 Z M0 2 h2.5 v2.5 h-2.5 Z"/>',
mono:'<path class="rabo" d="M-6 5 Q-13 5 -12 -1 Q-11 -5 -8 -4"/><ellipse class="cuerpo" cx="-1" cy="3" rx="6" ry="5"/><path class="cuerpo" d="M3 6 l1 4 h2 l-1 -4 Z M-4 7 l-1 3 h2 l1 -3 Z"/><circle class="cuerpo" cx="4" cy="-4" r="4.5"/><circle class="oscuro" cx="5" cy="-3.5" r="2.6"/><circle class="claro" cx="4.2" cy="-4.3" r=".6"/><circle class="claro" cx="6" cy="-4.3" r=".6"/>',
tiburon:'<path class="cuerpo" d="M-12 0 L-10 -5 L-7 -1 Z M-12 0 L-10 5 L-7 1 Z"/><path class="cuerpo" d="M-12 0 Q-6 -3 2 -3 Q9 -3 12 0 Q9 3 2 3 Q-6 3 -12 0 Z"/><path class="cuerpo" d="M-1 -3 L2 -9 L5 -3 Z"/><path class="cuerpo" d="M2 3 L4 6 L6 3 Z"/><circle class="oscuro" cx="8" cy="-1.5" r=".8"/><path class="bigote" d="M2 0 v2 M3.5 0 v2 M5 0 v2"/>',
lapa:'<path class="cuerpo" d="M-3 2 L-12 9 L-9 2 Z"/><path class="oscuro" d="M-3 2 L-12 10 L-11 4 Z" fill-opacity=".5"/><path class="cuerpo" d="M-2 -6 Q4 -9 7 -5 Q9 0 4 3 Q0 5 -3 2 Z"/><path class="acento" d="M0 -4 Q-6 -3 -8 2 L-2 0 Z"/><circle class="claro" cx="6" cy="-5" r="2"/><circle class="oscuro" cx="6.5" cy="-5.2" r=".7"/><path class="acento" d="M8 -6 Q12 -6 10 -2 L8 -4 Z"/>',
cangrejo:'<path class="pata" d="M-6 3 l-4 4 M-4 4 l-3 5 M4 4 l3 5 M6 3 l4 4"/><ellipse class="cuerpo" cx="0" cy="1" rx="7" ry="4.5"/><path class="cuerpo" d="M-7 0 L-12 -3 L-10 -6 L-9 -2 Z M7 0 L12 -3 L10 -6 L9 -2 Z"/><circle class="claro" cx="-2.5" cy="-2.5" r="1.3"/><circle class="claro" cx="2.5" cy="-2.5" r="1.3"/><circle class="oscuro" cx="-2.5" cy="-2.5" r=".6"/><circle class="oscuro" cx="2.5" cy="-2.5" r=".6"/>'};
function animal(m,extra){const g=m&&ANIMALES[m.glifo];return g?`<svg class="animal${extra?' '+extra:''}" viewBox="-14 -14 28 28" aria-hidden="true">${g}</svg>`:esc(m?m.emoji:'')}
/* ---------- escenas: pictogramas SVG (caja 40×40, suelo en y=40, centrados en x=20) en la paleta ---------- */
const PICTOS={
palmera:'<path class="p" d="M18 40 Q20 26 18 14 h4 Q24 26 22 40 Z"/><ellipse class="p" cx="11" cy="12" rx="10" ry="3" transform="rotate(-28 11 12)"/><ellipse class="p" cx="29" cy="12" rx="10" ry="3" transform="rotate(28 29 12)"/><ellipse class="p" cx="14" cy="7" rx="8" ry="2.6" transform="rotate(-62 14 7)"/><ellipse class="p" cx="26" cy="7" rx="8" ry="2.6" transform="rotate(62 26 7)"/><circle class="d" cx="20" cy="14" r="2"/>',
arbol:'<rect class="p" x="18" y="24" width="4" height="16"/><circle class="p" cx="20" cy="17" r="10"/>',
selva:'<circle class="p" cx="10" cy="23" r="9"/><circle class="p" cx="22" cy="16" r="11"/><circle class="p" cx="32" cy="24" r="8"/><rect class="p" x="20" y="24" width="4" height="16"/><rect class="p" x="9" y="29" width="3" height="11"/><rect class="p" x="31" y="30" width="3" height="10"/>',
'montaña':'<path class="p" d="M0 40 L14 12 L22 24 L30 8 L40 40 Z"/>',
nieve:'<path class="p" d="M0 40 L16 6 L40 40 Z"/><path class="b" d="M16 6 L22 18 L18 16 L14 19 L10 16 Z"/>',
volcan:'<path class="p" d="M2 40 L15 12 L25 12 L38 40 Z"/><path class="d" d="M15 12 L25 12 L23 8 L17 8 Z"/><circle class="b" cx="20" cy="4" r="3" fill-opacity=".8"/><circle class="b" cx="26" cy="2" r="2" fill-opacity=".6"/>',
duna:'<path class="d" d="M0 40 Q12 26 24 34 Q32 38 40 30 V40 Z"/><path class="p" d="M0 40 Q14 33 26 38 L40 40 Z" fill-opacity=".35"/>',
pantano:'<path class="l" d="M8 40 V22 M14 40 V18 M20 40 V24 M26 40 V16 M32 40 V22"/><ellipse class="p" cx="14" cy="16" rx="1.6" ry="4"/><ellipse class="p" cx="26" cy="14" rx="1.6" ry="4"/>',
manglar:'<path class="l" d="M10 40 Q10 28 16 26 M16 40 Q14 28 16 26 M22 40 Q18 28 16 26 M28 40 Q30 28 26 24 M34 40 Q32 30 26 24" stroke-width="2"/><ellipse class="p" cx="16" cy="18" rx="10" ry="7"/><ellipse class="p" cx="27" cy="16" rx="9" ry="7"/>',
cataratas:'<path class="p" d="M0 40 V10 h14 v30 Z M26 40 V10 h14 v30 Z"/><path class="b" d="M14 12 h12 v28 h-12 Z"/><path class="w" d="M17 14 V38 M20 14 V38 M23 14 V38"/>',
hielo:'<path class="b" d="M2 40 L6 34 h10 l4 6 Z M22 40 l4 -8 h12 l2 8 Z"/><path class="p" d="M8 34 L12 26 L16 34 Z" fill-opacity=".5"/>',
garganta:'<path class="p" d="M0 40 L2 6 L16 10 L15 40 Z M25 40 L24 8 L38 4 L40 40 Z"/>',
campos:'<path class="p" d="M0 40 V30 L40 26 V40 Z" fill-opacity=".45"/><path class="l" d="M3 34 L37 30 M3 37.5 L37 33.5" stroke-width="1"/>',
lago:'<ellipse class="a" cx="20" cy="36" rx="18" ry="4"/><path class="w" d="M8 35 h6 M20 37 h8" stroke-width="1"/>',
piramide:'<path class="p" d="M2 40 L20 8 L38 40 Z"/><path class="d" d="M20 8 L24 15 h-8 Z"/><path class="p" d="M26 40 L34 26 L40 40 Z" fill-opacity=".7"/>',
mezquita:'<rect class="p" x="10" y="26" width="20" height="14"/><path class="p" d="M10 26 Q20 8 30 26 Z"/><rect class="p" x="33" y="12" width="3" height="28"/><path class="d" d="M34.5 6 L37 12 h-5 Z"/><circle class="d" cx="20" cy="10" r="1.6"/>',
pagoda:'<path class="p" d="M8 40 V34 h24 v6 Z M6 34 Q20 28 34 34 L30 30 H10 Z M10 30 V24 h20 v6 Z M8 24 Q20 18 32 24 L28 20 H12 Z M13 20 V14 h14 v6 Z M11 14 Q20 6 29 14 Z"/><path class="d" d="M20 2 L22 8 h-4 Z"/>',
templo:'<rect class="p" x="4" y="10" width="32" height="4"/><path class="p" d="M8 14 h4 v26 h-4 Z M15 14 h4 v26 h-4 Z M22 14 h4 v26 h-4 Z M29 14 h4 v26 h-4 Z"/><rect class="p" x="2" y="38" width="36" height="2"/>',
iglesia:'<rect class="p" x="4" y="24" width="22" height="16"/><path class="p" d="M4 24 L15 16 L26 24 Z"/><rect class="p" x="28" y="12" width="8" height="28"/><path class="p" d="M27 12 L32 4 L37 12 Z"/><rect class="b" x="30" y="18" width="4" height="6"/><path class="l" d="M32 0 V4 M30 2 H34" stroke-width="1"/>',
castillo:'<path class="p" d="M4 40 V16 h4 v-4 h4 v4 h4 v-4 h4 v4 h4 v-4 h4 v4 h4 v-4 h4 v4 V40 Z"/><rect class="b" x="18" y="28" width="4" height="8"/><path class="d" d="M20 4 V12 L26 8 Z"/>',
puente:'<rect class="p" x="0" y="26" width="40" height="3"/><path class="l" d="M4 40 V29 M36 40 V29 M8 29 Q20 14 32 29" stroke-width="2.5"/>',
presa:'<path class="p" d="M4 40 L10 12 h20 l6 28 Z"/><path class="b" d="M14 16 h12 v3 h-12 Z"/><path class="w" d="M16 24 v14 M20 22 v16 M24 24 v14" stroke-width="1.5"/>',
rascacielos:'<rect class="p" x="4" y="18" width="8" height="22"/><rect class="p" x="14" y="8" width="10" height="32"/><rect class="p" x="26" y="14" width="8" height="26"/><path class="l" d="M19 2 V8" stroke-width="1.5"/><rect class="b" x="16" y="12" width="2" height="2"/><rect class="b" x="20" y="12" width="2" height="2"/><rect class="b" x="16" y="17" width="2" height="2"/><rect class="b" x="20" y="17" width="2" height="2"/>',
fabrica:'<rect class="p" x="4" y="24" width="32" height="16"/><rect class="p" x="8" y="10" width="5" height="14"/><rect class="p" x="18" y="14" width="5" height="10"/><path class="p" d="M4 24 L14 18 V24 L24 18 V24 L34 18 V24 Z"/><circle class="b" cx="10.5" cy="7" r="2.5" fill-opacity=".8"/><circle class="b" cx="14" cy="4" r="2" fill-opacity=".6"/>',
muelle:'<rect class="p" x="0" y="26" width="30" height="3"/><path class="l" d="M4 29 V40 M12 29 V40 M20 29 V40 M28 29 V40" stroke-width="2"/><rect class="d" x="22" y="20" width="6" height="6"/>',
casas:'<path class="p" d="M2 40 V24 L9 16 L16 24 V40 Z M17 40 V26 L23 18 L29 26 V40 Z M30 40 V28 L35 22 L40 28 V40 Z"/><rect class="b" x="7" y="28" width="4" height="5"/><rect class="b" x="21" y="30" width="4" height="5"/>',
grua:'<path class="l" d="M10 40 V6 M10 6 H34 M34 6 V12 M22 6 V14 M14 40 V10 M6 40 V10" stroke-width="2"/><rect class="d" x="30" y="12" width="6" height="5"/><rect class="p" x="2" y="36" width="16" height="4"/>',
tren:'<rect class="p" x="6" y="24" width="30" height="10"/><rect class="p" x="26" y="16" width="10" height="8"/><rect class="p" x="10" y="12" width="4" height="12"/><circle class="p" cx="12" cy="37" r="3"/><circle class="p" cx="22" cy="37" r="3"/><circle class="p" cx="32" cy="37" r="3"/><circle class="b" cx="10" cy="8" r="2.5" fill-opacity=".8"/><path class="l" d="M0 40 H40" stroke-width="1"/>',
esferas:'<circle class="p" cx="10" cy="32" r="8"/><circle class="p" cx="26" cy="29" r="11"/><circle class="b" cx="8" cy="29" r="2" fill-opacity=".4"/><circle class="b" cx="22" cy="24" r="3" fill-opacity=".4"/>',
faro:'<path class="p" d="M14 40 L16 12 h8 l2 28 Z"/><rect class="d" x="15" y="8" width="10" height="4"/><path class="p" d="M14 8 L20 2 L26 8 Z"/><rect class="b" x="17" y="22" width="6" height="3"/>',
barco:'<path class="p" d="M2 30 h36 l-4 8 h-28 Z"/><rect class="p" x="22" y="20" width="10" height="10"/><rect class="d" x="8" y="24" width="12" height="6"/><rect class="p" x="26" y="14" width="3" height="6"/>',
obelisco:'<path class="p" d="M17 40 L18 8 h4 l1 32 Z"/><path class="d" d="M18 8 L20 3 L22 8 Z"/><rect class="p" x="14" y="38" width="12" height="2"/>',
mercado:'<path class="d" d="M2 22 Q10 14 18 22 Z"/><rect class="p" x="4" y="22" width="12" height="18"/><path class="d" d="M22 20 Q30 12 38 20 Z"/><rect class="p" x="24" y="20" width="12" height="20"/><rect class="b" x="7" y="26" width="6" height="4"/><rect class="b" x="27" y="24" width="6" height="4"/>',
balsa:'<rect class="d" x="6" y="30" width="28" height="6" rx="3"/><path class="l" d="M12 30 l-3 -8 M28 30 l3 -8" stroke-width="2"/><circle class="p" cx="16" cy="26" r="2.5"/><circle class="p" cx="24" cy="26" r="2.5"/>',
vaca:'<ellipse class="p" cx="18" cy="28" rx="11" ry="6"/><rect class="p" x="10" y="32" width="3" height="8"/><rect class="p" x="22" y="32" width="3" height="8"/><path class="p" d="M27 24 L36 22 L37 27 L30 30 Z"/><path class="l" d="M33 21 l2 -4 M36 22 l3 -3" stroke-width="1.5"/>',
camello:'<ellipse class="p" cx="18" cy="26" rx="11" ry="6"/><path class="p" d="M12 21 Q18 12 24 21 Z"/><rect class="p" x="9" y="30" width="3" height="10"/><rect class="p" x="24" y="30" width="3" height="10"/><path class="p" d="M27 24 L32 12 h4 l-3 12 Z"/><circle class="p" cx="35" cy="11" r="2.5"/>',
banano:'<rect class="p" x="19" y="18" width="2" height="22"/><ellipse class="p" cx="11" cy="16" rx="9" ry="3.5" transform="rotate(-30 11 16)"/><ellipse class="p" cx="29" cy="16" rx="9" ry="3.5" transform="rotate(30 29 16)"/><ellipse class="p" cx="20" cy="9" rx="3.5" ry="8"/><path class="d" d="M22 22 q3 4 1 8 q-3 -3 -1 -8 Z"/>',
aves:'<path class="p" d="M4 18 q5 -5 10 0 q-5 -1 -10 3 Z M14 18 q5 -5 10 0 q-5 -1 -10 3 Z M22 10 q5 -5 10 0 q-5 -1 -10 3 Z M32 10 q4 -4 8 0 q-4 -1 -8 3 Z"/>',
mascara:'<path class="d" d="M8 8 Q20 2 32 8 L30 30 Q20 38 10 30 Z"/><circle class="p" cx="15" cy="16" r="3"/><circle class="p" cx="25" cy="16" r="3"/><path class="p" d="M14 26 Q20 30 26 26 Q20 27 14 26 Z"/><path class="l" d="M6 6 l4 6 M34 6 l-4 6 M20 0 v6" stroke-width="1.5"/>'};
function picto(k){const [tipo,arg]=k.split(':');if(tipo==='animal')return ANIMALES[arg]?{vb:'-14 -14 28 28',svg:`<g class="animal">${ANIMALES[arg]}</g>`}:null;return PICTOS[k]?{vb:'0 0 40 40',svg:PICTOS[k]}:null}
function escena(items,cls){if(!items||!items.length)return '';const n=items.length,w=240/n;
  const partes=items.map((k,i)=>{const p=picto(k);if(!p)return '';const x=(i+0.5)*w;return p.vb[0]==='-'?`<g class="animal" transform="translate(${x.toFixed(1)} 55) scale(1.1)">${ANIMALES[k.split(':')[1]]}</g>`:`<g transform="translate(${(x-20).toFixed(1)} 28)">${p.svg}</g>`}).join('');
  return `<svg class="escena${cls?' '+cls:''}" viewBox="0 0 240 80" aria-hidden="true"><rect class="cielo" width="240" height="80"/><circle class="d" cx="222" cy="14" r="6"/><rect class="suelo" y="66" width="240" height="6"/><rect class="agua" y="72" width="240" height="8"/>${partes}</svg>`}
function glifo(t){/* vista lateral, proa a la derecha, origen en el centro del casco; ≈ 24 unidades de ancho, de y=-13 (arriba) a y=4 */
  switch(t){
    case 'latina':return '<path class="casco" d="M-11 -1 Q-6 -3 0 -3 Q8 -3 12 -2 L10 3 Q0 4 -9 3 Z"/><path class="palo" d="M-7 -3 L9 -13" stroke-width="1"/><path class="vela" d="M-6 -3 Q-1 -13 8 -12 Q4 -8 1 -3 Z"/><path class="casco" d="M9 -13 L12 -12 L9 -11 Z"/>';
    case 'junco':return '<path class="casco" d="M-11 -4 L-9 -1 L9 -1 L11 -3 L9 3 L-8 3 Z"/><path class="palo" d="M2 -1 L1 -13" stroke-width="1"/><path class="vela" d="M-1 -1 L-3 -12 L7 -11 L5 -1 Z"/><path class="linea" d="M-2.5 -9 L6.5 -8.3 M-2 -6 L6 -5.6 M-1.5 -3.5 L5.5 -3.2" stroke-width=".6"/><path class="casco" d="M1 -13 L4 -12 L1 -11 Z"/>';
    case 'vapor':return '<path class="casco" d="M-11 0 L11 0 L9 3 L-9 3 Z"/><path class="vela" d="M-8 -3 L8 -3 L8 0 L-8 0 Z"/><path class="vela" d="M-5 -6 L5 -6 L5 -3 L-5 -3 Z"/><path class="palo" d="M-3 -6 L-3 -11 M3 -6 L3 -11" stroke-width="1.6"/><circle class="humo" cx="-3" cy="-12.5" r="1.4"/><circle class="humo" cx="3" cy="-12.5" r="1.4"/><circle class="humo" cx="-6.5" cy="-13.8" r="1"/><circle class="palo" cx="-11" cy="0" r="3.2" stroke-width="1"/><path class="palo" d="M-11 -3.2 L-11 3.2 M-7.8 0 L-14.2 0" stroke-width=".7"/>';
    case 'balsa':return '<path class="casco" d="M-10 -2.5 Q-11 -2.5 -11 -1.5 L-11 1.5 Q-11 2.5 -10 2.5 L10 2.5 Q11 2.5 11 1.5 L11 -1.5 Q11 -2.5 10 -2.5 Z"/><path class="linea" d="M-6 -2.5 L-6 2.5 M-2 -2.5 L-2 2.5 M2 -2.5 L2 2.5 M6 -2.5 L6 2.5" stroke-width=".6"/><path class="vela" d="M-2 -2.5 Q0 -6.5 3 -2.5 Z"/><path class="palo" d="M-5 -2.5 L-8 -8 M5 -2.5 L8 -8" stroke-width="1"/><path class="casco" d="M-9 -9 L-7 -7 L-8.5 -6.5 Z M9 -9 L7 -7 L8.5 -6.5 Z"/>';
    case 'canoa':return '<path class="casco" d="M-13 -1 Q-9 -3 0 -3 Q9 -3 13 -1 Q9 2 0 2.5 Q-9 2 -13 -1 Z"/><path class="palo" d="M2 -3 L2 -7 L10 -7 L10 -3 M1 -7 L11 -7" stroke-width=".8"/><circle class="fig" cx="-3" cy="-6" r="1.6"/><path class="palo" d="M-3 -4.4 L-3 -3 M-2 -7.5 L2 0" stroke-width="1"/>';
    case 'barcaza':return '<path class="casco" d="M-13 -1 L13 -1 L12 3 L-12 3 Z"/><path class="linea" d="M-5 -1 L-5 -2.5 L9 -2.5 L9 -1" stroke-width=".8"/><path class="vela" d="M-12 -1 L-12 -6 L-6 -6 L-6 -1 Z"/><path class="linea" d="M-10.5 -4.5 L-7.5 -4.5" stroke-width=".7"/><path class="palo" d="M11 -1 L11 -6" stroke-width=".8"/><path class="casco" d="M11 -6 L14 -5 L11 -4 Z"/>';
    case 'caravana':return '<path class="casco" d="M-9 0 Q-10 -6 -4 -7 Q0 -11 4 -7 Q8 -7 8 -2 L8 0 Z"/><path class="casco" d="M8 -2 L10 -10 L13 -11 L14 -9 L11 -8 L10 0 Z"/><path class="palo" d="M-7 0 L-7 4 M-3 0 L-3 4 M2 0 L2 4 M6 0 L6 4" stroke-width="1"/><path class="vela" d="M-5 -10 L1 -10 L2 -7 L-6 -7 Z"/><path class="linea" d="M-2 -10 L-2 -7" stroke-width=".6"/><path class="palo" d="M-9 -1 L-12 3" stroke-width=".8"/>';
    case 'jinete':return '<path class="casco" d="M-10 0 Q-11 -5 -5 -6 Q-1 -6 2 -6 Q7 -6 8 -2 L8 0 Z"/><path class="casco" d="M8 -2 L10 -9 L13 -10 L14 -8 L11 -7 L10 0 Z"/><path class="palo" d="M-7 0 L-8 4 M-4 0 L-3 4 M2 0 L1 4 M6 0 L7 4" stroke-width="1"/><circle class="fig" cx="-1" cy="-11.5" r="1.8"/><path class="palo" d="M-1 -9.5 L-1 -6 M-1 -8 L3 -6.5" stroke-width="1.3"/><path class="vela" d="M-4 -9 L1 -9 L1 -6 L-4 -6 Z"/><path class="palo" d="M3 -13 L3 -4" stroke-width=".8"/><path class="palo" d="M-10 -1 L-13 3" stroke-width=".8"/>';
    case 'pie':return '<circle class="fig" cx="0" cy="-10.5" r="2"/><path class="palo" d="M0 -8.5 L0 -2 M0 -2 L-3 4 M0 -2 L3 4 M0 -7 L4 -4 M0 -7 L-3 -2" stroke-width="1.2"/><path class="palo" d="M5 -13 L5 4" stroke-width=".9"/><path class="casco" d="M-4 -8 L-1 -9 L-1 -4 L-4 -3 Z"/>';
    default:return '<path class="casco" d="M-10 -1 Q-6 -3 0 -3 Q7 -3 11 -1 L9 3 L-8 3 Z"/><path class="palo" d="M0 -3 L0 -13" stroke-width="1"/><path class="vela" d="M-6 -12 L6 -12 Q7 -7 6 -3 L-6 -3 Q-7 -7 -6 -12 Z"/><path class="casco" d="M0 -13 L4 -12 L0 -11 Z"/>'}}
let animB=null;
function animarBarca(poly,t0,t1,px,tierra){const g=document.getElementById('barca'),m=document.getElementById('masc');if(!g)return;if(animB)cancelAnimationFrame(animB);
  const poner=p=>{let ang=p.ang,sx=1;if(Math.cos(ang*Math.PI/180)<0){ang=ang-180;sx=-1}g.setAttribute('transform',`translate(${p.x.toFixed(2)} ${p.y.toFixed(2)}) rotate(${ang.toFixed(1)}) scale(${sx} 1)`);if(m)m.setAttribute('transform',`rotate(${(-ang*sx).toFixed(1)}) scale(${px.toFixed(4)})`)}/* derecho y mirando hacia adelante: se anula el giro, no el espejo */;
  if(poly.length<2){poner({x:poly[0][0],y:poly[0][1],ang:0});return}
  const L=[0];for(let i=1;i<poly.length;i++)L[i]=L[i-1]+Math.hypot(poly[i][0]-poly[i-1][0],poly[i][1]-poly[i-1][1]);const tot=L[L.length-1]||1;
  const pos=t=>{const s=t*tot;let i=1;while(i<L.length-1&&L[i]<s)i++;const a=poly[i-1],b=poly[i],u=(L[i]-L[i-1])?(s-L[i-1])/(L[i]-L[i-1]):0;return{x:a[0]+(b[0]-a[0])*u,y:a[1]+(b[1]-a[1])*u,ang:Math.atan2(b[1]-a[1],b[0]-a[0])*180/Math.PI,i}};
  const estela=document.getElementById('estela'),capa=document.getElementById('capa');
  const dibujarEstela=p=>{if(!estela)return;const pts=t1>=t0?poly.slice(0,p.i).concat([[p.x,p.y]]):[[p.x,p.y]].concat(poly.slice(p.i));estela.setAttribute('d','M'+pts.map(q=>q[0].toFixed(1)+' '+q[1].toFixed(1)).join('L'))};
  const salpicar=p=>{if(!capa||!capa.insertAdjacentHTML)return;capa.insertAdjacentHTML('beforeend',`<g class="salpicon${tierra?' polvo':''}" transform="translate(${p.x.toFixed(2)} ${p.y.toFixed(2)}) scale(${px.toFixed(4)})"><g class="sal"><circle r="4"/><circle cx="-5" cy="-2" r="1.5"/><circle cx="5" cy="-2" r="1.5"/><circle cy="-5" r="1.2"/></g></g>`);setTimeout(()=>{const s=capa.querySelector('.salpicon');if(s)s.remove()},1000)};
  const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(t0===t1||reduce){poner(pos(t1));return}
  const T=performance.now(),dur=1400;
  const step=now=>{let k=Math.min(1,(now-T)/dur);k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;const p=pos(t0+(t1-t0)*k);poner(p);dibujarEstela(p);if(k<1)animB=requestAnimationFrame(step);else{animB=null;if(estela)estela.setAttribute('class','estela fin');salpicar(p)}};
  animB=requestAnimationFrame(step)}

/* ---------- arranque ---------- */
(function init(){cargarPerfiles();if(voz.soporte())window.speechSynthesis.getVoices();render(true)})();
window.addEventListener('resize',()=>{if(S.foco)renderMapa(S.foco,true);const pf=document.getElementById('perfil');if(pf&&!pf.hidden&&S.pantalla==='rio')pf.innerHTML=perfilSVG(rioPor(S.rio))});
function plegarMapa(){const a=document.getElementById('arriba');a.classList.toggle('compacto');const b=document.querySelector('.plegar');b.textContent=a.classList.contains('compacto')?'▴':'▾';if(S.foco)renderMapa(S.foco,true)}
