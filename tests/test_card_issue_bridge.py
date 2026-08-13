from pathlib import Path

from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.card_issue_bridge import (
    EXACT_AUTHORED_IDENTITY,
    UNMAPPED_DERIVED_ARTICLE,
    criminal_act_article_key,
    plan_instance_issue_candidates,
    project_offense_articles,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

DEFINITIONS = Path("data/v2/definitions")


def test_criminal_act_article_key_preserves_subarticle_shape() -> None:
    assert criminal_act_article_key("형법 제329조") == "art329"
    assert criminal_act_article_key("형법 제258조의2 제1항") == "art2582_2"
    assert criminal_act_article_key("특정범죄 가중처벌 등에 관한 법률 제5조") is None


def test_projection_never_guesses_derived_article_from_base() -> None:
    registry = load_definitions(DEFINITIONS)
    direct = project_offense_articles(registry, "offense.theft")
    derived = project_offense_articles(registry, "derived_offense.special_theft")

    assert direct.status == EXACT_AUTHORED_IDENTITY
    assert direct.article_keys == ("art329",)
    assert derived.status == UNMAPPED_DERIVED_ARTICLE
    assert derived.article_keys == ()


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


def test_unmapped_derived_instance_opens_no_card_candidates() -> None:
    registry = load_definitions(DEFINITIONS)
    instance = OffenseInstanceKey(
        "case", "甲", "derived_offense.fraud", "binding:001"
    )
    plan = plan_instance_issue_candidates(
        registry,
        instance,
        episode_quotes=("상대방을 속여 돈을 받았다.",),
    )
    assert plan.projection.status == UNMAPPED_DERIVED_ARTICLE
    assert plan.candidates == ()
