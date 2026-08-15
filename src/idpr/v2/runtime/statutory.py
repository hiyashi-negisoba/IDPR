"""Concrete statutory runtime paths added by Phase 5.1.

These are deliberately article-specific rather than an actor-query DSL or a general statutory
exception framework.  They consume already-established symbolic results and never delegate a
legal classification to a model.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from idpr.v2 import expressions
from idpr.v2.evaluate import TRUE, UNKNOWN, evaluate
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.article263_grounding import (
    ARTICLE263_PREDICATE_REFS,
    ARTICLE263_SHARED_RESULT_REFS,
)
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime import pipeline
from idpr.v2.runtime.stages import (
    Article151OffenderStatusObligation,
    LiabilityEvaluation,
    ObligationOutcome,
    Article151PredecessorStatus,
    StatutoryDeemingObligation,
)
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.compile import CompiledOffense


@dataclass(frozen=True)
class Article151QualifyingLink:
    """The harboured offender's Article 151 status, at participant level.

    Not a `LiabilityEvaluation`: that would require inventing an answer-facing instance for
    someone the case never asks about.  Not a `UtilizedParticipantOutcome` either, even though the
    shape matches -- Article 34 asks whether the utilised person realized that offense, while
    Article 151 asks whether the person falls under its own 범인 concept, which reaches someone
    under investigation on suspicion of a crime.  Conflating the two would let "established as a
    thief" and "is an offender for Article 151" share one value.

    The threshold is not decided here.  `qualifies_for_article_151()` reads the authored
    classification off the offense definition, and an unauthored offense stays UNKNOWN.
    """

    status: Article151PredecessorStatus
    qualification_provenance: str


ARTICLE_151_QUALIFYING_STATUS = "qualifying"

ARTICLE_151_THRESHOLD_FIELD = "article151_penalty_threshold"
ARTICLE_151_QUALIFYING_CLASS = "fine_or_greater"


def qualifies_for_article_151(registry: DefinitionRegistry, offense_ref: str) -> bool:
    """Whether this offense reaches 형법 제151조 제1항's '벌금 이상의 형' threshold.

    Absence is not a pass.  Nearly every 형법각칙 offense does reach it, which is exactly why the
    host must not assume it: the one place the assumption is wrong would be invisible.  An
    unauthored offense makes the status leaf UNKNOWN, never TRUE.
    """
    entry = registry.get(offense_ref)
    if entry is None or entry.kind not in {"offense", "derived_offense"}:
        return False
    threshold = entry.payload.get(ARTICLE_151_THRESHOLD_FIELD)
    if not isinstance(threshold, Mapping):
        return False
    return threshold.get("class") == ARTICLE_151_QUALIFYING_CLASS


def resolve_article_151_liability(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
    qualifying_link: Article151QualifyingLink | None,
) -> LiabilityEvaluation:
    """Resolve Article 151 with its one approved cross-instance Elements source.

    `legal_element.offender_status_of_object` is always overridden here: a raw target-instance
    fact cannot impersonate the cross-actor legal result.  Absent or not-yet-liable links stay
    UNKNOWN, never FALSE, because this narrow caller input cannot establish that no qualifying
    offense exists.
    """
    linked_participant = None
    qualifying_offense_ref = None
    qualification_provenance = None
    truth = UNKNOWN
    if qualifying_link is not None:
        status = qualifying_link.status
        linked_participant = status.participant
        qualifying_offense_ref = status.offense_ref
        qualification_provenance = qualifying_link.qualification_provenance
        if status.status == ARTICLE_151_QUALIFYING_STATUS and qualifies_for_article_151(
            registry, status.offense_ref
        ):
            truth = TRUE

    obligation = ObligationOutcome(
        obligation=Article151OffenderStatusObligation(
            linked_participant=linked_participant,
            qualifying_offense_ref=qualifying_offense_ref,
            qualification_provenance=qualification_provenance,
        ),
        truth=truth,
    )
    return pipeline.resolve_liability(
        registry,
        compiled,
        instance,
        completion,
        active,
        truths,
        element_truth_overrides={"legal_element.offender_status_of_object": truth},
        element_provenance=(obligation,),
    )


class Article263AuthorityError(ValueError):
    """The authored Article 263 constraint is absent or is not the checked probe."""


def article_263_deeming_expression(
    registry: DefinitionRegistry, offense_ref: str
) -> expressions.CanonicalExpr:
    """Return the one authored Article 263 deeming condition.

    `participation_constraints.statutory_deeming.requires` in the offense definition is the sole
    owner of which predicates Article 263 deems on.  Every consumer -- this module's resolver, the
    Scallop backend, and the dedicated Call 2 route -- reads it from here so a YAML edit cannot
    leave one of them behind.  The wire-order tuples in `article263_grounding` stay the ordering
    authority for the request/response contract and are verified against the authored set.
    """
    entry = registry.get(offense_ref)
    constraints = (entry.payload.get("participation_constraints") or {}) if entry else {}
    statutory = constraints.get("statutory_deeming")
    if statutory is None:
        raise Article263AuthorityError(
            f"{offense_ref!r} has no approved Article 263 statutory_deeming constraint"
        )
    requires = expressions.canonicalize(statutory.get("requires"))
    if requires is None or expressions.canonical_leaf_refs(requires) != frozenset(
        ARTICLE263_PREDICATE_REFS
    ):
        raise Article263AuthorityError(
            "Article 263 statutory_deeming constraint is not the checked probe"
        )
    return expressions.combine_all(
        requires, *(("ref", ref) for ref in ARTICLE263_SHARED_RESULT_REFS)
    )


def resolve_article_263_deemed_liability(
    registry: DefinitionRegistry,
    compiled: CompiledOffense,
    instance: OffenseInstanceKey,
    completion: CompletionResult,
    active: ActiveDoctrineRefs,
    truths: CaseTruths,
) -> LiabilityEvaluation:
    """Apply Article 263's deemed effect to an underlying injury-offense evaluation.

    The result retains `instance.offense_ref`: Article 263 is not a standalone offense identity.
    This function never calls ATTRIBUTE or merges any actor's conduct truths.
    """
    truth = evaluate(
        article_263_deeming_expression(registry, compiled.id), truths.predicate_view(instance)
    )
    obligation = ObligationOutcome(
        obligation=StatutoryDeemingObligation(underlying_instance=instance),
        truth=truth,
    )
    return pipeline.resolve_liability(
        registry,
        compiled,
        instance,
        completion,
        active,
        truths,
        element_provenance=(obligation,),
    )


__all__ = [
    "ARTICLE_151_QUALIFYING_CLASS",
    "ARTICLE_151_THRESHOLD_FIELD",
    "ARTICLE_151_QUALIFYING_STATUS",
    "Article151QualifyingLink",
    "Article263AuthorityError",
    "article_263_deeming_expression",
    "qualifies_for_article_151",
    "resolve_article_151_liability",
    "resolve_article_263_deemed_liability",
]
