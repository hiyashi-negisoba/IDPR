#!/usr/bin/env python3
"""Run paired no-card/card atomic Call 2 assessments."""

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

PROMPTS = ("v2_call2_card_ab", "v2_call2_card_ab_user")


def schema(material_ids: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["truth", "evidence_quotes", "applied_material_ids", "missing_information"],
        "properties": {
            "truth": {"type": "string", "enum": ["TRUE", "FALSE", "UNKNOWN"]},
            "evidence_quotes": {"type": "array", "maxItems": 4, "items": {"type": "string"}},
            "applied_material_ids": {
                "type": "array",
                "maxItems": len(material_ids),
                "items": {"type": "string", "enum": material_ids},
            },
            "missing_information": {"type": "array", "maxItems": 4, "items": {"type": "string"}},
        },
    }


def validate(value: Any, *, source: str, material_ids: set[str]) -> dict[str, Any]:
    required = {"truth", "evidence_quotes", "applied_material_ids", "missing_information"}
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("invalid response fields")
    truth = value["truth"]
    if truth not in {"TRUE", "FALSE", "UNKNOWN"}:
        raise ValueError("invalid truth")
    for field in ("evidence_quotes", "applied_material_ids", "missing_information"):
        if not isinstance(value[field], list) or any(not isinstance(x, str) or not x for x in value[field]):
            raise ValueError(f"invalid {field}")
    if len(value["evidence_quotes"]) != len(set(value["evidence_quotes"])):
        raise ValueError("duplicate evidence quote")
    if any(quote not in source for quote in value["evidence_quotes"]):
        raise ValueError("non-exact evidence quote")
    if not set(value["applied_material_ids"]) <= material_ids:
        raise ValueError("unknown material id")
    if truth in {"TRUE", "FALSE"} and not value["evidence_quotes"]:
        raise ValueError("decisive truth lacks evidence")
    if truth == "UNKNOWN" and not value["missing_information"]:
        raise ValueError("UNKNOWN lacks missing information")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument(
        "--plan", type=Path, default=ROOT / "experiments/v2_call15_directscope_26_causal/card_call2_ab_v1/plan.jsonl"
    )
    parser.add_argument(
        "--out", type=Path, default=ROOT / "experiments/v2_call15_directscope_26_causal/card_call2_ab_v1/output.jsonl"
    )
    parser.add_argument("--max-tokens", type=int, default=768)
    args = parser.parse_args()

    system = load_prompt(PROMPTS[0])
    user_template = load_prompt(PROMPTS[1])
    client = VLLMClient(args.base_url, args.model, api_key=args.api_key)
    outputs = []
    counts: Counter[str] = Counter()
    usage: Counter[str] = Counter()
    for case_row in (json.loads(line) for line in args.plan.read_text().splitlines() if line):
        case_results = []
        for target in case_row["ab_targets"]:
            base = {
                "assessment_target": target["assessment_target"],
                "evidence_occurrence": target["evidence_occurrence"],
                "question_assumptions": target["question_assumptions"],
                "predicate_definition": target["predicate_definition"],
                "reviewed_issue": {
                    "issue_id": target["reviewed_issue"]["issue_id"],
                    "question": target["reviewed_issue"]["question"],
                },
            }
            pair = {}
            for arm, materials in (
                ("A_no_card", []),
                ("B_with_card", target["reviewed_issue"]["legal_materials"]),
            ):
                request = {**base, "legal_materials": materials}
                assert_no_leaked_fields(request)
                material_ids = [value["material_id"] for value in materials]
                raw, metadata = client.complete_json(
                    system_prompt=system,
                    payload=request,
                    schema_name="v2_call2_card_ab",
                    schema=schema(material_ids),
                    max_tokens=args.max_tokens,
                    temperature=0.0,
                    user_template=user_template,
                )
                value = validate(
                    raw,
                    source=target["evidence_occurrence"]["source_text"],
                    material_ids=set(material_ids),
                )
                response_usage = metadata.get("usage", {})
                pair[arm] = {**value, "usage": response_usage}
                counts[f"{arm}:{value['truth']}"] += 1
                for key, amount in response_usage.items():
                    if isinstance(amount, (int, float)):
                        usage[key] += int(amount)
            case_results.append(
                {
                    "ab_target_id": target["ab_target_id"],
                    "assessment_target": target["assessment_target"],
                    "original_truth": target["original_truth"],
                    "reviewed_issue": target["reviewed_issue"],
                    "retrieval": target["retrieval"],
                    **pair,
                }
            )
        outputs.append(
            {"sub_question_id": case_row["sub_question_id"], "results": case_results}
        )
        print(f"{case_row['sub_question_id']}: {len(case_results)} paired targets", flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in outputs))
    manifest = {
        "status": "SUCCEEDED",
        "case_count": len(outputs),
        "paired_target_count": sum(len(row["results"]) for row in outputs),
        "physical_request_count": 2 * sum(len(row["results"]) for row in outputs),
        "truth_counts": dict(counts),
        "usage": dict(usage),
        "prompt_sha256": {
            "system": hashlib.sha256(system.encode()).hexdigest(),
            "user": hashlib.sha256(user_template.encode()).hexdigest(),
        },
        "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
