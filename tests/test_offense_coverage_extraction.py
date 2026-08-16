"""죄명 추출·정규화. 이 세 가지가 커버리지 수치를 조용히 망쳤던 자리다."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "audit_v2_offense_coverage",
    Path(__file__).resolve().parents[1] / "scripts/audit_v2_offense_coverage.py",
)
audit = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(audit)


def test_number_inside_a_name_is_not_a_boundary() -> None:
    """`제3자뇌물교부죄`가 `자뇌물교부죄`로 잘리면 저작된 죄가 미저작으로 계산된다."""
    assert "제3자뇌물교부죄" in audit.offense_names("乙에게 제3자뇌물교부죄가 성립한다")


def test_concurrence_words_are_not_offences() -> None:
    text = "두 죄는 포괄일죄이고 기본범죄인 상해죄가 성립하며 후단 범죄는 논하지 않는다"
    assert audit.offense_names(text) == {"상해죄"}


def test_completion_and_participation_are_not_part_of_the_name() -> None:
    """미수는 completion, 교사는 participation -- 우리 스키마는 죄명 밖에서 표현한다."""
    assert audit.same_offense("살인미수죄", "살인죄")
    assert audit.same_offense("주거침입교사죄", "주거침입죄")
    assert audit.same_offense("존속살해교사미수죄", "존속살해죄")


def test_middle_dot_names_match_either_branch() -> None:
    assert audit.same_offense("사문서위조죄", "사문서위조·변조죄")
    assert audit.same_offense("사문서변조죄", "사문서위조·변조죄")


def test_middle_dot_split_invents_no_stem() -> None:
    """가능한 모든 자리에서 자르면 `사변조`가 생기고 다른 죄명과 우연히 맞는다."""
    values = audit.stems("사문서위조·변조죄")
    assert "사문서변조" in values
    assert not any(value in {"사변조", "사문변조", "사문서위변조"} for value in values)


def test_aggravated_form_is_a_different_offence() -> None:
    """기본범만 열고 가중범을 맞힌 것으로 세지 않는다."""
    assert not audit.same_offense("특수절도죄", "절도죄")
    assert not audit.same_offense("강도상해죄", "강도죄")
