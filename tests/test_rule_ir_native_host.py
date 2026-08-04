from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.rulegen.native_host import (
    DEFAULT_SCLI,
    NativeHostError,
    execute_native_case,
    execute_native_unit,
    predicate_assessment_request,
)
from idpr.rulegen.registry import build_registry
from scripts.run_p2_native_scallop_golden import UnitScenarios
from scripts.run_property_scallop_golden import scenarios_for


ROOT = Path(__file__).resolve().parents[1]
FACT_GRAPH = {
    "case_id": "case-1",
    "entities": [],
    "acts": [{"source_quote": "행위"}],
    "results": [],
    "roles": [],
    "relations": [],
    "holdings": [],
    "transfers": [],
}


def _bundle(unit_id: str, scenario: dict) -> dict:
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
            "basis_fact_ids": ["fact_001"] if status == "satisfied" else [],
            "counter_fact_ids": ["fact_001"] if status == "not_satisfied" else [],
            "missing_facts": ["해당 predicate 사실 부재"] if status == "unknown" else [],
            "unknown_reason": "record_absent" if status == "unknown" else "not_applicable",
        }
    return {"version": "2.2.0", "case_id": "case-1", "assessments": assessments}


def _roles(unit_id: str, scenario: dict, **overrides: str) -> dict[str, str]:
    entry = build_registry()[unit_id]
    values = {
        argument["name"]: scenario[argument["name"]]
        for argument in entry.role_predicate["arguments"]
    }
    values.update(overrides)
    values["case_id"] = "case-1"
    return values


def test_request_loads_every_registered_predicate_and_missing_is_closed() -> None:
    case = {"sub_question_id": "case-1", "question_text": "행위", "question_prompt": ""}
    request = predicate_assessment_request(
        case=case, fact_graph=FACT_GRAPH, unit_id="rape"
    )
    assert request["all_registered_predicates_loaded"] is True
    assert len(request["issues"]) == len(build_registry()["rape"].commentary_inputs)
    assert request["role_contract"]["predicate"] == "rape_case_roles"

    missing = predicate_assessment_request(
        case=case, fact_graph=FACT_GRAPH, unit_id="criminal_procedure"
    )
    assert missing["status"] == "predicate_ir_missing"


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_host_executes_nonproperty_rule_ir_and_returns_writer_directive(tmp_path: Path) -> None:
    scenario = UnitScenarios("rape").build()[0]
    result = execute_native_unit(
        unit_id="rape",
        case_id="case-1",
        role_values=_roles("rape", scenario),
        fact_graph=FACT_GRAPH,
        assessment_payload=_bundle("rape", scenario),
        work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli"
    assert result["symbolic_conclusion"] == "established"
    assert "rape_base_established" in result["established_relations"]


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_property_outcome_bridges_into_shared_punishment_module(tmp_path: Path) -> None:
    theft_rule_ir = json.loads(
        (ROOT / "data/rulegen/property/rule_ir/theft_rule_ir_candidate.json").read_text()
    )
    theft = scenarios_for(theft_rule_ir, "theft")[0]
    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    report = execute_native_case(
        case_id="case-1",
        fact_graph=FACT_GRAPH,
        unit_runs=[
            {
                "unit_id": "theft",
                "role_values": _roles("theft", theft),
                "assessment_payload": _bundle("theft", theft),
            },
            {
                "unit_id": "relative_property_crime_exception",
                "depends_on": ["theft"],
                "role_values": _roles(
                    "relative_property_crime_exception",
                    relative,
                    predicate_offense_id="theft",
                ),
                "assessment_payload": _bundle(
                    "relative_property_crime_exception", relative
                ),
            },
        ],
        work_dir=tmp_path,
    )
    assert report["unit_results"]["theft"]["symbolic_conclusion"] == "established"
    assert report["unit_results"]["relative_property_crime_exception"][
        "symbolic_conclusion"
    ] == "established"
    contract = report["generation_contract"]
    assert contract["source"] == "scallop_derivation_only"
    assert contract["model_may_override_symbolic_conclusion"] is False


def test_shared_module_cannot_run_without_outcome_bridge(tmp_path: Path) -> None:
    relative = UnitScenarios("relative_property_crime_exception").build()[0]
    with pytest.raises(NativeHostError, match="requires depends_on bridge"):
        execute_native_case(
            case_id="case-1",
            fact_graph=FACT_GRAPH,
            unit_runs=[{
                "unit_id": "relative_property_crime_exception",
                "role_values": _roles(
                    "relative_property_crime_exception",
                    relative,
                    predicate_offense_id="theft",
                ),
                "assessment_payload": _bundle(
                    "relative_property_crime_exception", relative
                ),
            }],
            work_dir=tmp_path,
        )
