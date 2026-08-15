"""다른 participant의 legal outcome을 요구하는 규칙의 dependency planner.

제151조가 첫 사례지만 이 모듈은 제151조를 알지 못한다. 아는 것은 하나다 -- 어떤 offense가
`linked_offender_dependency`를 저작했고, 그 seed의 binding이 `linked_offender`를 사실로
결박했다면, **그 사람에 대해 ROUTE를 다시 호출해야 한다**는 것.

왜 최초 Call 1에 함께 넣지 않는가
---------------------------------
그러면 한 call이 서로 다른 두 atomic task를 하게 된다. 질문받은 행위자의 routing과, 아직
결박되지도 않은 다른 행위자의 선행범죄 routing이다. 후자를 같이 시키면 router가 linked
offender를 사실상 다시 찾아야 하고, Call 1.5가 사실 결박을 담당한다는 분업이 무너진다.
제151조 전용 call을 새로 만드는 것도 조문 하나 때문에 stage를 늘리는 땜질이다.

그래서 순서가 뒤집힌다.

    Call 1.5가 사람을 사실로 결박한다  →  그 사람에 대해 같은 ROUTE를 다시 호출한다

이 모듈이 하지 않는 것
----------------------
* 선행범죄를 고르지 않는다. 그것은 ROUTE의 일이고, ROUTE는 Definition catalog를 본다.
* 답변용 instance를 만들지 않는다. linked offender는 factual participant로 남는다 --
  질문이 그의 죄책을 묻지 않았기 때문이다. 제34조의 이용된 참가자와 같은 자리다.
* 자격 여부를 판단하지 않는다. `article151_penalty_threshold`는 저작된 값이고
  `statutory.qualifies_for_article_151()`이 읽는다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from idpr.v2.issue_binding import FactualAction, IssueBinding
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.routing import LINKED_OFFENDER_ROUTING, RouteRequest
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey

if TYPE_CHECKING:  # pragma: no cover - typing only
    from idpr.v2.runtime.stages import Article151PredecessorStatus


@dataclass(frozen=True, slots=True)
class LinkedOffenderDependency:
    """하나의 dependent instance와, 그것이 요구하는 다른 사람의 결과.

    `dependent_instance`는 답변 대상 instance(예: 丙의 범인도피죄)이고, `participant`는 그
    죄가 전제하는 사람(乙)이다. 둘의 타입이 다른 것이 핵심이다 -- 한쪽은 answer-facing이고
    다른 쪽은 아니다.
    """

    dependent_instance: OffenseInstanceKey
    participant: FactualParticipantKey
    role: str
    resolved_element: str
    factual_scope_text: str

    def route_request(self) -> RouteRequest:
        return RouteRequest(
            routed_actor_ids=(self.participant.participant_id,),
            factual_scope_text=self.factual_scope_text,
            routing_basis=LINKED_OFFENDER_ROUTING,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "dependent_instance_key": {
                "case_id": self.dependent_instance.case_id,
                "actor_id": self.dependent_instance.actor_id,
                "offense_ref": self.dependent_instance.offense_ref,
                "occurrence_id": self.dependent_instance.occurrence_id,
            },
            "participant": {
                "case_id": self.participant.case_id,
                "participant_id": self.participant.participant_id,
            },
            "role": self.role,
            "resolved_element": self.resolved_element,
            "factual_scope_text": self.factual_scope_text,
        }


def _dependency_declaration(
    registry: DefinitionRegistry, offense_ref: str
) -> Mapping[str, Any] | None:
    entry = registry.get(offense_ref)
    if entry is None or entry.kind not in {"offense", "derived_offense"}:
        return None
    declaration = entry.payload.get("linked_offender_dependency")
    return declaration if isinstance(declaration, Mapping) else None


def _carried_scope(
    action_by_id: Mapping[str, FactualAction], binding: IssueBinding
) -> str:
    """이 binding이 실제로 carry하는 증거만. episode 전체를 주지 않는다.

    routing 범위가 episode로 넓어지면 그 서사에 등장하는 모든 사건이 linked offender의
    선행범죄 후보로 열린다. 좁게 결박한 사실을 넓은 범위로 되돌리는 셈이다.
    """
    action_ids = (binding.focal_action_id, *binding.supporting_action_ids)
    actions = [action_by_id[value] for value in action_ids if value in action_by_id]
    actions.sort(key=lambda value: value.sequence_index)
    return "\n".join(action.evidence_text for action in actions)


def linked_offender_dependencies(
    registry: DefinitionRegistry,
    *,
    case_id: str,
    realizations: Iterable[tuple[str, str, str, Sequence[str]]],
    bindings: Iterable[IssueBinding],
    factual_actions: Iterable[FactualAction],
) -> tuple[LinkedOffenderDependency, ...]:
    """저작이 요구하고 사실이 결박된 dependency만.

    `realizations`는 planner와 같은 `(realization_id, actor_id, offense_ref, binding_ids)`다.
    저작 선언이 없으면 아무것도 만들지 않고, 선언이 있어도 `linked_offender`가 null이면
    만들지 않는다 -- 원문이 대상자를 지목하지 않은 사건에서 host가 사람을 고르지 않는다.
    """
    binding_by_id = {binding.binding_id: binding for binding in bindings}
    action_by_id = {action.factual_action_id: action for action in factual_actions}
    output: list[LinkedOffenderDependency] = []
    for realization_id, actor_id, offense_ref, source_binding_ids in realizations:
        declaration = _dependency_declaration(registry, offense_ref)
        if declaration is None:
            continue
        named = {
            binding.linked_offender: binding
            for binding_id in source_binding_ids
            if (binding := binding_by_id.get(binding_id)) is not None
            and binding.linked_offender is not None
        }
        if len(named) != 1:
            # 지목이 없거나 서로 다른 사람을 지목했다. 어느 쪽인지 host가 고르면 사실 판단이다.
            continue
        participant_id, binding = next(iter(named.items()))
        output.append(
            LinkedOffenderDependency(
                OffenseInstanceKey(case_id, actor_id, offense_ref, realization_id),
                FactualParticipantKey(case_id, participant_id),
                str(declaration["role"]),
                str(declaration["resolved_element"]),
                _carried_scope(action_by_id, binding),
            )
        )
    return tuple(output)


@dataclass(frozen=True, slots=True)
class PredecessorCandidateGate:
    """ROUTE가 낸 선행범죄 후보를, 저작된 threshold로 미리 가른 결과.

    `article151_penalty_threshold`는 사건 사실이 아니라 authored static metadata다. 그러니
    Call 2로 보내기 **전에** 물어볼 수 있고, 물어보는 것이 맞다 -- 어차피 제151조 대상이 될
    수 없는 죄를 먼저 neural하게 평가할 이유가 없다.

    세 갈래를 각각 남긴다. `non_qualifying`은 결정론적 부정이고, `unauthored`는 부정이 아니라
    미확정이다. 둘을 합치면 "저작을 빠뜨렸다"가 "자격 없다"로 조용히 둔갑한다.
    """

    dependency: LinkedOffenderDependency
    qualifying: tuple[str, ...]
    non_qualifying: tuple[str, ...]
    unauthored: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.dependency.as_dict(),
            "qualifying_offense_refs": list(self.qualifying),
            "non_qualifying_offense_refs": list(self.non_qualifying),
            "unauthored_threshold_offense_refs": list(self.unauthored),
        }


def gate_predecessor_candidates(
    registry: DefinitionRegistry,
    dependency: LinkedOffenderDependency,
    candidate_offense_refs: Iterable[str],
) -> PredecessorCandidateGate:
    """저작된 threshold로 후보를 가른다. Call 2는 `qualifying`에만 쓴다."""
    from idpr.v2.runtime.statutory import (
        ARTICLE_151_QUALIFYING_CLASS,
        ARTICLE_151_THRESHOLD_FIELD,
    )

    qualifying: list[str] = []
    non_qualifying: list[str] = []
    unauthored: list[str] = []
    for ref in dict.fromkeys(candidate_offense_refs):
        entry = registry.get(ref)
        threshold = (
            entry.payload.get(ARTICLE_151_THRESHOLD_FIELD)
            if entry is not None and entry.kind in {"offense", "derived_offense"}
            else None
        )
        if not isinstance(threshold, Mapping):
            unauthored.append(ref)
        elif threshold.get("class") == ARTICLE_151_QUALIFYING_CLASS:
            qualifying.append(ref)
        else:
            non_qualifying.append(ref)
    return PredecessorCandidateGate(
        dependency, tuple(qualifying), tuple(non_qualifying), tuple(unauthored)
    )


@dataclass(frozen=True, slots=True)
class LinkedOffenderPredicateTarget:
    """`(participant, offense_ref, predicate_ref)` -- Call 2가 물을 하나의 사실.

    `OffenseInstanceKey`가 아니다. 이 사람의 죄책은 답안에 나가지 않고, 다른 사람의 구성요건
    하나를 채우기 위해서만 평가된다.
    """

    participant: FactualParticipantKey
    offense_ref: str
    predicate_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "participant": {
                "case_id": self.participant.case_id,
                "participant_id": self.participant.participant_id,
            },
            "offense_ref": self.offense_ref,
            "predicate_ref": self.predicate_ref,
        }


def linked_offender_predicate_targets(
    registry: DefinitionRegistry, gate: PredecessorCandidateGate
) -> tuple[LinkedOffenderPredicateTarget, ...]:
    """threshold를 통과한 후보의 구성요건 leaf만.

    통과하지 못한 후보에는 하나도 열지 않는다. 자격 없는 죄를 neural하게 평가할 이유가 없다는
    것이 threshold를 Call 2 앞으로 옮긴 이유 그대로다.
    """
    from idpr.v2 import expressions
    from idpr.v2.compile import CompiledOffense, compile_offense

    output: list[LinkedOffenderPredicateTarget] = []
    for offense_ref in gate.qualifying:
        compiled = compile_offense(registry, offense_ref)
        if not isinstance(compiled, CompiledOffense):
            raise ValueError(f"predecessor offense does not compile: {offense_ref!r}")
        refs: set[str] = set()
        for slot in expressions.SLOT_NAMES:
            refs.update(expressions.canonical_leaf_refs(compiled.slots[slot]))
        output.extend(
            LinkedOffenderPredicateTarget(gate.dependency.participant, offense_ref, ref)
            for ref in sorted(refs)
        )
    return tuple(output)


def article151_predecessor_status(
    registry: DefinitionRegistry,
    *,
    participant: FactualParticipantKey,
    offense_ref: str,
    predicate_truths: Mapping[str, str],
) -> "Article151PredecessorStatus":
    """제151조의 대상자 신분을 계산한다. **ordinary liability 평가가 아니다.**

    제34조의 fold를 재사용하지 않는 이유는 두 가지다. 계약상으로는 그쪽이
    `has_authored_indirect_principal_capability`를 요구하고 completion을 가진 죄를 명시적으로
    거부하는데, 선행범죄는 절도·상해처럼 거의 전부 completion policy를 가진다. 그리고 더
    근본적으로, 묻는 것이 다르다 -- 제34조는 이용된 사람이 그 죄를 실현했는지를 묻고, 여기서는
    그 사람이 제151조의 범인에 해당하는지를 묻는다.

    completion을 평가하지 않는 근거도 거기서 나온다. 제151조의 범인 개념은 확정판결을 받은
    자에 한정되지 않고 **범죄 혐의로 수사대상이 된 자를 포함**한다. 즉 이 조문은 대상자의
    죄책을 완결적으로 확정할 것을 요구하지 않으므로, 기수·미수의 구별은 이 신분 판단의
    요소가 아니다. 그래서 여기서 나오는 값은 죄책 결론이 아니라 신분 충족 여부이고,
    반환 타입도 그 사실을 이름으로 말한다.
    """
    from idpr.v2 import expressions
    from idpr.v2.compile import CompiledOffense, compile_offense
    from idpr.v2.evaluate import FALSE, UNKNOWN, evaluate, fold_all
    from idpr.v2.runtime.stages import Article151PredecessorStatus

    compiled = compile_offense(registry, offense_ref)
    if not isinstance(compiled, CompiledOffense):
        raise ValueError(f"predecessor offense does not compile: {offense_ref!r}")
    elements_truth = fold_all(
        [evaluate(compiled.slots[slot], predicate_truths) for slot in expressions.SLOT_NAMES]
    )
    if elements_truth == FALSE:
        status = "non_qualifying"
    elif elements_truth == UNKNOWN:
        status = "unresolved"
    else:
        status = "qualifying"
    return Article151PredecessorStatus(participant, offense_ref, status)


def article151_status_truths(
    registry: DefinitionRegistry,
    pairs: Iterable[tuple[LinkedOffenderDependency, "Article151PredecessorStatus"]],
) -> dict[tuple[OffenseInstanceKey, str], str]:
    """신분 계산 결과를 dependent instance의 predicate truth로 공급한다.

    제151조에는 제263조 같은 Scallop parity path를 만들지 않는다. 제263조가 별도 경로를 가진
    것은 그 조문이 **책임 자체를 의제**하기 때문이고, 제151조는 그렇지 않다 -- 여기서 나오는
    것은 `offender_status_of_object` 하나이고 최종 죄책은 기존 offense program이 그대로
    소유한다. 그러니 truth 하나를 공급하는 것으로 충분하고, 경로를 늘리면 같은 죄에 두 개의
    책임 계산이 생긴다.

    `qualifying`이 아닌 값은 FALSE로 내리지 않고 UNKNOWN으로 둔다. 이 좁은 조회는 "자격 있는
    선행범죄가 존재하지 않는다"를 증명하지 못하기 때문이다.
    """
    from idpr.v2.runtime.statutory import ARTICLE_151_QUALIFYING_STATUS, qualifies_for_article_151

    output: dict[tuple[OffenseInstanceKey, str], str] = {}
    for dependency, status in pairs:
        key = (dependency.dependent_instance, dependency.resolved_element)
        qualified = status.status == ARTICLE_151_QUALIFYING_STATUS and qualifies_for_article_151(
            registry, status.offense_ref
        )
        if qualified:
            output[key] = "TRUE"
        else:
            output.setdefault(key, "UNKNOWN")
    return output


__all__ = [
    "LinkedOffenderDependency",
    "article151_status_truths",
    "LinkedOffenderPredicateTarget",
    "PredecessorCandidateGate",
    "article151_predecessor_status",
    "gate_predecessor_candidates",
    "linked_offender_dependencies",
    "linked_offender_predicate_targets",
]
