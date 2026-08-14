#!/usr/bin/env python3
"""Run an exact-target paired diagnostic for the approved over-literal policy draft."""

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
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.question_assumptions import load_question_assumptions
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from scripts.diagnose_v2_call2_evidence_scope import factual_episode_evidence

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


def _key(instance: dict[str, Any] | OffenseInstanceKey, predicate_ref: str) -> TargetKey:
    if isinstance(instance, OffenseInstanceKey):
        return (
            instance.case_id,
            instance.actor_id,
            instance.offense_ref,
            instance.occurrence_id,
            str(predicate_ref),
        )
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(predicate_ref),
    )


def reviewed_targets(path: Path) -> tuple[dict[str, list[AssessmentTarget]], dict[TargetKey, dict[str, Any]]]:
    review = json.loads(path.read_text(encoding="utf-8"))
    by_case: dict[str, list[AssessmentTarget]] = defaultdict(list)
    metadata: dict[TargetKey, dict[str, Any]] = {}
    for value in review["records"]:
        instance = value["instance_key"]
        target = AssessmentTarget(
            OffenseInstanceKey(
                str(instance["case_id"]),
                str(instance["actor_id"]),
                str(instance["offense_ref"]),
                str(instance["occurrence_id"]),
            ),
            str(value["predicate_ref"]),
        )
        key = _key(instance, target.predicate_ref)
        if key in metadata:
            raise ValueError(f"duplicate reviewed target: {key}")
        by_case[target.instance_key.case_id].append(target)
        metadata[key] = value
    return dict(by_case), metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--candidate-review", type=Path, required=True)
    parser.add_argument(
        "--candidate-system-prompt",
        type=Path,
        default=ROOT / "prompts/candidates/v2_call2_grounding_overliteral_v1.md",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--question-assumptions",
        type=Path,
        default=ROOT / "data/v2/question_assumptions.jsonl",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    registry = load_definitions(args.definitions)
    plans = _rows(args.plan)
    frozen = _rows(args.call2_artifact)
    issues = _rows(args.issue_bindings)
    inventory = _rows(args.inventory)
    by_case, review_metadata = reviewed_targets(args.candidate_review)
    assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            case_id: str(value["question_prompt"]) for case_id, value in inventory.items()
        },
    )

    for case_id, targets in by_case.items():
        if (
            case_id not in plans
            or case_id not in frozen
            or case_id not in inventory
            or case_id not in issues
        ):
            raise ValueError(f"missing reviewed case: {case_id}")
        frozen_truths = {
            _key(value["instance_key"], str(value["predicate_ref"])): str(value["truth"])
            for value in frozen[case_id].get("assessments", ())
        }
        planner_keys = {
            _key(value["instance_key"], str(value["predicate_ref"]))
            for value in plans[case_id].get("assessment_targets", ())
        }
        for target in targets:
            key = _key(target.instance_key, target.predicate_ref)
            if frozen_truths.get(key) != "UNKNOWN":
                raise ValueError(f"reviewed target is not frozen UNKNOWN: {key}")
            if key not in planner_keys:
                raise ValueError(f"reviewed target is outside planner scope: {key}")

    current_prompt = load_prompt("v2_call2_grounding")
    candidate_prompt = args.candidate_system_prompt.read_text(encoding="utf-8")
    arms = (
        ("current_occurrence", current_prompt, False),
        ("candidate_occurrence", candidate_prompt, False),
        ("current_mixed", current_prompt, True),
        ("candidate_mixed", candidate_prompt, True),
    )
    user_prompt = load_prompt("v2_call2_grounding_user")
    client = VLLMClient(base_url=args.base_url, model=args.model)
    findings: list[dict[str, Any]] = []
    aggregate_usage = Counter()

    for case_id, reviewed in by_case.items():
        occurrences = {
            str(value["occurrence_id"]): GoldOccurrence(
                str(value["occurrence_id"]),
                str(value["actor_id"]),
                str(value["source_text"]),
                int(value["source_span"]["start"]),
                int(value["source_span"]["end"]),
            )
            for value in plans[case_id]["occurrences"]
        }
        episode_evidence = factual_episode_evidence(
            issues[case_id],
            plans[case_id],
            str(inventory[case_id]["question_text"]),
        )
        request_targets = grounding_request_targets(registry, tuple(reviewed))
        request_keys = {
            _key(value.instance_key, value.predicate_ref) for value in request_targets
        }
        reviewed_keys = {
            _key(value.instance_key, value.predicate_ref) for value in reviewed
        }
        if request_keys != reviewed_keys:
            raise ValueError(f"{case_id}: grounding projection changed reviewed target keys")
        fixed_groups: dict[tuple[str, str], list[AssessmentTarget]] = {}
        for target in request_targets:
            key = _key(target.instance_key, target.predicate_ref)
            group_key = (
                target.instance_key.occurrence_id,
                str(review_metadata[key].get("evidence_policy", "occurrence")),
            )
            fixed_groups.setdefault(group_key, []).append(target)
        shards = tuple(
            (group_key, shard)
            for group_key, group_targets in fixed_groups.items()
            for shard in shard_assessment_targets(group_targets, max_targets=24)
        )

        for arm, system_prompt, use_mixed_evidence in arms:
            assessments: list[dict[str, Any]] = []
            usage = Counter()
            for shard_index, (group_key, shard) in enumerate(shards, start=1):
                occurrence_id = shard[0].instance_key.occurrence_id
                evidence = occurrences[occurrence_id]
                if use_mixed_evidence and group_key[1] == "factual_episode":
                    text = episode_evidence.get(occurrence_id)
                    if text is None:
                        raise ValueError(f"{case_id}: missing factual episode evidence")
                    evidence = GoldOccurrence(
                        evidence.occurrence_id,
                        evidence.actor_id,
                        text,
                        0,
                        len(text),
                    )
                refs = tuple(dict.fromkeys(value.predicate_ref for value in shard))
                payload = call2_request_payload(
                    evidence_occurrence=evidence,
                    question_assumptions=assumptions.get(case_id, ()),
                    predicates=predicate_definitions(registry, refs),
                    targets=shard,
                )
                assert_no_leaked_fields(payload)
                raw, response = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_occurrence_scoped_call2",
                    schema=call2_schema(shard),
                    max_tokens=args.max_tokens,
                    temperature=0.0,
                    user_template=user_prompt,
                )
                values = validate_call2_output(raw, targets=shard)
                for value in values:
                    key = _key(value.target.instance_key, value.target.predicate_ref)
                    assessments.append(
                        {
                            **value.as_dict(),
                            "review_id": review_metadata[key]["review_id"],
                            "tier": review_metadata[key]["tier"],
                            "diagnostic_group": review_metadata[key].get(
                                "diagnostic_group", "C_OVERLITERAL"
                            ),
                            "evidence_policy": review_metadata[key].get(
                                "evidence_policy", "occurrence"
                            ),
                            "intended_truth": review_metadata[key]["counterfactual_truth"],
                            "shard_index": shard_index,
                        }
                    )
                for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
                    amount = int((response.get("usage") or {}).get(name, 0) or 0)
                    usage[name] += amount
                    aggregate_usage[name] += amount
            findings.append(
                {
                    "case_id": case_id,
                    "arm": arm,
                    "physical_request_count": len(shards),
                    "counts": dict(Counter(value["truth"] for value in assessments)),
                    "usage": dict(usage),
                    "assessments": assessments,
                }
            )
            print(f"{case_id:28} {arm:16} {dict(Counter(v['truth'] for v in assessments))}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "step": "v2_call2_overliteral_policy_paired_diagnostic",
                "contract": {
                    "target_count": len(review_metadata),
                    "temperature": 0.0,
                    "same_targets_evidence_and_batching": True,
                    "production_prompt_mutated": False,
                },
                "model": args.model,
                "plan_sha256": _sha256(args.plan),
                "call2_artifact_sha256": _sha256(args.call2_artifact),
                "candidate_review_sha256": _sha256(args.candidate_review),
                "current_system_prompt_sha256": hashlib.sha256(
                    current_prompt.encode("utf-8")
                ).hexdigest(),
                "candidate_system_prompt_sha256": _sha256(args.candidate_system_prompt),
                "usage": dict(aggregate_usage),
                "findings": findings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
