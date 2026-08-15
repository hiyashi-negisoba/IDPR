from __future__ import annotations

from pathlib import Path

from idpr.v2.issue_binding import IssueBinding
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.intended_object import (
    intended_object_divergences,
    mistake_findings,
    offense_instance_probe_targets,
)
from idpr.v2.runtime.mistake import apply_mistake_policy
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
POLICY = REGISTRY.get("mistake_policy.korean_law_concrete_fact")
CASE = "case"


def _binding(directed: str | None, bearer: str | None, binding_id: str = "binding:001") -> IssueBinding:
    return IssueBinding(
        binding_id,
        "factual_episode:001",
        0,
        "offense.injury",
        "甲",
        "factual_action:001:001",
        (),
        ("C",),
        directed,
        bearer,
        None,
    )


def _realizations(binding_ids: tuple[str, ...] = ("binding:001",)):
    return (("realization:001", "甲", "offense.injury", binding_ids),)


def test_two_bound_identities_produce_a_structural_divergence() -> None:
    values = intended_object_divergences(
        case_id=CASE, realizations=_realizations(), bindings=(_binding("乙", "C"),)
    )

    assert len(values) == 1
    assert values[0].truth == "TRUE"
    assert values[0].instance == OffenseInstanceKey(CASE, "甲", "offense.injury", "realization:001")


def test_the_same_object_is_a_deterministic_false_not_an_open_question() -> None:
    """불일치의 부재도 사실이다. 모델에게 되물으면 없는 착오를 만들 자리만 생긴다."""
    values = intended_object_divergences(
        case_id=CASE, realizations=_realizations(), bindings=(_binding("C", "C"),)
    )

    assert values[0].truth == "FALSE"
    assert offense_instance_probe_targets(REGISTRY, values) == ()


def test_a_missing_identity_leaves_the_case_unresolved() -> None:
    """정황에서 지향 대상을 추정하지 않는다 -- `factual_targets` 재해석을 거부한 것과 같은 이유다."""
    assert (
        intended_object_divergences(
            case_id=CASE, realizations=_realizations(), bindings=(_binding("乙", None),)
        )
        == ()
    )


def test_conflicting_source_bindings_produce_nothing() -> None:
    values = intended_object_divergences(
        case_id=CASE,
        realizations=_realizations(("binding:001", "binding:002")),
        bindings=(_binding("乙", "C"), _binding("丁", "C", "binding:002")),
    )

    assert values == ()


def test_divergence_opens_the_offense_instance_probe_leaf() -> None:
    """`applies_to: offense_instance` probe에는 target producer가 없었다.

    저작·런타임·Scallop 경로가 다 있는데 leaf가 계획되지 않으면 정책은 어떤 사건에서도
    발화하지 못한다. 제33조 단서에서 이미 한 번 나온 고장이다.
    """
    values = intended_object_divergences(
        case_id=CASE, realizations=_realizations(), bindings=(_binding("乙", "C"),)
    )
    targets = offense_instance_probe_targets(REGISTRY, values)

    # 저작된 probe는 고의도 같이 요구한다. 그것은 대개 이미 열려 있는 구성요건 target이라
    # planner에서 dedup되지만, 여기서는 probe가 요구하는 집합 그대로가 나오는지를 본다.
    assert sorted(ref for _instance, ref in targets) == [
        "legal_element.intent",
        "legal_element.object_misidentification",
    ]


def test_the_policy_fires_end_to_end_from_two_bound_identities() -> None:
    instance = OffenseInstanceKey(CASE, "甲", "offense.injury", "realization:001")
    values = intended_object_divergences(
        case_id=CASE, realizations=_realizations(), bindings=(_binding("乙", "C"),)
    )
    truths = CaseTruths(
        predicate={
            (instance, "legal_element.intent"): "TRUE",
            (instance, "legal_element.object_misidentification"): "TRUE",
        }
    )

    findings = mistake_findings(values, truths, policy=POLICY)
    updated = apply_mistake_policy(truths, findings, policy=POLICY)

    assert len(findings) == 1
    assert updated.predicate[(instance, "legal_element.intent")] == "TRUE"


def test_the_policy_stays_silent_when_intent_toward_the_intended_object_is_absent() -> None:
    """없는 고의를 만들어 귀속시키지 않는다. 침묵이 틀린 귀속보다 안전하다."""
    instance = OffenseInstanceKey(CASE, "甲", "offense.injury", "realization:001")
    values = intended_object_divergences(
        case_id=CASE, realizations=_realizations(), bindings=(_binding("乙", "C"),)
    )
    truths = CaseTruths(
        predicate={
            (instance, "legal_element.intent"): "FALSE",
            (instance, "legal_element.object_misidentification"): "TRUE",
        }
    )

    updated = apply_mistake_policy(
        truths, mistake_findings(values, truths, policy=POLICY), policy=POLICY
    )

    assert updated.predicate[(instance, "legal_element.intent")] == "FALSE"
