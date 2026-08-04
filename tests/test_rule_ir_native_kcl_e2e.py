from __future__ import annotations

from pathlib import Path

import pytest

from idpr.generation.native_hybrid_answer import (
    NativeHybridAnswerError,
    finalize_hybrid_answer,
    hybrid_answer_schema,
    render_hybrid_markdown,
)
from idpr.rulegen.native_host import NativeHostError
from scripts.run_rule_ir_native_kcl_e2e import (
    ROOT,
    _allowed_units,
    _native_fact_schema,
    _require_prompt_audit,
    _role_values,
)


def test_runner_refuses_unreviewed_or_changed_prompts(tmp_path: Path) -> None:
    report = _require_prompt_audit(
        ROOT / "data/e2e/rule_ir_native/prompt_audit.json"
    )
    assert report["status"] == "pass"

    bad = tmp_path / "audit.json"
    bad.write_text('{"status":"fail","api_calls":0}', encoding="utf-8")
    with pytest.raises(ValueError, match="did not pass"):
        _require_prompt_audit(bad)


def test_native_fact_and_unit_selection_are_search_free_and_closed() -> None:
    schema = _native_fact_schema()
    assert schema["properties"]["issue_candidates"]["maxItems"] == 0
    assert schema["properties"]["retrieval_queries"]["maxItems"] == 0
    units = _allowed_units()
    assert len(units) == 36
    assert len({item["unit_id"] for item in units}) == 36
    assert all("search_score" not in item for item in units)


def test_role_tuple_is_registry_owned() -> None:
    values = _role_values(
        case_id="case-1",
        unit_id="theft",
        candidates={
            "defendant_id": "defendant",
            "owner_id": "owner",
            "possessor_id": "possessor",
        },
    )
    assert values["case_id"] == "case-1"
    with pytest.raises(NativeHostError, match="missing possessor_id"):
        _role_values(
            case_id="case-1",
            unit_id="theft",
            candidates={"defendant_id": "defendant", "owner_id": "owner"},
        )


def test_hybrid_writer_separates_symbolic_and_model_only_conclusions() -> None:
    request = {
        "case_id": "case-1",
        "sections": [
            {
                "section_id": "special",
                "heading": "절도",
                "authority": "rule_ir_scallop",
                "symbolic_directive": "established",
                "established_relations": ["theft_established"],
            },
            {
                "section_id": "general",
                "heading": "피해자 승낙의 착오",
                "authority": "model_only_general_part_experiment",
            },
        ],
    }
    schema = hybrid_answer_schema(request["sections"])
    supported = schema["properties"]["sections"]["prefixItems"][0]
    general = schema["properties"]["sections"]["prefixItems"][1]
    assert "conclusion" not in supported["properties"]
    assert "provisional_conclusion" not in supported["properties"]
    assert "provisional_conclusion" in general["properties"]

    model = {
        "version": "1.0.0",
        "sections": [
            {"section_id": "special", "rule": "법리", "application": "적용"},
            {
                "section_id": "general",
                "rule": "총칙 법리",
                "application": "총칙 적용",
                "provisional_conclusion": "착오에 정당한 이유가 없다.",
            },
        ],
    }
    answer = finalize_hybrid_answer(request=request, model_payload=model)
    assert answer["sections"][0]["conclusion"] == "성립"
    assert answer["sections"][0]["authority"] == "rule_ir_scallop"
    assert answer["sections"][1]["authority"] == "model_only_general_part_experiment"
    assert "비기호 총칙 분석" in render_hybrid_markdown(answer)

    model["sections"][0]["conclusion"] = "불성립"
    with pytest.raises(NativeHybridAnswerError):
        finalize_hybrid_answer(request=request, model_payload=model)
