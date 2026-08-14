#!/usr/bin/env python3
"""Evaluate reviewed Call 2 targets with quote-validated deliberative grounding."""

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
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.question_assumptions import QuestionAssumption, load_question_assumptions
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    predicate_definitions,
)
from idpr.v2.runtime.grounding_evidence import actor_aware_realization_context
from idpr.v2.runtime.identity import OffenseInstanceKey

SYSTEM = ROOT / "prompts/candidates/v2_call2_grounding_deliberative_v1.md"
USER = ROOT / "prompts/candidates/v2_call2_grounding_deliberative_user_v1.md"
TRUTHS = {"TRUE", "FALSE", "UNKNOWN"}
BASES = {
    "EXPLICIT_FACT",
    "NECESSARY_APPLICATION",
    "INSUFFICIENT_FACT",
    "LEGAL_DISPUTE",
}


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


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


def _schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["truth", "basis", "evidence_quotes", "application"],
        "properties": {
            "truth": {"type": "string", "enum": sorted(TRUTHS)},
            "basis": {"type": "string", "enum": sorted(BASES)},
            "evidence_quotes": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "uniqueItems": True,
            },
            "application": {"type": "string", "minLength": 1, "maxLength": 500},
        },
    }


def _allowed_evidence(
    occurrence: GoldOccurrence,
    context: dict[str, object] | None,
    assumptions: tuple[QuestionAssumption, ...],
) -> tuple[str, ...]:
    values = [occurrence.source_text]
    if context:
        values.extend(str(v) for v in context.get("same_actor_action_evidence", ()))
        values.extend(str(v) for v in context.get("context_evidence", ()))
    values.extend(v.source_text for v in assumptions)
    return tuple(values)


def _validate(raw: dict[str, Any], allowed: tuple[str, ...]) -> dict[str, Any]:
    truth = str(raw.get("truth"))
    basis = str(raw.get("basis"))
    quotes = raw.get("evidence_quotes")
    application = raw.get("application")
    if truth not in TRUTHS or basis not in BASES:
        raise ValueError("invalid truth or basis")
    if not isinstance(quotes, list) or not all(isinstance(v, str) and v for v in quotes):
        raise ValueError("invalid evidence_quotes")
    if not isinstance(application, str) or not application.strip():
        raise ValueError("invalid application")
    if any(not any(quote in source for source in allowed) for quote in quotes):
        raise ValueError("evidence quote is not an exact substring of an allowed carrier")
    if truth in {"TRUE", "FALSE"} and not quotes:
        raise ValueError("known truth requires exact evidence")
    if truth == "UNKNOWN" and basis not in {"INSUFFICIENT_FACT", "LEGAL_DISPUTE"}:
        raise ValueError("UNKNOWN requires an uncertainty basis")
    if truth != "UNKNOWN" and basis not in {"EXPLICIT_FACT", "NECESSARY_APPLICATION"}:
        raise ValueError("known truth requires a known basis")
    return {
        "truth": truth,
        "basis": basis,
        "evidence_quotes": quotes,
        "application": application.strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument(
        "--inventory", type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--definitions", type=Path, default=ROOT / "data/v2/definitions"
    )
    parser.add_argument(
        "--question-assumptions", type=Path,
        default=ROOT / "data/v2/question_assumptions.jsonl",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--validation-attempts", type=int, default=3)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required")

    registry = load_definitions(args.definitions)
    plans = _rows(args.plan)
    issues = _rows(args.issue_bindings)
    inventory = _rows(args.inventory)
    review = json.loads(args.review.read_text(encoding="utf-8"))["records"]
    assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            key: str(value["question_prompt"]) for key, value in inventory.items()
        },
    )
    client = VLLMClient(args.base_url, args.model)
    system = SYSTEM.read_text(encoding="utf-8")
    user = USER.read_text(encoding="utf-8")
    usage_total = Counter()
    output = []
    for index, reviewed in enumerate(review, 1):
        target = _target(reviewed)
        case_id = target.instance_key.case_id
        plan = plans[case_id]
        occurrence_value = next(
            value for value in plan["occurrences"]
            if str(value["occurrence_id"]) == target.instance_key.occurrence_id
        )
        occurrence = GoldOccurrence(
            str(occurrence_value["occurrence_id"]),
            str(occurrence_value["actor_id"]),
            str(occurrence_value["source_text"]),
            int(occurrence_value["source_span"]["start"]),
            int(occurrence_value["source_span"]["end"]),
        )
        context = actor_aware_realization_context(
            registry=registry,
            target=target,
            plan_row=plan,
            issue_row=issues[case_id],
        )
        case_assumptions = assumptions.get(case_id, ())
        payload = call2_request_payload(
            evidence_occurrence=occurrence,
            question_assumptions=case_assumptions,
            predicates=predicate_definitions(registry, (target.predicate_ref,)),
            targets=(target,),
            realization_context=context,
        )
        assert_no_leaked_fields(payload)
        validation_errors = []
        for attempt in range(1, args.validation_attempts + 1):
            raw, metadata = client.complete_json(
                system_prompt=system,
                payload=payload,
                schema_name="v2_call2_deliberative_diagnostic",
                schema=_schema(),
                max_tokens=args.max_tokens,
                temperature=0.0,
                user_template=user,
            )
            usage = metadata.get("usage") or {}
            for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
                usage_total[name] += int(usage.get(name, 0) or 0)
            try:
                validated = _validate(
                    raw, _allowed_evidence(occurrence, context, case_assumptions)
                )
                break
            except ValueError as exc:
                validation_errors.append(str(exc))
        else:
            raise ValueError(
                f"{reviewed['review_id']}: validation failed after "
                f"{args.validation_attempts} attempts: {validation_errors}"
            )
        output.append({
            "review_id": reviewed["review_id"],
            "diagnostic_group": reviewed["diagnostic_group"],
            "intended_truth": reviewed["counterfactual_truth"],
            "instance_key": target.as_dict()["instance_key"],
            "predicate_ref": target.predicate_ref,
            "carrier_policy": context["carrier_policy"] if context else "exact_occurrence_only",
            **validated,
            "agrees_with_review": validated["truth"] == reviewed["counterfactual_truth"],
            "usage": usage,
            "validation_attempts": attempt,
            "validation_errors": validation_errors,
        })
        print(
            f"[{index}/{len(review)}] {reviewed['review_id']} "
            f"{validated['truth']} {validated['basis']}", flush=True
        )
        checkpoint = {
            "step": "v2_call2_deliberative_diagnostic_partial",
            "target_count": len(output),
            "usage": dict(usage_total),
            "records": output,
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    result = {
        "step": "v2_call2_deliberative_diagnostic",
        "review_sha256": hashlib.sha256(args.review.read_bytes()).hexdigest(),
        "system_prompt_sha256": hashlib.sha256(SYSTEM.read_bytes()).hexdigest(),
        "target_count": len(output),
        "truth_counts": dict(Counter(value["truth"] for value in output)),
        "basis_counts": dict(Counter(value["basis"] for value in output)),
        "intended_agreement": sum(value["agrees_with_review"] for value in output),
        "opposite_known": sum(
            value["truth"] in {"TRUE", "FALSE"} and not value["agrees_with_review"]
            for value in output
        ),
        "usage": dict(usage_total),
        "records": output,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: result[k] for k in (
        "truth_counts", "basis_counts", "intended_agreement", "opposite_known", "usage"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
