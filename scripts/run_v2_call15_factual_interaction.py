#!/usr/bin/env python3
"""Run offense-free Call 1.5-P over validated Call 1.5 factual episodes."""

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
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    factual_interaction_request_payload,
    factual_interaction_schema,
    validate_factual_interaction_output,
)
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    parse_issue_binding_result,
    question_actor_ids,
)

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
PROMPTS = (
    "v2_call15_factual_interaction",
    "v2_call15_factual_interaction_user",
)


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--repair-temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--contract-retries", type=int, default=2)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 1.5-P model run")

    case_ids = tuple(args.case_id) if args.case_id else _case_ids(args.case_list)
    inventory = _index(args.inventory, "inventory")
    call15 = _index(args.call15_artifact, "Call 1.5 artifact")
    missing = [
        case_id
        for case_id in case_ids
        if case_id not in inventory or case_id not in call15
    ]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")

    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    output_rows: list[dict[str, Any]] = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    request_count = 0
    failed_episode_count = 0

    for case_index, case_id in enumerate(case_ids, 1):
        source = inventory[case_id]
        binding_row = call15[case_id]
        seeds = binding_row.get("seeds")
        if not isinstance(seeds, list) or not seeds:
            raise ValueError(f"{case_id}: Call 1.5 row has no seed lineage")
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
        except IssueBindingContractError as exc:
            raise ValueError(f"{case_id}: invalid Call 1.5 lineage: {exc}") from exc

        case_interactions: list[dict[str, Any]] = []
        episode_results: list[dict[str, Any]] = []
        for episode in binding_result.factual_episodes:
            request_count += 1
            payload = factual_interaction_request_payload(
                case_id=case_id,
                question_prompt=str(source["question_prompt"]),
                responsibility_actor_ids=responsibility,
                episode=episode,
            )
            assert_no_leaked_fields(payload)
            raw: dict[str, Any] | None = None
            attempt_errors: list[str] = []
            episode_row: dict[str, Any] = {
                "factual_episode_id": episode.factual_episode_id,
                "episode_participant_ids": list(episode.participants),
            }
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
                                        "Correct only the factual interaction contract "
                                        "errors and resubmit the complete output."
                                    ),
                                },
                            }
                        raw, metadata = client.complete_json(
                            system_prompt=system_prompt,
                            user_template=user_prompt,
                            payload=attempt_payload,
                            schema_name="v2_call15_factual_interaction",
                            schema=factual_interaction_schema(),
                            max_tokens=args.max_tokens,
                            temperature=(
                                args.temperature
                                if attempt == 1
                                else args.repair_temperature
                            ),
                            seed=args.seed + attempt - 1,
                        )
                        usage = metadata.get("usage", {})
                        for key in usage_total:
                            usage_total[key] += int(usage.get(key, 0) or 0)
                        interactions = validate_factual_interaction_output(
                            raw,
                            case_text=str(source["question_text"]),
                            episode=episode,
                        )
                        break
                    except (
                        FactualInteractionContractError,
                        VLLMClientError,
                    ) as exc:
                        attempt_errors.append(
                            f"attempt {attempt}: {type(exc).__name__}: {exc}"
                        )
                        if attempt > args.contract_retries:
                            raise
                serialized = [value.as_dict() for value in interactions]
                case_interactions.extend(serialized)
                episode_row.update(
                    {
                        "interactions": serialized,
                        "interaction_count": len(serialized),
                        "attempt_count": len(attempt_errors) + 1,
                        "attempt_errors": attempt_errors,
                        "raw_response": raw,
                        "usage": usage,
                        "model_response": {
                            "id": metadata.get("id"),
                            "finish_reason": metadata.get("finish_reason"),
                        },
                    }
                )
            except (FactualInteractionContractError, VLLMClientError) as exc:
                failed_episode_count += 1
                episode_row.update(
                    {
                        "error": f"{type(exc).__name__}: {exc}",
                        "errors": list(getattr(exc, "errors", (str(exc),))),
                        "attempt_errors": attempt_errors,
                        "raw_response": raw,
                    }
                )
            episode_results.append(episode_row)

        output_rows.append(
            {
                "sub_question_id": case_id,
                "responsibility_actor_ids": list(responsibility),
                "episode_results": episode_results,
                "interactions": case_interactions,
                "interaction_count": len(case_interactions),
                "error": (
                    "one or more factual episodes failed"
                    if any("error" in value for value in episode_results)
                    else None
                ),
            }
        )
        print(
            f"[{case_index}/{len(case_ids)}] {case_id} "
            f"episodes={len(episode_results)} interactions={len(case_interactions)}",
            flush=True,
        )

    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output_rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call15_factual_interaction",
        "status": "SUCCEEDED" if failed_episode_count == 0 else "FAILED",
        "contract": "one episode per request; offense-free exact-quote factual interaction",
        "model": args.model,
        "sampling": {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "seed": args.seed,
        },
        "repair_sampling": {"temperature": args.repair_temperature},
        "contract_retries": args.contract_retries,
        "case_ids": list(case_ids),
        "case_count": len(output_rows),
        "episode_request_count": request_count,
        "failed_episode_count": failed_episode_count,
        "interaction_count": sum(row["interaction_count"] for row in output_rows),
        "usage": usage_total,
        "call15_artifact": str(args.call15_artifact),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "inventory_sha256": _sha256(args.inventory),
        "case_list_sha256": _sha256(args.case_list),
        "prompts": {value: _sha256(prompt_path(value)) for value in PROMPTS},
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    if failed_episode_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
