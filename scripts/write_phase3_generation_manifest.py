"""Write a deterministic handoff manifest for the final 59-case generation run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from idpr.rulebase.cards import PROJECT_ROOT


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--slurm-job-id", required=True)
    parser.add_argument("--tested-code-commit", required=True)
    parser.add_argument("--stage-seconds", action="append", default=[])
    parser.add_argument("--resume-from-job-id")
    parser.add_argument("--reused-answer-count", type=int)
    parser.add_argument("--repaired-call1-count", type=int)
    args = parser.parse_args()
    timings = {}
    for item in args.stage_seconds:
        name, value = item.split("=", 1)
        timings[name] = int(value)
    artifacts = {
        str(path.relative_to(args.run_root)): sha256(path)
        for path in sorted(args.run_root.rglob("*"))
        if path.is_file() and path != args.run_root / "generation_manifest.json"
    }
    prompt_hashes = {
        path.name: sha256(path)
        for path in (
            PROJECT_ROOT / "prompts/fact_graph_extract.md",
            PROJECT_ROOT / "prompts/fact_graph_contract_repair.md",
            PROJECT_ROOT / "prompts/article_select.md",
            PROJECT_ROOT / "prompts/issue_assess.md",
            PROJECT_ROOT / "prompts/issue_long_form_generate.md",
        )
    }
    inventory_ids = [
        json.loads(line)["sub_question_id"]
        for line in args.inventory.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output_rows = [
        json.loads(line)
        for line in args.output.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output_ids = [row.get("sub_question_id") for row in output_rows]
    if len(inventory_ids) != len(set(inventory_ids)):
        raise ValueError("inventory contains duplicate sub_question_id values")
    if output_ids != inventory_ids:
        raise ValueError("output ids must exactly match inventory order")
    if any(row.get("error") or not str(row.get("generated_response", "")).strip() for row in output_rows):
        raise ValueError("output contains an error or empty generated_response")

    payload = {
        "version": "1.0.0",
        "scope": "phase3_final_59_generation",
        "cases": sum(1 for line in args.inventory.read_text(encoding="utf-8").splitlines() if line.strip()),
        "git_sha": args.tested_code_commit,
        "model": args.model,
        "slurm_job_id": args.slurm_job_id,
        "parameters": {"retrieval_top_k_articles": 10, "temperature": 0.0},
        "stage_seconds": timings,
        "prompt_sha256": prompt_hashes,
        "scallop_sha256": sha256(PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"),
        "output_sha256": sha256(args.output),
        "artifact_sha256": artifacts,
        "future_work": "Compare this output with baselines using the frozen LLM-as-a-judge protocol.",
    }
    if args.resume_from_job_id:
        payload["resume"] = {
            "from_slurm_job_id": args.resume_from_job_id,
            "reused_answer_count": args.reused_answer_count,
            "repaired_call1_count": args.repaired_call1_count,
        }
    out = args.run_root / "generation_manifest.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
