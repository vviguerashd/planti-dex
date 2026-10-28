import { useState } from 'react'
import { supabase } from '../lib/supabase'
import { t } from '../lib/theme'

// Email + contraseña (no magic link): la app se instala en el celular y un link
// por correo abriría Safari, no la app instalada. Mismo criterio que DuoFit.
export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  async function submit(e) {
    e.preventDefault(); setBusy(true); setError(null)
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) setError('Correo o contraseña incorrectos.')
    setBusy(false)
  }
  const field = { display: 'block', width: '100%', padding: '12px 14px', fontSize: 16, border: `2px solid ${t.line}`, borderRadius: 10, background: t.surface, color: t.ink, marginTop: 6 }
  return (
    <main style={{ padding: 24, maxWidth: 420, margin: '10vh auto 0', color: t.ink }}>
      <h1 style={{ fontFamily: t.pixelFont, fontSize: 20, lineHeight: 1.4, color: t.brand }}>Planti-dex</h1>
      <form onSubmit={submit} noValidate>
        <label style={{ display: 'block', marginTop: 20, fontWeight: 600 }}>Correo
          <input type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} style={field} />
        </label>
        <label style={{ display: 'block', marginTop: 16, fontWeight: 600 }}>Contraseña
          <input type="password" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} style={field} />
        </label>
        {error && <p role="alert" style={{ color: '#7a1c14', fontWeight: 600 }}>{error}</p>}
        <button type="submit" disabled={busy} style={{ marginTop: 20, width: '100%', padding: 14, fontSize: 16, fontWeight: 700, borderRadius: 10, border: 0, background: t.brand, color: '#fff' }}>
          {busy ? 'Entrando…' : 'Entrar'}
        </button>
      </form>
    </main>
  )
}
