#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.benchmarks.external_data import KBL_CAUSATION_REF, definitions_fingerprint
from idpr.v2.closure import compile_candidate_offenses, compile_closure
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.routing import (
    normalize_router_seeds,
    router_catalog,
    router_catalog_fingerprint,
    router_request_payload,
    router_schema,
    validate_router_output,
)
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    predicate_definitions,
    validate_call2_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    output = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        output.append(value)
    return output


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _verify_manifest(
    manifest: dict[str, Any],
    *,
    benchmark: str,
    input_dir: Path,
    definitions_dir: Path,
    prompt_names: tuple[str, ...],
) -> None:
    if manifest.get("benchmark") != benchmark:
        raise ValueError(
            f"manifest benchmark mismatch: {manifest.get('benchmark')!r} != {benchmark!r}"
        )
    expected_definitions = manifest.get("definitions_fingerprint")
    actual_definitions = definitions_fingerprint(definitions_dir)
    if expected_definitions != actual_definitions:
        raise ValueError("definition registry drifted after external benchmark preparation")
    for name in prompt_names:
        expected = (manifest.get("prompts") or {}).get(name)
        actual = _file_hash(prompt_path(name))
        if expected != actual:
            raise ValueError(f"prompt drifted after external benchmark preparation: {name}")
    artifacts = manifest.get("artifacts") or {}
    for key, filename in (("gold", "gold.jsonl"), ("model_inputs", "model_inputs.jsonl")):
        expected = (artifacts.get(key) or {}).get("sha256")
        actual = _file_hash(input_dir / filename)
        if expected != actual:
            raise ValueError(f"materialized artifact drifted: {filename}")


def _target_from_dict(value: Any) -> AssessmentTarget:
    if not isinstance(value, dict):
        raise ValueError("target must be an object")
    key = value.get("instance_key")
    if not isinstance(key, dict):
        raise ValueError("target.instance_key must be an object")
    target = AssessmentTarget(
        OffenseInstanceKey(
            str(key.get("case_id", "")),
            str(key.get("actor_id", "")),
            str(key.get("offense_ref", "")),
            str(key.get("occurrence_id", "")),
        ),
        str(value.get("predicate_ref", "")),
    )
    if not all(
        (
            target.instance_key.case_id,
            target.instance_key.actor_id,
            target.instance_key.offense_ref,
            target.instance_key.occurrence_id,
            target.predicate_ref,
        )
    ):
        raise ValueError("target fields must be non-empty")
    return target


def _occurrence_from_payload(payload: dict[str, Any]) -> GoldOccurrence:
    value = payload.get("evidence_occurrence")
    if not isinstance(value, dict):
        raise ValueError("payload.evidence_occurrence must be an object")
    span = value.get("source_span")
    if not isinstance(span, dict):
        raise ValueError("evidence occurrence lacks source_span")
    return GoldOccurrence(
        str(value.get("occurrence_id", "")),
        str(value.get("actor_id", "")),
        str(value.get("source_text", "")),
        int(span.get("start")),
        int(span.get("end")),
    )


def _run_lbox(
    *,
    input_dir: Path,
    out: Path,
    definitions_dir: Path,
    client: VLLMClient,
    max_tokens: int,
    temperature: float,
) -> dict[str, Any]:
    manifest = _read_json(input_dir / "manifest.json")
    prompt_names = ("v2_call1_router", "v2_call1_router_user")
    _verify_manifest(
        manifest,
        benchmark="lbox_call1",
        input_dir=input_dir,
        definitions_dir=definitions_dir,
        prompt_names=prompt_names,
    )
    registry = load_definitions(definitions_dir)
    catalog = router_catalog(registry)
    expected_catalog = (manifest.get("coverage") or {}).get("router_catalog_fingerprint")
    if router_catalog_fingerprint(catalog) != expected_catalog:
        raise ValueError("Call 1 router catalog drifted after benchmark preparation")
    schema = router_schema(catalog)
    system_prompt, user_prompt = (load_prompt(name) for name in prompt_names)
    rows = _read_jsonl(input_dir / "model_inputs.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    succeeded = failed = 0
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    with out.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, start=1):
            case_id = str(row.get("id", ""))
            payload = row.get("payload")
            if not isinstance(payload, dict):
                raise ValueError(f"{case_id}: payload must be an object")
            rebuilt = router_request_payload(
                question_prompt=str(payload.get("question_prompt", "")),
                case_text=str(payload.get("case_text", "")),
                catalog=catalog,
            )
            if payload != rebuilt:
                raise ValueError(f"{case_id}: materialized Call 1 payload no longer reproduces")
            assert_no_leaked_fields(payload)
            output_row: dict[str, Any] = {"id": case_id}
            try:
                raw, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_call1_router",
                    schema=schema,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    user_template=user_prompt,
                )
                raw_seeds = validate_router_output(raw, catalog=catalog)
                normalized = normalize_router_seeds(raw_seeds)
                closure = compile_closure(registry, normalized.normalized_seeds)
                compiled = dict(compile_candidate_offenses(registry, closure))
                usage = metadata.get("usage", {})
                for key in usage_total:
                    usage_total[key] += int(usage.get(key, 0) or 0)
                output_row.update(
                    {
                        "raw_response": raw,
                        "raw_seeds": list(normalized.raw_seeds),
                        "seeds": list(normalized.normalized_seeds),
                        "duplicate_refs": list(normalized.duplicate_refs),
                        "candidate_offense_refs": sorted(closure.candidate_offense_refs),
                        "compiled_candidate_refs": sorted(compiled),
                        "usage": usage,
                    }
                )
                succeeded += 1
            except Exception as error:
                output_row["error"] = f"{type(error).__name__}: {error}"
                failed += 1
            handle.write(json.dumps(output_row, ensure_ascii=False) + "\n")
            handle.flush()
            status = "ok" if "error" not in output_row else "FAIL"
            print(f"[{index}/{len(rows)}] {case_id} {status}")
    return {
        "benchmark": "lbox_call1",
        "cases": len(rows),
        "succeeded": succeeded,
        "failed": failed,
        "usage": usage_total,
    }


def _run_kbl(
    *,
    input_dir: Path,
    out: Path,
    definitions_dir: Path,
    client: VLLMClient,
    max_tokens: int,
    temperature: float,
    binary: bool = False,
) -> dict[str, Any]:
    manifest = _read_json(input_dir / "manifest.json")
    prompt_names = (
        "v2_call2_grounding_binary" if binary else "v2_call2_grounding",
        "v2_call2_grounding_binary_user" if binary else "v2_call2_grounding_user",
    )
    _verify_manifest(
        manifest,
        benchmark="kbl_call2",
        input_dir=input_dir,
        definitions_dir=definitions_dir,
        prompt_names=prompt_names,
    )
    registry = load_definitions(definitions_dir)
    if registry.kind_of(KBL_CAUSATION_REF) != "legal_element":
        raise ValueError(f"missing production predicate: {KBL_CAUSATION_REF}")
    predicates = predicate_definitions(registry, (KBL_CAUSATION_REF,))
    system_prompt, user_prompt = (load_prompt(name) for name in prompt_names)
    rows = _read_jsonl(input_dir / "model_inputs.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    succeeded = failed = 0
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    with out.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, start=1):
            case_id = str(row.get("id", ""))
            payload = row.get("payload")
            if not isinstance(payload, dict):
                raise ValueError(f"{case_id}: payload must be an object")
            target = _target_from_dict(row.get("target"))
            if target.predicate_ref != KBL_CAUSATION_REF:
                raise ValueError(f"{case_id}: KBL target is not result_causation")
            occurrence = _occurrence_from_payload(payload)
            rebuilt = call2_request_payload(
                evidence_occurrence=occurrence,
                predicates=predicates,
                targets=(target,),
            )
            if payload != rebuilt:
                raise ValueError(f"{case_id}: materialized Call 2 payload no longer reproduces")
            assert_no_leaked_fields(payload)
            output_row: dict[str, Any] = {"id": case_id}
            try:
                raw, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_external_kbl_result_causation",
                    schema=call2_schema((target,), binary=binary),
                    max_tokens=max_tokens,
                    temperature=temperature,
                    user_template=user_prompt,
                )
                assessment = validate_call2_output(raw, targets=(target,), binary=binary)[0]
                usage = metadata.get("usage", {})
                for key in usage_total:
                    usage_total[key] += int(usage.get(key, 0) or 0)
                output_row.update(
                    {"label": assessment.truth, "raw_response": raw, "usage": usage}
                )
                succeeded += 1
            except Exception as error:
                output_row["error"] = f"{type(error).__name__}: {error}"
                failed += 1
            handle.write(json.dumps(output_row, ensure_ascii=False) + "\n")
            handle.flush()
            status = "ok" if "error" not in output_row else "FAIL"
            print(f"[{index}/{len(rows)}] {case_id} {status}")
    return {
        "benchmark": "kbl_call2",
        "cases": len(rows),
        "succeeded": succeeded,
        "failed": failed,
        "usage": usage_total,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=("lbox_call1", "kbl_call2"), required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--prompt-approved", action="store_true")
    parser.add_argument("--binary-mode", action="store_true",
                        help="Restrict output to TRUE/FALSE only (no UNKNOWN)")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before external model execution")

    client = VLLMClient(args.base_url, args.model, args.api_key)
    if args.benchmark == "lbox_call1":
        summary = _run_lbox(
            input_dir=args.input_dir,
            out=args.out,
            definitions_dir=args.definitions_dir,
            client=client,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
    else:
        summary = _run_kbl(
            input_dir=args.input_dir,
            out=args.out,
            definitions_dir=args.definitions_dir,
            client=client,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            binary=args.binary_mode,
        )
    run_manifest = {
        **summary,
        "git_commit": _git_commit(),
        "model": args.model,
        "base_url": args.base_url,
        "sampling": {"temperature": args.temperature, "max_tokens": args.max_tokens},
        "input_manifest_sha256": _file_hash(args.input_dir / "manifest.json"),
        "predictions_sha256": _file_hash(args.out),
        "binary_mode": args.binary_mode,
    }
    manifest_path = args.out.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(run_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(f"wrote {manifest_path}")
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
