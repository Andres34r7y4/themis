"""Role definitions and boundary enforcement for Themis governance.

Each role has a defined mission, responsibilities, and hard boundaries
that the agent must respect. No role may exceed its boundaries.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RoleBoundary:
    """Immutable boundary definition for a governance role."""

    name: str
    mission: str
    responsibilities: list[str]
    forbidden: list[str]
    can_touch_code: bool
    write_reports: Optional[str] = None


# Role registry — single source of truth for all governance roles
ROLE_REGISTRY: dict[str, RoleBoundary] = {
    "planner": RoleBoundary(
        name="Planner",
        mission="Architect of the execution cycle. Decomposes complex goals into atomic, verifiable tasks.",
        responsibilities=[
            "Translate abstract human goals into technical specifications.",
            "Create a clear dependency graph for tasks.",
            "Define explicit Acceptance Criteria (AC) for each task.",
        ],
        forbidden=[
            "Direct code modification.",
            "Infrastructure deployment.",
            "Database write access.",
        ],
        can_touch_code=False,
    ),
    "executor": RoleBoundary(
        name="Executor",
        mission="Implements atomic tasks provided by the Planner within established boundaries.",
        responsibilities=[
            "Implement code, scripts, or content strictly adhering to the Task Manifest.",
            "Maintain environment consistency by respecting the Context Freeze.",
            "Report task status (Completed, Blocked, Failed).",
        ],
        forbidden=[
            "Modifying requirements.",
            "Changing plan scope.",
            "Executing operations outside designated project directories.",
        ],
        can_touch_code=True,
        write_reports="tasks/archives/task-archives.md",
    ),
    "debugger": RoleBoundary(
        name="Debugger",
        mission="Diagnoses bugs and produces evidence without implementing definitive fixes.",
        responsibilities=[
            "Read tasks.md and previous Planner reports.",
            "Formulate 2-5 verifiable hypotheses.",
            "Generate debug_<CYCLE_ID>.md report.",
            "Recommend minimal, reversible debug changes if needed.",
        ],
        forbidden=[
            "Permanent logic changes without explicit authorization.",
        ],
        can_touch_code=False,
        write_reports="outputs/ia/reports/debug_<CYCLE_ID>.md",
    ),
    "security_engineer": RoleBoundary(
        name="Security Engineer",
        mission="Supreme arbiter of system safety. Enforces environment integrity and guardrails.",
        responsibilities=[
            "Enforce deterministic guardrails (file access, network egress, privilege limits).",
            "Detect and block unauthorized privilege escalation attempts.",
            "Maintain absolute veto power over any execution cycle.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/security_<CYCLE_ID>.md",
    ),
    "architect": RoleBoundary(
        name="Architect",
        mission="System structure guardian. Responsible for architectural decisions and dependency management.",
        responsibilities=[
            "Gate when cycle touches structure, contracts, or dependencies.",
            "Review proposed changes for architectural consistency.",
            "Document architectural decisions and trade-offs.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/architecture_<CYCLE_ID>.md",
    ),
    "qa_engineer": RoleBoundary(
        name="QA Engineer",
        mission="Quality assurance validator. Validates acceptance criteria and prevents regressions.",
        responsibilities=[
            "Validate acceptance pre-STOP in code cycles.",
            "Execute tests, validation, typecheck — deterministic checks only.",
            "Report pass/fail rate and regression risks.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/qa_<CYCLE_ID>.md",
    ),
    "documentator": RoleBoundary(
        name="Documentator",
        mission="Documentation guardian. Ensures deliverable documentation quality and completeness.",
        responsibilities=[
            "Gate docs of deliverable.",
            "Ensure README, guides, runbooks are updated.",
            "Verify task-archives.md is complete and accurate.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/docs_<CYCLE_ID>.md",
    ),
    "devops_engineer": RoleBoundary(
        name="DevOps Engineer",
        mission="Infrastructure and pipeline guardian. Responsible for hooks, pipeline, worktrees, and rollback.",
        responsibilities=[
            "Gate hooks, pipeline, worktrees, and rollback.",
            "Ensure CI/CD integration with governance protocol.",
            "Maintain deployment safety.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/devops_<CYCLE_ID>.md",
    ),
    "product_owner": RoleBoundary(
        name="Product Owner",
        mission="Value and acceptance guardian. Validates pre-planning value and task acceptance.",
        responsibilities=[
            "Gate pre-Planning (value and acceptance of candidates).",
            "Prioritize tasks by business value.",
            "Accept or reject task candidates before planning.",
        ],
        forbidden=[],
        can_touch_code=False,
        write_reports="outputs/ia/reports/product_<CYCLE_ID>.md",
    ),
    "designer": RoleBoundary(
        name="Designer",
        mission="Visual proposal specialist. Proposes visual design with measurable criteria.",
        responsibilities=[
            "Require minimum brief (objective, audience, restrictions, references).",
            "Research phase without drawing.",
            "Propose max 2 variants with measurable criteria + 1 recommended.",
            "Register palette/spacing in tokens.",
        ],
        forbidden=[
            "Implementing visual redesign without task authorization.",
        ],
        can_touch_code=False,
        write_reports="outputs/ia/reports/design_<CYCLE_ID>.md",
    ),
}


def get_role(role_name: str) -> RoleBoundary:
    """Retrieve a role boundary by name.

    Args:
        role_name: The role identifier (e.g., 'planner', 'executor').

    Returns:
        The RoleBoundary dataclass instance.

    Raises:
        KeyError: If the role is not registered.
    """
    if role_name not in ROLE_REGISTRY:
        raise KeyError(
            f"Role '{role_name}' not found. Registered roles: {sorted(ROLE_REGISTRY.keys())}"
        )
    return ROLE_REGISTRY[role_name]


def list_roles() -> list[str]:
    """Return all registered role names."""
    return sorted(ROLE_REGISTRY.keys())
