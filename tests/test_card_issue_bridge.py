from pathlib import Path

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

DEFINITIONS = Path("data/v2/definitions")


def test_derived_occurrence_quotes_follow_only_authored_source_bindings() -> None:
    binding_row = {
        "seed_results": [
            {
                "bindings": [
                    {
                        "binding_id": "binding:001",
                        "actor_action_fragments": [{"source_quote": "甲이 돈을 받았다."}],
                        "context_fragments": [{"source_quote": "乙이 속아서 교부했다."}],
                    },
                    {
                        "binding_id": "binding:999",
                        "actor_action_fragments": [{"source_quote": "무관한 행위"}],
                        "context_fragments": [],
                    },
                ]
            }
        ]
    }
    plan_row = {
        "derived_binding_candidates": [
            {
                "binding_id": "derived_binding:001",
                "source_binding_ids": ["binding:001"],
            }
        ]
    }
    assert _episode_quotes(binding_row, "derived_binding:001", plan_row) == (
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


def test_criminal_act_article_key_preserves_subarticle_shape() -> None:
    assert criminal_act_article_key("형법 제329조") == "art329"
    assert criminal_act_article_key("형법 제258조의2 제1항") == "art2582_2"
    assert criminal_act_article_key("특정범죄 가중처벌 등에 관한 법률 제5조") is None


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
