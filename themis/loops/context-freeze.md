# context-freeze.md — Context Freeze (V1)

## Purpose

The Context Freeze prevents scope creep and uncontrolled reading. Every cycle
must declare a **Freeze Map** before implementing changes.

## Rules

1) PASS 1 (Understand) must produce a Freeze Map listing the files that will be
   read and/or modified during the cycle.
2) The Freeze Map must contain **at most 10 files**.
3) PASS 2 (Implement) and PASS 3 (Verify) may only use the files in the Freeze
   Map, unless an explicit exception is approved by a human or by the
   corresponding gate.
4) Any new file added to the map must be justified in the cycle log.
5) The Freeze Map must not include secrets, credentials, or generated data.

## Freeze Map format

```text
CYCLE_ID: <id>
OBJECTIVE: <short objective>

READ:
- path/to/file

MODIFY:
- path/to/file

EXCEPTIONS:
- path/to/file — reason
```

## Exceptions

The following do not require a Freeze Map update, but must be logged:

- reading `themis/agent.md`, `themis/loops/roles-loop.md`, and the active role
- running read-only validation commands
- generating mandatory reports under `themis/outputs/ia/reports/`

## Enforcement

- If a change requires a file outside the Freeze Map, stop and request an
  exception.
- If the map exceeds 10 files, split the cycle into smaller tasks.
- The Executor must not read files outside the map "just in case".
