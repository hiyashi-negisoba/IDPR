from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.llm import (  # noqa: E402
    GatewayConfig,
    JSONCompletionJob,
    JSONCompletionResult,
    LLMGateway,
    ReasoningEffort,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    NormCandidateValidationError,
    RulegenCritiqueValidationError,
    repair_ocr_interrupted_candidate_quotes,
    validate_norm_candidate_batch,
    validate_rulegen_critique,
)


REQUESTS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
EXTRACT_PROMPT = PROJECT_ROOT / "prompts/rulegen_extract_norm_candidates.md"
EXTRACT_FEWSHOT = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_norm_candidate_fewshot_gold.json"
)
CRITIC_PROMPT = PROJECT_ROOT / "prompts/rulegen_critic.md"
NORM_CANDIDATE_SCHEMA = (
    PROJECT_ROOT / "docs/contracts/norm_candidate_batch.schema.json"
)
CRITIC_SCHEMA = PROJECT_ROOT / "docs/contracts/rulegen_critique_report.schema.json"
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen"
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9_.-]+$")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def select_requests(
    requests: list[dict[str, Any]], start: int, limit: int
) -> list[dict[str, Any]]:
    """Select a 1-based contiguous request window for resumable runs."""

    return requests[start - 1 : start - 1 + limit]


def build_extraction_jobs(
    requests: list[dict[str, Any]],
    max_tokens: int,
    use_fewshot: bool = True,
    reasoning_effort: "ReasoningEffort | None" = None,
) -> list[JSONCompletionJob]:
    prompt = prompt_with_schema(EXTRACT_PROMPT, NORM_CANDIDATE_SCHEMA)
    if use_fewshot:
        prompt += (
            "\nGold structural example:\n"
            "Learn only its source-to-structure transformation. Never copy its fraud "
            "doctrine, candidate IDs, source IDs, output count, or conclusions into "
            "another target. The current request remains the only legal source.\n"
            "```json\n"
            + EXTRACT_FEWSHOT.read_text(encoding="utf-8").rstrip()
            + "\n```\n"
        )
    return [
        JSONCompletionJob(
            request_id=request["request_id"],
            role="terra",
            system_prompt=prompt,
            payload=request,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
        )
        for request in requests
    ]


def build_critic_jobs(
    requests_by_id: dict[str, dict[str, Any]],
    terra_results: list[JSONCompletionResult],
    max_tokens: int,
) -> list[JSONCompletionJob]:
    prompt = prompt_with_schema(CRITIC_PROMPT, CRITIC_SCHEMA)
    jobs: list[JSONCompletionJob] = []
    for result in terra_results:
        request = requests_by_id[result.request_id]
        jobs.append(
            JSONCompletionJob(
                request_id=f"{result.request_id}.critic",
                role="sol",
                system_prompt=prompt,
                payload={
                    "stage": "norm_candidate_batch",
                    "target_id": result.request_id,
                    "target": result.output,
                    "bounded_source_material": request,
                },
                max_tokens=max_tokens,
                reasoning_effort="low",
            )
        )
    return jobs


def prompt_with_schema(prompt_path: Path, schema_path: Path) -> str:
    prompt = prompt_path.read_text(encoding="utf-8").rstrip()
    schema = schema_path.read_text(encoding="utf-8").rstrip()
    return f"{prompt}\n\nExact output JSON Schema:\n```json\n{schema}\n```\n"


def request_commentary(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["comment_id"]: row for row in request.get("commentary_chunks", [])
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_terra_results(
    gateway: LLMGateway,
    results: list[JSONCompletionResult],
    requests_by_id: dict[str, dict[str, Any]],
    run_dir: Path,
) -> tuple[list[JSONCompletionResult], list[dict[str, Any]]]:
    valid: list[JSONCompletionResult] = []
    records: list[dict[str, Any]] = []
    for result in results:
        repaired_output, provenance_repairs = (
            repair_ocr_interrupted_candidate_quotes(
                result.output,
                request_commentary(requests_by_id[result.request_id]),
            )
        )
        validated_result = replace(result, output=repaired_output)
        output_path = run_dir / "terra" / f"{result.request_id}.json"
        if provenance_repairs:
            raw_output_path = (
                run_dir / "terra_raw" / f"{result.request_id}.json"
            )
            write_json(raw_output_path, result.output)
        else:
            raw_output_path = None
        write_json(output_path, repaired_output)
        try:
            validate_norm_candidate_batch(
                repaired_output, requests_by_id[result.request_id]
            )
        except NormCandidateValidationError as exc:
            gateway.discard_cache(result)
            records.append(
                {
                    "request_id": result.request_id,
                    "stage": "norm_candidate_batch",
                    "valid": False,
                    "errors": exc.errors,
                    "provenance_repairs": provenance_repairs,
                    "raw_output_path": (
                        str(raw_output_path.relative_to(PROJECT_ROOT))
                        if raw_output_path
                        else None
                    ),
                    "output_path": str(output_path.relative_to(PROJECT_ROOT)),
                }
            )
        else:
            valid.append(validated_result)
            records.append(
                {
                    "request_id": result.request_id,
                    "stage": "norm_candidate_batch",
                    "valid": True,
                    "errors": [],
                    "candidates": len(repaired_output["candidates"]),
                    "provenance_repairs": provenance_repairs,
                    "raw_output_path": (
                        str(raw_output_path.relative_to(PROJECT_ROOT))
                        if raw_output_path
                        else None
                    ),
                    "output_path": str(output_path.relative_to(PROJECT_ROOT)),
                }
            )
    return valid, records


def validate_sol_results(
    gateway: LLMGateway,
    results: list[JSONCompletionResult],
    requests_by_id: dict[str, dict[str, Any]],
    run_dir: Path,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for result in results:
        target_id = result.request_id.removesuffix(".critic")
        request = requests_by_id[target_id]
        commentary = request_commentary(request)
        output_path = run_dir / "sol" / f"{result.request_id}.json"
        write_json(output_path, result.output)
        try:
            validate_rulegen_critique(
                result.output,
                expected_stage="norm_candidate_batch",
                expected_target_id=target_id,
                commentary_by_id=commentary,
                allowed_comment_ids=set(commentary),
            )
        except RulegenCritiqueValidationError as exc:
            gateway.discard_cache(result)
            records.append(
                {
                    "request_id": result.request_id,
                    "stage": "critic",
                    "valid": False,
                    "errors": exc.errors,
                    "output_path": str(output_path.relative_to(PROJECT_ROOT)),
                }
            )
        else:
            records.append(
                {
                    "request_id": result.request_id,
                    "stage": "critic",
                    "valid": True,
                    "errors": [],
                    "verdict": result.output["verdict"],
                    "findings": len(result.output["findings"]),
                    "output_path": str(output_path.relative_to(PROJECT_ROOT)),
                }
            )
    return records


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    requests = select_requests(load_jsonl(args.requests), args.start, args.limit)
    requests_by_id = {request["request_id"]: request for request in requests}
    run_dir = args.run_root / args.run_id
    gateway = LLMGateway(config)

    terra_results = await gateway.complete_many(
        build_extraction_jobs(
            requests,
            args.terra_max_tokens,
            use_fewshot=not args.no_fewshot,
            reasoning_effort=args.terra_reasoning_effort,
        )
    )
    write_usage_manifest(run_dir / "terra_usage.jsonl", terra_results)
    valid_terra, validation_records = validate_terra_results(
        gateway, terra_results, requests_by_id, run_dir
    )

    sol_results: list[JSONCompletionResult] = []
    if args.with_critic and valid_terra:
        sol_results = await gateway.complete_many(
            build_critic_jobs(requests_by_id, valid_terra, args.sol_max_tokens)
        )
        write_usage_manifest(run_dir / "sol_usage.jsonl", sol_results)
        validation_records.extend(
            validate_sol_results(gateway, sol_results, requests_by_id, run_dir)
        )

    all_results = [*terra_results, *sol_results]
    total_usage = {
        key: sum(
            result.usage.get(key, 0) for result in all_results if not result.cached
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
        "with_critic": args.with_critic,
        "fewshot": not args.no_fewshot,
        "terra_model": config.model_for_role("terra"),
        "sol_model": config.model_for_role("sol") if args.with_critic else None,
        "max_concurrency": config.max_concurrency,
        "api_calls": sum(not result.cached for result in all_results),
        "cache_hits": sum(result.cached for result in all_results),
        "usage": total_usage,
        "validation": validation_records,
        "all_valid": all(record["valid"] for record in validation_records),
    }
    write_json(run_dir / "run.json", summary)
    return summary


def dry_run_summary(args: argparse.Namespace) -> dict[str, Any]:
    requests = select_requests(load_jsonl(args.requests), args.start, args.limit)
    return {
        "mode": "dry_run",
        "requests": [request["request_id"] for request in requests],
        "start": args.start,
        "commentary_chars": sum(request["batch"]["n_chars"] for request in requests),
        "planned_api_calls": len(requests) * (2 if args.with_critic else 1),
        "with_critic": args.with_critic,
        "fewshot": not args.no_fewshot,
        "terra_model": _env_or_missing("IDPR_TERRA_MODEL"),
        "sol_model": _env_or_missing("IDPR_SOL_MODEL") if args.with_critic else None,
        "api_key": "set" if _env_or_missing("SKIML_API_KEY") != "MISSING" else "MISSING",
        "api_base": _env_or_missing("SKIML_API_BASE", default=GatewayConfig.from_env(
            require_api_key=False, require_models=False
        ).api_base),
        "max_concurrency": args.concurrency,
        "terra_max_completion_tokens": args.terra_max_tokens,
        "sol_max_completion_tokens": args.sol_max_tokens if args.with_critic else None,
        "sol_reasoning_effort": "low" if args.with_critic else None,
    }


def _env_or_missing(name: str, *, default: str | None = None) -> str:
    import os

    value = os.environ.get(name, "").strip()
    return value or default or "MISSING"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded Terra extraction and optional Sol critic pilot."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--with-critic", action="store_true")
    parser.add_argument("--no-fewshot", action="store_true")
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="1-based index of the first request to run.",
    )
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--terra-max-tokens", type=int, default=6_000)
    parser.add_argument(
        "--terra-reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        default=None,
        help="추론 terra(gpt-5.6) 대비. 미설정 시 모델 기본(6k 한도를 reasoning이 전부 소진).",
    )
    parser.add_argument("--sol-max-tokens", type=int, default=25_000)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--requests",
        type=Path,
        default=REQUESTS,
        help="rulegen requests JSONL (죄명별). 기본은 사기.",
    )
    parser.add_argument(
        "--run-root",
        type=Path,
        default=RUN_ROOT,
        help="run 산출 루트. 죄명별로 분리 권장.",
    )
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    # run_dir 산출물은 PROJECT_ROOT 기준 relative_to로 로깅되므로 절대경로로 고정한다.
    args.run_root = args.run_root.resolve()
    args.requests = args.requests.resolve()
    request_count = len(load_jsonl(args.requests))
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
    if not args.execute:
        print(json.dumps(dry_run_summary(args), ensure_ascii=False, indent=2))
        return

    config = GatewayConfig.from_env(require_api_key=True, require_models=False)
    config.model_for_role("terra")
    if args.with_critic:
        config.model_for_role("sol")
    config = replace(config, max_concurrency=args.concurrency)
    summary = asyncio.run(execute(args, config))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["all_valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
