# Guía de uso del sistema `core`

## Principio obligatorio
Antes de cualquier acción o respuesta del agente, se debe leer y obedecer el contrato central en `/agents/AGENTS.md` y luego las reglas del loop y del rol correspondiente.

## Propósito de `core`
`core` centraliza el contrato, roles, loops, tareas y salidas de IA para ejecutar ciclos controlados con trazabilidad, cambios mínimos y seguridad.

## Formas de uso (modos de operación)

### 1) Ciclo normal (feature / mejora / análisis)
Se inicia en `PLANNER_PHASE` y sigue el `roles-loop` hasta `STOP`.

### 2) Ciclo de bug / diagnóstico
Se inicia en `DEBUGGER_PHASE` cuando el síntoma está claro. El Debugger produce evidencia y el Executor solo implementa con informe previo.

### 3) Solo ejecución de tasks
Cuando el usuario indica explícitamente “solo ejecutar tasks.md”, se arranca en `EXECUTOR_PHASE`.

### 4) Backlog → tasks
El Planner genera backlog desde documentación y luego convierte tareas prioritarias en `tasks.md`.

### 5) Index-first
Uso del repo index en `/agents/outputs/repo_index/` para inspección rápida (sin lectura masiva de archivos).

## Flujo de trabajo (alto nivel)
1. **Pre-flight**: leer `AGENTS.md`, `roles-loop.md` y rol activo; imprimir `PRE-FLIGHT OK`, `ROLE`, `MODE`, `CYCLE_ID`.
2. **PASADA 1 (Entender)**: definir Freeze Map y plan mínimo.
3. **PASADA 2 (Implementar)**: cambios mínimos (solo si aplica).
4. **PASADA 3 (Verificar)**: verificación mínima según tipo de ciclo.
5. **Archivar**: registrar en `task-archives.md` y limpiar `tasks.md`.

## Pruebas sin tocar código (no invasivas)
Estas pruebas son **documentales** y **no ejecutan** automatizaciones del dominio:
- Verificar que existan las rutas clave:
  - `/agents/AGENTS.md`
  - `/agents/loops/roles-loop.md`
  - `/agents/roles/`
  - `/agents/tasks/tasks.md`
  - `/agents/tasks/archives/task-archives.md`
- Confirmar que los templates existan:
  - `/agents/in/humans/template-task.md`
  - `/agents/in/humans/template-backlog.md`
- Confirmar que el backlog activo y el histórico existan:
  - `/agents/outputs/ia/reports/backlog_mejoras.md`
  - `/agents/outputs/ia/reports/backlog_archives.md`
- Validar que el repo index esté presente si se requiere flujo index-first:
  - `/agents/outputs/repo_index/index.sqlite`
  - `/agents/outputs/repo_index/queries/README.md`

## Planificación del flujo (rol Planner)
El Planner debe:
- Leer documentación relevante (si aplica).
- Generar backlog (máx. 10 tareas, atómicas).
- Priorizar según el contrato (impacto ↓, esfuerzo ↑, riesgo ↑, dependencias).
- Convertir a `tasks.md` (máx. 3 tareas por ciclo).
- No tocar código ni ejecutar comandos.

## Ejemplos de uso (sin ejecución)

### A) Generar backlog
- Entrada: `agents/agents/objetivo.md`
- Salida: `/agents/outputs/ia/reports/backlog_mejoras.md`

### B) Convertir backlog en tareas
- Entrada: `/agents/outputs/ia/reports/backlog_mejoras.md`
- Salida: `/agents/tasks/tasks.md` (máx. 3 tareas)

### C) Diagnóstico de bug
- Entrada: síntoma claro + `tasks.md`
- Salida: `/agents/outputs/ia/reports/debug/debug_<CYCLE_ID>.md`

### D) Ejecución de tasks
- Entrada: `/agents/tasks/tasks.md`
- Salida: cambios mínimos + `task-archives.md` actualizado

## Reglas de seguridad (resumen)
- No exponer credenciales ni tokens.
- No agregar dependencias sin autorización.
- No modificar adaptadores específicos ni la capa base sin tarea explícita.
- No inventar rutas, módulos o datos.
- Mantener cambios mínimos y reversibles.

## Extender el sistema con nuevos roles
Para agregar un rol se requiere:
1. Actualizar `/agents/AGENTS.md` declarando el rol y sus límites.
2. Crear `/agents/roles/<rol>.md`.
3. Actualizar `/agents/loops/roles-loop.md` con estados y handoffs.
4. Asegurar el pre-flight y la precedencia del contrato central.

## Checklist rápido del Planner (ciclo de documentación)
- [ ] Leí `/agents/AGENTS.md`
- [ ] Leí `/agents/loops/roles-loop.md`
- [ ] Leí `/agents/roles/planner.md`
- [ ] No toqué código
- [ ] No ejecuté comandos del dominio
- [ ] Documenté el flujo y ejemplos
