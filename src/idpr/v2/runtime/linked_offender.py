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
    from idpr.v2.runtime.stages import UtilizedParticipantOutcome


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


def fold_linked_offender_outcome(
    registry: DefinitionRegistry,
    *,
    participant: FactualParticipantKey,
    offense_ref: str,
    predicate_truths: Mapping[str, str],
) -> "UtilizedParticipantOutcome":
    """구성요건 truth를 participant 수준 outcome 하나로 접는다.

    제34조의 fold를 재사용하지 않는다. 그쪽은 `has_authored_indirect_principal_capability`를
    요구하고 **completion을 가진 죄를 명시적으로 거부**하는데, 선행범죄는 절도·상해처럼 거의
    전부 completion policy를 가진다. 계약이 다른 것을 억지로 통과시키면 그 계약이 막으려던
    것을 우회하게 된다.

    completion을 여기서 평가하지 않는 것은 의도적이다. 제151조가 묻는 것은 "벌금 이상의 형에
    해당하는 죄를 범한 사람인가"이고, 미수도 처벌규정이 있으면 죄다 -- 기수 여부는 이 신분
    판단의 요소가 아니라고 보았다. **이 점은 authoring-review item으로 남긴다.**
    """
    from idpr.v2 import expressions
    from idpr.v2.compile import CompiledOffense, compile_offense
    from idpr.v2.evaluate import FALSE, UNKNOWN, evaluate, fold_all
    from idpr.v2.runtime.stages import UtilizedParticipantOutcome

    compiled = compile_offense(registry, offense_ref)
    if not isinstance(compiled, CompiledOffense):
        raise ValueError(f"predecessor offense does not compile: {offense_ref!r}")
    elements_truth = fold_all(
        [evaluate(compiled.slots[slot], predicate_truths) for slot in expressions.SLOT_NAMES]
    )
    if elements_truth == FALSE:
        status = "elements_failure"
    elif elements_truth == UNKNOWN:
        status = "unresolved"
    else:
        status = "liable_exact_offense"
    return UtilizedParticipantOutcome(participant, offense_ref, status)


__all__ = [
    "LinkedOffenderDependency",
    "LinkedOffenderPredicateTarget",
    "PredecessorCandidateGate",
    "fold_linked_offender_outcome",
    "gate_predecessor_candidates",
    "linked_offender_dependencies",
    "linked_offender_predicate_targets",
]
