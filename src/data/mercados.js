const MERCADOS={
nilo:[{n:"café",e:"☕",o:0,b:3},{n:"pescado seco",e:"🐟",o:1,b:2,d:2},{n:"goma arábiga",e:"🍯",o:2,b:4},{n:"dátiles",e:"🌴",o:3,b:3},{n:"trigo",e:"🌾",o:4,b:3}],
amazonas:[{n:"caucho",e:"🛞",o:0,b:4,m:2},{n:"pirarucú",e:"🐟",o:1,b:3,d:2},{n:"plátanos",e:"🍌",o:1,b:2,d:2},{n:"castañas",e:"🌰",o:2,b:3},{n:"soya",e:"🫘",o:3,b:2}],
yangtse:[{n:"sal",e:"🧂",o:0,b:3},{n:"pimienta",e:"🌶️",o:0,b:2},{n:"naranjas",e:"🍊",o:1,b:2,d:2},{n:"té",e:"🍵",o:2,b:4},{n:"brocado",e:"🧵",o:3,b:5}],
misisipi:[{n:"harina",e:"🌾",o:0,b:3},{n:"manzanas",e:"🍎",o:0,b:2,d:2},{n:"pieles",e:"🦫",o:1,b:4,m:4},{n:"algodón",e:"☁️",o:2,b:4},{n:"azúcar",e:"🍬",o:3,b:3}],
danubio:[{n:"vino",e:"🍷",o:0,b:3},{n:"sal",e:"🧂",o:1,b:3,m:4},{n:"cuchillos",e:"🔪",o:2,b:4},{n:"tarta Linzer",e:"🥧",o:3,b:2,d:2},{n:"pastel Sacher",e:"🍰",o:4,b:3,d:2},{n:"trigo",e:"🌾",o:5,b:2},{n:"pimentón",e:"🌶️",o:6,b:3}],
rin:[{n:"sal",e:"🧂",o:0,b:3},{n:"chucrut",e:"🥬",o:1,b:2,d:2},{n:"libros",e:"📚",o:2,b:4},{n:"pizarra",e:"🪨",o:3,b:2},{n:"perfume",e:"🧴",o:4,b:5},{n:"carbón",e:"⚫",o:5,b:3}],
ganges:[{n:"agua sagrada",e:"🏺",o:0,b:2},{n:"cuero",e:"👞",o:1,b:3},{n:"guayabas",e:"🍈",o:2,b:2,d:2},{n:"seda",e:"🧵",o:3,b:5},{n:"arroz",e:"🍚",o:4,b:3}],
volga:[{n:"pieles",e:"🦫",o:0,b:4,m:2},{n:"lino",e:"🧵",o:1,b:3},{n:"té",e:"🍵",o:2,b:4},{n:"cuero",e:"👞",o:3,b:3},{n:"trigo",e:"🌾",o:4,b:2},{n:"sandías",e:"🍉",o:5,b:2,d:2}],
tigris:[{n:"sandías",e:"🍉",o:0,b:2,d:2},{n:"cobre",e:"🥉",o:0,b:4,m:4},{n:"muselina",e:"🧵",o:1,b:3},{n:"lana",e:"🐑",o:2,b:2},{n:"cerámica",e:"🏺",o:3,b:4},{n:"papel",e:"📜",o:4,b:3}],
mekong:[{n:"té pu'er",e:"🍵",o:0,b:4},{n:"seda",e:"🧵",o:1,b:4},{n:"mangos",e:"🥭",o:1,b:2,d:2},{n:"teca",e:"🪵",o:2,b:3},{n:"prahok",e:"🐟",o:3,b:2}],
niger:[{n:"oro",e:"🪙",o:0,b:5,m:2},{n:"pescado",e:"🐟",o:1,b:2,d:2},{n:"sal",e:"🧂",o:2,b:3},{n:"manuscrito",e:"📜",o:2,b:4},{n:"telas índigo",e:"🧵",o:3,b:3},{n:"cacahuate",e:"🥜",o:4,b:2},{n:"aceite de palma",e:"🫙",o:5,b:3}],
parana:[{n:"yerba mate",e:"🧉",o:0,b:3,m:4},{n:"naranjas",e:"🍊",o:1,b:2,d:2},{n:"algodón",e:"☁️",o:2,b:3},{n:"soya",e:"🫘",o:3,b:3},{n:"carne",e:"🥩",o:4,b:4,d:1}],
indo:[{n:"pashmina",e:"🧣",o:0,b:5},{n:"albaricoques",e:"🍑",o:1,b:2},{n:"almendras",e:"🌰",o:2,b:3},{n:"dátiles",e:"🌴",o:3,b:3},{n:"ajrak",e:"🧵",o:4,b:4}],
tempisque:[{n:"cueros",e:"🐂",o:0,b:3,m:4},{n:"queso",e:"🧀",o:1,b:2,d:3},{n:"marañón",e:"🌰",o:2,b:3,m:4},{n:"maíz",e:"🌽",o:3,b:2}],
reventazon:[{n:"café",e:"☕",o:0,b:3,m:4},{n:"tallas",e:"🪵",o:1,b:2},{n:"tapa de dulce",e:"🍯",o:2,b:2,m:5},{n:"queso",e:"🧀",o:3,b:3,d:2},{n:"bananos",e:"🍌",o:4,b:2,d:2}],
sarapiqui:[{n:"queso",e:"🧀",o:0,b:2,d:3},{n:"palmito",e:"🥬",o:1,b:3,m:3},{n:"piñas",e:"🍍",o:2,b:2,d:2},{n:"cacao",e:"🍫",o:3,b:3}],
sanjuan:[{n:"queso",e:"🧀",o:0,b:3,d:3},{n:"cacao",e:"🍫",o:1,b:2,m:5},{n:"madera",e:"🪵",o:2,b:3},{n:"bananos",e:"🍌",o:3,b:2,d:2},{n:"pescado seco",e:"🐟",o:4,b:2}],
tarcoles:[{n:"café",e:"☕",o:0,b:3,m:3},{n:"chips",e:"💾",o:1,b:5,m:4},{n:"tapa de dulce",e:"🍯",o:2,b:2},{n:"frutas",e:"🥭",o:3,b:2,d:2}],
terraba:[{n:"café",e:"☕",o:0,b:3,m:3},{n:"piñas",e:"🍍",o:1,b:2,d:2},{n:"maíz",e:"🌽",o:2,b:2},{n:"máscaras",e:"🎭",o:3,b:4,m:5},{n:"bananos",e:"🍌",o:4,b:2,d:2}]
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
