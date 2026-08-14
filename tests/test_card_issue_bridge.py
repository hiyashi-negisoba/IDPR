from pathlib import Path

import pytest

from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import _episode_quotes
from idpr.v2.runtime.card_issue_bridge import (
    EXACT_AUTHORED_IDENTITY,
    UNMAPPED_DERIVED_ARTICLE,
    criminal_act_article_key,
    plan_instance_issue_candidates,
    project_offense_articles,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from scripts.audit_v2_card_issue_join import (
    _action_quotes,
    _provenance_by_instance,
    _quotes_for_instance,
)
from scripts.build_v2_card_rule_statements import targets_for_case

DEFINITIONS = Path("data/v2/definitions")


def test_derived_realization_quotes_follow_only_authored_source_actions() -> None:
    binding_row = {
        "factual_episodes": [
            {
                "factual_episode_id": "factual_episode:001",
                "factual_actions": [
                    {
                        "factual_action_id": "factual_action:001:001",
                        "source_fragments": [
                            {
                                "source_quote": "甲이 돈을 받았다.",
                                "source_start": 0,
                                "source_end": 10,
                            }
                        ],
                    },
                    {
                        "factual_action_id": "factual_action:001:002",
                        "source_fragments": [
                            {
                                "source_quote": "乙이 속아서 교부했다.",
                                "source_start": 11,
                                "source_end": 22,
                            }
                        ],
                    },
                    {
                        "factual_action_id": "factual_action:001:003",
                        "source_fragments": [
                            {
                                "source_quote": "무관한 행위",
                                "source_start": 23,
                                "source_end": 29,
                            }
                        ],
                    },
                ],
            }
        ],
        "seed_results": [
            {
                "bindings": [
                    {
                        "binding_id": "binding:001",
                        "focal_action_id": "factual_action:001:001",
                        "supporting_action_ids": ["factual_action:001:002"],
                    },
                    {
                        "binding_id": "binding:999",
                        "focal_action_id": "factual_action:001:003",
                        "supporting_action_ids": [],
                    },
                ]
            }
        ]
    }
    plan_row = {
        "instance_provenance": [
            {
                "instance_key": {
                    "case_id": "case",
                    "actor_id": "甲",
                    "offense_ref": "derived_offense.fraud",
                    "occurrence_id": "realization:derived:001",
                },
                "source_binding_ids": ["binding:001"],
                "focal_action_id": None,
                "supporting_action_ids": [
                    "factual_action:001:001",
                    "factual_action:001:002",
                ],
            }
        ]
    }
    assert _episode_quotes(binding_row, "realization:derived:001", plan_row) == (
        "甲이 돈을 받았다.",
        "乙이 속아서 교부했다.",
    )


def test_participation_occurrence_quotes_use_planner_authored_span() -> None:
    plan_row = {
        "occurrences": [
            {
                "occurrence_id": "participation_binding:001",
                "actor_id": "甲",
                "source_text": "甲이 乙에게 범행을 부탁하였다.",
            }
        ]
    }
    assert _episode_quotes({}, "participation_binding:001", plan_row) == (
        "甲이 乙에게 범행을 부탁하였다.",
    )


def test_card_audit_keeps_receipt_and_later_use_as_separate_query_evidence() -> None:
    action_quotes = _action_quotes(
        [
            {
                "sub_question_id": "case",
                "factual_episodes": [
                    {
                        "factual_actions": [
                            {
                                "factual_action_id": "factual_action:001:001",
                                "source_fragments": [
                                    {
                                        "source_quote": "甲이 돈을 받았다.",
                                        "source_start": 0,
                                        "source_end": 10,
                                    }
                                ],
                            },
                            {
                                "factual_action_id": "factual_action:001:002",
                                "source_fragments": [
                                    {
                                        "source_quote": "甲이 나중에 그 돈을 썼다.",
                                        "source_start": 11,
                                        "source_end": 25,
                                    }
                                ],
                            },
                        ]
                    }
                ],
            }
        ]
    )
    instance = OffenseInstanceKey("case", "甲", "offense.embezzlement", "realization:001")
    quote = _quotes_for_instance(
        instance=instance,
        provenance={
            "focal_action_id": "factual_action:001:001",
            "supporting_action_ids": [],
        },
        action_quotes=action_quotes,
        occurrence_quotes={"realization:001": ("두 행동을 합친 episode",)},
    )
    assert quote == ("甲이 돈을 받았다.",)


def test_card_audit_rejects_binding_as_occurrence_identity() -> None:
    with pytest.raises(ValueError, match="occurrence must equal legal realization identity"):
        _provenance_by_instance(
            [
                {
                    "sub_question_id": "case",
                    "instance_provenance": [
                        {
                            "instance_key": {
                                "case_id": "case",
                                "actor_id": "甲",
                                "offense_ref": "offense.theft",
                                "occurrence_id": "binding:001",
                            },
                            "realization_id": "realization:001",
                        }
                    ],
                }
            ]
        )


def test_card_retrieval_refuses_a_realization_without_action_provenance() -> None:
    instance = {
        "case_id": "case",
        "actor_id": "甲",
        "offense_ref": "offense.theft",
        "occurrence_id": "realization:001",
    }
    with pytest.raises(ValueError, match="lacks planner action provenance"):
        targets_for_case(
            None,
            {"liability_results": [{"instance_key": instance}]},
            {"case_truths": []},
            {"factual_episodes": []},
            {"instance_provenance": []},
        )


def test_criminal_act_article_key_preserves_subarticle_shape() -> None:
    assert criminal_act_article_key("형법 제329조") == "art329"
    assert criminal_act_article_key("형법 제258조의2 제1항") == "art2582_2"
    assert criminal_act_article_key("특정범죄 가중처벌 등에 관한 법률 제5조") is None


def test_live_card_preserves_reviewed_variant_group_for_dispute_routing() -> None:
    card = card_corpus().by_id["art329_sec2_2.dead_person_possession_continuing"]
    assert card.variant_group == "art329_sec2_2.dead_person_possession"


def test_projection_uses_only_authored_identity_for_derived_offense() -> None:
    registry = load_definitions(DEFINITIONS)
    direct = project_offense_articles(registry, "offense.theft")
    derived = project_offense_articles(registry, "derived_offense.fraud")
    unmapped = project_offense_articles(registry, "derived_offense.aggravated_injury")

    assert direct.status == EXACT_AUTHORED_IDENTITY
    assert direct.article_keys == ("art329",)
    assert derived.status == EXACT_AUTHORED_IDENTITY
    assert derived.article_keys == ("art347",)
    assert unmapped.status == UNMAPPED_DERIVED_ARTICLE
    assert unmapped.article_keys == ()


def test_instance_plan_stays_inside_authored_article() -> None:
    registry = load_definitions(DEFINITIONS)
    corpus = card_corpus()
    issues = compile_issue_catalog_v2(corpus)[0]
    instance = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")

    plan = plan_instance_issue_candidates(
        registry,
        instance,
        episode_quotes=("야간에 타인의 주거에 들어가 재물을 가지고 나왔다.",),
        corpus=corpus,
        issues=issues,
        top_k_issues=2,
    )

    assert len(plan.candidates) == 2
    assert all(candidate.article == "art329" for candidate in plan.candidates)


def test_authored_derived_instance_opens_its_exact_article_candidates() -> None:
    registry = load_definitions(DEFINITIONS)
    instance = OffenseInstanceKey(
        "case", "甲", "derived_offense.fraud", "binding:001"
    )
    plan = plan_instance_issue_candidates(
        registry,
        instance,
        episode_quotes=("상대방을 속여 돈을 받았다.",),
    )
    assert plan.projection.status == EXACT_AUTHORED_IDENTITY
    assert plan.projection.article_keys == ("art347",)
    assert plan.candidates
    assert all(value.article == "art347" for value in plan.candidates)
