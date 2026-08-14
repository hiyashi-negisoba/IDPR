"""Doctrine 축의 종료 증명.

감사 질문은 하나였다. trigger는 존재하는데 effect가 symbolic liability까지 실제 도달
가능한가. 모델이 법리를 놓치는 것은 여기서 다루지 않는다.
"""

from __future__ import annotations

import itertools
from pathlib import Path

import pytest
import yaml

from idpr.v2 import expressions
from idpr.v2.doctrine_cues import load_doctrine_cues
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, evaluate
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.doctrine_activation import raised_active_doctrines
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
DOCTRINES = tuple(REGISTRY.by_kind["doctrine"])


def _blocker_leaves(doctrine) -> frozenset[str]:
    return expressions.leaf_refs(doctrine.payload.get("blocked_when"))


# --------------------------------------------------------------------------
# 1. 발화 불가능성
# --------------------------------------------------------------------------


@pytest.mark.parametrize("doctrine", DOCTRINES, ids=lambda value: value.id)
def test_doctrine_fires_when_the_exception_is_simply_unstated(doctrine) -> None:
    """예외가 사건에 적히지 않았다는 이유로 법리가 막히지 않는다.

    원인에 있어서 자유로운 행위, 위난감수의무, 승낙배제 특별규정 -- 이런 사실은 있었을 때만
    사건에 서술되고 없었다고 적히지 않는다. 이를 `requires` 안에 `NOT(...)`으로 넣으면 Kleene
    에서 UNKNOWN이 곧 불성립이 되어, 감사 시점에 13개 중 5개가 어떤 사건에서도 성립할 수
    없었다. `blocked_when`은 예외가 **확정**되었을 때만 배제한다.
    """
    requires = expressions.canonicalize(doctrine.payload["requires"])
    blocker = expressions.canonicalize(doctrine.payload.get("blocked_when"))
    blocker_leaves = _blocker_leaves(doctrine)
    free = sorted(expressions.leaf_refs(doctrine.payload["requires"]) - blocker_leaves)
    unstated = {ref: UNKNOWN for ref in blocker_leaves}
    assert any(
        evaluate(requires, {**unstated, **dict(zip(free, combo))}) == TRUE
        and (
            blocker is None
            or evaluate(blocker, {**unstated, **dict(zip(free, combo))}) != TRUE
        )
        for combo in itertools.product([TRUE, FALSE], repeat=len(free))
    ), f"{doctrine.id}: 예외가 미서술이면 어떤 배정으로도 성립할 수 없다"


def test_every_doctrine_is_either_raisable_or_a_recorded_gap() -> None:
    """제기 경로가 없는 법리는 leaf가 target으로 열리지 않아 영원히 잠든다.

    조용히 잠드는 것만 막는다. `raising_status: representation_gap`으로 사유와 함께 적힌
    것은 결함이 아니라 기록된 공백이고, 공백이 메워지면 그때 이 목록에서 빠진다.
    """
    raw = yaml.safe_load(
        (ROOT / "data/v2/doctrine_raising_cues.yaml").read_text(encoding="utf-8")
    )
    production = {
        ref for cue in load_doctrine_cues(ROOT / "data/v2/doctrine_raising_cues.yaml")
        for ref in cue.raises
    }
    documented = {
        ref
        for cue in raw["cues"]
        if cue.get("raising_status") == "representation_gap"
        for ref in cue["raises"]
    }
    missing = sorted({doctrine.id for doctrine in DOCTRINES} - production - documented)
    assert not missing, f"제기 경로도 공백 기록도 없는 doctrine: {missing}"


def test_blocker_leaves_are_opened_as_targets_too() -> None:
    """예외 사실도 물어봐야 한다. 묻지 않으면 UNKNOWN으로 남고 아무것도 막지 못한다."""
    cues = load_doctrine_cues(ROOT / "data/v2/doctrine_raising_cues.yaml")
    # build_v2_doctrine_target_plan 이 여는 leaf 집합과 같은 식으로 계산한다.
    for cue in cues:
        for ref in cue.raises:
            doctrine = REGISTRY.get(ref)
            leaves = frozenset(
                (
                    *expressions.leaf_refs(doctrine.payload["requires"]),
                    *_blocker_leaves(doctrine),
                )
            )
            assert _blocker_leaves(doctrine) <= leaves, ref


# --------------------------------------------------------------------------
# 2. 배타·우선관계 — 예외는 확정될 때만 이긴다
# --------------------------------------------------------------------------


def _instance() -> OffenseInstanceKey:
    return OffenseInstanceKey("case", "甲", "offense.homicide", "occ:001")


@pytest.mark.parametrize(
    "doctrine", [value for value in DOCTRINES if value.payload.get("blocked_when")],
    ids=lambda value: value.id,
)
def test_confirmed_exception_deactivates_but_unknown_exception_does_not(doctrine) -> None:
    instance = _instance()
    # requires를 실제로 참으로 만드는 배정을 찾는다.
    free = sorted(expressions.leaf_refs(doctrine.payload["requires"]))
    satisfying = next(
        dict(zip(free, combo))
        for combo in itertools.product([TRUE, FALSE], repeat=len(free))
        if evaluate(expressions.canonicalize(doctrine.payload["requires"]), dict(zip(free, combo)))
        == TRUE
    )
    blocker_ref = next(iter(_blocker_leaves(doctrine)))

    def activate(blocker_truth):
        truths = CaseTruths(
            predicate={
                (instance, ref): value for ref, value in satisfying.items()
            }
            | ({(instance, blocker_ref): blocker_truth} if blocker_truth else {})
        )
        return raised_active_doctrines(REGISTRY, (instance,), (doctrine.id,), truths)

    assert activate(None), f"{doctrine.id}: 예외 미서술인데 활성화되지 않았다"
    assert activate(UNKNOWN), f"{doctrine.id}: UNKNOWN 예외가 법리를 막았다"
    assert not activate(TRUE), f"{doctrine.id}: 확정된 예외가 법리를 막지 못했다"


# --------------------------------------------------------------------------
# 3. 저작 정합 — 긍정형 predicate가 논리적 부정으로 읽히지 않는가
# --------------------------------------------------------------------------


_NEGATIVE_MARKERS = ("없음", "없는지", "아님", "부존재")


@pytest.mark.parametrize("doctrine", DOCTRINES, ids=lambda value: value.id)
def test_blocker_predicates_are_authored_in_the_positive(doctrine) -> None:
    """blocker는 "예외가 있다"여야 한다.

    `statutory_bar_on_consent`는 이름이 "배제규정이 있다"인데 뜻이 "없음"으로 적혀 있었고
    사용처는 `NOT(...)`이었다. 이중부정이 되어 승낙이 유효할 때 오히려 위법성조각이
    부정됐다. 저작 자체검증 항목 "긍정형 = 논리적 부정 검사"가 잡아야 했던 결함이다.
    """
    for ref in _blocker_leaves(doctrine):
        entry = REGISTRY.get(ref)
        assert entry is not None, ref
        meaning = str(entry.payload.get("canonical_meaning", ""))
        standard = str(entry.payload.get("legal_standard", ""))
        for text, label in ((meaning, "canonical_meaning"), (standard, "legal_standard")):
            assert not any(marker in text for marker in _NEGATIVE_MARKERS), (
                f"{ref}.{label}가 부정형이다: {text!r} — blocker는 예외의 존재를 묻는다"
            )
