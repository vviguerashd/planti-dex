// Tokens definidos ANTES de los componentes (lección de DuoFit).
// Contrastes verificados contra el fondo correspondiente (AA ≥ 4.5:1 para texto normal).
export const t = {
  bg: '#f6f4ec',          // papel
  surface: '#ffffff',
  ink: '#1c241e',         // texto principal  (14.4:1 sobre bg)
  inkMuted: '#4a554c',    // texto secundario (7.1:1 sobre bg)
  line: '#d9d4c3',
  brand: '#1f3a26',       // verde oscuro de cabecera (texto blanco 12.4:1)
  focus: '#1d5fd1',
  // Chips de ánimo: todos ≥ 7:1 texto/fondo.
  mood: {
    feliz:        { bg: '#dcefd5', ink: '#1e4d22' },
    con_sed:      { bg: '#fdebb3', ink: '#5c3d00' },
    sedienta:     { bg: '#f9d0cc', ink: '#7a1c14' },
    enferma:      { bg: '#e4dcf3', ink: '#45246e' },
    sin_registro: { bg: '#ebe8de', ink: '#3d4540' },
  },
  pixelFont: "'Press Start 2P', ui-monospace, monospace",
  bodyFont: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
}
