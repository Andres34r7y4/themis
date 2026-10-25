# roles-loop.md — Planner ↔ Executor Orchestration (V1)

## 0) Pre-flight (MANDATORY)
Before any action, the system MUST:
1) read `./themis/agent.md`
2) read `./themis/loops/roles-loop.md`
3) read `./themis/roles/planner.md` or `./themis/roles/debugger.md` or `./themis/roles/executor.md` according to the case
4) print a status line:
   - `ROLE: planner` or `ROLE: debugger` or `ROLE: executor`
   - `CYCLE_ID: <id>`
   - `MODE: roles-loop`

Hard rule:
- If there is a conflict between roles-loop / roles/* and `agent.md`, **`agent.md` prevails**.

---

## 1) Loop States

Valid states:
- `PLANNER_PHASE`
- `DEBUGGER_PHASE`
- `DESIGNER_PHASE`
- `EXECUTOR_PHASE`
- `STOP`

The system starts in:

- `PLANNER_PHASE` for normal cycles (`feature`, `backlog`, `analysis`)
- `DEBUGGER_PHASE` if the user explicitly indicates a cycle of type:
  - `bug`
  - `diagnosis`
  - `dynamic_analysis`
  and there is already a sufficiently defined symptom
- `DESIGNER_PHASE` if the cycle is of type `design` or the task brings a visual brief
- `PLANNER_PHASE` if the bug still needs to be decomposed or clarified before diagnosis
- `EXECUTOR_PHASE` only if the user explicitly says "only execute tasks.md"

---

## 2) Canonical Inputs / Outputs

Planner reads:
- `themis/objective.md` (if it exists)
- `./themis/tasks/tasks.md`
- (optional) backlog/improvements if they exist in docs

Planner writes:
- `./themis/tasks/tasks.md` (max 3 tasks per cycle, following template)
- (optional) planning notes in outputs (only if the contract allows)

Debugger reads:
- `./themis/tasks/tasks.md` (if active cycle exists)
- previous Planner report (if exists)
- real repo (real files)
- `repo_index` / structural outputs if they exist
- symptom declared by user or by Planner

Debugger writes:
- `./themis/outputs/ia/reports/debug_<CYCLE_ID>.md` (mandatory report)
- (optional) minimum traces or temporary diagnostic changes, only if contract and cycle allow
- (optional) recommendations for partition or handoff to Executor

Designer reads:
- `./themis/tasks/tasks.md` (visual brief of the cycle)
- `tokens.yaml` / current themes + brief references
- real repo (only visual reached by brief)

Designer writes:
- `./themis/outputs/ia/reports/design_<CYCLE_ID>.md` (mandatory report + veto)
- (optional) proposals with measurable criteria and tokens (without implementing if task does not authorize)

Executor reads:
- `./themis/tasks/tasks.md` (UNIQUE source of tasks)
- real repo (real files)

Executor writes:
- minimal code changes (only to fulfill tasks.md)
- `./themis/tasks/archives/task-archives.md` (mandatory log)
- updates `./themis/tasks/tasks.md` removing completed tasks

---

## 3) Planner Rules (PLANNER_PHASE)
Objective: convert objectives/backlog into atomic tasks.

Checklist:
1) NO touching code.
2) NO executing smoke tests.
3) Create/update `tasks.md`:
   - ordered by priority: **High Impact + Low Effort** first
   - then: high+medium, high+high, medium+low, medium+medium, low+* at the end
4) Each task must include:
   - impact: high|medium|low
   - effort: low|medium|high
   - completion criteria
   - probable files to touch (if they can be inferred without inventing)

Handoff condition:
- If `tasks.md` has ≥ 1 task, pass to `EXECUTOR_PHASE`.
- If `tasks.md` is empty, pass to `STOP`.

---

## 4) Debugger Rules (DEBUGGER_PHASE)

Objective: diagnose bugs without implementing definitive fixes and produce usable evidence.

Checklist:
1) NO refactoring.
2) NO permanent logic changes unless explicit authorization.
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
   - evidence
   - result
   - next step
6) If debug changes are required:
   - they must be minimal
   - reversible
   - documented as temporary
7) If diagnosis requires sandbox, prefer temporary worktree.

Handoff condition:
- pass to `EXECUTOR_PHASE` only if:
  - `debug_<CYCLE_ID>.md` exists
  - there is probable root cause or dominant hypothesis supported
  - next step is sufficiently delimited
- return to `PLANNER_PHASE` if:
  - bug remains ambiguous
  - task must be split
  - human input is required
- pass to `STOP` if:
  - no reproducible symptom
  - missing environment
  - cycle remains blocked

---

## 5) Executor Rules (EXECUTOR_PHASE)
Objective: execute ONLY what is in `tasks.md`.

Checklist:
0) If the cycle is a bug, read obligatorily `debug_<CYCLE_ID>.md` before touching code.
0b) If the task is visual (brief/`design`), read obligatorily `design_<CYCLE_ID>.md` before touching visual.
1) Apply Tree workflow of `agent.md` (3 passes).
2) Implement minimal changes.
3) Minimum verification (smoke test) ONLY if it applies to cycle type.
4) Archive in `task-archives.md` with:
   - CYCLE_ID
   - objective
   - completed tasks ✅
   - files touched (real paths)
   - how to test (real commands)
   - TODOs / risks

Handoff condition:
- If pending tasks remain in `tasks.md`:
  - return to `PLANNER_PHASE` ONLY if ambiguity / non-atomic task / anti-catastrophe.
  - if clear remaining tasks, can continue in `EXECUTOR_PHASE` until max 3 tasks/cycle.
- If `tasks.md` is empty: `STOP`.

In cycle types `bug`, `diagnosis` or `dynamic_analysis`, Executor MUST NOT act without a prior Debugger report:

`./themis/outputs/ia/reports/debug_<CYCLE_ID>.md`

That report functions as mandatory technical context source for fix implementation.

In cycle types `design` or tasks with visual brief, Executor MUST NOT touch visual without a prior Designer report:

`./themis/outputs/ia/reports/design_<CYCLE_ID>.md`

## 5c) Support Role Gates (no new phases)

The 6 support roles operate as Executor checklist gates (besides `0b` visual):

- `0c` **Security**: enforces `agent.md §4` in all cycles with changes.
- `0d` **QA**: validates acceptance pre-STOP in code cycles.
- `0e` **Architect**: gate when cycle touches structure, contracts, or dependencies.
- `0f` **Documentator**: gate of deliverable docs (log remains in Executor).
- `0g` **DevOps**: gate of hooks/pipeline/worktrees and rollback.
- `0h` **Product Owner**: gate pre-Planning (value and acceptance of candidates).

Each gate is settled with its report (`security_/qa_/architecture_/docs_/devops_/product_<CYCLE_ID>.md`) or with founded veto that returns to `PLANNER_PHASE`. Veto precedence in `agent.md §12.7`.

## 5b) Designer Rules (DESIGNER_PHASE)

Objective: investigate and propose the visual with theory and measurable criteria, without implementing the redesign unless authorized in the task.

Checklist:
1) Require minimum brief (objective, audience/context, restrictions, references). Without brief: STOP + input request.
2) Research phase without drawing (real references + role theory, 3-6 bullets).
3) Propose max 2 variants with measurable criteria + 1 recommended, in `design_<CYCLE_ID>.md`.
4) Register palette/spacing in tokens (names, via Planner if creating keys).
5) Veto in writing what does not meet criteria, with alternative.

Handoff condition:
- pass to `EXECUTOR_PHASE` with report + tokens + criteria when proposal is ready to implement.
- return to `PLANNER_PHASE` if missing brief, design must be split, or contract conflict.
- pass to `STOP` if no verification environment or human must decide.

---

## 6) Anti-Catastrophe (automatic cut)
Before implementing, evaluate:
- estimated number of files to modify
- structural changes
- task atomicity

Blocking conditions:
- more than 5 files
- structural refactor
- unauthorized architecture change
- ambiguous / non-atomic task

If triggered:
1) DO NOT execute changes.
2) register in `task-archives.md` (with CYCLE_ID and reason)
3) propose partition into smaller tasks (returns to `PLANNER_PHASE`)

---

## 7) Stop conditions

The loop ends when:
- `tasks.md` is empty, or
- anti-catastrophe triggered and human input required, or
- max 3 tasks reached for current cycle, or
- bug cycle remains blocked by:
  - missing clear symptom
  - missing reproducible environment
  - insufficient evidence after minimum diagnosis
  - need for human decision

---

## 8) Verification and budget (best practices multi-agent)

Mandatory roles per cycle: **Planner** (decomposes), **Executor** (executes one step at a time), **Verifier** (deterministic check: tests, validation, typecheck — never just "looks good").

1) **Evidence before STOP**: no cycle closes without a check executed by code (green suite, `validate`, honest ping).
2) **Loop budget**: max 2 Executor→review rounds; at 3rd escalate to human with disagreement in writing.
3) **Communicative dehallucination**: if Executor lacks a plan data, ask corresponding role BEFORE inventing it.
4) **Minimum privilege per role**: each role only touches their artifacts (Planner: tasks/plan; Executor: code; Debugger: reports). No keys or secrets in artifacts, ever.
