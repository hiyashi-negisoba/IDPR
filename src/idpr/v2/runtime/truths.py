"""Case truth store and the boundary adapter to v2.1 (build-order step 6A).

This is the single place where case-scoped truths become the case-blind mappings that v2.1 already
takes. `evaluate.evaluate()` wants `Mapping[str, TruthValue]`; `relations.evaluate_relation()` wants
`Mapping[RelationInstanceKey, TruthValue]`. Rather than change either signature -- which would push
case identity down into the definition layer -- `CaseTruths` projects a view for one instance.

The views are lazy read-only mappings, not copies: `evaluate()` only ever does `.get(ref)`, so the
O(1) `__getitem__` is the path that matters, and nothing is materialized per evaluation.

A consequence worth naming now, because it is what makes step 6C cheap: ATTRIBUTE (co-principal
attribution, section 15.2) becomes a *view transformation* -- 乙's conduct facts appear in 甲's
predicate view -- rather than any change to definitions or to the evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Mapping

from idpr.v2.evaluate import TruthValue
from idpr.v2.relations import RelationInstanceKey
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey


class _PredicateView(Mapping[str, TruthValue]):
    """`{predicate ref: truth}` for one instance, backed by the shared store."""

    __slots__ = ("_backing", "_instance")

    def __init__(
        self,
        backing: Mapping[tuple[OffenseInstanceKey, str], TruthValue],
        instance: OffenseInstanceKey,
    ) -> None:
        self._backing = backing
        self._instance = instance

    def __getitem__(self, ref: str) -> TruthValue:
        return self._backing[(self._instance, ref)]

    def __iter__(self) -> Iterator[str]:
        return (ref for (instance, ref) in self._backing if instance == self._instance)

    def __len__(self) -> int:
        return sum(1 for _ in self)


class _RelationView(Mapping[RelationInstanceKey, TruthValue]):
    """`{RelationInstanceKey: truth}` for one instance -- exactly what `evaluate_relation` takes."""

    __slots__ = ("_backing", "_instance")

    def __init__(
        self,
        backing: Mapping[RuntimeRelationKey, TruthValue],
        instance: OffenseInstanceKey,
    ) -> None:
        self._backing = backing
        self._instance = instance

    def __getitem__(self, key: RelationInstanceKey) -> TruthValue:
        return self._backing[RuntimeRelationKey(instance=self._instance, definition_key=key)]

    def __iter__(self) -> Iterator[RelationInstanceKey]:
        return (
            runtime_key.definition_key
            for runtime_key in self._backing
            if runtime_key.instance == self._instance
        )

    def __len__(self) -> int:
        return sum(1 for _ in self)


@dataclass(frozen=True)
class CaseTruths:
    """Everything known about a case, keyed by `OffenseInstanceKey` -- never by form.

    Facts exist before any form is chosen (you need them to choose it), and are stored once rather
    than once per form.
    """

    predicate: Mapping[tuple[OffenseInstanceKey, str], TruthValue] = field(default_factory=dict)
    relation: Mapping[RuntimeRelationKey, TruthValue] = field(default_factory=dict)

    def predicate_view(self, instance: OffenseInstanceKey) -> Mapping[str, TruthValue]:
        return _PredicateView(self.predicate, instance)

    def relation_view(
        self, instance: OffenseInstanceKey
    ) -> Mapping[RelationInstanceKey, TruthValue]:
        return _RelationView(self.relation, instance)
