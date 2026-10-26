# Plantilla de Tarea — Themis

```markdown
### tarea
id: AUTO
título: <título corto e imperativo>
impacto: alto | medio | bajo
esfuerzo: bajo | medio | alto
riesgo: bajo | medio | alto
depende_de: []

#### Objetivo
<qué debe lograrse y por qué>

#### Definición de terminado
- [ ] <criterio verificable>
- [ ] <criterio verificable>

#### Archivos probables
- <ruta real o "desconocido">

#### Verificación
- Comando: <comando real>
- Esperado: <resultado observable>

#### Notas
<restricción, pregunta abierta o TODO>
```

## Reglas

- Los IDs se generan automáticamente (`YYYY-MM-DD-XX` para ciclos, `backlog-XXX` para backlog).
- Máximo 3 tareas activas por ciclo.
- Cada tarea debe ser atómica y verificable en un ciclo.
- No listes archivos que no hayas verificado salvo que estén marcados como probables.
