"""재산죄 RuleIR — 결정론적 조립·계약·Scallop 런타임 회귀.

사기 트랙(`test_rulegen_exemplar.py`, `test_fraud_scallop_runtime.py`)이 지키는 것을 재산죄 10단위에
대해 같은 방식으로 지킨다. 조립은 결정론이므로 재실행 결과가 커밋된 산출물과 바이트 단위로 같아야
하고, 계약 검증과 런타임 골든이 모두 통과해야 한다.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from idpr.rulegen import (
    RuleIRGenerationProfile,
    compile_rule_ir,
    validate_full_rule_ir_generation,
)
from scripts.build_property_core_norm_card_sets import commentary_index
from scripts.build_property_rule_ir import (
    CARD_ROLES,
    DEFERRED_UNITS,
    OUT_DIR,
    UNIT_MANIFEST,
    UNIT_TRACKS,
    UNITS,
    UnitBuilder,
    read_json,
)
from scripts.build_property_rule_ir_preflight import ACTOR_ROLES
from scripts.run_property_scallop_golden import (
    DEFAULT_SCLI,
    SCLI_SHA256,
    scenarios_for,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHASE_MAP = PROJECT_ROOT / "data/rulegen/property/rule_ir_phase_map.json"
COMPILED_DIR = PROJECT_ROOT / "rules/generated"


def unit_tags() -> list[str]:
    return [entry["issue_tag"] for entry in read_json(UNIT_MANIFEST)["units"]
            if entry["issue_tag"] not in DEFERRED_UNITS]


def commentary_for(unit: str) -> dict[str, dict]:
    articles = next(entry["articles"] for entry in read_json(UNIT_MANIFEST)["units"]
                    if entry["issue_tag"] == unit)
    commentary: dict[str, dict] = {}
    for article in articles:
        chunks, _ = commentary_index(article)
        commentary.update(chunks)
    return commentary


@pytest.mark.parametrize("unit", unit_tags())
def test_rule_ir_is_deterministic_and_contract_valid(unit: str) -> None:
    card_set = read_json(UNITS / f"{unit}.json")
    phase_rows = read_json(PHASE_MAP)["rows"]
    rule_ir = UnitBuilder(unit, card_set, phase_rows).build()

    committed = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")
    assert rule_ir == committed, "조립이 결정론이 아니거나 산출물이 뒤처졌다"

    tracks = tuple(UNIT_TRACKS.get(unit, {}))
    validate_full_rule_ir_generation(
        rule_ir, commentary_for(unit), card_set,
        RuleIRGenerationProfile.for_crime(unit, ACTOR_ROLES[unit], tracks=tracks))

    # track이 없으면 부정은 최종 결론 규칙 하나에서만 쓴다. track이 있는 단위(로버리 등)는
    # track 전용 저지 카드가 다른 track까지 막지 않도록 track마다 자기 몫만 부정하는
    # 게이트를 따로 둔다(검수 003) — 허용되는 부정 자리는 그 track별 게이트뿐이다.
    negating = {rule["id"] for rule in rule_ir["rules"]
                if any(atom.get("negated") for atom in rule["body"])}
    if tracks:
        assert negating == {f"{unit}.outcome.{track}.established" for track in tracks}
    else:
        assert negating == {f"{unit}.core.outcome.established"}


@pytest.mark.parametrize("unit", unit_tags())
def test_compiled_scallop_matches_rule_ir(unit: str) -> None:
    rule_ir = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")
    card_set = read_json(UNITS / f"{unit}.json")
    compiled = COMPILED_DIR / f"property_{unit}_v1_candidate.scl"
    assert compiled.read_text(encoding="utf-8") == compile_rule_ir(
        rule_ir, commentary_for(unit), card_set)


@pytest.mark.parametrize("unit", unit_tags())
def test_scallop_golden_scenarios(unit: str) -> None:
    scli_path = Path(os.environ.get("SCALLOP_SCLI", DEFAULT_SCLI))
    if not scli_path.is_file():
        pytest.skip("install the pinned runtime with scripts/install_scallop_runtime.sh")

    from idpr.rulegen.scallop_runtime import run_scenario, sha256_file

    assert sha256_file(scli_path) == SCLI_SHA256
    rule_ir = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")
    compiled = (COMPILED_DIR / f"property_{unit}_v1_candidate.scl").read_text(
        encoding="utf-8")
    scenarios = scenarios_for(rule_ir, unit)
    assert len(scenarios) >= 4

    for scenario in scenarios:
        expected = scenario.pop("expected_nonempty")
        results = run_scenario(
            rule_ir=rule_ir, compiled_source=compiled, scenario=scenario,
            query_relations=tuple(expected), scli_path=scli_path,
            work_dir=PROJECT_ROOT / ".cache/scallop/property_pytest" / unit)
        observed = {relation: result["nonempty"] for relation, result in results.items()}
        assert observed == expected, f"{unit}:{scenario['scenario_id']}"


def test_runtime_report_is_current() -> None:
    report = read_json(
        PROJECT_ROOT / "data/rulegen/property/rule_ir_scallop_runtime_report.json")
    assert report["model_output_executed_directly"] is False
    assert report["counts"]["units"] == len(unit_tags())
    assert report["counts"]["passed"] == report["counts"]["scenarios"]


def _robbery_builder() -> UnitBuilder:
    card_set = read_json(UNITS / "robbery.json")
    phase_rows = read_json(PHASE_MAP)["rows"]
    return UnitBuilder("robbery", card_set, phase_rows)


def _add_synthetic_bar(builder: UnitBuilder, level: str, effect_scope: str) -> dict:
    """A bar card placed by hand at a track-exclusive level — none exist in committed
    property data today, so track-scoped defeat has to be exercised synthetically."""
    card = {
        "id": "test.synthetic_track_bar",
        "polarity": "negative",
        "proposition": "테스트용 합성 저지 카드",
        "formalization": "standard_input",
        "source_refs": [],
    }
    builder.cards.append(card)
    builder.cards_by_id[card["id"]] = card
    builder.levels[card["id"]] = level
    builder.card_roles[card["id"]] = {"role": "bar", "effect_scope": effect_scope}
    return card


def test_component_scoped_bar_defeats_only_its_own_track() -> None:
    """장물 취득 경로의 요건 결여가 보관죄까지 죽이면 안 되는 것과 같은 문제를 로버리의
    두 track(재물강취/이득강취)으로 재현한다(검수 003)."""

    builder = _robbery_builder()
    card = _add_synthetic_bar(builder, "L0r", "component")

    assert builder.track_scoped_bars() == {"property": [card]}


def test_unit_scope_override_skips_track_scoping() -> None:
    """track 전용 레벨에 있어도 ``effect_scope: unit``이면 죄 전체를 막아야 한다."""

    builder = _robbery_builder()
    _add_synthetic_bar(builder, "L0r", "unit")

    assert builder.track_scoped_bars() == {}


def test_unknown_effect_scope_is_rejected() -> None:
    builder = _robbery_builder()
    _add_synthetic_bar(builder, "L0r", "bogus")

    with pytest.raises(SystemExit, match="effect_scope"):
        builder.track_scoped_bars()


def test_quarantined_track_bar_never_gates_a_track() -> None:
    """검수 003 I — 극성 미검수 카드는 격리될 뿐 어느 track도 막지 않는다."""

    builder = _robbery_builder()
    card = _add_synthetic_bar(builder, "L0r", "component")
    builder.quarantined.add(card["id"])

    assert builder.track_scoped_bars() == {}


def test_track_without_positive_components_never_derives_established() -> None:
    """장물죄 양도·알선처럼 track 전용 레벨에 positive component가 하나도 없는 경우를
    로버리의 두 track으로 재현한다. 공유 component만으로 그 track이 성립하면 실행행위
    사실 없이 established가 나오므로, 이 track은 긍정 도출 규칙 자체가 컴파일되지
    않아야 한다 — 반면 track-scoped bar는 이 predicate와 무관하게 독립적으로 동작해야
    하고, 다른(정상) track은 전혀 영향받지 않아야 한다."""

    builder = _robbery_builder()
    builder.cards = [card for card in builder.cards
                     if builder.levels.get(card["id"]) not in ("L0r", "L4r")]
    builder.cards_by_id = {card["id"]: card for card in builder.cards}
    _add_synthetic_bar(builder, "L0r", "component")

    rule_ir = builder.build()
    rule_ids = {rule["id"] for rule in rule_ir["rules"]}

    assert "robbery.core.outcome.track.property" not in rule_ids
    assert "robbery.core.outcome.elements_satisfied.property" not in rule_ids
    # The unaffected track keeps its ordinary positive derivation.
    assert "robbery.core.outcome.track.benefit" in rule_ids
    assert "robbery.core.outcome.elements_satisfied.benefit" in rule_ids
    # A track-scoped bar still compiles and gates that track's not_established,
    # independently of the missing positive path. Robbery's committed data
    # already has real property-track bars, so the synthetic one lands at
    # whatever index follows them rather than always being 001.
    assert any(rule_id.startswith("robbery.test.track_bar.property.")
               for rule_id in rule_ids)
    assert any(gap.startswith("track_positive_path_missing: property")
               for gap in rule_ir["coverage_gaps"])
    assert not any(gap.startswith("track_positive_path_missing: benefit")
                   for gap in rule_ir["coverage_gaps"])


def test_unselected_variant_card_is_dropped_but_recorded() -> None:
    card_set = read_json(UNITS / "theft.json")
    phase_rows = read_json(PHASE_MAP)["rows"]
    card_id = card_set["cards"][0]["id"]
    roles = dict(read_json(CARD_ROLES)["cards"])
    roles[card_id] = {**roles.get(card_id, {}), "variant_status": "unselected"}

    builder = UnitBuilder("theft", card_set, phase_rows, card_roles=roles)

    assert card_id not in builder.cards_by_id
    assert card_id in {card["id"] for card in builder.variant_views}


def test_rejected_variant_card_is_dropped_and_not_recorded() -> None:
    card_set = read_json(UNITS / "theft.json")
    phase_rows = read_json(PHASE_MAP)["rows"]
    card_id = card_set["cards"][0]["id"]
    roles = dict(read_json(CARD_ROLES)["cards"])
    roles[card_id] = {**roles.get(card_id, {}), "variant_status": "rejected"}

    builder = UnitBuilder("theft", card_set, phase_rows, card_roles=roles)

    assert card_id not in builder.cards_by_id
    assert card_id not in {card["id"] for card in builder.variant_views}


def test_two_adopted_views_in_one_group_are_refused() -> None:
    """같은 견해 그룹에서 둘을 함께 채택하면 룰베이스가 학설을 두 번 확정한다."""

    card_set = read_json(UNITS / "theft.json")
    phase_rows = read_json(PHASE_MAP)["rows"]
    ids = [card["id"] for card in card_set["cards"][:2]]
    roles = dict(read_json(CARD_ROLES)["cards"])
    for card_id in ids:
        roles[card_id] = {**roles.get(card_id, {}), "variant_group": "test_group",
                          "variant_status": "authority_default"}

    with pytest.raises(SystemExit, match="상호 배타적인 견해"):
        UnitBuilder("theft", card_set, phase_rows, card_roles=roles)
