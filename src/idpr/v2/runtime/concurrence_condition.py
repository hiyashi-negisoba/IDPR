"""Pair-scoped assessment channel for authored concurrence conditions.

승인된 흡수 규칙은 조건을 물을 곳이 없어 후보가 열려도 UNKNOWN이었다. 이 모듈이 그 채널이다.

조건은 단일 instance의 predicate가 아니라 **두 instance 사이의 관계**이므로 ordinary predicate
Call 2에 얹지 않고 Article 263과 같은 pair carrier로 간다. 그리고 그 관계 하나만 진다 --
흡수되는 쪽 죄가 성립하는지(권한 없는 위조·부정사용이었는지)는 그 instance의 elements가 이미
판단했고, 해소 시점에는 그 instance가 established라는 사실이 그것을 보장한다. 조건이 그것을 다시
물으면 하나의 neural target이 자기 몫의 atomic proposition 하나만 판단한다는 v2 원칙이 깨지고,
같은 질문에 두 곳이 다르게 답할 수 있게 된다.

방향은 모델에게 묻지 않는다. `left/right`가 아니라 `absorbed/absorbing`인 이유이며, 그 방향은
저작된 규칙의 `first/second`가 이미 정했다.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.evaluate import TruthValue
from idpr.v2.runtime.concurrence import (
    ABSORPTION,
    IMAGINATIVE_CONCURRENCE,
    ConcurrenceRule,
    plan_concurrence_candidates,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})

ASSESSABLE_KINDS = frozenset({ABSORPTION, IMAGINATIVE_CONCURRENCE})
"""SPECIALTY는 여기 없다. 그 관계는 DSL 자신의 qualify-derivation이 지므로 물을 것이 없다."""


class ConcurrenceConditionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ConcurrenceConditionPair:
    pair_id: str
    rule_id: str
    condition_ref: str
    absorbed: OffenseInstanceKey
    absorbing: OffenseInstanceKey
    factual_episode_id: str

    def as_dict(self) -> dict[str, Any]:
        def key(value: OffenseInstanceKey) -> dict[str, str]:
            return {
                "case_id": value.case_id,
                "actor_id": value.actor_id,
                "offense_ref": value.offense_ref,
                "occurrence_id": value.occurrence_id,
            }

        return {
            "pair_id": self.pair_id,
            "rule_id": self.rule_id,
            "condition_ref": self.condition_ref,
            "absorbed_instance_key": key(self.absorbed),
            "absorbing_instance_key": key(self.absorbing),
            "factual_episode_id": self.factual_episode_id,
        }


def plan_concurrence_condition_pairs(
    planned_instances: Iterable[OffenseInstanceKey],
    *,
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    rules: Iterable[ConcurrenceRule],
    factual_episode_order: Sequence[str] = (),
) -> tuple[ConcurrenceConditionPair, ...]:
    """Open one pair per authored rule join, using the resolution-time join itself.

    평가 시점과 해소 시점의 후보가 다르다는 점이 이 함수의 전제다. 조건 assessment는 Call 2
    시점이라 *계획된* instance로 열리고, 실제 흡수는 최종 책임 단계에서 *성립한* instance에만
    적용된다. 그래서 assessment 후보 ⊇ 해소 후보이고, 조건이 TRUE여도 한쪽이 성립하지 않으면
    흡수는 발화하지 않는다.

    그 관계가 성립하려면 두 시점이 **같은 join**을 써야 한다. 그래서 여기서 join을 다시 쓰지
    않고 :func:`plan_concurrence_candidates`를 그대로 호출한다 -- 후보를 넓히는 별도의 문이
    생기지 않는다.
    """
    candidates = plan_concurrence_candidates(
        planned_instances,
        episode_by_instance=episode_by_instance,
        rules=(rule for rule in rules if rule.kind in ASSESSABLE_KINDS),
        factual_episode_order=tuple(factual_episode_order),
    )
    output: list[ConcurrenceConditionPair] = []
    for candidate in candidates:
        output.append(
            ConcurrenceConditionPair(
                pair_id=f"concurrence-pair:{len(output) + 1:04d}",
                rule_id=candidate.rule.rule_id,
                condition_ref=candidate.rule.condition_ref,
                absorbed=candidate.first,
                absorbing=candidate.second,
                factual_episode_id=candidate.factual_episode_id,
            )
        )
    return tuple(output)


def canonical_text(value: str) -> str:
    """prompt와 exact-substring 검증이 보는 단 하나의 문자열.

    Call 1.5-D에서 확정한 것과 같은 처리다. 모델이 낸 인용의 개행만 고쳐 통과시키는 것은
    repair이고, 한 번 허용하면 경계가 사라진다. 대신 보내는 문자열 자체를 정규화한다.
    원본 span은 plan artifact에 그대로 남으므로 provenance를 잃지 않는다.
    """
    return " ".join(value.split())


def canonical_conduct_text(evidence_text: str) -> str:
    """binding evidence를 프롬프트에 실을 하나의 문자열로 만든다.

    `IssueBinding.evidence_text`는 actor-action fragment와 context fragment를 개행으로 이어
    붙인 것이고, 둘이 겹치는 일이 흔하다(`r12_p2_q1_da` binding:004는 짧은 인용과 그것을 품은
    긴 문장이 함께 들어 있다). 그대로 실으면 같은 사실이 두 번 적힌 지문이 된다.

    그래서 다른 fragment에 통째로 포함되는 fragment만 뺀다. 문장을 고치거나 골라내는 것이
    아니라 **같은 문자열의 중복을 없애는 것**이고, 원본 fragment와 span은 Call 1.5 artifact에
    그대로 남는다.
    """
    fragments = [
        canonical_text(fragment)
        for fragment in evidence_text.split("\n")
        if canonical_text(fragment)
    ]
    kept = [
        fragment
        for index, fragment in enumerate(fragments)
        if not any(
            fragment != other and fragment in other
            for position, other in enumerate(fragments)
            if position != index
        )
    ]
    return " ".join(dict.fromkeys(kept))


def condition_request_payload(
    pair: ConcurrenceConditionPair,
    *,
    rule: ConcurrenceRule,
    episode_text: str,
    absorbed_conduct: str,
    absorbing_conduct: str,
) -> dict[str, Any]:
    """모델에게 가는 요청. 죄명·조문·`흡수`는 들어가지 않는다.

    두 행위는 `first_conduct`/`second_conduct`로만 제시한다. 죄명을 실으면 모델이 그 죄의
    성립 여부를 함께 판단하기 시작하고, 그것은 이 target의 몫이 아니다.
    """
    if rule.rule_id != pair.rule_id:
        raise ConcurrenceConditionError(f"{pair.pair_id}: rule does not match the pair")
    if not rule.condition_statement or not rule.legal_standard:
        raise ConcurrenceConditionError(
            f"{rule.rule_id}: condition meaning must be authored before it can be asked"
        )
    texts = {
        "episode_text": canonical_text(episode_text),
        "first_conduct": canonical_text(absorbed_conduct),
        "second_conduct": canonical_text(absorbing_conduct),
    }
    for field, value in texts.items():
        if not value:
            raise ConcurrenceConditionError(f"{pair.pair_id}: empty {field}")
    return {
        "case_id": pair.absorbed.case_id,
        "pair_id": pair.pair_id,
        "condition_statement": rule.condition_statement,
        "legal_standard": rule.legal_standard,
        "actor_id": pair.absorbed.actor_id,
        "factual_episode_id": pair.factual_episode_id,
        **texts,
    }


def evidence_texts(payload: Mapping[str, Any]) -> tuple[str, ...]:
    """검증이 보는 문자열 집합 -- 모델에게 실제로 보낸 그것뿐이다."""
    return tuple(
        str(payload[field]) for field in ("episode_text", "first_conduct", "second_conduct")
    )


def condition_output_schema(pair: ConcurrenceConditionPair) -> dict[str, Any]:
    """Guided-decoding schema. pair 식별자는 `const`로 못 박는다.

    Call 1.5-D 1차 실행이 43/43 계약 실패했던 원인이 자유 문자열 식별자였다. 되받아 적는
    지시의 준수 여부는 이 호출이 답할 질문이 아니므로 디코딩에서 강제한다.
    """
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["pair_id", "truth", "supporting_quotes"],
        "properties": {
            "pair_id": {"const": pair.pair_id},
            "truth": {"enum": sorted(_TRUTHS)},
            "supporting_quotes": {"type": "array", "items": {"type": "string"}},
        },
    }


@dataclass(frozen=True, slots=True)
class ConcurrenceConditionAssessment:
    pair: ConcurrenceConditionPair
    truth: TruthValue
    supporting_quotes: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.pair.as_dict(),
            "truth": self.truth,
            "supporting_quotes": list(self.supporting_quotes),
        }


def validate_condition_output(
    raw: Mapping[str, Any],
    *,
    pair: ConcurrenceConditionPair,
    evidence: Sequence[str],
) -> ConcurrenceConditionAssessment:
    """Exact-correspondence 검증. 위반은 hard-fail이고 host가 고치지 않는다.

    TRUE인데 근거 인용이 보낸 문자열의 정확한 부분문자열이 아니면 그 pair는 reject한다.
    근거 없는 흡수는 흡수하지 않는 것보다 나쁘다 -- 죄 하나가 조용히 사라지기 때문이다.
    """
    if not isinstance(raw, Mapping) or set(raw) != {"pair_id", "truth", "supporting_quotes"}:
        raise ConcurrenceConditionError(f"{pair.pair_id}: response shape mismatch")
    if str(raw["pair_id"]) != pair.pair_id:
        raise ConcurrenceConditionError(f"{pair.pair_id}: pair identity mismatch")
    truth = str(raw["truth"])
    if truth not in _TRUTHS:
        raise ConcurrenceConditionError(f"{pair.pair_id}: unsupported truth {truth!r}")
    values = raw["supporting_quotes"]
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise ConcurrenceConditionError(f"{pair.pair_id}: supporting_quotes must be strings")
    quotes = tuple(canonical_text(value) for value in values)
    if truth == "TRUE":
        if not quotes:
            raise ConcurrenceConditionError(f"{pair.pair_id}: TRUE needs a supporting quote")
        for quote in quotes:
            if not any(quote and quote in text for text in evidence):
                raise ConcurrenceConditionError(
                    f"{pair.pair_id}: quote is not an exact substring of the sent evidence: "
                    f"{quote!r}"
                )
    return ConcurrenceConditionAssessment(pair, truth, quotes)


def concurrence_condition_truths(
    assessments: Iterable[ConcurrenceConditionAssessment],
) -> dict[tuple[str, OffenseInstanceKey, OffenseInstanceKey], TruthValue]:
    """`resolve_concurrence`가 읽는 형태로 낮춘다. 새 심볼릭 코드는 없다.

    키가 `(rule_id, first, second)`인 것이 방향을 지킨다 -- first가 흡수되는 쪽이다.
    """
    output: dict[tuple[str, OffenseInstanceKey, OffenseInstanceKey], TruthValue] = {}
    for assessment in assessments:
        key = (assessment.pair.rule_id, assessment.pair.absorbed, assessment.pair.absorbing)
        existing = output.get(key)
        if existing is not None and existing != assessment.truth:
            raise ConcurrenceConditionError(f"conflicting condition truths for {key[0]!r}")
        output[key] = assessment.truth
    return output


__all__ = [
    "ASSESSABLE_KINDS",
    "ConcurrenceConditionAssessment",
    "ConcurrenceConditionError",
    "ConcurrenceConditionPair",
    "canonical_conduct_text",
    "canonical_text",
    "concurrence_condition_truths",
    "condition_output_schema",
    "condition_request_payload",
    "evidence_texts",
    "plan_concurrence_condition_pairs",
    "validate_condition_output",
]
