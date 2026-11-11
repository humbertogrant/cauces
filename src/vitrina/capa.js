// La capa de acabado de la vitrina (docs/vitrina/contrato.md). Se carga antes que el motor: aquí solo se define CAPA; lo del
// motor (S, rioPor, render…) se usa dentro de funciones, que corren después. Los módulos (carta, panel, sonido) le agregan lo
// suyo: CAPA.descender, CAPA.pie, CAPA.mapa, CAPA.vista y oyentes con CAPA.oir. Si CAPA no existe, el motor juega como siempre.
const CAPA={rio:'nilo',fase:'parada',_oyentes:{},_pend:null,_toque:false,
  /* eventos del viaje: zarpar {r,de,a} · avanza {k,x,y} · parada {r,i} · mar {r} · moneda {} · sello {r,i} · toque {} */
  oir(nombre,fn){(CAPA._oyentes[nombre]=CAPA._oyentes[nombre]||[]).push(fn)},
  emitir(nombre,datos){const l=CAPA._oyentes[nombre];if(!l)return;for(const fn of l){try{fn(datos||{})}catch(e){if(typeof console!=='undefined'&&console.error)console.error('capa: falló un oyente de '+nombre,e)}}},
  /* la fase de una parada: 'parada' (lo que hay en ella) o 'navega' (la guía antes de zarpar); paso() la devuelve a 'parada' */
  navegar(){CAPA.fase='navega';render(false);if(typeof window!=='undefined'&&window.scrollTo)window.scrollTo(0,0)},
  momento(){if(typeof S==='undefined'||S.pantalla!=='rio'||S.tab!=='descender')return 'otro';
    const r=rioPor(S.rio);if(!r||r.id!==CAPA.rio)return 'otro';if(S.evento)return 'evento';/* la prueba entre puertos: el panel es el del motor, dentro de la misma hoja */
    const n=r.paradas.length,p=S.paso;
    if(p>n)return 'mar';if(CAPA.fase==='navega'&&p<n)return 'navega';return p===0?'portada':'parada'},
  /* la llegada se anuncia cuando la barca termina de viajar; si no hay animación en curso (pruebas, movimiento reducido), ya */
  llegada(r,a,enViaje){CAPA.llegar();CAPA._pend={r,a};if(!enViaje)CAPA.llegar()},
  llegar(){const p=CAPA._pend;if(!p)return;CAPA._pend=null;if(p.a>p.r.paradas.length)CAPA.emitir('mar',{r:p.r});else if(p.a>=1)CAPA.emitir('parada',{r:p.r,i:p.a-1})},
  /* el primer toque o tecla del jugador: ahí puede arrancar el sonido */
  escuchar(){if(CAPA._toque||typeof document==='undefined'||!document.addEventListener)return;CAPA._toque=true;
    const GESTOS=['pointerup','click','keydown'];/* en táctil, pointerdown no cuenta como gesto para el AudioContext: se espera a que el dedo se levante */
    const una=()=>{for(const g of GESTOS)document.removeEventListener(g,una,true);CAPA.emitir('toque',{})};
    for(const g of GESTOS)document.addEventListener(g,una,true)},
  /* la vitrina abre directo en su río (donde quedó anclada la barca, si quedó) */
  arranque(){CAPA.escuchar();if(typeof rioPor==='function'&&rioPor(CAPA.rio))abrirRio(CAPA.rio)}};
