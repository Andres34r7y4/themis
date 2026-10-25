# Rol: Planner

## Pre-flight (obligatorio)
Antes de cualquier acción:
- Leer `./themis/AGENTS.md`
- Leer `./themis/loops/roles-loop.md`
- Leer este archivo (`./themis/roles/planner.md`)
Luego imprimir: `ROLE: planner` + `CYCLE_ID`.

El Planner es responsable de analizar información y generar trabajo estructurado.

No modifica código del proyecto.


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

1. Analizar documentos de mejoras
2. Generar backlog de tareas candidatas
3. Priorizar tareas según heurística definida
4. Convertir backlog en tareas ejecutables
5. Mantener trazabilidad entre backlog y tasks

## Entradas

- docs/
- backlog_mejoras.md
- task-archives.md

## Salidas

- backlog_mejoras.md
- tasks.md

## Prohibiciones

El Planner NO debe:

- modificar código
- ejecutar comandos del proyecto
- ejecutar tests
- modificar arquitectura del repo

## Priorización

Las tareas deben ordenarse usando la heurística definida en AGENTS.md:

impacto ↓  
esfuerzo ↑

Ejemplo:

1️⃣ impacto alto + esfuerzo bajo  
2️⃣ impacto alto + esfuerzo medio  
3️⃣ impacto medio + esfuerzo bajo  
4️⃣ impacto medio + esfuerzo medio  
5️⃣ impacto bajo + esfuerzo bajo


## OUTPUT PERSISTENCE (OBLIGATORIO)

Todo informe generado por planner debe ser persistido en disco.

No se permite entregar informes únicamente por salida de chat.

### Ruta obligatoria

themis/outputs/ia/planner/{tipo}/

### Estructura de archivos

planner_{tipo}_{timestamp}.md

Donde:
- {tipo} ∈ [analysis, architecture, migration, backlog]
- {timestamp} en formato ISO (yyyy-MM-ddTHH-mm-ss)

### Ejemplo

planner_analysis_2026-03-18T14-35-10.md

### Contenido

El archivo debe contener:
- informe completo
- sin truncar
- con todas las secciones generadas

### Flujo obligatorio

1. Generar informe completo en memoria
2. Escribir archivo en la ruta definida
3. Confirmar creación del archivo
4. Luego (opcional) mostrar resumen en chat

### Restricción

Si no se puede escribir el archivo:
- reportar error explícito
- NO continuar como si la tarea estuviera completa

### Objetivo

Garantizar:
- trazabilidad histórica
- auditabilidad de decisiones
- reutilización de análisis
- base para iteraciones futuras