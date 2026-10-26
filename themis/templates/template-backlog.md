# Plantilla de Backlog — Themis

```markdown
# Backlog — <repositorio>

## tarea
id: backlog-AUTO
título: <título corto e imperativo>
impacto: alto | medio | bajo
esfuerzo: bajo | medio | alto
riesgo: bajo | medio | alto
depende_de: []

### Contexto
<por qué importa y qué problema resuelve>

### Propuesta
<cambio mínimo o resultado esperado>

### Criterios de aceptación
- [ ] <criterio verificable>

### Notas
<restricción o pregunta abierta>
```

## Reglas

- Máximo 10 entradas de backlog.
- Ordenar por impacto (desc), esfuerzo (asc), riesgo (asc), dependencias e ID.
- Máximo 3 entradas se convierten a `tasks.md` por ciclo.
- El Planner consume esta cola y agrega las entradas consumidas a
  `themis/outputs/ia/reports/backlog_archives.md`.
