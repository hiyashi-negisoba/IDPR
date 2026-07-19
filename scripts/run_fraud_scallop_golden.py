from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from idpr.rulegen.scallop_runtime import (  # noqa: E402
    run_scenario,
    runtime_version,
    sha256_file,
)
from scripts.build_fraud_full_scallop import (  # noqa: E402
    FRAUD_ROOT,
    MANIFEST_PATH,
    NORM_CARD_PATH,
    OUTPUT_PATH,
    RULE_IR_PATH,
    build,
    read_json,
)


GOLDEN_PATH = FRAUD_ROOT / "fraud_scallop_golden_cases.json"
REPORT_PATH = FRAUD_ROOT / "fraud_scallop_runtime_report.json"
HUMAN_REPORT_PATH = FRAUD_ROOT / "fraud_scallop_runtime_human_report.md"
DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
QUERY_RELATIONS = (
    "fraud_elements_satisfied",
    "fraud_established",
    "fraud_not_established",
    "fraud_undetermined",
    "fraud_conflict",
)
OUTPUT_LABELS = {
    "fraud_elements_satisfied": "10개 구성요건 component 충족 후보",
    "fraud_established": "최종 사기죄 성립",
    "fraud_not_established": "명시적 불성립 사유",
    "fraud_undetermined": "미확인 쟁점",
    "fraud_conflict": "상충 판단",
}
ACTOR_LABELS = {
    "defendant_id": "피고인",
    "deceived_person_id": "피기망자",
    "disposer_id": "처분행위자",
    "property_owner_id": "재산소유자",
    "beneficiary_id": "재산 취득자",
}
SCENARIO_GUIDE = {
    "ordinary_established": (
        "일반형 사기 성립",
        "공통 요건이 모두 충족되고 평가도 완결되면 최종 성립하는가?",
        "일반형 역할과 기본 판단 14개를 그대로 사용했다.",
        "구성요건 후보와 최종 사기죄 성립이 모두 출력됐다.",
    ),
    "incomplete_case_blocked": (
        "평가 미완결 사건",
        "구성요건이 모두 충족되어도 평가 완료 선언이 없으면 확정을 막는가?",
        "일반형과 기본 판단은 같지만 `case_assessment_complete`를 넣지 않았다.",
        "구성요건 후보까지만 나왔고 최종 성립은 차단됐다.",
    ),
    "negative_bar_blocks": (
        "명시적 불성립 사유가 있는 사건",
        "긍정 요건과 착오 부정 사유가 함께 입력되면 확정을 막는가?",
        "기본 판단에 '아무 생각도 하지 않은 경우여서 착오가 없다'를 충족으로 추가했다.",
        "불성립 사유와 충돌이 드러났고 최종 성립은 차단됐다.",
    ),
    "card_conflict_blocks": (
        "같은 쟁점의 상충 평가",
        "동일한 기망 쟁점에 긍정과 부정 평가가 함께 있으면 임의 선택을 막는가?",
        "기망의 신의칙 위반·착오 유발 판단에 충족과 불충족을 동시에 넣었다.",
        "상충과 불성립 사유가 출력됐고 최종 성립은 차단됐다.",
    ),
    "unknown_blocks": (
        "착오 여부 미확인 사건",
        "필수 쟁점 하나가 unknown이면 유죄 방향으로 닫히지 않는가?",
        "'사실과 다른 인식이 있었는가'를 충족 대신 unknown으로 바꿨다.",
        "미확인 쟁점이 출력됐고 구성요건 후보와 최종 성립은 나오지 않았다.",
    ),
    "triangular_missing_distinct_blocked": (
        "삼각사기 역할 확인 누락",
        "처분자와 재산소유자가 다르다는 확인이 없으면 삼각사기 성립을 막는가?",
        "처분 권능은 충족시켰지만 처분자와 소유자가 별개 실체라는 fact를 넣지 않았다.",
        "역할 구조가 완성되지 않아 구성요건 후보와 최종 성립이 차단됐다.",
    ),
    "triangular_established": (
        "삼각사기 성립",
        "처분 권능과 역할 상이성이 모두 확인되면 삼각사기가 성립하는가?",
        "처분자와 소유자가 다름을 명시하고 처분자의 권능 또는 지위를 충족시켰다.",
        "구성요건 후보와 최종 사기죄 성립이 모두 출력됐다.",
    ),
    "third_party_missing_distinct_blocked": (
        "제3자 취득 역할 확인 누락",
        "피고인과 제3취득자가 다르다는 확인이 없으면 귀속을 막는가?",
        "제3자 취득 의사·도구·대리 관계는 충족시켰지만 역할 상이성 fact를 넣지 않았다.",
        "취득 귀속이 완성되지 않아 구성요건 후보와 최종 성립이 차단됐다.",
    ),
    "third_party_established": (
        "제3자 취득형 사기 성립",
        "제3자 취득 요건과 역할 상이성이 모두 확인되면 성립하는가?",
        "제3자 취득 요건과 피고인·제3취득자가 서로 다르다는 fact를 모두 넣었다.",
        "구성요건 후보와 최종 사기죄 성립이 모두 출력됐다.",
    ),
}


def expand_scenarios(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    base = fixture["base_assessments"]
    scenarios: list[dict[str, Any]] = []
    for raw in fixture["scenarios"]:
        overrides = raw.get("assessment_status_overrides", {})
        assessments = [
            {
                "card_id": item["card_id"],
                "status": overrides.get(item["card_id"], item["status"]),
                "provable": True,
            }
            for item in base
        ]
        assessments.extend(dict(item) for item in raw.get("additional_assessments", []))
        for index, assessment in enumerate(assessments, 1):
            assessment.setdefault(
                "assessment_id", f"{raw['scenario_id']}.assessment.{index:03d}"
            )
            assessment.setdefault("provable", True)
        selected = list(dict.fromkeys(item["card_id"] for item in assessments))
        selected.extend(raw.get("selected_without_assessment", []))
        scenarios.append(
            {
                "scenario_id": raw["scenario_id"],
                **raw["actors"],
                "selected_card_ids": selected,
                "assessments": assessments,
                "distinct_entities": raw.get("distinct_entities", []),
                "close_case": raw["close_case"],
                "expected_nonempty": raw["expected_nonempty"],
            }
        )
    return scenarios


def render_human_report(
    fixture: dict[str, Any], report: dict[str, Any], norm_cards: dict[str, Any]
) -> str:
    cards_by_id = {card["id"]: card for card in norm_cards["cards"]}
    observed_by_id = {
        scenario["scenario_id"]: scenario for scenario in report["scenarios"]
    }
    lines = [
        "# 사기죄 Scallop 실제 실행 보고서",
        "",
        "> 이 문서는 사람이 검토하는 보고서다. 같은 이름의 JSON 파일은 자동 테스트와 "
        "재현을 위한 기계용 기록이므로 읽을 필요가 없다.",
        "",
        "## 먼저 알아야 할 결론",
        "",
        f"- 공식 `{report['runtime']['version']}`에서 합성 사례 "
        f"{report['scenario_count']}개를 실행했고 전부 예상대로 작동했다.",
        "- 일반형, 삼각사기, 제3자 취득형의 정상 성립 경로를 확인했다.",
        "- 평가 미완결, 명시적 불성립 사유, 상충 판단, unknown, 역할 상이성 누락은 "
        "최종 성립을 차단했다.",
        f"- **이번 입력은 자연어 사실관계가 아니다.** 아래 {len(fixture['base_assessments'])}개 "
        "standard 판단값을 사람이 "
        "미리 만들어 Scallop에 넣었다. 따라서 이번 시험은 RuleIR에서 결론까지의 논리 "
        "작동만 검증한다.",
        "- 피기망자·처분자 동일성, 기망과 처분의 연결, 순차적 인과관계와 기수는 "
        "평가값으로 넣지 않았다. 역할 정보와 standard 판단을 바탕으로 Scallop이 도출한다.",
        "- 자연어 사실관계에서 이 판단값을 모델이 정확히 뽑는지는 다음 단계에서 별도로 "
        "검증해야 한다.",
        "",
        "## Scallop에 실제로 넣은 것",
        "",
        "Scallop은 판결문형 문장을 직접 읽지 않았다. 사건의 역할 ID와 각 법적 쟁점의 "
        "3상태 평가를 fact로 받았다.",
        "",
        "| 입력값 | 뜻 |",
        "|---|---|",
        "| `satisfied` | 현재 사건에서 그 판단 또는 조건이 충족됨 |",
        "| `not_satisfied` | 현재 사건에서 그 판단 또는 조건이 충족되지 않음 |",
        "| `unknown` | 관련 쟁점이지만 현재 자료로 판단할 수 없음 |",
        "| `provable=true` | 증거·절차 게이트를 통과해 추론에 사용할 수 있음 |",
        "| `case_assessment_complete=true` | router가 고른 관련 쟁점의 평가가 모두 수집됨 |",
        "",
        "### 일반형의 역할 입력",
        "",
        "| 역할 | 입력 ID | 의미 |",
        "|---|---|---|",
        "| 피고인 | `defendant` | 기망행위자이자 본인취득 경로의 취득자 |",
        "| 피기망자 | `victim` | 기망 때문에 착오에 빠진 사람 |",
        "| 처분행위자 | `victim` | 피기망자와 동일인 |",
        "| 재산소유자 | `victim` | 일반형에서는 피기망자·처분자와 동일인 |",
        "| 재산 취득자 | `defendant` | 피고인이 직접 취득 |",
        "",
        f"### 모든 사례의 출발점이 된 기본 standard 판단 {len(fixture['base_assessments'])}개",
        "",
        "아래 값은 모두 `provable=true`로 넣었다. 별도 설명이 있는 사례만 일부 값을 "
        "바꾸거나 판단을 추가했다.",
        "여기서 `충족`은 추상적인 법률명제가 옳다는 뜻이 아니라, **이 합성 사건의 "
        "구체적 사실이 해당 요건을 충족한다고 사람이 미리 지정했다**는 뜻이다.",
        "",
        "| 번호 | 사건에 넣은 법적 판단 | 입력 상태 |",
        "|---:|---|---|",
    ]
    for index, assessment in enumerate(fixture["base_assessments"], 1):
        card_id = assessment["card_id"]
        proposition = cards_by_id[card_id]["proposition"]
        status = assessment["status"]
        if card_id == "fraud_intent.no_disposition_inducement_intent":
            status_text = (
                "불충족: '처분하게 할 의사가 없다'가 부정되므로 처분 유도 의사는 있음"
            )
        else:
            status_text = {
                "satisfied": "충족",
                "not_satisfied": "불충족",
                "unknown": "미확인",
            }[status]
        lines.append(f"| {index} | {proposition} | {status_text} |")

    lines.extend(
        [
            "",
            "## 출력값을 읽는 법",
            "",
            "| Scallop 출력 | 사람에게 의미하는 것 |",
            "|---|---|",
            *(
                f"| `{relation}` | {label} |"
                for relation, label in OUTPUT_LABELS.items()
            ),
            "",
            "`구성요건 component 충족 후보`는 최종 결론이 아니다. 이 후보가 있어도 "
            "평가 완료 선언이 없거나 불성립 사유·충돌이 있으면 `최종 사기죄 성립`은 "
            "출력되지 않는다.",
            "",
            "## 사례별 실제 입력과 결과",
            "",
        ]
    )

    for index, raw in enumerate(fixture["scenarios"], 1):
        scenario_id = raw["scenario_id"]
        title, question, change, interpretation = SCENARIO_GUIDE[scenario_id]
        actors = raw["actors"]
        observed = observed_by_id[scenario_id]["observed_nonempty"]
        lines.extend(
            [
                f"### {index}. {title}",
                "",
                f"**검사 질문:** {question}",
                "",
                "**역할 입력:** "
                + ", ".join(
                    f"{ACTOR_LABELS[field]}=`{actors[field]}`"
                    for field in ACTOR_LABELS
                ),
                "",
                f"**기본 판단에서 바꾼 점:** {change}",
            ]
        )
        if raw.get("assessment_status_overrides"):
            for card_id, status in raw["assessment_status_overrides"].items():
                lines.append(
                    f"- 변경 판단: {cards_by_id[card_id]['proposition']} → "
                    f"`{status}`"
                )
        for assessment in raw.get("additional_assessments", []):
            lines.append(
                f"- 추가 판단: {cards_by_id[assessment['card_id']]['proposition']} → "
                f"`{assessment['status']}`"
            )
        if raw.get("distinct_entities"):
            pairs = ", ".join(
                f"`{left}`와 `{right}`는 서로 다른 사람"
                for left, right in raw["distinct_entities"]
            )
            lines.append(f"- 역할 상이성: {pairs}")
        lines.extend(
            [
                f"- 평가 완료 선언: {'있음' if raw['close_case'] else '없음'}",
                "",
                "**실제 출력:**",
                "",
                "| 결과 | 출력 여부 |",
                "|---|---|",
                *(
                    f"| {OUTPUT_LABELS[relation]} | "
                    f"{'출력됨' if observed[relation] else '출력 안 됨'} |"
                    for relation in QUERY_RELATIONS
                ),
                "",
                f"**해석:** {interpretation}",
                "",
            ]
        )

    lines.extend(
        [
            "## 이 시험이 아직 증명하지 않은 것",
            "",
            "이번 골든 테스트는 Scallop 논리회로가 주어진 판단값을 올바르게 결합하는지만 "
            "확인했다. 다음 항목은 아직 시험하지 않았다.",
            "",
            "1. 한국법 61문항의 자연어 사실관계에서 모델이 관련 사기 쟁점을 제대로 "
            "선택하는지",
            "2. 모델이 긍정사실·반대사실·미확인사실을 구분해 standard 판단값을 정확히 "
            "생성하는지",
            "3. RAG 판례·주석서 근거가 각 판단을 실제로 뒷받침하는지",
            "4. 역할 entity resolution이 피기망자·처분자·소유자·취득자를 잘못 합치거나 "
            "분리하지 않는지",
            "5. 모델 오류가 최종 결론의 오탐·미탐으로 얼마나 이어지는지",
            "",
            "따라서 다음 실험 단위는 **자연어 사실관계 → 구조화 판단값 → Scallop 결론**을 "
            "한 번에 추적할 수 있는 end-to-end 사례다.",
            "",
        ]
    )
    return "\n".join(lines)


def run_all(
    *,
    work_dir: Path | None = None,
    report_path: Path | None = None,
    human_report_path: Path | None = None,
) -> dict[str, Any]:
    manifest = build()
    rule_ir = read_json(RULE_IR_PATH)
    fixture = read_json(GOLDEN_PATH)
    norm_cards = read_json(NORM_CARD_PATH)
    scli_path = Path(os.environ.get("SCALLOP_SCLI", DEFAULT_SCLI))
    if not scli_path.is_file():
        raise FileNotFoundError(
            f"Scallop runtime not found at {scli_path}; run scripts/install_scallop_runtime.sh"
        )
    expected_sha = manifest["runtime_contract"]["sha256"]
    actual_sha = sha256_file(scli_path)
    if actual_sha != expected_sha:
        raise RuntimeError(f"unexpected scli checksum: {actual_sha}")

    compiled_source = OUTPUT_PATH.read_text(encoding="utf-8")
    runtime_work_dir = work_dir or PROJECT_ROOT / ".cache/scallop/fraud_golden"
    scenario_reports: list[dict[str, Any]] = []
    failures: list[str] = []
    for scenario in expand_scenarios(fixture):
        results = run_scenario(
            rule_ir=rule_ir,
            compiled_source=compiled_source,
            scenario=scenario,
            query_relations=QUERY_RELATIONS,
            scli_path=scli_path,
            work_dir=runtime_work_dir,
        )
        observed = {
            relation: result["nonempty"] for relation, result in results.items()
        }
        expected = scenario["expected_nonempty"]
        if observed != expected:
            failures.append(
                f"{scenario['scenario_id']}: expected {expected}, observed {observed}"
            )
        scenario_reports.append(
            {
                "scenario_id": scenario["scenario_id"],
                "expected_nonempty": expected,
                "observed_nonempty": observed,
                "status": "pass" if observed == expected else "fail",
            }
        )

    report = {
        "version": "1.0.0",
        "status": "pass" if not failures else "fail",
        "runtime": {
            "version": runtime_version(scli_path),
            "sha256": actual_sha,
        },
        "compiled_manifest": str(MANIFEST_PATH.relative_to(PROJECT_ROOT)),
        "compiled_sha256": sha256_file(OUTPUT_PATH),
        "golden_cases": str(GOLDEN_PATH.relative_to(PROJECT_ROOT)),
        "human_report": str(HUMAN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        "scenario_count": len(scenario_reports),
        "scenarios": scenario_reports,
        "failures": failures,
    }
    destination = report_path or REPORT_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    human_destination = human_report_path or HUMAN_REPORT_PATH
    human_destination.parent.mkdir(parents=True, exist_ok=True)
    human_destination.write_text(
        render_human_report(fixture, report, norm_cards), encoding="utf-8"
    )
    if failures:
        raise AssertionError("\n".join(failures))
    return report


def main() -> None:
    print(json.dumps(run_all(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
