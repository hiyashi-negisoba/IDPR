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

from idpr.v2.runtime.answer_plan import (
    extract_final_conclusion_section,
    missing_final_conclusions,
    parse_required_final_conclusions,
)


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(json.loads(line)["sub_question_id"]): json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def _as_dict(anchor) -> dict[str, str]:
    return {
        "actor": anchor.actor,
        "offense_label": anchor.offense_label,
        "state": anchor.state,
    }


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
        # 규칙은 runtime이 소유한다. Call 3 runner도 같은 함수를 부르므로 두 감사가 "이
        # 앵커가 언급되었는가"를 두고 다른 답을 낼 수 없다.
        required = str(plan_row.get("required_final_conclusions", ""))
        anchors = parse_required_final_conclusions(required)
        missing = [_as_dict(value) for value in missing_final_conclusions(answer_text, required)]
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
