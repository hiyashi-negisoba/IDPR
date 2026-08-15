"""AnswerPlan → Call 3 전달 감사의 종료 증명.

축이 아니라 전달이다. 여기서 보는 것은 하나 -- **AnswerPlan이 아는 것만 정확한 단위로
넘기는가.** 모르는 것을 안다고 말하지 않고, 아는 것을 다른 쟁점으로 흘리지 않고, 결론을
막고 있지 않은 것을 쟁점으로 부풀리지 않는다.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import (
    UNRESOLVED,
    AnchoredIssue,
    AnswerPlan,
    Finding,
    FinalResponsibility,
    issue_authorities,
    live_unresolved_frontier,
    serialize_open_points,
    serialize_required_authorities,
)
from idpr.v2.runtime.concurrence import (
    IMAGINATIVE_CONCURRENCE_CANDIDATE,
    REAL_CONCURRENCE_CANDIDATE,
    classify_concurrence_relations,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _issue(**overrides) -> AnchoredIssue:
    base = dict(
        issue_id="i1",
        actor="甲",
        offense_label="살인죄",
        governing_provision="형법 제250조 제1항",
        episode_quotes=(),
        final_state=UNRESOLVED,
        completion_state=None,
        completion_why=None,
        participation=None,
        decisive_stage=None,
        satisfied=(),
        failed=(),
        blocking=(),
        doctrines=(),
        contested_points=(),
    )
    base.update(overrides)
    return AnchoredIssue(**base)


def _plan(issues) -> AnswerPlan:
    return AnswerPlan(
        case_id="case",
        case_text="",
        question="",
        discussion_order=tuple(i.issue_id for i in issues),
        anchored_issues=tuple(issues),
        final_responsibility=FinalResponsibility((), (), (), (), ()),
    )


# --------------------------------------------------------------------------
# A. 모르는 것을 안다고 말하지 않는다
# --------------------------------------------------------------------------


def test_empty_open_points_is_empty_not_a_completeness_claim() -> None:
    """"다루지 않은 영역으로 특정된 것은 없다"는 host가 할 수 없는 말이다.

    26문항 전부가 그 문장을 달고 나갔고, 그 중에는 Call 1이 죄명 자체를 잡지 못해 주거침입죄가
    통째로 빠진 문항도 있었다. 미포착은 부존재가 아니다.
    """
    assert serialize_open_points(_plan((_issue(),))) == ""


def test_known_gaps_are_still_reported() -> None:
    """아는 공백은 그대로 말한다. 침묵과 완결성 선언은 다르다."""
    plan = replace(
        _plan((_issue(),)),
        representation_gaps=("구성요건적 착오는 아직 사실로 결박되지 않는다.",),
    )
    assert "구성요건적 착오" in serialize_open_points(plan)


# --------------------------------------------------------------------------
# C. 아는 것을 다른 쟁점으로 흘리지 않는다
# --------------------------------------------------------------------------


def test_generic_element_authority_does_not_spread_to_the_offence() -> None:
    """죄를 가리지 않는 요소의 조문이 그 죄의 필수 인용이 되지 않는다.

    `result_causation`이 살인·과실치사 조문을 함께 달고 있어서, 그 요소를 쓰는 모든 죄가
    과실치사 조문을 인용하도록 강제되고 있었다.
    """
    issue = _issue(
        blocking=(
            Finding(
                label="인과관계",
                truth="UNKNOWN",
                predicate_ref="legal_element.result_causation",
                governing_provision="형법 제267조; 제268조",
            ),
        )
    )
    statutory, doctrinal = issue_authorities(issue)
    assert statutory == ("형법 제250조 제1항",)
    assert "형법 제267조" in doctrinal and "형법 제268조" in doctrinal
    # 강제되는 줄은 `· `로 시작하는 것뿐이다.
    forced = [
        line for line in serialize_required_authorities(_plan((issue,))).splitlines()
        if line.startswith("·")
    ]
    assert forced == ["· 형법 제250조 제1항"]


def test_bare_article_numbers_inherit_their_statute_name() -> None:
    """`제337조`가 그대로 나가면 답안에 벌거벗은 조문번호가 적힌다."""
    issue = _issue(governing_provision="형법 제333조; 제337조")
    statutory, _ = issue_authorities(issue)
    assert statutory == ("형법 제333조", "형법 제337조")


def test_an_article_and_its_paragraph_are_not_both_required() -> None:
    issue = _issue(governing_provision="형법 제319조; 형법 제319조 제1항")
    statutory, _ = issue_authorities(issue)
    assert statutory == ("형법 제319조 제1항",)


# --------------------------------------------------------------------------
# B. 죄수관계는 산출된 것만 말한다
# --------------------------------------------------------------------------


def _instance(ref: str, occurrence: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", "甲", ref, occurrence)


def test_realization_identity_opens_candidates_not_conclusions() -> None:
    """초점행위 동일성은 후보를 여는 근거지 죄수관계의 확정이 아니다.

    형법 제40조의 "한 개의 행위"는 사회관념상 하나의 행위로 평가되는지를 묻는 규범적
    판단이고, 초점행위가 다르다는 구조적 사실이 곧 제37조 전단의 경합범은 아니다.
    """
    left = _instance("offense.homicide", "r1")
    right = _instance("offense.arson_of_occupied_structure", "r2")
    far = _instance("offense.dwelling_intrusion", "r3")
    relations = classify_concurrence_relations(
        (left, right, far),
        realization_by_instance={
            left: "factual_action:001:003",
            right: "factual_action:001:003",
            far: "factual_action:001:001",
        },
    )
    by_pair = {frozenset((a, b)): kind for a, b, kind in relations}
    assert by_pair[frozenset((left, right))] == IMAGINATIVE_CONCURRENCE_CANDIDATE
    assert by_pair[frozenset((left, far))] == REAL_CONCURRENCE_CANDIDATE


def test_an_unknown_realization_produces_no_relation_at_all() -> None:
    """실현을 모르는 instance는 짝을 만들지 않는다. 모르면 말하지 않는다."""
    left = _instance("offense.homicide", "r1")
    right = _instance("offense.dwelling_intrusion", "r2")
    assert (
        classify_concurrence_relations(
            (left, right), realization_by_instance={left: "factual_action:001:003"}
        )
        == ()
    )


def test_relations_never_cross_actors() -> None:
    left = _instance("offense.homicide", "r1")
    other = OffenseInstanceKey("case", "乙", "offense.homicide", "r2")
    assert (
        classify_concurrence_relations(
            (left, other),
            realization_by_instance={left: "a", other: "a"},
        )
        == ()
    )


# --------------------------------------------------------------------------
# D. 결론을 막고 있지 않은 것을 쟁점으로 부풀리지 않는다
# --------------------------------------------------------------------------


def _blocking(*refs: str) -> tuple[Finding, ...]:
    return tuple(
        Finding(label=ref.split(".")[-1], truth="UNKNOWN", predicate_ref=ref)
        for ref in refs
    )


def test_completion_frontier_keeps_only_what_separates_the_open_states() -> None:
    """살인 하나에 예비·중지미수·불능미수 요건까지 붙어 나가고 있었다.

    어느 상태도 사실로 제기되지 않았을 때 남는 것은 여러 상태가 함께 걸려 있는 요건 --
    사망 결과와 실행의 착수 -- 이고, 한 갈래에만 있는 요건은 아직 논점이 아니다.
    """
    blocking = _blocking(
        "ground_fact.death_of_victim",
        "legal_element.commencement_of_execution",
        "legal_element.voluntary_cessation_or_prevention",
        "legal_element.dangerousness",
        "legal_element.purpose_to_commit_target_offense",
        "ground_fact.means_or_object_defect",
    )
    result = {
        "decisive_stage": "completion",
        "completion": {
            "provenance": [
                {"state": name, "truth": "UNKNOWN"}
                for name in (
                    "completed",
                    "attempted",
                    "abandoned_attempt",
                    "impossible_attempt",
                    "preparation",
                )
            ]
        },
    }
    kept = {
        value.predicate_ref
        for value in live_unresolved_frontier(
            REGISTRY, result, "offense.homicide", blocking
        )
    }
    assert kept == {
        "ground_fact.death_of_victim",
        "legal_element.commencement_of_execution",
    }


def test_an_elements_decisive_issue_drops_completion_only_requirements() -> None:
    """구성요건이 결정 단계인데 미수 유형 요건을 쟁점으로 내보내면 단계를 섞는 것이다."""
    blocking = _blocking(
        "legal_element.intent",
        "legal_element.commencement_of_execution",
        "legal_element.voluntary_cessation_or_prevention",
    )
    kept = {
        value.predicate_ref
        for value in live_unresolved_frontier(
            REGISTRY, {"decisive_stage": "elements"}, "offense.homicide", blocking
        )
    }
    assert kept == {"legal_element.intent"}


def test_narrowing_never_empties_the_frontier() -> None:
    """막고 있는 것이 무엇인지 말하지 못하는 것보다는 넓게 말하는 편이 낫다."""
    blocking = _blocking("legal_element.commencement_of_execution")
    kept = live_unresolved_frontier(
        REGISTRY, {"decisive_stage": "elements"}, "offense.homicide", blocking
    )
    assert kept == blocking
