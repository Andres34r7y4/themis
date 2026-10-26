# Run Roles Loop — Themis

Use this prompt to run one complete governance cycle.

```text
Run one Themis cycle.

1) PRE-FLIGHT: declare ROLE, MODE, CYCLE_ID and read agent.md → roles-loop.md → your role.
2) PLANNER_PHASE: read themis/tasks/tasks.md and the optional objective.
   - If tasks.md is empty, generate at most 3 atomic tasks or move to STOP.
3) EXECUTOR_PHASE: implement only the tasks in tasks.md.
   - Respect the Context Freeze and the 5-file anti-catastrophe limit.
4) VERIFY: run the minimum verification and record real output.
5) ARCHIVE: update themis/tasks/archives/task-archives.md and clean tasks.md.
6) STOP: report the cycle summary, evidence, and open risks.

Never skip PRE-FLIGHT. Never exceed your role boundaries.
```
