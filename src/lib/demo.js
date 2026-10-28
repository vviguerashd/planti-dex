// Modo demo: sin Supabase configurado, la app corre con las 24 plantas y registros inventados
// en memoria. Sirve para ver el diseño antes de crear la base. Nada se guarda.
import plants from './demoData.json'

const VIC = 'demo-vic', FER = 'demo-fer'
const daysAgo = n => { const d = new Date(); d.setDate(d.getDate() - n); return d.toISOString() }
// Algunos casos para que se vean los cuatro estados
const seed = [
  ['P01', 'watered', 6, VIC, 'regular'], ['P02', 'watered', 2, FER, 'bien'], ['P03', 'watered', 5, VIC, null],
  ['P05', 'watered', 1, FER, 'bien'], ['P07', 'watered', 3, VIC, 'mal'], ['P06', 'watered', 4, FER, 'bien'],
  ['P08', 'watered', 12, VIC, null], ['P09', 'watered', 2, FER, 'bien'], ['P10', 'water_changed', 7, VIC, null],
  ['P11', 'water_changed', 2, FER, 'bien'], ['P13', 'water_changed', 9, VIC, 'regular'], ['P14', 'watered', 3, FER, 'bien'],
  ['P16', 'watered', 5, VIC, 'bien'], ['P17', 'watered', 7, FER, null], ['P23', 'watered', 3, VIC, null],
]
export const demo = {
  plants,
  logs: seed.map(([plant_id, action, d, by, condition], i) => ({ id: 'd' + i, plant_id, action, done_at: daysAgo(d), done_by: by, condition, note: null })),
  members: { [VIC]: 'Vic', [FER]: 'Fer' },
}
