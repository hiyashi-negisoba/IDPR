"""Evaluation aggregation and statistics layer (A1).

The per-run scoring primitives already live in ``generation``/``verification``
and run inside ``scripts/run_fraud_irac_matrix.py``. Each matrix run emits, per
method, an ``overall_conclusion`` plus a residual list of validation
violations. This layer does **not** re-score answers; it reads those residual
violations across a *case set × method* grid and turns them into the
``idpr_research_draft.md`` §8.2 internal-consistency metrics, with paired
significance tests and bootstrap confidence intervals for the paper tables.

Boundary (2026-07-21): the metric machinery here is validated against existing
single-case reports plus synthetic multi-case fixtures. Producing paper numbers
requires running the matrix over the evaluation set (A3); this module is the
aggregation target that consumes those runs, not the sweep runner itself.

The mapping from a raw violation ``code`` to the named §8.2 metric it counts
against is a legal-semantic decision. It is isolated in :data:`METRIC_CODE_MAP`
so it can be reviewed and adjusted in one place without touching the loader or
the statistics.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np

# --------------------------------------------------------------------------- #
# §8.2 metric definitions.
# --------------------------------------------------------------------------- #
# A run *fails* a metric if it carries at least one residual violation whose
# ``code`` is in that metric's bucket. ``argument_conclusion_consistency`` is
# reported as a consistency rate (1 - fail rate); every other metric is a fail
# rate where lower is better. ``conclusion_flip`` is kept separate from
# ``contradiction`` because the draft lists them as distinct metrics: a flip is
# a document-level disagreement with the Scallop-computed conclusion, whereas a
# contradiction is a section-level disagreement inside the argument.
#
# LEGAL-SEMANTIC MAPPING — under user review. Adjust the code sets here only;
# the loader and statistics are mapping-agnostic.
METRIC_CODE_MAP: dict[str, set[str]] = {
    "argument_conclusion_consistency": {
        "section_plan_mismatch",
        "whole_irac_structure_mismatch",
        "missing_required_card_metadata",
        "missing_required_fact_metadata",
        "whole_irac_provenance_missing",
        "whole_irac_application_unit_missing",
        "missing_grounded_application",
        "answer_contract_violation",
        "duplicate_section_conclusion",
        "unknown_section",
        "unknown_section_conclusion",
    },
    "contradiction": {
        "section_conclusion_mismatch",
        "whole_irac_conclusion_mismatch",
        "backparsed_section_conclusion",
    },
    "unsupported_rule": {
        "unsupported_claim",
        "unknown_provenance_id",
        "claim_card_coverage",
        "inexact_claim_quote",
        "duplicate_claim",
        "claim_schema",
        "claim_case_mismatch",
    },
    "fact_hallucination": {
        "claim_fact_coverage",
    },
    "conclusion_flip": {
        "overall_conclusion_mismatch",
        "backparsed_overall_conclusion",
    },
}

# Metrics reported as "higher is better" (a consistency rate). Everything else
# is a fail rate where 0.0 is perfect.
CONSISTENCY_METRICS: frozenset[str] = frozenset({"argument_conclusion_consistency"})

METRIC_ORDER: tuple[str, ...] = (
    "argument_conclusion_consistency",
    "contradiction",
    "unsupported_rule",
    "fact_hallucination",
    "conclusion_flip",
)


@dataclass(frozen=True)
class RunRecord:
    """One (case, method) evaluation cell distilled from a matrix report."""

    case_id: str
    method_id: str
    overall_conclusion: str
    violation_codes: Counter[str] = field(default_factory=Counter)
    warm_latency_seconds: float = 0.0
    model_call_count: int = 0
    model_completion_tokens: int = 0
    status: str = "completed"
    source_path: str = ""

    def fails_metric(self, metric: str) -> bool:
        """Whether this run counts as a *failure* for ``metric``.

        For a consistency metric the bucket codes are still the failure codes;
        the rate inversion happens at aggregation time.
        """
        codes = METRIC_CODE_MAP[metric]
        return any(self.violation_codes.get(code, 0) for code in codes)


# --------------------------------------------------------------------------- #
# Loading.
# --------------------------------------------------------------------------- #
def _residual_codes(method: Mapping[str, Any]) -> Counter[str]:
    """Residual violation codes for a method entry.

    Mirrors how ``method_summary`` decides ``status``: the recorded
    ``answer_validation_violations`` plus, for the claim-verified path, the
    verifier's ``violations_after`` (post-repair residue).
    """
    codes: Counter[str] = Counter()
    for violation in method.get("answer_validation_violations", []) or []:
        code = violation.get("code")
        if code:
            codes[code] += 1
    verification = method.get("claim_verification") or {}
    for violation in verification.get("violations_after", []) or []:
        code = violation.get("code")
        if code:
            codes[code] += 1
    return codes


def records_from_report(report: Mapping[str, Any], *, source_path: str = "") -> list[RunRecord]:
    """Turn one matrix report (single case, many methods) into run records."""
    case_id = report.get("case", {}).get("case_id", "")
    records: list[RunRecord] = []
    for method in report.get("methods", []) or []:
        answer = method.get("answer", {}) or {}
        records.append(
            RunRecord(
                case_id=case_id,
                method_id=method.get("method_id", ""),
                overall_conclusion=answer.get("overall_conclusion", ""),
                violation_codes=_residual_codes(method),
                warm_latency_seconds=float(method.get("warm_latency_seconds", 0.0) or 0.0),
                model_call_count=int(method.get("model_call_count", 0) or 0),
                model_completion_tokens=int(method.get("model_completion_tokens", 0) or 0),
                status=method.get("status", "completed"),
                source_path=source_path,
            )
        )
    return records


def _iter_report_paths(paths: Iterable[Path | str]) -> list[Path]:
    """Expand paths: a directory contributes every matrix report it
    (recursively) contains; a file is taken as-is."""
    resolved: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            resolved.extend(sorted(path.rglob("fraud_irac_matrix_report.json")))
        elif path.is_file():
            resolved.append(path)
        else:
            raise FileNotFoundError(f"no such report path: {path}")
    return resolved


def load_matrix_reports(paths: Iterable[Path | str]) -> list[RunRecord]:
    """Load run records from one or more matrix reports or directories.

    A (case_id, method_id) pair may legitimately recur (repeated runs of the
    same case). The last occurrence wins so a re-run supersedes an earlier one;
    callers wanting every replicate should build records directly.
    """
    by_cell: dict[tuple[str, str], RunRecord] = {}
    for path in _iter_report_paths(paths):
        report = json.loads(path.read_text(encoding="utf-8"))
        for record in records_from_report(report, source_path=str(path)):
            by_cell[(record.case_id, record.method_id)] = record
    return list(by_cell.values())


# --------------------------------------------------------------------------- #
# Statistics.
# --------------------------------------------------------------------------- #
def _fail_indicator(records: Sequence[RunRecord], metric: str) -> dict[str, int]:
    """{case_id -> 0/1 failure indicator} for a single method's records."""
    return {r.case_id: int(r.fails_metric(metric)) for r in records}


def bootstrap_rate_ci(
    indicators: Sequence[int],
    *,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Point estimate and percentile bootstrap CI of a mean over cases.

    Returns ``(rate, lo, hi)``. Cases are the resampling unit (paired designs
    resample case *indices*, not methods). Deterministic given ``seed``.
    """
    values = np.asarray(indicators, dtype=float)
    n = values.size
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    rate = float(values.mean())
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = values[idx].mean(axis=1)
    lo = float(np.quantile(means, alpha / 2))
    hi = float(np.quantile(means, 1 - alpha / 2))
    return (rate, lo, hi)


def mcnemar_exact(baseline: Sequence[int], treatment: Sequence[int]) -> dict[str, Any]:
    """Two-sided exact McNemar test on paired binary failure indicators.

    ``baseline``/``treatment`` are aligned per case (same order). Discordant
    pairs: ``b`` = baseline fails & treatment passes, ``c`` = baseline passes &
    treatment fails. Exact two-sided p-value from Binomial(b + c, 0.5).
    """
    if len(baseline) != len(treatment):
        raise ValueError("paired indicators must be the same length")
    b = sum(1 for x, y in zip(baseline, treatment) if x == 1 and y == 0)
    c = sum(1 for x, y in zip(baseline, treatment) if x == 0 and y == 1)
    n = b + c
    if n == 0:
        p_value = 1.0
    else:
        k = min(b, c)
        tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2**n)
        p_value = min(1.0, 2 * tail)
    return {
        "baseline_only_failures": b,
        "treatment_only_failures": c,
        "discordant_pairs": n,
        "p_value": p_value,
    }


# --------------------------------------------------------------------------- #
# Aggregation.
# --------------------------------------------------------------------------- #
def _paired_case_ids(records_by_method: Mapping[str, list[RunRecord]]) -> list[str]:
    """Case ids present for *every* method (the paired evaluation universe)."""
    if not records_by_method:
        return []
    common: set[str] | None = None
    for records in records_by_method.values():
        ids = {r.case_id for r in records}
        common = ids if common is None else (common & ids)
    return sorted(common or set())


def summarize(
    records: Sequence[RunRecord],
    *,
    baseline: str = "m1_direct",
    reference: str = "m5_irac_plan",
    metrics: Sequence[str] = METRIC_ORDER,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0,
) -> dict[str, Any]:
    """Aggregate §8.2 metrics over the paired case set × method grid.

    ``reference`` (IDPR, default M5) is compared against ``baseline`` with an
    exact McNemar test per metric. Rates carry bootstrap CIs. Only cases run by
    every method are counted, so all methods share one paired universe.
    """
    by_method: dict[str, list[RunRecord]] = {}
    for record in records:
        by_method.setdefault(record.method_id, []).append(record)

    paired_cases = _paired_case_ids(by_method)
    methods = sorted(by_method)

    method_summaries: dict[str, Any] = {}
    for method in methods:
        indicator_map = {m: _fail_indicator(by_method[method], m) for m in metrics}
        latencies = [
            r.warm_latency_seconds for r in by_method[method] if r.case_id in paired_cases
        ]
        calls = [r.model_call_count for r in by_method[method] if r.case_id in paired_cases]
        metric_block: dict[str, Any] = {}
        for metric in metrics:
            indicators = [indicator_map[metric][cid] for cid in paired_cases]
            fails = sum(indicators)
            fail_rate, fail_lo, fail_hi = bootstrap_rate_ci(
                indicators, n_boot=n_boot, alpha=alpha, seed=seed
            )
            reported = 1.0 - fail_rate if metric in CONSISTENCY_METRICS else fail_rate
            lo, hi = (
                (1.0 - fail_hi, 1.0 - fail_lo)
                if metric in CONSISTENCY_METRICS
                else (fail_lo, fail_hi)
            )
            metric_block[metric] = {
                "higher_is_better": metric in CONSISTENCY_METRICS,
                "rate": reported,
                "ci_low": lo,
                "ci_high": hi,
                "failures": fails,
                "n": len(paired_cases),
            }
        method_summaries[method] = {
            "n_cases": len(paired_cases),
            "metrics": metric_block,
            "median_latency_seconds": float(np.median(latencies)) if latencies else 0.0,
            "median_model_calls": float(np.median(calls)) if calls else 0.0,
            "conclusion_distribution": dict(
                Counter(
                    r.overall_conclusion
                    for r in by_method[method]
                    if r.case_id in paired_cases
                )
            ),
        }

    comparisons: dict[str, Any] = {}
    if baseline in by_method and reference in by_method:
        for metric in metrics:
            base_ind = _fail_indicator(by_method[baseline], metric)
            ref_ind = _fail_indicator(by_method[reference], metric)
            base_vec = [base_ind[cid] for cid in paired_cases]
            ref_vec = [ref_ind[cid] for cid in paired_cases]
            comparisons[metric] = mcnemar_exact(base_vec, ref_vec)

    return {
        "paired_case_count": len(paired_cases),
        "paired_case_ids": paired_cases,
        "methods": method_summaries,
        "baseline": baseline,
        "reference": reference,
        "comparisons": comparisons,
        "config": {
            "metrics": list(metrics),
            "n_boot": n_boot,
            "alpha": alpha,
            "seed": seed,
        },
        "metric_code_map": {m: sorted(codes) for m, codes in METRIC_CODE_MAP.items()},
    }


# --------------------------------------------------------------------------- #
# Rendering.
# --------------------------------------------------------------------------- #
_METRIC_LABELS = {
    "argument_conclusion_consistency": "argument-conclusion consistency",
    "contradiction": "contradiction rate",
    "unsupported_rule": "unsupported rule rate",
    "fact_hallucination": "fact hallucination rate",
    "conclusion_flip": "conclusion flip rate",
}


def render_markdown(summary: Mapping[str, Any]) -> str:
    """Paper-oriented markdown table: method × §8.2 metric (rate [CI])."""
    metrics = summary["config"]["metrics"]
    n = summary["paired_case_count"]
    lines = [
        f"# §8.2 internal-consistency summary (paired n={n})",
        "",
        f"Baseline `{summary['baseline']}` vs reference `{summary['reference']}`; "
        "cells are rate [95% bootstrap CI]. Arrows: ↑ higher is better, ↓ lower is better.",
        "",
    ]
    header = (
        ["method"]
        + [
            f"{_METRIC_LABELS.get(m, m)} " + ("↑" if m in CONSISTENCY_METRICS else "↓")
            for m in metrics
        ]
        + ["median s", "calls"]
    )
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for method in sorted(summary["methods"]):
        block = summary["methods"][method]
        cells = [f"`{method}`"]
        for metric in metrics:
            m = block["metrics"][metric]
            cells.append(f"{m['rate']:.2f} [{m['ci_low']:.2f}, {m['ci_high']:.2f}]")
        cells.append(f"{block['median_latency_seconds']:.1f}")
        cells.append(f"{block['median_model_calls']:.0f}")
        lines.append("| " + " | ".join(cells) + " |")

    if summary.get("comparisons"):
        lines += [
            "",
            f"## Paired McNemar: `{summary['reference']}` vs `{summary['baseline']}`",
            "",
        ]
        lines.append(
            "| metric | baseline-only fails | reference-only fails | discordant | p (exact) |"
        )
        lines.append("| --- | --- | --- | --- | --- |")
        for metric in metrics:
            c = summary["comparisons"].get(metric)
            if not c:
                continue
            lines.append(
                f"| {_METRIC_LABELS.get(metric, metric)} | {c['baseline_only_failures']} "
                f"| {c['treatment_only_failures']} | {c['discordant_pairs']} "
                f"| {c['p_value']:.3f} |"
            )
    return "\n".join(lines) + "\n"
