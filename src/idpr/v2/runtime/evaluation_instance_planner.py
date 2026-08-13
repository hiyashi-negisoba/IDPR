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
from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.issue_binding import FactualEpisode, IssueBinding
from idpr.v2.registry import DefinitionRegistry
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
class DerivedBindingCandidate:
    binding_id: str
    factual_episode_id: str
    actor_id: str
    offense_ref: str
    source_binding_ids: tuple[str, ...]
    authored_source_paths: tuple[tuple[str, ...], ...]
    required_binding_refs: tuple[str, ...]
    supporting_actor_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "factual_episode_id": self.factual_episode_id,
            "actor_id": self.actor_id,
            "offense_ref": self.offense_ref,
            "source_binding_ids": list(self.source_binding_ids),
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
    derived_binding_candidates: tuple[DerivedBindingCandidate, ...] = ()
    unbound_seed_refs: tuple[str, ...] = ()
    article263_pair_candidates: tuple[Article263OccurrencePair, ...] = ()
    context_only_binding_ids: tuple[str, ...] = ()
    instance_provenance: tuple[InstanceProvenance, ...] = ()

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
    """Materialize one top-level evaluation context per Call 1.5 binding.

    Actor-action and contextual fragments inside one binding are joined into one
    evidence carrier while remaining typed in the Call 1.5 artifact. Closure remains scoped to the binding. Conditional closure
    offenses are recorded as candidates but are not implicitly promoted to
    top-level instances; a separate host rule must create a derived binding.
    """
    all_binding_values = tuple(bindings)
    if tuple(value.binding_id for value in all_binding_values) != tuple(
        f"binding:{index:03d}" for index in range(1, len(all_binding_values) + 1)
    ):
        raise EvaluationInstancePlannerError(f"{case_id}: noncanonical binding ids")
    source_spans = tuple(liability_source_spans or ())
    if any(start < 0 or end <= start for start, end in source_spans):
        raise EvaluationInstancePlannerError(f"{case_id}: invalid liability source span")
    if source_spans:
        binding_values = tuple(
            binding
            for binding in all_binding_values
            if any(
                fragment.source_start < target_end
                and target_start < fragment.source_end
                for fragment in binding.actor_action_fragments
                for target_start, target_end in source_spans
            )
        )
    else:
        binding_values = all_binding_values
    active_binding_ids = {value.binding_id for value in binding_values}
    context_only_binding_ids = tuple(
        value.binding_id
        for value in all_binding_values
        if value.binding_id not in active_binding_ids
    )

    episode_values = tuple(factual_episodes)
    episode_by_id = {value.factual_episode_id: value for value in episode_values}
    if len(episode_by_id) != len(episode_values):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate factual episode ids")
    if episode_values and any(
        binding.factual_episode_id not in episode_by_id for binding in binding_values
    ):
        raise EvaluationInstancePlannerError(f"{case_id}: dangling binding episode identity")
    allowed_candidates = (
        frozenset(allowed_candidate_offense_refs)
        if allowed_candidate_offense_refs is not None
        else None
    )
    evidence: list[GoldOccurrence] = []
    top_level: list[OffenseInstanceKey] = []
    closure_candidates: list[str] = []
    doctrine_refs: list[str] = []
    for binding in binding_values:
        combined = binding.evidence_text
        if not combined:
            raise EvaluationInstancePlannerError(
                f"{case_id}/{binding.binding_id}: empty binding evidence"
            )
        evidence.append(
            GoldOccurrence(binding.binding_id, binding.actor_id, combined, 0, len(combined))
        )
        top_level.append(
            OffenseInstanceKey(
                case_id, binding.actor_id, binding.offense_ref, binding.binding_id
            )
        )
        binding_closure = compile_closure(registry, (binding.offense_ref,))
        closure_candidates.extend(sorted(binding_closure.candidate_offense_refs))
        doctrine_refs.extend(item.definition_ref for item in binding_closure.doctrine_probes)

    derived_bindings: list[DerivedBindingCandidate] = []
    grouped: dict[tuple[str, str], list[IssueBinding]] = {}
    for binding in binding_values:
        grouped.setdefault((binding.factual_episode_id, binding.actor_id), []).append(binding)
    for (episode_id, actor_id), episode_bindings in grouped.items():
        if episode_id not in episode_by_id:
            continue
        episode = episode_by_id[episode_id]
        direct_refs = tuple(dict.fromkeys(value.offense_ref for value in episode_bindings))
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
        episode_text = "\n".join(
            value.source_quote for value in episode.source_fragments
        )
        supporting_ids: dict[str, tuple[str, ...]] = {
            value.offense_ref: tuple(
                item.binding_id
                for item in episode_bindings
                if item.offense_ref == value.offense_ref
            )
            for value in episode_bindings
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
                if not isinstance(binding_sets, list) or not isinstance(
                    peer_binding_sets, list
                ):
                    raise EvaluationInstancePlannerError(
                        f"{case_id}/{offense_ref}: malformed materialization metadata"
                    )
                for refs in (*binding_sets, *peer_binding_sets):
                    if any(registry.kind_of(ref) not in _OFFENSE_KINDS for ref in refs):
                        raise EvaluationInstancePlannerError(
                            f"{case_id}/{offense_ref}: materialization binding ref is not an offense"
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
                peer_bindings: tuple[IssueBinding, ...] = ()
                if matched is None:
                    for refs in peer_binding_sets:
                        if (
                            not isinstance(refs, list)
                            or not refs
                            or not all(
                                isinstance(ref, str) and ref in supporting_ids
                                for ref in refs
                            )
                        ):
                            continue
                        candidates = tuple(
                            value
                            for value in binding_values
                            if value.factual_episode_id == episode_id
                            and value.actor_id != actor_id
                            and value.offense_ref in refs
                        )
                        if {value.offense_ref for value in candidates} >= set(refs):
                            peer_matched = tuple(refs)
                            peer_bindings = candidates
                            break
                if matched is None and peer_matched is None:
                    continue
                required_refs = matched if matched is not None else peer_matched
                assert required_refs is not None
                source_binding_ids = tuple(
                    dict.fromkeys(
                        binding_id
                        for ref in required_refs
                        for binding_id in supporting_ids[ref]
                    )
                ) + tuple(value.binding_id for value in peer_bindings)
                binding_id = f"derived_binding:{len(derived_bindings) + 1:03d}"
                provenance = tuple(probe_paths.get(offense_ref, ()))
                if not provenance:
                    raise EvaluationInstancePlannerError(
                        f"{case_id}/{offense_ref}: derived candidate lacks authored probe path"
                    )
                derived_bindings.append(
                    DerivedBindingCandidate(
                        binding_id,
                        episode_id,
                        actor_id,
                        offense_ref,
                        source_binding_ids,
                        provenance,
                        required_refs,
                        tuple(
                            dict.fromkeys(
                                (actor_id, *(value.actor_id for value in peer_bindings))
                            )
                        ),
                    )
                )
                supporting_ids[offense_ref] = (binding_id,)
                evidence.append(
                    GoldOccurrence(binding_id, actor_id, episode_text, 0, len(episode_text))
                )
                top_level.append(
                    OffenseInstanceKey(case_id, actor_id, offense_ref, binding_id)
                )
                closure_candidates.append(offense_ref)
                pending.remove(offense_ref)
                materialized = True
            if not materialized:
                break

    top_level_values = tuple(top_level)
    if len(top_level_values) != len(set(top_level_values)):
        raise EvaluationInstancePlannerError(f"{case_id}: duplicate binding instance")
    episode_by_binding_id = {
        value.binding_id: value.factual_episode_id for value in binding_values
    }
    sources_by_binding_id = {
        value.binding_id: value.source_binding_ids for value in derived_bindings
    }
    episode_by_binding_id.update(
        {value.binding_id: value.factual_episode_id for value in derived_bindings}
    )
    provenance_values = tuple(
        InstanceProvenance(
            instance,
            episode_by_binding_id[instance.occurrence_id],
            sources_by_binding_id.get(instance.occurrence_id, ()),
        )
        for instance in top_level_values
        if instance.occurrence_id in episode_by_binding_id
    )
    if len(provenance_values) != len(top_level_values):
        raise EvaluationInstancePlannerError(
            f"{case_id}: top-level instance without factual episode provenance"
        )
    selected_offenses = tuple(dict.fromkeys(value.offense_ref for value in top_level_values))
    compiled_by_ref: dict[str, CompiledOffense] = {}
    policies: dict[str, Any] = {}
    for ref in selected_offenses:
        compiled = compile_offense(registry, ref)
        if not isinstance(compiled, CompiledOffense):
            raise EvaluationInstancePlannerError(f"{case_id}: binding offense does not compile")
        compiled_by_ref[ref] = compiled
        policies[ref] = completion_mod.completion_policy_for(registry, ref)

    predicate_scopes = _component_scopes(top_level_values, compiled_by_ref, policies)
    assessment = tuple(dict.fromkeys((*top_level_values, *predicate_scopes)))
    target_values = tuple(
        (instance, ref)
        for instance in assessment
        for ref in _instance_predicate_refs(registry, instance)
    )
    selected_predicates = tuple(dict.fromkeys(ref for _, ref in target_values))
    neural_count = len(
        grounding_request_targets(
            registry,
            tuple(AssessmentTarget(instance, ref) for instance, ref in target_values),
        )
    )
    relation_targets = relation_assessment_targets(registry, assessment)
    article263_pairs: list[Article263OccurrencePair] = []
    injury_bindings = tuple(
        value for value in binding_values if value.offense_ref == "offense.injury"
    )
    for left, right in combinations(injury_bindings, 2):
        if (
            left.factual_episode_id != right.factual_episode_id
            or left.actor_id == right.actor_id
            or not (set(left.factual_targets) & set(right.factual_targets))
        ):
            continue
        episode = episode_by_id.get(left.factual_episode_id)
        if episode is None or not episode.source_fragments:
            continue
        start = min(value.source_start for value in episode.source_fragments)
        end = max(value.source_end for value in episode.source_fragments)
        relation_text = (
            case_text[start:end]
            if case_text is not None
            else "\n".join(value.source_quote for value in episode.source_fragments)
        )
        article263_pairs.append(
            Article263OccurrencePair(
                pair_id=f"article263-pair:{len(article263_pairs) + 1:04d}",
                left=OffenseInstanceKey(
                    case_id, left.actor_id, left.offense_ref, left.binding_id
                ),
                right=OffenseInstanceKey(
                    case_id, right.actor_id, right.offense_ref, right.binding_id
                ),
                relation_source_text=relation_text,
                relation_source_start=start,
                relation_source_end=end,
            )
        )
    # Call 1.5 factual_targets carry no legal role.  Until a later typed relation
    # stage interprets them, they cannot create indirect-principal or participant
    # outcome targets.  In particular, offline gold participants are not a
    # production fallback.
    utilization_targets: tuple[FactualUtilizationTarget, ...] = ()
    participant_outcomes: tuple[UtilizedParticipantOutcomeTarget, ...] = ()
    participant_predicates: tuple[UtilizedParticipantPredicateTarget, ...] = ()
    return OccurrenceAwareEvaluationInstancePlan(
        case_id=case_id,
        top10_seeds=selected_offenses,
        occurrences=tuple(evidence),
        candidate_offense_refs=tuple(dict.fromkeys(closure_candidates)),
        top_level_instances=top_level_values,
        predicate_scope_instances=predicate_scopes,
        assessment_instances=assessment,
        selected_predicate_refs=selected_predicates,
        assessment_targets=target_values,
        neural_predicate_request_target_count=neural_count,
        relation_assessment_targets=relation_targets,
        participation_local_targets=(),
        factual_utilization_targets=utilization_targets,
        utilized_participant_outcome_targets=participant_outcomes,
        utilized_participant_predicate_targets=participant_predicates,
        candidate_doctrine_refs=tuple(dict.fromkeys(doctrine_refs)),
        derived_binding_candidates=tuple(derived_bindings),
        unbound_seed_refs=tuple(dict.fromkeys(unbound_seed_refs)),
        article263_pair_candidates=tuple(article263_pairs),
        context_only_binding_ids=context_only_binding_ids,
        instance_provenance=provenance_values,
    )


__all__ = [
    "DerivedBindingCandidate",
    "InstanceProvenance",
    "EvaluationInstancePlannerError",
    "OccurrenceAwareEvaluationInstancePlan",
    "plan_binding_scoped_evaluation_instances",
    "plan_occurrence_aware_evaluation_instances",
    "selected_predicate_refs",
]
