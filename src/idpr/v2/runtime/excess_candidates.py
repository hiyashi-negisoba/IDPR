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

from collections.abc import Iterable
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
            INSTIGATED_PROVENANCE_REF: self.instigated_offense_ref,
            REALIZED_PROVENANCE_REF: self.realized_offense_ref,
        }


def plan_accessory_excess_candidates(
    accessory_instances: Iterable[OffenseInstanceKey],
    principal_instances: Iterable[OffenseInstanceKey],
    *,
    episode_by_instance: dict[OffenseInstanceKey, str],
) -> tuple[AccessoryExcessCandidate, ...]:
    """Pair each accessory with the principals that realized something else in the same episode.

    Three joins, and each one is a place where a looser rule would invent a case:

    * different actors -- an actor is not their own accessory;
    * same factual episode -- otherwise an unrelated offense elsewhere in the case reads as excess;
    * different offense refs -- realizing exactly what was instigated is not excess at all, and
      emitting it here would make `classify_excess` answer a question nobody asked.
    """
    accessories = tuple(dict.fromkeys(accessory_instances))
    principals = tuple(dict.fromkeys(principal_instances))
    missing = (set(accessories) | set(principals)) - set(episode_by_instance)
    if missing:
        raise ExcessCandidateError(
            f"instances lack factual episode ids: {sorted(missing, key=repr)}"
        )

    output: list[AccessoryExcessCandidate] = []
    for accessory in accessories:
        for principal in principals:
            if accessory.case_id != principal.case_id:
                continue
            if accessory.actor_id == principal.actor_id:
                continue
            if accessory.offense_ref == principal.offense_ref:
                continue
            episode = episode_by_instance[accessory]
            if episode != episode_by_instance[principal]:
                continue
            output.append(AccessoryExcessCandidate(accessory, principal, episode))
    return tuple(output)


__all__ = [
    "INSTIGATED_PROVENANCE_REF",
    "REALIZED_PROVENANCE_REF",
    "AccessoryExcessCandidate",
    "ExcessCandidateError",
    "plan_accessory_excess_candidates",
]
