"""Themis CLI — command-line interface for governance operations.

Commands:
    themis init       Scaffold the governance structure in a repository
    themis validate   Validate the governance structure and PRE-FLIGHT readiness
    themis run-cycle  Execute PRE-FLIGHT for a given role and mode
"""

from __future__ import annotations

import argparse
import shutil
import sys
from importlib import resources
from pathlib import Path

from core import __version__
from core.kernel import GovernanceKernel


def _assets_dir() -> Path:
    """Return the directory that contains the bundled governance assets."""
    return Path(str(resources.files("themis")))


def _count_files(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file())


def cmd_init(repo: str = ".", base_dir: str = "themis", force: bool = False) -> int:
    """Scaffold the Themis governance structure in a repository.

    Copies the bundled governance assets (agent.md, roles, loops, tasks and
    templates) into ``<repo>/<base_dir>``.
    """
    repo_path = Path(repo).resolve()
    if not repo_path.is_dir():
        print(f"Error: repository path does not exist: {repo_path}")
        return 1

    source = _assets_dir().resolve()
    target = (repo_path / base_dir).resolve()

    if source == target:
        print("Error: target is the Themis source repository itself; nothing to scaffold.")
        return 1

    if target.exists():
        if not force:
            print(
                f"Governance structure already exists at {target}. "
                "Use --force to overwrite."
            )
            return 1
        shutil.rmtree(target)

    ignore = shutil.ignore_patterns("__init__.py", "__pycache__", "*.pyc")
    shutil.copytree(source, target, ignore=ignore)

    files = _count_files(target)
    print(f"Themis governance initialized at {target}")
    print(f"Files created: {files}")
    print("Next steps:")
    print(f"  1. Review {base_dir}/agent.md (the governance kernel)")
    print(f"  2. Run: themis validate --repo {repo_path} --base-dir {base_dir}")
    print(f"  3. Run: themis run-cycle --role planner --repo {repo_path}")
    return 0


def cmd_validate(repo: str = ".", base_dir: str = "themis") -> int:
    """Validate that the governance structure is complete and PRE-FLIGHT ready."""
    repo_path = Path(repo).resolve()
    kernel = GovernanceKernel(repo_path, base_dir_name=base_dir)

    missing = kernel.validate_structure()
    if missing:
        print("GOVERNANCE STRUCTURE INCOMPLETE")
        print(f"Missing {len(missing)} required file(s):")
        for item in missing:
            print(f"  - {item}")
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
    """Execute PRE-FLIGHT for a given role and mode."""
    repo_path = Path(repo).resolve()
    kernel = GovernanceKernel(repo_path, base_dir_name=base_dir)

    try:
        result = kernel.pre_flight(role=role, mode=mode, cycle_id=cycle_id)
    except ValueError as exc:
        print(f"PRE-FLIGHT FAILED: {exc}")
        return 1

    print(kernel.format_pre_flight(result))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="themis",
        description="Deterministic governance protocol for LLM agents.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Scaffold the governance structure in a repository"
    )
    init_parser.add_argument("--repo", default=".", help="Target repository (default: .)")
    init_parser.add_argument(
        "--base-dir", default="themis", help="Governance directory name (default: themis)"
    )
    init_parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing governance directory"
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Validate governance structure completeness"
    )
    validate_parser.add_argument(
        "--repo", default=".", help="Target repository (default: .)"
    )
    validate_parser.add_argument(
        "--base-dir", default="themis", help="Governance directory name (default: themis)"
    )

    cycle_parser = subparsers.add_parser(
        "run-cycle", help="Execute PRE-FLIGHT for a role and mode"
    )
    cycle_parser.add_argument(
        "--role",
        required=True,
        choices=sorted(GovernanceKernel.VALID_ROLES),
        help="Governance role",
    )
    cycle_parser.add_argument(
        "--mode",
        default="roles-loop",
        choices=sorted(GovernanceKernel.VALID_MODES),
        help="Operation mode (default: roles-loop)",
    )
    cycle_parser.add_argument(
        "--cycle-id", default=None, help="ISO timestamp (generated when omitted)"
    )
    cycle_parser.add_argument(
        "--repo", default=".", help="Target repository (default: .)"
    )
    cycle_parser.add_argument(
        "--base-dir", default="themis", help="Governance directory name (default: themis)"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        return cmd_init(repo=args.repo, base_dir=args.base_dir, force=args.force)
    if args.command == "validate":
        return cmd_validate(repo=args.repo, base_dir=args.base_dir)
    if args.command == "run-cycle":
        return cmd_run_cycle(
            role=args.role,
            mode=args.mode,
            cycle_id=args.cycle_id,
            repo=args.repo,
            base_dir=args.base_dir,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
