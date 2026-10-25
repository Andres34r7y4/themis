# Registro de Cambios — Themis

## [v1.0.0] — 2026-10-24

### 🚀 Lanzamiento inicial

- **Kernel de gobernanza**: `agent.md` con PRE-FLIGHT obligatorio y separación de roles.
- **Loop de orquestación**: `roles-loop.md` con estados `PLANNER_PHASE`, `EXECUTOR_PHASE`, `DEBUGGER_PHASE`, `DISENADOR_PHASE`, `STOP`.
- **Roles definidos**: Planner, Executor, Debugger, Security Engineer, Architect, QA Engineer, Documentator, DevOps, Product Owner, Diseñador.
- **Contexto congelado**: `context-freeze.md` para snapshots deterministas.
- **Bucle de memoria**: `memory-loop.md` para trazabilidad de ejecuciones.
- **Plantillas**: templates de task, backlog, prompt inicial y run-roles-loop.
- **GUIA de uso**: Documentación operativa completa.
- **Imagen de portada**: Banner oficial en `docs/assets/themis-banner.jpeg`.
- **Multilingüe**: Rama `main` en español (default), rama `english` en inglés.

## Próximos pasos

- Versión en inglés de toda la documentación.
- Ejemplos de integración con proveedores LLM (OpenAI, Anthropic, DeepSeek, Ollama).
- CLI de inicialización de gobernanza (`themis init`).
