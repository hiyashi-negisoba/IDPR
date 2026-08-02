"""Call 1.5 contracts: the catalog is closed, and the host mints the identifiers."""

from __future__ import annotations

import json

import pytest

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.article_select import (
    MAX_SELECTED,
    NON_SUBSTANTIVE_DOMAIN,
    NO_SUBSTANTIVE_OFFENSE,
    SUBSTANTIVE_DOMAIN,
    ArticleSelectError,
    article_select_schema,
    attempt_article_map,
    catalog_keys,
    catalog_lines,
    expand_attempt_articles,
    load_catalog,
    selectable_catalog,
    selection_payload,
    validate_selection,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.doctrine import OFFENSE_NAMES


def test_catalog_covers_every_article_the_corpus_carries():
    """An article missing from the catalog is one the pipeline can never select."""
    corpus_articles = {card.article for card in card_corpus().cards}
    assert corpus_articles <= set(catalog_keys())


def test_catalog_is_the_source_of_the_offence_names():
    """The names moved out of the code; both readers must see one table."""
    assert OFFENSE_NAMES == {e["key"]: e["offense"] for e in load_catalog()}


def test_catalog_line_leads_with_the_key_the_model_must_emit():
    line = catalog_lines()[0]
    key = catalog_keys()[0]
    assert line.startswith(f"{key} ")
    assert "제" in line


def test_catalog_lines_do_not_eagerly_load_the_rule_hierarchy():
    lines = catalog_lines()
    robbery_injury = next(line for line in lines if line.startswith("art337 "))
    assert robbery_injury == "art337 제337조 강도상해·치상"


def test_schema_closes_the_article_set():
    """Guided decoding, not a post-hoc check, is what stops an invented article number."""
    schema = article_select_schema()
    enum = schema["properties"]["selected"]["items"]["properties"]["article"]["enum"]
    assert set(enum) == {
        *catalog_keys(selectable_catalog()),
        NO_SUBSTANTIVE_OFFENSE,
    }
    assert schema["properties"]["selected"]["minItems"] == 0
    assert schema["properties"]["selected"]["maxItems"] == MAX_SELECTED
    assert schema["properties"]["question_domain"]["enum"] == [
        SUBSTANTIVE_DOMAIN,
        NON_SUBSTANTIVE_DOMAIN,
    ]
    decisions = article_select_schema(retrieval_hints=["art297", "art298", "art301"])["properties"][
        "candidate_decisions"
    ]
    assert decisions["minItems"] == decisions["maxItems"] == 3
    selected_enum = article_select_schema(retrieval_hints=["art298"])["properties"][
        "selected"
    ]["items"]["properties"]["article"]["enum"]
    assert "art298" not in selected_enum


def test_payload_carries_only_whitelisted_case_fields():
    payload = selection_payload(
        case_id="c1", question_text="甲은 …", question_prompt="죄책을 논하라."
    )
    assert_no_leaked_fields(payload)
    assert set(payload) == {
        "case_id",
        "case_text",
        "question_prompt",
        "issue_hints",
        "retrieval_hints",
        "article_catalog",
    }


def test_payload_carries_only_grounded_call1_issue_hints():
    payload = selection_payload(
        case_id="c1",
        question_text="甲은 …",
        question_prompt="죄책을 논하라.",
        issue_hints=[
            {"label": "강간미수", "source_quote": "간음하려 하였으나 단념하였다."},
            {"label": "", "source_quote": "버린다."},
        ],
        retrieval_hints=["art297", "art301", "art297"],
    )

    assert payload["issue_hints"] == [
        {"label": "강간미수", "source_quote": "간음하려 하였으나 단념하였다."}
    ]
    assert payload["retrieval_hints"] == [
        "art297 제297조 강간",
        "art301 제301조 강간등 상해·치상",
    ]


def test_payload_never_carries_card_provenance():
    """Plan verification #4: only the reviewed proposition may reach a model.

    Here not even that -- selection sees article names, never card text -- so quotes and
    comment ids must be absent from the serialised request.
    """
    payload = selection_payload(
        case_id="c1", question_text="甲은 …", question_prompt="죄책을 논하라."
    )
    blob = json.dumps(payload, ensure_ascii=False)
    for forbidden in ("source_refs", "comment_id", "quote", "proposition"):
        assert forbidden not in blob


def test_selection_rejects_an_article_outside_the_catalog():
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [{"article": "art999", "reason": "x"}],
            }
        )


def test_selection_requires_a_reason():
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [{"article": "art298", "reason": "  "}],
            }
        )


def test_selection_keeps_the_first_reason_for_a_repeated_article():
    articles, entries = validate_selection(
        {
            "question_domain": SUBSTANTIVE_DOMAIN,
            "candidate_decisions": [],
            "selected": [
                {"article": "art298", "reason": "첫 근거"},
                {"article": "art298", "reason": "둘째 근거"},
            ]
        }
    )
    assert articles == ("art298",)
    assert entries[0]["reason"] == "첫 근거"


def test_no_offence_sentinel_maps_to_an_empty_selection():
    articles, entries = validate_selection(
        {
            "question_domain": NON_SUBSTANTIVE_DOMAIN,
            "candidate_decisions": [],
            "selected": [
                {
                    "article": NO_SUBSTANTIVE_OFFENSE,
                    "reason": "설문은 증거능력만 묻는다.",
                }
            ]
        }
    )
    assert articles == ()
    assert entries == ()


def test_empty_selection_and_mixed_sentinel_are_contract_violations():
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [],
            }
        )
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": NON_SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [
                    {"article": NO_SUBSTANTIVE_OFFENSE, "reason": "없음"},
                    {"article": "art298", "reason": "추행"},
                ]
            }
        )


def test_question_domain_must_agree_with_the_selection_kind():
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [
                    {"article": NO_SUBSTANTIVE_OFFENSE, "reason": "없음"}
                ],
            }
        )
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": NON_SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [{"article": "art298", "reason": "추행"}],
            }
        )


def test_attempt_expansion_follows_the_statute_reference():
    """제254조 punishes the attempt of 제250조; selecting the base pulls it in."""
    mapping = attempt_article_map()
    assert mapping["art250"] == "art254"
    assert mapping["art329"] == "art342"
    assert expand_attempt_articles(["art250"], mapping=mapping) == ("art250", "art254")


def test_attempt_articles_are_host_derived_not_model_selectable():
    mapping = attempt_article_map()
    selectable = set(catalog_keys(selectable_catalog(attempt_mapping=mapping)))
    assert not (set(mapping.values()) & selectable)
    schema = article_select_schema()
    enum = schema["properties"]["selected"]["items"]["properties"]["article"]["enum"]
    assert not (set(mapping.values()) & set(enum))
    with pytest.raises(ArticleSelectError):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [],
                "selected": [{"article": "art300", "reason": "미수"}],
            }
        )


def test_retrieval_candidates_are_reviewed_positionally_and_merged():
    articles, entries = validate_selection(
        {
            "question_domain": SUBSTANTIVE_DOMAIN,
            "candidate_decisions": [
                {"relevant": True, "reason": "폭행으로 추행하였다."},
                {"relevant": False, "reason": "재물 취득 사실이 없다."},
            ],
            "selected": [{"article": "art319", "reason": "주거에 침입하였다."}],
        },
        retrieval_hints=["art298", "art333"],
    )

    assert articles == ("art319", "art298")
    assert entries[-1] == {"article": "art298", "reason": "폭행으로 추행하였다."}


def test_retrieval_review_count_and_non_substantive_acceptance_are_structural():
    with pytest.raises(ArticleSelectError, match="exactly 2"):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [
                    {"relevant": True, "reason": "추행 사실"}
                ],
                "selected": [],
            },
            retrieval_hints=["art298", "art319"],
        )

    with pytest.raises(ArticleSelectError, match="decided positionally"):
        validate_selection(
            {
                "question_domain": SUBSTANTIVE_DOMAIN,
                "candidate_decisions": [
                    {"relevant": True, "reason": "추행 사실"}
                ],
                "selected": [{"article": "art298", "reason": "중복 보충"}],
            },
            retrieval_hints=["art298"],
        )

    articles, entries = validate_selection(
        {
            "question_domain": NON_SUBSTANTIVE_DOMAIN,
            "candidate_decisions": [{"relevant": True, "reason": "배경 범행"}],
            "selected": [
                {"article": NO_SUBSTANTIVE_OFFENSE, "reason": "증거 문제"}
            ],
        },
        retrieval_hints=["art298"],
    )
    assert articles == entries == ()


def test_attempt_expansion_preserves_order_and_is_idempotent():
    mapping = attempt_article_map()
    once = expand_attempt_articles(["art319", "art297"], mapping=mapping)
    assert once == ("art319", "art297", "art300")
    assert expand_attempt_articles(once, mapping=mapping) == once


def test_attempt_expansion_only_names_articles_the_corpus_covers():
    """An expansion target with no cards would add a candidate that carries nothing."""
    corpus_articles = {card.article for card in card_corpus().cards}
    assert set(attempt_article_map().values()) <= corpus_articles
