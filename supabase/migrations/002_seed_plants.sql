-- planti-dex · las 24 plantas iniciales (fuente: hoja "Plantitas tamagochi: inventario", 27/10/2026)
-- Correr después de 001_schema.sql. Re-correrlo actualiza los datos sin borrar el historial.

insert into plants (id, name, species, zone, tracking, location_note, indoor, medium, light, water_interval_days, care_action, toxic_pets, notes) values
  ('P01', 'Pothos colgante (escalera)', 'Epipremnum aureum', 'escaleras', 'mascota', 'Colgada bajo la escalera exterior', false, 'Maceta colgante', 'Sombra o luz indirecta', 5, 'watered', 'si', 'Hojas secas y cafés en el centro de la maceta. Quitarlas y revisar si la tierra se seca de más entre riegos.'),
  ('P02', 'Pothos colgante (piedra)', 'Epipremnum aureum', 'escaleras', 'mascota', 'Sobre una piedra junto a la pared', false, 'Maceta colgante', 'Luz indirecta', 5, 'watered', 'si', 'Sana. Tallos largos con pocas hojas cerca de la maceta.'),
  ('P03', 'Limonero', 'Citrus (limonero)', 'jardin', 'mascota', 'Andador del patio, maceta verde', false, 'Maceta', 'Sol parcial', 5, 'watered', null, 'Maceta invadida por pasto y trébol, que le quitan agua. Hojas verde claro: vigilar.'),
  ('P04', 'Bugambilia roja (bolsa)', 'Bougainvillea', 'jardin', 'mascota', 'Debajo de la bugambilia grande (P18), aún sin sembrar', false, 'Bolsa de vivero', 'Sol parcial', 5, 'watered', null, 'Sigue en la bolsa del vivero, con trébol. Hojas amarillentas y moteadas: revisar el envés por plagas.'),
  ('P05', 'Begonia colgante', 'Begonia semperflorens', 'escaleras', 'mascota', 'Balcón, colgada del barandal', false, 'Maceta colgante', 'Sol parcial', 3, 'watered', 'si', 'Solo flores blancas. Algunas hojas bajas con bordes cafés.'),
  ('P06', 'Palo de Brasil grande (dos cañas)', 'Dracaena fragrans', 'sala', 'mascota', 'Rincón con guirnaldas de cempasúchil', true, 'Maceta', 'Luz indirecta', 10, 'watered', 'si', 'Hojas caídas y algunas puntas secas.'),
  ('P07', 'Palo de Brasil chico (maceta blanca)', 'Dracaena fragrans', 'sala', 'mascota', 'Junto al sillón', true, 'Maceta', 'Luz indirecta', 10, 'watered', 'si', 'Hojas caídas y retorcidas. Superficie de la tierra cuarteada en placas.'),
  ('P08', 'Palo de Brasil mediano (maceta verde)', 'Dracaena fragrans', 'sala', 'mascota', 'Rincón con piso de loseta roja', true, 'Maceta', 'Luz indirecta', 10, 'watered', 'si', 'Hojas colgando, una con borde amarillo. Superficie de la tierra cuarteada en placas.'),
  ('P09', 'Dieffenbachia', 'Dieffenbachia seguine', 'estudio', 'mascota', 'Maceta blanca sobre piso gris', true, 'Maceta', 'Luz indirecta', 7, 'watered', 'si', 'Sana. Hay una hoja seca dentro de la maceta: retirarla.'),
  ('P10', 'Esqueje de pothos (botella tapa azul A)', 'Epipremnum aureum', 'bufetera', 'esqueje', 'Botella con tapa azul', true, 'Agua', 'Luz indirecta', 7, 'water_changed', 'si', 'Raíces abundantes. Lista para pasar a tierra.'),
  ('P11', 'Esqueje de pothos (botella tapa azul B)', 'Epipremnum aureum', 'bufetera', 'esqueje', 'Botella con tapa azul', true, 'Agua', 'Luz indirecta', 7, 'water_changed', 'si', 'Esqueje joven, la raíz apenas empieza.'),
  ('P12', 'Esqueje de pothos (frasco de café)', 'Epipremnum aureum', 'bufetera', 'esqueje', 'Frasco de café de vidrio', true, 'Agua', 'Luz indirecta', 7, 'water_changed', 'si', 'Frasco de café de vidrio.'),
  ('P13', 'Esqueje de pothos neón (frasco de café)', 'Epipremnum aureum ''Neon''', 'bufetera', 'esqueje', 'Frasco de café de vidrio', true, 'Agua', 'Luz indirecta', 7, 'water_changed', 'si', 'Una hoja amarilla (normal al enraizar, retirarla). Agua turbia: cambiarla.'),
  ('P14', 'Liquidambar', 'Liquidambar styraciflua', 'jardin', 'zona', 'Jardín frontal', false, 'Suelo', 'Sol', 14, 'watered', null, 'El árbol más grande del jardín; copa triangular.'),
  ('P15', 'Bambú', 'Bambú (especie por confirmar)', 'jardin', 'zona', 'Tres puntos del jardín', false, 'Suelo', 'Sol', 7, 'watered', null, 'Hay bambú en tres puntos del jardín; se separará por zonas después.'),
  ('P16', 'Lengua de suegra', 'Sansevieria trifasciata ''Laurentii''', 'jardin', 'zona', 'Al pie del liquidambar', false, 'Suelo', 'Sombra parcial', 21, 'watered', 'si', 'Sana. Necesita muy poca agua.'),
  ('P17', 'Nochebuena', 'Euphorbia pulcherrima', 'jardin', 'zona', 'Esquina junto a la pared amarilla', false, 'Suelo', 'Sol parcial', 7, 'watered', 'irritante', 'Para pintarse de rojo en diciembre necesita noches largas sin luz artificial.'),
  ('P18', 'Bugambilia grande (morada)', 'Bougainvillea', 'jardin', 'zona', 'Jardinera elevada junto a la entrada', false, 'Suelo (jardinera)', 'Sol', 10, 'watered', null, 'Con flor.'),
  ('P19', 'Palma enana', 'Phoenix roebelenii', 'jardin', 'zona', 'Patio', false, 'Suelo', 'Sol', 10, 'watered', null, 'Muchas hojas secas acumuladas en el tronco: limpiar.'),
  ('P20', 'Flor morada (por identificar)', 'Por identificar: da flores moradas muy pequeñas', 'jardin', 'zona', 'Patio, junto a la palma', false, 'Suelo', 'Sol', 14, 'watered', null, 'Sana.'),
  ('P21', 'Iris africano', 'Dietes grandiflora', 'jardin', 'zona', 'Junto a la reja, entre piedras', false, 'Suelo', 'Sol', 10, 'watered', null, 'Con flor.'),
  ('P22', 'Duranta dorada (2 arbustos)', 'Duranta erecta ''Gold''', 'jardin', 'zona', 'Frente a la pared amarilla', false, 'Suelo', 'Sol', 7, 'watered', null, 'Podados en forma redonda. Sanos.'),
  ('P23', 'Cempasúchil (calabaza de Halloween)', 'Tagetes erecta', 'jardin', 'temporal', 'Calabaza de Halloween en el patio', false, 'Maceta', 'Sol', 2, 'watered', null, 'De temporada: darla de baja después de Día de Muertos.'),
  ('P24', 'Bugambilia naranja (bolsa)', 'Bougainvillea', 'jardin', 'mascota', 'Debajo de la bugambilia grande (P18), aún sin sembrar', false, 'Bolsa de vivero', 'Sol parcial', 5, 'watered', null, 'Sin foto todavía.')
on conflict (id) do update set
  name=excluded.name, species=excluded.species, zone=excluded.zone, tracking=excluded.tracking,
  location_note=excluded.location_note, indoor=excluded.indoor, medium=excluded.medium, light=excluded.light,
  water_interval_days=excluded.water_interval_days, care_action=excluded.care_action,
  toxic_pets=excluded.toxic_pets, notes=excluded.notes;
