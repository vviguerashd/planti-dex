import { useId } from 'react'
import { t } from '../lib/theme'

// "¿Cuándo fue?" Hoy (ahora), Ayer (misma hora) u otra fecha (a mediodía local).
export function resolveWhen(when) {
  const now = new Date()
  if (when.kind === 'today') return now
  if (when.kind === 'yesterday') { const d = new Date(now); d.setDate(d.getDate() - 1); return d }
  const [y, m, d] = when.date.split('-').map(Number)
  return new Date(y, m - 1, d, 12, 0, 0)            // fecha local, nunca new Date('YYYY-MM-DD')
}
function localISODate(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export default function WhenPicker({ when, setWhen }) {
  const id = useId()
  const today = localISODate(new Date())
  const opt = (kind, label) => (
    <button type="button" aria-pressed={when.kind === kind} onClick={() => setWhen(kind === 'other' ? { kind, date: when.date || today } : { kind })}
      style={{ flex: 1, padding: 10, borderRadius: 10, fontWeight: 600, cursor: 'pointer', color: t.ink,
        border: `2px solid ${when.kind === kind ? t.brand : t.line}`, background: when.kind === kind ? t.selected : t.surface }}>
      {label}
    </button>
  )
  return (
    <fieldset style={{ border: 0, padding: 0, margin: '16px 0 0' }}>
      <legend style={{ fontWeight: 700, marginBottom: 8 }}>¿Cuándo fue?</legend>
      <div style={{ display: 'flex', gap: 8 }}>{opt('today', 'Hoy')}{opt('yesterday', 'Ayer')}{opt('other', 'Otro día')}</div>
      {when.kind === 'other' && (
        <label htmlFor={id} style={{ display: 'block', marginTop: 10, fontWeight: 600 }}>Fecha
          <input id={id} type="date" max={today} value={when.date} onChange={e => setWhen({ kind: 'other', date: e.target.value })}
            style={{ display: 'block', marginTop: 6, padding: 10, fontSize: 16, borderRadius: 10, border: `2px solid ${t.line}`, background: t.surface, color: t.ink }} />
        </label>
      )}
    </fieldset>
  )
}
