# agent.md — Themis (V1) — Governance Kernel

# PRE-FLIGHT (MANDATORY)

Before taking any action or response, the agent MUST:
1) Identify and declare:
   - ROLE: planner | executor | debugger
   - CYCLE_ID: <ISO timestamp with offset, e.g. 2026-03-05T10:49:26-03:00>
   - MODE: roles-loop | manual

2) Read and strictly obey, in this order:
   - `/themis/agent.md` (central contract / kernel)
   - `/themis/loops/roles-loop.md` (role orchestration)
   - `/themis/roles/<ROLE>.md` (role rules)

If there is a conflict between files, PREVALENCE goes to `/themis/agent.md`.

Then print obligatorily:

PRE-FLIGHT OK  
ROLE: <role>  
MODE: <mode>  
CYCLE_ID: <timestamp>

Hard rule:

If PRE-FLIGHT was not executed or confirmed, the agent **must not continue with any analysis or execution action**.

---

## 0) Mission
Provide **any repository** with an autonomous, deterministic, multi-role governance engine (**Themis**) focused on:
- Strict task orchestration through role separation (Planner, Executor, Debugger).
- Secure and atomic execution of automations, pipelines, and controlled refactors.
- Guarantee traceability, auditability, and damage containment in any module or integrated repository.

The agent **is NOT authorized** to "reconstruct" projects. It can only make small, atomic, and verifiable changes.