![Themis Banner](docs/assets/themis-banner.jpeg)

# ⚖️ Themis — Protocolo de Gobernanza Determinista para Agentes LLM

> **Rama principal (`main`) en español. Rama `english` con documentación traducida al inglés.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Andres34r7y4/themis/pulls)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/Andres34r7y4?style=social)](https://github.com/sponsors/Andres34r7y4)

Themis es un protocolo de gobernanza autónomo, determinístico y multi-rol para cualquier repositorio que utilice agentes basados en LLM. Su propósito es hacer **predecible el camino de la IA en producción** mediante pautas obligatorias que definen quién decide, quién ejecuta y quién audita.

---

## 🎯 El Problema

Los agentes LLM actuales operan como "caja negra": ejecutan comandos, modifican archivos y toman decisiones sin un marco de gobernanza estricto. Esto genera:
- ❌ Cambios no verificables en producción
- ❌ Falta de trazabilidad de quién tomó qué decisión
- ❌ Sin contención de daños ante errores
- ❌ Confusión entre roles de planificación, ejecución y auditoría

---

## ✅ La Solución: Themis

Themis introduce un **kernel de gobernanza** (`agent.md`) que el LLM debe consumir obligatoriamente antes de cualquier acción. Define un flujo de estados cerrado y obligatorio que garantiza previsibilidad.

### Características principales

| Característica | Descripción |
|--------------|-------------|
| 🔒 **PRE-FLIGHT Obligatorio** | Ningún agente actúa sin declarar ROLE, CYCLE_ID y MODE |
| 🏗️ **Separación de Roles** | Planner, Executor, Debugger, Security, QA, Architect, Documentator, DevOps, Product Owner |
| 🔄 **Loop de Estados** | PLANNER → EXECUTOR → STOP con fases controladas |
| ❄️ **Context Freeze** | Snapshots deterministas antes de ejecutar cambios |
| 🛡️ **Anti-catástrofe** | Bloqueo automático si una tarea toca >5 archivos o es no atómica |
| 📋 **Trazabilidad total** | Bitácora en `task-archives.md` con CYCLE_ID, archivos tocados y comandos reales |
| 🧩 **Agnóstico** | Funciona con cualquier LLM (OpenAI, Anthropic, DeepSeek, Ollama, etc.) |

---

## 📁 Estructura del Repositorio

```
themis/
├── .github/
│   ├── FUNDING.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── assets/
│   │   └── themis-banner.jpeg      # Imagen de portada oficial
│   ├── ARCHITECTURE.md             # Diagrama Mermaid del state machine
│   ├── EXAMPLES.md                 # Ejemplos de integración con LLMs
│   ├── SECURITY.md                 # Política de seguridad
│   └── guia-uso.md                 # Guía operativa
├── themis/
│   ├── agent.md                    # Kernel de gobernanza (contrato central)
│   ├── PATHS.md                    # Fuente única de rutas del sistema
│   ├── loops/
│   │   ├── roles-loop.md           # Orquestación de estados y fases
│   │   ├── context-freeze.md       # Congelación de contexto
│   │   └── memory-loop.md          # Bucle de memoria y trazabilidad
│   ├── roles/
│   │   ├── planner.md              # Rol: Planeador
│   │   ├── executor.md             # Rol: Ejecutor
│   │   ├── debugger.md             # Rol: Depurador
│   │   ├── security_engineer.md    # Rol: Seguridad
│   │   ├── architect.md            # Rol: Arquitecto
│   │   ├── qa_engineer.md          # Rol: QA
│   │   ├── documentator.md         # Rol: Documentador
│   │   ├── devops_engineer.md      # Rol: DevOps
│   │   ├── product_owner.md        # Rol: Product Owner
│   │   └── disenador.md            # Rol: Diseñador
│   ├── tasks/
│   │   ├── tasks.md                # Tareas activas del ciclo
│   │   └── archives/
│   │       └── task-archives.md    # Bitácora de tareas completadas
│   └── templates/
│       ├── prompt-inicial.md       # Prompt de inicialización
│       ├── run-roles-loop.md       # Ejecución del loop de roles
│       ├── template-task.md        # Plantilla de tarea
│       └── template-backlog.md     # Plantilla de backlog
├── cli.py                          # CLI de gobernanza
├── core/
│   ├── __init__.py
│   ├── kernel.py                   # Motor PRE-FLIGHT
│   ├── roles.py                    # Registro de 10 roles
│   └── loop.py                     # Orquestador de estados
├── LICENSE                         # Licencia MIT
├── README.md                       # Este archivo
├── CONTRIBUTING.md                 # Guía de contribución
├── CHANGELOG.md                    # Registro de cambios
└── pyproject.toml                  # Empaquetado Python
```

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone git@github.com:Andres34r7y4/themis.git
cd themis
```

### 2. Leer el Kernel de Gobernanza

El archivo `themis/agent.md` es el **contrato central**. Todo agente debe leerlo antes de actuar:

```markdown
# PRE-FLIGHT (OBLIGATORIO)
Antes de realizar cualquier acción o respuesta, el agente DEBE:
1) Identificar y declarar: ROLE, CYCLE_ID, MODE
2) Leer y obedecer estrictamente: agent.md → roles-loop.md → roles/<ROL>.md
3) Imprimir: PRE-FLIGHT OK
```

### 3. Ejecutar un ciclo de gobernanza

1. **PLANNER_PHASE**: El Planner descompone el objetivo en tareas atómicas en `tasks.md`
2. **EXECUTOR_PHASE**: El Executor implementa SOLO lo definido en `tasks.md`
3. **STOP**: El ciclo termina cuando las tareas están completadas o se alcanza el límite de 3 tareas por ciclo

---

## 🏛️ Roles y Responsabilidades

| Rol | Responsabilidad Principal | Puede tocar código |
|-----|--------------------------|-------------------|
| **Planner** | Descompone objetivos, define backlog y tareas atómicas | ❌ No |
| **Executor** | Implementa cambios mínimos y verificables | ✅ Sí (solo tasks.md) |
| **Debugger** | Diagnostica bugs, produce evidencia, no aplica fixes definitivos | ❌ No |
| **Security Engineer** | Valida seguridad en todo ciclo con cambios | ❌ No (solo veto) |
| **QA Engineer** | Valida aceptación pre-STOP en ciclos con código | ❌ No (solo veto) |
| **Architect** | Gate cuando el ciclo toca estructura, contratos o dependencias | ❌ No (solo veto) |
| **Documentator** | Valida documentación del entregable | ❌ No (solo veto) |
| **DevOps** | Gate de hooks, pipeline, worktrees y rollback | ❌ No (solo veto) |
| **Product Owner** | Gate pre-planificación (valor y aceptación) | ❌ No (solo veto) |
| **Diseñador** | Propone lo visual con criterios medibles | ❌ No (solo veto) |

---

## 👤 Autor

**Andres Delgado** — Software Architect & AI Governance Specialist

- GitHub: [@Andres34r7y4](https://github.com/Andres34r7y4)
- LinkedIn: [andresdelgado-architect](https://www.linkedin.com/in/andresdelgado-architect/)
- Repositorio: [themis](https://github.com/Andres34r7y4/themis)

---

## 💖 Soporte y Donaciones

¿Te gusta el proyecto? Considera sponsorear el desarrollo:

[![GitHub Sponsors](https://img.shields.io/github/sponsors/Andres34r7y4?style=for-the-badge&logo=github)](https://github.com/sponsors/Andres34r7y4)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/andresdelgado)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-Donate-orange.svg?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/andres34r7y4)

---

## 📜 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Puedes usarlo, modificarlo y distribuirlo libremente en proyectos personales y comerciales.

---

## 🤝 Contribuir

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para conocer las reglas de contribución, el flujo de trabajo y cómo enviar Pull Requests.

---

## 📊 Versiones

Consulta [CHANGELOG.md](CHANGELOG.md) para ver el historial de cambios y versiones.

---

## 🔒 Seguridad

Consulta [docs/SECURITY.md](docs/SECURITY.md) para conocer nuestra política de seguridad y cómo reportar vulnerabilidades.

---

<div align="center">

**Themis** — Gobernanza determinista para la IA.  
Hecho con ⚖️ para sistemas predecibles.

</div>
