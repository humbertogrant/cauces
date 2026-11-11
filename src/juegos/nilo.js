// Configuración de la vitrina del Nilo: el mismo motor y los mismos datos de Cauces, con un solo río y la capa de acabado de
// src/vitrina/ encima (ver docs/vitrina/contrato.md). Guarda aparte de Cauces (clave propia) para no mezclar pasaportes.
const JUEGO={id:'nilo',nombre:'Cauces',sub:'El Nilo, ciudad por ciudad',tipo:'rio',clave:'cauces-nilo',
  zonas:{},
  rutas:()=>RIVERS.filter(r=>r.id==='nilo').map(r=>desdeRio(cauceFino(r))),
  grupos:[{titulo:'El Nilo',filtro:r=>true}],
  comoSeJuega:'<p>Cada río es un recorrido fijo de la fuente al mar, y cada ciudad una habitación con una imagen absurda que la amarra al lugar. Cada río se baja en su propia embarcación, con un animal de guía y una bodega que cambia en cada puerto. Bajás el río una vez, después lo ordenás de memoria y luego te pregunto. Lo que fallés vuelve pronto; lo que sepás se espacia.</p>'};
/* El cauce fino de la vitrina (CARTA.curso, de Natural Earth 10 m; lo genera tools/carta.py) sin que cambie ninguna cifra del juego.
   Con otro dibujo del río cambiarían los kilómetros de cada parada (salen de la fracción del cauce) y la altura que se lee en cada
   una (sale del perfil, que va por fracción). Aquí, antes de que el motor vea el río: (1) los kilómetros se calculan con el curso de
   Cauces, igual que normalizar(), y quedan fijos en cada parada; (2) el perfil de altura pasa al cauce nuevo corriendo sus
   fracciones entre parada y parada, con cada parada como punto del perfil, así que en cada una se lee la misma altura que en
   Cauces. Sin CARTA.curso no hace nada. test/vitrina.js compara las cifras con las de dist/cauces-amplia.html. */
function cauceFino(r){const C=typeof CARTA!=='undefined'&&CARTA.curso;if(!C||C.length<2||r._fino)return r;
  const medir=curso=>{const L=[0];for(let i=1;i<curso.length;i++)L[i]=L[i-1]+hav(curso[i-1],curso[i]);const tot=L[L.length-1];let ult=0;
    return r.ciudades.map(c=>{let best=ult,bd=1e9;for(let i=ult;i<curso.length;i++){const d=(curso[i][0]-c.pos[0])**2+(curso[i][1]-c.pos[1])**2;if(d<bd){bd=d;best=i}}ult=best;return{f:L[best]/tot,km:Math.round(L[best]/tot*(r.longitud||tot))}})};
  const antes=medir(r.curso),ahora=medir(C);
  for(let i=1;i<ahora.length;i++)if(!(ahora[i].f>ahora[i-1].f))return r;/* las paradas tienen que quedar en orden sobre el cauce nuevo; si no, se queda el de Cauces */
  const P=typeof ALTURAS!=='undefined'&&ALTURAS[r.id];
  if(P){const alt=f=>{if(f<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++)if(f<=P[i][0]){const a=P[i-1],b=P[i];return a[1]+(b[1]-a[1])*((f-a[0])/((b[0]-a[0])||1))}return P[P.length-1][1]};
    const anc=[[0,0],...antes.map((a,i)=>[a.f,ahora[i].f]),[1,1]];/* fracción vieja → fracción nueva, por tramos entre paradas */
    const g=f=>{for(let i=1;i<anc.length;i++)if(f<=anc[i][0]){const a=anc[i-1],b=anc[i];return a[1]+(b[1]-a[1])*((f-a[0])/((b[0]-a[0])||1))}return 1};
    const pts=P.map(p=>[p[0],p[1]]).concat(antes.map(a=>[a.f,alt(a.f)])).sort((a,b)=>a[0]-b[0]||b[1]-a[1]);
    ALTURAS[r.id]=pts.map(p=>[g(p[0]),p[1]])}
  r.ciudades.forEach((c,i)=>Object.defineProperty(c,'km',{get:()=>antes[i].km,set(){},enumerable:true,configurable:true}));
  r.curso=C;if(CARTA.brazos&&CARTA.brazos.length)r.brazos=CARTA.brazos;r._fino=true;return r}
