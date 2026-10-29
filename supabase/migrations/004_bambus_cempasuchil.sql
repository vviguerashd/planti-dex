-- planti-dex · el bambú se separa en tres puntos y llega el segundo cempasúchil.
-- P15 se queda como el bambú de la cochera (su id no cambia: puede estar en un sticker).

update plants set name = 'Bambú (cochera)', location_note = 'Cochera, junto a la reja',
  notes = 'Uno de los tres bambús del jardín.' where id = 'P15';

update plants set name = 'Cempasúchil (calabaza 1)' where id = 'P23';

insert into plants (id, name, species, zone, tracking, location_note, indoor, medium, light, water_interval_days, care_action, toxic_pets, notes) values
  ('P25', 'Bambú (pasillo, junto al iris)', 'Bambú (especie por confirmar)', 'jardin', 'zona', 'Pasillo del patio, entre el iris y el liquidámbar', false, 'Suelo', 'Sol', 7, 'watered', null, 'Uno de los tres bambús del jardín.'),
  ('P26', 'Bambú (pasillo, junto al limón)', 'Bambú (especie por confirmar)', 'jardin', 'zona', 'Pasillo del patio, entre el limón y la palma', false, 'Suelo', 'Sol', 7, 'watered', null, 'Uno de los tres bambús del jardín.'),
  ('P27', 'Cempasúchil (calabaza 2)', 'Tagetes erecta', 'jardin', 'temporal', 'Calabaza de Halloween junto a la casita', false, 'Maceta', 'Sol', 2, 'watered', null, 'De temporada: darla de baja después de Día de Muertos.')
on conflict (id) do nothing;
