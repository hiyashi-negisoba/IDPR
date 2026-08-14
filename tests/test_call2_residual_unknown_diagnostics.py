from pathlib import Path

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.evaluation_instance_planner import _instance_predicate_refs
from idpr.v2.runtime.grounding import AssessmentTarget
from idpr.v2.runtime.identity import OffenseInstanceKey
from scripts.analyze_v2_call2_mixed_evidence import transition_counts
from scripts.analyze_v2_call2_overliteral_impact import changed_symbolic_cases
from scripts.analyze_v2_call2_residual_unknown import bucket
from scripts.analyze_v2_call2_target_placement import (
    placement_bucket,
    review_records_from_call2,
)
from scripts.analyze_v2_call2_uncertainty_factorial import _transition_counts
from scripts.analyze_v2_realization_link_impact import assessment_truths
from scripts.diagnose_v2_call2_evidence_scope import factual_episode_evidence
from scripts.diagnose_v2_call2_mixed_evidence import (
    actor_bound_ground_fact,
    mixed_carrier,
)
from scripts.diagnose_v2_call2_overliteral_policy import reviewed_targets


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


def test_target_placement_can_audit_every_scheduled_call2_target(tmp_path):
    path = tmp_path / "call2.jsonl"
    path.write_text(
        '{"sub_question_id":"case","assessments":['
        '{"instance_key":{"case_id":"case","actor_id":"A",'
        '"offense_ref":"offense.theft","occurrence_id":"binding:1"},'
        '"predicate_ref":"ground_fact.taking_conduct","truth":"UNKNOWN"}]}'
        "\n",
        encoding="utf-8",
    )
    assert review_records_from_call2(path) == [
        {
            "review_id": "ALL-001",
            "operational_bucket": "ALL_SCHEDULED",
            "instance_key": {
                "case_id": "case",
                "actor_id": "A",
                "offense_ref": "offense.theft",
                "occurrence_id": "binding:1",
            },
            "predicate_ref": "ground_fact.taking_conduct",
            "predicate_meaning": "",
            "truths": {"production": "UNKNOWN"},
        }
    ]


def test_realization_link_impact_reads_exact_assessment_keys(tmp_path):
    path = tmp_path / "call2.jsonl"
    path.write_text(
        '{"sub_question_id":"case","assessments":['
        '{"instance_key":{"case_id":"case","actor_id":"A",'
        '"offense_ref":"offense.robbery","occurrence_id":"binding:2"},'
        '"predicate_ref":"ground_fact.taking_conduct","truth":"TRUE"}]}'
        "\n",
        encoding="utf-8",
    )
    assert assessment_truths(path) == {
        (
            "case",
            "A",
            "offense.robbery",
            "binding:2",
            "ground_fact.taking_conduct",
        ): "TRUE"
    }


def test_overliteral_impact_separates_instance_and_final_view_changes():
    instance = {
        "case_id": "case",
        "actor_id": "A",
        "offense_ref": "offense.theft",
        "occurrence_id": "binding:1",
    }
    baseline = {
        "case": {
            "liability_results": [{"instance_key": instance, "result": {"state": "U"}}],
            "final_responsibility": {"final": []},
        }
    }
    counterfactual = {
        "case": {
            "liability_results": [{"instance_key": instance, "result": {"state": "T"}}],
            "final_responsibility": {"final": []},
        }
    }
    assert changed_symbolic_cases(baseline, counterfactual) == [
        {
            "case_id": "case",
            "changed_instance_count": 1,
            "final_responsibility_changed": False,
        }
    ]


def test_overliteral_policy_runner_loads_exact_reviewed_targets(tmp_path):
    path = tmp_path / "review.json"
    path.write_text(
        '{"records":[{"review_id":"RU-1","tier":"C_HIGH",'
        '"instance_key":{"case_id":"case","actor_id":"A",'
        '"offense_ref":"offense.theft","occurrence_id":"binding:1"},'
        '"predicate_ref":"legal_element.intent","counterfactual_truth":"TRUE"}]}'
        "\n",
        encoding="utf-8",
    )
    by_case, metadata = reviewed_targets(path)
    assert list(by_case) == ["case"]
    assert by_case["case"][0].predicate_ref == "legal_element.intent"
    assert next(iter(metadata.values()))["review_id"] == "RU-1"


def test_uncertainty_factorial_transition_counts_are_exact():
    keys = [("case", "A", "offense", "binding:1", "predicate")]
    assert _transition_counts({keys[0]: "UNKNOWN"}, {keys[0]: "TRUE"}, keys) == {
        "UNKNOWN->TRUE": 1
    }


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
