"""Call 2 target 하나에 붙는 물리적 carrier -- 누가 target을 열었든 같은 계약.

이 모듈이 존재하는 이유는 하나의 결함 클래스가 세 번 반복됐기 때문이다.

    ordinary elements     -> evaluation planner        (carrier 계약 있음)
    participation target  -> participation plan 빌더    (자체 carrier 코드)
    doctrine leaf target  -> doctrine plan 빌더         (carrier 코드 없음)

target을 만드는 모듈이 carrier도 알아서 붙이는 구조였다. 그래서 `evidence_scope`를 고쳐도
그 수정이 다른 producer로 전달되지 않았고, doctrine 단계를 체인에 넣자 Call 2가
`missing=3`으로 처음 알려 줬다. 같은 invariant가 producer마다 흩어져 있으면 한 군데씩
터진다.

그래서 여기서 두 가지를 소유한다.

* :func:`carrier_kind_for` -- 어떤 종류의 사실이 이 predicate를 담는가. 저작된
  `evidence_scope`/`temporal_anchor`가 정하고, host가 다시 고르지 않는다.
* :func:`validate_plan_carriers` -- 최종 plan의 모든 target이 의미적으로 맞는 carrier를
  정확히 하나 갖는가. producer를 가리지 않는다.

새 target producer가 생겨도 carrier를 빼먹는 순간 plan 단계에서 실패한다. Call 2까지 가서
알게 되지 않는다.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from idpr.v2.registry import DefinitionRegistry

#: 관계 판단에만 쓰는 typed carrier. 행위자에게 국한된 사실이 아니라 사람 사이의 관계이므로
#: `evidence_scope` 계약을 타지 않는다. 예외는 이것 하나뿐이고, 이름으로 명시된다.
PARTICIPATION_CARRIER = "participation_action_or_realization"

_ACTOR_BOUND_ARGUMENTS = frozenset(
    {"actor", "witness", "offender", "disposer", "possessor", "official"}
)


class CarrierContractError(ValueError):
    """target과 carrier의 계약이 어긋났다. plan을 내보내지 않는다."""


def _actor_bound_ground_fact(registry: DefinitionRegistry, predicate_ref: str) -> bool:
    entry = registry.get(predicate_ref)
    if entry is None or entry.kind != "ground_fact":
        return False
    return any(
        isinstance(argument, dict)
        and argument.get("name") in _ACTOR_BOUND_ARGUMENTS
        for argument in entry.payload.get("arguments", ())
    )


def carrier_kind_for(
    registry: DefinitionRegistry,
    predicate_ref: str,
    *,
    actor_in_focal: bool,
) -> tuple[str, bool]:
    """`(carrier kind, 초점시점 고정 여부)`.

    Width is the definition's business.  An explicitly authored `evidence_scope` beats the
    generic actor-bound narrowing: that rule exists to stop another actor's conduct being
    read as this one's, and `actor_episode` already carries only actions this actor takes
    part in, so the attribution risk it guards against is absent.  Without an authored
    scope the generic rule still decides.

    `actor_in_focal`이 거짓이면 focal 전용 carrier로 좁히지 않는다. 가담자의 초점행위는
    정범의 실행이므로, 그리로 좁히면 carrier가 언급하지도 않는 행위자를 두고 묻게 된다.
    """
    entry = registry.get(predicate_ref)
    if entry is None:
        raise CarrierContractError(f"unknown predicate carrier: {predicate_ref!r}")
    scope = str(entry.payload.get("evidence_scope") or "")
    if scope == "same_actor_episode":
        carrier_kind = "actor_episode"
    elif scope == "exact_actor_action":
        carrier_kind = "focal_action"
    elif not scope and entry.kind == "ground_fact" and _actor_bound_ground_fact(
        registry, predicate_ref
    ):
        carrier_kind = "focal_action"
    else:
        carrier_kind = "realization"
    if carrier_kind == "focal_action" and not actor_in_focal:
        carrier_kind = "realization"
    return carrier_kind, entry.payload.get("temporal_anchor") == "focal_action"


def carrier_kind_label(carrier_kind: str, anchored_at_focal: bool) -> str:
    return f"{carrier_kind}_at_focal" if anchored_at_focal else carrier_kind


def resolve_carrier(
    registry: DefinitionRegistry,
    predicate_ref: str,
    *,
    provenance: Mapping[str, Any],
    occurrence_id: str,
) -> tuple[str, str]:
    """`(carrier_id, carrier_kind label)` -- plan이 이미 만들어 둔 carrier 중 계약에 맞는 것.

    새 carrier를 만들지 않는다. planner가 realization마다 기록해 둔 `carrier_ids`에서 고르고,
    계약이 요구하는 종류가 없으면 조용히 넓히지 않고 실패한다.
    """
    carrier_ids = provenance.get("carrier_ids") or {}
    if not isinstance(carrier_ids, Mapping):
        raise CarrierContractError(f"{occurrence_id}: malformed carrier provenance")
    if not carrier_ids:
        # 참가 후보는 planner가 만든 realization이 아니다. 하나의 명시적 상호작용 행위가
        # 그 후보의 증거 전부이므로 고를 carrier가 없고, occurrence 자체가 물리 carrier다.
        # 이것이 evidence_scope 계약을 타지 않는 유일한 예외이고, instance의 성질이지
        # predicate의 성질이 아니다.
        return occurrence_id, PARTICIPATION_CARRIER
    carrier_kind, anchored_at_focal = carrier_kind_for(
        registry,
        predicate_ref,
        actor_in_focal=bool(provenance.get("actor_in_focal_action")),
    )
    label = carrier_kind_label(carrier_kind, anchored_at_focal)
    carrier_id = carrier_ids.get(f"{carrier_kind}@focal" if anchored_at_focal else carrier_kind)
    if not carrier_id and anchored_at_focal:
        carrier_id = carrier_ids.get(carrier_kind)
    if not carrier_id and carrier_kind == "realization":
        # 참가 후보처럼 realization 자체가 물리 carrier인 경우.
        carrier_id = occurrence_id
    if not isinstance(carrier_id, str) or not carrier_id:
        raise CarrierContractError(
            f"{occurrence_id}: {predicate_ref} requires a {carrier_kind} carrier that "
            "this realization does not have"
        )
    return carrier_id, label


def validate_plan_carriers(
    registry: DefinitionRegistry, row: Mapping[str, Any]
) -> None:
    """이 사건의 모든 Call 2 target이 의미적으로 맞는 carrier를 정확히 하나 갖는가.

    target을 누가 열었는지 묻지 않는다. 그것이 이 검사의 요점이다.
    """
    case_id = str(row.get("sub_question_id", ""))
    carriers: dict[tuple[str, str, str, str], Mapping[str, Any]] = {}
    for value in row.get("assessment_carriers") or ():
        instance = value["instance_key"]
        key = (
            str(instance["actor_id"]),
            str(instance["offense_ref"]),
            str(instance["occurrence_id"]),
            str(value["predicate_ref"]),
        )
        if key in carriers:
            raise CarrierContractError(f"{case_id}: duplicate carrier for {key}")
        carriers[key] = value
    # provenance의 identity는 occurrence_id 하나가 아니다. 절도와 특수절도가 같은
    # `realization:001`을 공유하고 그 둘의 `actor_in_focal_action`이 다를 수 있다.
    provenance_by_instance = {
        (
            str(value["instance_key"]["actor_id"]),
            str(value["instance_key"]["offense_ref"]),
            str(value["instance_key"]["occurrence_id"]),
        ): value
        for value in row.get("instance_provenance") or ()
    }
    problems: list[str] = []
    for target in row.get("assessment_targets") or ():
        instance = target["instance_key"]
        occurrence_id = str(instance["occurrence_id"])
        key = (
            str(instance["actor_id"]),
            str(instance["offense_ref"]),
            occurrence_id,
            str(target["predicate_ref"]),
        )
        carrier = carriers.pop(key, None)
        if carrier is None:
            problems.append(f"target without carrier: {key} (opened_by={target.get('opened_by')})")
            continue
        supplied = str(carrier["carrier_kind"])
        if supplied == PARTICIPATION_CARRIER:
            # 관계 carrier는 evidence_scope 계약을 타지 않는 명시적 예외다.
            continue
        provenance = provenance_by_instance.get(key[:3])
        if provenance is None:
            problems.append(f"carrier without realization provenance: {key}")
            continue
        carrier_kind, anchored = carrier_kind_for(
            registry,
            str(target["predicate_ref"]),
            actor_in_focal=bool(provenance.get("actor_in_focal_action")),
        )
        expected = carrier_kind_label(carrier_kind, anchored)
        if supplied != expected:
            problems.append(
                f"carrier kind {supplied!r} does not match the authored contract "
                f"{expected!r}: {key}"
            )
    for key in carriers:
        problems.append(f"carrier without target: {key}")
    if problems:
        raise CarrierContractError(f"{case_id}: " + "; ".join(problems[:8]))


__all__ = [
    "PARTICIPATION_CARRIER",
    "CarrierContractError",
    "carrier_kind_for",
    "carrier_kind_label",
    "resolve_carrier",
    "validate_plan_carriers",
]
