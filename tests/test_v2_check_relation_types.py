"""build-order step 5 -- idpr.v2.checks.relation_types: relation lowering (axis 7)."""

from __future__ import annotations

import copy

from idpr.v2.checks.relation_types import check_relation_types
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


def _rebuild(by_kind: dict) -> DefinitionRegistry:
    by_id = {}
    frozen_by_kind = {}
    for kind, entries in by_kind.items():
        frozen_by_kind[kind] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def _mutate(registry: DefinitionRegistry, kind: str, entry_id: str, mutator) -> DefinitionRegistry:
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
    return _rebuild(by_kind)


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, [])
    by_kind[kind].append(DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>"))
    return _rebuild(by_kind)


def _codes(findings, object_id):
    return {f.code for f in findings if f.object_id == object_id}


def test_real_corpus_has_no_relation_type_findings() -> None:
    assert check_relation_types(load_definitions()) == []


def test_same_offense_is_a_conduct_endpoint_in_one_relation_and_an_event_endpoint_in_another() -> None:
    """The fixture pair that rules out an intrinsic per-definition semantic type: offense.robbery
    passes lowering as a `conduct` endpoint of occasion_identity AND as an `event` endpoint of
    causal_nexus. A single fixed type on OffenseDef would have to fail one of these."""
    registry = load_definitions()
    assert check_relation_types(registry) == []

    rape = registry.get("derived_offense.robbery_rape").payload["derivation"]["relations"][0]
    injury = registry.get("derived_offense.robbery_causing_injury").payload["derivation"]["relations"][0]
    assert rape["left"] == "robbery_part" and rape["left_view"] == "conduct"
    assert injury["left"] == "base_robbery" and injury["left_view"] == "event"


def test_view_not_matching_relation_declared_type_is_reported() -> None:
    def mutate(payload):
        payload["derivation"]["relations"][0]["right_view"] = "conduct"  # causal_nexus is event x event

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_causing_injury", mutate)
    findings = check_relation_types(registry)
    assert "relation_view_type_mismatch" in _codes(findings, "derived_offense.robbery_causing_injury")


def test_both_endpoints_are_checked_independently() -> None:
    """One good side never excuses the other -- two mismatches produce two findings."""
    def mutate(payload):
        binding = payload["derivation"]["relations"][0]
        binding["left_view"] = "actor"
        binding["right_view"] = "actor"

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = [
        f for f in check_relation_types(registry)
        if f.object_id == "derived_offense.robbery_rape" and f.code == "relation_view_type_mismatch"
    ]
    assert {f.field_path for f in findings} == {
        "derivation.relations[0].left_view",
        "derivation.relations[0].right_view",
    }


def test_offense_endpoint_cannot_be_viewed_through_an_unsupported_aspect() -> None:
    """Obligation B, structured side: even when the view agrees with the RelationDef (so
    obligation A passes), an offense can only be projected through the aspects it actually has."""
    registry = load_definitions()

    def mutate_relation(payload):
        payload["left_type"] = "actor"
        payload["right_type"] = "actor"

    def mutate_offense(payload):
        binding = payload["derivation"]["relations"][0]
        binding["left_view"] = "actor"
        binding["right_view"] = "actor"

    registry = _mutate(registry, "relation", "relation.occasion_identity", mutate_relation)
    registry = _mutate(registry, "derived_offense", "derived_offense.robbery_rape", mutate_offense)

    findings = check_relation_types(registry)
    codes = _codes(findings, "derived_offense.robbery_rape")
    assert "relation_view_unsupported_by_component_kind" in codes
    assert "relation_view_type_mismatch" not in codes  # A passes, B is what fails


def test_atomic_endpoint_view_must_equal_its_declared_semantic_sort() -> None:
    """Obligation B, atomic side: an exported_component resolves to ground_fact.injury_occurred,
    whose semantic_sort is `event`, so viewing it as anything else is rejected."""
    registry = load_definitions()

    def mutate_relation(payload):
        payload["right_type"] = "conduct"

    def mutate_offense(payload):
        payload["derivation"]["relations"][0]["right_view"] = "conduct"

    registry = _mutate(registry, "relation", "relation.causal_nexus", mutate_relation)
    registry = _mutate(registry, "derived_offense", "derived_offense.robbery_causing_injury", mutate_offense)

    findings = check_relation_types(registry)
    codes = _codes(findings, "derived_offense.robbery_causing_injury")
    assert "relation_view_unsupported_by_component_kind" in codes
    assert "relation_view_type_mismatch" not in codes


def test_atomic_endpoint_without_semantic_sort_is_untyped_not_silently_accepted() -> None:
    """The permissive-baseline trap this axis was corrected to avoid: an endpoint with no declared
    typing must be REPORTED, never treated as compatible with whatever view was authored."""
    def mutate(payload):
        payload.pop("semantic_sort")

    registry = _mutate(load_definitions(), "ground_fact", "ground_fact.injury_occurred", mutate)
    findings = check_relation_types(registry)
    assert "relation_endpoint_untyped" in _codes(findings, "derived_offense.robbery_causing_injury")


def test_bundle_endpoint_is_always_unsupported_at_this_baseline() -> None:
    """Complements tests/test_v2_compile.py's
    test_bundle_as_relation_endpoint_compiles_without_type_validation: step 4 still PRESERVES the
    bundle endpoint in the IR (that test is untouched); this axis is where it is rejected, because
    a bundle is a tree of predicates with no single endpoint sort to project."""
    synthetic = {
        "id": "derived_offense.synthetic_bundle_relation_endpoint",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.injury", "local_key": "base"},
                {
                    "kind": "bundle",
                    "ref": "bundle.robbery_conduct_bundle",
                    "local_key": "conduct_bundle",
                    "placement": {
                        "ground_fact.property_taking": "conduct",
                        "legal_element.robbery_level_violence": "conduct",
                    },
                },
            ],
            "relations": [{
                "relation": "relation.causal_nexus", "left": "base", "right": "conduct_bundle",
                "left_view": "event", "right_view": "event",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    findings = check_relation_types(registry)
    bundle_findings = [
        f for f in findings
        if f.object_id == "derived_offense.synthetic_bundle_relation_endpoint"
        and f.code == "relation_endpoint_untyped"
    ]
    assert [f.field_path for f in bundle_findings] == ["derivation.relations[0].right_view"]


def test_compile_failure_is_skipped_not_re_reported() -> None:
    """Compile diagnostics belong to axes 2/6. Forwarding them here would double every one of them
    in run_type_checks() output."""
    synthetic = {
        "id": "derived_offense.synthetic_broken_component",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "a"},
                {"kind": "primitive", "ref": "primitive.does_not_exist", "local_key": "broken", "slot": "result"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "a", "right": "broken",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    findings = check_relation_types(registry)  # must not raise
    assert _codes(findings, "derived_offense.synthetic_broken_component") == set()


def test_cyclic_derivation_terminates_without_findings() -> None:
    a = {
        "id": "derived_offense.synthetic_rel_cycle_a",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_rel_cycle_b", "local_key": "b"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "base", "right": "b",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    b = copy.deepcopy(a)
    b["id"] = "derived_offense.synthetic_rel_cycle_b"
    b["derivation"]["components"][1] = {
        "kind": "offense", "ref": "derived_offense.synthetic_rel_cycle_a", "local_key": "a",
    }
    b["derivation"]["relations"][0]["right"] = "a"

    registry = _add(_add(load_definitions(), "derived_offense", a), "derived_offense", b)
    findings = check_relation_types(registry)  # must terminate, not RecursionError
    assert _codes(findings, "derived_offense.synthetic_rel_cycle_a") == set()
