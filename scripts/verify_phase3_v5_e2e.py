#!/usr/bin/env python3
"""Gate the v5 smoke on coverage preservation and host-owned logical consistency."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.report_phase3_candidate_lifecycle import build_report


KCL = "kcl_criminal_r10_p1_q1_ga"
USER = "CASE_KCL1730_2026_BRIBERY_FRAUD_002"
KCL_CORE = frozenset({"art298", "art297", "art301"})


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl_index(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def verify_v5(run_root: Path) -> dict[str, Any]:
    candidates = _jsonl_index(run_root / "l0_candidates.jsonl")
    lifecycle_report = build_report(run_root)
    checks: dict[str, bool] = {
        "lifecycle_audit_passed": lifecycle_report["status"] == "passed",
        "must_discuss_survival_100pct": lifecycle_report["must_discuss"]["hidden"] == 0,
    }

    kcl_candidate_articles = set(candidates[KCL]["articles"])
    checks["kcl_core_issue_families_retrieved"] = KCL_CORE <= kcl_candidate_articles

    requests = {
        case_id: _json(run_root / "cases" / case_id / "answer.json")["request"]
        for case_id in (KCL, USER)
    }
    kcl_included = {
        str(section["article"]) for section in requests[KCL]["required_sections"]
    }
    checks["kcl_core_issue_families_reach_call3"] = KCL_CORE <= kcl_included
    checks["user_fraud_reaches_call3"] = "art347" in {
        str(section["article"]) for section in requests[USER]["required_sections"]
    }

    logic_errors: list[str] = []
    for case_id, request in requests.items():
        for section in request["required_sections"]:
            article = str(section["article"])
            verdict = str(section.get("verdict", "unknown"))
            stated = str(section.get("stated_conclusion", "undetermined"))
            directive = str(section.get("symbolic_directive", ""))
            if verdict == "established" and stated != "established":
                logic_errors.append(f"{case_id}:{article}: established verdict drift")
            if verdict == "not_established" and stated == "established":
                logic_errors.append(f"{case_id}:{article}: refuted but stated established")
            if verdict == "attempt_review" and directive != "attempt_review":
                logic_errors.append(f"{case_id}:{article}: attempt directive drift")
    checks["relevance_verdict_conclusion_consistent"] = not logic_errors

    failures = sorted(name for name, passed in checks.items() if not passed)
    return {
        "version": "1.0.0",
        "status": "passed" if not failures else "failed",
        "checks": checks,
        "failures": failures,
        "logic_errors": logic_errors,
        "lifecycle_summary": {
            "must_discuss": lifecycle_report["must_discuss"],
            "visibility_counts": lifecycle_report["visibility_counts"],
            "visibility_reason_counts": lifecycle_report[
                "visibility_reason_counts"
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = verify_v5(args.run_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(args.out)
    print(f"status={report['status']} out={args.out}")
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
