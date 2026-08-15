"""raised doctrine -> Call 2 leaf target, with the identity gate that stops orphan raisings.

`policy_probe_targets`와 같은 자리, 같은 방식이다. 다른 것은 여기에 하나의 게이트가 붙는다는
점이다.

**제기된 doctrine의 주체가 이 사건의 법적 instance를 가진 행위자가 아니면 leaf를 열지 않는다.**

2026-08-13 감사에서 강요된행위 cue가 강제추행 **피해자** A를 주체로 TRUE를 냈다. 여기서
프롬프트를 더 조이는 선택지가 있었지만 그 방향은 모델이 "협박"이라는 낱말에 계속 끌리는 것을
문구로 이기려는 시도다. 대신 host가 이미 아는 typed 구조로 막는다 -- A에게는 이 사건에서
평가되는 offense instance가 없으므로, 그에게 적용할 법리도 없다. 이것은 host가 원문의 의미를
다시 판단하는 것이 아니라 "이 doctrine을 적용할 법적 instance가 존재하는가"라는 identity
check이고, 정확히 compiler의 일이다.

거른 후보는 지우지 않고 `NOT_MATERIALIZED`로 남긴다. cue assessment raw artifact에는 TRUE가
그대로 있고, 여기서 왜 target이 되지 않았는지가 함께 남아야 둘을 대조할 수 있다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.runtime.doctrine_raising import RaisedDoctrine
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.target_scheduling import merge_target_opener

NOT_MATERIALIZED = "NOT_MATERIALIZED_NO_MATCHING_LEGAL_INSTANCE"

#: 이 producer의 이름. 행에 적히는 값과 여기서 쓰는 값이 갈라지지 않도록 한 곳에서 정한다.
DOCTRINE_OPENER = "doctrine_raising_cue"


@dataclass(frozen=True, slots=True)
class DoctrineLeafTarget:
    instance: OffenseInstanceKey
    predicate_ref: str
    doctrine_ref: str
    raised_by_cue_id: str

    reuses_existing_target: bool = False
    """이 leaf가 이미 다른 이유로 열려 있던 target인가.

    참이면 새 행을 만들지 않는다. 그렇다고 조용히 버려도 되는 것은 아니다 -- 이 doctrine이
    그 사실을 필요로 한다는 것은 기존 행의 `opened_by`가 말해 주지 않고, 그 정보가 사라지면
    scheduler는 죄 쪽 사정만 보고 그 target을 지워도 된다고 판단한다. 호출자는 기존 행에
    이 opener를 합쳐야 한다.
    """

    def as_dict(self) -> dict[str, Any]:
        return {
            "instance_key": {
                "case_id": self.instance.case_id,
                "actor_id": self.instance.actor_id,
                "offense_ref": self.instance.offense_ref,
                "occurrence_id": self.instance.occurrence_id,
            },
            "predicate_ref": self.predicate_ref,
            "opened_by": DOCTRINE_OPENER,
            "doctrine_ref": self.doctrine_ref,
            "raised_by_cue_id": self.raised_by_cue_id,
        }


@dataclass(frozen=True, slots=True)
class UnmaterializedRaising:
    raised: RaisedDoctrine
    status: str = NOT_MATERIALIZED

    def as_dict(self) -> dict[str, Any]:
        return {**self.raised.as_dict(), "status": self.status}


def materialize_doctrine_leaf_targets(
    raised: Iterable[RaisedDoctrine],
    *,
    instances: Iterable[tuple[OffenseInstanceKey, str]],
    leaves_by_doctrine: Mapping[str, Sequence[str]],
    existing_targets: Iterable[tuple[OffenseInstanceKey, str]] = (),
) -> tuple[tuple[DoctrineLeafTarget, ...], tuple[UnmaterializedRaising, ...]]:
    """`(instance, factual episode)` 목록에 raised doctrine을 붙여 leaf target을 만든다.

    `instances`는 이 사건에서 실제로 평가되는 instance와 그 episode다. 호출자가 top-level만
    넘기면 top-level에만 열린다(2026-08-13 검수: 참가 후보는 link 확정 후로 미룬다).

    이미 열려 있는 `(instance, leaf)`도 **결과에서 빼지 않는다.** 빼면 "이 doctrine이 그
    사실을 필요로 한다"는 provenance가 그 자리에서 사라지고, 하류는 그 target을 죄의 일반
    요소로만 보게 된다. 대신 `reuses_existing_target`으로 표시해서 호출자가 기존 행에 opener를
    합치도록 한다.
    """
    universe = tuple(instances)
    already = set(existing_targets)
    targets: list[DoctrineLeafTarget] = []
    unmaterialized: list[UnmaterializedRaising] = []
    for value in raised:
        leaves = leaves_by_doctrine.get(value.doctrine_ref)
        if not leaves:
            raise ValueError(f"no authored leaves for {value.doctrine_ref!r}")
        matched = tuple(
            instance
            for instance, episode_id in universe
            if instance.case_id == value.case_id
            and instance.actor_id == value.actor_id
            and episode_id == value.target_episode_id
        )
        if not matched:
            unmaterialized.append(UnmaterializedRaising(value))
            continue
        for instance in matched:
            for leaf in leaves:
                # 두 doctrine이 같은 leaf를 필요로 할 수도 있다. 두 번째부터는 재사용이므로
                # `already`를 여기서도 키운다 -- 그러지 않으면 같은 `(instance, leaf)`에 대해
                # 행이 둘 생기고, carrier는 하나뿐이라 plan이 계약 위반으로 거부된다.
                reused = (instance, leaf) in already
                already.add((instance, leaf))
                targets.append(
                    DoctrineLeafTarget(
                        instance,
                        leaf,
                        value.doctrine_ref,
                        value.raised_by_cue_id,
                        reuses_existing_target=reused,
                    )
                )
    return tuple(dict.fromkeys(targets)), tuple(dict.fromkeys(unmaterialized))


def merge_reused_openers(
    assessment_targets: Sequence[MutableMapping[str, Any]],
    reused: Iterable[DoctrineLeafTarget],
) -> int:
    """재사용된 leaf의 opener를 기존 target 행에 합친다. 합쳐진 행 수를 돌려준다.

    규칙 자체는 `merge_target_opener`가 소유한다. 여기서는 leaf를 그 행에 맞춰 주기만 한다.
    """
    rows = {
        (
            str(item["instance_key"]["actor_id"]),
            str(item["instance_key"]["offense_ref"]),
            str(item["instance_key"]["occurrence_id"]),
            str(item["predicate_ref"]),
        ): item
        for item in assessment_targets
    }
    merged = 0
    for value in reused:
        item = rows.get(
            (
                value.instance.actor_id,
                value.instance.offense_ref,
                value.instance.occurrence_id,
                value.predicate_ref,
            )
        )
        if item is None:
            raise ValueError(
                "reused doctrine leaf has no existing target row: "
                f"{value.instance.occurrence_id}/{value.predicate_ref}"
            )
        merged += merge_target_opener(item, DOCTRINE_OPENER)
    return merged


__all__ = [
    "DOCTRINE_OPENER",
    "NOT_MATERIALIZED",
    "DoctrineLeafTarget",
    "UnmaterializedRaising",
    "materialize_doctrine_leaf_targets",
    "merge_reused_openers",
]
