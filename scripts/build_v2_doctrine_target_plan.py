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
from idpr.v2.runtime.carrier_contract import resolve_carrier, validate_plan_carriers
from idpr.v2.runtime.doctrine_targets import (
    materialize_doctrine_leaf_targets,
    merge_reused_openers,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.plan_lineage import (
    LINEAGE_KEY,
    lineage_for_manifest,
    provenance as plan_provenance,
)

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
    # `leaf_refs`는 frozenset이라 반복 순서가 해시 시드에 따라 달라진다. 정렬하지 않으면
    # 같은 입력에서 target 순서가 실행마다 바뀌고, manifest의 sha256 provenance가 아무것도
    # 보증하지 못하게 된다.
    leaves_by_doctrine = {
        ref: tuple(
            sorted(
                {
                    *expressions.leaf_refs(registry.get(ref).payload["requires"]),
                    *expressions.leaf_refs(
                        registry.get(ref).payload.get("blocked_when")
                    ),
                }
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
    total_reused = 0
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
        materialized, unmaterialized = materialize_doctrine_leaf_targets(
            raised,
            instances=universe,
            leaves_by_doctrine=leaves_by_doctrine,
            existing_targets=existing,
        )
        targets = tuple(
            value for value in materialized if not value.reuses_existing_target
        )
        reused = tuple(value for value in materialized if value.reuses_existing_target)
        row["assessment_targets"].extend(value.as_dict() for value in targets)
        # 이미 열려 있던 target을 이 doctrine도 필요로 한다면, 새 행을 만들지 않되 그 사실을
        # 기존 행에 남긴다. 규칙은 runtime이 소유한다 -- 여기서 다시 구현하면 그것이 두 번째
        # 권위가 되고, 이 감사가 반복해서 잡아낸 결함 클래스가 하나 더 생긴다.
        merge_reused_openers(row["assessment_targets"], reused)

        # 새로 연 target에는 물리적 carrier가 함께 있어야 한다. 없으면 Call 2가 target 목록과
        # carrier 목록의 불일치로 사건 전체를 거부한다 -- 실제로 첫 관통에서 여기서 멈췄다.
        # 법리는 그 instance가 실현된 행위에 대해 묻는 것이므로 realization이 그 carrier다.
        # identity는 occurrence_id 하나가 아니다. 절도와 특수절도가 같은 realization을
        # 공유하고 그 둘의 carrier 사정이 다를 수 있다.
        provenance_by_instance = {
            (
                str(item["instance_key"]["actor_id"]),
                str(item["instance_key"]["offense_ref"]),
                str(item["instance_key"]["occurrence_id"]),
            ): item
            for item in row.get("instance_provenance", ())
        }
        covered = {
            (
                value["instance_key"]["actor_id"],
                value["instance_key"]["offense_ref"],
                value["instance_key"]["occurrence_id"],
                value["predicate_ref"],
            )
            for value in row.get("assessment_carriers", ())
        }
        for value in targets:
            key = (
                value.instance.actor_id,
                value.instance.offense_ref,
                value.instance.occurrence_id,
                value.predicate_ref,
            )
            if key in covered:
                continue
            provenance = provenance_by_instance.get(
                (value.instance.actor_id, value.instance.offense_ref, value.instance.occurrence_id)
            )
            if provenance is None:
                raise ValueError(
                    f"{case_id}: doctrine leaf target lacks realization provenance "
                    f"({value.instance.occurrence_id})"
                )
            carrier_id, carrier_label = resolve_carrier(
                registry,
                value.predicate_ref,
                provenance=provenance,
                occurrence_id=value.instance.occurrence_id,
            )
            covered.add(key)
            row.setdefault("assessment_carriers", []).append(
                {
                    "instance_key": {
                        "case_id": value.instance.case_id,
                        "actor_id": value.instance.actor_id,
                        "offense_ref": value.instance.offense_ref,
                        "occurrence_id": value.instance.occurrence_id,
                    },
                    "predicate_ref": value.predicate_ref,
                    "carrier_id": carrier_id,
                    "carrier_kind": carrier_label,
                }
            )
        validate_plan_carriers(registry, row)
        row["assessment_carrier_count"] = len(row.get("assessment_carriers", ()))
        row["final_assessment_target_count"] = len(row["assessment_targets"])
        row["doctrine_target_count"] = len(targets)
        row["doctrine_reused_target_count"] = len(reused)
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
        total_reused += len(reused)
        total_unmaterialized += len(unmaterialized)
        output.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_doctrine_target_plan",
        # 이 단계는 plan을 새로 만드는 것이 아니라 증강한다. 입력 plan이 거쳐 온 단계를
        # 이어받지 않으면 하류 가드가 참가 병합 여부를 알 방법이 없다.
        LINEAGE_KEY: list(
            lineage_for_manifest(args.plan_artifact, "v2_doctrine_target_plan")
        ),
        "status": "SUCCEEDED",
        "rule": (
            "open leaves only for doctrines raised by an authored factual cue whose subject "
            "has a legal instance in the target episode"
        ),
        "case_count": len(output),
        "doctrine_target_count": total_targets,
        "doctrine_reused_target_count": total_reused,
        "not_materialized_raising_count": total_unmaterialized,
        "final_assessment_target_count": sum(
            row["final_assessment_target_count"] for row in output
        ),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "call15d_artifact": str(args.call15d_artifact),
        "call15d_artifact_sha256": _sha256(args.call15d_artifact),
        "cues_sha256": _sha256(args.cues),
        # 입력의 내용 해시를 한 자리에 모아 둔다. 소비자는 이 기록으로 "이 산출물이 만들어진
        # 뒤에 상류가 다시 생성되었는가"를 확인한다.
        **plan_provenance(
            {
                "plan": args.plan_artifact,
                "call15d": args.call15d_artifact,
                "cues": args.cues,
            },
            definitions_dir=args.definitions,
        ),
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
