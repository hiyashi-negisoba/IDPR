"""Occurrence-aware Step 8 evaluation-instance planning.

The only top-level product is validated factual occurrence × that occurrence's
agents × frozen Step 7 candidate offenses.  Report targets never destructively
filter the assessment universe.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from idpr.v2 import expressions
from idpr.v2.closure import ClosureResult
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime import completion as completion_mod
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationRouteTarget,
    participation_route_targets,
)
from idpr.v2.runtime.relation_grounding import (
    RelationAssessmentTarget,
    relation_assessment_targets,
)

_OFFENSE_KINDS = frozenset({"offense", "derived_offense"})
_CLASSIFICATIONS = (
    "mandatory_core",
    "offense_probes",
    "doctrine_probes",
    "completion_probes",
    "participation_probes",
)


class EvaluationInstancePlannerError(ValueError):
    """A frozen-lineage or factual-identity invariant was violated."""


def selected_predicate_refs(
    registry: DefinitionRegistry, closure: ClosureResult
) -> tuple[str, ...]:
    """Stable-first instance-bound GroundFact/LegalElement Call 2 targets."""
    refs: list[str] = []
    seen: set[str] = set()
    for attribute in _CLASSIFICATIONS:
        for item in getattr(closure, attribute):
            for frontier in item.ground_fact_frontier:
                ref = frontier.ground_fact_ref
                if registry.kind_of(ref) != "ground_fact":
                    raise EvaluationInstancePlannerError(
                        f"closure frontier ref is not a GroundFact: {ref!r}"
                    )
                if ref not in seen:
                    seen.add(ref)
                    refs.append(ref)
            for ref in item.deferred_refs:
                if registry.kind_of(ref) == "legal_element" and ref not in seen:
                    seen.add(ref)
                    refs.append(ref)
    return tuple(refs)


@dataclass(frozen=True)
class OccurrenceAwareEvaluationInstancePlan:
    """One case's canonical factual and symbolic assessment universe."""

    case_id: str
    top10_seeds: tuple[str, ...]
    occurrences: tuple[GoldOccurrence, ...]
    candidate_offense_refs: tuple[str, ...]
    top_level_instances: tuple[OffenseInstanceKey, ...]
    predicate_scope_instances: tuple[OffenseInstanceKey, ...]
    assessment_instances: tuple[OffenseInstanceKey, ...]
    selected_predicate_refs: tuple[str, ...]
    assessment_targets: tuple[tuple[OffenseInstanceKey, str], ...]
    relation_assessment_targets: tuple[RelationAssessmentTarget, ...]
    participation_route_targets: tuple[ParticipationRouteTarget, ...]
    candidate_doctrine_refs: tuple[str, ...]

    @property
    def final_assessment_target_count(self) -> int:
        return len(self.assessment_targets)

    def as_dict(self) -> dict[str, Any]:
        def render(instance: OffenseInstanceKey) -> dict[str, str]:
            return {
                "case_id": instance.case_id,
                "actor_id": instance.actor_id,
                "offense_ref": instance.offense_ref,
                "occurrence_id": instance.occurrence_id,
            }

        assessment = [render(instance) for instance in self.assessment_instances]
        return {
            "sub_question_id": self.case_id,
            "top10_seeds": list(self.top10_seeds),
            "occurrences": [occurrence.as_dict() for occurrence in self.occurrences],
            "candidate_offense_refs": list(self.candidate_offense_refs),
            "top_level_instances": [render(value) for value in self.top_level_instances],
            "predicate_scope_instances": [
                render(value) for value in self.predicate_scope_instances
            ],
            "assessment_instances": assessment,
            "instances": assessment,
            "selected_predicate_refs": list(self.selected_predicate_refs),
            "assessment_targets": [
                {"instance_key": render(instance), "predicate_ref": ref}
                for instance, ref in self.assessment_targets
            ],
            "relation_assessment_targets": [value.as_dict() for value in self.relation_assessment_targets],
            "participation_route_targets": [
                value.as_dict() for value in self.participation_route_targets
            ],
            "candidate_doctrine_refs": list(self.candidate_doctrine_refs),
            "top_level_instance_count": len(self.top_level_instances),
            "predicate_scope_instance_count": len(self.predicate_scope_instances),
            "assessment_instance_count": len(self.assessment_instances),
            "selected_predicate_count": len(self.selected_predicate_refs),
            "final_assessment_target_count": self.final_assessment_target_count,
            "relation_assessment_target_count": len(self.relation_assessment_targets),
            "participation_route_target_count": len(self.participation_route_targets),
        }


def _validate_lineage(case_id: str, top10_seeds: Iterable[str]) -> tuple[str, ...]:
    seeds = tuple(top10_seeds)
    if (
        not seeds
        or len(seeds) > 10
        or any(not isinstance(seed, str) for seed in seeds)
        or len(set(seeds)) != len(seeds)
    ):
        raise EvaluationInstancePlannerError(f"{case_id}: invalid top10 seed lineage")
    return seeds


def _compile_candidates(
    registry: DefinitionRegistry,
    closure: ClosureResult,
    *,
    case_id: str,
) -> tuple[tuple[str, ...], dict[str, CompiledOffense], dict[str, Any]]:
    candidates = tuple(sorted(closure.candidate_offense_refs))
    if not candidates:
        raise EvaluationInstancePlannerError(f"{case_id}: closure has no candidate offense refs")
    compiled_by_ref: dict[str, CompiledOffense] = {}
    policies: dict[str, Any] = {}
    for ref in candidates:
        if registry.kind_of(ref) not in _OFFENSE_KINDS:
            raise EvaluationInstancePlannerError(
                f"{case_id}: non-offense candidate ref {ref!r}"
            )
        compiled = compile_offense(registry, ref)
        if not isinstance(compiled, CompiledOffense):
            raise EvaluationInstancePlannerError(
                f"{case_id}: candidate does not compile: {ref!r}"
            )
        compiled_by_ref[ref] = compiled
        policies[ref] = completion_mod.completion_policy_for(registry, ref)
    return candidates, compiled_by_ref, policies


def _component_scopes(
    top_level: Iterable[OffenseInstanceKey],
    compiled_by_ref: dict[str, CompiledOffense],
    policies: dict[str, Any],
) -> tuple[OffenseInstanceKey, ...]:
    values: list[OffenseInstanceKey] = []
    seen: set[OffenseInstanceKey] = set()
    for target in top_level:
        compiled = compiled_by_ref[target.offense_ref]
        policy = policies[target.offense_ref]
        if policy is None:
            continue
        wanted: list[tuple[str, str]] = []
        for state in policy.payload["states"].values():
            scope = state.get("when_component")
            if scope:
                wanted.append((scope["local_key"], scope["offense"]))
            if state.get("component_suspends"):
                wanted.extend(
                    (component.local_key, component.source_ref)
                    for component in compiled.components
                )
        for local_key, offense_ref in wanted:
            instance = completion_mod.component_instance_for(
                compiled, target, local_key, offense_ref
            )
            if (
                instance.case_id != target.case_id
                or instance.actor_id != target.actor_id
                or instance.occurrence_id != target.occurrence_id
            ):
                raise EvaluationInstancePlannerError(
                    "component scope failed case/actor/occurrence inheritance"
                )
            if instance not in seen:
                seen.add(instance)
                values.append(instance)
    return tuple(values)


def _instance_predicate_refs(
    registry: DefinitionRegistry, instance: OffenseInstanceKey
) -> tuple[str, ...]:
    """Predicates actually consumed by this offense instance and its completion policy."""
    compiled = compile_offense(registry, instance.offense_ref)
    if not isinstance(compiled, CompiledOffense):
        raise EvaluationInstancePlannerError(
            f"cannot compile predicate scope offense {instance.offense_ref!r}"
        )
    refs: list[str] = []
    seen: set[str] = set()

    def add(values: Iterable[str]) -> None:
        for ref in values:
            if registry.kind_of(ref) in {"ground_fact", "legal_element"} and ref not in seen:
                seen.add(ref)
                refs.append(ref)

    for slot in expressions.SLOT_NAMES:
        add(sorted(expressions.canonical_leaf_refs(compiled.slots[slot])))
    policy = completion_mod.completion_policy_for(registry, instance.offense_ref)
    if policy is not None:
        for state in policy.payload["states"].values():
            add(sorted(expressions.leaf_refs(state.get("when"))))
            add(sorted(expressions.leaf_refs(state.get("requires"))))
    return tuple(refs)


def plan_occurrence_aware_evaluation_instances(
    registry: DefinitionRegistry,
    closure: ClosureResult,
    *,
    case_id: str,
    top10_seeds: Iterable[str],
    occurrences: Iterable[GoldOccurrence],
) -> OccurrenceAwareEvaluationInstancePlan:
    """Materialize occurrence × occurrence agents × Step 7 candidates.

    The actor and occurrence identity comes only from the manually reviewed
    KCL-26 gold file.  Offense candidates remain frozen Step 7 output.
    """
    if not isinstance(case_id, str) or not case_id:
        raise EvaluationInstancePlannerError("case_id must be a non-empty string")
    seeds = _validate_lineage(case_id, top10_seeds)
    occurrence_values = tuple(occurrences)
    occurrence_ids = tuple(value.occurrence_id for value in occurrence_values)
    if (
        not occurrence_values
        or len(set(occurrence_ids)) != len(occurrence_ids)
        or any(value != f"gocc:{index:03d}" for index, value in enumerate(occurrence_ids, 1))
    ):
        raise EvaluationInstancePlannerError(f"{case_id}: invalid gold occurrence universe")
    for occurrence in occurrence_values:
        if not occurrence.actor_id or not occurrence.source_text:
            raise EvaluationInstancePlannerError(f"{case_id}: malformed gold occurrence")

    candidates, compiled_by_ref, policies = _compile_candidates(
        registry, closure, case_id=case_id
    )
    top_level = tuple(
        OffenseInstanceKey(case_id, occurrence.actor_id, ref, occurrence.occurrence_id)
        for occurrence in occurrence_values
        for ref in candidates
    )
    if len(top_level) != len(set(top_level)):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate top-level instance key")
    predicate_scopes = _component_scopes(top_level, compiled_by_ref, policies)
    assessment = tuple(dict.fromkeys((*top_level, *predicate_scopes)))
    if len(assessment) != len(set(assessment)):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate assessment instance key")
    target_values = tuple(
        (instance, ref)
        for instance in assessment
        for ref in _instance_predicate_refs(registry, instance)
    )
    selected_refs = tuple(dict.fromkeys(ref for _, ref in target_values))
    relation_targets = relation_assessment_targets(registry, assessment)
    participation_targets = participation_route_targets(registry, top_level)
    doctrine_refs = tuple(
        dict.fromkeys(item.definition_ref for item in closure.doctrine_probes)
    )
    return OccurrenceAwareEvaluationInstancePlan(
        case_id=case_id,
        top10_seeds=seeds,
        occurrences=occurrence_values,
        candidate_offense_refs=candidates,
        top_level_instances=top_level,
        predicate_scope_instances=predicate_scopes,
        assessment_instances=assessment,
        selected_predicate_refs=selected_refs,
        assessment_targets=target_values,
        relation_assessment_targets=relation_targets,
        participation_route_targets=participation_targets,
        candidate_doctrine_refs=doctrine_refs,
    )


__all__ = [
    "EvaluationInstancePlannerError",
    "OccurrenceAwareEvaluationInstancePlan",
    "plan_occurrence_aware_evaluation_instances",
    "selected_predicate_refs",
]
