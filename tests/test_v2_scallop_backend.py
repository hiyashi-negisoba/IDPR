"""Step 8 v2-only Scallop backend Step 1 parity and contract tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import evaluate, expressions
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.runtime.scallop_backend import (
    ExpressionRoot,
    ScallopBackendContractError,
    canonical_expression_serialization,
    compile_expression_program,
    render_case_truths_edb,
    run_expression_parity_program,
    validate_expression_query_rows,
)
from idpr.v2.relations import RelationInstanceKey


_DEFINITIONS = Path(__file__).resolve().parents[1] / "data/v2/definitions"
_INSTANCE = OffenseInstanceKey("C1", "actor", "offense.robbery", "o1")
_OTHER_INSTANCE = OffenseInstanceKey("C1", "other", "offense.robbery", "o1")
_A = "ground_fact.taking_conduct"
_B = "ground_fact.death_of_victim"
_C = "ground_fact.killing_conduct"
_LEGAL = "legal_element.intent"


def _registry():
    return load_definitions(_DEFINITIONS)


def _ref(value: str) -> dict[str, str]:
    return {"op": "ref", "ref": value}


def _canonical(tree: dict) -> expressions.CanonicalExpr:
    value = expressions.canonicalize(tree)
    assert value is not None
    return value


def _truths(values: dict[str, str]) -> CaseTruths:
    return CaseTruths(predicate={(_INSTANCE, ref): truth for ref, truth in values.items()})


@pytest.mark.parametrize(
    ("expression", "truths"),
    [
        (_canonical(_ref(_A)), {_A: evaluate.TRUE}),
        (_canonical(_ref(_A)), {}),
        (_canonical({"op": "all", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.FALSE, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "all", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.TRUE, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "any", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.TRUE, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "any", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.FALSE, _B: evaluate.FALSE}),
        (_canonical({"op": "any", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.FALSE, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "not", "arg": _ref(_A)}), {_A: evaluate.TRUE}),
        (_canonical({"op": "not", "arg": _ref(_A)}), {_A: evaluate.FALSE}),
        (_canonical({"op": "not", "arg": _ref(_A)}), {_A: evaluate.UNKNOWN}),
        (_canonical({"op": "one_of", "args": [_ref(_A), _ref(_B), _ref(_C)]}), {_A: evaluate.TRUE, _B: evaluate.FALSE, _C: evaluate.FALSE}),
        (_canonical({"op": "one_of", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.FALSE, _B: evaluate.FALSE}),
        (_canonical({"op": "one_of", "args": [_ref(_A), _ref(_B), _ref(_C)]}), {_A: evaluate.TRUE, _B: evaluate.TRUE, _C: evaluate.UNKNOWN}),
        (_canonical({"op": "one_of", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.TRUE, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "one_of", "args": [_ref(_A), _ref(_B)]}), {_A: evaluate.UNKNOWN, _B: evaluate.UNKNOWN}),
        (_canonical({"op": "all", "args": [_ref(_LEGAL), {"op": "not", "arg": _ref(_A)}]}), {_LEGAL: evaluate.TRUE, _A: evaluate.FALSE}),
    ],
)
def test_scallop_expression_results_match_python_evaluator(tmp_path: Path, expression, truths) -> None:
    root = ExpressionRoot("expr.parity", expression)
    result = run_expression_parity_program(
        _registry(), [root], [_INSTANCE], _truths(truths), work_dir=tmp_path
    )
    assert result[(_INSTANCE, root.expression_id)] == evaluate.evaluate(expression, truths)


def test_instance_universe_makes_missing_truth_unknown_and_empty_universe_has_no_rows(tmp_path: Path) -> None:
    root = ExpressionRoot("expr.missing", _canonical(_ref(_A)))
    registry = _registry()
    result = run_expression_parity_program(registry, [root], [_INSTANCE], CaseTruths(), work_dir=tmp_path)
    assert result == {(_INSTANCE, "expr.missing"): evaluate.UNKNOWN}

    program = compile_expression_program(registry, [root])
    assert "v2_instance" in program
    assert validate_expression_query_rows([], instances=[], roots=[root]) == {}


def test_canonical_frozenset_serialization_and_program_emission_are_deterministic() -> None:
    first = _canonical({"op": "all", "args": [_ref(_A), _ref(_B)]})
    second = _canonical({"op": "all", "args": [_ref(_B), _ref(_A)]})
    assert canonical_expression_serialization(first) == canonical_expression_serialization(second)

    registry = _registry()
    roots = [ExpressionRoot("expr.order", first)]
    assert compile_expression_program(registry, roots) == compile_expression_program(
        registry, [ExpressionRoot("expr.order", second)]
    )


def test_non_none_roots_and_loaded_predicate_refs_are_required() -> None:
    registry = _registry()
    with pytest.raises(ScallopBackendContractError, match="non-None"):
        compile_expression_program(registry, [ExpressionRoot("expr.none", None)])
    with pytest.raises(ScallopBackendContractError, match="non-predicate"):
        compile_expression_program(
            registry, [ExpressionRoot("expr.bad", ("ref", "offense.robbery"))]
        )


def test_edb_renderer_preserves_predicate_and_relation_case_truth_identity(tmp_path: Path) -> None:
    registry = _registry()
    relation = RuntimeRelationKey(
        instance=_INSTANCE,
        definition_key=RelationInstanceKey(
            occurrence_path=("derived_offense.example", "left"),
            relation_ref="relation.causal_nexus",
            left_local_key="left",
            right_local_key="right",
        ),
    )
    edb = render_case_truths_edb(
        registry,
        [_INSTANCE],
        CaseTruths(
            predicate={(_INSTANCE, _A): evaluate.TRUE},
            relation={relation: evaluate.UNKNOWN},
        ),
        relation_keys=[relation],
    )
    assert '"ground_fact.taking_conduct", "TRUE"' in edb
    assert '"relation.causal_nexus", "left", "right", "UNKNOWN"' in edb
    assert '"[\\"derived_offense.example\\",\\"left\\"]"' in edb

    root = ExpressionRoot("expr.relation-edb", _canonical(_ref(_A)))
    result = run_expression_parity_program(
        registry,
        [root],
        [_INSTANCE],
        CaseTruths(
            predicate={(_INSTANCE, _A): evaluate.TRUE},
            relation={relation: evaluate.UNKNOWN},
        ),
        relation_keys=[relation],
        work_dir=tmp_path,
    )
    assert result == {(_INSTANCE, root.expression_id): evaluate.TRUE}


def test_query_result_validation_is_order_independent_and_rejects_invalid_key_sets() -> None:
    roots = [ExpressionRoot("expr.a", _canonical(_ref(_A))), ExpressionRoot("expr.b", _canonical(_ref(_B)))]
    rows = [
        (*_fields(_OTHER_INSTANCE), "expr.b", evaluate.FALSE),
        (*_fields(_INSTANCE), "expr.a", evaluate.TRUE),
        (*_fields(_OTHER_INSTANCE), "expr.a", evaluate.UNKNOWN),
        (*_fields(_INSTANCE), "expr.b", evaluate.FALSE),
    ]
    result = validate_expression_query_rows(rows[::-1], instances=[_OTHER_INSTANCE, _INSTANCE], roots=roots)
    assert result[(_INSTANCE, "expr.a")] == evaluate.TRUE
    assert result[(_OTHER_INSTANCE, "expr.a")] == evaluate.UNKNOWN

    with pytest.raises(ScallopBackendContractError, match="duplicate"):
        validate_expression_query_rows(rows + [rows[0]], instances=[_INSTANCE, _OTHER_INSTANCE], roots=roots)
    with pytest.raises(ScallopBackendContractError, match="unexpected instance"):
        validate_expression_query_rows(
            [(*("bad", "actor", "offense.robbery", "o1"), "expr.a", evaluate.TRUE)],
            instances=[_INSTANCE, _OTHER_INSTANCE],
            roots=roots,
        )
    with pytest.raises(ScallopBackendContractError, match="unknown expression_id"):
        validate_expression_query_rows(
            [(*_fields(_INSTANCE), "expr.other", evaluate.TRUE)], instances=[_INSTANCE, _OTHER_INSTANCE], roots=roots
        )
    with pytest.raises(ScallopBackendContractError, match="truth must"):
        validate_expression_query_rows(
            [(*_fields(_INSTANCE), "expr.a", "MAYBE")], instances=[_INSTANCE, _OTHER_INSTANCE], roots=roots
        )
    with pytest.raises(ScallopBackendContractError, match="missing"):
        validate_expression_query_rows(rows[:-1], instances=[_INSTANCE, _OTHER_INSTANCE], roots=roots)


def _fields(instance: OffenseInstanceKey) -> tuple[str, str, str, str]:
    return (instance.case_id, instance.actor_id, instance.offense_ref, instance.occurrence_id)
