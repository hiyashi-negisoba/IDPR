#!/usr/bin/env python3
"""Report required final conclusions absent from each answer's closing section.

No model is called and no answer is edited.  This is the completeness half of the Call 3
contract: whether every anchor the plan required was mentioned where the closing-paragraph
instruction applies.  Whether the state each one asserts is the *right* one is the fidelity
half, which reads the analysis and is not decided here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.runtime.answer_plan import extract_final_conclusion_section


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(json.loads(line)["sub_question_id"]): json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def _anchors(serialized: str) -> list[dict[str, str]]:
    """Parse back the `· actor — offense: state ...` lines the plan serialized."""
    out: list[dict[str, str]] = []
    for line in serialized.splitlines():
        line = line.strip()
        if not line.startswith("·"):
            continue
        body = line[1:].strip()
        if "—" not in body or ":" not in body:
            continue
        actor, rest = body.split("—", 1)
        offense, state = rest.split(":", 1)
        out.append(
            {
                "actor": actor.strip(),
                "offense_label": offense.strip(),
                "state": state.strip(),
                "line": line,
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    answers = _rows(args.answers)
    plans = _rows(args.answer_plans)

    findings: list[dict[str, Any]] = []
    for case_id, answer_row in sorted(answers.items()):
        plan_row = plans.get(case_id)
        if plan_row is None:
            raise SystemExit(f"{case_id}: no answer plan")
        answer_text = str(answer_row["answer"])
        section = extract_final_conclusion_section(answer_text)
        anchors = _anchors(str(plan_row.get("required_final_conclusions", "")))
        missing = [
            anchor
            for anchor in anchors
            if anchor["actor"] not in section or anchor["offense_label"] not in section
        ]
        findings.append(
            {
                "case_id": case_id,
                "required_count": len(anchors),
                "missing_count": len(missing),
                "missing": missing,
                "closing_section_chars": len(section),
                "answer_chars": len(answer_text),
            }
        )

    summary = {
        "answers": str(args.answers),
        "answer_plans": str(args.answer_plans),
        "cases": len(findings),
        "total_required": sum(item["required_count"] for item in findings),
        "total_missing": sum(item["missing_count"] for item in findings),
        "cases_with_missing": sum(1 for item in findings if item["missing_count"]),
        "repaired": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for item in findings:
        mark = "MISSING" if item["missing_count"] else "ok"
        print(f"  {item['case_id']}: {item['required_count']} required, {mark}")
        for anchor in item["missing"]:
            print(f"      absent from closing section: {anchor['line']}")


if __name__ == "__main__":
    main()
