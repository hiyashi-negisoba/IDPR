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
from typing import Generic, Literal, Mapping, TypeVar

from idpr.v2.evaluate import TruthValue
from idpr.v2.expressions import CanonicalExpr
from idpr.v2.relations import RelationInstanceKey
from idpr.v2.runtime.identity import OffenseFormKey, RuntimeRelationKey

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
class RelationObligation:
    """One relation obligation evaluated FALSE. Keyed at runtime (case-scoped)."""

    key: RuntimeRelationKey


@dataclass(frozen=True)
class FormRequirementObligation:
    """A completion form's own extra requirement evaluated FALSE (e.g. attempt's 실행의 착수).

    Unused in step 6A -- the completed form has no extra requirement -- but declared now because
    step 6B's Elements program is `active slots + form requirement + retained relations`, so a
    failure that is neither a slot nor a relation is reachable the moment attempt exists.
    """

    form: str


Obligation = SlotObligation | RelationObligation | FormRequirementObligation
"""Deliberately NOT `PredicateObligation(ref)`. `evaluate()` returns one TruthValue, and an
expression can be FALSE with no FALSE leaf anywhere in it -- `NOT(A)` with `A=TRUE`, or
`ONE_OF(A, B)` with both TRUE. Walking the tree again in the pipeline to guess a "decisive leaf"
would be a second, unsound evaluator. These three units are exactly what the existing evaluator can
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
# Completion program (type only in 6A -- semantics land in 6B)
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class FormProgram:
    """The executable legal program for one completion form.

    Section 14's point, made concrete: an attempt is not "the completed offense plus extras". It is
    a program in which the result and causation obligations *do not exist*. Suspension removes an
    obligation from the fold; it never rewrites a FALSE into a TRUE.

    Declared in 6A, consumed in 6B. The pipeline rejects any non-completed value rather than
    accepting and ignoring it.
    """

    form: str

    punishable: bool
    """From `CompletionPolicyDef.forms[form].punishable`. Carried here so the compiled program does
    not silently drop it -- otherwise the runtime would have to rediscover whether an offense has an
    attempt/preparation punishment provision at all. NOT the same question as the Punishability
    stage's EXEMPT: this asks whether this incomplete *form* is a punishable legal shape, while the
    stage asks whether an established offense carries an exemption or modification."""

    suspended_slots: frozenset[str] = frozenset()
    extra: CanonicalExpr = None
    """`CompletionPolicyDef.forms[form].requires` -- the form's own requirement (attempt's 착수),
    added to the fold, never replacing base obligations."""

    relation_dispositions: Mapping[RelationInstanceKey, Literal["retain", "suspend"]] = (
        None  # type: ignore[assignment]
    )
    """Explicit per-relation disposition. A relation affected by a suspended obligation must be
    declared `retain` or `suspend` by the policy -- there is no safe default, since slot topology
    does not determine it (in a result-crime attempt only the result side is suspended, yet
    `causal_nexus` must still disappear). Unaffected relations are retained without declaration."""

    def __post_init__(self) -> None:
        if self.relation_dispositions is None:
            object.__setattr__(self, "relation_dispositions", {})


def completed_program() -> FormProgram:
    """The only program step 6A evaluates."""
    return FormProgram(form="completed", punishable=True)


# --------------------------------------------------------------------------------------------
# Legal conclusions -- constructed only when the corresponding gate actually passed
# --------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class OffenseRealization:
    """Section 4.5: Elements satisfied AND Unlawfulness preserved. Exists only when true."""

    form_key: OffenseFormKey
    elements: StageResult[ElementsState]
    unlawfulness: StageResult[UnlawfulnessState]


@dataclass(frozen=True)
class OffenseEstablishment:
    """Section 4.5: Realization AND culpability legally sufficient. Exists only when true."""

    form_key: OffenseFormKey
    realization: OffenseRealization
    culpability: StageResult[CulpabilityState]


@dataclass(frozen=True)
class LiabilityResult:
    """Section 4.5: Establishment AND a punishability assessment. Exists only when true."""

    form_key: OffenseFormKey
    establishment: OffenseEstablishment
    punishability: StageResult[PunishabilityState]


@dataclass(frozen=True)
class LiabilityEvaluation:
    """The always-present trace of one instance/form evaluation.

    Every stage is here whether reached or not; the three conclusions above are here only if their
    gate passed. That keeps the legal ontology (what was concluded) out of the runtime trace (what
    was computed).
    """

    form_key: OffenseFormKey

    elements: StageResult[ElementsState]
    unlawfulness: StageResult[UnlawfulnessState]
    culpability: StageResult[CulpabilityState]
    punishability: StageResult[PunishabilityState]

    realization: OffenseRealization | None = None
    establishment: OffenseEstablishment | None = None
    liability_result: LiabilityResult | None = None

    decisive_stage: str | None = None
    """The first stage whose gate did not pass. `None` on a path that ran to the end -- a fully
    successful evaluation has no stage that decisively stopped it."""

    decisive_obligation: Obligation | None = None
    decisive_doctrine: str | None = None
