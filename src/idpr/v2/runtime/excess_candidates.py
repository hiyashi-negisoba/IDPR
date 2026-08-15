"""공범의 초과 후보 -- excess_policy의 두 provenance 입력을 실어 나르는 typed candidate.

`ParticipationLocalTarget`에 필드를 더할 수 없다. 그 타입은 actor와 principal이 **같은
offense**에 있다고 가정하고 group key도 그 하나의 offense로 잡는다(`offense_ref` property가
`members[0].offense_ref`를 그대로 쓴다). 초과는 정확히 둘이 다른 경우이므로, 기존 타입에
`realized_offense_ref`를 얹으면 그 불변식이 조용히 깨진다.

여기서 만드는 것은 새 판단이 아니다. 두 값 모두 상류가 이미 정했다.

* 교사 대상 offense = Call 1이 그 가담자에게 연 seed를 Call 1.5가 결박한 binding의 offense.
* 실현된 offense = 정범 쪽에서 실제로 성립한 instance의 offense.

host는 이 둘을 짝지어 나르기만 하고 어느 쪽도 해석하지 않는다. 분류는 `excess.py`가
저작된 derivation 구조만 읽어서 한다.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.runtime.identity import OffenseInstanceKey

INSTIGATED_PROVENANCE_REF = "provenance.instigated_offense_ref"
REALIZED_PROVENANCE_REF = "provenance.realized_offense_ref"


class ExcessCandidateError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class AccessoryExcessCandidate:
    accessory_instance: OffenseInstanceKey
    """가담자가 결박된 instance. 그 offense가 곧 교사 대상이다."""

    principal_instance: OffenseInstanceKey
    """정범 쪽에서 실제로 성립한 instance."""

    factual_episode_id: str
    """실현된 죄의 factual episode. 가담자의 episode가 아니다 -- 교사는 앞선 episode에서
    일어나므로 둘은 정상적으로 다르다."""

    same_execution: bool = True
    """실현된 죄가 링크된 정범의 **그 실행**에서 나온 것인가.

    거짓이면 정범이 그 실행 뒤 다른 자리에서 저지른 죄다. 그것이 교사받은 실행이 더 나아간
    것인지, 교사와 무관한 별개 범행인지는 이 단계가 가진 provenance로 판정할 수 없다.
    후보는 열되 최종 책임 단계가 unresolved로 올린다."""

    @property
    def instigated_offense_ref(self) -> str:
        return self.accessory_instance.offense_ref

    @property
    def realized_offense_ref(self) -> str:
        return self.principal_instance.offense_ref

    def as_dict(self) -> dict[str, Any]:
        return {
            "accessory_instance": {
                "case_id": self.accessory_instance.case_id,
                "actor_id": self.accessory_instance.actor_id,
                "offense_ref": self.accessory_instance.offense_ref,
                "occurrence_id": self.accessory_instance.occurrence_id,
            },
            "principal_instance": {
                "case_id": self.principal_instance.case_id,
                "actor_id": self.principal_instance.actor_id,
                "offense_ref": self.principal_instance.offense_ref,
                "occurrence_id": self.principal_instance.occurrence_id,
            },
            "factual_episode_id": self.factual_episode_id,
            "same_execution": self.same_execution,
            INSTIGATED_PROVENANCE_REF: self.instigated_offense_ref,
            REALIZED_PROVENANCE_REF: self.realized_offense_ref,
        }


def plan_accessory_excess_candidates(
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
    established_instances: Iterable[OffenseInstanceKey],
    *,
    episode_by_instance: dict[OffenseInstanceKey, str],
    episode_order: Sequence[str],
) -> tuple[AccessoryExcessCandidate, ...]:
    """Open candidates along an already-confirmed participation link, not by factual episode.

    2026-08-13 검수에서 same-episode join이 교체됐다. 교사행위와 정범의 실행이 시간적으로
    분리되는 것이 정상이고, 판례가 찾는 것은 "교사행위로 정범이 실행을 결의하고 실제
    실행했는가"라는 연결관계다. 그 연결은 derivative link가 이미 확정했으므로, 초과 판정에서
    episode 일치를 다시 요구하면 같은 것을 두 번 물으면서 경로만 닫는다.

    대신 link의 principal realization에서 **이어지는** 실행 범위로 제한한다. 세 join 모두
    느슨해지면 사건을 지어내는 자리다.

    * linked principal과 같은 행위자 -- 사건 안의 다른 사람이 저지른 죄는 이 교사의 초과가
      아니다;
    * linked principal realization의 episode 이후 -- 그 실행보다 앞선 죄는 교사한 범위를
      넘어선 것일 수 없다;
    * 교사 대상과 다른 offense ref -- 교사한 그대로를 실현한 것은 초과가 아니고, 여기서
      내보내면 `classify_excess`가 아무도 묻지 않은 질문에 답하게 된다.

    두 번째 join은 **"교사받은 그 실행이 더 나아간 것"과 "정범이 나중에 따로 저지른 죄"를
    구별하지 못한다.** 甲이 절도를 교사하고 乙이 절도를 실행한 뒤 별개 사건에서 특수절도를
    저질렀다면 그것은 첫 교사의 초과가 아닌데, 지금 join은 그것도 후보로 연다.

    구별에 필요한 것은 "교사받은 그 실현"의 신원인데, 상류가 그것을 주지 않는다 -- 참가
    링크는 정범 instance를 가리킬 뿐 그 실행이 어디까지 이어졌는지는 기록하지 않는다.
    그렇다고 episode 동일성으로 좁히면 반대로 틀린다: 교사한 절도(episode 4)와 정범이 저지른
    상해(episode 5)의 질적 초과는 실제 판례 형태이고, 좁히면 그 후보가 닫힌다.

    그래서 여기서 정하지 않는다. 후보는 열되 :attr:`AccessoryExcessCandidate.same_execution`
    으로 그 후보가 **한 실행 안의 초과인지, 정범의 다른 실행에 걸친 것인지**를 함께 나른다.
    후자는 최종 책임 단계가 unresolved로 올린다. host가 둘 중 하나로 접으면 그것은 저작되지
    않은 법리를 코드로 쓰는 일이다.
    """
    links = tuple(dict.fromkeys(derivative_links))
    established = tuple(dict.fromkeys(established_instances))
    endpoints = {value for link in links for value in link[:2]}
    missing = (endpoints | set(established)) - set(episode_by_instance)
    if missing:
        raise ExcessCandidateError(
            f"instances lack factual episode ids: {sorted(missing, key=repr)}"
        )
    rank = {episode_id: index for index, episode_id in enumerate(episode_order)}
    unranked = {episode_by_instance[value] for value in endpoints | set(established)} - set(rank)
    if unranked:
        raise ExcessCandidateError(f"factual episodes are not ordered: {sorted(unranked)}")

    output: list[AccessoryExcessCandidate] = []
    for accessory, principal, _mode in links:
        principal_episode = episode_by_instance[principal]
        for realized in established:
            if realized.case_id != accessory.case_id:
                continue
            if realized.actor_id != principal.actor_id:
                continue
            if realized.offense_ref == accessory.offense_ref:
                continue
            if rank[episode_by_instance[realized]] < rank[principal_episode]:
                continue
            output.append(
                AccessoryExcessCandidate(
                    accessory,
                    realized,
                    episode_by_instance[realized],
                    same_execution=episode_by_instance[realized] == principal_episode,
                )
            )
    return tuple(dict.fromkeys(output))


__all__ = [
    "INSTIGATED_PROVENANCE_REF",
    "REALIZED_PROVENANCE_REF",
    "AccessoryExcessCandidate",
    "ExcessCandidateError",
    "plan_accessory_excess_candidates",
]
