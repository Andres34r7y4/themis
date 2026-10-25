"""Kernel engine for PRE-FLIGHT validation and governance contract enforcement.

This module implements the core validation logic that every agent must pass
before executing any action under the Themis protocol.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class GovernanceKernel:
    """Deterministic governance kernel for LLM agents.

    Enforces the PRE-FLIGHT protocol: no agent action proceeds without
    declaring ROLE, CYCLE_ID, and MODE, and reading the required contract
    files in the correct order.
    """

    VALID_ROLES = {
        "planner",
        "executor",
        "debugger",
        "security_engineer",
        "architect",
        "qa_engineer",
        "documentator",
        "devops_engineer",
        "product_owner",
        "designer",
    }

    VALID_MODES = {"roles-loop", "manual"}

    REQUIRED_READ_ORDER = [
        "agent.md",
        "loops/roles-loop.md",
        "roles/{role}.md",
    ]

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir).resolve()
        self.themis_dir = self.base_dir / "themis"

    def validate_structure(self) -> list[str]:
        """Check that all required governance files exist.

        Returns a list of missing files (empty if all present).
        """
        missing: list[str] = []
        required = [
            "agent.md",
            "PATHS.md",
            "loops/roles-loop.md",
            "loops/context-freeze.md",
            "loops/memory-loop.md",
            "roles/planner.md",
            "roles/executor.md",
            "roles/debugger.md",
            "roles/security_engineer.md",
            "roles/architect.md",
            "roles/qa_engineer.md",
            "roles/documentator.md",
            "roles/devops_engineer.md",
            "roles/product_owner.md",
            "roles/designer.md",
            "tasks/tasks.md",
            "tasks/archives/task-archives.md",
            "templates/prompt-inicial.md",
            "templates/run-roles-loop.md",
            "templates/template-task.md",
            "templates/template-backlog.md",
        ]
        for rel in required:
            if not (self.themis_dir / rel).exists():
                missing.append(str(self.themis_dir / rel))
        return missing

    def pre_flight(
        self,
        role: str,
        mode: str = "roles-loop",
        cycle_id: Optional[str] = None,
    ) -> dict:
        """Execute the PRE-FLIGHT protocol.

        Args:
            role: The agent role (planner, executor, debugger, etc.)
            mode: Operation mode (roles-loop or manual)
            cycle_id: ISO timestamp. If None, generates one.

        Returns:
            A dict with validation results and the PRE-FLIGHT OK line.

        Raises:
            ValueError: If role or mode is invalid, or structure is incomplete.
        """
        # Validate role
        if role not in self.VALID_ROLES:
            raise ValueError(
                f"Invalid role: '{role}'. Must be one of: {sorted(self.VALID_ROLES)}"
            )

        # Validate mode
        if mode not in self.VALID_MODES:
            raise ValueError(
                f"Invalid mode: '{mode}'. Must be one of: {sorted(self.VALID_MODES)}"
            )

        # Validate structure
        missing = self.validate_structure()
        if missing:
            raise ValueError(
                f"Governance structure incomplete. Missing files: {missing}"
            )

        # Generate cycle ID if not provided
        if cycle_id is None:
            cycle_id = datetime.now(timezone.utc).isoformat()

        # Build the read order for this role
        read_order = [
            str(self.themis_dir / "agent.md"),
            str(self.themis_dir / "loops" / "roles-loop.md"),
            str(self.themis_dir / "roles" / f"{role}.md"),
        ]

        # Verify all read-order files exist
        for path in read_order:
            if not Path(path).exists():
                raise ValueError(f"Required contract file not found: {path}")

        return {
            "status": "PRE-FLIGHT OK",
            "role": role,
            "mode": mode,
            "cycle_id": cycle_id,
            "read_order": read_order,
            "validated_at": datetime.now(timezone.utc).isoformat(),
        }

    def format_pre_flight(self, result: dict) -> str:
        """Format a PRE-FLIGHT result as the standard output string."""
        lines = [
            "PRE-FLIGHT OK",
            f"ROLE: {result['role']}",
            f"MODE: {result['mode']}",
            f"CYCLE_ID: {result['cycle_id']}",
        ]
        return "\n".join(lines)
