# Ejemplos de Integración — Gobernanza Themis con LLMs

Este documento muestra cómo integrar la gobernanza de Themis en sistemas reales
de agentes basados en LLM.

## Ejemplo 1: Inyección en el system prompt (OpenAI / Anthropic / DeepSeek / Ollama)

El archivo `themis/agent.md` es el **kernel de gobernanza**. Inyéctalo en el
system prompt de tu agente:

```python
from pathlib import Path

THEMIS_KERNEL = Path("themis/agent.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""
Sos un agente autónomo que opera bajo el Protocolo de Gobernanza Themis V1.

{THEMIS_KERNEL}

Antes de CADA acción, debés:
1. Ejecutar PRE-FLIGHT: declarar ROLE, CYCLE_ID, MODE.
2. Leer agent.md -> roles-loop.md -> roles/<ROL>.md.
3. Imprimir "PRE-FLIGHT OK" con tu ROLE, MODE y CYCLE_ID.
4. Solo entonces continuar con las responsabilidades de tu rol.

Nunca omitas el PRE-FLIGHT. Nunca excedas los límites de tu rol.
"""

# Luego pasa SYSTEM_PROMPT a tu proveedor de LLM.
response = llm.complete(system=SYSTEM_PROMPT, user=user_request)
```

## Ejemplo 2: Validación PRE-FLIGHT en el loop del agente

El paquete Python vive en `core/` (módulo de nivel superior):

```python
from pathlib import Path

from core.kernel import GovernanceKernel

kernel = GovernanceKernel(Path("."))

try:
    result = kernel.pre_flight(role="planner", mode="roles-loop")
    print(kernel.format_pre_flight(result))

    # Solo ahora continuar con las tareas del Planner...
    # plan = planner.decompose(objective)

except ValueError as exc:
    print(f"GOVERNANCE BLOCK: {exc}")
    # Detener la ejecución — no continuar.
```

## Ejemplo 3: Ciclo completo con enforcement de roles

```python
from pathlib import Path

from core.kernel import GovernanceKernel
from core.loop import LoopOrchestrator
from core.roles import get_role

kernel = GovernanceKernel(Path("."))

# Validar la estructura primero.
missing = kernel.validate_structure()
if missing:
    raise RuntimeError(f"Faltan archivos de gobernanza: {missing}")

# Inicializar el loop.
loop = LoopOrchestrator(cycle_id="2026-10-24T10:00:00Z")

# Fase del Planner.
result = kernel.pre_flight(role="planner", mode="roles-loop")
print(kernel.format_pre_flight(result))
planner = get_role("planner")
print(f"Misión del Planner: {planner.mission}")

# Transición al Executor.
loop.transition("EXECUTOR_PHASE", new_role="executor")

result = kernel.pre_flight(role="executor", mode="roles-loop")
print(kernel.format_pre_flight(result))
executor = get_role("executor")
print(f"El Executor puede tocar código: {executor.can_touch_code}")

print(f"Estado del loop: {loop.get_summary()}")
```

## Ejemplo 4: Uso del CLI

```bash
# Instalar el CLI desde un clon.
python -m pip install -e .

# Inicializar la gobernanza en un repositorio nuevo.
themis init --repo ./mi-proyecto --base-dir themis

# Validar la estructura.
themis validate --repo ./mi-proyecto

# Ejecutar PRE-FLIGHT para un Planner.
themis run-cycle --role planner --mode roles-loop

# Ejecutar PRE-FLIGHT para un Executor.
themis run-cycle --role executor --mode roles-loop

# Usar un directorio de gobernanza personalizado.
themis init --repo ./mi-proyecto --base-dir governance
themis validate --repo ./mi-proyecto --base-dir governance
```

## Ejemplo 5: Verificación de límites de rol

```python
from core.roles import get_role

# Antes de permitir una modificación de código:
role = get_role("planner")
if not role.can_touch_code:
    print(f"BLOQUEADO: {role.name} no puede modificar código")
    print(f"Prohibido: {', '.join(role.forbidden)}")
    # Detener — no continuar.
```

## Ejemplo 6: Corte anti-catástrofe

```python
from core.loop import LoopOrchestrator

loop = LoopOrchestrator(cycle_id="2026-10-24T10:00:00Z")

files_to_modify = ["a.py", "b.py", "c.py", "d.py", "e.py", "f.py"]
if len(files_to_modify) > 5:
    loop.trigger_anti_catastrophe("más de 5 archivos a modificar")
    print(loop.get_summary())
    # STOP: dividir la tarea en ciclos más pequeños.
```

## Proveedores de LLM soportados

Themis es **agnóstico del proveedor**. Funciona con cualquier LLM porque el
contrato de gobernanza se inyecta como texto (system prompt) y no depende del
proveedor.

| Proveedor | Método de integración |
|-----------|-----------------------|
| OpenAI | Inyección en system prompt |
| Anthropic | Inyección en system prompt |
| DeepSeek | Inyección en system prompt |
| Ollama (local) | Inyección en system prompt |
| Cualquier API compatible con OpenAI | Inyección en system prompt |

## Principio clave

**Themis no es una librería que se importa dentro del agente.** Es un
**protocolo** que se inyecta en el system prompt y se hace cumplir desde la capa
de orquestación. El paquete Python (`cli.py`, `core/`) provee herramientas para
validar y ejecutar el protocolo, pero el enforcement real ocurre a nivel de prompt.
