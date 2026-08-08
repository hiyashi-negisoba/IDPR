from __future__ import annotations

from idpr.v2.checks.derivation import check_derivation_graph
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, [])
    by_kind[kind].append(DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>"))
    by_id = {}
    frozen_by_kind = {}
    for k, entries in by_kind.items():
        frozen_by_kind[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen_by_kind)


def test_real_corpus_has_no_cycles() -> None:
    assert check_derivation_graph(load_definitions()) == []


def test_two_derived_offenses_composing_each_other_is_a_cycle() -> None:
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
    registry = _add(load_definitions(), "derived_offense", a)
    registry = _add(registry, "derived_offense", b)

    findings = check_derivation_graph(registry)
    assert len(findings) >= 1
    assert all(f.code == "derivation_cycle" for f in findings)


def test_self_composing_derived_offense_is_a_length_one_cycle() -> None:
    c = {
        "id": "derived_offense.synthetic_self_cycle",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.robbery", "local_key": "base"},
                {"kind": "offense", "ref": "derived_offense.synthetic_self_cycle", "local_key": "self"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "base", "right": "self", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", c)
    findings = check_derivation_graph(registry)
    assert any(f.code == "derivation_cycle" for f in findings)


def test_legitimate_chain_without_back_edge_is_not_flagged() -> None:
    # derived_offense.robbery_causing_injury composes offense.robbery (a real OffenseDef, not a
    # DerivedOffenseDef) -- a legitimate chain with no back-edge should never be flagged.
    registry = load_definitions()
    chain = {
        "id": "derived_offense.synthetic_wraps_existing",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "offense.rape", "local_key": "rape_part"},
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "b"},
            ],
            "relations": [{"relation": "relation.occasion_identity", "left": "rape_part", "right": "b", "left_view": "conduct", "right_view": "conduct"}],
        },
        "flattened_elements": {},
    }
    registry = _add(registry, "derived_offense", chain)
    assert check_derivation_graph(registry) == []
