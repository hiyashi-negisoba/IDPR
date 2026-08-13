"""cue assessment -> raised doctrine. 저작된 표만 읽고 원문은 읽지 않는다.

이 모듈이 doctrine activation dead loop의 잠금 장치다. 여기서 raised된 doctrine만 planner가
leaf target으로 열고, 그 leaf만 Call 2가 평가하며, 그래야 기존
`doctrine_activation.raised_active_doctrines`의 "leaf 하나는 non-UNKNOWN이어야 한다"가 만족된다.
반대로 여기서 raised되지 않은 doctrine은 **부정된 것이 아니라 제기되지 않은 것**이고, 그 단계는
지금처럼 preserved로 남는다.

scope 처리가 이 모듈의 유일한 판단이고, 그것도 저작된 값을 읽는 것뿐이다. actor scope cue는
관찰된 episode 밖으로 투영되므로 어디서 관찰됐는지를 잃으면 안 된다. `RaisedDoctrine`이
`source_episode_id`와 `target_episode_id`를 따로 들고 있는 이유다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.doctrine_cues import DoctrineCue, DoctrineCueAssessment, DoctrineCueError


@dataclass(frozen=True, slots=True)
class RaisedDoctrine:
    case_id: str
    actor_id: str
    target_episode_id: str
    """doctrine을 평가할 episode. 이 episode의 그 행위자 instance에 leaf가 열린다."""

    doctrine_ref: str
    scope: str
    source_episode_id: str
    """단서가 실제로 관찰된 episode. actor scope에서 둘이 달라진다."""

    raised_by_cue_id: str
    source_quote: str

    @property
    def is_projected(self) -> bool:
        return self.source_episode_id != self.target_episode_id

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "actor_id": self.actor_id,
            "target_episode_id": self.target_episode_id,
            "doctrine_ref": self.doctrine_ref,
            "scope": self.scope,
            "source_episode_id": self.source_episode_id,
            "projected": self.is_projected,
            "raised_by_cue_id": self.raised_by_cue_id,
            "source_quote": self.source_quote,
        }


def raise_doctrines(
    assessments: Iterable[DoctrineCueAssessment],
    *,
    cues: Sequence[DoctrineCue],
    episode_ids_by_case: Mapping[str, Sequence[str]],
) -> tuple[RaisedDoctrine, ...]:
    """제기된 cue를 저작된 매핑으로 doctrine으로 바꾼다.

    `episode_ids_by_case`는 actor scope 투영의 대상 집합이다. host가 새 episode를 만들지
    않고 Call 1.5가 이미 결박한 목록만 쓴다.
    """
    cue_by_id = {cue.cue_id: cue for cue in cues}
    output: list[RaisedDoctrine] = []
    for assessment in assessments:
        cue = cue_by_id.get(assessment.cue_id)
        if cue is None:
            raise DoctrineCueError(f"unknown cue in assessment: {assessment.cue_id!r}")
        if not assessment.is_raising:
            continue
        if cue.is_actor_scoped:
            targets = tuple(episode_ids_by_case.get(assessment.case_id, ()))
            if not targets:
                raise DoctrineCueError(
                    f"{assessment.case_id}: actor-scoped cue has no episode universe to project onto"
                )
        else:
            targets = (assessment.factual_episode_id,)
        for actor_id in assessment.subject_actor_ids:
            for target_episode_id in targets:
                for doctrine_ref in cue.raises:
                    output.append(
                        RaisedDoctrine(
                            case_id=assessment.case_id,
                            actor_id=actor_id,
                            target_episode_id=target_episode_id,
                            doctrine_ref=doctrine_ref,
                            scope=cue.scope,
                            source_episode_id=assessment.factual_episode_id,
                            raised_by_cue_id=cue.cue_id,
                            source_quote=assessment.source_quote,
                        )
                    )
    return tuple(dict.fromkeys(output))


def raised_refs_by_actor_episode(
    raised: Iterable[RaisedDoctrine],
) -> dict[tuple[str, str, str], tuple[str, ...]]:
    """`{(case, actor, episode): doctrine refs}` -- planner가 instance와 join할 형태."""
    grouped: dict[tuple[str, str, str], list[str]] = {}
    for value in raised:
        key = (value.case_id, value.actor_id, value.target_episode_id)
        refs = grouped.setdefault(key, [])
        if value.doctrine_ref not in refs:
            refs.append(value.doctrine_ref)
    return {key: tuple(sorted(value)) for key, value in grouped.items()}


__all__ = ["RaisedDoctrine", "raise_doctrines", "raised_refs_by_actor_episode"]
