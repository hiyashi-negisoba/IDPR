"""결정 B-3 검토 반영 — 질의문 수정 3건 + 카드 재작성·병합 (v9 → v10).

사용자 지적 4건. 4번은 질의문 승인이고 별도 설계 요청(가중유형 on/off)이라 문서로 넘긴다.
나머지 3건은 모두 내 작성이 원문을 잘못 읽은 것이다.

**2번 `art332_sec1_1.different_offense_types`** — "절도 강도 사기라는 건 각 죄종을 번갈아 한 게
아니라 저 세 개가 상습성 가중조항을 가지고 있어서 포괄하여 설명하는 것"이라는 지적. 주석서 원문은
"상습성은 동종의 형태의 행위를 반복누행하는 습벽을 말하는 것이므로 예컨대 서로 유형을 달리하는
절도, 강도 및 사기 등을 반복한 경우에 절도의 상습성을 인정할 수 없다"이고, 바로 다음 문장이
"그러나 단순절도·야간주거침입절도·특수절도의 각 죄의 본체는 동종의 행위 유형인 절도행위이므로
포괄하여 하나의 상습범"으로 이어진다. 즉 이 카드가 담는 규칙은 **동종성 판단의 범위**다 —
절도 상습성은 절도행위의 반복에서만 나온다. 초안 질의문("전력과 범행이 절도·강도·사기 등 서로
다른 유형으로 이루어져 있다")은 강도 전과가 섞여 있으면 절도 상습성을 부정하는 것처럼 읽혀
과잉이다. 실제로는 그 경력을 상습성 근거에서 **제외**할 뿐이다. 명제와 질의문을 다시 쓴다.

**6번 `art333_sec2_3.lesser_threat_extortion`** — "반항억압 강제로 탈취가 있고 그보다 조금 더
약한 수준이라는 점이 질의문에 안 나타난다"는 지적. 정도의 상한이 빠졌다. "반항할 수 있는 상태"로
상한을 긍정형으로 넣는다.

**8번 `art333_sec3_1.real_estate_as_robbery_property_negative`** — "이것도 좀 이상해". 원문은
두 문장 한 세트다: "부동산도 도취죄의 객체인 재물에 해당하는지 견해가 대립되나 소극적으로 봄이
타당" + "폭행·협박으로 부동산에 관한 권리를 강취한 경우 이는 재산상 이익에 대한 강취로 보면
족하다". 카드를 둘로 쪼개 놓으니 "재물 아님"만 발동하고 그 다음(재산상 이익으로 처리)이 끊긴다.
학설선택에서 둘 다 살리기로 한 것도 실은 하나의 규칙이라는 뜻이므로 **병합**한다.

API 0회.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"
CORE_V9 = PROP / "property_core_set_final_v9.json"
CORE_V10 = PROP / "property_core_set_final_v10.json"
DRAFTS = PROP / "supplement_query_drafts.json"
OUT_QUERY = PROP / "supplement_query_final.json"
LEDGER = PROP / "결정B3_반영원장.json"

# card_id → (새 명제, 근거)
REWRITE: dict[str, tuple[str, str]] = {
    "art332_sec1_1.different_offense_types": (
        "절도의 상습성은 동종의 절도행위를 반복누행한 습벽에서 인정되므로, 강도·사기와 같이 "
        "죄종을 달리하는 범행 경력은 절도 상습성의 근거가 되지 않는다.",
        "초안 명제('유형이 다른 절도·강도·사기를 반복한 경우 절도의 상습성을 인정할 수 없다')는 "
        "죄종이 섞이면 절도 상습성이 부정되는 것처럼 읽힌다. 원문의 취지는 동종성 판단의 범위이고, "
        "다른 죄종의 경력을 상습성 근거에서 제외하는 것이다(사용자 지적)."),
}

# 병합: (흡수되는 카드, 남는 카드, 남는 카드의 새 명제, 근거)
MERGE: tuple[str, str, str, str] = (
    "art333_sec3_1.real_estate_rights_as_property_benefit",
    "art333_sec3_1.real_estate_as_robbery_property_negative",
    "부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않으므로, 폭행·협박으로 "
    "부동산에 관한 권리를 취득한 경우에는 재물의 강취가 아니라 재산상 이익의 강취로 본다.",
    "주석서 원문이 '재물 아님'과 '권리는 재산상 이익으로 본다'를 한 세트로 서술한다. 카드를 쪼개면 "
    "'재물 아님'만 발동하고 그 다음이 끊긴다(사용자 지적). 학설선택에서 둘 다 살리기로 한 것도 "
    "하나의 규칙이라는 뜻이므로 병합한다.",
)

# card_id → (새 질의문, 발동방향, 발동 시 결론, 근거)
REVISE_QUERY: dict[str, tuple[str, str, str, str]] = {
    "art332_sec1_1.different_offense_types": (
        "상습성의 근거로 함께 고려되는 범행 경력 중에 절도가 아닌 강도·사기 등 다른 죄종의 범행이 "
        "있다.",
        "satisfied",
        "그 다른 죄종의 경력은 절도 상습성의 근거에서 제외한다 — 절도 상습성은 절도행위(단순절도·"
        "야간주거침입절도·특수절도를 포함한다)의 반복만으로 판단한다",
        "초안은 죄종이 섞였다는 사실만으로 상습성을 부정하게 만들었다. 지금은 같은 사실을 묻되 "
        "발동 시 결론을 '근거에서 제외'로 정확히 적었다. 무엇이 동종인지는 짝 카드 "
        "`art332_sec1_1.aggregate_theft_types`가 채운다."),
    "art333_sec2_3.lesser_threat_extortion": (
        "그 폭행·협박은 피해자에게 두려움을 일으키는 정도였고, 피해자는 반항할 수 있는 상태에서 "
        "스스로 결정하여 재물을 건넸다.",
        "satisfied",
        "강도죄가 아니라 공갈죄가 성립한다",
        "정도의 상한이 초안에 없었다(사용자 지적). '반항할 수 있는 상태'로 상한을 긍정형으로 넣어 "
        "강도 쪽 core 카드(객관적 반항억압)와 상호배타적으로 걸리게 했다."),
    "art333_sec3_1.real_estate_as_robbery_property_negative": (
        "강취의 대상은 부동산 또는 부동산에 관한 권리다.",
        "satisfied",
        "재물의 강취가 아니라 재산상 이익의 강취로 처리한다(강도죄는 재산상 이익 취득으로 성립할 "
        "수 있다)",
        "카드 병합에 맞춰 질의문도 객체를 한 번에 묻는다. 초안('강취의 대상은 부동산이다')은 재물성 "
        "부정에서 멈춰 그 다음 처리가 끊겼다."),
}

AGGRAVATION_NOTE = (
    "4번 코멘트(가중적 구성요건을 기본범과 구별해 on/off로 판정하자)는 질의문 문제가 아니라 RuleIR "
    "출력 술어 설계 사항이라 `docs/research/rulegen_rule_ir_units.md` §3.1로 옮겨 preflight 항목으로 "
    "세웠다."
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    core = read_json(CORE_V9)
    rows = {row["card_id"]: row for row in core["rows"]}
    ledger: list[dict[str, Any]] = []
    stats: Counter = Counter()

    for card_id, (new, why) in REWRITE.items():
        row = rows[card_id]
        if row["final_role"] in ("context_only", "deferred_track"):
            raise SystemExit(f"{card_id}는 core가 아니다")
        ledger.append({"card_id": card_id, "kind": "rewrite",
                       "from": row["proposition"], "to": new, "reason": why})
        row["prev_proposition"] = row["proposition"]
        row["proposition"] = new
        row["rewrite_reason"] = why
        stats["rewritten"] += 1

    absorbed, kept_id, kept_proposition, merge_why = MERGE
    for card_id in (absorbed, kept_id):
        if rows[card_id]["final_role"] in ("context_only", "deferred_track"):
            raise SystemExit(f"{card_id}는 core가 아니다 — 병합할 수 없다")
    rows[absorbed].update(final_role="context_only", demoted_at="decision_b3",
                          reason=merge_why, merged_into=kept_id)
    kept = rows[kept_id]
    ledger.append({"card_id": kept_id, "kind": "merge",
                   "absorbed": absorbed, "from": kept["proposition"],
                   "to": kept_proposition, "reason": merge_why})
    kept["prev_proposition"] = kept["proposition"]
    kept["proposition"] = kept_proposition
    kept["rewrite_reason"] = merge_why
    # 병합된 카드의 인용까지 근거로 삼는다 — 조립 단계가 이 목록을 보고 source_refs를 합친다.
    kept["absorb_source_refs_from"] = [absorbed]
    stats["merged"] += 1

    live = [row for row in core["rows"]
            if row["final_role"] not in ("context_only", "deferred_track")]
    core["version"] = "10.0.0"
    core["supersedes"] = CORE_V9.name
    core["counts"]["core_final"] = len(live)
    core["counts"]["merged_decision_b3"] = stats["merged"]
    core["per_article_core"] = dict(sorted(Counter(r["article"] for r in live).items()))
    write_json(CORE_V10, core)

    drafts = read_json(DRAFTS)
    items = []
    for item in drafts["items"]:
        card_id = item["card_id"]
        if card_id == absorbed:
            continue
        if card_id in REVISE_QUERY:
            query, direction, conclusion, why = REVISE_QUERY[card_id]
            ledger.append({"card_id": card_id, "kind": "revise_query",
                           "from": item["neural_query"], "to": query, "reason": why})
            stats["query_revised"] += 1
            item = {**item, "neural_query": query,
                    "card_status_when_query_satisfied": direction,
                    "conclusion_when_fired": conclusion, "authoring_note": why}
        if card_id in REWRITE:
            item = {**item, "proposition": rows[card_id]["proposition"]}
        if card_id == kept_id:
            item = {**item, "proposition": kept_proposition}
        items.append({**item, "human_review": {"decision": "approved",
                                               "approved_query": item["neural_query"],
                                               "notes": None}})

    write_json(OUT_QUERY, {
        "version": "2.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": DRAFTS.name,
        "basis": "결정B3 사용자 검토(2026-07-25) 반영 — 질의문 수정 3건, 카드 병합 1건",
        "counts": {"queries": len(items), "waivers": len(drafts["no_query_needed"])},
        "status": "user_review_complete_pending_reconfirm",
        "reconfirm_items": sorted(REVISE_QUERY),
        "design_note": AGGRAVATION_NOTE,
        "items": items,
        "no_query_needed": drafts["no_query_needed"],
    })

    write_json(LEDGER, {
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "결정B3_보강조문_질의문승인.md (사용자 코멘트 4건)",
        "user_comments": {
            "art332_sec1_1.different_offense_types":
                "죄종을 번갈아 한 게 아니라 각 죄종이 상습 가중조항을 가져 포괄 설명한 것이다.",
            "art332_sec1_2.incidental-or-economic-theft-exception":
                "질의문은 승인. 가중적 구성요건을 기본범과 구별해 on/off로 판정하는 구조를 설계하라.",
            "art333_sec2_3.lesser_threat_extortion":
                "반항억압보다 약한 수준이라는 점이 질의문에 나타나지 않는다.",
            "art333_sec3_1.real_estate_as_robbery_property_negative": "이것도 좀 이상하다.",
        },
        "design_handoff": AGGRAVATION_NOTE,
        "stats": dict(stats), "entries": ledger,
    })

    print(f"재작성 {stats['rewritten']} / 병합 {stats['merged']} / 질의문 수정 {stats['query_revised']}")
    print(f"질의문 {len(items)}건 / 면제 {len(drafts['no_query_needed'])}건")
    print(f"재산죄 core {len(live)}장 (v9 481 → 병합으로 {len(live)})")


if __name__ == "__main__":
    main()
