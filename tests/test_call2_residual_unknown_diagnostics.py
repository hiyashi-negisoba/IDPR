from pathlib import Path

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import _instance_predicate_refs
from idpr.v2.runtime.grounding import AssessmentTarget
from idpr.v2.runtime.identity import OffenseInstanceKey
from scripts.analyze_v2_call2_mixed_evidence import transition_counts
from scripts.analyze_v2_call2_residual_unknown import bucket
from scripts.analyze_v2_call2_target_placement import placement_bucket
from scripts.diagnose_v2_call2_evidence_scope import factual_episode_evidence
from scripts.diagnose_v2_call2_mixed_evidence import (
    actor_bound_ground_fact,
    mixed_carrier,
)


def test_residual_unknown_operational_buckets_are_conservative():
    assert (
        bucket(("UNKNOWN", "TRUE", "TRUE"))
        == "B_EPISODE_SCOPE_CONFIRMED"
    )
    assert (
        bucket(("UNKNOWN", "UNKNOWN", "FALSE"))
        == "A_OR_CASE_CONTEXT_REVIEW"
    )
    assert (
        bucket(("UNKNOWN", "UNKNOWN", "UNKNOWN"))
        == "C_OR_D_PERSISTENT_REVIEW"
    )
    assert bucket(("TRUE", "TRUE", "UNKNOWN")) == "UNSTABLE_OR_DRIFT"


def test_factual_episode_evidence_maps_direct_and_derived_bindings():
    issue = {
        "factual_episodes": [
            {
                "factual_episode_id": "episode:1",
                "source_fragments": [
                    {"source_span": {"start": 2, "end": 6}},
                    {"source_span": {"start": 5, "end": 9}},
                ],
            }
        ],
        "seed_results": [
            {
                "bindings": [
                    {
                        "binding_id": "binding:1",
                        "factual_episode_id": "episode:1",
                    }
                ]
            }
        ],
    }
    plan = {
        "derived_binding_candidates": [
            {
                "binding_id": "derived:1",
                "factual_episode_id": "episode:1",
            }
        ]
    }
    assert factual_episode_evidence(issue, plan, "0123456789") == {
        "binding:1": "2345678",
        "derived:1": "2345678",
    }


def test_target_placement_buckets_keep_role_review_separate_from_provenance():
    assert placement_bucket(
        predicate_kind="legal_element",
        actor_bound_ground_fact=False,
        derived=False,
        exact_actor_sources=0,
        other_actor_sources=0,
        exact_source_has_peer_actor=False,
        same_actor_other_episode=1,
        same_episode_peer_actors=1,
    ) == "LEGAL_ELEMENT_REALIZATION_SCOPE"
    assert placement_bucket(
        predicate_kind="ground_fact",
        actor_bound_ground_fact=True,
        derived=True,
        exact_actor_sources=1,
        other_actor_sources=2,
        exact_source_has_peer_actor=False,
        same_actor_other_episode=0,
        same_episode_peer_actors=0,
    ) == "DERIVED_EXACT_ACTOR_SOURCE"
    assert placement_bucket(
        predicate_kind="ground_fact",
        actor_bound_ground_fact=True,
        derived=False,
        exact_actor_sources=1,
        other_actor_sources=0,
        exact_source_has_peer_actor=False,
        same_actor_other_episode=1,
        same_episode_peer_actors=0,
    ) == "CROSS_EPISODE_SAME_ACTOR_CARRIER"
    assert placement_bucket(
        predicate_kind="ground_fact",
        actor_bound_ground_fact=True,
        derived=False,
        exact_actor_sources=1,
        other_actor_sources=0,
        exact_source_has_peer_actor=False,
        same_actor_other_episode=0,
        same_episode_peer_actors=2,
    ) == "PARTICIPATION_ROLE_REVIEW"
    assert placement_bucket(
        predicate_kind="ground_fact",
        actor_bound_ground_fact=False,
        derived=False,
        exact_actor_sources=1,
        other_actor_sources=0,
        exact_source_has_peer_actor=False,
        same_actor_other_episode=1,
        same_episode_peer_actors=1,
    ) == "GROUND_FACT_REALIZATION_SCOPE"
    assert placement_bucket(
        predicate_kind="ground_fact",
        actor_bound_ground_fact=True,
        derived=True,
        exact_actor_sources=1,
        other_actor_sources=0,
        exact_source_has_peer_actor=True,
        same_actor_other_episode=0,
        same_episode_peer_actors=0,
    ) == "DERIVED_SOURCE_PARTICIPATION_REVIEW"


def test_mixed_carrier_keeps_actor_ground_fact_local_and_expands_legal_element():
    registry = load_definitions(Path("data/v2/definitions"))
    instance = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")
    occurrences = {
        "binding:001": GoldOccurrence("binding:001", "甲", "local", 0, 5)
    }
    common = {
        "registry": registry,
        "plan": {},
        "issue": {"seed_results": []},
        "occurrences": occurrences,
        "episode_evidence": {"binding:001": "whole episode"},
    }
    assert actor_bound_ground_fact(registry, "ground_fact.taking_conduct")
    assert not actor_bound_ground_fact(registry, "ground_fact.means_or_object_defect")
    carrier, evidence = mixed_carrier(
        target=AssessmentTarget(instance, "ground_fact.taking_conduct"), **common
    )
    assert (carrier, evidence.source_text) == ("actor_action_binding", "local")
    carrier, evidence = mixed_carrier(
        target=AssessmentTarget(instance, "legal_element.possession"), **common
    )
    assert (carrier, evidence.source_text) == ("factual_episode", "whole episode")


def test_mixed_evidence_transition_counts_require_exact_paired_keys():
    key = ("case", "甲", "offense.theft", "binding:001", "predicate")
    assert transition_counts({key: "UNKNOWN"}, {key: "TRUE"}) == {
        ("UNKNOWN", "TRUE"): 1
    }


def test_bribe_giver_is_asked_delivery_not_recipient_acceptance():
    registry = load_definitions(Path("data/v2/definitions"))
    refs = _instance_predicate_refs(
        registry,
        OffenseInstanceKey("case", "甲", "offense.bribe_giving", "binding:001"),
    )
    assert "ground_fact.bribe_delivery" in refs
    assert "ground_fact.bribe_acceptance" not in refs
