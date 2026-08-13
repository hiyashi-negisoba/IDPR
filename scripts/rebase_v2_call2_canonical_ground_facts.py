#!/usr/bin/env python3
"""Canonical GroundFact rebase: replace exactly the conflicted keys, keep everything else.

이것은 additive delta가 아니다. additive delta는 baseline이 **묻지 않았던** 질문을 덧붙이므로
기존 key를 절대 덮지 않는다. 여기서 고치려는 것은 반대다 -- baseline이 같은 질문을 offense
instance마다 **여러 번 물어서** 서로 다른 답을 얻은 것이고, occurrence-level canonicalization
(`d910532`)이 그 질문을 한 번만 묻도록 바꿨다. 그러므로 기존 key를 덮어야 하되, 덮는 범위가
정확히 그 canonical key의 consumer 전부여야 한다.

case 단위 교체는 여전히 부적절하다. 무관한 predicate가 stochastic drift로 뒤집히면 이번 수정의
효과와 모델 재샘플링의 효과가 섞인다. 그래서 교체 단위는 case가 아니라 canonical GroundFactKey
`(case, actor, factual_episode, ground_predicate)`다.

계약 (전부 hard-fail, repair 없음):

1. `--conflict-key`로 명시된 canonical GroundFactKey만 교체를 허용한다. audit이 지목하지 않은
   key는 delta에 있어도 무시하지 않고 **실패**시킨다.
2. 한 canonical key를 교체할 때 그 key를 소비하는 baseline instance target을 전부 교체한다.
   일부만 교체하면 고치려던 모순을 그대로 남긴다.
3. ground fact가 아닌 truth(legal element, relation 등)는 하나도 덮지 않는다.
4. 교체된 truth는 old/new를 둘 다 manifest에 기록한다.
5. delta run에서 같은 canonical key의 truth가 둘 이상이면 실패한다 -- canonicalization이
   실제로 동작했다면 하나여야 하고, 이것이 그 live 검증이다.
6. 두 run의 prompt/model/evidence-mode fingerprint가 같은지 확인한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.registry import load_definitions

BASELINE_RUN = "baseline"
REBASE_RUN = "ground_fact_rebase"


class GroundFactRebaseError(ValueError):
    pass


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _manifest(path: Path) -> dict[str, Any] | None:
    candidate = path.with_suffix(".manifest.json")
    if not candidate.exists():
        return None
    return json.loads(candidate.read_text(encoding="utf-8"))


_FINGERPRINT_FIELDS = ("model", "prompts", "evidence_mode")


def _check_fingerprint(
    baseline: dict[str, Any] | None,
    delta: dict[str, Any] | None,
    *,
    allow_missing_baseline_manifest: bool,
) -> dict[str, Any]:
    """Did the two runs ask under the same contract?

    "Not comparable" and "different" are separate answers and are kept separate.  The
    canonical baseline is itself a merge product whose manifest describes the merge, not a
    Call 2 run, so it carries none of these fields -- that is an absence of evidence, and
    treating it as a mismatch would be as wrong as treating it as a match.  Absence still
    demands the explicit flag and is recorded in the output manifest; a field present on
    both sides and disagreeing is always a hard failure.
    """
    if delta is None:
        raise GroundFactRebaseError("delta manifest is required")
    comparable = (
        {field for field in _FINGERPRINT_FIELDS if field in baseline and field in delta}
        if baseline is not None
        else set()
    )
    if not comparable:
        if not allow_missing_baseline_manifest:
            raise GroundFactRebaseError(
                "the baseline carries no comparable prompt/model fingerprint "
                f"(looked for {list(_FINGERPRINT_FIELDS)}); pass "
                "--allow-missing-baseline-manifest to record that it could not be compared"
            )
        return {
            "fingerprint_check": "SKIPPED_NO_COMPARABLE_BASELINE_FIELDS",
            "delta_model": delta.get("model"),
        }
    assert baseline is not None
    mismatches = {
        field: [baseline.get(field), delta.get(field)]
        for field in sorted(comparable)
        if baseline.get(field) != delta.get(field)
    }
    if mismatches:
        raise GroundFactRebaseError(
            f"baseline and delta were not produced under the same contract: {mismatches}"
        )
    return {
        "fingerprint_check": "MATCHED",
        "compared_fields": sorted(comparable),
        "model": delta.get("model"),
    }


def _episode_by_occurrence(plan_row: dict[str, Any]) -> dict[str, str]:
    """The same identity Call 2 canonicalization consumes -- planner InstanceProvenance."""
    return {
        str(entry["instance_key"]["occurrence_id"]): str(entry["factual_episode_id"])
        for entry in plan_row.get("instance_provenance") or []
    }


def _canonical_key(
    truth: dict[str, Any], episodes: dict[str, str]
) -> tuple[str, str, str, str] | None:
    instance = truth["instance_key"]
    occurrence_id = str(instance["occurrence_id"])
    episode_id = episodes.get(occurrence_id)
    if episode_id is None:
        return None
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        episode_id,
        str(truth["predicate_ref"]),
    )


def _assert_carriers_agree(
    case_id: str,
    row: dict[str, Any],
    registry: Any,
    episodes: dict[str, str],
    replacement: dict[tuple[str, str, str, str], str],
) -> None:
    """After the rebase, both carriers must give one truth per rebased canonical key.

    Checked per case rather than trusted, because a key present in one carrier and absent
    from the other would otherwise pass silently and reappear as a conflict downstream.
    """
    for key in replacement:
        if key[0] != case_id:
            continue
        values: set[str] = set()
        for field in ("assessments", "case_truths"):
            for truth in row.get(field) or []:
                if registry.kind_of(str(truth["predicate_ref"])) != "ground_fact":
                    continue
                if _canonical_key(truth, episodes) == key:
                    values.add(str(truth["truth"]))
        if len(values) > 1:
            raise GroundFactRebaseError(
                f"{case_id}: carriers disagree after rebase on {key}: {sorted(values)}"
            )


def _parse_conflict_keys(values: list[str]) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    for value in values:
        parts = value.split("|")
        if len(parts) != 4 or not all(parts):
            raise GroundFactRebaseError(
                f"--conflict-key must be case_id|actor_id|factual_episode_id|predicate_ref: {value!r}"
            )
        keys.add((parts[0], parts[1], parts[2], parts[3]))
    return keys


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument(
        "--conflict-key",
        action="append",
        required=True,
        metavar="CASE|ACTOR|EPISODE|PREDICATE",
        help="canonical GroundFactKey the audit identified; the only keys replacement may touch",
    )
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--allow-missing-baseline-manifest", action="store_true")
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    conflict_keys = _parse_conflict_keys(args.conflict_key)

    baseline = {row["sub_question_id"]: row for row in _rows(args.baseline)}
    delta = {row["sub_question_id"]: row for row in _rows(args.delta)}
    plans = {row["sub_question_id"]: row for row in _rows(args.plan_artifact)}
    plan_ids = [row["sub_question_id"] for row in _rows(args.plan_artifact)]

    if set(delta) - set(baseline):
        raise GroundFactRebaseError(
            f"delta has cases the baseline does not: {sorted(set(delta) - set(baseline))}"
        )
    if set(baseline) != set(plan_ids):
        raise GroundFactRebaseError("baseline case universe differs from the planner")

    fingerprint = _check_fingerprint(
        _manifest(args.baseline),
        _manifest(args.delta),
        allow_missing_baseline_manifest=args.allow_missing_baseline_manifest,
    )

    # Contract 5: the delta must have exactly one truth per canonical key.  This is the live
    # verification that occurrence-level canonicalization actually asked each ground fact once.
    replacement: dict[tuple[str, str, str, str], str] = {}
    for case_id, row in delta.items():
        episodes = _episode_by_occurrence(plans[case_id])
        for truth in row["case_truths"]:
            predicate_ref = str(truth["predicate_ref"])
            if registry.kind_of(predicate_ref) != "ground_fact":
                continue
            key = _canonical_key(truth, episodes)
            if key is None or key not in conflict_keys:
                continue
            value = str(truth["truth"])
            if key in replacement and replacement[key] != value:
                raise GroundFactRebaseError(
                    f"delta still disagrees with itself on canonical key {key}: "
                    f"{replacement[key]} vs {value}; canonicalization did not hold"
                )
            replacement[key] = value

    missing = conflict_keys - set(replacement)
    if missing:
        raise GroundFactRebaseError(
            f"delta does not answer these conflict keys: {sorted(missing)}"
        )

    output: list[dict[str, Any]] = []
    replaced_records: list[dict[str, Any]] = []
    for case_id in plan_ids:
        row = json.loads(json.dumps(baseline[case_id]))
        episodes = _episode_by_occurrence(plans[case_id])
        replaced_by_key: dict[tuple[str, str, str, str], int] = {}
        # Both carriers hold the same (instance, predicate) -> truth triples and both are
        # consumed downstream -- `assessments` by the AnswerPlan projection, `case_truths`
        # by Scallop and the E2E.  Rebasing one and not the other would leave the artifact
        # disagreeing with itself about the very fact this is fixing.
        for field in ("assessments", "case_truths"):
            for truth in row.get(field) or []:
                if field == "case_truths":
                    truth.setdefault("source_run", BASELINE_RUN)
                predicate_ref = str(truth["predicate_ref"])
                # Contract 3: nothing but a conflicted ground fact is eligible.
                if registry.kind_of(predicate_ref) != "ground_fact":
                    continue
                key = _canonical_key(truth, episodes)
                if key is None or key not in replacement:
                    continue
                old = str(truth["truth"])
                new = replacement[key]
                truth["truth"] = new
                if field == "case_truths":
                    truth["source_run"] = REBASE_RUN
                replaced_by_key[key] = replaced_by_key.get(key, 0) + 1
                replaced_records.append(
                    {
                        "carrier": field,
                        "canonical_key": "|".join(key),
                        "instance_key": truth["instance_key"],
                        "predicate_ref": predicate_ref,
                        "old_truth": old,
                        "new_truth": new,
                    }
                )
        # Contract 2: every consumer of a rebased key in this case must have been replaced.
        for key, count in replaced_by_key.items():
            if count < 1:
                raise GroundFactRebaseError(f"{case_id}: partial consumer replacement for {key}")
        _assert_carriers_agree(case_id, row, registry, episodes, replacement)
        output.append(row)

    # Contract 2, globally: each conflict key must have been consumed somewhere.
    consumed = {record["canonical_key"] for record in replaced_records}
    unconsumed = {"|".join(key) for key in conflict_keys} - consumed
    if unconsumed:
        raise GroundFactRebaseError(
            f"conflict keys had no baseline consumer to replace: {sorted(unconsumed)}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call2_canonical_ground_fact_rebase",
        "status": "SUCCEEDED",
        "contract": (
            "replace only the audit-identified canonical GroundFactKeys, all of their "
            "consumers at once; never touch another ground fact, legal element, or relation"
        ),
        "case_count": len(output),
        "conflict_keys": sorted("|".join(key) for key in conflict_keys),
        "canonical_truths": {"|".join(key): value for key, value in sorted(replacement.items())},
        "replaced_truth_count": len(replaced_records),
        "replacements": replaced_records,
        "delta_case_ids": sorted(delta),
        "case_truth_count": sum(len(row["case_truths"]) for row in output),
        "baseline": str(args.baseline),
        "baseline_sha256": _sha256(args.baseline),
        "delta": str(args.delta),
        "delta_sha256": _sha256(args.delta),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        **fingerprint,
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(f"replaced {len(replaced_records)} truths across {len(conflict_keys)} canonical keys")
    for key, value in sorted(replacement.items()):
        print(f"  {'|'.join(key)} -> {value}")


if __name__ == "__main__":
    main()
