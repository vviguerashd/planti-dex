import { t } from '../lib/theme'
// Nunca pantalla en blanco: así se distingue "cargando" de "algo se rompió".
export default function Loading() {
  return (
    <main style={{ minHeight: '70vh', display: 'grid', placeItems: 'center', color: t.ink }}>
      <div role="status" style={{ textAlign: 'center' }}>
        <img className="pixel" src="/sprites/P01_feliz.png" alt="" width={80} height={96} />
        <p style={{ fontFamily: t.pixelFont, fontSize: 12, color: t.brand }}>Regando datos…</p>
      </div>
    </main>
  )
}
