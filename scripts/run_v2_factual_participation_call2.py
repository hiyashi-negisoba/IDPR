#!/usr/bin/env python3
"""Run only evidence-scoped legal participation Call 2 probes."""

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

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationLocalTarget,
    compile_participation_bindings,
    participation_request_payload,
    participation_schema,
    validate_participation_output,
)

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
PROMPTS = ("v2_call2_participation", "v2_call2_participation_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


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
        tuple(_instance(item) for item in value["member_instances"]),
    )


def _occurrence(value: Mapping[str, Any]) -> GoldOccurrence:
    return GoldOccurrence(
        str(value["occurrence_id"]),
        str(value["actor_id"]),
        str(value["source_text"]),
        int(value["source_span"]["start"]),
        int(value["source_span"]["end"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a participation Call 2 run")

    plan_rows = _rows(args.plan_artifact)
    plans = {row["sub_question_id"]: row for row in plan_rows}
    selected = tuple(args.case_id) if args.case_id else tuple(plans)
    missing = sorted(set(selected) - set(plans))
    if missing:
        raise ValueError(f"missing selected cases: {missing}")
    registry = load_definitions(args.definitions)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    physical_requests = 0
    rejected_cases = 0
    output: list[dict[str, Any]] = []

    for case_index, case_id in enumerate(selected, 1):
        plan = plans[case_id]
        targets = tuple(_target(value) for value in plan["participation_local_targets"])
        occurrences = {
            value.occurrence_id: value
            for value in (_occurrence(raw) for raw in plan["occurrences"])
        }
        assessments = []
        requests = []
        for target_index, target in enumerate(targets, 1):
            evidence_ids = tuple(
                dict.fromkeys(value.occurrence_id for value in target.members)
            )
            evidence = tuple(occurrences[value] for value in evidence_ids)
            payload = participation_request_payload(
                registry=registry,
                occurrences=evidence,
                targets=(target,),
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=system_prompt,
                user_template=user_prompt,
                payload=payload,
                schema_name="v2_factual_participation_call2",
                schema=participation_schema((target,)),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            assessment = validate_participation_output(raw, targets=(target,))
            assessments.append(assessment)
            usage = metadata.get("usage", {})
            for key in usage_total:
                usage_total[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            requests.append(
                {
                    "target_index": target_index,
                    "relation_kind": target.kind,
                    "evidence_occurrence_ids": list(evidence_ids),
                    "usage": usage,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                }
            )
        compile_status = "SUCCEEDED"
        compile_errors: list[str] = []
        try:
            compiled = compile_participation_bindings(
                assessments, expected_targets=targets, registry=registry
            )
            co_count = len(compiled.co_principal_sources)
            derivative_count = len(compiled.derivative_links)
        except ParticipationGroundingError as exc:
            rejected_cases += 1
            compile_status = "REJECTED"
            compile_errors = list(exc.errors)
            co_count = 0
            derivative_count = 0
            mode_resolutions: list[dict[str, Any]] = []
        else:
            mode_resolutions = list(compiled.mode_resolutions)
        output.append(
            {
                "sub_question_id": case_id,
                "participation_local_target_count": len(targets),
                "participation_local_assessments": [
                    value.as_dict() for value in assessments
                ],
                "planned_participation_local_targets": [
                    value.as_dict() for value in targets
                ],
                "participation_compile_status": compile_status,
                "participation_compile_errors": compile_errors,
                "co_principal_source_count": co_count,
                "derivative_link_count": derivative_count,
                "participation_mode_resolutions": mode_resolutions,
                "requests": requests,
            }
        )
        truths = {
            truth: sum(value.truth == truth for value in assessments)
            for truth in ("TRUE", "FALSE", "UNKNOWN")
        }
        print(
            f"[{case_index}/{len(selected)}] {case_id}: "
            f"targets={len(targets)} truths={truths} compile={compile_status}",
            flush=True,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_factual_participation_call2",
        "status": "SUCCEEDED" if rejected_cases == 0 else "DEGRADED_DIAGNOSTIC",
        "case_count": len(output),
        "participation_local_target_count": sum(
            row["participation_local_target_count"] for row in output
        ),
        "truth_counts": {
            truth: sum(
                value["truth"] == truth
                for row in output
                for value in row["participation_local_assessments"]
            )
            for truth in ("TRUE", "FALSE", "UNKNOWN")
        },
        "physical_request_count": physical_requests,
        "rejected_case_count": rejected_cases,
        "usage": usage_total,
        "model": args.model,
        "sampling": {"temperature": args.temperature, "max_tokens": args.max_tokens},
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "prompts": {value: _sha256(prompt_path(value)) for value in PROMPTS},
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
