// Configuración del juego Cauces: nombre, tipo de ruta por defecto, clave de guardado, zonas del mapa, grupos de la lista y
// textos de portada. Se carga antes de motor.js; JUEGO.rutas() entrega las rutas ya en el esquema RUTA (docs/itinerarios.md).
const JUEGO={id:'cauces',nombre:'Cauces',sub:'Los grandes ríos, ciudad por ciudad',tipo:'rio',clave:'cauces',
  zonas:{cr:{nombre:'Costa Rica',pos:[10.3,-84.3]}},
  rutas:()=>RIVERS.map(desdeRio),
  grupos:[{titulo:'Los grandes ríos',filtro:r=>!r.zona,antes:'<div class="frase"><div class="fkicker">Podio por longitud</div><div class="ftexto"><b>No</b> <b>Am</b>es <b>Ya</b> <b>M</b>ás</div><div class="fnota">Nilo, Amazonas, Yangtsé, Misisipi: los cuatro más largos, en orden.</div></div>'},
    {titulo:'Ríos de Costa Rica',clase:'zona-titulo',filtro:r=>r.zona==='cr',nota:'Seis ríos de casa, con su historia: el Tempisque, el Reventazón, el Sarapiquí, el San Juan de la frontera, el Tárcoles y el Térraba.'}],
  comoSeJuega:'<p>Cada río es un recorrido fijo de la fuente al mar, y cada ciudad una habitación con una imagen absurda que la amarra al lugar. Cada río se baja en su propia embarcación, con un animal de guía y una bodega que cambia en cada puerto. Bajás el río una vez, después lo ordenás de memoria y luego te pregunto. Lo que fallés vuelve pronto; lo que sepás se espacia.</p>'};
