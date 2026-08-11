"""Step 2 v2 Scallop backend parity: compiled offense slots plus relations."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2 import evaluate, relations
from idpr.v2.expressions import SLOT_NAMES, canonical_leaf_refs
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.runtime.scallop_backend import (
    OFFENSE_ELEMENTS_QUERY_RELATION,
    ScallopBackendContractError,
    compile_offense_elements_program,
    render_offense_elements_edb,
    run_offense_elements_parity_program,
    validate_offense_elements_query_rows,
)


def _registry() -> DefinitionRegistry:
    return load_definitions()


def _compiled(registry: DefinitionRegistry, ref: str) -> compilemod.CompiledOffense:
    result = compilemod.compile_offense(registry, ref)
    assert isinstance(result, compilemod.CompiledOffense), result
    return result


def _instance(compiled: compilemod.CompiledOffense, occurrence: str = "o1") -> OffenseInstanceKey:
    return OffenseInstanceKey("C1", "actor", compiled.id, occurrence)


def _all_predicates_true(
    compiled: compilemod.CompiledOffense, instance: OffenseInstanceKey
) -> dict[tuple[OffenseInstanceKey, str], str]:
    refs = set().union(*(canonical_leaf_refs(compiled.slots[slot]) for slot in SLOT_NAMES))
    return {(instance, ref): evaluate.TRUE for ref in refs}


def _relation_truths(
    compiled: compilemod.CompiledOffense,
    instance: OffenseInstanceKey,
    truth: str,
) -> dict[RuntimeRelationKey, str]:
    return {
        RuntimeRelationKey(instance, relation_key): truth
        for relation_key, _binding in relations.iter_relation_instances(compiled)
    }


def _assert_parity(
    tmp_path: Path,
    registry: DefinitionRegistry,
    compiled: compilemod.CompiledOffense,
    truths: CaseTruths,
    instance: OffenseInstanceKey | None = None,
) -> str:
    instance = instance or _instance(compiled)
    result = run_offense_elements_parity_program(
        registry, [compiled], [instance], truths, work_dir=tmp_path
    )
    expected = relations.evaluate_compiled_offense(
        compiled, truths.predicate_view(instance), truths.relation_view(instance)
    )
    assert result == {instance: expected}
    return expected


def test_plain_offense_slots_match_python_and_absent_slots_are_vacuous(tmp_path: Path) -> None:
    registry = _registry()
    compiled = _compiled(registry, "offense.robbery")
    instance = _instance(compiled)
    predicates = _all_predicates_true(compiled, instance)

    assert _assert_parity(tmp_path, registry, compiled, CaseTruths(predicate=predicates), instance) == evaluate.TRUE

    false_ref = next(iter(predicates))
    predicates[false_ref] = evaluate.FALSE
    assert _assert_parity(tmp_path, registry, compiled, CaseTruths(predicate=predicates), instance) == evaluate.FALSE
    assert _assert_parity(tmp_path, registry, compiled, CaseTruths(), instance) == evaluate.UNKNOWN


def test_qualify_slots_and_flat_compose_relations_match_python(tmp_path: Path) -> None:
    registry = _add_qualify(_registry())
    qualified = _compiled(registry, "derived_offense.synthetic_step2_qualified")
    qualified_instance = _instance(qualified)
    qualified_predicates = _all_predicates_true(qualified, qualified_instance)
    assert _assert_parity(
        tmp_path, registry, qualified, CaseTruths(predicate=qualified_predicates), qualified_instance
    ) == evaluate.TRUE

    composed = _compiled(registry, "derived_offense.robbery_causing_injury")
    composed_instance = _instance(composed)
    predicates = _all_predicates_true(composed, composed_instance)
    for relation_truth in (evaluate.TRUE, evaluate.FALSE, evaluate.UNKNOWN):
        truths = CaseTruths(
            predicate=predicates,
            relation=_relation_truths(composed, composed_instance, relation_truth),
        )
        assert _assert_parity(tmp_path, registry, composed, truths, composed_instance) == relation_truth
    assert _assert_parity(
        tmp_path, registry, composed, CaseTruths(predicate=predicates), composed_instance
    ) == evaluate.UNKNOWN


def test_nested_compose_keeps_occurrence_preserving_relation_obligations(tmp_path: Path) -> None:
    registry = _add_nested_compose(_registry())
    compiled = _compiled(registry, "derived_offense.synthetic_step2_outer")
    instance = _instance(compiled)
    predicates = _all_predicates_true(compiled, instance)
    relation_truths = _relation_truths(compiled, instance, evaluate.TRUE)
    nested_keys = {
        key
        for key in relation_truths
        if key.definition_key.relation_ref == "relation.causal_nexus"
    }
    assert {key.definition_key.occurrence_path for key in nested_keys} == {
        ("derived_offense.synthetic_step2_outer", "first"),
        ("derived_offense.synthetic_step2_outer", "second"),
    }
    nested_key = next(key for key in nested_keys if key.definition_key.occurrence_path[-1] == "first")
    relation_truths[nested_key] = evaluate.FALSE

    assert _assert_parity(
        tmp_path, registry, compiled, CaseTruths(predicate=predicates, relation=relation_truths), instance
    ) == evaluate.FALSE

    static = compile_offense_elements_program(registry, [compiled])
    manifest_keys = {key for _helper, _offense, key in static.relation_helper_manifest}
    assert nested_key.definition_key in manifest_keys
    assert all(not isinstance(key, RuntimeRelationKey) for key in manifest_keys)


def test_step2_edb_requires_exact_relation_universe_and_query_is_unordered(tmp_path: Path) -> None:
    registry = _registry()
    compiled = _compiled(registry, "derived_offense.robbery_causing_injury")
    instance = _instance(compiled)
    predicates = _all_predicates_true(compiled, instance)
    edb = render_offense_elements_edb(registry, [compiled], [instance], CaseTruths(predicate=predicates))
    assert "rel v2_relation_key" in edb  # required key exists even without an observation

    relation_key, _binding = next(iter(relations.iter_relation_instances(compiled)))
    unexpected = RuntimeRelationKey(
        instance,
        relation_key.__class__(("wrong",), relation_key.relation_ref, relation_key.left_local_key, relation_key.right_local_key),
    )
    with pytest.raises(ScallopBackendContractError, match="unregistered relation key"):
        render_offense_elements_edb(
            registry,
            [compiled],
            [instance],
            CaseTruths(predicate=predicates, relation={unexpected: evaluate.TRUE}),
        )

    rows = [
        ("C1", "actor", compiled.id, "o2", evaluate.FALSE),
        ("C1", "actor", compiled.id, "o1", evaluate.TRUE),
    ]
    second = _instance(compiled, "o2")
    result = validate_offense_elements_query_rows(
        rows[::-1], instances=[instance, second], compiled_offenses=[compiled]
    )
    assert result == {instance: evaluate.TRUE, second: evaluate.FALSE}
    with pytest.raises(ScallopBackendContractError, match="duplicate"):
        validate_offense_elements_query_rows(
            rows + [rows[0]], instances=[instance, second], compiled_offenses=[compiled]
        )
    with pytest.raises(ScallopBackendContractError, match="missing"):
        validate_offense_elements_query_rows(
            rows[:1], instances=[instance, second], compiled_offenses=[compiled]
        )
    with pytest.raises(ScallopBackendContractError, match="unexpected instance"):
        validate_offense_elements_query_rows(
            [("C1", "actor", "offense.other", "o1", evaluate.TRUE)],
            instances=[instance],
            compiled_offenses=[compiled],
        )
    with pytest.raises(ScallopBackendContractError, match="truth must"):
        validate_offense_elements_query_rows(
            [("C1", "actor", compiled.id, "o1", "MAYBE")],
            instances=[instance],
            compiled_offenses=[compiled],
        )

    assert OFFENSE_ELEMENTS_QUERY_RELATION == "v2_offense_elements_truth"


def test_step2_static_root_and_relation_emission_is_deterministic() -> None:
    registry = _registry()
    plain = _compiled(registry, "offense.robbery")
    composed = _compiled(registry, "derived_offense.robbery_causing_injury")
    first = compile_offense_elements_program(registry, [plain, composed])
    second = compile_offense_elements_program(registry, [composed, plain])

    assert first.program == second.program
    assert first.offense_helper_manifest == second.offense_helper_manifest
    assert first.relation_helper_manifest == second.relation_helper_manifest


def _add_qualify(registry: DefinitionRegistry) -> DefinitionRegistry:
    return _add_derived(
        registry,
        {
            "id": "derived_offense.synthetic_step2_qualified",
            "derivation": {
                "kind": "qualify",
                "base": "offense.robbery",
                "qualifier": "qualifier.occupational_status",
            },
            "flattened_elements": {},
        },
    )


def _add_nested_compose(registry: DefinitionRegistry) -> DefinitionRegistry:
    return _add_derived(
        registry,
        {
            "id": "derived_offense.synthetic_step2_outer",
            "derivation": {
                "kind": "compose",
                "components": [
                    {
                        "kind": "offense",
                        "ref": "derived_offense.robbery_causing_injury",
                        "local_key": "first",
                    },
                    {
                        "kind": "offense",
                        "ref": "derived_offense.robbery_causing_injury",
                        "local_key": "second",
                    },
                ],
                "relations": [
                    {
                        "relation": "relation.occasion_identity",
                        "left": "first",
                        "right": "second",
                        "left_view": "conduct",
                        "right_view": "conduct",
                    }
                ],
            },
            "flattened_elements": {},
        },
    )


def _add_derived(registry: DefinitionRegistry, payload: dict) -> DefinitionRegistry:
    by_kind = {kind: list(entries) for kind, entries in registry.by_kind.items()}
    by_kind.setdefault("derived_offense", []).append(
        DefinitionEntry(
            id=payload["id"], kind="derived_offense", payload=payload, source_file="<synthetic>"
        )
    )
    frozen = {kind: tuple(entries) for kind, entries in by_kind.items()}
    by_id = {entry.id: entry for entries in frozen.values() for entry in entries}
    return DefinitionRegistry(by_id=by_id, by_kind=frozen)
