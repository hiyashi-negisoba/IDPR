"""Closed-option Call 2 grounding for participation caller bindings."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Literal

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey

ParticipationMode = Literal["co_principal", "instigator", "aider", "none", "unknown"]


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
class ParticipationRouteOption:
    option_id: str
    mode: ParticipationMode
    sources: tuple[OffenseInstanceKey, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "mode": self.mode,
            "source_instances": [_instance(value) for value in self.sources],
        }


@dataclass(frozen=True)
class ParticipationRouteTarget:
    participant: OffenseInstanceKey
    options: tuple[ParticipationRouteOption, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "participant_instance": _instance(self.participant),
            "route_options": [value.as_dict() for value in self.options],
        }

    def option(self, option_id: str) -> ParticipationRouteOption:
        matches = tuple(value for value in self.options if value.option_id == option_id)
        if len(matches) != 1:
            raise ParticipationGroundingError([f"unknown route option: {option_id!r}"])
        return matches[0]


@dataclass(frozen=True)
class ParticipationRouteAssessment:
    target: ParticipationRouteTarget
    option_id: str

    @property
    def selected(self) -> ParticipationRouteOption:
        return self.target.option(self.option_id)

    def as_dict(self) -> dict[str, Any]:
        return {**self.target.as_dict(), "option_id": self.option_id}


@dataclass(frozen=True)
class ParticipationBindings:
    co_principal_sources: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...]
    derivative_links: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...]


def participation_route_targets(
    registry: DefinitionRegistry,
    instances: Iterable[OffenseInstanceKey],
) -> tuple[ParticipationRouteTarget, ...]:
    """One globally exclusive route choice per participant offense instance."""
    values = tuple(instances)
    if len(values) != len(set(values)):
        raise ParticipationGroundingError(["participation instances contain duplicates"])
    output: list[ParticipationRouteTarget] = []
    for participant in values:
        offense = registry.get(participant.offense_ref)
        if offense is None or offense.kind not in {"offense", "derived_offense"}:
            raise ParticipationGroundingError(["participation endpoint is not an offense"])
        sources = tuple(
            value
            for value in values
            if value.case_id == participant.case_id
            and value.offense_ref == participant.offense_ref
            and value.actor_id != participant.actor_id
        )
        if not sources:
            continue
        disabled = frozenset(
            (offense.payload.get("participation_constraints") or {}).get("disabled_modes") or ()
        )
        options: list[ParticipationRouteOption] = [
            ParticipationRouteOption("none", "none"),
            ParticipationRouteOption("unknown", "unknown"),
        ]
        if "co_principal" not in disabled:
            option_index = 1
            for size in range(1, len(sources) + 1):
                for source_group in combinations(sources, size):
                    options.append(
                        ParticipationRouteOption(
                            f"co_principal:{option_index:04d}",
                            "co_principal",
                            tuple(source_group),
                        )
                    )
                    option_index += 1
        for mode in ("instigator", "aider"):
            if mode in disabled:
                continue
            options.extend(
                ParticipationRouteOption(f"{mode}:{index:04d}", mode, (source,))
                for index, source in enumerate(sources, 1)
            )
        output.append(ParticipationRouteTarget(participant, tuple(options)))
    if len(output) != len(set(output)):
        raise ParticipationGroundingError(["duplicate participation route target"])
    return tuple(output)


def shard_participation_targets_by_pair(
    targets: Iterable[ParticipationRouteTarget], *, max_targets: int
) -> tuple[tuple[ParticipationRouteTarget, ...], ...]:
    """Each target has a distinct option enum and exact evidence universe; keep it isolated."""
    if max_targets <= 0:
        raise ParticipationGroundingError(["max_targets must be positive"])
    return tuple((value,) for value in targets)


def participation_request_payload(
    *,
    registry: DefinitionRegistry,
    occurrences: Iterable[GoldOccurrence],
    targets: Iterable[ParticipationRouteTarget],
) -> dict[str, Any]:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise ParticipationGroundingError(
            ["one participation request must contain exactly one exclusive target"]
        )
    target = target_values[0]
    source_instances = tuple(
        dict.fromkeys(source for option in target.options for source in option.sources)
    )
    required_instances = (target.participant, *source_instances)
    occurrence_values = tuple(occurrences)
    occurrence_by_id = {value.occurrence_id: value for value in occurrence_values}
    required_ids = {value.occurrence_id for value in required_instances}
    errors: list[str] = []
    if len(occurrence_by_id) != len(occurrence_values) or set(occurrence_by_id) != required_ids:
        errors.append("participation evidence must exactly equal the option endpoint occurrences")
    for instance in required_instances:
        occurrence = occurrence_by_id.get(instance.occurrence_id)
        if occurrence is None or occurrence.actor_id != instance.actor_id:
            errors.append("participation endpoint differs from gold occurrence identity")
    offense = registry.get(target.participant.offense_ref)
    if offense is None or offense.kind not in {"offense", "derived_offense"}:
        errors.append("participation offense definition is missing")
    if errors:
        raise ParticipationGroundingError(errors)
    assert offense is not None
    return {
        "occurrence_evidence": [occurrence_by_id[value].as_dict() for value in sorted(required_ids)],
        "offense_definition": {
            "definition_id": offense.id,
            "kind": offense.kind,
            **dict(offense.payload),
        },
        "route_target": target.as_dict(),
        "mode_contract": {
            "co_principal": "joint commission; every listed source contributes attributable conduct",
            "instigator": "participant intentionally causes the one source to decide and commit the offense",
            "aider": "participant intentionally facilitates the one source's commission of the offense",
            "none": "the evidence affirmatively concerns no participation route for this exact offense",
            "unknown": "the exact-offense participation route is evidentially unresolved",
        },
    }


def participation_schema(targets: Iterable[ParticipationRouteTarget]) -> dict[str, Any]:
    target_values = tuple(targets)
    if len(target_values) != 1:
        raise ParticipationGroundingError(["participation schema requires one target"])
    option_ids = [value.option_id for value in target_values[0].options]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["option_id"],
        "properties": {"option_id": {"type": "string", "enum": option_ids}},
    }


def validate_participation_output(
    payload: Any, *, targets: Iterable[ParticipationRouteTarget]
) -> tuple[ParticipationRouteAssessment, ...]:
    expected = tuple(targets)
    if len(expected) != 1:
        raise ParticipationGroundingError(["participation validation requires one target"])
    if not isinstance(payload, Mapping) or set(payload) != {"option_id"}:
        raise ParticipationGroundingError(["participation response shape mismatch"])
    option_id = payload["option_id"]
    if not isinstance(option_id, str):
        raise ParticipationGroundingError(["participation option_id must be a string"])
    expected[0].option(option_id)
    return (ParticipationRouteAssessment(expected[0], option_id),)


def participation_bindings_from_assessments(
    assessments: Iterable[ParticipationRouteAssessment],
) -> ParticipationBindings:
    values = tuple(assessments)
    targets = tuple(value.target for value in values)
    if len(targets) != len(set(targets)):
        raise ParticipationGroundingError(["duplicate exclusive participation target"])
    co_sources: list[tuple[OffenseInstanceKey, OffenseInstanceKey]] = []
    derivatives: list[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = []
    for assessment in values:
        option = assessment.selected
        if option.mode in {"none", "unknown"}:
            continue
        if option.mode == "co_principal":
            co_sources.extend((assessment.target.participant, source) for source in option.sources)
        else:
            if len(option.sources) != 1:
                raise ParticipationGroundingError(["derivative option must have one source"])
            derivatives.append(
                (assessment.target.participant, option.sources[0], option.mode)
            )
    return ParticipationBindings(tuple(co_sources), tuple(derivatives))


__all__ = [
    "ParticipationBindings",
    "ParticipationGroundingError",
    "ParticipationRouteAssessment",
    "ParticipationRouteOption",
    "ParticipationRouteTarget",
    "participation_bindings_from_assessments",
    "participation_request_payload",
    "participation_route_targets",
    "participation_schema",
    "shard_participation_targets_by_pair",
    "validate_participation_output",
]
