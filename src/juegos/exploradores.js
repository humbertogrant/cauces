// Configuración del juego Exploradores: viajes de exploradores y conquistadores, etapa por etapa, con el mismo motor de Cauces.
const JUEGO={id:'exploradores',nombre:'Exploradores',sub:'Los grandes viajes, etapa por etapa',tipo:'itinerario',clave:'exploradores',
  zonas:{},
  rutas:()=>ITINERARIOS,
  grupos:[{titulo:'Los grandes viajes',filtro:r=>true,nota:'Cada viaje se recorre en orden, etapa por etapa, con una caravana, un animal de guía y un morral que se cambia en cada alto.'}],
  rangos:[[500,'Señor de los Caminos'],[250,'Gran Viajero'],[100,'Caravanero'],[30,'Peregrino'],[0,'Aprendiz']],
  comoSeJuega:'<p>Cada viaje es un recorrido fijo de la partida al regreso, y cada etapa una habitación con una imagen absurda que la amarra al lugar. Cada viaje se hace con su propia caravana, con un animal de guía y un morral que se cambia en cada alto. Recorrés el viaje una vez, después lo ordenás de memoria y luego te pregunto. Lo que fallés vuelve pronto; lo que sepás se espacia.</p>'};
