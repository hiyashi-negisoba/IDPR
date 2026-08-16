#!/usr/bin/env python3
"""답안의 **형식**만 감사한다 -- substantive 정오는 판정하지 않는다.

sealed-59 정책상 dev 2건 외의 답안 본문은 사람이 읽지 않는다. 이 스크립트는
본문을 표준출력에 흘리지 않고 다음 다섯 축의 카운트만 낸다.

1. 유보율        -- 결론을 열어 둔 채 닫는 표현의 밀도
2. occurrence 중복 -- 같은 죄명이 최종 결론에 두 항목 이상으로 서는 것
3. 조문 오류      -- (죄명, 인용 조문) 쌍이 검수된 매핑과 어긋나는 것
4. 죄수 단정      -- 경합/흡수 관계를 명시적으로 단정하는지
5. 논증 밀도/구조  -- 분량, 절 구조, 조문·판례 인용, 결론 항목 수

죄명->조문 대조표는 `data/eval/rubric_crime_article_map.json`(status: reviewed)이다.
매핑에 없는 죄명은 오류가 아니라 `unmapped`로 센다 -- 커버리지 공백이지 오답이 아니다.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARTICLE_MAP = REPO / "data" / "eval" / "rubric_crime_article_map.json"

# 결론을 확정하지 않고 닫는 표현. 학설 대립 서술("견해가 대립한다")은 유보가
# 아니라 논증이므로 넣지 않는다.
HEDGE_PATTERNS = [
    r"확정할 수 없",
    r"확정하기 어렵",
    r"판단하기 어렵",
    r"인정하기 어렵다고 볼 여지",
    r"여부에 따라 (?:그 )?성부가 결정",
    r"여부에 따라 달라진",
    r"사실관계만으로는",
    r"명시되지 않아",
    r"명확하지 않",
    r"불분명하므로",
    r"단정할 수 없",
    r"알 수 없",
    r"추가 (?:심리|확인)가 필요",
]

CONCURRENCE_PATTERNS = {
    "실체적경합": r"실체적\s*경합",
    "상상적경합": r"상상적\s*경합",
    "흡수": r"흡수(?:관계|된|되어|되는|한다)",
    "법조경합": r"법조\s*경합",
    "포괄일죄": r"포괄일죄",
    "특별관계": r"특별관계",
}

PRECEDENT = r"판례|대법원|판시|선고"
HEADING = re.compile(r"^\s*(?:#{1,6}\s|[IVX]+\.\s|\d+\.\s|[가-하]\.\s|\(\d+\)\s)", re.M)
# 죄명에 숫자가 들어간다(제3자뇌물제공죄). 한글만 잡으면 숫자에서 잘린다.
CRIME = re.compile(r"[가-힣][가-힣0-9]{1,13}죄")
ARTICLE = re.compile(r"제\s*(\d{1,3})\s*조(?:\s*의\s*(\d))?")

# (죄명, 조문) 쌍은 같은 괄호/절 안에 있을 때만 센다. 문단 건너 붙은 조문을
# 그 죄명의 인용으로 읽으면 거짓 오류가 대량으로 난다.
PAIR_TAIL = r"[^.\n]{0,30}?\(\s*(?:형법\s*)?(?P<body>제\s*\d{1,3}\s*조[^)]*)\)"
PAIR = re.compile(r"(?P<crime>[가-힣][가-힣0-9]{1,13}죄)" + PAIR_TAIL)

# 최종 결론 블록의 시작. 없으면 답안 전체 마지막 25%를 본다.
FINAL_BLOCK = re.compile(r"(?:\[?최종\s*(?:결론|요약|죄책)\]?|III?\.\s*죄수|결론\s*$)", re.M)

# 형법 총칙(제1~86조)은 죄명이 아니라 요건·법리에 붙는다. 죄명-조문 쌍으로 읽으면
# "상해죄가 성립하려면 고의가 있어야 한다(제13조)"가 통째로 오류가 된다.
GENERAL_PART_MAX = 86


def _gap_names(titles: dict[str, str]) -> dict[str, set[str]]:
    """coverage_gap의 조문 표제에서 죄명을 기계적으로 복원한다.

    카드가 없을 뿐 실재하는 조문이므로, 그 조문을 인용한 것은 오류가 아니다.
    표제 -> 죄명 변환은 두 가지만 한다: 중점(·) 분리와 '치사상' 전개.
    """
    out: dict[str, set[str]] = {}
    for article, title in titles.items():
        num = re.search(r"\d+", article)
        if not num:
            continue
        key = f"art{int(num.group())}"
        title = re.sub(r"\(.*?\)", "", title).strip()
        for part in title.split("·"):
            part = part.strip()
            if not part:
                continue
            names = [f"{part}죄"]
            if part.endswith("치사상"):
                stem = part[:-3]
                names = [f"{stem}치상죄", f"{stem}치사죄"]
            for name in names:
                out.setdefault(name, set()).add(key)
    return out


def _load_article_map() -> tuple[dict[str, set[str]], set[str]]:
    raw = json.loads(ARTICLE_MAP.read_text(encoding="utf-8"))
    attempt = {k: v for k, v in raw["attempt_articles"].items() if k.startswith("art")}
    out: dict[str, set[str]] = {}
    out_of_corpus: set[str] = set()
    for crime, entry in raw["crimes"].items():
        arts = set(entry["articles"])
        if not arts:
            # 매핑은 있으나 조문이 비었다 = 스코프 밖. 오류로 세지 않는다.
            out_of_corpus.add(crime)
            continue
        # 미수 준용조문도 정당한 인용이다.
        arts |= {attempt[a] for a in list(arts) if a in attempt}
        out[crime] = arts
    for crime, arts in _gap_names(raw["coverage_gap"]["articles"]).items():
        out.setdefault(crime, set()).update(arts)
        out_of_corpus.discard(crime)
    return out, out_of_corpus


def _bare_name_pattern(amap: dict[str, set[str]], oob: set[str]) -> re.Pattern[str]:
    """'강간상해(제301조의2)'처럼 '죄'를 안 붙인 표기도 잡는다.

    임의의 한글 조각이 아니라 검수된 매핑에 실재하는 죄명의 어간만 후보로 둔다.
    """
    stems = sorted(
        (name[:-1] for name in list(amap) + list(oob) if name.endswith("죄")),
        key=len,
        reverse=True,
    )
    alt = "|".join(re.escape(s) for s in stems if len(s) >= 3)
    return re.compile(rf"(?P<crime>{alt})(?!죄)" + PAIR_TAIL)


def _norm_crime(name: str) -> str:
    return name.replace(" ", "")


def _article_keys(body: str) -> list[str]:
    keys = []
    for num, sub in ARTICLE.findall(body):
        if int(num) <= GENERAL_PART_MAX:
            continue
        keys.append(f"art{int(num)}" + (f"_{sub}" if sub else ""))
    return keys


def _final_block(text: str) -> str:
    """답안 후반부의 결론 절. 여러 헤딩이 걸리면 가장 이른 것부터 끝까지 본다."""
    half = len(text) // 2
    for m in FINAL_BLOCK.finditer(text):
        if m.start() >= half:
            return text[m.start():]
    return text[int(len(text) * 0.75):]


def _enumerated_run(block: str) -> list[str]:
    """블록 안의 가장 긴 연속 번호목록. 죄책 열거 하나만 본다.

    결론 절에는 죄책 열거와 죄수 판단이 함께 오는데, 둘을 합쳐 세면 같은 죄명이
    양쪽에 나와 occurrence 중복으로 오인된다.
    """
    runs: list[list[str]] = []
    current: list[str] = []
    for line in block.splitlines():
        if re.match(r"^\s*(?:\d+\.|\(\d+\))\s+\S", line):
            current.append(line.strip())
        elif current and not line.strip():
            continue
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return max(runs, key=len) if runs else []


def audit_one(
    case_id: str,
    text: str,
    amap: dict[str, set[str]],
    oob: set[str],
    bare: re.Pattern[str],
) -> dict:
    chars = len(text)

    hedges = sum(len(re.findall(p, text)) for p in HEDGE_PATTERNS)

    final = _final_block(text)
    final_items = _enumerated_run(final)
    hedged_items = [
        it for it in final_items if any(re.search(p, it) for p in HEDGE_PATTERNS)
    ]

    # occurrence 중복: 최종 결론 항목들이 같은 죄명을 두 번 이상 세우는지.
    crimes_per_item = [set(_norm_crime(c) for c in CRIME.findall(it)) for it in final_items]
    dup = Counter()
    for names in crimes_per_item:
        for n in names:
            dup[n] += 1
    duplicated = {n: c for n, c in dup.items() if c >= 2}

    mismatch, unmapped, ok = [], [], 0
    seen_spans: set[int] = set()
    for m in list(PAIR.finditer(text)) + list(bare.finditer(text)):
        if m.end() in seen_spans:
            continue
        seen_spans.add(m.end())
        crime = _norm_crime(m.group("crime"))
        if not crime.endswith("죄"):
            crime += "죄"
        keys = _article_keys(m.group("body"))
        if not keys:
            continue
        expected = amap.get(crime)
        if not expected or crime in oob:
            unmapped.append(crime)
            continue
        if set(keys) & expected:
            ok += 1
        else:
            mismatch.append({"crime": crime, "cited": keys, "expected": sorted(expected)})

    concurrence = sorted(
        k for k, p in CONCURRENCE_PATTERNS.items() if re.search(p, text)
    )

    return {
        "case_id": case_id,
        "chars": chars,
        "hedge_hits": hedges,
        "hedge_per_1k": round(hedges / chars * 1000, 2) if chars else 0.0,
        "final_items": len(final_items),
        "hedged_final_items": len(hedged_items),
        "duplicated_crimes": duplicated,
        "article_pairs_checked": ok + len(mismatch),
        "article_ok": ok,
        "article_mismatch": mismatch,
        "article_unmapped": sorted(set(unmapped)),
        "concurrence_asserted": concurrence,
        "headings": len(HEADING.findall(text)),
        "article_cites": len(ARTICLE.findall(text)),
        "precedent_mentions": len(re.findall(PRECEDENT, text)),
        "unique_crimes": len({_norm_crime(c) for c in CRIME.findall(text)}),
    }


def _read(path: Path, id_key: str, text_key: str) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        out[rec[id_key]] = rec[text_key]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--idpr",
        type=Path,
        default=REPO / "experiments/v2_unknown_reduction_26/frozen_B/answers.jsonl",
    )
    ap.add_argument(
        "--cot",
        type=Path,
        default=REPO
        / "experiments/results/cot_26_8192/chain_of_thought_outputs.jsonl",
    )
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    amap, oob = _load_article_map()
    bare = _bare_name_pattern(amap, oob)
    sources = {
        "idpr_b": _read(args.idpr, "sub_question_id", "answer"),
        "cot": _read(args.cot, "sub_question_id", "generated_response"),
    }

    report = {"per_case": {}, "aggregate": {}}
    for method, answers in sources.items():
        rows = [
            audit_one(cid, txt, amap, oob, bare)
            for cid, txt in sorted(answers.items())
        ]
        report["per_case"][method] = rows
        n = len(rows)
        report["aggregate"][method] = {
            "cases": n,
            "mean_chars": round(sum(r["chars"] for r in rows) / n),
            "mean_hedge_per_1k": round(
                sum(r["hedge_per_1k"] for r in rows) / n, 2
            ),
            "cases_with_hedge": sum(1 for r in rows if r["hedge_hits"]),
            "hedged_final_items": sum(r["hedged_final_items"] for r in rows),
            "total_final_items": sum(r["final_items"] for r in rows),
            "cases_with_duplicate_crime": sum(
                1 for r in rows if r["duplicated_crimes"]
            ),
            "duplicate_crime_instances": sum(
                len(r["duplicated_crimes"]) for r in rows
            ),
            "article_pairs_checked": sum(r["article_pairs_checked"] for r in rows),
            "article_mismatch": sum(len(r["article_mismatch"]) for r in rows),
            "cases_with_article_mismatch": sum(
                1 for r in rows if r["article_mismatch"]
            ),
            "cases_asserting_concurrence": sum(
                1 for r in rows if r["concurrence_asserted"]
            ),
            "mean_headings": round(sum(r["headings"] for r in rows) / n, 1),
            "mean_article_cites": round(sum(r["article_cites"] for r in rows) / n, 1),
            "mean_precedent_mentions": round(
                sum(r["precedent_mentions"] for r in rows) / n, 1
            ),
            "mean_unique_crimes": round(sum(r["unique_crimes"] for r in rows) / n, 1),
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report["aggregate"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
