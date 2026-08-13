#!/usr/bin/env python3
"""Append-only Call 2 delta merge: baseline truths + targets that did not exist before.

이것은 "예전 truth를 새 실행 결과로 섞는 것"이 아니다. baseline에는 **묻지 않았던 질문**이
delta에 추가된 것이고, 그래서 한 case 안에 서로 다른 실행 provenance가 섞이는 것이 문제가
되지 않는다. 질문 자체가 서로 다른 시점에 열렸기 때문이다.

case 단위 교체가 왜 부적절한지는 2026-08-13 doctrine 증분이 그대로 보여 줬다. target 19개를
추가하려고 문항 전체를 다시 물었더니 무관한 predicate 8개가 stochastic drift로 뒤집혔고,
`r11_p1_q1`의 기존 liability 2건이 회귀했다. 그것을 정본으로 삼으면 doctrine 구현의 효과와
모델 재샘플링의 효과가 섞여 둘을 분리할 수 없다.

계약 (전부 hard-fail, repair 없음):

1. baseline에 이미 있는 target key는 절대 덮어쓰지 않는다.
2. delta에는 baseline에 없던 target key만 허용한다.
3. 같은 key가 delta 안에서 중복되면 실패한다.
4. 각 truth는 어느 run에서 왔는지 provenance를 갖는다.
5. 두 run의 target/prompt 계약 fingerprint가 같은지 확인한다. 다르면 같은 질문이 아니다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BASELINE_RUN = "baseline"
DELTA_RUN = "delta"


class AdditiveDeltaError(ValueError):
    pass


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _key(truth: dict[str, Any]) -> tuple[str, str, str, str]:
    instance = truth["instance_key"]
    return (
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        str(truth["predicate_ref"]),
    )


def _manifest(path: Path) -> dict[str, Any] | None:
    candidate = path.with_suffix(".manifest.json")
    if not candidate.exists():
        return None
    return json.loads(candidate.read_text(encoding="utf-8"))


def _check_fingerprint(
    baseline: dict[str, Any] | None,
    delta: dict[str, Any] | None,
    *,
    allow_missing_baseline_manifest: bool,
) -> dict[str, Any]:
    """두 run이 같은 계약으로 물었는지 확인한다.

    baseline manifest가 없는 경우가 실제로 있다(v8 artifact). 그때는 확인을 조용히 건너뛰지
    않고 명시적 플래그를 요구하며, 확인하지 못했다는 사실을 출력 manifest에 남긴다.
    """
    if baseline is None:
        if not allow_missing_baseline_manifest:
            raise AdditiveDeltaError(
                "baseline manifest is missing; pass --allow-missing-baseline-manifest to "
                "record that the prompt/model fingerprint could not be compared"
            )
        return {"fingerprint_check": "SKIPPED_MISSING_BASELINE_MANIFEST"}
    if delta is None:
        raise AdditiveDeltaError("delta manifest is required")
    mismatches = {
        field: [baseline.get(field), delta.get(field)]
        for field in ("model", "prompts", "evidence_mode")
        if baseline.get(field) != delta.get(field)
    }
    if mismatches:
        raise AdditiveDeltaError(
            f"baseline and delta were not produced under the same contract: {mismatches}"
        )
    return {"fingerprint_check": "MATCHED", "model": delta.get("model")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--carry-field",
        action="append",
        default=["candidate_doctrine_refs"],
        help="delta row field that replaces the baseline field (plan-derived, not a truth)",
    )
    parser.add_argument("--allow-missing-baseline-manifest", action="store_true")
    args = parser.parse_args()

    baseline = {row["sub_question_id"]: row for row in _rows(args.baseline)}
    delta = {row["sub_question_id"]: row for row in _rows(args.delta)}
    plan_ids = [row["sub_question_id"] for row in _rows(args.plan_artifact)]
    if set(delta) - set(baseline):
        raise AdditiveDeltaError(
            f"delta has cases the baseline does not: {sorted(set(delta) - set(baseline))}"
        )
    if set(baseline) != set(plan_ids):
        raise AdditiveDeltaError("baseline case universe differs from the planner")

    fingerprint = _check_fingerprint(
        _manifest(args.baseline),
        _manifest(args.delta),
        allow_missing_baseline_manifest=args.allow_missing_baseline_manifest,
    )

    output: list[dict[str, Any]] = []
    appended = 0
    for case_id in plan_ids:
        row = json.loads(json.dumps(baseline[case_id]))
        for truth in row["case_truths"]:
            truth.setdefault("source_run", BASELINE_RUN)
        if case_id in delta:
            existing = {_key(truth) for truth in row["case_truths"]}
            seen: set[tuple[str, str, str, str]] = set()
            for truth in delta[case_id]["case_truths"]:
                key = _key(truth)
                if key in seen:
                    raise AdditiveDeltaError(f"{case_id}: duplicate delta target {key}")
                seen.add(key)
                if key in existing:
                    # 계약 1·2. baseline이 이미 답한 질문은 delta의 관심사가 아니다.
                    continue
                appended += 1
                output_truth = dict(truth)
                output_truth["source_run"] = DELTA_RUN
                row["case_truths"].append(output_truth)
            for field in args.carry_field:
                if field in delta[case_id]:
                    row[field] = delta[case_id][field]
        output.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call2_additive_delta_merge",
        "status": "SUCCEEDED",
        "contract": (
            "append-only: baseline target keys are never overwritten; the delta may only add "
            "target keys the baseline never asked; every truth carries its source run"
        ),
        "case_count": len(output),
        "appended_truth_count": appended,
        "delta_case_ids": sorted(delta),
        "case_truth_count": sum(len(row["case_truths"]) for row in output),
        "baseline": str(args.baseline),
        "baseline_sha256": _sha256(args.baseline),
        "delta": str(args.delta),
        "delta_sha256": _sha256(args.delta),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "carried_fields": list(args.carry_field),
        **fingerprint,
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(f"appended {appended} truths from {len(delta)} delta cases")


if __name__ == "__main__":
    main()
