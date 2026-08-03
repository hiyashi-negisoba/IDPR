#!/usr/bin/env python3
"""Run the sealed Phase-3 KCL pointwise LLM-as-a-judge evaluation."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import shutil
import subprocess
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from dotenv import load_dotenv
from jsonschema import Draft202012Validator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.eval.phase3_judge import (  # noqa: E402
    JudgeContractError,
    aggregate_records,
    canonical_sha256,
    index_unique,
    load_method_answers,
    paired_bootstrap_deltas,
    read_json,
    read_jsonl,
    reduce_judge_output,
    sha256_file,
)
from idpr.eval.rubric import load_rubric_sets  # noqa: E402
from idpr.llm import GatewayConfig, JSONCompletionJob  # noqa: E402
from idpr.llm.gemini_native import GeminiNativeGateway  # noqa: E402


GEMINI_SAFETY_CATEGORIES = (
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
)


def _gemini_safety_settings(threshold: str) -> list[dict[str, str]]:
    return [
        {"category": category, "threshold": threshold}
        for category in GEMINI_SAFETY_CATEGORIES
    ]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _write_jsonl(path: Path, records: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )
    temporary.replace(path)


def _git_revision() -> str:
    pinned_revision = os.environ.get("IDPR_TESTED_CODE_COMMIT", "").strip()
    if pinned_revision:
        return pinned_revision
    if shutil.which("git") is None:
        raise JudgeContractError(
            "IDPR_TESTED_CODE_COMMIT is required when git is unavailable"
        )
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _result_key(record: Mapping[str, Any]) -> tuple[str, str]:
    return str(record["method_id"]), str(record["sub_question_id"])


def _load_existing(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    if not path.is_file():
        return {}
    records: dict[tuple[str, str], dict[str, Any]] = {}
    for record in read_jsonl(path):
        records[_result_key(record)] = record
    return records


def _contract_errors(validator: Draft202012Validator, output: Any) -> list[str]:
    return [
        error.message
        for error in sorted(validator.iter_errors(output), key=lambda item: list(item.path))
    ]


async def _score_one(
    *,
    gateway: GeminiNativeGateway,
    validator: Draft202012Validator,
    system_prompt: str,
    protocol: Mapping[str, Any],
    method_id: str,
    case_id: str,
    question: str,
    rubrics: Sequence[str],
    rubric_set: Any,
    answer: str,
    max_tokens: int,
    temperature: float,
    reasoning_effort: str | None,
    contract_attempts: int,
) -> dict[str, Any]:
    answer_sha256 = canonical_sha256(answer)
    anonymous_id = canonical_sha256(
        {"case": case_id, "answer_sha256": answer_sha256}
    )[:20]
    feedback: list[str] = []
    previous_invalid_output: Mapping[str, Any] | None = None
    api_attempts: list[dict[str, Any]] = []
    api_failures: list[dict[str, Any]] = []
    question_variant = "full_question"
    for attempt in range(1, contract_attempts + 1):
        active_prompt = system_prompt
        if feedback:
            active_prompt += (
                "\n\n# 직전 출력의 계약 오류\n이 요청은 새 채점이 아니라 입력의 "
                "`previous_invalid_output`을 수리하는 요청이다. 다음 오류만 교정하여 전체 "
                "JSON을 다시 출력하고 나머지 판단은 유지하라. `answer_quote`와 "
                "`answer_quotes`는 반드시 입력 `answer`에 존재하는 연속 문자열을 그대로 "
                "복사하라.\n- "
                + "\n- ".join(feedback)
            )
        payload: dict[str, Any] = {
            "question": question,
            "rubrics": [
                {"index": index, "text": rubric}
                for index, rubric in enumerate(rubrics, 1)
            ],
            "answer": answer,
        }
        if previous_invalid_output is not None:
            payload["previous_invalid_output"] = previous_invalid_output
            payload["contract_errors"] = feedback
        job = JSONCompletionJob(
            request_id=f"judge_{anonymous_id}_a{attempt}",
            role="terra",
            system_prompt=active_prompt,
            payload=payload,
            max_tokens=max_tokens,
            temperature=temperature,
            reasoning_effort=reasoning_effort,
        )
        try:
            result = await gateway.complete_json(job)
            api_attempts.append(result.manifest_record())
            schema_errors = _contract_errors(validator, result.output)
            if schema_errors:
                feedback = schema_errors[:20]
                previous_invalid_output = result.output
                gateway.discard_cache(result)
                continue
            try:
                metrics = reduce_judge_output(
                    output=result.output,
                    answer=answer,
                    rubric_set=rubric_set,
                    protocol=protocol,
                )
            except JudgeContractError as error:
                feedback = [str(error)]
                previous_invalid_output = result.output
                gateway.discard_cache(result)
                continue
            return {
                "version": "1.0.0",
                "status": "ok",
                "transport": gateway.transport,
                "sub_question_id": case_id,
                "method_id": method_id,
                "anonymous_answer_id": anonymous_id,
                "answer_sha256": answer_sha256,
                "question_variant": question_variant,
                "judge_output": result.output,
                "metrics": metrics,
                "api_attempts": api_attempts,
                "api_failures": api_failures,
                "completed_at": _utc_now(),
            }
        except Exception as error:  # API errors are retained; no case is silently dropped.
            message = f"{type(error).__name__}: {error}"
            api_failures.append(
                {"attempt": attempt, "question_variant": question_variant, "error": message}
            )
            # Provider failures retry the same original or contract-repair request.
    return {
        "version": "1.0.0",
        "status": "failed",
        "transport": gateway.transport,
        "sub_question_id": case_id,
        "method_id": method_id,
        "anonymous_answer_id": anonymous_id,
        "answer_sha256": answer_sha256,
        "question_variant": question_variant,
        "errors": feedback,
        "api_attempts": api_attempts,
        "api_failures": api_failures,
        "completed_at": _utc_now(),
    }


async def _run(args: argparse.Namespace) -> None:
    started_at = _utc_now()
    load_dotenv(args.env_file)
    protocol = read_json(args.protocol)
    schema = read_json(args.schema)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    prompt_text = args.prompt.read_text(encoding="utf-8")
    safety_prompt_text = args.safety_prompt.read_text(encoding="utf-8")
    system_prompt = (
        prompt_text
        + "\n\n# 강제 JSON Schema\n"
        + json.dumps(schema, ensure_ascii=False, sort_keys=True)
        + "\n\n"
        + safety_prompt_text
    )

    sealed_rows = read_jsonl(args.sealed_inventory)
    sealed_index = index_unique(
        sealed_rows, key="sub_question_id", source=str(args.sealed_inventory)
    )
    sealed_case_ids = list(sealed_index)
    if len(sealed_case_ids) != args.expected_cases:
        raise JudgeContractError(
            f"expected {args.expected_cases} sealed cases, got {len(sealed_case_ids)}"
        )
    rubric_sets = load_rubric_sets(args.rubric_inventory, parquet_path=args.parquet)
    missing_rubrics = sorted(set(sealed_case_ids) - set(rubric_sets))
    if missing_rubrics:
        raise JudgeContractError(f"sealed cases missing full rubrics: {missing_rubrics}")

    answers, method_paths = load_method_answers(
        project_root=PROJECT_ROOT,
        methods_manifest_path=args.methods_manifest,
        expected_case_ids=sealed_case_ids,
        selected_methods=args.method_id,
    )
    selected_case_ids = list(args.case_id) if args.case_id else sealed_case_ids
    unknown_cases = sorted(set(selected_case_ids) - set(sealed_case_ids))
    if unknown_cases:
        raise JudgeContractError(f"unknown sealed cases: {unknown_cases}")
    unknown_exclusions = sorted(set(args.exclude_case_id) - set(sealed_case_ids))
    if unknown_exclusions:
        raise JudgeContractError(f"unknown excluded sealed cases: {unknown_exclusions}")
    excluded_case_ids = set(args.exclude_case_id)
    selected_case_ids = [
        case_id for case_id in selected_case_ids if case_id not in excluded_case_ids
    ]
    if not selected_case_ids:
        raise JudgeContractError("case selection is empty after exclusions")

    jobs = [
        (method_id, case_id)
        for method_id in answers
        for case_id in selected_case_ids
    ]
    random.Random(args.order_seed).shuffle(jobs)
    if args.limit:
        jobs = jobs[: args.limit]

    if args.overwrite:
        existing: dict[tuple[str, str], dict[str, Any]] = {}
    else:
        existing = _load_existing(args.out)
    pending = [
        job
        for job in jobs
        if not (
            existing.get(job, {}).get("status") == "ok"
            and existing.get(job, {}).get("transport")
            == GeminiNativeGateway.transport
        )
    ]

    base_config = GatewayConfig.from_env(require_models=False)
    config = replace(
        base_config,
        terra_model=args.model,
        sol_model=args.model,
        cache_dir=args.cache_dir,
        max_concurrency=args.concurrency,
        timeout_seconds=args.timeout_seconds,
        max_retries=args.api_retries,
        use_json_response_format=True,
    )
    safety_settings = _gemini_safety_settings(args.gemini_safety_threshold)
    gateway = GeminiNativeGateway(
        config,
        model=args.model,
        safety_settings=safety_settings,
        response_json_schema=schema,
    )

    print(
        json.dumps(
            {
                "model": args.model,
                "methods": list(answers),
                "sealed_cases": len(sealed_case_ids),
                "selected_jobs": len(jobs),
                "pending_jobs": len(pending),
                "concurrency": args.concurrency,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    for offset in range(0, len(pending), args.concurrency):
        batch = pending[offset : offset + args.concurrency]
        results = await asyncio.gather(
            *(
                _score_one(
                    gateway=gateway,
                    validator=validator,
                    system_prompt=system_prompt,
                    protocol=protocol,
                    method_id=method_id,
                    case_id=case_id,
                    question=rubric_sets[case_id].question,
                    rubrics=rubric_sets[case_id].rubrics,
                    rubric_set=rubric_sets[case_id],
                    answer=answers[method_id][case_id],
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    reasoning_effort=args.reasoning_effort,
                    contract_attempts=args.contract_attempts,
                )
                for method_id, case_id in batch
            )
        )
        for result in results:
            existing[_result_key(result)] = result
        ordered_records = [existing[key] for key in sorted(existing)]
        _write_jsonl(args.out, ordered_records)
        completed = sum(result["status"] == "ok" for result in results)
        print(
            f"[{min(offset + len(batch), len(pending))}/{len(pending)}] "
            f"batch_ok={completed} batch_failed={len(results) - completed}",
            flush=True,
        )

    records = [existing[key] for key in sorted(existing)]
    relevant_keys = set(jobs)
    selected_records = [record for record in records if _result_key(record) in relevant_keys]
    summary = aggregate_records(selected_records, expected_case_ids=selected_case_ids)
    complete = (
        len(selected_records) == len(jobs)
        and all(record.get("status") == "ok" for record in selected_records)
    )
    if complete and "idpr_nsn" in answers and len(answers) > 1:
        summary["paired_bootstrap"] = {
            "coverage": paired_bootstrap_deltas(
                selected_records,
                target_method="idpr_nsn",
                metric_path=("coverage", "rubric_score"),
                samples=args.bootstrap_samples,
                seed=args.bootstrap_seed,
            ),
            "precision": paired_bootstrap_deltas(
                selected_records,
                target_method="idpr_nsn",
                metric_path=("precision", "score"),
                samples=args.bootstrap_samples,
                seed=args.bootstrap_seed,
            ),
            "hallucination": paired_bootstrap_deltas(
                selected_records,
                target_method="idpr_nsn",
                metric_path=("hallucination", "score"),
                samples=args.bootstrap_samples,
                seed=args.bootstrap_seed,
            ),
            "consistency": paired_bootstrap_deltas(
                selected_records,
                target_method="idpr_nsn",
                metric_path=("consistency", "normalized_score"),
                samples=args.bootstrap_samples,
                seed=args.bootstrap_seed,
            ),
        }
    _write_json(args.summary, summary)

    source_hashes = {
        "rubric_inventory": sha256_file(args.rubric_inventory),
        "sealed_inventory": sha256_file(args.sealed_inventory),
        "methods_manifest": sha256_file(args.methods_manifest),
        "protocol": sha256_file(args.protocol),
        "schema": sha256_file(args.schema),
        "prompt": sha256_file(args.prompt),
        "safety_prompt": sha256_file(args.safety_prompt),
        **{
            f"method:{method_id}": sha256_file(path)
            for method_id, path in method_paths.items()
        },
    }
    manifest = {
        "version": "1.0.0",
        "status": "complete" if complete else "partial",
        "started_at": started_at,
        "completed_at": _utc_now(),
        "git_revision": _git_revision(),
        "requested_backbone_model": args.model,
        "gateway_model": args.model,
        "transport": gateway.transport,
        "methods": list(answers),
        "sealed_cases": len(sealed_case_ids),
        "excluded_case_ids": sorted(excluded_case_ids),
        "selected_jobs": len(jobs),
        "completed_jobs": sum(record.get("status") == "ok" for record in selected_records),
        "failed_jobs": sum(record.get("status") != "ok" for record in selected_records),
        "order_seed": args.order_seed,
        "temperature": args.temperature,
        "reasoning_effort": args.reasoning_effort,
        "max_tokens": args.max_tokens,
        "contract_attempts": args.contract_attempts,
        "api_retries": args.api_retries,
        "gemini_safety_settings": safety_settings,
        "source_sha256": source_hashes,
        "output_sha256": sha256_file(args.out),
        "summary_sha256": sha256_file(args.summary),
    }
    _write_json(args.manifest, manifest)
    print(f"status={manifest['status']} output={args.out} summary={args.summary}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--rubric-inventory",
        type=Path,
        default=PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--sealed-inventory",
        type=Path,
        default=PROJECT_ROOT / "experiments/results/phase3_final_59/final_59_inventory.jsonl",
    )
    parser.add_argument("--parquet", type=Path)
    parser.add_argument(
        "--methods-manifest",
        type=Path,
        default=PROJECT_ROOT / "data/eval/phase3_method_outputs.json",
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=PROJECT_ROOT / "data/eval/phase3_judge_protocol.json",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=PROJECT_ROOT / "docs/contracts/phase3_llm_judge.schema.json",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=PROJECT_ROOT / "prompts/phase3_kcl_pointwise_judge.md",
    )
    parser.add_argument(
        "--safety-prompt",
        type=Path,
        default=PROJECT_ROOT / "prompts/phase3_kcl_academic_safety.md",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "experiments/results/phase3_judge/judgments.jsonl",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=PROJECT_ROOT / "experiments/results/phase3_judge/summary.json",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=PROJECT_ROOT / "experiments/results/phase3_judge/manifest.json",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=PROJECT_ROOT / ".cache/phase3_judge",
    )
    parser.add_argument("--method-id", action="append", default=[])
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--exclude-case-id", action="append", default=[])
    parser.add_argument("--expected-cases", type=int, default=59)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=float, default=600.0)
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "minimal", "low", "medium", "high", "xhigh"),
    )
    parser.add_argument("--contract-attempts", type=int, default=2)
    parser.add_argument("--api-retries", type=int, default=2)
    parser.add_argument(
        "--gemini-safety-threshold",
        choices=("BLOCK_NONE", "OFF"),
        default="BLOCK_NONE",
    )
    parser.add_argument("--order-seed", type=int, default=20260803)
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=20260803)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    for name in ("expected_cases", "concurrency", "max_tokens", "contract_attempts"):
        if getattr(args, name) < 1:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.bootstrap_samples < 2:
        parser.error("--bootstrap-samples must be at least 2")
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
