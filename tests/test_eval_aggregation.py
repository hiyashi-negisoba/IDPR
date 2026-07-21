from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import pytest

from idpr.eval import (
    METRIC_CODE_MAP,
    METRIC_ORDER,
    RunRecord,
    bootstrap_rate_ci,
    load_matrix_reports,
    mcnemar_exact,
    records_from_report,
    render_markdown,
    summarize,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_REPORT = PROJECT_ROOT / "data/e2e/fraud/irac_matrix/fraud_irac_matrix_report.json"


def _rec(case_id: str, method_id: str, codes: dict[str, int] | None = None, **kw) -> RunRecord:
    return RunRecord(
        case_id=case_id,
        method_id=method_id,
        overall_conclusion=kw.get("overall_conclusion", "established"),
        violation_codes=Counter(codes or {}),
        warm_latency_seconds=kw.get("warm_latency_seconds", 1.0),
        model_call_count=kw.get("model_call_count", 1),
    )


# --------------------------------------------------------------------------- #
# Metric mapping.
# --------------------------------------------------------------------------- #
def test_metric_code_map_partitions_codes_without_overlap():
    seen: Counter[str] = Counter()
    for codes in METRIC_CODE_MAP.values():
        seen.update(codes)
    overlaps = {code: n for code, n in seen.items() if n > 1}
    assert not overlaps, f"codes assigned to multiple metrics: {overlaps}"


def test_fails_metric_reads_bucket():
    rec = _rec("c1", "m5_irac_plan", {"section_conclusion_mismatch": 1})
    assert rec.fails_metric("contradiction")
    assert not rec.fails_metric("fact_hallucination")
    assert not rec.fails_metric("argument_conclusion_consistency")


# --------------------------------------------------------------------------- #
# Loading real report.
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not REAL_REPORT.exists(), reason="real matrix report absent")
def test_records_from_real_report():
    report = json.loads(REAL_REPORT.read_text(encoding="utf-8"))
    records = records_from_report(report, source_path=str(REAL_REPORT))
    by_method = {r.method_id: r for r in records}
    assert "m5_irac_plan" in by_method
    # The recorded m5 run carried contract + missing-card violations.
    m5 = by_method["m5_irac_plan"]
    assert m5.violation_codes.total() >= 1
    assert m5.fails_metric("argument_conclusion_consistency")
    # m1 direct recorded no residual violations.
    assert by_method["m1_direct"].violation_codes.total() == 0


@pytest.mark.skipif(not REAL_REPORT.exists(), reason="real matrix report absent")
def test_load_matrix_reports_dedupes_cells():
    records = load_matrix_reports([REAL_REPORT, REAL_REPORT])
    cells = [(r.case_id, r.method_id) for r in records]
    assert len(cells) == len(set(cells))


# --------------------------------------------------------------------------- #
# McNemar exact.
# --------------------------------------------------------------------------- #
def test_mcnemar_no_discordant_pairs_is_p1():
    out = mcnemar_exact([1, 0, 1], [1, 0, 1])
    assert out["discordant_pairs"] == 0
    assert out["p_value"] == 1.0


def test_mcnemar_all_discordant_one_direction():
    # baseline fails everywhere, treatment passes everywhere: 5 discordant, all b.
    out = mcnemar_exact([1, 1, 1, 1, 1], [0, 0, 0, 0, 0])
    assert out["baseline_only_failures"] == 5
    assert out["treatment_only_failures"] == 0
    assert out["discordant_pairs"] == 5
    # two-sided exact = 2 * (1/2)^5 = 0.0625
    assert out["p_value"] == pytest.approx(2 * (0.5**5))


def test_mcnemar_length_mismatch_raises():
    with pytest.raises(ValueError):
        mcnemar_exact([1, 0], [1])


# --------------------------------------------------------------------------- #
# Bootstrap CI.
# --------------------------------------------------------------------------- #
def test_bootstrap_ci_deterministic_and_bounded():
    ind = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    rate_a, lo_a, hi_a = bootstrap_rate_ci(ind, n_boot=2000, seed=7)
    rate_b, lo_b, hi_b = bootstrap_rate_ci(ind, n_boot=2000, seed=7)
    assert (rate_a, lo_a, hi_a) == (rate_b, lo_b, hi_b)
    assert rate_a == pytest.approx(0.5)
    assert 0.0 <= lo_a <= rate_a <= hi_a <= 1.0


def test_bootstrap_all_zero_is_point_mass():
    rate, lo, hi = bootstrap_rate_ci([0, 0, 0, 0], n_boot=500, seed=1)
    assert rate == 0.0 and lo == 0.0 and hi == 0.0


def test_bootstrap_empty_is_nan():
    rate, lo, hi = bootstrap_rate_ci([], n_boot=10, seed=1)
    assert math.isnan(rate) and math.isnan(lo) and math.isnan(hi)


# --------------------------------------------------------------------------- #
# Aggregation over a synthetic multi-case grid.
# --------------------------------------------------------------------------- #
def _synthetic_records() -> list[RunRecord]:
    records: list[RunRecord] = []
    for i in range(4):
        cid = f"case_{i}"
        # baseline m1: flips the conclusion on 3 of 4 cases.
        records.append(
            _rec(cid, "m1_direct", {"overall_conclusion_mismatch": 1} if i < 3 else {})
        )
        # reference m5: never flips (Scallop-fixed conclusion); clean.
        records.append(_rec(cid, "m5_irac_plan", {}))
    return records


def test_summarize_paired_universe_and_rates():
    summary = summarize(_synthetic_records(), n_boot=1000, seed=3)
    assert summary["paired_case_count"] == 4
    assert set(summary["methods"]) == {"m1_direct", "m5_irac_plan"}

    m1 = summary["methods"]["m1_direct"]["metrics"]
    m5 = summary["methods"]["m5_irac_plan"]["metrics"]
    # m1 flips on 3/4 cases.
    assert m1["conclusion_flip"]["rate"] == pytest.approx(0.75)
    assert m1["conclusion_flip"]["failures"] == 3
    # m5 never flips.
    assert m5["conclusion_flip"]["rate"] == 0.0
    # consistency is reported inverted (higher better); m5 fully consistent.
    assert m5["argument_conclusion_consistency"]["rate"] == 1.0
    assert m5["argument_conclusion_consistency"]["higher_is_better"] is True


def test_summarize_mcnemar_comparison_present():
    summary = summarize(_synthetic_records(), n_boot=500, seed=3)
    comp = summary["comparisons"]["conclusion_flip"]
    # baseline fails 3 where reference passes -> 3 baseline-only discordant.
    assert comp["baseline_only_failures"] == 3
    assert comp["treatment_only_failures"] == 0
    assert comp["discordant_pairs"] == 3


def test_summarize_paired_universe_drops_unshared_cases():
    records = _synthetic_records()
    # add a case only m1 ran; it must be excluded from the paired universe.
    records.append(_rec("case_only_m1", "m1_direct", {}))
    summary = summarize(records, n_boot=200, seed=1)
    assert summary["paired_case_count"] == 4
    assert "case_only_m1" not in summary["paired_case_ids"]


def test_render_markdown_smoke():
    summary = summarize(_synthetic_records(), n_boot=200, seed=1)
    md = render_markdown(summary)
    assert "internal-consistency summary" in md
    assert "m5_irac_plan" in md
    assert "McNemar" in md
    for metric in METRIC_ORDER:
        # every metric label fragment appears in the header
        assert metric.split("_")[0] in md
