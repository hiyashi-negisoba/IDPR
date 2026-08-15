"""계획된 target은 Call 2까지 도달하거나, 도달하지 못한 이유가 있어야 한다.

축별 테스트는 각 단계 안에서는 초록이었는데 단계 사이에서 target이 사라졌다. planner는
`instigator_intent`를 열고 carrier까지 붙였지만 scheduler가 자기 후보 universe(슬롯 +
completion `when`/`requires`)와 교집합을 내면서 그것을 지웠다. 아무도 묻지 않은 사실은
Kleene에서 UNKNOWN이므로, 참가 축에서 고친 "교사범은 어떤 사건에서도 성립할 수 없다"가
scheduler에서 그대로 재현될 수 있었다.

여기서 고정하는 것은 하나다 -- **scheduling은 planner의 target을 줄이기만 하고, 줄일 때는
이 모듈이 소유한 표현식으로 그 이유를 댈 수 있어야 한다.** 표현식이 없는 target은 무의미한
것이 아니라 이 모듈이 모르는 것이고, 모르는 것은 지우지 않는다.

표현식이 **있는** 경우도 그것만으로 부족하다. 한 predicate를 이 죄의 요소로도 쓰고 doctrine이
따로 열기도 하면 scheduler에게는 같은 ref 하나이고, 이 죄가 더 이상 그것을 필요로 하지 않게
된 순간 지워진다. 그 판단은 이 죄에 대해서만 옳다. 그래서 개방 이유를 함께 넘긴다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import expressions
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime.doctrine_raising import RaisedDoctrine
from idpr.v2.runtime.doctrine_targets import (
    materialize_doctrine_leaf_targets,
    merge_reused_openers,
)
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.target_scheduling import (
    ALSO_OPENED_BY_KEY,
    ELEMENT_DERIVED_OPENERS,
    frontier_predicate_refs,
    is_externally_opened,
    live_predicate_refs,
    merge_target_opener,
    next_round_targets,
    target_openers,
)

DEFINITIONS = Path(__file__).resolve().parents[1] / "data/v2/definitions"

HOMICIDE = "offense.homicide"
POLICY = "completion_policy.homicide"
DEFECT = "ground_fact.means_or_object_defect"
COMMENCEMENT = "legal_element.commencement_of_execution"

#: planner가 참가 mode의 `requires`에서 여는 target. 어떤 죄의 슬롯에도, 어떤 completion
#: policy에도 나오지 않는다 -- scheduler가 모델링하지 않는 종류의 target의 실례다.
INSTIGATOR_INTENT = "legal_element.instigator_intent"
AIDING_INTENT = "legal_element.aiding_intent"


@pytest.fixture(scope="module")
def registry():
    return load_definitions(DEFINITIONS)


def instance(offense_ref: str = HOMICIDE) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        case_id="case", actor_id="甲", offense_ref=offense_ref, occurrence_id="binding:001"
    )


def _modelled_refs(registry) -> set[str]:
    """이 죄에 대해 scheduler가 표현식을 소유한 predicate 전부."""
    refs: set[str] = set()
    offense = registry.get(HOMICIDE)
    for slot in expressions.SLOT_NAMES:
        refs |= set(expressions.leaf_refs((offense.payload.get("elements") or {}).get(slot)))
    policy = registry.get(POLICY)
    for state in (policy.payload.get("states") or {}).values():
        for field in ("when", "requires", "blocked_when"):
            refs |= set(expressions.leaf_refs(state.get(field)))
    return refs


def test_a_planner_target_with_no_expression_here_is_still_asked(registry):
    """참가 mode의 요구사실은 planner만 아는 target이다. scheduler는 그것을 지우지 않는다."""
    planned = {COMMENCEMENT, INSTIGATOR_INTENT, AIDING_INTENT}
    assert INSTIGATOR_INTENT not in _modelled_refs(registry)

    live = live_predicate_refs(registry, instance(), {}, candidate_refs=planned)
    frontier = frontier_predicate_refs(registry, instance(), {}, candidate_refs=planned)
    assert INSTIGATOR_INTENT in live and AIDING_INTENT in live
    assert INSTIGATOR_INTENT in frontier and AIDING_INTENT in frontier


def test_an_unmodelled_target_is_asked_once_and_not_again(registry):
    """물었는데 답이 오지 않아도 같은 target을 영원히 다시 묻지 않는다."""
    planned = {INSTIGATOR_INTENT}
    key = instance()
    first = next_round_targets(
        registry, (key,), {}, candidate_refs={key: planned}
    )
    assert first == ((key, INSTIGATOR_INTENT),)
    second = next_round_targets(
        registry,
        (key,),
        {},
        already_asked={key: {INSTIGATOR_INTENT}},
        candidate_refs={key: planned},
    )
    assert second == ()


def test_every_planned_target_is_asked_or_moot_for_a_stated_reason(registry):
    """전수 회계: 계획된 것은 물어지거나, 모델링된 표현식이 무의미하다고 말한 것이다.

    이것이 이 파일의 종료 증명이다. Call 2가 target을 버릴 수 있는 유일한 경로가
    "이 모듈의 표현식이 어떤 답에도 같은 값을 낸다"임을 고정한다.
    """
    key = instance()
    modelled = _modelled_refs(registry)
    planned = modelled | {INSTIGATOR_INTENT, AIDING_INTENT}

    asked: set[str] = set()
    for _ in range(20):
        batch = next_round_targets(
            registry,
            (key,),
            {},
            already_asked={key: asked},
            candidate_refs={key: planned},
        )
        if not batch:
            break
        # Call 2가 답을 주지 않은 최악의 경우를 가정한다 -- truths는 비운 채로 둔다.
        asked |= {ref for _instance, ref in batch}
    else:
        pytest.fail("scheduling did not reach a fixpoint")

    dropped = planned - asked
    live_at_start = set(live_predicate_refs(registry, key, {}, candidate_refs=planned))
    assert dropped.isdisjoint(live_at_start), (
        f"planned targets vanished without a reason: {sorted(dropped & live_at_start)}"
    )
    assert {INSTIGATOR_INTENT, AIDING_INTENT} <= asked


def _registry_with_blocker_only_predicate(registry) -> tuple[DefinitionRegistry, str]:
    """`blocked_when`에만 나오는 predicate를 가진 완성정책으로 registry를 갈아 끼운다.

    현재 저작에는 그런 predicate가 없다 -- 모든 blocker가 다른 곳에도 나온다. 그래서 이
    결함은 아직 물리지 않았고, 물리는 날 조용히 fail-open한다: 묻지 않은 blocker는 UNKNOWN,
    UNKNOWN인 blocker는 아무것도 막지 않는다.
    """
    blocker = "ground_fact.coerced_act_performed"
    assert registry.get(blocker) is not None
    assert blocker not in _modelled_refs(registry)
    policy = registry.get(POLICY)
    states = {
        name: (
            {**state, "blocked_when": {"op": "ref", "ref": blocker}}
            if name == "attempted"
            else state
        )
        for name, state in policy.payload["states"].items()
    }
    patched = DefinitionEntry(
        policy.id, policy.kind, {**policy.payload, "states": states}, policy.source_file
    )
    by_id = {**registry.by_id, patched.id: patched}
    by_kind = {
        kind: tuple(patched if value.id == patched.id else value for value in values)
        for kind, values in registry.by_kind.items()
    }
    return DefinitionRegistry(by_id, by_kind), blocker


def test_a_blocker_is_a_question_this_case_has_to_be_asked(registry):
    """`blocked_when`은 TRUE일 때만 막는다. 묻지 않으면 영원히 UNKNOWN이고 fail-open이다."""
    patched, blocker = _registry_with_blocker_only_predicate(registry)
    settled = {COMMENCEMENT: TRUE, DEFECT: FALSE}
    assert blocker in live_predicate_refs(patched, instance(), settled)
    assert blocker in frontier_predicate_refs(patched, instance(), settled)


def test_a_blocker_of_a_dead_state_is_not_asked(registry):
    """상태가 이미 죽었으면 그 상태를 무엇이 막는지는 이 사건의 질문이 아니다."""
    patched, blocker = _registry_with_blocker_only_predicate(registry)
    guard_dead = {
        ref: FALSE
        for ref in expressions.leaf_refs(
            patched.get(POLICY).payload["states"]["attempted"].get("when")
        )
    }
    assert blocker not in live_predicate_refs(patched, instance(), guard_dead)


def test_scheduling_never_widens_beyond_the_planner(registry):
    """계약의 반대 방향. planner가 열지 않은 것을 scheduler가 물어서는 안 된다."""
    planned = {COMMENCEMENT}
    for value in frontier_predicate_refs(
        registry, instance(), {}, candidate_refs=planned
    ):
        assert value in planned
    assert UNKNOWN  # 세 값 논리를 쓰는 모듈임을 명시한다


# --------------------------------------------------------------------------
# 겹치는 경우: 이 offense도 쓰고, 외부 producer도 연 predicate
# --------------------------------------------------------------------------

DANGEROUSNESS = "legal_element.dangerousness"


def _raised(key: OffenseInstanceKey, doctrine_ref: str) -> RaisedDoctrine:
    return RaisedDoctrine(
        case_id=key.case_id,
        actor_id=key.actor_id,
        target_episode_id="factual_episode:001",
        doctrine_ref=doctrine_ref,
        scope="episode",
        source_episode_id="factual_episode:001",
        raised_by_cue_id="cue.made_up",
        source_quote="시험용",
    )


def test_an_externally_opened_ref_survives_this_offense_losing_interest(registry) -> None:
    """같은 ref를 offense/completion도 쓰고 doctrine도 쓸 수 있다.

    그러면 scheduler에게는 그냥 하나의 ref이고, 이 offense에서 더 이상 결정적이지 않다는
    이유로 지울 수 있다. 그 판단은 offense에 대해서만 옳다 -- 그 ref를 함께 연 doctrine은
    여전히 답을 필요로 하고, 아무도 그쪽에 묻지 않았다. 개방 이유를 버린 채 pruning하면
    묻지 않은 producer를 대신해 답하는 일이 된다.
    """
    key = instance()
    settled = {COMMENCEMENT: TRUE, DEFECT: FALSE}
    planned = {DANGEROUSNESS}

    # 이 offense만 보면 죽은 target이 맞다. 그래서 평소에는 묻지 않는다.
    assert DANGEROUSNESS in _modelled_refs(registry)
    assert frontier_predicate_refs(
        registry, key, settled, candidate_refs=planned
    ) == ()

    # doctrine이 같은 ref를 열었다면 그 이유는 아직 살아 있다.
    assert DANGEROUSNESS in frontier_predicate_refs(
        registry, key, settled, candidate_refs=planned, external_refs=planned
    )
    assert DANGEROUSNESS in live_predicate_refs(
        registry, key, settled, candidate_refs=planned, external_refs=planned
    )
    assert next_round_targets(
        registry,
        (key,),
        {key: settled},
        candidate_refs={key: planned},
        external_refs={key: planned},
    ) == ((key, DANGEROUSNESS),)


def test_an_unknown_opener_is_protected_before_anyone_registers_it(registry) -> None:
    """기본값이 방어 쪽이다. 새 producer는 이 목록에 이름을 올리기 전부터 보호된다.

    옛 코드의 실패 형태가 정확히 "이 모듈이 들어 본 적 없는 producer"였다. 목록에 없는
    opener를 prunable로 두면 같은 사고가 새 producer마다 한 번씩 반복된다.
    """
    assert "doctrine_raising_cue" not in ELEMENT_DERIVED_OPENERS
    assert "participation_mode_requirement" not in ELEMENT_DERIVED_OPENERS
    assert "a_producer_that_does_not_exist_yet" not in ELEMENT_DERIVED_OPENERS
    # 기본 planner의 일반 요소 target만 pruning 대상이다.
    assert {"", "unspecified"} <= ELEMENT_DERIVED_OPENERS


def test_the_call2_runner_keeps_the_opener_when_it_calls_the_scheduler(registry) -> None:
    """계약은 runner가 개방 이유를 실제로 넘길 때만 성립한다."""
    source = (
        Path(__file__).resolve().parents[1] / "scripts/run_v2_call2_pilot.py"
    ).read_text(encoding="utf-8")
    assert "external_refs=external_refs" in source
    # 판정 규칙은 runtime이 소유한다. runner가 자기 코드로 opener를 분류하면 그것이 두 번째
    # 권위가 되고, 재사용 target의 opener 병합 같은 수정이 한쪽에만 반영된다.
    assert "is_externally_opened(" in source
    assert "target_openers(" in source


def test_a_doctrine_reusing_an_element_target_keeps_its_reason(registry) -> None:
    """producer → plan 행 → runner → scheduler 관통.

    doctrine이 필요로 하는 leaf가 마침 그 죄의 일반 요소이기도 하면 새 행을 만들 이유가
    없다. 그런데 행을 만들지 않으면서 이유까지 버리면 행에는 `unspecified` 하나만 남고,
    scheduler는 죄 쪽 사정만 보고 지워도 된다고 판단한다 -- 개방 이유를 넘기기로 한 수정이
    producer 쪽에서 무효가 되는 자리다.

    그래서 여기서는 scheduler에 external을 주입하지 않는다. doctrine 빌더가 쓴 행에서
    runner가 실제로 그것을 읽어 내는지까지 간다.
    """
    key = instance()
    raised = (_raised(key, "doctrine.made_up_for_this_test"),)
    # 이 죄의 일반 요소가 이미 열려 있다. 그리고 이 doctrine의 leaf가 바로 그것이다.
    row = {
        "assessment_targets": [
            {
                "instance_key": {
                    "case_id": key.case_id,
                    "actor_id": key.actor_id,
                    "offense_ref": key.offense_ref,
                    "occurrence_id": key.occurrence_id,
                },
                "predicate_ref": DANGEROUSNESS,
            }
        ]
    }
    existing = [(key, DANGEROUSNESS)]
    materialized, _unmaterialized = materialize_doctrine_leaf_targets(
        raised,
        instances=((key, "factual_episode:001"),),
        leaves_by_doctrine={"doctrine.made_up_for_this_test": (DANGEROUSNESS,)},
        existing_targets=existing,
    )
    assert [value.reuses_existing_target for value in materialized] == [True], (
        "재사용은 결과에서 빠지지 않는다 -- 빠지면 호출자가 병합할 것이 없다"
    )
    assert merge_reused_openers(row["assessment_targets"], materialized) == 1

    # runner가 읽는 자리. 하나만 읽으면 여기서 element-derived로 보인다.
    raw_target = row["assessment_targets"][0]
    assert target_openers(raw_target) == frozenset(
        {"unspecified", "doctrine_raising_cue"}
    )
    assert is_externally_opened(raw_target)

    # 그리고 그 결과가 scheduling까지 간다. 이 죄만 보면 죽은 target이다.
    settled = {COMMENCEMENT: TRUE, DEFECT: FALSE}
    planned = {DANGEROUSNESS}
    assert frontier_predicate_refs(
        registry, key, settled, candidate_refs=planned
    ) == ()
    external = {key: {DANGEROUSNESS}} if is_externally_opened(raw_target) else {}
    assert next_round_targets(
        registry,
        (key,),
        {key: settled},
        candidate_refs={key: planned},
        external_refs=external,
    ) == ((key, DANGEROUSNESS),)


def test_two_doctrines_needing_one_leaf_do_not_duplicate_the_row(registry) -> None:
    """같은 leaf를 두 doctrine이 요구해도 행은 하나다.

    행이 둘 생기면 carrier는 하나뿐이라 plan이 carrier 계약 위반으로 거부된다.
    """
    key = instance()
    raised = tuple(
        _raised(key, ref) for ref in ("doctrine.first", "doctrine.second")
    )
    materialized, _ = materialize_doctrine_leaf_targets(
        raised,
        instances=((key, "factual_episode:001"),),
        leaves_by_doctrine={
            "doctrine.first": (DANGEROUSNESS,),
            "doctrine.second": (DANGEROUSNESS,),
        },
    )
    assert [value.reuses_existing_target for value in materialized] == [False, True]


def test_a_participation_requirement_reusing_an_element_target_keeps_its_reason(
    registry,
) -> None:
    """참가 빌더도 같은 계약을 진다. producer마다 다시 새지 않는다.

    교사·방조가 요구하는 요소가 마침 그 죄의 일반 요소이기도 하면 참가 빌더도 기존 target을
    재사용한다. doctrine 쪽에서 닫은 것과 **같은** 구멍이므로 규칙도 같은 곳이 소유한다.
    """
    key = instance()
    raw_target = {
        "instance_key": {
            "case_id": key.case_id,
            "actor_id": key.actor_id,
            "offense_ref": key.offense_ref,
            "occurrence_id": key.occurrence_id,
        },
        "predicate_ref": DANGEROUSNESS,
    }
    assert merge_target_opener(raw_target, "participation_mode_requirement")
    assert not merge_target_opener(raw_target, "participation_mode_requirement")
    assert target_openers(raw_target) == frozenset(
        {"unspecified", "participation_mode_requirement"}
    )
    assert is_externally_opened(raw_target)


def test_the_participation_builder_merges_instead_of_dropping_the_opener() -> None:
    """재사용을 `continue` 한 줄로 처리한 producer가 둘 있었고 둘 다 같은 구멍이었다.

    `post_participation_derived_group`만 예외다 -- 그 opener가 여는 것은 파생 group 위의 일반
    구성요건이고, 그 필요를 표현하는 것이 offense/completion 표현식 그 자체이므로 scheduler가
    모르는 별도 요구를 싣지 않는다.
    """
    source = (
        Path(__file__).resolve().parents[1]
        / "scripts/build_v2_factual_participation_plan.py"
    ).read_text(encoding="utf-8")
    assert "merge_target_opener(row_by_target[key], opened_by)" in source


def test_the_opener_merge_rule_has_exactly_one_owner() -> None:
    """같은 불변식이 producer마다 흩어지면 한 곳을 고쳐도 다른 곳으로 전달되지 않는다."""
    root = Path(__file__).resolve().parents[1]
    writers = [
        path
        for path in (root / "scripts").glob("build_v2_*.py")
        if ALSO_OPENED_BY_KEY in path.read_text(encoding="utf-8")
    ]
    assert writers == [], (
        "opener 병합은 target_scheduling이 소유한다 -- producer가 그 키를 직접 쓰면 "
        f"두 번째 권위가 된다: {[p.name for p in writers]}"
    )
