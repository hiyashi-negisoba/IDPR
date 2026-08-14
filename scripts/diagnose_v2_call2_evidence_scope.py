#!/usr/bin/env python3
"""Ask what the Call 2 UNKNOWN rate is actually caused by: the evidence window.

73% of the plan's anchors end up undetermined, which costs the rubric's conclusion
items.  The assessor sees one occurrence's quoted span and is told that a fact merely
absent from it is UNKNOWN, so the question is whether those UNKNOWNs are genuine legal
indeterminacy or an artifact of showing it a third of the case.

This replays the residual UNKNOWN targets against the same served model with three
evidence carriers: the occurrence span used in production, the factual episode recorded
by Call 1.5, and the full case text.  Prompt, schema, predicate catalogue and target set
are identical between the arms -- only `evidence_occurrence.source_text` differs.

Nothing is installed and no artifact is rebuilt.  The output is a comparison table.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.question_assumptions import load_question_assumptions
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    call2_request_payload,
    call2_schema,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets_by_occurrence,
    validate_call2_output,
)


def rows(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[str(row["sub_question_id"])] = row
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factual_episode_evidence(
    issue_row: dict[str, Any], plan_row: dict[str, Any], case_text: str
) -> dict[str, str]:
    """Map every binding occurrence to its Call 1.5 factual-episode text."""
    episode_text: dict[str, str] = {}
    for episode in issue_row.get("factual_episodes", []):
        spans = [
            value.get("source_span")
            for value in episode.get("source_fragments", [])
            if isinstance(value, dict)
        ]
        spans = [
            value
            for value in spans
            if isinstance(value, dict)
            and isinstance(value.get("start"), int)
            and isinstance(value.get("end"), int)
        ]
        if not spans:
            continue
        start = min(value["start"] for value in spans)
        end = max(value["end"] for value in spans)
        if not 0 <= start < end <= len(case_text):
            raise ValueError("factual episode span is outside question_text")
        episode_text[str(episode["factual_episode_id"])] = case_text[start:end]

    occurrence_to_episode: dict[str, str] = {}
    for seed in issue_row.get("seed_results", []):
        for binding in seed.get("bindings", []):
            occurrence_to_episode[str(binding["binding_id"])] = str(
                binding["factual_episode_id"]
            )
    for binding in plan_row.get("derived_binding_candidates", []):
        occurrence_to_episode[str(binding["binding_id"])] = str(
            binding["factual_episode_id"]
        )
    return {
        occurrence_id: episode_text[episode_id]
        for occurrence_id, episode_id in occurrence_to_episode.items()
        if episode_id in episode_text
    }


def assessment_key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl")
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--question-assumptions",
        type=Path,
        default=ROOT / "data/v2/question_assumptions.jsonl",
    )
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    registry = load_definitions(args.definitions)
    inventory = rows(args.inventory)
    plans = rows(args.plan)
    frozen = rows(args.call2_artifact)
    issue_bindings = rows(args.issue_bindings)
    assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            key: str(value["question_prompt"]) for key, value in inventory.items()
        },
    )

    system_prompt = load_prompt("v2_call2_grounding")
    user_prompt = load_prompt("v2_call2_grounding_user")
    client = VLLMClient(base_url=args.base_url, model=args.model)

    findings: list[dict[str, Any]] = []
    selected = tuple(args.case_id) if args.case_id else tuple(plans)
    missing = [
        value
        for value in selected
        if value not in inventory
        or value not in plans
        or value not in frozen
        or value not in issue_bindings
    ]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")
    aggregate_usage = Counter()
    for case_id in selected:
        plan_row = plans[case_id]
        case_text = str(inventory[case_id]["question_text"])
        occurrences = {
            str(value["occurrence_id"]): GoldOccurrence(
                str(value["occurrence_id"]),
                str(value["actor_id"]),
                str(value["source_text"]),
                int(value["source_span"]["start"]),
                int(value["source_span"]["end"]),
            )
            for value in plan_row["occurrences"]
        }
        episode_evidence = factual_episode_evidence(
            issue_bindings[case_id], plan_row, case_text
        )

        targets = tuple(
            _target(value)
            for value in frozen[case_id].get("assessments", [])
            if value.get("truth") == "UNKNOWN"
        )
        if not targets:
            print(f"{case_id}: no residual UNKNOWN targets", file=sys.stderr)
            continue
        planner_keys = {
            assessment_key(value)
            for value in plan_row.get("assessment_targets", [])
        }
        outside = [value for value in targets if assessment_key(value.as_dict()) not in planner_keys]
        if outside:
            raise ValueError(f"{case_id}: residual target is outside planner scope")
        request_targets = grounding_request_targets(registry, targets)
        shards = shard_assessment_targets_by_occurrence(request_targets, max_targets=24)

        for arm in ("occurrence_span", "factual_episode", "full_case_text"):
            arm_assessments: list[dict[str, Any]] = []
            arm_usage = Counter()
            for shard in shards:
                occurrence_id = shard[0].instance_key.occurrence_id
                evidence = occurrences[occurrence_id]
                if arm == "factual_episode" and occurrence_id in episode_evidence:
                    text = episode_evidence[occurrence_id]
                    evidence = GoldOccurrence(
                        evidence.occurrence_id,
                        evidence.actor_id,
                        text,
                        0,
                        len(text),
                    )
                elif arm == "full_case_text":
                    evidence = GoldOccurrence(
                        evidence.occurrence_id,
                        evidence.actor_id,
                        case_text,
                        0,
                        len(case_text),
                    )
                refs = tuple(dict.fromkeys(value.predicate_ref for value in shard))
                payload = call2_request_payload(
                    evidence_occurrence=evidence,
                    question_assumptions=assumptions.get(case_id, ()),
                    predicates=predicate_definitions(registry, refs),
                    targets=shard,
                )
                assert_no_leaked_fields(payload)
                raw, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_occurrence_scoped_call2",
                    schema=call2_schema(shard),
                    max_tokens=args.max_tokens,
                    temperature=0.0,
                    user_template=user_prompt,
                )
                values = validate_call2_output(raw, targets=shard)
                arm_assessments.extend(value.as_dict() for value in values)
                usage = metadata.get("usage", {})
                for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                    amount = int(usage.get(key, 0) or 0)
                    arm_usage[key] += amount
                    aggregate_usage[key] += amount
            findings.append(
                {
                    "case_id": case_id,
                    "arm": arm,
                    "counts": dict(Counter(value["truth"] for value in arm_assessments)),
                    "physical_request_count": len(shards),
                    "usage": dict(arm_usage),
                    "assessments": arm_assessments,
                }
            )
            print(
                f"{case_id:28} {arm:16} "
                f"{dict(Counter(value['truth'] for value in arm_assessments))}"
            )

    baseline = {
        case_id: dict(Counter(value["truth"] for value in frozen[case_id]["assessments"]))
        for case_id in selected
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "step": "v2_call2_residual_unknown_evidence_scope",
                "plan_sha256": sha256(args.plan),
                "call2_artifact_sha256": sha256(args.call2_artifact),
                "issue_bindings_sha256": sha256(args.issue_bindings),
                "case_ids": list(selected),
                "residual_unknown_target_count": sum(
                    1
                    for case_id in selected
                    for value in frozen[case_id]["assessments"]
                    if value["truth"] == "UNKNOWN"
                ),
                "usage": dict(aggregate_usage),
                "frozen_run": baseline,
                "findings": findings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nfrozen run, for reference: {baseline}")


def _target(value: dict[str, Any]):
    from idpr.v2.runtime.grounding import AssessmentTarget
    from idpr.v2.runtime.identity import OffenseInstanceKey

    instance = value["instance_key"]
    return AssessmentTarget(
        instance_key=OffenseInstanceKey(
            case_id=str(instance["case_id"]),
            actor_id=str(instance["actor_id"]),
            offense_ref=str(instance["offense_ref"]),
            occurrence_id=str(instance["occurrence_id"]),
        ),
        predicate_ref=str(value["predicate_ref"]),
    )


if __name__ == "__main__":
    main()
