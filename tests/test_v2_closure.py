"""Step 7 Closure / Probe compiler over the production Definition Layer."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from idpr.v2.closure import ClosureError, compile_closure
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions

_PRODUCTION = Path(__file__).resolve().parents[1] / "data/v2/definitions"


def _registry() -> DefinitionRegistry:
    return load_definitions(_PRODUCTION)


def _mutate(registry: DefinitionRegistry, kind: str, entry_id: str, mutator) -> DefinitionRegistry:
    by_kind = {key: list(entries) for key, entries in registry.by_kind.items()}
    for index, entry in enumerate(by_kind[kind]):
        if entry.id == entry_id:
            payload = copy.deepcopy(dict(entry.payload))
            mutator(payload)
            by_kind[kind][index] = DefinitionEntry(entry.id, kind, payload, entry.source_file)
            break
    else:
        raise KeyError(entry_id)
    return _rebuild(by_kind)


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {key: list(entries) for key, entries in registry.by_kind.items()}
    by_kind[kind].append(DefinitionEntry(payload["id"], kind, payload, "<synthetic>"))
    return _rebuild(by_kind)


def _rebuild(by_kind: dict[str, list[DefinitionEntry]]) -> DefinitionRegistry:
    by_id = {entry.id: entry for entries in by_kind.values() for entry in entries}
    return DefinitionRegistry(by_id=by_id, by_kind={key: tuple(entries) for key, entries in by_kind.items()})


def test_seed_contract_rejects_empty_unknown_and_non_offense_refs() -> None:
    registry = _registry()
    with pytest.raises(ClosureError, match="at least one"):
        compile_closure(registry, ())
    with pytest.raises(ClosureError, match="unknown"):
        compile_closure(registry, {"offense.not_present"})
    with pytest.raises(ClosureError, match="expected offense"):
        compile_closure(registry, {"legal_element.intent"})


def test_qualify_seed_restores_base_and_qualifier_as_mandatory_structure() -> None:
    result = compile_closure(_registry(), {"derived_offense.occupational_embezzlement"})
    mandatory = {(item.definition_ref, item.source_path) for item in result.mandatory_core}

    assert ("derived_offense.occupational_embezzlement", ("seed:derived_offense.occupational_embezzlement",)) in mandatory
    assert any(ref == "offense.embezzlement" and path[-1] == "derivation.base" for ref, path in mandatory)
    assert any(ref == "qualifier.occupational_status" and path[-1] == "derivation.qualifier" for ref, path in mandatory)


def test_compose_occurrences_remain_distinct_even_for_the_same_ground_fact() -> None:
    registry = _add(_registry(), "derived_offense", {
        "id": "derived_offense.step7_duplicate_robbery",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "left"},
                {"kind": "offense", "ref": "offense.robbery", "local_key": "right"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "left", "right": "right",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    })

    result = compile_closure(registry, {"derived_offense.step7_duplicate_robbery"})
    robbery_items = [item for item in result.mandatory_core if item.definition_ref == "offense.robbery"]
    taking_facts = [
        fact for item in robbery_items for fact in item.ground_fact_frontier
        if fact.ground_fact_ref == "ground_fact.taking_conduct"
    ]

    assert {fact.occurrence_path for fact in taking_facts} == {("left",), ("right",)}
    assert len(taking_facts) == 2


def test_legal_element_is_deferred_while_its_grounded_by_fact_is_frontier() -> None:
    registry = _mutate(
        _registry(), "legal_element", "legal_element.possession",
        lambda payload: payload.__setitem__("grounded_by", ["ground_fact.taking_conduct"]),
    )
    result = compile_closure(registry, {"offense.robbery"})
    item = next(item for item in result.mandatory_core if item.definition_ref == "offense.robbery")

    assert "legal_element.possession" in item.deferred_refs
    taking_facts = [
        fact for fact in item.ground_fact_frontier
        if fact.ground_fact_ref == "ground_fact.taking_conduct"
    ]
    assert len(taking_facts) == 2  # direct conduct and possession.grounded_by are distinct paths
    assert any("grounded_by[0]" in fact.source_path for fact in taking_facts)


def test_direct_seed_uses_existing_empty_root_occurrence_path() -> None:
    result = compile_closure(_registry(), {"offense.robbery"})
    item = next(item for item in result.mandatory_core if item.definition_ref == "offense.robbery")
    assert item.occurrence_path == ()
    assert all(fact.occurrence_path == () for fact in item.ground_fact_frontier)


def test_doctrine_scope_filters_candidate_only_by_mandatory_closure() -> None:
    registry = _mutate(
        _registry(), "doctrine", "doctrine.self_defense",
        lambda payload: payload.__setitem__("offense_scope", "offense.injury"),
    )
    injury = compile_closure(registry, {"offense.injury"})
    robbery = compile_closure(registry, {"offense.robbery"})

    assert "doctrine.self_defense" in {item.definition_ref for item in injury.doctrine_probes}
    assert "doctrine.self_defense" not in {item.definition_ref for item in robbery.doctrine_probes}


def test_article_263_constraint_becomes_a_participation_probe_without_injury_result_duplication() -> None:
    result = compile_closure(_registry(), {"offense.injury"})
    item = next(
        item for item in result.participation_probes
        if item.definition_ref == "offense.injury" and item.source_path[-1] == "participation:statutory_deeming"
    )

    assert item.deferred_refs == (
        "legal_element.causal_origin_unascertained",
        "legal_element.concurrent_independent_acts",
        "legal_element.same_object_of_result",
    )
    assert "legal_element.injury_result" not in item.deferred_refs


def test_reverse_derived_branches_are_probes_not_mandatory() -> None:
    result = compile_closure(_registry(), {"offense.robbery"})
    assert "derived_offense.robbery_causing_injury_by_aggravated_result" not in {
        item.definition_ref for item in result.mandatory_core
    }
    assert "derived_offense.robbery_causing_injury_by_aggravated_result" in {
        item.definition_ref for item in result.offense_probes
    }
