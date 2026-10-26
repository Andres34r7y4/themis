# Integration Examples — Themis Governance with LLMs

This document shows how to integrate Themis governance into real LLM-based agent
systems.

## Example 1: System Prompt Injection (OpenAI / Anthropic / DeepSeek / Ollama)

The `themis/agent.md` file is the **governance kernel**. Inject it into your
agent's system prompt:

```python
from pathlib import Path

THEMIS_KERNEL = Path("themis/agent.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""
You are an autonomous agent operating under Themis Governance Protocol V1.

{THEMIS_KERNEL}

Before EVERY action, you must:
1. Execute PRE-FLIGHT: declare ROLE, CYCLE_ID, MODE.
2. Read agent.md -> roles-loop.md -> roles/<ROLE>.md.
3. Print "PRE-FLIGHT OK" with your ROLE, MODE, and CYCLE_ID.
4. Only then proceed with your role-specific responsibilities.

Never skip PRE-FLIGHT. Never exceed your role boundaries.
"""

# Then pass SYSTEM_PROMPT to your LLM provider.
response = llm.complete(system=SYSTEM_PROMPT, user=user_request)
```

## Example 2: PRE-FLIGHT Validation in an Agent Loop

The Python package lives in `core/` (top-level module):

```python
from pathlib import Path

from core.kernel import GovernanceKernel

kernel = GovernanceKernel(Path("."))

try:
    result = kernel.pre_flight(role="planner", mode="roles-loop")
    print(kernel.format_pre_flight(result))

    # Only now proceed with planner duties...
    # plan = planner.decompose(objective)

except ValueError as exc:
    print(f"GOVERNANCE BLOCK: {exc}")
    # Halt execution — do not proceed.
```

## Example 3: Complete Cycle with Role Enforcement

```python
from pathlib import Path

from core.kernel import GovernanceKernel
from core.loop import LoopOrchestrator
from core.roles import get_role

kernel = GovernanceKernel(Path("."))

# Validate the structure first.
missing = kernel.validate_structure()
if missing:
    raise RuntimeError(f"Missing governance files: {missing}")

# Initialize the loop.
loop = LoopOrchestrator(cycle_id="2026-10-24T10:00:00Z")

# Planner phase.
result = kernel.pre_flight(role="planner", mode="roles-loop")
print(kernel.format_pre_flight(result))
planner = get_role("planner")
print(f"Planner mission: {planner.mission}")

# Transition to executor.
loop.transition("EXECUTOR_PHASE", new_role="executor")

result = kernel.pre_flight(role="executor", mode="roles-loop")
print(kernel.format_pre_flight(result))
executor = get_role("executor")
print(f"Executor can touch code: {executor.can_touch_code}")

print(f"Loop state: {loop.get_summary()}")
```

## Example 4: CLI Usage

```bash
# Install the CLI from a clone.
python -m pip install -e .

# Initialize governance in a new repository.
themis init --repo ./my-project --base-dir themis

# Validate the structure.
themis validate --repo ./my-project

# Run PRE-FLIGHT for a planner.
themis run-cycle --role planner --mode roles-loop

# Run PRE-FLIGHT for an executor.
themis run-cycle --role executor --mode roles-loop

# Use a custom governance directory.
themis init --repo ./my-project --base-dir governance
themis validate --repo ./my-project --base-dir governance
```

## Example 5: Role Boundary Check

```python
from core.roles import get_role

# Before allowing code modification:
role = get_role("planner")
if not role.can_touch_code:
    print(f"BLOCKED: {role.name} cannot modify code")
    print(f"Forbidden: {', '.join(role.forbidden)}")
    # Halt — do not proceed.
```

## Example 6: Anti-Catastrophe Cutoff

```python
from core.loop import LoopOrchestrator

loop = LoopOrchestrator(cycle_id="2026-10-24T10:00:00Z")

files_to_modify = ["a.py", "b.py", "c.py", "d.py", "e.py", "f.py"]
if len(files_to_modify) > 5:
    loop.trigger_anti_catastrophe("more than 5 files to modify")
    print(loop.get_summary())
    # STOP: split the task into smaller cycles.
```

## Supported LLM Providers

Themis is **provider-agnostic**. It works with any LLM because the governance
contract is injected as text (system prompt) rather than being provider-specific.

| Provider | Integration Method |
|----------|-------------------|
| OpenAI | System prompt injection |
| Anthropic | System prompt injection |
| DeepSeek | System prompt injection |
| Ollama (local) | System prompt injection |
| Any OpenAI-compatible API | System prompt injection |

## Key Principle

**Themis is not a library you import into your agent.** It is a **protocol** you
inject into your agent's system prompt and enforce through your orchestration
layer. The Python package (`cli.py`, `core/`) provides tooling to validate and
run the protocol, but the actual enforcement happens at the prompt level.
