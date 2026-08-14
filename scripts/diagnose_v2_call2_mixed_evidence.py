#!/usr/bin/env python3
"""Replay frozen residual UNKNOWN targets with a predicate-typed evidence carrier."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
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
from idpr.v2.registry import DefinitionRegistry, load_definitions
from idpr.v2.runtime.evaluation_instance_planner import _instance_predicate_refs
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
from scripts.diagnose_v2_call2_evidence_scope import (
    _target,
    assessment_key,
    factual_episode_evidence,
    rows,
    sha256,
)

_ACTOR_ARGUMENTS = frozenset(
    {"actor", "witness", "offender", "disposer", "possessor", "official"}
)


def actor_bound_ground_fact(registry: DefinitionRegistry, predicate_ref: str) -> bool:
    entry = registry.get(predicate_ref)
    if entry is None or entry.kind != "ground_fact":
        return False
    return any(
        isinstance(value, dict) and value.get("name") in _ACTOR_ARGUMENTS
        for value in entry.payload.get("arguments", ())
    )


def _direct_bindings(issue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(binding["binding_id"]): binding
        for seed in issue.get("seed_results", ())
        for binding in seed.get("bindings", ())
    }


def mixed_carrier(
    *,
    registry: DefinitionRegistry,
    target: AssessmentTarget,
    plan: dict[str, Any],
    issue: dict[str, Any],
    occurrences: dict[str, GoldOccurrence],
    episode_evidence: dict[str, str],
) -> tuple[str, GoldOccurrence]:
    """Select evidence without changing target identity or projecting another actor's truth."""
    occurrence_id = target.instance_key.occurrence_id
    original = occurrences[occurrence_id]
    if not actor_bound_ground_fact(registry, target.predicate_ref):
        text = episode_evidence.get(occurrence_id, original.source_text)
        return (
            "factual_episode" if occurrence_id in episode_evidence else "occurrence_fallback",
            GoldOccurrence(occurrence_id, original.actor_id, text, 0, len(text)),
        )

    derived = {
        str(value["binding_id"]): value
        for value in plan.get("derived_binding_candidates", ())
    }.get(occurrence_id)
    if derived is None:
        return "actor_action_binding", original

    bindings = _direct_bindings(issue)
    exact_sources = []
    for source_id in derived.get("source_binding_ids", ()):
        binding = bindings.get(str(source_id))
        if binding is None or str(binding["actor_id"]) != target.instance_key.actor_id:
            continue
        source_instance = OffenseInstanceKey(
            target.instance_key.case_id,
            target.instance_key.actor_id,
            str(binding["offense_ref"]),
            str(source_id),
        )
        if target.predicate_ref in _instance_predicate_refs(registry, source_instance):
            exact_sources.append(str(source_id))
    if len(exact_sources) != 1:
        return "derived_actor_source_ambiguous_fallback", original
    source = occurrences[exact_sources[0]]
    return (
        "derived_exact_actor_source",
        GoldOccurrence(occurrence_id, original.actor_id, source.source_text, 0, len(source.source_text)),
    )


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
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    registry = load_definitions(args.definitions)
    inventory = rows(args.inventory)
    plans = rows(args.plan)
    frozen = rows(args.call2_artifact)
    issues = rows(args.issue_bindings)
    assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            key: str(value["question_prompt"]) for key, value in inventory.items()
        },
    )
    selected = tuple(args.case_id) if args.case_id else tuple(plans)
    missing = [
        value
        for value in selected
        if value not in inventory
        or value not in plans
        or value not in frozen
        or value not in issues
    ]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")

    client = VLLMClient(base_url=args.base_url, model=args.model)
    system_prompt = load_prompt("v2_call2_grounding")
    user_prompt = load_prompt("v2_call2_grounding_user")
    findings: list[dict[str, Any]] = []
    aggregate_usage = Counter()
    aggregate_carriers = Counter()

    for case_id in selected:
        plan = plans[case_id]
        case_text = str(inventory[case_id]["question_text"])
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
        episodes = factual_episode_evidence(issues[case_id], plan, case_text)
        targets = tuple(
            _target(value)
            for value in frozen[case_id].get("assessments", ())
            if value.get("truth") == "UNKNOWN"
        )
        planner_keys = {
            assessment_key(value) for value in plan.get("assessment_targets", ())
        }
        if any(assessment_key(value.as_dict()) not in planner_keys for value in targets):
            raise ValueError(f"{case_id}: residual target is outside planner scope")
        request_targets = grounding_request_targets(registry, targets)

        for arm in ("occurrence_control", "mixed_evidence"):
            groups: dict[tuple[str, str, str], list[AssessmentTarget]] = {}
            evidence_by_group: dict[tuple[str, str, str], GoldOccurrence] = {}
            carrier_by_target: dict[AssessmentTarget, str] = {}
            for target in request_targets:
                mixed_name, mixed_evidence = mixed_carrier(
                    registry=registry,
                    target=target,
                    plan=plan,
                    issue=issues[case_id],
                    occurrences=occurrences,
                    episode_evidence=episodes,
                )
                if arm == "occurrence_control":
                    carrier = f"occurrence_control_for_{mixed_name}"
                    evidence = occurrences[target.instance_key.occurrence_id]
                else:
                    carrier, evidence = mixed_name, mixed_evidence
                    aggregate_carriers[carrier] += 1
                group_key = (
                    target.instance_key.occurrence_id,
                    carrier,
                    evidence.source_text,
                )
                groups.setdefault(group_key, []).append(target)
                evidence_by_group[group_key] = evidence
                carrier_by_target[target] = carrier

            assessments: list[dict[str, Any]] = []
            usage = Counter()
            request_count = 0
            for group_key, group_targets in groups.items():
                for shard in shard_assessment_targets(group_targets, max_targets=24):
                    evidence = evidence_by_group[group_key]
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
                    for value in values:
                        assessments.append(
                            {
                                **value.as_dict(),
                                "evidence_carrier": carrier_by_target[value.target],
                            }
                        )
                    request_count += 1
                    for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
                        amount = int((metadata.get("usage") or {}).get(name, 0) or 0)
                        usage[name] += amount
                        aggregate_usage[name] += amount
            findings.append(
                {
                    "case_id": case_id,
                    "arm": arm,
                    "counts": dict(Counter(value["truth"] for value in assessments)),
                    "carrier_counts": dict(
                        Counter(value["evidence_carrier"] for value in assessments)
                    ),
                    "physical_request_count": request_count,
                    "usage": dict(usage),
                    "assessments": assessments,
                }
            )
            print(
                f"{case_id:28} {arm:18} "
                f"{dict(Counter(v['truth'] for v in assessments))}"
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "step": "v2_call2_residual_unknown_mixed_evidence",
                "plan_sha256": sha256(args.plan),
                "call2_artifact_sha256": sha256(args.call2_artifact),
                "issue_bindings_sha256": sha256(args.issue_bindings),
                "case_ids": list(selected),
                "residual_unknown_target_count": sum(
                    1
                    for case_id in selected
                    for value in frozen[case_id].get("assessments", ())
                    if value.get("truth") == "UNKNOWN"
                ),
                "carrier_counts": dict(aggregate_carriers),
                "usage": dict(aggregate_usage),
                "findings": findings,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
