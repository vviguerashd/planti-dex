// Ficha de un depósito de lombricomposta (/l/L1). Solo Vic las atiende, pero cualquiera de la casa puede registrar.
import { useState } from 'react'
import { supabase } from '../lib/supabase'
import WhenPicker, { resolveWhen } from './WhenPicker'
import { COMPOST_ACTIONS, COMPOST_MOOD_LABEL, compostStatus, HARVEST_DAYS } from '../lib/compost'
import { relativeDay, shortDate } from '../lib/dates'
import { t } from '../lib/theme'
import CompostTips from './CompostTips'

export default function CompostSheet({ bin, compostLogs, members, onBack, onSaved, demoSave }) {
  const s = compostStatus(bin, compostLogs)
  const history = compostLogs.filter(l => l.bin_id === bin.id).slice(0, 8)
  const [when, setWhen] = useState({ kind: 'today' })
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const m = t.mood[s.mood]

  async function log(action) {
    setBusy(true); setMsg('')
    const entry = { bin_id: bin.id, action, done_at: resolveWhen(when).toISOString() }
    let error = null
    if (demoSave) demoSave([entry], 'compost')
    else ({ error } = await supabase.from('compost_log').insert([entry]))
    setBusy(false)
    if (error) { setMsg(`No se guardó: ${error.message}`); return }
    setMsg(`Guardado: ${COMPOST_ACTIONS[action]}.`); setWhen({ kind: 'today' }); onSaved()
  }

  const btn = primary => ({ padding: '12px', fontSize: 15, fontWeight: 700, borderRadius: 12, cursor: 'pointer',
    border: primary ? 0 : `2px solid ${t.brand}`, background: primary ? t.brand : t.surface, color: primary ? '#fff' : t.brand })
  const sub = { margin: '20px 0 8px', fontSize: 15, color: t.brand }

  return (
    <main style={{ maxWidth: 520, margin: '0 auto', padding: '12px 16px 40px', color: t.ink }}>
      <button onClick={onBack} style={{ ...btn(false), padding: '8px 12px', fontSize: 14 }}>← Volver</button>
      <p style={{ margin: '16px 0 0', fontFamily: t.pixelFont, fontSize: 11, color: t.inkMuted }}>#{bin.id} · Patio trasero</p>
      <h1 style={{ fontSize: 22, margin: '6px 0 4px' }}>{bin.name}</h1>
      <p style={{ margin: 0, color: t.inkMuted }}>{bin.notes}</p>
      <p style={{ margin: '12px 0 0' }}>
        <span style={{ fontWeight: 700, padding: '4px 10px', borderRadius: 99, background: m.bg, color: m.ink }}>{COMPOST_MOOD_LABEL[s.mood]}</span>
      </p>
      <dl style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '6px 12px', margin: '14px 0 0' }}>
        <dt style={{ color: t.inkMuted }}>Última comida</dt><dd style={{ margin: 0 }}>{s.lastFeed ? relativeDay(s.lastFeed.done_at) : 'sin registro'}</dd>
        <dt style={{ color: t.inkMuted }}>Humedad</dt><dd style={{ margin: 0 }}>{s.lastMoist ? `${COMPOST_ACTIONS[s.lastMoist.action]} · ${relativeDay(s.lastMoist.done_at)}` : 'sin revisar'}</dd>
        <dt style={{ color: t.inkMuted }}>Última cosecha</dt><dd style={{ margin: 0 }}>{s.lastHarvest ? `${shortDate(s.lastHarvest.done_at)} (${relativeDay(s.lastHarvest.done_at)})` : 'sin registro'}</dd>
      </dl>
      {s.harvestDue && (
        <p style={{ margin: '12px 0 0', padding: '10px 12px', borderRadius: 10, background: t.mood.con_sed.bg, color: t.mood.con_sed.ink, fontWeight: 600 }}>
          Ya pasaron más de {Math.round(HARVEST_DAYS / 30)} meses desde la última cosecha. Si casi todo es tierra negra y ya no reconoces la comida, toca cosechar.
        </p>
      )}

      <CompostTips />

      <h2 style={sub}>Rutina del sábado</h2>
      <ol style={{ margin: 0, paddingLeft: 20, lineHeight: 1.5, color: t.ink }}>
        <li>Revisa si quedó comida de la semana pasada: si queda mucha, da menos.</li>
        <li>Restos picados y descongelados (escúrrelos), enterrados en una esquina distinta.</li>
        <li>Encima, un puñado de hojas secas o cartón.</li>
        <li>Prueba del puño: unas gotas, como esponja exprimida.</li>
        {bin.id === 'L1' && <li>Vacía la cubeta de abajo si tiene líquido.</li>}
      </ol>

      <WhenPicker when={when} setWhen={setWhen} />

      <div style={{ display: 'grid', gap: 10, marginTop: 14 }}>
        <button disabled={busy} onClick={() => log('feed')} style={btn(true)}>{COMPOST_ACTIONS.feed}</button>
        <button disabled={busy} onClick={() => log('bedding')} style={btn(false)}>{COMPOST_ACTIONS.bedding}</button>
      </div>
      <p style={{ margin: '14px 0 6px', fontWeight: 700 }}>Humedad</p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
        <button disabled={busy} onClick={() => log('moisture_ok')} style={{ ...btn(false), fontSize: 14 }}>Bien</button>
        <button disabled={busy} onClick={() => log('moisture_dry')} style={{ ...btn(false), fontSize: 14 }}>Seca</button>
        <button disabled={busy} onClick={() => log('moisture_wet')} style={{ ...btn(false), fontSize: 14 }}>Encharcada</button>
      </div>
      <div style={{ display: 'grid', gap: 10, marginTop: 14 }}>
        {bin.id === 'L1' && <button disabled={busy} onClick={() => log('drained')} style={btn(false)}>{COMPOST_ACTIONS.drained}</button>}
        <button disabled={busy} onClick={() => log('harvest')} style={btn(false)}>{COMPOST_ACTIONS.harvest}</button>
      </div>
      <p role="status" style={{ minHeight: 24, margin: '12px 0 0', fontWeight: 600 }}>{msg}</p>

      {history.length > 0 && (<>
        <h2 style={sub}>Historial</h2>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'grid', gap: 6 }}>
          {history.map(h => (
            <li key={h.id} style={{ color: t.ink }}>{shortDate(h.done_at)} · {COMPOST_ACTIONS[h.action]}{members?.[h.done_by] ? ` · ${members[h.done_by]}` : ''}</li>
          ))}
        </ul>
      </>)}
    </main>
  )
}
