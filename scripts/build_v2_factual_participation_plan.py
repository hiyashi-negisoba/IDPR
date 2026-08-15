#!/usr/bin/env python3
"""Augment the canonical binding plan with evidence-scoped participation probes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    parse_factual_interactions,
)
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    parse_issue_binding_result,
    question_actor_ids,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import _instance_predicate_refs
from idpr.v2.runtime.factual_participation import (
    FactualParticipationError,
    derived_co_principal_targets,
    materialize_factual_participation_candidates,
)
from idpr.v2.runtime.carrier_contract import (
    PARTICIPATION_CARRIER,
    resolve_carrier,
    validate_plan_carriers,
)
from idpr.v2.runtime.plan_lineage import (
    LINEAGE_KEY,
    lineage_for_manifest,
    provenance as plan_provenance,
)
from idpr.v2.runtime.policy_probe_targets import (
    DERIVATIVE_RELATION_KINDS,
    participation_candidate_probe_targets,
    participation_mode_requirement_targets,
    unreachable_mode_findings,
)
from idpr.v2.runtime.target_scheduling import merge_target_opener

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: every row must be an object")
    return rows


def _index(path: Path, label: str) -> dict[str, dict[str, Any]]:
    rows = _jsonl(path)
    output = {str(row.get("sub_question_id")): row for row in rows}
    if len(output) != len(rows):
        raise ValueError(f"{label}: duplicate sub_question_id")
    return output


def _case_ids(path: Path) -> tuple[str, ...]:
    values = tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    if not values or len(values) != len(set(values)):
        raise ValueError(f"{path}: case ids must be nonempty and unique")
    return values


def _is_relation_predicate(registry: Any, predicate_ref: str) -> bool:
    """참가 관계 자체를 묻는 target인가. 행위자에게 국한된 사실이 아니라 사람 사이의 관계다."""
    entry = registry.get(predicate_ref)
    return entry is not None and entry.kind == "relation"


# `_requires_focal_action_carrier`가 여기 있었다. 이 빌더가 carrier 규칙을 자기 코드로
# 한 벌 더 갖고 있던 흔적이고, 그 중복이 바로 `evidence_scope` 수정이 다른 producer로
# 전달되지 않은 이유다. 규칙은 `carrier_contract`가 단독으로 소유하며 이 빌더는
# `resolve_carrier`를 부른다 -- 복사본을 남겨 두면 다음 사람이 그것을 고친다.


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--interaction-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    args = parser.parse_args()

    case_ids = _case_ids(args.case_list)
    plans = _index(args.plan_artifact, "planner")
    bindings = _index(args.call15_artifact, "Call 1.5")
    interactions = _index(args.interaction_artifact, "Call 1.5-P")
    inventory = _index(args.inventory, "inventory")
    registry = load_definitions(args.definitions)
    for label, values in (
        ("planner", plans),
        ("Call 1.5", bindings),
        ("Call 1.5-P", interactions),
    ):
        missing = sorted(set(case_ids) - set(values))
        extra = sorted(set(values) - set(case_ids))
        if missing or extra:
            raise ValueError(
                f"{label}: case-list mismatch missing={missing}, extra={extra}"
            )
    missing_inventory = sorted(set(case_ids) - set(inventory))
    if missing_inventory:
        raise ValueError(f"inventory: missing selected cases {missing_inventory}")

    output: list[dict[str, Any]] = []
    for case_id in case_ids:
        source = inventory[case_id]
        binding_row = bindings[case_id]
        interaction_row = interactions[case_id]
        if interaction_row.get("error") not in {None, ""}:
            raise ValueError(f"{case_id}: unsuccessful Call 1.5-P row")
        seeds = binding_row.get("seeds")
        if not isinstance(seeds, list) or not seeds:
            raise ValueError(f"{case_id}: missing Call 1.5 seed lineage")
        responsibility = question_actor_ids(str(source["question_prompt"]))
        try:
            binding_result = parse_issue_binding_result(
                {
                    "factual_episodes": binding_row.get("factual_episodes"),
                    "seed_results": binding_row.get("seed_results"),
                },
                seeds=seeds,
                case_text=str(source["question_text"]),
                candidate_actor_ids=responsibility,
            )
            factual_interactions = parse_factual_interactions(
                interaction_row.get("interactions", []),
                case_text=str(source["question_text"]),
                episodes=binding_result.factual_episodes,
            )
            compiled = materialize_factual_participation_candidates(
                case_id=case_id,
                plan_row=plans[case_id],
                binding_result=binding_result,
                interactions=factual_interactions,
                responsibility_actor_ids=responsibility,
                registry=registry,
            )
            post_participation_derived = derived_co_principal_targets(
                registry,
                compiled.targets,
                # 파생 group의 정범 member는 그 파생죄의 실현을 가리켜야 한다. base 실현의
                # occurrence를 들고 offense_ref만 바꾸면 `special_theft`를 선언하면서
                # `theft` 실현을 가리키는 instance가 나온다.
                realization_occurrences={
                    (str(value["actor_id"]), str(value["offense_ref"])): str(
                        value["realization_id"]
                    )
                    for value in plans[case_id].get("legal_realizations", [])
                },
            )
        except (
            IssueBindingContractError,
            FactualInteractionContractError,
            FactualParticipationError,
        ) as exc:
            raise ValueError(f"{case_id}: {exc}") from exc

        row = copy.deepcopy(plans[case_id])
        row["occurrences"].extend(
            value.as_dict() for value in compiled.evidence_occurrences
        )
        participation_targets = (*compiled.targets, *post_participation_derived)
        row["participation_local_targets"] = [
            value.as_dict() for value in participation_targets
        ]
        row["participation_local_target_count"] = len(participation_targets)
        row["post_participation_derived_group_count"] = len(
            post_participation_derived
        )
        row["factual_interaction_count"] = len(factual_interactions)
        row["factual_interaction_candidate_count"] = len(
            {
                value.interaction_id
                for value in factual_interactions
                if value.interaction_id not in compiled.skipped_interaction_ids
            }
        )
        row["skipped_factual_interaction_ids"] = list(
            compiled.skipped_interaction_ids
        )
        row["participation_evidence_occurrence_count"] = len(
            compiled.evidence_occurrences
        )
        row.setdefault("instance_provenance", []).extend(
            {
                "instance_key": {
                    "case_id": instance.case_id,
                    "actor_id": instance.actor_id,
                    "offense_ref": instance.offense_ref,
                    "occurrence_id": instance.occurrence_id,
                },
                "factual_episode_id": episode_id,
                "source_binding_ids": [],
                "realization_id": instance.occurrence_id,
                "focal_action_id": None,
                "supporting_action_ids": [],
                "source_realization_ids": [],
                "carrier_ids": {},
            }
            for instance, episode_id in compiled.candidate_episodes
        )
        row["instance_provenance_count"] = len(row["instance_provenance"])
        occurrence_ids = {
            value["occurrence_id"] for value in row["occurrences"]
        }
        if len(occurrence_ids) != len(row["occurrences"]):
            raise ValueError(f"{case_id}: duplicate occurrence after augmentation")
        for target in row["participation_local_targets"]:
            if any(
                value["occurrence_id"] not in occurrence_ids
                for value in target["member_instances"]
            ):
                raise ValueError(f"{case_id}: dangling participation evidence")

        # 저작된 참가 정책이 요구하는 predicate를 Call 2 target으로 연다. planner는 어느
        # 법리인지 모른 채 probe가 선언한 offense/mode 범위만 읽는다.
        # A derived co-group discovered after Call 1.5-P must also enter the ordinary
        # liability universe.  It reuses the members' exact occurrences; no new evidence
        # span or actor attribution is synthesized here.
        existing_instances = {
            (
                value["case_id"], value["actor_id"], value["offense_ref"], value["occurrence_id"]
            )
            for value in row["assessment_instances"]
        }
        provenance_by_occurrence: dict[str, dict[str, Any]] = {}
        for value in row.get("instance_provenance", ()):
            if not isinstance(value, dict) or not isinstance(
                value.get("instance_key"), dict
            ):
                raise ValueError(f"{case_id}: malformed instance provenance")
            occurrence_id = value["instance_key"].get("occurrence_id")
            episode_id = value.get("factual_episode_id")
            if not isinstance(occurrence_id, str) or not isinstance(episode_id, str):
                raise ValueError(f"{case_id}: incomplete instance provenance")
            previous = provenance_by_occurrence.setdefault(occurrence_id, value)
            if previous.get("factual_episode_id") != episode_id:
                raise ValueError(
                    f"{case_id}: realization occurrence has conflicting episode lineage"
                )
        episode_by_occurrence = {
            occurrence_id: str(value["factual_episode_id"])
            for occurrence_id, value in provenance_by_occurrence.items()
        }
        episode_by_occurrence.update(
            {instance.occurrence_id: episode_id for instance, episode_id in compiled.candidate_episodes}
        )
        for instance, episode_id in compiled.candidate_episodes:
            provenance_by_occurrence.setdefault(
                instance.occurrence_id,
                {
                    "instance_key": {
                        "case_id": instance.case_id,
                        "actor_id": instance.actor_id,
                        "offense_ref": instance.offense_ref,
                        "occurrence_id": instance.occurrence_id,
                    },
                    "factual_episode_id": episode_id,
                    "source_binding_ids": [],
                    "realization_id": instance.occurrence_id,
                    "focal_action_id": None,
                    "supporting_action_ids": [],
                    "source_realization_ids": [],
                    "carrier_ids": {},
                },
            )
        for target in post_participation_derived:
            for member in target.members:
                key = (member.case_id, member.actor_id, member.offense_ref, member.occurrence_id)
                if key in existing_instances:
                    continue
                existing_instances.add(key)
                serialized = {
                    "case_id": member.case_id,
                    "actor_id": member.actor_id,
                    "offense_ref": member.offense_ref,
                    "occurrence_id": member.occurrence_id,
                }
                row["assessment_instances"].append(serialized)
                row["top_level_instances"].append(serialized)
                row["instances"].append(serialized)
                episode_id = episode_by_occurrence.get(member.occurrence_id)
                if episode_id is None:
                    raise ValueError(
                        f"{case_id}: derived participation member lacks episode provenance"
                    )
                source_provenance = provenance_by_occurrence.get(member.occurrence_id)
                if source_provenance is None:
                    raise ValueError(
                        f"{case_id}: derived participation member lacks realization provenance"
                    )
                source_binding_ids = source_provenance.get("source_binding_ids") or []
                supporting_action_ids = (
                    source_provenance.get("supporting_action_ids") or []
                )
                source_realization_ids = tuple(
                    dict.fromkeys(
                        (
                            member.occurrence_id,
                            *(
                                str(value)
                                for value in source_provenance.get(
                                    "source_realization_ids", ()
                                )
                            ),
                        )
                    )
                )
                source_carrier_ids = source_provenance.get("carrier_ids") or {}
                if not isinstance(source_carrier_ids, Mapping):
                    raise ValueError(
                        f"{case_id}: derived participation member has malformed carrier provenance"
                    )
                derived_provenance = {
                    "instance_key": serialized,
                    "factual_episode_id": episode_id,
                    "source_binding_ids": [str(value) for value in source_binding_ids],
                    "realization_id": member.occurrence_id,
                    "focal_action_id": source_provenance.get("focal_action_id"),
                    "supporting_action_ids": [
                        str(value) for value in supporting_action_ids
                    ],
                    "source_realization_ids": list(source_realization_ids),
                    "carrier_ids": dict(source_carrier_ids),
                }
                row.setdefault("instance_provenance", []).append(derived_provenance)
                provenance_by_occurrence.setdefault(
                    member.occurrence_id, derived_provenance
                )
                if member.offense_ref not in row["candidate_offense_refs"]:
                    row["candidate_offense_refs"].append(member.offense_ref)
        # 교사·방조 후보 가담자는 자기 고의를 스스로 답해야 하므로 assessment universe
        # 안에 있어야 한다. 그렇지 않으면 planner가 연 target이 존재하지 않는 instance를
        # 가리키고, Call 2도 symbolic도 그 target을 받을 자리가 없다.  다만 관계가 참으로
        # 확정되기 전에는 책임 결론이 아니므로 top_level에는 넣지 않는다 -- 승격은 관계가
        # 실제로 참이 된 뒤 symbolic 단계가 한다.
        for target in participation_targets:
            if target.kind not in DERIVATIVE_RELATION_KINDS:
                continue
            accessory = target.members[0]
            key = (
                accessory.case_id,
                accessory.actor_id,
                accessory.offense_ref,
                accessory.occurrence_id,
            )
            if key in existing_instances:
                continue
            existing_instances.add(key)
            serialized = {
                "case_id": accessory.case_id,
                "actor_id": accessory.actor_id,
                "offense_ref": accessory.offense_ref,
                "occurrence_id": accessory.occurrence_id,
            }
            row["assessment_instances"].append(serialized)
            if accessory.offense_ref not in row["candidate_offense_refs"]:
                row["candidate_offense_refs"].append(accessory.offense_ref)
        row["assessment_instance_count"] = len(row["assessment_instances"])
        row["top_level_instance_count"] = len(row["top_level_instances"])
        row["instances"] = list(row["assessment_instances"])
        row["instance_provenance_count"] = len(row.get("instance_provenance", ()))

        probe_targets = participation_candidate_probe_targets(registry, participation_targets)
        # 재사용할 때 opener를 버리지 않으려면 행 자체를 찾을 수 있어야 한다. key만 들고
        # 있으면 할 수 있는 것이 `continue`뿐이고, 그것이 doctrine 빌더에서 닫은 것과 같은
        # 구멍이다 -- 행에는 일반 요소 opener 하나만 남고 하류는 그렇게 읽는다.
        row_by_target = {
            (
                value["instance_key"]["case_id"],
                value["instance_key"]["actor_id"],
                value["instance_key"]["offense_ref"],
                value["instance_key"]["occurrence_id"],
                value["predicate_ref"],
            ): value
            for value in row["assessment_targets"]
        }
        existing = set(row_by_target)
        requirement_targets = participation_mode_requirement_targets(
            registry, participation_targets
        )
        added = 0
        requirement_added = 0
        for opened_by, values in (
            ("participation_candidate_probe", probe_targets),
            ("participation_mode_requirement", requirement_targets),
        ):
            for instance, predicate_ref in values:
                key = (
                    instance.case_id,
                    instance.actor_id,
                    instance.offense_ref,
                    instance.occurrence_id,
                    predicate_ref,
                )
                if key in existing:
                    # 이미 열려 있어도 이 producer가 그 사실을 필요로 한다는 것은 남는다.
                    merge_target_opener(row_by_target[key], opened_by)
                    continue
                existing.add(key)
                created = {
                    "instance_key": {
                        "case_id": instance.case_id,
                        "actor_id": instance.actor_id,
                        "offense_ref": instance.offense_ref,
                        "occurrence_id": instance.occurrence_id,
                    },
                    "predicate_ref": predicate_ref,
                    "opened_by": opened_by,
                }
                row_by_target[key] = created
                row["assessment_targets"].append(created)
                if predicate_ref not in row["selected_predicate_refs"]:
                    row["selected_predicate_refs"].append(predicate_ref)
                if opened_by == "participation_candidate_probe":
                    added += 1
                else:
                    requirement_added += 1
        for target in post_participation_derived:
            for instance in target.members:
                for predicate_ref in _instance_predicate_refs(registry, instance):
                    key = (
                        instance.case_id,
                        instance.actor_id,
                        instance.offense_ref,
                        instance.occurrence_id,
                        predicate_ref,
                    )
                    if key in existing:
                        # 이 opener는 합치지 않는다. 파생 group의 일반 구성요건 target이고,
                        # 그 필요를 표현하는 것이 offense/completion 표현식 그 자체다 --
                        # scheduler가 모르는 별도 요구를 싣지 않으므로 기록할 것이 없다.
                        continue
                    existing.add(key)
                    created = {
                        "instance_key": {
                            "case_id": instance.case_id,
                            "actor_id": instance.actor_id,
                            "offense_ref": instance.offense_ref,
                            "occurrence_id": instance.occurrence_id,
                        },
                        "predicate_ref": predicate_ref,
                        "opened_by": "post_participation_derived_group",
                    }
                    row_by_target[key] = created
                    row["assessment_targets"].append(created)
                    if predicate_ref not in row["selected_predicate_refs"]:
                        row["selected_predicate_refs"].append(predicate_ref)
        # Newly opened participation probes are logical targets too.  Give each
        # one an explicit physical carrier so Call 2 never falls back to its whole
        # factual episode.  Existing realization targets retain the planner's
        # action/realization assignment verbatim.
        # identity는 occurrence_id 하나가 아니다. 절도와 특수절도가 같은 realization을
        # 공유하고 그 둘의 carrier 사정이 다를 수 있다.
        provenance_by_instance = {
            (
                str(item["instance_key"]["actor_id"]),
                str(item["instance_key"]["offense_ref"]),
                str(item["instance_key"]["occurrence_id"]),
            ): item
            for item in row.get("instance_provenance", ())
        }
        carrier_by_target = {
            (
                value["instance_key"]["case_id"],
                value["instance_key"]["actor_id"],
                value["instance_key"]["offense_ref"],
                value["instance_key"]["occurrence_id"],
                value["predicate_ref"],
            )
            for value in row.get("assessment_carriers", ())
        }
        for target in row["assessment_targets"]:
            instance = target["instance_key"]
            key = (
                instance["case_id"],
                instance["actor_id"],
                instance["offense_ref"],
                instance["occurrence_id"],
                target["predicate_ref"],
            )
            if key in carrier_by_target:
                continue
            provenance = provenance_by_instance.get(
                (
                    str(instance["actor_id"]),
                    str(instance["offense_ref"]),
                    str(instance["occurrence_id"]),
                )
            )
            if provenance is None:
                raise ValueError(
                    f"{case_id}: participation target lacks realization provenance"
                )
            carrier_id, carrier_kind = resolve_carrier(
                registry,
                str(target["predicate_ref"]),
                provenance=provenance,
                occurrence_id=str(instance["occurrence_id"]),
            )
            if carrier_id not in occurrence_ids:
                raise ValueError(
                    f"{case_id}: participation target has no physical carrier {carrier_id}"
                )
            row.setdefault("assessment_carriers", []).append(
                {
                    "instance_key": dict(instance),
                    "predicate_ref": target["predicate_ref"],
                    "carrier_id": carrier_id,
                    "carrier_kind": carrier_kind,
                }
            )
            carrier_by_target.add(key)
        validate_plan_carriers(registry, row)
        row["assessment_carrier_count"] = len(row.get("assessment_carriers", ()))
        row["participation_probe_target_count"] = added
        row["participation_mode_requirement_target_count"] = requirement_added
        row["final_assessment_target_count"] = len(row["assessment_targets"])
        unreachable = unreachable_mode_findings(registry, participation_targets)
        row["participation_probe_unreachable_modes"] = [
            {"policy_id": policy_id, "mode": mode, "relation_kind": relation_kind}
            for policy_id, mode, relation_kind in unreachable
        ]
        output.append(row)
        print(
            f"{case_id}: interactions={len(factual_interactions)} "
            f"targets={len(compiled.targets)} "
            f"new_evidence={len(compiled.evidence_occurrences)}",
            flush=True,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_factual_participation_plan",
        LINEAGE_KEY: list(
            lineage_for_manifest(args.plan_artifact, "v2_factual_participation_plan")
        ),
        "status": "SUCCEEDED",
        "case_count": len(output),
        "factual_interaction_count": sum(
            row["factual_interaction_count"] for row in output
        ),
        "factual_interaction_candidate_count": sum(
            row["factual_interaction_candidate_count"] for row in output
        ),
        "participation_local_target_count": sum(
            row["participation_local_target_count"] for row in output
        ),
        "participation_evidence_occurrence_count": sum(
            row["participation_evidence_occurrence_count"] for row in output
        ),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "call15_artifact": str(args.call15_artifact),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        # 이 단계가 실제로 읽은 파일 **전부**의 내용 해시. 하나라도 빠지면 그 입력은 아래
        # 개별 sha 필드에 기록만 되고 freshness 검증에서는 빠진다 -- 기록과 검증이 서로 다른
        # 목록을 보면, 상호작용 artifact가 나중에 다시 생성되어도 아무도 걸러 내지 못한다.
        **plan_provenance(
            {
                "plan": args.plan_artifact,
                "call15": args.call15_artifact,
                "interaction": args.interaction_artifact,
                "inventory": args.inventory,
                "case_list": args.case_list,
            },
            definitions_dir=args.definitions,
        ),
        "interaction_artifact": str(args.interaction_artifact),
        "interaction_artifact_sha256": _sha256(args.interaction_artifact),
        "inventory_sha256": _sha256(args.inventory),
        "case_list_sha256": _sha256(args.case_list),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
