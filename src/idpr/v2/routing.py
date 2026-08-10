"""Step 8 Call 1's closed offense-seed router contract.

The router sees case text and a catalog generated from the loaded Definition
Layer.  It returns an ordered seed list only; it never extracts case facts or
assigns legal effects.  The order is preserved because the pilot compares the
first ten emitted candidates with the full fifteen-candidate budget.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from idpr.v2.registry import DefinitionRegistry


MAX_SEEDS_PER_CASE = 15
_OFFENSE_KINDS = frozenset({"offense", "derived_offense"})


class RouterContractError(ValueError):
    """The model response is outside the closed Call 1 contract."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class RouterCatalogEntry:
    """One Definition Layer candidate shown to the router.

    A DerivedOffenseDef currently has no authored ``identity`` field.  Its
    canonical id is therefore its display value and it carries no invented
    statute metadata.  This keeps the catalog source-derived rather than
    reintroducing a parallel legal-name map.
    """

    definition_id: str
    kind: str
    display_name: str
    statutory_refs: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "definition_id": self.definition_id,
            "kind": self.kind,
            "display_name": self.display_name,
            "statutory_refs": list(self.statutory_refs),
        }


def router_catalog(registry: DefinitionRegistry) -> tuple[RouterCatalogEntry, ...]:
    """Return the deterministic closed Call 1 catalog from the registry alone."""
    entries: list[RouterCatalogEntry] = []
    for kind in sorted(_OFFENSE_KINDS):
        for entry in registry.by_kind.get(kind, ()):
            identity = entry.payload.get("identity")
            if isinstance(identity, Mapping):
                name = identity.get("name")
                statutory_refs = identity.get("statutory_refs")
            else:
                name = None
                statutory_refs = None
            entries.append(
                RouterCatalogEntry(
                    definition_id=entry.id,
                    kind=entry.kind,
                    display_name=name if isinstance(name, str) else entry.id,
                    statutory_refs=tuple(
                        ref for ref in (statutory_refs or ()) if isinstance(ref, str)
                    ),
                )
            )
    return tuple(sorted(entries, key=lambda entry: entry.definition_id))


def router_schema(catalog: Iterable[RouterCatalogEntry]) -> dict[str, Any]:
    """JSON Schema for an ordered, non-duplicated closed seed list."""
    ids = [entry.definition_id for entry in catalog]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["seeds"],
        "properties": {
            "seeds": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_SEEDS_PER_CASE,
                "uniqueItems": True,
                "items": {"type": "string", "enum": ids},
            }
        },
    }


def router_request_payload(
    *, case_text: str, catalog: Iterable[RouterCatalogEntry]
) -> dict[str, Any]:
    """The complete model input: raw case text and the closed definition catalog."""
    return {
        "case_text": case_text,
        "offense_catalog": [entry.as_dict() for entry in catalog],
    }


def validate_router_output(
    payload: Mapping[str, Any], *, catalog: Iterable[RouterCatalogEntry]
) -> tuple[str, ...]:
    """Validate and preserve the exact model-emitted seed order.

    Duplicate entries are a hard failure, even though JSON Schema guided
    decoding also declares ``uniqueItems``.  Silently deduplicating would alter
    both candidate rank and the ten-vs-fifteen pilot measurement.
    """
    errors: list[str] = []
    unexpected = sorted(set(payload) - {"seeds"})
    if unexpected:
        errors.append(f"unexpected output fields: {unexpected}")
    if "seeds" not in payload:
        errors.append("seeds is required")
        raise RouterContractError(errors)

    raw_seeds = payload["seeds"]
    if not isinstance(raw_seeds, list):
        errors.append("seeds must be an array")
        raise RouterContractError(errors)
    if not raw_seeds:
        errors.append("seeds must contain at least one definition id")
    if len(raw_seeds) > MAX_SEEDS_PER_CASE:
        errors.append(f"seeds must contain at most {MAX_SEEDS_PER_CASE} definition ids")

    allowed = {entry.definition_id for entry in catalog}
    seen: set[str] = set()
    seeds: list[str] = []
    for index, seed in enumerate(raw_seeds):
        where = f"seeds[{index}]"
        if not isinstance(seed, str):
            errors.append(f"{where} must be a string")
            continue
        if seed in seen:
            errors.append(f"{where} duplicates earlier seed {seed!r}")
            continue
        seen.add(seed)
        if seed not in allowed:
            errors.append(f"{where} is not a closed offense definition id: {seed!r}")
            continue
        seeds.append(seed)

    if errors:
        raise RouterContractError(errors)
    return tuple(seeds)


__all__ = [
    "MAX_SEEDS_PER_CASE",
    "RouterCatalogEntry",
    "RouterContractError",
    "router_catalog",
    "router_request_payload",
    "router_schema",
    "validate_router_output",
]
