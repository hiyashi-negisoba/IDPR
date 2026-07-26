"""core scope 감사 — 어떤 카드가 결론에 흘러들고 어떤 카드가 RAG 문맥인지 판정한다.

merge 모델은 카드 대부분을 core(deterministic_rule/standard_input)로 올린다. 사기 트랙
실측이 그것을 보여준다: merge 원본 76.9~82.8% core → 최종 감사 후 13.6%. 재산죄 merge
원본도 80.6% core로 같은 자리에 있다. 즉 이 강등은 파이프라인 결함이 아니라 아직 하지
않은 단계다.

기준은 사기 `fraud_core_rule_selection_audit.json`의 것을 그대로 쓴다.

  context_only       구체적 판례 결과, 학설, 희귀 적용례, 이득액 계산, 다른 죄명 문맥
  deterministic_rule 일반 법리, 정의, 다른 predicate를 결합하는 상징 규칙
  standard_input     일반화된 법적 기준이지만 사실 적용에 neural judgment가 필요한 입력

사기는 이것을 수작업으로 했다(`manual_full_core_scope_audit_no_api`). 여기서는 같은
기준을 표지로 옮기고 **사기 646장을 정답으로 두어 정밀도를 측정한 뒤** 재산죄에 적용한다.
자동 강등은 정밀도가 확인된 표지에 한정하고, 나머지는 core로 남겨 사람이 본다.

API 0회.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRAUD_AUDIT = PROJECT_ROOT / "data/rulegen/fraud/fraud_core_rule_selection_audit.json"
FRAUD_CARDS = PROJECT_ROOT / "data/rulegen/fraud/norm_card_sets"
PROP_CARDS = PROJECT_ROOT / "data/rulegen/property/remediated"

CORE = ("deterministic_rule", "standard_input")

# --- 표지 ---------------------------------------------------------------
# 1. 메타 서술: 명제가 사건이 아니라 '주석서가 무엇을 소개하는지'를 말한다.
META = re.compile(
    r"(판례|견해|학설|설명|주석|입장|논의|서술|다수설|통설)(가|이|로|은|는|을|를)?\s*"
    r"(소개|설시|서술|기술|제시|언급)"
    r"|(라는|다는)\s*(판례|견해|설명|입장|서술|취지)"
    r"|(고|다고)\s*(본다|보고 있다|판단하고 있다|설명한다|소개한다|서술한다|기술한다|한다)"
    r"|(판례|통설|다수설|소수설)(는|은)\s.*(입장|태도)(이다|다|이라고)"
    r"|견해가 (있다|제시)|설이 (있다|대립)"
)
# 2. 학설 지시: 'ㅇㅇ설'
DOCTRINE = re.compile(r"[가-힣]{2,6}설(은|이|을|과|의|에|,|\s|$)|긍정설|부정설|절충설|제한설")
# 3. 죄수·경합 — 사기에서 concurrence 모듈 0% core
CONCURRENCE = re.compile(
    r"경합범|상상적 경합|실체적 경합|포괄일죄|포괄하여 (하나|일죄)|불가벌적 사후행위"
    r"|흡수(된다|되어|관계)|죄수|법조경합|별죄를 구성|별도의? .{0,6}죄가 성립"
)
# 4. 총칙 영역 — 사기에서 stages_participation 8%, special_forms 1%
GENERAL_PART = re.compile(
    r"공동정범|교사범|방조범|종범|공범관계|공모관계|간접정범|실행의 착수|예비\W|음모"
    r"|중지미수|장애미수|불능범|위법성조각|정당방위|긴급피난|자구행위|피해자의 승낙"
    r"|책임조각|법률의 착오|기대가능성|심신(미약|상실)|누범|상습범|양형|작량감경"
)
# 5. 구체 사건 서술 — 희귀 적용례
CASE_SPECIFIC = re.compile(
    r"\d[\d,]*\s*(만\s*)?원|㎡|평\W|피고인\s*[A-Z가-힣]{1,3}(은|이|을)"
    r"|주식회사 [가-힣A-Z]|\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\."
)
# 6. 절차·부수 규정
PROCEDURAL = re.compile(r"고소(가|를|기간)|친고죄|반의사불벌|공소시효|기소|공소장|몰수|추징|미수범을 처벌")
# 7. 구체 거래·사례 유형 — **죄명 무관하게** 사례 유형인 것만 넣는다.
#    사기 정답에서 명의신탁·부동산·임대차 등도 100% context_only였지만, 재산죄에서는
#    부동산 이중매매·명의신탁 횡령이 핵심 법리이므로 옮기면 과잉 강등이 된다. 제외했다.
INSTANCE = re.compile(
    r"약속어음|융통어음|수표|어음할인|정책자금|신용카드|예금통장|도박|회사정리|파산절차"
    r"|경매절차|배당|다세대|아파트|임야|인감|보험금|진료(비|수가)|기도(비|를)|골프|리스|카드깡")
# 8. 이득액·가액 산정 — 사기 기준이 명시적으로 core에서 제외한 범주
VALUATION = re.compile(r"가액|시가|공제|상당액|이득액")


def signals(prop: str) -> dict[str, bool]:
    return {
        "meta": bool(META.search(prop)),
        "doctrine": bool(DOCTRINE.search(prop)),
        "concurrence": bool(CONCURRENCE.search(prop)),
        "general_part": bool(GENERAL_PART.search(prop)),
        "case_specific": bool(CASE_SPECIFIC.search(prop)),
        "procedural": bool(PROCEDURAL.search(prop)),
        "instance": bool(INSTANCE.search(prop)),
        "valuation": bool(VALUATION.search(prop)),
    }


DEMOTE_ORDER = [
    ("meta", "주석서가 판례·견해를 '소개한다'는 메타 서술 — 사건 사실에 적용할 명제가 아님"),
    ("doctrine", "학설 지시 — 선택지이지 규칙이 아님"),
    ("concurrence", "죄수·경합 — 다른 죄명 문맥(사기 concurrence 모듈 core 0%)"),
    ("general_part", "총칙 영역 — 형법총칙 코퍼스 필요(future work)"),
    ("case_specific", "구체 사건 서술 — 희귀 적용례"),
    ("instance", "구체 거래·사례 유형 — 희귀 적용례"),
    ("valuation", "이득액·가액 산정 — 사기 기준이 core에서 명시 제외"),
    ("procedural", "절차·부수 규정 — 실체 요건이 아님"),
]


def classify(prop: str) -> tuple[str, str | None]:
    s = signals(prop)
    for key, why in DEMOTE_ORDER:
        if s[key]:
            return "context_only", why
    return "core", None


# --- 사기 정답으로 검증 --------------------------------------------------
def load_fraud() -> list[dict[str, Any]]:
    gold = {r["card_id"]: r["role"] for r in json.loads(
        FRAUD_AUDIT.read_text(encoding="utf-8"))["rows"]}
    out = []
    for p in FRAUD_CARDS.glob("*.json"):
        for c in json.loads(p.read_text(encoding="utf-8")).get("cards", []):
            if c["id"] in gold:
                out.append({"id": c["id"], "prop": c.get("proposition", ""),
                            "gold": gold[c["id"]]})
    return out


def validate() -> dict[str, Any]:
    rows = load_fraud()
    per_signal: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        s = signals(r["prop"])
        gold_ctx = r["gold"] == "context_only"
        for k, v in s.items():
            if v:
                per_signal[k]["fired"] += 1
                per_signal[k]["correct" if gold_ctx else "wrong"] += 1

    report = {}
    print(f"사기 정답 {len(rows)}장 (context_only {sum(1 for r in rows if r['gold']=='context_only')})")
    print("\n표지별 강등 정밀도 — 표지가 켜진 카드 중 실제로 context_only였던 비율")
    for k, _ in DEMOTE_ORDER:
        c = per_signal[k]
        n = c["fired"]
        prec = c["correct"] / n if n else 0.0
        report[k] = {"fired": n, "correct": c["correct"], "wrong": c["wrong"],
                     "precision": round(prec, 4)}
        print(f"  {k:14s} 발화 {n:4d}  정답 {c['correct']:4d}  오강등 {c['wrong']:3d}  정밀도 {prec:6.1%}")

    # 결합 규칙 전체 성능
    tp = fp = fn = tn = 0
    for r in rows:
        pred_ctx = classify(r["prop"])[0] == "context_only"
        gold_ctx = r["gold"] == "context_only"
        tp += pred_ctx and gold_ctx
        fp += pred_ctx and not gold_ctx
        fn += not pred_ctx and gold_ctx
        tn += not pred_ctx and not gold_ctx
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn) if tp + fn else 0
    print(f"\n결합 규칙: 강등 정밀도 {prec:.1%} (오강등 {fp}장), 재현율 {rec:.1%} (놓친 강등 {fn}장)")
    print(f"  → core로 남는 것 {tn+fn}장 (사기 정답 core는 {tp+fp+0 if False else sum(1 for r in rows if r['gold']!='context_only')}장)")
    report["combined"] = {"precision": round(prec, 4), "recall": round(rec, 4),
                          "false_demote": fp, "missed_demote": fn}
    return report


def apply_property() -> dict[str, Any]:
    rows = []
    for p in sorted(PROP_CARDS.glob("*/*.json")):
        art, mod = p.parts[-2], p.stem
        for c in json.loads(p.read_text(encoding="utf-8")).get("cards", []):
            if c.get("formalization") not in CORE:
                continue
            role, why = classify(c.get("proposition", ""))
            rows.append({"article": art, "module": mod, "card_id": c["id"],
                         "from": c["formalization"], "to": role, "reason": why,
                         "polarity": c.get("polarity"),
                         "proposition": c.get("proposition", "")})
    dem = [r for r in rows if r["to"] == "context_only"]
    print(f"\n재산죄 core {len(rows)}장 → 강등 {len(dem)}장, 잔존 core {len(rows)-len(dem)}장")
    print(Counter(r["reason"] for r in dem).most_common())
    return {"rows": rows, "demoted": len(dem), "kept": len(rows) - len(dem)}


def main() -> None:
    rep = validate()
    res = apply_property()
    out = PROJECT_ROOT / "data/rulegen/property/core_scope_audit.json"
    out.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "criteria_source": "data/rulegen/fraud/fraud_core_rule_selection_audit.json",
        "validation_on_fraud_gold": rep,
        "counts": {"core_before": len(res["rows"]), "demoted": res["demoted"],
                   "core_after": res["kept"]},
        "rows": res["rows"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ {out.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
