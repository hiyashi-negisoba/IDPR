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
    unraisable_doctrine_refs,
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


def test_every_authored_doctrine_has_a_raising_path(cues, registry) -> None:
    """단서 없는 doctrine은 정의도 런타임도 있는 채로 영원히 잠긴다."""
    refs = [entry.id for entry in registry.by_kind.get("doctrine", ())]
    assert unraisable_doctrine_refs(cues, refs) == ()


def test_every_raised_doctrine_ref_exists_and_has_leaves(cues, registry) -> None:
    for cue in cues:
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
