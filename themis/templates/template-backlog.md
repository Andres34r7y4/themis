# Backlog Template — Themis

```markdown
# Backlog — <repository>

## task
id: backlog-AUTO
title: <short imperative title>
impact: high | medium | low
effort: low | medium | high
risk: low | medium | high
depends_on: []

### Context
<why this matters and what problem it solves>

### Proposal
<minimal change or outcome>

### Acceptance criteria
- [ ] <verifiable criterion>

### Notes
<any restriction or open question>
```

## Rules

- Maximum 10 backlog entries.
- Order by impact (desc), effort (asc), risk (asc), dependencies, then ID.
- Maximum 3 entries are converted to `tasks.md` per cycle.
- The Planner consumes this queue and appends consumed entries to
  `themis/outputs/ia/reports/backlog_archives.md`.
