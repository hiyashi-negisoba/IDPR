"""결정 B(긍정형 질의문 승인) 재발행 — 최종 core set 기준.

구판 190건은 모수가 틀렸다. core scope 감사 **전** 카드셋에 대고 초안했기 때문에
RAG 문맥으로 내려갈 카드가 대거 섞여 있었다. 최종 core 452장 기준으로 다시 짠다.

  negative 극성 최종 core 106장
    ├ 구판 초안 있음        87  → confirm/수정 (사용자)
    ├ 요건불요형(질의 불요)   7  → 자동 (요건 제외 규칙이지 사실 질문이 아님)
    └ 초안 없음             12  → 이번에 신규 작성 (사용자)

12장이 구판에 없던 이유: 초안은 remediation 이전(12:35) 카드셋에서 만들었고 remediated/
반영(15:52)에서 늘어난 negative core가 반영되지 않았다.

API 0회.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

# 신규 작성분 — 조건절의 사실 쟁점을 긍정형으로 묻고 호스트가 부호를 되돌린다(A6).
NEW: dict[str, tuple[str, str]] = {
    "art329_sec2.theft_exception_ownership_or_self_possession": (
        "취거한 재물은 타인의 소유이면서 동시에 타인의 점유 아래 있었다.", "not_satisfied"),
    "art329_sec2_2.sole_custodian_coowned_property": (
        "그 재물은 공동소유자들의 공동점유가 아니라 행위자 1인의 단독보관 아래 있었다.", "satisfied"),
    "art331_sec3_1.toy_gun_not_weapon_exception": (
        "휴대한 물건은 객관적으로 살상·파괴에 쓰일 수 있는 흉기의 성질을 가지고 있었다.", "not_satisfied"),
    "art335_sec3_1.pre_control_violence_is_robbery_exception": (
        "폭행·협박 당시 행위자는 재물에 대한 배타적 지배를 아직 확립하지 못한 상태였고, "
        "그 지배를 확보하기 위하여 폭행·협박을 하였다.", "satisfied"),
    "art337_sec3_2.trivial_injury_excluded": (
        "피해자가 입은 상처는 치료를 요하거나 일상생활에 지장을 줄 정도였다.", "not_satisfied"),
    "art337_sec3_2.robbery_occasion_ended": (
        "상해행위는 강도 현장이나 추적이 계속되는 상황에서 강도행위와 시간적·장소적으로 "
        "근접하여 이루어졌다.", "not_satisfied"),
    "art343.special_robbery_attempt_home_invasion": (
        "행위자는 강도 목적으로 야간에 피해자의 주거에 침입하였다.", "satisfied"),
    "art350_sec3.own_property_exception": (
        "갈취의 대상이 된 재물 또는 재산상 이익은 타인에게 속하는 것이었다.", "not_satisfied"),
    "art350_sec8_2.permitted_threat_no_extortion": (
        "권리행사 과정에서 한 위협적 언사가 사회통념상 허용되는 범위를 넘어섰다.", "not_satisfied"),
    "art355_sec3_3.simple_destruction_exception": (
        "행위자의 행위는 목적물의 단순한 손괴에 그치지 않고 이를 자기 소유물처럼 사실상 또는 "
        "법률상 처분하는 것이었다.", "not_satisfied"),
    "art355_sec4_2.breach_for_principal_no_illicit_gain": (
        "행위자는 본인이 아니라 자기 또는 제3자의 이익을 위하여 그 사무를 처리하였다.", "not_satisfied"),
    "art355_sec7_3.breach_property_not_stolen_goods": (
        "취득 또는 전득한 물건은 배임행위에 제공된 물건이었다.", "satisfied"),
}

DOUBLE_NEG = re.compile(r"(없|않|아니|못)[^.]{0,25}(없|않|아니|못)")
LEAK = re.compile(r"죄가 성립|죄에 해당|죄로 처벌|죄가 인정")


def main() -> None:
    fin = {r["card_id"]: r for r in json.loads(
        (PROP / "property_core_set_final.json").read_text(encoding="utf-8"))["rows"]}
    drafts = {i["card_id"]: i for i in json.loads(
        (PROP / "property_negative_query_drafts.json").read_text(encoding="utf-8"))["items"]}

    items, no_query, dropped = [], [], []
    for cid, r in fin.items():
        if r["final_role"] == "context_only" or r["polarity"] != "negative":
            continue
        d = drafts.get(cid)
        if cid in NEW:
            q, status, origin = NEW[cid][0], NEW[cid][1], "신규"
        elif d and isinstance(d.get("neural_query"), dict):
            q, status, origin = (d["neural_query"]["proposition"],
                                 d["neural_query"]["card_status_when_query_satisfied"], "구판")
        else:
            no_query.append({"card_id": cid, "proposition": r["proposition"],
                             "reason": (d or {}).get("note", "요건 제외 규칙 → 사실 질문 아님")})
            continue
        assert not LEAK.search(q), f"결론 누설 질의: {cid}"
        items.append({"card_id": cid, "article": r["article"], "module": r["module"],
                      "proposition": r["proposition"], "neural_query": q,
                      "card_status_when_query_satisfied": status, "origin": origin,
                      "double_negative": bool(DOUBLE_NEG.search(r["proposition"])),
                      "human_review": {"decision": None, "approved_query": None, "notes": None}})
    for cid, d in drafts.items():
        if isinstance(d.get("neural_query"), dict) and \
                fin.get(cid, {}).get("final_role") == "context_only":
            dropped.append({"card_id": cid, "reason": fin[cid]["reason"],
                            "demoted_at": fin[cid]["demoted_at"]})

    # 이중부정 먼저, 그다음 신규
    items.sort(key=lambda x: (not x["double_negative"], x["origin"] != "신규", x["card_id"]))

    out = {"version": "2.0.0", "api_calls": 0,
           "created_at": datetime.now(timezone.utc).isoformat(),
           "basis": "property_core_set_final.json (merge core 896 → 최종 core 452)",
           "supersedes": "결정B_질의문승인.md (190건, core scope 감사 전 모수)",
           "counts": {"review": len(items), "신규작성": sum(1 for i in items if i["origin"] == "신규"),
                      "구판유지": sum(1 for i in items if i["origin"] == "구판"),
                      "이중부정": sum(1 for i in items if i["double_negative"]),
                      "질의불요": len(no_query), "구판에서_강등탈락": len(dropped)},
           "items": items, "no_query_needed": no_query, "dropped_from_v1": dropped}
    (PROP / "property_negative_query_drafts_v2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    g = ["# 검토 B (재발행) — 긍정형 질의문 승인", "",
         f"총 **{len(items)}건**. 구판 190건은 core scope 감사 **전** 카드셋으로 만든 것이라 "
         f"폐기했습니다 — 그중 {len(dropped)}건은 RAG 문맥으로 내려가 질의문 자체가 불필요해졌습니다.",
         "", f"대신 구판에 빠져 있던 **{out['counts']['신규작성']}건**을 새로 작성해 넣었습니다"
         "(remediation 이후 늘어난 카드가 구판에 반영되지 않았습니다).", "",
         "## 왜 카드는 명제인데 질의문은 사실진술인가", "",
         "카드는 **규칙**이고(Scallop이 씁니다), 질의문은 그 규칙의 **조건이 이 사건에 있는지** "
         "모델에게 묻는 문장입니다. 층위가 다른 것이 설계입니다. 부정형 카드를 그대로 물으면 "
         "모델이 이중부정에서 부호를 뒤집으므로(사기 A6 실측: 5회 중 3회 → 긍정형 전환 후 8회 중 0회) "
         "긍정으로 묻고 호스트가 부호를 되돌립니다. **극성** 표시가 그 되돌림 방향입니다.", "",
         "## 하실 일", "",
         "- 초안이 그 카드의 사실 쟁점을 맞게 묻고 있으면 비워두시면 됩니다(= 승인).",
         "- 틀리면 `수정:` 뒤에 문장을 고쳐 적어주세요.",
         "- **극성**도 함께 봐주세요.", "",
         "이중부정 카드를 앞에, 그다음 신규 작성분을 뒀습니다.", ""]
    for n, it in enumerate(items, 1):
        tags = []
        if it["double_negative"]:
            tags.append("⚠️이중부정")
        if it["origin"] == "신규":
            tags.append("🆕신규")
        pol = ("**불성립** (질의가 참이면 이 카드는 작동 안 함)"
               if it["card_status_when_query_satisfied"] == "not_satisfied"
               else "**성립** (질의가 참이면 이 카드가 작동함)")
        g += [f"### {n}. `{it['card_id']}` {' '.join(tags)}", "",
              "**카드 원문 (부정형)**", f"> {it['proposition']}", "",
              "**질의문 초안 (긍정형)**", f"> {it['neural_query']}", "",
              f"**극성**: 질의가 참일 때 → {pol}", "", "**수정:** ", ""]
    g += ["---", "", f"## 참고 — 질의 불요 {len(no_query)}건 (확인만)", "",
          "요건을 **제외하는 규칙**이라 물어볼 사실이 없는 카드입니다.", ""]
    for it in no_query:
        g += [f"- `{it['card_id']}` — {it['proposition'][:120]}"]
    (PROP / "결정B_질의문승인_v2.md").write_text("\n".join(g) + "\n", encoding="utf-8")

    print(f"검토 대상 {len(items)}건 (구판유지 {out['counts']['구판유지']} + "
          f"신규 {out['counts']['신규작성']}), 이중부정 {out['counts']['이중부정']}")
    print(f"질의 불요 {len(no_query)}건 · 구판에서 강등 탈락 {len(dropped)}건")
    print("→ data/rulegen/property/결정B_질의문승인_v2.md")


if __name__ == "__main__":
    main()
