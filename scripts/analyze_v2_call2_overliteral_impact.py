#!/usr/bin/env python3
"""Summarize reviewed over-literal Call 2 truth counterfactuals downstream."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze_v2_realization_link_impact import assessment_truths


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def changed_symbolic_cases(
    baseline: dict[str, dict[str, Any]],
    counterfactual: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if baseline.keys() != counterfactual.keys():
        raise ValueError("symbolic case universes differ")
    changed: list[dict[str, Any]] = []
    for case_id, baseline_row in baseline.items():
        counterfactual_row = counterfactual[case_id]
        if baseline_row == counterfactual_row:
            continue
        baseline_instances = {
            json.dumps(value["instance_key"], ensure_ascii=False, sort_keys=True): value[
                "result"
            ]
            for value in baseline_row.get("liability_results", ())
        }
        counterfactual_instances = {
            json.dumps(value["instance_key"], ensure_ascii=False, sort_keys=True): value[
                "result"
            ]
            for value in counterfactual_row.get("liability_results", ())
        }
        changed.append(
            {
                "case_id": case_id,
                "changed_instance_count": sum(
                    baseline_instances.get(key) != counterfactual_instances.get(key)
                    for key in baseline_instances.keys() | counterfactual_instances.keys()
                ),
                "final_responsibility_changed": baseline_row.get("final_responsibility")
                != counterfactual_row.get("final_responsibility"),
            }
        )
    return changed


def _answer_plan_delta(baseline_path: Path, counterfactual_path: Path) -> dict[str, Any]:
    baseline = _rows(baseline_path)
    counterfactual = _rows(counterfactual_path)
    common = baseline.keys() & counterfactual.keys()
    changed_fields: dict[str, list[str]] = {}
    fields = (
        "analysis",
        "open_points",
        "required_final_conclusions",
        "anchored_issue_count",
        "required_final_conclusion_count",
        "retained_offense_count",
    )
    for case_id in sorted(common):
        changed = [
            field
            for field in fields
            if baseline[case_id].get(field) != counterfactual[case_id].get(field)
        ]
        if changed:
            changed_fields[case_id] = changed
    return {
        "common_case_count": len(common),
        "changed_case_count": len(changed_fields),
        "changed_fields_by_case": changed_fields,
        "required_final_conclusion_changed_cases": sorted(
            case_id
            for case_id, changed in changed_fields.items()
            if "required_final_conclusions" in changed
        ),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    review = json.loads(args.candidate_review.read_text(encoding="utf-8"))
    candidates = review["records"]
    baseline_truths = assessment_truths(args.baseline_call2)
    high_truths = assessment_truths(args.high_call2)
    broad_truths = assessment_truths(args.broad_call2)
    if not (baseline_truths.keys() == high_truths.keys() == broad_truths.keys()):
        raise ValueError("Call 2 target universes differ")

    reviewed = {
        (
            str(value["instance_key"]["case_id"]),
            str(value["instance_key"]["actor_id"]),
            str(value["instance_key"]["offense_ref"]),
            str(value["instance_key"]["occurrence_id"]),
            str(value["predicate_ref"]),
        ): value
        for value in candidates
    }
    high_changes = {
        key: truth
        for key, truth in high_truths.items()
        if baseline_truths[key] != truth
    }
    broad_changes = {
        key: truth
        for key, truth in broad_truths.items()
        if baseline_truths[key] != truth
    }
    expected_high = {
        key: str(value["counterfactual_truth"])
        for key, value in reviewed.items()
        if value["tier"] == "C_HIGH"
    }
    expected_broad = {
        key: str(value["counterfactual_truth"]) for key, value in reviewed.items()
    }
    if high_changes != expected_high or broad_changes != expected_broad:
        raise ValueError("counterfactual truth delta differs from reviewed candidates")

    baseline_results = _rows(args.baseline_e2e)
    high_results = _rows(args.high_e2e)
    broad_results = _rows(args.broad_e2e)
    high_symbolic = changed_symbolic_cases(baseline_results, high_results)
    broad_symbolic = changed_symbolic_cases(baseline_results, broad_results)

    return {
        "step": "v2_call2_overliteral_downstream_impact",
        "inputs": {
            name: {"path": str(path), "sha256": _sha256(path)}
            for name, path in {
                "candidate_review": args.candidate_review,
                "baseline_call2": args.baseline_call2,
                "high_call2": args.high_call2,
                "broad_call2": args.broad_call2,
                "baseline_e2e": args.baseline_e2e,
                "high_e2e": args.high_e2e,
                "broad_e2e": args.broad_e2e,
            }.items()
        },
        "candidate_count": len(candidates),
        "tier_counts": dict(Counter(str(value["tier"]) for value in candidates)),
        "counterfactual_truth_counts": dict(
            Counter(str(value["counterfactual_truth"]) for value in candidates)
        ),
        "high": {
            "truth_change_count": len(high_changes),
            "symbolic_changed_case_count": len(high_symbolic),
            "symbolic_changed_cases": high_symbolic,
            "final_responsibility_changed_case_count": sum(
                value["final_responsibility_changed"] for value in high_symbolic
            ),
        },
        "broad": {
            "truth_change_count": len(broad_changes),
            "symbolic_changed_case_count": len(broad_symbolic),
            "symbolic_changed_cases": broad_symbolic,
            "final_responsibility_changed_case_count": sum(
                value["final_responsibility_changed"] for value in broad_symbolic
            ),
        },
        "answer_plan_after_equal_link_fill": _answer_plan_delta(
            args.link_baseline_answer_plans, args.link_broad_answer_plans
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "candidate_review",
        "baseline_call2",
        "high_call2",
        "broad_call2",
        "baseline_e2e",
        "high_e2e",
        "broad_e2e",
        "link_baseline_answer_plans",
        "link_broad_answer_plans",
    ):
        parser.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
