#!/usr/bin/env python3
"""Run Call 1.5 case-time issue binding over a frozen Call 1 artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    binding_seed_cues,
    issue_binding_request_payload,
    issue_binding_schema,
    load_binding_seed_cue_catalog,
    normalize_issue_binding_output,
    question_actor_ids,
    validate_issue_binding_output,
)
from idpr.v2.registry import load_definitions

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_BINDING_CUES = ROOT / "data/v2/binding_seed_cues.yaml"
PROMPTS = ("v2_call15_issue_binding", "v2_call15_issue_binding_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(value, dict) for value in values):
        raise ValueError(f"{path}: every row must be an object")
    return values


def _index(path: Path, label: str) -> dict[str, dict[str, Any]]:
    values = _jsonl(path)
    output = {str(value.get("sub_question_id")): value for value in values}
    if len(output) != len(values):
        raise ValueError(f"{label}: duplicate sub_question_id")
    return output


def _case_ids(path: Path) -> tuple[str, ...]:
    values = tuple(line.strip() for line in path.read_text().splitlines() if line.strip())
    if not values or len(values) != len(set(values)):
        raise ValueError(f"{path}: case ids must be nonempty and unique")
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--call1-artifact", type=Path, required=True)
    parser.add_argument(
        "--occurrences",
        type=Path,
        required=True,
        help="reference/supervision lineage only; never constrains the production binding universe",
    )
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--binding-cues", type=Path, default=DEFAULT_BINDING_CUES)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--repair-temperature", type=float, default=0.2)
    parser.add_argument("--contract-retries", type=int, default=2)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 1.5 model run")

    case_ids = tuple(args.case_id) if args.case_id else _case_ids(args.case_list)
    inventory = _index(args.inventory, "inventory")
    call1 = _index(args.call1_artifact, "Call 1 artifact")
    missing = [value for value in case_ids if value not in inventory or value not in call1]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")
    registry = load_definitions(args.definitions)
    cue_catalog = load_binding_seed_cue_catalog(args.binding_cues)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for case_index, case_id in enumerate(case_ids, start=1):
        source = inventory[case_id]
        call1_row = call1[case_id]
        seeds = call1_row.get("normalized_seeds")
        if call1_row.get("error") or not isinstance(seeds, list) or not seeds:
            raise ValueError(f"{case_id}: unusable Call 1 row")
        case_text = str(source["question_text"])
        factual_scope_text = scoped_question_text(
            case_text, str(source["question_prompt"])
        )
        cues = binding_seed_cues(registry, seeds, cue_catalog=cue_catalog)
        payload = issue_binding_request_payload(
            question_prompt=str(source["question_prompt"]),
            case_text=case_text,
            factual_scope_text=factual_scope_text,
            seed_cues=cues,
        )
        assert_no_leaked_fields(payload)
        row: dict[str, Any] = {
            "sub_question_id": case_id,
            "seeds": seeds,
            "seed_cues": [value.as_dict() for value in cues],
        }
        raw: dict[str, Any] | None = None
        attempt_errors: list[str] = []
        try:
            for attempt in range(1, args.contract_retries + 2):
                try:
                    attempt_payload = payload
                    if attempt_errors:
                        attempt_payload = {
                            **payload,
                            "retry_contract_feedback": {
                                "validation_errors": attempt_errors[-1:],
                                "previous_invalid_output": raw,
                                "instruction": (
                                    "Correct only the factual episode/binding contract errors "
                                    "and resubmit the complete output."
                                ),
                            },
                        }
                    raw, metadata = client.complete_json(
                        system_prompt=system_prompt,
                        user_template=user_prompt,
                        payload=attempt_payload,
                        schema_name="v2_call15_issue_binding",
                        schema=issue_binding_schema(seed_count=len(seeds)),
                        max_tokens=args.max_tokens,
                        temperature=(
                            args.temperature if attempt == 1 else args.repair_temperature
                        ),
                        seed=attempt,
                    )
                    usage = metadata.get("usage", {})
                    for key in usage_total:
                        usage_total[key] += int(usage.get(key, 0) or 0)
                    model_raw = raw
                    raw, host_normalizations = normalize_issue_binding_output(
                        raw,
                        case_text=case_text,
                        factual_scope_text=factual_scope_text,
                    )
                    result = validate_issue_binding_output(
                        raw,
                        seeds=seeds,
                        case_text=case_text,
                        factual_scope_text=factual_scope_text,
                        candidate_actor_ids=question_actor_ids(
                            str(source["question_prompt"])
                        ),
                    )
                    break
                except (IssueBindingContractError, VLLMClientError) as exc:
                    attempt_errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
                    if attempt > args.contract_retries:
                        raise
            row.update(
                {
                    **result.as_dict(),
                    "binding_count": len(result.bindings),
                    "usage": usage,
                    "attempt_count": len(attempt_errors) + 1,
                    "attempt_errors": attempt_errors,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                    "raw_response": raw,
                    "model_raw_response": model_raw,
                    "host_normalizations": list(host_normalizations),
                }
            )
            status = f"ok ({len(result.bindings)} bindings)"
        except (IssueBindingContractError, VLLMClientError) as exc:
            row.update(
                {
                    "raw_response": raw,
                    "error": f"{type(exc).__name__}: {exc}",
                    "errors": list(getattr(exc, "errors", (str(exc),))),
                    "attempt_errors": attempt_errors,
                }
            )
            status = "FAIL"
        rows.append(row)
        print(f"[{case_index}/{len(case_ids)}] {case_id} {status}", flush=True)

    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in rows),
        encoding="utf-8",
    )
    failures = sum("error" in value for value in rows)
    manifest = {
        "step": "v2_call15_issue_binding",
        "status": "SUCCEEDED" if not failures else "FAILED",
        "contract": (
            "full-case factual episode binding with distinct actor-action/context fragments; "
            "no legal dependency or DAG"
        ),
        "model": args.model,
        "sampling": {"temperature": args.temperature, "max_tokens": args.max_tokens},
        "repair_sampling": {
            "temperature": args.repair_temperature,
            "seed_rule": "attempt_number",
        },
        "contract_retries": args.contract_retries,
        "case_ids": list(case_ids),
        "case_count": len(rows),
        "failed_case_count": failures,
        "binding_count": sum(int(value.get("binding_count", 0)) for value in rows),
        "usage": usage_total,
        "call1_artifact": str(args.call1_artifact),
        "call1_artifact_sha256": _sha256(args.call1_artifact),
        "occurrences": str(args.occurrences),
        "occurrences_sha256": _sha256(args.occurrences),
        "occurrences_role": "reference/supervision only; not a production input universe",
        "definitions": str(args.definitions),
        "definitions_note": "source of closed seed identity and statutory references",
        "binding_cues": str(args.binding_cues),
        "binding_cues_sha256": _sha256(args.binding_cues),
        "inventory_sha256": _sha256(args.inventory),
        "case_list_sha256": _sha256(args.case_list),
        "prompts": {value: _sha256(prompt_path(value)) for value in PROMPTS},
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
