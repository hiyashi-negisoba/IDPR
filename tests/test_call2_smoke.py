"""The smoke runner consumes Phase 2 artifacts without weakening their invariants."""

from __future__ import annotations

from idpr.neural.card_assessment import assessment_request, card_assessment_schema
from idpr.neural.fact_graph import assessment_facts
from idpr.prompts import load_prompt
from scripts.run_call2_smoke import (
    DEFAULT_CASE_ID,
    DEFAULT_OUTPUT_OVERHEAD,
    DEFAULT_TOKENS_PER_CARD,
    prepare_case,
    select_article_batches,
)


def test_smoke_plan_is_two_article_whole_batches():
    case, graph, batches = prepare_case(case_id=DEFAULT_CASE_ID)
    assert len(batches) == 2
    card_ids = [card_id for batch in batches for card_id in batch.card_ids]
    assert len(card_ids) == len(set(card_ids)) == 749
    article_to_batch = {
        article: index
        for index, batch in enumerate(batches)
        for article in batch.articles
    }
    assert len(article_to_batch) == 22
    assert all(
        article_to_batch[card.article] == index
        for index, batch in enumerate(batches)
        for card in batch.cards
    )
    assert [
        DEFAULT_OUTPUT_OVERHEAD + DEFAULT_TOKENS_PER_CARD * len(batch.cards)
        for batch in batches
    ] == [30_464, 31_504]

    facts = assessment_facts(graph)
    request = assessment_request(
        case=case, fact_graph=graph, cards=batches[0].model_payload()
    )
    assert all(set(card) == {"id", "proposition"} for card in request["cards"])
    card_assessment_schema(
        case_id=DEFAULT_CASE_ID,
        card_ids=batches[0].card_ids,
        fact_ids=[fact["fact_id"] for fact in facts],
    )


def test_approved_prompt_contains_no_removed_card_provenance_or_outputs():
    prompt = load_prompt("card_assess") + load_prompt("card_assess_user")
    for forbidden in (
        "source_refs",
        "comment_id",
        "authority_comment_ids",
        "rationale",
        "confidence",
    ):
        assert forbidden not in prompt


def test_prompt_treats_cards_as_norms_and_missing_items_as_case_facts_only():
    prompt = load_prompt("card_assess") + load_prompt("card_assess_user")
    for required in (
        "검수 완료된 법규범",
        "사실적 적용조건",
        "구체적 사건 사실",
        "상해죄 성립 여부",
    ):
        assert required in prompt


def test_article_ab_batches_keep_each_requested_article_complete():
    _, _, original = prepare_case(case_id=DEFAULT_CASE_ID)
    batches = select_article_batches(
        original, ("art298", "art297", "art301", "art319")
    )
    assert [batch.articles for batch in batches] == [
        ("art298",),
        ("art297",),
        ("art301",),
        ("art319",),
    ]
    assert [len(batch.cards) for batch in batches] == [28, 50, 23, 92]
    assert all(
        card.article == batch.articles[0]
        for batch in batches
        for card in batch.cards
    )
    assert len({card.id for batch in batches for card in batch.cards}) == 193
