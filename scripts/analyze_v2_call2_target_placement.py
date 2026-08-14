#!/usr/bin/env python3
"""Build a provenance-first placement audit for residual Call 2 UNKNOWN targets.

This audit does not move targets or alter truth.  It separates carrier candidates that
are recoverable from existing planner provenance from direct bindings whose
principal/participant role must still be reviewed.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import _instance_predicate_refs
from idpr.v2.runtime.identity import OffenseInstanceKey


def _jsonl(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _bindings(issue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(binding["binding_id"]): binding
        for seed in issue.get("seed_results", ())
        for binding in seed.get("bindings", ())
    }


def placement_bucket(
    *,
    predicate_kind: str,
    actor_bound_ground_fact: bool,
    derived: bool,
    exact_actor_sources: int,
    other_actor_sources: int,
    exact_source_has_peer_actor: bool,
    same_actor_other_episode: int,
    same_episode_peer_actors: int,
) -> str:
    """Return a conservative structural queue, never a legal conclusion."""
    if predicate_kind == "legal_element":
        return "LEGAL_ELEMENT_REALIZATION_SCOPE"
    if predicate_kind != "ground_fact":
        return "UNSUPPORTED_PREDICATE_KIND"
    if not actor_bound_ground_fact:
        return "GROUND_FACT_REALIZATION_SCOPE"
    if derived and exact_actor_sources == 1 and exact_source_has_peer_actor:
        return "DERIVED_SOURCE_PARTICIPATION_REVIEW"
    if derived and exact_actor_sources == 1:
        return "DERIVED_EXACT_ACTOR_SOURCE"
    if derived and exact_actor_sources > 1:
        return "DERIVED_AMBIGUOUS_ACTOR_SOURCES"
    if derived and other_actor_sources:
        return "DERIVED_OTHER_ACTOR_SOURCE_REVIEW"
    if same_actor_other_episode:
        return "CROSS_EPISODE_SAME_ACTOR_CARRIER"
    if same_episode_peer_actors:
        return "PARTICIPATION_ROLE_REVIEW"
    return "DIRECT_BINDING_CONTENT_REVIEW"


def _fragments(binding: dict[str, Any]) -> dict[str, list[str]]:
    return {
        name: [
            str(value["source_quote"])
            for value in binding.get(name, ())
            if value.get("source_quote")
        ]
        for name in ("actor_action_fragments", "context_fragments")
    }


def build_audit(
    *,
    definitions: Path,
    plan_path: Path,
    bindings_path: Path,
    review_path: Path,
    selected_buckets: set[str] | None = None,
) -> dict[str, Any]:
    registry = load_definitions(definitions)
    plans = _jsonl(plan_path)
    issues = _jsonl(bindings_path)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    selected_buckets = selected_buckets or {
        "A_OR_CASE_CONTEXT_REVIEW",
        "C_OR_D_PERSISTENT_REVIEW",
    }

    predicate_cache: dict[str, frozenset[str]] = {}

    def offense_predicates(offense_ref: str) -> frozenset[str]:
        if offense_ref not in predicate_cache:
            predicate_cache[offense_ref] = frozenset(
                _instance_predicate_refs(
                    registry, OffenseInstanceKey("audit", "actor", offense_ref, "occ")
                )
            )
        return predicate_cache[offense_ref]

    records: list[dict[str, Any]] = []
    for residual in review["records"]:
        if residual["operational_bucket"] not in selected_buckets:
            continue
        instance = residual["instance_key"]
        case_id = str(instance["case_id"])
        occurrence_id = str(instance["occurrence_id"])
        actor_id = str(instance["actor_id"])
        predicate_ref = str(residual["predicate_ref"])
        plan = plans[case_id]
        direct = _bindings(issues[case_id])
        derived = {
            str(value["binding_id"]): value
            for value in plan.get("derived_binding_candidates", ())
        }
        provenance = derived.get(occurrence_id)
        current_source_ids = (
            [str(value) for value in provenance.get("source_binding_ids", ())]
            if provenance is not None
            else [occurrence_id]
        )
        current_episode = (
            str(provenance["factual_episode_id"])
            if provenance is not None
            else str(direct[occurrence_id]["factual_episode_id"])
        )

        carrying = [
            binding
            for binding in direct.values()
            if predicate_ref in offense_predicates(str(binding["offense_ref"]))
        ]
        source_candidates = [
            binding for binding in carrying if str(binding["binding_id"]) in current_source_ids
        ]
        exact_actor_sources = [
            binding for binding in source_candidates if str(binding["actor_id"]) == actor_id
        ]
        other_actor_sources = [
            binding for binding in source_candidates if str(binding["actor_id"]) != actor_id
        ]
        exact_source_ids = {str(value["binding_id"]) for value in exact_actor_sources}
        exact_source_has_peer_actor = any(
            str(binding["binding_id"]) not in exact_source_ids
            and str(binding["actor_id"]) != actor_id
            and str(binding["factual_episode_id"]) == str(source["factual_episode_id"])
            and str(binding["offense_ref"]) == str(source["offense_ref"])
            for source in exact_actor_sources
            for binding in direct.values()
        )
        same_actor_other_episode = [
            binding
            for binding in carrying
            if str(binding["actor_id"]) == actor_id
            and str(binding["factual_episode_id"]) != current_episode
        ]
        same_episode_peer_actors = [
            binding
            for binding in carrying
            if str(binding["actor_id"]) != actor_id
            and str(binding["factual_episode_id"]) == current_episode
            and str(binding["offense_ref"]) == str(instance["offense_ref"])
        ]
        episode_other_actor_bindings = [
            binding
            for binding in direct.values()
            if str(binding["actor_id"]) != actor_id
            and str(binding["factual_episode_id"]) == current_episode
        ]
        episode_other_actor_predicate_bindings = [
            binding
            for binding in carrying
            if str(binding["actor_id"]) != actor_id
            and str(binding["factual_episode_id"]) == current_episode
        ]
        predicate_kind = str(registry.kind_of(predicate_ref))
        predicate_entry = registry.get(predicate_ref)
        arguments = predicate_entry.payload.get("arguments", ()) if predicate_entry else ()
        actor_argument_names = {
            "actor",
            "witness",
            "offender",
            "disposer",
            "possessor",
            "official",
        }
        actor_bound_predicate = any(
            isinstance(value, dict)
            and str(value.get("name")) in actor_argument_names
            for value in arguments
        )
        actor_bound_ground_fact = (
            predicate_kind == "ground_fact" and actor_bound_predicate
        )
        bucket = placement_bucket(
            predicate_kind=predicate_kind,
            actor_bound_ground_fact=actor_bound_ground_fact,
            derived=provenance is not None,
            exact_actor_sources=len(exact_actor_sources),
            other_actor_sources=len(other_actor_sources),
            exact_source_has_peer_actor=exact_source_has_peer_actor,
            same_actor_other_episode=len(same_actor_other_episode),
            same_episode_peer_actors=len(same_episode_peer_actors),
        )

        def render(binding: dict[str, Any]) -> dict[str, Any]:
            return {
                "binding_id": str(binding["binding_id"]),
                "factual_episode_id": str(binding["factual_episode_id"]),
                "actor_id": str(binding["actor_id"]),
                "offense_ref": str(binding["offense_ref"]),
                **_fragments(binding),
            }

        records.append(
            {
                "review_id": residual["review_id"],
                "operational_bucket": residual["operational_bucket"],
                "placement_bucket": bucket,
                "instance_key": instance,
                "predicate_ref": predicate_ref,
                "predicate_kind": predicate_kind,
                "actor_bound_ground_fact": actor_bound_ground_fact,
                "actor_bound_predicate": actor_bound_predicate,
                "predicate_meaning": residual.get("predicate_meaning", ""),
                "truths": residual["truths"],
                "current_factual_episode_id": current_episode,
                "current_source_binding_ids": current_source_ids,
                "current_source_bindings": [
                    render(direct[value]) for value in current_source_ids if value in direct
                ],
                "exact_actor_source_candidates": [render(value) for value in exact_actor_sources],
                "other_actor_source_candidates": [render(value) for value in other_actor_sources],
                "same_actor_other_episode_candidates": [
                    render(value) for value in same_actor_other_episode
                ],
                "same_episode_peer_actor_candidates": [
                    render(value) for value in same_episode_peer_actors
                ],
                "episode_other_actor_bindings": [
                    render(value) for value in episode_other_actor_bindings
                ],
                "episode_other_actor_predicate_bindings": [
                    render(value) for value in episode_other_actor_predicate_bindings
                ],
                "episode_attribution_risk": bool(
                    actor_bound_predicate and episode_other_actor_predicate_bindings
                ),
                "review_decision": None,
            }
        )

    counts = Counter(value["placement_bucket"] for value in records)
    risk_counts = Counter(
        "RISK" if value["episode_attribution_risk"] else "NO_STRUCTURAL_RISK"
        for value in records
    )
    return {
        "step": "v2_call2_residual_unknown_target_placement_audit",
        "contract": {
            "input_operational_buckets": sorted(selected_buckets),
            "truth_mutation": "none",
            "target_mutation": "none",
            "structural_limit": (
                "Call 1.5 has no principal/participant role label; PARTICIPATION_ROLE_REVIEW "
                "and DIRECT_BINDING_CONTENT_REVIEW require review"
            ),
        },
        "target_count": len(records),
        "placement_bucket_counts": dict(counts.most_common()),
        "episode_attribution_risk_counts": dict(risk_counts.most_common()),
        "records": records,
    }


def _markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Residual UNKNOWN target-placement provenance audit",
        "",
        "이 packet은 target을 이동하거나 truth를 바꾸지 않는다. 기존 binding/derived provenance로",
        "carrier 후보가 구조적으로 보이는 경우와 principal/participant 검수가 필요한 경우를 나눈다.",
        "",
        "| placement bucket | count |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{name}` | {count} |"
        for name, count in audit["placement_bucket_counts"].items()
    )
    lines.extend(
        [
            "",
            "`DERIVED_*`와 `CROSS_EPISODE_*`도 자동 truth 복사 허가가 아니다. 전자는 어느",
            "source realization이 leaf를 공급해야 하는지, 후자는 현재 occurrence 밖에 같은 actor의",
            "후보 carrier가 있음을 뜻한다. Call 1.5에 법적 가담 역할이 없으므로 망보기·교사·방조와",
            "공동정범의 구별은 `PARTICIPATION_ROLE_REVIEW`에서 명시적으로 검수한다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--operational-bucket", action="append", default=[])
    args = parser.parse_args()
    audit = build_audit(
        definitions=args.definitions,
        plan_path=args.plan,
        bindings_path=args.issue_bindings,
        review_path=args.review,
        selected_buckets=set(args.operational_bucket) if args.operational_bucket else None,
    )
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.out_md.write_text(_markdown(audit), encoding="utf-8")
    print(json.dumps(audit["placement_bucket_counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
