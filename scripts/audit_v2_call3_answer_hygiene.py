#!/usr/bin/env python3
"""Automatic checks over a Call 3 run that do not require reading the answers.

Three of the four freeze criteria are decided by a human reading the analysis (F1, F2)
or by comparing a citation against the plan (F3).  The two that can be decided
mechanically are here, plus the participation check the freeze document requires:

* identifier hygiene -- no internal id (binding, instance, issue, card, predicate slug)
  reaches the answer text;
* citation identity -- every case number in the answer is one the plan supplied, and no
  pronouncement date is attached to a case the plan gave without one.  Per the freeze
  decision, `verbatim` means preserved identifying information, not string equality, so
  word order around the number is not a violation;
* participation fidelity -- for sealed questions the answer body must not be printed, so
  the participation form vocabulary and actor survival are checked and only the verdict
  is reported.

No model is called and no answer is edited.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.runtime.answer_plan import extract_final_conclusion_section

# Internal identifiers the plan carries but the answer must never surface.
_ID_PATTERNS = [
    re.compile(r"\bderived_binding[:\s]*\d*", re.IGNORECASE),
    re.compile(r"\bbinding[:_]\s*\d+", re.IGNORECASE),
    re.compile(r"\binstance[:_]\s*\d+", re.IGNORECASE),
    re.compile(r"\bissue[:_]\s*\d+", re.IGNORECASE),
    re.compile(r"\bcard[:_]\s*[0-9a-z_]+", re.IGNORECASE),
    re.compile(r"\bGroundFact\b"),
    re.compile(r"\bsub_question_id\b"),
    re.compile(r"\bkcl_criminal_r\d+", re.IGNORECASE),
]

# Korean case numbers: 2018도13877, 2015가합1234, 93헌마120 ...
_CASE_NUMBER = re.compile(r"\d{2,4}\s*(?:도|다|가[합단소]?|허|후|헌[가나마바]|초기|모|오|우|재도)\s*\d+")
# A pronouncement date immediately around a citation: 2018. 5. 17. 선고
_DATE_NEAR_CITATION = re.compile(r"\d{4}\s*\.\s*\d{1,2}\s*\.\s*\d{1,2}\s*\.?\s*선고")

_ACTOR = re.compile(r"[甲乙丙丁戊己庚辛]")
_PARTICIPATION_FORMS = ("교사", "방조", "공동정범", "간접정범", "종범", "정범")


def _norm(text: str) -> str:
    """Whitespace-insensitive form, so `2018 도 13877` and `2018도13877` compare equal."""
    return re.sub(r"\s+", "", text)


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[str(row["sub_question_id"])] = row
    return out


def _plan_text(plan: dict[str, Any]) -> str:
    return "\n".join(
        str(plan.get(key) or "")
        for key in ("case_text", "question", "analysis", "open_points", "required_final_conclusions")
    )


def _leaked_identifiers(answer: str) -> list[str]:
    found: list[str] = []
    for pattern in _ID_PATTERNS:
        found.extend(match.group(0) for match in pattern.finditer(answer))
    return sorted(set(found))


def _citation_findings(answer: str, plan_text: str) -> dict[str, list[str]]:
    plan_norm = _norm(plan_text)
    invented = [
        match.group(0)
        for match in _CASE_NUMBER.finditer(answer)
        if _norm(match.group(0)) not in plan_norm
    ]
    invented_dates = [
        match.group(0)
        for match in _DATE_NEAR_CITATION.finditer(answer)
        if _norm(match.group(0)) not in plan_norm
    ]
    return {
        "unsupported_case_numbers": sorted(set(invented)),
        "unsupported_pronouncement_dates": sorted(set(invented_dates)),
    }


def _participation_findings(answer: str, plan: dict[str, Any]) -> dict[str, Any]:
    required = str(plan.get("required_final_conclusions") or "")
    closing = extract_final_conclusion_section(answer)

    plan_forms = sorted({form for form in _PARTICIPATION_FORMS if form in required})
    missing_forms = [form for form in plan_forms if form not in answer]

    plan_actors = sorted(set(_ACTOR.findall(required)))
    missing_actors = [actor for actor in plan_actors if actor not in closing]

    return {
        "plan_participation_forms": plan_forms,
        "missing_participation_forms": missing_forms,
        "plan_actors": plan_actors,
        "actors_absent_from_closing": missing_actors,
        "ok": not missing_forms and not missing_actors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--sealed-case-id-file",
        type=Path,
        help="One id per line.  These are reported by verdict only, never by content.",
    )
    args = parser.parse_args()

    answers = _rows(args.answers)
    plans = _rows(args.answer_plans)
    sealed = set()
    if args.sealed_case_id_file:
        sealed = {
            line.strip()
            for line in args.sealed_case_id_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }

    findings: list[dict[str, Any]] = []
    for case_id, answer_row in answers.items():
        plan = plans.get(case_id)
        if plan is None:
            findings.append({"case_id": case_id, "error": "no plan for this answer"})
            continue
        answer = str(answer_row["answer"])
        finding: dict[str, Any] = {
            "case_id": case_id,
            "sealed": case_id in sealed,
            "leaked_identifiers": _leaked_identifiers(answer),
        }
        finding.update(_citation_findings(answer, _plan_text(plan)))
        finding["participation"] = _participation_findings(answer, plan)
        findings.append(finding)

    def _failed(finding: dict[str, Any]) -> bool:
        return bool(
            finding.get("error")
            or finding.get("leaked_identifiers")
            or finding.get("unsupported_case_numbers")
            or finding.get("unsupported_pronouncement_dates")
            or not finding.get("participation", {}).get("ok", True)
        )

    summary = {
        "answers": str(args.answers),
        "answer_plans": str(args.answer_plans),
        "cases": len(findings),
        "sealed_cases": sorted(sealed),
        "cases_with_leaked_identifiers": sum(1 for f in findings if f.get("leaked_identifiers")),
        "cases_with_unsupported_case_numbers": sum(
            1 for f in findings if f.get("unsupported_case_numbers")
        ),
        "cases_with_unsupported_dates": sum(
            1 for f in findings if f.get("unsupported_pronouncement_dates")
        ),
        "cases_failing_participation_check": sum(
            1 for f in findings if not f.get("participation", {}).get("ok", True)
        ),
        "cases_failing_any": sum(1 for f in findings if _failed(f)),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for finding in findings:
        if _failed(finding):
            seal = " [sealed]" if finding.get("sealed") else ""
            print(f"  {finding['case_id']}{seal}: {json.dumps(finding, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
