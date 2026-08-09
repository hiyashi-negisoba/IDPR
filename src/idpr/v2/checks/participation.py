"""Axis 5: participation dependency typing, Definition-Layer-only.

No case/runtime data exists yet, so the real 15.4 TYPE ERROR ("instigation requires
OffenseRealization<X> but only ElementsResult<X> is available") is step 6-8's job, out of scope
here. What IS checkable at this layer:
  - at most one ParticipationPolicyDef may exist (it's offense-agnostic/shared by design --
    nothing else pins which policy governs which offense, so a second instance is ambiguous).
  - participation_constraints without any policy to constrain is a dangling override.
  - disabled_modes must name modes the sole policy actually declares.
  - attributable_slots (explicit override, or inherited from the policy's default
    co_principal.attributable_slots when co_principal isn't disabled) must name slots this
    offense's own elements actually declares.
"""

from __future__ import annotations

from idpr.v2 import participation
from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "participation"


def check_participation(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    policies = registry.by_kind.get("participation_policy", ())
    offenses = registry.by_kind.get("offense", ())

    if len(policies) > 1:
        ids = sorted(policy.id for policy in policies)
        for policy in policies:
            findings.append(Finding(
                _AXIS, "multiple_participation_policies", policy.id, "$",
                f"more than one ParticipationPolicyDef exists: {ids}",
            ))

    policy = participation.participation_policy_for(registry)

    if policy is None:
        for entry in offenses:
            if entry.payload.get("participation_constraints"):
                findings.append(Finding(
                    _AXIS, "participation_constraints_without_policy", entry.id, "participation_constraints",
                    "participation_constraints given but no single ParticipationPolicyDef exists to constrain",
                ))
        return findings

    modes = policy.payload.get("modes") or {}
    for entry in offenses:
        constraints = entry.payload.get("participation_constraints") or {}
        disabled_modes = frozenset(constraints.get("disabled_modes") or [])
        for mode in disabled_modes:
            if mode not in modes:
                findings.append(Finding(
                    _AXIS, "disabled_mode_undeclared", entry.id, "participation_constraints.disabled_modes",
                    f"mode {mode!r} is not declared in {policy.id!r}'s modes",
                ))

        if "co_principal" in disabled_modes:
            field_path = "participation_constraints.disabled_modes"
        elif constraints.get("attributable_slots") is not None:
            field_path = "participation_constraints.attributable_slots"
        elif "co_principal" in modes:
            field_path = f"<inherited from {policy.id}.modes.co_principal.attributable_slots>"
        else:
            field_path = ""

        # Single source for the actual slot list: idpr.v2.participation, also used by
        # runtime/participation.py's ATTRIBUTE view merge (decision #1). `field_path` above stays
        # local -- it's Finding-message presentation, not shared semantics.
        effective_attributable_slots = participation.effective_attributable_slots(policy, entry)

        elements = entry.payload.get("elements") or {}
        for slot in effective_attributable_slots:
            if elements.get(slot) is None:
                findings.append(Finding(
                    _AXIS, "attributable_slot_not_declared", entry.id, field_path,
                    f"slot {slot!r} is not declared in this offense's own elements",
                ))
    return findings
