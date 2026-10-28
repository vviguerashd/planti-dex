# CLAUDE.md

Guía para Claude Code en este repo. Ver README para arquitectura y puesta en marcha.

## Comandos
`npm run dev` · `npm run build` · `npm run preview`. Sin tests ni linter.

## Convenciones
- **UI en español** (usuarios: Vic y Fer). Valores internos en inglés/ASCII (`watered`, `jardin`): son datos en Supabase, no se traducen.
- **Estilos inline** con tokens de `src/lib/theme.js`. Nada de colores sueltos en componentes. Texto ≥ 4.5:1; chips de ánimo verificados ≥ 7:1.
- **Accesibilidad desde el inicio:** botones reales, `aria-pressed` en toggles, `role="status"` para confirmaciones, `alt=""` en sprites cuando el nombre ya está en texto, foco visible global en `index.css`.
- **Fechas locales siempre** (`src/lib/dates.js`). Nunca `toISOString()` para "hoy" (Pachuca es UTC-6).
- **El id de planta (`P07`) nunca cambia:** está escrito en un sticker NFC.
- **Toda tabla nueva:** activar RLS y políticas con `is_household()` en la misma migración.
- Sprites: `public/sprites/{id}_{feliz|con_sed|sedienta|enferma}.png`, 80×96, siempre `className="pixel"` (image-rendering: pixelated).

## Pendiente de diseño
La ficha `PlantSheet.jsx` es provisional. Vic quiere ver el arte de la tarjeta tipo Pokédex antes de que se programe.
