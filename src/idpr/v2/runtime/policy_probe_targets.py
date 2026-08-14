"""authored probe -> Call 2 target, for policies that attach to a participation candidate.

`policy_probes` answers "what would this policy need?"; this module answers "and on which
instance, in this case". The split matters: the compiler stays legally blind and this join stays
free of any policy's content -- it reads `candidate_offense_refs` / `candidate_modes` off the
requirement and never names an offense or a doctrine.

Without this join the 제33조 단서 reproduced the doctrine dead loop exactly: the definition, the
runtime, the Scallop lowering and the probe declaration were all in place, and the status leaf was
never once planned as a target, so the proviso could not fire in any case.

Two things this deliberately does not do.

* It does not open a target on every member of a co-principal group. The proviso authorizes
  `co_principal`, but co-principals compile to a group node rather than a derivative link and the
  redirection runtime only walks derivative links. Planning those targets would buy neural work
  that nothing reads. :func:`unreachable_mode_findings` records that gap instead of hiding it.
* It does not invent an instance. The target lands on the participation candidate the planner
  already created.
* It does not open `optional` requirements. Those belong to a branch that may not be taken --
   초과 정책의 예견가능성은 결과적 가중범 분기에서만 읽힌다 -- and opening them on every
  candidate buys a model call per accessory for a branch that usually does not run. The cost is
  real: 26문항에서 그것만으로 target이 31개 늘었다. When such a branch is reached without its
  input the policy already reports `unresolved` rather than guessing, which is the correct
  behaviour; widening the plan is a separate decision with its own budget.
"""

from __future__ import annotations

from collections.abc import Iterable

from idpr.v2.participation import (
    derivative_mode_required_predicate_refs,
    participation_policy_for,
)
from idpr.v2.policy_probes import (
    PARTICIPATION_CANDIDATE,
    ProbeRequirement,
    probe_requirements,
)
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import ParticipationLocalTarget

MODE_BY_RELATION_KIND = {
    "instigation": "instigator",
    "aiding": "aider",
    "co_principal_group": "co_principal",
}
"""참가 target의 관계 종류 <-> 저작된 mode 이름. 두 어휘가 다른 것은 기존 계약이다."""

DERIVATIVE_RELATION_KINDS = frozenset({"instigation", "aiding"})
"""가담자 위치가 하나로 정해지는 관계. 여기서만 status target을 연다."""


def participation_candidate_probe_targets(
    registry: DefinitionRegistry,
    targets: Iterable[ParticipationLocalTarget],
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """`(가담자 instance, predicate ref)` targets the authored participation probes require."""
    requirements = tuple(
        requirement
        for requirement in probe_requirements(registry, applies_to=PARTICIPATION_CANDIDATE)
        if requirement.is_neural_target and not requirement.optional
    )
    output: list[tuple[OffenseInstanceKey, str]] = []
    for target in targets:
        if target.kind not in DERIVATIVE_RELATION_KINDS:
            continue
        mode = MODE_BY_RELATION_KIND[target.kind]
        # 가담자는 첫 member다. 신분은 가담자 자신의 것이지 정범의 것이 아니다.
        accessory = target.members[0]
        for requirement in requirements:
            if not _matches(requirement, accessory.offense_ref, mode):
                continue
            output.append((accessory, requirement.ref))
    return tuple(dict.fromkeys(output))


def participation_mode_requirement_targets(
    registry: DefinitionRegistry,
    targets: Iterable[ParticipationLocalTarget],
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """`(가담자 instance, predicate ref)` -- derivative mode가 요구하는 가담자 자신의 요소.

    저작은 교사·방조를 `requires: legal_element.instigator_intent | aiding_intent`로 정의한다.
    그런데 그 predicate를 planner가 target으로 열지 않으면 Call 2가 묻지 않고, Kleene에서
    영원히 UNKNOWN으로 남아 교사범·방조범은 어떤 사건에서도 성립할 수 없다. co_principal이
    `establishes_predicate_refs`로 사실을 공급받는 것과 대칭을 이루는 자리다.
    """
    policy = participation_policy_for(registry)
    if policy is None:
        return ()
    required = derivative_mode_required_predicate_refs(policy)
    output: list[tuple[OffenseInstanceKey, str]] = []
    for target in targets:
        if target.kind not in DERIVATIVE_RELATION_KINDS:
            continue
        # 요구되는 고의는 가담자 자신의 것이다. members[0]가 가담자다.
        accessory = target.members[0]
        for ref in sorted(required.get(MODE_BY_RELATION_KIND[target.kind], ())):
            output.append((accessory, ref))
    return tuple(dict.fromkeys(output))


def unreachable_mode_findings(
    registry: DefinitionRegistry,
    targets: Iterable[ParticipationLocalTarget],
) -> tuple[tuple[str, str, str], ...]:
    """`(policy_id, mode, target)` -- 저작이 **명시적으로** 이 mode를 허용하는데 소비 경로가 없는 경우.

    `candidate_modes`가 비어 있는 요구는 여기 들어오지 않는다. 비어 있다는 것은 mode로
    제한하지 않는다는 뜻이지 공동정범까지 발화한다는 주장이 아니다. 둘을 섞으면 모든 공동정범
    후보마다 무관한 정책 이름이 찍혀 진짜 gap이 묻힌다.

    현재 남는 것은 제33조 단서의 공동정범 하나뿐이다. 저작을 좁히는 것도 경로를 만드는 것도
    검수 사항이므로 host가 고르지 않고 드러내기만 한다.
    """
    requirements = probe_requirements(registry, applies_to=PARTICIPATION_CANDIDATE)
    output: list[tuple[str, str, str]] = []
    for target in targets:
        if target.kind in DERIVATIVE_RELATION_KINDS:
            continue
        mode = MODE_BY_RELATION_KIND[target.kind]
        for requirement in requirements:
            if mode not in requirement.candidate_modes:
                continue
            if not _matches(requirement, target.members[0].offense_ref, mode):
                continue
            output.append((requirement.policy_id, mode, target.kind))
    return tuple(dict.fromkeys(output))


def _matches(requirement: ProbeRequirement, offense_ref: str, mode: str) -> bool:
    if requirement.candidate_offense_refs and offense_ref not in requirement.candidate_offense_refs:
        return False
    return not requirement.candidate_modes or mode in requirement.candidate_modes


__all__ = [
    "DERIVATIVE_RELATION_KINDS",
    "MODE_BY_RELATION_KIND",
    "participation_candidate_probe_targets",
    "participation_mode_requirement_targets",
    "unreachable_mode_findings",
]
