// Sticker de zona (/z/jardin): registrar el riego de varias plantas de un jalón.
// Todas vienen marcadas; se desmarca la que no se regó.
import { useState } from 'react'
import { logCare } from '../lib/logCare'
import { MOODS, plantStatus, spriteUrl } from '../lib/mood'
import { ACTIONS, ZONES } from '../lib/zones'
import { relativeDay } from '../lib/dates'
import WhenPicker, { resolveWhen } from './WhenPicker'
import { t } from '../lib/theme'

const URGENCY = { sedienta: 0, enferma: 1, con_sed: 2, sin_registro: 3, feliz: 4 }

export default function ZoneSheet({ zone, plants, logs, onBack, onSaved, onOpen, demoSave }) {
  const label = ZONES.find(z => z.id === zone)?.label || zone
  const items = plants.map(p => ({ plant: p, status: plantStatus(p, logs) }))
    .sort((a, b) => URGENCY[a.status.mood] - URGENCY[b.status.mood] || a.plant.id.localeCompare(b.plant.id))
  const [checked, setChecked] = useState(() => new Set(plants.map(p => p.id)))
  const [when, setWhen] = useState({ kind: 'today' })
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')

  const toggle = id => setChecked(s => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n })
  const all = checked.size === plants.length

  async function save() {
    if (!checked.size) return
    setBusy(true); setMsg('')
    const at = resolveWhen(when).toISOString()
    const entries = plants.filter(p => checked.has(p.id)).map(p => ({ plant_id: p.id, action: p.care_action, done_at: at }))
    const { error } = await logCare(entries, demoSave)
    setBusy(false)
    if (error) { setMsg(`No se guardó: ${error.message}`); return }
    setMsg(`Guardado: ${entries.length} ${entries.length === 1 ? 'planta' : 'plantas'}.`); setWhen({ kind: 'today' }); onSaved()
  }

  return (
    <main style={{ maxWidth: 560, margin: '0 auto', padding: '12px 16px 40px', color: t.ink }}>
      <button onClick={onBack} style={{ padding: '8px 12px', fontSize: 14, fontWeight: 700, borderRadius: 12, border: `2px solid ${t.brand}`, background: t.surface, color: t.brand, cursor: 'pointer' }}>← Volver</button>
      <h1 style={{ fontFamily: t.pixelFont, fontSize: 16, color: t.brand, lineHeight: 1.5, margin: '18px 0 4px' }}>{label}</h1>
      <p style={{ margin: 0, color: t.inkMuted }}>Marca las que regaste y guarda una sola vez.</p>

      <button type="button" onClick={() => setChecked(all ? new Set() : new Set(plants.map(p => p.id)))}
        style={{ marginTop: 14, background: 'none', border: 0, padding: 0, color: t.brand, fontWeight: 700, textDecoration: 'underline', cursor: 'pointer' }}>
        {all ? 'Desmarcar todas' : 'Marcar todas'}
      </button>

      <ul style={{ listStyle: 'none', padding: 0, margin: '10px 0 0', display: 'grid', gap: 8 }}>
        {items.map(({ plant, status }) => {
          const m = t.mood[status.mood]
          const id = `chk-${plant.id}`
          return (
            <li key={plant.id} style={{ display: 'flex', alignItems: 'center', gap: 10, border: `2px solid ${checked.has(plant.id) ? t.brand : t.line}`, borderRadius: 12, background: t.surface, padding: '6px 10px' }}>
              <input id={id} type="checkbox" checked={checked.has(plant.id)} onChange={() => toggle(plant.id)} style={{ width: 22, height: 22, accentColor: t.brand }} />
              <img className="pixel" src={spriteUrl(plant.id, status.mood)} alt="" width={40} height={48} />
              <label htmlFor={id} style={{ flex: 1, cursor: 'pointer' }}>
                <span style={{ display: 'block', fontWeight: 600 }}>{plant.nickname || plant.name}</span>
                <span style={{ fontSize: 13, color: t.inkMuted }}>
                  <span style={{ fontWeight: 700, padding: '1px 6px', borderRadius: 99, background: m.bg, color: m.ink }}>{MOODS[status.mood].label}</span>
                  {' · '}{status.lastCare ? `regada ${relativeDay(status.lastCare.done_at)}` : 'sin registro'}
                </span>
              </label>
              <button type="button" onClick={() => onOpen(plant.id)} aria-label={`Abrir ficha de ${plant.nickname || plant.name}`}
                style={{ border: 0, background: 'none', color: t.brand, fontSize: 20, cursor: 'pointer', padding: 6 }}>›</button>
            </li>
          )
        })}
      </ul>

      <WhenPicker when={when} setWhen={setWhen} />
      <button disabled={busy || !checked.size} onClick={save}
        style={{ marginTop: 16, width: '100%', padding: 14, fontSize: 16, fontWeight: 700, borderRadius: 12, border: 0, background: t.brand, color: '#fff', cursor: 'pointer', opacity: checked.size ? 1 : 0.5 }}>
        {ACTIONS.watered} {checked.size} {checked.size === 1 ? 'planta' : 'plantas'}
      </button>
      <p role="status" aria-live="polite" style={{ minHeight: 24, fontWeight: 600 }}>{msg}</p>
    </main>
  )
}
