from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import defaultdict
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.llm import (  # noqa: E402
    GatewayConfig,
    JSONCompletionJob,
    LLMGateway,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    NormCardValidationError,
    validate_norm_card_set,
)

from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    SAFE_RUN_ID,
    load_jsonl,
    prompt_with_schema,
    write_json,
)


REQUESTS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_candidate_manifest.json"
MERGE_PROMPT = PROJECT_ROOT / "prompts/rulegen_merge_norm_cards.md"
NORM_CARD_SCHEMA = PROJECT_ROOT / "docs/contracts/norm_card_set.schema.json"
NORM_CARD_GOLD = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_set_exemplar.json"
)
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_norm_card_merge"


MODULE_PREFIXES: dict[str, tuple[str, ...]] = {
    "general_object": ("Ⅰ", "Ⅱ", "Ⅲ"),
    "deception": ("Ⅳ.1",),
    "mistake_disposition": ("Ⅳ.2", "Ⅳ.3"),
    "damage_acquisition": ("Ⅳ.4", "Ⅳ.5", "Ⅳ.6"),
    "intent": ("Ⅴ",),
    "special_forms": ("Ⅵ",),
    "stages_participation": ("Ⅶ", "Ⅷ"),
    "concurrence": ("Ⅸ", "Ⅹ"),
}


def module_for_section(section_path: str) -> str:
    for module, prefixes in MODULE_PREFIXES.items():
        if any(section_path.startswith(prefix) for prefix in prefixes):
            return module
    raise ValueError(f"No NormCard module for section {section_path}")


def load_merge_context() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    requests = load_jsonl(REQUESTS)
    requests_by_id = {request["request_id"]: request for request in requests}
    manifest = read_json(MANIFEST)
    batches = {
        batch["request_id"]: read_json(PROJECT_ROOT / batch["path"])
        for batch in manifest["batches"]
    }
    return requests, requests_by_id, batches


def build_module_payloads() -> dict[str, dict[str, Any]]:
    _, requests_by_id, batches = load_merge_context()
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    modules_by_request: dict[str, set[str]] = defaultdict(set)
    for request_id, batch in batches.items():
        for candidate in batch["candidates"]:
            module = module_for_section(
                candidate["source_refs"][0]["section_path"]
            )
            grouped[module][request_id].append(candidate)
            modules_by_request[request_id].add(module)

    payloads: dict[str, dict[str, Any]] = {}
    for module in MODULE_PREFIXES:
        validated_batches: list[dict[str, Any]] = []
        comment_ids: set[str] = set()
        for request_id, candidates in grouped[module].items():
            batch = batches[request_id]
            validated_batches.append(
                {
                    "request_id": request_id,
                    "status": "draft",
                    "candidates": candidates,
                    "unresolved_questions": (
                        batch["unresolved_questions"]
                        if len(modules_by_request[request_id]) == 1
                        else []
                    ),
                }
            )
            comment_ids.update(
                ref["comment_id"]
                for candidate in candidates
                for ref in candidate["source_refs"]
            )
        payloads[module] = {
            "task": "merge_norm_cards",
            "card_set_id": f"kr.fraud.article347.{module}.norms.v1",
            "issue_tag": f"fraud_{module}",
            "target_paths": [f"commentary://001692/제347조#{module}"],
            "allowed_comment_ids": sorted(comment_ids),
            "validated_batches": validated_batches,
            "unresolved_questions": sorted(
                {
                    question
                    for request_id in grouped[module]
                    for question in batches[request_id]["unresolved_questions"]
                }
            ),
            "constraints": {
                "status": "draft",
                "legal_review": "pending",
                "construction": "api_merged",
            },
        }
    return payloads


def allowed_refs(payload: dict[str, Any]) -> set[tuple[str, str, str]]:
    return {
        (ref["comment_id"], ref["section_path"], ref["quote"])
        for batch in payload["validated_batches"]
        for candidate in batch["candidates"]
        for ref in candidate["source_refs"]
    }


def allowed_candidates(
    payload: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (batch["request_id"], candidate["candidate_id"]): candidate
        for batch in payload["validated_batches"]
        for candidate in batch["candidates"]
    }


def build_jobs(
    payloads: dict[str, dict[str, Any]], max_tokens: int
) -> list[JSONCompletionJob]:
    prompt = prompt_with_schema(MERGE_PROMPT, NORM_CARD_SCHEMA)
    prompt += (
        "\nGold structural example:\n"
        "Learn only its candidate-to-card transformation. Never copy a card, source, "
        "authority choice, or conclusion absent from the current module payload.\n"
        "```json\n"
        + NORM_CARD_GOLD.read_text(encoding="utf-8").rstrip()
        + "\n```\n"
    )
    return [
        JSONCompletionJob(
            request_id=f"fraud.{module}.normcards.v1",
            role="terra",
            system_prompt=prompt,
            payload=payload,
            max_tokens=max_tokens,
        )
        for module, payload in payloads.items()
    ]


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    all_payloads = build_module_payloads()
    payloads = {
        module: all_payloads[module]
        for module in args.module or MODULE_PREFIXES
    }
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    results = await gateway.complete_many(
        build_jobs(payloads, args.terra_max_tokens)
    )
    write_usage_manifest(run_dir / "terra_usage.jsonl", results)

    requests, _, _ = load_merge_context()
    commentary_by_id = {
        row["comment_id"]: row
        for request in requests
        for row in request["commentary_chunks"]
    }
    request_comment_ids = {
        request["request_id"]: {
            row["comment_id"] for row in request["commentary_chunks"]
        }
        for request in requests
    }
    validation: list[dict[str, Any]] = []
    for result in results:
        module = result.request_id.removeprefix("fraud.").removesuffix(
            ".normcards.v1"
        )
        payload = payloads[module]
        output_path = run_dir / "norm_cards" / f"{module}.json"
        write_json(output_path, result.output)
        errors: list[str] = []
        if result.output.get("card_set_id") != payload["card_set_id"]:
            errors.append("card_set_id does not match the module request")
        if result.output.get("issue_tag") != payload["issue_tag"]:
            errors.append("issue_tag does not match the module request")
        try:
            validate_norm_card_set(
                result.output,
                commentary_by_id,
                request_comment_ids,
                allowed_candidates=allowed_candidates(payload),
            )
        except NormCardValidationError as exc:
            errors.extend(exc.errors)
        if errors:
            gateway.discard_cache(result)
        validation.append(
            {
                "module": module,
                "valid": not errors,
                "errors": errors,
                "input_candidates": sum(
                    len(batch["candidates"])
                    for batch in payload["validated_batches"]
                ),
                "cards": len(result.output.get("cards", [])),
                "output_path": str(output_path.relative_to(PROJECT_ROOT)),
            }
        )

    usage = {
        key: sum(
            result.usage.get(key, 0) for result in results if not result.cached
        )
        for key in (
            "prompt_tokens",
            "completion_tokens",
            "reasoning_tokens",
            "total_tokens",
        )
    }
    summary = {
        "version": "1.0.0",
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "modules": list(payloads),
        "terra_model": config.model_for_role("terra"),
        "api_calls": sum(not result.cached for result in results),
        "cache_hits": sum(result.cached for result in results),
        "usage": usage,
        "validation": validation,
        "all_valid": all(record["valid"] for record in validation),
    }
    write_json(run_dir / "run.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge fraud candidate modules into validated NormCardSets."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--module", action="append", choices=MODULE_PREFIXES)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--terra-max-tokens", type=int, default=64_000)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    payloads = build_module_payloads()
    selected = args.module or list(MODULE_PREFIXES)
    if not args.execute:
        summary = {
            "mode": "dry_run",
            "modules": {
                module: {
                    "candidates": sum(
                        len(batch["candidates"])
                        for batch in payloads[module]["validated_batches"]
                    ),
                    "payload_chars": len(
                        json.dumps(payloads[module], ensure_ascii=False)
                    ),
                }
                for module in selected
            },
            "planned_api_calls": len(selected),
            "max_concurrency": args.concurrency,
            "terra_max_completion_tokens": args.terra_max_tokens,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    config = GatewayConfig.from_env(require_api_key=True, require_models=True)
    config = replace(config, max_concurrency=args.concurrency)
    summary = asyncio.run(execute(args, config))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["all_valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
