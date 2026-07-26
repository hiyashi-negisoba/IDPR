"""결정 B 완료 반영 — v3 전수 검토(99건) 결과를 카드·질의문에 적용한다.

사용자는 v3을 끝까지 검토했다. 공란 = 승인, 기입 31건이 지적이다. 그중 9건은 카드 감사에서
해당 카드가 강등되어 자동 해소됐고, 남은 22건을 여기서 반영한다.

코멘트는 해석 입력이지 옮겨 적을 문안이 아니다. 취지를 반영해 문장은 에이전트가 쓴다.

처리 종류
  Q  질의문만 교체
  C  카드 명제까지 재작성
  D  카드 삭제
  A  답변만 필요했던 것 (변경 없음)

API 0회.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

DEC: dict[int, tuple] = {
    26: ("Q", "art366_sec4_1.intent_absence", None,
         "행위자는 그 물건이 타인의 소유라는 사실을 알고 있었다.", "not_satisfied",
         "예견가능성을 함께 물으면 모델이 미필적 예견을 놓친다. 소유 인식만 묻고 결과 예견은 "
         "고의 판단으로 넘긴다."),
    27: ("Q", "art329_sec2.theft_exception_ownership_or_self_possession", None,
         "취거한 재물은 타인이 점유하고 있는 타인의 재물이다.", "not_satisfied",
         "절도죄 객체의 정식 표현으로 통일."),
    28: ("Q", "art329_sec2_2.sole_custodian_coowned_property", None,
         "그 재물은 공동소유인 물건이고, 행위자는 그 물건을 보관하고 있던 사람이다.", "satisfied",
         "'공동점유가 아니라 단독보관'이라는 부정 대비를 걷고 보관자 지위만 묻는다."),
    35: ("C", "art355_sec3_3.simple_destruction_exception",
         "보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.",
         "행위자는 보관물을 손괴하였을 뿐 이를 자기 것으로 영득하거나 반환을 거부하지 않았다.",
         "not_satisfied",
         "구판은 '단순 손괴에 그치지 않고'로 써서 손괴와 영득 사이에 없는 연속성을 만들었다. "
         "횡령의 구성요건은 영득·반환거부이고 손괴는 그 연장선이 아니다."),
    39: ("D", "art328_sec3_2.full_adoption_ends_pre_adoption_kinship", None, None, None,
         "사용자 지시 — 카드 삭제."),
    43: ("Q", "art328_sec4_1.entrusted_property_owner_entrustor_both_required", None,
         "그 물건의 소유자와 위탁자가 서로 다른 사람이고, 범인은 소유자와 위탁자 모두와 "
         "친족관계에 있다.", "not_satisfied",
         "소유자와 위탁자가 분리된 사안에서만 발동해야 한다. 동일인인 경우까지 끌어오지 않도록 "
         "분리 사실을 발동조건에 명시."),
    44: ("Q", "art328_sec4_1.theft_owner_possessor_both_required", None,
         "피해물건의 소유자와 점유자가 서로 다른 사람이고, 범인은 소유자와 점유자 모두와 "
         "친족관계에 있다.", "not_satisfied",
         "43번과 같은 취지 — 소유자·점유자 분리 사안으로 발동조건을 좁힌다."),
    50: ("Q", "art334_sec2_1.weapon_direct_use_not_required", None,
         "행위자는 범행 당시 흉기를 지니고 있었고, 이를 제시하거나 겨누는 등으로 사용하지는 "
         "않았다.", "satisfied",
         "휴대만 물으면 모델이 '사용 안 했으니 이 카드는 아니다'로 빠진다. 이 카드가 겨냥하는 "
         "사안이 바로 미사용 사안이므로 미사용을 조건에 넣는다."),
    59: ("Q", "art350_sec5_2.fear_causation_required", None,
         "협박 또는 폭행과 외포 사이, 그리고 외포와 재산적 처분행위 사이에 각각 인과관계가 "
         "존재한다.", "not_satisfied", "두 인과관계가 각각 필요함을 드러냄."),
    64: ("Q", "art355_sec4_1.representative_corporate_debt_payment", None,
         "그 변제충당은 행위자가 가진 법적 권한 범위 안에서 이루어진 유효한 법률행위였다.",
         "not_satisfied",
         "'대표이사'는 판례 사안의 지위일 뿐이다. 권한 범위 내 유효한 행위인지로 일반화."),
    66: ("D", "art355_sec4_2.subsequent_return_not_negating_appropriation", None, None, None,
         "같은 조문 art355_sec4_1의 '소유자로서 처분하려는 의사가 있으면 사후 반환·변상 의사가 "
         "있어도 불법영득의사를 인정할 수 있다'와 중복이고, 단독으로는 반환의사를 물어 모델을 "
         "반대 방향으로 유도한다."),
    67: ("Q", "art355_sec4_3.accounting_only_adjustment", None,
         "그 처리는 장부상 정리에 그치지 않고 실제로 자금이 법인 밖으로 유출되었다.",
         "not_satisfied",
         "허위채용·변칙 장부정리처럼 그 자체로 부당한 처리여도 장부상 정리에 그치면 불법영득의사가 "
         "부정된다는 점을 카드 쪽에서 유지하고, 질의는 자금 유출 여부만 묻는다."),
    70: ("Q", "art355_sec4_3.slush_fund_concealment", None,
         "비자금을 장부에 은닉하거나 차명계좌로 관리한 사실에 더하여, 이를 개인 용도로 사용한 "
         "사정이 있다.", "not_satisfied",
         "은닉·차명관리라는 부정적 사정만으로는 부족하고 그 이상이 있어야 한다는 구조를 "
         "질의문에 드러냄."),
    72: ("A", "art355_sec5_2.assigned_claim_proceeds_embezzlement", None, None, None,
         "질문에 대한 답변 — 의도된 동작이 맞다. 조건이 맞는 사안에서만 발동한다."),
    75: ("C", "art355_sec5_2.leasehold_transfer",
         "권리이전계약에서 양도인이 부담하는 의무가 양도인 자신의 채무인 경우, 양도인은 배임죄의 "
         "타인 사무처리자가 아니므로 그 의무를 이행하지 않아도 배임죄가 성립하지 않는다.",
         "행위자가 부담한 의무는 계약상 자기 자신의 채무였다.", "not_satisfied",
         "임차권이라는 개별 사안을 일반 법리로 올린다 — 자기 채무 불이행은 배임이 아니다."),
    76: ("D", "art355_sec5_2.pre_sale_right_transfer", None, None, None,
         "75번을 일반 법리로 재작성하면서 수분양권 사안은 그 적용례가 되어 흡수된다."),
    78: ("T", "art355_sec5_3.double_sale_victim_first_purchaser", None, None, None,
         "이중매매 피해자 획정은 인적 구성요건 가이드라인이다. 사기죄에서 삼각사기를 별도 관리한 "
         "것처럼 이중매매도 별도 트랙으로 뺀다 — 트랙은 모듈 전체다(아래 참조)."),
    79: ("T", "art355_sec5_3.invalid_rescission_mistake", None, None, None,
         "해제 적법성 오신 사안 — 지엽적. 이중매매 트랙으로 이관."),
    80: ("T", "art355_sec5_3.no_effective_first_contract", None, None, None,
         "카드 자체는 정당하다는 사용자 확인이 있었으나, 이중매매 모듈이 통째로 별도 트랙이 되므로 "
         "함께 이관한다. 트랙 안에서 유지된다."),
    84: ("Q", "art356_sec2_2.illegal_business", None,
         "행위자는 그 활동을 계속·반복하여 하였고, 그 활동은 사회질서에 반하거나 강행법규에 "
         "위반되어 법이 절대적으로 금지하는 행위였다.", "satisfied",
         "업무성 판단이므로 계속·반복이라는 업무 요건이 질의에 함께 있어야 의미가 있다."),
    89: ("Q", "art357_sec3_2.self_rights_protection_not_improper", None,
         "그 청탁은 행위자에게 법률상 인정되는 권리를 확보하기 위한 것이었다.", "satisfied",
         "'권리'를 법률상 정당한 권리로 한정해 모델의 자의적 확장을 막는다."),
    98: ("D", "art366_sec3_2.emotional_use_objective_limit", None, None, None,
         "'감정상의 용법' 개념 구분 서술로, 사실에 적용할 요건이 없다."),
}

# 이중매매는 카드 몇 장이 아니라 **모듈 전체**가 한 법리 단위다.
# 주석서 절 제목이 "3. 부동산의 이중매매"이고 core 19장이 전부 여기서 나온다.
# 문언에 '이중매매'가 없는 카드(중도금 단계·가등기·구두증여)도 같은 법리의 구성요소다.
TRACK_MODULE = ("art355", "sec5_3")
TRACK = {
    "name": "부동산 이중매매",
    "module": "art355/sec5_3",
    "section_title": "3. 부동산의 이중매매",
    "reason": "매도인·제1매수인·제2매수인의 3자 권리관계가 얽혀 단일 조문 규칙으로 다루면 인적 "
              "구성요건이 섞인다. 사기죄에서 삼각사기(3자 구조)를 별도 관리한 선례를 따른다"
              "(사용자 지적, 결정B 78번). 검토 대상이던 negative 2장만 빼면 같은 법리의 나머지가 "
              "본 트랙에 남아 인적 관계가 반쪽만 배선되므로 모듈 단위로 이관한다.",
    "status": "deferred_to_separate_track",
    "note": "강등이 아니다. 별도 트랙에서 3자 관계를 명시한 규칙으로 다시 설계한다.",
}


def main() -> None:
    core = json.loads((PROP / "property_core_set_final_v2.json").read_text(encoding="utf-8"))
    drafts = json.loads((PROP / "property_negative_query_drafts_v3.json")
                        .read_text(encoding="utf-8"))
    by_id = {i["card_id"]: i for i in drafts["items"]}
    rows = {r["card_id"]: r for r in core["rows"]}

    ledger, counts = [], {"Q": 0, "C": 0, "D": 0, "A": 0, "T": 0}
    for n, (kind, cid, prop, query, status, why) in sorted(DEC.items()):
        counts[kind] += 1
        e = {"item": n, "card_id": cid, "kind": kind, "reason": why}
        if kind == "D":
            e["prev_proposition"] = rows[cid]["proposition"]
            rows[cid].update(final_role="context_only", demoted_at="decision_b", reason=why)
        elif kind == "T":
            pass  # 모듈 단위 이관에서 일괄 처리
        else:
            if prop:
                e["prev_proposition"] = rows[cid]["proposition"]
                e["new_proposition"] = prop
                rows[cid]["prev_proposition"] = rows[cid]["proposition"]
                rows[cid]["proposition"] = prop
                rows[cid]["rewrite_reason"] = why
            if query:
                it = by_id[cid]
                e["prev_query"], e["new_query"] = it["neural_query"], query
                it["prev_neural_query"] = it["neural_query"]
                it["neural_query"] = query
                it["card_status_when_query_satisfied"] = status
                it["revision"] = why
        ledger.append(e)

    # 이중매매 모듈 전체 이관
    art, mod = TRACK_MODULE
    moved = [r for r in rows.values()
             if r["article"] == art and r["module"] == mod and r["final_role"] != "context_only"]
    for r in moved:
        r.update(final_role="deferred_track", deferred_to=TRACK["name"], reason=TRACK["reason"])
    TRACK["cards"] = sorted(r["card_id"] for r in moved)
    TRACK["card_count"] = len(moved)

    core["rows"] = list(rows.values())
    kept = [r for r in core["rows"] if r["final_role"] not in ("context_only", "deferred_track")]
    core["version"] = "3.0.0"
    core["counts"]["demoted_decision_b"] = counts["D"]
    core["counts"]["deferred_double_sale"] = len(moved)
    core["counts"]["core_final"] = len(kept)
    core["deferred_tracks"] = [TRACK]
    (PROP / "property_core_set_final_v3.json").write_text(
        json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    live = [i for i in drafts["items"]
            if rows[i["card_id"]]["final_role"] not in ("context_only", "deferred_track")]
    for i in live:
        i["proposition"] = rows[i["card_id"]]["proposition"]
    drafts.update(version="5.0.0", items=live, status="user_review_complete")
    drafts["counts"]["review"] = len(live)
    (PROP / "property_negative_query_final.json").write_text(
        json.dumps(drafts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (PROP / "결정B_반영원장.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "결정B_질의문승인_v3.md — 사용자 전수 검토 완료(99건). 공란=승인, 기입 31건.",
        "auto_resolved_by_card_audit": [32, 36, 38, 71, 73, 74, 81, 83, 91],
        "principle": "사용자 코멘트는 해석 입력이며 문장은 에이전트가 작성한다.",
        "counts": counts, "entries": ledger, "deferred_tracks": [TRACK],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"결정B 반영 22건 — 질의문교체 {counts['Q']} / 카드재작성 {counts['C']} / "
          f"삭제 {counts['D']} / 트랙이관 {counts['T']} / 답변만 {counts['A']}")
    print(f"이중매매 모듈 이관: {len(moved)}장 (검토대상 3장 + 같은 법리 {len(moved)-3}장)")
    print(f"재산죄 core {len(kept)}장 (이전 409)")
    print(f"질의문 {len(live)}건")
    print("\n삭제된 카드")
    for e in ledger:
        if e["kind"] == "D":
            print(f"  {e['item']:3d}. {e['card_id']}")


if __name__ == "__main__":
    main()
