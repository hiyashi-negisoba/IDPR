"""한 사건의 최종 책임 뷰 -- 성립한 죄들 위에서 한 번만 도는 심볼릭 단계.

인스턴스별 liability chain이 끝난 뒤에도 답이 아직 아니다. 같은 사실에서 나온 두 죄가 각각
성립한 채로 나열되어 있고, 교사한 죄와 실현된 죄가 다른데도 가담자가 실현된 죄로 그대로
걸려 있으며, 어떤 법리는 필요한 입력이 없어 조용히 침묵한다. 이 모듈이 그 마지막 층이다.

**모델을 부르지 않는다.** 네 갈래 전부 이미 받은 truth 아니면 저작된 구조만 읽는다.

1. 경합·흡수 -- 특별관계는 저작된 `derivation.kind == "qualify"`에서, 그 밖의 흡수·상상적
   경합은 승인된 규칙에서만 후보를 연다.
2. 공범의 초과 -- 교사 대상과 실현된 죄를 짝지어 저작된 derivation 구조로 분류한다.
3. 제33조 단서 -- 가감적 신분자의 죄책을 가중죄로 옮긴다. 다만 여기서 계산만 하고,
   적용은 책임 평가 **이전에** 호출자가 한다(`aggravating_status` 모듈 주석 참조).
4. 표현 공백 -- 저작된 정책이 요구하는 입력이 이 사건에 없으면 침묵하지 않고 marker를 남긴다.

4번이 이 모듈의 존재 이유의 절반이다. doctrine activation이 26문항 전부에서 0이었던 것은
Scallop 결함이 아니라 아무도 leaf를 planner target으로 만들지 않은 dead loop였고, 그 사실이
드러나는 데 오래 걸린 이유는 "발화하지 않음"과 "적용되지 않음"이 출력에서 똑같이 보였기
때문이다. 여기서는 두 가지가 다르게 보인다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from idpr.v2.evaluate import UNKNOWN, TruthValue
from idpr.v2.policy_probes import (
    OFFENSE_INSTANCE,
    PARTICIPATION_CANDIDATE,
    unsatisfied_requirements,
)
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.runtime.aggravating_status import (
    AggravatingStatusRedirection,
    redirect_by_aggravating_status,
)
from idpr.v2.runtime.concurrence import (
    ConcurrenceCandidate,
    ConcurrenceResolution,
    ConcurrenceRule,
    plan_concurrence_candidates,
    plan_specialty_candidates,
    resolve_concurrence,
)
from idpr.v2.runtime.excess import (
    LIABLE_FOR_AGGRAVATED_RESULT,
    LIABLE_FOR_INSTIGATED_SCOPE,
    NO_LIABILITY_FOR_EXCESS,
    UNRESOLVED as EXCESS_UNRESOLVED,
    ExcessAssessment,
    classify_excess,
)
from idpr.v2.runtime.excess_candidates import (
    INSTIGATED_PROVENANCE_REF,
    REALIZED_PROVENANCE_REF,
    AccessoryExcessCandidate,
    plan_accessory_excess_candidates,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import LiabilityEvaluation
from idpr.v2.runtime.truths import CaseTruths

UNRESOLVED_STATUS_REDIRECTION_TARGET = "UNRESOLVED_STATUS_REDIRECTION_TARGET"
"""제33조 단서가 옮겨 갈 가중죄 instance가 이 사건의 평가 universe에 없다.

가중죄를 host가 새로 만들어 넣지 않는다. Call 1이 그 죄를 후보로 열지 않았다면 predicate
truth도 없고, 없는 truth 위에서 평가하면 전부 UNKNOWN인 성립을 만들어 내게 된다.
"""


class FinalResponsibilityError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class UnresolvedFinding:
    """발화하지 못한 정책 하나. 법적 부정이 아니라 입력 부재의 기록이다."""

    marker: str
    policy_id: str
    scope: str
    missing_refs: tuple[str, ...] = ()
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "marker": self.marker,
            "policy_id": self.policy_id,
            "scope": self.scope,
            "missing_refs": list(self.missing_refs),
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class ExcessFinding:
    candidate: AccessoryExcessCandidate
    assessment: ExcessAssessment

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.candidate.as_dict(),
            "classification": self.assessment.classification,
            "effect": self.assessment.effect,
            "reason": self.assessment.reason,
        }


ATTRIBUTED = "attributed"
NOT_ATTRIBUTABLE_BY_EXCESS = "NOT_ATTRIBUTABLE_BY_EXCESS"
UNRESOLVED_EXCESS_ATTRIBUTION = "UNRESOLVED_EXCESS_ATTRIBUTION"

_EXCESS_DECISION: Mapping[str, str] = {
    # 교사한 범위까지만 책임진다. 그 범위를 넘은 죄로의 귀속은 열리지 않는다.
    LIABLE_FOR_INSTIGATED_SCOPE: NOT_ATTRIBUTABLE_BY_EXCESS,
    # 결과적 가중범이고 가담자에게 예견가능성이 있었다. 중한 죄로의 귀속이 열린다.
    LIABLE_FOR_AGGRAVATED_RESULT: ATTRIBUTED,
    # 질적 초과. 교사한 죄와 양립하지 않는 죄가 실현됐다.
    NO_LIABILITY_FOR_EXCESS: NOT_ATTRIBUTABLE_BY_EXCESS,
    # 무책으로 접지도, 중한 죄를 세우지도 않는다. 기존 책임은 그대로 두고 초과 귀속만 미정.
    EXCESS_UNRESOLVED: UNRESOLVED_EXCESS_ATTRIBUTION,
}


@dataclass(frozen=True, slots=True)
class ExcessAttribution:
    """초과 판정이 가담자에게 실제로 미치는 효과 하나.

    2026-08-13 검수 확정: 이것은 서술 문제가 아니라 가담자의 책임 범위를 제한하는 심볼릭
    결론이므로 이 단계가 소비한다. 다만 효과의 범위가 좁다는 것이 핵심이다.

    * 가담자의 전체 liability를 뒤집지 않는다. 교사·방조한 죄의 책임은 그대로 유지된다.
    * 초과하여 실현된 죄로 가는 **귀속 edge만** 차단한다.
    * finding 자체는 provenance로 남는다 -- Call 3가 "乙의 상해는 甲의 교사 범위를 질적으로
      초과하므로 그 부분에 대한 책임은 없다"고 설명할 근거가 여기서 나온다.
    """

    accessory_instance: OffenseInstanceKey
    """가담자가 교사·방조한 죄의 instance. 이 죄의 책임은 초과와 무관하게 유지된다."""

    excess_offense_ref: str
    decision: str
    effect: str
    blocked_instance: OffenseInstanceKey | None = None
    """차단된 귀속의 실제 instance. `None`이면 애초에 그런 귀속이 만들어지지 않았다는 뜻이고,
    그것도 기록한다 -- "생성되지 않음"과 "생성 후 제거"는 결론이 같아도 근거가 다르다."""

    def as_dict(self) -> dict[str, Any]:
        return {
            "accessory_instance": {
                "case_id": self.accessory_instance.case_id,
                "actor_id": self.accessory_instance.actor_id,
                "offense_ref": self.accessory_instance.offense_ref,
                "occurrence_id": self.accessory_instance.occurrence_id,
            },
            "excess_offense_ref": self.excess_offense_ref,
            "decision": self.decision,
            "effect": self.effect,
            "blocked_instance": None
            if self.blocked_instance is None
            else {
                "case_id": self.blocked_instance.case_id,
                "actor_id": self.blocked_instance.actor_id,
                "offense_ref": self.blocked_instance.offense_ref,
                "occurrence_id": self.blocked_instance.occurrence_id,
            },
        }


def plan_excess_attributions(
    findings: Iterable[ExcessFinding],
    *,
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
) -> tuple[ExcessAttribution, ...]:
    """각 초과 판정을 하나의 귀속 결정으로 바꾼다. 다른 죄책은 건드리지 않는다."""
    accessory_instances = {
        (accessory.actor_id, accessory.offense_ref): accessory
        for accessory, _principal, _mode in derivative_links
    }
    output: list[ExcessAttribution] = []
    for finding in findings:
        accessory = finding.candidate.accessory_instance
        excess_ref = finding.candidate.realized_offense_ref
        decision = _EXCESS_DECISION.get(finding.assessment.effect)
        if decision is None:
            raise FinalResponsibilityError(
                f"unhandled excess effect: {finding.assessment.effect!r}"
            )
        output.append(
            ExcessAttribution(
                accessory_instance=accessory,
                excess_offense_ref=excess_ref,
                decision=decision,
                effect=finding.assessment.effect,
                blocked_instance=accessory_instances.get((accessory.actor_id, excess_ref)),
            )
        )
    return tuple(dict.fromkeys(output))


@dataclass(frozen=True, slots=True)
class FinalResponsibilityView:
    case_id: str
    established_instances: tuple[OffenseInstanceKey, ...]
    concurrence: ConcurrenceResolution
    specialty_candidates: tuple[ConcurrenceCandidate, ...]
    authored_candidates: tuple[ConcurrenceCandidate, ...]
    excess_findings: tuple[ExcessFinding, ...]
    excess_attributions: tuple[ExcessAttribution, ...]
    attribution_withheld_instances: frozenset[OffenseInstanceKey]
    status_redirections: tuple[AggravatingStatusRedirection, ...]
    unresolved: tuple[UnresolvedFinding, ...]

    def as_dict(self) -> dict[str, Any]:
        def instance(value: OffenseInstanceKey) -> dict[str, str]:
            return {
                "case_id": value.case_id,
                "actor_id": value.actor_id,
                "offense_ref": value.offense_ref,
                "occurrence_id": value.occurrence_id,
            }

        def candidate(value: ConcurrenceCandidate) -> dict[str, Any]:
            return {
                "rule_id": value.rule.rule_id,
                "kind": value.rule.kind,
                "first_instance": instance(value.first),
                "second_instance": instance(value.second),
                "factual_episode_id": value.factual_episode_id,
            }

        return {
            "case_id": self.case_id,
            "established_instance_count": len(self.established_instances),
            "retained_instances": [
                instance(value)
                for value in sorted(self.concurrence.retained_instances, key=repr)
            ],
            "absorbed_instances": [
                instance(value)
                for value in sorted(self.concurrence.absorbed_instances, key=repr)
            ],
            "imaginative_concurrence_pairs": [
                {"first_instance": instance(left), "second_instance": instance(right)}
                for left, right in self.concurrence.imaginative_pairs
            ],
            "unresolved_concurrence_candidates": [
                candidate(value) for value in self.concurrence.unresolved_candidates
            ],
            "specialty_candidate_count": len(self.specialty_candidates),
            "authored_candidate_count": len(self.authored_candidates),
            "final_instances": [
                instance(value)
                for value in sorted(self.concurrence.retained_instances, key=repr)
            ],
            "excess_findings": [value.as_dict() for value in self.excess_findings],
            "excess_attributions": [value.as_dict() for value in self.excess_attributions],
            "attribution_withheld_instances": [
                instance(value)
                for value in sorted(self.attribution_withheld_instances, key=repr)
            ],
            "status_redirections": [
                {
                    "accessory_instance": instance(value.accessory_instance),
                    "base_offense_ref": value.base_offense_ref,
                    "aggravated_offense_ref": value.aggravated_offense_ref,
                    "status_ref": value.status_ref,
                    "mode": value.mode,
                }
                for value in self.status_redirections
            ],
            "unresolved_findings": [value.as_dict() for value in self.unresolved],
        }


def established_instances(
    results: Mapping[OffenseInstanceKey, LiabilityEvaluation],
) -> tuple[OffenseInstanceKey, ...]:
    """성립(구성요건해당성·위법성·책임)까지 간 instance만. 경합은 성립을 전제로 한다.

    가벌성 단계에서 멈춘 instance도 여기 들어온다. 인적 처벌조각사유로 처벌되지 않는 죄도
    성립한 죄이고, 그것이 다른 죄를 흡수하는지는 별개 문제이기 때문이다.
    """
    return tuple(
        instance
        for instance, evaluation in results.items()
        if evaluation.establishment is not None
    )


def excess_policy_for(registry: DefinitionRegistry) -> DefinitionEntry | None:
    entries = tuple(registry.by_kind.get("excess_policy", ()))
    if len(entries) > 1:
        raise FinalResponsibilityError(
            "multiple excess policies are authored; profile selection is not implemented"
        )
    return entries[0] if entries else None


def plan_status_redirections(
    registry: DefinitionRegistry,
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    truths: CaseTruths,
    *,
    known_instances: Iterable[OffenseInstanceKey],
) -> tuple[tuple[AggravatingStatusRedirection, ...], tuple[UnresolvedFinding, ...]]:
    """제33조 단서 전환을 계산한다. 적용은 호출자가 책임 평가 전에 한다.

    전환 대상 instance가 평가 universe에 없으면 만들지 않고 marker를 남긴다.
    """
    universe = frozenset(known_instances)
    applied: list[AggravatingStatusRedirection] = []
    unresolved: list[UnresolvedFinding] = []
    for accessory, principal, mode in derivative_links:
        redirection = redirect_by_aggravating_status(
            registry,
            accessory_instance=accessory,
            principal_offense_ref=principal.offense_ref,
            mode=mode,
            truths=truths,
        )
        if redirection is None:
            continue
        if redirection.accessory_instance not in universe:
            unresolved.append(
                UnresolvedFinding(
                    marker=UNRESOLVED_STATUS_REDIRECTION_TARGET,
                    policy_id=redirection.aggravated_offense_ref,
                    scope=f"{accessory.actor_id}/{accessory.occurrence_id}",
                    detail=(
                        f"{redirection.aggravated_offense_ref} is not a planned instance for "
                        f"{accessory.actor_id} on {accessory.occurrence_id}"
                    ),
                )
            )
            continue
        applied.append(redirection)
    return tuple(applied), tuple(unresolved)


def resolve_final_responsibility(
    registry: DefinitionRegistry,
    *,
    case_id: str,
    results: Mapping[OffenseInstanceKey, LiabilityEvaluation],
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    source_bindings_by_instance: Mapping[OffenseInstanceKey, tuple[str, ...]],
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = (),
    truths: CaseTruths | None = None,
    concurrence_rules: Iterable[ConcurrenceRule] = (),
    condition_truths: Mapping[
        tuple[str, OffenseInstanceKey, OffenseInstanceKey], TruthValue
    ] = {},
    episode_order: Iterable[str] = (),
    available_predicate_refs: Iterable[str] = (),
    status_redirections: Iterable[AggravatingStatusRedirection] = (),
    status_redirection_findings: Iterable[UnresolvedFinding] = (),
) -> FinalResponsibilityView:
    """성립한 죄들 위에서 초과 귀속 -> 경합 -> 공백을 순서대로 계산한다.

    초과가 경합보다 먼저 도는 것이 순서상 중요하다. 초과로 귀속이 차단된 죄는 애초에 그
    가담자의 죄가 아니므로, 다른 죄를 흡수하거나 흡수당하는 자리에 서면 안 된다.
    """
    established = established_instances(results)
    scoped_episodes = {
        instance: episode_by_instance[instance]
        for instance in established
        if instance in episode_by_instance
    }
    missing_episode = tuple(value for value in established if value not in scoped_episodes)

    # 가담자 instance는 성립하지 않았을 수 있다. 성립 여부야말로 초과가 바꾸려는 것이므로
    # link의 양 끝은 established가 아니라 전체 provenance에서 찾는다.
    links = tuple(
        link
        for link in derivative_links
        if link[0] in episode_by_instance and link[1] in episode_by_instance
    )
    excess_findings = _excess_findings(
        registry,
        links=links,
        established=tuple(scoped_episodes),
        episode_by_instance=dict(episode_by_instance),
        episode_order=tuple(episode_order),
        truths=truths,
    )
    attributions = plan_excess_attributions(excess_findings, derivative_links=links)
    withheld = frozenset(
        attribution.blocked_instance
        for attribution in attributions
        if attribution.blocked_instance is not None
        and attribution.decision != ATTRIBUTED
    )
    attributed_episodes = {
        instance: episode
        for instance, episode in scoped_episodes.items()
        if instance not in withheld
    }

    specialty = plan_specialty_candidates(
        tuple(attributed_episodes),
        registry=registry,
        episode_by_instance=attributed_episodes,
        source_bindings_by_instance=source_bindings_by_instance,
    )
    authored = plan_concurrence_candidates(
        tuple(attributed_episodes),
        episode_by_instance=attributed_episodes,
        rules=concurrence_rules,
    )
    resolution = resolve_concurrence(
        tuple(attributed_episodes),
        (*specialty, *authored),
        condition_truths=condition_truths,
    )

    unresolved = [
        *status_redirection_findings,
        *_multiple_excess_findings(excess_findings),
        *_probe_gap_findings(
            registry,
            available_predicate_refs=(
                *available_predicate_refs,
                # 초과 정책의 두 provenance 입력은 뉴럴 target이 아니라 host가 후보와 함께
                # 실어 나르는 값이다. 공백으로 세면 진짜 공백이 묻힌다.
                *((INSTIGATED_PROVENANCE_REF, REALIZED_PROVENANCE_REF) if links else ()),
            ),
            has_participation_candidate=bool(links),
        ),
    ]
    for instance in missing_episode:
        unresolved.append(
            UnresolvedFinding(
                marker="MISSING_INSTANCE_EPISODE_PROVENANCE",
                policy_id="runtime.final_responsibility",
                scope=f"{instance.actor_id}/{instance.occurrence_id}",
                detail=(
                    "established instance has no planner episode provenance and was excluded "
                    "from concurrence and excess"
                ),
            )
        )
    return FinalResponsibilityView(
        case_id=case_id,
        established_instances=established,
        concurrence=resolution,
        specialty_candidates=specialty,
        authored_candidates=authored,
        excess_findings=excess_findings,
        excess_attributions=attributions,
        attribution_withheld_instances=withheld,
        status_redirections=tuple(status_redirections),
        unresolved=tuple(unresolved),
    )


def _excess_findings(
    registry: DefinitionRegistry,
    *,
    links: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...],
    established: tuple[OffenseInstanceKey, ...],
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    episode_order: tuple[str, ...],
    truths: CaseTruths | None,
) -> tuple[ExcessFinding, ...]:
    """확정된 참가 링크를 따라가 정범이 그 실행에서 이어서 실현한 다른 죄를 분류한다.

    성립하지 않은 죄는 후보에서 빠진다 -- 실현되지 않은 죄를 초과의 상대항으로 삼을 수 없다.
    """
    policy = excess_policy_for(registry)
    if policy is None or not links:
        return ()
    candidates = plan_accessory_excess_candidates(
        links,
        established,
        episode_by_instance=dict(episode_by_instance),
        episode_order=episode_order,
    )
    foreseeability_ref = policy.payload["quantitative"]["result_aggravated"]["foreseeability_ref"]
    output: list[ExcessFinding] = []
    for candidate in candidates:
        foreseeability: TruthValue = UNKNOWN
        if truths is not None:
            view = truths.predicate_view(candidate.accessory_instance)
            foreseeability = view.get(foreseeability_ref, UNKNOWN)
        output.append(
            ExcessFinding(
                candidate,
                classify_excess(
                    registry,
                    policy,
                    instigated_offense_ref=candidate.instigated_offense_ref,
                    realized_offense_ref=candidate.realized_offense_ref,
                    participant_foreseeability=foreseeability,
                ),
            )
        )
    return tuple(output)


MULTIPLE_EXCESS_CANDIDATES = "MULTIPLE_EXCESS_CANDIDATES"
"""한 가담자에게 같은 episode의 정범 실현이 여럿이라 초과를 하나로 접을 수 없다.

우선순위를 host가 정해 하나를 고르면 그것은 저작되지 않은 법리를 코드로 쓰는 것이다.
Scallop lowering도 (가담자, 교사대상) 하나만 키로 받으므로 여기서 멈추는 것이 맞다.
"""


def _multiple_excess_findings(
    findings: tuple[ExcessFinding, ...],
) -> tuple[UnresolvedFinding, ...]:
    grouped: dict[OffenseInstanceKey, list[ExcessFinding]] = {}
    for finding in findings:
        grouped.setdefault(finding.candidate.accessory_instance, []).append(finding)
    return tuple(
        UnresolvedFinding(
            marker=MULTIPLE_EXCESS_CANDIDATES,
            policy_id="excess_policy",
            scope=f"{accessory.actor_id}/{accessory.occurrence_id}",
            detail=(
                "one accessory faces several realized offenses in this episode: "
                + ", ".join(
                    sorted(value.candidate.realized_offense_ref for value in values)
                )
            ),
        )
        for accessory, values in sorted(grouped.items(), key=lambda item: repr(item[0]))
        if len(values) > 1
    )


def excess_parity_rows(
    view: FinalResponsibilityView,
    truths: CaseTruths | None,
    *,
    foreseeability_ref: str,
) -> tuple[tuple[OffenseInstanceKey, str, ExcessAssessment, TruthValue], ...]:
    """Scallop 초과 parity에 내릴 행. 접을 수 없는 가담자는 제외한다."""
    blocked = {
        finding.scope
        for finding in view.unresolved
        if finding.marker == MULTIPLE_EXCESS_CANDIDATES
    }
    output: list[tuple[OffenseInstanceKey, str, ExcessAssessment, TruthValue]] = []
    for finding in view.excess_findings:
        accessory = finding.candidate.accessory_instance
        if f"{accessory.actor_id}/{accessory.occurrence_id}" in blocked:
            continue
        foreseeability: TruthValue = UNKNOWN
        if truths is not None:
            foreseeability = truths.predicate_view(accessory).get(foreseeability_ref, UNKNOWN)
        output.append(
            (accessory, finding.candidate.instigated_offense_ref, finding.assessment, foreseeability)
        )
    return tuple(output)


def _probe_gap_findings(
    registry: DefinitionRegistry,
    *,
    available_predicate_refs: Iterable[str],
    has_participation_candidate: bool,
) -> tuple[UnresolvedFinding, ...]:
    """저작된 정책이 요구했는데 이 사건이 공급하지 못한 입력을 marker로 남긴다.

    참가 후보가 아예 없는 사건에서 participation 정책의 공백을 보고하지는 않는다. 그것은
    입력 부재가 아니라 적용 대상 부재이고, 둘을 섞으면 진짜 공백이 묻힌다.
    """
    available = tuple(available_predicate_refs)
    scopes = [OFFENSE_INSTANCE]
    if has_participation_candidate:
        scopes.append(PARTICIPATION_CANDIDATE)
    grouped: dict[tuple[str, str, str], list[str]] = {}
    for scope in scopes:
        for requirement in unsatisfied_requirements(registry, available, applies_to=scope):
            key = (requirement.unresolved_marker, requirement.policy_id, requirement.applies_to)
            grouped.setdefault(key, []).append(requirement.ref)
    return tuple(
        UnresolvedFinding(
            marker=marker,
            policy_id=policy_id,
            scope=scope,
            missing_refs=tuple(sorted(refs)),
            detail="authored policy input is not represented for this case",
        )
        for (marker, policy_id, scope), refs in sorted(grouped.items())
    )


__all__ = [
    "ATTRIBUTED",
    "MULTIPLE_EXCESS_CANDIDATES",
    "NOT_ATTRIBUTABLE_BY_EXCESS",
    "UNRESOLVED_EXCESS_ATTRIBUTION",
    "ExcessAttribution",
    "plan_excess_attributions",
    "UNRESOLVED_STATUS_REDIRECTION_TARGET",
    "excess_parity_rows",
    "ExcessFinding",
    "FinalResponsibilityError",
    "FinalResponsibilityView",
    "UnresolvedFinding",
    "established_instances",
    "excess_policy_for",
    "plan_status_redirections",
    "resolve_final_responsibility",
]
