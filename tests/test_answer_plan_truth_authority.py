from __future__ import annotations

from pathlib import Path

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import build_answer_plan

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")

_CASE = "case"
_GROUND_FACT = "ground_fact.taking_conduct"
_MERGED_ONLY = "legal_element.instigator_intent"


def _instance(offense: str = "offense.theft", occurrence: str = "binding:001") -> dict:
    return {
        "case_id": _CASE,
        "actor_id": "甲",
        "offense_ref": offense,
        "occurrence_id": occurrence,
    }


def _truth(predicate_ref: str, truth: str, **instance_overrides) -> dict:
    return {
        "instance_key": _instance(**instance_overrides),
        "predicate_ref": predicate_ref,
        "truth": truth,
    }


def _e2e_row() -> dict:
    return {
        "sub_question_id": _CASE,
        "liability_results": [
            {
                "instance_key": _instance(),
                "result": {"elements": {"gate_state": "unresolved"}},
            }
        ],
        "final_responsibility": {},
    }


def _build(call2_row: dict):
    return build_answer_plan(
        case_id=_CASE,
        case_text="",
        question="",
        binding_row={},
        call2_row=call2_row,
        e2e_row=_e2e_row(),
        registry=REGISTRY,
        offense_labels={"offense.theft": "절도죄"},
    )


def test_truths_present_only_in_case_truths_reach_the_plan() -> None:
    """The merged participation and doctrine truths land only in case_truths.

    Projecting from `assessments` dropped them, which meant the plan asserted conclusions
    while withholding the grounds the symbolic layer actually used for them.
    """
    plan = _build(
        {
            "assessments": [_truth(_GROUND_FACT, "TRUE")],
            "case_truths": [
                _truth(_GROUND_FACT, "TRUE"),
                _truth(_MERGED_ONLY, "TRUE"),
            ],
        }
    )
    issue = plan.anchored_issues[0]
    labels = {finding.label for finding in issue.satisfied}
    assert len(labels) == 2, labels


def test_case_truths_do_not_widen_the_issue_universe() -> None:
    """A truth about an instance the run reached no conclusion for creates no issue.

    Issue selection stays owned by the run's liability results; changing the truth
    authority must not turn every extra truth into something the answer has to discuss.
    """
    plan = _build(
        {
            "assessments": [],
            "case_truths": [
                _truth(_GROUND_FACT, "TRUE"),
                _truth(_GROUND_FACT, "TRUE", offense="offense.robbery", occurrence="binding:009"),
            ],
        }
    )
    assert len(plan.anchored_issues) == 1
    assert plan.anchored_issues[0].offense_label == "절도죄"
    assert len(plan.required_final_conclusions) == 1


def test_a_ground_fact_conflict_between_the_two_carriers_is_refused() -> None:
    """The carriers feed different downstream stages, so they may not disagree."""
    import pytest

    from idpr.v2.runtime.answer_plan import AnswerPlanError

    with pytest.raises(AnswerPlanError, match="CROSS_INSTANCE_GROUND_FACT_CONFLICT"):
        build_answer_plan(
            case_id=_CASE,
            case_text="",
            question="",
            binding_row={},
            call2_row={
                "assessments": [_truth(_GROUND_FACT, "FALSE")],
                "case_truths": [_truth(_GROUND_FACT, "TRUE")],
            },
            e2e_row=_e2e_row(),
            registry=REGISTRY,
            offense_labels={"offense.theft": "절도죄"},
            plan_row={
                "instance_provenance": [
                    {"instance_key": _instance(), "factual_episode_id": "factual_episode:001"}
                ]
            },
        )
