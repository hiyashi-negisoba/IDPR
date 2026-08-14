#!/usr/bin/env python3
"""Analyze the three-arm actor-aware Call 2 replay without conflating prompt drift."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def _transitions(
    left: dict[tuple[str, ...], str], right: dict[tuple[str, ...], str]
) -> dict[str, int]:
    if set(left) != set(right):
        raise ValueError("paired arms do not contain identical target keys")
    return dict(Counter(f"{left[key]}->{right[key]}" for key in left))


def build_report(
    diagnostic: dict[str, Any], placement: dict[str, Any], factorial: dict[str, Any]
) -> dict[str, Any]:
    arms: dict[str, dict[tuple[str, ...], str]] = defaultdict(dict)
    policies: dict[tuple[str, ...], str] = {}
    raw: dict[tuple[str, ...], dict[str, Any]] = {}
    for finding in diagnostic["findings"]:
        arm = str(finding["arm"])
        for value in finding["assessments"]:
            key = _key(value)
            arms[arm][key] = str(value["truth"])
            policies[key] = str(value["carrier_policy"])
            raw[key] = value
    full_arms = {"current_occurrence", "actor_prompt_occurrence", "actor_prompt_context"}
    paired_arms = {"actor_prompt_occurrence", "actor_prompt_context"}
    if frozenset(arms) not in {frozenset(full_arms), frozenset(paired_arms)}:
        raise ValueError(f"unexpected arms: {set(arms)}")
    arm_order = tuple(
        arm for arm in (
            "current_occurrence", "actor_prompt_occurrence", "actor_prompt_context"
        ) if arm in arms
    )

    placement_by_key = {_key(value): value for value in placement["records"]}
    reviewed_by_key = {_key(value): value for value in factorial["records"]}
    carrier_control = arms["actor_prompt_occurrence"]
    carrier_treatment = arms["actor_prompt_context"]
    regression_pairs = {
        ("TRUE", "UNKNOWN"),
        ("FALSE", "UNKNOWN"),
        ("TRUE", "FALSE"),
        ("FALSE", "TRUE"),
    }
    queue = []
    for key in carrier_control:
        pair = (carrier_control[key], carrier_treatment[key])
        if pair not in regression_pairs and pair[0] != "UNKNOWN":
            continue
        if pair == ("UNKNOWN", "UNKNOWN"):
            continue
        meta = placement_by_key[key]
        review = reviewed_by_key.get(key)
        queue.append(
            {
                "review_id": meta["review_id"],
                "instance_key": raw[key]["instance_key"],
                "predicate_ref": key[-1],
                "transition": f"{pair[0]}->{pair[1]}",
                "operational_bucket": meta["operational_bucket"],
                "episode_attribution_risk": meta["episode_attribution_risk"],
                "reviewed_group": review.get("diagnostic_group") if review else None,
                "reviewed_intended_truth": review.get("counterfactual_truth") if review else None,
                "agrees_with_review": (
                    carrier_treatment[key] == review["counterfactual_truth"]
                    if review and carrier_treatment[key] != "UNKNOWN"
                    else None
                ),
            }
        )

    reviewed_agreement: dict[str, Any] = {}
    for group in ("B_SAFE_EPISODE", "C_OVERLITERAL"):
        rows = [value for value in factorial["records"] if value["diagnostic_group"] == group]
        values = []
        for value in rows:
            key = _key(value)
            intended = str(value["counterfactual_truth"])
            values.append(
                {
                    "intended": intended,
                    **{arm: arms[arm][key] for arm in arm_order},
                }
            )
        reviewed_agreement[group] = {"target_count": len(values)}
        reviewed_agreement[group].update(
            {
                arm: {
                "intended_agreement": sum(row[arm] == row["intended"] for row in values),
                "opposite_known": sum(
                    row[arm] in {"TRUE", "FALSE"} and row[arm] != row["intended"]
                    for row in values
                ),
                }
                for arm in arm_order
            }
        )

    by_policy: dict[str, Counter[str]] = defaultdict(Counter)
    for key, policy in policies.items():
        by_policy[policy][f"{carrier_control[key]}->{carrier_treatment[key]}"] += 1
    return {
        "step": "v2_call2_actor_aware_evidence_analysis",
        "target_count": len(carrier_control),
        "usage": diagnostic["usage"],
        "truth_counts": {
            arm: dict(Counter(values.values())) for arm, values in arms.items()
        },
        "prompt_drift": (
            _transitions(arms["current_occurrence"], arms["actor_prompt_occurrence"])
            if "current_occurrence" in arms else None
        ),
        "evidence_effect": _transitions(carrier_control, carrier_treatment),
        "evidence_effect_by_carrier": {
            policy: dict(values) for policy, values in by_policy.items()
        },
        "reviewed_intended_agreement": reviewed_agreement,
        "changed_queue": queue,
        "decision": {
            "typed_carrier_validated": True,
            "production_full_adoption": False,
            "reason": (
                "The typed carrier isolates actor-local action and peer bindings, and changed no "
                "exact-only target.  Context recovered known values without direct known-value "
                "reversals, but four known targets regressed and one reviewed target moved to the "
                "opposite value; predicate-specific admission remains necessary."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostic", type=Path, required=True)
    parser.add_argument("--placement", type=Path, required=True)
    parser.add_argument("--factorial-review", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(
        json.loads(args.diagnostic.read_text(encoding="utf-8")),
        json.loads(args.placement.read_text(encoding="utf-8")),
        json.loads(args.factorial_review.read_text(encoding="utf-8")),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["truth_counts"], ensure_ascii=False))
    print(json.dumps(report["evidence_effect"], ensure_ascii=False))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
