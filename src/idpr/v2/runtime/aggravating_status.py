"""형법 제33조 단서 -- 가감적 신분자가 비신분자의 범행에 가담한 경우의 죄책 전환.

甲(직계비속)이 乙에게 甲의 아버지 살해를 교사하면 乙은 보통살인이지만 甲은 존속살해교사다.
derivative mode는 `requires_conclusion: offense_realization`으로 정범이 실현한 죄에 고정되어
있으므로, 가담자가 정범보다 무거운 죄를 지는 경로가 구조적으로 없었다. 이 모듈은 그 경로를
**책임 평가 이전에 instance를 바꿔치는 방식**으로 연다. 정범의 realization은 그대로 두고,
가담자의 liability를 어느 offense에서 평가할지만 옮긴다.

2026-08-13 검수 확정: 성립은 기본죄로 두고 과형만 가중하는 표현이 아니라 가중 신분범의
해당 mode realization 자체를 만든다(93도1002의 모해위증교사 처단 구조).

경계:

* 가담자 본인의 신분이 TRUE일 때만 전환한다. FALSE는 물론 UNKNOWN에서도 전환하지 않는다 --
  모르는 신분으로 죄책을 올리는 것은 UNKNOWN을 host가 repair하는 것과 같다.
* 한 기본죄에 대해 전환 후보가 둘 이상이면 고르지 않고 hard-fail한다.
* 신분은 가담자 자신의 predicate view에서 읽는다. 정범의 신분이 아니다.
"""

from __future__ import annotations

from dataclasses import dataclass

from idpr.v2.evaluate import TRUE
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

_FIELD = "aggravating_status_participation"


class AggravatingStatusError(ValueError):
    """Two authored offenses claim the same base offense and mode for one participant."""


@dataclass(frozen=True, slots=True)
class AggravatingStatusRedirection:
    accessory_instance: OffenseInstanceKey
    """가담자의 죄책을 평가할 새 instance. offense_ref만 가중죄로 바뀐다."""

    base_offense_ref: str
    aggravated_offense_ref: str
    status_ref: str
    mode: str


def redirect_by_aggravating_status(
    registry: DefinitionRegistry,
    *,
    accessory_instance: OffenseInstanceKey,
    principal_offense_ref: str,
    mode: str,
    truths: CaseTruths,
) -> AggravatingStatusRedirection | None:
    """Return the redirection to apply before resolving this accessory, or None to leave it alone."""
    view = truths.predicate_view(accessory_instance)
    matches: list[AggravatingStatusRedirection] = []
    for entry in registry.by_kind.get("offense", ()):
        proviso = (entry.payload.get("participation_constraints") or {}).get(_FIELD)
        if not proviso:
            continue
        if proviso["base_offense_ref"] != principal_offense_ref:
            continue
        if mode not in proviso["applies_to_modes"]:
            continue
        if view.get(proviso["status_ref"]) != TRUE:
            continue
        matches.append(
            AggravatingStatusRedirection(
                accessory_instance=OffenseInstanceKey(
                    case_id=accessory_instance.case_id,
                    actor_id=accessory_instance.actor_id,
                    offense_ref=entry.id,
                    occurrence_id=accessory_instance.occurrence_id,
                ),
                base_offense_ref=principal_offense_ref,
                aggravated_offense_ref=entry.id,
                status_ref=proviso["status_ref"],
                mode=mode,
            )
        )
    if len(matches) > 1:
        raise AggravatingStatusError(
            "multiple aggravating-status offenses claim "
            f"{principal_offense_ref!r}/{mode!r}: "
            f"{sorted(match.aggravated_offense_ref for match in matches)}"
        )
    return matches[0] if matches else None


__all__ = [
    "AggravatingStatusError",
    "AggravatingStatusRedirection",
    "redirect_by_aggravating_status",
]
