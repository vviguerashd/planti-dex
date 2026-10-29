import { supabase } from './supabase'

// Inserta uno o varios cuidados. En modo demo los guarda en memoria.
export async function logCare(entries, demoSave) {
  if (demoSave) { demoSave(entries); return { error: null } }
  return supabase.from('care_log').insert(entries)
}
