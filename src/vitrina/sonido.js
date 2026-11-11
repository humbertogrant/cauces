/* Sonido de la vitrina del Nilo: madera, agua y viento, sintetizados con Web Audio. Sin archivos.
   Extiende el audio del motor, no lo reemplaza: usa su mismo AudioContext, obedece su interruptor (audio.on) y el
   agua del motor sigue sonando debajo. Nada corre al cargar: aquí solo se definen funciones y se registran oyentes
   en CAPA; todo lo del navegador va dentro de funciones y con guardas.
   Cada efecto es una función pura (ctx, destino, t0) => duración en segundos, que arma sus nodos en cualquier
   BaseAudioContext (AudioContext u OfflineAudioContext): por eso CAPA.sonido.probar() lo puede medir sin oírlo. */
(function(){
'use strict';
const CLAVE='nilo:silencio';   // '1' = el jugador apagó el sonido; se recuerda entre visitas
const NIVEL=0.45;              // ganancia maestra, baja, después del compresor
const BAJO=0.3;                // a cuánto bajan los efectos mientras la voz lee

/* ---------- piezas ---------- */
/* Ruido blanco determinista (xorshift con semilla fija): suena igual a cualquier ruido, pero la medición se repite. */
const RUIDOS=typeof WeakMap==='function'?new WeakMap():null;
function ruido(ctx){let b=RUIDOS&&RUIDOS.get(ctx);if(b)return b;
  const n=Math.floor(ctx.sampleRate*2);b=ctx.createBuffer(1,n,ctx.sampleRate);const d=b.getChannelData(0);let s=0x9E3779B9|0;
  for(let i=0;i<n;i++){s^=s<<13;s^=s>>>17;s^=s<<5;d[i]=((s>>>0)/4294967296)*2-1}
  if(RUIDOS)RUIDOS.set(ctx,b);return b}
function fuente(ctx,t0,dur,desde){const s=ctx.createBufferSource();s.buffer=ruido(ctx);s.loop=true;s.start(t0,desde||0);s.stop(t0+dur);return s}
function filtro(ctx,tipo,f,q){const b=ctx.createBiquadFilter();b.type=tipo;b.frequency.value=f;if(q!=null)b.Q.value=q;return b}
function gan(ctx,v){const g=ctx.createGain();g.gain.value=v;return g}
/* una curva por puntos [segundos desde t0, valor] */
function curva(p,t0,pts){p.setValueAtTime(pts[0][1],t0+pts[0][0]);for(let i=1;i<pts.length;i++)p.linearRampToValueAtTime(pts[i][1],t0+pts[i][0])}
/* un golpe: una onda grave que cae de tono y se apaga en centésimas (no llega a ser una nota) */
function tumbo(ctx,dest,t,f0,f1,dur,g){const o=ctx.createOscillator(),e=gan(ctx,0);o.type='sine';
  o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(f1,t+dur);
  e.gain.setValueAtTime(0,t);e.gain.linearRampToValueAtTime(g,t+0.005);e.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  o.connect(e);e.connect(dest);o.start(t);o.stop(t+dur+0.01)}
/* una ráfaga corta de ruido filtrado: el contacto de dos cosas */
function rafaga(ctx,dest,t,dur,tipo,f,q,g){const s=fuente(ctx,t,dur+0.01,(t*7.3)%1.5),b=filtro(ctx,tipo,f,q),e=gan(ctx,0);
  e.gain.setValueAtTime(0,t);e.gain.linearRampToValueAtTime(g,t+0.003);e.gain.exponentialRampToValueAtTime(0.0001,t+dur);
  s.connect(b);b.connect(e);e.connect(dest)}
/* un golpe sordo de madera: el cuerpo, la tabla y el contacto */
function madera(ctx,dest,t,k,af){
  tumbo(ctx,dest,t,128*af,84*af,0.16,0.30*k);
  tumbo(ctx,dest,t,236*af,190*af,0.07,0.13*k);
  rafaga(ctx,dest,t,0.05,'bandpass',420*af,1.2,0.5*k)}

/* ---------- los cinco efectos ---------- */
/* El viento en la vela: ruido filtrado, bajo, con un soplo lento que entra y sale. */
function viento(ctx,dest,t0){const D=5.2;
  const s=fuente(ctx,t0,D,0.31),a=filtro(ctx,'bandpass',340,0.9),b=filtro(ctx,'bandpass',170,0.7),lp=filtro(ctx,'lowpass',1500,0.5);
  const ga=gan(ctx,0.5),gb=gan(ctx,0.5),e=gan(ctx,0);
  curva(a.frequency,t0,[[0,340],[1.7,560],[2.9,420],[3.9,600],[D,360]]);
  curva(e.gain,t0,[[0,0],[1.6,1],[2.8,0.55],[3.8,0.9],[D-0.05,0],[D,0]]);
  s.connect(a);a.connect(ga);ga.connect(lp);s.connect(b);b.connect(gb);gb.connect(lp);lp.connect(e);e.connect(dest);return D}

/* La llegada a puerto: dos golpes sordos del casco contra el muelle y un crujido corto de soga. */
function puerto(ctx,dest,t0){
  const lp=filtro(ctx,'lowpass',900,0.5);lp.connect(dest);
  madera(ctx,lp,t0,1,1);madera(ctx,lp,t0+0.38,0.7,0.92);
  /* la soga se tensa: ruido angosto que se abre y se cierra a tirones, cada vez más seguidos */
  const t=t0+0.66,D=0.4,s=fuente(ctx,t,D,0.9),bp=filtro(ctx,'bandpass',700,5),am=gan(ctx,0),e=gan(ctx,0),o=ctx.createOscillator();
  o.type='sawtooth';o.frequency.setValueAtTime(22,t);o.frequency.linearRampToValueAtTime(58,t+D);
  bp.frequency.setValueAtTime(700,t);bp.frequency.linearRampToValueAtTime(1250,t+D);
  o.connect(am.gain);curva(e.gain,t,[[0,0],[0.05,1.1],[0.3,0.8],[D-0.01,0],[D,0]]);
  s.connect(bp);bp.connect(am);am.connect(e);e.connect(dest);o.start(t);o.stop(t+D);return 1.1}

/* Una moneda sobre madera: tres rebotes, cada uno más chico; cuerpo de madera y un filo de metal que no dura. */
function moneda(ctx,dest,t0){
  for(const [dt,k] of [[0,1],[0.115,0.42],[0.195,0.2]]){const t=t0+dt;
    tumbo(ctx,dest,t,210,150,0.07,0.24*k);
    rafaga(ctx,dest,t,0.03,'bandpass',1500,1,0.28*k);
    for(const [f,g,d] of [[2380,0.08,0.09],[3710,0.05,0.07],[5290,0.035,0.05]])tumbo(ctx,dest,t,f,f*0.995,d,g*k)}
  return 0.3}

/* El sello sobre el papel: un golpe grave y seco y el roce breve del papel. */
function sello(ctx,dest,t0){
  tumbo(ctx,dest,t0,118,58,0.11,0.4);
  rafaga(ctx,dest,t0,0.035,'lowpass',520,0.5,0.55);
  const t=t0+0.1,D=0.24,s=fuente(ctx,t,D,0.47),bp=filtro(ctx,'bandpass',2400,0.7),e=gan(ctx,0);
  bp.frequency.setValueAtTime(2400,t);bp.frequency.linearRampToValueAtTime(3600,t+D);
  curva(e.gain,t,[[0,0],[0.04,0.11],[0.12,0.06],[D-0.01,0],[D,0]]);
  s.connect(bp);bp.connect(e);e.connect(dest);return 0.36}

/* El mar: una ola larga que crece, rompe y se retira (ruido con barrido de filtro) y la espuma que queda. */
function mar(ctx,dest,t0){const D=6.4;
  const s=fuente(ctx,t0,D,1.1),lp=filtro(ctx,'lowpass',280,0.7),e=gan(ctx,0);
  curva(lp.frequency,t0,[[0,280],[1.4,700],[2.3,2600],[3.1,1500],[D,420]]);
  curva(e.gain,t0,[[0,0],[1.3,0.3],[2.3,0.42],[3,0.3],[4.6,0.16],[D-0.05,0],[D,0]]);
  s.connect(lp);lp.connect(e);e.connect(dest);
  const s2=fuente(ctx,t0+2.1,D-2.1,0.2),bp=filtro(ctx,'bandpass',5200,0.8),e2=gan(ctx,0);
  curva(bp.frequency,t0,[[2.1,5200],[D,2600]]);
  curva(e2.gain,t0,[[2.1,0],[2.5,0.05],[3.4,0.035],[D-0.05,0],[D,0]]);
  s2.connect(bp);bp.connect(e2);e2.connect(dest);return D}

/* Un acierto: un solo golpe suave de madera, como un nudillo sobre la borda. Más bajo que la moneda. */
function acierto(ctx,dest,t0){
  const lp=filtro(ctx,'lowpass',1400,0.5);lp.connect(dest);
  tumbo(ctx,lp,t0,330,250,0.12,0.13);
  tumbo(ctx,lp,t0,172,140,0.16,0.09);
  rafaga(ctx,lp,t0,0.03,'bandpass',900,1.2,0.22);return 0.18}

const efectos={viento,puerto,moneda,sello,mar,acierto};

/* ---------- la cadena: todo pasa por un bus (que baja con la voz), un compresor y una ganancia maestra baja ---------- */
function cadena(ctx,destino){const bus=gan(ctx,1),comp=ctx.createDynamicsCompressor(),maestra=gan(ctx,NIVEL);
  comp.threshold.value=-12;comp.knee.value=6;comp.ratio.value=4;comp.attack.value=0.003;comp.release.value=0.2;
  bus.connect(comp);comp.connect(maestra);maestra.connect(destino);return {ctx,bus,comp,maestra}}

/* ---------- en vivo: sobre el audio del motor ---------- */
let vivo=null,hecho=false,tog0=null,autoT=0,tMS=0,pingReloj=0,finPuerto=0,hablando=false,viaje=null,selloPend=false;
/* el objeto audio del motor (const global de motor.js); el motor se carga después: por eso se busca al usarlo */
function motor(){try{return typeof audio!=='undefined'&&audio?audio:null}catch(e){return null}}
function encendido(){const a=motor();return !!(a&&a.ctx&&a.on)}
function silencio(){try{return typeof localStorage!=='undefined'&&localStorage.getItem(CLAVE)==='1'}catch(e){return false}}
function recordar(callado){try{if(typeof localStorage==='undefined')return;if(callado)localStorage.setItem(CLAVE,'1');else localStorage.removeItem(CLAVE)}catch(e){}}
function cadenaViva(){const a=motor();if(!a||!a.ctx)return null;
  if(!vivo||vivo.ctx!==a.ctx){vivo=cadena(a.ctx,a.ctx.destination);vivo.bus.gain.value=hablando?BAJO:1}return vivo}
function ahora(){return Date.now()}
function luego(fn,ms){return typeof setTimeout==='function'?setTimeout(fn,ms):(fn(),0)}
/* la voz lee: el motor baja el agua (audio.duck) y aquí bajan los efectos */
function bajar(on){hablando=!!on;try{const c=cadenaViva();if(!c)return;const t=c.ctx.currentTime;c.bus.gain.cancelScheduledValues(t);c.bus.gain.setTargetAtTime(on?BAJO:1,t,0.3)}catch(e){}}
/* el interruptor del motor cambió: abrir o cerrar la maestra */
function nivelar(){try{const c=cadenaViva();if(!c)return;const t=c.ctx.currentTime,si=encendido();c.maestra.gain.cancelScheduledValues(t);c.maestra.gain.setTargetAtTime(si?NIVEL:0,t,0.12);if(!si)llegar()}catch(e){}}
/* Engancharse al audio del motor sin tocar motor.js: su interruptor guarda el silencio, su duck baja también los
   efectos y su ping (un tono puro) pasa a ser un golpe suave de madera (acierto); nunca suena a moneda. */
function enganchar(){const a=motor();if(!a)return false;if(hecho)return true;hecho=true;
  const toggle=tog0=a.toggle,duck=a.duck,ping=a.ping;
  if(typeof toggle==='function')a.toggle=function(){
    if(this.on&&autoT&&ahora()-autoT<700){autoT=0;return}   /* el primer toque fue sobre «≈ sonido»: ya quedó encendido */
    autoT=0;const r=toggle.apply(this,arguments);recordar(!this.on);nivelar();return r};
  if(typeof duck==='function')a.duck=function(on){const r=duck.apply(this,arguments);bajar(on);return r};
  /* el aviso de evento (392 Hz) queda mudo; cualquier otro ping agenda el acierto para el final del turno, y si en ese
     mismo turno el motor avisa «moneda» o «sello», se cancela: vender no suena a golpe y a moneda a la vez */
  if(typeof ping==='function')a.ping=function(f){if(!this.ctx||!this.on||(f&&f<600)||pingReloj||ahora()-tMS<30)return;
    pingReloj=luego(()=>{pingReloj=0;sonar('acierto')},0)};
  return true}
/* el primer toque del jugador: se enciende el sonido, salvo que lo haya apagado antes */
function arrancar(){try{if(!enganchar())return;const a=motor();
  if(a.on){nivelar();return}
  if(silencio()||typeof tog0!=='function')return;
  if(typeof AudioContext==='undefined'&&typeof webkitAudioContext==='undefined')return;
  tog0.call(a);if(a.on){autoT=ahora();nivelar()}}catch(e){}}
function tocar(nombre){const f=efectos[nombre];if(!f||!encendido())return null;const c=cadenaViva();if(!c)return null;
  try{if(c.ctx.state==='suspended'&&c.ctx.resume)c.ctx.resume()}catch(e){}
  const g=gan(c.ctx,1);g.connect(c.bus);const t=c.ctx.currentTime+0.02,dur=f(c.ctx,g,t);
  luego(()=>{try{g.disconnect()}catch(e){}},(dur+0.6)*1000);return {g,dur}}
function sonar(nombre){try{const v=tocar(nombre);return v?v.dur:0}catch(e){return 0}}
/* el viento dura lo que dura el viaje: un soplo tras otro, encimados, hasta que la barca llega */
function soplar(){const v=viaje;if(!v)return;if(ahora()-v.desde>40000){llegar();return}
  let x=null;try{x=tocar('viento')}catch(e){}if(!x){viaje=null;return}
  v.voces.push(x);v.reloj=typeof setTimeout==='function'?setTimeout(soplar,(x.dur-1.2)*1000):0}
function zarpar(){llegar();enganchar();if(!encendido())return;viaje={voces:[],reloj:0,desde:ahora()};soplar()}
function llegar(){const v=viaje;viaje=null;if(!v)return;if(v.reloj&&typeof clearTimeout==='function')clearTimeout(v.reloj);
  for(const x of v.voces){try{x.g.gain.setTargetAtTime(0,x.g.context.currentTime,0.18)}catch(e){}}}
/* lo que avisa el motor: el sello espera a que terminen los golpes del puerto */
function evento(nombre){enganchar();
  if(nombre==='moneda'||nombre==='sello'){tMS=ahora();if(pingReloj){if(typeof clearTimeout==='function')clearTimeout(pingReloj);pingReloj=0}}
  if(nombre==='puerto'){finPuerto=ahora()+1150;sonar('puerto');return}
  /* el motor avisa el sello al zarpar: si la barca va de viaje, se guarda y suena al llegar, después del puerto */
  if(nombre==='sello'){luego(()=>{if(viaje){selloPend=true;return}const falta=finPuerto-ahora();if(falta>0)luego(()=>sonar('sello'),falta);else sonar('sello')},30);return}
  sonar(nombre)}

/* ---------- la medición: cada efecto en un OfflineAudioContext de 44 100 Hz, mono ---------- */
function rendir(ctx){return new Promise((si,no)=>{ctx.oncomplete=e=>si(e.renderedBuffer);try{const p=ctx.startRendering();if(p&&p.then)p.then(si,no)}catch(e){no(e)}})}
async function medir(O,nombre,conCadena){const HZ=44100,ctx=new O(1,HZ*8,HZ);
  /* con la cadena, el efecto empieza a los 0,3 s: el compresor recién creado arranca cerrado unas centésimas y se comería el golpe */
  const duracion=efectos[nombre](ctx,conCadena?cadena(ctx,ctx.destination).bus:ctx.destination,conCadena?0.3:0);
  const d=(await rendir(ctx)).getChannelData(0);let pico=0,invalidos=0,ult=-1;
  for(let i=0;i<d.length;i++){const v=d[i];if(v!==v||v===Infinity||v===-Infinity){invalidos++;continue}const a=v<0?-v:v;if(a>pico)pico=a;if(a>1e-4)ult=i}
  return {duracion,pico:+pico.toFixed(4),dBFS:pico>0?+(20*Math.log10(pico)).toFixed(1):-120,invalidos,fin:+((ult+1)/HZ).toFixed(3)}}
/* Devuelve [{nombre, duracion, pico, dBFS, invalidos, fin, picoSalida, dBFSSalida}]: pico y dBFS son del efecto solo
   (directo a la salida, lo más exigente); picoSalida, del efecto ya pasado por el compresor y la maestra, como se oye;
   fin es el segundo en que de verdad calla (tiene que ser ≤ duracion). */
async function probar(){
  const O=typeof OfflineAudioContext!=='undefined'?OfflineAudioContext:typeof webkitOfflineAudioContext!=='undefined'?webkitOfflineAudioContext:null;
  if(!O)return [];const sal=[];
  for(const nombre of Object.keys(efectos)){const c=await medir(O,nombre,false),s=await medir(O,nombre,true);
    sal.push({nombre,duracion:c.duracion,pico:c.pico,dBFS:c.dBFS,invalidos:c.invalidos+s.invalidos,fin:c.fin,picoSalida:s.pico,dBFSSalida:s.dBFS})}
  return sal}

/* ---------- registro en CAPA (si al cargar no está, no se falla) ---------- */
let suscrito=false;
function suscribir(){try{if(suscrito||typeof CAPA==='undefined'||!CAPA||typeof CAPA.oir!=='function')return suscrito;suscrito=true;
  CAPA.oir('toque',arrancar);CAPA.oir('zarpar',zarpar);
  CAPA.oir('parada',()=>{llegar();evento('puerto');if(selloPend){selloPend=false;luego(()=>sonar('sello'),1150)}});
  CAPA.oir('mar',()=>{llegar();selloPend=false;evento('mar')});
  CAPA.oir('moneda',()=>evento('moneda'));CAPA.oir('sello',()=>evento('sello'));return true}catch(e){return false}}
const api={efectos,sonar,probar,suscribir,clave:CLAVE,encendido,silencio};
try{if(typeof CAPA!=='undefined'&&CAPA){CAPA.sonido=api;suscribir()}}catch(e){}
})();
