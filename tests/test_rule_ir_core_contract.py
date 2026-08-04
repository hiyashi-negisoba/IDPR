from __future__ import annotations

from pathlib import Path

import pytest

from idpr.neural.core_contract import (
    assessment_groups,
    core_assessment_schema,
    core_issue_selection_schema,
    core_fact_inventory_schema,
    context_packet,
    role_binding_schema,
    validate_core_assessments,
    validate_role_binding,
    validate_core_fact_inventory,
    validate_core_issue_selection,
)
from idpr.rulegen.core_profile import load_core_profiles
from idpr.rulegen.core_runtime import execute_core_unit
from idpr.rulegen.native_host import DEFAULT_SCLI


def _profiles() -> dict:
    return load_core_profiles()["units"]


def _inventory() -> dict:
    return {
        "version": "1.0.0", "case_id": "case-1",
        "actors": [
            {"actor_id": "gap", "label": "甲", "source_quotes": ["甲은"]},
            {"actor_id": "eul", "label": "乙", "source_quotes": ["乙에게"]},
        ],
        "facts": [{
            "fact_id": "fact-1", "fact_type": "transfer",
            "focus_actor_id": "gap", "related_actor_ids": ["eul"],
            "claim": "甲이 乙에게 물건을 이전했다",
            "source_quotes": ["甲은 물건을 乙에게 주었다"],
        }],
    }


def test_fact_inventory_allows_grounded_paraphrase() -> None:
    schema = core_fact_inventory_schema(case_id="case-1")
    assert "facts" in schema["required"]
    inventory = _inventory()
    validate_core_fact_inventory(
        inventory, case_id="case-1", case_text="甲은 물건을 乙에게 주었다"
    )
    inventory["facts"][0]["source_quotes"] = ["甲이 물건을 주었다"]
    validate_core_fact_inventory(
        inventory, case_id="case-1", case_text="甲은 물건을 乙에게 주었다"
    )


def test_issue_selection_references_facts_without_reciprocal_ledger() -> None:
    inventory = _inventory()
    schema = core_issue_selection_schema(
        case_id="case-1", unit_ids=["fraud"],
        actor_ids=["gap", "eul"], fact_ids=["fact-1"],
    )
    required = schema["properties"]["issues"]["items"]["required"]
    assert {"subject_actor_id", "fact_ids"}.issubset(required)
    assert "fact_dispositions" not in schema["properties"]
    payload = {
        "version": "1.0.0", "case_id": "case-1",
        "issues": [{
            "issue_id": "i1", "unit_id": "unsupported",
            "reported_label": "피해자 승낙의 착오",
            "subject_actor_id": "gap", "fact_ids": ["fact-1"],
        }],
    }
    validate_core_issue_selection(
        payload, case_id="case-1", unit_ids=["fraud"], inventory=inventory
    )
def test_role_binding_is_conditioned_on_the_selected_unit_contract() -> None:
    fraud = _profiles()["fraud"]
    schema = role_binding_schema(case_id="case-1", issue_id="issue-1", profile=fraud)
    required = schema["properties"]["role_bindings"]["required"]
    assert required == [
        "defendant_id", "deceived_person_id", "disposer_id",
        "property_owner_id", "beneficiary_id",
    ]
    assert schema["properties"]["track_selections"]["items"]["properties"][
        "track_id"
    ]["enum"] == ["base"]
    assert schema["properties"]["track_selections"]["items"]["required"] == [
        "track_id", "reason",
    ]
    assert schema["properties"]["relations"]["maxItems"] == 16


def test_role_binding_accepts_normalized_labels_and_paraphrased_evidence() -> None:
    theft = _profiles()["theft"]
    text = "甲은 C의 지갑에서 수표를 꺼내 가져갔다."
    subject = {"label": "甲", "source_quotes": ["甲은"]}
    payload = {
        "version": "1.0.0", "case_id": "case-1", "issue_id": "issue-1",
        "unit_id": "theft",
        "track_selections": [{
            "track_id": "base", "reason": "취거 행위",
        }],
        "entities": [
            {"entity_id": "defendant", "label": "甲", "source_quotes": ["甲"]},
            {"entity_id": "owner", "label": "C", "source_quotes": ["C"]},
            {"entity_id": "possessor", "label": "C", "source_quotes": ["C"]},
        ],
        "role_bindings": {
            "defendant_id": {"entity_id": "defendant", "source_quotes": ["甲은"], "reason": "행위자"},
            "owner_id": {"entity_id": "owner", "source_quotes": ["C"], "reason": "소유자"},
            "possessor_id": {"entity_id": "possessor", "source_quotes": ["C"], "reason": "점유자"},
        },
        "relations": [],
    }
    validate_role_binding(
        payload, case_text=text, case_id="case-1", issue_id="issue-1",
        profile=theft, subject=subject,
    )


def test_role_binding_allows_cross_stage_entity_aliases() -> None:
    fraud = _profiles()["fraud"]
    text = "乙은 B에게 거짓말하여 B가 乙에게 돈을 주었다."
    payload = {
        "version": "1.0.0", "case_id": "case-1", "issue_id": "issue-1",
        "unit_id": "fraud", "track_selections": [{
            "track_id": "base", "reason": "乙의 기망행위",
        }],
        "entities": [
            {"entity_id": "eul", "label": "乙", "source_quotes": ["乙"]},
            {"entity_id": "b", "label": "B", "source_quotes": ["B"]},
        ],
        "role_bindings": {
            "defendant_id": {"entity_id": "eul", "source_quotes": ["乙은"], "reason": "행위자"},
            "deceived_person_id": {"entity_id": "b", "source_quotes": ["B에게"], "reason": "기망 상대방"},
            "disposer_id": {"entity_id": "b", "source_quotes": ["B가 乙에게 돈을 주었다"], "reason": "교부자"},
            "property_owner_id": {"entity_id": "b", "source_quotes": ["B가 乙에게 돈을 주었다"], "reason": "재산권자"},
            "beneficiary_id": {"entity_id": "eul", "source_quotes": ["乙에게 돈을 주었다"], "reason": "수익자"},
        },
        "relations": [{
            "relation_id": "r1", "subject_id": "b", "relation": "금전교부",
            "object_id": "eul", "source_quote": "B가 乙에게 돈을 주었다",
        }],
    }
    validate_role_binding(
        payload, case_text=text, case_id="case-1", issue_id="issue-1", profile=fraud,
        subject={"label": "乙", "source_quotes": ["乙은"]},
    )
    payload["role_bindings"]["disposer_id"]["entity_id"] = "ghost"
    validate_role_binding(
        payload, case_text=text, case_id="case-1", issue_id="issue-1", profile=fraud,
        subject={"label": "乙", "source_quotes": ["乙은"]},
    )


def test_assessment_allows_reason_only_status() -> None:
    theft = _profiles()["theft"]
    predicate_id = theft["model_input_predicates"][0]["predicate_id"]
    schema = core_assessment_schema(
        case_id="case-1", predicate_ids=[predicate_id]
    )
    payload = {
        "version": "1.0.0", "case_id": "case-1",
        "assessments": {
            predicate_id: {"status": "not_satisfied", "reason": "사실상 요건이 없다"}
        },
    }
    assert schema["properties"]["assessments"]["additionalProperties"] is False
    validate_core_assessments(
        payload, case_id="case-1", predicate_ids=[predicate_id], case_text="사례 사실",
    )


def test_assessment_is_grouped_and_context_cannot_change_predicates() -> None:
    homicide = _profiles()["homicide"]
    groups = assessment_groups(homicide, ["base"], max_predicates=8)
    ids = [item["predicate_id"] for group in groups for item in group["predicates"]]
    assert len(groups) == 2
    assert len(ids) == 14
    assert len(ids) == len(set(ids))
    packet = context_packet(homicide, ids[:2])
    assert packet["predicate_set_mutable"] is False
    assert packet["external_search_used"] is False
    assert set(packet["items"]) == set(ids[:2])


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_core_projection_reaches_a_real_scallop_derivation(tmp_path: Path) -> None:
    theft = _profiles()["theft"]
    assessments = {
        item["predicate_id"]: {"status": "satisfied"}
        for item in theft["model_input_predicates"]
    }
    result = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"],
        assessments=assessments,
        work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli_core_projection"
    assert result["track_outcomes"]["base"]["symbolic_conclusion"] == "established"
    assert result["query_results"]["theft_established"] is True

    first = next(iter(assessments))
    assessments[first] = {"status": "not_satisfied"}
    negative = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "negative",
    )
    assert negative["track_outcomes"]["base"]["symbolic_conclusion"] == "not_established"

    assessments[first] = {"status": "unknown"}
    unknown = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "unknown",
    )
    assert unknown["track_outcomes"]["base"]["symbolic_conclusion"] == "undetermined"
