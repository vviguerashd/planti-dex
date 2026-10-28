import { useCallback, useEffect, useState } from 'react'
import { supabase, supabaseConfigured } from './lib/supabase'
import { useAuth } from './lib/useAuth'
import Login from './components/Login'
import Home from './components/Home'
import PlantSheet from './components/PlantSheet'
import { t } from './lib/theme'
import { demo } from './lib/demo'

// Rutas mínimas sin router: "/" y "/p/P07". La segunda es la que abre un sticker NFC.
function plantIdFromPath() {
  const m = window.location.pathname.match(/^\/p\/(P\d{2,3})\/?$/i)
  return m ? m[1].toUpperCase() : null
}

export default function App() {
  const session = useAuth()
  const [plants, setPlants] = useState([])
  const [logs, setLogs] = useState([])
  const [members, setMembers] = useState({})
  const [error, setError] = useState(null)
  const [openId, setOpenId] = useState(plantIdFromPath())

  const load = useCallback(async () => {
    const [p, l, m] = await Promise.all([
      supabase.from('plants').select('*').eq('active', true).order('id'),
      supabase.from('care_log').select('*').order('done_at', { ascending: false }).limit(2000),
      supabase.from('household_members').select('*'),
    ])
    const err = p.error || l.error || m.error
    if (err) { setError(err.message); return }
    setPlants(p.data); setLogs(l.data)
    setMembers(Object.fromEntries(m.data.map(x => [x.user_id, x.display_name])))
  }, [])

  useEffect(() => { if (session) load() }, [session, load])
  useEffect(() => {
    const onPop = () => setOpenId(plantIdFromPath())
    window.addEventListener('popstate', onPop)
    return () => window.removeEventListener('popstate', onPop)
  }, [])

  const openPlant = id => { window.history.pushState({}, '', `/p/${id}`); setOpenId(id) }
  const closePlant = () => { window.history.pushState({}, '', '/'); setOpenId(null) }

  if (!supabaseConfigured) return <Demo openId={openId} openPlant={openPlant} closePlant={closePlant} />
  if (session === undefined) return null
  if (!session) return <Login />
  if (error) return <Notice>No pude leer los datos: {error}. ¿Tu cuenta ya está en household_members?</Notice>

  const plant = plants.find(p => p.id === openId)
  return plant
    ? <PlantSheet plant={plant} logs={logs} members={members} onBack={closePlant} onSaved={load} />
    : <Home plants={plants} logs={logs} onOpen={openPlant} />
}

function Notice({ children }) {
  return <main style={{ padding: 24, maxWidth: 520, margin: '0 auto', color: t.ink, lineHeight: 1.5 }}><p>{children}</p></main>
}

// Sin Supabase: mismas pantallas con datos de ejemplo en memoria.
function Demo({ openId, openPlant, closePlant }) {
  const [logs, setLogs] = useState(demo.logs)
  const plant = demo.plants.find(p => p.id === openId)
  const fakeSave = entry => setLogs(l => [{ id: 'n' + l.length, done_at: new Date().toISOString(), done_by: 'demo-vic', note: null, ...entry }, ...l])
  return (
    <>
      <p style={{ margin: 0, padding: '6px 16px', background: '#fdebb3', color: '#5c3d00', fontSize: 13, fontWeight: 600 }}>Modo demo: datos de ejemplo, nada se guarda.</p>
      {plant
        ? <PlantSheet plant={plant} logs={logs} members={demo.members} onBack={closePlant} demoSave={fakeSave} />
        : <Home plants={demo.plants} logs={logs} onOpen={openPlant} />}
    </>
  )
}
