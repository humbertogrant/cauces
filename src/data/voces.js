// Voces genéricas del compañero (VOCES), rangos del tesoro (RANGOS) y voces de la economía: compartidos por todos los juegos.
// Las frases que nombran el río se sustituyen por VOCAB[tipo].voces en las rutas que no son ríos (ver docs/itinerarios.md).
const VOCES={
  ordenInicio:["Yo ya me la sé. ¿Y vos?","Tocá con calma; yo te miro.","Si te trabás, acordate de la frase."],
  ordenBien:["¡Esa es!","¡Sí! Seguí.","Yo también me la sabía.","¡Vamos bien!","Esa la vi pasar."],
  ordenMal:["Mmm, esa viene más adelante.","Todavía no llegamos ahí.","Casi. Pensá en la frase.","Nop. ¿Cuál venía primero?"],
  ordenFin:["¡Perfecto! ¡Te lo sabés como yo!","¡Casi perfecto! Uno más y me gano un pescado.","Volvamos a bajar el río juntos, con la frase en la mano."],
  pregunta:["¿Vos qué decís?","Pensá con calma.","Yo sé la respuesta, pero no digo nada.","Esta es fácil... ¿o no?","Mirá bien las opciones."],
  quizBien:["¡Sí! ¡Te lo sabías!","¡Eso! Yo estaba seguro.","¡Bravo! Otra más.","¡Claro que sí!","¡Ese es mi río!"],
  quizMal:["Uy. Esa se nos escapó.","No pasa nada: ahora ya la sabemos.","Yo también me habría confundido.","Mmm, esa la repasamos."],
  resultado:["¡Sos capitán de este río!","¡Bien! Un par de viajes más y sos capitán.","Bajemos el río otra vez; yo te acompaño."]
};
const RANGOS=[[500,"Señor de los Cauces"],[250,"Almirante"],[100,"Capitán"],[30,"Marinero"],[0,"Grumete"]];
const rango=t=>RANGOS.find(x=>t>=x[0])[1];
Object.assign(VOCES,{
  compra:["{g}: buena compra.","Cargado. Ahora a venderlo río abajo.","{g} en la bodega. ¿Cuánto valdrá más adelante?"],
  venta:["¡{n} monedas! Buen negocio.","Vendido por {n}. Yo ya lo sabía.","{n} monedas a la bolsa."],
  podrido:["Uy, {g}: se pasó. Al agua.","{g} podrido. Hay que vender más rápido."],
  sinMonedas:["No alcanzan las monedas. Vendé algo primero.","Estamos sin plata. ¿Qué tenés en la bodega?"],
  sinEspacio:["La bodega está llena. Vendé algo o dejalo.","Solo caben tres cosas. Elegí."],
  ganancia:["¡Qué negociante! Ganaste {n} monedas.","Ganaste {n} monedas. La próxima, más.","Esta vez no ganamos nada. Yo te sigo queriendo."]
});
