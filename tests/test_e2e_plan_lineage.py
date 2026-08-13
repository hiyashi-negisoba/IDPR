"""정본 E2E는 참가 병합을 거친 plan만 받는다.

2026-08-13에 실제로 난 회귀를 잠근다. `evaluation_instance_plan.jsonl`을 `--plan`에 넘겼더니
참가 instance가 통째로 빠졌고 excess finding 1건과 방화 instance 1건이 함께 사라진 결과가
**아무 오류 없이** 나왔다. 조용히 다른 답을 내는 실행 인자는 계약으로 막는다.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _module():
    path = ROOT / "scripts/run_v2_scallop_e2e.py"
    spec = importlib.util.spec_from_file_location("run_v2_scallop_e2e", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "src"))
    spec.loader.exec_module(module)
    return module


def _plan(directory: Path, name: str, *, step: str | None, row: dict) -> Path:
    path = directory / name
    path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    if step is not None:
        path.with_suffix(".manifest.json").write_text(
            json.dumps({"step": step}), encoding="utf-8"
        )
    return path


def test_a_participation_plan_passes_the_lineage_guard(tmp_path: Path) -> None:
    module = _module()
    path = _plan(
        tmp_path,
        "participation_plan.jsonl",
        step="v2_factual_participation_plan",
        row={"sub_question_id": "case", "factual_interaction_count": 1},
    )
    assert module.require_participation_plan_lineage(path)["plan_lineage"] == "MANIFEST_MATCHED"


def test_a_bare_evaluation_plan_is_rejected(tmp_path: Path) -> None:
    module = _module()
    path = _plan(
        tmp_path,
        "evaluation_instance_plan.jsonl",
        step="v2_evaluation_instance_planner",
        row={"sub_question_id": "case"},
    )
    with pytest.raises(ValueError, match="v2_factual_participation_plan"):
        module.require_participation_plan_lineage(path)
    assert (
        module.require_participation_plan_lineage(
            path, allow_non_participation_plan=True
        )["plan_lineage"]
        == "OVERRIDDEN"
    )


def test_a_manifestless_plan_falls_back_to_the_row_field(tmp_path: Path) -> None:
    """manifest가 없어도 참가 빌더만 쓰는 행 필드로 2차 확인한다."""
    module = _module()
    participation = _plan(
        tmp_path,
        "merged.jsonl",
        step=None,
        row={"sub_question_id": "case", "factual_interaction_count": 0},
    )
    assert (
        module.require_participation_plan_lineage(participation)["plan_lineage"]
        == "ROW_FIELD_MATCHED"
    )
    bare = _plan(tmp_path, "bare.jsonl", step=None, row={"sub_question_id": "case"})
    with pytest.raises(ValueError, match="not a v2_factual_participation_plan"):
        module.require_participation_plan_lineage(bare)


def test_the_canonical_run_uses_a_participation_plan() -> None:
    """정본 산출물 자체가 계약을 만족하는지 -- 문서가 아니라 파일로 확인한다."""
    module = _module()
    path = (
        ROOT
        / "experiments/v2_call15_directscope_26_causal/final_responsibility_v10"
        / "participation_plan.jsonl"
    )
    if not path.exists():  # experiments/ is gitignored
        pytest.skip("canonical run artifact is not present in this checkout")
    assert module.require_participation_plan_lineage(path)["plan_step"] == (
        "v2_factual_participation_plan"
    )
