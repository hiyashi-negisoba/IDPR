#!/usr/bin/env python3
"""Report Call 1 router survival and the ordered 10-vs-15 calibration signal."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.issue_recall import INVENTORY_PATH, load_issue_gold  # noqa: E402
from idpr.neural.article_select import load_catalog  # noqa: E402
from idpr.v2.call1_pilot import (  # noqa: E402
    article_definition_refs,
    case_calibration,
    summarize_calibrations,
)
from idpr.v2.registry import load_definitions  # noqa: E402


DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_ARTIFACT = ROOT / "experiments/v2_call1_pilot/router_output.jsonl"


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
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path}: duplicate case ids")
    return ids


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--parquet", type=Path, help="KCL source parquet required for rubric gold")
    args = parser.parse_args()
    output = args.out or args.artifact.with_suffix(".report.json")

    case_ids = _case_ids(args.case_list)
    rows = _read_jsonl(args.artifact)
    indexed = {str(row.get("sub_question_id")): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("artifact contains duplicate sub_question_id values")
    missing = sorted(set(case_ids) - set(indexed))
    extra = sorted(set(indexed) - set(case_ids))
    if missing or extra:
        raise ValueError(f"artifact/case-list mismatch: missing={missing}, extra={extra}")

    registry = load_definitions(args.definitions_dir)
    mapped_refs = article_definition_refs(registry, load_catalog())
    gold = load_issue_gold(
        inventory_path=args.inventory, parquet_path=args.parquet, with_attempt=False
    )
    missing_gold = sorted(set(case_ids) - set(gold))
    if missing_gold:
        raise ValueError(f"case-list ids are absent from rubric gold: {missing_gold}")

    report_rows: list[dict[str, Any]] = []
    for case_id in case_ids:
        row = indexed[case_id]
        rendered = {
            "sub_question_id": case_id,
            "seeds": list(row.get("seeds") or ()),
            "closure": row.get("closure") or {},
        }
        if row.get("error"):
            rendered["error"] = row["error"]
        else:
            rendered["calibration"] = case_calibration(
                registry,
                seeds=tuple(row["seeds"]),
                gold_articles=gold[case_id].articles,
                mapped_refs_by_article=mapped_refs,
            )
        report_rows.append(rendered)

    report = {
        "step": "v2_call1_router_pilot_report",
        "artifact": str(args.artifact),
        "artifact_sha256": _sha256(args.artifact),
        "case_list": str(args.case_list),
        "case_list_sha256": _sha256(args.case_list),
        "definitions_dir": str(args.definitions_dir),
        "article_to_mapped_refs": mapped_refs,
        "summary": summarize_calibrations(report_rows),
        "cases": report_rows,
        "metric_contract": {
            "raw_success": "mapped_refs(article) intersects router seeds",
            "closure_success": "mapped_refs(article) intersects candidate_offense_refs",
            "additional_recovery": "full15 survives while prefix10 does not",
            "attempt_gold": "excluded; CompletionPolicy represents attempts in v2",
        },
    }
    failed_cases = int(report["summary"].get("failed_cases", 0))
    report["run_status"] = "FAILED" if failed_cases else "SUCCEEDED"
    report["calibration_valid"] = failed_cases == 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
