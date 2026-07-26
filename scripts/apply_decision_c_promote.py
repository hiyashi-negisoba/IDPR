"""학설선택(C/C2) 반영 재작업 — 승격 대상 선정 버그 수정 + 승격분 결함감사 + 학설 어법 제거.

`apply_decisions_ac.py`의 승격 로직에 버그가 두 개 있었다.

버그 1 — 승격 대상 선정
  `auto_self_declared` 16그룹은 `picked`가 인덱스가 아니라 **카드 ID 문자열**이다.
  그런데 코드가 문자열을 문자 단위로 순회하며 'art323_sec1_1...'에 든 숫자를 인덱스로 읽어
  **패자까지 전부 승격**했다. art323_sec1_1 그룹은 3개 선지가 모두 core에 올라갔다.

버그 2 — 감사 우회
  승격 카드는 오늘 돌린 결함감사(죄수·공범·학설·지침·증명)를 거치지 않았다. 그 결과
  죄수·경합 카드와 총칙(공범) 카드가 감사 없이 core로 들어왔다.

추가로, 승격 카드는 "~라는 견해가 있다 / ~설이 소개되어 있다" 어법을 그대로 달고 있다.
사용자가 그 견해를 **실무규칙으로 선택**했으므로 학설 어법을 벗기고 규칙 문장으로 다시 쓴다.
이 재작성은 카드 문언을 바꾸므로 원장에 근거를 남긴다.

API 0회.
"""

from __future__ import annotations

import glob
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

CONC_SEC = re.compile(r"죄수|다른 죄와의 관계|타죄와의 관계|기타의? 죄와의 관계"
                      r"|[가-힣]죄와의 관계|법위반죄와의 관계|본죄와 다른 죄")
COMP_SEC = re.compile(r"공범관계|공범")

# 승격 카드 재작성 — 학설 어법을 벗기고 규칙으로. 값이 None이면 원문 유지.
REWRITE: dict[str, str] = {
    "art323_sec1_1.abstract_danger_offense":
        "권리행사방해죄는 권리행사가 현실적으로 방해되는 결과를 요구하지 않는 추상적 위험범이다.",
    "art323_sec2_1.subject_genuine_status_offense":
        "권리행사방해죄는 타인의 점유 또는 권리의 목적물로 제공한 사람만이 주체가 될 수 있는 "
        "진정신분범이다.",
    "art328_sec4_1.kinship_owner_theory":
        "재산죄에서 친족상도례가 적용되려면 행위자와 재물 소유자 사이에 친족관계가 있어야 한다.",
    "art328_sec4_1.fraud_deceived_person_procedural_theory":
        "사기죄에서 친족상도례가 소추조건인 경우에는 피기망자도 피해자의 하나로서 고소권을 가지나, "
        "형 면제사유인 경우에는 피기망자를 피해자로 취급하지 않는다.",
    "art328_sec4_1.adult_guardian_no_extra_statutory_exclusion":
        "친족인 성년후견인이 가정법원의 감독을 받는 공적 지위에 있더라도, 법률에 별도의 예외 규정이 "
        "없는 한 성년후견인이라는 이유만으로 친족상도례 적용이 배제되지 않는다.",
    "art329_sec2_2.sealed_deposit_entrustment_nature":
        "임치된 포장물의 점유는 위탁관계의 구체적 태양에 따라 정해진다. 봉함·시정 조치가 되어 있으면 "
        "임치인이 점유하므로 수치인의 영득은 절도가 되고, 그러한 조치 없이 관리만 의뢰한 경우에는 "
        "수치인에게 점유가 이전된다.",
    "art329_sec2_2.dead_person_possession_continuing":
        "형법상 점유는 현실적 지배관계이므로 피해자가 사망한 뒤에도 그 점유는 계속되며, 사자로부터 "
        "재물을 탈취하는 행위는 사자의 점유를 침해한다.",
    "art329_sec2_2.carrier_control_based_possession":
        "운반자에 대하여 위탁자 또는 고용주의 현실적 감독·통제가 가능하면 공동점유가 인정되고, "
        "그것이 불가능하면 운반자의 단독점유가 인정된다.",
    "art329_sec5_2.use_theft_possession_not_completely_lost":
        "극히 단시간의 사용으로 재물에 대한 소유자의 소지가 완전히 상실되지 않고 곧 환원될 상태인 "
        "경우에만 영득의사가 없어 사용절도로서 처벌되지 않는다.",
    "art329_sec5_2.fuel_consumption_incidental_use":
        "가솔린 등 연료는 일시 사용에 필연적으로 소비되므로, 소비량이 특별히 많은 경우가 아니면 "
        "그 소비를 차량의 일시 사용과 별도로 문제 삼지 않는다.",
    "art329_sec6.consent_no_taking":
        "피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다.",
    "art331_sec3_3.group_offense_scene_presence":
        "합동범은 2명 이상의 공범자 사이에 현장성이 인정될 때 성립하며, 현장성을 갖추지 않은 단순 "
        "공모자는 합동범이 되지 않는다.",
    "art334_sec3.nighttime_home_intrusion_attempt_on_intrusion":
        "야간주거침입강도는 주거침입과 강도의 결합범이므로 주거에 침입한 때 실행에 착수한다.",
    "art335_sec7_1.attempt_theft_act_standard":
        "준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다.",
    "art335_sec8.weapon_acquired_during_violence.reported_precedent":
        "단순절도범이 체포를 면탈할 목적으로 도주하다가 주운 흉기로 폭행한 경우, 절도 당시에는 흉기를 "
        "휴대하지 않았더라도 폭행 당시 흉기를 휴대하게 되었으므로 특수강도의 준강도가 된다.",
    "art337_sec3.injury_result_violence_intent":
        "강도치상죄는 강도의 기회에 행한 폭행으로 인한 결과적 가중범이므로, 상해의 고의가 없더라도 "
        "적어도 폭행의 고의는 있어야 한다.",
    "art343_sec2_1.contingent_intent_sufficient_precedent":
        "행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다.",
    "art343_sec3.abandonment_before_execution_denied":
        "예비·음모죄는 예비·음모 행위가 있으면 완성되는 범죄이므로 중지미수가 인정될 여지가 없다.",
    "art350_sec3.possessed_property_object_affirmative":
        "자기가 점유하는 타인 소유의 재물도 공갈죄의 객체가 될 수 있다. 타인을 공갈하여 소유권을 "
        "이전하는 처분행위를 하게 할 수 있기 때문이다.",
    "art350_sec8_1.right_enforcement_method_standard":
        "정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 "
        "범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다.",
    "art350_sec9.illicit_gain_intent.required":
        "공갈죄가 성립하려면 고의 외에 불법이득의사가 있어야 한다.",
    "art355_sec1_2.embezzlement_illegal_appropriation_theory":
        "횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 "
        "보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.",
    "art355_sec1_2.embezzlement_illegal_appropriation_exclusion":
        "일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 "
        "불법영득의사가 없어 횡령죄가 성립하지 않는다.",
    "art355_sec1_2.breach_of_trust_betrayal_theory":
        "배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다.",
    "art355_sec1_3.breach_of_trust_case_concrete_risk_of_loss":
        "배임죄의 재산상 손해에는 현실적 손해뿐 아니라 재산상 실해 발생의 위험도 포함되나, 막연한 "
        "위험만으로는 부족하고 경제적으로 손해 발생과 같은 정도의 구체적 위험이 있어야 한다.",
    "art355_sec3_3.authority_excess_theory":
        "위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, "
        "경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.",
    "art355_sec3_3.invalid_disposition_majority":
        "보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 "
        "있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.",
    "art355_sec4_1.temporary_company_fund_objective_assessment_view":
        "회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 "
        "평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.",
    "art355_sec4_2.breach_illicit_gain_separate_requirement":
        "배임죄는 이득죄이므로 고의와 별도로 불법이득의 의사가 있어야 한다.",
    "art355_sec5_2.real_estate_double_sale_majority":
        "부동산 매매계약이 중도금 지급 등으로 본격적인 이행 단계에 이르면, 매도인은 매수인의 재산보전에 "
        "협력하여 그 재산적 이익을 보호·관리할 신임관계에 기초한 타인의 사무처리자에 해당한다.",
    "art357.protected_interest.integrity":
        "배임수증재죄의 보호법익은 거래 또는 사무처리의 청렴성이다.",
    "art357_sec3_4.illegal_appropriation_intent_separate":
        "배임수재죄가 성립하려면 고의 외에 불법영득의 의사가 있어야 한다.",
    "art360_sec2_2.mistaken_bank_transfer_embezzlement_holding":
        "자기 은행계좌에 착오로 입금된 금원은 횡령죄의 객체가 되고 점유이탈물횡령죄의 객체가 되지 않는다.",
    "art360_sec2_3.mistake_property_status_punishable":
        "타인이 점유하는 재물을 점유이탈물로 오인하여 영득한 경우에는 점유이탈물횡령죄로 처벌한다.",
    "art366.special_medium_record_limited_view":
        "특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 "
        "기록으로 한정하여 해석한다.",
    "art366.public_building_affirmative_view":
        "공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 "
        "건조물손괴죄의 객체에 포함된다.",
    "art366_sec3_2.preservation_state_change_view":
        "유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 "
        "다할 수 없게 한 경우에도 손괴가 성립한다.",
    "art366_sec3_2.wall_graffiti_functional_efficiency_limit":
        "벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 "
        "재물손괴죄가 성립한다.",
    "art357_sec3_5.attempt_commencement_standard": None,
    "art357_sec3_3.principal_not_third_party_precedent": None,
}


def section_titles() -> dict[str, str]:
    t: dict[str, str] = {}
    for p in glob.glob(str(ROOT / "data/rulegen/campaign/*_rulegen_requests.jsonl")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                for ch in json.loads(line).get("commentary_chunks", []):
                    if ch.get("section_title"):
                        t[ch["comment_id"]] = ch["section_title"]
    return t


def parse_picked(picked, options: list[str]) -> list[str]:
    """picked를 카드 id 목록으로. 인덱스 리스트 / 카드 id 문자열 / 자유문 모두 처리."""
    if isinstance(picked, str):
        if picked in options:                      # auto_self_declared: 카드 id
            return [picked]
        found = [o for o in options if o in picked]  # "(2) art355_...theory"
        if found:
            return found
        nums = re.findall(r"\((\d+)\)", picked)      # "(1)+(2) 병합"
        return [options[int(n) - 1] for n in nums if 0 < int(n) <= len(options)]
    if isinstance(picked, list):
        out = []
        for x in picked:
            if str(x).isdigit() and 0 < int(x) <= len(options):
                out.append(options[int(x) - 1])
            elif x in options:
                out.append(x)
        return out
    return []


def main() -> None:
    sec = section_titles()
    allc: dict[str, tuple] = {}
    card_sec: dict[str, list[str]] = {}
    for p in glob.glob(str(PROP / "remediated/*/*.json")):
        a, m = Path(p).parts[-2], Path(p).stem
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            allc[c["id"]] = (a, m, c)
            card_sec[c["id"]] = [s for s in (sec.get(r.get("comment_id", ""))
                                             for r in c.get("source_refs", [])) if s]

    # v3(승격 전) 기준에서 다시 시작한다 — v4의 잘못된 승격을 버린다
    core = json.loads((PROP / "property_core_set_final_v3.json").read_text(encoding="utf-8"))
    rows = {r["card_id"]: r for r in core["rows"]}
    ledger = json.loads((PROP / "학설선택_확정원장.json").read_text(encoding="utf-8"))
    groups = {i["variant_group"]: i for i in json.loads(
        (PROP / "property_norm_card_review_queue.json").read_text(encoding="utf-8"))["items"]
        if i.get("type") == "3.1_variant_group"}

    entries, stats = [], Counter()
    for item in ledger["items"]:
        gid = item["variant_group"]
        g = groups.get(gid)
        if not g:
            stats["group_missing"] += 1
            continue
        opts = [o["card_id"] for o in g.get("options", [])]
        res = item["resolution"]
        if res in ("user_hold", "gap_missing_option"):
            stats["group_uncovered"] += 1
            entries.append({"group": gid, "resolution": res, "promoted": [],
                            "note": "uncovered로 정직 보고"})
            continue
        chosen = parse_picked(item.get("picked"), opts)
        if not chosen:
            stats["group_unparsed"] += 1
            entries.append({"group": gid, "resolution": res, "promoted": [],
                            "note": f"picked 해석 실패: {item.get('picked')!r}"})
            continue

        promoted, blocked = [], []
        for cid in chosen:
            if cid in rows and rows[cid]["final_role"] not in ("context_only", "deferred_track"):
                rows[cid]["doctrine_selected"] = {"group": gid, "resolution": res}
                stats["already_core"] += 1
                continue
            if cid not in allc:
                stats["card_missing"] += 1
                continue
            ss = card_sec.get(cid, [])
            if any(CONC_SEC.search(x) for x in ss):
                blocked.append((cid, "죄수·다른죄 관계 절"))
                stats["blocked_concurrence"] += 1
                continue
            if any(COMP_SEC.search(x) for x in ss):
                blocked.append((cid, "공범관계 절 — 총칙"))
                stats["blocked_complicity"] += 1
                continue
            a, m, c = allc[cid]
            prop = REWRITE.get(cid) or c.get("proposition", "")
            row = {"article": a, "module": m, "card_id": cid, "polarity": c.get("polarity"),
                   "proposition": prop, "merge_role": "policy_variant",
                   "final_role": "standard_input", "demoted_at": None, "reason": None,
                   "promoted_from_variant": True,
                   "doctrine_selected": {"group": gid, "resolution": res,
                                         "user_comment": item.get("user_comment")}}
            if cid in REWRITE and REWRITE[cid]:
                row["prev_proposition"] = c.get("proposition", "")
                row["rewrite_reason"] = ("학설 어법 제거 — 사용자가 이 견해를 실무규칙으로 "
                                         "선택했으므로 '~라는 견해가 있다'를 벗기고 규칙으로 진술")
                stats["rewritten"] += 1
            elif cid not in REWRITE:
                row["rewrite_pending"] = "학설 어법이 남아 있을 수 있음 — 재작성 미지정"
                stats["rewrite_pending"] += 1
            rows[cid] = row
            promoted.append(cid)
            stats["promoted"] += 1
        entries.append({"group": gid, "resolution": res, "chosen": chosen,
                        "promoted": promoted,
                        "blocked": [{"card_id": c, "reason": r} for c, r in blocked]})

    core["rows"] = list(rows.values())
    kept = [r for r in core["rows"] if r["final_role"] not in ("context_only", "deferred_track")]
    core["version"] = "5.0.0"
    core["counts"]["promoted_from_doctrine"] = stats["promoted"]
    core["counts"]["core_final"] = len(kept)
    (PROP / "property_core_set_final_v5.json").write_text(
        json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (PROP / "결정C_승격원장.json").write_text(json.dumps({
        "version": "2.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supersedes": "결정AC_반영원장.json 의 승격분 (선정 버그·감사 우회)",
        "bugfix": ["auto_self_declared의 picked는 카드 id 문자열인데 인덱스로 읽어 패자까지 승격했다",
                   "승격 카드가 결함감사(죄수·공범)를 거치지 않았다"],
        "stats": dict(stats), "entries": entries, "rewrites": REWRITE,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("학설선택 승격 재작업")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print(f"\n재산죄 core {len(kept)}장")


if __name__ == "__main__":
    main()
