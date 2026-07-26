"""결정 B-2 사용자 검토 반영 — 강등·중복병합·질의문 수정 (v7 → v8).

1부 32건 중 11건에 코멘트가 달렸고 2부 면제 12건은 전부 승인됐다. 코멘트는 승인할 문안이
아니라 해석 입력이므로 취지를 읽어 직접 반영한다.

**강등 4장 + 중복병합 1장**
  18 사후 반환의사 — "있어도 상관없이 유죄라는 취지인데 굳이 이렇게 꼬아야 할까, 없어도 될 것"
  20 범행 전 상계정산 — "특별한 사정이라는 게 애매하다, 이 카드도 애매하다"
  23 수분양권 위임 — "사실상 위(22)랑 중복"  → 일반 규칙 22를 남기고 구체사안 23을 내린다
  26 법인 운영권 양도 청탁 — "너무 구체적이고 지엽적인 케이스"
  13 다른 원인에 의한 교부 — "중복 인정" → 같은 조건을 묻는 11을 남긴다

**질의문 수정 3건**
  2  명의신탁 — "대외적 소유명의보다 법률상 소유자로 표현하는 게 낫다"
  10 권리행사 — "실제 맥락인지 확인해야 할 듯" → 원문 확인 결과 초안이 원문에 없는 요건
     (채권액 비교)을 집어넣었다. 원문은 "행위가 권리행사인 경우"라고만 한다.
  22 개별 위임요소 — "약정이라는 말은 없다, 원본 워딩을 그대로 옮기라"

**질의 불요로 이동 1장**
  25 행정절차상 불법 — "그래도 괜찮다=죄가 인정된다는 거잖아, 이것도 좀 이상해". 지적이 맞다.
     이 카드는 면허 미취득을 이유로 업무성을 부정하는 항변을 차단하는 규칙이고, 분기가 되는
     사실은 같은 절 `illegal_business`가 묻는 "사무 내용 자체의 위법성"이다. 모델에 물을 사실이
     없으므로 deterministic_rule로 내리고 질의를 면제한다.

**확인만 하고 그대로 두는 것 2건** — 12(극성 방향), 27(대칭)은 원장에 판단 근거를 남긴다.

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

DEMOTE: dict[str, str] = {
    "art355_sec4_1.later_return_intent_irrelevant":
        "사후 반환·변상 의사가 있어도 유죄라는 취지의 카드다. 규칙으로 세우면 '그 사정이 있었다'를 "
        "물어 놓고 결론에는 영향을 주지 않는 질의가 되므로, 카드를 두는 이득이 없다(사용자 판단).",
    "art355_sec4_1.preoffense_setoff_only":
        "'범행 전 상계정산 등의 특별한 사정'이 무엇인지 명제 안에서 특정되지 않아 물을 사실이 "
        "확정되지 않는다(사용자 판단: 카드 자체가 애매).",
    "art355_sec5_2.pre_sale_right_delegated_management_exception":
        "수분양권이라는 구체사안에서 같은 판단을 반복한다. 일반 규칙인 "
        "art355_sec5_2.individual_delegation_exception을 남긴다(사용자: 사실상 중복).",
    "art357_sec3_2.corporate_control_transfer_exception":
        "사회복지법인·학교법인 운영권 양도라는 지엽적 사안에 한정된 판단이다(사용자 판단). "
        "구체사안 축 강등 기준과 같다.",
    "art350_sec7_2.completion.other_cause_disposition_attempt":
        "art350_sec5_2.no_fear_attempt와 같은 조건(교부의 원인이 외포가 아닌 다른 사정)을 묻고 "
        "같은 결론(미수)에 이른다. 근사중복으로 병합하고 no_fear_attempt를 남긴다(사용자: 중복 인정).",
}

MERGED_INTO = {
    "art350_sec7_2.completion.other_cause_disposition_attempt": "art350_sec5_2.no_fear_attempt",
    "art355_sec5_2.pre_sale_right_delegated_management_exception":
        "art355_sec5_2.individual_delegation_exception",
}

# card_id → (새 질의문, 발동방향, 수정 근거)
REVISE_QUERY: dict[str, tuple[str, str, str]] = {
    "art323_sec2_2.nominee_owner_not_subject": (
        "그 물건은 피고인이 명의신탁한 것이어서 법률상 소유자는 명의수탁자였다.",
        "satisfied",
        "'대외적인 소유 명의'를 '법률상 소유자'로 바꿨다(사용자). 권리행사방해죄의 객체는 자기의 "
        "물건이므로, 법률상 소유자가 수탁자면 신탁자에게는 자기 물건이 아니어서 주체가 되지 않는다."),
    "art350_sec4_2.right_exercise_exception": (
        "피고인이 고지한 해악의 내용은 피고인이 가진 권리를 행사하는 것이었다.",
        "satisfied",
        "초안은 원문에 없는 요건(채권액과 요구액의 비교)을 넣었다. 원문은 '다만 행위가 권리행사인 "
        "경우에는 위법성이 조각될 수 있다'뿐이므로 권리행사라는 사실만 묻는다."),
    "art355_sec5_2.individual_delegation_exception": (
        "그 계약에는 단순한 권리이전이나 담보설정을 넘어 상대방의 재산에 대한 관리·처리에 관한 "
        "요소가 있었다.",
        "satisfied",
        "'약정'은 원문에 없는 말이다(사용자). 원문의 '위임 등 신임관계를 인정할 개별 요소'를 "
        "관리·처리 요소의 존재로 옮겼다."),
}

TO_WAIVER: dict[str, str] = {
    "art356_sec2_2.administrative_illegality":
        "면허·인가 미취득을 이유로 업무성을 부정하는 항변을 차단하는 규칙이다. 실제로 업무성을 "
        "가르는 사실은 같은 절 art356_sec2_2.illegal_business가 묻는 '사무 내용 자체의 위법성'이고, "
        "이 카드는 그 판정 결과에 규칙을 적용한다(사용자: 면허 미취득을 물어 죄를 인정하는 흐름이 "
        "이상하다). deterministic_rule로 내리고 질의를 면제한다.",
}

CONFIRMED: dict[str, str] = {
    "art350_sec5_3.complete_suppression_robbery":
        "극성 방향은 초안대로 맞다 — 질의('협박 정도가 반항을 억압할 정도였다')가 참이면 이 카드가 "
        "발동해 강도죄 성립으로 간다. 혼동은 표기에서 왔다. 이 카드는 공갈죄 관점에서 배제 규칙"
        "(polarity=exception)이면서 문언으로는 강도죄 성립을 긍정하므로, '카드 발동'이 무엇을 "
        "뜻하는지가 모호했다. 이후 문서에는 발동 시 결론(강도죄 성립·공갈죄 배제)을 함께 적는다.",
    "art357_sec3_2.giver_not_necessarily_liable":
        "대칭은 이미 확보돼 있다 — 증재자 관점 카드 art357_sec4.giver_view_justification이 결정B에서 "
        "질의문 승인을 받았고(질의: '증재자는 자신이 한 청탁이 부정한 청탁이라는 점을 인식하고 "
        "있었다'), 이 카드는 수재자 관점을 담당한다. 두 카드가 짝이므로 이 카드의 질의문은 "
        "그대로 둔다.",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    core = read_json(PROP / "property_core_set_final_v7.json")
    rows = {row["card_id"]: row for row in core["rows"]}
    drafts = read_json(PROP / "property_exception_query_drafts.json")
    ledger: list[dict[str, Any]] = []
    stats: Counter = Counter()

    for card_id, reason in DEMOTE.items():
        row = rows[card_id]
        if row["final_role"] in ("context_only", "deferred_track"):
            raise SystemExit(f"{card_id}는 이미 core가 아니다")
        row.update(final_role="context_only", demoted_at="decision_b2", reason=reason)
        entry = {"card_id": card_id, "kind": "demote", "reason": reason}
        if card_id in MERGED_INTO:
            entry["merged_into"] = MERGED_INTO[card_id]
            stats["merged"] += 1
        ledger.append(entry)
        stats["demoted"] += 1

    for card_id, note in TO_WAIVER.items():
        row = rows[card_id]
        if row["final_role"] != "standard_input":
            raise SystemExit(f"{card_id}는 standard_input이 아니다")
        row.update(final_role="deterministic_rule", role_changed_at="decision_b2",
                   role_change_reason=note)
        ledger.append({"card_id": card_id, "kind": "to_deterministic_rule", "reason": note})
        stats["to_deterministic_rule"] += 1

    kept = [row for row in rows.values()
            if row["final_role"] not in ("context_only", "deferred_track")]
    core["rows"] = list(rows.values())
    core["version"] = "8.0.0"
    core["supersedes"] = "property_core_set_final_v7.json"
    core["counts"]["core_final"] = len(kept)
    core["counts"]["demoted_decision_b2"] = stats["demoted"]
    write_json(PROP / "property_core_set_final_v8.json", core)

    # 질의문 최종 — 강등·면제분 제거, 수정 3건 반영
    items, waived = [], list(drafts["no_query_needed"])
    for item in drafts["items"]:
        card_id = item["card_id"]
        if card_id in DEMOTE:
            continue
        if card_id in TO_WAIVER:
            waived.append({"card_id": card_id, "proposition": item["proposition"],
                           "reason": TO_WAIVER[card_id]})
            continue
        if card_id in REVISE_QUERY:
            query, direction, note = REVISE_QUERY[card_id]
            ledger.append({"card_id": card_id, "kind": "revise_query",
                           "from": item["neural_query"], "to": query, "reason": note})
            stats["query_revised"] += 1
            item = {**item, "neural_query": query,
                    "card_status_when_query_satisfied": direction,
                    "authoring_note": note}
        item = {**item, "human_review": {"decision": "approved", "approved_query":
                                         item["neural_query"], "notes": None}}
        items.append(item)

    for card_id, note in CONFIRMED.items():
        ledger.append({"card_id": card_id, "kind": "confirmed_as_drafted", "reason": note})
        stats["confirmed"] += 1

    write_json(PROP / "property_exception_query_final.json", {
        "version": "2.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": "property_exception_query_drafts.json",
        "basis": "결정B2 사용자 검토(2026-07-25) 반영",
        "counts": {"queries": len(items), "waivers": len(waived)},
        "status": "user_review_complete",
        "items": items,
        "no_query_needed": waived,
    })

    write_json(PROP / "결정B2_반영원장.json", {
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "결정B2_예외형질의문승인.md (사용자 코멘트 11건 / 면제 12건 전부 승인)",
        "stats": dict(stats), "entries": ledger,
    })

    print(f"강등 {stats['demoted']}장(그중 중복병합 {stats['merged']}) / "
          f"질의 면제 이동 {stats['to_deterministic_rule']} / 질의문 수정 {stats['query_revised']}")
    print(f"재산죄 core {len(kept)}장 (v7 427장)")
    print(f"  역할 {Counter(row['final_role'] for row in kept).most_common()}")
    print(f"질의문 {len(items)}건 / 면제 {len(waived)}건")


if __name__ == "__main__":
    main()
