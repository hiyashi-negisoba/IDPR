"""Shared participation logic (build-order step 6C) -- Definition Layer, case-blind.

Mirrors `relations.py`'s role: logic consumed by both a `checks/` axis
(`checks/participation.py`, axis 5) and the runtime (`runtime/participation.py`). Extracted rather
than duplicated, same precedent as Step 4 hoisting `replay_slot` out of `checks/operators.py` into
`compile.py` -- `checks/participation.py` becomes a thin consumer of `effective_attributable_slots`
instead of recomputing it, and the runtime's ATTRIBUTE view merge (decision #1) needs the exact same
answer to "which slots does this offense allow attribution on" that axis 5 already validates.
"""

from __future__ import annotations

from idpr.v2.registry import DefinitionEntry, DefinitionRegistry


def participation_policy_for(registry: DefinitionRegistry) -> DefinitionEntry | None:
    """The single shared ParticipationPolicyDef, or None if the corpus has none yet.

    Mirrors `completion.completion_policy_for()`. Axis 5 already enforces that at most one exists
    (`multiple_participation_policies`), so by the time runtime code calls this the checks have
    passed and "more than one" cannot occur."""
    policies = registry.by_kind.get("participation_policy", ())
    return policies[0] if len(policies) == 1 else None


def effective_attributable_slots(policy: DefinitionEntry, offense: DefinitionEntry) -> frozenset[str]:
    """Which fixed slots this offense allows co-principal ATTRIBUTE on.

    Precedence, all offense-local override before the shared policy default:
      1. `co_principal` disabled for this offense (via `participation_constraints.disabled_modes`)
         -> none, regardless of anything else.
      2. This offense's own `participation_constraints.attributable_slots` override, if given.
      3. The shared policy's `modes.co_principal.attributable_slots` default.
      4. No `co_principal` mode declared at all -> none.
    """
    modes = policy.payload.get("modes") or {}
    constraints = offense.payload.get("participation_constraints") or {}
    disabled_modes = frozenset(constraints.get("disabled_modes") or ())
    if "co_principal" in disabled_modes:
        return frozenset()
    if constraints.get("attributable_slots") is not None:
        return frozenset(constraints["attributable_slots"])
    if "co_principal" in modes:
        return frozenset(modes["co_principal"].get("attributable_slots") or ())
    return frozenset()


def constitutive_status_refs(offense: DefinitionEntry) -> frozenset[str]:
    """Article 33-only status leaves whose Elements truth comes from a co-principal obligation.

    There is deliberately no shared-policy default: every affected offense opts in with its own
    frozen status leaf, and all other co-principal cases keep ordinary attribution semantics.
    """
    constraints = offense.payload.get("participation_constraints") or {}
    return frozenset(constraints.get("constitutive_status_refs") or ())


def co_principal_established_predicate_refs(
    policy: DefinitionEntry,
) -> frozenset[str]:
    """Facts entailed by the validated co-principal relation itself."""
    modes = policy.payload.get("modes") or {}
    co_principal = modes.get("co_principal") or {}
    return frozenset(co_principal.get("establishes_predicate_refs") or ())


def derivative_mode_subsumptions(
    policy: DefinitionEntry,
) -> dict[str, frozenset[str]]:
    """Authored derivative-mode precedence for one logical participation edge."""
    result: dict[str, set[str]] = {}
    for rule in policy.payload.get("mode_subsumptions") or ():
        result.setdefault(str(rule["dominant_mode"]), set()).update(
            str(mode) for mode in rule.get("subsumed_modes") or ()
        )
    return {mode: frozenset(subsumed) for mode, subsumed in result.items()}


def _expression_refs(expression: object) -> set[str]:
    if not isinstance(expression, dict):
        return set()
    if expression.get("op") == "ref":
        ref = expression.get("ref")
        return {str(ref)} if ref else set()
    output: set[str] = set()
    for value in expression.values():
        if isinstance(value, dict):
            output |= _expression_refs(value)
        elif isinstance(value, list):
            for item in value:
                output |= _expression_refs(item)
    return output


def derivative_mode_required_predicate_refs(
    policy: DefinitionEntry,
) -> dict[str, frozenset[str]]:
    """가담자 자신에게서 확인해야 하는 요소 -- 교사의 고의, 방조의 고의.

    co_principal은 `establishes_predicate_refs`로 관계가 사실을 *공급*하지만, derivative mode는
    `requires`로 사실을 *요구*한다. 요구된 predicate를 아무도 묻지 않으면 그 mode는 어떤 진리값
    배정으로도 성립할 수 없다. 그래서 이 목록은 planner가 target을 여는 근거가 된다.
    """
    output: dict[str, frozenset[str]] = {}
    for mode, payload in (policy.payload.get("modes") or {}).items():
        if not isinstance(payload, dict) or payload.get("basis") != "derivative":
            continue
        refs = _expression_refs(payload.get("requires"))
        if refs:
            output[str(mode)] = frozenset(refs)
    return output


__all__ = [
    "co_principal_established_predicate_refs",
    "derivative_mode_required_predicate_refs",
    "constitutive_status_refs",
    "derivative_mode_subsumptions",
    "effective_attributable_slots",
    "participation_policy_for",
]
