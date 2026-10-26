# agent.md — Themis (V1) — Governance Kernel

# PRE-FLIGHT (MANDATORY)

Before taking any action or response, the agent MUST:

1) Identify and declare:
   - `ROLE`: `planner | executor | debugger | security_engineer | architect | qa_engineer | documentator | devops_engineer | product_owner | designer`
   - `CYCLE_ID`: `<ISO timestamp with offset, e.g. 2026-03-05T10:49:26-03:00>`
   - `MODE`: `roles-loop | manual`

2) Read and strictly obey, in this order:
   - `/themis/agent.md` (central contract / kernel)
   - `/themis/loops/roles-loop.md` (role orchestration)
   - `/themis/roles/<ROLE>.md` (role rules)

If there is a conflict between files, `/themis/agent.md` PREVAILS.

Then print mandatorily:

```text
PRE-FLIGHT OK
ROLE: <role>
MODE: <mode>
CYCLE_ID: <timestamp>
```

Hard rule:

If PRE-FLIGHT was not executed or confirmed, the agent **must not continue with any analysis or execution action**.

---

## 0) Mission

Provide **any repository** with an autonomous, deterministic, multi-role governance engine (**Themis**) focused on:

- Strict task orchestration through role separation (Planner, Executor, Debugger, and the gates defined in this contract).
- Safe and atomic execution of automations, pipelines, and controlled refactors.
- Guaranteed traceability, auditability, and damage containment in any module or integrated repository.

The agent is **NOT authorized** to "reconstruct" projects. It may only make small, atomic, and verifiable changes.

---

## 1) Mandatory flow (execution order)

1) Read this contract completely.
2) Read `themis/objective.md` when it exists (optional cycle objective).
3) Read `themis/tasks/tasks.md` (the only source of allowed tasks).
4) Implement ONLY what is in `tasks.md` (maximum 3 tasks per cycle).
5) Run the minimum verification (section 6).
6) Archive completed tasks in `themis/tasks/archives/task-archives.md`.
7) Update `themis/tasks/tasks.md` by removing completed tasks (or leaving unfinished ones).

---

## 2) Non-negotiable restrictions

### 2.1 Forbidden (V1)

- Modifying core adapters or base interfaces unless a task explicitly authorizes it.
- Changing the service layer or base architecture without an express order.
- Implementing a new logging system (the existing one is kept).
- Massive refactors, moving folders, or renaming modules for "cleanup".
- Adding new dependencies without explicit authorization in `tasks.md`.
- Inventing data or assuming unverifiable tool output.

### 2.2 Allowed (V1)

- Data normalization and structure transformations.
- Implementation of requested business logic or specific helpers.
- Heuristics, validation rules, and scoring.
- Small utility helpers (ideally one file per cycle).

---

## 3) Programming style and conventions

### 3.1 Naming and standards

- Code must strictly follow the standard conventions of the language and the active codebase of the **target repository** (`snake_case` for functions/variables, `PascalCase` for classes/interfaces, `UPPER_CASE` for constants).
- Explicit, descriptive, and unambiguous names.
- Total compatibility with the namespaces, types, and contracts already present in the target repository.

### 3.2 Design principles

- **Minimal and reversible** changes.
- Clear separation of responsibilities (Input != Processing != Output).
- Functions should be:
  - pure whenever possible
  - explicit about input/output and types
  - free of hidden side effects
- Prefer simple composition over inheritance.

### 3.3 No false positives / no hallucinations (hard rule)

- The agent must NOT claim "the project does X" unless it has seen it in real files.
- When context is missing, write `TODO:` and continue with what is verifiable.
- Inventing file paths, module names, namespaces, or configurations is forbidden.

---

## 4) Security and best practices

- Never expose credentials or tokens.
- Never log sensitive data.
- Never hardcode secrets.
- Never add external automations without authorization.
- Preserve compatibility: when a field or attribute does not exist, handle the optional case explicitly (`None` / `null`) and continue.

---

## 5) Three-pass workflow (anti-error)

For each cycle in `tasks.md`, the agent must run this loop:

### PASS 1 — Understand (read and map)

- Identify exactly where each task is implemented (real files).
- Declare the minimum plan in 3–6 bullets.
- If the location cannot be found, do not invent it: write `TODO: locate module...`.

### PASS 2 — Implement (minimal change)

- Implement task by task.
- Keep changes localized.
- Do not "take the opportunity" to clean up unrelated things.

### PASS 3 — Verify (damage control)

- Confirm that the application or script runs (at least a smoke test).
- Confirm that:
  - no base interfaces or contracts were changed without permission
  - no dependencies were added
  - the base flow was not broken
- If it fails, revert the change or leave it disabled.

---

## 6) Mandatory minimum verification

Every cycle must include:

- Smoke test: run the main script or the module entrypoint (according to the repository/component).
- Minimum functional validation:
  - it produces the expected output or artifact
  - the introduced logic is evaluated correctly
  - it does not crash on missing fields or null values

If it cannot be run (missing environment), document in `task-archives.md`:

- what prevented execution
- which command was attempted
- which output/error was obtained

### 6.1 Exception by cycle type (backlog / analysis)

If the cycle is of type **backlog** or **analysis** (that is, the task does NOT modify code and only generates documentation/artifacts), then:

- The entrypoint smoke test is **NOT mandatory**.
- **Do not run** commands that depend on credentials or unavailable external environments.
- Verification is reduced to:
  - confirm that the output file was generated at the indicated path
  - confirm that project code was NOT modified
  - confirm that `tasks.md` was archived/cleaned correctly

If a command is run by mistake and fails (timeout, missing variables, etc.), record it in `task-archives.md` as a **data point**, without trying to "fix it" (it is not part of the cycle).

### 6.2 Smoke test (entrypoint execution)

When a task modifies project code, the agent must attempt a **minimum smoke test** of the entrypoint.

Rules:

1) If a `.venv` virtual environment exists at the project root, the smoke test MUST use its executable:

Windows:
```text
.\.venv\Scripts\python.exe main.py
```

Linux/macOS:
```text
./.venv/bin/python main.py
```

2) If `.venv` does not exist:
- the agent may try the project entrypoint (`python main.py`, `npm test`, etc.)
- if it fails because of missing dependencies, it **must not install packages**
- it must document the error in `task-archives.md`

3) If the required environment is unavailable (credentials, external services, etc.):
- record the attempt
- record the error
- continue the cycle normally

4) The smoke test only verifies that:
- the entrypoint starts
- there are no immediate syntax/import errors

The process does not need to complete a long real execution cycle.

The agent must record:

```text
environment_used: <path>
venv_detected: true/false
```

---

## 7) Mandatory log (archiving)

When finishing, the agent must move completed work to:
`themis/tasks/archives/task-archives.md`

The file must include:

- cycle id
- objective
- completed tasks
- files touched (real paths)
- how to test (commands or steps)
- TODOs/risks

---

## 8) Outputs (optional, only when the task requires them)

If the task requires artifacts:

- AI: `themis/outputs/ia/`
- Human: `themis/outputs/human/`

If they are not needed, do not create files "just in case".

---

## 9) Backlog generation

When a task requires analyzing documentation and generating a backlog:

1. Read the template: `themis/templates/template-backlog.md`.
2. Strictly respect its structure.
3. Save the generated file at: `themis/outputs/ia/reports/backlog_mejoras.md`.
4. The backlog must contain at most 10 tasks.
5. Each task must be atomic and executable in a single agent cycle.

### 9.1 Backlog consumption (backlog -> tasks)

The backlog works as a **queue of candidate tasks** that can become active agent tasks.

Active backlog path: `themis/outputs/ia/reports/backlog_mejoras.md`

Backlog archive path: `themis/outputs/ia/reports/backlog_archives.md`

Rules when converting backlog tasks into active tasks:

1. Select **at most 3 tasks** from the backlog.
2. Convert them to the format defined in `themis/templates/template-task.md`.
3. Add them to `themis/tasks/tasks.md`.
4. Once added to `tasks.md`, **completely remove** those tasks from `themis/outputs/ia/reports/backlog_mejoras.md`.
5. **Append** the removed entries to `themis/outputs/ia/reports/backlog_archives.md`, preserving their original structure.

Identification rule:

Move the entire task entry using the field `id: backlog-XXX`, from `### task` / `id: backlog-XXX` through the end of its acceptance block.

This guarantees that:

- the backlog works as a **consumable queue**
- already selected tasks are not reprocessed
- there is **full traceability** of tasks that moved from backlog to execution

### 9.2 Automatic ID generation

Backlog and task IDs must be generated automatically. The agent must never leave empty ID fields or require the human to fill them in.

Backlog:

1. Read all existing IDs in `backlog_mejoras.md` and `backlog_archives.md`.
2. Detect the highest existing number.
3. Generate the next available ID using `id: backlog-XXX` (for example `backlog-001`, `backlog-002`).

Tasks:

When creating or adding a cycle in `themis/tasks/tasks.md`, generate the cycle ID automatically using:

```text
YYYY-MM-DD-XX
```

where `YYYY` is the year, `MM` the month, `DD` the day, and `XX` an incremental cycle number for that day (for example `2026-03-05-01`).

Template rule:

Templates may use `id: AUTO`. The agent must replace `AUTO` with the correct ID when generating the final file.

### 9.3 Backlog prioritization and order (mandatory heuristic)

When selecting tasks from `backlog_mejoras.md`, the agent must NOT choose them arbitrarily. It must compute a deterministic priority order and select in that order.

Priority order (highest to lowest):

1) **impact** (descending): `high` > `medium` > `low`
2) **effort** (ascending): `low` < `medium` < `high`
3) **risk** (ascending): `low` < `medium` < `high`
4) **dependencies**: tasks with `depends_on: []` first; then tasks with dependencies
5) **final tie-breaker**: by `id` ascending (`backlog-001` before `backlog-002`)

Explicit buckets:

1. impact **high** + effort **low**
2. impact **high** + effort **medium**
3. impact **high** + effort **high**
4. impact **medium** + effort **low**
5. impact **medium** + effort **medium**
6. impact **medium** + effort **high**
7. impact **low** + effort **low**
8. impact **low** + effort **medium**
9. impact **low** + effort **high**

Within each bucket, order by:

- lower `risk` first
- then `depends_on: []` first
- then `id` ascending

Per-cycle limit:

Select at most N tasks per cycle (according to the contract or template) and document explicitly in `task-archives.md`:

- which tasks were selected (IDs)
- which criterion was applied (this section 9.3)
- how many remained pending due to lower priority

---

## 10 Anti-catastrophe protection

The agent must avoid executing tasks that are too large or ambiguous.

Before implementing a task, evaluate:

1. Estimated number of files to modify.
2. Whether it implies structural changes.
3. Whether the task is sufficiently atomic.

Blocking conditions:

- more than **5 files to modify**
- structural refactor
- unauthorized changes to the base system architecture
- ambiguous or non-atomic tasks

In these cases the agent must:

1. NOT execute changes
2. record the problem in `task-archives.md`
3. propose splitting the task into smaller tasks

---

## 11) Interaction language

All agent communication must be in English.

This includes:

- explanations
- questions
- execution reports
- verification messages

Allowed exceptions:

- library names
- programming reserved words
- file paths
- terminal commands

---

## 12 Agent roles

The system operates through ten logical roles:

- **Planner** — `themis/roles/planner.md`
- **Executor** — `themis/roles/executor.md`
- **Debugger** — `themis/roles/debugger.md`
- **Designer** — `themis/roles/designer.md`
- **Architect** — `themis/roles/architect.md`
- **Security Engineer** — `themis/roles/security_engineer.md`
- **QA Engineer** — `themis/roles/qa_engineer.md`
- **DevOps Engineer** — `themis/roles/devops_engineer.md`
- **Documentator** — `themis/roles/documentator.md`
- **Product Owner** — `themis/roles/product_owner.md`

Rules:

1. All roles must respect every rule defined in this contract (`agent.md`).
2. If there is a conflict between role files and this contract, `agent.md` prevails.
3. Role files only add specific responsibilities; they never redefine global rules.
4. The **Debugger** role is used only for cycles of type `bug`, `diagnosis`, or `dynamic_analysis`.
5. The **Debugger** does not implement definitive fixes unless explicitly authorized; its goal is to diagnose and produce evidence.
6. The **Designer** role is used for visual briefs (banners, themes, help screens, TUI) and `design` cycles. It researches and proposes with theory and measurable criteria; it does not implement the redesign unless the task authorizes it. No visual change enters `EXECUTOR_PHASE` without its prior report.

---

## 13) Role orchestration (roles-loop)

The system operates through **ten logical roles**: Planner, Debugger, Executor, Designer, Architect, Security Engineer, QA Engineer, DevOps Engineer, Documentator, and Product Owner.

- Role switching and execution order are governed **exclusively** by `themis/loops/roles-loop.md`.

Rules:

1. Before any action, the agent must read:
   - `themis/agent.md`
   - `themis/loops/roles-loop.md`
   - `themis/roles/<role>.md`
2. If there is a conflict between `roles-loop` / role files and this contract, `agent.md` prevails.
3. Role and loop files do **not** redefine global rules: they only add responsibilities and operational sequence.
4. For `bug`, `diagnosis`, or `dynamic_analysis` cycles, the system must evaluate entry through the **Debugger** role according to `roles-loop.md`.
5. In bug cycles, the **Executor** must not implement changes without a prior Debugger report, unless a human explicitly authorizes it.
6. For `design` cycles or visual briefs, the system must evaluate entry through the **Designer** role according to `roles-loop.md`. The **Executor** must not implement visual changes without its prior report, unless a human explicitly authorizes it.
7. Veto precedence (highest to lowest): **security > qa > architect > designer > documentator > devops > product_owner**. Rationale: damage containment > evidence > structure > presentation > knowledge > operations > scope. When vetoes conflict, the highest precedence wins; a tie is resolved by the human.
8. Boundaries: **Product Owner** proposes value and acceptance (does not write `tasks.md`); **Planner** applies section 9.3 and writes tasks; **QA** defines gates and judges (does not implement); **Architect** proposes ADRs without authorizing changes (section 2.1 remains intact); **Security** enforces section 4; **Documentator** owns documentation (the log remains the Executor's responsibility); **DevOps** owns hooks/pipeline/worktrees.

---

## 14) Memory loop (controlled persistence)

Memory persistence is governed exclusively by `themis/loops/memory-loop.md`.

Rules:

1) Planner decides *what to save* (selection).
2) Executor writes/applies the persistence (minimal changes, never inventing files).
3) If there is a conflict, this contract (`agent.md`) prevails.

---

## 15) Context Freeze (minimum map per cycle)

Reading policy and per-cycle scope are governed by `themis/loops/context-freeze.md`.

Rules:

1) PASS 1 must produce a **Freeze Map** (list of files to touch/read). The Freeze Map must contain at most 10 files.
2) PASS 2 and PASS 3 may only use those files unless an explicit exception is granted.
