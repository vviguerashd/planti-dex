import { useEffect, useMemo, useRef, useState } from 'react'
import SCENES from '../lib/scenes.json'
import { MOODS, spriteUrl } from '../lib/mood'
import { t } from '../lib/theme'
import { currentSeason } from '../lib/season'

// Escenarios de la casa con Gala.
// Regla: si alguna planta necesita algo, Gala se pone al acecho junto a la más urgente
// y no se deja acariciar. Si todas están a salvo, duerme y se puede acariciar.
const URGENCY = { sedienta: 0, enferma: 1, con_sed: 2 }
const SCALE = 2
const sceneOf = id => SCENES.find(s => s.plants[id])

export default function Scene({ items, onOpen }) {
  const urgent = useMemo(() => items
    .filter(i => i.status.mood in URGENCY)
    .sort((a, b) => URGENCY[a.status.mood] - URGENCY[b.status.mood] || (a.status.daysLeft ?? 0) - (b.status.daysLeft ?? 0)), [items])
  const safe = urgent.length === 0
  const target = urgent.find(i => sceneOf(i.plant.id))
  const [sceneId, setSceneId] = useState(() => (target && sceneOf(target.plant.id)?.id) || 'sala')
  const scene = SCENES.find(s => s.id === sceneId)
  const byId = useMemo(() => Object.fromEntries(items.map(i => [i.plant.id, i])), [items])
  const scroller = useRef(null)
  const season = currentSeason()
  const bgSrc = `/scenes/${scene.id}${season && scene.seasons?.includes(season) ? `_${season}` : ''}.png`

  // Gala al acecho: al lado de la planta, mirándola
  let gala = null
  if (!safe && target && scene.plants[target.plant.id]) {
    const [px] = scene.plants[target.plant.id]
    const right = px + 40 < scene.w / 2
    const left = Math.max(0, Math.min(scene.w - 86, right ? px + 66 : px - 72))
    gala = { left, top: scene.floor - 54, flip: !right }
  }

  // Centrar la vista en Gala o en la planta urgente
  useEffect(() => {
    const el = scroller.current; if (!el) return
    const focusX = gala ? gala.left + 43 : safe ? scene.sleep[0] + 42 : scene.w / 2
    el.scrollLeft = Math.max(0, focusX * SCALE - el.clientWidth / 2)
  }, [sceneId, gala?.left, safe])

  const [petting, setPetting] = useState(false)
  const [tail, setTail] = useState(1)
  const [hearts, setHearts] = useState([])
  useEffect(() => {
    if (!petting) return
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
    const wag = reduce ? null : setInterval(() => setTail(x => (x + 1) % 4), 140)
    const end = setTimeout(() => setPetting(false), 2600)
    return () => { clearInterval(wag); clearTimeout(end) }
  }, [petting])
  const pet = () => {
    setPetting(true)
    setHearts(h => [...h.slice(-6), ...[0, 1, 2].map(k => ({ key: Date.now() + k, dx: [-14, 10, 30][k], delay: k * 180 }))])
  }

  const targetScene = target && sceneOf(target.plant.id)
  const name = p => p.nickname || p.name
  let message
  if (safe) message = petting ? 'A Gala le encantó.' : 'Todas las plantas están a salvo. Gala se echó a dormir: ya la puedes acariciar.'
  else if (!target) message = `${urgent.length} ${urgent.length === 1 ? 'planta necesita' : 'plantas necesitan'} atención. Gala no se deja acariciar hasta que estén a salvo.`
  else if (targetScene.id === sceneId) message = `Gala encontró algo: ${name(target.plant)} está ${MOODS[target.status.mood].label.toLowerCase()}.`
  else message = `Gala está en ${targetScene.label.toLowerCase()}, junto a ${name(target.plant)}.`
  const tone = safe ? t.mood.feliz : t.mood[target?.status.mood || 'con_sed']

  return (
    <section aria-labelledby="escenario-titulo" style={{ margin: '16px 0 8px' }}>
      <h2 id="escenario-titulo" className="sr-only">Escenarios de la casa</h2>
      <div role="group" aria-label="Escenario" style={{ display: 'flex', gap: 6, overflowX: 'auto', padding: '2px 2px 8px' }}>
        {SCENES.map(s => {
          const on = s.id === sceneId
          const hasGala = !safe && targetScene?.id === s.id
          return (
            <button key={s.id} aria-pressed={on} onClick={() => setSceneId(s.id)}
              style={{ flex: '0 0 auto', border: `2px solid ${t.ink}`, borderRadius: 999, padding: '6px 12px', fontWeight: 700, fontSize: 13, cursor: 'pointer', background: on ? t.brand : t.surface, color: on ? '#fff' : t.ink }}>
              {s.label}{hasGala ? ' 🐾' : ''}
            </button>
          )
        })}
      </div>

      <div ref={scroller} className="scene-scroll" style={{ overflowX: 'auto', borderRadius: 12, border: `3px solid ${t.ink}`, background: t.sceneBg }}>
        <div style={{ position: 'relative', width: scene.w * SCALE, height: scene.h * SCALE }}>
          <img className="pixel" src={bgSrc} alt="" width={scene.w * SCALE} height={scene.h * SCALE} style={{ display: 'block' }} />
          {safe && (
            <button onClick={pet} aria-label="Acariciar a Gala"
              style={{ position: 'absolute', left: (petting ? scene.sleep[0] + 10 : scene.sleep[0]) * SCALE, top: (petting ? scene.floor - 80 : scene.sleep[1]) * SCALE, padding: 0, border: 0, background: 'none', cursor: 'pointer', zIndex: 3 }}>
              <img className="pixel" alt="" src={petting ? `/gala/feliz${[0, 1, 2, 1][tail]}.png` : '/gala/dormida.png'}
                width={(petting ? 66 : 84) * SCALE} height={(petting ? 80 : 46) * SCALE} style={{ display: 'block' }} />
            </button>
          )}
          {hearts.map(h => (
            <span key={h.key} aria-hidden="true" className="heart-up"
              style={{ position: 'absolute', left: (scene.sleep[0] + 30) * SCALE + h.dx, top: (scene.floor - 90) * SCALE, color: t.heart, fontSize: 28, animationDelay: `${h.delay}ms`, opacity: 0, zIndex: 4, pointerEvents: 'none' }}>♥</span>
          ))}
          {Object.entries(scene.plants).map(([id, [x, y]]) => {
            const it = byId[id]; if (!it) return null
            return (
              <button key={id} onClick={() => onOpen(id)} aria-label={`${name(it.plant)}: ${MOODS[it.status.mood].label}`}
                style={{ position: 'absolute', left: x * SCALE, top: y * SCALE, width: 80 * SCALE, height: 96 * SCALE, padding: 0, border: 0, background: 'none', cursor: 'pointer', zIndex: 2 }}>
                <img className="pixel" src={spriteUrl(id, it.status.mood)} alt="" width={80 * SCALE} height={96 * SCALE} style={{ display: 'block' }} />
              </button>
            )
          })}
          {gala && (
            <img className="pixel" src="/gala/acecho.png" alt="" width={86 * SCALE} height={54 * SCALE}
              style={{ position: 'absolute', left: gala.left * SCALE, top: gala.top * SCALE, transform: gala.flip ? 'scaleX(-1)' : 'none', zIndex: 3, pointerEvents: 'none' }} />
          )}
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginTop: 10, padding: '10px 12px', borderRadius: 10, background: tone.bg, color: tone.ink, flexWrap: 'wrap' }}>
        <p role="status" style={{ margin: 0, flex: '1 1 220px', fontSize: 14, fontWeight: 600 }}>{message}</p>
        {!safe && target && targetScene.id !== sceneId && (
          <button onClick={() => setSceneId(targetScene.id)} style={{ border: `2px solid ${tone.ink}`, background: t.surface, color: t.ink, borderRadius: 8, padding: '6px 10px', fontWeight: 700, cursor: 'pointer' }}>Ir con Gala</button>
        )}
        {!safe && target && targetScene.id === sceneId && (
          <button onClick={() => onOpen(target.plant.id)} style={{ border: 0, background: t.brand, color: '#fff', borderRadius: 8, padding: '8px 12px', fontWeight: 700, cursor: 'pointer' }}>Ver {name(target.plant)}</button>
        )}
        {safe && (
          <button onClick={pet} style={{ border: `2px solid ${t.ink}`, background: t.surface, color: t.ink, borderRadius: 8, padding: '6px 10px', fontWeight: 700, cursor: 'pointer' }}>🐾 Acariciar a Gala</button>
        )}
      </div>
    </section>
  )
}
