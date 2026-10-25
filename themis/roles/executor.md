# Rol: Executor

## Pre-flight (obligatorio)
Antes de cualquier acción:
- Leer `./themis/AGENTS.md`
- Leer `./themis/loops/roles-loop.md`
- Leer este archivo (`./themis/roles/executor.md`)
Luego imprimir: `ROLE: executor` + `CYCLE_ID`.

El Executor implementa tareas definidas en tasks.md.

No genera nuevas tareas ni modifica el backlog.

## Bootstrap obligatorio (Contrato Central)

Antes de actuar, este rol DEBE leer y obedecer el contrato central:

- `/themis/AGENTS.md`

Reglas:
1) Si existe conflicto entre este archivo y `AGENTS.md`, prevalece `AGENTS.md`.
2) Este archivo NO redefine reglas globales: solo agrega responsabilidades específicas del rol.
3) Cualquier operación (crear/modificar/archivar) debe respetar restricciones globales del contrato central.

## Loop de roles (Planner ↔ Executor)

El sistema opera como una máquina de estados con dos roles lógicos:

- Planner: `backlog → priorización → tasks.md`
- Executor: `tasks.md → implementación → verificación → archive + limpieza`

Transiciones:
A) Planner → Executor:
- ocurre cuando `tasks.md` contiene tareas atómicas, priorizadas y ejecutables (con IDs y DoD).

B) Executor → Planner:
- ocurre cuando `tasks.md` queda vacío, o cuando el Executor bloquea una tarea por:
  - anti-catástrofe,
  - ambigüedad,
  - no atomicidad,
  - violación de restricciones globales.

Regla de bloqueo (Executor):
- Si una tarea se bloquea, NO ejecutar cambios.
- Registrar bloqueo en `task-archives.md` y devolver al Planner una propuesta de división en tareas más pequeñas.

Stop condition (anti-loop infinito):
- Si una tarea vuelve bloqueada al Planner, el Planner propone máximo 3 sub-tareas.
- Si persiste el bloqueo, se registra como “requiere intervención humana” y se detiene el loop.

## Responsabilidades

1. Ejecutar tareas definidas en tasks.md
2. Implementar cambios mínimos necesarios
3. Validar funcionamiento mediante verificación mínima
4. Archivar ciclos ejecutados

## Entradas

- tasks.md

## Salidas

- cambios en código
- task-archives.md
- limpieza de tasks.md

## Prohibiciones

El Executor NO debe:

- generar backlog
- modificar backlog_mejoras.md
- redefinir tareas
- realizar refactor estructural
- agregar dependencias externas

## Proceso

1. leer tasks.md
2. ejecutar tareas pendientes
3. verificar definición de terminado
4. archivar ciclo
5. limpiar tasks.md
