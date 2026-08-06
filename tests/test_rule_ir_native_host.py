from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.generation.native_rule_ir_answer import (
    NativeGenerationError,
    build_native_section_requests,
    finalize_native_answer,
    render_native_answer,
)
from idpr.rulegen.native_host import (
    DEFAULT_SCLI,
    NativeHostError,
    execute_native_case,
    execute_native_unit,
    predicate_assessment_request,
    selected_predicate_requests,
    validate_closed_issue_selection,
    validate_predicate_assessment,
)
from idpr.rulegen.registry import build_registry
from scripts.run_p2_native_scallop_golden import UnitScenarios
from scripts.run_property_scallop_golden import scenarios_for


ROOT = Path(__file__).resolve().parents[1]
CASE_TEXT = "피고인이 피해자에게 행위하였다."


def _roles(unit_id: str, scenario: dict, **overrides: str) -> dict[str, str]:
    entry = build_registry()[unit_id]
    values = {
        argument["name"]: scenario[argument["name"]]
        for argument in entry.role_predicate["arguments"]
    }
    values.update(overrides)
    values["case_id"] = "case-1"
    return values


def _assessment(unit_id: str, scenario: dict, *, issue_id: str) -> dict:
    entry = build_registry()[unit_id]
    status_by_card = {
        item["card_id"]: item["status"] for item in scenario["assessments"]
    }
    assessments = {}
    for predicate in entry.commentary_inputs:
        card_id = predicate["norm_card_ids"][0]
        status = status_by_card.get(card_id, "unknown")
        assessments[predicate["id"]] = {
            "status": status,
            "source_quotes": [CASE_TEXT] if status != "unknown" else [],
            "missing_facts": ["판단에 필요한 구체적 사실"] if status == "unknown" else [],
        }
    return {
        "version": "1.0.0",
        "case_id": "case-1",
        "issue_id": issue_id,
        "unit_id": unit_id,
        "role_values": _roles(unit_id, scenario),
        "distinct_entities": scenario.get("distinct_entities", []),
        "assessments": assessments,
    }


def _issue(issue_id: str, unit_id: str, *, dependencies: list[str] | None = None) -> dict:
    entry = build_registry().get(unit_id)
    roles = (
        {
            argument["name"]: f"{argument['name']}-1"
            for argument in entry.role_predicate["arguments"]
            if argument["name"] != "case_id"
        }
        if entry is not None
        else {}
    )
    return {
        "issue_id": issue_id,
        "unit_id": unit_id,
        "reported_label": "미지원 쟁점" if unit_id == "unsupported" else unit_id,
        "source_quote": CASE_TEXT,
        "role_candidates": roles,
        "depends_on_issue_ids": dependencies or [],
    }


def test_request_loads_every_registered_predicate_without_fact_graph() -> None:
    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    issue = _issue("issue-1", "rape")
    request = predicate_assessment_request(
        case=case, issue=issue, unit_id="rape"
    )
    assert request["all_registered_predicates_loaded"] is True
    assert len(request["predicates"]) == len(
        build_registry()["rape"].commentary_inputs
    )
    assert request["case_text"] == CASE_TEXT
    assert "facts" not in request

    missing = predicate_assessment_request(
        case=case, issue=issue, unit_id="criminal_procedure"
    )
    assert missing["status"] == "predicate_ir_missing"


def test_closed_selection_uses_registry_enum_and_validates_dependencies() -> None:
    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    selection = {
        "version": "1.0.0",
        "case_id": "case-1",
        "issues": [
            _issue("issue-1", "rape"),
            _issue("issue-2", "unsupported"),
        ],
    }
    result = selected_predicate_requests(case=case, selection=selection)
    assert result["selection_mode"] == "closed_registry_enum"
    assert result["semantic_search_used"] is False
    assert result["requests"][0]["assessment_request"][
        "all_registered_predicates_loaded"
    ] is True
    assert result["requests"][1]["status"] == "predicate_ir_missing"

    selection["issues"][0]["unit_id"] = "invented_crime"
    with pytest.raises(NativeHostError):
        validate_closed_issue_selection(
            selection,
            case_id="case-1",
            case_text=CASE_TEXT,
        )


def test_closed_selection_demotes_bad_label_dependency_and_missing_role() -> None:
    """A defective issue is handed back, not thrown — the case keeps its others.

    These three defects used to abort the whole run.  On the 26-item sweep that
    discarded 15 cases whose remaining issues were well formed, so each defect
    now names one issue for the writer to argue without symbolic support.
    """

    selection = {
        "version": "1.0.0",
        "case_id": "case-1",
        "issues": [_issue("issue-1", "rape")],
    }
    selection["issues"][0]["reported_label"] = "unsupported"
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    assert [item["issue_id"] for item in rejected] == ["issue-1"]
    assert "죄명" in rejected[0]["reason"]

    unsupported = _issue("issue-2", "unsupported", dependencies=["issue-1"])
    selection["issues"] = [_issue("issue-1", "rape"), unsupported]
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    # The well-formed issue survives; only the dependent one is dropped.
    assert [item["issue_id"] for item in rejected] == ["issue-2"]

    supported = _issue("issue-1", "rape")
    supported["role_candidates"].pop(next(iter(supported["role_candidates"])))
    selection["issues"] = [supported]
    rejected = validate_closed_issue_selection(
        selection, case_id="case-1", case_text=CASE_TEXT
    )
    assert "당사자 역할이 빠졌다" in rejected[0]["reason"]

    # A payload that is unusable as a whole still raises.
    selection["issues"] = [_issue("issue-1", "rape"), _issue("issue-1", "rape")]
    with pytest.raises(NativeHostError, match="unique"):
        validate_closed_issue_selection(
            selection, case_id="case-1", case_text=CASE_TEXT
        )


def test_selected_predicate_requests_tolerates_every_issue_rejected() -> None:
    """A case where per-issue rejection empties ``issues`` is a degraded case,
    not a malformed payload.

    219740 crashed two cases this way: the raw selection had issues, but every
    one of them failed the role/quote contract, and ``selected_predicate_requests``
    re-ran the same schema — with its ``minItems: 1`` for raw model output —
    against the now-empty, already-filtered selection.
    """

    case = {
        "sub_question_id": "case-1",
        "question_text": CASE_TEXT,
        "question_prompt": "죄책을 검토하라.",
    }
    filtered = {"version": "1.0.0", "case_id": "case-1", "issues": []}
    result = selected_predicate_requests(case=case, selection=filtered)
    assert result["requests"] == []

    # The model's raw output must still name at least one issue — this path
    # is unchanged.
    with pytest.raises(NativeHostError, match="non-empty"):
        validate_closed_issue_selection(
            filtered, case_id="case-1", case_text=CASE_TEXT
        )


def test_direct_assessment_requires_exact_source_quotes() -> None:
    scenario = UnitScenarios("rape").build()[0]
    payload = _assessment("rape", scenario, issue_id="issue-1")
    predicate_id = next(iter(payload["assessments"]))
    payload["assessments"][predicate_id] = {
        "status": "satisfied",
        "source_quotes": ["원문에 없는 문장"],
        "missing_facts": [],
    }
    with pytest.raises(NativeHostError, match="not in case text"):
        validate_predicate_assessment(
            payload,
            case_id="case-1",
            issue_id="issue-1",
            unit_id="rape",
            case_text=CASE_TEXT,
        )


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_host_executes_committed_nonproperty_rule_ir(tmp_path: Path) -> None:
    scenario = UnitScenarios("rape").build()[0]
    result = execute_native_unit(
        issue_id="issue-1",
        unit_id="rape",
        case_id="case-1",
        case_text=CASE_TEXT,
        assessment_payload=_assessment("rape", scenario, issue_id="issue-1"),
        work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli_committed_rule_ir"
    assert result["compiled_scl_path"] == "rules/generated/p2_rape_v1_candidate.scl"
    assert len(result["compiled_scl_sha256"]) == 64
    assert result["symbolic_conclusion"] == "established"
    assert "rape_base_established" in result["established_relations"]


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_execute_native_case_degrades_single_symbolic_execution_failure(
    tmp_path: Path,
) -> None:
    """A Scallop-fact-level defect in one issue must not discard its siblings.

    ``distinct_entities`` naming an id outside the actor tuple passes
    ``validate_predicate_assessment``'s own quote/missing-facts contract but
    fails later, at scenario rendering — a case in the 219740 sweep hit
    exactly this and lost every issue, not just the broken one.
    """

    scenario = UnitScenarios("rape").build()[0]
    good = _assessment("rape", scenario, issue_id="issue-1")
    bad = _assessment("rape", scenario, issue_id="issue-2")
    bad["distinct_entities"] = [[bad["role_values"]["defendant_id"], "no-such-entity"]]

    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-1",
                "unit_id": "rape",
                "depends_on_issue_ids": [],
                "assessment_payload": good,
            },
            {
                "issue_id": "issue-2",
                "unit_id": "rape",
                "depends_on_issue_ids": [],
                "assessment_payload": bad,
            },
        ],
        work_dir=tmp_path,
    )

    contract = report["generation_contract"]
    assert {d["issue_id"] for d in contract["conclusion_directives"]} == {"issue-1"}
    assert report["unit_results"]["issue-2"]["status"] == "symbolic_execution_failed"
    assert any(
        item["issue_id"] == "issue-2" for item in contract["skipped_directives"]
    )


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_property_outcome_bridges_into_shared_module(tmp_path: Path) -> None:
    theft_rule_ir = json.loads(
        (ROOT / "data/rulegen/property/rule_ir/theft_rule_ir_candidate.json").read_text()
    )
    theft = scenarios_for(theft_rule_ir, "theft")[0]
    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    relative_payload = _assessment(
        "relative_property_crime_exception", relative, issue_id="issue-relative"
    )
    relative_payload["role_values"]["predicate_offense_id"] = "theft"
    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-theft",
                "unit_id": "theft",
                "assessment_payload": _assessment(
                    "theft", theft, issue_id="issue-theft"
                ),
            },
            {
                "issue_id": "issue-relative",
                "unit_id": "relative_property_crime_exception",
                "depends_on_issue_ids": ["issue-theft"],
                "assessment_payload": relative_payload,
            },
        ],
        work_dir=tmp_path,
    )
    assert report["unit_results"]["issue-theft"]["symbolic_conclusion"] == "established"
    assert report["unit_results"]["issue-relative"]["symbolic_conclusion"] == "established"
    contract = report["generation_contract"]
    assert contract["source"] == "committed_rule_ir_scallop_only"
    assert contract["model_may_override_symbolic_conclusion"] is False


def test_shared_module_without_dependency_degrades_instead_of_crashing(
    tmp_path: Path,
) -> None:
    """A shared module selected with no dependency has nothing to bridge from,
    but that must demote only this one issue, not the whole case.

    219774's remaining failure (after the other three per-issue defects were
    fixed) was exactly this: the model selected a bridge-only unit as if it
    stood on its own, and the host used to raise out of the case loop for it.
    """

    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    report = execute_native_case(
        case_id="case-1",
        case_text=CASE_TEXT,
        unit_runs=[
            {
                "issue_id": "issue-relative",
                "unit_id": "relative_property_crime_exception",
                "assessment_payload": _assessment(
                    "relative_property_crime_exception",
                    relative,
                    issue_id="issue-relative",
                ),
            }
        ],
        work_dir=tmp_path,
    )
    assert (
        report["unit_results"]["issue-relative"]["status"]
        == "shared_module_missing_dependency"
    )
    assert any(
        item["issue_id"] == "issue-relative"
        for item in report["generation_contract"]["skipped_directives"]
    )


def test_section_writer_cannot_supply_host_conclusion() -> None:
    selection = {
        "issues": [
            {
                "issue_id": "issue-1",
                "unit_id": "rape",
                "reported_label": "강간죄",
            }
        ]
    }
    report = {
        "case_id": "case-1",
        "generation_contract": {
            "source": "committed_rule_ir_scallop_only",
            "conclusion_directives": [
                {
                    "issue_id": "issue-1",
                    "unit_id": "rape",
                    "symbolic_conclusion": "established",
                    "established_relations": ["rape_base_established"],
                    "evidence": {},
                    "compiled_scl_path": "rules/generated/p2_rape_v1_candidate.scl",
                    "compiled_scl_sha256": "0" * 64,
                }
            ],
        },
    }
    requests = build_native_section_requests(
        case={"question_text": CASE_TEXT, "question_prompt": "죄책"},
        selection=selection,
        native_report=report,
    )
    prose = "### 법리\n\n법리 설명\n\n### 사안의 적용\n\n사실 적용"
    answer = finalize_native_answer(
        section_requests=requests, prose_by_issue={"issue-1": prose}
    )
    assert answer["sections"][0]["conclusion"] == "성립"
    assert render_native_answer(answer).endswith("### 결론\n\n성립\n")

    with pytest.raises(NativeGenerationError, match="host-owned"):
        finalize_native_answer(
            section_requests=requests,
            prose_by_issue={"issue-1": prose + "\n\n### 결론\n\n불성립"},
        )
