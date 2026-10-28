// Siempre fechas LOCALES (Pachuca, UTC-6). Nunca toISOString() para "hoy".
export function startOfLocalDay(d) {
  const x = new Date(d)
  return new Date(x.getFullYear(), x.getMonth(), x.getDate())
}
export function daysBetween(a, b) {
  return Math.round((startOfLocalDay(b) - startOfLocalDay(a)) / 86400000)
}
export function addDays(d, n) {
  const x = startOfLocalDay(d); x.setDate(x.getDate() + n); return x
}
const fmt = new Intl.DateTimeFormat('es-MX', { day: 'numeric', month: 'short' })
export function shortDate(d) { return fmt.format(new Date(d)) }
export function relativeDay(d) {
  const n = daysBetween(d, new Date())
  if (n === 0) return 'hoy'
  if (n === 1) return 'ayer'
  return `hace ${n} días`
}
