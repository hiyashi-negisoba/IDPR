"""Axis 3: stage/effect typing.

The stage == effect.stage invariant is already schema-enforced (doctrine_def.schema.json's
if/then), so nothing to re-check there. No ModifierDef registry object exists yet (Open Question
#4, deliberately still open), so `modifier_ref` can't be resolved against a real declared object.
The only thing checkable now: the same modifier_ref string must always pair with the same stage
across every MODIFY doctrine -- catches a copy-paste-onto-wrong-stage bug.
"""

from __future__ import annotations

from idpr.v2.findings import Finding
from idpr.v2.registry import DefinitionRegistry

_AXIS = "stage_effect"


def check_stage_effect(registry: DefinitionRegistry) -> list[Finding]:
    findings: list[Finding] = []
    seen: dict[str, tuple[str, str]] = {}  # modifier_ref -> (stage, doctrine_id)

    for entry in registry.by_kind.get("doctrine", ()):
        effect = entry.payload["effect"]
        if effect["effect"] != "MODIFY":
            continue
        modifier_ref = effect["modifier_ref"]
        stage = effect["stage"]
        if modifier_ref in seen:
            prior_stage, prior_doctrine = seen[modifier_ref]
            if prior_stage != stage:
                findings.append(Finding(
                    _AXIS,
                    "modifier_ref_stage_inconsistent",
                    entry.id,
                    "effect.modifier_ref",
                    f"{modifier_ref!r} used at stage={stage!r} here but stage={prior_stage!r} in {prior_doctrine!r}",
                ))
        else:
            seen[modifier_ref] = (stage, entry.id)
    return findings
