"""사용자만 할 수 있는 **법률 결정**만 뽑아 마크다운으로 낸다 (API 0회).

구조적 지적(누락 견해 추가, 병합 카드 분리, variant_group 부여, coverage_gaps,
review_question 문구, 끊긴 candidate_refs, 권위 라벨 정규화)은 전부 에이전트 몫이라
이 문서에 넣지 않는다.

남기는 것은 셋뿐이고, 그중 3.1은 구조 정리가 끝나야 선택지가 확정되므로 별도 발행한다.

  A. 출처 범위 판정 (3.3)  — 카드가 출처보다 넓은지. 예/아니오 판정만 하면
                             좁히는 작업은 에이전트가 한다.
  B. 긍정형 질의문 승인 (3.4) — 에이전트가 쓴 초안을 confirm/수정. 활성 질의문은
                             사용자 승인이 필요하다(prompt-approval-gate).
  C. 학설 선택 (3.1)      — **보류**. 누락 견해 추가·분리 후 선택지가 바뀐다.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DS = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
REM = PROJECT_ROOT / "data/rulegen/property/remediated"
OUT = PROJECT_ROOT / "data/rulegen/property"

SCOPE_TYPES = {"overgeneralization", "source_scope", "source_entailment", "rule_mismatch"}
ASK = {
    "overgeneralization": "출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.",
    "source_scope": "카드가 출처에 없는 내용까지 담았다는 지적입니다.",
    "source_entailment": "출처가 이 명제를 지지하지 않는다는 지적입니다.",
    "rule_mismatch": "카드 명제와 출처 규범이 어긋난다는 지적입니다.",
}


def load_cards() -> dict[tuple[str, str], list[dict[str, Any]]]:
    """정리(remediated) 후 카드셋을 쓴다 — 강등·라벨정규화가 반영된 상태."""
    return {(p.parts[-2], p.stem): json.loads(p.read_text(encoding="utf-8")).get("cards", [])
            for p in REM.glob("*/*.json")}


def load_sets() -> dict[tuple[str, str], dict[str, Any]]:
    return {(p.parts[-2], p.stem): json.loads(p.read_text(encoding="utf-8"))
            for p in REM.glob("*/*.json")}


def resolve(cards: list[dict[str, Any]], part: int, tp: str | None):
    t = (tp or "").replace("/", ".")
    m = re.search(r"cards[\.\[](\d+)", t)
    if not m:
        return None
    seg = cards[(part - 1) * 50: part * 50]
    i = int(m.group(1))
    return seg[i] if i < len(seg) else None


def main() -> None:
    cards_by = load_cards()

    # ---- A. 출처 범위 판정 ----
    rows: list[dict[str, Any]] = []
    for sp in sorted(DS.glob("art*/*/sol/*.json")):
        art = sp.parts[-4]
        m = re.match(r".+\.normcards\.(.+)\.part(\d+)\.critic\.json$", sp.name)
        if not m:
            continue
        mod, part = m.group(1), int(m.group(2))
        for f in json.loads(sp.read_text(encoding="utf-8")).get("findings", []):
            ft = f.get("type")
            if ft not in SCOPE_TYPES:
                continue
            card = resolve(cards_by.get((art, mod), []), part, f.get("target_path"))
            if card is None or card.get("formalization") not in (
                    "deterministic_rule", "standard_input"):
                continue          # 결론에 안 흘러드는 카드는 굳이 안 물어본다
            qs = [r.get("quote", "") for r in card.get("source_refs", []) if r.get("quote")]
            rows.append({
                "article": art, "module": mod, "card_id": card.get("id"),
                "proposition": card.get("proposition", ""),
                "quote": (qs[0] if qs else "(인용 없음)")[:400],
                "ask": ASK.get(ft, ""), "finding": (f.get("message") or "").strip(),
            })

    g = ["# 검토 A — 카드가 출처 범위를 넘었는지 판정\n",
         f"총 **{len(rows)}건**. 결론에 흘러드는 카드(Scallop 규칙·모델 판단 입력)만 담았습니다.\n",
         "## 하실 일\n",
         "각 항목에서 **카드 명제**와 **출처 원문**을 비교해 한 가지만 답해 주세요.\n",
         "- `넓음` — 출처보다 넓습니다 → **제가 출처 범위로 좁히겠습니다**",
         "- `괜찮음` — 이 정도 일반화는 타당합니다 → 그대로 둡니다",
         "- 비워두시면 `괜찮음`으로 처리합니다.\n",
         "좁히는 문장 작성은 제가 합니다. 판정만 해주시면 됩니다.\n"]
    cur = None
    for i, r in enumerate(rows, 1):
        if (r["article"], r["module"]) != cur:
            cur = (r["article"], r["module"])
            g.append(f"\n---\n\n## {r['article']} / {r['module']}\n")
        g.append(f"### {i}. `{r['card_id']}`\n")
        g.append(f"**카드 명제**\n> {r['proposition']}\n")
        g.append(f"**출처 원문**\n> {r['quote']}\n")
        g.append(f"**지적**: {r['ask']}\n")
        g.append(f"<details><summary>상세</summary>\n\n{r['finding']}\n\n</details>\n")
        g.append("**판정 (넓음 / 괜찮음):** \n")
    (OUT / "결정A_출처범위판정.md").write_text("\n".join(g) + "\n", encoding="utf-8")

    # ---- B. 긍정형 질의문 승인 ----
    dp = OUT / "property_negative_query_drafts.json"
    drafts = json.loads(dp.read_text(encoding="utf-8"))["items"] if dp.exists() else []
    d = [x for x in drafts if x.get("neural_query")]
    d.sort(key=lambda x: (not x.get("double_negative"), x["article"]))
    g = ["# 검토 B — 긍정형 질의문 승인\n",
         f"총 **{len(d)}건**. 부정형 카드는 모델이 이중부정을 못 읽어 오판하므로, "
         "호스트가 **긍정형으로 물어보고 부호를 되돌립니다**(사기 A6에서 확정된 방식).\n",
         "## 하실 일\n",
         "초안 문장이 그 카드의 사실 쟁점을 맞게 묻고 있는지만 봐주세요.\n",
         "- 맞으면 비워두시면 됩니다(= 승인).",
         "- 틀리면 `수정:` 뒤에 문장을 고쳐 적어주세요.",
         "- **극성**도 함께 봐주세요: 질의가 참일 때 카드가 `성립`인지 `불성립`인지입니다.\n",
         "이중부정 카드부터 정렬했습니다(가장 오판이 잦은 유형).\n"]
    for i, x in enumerate(d, 1):
        nq = x["neural_query"]
        dn = " ⚠️이중부정" if x.get("double_negative") else ""
        g.append(f"\n### {i}. `{x['card_id']}`{dn}\n")
        g.append(f"**카드 원문 (부정형)**\n> {x['proposition']}\n")
        g.append(f"**질의문 초안 (긍정형)**\n> {nq['proposition']}\n")
        st = nq["card_status_when_query_satisfied"]
        ko = "**불성립** (질의가 참이면 이 카드는 작동 안 함)" if st == "not_satisfied" \
            else "**성립** (질의가 참이면 이 카드가 작동함)"
        g.append(f"**극성**: 질의가 참일 때 → {ko}\n")
        g.append("**수정:** \n")
    (OUT / "결정B_질의문승인.md").write_text("\n".join(g) + "\n", encoding="utf-8")

    print(f"A 출처범위 판정 {len(rows)}건 → 결정A_출처범위판정.md")
    print(f"B 질의문 승인 {len(d)}건 → 결정B_질의문승인.md")
    print("C 학설 선택 → 구조 정리(누락견해 추가·분리) 후 발행")


if __name__ == "__main__":
    main()
