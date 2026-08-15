"""plan 계보. 소비자는 마지막 단계의 이름이 아니라 거쳐 온 단계를 본다.

plan은 한 번 만들고 끝나는 파일이 아니라 증강되는 파일이다. 참가 병합 위에 doctrine target이
얹히면 마지막 `step` 이름은 당연히 달라진다. 그런데 symbolic 가드는 이름 하나를 하드코딩해서
확인했고, 그래서 **실제로 참가 병합을 거친** plan을 거부하며 체인을 끊었다.

이 파일이 검사하는 것은 하나다 -- **증강 단계는 계보를 이어받고, 소비자는 계보로 확인한다.**
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from idpr.v2.runtime.plan_lineage import (
    LINEAGE_KEY,
    PlanLineageError,
    definitions_drift,
    lineage_for_manifest,
    passed_through,
    plan_lineage,
    provenance,
    require_fresh_inputs,
    stale_inputs,
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


# --------------------------------------------------------------------------
# 계보의 두 번째 질문: 거쳐 온 단계들이 **지금 그 파일**을 읽었는가
# --------------------------------------------------------------------------


def test_a_regenerated_upstream_artifact_is_rejected_downstream(tmp_path: Path) -> None:
    """축별 수정과 부분 재실행을 섞어 돌릴 때 조용히 만들어지던 조합.

    단계 이름은 다 맞는데 상류 파일이 그 뒤에 다시 생성된 상태다. 코드가 바뀌어도 옛 상류
    artifact를 그대로 읽고 이어 돌리면, 상류의 의미와 하류의 가정이 어긋난 채로 끝까지
    간다. 이름만 보는 계보로는 보이지 않는다.
    """
    base = _plan(tmp_path, "base", {"step": "v2_evaluation_instance_plan"})
    doctrine = _plan(
        tmp_path,
        "doctrine",
        {
            "step": DOCTRINE_STEP,
            LINEAGE_KEY: list(lineage_for_manifest(base, DOCTRINE_STEP)),
            **provenance({"plan": base}),
        },
    )
    assert stale_inputs(doctrine) == ()
    require_fresh_inputs(doctrine)

    base.write_text('{"regenerated": true}\n', encoding="utf-8")
    problems = stale_inputs(doctrine)
    assert problems and "changed after" in problems[0]
    with pytest.raises(PlanLineageError):
        require_fresh_inputs(doctrine)


def test_the_whole_ancestry_is_walked_not_just_the_parent(tmp_path: Path) -> None:
    base = _plan(tmp_path, "base", {"step": "v2_evaluation_instance_plan"})
    participation = _plan(
        tmp_path,
        "participation",
        {"step": PARTICIPATION_STEP, **provenance({"plan": base})},
    )
    doctrine = _plan(
        tmp_path,
        "doctrine",
        {"step": DOCTRINE_STEP, **provenance({"plan": participation})},
    )
    base.write_text('{"regenerated": true}\n', encoding="utf-8")
    assert stale_inputs(doctrine), "조부모가 바뀐 것은 부모만 봐서는 보이지 않는다"


def test_an_old_artifact_without_input_hashes_is_unverifiable_not_stale(
    tmp_path: Path,
) -> None:
    """확인할 수 없는 것과 틀린 것은 다르다. 옛 산출물을 소급해 거부하지 않는다."""
    legacy = _plan(tmp_path, "legacy", {"step": DOCTRINE_STEP})
    assert stale_inputs(legacy) == ()


def test_definition_drift_is_reported_but_does_not_abort(tmp_path: Path) -> None:
    """Call 2 산출물은 비싸다. 저작 한 줄 때문에 그것을 버리게 하면 계약이 아니라 장애다."""
    definitions = tmp_path / "definitions"
    definitions.mkdir()
    (definitions / "offenses.yaml").write_text("- id: offense.x\n", encoding="utf-8")
    plan = _plan(
        tmp_path,
        "plan",
        {"step": DOCTRINE_STEP, **provenance({}, definitions_dir=definitions)},
    )
    assert definitions_drift(plan, definitions) == ()
    (definitions / "offenses.yaml").write_text("- id: offense.y\n", encoding="utf-8")
    assert definitions_drift(plan, definitions)
    require_fresh_inputs(plan)  # 규칙베이스 변경은 계보를 끊지 않는다


BUILDERS = (
    "scripts/build_v2_factual_participation_plan.py",
    "scripts/build_v2_doctrine_target_plan.py",
)


def _provenance_block(source: str) -> str:
    start = source.index("plan_provenance(")
    depth = 0
    for offset in range(start, len(source)):
        if source[offset] == "(":
            depth += 1
        elif source[offset] == ")":
            depth -= 1
            if depth == 0:
                return source[start : offset + 1]
    raise AssertionError("unbalanced plan_provenance call")


@pytest.mark.parametrize("builder", BUILDERS)
def test_every_artifact_a_builder_reads_is_in_the_freshness_chain(builder: str) -> None:
    """기록하는 목록과 검증하는 목록이 같아야 한다.

    입력 해시를 manifest 어딘가에 적어 두는 것만으로는 아무것도 걸러지지 않는다.
    `stale_inputs()`가 따라가는 것은 `plan_inputs`뿐이고, 거기 빠진 입력은 나중에 다시
    생성되어도 조용히 통과한다. 실제로 참가 빌더의 상호작용 artifact가 그 상태였다.

    출력과 정의 디렉터리는 제외한다 -- 전자는 입력이 아니고, 후자는 별도 해시로 다룬다.
    """
    root = Path(__file__).resolve().parents[1]
    source = (root / builder).read_text(encoding="utf-8")
    inputs = {
        name.replace("-", "_")
        for name in re.findall(r'add_argument\("--([a-z0-9-]+)", type=Path', source)
    } - {"out", "definitions"}
    assert inputs, builder
    block = _provenance_block(source)
    missing = sorted(name for name in inputs if f"args.{name}" not in block)
    assert not missing, f"{builder}: freshness chain is missing {missing}"
