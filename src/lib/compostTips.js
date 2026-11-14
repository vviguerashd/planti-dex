// Lo aprendido sobre la lombricomposta (sesión del 13 nov 2026), en tarjetas.
// Cada semana la app abre en un tip distinto; el carrusel deja ver todos.
export const COMPOST_TIPS = [
  { cat: 'comida', title: 'Las lombrices no comen la comida tal cual', body: 'Primero bacterias y hongos ablandan los restos y luego la lombriz se come esa papilla junto con los microbios. Comida picada se deshace mucho más rápido que entera.' },
  { cat: 'comida', title: 'Poquito y seguido', body: 'La población se ajusta a la comida: con un montón una vez al mes mantienes pocas lombrices. Con porciones chicas cada sábado, crecen.' },
  { cat: 'comida', title: '¿Les doy más o menos?', body: 'Antes de alimentar, busca la comida del sábado pasado. Si queda mucha, da menos esta vez. Si no queda nada, da un poco más.' },
  { cat: 'comida', title: 'Entiérrala en otra esquina', body: 'Cada semana pon la comida en una esquina distinta y tápala con tierra. Así no se acumula en un solo lugar y no atrae moscas.' },
  { cat: 'comida', title: 'Congelar sí ayuda', body: 'Junta los restos de la semana en el congelador: no huelen, no hay moscas, y el hielo rompe las células para que se deshagan rápido. Es opcional, no obligatorio.' },
  { cat: 'comida', title: 'Descongela y escurre', body: 'Saca los restos el viernes en la noche. Congelados enfrían su zona y al derretirse sueltan agua de golpe: escúrrelos antes de echarlos.' },
  { cat: 'comida', title: 'Qué no va', body: 'Nada de grasa, aceite, carne, lácteos ni huesos. Tampoco mucho cítrico, cebolla o ajo de golpe. Restos de fruta, verdura, café y cáscara de huevo molida, sí.' },
  { cat: 'cama', title: 'La cama café', body: 'Cartón picado y hojas secas son la cama: absorben la humedad de la comida y les dan dónde esconderse. Es lo que más le faltaba a tus depósitos.' },
  { cat: 'cama', title: 'Comida siempre tapada', body: 'Después de alimentar, un puñado de hojas secas o cartón encima. Tapa el olor, guarda la humedad y evita moscas.' },
  { cat: 'cama', title: 'No tires las hojas del jardín', body: 'Las hojas que barres son alimento y cama. Guárdalas secas para tener reserva todo el año.' },
  { cat: 'cama', title: 'Secar hojas: con aire', body: 'Sécalas en un costal de rafia o extendidas en la azotea. En bolsa negra cerrada no se secan: sudan y se pudren.' },
  { cat: 'humedad', title: 'Prueba del puño', body: 'Aprieta un puñado de tierra. Bien: suelta unas gotas, como esponja exprimida. Nada: rocía agua. Escurre: agrega cama seca.' },
  { cat: 'humedad', title: 'Sombra y tapa', body: 'El sol directo las seca y las calienta. Tus tapetes de fibra de coco son buena tapa: dejan respirar, dan sombra y guardan humedad.' },
  { cat: 'humedad', title: 'Podrido bueno, podrido malo', body: 'Que la comida se descomponga es buena señal. Lo malo es que se pudra sin aire: olor agrio o a huevo, o pasta pegajosa. Eso es exceso de agua o comida.' },
  { cat: 'humedad', title: 'Si huele feo', body: 'Deja de alimentar una semana, mezcla bastante cama seca y revuelve un poco para que entre aire. Una buena lombricomposta huele a tierra mojada.' },
  { cat: 'liquido', title: 'El agua negra no es premio', body: 'El líquido de la cubeta de abajo es agua que atravesó el depósito. Mucho y muy oscuro casi siempre significa que sobra agua o comida, no que vaya mejor.' },
  { cat: 'liquido', title: 'Tu agua clarita está bien', body: 'Alimentas poco y no encharcas, por eso escurre poco y claro. Tu tesoro es la tierra negra de arriba, no el agua de abajo.' },
  { cat: 'liquido', title: 'Si usas el líquido', body: 'Diluye 1 parte en 10 de agua, solo en plantas de ornato y nunca si huele feo. Lo más seguro es tirarlo.' },
  { cat: 'lombrices', title: 'No las sueltes en el jardín', body: 'La californiana vive en hojarasca y materia orgánica, no en tierra limpia. Al jardín va la composta; las lombrices se quedan en sus depósitos.' },
  { cat: 'lombrices', title: 'No están solas', body: 'Además de lombrices hay bichitos chiquitos, ácaros, hongos y bacterias. Son parte del equipo, no una plaga.' },
  { cat: 'cosecha', title: '¿Ya toca cosechar?', body: 'Casi todo es tierra negra granulada, ya no reconoces la comida y huele a bosque. Suele pasar cada 3 o 4 meses.' },
  { cat: 'cosecha', title: 'Depósito 1: tercera cubeta', body: 'Pon encima una cubeta perforada con cama y comida. En 3 a 4 semanas las lombrices suben solas y la de en medio ya es composta.' },
  { cat: 'cosecha', title: 'Depósito 2: de un lado al otro', body: 'Empuja la tierra a una mitad y alimenta solo la otra durante 2 o 3 semanas. Las lombrices se mudan y cosechas el lado viejo.' },
  { cat: 'cosecha', title: 'Montoncitos al sol', body: 'Sobre una lona, haz conos con la composta. Las lombrices huyen de la luz y bajan; cada 20 minutos raspa la capa de arriba.' },
  { cat: 'cosecha', title: 'No necesitas tierra nueva', body: 'Después de cosechar rellena con cama humedecida y un puñado de composta vieja para los microbios. Eso se vuelve tierra en unos meses.' },
  { cat: 'cosecha', title: 'Cómo usar la composta', body: 'Una capa de 1 a 2 cm alrededor de la planta, o 1 parte por 3 o 4 de tierra en macetas. Mejora la tierra poco a poco: se nota en meses, no en días.' },
]

export function weekIndex(date = new Date()) {
  const start = new Date(date.getFullYear(), 0, 1)
  return Math.floor((date - start) / (7 * 86400000))
}
