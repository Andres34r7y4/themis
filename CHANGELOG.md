# Change Log — Themis

## [v1.1.0] — 2026-10-25

### 🧰 Tooling and packaging

- Functional `themis init`: scaffolds the complete governance structure into any
  repository, with `--base-dir` and `--force` support.
- `themis validate` and `themis run-cycle` now honour `--base-dir`.
- Standard `argparse` CLI with `--version`, `--help`, and consistent exit codes.
- `pyproject.toml` now packages `cli.py` and the `themis` governance assets, so
  the installed `themis` command works.
- Minimum Python version is now 3.10, matching the type hints in use.
- Added a `unittest` test suite and GitHub Actions CI (Python 3.10–3.12).

### 🛠️ Kernel and roles

- Fixed the `STOP → STOP` transition and the anti-catastrophe flag/reason.
- `PLANNER_PHASE` can now transition to `DEBUGGER_PHASE` and `DESIGNER_PHASE`,
  matching the documented state machine.
- Unified the canonical role files on `themis/roles/designer.md`; removed the
  duplicated `disenador.md` asset and the contaminated references to another
  project (`AGENTS.md`, `UI_GOVERNANCE.md`).
- Standardized all ten role documents with the same structure: mission,
  PRE-FLIGHT, responsibilities, boundaries, inputs, outputs, handoff, and checklist.

### 📚 Documentation

- English `agent.md`, loops, roles, templates, and user guide aligned with the
  expanded Spanish contract.
- Corrected stale paths in `PATHS.md` (`themis/templates/`, real docs paths).
- README rewritten with accurate structure, CLI reference, badges, author, and
  donations section.
- `docs/EXAMPLES.md` now imports the real `core` package and reflects the
  functional CLI.
- `docs/SECURITY.md`, issue templates, and PR template translated to English on
  the `english` branch.

### 🔗 Author and support

- Added author and social links: GitHub, LinkedIn, and repository.
- Added donations: GitHub Sponsors, PayPal, and Buy Me a Coffee.

## [v1.0.0] — 2026-10-24

### 🚀 Initial Release

- **Governance Kernel**: `agent.md` with mandatory PRE-FLIGHT and role separation.
- **Orchestration Loop**: `roles-loop.md` with states `PLANNER_PHASE`,
  `EXECUTOR_PHASE`, `DEBUGGER_PHASE`, `DESIGNER_PHASE`, `STOP`.
- **Roles defined**: Planner, Executor, Debugger, Security Engineer, Architect,
  QA Engineer, Documentator, DevOps, Product Owner, Designer.
- **Frozen Context**: `context-freeze.md` for deterministic snapshots.
- **Memory Loop**: `memory-loop.md` for execution traceability.
- **Templates**: task, backlog, initial prompt, and run-roles-loop templates.
- **User Guide**: Complete operational documentation.
- **Banner Image**: Official banner in `docs/assets/themis-banner.jpeg`.
- **Multilingual**: Branch `main` in Spanish (default), branch `english` in English.

## Next Steps

- Publish both branches and keep the English documentation in sync with `main`.
- Add integration examples for specific provider SDKs (OpenAI, Anthropic,
  DeepSeek, Ollama) on top of the provider-agnostic prompt injection.
- Expand the test suite with integration tests for a scaffolded repository.
