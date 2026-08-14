#!/usr/bin/env python3
"""Open Call 2 targets for the doctrines Call 1.5-D actually raised.

이 스크립트가 doctrine activation dead loop의 마지막 조각이다. 지금까지 closure는 13개
doctrine을 모든 사건에 후보로 열었지만 그 leaf는 한 번도 target이 아니었고, 그래서
`raised_active_doctrines`의 "leaf 하나는 non-UNKNOWN이어야 한다"가 영원히 거짓이었다.

두 가지를 한다.

1. raised doctrine의 leaf를 target으로 연다. identity gate를 통과한 것만 -- 주체가 이 사건의
   법적 instance를 가진 행위자가 아니면 열지 않고 `NOT_MATERIALIZED`로 남긴다.
2. `candidate_doctrine_refs`를 raised 집합으로 좁힌다. 제기되지 않은 doctrine은 부정된 것이
   아니라 미제기이며, 후보에서 빠지는 것으로 충분하다.
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

from idpr.v2 import expressions
from idpr.v2.doctrine_cues import DoctrineCueAssessment, load_doctrine_cues
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.doctrine_raising import raise_doctrines
from idpr.v2.runtime.doctrine_targets import materialize_doctrine_leaf_targets
from idpr.v2.runtime.identity import OffenseInstanceKey

DEFAULT_CUES = ROOT / "data/v2/doctrine_raising_cues.yaml"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--call15d-artifact", type=Path, required=True)
    parser.add_argument("--cues", type=Path, default=DEFAULT_CUES)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cues = load_doctrine_cues(args.cues)
    registry = load_definitions(args.definitions)
    # blocker leaf도 함께 연다. 예외가 실제로 있었는지는 물어봐야 알고, 묻지 않으면
    # UNKNOWN으로 남아 아무것도 막지 않는다 -- 그것이 blocked_when의 의도된 기본값이다.
    leaves_by_doctrine = {
        ref: tuple(
            dict.fromkeys(
                (
                    *expressions.leaf_refs(registry.get(ref).payload["requires"]),
                    *expressions.leaf_refs(
                        registry.get(ref).payload.get("blocked_when")
                    ),
                )
            )
        )
        for cue in cues
        for ref in cue.raises
    }

    plans = {str(row["sub_question_id"]): row for row in _jsonl(args.plan_artifact)}
    cue_rows = {str(row["sub_question_id"]): row for row in _jsonl(args.call15d_artifact)}
    missing = sorted(set(plans) - set(cue_rows))
    if missing:
        raise ValueError(f"Call 1.5-D artifact is missing cases: {missing}")

    output: list[dict[str, Any]] = []
    total_targets = 0
    total_unmaterialized = 0
    for case_id, plan in plans.items():
        cue_row = cue_rows[case_id]
        if cue_row.get("error"):
            raise ValueError(f"{case_id}: Call 1.5-D row is not contract-valid")
        assessments = [
            DoctrineCueAssessment(
                case_id=str(value["case_id"]),
                factual_episode_id=str(value["factual_episode_id"]),
                cue_id=str(value["cue_id"]),
                truth=str(value["truth"]),
                subject_actor_ids=tuple(str(item) for item in value["subject_actor_ids"]),
                source_quote=str(value["source_quote"]),
            )
            for value in cue_row["cue_assessments"]
        ]
        raised = raise_doctrines(
            assessments,
            cues=cues,
            episode_ids_by_case={
                case_id: tuple(str(v) for v in cue_row["factual_episode_ids"])
            },
        )

        row = copy.deepcopy(plan)
        planned_top_level = {
            (item["actor_id"], item["offense_ref"], item["occurrence_id"])
            for item in row["top_level_instances"]
        }
        universe = [
            (
                OffenseInstanceKey(
                    case_id,
                    item["instance_key"]["actor_id"],
                    item["instance_key"]["offense_ref"],
                    item["instance_key"]["occurrence_id"],
                ),
                item["factual_episode_id"],
            )
            for item in row["instance_provenance"]
            if (
                item["instance_key"]["actor_id"],
                item["instance_key"]["offense_ref"],
                item["instance_key"]["occurrence_id"],
            )
            in planned_top_level
        ]
        existing = [
            (
                OffenseInstanceKey(
                    case_id,
                    item["instance_key"]["actor_id"],
                    item["instance_key"]["offense_ref"],
                    item["instance_key"]["occurrence_id"],
                ),
                item["predicate_ref"],
            )
            for item in row["assessment_targets"]
        ]
        targets, unmaterialized = materialize_doctrine_leaf_targets(
            raised,
            instances=universe,
            leaves_by_doctrine=leaves_by_doctrine,
            existing_targets=existing,
        )
        row["assessment_targets"].extend(value.as_dict() for value in targets)
        row["final_assessment_target_count"] = len(row["assessment_targets"])
        row["doctrine_target_count"] = len(targets)
        row["raised_doctrines"] = [value.as_dict() for value in raised]
        row["not_materialized_raisings"] = [
            value.as_dict() for value in unmaterialized
        ]
        # 제기되지 않은 doctrine은 후보에서 빠진다. 부정이 아니라 미제기다.
        raised_refs = tuple(dict.fromkeys(value.doctrine_ref for value in raised))
        row["candidate_doctrine_refs_before_raising"] = list(
            row["candidate_doctrine_refs"]
        )
        row["candidate_doctrine_refs"] = [
            ref for ref in row["candidate_doctrine_refs"] if ref in raised_refs
        ]
        # 새 predicate ref가 selected 목록에 반영되어야 Call 2 요청이 만들어진다.
        selected = list(row["selected_predicate_refs"])
        for value in targets:
            if value.predicate_ref not in selected:
                selected.append(value.predicate_ref)
        row["selected_predicate_refs"] = selected
        row["selected_predicate_count"] = len(selected)
        total_targets += len(targets)
        total_unmaterialized += len(unmaterialized)
        output.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_doctrine_target_plan",
        "status": "SUCCEEDED",
        "rule": (
            "open leaves only for doctrines raised by an authored factual cue whose subject "
            "has a legal instance in the target episode"
        ),
        "case_count": len(output),
        "doctrine_target_count": total_targets,
        "not_materialized_raising_count": total_unmaterialized,
        "final_assessment_target_count": sum(
            row["final_assessment_target_count"] for row in output
        ),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "call15d_artifact": str(args.call15d_artifact),
        "call15d_artifact_sha256": _sha256(args.call15d_artifact),
        "cues_sha256": _sha256(args.cues),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(
        f"doctrine targets={total_targets} not_materialized={total_unmaterialized} "
        f"final targets={manifest['final_assessment_target_count']}"
    )


if __name__ == "__main__":
    main()
