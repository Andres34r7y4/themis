![Themis Banner](docs/assets/themis-banner.jpeg)

# ⚖️ Themis — Protocolo de Gobernanza Determinista para Agentes LLM

> **Rama principal (`main`) en español. Rama `english` con documentación traducida al inglés.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Andres34r7y4/themis/pulls)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/Andres34r7y4?style=social)](https://github.com/sponsors/Andres34r7y4)
[![CI](https://github.com/Andres34r7y4/themis/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Andres34r7y4/themis/actions/workflows/ci.yml)

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
| 🏗️ **Separación de Roles** | Planner, Executor, Debugger, Security, QA, Architect, Documentator, DevOps, Product Owner, Diseñador |
| 🔄 **Loop de Estados** | PLANNER → EXECUTOR → STOP con fases controladas |
| ❄️ **Context Freeze** | Snapshots deterministas antes de ejecutar cambios |
| 🛡️ **Anti-catástrofe** | Bloqueo automático si una tarea toca >5 archivos o es no atómica |
| 📋 **Trazabilidad total** | Bitácora en `task-archives.md` con CYCLE_ID, archivos tocados y comandos reales |
| 🧩 **Agnóstico** | Funciona con cualquier LLM (OpenAI, Anthropic, DeepSeek, Ollama, etc.) |
| 🧰 **CLI incluido** | `themis init`, `themis validate` y `themis run-cycle` |

---

## 📁 Estructura del Repositorio

```
themis/
├── .github/
│   ├── FUNDING.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── config.yml
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml                  # CI: tests + validate + install
├── docs/
│   ├── assets/
│   │   └── themis-banner.jpeg      # Imagen de portada oficial
│   ├── ARCHITECTURE.md             # Diagrama Mermaid del state machine
│   ├── EXAMPLES.md                 # Ejemplos de integración con LLMs
│   ├── MULTI_MODEL_CONFIG.md     # Configuración un modelo vs varios modelos con orquestador
│   ├── SECURITY.md                 # Política de seguridad
│   ├── TOKEN_EFFICIENCY_ROI.md   # Benchmark de eficiencia de tokens y ROI
│   └── guia-uso.md                 # Guía operativa
├── scripts/
│   └── token_benchmark.py        # Medición de eficiencia de tokens y ROI
├── sandbox/
│   ├── experiment.md             # Experimento de gobernanza (saludo parametrizado)
│   ├── target/
│   │   └── greeting.py           # Script mínimo gobernado por Themis
│   └── tasks/
│       ├── tasks.md              # Tareas activas del ciclo de sandbox
│       └── archives/
│           └── task-archives.md  # Bitácora del ciclo de sandbox
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
│   │   └── designer.md             # Rol: Diseñador
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
├── tests/
│   └── test_governance.py          # Tests de kernel, CLI, loop y roles
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
git clone https://github.com/Andres34r7y4/themis.git
cd themis
```

### 2. Instalar el CLI

```bash
python -m pip install -e .
themis --version
```

También puedes ejecutarlo sin instalar:

```bash
python cli.py --help
```

### 3. Inicializar la gobernanza en tu proyecto

```bash
themis init --repo ./mi-proyecto
themis validate --repo ./mi-proyecto
```

### 4. Leer el Kernel de Gobernanza

El archivo `themis/agent.md` es el **contrato central**. Todo agente debe leerlo antes de actuar:

```markdown
# PRE-FLIGHT (OBLIGATORIO)
Antes de realizar cualquier acción o respuesta, el agente DEBE:
1) Identificar y declarar: ROLE, CYCLE_ID, MODE
2) Leer y obedecer estrictamente: agent.md → roles-loop.md → roles/<ROL>.md
3) Imprimir: PRE-FLIGHT OK
```

### 5. Ejecutar un ciclo de gobernanza

1. **PLANNER_PHASE**: El Planner descompone el objetivo en tareas atómicas en `tasks.md`
2. **EXECUTOR_PHASE**: El Executor implementa SOLO lo definido en `tasks.md`
3. **STOP**: El ciclo termina cuando las tareas están completadas o se alcanza el límite de 3 tareas por ciclo

```bash
themis run-cycle --role planner
themis run-cycle --role executor
```

### Referencia rápida del CLI

| Comando | Descripción |
|---------|-------------|
| `themis init [--repo RUTA] [--base-dir NOMBRE] [--force]` | Crea la estructura de gobernanza |
| `themis validate [--repo RUTA] [--base-dir NOMBRE]` | Valida estructura y PRE-FLIGHT |
| `themis run-cycle --role ROL [--mode MODO] [--cycle-id ID]` | Ejecuta PRE-FLIGHT para un rol |

Códigos de salida: `0` éxito, `1` error de gobernanza/estructura, `2` uso inválido del CLI.

---

## 🤖 Un modelo o varios modelos con orquestador

Themis puede operar de dos formas, y ambas son compatibles porque el protocolo es **modelo-agnóstico**: no depende de OpenAI, Anthropic, DeepSeek ni Ollama, solo del system prompt.

### 1) Un solo modelo para todos los roles

Un mismo LLM actúa como Planner, Executor, Debugger o cualquier otro rol, cambiando de rol entre ciclos o dentro de un ciclo. Cada vez que el modelo actúa, inyecta `themis/agent.md` y el rol correspondiente en su system prompt, imprime `PRE-FLIGHT OK` y respeta los límites de ese rol (`can_touch_code`, `forbidden`, `write_reports`).

**Ventajas:** simplicidad, un solo proveedor, menor costo de integración.

### 2) Varios modelos con un orquestador (multi-modelo)

Un orquestador asigna cada rol a un modelo diferente. Por ejemplo:

| Rol | Modelo sugerido | Por qué |
|-----|-----------------|---------|
| Planner | Modelo con fuerte razonamiento | Descompone objetivos y define tareas atómicas |
| Executor | Modelo rápido y económico | Implementa solo lo que dice `tasks.md` |
| Debugger | Modelo analítico | Diagnostica y produce evidencia |
| Security Engineer / QA | Modelo especializado en validación | Veto y verificación determinística |
| Architect | Modelo con contexto largo | Revisa estructura, contratos y dependencias |

Cada modelo recibe solo el contrato de su rol (`themis/roles/<ROL>.md`) y ejecuta su fase. El orquestador coordina las transiciones entre `PLANNER_PHASE`, `EXECUTOR_PHASE`, `DEBUGGER_PHASE`, etc., y garantiza que `PRE-FLIGHT` se cumpla en cada cambio de modelo o rol.

Consulta [docs/MULTI_MODEL_CONFIG.md](docs/MULTI_MODEL_CONFIG.md) para ver cómo configurar ambos escenarios.

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

## 📊 Token Efficiency & ROI Benchmark

Themis incluye un marco de medición para validar, con datos reales, si el coste de tokens de la gobernanza se compensa con los errores evitados, la trazabilidad y la reducción de retrabajo.

### ¿Qué mide?

| Métrica | Qué revela |
|---------|------------|
| **Overhead de tokens por ciclo** | Tokens extra que consume la gobernanza (PRE-FLIGHT, roles, loops) frente a un agente sin gobernanza. |
| **Tokens ahorrados por Context Freeze** | Archivos que no se leen gracias al Freeze Map (solo lo necesario). |
| **Coste por ciclo (USD)** | Precio real según tu proveedor y modelo (OpenAI, Anthropic, DeepSeek, Ollama…). |
| **Errores evitados pre-ejecución** | Errores detectados por QA/Security antes de tocar código. |
| **Ciclos de retrabajo reducidos** | Tareas atómicas que evitan refactors y reejecuciones. |
| **ROI de gobernanza** | (Valor de incidentes evitados + retrabajo evitado + trazabilidad) / coste en tokens. |

### Fórmula de ROI

```text
ROI = Valor evitado (USD) / Coste de gobernanza (USD)

Valor evitado =
  (incidentes prevenidos × coste por incidente) +
  (ciclos de retrabajo evitados × coste por ciclo) +
  valor de trazabilidad y auditoría
```

- **ROI > 100 %**: la gobernanza se paga sola.
- **ROI >> 100 %**: genera ahorro neto.

### Cómo ejecutar el benchmark

```bash
# Modo simulación (sin API, con datos de ejemplo)
python scripts/token_benchmark.py --mode dry-run --output docs/benchmark-results.md

# Modo real con OpenAI (requiere OPENAI_API_KEY)
python scripts/token_benchmark.py --provider openai --model gpt-4o \
  --task "Validar un archivo de configuración JSON" \
  --output docs/benchmark-results.md
```

Consulta la documentación completa en [docs/TOKEN_EFFICIENCY_ROI.md](docs/TOKEN_EFFICIENCY_ROI.md) con la metodología, fórmula detallada, tabla de resultados esperada y checklist de lo que debe auditar un experto.

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
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue.svg?style=for-the-badge&logo=paypal)](https://paypal.me/34r7y4)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-Donate-orange.svg?style=for-the-badge&logo=buymeacoffee)](https://buymeacoffee.com/delgadoranv)

Conecta con el proyecto:

- GitHub: [@Andres34r7y4](https://github.com/Andres34r7y4)
- LinkedIn: [andresdelgado-architect](https://www.linkedin.com/in/andresdelgado-architect/)

---

## 📚 Documentación

- [Arquitectura](docs/ARCHITECTURE.md)
- [Ejemplos de integración](docs/EXAMPLES.md)
- [Guía de uso](docs/guia-uso.md)
- [Configuración multi-modelo](docs/MULTI_MODEL_CONFIG.md)
- [Benchmark de tokens y ROI](docs/TOKEN_EFFICIENCY_ROI.md)
- [Política de seguridad](docs/SECURITY.md)
- [Registro de cambios](CHANGELOG.md)

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
