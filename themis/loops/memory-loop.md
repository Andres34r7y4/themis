# memory-loop.md — Memory Loop Protocol

## Purpose
Maintain traceability of agent executions across cycles for auditing and continuous improvement.

## Memory Structure
Each cycle produces:
1. Cycle ID and timestamp
2. Role sequence executed
3. Tasks completed and their outcomes
4. Files modified with before/after state
5. Verification results
6. Human decisions and vetoes

## Retention
Memory logs are stored in `themis/outputs/ia/memory/` and must be preserved for audit purposes.
