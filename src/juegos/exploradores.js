// Configuración del juego Exploradores: viajes de exploradores y conquistadores, etapa por etapa, con el mismo motor de Cauces.
const JUEGO={id:'exploradores',nombre:'Exploradores',sub:'Los grandes viajes, etapa por etapa',tipo:'itinerario',clave:'exploradores',
  zonas:{},
  rutas:()=>ITINERARIOS,
  grupos:[{titulo:'Viajeros',filtro:r=>!r.conquista,nota:'Los que fueron a ver: peregrinos, mercaderes y marinos. Cada viaje se recorre en orden, con su caravana o su flota, un animal de guía y una carga que se cambia en cada alto.'},
    {titulo:'Conquistadores',clase:'zona-titulo',filtro:r=>!!r.conquista,nota:'Los que fueron a quedarse: ejércitos, alianzas y ciudades tomadas. Se cuentan con los que ganaron y con los que perdieron.'}],
  rangos:[[500,'Señor de los Caminos'],[250,'Gran Viajero'],[100,'Caravanero'],[30,'Peregrino'],[0,'Aprendiz']],
  comoSeJuega:'<p>Cada viaje es un recorrido fijo de la partida al regreso, y cada etapa una habitación con una imagen absurda que la amarra al lugar. Cada viaje se hace con su propia caravana, flota o ejército, con un animal de guía y una carga que se cambia en cada alto. Recorrés el viaje una vez, después lo ordenás de memoria y luego te pregunto. Lo que fallés vuelve pronto; lo que sepás se espacia.</p>'};
