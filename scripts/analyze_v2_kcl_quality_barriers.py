#!/usr/bin/env python3
"""Audit structural reasons a V2 KCL answer bundle can lose rubric credit.

Rubrics are read only after generation and are never emitted into a model input.  Exact
article and dispute-marker checks are diagnostic lower bounds, not semantic judge scores.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.rubric import load_rubric_sets

ARTICLE = re.compile(r"제\s*(\d+)\s*조(?:\s*의\s*(\d+))?")
ARTICLE_REQUIREMENT = re.compile(
    r"조문|조항|법조|법문|규정|명시|언급|적시|제시|인용|검토"
)
DISPUTE = re.compile(r"견해|학설|다수의견|소수의견|다수설|소수설|대립")


def rows(path: Path, field: str) -> dict[str, str]:
    return {
        str(row["sub_question_id"]): str(row[field])
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _article_pairs(text: str) -> tuple[set[tuple[str, str | None]], set[str]]:
    pairs = {(match.group(1), match.group(2)) for match in ARTICLE.finditer(text)}
    return pairs, {article for article, _ in pairs}


def answer_diagnostics(
    *, answers: dict[str, str], rubric_sets: dict[str, Any], crime_names: tuple[str, ...]
) -> dict[str, Any]:
    article_required = 0
    article_hit = 0
    article_misses_by_case: dict[str, int] = {}
    dispute_items = 0
    dispute_required_cases = 0
    dispute_marker_cases = 0
    dispute_marker_missing_cases: list[str] = []
    crime_required = 0
    crime_mentioned = 0
    crime_missing_by_case: dict[str, list[str]] = {}

    for case_id, answer in answers.items():
        rubric = rubric_sets[case_id]
        pairs, articles = _article_pairs(answer)
        case_article_misses = 0
        for item in rubric.rubrics:
            match = ARTICLE.search(item)
            if match is None or ARTICLE_REQUIREMENT.search(item) is None:
                continue
            article_required += 1
            present = (
                (match.group(1), match.group(2)) in pairs
                if match.group(2)
                else match.group(1) in articles
            )
            article_hit += int(present)
            case_article_misses += int(not present)
        if case_article_misses:
            article_misses_by_case[case_id] = case_article_misses

        case_disputes = sum(bool(DISPUTE.search(item)) for item in rubric.rubrics)
        dispute_items += case_disputes
        if case_disputes:
            dispute_required_cases += 1
            if DISPUTE.search(answer):
                dispute_marker_cases += 1
            else:
                dispute_marker_missing_cases.append(case_id)

        rubric_text = "\n".join(rubric.rubrics)
        required_names = {name for name in crime_names if name in rubric_text}
        mentioned_names = {name for name in required_names if name in answer}
        crime_required += len(required_names)
        crime_mentioned += len(mentioned_names)
        missing = sorted(required_names - mentioned_names)
        if missing:
            crime_missing_by_case[case_id] = missing

    return {
        "case_count": len(answers),
        "explicit_article_requirements": {
            "hit": article_hit,
            "total": article_required,
            "rate": article_hit / article_required if article_required else None,
            "misses_by_case": article_misses_by_case,
        },
        "dispute_marker_lower_bound": {
            "rubric_items": dispute_items,
            "cases_requiring_dispute_discussion": dispute_required_cases,
            "answers_with_dispute_marker": dispute_marker_cases,
            "required_cases_without_marker": dispute_marker_missing_cases,
        },
        "crime_name_lexical_lower_bound": {
            "mentioned": crime_mentioned,
            "required": crime_required,
            "rate": crime_mentioned / crime_required if crime_required else None,
            "missing_by_case": crime_missing_by_case,
        },
    }


def _plan_diagnostics(path: Path) -> dict[str, Any]:
    plans = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    states = Counter()
    open_points = Counter()
    for plan in plans:
        for line in str(plan.get("required_final_conclusions", "")).splitlines():
            if not line.strip():
                continue
            if "확정하기 어렵" in line:
                states["unresolved"] += 1
            elif "성립하지" in line or "불성립" in line:
                states["failed"] += 1
            else:
                states["established"] += 1
        for line in str(plan.get("open_points", "")).splitlines():
            if line.strip().startswith("·"):
                open_points[line.strip()] += 1
    total = sum(states.values())
    return {
        "case_count": len(plans),
        "anchored_issue_count": sum(int(value["anchored_issue_count"]) for value in plans),
        "required_final_conclusion_states": dict(states),
        "unresolved_rate": states["unresolved"] / total if total else None,
        "retained_offense_count": sum(int(value["retained_offense_count"]) for value in plans),
        "open_point_occurrences": sum(open_points.values()),
        "unique_open_points": len(open_points),
        "open_point_case_frequency": dict(open_points),
    }


def _call2_diagnostics(path: Path) -> dict[str, Any]:
    counts = Counter()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        counts.update(value["truth"] for value in row.get("assessments", ()))
    total = sum(counts.values())
    return {
        "truth_counts": dict(counts),
        "unknown_rate": counts["UNKNOWN"] / total if total else None,
    }


def _active_doctrines(path: Path) -> dict[str, Any]:
    counts = Counter()
    unresolved = Counter()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        for doctrine in row.get("active_doctrines") or ():
            counts[str(doctrine.get("doctrine_ref") or doctrine.get("id") or "unknown")] += 1
        final = row.get("final_responsibility") or {}
        for finding in final.get("unresolved_findings") or ():
            unresolved[str(finding.get("marker"))] += 1
    return {
        "active_doctrine_counts": dict(counts),
        "unresolved_finding_counts": dict(unresolved),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
    )
    parser.add_argument("--p-answers", type=Path, required=True)
    parser.add_argument("--n-answers", type=Path, required=True)
    parser.add_argument("--baseline-answers", type=Path, required=True)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--call2", type=Path, required=True)
    parser.add_argument("--e2e-results", type=Path, required=True)
    parser.add_argument(
        "--rubric-binding-audit", type=Path, required=True
    )
    parser.add_argument("--card-summary", type=Path, required=True)
    parser.add_argument(
        "--crime-map", type=Path, default=ROOT / "data/eval/rubric_crime_article_map.json"
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rubrics = load_rubric_sets(args.inventory)
    crime_map = json.loads(args.crime_map.read_text(encoding="utf-8"))
    crime_names = tuple(sorted(crime_map["crimes"], key=len, reverse=True))
    p_answers = rows(args.p_answers, "answer")
    case_ids = tuple(p_answers)
    rubric_types = Counter(
        item_type for case_id in case_ids for item_type in rubrics[case_id].item_types
    )
    report = {
        "scope": {
            "case_count": len(case_ids),
            "rubric_item_count": sum(len(rubrics[case_id]) for case_id in case_ids),
            "rubric_type_counts": dict(rubric_types),
            "warning": (
                "article/dispute/crime-name checks are deterministic lower-bound diagnostics, "
                "not semantic rubric scores"
            ),
        },
        "call2": _call2_diagnostics(args.call2),
        "answer_plan": _plan_diagnostics(args.answer_plans),
        "doctrine_runtime": _active_doctrines(args.e2e_results),
        "answer_diagnostics": {
            "P": answer_diagnostics(
                answers=p_answers, rubric_sets=rubrics, crime_names=crime_names
            ),
            "N": answer_diagnostics(
                answers=rows(args.n_answers, "answer"),
                rubric_sets=rubrics,
                crime_names=crime_names,
            ),
            "baseline": answer_diagnostics(
                answers=rows(args.baseline_answers, "generated_response"),
                rubric_sets=rubrics,
                crime_names=crime_names,
            ),
        },
        "binding_coverage": json.loads(
            args.rubric_binding_audit.read_text(encoding="utf-8")
        )["aggregate"],
        "card_coverage": json.loads(args.card_summary.read_text(encoding="utf-8")),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["scope"], ensure_ascii=False))
    print(json.dumps(report["answer_plan"], ensure_ascii=False))
    for name, value in report["answer_diagnostics"].items():
        print(name, json.dumps(value["explicit_article_requirements"], ensure_ascii=False))
        print(name, json.dumps(value["dispute_marker_lower_bound"], ensure_ascii=False))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
