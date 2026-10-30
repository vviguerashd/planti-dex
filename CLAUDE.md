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
- Fondos en `public/scenes/{id}.png` y `{id}_{temporada}.png` (pixel nativo, se muestran a ×2); posiciones de cada planta en `src/lib/scenes.json`. Generador vigente: `TV_IMG=/ruta/gala_con_dios.png python3 tools/scenes2/build2.py` (Pillow + numpy). `tools/scenes/` es la v1 y solo aporta los sprites de Gala. Planta nueva = agregarla al `POS` de su escena.
- Temporadas: `src/lib/season.js` decide por fecha local (Halloween/Muertos 15 oct–2 nov). Los adornos de temporada se dibujan solo si `SEASON` coincide; todo lo demás es fijo.
- Gala (`public/gala/`): al acecho junto a la planta más urgente; solo se deja acariciar cuando ninguna planta está sedienta, con sed o enferma. Las fotos reales de la casa y de Gala NO van al repo.
- El jardín se divide en Cochera y Pasillo solo a nivel de escena; en la base sigue siendo `zone = 'jardin'`.
