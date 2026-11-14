// Carrusel de tips de lombricomposta. Abre en el "tip de la semana" y se desliza a los demás.
import { useEffect, useRef, useState } from 'react'
import { COMPOST_TIPS, weekIndex } from '../lib/compostTips'
import { t } from '../lib/theme'

const CAT = { comida: 'Comida', cama: 'Cama', humedad: 'Humedad', liquido: 'Líquido', lombrices: 'Lombrices', cosecha: 'Cosecha' }

function Mini({ cat }) {
  const c = t.compost
  const worm = <path d="M22 54 q6 -6 12 0 t12 0" stroke={c.worm} strokeWidth="3" fill="none" strokeLinecap="round" />
  const art = {
    comida: <><rect x="8" y="40" width="64" height="26" fill={c.soil} /><rect x="22" y="34" width="20" height="10" rx="2" fill={c.food} /><rect x="44" y="36" width="12" height="8" rx="2" fill={c.food} />{worm}</>,
    cama: <><rect x="8" y="44" width="64" height="22" fill={c.soil} /><rect x="8" y="34" width="64" height="10" fill={c.bed} /><path d="M14 30 l10 -8 l6 8 M40 30 l8 -10 l8 10" stroke={c.bed} strokeWidth="4" fill="none" /></>,
    humedad: <><rect x="8" y="44" width="64" height="22" fill={c.soil} /><path d="M40 10 C30 24 30 32 40 34 C50 32 50 24 40 10 Z" fill={c.water} /></>,
    liquido: <><path d="M14 14 h52 l-4 22 h-44 Z" fill="none" stroke={c.line} strokeWidth="3" /><path d="M14 40 h52 l-4 26 h-44 Z" fill="none" stroke={c.line} strokeWidth="3" /><rect x="19" y="56" width="42" height="9" fill={c.water} /><rect x="17" y="20" width="46" height="14" fill={c.soil} /></>,
    lombrices: <><rect x="8" y="40" width="64" height="26" fill={c.soil} />{worm}<path d="M30 46 q6 -6 12 0" stroke={c.worm} strokeWidth="3" fill="none" strokeLinecap="round" /></>,
    cosecha: <><path d="M10 64 L40 20 L70 64 Z" fill={c.soil} /><circle cx="64" cy="14" r="7" fill={c.sun} />{worm}</>,
  }[cat]
  return <svg viewBox="0 0 80 72" width="80" height="72" aria-hidden="true" className="pixel" style={{ flex: '0 0 auto' }}>{art}</svg>
}

export default function CompostTips() {
  const start = weekIndex() % COMPOST_TIPS.length
  const [i, setI] = useState(start)
  const track = useRef(null)
  const go = n => {
    const k = (n + COMPOST_TIPS.length) % COMPOST_TIPS.length
    setI(k)
    const el = track.current?.children[k]
    el?.scrollIntoView({ behavior: window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', inline: 'start', block: 'nearest' })
  }
  useEffect(() => { const el = track.current?.children[start]; if (el) track.current.scrollLeft = el.offsetLeft - track.current.offsetLeft }, [start])
  const onScroll = () => {
    const el = track.current; if (!el) return
    const k = Math.round(el.scrollLeft / (el.firstChild?.offsetWidth + 12 || 1))
    if (k !== i && k >= 0 && k < COMPOST_TIPS.length) setI(k)
  }
  const navBtn = { border: `2px solid ${t.brand}`, background: t.surface, color: t.brand, borderRadius: 8, padding: '6px 12px', fontWeight: 700, cursor: 'pointer' }

  return (
    <section aria-labelledby="tips-titulo" style={{ marginTop: 20 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
        <h2 id="tips-titulo" style={{ margin: 0, fontSize: 15, color: t.brand }}>Tips de lombricomposta</h2>
        <span style={{ fontSize: 13, color: t.inkMuted }}>{i + 1} de {COMPOST_TIPS.length}</span>
      </div>
      <div ref={track} onScroll={onScroll} role="list" aria-label="Tips" tabIndex={0}
        style={{ display: 'flex', gap: 12, overflowX: 'auto', scrollSnapType: 'x mandatory', padding: '10px 2px 12px' }}>
        {COMPOST_TIPS.map((tip, k) => (
          <article key={k} role="listitem" aria-roledescription="tarjeta" aria-label={`${k + 1} de ${COMPOST_TIPS.length}: ${tip.title}`}
            style={{ flex: '0 0 86%', scrollSnapAlign: 'start', background: t.surface, border: `2px solid ${k === start ? t.brand : t.line}`, borderRadius: 14, padding: 14, display: 'grid', gap: 8 }}>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              <Mini cat={tip.cat} />
              <div style={{ display: 'grid', gap: 4 }}>
                <span style={{ fontSize: 12, fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase', color: t.inkMuted }}>{CAT[tip.cat]}{k === start ? ' · tip de la semana' : ''}</span>
                <h3 style={{ margin: 0, fontSize: 16, lineHeight: 1.3, color: t.ink }}>{tip.title}</h3>
              </div>
            </div>
            <p style={{ margin: 0, fontSize: 15, lineHeight: 1.5, color: t.ink }}>{tip.body}</p>
          </article>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={() => go(i - 1)} style={navBtn} aria-label="Tip anterior">← Anterior</button>
        <button onClick={() => go(i + 1)} style={navBtn} aria-label="Siguiente tip">Siguiente →</button>
      </div>
    </section>
  )
}
