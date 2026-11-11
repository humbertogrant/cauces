// Configuración de la vitrina del Nilo: el mismo motor y los mismos datos de Cauces, con un solo río y la capa de acabado de
// src/vitrina/ encima (ver docs/vitrina/contrato.md). Guarda aparte de Cauces (clave propia) para no mezclar pasaportes.
const JUEGO={id:'nilo',nombre:'Cauces',sub:'El Nilo, ciudad por ciudad',tipo:'rio',clave:'cauces-nilo',
  zonas:{},
  rutas:()=>RIVERS.filter(r=>r.id==='nilo').map(desdeRio),
  grupos:[{titulo:'El Nilo',filtro:r=>true}],
  comoSeJuega:'<p>Cada río es un recorrido fijo de la fuente al mar, y cada ciudad una habitación con una imagen absurda que la amarra al lugar. Cada río se baja en su propia embarcación, con un animal de guía y una bodega que cambia en cada puerto. Bajás el río una vez, después lo ordenás de memoria y luego te pregunto. Lo que fallés vuelve pronto; lo que sepás se espacia.</p>'};
