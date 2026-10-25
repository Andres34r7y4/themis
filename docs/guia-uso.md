# Guía de Uso del Sistema Themis (EN)

## Principio Obligatorio
Before any agent action or response, read and obey the central contract in `/themis/agent.md` and then the loop rules and corresponding role.

## Purpose of Core
`themis/` centralizes the contract, roles, loops, tasks, and AI outputs to execute controlled cycles with traceability, minimal changes, and security.

## Operation Modes

### 1) Normal Cycle (feature / improvement / analysis)
Starts in `PLANNER_PHASE` and follows `roles-loop` until `STOP`.

### 2) Bug / Diagnosis Cycle
Starts in `DEBUGGER_PHASE` when symptom is clear. Debugger produces evidence and Executor only implements with prior report.

### 3) Only task execution
When user explicitly says "only execute tasks.md", start in `EXECUTOR_PHASE`.

### 4) Backlog → Tasks
Planner generates backlog from documentation and converts priority tasks to `tasks.md`.

### 5) Index-first
Use repo index in `/themis/outputs/repo_index/` for quick inspection (without massive file reading).

## Workflow (High Level)
1. **Pre-flight**: Read `agent.md`, `roles-loop.md`, and active role; print `PRE-FLIGHT OK`, `ROLE`, `MODE`, `CYCLE_ID`.
2. **PASS 1 (Understand)**: Define Freeze Map and minimal plan.
3. **PASS 2 (Implement)**: Minimal changes (only if applicable).
4. **PASS 3 (Verify)**: Minimum verification per cycle type.
5. **Archive**: Register in `task-archives.md` and clear `tasks.md`.

## Non-invasive Tests (documentary, no execution)
Verify key routes exist:
- `/themis/agent.md`
- `/themis/loops/roles-loop.md`
- `/themis/roles/`
- `/themis/tasks/tasks.md`
- `/themis/tasks/archives/task-archives.md`

## Planner Task Planning
The Planner must:
- Read relevant documentation (if applicable).
- Generate backlog (max 10 atomic tasks).
- Prioritize by contract (impact ↓, effort ↑, risk ↑, dependencies).
- Convert to `tasks.md` (max 3 tasks per cycle).
- NO touching code.
- NO executing domain commands.

## Security Rules (Summary)
- No exposing credentials or tokens.
- No adding dependencies without authorization.
- No modifying core adapters or base interfaces without explicit task.
- No massive refactor, NO moving folders, NO renaming modules for "cleanup".
- No inventing data or assuming unverifiable tool outputs.
- Maintain minimal and reversible changes.

## Extending System with New Roles
To add a role:
1. Update `/themis/agent.md` declaring the role and its limits.
2. Create `/themis/roles/<role>.md`.
3. Update `/themis/loops/roles-loop.md` with states and handoffs.
4. Ensure pre-flight and central contract precedence.

## Quick Planner Checklist (documentation cycle)
- [ ] Read `/themis/agent.md`
- [ ] Read `/themis/loops/roles-loop.md`
- [ ] Read `/themis/roles/planner.md`
- [ ] Did not touch code
- [ ] Did not execute domain commands
- [ ] Documented flow and examples
