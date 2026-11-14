// Lombricomposta: rutina semanal (sábado) y cosecha cada 3–4 meses.
import { daysBetween } from './dates'

export const COMPOST_ACTIONS = {
  feed: 'Alimenté',
  bedding: 'Puse hojas secas o cartón',
  moisture_ok: 'Humedad bien',
  moisture_dry: 'Estaba seca (le eché agua)',
  moisture_wet: 'Estaba encharcada (le puse cama seca)',
  drained: 'Vacié el líquido',
  harvest: 'Coseché',
}
export const FEED_DAYS = 7
export const HARVEST_DAYS = 90

export function compostStatus(bin, logs) {
  const mine = logs.filter(l => l.bin_id === bin.id)
  const last = a => mine.find(l => l.action === a) || null
  const lastFeed = last('feed'), lastHarvest = last('harvest')
  const lastMoist = mine.find(l => l.action.startsWith('moisture_')) || null
  const daysFed = lastFeed ? daysBetween(lastFeed.done_at, new Date()) : null
  const sinceHarvest = lastHarvest ? daysBetween(lastHarvest.done_at, new Date()) : null
  const hungry = daysFed === null || daysFed >= FEED_DAYS
  // Mismo vocabulario de ánimo que las plantas para que Gala y los chips funcionen igual.
  const mood = daysFed === null ? 'sin_registro' : daysFed >= FEED_DAYS * 2 ? 'sedienta' : hungry ? 'con_sed' : 'feliz'
  return { mood, hungry, lastFeed, lastHarvest, lastMoist, daysFed, sinceHarvest, harvestDue: sinceHarvest !== null && sinceHarvest >= HARVEST_DAYS }
}
export const COMPOST_MOOD_LABEL = { feliz: 'Comieron esta semana', con_sed: 'Tienen hambre', sedienta: 'Mucha hambre', sin_registro: 'Sin registro' }
