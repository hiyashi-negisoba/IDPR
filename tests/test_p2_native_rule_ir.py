from __future__ import annotations

from typing import Any

import pytest

from scripts.build_p2_native_decision_ledger import build_ledger
from scripts.build_p2_native_rule_ir import UnitAssembler, commentary_index

from idpr.rulegen import compile_rule_ir


UNIT = "arson_of_occupied_structure"


def assembled() -> tuple[dict, dict]:
    return UnitAssembler(UNIT, None).build()


def test_only_the_gate_approved_tracks_are_compiled() -> None:
    assembler = UnitAssembler(UNIT, None)
    rule_ir, _ = assembler.build()
    assert set(assembler.tracks) == {"base", "attempt", "completed"}
    deferred = [gap for gap in rule_ir["coverage_gaps"] if gap.startswith("track_deferred")]
    assert deferred, "the deferred aggravated-result track must stay visible"


def test_a_bar_card_never_joins_the_element_it_qualifies() -> None:
    """A component may hold a defining card, a bar and a boundary at once."""
    assembler = UnitAssembler(UNIT, None)
    compiled = set(assembler.tracks)
    rows = [
        row for row in assembler.ledger["placements"]
        if row["track_id"] in compiled
    ]
    by_component: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        key = (row["track_id"], row["component_id"])
        by_component.setdefault(key, set()).add(row["role"])
    mixed = [key for key, roles in by_component.items() if len(roles) > 1]
    assert mixed, "the arson approval mixes roles on at least one element"

    rule_ir, _ = assembled()
    blocked_cards = {
        rule["norm_card_ids"][0]
        for rule in rule_ir["rules"]
        if rule["head"]["predicate"].endswith("_track_not_established")
    }
    component_cards = {row["card_id"] for row in rows if row["role"] == "component"}
    bar_cards = {row["card_id"] for row in rows if row["role"] in ("bar", "boundary")}
    assert blocked_cards == bar_cards
    assert not (blocked_cards & (component_cards - bar_cards))


def test_every_rule_names_the_cards_it_came_from() -> None:
    rule_ir, _ = assembled()
    for rule in rule_ir["rules"]:
        assert rule["norm_card_ids"], rule["id"]
        assert rule["source_refs"], rule["id"]


def test_the_repository_unit_compiles_to_scallop() -> None:
    rule_ir, card_set = assembled()
    program = compile_rule_ir(rule_ir, commentary_index(["art164", "art250"]), card_set)
    for track in ("base", "attempt", "completed"):
        assert f"type {UNIT}_{track}_established(" in program
    assert f"type {UNIT}_not_established(" in program


def test_role_tuple_comes_from_the_declared_signature_not_from_code() -> None:
    assembler = UnitAssembler(UNIT, None)
    assert assembler.roles[0] == "case_id"
    rule_ir, _ = assembler.build()
    roles = next(
        item for item in rule_ir["predicates"]
        if item["id"] == assembler.signature["predicate"]
    )
    assert [argument["name"] for argument in roles["arguments"]] == assembler.roles


BODILY_INJURY = "intentional_bodily_injury"


def test_a_gaining_track_requires_the_base_track_it_inherits() -> None:
    """존속·특수·상해치사는 기본 구성요건을 그대로 요구한다."""
    rule_ir, _ = UnitAssembler(BODILY_INJURY, None).build()
    base_elements = f"{BODILY_INJURY}_base_elements_satisfied"
    for track in ("ancestral", "special", "aggravated_result"):
        rule = next(item for item in rule_ir["rules"]
                    if item["id"] == f"{BODILY_INJURY}.outcome.{track}.elements_satisfied")
        body = [atom["predicate"] for atom in rule["body"]]
        assert base_elements in body, track
        assert any(name.startswith(f"{BODILY_INJURY}_{track}_") for name in body), track


def test_the_base_track_does_not_inherit_anything() -> None:
    rule_ir, _ = UnitAssembler(BODILY_INJURY, None).build()
    rule = next(item for item in rule_ir["rules"]
                if item["id"] == f"{BODILY_INJURY}.outcome.base.elements_satisfied")
    body = [atom["predicate"] for atom in rule["body"]]
    assert not any(name.endswith("_elements_satisfied") for name in body)


def test_a_track_needing_extra_roles_is_declared_but_not_compiled() -> None:
    """제263조 동시범 특례는 2인 이상의 역할이 필요하므로 이번 회차에서 컴파일하지 않는다."""
    assembler = UnitAssembler(BODILY_INJURY, None)
    rule_ir, _ = assembler.build()
    assert "concurrent_offenders" not in assembler.tracks
    deferred = [gap for gap in rule_ir["coverage_gaps"]
                if gap.startswith("track_deferred: concurrent_offenders")]
    assert deferred, "이관 대상 track은 gap으로 계속 보여야 한다"


def test_the_bodily_injury_unit_compiles_to_scallop() -> None:
    rule_ir, card_set = UnitAssembler(BODILY_INJURY, None).build()
    program = compile_rule_ir(
        rule_ir, commentary_index(["art257", "art2582_2", "art259", "art263"]), card_set)
    for track in ("base", "attempt", "ancestral", "special", "aggravated_result"):
        assert f"type {BODILY_INJURY}_{track}_established(" in program
    assert "type bodily_injury_case_roles(String, String, String)" in program


HOMICIDE = "homicide"


def test_homicide_omission_and_attempt_inherit_only_declared_common_placements() -> None:
    rule_ir, _ = UnitAssembler(HOMICIDE, None).build()
    omission = next(rule for rule in rule_ir["rules"]
                    if rule["id"] == f"{HOMICIDE}.outcome.omission.elements_satisfied")
    omission_body = {item["predicate"] for item in omission["body"]}
    assert f"{HOMICIDE}_base_object_scope_satisfied" in omission_body
    assert f"{HOMICIDE}_base_death_result_satisfied" in omission_body
    assert f"{HOMICIDE}_base_murder_intent_satisfied" not in omission_body
    assert f"{HOMICIDE}_base_causation_satisfied" not in omission_body

    attempt = next(rule for rule in rule_ir["rules"]
                   if rule["id"] == f"{HOMICIDE}.outcome.attempt.elements_satisfied")
    attempt_body = {item["predicate"] for item in attempt["body"]}
    assert f"{HOMICIDE}_base_object_scope_satisfied" in attempt_body
    assert f"{HOMICIDE}_base_murder_intent_satisfied" in attempt_body
    assert f"{HOMICIDE}_base_death_result_satisfied" not in attempt_body
    assert f"{HOMICIDE}_base_causation_satisfied" not in attempt_body


def test_homicide_child_track_bar_does_not_block_its_parent() -> None:
    assembler = UnitAssembler(HOMICIDE, None)
    rule_ir, _ = assembler.build()
    ledger = build_ledger(HOMICIDE)
    parricide_bar = next(row for row in ledger["placements"]
                         if row["track_id"] == "parricide" and row["role"] == "bar")
    rules = [rule for rule in rule_ir["rules"]
             if rule["head"]["predicate"] == assembler.track_not_established
             and parricide_bar["card_id"] in rule["norm_card_ids"]]
    target_tracks = {rule["head"]["arguments"][2]["value"] for rule in rules}
    assert "parricide" in target_tracks
    assert "base" not in target_tracks


def test_homicide_voluntary_desistance_bar_does_not_block_plain_attempt() -> None:
    assembler = UnitAssembler(HOMICIDE, None)
    rule_ir, _ = assembler.build()
    ledger = build_ledger(HOMICIDE)
    desistance_bar = next(row for row in ledger["placements"]
                          if row["track_id"] == "voluntary_desistance"
                          and row["role"] == "bar")
    rules = [rule for rule in rule_ir["rules"]
             if rule["head"]["predicate"] == assembler.track_not_established
             and desistance_bar["card_id"] in rule["norm_card_ids"]]
    target_tracks = {rule["head"]["arguments"][2]["value"] for rule in rules}
    assert "voluntary_desistance" in target_tracks
    assert "attempt" not in target_tracks


def test_homicide_attempt_children_transitively_receive_selective_base_placements() -> None:
    assembler = UnitAssembler(HOMICIDE, None)
    ledger = build_ledger(HOMICIDE)
    intent = next(row for row in ledger["placements"]
                  if row["track_id"] == "base"
                  and row["component_id"] == "murder_intent"
                  and row["role"] == "component")
    death = next(row for row in ledger["placements"]
                 if row["track_id"] == "base"
                 and row["component_id"] == "death_result"
                 and row["role"] == "component")

    for child in ("voluntary_desistance", "impossible_attempt"):
        assert assembler.placement_applies_to_track(intent, child)
        assert not assembler.placement_applies_to_track(death, child)


NEGLIGENT_BODILY_HARM = "negligent_bodily_harm"


def test_negligent_bodily_harm_repairs_quotes_to_exact_source_spans() -> None:
    assembler = UnitAssembler(NEGLIGENT_BODILY_HARM, None)
    rule_ir, card_set = assembler.build()
    commentary = commentary_index(["art267", "art268"])

    assert assembler.source_repairs
    assert all(item["from"] != item["to"] for item in assembler.source_repairs)
    for card in card_set["cards"]:
        for ref in card["source_refs"]:
            assert ref["quote"] in commentary[ref["comment_id"]]["document_text"]

    program = compile_rule_ir(rule_ir, commentary, card_set)
    assert "type negligent_bodily_harm_ordinary_established(" in program
    assert "type negligent_bodily_harm_occupational_established(" in program
    assert "type negligent_bodily_harm_gross_established(" in program


def test_gross_negligence_does_not_inherit_the_occupational_business_status() -> None:
    rule_ir, _ = UnitAssembler(NEGLIGENT_BODILY_HARM, None).build()
    gross = next(rule for rule in rule_ir["rules"]
                 if rule["id"] == f"{NEGLIGENT_BODILY_HARM}.outcome.gross.elements_satisfied")
    predicates = {item["predicate"] for item in gross["body"]}

    assert f"{NEGLIGENT_BODILY_HARM}_occupational_general_requirements_satisfied" in predicates
    assert f"{NEGLIGENT_BODILY_HARM}_occupational_business_status_satisfied" not in predicates


def test_approved_proposition_rewrite_is_the_executed_card_text() -> None:
    _, card_set = UnitAssembler(NEGLIGENT_BODILY_HARM, None).build()
    card = next(item for item in card_set["cards"]
                if item["id"] == "art267_sec2.standard.bus_driver_instant_wheel_entry")

    assert card["proposition"] == (
        "피해자가 버스 발차 순간 바퀴 밑으로 갑자기 들어가 운전자가 이를 발견하거나 "
        "회피할 수 없었던 경우에는 운전자의 과실을 인정할 수 없다."
    )


def test_approved_split_parts_become_distinct_executable_cards() -> None:
    _, card_set = UnitAssembler(UNIT, None).build()
    parts = {
        item["id"]: item["proposition"]
        for item in card_set["cards"]
        if item["id"].startswith("art164_sec2_1.burning_result.part.")
    }

    assert parts == {
        "art164_sec2_1.burning_result.part.burning_definition":
            "불태움이란 화력에 의하여 건조물 등이 훼손 또는 손괴되는 것을 말한다.",
        "art164_sec2_1.burning_result.part.completion_on_burning":
            "불태움의 결과가 발생하면 방화죄는 기수에 이른다.",
    }


def test_selective_placement_source_need_not_publish_a_track_outcome() -> None:
    assembler = UnitAssembler("sexual_offense_injury_or_death", None)
    rule_ir, _ = assembler.build()
    predicates = {item["id"] for item in rule_ir["predicates"]}

    assert "sexual_offense_injury_or_death_common_injury_satisfied" in predicates
    assert "sexual_offense_injury_or_death_common_established" not in predicates
    for track in ("intentional_injury", "result_aggravated_injury", "death"):
        assert f"sexual_offense_injury_or_death_{track}_established" in predicates


def test_justification_waiver_reaches_a_blocking_head() -> None:
    """위법성 조각 카드는 결론 계층에 닿되, 극성 미검수면 격리 relation으로 간다.

    이 카드는 ``polarity=exception``이라 어느 방향의 명제인지 필드만으로는 알 수 없다.
    검수 003 I에 따라 검수 전까지는 저지 효과를 결론에서 떼어 놓고 격리해 기록만 하며,
    승인 목록에 오르면 다시 ``track_not_established``로 간다.
    """

    assembler = UnitAssembler("official_secret_disclosure", None)
    rule_ir, _ = assembler.build()
    waiver_id = "art127_sec6.statutorily_required_corruption_report"
    head = ("official_secret_disclosure_quarantined_effect"
            if waiver_id in assembler.quarantined
            else "official_secret_disclosure_track_not_established")
    rules = [item for item in rule_ir["rules"]
             if item["head"]["predicate"] == head]

    assert any(waiver_id in item["norm_card_ids"] for item in rules)


def test_non_ascii_source_card_ids_get_canonical_execution_ids() -> None:
    rule_ir, card_set = UnitAssembler("third_party_bribery", None).build()
    ids = {item["id"] for item in card_set["cards"]}

    assert "art130_sec3_ga.controlled_consulting_account" in ids
    assert not any("가" in card_id for card_id in ids)
    assert not any(
        "가" in card_id
        for rule in rule_ir["rules"]
        for card_id in rule["norm_card_ids"]
    )


def _blocking_placement(unit_id: str) -> tuple[Any, dict[str, Any]]:
    """A live bar in a multi-track unit, with its assembler."""
    assembler = UnitAssembler(unit_id, None)
    for row in assembler.ledger["placements"]:
        if row["role"] == "bar" and len(assembler.tracks) > 1:
            return assembler, row
    raise AssertionError(f"{unit_id}: no bar placement to scope")


def test_component_scope_blocks_only_tracks_that_need_the_component() -> None:
    """장물의 취득 경로가 막혀도 보관·운반죄까지 죽어서는 안 된다.

    A bar defaults to defeating every track its placement reaches.  Declaring
    ``effect_scope: component`` narrows that to the tracks whose element
    conjunction actually contains the named component, which is what an offence
    with parallel 행위태양 needs (검수 003).
    """

    assembler, row = _blocking_placement("homicide")
    placements = assembler.placements()
    satisfied = assembler.emit_cards(placements)
    assembler.satisfied_by_card = satisfied
    by_track = assembler.emit_components(placements, satisfied)

    wide = assembler.blocked_tracks({**row, "effect_scope": "track"}, by_track)
    narrow = assembler.blocked_tracks(
        {**row, "effect_scope": "component",
         "effect_target": row["component_id"]}, by_track)
    everything = assembler.blocked_tracks({**row, "effect_scope": "unit"}, by_track)

    assert set(narrow) <= set(wide) <= set(everything)
    assert set(everything) == set(assembler.tracks)
    # The component's own track always needs it, so narrowing never empties.
    assert row["track_id"] in narrow


def test_unadopted_view_never_reaches_a_conclusion() -> None:
    """미채택 견해는 규칙에서 빠지되 사라지지는 않는다."""

    assembler, row = _blocking_placement("homicide")
    baseline = {item["card_id"] for item in assembler.placements()}

    shelved = UnitAssembler("homicide", None)
    for item in shelved.ledger["placements"]:
        if item["card_id"] == row["card_id"]:
            item["variant_status"] = "unselected"
    compiled = {item["card_id"] for item in shelved.placements()}

    assert row["card_id"] in baseline
    assert row["card_id"] not in compiled
    assert [item["card_id"] for item in shelved.variant_views] == [row["card_id"]]

    dropped = UnitAssembler("homicide", None)
    for item in dropped.ledger["placements"]:
        if item["card_id"] == row["card_id"]:
            item["variant_status"] = "rejected"
    assert row["card_id"] not in {item["card_id"] for item in dropped.placements()}
    assert dropped.variant_views == []


def test_two_adopted_views_in_one_group_are_refused() -> None:
    """같은 견해 그룹에서 둘을 함께 채택하면 룰베이스가 학설을 두 번 확정한다."""

    assembler = UnitAssembler("homicide", None)
    rows = [row for row in assembler.ledger["placements"]][:2]
    for row in rows:
        row["variant_group"] = "test_group"
        row["variant_status"] = "authority_default"

    with pytest.raises(SystemExit, match="상호 배타적인 견해"):
        assembler.placements()
