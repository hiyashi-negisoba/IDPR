"""부정형 카드의 긍정형 neural_query 초안 생성 (API 0회, 규칙 기반).

사기죄 A6 사례를 패턴 앵커로 쓴다:

  카드 원문 : 피기망자로 하여금 처분행위를 하게 할 의사가 **없으면** 사기죄가 성립하지 않는다.
  neural_query: 행위자에게 피기망자로 하여금 바로 그 재산적 처분행위를 하게 할 의사가 **있었다**.
  card_status_when_query_satisfied: not_satisfied

즉 (1) 사건 사실에 관한 **조건절**을 골라 (2) 부정 술어를 긍정 사실주장으로 바꾸고
(3) 귀결절(…성립하지 않는다)은 버린다. 호스트가 부호를 되돌리므로 카드 문언은 원문 유지.

부정형 카드 전부가 질의 대상은 아니다:
  A 요건불요형 (…요구되지 않는다)  → 요건 제외 **규칙**이지 사실 질문이 아님 → 질의 없음
  B 판례소개형 (…판례가 소개되어 있다) → 규범 주장이 아닌 **보고문** → 질의 없음(카드 재분류 대상)
  C 조건부 사실부정형                → 사기 사례와 동형 → **초안 생성**

초안에는 confidence를 붙인다. low는 사용자가 직접 손봐야 하는 것들이다.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEUE = PROJECT_ROOT / "data/rulegen/property/property_norm_card_review_queue.json"
OUT = PROJECT_ROOT / "data/rulegen/property/property_negative_query_drafts.json"

REPORT = re.compile(r"(판례|견해|법리|학설)가?\s*(소개|제시)")
NOREQ = re.compile(r"(요구되지 않|요하지 않|묻지 않|불문|필요 없|필요하지 않|불요)")

# 조건절 경계 (앞부분이 사건 사실 조건)
COND = re.compile(r"^(?P<ante>.+?)(?P<mark>으면|지 않으면|않으면|경우에는|경우|어서|아서|므로|때문에|므로써)(?P<rest>.+)$")

# 부정 술어 → 긍정 사실주장
POSITIVE: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"이 없$"), "이 있었다"),
    (re.compile(r"가 없$"), "가 있었다"),
    (re.compile(r"없$"), "있었다"),
    (re.compile(r"인정되지 않$"), "인정된다"),
    (re.compile(r"성립하지 않$"), "성립한다"),
    (re.compile(r"해당하지 않$"), "해당한다"),
    (re.compile(r"되지 않$"), "된다"),
    (re.compile(r"하지 않$"), "한다"),
    (re.compile(r"볼 수 없$"), "에 해당한다"),
    (re.compile(r"할 수 없$"), "할 수 있다"),
    (re.compile(r"수 없$"), "수 있다"),
    (re.compile(r"아니$"), "이다"),
    (re.compile(r"이 아닌$"), "이다"),
]

TAIL_NEG = re.compile(
    r"(가|이)?\s*(없다|없음|아니다|않는다|못한다|"
    r"인정되지 않는다|성립하지 않는다|해당하지 않는다|볼 수 없다|할 수 없다)\.?$"
)


def positivize(clause: str) -> tuple[str, str]:
    """부정 술어를 긍정 사실주장으로. (문장, confidence)"""
    c = clause.strip().rstrip(",.")
    for pat, rep in POSITIVE:
        if pat.search(c):
            return pat.sub(rep, c), "high"
    # 말미 부정 표현 치환
    m = TAIL_NEG.search(c)
    if m:
        head = c[: m.start()].rstrip()
        neg = m.group(0)
        if "없" in neg:
            return f"{head}가 있었다", "medium"
        if "아니" in neg:
            return f"{head}에 해당한다", "medium"
        if "수 없" in neg:
            return f"{head}할 수 있다", "medium"
        return f"{head}가 인정된다", "medium"
    return c, "low"


def draft(proposition: str) -> dict[str, Any]:
    p = proposition.strip()
    m = COND.match(p)
    if m and len(m.group("ante")) >= 6:
        ante = m.group("ante")
        mark = m.group("mark")
        # '…지 않으면' 형태면 부정이 조건절에 있으므로 그대로 긍정화
        if "않으면" in mark or "으면" in mark:
            q, conf = positivize(ante)
        else:
            q, conf = positivize(ante)
        basis = f"조건절('{ante[:28]}…{mark}')을 긍정 사실주장으로 전환"
    else:
        q, conf = positivize(p)
        basis = "주절 부정 술어를 긍정 사실주장으로 전환"
        conf = "low" if conf == "low" else "medium"
    if not q.endswith(("다", "다.")):
        q = q + "고 인정된다"
        conf = "low"
    return {
        "proposition": q.rstrip(".") + ".",
        "card_status_when_query_satisfied": "not_satisfied",
        "draft_confidence": conf,
        "derivation": basis,
    }


def main() -> None:
    items = json.loads(QUEUE.read_text(encoding="utf-8"))["items"]
    neg = [x for x in items if x["type"] == "3.4_negative_query"]

    drafts: list[dict[str, Any]] = []
    counts = {"A_요건불요": 0, "B_판례소개": 0, "C_초안생성": 0,
              "high": 0, "medium": 0, "low": 0}
    for x in neg:
        p = x["proposition"]
        row = {
            "article": x["article"], "card_id": x["card_id"],
            "double_negative": x.get("double_negative"),
            "proposition": p,
            "human_review": {"decision": None, "notes": None, "approved_query": None},
        }
        if REPORT.search(p):
            counts["B_판례소개"] += 1
            row.update(category="B_판례소개형", neural_query=None,
                       note="규범 주장이 아닌 판례 보고문 → 질의 대상 아님. 카드 재분류(context_only) 검토 필요.")
        elif NOREQ.search(p):
            counts["A_요건불요"] += 1
            row.update(category="A_요건불요형", neural_query=None,
                       note="요건 제외 규칙이지 사실 질문이 아님 → deterministic rule로 처리, 질의 불요.")
        else:
            d = draft(p)
            counts["C_초안생성"] += 1
            counts[d["draft_confidence"]] += 1
            row.update(category="C_조건부사실부정형", neural_query=d,
                       note="사기 A6와 동형. 초안 승인/수정 필요.")
        drafts.append(row)

    # 이중부정 먼저, 그 다음 confidence 낮은 순(손봐야 할 것 우선 노출)
    order = {"low": 0, "medium": 1, "high": 2}
    drafts.sort(key=lambda r: (
        r["category"] != "C_조건부사실부정형",
        not r.get("double_negative"),
        order.get((r.get("neural_query") or {}).get("draft_confidence"), 9),
    ))
    OUT.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "pattern_anchor": {
            "card": "fraud_intent.no_disposition_inducement_intent",
            "original": "피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다.",
            "neural_query": "행위자에게 피기망자로 하여금 바로 그 재산적 처분행위를 하게 할 의사가 있었다.",
            "card_status_when_query_satisfied": "not_satisfied",
        },
        "counts": counts, "items": drafts,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    print(f"→ {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
