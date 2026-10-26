# Registro de Cambios — Themis

## [v1.1.0] — 2026-10-25

### 🧰 Herramientas y empaquetado

- `themis init` funcional: crea la estructura completa de gobernanza en cualquier
  repositorio, con soporte para `--base-dir` y `--force`.
- `themis validate` y `themis run-cycle` ahora respetan `--base-dir`.
- CLI estándar con `argparse`, `--version`, `--help` y códigos de salida consistentes.
- `pyproject.toml` empaqueta `cli.py` y los activos de `themis`, por lo que el
  comando instalado `themis` funciona.
- La versión mínima de Python pasa a 3.10, en línea con los type hints usados.
- Se agrega una suite de tests con `unittest` y CI de GitHub Actions (Python 3.10–3.12).

### 🛠️ Kernel y roles

- Se corrige la transición `STOP → STOP` y el estado de anti-catástrofe.
- `PLANNER_PHASE` ahora puede pasar a `DEBUGGER_PHASE` y `DESIGNER_PHASE`, igual
  que la máquina de estados documentada.
- Se unifican los roles en `themis/roles/designer.md`; se elimina el duplicado
  `disenador.md` y las referencias contaminadas de otro proyecto (`AGENTS.md`,
  `UI_GOVERNANCE.md`).
- Se estandarizan los diez documentos de rol con la misma estructura: misión,
  PRE-FLIGHT, responsabilidades, límites, entradas, salidas, handoff y checklist.

### 📚 Documentación

- `agent.md`, loops, roles, plantillas y guía de uso alineados con el contrato ampliado.
- Se corrigen rutas obsoletas en `PATHS.md` (`themis/templates/`, rutas reales de docs).
- README reescrito con estructura exacta, referencia del CLI, badges, autor y donaciones.
- `docs/EXAMPLES.md` importa el paquete real `core` y refleja el CLI funcional.
- `docs/SECURITY.md`, plantillas de issues y PR traducidas al inglés en la rama `english`.

### 🔗 Autor y soporte

- Se agregan enlaces de autor y redes: GitHub, LinkedIn y repositorio.
- Se agregan donaciones: GitHub Sponsors, PayPal y Buy Me a Coffee.

## [v1.0.0] — 2026-10-24

### 🚀 Lanzamiento inicial

- **Kernel de gobernanza**: `agent.md` con PRE-FLIGHT obligatorio y separación de roles.
- **Loop de orquestación**: `roles-loop.md` con estados `PLANNER_PHASE`,
  `EXECUTOR_PHASE`, `DEBUGGER_PHASE`, `DESIGNER_PHASE`, `STOP`.
- **Roles definidos**: Planner, Executor, Debugger, Security Engineer, Architect,
  QA Engineer, Documentator, DevOps, Product Owner, Designer.
- **Contexto congelado**: `context-freeze.md` para snapshots deterministas.
- **Bucle de memoria**: `memory-loop.md` para trazabilidad de ejecuciones.
- **Plantillas**: task, backlog, prompt inicial y run-roles-loop.
- **Guía de uso**: documentación operativa completa.
- **Imagen de portada**: banner oficial en `docs/assets/themis-banner.jpeg`.
- **Multilingüe**: rama `main` en español (default), rama `english` en inglés.

## Próximos pasos

- Publicar ambas ramas y mantener la documentación inglesa sincronizada con `main`.
- Agregar ejemplos de integración para SDKs específicos (OpenAI, Anthropic,
  DeepSeek, Ollama) sobre la inyección de prompt agnóstica.
- Ampliar la suite con tests de integración para un repositorio inicializado.
