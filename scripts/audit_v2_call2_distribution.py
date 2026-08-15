"""Call 2 결과를 planned / asked / pruned 로 나누고, 새로 열린 target군을 따로 센다.

사이클 사이의 UNKNOWN 비율을 그냥 비교하면 안 된다. rulebase가 바뀌면 planned target 수
자체가 달라지므로, 비율이 올라간 것이 "모델이 나빠졌다"인지 "이전에는 질문조차 못 하던
어려운 predicate가 새로 도달 가능해졌다"인지 구별되지 않는다. 그래서 분모를 함께 낸다.

새 target군을 따로 세는 이유도 같다. A3/A4가 추가한 죄, linked-offender dependency,
제263조 복원분은 이번 사이클에서 처음 평가되는 것이라 기존 분포와 섞으면 둘 다 못 읽는다.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

NEW_OFFENSE_REFS = frozenset({
    "offense.assault",
    "derived_offense.special_assault",
    "derived_offense.assault_causing_injury",
    "derived_offense.assault_causing_death",
    "offense.stolen_property_acquisition",
    "offense.stolen_property_custody",
})
ARTICLE263_REFS = frozenset({
    "legal_element.concurrent_independent_acts",
    "legal_element.same_object_of_result",
    "legal_element.causal_origin_unascertained",
})


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    instance = value["instance_key"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(value["predicate_ref"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--call2", type=Path, required=True)
    parser.add_argument("--top", type=int, default=15)
    args = parser.parse_args()

    planned: set[tuple[str, ...]] = set()
    for row in _jsonl(args.plan):
        for value in row.get("assessment_targets", []):
            planned.add(_key(value))

    asked: dict[tuple[str, ...], str] = {}
    article263 = Counter()
    for row in _jsonl(args.call2):
        for value in row.get("case_truths", []):
            asked[_key(value)] = str(value["truth"])
        for value in row.get("article263_assessments", []):
            for item in (*value.get("truths", ()), *value.get("shared_result_truths", ())):
                article263[str(item[1] if isinstance(item, list) else item)] += 1

    truths = Counter(asked.values())
    print(f"planned {len(planned)}")
    print(f"asked   {len(asked)}")
    print(f"pruned  {len(planned - set(asked))}")
    print(f"asked 밖에서 온 것 {len(set(asked) - planned)}  (참가·법리 등 다른 producer)")
    print()
    total = sum(truths.values()) or 1
    for truth in ("TRUE", "FALSE", "UNKNOWN"):
        print(f"  {truth:8} {truths.get(truth, 0):5}  {truths.get(truth, 0) / total:6.1%}")

    def cohort(name: str, keys: set[tuple[str, ...]]) -> None:
        values = Counter(asked[key] for key in keys if key in asked)
        n = sum(values.values())
        if not n:
            print(f"\n{name}: asked 0")
            return
        share = "  ".join(f"{t} {values.get(t, 0)}" for t in ("TRUE", "FALSE", "UNKNOWN"))
        print(f"\n{name}: asked {n}  |  {share}")

    cohort(
        "A3/A4 신규 죄 target",
        {key for key in asked if key[2] in NEW_OFFENSE_REFS},
    )
    cohort(
        "제263조 predicate target",
        {key for key in asked if key[4] in ARTICLE263_REFS},
    )
    if article263:
        print(f"제263조 전용 route 응답: {dict(article263)}")

    unknown_by_ref = Counter(key[4] for key, truth in asked.items() if truth == "UNKNOWN")
    asked_by_ref = Counter(key[4] for key in asked)
    print(f"\nUNKNOWN 상위 {args.top} predicate (asked 대비)")
    for ref, count in unknown_by_ref.most_common(args.top):
        print(f"  {count:4}/{asked_by_ref[ref]:4}  {ref}")


if __name__ == "__main__":
    main()
