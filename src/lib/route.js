// Rutas sin router: "/", "/p/P07" (planta), "/z/jardin" (zona), "/lluvia" y "/l/L1" (depósito de lombricomposta).
export function parseRoute() {
  const path = window.location.pathname
  let m = path.match(/^\/p\/(P\d{2,3})\/?$/i)
  if (m) return { kind: 'plant', id: m[1].toUpperCase() }
  m = path.match(/^\/z\/([a-z]+)\/?$/i)
  if (m) return { kind: 'zone', id: m[1].toLowerCase() }
  if (/^\/lluvia\/?$/i.test(path)) return { kind: 'rain' }
  m = path.match(/^\/l\/(L\d)\/?$/i)
  if (m) return { kind: 'compost', id: m[1].toUpperCase() }
  return { kind: 'home' }
}
export function go(path) { window.history.pushState({}, '', path) }
