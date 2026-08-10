"""Concrete statutory runtime paths added by Phase 5.1.

These are deliberately article-specific rather than an actor-query DSL or a general statutory
exception framework.  They consume already-established symbolic results and never delegate a
legal classification to a model.
"""

from __future__ import annotations

from dataclasses import dataclass

from idpr.v2 import expressions
from idpr.v2.evaluate import TRUE, UNKNOWN, evaluate
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime import pipeline
from idpr.v2.runtime.stages import (
    Article151OffenderStatusObligation,
    LiabilityEvaluation,
    ObligationOutcome,
    StatutoryDeemingObligation,
)
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.compile import CompiledOffense


@dataclass(frozen=True)
class Article151QualifyingLink:
    """A caller-selected, qualifying other-actor result.

    The caller supplies the fine-or-greater classification and records why.  `evaluation` is
    retained rather than reduced to a Boolean so the linked `OffenseInstanceKey` remains available
    in Elements provenance.  The runtime accepts no missing-result shortcut as TRUE.
    """

    evaluation: LiabilityEvaluation
    qualification_provenance: str


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
    linked_instance = None
    qualification_provenance = None
    truth = UNKNOWN
    if qualifying_link is not None:
        linked_instance = qualifying_link.evaluation.instance
        qualification_provenance = qualifying_link.qualification_provenance
        if qualifying_link.evaluation.liability_result is not None:
            truth = TRUE

    obligation = ObligationOutcome(
        obligation=Article151OffenderStatusObligation(
            linked_instance=linked_instance,
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


_ARTICLE_263_REQUIRES = {
    "op": "all",
    "args": [
        {"op": "ref", "ref": "legal_element.concurrent_independent_acts"},
        {"op": "ref", "ref": "legal_element.same_object_of_result"},
        {"op": "ref", "ref": "legal_element.causal_origin_unascertained"},
        {"op": "ref", "ref": "legal_element.injury_result"},
    ],
}


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
        expressions.canonicalize(_ARTICLE_263_REQUIRES), truths.predicate_view(instance)
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
    "Article151QualifyingLink",
    "resolve_article_151_liability",
    "resolve_article_263_deemed_liability",
]
