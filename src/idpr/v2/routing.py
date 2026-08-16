"""Step 8 Call 1's closed offense-seed router contract.

The router sees case text and a catalog generated from the loaded Definition
Layer.  It returns an ordered seed list only; it never extracts case facts or
assigns legal effects.  The completed pilot preserved rank to compare its first
ten candidates with the 15-cap calibration budget; production Call 1 is frozen
at ten normalized candidates.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.registry import DefinitionRegistry

MAX_SEEDS_PER_CASE = 10
"""Routing budget, counted in **distinct** offense refs.

A repeated ref names the same Definition type and therefore adds no seed
information, so it must not consume budget.  The raw array is bounded
separately by :data:`MAX_RAW_SEED_ITEMS`.
"""

MAX_RAW_SEED_ITEMS = 2 * MAX_SEEDS_PER_CASE
"""Slack bound on the raw array so duplicates cannot crowd out distinct refs.

``uniqueItems`` in the schema is only a generation hint and the guidance
backend does not enforce it: an observed Call 1 response filled six of ten
slots with one repeated ref, which silently cut that case's budget to four.
The bound stays finite so a degenerate response still fails the contract
instead of running unbounded.
"""

_OFFENSE_KINDS = frozenset({"offense", "derived_offense"})


class RouterContractError(ValueError):
    """The model response is outside the closed Call 1 contract."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class RouterSeedNormalization:
    """Auditable stable-unique projection of a valid raw router seed array.

    Call 1 seeds name Definition types, not case-time offense occurrences.  A
    later occurrence of an already valid canonical ref therefore adds no seed
    information.  The raw array remains available for model-behavior audit;
    downstream closure and ranked-cap measurement use ``normalized_seeds``.
    """

    raw_seeds: tuple[str, ...]
    normalized_seeds: tuple[str, ...]
    duplicate_refs: tuple[str, ...]

    @property
    def normalization_applied(self) -> bool:
        return bool(self.duplicate_refs)


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


def router_catalog_fingerprint(catalog: Iterable[RouterCatalogEntry]) -> str:
    """Hash exactly the catalog metadata visible to the frozen Call 1 router."""
    encoded = json.dumps(
        [entry.as_dict() for entry in catalog],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def router_schema(catalog: Iterable[RouterCatalogEntry]) -> dict[str, Any]:
    """JSON Schema for an ordered closed seed list.

    ``uniqueItems`` remains a generation hint.  Host semantics do not rely on
    every vLLM structured-output backend enforcing it: valid duplicate refs are
    recorded and normalized explicitly below.

    ``maxItems`` therefore bounds the *raw* array, not the routing budget.  If
    it were the budget, an unenforced ``uniqueItems`` would let repeated refs
    consume slots that distinct candidates never get to use.
    """
    ids = [entry.definition_id for entry in catalog]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["seeds"],
        "properties": {
            "seeds": {
                "type": "array",
                "minItems": 1,
                "maxItems": MAX_RAW_SEED_ITEMS,
                "uniqueItems": True,
                "items": {"type": "string", "enum": ids},
            },
        },
    }


QUESTION_ROUTING = "question_actors"
LINKED_OFFENDER_ROUTING = "linked_offender"


@dataclass(frozen=True)
class RouteRequest:
    """One invocation of ROUTE(actor, factual_scope, offense_catalog).

    Call 1 was written as "the stage that runs once at the beginning", but what it actually does
    is an operation: given whose conduct is in scope and which text bounds that scope, choose
    offense candidates from the closed catalog.  Nothing in it is specific to the actors the
    question happens to name.

    That matters because a legal rule can require another participant's own outcome -- Article
    151's object, and the same shape recurs in Articles 33 and 34.  The alternative designs were
    both worse: widening the first invocation would make one call do two different atomic tasks
    (route the asked actors, and re-find an offender it has not bound yet), and a dedicated
    Article 151 call would grow a pipeline stage for one article.  So the operation is reused
    instead, after Call 1.5 has bound the participant as a fact.

    `routed_actor_ids` is never chosen by a model at this point.  For the first invocation it is
    the question's actors; for a dependency invocation it is the participant Call 1.5 bound.
    """

    routed_actor_ids: tuple[str, ...]
    factual_scope_text: str
    routing_basis: str = QUESTION_ROUTING
    question_prompt: str | None = None
    """The original sub-question, kept only for the question-actor invocation.

    A dependency invocation deliberately has none: the question does not ask about this person,
    and passing it would re-scope the routing back onto the asked actors.
    """


def route_request_payload(
    request: RouteRequest, *, case_text: str, catalog: Iterable[RouterCatalogEntry]
) -> dict[str, Any]:
    """Serialize one ROUTE invocation for the router prompt."""
    if not request.routed_actor_ids or not all(
        value.strip() for value in request.routed_actor_ids
    ):
        raise RouterContractError(["routed_actor_ids must be non-empty labels"])
    if not request.factual_scope_text.strip():
        raise RouterContractError(["factual_scope_text must be a non-empty string"])
    if request.routing_basis == QUESTION_ROUTING and not (request.question_prompt or "").strip():
        raise RouterContractError(["question routing requires the question_prompt"])
    if request.routing_basis != QUESTION_ROUTING and request.question_prompt is not None:
        # 의존 routing에 질문을 함께 주면 범위가 다시 질문받은 행위자로 끌려간다.
        raise RouterContractError(["dependency routing must not carry the question_prompt"])
    payload: dict[str, Any] = {
        "routing_basis": request.routing_basis,
        "routed_actor_ids": list(request.routed_actor_ids),
        "factual_scope_text": request.factual_scope_text,
        "case_text": case_text,
        "offense_catalog": [entry.as_dict() for entry in catalog],
    }
    if request.question_prompt is not None:
        payload["question_prompt"] = request.question_prompt
    return payload


def router_request_payload(
    *, question_prompt: str, case_text: str, catalog: Iterable[RouterCatalogEntry]
) -> dict[str, Any]:
    """The exact sub-question, its raw case text, and the closed definition catalog.

    The frozen wire shape of the first ROUTE invocation.  Kept as-is so the existing Call 1
    artifacts and their lineage hashes stay comparable; `route_request_payload` is the general
    form the dependency invocation uses.
    """
    if not question_prompt.strip():
        raise RouterContractError(["question_prompt must be a non-empty string"])
    return {
        "question_prompt": question_prompt,
        "case_text": case_text,
        "offense_catalog": [entry.as_dict() for entry in catalog],
    }


def validate_router_output(
    payload: Mapping[str, Any], *, catalog: Iterable[RouterCatalogEntry]
) -> tuple[str, ...]:
    """Hard-validate and preserve the exact model-emitted seed order.

    This validates JSON shape, the 1--10 raw output limit, strings, and closed
    offense membership.  It intentionally permits repeated *valid* refs; call
    :func:`normalize_router_seeds` is the explicit, auditable next stage.
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
    if len(raw_seeds) > MAX_RAW_SEED_ITEMS:
        errors.append(f"seeds must contain at most {MAX_RAW_SEED_ITEMS} array items")

    allowed = {entry.definition_id for entry in catalog}
    seeds: list[str] = []
    for index, seed in enumerate(raw_seeds):
        where = f"seeds[{index}]"
        if not isinstance(seed, str):
            errors.append(f"{where} must be a string")
            continue
        if seed not in allowed:
            errors.append(f"{where} is not a closed offense definition id: {seed!r}")
            continue
        seeds.append(seed)

    # The budget is spent on distinct refs, so it is checked after the repeated
    # ones have collapsed. Only valid refs are counted -- an unknown id is
    # already its own error above and must not also inflate the budget.
    distinct_count = len(dict.fromkeys(seeds))
    if distinct_count > MAX_SEEDS_PER_CASE:
        errors.append(
            f"seeds must contain at most {MAX_SEEDS_PER_CASE} distinct definition ids"
        )

    if errors:
        raise RouterContractError(errors)
    return tuple(seeds)


def normalize_router_seeds(raw_seeds: Sequence[str]) -> RouterSeedNormalization:
    """Stable-unique valid canonical refs without hiding the raw output.

    The caller must first use :func:`validate_router_output`; malformed,
    unknown, and non-offense values never reach this function as repairs.
    """
    seen: set[str] = set()
    normalized: list[str] = []
    duplicates: list[str] = []
    for seed in raw_seeds:
        if seed in seen:
            if seed not in duplicates:
                duplicates.append(seed)
            continue
        seen.add(seed)
        normalized.append(seed)
    return RouterSeedNormalization(
        raw_seeds=tuple(raw_seeds),
        normalized_seeds=tuple(normalized),
        duplicate_refs=tuple(duplicates),
    )


__all__ = [
    "MAX_RAW_SEED_ITEMS",
    "MAX_SEEDS_PER_CASE",
    "RouterCatalogEntry",
    "RouterContractError",
    "RouterSeedNormalization",
    "normalize_router_seeds",
    "router_catalog",
    "router_catalog_fingerprint",
    "router_request_payload",
    "router_schema",
    "validate_router_output",
]
