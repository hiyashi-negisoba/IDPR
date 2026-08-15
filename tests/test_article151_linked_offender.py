"""제151조의 대상자 신분은 그 사람의 결과에서만 나온다.

이 파일이 이번에 처음 생겼다는 사실 자체가 이 결함의 배경이다. `resolve_article_151_liability()`는
Phase 5.1부터 있었지만 레포 어디에도 호출부가 없었고 테스트도 없었으므로, "구현되어 있다"는
믿음과 "한 번도 실행되지 않는다"는 사실이 오래 공존할 수 있었다.
"""

from __future__ import annotations

from pathlib import Path

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.effects import ActiveDoctrineRefs
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey
from idpr.v2.runtime.stages import UtilizedParticipantOutcome
from idpr.v2.runtime.statutory import (
    Article151QualifyingLink,
    qualifies_for_article_151,
    resolve_article_151_liability,
)
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
CASE = "case"
INSTANCE = OffenseInstanceKey(CASE, "丙", "offense.harboring_or_escape", "realization:001")
STATUS_REF = "legal_element.offender_status_of_object"


def _compiled() -> CompiledOffense:
    compiled = compile_offense(REGISTRY, "offense.harboring_or_escape")
    assert isinstance(compiled, CompiledOffense)
    return compiled


def _link(offense_ref: str, status: str) -> Article151QualifyingLink:
    return Article151QualifyingLink(
        UtilizedParticipantOutcome(
            FactualParticipantKey(CASE, "乙"), offense_ref, status
        ),
        "linked offender outcome",
    )


def _resolve(link: Article151QualifyingLink | None, truths: CaseTruths | None = None):
    return resolve_article_151_liability(
        REGISTRY,
        _compiled(),
        INSTANCE,
        CompletionResult(state="completed", punishable=True),
        ActiveDoctrineRefs(),
        truths if truths is not None else CaseTruths(predicate={}),
        link,
    )


def _status_truth(evaluation) -> str:
    obligation = next(
        value
        for value in evaluation.elements.provenance
        if type(value.obligation).__name__ == "Article151OffenderStatusObligation"
    )
    return obligation.truth


def test_the_linked_offender_stays_a_participant_and_never_becomes_an_instance() -> None:
    """질문은 丙의 죄책만 묻는다. 乙에게 답변용 instance를 만들어 타입을 맞추면 안 된다."""
    evaluation = _resolve(_link("offense.theft", "liable_exact_offense"))
    obligation = next(
        value.obligation
        for value in evaluation.elements.provenance
        if type(value.obligation).__name__ == "Article151OffenderStatusObligation"
    )

    assert obligation.linked_participant == FactualParticipantKey(CASE, "乙")
    assert obligation.qualifying_offense_ref == "offense.theft"
    assert not hasattr(obligation, "linked_instance")


def test_an_absent_link_is_unknown_rather_than_false() -> None:
    """이 좁은 입력은 "자격 있는 선행범죄가 없다"를 증명하지 못한다."""
    assert _status_truth(_resolve(None)) == "UNKNOWN"


def test_a_linked_offender_who_is_not_liable_does_not_establish_the_status() -> None:
    assert _status_truth(_resolve(_link("offense.theft", "elements_failure"))) == "UNKNOWN"
    assert _status_truth(_resolve(_link("offense.theft", "unresolved"))) == "UNKNOWN"


def test_an_unauthored_penalty_threshold_is_unknown_not_an_implied_pass() -> None:
    """형법각칙은 사실상 전부 벌금 이상이다. 그래서 더더욱 host가 가정하면 안 된다.

    가정이 틀린 단 한 자리가 보이지 않게 되기 때문이다. 값 저작 전에는 UNKNOWN이 맞다.
    """
    assert qualifies_for_article_151(REGISTRY, "offense.theft") is False
    assert _status_truth(_resolve(_link("offense.theft", "liable_exact_offense"))) == "UNKNOWN"


def test_the_raw_target_instance_fact_cannot_impersonate_the_linked_result() -> None:
    """대상자 신분은 override되는 값이다. Call 2가 무슨 답을 냈든 링크가 이긴다."""
    truths = CaseTruths(predicate={(INSTANCE, STATUS_REF): "TRUE"})

    assert _status_truth(_resolve(None, truths)) == "UNKNOWN"
