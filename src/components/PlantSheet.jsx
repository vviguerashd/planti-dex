// Ficha provisional de una planta. Se reemplaza por la tarjeta tipo Pokédex cuando Vic apruebe el diseño.
import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { MOODS, plantStatus, spriteUrl } from '../lib/mood'
import { ACTIONS, CONDITIONS, ZONES } from '../lib/zones'
import { relativeDay, shortDate } from '../lib/dates'
import { t } from '../lib/theme'

export default function PlantSheet({ plant, logs, members, onBack, onSaved, demoSave }) {
  const status = plantStatus(plant, logs)
  const history = logs.filter(l => l.plant_id === plant.id).slice(0, 6)
  const [condition, setCondition] = useState(null)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const m = t.mood[status.mood]

  async function log(action) {
    setBusy(true); setMsg('')
    if (demoSave) { demoSave({ plant_id: plant.id, action, condition }); setBusy(false); setMsg(`Guardado (demo): ${ACTIONS[action]}.`); setCondition(null); return }
    const { error } = await supabase.from('care_log').insert({ plant_id: plant.id, action, condition })
    setBusy(false)
    if (error) { setMsg(`No se guardó: ${error.message}`); return }
    setMsg(`Guardado: ${ACTIONS[action]}.`); setCondition(null); onSaved()
  }

  const btn = (primary) => ({ padding: '14px 12px', fontSize: 16, fontWeight: 700, borderRadius: 12, cursor: 'pointer',
    border: primary ? 0 : `2px solid ${t.brand}`, background: primary ? t.brand : t.surface, color: primary ? '#fff' : t.brand })

  return (
    <main style={{ maxWidth: 520, margin: '0 auto', padding: '12px 16px 40px', color: t.ink }}>
      <button onClick={onBack} style={{ ...btn(false), padding: '8px 12px', fontSize: 14 }}>← Volver</button>
      <div style={{ textAlign: 'center', marginTop: 12 }}>
        <img className="pixel" src={spriteUrl(plant.id, status.mood)} alt="" width={200} height={240} />
        <p style={{ margin: 0, fontFamily: t.pixelFont, fontSize: 11, color: t.inkMuted }}>#{plant.id}</p>
        <h1 style={{ fontSize: 22, margin: '6px 0 2px' }}>{plant.nickname || plant.name}</h1>
        <p style={{ margin: 0, color: t.inkMuted, fontStyle: 'italic' }}>{plant.species}</p>
        <p style={{ margin: '10px 0 0' }}>
          <span style={{ fontWeight: 700, padding: '4px 10px', borderRadius: 99, background: m.bg, color: m.ink }}>{MOODS[status.mood].label}</span>
          <span style={{ marginLeft: 8, color: t.inkMuted }}>{ZONES.find(z => z.id === plant.zone)?.label}</span>
        </p>
      </div>
      <dl style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '6px 12px', marginTop: 20 }}>
        <dt style={{ fontWeight: 600 }}>Último {plant.care_action === 'water_changed' ? 'cambio de agua' : 'riego'}</dt>
        <dd style={{ margin: 0 }}>{status.lastCare ? `${relativeDay(status.lastCare.done_at)} · ${members[status.lastCare.done_by] || '—'}` : 'Sin registro'}</dd>
        <dt style={{ fontWeight: 600 }}>Próximo</dt>
        <dd style={{ margin: 0 }}>{status.next ? shortDate(status.next) : '—'}</dd>
        <dt style={{ fontWeight: 600 }}>Cada</dt>
        <dd style={{ margin: 0 }}>{plant.water_interval_days} días</dd>
      </dl>

      <fieldset style={{ border: 0, padding: 0, margin: '20px 0 0' }}>
        <legend style={{ fontWeight: 700, marginBottom: 8 }}>¿Cómo se ve? <span style={{ fontWeight: 400, color: t.inkMuted }}>(opcional)</span></legend>
        <div style={{ display: 'flex', gap: 8 }}>
          {CONDITIONS.map(c => (
            <button key={c.id} aria-pressed={condition === c.id} onClick={() => setCondition(condition === c.id ? null : c.id)}
              style={{ flex: 1, padding: 10, borderRadius: 10, fontWeight: 600, cursor: 'pointer',
                border: `2px solid ${condition === c.id ? t.brand : t.line}`, background: condition === c.id ? '#e3eee2' : t.surface, color: t.ink }}>
              {c.label}
            </button>
          ))}
        </div>
      </fieldset>

      <div style={{ display: 'grid', gap: 10, marginTop: 16 }}>
        <button disabled={busy} onClick={() => log(plant.care_action)} style={btn(true)}>{ACTIONS[plant.care_action]}</button>
        <button disabled={busy} onClick={() => log('checked_ok')} style={btn(false)}>{ACTIONS.checked_ok}</button>
      </div>
      <p role="status" aria-live="polite" style={{ minHeight: 24, fontWeight: 600 }}>{msg}</p>

      {history.length > 0 && (
        <section aria-labelledby="hist">
          <h2 id="hist" style={{ fontSize: 16 }}>Últimos cuidados</h2>
          <ul style={{ paddingLeft: 18, lineHeight: 1.6 }}>
            {history.map(h => (
              <li key={h.id}>{shortDate(h.done_at)} · {ACTIONS[h.action]}{h.condition ? ` · se veía ${h.condition}` : ''} · {members[h.done_by] || '—'}</li>
            ))}
          </ul>
        </section>
      )}
      {plant.notes && <p style={{ color: t.inkMuted, marginTop: 16 }}>{plant.notes}</p>}
      {plant.toxic_pets && <p style={{ color: t.inkMuted }}>⚠️ {plant.toxic_pets === 'si' ? 'Tóxica' : 'Irritante'} para perros y gatos.</p>}
    </main>
  )
}
