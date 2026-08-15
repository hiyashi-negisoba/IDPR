"""최종 책임 뷰. 인스턴스별 liability chain이 끝난 뒤 한 번 도는 심볼릭 단계."""

from pathlib import Path

import pytest
import yaml

from idpr.v2.evaluate import TRUE
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.concurrence import APPROVED, load_concurrence_rules
from idpr.v2.runtime.excess import (
    LIABLE_FOR_INSTIGATED_SCOPE,
    QUANTITATIVE_ORDINARY,
    UNRESOLVED_EXCESS_RELATION,
)
from idpr.v2.runtime.final_responsibility import (
    EXCESS_ACROSS_EXECUTIONS,
    MULTIPLE_EXCESS_CANDIDATES,
    NOT_ATTRIBUTABLE_BY_EXCESS,
    UNRESOLVED_EXCESS_ATTRIBUTION,
    UNRESOLVED_STATUS_REDIRECTION_TARGET,
    excess_parity_rows,
    plan_status_redirections,
    resolve_final_responsibility,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.stages import (
    LiabilityEvaluation,
    OffenseEstablishment,
    OffenseRealization,
    not_reached,
)
from idpr.v2.runtime.truths import CaseTruths

CASE = "case"
ASCENDANT_STATUS = "legal_element.lineal_ascendant_of_self_or_spouse_status"


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def _instance(offense: str, occurrence: str, actor: str = "甲") -> OffenseInstanceKey:
    return OffenseInstanceKey(CASE, actor, offense, occurrence)


def _established(instance: OffenseInstanceKey) -> LiabilityEvaluation:
    """성립까지 간 평가. 이 모듈이 읽는 것은 `establishment`가 있는지 뿐이다."""
    stage = not_reached()
    realization = OffenseRealization(instance=instance, elements=stage, unlawfulness=stage)
    return LiabilityEvaluation(
        instance=instance,
        completion=None,
        elements=stage,
        unlawfulness=stage,
        culpability=stage,
        punishability=stage,
        realization=realization,
        establishment=OffenseEstablishment(
            instance=instance, realization=realization, culpability=stage
        ),
    )


def _stopped(instance: OffenseInstanceKey) -> LiabilityEvaluation:
    stage = not_reached()
    return LiabilityEvaluation(
        instance=instance,
        completion=None,
        elements=stage,
        unlawfulness=stage,
        culpability=stage,
        punishability=stage,
        decisive_stage="elements",
    )


ORDER = tuple(f"factual_episode:{index:03d}" for index in range(1, 10))


def _view(registry, *, results, provenance, links=(), truths=None, rules=()):
    return resolve_final_responsibility(
        registry,
        case_id=CASE,
        results=results,
        episode_order=ORDER,
        episode_by_instance={key: value[0] for key, value in provenance.items()},
        source_bindings_by_instance={key: value[1] for key, value in provenance.items()},
        derivative_links=links,
        truths=truths if truths is not None else CaseTruths(),
        concurrence_rules=rules,
    )


def test_special_theft_absorbs_the_theft_it_was_materialized_from(registry) -> None:
    theft = _instance("offense.theft", "binding:001")
    special = _instance("derived_offense.special_theft", "derived_binding:001")
    view = _view(
        registry,
        results={theft: _established(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.concurrence.absorbed_instances == frozenset({theft})
    assert view.concurrence.retained_instances == frozenset({special})
    assert len(view.specialty_candidates) == 1


def test_absorption_does_not_cross_actors_in_one_episode(registry) -> None:
    """한 episode에 甲乙丙의 절도가 모두 있을 수 있다. 甲의 특수절도가 乙의 절도를
    삼키면 안 된다."""
    theft = _instance("offense.theft", "binding:001", actor="乙")
    special = _instance("derived_offense.special_theft", "derived_binding:001", actor="甲")
    view = _view(
        registry,
        results={theft: _established(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.concurrence.absorbed_instances == frozenset()
    assert view.specialty_candidates == ()


def test_an_unestablished_offense_never_enters_the_final_view(registry) -> None:
    theft = _instance("offense.theft", "binding:001")
    special = _instance("derived_offense.special_theft", "derived_binding:001")
    view = _view(
        registry,
        results={theft: _stopped(theft), special: _established(special)},
        provenance={
            theft: ("factual_episode:001", ()),
            special: ("factual_episode:001", ("binding:001",)),
        },
    )
    assert view.established_instances == (special,)
    assert view.concurrence.absorbed_instances == frozenset()


def test_instigated_theft_realized_as_special_theft_is_quantitative_excess(registry) -> None:
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    realized = _instance("derived_offense.special_theft", "binding:002", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            realized: _established(realized),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:002", ()),
            realized: ("factual_episode:002", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert len(view.excess_findings) == 1
    finding = view.excess_findings[0]
    assert finding.assessment.classification == QUANTITATIVE_ORDINARY
    assert finding.assessment.effect == LIABLE_FOR_INSTIGATED_SCOPE
    rows = excess_parity_rows(view, None, foreseeability_ref="legal_element.foreseeability")
    assert [row[0] for row in rows] == [accessory]


def test_an_unauthored_offense_relation_stays_unresolved_not_qualitative(registry) -> None:
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    realized = _instance("offense.dwelling_intrusion", "binding:002", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            realized: _established(realized),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:002", ()),
            realized: ("factual_episode:002", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert view.excess_findings[0].assessment.classification == UNRESOLVED_EXCESS_RELATION


def test_two_realized_offenses_for_one_accessory_are_not_folded(registry) -> None:
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    first = _instance("derived_offense.special_theft", "binding:002", actor="乙")
    second = _instance("offense.dwelling_intrusion", "binding:003", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            first: _established(first),
            second: _established(second),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:002", ()),
            first: ("factual_episode:002", ()),
            second: ("factual_episode:002", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert len(view.excess_findings) == 2
    markers = {finding.marker for finding in view.unresolved}
    assert MULTIPLE_EXCESS_CANDIDATES in markers
    # 접을 수 없으면 Scallop에도 내리지 않는다.
    assert excess_parity_rows(view, None, foreseeability_ref="x") == ()


def test_the_mistake_policy_reports_its_missing_inputs_instead_of_going_silent(registry) -> None:
    """doctrine activation 0을 몇 주 동안 못 본 이유가 이것이다. 침묵과 부적용이 같아 보였다."""
    theft = _instance("offense.theft", "binding:001")
    view = _view(
        registry,
        results={theft: _established(theft)},
        provenance={theft: ("factual_episode:001", ())},
    )
    gaps = [
        finding
        for finding in view.unresolved
        if finding.policy_id == "mistake_policy.korean_law_concrete_fact"
    ]
    assert len(gaps) == 1
    assert gaps[0].marker == "UNRESOLVED_MISTAKE_BINDING"
    assert "relation.intended_object_divergence" in gaps[0].missing_refs


def test_the_excess_provenance_inputs_are_not_reported_as_a_gap(registry) -> None:
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    view = _view(
        registry,
        results={accessory: _established(accessory), principal: _established(principal)},
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:002", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    missing = {ref for finding in view.unresolved for ref in finding.missing_refs}
    assert "provenance.instigated_offense_ref" not in missing


def test_article_33_proviso_redirects_only_into_a_planned_instance(registry) -> None:
    accessory = _instance("offense.homicide", "binding:001", actor="甲")
    principal = _instance("offense.homicide", "binding:002", actor="乙")
    redirected = _instance("offense.ancestral_homicide", "binding:001", actor="甲")
    truths = CaseTruths(predicate={(accessory, ASCENDANT_STATUS): TRUE})
    links = ((accessory, principal, "instigator"),)

    applied, unresolved = plan_status_redirections(
        registry, links, truths, known_instances=(accessory, principal)
    )
    assert applied == ()
    assert [finding.marker for finding in unresolved] == [
        UNRESOLVED_STATUS_REDIRECTION_TARGET
    ]

    applied, unresolved = plan_status_redirections(
        registry, links, truths, known_instances=(accessory, principal, redirected)
    )
    assert unresolved == ()
    assert [value.accessory_instance for value in applied] == [redirected]


def test_only_approved_concurrence_rules_reach_the_runtime() -> None:
    """검수 전 규칙은 저작되어 보이되 발화하지 않는다."""
    path = Path("data/v2/concurrence_rules.yaml")
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    approved = {
        entry["rule_id"]
        for entry in document["rules"]
        if entry.get("status") == APPROVED
    }
    assert load_concurrence_rules(path, include_unapproved=True), "rule file is empty"
    assert {rule.rule_id for rule in load_concurrence_rules(path)} == approved


def test_the_r11_shape_now_opens_a_candidate_across_episodes(registry) -> None:
    """甲이 절도를 교사하고 乙이 뒤 episode에서 상해까지 실현한 사안.

    검수 전 same-episode join은 여기서 후보를 닫았다. 지금은 링크를 따라 열리고,
    저작된 incompatible pair(절도->상해)가 질적 초과로 분류한다.
    """
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    injury = _instance("offense.injury", "binding:003", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            injury: _established(injury),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:004", ()),
            injury: ("factual_episode:005", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert len(view.excess_findings) == 1
    finding = view.excess_findings[0]
    assert finding.assessment.classification == "qualitative"
    assert finding.assessment.effect == "no_liability_for_excess"


def test_qualitative_excess_blocks_only_the_excess_attribution(registry) -> None:
    """甲의 절도 교사 책임은 유지되고, 상해로 가는 귀속 edge만 끊긴다."""
    instigated = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    injury = _instance("offense.injury", "binding:003", actor="乙")
    # 모델이 상해에도 참가를 인정해 가담자 instance가 만들어진 경우.
    excess_accessory = _instance("offense.injury", "participation_binding:002", actor="甲")
    view = _view(
        registry,
        results={
            instigated: _established(instigated),
            principal: _established(principal),
            injury: _established(injury),
            excess_accessory: _established(excess_accessory),
        },
        provenance={
            instigated: ("factual_episode:001", ()),
            principal: ("factual_episode:004", ()),
            injury: ("factual_episode:005", ()),
            excess_accessory: ("factual_episode:005", ()),
        },
        links=(
            (instigated, principal, "instigator"),
            (excess_accessory, injury, "instigator"),
        ),
    )
    attributions = [
        value for value in view.excess_attributions if value.excess_offense_ref == "offense.injury"
    ]
    assert len(attributions) == 1
    assert attributions[0].decision == NOT_ATTRIBUTABLE_BY_EXCESS
    assert attributions[0].blocked_instance == excess_accessory
    # 초과한 죄로의 귀속만 빠지고 교사한 죄는 그대로다.
    assert excess_accessory in view.attribution_withheld_instances
    assert excess_accessory not in view.concurrence.retained_instances
    assert instigated in view.concurrence.retained_instances


def test_an_unresolved_excess_neither_convicts_nor_acquits(registry) -> None:
    """미저작 관계는 무책으로 접지도, 중한 죄를 세우지도 않는다."""
    instigated = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    other = _instance("offense.dwelling_intrusion", "binding:002", actor="乙")
    view = _view(
        registry,
        results={
            instigated: _established(instigated),
            principal: _established(principal),
            other: _established(other),
        },
        provenance={
            instigated: ("factual_episode:001", ()),
            principal: ("factual_episode:002", ()),
            other: ("factual_episode:002", ()),
        },
        links=((instigated, principal, "instigator"),),
    )
    assert [value.decision for value in view.excess_attributions] == [
        UNRESOLVED_EXCESS_ATTRIBUTION
    ]
    assert view.excess_attributions[0].blocked_instance is None
    assert instigated in view.concurrence.retained_instances


def test_an_excess_outside_the_linked_execution_is_raised_as_unresolved(registry) -> None:
    """근거가 약한 join을 조용히 단정하지 않는다.

    甲이 절도를 교사하고 乙이 절도를 실행한 뒤 다른 자리에서 또 죄를 저질렀을 때, 그것이
    교사받은 실행이 더 나아간 것인지 별개 범행인지는 여기 있는 provenance로 갈리지 않는다.
    후보는 살리되 그 사실을 표시한다 -- 접는 쪽이든 여는 쪽이든 host가 정하면 저작되지 않은
    법리를 코드로 쓰는 것이다.
    """
    accessory = _instance("offense.theft", "participation_binding:001", actor="甲")
    principal = _instance("offense.theft", "binding:001", actor="乙")
    injury = _instance("offense.injury", "binding:003", actor="乙")
    view = _view(
        registry,
        results={
            accessory: _established(accessory),
            principal: _established(principal),
            injury: _established(injury),
        },
        provenance={
            accessory: ("factual_episode:001", ()),
            principal: ("factual_episode:004", ()),
            injury: ("factual_episode:005", ()),
        },
        links=((accessory, principal, "instigator"),),
    )
    assert len(view.excess_findings) == 1
    assert not view.excess_findings[0].candidate.same_execution
    assert any(
        value.marker == EXCESS_ACROSS_EXECUTIONS for value in view.unresolved
    ), view.unresolved
