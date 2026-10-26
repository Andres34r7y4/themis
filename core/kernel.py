"""Kernel engine for PRE-FLIGHT validation and governance contract enforcement.

This module implements the core validation logic that every agent must pass
before executing any action under the Themis protocol.
"""

from __future__ import annotations

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

    REQUIRED_FILES = [
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

    def __init__(self, base_dir: Path, base_dir_name: str = "themis"):
        self.base_dir = Path(base_dir).resolve()
        self.base_dir_name = base_dir_name
        self.themis_dir = self.base_dir / base_dir_name

    def validate_structure(self) -> list[str]:
        """Check that all required governance files exist.

        Returns a list of missing file paths (empty when all are present).
        """
        return [
            str(self.themis_dir / rel)
            for rel in self.REQUIRED_FILES
            if not (self.themis_dir / rel).is_file()
        ]

    def pre_flight(
        self,
        role: str,
        mode: str = "roles-loop",
        cycle_id: Optional[str] = None,
    ) -> dict:
        """Execute the PRE-FLIGHT protocol.

        Args:
            role: The agent role (planner, executor, debugger, etc.).
            mode: Operation mode (roles-loop or manual).
            cycle_id: ISO timestamp. If None, generates one.

        Returns:
            A dict with validation results and the PRE-FLIGHT OK line.

        Raises:
            ValueError: If role or mode is invalid, or structure is incomplete.
        """
        if role not in self.VALID_ROLES:
            raise ValueError(
                f"Invalid role: '{role}'. Must be one of: {sorted(self.VALID_ROLES)}"
            )

        if mode not in self.VALID_MODES:
            raise ValueError(
                f"Invalid mode: '{mode}'. Must be one of: {sorted(self.VALID_MODES)}"
            )

        missing = self.validate_structure()
        if missing:
            raise ValueError(
                "Governance structure incomplete. Missing files: " + ", ".join(missing)
            )

        if cycle_id is None:
            cycle_id = datetime.now(timezone.utc).isoformat()

        read_order = [
            str(self.themis_dir / "agent.md"),
            str(self.themis_dir / "loops" / "roles-loop.md"),
            str(self.themis_dir / "roles" / f"{role}.md"),
        ]

        for path in read_order:
            if not Path(path).is_file():
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
