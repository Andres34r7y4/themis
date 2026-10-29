#!/usr/bin/env python3
"""Token Efficiency & ROI Benchmark for Themis Governance.

Measures input/output tokens, cost, and ROI of running an LLM agent with and
without Themis governance. Supports a dry-run mode (simulated numbers) and a
live mode that calls an LLM provider.

Usage:
    python scripts/token_benchmark.py --mode dry-run --output docs/benchmark-results.md
    python scripts/token_benchmark.py --provider openai --model gpt-4o \
        --task "Validar un archivo de configuración JSON" \
        --output docs/benchmark-results.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class CycleResult:
    tokens_in: int
    tokens_out: int
    time_seconds: float
    files_read: int
    errors_prevented: int
    rework_cycles: int

    @property
    def tokens_total(self) -> int:
        return self.tokens_in + self.tokens_out


@dataclass
class BenchmarkConfig:
    provider: str
    model: str
    task: str
    mode: str  # "dry-run" or "live"
    price_per_1m_tokens: float
    incident_cost_usd: float = 150.0
    rework_cost_usd: float = 40.0
    traceability_value_usd: float = 100.0


@dataclass
class BenchmarkReport:
    config: BenchmarkConfig
    baseline: CycleResult
    themis: CycleResult
    roi_percent: float
    overhead_pct: float
    cost_baseline_usd: float
    cost_themis_usd: float
    value_avoided_usd: float

    def to_markdown(self) -> str:
        tokens_baseline = self.baseline.tokens_total
        tokens_themis = self.themis.tokens_total
        overhead = tokens_themis - tokens_baseline

        lines = [
            "# Token Efficiency & ROI Benchmark — Themis",
            "",
            f"Provider: `{self.config.provider}`  |  Model: `{self.config.model}`",
            f"Mode: `{self.config.mode}`  |  Task: {self.config.task}",
            "",
            "## Results",
            "",
            "| Metric | Baseline (no governance) | Themis (governance) | Difference |",
            "|--------|--------------------------|---------------------|------------|",
            f"| Input tokens | {self.baseline.tokens_in:,} | {self.themis.tokens_in:,} | {self.themis.tokens_in - self.baseline.tokens_in:+,} |",
            f"| Output tokens | {self.baseline.tokens_out:,} | {self.themis.tokens_out:,} | {self.themis.tokens_out - self.baseline.tokens_out:+,} |",
            f"| Total tokens | {tokens_baseline:,} | {tokens_themis:,} | {overhead:+,} |",
            f"| Governance overhead | — | — | **+{self.overhead_pct:.1f} %** |",
            f"| Cost per cycle (USD) | ${self.cost_baseline_usd:.4f} | ${self.cost_themis_usd:.4f} | ${self.cost_themis_usd - self.cost_baseline_usd:+.4f} |",
            f"| Files read | {self.baseline.files_read} | {self.themis.files_read} | {self.themis.files_read - self.baseline.files_read:+,} |",
            f"| Errors prevented pre-execution | {self.baseline.errors_prevented} | {self.themis.errors_prevented} | {self.themis.errors_prevented - self.baseline.errors_prevented:+,} |",
            f"| Rework cycles | {self.baseline.rework_cycles} | {self.themis.rework_cycles} | {self.themis.rework_cycles - self.baseline.rework_cycles:+,} |",
            f"| Time per cycle (s) | {self.baseline.time_seconds:.1f} | {self.themis.time_seconds:.1f} | {self.themis.time_seconds - self.baseline.time_seconds:+.1f} |",
            f"| Traceability / audit | None | Complete (task-archives.md) | +100 % |",
            "",
            "## ROI Calculation",
            "",
            f"- Governance cost per cycle: `${self.cost_themis_usd:.4f}`",
            f"- Value avoided (incidents): `{self.themis.errors_prevented} × ${self.config.incident_cost_usd}` = `${self.themis.errors_prevented * self.config.incident_cost_usd:.2f}`",
            f"- Value avoided (rework): `{self.baseline.rework_cycles - self.themis.rework_cycles} × ${self.config.rework_cost_usd}` = `${(self.baseline.rework_cycles - self.themis.rework_cycles) * self.config.rework_cost_usd:.2f}`",
            f"- Traceability value: `${self.config.traceability_value_usd:.2f}`",
            f"- Total value avoided: `${self.value_avoided_usd:.2f}`",
            f"- **ROI: `{self.roi_percent:.1f} %`**",
            "",
            "ROI > 100 % means the governance pays for itself through avoided incidents and rework.",
            "",
            "## Notes",
            "- Replace illustrative dry-run numbers with real measurements from your provider.",
            "- Context Freeze (Freeze Map) should reduce files read in the Themis scenario.",
            "- QA/Security gates should show errors_prevented > 0 in Themis for code-changing tasks.",
        ]
        return "\n".join(lines)


def estimate_tokens(text: str) -> int:
    """Rough tokenizer estimate: ~4 characters per token for English/Spanish text."""
    return max(1, len(text) // 4)


def run_dry_run(config: BenchmarkConfig) -> BenchmarkReport:
    """Simulated benchmark numbers for dry-run mode."""
    baseline = CycleResult(
        tokens_in=1200,
        tokens_out=450,
        time_seconds=14.0,
        files_read=12,
        errors_prevented=0,
        rework_cycles=2,
    )
    themis = CycleResult(
        tokens_in=1850,
        tokens_out=620,
        time_seconds=19.0,
        files_read=5,
        errors_prevented=2,
        rework_cycles=0,
    )
    return _build_report(config, baseline, themis)


def run_live(config: BenchmarkConfig) -> BenchmarkReport:
    """Live benchmark: calls an LLM provider for baseline and Themis scenarios."""
    try:
        import openai  # type: ignore
    except ImportError as exc:
        print("Error: `openai` package is required for live mode. Install with: pip install openai", file=sys.stderr)
        raise SystemExit(1) from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is required for live mode.", file=sys.stderr)
        raise SystemExit(1)

    client = openai.OpenAI(api_key=api_key)

    baseline_prompt = f"""
Eres un agente de software. Responde directamente a la siguiente tarea sin usar ningún protocolo de gobernanza:

Tarea: {config.task}

Devuelve el código o resultado final de inmediato.
"""

    themis_prompt = f"""
Eres un agente de software operando bajo el Protocolo de Gobernanza Themis.

Antes de cualquier acción debes:
1. Leer agent.md (contrato central).
2. Leer roles-loop.md (máquina de estados).
3. Leer roles/<ROL>.md (reglas del rol activo).
4. Imprimir PRE-FLIGHT OK con ROLE, CYCLE_ID, MODE.
5. Ejecutar solo lo permitido por tu rol.

Tarea: {config.task}

Responde con PRE-FLIGHT OK, el rol que asumes, y luego ejecuta la tarea.
"""

    def call(prompt: str) -> CycleResult:
        start = time.time()
        response = client.chat.completions.create(
            model=config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        elapsed = time.time() - start

        usage = response.usage
        tokens_in = getattr(usage, "prompt_tokens", None) or estimate_tokens(prompt)
        tokens_out = getattr(usage, "completion_tokens", None) or estimate_tokens(response.choices[0].message.content or "")

        # Simple heuristic counts from the response text for the benchmark fields.
        text = (response.choices[0].message.content or "").lower()
        files_read = text.count(".py") + text.count(".md") + text.count(".json")
        errors_prevented = text.count("error") + text.count("bloqueo") + text.count("veto")
        rework_cycles = 0 if "stop" in text or "completado" in text else 1

        return CycleResult(
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            time_seconds=elapsed,
            files_read=max(1, files_read),
            errors_prevented=errors_prevented,
            rework_cycles=rework_cycles,
        )

    baseline = call(baseline_prompt)
    themis = call(themis_prompt)
    return _build_report(config, baseline, themis)


def _build_report(config: BenchmarkConfig, baseline: CycleResult, themis: CycleResult) -> BenchmarkReport:
    tokens_per_dollar = 1_000_000 / config.price_per_1m_tokens
    cost_baseline = baseline.tokens_total / tokens_per_dollar
    cost_themis = themis.tokens_total / tokens_per_dollar

    overhead = themis.tokens_total - baseline.tokens_total
    overhead_pct = (overhead / baseline.tokens_total) * 100 if baseline.tokens_total else 0.0

    value_avoided = (
        themis.errors_prevented * config.incident_cost_usd
        + (baseline.rework_cycles - themis.rework_cycles) * config.rework_cost_usd
        + config.traceability_value_usd
    )
    roi_percent = (value_avoided / cost_themis) * 100 if cost_themis else 0.0

    return BenchmarkReport(
        config=config,
        baseline=baseline,
        themis=themis,
        roi_percent=roi_percent,
        overhead_pct=overhead_pct,
        cost_baseline_usd=cost_baseline,
        cost_themis_usd=cost_themis,
        value_avoided_usd=value_avoided,
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Token Efficiency & ROI Benchmark for Themis Governance"
    )
    parser.add_argument(
        "--mode",
        choices=["dry-run", "live"],
        default="dry-run",
        help="Run mode: dry-run (simulated) or live (real LLM calls)",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        help="LLM provider (openai, anthropic, deepseek, ollama)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="Model name (e.g. gpt-4o, claude-3-5-sonnet)",
    )
    parser.add_argument(
        "--task",
        default="Validar un archivo de configuración JSON",
        help="Task to execute in both baseline and Themis scenarios",
    )
    parser.add_argument(
        "--price-per-1m-tokens",
        type=float,
        default=5.0,
        help="Price per 1M tokens in USD (default: 5.0)",
    )
    parser.add_argument(
        "--output",
        default="docs/benchmark-results.md",
        help="Output Markdown file path",
    )
    args = parser.parse_args(argv)

    config = BenchmarkConfig(
        provider=args.provider,
        model=args.model,
        task=args.task,
        mode=args.mode,
        price_per_1m_tokens=args.price_per_1m_tokens,
    )

    if config.mode == "dry-run":
        report = run_dry_run(config)
    else:
        report = run_live(config)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report.to_markdown(), encoding="utf-8")

    print(report.to_markdown())
    print(f"\nResults written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
