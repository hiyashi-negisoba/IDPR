from __future__ import annotations

import argparse
import asyncio
import json
import sys
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
    apply_norm_candidate_patch,
    repair_ocr_interrupted_candidate_quotes,
    validate_norm_candidate_batch,
)

from scripts.run_fraud_rulegen_critics import (  # noqa: E402
    MANIFEST,
    load_candidate_paths,
    read_json,
    selected_requests,
)
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    REQUESTS,
    SAFE_RUN_ID,
    load_jsonl,
    prompt_with_schema,
    write_json,
)


PATCH_PROMPT = PROJECT_ROOT / "prompts/rulegen_patch_norm_candidates.md"
PATCH_SCHEMA = PROJECT_ROOT / "docs/contracts/norm_candidate_patch.schema.json"
DEFAULT_CRITIC_ROOT = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_critics/fraud_full_critics_v1/sol"
)
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen_patches"


def build_jobs(
    requests: list[dict[str, Any]],
    candidate_paths: dict[str, Path],
    critic_root: Path,
    max_tokens: int,
) -> list[JSONCompletionJob]:
    prompt = prompt_with_schema(PATCH_PROMPT, PATCH_SCHEMA)
    jobs: list[JSONCompletionJob] = []
    for request in requests:
        request_id = request["request_id"]
        target = read_json(candidate_paths[request_id])
        validate_norm_candidate_batch(target, request)
        critique = read_json(critic_root / f"{request_id}.critic.json")
        jobs.append(
            JSONCompletionJob(
                request_id=f"{request_id}.patch1",
                role="terra",
                system_prompt=prompt,
                payload={
                    "source_request": request,
                    "target": target,
                    "critic_report": critique,
                },
                max_tokens=max_tokens,
            )
        )
    return jobs


def repair_patch_quotes(
    patch: dict[str, Any], request: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    batch = {
        "request_id": request["request_id"],
        "status": "draft",
        "candidates": patch.get("add_candidates", []),
        "unresolved_questions": [],
    }
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    repaired, records = repair_ocr_interrupted_candidate_quotes(
        batch, commentary
    )
    result = dict(patch)
    result["add_candidates"] = repaired["candidates"]
    return result, records


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    requests = selected_requests(args)
    requests_by_id = {request["request_id"]: request for request in requests}
    candidate_paths = load_candidate_paths()
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    results = await gateway.complete_many(
        build_jobs(
            requests,
            candidate_paths,
            args.critic_root,
            args.terra_max_tokens,
        )
    )
    write_usage_manifest(run_dir / "terra_usage.jsonl", results)

    validation: list[dict[str, Any]] = []
    for result in results:
        request_id = result.request_id.removesuffix(".patch1")
        request = requests_by_id[request_id]
        target = read_json(candidate_paths[request_id])
        raw_path = run_dir / "patch_raw" / f"{request_id}.json"
        write_json(raw_path, result.output)
        patch, repairs = repair_patch_quotes(result.output, request)
        patch_path = run_dir / "patch" / f"{request_id}.json"
        write_json(patch_path, patch)
        try:
            revised = apply_norm_candidate_patch(
                target,
                patch,
                request,
                expected_target_id=request_id,
            )
        except ValueError as exc:
            gateway.discard_cache(result)
            validation.append(
                {
                    "request_id": request_id,
                    "valid": False,
                    "error": str(exc),
                    "quote_repairs": repairs,
                    "patch_path": str(patch_path.relative_to(PROJECT_ROOT)),
                }
            )
            continue

        output_path = run_dir / "candidates" / f"{request_id}.json"
        write_json(output_path, revised)
        validation.append(
            {
                "request_id": request_id,
                "valid": True,
                "removed": len(patch["remove_candidate_ids"]),
                "added": len(patch["add_candidates"]),
                "questions_added": len(patch["append_unresolved_questions"]),
                "quote_repairs": repairs,
                "candidates_before": len(target["candidates"]),
                "candidates_after": len(revised["candidates"]),
                "patch_path": str(patch_path.relative_to(PROJECT_ROOT)),
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
        "manifest": str(MANIFEST.relative_to(PROJECT_ROOT)),
        "critic_root": str(args.critic_root),
        "requests": len(requests),
        "start": args.start,
        "terra_model": config.model_for_role("terra"),
        "max_concurrency": config.max_concurrency,
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
        description="Adjudicate fraud critic reports into minimal candidate patches."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--request-id",
        action="append",
        help="Exact request ID to patch; repeat for a non-contiguous selection.",
    )
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--terra-max-tokens", type=int, default=32_000)
    parser.add_argument("--critic-root", type=Path, default=DEFAULT_CRITIC_ROOT)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    request_count = len(load_jsonl(REQUESTS))
    known_request_ids = {
        request["request_id"] for request in load_jsonl(REQUESTS)
    }
    if args.request_id:
        unknown = sorted(set(args.request_id) - known_request_ids)
        if unknown:
            parser.error(f"unknown --request-id values: {unknown}")
        if len(args.request_id) != len(set(args.request_id)):
            parser.error("--request-id values must be unique")
    if not 1 <= args.start <= request_count:
        parser.error(f"--start must be between 1 and {request_count}")
    if not 1 <= args.limit <= request_count - args.start + 1:
        parser.error("--limit exceeds the available request window")
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    requests = selected_requests(args)
    if not args.execute:
        summary = {
            "mode": "dry_run",
            "requests": [request["request_id"] for request in requests],
            "planned_api_calls": len(requests),
            "max_concurrency": args.concurrency,
            "terra_max_completion_tokens": args.terra_max_tokens,
            "critic_root": str(args.critic_root),
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
