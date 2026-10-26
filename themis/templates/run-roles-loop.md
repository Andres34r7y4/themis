# Run Roles Loop — Themis

Usa este prompt para ejecutar un ciclo completo de gobernanza.

```text
Ejecutá un ciclo Themis.

1) PRE-FLIGHT: declarar ROLE, MODE, CYCLE_ID y leer agent.md → roles-loop.md → tu rol.
2) PLANNER_PHASE: leer themis/tasks/tasks.md y el objetivo opcional.
   - Si tasks.md está vacío, generar como máximo 3 tareas atómicas o pasar a STOP.
3) EXECUTOR_PHASE: implementar solo las tareas de tasks.md.
   - Respetar el Context Freeze y el límite anti-catástrofe de 5 archivos.
4) VERIFICAR: ejecutar la verificación mínima y registrar la salida real.
5) ARCHIVAR: actualizar themis/tasks/archives/task-archives.md y limpiar tasks.md.
6) STOP: reportar resumen del ciclo, evidencia y riesgos abiertos.

Nunca omitas el PRE-FLIGHT. Nunca excedas los límites de tu rol.
```
