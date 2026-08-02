from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.legacy.fraud_planning import (  # noqa: E402
    render_reasoning_plan_text,
    select_fraud_reasoning_plan,
    validate_fraud_case,
)


DEFAULT_CASE_SET = (
    PROJECT_ROOT
    / "data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.json"
)
DEFAULT_NORM_CARDS = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data/e2e/fraud/manual_paraphrases/fraud_manual_card_review.md"
)
CASE_LABELS = {
    "manual_fraud_046_01_loan_repayment": "차용 당시 변제 의사·능력",
    "manual_fraud_047_01_loan_extension": "변제기 연장과 재산상 이익",
    "manual_fraud_050_01_unpaid_dining": "무전취식과 묵시적 기망",
    "manual_fraud_052_01_supply_deposit": "전선 공급계약의 계약금",
    "manual_fraud_063_01_parcel_triangular": "택배물 삼각사기",
}
STATUS_LABELS = {
    "satisfied": "충족",
    "not_satisfied": "불충족",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_text(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_review(
    case_set: Mapping[str, Any], norm_card_set: Mapping[str, Any]
) -> str:
    cards_by_id = {
        card["id"]: card for card in norm_card_set.get("cards", [])
    }
    lines = [
        "# 사기죄 Paraphrase 5건 카드별 적용 검토표",
        "",
        "## 검토 방법",
        "",
        "이 표는 이미 승인된 법리 카드의 문구를 다시 검수하는 표가 아니라, 각 사건 사실에",
        "그 카드가 어떻게 적용되는지를 정하는 표다. `성립 경로 요구`는 사기죄 성립 branch가",
        "통과하려면 필요한 상태일 뿐 사건의 정답을 미리 표시한 것이 아니다.",
        "",
        "`사용자 판정`에는 `S`(충족), `NS`(불충족), `U`(미확인), `EDIT`(카드·계획 수정 필요)",
        "중 하나를 적는다. `U`가 하나라도 남으면 닫힌 사건에서 Scallop은 성립을 확정하지 않는다.",
        "",
        "4번 사건은 ‘아직 생산하지 않았다’는 객관적 사실과 ‘이미 생산하고 있다’는 A의 말을",
        "명시적으로 대비하도록 수정했다. 1번 사건 문구는 변경하지 않았다.",
        "",
    ]

    for case_number, case in enumerate(case_set.get("cases", []), start=1):
        validate_fraud_case(case)
        synthetic_graph = {"profiles": case["required_profiles"]}
        plan = select_fraud_reasoning_plan(synthetic_graph, case=case)
        label = CASE_LABELS.get(case["case_id"], case["case_id"])
        lines.extend(
            [
                f"## {case_number}. {label}",
                "",
                f"- 사건 ID: `{case['case_id']}`",
                f"- 계획: `{plan['plan_id']}`",
                f"- 사건 사실: {case['case_text']}",
                "",
            ]
        )
        row_number = 0
        for unit in plan["units"]:
            question = render_reasoning_plan_text(unit["question_template"], case)
            lines.extend(
                [
                    f"### {unit['issue_template']}",
                    "",
                    f"검토 질문: {question}",
                    "",
                    "| 항목 | 카드 ID | 카드 명제 | 성립 경로 요구 | 사용자 판정 | 메모 |",
                    "|---|---|---|---|---|---|",
                ]
            )
            for plan_card in unit["cards"]:
                row_number += 1
                card_id = plan_card["card_id"]
                card = cards_by_id.get(card_id)
                if card is None:
                    raise ValueError(f"missing NormCard {card_id}")
                row_id = f"C{case_number}-{row_number:02d}"
                lines.append(
                    "| {row_id} | `{card_id}` | {proposition} | {required} |  |  |".format(
                        row_id=row_id,
                        card_id=card_id,
                        proposition=table_text(card["proposition"]),
                        required=STATUS_LABELS[plan_card["satisfied_when"]],
                    )
                )
            lines.append("")
        lines.extend(
            [
                "**사건 전체 허용 결론:** `established / not_established / undetermined / conflict`",
                "",
                "**사건 메모:**",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-set", type=Path, default=DEFAULT_CASE_SET)
    parser.add_argument("--norm-cards", type=Path, default=DEFAULT_NORM_CARDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = render_review(read_json(args.case_set), read_json(args.norm_cards))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
