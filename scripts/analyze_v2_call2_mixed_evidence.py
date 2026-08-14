#!/usr/bin/env python3
"""Analyze an exact-key occurrence-control / mixed-evidence paired replay."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def target_key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def transition_counts(
    control: dict[tuple[str, str, str, str, str], str],
    treatment: dict[tuple[str, str, str, str, str], str],
) -> Counter[tuple[str, str]]:
    if set(control) != set(treatment):
        raise ValueError("paired arms do not contain the same exact target keys")
    return Counter((control[key], treatment[key]) for key in control)


def _render_transitions(values: Counter[tuple[str, str]]) -> list[dict[str, Any]]:
    return [
        {"control": left, "mixed": right, "count": count}
        for (left, right), count in values.most_common()
    ]


def build_report(diagnostic: dict[str, Any], placement: dict[str, Any]) -> dict[str, Any]:
    arms: dict[str, dict[tuple[str, str, str, str, str], str]] = defaultdict(dict)
    carriers: dict[tuple[str, str, str, str, str], str] = {}
    raw_by_key: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    request_counts = Counter()
    for finding in diagnostic["findings"]:
        arm = str(finding["arm"])
        request_counts[arm] += int(finding["physical_request_count"])
        for value in finding["assessments"]:
            key = target_key(value)
            arms[arm][key] = str(value["truth"])
            if arm == "mixed_evidence":
                carriers[key] = str(value["evidence_carrier"])
                raw_by_key[key] = value
    if set(arms) != {"occurrence_control", "mixed_evidence"}:
        raise ValueError("diagnostic must contain exactly two paired arms")
    control = arms["occurrence_control"]
    mixed = arms["mixed_evidence"]
    total = transition_counts(control, mixed)

    placement_by_key = {
        target_key(value): value for value in placement.get("records", ())
    }
    if set(placement_by_key) != set(control):
        raise ValueError("placement packet does not exactly cover paired targets")

    by_carrier: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    by_operational: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    by_risk: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    regressions = []
    regression_pairs = {
        ("TRUE", "UNKNOWN"),
        ("FALSE", "UNKNOWN"),
        ("TRUE", "FALSE"),
        ("FALSE", "TRUE"),
    }
    for key in control:
        pair = (control[key], mixed[key])
        carrier = carriers[key]
        meta = placement_by_key[key]
        by_carrier[carrier][pair] += 1
        by_operational[str(meta["operational_bucket"])][pair] += 1
        risk = "RISK" if meta["episode_attribution_risk"] else "NO_STRUCTURAL_RISK"
        by_risk[risk][pair] += 1
        if pair in regression_pairs:
            regressions.append(
                {
                    "review_id": meta["review_id"],
                    "instance_key": raw_by_key[key]["instance_key"],
                    "predicate_ref": key[-1],
                    "transition": {"control": pair[0], "mixed": pair[1]},
                    "evidence_carrier": carrier,
                    "operational_bucket": meta["operational_bucket"],
                    "episode_attribution_risk": meta["episode_attribution_risk"],
                }
            )

    return {
        "step": "v2_call2_residual_unknown_mixed_evidence_review",
        "source": {
            "plan_sha256": diagnostic["plan_sha256"],
            "call2_artifact_sha256": diagnostic["call2_artifact_sha256"],
            "issue_bindings_sha256": diagnostic["issue_bindings_sha256"],
        },
        "target_count": len(control),
        "physical_request_counts": dict(request_counts),
        "usage": diagnostic["usage"],
        "carrier_counts": dict(Counter(carriers.values())),
        "truth_counts": {
            "occurrence_control": dict(Counter(control.values())),
            "mixed_evidence": dict(Counter(mixed.values())),
        },
        "transitions": _render_transitions(total),
        "transitions_by_carrier": {
            name: _render_transitions(values) for name, values in by_carrier.items()
        },
        "transitions_by_operational_bucket": {
            name: _render_transitions(values) for name, values in by_operational.items()
        },
        "transitions_by_attribution_risk": {
            name: _render_transitions(values) for name, values in by_risk.items()
        },
        "known_regressions_or_reversals": regressions,
    }


def _markdown(report: dict[str, Any]) -> str:
    counts = report["truth_counts"]
    carrier = report["transitions_by_carrier"]
    lines = [
        "# Mixed evidence paired 진단",
        "",
        "동일한 target grouping으로 occurrence control과 mixed carrier를 paired 실행했다.",
        "prompt·schema·question assumptions·target key는 같고 evidence text만 다르다.",
        "",
        f"- targets: {report['target_count']}",
        f"- requests: {report['physical_request_counts']}",
        f"- control truth: {counts['occurrence_control']}",
        f"- mixed truth: {counts['mixed_evidence']}",
        f"- carriers: {report['carrier_counts']}",
        "",
        "## Carrier별 paired transition",
        "",
    ]
    for name, transitions in carrier.items():
        rendered = ", ".join(
            f"{value['control']}->{value['mixed']} {value['count']}"
            for value in transitions
        )
        lines.append(f"- `{name}`: {rendered}")
    lines.extend(
        [
            "",
            "actor-action 31개는 전부 동일했다. factual episode 197개에서는 UNKNOWN 해소와 함께",
            "known->UNKNOWN 및 FALSE->TRUE도 발생했으므로 전면 production 채택 근거가 아니다.",
            "",
            "## known regression / reversal queue",
            "",
        ]
    )
    for value in report["known_regressions_or_reversals"]:
        instance = value["instance_key"]
        transition = value["transition"]
        lines.append(
            f"- `{value['review_id']}` {instance['case_id']} {instance['actor_id']} "
            f"{instance['offense_ref']} `{value['predicate_ref']}`: "
            f"{transition['control']} -> {transition['mixed']} "
            f"(collision={value['episode_attribution_risk']})"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostic", type=Path, required=True)
    parser.add_argument("--placement", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(
        json.loads(args.diagnostic.read_text(encoding="utf-8")),
        json.loads(args.placement.read_text(encoding="utf-8")),
    )
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.out_md.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps(report["truth_counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
