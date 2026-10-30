// Temporada de adornos según la fecha local (no UTC: Pachuca es UTC-6).
// Por ahora solo Halloween / Día de Muertos: del 15 de octubre al 2 de noviembre.
export function currentSeason(date = new Date()) {
  const m = date.getMonth() + 1, d = date.getDate()
  if ((m === 10 && d >= 15) || (m === 11 && d <= 2)) return 'halloween'
  return null
}
