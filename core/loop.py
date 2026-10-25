"""State loop orchestrator for Themis governance.

Implements the deterministic state machine:
PLANNER_PHASE → EXECUTOR_PHASE → STOP

With optional branches:
- DEBUGGER_PHASE (for bug/diagnosis cycles)
- DESIGNER_PHASE (for visual/design cycles)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LoopState:
    """Current state of the governance loop."""

    phase: str
    cycle_id: str
    role: str
    tasks_remaining: int = 0
    anti_catastrophe_triggered: bool = False

    def is_terminal(self) -> bool:
        """Check if the loop has reached a terminal state."""
        return self.phase == "STOP"


# Valid phases in the governance loop
VALID_PHASES = {
    "PLANNER_PHASE",
    "EXECUTOR_PHASE",
    "DEBUGGER_PHASE",
    "DESIGNER_PHASE",
    "STOP",
}

# Valid transitions: from_phase -> [allowed_to_phases]
VALID_TRANSITIONS = {
    "PLANNER_PHASE": ["EXECUTOR_PHASE", "STOP"],
    "EXECUTOR_PHASE": ["PLANNER_PHASE", "STOP"],
    "DEBUGGER_PHASE": ["EXECUTOR_PHASE", "PLANNER_PHASE", "STOP"],
    "DESIGNER_PHASE": ["EXECUTOR_PHASE", "PLANNER_PHASE", "STOP"],
    "STOP": [],  # Terminal
}

# Anti-catastrophe blocking conditions
ANTI_CATASTROPE_CONDITIONS = [
    "more than 5 files to modify",
    "structural refactor",
    "unauthorized architecture change",
    "ambiguous / non-atomic task",
]


class LoopOrchestrator:
    """Orchestrates state transitions in the governance loop."""

    def __init__(self, cycle_id: str, initial_role: str = "planner"):
        self.cycle_id = cycle_id
        self.state = LoopState(
            phase="PLANNER_PHASE",
            cycle_id=cycle_id,
            role=initial_role,
            tasks_remaining=0,
        )
        self.history: list[LoopState] = [self.state]

    def transition(self, new_phase: str, new_role: Optional[str] = None) -> LoopState:
        """Transition to a new phase in the governance loop.

        Args:
            new_phase: The target phase.
            new_role: The role for the new phase (defaults to current role).

        Returns:
            The new LoopState.

        Raises:
            ValueError: If the transition is invalid or the phase is unknown.
        """
        if new_phase not in VALID_PHASES:
            raise ValueError(
                f"Invalid phase: '{new_phase}'. Valid phases: {sorted(VALID_PHASES)}"
            )

        current = self.state.phase
        if new_phase not in VALID_TRANSITIONS.get(current, []):
            raise ValueError(
                f"Invalid transition: {current} → {new_phase}. "
                f"Allowed from {current}: {sorted(VALID_TRANSITIONS.get(current, []))}"
            )

        if new_role is None:
            new_role = self.state.role

        self.state = LoopState(
            phase=new_phase,
            cycle_id=self.cycle_id,
            role=new_role,
            tasks_remaining=self.state.tasks_remaining,
            anti_catastrophe_triggered=self.state.anti_catastrophe_triggered,
        )
        self.history.append(self.state)
        return self.state

    def trigger_anti_catastrophe(self, reason: str) -> None:
        """Trigger the anti-catastrophe cutoff.

        Args:
            reason: Human-readable reason for the cutoff.
        """
        self.state.anti_catastrophe_triggered = True
        # Transition to STOP since no changes should be made
        self.transition("STOP")

    def set_tasks_remaining(self, count: int) -> None:
        """Update the number of remaining tasks in the current cycle."""
        self.state.tasks_remaining = count

    def get_summary(self) -> dict:
        """Return a summary of the current loop state."""
        return {
            "cycle_id": self.cycle_id,
            "current_phase": self.state.phase,
            "current_role": self.state.role,
            "tasks_remaining": self.state.tasks_remaining,
            "anti_catastrophe_triggered": self.state.anti_catastrophe_triggered,
            "is_terminal": self.state.is_terminal(),
            "transition_count": len(self.history),
        }
