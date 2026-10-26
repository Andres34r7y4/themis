# roles-loop.md — Orquestación Planner ↔ Executor (V1)

## 0) Pre-flight (OBLIGATORIO)
Antes de cualquier acción, el sistema DEBE:
1) leer `./themis/agent.md`
2) leer `./themis/loops/roles-loop.md`
3) leer `./themis/roles/planner.md` o `./themis/roles/debugger.md` o `./themis/roles/executor.md` según corresponda
4) imprimir una línea de estado:
   - `ROLE: planner` o `ROLE: debugger` o `ROLE: executor`
   - `CYCLE_ID: <id>`
   - `MODE: roles-loop`

Regla dura:
- Si hay conflicto entre roles-loop / roles/* y `agent.md`, **prevalece `agent.md`**.

---

## 1) Estados del loop

Estados válidos:
- `PLANNER_PHASE`
- `DEBUGGER_PHASE`
- `DESIGNER_PHASE`
- `EXECUTOR_PHASE`
- `STOP`

El sistema inicia en:

- `PLANNER_PHASE` para ciclos normales (`feature`, `backlog`, `analisis`)
- `DEBUGGER_PHASE` si el usuario indica explícitamente un ciclo de tipo:
  - `bug`
  - `diagnostico`
  - `analisis_dinamico`
  y ya existe un síntoma suficientemente definido
- `DESIGNER_PHASE` si el ciclo es de tipo `diseno` o la tarea trae brief visual
- `PLANNER_PHASE` si el bug todavía debe descomponerse o aclararse antes del diagnóstico
- `EXECUTOR_PHASE` solo si el usuario indica explícitamente “solo ejecutar tasks.md”

---

## 2) Entradas / salidas canónicas
Planner lee:
- `themis/objective.md` (si existe)
- `./themis/tasks/tasks.md`
- (opcional) backlog/mejoras si existiera en docs

Planner escribe:
- `./themis/tasks/tasks.md` (máx 3 tareas por ciclo, siguiendo template)
- (opcional) notas de planificación en outputs (solo si el contrato lo permite)

Debugger lee:
- `./themis/tasks/tasks.md` (si existe ciclo activo)
- reporte previo del Planner (si existe)
- repo real (archivos reales)
- `repo_index` / outputs estructurales si existen
- síntoma declarado por el usuario o por Planner

Debugger escribe:
- `./themis/outputs/ia/reports/debug_<CYCLE_ID>.md` (informe obligatorio)
- (opcional) trazas mínimas o cambios temporales de diagnóstico, solo si el contrato y el ciclo lo permiten
- (opcional) recomendaciones para partición o handoff a Executor

Diseñador lee:
- `./themis/tasks/tasks.md` (brief visual del ciclo)
- `tokens.yaml` / temas vigentes + referencias del brief
- repo real (solo lo visual alcanzado por el brief)

Diseñador escribe:
- `./themis/outputs/ia/reports/design_<CYCLE_ID>.md` (informe obligatorio + veto)
- (opcional) propuestas con criterios medibles y tokens (sin implementar si la tarea no lo autoriza)

Executor lee:
- `./themis/tasks/tasks.md` (ÚNICA fuente de tareas)
- repo real (archivos reales)

Executor escribe:
- cambios mínimos en código (solo para cumplir tasks.md)
- `./themis/tasks/archives/task-archives.md` (bitácora obligatoria)
- actualiza `./themis/tasks/tasks.md` removiendo tareas completadas

---

## 3) Reglas del Planner (PLANNER_PHASE)
Objetivo: convertir objetivos/backlog en tareas atómicas.

Checklist:
1) NO tocar código.
2) NO ejecutar smoke test.
3) Crear/actualizar `tasks.md`:
   - ordenadas por prioridad: **Impacto alto + Esfuerzo bajo** primero
   - luego: alto+medio, alto+alto, medio+bajo, medio+medio, bajo+* al final
4) Cada tarea debe incluir:
   - impacto: alto|medio|bajo
   - esfuerzo: bajo|medio|alto
   - criterio de terminado
   - archivos probables a tocar (si se pueden inferir sin inventar)

Condición de handoff:
- Si `tasks.md` tiene ≥ 1 tarea, pasar a `EXECUTOR_PHASE`.
- Si `tasks.md` queda vacío, pasar a `STOP`.

---

## 4) Reglas del Debugger (DEBUGGER_PHASE)

Objetivo: diagnosticar bugs sin implementar fixes definitivos y producir evidencia utilizable.

Checklist:
1) NO refactorizar.
2) NO hacer cambios permanentes de lógica salvo autorización explícita.
3) Alinear el síntoma:
   - esperado
   - observado
   - contexto
   - alcance
4) Formular entre 2 y 5 hipótesis verificables.
5) Generar `debug_<CYCLE_ID>.md` con:
   - síntoma
   - zona del problema
   - hipótesis
   - evidencia
   - resultado
   - próximo paso
6) Si requiere cambios de debug:
   - deben ser mínimos
   - reversibles
   - documentados como temporales
7) Si el diagnóstico requiere sandbox, preferir worktree temporal.

Condición de handoff:
- pasar a `EXECUTOR_PHASE` solo si:
  - existe `debug_<CYCLE_ID>.md`
  - hay causa raíz probable o hipótesis dominante sustentada
  - el próximo paso está suficientemente delimitado
- volver a `PLANNER_PHASE` si:
  - el bug sigue ambiguo
  - la tarea debe partirse
  - se requiere input humano
- pasar a `STOP` si:
  - no hay síntoma reproducible
  - falta entorno
  - el ciclo queda bloqueado

---

## 5) Reglas del Executor (EXECUTOR_PHASE)
Objetivo: ejecutar SOLO lo que está en `tasks.md`.

Checklist:
0) Si el ciclo es de bug, leer obligatoriamente `debug_<CYCLE_ID>.md` antes de tocar código.
0b) Si la tarea es visual (brief/`diseno`), leer obligatoriamente `design_<CYCLE_ID>.md` antes de tocar lo visual.
1) Aplicar Tree workflow de `agent.md` (3 pasadas).
2) Implementar cambios mínimos.
3) Verificación mínima (smoke test) SOLO si aplica al tipo de ciclo.
4) Archivar en `task-archives.md` con:
   - CYCLE_ID
   - objetivo
   - tareas completadas ✅
   - archivos tocados (rutas reales)
   - cómo probar (comandos reales)
   - TODOs / riesgos

Condición de handoff:
- Si quedan tareas pendientes en `tasks.md`:
  - volver a `PLANNER_PHASE` SOLO si hay ambigüedad / tarea no atómica / anti-catástrofe.
  - si son tareas claras restantes, puede continuar en `EXECUTOR_PHASE` hasta max 3 tareas/ciclo.
- Si `tasks.md` queda vacío: `STOP`.

En ciclos de tipo `bug`, `diagnostico` o `analisis_dinamico`, el Executor NO debe actuar si no existe un informe previo del Debugger:

`./themis/outputs/ia/reports/debug_<CYCLE_ID>.md`

Ese informe funciona como fuente obligatoria de contexto técnico para la implementación del fix.

En ciclos de tipo `diseno` o tareas con brief visual, el Executor NO debe tocar lo visual si no existe un informe previo del Diseñador:

`./themis/outputs/ia/reports/design_<CYCLE_ID>.md`

## 5c) Gates de roles de soporte (sin fases nuevas)

Los 6 roles de soporte operan como gates del checklist Executor (además del `0b` visual):

- `0c` **Security**: hace cumplir `agent.md §4` en todo ciclo con cambios.
- `0d` **QA**: valida aceptación pre-STOP en ciclos con código.
- `0e` **Architect**: gate cuando el ciclo toca estructura, contratos o dependencias.
- `0f` **Documentator**: gate de docs del entregable (la bitácora sigue en Executor).
- `0g` **DevOps**: gate de hooks/pipeline/worktrees y rollback.
- `0h` **Product Owner**: gate pre-Planificación (valor y aceptación de candidatas).

Cada gate se salda con su informe (`security_/qa_/architecture_/docs_/devops_/product_<CYCLE_ID>.md`) o con veto fundado que devuelve a `PLANNER_PHASE`. Precedencia de vetos en `agent.md §12.7`.

## 5b) Reglas del Diseñador (DESIGNER_PHASE)

Objetivo: investigar y proponer lo visual con teoría y criterios medibles, sin implementar el rediseño salvo autorización en la tarea.

Checklist:
1) Exigir brief mínimo (objetivo, audiencia/contexto, restricciones, referencias). Sin brief: STOP + pedido de input.
2) Fase research sin dibujar (referencias reales + teoría del rol, 3–6 bullets).
3) Proponer máx 2 variantes con criterios medibles + 1 recomendada, en `design_<CYCLE_ID>.md`.
4) Registrar paleta/espaciado en tokens (nombres, vía Planner si crea llaves).
5) Vetar por escrito lo que no cumpla los criterios, con alternativa.

Condición de handoff:
- pasar a `EXECUTOR_PHASE` con informe + tokens + criterios cuando la propuesta está lista para implementar.
- volver a `PLANNER_PHASE` si falta brief, el diseño debe partirse o hay conflicto de contrato.
- pasar a `STOP` si no hay entorno de verificación o el humano debe decidir.

---

## 6) Anti-catástrofe (corte automático)
Antes de implementar, evaluar:
- cantidad estimada de archivos a modificar
- cambios estructurales
- atomicidad de la tarea

Condiciones de bloqueo:
- más de 5 archivos
- refactor estructural
- cambio no autorizado de arquitectura
- tarea ambigua / no atómica

Si se dispara:
1) NO ejecutar cambios.
2) registrar en `task-archives.md` (con CYCLE_ID y motivo)
3) proponer partición en tareas más pequeñas (vuelve a `PLANNER_PHASE`)

---

## 7) Stop conditions

El loop termina cuando:
- `tasks.md` está vacío, o
- se dispara anti-catástrofe y se requiere input humano, o
- se alcanzó el máximo de 3 tareas para el ciclo actual, o
- un ciclo de bug queda bloqueado por:
  - falta de síntoma claro
  - falta de entorno reproducible
  - evidencia insuficiente tras diagnóstico mínimo
  - necesidad de decisión humana

---

## 8) Verificación y presupuesto (best practices multi-agente)

Roles obligatorios por ciclo: **Planner** (descompone), **Executor**
(ejecuta un paso por vez), **Verifier** (chequeo determinístico:
tests, validación, typecheck — nunca solo "se ve bien").

1) **Evidencia antes de STOP**: ningún ciclo cierra sin un chequeo
   ejecutado por código (suite verde, `validate`, ping honesto).
2) **Loop budget**: máx 2 rondas Executor→revisión; a la 3ª se escala
   a humano con el desacuerdo por escrito.
3) **Dehallucinación comunicativa**: si al Executor le falta un dato
   del plan, pregunta al rol que corresponda ANTES de inventarlo.
4) **Mínimo privilegio por rol**: cada rol solo toca sus artefactos
   (Planner: tasks/plan; Executor: código; Debugger: reportes).
   Sin llaves ni secretos en artefactos, jamás.
