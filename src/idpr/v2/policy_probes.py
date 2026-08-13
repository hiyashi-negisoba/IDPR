"""authored policy -> required typed inputs, as one generic compiler.

This exists because of a failure mode we hit twice. `DoctrineDef` was fully authored and fully
wired into Scallop, and active doctrine was nevertheless 0 for every case -- activation needed a
non-UNKNOWN leaf, and no doctrine leaf was ever planned as a target. The definition was there, the
runtime was there, and nobody asked the question. `mistake_policy`, `excess_policy` and
`aggravating_status_participation` were each about to reproduce it.

The obvious fix -- a planner branch per policy -- reproduces the *shape* of the bug instead: every
new policy needs someone to remember to add its branch, and forgetting is silent. So the
requirement moves into the authored definition (`probe`), and the planner reads it without knowing
any policy's legal content. Adding a policy kind here means registering one accessor, not writing
new planner logic.

What this module does not do: decide whether a policy applies to a given case, supply any value, or
guess an identity that is missing. It answers one question -- "what would this policy need in order
to run here?" -- and names the marker to record when the answer cannot be supplied.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

OFFENSE_INSTANCE = "offense_instance"
PARTICIPATION_CANDIDATE = "participation_candidate"

NEURAL_PREDICATE = "neural_predicate"
STRUCTURAL_RELATION = "structural_relation"
PROVENANCE = "provenance"

_PROVENANCE_PREFIX = "provenance."


class PolicyProbeError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ProbeRequirement:
    """One typed input a policy needs before it can run."""

    policy_id: str
    applies_to: str
    ref: str
    supply: str
    optional: bool
    unresolved_marker: str
    candidate_offense_refs: tuple[str, ...] = ()
    """이 요구가 붙는 후보의 exact offense refs. 비어 있으면 후보 종류로 제한하지 않는다.

    이 두 필드가 있어야 planner가 "이 사건에 이 정책이 붙을 자리가 있는가"를 물을 수 있다.
    없으면 살인 참가 후보가 하나도 없는 사건에서도 존속살해 신분을 target으로 열거나, 반대로
    열지 않은 채 공백 marker만 찍게 된다 -- 둘 다 틀렸다.

    compiler는 이 값을 해석하지 않는다. 정책이 어디에 붙는지는 저작이 정하고 여기서는
    나르기만 한다.
    """

    candidate_modes: tuple[str, ...] = ()
    """이 요구가 붙는 참가 mode. 비어 있으면 mode로 제한하지 않는다."""

    @property
    def is_neural_target(self) -> bool:
        """True when the planner must open an ordinary Call 2 target for this ref.

        Note this is the *only* thing that costs a model call. `structural_relation` is read off
        bindings and `provenance` is carried from an upstream stage, so declaring a policy does not
        by itself widen neural load.
        """
        return self.supply == NEURAL_PREDICATE


def _probe_blocks(
    entry: DefinitionEntry,
) -> tuple[tuple[Mapping[str, Any], tuple[str, ...], tuple[str, ...]], ...]:
    """Every `probe` block this definition carries, with the candidate scope it is authored in.

    Policy kinds put it at the top level; `aggravating_status_participation` is nested inside an
    offense because it is authored on the aggravated offense rather than standing alone. That
    nesting is also where the scope lives -- the proviso names the base offense and the modes it
    reaches -- so the accessor that knows the shape reads it out here and the rest of the module
    stays legally blind.
    """
    if entry.kind in {"mistake_policy", "excess_policy"}:
        return ((entry.payload["probe"], (), ()),)
    if entry.kind == "offense":
        proviso = (entry.payload.get("participation_constraints") or {}).get(
            "aggravating_status_participation"
        )
        if not proviso:
            return ()
        return (
            (
                proviso["probe"],
                (str(proviso["base_offense_ref"]),),
                tuple(str(value) for value in proviso["applies_to_modes"]),
            ),
        )
    return ()


def probe_requirements(
    registry: DefinitionRegistry,
    *,
    applies_to: str | None = None,
) -> tuple[ProbeRequirement, ...]:
    """Every authored requirement, optionally narrowed to one kind of case-time object."""
    if applies_to is not None and applies_to not in {OFFENSE_INSTANCE, PARTICIPATION_CANDIDATE}:
        raise PolicyProbeError(f"unknown probe target kind: {applies_to!r}")
    output: list[ProbeRequirement] = []
    for entry in registry.by_id.values():
        for probe, offense_refs, modes in _probe_blocks(entry):
            if applies_to is not None and probe["applies_to"] != applies_to:
                continue
            for requirement in probe["requires"]:
                output.append(
                    ProbeRequirement(
                        policy_id=entry.id,
                        applies_to=probe["applies_to"],
                        ref=requirement["ref"],
                        supply=requirement["supply"],
                        optional=bool(requirement.get("optional", False)),
                        unresolved_marker=probe["unresolved_marker"],
                        candidate_offense_refs=offense_refs,
                        candidate_modes=modes,
                    )
                )
    return tuple(sorted(output, key=lambda item: (item.policy_id, item.ref)))


def neural_target_refs(
    registry: DefinitionRegistry, *, applies_to: str | None = None
) -> tuple[str, ...]:
    """The predicate refs the planner must materialize as Call 2 targets, de-duplicated."""
    refs = {
        requirement.ref
        for requirement in probe_requirements(registry, applies_to=applies_to)
        if requirement.is_neural_target
    }
    return tuple(sorted(refs))


def unsatisfied_requirements(
    registry: DefinitionRegistry,
    available_refs: Iterable[str],
    *,
    applies_to: str | None = None,
) -> tuple[ProbeRequirement, ...]:
    """Required inputs that nothing supplies -- each one a representation gap, not a FALSE.

    Optional requirements are excluded: a policy that branches without them is not broken by their
    absence, and reporting them would bury the real gaps.
    """
    available = frozenset(available_refs)
    return tuple(
        requirement
        for requirement in probe_requirements(registry, applies_to=applies_to)
        if not requirement.optional and requirement.ref not in available
    )


def validate_probe_refs(registry: DefinitionRegistry) -> tuple[str, ...]:
    """Authoring errors in probe blocks: a ref that resolves to nothing or to the wrong kind.

    `provenance.*` refs are exempt -- they name a value an upstream stage carries, not a definition,
    and requiring them to exist in the registry would force fake definitions for pipeline plumbing.
    """
    errors: list[str] = []
    for requirement in probe_requirements(registry):
        if requirement.supply == PROVENANCE:
            if not requirement.ref.startswith(_PROVENANCE_PREFIX):
                errors.append(
                    f"{requirement.policy_id}: provenance requirement {requirement.ref!r} must "
                    f"start with {_PROVENANCE_PREFIX!r}"
                )
            continue
        kind = registry.kind_of(requirement.ref)
        if kind is None:
            errors.append(f"{requirement.policy_id}: {requirement.ref!r} does not exist")
            continue
        expected = (
            {"relation"}
            if requirement.supply == STRUCTURAL_RELATION
            else {"ground_fact", "legal_element"}
        )
        if kind not in expected:
            errors.append(
                f"{requirement.policy_id}: {requirement.ref!r} is kind={kind!r}, "
                f"expected one of {sorted(expected)} for supply={requirement.supply!r}"
            )
    return tuple(errors)


__all__ = [
    "NEURAL_PREDICATE",
    "OFFENSE_INSTANCE",
    "PARTICIPATION_CANDIDATE",
    "PROVENANCE",
    "STRUCTURAL_RELATION",
    "PolicyProbeError",
    "ProbeRequirement",
    "neural_target_refs",
    "probe_requirements",
    "unsatisfied_requirements",
    "validate_probe_refs",
]
