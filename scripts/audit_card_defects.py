"""카드 결함 전수감사 — 재산죄 core 452장 + 사기 core 88장 (사용자 지시 2026-07-23).

계기: 결정B 91번. `art360_sec2_1.status_offense.not_majority`
"점유이탈물횡령죄는 신분범으로 보지 않는 것이 통설적 견해이다" 가 core로 살아남았고,
긍정형 전환 시 통설과 정반대인 명제를 모델에게 사실로 묻게 됐다. 자동 표지("통설**적**"이
DOCTRINE regex를 빠져나감)와 2차 전수 판독이 모두 놓쳤다.

핵심 교훈: **명제 텍스트만으로 거르면 놓친다.** 카드가 어느 절에서 나왔는지(section_title)가
훨씬 강한 신호다. 32번(`art343.special_robbery_attempt_home_invasion`)이 그 증거로,
명제에는 죄수 키워드가 하나도 없지만 출처는 "2. 주거침입죄와의 관계" 절이다.

감사 축:
  S. 절 출처       죄수·다른죄 관계 / 공범관계 절에서 나온 카드      ← 신규, 가장 강함
  1. 메타 래핑     규칙을 '~라는 견해/판례/설명이다'로 감쌈
  2. 판단지침형     '결정적 요소가 아니다' '단정할 수 없다' 등 해석 지침
  3. 증명·소송법    증명책임·추단 등 사실인정 방법론
  4. 근사중복       같은 조문 안에서 동일 취지 카드 반복

1은 다시 둘로 갈린다. **래퍼만 벗기면 되는 것**(안에 실질 규칙이 있음)과 **알맹이가 없는
것**(순수 학설 분류)이다. 전자는 재작성, 후자는 강등이다.

API 0회.
"""

from __future__ import annotations

import difflib
import glob
import itertools
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/rulegen/property/card_defect_audit.json"

CONC_SEC = re.compile(r"죄수|다른 죄와의 관계|타죄와의 관계|기타의? 죄와의 관계"
                      r"|[가-힣]죄와의 관계|법위반죄와의 관계|본죄와 다른 죄")
COMP_SEC = re.compile(r"공범관계|공범")
WRAP = re.compile(r"(통설|다수설|소수설|유력설|학설|견해|판례|평가|설명|서술|태도|입장)"
                  r"(이다|이라는|가 제시|가 소개|되어 있다|되어있다|으로 이해|으로 본다|이라고 본다)"
                  r"|소개(된다|되어 있다|하고 있다|된 )|설명되어|서술되어|이해된다|평가된다"
                  r"|보지 않는 것이|것이 통설")
GUIDE = re.compile(r"결정적 요소가 아니|기준으로 판단해야|제한적으로 해석해야|신중하게 판단"
                   r"|우선 존중되어야|함부로 인정할 수 없|단정(하기 어렵|할 수 없)|곧바로 (인정|성립)")
PROOF = re.compile(r"증명책임|입증하여야|증명하여야|합리적 의심|검사가 (입증|증명)"
                   r"|추단할 수 있|추인할 수 있|피고인 이익|공소사실")

# 래퍼 안에 실질 규칙이 있어 재작성으로 살릴 카드 (알맹이 없는 것과 구분)
UNWRAP = {
    "fraud_intent.precedent_illegal_appropriation_intent":
        "사기죄가 성립하려면 고의 외에 불법영득의사가 있어야 한다.",
    "art323_sec2_2.title_transfer_criteria":
        "자기 물건인지 여부는 법률에 따른 소유권 귀속으로 판단하며, 부동산은 등기, 동산은 인도, "
        "등록으로 소유권이 이전되는 동산은 등록 여부가 판단기준이 된다.",
    "art329_sec2_2.possession_assistant_control":
        "점유보조자가 물건에 대한 사실상 지배를 가지면 그 영득행위는 절도가 아니라 횡령이 되고, "
        "본점유자의 지시·감독 아래 소지 또는 감수할 뿐이면 형법상 점유자가 아니어서 절도죄가 성립한다.",
    "art328_sec2_1.personal_exemption":
        "제328조 제1항의 형 면제는 범죄 성립에는 영향이 없고 형벌만 면제하는 인적 처벌조각사유이다.",
}
# 알맹이가 없어 강등할 카드
DEMOTE_WRAP = {
    "art360_sec2_1.status_offense.not_majority":
        "죄의 신분범 분류에 관한 학설 진술이며 사실관계에 적용할 요건이 없다. 긍정형 전환 시 "
        "통설과 반대되는 명제가 되어 오히려 유해하다(사용자 지적, 결정B 91번).",
    "art355_sec5_2.general_civil_contract_direction":
        "'제한적으로 해석해야 한다는 평가'는 해석 방향 제시이지 적용 규칙이 아니다. 같은 취지의 "
        "적용 규칙은 art355_sec5_2.right_transfer_ordinary_duty가 이미 담고 있다(사용자 지적 74번).",
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


def load_property() -> list[dict[str, Any]]:
    sec = section_titles()
    card_sec: dict[str, list[str]] = {}
    for p in glob.glob(str(ROOT / "data/rulegen/property/remediated/*/*.json")):
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            card_sec[c["id"]] = [s for s in
                                 (sec.get(r.get("comment_id", "")) for r in c.get("source_refs", []))
                                 if s]
    rows = json.loads((ROOT / "data/rulegen/property/property_core_set_final.json")
                      .read_text(encoding="utf-8"))["rows"]
    return [{"card_id": r["card_id"], "group": r["article"], "polarity": r["polarity"],
             "proposition": r["proposition"], "sections": card_sec.get(r["card_id"], [])}
            for r in rows if r["final_role"] != "context_only"]


def load_fraud() -> list[dict[str, Any]]:
    R = ROOT / "data/rulegen/fraud"
    gold = {r["card_id"]: r for r in json.loads(
        (R / "fraud_core_rule_selection_audit.json").read_text(encoding="utf-8"))["rows"]}
    cards: dict[str, Any] = {}
    for p in glob.glob(str(R / "norm_card_sets/*.json")):
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            cards[c["id"]] = c
    return [{"card_id": k, "group": gold[k]["module"], "polarity": cards[k].get("polarity"),
             "proposition": cards[k]["proposition"], "sections": []}
            for k, v in gold.items() if v["role"] != "context_only" and k in cards]


def audit(name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    f = defaultdict(list)
    for r in rows:
        p, s = r["proposition"], r["sections"]
        if any(CONC_SEC.search(x) for x in s):
            f["S1_죄수·다른죄_절"].append(r)
        elif any(COMP_SEC.search(x) for x in s):
            f["S2_공범관계_절"].append(r)
        if WRAP.search(p):
            f["W1_래퍼벗기기" if r["card_id"] in UNWRAP else
              ("W2_강등" if r["card_id"] in DEMOTE_WRAP else "W3_미분류")].append(r)
        if GUIDE.search(p):
            f["G_판단지침형"].append(r)
        if PROOF.search(p):
            f["P_증명·소송법"].append(r)
    byg = defaultdict(list)
    for r in rows:
        byg[r["group"]].append(r)
    dups = []
    for rs in byg.values():
        for a, b in itertools.combinations(rs, 2):
            s = difflib.SequenceMatcher(None, a["proposition"], b["proposition"]).ratio()
            if s >= 0.72:
                dups.append({"similarity": round(s, 2),
                             "a": a["card_id"], "b": b["card_id"],
                             "prop_a": a["proposition"], "prop_b": b["proposition"]})
    flagged = {r["card_id"] for v in f.values() for r in v} | \
              {d["a"] for d in dups} | {d["b"] for d in dups}
    print(f"\n{'='*66}\n{name} core {len(rows)}장 — 결함 지적 {len(flagged)}장 "
          f"({len(flagged)/len(rows):.1%})")
    for k in sorted(f):
        print(f"  {k}: {len(f[k])}장")
    print(f"  D_근사중복: {len(dups)}쌍")
    return {"core_size": len(rows), "flagged": len(flagged),
            "by_axis": {k: [r["card_id"] for r in v] for k, v in sorted(f.items())},
            "duplicates": dups,
            "detail": {k: [{"card_id": r["card_id"], "sections": r["sections"],
                            "proposition": r["proposition"]} for r in v]
                       for k, v in sorted(f.items())}}


def main() -> None:
    res = {"version": "1.0.0", "api_calls": 0,
           "created_at": datetime.now(timezone.utc).isoformat(),
           "trigger": "결정B 91번 사용자 지적 — 학설 서술 카드가 core로 통과",
           "unwrap_rewrites": UNWRAP, "wrap_demotions": DEMOTE_WRAP,
           "property": audit("재산죄", load_property()),
           "fraud": audit("사기", load_fraud())}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
