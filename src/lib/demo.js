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
  bins: [
    { id: 'L1', name: 'Depósito 1 · cubetas', notes: 'Dos cubetas de 19 L apiladas: arriba tierra y lombrices, abajo junta el líquido.' },
    { id: 'L2', name: 'Depósito 2 · talavera', notes: 'Maceta de talavera con girasoles sobre base de fierro.' },
  ],
  compostLogs: [
    { id: 'c1', bin_id: 'L1', action: 'feed', done_at: daysAgo(8), done_by: VIC, note: null },
    { id: 'c2', bin_id: 'L2', action: 'feed', done_at: daysAgo(3), done_by: VIC, note: null },
    { id: 'c3', bin_id: 'L2', action: 'moisture_ok', done_at: daysAgo(3), done_by: VIC, note: null },
  ],
}
