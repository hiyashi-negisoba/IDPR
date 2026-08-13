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
from idpr.v2.runtime.doctrine_activation import raised_active_doctrines
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
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
        derivative_accessories = {
            accessory for accessory, _principal, _mode in bindings.derivative_links
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
                derivative_links=bindings.derivative_links,
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
        output.append({
            "sub_question_id": row["sub_question_id"],
            "execution_status": "SUCCEEDED",
            "case_truth_count": len(truths.predicate),
            "case_relation_truth_count": len(truths.relation),
            "co_principal_source_count": len(bindings.co_principal_sources),
            "derivative_link_count": len(bindings.derivative_links),
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
