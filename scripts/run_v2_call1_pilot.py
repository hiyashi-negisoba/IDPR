#!/usr/bin/env python3
"""Run the approved Step 8 Call 1 seed-router pilot over an explicit case list.

This runner intentionally has no Call 2/3 work.  It requires an explicit
``--prompt-approved`` acknowledgement before it opens a model connection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields  # noqa: E402
from idpr.neural.vllm_client import VLLMClient, VLLMClientError  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.v2.closure import ClosureError, compile_candidate_offenses, compile_closure  # noqa: E402
from idpr.v2.registry import KIND_TO_EXAMPLE_FILE, load_definitions  # noqa: E402
from idpr.v2.routing import (  # noqa: E402
    RouterContractError,
    router_catalog,
    router_request_payload,
    router_schema,
    validate_router_output,
)


DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_OUT = ROOT / "experiments/v2_call1_pilot/router_output.jsonl"
PROMPTS = ("v2_call1_router", "v2_call1_router_user")
SOURCE_FILES = (
    "src/idpr/v2/routing.py",
    "src/idpr/v2/call1_pilot.py",
    "src/idpr/v2/closure.py",
    "src/idpr/v2/registry.py",
    "scripts/run_v2_call1_pilot.py",
    "scripts/report_v2_call1_pilot.py",
    "prompts/v2_call1_router.md",
    "prompts/v2_call1_router_user.md",
)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _registry_sha256(definitions_dir: Path) -> str:
    digest = hashlib.sha256()
    for filename in sorted(set(KIND_TO_EXAMPLE_FILE.values())):
        path = definitions_dir / filename
        digest.update(filename.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _source_fingerprint() -> str:
    digest = hashlib.sha256()
    for relative_path in SOURCE_FILES:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update((ROOT / relative_path).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _case_ids(path: Path) -> tuple[str, ...]:
    ids = tuple(
        line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    if not ids:
        raise ValueError(f"{path}: case list is empty")
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: case list contains duplicate ids")
    return ids


def _selected_cases(
    inventory: Iterable[dict[str, Any]], case_ids: tuple[str, ...]
) -> list[dict[str, Any]]:
    records = tuple(inventory)
    indexed = {str(record.get("sub_question_id")): record for record in records}
    if len(indexed) != len(records):
        raise ValueError("inventory contains duplicate sub_question_id values")
    missing = [case_id for case_id in case_ids if case_id not in indexed]
    if missing:
        raise ValueError(f"case list ids are absent from inventory: {missing}")
    return [indexed[case_id] for case_id in case_ids]


def _closure_payload(closure, compiled: dict[str, Any]) -> dict[str, Any]:
    classifications = {
        "mandatory_core": closure.mandatory_core,
        "offense_probe": closure.offense_probes,
        "doctrine_probe": closure.doctrine_probes,
        "completion_probe": closure.completion_probes,
        "participation_probe": closure.participation_probes,
    }
    items: dict[str, list[dict[str, Any]]] = {}
    frontier_count = 0
    for classification, values in classifications.items():
        rendered = []
        for item in values:
            frontier_count += len(item.ground_fact_frontier)
            rendered.append({
                "definition_ref": item.definition_ref,
                "source_path": list(item.source_path),
                "occurrence_path": list(item.occurrence_path),
                "ground_fact_frontier": [
                    {
                        "occurrence_path": list(fact.occurrence_path),
                        "source_path": list(fact.source_path),
                        "ground_fact_ref": fact.ground_fact_ref,
                    }
                    for fact in item.ground_fact_frontier
                ],
                "deferred_refs": list(item.deferred_refs),
            })
        items[classification] = rendered
    return {
        "mandatory_offense_refs": sorted(closure.mandatory_offense_refs),
        "candidate_offense_refs": sorted(closure.candidate_offense_refs),
        "compiled_candidate_refs": sorted(compiled),
        "items": items,
        "ground_fact_frontier_count": frontier_count,
        "probe_count": sum(
            len(values) for key, values in classifications.items() if key != "mandatory_core"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--gold-parquet", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--vllm-max-model-len", type=int, default=32768)
    parser.add_argument("--vllm-max-num-seqs", type=int, default=1)
    parser.add_argument("--vllm-gpu-memory-utilization", type=float, default=0.90)
    parser.add_argument("--vllm-reasoning-parser", default="gemma4")
    parser.add_argument(
        "--vllm-structured-outputs-config",
        default='{"backend":"guidance","disable_any_whitespace":true}',
    )
    parser.add_argument(
        "--prompt-approved",
        action="store_true",
        help="required acknowledgement that the Call 1 prompt has passed separate review",
    )
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 1 model run")
    if not args.gold_parquet.is_file():
        parser.error(f"--gold-parquet does not exist: {args.gold_parquet}")
    if not args.model_snapshot.is_dir():
        parser.error(f"--model-snapshot does not exist: {args.model_snapshot}")

    registry = load_definitions(args.definitions_dir)
    catalog = router_catalog(registry)
    schema = router_schema(catalog)
    case_ids = _case_ids(args.case_list)
    inventory = _read_jsonl(args.inventory)
    records = _selected_cases(inventory, case_ids)
    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt, user_prompt = (load_prompt(name) for name in PROMPTS)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = args.out.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps({
        "step": "v2_call1_router_pilot",
        "git_commit": _git_commit(),
        "source_fingerprint": _source_fingerprint(),
        "model": args.model,
        "model_snapshot": str(args.model_snapshot),
        "model_revision": args.model_revision,
        "sampling": {"temperature": args.temperature, "max_tokens": args.max_tokens},
        "vllm": {
            "max_model_len": args.vllm_max_model_len,
            "max_num_seqs": args.vllm_max_num_seqs,
            "gpu_memory_utilization": args.vllm_gpu_memory_utilization,
            "reasoning_parser": args.vllm_reasoning_parser,
            "structured_outputs_config": args.vllm_structured_outputs_config,
        },
        "definitions_dir": str(args.definitions_dir),
        "registry_sha256": _registry_sha256(args.definitions_dir),
        "case_list": str(args.case_list),
        "case_list_sha256": _sha256_file(args.case_list),
        "inventory": str(args.inventory),
        "inventory_sha256": _sha256_file(args.inventory),
        "gold_parquet": str(args.gold_parquet),
        "gold_parquet_sha256": _sha256_file(args.gold_parquet),
        "prompts": {name: _sha256_file(prompt_path(name)) for name in PROMPTS},
        "catalog_definition_ids": [entry.definition_id for entry in catalog],
        "case_ids": list(case_ids),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    succeeded = failed = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for index, record in enumerate(records, start=1):
            case_id = str(record["sub_question_id"])
            payload = router_request_payload(
                case_text=str(record["question_text"]), catalog=catalog
            )
            assert set(payload) == {"case_text", "offense_catalog"}
            assert_no_leaked_fields(payload)
            row: dict[str, Any] = {"sub_question_id": case_id}
            output: dict[str, Any] | None = None
            try:
                output, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_call1_router",
                    schema=schema,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    user_template=user_prompt,
                )
                seeds = validate_router_output(output, catalog=catalog)
                closure = compile_closure(registry, seeds)
                compiled = dict(compile_candidate_offenses(registry, closure))
                row.update({
                    "raw_response": output,
                    "seeds": list(seeds),
                    "usage": metadata.get("usage", {}),
                    "model_response": {
                        "id": metadata.get("id"),
                        "model": metadata.get("model"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                    "closure": _closure_payload(closure, compiled),
                })
                succeeded += 1
                status = f"ok ({len(seeds)} seeds)"
            except (RouterContractError, ClosureError, VLLMClientError) as error:
                row.update({
                    "raw_response": output,
                    "error": f"{type(error).__name__}: {error}",
                    "errors": list(getattr(error, "errors", (str(error),))),
                })
                failed += 1
                status = "FAIL"
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            print(f"[{index}/{len(records)}] {case_id} {status}")
    print(f"ok={succeeded} failed={failed}")
    print(f"wrote {args.out}")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
