"""Local typed participation grounding and deterministic dependency compilation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Literal

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.participation import (
    co_principal_established_predicate_refs,
    derivative_mode_subsumptions,
    participation_policy_for,
)
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey, realization_identity
from idpr.v2.runtime.truths import CaseTruths, TruthValue

ParticipationRelationKind = Literal["instigation", "aiding", "co_principal_group"]


class ParticipationGroundingError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


def _instance(value: OffenseInstanceKey) -> dict[str, str]:
    return {
        "case_id": value.case_id,
        "actor_id": value.actor_id,
        "offense_ref": value.offense_ref,
        "occurrence_id": value.occurrence_id,
    }


@dataclass(frozen=True)
class ParticipationLocalTarget:
    kind: ParticipationRelationKind
    members: tuple[OffenseInstanceKey, ...]

    @property
    def case_id(self) -> str:
        return self.members[0].case_id

    @property
    def offense_ref(self) -> str:
        return self.members[0].offense_ref

    @property
    def actor(self) -> OffenseInstanceKey:
        if self.kind == "co_principal_group":
            raise ParticipationGroundingError(["co-principal group has no derivative actor"])
        return self.members[0]

    @property
    def principal(self) -> OffenseInstanceKey:
        if self.kind == "co_principal_group":
            raise ParticipationGroundingError(["co-principal group has no derivative principal"])
        return self.members[1]

    def as_dict(self) -> dict[str, Any]:
        return {
            "relation_kind": self.kind,
            "group_key": {
                "case_id": self.case_id,
                "offense_ref": self.offense_ref,
            },
            "member_instances": [_instance(value) for value in self.members],
        }


@dataclass(frozen=True)
class ParticipationLocalAssessment:
    target: ParticipationLocalTarget
    truth: TruthValue

    def as_dict(self) -> dict[str, Any]:
        return {**self.target.as_dict(), "truth": self.truth}


@dataclass(frozen=True)
class ParticipationBindings:
    co_principal_sources: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...]
    derivative_links: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...]
    mode_resolutions: tuple[dict[str, Any], ...] = ()


def add_co_principal_established_truths(
    registry: DefinitionRegistry,
    truths: CaseTruths,
    bindings: ParticipationBindings,
) -> tuple[CaseTruths, tuple[dict[str, Any], ...]]:
    """Project predicates entailed by validated TRUE co-principal relations."""
    policy = participation_policy_for(registry)
    if policy is None:
        return truths, ()
    refs = co_principal_established_predicate_refs(policy)
    if not refs:
        return truths, ()
    members = {
        instance for pair in bindings.co_principal_sources for instance in pair
    }
    predicate = dict(truths.predicate)
    projections: list[dict[str, Any]] = []
    for instance in sorted(
        members,
        key=lambda value: (
            value.case_id,
            value.actor_id,
            value.offense_ref,
            value.occurrence_id,
        ),
    ):
        for ref in sorted(refs):
            prior = predicate.get((instance, ref))
            predicate[(instance, ref)] = "TRUE"
            projections.append(
                {
                    "instance_key": _instance(instance),
                    "predicate_ref": ref,
                    "prior_truth": prior,
                    "truth": "TRUE",
                    "derived_from": "validated_co_principal_group",
                }
            )
    return CaseTruths(predicate=predicate, relation=truths.relation), tuple(projections)


def _validate_target(target: ParticipationLocalTarget) -> None:
    members = target.members
    errors: list[str] = []
    if target.kind not in {"instigation", "aiding", "co_principal_group"}:
        errors.append("unknown participation relation kind")
    if target.kind in {"instigation", "aiding"} and len(members) != 2:
        errors.append("derivative local relation requires actor and principal")
    if target.kind == "co_principal_group" and len(members) < 2:
        errors.append("co-principal group requires at least two members")
    if not members:
        errors.append("participation local target has no members")
    elif any(
        value.case_id != members[0].case_id
        or value.offense_ref != members[0].offense_ref
        for value in members
    ):
        errors.append("participation members differ from case/offense group identity")
    if len(members) != len(set(members)):
        errors.append("participation local target contains duplicate instances")
    if len({value.actor_id for value in members}) != len(members):
        errors.append("participation local target repeats an actor")
    if errors:
        raise ParticipationGroundingError(errors)


def participation_local_targets(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
) -> tuple[ParticipationLocalTarget, ...]:
    """Enumerate independent local relations without choosing a legal route."""
    values = tuple(instances)
    if len(values) != len(set(values)):
        raise ParticipationGroundingError(["participation instances contain duplicates"])
    grouped: dict[tuple[str, str], list[OffenseInstanceKey]] = {}
    for instance in values:
        offense = registry.get(instance.offense_ref)
        if offense is None or offense.kind not in {"offense", "derived_offense"}:
            raise ParticipationGroundingError(["participation endpoint is not an offense"])
        grouped.setdefault((instance.case_id, instance.offense_ref), []).append(instance)
    output: list[ParticipationLocalTarget] = []
    for group_instances in grouped.values():
        offense = registry.get(group_instances[0].offense_ref)
        assert offense is not None
        disabled = frozenset(
            (offense.payload.get("participation_constraints") or {}).get(
                "disabled_modes"
            )
            or ()
        )
        for actor in group_instances:
            for principal in group_instances:
                if actor.actor_id == principal.actor_id:
                    continue
                if "instigator" not in disabled:
                    output.append(
                        ParticipationLocalTarget("instigation", (actor, principal))
                    )
                if "aider" not in disabled:
                    output.append(ParticipationLocalTarget("aiding", (actor, principal)))
        if "co_principal" not in disabled:
            for size in range(2, len(group_instances) + 1):
                for members in combinations(group_instances, size):
                    if len({value.actor_id for value in members}) == size:
                        output.append(
                            ParticipationLocalTarget("co_principal_group", members)
                        )
    for target in output:
        _validate_target(target)
    if len(output) != len(set(output)):
        raise ParticipationGroundingError(["duplicate participation local target"])
    return tuple(output)


def participation_request_payload(
    *,
    registry: DefinitionRegistry,
    occurrences: Iterable[GoldOccurrence],
    targets: Iterable[ParticipationLocalTarget],
) -> dict[str, Any]:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise ParticipationGroundingError(
            ["one participation request must contain exactly one local relation"]
        )
    target = target_values[0]
    _validate_target(target)
    occurrence_values = tuple(occurrences)
    occurrence_by_id = {value.occurrence_id: value for value in occurrence_values}
    required_ids = {value.occurrence_id for value in target.members}
    errors: list[str] = []
    if len(occurrence_by_id) != len(occurrence_values) or set(occurrence_by_id) != required_ids:
        errors.append("participation evidence must exactly equal relation member occurrences")
    for instance in target.members:
        occurrence = occurrence_by_id.get(instance.occurrence_id)
        if occurrence is None or occurrence.actor_id != instance.actor_id:
            errors.append("participation endpoint differs from gold occurrence identity")
    offense = registry.get(target.offense_ref)
    if offense is None or offense.kind not in {"offense", "derived_offense"}:
        errors.append("participation offense definition is missing")
    if errors:
        raise ParticipationGroundingError(errors)
    assert offense is not None
    relation_contract: dict[str, Any]
    if target.kind == "instigation":
        relation_contract = {
            "predicate": "actor intentionally causes principal to decide and commit the exact offense",
            "actor_instance": _instance(target.actor),
            "principal_instance": _instance(target.principal),
        }
    elif target.kind == "aiding":
        relation_contract = {
            "predicate": (
                "actor intentionally facilitates execution of the exact offense after "
                "principal has formed the criminal intent independently of actor"
            ),
            "actor_instance": _instance(target.actor),
            "principal_instance": _instance(target.principal),
        }
    else:
        relation_contract = {
            "predicate": "all members jointly execute the exact offense under a shared criminal plan",
            "member_instances": [_instance(value) for value in target.members],
        }
    return {
        "occurrence_evidence": [
            occurrence_by_id[value].as_dict() for value in sorted(required_ids)
        ],
        "offense_definition": {
            "definition_id": offense.id,
            "kind": offense.kind,
            **dict(offense.payload),
        },
        "local_relation_target": target.as_dict(),
        "relation_contract": relation_contract,
    }


def participation_schema(targets: Iterable[ParticipationLocalTarget]) -> dict[str, Any]:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise ParticipationGroundingError(
            ["participation schema requires one local relation"]
        )
    _validate_target(target_values[0])
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["truth"],
        "properties": {
            "truth": {"type": "string", "enum": ["TRUE", "FALSE", "UNKNOWN"]}
        },
    }


def validate_participation_output(
    payload: Any, *, targets: Iterable[ParticipationLocalTarget]
) -> ParticipationLocalAssessment:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise ParticipationGroundingError(
            ["participation validation requires one local relation"]
        )
    target = target_values[0]
    _validate_target(target)
    if (
        not isinstance(payload, Mapping)
        or set(payload) != {"truth"}
        or payload["truth"] not in {"TRUE", "FALSE", "UNKNOWN"}
    ):
        raise ParticipationGroundingError(["participation truth response mismatch"])
    return ParticipationLocalAssessment(target, payload["truth"])


def _node_for(
    instance: OffenseInstanceKey,
    co_group_by_member: Mapping[OffenseInstanceKey, frozenset[OffenseInstanceKey]],
) -> frozenset[OffenseInstanceKey]:
    return co_group_by_member.get(instance, frozenset((instance,)))


def compile_participation_bindings(
    assessments: Iterable[ParticipationLocalAssessment],
    *,
    expected_targets: Iterable[ParticipationLocalTarget] | None = None,
    registry: DefinitionRegistry | None = None,
) -> ParticipationBindings:
    """Compile local truths, applying only explicitly authored mode subsumption."""
    values = tuple(assessments)
    targets = tuple(value.target for value in values)
    if expected_targets is not None:
        expected = tuple(expected_targets)
        if targets != expected:
            raise ParticipationGroundingError(
                ["local participation assessments do not exactly match expected targets"]
            )
    for target in targets:
        _validate_target(target)
    if len(targets) != len(set(targets)):
        raise ParticipationGroundingError(["duplicate participation local assessment"])
    grouped: dict[tuple[str, str], list[ParticipationLocalAssessment]] = {}
    for assessment in values:
        grouped.setdefault(
            (assessment.target.case_id, assessment.target.offense_ref), []
        ).append(assessment)
    policy = participation_policy_for(registry) if registry is not None else None
    authored_subsumptions = (
        derivative_mode_subsumptions(policy) if policy is not None else {}
    )
    mode_conflicts: list[str] = []
    subsumed_targets: set[ParticipationLocalTarget] = set()
    mode_resolutions: list[dict[str, Any]] = []
    for key, group_values in grouped.items():
        modes_by_logical_edge: dict[
            tuple[str, OffenseInstanceKey], set[ParticipationRelationKind]
        ] = {}
        for value in group_values:
            if value.truth != "TRUE" or value.target.kind not in {
                "instigation",
                "aiding",
            }:
                continue
            logical_edge = (
                value.target.actor.actor_id,
                value.target.principal,
            )
            modes_by_logical_edge.setdefault(logical_edge, set()).add(
                value.target.kind
            )
        for (actor_id, principal), relation_kinds in modes_by_logical_edge.items():
            if relation_kinds != {"instigation", "aiding"}:
                continue
            policy_modes = {
                "instigation": "instigator",
                "aiding": "aider",
            }
            dominant_kind: ParticipationRelationKind | None = None
            subsumed_kind: ParticipationRelationKind | None = None
            for candidate in ("instigation", "aiding"):
                other = "aiding" if candidate == "instigation" else "instigation"
                if policy_modes[other] in authored_subsumptions.get(
                    policy_modes[candidate], frozenset()
                ):
                    dominant_kind = candidate
                    subsumed_kind = other
                    break
            if dominant_kind is None or subsumed_kind is None:
                mode_conflicts.append(
                    f"{key}: CONFLICTING_PARTICIPATION_MODE for "
                    f"source={actor_id} principal={principal.actor_id}/"
                    f"{principal.occurrence_id}"
                )
                continue
            matching = [
                value for value in group_values
                if value.truth == "TRUE"
                and value.target.kind == subsumed_kind
                and value.target.actor.actor_id == actor_id
                and value.target.principal == principal
            ]
            subsumed_targets.update(value.target for value in matching)
            mode_resolutions.append({
                "case_id": key[0],
                "offense_ref": key[1],
                "participant_id": actor_id,
                "principal_instance": _instance(principal),
                "dominant_mode": policy_modes[dominant_kind],
                "subsumed_mode": policy_modes[subsumed_kind],
                "raw_dominant_truth": "TRUE",
                "raw_subsumed_truth": "TRUE",
                "resolution_basis": "authored_participation_policy",
            })
    if mode_conflicts:
        raise ParticipationGroundingError(mode_conflicts)
    co_sources: list[tuple[OffenseInstanceKey, OffenseInstanceKey]] = []
    derivative_links: list[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = []
    for key, group_values in grouped.items():
        instances = {
            member for value in group_values for member in value.target.members
        }
        true_co = tuple(
            frozenset(value.target.members)
            for value in group_values
            if value.truth == "TRUE" and value.target.kind == "co_principal_group"
        )
        # 같은 사람들 사이의 같은 관계가 두 상호작용에서 각각 확인되면 후보 instance가
        # 상호작용마다 따로 만들어진다. 甲과 乙의 특수절도 공동정범은 그렇게 두 번 나와도
        # 하나의 관계이지 서로 다투는 두 주장이 아니다.
        #
        # 그렇다고 행위자 구성만으로 접으면 반대쪽으로 틀린다 -- 甲·乙이 함께 절도를 두 번
        # 저지르면 그것은 두 개의 관계다. 상호작용 중복과 법적 중복은 다른 것이고, 둘을
        # 가르는 것은 그 group이 가리키는 **realization**이다. 후보 instance의 occurrence는
        # 증거 식별자라 관계의 신원이 되지 못하지만(그래서 `None`으로 접힌다), 실현 instance의
        # occurrence는 신원이 된다.
        #
        # 정규화가 subset 억제보다 **먼저** 와야 한다. raw instance로 먼저 억제하면, 같은
        # 관계의 더 좁은 주장이 상호작용별 후보 occurrence 때문에 subset으로 보이지 않아
        # 살아남고, 그 뒤 정규화해도 이미 늦어 실현 instance에서 겹쳐 계약 위반으로 죽는다.
        # `r13_p1_q1`이 그랬다 -- {甲,乙,丙}과 {甲,丙}이 서로 다른 상호작용에서 나와
        # 丙의 후보 occurrence가 달랐고, 행위자로 보면 후자가 전자의 부분집합이었다.
        by_relation: dict[
            frozenset[tuple[str, str | None]], frozenset[OffenseInstanceKey]
        ] = {}
        for group in sorted(
            true_co,
            key=lambda value: sorted(
                (i.case_id, i.actor_id, i.offense_ref, i.occurrence_id) for i in value
            ),
        ):
            by_relation.setdefault(
                frozenset(
                    (item.actor_id, realization_identity(item)) for item in group
                ),
                group,
            )
        relations = tuple(by_relation)
        maximal_relations = tuple(
            relation
            for relation in relations
            if not any(relation < other for other in relations)
        )
        maximal_co = tuple(by_relation[relation] for relation in maximal_relations)
        # 여기 남은 겹침은 행위자 구성 자체가 다른 두 주장이다. 어느 쪽이 옳은지는 이
        # 단계가 정할 수 없으므로 양보시키지 않고 계약 위반으로 올린다.
        for left, right in combinations(maximal_relations, 2):
            if left & right:
                raise ParticipationGroundingError(
                    [f"{key}: overlapping co-principal group truths"]
                )
        co_group_by_member: dict[
            OffenseInstanceKey, frozenset[OffenseInstanceKey]
        ] = {}
        for group in maximal_co:
            for member in group:
                co_group_by_member[member] = group
            for target in sorted(group, key=lambda value: (
                value.case_id, value.actor_id, value.offense_ref, value.occurrence_id
            )):
                for source in sorted(group - {target}, key=lambda value: (
                    value.case_id, value.actor_id, value.offense_ref, value.occurrence_id
                )):
                    co_sources.append((target, source))
        # 정범 경로와 종범 경로가 한 사람에게 동시에 참일 수 있다. 저작이 그 우선관계를
        # 선언해 두면 여기서 양보시키고, 선언이 없을 때만 계약 위반으로 올린다. 우선관계
        # 없음을 예외로 처리하면 사건 하나가 통째로 중단되므로 unresolved보다 나쁘다.
        co_principal_dominates = authored_subsumptions.get("co_principal", frozenset())
        for value in group_values:
            if (
                value.truth != "TRUE"
                or value.target.kind not in {"instigation", "aiding"}
                or value.target in subsumed_targets
                or value.target.actor not in co_group_by_member
            ):
                continue
            mode = "instigator" if value.target.kind == "instigation" else "aider"
            if mode not in co_principal_dominates:
                continue
            subsumed_targets.add(value.target)
            mode_resolutions.append({
                "case_id": key[0],
                "offense_ref": key[1],
                "participant_id": value.target.actor.actor_id,
                "principal_instance": _instance(value.target.principal),
                "dominant_mode": "co_principal",
                "subsumed_mode": mode,
                "raw_dominant_truth": "TRUE",
                "raw_subsumed_truth": "TRUE",
                "resolution_basis": "authored_participation_policy",
            })
        true_derivative = tuple(
            value
            for value in group_values
            if value.truth == "TRUE"
            and value.target.kind in {"instigation", "aiding"}
            and value.target not in subsumed_targets
        )
        by_actor: dict[OffenseInstanceKey, list[ParticipationLocalAssessment]] = {}
        for value in true_derivative:
            by_actor.setdefault(value.target.actor, []).append(value)
        if any(len(relations) != 1 for relations in by_actor.values()):
            raise ParticipationGroundingError(
                [f"{key}: participant has multiple derivative relations"]
            )
        if any(actor in co_group_by_member for actor in by_actor):
            raise ParticipationGroundingError(
                [f"{key}: participant has both co-principal and derivative routes"]
            )
        node_edges: dict[
            frozenset[OffenseInstanceKey], frozenset[OffenseInstanceKey]
        ] = {}
        for actor, relations in by_actor.items():
            relation = relations[0]
            principal = relation.target.principal
            if actor not in instances or principal not in instances:
                raise ParticipationGroundingError([f"{key}: dangling derivative endpoint"])
            actor_node = _node_for(actor, co_group_by_member)
            principal_node = _node_for(principal, co_group_by_member)
            if actor_node == principal_node:
                raise ParticipationGroundingError([f"{key}: derivative self-loop"])
            node_edges[actor_node] = principal_node
            mode = "instigator" if relation.target.kind == "instigation" else "aider"
            derivative_links.append((actor, principal, mode))
        complete: set[frozenset[OffenseInstanceKey]] = set()
        for start in node_edges:
            path: set[frozenset[OffenseInstanceKey]] = set()
            current = start
            while current in node_edges:
                if current in path:
                    raise ParticipationGroundingError(
                        [f"{key}: derivative dependency cycle"]
                    )
                path.add(current)
                current = node_edges[current]
            complete.update(path)
    return ParticipationBindings(
        tuple(co_sources), tuple(derivative_links), tuple(mode_resolutions)
    )


__all__ = [
    "ParticipationBindings",
    "ParticipationGroundingError",
    "ParticipationLocalAssessment",
    "ParticipationLocalTarget",
    "add_co_principal_established_truths",
    "compile_participation_bindings",
    "participation_local_targets",
    "participation_request_payload",
    "participation_schema",
    "validate_participation_output",
]
