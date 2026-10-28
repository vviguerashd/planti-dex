import { useEffect, useState } from 'react'
import { supabase } from './supabase'

// undefined = cargando · null = sin sesión · objeto = sesión
export function useAuth() {
  const [session, setSession] = useState(undefined)
  useEffect(() => {
    if (!supabase) { setSession(null); return }
    supabase.auth.getSession().then(({ data }) => setSession(data.session ?? null))
    const { data: sub } = supabase.auth.onAuthStateChange((_e, s) => setSession(s ?? null))
    return () => sub.subscription.unsubscribe()
  }, [])
  return session
}
