"""Runtime stage objects and legal conclusions (v2.1.0 sections 12-13, build-order step 6A).

Three separations are load-bearing here, and each one was a bug in an earlier draft:

1. **legal state vs evaluation state** (section 4.4). `not_reached` is not a legal result. No legal
   state enum contains it; it lives in `evaluation_state`, and the legal fields go `None`.

2. **legal state vs gate state.** "What is this stage's legal state?" and "does this stage let the
   next conclusion be drawn?" are different questions. With an UNKNOWN MODIFY the culpability state
   is genuinely *unknown* (preserved or diminished -- nobody knows which), yet the establishment
   gate passes either way (section 13.2 admits both). Collapsing that to `preserved` would have the
   symbolic runtime assert a stronger legal conclusion than the evidence supports.

3. **evaluation trace vs legal conclusion.** `OffenseRealization` means "the offense WAS realized"
   (section 4.5). If it were a mandatory field of the result, a case with failed Elements would
   force construction of `OffenseRealization(elements=failed, ...)` -- an object whose name asserts
   the opposite of its contents. So conclusions exist only when their gate actually passed, and
   `LiabilityEvaluation` is the always-present trace that holds them optionally.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from idpr.v2.evaluate import TruthValue
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.identity import (
    FactualParticipantKey,
    OffenseInstanceKey,
    RuntimeRelationKey,
)

ElementsState = Literal["satisfied", "failed", "unresolved"]
UnlawfulnessState = Literal["preserved", "defeated", "unresolved"]
CulpabilityState = Literal["preserved", "defeated", "diminished", "unresolved"]
PunishabilityState = Literal["punishable", "exempted", "modified", "unresolved"]

EvaluationState = Literal["evaluated", "not_reached"]
"""Section 4.4: whether this stage was reached at all. Deliberately NOT a legal value."""

GateState = Literal["passes", "fails", "unresolved"]
"""Whether this stage permits the next typed conclusion (Realization / Establishment / Liability).
Independent of `legal_state`: an unknown MODIFY leaves the legal state unknown but the gate open."""

STAGE_NAMES: tuple[str, ...] = ("elements", "unlawfulness", "culpability", "punishability")


# --------------------------------------------------------------------------------------------
# Obligations -- what an Elements evaluation can point at as decisive
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class SlotObligation:
    """One fixed slot's whole expression evaluated FALSE."""

    slot: str


@dataclass(frozen=True)
class ComponentSlotObligation:
    """One direct COMPOSE component's contribution to a fixed slot (Article 339 only)."""

    local_key: str
    slot: str


@dataclass(frozen=True)
class RelationObligation:
    """One relation obligation evaluated FALSE. Keyed at runtime (case-scoped)."""

    key: RuntimeRelationKey


@dataclass(frozen=True)
class CompletionRequirementObligation:
    """A completion state's own `requires` evaluated FALSE (e.g. an attempt's 실행의 착수).

    The Elements program is `active slots + retained relations + this state's requirement`, so a
    failure that is neither a slot nor a relation becomes reachable as soon as any state authors
    `requires`.
    """

    state: str


@dataclass(frozen=True)
class ParticipationDependencyObligation:
    """Step 6C: the typed principal-realization gate a derivative participant's (instigator/aider)
    Elements starts from -- `principal_realization_truth()` in `runtime/participation.py`."""

    mode: Literal["instigator", "aider"]


@dataclass(frozen=True)
class ParticipationRequirementObligation:
    """Step 6C: a derivative mode's own `requires` (8th schema addendum on `derivative_mode`),
    evaluated against the participant's OWN truths -- never the principal's."""

    mode: Literal["instigator", "aider"]


@dataclass(frozen=True)
class CoPrincipalConstitutiveStatusObligation:
    """Article 33 status effect without changing the target actor's truth."""

    ref: str
    satisfying_instances: tuple[OffenseInstanceKey, ...]


@dataclass(frozen=True)
class Article151OffenderStatusObligation:
    """The linked offender's own outcome, as Article 151's status leaf reads it.

    The linked person is a factual participant, not an answer-facing actor: the question asks
    about the harbourer's liability, so the harboured offender has no `OffenseInstanceKey` in this
    case and never should be given one to satisfy a type.  This mirrors Article 34, where the
    utilised participant also stays at participant level.  `qualifying_offense_ref` records which
    offense cleared the threshold, so Elements provenance still says why the status held.
    """

    linked_participant: FactualParticipantKey | None
    qualifying_offense_ref: str | None
    qualification_provenance: str | None


@dataclass(frozen=True)
class StatutoryDeemingObligation:
    """Article 263's deemed effect, distinct from actual co-principal attribution."""

    underlying_instance: OffenseInstanceKey


@dataclass(frozen=True)
class IndirectPrincipalDependencyObligation:
    """Article 34's direction-reversed dependency on the utilised actor's outcome."""

    reason: str


@dataclass(frozen=True)
class UtilizedParticipantOutcome:
    """Typed internal outcome for a factual participant, never ordinary liability output."""

    participant: FactualParticipantKey
    offense_ref: str
    status: Literal[
        "elements_failure",
        "unlawfulness_defeat",
        "culpability_defeat",
        "punishability_defeat",
        "different_negligence_offense",
        "liable_exact_offense",
        "unresolved",
    ]


Obligation = (
    SlotObligation
    | ComponentSlotObligation
    | RelationObligation
    | CompletionRequirementObligation
    | ParticipationDependencyObligation
    | ParticipationRequirementObligation
    | CoPrincipalConstitutiveStatusObligation
    | Article151OffenderStatusObligation
    | StatutoryDeemingObligation
    | IndirectPrincipalDependencyObligation
)
"""Deliberately NOT `PredicateObligation(ref)`. `evaluate()` returns one TruthValue, and an
expression can be FALSE with no FALSE leaf anywhere in it -- `NOT(A)` with `A=TRUE`, or
`ONE_OF(A, B)` with both TRUE. Walking the tree again in the pipeline to guess a "decisive leaf"
would be a second, unsound evaluator. These five units are exactly what the existing evaluator can
answer honestly. Predicate-level provenance, if ever needed, means a real `evaluate_with_trace()`,
not a heuristic here."""


@dataclass(frozen=True)
class ObligationOutcome:
    """One obligation's evaluated truth -- the Elements stage's provenance record."""

    obligation: Obligation
    truth: TruthValue


ProvenanceItem = ObligationOutcome


# --------------------------------------------------------------------------------------------
# Stage results
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class AppliedEffect:
    """A doctrine effect that fired (`truth=TRUE`) or might still fire (`truth=UNKNOWN`).

    This is the derivation of the stage's legal state -- "Unlawfulness = defeated BECAUSE
    DEFEAT<Unlawfulness>(self_defense)" -- not writer decoration. It is also the only thing that
    carries `modifier_ref` forward; without it a MODIFY's payload vanishes at the stage boundary and
    nothing downstream can say which modification applied.
    """

    doctrine_ref: str
    effect: Literal["DEFEAT", "MODIFY", "EXEMPT"]
    stage: str
    modifier_ref: str | None
    truth: TruthValue


S = TypeVar("S")


@dataclass(frozen=True)
class StageResult(Generic[S]):
    evaluation_state: EvaluationState
    legal_state: S | None
    gate_state: GateState | None
    effects: tuple[AppliedEffect, ...] = ()
    provenance: tuple[ProvenanceItem, ...] = ()

    def __post_init__(self) -> None:
        """Enforce the three-way equivalence at construction.

        Type annotations alone permit `StageResult("evaluated", None, None)`, which would leave the
        invariant as a comment. `not_reached` additionally forces `effects=()`: an effect recorded on
        a stage that was never reached is a hypothetical ("self-defense *would have* applied"), and
        v2.2.0 section 24 keeps hypothetical reasoning out of symbolic state entirely.
        """
        reached = self.evaluation_state != "not_reached"
        if reached != (self.legal_state is not None) or reached != (self.gate_state is not None):
            raise ValueError(
                "StageResult invariant violated: evaluation_state="
                f"{self.evaluation_state!r} with legal_state={self.legal_state!r}, "
                f"gate_state={self.gate_state!r} -- not_reached must pair with both being None, "
                "and evaluated with neither being None"
            )
        if not reached and self.effects:
            raise ValueError(
                "StageResult invariant violated: a not_reached stage carries effects "
                f"{self.effects!r} -- that is hypothetical reasoning, not symbolic state"
            )


def not_reached() -> StageResult:
    """The one legitimate way to build a stage that evaluation never got to."""
    return StageResult(evaluation_state="not_reached", legal_state=None, gate_state=None)


# --------------------------------------------------------------------------------------------
# Legal conclusions -- constructed only when the corresponding gate actually passed
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class OffenseRealization:
    """Section 4.5: Elements satisfied AND Unlawfulness preserved. Exists only when true."""

    instance: OffenseInstanceKey
    elements: StageResult[ElementsState]
    unlawfulness: StageResult[UnlawfulnessState]


@dataclass(frozen=True)
class OffenseEstablishment:
    """Section 4.5: Realization AND culpability legally sufficient. Exists only when true."""

    instance: OffenseInstanceKey
    realization: OffenseRealization
    culpability: StageResult[CulpabilityState]


@dataclass(frozen=True)
class LiabilityResult:
    """Section 4.5: Establishment AND a punishability assessment. Exists only when true."""

    instance: OffenseInstanceKey
    establishment: OffenseEstablishment
    punishability: StageResult[PunishabilityState]


@dataclass(frozen=True)
class LiabilityEvaluation:
    """The always-present trace of one instance's evaluation.

    Every stage is here whether reached or not; the three conclusions above are here only if their
    gate passed. That keeps the legal ontology (what was concluded) out of the runtime trace (what
    was computed).

    `completion` is a legal judgement about this instance, so it belongs in the trace next to the
    stages -- not in the instance key, which identifies the offense occurrence itself and does not
    change with what the evidence shows about its completion.

    `completion` is present as a *field* on every evaluation, but its value is `None` specifically
    for derivative-participation instances (step 6C, `runtime/participation.py`): instigators/
    aiders never derive a completion judgement of their own (decision #3 -- Completion is skipped
    entirely for them, in favor of a principal-realization + own-requirement Elements gate), so
    storing the principal's `CompletionResult` here would misrepresent the record as if the
    accessory had one. The principal's own completion is already reachable via the principal's own
    `LiabilityEvaluation.completion` if ever needed.
    """

    instance: OffenseInstanceKey
    completion: CompletionResult | None

    elements: StageResult[ElementsState]
    unlawfulness: StageResult[UnlawfulnessState]
    culpability: StageResult[CulpabilityState]
    punishability: StageResult[PunishabilityState]

    realization: OffenseRealization | None = None
    establishment: OffenseEstablishment | None = None
    liability_result: LiabilityResult | None = None

    decisive_stage: str | None = None
    """The first stage whose gate did not pass, or `"completion"` when the run stopped before any
    stage was reached (unresolved / not_applicable / non-punishable completion state). `None` on a
    path that ran to the end -- a fully successful evaluation has no stage that decisively stopped
    it. Note `"completion"` is deliberately not in `STAGE_NAMES`: Completion is an orthogonal axis
    (section 14), not a fifth stage in the Elements->Punishability chain."""

    decisive_obligation: Obligation | None = None
    decisive_doctrine: str | None = None
