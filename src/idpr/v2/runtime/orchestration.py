"""Step 7 caller/orchestration adapters over compiled structural candidates.

The adapters distinguish mandatory-active offenses from discovered candidates.
A caller must explicitly report a candidate probe as conditionally active only
after it survives. The adapters then delegate legal evaluation to the existing
dedicated runtimes; they do not select actors, modes, target offenses, or legal
truths.
"""

from __future__ import annotations

from typing import Iterable, Mapping

from idpr.v2.closure import ClosureResult
from idpr.v2.compile import CompiledOffense
from idpr.v2 import expressions
from idpr.v2.evaluate import TRUE, evaluate
from idpr.v2.participation import participation_policy_for
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation import DerivativeMode, resolve_derivative_liability
from idpr.v2.runtime.stages import LiabilityEvaluation
from idpr.v2.runtime.statutory import resolve_article_263_deemed_liability
from idpr.v2.runtime.truths import CaseTruths


class OrchestrationError(ValueError):
    """A caller supplied a route outside the active, compiled Step 7 set."""


def resolve_cross_offense_derivative_route(
    registry: DefinitionRegistry,
    closure: ClosureResult,
    compiled_candidates: Mapping[str, CompiledOffense],
    mode: DerivativeMode,
    principal: LiabilityEvaluation,
    target: OffenseInstanceKey,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
    *,
    conditionally_active_offense_refs: Iterable[str] = (),
) -> LiabilityEvaluation:
    """Run C-33b's caller-selected derivative route without a graph edge.

    Both offense refs must independently be mandatory-active or caller-reported
    conditionally active after their probes survive, and must be compiled. They
    need not be the same, and no principal-to-target derivation relation is
    inferred. The participation runtime remains the sole owner of derivative
    liability.
    """
    active_offense_refs = _active_offense_refs(closure, conditionally_active_offense_refs)
    _require_active_compiled(active_offense_refs, compiled_candidates, principal.instance.offense_ref, "principal")
    _require_active_compiled(active_offense_refs, compiled_candidates, target.offense_ref, "target")
    policy = participation_policy_for(registry)
    if policy is None:
        raise OrchestrationError("cross-offense derivative route requires the shared participation policy")
    return resolve_derivative_liability(registry, policy, mode, principal, target, active, truths)


def resolve_article_263_from_participation_probe(
    registry: DefinitionRegistry,
    closure: ClosureResult,
    compiled_candidates: Mapping[str, CompiledOffense],
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
    *,
    conditionally_active_offense_refs: Iterable[str] = (),
) -> LiabilityEvaluation | None:
    """Delegate a surviving Article 263 probe to its existing dedicated runtime.

    `None` means the statutory-deeming probe is not positively alive yet.  This
    is neither an attribution fallback nor an `offense_ref=263` evaluation;
    unresolved evidence remains available to the caller for later grounding.
    """
    active_offense_refs = _active_offense_refs(closure, conditionally_active_offense_refs)
    _require_active_compiled(active_offense_refs, compiled_candidates, instance.offense_ref, "statutory-deeming target")
    offense = registry.get(instance.offense_ref)
    constraints = (offense.payload.get("participation_constraints") or {}) if offense else {}
    statutory_deeming = constraints.get("statutory_deeming")
    if statutory_deeming is None:
        raise OrchestrationError(
            f"{instance.offense_ref!r} has no approved statutory_deeming participation constraint"
        )
    if evaluate(expressions.canonicalize(statutory_deeming["requires"]), truths.predicate_view(instance)) != TRUE:
        return None
    return resolve_article_263_deemed_liability(
        registry, compiled_candidates[instance.offense_ref], instance, completion, active, truths
    )


def _active_offense_refs(
    closure: ClosureResult,
    conditionally_active_offense_refs: Iterable[str],
) -> frozenset[str]:
    conditional = frozenset(conditionally_active_offense_refs)
    unexpected = conditional - closure.candidate_offense_refs
    if unexpected:
        raise OrchestrationError(
            f"conditionally active refs were not discovered Step 7 candidates: {sorted(unexpected)!r}"
        )
    return closure.mandatory_offense_refs | conditional


def _require_active_compiled(
    active_offense_refs: frozenset[str],
    compiled_candidates: Mapping[str, CompiledOffense],
    ref: str,
    label: str,
) -> None:
    if ref not in active_offense_refs:
        raise OrchestrationError(
            f"{label} offense {ref!r} is neither mandatory-active nor a conditionally active survivor"
        )
    if ref not in compiled_candidates:
        raise OrchestrationError(f"{label} offense {ref!r} is not in the compiled candidate set")


__all__ = [
    "OrchestrationError",
    "resolve_article_263_from_participation_probe",
    "resolve_cross_offense_derivative_route",
]
