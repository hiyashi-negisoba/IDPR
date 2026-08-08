"""Axis 2: operator typing.

flattened_elements must be exactly what `derivation` implies -- full semantic equality via
idpr.v2.compile.compile_offense(), not a leaf-ref superset check (a superset check can't
distinguish ALL(A,B) from ANY(A,B), which have the same leaf-ref set but very different truth
conditions).

The single invariant this whole module protects: `flattened_elements` is read in exactly ONE
place -- as the `actual` side of the top-level equality check in check_operators(). It is NEVER
used as an input when computing some OTHER entry's expected value, even when that other entry
composes a DerivedOffenseDef as one of its own components.

Type checking was always answering "does flattened_elements match what compiling derivation would
produce" -- now that compiling is a first-class public operation (build-order step 4, "QUALIFY /
COMPOSE compiler"), this module is a thin consumer of idpr.v2.compile: it calls
compile.compile_offense() for the expected value and forwards any compilation Finding as its own.
"""

from __future__ import annotations

from idpr.v2 import compile, expressions
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "operator"


def check_operators(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    memo: dict = {}
    in_progress: set = set()

    for entry in registry.by_kind.get("derived_offense", ()):
        compiled = compile.compile_offense(registry, entry.id, memo=memo, in_progress=in_progress)
        if isinstance(compiled, compile.DerivationCycle):
            continue
        if isinstance(compiled, list):
            findings.extend(compiled)
            continue

        for slot in expressions.SLOT_NAMES:
            expected = compiled.slots.get(slot)
            actual = expressions.canonicalize((entry.payload.get("flattened_elements") or {}).get(slot))
            if expected is None and actual is None:
                continue
            if expected is None:
                findings.append(Finding(
                    _AXIS, "flattened_elements_unexpected_slot", entry.id, f"flattened_elements.{slot}",
                    "no contributor implies this slot, but flattened_elements sets it",
                ))
            elif actual is None:
                findings.append(Finding(
                    _AXIS, "flattened_elements_missing_slot", entry.id, f"flattened_elements.{slot}",
                    "a contributor implies this slot, but flattened_elements omits it",
                ))
            elif expected != actual:
                findings.append(Finding(
                    _AXIS, "flattened_elements_semantic_mismatch", entry.id, f"flattened_elements.{slot}",
                    f"expected {expected!r}, got {actual!r}",
                ))
    return findings
