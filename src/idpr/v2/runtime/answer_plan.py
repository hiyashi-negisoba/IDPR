"""Project the finished symbolic run into the input representation Call 3 reads.

The plan computes no new legal judgment.  Every conclusion in it already exists in
``LiabilityEvaluation``, ``FinalResponsibilityView`` or the Call 2 assessments; this module
rearranges them deterministically and attaches the authored norm each finding is about.
Two fields are not direct projections -- ``contested_points`` looks up authored doctrine
branches, and ``rule_statements`` is filled by the card retrieval of ANSWERPLAN_SPEC 5.5 --
and both carry an explicit origin so the distinction survives into the audit.

Three locks keep the evaluation material out of what we produce, because without them the
rule-base contribution we report would be a reflection of the grading key rather than a
measurement of it:

* the dataset ``supporting_precedents`` column is never read;
* no field derives from per-question rubric item counts or scores;
* contested points come only from authored doctrine or reviewed cards.

The rubric statistics that motivated the schema stay in the design document.  They do not
enter the artifact.
"""

from __future__ import annotations

import collections
import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2 import expressions
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.completion import DERIVABLE_STATES, completion_policy_for

#: Internal vocabulary that must never survive serialization into the Call 3 payload.
#: A leak here does not merely look untidy -- it teaches the writer to quote machine state
#: back into a legal answer.
_INTERNAL_MARKERS = (
    "binding:",
    "factual_episode:",
    "offense.",
    "derived_offense.",
    "legal_element.",
    "ground_fact.",
    "relation.",
    "doctrine.",
    "condition.",
    "concurrence-pair:",
    "UNKNOWN",
    "stage=",
    "source_run=",
    "Scallop",
    "Call 2",
    # 점 없는 형태로도 샌다. `legal_element.result_causation`의 판단기준이
    # "현재 offense instance의 …"였고 위의 `offense.`에 걸리지 않았다. 본 수정은 저작 쪽에서
    # 했고 이 목록은 회귀 방지용이다.
    "offense instance",
    "offense_instance",
    "predicate",
    "death-agnostic",
)

_ALLOWED_CONTESTED_ORIGINS = ("authored_doctrine", "reviewed_card")

#: Final states, in the vocabulary the answer writer sees rendered as prose.
ESTABLISHED = "ESTABLISHED"
NOT_ESTABLISHED = "NOT_ESTABLISHED"
UNRESOLVED = "UNRESOLVED"
NOT_ATTRIBUTABLE = "NOT_ATTRIBUTABLE"
ABSORBED = "ABSORBED"


class AnswerPlanError(RuntimeError):
    """A plan that would mislead the writer is not built."""


@dataclass(frozen=True, slots=True)
class RuleStatement:
    """One norm sentence the answer may state, copied verbatim from its source."""

    statement: str
    origin: str
    source_id: str

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise AnswerPlanError("rule statement is empty")
        if not self.source_id:
            raise AnswerPlanError(f"rule statement without source id: {self.statement[:40]}")


@dataclass(frozen=True, slots=True)
class Finding:
    """A decisive element of one instance, with the norm it was measured against."""

    label: str
    truth: str
    legal_standard: str | None = None
    #: 직렬화되지 않는다. live frontier 계산이 어느 요건인지 알아야 해서 남긴다.
    predicate_ref: str = ""
    governing_provision: str | None = None
    rule_statements: tuple[RuleStatement, ...] = ()
    supporting_quotes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ParticipationRoute:
    mode: str
    principal_actor: str | None
    principal_offense: str | None
    principal_realization: str | None
    relation: str | None = None


@dataclass(frozen=True, slots=True)
class ContestedPoint:
    """A doctrinal split the answer should present before adopting one side.

    ``origin`` is mandatory and closed.  A contested point invented from the grading
    rubric would hand back the very thing the rubric is testing.
    """

    label: str
    positions: tuple[str, ...]
    adopted: str
    why_adopted: str
    origin: str
    source_id: str

    def __post_init__(self) -> None:
        if self.origin not in _ALLOWED_CONTESTED_ORIGINS:
            raise AnswerPlanError(
                f"contested point origin {self.origin!r} is not one of {_ALLOWED_CONTESTED_ORIGINS}"
            )
        if not self.source_id:
            raise AnswerPlanError(f"contested point without source id: {self.label!r}")


@dataclass(frozen=True, slots=True)
class AnchoredIssue:
    issue_id: str
    actor: str
    offense_label: str
    governing_provision: str | None
    episode_quotes: tuple[str, ...]
    final_state: str
    completion_state: str | None
    completion_why: str | None
    participation: ParticipationRoute | None
    decisive_stage: str | None
    satisfied: tuple[Finding, ...]
    failed: tuple[Finding, ...]
    blocking: tuple[Finding, ...]
    doctrines: tuple[Mapping[str, Any], ...]
    contested_points: tuple[ContestedPoint, ...]
    #: True when a stage gate actually failed in the run.  This is the symbolic fact the
    #: no-acquittal-from-UNKNOWN contract is about; the predicate lists cannot stand in for
    #: it, because a gate can fail on a relation obligation that is not a predicate at all.
    gate_failed: bool = False
    absorbed_into: str | None = None
    absorption_relation: str | None = None
    absorption_reason: str | None = None
    not_attributable_reason: str | None = None


@dataclass(frozen=True, slots=True)
class FinalResponsibility:
    retained: tuple[Mapping[str, str], ...]
    absorbed: tuple[Mapping[str, Any], ...]
    imaginative_pairs: tuple[Mapping[str, Any], ...]
    excess_attributions: tuple[Mapping[str, Any], ...]
    status_redirections: tuple[Mapping[str, Any], ...]
    #: 죄수관계. 상상적 경합과 실체적 경합 모두 symbolic 단계가 실현 행위의 동일성에서
    #: 적극적으로 판정한 것이고, host가 흡수의 여집합으로 찍은 것이 아니다.
    concurrence_relations: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True, slots=True)
class RequiredFinalConclusion:
    """One anchor the closing paragraph must restate, in the model's own words.

    This is not a sentence to hand the writer -- it is the smallest closed set of facts a
    closing paragraph cannot omit or invert: which actor, which offence, and the one
    conclusion word already fixed for it elsewhere in the plan.  Wording, ordering, and
    connective prose stay the model's to compose; only the presence and polarity of each
    of these anchors is required, one per anchored issue.
    """

    actor: str
    offense_label: str
    state: str
    completion_state: str | None = None
    participation_mode: str | None = None
    #: 같은 행위자의 같은 죄가 서로 다른 행위로 두 번 열렸을 때, 어느 행위에 대한 결론인지.
    #: 죄명 자체는 손대지 않는다 -- 완결성 감사가 죄명으로 답안을 찾기 때문이다.
    occurrence_hint: str | None = None


@dataclass(frozen=True, slots=True)
class AnswerPlan:
    case_id: str
    case_text: str
    question: str
    discussion_order: tuple[str, ...]
    anchored_issues: tuple[AnchoredIssue, ...]
    final_responsibility: FinalResponsibility
    required_final_conclusions: tuple[RequiredFinalConclusion, ...] = ()
    representation_gaps: tuple[str, ...] = ()
    unmapped_instances: tuple[str, ...] = ()


# --------------------------------------------------------------------------------------
# identity and labels
# --------------------------------------------------------------------------------------


def instance_ref(instance: Mapping[str, Any]) -> str:
    """Stable internal key for one liability instance.  Never serialized to the model."""
    return "|".join(
        (
            str(instance.get("case_id", "")),
            str(instance.get("actor_id", "")),
            str(instance.get("offense_ref", "")),
            str(instance.get("occurrence_id", "")),
        )
    )


def offense_label(
    registry: DefinitionRegistry,
    offense_ref: str,
    labels: Mapping[str, str] | None = None,
) -> str:
    """The Korean offence name, from authored sources only.

    Two sources carry it: the offence's own ``identity.name``, and the reviewed seed-cue
    catalogue that Call 1.5 already routes with.  Derived offences have no ``identity`` at
    all, so the catalogue is the only name they have.  When neither has one we refuse
    rather than fall back to the ref -- an answer that names a crime ``special_theft``
    would be worse than one that fails to build.
    """
    entry = registry.by_id.get(offense_ref)
    if entry is not None:
        name = (entry.payload.get("identity") or {}).get("name")
        if name:
            return str(name)
    if labels and offense_ref in labels:
        return str(labels[offense_ref])
    raise AnswerPlanError(
        f"no authored Korean name for {offense_ref}; "
        "author it in data/v2/binding_seed_cues.yaml before building the plan"
    )


def governing_provision(registry: DefinitionRegistry, offense_ref: str) -> str | None:
    entry = registry.by_id.get(offense_ref)
    if entry is None:
        return None
    identity = entry.payload.get("identity") or {}
    refs = identity.get("statutory_refs") or []
    return "; ".join(str(ref) for ref in refs) if refs else None


#: Latin script inside a ``canonical_meaning`` marks an authoring note rather than a legal
#: term -- "death-agnostic 패턴", "(+NOT())", "아래 B-7".  Five predicates carry one.
_AUTHORING_NOTE = re.compile(r"[A-Za-z]")


def predicate_label(registry: DefinitionRegistry, predicate_ref: str) -> str:
    """What a lawyer calls this element.

    ``canonical_meaning`` is the authored short name and is usually exactly right.  Where
    it still carries a worksheet annotation, the authored ``legal_standard`` is used
    instead: it is a full sentence rather than a label, but it is written in law rather
    than in modelling vocabulary.
    """
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return predicate_ref.rsplit(".", 1)[-1].replace("_", " ")
    meaning = entry.payload.get("canonical_meaning")
    if meaning and not _AUTHORING_NOTE.search(str(meaning)):
        return str(meaning)
    standard = entry.payload.get("legal_standard")
    if standard:
        return str(standard)
    if meaning:
        return _AUTHORING_NOTE.sub("", str(meaning)).strip()
    return predicate_ref.rsplit(".", 1)[-1].replace("_", " ")


def predicate_standard(registry: DefinitionRegistry, predicate_ref: str) -> str | None:
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return None
    standard = entry.payload.get("legal_standard")
    return str(standard) if standard else None


def predicate_provision(registry: DefinitionRegistry, predicate_ref: str) -> str | None:
    """The statutory citation authored on the predicate, if any."""
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return None
    for ref in entry.payload.get("authority_refs") or []:
        if not isinstance(ref, Mapping):
            continue
        if ref.get("authority_basis") == "statute_text" and ref.get("citation"):
            return str(ref["citation"])
    return None


#: 형법 총칙의 마지막 조문. 고의(제13조)·미수(제25조)·독립행위경합(제19조)처럼 총칙 조문은
#: 어느 죄를 논하든 그 요건의 근거가 맞으므로 죄명 범위 밖이라는 이유로 떼지 않는다.
_GENERAL_PART_LAST_ARTICLE = 86

_ARTICLE_NUMBER = re.compile(r"제(\d+)조")


def offense_article_scope(registry: DefinitionRegistry, offense_ref: str) -> frozenset[int]:
    """이 죄가 자기 이름으로 댈 수 있는 각칙 조문 번호.

    자기 `statutory_refs`와, `derivation.base`를 따라 올라간 기초범죄의 것을 함께 센다.
    특수절도죄가 제329조를, 강간치상죄가 제297조를 대는 것은 누출이 아니라 그 죄의 구성이다.
    """
    numbers: set[int] = set()
    seen: set[str] = set()
    frontier = [offense_ref]
    while frontier:
        ref = frontier.pop()
        if not ref or ref in seen:
            continue
        seen.add(ref)
        entry = registry.by_id.get(ref)
        if entry is None:
            continue
        identity = entry.payload.get("identity") or {}
        for citation in identity.get("statutory_refs") or []:
            numbers.update(int(n) for n in _ARTICLE_NUMBER.findall(str(citation)))
        base = (entry.payload.get("derivation") or {}).get("base")
        if base:
            frontier.append(str(base))
    return frozenset(numbers)


def scope_provision(provision: str | None, scope: frozenset[int]) -> str | None:
    """요건에 저작된 조문 가운데 이 죄가 댈 수 있는 것만 남긴다.

    `legal_element.unlawful_appropriation_intent`는 절도죄 밑에서 저작돼 제329조를 달고
    다니는데, 같은 요건이 사기·횡령·강도에도 쓰인다. 그대로 내보내면 사기죄 논증에서
    절도죄 조문을 인용하게 된다 -- 26문항에서 각칙 조문 110건이 그랬다. 떼는 것은 조문뿐이고
    `legal_standard`는 그대로 간다. 요건의 뜻은 저작된 자리에 그대로 있다.
    """
    kept = [
        citation
        for citation in _split_citations(provision)
        if all(
            int(number) <= _GENERAL_PART_LAST_ARTICLE or int(number) in scope
            for number in _ARTICLE_NUMBER.findall(citation)
        )
    ]
    return "; ".join(kept) if kept else None


def authored_precedent_statements(
    registry: DefinitionRegistry, predicate_ref: str
) -> tuple[RuleStatement, ...]:
    """Precedent-based authority already authored on the predicate itself.

    Only twelve predicates carry one, which is exactly why the card channel exists.  The
    two sources stay distinguishable by ``origin`` rather than being merged.
    """
    entry = registry.by_id.get(predicate_ref)
    if entry is None:
        return ()
    statements: list[RuleStatement] = []
    for ref in entry.payload.get("authority_refs") or []:
        if not isinstance(ref, Mapping):
            continue
        basis = str(ref.get("authority_basis", ""))
        if "precedent" not in basis:
            continue
        citation = str(ref.get("citation", "")).strip()
        if not citation:
            continue
        statements.append(
            RuleStatement(statement=citation, origin="authored_doctrine", source_id=predicate_ref)
        )
    return tuple(statements)


# --------------------------------------------------------------------------------------
# projection
# --------------------------------------------------------------------------------------


def _findings_for_instance(
    registry: DefinitionRegistry,
    truths: Sequence[Mapping[str, Any]],
    ref: str,
    quotes_by_predicate: Mapping[str, tuple[str, ...]],
    card_statements: Mapping[tuple[str, str], Sequence[RuleStatement]] | None = None,
    offense_ref: str = "",
) -> tuple[tuple[Finding, ...], tuple[Finding, ...], tuple[Finding, ...]]:
    """Findings for one already-selected instance, from the authoritative truth store.

    `truths` is `case_truths`: what the symbolic layer actually consumed to reach the
    conclusion this issue states.  The raw `assessments` of a single Call 2 run is a subset
    of it -- merged participation and doctrine truths land only in `case_truths` -- and
    projecting from the subset silently drops the grounds for conclusions the plan is
    simultaneously asserting.

    This does not widen the issue universe.  Every finding still has to match a `ref` that
    came from the run's liability results, so a truth about an instance no legal conclusion
    was reached for contributes nothing here, exactly as before.

    ``card_statements`` is the SPEC 5.5 retrieval, keyed on the pair it searched for --
    ``(instance ref, predicate ref)``.  It reaches every finding, not just the satisfied
    ones: stating why an element was not met is exactly where the norm behind it matters.
    It can only lengthen ``rule_statements``; which list a finding lands in is decided by
    its truth alone (SPEC 4-10).
    """
    card_statements = card_statements or {}
    scope = offense_article_scope(registry, offense_ref)
    satisfied: list[Finding] = []
    failed: list[Finding] = []
    blocking: list[Finding] = []
    for row in truths:
        instance = row.get("instance_key") or {}
        if instance_ref(instance) != ref:
            continue
        predicate_ref = str(row.get("predicate_ref", ""))
        if not predicate_ref:
            continue
        finding = Finding(
            label=predicate_label(registry, predicate_ref),
            truth=str(row.get("truth", "")),
            predicate_ref=predicate_ref,
            legal_standard=predicate_standard(registry, predicate_ref),
            governing_provision=scope_provision(
                predicate_provision(registry, predicate_ref), scope
            ),
            rule_statements=(
                authored_precedent_statements(registry, predicate_ref)
                + tuple(card_statements.get((ref, predicate_ref), ()))
            ),
            supporting_quotes=quotes_by_predicate.get(predicate_ref, ()),
        )
        if finding.truth == "TRUE":
            satisfied.append(finding)
        elif finding.truth == "FALSE":
            failed.append(finding)
        else:
            blocking.append(finding)
    return tuple(satisfied), tuple(failed), tuple(blocking)


def _completion_state_refs(
    registry: DefinitionRegistry, offense_ref: str
) -> dict[str, frozenset[str]]:
    """`{완성 상태: 그 상태를 정하는 predicate ref}`. 정책이 없으면 빈 사전."""
    policy = completion_policy_for(registry, offense_ref)
    if policy is None:
        return {}
    output: dict[str, frozenset[str]] = {}
    for name, state in (policy.payload.get("states") or {}).items():
        refs = set(expressions.leaf_refs(state.get("when")))
        refs |= set(expressions.leaf_refs(state.get("requires")))
        # `blocked_when`은 뺀다. 확정되었을 때만 배제하는 장치이므로 UNKNOWN인 동안에는
        # 아무것도 막지 않고, 막지 않는 것을 "결론을 막는 요건"으로 내보낼 수 없다.
        refs -= set(expressions.leaf_refs(state.get("blocked_when")))
        output[str(name)] = frozenset(refs)
    return output


def _completion_blockers(
    registry: DefinitionRegistry, offense_ref: str
) -> frozenset[str]:
    policy = completion_policy_for(registry, offense_ref)
    if policy is None:
        return frozenset()
    return frozenset().union(
        *(
            expressions.leaf_refs(state.get("blocked_when"))
            for state in (policy.payload.get("states") or {}).values()
        ),
        frozenset(),
    )


def live_unresolved_frontier(
    registry: DefinitionRegistry,
    result: Mapping[str, Any],
    offense_ref: str,
    blocking: Sequence[Finding],
    known: Sequence[Finding] = (),
) -> tuple[Finding, ...]:
    """지금 결론을 실제로 막고 있는 미확정 요건만 남긴다.

    모든 UNKNOWN을 평평하게 넘기면 Call 3는 그것들을 전부 실제 쟁점으로 받아들인다. 살인
    하나에 예비·불능미수·중지미수 요건까지 "확정되지 않은 요건"으로 붙어 나갔고, 사안에서
    아무도 제기하지 않은 논점을 답안이 늘어놓게 된다.

    두 갈래로 좁힌다.

    * 결정 단계가 완성단계면, 아직 배제되지 않은 상태들의 요건만 본다. 그 중 **근거가 하나라도
      확정된** 상태가 있으면 그 상태들의 요건이 frontier다. 하나도 없으면 -- 어느 상태도
      사실로 제기되지 않았다는 뜻이므로 -- 남은 상태들이 **공유하는** 요건만 남긴다. 그것이
      상태들을 가르는 최소 지점이고, 보통 실행의 착수다.
    * 그 밖의 단계면 완성단계 전용 요건을 뺀다. 구성요건이 결정 단계인데 미수 유형 요건을
      쟁점으로 내보내는 것은 단계를 섞는 것이다.

    좁힌 결과가 비면 좁히지 않은 것을 그대로 돌려준다. 막고 있는 것이 무엇인지 말하지 못하는
    것보다는 넓게 말하는 편이 낫다.
    """
    values = tuple(blocking)
    state_refs = _completion_state_refs(registry, offense_ref)
    if not state_refs:
        return values
    completion_only = frozenset().union(*state_refs.values())
    blockers = _completion_blockers(registry, offense_ref)
    values = tuple(v for v in values if v.predicate_ref not in blockers) or values
    if result.get("decisive_stage") != "completion":
        return tuple(v for v in values if v.predicate_ref not in completion_only) or values

    provenance = (result.get("completion") or {}).get("provenance") or []
    open_states = [
        str(row.get("state"))
        for row in provenance
        if row.get("truth") != "FALSE" and str(row.get("state")) in state_refs
    ]
    if not open_states:
        return values
    # 사실로 제기된 상태 = 그 상태의 요건 중 **확정된 답이 하나라도 있는** 상태.
    # 아예 답이 없는 요건(미질문·미기록)을 근거로 세면 안 된다 -- 부재는 증거가 아니다.
    known_refs = {value.predicate_ref for value in known if value.predicate_ref}
    grounded = [name for name in open_states if state_refs[name] & known_refs]
    if grounded:
        scope = frozenset().union(*(state_refs[name] for name in grounded))
    else:
        # 어느 상태도 사실로 제기되지 않았다. 그러면 여러 상태가 **함께** 걸려 있는 요건이
        # 그 갈림의 최소 지점이다 -- 살인이라면 사망 결과와 실행의 착수이고, 중지의 자의성이나
        # 예비의 목적처럼 한 갈래에만 있는 요건은 아직 제기된 논점이 아니다.
        shared = collections.Counter(
            ref for name in open_states for ref in state_refs[name]
        )
        scope = frozenset(ref for ref, count in shared.items() if count > 1)
    return tuple(v for v in values if v.predicate_ref in scope) or values


def _gate_failed(result: Mapping[str, Any]) -> bool:
    return any(
        (result.get(stage) or {}).get("gate_state") == "fails"
        for stage in ("elements", "unlawfulness", "culpability", "punishability")
    )


def _final_state(
    result: Mapping[str, Any],
    ref: str,
    retained: frozenset[str],
    absorbed: frozenset[str],
    withheld: frozenset[str],
    has_blocking: bool,
) -> str:
    if ref in absorbed:
        return ABSORBED
    if ref in withheld:
        return NOT_ATTRIBUTABLE
    if ref in retained:
        return ESTABLISHED
    # An instance whose decisive stage never resolved is not an acquittal.  UNKNOWN is not
    # FALSE, and the writer must be able to tell the two apart.
    if _gate_failed(result):
        return NOT_ESTABLISHED
    # Nothing decided against this instance and nothing established it either.  Falling
    # through to "not established" here would turn every instance the run simply never
    # reached into an acquittal -- the exact conversion the contract exists to prevent.
    return UNRESOLVED


def _episode_quotes(
    binding_row: Mapping[str, Any],
    occurrence_id: str,
    plan_row: Mapping[str, Any] | None = None,
) -> tuple[str, ...]:
    """Exact action spans behind one realization's planner provenance."""
    source_ids: set[str] = set()
    action_ids: set[str] = set()
    if plan_row:
        for provenance in plan_row.get("instance_provenance") or ():
            instance = provenance.get("instance_key") or {}
            if str(instance.get("occurrence_id", "")) != occurrence_id:
                continue
            source_ids.update(
                str(value) for value in provenance.get("source_binding_ids") or ()
            )
            focal = provenance.get("focal_action_id")
            if focal:
                action_ids.add(str(focal))
            action_ids.update(
                str(value) for value in provenance.get("supporting_action_ids") or ()
            )
    for seed in binding_row.get("seed_results") or []:
        for binding in seed.get("bindings") or []:
            if str(binding.get("binding_id", "")) not in source_ids:
                continue
            focal_action_id = binding.get("focal_action_id")
            if focal_action_id and str(focal_action_id) not in action_ids:
                # The plan provenance above normally covers this.  Preserve a
                # binding's own action reference for detached participation joins.
                action_ids.add(str(focal_action_id))
            action_ids.update(
                str(value) for value in binding.get("supporting_action_ids") or ()
            )
    quotes: list[str] = []
    for episode in binding_row.get("factual_episodes") or []:
        for action in episode.get("factual_actions") or []:
            if str(action.get("factual_action_id", "")) not in action_ids:
                continue
            for fragment in action.get("source_fragments") or []:
                quote = str(fragment.get("source_quote", "")).strip()
                if quote and quote not in quotes:
                    quotes.append(quote)
    # Participation instances are authored by the planner rather than Call 1.5, so they
    # have no seed binding to follow.  The planner nevertheless records their exact
    # source span in ``occurrences``.  Use it only as a provenance fallback: direct and
    # derived source bindings above remain the preferred, narrower evidence carrier.
    if not quotes and plan_row:
        for occurrence in plan_row.get("occurrences") or ():
            if str(occurrence.get("occurrence_id", "")) != occurrence_id:
                continue
            quote = str(occurrence.get("source_text", "")).strip()
            if quote:
                quotes.append(quote)
            break
    return tuple(quotes)


def _participation_route(
    registry: DefinitionRegistry, result: Mapping[str, Any]
) -> ParticipationRoute | None:
    """Recover the accessory route from the stage provenance.

    Losing this turns an instigator into a principal in the written answer, so a mode
    without its principal is refused rather than emitted half-formed.
    """
    mode: str | None = None
    for stage_name in ("elements", "unlawfulness", "culpability", "punishability"):
        stage = result.get(stage_name) or {}
        for outcome in stage.get("provenance") or []:
            obligation = outcome.get("obligation") or {}
            if "mode" in obligation:
                mode = str(obligation["mode"])
    if mode is None:
        return None
    return ParticipationRoute(
        mode=mode,
        principal_actor=None,
        principal_offense=None,
        principal_realization=None,
    )


def _ground_fact_episode_map(
    binding_row: Mapping[str, Any],
    plan_row: Mapping[str, Any] | None,
) -> dict[str, str]:
    """occurrence_id -> factual_episode_id, the identity Call 2 canonicalizes GroundFacts on.

    A real Call 1.5 binding carries its episode directly on itself in `binding_row`.  A
    binding the planner derived (a `derived_binding:*` occurrence_id) has no entry there;
    its episode only exists in the planner's `InstanceProvenance`, which is why `plan_row`
    is accepted and, where given, is authoritative -- it is exactly what generated the Call 2
    request. An occurrence absent from both stays unmapped rather than guessed.
    """
    mapping: dict[str, str] = {}
    for seed in binding_row.get("seed_results") or []:
        for binding in seed.get("bindings") or []:
            binding_id = binding.get("binding_id")
            episode_id = binding.get("factual_episode_id")
            if binding_id and episode_id:
                mapping[str(binding_id)] = str(episode_id)
    if plan_row:
        for entry in plan_row.get("instance_provenance") or []:
            occurrence_id = (entry.get("instance_key") or {}).get("occurrence_id")
            episode_id = entry.get("factual_episode_id")
            if occurrence_id and episode_id:
                mapping[str(occurrence_id)] = str(episode_id)
    return mapping


def _ground_fact_carrier_map(
    plan_row: Mapping[str, Any] | None,
) -> dict[tuple[str, str, str, str, str], str] | None:
    """Logical target -> factual carrier from an action-realization plan."""
    if not plan_row or plan_row.get("assessment_carriers") is None:
        return None
    mapping: dict[tuple[str, str, str, str, str], str] = {}
    for value in plan_row.get("assessment_carriers") or ():
        instance = value.get("instance_key") or {}
        key = (
            str(instance.get("case_id", "")),
            str(instance.get("actor_id", "")),
            str(instance.get("offense_ref", "")),
            str(instance.get("occurrence_id", "")),
            str(value.get("predicate_ref", "")),
        )
        carrier_id = value.get("carrier_id")
        if not all(key) or not isinstance(carrier_id, str) or not carrier_id:
            raise AnswerPlanError("malformed action-realization carrier provenance")
        if key in mapping:
            raise AnswerPlanError("duplicate action-realization carrier provenance")
        mapping[key] = carrier_id
    return mapping


def _check_ground_fact_canonicalization(
    registry: DefinitionRegistry,
    truth_rows: Sequence[Mapping[str, Any]],
    episode_by_occurrence: Mapping[str, str],
    carrier_by_target: Mapping[tuple[str, str, str, str, str], str] | None = None,
) -> None:
    """Refuse a plan built on a GroundFact that disagrees with itself about one episode.

    `truth_rows` is both carriers concatenated -- `case_truths` and `assessments`.  Rows
    repeated across the two agree and cost nothing; a disagreement between them is itself a
    conflict worth refusing, since the two feed different downstream stages.

    This is a corruption detector, not a repair path.  A well-formed Call 2 artifact cannot
    trip it, because occurrence-level GroundFact canonicalization already asks each
    (case, actor, factual_episode, ground_predicate) once and projects the single answer to
    every consuming offense instance.  Firing here means that guarantee did not hold for the
    artifact the plan was built from -- an older run, or a defect in a newer one -- and the
    plan does not get to pick a side by majority, polarity, or UNKNOWN downgrade.  An
    occurrence this guard cannot place in an episode is not evidence either way, so it is
    skipped rather than treated as a conflict.
    """
    seen: dict[tuple[str, str, str, str], tuple[str, str]] = {}
    conflicts: list[str] = []
    for row in truth_rows:
        predicate_ref = str(row.get("predicate_ref", ""))
        if not predicate_ref or registry.kind_of(predicate_ref) != "ground_fact":
            continue
        instance = row.get("instance_key") or {}
        case_id = str(instance.get("case_id", ""))
        actor_id = str(instance.get("actor_id", ""))
        offense_ref = str(instance.get("offense_ref", ""))
        occurrence_id = str(instance.get("occurrence_id", ""))
        if carrier_by_target is not None:
            scope_id = carrier_by_target.get(
                (case_id, actor_id, offense_ref, occurrence_id, predicate_ref)
            )
            if scope_id is None:
                raise AnswerPlanError(
                    "action-realization plan lacks a GroundFact carrier for "
                    f"{predicate_ref} @ {occurrence_id}"
                )
        else:
            scope_id = episode_by_occurrence.get(occurrence_id)
            if scope_id is None:
                continue
        truth = str(row.get("truth", ""))
        key = (case_id, actor_id, scope_id, predicate_ref)
        if key in seen:
            prior_truth, prior_occurrence = seen[key]
            if prior_truth != truth:
                conflicts.append(
                    f"{predicate_ref} @ {scope_id} ({actor_id}): "
                    f"{prior_occurrence}={prior_truth} vs {occurrence_id}={truth}"
                )
        else:
            seen[key] = (truth, occurrence_id)
    if conflicts:
        raise AnswerPlanError(
            "CROSS_INSTANCE_GROUND_FACT_CONFLICT: " + "; ".join(sorted(conflicts))
        )


def build_answer_plan(
    *,
    case_id: str,
    case_text: str,
    question: str,
    binding_row: Mapping[str, Any],
    call2_row: Mapping[str, Any],
    e2e_row: Mapping[str, Any],
    registry: DefinitionRegistry,
    offense_labels: Mapping[str, str] | None = None,
    representation_gaps: Sequence[str] = (),
    contested_points: Mapping[str, Sequence[ContestedPoint]] | None = None,
    rule_statements: Mapping[tuple[str, str], Sequence[RuleStatement]] | None = None,
    plan_row: Mapping[str, Any] | None = None,
) -> AnswerPlan:
    """Assemble one case's plan from the three canonical artifacts.

    ``contested_points`` is injected by the caller keyed on ``issue_id`` and
    ``rule_statements`` on ``(issue_id, predicate_ref)`` -- the pair SPEC 5.5 searches
    for -- so their provenance is decided outside this projection.  Nothing is
    invented here when they are absent -- an empty slot means the answer simply will not
    be prompted for that discussion.  ``plan_row`` is the optional Step 8 planner artifact
    row; it extends the GroundFact conflict guard's episode identity to derived bindings.
    """
    contested_points = contested_points or {}
    rule_statements = rule_statements or {}

    final = e2e_row.get("final_responsibility") or {}
    retained = frozenset(instance_ref(i) for i in final.get("retained_instances") or [])
    absorbed_records = final.get("absorbed_instances") or []
    absorbed = frozenset(
        instance_ref(record["instance"]) for record in absorbed_records
    )
    withheld = frozenset(
        instance_ref(i) for i in final.get("attribution_withheld_instances") or []
    )
    # `case_truths` is the authority: it is what Scallop and the final-responsibility stage
    # consumed to reach the conclusions this plan restates.  `assessments` is the raw output
    # of one Call 2 run and stays available as a secondary carrier for neural provenance --
    # exact quotes and per-request evidence -- which no truth is invented from.
    truths = call2_row.get("case_truths") or []
    assessments = call2_row.get("assessments") or []
    episodes = _ground_fact_episode_map(binding_row, plan_row)
    carriers = _ground_fact_carrier_map(plan_row)
    _check_ground_fact_canonicalization(
        registry,
        (*truths, *assessments),
        episodes,
        carrier_by_target=carriers,
    )

    issues: list[AnchoredIssue] = []
    for entry in e2e_row.get("liability_results") or []:
        instance = entry.get("instance_key") or {}
        result = entry.get("result") or {}
        ref = instance_ref(instance)
        offense_ref = str(instance.get("offense_ref", ""))
        satisfied, failed, blocking = _findings_for_instance(
            registry, truths, ref, {}, rule_statements, offense_ref
        )
        # 결론을 실제로 막고 있는 것만 남긴다. 전체 UNKNOWN closure를 넘기면 사안에서
        # 제기되지도 않은 예비·불능미수까지 쟁점으로 서술된다.
        blocking = live_unresolved_frontier(
            registry, result, offense_ref, blocking, (*satisfied, *failed)
        )
        state = _final_state(result, ref, retained, absorbed, withheld, bool(blocking))
        completion = result.get("completion") or {}
        route = _participation_route(registry, result)
        issue = AnchoredIssue(
            issue_id=ref,
            actor=str(instance.get("actor_id", "")),
            offense_label=offense_label(registry, offense_ref, offense_labels),
            governing_provision=governing_provision(registry, offense_ref),
            episode_quotes=_episode_quotes(
                binding_row,
                str(instance.get("occurrence_id", "")),
                plan_row,
            ),
            final_state=state,
            completion_state=completion.get("state"),
            completion_why=None,
            participation=route,
            decisive_stage=result.get("decisive_stage"),
            satisfied=satisfied,
            failed=failed,
            blocking=blocking,
            doctrines=tuple(_doctrines_for(e2e_row, ref)),
            contested_points=tuple(contested_points.get(ref, ())),
            gate_failed=_gate_failed(result),
        )
        issues.append(issue)

    plan = AnswerPlan(
        case_id=case_id,
        case_text=case_text,
        question=question,
        discussion_order=tuple(_discussion_order(issues, absorbed_records)),
        anchored_issues=tuple(issues),
        required_final_conclusions=tuple(_required_final_conclusions(issues)),
        final_responsibility=FinalResponsibility(
            retained=tuple(
                {
                    "actor": str(i.get("actor_id", "")),
                    "offense": offense_label(
                        registry, str(i.get("offense_ref", "")), offense_labels
                    ),
                }
                for i in final.get("retained_instances") or []
            ),
            absorbed=tuple(_absorption_records(registry, absorbed_records, offense_labels)),
            concurrence_relations=tuple(
                _relation_records(
                    registry, final.get("concurrence_relations") or [], offense_labels
                )
            ),
            imaginative_pairs=tuple(
                _pair_records(registry, final.get("imaginative_concurrence_pairs") or [], offense_labels)
            ),
            excess_attributions=tuple(
                _excess_records(registry, final.get("excess_attributions") or [], offense_labels)
            ),
            status_redirections=tuple(
                _redirection_records(registry, final.get("status_redirections") or [], offense_labels)
            ),
        ),
        representation_gaps=tuple(representation_gaps),
        unmapped_instances=(),
    )
    check_contracts(plan)
    return plan


def _doctrines_for(e2e_row: Mapping[str, Any], ref: str) -> list[Mapping[str, Any]]:
    """Active doctrines only.  A doctrine that was raised but never fired is not law here."""
    out: list[Mapping[str, Any]] = []
    for doctrine in e2e_row.get("active_doctrines") or []:
        instance = doctrine.get("instance") or doctrine.get("instance_key") or {}
        if instance and instance_ref(instance) != ref:
            continue
        out.append(doctrine)
    return out


def _absorption_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None = None,
) -> list[Mapping[str, Any]]:
    """Both sides of every absorbed pair.

    Dropping the absorbed offence from the plan would make it disappear from the answer,
    and an answer that never says why the lesser offence does not stand separately has
    simply omitted a point it was supposed to make.
    """
    out: list[Mapping[str, Any]] = []
    for record in records:
        absorbed_instance = record.get("instance") or {}
        absorbing_instance = record.get("absorbed_by") or {}
        out.append(
            {
                "absorbed_offense": offense_label(
                    registry, str(absorbed_instance.get("offense_ref", "")), offense_labels
                ),
                "absorbing_offense": offense_label(
                    registry, str(absorbing_instance.get("offense_ref", "")), offense_labels
                )
                if absorbing_instance
                else None,
                "relation": record.get("relation") or record.get("kind"),
                "condition_statement": record.get("condition_statement"),
                "legal_standard": record.get("legal_standard"),
            }
        )
    return out


def _excess_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    """Say who is not answerable for what, in offence names rather than in refs."""
    out: list[Mapping[str, Any]] = []
    for record in records:
        accessory = record.get("accessory_instance") or {}
        out.append(
            {
                "actor": str(accessory.get("actor_id", "")),
                "accessory_offense": offense_label(
                    registry, str(accessory.get("offense_ref", "")), offense_labels
                ),
                "excess_offense": offense_label(
                    registry, str(record.get("excess_offense_ref", "")), offense_labels
                ),
                "effect": str(record.get("effect", "")),
            }
        )
    return out


#: 답안에 나갈 수 있는 죄수관계. **확정된 것만** 있다.
#:
#: `*_candidate`는 실려 오지만 여기 없다. 초점행위가 다르다는 구조적 사실은 형법 제40조가
#: 묻는 "사회관념상 한 개의 행위인지"에 대한 답이 아니고, 상상적 경합 규칙에 걸리지 않았다는
#: 사실을 실체적 경합의 근거로 쓰는 것은 부존재를 적극적 사실로 쓰는 일이다. 후보는 symbolic
#: 산출물에 provenance로 남고, 확정은 저작이나 별도의 typed 판단이 한다.
_RELATION_PROSE = {
    "imaginative_concurrence": "상상적 경합",
}


def _relation_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    """죄수관계를 법률가가 쓰는 이름으로 바꾼다. 모르는 관계 이름은 내보내지 않는다."""
    out: list[Mapping[str, Any]] = []
    for record in records:
        relation = _RELATION_PROSE.get(str(record.get("relation", "")))
        if relation is None:
            continue
        first = record.get("first_instance") or {}
        second = record.get("second_instance") or {}
        out.append(
            {
                "actor": str(first.get("actor_id", "")),
                "first_offense": offense_label(
                    registry, str(first.get("offense_ref", "")), offense_labels
                ),
                "second_offense": offense_label(
                    registry, str(second.get("offense_ref", "")), offense_labels
                ),
                "relation": relation,
            }
        )
    return out


def _pair_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    out: list[Mapping[str, Any]] = []
    for record in records:
        first = record.get("first_instance") or {}
        second = record.get("second_instance") or {}
        out.append(
            {
                "first_offense": offense_label(
                    registry, str(first.get("offense_ref", "")), offense_labels
                ),
                "second_offense": offense_label(
                    registry, str(second.get("offense_ref", "")), offense_labels
                ),
            }
        )
    return out


def _redirection_records(
    registry: DefinitionRegistry,
    records: Sequence[Mapping[str, Any]],
    offense_labels: Mapping[str, str] | None,
) -> list[Mapping[str, Any]]:
    """Article 33 proviso: the participant answers under a different offence."""
    out: list[Mapping[str, Any]] = []
    for record in records:
        instance = record.get("accessory_instance") or {}
        base_offense_ref = str(record.get("base_offense_ref", ""))
        aggravated_offense_ref = str(record.get("aggravated_offense_ref", ""))
        out.append(
            {
                "actor": str(instance.get("actor_id", "")),
                "from_offense": offense_label(
                    registry, base_offense_ref, offense_labels
                ),
                "to_offense": offense_label(
                    registry, aggravated_offense_ref, offense_labels
                ),
            }
        )
    return out


def _discussion_order(
    issues: Sequence[AnchoredIssue], absorbed_records: Sequence[Mapping[str, Any]]
) -> list[str]:
    """Order issues so a prerequisite is never discussed after what depends on it.

    Only one dependency is representable today: an absorbed offence has to be settled
    before the offence that absorbs it can be stated as the final one.
    """
    order = [issue.issue_id for issue in issues]
    absorbed_first = {
        instance_ref(record["instance"]): instance_ref(record["absorbed_by"])
        for record in absorbed_records
    }
    for absorbed_ref, absorbing_ref in absorbed_first.items():
        if absorbed_ref not in order or absorbing_ref not in order:
            continue
        if order.index(absorbed_ref) > order.index(absorbing_ref):
            order.remove(absorbed_ref)
            order.insert(order.index(absorbing_ref), absorbed_ref)
    return order


# --------------------------------------------------------------------------------------
# contracts
# --------------------------------------------------------------------------------------


def check_contracts(plan: AnswerPlan) -> None:
    """Refuse a plan that would mislead the writer.  ANSWERPLAN_SPEC section 4."""
    for issue in plan.anchored_issues:
        if issue.participation is not None and not issue.participation.mode:
            raise AnswerPlanError(f"{issue.issue_id}: participation without a mode")
        if issue.final_state == NOT_ESTABLISHED and not issue.gate_failed:
            # The run deciding against an instance is what makes an acquittal sayable.  A
            # gate can fail on a relation obligation rather than on a predicate, so the
            # predicate lists are not evidence either way -- only the gate is.
            raise AnswerPlanError(
                f"{issue.issue_id}: unresolved elements reported as not established"
            )
        for point in issue.contested_points:
            if point.origin not in _ALLOWED_CONTESTED_ORIGINS:
                raise AnswerPlanError(f"{issue.issue_id}: contested point from {point.origin!r}")
        for finding in (*issue.satisfied, *issue.failed, *issue.blocking):
            for statement in finding.rule_statements:
                if statement.origin not in _ALLOWED_CONTESTED_ORIGINS:
                    raise AnswerPlanError(
                        f"{issue.issue_id}: rule statement from {statement.origin!r}"
                    )
    for record in plan.final_responsibility.absorbed:
        if not record.get("absorbed_offense") or not record.get("absorbing_offense"):
            raise AnswerPlanError("absorbed pair is missing one of its two sides")


def assert_no_internal_markers(payload: str) -> None:
    """The serialized analysis must read as law, not as machine state."""
    found = [marker for marker in _INTERNAL_MARKERS if marker in payload]
    if found:
        raise AnswerPlanError(f"internal markers leaked into the Call 3 payload: {found}")


def assert_no_rubric_fields(payload: Mapping[str, Any] | str) -> None:
    """No field may carry this question's rubric item count or score.

    Hiding the rubric text is not enough.  "37 items, 30 points" is a per-question gold
    annotation, and handing it to the generator would make the answer length a function of
    the grading key rather than of the analysis.
    """
    blob = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    for marker in ("rubric_item_count", "rubric_count", "rubric_summary", "\"score\""):
        if marker in blob:
            raise AnswerPlanError(f"rubric-derived field {marker!r} reached the answer plan")


# --------------------------------------------------------------------------------------
# serialization for the model
# --------------------------------------------------------------------------------------

_STATE_PROSE = {
    ESTABLISHED: "성립한다.",
    NOT_ESTABLISHED: "성립하지 않는다.",
    UNRESOLVED: "주어진 사실만으로는 성부를 확정하기 어렵다.",
    NOT_ATTRIBUTABLE: "이 행위자에게 귀속되지 않는다.",
    ABSORBED: "따로 성립하지 않는다. 다른 죄에 흡수된다.",
}

#: Participation modes in the words a Korean criminal-law answer uses for them.
_MODE_PROSE = {
    "co_principal": "공동정범",
    "instigator": "교사범",
    "aider": "방조범",
}

_COMPLETION_PROSE = {
    "completed": "기수",
    "attempted": "미수",
    "abandoned_attempt": "중지미수",
    "impossible_attempt": "불능미수",
    "preparation": "예비",
}


def occurrence_hints(issues: Sequence[AnchoredIssue]) -> dict[str, str]:
    """같은 행위자의 같은 죄가 두 번 열렸을 때 둘을 갈라 부르는 우리말 표지.

    occurrence를 합치지 않는 것은 서로 다른 행위이기 때문이다. 그런데 답안에는 죄명만
    나가므로 결론 목록에 "甲 — 강간죄"가 상반된 상태로 두 번 실리고, 채점자에게는 하나의
    죄에 대한 모순으로 읽힌다. 갈라 부르되 죄명은 건드리지 않는다.

    표지는 그 행위의 사건 원문 인용에서 가져온다 -- 지어내지 않고, 내부 식별자도 쓰지
    않는다. 두 행위가 같은 인용을 공유해 구별이 서지 않으면 등장 순서로 부른다.
    """
    grouped: dict[tuple[str, str], list[AnchoredIssue]] = {}
    for issue in issues:
        grouped.setdefault((issue.actor, issue.offense_label), []).append(issue)
    hints: dict[str, str] = {}
    for members in grouped.values():
        if len(members) < 2:
            continue
        for position, issue in enumerate(members, start=1):
            others = {
                quote for other in members if other is not issue for quote in other.episode_quotes
            }
            distinctive = next(
                (quote for quote in issue.episode_quotes if quote not in others), ""
            )
            hints[issue.issue_id] = (
                f'"{distinctive}" 행위' if distinctive else f"{position}번째 행위"
            )
    return hints


def _required_final_conclusions(
    issues: Sequence[AnchoredIssue],
) -> tuple[RequiredFinalConclusion, ...]:
    """One anchor per anchored issue, reusing the exact vocabulary `analysis` is written in.

    Anchor and analysis body share `_STATE_PROSE`/`_COMPLETION_PROSE`/`_MODE_PROSE` on
    purpose -- an anchor list in different words than the body would just relocate the
    drift this list exists to prevent, rather than remove it.
    """
    hints = occurrence_hints(issues)
    out: list[RequiredFinalConclusion] = []
    for issue in issues:
        out.append(
            RequiredFinalConclusion(
                actor=issue.actor,
                offense_label=issue.offense_label,
                occurrence_hint=hints.get(issue.issue_id),
                state=_STATE_PROSE.get(issue.final_state, issue.final_state),
                completion_state=_COMPLETION_PROSE.get(issue.completion_state)
                if issue.completion_state in _COMPLETION_PROSE
                else None,
                participation_mode=(
                    _MODE_PROSE.get(issue.participation.mode, issue.participation.mode)
                    if issue.participation is not None
                    else None
                ),
            )
        )
    return tuple(out)


def serialize_analysis(plan: AnswerPlan) -> str:
    """Render the plan as the prose block the prompt calls ``analysis``.

    Field names do not reach the model.  What reaches it is a lawyer's reading of the same
    content, in the discussion order the plan fixed.
    """
    by_id = {issue.issue_id: issue for issue in plan.anchored_issues}
    hints = occurrence_hints(plan.anchored_issues)
    lines: list[str] = []
    for position, issue_id in enumerate(plan.discussion_order, start=1):
        issue = by_id.get(issue_id)
        if issue is None:
            continue
        lines.extend(_serialize_issue(position, issue, hints.get(issue.issue_id)))
        lines.append("")
    lines.extend(_serialize_final(plan.final_responsibility))
    payload = "\n".join(lines).strip() + "\n"
    assert_no_internal_markers(payload)
    assert_no_rubric_fields(payload)
    return payload


def _serialize_issue(
    position: int, issue: AnchoredIssue, occurrence_hint: str | None = None
) -> list[str]:
    head = f"[{position}] {issue.actor} — {issue.offense_label}"
    if issue.governing_provision:
        head += f" ({issue.governing_provision})"
    # 같은 죄가 두 행위로 열렸으면 어느 행위에 대한 항목인지 여기서 갈라 부른다.
    if occurrence_hint:
        head += f" — {occurrence_hint}"
    lines = [head, f"    결론: {_STATE_PROSE.get(issue.final_state, issue.final_state)}"]
    if issue.absorbed_into:
        lines.append(f"        흡수되는 죄: {issue.absorbed_into}")
        if issue.absorption_reason:
            lines.append(f"        흡수 근거: {issue.absorption_reason}")
    if issue.not_attributable_reason:
        lines.append(f"        귀속되지 않는 이유: {issue.not_attributable_reason}")
    if issue.participation is not None:
        mode = issue.participation.mode
        lines.append(f"    가담 형태: {_MODE_PROSE.get(mode, mode)}")
        if issue.participation.principal_actor:
            lines.append(f"        정범: {issue.participation.principal_actor}")
        if issue.participation.principal_offense:
            lines.append(f"        정범의 죄: {issue.participation.principal_offense}")
    if issue.completion_state in _COMPLETION_PROSE:
        lines.append(f"    기수 여부: {_COMPLETION_PROSE[issue.completion_state]}")
    elif issue.completion_state:
        # An unresolved completion is not a stage word to be echoed at the writer.  It is
        # one more thing the facts did not settle, and it is said that way or not at all.
        lines.append("    기수 여부: 주어진 사실만으로는 확정하기 어렵다.")
    if issue.episode_quotes:
        lines.append("    관련 사실")
        for quote in issue.episode_quotes:
            lines.append(f"      · \"{quote}\"")
    lines.extend(_serialize_findings("인정된 요건", issue.satisfied))
    lines.extend(_serialize_findings("인정되지 않은 요건", issue.failed))
    lines.extend(_serialize_findings("확정되지 않은 요건", issue.blocking))
    for point in issue.contested_points:
        lines.append(f"    견해가 갈리는 지점: {point.label}")
        for stance in point.positions:
            lines.append(f"        · {stance}")
        lines.append(f"        채택: {point.adopted} — {point.why_adopted}")
    for doctrine in issue.doctrines:
        label = doctrine.get("display_name") or doctrine.get("label")
        if label:
            lines.append(f"    적용되는 법리: {label}")
    return lines


def _serialize_findings(title: str, findings: Sequence[Finding]) -> list[str]:
    if not findings:
        return []
    lines = [f"    {title}"]
    for finding in findings:
        lines.append(f"      · {finding.label}")
        if finding.legal_standard and finding.legal_standard != finding.label:
            lines.append(f"        판단 기준: {finding.legal_standard}")
        if finding.governing_provision:
            lines.append(f"        근거 조문: {finding.governing_provision}")
        for statement in finding.rule_statements:
            mark = "[판례 법리]" if statement.origin == "reviewed_card" else "[법리]"
            lines.append(f"        {mark} {statement.statement}")
        for quote in finding.supporting_quotes:
            lines.append(f"        근거 사실: \"{quote}\"")
    return lines


def _serialize_final(final: FinalResponsibility) -> list[str]:
    lines = ["최종 죄책"]
    if final.retained:
        # Grouped by actor: two actors answering for theft is not one conclusion said
        # twice, and an answer that loses the actor loses the conclusion.
        by_actor: dict[str, list[str]] = {}
        for record in final.retained:
            by_actor.setdefault(record["actor"], []).append(record["offense"])
        for actor, offenses in by_actor.items():
            lines.append(f"    {actor}: {', '.join(offenses)}")
    else:
        lines.append("    성립이 확정된 죄가 없다.")
    for record in final.absorbed:
        relation = record.get("relation") or "흡수"
        lines.append(
            f"    {record['absorbed_offense']}는 {record['absorbing_offense']}에 "
            f"{relation} 관계로 흡수되어 따로 성립하지 않는다."
        )
        if record.get("condition_statement"):
            lines.append(f"        흡수 근거: {record['condition_statement']}")
    for record in final.concurrence_relations:
        lines.append(
            f"    {record['actor']}의 {record['first_offense']}와 {record['second_offense']}는 "
            f"{record['relation']} 관계다."
        )
    known = {
        (record["first_offense"], record["second_offense"])
        for record in final.concurrence_relations
    }
    for pair in final.imaginative_pairs:
        if (pair["first_offense"], pair["second_offense"]) in known:
            continue
        lines.append(
            f"    {pair['first_offense']}와 {pair['second_offense']}는 상상적 경합 관계다."
        )
    for attribution in final.excess_attributions:
        lines.append(
            f"    {attribution['actor']}의 {attribution['accessory_offense']} 가담 범위를 "
            f"넘는 {attribution['excess_offense']} 부분은 그에게 귀속되지 않는다."
        )
    for redirection in final.status_redirections:
        target = redirection.get("to_offense")
        if target:
            lines.append(
                f"    {redirection['actor']}는 신분에 따라 {redirection['from_offense']}가 "
                f"아니라 {target}의 죄책을 진다."
            )
    return lines


def serialize_open_points(plan: AnswerPlan) -> str:
    """분석이 다루지 못한 것으로 **host가 실제로 아는** 공백. 없으면 빈 문자열이다.

    예전에는 비었을 때 "다루지 않은 영역으로 특정된 것은 없다"고 적었다. 그것은 분석의
    완결성을 적극적으로 선언하는 문장인데, host는 그것을 알 수 없다 -- 26문항 전부가 이
    문장을 달고 나갔고, 그 중에는 Call 1이 죄명 자체를 잡지 못해 주거침입죄가 통째로 빠진
    문항도 있었다. 미포착은 부존재가 아니다.

    반대로 빠진 죄명을 host가 추정해 채우지도 않는다. Call 1이 못 잡은 쟁점은 여기서도 알
    방법이 없다. 아는 공백만 적고, 아무것도 없으면 섹션 자체를 비워 caller가 생략하게 한다.
    """
    lines: list[str] = []
    for gap in plan.representation_gaps:
        lines.append(f"· {gap}")
    for instance in plan.unmapped_instances:
        lines.append(f"· {instance}")
    return "\n".join(lines)


def serialize_required_final_conclusions(plan: AnswerPlan) -> str:
    """The closed list the closing paragraph must restate -- anchors, not sentences.

    Each line names an actor, an offence, and the one conclusion word for it.  The model
    still composes the sentence; this only fixes what the sentence has to say, so a
    closing paragraph that drops or inverts one of these is checkably wrong rather than
    merely a stylistic choice.
    """
    lines: list[str] = []
    for item in plan.required_final_conclusions:
        # 결박된 성립·불성립은 그대로 다시 말하게 하고, 결박하지 못한 것은 그 사실만 알린다.
        # 유보 문장을 앵커로 주면 프롬프트가 논증 뒤 결론을 요구하는 것과 정면으로 어긋나고,
        # 모델은 둘 중 앵커를 따른다. 이 줄은 "무엇을 빠뜨리지 말라"만 정하고 결론은 정하지
        # 않는다 -- 완결성 감사도 행위자와 죄명만 본다.
        state = (
            "성부는 본문의 논증에 따라 결론낸다. 그 결론을 결론 문단에도 반드시 올린다."
            if item.state == _STATE_PROSE[UNRESOLVED]
            else item.state
        )
        line = f"· {item.actor} — {item.offense_label}: {state}"
        if item.completion_state:
            line += f" ({item.completion_state})"
        if item.participation_mode:
            line += f" [{item.participation_mode}]"
        # 표지는 죄명 뒤가 아니라 줄 끝에 붙인다. 죄명 토큰을 건드리면 완결성 감사가 답안에서
        # 그 죄를 찾지 못해 멀쩡한 결론을 누락으로 신고한다.
        if item.occurrence_hint:
            line += f" [{item.occurrence_hint}에 관한 결론]"
        lines.append(line)
    payload = "\n".join(lines) if lines else "없음"
    assert_no_internal_markers(payload)
    assert_no_rubric_fields(payload)
    return payload


_ARTICLE = re.compile(r"^제\s*\d")


def _split_citations(value: str | None) -> list[str]:
    """`"형법 제250조; 제267조"` -> `["형법 제250조", "형법 제267조"]`.

    세미콜론으로 뭉친 저작을 canonical citation 단위로 나누고, 뒤쪽 조각이 잃어버린 법령명을
    앞 조각에서 물려준다. 이것을 하지 않으면 답안에 벌거벗은 조문번호가 그대로 나간다 --
    26문항에서 30건이 그랬다.
    """
    if not value:
        return []
    output: list[str] = []
    statute = "형법"
    for piece in value.split(";"):
        text = piece.strip()
        if not text:
            continue
        if _ARTICLE.match(text):
            text = f"{statute} {text}"
        else:
            head = text.split(maxsplit=1)
            if head and not _ARTICLE.match(head[0]):
                statute = head[0]
        output.append(text)
    return output


def _drop_less_specific(citations: Sequence[str]) -> tuple[str, ...]:
    """같은 조문의 조·항이 함께 실리면 더 구체적인 쪽만 남긴다.

    `형법 제319조`와 `형법 제319조 제1항`을 둘 다 인용하라고 시키면 같은 조문을 두 번 대게
    된다. 26문항에서 28쌍이 그랬다.
    """
    values = tuple(dict.fromkeys(citations))
    return tuple(
        value
        for value in values
        if not any(other != value and other.startswith(f"{value} ") for other in values)
    )


def issue_authorities(issue: AnchoredIssue) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`(그 죄의 조문, 그 쟁점에서 쓰인 법리의 근거)`.

    둘을 나누는 이유는 하나다. `result_causation` 같은 죄를 가리지 않는 요소의 조문이 그
    요소를 쓰는 모든 죄로 번져, 살인죄 논증에서 과실치사 조문을 인용하게 만들고 있었다.
    죄의 조문은 그 죄가 대고, 요소·법리의 근거는 그 요소를 논하는 자리에서만 쓴다.
    """
    statutory = _drop_less_specific(_split_citations(issue.governing_provision))
    doctrinal: list[str] = []
    for finding in (*issue.satisfied, *issue.failed, *issue.blocking):
        doctrinal.extend(_split_citations(finding.governing_provision))
    return statutory, tuple(
        value for value in _drop_less_specific(doctrinal) if value not in statutory
    )


def serialize_required_authorities(plan: AnswerPlan) -> str:
    """쟁점별로 묶인 근거. 전역 닫힌 목록이 아니다.

    이 목록은 새 권위를 더하거나 판단하지 않는다. 이미 쟁점에 붙어 있는 근거를 그 쟁점
    안에서만 쓰도록 범위를 정할 뿐이고, 반드시 인용해야 하는 것은 그 죄의 조문이다.
    """
    lines: list[str] = []
    for issue in plan.anchored_issues:
        statutory, doctrinal = issue_authorities(issue)
        if not statutory and not doctrinal:
            continue
        lines.append(f"[{issue.actor} — {issue.offense_label}]")
        for value in statutory:
            lines.append(f"· {value}")
        for value in doctrinal:
            lines.append(f"  (관련 법리) {value}")
    payload = "\n".join(lines)
    if not payload:
        return ""
    assert_no_internal_markers(payload)
    assert_no_rubric_fields(payload)
    return payload


def missing_required_authorities(
    answer_text: str, required_authorities: str
) -> tuple[str, ...]:
    """Return authored citation anchors absent from the generated answer.

    This is deliberately an exact presence audit.  It neither repairs a citation nor
    treats a different provision as equivalent, because the closed list already carries
    the exact authored strings the writer received.
    """
    if not required_authorities.strip() or required_authorities.strip() == "없음":
        return ()
    # 강제되는 것은 그 죄의 조문(`· `)뿐이다. 쟁점 머리글과 관련 법리 줄은 그 논증에서 쓰라고
    # 준 맥락이지 빠뜨리면 안 되는 목록이 아니다.
    required = tuple(
        line.removeprefix("·").strip()
        for line in required_authorities.splitlines()
        if line.startswith("·") and line.removeprefix("·").strip() not in ("", "없음")
    )
    return tuple(dict.fromkeys(value for value in required if value not in answer_text))


#: Words that mark a closing-summary heading.  The prompt asks for "최종 죄책과 죄수관계"
#: but leaves the structure to the writer, who numbers and titles it freely -- "III. 최종
#: 결론" and "IV. 결론" are the same section.  Matching whole heading titles instead of
#: these keywords made the audit miss the second form and fall back to the last paragraph,
#: reporting a complete answer as incomplete.
_FINAL_SECTION_KEYWORDS = ("결론", "최종 죄책", "죄수")

#: A heading is a line that does not end as a sentence.  This is what separates the title
#: "IV. 결론" from prose like "...결론을 확정하기 어렵다." that merely contains the word.
_SENTENCE_ENDINGS = (".", "다", "。", ":", "：")

#: Numbered or lettered sub-headings inside a closing section (`1.`, `2)`, `가.`, `나.`).
#: These sit *under* the section's own heading and never start it.
_SUB_HEADING = re.compile(r"^(?:\d+|[가-힣])\s*[.)]\s*\S")


def extract_final_conclusion_section(answer_text: str) -> str:
    """The mechanically-cut tail of the answer the closing-paragraph instruction targets.

    F4 was not an absence from the answer -- the dropped actor's offences were discussed
    in the body -- it was an absence from the *closing* paragraph specifically.  A
    whole-document presence check cannot see that distinction, so this narrows to where
    the closing section begins and takes everything from there onward.

    The cut anchors on a heading line rather than on the last textual match, because these
    keywords also occur inside conclusion sentences ("丙의 최종 죄책은 횡령죄이다"): cutting
    there would start the section midway and report the actors named above it as missing.
    A heading is distinguished from a sentence by not ending as one, which is what
    separates the title "IV. 결론" from prose that merely contains the word.  Absent any
    heading the last paragraph stands in, since an answer that skips the heading still
    ends with some closing block and widening back to the whole document would restore
    the very blind spot this replaces.
    """
    lines = answer_text.splitlines(keepends=True)
    top_level_offset: int | None = None
    heading_offset: int | None = None
    fallback_offset: int | None = None
    offset = 0
    for line in lines:
        stripped = line.strip()
        if any(keyword in stripped for keyword in _FINAL_SECTION_KEYWORDS):
            fallback_offset = offset
            if not stripped.endswith(_SENTENCE_ENDINGS):
                heading_offset = offset
                if not _SUB_HEADING.match(stripped):
                    top_level_offset = offset
        offset += len(line)
    # A closing section carries its own sub-headings -- `III. 죄수 및 최종 결론` followed by
    # `1. 乙의 최종 죄책` and `2. 甲의 최종 죄책`.  Taking the last heading starts the section
    # at the final actor and reports every actor above it as missing, so the section starts
    # at its outermost heading and a sub-heading is used only when there is no outer one.
    start = top_level_offset if top_level_offset is not None else heading_offset
    if start is None:
        start = fallback_offset
    if start is not None:
        return answer_text[start:]
    paragraphs = [part for part in answer_text.split("\n\n") if part.strip()]
    return paragraphs[-1] if paragraphs else answer_text


def missing_required_final_conclusions(
    answer_text: str, plan: AnswerPlan
) -> tuple[RequiredFinalConclusion, ...]:
    """Mechanical presence check scoped to the closing section.  Never edits an answer.

    An anchor counts as covered when both the actor and the offence label occur in the
    closing section `extract_final_conclusion_section` isolates -- not anywhere in the
    document, which would pass even when the closing paragraph itself dropped the issue.
    This cannot tell whether the stated state is the *right* one; that is the fidelity
    contract on `analysis` (F1/F2), not this completeness check's job. A finding here is a
    fact for an offline audit, not a repair signal.
    """
    section = extract_final_conclusion_section(answer_text)
    normalized = _normalize_offense_text(section)
    missing: list[RequiredFinalConclusion] = []
    for item in plan.required_final_conclusions:
        names = offense_label_variants(item.offense_label)
        if item.actor not in section or not any(name in normalized for name in names):
            missing.append(item)
    return tuple(missing)


def parse_required_final_conclusions(
    serialized: str,
) -> tuple[RequiredFinalConclusion, ...]:
    """`serialize_required_final_conclusions`가 쓴 줄을 앵커로 되읽는다.

    Call 3 runner와 오프라인 감사는 둘 다 plan **행**을 읽지 `AnswerPlan` 객체를 들고 있지
    않다. 각자 이 줄을 자기 방식으로 파싱하면 같은 불변식의 두 번째 구현이 생기고, 한쪽만
    고쳐지는 그 결함 클래스로 되돌아간다.
    """
    output: list[RequiredFinalConclusion] = []
    for line in serialized.splitlines():
        body = line.strip()
        if not body.startswith("·"):
            continue
        body = body[1:].strip()
        if "—" not in body or ":" not in body:
            continue
        actor, rest = body.split("—", 1)
        offense, state = rest.split(":", 1)
        output.append(
            RequiredFinalConclusion(actor.strip(), offense.strip(), state.strip())
        )
    return tuple(output)


def missing_final_conclusions(
    answer_text: str, serialized_required: str
) -> tuple[RequiredFinalConclusion, ...]:
    """직렬화된 요구목록 기준의 완결성 감사. 답안을 고치지 않는다.

    `missing_required_final_conclusions`와 같은 규칙을 plan 행에 대해 적용한다. 이것이
    production runner가 부를 수 있는 형태이고, 함수만 있고 아무도 부르지 않아 "프롬프트는
    빠뜨리지 말라고 하고, 모델은 빠뜨리고, host는 그대로 저장"이 가능했던 자리다.
    """
    if not serialized_required.strip() or serialized_required.strip() == "없음":
        return ()
    section = extract_final_conclusion_section(answer_text)
    normalized = _normalize_offense_text(section)
    return tuple(
        item
        for item in parse_required_final_conclusions(serialized_required)
        if item.actor not in section
        or not any(name in normalized for name in offense_label_variants(item.offense_label))
    )


#: Particles a writer inserts into an offence name without changing which offence it is:
#: `위계공무집행방해죄` and `위계에 의한 공무집행방해죄` are the same crime.
_OFFENSE_PARTICLES = ("에의한", "에의하여", "에관한")


def _normalize_offense_text(text: str) -> str:
    stripped = re.sub(r"\s+", "", text)
    for particle in _OFFENSE_PARTICLES:
        stripped = stripped.replace(particle, "")
    return stripped


def offense_label_variants(offense_label: str) -> tuple[str, ...]:
    """Forms of one offence name that all denote the same offence.

    The completeness check would otherwise measure how closely the answer echoes the
    plan's own label rather than whether it named the crime.  That distinction is not
    cosmetic here: a condition whose plan carries more material writes more freely, so an
    echo-sensitive check would report it as less complete for writing better Korean.

    Three rewritings are accepted, all of which preserve identity.  A `·` alternation
    (`공문서위조·변조죄`) may be answered by either branch; the particles above may be
    dropped; and the enumeration marker `등` may be left out, since `현주건조물등방화죄`
    and `현주건조물방화죄` are the same article.  Nothing widens a name into a different
    crime -- callers still match on whole names, so `상해죄` never satisfies `강도상해죄`.
    """
    label = _normalize_offense_text(offense_label)
    variants = {label}
    if "·" in label:
        head, _, tail = label.partition("·")
        variants.add(head if head.endswith("죄") else f"{head}죄")
        variants.add(tail)
    for variant in tuple(variants):
        if "등" in variant:
            variants.add(variant.replace("등", ""))
    return tuple(sorted(variants))
