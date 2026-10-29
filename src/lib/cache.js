// Caché por dispositivo (conveniencia, no fuente de verdad): la última lectura se muestra al
// instante y luego se refresca contra Supabase. La primera consulta a Supabase en frío tarda 1–3 s.
const KEY = 'plantidex_cache_v1'
export function readCache() {
  try { return JSON.parse(localStorage.getItem(KEY)) } catch { return null }
}
export function writeCache(data) {
  try { localStorage.setItem(KEY, JSON.stringify(data)) } catch { /* sin almacenamiento: no pasa nada */ }
}
export function clearCache() {
  try { localStorage.removeItem(KEY) } catch { /* idem */ }
}
