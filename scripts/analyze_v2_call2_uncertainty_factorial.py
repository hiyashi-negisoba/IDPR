#!/usr/bin/env python3
"""Analyze the 49-target prompt/evidence factorial and its safe downstream arm."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze_v2_call2_overliteral_impact import (
    _answer_plan_delta,
    _rows,
    changed_symbolic_cases,
)

TargetKey = tuple[str, str, str, str, str]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _key(value: dict[str, Any]) -> TargetKey:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def _transition_counts(
    left: dict[TargetKey, str], right: dict[TargetKey, str], keys: list[TargetKey]
) -> dict[str, int]:
    return {
        f"{before}->{after}": count
        for (before, after), count in sorted(
            Counter((left[key], right[key]) for key in keys).items()
        )
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    review = json.loads(args.review.read_text(encoding="utf-8"))
    metadata = {_key(value): value for value in review["records"]}
    run = json.loads(args.run.read_text(encoding="utf-8"))
    arms: dict[str, dict[TargetKey, str]] = defaultdict(dict)
    for finding in run["findings"]:
        for assessment in finding["assessments"]:
            arms[str(finding["arm"])][_key(assessment)] = str(assessment["truth"])
    if any(values.keys() != metadata.keys() for values in arms.values()):
        raise ValueError("factorial arm target universes differ from the review")

    groups = {
        name: [
            key
            for key, value in metadata.items()
            if value["diagnostic_group"] == name
        ]
        for name in ("C_OVERLITERAL", "B_SAFE_EPISODE")
    }
    comparisons = {
        "prompt_at_occurrence": ("current_occurrence", "candidate_occurrence"),
        "evidence_under_current_prompt": ("current_occurrence", "current_mixed"),
        "prompt_at_mixed_evidence": ("current_mixed", "candidate_mixed"),
        "combined": ("current_occurrence", "candidate_mixed"),
    }
    transitions = {
        name: {
            group: _transition_counts(arms[left], arms[right], keys)
            for group, keys in groups.items()
        }
        for name, (left, right) in comparisons.items()
    }
    intended_agreement = {
        arm: {
            group: {
                "agree": sum(
                    truths[key] == metadata[key]["counterfactual_truth"] for key in keys
                ),
                "total": len(keys),
            }
            for group, keys in groups.items()
        }
        for arm, truths in arms.items()
    }

    baseline_results = _rows(args.link_baseline_e2e)
    safe_results = _rows(args.link_safe_episode_e2e)
    downstream = changed_symbolic_cases(baseline_results, safe_results)
    final_changed = [
        value["case_id"] for value in downstream if value["final_responsibility_changed"]
    ]
    answer_plan = _answer_plan_delta(
        args.link_baseline_answer_plans, args.link_safe_episode_answer_plans
    )

    return {
        "step": "v2_call2_uncertainty_policy_factorial_analysis",
        "inputs": {
            name: {"path": str(path), "sha256": _sha256(path)}
            for name, path in {
                "review": args.review,
                "run": args.run,
                "link_baseline_e2e": args.link_baseline_e2e,
                "link_safe_episode_e2e": args.link_safe_episode_e2e,
            }.items()
        },
        "target_counts": {name: len(keys) for name, keys in groups.items()},
        "arm_truth_counts": {
            arm: dict(Counter(truths.values())) for arm, truths in arms.items()
        },
        "transitions": transitions,
        "intended_agreement": intended_agreement,
        "prompt_decision": {
            "status": "REJECTED",
            "reason": (
                "no C improvement at occurrence scope; one known target regressed, and "
                "mixed evidence introduced a TRUE-to-FALSE reversal"
            ),
        },
        "safe_episode_decision": {
            "known_intended_recoveries": intended_agreement["current_mixed"][
                "B_SAFE_EPISODE"
            ]["agree"],
            "reviewed_targets": len(groups["B_SAFE_EPISODE"]),
            "opposite_known_values": sum(
                arms["current_mixed"][key]
                in {"TRUE", "FALSE"}
                and arms["current_mixed"][key]
                != metadata[key]["counterfactual_truth"]
                for key in groups["B_SAFE_EPISODE"]
            ),
        },
        "safe_episode_downstream": {
            "symbolic_changed_case_count": len(downstream),
            "final_responsibility_changed_cases": final_changed,
            "answer_plan": answer_plan,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--link-baseline-e2e", type=Path, required=True)
    parser.add_argument("--link-safe-episode-e2e", type=Path, required=True)
    parser.add_argument("--link-baseline-answer-plans", type=Path, required=True)
    parser.add_argument("--link-safe-episode-answer-plans", type=Path, required=True)
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
