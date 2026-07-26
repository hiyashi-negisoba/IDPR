"""재산죄 RuleIR 생성 preflight 10항목 (승인용) — API 0회.

사기 RuleIR이 통과했던 게이트와 같은 형식이다(`run_fraud_full_rule_ir_generation.py`의
`EXPECTED_REVIEW_IDS`). 항목마다 제안·근거를 붙여 사용자 승인을 받고, 승인 없이는 생성을
실행하지 않는다.

사기와 달라지는 지점이 셋이다.
  · 단위가 11개다(죄명 9 + 공유 모듈 2) → 단위당 1콜, 단위별 출력 술어가 다르다.
  · 가중유형을 기본범과 분리해 플래그로 판정한다(사용자 요청, `rulegen_rule_ir_units.md` §3.1).
  · 공유 모듈(친족상도례·업무자 신분)이 브리지 술어로 죄명 규칙집합에 붙는다. 친족상도례 배선은
    A4 절차 레이어로 이월했으므로 이번 생성에서는 **브리지 술어를 배출하는 쪽까지만** 만든다.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"
UNITS = PROP / "rule_ir_units"
UNIT_MANIFEST = PROP / "rule_ir_unit_manifest.json"
QUERY_FINAL = (PROP / "property_negative_query_final.json",
               PROP / "property_exception_query_final.json",
               PROP / "supplement_query_final.json")
OUT_QUEUE = PROP / "rule_ir_prep_review_queue.json"
OUT_DOC = PROP / "RuleIR_preflight_10항목.md"

# 단위 → 행위자 역할 슬롯
ACTOR_ROLES: dict[str, list[str]] = {
    "theft": ["defendant_id", "owner_id", "possessor_id"],
    "robbery": ["defendant_id", "coerced_person_id", "owner_id", "possessor_id"],
    "extortion": ["defendant_id", "coerced_person_id", "disposer_id", "owner_id"],
    "embezzlement": ["defendant_id", "entrustor_id", "owner_id"],
    "breach_of_trust": ["defendant_id", "principal_id", "beneficiary_id"],
    "breach_of_trust_bribe": ["receiver_id", "giver_id", "principal_id"],
    "lost_property_embezzlement": ["defendant_id", "owner_id"],
    "property_damage": ["defendant_id", "owner_id"],
    "interference_with_exercise_of_right": ["defendant_id", "right_holder_id"],
    "occupational_status": ["defendant_id"],
    "relative_property_crime_exception": ["defendant_id", "owner_id", "possessor_id"],
}

# 단위 → 가중유형 플래그 (kind, 근거 조문, 전제조건)
AGGRAVATION: dict[str, list[tuple[str, str, str]]] = {
    "theft": [
        ("nighttime_residential", "제330조", "야간 침입 + 주거 등"),
        ("special", "제331조", "야간 손괴 침입 또는 흉기휴대·합동"),
        ("habitual", "제332조", "절도 습벽의 발현"),
    ],
    "robbery": [
        ("special", "제334조", "야간 주거침입 또는 흉기휴대·합동"),
        ("quasi", "제335조", "절도 기수 후 탈환방지·체포면탈·증거인멸 목적 폭행·협박"),
        ("injury", "제337조", "강도의 기회에 상해 — 치상은 폭행의 고의를 전제로 한다"),
        ("death", "제338조", "강도의 기회에 살해 — 치사는 폭행의 고의를 전제로 한다"),
        ("preparation", "제343조", "강도 목적의 예비·음모"),
    ],
    "embezzlement": [("occupational", "제356조", "업무자 신분 — 공유 모듈이 배출")],
    "breach_of_trust": [("occupational", "제356조", "업무자 신분 — 공유 모듈이 배출")],
}

SHARED_MODULES = ("occupational_status", "relative_property_crime_exception")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def item(review_id: str, topic: str, proposal: str, rationale: str,
         detail: list[str] | None = None) -> dict[str, Any]:
    return {
        "review_id": f"property.rule_ir.prep.{review_id}",
        "topic": topic,
        "proposal": proposal,
        "rationale": rationale,
        "detail": detail or [],
        "agent_recommendation": "approve",
        "human_review": {"review_id": f"property.rule_ir.prep.{review_id}",
                         "decision": None, "notes": None, "status": "pending"},
    }


def main() -> None:
    manifest = read_json(UNIT_MANIFEST)
    units = {unit["issue_tag"]: unit for unit in manifest["units"]}
    total_cards = manifest["counts"]["cards"]
    queries: dict[str, str] = {}
    waived: set[str] = set()
    for path in QUERY_FINAL:
        payload = read_json(path)
        for entry in payload["items"]:
            queries[entry["card_id"]] = entry["neural_query"]
        waived |= {entry["card_id"] for entry in payload["no_query_needed"]}

    cards_by_unit = {tag: read_json(UNITS / f"{tag}.json")["cards"] for tag in units}
    standard_cards = {tag: [c for c in cards if c["formalization"] == "standard_input"]
                      for tag, cards in cards_by_unit.items()}
    negative_standard = {tag: [c for c in cards if c["polarity"] in ("negative", "exception")]
                         for tag, cards in standard_cards.items()}
    uncovered = sorted(card["id"] for cards in negative_standard.values() for card in cards
                       if card["id"] not in queries and card["id"] not in waived)

    items = [
        item("scope",
             "core_scope",
             f"검토완료 core **{total_cards}장**만 RuleIR 입력으로 쓴다. context_only로 내린 카드"
             "(구체사안·죄수·공범총칙·타법률·판단지침형·증명소송법)와 이중매매 별도트랙 21장은 "
             "제외한다.",
             "구체 사안과 학설을 실행 규칙으로 되돌리지 않는다. 사기 트랙과 같은 기준이며, "
             "제외분은 RAG 문맥으로 남아 착안사항 생성에만 쓰인다.",
             [f"{tag}: {unit['cards']}장" for tag, unit in units.items()]),
        item("unit_granularity",
             "generation_unit",
             "단위는 **죄명 9 + 공유 모듈 2 = 11개**이고 단위마다 RuleIR 1콜을 낸다. 조문 단위로 "
             "묶지 않는다.",
             "검증기가 RuleIR과 NormCardSet의 `issue_tag` 일치를 요구하고 라우터가 쟁점 태그로 "
             "규칙집합을 고른다. 제355조를 한 단위로 두면 '횡령 쟁점'에서 배임 요건이 함께 발화한다. "
             "제355조는 항 표시로, 제356조는 절 구조로 분할했다(혼합 0장).",
             ["theft·robbery는 가중유형 조문을 같은 단위에 담는다(기본 요건 카드 복제 방지)",
              "공유 모듈은 죄명이 아니라 수정요소다 — 업무자 신분(가중), 친족상도례(처벌·소추)"]),
        item("outputs",
             "required_output_predicates",
             "출력 술어를 3층으로 나눈다 — `<unit>_established`(기본범 성립) / "
             "`<unit>_aggravation(kind)`(가중 플래그) / `charge(label)`(죄명 확정). 여기에 "
             "`<unit>_not_established` · `<unit>_undetermined` · `<unit>_conflict`를 둔다.",
             "결론이 비지 않게 하려면 미확정과 불성립을 구별해야 한다(무죄와 미완결의 분리). "
             "가중 플래그가 꺼지면 자동으로 기본범으로 내려간다.",
             [f"{tag}: {tag}_established({', '.join(ACTOR_ROLES[tag])})"
              for tag in units if tag not in SHARED_MODULES]),
        item("aggravation",
             "aggravation_flags",
             "단위별 가중유형을 열거하고 각 플래그의 전제조건을 명시한다(사용자 요청 2026-07-25). "
             "열거된 kind 외에는 생성하지 않는다.",
             "가중유형을 기본범과 섞으면 요건이 한 벌로 뭉쳐 어느 카드가 어느 유형을 켜는지 "
             "추적할 수 없다. 결과적 가중범(치상·치사)은 폭행의 고의를 전제조건으로 요구한다.",
             [f"{tag} — {kind}({article}): {condition}"
              for tag, entries in AGGRAVATION.items()
              for kind, article, condition in entries]),
        item("actor_roles",
             "actor_roles",
             "단위별 행위자 역할 슬롯을 위와 같이 고정한다. 슬롯이 다르면 다른 사람이라는 뜻이 "
             "아니고(한 사람이 여러 슬롯을 채울 수 있다), 같은 변수로 묶어야 하는 곳만 규칙에서 "
             "명시한다.",
             "강도는 폭행의 상대방이 소유자·점유자와 다를 수 있다 — core 카드 "
             "`art333_sec2_4.target_person_obstructing_taking`(폭행 상대방은 탈취에 장애가 되는 "
             "자이면 된다)이 이 분리를 요구한다. 공갈은 외포된 자와 처분한 자를 나눈다.",
             [f"{tag}: {', '.join(roles)}" for tag, roles in ACTOR_ROLES.items()]),
        item("bridge_predicate",
             "shared_module_interface",
             "죄명 규칙집합은 공통 브리지 술어 "
             "`property_crime_established(case_id, crime_id, defendant_id, owner_id, possessor_id)`를 "
             "배출한다. 업무자 신분 모듈은 `occupational_status_established`를 배출해 횡령·배임 "
             "가중 플래그가 참조한다. **친족상도례 규칙은 이번 생성에서 만들지 않는다** — 배출하는 "
             "쪽까지만 만들고 받는 쪽은 A4 절차 레이어에서 쓴다(사용자 결정).",
             "친족상도례는 성립이 아니라 처벌·소추 층이고 준용 범위가 죄명마다 다르다. 한 곳에서 "
             "관리해야 개정·헌재 결정 반영이 흩어지지 않는다.",
             ["친족 모듈 카드 25장은 NormCardSet으로 확정해 두고 RuleIR 생성은 보류한다"]),
        item("neural_state",
             "standard_input_wiring",
             "`standard_input` 카드는 승인된 질의문으로만 neural에 배선한다. 부정형·예외형 명제는 "
             "모델에 그대로 보내지 않는다.",
             "부정형 명제를 그대로 물으면 이중부정이 되어 모델이 사실을 반대로 답한다. 결정 "
             "B·B-2·B-3에서 질의문과 발동 방향(satisfied/not_satisfied)을 확정했다.",
             [f"{tag}: standard_input {len(standard_cards[tag])}장 "
              f"(그중 부정형·예외형 {len(negative_standard[tag])}장)" for tag in units]
             + [f"질의문 승인 {len(queries)}건 / 질의 면제 {len(waived)}건",
                f"질의문 미보유 부정형: {len(uncovered)}건" if uncovered
                else "부정형 카드 전부 질의문 또는 면제를 보유한다"]),
        item("evidence_gate",
             "evidence_gate_and_negation",
             "commentary에서 온 모든 입력은 `provable(case_id, assessment_id)` 게이트를 통과해야 "
             "하고, 부정은 `case_assessment_complete` 게이트 이후 **최종 결론 스트라텀에서만** "
             "쓴다.",
             "사기 RuleIR과 같은 계약이다. 열린 세계에서 '증명되지 않음'을 '없음'으로 바꾸지 "
             "않으려는 것이고, 절차 레이어의 증거능력 gating이 이 게이트에 붙는다.",
             None),
        item("fewshot",
             "structural_exemplar",
             "사기 RuleIR(`fraud_full_rule_ir_rebuilt.json`)을 **구조 예시로만** 준다. 규칙·술어·"
             "결론을 복사하는 것을 금지한다.",
             "사기는 이미 계약을 통과한 유일한 완성 RuleIR이라 형식 참조로는 최적이다. 다만 내용을 "
             "옮기면 재산죄 카드에 없는 요건이 들어온다.",
             None),
        item("api_ceiling",
             "execution_ceiling",
             "단위 11개 × (terra 생성 + sol 비평) = 최대 22콜. terra `max_tokens=64000`, "
             "`reasoning_effort=low`. 추정 **$3.5**, 상한 $6에서 중단. **sbatch로 제출**한다.",
             "사기 실측 1회가 terra $0.17 + sol $0.43 = $0.60/88장이었고 재산죄 단위 평균은 44장이다. "
             "누적 $62.4/$100이므로 잔액에 여유가 있다.",
             ["오래 걸리는 작업은 sbatch(사용자 지시) — nohup은 고아 프로세스를 남긴다"]),
    ]

    OUT_QUEUE.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "issue_tags": sorted(units),
        "method": "사기 preflight와 같은 10항목 게이트 — 승인 없이는 생성하지 않는다",
        "counts": {"units": len(units), "cards": total_cards,
                   "queries_approved": len(queries), "queries_waived": len(waived)},
        "status": "pending_user_approval",
        "items": items,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# RuleIR 생성 preflight — 10항목 승인 요청",
        "",
        f"재산죄 core **{total_cards}장** / 죄명 단위 **{len(units)}개**(죄명 9 + 공유 모듈 2)로 "
        "RuleIR을 생성합니다. 사기 RuleIR이 통과했던 것과 같은 형식의 게이트입니다 — "
        "**10항목 승인 후에만 실행**합니다.",
        "",
        "| 단위 | 카드 | deterministic | standard | 부정형·예외형 |",
        "|---|---:|---:|---:|---:|",
    ]
    for tag, unit in units.items():
        roles = unit["roles"]
        lines.append(f"| `{tag}` | {unit['cards']} | {roles.get('deterministic_rule', 0)} | "
                     f"{roles.get('standard_input', 0)} | {len(negative_standard[tag])} |")
    lines += ["", "각 항목의 **판단:** 뒤에 승인/수정을 적어 주십시오.", "", "---", ""]
    for index, entry in enumerate(items, start=1):
        lines += [f"## {index}. {entry['topic']} (`{entry['review_id'].split('.')[-1]}`)", "",
                  f"**제안**: {entry['proposal']}", "",
                  f"**근거**: {entry['rationale']}", ""]
        if entry["detail"]:
            lines += ["<details><summary>상세</summary>", ""]
            lines += [f"- {line}" for line in entry["detail"]]
            lines += ["", "</details>", ""]
        lines += ["**판단:** ", ""]
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")

    print(f"preflight {len(items)}항목 / 단위 {len(units)} / 카드 {total_cards}")
    print(f"  질의문 승인 {len(queries)} / 면제 {len(waived)} / 미보유 {len(uncovered)}")
    if uncovered:
        print(f"  ⚠️ 질의문 미보유: {uncovered}")
    print(f"  → {OUT_QUEUE.relative_to(ROOT)}")
    print(f"  → {OUT_DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
