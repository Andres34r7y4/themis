"""Test suite for the Themis governance CLI and kernel."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli import cmd_init, cmd_run_cycle, cmd_validate
from core.kernel import GovernanceKernel
from core.loop import LoopOrchestrator
from core.roles import ROLE_REGISTRY, get_role, list_roles

REPO_ROOT = Path(__file__).resolve().parents[1]


class KernelTests(unittest.TestCase):
    def test_repository_structure_is_complete(self) -> None:
        kernel = GovernanceKernel(REPO_ROOT)
        self.assertEqual(kernel.validate_structure(), [])

    def test_pre_flight_returns_required_fields(self) -> None:
        kernel = GovernanceKernel(REPO_ROOT)
        result = kernel.pre_flight("planner", cycle_id="2026-01-01T00:00:00+00:00")
        self.assertEqual(result["status"], "PRE-FLIGHT OK")
        self.assertEqual(result["role"], "planner")
        self.assertEqual(result["cycle_id"], "2026-01-01T00:00:00+00:00")
        self.assertEqual(len(result["read_order"]), 3)

    def test_pre_flight_rejects_invalid_role(self) -> None:
        kernel = GovernanceKernel(REPO_ROOT)
        with self.assertRaises(ValueError):
            kernel.pre_flight("wizard")

    def test_pre_flight_rejects_invalid_mode(self) -> None:
        kernel = GovernanceKernel(REPO_ROOT)
        with self.assertRaises(ValueError):
            kernel.pre_flight("planner", mode="autopilot")

    def test_base_dir_is_honoured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cmd_init(repo=tmp, base_dir="governance"), 0)
            kernel = GovernanceKernel(Path(tmp), base_dir_name="governance")
            self.assertEqual(kernel.validate_structure(), [])
            self.assertEqual(
                cmd_run_cycle("executor", repo=tmp, base_dir="governance"), 0
            )


class CliTests(unittest.TestCase):
    def test_init_creates_governance_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cmd_init(repo=tmp), 0)
            target = Path(tmp) / "themis"
            self.assertTrue((target / "agent.md").is_file())
            self.assertTrue((target / "roles" / "designer.md").is_file())
            self.assertEqual(cmd_validate(repo=tmp), 0)

    def test_init_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cmd_init(repo=tmp), 0)
            self.assertEqual(cmd_init(repo=tmp), 1)
            self.assertEqual(cmd_init(repo=tmp, force=True), 0)

    def test_init_rejects_the_source_repository(self) -> None:
        self.assertEqual(cmd_init(repo=str(REPO_ROOT)), 1)

    def test_validate_reports_missing_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cmd_validate(repo=tmp), 1)


class LoopTests(unittest.TestCase):
    def test_happy_path_planner_executor_stop(self) -> None:
        loop = LoopOrchestrator("cycle-1")
        loop.transition("EXECUTOR_PHASE", new_role="executor")
        loop.transition("STOP")
        self.assertTrue(loop.get_summary()["is_terminal"])
        self.assertEqual(loop.get_summary()["current_role"], "executor")

    def test_invalid_transition_is_rejected(self) -> None:
        loop = LoopOrchestrator("cycle-1")
        with self.assertRaises(ValueError):
            loop.transition("STOP")
            loop.transition("EXECUTOR_PHASE")

    def test_anti_catastrophe_is_idempotent_at_stop(self) -> None:
        loop = LoopOrchestrator("cycle-1")
        loop.trigger_anti_catastrophe("too many files")
        self.assertTrue(loop.state.is_terminal())
        loop.trigger_anti_catastrophe("called twice")
        self.assertTrue(loop.state.anti_catastrophe_triggered)
        self.assertEqual(loop.state.stop_reason, "called twice")


class RoleTests(unittest.TestCase):
    def test_all_roles_have_a_document(self) -> None:
        for role in list_roles():
            path = REPO_ROOT / "themis" / "roles" / f"{role}.md"
            self.assertTrue(path.is_file(), f"missing role document: {path}")

    def test_registry_matches_kernel_roles(self) -> None:
        self.assertEqual(set(ROLE_REGISTRY), set(GovernanceKernel.VALID_ROLES))

    def test_get_role_is_strict(self) -> None:
        self.assertTrue(get_role("planner").can_touch_code is False)
        with self.assertRaises(KeyError):
            get_role("wizard")


if __name__ == "__main__":
    unittest.main()
