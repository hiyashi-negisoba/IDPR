"""Call 1.5-D 사실 단서 카탈로그와 입출력 계약."""

from pathlib import Path

import pytest

from idpr.v2 import expressions
from idpr.v2.doctrine_cues import (
    ACTOR_SCOPE,
    EPISODE_SCOPE,
    DoctrineCueAssessment,
    DoctrineCueError,
    cue_request_payload,
    load_doctrine_cues,
    representation_gap_doctrine_refs,
    unaccounted_doctrine_refs,
    validate_cue_output,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.doctrine_raising import raise_doctrines, raised_refs_by_actor_episode

CATALOG = Path("data/v2/doctrine_raising_cues.yaml")
EPISODE_TEXT = "甲은 술에 만취한 상태에서 乙의 멱살을 잡았다. 乙은 이를 뿌리쳤다."


@pytest.fixture(scope="module")
def cues():
    return load_doctrine_cues(CATALOG)


@pytest.fixture(scope="module")
def cues_all():
    return load_doctrine_cues(CATALOG, include_representation_gaps=True)


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def _assessment(cue_id, truth="TRUE", subjects=("甲",), quote="甲은 술에 만취한 상태에서"):
    return DoctrineCueAssessment(
        case_id="case",
        factual_episode_id="factual_episode:001",
        cue_id=cue_id,
        truth=truth,
        subject_actor_ids=tuple(subjects),
        source_quote=quote,
    )


def test_every_authored_doctrine_is_accounted_for(cues_all, registry) -> None:
    """제기 경로가 있거나, 명시된 표현 공백이거나. 둘 중 어느 쪽도 아니면 조용히 잠긴다.

    "모든 doctrine에 제기 경로가 있어야 한다"는 절대조건이 아니다. 사실 층이 그 법리를
    안정적으로 가려낼 수 없으면 공백으로 남기는 것이 옳다. 금지되는 것은 아무도 모르게
    잠기는 상태다.
    """
    refs = [entry.id for entry in registry.by_kind.get("doctrine", ())]
    assert unaccounted_doctrine_refs(cues_all, refs) == ()


def test_the_justifying_premise_cue_is_withdrawn_from_production(cues, cues_all) -> None:
    """두 번 좁혔는데도 객체 동일성 착오를 잡았고, 실제로 target 8개를 열었다."""
    assert "cue.justifying_premise_belief_mismatch_stated" not in {
        cue.cue_id for cue in cues
    }
    withdrawn = [
        cue
        for cue in cues_all
        if cue.cue_id == "cue.justifying_premise_belief_mismatch_stated"
    ]
    assert len(withdrawn) == 1
    assert withdrawn[0].gap_reason
    assert representation_gap_doctrine_refs(cues_all) == (
        "doctrine.mistaken_justifying_circumstance",
    )


def test_every_raised_doctrine_ref_exists_and_has_leaves(cues_all, registry) -> None:
    for cue in cues_all:
        for ref in cue.raises:
            entry = registry.get(ref)
            assert entry is not None and entry.kind == "doctrine", ref
            assert expressions.leaf_refs(entry.payload["requires"]), ref


def test_persistent_and_transient_mental_states_are_separate_cues(cues) -> None:
    """episode 1의 만취가 episode 7의 별개 범행까지 번지면 안 된다."""
    by_id = {cue.cue_id: cue for cue in cues}
    assert by_id["cue.actor_persistent_mental_disorder_stated"].scope == ACTOR_SCOPE
    assert by_id["cue.actor_transient_intoxication_stated"].scope == EPISODE_SCOPE
    # 두 cue는 같은 doctrine을 연다. 다른 것은 미치는 범위뿐이다.
    assert by_id["cue.actor_persistent_mental_disorder_stated"].raises == (
        "doctrine.insanity_defeat",
    )
    assert by_id["cue.actor_transient_intoxication_stated"].raises == (
        "doctrine.insanity_defeat",
    )


def test_only_actor_status_cues_are_actor_scoped(cues) -> None:
    actor_scoped = {cue.cue_id for cue in cues if cue.scope == ACTOR_SCOPE}
    assert actor_scoped == {
        "cue.actor_age_stated",
        "cue.actor_persistent_mental_disorder_stated",
        "cue.actor_hearing_or_speech_impairment_stated",
    }


def test_the_request_payload_never_leaks_a_doctrine_name(cues) -> None:
    payload = cue_request_payload(
        case_id="case",
        factual_episode_id="factual_episode:001",
        episode_text=EPISODE_TEXT,
        actor_labels=("甲", "乙"),
        cues=cues,
    )
    serialized = repr(payload)
    assert "doctrine" not in serialized
    assert "scope" not in serialized
    assert "형법" not in serialized
    assert {value["cue_id"] for value in payload["cues"]} == {cue.cue_id for cue in cues}


def test_a_missing_cue_in_the_output_is_fatal(cues) -> None:
    raw = {
        "factual_episode_id": "factual_episode:001",
        "cue_assessments": [
            {
                "cue_id": cue.cue_id,
                "truth": "FALSE",
                "subject_actor_ids": [],
                "source_quote": "",
            }
            for cue in cues[:-1]
        ],
    }
    with pytest.raises(DoctrineCueError, match="cue set must match exactly"):
        validate_cue_output(
            raw,
            case_id="case",
            factual_episode_id="factual_episode:001",
            episode_text=EPISODE_TEXT,
            actor_labels=("甲", "乙"),
            cues=cues,
        )


def test_a_true_cue_without_a_real_quote_is_rejected(cues) -> None:
    raw = {
        "factual_episode_id": "factual_episode:001",
        "cue_assessments": [
            {
                "cue_id": cue.cue_id,
                "truth": "TRUE" if cue.cue_id == cues[0].cue_id else "FALSE",
                "subject_actor_ids": ["甲"] if cue.cue_id == cues[0].cue_id else [],
                "source_quote": "원문에 없는 문장" if cue.cue_id == cues[0].cue_id else "",
            }
            for cue in cues
        ],
    }
    with pytest.raises(DoctrineCueError, match="not a substring"):
        validate_cue_output(
            raw,
            case_id="case",
            factual_episode_id="factual_episode:001",
            episode_text=EPISODE_TEXT,
            actor_labels=("甲", "乙"),
            cues=cues,
        )


def test_an_actor_outside_the_episode_universe_is_rejected(cues) -> None:
    raw = {
        "factual_episode_id": "factual_episode:001",
        "cue_assessments": [
            {
                "cue_id": cue.cue_id,
                "truth": "FALSE",
                "subject_actor_ids": ["丙"] if cue.cue_id == cues[0].cue_id else [],
                "source_quote": "",
            }
            for cue in cues
        ],
    }
    with pytest.raises(DoctrineCueError, match="outside the episode actor universe"):
        validate_cue_output(
            raw,
            case_id="case",
            factual_episode_id="factual_episode:001",
            episode_text=EPISODE_TEXT,
            actor_labels=("甲", "乙"),
            cues=cues,
        )


def test_a_true_cue_without_a_subject_raises_nothing(cues) -> None:
    """주체를 모르는 TRUE로 doctrine을 열면 甲의 심신장애가 乙의 죄책을 흔든다."""
    raised = raise_doctrines(
        (_assessment("cue.actor_transient_intoxication_stated", subjects=()),),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001",)},
    )
    assert raised == ()


def test_unknown_is_not_raised_and_not_denied(cues) -> None:
    raised = raise_doctrines(
        (_assessment("cue.actor_transient_intoxication_stated", truth="UNKNOWN"),),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001",)},
    )
    assert raised == ()


def test_an_episode_cue_stays_in_its_episode(cues) -> None:
    raised = raise_doctrines(
        (_assessment("cue.actor_transient_intoxication_stated"),),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001", "factual_episode:007")},
    )
    assert [value.target_episode_id for value in raised] == ["factual_episode:001"]
    assert not raised[0].is_projected


def test_an_actor_cue_projects_across_episodes_and_keeps_its_source(cues) -> None:
    raised = raise_doctrines(
        (_assessment("cue.actor_age_stated"),),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001", "factual_episode:007")},
    )
    assert {value.target_episode_id for value in raised} == {
        "factual_episode:001",
        "factual_episode:007",
    }
    projected = [value for value in raised if value.target_episode_id == "factual_episode:007"]
    assert projected[0].source_episode_id == "factual_episode:001"
    assert projected[0].is_projected


def test_the_planner_join_key_groups_by_actor_and_episode(cues) -> None:
    raised = raise_doctrines(
        (
            _assessment("cue.actor_transient_intoxication_stated"),
            _assessment("cue.prior_force_by_other_stated", quote="乙은 이를 뿌리쳤다"),
        ),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001",)},
    )
    grouped = raised_refs_by_actor_episode(raised)
    assert grouped[("case", "甲", "factual_episode:001")] == (
        "doctrine.insanity_defeat",
        "doctrine.self_defense",
    )


def test_the_schema_pins_the_episode_identifier(cues) -> None:
    """첫 실행 43/43 실패의 원인. 모델이 `factual_episode:001`을 `:001`로 되돌려 주었다."""
    from idpr.v2.doctrine_cues import cue_output_schema

    schema = cue_output_schema(cues, ("甲",), factual_episode_id="factual_episode:001")
    assert schema["properties"]["factual_episode_id"] == {"const": "factual_episode:001"}


def test_an_unapproved_catalog_cannot_be_loaded(tmp_path) -> None:
    path = tmp_path / "cues.yaml"
    path.write_text(
        "version: 1\nstatus: draft\ncues:\n"
        "  - id: cue.x\n    scope: episode\n    factual_cue: 'x'\n    raises: [doctrine.y]\n",
        encoding="utf-8",
    )
    with pytest.raises(DoctrineCueError, match="not approved"):
        load_doctrine_cues(path)


def test_the_canonical_episode_text_is_what_validation_sees() -> None:
    """모델 출력을 사후 보정하지 않는다. 대신 prompt와 검증이 같은 문자열을 본다."""
    from idpr.v2.doctrine_cues import canonical_episode_text

    text = canonical_episode_text(("丙은 당연히 乙의\n카드로", " 생각하고  "))
    assert text == "丙은 당연히 乙의 카드로 생각하고"
    assert "\n" not in text


def test_a_raising_without_a_matching_legal_instance_is_not_materialized(cues) -> None:
    """강요된행위 cue가 강제추행 피해자 A를 주체로 TRUE를 낸 사안.

    프롬프트를 더 조이는 대신 host가 아는 typed 구조로 막는다. A에게는 이 사건에서 평가되는
    instance가 없으므로 적용할 법리도 없다. 원문의 의미를 다시 읽는 것이 아니라 identity
    check다.
    """
    from idpr.v2.runtime.doctrine_targets import (
        NOT_MATERIALIZED,
        materialize_doctrine_leaf_targets,
    )
    from idpr.v2.runtime.identity import OffenseInstanceKey

    raised = raise_doctrines(
        (
            _assessment(
                "cue.coercion_against_actor_stated",
                subjects=("A",),
                quote="甲은 술에 만취한 상태에서",
            ),
        ),
        cues=cues,
        episode_ids_by_case={"case": ("factual_episode:001",)},
    )
    assert raised, "cue TRUE는 후보를 만든다"
    instance = OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "binding:001")
    targets, blocked = materialize_doctrine_leaf_targets(
        raised,
        instances=((instance, "factual_episode:001"),),
        leaves_by_doctrine={"doctrine.coerced_act_defeat": ("legal_element.irresistible_coercion",)},
    )
    assert targets == ()
    assert [value.status for value in blocked] == [NOT_MATERIALIZED]
    # 후보 자체는 지우지 않는다. raw assessment와 대조할 수 있어야 한다.
    assert blocked[0].raised.actor_id == "A"
