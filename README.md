![Themis Banner](docs/assets/themis-banner.jpeg)

# ⚖️ Themis — Deterministic Governance Protocol for LLM Agents

> **Default branch (`main`) in Spanish. Branch `english` with documentation translated to English.**

Themis is an autonomous, deterministic, multi-role governance protocol for any repository using LLM-based agents. Its purpose is to make **the AI's path in production predictable** through mandatory guidelines that define who decides, who executes, and who audits.

---

## 🎯 The Problem

Current LLM agents operate as a "black box": they execute commands, modify files, and make decisions without a strict governance framework. This generates:
- ❌ Unverifiable changes in production
- ❌ Lack of traceability of who made which decision
- ❌ No damage containment on errors
- ❌ Confusion between planning, execution, and auditing roles

---

## ✅ The Solution: Themis

Themis introduces a **governance kernel** (`agent.md`) that the LLM must consume obligatorily before any action. It defines a closed and mandatory state flow that guarantees predictability.

### Key Features

| Feature | Description |
|---------|-------------|
| 🔒 **Mandatory PRE-FLIGHT** | No agent acts without declaring ROLE, CYCLE_ID, and MODE |
| 🏗️ **Role Separation** | Planner, Executor, Debugger, Security, QA, Architect, Documentator, DevOps, Product Owner |
| 🔄 **State Loop** | PLANNER → EXECUTOR → STOP with controlled phases |
| ❄️ **Context Freeze** | Deterministic snapshots before executing changes |
| 🛡️ **Anti-Catastrophe** | Automatic blocking if task touches >5 files or is non-atomic |
| 📋 **Full Traceability** | Log in `task-archives.md` with CYCLE_ID, files touched, and real commands |
| 🧩 **Agnostic** | Works with any LLM (OpenAI, Anthropic, DeepSeek, Ollama, etc.) |

---

## 📁 Repository Structure

```
themis/
├── docs/
│   └── assets/
│       └── themis-banner.jpeg      # Official banner image
├── themis/
│   ├── agent.md                    # Governance kernel (central contract)
│   ├── PATHS.md                    # Single source of system paths
│   ├── loops/
│   │   ├── roles-loop.md           # State and phase orchestration
│   │   ├── context-freeze.md       # Context freezing
│   │   └── memory-loop.md          # Memory loop and traceability
│   ├── roles/
│   │   ├── planner.md              # Role: Planner
│   │   ├── executor.md             # Role: Executor
│   │   ├── debugger.md             # Role: Debugger
│   │   ├── security_engineer.md    # Role: Security Engineer
│   │   ├── architect.md            # Role: Architect
│   │   ├── qa_engineer.md          # Role: QA Engineer
│   │   ├── documentator.md         # Role: Documentator
│   │   ├── devops_engineer.md      # Role: DevOps Engineer
│   │   ├── product_owner.md        # Role: Product Owner
│   │   └── disenador.md            # Role: Designer
│   ├── tasks/
│   │   ├── tasks.md                # Active cycle tasks
│   │   └── archives/
│   │       └── task-archives.md    # Completed tasks log
│   └── templates/
│       ├── prompt-inicial.md       # Initialization prompt
│       ├── run-roles-loop.md       # Roles loop execution
│       ├── template-task.md        # Task template
│       └── template-backlog.md     # Backlog template
├── LICENSE                         # MIT License
├── README.md                       # This file
├── CONTRIBUTING.md                 # Contribution Guide
└── CHANGELOG.md                    # Change Log
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/themis.git
cd themis
```

### 2. Read the Governance Kernel

The file `themis/agent.md` is the **central contract**. Every agent must read it before acting:

```markdown
# PRE-FLIGHT (MANDATORY)
Before taking any action or response, the agent MUST:
1) Identify and declare: ROLE, CYCLE_ID, MODE
2) Read and strictly obey: agent.md → roles-loop.md → roles/<ROLE>.md
3) Print: PRE-FLIGHT OK
```

### 3. Execute a governance cycle

1. **PLANNER_PHASE**: Planner decomposes objective into atomic tasks in `tasks.md`
2. **EXECUTOR_PHASE**: Executor implements ONLY what is defined in `tasks.md`
3. **STOP**: Cycle ends when tasks are complete or max 3 tasks per cycle reached

---

## 🏛️ Roles and Responsibilities

| Role | Main Responsibility | Can touch code |
|------|---------------------|----------------|
| **Planner** | Decomposes objectives, defines backlog and atomic tasks | ❌ No |
| **Executor** | Implements minimal and verifiable changes | ✅ Yes (only tasks.md) |
| **Debugger** | Diagnoses bugs, produces evidence, does not apply definitive fixes | ❌ No |
| **Security Engineer** | Validates security in all cycles with changes | ❌ No (veto only) |
| **QA Engineer** | Validates acceptance pre-STOP in code cycles | ❌ No (veto only) |
| **Architect** | Gate when cycle touches structure, contracts, or dependencies | ❌ No (veto only) |
| **Documentator** | Validates deliverable documentation | ❌ No (veto only) |
| **DevOps** | Gate of hooks, pipeline, worktrees, and rollback | ❌ No (veto only) |
| **Product Owner** | Gate pre-planning (value and acceptance) | ❌ No (veto only) |
| **Designer** | Proposes visual with measurable criteria | ❌ No (veto only) |

---

## 📜 License

This project is under the [MIT](LICENSE) license. You can use, modify, and distribute it freely in personal and commercial projects.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, workflow, and how to submit Pull Requests.

---

## 📊 Versions

See [CHANGELOG.md](CHANGELOG.md) for change history and versions.

---

<div align="center">

**Themis** — Deterministic governance for AI.  
Made with ⚖️ for predictable systems.

</div>
