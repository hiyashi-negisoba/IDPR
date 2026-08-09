"""v2 실적재 저작 워크시트 빌더 (읽기 전용 추출, API 0회).

카드/주석서를 조문별로 묶어 predicate 저작 재료를 한 화면에 모은다. 자동 변환이
아니다 — 스크립트는 어느 chunk가 어느 카드의 근거인지 판정하지 않는다. 카드는
카드끼리, 조문 주석은 조문당 한 번만 배치해서 보여줄 뿐이고, 관련성 판단과
predicate 경계 확정은 검수 단계에서 사람이 한다.

두 모드:
  각칙(기본)  card_catalog_v2.json을 function/form으로 필터한 카드를 article별로
              묶고, 형각 주석서(정본+보강 번들)를 article_no로 붙인다.
  총칙(--no-cards)  카드가 없으므로 좌변이 빈다. 형법총칙 원천(조문별 chunks/
              sections.jsonl)에서 절 구조 단위로 워크시트를 만든다.

사용 예:
  python scripts/v2_migration_worksheet.py
  python scripts/v2_migration_worksheet.py --articles art329 art333
  python scripts/v2_migration_worksheet.py --no-cards
  python scripts/v2_migration_worksheet.py --no-cards --articles 제10조 제21조
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CARD_CATALOG = ROOT / "data/rulebase/card_catalog_v2.json"
ARTICLE_CATALOG = ROOT / "data/rulebase/article_catalog.json"
COMMENTARY_PRIMARY = ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
COMMENTARY_SUPPLEMENT = ROOT / "data/commentary/kcl_criminal_v1_commentary_supplement.jsonl"
CRIMINAL_CODE_LAW_ID = "001692"

GENERAL_PART_ROOT = Path(
    os.environ.get(
        "IDPR_GENERAL_PART_ONTOLOGY_ROOT",
        "/home/jaehoonjeong/data/sp/data/processed/Ontology/형법총칙",
    )
)

CARD_FILTER_FUNCTIONS = {"canonical_element", "exception", "stage", "defeater", "participation"}
CARD_FILTER_FORM = "abstract_rule"

OUTPUT_ROOT = ROOT / "data/v2/worksheets"

DEFAULT_CRIMINAL_CODE_ARTICLES = ["art329", "art333", "art347", "art350", "art355", "art357", "art366"]
DEFAULT_GENERAL_PART_ARTICLES = ["제10조", "제21조", "제25조", "제26조", "제27조", "제30조", "제31조", "제32조"]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def art_key_to_article_no(art_key: str) -> str:
    """art333 -> 제333조"""
    digits = art_key[len("art") :]
    return f"제{digits}조"


def zero_padded_filename_prefix(article_no: str) -> str:
    """제10조 -> 제0010조 (형법총칙 원천 파일명이 조문 번호를 4자리로 0-패딩한다)."""
    match = re.match(r"제(\d+)조(.*)", article_no)
    if not match:
        return article_no
    number, suffix = match.groups()
    return f"제{int(number):04d}조{suffix}"


# ---------------------------------------------------------------------------
# 각칙 모드
# ---------------------------------------------------------------------------


def load_authoring_cards() -> dict[str, list[dict[str, Any]]]:
    """function/form 필터를 통과한 카드(≈496장)를 article별로 묶는다."""
    catalog = json.loads(CARD_CATALOG.read_text(encoding="utf-8"))
    by_article: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in catalog["cards"]:
        if card["function"] in CARD_FILTER_FUNCTIONS and card["form"] == CARD_FILTER_FORM:
            by_article[card["article"]].append(card)
    return by_article


def load_article_titles() -> dict[str, str]:
    catalog = json.loads(ARTICLE_CATALOG.read_text(encoding="utf-8"))
    return {a["key"]: f"{a['label']} [{a['offense']}]" for a in catalog["articles"]}


def load_criminal_code_commentary() -> dict[str, list[dict[str, Any]]]:
    """정본+보강 번들을 머지해 article_no -> chunk 목록. law_id로 형소법 chunk는 제외한다."""
    by_article_no: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in (COMMENTARY_PRIMARY, COMMENTARY_SUPPLEMENT):
        for row in load_jsonl(path):
            if row.get("law_id") != CRIMINAL_CODE_LAW_ID:
                continue
            by_article_no[row["article_no"]].append(row)
    for chunks in by_article_no.values():
        chunks.sort(key=lambda row: (row["section_path"], row["comment_id"]))
    return by_article_no


def render_criminal_code_worksheet(
    article_key: str, article_title: str, cards: list[dict[str, Any]], chunks: list[dict[str, Any]]
) -> str:
    lines = [f"# {article_key} {article_title}", "", "## 카드", ""]
    if not cards:
        lines.append("(필터를 통과한 카드 없음)")
        lines.append("")
    for card in cards:
        lines.append(f"### {card['card_id']} — {card['element_group']}")
        lines.append(
            f"- 카드 명제: {card['proposition']} "
            f"({card['function']}/{card['polarity']}/{card['norm_kind']})"
        )
        lines.append("- 제안 v2 분류: ")
        lines.append("")

    lines.append("## 조문 주석")
    lines.append("")
    if not chunks:
        lines.append("(관련 주석 chunk 없음)")
        lines.append("")
    for row in chunks:
        lines.append(f"### {row['section_path']} {row['section_title']}")
        lines.append("")
        lines.append(row["document_text"])
        lines.append("")

    return "\n".join(lines)


def run_criminal_code_mode(articles: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cards_by_article = load_authoring_cards()
    titles = load_article_titles()
    commentary_by_article_no = load_criminal_code_commentary()

    for article_key in articles:
        article_no = art_key_to_article_no(article_key)
        cards = cards_by_article.get(article_key, [])
        chunks = commentary_by_article_no.get(article_no, [])
        title = titles.get(article_key, "")
        text = render_criminal_code_worksheet(article_key, title, cards, chunks)
        out_path = out_dir / f"{article_key}.md"
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path} ({len(cards)} cards, {len(chunks)} chunks)")


# ---------------------------------------------------------------------------
# 총칙 모드 (--no-cards)
# ---------------------------------------------------------------------------


def load_general_part_chunks(article_no: str) -> list[dict[str, Any]] | None:
    """article_no(예: 제30조)에 대응하는 원천 chunks.jsonl 전부를 읽는다.

    조문 하나가 파일 여러 개로 쪼개진 경우(예: 제15조 1항/2항)는 전부 합친다.
    조문에 해당하는 파일이 없으면 None(주석 자료 없음과 구분하기 위해).
    """
    prefix = zero_padded_filename_prefix(article_no)
    matches = sorted(GENERAL_PART_ROOT.glob(f"{prefix}_*.chunks.jsonl"))
    if not matches:
        return None
    chunks: list[dict[str, Any]] = []
    for path in matches:
        chunks.extend(load_jsonl(path))
    chunks.sort(key=lambda row: (row["section_path"], row["comment_id"]))
    return chunks


def render_general_part_worksheet(article_no: str, chunks: list[dict[str, Any]] | None) -> str:
    lines = [f"# {article_no}", ""]
    if chunks is None:
        lines.append("(원천 파일 없음)")
        return "\n".join(lines)
    if not chunks:
        lines.append("(주석 chunk 0개)")
        return "\n".join(lines)
    for row in chunks:
        lines.append(f"### {row['section_path']} {row['section_title']}")
        lines.append("")
        lines.append(row["text"])
        lines.append("")
        lines.append("- 제안 predicate 후보: ")
        lines.append("")
    return "\n".join(lines)


def run_general_part_mode(articles: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for article_no in articles:
        chunks = load_general_part_chunks(article_no)
        text = render_general_part_worksheet(article_no, chunks)
        out_path = out_dir / f"{article_no}.md"
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path} ({len(chunks or [])} chunks)")


# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--no-cards",
        action="store_true",
        help="총칙 모드: 카드 없이 형법총칙 원천 주석서의 절 구조만으로 워크시트를 만든다.",
    )
    parser.add_argument(
        "--articles",
        nargs="*",
        default=None,
        help="각칙 모드는 art333 형식, 총칙 모드는 제333조 형식. 생략하면 우선순위 기본값 사용.",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="출력 디렉토리(기본: data/v2/worksheets/{각칙|총칙}).",
    )
    args = parser.parse_args()

    if args.no_cards:
        articles = args.articles or DEFAULT_GENERAL_PART_ARTICLES
        out_dir = Path(args.out) if args.out else OUTPUT_ROOT / "총칙"
        run_general_part_mode(articles, out_dir)
    else:
        articles = args.articles or DEFAULT_CRIMINAL_CODE_ARTICLES
        out_dir = Path(args.out) if args.out else OUTPUT_ROOT / "각칙"
        run_criminal_code_mode(articles, out_dir)


if __name__ == "__main__":
    main()
