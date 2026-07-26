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
    DEFERRED_UNITS,
    OUT_DIR,
    UNIT_MANIFEST,
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

    validate_full_rule_ir_generation(
        rule_ir, commentary_for(unit), card_set,
        RuleIRGenerationProfile.for_crime(unit, ACTOR_ROLES[unit]))

    # 부정은 최종 결론 규칙 하나에서만 쓴다
    negating = [rule["id"] for rule in rule_ir["rules"]
                if any(atom.get("negated") for atom in rule["body"])]
    assert negating == [f"{unit}.core.outcome.established"]


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
