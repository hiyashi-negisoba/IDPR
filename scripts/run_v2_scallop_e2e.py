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
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationRouteAssessment,
    ParticipationRouteOption,
    ParticipationRouteTarget,
    participation_bindings_from_assessments,
)
from idpr.v2.runtime.relation_grounding import (
    RelationAssessment,
    RelationAssessmentTarget,
    add_relation_assessments,
)
from idpr.v2.runtime.scallop_backend import run_liability_chain_parity_program


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


def _participation_assessment(value: dict[str, Any]) -> ParticipationRouteAssessment:
    return ParticipationRouteAssessment(
        ParticipationRouteTarget(
            _instance(value["participant_instance"]),
            tuple(
                ParticipationRouteOption(
                    str(option["option_id"]),
                    str(option["mode"]),
                    tuple(_instance(source) for source in option["source_instances"]),
                )
                for option in value["route_options"]
            ),
        ),
        str(value["option_id"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = [
        json.loads(line)
        for line in args.call2_artifact.read_text(encoding="utf-8").splitlines()
        if line
    ]
    registry = load_definitions(args.definitions)
    output = []
    for row in rows:
        assessments = tuple(_assessment(value) for value in row["case_truths"])
        targets = tuple(value.target for value in assessments)
        truths = case_truths_from_assessments(assessments, expected_targets=targets)
        relation_assessments = tuple(
            _relation_assessment(value) for value in row["case_relation_truths"]
        )
        truths = add_relation_assessments(truths, relation_assessments)
        instances = tuple(_instance(value) for value in row["assessment_instances"])
        top_level_instances = tuple(_instance(value) for value in row["top_level_instances"])
        participation_assessments = tuple(
            _participation_assessment(value)
            for value in row["participation_route_assessments"]
        )
        bindings = participation_bindings_from_assessments(participation_assessments)
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
        case_work_dir = args.work_dir / str(row["sub_question_id"])
        active_doctrines = raised_active_doctrines(
            registry,
            top_level_instances,
            tuple(str(value) for value in row["candidate_doctrine_refs"]),
            truths,
        )
        results = run_liability_chain_parity_program(
            registry,
            compiled,
            instances,
            truths,
            work_dir=case_work_dir,
            completion_targets=completion_targets,
            co_principal_sources=bindings.co_principal_sources,
            derivative_links=bindings.derivative_links,
            active_doctrines=active_doctrines,
        )
        output.append({
            "sub_question_id": row["sub_question_id"],
            "case_truth_count": len(truths.predicate),
            "case_relation_truth_count": len(truths.relation),
            "co_principal_source_count": len(bindings.co_principal_sources),
            "derivative_link_count": len(bindings.derivative_links),
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
