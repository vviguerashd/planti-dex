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

**Sin Supabase configurado la app corre en modo demo** (24 plantas y registros inventados en memoria).

Rutas: `/` (zonas) y `/p/P07` (ficha de una planta). La segunda es la que abre cada sticker NFC.

## Puesta en marcha

1. **Supabase:** proyecto nuevo → SQL Editor → correr en orden:
   - `supabase/migrations/001_schema.sql` (tablas, `is_household()`, RLS)
   - `supabase/migrations/002_seed_plants.sql` (las 24 plantas)
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

## Seguridad

Nada es público: `anon` no tiene permisos y las políticas exigen `is_household()`.
La key del bundle es pública por diseño; sin una sesión de la casa no lee ni escribe nada.
**Toda tabla nueva nace sin RLS:** activarla y agregar sus políticas en la misma migración.
Las fotos de la casa no van al repo (en una se ve el letrero de la calle).

## Ánimo

`src/lib/mood.js`, misma regla que la hoja original:
Enferma si el último "¿cómo se ve?" fue *mal*; si no, días desde el último cuidado (`care_action`:
regar, o cambiar el agua en esquejes) contra `water_interval_days`: < 0 sedienta, 0 con sed, > 0 feliz.
"Revisé y no necesitaba" no reinicia el contador, pero queda registrado para ajustar intervalos.

## Sprites

`tools/sprites/plantitas.py` dibuja las 24 plantas × 4 estados con Pillow.
`python3 plantitas.py` regenera `final/`; copiar las versiones 80×96 a `public/sprites/` como `P07_feliz.png`.

## Roadmap

- [x] Zonas, ficha provisional, registro de cuidados, modo demo
- [ ] Tarjeta tipo Pokédex (diseño pendiente de aprobación)
- [ ] Stickers NFC (cuando la URL de producción sea definitiva)
- [ ] Avisos cuando una planta tenga sed
- [ ] Propagación: esquejes que "nacen" y heredan linaje (`parent_id`)
- [ ] Lombricomposta como mascota
- [ ] Fondos ilustrados por zona; bambú separado en sus tres puntos
- [ ] Sensores de humedad
