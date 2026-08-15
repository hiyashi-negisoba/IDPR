"""plan 계보. 소비자는 마지막 단계의 이름이 아니라 거쳐 온 단계를 본다.

plan은 한 번 만들고 끝나는 파일이 아니라 증강되는 파일이다. 참가 병합 위에 doctrine target이
얹히면 마지막 `step` 이름은 당연히 달라진다. 그런데 symbolic 가드는 이름 하나를 하드코딩해서
확인했고, 그래서 **실제로 참가 병합을 거친** plan을 거부하며 체인을 끊었다.

이 파일이 검사하는 것은 하나다 -- **증강 단계는 계보를 이어받고, 소비자는 계보로 확인한다.**
"""

from __future__ import annotations

import json
from pathlib import Path

from idpr.v2.runtime.plan_lineage import (
    LINEAGE_KEY,
    lineage_for_manifest,
    passed_through,
    plan_lineage,
)

PARTICIPATION_STEP = "v2_factual_participation_plan"
DOCTRINE_STEP = "v2_doctrine_target_plan"


def _plan(tmp_path: Path, name: str, manifest: dict | None) -> Path:
    path = tmp_path / f"{name}.jsonl"
    path.write_text("{}\n", encoding="utf-8")
    if manifest is not None:
        path.with_suffix(".manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
        )
    return path


def test_an_augmenting_step_inherits_the_chain(tmp_path: Path) -> None:
    base = _plan(tmp_path, "base", {"step": "v2_evaluation_instance_plan"})
    participation = _plan(
        tmp_path,
        "participation",
        {
            "step": PARTICIPATION_STEP,
            LINEAGE_KEY: list(lineage_for_manifest(base, PARTICIPATION_STEP)),
        },
    )
    doctrine = _plan(
        tmp_path,
        "doctrine",
        {
            "step": DOCTRINE_STEP,
            LINEAGE_KEY: list(lineage_for_manifest(participation, DOCTRINE_STEP)),
        },
    )
    assert plan_lineage(doctrine) == (
        "v2_evaluation_instance_plan",
        PARTICIPATION_STEP,
        DOCTRINE_STEP,
    )


def test_a_downstream_step_does_not_hide_the_participation_merge(tmp_path: Path) -> None:
    """이것이 2026-08-15에 체인을 끊은 그 상태다."""
    participation = _plan(
        tmp_path, "participation", {"step": PARTICIPATION_STEP, LINEAGE_KEY: [PARTICIPATION_STEP]}
    )
    doctrine = _plan(
        tmp_path,
        "doctrine",
        {
            "step": DOCTRINE_STEP,
            LINEAGE_KEY: list(lineage_for_manifest(participation, DOCTRINE_STEP)),
        },
    )
    assert passed_through(doctrine, PARTICIPATION_STEP)


def test_a_step_that_drops_the_chain_is_not_credited(tmp_path: Path) -> None:
    """계보를 이어받지 않는 새 증강 단계는 통과하지 못한다. 그것이 가드의 요점이다."""
    orphan = _plan(tmp_path, "orphan", {"step": DOCTRINE_STEP})
    assert plan_lineage(orphan) == (DOCTRINE_STEP,)
    assert not passed_through(orphan, PARTICIPATION_STEP)


def test_a_legacy_manifest_reads_as_its_single_step(tmp_path: Path) -> None:
    legacy = _plan(tmp_path, "legacy", {"step": PARTICIPATION_STEP})
    assert passed_through(legacy, PARTICIPATION_STEP)


def test_no_manifest_is_no_lineage_not_a_crash(tmp_path: Path) -> None:
    assert plan_lineage(_plan(tmp_path, "bare", None)) == ()
