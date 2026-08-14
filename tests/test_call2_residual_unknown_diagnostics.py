from scripts.analyze_v2_call2_residual_unknown import bucket
from scripts.diagnose_v2_call2_evidence_scope import factual_episode_evidence


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
