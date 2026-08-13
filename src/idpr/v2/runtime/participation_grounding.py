"""Local typed participation grounding and deterministic dependency compilation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Literal

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import TruthValue

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
) -> ParticipationBindings:
    """Compile resolved local truths; never repair conflicts or dependency failures."""
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
    mode_conflicts: list[str] = []
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
        mode_conflicts.extend(
            f"{key}: CONFLICTING_PARTICIPATION_MODE for "
            f"source={actor_id} principal={principal.actor_id}/"
            f"{principal.occurrence_id}"
            for (actor_id, principal), modes in modes_by_logical_edge.items()
            if modes == {"instigation", "aiding"}
        )
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
        maximal_co = tuple(
            group
            for group in true_co
            if not any(group < other for other in true_co)
        )
        for left, right in combinations(maximal_co, 2):
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
        true_derivative = tuple(
            value
            for value in group_values
            if value.truth == "TRUE" and value.target.kind in {"instigation", "aiding"}
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
    return ParticipationBindings(tuple(co_sources), tuple(derivative_links))


__all__ = [
    "ParticipationBindings",
    "ParticipationGroundingError",
    "ParticipationLocalAssessment",
    "ParticipationLocalTarget",
    "compile_participation_bindings",
    "participation_local_targets",
    "participation_request_payload",
    "participation_schema",
    "validate_participation_output",
]
