from __future__ import annotations

from idpr.v2 import expressions

REF_A = {"op": "ref", "ref": "ground_fact.a"}
REF_B = {"op": "ref", "ref": "ground_fact.b"}
REF_C = {"op": "ref", "ref": "ground_fact.c"}


def _all(*args):
    return {"op": "all", "args": list(args)}


def _any(*args):
    return {"op": "any", "args": list(args)}


def _one_of(*args):
    return {"op": "one_of", "args": list(args)}


def _not(arg):
    return {"op": "not", "arg": arg}


def test_iter_leaf_refs_walks_into_not() -> None:
    tree = _all(_any(REF_A, REF_B), _not(REF_C), _one_of(REF_A, REF_B))
    assert set(expressions.iter_leaf_refs(tree)) == {"ground_fact.a", "ground_fact.b", "ground_fact.c"}


def test_leaf_refs_of_none_is_empty() -> None:
    assert expressions.leaf_refs(None) == frozenset()


def test_slot_leaf_refs_fills_all_seven_slots() -> None:
    result = expressions.slot_leaf_refs({"conduct": REF_A})
    assert set(result) == set(expressions.SLOT_NAMES)
    assert result["conduct"] == frozenset({"ground_fact.a"})
    assert result["mental"] == frozenset()


def test_canonical_leaf_refs_of_none_is_empty() -> None:
    assert expressions.canonical_leaf_refs(None) == frozenset()


def test_canonical_leaf_refs_walks_all_any_not_one_of() -> None:
    # step 6C: compiled.slots[...] is already CanonicalExpr by the time attribution reads it, so
    # this must walk the tuple form -- leaf_refs()/iter_leaf_refs() walk the raw dict form instead.
    tree = _all(_any(REF_A, REF_B), _not(REF_C), _one_of(REF_A, REF_B))
    canon = expressions.canonicalize(tree)
    assert expressions.canonical_leaf_refs(canon) == {"ground_fact.a", "ground_fact.b", "ground_fact.c"}


def test_canonical_leaf_refs_matches_raw_leaf_refs_after_canonicalize() -> None:
    for tree in (
        _all(REF_A, _any(REF_B, REF_C)),
        _one_of(REF_A, _not(REF_B)),
        REF_A,
    ):
        assert expressions.canonical_leaf_refs(expressions.canonicalize(tree)) == expressions.leaf_refs(tree)


def test_all_is_commutative() -> None:
    assert expressions.canonicalize(_all(REF_A, REF_B)) == expressions.canonicalize(_all(REF_B, REF_A))


def test_all_is_associative_and_flattens() -> None:
    left = expressions.canonicalize(_all(REF_A, _all(REF_B, REF_C)))
    right = expressions.canonicalize(_all(REF_A, REF_B, REF_C))
    assert left == right


def test_all_is_idempotent() -> None:
    assert expressions.canonicalize(_all(REF_A, REF_A)) == expressions.canonicalize(REF_A)


def test_all_and_any_never_compare_equal() -> None:
    assert expressions.canonicalize(_all(REF_A, REF_B)) != expressions.canonicalize(_any(REF_A, REF_B))


def test_one_of_is_not_associative() -> None:
    nested = expressions.canonicalize(_one_of(REF_A, _one_of(REF_B, REF_C)))
    flat = expressions.canonicalize(_one_of(REF_A, REF_B, REF_C))
    assert nested != flat


def test_one_of_is_order_independent() -> None:
    assert expressions.canonicalize(_one_of(REF_A, REF_B)) == expressions.canonicalize(_one_of(REF_B, REF_A))


def test_one_of_single_child_collapses() -> None:
    assert expressions.canonicalize(_one_of(REF_A)) == expressions.canonicalize(REF_A)


def test_combine_all_of_nothing_is_none() -> None:
    assert expressions.combine_all(None, None) is None


def test_combine_all_of_one_expr_equals_that_expr() -> None:
    canon = expressions.canonicalize(REF_A)
    assert expressions.combine_all(canon) == canon
