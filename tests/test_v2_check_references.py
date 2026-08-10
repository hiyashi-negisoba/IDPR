from __future__ import annotations

import copy

from idpr.v2.checks.references import check_references
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


def _mutate(registry: DefinitionRegistry, kind: str, entry_id: str, mutator) -> DefinitionRegistry:
    """A real-corpus registry with one entry's payload deep-copied and mutated in place."""
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    for index, entry in enumerate(by_kind[kind]):
        if entry.id == entry_id:
            payload = copy.deepcopy(dict(entry.payload))
            mutator(payload)
            by_kind[kind][index] = DefinitionEntry(
                id=payload.get("id", entry.id), kind=kind, payload=payload, source_file=entry.source_file,
            )
            break
    else:
        raise KeyError(entry_id)
    by_id = {}
    frozen_by_kind = {}
    for k, entries in by_kind.items():
        frozen_by_kind[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def _codes(findings) -> set[str]:
    return {finding.code for finding in findings}


def test_real_corpus_has_no_reference_findings() -> None:
    assert check_references(load_definitions()) == []


def test_dangling_ref_reported() -> None:
    registry = _mutate(
        load_definitions(), "offense", "offense.robbery",
        lambda p: p["elements"].__setitem__("mental", {"op": "ref", "ref": "ground_fact.nonexistent"}),
    )
    findings = check_references(registry)
    assert "missing_reference" in _codes(findings)


def test_wrong_kind_ref_reported_as_kind_mismatch_not_missing() -> None:
    registry = _mutate(
        load_definitions(), "offense", "offense.robbery",
        lambda p: p["elements"].__setitem__("mental", {"op": "ref", "ref": "offense.injury"}),
    )
    findings = check_references(registry)
    assert _codes(findings) == {"kind_mismatch"}


def test_qualify_base_pointing_at_derived_offense_is_kind_mismatch() -> None:
    registry = _mutate(
        load_definitions(), "derived_offense", "derived_offense.occupational_embezzlement",
        lambda p: p["derivation"].__setitem__("base", "derived_offense.robbery_rape"),
    )
    findings = [f for f in check_references(registry) if f.field_path == "derivation.base"]
    assert len(findings) == 1
    assert findings[0].code == "kind_mismatch"


def test_compose_offense_tagged_component_pointing_at_ground_fact_is_kind_mismatch() -> None:
    def mutate(payload):
        payload["derivation"]["components"][0]["ref"] = "ground_fact.property_taking"

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_references(registry)
    assert "kind_mismatch" in _codes(findings)


def test_primitive_ref_kind_mismatch() -> None:
    registry = _mutate(
        load_definitions(), "primitive", "primitive.aggravated_result_attribution",
        lambda p: p.__setitem__("ref", "ground_fact.injury_occurred"),
        # ref_kind stays 'legal_element' but ref now points to a ground_fact
    )
    findings = check_references(registry)
    assert _codes(findings) == {"kind_mismatch"}


def test_exported_component_source_offense_pointing_at_derived_offense_is_kind_mismatch() -> None:
    registry = _mutate(
        load_definitions(), "exported_component", "exported_component.injury_result",
        lambda p: p.__setitem__("source_offense", "derived_offense.robbery_rape"),
    )
    findings = check_references(registry)
    assert _codes(findings) == {"kind_mismatch"}


def test_duplicate_local_key_reported() -> None:
    def mutate(payload):
        payload["derivation"]["components"][1]["local_key"] = payload["derivation"]["components"][0]["local_key"]

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_references(registry)
    assert "duplicate_local_key" in _codes(findings)


def test_relation_binding_unresolved_local_key_reported() -> None:
    def mutate(payload):
        payload["derivation"]["relations"][0]["left"] = "nonexistent_local_key"

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_references(registry)
    assert "unresolved_local_key" in _codes(findings)


def test_relation_binding_self_loop_reported() -> None:
    def mutate(payload):
        right = payload["derivation"]["relations"][0]["right"]
        payload["derivation"]["relations"][0]["left"] = right

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_references(registry)
    assert "relation_binding_self_loop" in _codes(findings)


def test_compose_bundle_placement_key_mismatch_reported() -> None:
    def mutate(payload):
        payload["derivation"]["components"].append({
            "kind": "bundle",
            "ref": "bundle.robbery_conduct_bundle",
            "local_key": "conduct_bundle",
            "placement": {"ground_fact.property_taking": "conduct"},  # missing the bundle's 2nd leaf
        })
        payload["derivation"]["relations"].append({
            "relation": "relation.occasion_identity",
            "left": "robbery_part",
            "right": "conduct_bundle",
        })

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_references(registry)
    assert "placement_missing_leaves" in _codes(findings)


def test_element_modules_placement_key_mismatch_reported() -> None:
    def mutate(payload):
        payload["element_modules"] = [{
            "ref": "bundle.robbery_conduct_bundle",
            "placement": {
                "ground_fact.property_taking": "conduct",
                "legal_element.robbery_level_violence": "conduct",
                "ground_fact.injury_occurred": "result",  # not one of this bundle's own leaves
            },
        }]

    registry = _mutate(load_definitions(), "offense", "offense.robbery", mutate)
    findings = check_references(registry)
    assert "placement_extra_leaves" in _codes(findings)


def test_one_of_duplicate_branch_reported() -> None:
    def mutate(payload):
        payload["elements"]["mental"] = {
            "op": "one_of",
            "args": [
                {"op": "ref", "ref": "legal_element.appropriation_intent"},
                {"op": "ref", "ref": "legal_element.appropriation_intent"},
            ],
        }

    registry = _mutate(load_definitions(), "offense", "offense.robbery", mutate)
    findings = check_references(registry)
    assert "duplicate_one_of_branch" in _codes(findings)


def test_doctrine_offense_scope_requires_an_offense_family_ref() -> None:
    registry = _mutate(
        load_definitions(), "doctrine", "doctrine.self_defense",
        lambda p: p.__setitem__("offense_scope", "ground_fact.property_taking"),
    )
    findings = [f for f in check_references(registry) if f.field_path == "offense_scope"]
    assert len(findings) == 1
    assert findings[0].code == "kind_mismatch"


def test_statutory_deeming_requires_an_expression_with_predicate_refs() -> None:
    registry = _mutate(
        load_definitions(), "offense", "offense.injury",
        lambda p: p.__setitem__("participation_constraints", {
            "statutory_deeming": {"requires": {"op": "ref", "ref": "offense.robbery"}},
        }),
    )
    findings = check_references(registry)
    assert "kind_mismatch" in _codes(findings)
