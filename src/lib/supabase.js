import { createClient } from '@supabase/supabase-js'

// Ambas variables son públicas por diseño (terminan en el bundle).
// La seguridad la da RLS: sin sesión de un miembro de la casa no se lee ni se escribe nada.
const url = import.meta.env.VITE_SUPABASE_URL
const key = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabaseConfigured = Boolean(url && key)
export const supabase = supabaseConfigured ? createClient(url, key) : null
