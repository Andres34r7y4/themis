# ✅ Contribution Guide — Themis (EN)

Thanks for your interest in contributing to **Themis**, the deterministic
governance protocol for LLM agents.

## How to Contribute

1. **Fork** the repository.
2. Create a branch: `git checkout -b feature/your-improvement`
3. Make your changes and commit: `git commit -m "feat: description of change"`
4. Push to your branch: `git push origin feature/your-improvement`
5. Open a Pull Request describing the problem and the solution.

## Development setup

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python cli.py validate
```

The project supports Python 3.10+ and has no runtime dependencies.

## What to include in a PR

- A clear problem statement and the chosen solution.
- Tests for new behavior (or an explanation of why they are not applicable).
- Updates to `README.md`, `docs/`, and `CHANGELOG.md` when behavior changes.
- A note about the affected branch: `main` (Spanish) or `english`.

## PR Rules

- Any new feature must include documentation in Spanish (branch `main`) and
  English (branch `english`).
- Changes to the governance kernel (`agent.md`, `roles-loop.md`, roles) require
  review by at least two maintainers.
- No changes that break mandatory PRE-FLIGHT are accepted.
- No new dependencies without an explicit justification in the PR.
- Keep changes minimal, atomic, and reversible.

## Code style

- Follow the conventions of the surrounding code.
- Use type hints and `snake_case` for functions and variables.
- Keep the CLI and kernel deterministic and testable.

## Security

Report vulnerabilities privately as described in [docs/SECURITY.md](docs/SECURITY.md).
Do not open a public issue for a security problem.

## License

This project is under the [MIT](LICENSE) license.
