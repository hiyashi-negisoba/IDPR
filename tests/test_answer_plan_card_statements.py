"""The P condition's card channel: what it may add, and what it may never touch.

ANSWERPLAN_SPEC 4-10 and 5.5.  The Call 2 card A/B was rejected because cards moved
truths; the whole argument for reusing them at Call 3 is that here they cannot.  These
tests are what makes that claim checkable rather than asserted.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import (
    AnswerPlanError,
    RuleStatement,
    build_answer_plan,
    check_contracts,
    serialize_analysis,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")

_CASE = "case"
_SATISFIED = "ground_fact.taking_conduct"
_FAILED = "legal_element.intent"
_BLOCKING = "legal_element.instigator_intent"
_CARD = RuleStatement(
    statement="재물의 타인성은 소유권의 귀속에 따라 판단한다.",
    origin="reviewed_card",
    source_id="card:art329:0007",
)


def _instance() -> dict:
    return {
        "case_id": _CASE,
        "actor_id": "甲",
        "offense_ref": "offense.theft",
        "occurrence_id": "binding:001",
    }


def _truth(predicate_ref: str, truth: str) -> dict:
    return {"instance_key": _instance(), "predicate_ref": predicate_ref, "truth": truth}


def _ref() -> str:
    from idpr.v2.runtime.answer_plan import instance_ref

    return instance_ref(_instance())


def _build(rule_statements=None):
    return build_answer_plan(
        case_id=_CASE,
        case_text="",
        question="",
        binding_row={},
        call2_row={
            "assessments": [],
            "case_truths": [
                _truth(_SATISFIED, "TRUE"),
                _truth(_FAILED, "FALSE"),
                _truth(_BLOCKING, "UNKNOWN"),
            ],
        },
        e2e_row={
            "sub_question_id": _CASE,
            "liability_results": [
                {"instance_key": _instance(), "result": {"elements": {"gate_state": "unresolved"}}}
            ],
            "final_responsibility": {},
        },
        registry=REGISTRY,
        offense_labels={"offense.theft": "절도죄"},
        rule_statements=rule_statements,
    )


def _findings_by_predicate(plan):
    issue = plan.anchored_issues[0]
    return {
        "satisfied": issue.satisfied,
        "failed": issue.failed,
        "blocking": issue.blocking,
    }


@pytest.mark.parametrize("predicate,bucket", [(_FAILED, "failed"), (_BLOCKING, "blocking")])
def test_cards_reach_findings_that_did_not_succeed(predicate: str, bucket: str) -> None:
    """A card must land on a failed or blocking finding, not only on a satisfied one.

    Saying why an element was not met is where the norm behind it carries the most weight,
    and an earlier revision attached cards to `satisfied` alone.
    """
    plan = _build({(_ref(), predicate): (_CARD,)})
    findings = _findings_by_predicate(plan)[bucket]
    assert [statement.source_id for finding in findings for statement in finding.rule_statements] == [
        _CARD.source_id
    ]


def test_a_card_reaches_only_the_predicate_it_was_retrieved_for() -> None:
    """The search unit is `(instance, predicate)` and so is the attachment.

    Keying on the instance would spray one element's norm across every element of the
    offence, which is exactly the distinction this channel exists to make.
    """
    plan = _build({(_ref(), _SATISFIED): (_CARD,)})
    findings = _findings_by_predicate(plan)
    assert [s.source_id for f in findings["satisfied"] for s in f.rule_statements] == [_CARD.source_id]
    assert not [s for f in findings["failed"] for s in f.rule_statements]
    assert not [s for f in findings["blocking"] for s in f.rule_statements]


def test_cards_change_nothing_but_the_rule_statements() -> None:
    """SPEC 4-10.  The P plan and the N plan differ in one field and no other.

    This is the contract that makes P-N a measurement of the card channel rather than of
    a second, quietly different pipeline.
    """
    without = _build()
    with_cards = _build(
        {
            (_ref(), _SATISFIED): (_CARD,),
            (_ref(), _FAILED): (_CARD,),
            (_ref(), _BLOCKING): (_CARD,),
        }
    )

    assert with_cards.required_final_conclusions == without.required_final_conclusions
    assert with_cards.discussion_order == without.discussion_order
    assert len(with_cards.anchored_issues) == len(without.anchored_issues)
    for p_issue, n_issue in zip(with_cards.anchored_issues, without.anchored_issues):
        assert p_issue.final_state == n_issue.final_state
        assert p_issue.gate_failed == n_issue.gate_failed
        for bucket in ("satisfied", "failed", "blocking"):
            p_findings = getattr(p_issue, bucket)
            n_findings = getattr(n_issue, bucket)
            assert [f.label for f in p_findings] == [f.label for f in n_findings]
            assert [f.truth for f in p_findings] == [f.truth for f in n_findings]
            # Stripping the added statements must recover the N finding exactly.
            assert [replace(f, rule_statements=()) for f in p_findings] == [
                replace(f, rule_statements=()) for f in n_findings
            ]


def test_a_statement_from_an_unknown_origin_is_refused() -> None:
    """Grounds whose provenance we cannot name are not grounds (SPEC 4-6/4-9)."""
    with pytest.raises(AnswerPlanError, match="rule statement from"):
        _build({(_ref(), _SATISFIED): (RuleStatement("x", "retrieved", "card:1"),)})


def test_a_statement_without_a_source_id_is_refused() -> None:
    with pytest.raises(AnswerPlanError, match="without source id"):
        RuleStatement(statement="x", origin="reviewed_card", source_id="")


def test_a_card_statement_survives_serialization_with_its_marker() -> None:
    """The writer must be able to tell a precedent-derived norm from an authored one."""
    plan = _build({(_ref(), _BLOCKING): (_CARD,)})
    payload = serialize_analysis(plan)
    assert f"[판례 법리] {_CARD.statement}" in payload
    assert _CARD.source_id not in payload


def test_check_contracts_rejects_a_bad_origin_on_any_bucket() -> None:
    plan = _build({(_ref(), _FAILED): (_CARD,)})
    issue = plan.anchored_issues[0]
    bad = replace(
        issue,
        blocking=tuple(
            replace(f, rule_statements=(RuleStatement("x", "rubric", "r1"),))
            for f in issue.blocking
        ),
    )
    with pytest.raises(AnswerPlanError, match="rule statement from"):
        check_contracts(replace(plan, anchored_issues=(bad,)))
