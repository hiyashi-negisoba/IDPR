"""Known gaps must stay honest in both directions.

A gap recorded here and then quietly closed is as bad as one that is never recorded: the next
person reads the file, believes 폭행죄 is still missing, and works around an absence that no longer
exists. So these tests fail when a listed offense *appears*, which is the moment someone should
come back and delete the entry.
"""

import dataclasses
from pathlib import Path

import pytest
import yaml

from idpr.v2.issue_binding import IssueBinding
from idpr.v2.policy_probes import probe_requirements, unsatisfied_requirements
from idpr.v2.registry import load_definitions

GAPS = Path("data/v2/representation_gaps.yaml")


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


@pytest.fixture(scope="module")
def gaps():
    return yaml.safe_load(GAPS.read_text())["gaps"]


def test_every_unauthored_offense_family_is_still_unauthored(registry, gaps) -> None:
    for gap in gaps:
        for ref in gap.get("absent_offense_refs") or ():
            assert registry.get(ref) is None, (
                f"{ref!r} now exists -- close {gap['id']!r} in {GAPS} and revisit "
                f"whatever it was blocking"
            )


def test_the_assault_family_gap_is_closed_without_dropping_what_it_covered(gaps) -> None:
    """공백은 조용히 사라져서도 안 된다.

    폭행죄 family는 저작되었지만 그 gap이 덮고 있던 것 중 둘이 남았다. 항목만 지우면
    다음 사람은 `r11_p1_q1`이 완전히 닫힌 줄 알게 된다.
    """
    recorded = {gap["id"] for gap in gaps}

    assert "gap.assault_offense_family" not in recorded
    assert "gap.co_principal_qualitative_excess" in recorded
    assert "gap.special_assault_aggravated_result" in recorded
    assert "gap.stolen_property_offense_family" in recorded


def test_the_intended_object_gap_is_closed_by_representation_not_reinterpretation(
    registry, gaps
) -> None:
    """2026-08-13에 거부된 것은 `factual_targets` 재해석이지 이 기능이 아니다.

    공백은 좁은 factual representation 두 개를 새로 결박해서 닫혔다. 그러니 gap 항목이
    남아 있으면 안 되고(다음 사람이 없는 공백을 우회하게 된다), 동시에 재해석 경로가
    되살아나도 안 된다. 둘 다 여기서 지킨다.
    """
    assert "gap.intended_object_identity" not in {gap["id"] for gap in gaps}

    supplied = {
        requirement.ref
        for requirement in probe_requirements(registry)
        if requirement.supply != "structural_relation"
    }
    outstanding = {
        requirement.ref
        for requirement in unsatisfied_requirements(registry, available_refs=supplied)
        if requirement.policy_id == "mistake_policy.korean_law_concrete_fact"
    }
    # 이 relation은 Call 2가 아니라 host가 공급한다. 그래서 "아직 공급되지 않은 것"으로
    # 남아 있는 것이 정상이고, 그 공급자가 실재하는지는 아래에서 확인한다.
    assert outstanding == {"relation.intended_object_divergence"}

    fields = {field.name for field in dataclasses.fields(IssueBinding)}
    assert {"directed_action_target", "actual_result_bearer"} <= fields


def test_every_gap_names_a_typed_marker(gaps) -> None:
    """A gap without a marker degrades into silence at runtime."""
    for gap in gaps:
        assert gap.get("marker"), f"{gap['id']} has no typed marker"
        assert gap.get("summary"), f"{gap['id']} has no summary"
