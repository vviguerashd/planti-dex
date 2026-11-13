// Alertas de clima para el jardín (helada y tormenta con posible granizo).
// Corre con Vercel Cron a la 1 pm y a las 6 pm (hora de Pachuca) y SOLO manda correo si hay riesgo.
//
// Variables de entorno (Vercel → Settings → Environment Variables, solo servidor, nunca VITE_):
//   CRON_SECRET               Vercel la manda como "Authorization: Bearer ..." en cada ejecución.
//   RESEND_API_KEY            llave de Resend para mandar el correo.
//   ALERT_EMAIL               a quién le llega (no se guarda en el repo).
//   SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY   para leer qué plantas son sensibles al frío.
//   ALERT_FORCE=1             (opcional, temporal) manda el correo aunque no haya riesgo, para probar.

const LAT = 20.10, LON = -98.76              // Pachuca, nivel ciudad (no la dirección de la casa)
const FROST_C = 4                             // con cielo despejado hay escarcha aunque el aire marque 3–4 °C
const STORM_CODES = new Set([95, 96, 99])     // tormenta eléctrica; 96/99 = con granizo según el modelo
const FALLBACK = [                            // por si no hay acceso a la base
  { id: 'P04', name: 'Bugambilia roja (bolsa)' }, { id: 'P18', name: 'Bugambilia grande (morada)' }, { id: 'P24', name: 'Bugambilia naranja (bolsa)' },
]

export default async function handler(req, res) {
  if (!process.env.CRON_SECRET || req.headers.authorization !== `Bearer ${process.env.CRON_SECRET}`) {
    return res.status(401).json({ error: 'no autorizado' })
  }
  try {
    const forecast = await getForecast()
    const risk = assess(forecast)
    const force = process.env.ALERT_FORCE === '1'
    if (!risk.frost && !risk.storm && !force) return res.status(200).json({ sent: false, ...risk })

    const plants = await getSensitivePlants()
    const { subject, html, text } = buildEmail(risk, plants, force)
    await sendEmail(subject, html, text)
    return res.status(200).json({ sent: true, ...risk })
  } catch (e) {
    console.error(e)
    return res.status(500).json({ error: String(e.message || e) })
  }
}

async function getForecast() {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${LAT}&longitude=${LON}` +
    `&hourly=temperature_2m,weather_code&timezone=America%2FMexico_City&forecast_days=2`
  const r = await fetch(url)
  if (!r.ok) throw new Error(`Open-Meteo respondió ${r.status}`)
  return r.json()
}

// Ventana: desde ahora hasta las 10 am de mañana (hora local) para helada; próximas 24 h para tormenta.
export function assess(f, now = new Date()) {
  const local = new Date(now.toLocaleString('en-US', { timeZone: 'America/Mexico_City' }))
  const pad = n => String(n).padStart(2, '0')
  const key = d => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:00`
  const startKey = key(local)
  const tomorrow = new Date(local); tomorrow.setDate(tomorrow.getDate() + 1); tomorrow.setHours(10, 0, 0, 0)
  const frostEnd = key(tomorrow)
  const in24 = new Date(local); in24.setHours(in24.getHours() + 24)
  const stormEnd = key(in24)
  const { time, temperature_2m: temp, weather_code: code } = f.hourly
  let min = Infinity, minAt = null, storm = null
  time.forEach((t, i) => {
    if (t >= startKey && t <= frostEnd && temp[i] < min) { min = temp[i]; minAt = t }
    if (t >= startKey && t <= stormEnd && STORM_CODES.has(code[i]) && !storm) storm = { at: t, hail: code[i] !== 95 }
  })
  return { minTemp: Number.isFinite(min) ? Math.round(min * 10) / 10 : null, minAt, frost: min <= FROST_C, storm }
}

async function getSensitivePlants() {
  const url = process.env.SUPABASE_URL || process.env.VITE_SUPABASE_URL
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY
  if (!url || !key) return FALLBACK
  const r = await fetch(`${url}/rest/v1/plants?select=id,name,nickname&frost_sensitive=eq.true&active=eq.true&order=id`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
  })
  if (!r.ok) return FALLBACK
  const rows = await r.json()
  return rows.length ? rows.map(p => ({ id: p.id, name: p.nickname || p.name })) : FALLBACK
}

const hour = t => t ? `${Number(t.slice(11, 13)) % 12 || 12}:00 ${Number(t.slice(11, 13)) < 12 ? 'am' : 'pm'}` : ''

export function buildEmail(risk, plants, force) {
  const parts = [], lines = []
  if (risk.frost) {
    parts.push(`❄️ Puede helar (${risk.minTemp} °C)`)
    lines.push(`Esta noche Pachuca puede bajar a ${risk.minTemp} °C hacia las ${hour(risk.minAt)}. Con cielo despejado puede haber escarcha aunque no llegue a 0 °C.`)
    lines.push(`Tapa o mete: ${plants.map(p => p.name).join(', ')}.`)
  }
  if (risk.storm) {
    parts.push(risk.storm.hail ? '⛈️ Tormenta con posible granizo' : '⛈️ Tormenta eléctrica')
    lines.push(`El pronóstico marca tormenta eléctrica hacia las ${hour(risk.storm.at)}${risk.storm.hail ? ', con posible granizo' : ''}. El granizo no se puede asegurar con anticipación: si ves que se carga el cielo, mete o cubre las macetas que puedas.`)
  }
  if (force && !parts.length) {
    parts.push('✅ Prueba de alertas')
    lines.push(`Correo de prueba: hoy no hay riesgo. Mínima prevista: ${risk.minTemp ?? '—'} °C. Plantas que se avisarían en helada: ${plants.map(p => p.name).join(', ')}.`)
  }
  const subject = `Planti-dex · ${parts.join(' · ')}`
  const text = lines.join('\n\n') + '\n\nPronóstico: Open-Meteo para Pachuca. planti-dex.vercel.app'
  const html = `<div style="font-family:system-ui,sans-serif;font-size:16px;line-height:1.5;color:#1c241e">` +
    lines.map(l => `<p>${l}</p>`).join('') +
    `<p style="font-size:13px;color:#4a554c">Pronóstico: Open-Meteo para Pachuca. <a href="https://planti-dex.vercel.app">Abrir Planti-dex</a></p></div>`
  return { subject, html, text }
}

async function sendEmail(subject, html, text) {
  if (!process.env.RESEND_API_KEY || !process.env.ALERT_EMAIL) throw new Error('Faltan RESEND_API_KEY o ALERT_EMAIL')
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: 'Planti-dex <onboarding@resend.dev>', to: [process.env.ALERT_EMAIL], subject, html, text }),
  })
  if (!r.ok) throw new Error(`Resend respondió ${r.status}: ${await r.text()}`)
}
