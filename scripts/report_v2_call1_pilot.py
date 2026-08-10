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

from idpr.v2.call1_pilot import (  # noqa: E402
    case_definition_calibration,
    summarize_definition_calibrations,
)
from idpr.v2.registry import DefinitionRegistry, load_definitions  # noqa: E402
from idpr.v2.routing import router_catalog  # noqa: E402


DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_ARTIFACT = ROOT / "experiments/v2_call1_pilot/router_output.jsonl"
DEFAULT_DEFINITION_GOLD = ROOT / "data/eval/v2_call1_definition_gold_draft.json"


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


def _definition_gold(
    path: Path, *, case_ids: tuple[str, ...], registry: DefinitionRegistry
) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("cases")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: cases must be a list")
    indexed = {str(row.get("case_id")): row for row in rows if isinstance(row, dict)}
    if len(indexed) != len(rows) or tuple(indexed) != case_ids:
        raise ValueError(f"{path}: case ids must exactly match the ordered case list")
    allowed = {entry.definition_id for entry in router_catalog(registry)}
    for case_id, row in indexed.items():
        refs = row.get("gold_definition_refs")
        notes = row.get("scope_notes")
        if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
            raise ValueError(f"{path}: {case_id} has invalid gold_definition_refs")
        if len(set(refs)) != len(refs) or not set(refs) <= allowed:
            raise ValueError(f"{path}: {case_id} has non-canonical gold_definition_refs")
        if not refs and (
            not isinstance(notes, list)
            or not any(isinstance(note, str) and "outside the closed catalog" in note for note in notes)
        ):
            raise ValueError(f"{path}: {case_id} empty gold requires an out-of-scope note")
    return indexed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--definition-gold", type=Path, default=DEFAULT_DEFINITION_GOLD)
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
    gold = _definition_gold(args.definition_gold, case_ids=case_ids, registry=registry)

    report_rows: list[dict[str, Any]] = []
    for case_id in case_ids:
        row = indexed[case_id]
        rendered = {
            "sub_question_id": case_id,
            "raw_seeds": list(row.get("raw_seeds") or row.get("seeds") or ()),
            "normalized_seeds": list(row.get("normalized_seeds") or row.get("seeds") or ()),
            "duplicate_refs": list(row.get("duplicate_refs") or ()),
            "normalization_applied": bool(row.get("normalization_applied", False)),
            "seeds": list(row.get("normalized_seeds") or row.get("seeds") or ()),
            "closure": row.get("closure") or {},
            "gold": {
                "source_article_gold": list(gold[case_id].get("source_article_gold") or ()),
                "gold_definition_refs": list(gold[case_id]["gold_definition_refs"]),
                "scope_notes": list(gold[case_id].get("scope_notes") or ()),
            },
        }
        if row.get("error"):
            rendered["error"] = row["error"]
        else:
            rendered["calibration"] = case_definition_calibration(
                registry,
                seeds=tuple(rendered["normalized_seeds"]),
                gold_definition_refs=tuple(gold[case_id]["gold_definition_refs"]),
            )
        report_rows.append(rendered)

    report = {
        "step": "v2_call1_router_pilot_report",
        "artifact": str(args.artifact),
        "artifact_sha256": _sha256(args.artifact),
        "case_list": str(args.case_list),
        "case_list_sha256": _sha256(args.case_list),
        "definition_gold": str(args.definition_gold),
        "definition_gold_sha256": _sha256(args.definition_gold),
        "definitions_dir": str(args.definitions_dir),
        "summary": summarize_definition_calibrations(report_rows),
        "cases": report_rows,
        "metric_contract": {
            "metric_name": "closed-catalog DefinitionRef recall",
            "denominator": "approved in-scope gold_definition_refs only",
            "raw_success": "gold_definition_ref intersects normalized_seeds",
            "closure_success": "gold_definition_ref intersects candidate_offense_refs",
            "additional_recovery": "full15 survives while prefix10 does not",
            "seed_count": "normalized_seeds; raw_seed_count is model-behavior diagnostic only",
            "normalization": "stable unique canonical refs, preserving first occurrence order",
            "attempt_and_preparation": "not separate router labels; evaluated downstream from the selected offense",
            "out_of_scope": "empty gold rows with an explicit closed-catalog scope note are reported outside the denominator",
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
