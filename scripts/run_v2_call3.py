#!/usr/bin/env python3
"""Run one final neural IRAC writer call per frozen KCL sub-question."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import load_gold_occurrences
from idpr.v2.registry import load_definitions

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
PROMPTS = ("v2_call3_irac", "v2_call3_irac_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _index(path: Path) -> dict[str, dict[str, Any]]:
    values = _jsonl(path)
    output = {str(value["sub_question_id"]): value for value in values}
    if len(output) != len(values):
        raise ValueError(f"{path}: duplicate sub_question_id")
    return output


def _offense_catalog(definitions: Path) -> dict[str, dict[str, Any]]:
    registry = load_definitions(definitions)
    output = {}
    for kind in ("offense", "derived_offense"):
        for entry in registry.by_kind.get(kind, ()):
            identity = entry.payload.get("identity") or {}
            output[entry.id] = {
                "display_name": identity.get("name", entry.id),
                "statutory_refs": identity.get("statutory_refs", []),
            }
    return output


def _conclusions(row: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    seen = set()
    for value in row["liability_results"]:
        key = value["instance_key"]
        identity = (
            key["case_id"], key["actor_id"], key["offense_ref"], key["occurrence_id"]
        )
        if identity in seen:
            raise ValueError(f"{row['sub_question_id']}: duplicate symbolic instance")
        seen.add(identity)
        result = value["result"]
        output.append({
            "actor_id": key["actor_id"],
            "offense_ref": key["offense_ref"],
            "offense_identity": catalog[key["offense_ref"]],
            "occurrence_id": key["occurrence_id"],
            "completion_state": result["completion"]["state"],
            "elements_state": result["elements"]["legal_state"],
            "liability_established": result.get("liability_result") is not None,
            "decisive_stage": result.get("decisive_stage"),
        })
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--scallop-artifact", type=Path, required=True)
    parser.add_argument("--gold-occurrences", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before Call 3")
    inventory = _index(args.inventory)
    scallop = _index(args.scallop_artifact)
    case_ids = tuple(scallop)
    if tuple(value for value in case_ids if value in inventory) != case_ids:
        raise ValueError("Scallop/inventory case mismatch")
    gold = load_gold_occurrences(
        args.gold_occurrences,
        case_text_by_id={key: str(value["question_text"]) for key, value in inventory.items()},
        required_case_ids=case_ids,
    )
    catalog = _offense_catalog(args.definitions)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["answer_markdown"],
        "properties": {"answer_markdown": {"type": "string", "minLength": 1}},
    }
    output = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for index, case_id in enumerate(case_ids, 1):
        source = inventory[case_id]
        conclusions = _conclusions(scallop[case_id], catalog)
        payload = {
            "sub_question_id": case_id,
            "case_text": source["question_text"],
            "question_prompt": source.get("question_prompt", ""),
            "gold_occurrences": [value.as_dict() for value in gold[case_id].occurrences],
            "symbolic_conclusions": conclusions,
        }
        assert_no_leaked_fields(payload)
        raw, metadata = client.complete_json(
            system_prompt=system_prompt,
            payload=payload,
            schema_name="v2_call3_irac",
            schema=schema,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            user_template=user_prompt,
        )
        usage = metadata.get("usage", {})
        for key in usage_total:
            usage_total[key] += int(usage.get(key, 0) or 0)
        output.append({
            "sub_question_id": case_id,
            "answer_markdown": raw["answer_markdown"],
            "symbolic_instance_count": len(conclusions),
            "established_instance_count": sum(
                bool(value["liability_established"]) for value in conclusions
            ),
            "usage": usage,
        })
        print(f"[{index}/{len(case_ids)}] {case_id}", flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call3_irac",
        "status": "SUCCEEDED",
        "case_ids": list(case_ids),
        "physical_request_count": len(case_ids),
        "usage": usage_total,
        "scallop_artifact_sha256": _sha256(args.scallop_artifact),
        "gold_occurrences_sha256": _sha256(args.gold_occurrences),
        "inventory_sha256": _sha256(args.inventory),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
