import { addDays, daysBetween } from './dates'

// Misma regla que la hoja de cálculo:
// Enferma gana si el último "cómo se ve" fue "mal"; si no, manda el calendario de riego.
export const MOODS = {
  feliz:        { label: 'Feliz',        sprite: 'feliz' },
  con_sed:      { label: 'Con sed',      sprite: 'con_sed' },
  sedienta:     { label: 'Sedienta',     sprite: 'sedienta' },
  enferma:      { label: 'Enferma',      sprite: 'enferma' },
  sin_registro: { label: 'Sin registro', sprite: 'feliz' },
}

export function plantStatus(plant, logs) {
  const mine = logs.filter(l => l.plant_id === plant.id)          // ya vienen ordenados desc
  const lastCare = mine.find(l => l.action === plant.care_action) || null
  const lastCondition = mine.find(l => l.condition) || null
  let next = null, daysLeft = null
  if (lastCare) {
    next = addDays(lastCare.done_at, plant.water_interval_days)
    daysLeft = daysBetween(new Date(), next)
  }
  let mood = 'sin_registro'
  if (lastCondition?.condition === 'mal') mood = 'enferma'
  else if (daysLeft !== null) mood = daysLeft < 0 ? 'sedienta' : daysLeft === 0 ? 'con_sed' : 'feliz'
  return { lastCare, lastCondition, next, daysLeft, mood }
}

export function spriteUrl(plantId, mood) {
  return `/sprites/${plantId}_${MOODS[mood].sprite}.png`
}
