#!/usr/bin/env python3
"""Project validated Call 2 rows to CaseTruths and execute the Scallop chain."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.registry import load_definitions
from idpr.v2.relations import RelationInstanceKey
from idpr.v2.runtime.concurrence import load_concurrence_rules
from idpr.v2.runtime.doctrine_activation import raised_active_doctrines
from idpr.v2.runtime.final_responsibility import (
    excess_parity_rows,
    excess_policy_for,
    plan_status_redirections,
    resolve_final_responsibility,
)
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    PredicateAssessment,
    case_truths_from_assessments,
)
from idpr.v2.runtime.identity import (
    FactualParticipantKey,
    OffenseInstanceKey,
    RuntimeRelationKey,
)
from idpr.v2.runtime.indirect_principal_grounding import IndirectPrincipalDependency
from idpr.v2.runtime.participation_grounding import (
    ParticipationLocalAssessment,
    ParticipationLocalTarget,
    compile_participation_bindings,
)
from idpr.v2.runtime.relation_grounding import (
    RelationAssessment,
    RelationAssessmentTarget,
    add_relation_assessments,
)
from idpr.v2.runtime.scallop_backend import (
    run_accessory_excess_program,
    run_article_263_liability_parity_program,
    run_indirect_principal_liability_parity_program,
    run_liability_chain_parity_program,
)
from idpr.v2.runtime.stages import UtilizedParticipantOutcome


def _json_value(value: Any) -> Any:
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _json_value(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return [
            {"key": _json_value(key), "value": _json_value(item)}
            for key, item in value.items()
        ]
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _assessment(value: dict[str, Any]) -> PredicateAssessment:
    raw = value["instance_key"]
    instance = OffenseInstanceKey(
        str(raw["case_id"]),
        str(raw["actor_id"]),
        str(raw["offense_ref"]),
        str(raw["occurrence_id"]),
    )
    return PredicateAssessment(
        AssessmentTarget(instance, str(value["predicate_ref"])),
        str(value["truth"]),
    )


def _instance(value: dict[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _article263_instances(row: dict[str, Any]) -> tuple[OffenseInstanceKey, ...]:
    output: list[OffenseInstanceKey] = []
    seen: set[OffenseInstanceKey] = set()
    for assessment in row.get("article263_assessments", []):
        pair = assessment.get("pair")
        if not isinstance(pair, dict):
            raise TypeError("malformed Article 263 assessment pair")
        for field in ("left_instance_key", "right_instance_key"):
            raw = pair.get(field)
            if not isinstance(raw, dict):
                raise TypeError(f"Article 263 pair missing {field}")
            instance = _instance(raw)
            if instance.offense_ref != "offense.injury":
                raise ValueError("Article 263 endpoint must be an injury instance")
            if instance in seen:
                raise ValueError("duplicate Article 263 endpoint instance")
            seen.add(instance)
            output.append(instance)
    return tuple(output)


def _relation_assessment(value: dict[str, Any]) -> RelationAssessment:
    raw_instance = value["instance_key"]
    instance = OffenseInstanceKey(
        str(raw_instance["case_id"]),
        str(raw_instance["actor_id"]),
        str(raw_instance["offense_ref"]),
        str(raw_instance["occurrence_id"]),
    )
    raw_relation = value["relation_key"]
    endpoints = value["endpoints"]
    definition = RelationInstanceKey(
        tuple(str(item) for item in raw_relation["occurrence_path"]),
        str(raw_relation["relation_ref"]),
        str(raw_relation["left_local_key"]),
        str(raw_relation["right_local_key"]),
    )
    return RelationAssessment(
        RelationAssessmentTarget(
            RuntimeRelationKey(instance, definition),
            str(endpoints["left_ref"]),
            str(endpoints["right_ref"]),
            str(endpoints["left_view"]),
            str(endpoints["right_view"]),
        ),
        str(value["truth"]),
    )


def _participation_target(value: dict[str, Any]) -> ParticipationLocalTarget:
    return ParticipationLocalTarget(
        str(value["relation_kind"]),
        tuple(_instance(member) for member in value["member_instances"]),
    )


def _participation_assessment(value: dict[str, Any]) -> ParticipationLocalAssessment:
    return ParticipationLocalAssessment(
        _participation_target(value),
        str(value["truth"]),
    )


def _indirect_dependency(value: dict[str, Any]) -> IndirectPrincipalDependency:
    truths = {"TRUE", "FALSE", "UNKNOWN"}
    statuses = {
        "elements_failure",
        "unlawfulness_defeat",
        "culpability_defeat",
        "punishability_defeat",
        "different_negligence_offense",
        "liable_exact_offense",
        "unresolved",
    }
    relation_truth = str(value["relation_truth"])
    dependency_truth = str(value["dependency_truth"])
    outcome_status = str(value["utilized_outcome_status"])
    if relation_truth not in truths or dependency_truth not in truths:
        raise ValueError("indirect-principal dependency contains an invalid truth value")
    if outcome_status not in statuses:
        raise ValueError("indirect-principal dependency contains an invalid outcome status")
    instance = _instance(value["utilizer_instance"])
    raw_participant = value["utilized_participant"]
    participant = FactualParticipantKey(
        str(raw_participant["case_id"]),
        str(raw_participant["participant_id"]),
    )
    outcome = UtilizedParticipantOutcome(
        participant,
        instance.offense_ref,
        outcome_status,
    )
    return IndirectPrincipalDependency(
        instance,
        participant,
        relation_truth,
        outcome,
        dependency_truth,
        str(value["reason"]),
    )


PARTICIPATION_PLAN_STEP = "v2_factual_participation_plan"


def require_participation_plan_lineage(
    plan_path: Path, *, allow_non_participation_plan: bool = False
) -> dict[str, Any]:
    """정본 E2E는 참가 병합을 거친 plan만 받는다. 다른 plan이면 hard-fail한다.

    2026-08-13에 실제로 났던 회귀다. `evaluation_instance_plan.jsonl`을 넘겼더니 참가 instance가
    통째로 빠졌고, `r11_p1_q1`의 excess finding 1건과 `r14_p1_q1`의 甲 방화 instance가 함께
    사라진 결과가 **아무 오류 없이** 나왔다. 조용히 다른 답을 내는 실행 인자는 사람의 주의로
    막을 것이 아니라 계약으로 막아야 한다.

    확인은 두 겹이다. 옆에 있는 manifest의 `step`이 1차이고, manifest가 없으면 참가 빌더만
    쓰는 행 필드로 2차 확인한다. 진단용으로 다른 plan을 넣어야 하면 명시적 플래그로만 열린다.
    """
    manifest_path = plan_path.with_suffix(".manifest.json")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        step = str(manifest.get("step", ""))
        if step == PARTICIPATION_PLAN_STEP:
            return {"plan_lineage": "MANIFEST_MATCHED", "plan_step": step}
        if not allow_non_participation_plan:
            raise ValueError(
                f"{plan_path}: canonical E2E requires a {PARTICIPATION_PLAN_STEP} artifact, "
                f"got step {step!r}; pass --allow-non-participation-plan for a diagnostic run"
            )
        return {"plan_lineage": "OVERRIDDEN", "plan_step": step}
    first = next(
        (line for line in plan_path.read_text(encoding="utf-8").splitlines() if line), None
    )
    if first is not None and "factual_interaction_count" in json.loads(first):
        return {"plan_lineage": "ROW_FIELD_MATCHED", "plan_step": PARTICIPATION_PLAN_STEP}
    if not allow_non_participation_plan:
        raise ValueError(
            f"{plan_path}: no manifest and no participation-plan row fields; this is not a "
            f"{PARTICIPATION_PLAN_STEP} artifact"
        )
    return {"plan_lineage": "OVERRIDDEN", "plan_step": None}


def _episode_order(plan_path: Path) -> dict[str, tuple[str, ...]]:
    """`{case: factual episode 순서}`. 초과가 "정범의 실행에서 이어지는 범위"를 계산할 때 쓴다."""
    output: dict[str, tuple[str, ...]] = {}
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        plan = json.loads(line)
        output[str(plan["sub_question_id"])] = tuple(
            str(value) for value in plan.get("factual_episode_order", ())
        )
    return output


def _instance_provenance(
    plan_path: Path,
) -> dict[str, dict[OffenseInstanceKey, tuple[str, tuple[str, ...]]]]:
    """`{case: {instance: (factual episode, source bindings)}}` straight from the planner.

    The final-responsibility stage needs the factual episode of each instance, and the planner is
    the only honest source: recomputing it here would mean a second reading of the case text in a
    stage that must not read it at all.
    """
    output: dict[str, dict[OffenseInstanceKey, tuple[str, tuple[str, ...]]]] = {}
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        plan = json.loads(line)
        case = str(plan["sub_question_id"])
        entries = plan.get("instance_provenance")
        if entries is None:
            raise ValueError(
                f"{case}: planner artifact predates instance_provenance; re-run the planner"
            )
        output[case] = {
            _instance(value["instance_key"]): (
                str(value["factual_episode_id"]),
                tuple(str(item) for item in value["source_binding_ids"]),
            )
            for value in entries
        }
    return output


def _concurrence_condition_truths(
    path: Path,
) -> dict[str, dict[tuple[str, OffenseInstanceKey, OffenseInstanceKey], str]]:
    """`{case: {(rule, absorbed, absorbing): truth}}` from the pair assessment artifact.

    실패한 pair는 싣지 않는다. 계약을 통과하지 못한 응답은 UNKNOWN으로 취급되어 두 죄가 모두
    유지되고 unresolved로 남는다 -- 근거 없는 흡수는 흡수하지 않는 것보다 나쁘다.
    """
    output: dict[str, dict[tuple[str, OffenseInstanceKey, OffenseInstanceKey], str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        case = str(row["sub_question_id"])
        truths: dict[tuple[str, OffenseInstanceKey, OffenseInstanceKey], str] = {}
        for value in row.get("concurrence_condition_assessments") or ():
            if value.get("error") or "truth" not in value:
                continue
            key = (
                str(value["rule_id"]),
                _instance(value["absorbed_instance_key"]),
                _instance(value["absorbing_instance_key"]),
            )
            truths[key] = str(value["truth"])
        output[case] = truths
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--plan",
        type=Path,
        help=(
            "evaluation_instance_plan.jsonl; enables the final-responsibility stage "
            "(concurrence, accessory excess, Article 33 proviso, policy input gaps)"
        ),
    )
    parser.add_argument(
        "--concurrence-rules",
        type=Path,
        default=ROOT / "data/v2/concurrence_rules.yaml",
    )
    parser.add_argument(
        "--allow-non-participation-plan",
        action="store_true",
        help="diagnostic escape from the participation-plan lineage guard",
    )
    parser.add_argument(
        "--concurrence-condition-assessments",
        type=Path,
        help="pair carrier artifact from run_v2_absorption_condition_pairs.py",
    )
    parser.add_argument(
        "--diagnostic-skip-rejected-participation",
        action="store_true",
        help="preserve rejected Call 2 rows as skipped diagnostics instead of executing them",
    )
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in args.call2_artifact.read_text(encoding="utf-8").splitlines()
        if line
    ]
    registry = load_definitions(args.definitions)
    plan_lineage = (
        require_participation_plan_lineage(
            args.plan,
            allow_non_participation_plan=args.allow_non_participation_plan,
        )
        if args.plan
        else {}
    )
    if plan_lineage:
        print(f"plan lineage: {plan_lineage}")
    provenance_by_case = _instance_provenance(args.plan) if args.plan else {}
    episode_order_by_case = _episode_order(args.plan) if args.plan else {}
    concurrence_rules = (
        load_concurrence_rules(args.concurrence_rules)
        if args.plan and args.concurrence_rules.exists()
        else ()
    )
    condition_truths_by_case = (
        _concurrence_condition_truths(args.concurrence_condition_assessments)
        if args.concurrence_condition_assessments
        else {}
    )
    excess_policy = excess_policy_for(registry)
    foreseeability_ref = (
        excess_policy.payload["quantitative"]["result_aggravated"]["foreseeability_ref"]
        if excess_policy is not None
        else ""
    )
    output = []
    for row in rows:
        participation_status = row.get("participation_compile_status")
        if participation_status == "REJECTED":
            if not args.diagnostic_skip_rejected_participation:
                raise ValueError(
                    f"{row['sub_question_id']}: rejected participation cannot enter Scallop"
                )
            output.append(
                {
                    "sub_question_id": row["sub_question_id"],
                    "execution_status": "SKIPPED_REJECTED_PARTICIPATION",
                    "participation_compile_errors": list(
                        row.get("participation_compile_errors", [])
                    ),
                    "case_truth_count": len(row["case_truths"]),
                    "case_relation_truth_count": len(row["case_relation_truths"]),
                    "co_principal_source_count": 0,
                    "derivative_link_count": 0,
                    "article263_dedicated_instance_count": 0,
                    "indirect_principal_instance_count": 0,
                    "final_responsibility": None,
                    "accessory_excess_scallop_effects": {},
                    "active_doctrines": [],
                    "liability_results": [],
                }
            )
            continue
        if participation_status not in {"SUCCEEDED", "UNRESOLVED_CONFLICT"}:
            raise ValueError(
                f"{row['sub_question_id']}: missing successful participation compile status"
            )
        assessments = tuple(_assessment(value) for value in row["case_truths"])
        targets = tuple(value.target for value in assessments)
        truths = case_truths_from_assessments(assessments, expected_targets=targets)
        relation_assessments = tuple(
            _relation_assessment(value) for value in row["case_relation_truths"]
        )
        truths = add_relation_assessments(truths, relation_assessments)
        instances = tuple(_instance(value) for value in row["assessment_instances"])
        top_level_instances = tuple(_instance(value) for value in row["top_level_instances"])
        if not instances:
            if (
                top_level_instances
                or truths.predicate
                or truths.relation
                or row["participation_local_assessments"]
                or row.get("article263_assessments")
                or row.get("indirect_principal_dependencies")
            ):
                raise ValueError(
                    f"{row['sub_question_id']}: empty assessment universe has downstream facts"
                )
            output.append(
                {
                    "sub_question_id": row["sub_question_id"],
                    "execution_status": "SUCCEEDED",
                    "result_status": "NO_LIABILITY_TARGET",
                    "case_truth_count": 0,
                    "case_relation_truth_count": 0,
                    "co_principal_source_count": 0,
                    "derivative_link_count": 0,
                    "article263_dedicated_instance_count": 0,
                    "indirect_principal_instance_count": 0,
                    "final_responsibility": None,
                    "accessory_excess_scallop_effects": {},
                    "active_doctrines": [],
                    "liability_results": [],
                }
            )
            continue
        participation_assessments = tuple(
            _participation_assessment(value)
            for value in row["participation_local_assessments"]
        )
        serialized_participation_targets = row.get(
            "planned_participation_local_targets"
        )
        if serialized_participation_targets is None:
            planned_count = int(row.get("planned_participation_local_target_count", -1))
            if planned_count != len(participation_assessments):
                raise ValueError(
                    f"{row['sub_question_id']}: Call 2 lacks serialized planned "
                    "participation targets"
                )
            expected_participation_targets = tuple(
                value.target for value in participation_assessments
            )
        else:
            expected_participation_targets = tuple(
                _participation_target(value)
                for value in serialized_participation_targets
            )
        bindings = compile_participation_bindings(
            participation_assessments,
            expected_targets=expected_participation_targets,
        )
        # 형법 제33조 단서는 책임 평가 *이전에* 적용된다. 가담자가 어느 죄에서 평가되는지를
        # 바꾸는 것이므로, 평가가 끝난 뒤에 결론만 갈아끼우는 것은 다른 일이 된다.
        status_redirections, redirection_findings = plan_status_redirections(
            registry,
            bindings.derivative_links,
            truths,
            known_instances=instances,
        )
        redirect_map = {
            # 전환 전 instance. derivative mode는 가담자를 정범이 실현한 죄에 고정하므로
            # 원래 offense_ref가 곧 base_offense_ref다.
            OffenseInstanceKey(
                redirection.accessory_instance.case_id,
                redirection.accessory_instance.actor_id,
                redirection.base_offense_ref,
                redirection.accessory_instance.occurrence_id,
            ): redirection.accessory_instance
            for redirection in status_redirections
        }
        derivative_links = tuple(
            (redirect_map.get(accessory, accessory), principal, mode)
            for accessory, principal, mode in bindings.derivative_links
        )
        derivative_accessories = {
            accessory for accessory, _principal, _mode in derivative_links
        }
        completion_targets = tuple(
            value for value in top_level_instances if value not in derivative_accessories
        )
        compiled: list[CompiledOffense] = []
        for ref in dict.fromkeys(instance.offense_ref for instance in instances):
            value = compile_offense(registry, ref)
            if not isinstance(value, CompiledOffense):
                raise TypeError(f"cannot compile {ref!r}")
            compiled.append(value)
        compiled_by_ref = {value.id: value for value in compiled}
        case_work_dir = args.work_dir / str(row["sub_question_id"])
        active_doctrines = raised_active_doctrines(
            registry,
            top_level_instances,
            tuple(str(value) for value in row["candidate_doctrine_refs"]),
            truths,
        )
        try:
            results = dict(run_liability_chain_parity_program(
                registry,
                compiled,
                instances,
                truths,
                work_dir=case_work_dir,
                completion_targets=completion_targets,
                co_principal_sources=bindings.co_principal_sources,
                derivative_links=derivative_links,
                active_doctrines=active_doctrines,
            ))
        except Exception as exc:
            raise RuntimeError(
                f"{row['sub_question_id']}: integrated Scallop execution failed"
            ) from exc
        article263_instances = _article263_instances(row)
        for instance in article263_instances:
            if instance not in top_level_instances:
                raise ValueError("Article 263 endpoint is outside top-level instances")
            if instance in derivative_accessories:
                raise ValueError("Article 263 endpoint cannot be a derivative accessory")
            compiled_injury = compiled_by_ref.get(instance.offense_ref)
            if compiled_injury is None:
                raise ValueError("Article 263 injury offense was not compiled")
            instance_active_doctrines = tuple(
                value for value in active_doctrines if value[0] == instance
            )
            results[instance] = run_article_263_liability_parity_program(
                registry,
                compiled_injury,
                instance,
                truths,
                work_dir=case_work_dir
                / "article263"
                / f"{instance.actor_id}_{instance.occurrence_id.replace(':', '_')}",
                active_doctrines=instance_active_doctrines,
            )
        indirect_dependencies = tuple(
            _indirect_dependency(value)
            for value in row.get("indirect_principal_dependencies", [])
        )
        indirect_instances = tuple(
            value.utilizer_instance for value in indirect_dependencies
        )
        if len(indirect_instances) != len(set(indirect_instances)):
            raise ValueError(
                "multiple utilized participants for one indirect-principal instance need "
                "an authored dependency fold"
            )
        for dependency in indirect_dependencies:
            instance = dependency.utilizer_instance
            if instance not in top_level_instances:
                raise ValueError("indirect-principal instance is outside top-level instances")
            if instance in derivative_accessories:
                raise ValueError("indirect-principal instance cannot be a derivative accessory")
            instance_active_doctrines = tuple(
                doctrine_ref
                for active_instance, doctrine_ref in active_doctrines
                if active_instance == instance
            )
            results[instance] = run_indirect_principal_liability_parity_program(
                registry,
                dependency,
                truths,
                work_dir=case_work_dir
                / "indirect_principal"
                / f"{instance.actor_id}_{instance.occurrence_id.replace(':', '_')}",
                active_doctrines=instance_active_doctrines,
            )
        final_view = None
        excess_parity: dict[str, str] = {}
        provenance = provenance_by_case.get(str(row["sub_question_id"]))
        if provenance is not None:
            final_view = resolve_final_responsibility(
                registry,
                case_id=str(row["sub_question_id"]),
                results=results,
                episode_by_instance={
                    instance: episode for instance, (episode, _) in provenance.items()
                },
                source_bindings_by_instance={
                    instance: sources for instance, (_, sources) in provenance.items()
                },
                derivative_links=derivative_links,
                truths=truths,
                concurrence_rules=concurrence_rules,
                condition_truths=condition_truths_by_case.get(
                    str(row["sub_question_id"]), {}
                ),
                episode_order=episode_order_by_case.get(str(row["sub_question_id"]), ()),
                available_predicate_refs=tuple(
                    dict.fromkeys(ref for _instance_key, ref in truths.predicate)
                ),
                status_redirections=status_redirections,
                status_redirection_findings=redirection_findings,
            )
            parity_rows = excess_parity_rows(
                final_view, truths, foreseeability_ref=foreseeability_ref
            )
            if parity_rows:
                # host 분류와 Scallop 결과가 어긋나면 여기서 hard-fail한다. 초과는 전용
                # relation으로 내려가며 v2_derivative_link로 우회하지 않는다.
                excess_parity = {
                    f"{instance.actor_id}/{instance.occurrence_id}/{instigated}": effect
                    for (instance, instigated), effect in run_accessory_excess_program(
                        parity_rows, work_dir=case_work_dir / "accessory_excess"
                    ).items()
                }
        output.append({
            "sub_question_id": row["sub_question_id"],
            "execution_status": "SUCCEEDED",
            "case_truth_count": len(truths.predicate),
            "case_relation_truth_count": len(truths.relation),
            "co_principal_source_count": len(bindings.co_principal_sources),
            "derivative_link_count": len(derivative_links),
            "final_responsibility": None if final_view is None else final_view.as_dict(),
            # 조건 truth가 실제로 이 단계에 도착했는지를 artifact에 남긴다. 남기지 않으면
            # "효과 없음"과 "플래그가 무시됨"이 출력에서 구별되지 않는다.
            "concurrence_condition_truths": [
                {
                    "rule_id": rule_id,
                    "absorbed_instance_key": _json_value(absorbed),
                    "absorbing_instance_key": _json_value(absorbing),
                    "truth": truth,
                    "both_instances_established": bool(
                        final_view is not None
                        and absorbed in final_view.established_instances
                        and absorbing in final_view.established_instances
                    ),
                }
                for (rule_id, absorbed, absorbing), truth in condition_truths_by_case.get(
                    str(row["sub_question_id"]), {}
                ).items()
            ],
            "accessory_excess_scallop_effects": excess_parity,
            "article263_dedicated_instance_count": len(article263_instances),
            "indirect_principal_instance_count": len(indirect_dependencies),
            "active_doctrines": [
                {"instance_key": _json_value(instance), "doctrine_ref": doctrine_ref}
                for instance, doctrine_ref in active_doctrines
            ],
            "liability_results": [
                {"instance_key": _json_value(instance), "result": _json_value(result)}
                for instance, result in results.items()
            ],
        })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output),
        encoding="utf-8",
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
