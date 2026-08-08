"""element_expression truth-value evaluator (v2.1.0 section 8 grammar, v2.2.0 section 12
three-valued semantics). Executes the truth semantics of an already-canonical element_expression --
it does not re-interpret legal definitions, assemble slot contributions (checks/operators.py's
replay_slot does that, step 2), or compile anything (step 4). Build-order step 3.
"""

from __future__ import annotations

from typing import Iterable, Literal, Mapping

from idpr.v2.expressions import CanonicalExpr

TruthValue = Literal["TRUE", "FALSE", "UNKNOWN"]
TRUE: TruthValue = "TRUE"
FALSE: TruthValue = "FALSE"
UNKNOWN: TruthValue = "UNKNOWN"


def evaluate(expr: CanonicalExpr, truths: Mapping[str, TruthValue]) -> TruthValue:
    """Evaluate a canonicalized element_expression (expressions.canonicalize output) against a
    leaf-ref -> TruthValue map.

    - expr is None (an empty slot, or combine_all() of nothing) -> TRUE: vacuous truth, nothing to
      fail.
    - a ref missing from `truths` -> UNKNOWN (v2.1.0 section 4.3: missing evidence is not negation;
      the same default v2.2.0 section 10 assumes for an ungrounded predicate, e.g.
      "weapon_used = unresolved").
    - all/any/not: v2.2.0 section 12 truth tables, verbatim.
    - one_of: Kleene "exactly-one" extension, truth-functional over each child's own already-
      evaluated TruthValue -- it does NOT perform joint completion analysis over leaf refs shared
      across children (see docs/handoff/CURRENT.md, this step's entry, and the
      ONE_OF(A, NOT(A))-with-A=UNKNOWN regression test in tests/test_v2_evaluate.py for the exact
      boundary this draws).

    Recurses directly into CanonicalExpr children (already-canonical tuples, never raw op/args
    dicts) -- callers holding a raw authored tree call expressions.canonicalize() first; no second
    tree-walker is introduced here. No re-validation of structural invariants (duplicate ONE_OF
    branches etc.) -- axis 1 (checks/references.py) already guarantees a type-checked registry has
    none of these.
    """
    if expr is None:
        return TRUE
    op, payload = expr
    if op == "ref":
        return truths.get(payload, UNKNOWN)
    if op == "all":
        return fold_all(evaluate(child, truths) for child in payload)
    if op == "any":
        return fold_any(evaluate(child, truths) for child in payload)
    if op == "one_of":
        return _fold_one_of(evaluate(child, truths) for child in payload)
    if op == "not":
        return _negate(evaluate(payload, truths))
    raise ValueError(f"unknown canonical op {op!r}")


def fold_all(values: Iterable[TruthValue]) -> TruthValue:
    """Three-valued conjunction over an arbitrary sequence of already-evaluated TruthValues.

    Public (unlike its ANY/ONE_OF/NOT siblings) because conjunction is the one fold other layers
    legitimately need over things that are not element_expression children: step 5's
    relations.evaluate_compiled_offense() ANDs slot results with relation obligations. This module
    stays the single source of truth for three-valued Boolean semantics -- callers reuse this rather
    than reimplementing the truth table.
    """
    values = list(values)
    if any(value == FALSE for value in values):
        return FALSE
    if all(value == TRUE for value in values):
        return TRUE
    return UNKNOWN


def fold_any(values: Iterable[TruthValue]) -> TruthValue:
    """Three-valued disjunction over an arbitrary sequence of already-evaluated TruthValues.

    Public for the same reason and by the same rule as fold_all: a layer above needs this fold over
    things that are not element_expression children, and must not reimplement the truth table. Here
    that layer is the runtime's doctrine pool -- "is this stage defeated?" is exactly ANY over each
    active doctrine's own requires-truth (runtime/effects.py). Reimplementing it there is how
    "self_defense=TRUE but necessity=UNKNOWN -> unresolved" bugs get written: a confirmed TRUE must
    win over any number of UNKNOWNs, which is precisely what this fold already says.
    """
    values = list(values)
    if any(value == TRUE for value in values):
        return TRUE
    if all(value == FALSE for value in values):
        return FALSE
    return UNKNOWN


def _fold_one_of(values: Iterable[TruthValue]) -> TruthValue:
    values = list(values)
    true_count = sum(1 for value in values if value == TRUE)
    unknown_count = sum(1 for value in values if value == UNKNOWN)
    if true_count >= 2:
        return FALSE
    if unknown_count == 0:
        return TRUE if true_count == 1 else FALSE
    return UNKNOWN


def _negate(value: TruthValue) -> TruthValue:
    if value == TRUE:
        return FALSE
    if value == FALSE:
        return TRUE
    return UNKNOWN
