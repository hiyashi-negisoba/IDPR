#!/usr/bin/env python3
"""Replay residual UNKNOWNs with an actor-aware realization evidence carrier."""

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
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets,
    validate_call2_output,
)
from idpr.v2.runtime.grounding_evidence import (
    actor_aware_realization_context,
    source_binding_realization_context,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

CURRENT_PROMPT = ROOT / "prompts/v2_call2_grounding.md"
CANDIDATE_PROMPT = ROOT / "prompts/candidates/v2_call2_grounding_actor_aware_v1.md"
CANDIDATE_USER = ROOT / "prompts/candidates/v2_call2_grounding_actor_aware_user_v1.md"


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _target(value: dict[str, Any]) -> AssessmentTarget:
    key = value["instance_key"]
    return AssessmentTarget(
        OffenseInstanceKey(
            str(key["case_id"]),
            str(key["actor_id"]),
            str(key["offense_ref"]),
            str(key["occurrence_id"]),
        ),
        str(value["predicate_ref"]),
    )


def _context_key(value: dict[str, object] | None) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True) if value else "NO_CONTEXT"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
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
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-targets-per-request", type=int, default=24)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--prompt-approved", action="store_true")
    parser.add_argument(
        "--source-binding-only",
        action="store_true",
        help="paired control vs narrow planner-source carrier; excludes same-actor siblings",
    )
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    registry = load_definitions(args.definitions)
    plans = _rows(args.plan)
    frozen = _rows(args.call2_artifact)
    issues = _rows(args.issue_bindings)
    inventory = _rows(args.inventory)
    assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            key: str(value["question_prompt"]) for key, value in inventory.items()
        },
    )
    selected = tuple(args.case_id) if args.case_id else tuple(plans)
    missing = [
        case_id
        for case_id in selected
        if case_id not in frozen or case_id not in issues or case_id not in inventory
    ]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")

    client = VLLMClient(args.base_url, args.model)
    current_system = load_prompt("v2_call2_grounding")
    current_user = load_prompt("v2_call2_grounding_user")
    candidate_system = CANDIDATE_PROMPT.read_text(encoding="utf-8")
    candidate_user = CANDIDATE_USER.read_text(encoding="utf-8")
    aggregate_usage = Counter()
    findings: list[dict[str, Any]] = []

    for case_id in selected:
        plan = plans[case_id]
        issue = issues[case_id]
        occurrences = {
            str(value["occurrence_id"]): GoldOccurrence(
                str(value["occurrence_id"]),
                str(value["actor_id"]),
                str(value["source_text"]),
                int(value["source_span"]["start"]),
                int(value["source_span"]["end"]),
            )
            for value in plan["occurrences"]
        }
        semantic_targets = tuple(
            _target(value)
            for value in frozen[case_id].get("assessments", ())
            if value.get("truth") == "UNKNOWN"
        )
        request_targets = grounding_request_targets(registry, semantic_targets)
        context_builder = (
            source_binding_realization_context
            if args.source_binding_only
            else actor_aware_realization_context
        )
        context_by_target = {
            target: context_builder(
                registry=registry,
                target=target,
                plan_row=plan,
                issue_row=issue,
            )
            for target in request_targets
        }
        groups: dict[tuple[str, str], list[AssessmentTarget]] = {}
        for target in request_targets:
            groups.setdefault(
                (target.instance_key.occurrence_id, _context_key(context_by_target[target])),
                [],
            ).append(target)

        arms = (
            ("actor_prompt_occurrence", "actor_prompt_source_binding")
            if args.source_binding_only
            else ("current_occurrence", "actor_prompt_occurrence", "actor_prompt_context")
        )
        for arm in arms:
            system_prompt = current_system if arm == "current_occurrence" else candidate_system
            user_prompt = current_user if arm == "current_occurrence" else candidate_user
            assessments: list[dict[str, Any]] = []
            arm_usage = Counter()
            request_count = 0
            for group_targets in groups.values():
                for shard in shard_assessment_targets(
                    group_targets, max_targets=args.max_targets_per_request
                ):
                    occurrence = occurrences[shard[0].instance_key.occurrence_id]
                    context = (
                        context_by_target[shard[0]]
                        if arm in {"actor_prompt_context", "actor_prompt_source_binding"}
                        else None
                    )
                    refs = tuple(dict.fromkeys(value.predicate_ref for value in shard))
                    payload = call2_request_payload(
                        evidence_occurrence=occurrence,
                        question_assumptions=assumptions.get(case_id, ()),
                        predicates=predicate_definitions(registry, refs),
                        targets=shard,
                        realization_context=context,
                    )
                    assert_no_leaked_fields(payload)
                    raw, metadata = client.complete_json(
                        system_prompt=system_prompt,
                        payload=payload,
                        schema_name="v2_actor_aware_realization_call2",
                        schema=call2_schema(shard),
                        max_tokens=args.max_tokens,
                        temperature=0.0,
                        user_template=user_prompt,
                    )
                    validated = validate_call2_output(raw, targets=shard)
                    assessments.extend(
                        {
                            **value.as_dict(),
                            "carrier_policy": (
                                str(context_by_target[value.target]["carrier_policy"])
                                if context_by_target[value.target] is not None
                                else "exact_occurrence_only"
                            ),
                        }
                        for value in validated
                    )
                    request_count += 1
                    usage = metadata.get("usage") or {}
                    for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
                        amount = int(usage.get(name, 0) or 0)
                        arm_usage[name] += amount
                        aggregate_usage[name] += amount
            findings.append(
                {
                    "case_id": case_id,
                    "arm": arm,
                    "counts": dict(Counter(value["truth"] for value in assessments)),
                    "physical_request_count": request_count,
                    "usage": dict(arm_usage),
                    "assessments": assessments,
                }
            )
            print(f"{case_id:32} {arm:24} {dict(Counter(v['truth'] for v in assessments))}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "step": "v2_call2_actor_aware_realization_diagnostic",
                "plan_sha256": _sha(args.plan),
                "call2_artifact_sha256": _sha(args.call2_artifact),
                "issue_bindings_sha256": _sha(args.issue_bindings),
                "current_prompt_sha256": _sha(CURRENT_PROMPT),
                "candidate_prompt_sha256": _sha(CANDIDATE_PROMPT),
                "candidate_user_prompt_sha256": _sha(CANDIDATE_USER),
                "case_ids": list(selected),
                "source_binding_only": args.source_binding_only,
                "residual_unknown_target_count": sum(
                    1
                    for case_id in selected
                    for value in frozen[case_id].get("assessments", ())
                    if value.get("truth") == "UNKNOWN"
                ),
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
