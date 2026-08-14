#!/usr/bin/env python3
"""Compare a reviewed realization-link counterfactual through symbolic and AnswerPlan."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

TargetKey = tuple[str, str, str, str, str]


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


def _target_key(case_id: str, value: dict[str, Any]) -> TargetKey:
    instance = value["instance_key"]
    return (
        case_id,
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def assessment_truths(path: Path) -> dict[TargetKey, str]:
    truths: dict[TargetKey, str] = {}
    for case_id, row in _rows(path).items():
        for value in row.get("assessments", ()):
            key = _target_key(case_id, value)
            if key in truths:
                raise ValueError(f"duplicate assessment target: {key}")
            truths[key] = str(value["truth"])
    return truths


def _candidate_key(value: dict[str, Any]) -> TargetKey:
    return tuple(
        str(value[name])
        for name in (
            "case_id",
            "actor_id",
            "offense_ref",
            "occurrence_id",
            "predicate_ref",
        )
    )  # type: ignore[return-value]


def _liability_by_instance(row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        json.dumps(value["instance_key"], ensure_ascii=False, sort_keys=True): value[
            "result"
        ]
        for value in row.get("liability_results", ())
    }


def build_report(
    *,
    candidate_review: Path,
    baseline_call2: Path,
    counterfactual_call2: Path,
    baseline_e2e: Path,
    counterfactual_e2e: Path,
    baseline_answer_manifest: Path,
    counterfactual_answer_manifest: Path,
) -> dict[str, Any]:
    review = json.loads(candidate_review.read_text(encoding="utf-8"))
    candidates = review["candidates"]
    candidate_by_key = {_candidate_key(value): value for value in candidates}
    if len(candidate_by_key) != len(candidates):
        raise ValueError("duplicate reviewed candidate")

    baseline_truths = assessment_truths(baseline_call2)
    counterfactual_truths = assessment_truths(counterfactual_call2)
    if baseline_truths.keys() != counterfactual_truths.keys():
        raise ValueError("counterfactual changed the assessment target universe")
    changed_truths = {
        key: {"baseline": baseline_truths[key], "counterfactual": value}
        for key, value in counterfactual_truths.items()
        if baseline_truths[key] != value
    }
    expected_changes = {
        key: str(value["counterfactual_truth"])
        for key, value in candidate_by_key.items()
        if value.get("counterfactual_truth") is not None
    }
    if {key: value["counterfactual"] for key, value in changed_truths.items()} != expected_changes:
        raise ValueError("Call 2 delta differs from the reviewed counterfactual")
    for key, value in candidate_by_key.items():
        if baseline_truths.get(key) != value["production_truth"]:
            raise ValueError(f"reviewed production truth drifted: {key}")

    baseline_results = _rows(baseline_e2e)
    counterfactual_results = _rows(counterfactual_e2e)
    if baseline_results.keys() != counterfactual_results.keys():
        raise ValueError("E2E case universes differ")
    changed_cases: list[dict[str, Any]] = []
    for case_id in baseline_results:
        baseline_row = baseline_results[case_id]
        counterfactual_row = counterfactual_results[case_id]
        if baseline_row == counterfactual_row:
            continue
        baseline_liability = _liability_by_instance(baseline_row)
        counterfactual_liability = _liability_by_instance(counterfactual_row)
        changed_instances = [
            json.loads(key)
            for key in sorted(baseline_liability.keys() | counterfactual_liability.keys())
            if baseline_liability.get(key) != counterfactual_liability.get(key)
        ]
        changed_cases.append(
            {
                "case_id": case_id,
                "changed_liability_instances": changed_instances,
                "final_responsibility_changed": baseline_row.get("final_responsibility")
                != counterfactual_row.get("final_responsibility"),
            }
        )

    baseline_manifest = json.loads(baseline_answer_manifest.read_text(encoding="utf-8"))
    counterfactual_manifest = json.loads(
        counterfactual_answer_manifest.read_text(encoding="utf-8")
    )
    baseline_failures = {str(value["case_id"]) for value in baseline_manifest["failures"]}
    counterfactual_failures = {
        str(value["case_id"]) for value in counterfactual_manifest["failures"]
    }

    return {
        "step": "v2_realization_link_downstream_impact",
        "inputs": {
            name: {"path": str(path), "sha256": _sha256(path)}
            for name, path in {
                "candidate_review": candidate_review,
                "baseline_call2": baseline_call2,
                "counterfactual_call2": counterfactual_call2,
                "baseline_e2e": baseline_e2e,
                "counterfactual_e2e": counterfactual_e2e,
            }.items()
        },
        "candidate_count": len(candidates),
        "candidate_truth_counts": dict(
            Counter(str(value["production_truth"]) for value in candidates)
        ),
        "candidate_link_kind_counts": dict(
            Counter(str(value["link_kind"]) for value in candidates)
        ),
        "impact_class_counts": dict(
            Counter(str(value["impact_class"]) for value in candidates)
        ),
        "counterfactual_truth_change_count": len(changed_truths),
        "counterfactual_truth_changes": [
            {
                "target_key": list(key),
                **value,
            }
            for key, value in changed_truths.items()
        ],
        "symbolic_changed_case_count": len(changed_cases),
        "symbolic_changed_cases": changed_cases,
        "final_responsibility_changed_case_count": sum(
            value["final_responsibility_changed"] for value in changed_cases
        ),
        "answer_plan": {
            "baseline_cases_written": baseline_manifest["cases_written"],
            "counterfactual_cases_written": counterfactual_manifest["cases_written"],
            "failures_removed": sorted(baseline_failures - counterfactual_failures),
            "failures_added": sorted(counterfactual_failures - baseline_failures),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-review", type=Path, required=True)
    parser.add_argument("--baseline-call2", type=Path, required=True)
    parser.add_argument("--counterfactual-call2", type=Path, required=True)
    parser.add_argument("--baseline-e2e", type=Path, required=True)
    parser.add_argument("--counterfactual-e2e", type=Path, required=True)
    parser.add_argument("--baseline-answer-manifest", type=Path, required=True)
    parser.add_argument("--counterfactual-answer-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(
        candidate_review=args.candidate_review,
        baseline_call2=args.baseline_call2,
        counterfactual_call2=args.counterfactual_call2,
        baseline_e2e=args.baseline_e2e,
        counterfactual_e2e=args.counterfactual_e2e,
        baseline_answer_manifest=args.baseline_answer_manifest,
        counterfactual_answer_manifest=args.counterfactual_answer_manifest,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
