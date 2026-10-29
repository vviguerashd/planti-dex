import { useCallback, useEffect, useState } from 'react'
import { supabase, supabaseConfigured } from './lib/supabase'
import { useAuth } from './lib/useAuth'
import { readCache, writeCache, clearCache } from './lib/cache'
import { parseRoute, go } from './lib/route'
import Login from './components/Login'
import Home from './components/Home'
import PlantSheet from './components/PlantSheet'
import ZoneSheet from './components/ZoneSheet'
import Loading from './components/Loading'
import { t } from './lib/theme'
import { demo } from './lib/demo'

export default function App() {
  const session = useAuth()
  const cached = readCache()
  const [data, setData] = useState(cached)        // { plants, logs, members } o null
  const [error, setError] = useState(null)
  const [route, setRoute] = useState(parseRoute())

  const load = useCallback(async () => {
    const [p, l, m] = await Promise.all([
      supabase.from('plants').select('*').eq('active', true).order('id'),
      supabase.from('care_log').select('*').order('done_at', { ascending: false }).limit(2000),
      supabase.from('household_members').select('*'),
    ])
    const err = p.error || l.error || m.error
    if (err) { setError(err.message); return }
    const fresh = { plants: p.data, logs: l.data, members: Object.fromEntries(m.data.map(x => [x.user_id, x.display_name])) }
    setData(fresh); writeCache(fresh); setError(null)
  }, [])

  useEffect(() => { if (session) load() }, [session, load])
  useEffect(() => { if (session === null) { clearCache(); setData(null) } }, [session])
  useEffect(() => {
    const onPop = () => setRoute(parseRoute())
    window.addEventListener('popstate', onPop)
    return () => window.removeEventListener('popstate', onPop)
  }, [])

  const nav = path => { go(path); setRoute(parseRoute()); window.scrollTo(0, 0) }

  if (!supabaseConfigured) return <Demo route={route} nav={nav} />
  if (session === undefined) return <Loading />
  if (!session) return <Login />
  if (error && !data) return <Notice>No pude leer los datos: {error}. ¿Tu cuenta ya está en household_members?</Notice>
  if (!data) return <Loading />

  return <Screen route={route} nav={nav} {...data} onSaved={load} />
}

function Screen({ route, nav, plants, logs, members, onSaved, demoSave }) {
  const common = { logs, members, onSaved, demoSave, onBack: () => nav('/') }
  if (route.kind === 'plant') {
    const plant = plants.find(p => p.id === route.id)
    if (plant) return <PlantSheet plant={plant} {...common} />
  }
  if (route.kind === 'zone') {
    const inZone = plants.filter(p => p.zone === route.id)
    if (inZone.length) return <ZoneSheet zone={route.id} plants={inZone} {...common} onOpen={id => nav(`/p/${id}`)} />
  }
  return <Home plants={plants} logs={logs} onOpen={id => nav(`/p/${id}`)} onOpenZone={z => nav(`/z/${z}`)} />
}

function Notice({ children }) {
  return <main style={{ padding: 24, maxWidth: 520, margin: '0 auto', color: t.ink, lineHeight: 1.5 }}><p>{children}</p></main>
}

// Sin Supabase: mismas pantallas con datos de ejemplo en memoria.
function Demo({ route, nav }) {
  const [logs, setLogs] = useState(demo.logs)
  const demoSave = entries => setLogs(l => [...entries.map((e, i) => ({ id: 'n' + l.length + i, done_by: 'demo-vic', note: null, ...e })), ...l])
  return (
    <>
      <p style={{ margin: 0, padding: '6px 16px', background: '#fdebb3', color: '#5c3d00', fontSize: 13, fontWeight: 600 }}>Modo demo: datos de ejemplo, nada se guarda.</p>
      <Screen route={route} nav={nav} plants={demo.plants} logs={logs} members={demo.members} onSaved={() => {}} demoSave={demoSave} />
    </>
  )
}
