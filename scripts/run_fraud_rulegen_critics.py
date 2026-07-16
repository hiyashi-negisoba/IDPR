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
from idpr.rulegen import validate_norm_candidate_batch  # noqa: E402

from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    CRITIC_PROMPT,
    CRITIC_SCHEMA,
    REQUESTS,
    SAFE_RUN_ID,
    load_jsonl,
    prompt_with_schema,
    select_requests,
    validate_sol_results,
    write_json,
)


MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_candidate_manifest.json"
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen_critics"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def load_candidate_paths() -> dict[str, Path]:
    manifest = read_json(MANIFEST)
    return {
        batch["request_id"]: PROJECT_ROOT / batch["path"]
        for batch in manifest["batches"]
    }


def selected_requests(args: argparse.Namespace) -> list[dict[str, Any]]:
    requests = load_jsonl(REQUESTS)
    if not args.request_id:
        return select_requests(requests, args.start, args.limit)
    by_id = {request["request_id"]: request for request in requests}
    return [by_id[request_id] for request_id in args.request_id]


def build_jobs(
    requests: list[dict[str, Any]],
    candidate_paths: dict[str, Path],
    max_tokens: int,
) -> list[JSONCompletionJob]:
    prompt = prompt_with_schema(CRITIC_PROMPT, CRITIC_SCHEMA)
    jobs: list[JSONCompletionJob] = []
    for request in requests:
        request_id = request["request_id"]
        target = read_json(candidate_paths[request_id])
        validate_norm_candidate_batch(target, request)
        jobs.append(
            JSONCompletionJob(
                request_id=f"{request_id}.critic",
                role="sol",
                system_prompt=prompt,
                payload={
                    "stage": "norm_candidate_batch",
                    "target_id": request_id,
                    "target": target,
                    "bounded_source_material": request,
                },
                max_tokens=max_tokens,
                reasoning_effort="low",
            )
        )
    return jobs


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    requests = selected_requests(args)
    requests_by_id = {request["request_id"]: request for request in requests}
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    results = await gateway.complete_many(
        build_jobs(requests, load_candidate_paths(), args.sol_max_tokens)
    )
    write_usage_manifest(run_dir / "sol_usage.jsonl", results)
    validation = validate_sol_results(
        gateway, results, requests_by_id, run_dir
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
        "requests": len(requests),
        "start": args.start,
        "sol_model": config.model_for_role("sol"),
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
        description="Critique tracked fraud NormCandidateBatch artifacts with Sol."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--request-id",
        action="append",
        help="Exact request ID to review; repeat for a non-contiguous selection.",
    )
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--sol-max-tokens", type=int, default=25_000)
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
            "sol_max_completion_tokens": args.sol_max_tokens,
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
