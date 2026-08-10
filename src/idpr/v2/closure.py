"""Step 7 structural closure and Call 2 probe compilation.

This module traverses only the loaded Definition Layer registry.  It does not
evaluate an element, decide doctrine applicability, or infer participation
roles.  Every emitted item carries the registry path that produced it, so the
Step 7 output can be audited without a second legal-knowledge table.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

Classification = Literal[
    "mandatory_core",
    "offense_probe",
    "doctrine_probe",
    "completion_probe",
    "participation_probe",
]

_OFFENSE_KINDS = frozenset({"offense", "derived_offense"})


class ClosureError(ValueError):
    """A caller or registry graph violates the Step 7 structural contract."""


@dataclass(frozen=True, order=True)
class FrontierFact:
    """One Call 2 GroundFact request at one structural occurrence.

    `occurrence_path=()` is the existing root path for a direct seed.  A
    COMPOSE component appends its authored local key, so same-ref components
    remain distinct rather than collapsing into one factual request.
    """

    occurrence_path: tuple[str, ...]
    source_path: tuple[str, ...]
    ground_fact_ref: str


@dataclass(frozen=True, order=True)
class ClosureItem:
    """A single source-derived Step 7 classification item."""

    definition_ref: str
    classification: Classification
    source_path: tuple[str, ...]
    occurrence_path: tuple[str, ...]
    ground_fact_frontier: tuple[FrontierFact, ...]
    deferred_refs: tuple[str, ...]


@dataclass(frozen=True)
class ClosureResult:
    """The complete deterministic result for one canonical offense-seed set."""

    mandatory_core: tuple[ClosureItem, ...]
    offense_probes: tuple[ClosureItem, ...]
    doctrine_probes: tuple[ClosureItem, ...]
    completion_probes: tuple[ClosureItem, ...]
    participation_probes: tuple[ClosureItem, ...]
    mandatory_offense_refs: frozenset[str]
    candidate_offense_refs: frozenset[str]

    @property
    def items(self) -> tuple[ClosureItem, ...]:
        return (
            self.mandatory_core
            + self.offense_probes
            + self.doctrine_probes
            + self.completion_probes
            + self.participation_probes
        )


def compile_closure(registry: DefinitionRegistry, offense_seeds: Iterable[str]) -> ClosureResult:
    """Compile mandatory structure and conditional probes from canonical offense seeds.

    The input must already be canonical Definition Layer refs.  This is not a
    name resolver and deliberately does not accept a free-text offense label.
    """
    seeds = tuple(sorted(set(offense_seeds)))
    if not seeds:
        raise ClosureError("Step 7 requires at least one offense or derived_offense seed")
    for ref in seeds:
        entry = registry.get(ref)
        if entry is None:
            raise ClosureError(f"unknown Step 7 offense seed {ref!r}")
        if entry.kind not in _OFFENSE_KINDS:
            raise ClosureError(
                f"Step 7 seed {ref!r} has kind={entry.kind!r}, expected offense or derived_offense"
            )

    mandatory: list[ClosureItem] = []
    mandatory_seen: set[tuple[str, tuple[str, ...], tuple[str, ...]]] = set()
    visiting: set[tuple[str, tuple[str, ...]]] = set()

    def add_mandatory(ref: str, source_path: tuple[str, ...], occurrence_path: tuple[str, ...]) -> None:
        key = (ref, source_path, occurrence_path)
        if key in mandatory_seen:
            return
        entry = _entry(registry, ref)
        cycle_key = (ref, occurrence_path)
        if cycle_key in visiting:
            raise ClosureError(f"cycle while compiling Step 7 mandatory closure at {ref!r}")
        visiting.add(cycle_key)
        try:
            mandatory_seen.add(key)
            mandatory.append(_item_for_entry(
                registry, entry, "mandatory_core", source_path, occurrence_path
            ))
            _add_mandatory_dependencies(registry, entry, source_path, occurrence_path, add_mandatory)
        finally:
            visiting.discard(cycle_key)

    for seed in seeds:
        add_mandatory(seed, (f"seed:{seed}",), ())

    mandatory_offense_refs = frozenset(
        item.definition_ref
        for item in mandatory
        if registry.kind_of(item.definition_ref) in _OFFENSE_KINDS
    )
    offense_probes = _offense_probes(registry, mandatory_offense_refs)
    candidate_offense_refs = mandatory_offense_refs | frozenset(
        item.definition_ref for item in offense_probes
    )
    doctrine_probes = _doctrine_probes(registry, mandatory_offense_refs)
    completion_probes = _completion_probes(registry, mandatory, offense_probes)
    participation_probes = _participation_probes(registry, mandatory, offense_probes)

    return ClosureResult(
        mandatory_core=_sorted_items(mandatory),
        offense_probes=_sorted_items(offense_probes),
        doctrine_probes=_sorted_items(doctrine_probes),
        completion_probes=_sorted_items(completion_probes),
        participation_probes=_sorted_items(participation_probes),
        mandatory_offense_refs=mandatory_offense_refs,
        candidate_offense_refs=candidate_offense_refs,
    )


def compile_candidate_offenses(
    registry: DefinitionRegistry, closure: ClosureResult,
) -> Mapping[str, CompiledOffense]:
    """Compile every structural candidate once for later Step 7 orchestration.

    A mandatory offense is active. A reverse branch discovered as a probe is
    merely a candidate, even though it is compilable here. Its later factual
    survival, not this function, makes it conditionally active. This mechanical
    compilation is not a second closure or activation rule.
    """
    compiled: dict[str, CompiledOffense] = {}
    for ref in sorted(closure.candidate_offense_refs):
        result = compile_offense(registry, ref)
        if not isinstance(result, CompiledOffense):
            raise ClosureError(f"Step 7 candidate {ref!r} did not compile: {result!r}")
        compiled[ref] = result
    return compiled


def _add_mandatory_dependencies(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    add_mandatory,
) -> None:
    if entry.kind == "offense":
        for index, module in enumerate(entry.payload.get("element_modules") or ()):
            add_mandatory(
                module["ref"], source_path + (f"element_modules[{index}]",), occurrence_path
            )
        return
    if entry.kind != "derived_offense":
        return
    derivation = entry.payload["derivation"]
    if derivation["kind"] == "qualify":
        add_mandatory(derivation["base"], source_path + ("derivation.base",), occurrence_path)
        add_mandatory(
            derivation["qualifier"], source_path + ("derivation.qualifier",), occurrence_path
        )
        return
    for component in derivation["components"]:
        local_key = component["local_key"]
        add_mandatory(
            component["ref"],
            source_path + (f"components[{local_key}]",),
            occurrence_path + (local_key,),
        )
    for index, relation in enumerate(derivation["relations"]):
        add_mandatory(
            relation["relation"],
            source_path + (f"relations[{index}:{relation['left']}→{relation['right']}]",),
            occurrence_path,
        )


def _offense_probes(
    registry: DefinitionRegistry, mandatory_offense_refs: frozenset[str]
) -> list[ClosureItem]:
    probes: list[ClosureItem] = []
    for entry in sorted(registry.by_kind.get("derived_offense", ()), key=lambda item: item.id):
        derivation = entry.payload["derivation"]
        if derivation["kind"] == "qualify":
            base = derivation["base"]
            if base in mandatory_offense_refs:
                source_path = (f"probe:{entry.id}", f"qualify_base:{base}")
                probes.append(_item_for_entry(
                    registry,
                    _entry(registry, derivation["qualifier"]),
                    "offense_probe",
                    source_path + ("derivation.qualifier",),
                    (),
                    definition_ref=entry.id,
                ))
            continue

        for component in derivation["components"]:
            if component["kind"] != "offense" or component["ref"] not in mandatory_offense_refs:
                continue
            local_key = component["local_key"]
            source_path = (f"probe:{entry.id}", f"compose_base:{local_key}")
            facts: list[FrontierFact] = []
            deferred: list[str] = []
            for other in derivation["components"]:
                if other["local_key"] == local_key:
                    continue
                _collect_entry(
                    registry,
                    _entry(registry, other["ref"]),
                    source_path + (f"components[{other['local_key']}]",),
                    (other["local_key"],),
                    facts,
                    deferred,
                    set(),
                )
            for index, relation in enumerate(derivation["relations"]):
                deferred.append(relation["relation"])
                source_path = source_path + (f"relations[{index}]",)
            probes.append(_make_item(
                entry.id, "offense_probe", source_path, (), facts, deferred
            ))
    return probes


def _doctrine_probes(
    registry: DefinitionRegistry, mandatory_offense_refs: frozenset[str]
) -> list[ClosureItem]:
    probes: list[ClosureItem] = []
    for entry in sorted(registry.by_kind.get("doctrine", ()), key=lambda item: item.id):
        scope = entry.payload.get("offense_scope")
        if scope is not None and scope not in mandatory_offense_refs:
            continue
        probes.append(_item_for_entry(
            registry, entry, "doctrine_probe", (f"doctrine:{entry.id}",), ()
        ))
    return probes


def _completion_probes(
    registry: DefinitionRegistry,
    mandatory: Iterable[ClosureItem],
    offense_probes: Iterable[ClosureItem],
) -> list[ClosureItem]:
    contexts = [
        item for item in (*tuple(mandatory), *tuple(offense_probes))
        if registry.kind_of(item.definition_ref) in _OFFENSE_KINDS
    ]
    policies = {entry.payload["offense"]: entry for entry in registry.by_kind.get("completion_policy", ())}
    probes: list[ClosureItem] = []
    for context in contexts:
        policy = policies.get(context.definition_ref)
        if policy is None:
            continue
        probes.append(_item_for_entry(
            registry,
            policy,
            "completion_probe",
            context.source_path + (f"completion:{policy.id}",),
            context.occurrence_path,
        ))
    return probes


def _participation_probes(
    registry: DefinitionRegistry,
    mandatory: Iterable[ClosureItem],
    offense_probes: Iterable[ClosureItem],
) -> list[ClosureItem]:
    policy = next(iter(registry.by_kind.get("participation_policy", ())), None)
    if policy is None:
        return []
    contexts = [
        item for item in (*tuple(mandatory), *tuple(offense_probes))
        if registry.kind_of(item.definition_ref) in _OFFENSE_KINDS
    ]
    probes: list[ClosureItem] = []
    for context in contexts:
        offense = _entry(registry, context.definition_ref)
        constraints = offense.payload.get("participation_constraints") or {}
        for mode in sorted(policy.payload["modes"]):
            probes.append(_item_for_mode(
                registry,
                policy,
                mode,
                context.source_path + (f"participation:{mode}",),
                context.occurrence_path,
            ))
        statutory_deeming = constraints.get("statutory_deeming")
        if statutory_deeming is not None:
            probes.append(_item_for_expression(
                registry,
                definition_ref=offense.id,
                classification="participation_probe",
                source_path=context.source_path + ("participation:statutory_deeming",),
                occurrence_path=context.occurrence_path,
                expressions=(statutory_deeming["requires"],),
                initial_deferred=(),
            ))
    return probes


def _item_for_entry(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    classification: Classification,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    *,
    definition_ref: str | None = None,
) -> ClosureItem:
    expressions: list[Mapping[str, object]] = []
    initial_deferred: list[str] = []
    if entry.kind == "offense":
        expressions.extend((entry.payload.get("elements") or {}).values())
    elif entry.kind == "element_bundle":
        expressions.append(entry.payload["requires"])
    elif entry.kind == "qualifier":
        expressions.extend((entry.payload.get("additions") or {}).values())
    elif entry.kind == "doctrine":
        expressions.append(entry.payload["requires"])
        initial_deferred.append(entry.id)
    elif entry.kind == "completion_policy":
        for state in (entry.payload.get("states") or {}).values():
            if state.get("when") is not None:
                expressions.append(state["when"])
            if state.get("requires") is not None:
                expressions.append(state["requires"])
    elif entry.kind == "participation_policy":
        for mode in (entry.payload.get("modes") or {}).values():
            if mode.get("requires") is not None:
                expressions.append(mode["requires"])
    elif entry.kind == "primitive":
        return _item_for_ref(
            registry, definition_ref or entry.id, classification, source_path, occurrence_path, entry.payload["ref"]
        )
    elif entry.kind == "exported_component":
        resolved = registry.resolve_export(entry.id)
        if resolved is None:
            raise ClosureError(f"exported component {entry.id!r} cannot be resolved by registry.resolve_export()")
        return _item_for_ref(
            registry, definition_ref or entry.id, classification, source_path, occurrence_path, resolved
        )
    elif entry.kind == "relation":
        initial_deferred.append(entry.id)
    return _item_for_expression(
        registry,
        definition_ref=definition_ref or entry.id,
        classification=classification,
        source_path=source_path,
        occurrence_path=occurrence_path,
        expressions=tuple(expr for expr in expressions if expr is not None),
        initial_deferred=tuple(initial_deferred),
    )


def _item_for_mode(
    registry: DefinitionRegistry,
    policy: DefinitionEntry,
    mode: str,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
) -> ClosureItem:
    payload = policy.payload["modes"][mode]
    expressions = (payload["requires"],) if payload.get("requires") is not None else ()
    return _item_for_expression(
        registry,
        definition_ref=policy.id,
        classification="participation_probe",
        source_path=source_path,
        occurrence_path=occurrence_path,
        expressions=expressions,
        initial_deferred=(),
    )


def _item_for_ref(
    registry: DefinitionRegistry,
    definition_ref: str,
    classification: Classification,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    ref: str,
) -> ClosureItem:
    facts: list[FrontierFact] = []
    deferred: list[str] = []
    _collect_ref(registry, ref, source_path + (f"ref:{ref}",), occurrence_path, facts, deferred, set())
    return _make_item(definition_ref, classification, source_path, occurrence_path, facts, deferred)


def _item_for_expression(
    registry: DefinitionRegistry,
    *,
    definition_ref: str,
    classification: Classification,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    expressions: Iterable[Mapping[str, object]],
    initial_deferred: Iterable[str],
) -> ClosureItem:
    facts: list[FrontierFact] = []
    deferred = list(initial_deferred)
    for index, expression in enumerate(expressions):
        _collect_expression(
            registry,
            expression,
            source_path + (f"expression[{index}]",),
            occurrence_path,
            facts,
            deferred,
            set(),
        )
    return _make_item(definition_ref, classification, source_path, occurrence_path, facts, deferred)


def _collect_entry(
    registry: DefinitionRegistry,
    entry: DefinitionEntry,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    facts: list[FrontierFact],
    deferred: list[str],
    visiting: set[str],
) -> None:
    if entry.id in visiting:
        raise ClosureError(f"cycle while collecting Step 7 frontier at {entry.id!r}")
    visiting.add(entry.id)
    try:
        if entry.kind == "ground_fact":
            facts.append(FrontierFact(occurrence_path, source_path, entry.id))
        elif entry.kind == "legal_element":
            deferred.append(entry.id)
            for index, ground_fact in enumerate(entry.payload.get("grounded_by") or ()):
                facts.append(FrontierFact(
                    occurrence_path, source_path + (f"grounded_by[{index}]",), ground_fact
                ))
        elif entry.kind == "primitive":
            _collect_ref(registry, entry.payload["ref"], source_path + ("primitive.ref",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "exported_component":
            resolved = registry.resolve_export(entry.id)
            if resolved is None:
                raise ClosureError(f"exported component {entry.id!r} cannot be resolved by registry.resolve_export()")
            _collect_ref(registry, resolved, source_path + ("export.resolve_export",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "element_bundle":
            _collect_expression(registry, entry.payload["requires"], source_path + ("requires",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "qualifier":
            for slot, expression in (entry.payload.get("additions") or {}).items():
                _collect_expression(registry, expression, source_path + (f"additions.{slot}",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "offense":
            for slot, expression in (entry.payload.get("elements") or {}).items():
                _collect_expression(registry, expression, source_path + (f"elements.{slot}",), occurrence_path, facts, deferred, visiting)
            for index, module in enumerate(entry.payload.get("element_modules") or ()):
                _collect_ref(registry, module["ref"], source_path + (f"element_modules[{index}]",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "derived_offense":
            derivation = entry.payload["derivation"]
            if derivation["kind"] == "qualify":
                _collect_ref(registry, derivation["base"], source_path + ("derivation.base",), occurrence_path, facts, deferred, visiting)
                _collect_ref(registry, derivation["qualifier"], source_path + ("derivation.qualifier",), occurrence_path, facts, deferred, visiting)
            else:
                for component in derivation["components"]:
                    _collect_ref(registry, component["ref"], source_path + (f"components[{component['local_key']}]",), occurrence_path + (component["local_key"],), facts, deferred, visiting)
                deferred.extend(relation["relation"] for relation in derivation["relations"])
        elif entry.kind == "doctrine":
            deferred.append(entry.id)
            _collect_expression(registry, entry.payload["requires"], source_path + ("requires",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "relation":
            deferred.append(entry.id)
        elif entry.kind == "completion_policy":
            for state_name, state in (entry.payload.get("states") or {}).items():
                if state.get("when") is not None:
                    _collect_expression(registry, state["when"], source_path + (f"states.{state_name}.when",), occurrence_path, facts, deferred, visiting)
                if state.get("requires") is not None:
                    _collect_expression(registry, state["requires"], source_path + (f"states.{state_name}.requires",), occurrence_path, facts, deferred, visiting)
        elif entry.kind == "participation_policy":
            for mode_name, mode in (entry.payload.get("modes") or {}).items():
                if mode.get("requires") is not None:
                    _collect_expression(registry, mode["requires"], source_path + (f"modes.{mode_name}.requires",), occurrence_path, facts, deferred, visiting)
    finally:
        visiting.discard(entry.id)


def _collect_expression(
    registry: DefinitionRegistry,
    expression: Mapping[str, object],
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    facts: list[FrontierFact],
    deferred: list[str],
    visiting: set[str],
) -> None:
    op = expression["op"]
    if op == "ref":
        _collect_ref(registry, expression["ref"], source_path, occurrence_path, facts, deferred, visiting)
    elif op in ("all", "any", "one_of"):
        for index, child in enumerate(expression["args"]):
            _collect_expression(registry, child, source_path + (f"{op}[{index}]",), occurrence_path, facts, deferred, visiting)
    elif op == "not":
        _collect_expression(registry, expression["arg"], source_path + ("not",), occurrence_path, facts, deferred, visiting)
    else:
        raise ClosureError(f"unknown expression operator {op!r}")


def _collect_ref(
    registry: DefinitionRegistry,
    ref: str,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    facts: list[FrontierFact],
    deferred: list[str],
    visiting: set[str],
) -> None:
    _collect_entry(registry, _entry(registry, ref), source_path, occurrence_path, facts, deferred, visiting)


def _make_item(
    definition_ref: str,
    classification: Classification,
    source_path: tuple[str, ...],
    occurrence_path: tuple[str, ...],
    facts: Iterable[FrontierFact],
    deferred: Iterable[str],
) -> ClosureItem:
    return ClosureItem(
        definition_ref=definition_ref,
        classification=classification,
        source_path=source_path,
        occurrence_path=occurrence_path,
        ground_fact_frontier=tuple(sorted(set(facts))),
        deferred_refs=tuple(sorted(set(deferred))),
    )


def _entry(registry: DefinitionRegistry, ref: str) -> DefinitionEntry:
    entry = registry.get(ref)
    if entry is None:
        raise ClosureError(f"unresolved registry ref during Step 7 traversal: {ref!r}")
    return entry


def _sorted_items(items: Iterable[ClosureItem]) -> tuple[ClosureItem, ...]:
    return tuple(sorted(set(items), key=lambda item: (
        item.definition_ref,
        item.source_path,
        item.occurrence_path,
        item.classification,
    )))


__all__ = [
    "Classification",
    "ClosureError",
    "ClosureItem",
    "ClosureResult",
    "FrontierFact",
    "compile_candidate_offenses",
    "compile_closure",
]
