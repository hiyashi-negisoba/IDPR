#!/usr/bin/env python3
"""Ask the authored concurrence condition for each planned pair.

한 요청 = pair 하나. 모델은 두 행위 사이의 관계 하나만 답하고, 죄명·조문·`흡수`는 payload에
들어가지 않는다. 흡수되는 쪽 죄가 성립하는지는 그 instance의 elements가 이미 판단했다.
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
from idpr.v2.doctrine_cues import canonical_episode_text
from idpr.v2.issue_binding import parse_issue_binding_result, question_actor_ids
from idpr.v2.runtime.concurrence import load_concurrence_rules
from idpr.v2.runtime.concurrence_condition import (
    ConcurrenceConditionError,
    ConcurrenceConditionPair,
    condition_output_schema,
    condition_request_payload,
    evidence_texts,
    validate_condition_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_RULES = ROOT / "data/v2/concurrence_rules.yaml"
PROMPTS = ("v2_absorption_condition_pair", "v2_absorption_condition_pair_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _index(path: Path) -> dict[str, dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    return {str(row["sub_question_id"]): row for row in rows}


def _pair(case_id: str, entry: dict[str, Any]) -> ConcurrenceConditionPair:
    def key(payload: dict[str, Any]) -> OffenseInstanceKey:
        return OffenseInstanceKey(
            case_id,
            str(payload["actor_id"]),
            str(payload["offense_ref"]),
            str(payload["occurrence_id"]),
        )

    return ConcurrenceConditionPair(
        pair_id=str(entry["pair_id"]),
        rule_id=str(entry["rule_id"]),
        condition_ref=str(entry["condition_ref"]),
        absorbed=key(entry["absorbed_instance_key"]),
        absorbing=key(entry["absorbing_instance_key"]),
        factual_episode_id=str(entry["factual_episode_id"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--pair-plan", type=Path, required=True)
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--repair-temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--contract-retries", type=int, default=2)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before an absorption-condition run")

    rules = {rule.rule_id: rule for rule in load_concurrence_rules(args.rules)}
    plans = _index(args.pair_plan)
    inventory = _index(args.inventory)
    call15 = _index(args.call15_artifact)

    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    output_rows: list[dict[str, Any]] = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    request_count = 0
    failed_count = 0
    for case_id, plan in plans.items():
        entries = plan.get("concurrence_condition_pairs") or []
        if not entries:
            continue
        source = inventory[case_id]
        binding_row = call15[case_id]
        binding_result = parse_issue_binding_result(
            {
                "factual_episodes": binding_row.get("factual_episodes"),
                "seed_results": binding_row.get("seed_results"),
            },
            seeds=binding_row["seeds"],
            case_text=str(source["question_text"]),
            candidate_actor_ids=question_actor_ids(str(source["question_prompt"])),
        )
        episode_text_by_id = {
            episode.factual_episode_id: canonical_episode_text(
                fragment.source_quote for fragment in episode.source_fragments
            )
            for episode in binding_result.factual_episodes
        }

        assessments: list[dict[str, Any]] = []
        for entry in entries:
            request_count += 1
            pair = _pair(case_id, entry)
            rule = rules[pair.rule_id]
            payload = condition_request_payload(
                pair,
                rule=rule,
                episode_text=episode_text_by_id[pair.factual_episode_id],
                absorbed_conduct=str(entry["first_conduct"]),
                absorbing_conduct=str(entry["second_conduct"]),
            )
            assert_no_leaked_fields(payload)
            evidence = evidence_texts(payload)
            raw: dict[str, Any] | None = None
            usage: dict[str, Any] = {}
            metadata: dict[str, Any] = {}
            attempt_errors: list[str] = []
            row: dict[str, Any] = {
                "pair_id": pair.pair_id,
                "rule_id": pair.rule_id,
                "condition_ref": pair.condition_ref,
                "request_payload": payload,
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
                                        "Correct only the contract errors and resubmit the "
                                        "complete output."
                                    ),
                                },
                            }
                        raw, metadata = client.complete_json(
                            system_prompt=system_prompt,
                            user_template=user_prompt,
                            payload=attempt_payload,
                            schema_name="v2_absorption_condition_pair",
                            schema=condition_output_schema(pair),
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
                        assessment = validate_condition_output(
                            raw, pair=pair, evidence=evidence
                        )
                        break
                    except (ConcurrenceConditionError, VLLMClientError) as exc:
                        attempt_errors.append(f"attempt {attempt}: {type(exc).__name__}: {exc}")
                        if attempt > args.contract_retries:
                            raise
                row.update(
                    {
                        **assessment.as_dict(),
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
                assessments.append(row)
            except (ConcurrenceConditionError, VLLMClientError) as exc:
                failed_count += 1
                row.update(
                    {
                        "error": f"{type(exc).__name__}: {exc}",
                        "attempt_errors": attempt_errors,
                        "raw_response": raw,
                    }
                )
                assessments.append(row)
            print(
                f"{case_id} {pair.pair_id} -> {row.get('truth', row.get('error'))}",
                flush=True,
            )

        output_rows.append(
            {
                "sub_question_id": case_id,
                "concurrence_condition_assessments": assessments,
                "error": (
                    "one or more pairs failed"
                    if any("error" in value for value in assessments)
                    else None
                ),
            }
        )

    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output_rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_absorption_condition_pair",
        "status": "SUCCEEDED" if failed_count == 0 else "FAILED",
        "contract": (
            "one pair per request; the model answers only the authored pair relation; no "
            "offense ref, statute, rule id or absorption vocabulary in the payload"
        ),
        "model": args.model,
        "sampling": {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "seed": args.seed,
        },
        "contract_retries": args.contract_retries,
        "case_count": len(output_rows),
        "pair_request_count": request_count,
        "failed_pair_count": failed_count,
        "pair_plan": str(args.pair_plan),
        "pair_plan_sha256": _sha256(args.pair_plan),
        "rules_sha256": _sha256(args.rules),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "usage": usage_total,
        "prompts": {value: _sha256(prompt_path(value)) for value in PROMPTS},
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    if failed_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
