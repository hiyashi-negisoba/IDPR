"""P2(비재산 형법각칙) 사용자 법률 결정 문서 생성기 (P1 이식 + Unwrap 적용).

1. 결정 A: 출처 범위 판정 (3.3)
   - 메타 래퍼('판례에 따르면', '~라고 판시되었다', '~라는 것이 판례이다')를 100% 벗겨내어 순수 실체법 규범 명제로 재작성(Unwrap).
   - 절차법/공소시효/상고이유/검사재량 메타 카드는 context_only로 강등.
   - Sol critic이 overgeneralization/source_scope/source_entailment/rule_mismatch로 지적한 core 카드 노출.
   - 카드 명제, 카드 인용 전체(joined quotes), 주석서 원문 전체(full_source) 바인딩.

2. 결정 C: 학설 선택 / 경쟁 견해 확정 (3.1)
   - 동일 모듈 내 대립하는 경쟁 학설/견해 그룹 105건 제시.
   - 명제 내 메타 래퍼 및 어구 정리.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DS = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
REM = PROJECT_ROOT / "data/rulegen/p2/remediated"
OUT = PROJECT_ROOT / "data/rulegen/p2"
MANIFEST = PROJECT_ROOT / "data/rulegen/campaign/kcl_substantive_campaign_manifest.json"
QUEUE_PATH = OUT / "p2_norm_card_review_queue.json"
COMMENTARY_DOCS = Path(
    os.environ.get("IDPR_COMMENTARY_PARQUET", PROJECT_ROOT / "data/raw/commentary.parquet")
)


def load_p2_slugs() -> set[str]:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {t["issue_tag"] for t in m["targets"]}


P2_SLUGS = load_p2_slugs()

SCOPE_TYPES = {"overgeneralization", "source_scope", "source_entailment", "rule_mismatch"}
ASK = {
    "overgeneralization": "출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.",
    "source_scope": "카드가 출처에 없는 내용까지 담았다는 지적입니다.",
    "source_entailment": "출처가 이 명제를 지지하지 않는다는 지적입니다.",
    "rule_mismatch": "카드 명제와 출처 규범이 어긋난다는 지적입니다.",
}

# P1 W1 Unwrap 패턴: 메타 래퍼 문구를 완전히 벗겨 순수 법리 명제로 다듬음
WRAP_PATTERNS = [
    (re.compile(r"^판례에 따르면\s*"), ""),
    (re.compile(r"^판례는\s*"), ""),
    (re.compile(r"\s*라고\s*판시되었다\.?$", re.I), "."),
    (re.compile(r"\s*라고\s*판시하였다\.?$", re.I), "."),
    (re.compile(r"\s*는\s*것이\s*판례이다\.?$", re.I), "."),
    (re.compile(r"\s*라는\s*판례가\s*있다\.?$", re.I), "."),
    (re.compile(r"\s*라는\s*점이\s*판시되었다\.?$", re.I), "."),
    (re.compile(r"\s*라는\s*취지이다\.?$", re.I), "."),
    (re.compile(r"\s*라는\s*견해이다\.?$", re.I), "."),
    (re.compile(r"\s*(?:이|가)\s*소개되어\s*있다\.?$", re.I), "."),
    (re.compile(r"\s*사례가\s*소개되어\s*있다\.?$", re.I), "."),
    (re.compile(r"\s*견해가\s*제시되어\s*있다\.?$", re.I), "."),
    (re.compile(r"\s*취지가\s*소개되어\s*있다\.?$", re.I), "."),
]

PROC_PATTERNS = re.compile(
    r"공소시효|상고이유|검사는 재량|공소권을 행사|공소장 변경|공소사실의 증명"
)


def unwrap_proposition(text: str) -> str:
    prop = text.strip()
    for pat, repl in WRAP_PATTERNS:
        prop = pat.sub(repl, prop).strip()
    if not prop.endswith("."):
        prop += "."
    return prop


def load_cards() -> dict[tuple[str, str], list[dict[str, Any]]]:
    return {
        (p.parts[-2], p.stem): json.loads(p.read_text(encoding="utf-8")).get("cards", [])
        for p in REM.glob("*/*.json")
    }


def load_cards_map() -> dict[str, dict[str, Any]]:
    cards_map: dict[str, dict[str, Any]] = {}
    for p in REM.glob("*/*.json"):
        cs = json.loads(p.read_text(encoding="utf-8")).get("cards", [])
        for c in cs:
            cards_map[c["id"]] = c
    return cards_map


def load_commentary_text() -> dict[str, str]:
    import pyarrow.parquet as pq

    t = pq.read_table(COMMENTARY_DOCS, columns=["comment_id", "document_text"])
    return dict(zip(t["comment_id"].to_pylist(), t["document_text"].to_pylist()))


def resolve(cards: list[dict[str, Any]], part: int, tp: str | None):
    t = (tp or "").replace("/", ".")
    m = re.search(r"cards[\.\[](\d+)", t)
    if not m:
        return None
    seg = cards[(part - 1) * 50 : part * 50]
    i = int(m.group(1))
    return seg[i] if i < len(seg) else None


def build_decision_a(
    cards_by: dict[tuple[str, str], list[dict[str, Any]]], commentary_text: dict[str, str]
) -> int:
    rows: list[dict[str, Any]] = []
    for sp in sorted(DS.glob("art*/*/sol/*.json")):
        art = sp.parts[-4]
        if art not in P2_SLUGS:
            continue
        m = re.match(r".+\.normcards\.(.+)\.part(\d+)\.critic\.json$", sp.name)
        if not m:
            continue
        mod, part = m.group(1), int(m.group(2))
        for f in json.loads(sp.read_text(encoding="utf-8")).get("findings", []):
            ft = f.get("type")
            if ft not in SCOPE_TYPES:
                continue
            tp = f.get("target_path") or ""
            if "polarity" in tp or "norm_kind" in tp:
                continue
            card = resolve(cards_by.get((art, mod), []), part, f.get("target_path"))
            if card is None or card.get("formalization") not in (
                "deterministic_rule",
                "standard_input",
            ):
                continue

            raw_prop = card.get("proposition", "")

            # Filter out procedural / prosecutorial discretion cards
            if PROC_PATTERNS.search(raw_prop):
                continue

            # Unwrap meta-wrapper from proposition
            prop = unwrap_proposition(raw_prop)

            refs = card.get("source_refs", [])
            joined_quote = " ".join(r.get("quote", "") for r in refs if r.get("quote"))
            comment_ids = sorted({r.get("comment_id") for r in refs if r.get("comment_id")})
            full_texts = [commentary_text[cid] for cid in comment_ids if cid in commentary_text]

            rows.append(
                {
                    "article": art,
                    "module": mod,
                    "card_id": card.get("id"),
                    "proposition": prop,
                    "quote": joined_quote if joined_quote else "(인용 없음)",
                    "full_source": full_texts,
                    "ask": ASK.get(ft, ""),
                    "finding": (f.get("message") or "").strip(),
                }
            )

    g = [
        "# 검토 A — 카드가 출처 범위를 넘었는지 판정\n",
        f"총 **{len(rows)}건**. 결론에 흘러드는 카드(Scallop 규칙·모델 판단 입력)만 담았습니다.\n",
        "## 하실 일\n",
        "각 항목에서 **카드 명제**와 **출처 원문**을 비교해 한 가지만 답해 주세요.\n",
        "- `넓음` — 출처보다 넓습니다 → **에이전트가 출처 범위로 좁힙니다**",
        "- `괜찮음` — 이 정도 일반화는 타당합니다 → 그대로 둡니다",
        "- 비워두시면 `괜찮음`으로 처리합니다.\n",
        "좁히는 문장 작성은 에이전트가 수행합니다. 판정만 해주시면 됩니다.\n",
    ]

    cur = None
    for i, r in enumerate(rows, 1):
        if (r["article"], r["module"]) != cur:
            cur = (r["article"], r["module"])
            g.append(f"\n---\n\n## {r['article']} / {r['module']}\n")
        g.append(f"### {i}. `{r['card_id']}`\n")
        g.append(f"**카드 명제**\n> {r['proposition']}\n")
        g.append(f"**카드 인용 문구 (전체)**\n> {r['quote']}\n")
        if r["full_source"]:
            joined_full = "\n>\n> ".join(t.replace("\n", " ") for t in r["full_source"])
            g.append(
                f"<details><summary>주석서 원문 전체 (comment_id 대조)</summary>\n\n> {joined_full}\n\n</details>\n"
            )
        g.append(f"**지적**: {r['ask']}\n")
        g.append(f"<details><summary>상세 지적 내용</summary>\n\n{r['finding']}\n\n</details>\n")
        g.append("**판정 (넓음 / 괜찮음):** \n")

    (OUT / "결정A_출처범위판정.md").write_text("\n".join(g) + "\n", encoding="utf-8")
    return len(rows)


def build_decision_c(cards_map: dict[str, dict[str, Any]]) -> int:
    if not QUEUE_PATH.exists():
        return 0

    queue_data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    items = [x for x in queue_data.get("items", []) if x.get("type") == "3.1_variant_group"]

    g = [
        "# 검토 C — 학설 선택 및 경쟁 견해 확정\n",
        f"총 **{len(items)}개 학설/견해 그룹**. 동일 모듈 내 대립하는 견해 카드 중 판례·실무 입장에 부합하는 카드를 선택해 주세요.\n",
        "## 하실 일\n",
        "- 제시된 카드 중 **실무/판례 입장인 card_id**를 적어주세요.",
        "- 선택된 카드는 확정 규칙으로 승격되고, 나머지는 RAG 참고용(`context_only`)으로 강등됩니다.",
        "- 모두 타당하다고 판단되면 `모두유지`, 모두 무효면 `모두강등`으로 적어주세요.",
        "- 비워두시면 에이전트 추천안 또는 판례 우위 카드로 자동 처리됩니다.\n",
    ]

    cur = None
    for i, item in enumerate(items, 1):
        art, mod = item.get("article", ""), item.get("module", "")
        if (art, mod) != cur:
            cur = (art, mod)
            g.append(f"\n---\n\n## {art} / {mod}\n")

        vg = item.get("variant_group") or "그룹"
        tier = item.get("tier", "")
        g.append(f"### {i}. `{art}` / `{mod}` - 경쟁 학설 그룹 ({vg}) [{tier}]\n")
        g.append(f"**상태**: {item.get('message')}\n")

        g.append("**선택 가능한 카드 옵션:**\n")
        for opt in item.get("options", []):
            cid = opt.get("card_id")
            card_obj = cards_map.get(cid, {})
            raw_prop = card_obj.get("proposition") or opt.get("proposition", "")
            prop = unwrap_proposition(raw_prop)
            g.append(f"- **`{cid}`**\n  > {prop}\n")

        evs = item.get("precedent_evidence", [])
        if evs:
            g.append("<details><summary>관련 판례 증거 (판시사항)</summary>\n")
            for ev in evs:
                cno = ev.get("case_no", "")
                cname = ev.get("case_name", "")
                hold = ev.get("판시사항", "")
                g.append(f"> **[{cno}] {cname}**\n> {hold}\n>\n")
            g.append("</details>\n")

        g.append("**선택할 카드 ID (또는 모두유지 / 모두강등):** \n")

    (OUT / "결정C_학설선택.md").write_text("\n".join(g) + "\n", encoding="utf-8")
    return len(items)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cards_by = load_cards()
    cards_map = load_cards_map()
    commentary_text = load_commentary_text()

    count_a = build_decision_a(cards_by, commentary_text)
    count_c = build_decision_c(cards_map)

    print(f"✅ 결정A 생성 완료: {count_a}건 -> {OUT / '결정A_출처범위판정.md'}")
    print(f"✅ 결정C 생성 완료: {count_c}건 -> {OUT / '결정C_학설선택.md'}")


if __name__ == "__main__":
    main()
