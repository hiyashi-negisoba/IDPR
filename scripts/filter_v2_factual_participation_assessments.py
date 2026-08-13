#!/usr/bin/env python3
"""Causally reuse participation assessments when a revised plan only removes targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationLocalAssessment,
    ParticipationLocalTarget,
    compile_participation_bindings,
)


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _key(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _target(value: Mapping[str, Any]) -> ParticipationLocalTarget:
    return ParticipationLocalTarget(
        str(value["relation_kind"]),
        tuple(_instance(member) for member in value["member_instances"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--source-assessments", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    plans = {row["sub_question_id"]: row for row in _rows(args.plan_artifact)}
    sources = {
        row["sub_question_id"]: row for row in _rows(args.source_assessments)
    }
    if tuple(plans) != tuple(sources):
        raise ValueError("plan and assessment case universes differ")

    output: list[dict[str, Any]] = []
    removed = 0
    rejected = 0
    for case_id, plan in plans.items():
        source = sources[case_id]
        source_targets = source["planned_participation_local_targets"]
        source_assessments = source["participation_local_assessments"]
        source_requests = source["requests"]
        if not (
            len(source_targets) == len(source_assessments) == len(source_requests)
        ):
            raise ValueError(f"{case_id}: malformed source assessment row")
        indexed = {
            _key(target): (assessment, request)
            for target, assessment, request in zip(
                source_targets, source_assessments, source_requests
            )
        }
        if len(indexed) != len(source_targets):
            raise ValueError(f"{case_id}: duplicate source target")
        targets = plan["participation_local_targets"]
        missing = [_key(target) for target in targets if _key(target) not in indexed]
        if missing:
            raise ValueError(f"{case_id}: revised plan introduced an unevaluated target")
        assessments = [indexed[_key(target)][0] for target in targets]
        requests = []
        for index, target in enumerate(targets, 1):
            request = dict(indexed[_key(target)][1])
            request["target_index"] = index
            request["causal_reuse"] = True
            requests.append(request)
        typed_targets = tuple(_target(target) for target in targets)
        typed_assessments = tuple(
            ParticipationLocalAssessment(target, assessment["truth"])
            for target, assessment in zip(
                typed_targets, assessments, strict=True
            )
        )
        compile_status = "SUCCEEDED"
        compile_errors: list[str] = []
        co_count = derivative_count = 0
        try:
            compiled = compile_participation_bindings(
                typed_assessments, expected_targets=typed_targets
            )
            co_count = len(compiled.co_principal_sources)
            derivative_count = len(compiled.derivative_links)
        except ParticipationGroundingError as exc:
            rejected += 1
            compile_status = "REJECTED"
            compile_errors = list(exc.errors)
        removed += len(source_targets) - len(targets)
        output.append(
            {
                **source,
                "participation_local_target_count": len(targets),
                "participation_local_assessments": assessments,
                "planned_participation_local_targets": targets,
                "requests": requests,
                "participation_compile_status": compile_status,
                "participation_compile_errors": compile_errors,
                "co_principal_source_count": co_count,
                "derivative_link_count": derivative_count,
                "causal_reuse_source": str(args.source_assessments),
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    truth_counts = {
        truth: sum(
            value["truth"] == truth
            for row in output
            for value in row["participation_local_assessments"]
        )
        for truth in ("TRUE", "FALSE", "UNKNOWN")
    }
    manifest = {
        "step": "v2_factual_participation_causal_filter",
        "status": "SUCCEEDED",
        "case_count": len(output),
        "participation_local_target_count": sum(
            row["participation_local_target_count"] for row in output
        ),
        "removed_target_count": removed,
        "truth_counts": truth_counts,
        "physical_request_count": 0,
        "rejected_case_count": rejected,
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "source_assessments": str(args.source_assessments),
        "source_assessments_sha256": _sha256(args.source_assessments),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
