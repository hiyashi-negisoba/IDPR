"""Step 8 Call 1 closed seed-router and calibration contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.call1_pilot import (
    article_definition_refs,
    case_calibration,
    case_definition_calibration,
    summarize_calibrations,
    summarize_definition_calibrations,
)
from idpr.v2.registry import load_definitions
from idpr.v2.routing import (
    MAX_SEEDS_PER_CASE,
    RouterContractError,
    normalize_router_seeds,
    router_catalog,
    router_request_payload,
    router_schema,
    validate_router_output,
)


_PRODUCTION = Path(__file__).resolve().parents[1] / "data/v2/definitions"
_PILOT_CASE_LIST = Path(__file__).resolve().parents[1] / "data/eval/kcl_substantive_case_ids.txt"


def _registry():
    return load_definitions(_PRODUCTION)


def _catalog():
    return router_catalog(_registry())


def test_pilot_case_list_is_an_exact_unique_26_case_cohort() -> None:
    case_ids = tuple(
        line.strip()
        for line in _PILOT_CASE_LIST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    assert len(case_ids) == 26
    assert len(set(case_ids)) == len(case_ids)


def test_catalog_is_closed_to_production_offense_kinds_and_never_invents_derived_identity() -> None:
    catalog = _catalog()
    assert len(catalog) == 63
    assert {entry.kind for entry in catalog} == {"offense", "derived_offense"}
    assert [entry.definition_id for entry in catalog] == sorted(
        entry.definition_id for entry in catalog
    )
    offense = next(entry for entry in catalog if entry.definition_id == "offense.injury")
    derived = next(
        entry for entry in catalog if entry.definition_id == "derived_offense.special_injury"
    )
    assert offense.display_name == "상해죄"
    assert offense.statutory_refs == ("형법 제257조 제1항",)
    assert derived.display_name == derived.definition_id
    assert derived.statutory_refs == ()


def test_schema_has_closed_enum_unique_items_and_pilot_budget() -> None:
    catalog = _catalog()
    seeds = router_schema(catalog)["properties"]["seeds"]
    assert seeds["uniqueItems"] is True
    assert seeds["minItems"] == 1
    assert MAX_SEEDS_PER_CASE == 10
    assert seeds["maxItems"] == MAX_SEEDS_PER_CASE
    assert set(seeds["items"]["enum"]) == {entry.definition_id for entry in catalog}


def test_request_contains_only_case_text_and_closed_catalog() -> None:
    payload = router_request_payload(case_text="甲은 …", catalog=_catalog())
    assert set(payload) == {"case_text", "offense_catalog"}
    assert payload["case_text"] == "甲은 …"
    assert set(payload["offense_catalog"][0]) == {
        "definition_id", "kind", "display_name", "statutory_refs"
    }


def test_raw_validation_preserves_duplicates_then_explicit_normalization_keeps_first_rank() -> None:
    catalog = _catalog()
    assert validate_router_output(
        {"seeds": ["offense.robbery", "offense.injury"]}, catalog=catalog
    ) == ("offense.robbery", "offense.injury")
    raw = validate_router_output(
        {"seeds": ["offense.robbery", "offense.injury", "offense.robbery"]}, catalog=catalog
    )
    normalization = normalize_router_seeds(raw)
    assert normalization.raw_seeds == raw
    assert normalization.normalized_seeds == ("offense.robbery", "offense.injury")
    assert normalization.duplicate_refs == ("offense.robbery",)
    assert normalization.normalization_applied is True


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"seeds": []},
        {"seeds": ["legal_element.intent"]},
        {"seeds": ["offense.not_present"]},
        {"seeds": ["offense.robbery"], "actor": "갑"},
        {"seeds": ["offense.robbery"] * (MAX_SEEDS_PER_CASE + 1)},
    ],
)
def test_validator_rejects_contract_violations(payload) -> None:
    with pytest.raises(RouterContractError):
        validate_router_output(payload, catalog=_catalog())


def test_article_projection_uses_authored_statutory_identity_and_keeps_same_article_refs() -> None:
    mapped = article_definition_refs(
        _registry(),
        [
            {"key": "art257", "label": "제257조"},
            {"key": "art328", "label": "제328조"},
        ],
    )
    assert mapped["art257"] == ("offense.ancestral_injury", "offense.injury")
    assert mapped["art328"] == ()


def test_calibration_uses_any_mapped_ref_and_ordered_prefix_without_padding() -> None:
    registry = _registry()
    seeds = (
        "offense.theft", "offense.robbery", "offense.embezzlement", "offense.property_damage",
        "offense.lost_property_embezzlement", "offense.extortion", "offense.dereliction_of_duty",
        "offense.official_secret_disclosure", "offense.bribery_taking", "offense.perjury",
        "offense.injury",
    )
    result = case_calibration(
        registry,
        seeds=seeds,
        gold_articles=("art257", "art328"),
        mapped_refs_by_article={
            "art257": ("offense.injury", "offense.ancestral_injury"),
            "art328": (),
        },
    )
    article = next(row for row in result["gold_articles"] if row["article"] == "art257")
    assert article["raw_success"] is True
    assert article["closure_success"] is True
    assert article["prefix10_closure_success"] is False
    assert article["additional_recovery"] is True
    assert result["prefix10"] == list(seeds[:10])
    assert result["full15"] == list(seeds)
    out_of_registry = next(row for row in result["gold_articles"] if row["article"] == "art328")
    assert out_of_registry["status"] == "out_of_registry"


def test_summary_separates_out_of_registry_and_additional_recovery() -> None:
    summary = summarize_calibrations([{
        "seeds": ["offense.injury"],
        "closure": {"ground_fact_frontier_count": 3, "probe_count": 2},
        "calibration": {
            "gold_articles": [
                {"status": "survives", "raw_success": True, "closure_success": True,
                 "additional_recovery": False},
                {"status": "out_of_registry"},
            ]
        },
    }])
    assert summary["mapped_articles"] == 1
    assert summary["out_of_registry_articles"] == 1
    assert summary["raw_survival_rate"] == 1.0
    assert summary["closure_survival_rate"] == 1.0
    assert summary["raw_seed_count"]["mean"] == 1.0


def test_definition_calibration_uses_approved_refs_and_ordered_prefix() -> None:
    registry = _registry()
    seeds = (
        "offense.theft", "offense.robbery", "offense.embezzlement", "offense.property_damage",
        "offense.lost_property_embezzlement", "offense.extortion", "offense.dereliction_of_duty",
        "offense.official_secret_disclosure", "offense.bribery_taking", "offense.perjury",
        "offense.injury",
    )
    result = case_definition_calibration(
        registry,
        seeds=seeds,
        gold_definition_refs=("offense.injury",),
    )
    gold = result["gold_definition_refs"][0]
    assert gold["raw_success"] is True
    assert gold["closure_success"] is True
    assert gold["prefix10_closure_success"] is False
    assert gold["additional_recovery"] is True
    assert result["prefix10"] == list(seeds[:10])
    assert result["full15"] == list(seeds)


def test_definition_summary_keeps_explicit_out_of_scope_cases_out_of_denominator() -> None:
    summary = summarize_definition_calibrations([
        {
            "seeds": ["offense.injury"],
            "closure": {"ground_fact_frontier_count": 3, "probe_count": 2},
            "gold": {"gold_definition_refs": ["offense.injury"]},
            "calibration": {"gold_definition_refs": [{
                "raw_success": True,
                "closure_success": True,
                "additional_recovery": False,
            }]},
        },
        {"seeds": ["offense.theft"], "gold": {"gold_definition_refs": []}},
    ])
    assert summary["in_scope_gold_definition_refs"] == 1
    assert summary["out_of_scope_cases"] == 1
    assert summary["raw_survival_rate"] == 1.0
    assert summary["closure_survival_rate"] == 1.0
