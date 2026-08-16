#!/usr/bin/env python3
"""rubric이 이름을 부른 죄가 저작되어 있는지, 라우팅되었는지.

**매칭 실패는 저작X가 아니다.** 이름이 저작 표기와 다르다는 것과 그 죄가 규칙베이스에 없다는
것은 다른 사실인데, 문자열 비교 하나로 두 가지를 함께 판정하면 후자가 부풀어 오른다. 그래서
이 파일은 판정을 넷으로 나눈다 -- `routed`, `authored·unrouted`, 사람이 확정한
`known unauthored`, 그리고 **아직 판정하지 않은** `UNRESOLVED_NAME`.

집계 단위는 `case x canonical offense ref`다. 같은 문항에서 `수뢰죄`와 `뇌물수수죄`가 함께
나오면 canonicalization 뒤 1건이다. raw 문자열을 set으로 만드는 것만으로는 이 중복이 남는다.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.rubric import load_rubric_sets
from idpr.v2.registry import load_definitions

OFFENSE = re.compile(r"[가-힣0-9·ㆍ]{2,24}죄")

#: 죄명처럼 끝나지만 죄명이 아닌 것. 죄수 개념과, 앞말이 잘려 나온 조각들.
NOT_AN_OFFENSE = frozenset(
    {
        "포괄일죄", "일죄", "수죄", "상상적경합죄", "경합죄", "본죄", "동죄", "각죄",
        "별죄", "무죄", "범죄", "기본범죄", "후단범죄", "전단범죄", "미수죄", "기수죄",
        "위반죄", "특정범죄", "가중처벌죄", "결과적가중범죄", "목적범죄", "신분범죄",
        "진정신분범죄", "부진정신분범죄", "고의범죄", "과실범죄",
    }
)

#: 숫자가 경계가 되어 앞이 잘린 이름을 되돌린다.
TRUNCATED = {
    "자뇌물교부죄": "제3자뇌물교부죄",
    "자뇌물취득죄": "제3자뇌물취득죄",
    "자뇌물제공죄": "제3자뇌물제공죄",
}

#: 우리 스키마가 죄명이 아니라 **다른 축**으로 표현하는 것. 미수 계열은 completion,
#: 정범·교사·방조는 participation이다. 세부 미수형(장애·중지·불능)을 빼면 `살인장애미수죄`가
#: `살인장애`로 남아 저작된 살인죄와 이어지지 않는다.
#:
#: **예비·음모는 일부러 넣지 않았다.** 그것은 완성범의 실행단계가 아니라 별도로 저작되어야 할
#: 죄이고, 접어 버리면 실제로 없는 저작을 있는 것으로 세게 된다.
SCHEMA_SUFFIXES = (
    "공동정범", "간접정범", "장애미수", "중지미수", "불능미수", "교사", "방조",
    "미수", "기수",
)

DEFAULT_NAME_REVIEW = ROOT / "data/v2/offense_name_review.yaml"


@dataclass(frozen=True)
class Resolution:
    raw: str
    surface: str
    refs: tuple[str, ...]
    status: str


def compact(text: str) -> str:
    """이름 하나를 정규화한다. **텍스트 전체에 걸지 않는다** -- 공백을 지우면 어절 경계가
    사라져 `기본범죄인 상해죄`가 통째로 한 이름으로 잡힌다."""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))


def offense_names(text: str) -> set[str]:
    """이 텍스트가 이름으로 부른 죄명들. 아직 canonical이 아니다.

    정규화는 NFKC까지만 하고 공백은 남긴다. 정규식이 한글·숫자·가운뎃점만 받으므로 공백이
    그대로 이름의 경계가 된다.
    """
    found: set[str] = set()
    for raw in OFFENSE.findall(unicodedata.normalize("NFKC", text)):
        name = TRUNCATED.get(raw, raw)
        if name not in NOT_AN_OFFENSE:
            found.add(name)
    return found


def strip_schema_suffixes(name: str) -> str:
    """죄명에서 completion·participation 축을 떼어 낸 표면형."""
    value = re.sub(r"죄$", "", compact(name))
    while True:
        matched = next(
            (
                suffix
                for suffix in SCHEMA_SUFFIXES
                if value.endswith(suffix) and len(value) > len(suffix)
            ),
            None,
        )
        if matched is None:
            return value + "죄"
        value = value[: -len(matched)]


def authored_surface_variants(name: str) -> set[str]:
    """`사문서위조·변조죄` -> {`사문서위조·변조죄`, `사문서위조죄`, `사문서변조죄`}.

    머리 조각은 `객체 + 행위`이고 뒤 조각은 행위만 남은 것이다. 뒤 조각의 길이만큼 머리에서
    떼면 객체 접두가 나온다. 그 경계 하나만 쓴다 -- 가능한 모든 자리에서 자르면 `사변조` 같은
    없는 표면형이 생기고, 그것이 다른 죄명과 우연히 맞으면 커버리지가 부풀어 오른다.
    """
    normalized = strip_schema_suffixes(name)
    base = re.sub(r"죄$", "", normalized)
    variants = {normalized}

    parts = [part for part in re.split(r"[·ㆍ]", base) if part]
    if len(parts) <= 1:
        return variants

    head = parts[0]
    variants.add(head + "죄")
    for part in parts[1:]:
        if len(head) > len(part):
            variants.add(head[: -len(part)] + part + "죄")
    return variants


def stems(name: str) -> set[str]:
    return {re.sub(r"죄$", "", value) for value in authored_surface_variants(name)}


def same_offense(left: str, right: str) -> bool:
    return bool(stems(left) & stems(right))


def authored_index(registry) -> tuple[dict[str, str], dict[str, set[str]]]:
    names: dict[str, str] = {}
    surfaces: dict[str, set[str]] = collections.defaultdict(set)
    for entry in registry.by_id.values():
        if entry.kind not in {"offense", "derived_offense"}:
            continue
        name = (entry.payload.get("identity") or {}).get("name")
        if not name:
            continue
        names[entry.id] = str(name)
        for surface in authored_surface_variants(str(name)):
            surfaces[surface].add(entry.id)
    return names, surfaces


def as_refs(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(value)
    raise ValueError(f"invalid alias target: {value!r}")


def load_name_review(
    path: Path | None, registry
) -> tuple[dict[str, tuple[str, ...]], set[str], set[str]]:
    if path is None or not path.exists():
        return {}, set(), set()

    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    aliases = {
        strip_schema_suffixes(str(name)): as_refs(value)
        for name, value in (payload.get("aliases") or {}).items()
    }
    known_unauthored = {
        strip_schema_suffixes(str(name)) for name in (payload.get("known_unauthored") or [])
    }
    ignore = {strip_schema_suffixes(str(name)) for name in (payload.get("ignore") or [])}

    for surface, refs in aliases.items():
        missing = [ref for ref in refs if ref not in registry.by_id]
        if missing:
            raise ValueError(f"{surface}: unknown offense refs {missing}")
    return aliases, known_unauthored, ignore


def resolve_name(
    raw: str,
    authored_surfaces: dict[str, set[str]],
    aliases: dict[str, tuple[str, ...]],
    known_unauthored: set[str],
    ignore: set[str],
) -> Resolution:
    surface = strip_schema_suffixes(raw)
    if surface in ignore:
        return Resolution(raw, surface, (), "IGNORE")
    refs = authored_surfaces.get(surface)
    if refs:
        return Resolution(raw, surface, tuple(sorted(refs)), "AUTHORED")
    alias_refs = aliases.get(surface)
    if alias_refs:
        return Resolution(raw, surface, tuple(sorted(alias_refs)), "ALIAS")
    if surface in known_unauthored:
        return Resolution(raw, surface, (), "KNOWN_UNAUTHORED")
    return Resolution(raw, surface, (), "UNRESOLVED_NAME")


def load_routed_refs(path: Path) -> dict[str, set[str]]:
    routed: dict[str, set[str]] = collections.defaultdict(set)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        for instance in row.get("instances") or []:
            ref = str(instance.get("offense_ref") or "")
            if ref:
                routed[row["sub_question_id"]].add(ref)
    return routed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--case-id-file", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
    )
    parser.add_argument("--name-review", type=Path, default=DEFAULT_NAME_REVIEW)
    parser.add_argument("--show", type=int, default=30)
    args = parser.parse_args()

    case_ids = [
        line.strip()
        for line in args.case_id_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

    registry = load_definitions(args.definitions)
    authored_names, authored_surfaces = authored_index(registry)
    aliases, known_unauthored, ignore = load_name_review(args.name_review, registry)
    routed = load_routed_refs(args.plan_artifact)
    rubrics = load_rubric_sets(args.inventory)

    counts: collections.Counter[str] = collections.Counter()
    unresolved: collections.Counter[str] = collections.Counter()
    known_missing: collections.Counter[str] = collections.Counter()
    authored_unrouted: collections.Counter[str] = collections.Counter()

    for cid in case_ids:
        resolved_units: dict[tuple[str, ...], str] = {}
        unresolved_units: set[str] = set()
        unauthored_units: set[str] = set()

        for raw in offense_names(" ".join(rubrics[cid].rubrics)):
            result = resolve_name(
                raw, authored_surfaces, aliases, known_unauthored, ignore
            )
            if result.status == "IGNORE":
                continue
            if result.status == "UNRESOLVED_NAME":
                unresolved_units.add(result.surface)
                continue
            if result.status == "KNOWN_UNAUTHORED":
                unauthored_units.add(result.surface)
                continue
            # canonical ref 집합이 단위다. 표기가 둘이어도 같은 죄면 여기서 하나로 접힌다.
            resolved_units[result.refs] = result.surface

        for refs, surface in resolved_units.items():
            counts["total"] += 1
            counts["resolved"] += 1
            if routed[cid] & set(refs):
                counts["routed"] += 1
            else:
                counts["authored_unrouted"] += 1
                authored_unrouted[surface] += 1

        for surface in sorted(unauthored_units):
            counts["total"] += 1
            counts["known_unauthored"] += 1
            known_missing[surface] += 1

        for surface in sorted(unresolved_units):
            counts["total"] += 1
            counts["unresolved_name"] += 1
            unresolved[surface] += 1

    total = counts["total"]
    resolved = counts["resolved"]
    print(
        f"저작된 offense ref {len(authored_names)}개 · "
        f"rubric case-offense unit {total}건 ({len(case_ids)}문항)"
    )
    print(f"  resolved           {resolved:3d} ({resolved / max(total, 1):5.1%})")
    print(
        f"  routed             {counts['routed']:3d} "
        f"({counts['routed'] / max(resolved, 1):5.1%} of resolved)"
    )
    print(
        f"  authored·unrouted  {counts['authored_unrouted']:3d} "
        f"({counts['authored_unrouted'] / max(resolved, 1):5.1%} of resolved)"
    )
    print(
        f"  known unauthored   {counts['known_unauthored']:3d} "
        f"({counts['known_unauthored'] / max(total, 1):5.1%})"
    )
    print(
        f"  unresolved name    {counts['unresolved_name']:3d} "
        f"({counts['unresolved_name'] / max(total, 1):5.1%})"
    )

    print("\n저작되어 있는데 라우팅되지 않은 죄:")
    for surface, count in authored_unrouted.most_common(args.show):
        refs = sorted(authored_surfaces.get(surface) or aliases.get(surface) or ())
        labels = ", ".join(f"{ref}={authored_names.get(ref, '?')}" for ref in refs)
        print(f"  {surface:28s} {count:3d}  {labels}")

    print("\n검토로 확정한 저작X:")
    for surface, count in known_missing.most_common(args.show):
        print(f"  {surface:28s} {count:3d}")

    print("\n아직 이름만으로 판정하지 않은 항목:")
    for surface, count in unresolved.most_common(args.show):
        print(f"  {surface:28s} {count:3d}")

    if counts["unresolved_name"]:
        print(
            "\nUNRESOLVED_NAME은 저작X로 계산하지 않는다. "
            "offense_name_review.yaml 검토 후 다시 집계한다."
        )


if __name__ == "__main__":
    main()
