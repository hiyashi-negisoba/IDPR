#!/usr/bin/env python3
"""Write and validate the manifest for the pinned Phase-3 v2 59-case run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--slurm-job-id", required=True)
    parser.add_argument("--stage-seconds", action="append", default=[])
    parser.add_argument(
        "--fact-graphs",
        type=Path,
        default=None,
        help="call-1 artifact actually consumed; defaults to run-root/fact_graphs.jsonl",
    )
    parser.add_argument(
        "--deviation",
        action="append",
        default=[],
        help="key=value record of a departure from the pinned configuration",
    )
    args = parser.parse_args()
    fact_graphs = args.fact_graphs or (args.run_root / "fact_graphs.jsonl")

    inventory = rows(args.inventory)
    outputs = rows(args.output)
    inventory_ids = [row["sub_question_id"] for row in inventory]
    output_ids = [row["sub_question_id"] for row in outputs]
    if len(inventory_ids) != 59 or len(set(inventory_ids)) != 59:
        raise ValueError("sealed inventory must contain 59 unique cases")
    if output_ids != inventory_ids:
        raise ValueError("v2 output IDs or order differ from the sealed inventory")
    if any(not str(row.get("generated_response", "")).strip() for row in outputs):
        raise ValueError("v2 output contains an empty answer")

    stage_seconds = {}
    for item in args.stage_seconds:
        key, value = item.split("=", 1)
        stage_seconds[key] = int(value)

    deviations = {}
    for item in args.deviation:
        key, value = item.split("=", 1)
        deviations[key] = value

    artifact_names = (
        fact_graphs.name,
        "article_selection.jsonl",
        "l0_candidates.jsonl",
        "l0_report.json",
        args.output.name,
    )
    manifest = {
        "version": "1.0.0",
        "status": "complete",
        "scope": "phase3_v2_final_59_generation",
        "slurm_job_id": args.slurm_job_id,
        "source_commit": args.source_commit,
        "source_root": str(args.source_root),
        "model": args.model,
        "model_snapshot": str(args.model_snapshot),
        "cases": len(outputs),
        "parameters": {
            "retrieval_top_k_articles": 10,
            "call1_max_tokens": 8192,
            "call1_5_max_tokens": 2048,
            "call2_max_tokens": 12288,
            "call3_max_tokens": 16384,
            "temperature": 0.0,
            "no_cache": True,
        },
        "stage_seconds": stage_seconds,
        "fact_graphs": str(fact_graphs.relative_to(args.run_root)),
        "deviations": deviations,
        "source_sha256": {
            "inventory": sha256(args.inventory),
            **{
                name: sha256(args.run_root / name)
                for name in artifact_names
            },
        },
    }
    target = args.run_root / "generation_manifest.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
