# Themis User Guide

## Mandatory principle

Before any agent action or response, read and obey the central contract in
`themis/agent.md`, then the loop rules and the active role document.

## Purpose

`themis/` centralizes the contract, roles, loops, tasks, and AI outputs needed to
run controlled cycles with traceability, minimal changes, and security.

## Installation

```bash
# From a clone (editable install)
python -m pip install -e .
themis --version

# Or run without installing
python cli.py --help
```

## Quick start

```bash
# Scaffold governance into a repository
themis init --repo ./my-project

# Validate the structure
themis validate --repo ./my-project

# Run PRE-FLIGHT for a role
themis run-cycle --role planner --repo ./my-project
```

`themis init` copies the governance assets into `<repo>/themis` and refuses to
overwrite them unless `--force` is passed. Use `--base-dir` to choose a
different directory name.

## Operation modes

### 1) Normal cycle (feature / improvement / analysis)

Starts in `PLANNER_PHASE` and follows `roles-loop` until `STOP`.

### 2) Bug / diagnosis cycle

Starts in `DEBUGGER_PHASE` when the symptom is clear. The Debugger produces
evidence; the Executor implements only with a prior report.

### 3) Task-only execution

When the user explicitly says "only execute tasks.md", start in
`EXECUTOR_PHASE`.

### 4) Backlog → Tasks

The Planner generates a backlog from documentation and converts at most three
priority tasks to `tasks.md`.

### 5) Index-first

Use the repository index under `themis/outputs/repo_index/` for quick inspection
without massive file reading.

## Workflow (high level)

1. **Pre-flight**: read `agent.md`, `roles-loop.md`, and the active role; print
   `PRE-FLIGHT OK`, `ROLE`, `MODE`, `CYCLE_ID`.
2. **PASS 1 (Understand)**: define the Freeze Map and the minimal plan.
3. **PASS 2 (Implement)**: minimal changes, only when applicable.
4. **PASS 3 (Verify)**: minimum verification per cycle type.
5. **Archive**: register the cycle in `task-archives.md` and clean `tasks.md`.

## Structure

```text
themis/
├── agent.md                 # Central governance contract
├── PATHS.md                 # Single source of paths
├── loops/
│   ├── roles-loop.md        # State machine and handoffs
│   ├── context-freeze.md    # Minimum scope per cycle
│   └── memory-loop.md       # Controlled persistence
├── roles/                   # Ten role contracts
├── tasks/
│   ├── tasks.md             # Active tasks
│   └── archives/            # Completed cycle log
├── templates/               # Task, backlog, and prompt templates
└── outputs/                 # Runtime reports (generated, not required)
```

## Planner task planning

The Planner must:

- read the relevant documentation;
- generate a backlog of at most 10 atomic tasks;
- prioritize by impact (desc), effort (asc), risk (asc), dependencies, and ID;
- convert at most 3 tasks per cycle to `tasks.md`;
- never touch code and never run domain commands.

## Security rules (summary)

- No exposing credentials or tokens.
- No adding dependencies without authorization.
- No modifying core adapters or base interfaces without an explicit task.
- No massive refactor, no moving folders, no renaming modules for "cleanup".
- No inventing data or assuming unverifiable tool output.
- Keep changes minimal and reversible.

## Extending the system with new roles

To add a role:

1. Add it to `themis/agent.md` and `core/kernel.py` (`VALID_ROLES`).
2. Create `themis/roles/<role>.md` and add it to `core/roles.py`.
3. Add it to `themis/loops/roles-loop.md` with states and handoffs.
4. Update `core/kernel.py` required files and the test suite.
5. Run `python -m unittest discover -s tests -v` and `python cli.py validate`.

## Quick planner checklist

- [ ] Read `themis/agent.md`
- [ ] Read `themis/loops/roles-loop.md`
- [ ] Read `themis/roles/planner.md`
- [ ] Did not touch code
- [ ] Did not execute domain commands
- [ ] Documented the flow and examples
