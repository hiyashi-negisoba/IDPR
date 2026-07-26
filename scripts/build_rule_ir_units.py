"""조문별 검토완료 카드셋 → **죄명 단위** NormCardSet (RuleIR 생성 단위).

사용자 결정(2026-07-25): RuleIR 단위는 죄명이다. 같은 조문의 항으로 갈리는 것(제355조 횡령/배임)도
분리한다. 근거와 단위 표는 `docs/research/rulegen_rule_ir_units.md`.

분할 신호는 데이터에 있다.
  · 제355조 — `comment_id`에 항이 박혀 있다(`..._제355조_1항_...`). 1항 60장/2항 33장, 혼합 0장.
  · 제356조 — 항 표시가 없고 절 구조로 갈린다. Ⅲ.1(업무상 보관)+`unrelated_possession`은 횡령,
    Ⅲ.2(업무상 사무처리)는 배임, 나머지(업무자 신분·업무 개념)는 두 죄명이 함께 쓰므로 공유 모듈.

가중유형은 기본죄와 같은 단위에 둔다(특수절도→절도, 강도류→강도). 기본 요건 카드를 복제하지
않으려는 것이다. 친족상도례(제328조)와 업무자 신분(제356조 공유분)은 독립 죄명이 아니므로 자체
`issue_tag`를 가진 **공유 모듈**로 뽑고, 죄명 규칙집합이 브리지 술어로 참조한다.

검증은 단위 구성 조문의 후보·commentary를 합집합으로 놓고 계약 검증을 다시 건다. API 0회.
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
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen import (  # noqa: E402
    NormCardValidationError,
    validate_norm_card_set,
)

from scripts.build_property_core_norm_card_sets import (  # noqa: E402
    commentary_index,
    extraction_candidates,
    read_json,
)

PROP = ROOT / "data/rulegen/property"
SETS = PROP / "core_norm_card_sets"
OUT_DIR = PROP / "rule_ir_units"
MANIFEST = PROP / "rule_ir_unit_manifest.json"

# 단위 → (한글 죄명, 통째로 들어가는 조문, 설명)
UNITS: dict[str, tuple[str, tuple[str, ...], str]] = {
    "theft": ("절도(야간주거침입·특수·상습 포함)",
              ("art329", "art330", "art331", "art332", "art342"),
              "야간주거침입절도(제330조)·특수절도(제331조)·상습절도(제332조)는 절취와 불법영득의사를 "
              "절도와 공유하므로 가중 스트라텀으로 같은 단위에 둔다. 제342조 미수 처벌근거 1장은 "
              "단위 간 공유 술어로 쓴다."),
    "robbery": ("강도류", ("art333", "art334", "art335", "art337", "art338", "art343"),
                "기본조문 제333조(강도) + 특수강도·준강도·강도상해치상·강도살인치사·예비음모. "
                "제333조를 보강 추출해 기본 구성요건(반항억압·강취·불법영득의사·착수·기수)이 "
                "규칙으로 들어왔다."),
    "extortion": ("공갈", ("art350",), ""),
    "breach_of_trust_bribe": ("배임수증재", ("art357",), ""),
    "lost_property_embezzlement": ("점유이탈물횡령", ("art360",), ""),
    "property_damage": ("재물손괴", ("art366",), ""),
    "interference_with_exercise_of_right": ("권리행사방해", ("art323",), ""),
    "relative_property_crime_exception": ("친족상도례(공유)", ("art328",),
        "독립 죄명이 아니라 인적 처벌조각사유(1항)·소추조건(2항)이다. 죄명 규칙집합이 배출하는 "
        "브리지 술어 property_crime_established를 받아 처벌·소추 층에서만 작동한다."),
    "embezzlement": ("횡령·업무상횡령", (), "제355조 1항 + 제356조 업무상 보관분"),
    "breach_of_trust": ("배임·업무상배임", (), "제355조 2항 + 제356조 업무상 사무처리분"),
    "occupational_status": ("업무자 가중신분(공유)", (),
        "제356조는 죄명이 아니라 가중신분을 정한다. 업무 개념 카드는 업무상횡령·업무상배임이 "
        "똑같이 쓰므로 공유 모듈로 뽑아 가중 스트라텀에서 참조한다."),
}

# 제356조 카드 → 단위 (절 기준)
ART356_TO_EMBEZZLEMENT_SECTIONS = ("Ⅲ.1",)
ART356_TO_BREACH_SECTIONS = ("Ⅲ.2",)
ART356_EXTRA_EMBEZZLEMENT = ("art356_sec2_2.unrelated_possession",)

PARAGRAPH = re.compile(r"제\d+조_(\d)항")


def article_of(card_id: str) -> str:
    return card_id.split("_")[0].split(".")[0]


def paragraph_of(card: dict[str, Any]) -> str | None:
    found = {match.group(1) for ref in card["source_refs"]
             if (match := PARAGRAPH.search(ref["comment_id"]))}
    if len(found) > 1:
        raise SystemExit(f"{card['id']}는 항을 걸친다: {sorted(found)}")
    return found.pop() if found else None


def sections_of(card: dict[str, Any]) -> set[str]:
    return {ref["section_path"] for ref in card["source_refs"]}


def assign(card: dict[str, Any], article: str) -> str:
    """카드 하나를 죄명 단위에 배정한다."""

    if article == "art355":
        paragraph = paragraph_of(card)
        if paragraph == "1":
            return "embezzlement"
        if paragraph == "2":
            return "breach_of_trust"
        raise SystemExit(f"{card['id']}에 항 정보가 없다 — 수동 배정 필요")

    if article == "art356":
        if card["id"] in ART356_EXTRA_EMBEZZLEMENT:
            return "embezzlement"
        sections = sections_of(card)
        if any(s.startswith(ART356_TO_EMBEZZLEMENT_SECTIONS) for s in sections):
            return "embezzlement"
        if any(s.startswith(ART356_TO_BREACH_SECTIONS) for s in sections):
            return "breach_of_trust"
        return "occupational_status"

    for unit, (_, articles, _) in UNITS.items():
        if article in articles:
            return unit
    raise SystemExit(f"{article}가 어느 단위에도 속하지 않는다")


def main() -> None:
    by_unit: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unit_articles: dict[str, set[str]] = defaultdict(set)
    per_article: Counter = Counter()

    for path in sorted(SETS.glob("*.json")):
        payload = read_json(path)
        article = payload["issue_tag"]
        for card in payload["cards"]:
            unit = assign(card, article)
            by_unit[unit].append(card)
            unit_articles[unit].add(article)
            per_article[article] += 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest, failures = [], []
    for unit in UNITS:
        cards = sorted(by_unit[unit], key=lambda card: card["id"])
        if not cards:
            raise SystemExit(f"단위 {unit}에 카드가 없다")
        articles = sorted(unit_articles[unit])

        commentary_by_id: dict[str, Any] = {}
        request_comment_ids: dict[str, set[str]] = {}
        candidates: dict[tuple[str, str], dict[str, Any]] = {}
        target_paths: set[str] = set()
        for article in articles:
            article_commentary, article_requests = commentary_index(article)
            commentary_by_id |= article_commentary
            request_comment_ids |= article_requests
            candidates |= extraction_candidates(article)
            target_paths |= {f"commentary://001692/{article}"}

        card_set = {
            "version": "1.1.0",
            "card_set_id": f"kr.property.{unit}.core.norms.v1",
            "issue_tag": unit,
            "status": "draft",
            "legal_review": "complete",
            "construction": "reviewed_aggregate",
            "source_scope": {
                "target_paths": sorted(target_paths),
                "comment_ids": sorted({ref["comment_id"] for card in cards
                                       for ref in card["source_refs"]}),
            },
            "cards": cards,
            "legal_review_questions": [],
            "coverage_gaps": sorted(dict.fromkeys(
                gap for article in articles
                for gap in read_json(SETS / f"{article}.json")["coverage_gaps"])),
        }

        try:
            validate_norm_card_set(card_set, commentary_by_id)
            verdict = "valid"
        except NormCardValidationError as exc:
            verdict, _ = "invalid", failures.append(f"{unit}: {exc}")

        (OUT_DIR / f"{unit}.json").write_text(
            json.dumps(card_set, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        label, _, note = UNITS[unit]
        manifest.append({
            "issue_tag": unit, "label": label, "articles": articles,
            "cards": len(cards),
            "roles": dict(Counter(card["formalization"] for card in cards)),
            "shared_module": unit in ("relative_property_crime_exception",
                                      "occupational_status"),
            "note": note, "validation": verdict,
        })
        print(f"  {unit:36s} {len(cards):4d}장  {','.join(articles):24s} {verdict}")

    total = sum(item["cards"] for item in manifest)
    MANIFEST.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "design": "docs/research/rulegen_rule_ir_units.md",
        "source": "data/rulegen/property/core_norm_card_sets (검토완료 core 422장)",
        "counts": {"units": len(manifest), "cards": total,
                   "per_article": dict(sorted(per_article.items()))},
        "bridge_predicate": {
            "name": "property_crime_established",
            "arguments": ["case_id", "crime_id", "defendant_id", "owner_id", "possessor_id"],
            "purpose": ("죄명 규칙집합이 공통으로 배출하고 공유 모듈(친족상도례·업무자 신분)이 "
                        "받는다. 준용 범위·시행일 조건을 한 곳에서 관리하기 위한 이음새."),
        },
        "units": manifest,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n단위 {len(manifest)}개 / 카드 {total}장 → {OUT_DIR.relative_to(ROOT)}")
    if failures:
        print("\n검증 실패:")
        for line in failures:
            print(f"  {line}")
        raise SystemExit(1)
    print("  전 단위 NormCardSet 계약 통과")


if __name__ == "__main__":
    main()
