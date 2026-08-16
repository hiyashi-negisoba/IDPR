#!/usr/bin/env python3
"""rubric이 이름을 부른 죄명이 저작되어 있는지, 라우팅되었는지, 답안에 나왔는지.

죄명 추출을 정규식 하나로 하면 세 가지가 함께 섞여 들어온다 -- 죄수 개념(`포괄일죄`,
`상상적 경합`), 문장 조각(`기본범죄인`, `후단 범죄`), 그리고 숫자에서 잘린 이름
(`제3자뇌물교부죄` -> `자뇌물교부죄`). 셋 다 죄명이 아니고, 셋 다 커버리지 수치를 조용히
망친다. 그래서 이 파일은 추출을 한 곳에 모아 두고 테스트로 고정한다.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.rubric import load_rubric_sets
from idpr.v2.registry import load_definitions

#: 이름 안에 숫자와 가운뎃점이 들어간다 -- `제3자뇌물교부죄`, `사문서위조·변조죄`.
OFFENSE = re.compile(r"[가-힣0-9·ㆍ]{2,20}죄")

#: 죄명처럼 끝나지만 죄명이 아닌 것. 죄수 개념과, 앞말이 잘려 나온 조각들.
NOT_AN_OFFENSE = frozenset(
    {
        "포괄일죄", "일죄", "수죄", "상상적경합죄", "경합죄", "본죄", "동죄", "각죄",
        "별죄", "무죄", "범죄", "기본범죄", "후단범죄", "전단범죄", "미수죄", "기수죄",
        "위반죄", "특정범죄", "가중처벌죄", "결과적가중범죄", "목적범죄", "신분범죄",
        "진정신분범죄", "부진정신분범죄", "고의범죄", "과실범죄",
    }
)

#: 잘린 이름을 원래 이름으로 되돌린다. 앞의 `제N` 부분이 사라진 형태만 다룬다.
TRUNCATED = {
    "자뇌물교부죄": "제3자뇌물교부죄",
    "자뇌물취득죄": "제3자뇌물취득죄",
    "자뇌물제공죄": "제3자뇌물제공죄",
}


def offense_names(text: str) -> set[str]:
    """이 텍스트가 이름으로 부른 죄명들."""
    found: set[str] = set()
    for raw in OFFENSE.findall(text):
        name = TRUNCATED.get(raw, raw)
        if name in NOT_AN_OFFENSE:
            continue
        # `성폭법위반죄`처럼 특별법 위반은 죄명으로 세되, 조각인 `위반죄`는 위에서 걸렀다.
        found.add(name)
    return found


#: 우리 스키마가 죄명이 아니라 **다른 축**으로 표현하는 것들. 미수·기수는 completion,
#: 교사·방조·공동정범은 participation이다. 이것을 죄명의 일부로 세면 `살인미수죄`가
#: "저작되지 않은 죄"로 계산되어 규칙베이스 공백이 실제보다 크게 나온다.
MODIFIERS = ("미수", "기수", "예비", "음모", "교사", "방조", "공동정범", "간접정범")


def stem(name: str) -> str:
    """죄명을 비교 가능한 어간으로. 접미 수식과 `죄`를 떼고, 가운뎃점 이형을 푼다."""
    value = re.sub(r"죄$", "", name)
    changed = True
    while changed:
        changed = False
        for modifier in MODIFIERS:
            if value.endswith(modifier) and len(value) > len(modifier):
                value = value[: -len(modifier)]
                changed = True
    return value


def stems(name: str) -> set[str]:
    """`사문서위조·변조죄` -> {`사문서위조·변조`, `사문서위조`, `사문서변조`}.

    가운뎃점으로 묶인 저작명은 두 행위를 한 이름에 담고 있고, 답안과 rubric은 그중 하나만
    부르는 일이 많다. 묶인 이름과 풀어낸 이름을 모두 같은 죄로 본다.
    """
    base = stem(name)
    out = {base}
    parts = [value for value in re.split(r"[·ㆍ]", base) if value]
    if len(parts) > 1:
        head = parts[0]
        out.add(head)
        # 머리 조각은 `객체 + 행위`(`사문서` + `위조`)이고 뒤 조각은 행위만 남은 것이다.
        # 뒤 조각의 길이만큼 머리에서 떼면 객체 접두가 그대로 나온다. 그 경계 하나만 쓴다 --
        # 가능한 모든 자리에서 자르면 `사변조` 같은 없는 어간이 생기고, 그것이 다른 죄명과
        # 우연히 맞으면 커버리지가 부풀어 오른다.
        for part in parts[1:]:
            prefix = head[: -len(part)] if len(head) > len(part) else ""
            out.add(part)
            if prefix:
                out.add(prefix + part)
    return {value for value in out if value}


def same_offense(left: str, right: str) -> bool:
    """죄명 둘이 같은 죄를 가리키는가.

    `절도`와 `특수절도`는 여기서 같다고 보지 않는다 -- 그렇게 세면 라우팅이 기본범만 열어도
    가중범을 맞힌 것으로 계산된다.
    """
    return bool(stems(left) & stems(right))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--case-id-file", type=Path, required=True)
    parser.add_argument(
        "--answers",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="method id and its answers jsonl (`answer` or `generated_response`)",
    )
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
    )
    parser.add_argument("--show", type=int, default=15)
    args = parser.parse_args()

    case_ids = [
        line.strip()
        for line in args.case_id_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    registry = load_definitions(args.definitions)
    authored: dict[str, str] = {}
    for entry in registry.by_id.values():
        if entry.kind not in {"offense", "derived_offense"}:
            continue
        name = (entry.payload.get("identity") or {}).get("name")
        if name:
            authored[str(name)] = entry.id
    authored_stems = {value for name in authored for value in stems(name)}

    routed: dict[str, set[str]] = collections.defaultdict(set)
    for line in args.plan_artifact.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        for instance in row.get("instances") or []:
            entry = registry.by_id.get(str(instance.get("offense_ref", "")))
            if entry is None:
                continue
            name = (entry.payload.get("identity") or {}).get("name")
            if name:
                routed[row["sub_question_id"]].add(str(name))

    rubrics = load_rubric_sets(args.inventory)
    gold = {cid: offense_names(" ".join(rubrics[cid].rubrics)) for cid in case_ids}
    total = sum(len(value) for value in gold.values())

    hit = collections.Counter()
    unrouted = collections.Counter()
    unauthored = collections.Counter()
    for cid in case_ids:
        for name in gold[cid]:
            if any(same_offense(name, other) for other in routed.get(cid, set())):
                hit[name] += 1
            elif stems(name) & authored_stems:
                unrouted[name] += 1
            else:
                unauthored[name] += 1

    print(f"저작된 죄명 {len(authored)}개 · rubric 죄명 {total}건 (26문항)")
    print(f"  라우팅됨       {sum(hit.values()):3d} ({sum(hit.values())/total:5.1%})")
    print(
        f"  저작O·라우팅X  {sum(unrouted.values()):3d} "
        f"({sum(unrouted.values())/total:5.1%})  <- 라우터 recall"
    )
    print(
        f"  저작X          {sum(unauthored.values()):3d} "
        f"({sum(unauthored.values())/total:5.1%})  <- 규칙베이스 커버리지"
    )
    print("\n저작되어 있는데 안 열린 죄명:")
    for name, count in unrouted.most_common(args.show):
        print(f"  {name:24s} {count}")
    print("\n저작 자체가 없는 죄명:")
    for name, count in unauthored.most_common(args.show):
        print(f"  {name:24s} {count}")

    for spec in args.answers:
        method_id, raw = spec.split("=", 1)
        rows = {}
        for line in Path(raw).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            rows[row["sub_question_id"]] = str(
                row.get("answer") or row.get("generated_response") or ""
            )
        covered = written = 0
        for cid in case_ids:
            said = offense_names(rows.get(cid, ""))
            covered += sum(
                1 for name in gold[cid] if any(same_offense(name, other) for other in said)
            )
            written += len(said)
        print(
            f"\n[{method_id}] 답안 죄명 재현율 {covered/total:5.1%} · "
            f"정밀도 {covered/max(written,1):5.1%} (답안이 부른 죄명 {written}건)"
        )


if __name__ == "__main__":
    main()
