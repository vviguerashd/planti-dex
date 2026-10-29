// Rutas sin router: "/", "/p/P07" (sticker de una planta) y "/z/jardin" (sticker de una zona).
export function parseRoute() {
  const path = window.location.pathname
  let m = path.match(/^\/p\/(P\d{2,3})\/?$/i)
  if (m) return { kind: 'plant', id: m[1].toUpperCase() }
  m = path.match(/^\/z\/([a-z]+)\/?$/i)
  if (m) return { kind: 'zone', id: m[1].toLowerCase() }
  return { kind: 'home' }
}
export function go(path) { window.history.pushState({}, '', path) }
