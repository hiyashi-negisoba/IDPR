from __future__ import annotations

import copy

from idpr.v2.checks.operators import check_operators
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


def _codes(findings) -> set[str]:
    return {finding.code for finding in findings}


def test_real_corpus_has_no_operator_findings() -> None:
    assert check_operators(load_definitions()) == []


def test_all_swapped_for_any_with_same_leaves_is_caught() -> None:
    def mutate(payload):
        conduct = payload["flattened_elements"]["conduct"]
        assert conduct["op"] == "all"
        conduct["op"] = "any"

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.robbery_rape", mutate)
    findings = check_operators(registry)
    assert "flattened_elements_semantic_mismatch" in _codes(findings)


def test_dropped_slot_is_caught() -> None:
    def mutate(payload):
        del payload["flattened_elements"]["subject"]

    registry = _mutate(
        load_definitions(), "derived_offense", "derived_offense.occupational_embezzlement", mutate,
    )
    findings = check_operators(registry)
    assert "flattened_elements_missing_slot" in _codes(findings)


def test_export_key_pointed_at_wrong_declared_export_is_caught() -> None:
    # offense.injury only exports 'result' -> ground_fact.injury_occurred; there's no other export
    # key to redirect to on the same offense, so instead corrupt the *source_offense's* exports map
    # itself to point 'result' at a different ground fact -- this proves the result slot now gets
    # full equality (round 3 could not have caught a change on the exported side at all).
    def mutate(payload):
        payload["exports"]["result"] = "ground_fact.violence_used"

    registry = _mutate(load_definitions(), "offense", "offense.injury", mutate)
    findings = check_operators(registry)
    assert "flattened_elements_semantic_mismatch" in _codes(findings)


MULTI_SLOT_BUNDLE = {
    "id": "bundle.synthetic_multi_slot",
    "requires": {
        "op": "all",
        "args": [
            {"op": "ref", "ref": "ground_fact.syn_a"},
            {"op": "ref", "ref": "ground_fact.syn_b"},
        ],
    },
}


def test_element_modules_multi_slot_attachment_combines_with_own_elements() -> None:
    offense_payload = {
        "id": "offense.synthetic_multi_slot",
        "identity": {"name": "synthetic"},
        "elements": {"conduct": {"op": "ref", "ref": "ground_fact.own_conduct"}},
        "element_modules": [{
            "ref": "bundle.synthetic_multi_slot",
            "placement": {"ground_fact.syn_a": "conduct", "ground_fact.syn_b": "circumstance"},
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", MULTI_SLOT_BUNDLE)
    registry = _add(registry, "offense", offense_payload)

    derived_payload = {
        "id": "derived_offense.synthetic_wraps_multi_slot",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_multi_slot", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "conduct": {
                "op": "all",
                "args": [
                    {"op": "ref", "ref": "ground_fact.own_conduct"},
                    {"op": "ref", "ref": "ground_fact.syn_a"},
                ],
            },
            "circumstance": {"op": "ref", "ref": "ground_fact.syn_b"},
        },
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = [f for f in check_operators(registry) if f.object_id == "derived_offense.synthetic_wraps_multi_slot"]
    assert findings == []


def test_non_decomposable_element_modules_bundle_is_rejected() -> None:
    non_decomposable_bundle = {
        "id": "bundle.synthetic_non_decomposable",
        "requires": {
            "op": "any",
            "args": [
                {"op": "ref", "ref": "ground_fact.syn_a"},   # -> conduct
                {"op": "ref", "ref": "ground_fact.syn_b"},   # -> circumstance
            ],
        },
    }
    offense_payload = {
        "id": "offense.synthetic_non_decomposable",
        "identity": {"name": "synthetic"},
        "elements": {},
        "element_modules": [{
            "ref": "bundle.synthetic_non_decomposable",
            "placement": {"ground_fact.syn_a": "conduct", "ground_fact.syn_b": "circumstance"},
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", non_decomposable_bundle)
    registry = _add(registry, "offense", offense_payload)
    derived_payload = {
        "id": "derived_offense.synthetic_wraps_non_decomposable",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_non_decomposable", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {"subject": {"op": "ref", "ref": "ground_fact.occupational_status"}},
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = check_operators(registry)
    assert "bundle_placement_not_decomposable" in _codes(findings)


def test_any_root_single_slot_bundle_preserved_whole() -> None:
    bundle_payload = {
        "id": "bundle.synthetic_any_single_slot",
        "requires": {
            "op": "any",
            "args": [
                {"op": "ref", "ref": "ground_fact.syn_a"},
                {"op": "ref", "ref": "ground_fact.syn_b"},
            ],
        },
    }
    offense_payload = {
        "id": "offense.synthetic_any_single_slot",
        "identity": {"name": "synthetic"},
        "elements": {},
        "element_modules": [{
            "ref": "bundle.synthetic_any_single_slot",
            "placement": {"ground_fact.syn_a": "conduct", "ground_fact.syn_b": "conduct"},
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", bundle_payload)
    registry = _add(registry, "offense", offense_payload)
    derived_payload = {
        "id": "derived_offense.synthetic_wraps_any_single_slot",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_any_single_slot", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "conduct": {
                "op": "any",
                "args": [
                    {"op": "ref", "ref": "ground_fact.syn_a"},
                    {"op": "ref", "ref": "ground_fact.syn_b"},
                ],
            },
        },
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = [f for f in check_operators(registry) if f.object_id == "derived_offense.synthetic_wraps_any_single_slot"]
    assert findings == []


def test_nested_all_of_all_bundle_decomposes() -> None:
    bundle_payload = {
        "id": "bundle.synthetic_nested_all",
        "requires": {
            "op": "all",
            "args": [
                {"op": "all", "args": [{"op": "ref", "ref": "ground_fact.syn_a"}, {"op": "ref", "ref": "ground_fact.syn_b"}]},
                {"op": "all", "args": [{"op": "ref", "ref": "ground_fact.syn_c"}, {"op": "ref", "ref": "ground_fact.syn_d"}]},
            ],
        },
    }
    offense_payload = {
        "id": "offense.synthetic_nested_all",
        "identity": {"name": "synthetic"},
        "elements": {},
        "element_modules": [{
            "ref": "bundle.synthetic_nested_all",
            "placement": {
                "ground_fact.syn_a": "conduct", "ground_fact.syn_b": "conduct",
                "ground_fact.syn_c": "circumstance", "ground_fact.syn_d": "circumstance",
            },
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", bundle_payload)
    registry = _add(registry, "offense", offense_payload)
    derived_payload = {
        "id": "derived_offense.synthetic_wraps_nested_all",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_nested_all", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "conduct": {"op": "all", "args": [{"op": "ref", "ref": "ground_fact.syn_a"}, {"op": "ref", "ref": "ground_fact.syn_b"}]},
            "circumstance": {"op": "all", "args": [{"op": "ref", "ref": "ground_fact.syn_c"}, {"op": "ref", "ref": "ground_fact.syn_d"}]},
        },
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = [f for f in check_operators(registry) if f.object_id == "derived_offense.synthetic_wraps_nested_all"]
    assert findings == []


def test_all_with_any_sub_part_single_slot_decomposes() -> None:
    bundle_payload = {
        "id": "bundle.synthetic_all_any_single_slot",
        "requires": {
            "op": "all",
            "args": [
                {"op": "any", "args": [{"op": "ref", "ref": "ground_fact.syn_a"}, {"op": "ref", "ref": "ground_fact.syn_b"}]},
                {"op": "ref", "ref": "ground_fact.syn_c"},
            ],
        },
    }
    offense_payload = {
        "id": "offense.synthetic_all_any_single_slot",
        "identity": {"name": "synthetic"},
        "elements": {},
        "element_modules": [{
            "ref": "bundle.synthetic_all_any_single_slot",
            "placement": {
                "ground_fact.syn_a": "conduct", "ground_fact.syn_b": "conduct", "ground_fact.syn_c": "conduct",
            },
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", bundle_payload)
    registry = _add(registry, "offense", offense_payload)
    derived_payload = {
        "id": "derived_offense.synthetic_wraps_all_any_single_slot",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_all_any_single_slot", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "conduct": {
                "op": "all",
                "args": [
                    {"op": "any", "args": [{"op": "ref", "ref": "ground_fact.syn_a"}, {"op": "ref", "ref": "ground_fact.syn_b"}]},
                    {"op": "ref", "ref": "ground_fact.syn_c"},
                ],
            },
        },
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = [f for f in check_operators(registry) if f.object_id == "derived_offense.synthetic_wraps_all_any_single_slot"]
    assert findings == []


def test_all_with_any_sub_part_spanning_slots_is_rejected() -> None:
    bundle_payload = {
        "id": "bundle.synthetic_all_any_multi_slot",
        "requires": {
            "op": "all",
            "args": [
                {"op": "ref", "ref": "ground_fact.syn_d"},
                {"op": "any", "args": [{"op": "ref", "ref": "ground_fact.syn_a"}, {"op": "ref", "ref": "ground_fact.syn_b"}]},
            ],
        },
    }
    offense_payload = {
        "id": "offense.synthetic_all_any_multi_slot",
        "identity": {"name": "synthetic"},
        "elements": {},
        "element_modules": [{
            "ref": "bundle.synthetic_all_any_multi_slot",
            "placement": {
                "ground_fact.syn_d": "conduct", "ground_fact.syn_a": "circumstance", "ground_fact.syn_b": "result",
            },
        }],
    }
    registry = load_definitions()
    registry = _add(registry, "element_bundle", bundle_payload)
    registry = _add(registry, "offense", offense_payload)
    derived_payload = {
        "id": "derived_offense.synthetic_wraps_all_any_multi_slot",
        "derivation": {"kind": "qualify", "base": "offense.synthetic_all_any_multi_slot", "qualifier": "qualifier.occupational_status"},
        "flattened_elements": {"subject": {"op": "ref", "ref": "ground_fact.occupational_status"}},
    }
    registry = _add(registry, "derived_offense", derived_payload)

    findings = check_operators(registry)
    assert "bundle_placement_not_decomposable" in _codes(findings)


def test_replay_uses_inner_derivation_not_corrupted_flattened_cache() -> None:
    """Round-5 regression: an outer DerivedOffenseDef COMPOSEs an inner one (as an offense-kind
    component) whose own stored flattened_elements is deliberately corrupted. check_operators must
    (a) flag the inner entry's own mismatch, and (b) compute the outer's expected value from the
    inner's TRUE derivation, not its corrupted cache -- so the outer's check is unaffected."""
    inner = {
        "id": "derived_offense.synthetic_inner",
        "derivation": {"kind": "qualify", "base": "offense.robbery", "qualifier": "qualifier.occupational_status"},
        # Corrupted: this doesn't match what qualify(offense.robbery, occupational_status) implies
        # -- 'mental' is dropped from what the true derivation would produce.
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "object": {"op": "ref", "ref": "ground_fact.property_taking"},
            "conduct": {
                "op": "all",
                "args": [
                    {"op": "ref", "ref": "ground_fact.property_taking"},
                    {"op": "ref", "ref": "legal_element.robbery_level_violence"},
                ],
            },
        },
    }
    outer = {
        "id": "derived_offense.synthetic_outer",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.synthetic_inner", "local_key": "inner"},
                {"kind": "offense", "ref": "offense.rape", "local_key": "rape_part"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "inner", "right": "rape_part", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {
            "subject": {"op": "ref", "ref": "ground_fact.occupational_status"},
            "object": {"op": "ref", "ref": "ground_fact.property_taking"},
            "conduct": {
                "op": "all",
                "args": [
                    {"op": "ref", "ref": "ground_fact.property_taking"},
                    {"op": "ref", "ref": "legal_element.robbery_level_violence"},
                    {"op": "ref", "ref": "ground_fact.forcible_intercourse"},
                ],
            },
            # The outer correctly includes 'mental' (from qualify's TRUE replay of the inner),
            # even though the inner's own stored cache omitted it.
            "mental": {"op": "ref", "ref": "legal_element.appropriation_intent"},
        },
    }
    registry = load_definitions()
    registry = _add(registry, "derived_offense", inner)
    registry = _add(registry, "derived_offense", outer)

    findings = check_operators(registry)
    inner_findings = [f for f in findings if f.object_id == "derived_offense.synthetic_inner"]
    outer_findings = [f for f in findings if f.object_id == "derived_offense.synthetic_outer"]

    assert any(f.code == "flattened_elements_missing_slot" and "mental" in f.field_path for f in inner_findings)
    assert outer_findings == []


def test_check_operators_terminates_on_cyclic_composition_without_axis_six() -> None:
    a = {
        "id": "derived_offense.synthetic_cycle_a",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_cycle_b", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "base", "right": "b", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    b = {
        "id": "derived_offense.synthetic_cycle_b",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_cycle_a", "local_key": "a"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "base", "right": "a", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = load_definitions()
    registry = _add(registry, "derived_offense", a)
    registry = _add(registry, "derived_offense", b)

    # Must not raise RecursionError -- axis 2 alone, without axis 6 having run, must still
    # terminate cleanly.
    check_operators(registry)


def test_dangling_compose_component_ref_does_not_crash() -> None:
    """axis 2 is independently callable -- it may see a malformed graph before axis 1 has run.
    A dangling ref in any component position must degrade to a Finding (or a silently-unfilled
    contribution deferred to axis 1's own report), never IndexError/KeyError/RecursionError."""
    broken = {
        "id": "derived_offense.synthetic_dangling_compose",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.does_not_exist", "local_key": "a"},
                {"kind": "primitive", "ref": "primitive.does_not_exist", "local_key": "p", "slot": "conduct"},
                {"kind": "exported_component", "ref": "exported_component.does_not_exist", "local_key": "e", "slot": "result"},
                {"kind": "bundle", "ref": "bundle.does_not_exist", "local_key": "b", "placement": {"ground_fact.x": "circumstance"}},
            ],
            "relations": [{"relation": "relation.does_not_exist", "left": "a", "right": "p", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {"conduct": {"op": "ref", "ref": "ground_fact.x"}},
    }
    registry = _add(load_definitions(), "derived_offense", broken)
    findings = check_operators(registry)  # must not raise
    assert isinstance(findings, list)


def test_broken_export_chain_does_not_crash() -> None:
    def mutate(payload):
        payload["source_offense"] = "offense.does_not_exist"

    registry = _mutate(load_definitions(), "exported_component", "exported_component.injury_result", mutate)
    findings = check_operators(registry)  # must not raise
    assert isinstance(findings, list)


def test_qualify_with_dangling_base_or_qualifier_does_not_crash() -> None:
    def mutate(payload):
        payload["derivation"]["base"] = "offense.does_not_exist"
        payload["derivation"]["qualifier"] = "qualifier.does_not_exist"

    registry = _mutate(load_definitions(), "derived_offense", "derived_offense.occupational_embezzlement", mutate)
    findings = check_operators(registry)  # must not raise
    assert isinstance(findings, list)
