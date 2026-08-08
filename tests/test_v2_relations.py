"""build-order step 5 -- idpr.v2.relations: relation evaluator + offense-level aggregation."""

from __future__ import annotations

from idpr.v2 import compile as compilemod
from idpr.v2 import evaluate, relations
from idpr.v2.expressions import SLOT_NAMES
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions

TRUE = evaluate.TRUE
FALSE = evaluate.FALSE
UNKNOWN = evaluate.UNKNOWN


def _add(registry: DefinitionRegistry, kind: str, payload: dict) -> DefinitionRegistry:
    by_kind = {k: list(v) for k, v in registry.by_kind.items()}
    by_kind.setdefault(kind, [])
    by_kind[kind].append(DefinitionEntry(id=payload["id"], kind=kind, payload=payload, source_file="<synthetic>"))
    by_id = {}
    frozen = {}
    for k, entries in by_kind.items():
        frozen[k] = tuple(entries)
        for entry in entries:
            by_id[entry.id] = entry
    return DefinitionRegistry(by_id=by_id, by_kind=frozen)


def _compiled(registry: DefinitionRegistry, ref: str) -> compilemod.CompiledOffense:
    compiled = compilemod.compile_offense(registry, ref)
    assert isinstance(compiled, compilemod.CompiledOffense), compiled
    return compiled


def _leaf_refs(compiled: compilemod.CompiledOffense) -> set[str]:
    found: set[str] = set()

    def walk(canon):
        if canon is None:
            return
        op, payload = canon
        if op == "ref":
            found.add(payload)
        elif op in ("all", "any", "one_of"):
            for child in payload:
                walk(child)
        else:
            walk(payload)

    for slot in SLOT_NAMES:
        walk(compiled.slots.get(slot))
    return found


def _all_true(compiled: compilemod.CompiledOffense) -> dict[str, str]:
    return {ref: TRUE for ref in _leaf_refs(compiled)}


def _all_relations_true(compiled: compilemod.CompiledOffense) -> dict:
    return {key: TRUE for key, _ in relations.iter_relation_instances(compiled)}


# --- RelationInstanceKey identity ---


def test_same_definition_reused_under_two_local_keys_gets_two_distinct_keys() -> None:
    """The collision this design was corrected to prevent. Keying by the defining offense's id
    alone would give both occurrences of derived_offense.robbery_causing_injury the same key
    (same id, same relation, same inner local_keys), so ONE supplied relation truth would silently
    answer for BOTH -- discarding exactly the occurrence distinction step 4 preserves."""
    outer = {
        "id": "derived_offense.synthetic_twice_reused",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "first"},
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "second"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "first", "right": "second",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", outer)
    compiled = _compiled(registry, "derived_offense.synthetic_twice_reused")

    keys = [key for key, _ in relations.iter_relation_instances(compiled)]
    assert len(keys) == 3  # the outer's own + one inside each of the two nested occurrences
    assert len(set(keys)) == 3  # ...and all three are distinct

    nested = [k for k in keys if k.relation_ref == "relation.causal_nexus"]
    assert {k.occurrence_path for k in nested} == {
        ("derived_offense.synthetic_twice_reused", "first"),
        ("derived_offense.synthetic_twice_reused", "second"),
    }
    # Both nested keys agree on everything EXCEPT the path -- the path is what separates them.
    assert len({(k.relation_ref, k.left_local_key, k.right_local_key) for k in nested}) == 1


def test_relation_instance_key_is_hashable_and_value_compared() -> None:
    key = relations.RelationInstanceKey(("a", "b"), "relation.r", "l", "r")
    same = relations.RelationInstanceKey(("a", "b"), "relation.r", "l", "r")
    other = relations.RelationInstanceKey(("a", "c"), "relation.r", "l", "r")
    assert key == same and hash(key) == hash(same)
    assert key != other
    assert {key: TRUE}[same] == TRUE


# --- iter_relation_instances ---


def test_iter_over_flat_fixture_yields_its_own_binding_with_top_level_path() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    items = list(relations.iter_relation_instances(compiled))
    assert len(items) == 1
    key, binding = items[0]
    assert key.occurrence_path == ("derived_offense.robbery_causing_injury",)
    assert key.relation_ref == "relation.causal_nexus"
    assert (key.left_local_key, key.right_local_key) == ("base_robbery", "aggravated_result")
    assert binding.left_view == "event" and binding.right_view == "event"


def test_iter_recurses_into_nested_offense_components() -> None:
    outer = {
        "id": "derived_offense.synthetic_nested_outer",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "inner"},
                {"kind": "offense", "ref": "offense.rape", "local_key": "other"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "inner", "right": "other",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", outer)
    compiled = _compiled(registry, "derived_offense.synthetic_nested_outer")

    by_relation = {key.relation_ref: key for key, _ in relations.iter_relation_instances(compiled)}
    assert set(by_relation) == {"relation.occasion_identity", "relation.causal_nexus"}
    assert by_relation["relation.occasion_identity"].occurrence_path == ("derived_offense.synthetic_nested_outer",)
    assert by_relation["relation.causal_nexus"].occurrence_path == (
        "derived_offense.synthetic_nested_outer", "inner",
    )


def test_plain_offense_has_no_relation_obligations() -> None:
    compiled = _compiled(load_definitions(), "offense.robbery")
    assert list(relations.iter_relation_instances(compiled)) == []


# --- evaluate_relation ---


def test_evaluate_relation_looks_up_supplied_truth() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    key, _ = next(iter(relations.iter_relation_instances(compiled)))
    assert relations.evaluate_relation(key, {key: TRUE}) == TRUE
    assert relations.evaluate_relation(key, {key: FALSE}) == FALSE


def test_unsupplied_relation_truth_is_unknown_not_false() -> None:
    """Section 4.3 -- missing evidence is not negation, same default evaluate() uses for an
    ungrounded predicate."""
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    key, _ = next(iter(relations.iter_relation_instances(compiled)))
    assert relations.evaluate_relation(key, {}) == UNKNOWN


# --- evaluate_compiled_offense ---


def test_all_slots_and_relations_true_is_true() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    assert relations.evaluate_compiled_offense(
        compiled, _all_true(compiled), _all_relations_true(compiled),
    ) == TRUE


def test_one_false_slot_predicate_makes_the_whole_offense_false() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    truths = _all_true(compiled)
    truths["ground_fact.property_taking"] = FALSE
    assert relations.evaluate_compiled_offense(compiled, truths, _all_relations_true(compiled)) == FALSE


def test_missing_relation_truth_holds_an_otherwise_satisfied_offense_at_unknown() -> None:
    """The whole point of CompiledOffense = Slots + Required Relation Bindings: every element
    predicate can be TRUE and the offense still is not established without its nexus."""
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    assert relations.evaluate_compiled_offense(compiled, _all_true(compiled), {}) == UNKNOWN


def test_false_relation_makes_the_offense_false() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    relation_truths = {key: FALSE for key, _ in relations.iter_relation_instances(compiled)}
    assert relations.evaluate_compiled_offense(compiled, _all_true(compiled), relation_truths) == FALSE


def test_nested_offense_relation_obligation_propagates_to_the_parent() -> None:
    """Core regression: the compiler folds a nested offense's SLOTS into the parent, but its
    relation obligations survive only inside the nested CompiledOffense. A parent that read only
    `.slots` would call this offense established while the inner causal nexus is false."""
    outer = {
        "id": "derived_offense.synthetic_nested_relation_propagation",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "inner"},
                {"kind": "offense", "ref": "offense.rape", "local_key": "other"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "inner", "right": "other",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", outer)
    compiled = _compiled(registry, "derived_offense.synthetic_nested_relation_propagation")

    truths = _all_true(compiled)
    relation_truths = _all_relations_true(compiled)
    assert relations.evaluate_compiled_offense(compiled, truths, relation_truths) == TRUE

    nested_key = next(
        key for key, _ in relations.iter_relation_instances(compiled)
        if key.occurrence_path == ("derived_offense.synthetic_nested_relation_propagation", "inner")
    )
    relation_truths[nested_key] = FALSE
    assert relations.evaluate_compiled_offense(compiled, truths, relation_truths) == FALSE


def test_slots_are_evaluated_exactly_once_never_again_per_nested_component(monkeypatch) -> None:
    """The nested offense is re-entered for its RELATION obligations only. Re-entering it whole
    would re-evaluate slots the compiler already folded into the parent."""
    outer = {
        "id": "derived_offense.synthetic_slot_eval_count",
        "derivation": {
            "kind": "compose",
            "components": [
                {"kind": "offense", "ref": "derived_offense.robbery_causing_injury", "local_key": "inner"},
                {"kind": "offense", "ref": "offense.rape", "local_key": "other"},
            ],
            "relations": [{
                "relation": "relation.occasion_identity", "left": "inner", "right": "other",
                "left_view": "conduct", "right_view": "conduct",
            }],
        },
        "flattened_elements": {},
    }
    registry = _add(load_definitions(), "derived_offense", outer)
    compiled = _compiled(registry, "derived_offense.synthetic_slot_eval_count")

    evaluated = []
    real_evaluate_all_slots = relations._evaluate_all_slots
    monkeypatch.setattr(
        relations, "_evaluate_all_slots",
        lambda c, truths: (evaluated.append(c), real_evaluate_all_slots(c, truths))[1],
    )
    relations.evaluate_compiled_offense(compiled, _all_true(compiled), _all_relations_true(compiled))

    # Exactly one slot evaluation, on the top-level offense -- not one per nested component.
    assert [c.id for c in evaluated] == ["derived_offense.synthetic_slot_eval_count"]


def test_offense_without_relations_is_decided_by_slots_alone() -> None:
    compiled = _compiled(load_definitions(), "offense.robbery")
    assert relations.evaluate_compiled_offense(compiled, _all_true(compiled), {}) == TRUE
    truths = _all_true(compiled)
    truths["legal_element.robbery_level_violence"] = FALSE
    assert relations.evaluate_compiled_offense(compiled, truths, {}) == FALSE


def test_ungrounded_predicates_leave_the_offense_unknown() -> None:
    compiled = _compiled(load_definitions(), "derived_offense.robbery_causing_injury")
    assert relations.evaluate_compiled_offense(compiled, {}, _all_relations_true(compiled)) == UNKNOWN
