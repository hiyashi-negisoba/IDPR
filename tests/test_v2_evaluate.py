from __future__ import annotations

from idpr.v2 import evaluate
from idpr.v2 import expressions

TRUE = evaluate.TRUE
FALSE = evaluate.FALSE
UNKNOWN = evaluate.UNKNOWN

REF_A = {"op": "ref", "ref": "ground_fact.a"}
REF_B = {"op": "ref", "ref": "ground_fact.b"}
REF_C = {"op": "ref", "ref": "ground_fact.c"}
REF_D = {"op": "ref", "ref": "ground_fact.d"}
REF_E = {"op": "ref", "ref": "ground_fact.e"}


def _all(*args):
    return {"op": "all", "args": list(args)}


def _any(*args):
    return {"op": "any", "args": list(args)}


def _one_of(*args):
    return {"op": "one_of", "args": list(args)}


def _not(arg):
    return {"op": "not", "arg": arg}


def _eval(tree, truths):
    return evaluate.evaluate(expressions.canonicalize(tree), truths)


# --- ALL ---


def test_all_true_and_true_is_true() -> None:
    assert _eval(_all(REF_A, REF_B), {"ground_fact.a": TRUE, "ground_fact.b": TRUE}) == TRUE


def test_all_false_wins_even_with_unknown_present() -> None:
    truths = {"ground_fact.a": FALSE, "ground_fact.b": UNKNOWN}
    assert _eval(_all(REF_A, REF_B), truths) == FALSE


def test_all_true_and_unknown_is_unknown() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": UNKNOWN}
    assert _eval(_all(REF_A, REF_B), truths) == UNKNOWN


# --- ANY ---


def test_any_true_present_is_true() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": FALSE, "ground_fact.c": UNKNOWN}
    assert _eval(_any(REF_A, REF_B, REF_C), truths) == TRUE


def test_any_all_false_is_false() -> None:
    truths = {"ground_fact.a": FALSE, "ground_fact.b": FALSE}
    assert _eval(_any(REF_A, REF_B), truths) == FALSE


def test_any_false_and_unknown_is_unknown() -> None:
    truths = {"ground_fact.a": FALSE, "ground_fact.b": UNKNOWN}
    assert _eval(_any(REF_A, REF_B), truths) == UNKNOWN


# --- NOT ---


def test_not_true_is_false() -> None:
    assert _eval(_not(REF_A), {"ground_fact.a": TRUE}) == FALSE


def test_not_false_is_true() -> None:
    assert _eval(_not(REF_A), {"ground_fact.a": FALSE}) == TRUE


def test_not_unknown_is_unknown() -> None:
    assert _eval(_not(REF_A), {"ground_fact.a": UNKNOWN}) == UNKNOWN


def test_not_missing_evidence_never_becomes_satisfaction() -> None:
    """4.3 invariant: NOT never converts missing/unresolved evidence into satisfaction."""
    assert _eval(_not(REF_A), {}) == UNKNOWN


# --- ONE_OF ---


def test_one_of_exactly_one_true_rest_false_is_true() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": FALSE, "ground_fact.c": FALSE}
    assert _eval(_one_of(REF_A, REF_B, REF_C), truths) == TRUE


def test_one_of_two_true_is_false_even_with_unknown_present() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": TRUE, "ground_fact.c": UNKNOWN}
    assert _eval(_one_of(REF_A, REF_B, REF_C), truths) == FALSE


def test_one_of_all_false_is_false() -> None:
    truths = {"ground_fact.a": FALSE, "ground_fact.b": FALSE}
    assert _eval(_one_of(REF_A, REF_B), truths) == FALSE


def test_one_of_one_true_one_unknown_is_unknown() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": UNKNOWN}
    assert _eval(_one_of(REF_A, REF_B), truths) == UNKNOWN


def test_one_of_zero_true_one_unknown_rest_false_is_unknown() -> None:
    truths = {"ground_fact.a": UNKNOWN, "ground_fact.b": FALSE, "ground_fact.c": FALSE}
    assert _eval(_one_of(REF_A, REF_B, REF_C), truths) == UNKNOWN


def test_one_of_zero_true_two_unknown_is_unknown() -> None:
    truths = {"ground_fact.a": UNKNOWN, "ground_fact.b": UNKNOWN}
    assert _eval(_one_of(REF_A, REF_B), truths) == UNKNOWN


def test_one_of_nested_vs_flat_doc_counterexample() -> None:
    """v2.1.0 type-checker plan's context section: with A=B=C=true, ONE_OF(A, ONE_OF(B,C)) is
    true (inner ONE_OF(B,C) is false since both true, so outer is ONE_OF(TRUE, FALSE)) but
    ONE_OF(A,B,C) is false (three-true, not exactly one) -- not the same proposition, confirmed
    here at the evaluation level (not just canonicalize's structural non-equivalence)."""
    truths = {"ground_fact.a": TRUE, "ground_fact.b": TRUE, "ground_fact.c": TRUE}
    nested = _eval(_one_of(REF_A, _one_of(REF_B, REF_C)), truths)
    flat = _eval(_one_of(REF_A, REF_B, REF_C), truths)
    assert nested == TRUE
    assert flat == FALSE


def test_one_of_is_truth_functional_not_leaf_joint() -> None:
    """Boundary regression: evaluate() folds over each child's own already-evaluated TruthValue,
    never over a joint completion of leaf refs shared across children. ONE_OF(A, NOT(A)) with
    A=UNKNOWN evaluates UNKNOWN here, even though a leaf-joint-completion analysis would notice A
    and NOT(A) are exactly-one-true under every completion of A and say TRUE. This is intended
    behavior, not an oversight -- see docs/handoff/CURRENT.md, Step 3 entry."""
    truths = {"ground_fact.a": UNKNOWN}
    assert _eval(_one_of(REF_A, _not(REF_A)), truths) == UNKNOWN


# --- missing ref / vacuous ---


def test_missing_ref_defaults_to_unknown() -> None:
    assert _eval(REF_A, {}) == UNKNOWN


def test_none_expression_is_vacuously_true() -> None:
    assert evaluate.evaluate(None, {}) == TRUE


# --- flatten-safety ---


def test_all_flatten_safety() -> None:
    truths = {"ground_fact.a": TRUE, "ground_fact.b": FALSE, "ground_fact.c": UNKNOWN}
    nested = _eval(_all(REF_A, _all(REF_B, REF_C)), truths)
    flat = _eval(_all(REF_A, REF_B, REF_C), truths)
    assert nested == flat == FALSE


def test_any_flatten_safety() -> None:
    truths = {"ground_fact.a": FALSE, "ground_fact.b": UNKNOWN, "ground_fact.c": UNKNOWN}
    nested = _eval(_any(REF_A, _any(REF_B, REF_C)), truths)
    flat = _eval(_any(REF_A, REF_B, REF_C), truths)
    assert nested == flat == UNKNOWN


# --- integration ---


def test_nested_mixed_operator_tree() -> None:
    tree = _all(
        _any(REF_A, REF_B),
        _not(REF_C),
        _one_of(REF_D, REF_E),
    )
    truths = {
        "ground_fact.a": FALSE,
        "ground_fact.b": TRUE,
        "ground_fact.c": FALSE,
        "ground_fact.d": TRUE,
        "ground_fact.e": FALSE,
    }
    assert _eval(tree, truths) == TRUE
