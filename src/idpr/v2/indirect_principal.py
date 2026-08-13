"""Definition-layer scope for indirect-principal grounding.

Capability authoring answers only whether an offense can legally take an indirect-principal
form in at least one factual configuration.  It deliberately does not answer whether that form
exists in the current case.  The latter belongs to a typed utilization relation plus the utilised
participant's runtime outcome.
"""

from __future__ import annotations

from idpr.v2.registry import DefinitionRegistry


def has_authored_indirect_principal_capability(
    registry: DefinitionRegistry,
    offense_ref: str,
) -> bool:
    """Return the explicit positive authoring bit for one exact offense.

    There is intentionally no inheritance across QUALIFY/COMPOSE derivations and no fallback to
    card prose, issue tags, statutory references, or participation defaults.  An absent field is
    outside the authored candidate scope; it is not a negative legal conclusion.
    """

    entry = registry.get(offense_ref)
    if entry is None or entry.kind not in {"offense", "derived_offense"}:
        return False
    capability = entry.payload.get("indirect_principal_capability")
    return isinstance(capability, dict) and capability.get("legally_possible") is True


__all__ = ["has_authored_indirect_principal_capability"]
