from pathlib import Path

import pytest

from idpr.v2.evaluate import TRUE, UNKNOWN
from idpr.v2.runtime.concurrence import (
    ABSORPTION,
    ACTOR_SAME,
    ConcurrenceRule,
    load_concurrence_rules,
    resolve_concurrence,
)
from idpr.v2.runtime.concurrence_condition import (
    ConcurrenceConditionError,
    canonical_conduct_text,
    concurrence_condition_truths,
    condition_output_schema,
    condition_request_payload,
    evidence_texts,
    plan_concurrence_condition_pairs,
    validate_condition_output,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

SEAL = "offense.seal_forgery_or_misuse"
DOCUMENT = "offense.private_document_forgery"
EPISODE = "factual_episode:001"


def _rule() -> ConcurrenceRule:
    return next(
        value
        for value in load_concurrence_rules(Path("data/v2/concurrence_rules.yaml"))
        if value.rule_id == "absorption.seal_forgery_by_private_document_forgery"
    )


def _instances(actor: str = "甲") -> tuple[OffenseInstanceKey, OffenseInstanceKey]:
    return (
        OffenseInstanceKey("case", actor, SEAL, "binding:004"),
        OffenseInstanceKey("case", "甲", DOCUMENT, "binding:002"),
    )


def _pair(actor: str = "甲"):
    seal, document = _instances(actor)
    return plan_concurrence_condition_pairs(
        (seal, document),
        episode_by_instance={seal: EPISODE, document: EPISODE},
        rules=(_rule(),),
    )


def test_the_pair_direction_comes_from_the_rule_not_the_model() -> None:
    pairs = _pair()
    assert len(pairs) == 1
    pair = pairs[0]
    assert pair.absorbed.offense_ref == SEAL
    assert pair.absorbing.offense_ref == DOCUMENT
    # 모델 출력 계약 어디에도 방향은 없다.
    assert set(condition_output_schema(pair)["properties"]) == {
        "pair_id",
        "truth",
        "supporting_quotes",
    }


def test_a_pair_does_not_open_across_actors_or_episodes() -> None:
    assert _pair(actor="乙") == ()
    seal, document = _instances()
    assert (
        plan_concurrence_condition_pairs(
            (seal, document),
            episode_by_instance={seal: EPISODE, document: "factual_episode:002"},
            rules=(_rule(),),
        )
        == ()
    )


def test_the_payload_carries_no_offense_or_absorption_vocabulary() -> None:
    """모델이 죄명을 보면 그 죄의 성립 여부를 함께 판단하기 시작한다."""
    pair = _pair()[0]
    payload = condition_request_payload(
        pair,
        rule=_rule(),
        episode_text="甲은 A의 인감도장을 가지고 나온 다음 A명의 위임장을 작성하였다",
        absorbed_conduct="A의 인감도장을 가지고 나온",
        absorbing_conduct="A명의 위임장 1장을 작성",
    )
    rendered = repr(payload)
    for leaked in (SEAL, DOCUMENT, "흡수", "absorption", "binding:004", pair.rule_id):
        assert leaked not in rendered
    assert payload["condition_statement"] and payload["legal_standard"]


def test_a_true_condition_needs_a_quote_from_what_was_actually_sent() -> None:
    pair = _pair()[0]
    payload = condition_request_payload(
        pair,
        rule=_rule(),
        episode_text="甲은 A의 인감도장을 가지고 나온 다음 A명의 위임장을 작성하였다",
        absorbed_conduct="A의 인감도장을 가지고 나온",
        absorbing_conduct="A명의 위임장 1장을 작성",
    )
    sent = evidence_texts(payload)

    accepted = validate_condition_output(
        {
            "pair_id": pair.pair_id,
            "truth": "TRUE",
            "supporting_quotes": ["A명의 위임장 1장을 작성"],
        },
        pair=pair,
        evidence=sent,
    )
    assert accepted.truth == TRUE

    with pytest.raises(ConcurrenceConditionError, match="exact substring"):
        validate_condition_output(
            {
                "pair_id": pair.pair_id,
                "truth": "TRUE",
                "supporting_quotes": ["그 인영은 위임장의 날인란에 찍혔다"],
            },
            pair=pair,
            evidence=sent,
        )
    with pytest.raises(ConcurrenceConditionError, match="supporting quote"):
        validate_condition_output(
            {"pair_id": pair.pair_id, "truth": "TRUE", "supporting_quotes": []},
            pair=pair,
            evidence=sent,
        )


def test_unknown_needs_no_quote_and_keeps_both_offenses() -> None:
    """UNKNOWN을 FALSE로 수선하지 않는다. 두 죄는 유지되고 unresolved로 남는다."""
    pair = _pair()[0]
    assessment = validate_condition_output(
        {"pair_id": pair.pair_id, "truth": "UNKNOWN", "supporting_quotes": []},
        pair=pair,
        evidence=("무엇이든",),
    )
    truths = concurrence_condition_truths((assessment,))
    assert truths[(pair.rule_id, pair.absorbed, pair.absorbing)] == UNKNOWN

    seal, document = _instances()
    from idpr.v2.runtime.concurrence import ConcurrenceCandidate

    candidate = ConcurrenceCandidate(_rule(), seal, document, EPISODE)
    resolution = resolve_concurrence(
        (seal, document), (candidate,), condition_truths=truths
    )
    assert resolution.absorbed_instances == frozenset()
    assert resolution.unresolved_candidates == (candidate,)


def test_a_true_condition_lowers_into_the_existing_absorption_reducer() -> None:
    """새 심볼릭 코드 없이 기존 reducer가 그대로 소비한다."""
    pair = _pair()[0]
    assessment = validate_condition_output(
        {
            "pair_id": pair.pair_id,
            "truth": "TRUE",
            "supporting_quotes": ["A명의 위임장"],
        },
        pair=pair,
        evidence=("甲은 A명의 위임장 1장을 작성하였다",),
    )
    seal, document = _instances()
    from idpr.v2.runtime.concurrence import ConcurrenceCandidate

    resolution = resolve_concurrence(
        (seal, document),
        (ConcurrenceCandidate(_rule(), seal, document, EPISODE),),
        condition_truths=concurrence_condition_truths((assessment,)),
    )
    assert resolution.absorbed_instances == frozenset({seal})
    assert resolution.retained_instances == frozenset({document})


def test_conduct_text_drops_only_fragments_contained_in_another() -> None:
    combined = (
        "A의 인감도장을 가지고 나온\n"
        "甲은 A를 살해한 직후 병실에 보관되어 있던 A의 인감도장을 가지고 나온"
    )
    assert canonical_conduct_text(combined) == (
        "甲은 A를 살해한 직후 병실에 보관되어 있던 A의 인감도장을 가지고 나온"
    )
    # 서로 포함하지 않는 두 조각은 둘 다 남는다.
    assert canonical_conduct_text("첫 번째 사실\n두 번째 사실") == "첫 번째 사실 두 번째 사실"


def test_an_unauthored_condition_meaning_cannot_be_asked() -> None:
    rule = ConcurrenceRule(
        "rule.draft", ABSORPTION, SEAL, DOCUMENT, "condition.draft",
        actor_constraint=ACTOR_SAME,
    )
    seal, document = _instances()
    pair = plan_concurrence_condition_pairs(
        (seal, document),
        episode_by_instance={seal: EPISODE, document: EPISODE},
        rules=(rule,),
    )[0]
    with pytest.raises(ConcurrenceConditionError, match="must be authored"):
        condition_request_payload(
            pair,
            rule=rule,
            episode_text="본문",
            absorbed_conduct="첫 행위",
            absorbing_conduct="두 번째 행위",
        )
