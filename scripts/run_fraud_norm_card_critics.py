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
    RulegenCritiqueValidationError,
    validate_rulegen_critique,
)

from scripts.run_fraud_norm_card_merge import (  # noqa: E402
    MODULE_PREFIXES,
    allowed_candidates,
    build_module_payloads,
)
from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    CRITIC_PROMPT,
    CRITIC_SCHEMA,
    SAFE_RUN_ID,
    prompt_with_schema,
    write_json,
)


NORM_CARD_MANIFEST = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_manifest.json"
)
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_norm_card_critics"
TRACKED_ROOT = PROJECT_ROOT / "data/rulegen/fraud/norm_card_reviews"


def load_card_sets() -> dict[str, dict[str, Any]]:
    manifest = read_json(NORM_CARD_MANIFEST)
    return {
        module["module"]: read_json(PROJECT_ROOT / module["path"])
        for module in manifest["modules"]
    }


def partition_cards(
    card_set: dict[str, Any], cards_per_job: int
) -> list[dict[str, Any]]:
    cards = card_set["cards"]
    partitions: list[dict[str, Any]] = []
    for start in range(0, len(cards), cards_per_job):
        part_cards = cards[start : start + cards_per_job]
        part_comment_ids = sorted(
            {
                ref["comment_id"]
                for card in part_cards
                for ref in card["source_refs"]
            }
        )
        review_questions: list[str] = []
        review_ids = [
            card["id"] for card in part_cards if card["review_required"]
        ]
        precedent_ids = [
            card["id"]
            for card in part_cards
            if card["formalization"] == "context_only"
        ]
        variant_ids = [
            card["id"]
            for card in part_cards
            if card["formalization"] == "policy_variant"
        ]
        if review_ids:
            review_questions.append(
                "Verify authority, scope, polarity, and formalization for these "
                "review-required cards: " + ", ".join(review_ids)
            )
        if precedent_ids:
            review_questions.append(
                "Verify the primary decisions and permissible generalization of these "
                "commentary-reported case cards: " + ", ".join(precedent_ids)
            )
        if variant_ids:
            review_questions.append(
                "Group competing views and select the precedent-aligned practical policy "
                "for these variant cards: " + ", ".join(variant_ids)
            )
        partitions.append(
            {
                **card_set,
                "source_scope": {
                    **card_set["source_scope"],
                    "comment_ids": part_comment_ids,
                },
                "cards": part_cards,
                # Keep partial review questions card-specific. Repeating the module's
                # global questions here creates false out-of-scope findings.
                "legal_review_questions": review_questions,
                "coverage_gaps": [],
            }
        )
    return partitions


def candidate_payload_for_cards(
    cards: list[dict[str, Any]],
    candidates: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    by_request: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for card in cards:
        for ref in card["candidate_refs"]:
            key = (ref["request_id"], ref["candidate_id"])
            if key in seen:
                continue
            seen.add(key)
            by_request[key[0]].append(candidates[key])
    return [
        {"request_id": request_id, "candidates": request_candidates}
        for request_id, request_candidates in sorted(by_request.items())
    ]


def build_jobs(
    modules: list[str], cards_per_job: int, max_tokens: int
) -> tuple[list[JSONCompletionJob], dict[str, dict[str, Any]]]:
    prompt = prompt_with_schema(CRITIC_PROMPT, CRITIC_SCHEMA)
    payloads = build_module_payloads()
    card_sets = load_card_sets()
    jobs: list[JSONCompletionJob] = []
    metadata: dict[str, dict[str, Any]] = {}
    for module in modules:
        candidates = allowed_candidates(payloads[module])
        parts = partition_cards(card_sets[module], cards_per_job)
        for index, target in enumerate(parts, start=1):
            target_id = f"{target['card_set_id']}.part{index:03d}"
            request_id = f"fraud.normcards.{module}.part{index:03d}.critic"
            jobs.append(
                JSONCompletionJob(
                    request_id=request_id,
                    role="sol",
                    system_prompt=prompt,
                    payload={
                        "stage": "norm_card_set",
                        "target_id": target_id,
                        "target": target,
                        "bounded_source_material": {
                            "validated_candidates": candidate_payload_for_cards(
                                target["cards"], candidates
                            )
                        },
                    },
                    max_tokens=max_tokens,
                    reasoning_effort="low",
                )
            )
            metadata[request_id] = {
                "module": module,
                "part": index,
                "target_id": target_id,
                "cards": len(target["cards"]),
                "card_ids": [card["id"] for card in target["cards"]],
                "allowed_source_refs": [
                    ref
                    for card in target["cards"]
                    for ref in card["source_refs"]
                ],
            }
    return jobs, metadata


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    modules = args.module or list(MODULE_PREFIXES)
    jobs, metadata = build_jobs(
        modules, args.cards_per_job, args.sol_max_tokens
    )
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    results = await gateway.complete_many(jobs)
    write_usage_manifest(run_dir / "sol_usage.jsonl", results)

    validation: list[dict[str, Any]] = []
    for result in results:
        meta = metadata[result.request_id]
        output_path = run_dir / "sol" / f"{result.request_id}.json"
        write_json(output_path, result.output)
        errors: list[str] = []
        try:
            validate_rulegen_critique(
                result.output,
                expected_stage="norm_card_set",
                expected_target_id=meta["target_id"],
                allowed_source_refs=meta["allowed_source_refs"],
            )
        except RulegenCritiqueValidationError as exc:
            gateway.discard_cache(result)
            errors.extend(exc.errors)
        validation.append(
            {
                "request_id": result.request_id,
                "module": meta["module"],
                "part": meta["part"],
                "cards": meta["cards"],
                "valid": not errors,
                "errors": errors,
                "verdict": result.output.get("verdict"),
                "findings": len(result.output.get("findings", [])),
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
        "modules": modules,
        "cards_per_job": args.cards_per_job,
        "sol_model": config.model_for_role("sol"),
        "api_calls": sum(not result.cached for result in results),
        "cache_hits": sum(result.cached for result in results),
        "usage": usage,
        "validation": validation,
        "all_valid": all(record["valid"] for record in validation),
    }
    write_json(run_dir / "run.json", summary)
    return summary


def track_valid_reports(run_id: str, summary: dict[str, Any]) -> None:
    source_root = RUN_ROOT / run_id / "sol"
    destination = TRACKED_ROOT / run_id
    for record in summary["validation"]:
        if not record["valid"]:
            continue
        report = read_json(source_root / f"{record['request_id']}.json")
        write_json(destination / f"{record['request_id']}.json", report)
    write_json(destination / "run.json", summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Critique final fraud NormCardSet modules with Sol."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--module", action="append", choices=MODULE_PREFIXES)
    parser.add_argument("--cards-per-job", type=int, default=50)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--sol-max-tokens", type=int, default=20_000)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if args.cards_per_job < 1:
        parser.error("--cards-per-job must be positive")
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    modules = args.module or list(MODULE_PREFIXES)
    jobs, _ = build_jobs(modules, args.cards_per_job, args.sol_max_tokens)
    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "dry_run",
                    "modules": modules,
                    "cards": sum(
                        len(card_set["cards"])
                        for module, card_set in load_card_sets().items()
                        if module in modules
                    ),
                    "planned_api_calls": len(jobs),
                    "cards_per_job": args.cards_per_job,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    run_summary = RUN_ROOT / args.run_id / "run.json"
    if run_summary.exists():
        raise SystemExit(
            f"run ID already has an audit manifest: {args.run_id}; use a new run ID"
        )
    config = GatewayConfig.from_env(require_api_key=True, require_models=True)
    config = replace(config, max_concurrency=args.concurrency)
    summary = asyncio.run(execute(args, config))
    track_valid_reports(args.run_id, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["all_valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
