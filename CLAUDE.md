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

## Escenarios y Gala
- Fondos en `public/scenes/{id}.png` (pixel nativo, se muestran a ×2) y posiciones de cada planta en `src/lib/scenes.json`. Se regeneran con `python3 tools/scenes/build.py` (necesita Pillow). Planta nueva = agregarla al `pos` de su escena en el script.
- Gala (`public/gala/`): al acecho junto a la planta más urgente; solo se deja acariciar cuando ninguna planta está sedienta, con sed o enferma. Las fotos reales de la casa y de Gala NO van al repo.
- El jardín se divide en Cochera y Pasillo solo a nivel de escena; en la base sigue siendo `zone = 'jardin'`.
