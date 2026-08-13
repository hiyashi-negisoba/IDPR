#!/usr/bin/env python3
"""Open concurrence-condition pair candidates on top of an existing plan artifact.

host가 하는 것은 여기까지다: 승인된 규칙 + 계획된 top-level instance 양쪽 존재 + 같은 factual
episode + (규칙이 요구하면) 같은 행위자. **같은 episode에 두 죄가 있다는 것만으로 조건을 TRUE로
만들지 않는다.** 그 인영이 바로 그 문서의 구성부분이 되었는가는 모델이 판단한다.

join은 `plan_concurrence_condition_pairs`가 해소 시점과 같은 함수로 수행한다. 후보를 넓히는
별도의 문을 여기서 만들지 않는다.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.runtime.concurrence import load_concurrence_rules
from idpr.v2.runtime.concurrence_condition import (
    canonical_conduct_text,
    plan_concurrence_condition_pairs,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

DEFAULT_RULES = ROOT / "data/v2/concurrence_rules.yaml"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _instance(case_id: str, key: dict[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        case_id,
        str(key["actor_id"]),
        str(key["offense_ref"]),
        str(key["occurrence_id"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rules = load_concurrence_rules(args.rules)
    output: list[dict[str, Any]] = []
    total_pairs = 0
    for plan in _jsonl(args.plan_artifact):
        case_id = str(plan["sub_question_id"])
        provenance = plan.get("instance_provenance")
        if provenance is None:
            raise ValueError(
                f"{case_id}: planner artifact predates instance_provenance; re-run the planner"
            )
        planned = [_instance(case_id, item) for item in plan["top_level_instances"]]
        episode_by_instance = {
            _instance(case_id, item["instance_key"]): str(item["factual_episode_id"])
            for item in provenance
        }
        # 계획된 top-level 중 episode를 모르는 것이 있으면 조용히 후보에서 빼지 않는다.
        missing = [value for value in planned if value not in episode_by_instance]
        if missing:
            raise ValueError(f"{case_id}: planned instances lack a factual episode: {missing}")
        conduct_by_occurrence = {
            str(item["occurrence_id"]): canonical_conduct_text(str(item["source_text"]))
            for item in plan["occurrences"]
        }
        pairs = plan_concurrence_condition_pairs(
            planned,
            episode_by_instance=episode_by_instance,
            rules=rules,
        )

        row = copy.deepcopy(plan)
        row["concurrence_condition_pairs"] = []
        for pair in pairs:
            absorbed_conduct = conduct_by_occurrence.get(pair.absorbed.occurrence_id, "")
            absorbing_conduct = conduct_by_occurrence.get(pair.absorbing.occurrence_id, "")
            if not absorbed_conduct or not absorbing_conduct:
                raise ValueError(
                    f"{case_id}/{pair.pair_id}: a pair instance has no bound conduct evidence"
                )
            row["concurrence_condition_pairs"].append(
                {
                    **pair.as_dict(),
                    "first_conduct": absorbed_conduct,
                    "second_conduct": absorbing_conduct,
                }
            )
        row["concurrence_condition_pair_count"] = len(pairs)
        total_pairs += len(pairs)
        output.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_concurrence_condition_pairs",
        "status": "SUCCEEDED",
        "rule": (
            "approved rule + both planned top-level instances + same factual episode + the "
            "rule's own actor constraint; nothing else opens a pair"
        ),
        "case_count": len(output),
        "approved_rule_ids": [rule.rule_id for rule in rules],
        "pair_count": total_pairs,
        "pair_case_ids": sorted(
            row["sub_question_id"]
            for row in output
            if row["concurrence_condition_pair_count"]
        ),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "rules_sha256": _sha256(args.rules),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(f"pairs={total_pairs} cases={manifest['pair_case_ids']}")


if __name__ == "__main__":
    main()
