#!/usr/bin/env python3
"""Report the three numbers that decide whether the Call 2 increment runs.

1. cue별 TRUE / UNKNOWN 수
2. raised doctrine별 actor-episode 수
3. Δ Call 2 target exact count  (게이트: 300)

여기에 위험 cue의 TRUE 사례만 source quote까지 뽑아 spot audit할 수 있게 낸다. 이 스크립트는
모델을 부르지 않고 target을 만들지도 않는다 -- 무엇이 열릴지 세기만 한다.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2 import expressions
from idpr.v2.doctrine_cues import DoctrineCueAssessment, load_doctrine_cues
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.doctrine_raising import raise_doctrines

DEFAULT_CUES = ROOT / "data/v2/doctrine_raising_cues.yaml"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
GATE = 300

RISKY_CUE_IDS = (
    # 낱말에 걸릴 위험이 가장 큰 셋. "승낙"이 공범의 승낙일 수 있고, 공무원 등장만으로
    # 직무 근거가 될 수 있으며, 부수적 사정이 의무 충돌로 읽힐 수 있다.
    "cue.victim_permission_stated",
    "cue.legal_or_occupational_basis_stated",
    "cue.competing_duty_stated",
)


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--cues", type=Path, default=DEFAULT_CUES)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    cues = load_doctrine_cues(args.cues)
    registry = load_definitions(args.definitions)
    leaves_by_doctrine = {
        ref: tuple(expressions.leaf_refs(registry.get(ref).payload["requires"]))
        for cue in cues
        for ref in cue.raises
    }

    rows = _jsonl(args.artifact)
    plans = {str(row["sub_question_id"]): row for row in _jsonl(args.plan_artifact)}

    assessments: list[DoctrineCueAssessment] = []
    for row in rows:
        for value in row["cue_assessments"]:
            assessments.append(
                DoctrineCueAssessment(
                    case_id=str(value["case_id"]),
                    factual_episode_id=str(value["factual_episode_id"]),
                    cue_id=str(value["cue_id"]),
                    truth=str(value["truth"]),
                    subject_actor_ids=tuple(str(item) for item in value["subject_actor_ids"]),
                    source_quote=str(value["source_quote"]),
                )
            )

    truth_by_cue: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for value in assessments:
        truth_by_cue[value.cue_id][value.truth] += 1
        if value.truth == "TRUE" and not value.subject_actor_ids:
            truth_by_cue[value.cue_id]["TRUE_WITHOUT_SUBJECT"] += 1

    episode_ids_by_case = {
        str(row["sub_question_id"]): tuple(str(v) for v in row["factual_episode_ids"])
        for row in rows
    }
    raised = raise_doctrines(
        assessments, cues=cues, episode_ids_by_case=episode_ids_by_case
    )

    raised_by_doctrine: dict[str, set[tuple[str, str, str]]] = collections.defaultdict(set)
    for value in raised:
        raised_by_doctrine[value.doctrine_ref].add(
            (value.case_id, value.actor_id, value.target_episode_id)
        )

    # top-level instance만 대상이다 (카드 C). 참가 후보는 link 확정 후로 미룬다.
    delta_targets: set[tuple[str, str, str, str, str]] = set()
    per_case_delta: collections.Counter = collections.Counter()
    for value in raised:
        plan = plans.get(value.case_id)
        if plan is None:
            continue
        top_level = {
            (
                item["instance_key"]["actor_id"],
                item["instance_key"]["offense_ref"],
                item["instance_key"]["occurrence_id"],
            ): item["factual_episode_id"]
            for item in plan["instance_provenance"]
        }
        planned_top_level = {
            (item["actor_id"], item["offense_ref"], item["occurrence_id"])
            for item in plan["top_level_instances"]
        }
        existing = {
            (
                item["instance_key"]["actor_id"],
                item["instance_key"]["offense_ref"],
                item["instance_key"]["occurrence_id"],
                item["predicate_ref"],
            )
            for item in plan["assessment_targets"]
        }
        for key, episode_id in top_level.items():
            if key not in planned_top_level:
                continue
            if key[0] != value.actor_id or episode_id != value.target_episode_id:
                continue
            for leaf in leaves_by_doctrine[value.doctrine_ref]:
                if (*key, leaf) in existing:
                    continue
                delta_targets.add((value.case_id, *key, leaf))
                per_case_delta[value.case_id] += 1

    spot: list[dict[str, Any]] = []
    for value in assessments:
        if value.cue_id in RISKY_CUE_IDS and value.truth == "TRUE":
            spot.append(value.as_dict())

    report = {
        "artifact": str(args.artifact),
        "episode_request_count": sum(len(row["episode_results"]) for row in rows),
        "cue_truth_counts": {
            cue.cue_id: dict(truth_by_cue.get(cue.cue_id, {})) for cue in cues
        },
        "raised_actor_episode_counts": {
            ref: len(values) for ref, values in sorted(raised_by_doctrine.items())
        },
        "raised_total": len(raised),
        "delta_call2_target_count": len(delta_targets),
        "delta_gate": GATE,
        "delta_within_gate": len(delta_targets) <= GATE,
        "delta_by_case": dict(per_case_delta.most_common()),
        "risky_cue_true_examples": spot,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    print(text)


if __name__ == "__main__":
    main()
