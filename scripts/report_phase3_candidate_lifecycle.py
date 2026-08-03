#!/usr/bin/env python3
"""Audit L0 candidate survival through the persisted Call-3 request."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build_report(run_root: Path) -> dict[str, Any]:
    candidates_path = run_root / "l0_candidates.jsonl"
    candidates = {
        str(row["sub_question_id"]): row for row in _rows(candidates_path)
    }
    errors: list[str] = []
    cases: list[dict[str, Any]] = []
    visibility = Counter()
    reasons = Counter()
    source_visibility = Counter()
    must_discuss = hidden_must_discuss = 0

    for case_id, candidate in candidates.items():
        answer_path = run_root / "cases" / case_id / "answer.json"
        if not answer_path.is_file():
            errors.append(f"{case_id}: missing answer.json")
            continue
        answer = json.loads(answer_path.read_text(encoding="utf-8"))
        request = answer.get("request", {})
        lifecycle = request.get("candidate_lifecycle")
        if not isinstance(lifecycle, list):
            errors.append(f"{case_id}: request has no candidate_lifecycle")
            continue
        expected = [str(article) for article in candidate.get("articles", ())]
        observed = [str(row.get("article", "")) for row in lifecycle]
        if expected != observed:
            errors.append(f"{case_id}: lifecycle articles differ from L0 candidates")

        case_hidden_mandatory: list[str] = []
        for row in lifecycle:
            article = str(row.get("article", ""))
            decision = str(row.get("visibility_decision", ""))
            reason = str(row.get("visibility_reason", ""))
            relevance = str(row.get("relevance", ""))
            provenance = row.get("provenance", {})
            sources = provenance.get("sources", ()) if isinstance(provenance, Mapping) else ()
            visibility[decision] += 1
            reasons[reason] += 1
            for source in sources:
                source_visibility[(str(source), decision)] += 1
            if relevance == "must_discuss":
                must_discuss += 1
                if not bool(row.get("included_in_call3")):
                    hidden_must_discuss += 1
                    case_hidden_mandatory.append(article)
        if case_hidden_mandatory:
            errors.append(
                f"{case_id}: hidden must_discuss articles {case_hidden_mandatory}"
            )
        cases.append(
            {
                "sub_question_id": case_id,
                "candidates": len(expected),
                "included": sum(
                    bool(row.get("included_in_call3")) for row in lifecycle
                ),
                "hidden_must_discuss": case_hidden_mandatory,
                "lifecycle": lifecycle,
            }
        )

    return {
        "version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_root": str(run_root),
        "cases_expected": len(candidates),
        "cases_audited": len(cases),
        "must_discuss": {
            "total": must_discuss,
            "hidden": hidden_must_discuss,
            "survival_rate": (
                (must_discuss - hidden_must_discuss) / must_discuss
                if must_discuss
                else None
            ),
        },
        "visibility_counts": dict(sorted(visibility.items())),
        "visibility_reason_counts": dict(sorted(reasons.items())),
        "source_visibility_counts": {
            f"{source}:{decision}": count
            for (source, decision), count in sorted(source_visibility.items())
        },
        "errors": errors,
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.run_root)
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
