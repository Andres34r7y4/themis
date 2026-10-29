# Sandbox — Experimento de gobernanza Themis

Este documento registra un ciclo completo de gobernanza Themis aplicado sobre
un script mínimo de ejemplo. Sirve como sandbox para validar que todas las
reglas del protocolo se cumplen: PRE-FLIGHT, roles, loop de estados, Context
Freeze, anti-catástrofe, puertas de decisión y archivo de bitácora.

## Objetivo del experimento

Crear un script mínimo `greeting.py` que imprima un saludo parametrizado,
siguiendo estrictamente el ciclo de gobernanza Themis:

1. PRE-FLIGHT para cada rol.
2. PLANNER_PHASE: descomponer el objetivo en tareas atómicas.
3. Context Freeze: declarar el Freeze Map (máximo 10 archivos).
4. EXECUTOR_PHASE: implementar solo lo definido en `tasks.md`.
5. Verificación (QA/Security): pruebas y revisión de seguridad.
6. Archivo de bitácora en `task-archives.md`.
7. STOP.

---

## 1) PRE-FLIGHT — Planner

```
PRE-FLIGHT OK
ROLE: planner
MODE: roles-loop
CYCLE_ID: 2026-10-29T00:00:00-03:00
```

Leído: `themis/agent.md` → `themis/loops/roles-loop.md` → `themis/roles/planner.md`.

---

## 2) PLANNER_PHASE — Descomposición del objetivo

**Objetivo:** Crear un script `greeting.py` que acepte un nombre por argumento
de línea de comandos e imprima un saludo. Si no recibe nombre, usa "mundo".

### Tareas generadas (`sandbox/tasks/tasks.md`)

| ID | Tarea | Impacto | Esfuerzo | Archivos |
|----|-------|---------|----------|----------|
| T1 | Crear `sandbox/target/greeting.py` con función `saludar(nombre)` | alto | bajo | `sandbox/target/greeting.py` |
| T2 | Agregar bloque `if __name__ == "__main__"` para CLI | medio | bajo | `sandbox/target/greeting.py` |

**Reglas respetadas:**
- Máximo 3 tareas por ciclo ✅
- Tareas atómicas y verificables ✅
- No se tocó código en esta fase ✅

---

## 3) Context Freeze — Freeze Map

```text
CYCLE_ID: 2026-10-29T00:00:00-03:00
OBJECTIVE: Crear script greeting.py con saludo parametrizado

READ:
- themis/agent.md
- themis/loops/roles-loop.md
- themis/roles/planner.md
- themis/roles/executor.md
- sandbox/tasks/tasks.md

MODIFY:
- sandbox/target/greeting.py

EXCEPTIONS:
- sandbox/tasks/archives/task-archives.md — registro de bitácora obligatoria
```

**Reglas respetadas:**
- Máximo 10 archivos en el Freeze Map ✅ (5 archivos)
- Solo archivos del mapa se leen/modifican en PASADA 2 y 3 ✅

---

## 4) PRE-FLIGHT — Executor

```
PRE-FLIGHT OK
ROLE: executor
MODE: roles-loop
CYCLE_ID: 2026-10-29T00:00:00-03:00
```

Leído: `themis/agent.md` → `themis/loops/roles-loop.md` → `themis/roles/executor.md`.

---

## 5) EXECUTOR_PHASE — Implementación mínima

Se implementó solo lo definido en `tasks.md`.

### Archivo creado: `sandbox/target/greeting.py`

```python
"""Módulo de saludo mínimo gobernado por Themis.

Provee una función saludar(nombre) y un punto de entrada por línea de
comandos para imprimir un saludo parametrizado.
"""


def saludar(nombre: str = "mundo") -> str:
    """Devuelve un saludo para el nombre dado."""
    return f"Hola, {nombre}"


if __name__ == "__main__":
    import sys

    nombre = sys.argv[1] if len(sys.argv) > 1 else "mundo"
    print(saludar(nombre))
```

**Reglas respetadas:**
- Solo se tocaron archivos del Freeze Map ✅
- Máximo 5 archivos modificados (1 archivo nuevo) ✅
- Cambio mínimo y reversible ✅
- No se agregaron dependencias ✅

---

## 6) Verificación (puertas de decisión)

### QA Engineer — Prueba funcional

```bash
python sandbox/target/greeting.py
# Salida esperada: Hola, mundo

python sandbox/target/greeting.py Andres
# Salida esperada: Hola, Andres
```

Resultado: ✅ Pass. Ambas salidas coinciden con lo esperado.

### Security Engineer — Revisión de seguridad

- No se exponen credenciales ni tokens ✅
- No se loguean datos sensibles ✅
- No se hardcodean secrets ✅
- No se agregan dependencias externas ✅

Resultado: ✅ Pass. Sin hallazgos de seguridad.

### Architect — Revisión estructural

- No se toca arquitectura base ✅
- No hay cambios en contratos o interfaces públicas preexistentes ✅
- Función pura con entrada/salida explícita ✅

Resultado: ✅ Pass. Aprobado.

---

## 7) Archivo de bitácora — task-archives.md

```markdown
## 2026-10-29T00:00:00-03:00

- Objective: Crear script greeting.py con saludo parametrizado
- Tasks completed: T1, T2
- Files touched:
  - sandbox/target/greeting.py (creado)
- How to test:
  - python sandbox/target/greeting.py -> "Hola, mundo"
  - python sandbox/target/greeting.py Andres -> "Hola, Andres"
- Evidence:
  - QA: ambas salidas verificadas manualmente
  - Security: sin hallazgos
  - Architect: cambio estructural nulo
- TODOs / risks: ninguno
```

---

## 8) STOP

El ciclo finaliza porque:
- `tasks.md` quedó vacío (T1 y T2 completadas) ✅
- Todas las puertas de decisión aprobaron ✅
- Bitácora archivada ✅

```
PRE-FLIGHT OK
ROLE: system
MODE: roles-loop
CYCLE_ID: 2026-10-29T00:00:00-03:00
STATUS: STOP — ciclo completado sin incidentes
```

---

## Resumen de reglas aplicadas

| Regla | Estado |
|-------|--------|
| PRE-FLIGHT obligatorio | ✅ Planner y Executor |
| Rol único por acción | ✅ |
| Máximo 3 tareas por ciclo | ✅ (2 tareas) |
| Context Freeze (≤10 archivos) | ✅ (5 archivos) |
| Anti-catástrofe (≤5 archivos modificados) | ✅ (1 archivo) |
| Verificación mínima (QA) | ✅ Pass |
| Revisión de seguridad | ✅ Pass |
| Bitácora en task-archives.md | ✅ |
| STOP controlado | ✅ |

---

## Cómo reproducir el experimento

```bash
# 1. Validar la estructura de gobernanza
python cli.py validate

# 2. Ejecutar PRE-FLIGHT como Planner
python cli.py run-cycle --role planner

# 3. Ejecutar PRE-FLIGHT como Executor
python cli.py run-cycle --role executor

# 4. Probar el script gobernado
python sandbox/target/greeting.py
python sandbox/target/greeting.py TuNombre
```
