#!/usr/bin/env python3
"""Build an exact-key review packet for the residual Call 2 UNKNOWN diagnostic."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ARMS = ("occurrence_span", "factual_episode", "full_case_text")


def jsonl(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(value["sub_question_id"]): value
        for value in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def bucket(truths: tuple[str, str, str]) -> str:
    occurrence, episode, full = truths
    if occurrence == "UNKNOWN" and episode in {"TRUE", "FALSE"} and full == episode:
        return "B_EPISODE_SCOPE_CONFIRMED"
    if occurrence == "UNKNOWN" and episode == "UNKNOWN" and full in {"TRUE", "FALSE"}:
        return "A_OR_CASE_CONTEXT_REVIEW"
    if occurrence == episode == full == "UNKNOWN":
        return "C_OR_D_PERSISTENT_REVIEW"
    return "UNSTABLE_OR_DRIFT"


def meanings(definitions: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for name in ("ground_facts.yaml", "legal_elements.yaml"):
        values = yaml.safe_load((definitions / name).read_text(encoding="utf-8"))
        for value in values:
            output[str(value["id"])] = str(value.get("canonical_meaning") or "")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostic", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    diagnostic = json.loads(args.diagnostic.read_text(encoding="utf-8"))
    plans = jsonl(args.plan)
    issues = jsonl(args.issue_bindings)
    inventory = jsonl(args.inventory)
    predicate_meanings = meanings(args.definitions)

    arm_truths: dict[str, dict[tuple[str, str, str, str, str], str]] = {}
    for finding in diagnostic["findings"]:
        arm_truths.setdefault(str(finding["arm"]), {}).update(
            {key(value): str(value["truth"]) for value in finding["assessments"]}
        )
    if set(arm_truths) != set(ARMS):
        raise ValueError(f"expected arms {ARMS!r}, got {sorted(arm_truths)!r}")
    target_keys = set.intersection(*(set(arm_truths[arm]) for arm in ARMS))
    if any(set(arm_truths[arm]) != target_keys for arm in ARMS):
        raise ValueError("diagnostic arms do not carry the same exact target keys")

    occurrence_text = {
        (case_id, str(value["occurrence_id"])): str(value["source_text"])
        for case_id, plan in plans.items()
        for value in plan["occurrences"]
    }
    episode_by_occurrence: dict[tuple[str, str], str] = {}
    episode_text: dict[tuple[str, str], str] = {}
    for case_id, issue in issues.items():
        case_text = str(inventory[case_id]["question_text"])
        for episode in issue.get("factual_episodes", []):
            spans = [
                value["source_span"]
                for value in episode.get("source_fragments", [])
                if isinstance(value, dict) and isinstance(value.get("source_span"), dict)
            ]
            if spans:
                start = min(int(value["start"]) for value in spans)
                end = max(int(value["end"]) for value in spans)
                episode_text[(case_id, str(episode["factual_episode_id"]))] = case_text[
                    start:end
                ]
        for seed in issue.get("seed_results", []):
            for binding in seed.get("bindings", []):
                episode_by_occurrence[(case_id, str(binding["binding_id"]))] = str(
                    binding["factual_episode_id"]
                )
        for binding in plans[case_id].get("derived_binding_candidates", []):
            episode_by_occurrence[(case_id, str(binding["binding_id"]))] = str(
                binding["factual_episode_id"]
            )

    records = []
    for target in sorted(target_keys):
        case_id, actor_id, offense_ref, occurrence_id, predicate_ref = target
        truths = tuple(arm_truths[arm][target] for arm in ARMS)
        episode_id = episode_by_occurrence.get((case_id, occurrence_id))
        records.append(
            {
                "review_id": f"RU-{len(records) + 1:03d}",
                "operational_bucket": bucket(truths),
                "instance_key": {
                    "case_id": case_id,
                    "actor_id": actor_id,
                    "offense_ref": offense_ref,
                    "occurrence_id": occurrence_id,
                },
                "predicate_ref": predicate_ref,
                "predicate_meaning": predicate_meanings.get(predicate_ref, ""),
                "truths": dict(zip(ARMS, truths, strict=True)),
                "occurrence_evidence": occurrence_text[(case_id, occurrence_id)],
                "factual_episode_id": episode_id,
                "factual_episode_evidence": episode_text.get(
                    (case_id, episode_id or ""), ""
                ),
                "case_text": str(inventory[case_id]["question_text"]),
                "legal_cause_review": None,
            }
        )

    counts = Counter(value["operational_bucket"] for value in records)
    patterns = Counter(
        tuple(value["truths"][arm] for arm in ARMS) for value in records
    )
    per_bucket_predicate: dict[str, Counter[str]] = defaultdict(Counter)
    for value in records:
        per_bucket_predicate[value["operational_bucket"]][value["predicate_ref"]] += 1
    report = {
        "step": "v2_call2_residual_unknown_review_packet",
        "source": {
            "diagnostic": str(args.diagnostic),
            "plan_sha256": diagnostic["plan_sha256"],
            "call2_artifact_sha256": diagnostic["call2_artifact_sha256"],
            "issue_bindings_sha256": diagnostic["issue_bindings_sha256"],
        },
        "target_count": len(records),
        "bucket_counts": dict(counts),
        "truth_patterns": [
            {"truths": dict(zip(ARMS, values, strict=True)), "count": count}
            for values, count in patterns.most_common()
        ],
        "per_bucket_predicate": {
            name: dict(values.most_common())
            for name, values in per_bucket_predicate.items()
        },
        "records": records,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Residual UNKNOWN 232개 검수 packet",
        "",
        (
            "이 문서는 evidence arm의 **실측 패턴**만 자동 분류한다. "
            "`legal_cause_review`의 A/B/C/D는 법률·representation 검수 전에는 "
            "확정하지 않는다."
        ),
        "",
        "| operational bucket | count | 의미 |",
        "| --- | ---: | --- |",
        f"| B_EPISODE_SCOPE_CONFIRMED | {counts['B_EPISODE_SCOPE_CONFIRMED']} | occurrence U -> episode/full 동일 known |",
        f"| A_OR_CASE_CONTEXT_REVIEW | {counts['A_OR_CASE_CONTEXT_REVIEW']} | occurrence/episode U -> full known; 오배치와 case context 혼재 |",
        f"| C_OR_D_PERSISTENT_REVIEW | {counts['C_OR_D_PERSISTENT_REVIEW']} | 세 arm 모두 U; 초literal과 진짜 법적 쟁점 분리 필요 |",
        f"| UNSTABLE_OR_DRIFT | {counts['UNSTABLE_OR_DRIFT']} | evidence 효과로 귀속할 수 없는 비단조·재호출 변동 |",
        "",
    ]
    for name in (
        "B_EPISODE_SCOPE_CONFIRMED",
        "A_OR_CASE_CONTEXT_REVIEW",
        "C_OR_D_PERSISTENT_REVIEW",
        "UNSTABLE_OR_DRIFT",
    ):
        lines.extend([f"## {name}", "", "| predicate | count |", "| --- | ---: |"])
        lines.extend(
            f"| `{predicate}` | {count} |"
            for predicate, count in per_bucket_predicate[name].most_common()
        )
        lines.append("")
    args.out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.out_json}")
    print(f"wrote {args.out_md}")


if __name__ == "__main__":
    main()
