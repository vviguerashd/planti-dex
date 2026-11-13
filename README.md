# Planti-dex 🌱

Las plantas de la casa de Vic y Fer como tamagotchis. Cada planta tiene un sprite kawaii 16-bit
con cuatro estados de ánimo (feliz, con sed, sedienta, enferma) que cambian según los cuidados
que registran. Objetivo: que ninguna se olvide y propagar más plantas. No es competencia.

## Cómo está armada

Misma arquitectura que DuoFit:

| Capa | Tech |
|------|------|
| Frontend | React 18 + Vite, estilos inline con tokens de `src/lib/theme.js` |
| Datos | Supabase (Postgres + RLS) |
| Deploy | Vercel, automático en cada push a `main` |
| Sprites | PNG 80×96 en `public/sprites/`, generados por código en `tools/sprites/` |

**Sin Supabase configurado la app corre en modo demo** (27 plantas y registros inventados en memoria).

Rutas: `/` (escenarios y zonas), `/p/P07` (ficha de una planta), `/z/jardin` (regar varias de una zona)
y `/lluvia` (marcar las plantas que se mojaron con la lluvia).
Los stickers NFC abren `/p/…` en plantas de maceta y `/z/…` en zonas que se riegan juntas, como el jardín.
Stickers grabados: `/z/jardin` (junto a la llave, **bloqueado** contra reescritura) y `/p/P09`.
Los stickers son chips ISO 14443-4 (Type 4): no aceptan contraseña en NFC Tools, pero sí bloqueo permanente.
En iPhone el sticker abre el navegador predeterminado, no el ícono de inicio: hay que iniciar sesión ahí una vez.

La última lectura se guarda en `localStorage` y se muestra al instante mientras se refresca:
la primera consulta a Supabase en frío tarda 1–3 s.

## Puesta en marcha

1. **Supabase:** proyecto nuevo → SQL Editor → correr en orden:
   - `supabase/migrations/001_schema.sql` (tablas, `is_household()`, RLS)
   - `supabase/migrations/002_seed_plants.sql` (las 24 plantas)
   - `supabase/migrations/003_rls_perf.sql` (mismas políticas, evaluadas una vez por consulta)
   - `supabase/migrations/004_bambus_cempasuchil.sql` (tres bambús P15/P25/P26 y segundo cempasúchil P27)
   - `supabase/migrations/005_lluvia_y_agua.sql` (acción `rained`; esquejes en agua cada 30 días)
   - `supabase/migrations/006_sensibles_al_frio.sql` (`frost_sensitive`: las tres bugambilias)
2. **Cuentas:** Authentication → Users → crear los usuarios de Vic y Fer (correo + contraseña).
   Luego desactivar registros nuevos (Authentication → Providers → Email → *Allow new users to sign up*: off).
3. **Dar acceso a la casa:** en SQL Editor, con los UID de cada usuario:
   ```sql
   insert into household_members (user_id, display_name) values
     ('UID-de-Vic', 'Vic'),
     ('UID-de-Fer', 'Fer');
   ```
4. **Local:** copiar `.env.example` a `.env` con la URL y la publishable key del proyecto. `npm install && npm run dev`.
5. **Vercel:** importar el repo y agregar las mismas dos variables (Production y Preview).

6. **Alertas de clima (opcional):** en Vercel, variables de servidor tipo *Secret*: `RESEND_API_KEY`, `CRON_SECRET`;
   tipo *Config*: `ALERT_EMAIL`. `SUPABASE_SERVICE_ROLE_KEY` la pone la integración de Supabase.
   Para probar: agregar `ALERT_FORCE=1`, Redeploy, Settings → Cron Jobs → Run, y luego **borrar** `ALERT_FORCE`.

## Seguridad

Nada es público: `anon` no tiene permisos y las políticas exigen `is_household()`.
La key del bundle es pública por diseño; sin una sesión de la casa no lee ni escribe nada.
**Toda tabla nueva nace sin RLS:** activarla y agregar sus políticas en la misma migración.
Las fotos de la casa no van al repo (en una se ve el letrero de la calle).

## Ánimo

`src/lib/mood.js`, misma regla que la hoja original:
Enferma si el último "¿cómo se ve?" fue *mal*; si no, días desde el último cuidado (`care_action`:
regar, o rellenar/cambiar el agua en esquejes) contra `water_interval_days`: < 0 sedienta, 0 con sed, > 0 feliz.
"Revisé y no necesitaba" no reinicia el contador, pero queda registrado para ajustar intervalos.
**Lluvia:** "Se mojó con la lluvia" (`rained`) reinicia el contador de las plantas de tierra, sin decir que alguien regó.
Se marca a mano desde 🌧️ Llovió porque las macetas se mueven (a veces se sacan a la lluvia).
Las plantas en agua (P10–P13) no se riegan: se rellenan o cambian el agua cada 30 días.

## Escenarios, Gala y temporadas

Seis escenarios ilustrados (escaleras, estudio, sala, bufetera, cochera y pasillo) con cada planta en su lugar.
Gala se pone al acecho junto a la planta más urgente y solo se deja acariciar cuando todas están a salvo.
Los adornos cambian por fecha (`src/lib/season.js`); hoy solo Halloween/Día de Muertos (15 oct–2 nov).
Generador: `TV_IMG=/ruta/imagen.png python3 tools/scenes2/build2.py`. La imagen de la tele no va al repo.

## Alertas de clima

`api/alertas.js` corre con Vercel Cron a la 1 pm y a las 6 pm (±59 min en plan Hobby) y **solo manda correo si hay riesgo**:
mínima ≤ 4 °C hasta las 10 am del día siguiente (con cielo despejado hay escarcha aunque el aire no llegue a 0 °C),
o tormenta eléctrica en las próximas 24 h (posible granizo; no se puede asegurar con días de anticipación).
Pronóstico de Open-Meteo a nivel ciudad; correo por Resend con banner pixel (`public/alertas/`, de `tools/alertas/banners.py`).

## Sprites

`tools/sprites/plantitas.py` dibuja las 24 plantas × 4 estados con Pillow.
`python3 plantitas.py` regenera `final/`; copiar las versiones 80×96 a `public/sprites/` como `P07_feliz.png`.

## Roadmap

- [x] Zonas, ficha provisional, registro de cuidados, modo demo
- [x] Pantalla de carga, caché local, elegir fecha del cuidado, regar varias por zona
- [ ] Tarjeta tipo Pokédex (diseño pendiente de aprobación)
- [x] Stickers NFC (jardín y P09)
- [x] Fondos ilustrados por zona con Gala; bambú separado en sus tres puntos
- [x] Lluvia, esquejes en agua cada mes, alertas de helada y tormenta por correo
- [ ] Resumen diario de riegos (solo cuando haya pendientes)
- [ ] Propagación: esquejes que "nacen" y heredan linaje (`parent_id`)
- [ ] Lombricomposta: depósitos 1 y 2, mantenimiento y cosecha
- [ ] Más temporadas (Navidad, amor y amistad, patrias); redibujar sillones de la sala y a Gala
- [ ] Sensores de humedad
