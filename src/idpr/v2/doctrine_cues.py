"""Call 1.5-D의 사실 단서 카탈로그와 입출력 계약.

모델이 보는 것은 `factual_cue` 문장뿐이다. doctrine id도 조문도 법리 이름도 payload에 넣지
않는다. 어느 doctrine이 열리는지는 host가 저작된 표로 정한다. 이 분리가 없으면 "정당방위를
찾아라"라고 물은 뒤 그 답으로 정당방위를 여는 순환이 된다.

계약은 hard-fail이고 repair하지 않는다. 특히 `source_quote`가 episode 본문의 정확한
부분문자열이 아니면 그 cue는 reject하고 not raised로 남긴다 -- 근거 없이 제기된 법리는
제기되지 않은 것보다 나쁘다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ACTOR_SCOPE = "actor"
EPISODE_SCOPE = "episode"
_SCOPES = frozenset({ACTOR_SCOPE, EPISODE_SCOPE})

ACTING_SUBJECT = "acting_subject"
RESPONDING_ACTOR = "responding_actor"

SUBJECT_INSTRUCTIONS: Mapping[str, str] = {
    ACTING_SUBJECT: "이 단서가 서술하는 사람을 그대로 넣는다.",
    RESPONDING_ACTOR: (
        "이 단서는 상대방이나 상황을 서술한다. 그 사정에 대응하여 행위한 사람을 넣는다."
    ),
}
"""저작된 subject_role에서 렌더링되는 지시문. 모델에게는 이 문장만 나간다.

단서가 서술하는 사람과 doctrine이 붙는 사람이 늘 같지 않다 -- "피해자가 허락하였다"는
피해자를 서술하지만 그 승낙으로 죄책이 영향받는 사람은 행위자다. 그 귀속 규칙을 모델의
자유해석에 맡기지 않고 저작에서 가져온다.
"""
_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})

APPROVED_STATUSES = frozenset({"approved", "awaiting_final_read"})
"""런타임이 읽을 수 있는 카탈로그 상태.

`awaiting_final_read`는 2026-08-13 조건부 승인 상태다 -- 구조와 매핑은 승인됐고 수정본
열람만 남았다. 실행 게이트는 프롬프트 승인이 따로 지므로 여기서 두 상태를 모두 허용한다.
"""


class DoctrineCueError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DoctrineCue:
    cue_id: str
    scope: str
    subject_role: str
    factual_cue: str
    raises: tuple[str, ...]

    @property
    def subject_instruction(self) -> str:
        return SUBJECT_INSTRUCTIONS[self.subject_role]

    @property
    def is_actor_scoped(self) -> bool:
        """행위자의 지속적 속성인가.

        나이와 청각·언어 장애는 사건 앞머리에 한 번 적히고 그 행위자의 모든 episode에
        미친다. 반대로 음주 같은 일시적 상태를 여기 넣으면 episode 1의 만취가 episode 7의
        별개 범행까지 번진다 -- 그래서 두 cue로 분리되어 있다.
        """
        return self.scope == ACTOR_SCOPE


def load_doctrine_cues(path: Path) -> tuple[DoctrineCue, ...]:
    """저작된 cue 카탈로그를 읽는다. 승인되지 않은 상태면 실행을 막는다."""
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    status = str(document.get("status", ""))
    if status not in APPROVED_STATUSES:
        raise DoctrineCueError(
            f"{path}: cue catalog status {status!r} is not approved for runtime use"
        )
    entries = document.get("cues") or ()
    output: list[DoctrineCue] = []
    for entry in entries:
        scope = str(entry.get("scope", ""))
        if scope not in _SCOPES:
            raise DoctrineCueError(f"{entry.get('id')!r}: scope must be one of {sorted(_SCOPES)}")
        subject_role = str(entry.get("subject_role", ""))
        if subject_role not in SUBJECT_INSTRUCTIONS:
            raise DoctrineCueError(
                f"{entry.get('id')!r}: subject_role must be one of "
                f"{sorted(SUBJECT_INSTRUCTIONS)}"
            )
        raises = tuple(str(value) for value in entry.get("raises") or ())
        if not raises:
            raise DoctrineCueError(f"{entry.get('id')!r}: a cue that raises nothing is dead weight")
        cue = DoctrineCue(
            cue_id=str(entry["id"]),
            scope=scope,
            subject_role=subject_role,
            factual_cue=str(entry["factual_cue"]),
            raises=raises,
        )
        if not cue.factual_cue.strip():
            raise DoctrineCueError(f"{cue.cue_id}: empty factual cue")
        output.append(cue)
    if not output:
        raise DoctrineCueError(f"{path}: cue catalog is empty")
    if len({value.cue_id for value in output}) != len(output):
        raise DoctrineCueError(f"{path}: duplicate cue id")
    return tuple(output)


def unraisable_doctrine_refs(
    cues: Iterable[DoctrineCue], doctrine_refs: Iterable[str]
) -> tuple[str, ...]:
    """단서가 없어 구조적으로 영원히 raised될 수 없는 doctrine.

    이것이 doctrine activation 0을 만든 dead loop의 다른 얼굴이다. 정의도 런타임도 Scallop도
    있는데 여는 경로가 없으면 출력에서 "적용되지 않음"과 구별되지 않는다.
    """
    raised = {ref for cue in cues for ref in cue.raises}
    return tuple(sorted(set(doctrine_refs) - raised))


def cue_request_payload(
    *,
    case_id: str,
    factual_episode_id: str,
    episode_text: str,
    actor_labels: Sequence[str],
    cues: Sequence[DoctrineCue],
) -> dict[str, Any]:
    """모델에게 가는 요청. doctrine ref, 조문, scope는 절대 들어가지 않는다.

    `scope`까지 빼는 이유: 어떤 단서가 사건 전체에 미치는지는 법적 효과 범위의 문제이고,
    모델은 그 문장이 원문에 있는지만 답해야 한다.
    """
    if not episode_text.strip():
        raise DoctrineCueError(f"{factual_episode_id}: empty episode text")
    if not actor_labels:
        raise DoctrineCueError(f"{factual_episode_id}: empty actor label universe")
    if not cues:
        raise DoctrineCueError(f"{factual_episode_id}: empty cue set")
    return {
        "case_id": case_id,
        "factual_episode_id": factual_episode_id,
        "episode_text": episode_text,
        "actor_labels": list(actor_labels),
        "cues": [
            {
                "cue_id": cue.cue_id,
                "factual_cue": cue.factual_cue,
                "subject_instruction": cue.subject_instruction,
            }
            for cue in cues
        ],
    }


def cue_output_schema(cues: Sequence[DoctrineCue], actor_labels: Sequence[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["factual_episode_id", "cue_assessments"],
        "properties": {
            "factual_episode_id": {"type": "string"},
            "cue_assessments": {
                "type": "array",
                "minItems": len(cues),
                "maxItems": len(cues),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["cue_id", "truth", "subject_actor_ids", "source_quote"],
                    "properties": {
                        "cue_id": {"enum": [cue.cue_id for cue in cues]},
                        "truth": {"enum": sorted(_TRUTHS)},
                        "subject_actor_ids": {
                            "type": "array",
                            "items": {"enum": list(actor_labels)},
                        },
                        "source_quote": {"type": "string"},
                    },
                },
            },
        },
    }


@dataclass(frozen=True, slots=True)
class DoctrineCueAssessment:
    case_id: str
    factual_episode_id: str
    cue_id: str
    truth: str
    subject_actor_ids: tuple[str, ...]
    source_quote: str

    @property
    def is_raising(self) -> bool:
        """제기로 볼 수 있는가.

        주체를 모르는 TRUE는 제기가 아니다. 그것으로 doctrine을 열면 甲의 심신장애가 乙의
        죄책을 흔든다. UNKNOWN도 제기가 아니지만 부정도 아니다 -- raw로 보존한다.
        """
        return self.truth == "TRUE" and bool(self.subject_actor_ids)

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "factual_episode_id": self.factual_episode_id,
            "cue_id": self.cue_id,
            "truth": self.truth,
            "subject_actor_ids": list(self.subject_actor_ids),
            "source_quote": self.source_quote,
        }


def validate_cue_output(
    raw: Mapping[str, Any],
    *,
    case_id: str,
    factual_episode_id: str,
    episode_text: str,
    actor_labels: Sequence[str],
    cues: Sequence[DoctrineCue],
) -> tuple[DoctrineCueAssessment, ...]:
    """Exact-correspondence 검증. 위반은 hard-fail이고 host가 고치지 않는다."""
    if str(raw.get("factual_episode_id")) != factual_episode_id:
        raise DoctrineCueError(f"{factual_episode_id}: episode identity mismatch")
    values = raw.get("cue_assessments")
    if not isinstance(values, list):
        raise DoctrineCueError(f"{factual_episode_id}: cue_assessments must be an array")
    expected = tuple(cue.cue_id for cue in cues)
    returned = tuple(str(value.get("cue_id")) for value in values)
    if returned != expected:
        raise DoctrineCueError(
            f"{factual_episode_id}: cue set must match exactly and keep order; "
            f"expected {expected}, got {returned}"
        )
    allowed_actors = frozenset(actor_labels)
    output: list[DoctrineCueAssessment] = []
    for value in values:
        truth = str(value.get("truth"))
        if truth not in _TRUTHS:
            raise DoctrineCueError(f"{factual_episode_id}: invalid cue truth {truth!r}")
        subjects = tuple(dict.fromkeys(str(item) for item in value.get("subject_actor_ids") or ()))
        unknown_actors = set(subjects) - allowed_actors
        if unknown_actors:
            raise DoctrineCueError(
                f"{factual_episode_id}: cue subject outside the episode actor universe: "
                f"{sorted(unknown_actors)}"
            )
        quote = str(value.get("source_quote") or "")
        if truth == "TRUE" and quote not in episode_text:
            # 근거 없는 제기는 미제기보다 나쁘다. 인용이 본문에 없으면 그 cue만 떨어뜨린다.
            raise DoctrineCueError(
                f"{factual_episode_id}/{value.get('cue_id')}: source quote is not a substring "
                "of the episode text"
            )
        output.append(
            DoctrineCueAssessment(
                case_id=case_id,
                factual_episode_id=factual_episode_id,
                cue_id=str(value["cue_id"]),
                truth=truth,
                subject_actor_ids=subjects,
                source_quote=quote,
            )
        )
    return tuple(output)


__all__ = [
    "ACTING_SUBJECT",
    "ACTOR_SCOPE",
    "RESPONDING_ACTOR",
    "SUBJECT_INSTRUCTIONS",
    "APPROVED_STATUSES",
    "EPISODE_SCOPE",
    "DoctrineCue",
    "DoctrineCueAssessment",
    "DoctrineCueError",
    "cue_output_schema",
    "cue_request_payload",
    "load_doctrine_cues",
    "unraisable_doctrine_refs",
    "validate_cue_output",
]
