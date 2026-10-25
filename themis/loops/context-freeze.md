# context-freeze.md — Context Freeze Protocol

## Purpose
Capture an immutable snapshot of system state before any execution cycle to ensure deterministic behavior and enable rollback.

## Freeze Map
Before implementing changes, Planner must define:
1. Files that will be modified
2. Current state of those files (hash or content reference)
3. Dependencies affected
4. Environment variables in use

## Rollback Trigger
If any of the following occur:
- Executor fails verification
- Security policy violation detected
- Anti-catastrophe condition triggered

The system restores to the frozen state snapshot.
