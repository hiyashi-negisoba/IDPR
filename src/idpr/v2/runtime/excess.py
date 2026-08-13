"""공범의 초과 분류 (ExcessPolicyDef 런타임).

교사·공모한 죄와 정범이 실제로 실현한 죄가 다를 때 가담자의 책임 범위를 정한다.
분류는 저작된 derivation 구조와 저작된 incompatible pair만 읽으므로 뉴럴 호출이 없고
사건 텍스트를 해석하지 않는다.

2026-08-13 검수에서 확정된 경계가 이 모듈의 핵심이다.

**derivation이 없다는 사실만으로 질적 초과라고 판정하지 않는다.** 아직 저작되지 않은
구조관계를 "무관하다"로 읽는 것이기 때문이다. 그래서 기본값은 질적 초과가 아니라
`UNRESOLVED_EXCESS_RELATION`이고, 질적 초과는 authored pair가 있을 때만 나온다.

derivation 사슬도 전부 양적 초과로 세지 않는다. 두 형태만 인정한다.

* `qualify` 사슬 -- 절도 -> 특수절도처럼 같은 불법이 가중된 경우.
* `primitive.aggravated_result_attribution`을 가진 `compose` -- 결과적 가중범.

`compose`인데 그 마커가 없는 경우(절도 + 폭행 -> 준강도처럼 독립한 불법이 더해진 경우)는
양적 초과로 자동 분류하지 않는다. 사슬이 있다는 사실만으로 "교사한 범위 안"이라고 읽으면
교사 내용을 넘는 새로운 불법까지 삼키게 된다.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry

AGGRAVATED_RESULT_MARKER = "primitive.aggravated_result_attribution"

NOT_EXCESS = "not_excess"
QUANTITATIVE_ORDINARY = "quantitative_ordinary_qualification"
QUANTITATIVE_RESULT_AGGRAVATED = "quantitative_result_aggravated"
QUALITATIVE = "qualitative"
UNRESOLVED_EXCESS_RELATION = "UNRESOLVED_EXCESS_RELATION"

LIABLE_FOR_INSTIGATED_SCOPE = "liable_for_instigated_scope"
LIABLE_FOR_AGGRAVATED_RESULT = "liable_for_aggravated_result"
NO_LIABILITY_FOR_EXCESS = "no_liability_for_excess"
UNRESOLVED = "unresolved"


class ExcessPolicyError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ExcessAssessment:
    classification: str
    effect: str
    reason: str


def _derivation_step(entry: DefinitionEntry) -> tuple[tuple[str, ...], bool] | None:
    """(따라갈 base offense refs, 결과적 가중범 여부). 따라가면 안 되는 사슬이면 None.

    `compose`인데 결과적 가중범 마커가 없으면 base를 아예 반환하지 않는다. 준강도는 절도를
    component로 갖지만 폭행·협박이라는 독립한 불법이 더해진 것이므로, 여기서 절도까지
    걸어가면 "절도 교사 범위 안"이라는 결론이 나온다.
    """
    if entry.kind != "derived_offense":
        return None
    derivation = entry.payload["derivation"]
    if derivation["kind"] == "qualify":
        return (derivation["base"],), False
    components = derivation.get("components") or ()
    if not any(component.get("ref") == AGGRAVATED_RESULT_MARKER for component in components):
        return None
    bases = tuple(
        component["ref"]
        for component in components
        if component.get("kind") in {"offense", "derived_offense"}
    )
    return bases, True


def _walk_to_instigated(
    registry: DefinitionRegistry, realized_ref: str, instigated_ref: str
) -> tuple[bool, bool]:
    """(도달했는가, 도달 경로에 결과적 가중범 단계가 있었는가).

    사이클이나 반복 방문은 visited로 끊는다 -- derivation은 DAG이지만 저작 오류로 사이클이
    생겼을 때 여기서 무한 루프가 나면 원인이 한참 뒤에 드러난다.
    """
    stack: list[tuple[str, bool]] = [(realized_ref, False)]
    visited: set[str] = set()
    while stack:
        ref, aggravated_so_far = stack.pop()
        if ref == instigated_ref:
            return True, aggravated_so_far
        if ref in visited:
            continue
        visited.add(ref)
        entry = registry.get(ref)
        if entry is None:
            continue
        step = _derivation_step(entry)
        if step is None:
            continue
        bases, aggravated = step
        for base in bases:
            stack.append((base, aggravated_so_far or aggravated))
    return False, False


def classify_excess(
    registry: DefinitionRegistry,
    policy: DefinitionEntry,
    *,
    instigated_offense_ref: str,
    realized_offense_ref: str,
    participant_foreseeability: TruthValue = UNKNOWN,
) -> ExcessAssessment:
    """Classify one (instigated, realized) pair under an authored ExcessPolicyDef."""
    if policy.kind != "excess_policy":
        raise ExcessPolicyError(f"not an excess policy: {policy.id!r}")
    payload = policy.payload

    if instigated_offense_ref == realized_offense_ref:
        return ExcessAssessment(NOT_EXCESS, LIABLE_FOR_INSTIGATED_SCOPE, "realized what was instigated")

    reached, via_aggravated_result = _walk_to_instigated(
        registry, realized_offense_ref, instigated_offense_ref
    )
    if reached and via_aggravated_result:
        branch = payload["quantitative"]["result_aggravated"]
        effect = {
            TRUE: branch["on_true"],
            FALSE: branch["on_false"],
            UNKNOWN: branch["on_unknown"],
        }[participant_foreseeability]
        return ExcessAssessment(
            QUANTITATIVE_RESULT_AGGRAVATED,
            effect,
            f"result-aggravated derivation; participant foreseeability={participant_foreseeability}",
        )
    if reached:
        return ExcessAssessment(
            QUANTITATIVE_ORDINARY,
            payload["quantitative"]["ordinary_qualification_effect"],
            "qualify derivation from the instigated offense",
        )

    authored: Mapping[tuple[str, str], object] = {
        (pair["instigated_offense_ref"], pair["realized_offense_ref"]): pair
        for pair in payload.get("incompatible_offense_pairs") or ()
    }
    if (instigated_offense_ref, realized_offense_ref) in authored:
        return ExcessAssessment(
            QUALITATIVE, payload["qualitative"]["effect"], "authored incompatible offense pair"
        )

    # 검수 ③-a. 여기서 질적 초과로 떨어뜨리면 안 된다.
    return ExcessAssessment(
        UNRESOLVED_EXCESS_RELATION,
        UNRESOLVED,
        "no authored derivation chain and no authored incompatible pair",
    )


__all__ = [
    "AGGRAVATED_RESULT_MARKER",
    "LIABLE_FOR_AGGRAVATED_RESULT",
    "LIABLE_FOR_INSTIGATED_SCOPE",
    "NOT_EXCESS",
    "NO_LIABILITY_FOR_EXCESS",
    "QUALITATIVE",
    "QUANTITATIVE_ORDINARY",
    "QUANTITATIVE_RESULT_AGGRAVATED",
    "UNRESOLVED",
    "UNRESOLVED_EXCESS_RELATION",
    "ExcessAssessment",
    "ExcessPolicyError",
    "classify_excess",
]
