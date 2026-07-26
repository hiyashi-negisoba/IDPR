"""재산죄 RuleIR 레벨(페이즈) 구조 정리 — 조문별·단위별 (API 0회).

사용자 요청(2026-07-26): 커버 중인 재산죄 전체에 대해 조문별 RuleIR 레벨 구조를 정리한다
(기본범 → 가중범 식). 추측으로 그리지 않고 **검토완료 core 480장을 레벨에 배정해** 각 레벨이
실제로 어떤 카드로 채워지는지, 빈 레벨이 어디인지 확인한다.

레벨 정의 — 판단이 흘러가는 순서다. 아래 레벨은 위 레벨의 결과를 입력으로 받는다.

  L0 적격·객체   재물성·재산상 이익·타인성·점유·주체 신분 — 무엇에 대한 누구의 죄인가
  L1 실행행위    절취·강취·폭행협박·처분·손괴·취거·임무위배·청탁 — 무엇을 했는가
  L2 인과·귀속   행위와 결과의 연결, 처분행위 매개, 결과 귀속
  L3 주관        고의·불법영득의사·불법이득의사·목적·인식
  L4 단계        실행의 착수·기수시기·미수
  L5 가중        가중유형 플래그 요건(야간·흉기·합동·상습·업무자·상해·사망·예비·준강도)
  L6 위법성·책임 권리행사·피해자의 승낙·정당행위
  L7 처벌·소추   친족상도례(형 면제·친고죄) — A4 절차 레이어로 이월

배정 규칙은 두 단계다. ① **가중유형 조문에서 온 카드는 L5**다(제330·331·332조는 절도 가중,
제334·335·337·338·343조는 강도 가중, 제356조는 업무자 신분). 그 조문 자체가 가중유형을 정하기
때문이다. ② 기본조문 카드는 명제 문언으로 L0~L4·L6에 배정한다. 제328조는 전부 L7이다.

문언 배정은 휴리스틱이므로 레벨별 표본을 함께 출력해 검증한다.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_property_core_norm_card_sets import commentary_index  # noqa: E402

PROP = ROOT / "data/rulegen/property"
UNITS = PROP / "rule_ir_units"
UNIT_MANIFEST = PROP / "rule_ir_unit_manifest.json"
OUT_JSON = PROP / "rule_ir_phase_map.json"  # 설계 문서는 rulegen_rule_ir_phases.md

LEVELS: dict[str, str] = {
    "L0": "적격·객체",
    "L0o": "적격·객체(소유)",
    "L0p": "적격·객체(점유)",
    "L0c": "적격·객체(보관자 지위·위탁관계)",
    "L0r": "적격·객체(재물강취 트랙)",
    "L0b": "적격·객체(이득강취 트랙)",
    "L1": "실행행위",
    "L2": "인과·귀속",
    "L3": "주관(일반 고의)",
    "L3a": "주관(불법영득·이득의사)",
    "L4": "단계(착수)",
    "L4r": "단계(재물강취 기수)",
    "L4b": "단계(이득강취 기수)",
    "L5": "가중",
    "L6": "위법성·책임",
    "L7": "처벌·소추",
}

# component 재분해 — 절 구조를 보니 일부 죄명은 L0/L3 하나에 **결합적(AND)** 요건 둘이
# 섞여 있었다(절도: 타인 소유 AND 타인 점유가 한 component로 묶여 19장 중 1장만 인정돼도
# 객체 요건 전체가 충족됐다). component_layer는 같은 레벨의 카드를 OR로 묶으므로, AND 관계인
# 하위요건은 레벨 자체를 쪼개야 한다. 반대로 절이 여러 개라도 하나의 요건에 대한 대안적
# 인정경로(예: 손괴죄 객체 카탈로그의 문서/전자기록/재물)면 OR가 맞으므로 쪼개지 않는다 —
# 그 구분은 조문마다 다르므로 카드별 명시 표로 남긴다(정규식 없음).
CARD_LEVEL_OVERRIDE: dict[str, str] = {
    # ── 절도(제329조) — 객체: 타인 소유 AND 타인 점유는 별개 요건이다 ──
    "art329_sec2.theft_object_anothers_property_in_possession": "L0o",
    "art329_sec2_1.co_owned_property_taking": "L0o",
    "art329_sec2_1.inherited_estate_not_ownerless": "L0o",
    "art329_sec2_1.other_person_legal_entity": "L0o",
    "art329_sec2_1.vehicle_internal_ownership_agreement": "L0o",
    "art329_sec2_2.carrier_control_based_possession": "L0p",
    "art329_sec2_2.clerk_subordinate_possession": "L0p",
    "art329_sec2_2.criminal_possession_definition": "L0p",
    "art329_sec2_2.dead_person_possession_continuing": "L0p",
    "art329_sec2_2.dead_person_possession_limited": "L0p",
    "art329_sec2_2.joint_custodian_unilateral_taking": "L0p",
    "art329_sec2_2.possession_assistant_control": "L0p",
    "art329_sec2_2.possession_control_and_intent": "L0p",
    "art329_sec2_2.possession_factual_control_standard": "L0p",
    "art329_sec2_2.possession_intent_definition": "L0p",
    "art329_sec2_2.property_in_managed_place": "L0p",
    "art329_sec2_2.sealed_deposit_entrustment_nature": "L0p",
    "art329_sec2_2.temporary_separation_possession": "L0p",
    "art329_sec2_2.unlawful_possession_protected": "L0p",
    # ── 절도(제329조) — 주관: 고의 AND 불법영득의사는 별개 요건이다 ──
    "art329_sec4.intent.conditional_intent_sufficient": "L3",
    "art329_sec4.intent.general_object_selection": "L3",
    "art329_sec4.intent.theft_intent_definition": "L3",
    "art329_sec5_1.unlawful_appropriation_required": "L3a",
    "art329_sec5_2.collateral_taking_unlawful_appropriation": "L3a",
    "art329_sec5_2.use_theft_long_possession_or_abandonment": "L3a",
    "art329_sec5_2.use_theft_value_consumption_or_delayed_return": "L3a",
    # ── 배임(제355조) — 주관: 배임의 고의 AND 불법이득의사는 별개 요건이다(제3항 "별개 요건") ──
    "art355_sec4_1.breach_of_trust_intent_elements": "L3",
    "art355_sec4_1.breach_of_trust_intent_no_purpose": "L3",
    "art355_sec4_1.business_judgment_intent": "L3",
    "art355_sec4_1.double_sale_unjustified_rescission_intent": "L3",
    "art355_sec4_1.role_violation_intent": "L3",
    "art355_sec4_2.breach_illicit_gain_intent": "L3a",
    "art355_sec4_2.breach_illicit_gain_separate_requirement": "L3a",
    "art355_sec4_2.mixed_motives_primary_purpose": "L3a",
    "art355_sec4_2.third_party_benefit_sufficient": "L3a",
    # ── 강도(제333조) — 재물강취(제1항) OR 이득강취(제2항)는 대안적 실행형태다(AND 아님).
    # 객체·기수만 트랙별로 갈리고, 폭행·협박(행위)·인과관계·불법영득/이득의사·착수는 공유한다.
    "art333_sec3_1.real_estate_as_robbery_property_negative": "L0r",
    "art333_sec7_1.completion.exclusive_control_transfer": "L4r",
    "art333_sec7_1.completion.exclusive_control_within_victim_domain": "L4r",
    "art333_sec4_1.apparent_property_benefit": "L0b",
    "art333_sec4_1.property_benefit": "L0b",
    "art333_sec4_2.debt_evasion_benefit_transfer": "L0b",
    "art333_sec4_2.debt_evasion_disposition_not_required": "L0b",
    "art333.illegal_cause_debt_evasion_robbery_murder": "L0b",
    "art333_sec7_2.completion_forcible_gain": "L4b",
    # 재물탈취 범의가 생긴 시점에 따른 인과관계 — 주관이 아니라 행위·결과의 연결 문제다.
    "art333_sec3_3.continuing_force_after_theft_intent": "L2",
    "art333_sec3_3.continuing_force_single_robbery": "L2",
    "art333_sec3_3.rape_fear_state_property_provision": "L2",
    "art333_sec3_3.rape_force_subsequent_taking_precedent": "L2",
    # ── 횡령(제355조) — 객체: 보관자 지위(위탁관계) AND 타인 소유는 별개 요건이다.
    # 타인 소유·객체 개념은 절도의 L0o("object_ownership")와 같은 성격이라 레벨을 공유한다.
    "art355.embezzlement.document-embodied-right": "L0o",
    "art355.embezzlement.object-identification": "L0o",
    "art355.embezzlement.object-other-property": "L0o",
    "art355.embezzlement.other-person": "L0o",
    "art355_sec2_1.embezzlement_object_property": "L0o",
    "art355.embezzlement_custody": "L0c",
    "art355.embezzlement_protectable_entrustment": "L0c",
    # 가장납입·비자금 카드는 "객체" 문제가 아니라 불법영득의사 판단자료다(절 제목 "구체적 검토"의
    # 문언 배정이 재물·자금이라는 명사에 걸려 L0로 샜다).
    "art355_sec4_3.fake_capital_real_increase_assessment": "L3",
    "art355_sec4_3.slush_fund_definition": "L3",
    "art355_sec4_3.slush_fund_purpose_assessment": "L3",
    # ── 공갈(제350조) — "수령할 권리와 불법이득의사"라는 절 제목 때문에 L3로 샜지만, 카드
    # 내용은 실행수단의 정도(착수) 판단이지 주관적 요건이 아니다.
    "art350_sec8_1.right_enforcement_method_standard": "L1",
    # ── 손괴(제366조) — 재물 개념은 유체물+관리가능동력 정의 자체가 객체 카드다(행위 카드가 아님).
    "art366.object_manageable_energy": "L0",
    # ── 권리행사방해(제323조) — 객체: 자기 소유(행위자 관점) AND 타인의 점유·권리(피해자
    # 관점)는 별개 요건이다. 이름은 절도의 소유/점유 component와 같지만(방향은 반대) 같은
    # 성격의 AND-분리라 레벨을 공유한다.
    "art323_sec2_2.self_property_owner": "L0o",
    "art323_sec2_2.title_transfer_criteria": "L0o",
    "art323_sec2_1.subject_genuine_status_offense": "L0o",
    "art323_sec2_2.joint_possession_object": "L0p",
    "art323_sec2_2.nonpossessory_claim_precedent": "L0p",
    "art323_sec2_2.possession_actual_control": "L0p",
    "art323_sec2_2.property_movables_real_estate": "L0p",
    "art323_sec2_2.protected_possession_potential_value": "L0p",
    "art323_sec2_2.rescinded_sale_recovery": "L0p",
    "art323_sec2_2.retained_title_sale": "L0p",
    "art323_sec2_2.rightful_possession_definition": "L0p",
    "art323_sec2_2.electronic_records": "L0p",
    "art323_sec2_2.corporate_system_records_other": "L0p",
    "art323_sec1_1.abstract_danger_offense": "L0p",
    "art323_sec1_1.conduct_and_object": "L0p",
    # 친족상도례 피해자 범위는 이 죄의 기본 성립요건이 아니다(절차법/A4 레이어 주제) — L0
    # 기본배정에 남으면 모든 사건에 친족상도례 카드까지 증명하라고 요구하는 버그가 된다.
    "art323_sec7.family_exception_victim": "L7",
}

# 가중유형을 정하는 조문 → 그 조문 카드는 전부 L5
AGGRAVATION_ARTICLES: dict[str, str] = {
    "art330": "야간주거침입절도(제330조)",
    "art331": "특수절도(제331조)",
    "art332": "상습절도(제332조)",
    "art334": "특수강도(제334조)",
    "art335": "준강도(제335조)",
    "art337": "강도상해·치상(제337조)",
    "art338": "강도살인·치사(제338조)",
    "art343": "강도 예비·음모(제343조)",
    "art356": "업무자 가중신분(제356조)",
    "art342": "미수 처벌근거(제342조)",
}
PUNISHABILITY_ARTICLES = {"art328": "친족상도례(제328조)"}

# 1차 신호는 **주석서 절 제목**이다. 카드 명제만 보면 객체 명사(재물·점유)가 행위 카드에도 나와
# L0가 전부를 삼킨다(첫 시도에서 480장 중 166장이 L0로 쏠렸다). 주석서는 절 자체를 객체·행위·
# 주관·착수로 나눠 놓았으므로 그 구조를 그대로 쓴다. 카드결함 감사에서도 절 제목이 명제 문언보다
# 강한 신호였다.
TITLE_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("L4", re.compile(r"착수|기수|미수")),
    # `이득의`만 보면 "1. 이득의 개념"(재산상 이익의 정의 = 객체)이 주관으로 간다.
    # 실제로 강도 제333조 Ⅳ.1이 그렇게 새서 robbery의 객체 component가 1장으로 줄었다.
    # 주관 표지는 '의사·범의·고의'가 붙은 것으로 한정한다.
    ("L3", re.compile(r"주관적|범의|고의|영득의사|이득의?\s*의사|사용절도")),
    ("L2", re.compile(r"인과관계")),
    ("L6", re.compile(r"정당행위|위법성")),
    ("L0", re.compile(r"객체|주체|타인의 (점유|소유|재물|물건)|인적 범위|재물|보관자|"
                      r"업무상 (보관|타인의 사무)|업무의 (의의|내용)|신분|"
                      r"이득의 (개념|의의)|이익의 (개념|의의)")),
    ("L1", re.compile(r"행위|폭행|협박|공갈|처분|청탁|취득|반항억압|혼취|강취|절취|손괴|"
                      r"효용|취거|은닉|임무")),
]

# 절 제목이 일반적일 때(총설·개설·의의·구체적 검토) 쓰는 명제 문언 배정.
# 여기서는 L1(행위 동사)을 L0보다 먼저 본다 — 절을 모를 때는 행위 동사가 더 강한 신호다.
# `권리행사`는 권리행사방해죄 명제에 죄명으로 들어가므로 L6 표지로 쓸 수 없다(전 단위가 L6로
# 쏠린다). 정당화 맥락에 한정된 문언만 쓴다. `귀속`·`때문`·`사용`도 같은 이유로 뺐다.
TEXT_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("L6", re.compile(r"위법성|정당행위|정당한 권리행사|피해자의 승낙|승낙이 (있|외부|없)|"
                      r"조각(된|되어|될|사유)|취득할 권리가 있는")),
    ("L2", re.compile(r"인과관계|기인하|매개|객관적 귀속|효과를 미친")),
    ("L4", re.compile(r"실행(의)? ?착수|착수(하|한|가|를|에|시)|기수|미수|예비|완성된 때|"
                      r"기수시기|종료된 뒤|계속성")),
    ("L3", re.compile(r"고의|불법영득|불법이득|영득의사|이득의사|의사가 (있|없)|목적으로|"
                      r"인식(하|이|을)|의욕|미필적|일시 사용|사용절도|반환.{0,3}의사")),
    ("L1", re.compile(r"절취|강취|탈취|폭행|협박|기망|처분행위|손괴|은닉|취거|교부|반환(을)? ?거부|"
                      r"임무(에)? ?위배|배임행위|청탁|공여|효용|침해행위")),
    ("L0", re.compile(r"재물(성|이|은|에|로|을 |의 개념)|재산상 이익|타인의 (재물|물건|사무|권리)|"
                      r"점유|소유|보관|신분범|주체|객체|위탁|사무처리자|사무를 처리하는|"
                      r"관리(가능|할 수)|무주물|금제품|물건")),
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def article_of(card_id: str) -> str:
    return card_id.split("_")[0].split(".")[0]


# 명제가 기수·미수·착수를 직접 말하면 절 제목보다 그 신호가 강하다. 주석서는 기수시기 규칙을
# '행위' 절 안에 적어 두는 경우가 있어(횡령 제355조 Ⅲ.3, 점유이탈물횡령 제360조 Ⅱ.3) 절 제목만
# 보면 단계 규칙이 실행행위로 흘러간다.
STAGE_OVERRIDE = re.compile(r"기수|미수|실행(의)? ?착수|착수한 것으로")


def assign_level(card: dict[str, Any]) -> tuple[str, str]:
    if card["id"] in CARD_LEVEL_OVERRIDE:
        level = CARD_LEVEL_OVERRIDE[card["id"]]
        return level, f"component 재분해 명시 배정 — {LEVELS[level]}(AND 결합요건 분리)"
    article = article_of(card["id"])
    if article in PUNISHABILITY_ARTICLES:
        return "L7", f"{PUNISHABILITY_ARTICLES[article]} — 성립이 아니라 처벌·소추 층"
    if article in AGGRAVATION_ARTICLES:
        return "L5", f"{AGGRAVATION_ARTICLES[article]} 조문에서 온 카드"
    if STAGE_OVERRIDE.search(card["proposition"]):
        return "L4", "명제가 기수·미수·착수를 직접 정한다"
    title = card.get("_section_title", "")
    for level, pattern in TITLE_RULES:
        if pattern.search(title):
            return level, f"절 제목 배정 — {LEVELS[level]} ({title[:24]})"
    text = card["proposition"]
    for level, pattern in TEXT_RULES:
        if pattern.search(text):
            return level, f"문언 배정 — {LEVELS[level]}"
    fallback = {"definition": "L0", "element": "L1", "causal_link": "L2",
                "standard": "L1", "exception": "L1", "variant": "L1"}
    level = fallback[card["norm_kind"]]
    return level, f"norm_kind={card['norm_kind']} 기본 배정"


def main() -> None:
    manifest = read_json(UNIT_MANIFEST)
    units = [unit["issue_tag"] for unit in manifest["units"]]

    rows: list[dict[str, Any]] = []
    by_unit_level: dict[str, Counter] = defaultdict(Counter)
    by_article_level: dict[str, Counter] = defaultdict(Counter)
    samples: dict[str, list[str]] = defaultdict(list)

    commentary: dict[str, Any] = {}
    for article in sorted({article_of(card["id"])
                           for tag in units
                           for card in read_json(UNITS / f"{tag}.json")["cards"]}):
        chunks, _ = commentary_index(article)
        commentary.update(chunks)

    for tag in units:
        for card in read_json(UNITS / f"{tag}.json")["cards"]:
            first = card["source_refs"][0]["comment_id"]
            card = {**card, "_section_title":
                    commentary.get(first, {}).get("section_title", "")}
            level, why = assign_level(card)
            article = article_of(card["id"])
            rows.append({"card_id": card["id"], "unit": tag, "article": article,
                         "level": level, "reason": why, "norm_kind": card["norm_kind"],
                         "formalization": card["formalization"],
                         "proposition": card["proposition"]})
            by_unit_level[tag][level] += 1
            by_article_level[article][level] += 1
            if len(samples[level]) < 4:
                samples[level].append(f"[{tag}] {card['proposition'][:90]}")

    OUT_JSON.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "levels": LEVELS,
        "method": ("가중유형 조문 카드는 L5, 제328조는 L7, 나머지는 명제 문언으로 L0~L4·L6 배정"),
        "aggravation_articles": AGGRAVATION_ARTICLES,
        "counts": {"cards": len(rows),
                   "per_level": dict(sorted(Counter(r["level"] for r in rows).items())),
                   "per_unit_level": {tag: dict(sorted(counter.items()))
                                      for tag, counter in by_unit_level.items()},
                   "per_article_level": {article: dict(sorted(counter.items()))
                                         for article, counter in sorted(by_article_level.items())}},
        "rows": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    order = list(LEVELS)
    print(f"카드 {len(rows)}장 배정")
    for level in order:
        count = sum(1 for r in rows if r["level"] == level)
        print(f"  {level} {LEVELS[level]:12s} {count:4d}")
    print("\n단위 × 레벨")
    header = "  " + " ".join(f"{lv:>4s}" for lv in order)
    print(f"  {'단위':36s}" + header)
    for tag in units:
        cells = " ".join(f"{by_unit_level[tag].get(lv, 0):4d}" for lv in order)
        print(f"  {tag:36s}   {cells}")
    print("\n레벨별 표본")
    for level in order:
        if samples[level]:
            print(f"  {level} {LEVELS[level]}")
            for line in samples[level]:
                print(f"      {line}")
    print(f"\n→ {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
