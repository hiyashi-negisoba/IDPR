"""Axis 8: completion policies (build-order step 6B, 7th schema addendum).

The load-bearing check here is relation coverage, and it is deliberately blunt:

    a state that suspends nothing   ->  no relation disposition needed (everything is retained)
    a state that suspends anything  ->  EVERY relation instance of the offense must be disposed
                                        of explicitly as retain | suspend

No "is this relation affected by the suspension?" inference happens. Two earlier attempts at one
were rejected, and the fixtures show why both were unsound:

  * "suspend a relation whose endpoints are all inside suspended slots" -- in a result-crime
    attempt only the result side is suspended, yet `causal_nexus` must still disappear.
  * "suspend a relation whose leaf refs intersect a suspended slot" -- `derived_offense.
    robbery_homicide` suspends result+causation for 강도살인미수, and its `occasion_identity`
    relation must be RETAINED (강도의 기회에 살해행위가 있었을 것은 미수에서도 요구된다). A leaf
    intersection rule gets that backwards.

Since relation endpoints are relation-scoped *views* (axis 7), there is no leaf set that reliably
stands for an endpoint anyway. So the compiler detects structure and stops; the legal judgement of
whether a relation survives an incomplete form is authored, once per relation, by a human.

Independence: like every other axis this one assumes no other axis has run, calls
compile.compile_offense() itself, and skips entries that fail to compile (axes 2/6 own those).
"""

from __future__ import annotations

from collections.abc import Mapping

from idpr.v2 import compile, expressions
from idpr.v2.compile import CompiledOffense
from idpr.v2.expressions import SLOT_NAMES
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.relations import iter_relation_instances

_AXIS = "completion"

DERIVABLE_STATES: tuple[str, ...] = (
    "completed",
    "attempted",
    "abandoned_attempt",
    "impossible_attempt",
    "preparation",
)


def check_completion(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    memo: dict = {}
    in_progress: set = set()
    claimed: dict[str, str] = {}

    for entry in registry.by_kind.get("completion_policy", ()):
        findings.extend(_check_distinct_conditions(entry))
        offense_ref = entry.payload["offense"]
        if offense_ref in claimed:
            findings.append(Finding(
                _AXIS, "completion_policy_offense_already_governed", entry.id, "offense",
                f"{offense_ref!r} is already governed by {claimed[offense_ref]!r} -- an offense "
                "has at most one CompletionPolicyDef, otherwise the derivation has two sources",
            ))
        else:
            claimed[offense_ref] = entry.id

        states = entry.payload.get("states") or {}
        findings.extend(_check_states_declared(entry, states))

        compiled = compile.compile_offense(registry, offense_ref, memo=memo, in_progress=in_progress)
        if not isinstance(compiled, CompiledOffense):
            continue  # unresolved / cyclic / non-compiling offense -- owned by axes 1/2/6
        offense_entry = registry.get(offense_ref)
        for name, state in states.items():
            findings.extend(_check_state(entry, name, state, compiled, offense_entry))
    return findings


def _check_states_declared(entry: DefinitionEntry, states: Mapping[str, object]) -> list[Finding]:
    """`completed` must be authored explicitly.

    Deriving it as "whatever is left when no other state's condition holds" would be a default
    ordering -- a hidden priority in exactly the place section 14 forbids one. If completed is
    absent the policy also cannot describe an ordinary case at all.
    """
    if "completed" not in states:
        return [Finding(
            _AXIS, "completion_completed_state_missing", entry.id, "states",
            "no 'completed' state declared -- every offense with a completion policy must author "
            "its completed condition rather than leaving it as an implicit default",
        )]
    return []


def _check_state(
    entry: DefinitionEntry,
    name: str,
    state: Mapping[str, object],
    compiled: CompiledOffense,
    offense_entry: DefinitionEntry | None,
) -> list[Finding]:
    findings: list[Finding] = []
    path = f"states.{name}"
    suspends = tuple(state.get("suspends") or ())

    if name == "completed" and suspends:
        findings.append(Finding(
            _AXIS, "completion_completed_state_suspends", entry.id, f"{path}.suspends",
            f"the completed state suspends {list(suspends)!r} -- by definition it obligates every "
            "slot the offense authors",
        ))

    for slot in suspends:
        if slot not in SLOT_NAMES:
            findings.append(Finding(
                _AXIS, "completion_suspends_unknown_slot", entry.id, f"{path}.suspends",
                f"{slot!r} is not a fixed offense slot",
            ))
        elif compiled.slots.get(slot) is None:
            findings.append(Finding(
                _AXIS, "completion_suspends_unauthored_slot", entry.id, f"{path}.suspends",
                f"{slot!r} carries no obligation in {compiled.id!r}, so suspending it is a no-op "
                "-- most likely the wrong slot name or the wrong offense",
            ))
        else:
            contributors = _contributors_to_slot(offense_entry, compiled, slot)
            if len(contributors) > 1:
                findings.append(Finding(
                    _AXIS, "completion_unsupported_slot_suspension", entry.id, f"{path}.suspends",
                    f"{slot!r} in {compiled.id!r} is contributed to by more than one component "
                    f"({sorted(contributors)}), and suspending it removes ALL of them. "
                    "Occurrence-scoped suspension is not implemented, so there is no way to "
                    "express 'only this component's contribution is suspended' -- refusing rather "
                    "than silently running a program that drops the other components too",
                ))

    findings.extend(_check_component_scopes(entry, name, state, compiled, offense_entry))
    findings.extend(_check_relation_dispositions(
        entry, name, state, compiled, bool(suspends or state.get("component_suspends"))
    ))
    return findings


def _check_component_scopes(
    entry: DefinitionEntry,
    name: str,
    state: Mapping[str, object],
    compiled: CompiledOffense,
    offense_entry: DefinitionEntry | None,
) -> list[Finding]:
    """Validate explicitly authored component-local completion on a direct COMPOSE.

    Local keys never escape the governed derivation.  Only offense-family components may supply
    a predicate view or have their slot contribution suspended; primitive and bundle components
    remain unavailable as independent completion programs.
    """
    when_scope = state.get("when_component")
    suspensions = tuple(state.get("component_suspends") or ())
    if not when_scope and not suspensions:
        return []

    findings: list[Finding] = []
    derivation = (offense_entry.payload.get("derivation") or {}) if offense_entry else {}
    if derivation.get("kind") != "compose":
        return [Finding(
            _AXIS, "component_completion_scope_not_direct_compose", entry.id, f"states.{name}",
            "component-local completion requires a direct COMPOSE derivation",
        )]

    offense_components = {
        component.local_key: component
        for component in compiled.components
        if component.component_kind == "offense"
        and component.resolved_kind in ("offense", "derived_offense")
    }
    def validate(scope: Mapping[str, object], field_path: str):
        component = offense_components.get(scope["local_key"])
        if component is None or component.source_ref != scope["offense"]:
            findings.append(Finding(
                _AXIS, "component_completion_scope_unresolved", entry.id, field_path,
                f"({scope['local_key']!r}, {scope['offense']!r}) is not an offense-family component",
            ))
        return component

    if when_scope:
        validate(when_scope, f"states.{name}.when_component")

    seen_local_keys: set[str] = set()
    for index, suspension in enumerate(suspensions):
        path = f"states.{name}.component_suspends[{index}]"
        component = validate(suspension, path)
        local_key = suspension["local_key"]
        if local_key in seen_local_keys:
            findings.append(Finding(
                _AXIS, "component_suspension_duplicate_local_key", entry.id, path,
                f"{local_key!r} is suspended more than once in the same completion state",
            ))
        seen_local_keys.add(local_key)
        if component is None:
            continue
        for slot in suspension["slots"]:
            if component.compiled_content.slots.get(slot) is None:
                findings.append(Finding(
                    _AXIS, "component_suspension_unauthored_slot", entry.id, f"{path}.slots",
                    f"{slot!r} has no contribution from {local_key!r}",
                ))
    return findings


def _contributors_to_slot(
    offense_entry: DefinitionEntry | None, compiled: CompiledOffense, slot: str
) -> list[str]:
    """Which COMPOSE components put an obligation into `slot`, by local_key.

    Structure only -- this never decides anything, it just tells `_check_state` when a suspension
    would silently take out more than the author could have meant. Non-COMPOSE offenses have a
    single authoring source by construction, so they return a single sentinel contributor.
    """
    derivation = (offense_entry.payload.get("derivation") or {}) if offense_entry else {}
    if derivation.get("kind") != "compose":
        return [compiled.id]

    nested = {
        instance.local_key: instance.compiled_content
        for instance in compiled.components
        if instance.component_kind == "offense"
    }
    contributors = []
    for component in derivation["components"]:
        local_key = component["local_key"]
        kind = component["kind"]
        if kind == "offense":
            content = nested.get(local_key)
            contributes = content is not None and content.slots.get(slot) is not None
        elif kind == "bundle":
            contributes = slot in (component.get("placement") or {}).values()
        else:  # primitive | exported_component -- a single authored slot
            contributes = component.get("slot") == slot
        if contributes:
            contributors.append(local_key)
    return contributors


def _check_relation_dispositions(
    entry: DefinitionEntry,
    name: str,
    state: Mapping[str, object],
    compiled: CompiledOffense,
    suspends_anything: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    path = f"states.{name}.relations"
    authored = state.get("relations") or ()

    instances = {
        (key.occurrence_path[1:], key.relation_ref, key.left_local_key, key.right_local_key): key
        for key, _binding in iter_relation_instances(compiled)
    }

    seen: set[tuple] = set()
    for index, item in enumerate(authored):
        signature = (tuple(item.get("path") or ()), item["relation"], item["left"], item["right"])
        if signature not in instances:
            findings.append(Finding(
                _AXIS, "completion_relation_disposition_unresolved", entry.id, f"{path}[{index}]",
                f"no relation instance of {compiled.id!r} matches "
                f"(path={list(signature[0])!r}, relation={signature[1]!r}, left={signature[2]!r}, "
                f"right={signature[3]!r})",
            ))
        elif signature in seen:
            findings.append(Finding(
                _AXIS, "completion_relation_disposition_duplicate", entry.id, f"{path}[{index}]",
                f"relation instance {signature[1]!r} ({signature[2]!r}, {signature[3]!r}) is "
                "disposed of twice in this state",
            ))
        seen.add(signature)

    if suspends_anything:
        for signature in instances:
            if signature not in seen:
                findings.append(Finding(
                    _AXIS, "completion_relation_disposition_missing", entry.id, path,
                    f"state {name!r} suspends slot obligations but leaves relation "
                    f"{signature[1]!r} ({signature[2]!r}, {signature[3]!r}) undisposed -- whether "
                    "a relation survives an incomplete form is a legal judgement this checker "
                    "will not make for you; declare retain or suspend",
                ))
    return findings


def _check_distinct_conditions(entry: DefinitionEntry) -> list[Finding]:
    """Duplicate `when` conditions across two states of one policy.

    This is the *only* static overlap check, on purpose. General overlap is undecidable, and the
    runtime already handles it honestly (two conditions TRUE at once -> `unresolved`, both recorded
    in provenance, no winner picked). What is worth catching statically is the degenerate case
    where two states are literally indistinguishable, because that one can never produce anything
    but `unresolved` and is always an authoring slip.
    """
    findings: list[Finding] = []
    by_condition: dict[object, str] = {}
    for name in DERIVABLE_STATES:
        state = (entry.payload.get("states") or {}).get(name)
        if state is None:
            continue
        canonical = expressions.canonicalize(state.get("when"))
        previous = by_condition.get(canonical)
        if previous is not None:
            findings.append(Finding(
                _AXIS, "completion_duplicate_state_condition", entry.id, f"states.{name}.when",
                f"identical `when` to state {previous!r} -- these two states can never be told "
                "apart, so the derivation can only ever return 'unresolved'",
            ))
        else:
            by_condition[canonical] = name
    return findings
