#!/usr/bin/env python3
"""Run Call 1.5-D factual defense-cue detection over validated Call 1.5 episodes.

한 요청 = factual episode 하나. 모델은 저작된 `factual_cue` 문장이 원문에 적혀 있는지만 답하고
doctrine id, 조문, cue scope는 payload에 들어가지 않는다. cue -> doctrine 매핑은 host가 저작된
표로만 적용한다.
"""

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
from idpr.v2.doctrine_cues import (
    DoctrineCueError,
    cue_output_schema,
    cue_request_payload,
    load_doctrine_cues,
    validate_cue_output,
)
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    parse_issue_binding_result,
    question_actor_ids,
)

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_CUES = ROOT / "data/v2/doctrine_raising_cues.yaml"
PROMPTS = ("v2_call15d_doctrine_cue", "v2_call15d_doctrine_cue_user")


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
    parser.add_argument("--cues", type=Path, default=DEFAULT_CUES)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--repair-temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--contract-retries", type=int, default=2)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 1.5-D model run")

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
    cues = load_doctrine_cues(args.cues)

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
            raise ValueError(f"{case_id}: missing Call 1.5 seed lineage")
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

        case_assessments: list[dict[str, Any]] = []
        episode_results: list[dict[str, Any]] = []
        for episode in binding_result.factual_episodes:
            request_count += 1
            episode_text = "\n".join(
                fragment.source_quote for fragment in episode.source_fragments
            )
            actor_labels = tuple(episode.participants)
            payload = cue_request_payload(
                case_id=case_id,
                factual_episode_id=episode.factual_episode_id,
                episode_text=episode_text,
                actor_labels=actor_labels,
                cues=cues,
            )
            assert_no_leaked_fields(payload)
            raw: dict[str, Any] | None = None
            usage: dict[str, Any] = {}
            metadata: dict[str, Any] = {}
            attempt_errors: list[str] = []
            episode_row: dict[str, Any] = {
                "factual_episode_id": episode.factual_episode_id,
                "episode_participant_ids": list(actor_labels),
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
                                        "Correct only the cue contract errors and resubmit "
                                        "the complete output."
                                    ),
                                },
                            }
                        raw, metadata = client.complete_json(
                            system_prompt=system_prompt,
                            user_template=user_prompt,
                            payload=attempt_payload,
                            schema_name="v2_call15d_doctrine_cue",
                            schema=cue_output_schema(cues, actor_labels),
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
                        assessments = validate_cue_output(
                            raw,
                            case_id=case_id,
                            factual_episode_id=episode.factual_episode_id,
                            episode_text=episode_text,
                            actor_labels=actor_labels,
                            cues=cues,
                        )
                        break
                    except (DoctrineCueError, VLLMClientError) as exc:
                        attempt_errors.append(
                            f"attempt {attempt}: {type(exc).__name__}: {exc}"
                        )
                        if attempt > args.contract_retries:
                            raise
                serialized = [value.as_dict() for value in assessments]
                case_assessments.extend(serialized)
                episode_row.update(
                    {
                        "cue_assessments": serialized,
                        "true_count": sum(
                            1 for value in serialized if value["truth"] == "TRUE"
                        ),
                        "unknown_count": sum(
                            1 for value in serialized if value["truth"] == "UNKNOWN"
                        ),
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
            except (DoctrineCueError, VLLMClientError) as exc:
                failed_episode_count += 1
                episode_row.update(
                    {
                        "error": f"{type(exc).__name__}: {exc}",
                        "attempt_errors": attempt_errors,
                        "raw_response": raw,
                    }
                )
            episode_results.append(episode_row)

        output_rows.append(
            {
                "sub_question_id": case_id,
                "responsibility_actor_ids": list(responsibility),
                "factual_episode_ids": [
                    value.factual_episode_id for value in binding_result.factual_episodes
                ],
                "episode_results": episode_results,
                "cue_assessments": case_assessments,
                "cue_assessment_count": len(case_assessments),
                "error": (
                    "one or more factual episodes failed"
                    if any("error" in value for value in episode_results)
                    else None
                ),
            }
        )
        print(
            f"[{case_index}/{len(case_ids)}] {case_id} "
            f"episodes={len(episode_results)} "
            f"true={sum(value.get('true_count', 0) for value in episode_results)}",
            flush=True,
        )

    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output_rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call15d_doctrine_cue",
        "status": "SUCCEEDED" if failed_episode_count == 0 else "FAILED",
        "contract": (
            "one episode per request; authored factual cues only; no doctrine ref, statute "
            "or cue scope in the payload"
        ),
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
        "cue_count": len(cues),
        "cue_ids": [cue.cue_id for cue in cues],
        "cue_assessment_count": sum(row["cue_assessment_count"] for row in output_rows),
        "usage": usage_total,
        "call15_artifact": str(args.call15_artifact),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "cues_sha256": _sha256(args.cues),
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
