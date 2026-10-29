# Configuración de Modelos — Themis

Este documento explica cómo configurar Themis para que funcione con **un solo modelo** o con **varios modelos asignados a diferentes roles** a través de un orquestador.

---

## Escenario A: Un solo modelo para todos los roles

En este modo, un mismo LLM asume todos los roles de Themis (Planner, Executor, Debugger, etc.), cambiando de rol entre ciclos o dentro de un ciclo.

### Flujo

1. El modelo lee `themis/agent.md` (contrato central).
2. Declara `ROLE`, `CYCLE_ID` y `MODE`.
3. Lee `themis/roles/<ROL>.md` para el rol activo.
4. Imprime `PRE-FLIGHT OK`.
5. Ejecuta solo lo permitido para ese rol.

### Configuración mínima

```python
from pathlib import Path

THEMIS_KERNEL = Path("themis/agent.md").read_text(encoding="utf-8")

def system_prompt_for_role(role: str) -> str:
    role_contract = Path(f"themis/roles/{role}.md").read_text(encoding="utf-8")
    return f"""
Sos un agente que opera bajo el Protocolo de Gobernanza Themis V1.

{THEMIS_KERNEL}

{role_contract}

Antes de CADA acción, debés:
1. Ejecutar PRE-FLIGHT: declarar ROLE, CYCLE_ID, MODE.
2. Leer agent.md -> roles-loop.md -> roles/<ROL>.md.
3. Imprimir "PRE-FLIGHT OK" con tu ROLE, MODE y CYCLE_ID.
4. Solo entonces continuar con las responsabilidades de tu rol.
"""
```

Puedes llamar a este prompt con cualquier proveedor (OpenAI, Anthropic, DeepSeek, Ollama, etc.) y cambiar el `role` entre llamadas.

---

## Escenario B: Varios modelos con un orquestador (multi-modelo)

Un orquestador externo asigna cada rol de Themis a un modelo diferente. Cada modelo solo conoce el contrato de su rol y ejecuta su fase correspondiente.

### Arquitectura propuesta

```text
Orquestador Themis
├── Modelo 1 (Planner)      → themis/roles/planner.md
├── Modelo 2 (Executor)     → themis/roles/executor.md
├── Modelo 3 (Debugger)     → themis/roles/debugger.md
├── Modelo 4 (Security QA)  → themis/roles/security_engineer.md
│                              themis/roles/qa_engineer.md
└── Modelo 5 (Architect)    → themis/roles/architect.md
```

### Responsabilidades del orquestador

1. **Enrutar por rol:** decidir qué modelo atiende cada fase (`PLANNER_PHASE`, `EXECUTOR_PHASE`, etc.).
2. **Inyectar contrato:** enviar `agent.md` + `roles-loop.md` + el `roles/<ROL>.md` correspondiente como system prompt.
3. **Imponer PRE-FLIGHT:** exigir que cada modelo imprima `PRE-FLIGHT OK` antes de actuar.
4. **Controlar transiciones:** mover el estado del loop (`roles-loop.md`) solo cuando el rol actual termine su trabajo.
5. **Agregar evidencia:** recopilar los reportes de cada modelo (`task-archives.md`, `debug_*.md`, `qa_*.md`, etc.).

### Ejemplo de orquestador (esqueleto en Python)

```python
from pathlib import Path
from typing import Dict, Optional

from core.kernel import GovernanceKernel
from core.loop import LoopOrchestrator


class MultiModelOrchestrator:
    def __init__(self, repo: str = "."):
        self.kernel = GovernanceKernel(Path(repo))
        self.loop = LoopOrchestrator(cycle_id=self._new_cycle_id())
        self.role_to_model: Dict[str, object] = {}  # rol -> cliente de modelo

    def register_model(self, role: str, model_client: object) -> None:
        """Asigna un modelo cliente a un rol de Themis."""
        self.role_to_model[role] = model_client

    def _build_prompt(self, role: str) -> str:
        kernel = Path("themis/agent.md").read_text(encoding="utf-8")
        loop = Path("themis/loops/roles-loop.md").read_text(encoding="utf-8")
        role_contract = Path(f"themis/roles/{role}.md").read_text(encoding="utf-8")
        return f"""{kernel}

{loop}

{role_contract}

Imprime obligatoriamente:
PRE-FLIGHT OK
ROLE: {role}
MODE: roles-loop
CYCLE_ID: {self.loop.cycle_id}
"""

    def run_cycle_for_role(self, role: str, user_input: str) -> str:
        """Ejecuta una fase del ciclo con el modelo asignado al rol."""
        if role not in self.role_to_model:
            raise ValueError(f"No hay modelo registrado para el rol: {role}")

        # PRE-FLIGHT validación de estructura
        self.kernel.pre_flight(role=role, mode="roles-loop")

        prompt = self._build_prompt(role) + f"\n\nEntrada del usuario:\n{user_input}"
        model = self.role_to_model[role]
        response = model.complete(system=prompt, user=user_input)

        # Aquí el orquestador podría parsear "PRE-FLIGHT OK" y validar
        # que el modelo respetó los límites de su rol antes de continuar.
        return response

    def _new_cycle_id(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def transition(self, new_phase: str, new_role: Optional[str] = None) -> None:
        self.loop.transition(new_phase, new_role=new_role)
```

### Registro de modelos ejemplo

```python
orch = MultiModelOrchestrator(repo=".")

# Asignar modelos a roles
orch.register_model("planner", modelo_razonamiento_fuerte)
orch.register_model("executor", modelo_rapido_barato)
orch.register_model("debugger", modelo_analitico)
orch.register_model("security_engineer", modelo_seguridad)
orch.register_model("qa_engineer", modelo_validacion)
orch.register_model("architect", modelo_contexto_largo)
```

---

## Comparativa rápida

| Característica | Un solo modelo | Varios modelos + orquestador |
|----------------|---------------|------------------------------|
| Complejidad | Baja | Media/Alta |
| Costo | Un solo proveedor | Varios proveedores, costo por rol |
| Especialización | Generalista | Cada modelo optimizado para su rol |
| Control de límites | El mismo modelo se autorregula | El orquestador impone límites por rol |
| Ideal para | Proyectos pequeños o pilotos | Producciones complejas con roles críticos |

---

## Requisitos comunes (ambos escenarios)

1. **No hardcodear proveedores:** Themis no importa ni depende de ningún SDK de LLM específico.
2. **PRE-FLIGHT obligatorio:** cualquier modelo, sea uno o varios, debe imprimir `PRE-FLIGHT OK` antes de actuar.
3. **Límites de rol respetados:** un modelo asignado a `planner` no debe escribir código; un modelo asignado a `executor` no debe redefinir requisitos.
4. **Contratos versionados:** `agent.md`, `roles-loop.md` y los archivos de `themis/roles/` viven en Git y se versionan junto al código.
