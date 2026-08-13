#!/usr/bin/env python3
"""Causally merge selected Call 2 rows and refresh planner lineage/counts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _row_usage(row: dict[str, Any]) -> dict[str, int]:
    output = {key: 0 for key in ("prompt_tokens", "completion_tokens", "total_tokens")}
    for shard in row.get("shards", []):
        usage = shard.get("usage", {})
        for key in output:
            output[key] += int(usage.get(key, 0) or 0)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--replacement", type=Path, required=True)
    parser.add_argument("--replace-case", action="append", required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    base_rows = _rows(args.base)
    replacement = {row["sub_question_id"]: row for row in _rows(args.replacement)}
    replace_ids = set(args.replace_case)
    if replace_ids - set(replacement):
        raise ValueError("replacement artifact lacks requested case")
    output = [replacement.get(row["sub_question_id"], row) if row["sub_question_id"] in replace_ids else row for row in base_rows]
    plan_ids = [row["sub_question_id"] for row in _rows(args.plan_artifact)]
    if [row["sub_question_id"] for row in output] != plan_ids:
        raise ValueError("merged Call 2 case universe differs from planner")

    base_manifest = json.loads(args.base.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old_by_id = {row["sub_question_id"]: row for row in base_rows}
    usage = dict(base_manifest["usage"])
    for case_id in replace_ids:
        old_usage = _row_usage(old_by_id[case_id])
        new_usage = _row_usage(replacement[case_id])
        for key in usage:
            usage[key] = int(usage[key]) - old_usage.get(key, 0) + new_usage.get(key, 0)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    count_fields = (
        "physical_request_count",
        "assessment_target_count",
        "neural_predicate_request_target_count",
        "relation_assessment_target_count",
        "participation_local_target_count",
        "factual_utilization_target_count",
        "utilized_participant_outcome_target_count",
        "utilized_participant_predicate_target_count",
    )
    manifest = dict(base_manifest)
    manifest.update(
        {
            "status": "SUCCEEDED",
            "logical_stage_count": len(output),
            "usage": usage,
            "plan_artifact_sha256": _sha256(args.plan_artifact),
            "base_artifact": str(args.base),
            "base_artifact_sha256": _sha256(args.base),
            "replacement_artifact": str(args.replacement),
            "replacement_artifact_sha256": _sha256(args.replacement),
            "replaced_case_ids": sorted(replace_ids),
            "merge_rule": "replace only planner-changed cases; preserve unchanged model rows",
        }
    )
    for field in count_fields:
        manifest[field] = sum(int(row.get(field, 0)) for row in output)
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
