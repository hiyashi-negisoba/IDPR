from __future__ import annotations

import itertools

import pytest

from idpr.v2 import expressions
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, evaluate

VALUES = (TRUE, FALSE, UNKNOWN)


def _ref(name: str) -> dict[str, str]:
    return {"op": "ref", "ref": name}


def _evaluate(op: str, values: tuple[str, ...]) -> str:
    tree = {"op": op, "args": [_ref(f"p{index}") for index in range(len(values))]}
    truths = {f"p{index}": value for index, value in enumerate(values)}
    return evaluate(expressions.canonicalize(tree), truths)


@pytest.mark.parametrize("values", tuple(itertools.product(VALUES, repeat=3)))
def test_all_is_strong_kleene_conjunction(values: tuple[str, ...]) -> None:
    expected = FALSE if FALSE in values else TRUE if all(v == TRUE for v in values) else UNKNOWN
    assert _evaluate("all", values) == expected


@pytest.mark.parametrize("values", tuple(itertools.product(VALUES, repeat=3)))
def test_any_is_strong_kleene_disjunction(values: tuple[str, ...]) -> None:
    expected = TRUE if TRUE in values else FALSE if all(v == FALSE for v in values) else UNKNOWN
    assert _evaluate("any", values) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    ((TRUE, FALSE), (FALSE, TRUE), (UNKNOWN, UNKNOWN)),
)
def test_not_preserves_unknown(value: str, expected: str) -> None:
    tree = {"op": "not", "arg": _ref("p")}
    assert evaluate(expressions.canonicalize(tree), {"p": value}) == expected


def test_missing_evidence_is_unknown_and_never_negation() -> None:
    ref = _ref("missing")
    assert evaluate(expressions.canonicalize(ref), {}) == UNKNOWN
    assert evaluate(expressions.canonicalize({"op": "not", "arg": ref}), {}) == UNKNOWN
