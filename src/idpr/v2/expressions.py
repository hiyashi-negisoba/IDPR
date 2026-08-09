"""element_expression tree walking and canonicalization (v2.1.0 section 8).

Two representations are in play:
  - the raw authored tree, e.g. {"op": "all", "args": [{"op": "ref", "ref": "..."}, ...]}
  - CanonicalExpr, a structural normal form used for semantic-equality comparison (axis 2).

Canonicalization rules (see docs/contracts/v2/SCHEMA_NOTES.md and the approved v2 type-checker
plan for the full rationale):
  - ALL/ANY: flatten nested same-op children (associative), hold children as a frozenset
    (commutative; idempotency falls out of frozenset dedup for free), single remaining child
    collapses to that child's own canonical form.
  - ONE_OF: NOT associative and NOT safely idempotent (concrete counterexample: with A=B=C=true,
    ONE_OF(A, ONE_OF(B,C)) is true but ONE_OF(A,B,C) is false -- not the same proposition), so
    nested ONE_OF is never flattened and duplicate branches are never deduped. Children are held
    order-independently (a genuinely exclusive-alternatives list doesn't care about listing order)
    via a deterministic recursive sort key, not raw repr() (hash-seed-dependent through any nested
    frozenset). A single remaining child still collapses (ONE_OF of one thing IS that thing; this
    is a base case, not a merge with a parent, so it doesn't hit the associativity problem).
  - NOT: wraps its one child, no flattening/double-negation collapsing (no fixture needs it).
"""

from __future__ import annotations

from typing import Any, Iterator, Mapping

SLOT_NAMES: tuple[str, ...] = (
    "subject",
    "object",
    "conduct",
    "circumstance",
    "result",
    "causation",
    "mental",
)

CanonicalExpr = Any  # None | ("ref", id) | ("all"|"any", frozenset[CanonicalExpr]) |
#                       ("one_of", tuple[CanonicalExpr, ...]) | ("not", CanonicalExpr)


def iter_leaf_refs(expr: Mapping[str, Any] | None) -> Iterator[str]:
    """Yield every {op: ref, ref: id} leaf's id, recursing through all/any/not/one_of (including
    inside NOT -- reference *typing* is in scope even though NOT's evidence semantics are a
    separate runtime invariant, section 4.3)."""
    if expr is None:
        return
    op = expr["op"]
    if op == "ref":
        yield expr["ref"]
    elif op in ("all", "any", "one_of"):
        for child in expr["args"]:
            yield from iter_leaf_refs(child)
    elif op == "not":
        yield from iter_leaf_refs(expr["arg"])
    else:
        raise ValueError(f"unknown element_expression op {op!r}")


def leaf_refs(expr: Mapping[str, Any] | None) -> frozenset[str]:
    return frozenset(iter_leaf_refs(expr))


def slot_leaf_refs(elements: Mapping[str, Any]) -> dict[str, frozenset[str]]:
    return {slot: leaf_refs(elements.get(slot)) for slot in SLOT_NAMES}


def canonical_leaf_refs(expr: CanonicalExpr) -> frozenset[str]:
    """Leaf predicate refs of an already-canonicalized expression.

    Sibling to `leaf_refs()`, which walks the pre-canonicalize raw dict form. `compiled.slots[...]`
    (compile.py) is already canonical by the time runtime attribution needs its leaves, so
    `leaf_refs()` would walk the wrong shape and silently return nothing."""
    if expr is None:
        return frozenset()
    op, payload = expr
    if op == "ref":
        return frozenset({payload})
    if op in ("all", "any"):
        return frozenset().union(*(canonical_leaf_refs(child) for child in payload))
    if op == "one_of":
        return frozenset().union(*(canonical_leaf_refs(child) for child in payload))
    if op == "not":
        return canonical_leaf_refs(payload)
    raise ValueError(f"unknown canonical op {op!r}")


def canonicalize(expr: Mapping[str, Any] | None) -> CanonicalExpr:
    if expr is None:
        return None
    op = expr["op"]
    if op == "ref":
        return ("ref", expr["ref"])
    if op in ("all", "any"):
        children: list[CanonicalExpr] = []
        for child in expr["args"]:
            canon_child = canonicalize(child)
            if isinstance(canon_child, tuple) and canon_child[0] == op:
                children.extend(canon_child[1])
            else:
                children.append(canon_child)
        unique = frozenset(children)
        if len(unique) == 1:
            return next(iter(unique))
        return (op, unique)
    if op == "one_of":
        children = tuple(canonicalize(child) for child in expr["args"])
        if len(children) == 1:
            return children[0]
        return ("one_of", tuple(sorted(children, key=_sort_key)))
    if op == "not":
        return ("not", canonicalize(expr["arg"]))
    raise ValueError(f"unknown element_expression op {op!r}")


def combine_all(*exprs: CanonicalExpr) -> CanonicalExpr:
    """ALL-combine already-canonical forms, applying canonicalize's ALL flatten/dedup/
    single-child-collapse rules. combine_all() with zero non-None args -> None."""
    children: list[CanonicalExpr] = []
    for expr in exprs:
        if expr is None:
            continue
        if isinstance(expr, tuple) and expr[0] == "all":
            children.extend(expr[1])
        else:
            children.append(expr)
    if not children:
        return None
    unique = frozenset(children)
    if len(unique) == 1:
        return next(iter(unique))
    return ("all", unique)


def _sort_key(canon: CanonicalExpr) -> tuple:
    """A fully deterministic total order over CanonicalExpr values, independent of Python's
    hash-seed-dependent frozenset iteration order (which raw repr() would be sensitive to through
    any nested frozenset)."""
    if canon is None:
        return (0,)
    op, payload = canon
    if op == "ref":
        return (1, payload)
    if op in ("all", "any"):
        return (2, op, tuple(sorted((_sort_key(child) for child in payload))))
    if op == "one_of":
        return (3, tuple(_sort_key(child) for child in payload))
    if op == "not":
        return (4, _sort_key(payload))
    raise ValueError(f"unknown canonical op {op!r}")
