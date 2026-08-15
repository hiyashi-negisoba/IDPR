"""행위가 향한 대상과 결과를 입은 대상의 불일치 -- structural 도출과 그 하류 target.

`relation.intended_object_divergence`는 evaluative가 아니라 structural relation으로 저작되어
있다. 즉 "착오가 있었는가"를 모델에게 묻지 않고, 두 사실이 다르다는 것만 host가 센다.
그 두 사실은 Call 1.5의 `directed_action_target`과 `actual_result_bearer`이며, 원문이 지향
대상을 명시한 경우에만 채워진다.

이 모듈이 하지 않는 것이 세 가지다.

* `factual_targets`를 읽지 않는다. 그 필드는 상대방·수령자까지 담는 넓은 집합이고, 거기서
  "의도한 대상"을 골라내면 host가 원문에 없는 의미를 만들게 된다. 2026-08-13에 명시적으로
  거부된 경로다.
* 둘 중 하나라도 없으면 아무것도 만들지 않는다. 없는 지향을 정황에서 추정하는 순간 같은
  문제가 다른 자리에서 되살아난다. 미확정은 미확정으로 남는다.
* 객체의 착오인지 방법의 착오인지 가르지 않는다. 그것은 대상 동일성이 사실로 확정된 **뒤에**
  모델에게 묻는 별개 질문(`divergence_kind_ref`)이고, 이 모듈은 그 질문을 열어 줄 뿐이다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.issue_binding import IssueBinding
from idpr.v2.policy_probes import OFFENSE_INSTANCE, probe_requirements
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths


@dataclass(frozen=True, slots=True)
class IntendedObjectDivergence:
    """하나의 realization에서 읽어 낸 지향 대상 / 결과 귀속 대상 쌍.

    `truth`는 두 표지가 다른가에 대한 답일 뿐 법적 평가가 아니다. 같으면 FALSE이고, 그
    FALSE도 결정론적 사실이다 -- 불일치의 부재를 모델에게 되물을 이유가 없다.
    """

    instance: OffenseInstanceKey
    directed_action_target: str
    actual_result_bearer: str

    @property
    def truth(self) -> TruthValue:
        return TRUE if self.directed_action_target != self.actual_result_bearer else FALSE

    def as_dict(self) -> dict[str, object]:
        return {
            "instance_key": {
                "case_id": self.instance.case_id,
                "actor_id": self.instance.actor_id,
                "offense_ref": self.instance.offense_ref,
                "occurrence_id": self.instance.occurrence_id,
            },
            "directed_action_target": self.directed_action_target,
            "actual_result_bearer": self.actual_result_bearer,
            "truth": self.truth,
        }


def intended_object_divergences(
    *,
    case_id: str,
    realizations: Iterable[tuple[str, str, str, Sequence[str]]],
    bindings: Iterable[IssueBinding],
) -> tuple[IntendedObjectDivergence, ...]:
    """각 realization이 실은 지향/결과 대상 쌍.

    `realizations`는 `(realization_id, actor_id, offense_ref, source_binding_ids)`다. planner의
    자료구조를 그대로 받지 않는 것은 이 도출이 planner의 조립 순서에 의존하지 않기 위해서다.

    한 realization이 여러 binding에서 왔고 그 binding들이 서로 다른 쌍을 실었다면 아무것도
    만들지 않는다. 어느 쪽이 이 실현의 대상인지 host가 고르면 그것은 사실 판단이다.
    """
    binding_by_id = {binding.binding_id: binding for binding in bindings}
    output: list[IntendedObjectDivergence] = []
    for realization_id, actor_id, offense_ref, source_binding_ids in realizations:
        pairs = {
            (binding.directed_action_target, binding.actual_result_bearer)
            for binding_id in source_binding_ids
            if (binding := binding_by_id.get(binding_id)) is not None
            and binding.directed_action_target is not None
            and binding.actual_result_bearer is not None
        }
        if len(pairs) != 1:
            continue
        directed, bearer = next(iter(pairs))
        output.append(
            IntendedObjectDivergence(
                OffenseInstanceKey(case_id, actor_id, offense_ref, realization_id),
                directed,
                bearer,
            )
        )
    return tuple(output)


def offense_instance_probe_targets(
    registry: DefinitionRegistry,
    divergences: Iterable[IntendedObjectDivergence],
) -> tuple[tuple[OffenseInstanceKey, str], ...]:
    """불일치가 사실로 확정된 instance에서만 여는 `(instance, predicate_ref)`.

    `applies_to: offense_instance` probe에는 지금까지 target producer가 없었다. 저작·런타임·
    Scallop 경로가 모두 있는데 leaf가 한 번도 계획되지 않아 정책이 어떤 사건에서도 발화하지
    못하는 상태였다 -- 제33조 단서에서 이미 한 번 나온 고장이다.

    불일치가 FALSE인 instance에서는 열지 않는다. 대상이 같은 사안에서 "객체의 착오였는가"는
    물을 필요가 없는 질문이고, 물으면 모델이 없는 착오를 만들어 낼 자리만 생긴다.
    """
    refs = tuple(
        dict.fromkeys(
            requirement.ref
            for requirement in probe_requirements(registry, applies_to=OFFENSE_INSTANCE)
            if requirement.is_neural_target and not requirement.optional
        )
    )
    return tuple(
        dict.fromkeys(
            (divergence.instance, ref)
            for divergence in divergences
            if divergence.truth == TRUE
            for ref in refs
        )
    )


def mistake_findings(
    divergences: Iterable[IntendedObjectDivergence],
    truths: CaseTruths,
    *,
    policy: DefinitionEntry,
) -> tuple["MistakeFinding", ...]:
    """저작된 정책이 요구하는 세 입력을 모아 finding으로 만든다.

    `intent_toward_intended_object`는 이 instance의 `legal_element.intent` truth를 그대로 쓴다.
    이 점에는 알려진 한계가 있다. 착오 사안에서 Call 2가 "행위자가 **실제 피해자**를 해할
    고의가 있었는가"로 읽으면 FALSE가 돌아오고, 그러면 정책은 침묵한다. 저작된 probe가
    요구하는 입력이 `legal_element.intent` 하나뿐이므로 host가 별도 scope의 고의 질문을
    임의로 만들지 않는다 -- 없는 고의를 만들어 귀속시키지 않는다는 이 정책의 계약과 같은
    방향이고, 침묵은 틀린 귀속보다 안전하다. 지향 대상 기준 고의를 따로 물을지는 저작 결정이다.
    """
    from idpr.v2.runtime.mistake import MistakeFinding

    payload = policy.payload
    divergence_kind_ref = payload["divergence_kind_ref"]
    output: list[MistakeFinding] = []
    for divergence in divergences:
        if divergence.truth != TRUE:
            continue
        view = truths.predicate_view(divergence.instance)
        output.append(
            MistakeFinding(
                divergence.instance,
                divergence.truth,
                view.get(divergence_kind_ref, UNKNOWN),
                view.get("legal_element.intent", UNKNOWN),
            )
        )
    return tuple(output)


def divergence_relation_truths(
    divergences: Iterable[IntendedObjectDivergence],
    *,
    relation_ref: str,
) -> Mapping[tuple[OffenseInstanceKey, str], TruthValue]:
    """structural relation truth. Call 2를 거치지 않는 유일한 relation 공급 경로다."""
    return {
        (divergence.instance, relation_ref): divergence.truth for divergence in divergences
    }


__all__ = [
    "IntendedObjectDivergence",
    "divergence_relation_truths",
    "mistake_findings",
    "intended_object_divergences",
    "offense_instance_probe_targets",
]
