"""구성요건적 착오의 고의 투영 (MistakePolicyDef 런타임).

Call 2에게 "甲이 C를 상해할 고의가 있었는가"를 그대로 물으면 FALSE가 돌아오는 것이
오히려 정확한 사실 판단이다. 甲은 C를 해칠 생각이 없었고 乙로 오인했을 뿐이기 때문이다.
법정적 부합설의 결론(발생사실에 대한 고의기수)은 그 사실 판단을 뒤집는 것이 아니라,
저작된 학설을 적용한 규범적 귀속이다. 그래서 이 모듈은 Call 2를 다시 부르지 않고
이미 받은 truth 위에 정책을 얹는다.

`apply_attribution()`과 같은 view transformation 패턴이다: 새 `CaseTruths`를 반환하고
원본은 손대지 않는다. 정책이 발화하지 않으면 입력 그대로를 돌려준다.

이 모듈이 하지 않는 것:

* 불일치 여부를 스스로 판정하지 않는다. `relation.intended_object_divergence`는 structural
  relation이고 host가 binding에서 읽어 온다.
* 의도한 대상에 대한 고의가 TRUE가 아니면 아무것도 하지 않는다. 없는 고의를 만들어
  귀속시키는 것은 부합설이 허용하는 범위가 아니다.
* UNKNOWN을 repair하지 않는다. 입력 셋 중 하나라도 UNKNOWN이면 정책은 침묵한다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.registry import DefinitionEntry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

SAME_STATUTORY_OFFENSE = "same_statutory_offense"

INTENT_PRESERVED = "intent_preserved"
INTENT_DEFEATED = "intent_defeated"
UNRESOLVED = "unresolved"

_EFFECT_TRUTH: Mapping[str, TruthValue] = {
    INTENT_PRESERVED: TRUE,
    INTENT_DEFEATED: FALSE,
    UNRESOLVED: UNKNOWN,
}


class MistakePolicyError(ValueError):
    """The policy was applied outside the scope it was authored for, or to an unplanned target."""


@dataclass(frozen=True, slots=True)
class MistakeFinding:
    """One 착오 사안. `instance`는 **결과가 실제로 발생한 대상**을 객체로 하는 instance다.

    甲이 乙을 상해하려다 C를 상해한 사안이라면 `instance`는 C에 대한 상해 instance이고,
    `intent_toward_intended_object`는 乙에 대한 고의다.
    """

    instance: OffenseInstanceKey
    divergence_truth: TruthValue
    divergence_kind_truth: TruthValue
    intent_toward_intended_object: TruthValue
    intent_ref: str = "legal_element.intent"


def apply_mistake_policy(
    truths: CaseTruths,
    findings: Iterable[MistakeFinding],
    *,
    policy: DefinitionEntry,
) -> CaseTruths:
    """Overlay one authored MistakePolicyDef onto the intent truths of the given findings."""
    if policy.kind != "mistake_policy":
        raise MistakePolicyError(f"not a mistake policy: {policy.id!r}")
    payload = policy.payload
    if payload["scope"] != SAME_STATUTORY_OFFENSE:
        # 추상적 사실의 착오는 처리가 전혀 다르다. 같은 코드로 덮으면 상이 구성요건 간
        # 착오에 동일 구성요건의 결론을 적용하게 된다.
        raise MistakePolicyError(
            f"{policy.id!r} has scope {payload['scope']!r}; only {SAME_STATUTORY_OFFENSE} is wired"
        )
    effects = payload["effects"]

    updated = dict(truths.predicate)
    for finding in findings:
        key = (finding.instance, finding.intent_ref)
        if key not in updated:
            raise MistakePolicyError(
                f"{finding.intent_ref!r} was never assessed for {finding.instance!r}; "
                "the mistake policy refines a planned target, it does not add one"
            )
        if finding.divergence_truth != TRUE:
            continue
        if finding.intent_toward_intended_object != TRUE:
            continue
        if finding.divergence_kind_truth == TRUE:
            effect = effects["object_misidentification"]
        elif finding.divergence_kind_truth == FALSE:
            effect = effects["method_divergence"]
        else:
            continue
        updated[key] = _EFFECT_TRUTH[effect]
    return CaseTruths(predicate=updated, relation=truths.relation)


__all__ = [
    "INTENT_DEFEATED",
    "INTENT_PRESERVED",
    "SAME_STATUTORY_OFFENSE",
    "UNRESOLVED",
    "MistakeFinding",
    "MistakePolicyError",
    "apply_mistake_policy",
]
