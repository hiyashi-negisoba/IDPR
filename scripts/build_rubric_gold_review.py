"""Render the 죄명 → 조문 review document from the draft map plus the rubric text.

The rubric text is the point. A reviewer cannot decide "준강도치상죄는 어느 조문인가" from
a slug and a count; they can decide it in one pass when the rubric item that uses the term
is sitting directly above the question. Four previous review documents failed on exactly
this, so the layout here is fixed: statute table at the top (scannable), evidence directly
above each question, and one answer line per question.

Regeneration never clobbers review. If the file already carries an answered ``> comment:``
line, the script refuses unless ``--rewrite`` is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

from idpr.rulebase.cards import card_corpus
from idpr.rulebase.compile_scl import ArticleLabelError, article_label

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = PROJECT_ROOT / "data" / "eval" / "rubric_crime_article_map.json"
INVENTORY_PATH = PROJECT_ROOT / "data" / "inventory" / "kcl_criminal_v1_draft.jsonl"
PARQUET_PATH = Path(
    os.environ.get("IDPR_KCL_PARQUET", PROJECT_ROOT / "data/raw/kcl_essay_test.parquet")
)
OUT_PATH = PROJECT_ROOT / "docs" / "rubric_crime_article_review.md"

CRIME_RE = re.compile(r"[가-힣0-9]{2,14}죄")  # 제3자뇌물…: digits or the name truncates
# ``[^\S\n]`` and not ``\s``: ``\s*`` crosses the newline and matches the ``#`` of the next
# heading, so every empty comment line reads as answered and the guard fires always.
ANSWERED = re.compile(r"^> comment:[^\S\n]*\S", re.MULTILINE)
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def has_answers(document: str) -> bool:
    """Whether the reviewer has written anything.

    Fenced blocks are stripped first: the document shows worked ``> comment:`` examples in
    a code fence, and counting those as answers would make the overwrite guard fire on
    every regeneration -- which trains everyone to pass ``--rewrite`` reflexively, and then
    it stops protecting anything.
    """
    return bool(ANSWERED.search(FENCE.sub("", document)))


def article_titles() -> dict[str, str]:
    """``art298`` -> ``제298조 강제추행``, from commentary target metadata.

    Headings the manifest never carried (no KCL tag pointed at those articles) come from
    the map asset's ``article_titles_supplement``, not from a literal here.
    """
    supplement = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    titles: dict[str, str] = dict(supplement.get("article_titles_supplement", {}).get("titles", {}))
    manifest = (
        PROJECT_ROOT / "data" / "commentary" / "kcl_criminal_v1_tag_commentary_manifest.jsonl"
    )
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        for target in json.loads(line).get("targets", []):
            if target.get("law_id") == "001692":
                titles.setdefault(target["article_no"], target.get("article_title", ""))
    return titles


def rubric_occurrences() -> dict[str, list[tuple[str, str]]]:
    """``죄명`` -> [(sub_question_id, rubric item text)], in inventory order."""
    frame = pd.read_parquet(PARQUET_PATH)
    inventory = [
        json.loads(line)
        for line in INVENTORY_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    occurrences: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for record in inventory:
        row_index = record["source"]["source_row_index"]
        for item in frame.iloc[row_index]["rubrics"]:
            text = str(item)
            for crime in dict.fromkeys(CRIME_RE.findall(text)):
                occurrences[crime].append((record["sub_question_id"], text))
    return occurrences


def render(draft: dict, occurrences: dict[str, list[tuple[str, str]]]) -> str:
    corpus = card_corpus()
    titles = article_titles()
    labels: dict[str, str] = {}
    for article in corpus.by_article():
        try:
            labels[article] = article_label(article)
        except ArticleLabelError:
            labels[article] = article

    crimes = draft["crimes"]
    review = {c: v for c, v in crimes.items() if v["confidence"] == "review"}
    clear = {c: v for c, v in crimes.items() if v["confidence"] == "clear"}
    non_offence = {c: v for c, v in crimes.items() if v["confidence"] == "not_an_offence"}

    lines: list[str] = []
    add = lines.append

    add("# 검수 요청 — 루브릭 죄명 → 조문")
    add("")
    add(
        f"L0 검색의 쟁점 리콜을 채점하려면 루브릭이 말하는 죄명이 어느 조문인지가 필요하다. "
        f"루브릭 표기 **{len(crimes)}종** 중 **{len(review)}종만 답해주면 된다**(A절)."
    )
    add("")
    add(
        "이전 골드였던 `issue_tags`는 KCL 데이터가 아니라 에이전트가 손으로 붙인 것이어서 "
        "폐기했다. 루브릭은 parquet 원본 `rubrics` 컬럼이라 진짜 gold이고, 죄명이 그대로 "
        "적혀 있다."
    )
    add("")
    add("**초안을 채워 뒀다.** 조문 번호 확인은 법률 사실 조회이지 우리 시스템에 대한 판단이")
    add("아니므로 초안이 채점을 오염시키지 않는다. 맞으면 그대로 두고, 틀린 것만 고치면 된다.")
    add("")
    add("## 답하는 법")
    add("")
    add("각 항목의 `> comment:` 줄 오른쪽에 적는다. 비워두면 **초안대로 확정**된다.")
    add("")
    add("```")
    add("> comment: art335, art337        ← 조문 키 (여러 개면 쉼표)")
    add("> comment: 코퍼스에 없음          ← 51조문 밖")
    add("> comment: 죄명 아님              ← 죄명 표기가 아님")
    add("```")
    add("")

    add("## 조문 키 51개")
    add("")
    add("| 키 | 조문 | 표제 | 키 | 조문 | 표제 |")
    add("|---|---|---|---|---|---|")
    ordered = sorted(labels, key=lambda a: (len(labels[a]), labels[a]))
    half = (len(ordered) + 1) // 2
    for left, right in zip(ordered[:half], ordered[half:] + [""] * half):
        cells = [f"`{left}`", labels[left], titles.get(labels[left], "")]
        if right:
            cells += [f"`{right}`", labels[right], titles.get(labels[right], "")]
        else:
            cells += ["", "", ""]
        add("| " + " | ".join(cells) + " |")
    add("")
    add("---")
    add("")

    add(f"# A. 답해야 할 것 — {len(review)}종")
    add("")
    for crime in sorted(review, key=lambda c: -len(occurrences.get(c, []))):
        entry = review[crime]
        items = occurrences.get(crime, [])
        add(f"## `{crime}`")
        add("")
        if entry.get("note"):
            add(f"*{entry['note']}*")
            add("")
        add(f"**이 표기가 쓰인 루브릭 항목 {len(items)}개** — 이걸 보고 조문을 정한다.")
        add("")
        for sub_question_id, text in items[:6]:
            add(f"- ({sub_question_id}) {text}")
        if len(items) > 6:
            add(f"- … 외 {len(items) - 6}개")
        add("")
        draft_answer = ", ".join(entry["articles"]) if entry["articles"] else "코퍼스에 없음"
        add(f"**초안**: {draft_answer}")
        add("")
        add("> comment: ")
        add("")

    add("---")
    add("")
    add(f"# B. 확인만 — {len(clear)}종")
    add("")
    add("표제와 그대로 대응하거나 파생형(교사·미수)이라 초안이 자명한 것들이다.")
    add("**틀린 것만 지적하면 되고, 침묵은 승인이다.**")
    add("")
    add("| 죄명 | 초안 조문 | 파생 | 루브릭 항목 수 |")
    add("|---|---|---|---:|")
    for crime in sorted(clear, key=lambda c: -len(occurrences.get(c, []))):
        entry = clear[crime]
        articles = ", ".join(f"`{a}`" for a in entry["articles"]) or "—"
        derived = {"attempt": "미수", "instigation": "교사·방조"}.get(entry.get("derived", ""), "")
        add(f"| {crime} | {articles} | {derived} | {len(occurrences.get(crime, []))} |")
    add("")
    add("> comment: ")
    add("")

    add("---")
    add("")
    add(f"# C. 죄명이 아니라고 본 것 — {len(non_offence)}종")
    add("")
    add("죄수·소추조건 용어이거나 정규식이 잘라낸 표기 단편이다. 채점 대상에서 뺀다.")
    add("**여기 죄명이 섞여 있으면 지적해달라.**")
    add("")
    add("| 표기 | 사유 |")
    add("|---|---|")
    for crime in sorted(non_offence):
        add(f"| {crime} | {non_offence[crime].get('note', '')} |")
    add("")
    add("> comment: ")
    add("")

    add("---")
    add("")
    add("# 미수 준용에 관한 확인 1건")
    add("")
    add(
        "기본죄가 gold에 들어가면 그 죄의 **미수범 조문도 함께** 넣으려 한다"
        "(살인 → 제250조 + 제254조, 절도·강도류 → + 제342조, 성범죄 → + 제300조)."
    )
    add("")
    add(
        "근거는 조문 자체가 준용을 명시한다는 것이지 정답 목록이 아니다. 다만 이 조문들은 "
        "사실관계 어휘와 겹칠 것이 원리적으로 없어 검색으로는 절대 회수되지 않으므로, "
        "gold에 넣으면 리콜이 구조적으로 깎인다. **넣을지 뺄지 판단이 필요하다.**"
    )
    add("")
    add("초안: **넣는다**(답안이 미수를 논해야 하므로 쟁점이 맞다)")
    add("")
    add("> comment: ")
    add("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--rewrite", action="store_true", help="overwrite answered review")
    args = parser.parse_args()

    if args.out.is_file() and has_answers(args.out.read_text(encoding="utf-8")):
        if not args.rewrite:
            raise SystemExit(
                f"{args.out} already carries reviewer comments; pass --rewrite to discard them"
            )

    draft = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    document = render(draft, rubric_occurrences())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(document + "\n", encoding="utf-8")

    counts = {
        name: sum(1 for v in draft["crimes"].values() if v["confidence"] == name)
        for name in ("review", "clear", "not_an_offence")
    }
    print(f"{counts} -> {args.out}")


if __name__ == "__main__":
    main()
