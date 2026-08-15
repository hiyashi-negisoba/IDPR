"""Occurrence-aware Step 8 evaluation-instance planning.

This module preserves the current frozen planner for audit.  Its Cartesian
top-level expansion is not an approved production route.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from typing import Any

from idpr.v2 import expressions
from idpr.v2.closure import ClosureResult, compile_closure
from idpr.v2.runtime.linked_offender import (
    LinkedOffenderDependency,
    linked_offender_dependencies,
)
from idpr.v2.runtime.intended_object import (
    IntendedObjectDivergence,
    intended_object_divergences,
    offense_instance_probe_targets,
)
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.issue_binding import FactualAction, FactualEpisode, IssueBinding
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.carrier_contract import carrier_kind_for
from idpr.v2.runtime import completion as completion_mod
from idpr.v2.runtime.article263_grounding import Article263OccurrencePair
from idpr.v2.runtime.grounding import AssessmentTarget, grounding_request_targets
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.indirect_principal_grounding import (
    FactualUtilizationTarget,
    factual_utilization_targets,
)
from idpr.v2.runtime.participation_grounding import (
    ParticipationLocalTarget,
    participation_local_targets,
)
from idpr.v2.runtime.relation_grounding import (
    RelationAssessmentTarget,
    relation_assessment_targets,
)
from idpr.v2.runtime.utilized_participant_outcome import (
    UtilizedParticipantOutcomeTarget,
    UtilizedParticipantPredicateTarget,
    utilized_participant_outcome_targets,
    utilized_participant_predicate_targets,
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


@dataclass(frozen=True)
class LegalRealization:
    """Host-materialized legal evaluation unit over atomic factual actions."""

    realization_id: str
    factual_episode_id: str
    actor_id: str
    offense_ref: str
    focal_action_id: str | None
    supporting_action_ids: tuple[str, ...]
    source_binding_ids: tuple[str, ...]
    source_realization_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "realization_id": self.realization_id,
            "factual_episode_id": self.factual_episode_id,
            "actor_id": self.actor_id,
            "offense_ref": self.offense_ref,
            "focal_action_id": self.focal_action_id,
            "supporting_action_ids": list(self.supporting_action_ids),
            "source_binding_ids": list(self.source_binding_ids),
            "source_realization_ids": list(self.source_realization_ids),
        }


@dataclass(frozen=True)
class AssessmentCarrier:
    """One physical Call 2 evidence carrier assigned by predicate scope."""

    target: AssessmentTarget
    carrier_id: str
    carrier_kind: str

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.target.as_dict(),
            "carrier_id": self.carrier_id,
            "carrier_kind": self.carrier_kind,
        }


@dataclass(frozen=True)
class DerivedBindingCandidate:
    binding_id: str
    factual_episode_id: str
    actor_id: str
    offense_ref: str
    source_binding_ids: tuple[str, ...]
    authored_source_paths: tuple[tuple[str, ...], ...]
    required_binding_refs: tuple[str, ...]
    supporting_actor_ids: tuple[str, ...]
    source_realization_ids: tuple[str, ...] = ()
    realization_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "factual_episode_id": self.factual_episode_id,
            "actor_id": self.actor_id,
            "offense_ref": self.offense_ref,
            "source_binding_ids": list(self.source_binding_ids),
            "source_realization_ids": list(self.source_realization_ids),
            "realization_id": self.realization_id,
            "authored_source_paths": [list(value) for value in self.authored_source_paths],
            "candidate_generated_because": "required_same_episode_bindings",
            "required_binding_refs": list(self.required_binding_refs),
            "supporting_actor_ids": list(self.supporting_actor_ids),
            "semantic_effect": "candidate_construction_only",
        }


@dataclass(frozen=True)
class InstanceProvenance:
    """Where one top-level instance came from, for the later final-responsibility stage.

    Both fields are already decided upstream and are only carried here.  The concurrence and
    excess runtimes need them and have no other honest source: `OffenseInstanceKey` deliberately
    carries no episode identity, and re-deriving "same factual episode" downstream would mean
    reading the case text a second time in a place that must not read it at all.

    `source_binding_ids` is empty for a direct binding and holds the base bindings the planner
    actually combined for a derived one.  특별관계 흡수 reads exactly that record back rather than
    re-deriving the base/derived link, which is what keeps it deterministic.
    """

    instance: OffenseInstanceKey
    factual_episode_id: str
    source_binding_ids: tuple[str, ...] = ()
    realization_id: str = ""
    focal_action_id: str | None = None
    supporting_action_ids: tuple[str, ...] = ()
    source_realization_ids: tuple[str, ...] = ()
    carrier_ids: tuple[tuple[str, str], ...] = ()
    actor_in_focal_action: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "instance_key": {
                "case_id": self.instance.case_id,
                "actor_id": self.instance.actor_id,
                "offense_ref": self.instance.offense_ref,
                "occurrence_id": self.instance.occurrence_id,
            },
            "factual_episode_id": self.factual_episode_id,
            "source_binding_ids": list(self.source_binding_ids),
            "realization_id": self.realization_id or self.instance.occurrence_id,
            "focal_action_id": self.focal_action_id,
            "supporting_action_ids": list(self.supporting_action_ids),
            "source_realization_ids": list(self.source_realization_ids),
            "carrier_ids": dict(self.carrier_ids),
            "actor_in_focal_action": self.actor_in_focal_action,
        }


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
    neural_predicate_request_target_count: int
    relation_assessment_targets: tuple[RelationAssessmentTarget, ...]
    participation_local_targets: tuple[ParticipationLocalTarget, ...]
    factual_utilization_targets: tuple[FactualUtilizationTarget, ...]
    utilized_participant_outcome_targets: tuple[UtilizedParticipantOutcomeTarget, ...]
    utilized_participant_predicate_targets: tuple[UtilizedParticipantPredicateTarget, ...]
    candidate_doctrine_refs: tuple[str, ...]
    legal_realizations: tuple[LegalRealization, ...] = ()
    assessment_carriers: tuple[AssessmentCarrier, ...] = ()
    derived_binding_candidates: tuple[DerivedBindingCandidate, ...] = ()
    unbound_seed_refs: tuple[str, ...] = ()
    article263_pair_candidates: tuple[Article263OccurrencePair, ...] = ()
    context_only_binding_ids: tuple[str, ...] = ()
    instance_provenance: tuple[InstanceProvenance, ...] = ()
    linked_offender_dependencies: tuple[LinkedOffenderDependency, ...] = ()
    """다른 participant의 결과를 요구하는 규칙과, 그 사람. ROUTE 재호출의 입력이다."""

    intended_object_divergences: tuple[IntendedObjectDivergence, ...] = ()
    """대상 동일성이 사실로 확정된 realization. TRUE도 FALSE도 결정론적 산출이다.

    이 값이 있어야 착오 정책이 발화할 수 있고, TRUE인 자리에서만 객체의 착오 여부를 묻는
    neural target이 열린다.
    """

    factual_episode_order: tuple[str, ...] = ()
    """Call 1.5가 정한 factual episode의 서사 순서.

    초과 판정이 "정범의 실행에서 이어지는 범위"를 계산하려면 순서가 필요하다. episode id가
    사실상 순번이더라도 그 우연에 기대지 않는다 -- 순서는 상류가 정한 값이고, 여기서 문자열을
    정렬해 다시 만들면 id 규칙이 바뀌는 날 조용히 틀린다.
    """

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
            "participation_local_targets": [
                value.as_dict() for value in self.participation_local_targets
            ],
            "factual_utilization_targets": [
                value.as_dict() for value in self.factual_utilization_targets
            ],
            "utilized_participant_outcome_targets": [
                {
                    **value.as_dict(),
                    "predicate_refs": [
                        predicate.predicate_ref
                        for predicate in self.utilized_participant_predicate_targets
                        if predicate.outcome_target == value
                    ],
                }
                for value in self.utilized_participant_outcome_targets
            ],
            "candidate_doctrine_refs": list(self.candidate_doctrine_refs),
            "legal_realizations": [value.as_dict() for value in self.legal_realizations],
            "legal_realization_count": len(self.legal_realizations),
            "assessment_carriers": [value.as_dict() for value in self.assessment_carriers],
            "assessment_carrier_count": len(self.assessment_carriers),
            "derived_binding_candidates": [
                value.as_dict() for value in self.derived_binding_candidates
            ],
            "derived_binding_candidate_count": len(self.derived_binding_candidates),
            "unbound_seeds": [
                {"offense_ref": ref, "status": "UNBOUND_SEED"}
                for ref in self.unbound_seed_refs
            ],
            "unbound_seed_count": len(self.unbound_seed_refs),
            "article263_pair_candidates": [
                value.as_dict() for value in self.article263_pair_candidates
            ],
            "article263_pair_candidate_count": len(self.article263_pair_candidates),
            "context_only_bindings": [
                {"binding_id": value, "status": "CONTEXT_ONLY_BINDING"}
                for value in self.context_only_binding_ids
            ],
            "context_only_binding_count": len(self.context_only_binding_ids),
            "instance_provenance": [value.as_dict() for value in self.instance_provenance],
            "instance_provenance_count": len(self.instance_provenance),
            "linked_offender_dependencies": [
                value.as_dict() for value in self.linked_offender_dependencies
            ],
            "linked_offender_dependency_count": len(self.linked_offender_dependencies),
            "intended_object_divergences": [
                value.as_dict() for value in self.intended_object_divergences
            ],
            "intended_object_divergence_count": len(self.intended_object_divergences),
            "factual_episode_order": list(self.factual_episode_order),
            "top_level_instance_count": len(self.top_level_instances),
            "predicate_scope_instance_count": len(self.predicate_scope_instances),
            "assessment_instance_count": len(self.assessment_instances),
            "selected_predicate_count": len(self.selected_predicate_refs),
            "final_assessment_target_count": self.final_assessment_target_count,
            "neural_predicate_request_target_count": self.neural_predicate_request_target_count,
            "relation_assessment_target_count": len(self.relation_assessment_targets),
            "participation_local_target_count": len(self.participation_local_targets),
            "factual_utilization_target_count": len(self.factual_utilization_targets),
            "utilized_participant_outcome_target_count": len(
                self.utilized_participant_outcome_targets
            ),
            "utilized_participant_predicate_target_count": len(
                self.utilized_participant_predicate_targets
            ),
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
            if state.get("component_suspends") and all(
                component.component_kind == "offense"
                and component.resolved_kind in ("offense", "derived_offense")
                for component in compiled.components
            ):
                wanted.extend(
                    (scope["local_key"], scope["offense"])
                    for scope in state["component_suspends"]
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
    # An element the offense declares as resolved by a linked offender's own outcome is not a
    # question for a model.  Asking it anyway is how 제151조's status leaf became 6/6 UNKNOWN:
    # Call 2 was handed a cross-actor legal result dressed up as a fact about this instance.
    entry = registry.get(instance.offense_ref)
    dependency = (entry.payload.get("linked_offender_dependency") or {}) if entry else {}
    host_resolved = {dependency["resolved_element"]} if dependency.get("resolved_element") else set()

    def add(values: Iterable[str]) -> None:
        for ref in values:
            if ref in host_resolved:
                continue
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
            # blocker leaf도 정식 입력이다. 묻지 않으면 UNKNOWN으로 남아 아무것도 막지
            # 않으므로, 수집 누락이 "이 사건에는 예외가 없다"로 읽힌다.
            add(sorted(expressions.leaf_refs(state.get("blocked_when"))))
    return tuple(refs)


def plan_occurrence_aware_evaluation_instances(
    registry: DefinitionRegistry,
    closure: ClosureResult,
    *,
    case_id: str,
    top10_seeds: Iterable[str],
    occurrences: Iterable[GoldOccurrence],
    factual_participants: Iterable[GoldFactualParticipant] = (),
) -> OccurrenceAwareEvaluationInstancePlan:
    """Materialize the frozen occurrence x Step 7 candidate audit universe."""
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
    neural_request_target_count = len(
        grounding_request_targets(
            registry,
            tuple(AssessmentTarget(instance, ref) for instance, ref in target_values),
        )
    )
    relation_targets = relation_assessment_targets(registry, assessment)
    participation_targets = participation_local_targets(registry, top_level)
    utilization_targets = factual_utilization_targets(
        registry, top_level, factual_participants
    )
    participant_outcome_targets = utilized_participant_outcome_targets(
        registry, top_level, factual_participants
    )
    participant_predicate_targets = utilized_participant_predicate_targets(
        registry, participant_outcome_targets
    )
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
        neural_predicate_request_target_count=neural_request_target_count,
        relation_assessment_targets=relation_targets,
        participation_local_targets=participation_targets,
        factual_utilization_targets=utilization_targets,
        utilized_participant_outcome_targets=participant_outcome_targets,
        utilized_participant_predicate_targets=participant_predicate_targets,
        candidate_doctrine_refs=doctrine_refs,
    )


def _actor_bound_ground_fact(registry: DefinitionRegistry, predicate_ref: str) -> bool:
    entry = registry.get(predicate_ref)
    if entry is None or entry.kind != "ground_fact":
        return False
    return any(
        isinstance(argument, dict)
        and argument.get("name")
        in {"actor", "witness", "offender", "disposer", "possessor", "official"}
        for argument in entry.payload.get("arguments", ())
    )


def _actor_participates_in_focal(
    action_by_id: dict[str, FactualAction], realization: LegalRealization
) -> bool:
    """Whether the liable actor is a participant of its focal action.

    False for accessories and instigators, whose focal action is the principal's
    execution.  A focal-only carrier is unreadable for those actors, so this
    gates every narrowing decision downstream.
    """
    if realization.focal_action_id is None:
        return False
    return realization.actor_id in action_by_id[realization.focal_action_id].participant_ids


def _ordered_action_evidence(
    action_by_id: dict[str, FactualAction], action_ids: Iterable[str]
) -> tuple[str, int, int]:
    fragments = [
        fragment
        for action_id in action_ids
        for fragment in action_by_id[action_id].source_fragments
    ]
    ordered = sorted(
        {(
            fragment.source_start,
            fragment.source_end,
            fragment.source_quote,
        ) for fragment in fragments}
    )
    if not ordered:
        raise EvaluationInstancePlannerError("legal realization has no factual action evidence")
    return (
        "\n".join(quote for _, _, quote in ordered),
        min(start for start, _, _ in ordered),
        max(end for _, end, _ in ordered),
    )


def _plan_action_atomic_binding_instances(
    registry: DefinitionRegistry,
    *,
    case_id: str,
    bindings: Iterable[IssueBinding],
    factual_episodes: Iterable[FactualEpisode] = (),
    allowed_candidate_offense_refs: Iterable[str] | None = None,
    unbound_seed_refs: Iterable[str] = (),
    case_text: str | None = None,
    liability_source_spans: Iterable[tuple[int, int]] | None = None,
) -> OccurrenceAwareEvaluationInstancePlan:
    """Materialize action-scoped legal realizations from Call 1.5 candidates.

    The only route from a binding to an occurrence is this host materialization.
    A binding id remains provenance; it is never an occurrence id.
    """
    all_bindings = tuple(bindings)
    if tuple(value.binding_id for value in all_bindings) != tuple(
        f"binding:{index:03d}" for index in range(1, len(all_bindings) + 1)
    ):
        raise EvaluationInstancePlannerError(f"{case_id}: noncanonical binding ids")
    episodes = tuple(factual_episodes)
    episode_by_id = {value.factual_episode_id: value for value in episodes}
    if len(episode_by_id) != len(episodes):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate factual episode ids")
    action_by_id = {
        action.factual_action_id: action
        for episode in episodes
        for action in episode.factual_actions
    }
    if len(action_by_id) != sum(len(value.factual_actions) for value in episodes):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate factual action ids")
    for binding in all_bindings:
        episode = episode_by_id.get(binding.factual_episode_id)
        focal = action_by_id.get(binding.focal_action_id)
        supports = [action_by_id.get(action_id) for action_id in binding.supporting_action_ids]
        if (
            episode is None
            or focal is None
            or focal.factual_episode_id != binding.factual_episode_id
            or any(action is None or action.factual_episode_id != binding.factual_episode_id for action in supports)
        ):
            raise EvaluationInstancePlannerError(
                f"{case_id}/{binding.binding_id}: dangling factual action identity"
            )
        # Accessories and instigators are bound to the principal's execution
        # action, so the liable actor only has to appear in the evidence this
        # realization carries -- focal action plus the supports Call 1.5 chose.
        carried_participants = set(focal.participant_ids)
        for action in supports:
            carried_participants.update(action.participant_ids)
        if binding.actor_id not in carried_participants:
            raise EvaluationInstancePlannerError(
                f"{case_id}/{binding.binding_id}: liable actor is outside its carried actions"
            )
    source_spans = tuple(liability_source_spans or ())
    if any(start < 0 or end <= start for start, end in source_spans):
        raise EvaluationInstancePlannerError(f"{case_id}: invalid liability source span")
    if source_spans:
        active_bindings = tuple(
            binding
            for binding in all_bindings
            if any(
                fragment.source_start < target_end and target_start < fragment.source_end
                for fragment in action_by_id[binding.focal_action_id].source_fragments
                for target_start, target_end in source_spans
            )
        )
    else:
        active_bindings = all_bindings
    active_binding_ids = {binding.binding_id for binding in active_bindings}
    context_only_binding_ids = tuple(
        binding.binding_id
        for binding in all_bindings
        if binding.binding_id not in active_binding_ids
    )
    allowed_candidates = (
        frozenset(allowed_candidate_offense_refs)
        if allowed_candidate_offense_refs is not None
        else None
    )

    grouped: dict[tuple[str, str, str, str, tuple[str, ...]], list[IssueBinding]] = {}
    for binding in active_bindings:
        key = (
            binding.factual_episode_id,
            binding.actor_id,
            binding.offense_ref,
            binding.focal_action_id,
            binding.supporting_action_ids,
        )
        grouped.setdefault(key, []).append(binding)
    legal_realizations: list[LegalRealization] = []
    top_level: list[OffenseInstanceKey] = []
    realization_by_id: dict[str, LegalRealization] = {}
    binding_to_realization: dict[str, str] = {}
    closure_candidates: list[str] = []
    doctrine_refs: list[str] = []
    for group_index, (key, group) in enumerate(grouped.items(), 1):
        episode_id, actor_id, offense_ref, focal_action_id, supporting_action_ids = key
        realization_id = f"realization:{group_index:03d}"
        realization = LegalRealization(
            realization_id,
            episode_id,
            actor_id,
            offense_ref,
            focal_action_id,
            supporting_action_ids,
            tuple(binding.binding_id for binding in group),
        )
        legal_realizations.append(realization)
        realization_by_id[realization_id] = realization
        for binding in group:
            binding_to_realization[binding.binding_id] = realization_id
        top_level.append(OffenseInstanceKey(case_id, actor_id, offense_ref, realization_id))
        closure = compile_closure(registry, (offense_ref,))
        closure_candidates.extend(sorted(closure.candidate_offense_refs))
        doctrine_refs.extend(item.definition_ref for item in closure.doctrine_probes)

    # Derived candidates still use the authored closure rule, but their structural
    # dependency now follows legal realizations rather than source binding ids.
    derived_candidates: list[DerivedBindingCandidate] = []
    direct_by_episode_actor: dict[tuple[str, str], list[LegalRealization]] = {}
    for realization in legal_realizations:
        direct_by_episode_actor.setdefault(
            (realization.factual_episode_id, realization.actor_id), []
        ).append(realization)
    for (episode_id, actor_id), direct_realizations in direct_by_episode_actor.items():
        direct_refs = tuple(dict.fromkeys(value.offense_ref for value in direct_realizations))
        local_closure = compile_closure(registry, direct_refs)
        local_candidates = {
            ref
            for ref in local_closure.candidate_offense_refs
            if registry.kind_of(ref) == "derived_offense" and ref not in direct_refs
        }
        if allowed_candidates is not None:
            local_candidates &= allowed_candidates
        probe_paths: dict[str, list[tuple[str, ...]]] = {}
        for item in local_closure.offense_probes:
            probe_paths.setdefault(item.definition_ref, []).append(item.source_path)
        supporting_ids: dict[str, tuple[str, ...]] = {
            ref: tuple(
                value.realization_id
                for value in direct_realizations
                if value.offense_ref == ref
            )
            for ref in direct_refs
        }
        pending = set(local_candidates)
        while pending:
            materialized = False
            for offense_ref in sorted(pending):
                entry = registry.get(offense_ref)
                metadata = entry.payload.get("candidate_materialization") if entry else None
                if not isinstance(metadata, dict):
                    continue
                if metadata.get("episode_constraint") != "same":
                    raise EvaluationInstancePlannerError(
                        f"{case_id}/{offense_ref}: unsupported episode constraint"
                    )
                binding_sets = metadata.get("binding_sets", [])
                peer_binding_sets = metadata.get("distinct_actor_binding_sets", [])
                if not isinstance(binding_sets, list) or not isinstance(peer_binding_sets, list):
                    raise EvaluationInstancePlannerError(
                        f"{case_id}/{offense_ref}: malformed materialization metadata"
                    )
                matched = next(
                    (
                        tuple(refs)
                        for refs in binding_sets
                        if isinstance(refs, list)
                        and len(refs) >= 2
                        and all(isinstance(ref, str) and ref in supporting_ids for ref in refs)
                    ),
                    None,
                )
                peer_matched: tuple[str, ...] | None = None
                peer_realizations: tuple[LegalRealization, ...] = ()
                if matched is None:
                    for refs in peer_binding_sets:
                        if (
                            not isinstance(refs, list)
                            or not refs
                            or not all(isinstance(ref, str) and ref in supporting_ids for ref in refs)
                        ):
                            continue
                        candidates = tuple(
                            value
                            for (candidate_episode, candidate_actor), values in direct_by_episode_actor.items()
                            if candidate_episode == episode_id and candidate_actor != actor_id
                            for value in values
                            if value.offense_ref in refs
                        )
                        if {value.offense_ref for value in candidates} >= set(refs):
                            peer_matched = tuple(refs)
                            peer_realizations = candidates
                            break
                if matched is None and peer_matched is None:
                    continue
                required_refs = matched if matched is not None else peer_matched
                assert required_refs is not None
                source_realization_ids = tuple(
                    dict.fromkeys(
                        (
                            *(
                                realization_id
                                for ref in required_refs
                                for realization_id in supporting_ids[ref]
                            ),
                            *(value.realization_id for value in peer_realizations),
                        )
                    )
                )
                source_realizations = [
                    realization_by_id[realization_id]
                    for realization_id in source_realization_ids
                ]
                source_binding_ids = tuple(
                    dict.fromkeys(
                        binding_id
                        for realization in source_realizations
                        for binding_id in realization.source_binding_ids
                    )
                )
                candidate_id = f"derived_binding:{len(derived_candidates) + 1:03d}"
                realization_id = f"realization:derived:{len(derived_candidates) + 1:03d}"
                provenance = tuple(probe_paths.get(offense_ref, ()))
                if not provenance:
                    raise EvaluationInstancePlannerError(
                        f"{case_id}/{offense_ref}: derived candidate lacks authored probe path"
                    )
                derived_candidates.append(
                    DerivedBindingCandidate(
                        candidate_id,
                        episode_id,
                        actor_id,
                        offense_ref,
                        source_binding_ids,
                        provenance,
                        required_refs,
                        tuple(
                            dict.fromkeys(
                                (actor_id, *(value.actor_id for value in peer_realizations))
                            )
                        ),
                        source_realization_ids,
                        realization_id,
                    )
                )
                action_ids = tuple(
                    dict.fromkeys(
                        action_id
                        for realization in source_realizations
                        for action_id in (
                            (realization.focal_action_id, *realization.supporting_action_ids)
                            if realization.focal_action_id is not None
                            else realization.supporting_action_ids
                        )
                    )
                )
                derived = LegalRealization(
                    realization_id,
                    episode_id,
                    actor_id,
                    offense_ref,
                    None,
                    action_ids,
                    source_binding_ids,
                    source_realization_ids,
                )
                legal_realizations.append(derived)
                realization_by_id[realization_id] = derived
                top_level.append(
                    OffenseInstanceKey(case_id, actor_id, offense_ref, realization_id)
                )
                supporting_ids[offense_ref] = (realization_id,)
                closure_candidates.append(offense_ref)
                pending.remove(offense_ref)
                materialized = True
            if not materialized:
                break

    top_level_values = tuple(top_level)
    if len(top_level_values) != len(set(top_level_values)):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate realization instance")
    selected_offenses = tuple(dict.fromkeys(value.offense_ref for value in top_level_values))
    compiled_by_ref: dict[str, CompiledOffense] = {}
    policies: dict[str, Any] = {}
    for ref in selected_offenses:
        compiled = compile_offense(registry, ref)
        if not isinstance(compiled, CompiledOffense):
            raise EvaluationInstancePlannerError(f"{case_id}: realization offense does not compile")
        compiled_by_ref[ref] = compiled
        policies[ref] = completion_mod.completion_policy_for(registry, ref)
    predicate_scopes = _component_scopes(top_level_values, compiled_by_ref, policies)
    assessment = tuple(dict.fromkeys((*top_level_values, *predicate_scopes)))
    # 지향 대상과 결과 귀속 대상이 둘 다 사실로 결박된 realization에서만 불일치를 센다.
    # 불일치가 TRUE인 자리에서만 `applies_to: offense_instance` probe의 neural leaf를 연다 --
    # 대상이 같은 사안에 "객체의 착오였는가"를 물으면 없는 착오를 만들 자리만 생긴다.
    realization_tuples = tuple(
        (
            realization.realization_id,
            realization.actor_id,
            realization.offense_ref,
            realization.source_binding_ids,
        )
        for realization in legal_realizations
    )
    # 저작이 다른 사람의 결과를 요구하고 Call 1.5가 그 사람을 결박했으면, 그에 대해 ROUTE를
    # 다시 호출해야 한다. 여기서는 그 필요를 기록만 하고 선행범죄를 고르지 않는다.
    linked_dependencies = linked_offender_dependencies(
        registry,
        case_id=case_id,
        realizations=realization_tuples,
        bindings=active_bindings,
        factual_actions=action_by_id.values(),
    )
    divergences = intended_object_divergences(
        case_id=case_id,
        realizations=tuple(
            (
                realization.realization_id,
                realization.actor_id,
                realization.offense_ref,
                realization.source_binding_ids,
            )
            for realization in legal_realizations
        ),
        bindings=active_bindings,
    )
    target_values = tuple(
        dict.fromkeys(
            (
                *(
                    (instance, ref)
                    for instance in assessment
                    for ref in _instance_predicate_refs(registry, instance)
                ),
                *offense_instance_probe_targets(registry, divergences),
            )
        )
    )
    assessment_targets = tuple(AssessmentTarget(instance, ref) for instance, ref in target_values)
    selected_predicates = tuple(dict.fromkeys(ref for _, ref in target_values))

    carrier_occurrences: dict[str, GoldOccurrence] = {}
    carrier_assignments: list[AssessmentCarrier] = []
    carrier_ids_by_realization: dict[str, dict[str, str]] = {}
    def ensure_carrier(
        realization: LegalRealization, carrier_kind: str, anchored_at_focal: bool = False
    ) -> str:
        cache_key = f"{carrier_kind}@focal" if anchored_at_focal else carrier_kind
        ids = carrier_ids_by_realization.setdefault(realization.realization_id, {})
        if cache_key in ids:
            return ids[cache_key]
        if carrier_kind == "focal_action":
            if realization.focal_action_id is None:
                # 좁히라고 한 폭을 넓혀서 내주면 label과 물리 carrier가 갈라진다.
                # 모델은 label을 읽고 판단 범위를 정하므로, 그 갈라짐은 "증거는 넓게 줄 테니
                # 좁게 판단하라"는 모순된 지시가 된다. 줄 수 없으면 여기서 멈춘다.
                raise EvaluationInstancePlannerError(
                    f"{case_id}: {realization.realization_id} has no focal action to carry "
                    "a focal_action-scoped predicate"
                )
            action_ids = (realization.focal_action_id,)
        elif carrier_kind == "actor_episode":
            # `same_actor_episode` is the widest authored scope: every action of this
            # episode the responsibility actor takes part in, not only the ones the
            # binding selected.  Peer actors' actions stay out -- the whole point of the
            # scope is to widen the actor's own factual record, not the episode's.
            action_ids = tuple(
                action.factual_action_id
                for action in sorted(
                    (
                        value
                        for value in action_by_id.values()
                        if value.factual_episode_id == realization.factual_episode_id
                        and realization.actor_id in value.participant_ids
                    ),
                    key=lambda value: value.sequence_index,
                )
            )
            if not action_ids:
                # 이 행위자가 참여한 행위가 이 episode에 하나도 없으면 `same_actor_episode`가
                # 가리키는 사실 자체가 없다. realization으로 갈아 끼우면 폭이 달라진 것을
                # label이 감추므로, 없는 것은 없다고 말한다.
                raise EvaluationInstancePlannerError(
                    f"{case_id}: {realization.actor_id} has no action in "
                    f"{realization.factual_episode_id} to carry an actor_episode-scoped "
                    "predicate"
                )
        else:
            action_ids = tuple(
                dict.fromkeys(
                    (
                        (realization.focal_action_id, *realization.supporting_action_ids)
                        if realization.focal_action_id is not None
                        else realization.supporting_action_ids
                    )
                )
            )
            carrier_kind = "realization"
        if anchored_at_focal:
            if realization.focal_action_id is None:
                # 초점행위가 없으면 자를 시점이 없다. 그대로 두면 carrier는 초점 이후 사실까지
                # 담은 채 `_at_focal`로 이름 붙고, 소급 사용 금지 계약이 이름만 남는다.
                raise EvaluationInstancePlannerError(
                    f"{case_id}: {realization.realization_id} has no focal action to anchor "
                    "a temporally anchored predicate"
                )
            # `temporal_anchor: focal_action` fixes the moment being judged, not the width
            # of the record.  Dropping only what happens after the focal action keeps a
            # later consumption or flight out of a receipt-time question while still
            # admitting the scope its definition authored.  Collapsing the carrier to the
            # focal action instead is what left 자기이득 목적 at 100% UNKNOWN.
            limit = action_by_id[realization.focal_action_id].sequence_index
            action_ids = tuple(
                value for value in action_ids if action_by_id[value].sequence_index <= limit
            )
            carrier_kind = f"{carrier_kind}_at_focal"
        source_text, source_start, source_end = _ordered_action_evidence(action_by_id, action_ids)
        # A legal realization is offense-scoped, but an evidence carrier is factual.
        # Separate offense candidates can therefore reuse one action carrier without
        # being projected from a whole factual episode.  Keep the focal action in the
        # realization carrier signature too: the same support set around a different
        # focal action is a different temporal/legal question.
        signature = tuple(
            value
            for value in (
                realization.focal_action_id,
                *realization.supporting_action_ids,
            )
            if value is not None
        )
        carrier_id = ":".join(
            (
                "carrier",
                carrier_kind,
                realization.actor_id,
                *signature,
            )
        )
        occurrence = GoldOccurrence(
            carrier_id,
            realization.actor_id,
            source_text,
            source_start,
            source_end,
        )
        previous = carrier_occurrences.get(carrier_id)
        if previous is not None and previous != occurrence:
            raise EvaluationInstancePlannerError(
                f"{case_id}: factual carrier identity has inconsistent evidence"
            )
        carrier_occurrences[carrier_id] = occurrence
        ids[cache_key] = carrier_id
        return carrier_id
    for target in assessment_targets:
        realization = realization_by_id.get(target.instance_key.occurrence_id)
        if realization is None:
            raise EvaluationInstancePlannerError(
                f"{case_id}: target lacks legal realization provenance"
            )
        carrier_kind, anchored_at_focal = carrier_kind_for(
            registry,
            target.predicate_ref,
            actor_in_focal=_actor_participates_in_focal(action_by_id, realization),
        )
        carrier_id = ensure_carrier(realization, carrier_kind, anchored_at_focal)
        carrier_assignments.append(
            AssessmentCarrier(
                target,
                carrier_id,
                f"{carrier_kind}_at_focal" if anchored_at_focal else carrier_kind,
            )
        )
    carrier_by_target = {value.target: value.carrier_id for value in carrier_assignments}
    neural_count = len(
        grounding_request_targets(
            registry, assessment_targets, carrier_by_target=carrier_by_target
        )
    )

    # Relation and participation paths retain their realization-level evidence
    # lookup.  Add that alias alongside the physical predicate carriers.
    realization_occurrences: list[GoldOccurrence] = []
    for realization in legal_realizations:
        source_text, source_start, source_end = _ordered_action_evidence(
            action_by_id,
            (
                (realization.focal_action_id, *realization.supporting_action_ids)
                if realization.focal_action_id is not None
                else realization.supporting_action_ids
            ),
        )
        realization_occurrences.append(
            GoldOccurrence(
                realization.realization_id,
                realization.actor_id,
                source_text,
                source_start,
                source_end,
            )
        )
    relation_targets = relation_assessment_targets(registry, assessment)
    binding_by_id = {binding.binding_id: binding for binding in active_bindings}
    article263_pairs: list[Article263OccurrencePair] = []
    injury_realizations = tuple(
        value for value in legal_realizations if value.offense_ref == "offense.injury"
    )
    for left, right in combinations(injury_realizations, 2):
        # episode 동일성은 요구하지 않는다. 제263조는 "독립행위가 경합하여 상해 결과를
        # 발생하게 한 경우 원인된 행위가 판명되지 아니한 때"라고만 하고 시간적 동시성을
        # 요구하지 않으며, 대법원 80도3321은 약 3시간 간격의 이시(異時) 독립 상해행위에도
        # 이 조문을 적용했다. episode 경계는 법적 요건이 아니라 Call 1.5가 서사를 나눈
        # 결과이므로, 그것을 join 조건으로 쓰면 판례가 정면으로 인정하는 사안을 구조적으로
        # 잘라낸다 -- `r10_p1_q2`의 2시간 간격이 정확히 그 경우였다.
        #
        # episode 동일성이 지고 있던 실질(같은 피해자에 대한 두 독립행위)은 아래 두 조건이
        # 이미 각각 지고 있다: 서로 다른 행위자, 그리고 factual_targets의 교집합.
        if left.actor_id == right.actor_id:
            continue
        left_targets = {
            target
            for binding_id in left.source_binding_ids
            for target in binding_by_id[binding_id].factual_targets
        }
        right_targets = {
            target
            for binding_id in right.source_binding_ids
            for target in binding_by_id[binding_id].factual_targets
        }
        if not (left_targets & right_targets):
            continue
        fragments = tuple(
            fragment
            for episode_id in dict.fromkeys(
                (left.factual_episode_id, right.factual_episode_id)
            )
            for fragment in episode_by_id[episode_id].source_fragments
        )
        if not fragments:
            continue
        # 두 episode를 아우르는 범위. 한쪽 episode만 주면 다른 쪽 행위가 증거에서 빠진다.
        start = min(fragment.source_start for fragment in fragments)
        end = max(fragment.source_end for fragment in fragments)
        relation_text = (
            case_text[start:end]
            if case_text is not None
            else "\n".join(fragment.source_quote for fragment in fragments)
        )
        article263_pairs.append(
            Article263OccurrencePair(
                f"article263-pair:{len(article263_pairs) + 1:04d}",
                OffenseInstanceKey(case_id, left.actor_id, left.offense_ref, left.realization_id),
                OffenseInstanceKey(case_id, right.actor_id, right.offense_ref, right.realization_id),
                relation_text,
                start,
                end,
            )
        )
    provenance_values = tuple(
        InstanceProvenance(
            instance,
            realization_by_id[instance.occurrence_id].factual_episode_id,
            realization_by_id[instance.occurrence_id].source_binding_ids,
            realization_by_id[instance.occurrence_id].realization_id,
            realization_by_id[instance.occurrence_id].focal_action_id,
            realization_by_id[instance.occurrence_id].supporting_action_ids,
            realization_by_id[instance.occurrence_id].source_realization_ids,
            tuple(
                sorted(
                    carrier_ids_by_realization.get(instance.occurrence_id, {}).items()
                )
            ),
            _actor_participates_in_focal(
                action_by_id, realization_by_id[instance.occurrence_id]
            ),
        )
        for instance in assessment
    )
    episode_sequence = tuple(value.factual_episode_id for value in episodes)
    return OccurrenceAwareEvaluationInstancePlan(
        case_id=case_id,
        top10_seeds=selected_offenses,
        occurrences=tuple((*realization_occurrences, *carrier_occurrences.values())),
        candidate_offense_refs=tuple(dict.fromkeys(closure_candidates)),
        top_level_instances=top_level_values,
        predicate_scope_instances=predicate_scopes,
        assessment_instances=assessment,
        selected_predicate_refs=selected_predicates,
        assessment_targets=target_values,
        neural_predicate_request_target_count=neural_count,
        relation_assessment_targets=relation_targets,
        participation_local_targets=(),
        factual_utilization_targets=(),
        utilized_participant_outcome_targets=(),
        utilized_participant_predicate_targets=(),
        candidate_doctrine_refs=tuple(dict.fromkeys(doctrine_refs)),
        legal_realizations=tuple(legal_realizations),
        assessment_carriers=tuple(carrier_assignments),
        derived_binding_candidates=tuple(derived_candidates),
        unbound_seed_refs=tuple(dict.fromkeys(unbound_seed_refs)),
        article263_pair_candidates=tuple(article263_pairs),
        context_only_binding_ids=context_only_binding_ids,
        instance_provenance=provenance_values,
        linked_offender_dependencies=linked_dependencies,
        intended_object_divergences=divergences,
        factual_episode_order=episode_sequence,
    )


def plan_binding_scoped_evaluation_instances(
    registry: DefinitionRegistry,
    *,
    case_id: str,
    bindings: Iterable[IssueBinding],
    factual_episodes: Iterable[FactualEpisode] = (),
    allowed_candidate_offense_refs: Iterable[str] | None = None,
    unbound_seed_refs: Iterable[str] = (),
    case_text: str | None = None,
    liability_source_spans: Iterable[tuple[int, int]] | None = None,
) -> OccurrenceAwareEvaluationInstancePlan:
    return _plan_action_atomic_binding_instances(
        registry,
        case_id=case_id,
        bindings=bindings,
        factual_episodes=factual_episodes,
        allowed_candidate_offense_refs=allowed_candidate_offense_refs,
        unbound_seed_refs=unbound_seed_refs,
        case_text=case_text,
        liability_source_spans=liability_source_spans,
    )

__all__ = [
    "DerivedBindingCandidate",
    "LegalRealization",
    "AssessmentCarrier",
    "InstanceProvenance",
    "EvaluationInstancePlannerError",
    "OccurrenceAwareEvaluationInstancePlan",
    "plan_binding_scoped_evaluation_instances",
    "plan_occurrence_aware_evaluation_instances",
    "selected_predicate_refs",
]
