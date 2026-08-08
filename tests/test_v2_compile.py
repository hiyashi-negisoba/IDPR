"""build-order step 4 -- idpr.v2.compile: QUALIFY / COMPOSE compiler."""

from __future__ import annotations

import copy

from idpr.v2 import compile as compilemod
from idpr.v2 import expressions
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


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


def _rebuild(by_kind: dict) -> DefinitionRegistry:
    by_id = {}
    frozen_by_kind = {}
    for kind, entries in by_kind.items():
        frozen_by_kind[kind] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def test_plain_offense_compiles_to_slots_only() -> None:
    registry = load_definitions()
    compiled = compilemod.compile_offense(registry, "offense.robbery")
    assert isinstance(compiled, compilemod.CompiledOffense)
    assert compiled.components == ()
    assert compiled.relations == ()
    elements = registry.get("offense.robbery").payload.get("elements") or {}
    for slot in expressions.SLOT_NAMES:
        assert compiled.slots.get(slot) == expressions.canonicalize(elements.get(slot))


def test_qualify_matches_stored_flattened_elements() -> None:
    registry = load_definitions()
    compiled = compilemod.compile_offense(registry, "derived_offense.occupational_embezzlement")
    assert compiled.components == ()
    assert compiled.relations == ()
    flattened = registry.get("derived_offense.occupational_embezzlement").payload["flattened_elements"]
    for slot in expressions.SLOT_NAMES:
        assert compiled.slots.get(slot) == expressions.canonicalize(flattened.get(slot))


def test_compose_offense_primitive_exported_component() -> None:
    registry = load_definitions()
    compiled = compilemod.compile_offense(registry, "derived_offense.robbery_causing_injury")
    flattened = registry.get("derived_offense.robbery_causing_injury").payload["flattened_elements"]
    for slot in expressions.SLOT_NAMES:
        assert compiled.slots.get(slot) == expressions.canonicalize(flattened.get(slot))

    by_local_key = {inst.local_key: inst for inst in compiled.components}
    assert set(by_local_key) == {"base_robbery", "result_attribution", "aggravated_result"}
    assert by_local_key["base_robbery"].component_kind == "offense"
    assert by_local_key["base_robbery"].resolved_kind == "offense"
    assert isinstance(by_local_key["base_robbery"].compiled_content, compilemod.CompiledOffense)
    assert by_local_key["result_attribution"].component_kind == "primitive"
    assert by_local_key["result_attribution"].resolved_kind == "primitive"
    assert by_local_key["result_attribution"].compiled_content == ("ref", "legal_element.aggravated_result_attribution")
    assert by_local_key["aggravated_result"].component_kind == "exported_component"
    assert by_local_key["aggravated_result"].resolved_kind == "exported_component"
    assert by_local_key["aggravated_result"].compiled_content == ("ref", "ground_fact.injury_occurred")

    assert len(compiled.relations) == 1
    binding = compiled.relations[0]
    assert binding.relation_ref == "relation.causal_nexus"
    assert binding.left is by_local_key["base_robbery"]
    assert binding.right is by_local_key["aggravated_result"]

    # 3rd correction (semantic clarification): CompiledOffense = Slots + Required Relation
    # Bindings, never Slots alone -- relations must not be silently empty/ignored here.
    assert compiled.relations != ()


def test_compose_two_full_offenses() -> None:
    registry = load_definitions()
    compiled = compilemod.compile_offense(registry, "derived_offense.robbery_rape")
    by_local_key = {inst.local_key: inst for inst in compiled.components}
    assert set(by_local_key) == {"robbery_part", "rape_part"}
    for instance in by_local_key.values():
        assert instance.component_kind == "offense"
        assert instance.resolved_kind == "offense"
        assert isinstance(instance.compiled_content, compilemod.CompiledOffense)
    assert len(compiled.relations) == 1
    binding = compiled.relations[0]
    assert binding.relation_ref == "relation.occasion_identity"
    assert binding.left is by_local_key["robbery_part"]
    assert binding.right is by_local_key["rape_part"]


def test_component_kind_vs_resolved_kind_and_nested_compose_not_flattened() -> None:
    """2nd correction: component_kind (authored category) and resolved_kind (what the ref
    actually is) must not be conflated -- an offense-kind component may resolve to either a
    plain OffenseDef or a DerivedOffenseDef. Also covers nested COMPOSE: the inner
    DerivedOffenseDef's own components/relations must stay inside its nested CompiledOffense,
    not get merged into the outer's."""
    outer = {
        "id": "derived_offense.synthetic_outer_of_derived",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "inner"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "other"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "inner", "right": "other", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", outer)
    compiled = compilemod.compile_offense(registry, "derived_offense.synthetic_outer_of_derived")
    assert isinstance(compiled, compilemod.CompiledOffense)

    by_local_key = {inst.local_key: inst for inst in compiled.components}
    assert by_local_key["inner"].component_kind == "offense"
    assert by_local_key["inner"].resolved_kind == "derived_offense"
    assert by_local_key["other"].component_kind == "offense"
    assert by_local_key["other"].resolved_kind == "offense"

    nested = by_local_key["inner"].compiled_content
    assert isinstance(nested, compilemod.CompiledOffense)
    assert nested.id == "derived_offense.robbery_causing_injury"
    assert len(nested.relations) == 1  # the inner's own relation (base_robbery <-> aggravated_result)
    assert len(nested.components) == 3  # the inner's own components, not flattened up
    assert len(compiled.relations) == 1  # only the outer's own relation (inner <-> other)


def test_duplicate_ref_different_local_keys_stay_distinct_instances() -> None:
    """Core corrected design point: local_key identifies a component *occurrence*, so the same
    ref appearing twice under different local_keys must produce two distinct
    CompiledComponentInstance objects, and a relation binding them must not collapse to a single
    global-ref identity."""
    synthetic = {
        "id": "derived_offense.synthetic_duplicate_ref",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "left_x"},
                {"kind": "offense", "ref": "offense.robbery", "local_key": "right_x"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "left_x", "right": "right_x", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    compiled = compilemod.compile_offense(registry, "derived_offense.synthetic_duplicate_ref")
    assert isinstance(compiled, compilemod.CompiledOffense)
    assert len(compiled.components) == 2
    left_instance = next(c for c in compiled.components if c.local_key == "left_x")
    right_instance = next(c for c in compiled.components if c.local_key == "right_x")
    assert left_instance is not right_instance
    assert left_instance.source_ref == right_instance.source_ref == "offense.robbery"
    binding = compiled.relations[0]
    assert binding.left is left_instance
    assert binding.right is right_instance


def test_bundle_as_relation_endpoint_compiles_without_type_validation() -> None:
    """1st correction (3-layer split): the compiler does not reject a bundle-kind relation
    endpoint -- it preserves the occurrence. Whether relation.causal_nexus's left_type/right_type
    is actually compatible with a bundle endpoint is Step 5's job (relation lowering), not
    checked here."""
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
            "relations": [{"relation": "relation.causal_nexus", "left": "base", "right": "conduct_bundle", "left_view": "event", "right_view": "event"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    compiled = compilemod.compile_offense(registry, "derived_offense.synthetic_bundle_relation_endpoint")
    assert isinstance(compiled, compilemod.CompiledOffense)  # no rejection at this layer

    bundle_instance = next(c for c in compiled.components if c.local_key == "conduct_bundle")
    assert bundle_instance.component_kind == "bundle"
    assert bundle_instance.resolved_kind == "element_bundle"
    assert bundle_instance.compiled_content == expressions.canonicalize(
        registry.get("bundle.robbery_conduct_bundle").payload["requires"]
    )
    assert compiled.relations[0].right is bundle_instance


def test_malformed_relation_binding_returns_findings_not_raise() -> None:
    synthetic = {
        "id": "derived_offense.synthetic_bad_relation_local_key",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "other"},
            ],
            "relations": [{"relation": "relation.causal_nexus", "left": "base", "right": "typo_local_key", "left_view": "event", "right_view": "event"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_bad_relation_local_key")
    assert isinstance(result, list)
    assert any(finding.code == "relation_binding_unresolved_local_key" for finding in result)


def test_relation_binding_missing_view_returns_findings_not_raise() -> None:
    """Step 5 addendum, same defensive posture as the checks above: left_view/right_view are
    schema-required, so authored YAML always has them -- but compile_offense() is callable
    standalone, and a missing view must produce a Finding (invalidating the whole entry) rather
    than a KeyError."""
    synthetic = {
        "id": "derived_offense.synthetic_missing_view",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "a"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "a", "right": "b"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_missing_view")
    assert isinstance(result, list)
    assert any(finding.code == "relation_binding_missing_view" for finding in result)

    def add_only_left(payload):
        payload["derivation"]["relations"][0]["left_view"] = "conduct"

    registry = _mutate(registry, "derived_offense", "derived_offense.synthetic_missing_view", add_only_left)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_missing_view")
    assert isinstance(result, list)  # one side present is still not enough
    assert any(finding.code == "relation_binding_missing_view" for finding in result)


def test_relation_binding_views_are_carried_through_verbatim() -> None:
    """The compiler passes views through without judging them -- deciding whether `event` is
    right for this endpoint is axis 7's job (tests/test_v2_check_relation_types.py)."""
    registry = load_definitions()
    compiled = compilemod.compile_offense(registry, "derived_offense.robbery_causing_injury")
    binding = compiled.relations[0]
    assert (binding.left_view, binding.right_view) == ("event", "event")


def test_one_broken_component_fails_the_whole_entry_never_a_partial_compiled_offense() -> None:
    synthetic = {
        "id": "derived_offense.synthetic_partial_break",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "good_one"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "good_two"},
                {"kind": "primitive", "ref": "primitive.does_not_exist", "local_key": "broken", "slot": "result"},
            ],
            "relations": [],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_partial_break")
    assert isinstance(result, list)  # never a CompiledOffense with the broken component silently dropped
    assert any(finding.code == "component_unresolved" for finding in result)


def test_duplicate_local_key_is_rejected_not_silently_overwritten() -> None:
    """4th correction, defensive check #1: compile_offense() builds a {local_key: instance} map
    and must not silently let a second occurrence overwrite the first, even when called without
    axis 1 (Type checker) having already rejected the duplicate."""
    synthetic = {
        "id": "derived_offense.synthetic_duplicate_local_key",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "dup"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "dup"},
            ],
            "relations": [],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_duplicate_local_key")
    assert isinstance(result, list)
    assert any(finding.code == "duplicate_local_key" for finding in result)


def test_relation_ref_must_resolve_to_a_relation() -> None:
    """4th correction, defensive check #2: relation_ref is confirmed to exist and resolve to a
    RelationDef before a CompiledRelationBinding is produced -- structural resolution only, not
    left_type/right_type compatibility (that stays Step 5)."""
    synthetic = {
        "id": "derived_offense.synthetic_bad_relation_ref",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "a"},
                {"kind": "offense", "ref": "offense.injury", "local_key": "b"},
            ],
            "relations": [{"relation": "offense.robbery", "left": "a", "right": "b", "left_view": "conduct", "right_view": "conduct"}],  # wrong kind, not a RelationDef
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", synthetic)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_bad_relation_ref")
    assert isinstance(result, list)
    assert any(finding.code == "relation_ref_unresolved" for finding in result)

    def mutate(payload):
        payload["derivation"]["relations"][0]["relation"] = "relation.does_not_exist"

    registry = _mutate(registry, "derived_offense", "derived_offense.synthetic_bad_relation_ref", mutate)
    result = compilemod.compile_offense(registry, "derived_offense.synthetic_bad_relation_ref")
    assert isinstance(result, list)
    assert any(finding.code == "relation_ref_unresolved" for finding in result)


def test_cycle_returns_derivation_cycle_without_recursion_error_and_is_not_memoized() -> None:
    a = {
        "id": "derived_offense.synthetic_compile_cycle_a",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_compile_cycle_b", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "base", "right": "b", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    b = {
        "id": "derived_offense.synthetic_compile_cycle_b",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_compile_cycle_a", "local_key": "a"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "base", "right": "a", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = load_definitions()
    registry = _add(registry, "derived_offense", a)
    registry = _add(registry, "derived_offense", b)

    memo: dict = {}
    in_progress: set = set()
    result = compilemod.compile_offense(  # must not raise RecursionError
        registry, "derived_offense.synthetic_compile_cycle_a", memo=memo, in_progress=in_progress,
    )
    assert isinstance(result, compilemod.DerivationCycle)
    # DerivationCycle must never be memoized -- it's a property of the traversal path
    # (in_progress), not an inherent property of the ref.
    assert "derived_offense.synthetic_compile_cycle_a" not in memo
    assert "derived_offense.synthetic_compile_cycle_b" not in memo
    assert in_progress == set()  # fully unwound
