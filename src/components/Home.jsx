import { ZONES } from '../lib/zones'
import { MOODS, plantStatus, spriteUrl } from '../lib/mood'
import { t } from '../lib/theme'

const URGENCY = { sedienta: 0, enferma: 1, con_sed: 2, sin_registro: 3, feliz: 4 }

export default function Home({ plants, logs, onOpen, onOpenZone }) {
  const items = plants.map(p => ({ plant: p, status: plantStatus(p, logs) }))
  const need = items.filter(i => ['sedienta', 'con_sed', 'enferma'].includes(i.status.mood)).length

  return (
    <>
      <header style={{ background: t.brand, color: '#fff', padding: '18px 16px 16px' }}>
        <h1 style={{ margin: 0, fontFamily: t.pixelFont, fontSize: 18, lineHeight: 1.4 }}>Planti-dex</h1>
        <p style={{ margin: '8px 0 0', fontSize: 15 }}>
          {need === 0 ? 'Todas están bien por ahora.' : `${need} ${need === 1 ? 'planta necesita' : 'plantas necesitan'} atención.`}
        </p>
      </header>
      <main style={{ padding: '8px 16px 40px', maxWidth: 900, margin: '0 auto' }}>
        {ZONES.map(z => {
          const inZone = items.filter(i => i.plant.zone === z.id)
            .sort((a, b) => URGENCY[a.status.mood] - URGENCY[b.status.mood] || a.plant.id.localeCompare(b.plant.id))
          if (!inZone.length) return null
          return (
            <section key={z.id} aria-labelledby={`zona-${z.id}`}>
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 8, margin: '24px 0 12px' }}>
                <h2 id={`zona-${z.id}`} style={{ fontFamily: t.pixelFont, fontSize: 13, color: t.brand, margin: 0 }}>
                  {z.label} <span style={{ fontFamily: t.bodyFont, fontSize: 14, color: t.inkMuted }}>· {inZone.length}</span>
                </h2>
                {inZone.length > 1 && (
                  <button onClick={() => onOpenZone(z.id)} style={{ background: 'none', border: 0, padding: 4, color: t.brand, fontWeight: 700, textDecoration: 'underline', cursor: 'pointer', fontSize: 14 }}>
                    Regar varias
                  </button>
                )}
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(104px, 1fr))', gap: 10 }}>
                {inZone.map(({ plant, status }) => <Tile key={plant.id} plant={plant} status={status} onOpen={onOpen} />)}
              </ul>
            </section>
          )
        })}
      </main>
    </>
  )
}

function Tile({ plant, status, onOpen }) {
  const m = t.mood[status.mood]
  const name = plant.nickname || plant.name
  return (
    <li>
      <button onClick={() => onOpen(plant.id)} style={{ width: '100%', border: `2px solid ${t.line}`, borderRadius: 12, background: t.surface, padding: '8px 6px 10px', cursor: 'pointer', color: t.ink, textAlign: 'center' }}>
        <img className="pixel" src={spriteUrl(plant.id, status.mood)} alt="" width={80} height={96} style={{ display: 'block', margin: '0 auto' }} />
        <span style={{ display: 'block', fontSize: 13, fontWeight: 600, lineHeight: 1.25, marginTop: 4, minHeight: 32 }}>{name}</span>
        <span style={{ display: 'inline-block', marginTop: 6, fontSize: 12, fontWeight: 700, padding: '3px 8px', borderRadius: 99, background: m.bg, color: m.ink }}>
          {MOODS[status.mood].label}
        </span>
      </button>
    </li>
  )
}
