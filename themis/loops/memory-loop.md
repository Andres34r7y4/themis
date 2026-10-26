# memory-loop.md — Controlled Persistence (V1)

## Purpose

Define what Themis remembers between cycles, where it is stored, and who is
allowed to write it.

## Responsibilities

1) **Planner** decides *what to save* (selection and relevance).
2) **Executor** writes/applies the persistence with minimal changes.
3) **Documentator** verifies that the persisted record is complete and readable.
4) If there is a conflict, `themis/agent.md` prevails.

## Canonical memory artifacts

| Artifact | Path | Owner |
|----------|------|-------|
| Cycle log | `themis/tasks/archives/task-archives.md` | Executor |
| Active tasks | `themis/tasks/tasks.md` | Planner / Executor |
| Debug reports | `themis/outputs/ia/reports/debug_<CYCLE_ID>.md` | Debugger |
| Design reports | `themis/outputs/ia/reports/design_<CYCLE_ID>.md` | Designer |
| Gate reports | `themis/outputs/ia/reports/<gate>_<CYCLE_ID>.md` | Gate role |
| Long-term memory | `themis/outputs/ia/memory/memory.md` | Planner / Executor |

## What to persist

- Decisions and their rationale.
- Files touched and commands actually run.
- Verification evidence and known limitations.
- Open risks and TODOs.
- Changes in contracts, roles, or loops.

## What NOT to persist

- Secrets, tokens, credentials, or personal data.
- Speculative claims not backed by evidence.
- Full file dumps when a path and summary are enough.

## Cycle log entry format

```markdown
## <CYCLE_ID>

- Objective: <objective>
- Tasks completed: <task ids>
- Files touched: <real paths>
- How to test: <real commands>
- Evidence: <output summary>
- TODOs / risks: <list>
```

## Retention

- The cycle log is append-only.
- Reports are immutable once the cycle reaches `STOP`.
- Memory must remain deterministic: the same cycle and evidence should produce
  the same record.
