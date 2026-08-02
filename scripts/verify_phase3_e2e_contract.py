"""Validate the two-case Phase-3 E2E run and write its reproducibility manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from idpr.eval.e2e_contract import verify_run
from idpr.eval.issue_recall import PROJECT_ROOT


def _pairs(values: list[str], *, numeric: bool) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected KEY=VALUE, got {value!r}")
        key, raw = value.split("=", 1)
        if not key or key in result:
            raise ValueError(f"invalid or duplicate key {key!r}")
        result[key] = float(raw) if numeric else raw
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=PROJECT_ROOT / "data/smoke/phase3_e2e_inventory.jsonl",
    )
    parser.add_argument(
        "--rubric",
        type=Path,
        default=PROJECT_ROOT / "data/smoke/phase3_e2e_rubrics.json",
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--slurm-job-id", required=True)
    parser.add_argument(
        "--tested-code-commit",
        help="Git commit used to generate the model artifacts (default: current HEAD)",
    )
    parser.add_argument("--parameter", action="append", default=[])
    parser.add_argument("--stage-seconds", action="append", default=[])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = verify_run(
        project_root=PROJECT_ROOT,
        run_root=args.run_root,
        inventory_path=args.inventory,
        rubric_path=args.rubric,
        model=args.model,
        slurm_job_id=args.slurm_job_id,
        parameters=_pairs(args.parameter, numeric=False),
        stage_seconds=_pairs(args.stage_seconds, numeric=True),
        tested_code_commit=args.tested_code_commit,
    )
    out = args.out or args.run_root / "freeze_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "manifest": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
