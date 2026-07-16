from __future__ import annotations

import argparse
import asyncio
import copy
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
    JSONCompletionResult,
    LLMGateway,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    NormCandidateValidationError,
    RulegenCritiqueValidationError,
    repair_ocr_interrupted_candidate_quotes,
    validate_norm_candidate_batch,
    validate_rulegen_critique,
)
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    CRITIC_PROMPT,
    CRITIC_SCHEMA,
    NORM_CANDIDATE_SCHEMA,
    REQUESTS,
    SAFE_RUN_ID,
    load_jsonl,
    prompt_with_schema,
    request_commentary,
    write_json,
)


REVISION_PROMPT = PROJECT_ROOT / "prompts/rulegen_revise_norm_candidates.md"
DEFAULT_TARGET = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen/pilot_20260716_critic_scope/terra"
    / "fraud.article347.pass1.001.json"
)
DEFAULT_CRITIC = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen/pilot_20260716_critic_scope/sol"
    / "fraud.article347.pass1.001.critic.json"
)
DEFAULT_ADDENDUM = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_review_addendum.json"
)
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen_correction"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def build_revision_job(
    request: dict[str, Any],
    target: dict[str, Any],
    critique_reports: list[dict[str, Any]],
    max_tokens: int,
    revision_label: str = "revision1",
) -> JSONCompletionJob:
    request_id = request["request_id"]
    return JSONCompletionJob(
        request_id=f"{request_id}.{revision_label}",
        role="terra",
        system_prompt=prompt_with_schema(REVISION_PROMPT, NORM_CANDIDATE_SCHEMA),
        payload={
            "source_request": request,
            "target": target,
            "critique_reports": critique_reports,
        },
        max_tokens=max_tokens,
    )


def build_final_critic_job(
    request: dict[str, Any],
    revised_target: dict[str, Any],
    revision_id: str,
    max_tokens: int,
) -> JSONCompletionJob:
    return JSONCompletionJob(
        request_id=f"{revision_id}.critic",
        role="sol",
        system_prompt=prompt_with_schema(CRITIC_PROMPT, CRITIC_SCHEMA),
        payload={
            "stage": "norm_candidate_batch",
            "target_id": revision_id,
            "target": revised_target,
            "bounded_source_material": request,
        },
        max_tokens=max_tokens,
        reasoning_effort="low",
    )


def validate_input_critique(
    critique: dict[str, Any],
    request: dict[str, Any],
    *,
    expected_target_id: str,
) -> None:
    commentary = request_commentary(request)
    validate_rulegen_critique(
        critique,
        expected_stage="norm_candidate_batch",
        expected_target_id=expected_target_id,
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )


def validate_revision_target(
    target: dict[str, Any], request: dict[str, Any]
) -> None:
    """Validate legacy pilot targets without mutating the revision input."""

    validation_copy = copy.deepcopy(target)
    for candidate in validation_copy.get("candidates", []):
        candidate.setdefault(
            "polarity",
            "exception"
            if candidate.get("norm_kind") == "exception"
            else "positive",
        )
    validate_norm_candidate_batch(validation_copy, request)


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    requests = {row["request_id"]: row for row in load_jsonl(REQUESTS)}
    request = requests[args.request_id]
    target = read_json(args.target)
    critic = read_json(args.critic)
    critiques = [critic]
    if not args.no_review_addendum:
        critiques.append(read_json(args.review_addendum))

    validate_revision_target(target, request)
    validate_input_critique(
        critic,
        request,
        expected_target_id=args.critic_target_id or args.request_id,
    )
    if not args.no_review_addendum:
        validate_input_critique(
            critiques[1], request, expected_target_id=args.request_id
        )

    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    revision_job = build_revision_job(
        request,
        target,
        critiques,
        args.terra_max_tokens,
        args.revision_label,
    )
    if args.raw_revision is None:
        revision_result = await gateway.complete_json(revision_job)
        raw_revision = revision_result.output
        write_usage_manifest(
            run_dir / "terra_revision_usage.jsonl", [revision_result]
        )
    else:
        revision_result = None
        raw_revision = read_json(args.raw_revision)

    raw_revision_path = run_dir / "terra_revision_raw" / f"{args.request_id}.json"
    write_json(raw_revision_path, raw_revision)
    revised_output, provenance_repairs = repair_ocr_interrupted_candidate_quotes(
        raw_revision, request_commentary(request)
    )
    revision_path = run_dir / "terra_revision" / f"{args.request_id}.json"
    write_json(revision_path, revised_output)

    validation: list[dict[str, Any]] = []
    try:
        validate_norm_candidate_batch(revised_output, request)
    except NormCandidateValidationError as exc:
        if revision_result is not None:
            gateway.discard_cache(revision_result)
        validation.append(
            {
                "request_id": revision_job.request_id,
                "stage": "norm_candidate_revision",
                "valid": False,
                "errors": exc.errors,
                "provenance_repairs": provenance_repairs,
                "raw_output_path": str(
                    raw_revision_path.relative_to(PROJECT_ROOT)
                ),
                "output_path": str(revision_path.relative_to(PROJECT_ROOT)),
            }
        )
        final_results: list[JSONCompletionResult] = []
    else:
        validation.append(
            {
                "request_id": revision_job.request_id,
                "stage": "norm_candidate_revision",
                "valid": True,
                "errors": [],
                "candidates": len(revised_output["candidates"]),
                "provenance_repairs": provenance_repairs,
                "raw_output_path": str(
                    raw_revision_path.relative_to(PROJECT_ROOT)
                ),
                "output_path": str(revision_path.relative_to(PROJECT_ROOT)),
            }
        )
        critic_job = build_final_critic_job(
            request,
            revised_output,
            revision_job.request_id,
            args.sol_max_tokens,
        )
        critic_result = await gateway.complete_json(critic_job)
        final_results = [critic_result]
        write_usage_manifest(run_dir / "sol_critic_usage.jsonl", final_results)
        critic_path = run_dir / "sol" / f"{critic_job.request_id}.json"
        write_json(critic_path, critic_result.output)
        commentary = request_commentary(request)
        try:
            validate_rulegen_critique(
                critic_result.output,
                expected_stage="norm_candidate_batch",
                expected_target_id=revision_job.request_id,
                commentary_by_id=commentary,
                allowed_comment_ids=set(commentary),
            )
        except RulegenCritiqueValidationError as exc:
            gateway.discard_cache(critic_result)
            validation.append(
                {
                    "request_id": critic_job.request_id,
                    "stage": "critic",
                    "valid": False,
                    "errors": exc.errors,
                    "output_path": str(critic_path.relative_to(PROJECT_ROOT)),
                }
            )
        else:
            validation.append(
                {
                    "request_id": critic_job.request_id,
                    "stage": "critic",
                    "valid": True,
                    "errors": [],
                    "verdict": critic_result.output["verdict"],
                    "findings": len(critic_result.output["findings"]),
                    "output_path": str(critic_path.relative_to(PROJECT_ROOT)),
                }
            )

    all_results = [
        result for result in [revision_result, *final_results] if result is not None
    ]
    usage = {
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
        "request_id": args.request_id,
        "target_path": str(args.target),
        "critic_path": str(args.critic),
        "critic_target_id": args.critic_target_id or args.request_id,
        "review_addendum_path": (
            None if args.no_review_addendum else str(args.review_addendum)
        ),
        "raw_revision_path": str(args.raw_revision) if args.raw_revision else None,
        "terra_model": config.model_for_role("terra"),
        "sol_model": config.model_for_role("sol"),
        "api_calls": sum(not result.cached for result in all_results),
        "cache_hits": sum(result.cached for result in all_results),
        "usage": usage,
        "validation": validation,
        "all_valid": all(record["valid"] for record in validation),
    }
    write_json(run_dir / "run.json", summary)
    return summary


def dry_run_summary(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "mode": "dry_run",
        "request_id": args.request_id,
        "target_path": str(args.target),
        "critic_path": str(args.critic),
        "critic_target_id": args.critic_target_id or args.request_id,
        "review_addendum_path": (
            None if args.no_review_addendum else str(args.review_addendum)
        ),
        "raw_revision_path": str(args.raw_revision) if args.raw_revision else None,
        "planned_api_calls": 1 if args.raw_revision else 2,
        "terra_max_completion_tokens": args.terra_max_tokens,
        "sol_max_completion_tokens": args.sol_max_tokens,
        "max_concurrency": args.concurrency,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Revise one fraud NormCandidateBatch and run a final Sol critic."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--request-id", default="fraud.article347.pass1.001"
    )
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--critic", type=Path, default=DEFAULT_CRITIC)
    parser.add_argument(
        "--critic-target-id",
        help="Expected target_id of the supplied critic report.",
    )
    parser.add_argument(
        "--review-addendum", type=Path, default=DEFAULT_ADDENDUM
    )
    parser.add_argument("--no-review-addendum", action="store_true")
    parser.add_argument("--revision-label", default="revision1")
    parser.add_argument(
        "--raw-revision",
        type=Path,
        help="Reuse a saved raw Terra revision and run only local validation plus Sol.",
    )
    parser.add_argument("--terra-max-tokens", type=int, default=12_000)
    parser.add_argument("--sol-max-tokens", type=int, default=25_000)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    if not SAFE_RUN_ID.fullmatch(args.revision_label):
        parser.error("--revision-label contains unsafe characters")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    if not args.execute:
        print(json.dumps(dry_run_summary(args), ensure_ascii=False, indent=2))
        return

    config = GatewayConfig.from_env(require_api_key=True, require_models=True)
    config = replace(config, max_concurrency=args.concurrency)
    try:
        summary = asyncio.run(execute(args, config))
    except (NormCandidateValidationError, RulegenCritiqueValidationError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["all_valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
