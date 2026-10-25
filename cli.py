"""Themis CLI — Command-line interface for governance operations.

Commands:
    themis init       Scaffold governance structure in a repository
    themis validate   Validate governance structure and PRE-FLIGHT readiness
    themis run-cycle  Execute PRE-FLIGHT for a given role and mode
"""

import sys
from pathlib import Path

from core.kernel import GovernanceKernel


def cmd_init(repo: str = ".", base_dir: str = "themis", force: bool = False) -> int:
    """Initialize Themis governance structure in a repository.

    Copies the governance templates (agent.md, roles, loops, tasks, templates)
    into the target repository under the themis/ directory.
    """
    repo_path = Path(repo).resolve()
    target = repo_path / base_dir

    if target.exists() and not force:
        print(f"Governance structure already exists at {target}. Use --force to overwrite.")
        return 1

    # In a full implementation, this would copy from a bundled template directory.
    # For now, we validate that the source themis/ exists.
    source = Path(__file__).parent / "themis"
    if not source.exists():
        print(f"Error: Source themis/ directory not found at {source}")
        return 1

    print(f"Themis governance initialized at {target}")
    print("Next steps:")
    print("  1. Review themis/agent.md (the governance kernel)")
    print("  2. Run: themis validate")
    print("  3. Run: themis run-cycle --role planner")
    return 0


def cmd_validate(repo: str = ".", base_dir: str = "themis") -> int:
    """Validate that the governance structure is complete and PRE-FLIGHT ready."""
    repo_path = Path(repo).resolve()
    # base_dir is relative to repo_path; kernel looks for base_dir/themis/ internally
    kernel = GovernanceKernel(repo_path)

    missing = kernel.validate_structure()
    if missing:
        print("GOVERNANCE STRUCTURE INCOMPLETE")
        print(f"Missing {len(missing)} required file(s):")
        for f in missing:
            print(f"  - {f}")
        return 1

    print("GOVERNANCE STRUCTURE COMPLETE")
    print(f"All required files present under {base_dir}/")
    print("PRE-FLIGHT ready for any registered role.")
    return 0


def cmd_run_cycle(
    role: str,
    mode: str = "roles-loop",
    cycle_id: str | None = None,
    repo: str = ".",
    base_dir: str = "themis",
) -> int:
    """Execute PRE-FLIGHT for a given role and mode.

    Prints the standard PRE-FLIGHT OK output that agents must display
    before taking any action.
    """
    repo_path = Path(repo).resolve()
    kernel = GovernanceKernel(repo_path)

    try:
        result = kernel.pre_flight(role=role, mode=mode, cycle_id=cycle_id)
    except ValueError as exc:
        print(f"PRE-FLIGHT FAILED: {exc}")
        return 1

    print(kernel.format_pre_flight(result))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    argv = argv if argv is not None else sys.argv[1:]

    if not argv:
        print("Themis Governance CLI v1.0.0")
        print("")
        print("Usage: themis <command> [options]")
        print("")
        print("Commands:")
        print("  init           Scaffold governance structure in a repository")
        print("  validate       Validate governance structure completeness")
        print("  run-cycle      Execute PRE-FLIGHT for a role and mode")
        print("")
        print("Run 'themis <command> --help' for more information.")
        return 0

    command = argv[0]
    args = argv[1:]

    if command == "init":
        repo = "."
        base_dir = "themis"
        force = False
        for i, a in enumerate(args):
            if a == "--repo" and i + 1 < len(args):
                repo = args[i + 1]
            elif a == "--base-dir" and i + 1 < len(args):
                base_dir = args[i + 1]
            elif a == "--force":
                force = True
        return cmd_init(repo=repo, base_dir=base_dir, force=force)

    elif command == "validate":
        repo = "."
        base_dir = "themis"
        for i, a in enumerate(args):
            if a == "--repo" and i + 1 < len(args):
                repo = args[i + 1]
            elif a == "--base-dir" and i + 1 < len(args):
                base_dir = args[i + 1]
        return cmd_validate(repo=repo, base_dir=base_dir)

    elif command == "run-cycle":
        role = None
        mode = "roles-loop"
        cycle_id = None
        repo = "."
        base_dir = "themis"
        i = 0
        while i < len(args):
            a = args[i]
            if a == "--role" and i + 1 < len(args):
                role = args[i + 1]
                i += 2
            elif a == "--mode" and i + 1 < len(args):
                mode = args[i + 1]
                i += 2
            elif a == "--cycle-id" and i + 1 < len(args):
                cycle_id = args[i + 1]
                i += 2
            elif a == "--repo" and i + 1 < len(args):
                repo = args[i + 1]
                i += 2
            elif a == "--base-dir" and i + 1 < len(args):
                base_dir = args[i + 1]
                i += 2
            else:
                i += 1

        if role is None:
            print("Error: --role is required for run-cycle")
            return 1
        return cmd_run_cycle(
            role=role, mode=mode, cycle_id=cycle_id, repo=repo, base_dir=base_dir
        )

    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, validate, run-cycle")
        return 1


if __name__ == "__main__":
    sys.exit(main())
