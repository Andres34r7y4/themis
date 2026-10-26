# roles-loop.md — Planner ↔ Executor Orchestration (V1)

## 0) Pre-flight (MANDATORY)

Before any action, the system MUST:

1) Read `./themis/agent.md`
2) Read `./themis/loops/roles-loop.md`
3) Read `./themis/roles/<ROLE>.md` for the active role
4) Print a status line:
   - `PRE-FLIGHT OK`
   - `ROLE: <role>`
   - `MODE: roles-loop`
   - `CYCLE_ID: <id>`

Hard rule:

- If there is a conflict between `roles-loop` / `roles/*` and `agent.md`, **`agent.md` prevails**.

---

## 1) Loop states

Valid states:

- `PLANNER_PHASE`
- `DEBUGGER_PHASE`
- `DESIGNER_PHASE`
- `EXECUTOR_PHASE`
- `STOP`

The system starts in:

- `PLANNER_PHASE` for normal cycles (`feature`, `backlog`, `analysis`)
- `DEBUGGER_PHASE` if the user explicitly indicates a cycle of type `bug`, `diagnosis`, or `dynamic_analysis` and a sufficiently defined symptom already exists
- `DESIGNER_PHASE` if the cycle is of type `design` or the task carries a visual brief
- `PLANNER_PHASE` if the bug still needs decomposition or clarification before diagnosis
- `EXECUTOR_PHASE` only if the user explicitly says "only execute tasks.md"

### Allowed transitions

| From | To |
|------|----|
| `PLANNER_PHASE` | `EXECUTOR_PHASE`, `DEBUGGER_PHASE`, `DESIGNER_PHASE`, `STOP` |
| `EXECUTOR_PHASE` | `PLANNER_PHASE`, `STOP` |
| `DEBUGGER_PHASE` | `EXECUTOR_PHASE`, `PLANNER_PHASE`, `STOP` |
| `DESIGNER_PHASE` | `EXECUTOR_PHASE`, `PLANNER_PHASE`, `STOP` |
| `STOP` | terminal |

---

## 2) Canonical inputs / outputs

### Planner

Reads:

- `themis/objective.md` (if it exists)
- `./themis/tasks/tasks.md`
- optional backlog/improvement notes in `themis/outputs/ia/reports/backlog_mejoras.md`

Writes:

- `./themis/tasks/tasks.md` (max 3 tasks per cycle, following the template)
- optional planning notes under `themis/outputs/ia/planner/`

### Debugger

Reads:

- `./themis/tasks/tasks.md` (if an active cycle exists)
- previous Planner report (if it exists)
- the real repository (real files)
- `repo_index` / structural outputs if they exist
- the symptom declared by the user or the Planner

Writes:

- `./themis/outputs/ia/reports/debug_<CYCLE_ID>.md` (mandatory report)
- optional minimum traces or temporary diagnostic changes, only if the contract and the cycle allow them

### Designer

Reads:

- `./themis/tasks/tasks.md` (visual brief of the cycle)
- current tokens/themes and brief references
- the real repository (only what the brief reaches)

Writes:

- `./themis/outputs/ia/reports/design_<CYCLE_ID>.md` (mandatory report + veto)
- optional proposals with measurable criteria and tokens (no implementation unless authorized)

### Executor

Reads:

- `./themis/tasks/tasks.md` (the ONLY source of tasks)
- the real repository (real files)

Writes:

- minimal code changes (only to satisfy `tasks.md`)
- `./themis/tasks/archives/task-archives.md` (mandatory log)
- updates `./themis/tasks/tasks.md` by removing completed tasks

---

## 3) Planner rules (`PLANNER_PHASE`)

Goal: convert objectives/backlog into atomic tasks.

Checklist:

1) Do NOT touch code.
2) Do NOT run the smoke test.
3) Create/update `tasks.md`:
   - ordered by priority: **high impact + low effort** first
   - then high+medium, high+high, medium+low, medium+medium, low+*
4) Each task must include:
   - impact: `high | medium | low`
   - effort: `low | medium | high`
   - definition of done
   - probable files to touch (only when inferable without inventing)

Handoff condition:

- If `tasks.md` has at least 1 task, move to `EXECUTOR_PHASE`.
- If `tasks.md` is empty, move to `STOP`.

---

## 4) Debugger rules (`DEBUGGER_PHASE`)

Goal: diagnose bugs without implementing definitive fixes and produce usable evidence.

Checklist:

1) Do NOT refactor.
2) Do NOT make permanent logic changes without explicit authorization.
3) Align the symptom:
   - expected
   - observed
   - context
   - scope
4) Formulate between 2 and 5 verifiable hypotheses.
5) Generate `debug_<CYCLE_ID>.md` with:
   - symptom
   - problem area
   - hypotheses
   - evidence collected
   - recommended minimal next step
   - explicit diagnosis or `inconclusive`

Handoff condition:

- Move to `EXECUTOR_PHASE` only when the evidence identifies a concrete, minimal, reversible action.
- Return to `PLANNER_PHASE` when the fix requires decomposition.
- Move to `STOP` when the bug is blocked or requires a human decision.

---

## 5) Designer rules (`DESIGNER_PHASE`)

Goal: propose visual solutions with measurable criteria before any implementation.

Checklist:

1) Do NOT implement the redesign without task authorization.
2) Require a minimum brief: objective, audience/context, restrictions, references.
3) Research first (real references and theory) without drawing yet.
4) Propose at most 2 variants plus 1 recommendation.
5) Define measurable criteria (contrast, spacing, hierarchy, accessibility, performance).
6) Generate `design_<CYCLE_ID>.md` with the proposal, criteria, and veto when applicable.

Handoff condition:

- Move to `EXECUTOR_PHASE` when a variant is approved and the implementation is authorized.
- Return to `PLANNER_PHASE` when the brief is incomplete or splits are needed.
- Move to `STOP` when the brief is blocked.

---

## 6) Executor rules (`EXECUTOR_PHASE`)

Goal: implement atomic tasks with minimal, verifiable changes.

Checklist:

1) Implement ONLY what is in `tasks.md`.
2) Maximum 3 tasks per cycle.
3) Respect the Context Freeze and the Anti-Catastrophe limits.
4) Do not add dependencies without explicit authorization.
5) Run the minimum verification required by `agent.md` section 6.
6) Archive completed tasks in `task-archives.md`.
7) Remove completed tasks from `tasks.md`.

Handoff condition:

- Return to `PLANNER_PHASE` if a new cycle is needed.
- Move to `STOP` when `tasks.md` is empty or the cycle limit is reached.

---

## 7) Mandatory gates before STOP

Depending on the cycle type, the following gates apply (see each role document):

| Gate | Role | Blocks |
|------|------|--------|
| Security | Security Engineer | Any unsafe execution |
| Quality | QA Engineer | STOP without passing verification |
| Architecture | Architect | Structural changes without approval |
| Documentation | Documentator | STOP without updated docs |
| Deployment | DevOps Engineer | Pipeline-breaking changes |
| Value | Product Owner | Low-value task candidates |
| Visual | Designer | Unauthorized visual changes |

Veto precedence: `security > qa > architect > designer > documentator > devops > product_owner`.

---

## 8) Verification and budget

Mandatory roles per cycle: **Planner** (decomposes), **Executor** (executes one step at a time), **QA Engineer** (deterministic check: tests, validation, typecheck — never just "looks good").

1) **Evidence before STOP**: no cycle closes without a check executed by code (green suite, `themis validate`, or an honest documented limitation).
2) **Loop budget**: maximum 2 Executor → review rounds; on the third, escalate to the human with the disagreement in writing.
3) **Communicative dehallucination**: if the Executor lacks plan data, ask the corresponding role BEFORE inventing it.
4) **Minimum privilege per role**: each role only touches its artifacts (Planner: tasks/plan; Executor: code and log; Debugger: reports). Never put keys or secrets in artifacts.

---

## 9) Anti-catastrophe

Stop and return to planning when any of these is detected:

- more than 5 files to modify
- structural refactor
- unauthorized architecture change
- ambiguous or non-atomic task

Record the block in `task-archives.md` and propose smaller tasks.

---

## 10) STOP

The cycle ends when:

- `tasks.md` is empty
- the maximum of 3 tasks per cycle is reached
- a gate vetoes the cycle
- an anti-catastrophe condition is triggered
- the human requests it

Before STOP:

1) Archive completed work.
2) Record verification evidence.
3) Leave `tasks.md` in a consistent state.
