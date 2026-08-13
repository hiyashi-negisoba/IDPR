#!/usr/bin/env python3
"""Run atomic single-seed recovery for offline-reviewed Call 1.5 misses."""

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
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    binding_seed_cues,
    load_binding_seed_cue_catalog,
    normalize_issue_binding_output,
    question_actor_ids,
    validate_issue_binding_output,
)
from idpr.v2.registry import load_definitions

PROMPTS = (
    "v2_call15_single_seed_recovery",
    "v2_call15_single_seed_recovery_user",
)


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema() -> dict[str, Any]:
    quotes = {
        "type": "array",
        "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["bindings"],
        "properties": {
            "bindings": {
                "type": "array",
                "maxItems": 8,
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "actor_id",
                        "actor_action_quotes",
                        "context_quotes",
                        "factual_targets",
                    ],
                    "properties": {
                        "actor_id": {"type": "string", "minLength": 1},
                        "actor_action_quotes": {**quotes, "minItems": 1},
                        "context_quotes": quotes,
                        "factual_targets": {
                            "type": "array",
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                    },
                },
            }
        },
    }


def _validate(
    raw: dict[str, Any],
    *,
    offense_ref: str,
    case_text: str,
    factual_scope_text: str,
    actor_ids: tuple[str, ...],
) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
    episodes = []
    bindings = []
    for index, binding in enumerate(raw.get("bindings", [])):
        quotes = list(
            dict.fromkeys(
                [*binding["actor_action_quotes"], *binding["context_quotes"]]
            )
        )
        participants = list(
            dict.fromkeys([binding["actor_id"], *binding["factual_targets"]])
        )
        episodes.append(
            {"episode_index": index, "source_quotes": quotes, "participants": participants}
        )
        bindings.append({"episode_index": index, **binding})
    payload = {
        "factual_episodes": episodes,
        "seed_results": [{"seed_index": 0, "bindings": bindings}],
    }
    normalized, changes = normalize_issue_binding_output(
        payload,
        case_text=case_text,
        factual_scope_text=factual_scope_text,
    )
    result = validate_issue_binding_output(
        normalized,
        seeds=(offense_ref,),
        case_text=case_text,
        factual_scope_text=factual_scope_text,
        candidate_actor_ids=actor_ids,
    )
    return result.as_dict(), changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--targets", type=Path)
    target_group.add_argument("--all-unbound", action="store_true")
    parser.add_argument("--call1", type=Path, required=True)
    parser.add_argument("--call15", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--binding-cues", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=1536)
    args = parser.parse_args()

    call1 = {row["sub_question_id"]: row for row in _jsonl(args.call1)}
    call15 = {row["sub_question_id"]: row for row in _jsonl(args.call15)}
    if args.targets is not None:
        targets = _jsonl(args.targets)
        selection_basis = "offline gold explicit misses; not a production selector"
        production_rule = (
            "apply the same recovery to every UNBOUND_SEED without rubric selection"
        )
    else:
        targets = [
            {
                "sub_question_id": case_id,
                "offense_ref": result["offense_ref"],
                "selection_basis": "all_unbound_seed_no_rubric",
            }
            for case_id, row in call15.items()
            for result in row["seed_results"]
            if not result["bindings"]
        ]
        selection_basis = "all Call 1.5 UNBOUND_SEED rows; no rubric selection"
        production_rule = "production-compatible target selection"
    inventory = {row["sub_question_id"]: row for row in _jsonl(args.inventory)}
    registry = load_definitions(args.definitions)
    cues = load_binding_seed_cue_catalog(args.binding_cues)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(name) for name in PROMPTS)
    rows = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for index, target in enumerate(targets, 1):
        case_id = target["sub_question_id"]
        offense_ref = target["offense_ref"]
        seeds = call1[case_id]["normalized_seeds"]
        if offense_ref not in seeds:
            raise ValueError(f"{case_id}/{offense_ref}: target is not an explicit Call 1 seed")
        seed_index = seeds.index(offense_ref)
        if call15[case_id]["seed_results"][seed_index]["bindings"]:
            raise ValueError(f"{case_id}/{offense_ref}: target is already bound")
        source = inventory[case_id]
        case_text = source["question_text"]
        scope = scoped_question_text(case_text, source["question_prompt"])
        actor_ids = question_actor_ids(source["question_prompt"])
        cue = binding_seed_cues(registry, (offense_ref,), cue_catalog=cues)[0]
        payload = {
            "question_prompt": source["question_prompt"],
            "candidate_actor_ids": list(actor_ids),
            "case_text": case_text,
            "factual_scope_text": scope,
            "seed": cue.as_dict(),
        }
        assert_no_leaked_fields(payload)
        raw, metadata = client.complete_json(
            system_prompt=system_prompt,
            user_template=user_prompt,
            payload=payload,
            schema_name="v2_call15_single_seed_recovery",
            schema=_schema(),
            max_tokens=args.max_tokens,
            temperature=0.0,
            seed=1,
        )
        usage = metadata.get("usage", {})
        for key in usage_total:
            usage_total[key] += int(usage.get(key, 0) or 0)
        try:
            validated, changes = _validate(
                raw,
                offense_ref=offense_ref,
                case_text=case_text,
                factual_scope_text=scope,
                actor_ids=actor_ids,
            )
            binding_count = sum(
                len(result["bindings"]) for result in validated["seed_results"]
            )
            row = {
                **target,
                "seed_index": seed_index,
                "binding_count": binding_count,
                **validated,
                "raw_response": raw,
                "host_normalizations": list(changes),
                "usage": usage,
            }
            status = str(binding_count)
        except IssueBindingContractError as exc:
            binding_count = 0
            row = {
                **target,
                "seed_index": seed_index,
                "binding_count": 0,
                "raw_response": raw,
                "error": f"{type(exc).__name__}: {exc}",
                "errors": list(exc.errors),
                "usage": usage,
            }
            status = "CONTRACT_FAIL"
        rows.append(row)
        print(f"[{index}/{len(targets)}] {case_id}/{offense_ref}: {status}", flush=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call15_single_seed_recovery_diagnostic",
        "status": "SUCCEEDED" if not any("error" in row for row in rows) else "DEGRADED",
        "selection_basis": selection_basis,
        "production_rule": production_rule,
        "model": args.model,
        "sampling": {"temperature": 0.0, "max_tokens": args.max_tokens, "seed": 1},
        "target_count": len(rows),
        "recovered_target_count": sum(bool(row["binding_count"]) for row in rows),
        "binding_count": sum(row["binding_count"] for row in rows),
        "contract_failure_count": sum("error" in row for row in rows),
        "usage": usage_total,
        "targets_sha256": _sha256(args.targets) if args.targets is not None else None,
        "call1_sha256": _sha256(args.call1),
        "call15_sha256": _sha256(args.call15),
        "prompts": {name: _sha256(prompt_path(name)) for name in PROMPTS},
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
