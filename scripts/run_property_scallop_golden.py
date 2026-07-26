"""재산죄 RuleIR Scallop 런타임 골든 시나리오 — 단위 10개 (API 0회).

사기 골든(`run_fraud_scallop_golden.py`)이 검증하는 축을 그대로 단위별로 만든다. 시나리오는
카드에서 결정론적으로 유도하므로 손으로 쓰지 않는다.

  1 ordinary_established     구성요건 component를 각각 하나씩 충족 + 사건 완결 → 성립
  2 incomplete_case_blocked  같은 사실에서 완결 게이트만 빼면 → 성립 차단(요건은 충족)
  3 negative_bar_blocks      BAR 카드 하나가 충족되면 → 불성립 사유 발생·성립 차단
  4 card_conflict_blocks     같은 카드에 satisfied·not_satisfied가 모두 증명되면 → 충돌·차단
  5 unknown_blocks           요건 카드가 unknown이면 → 미확정으로 보존(부정으로 접지 않음)
  6 aggravation_flag_on      가중 카드가 충족되면 → 기본범 성립 + 가중 플래그 on (가중 있는 단위만)

이 여섯이 확인하는 것은 규칙이 "성립을 함부로 만들지 않고, 모르면 모른다고 하고, 가중을 기본범과
분리한다"는 계약이다. 실제 사건 정답을 재현하는 시험이 아니다.

`scli`가 없으면 건너뛴다(`scripts/install_scallop_runtime.sh`).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen.scallop_runtime import (  # noqa: E402
    ScallopFactValidationError,
    run_scenario,
    runtime_version,
    sha256_file,
)
from scripts.build_property_rule_ir import LEVEL_COMPONENTS, UNIT_TRACKS  # noqa: E402

PROP = ROOT / "data/rulegen/property"
RULE_IR_DIR = PROP / "rule_ir"
UNITS = PROP / "rule_ir_units"
COMPILED = ROOT / "rules/generated"
REPORT = PROP / "rule_ir_scallop_runtime_report.json"
HUMAN_REPORT = PROP / "rule_ir_scallop_runtime_report.md"
WORK_ROOT = ROOT / ".cache/scallop/property_golden"
DEFAULT_SCLI = ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
SCLI_SHA256 = "8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def role_contract(rule_ir: dict[str, Any]) -> tuple[str, list[str]]:
    predicate_id = f"{rule_ir['issue_tag']}_case_roles"
    predicate = next(item for item in rule_ir["predicates"]
                     if item["id"] == predicate_id)
    return predicate_id, [argument["name"] for argument in predicate["arguments"]]


def component_members(rule_ir: dict[str, Any], unit: str) -> dict[str, list[str]]:
    """component 술어 → 그 인정 경로에 쓰인 카드들 (규칙에서 되짚는다)."""

    members: dict[str, list[str]] = {}
    for rule in rule_ir["rules"]:
        if ".component." not in rule["id"]:
            continue
        members.setdefault(rule["head"]["predicate"], []).extend(rule["norm_card_ids"])
    return {component: sorted(dict.fromkeys(cards)) for component, cards in members.items()}


def bar_cards(rule_ir: dict[str, Any]) -> list[str]:
    return sorted({card_id for rule in rule_ir["rules"] if ".bar." in rule["id"]
                   for card_id in rule["norm_card_ids"]})


def aggravation_cards(rule_ir: dict[str, Any]) -> list[str]:
    return sorted({card_id for rule in rule_ir["rules"]
                   if ".aggravation." in rule["id"]
                   for card_id in rule["norm_card_ids"]})


def scenarios_for(rule_ir: dict[str, Any], unit: str) -> list[dict[str, Any]]:
    _, actor_fields = role_contract(rule_ir)
    components = component_members(rule_ir, unit)
    bars = bar_cards(rule_ir)
    aggravations = aggravation_cards(rule_ir)

    # 대안적 실행형태(트랙)가 있으면 기본 시나리오는 한 트랙만 채운다 — 둘 다 채우면 두 트랙이
    # 동시에 충족되어 dual_track conflict가 뜨고, 그건 별도 시나리오가 검증할 몫이다.
    tracks = UNIT_TRACKS.get(unit, {})
    track_components = {name: {f"{unit}_{LEVEL_COMPONENTS[level][0]}_satisfied"
                               for level in levels}
                        for name, levels in tracks.items()}
    track_names = list(track_components)
    primary_only = (set().union(*(track_components[name] for name in track_names[1:]))
                    if len(track_names) > 1 else set())
    base_cards = [cards[0] for name, cards in components.items()
                 if cards and name not in primary_only]
    other_track_cards = [cards[0] for name, cards in components.items()
                         if cards and name in primary_only]
    if not base_cards:
        raise SystemExit(f"{unit}: component 카드가 없어 시나리오를 만들 수 없다")

    # card_conflict_blocks·unknown_blocks는 진짜 "필수(mandatory)" 카드로 검증해야 한다 —
    # 트랙 전용 component의 대표 카드는 mandatory_cards()에서 빠지므로(반대쪽 트랙이 없다고
    # 전체를 저지하면 안 되니까) not_satisfied를 줘도 not_established가 뜨지 않는다.
    all_track_components = {name for names in track_components.values() for name in names}
    mandatory_representative = next(
        (card_id for name, cards in components.items()
         for card_id in cards[:1] if cards and name not in all_track_components),
        base_cards[0])

    actors = {field: ("case" if field == "case_id" else field.replace("_id", ""))
              for field in actor_fields}

    def build(scenario_id: str, *, extra: list[tuple[str, str]] = (),
              drop: str | None = None, unknown: str | None = None,
              close: bool = True) -> dict[str, Any]:
        entries: list[tuple[str, str]] = [
            (card_id, "satisfied") for card_id in base_cards if card_id != drop
        ]
        if unknown:
            entries.append((unknown, "unknown"))
        entries.extend(extra)
        assessments = [{
            "card_id": card_id, "status": status, "provable": True,
            "assessment_id": f"{scenario_id}.assessment.{index:03d}",
        } for index, (card_id, status) in enumerate(entries, 1)]
        return {
            "scenario_id": scenario_id,
            **{field: (scenario_id if field == "case_id" else actors[field])
               for field in actor_fields},
            "selected_card_ids": list(dict.fromkeys(card_id for card_id, _ in entries)),
            "assessments": assessments,
            "distinct_entities": [],
            "close_case": close,
        }

    elements = f"{unit}_elements_satisfied"
    established = f"{unit}_established"
    result = [
        {**build("ordinary_established"),
         "expected_nonempty": {elements: True, established: True,
                               f"{unit}_not_established": False,
                               f"{unit}_undetermined": False,
                               f"{unit}_conflict": False}},
        {**build("incomplete_case_blocked", close=False),
         "expected_nonempty": {elements: True, established: False,
                               f"{unit}_not_established": False,
                               f"{unit}_undetermined": False,
                               f"{unit}_conflict": False}},
        {**build("card_conflict_blocks",
                 extra=[(mandatory_representative, "not_satisfied")]),
         "expected_nonempty": {elements: True, established: False,
                               f"{unit}_not_established": True,
                               f"{unit}_undetermined": False,
                               f"{unit}_conflict": True}},
        {**build("unknown_blocks", drop=mandatory_representative,
                 unknown=mandatory_representative),
         "expected_nonempty": {elements: False, established: False,
                               f"{unit}_not_established": False,
                               f"{unit}_undetermined": True,
                               f"{unit}_conflict": False}},
    ]
    if bars:
        result.append({
            **build("negative_bar_blocks", extra=[(bars[0], "satisfied")]),
            "expected_nonempty": {elements: True, established: False,
                                  f"{unit}_not_established": True,
                                  f"{unit}_undetermined": False,
                                  f"{unit}_conflict": False}})
    if aggravations:
        result.append({
            **build("aggravation_flag_on", extra=[(aggravations[0], "satisfied")]),
            "expected_nonempty": {elements: True, established: True,
                                  f"{unit}_not_established": False,
                                  f"{unit}_undetermined": False,
                                  f"{unit}_conflict": False,
                                  f"{unit}_aggravation": True}})
    if other_track_cards:
        result.append({
            **build("dual_track_conflict",
                    extra=[(card_id, "satisfied") for card_id in other_track_cards]),
            "expected_nonempty": {elements: True, established: False,
                                  f"{unit}_not_established": False,
                                  f"{unit}_undetermined": False,
                                  f"{unit}_conflict": True}})
    return result


def main() -> None:
    scli_path = Path(os.environ.get("SCALLOP_SCLI", DEFAULT_SCLI))
    if not scli_path.is_file():
        raise SystemExit("Scallop 런타임이 없다 — scripts/install_scallop_runtime.sh")
    actual = sha256_file(scli_path)
    if actual != SCLI_SHA256:
        raise SystemExit(f"scli 체크섬 불일치: {actual}")

    reports, failures = [], []
    for path in sorted(RULE_IR_DIR.glob("*_rule_ir_candidate.json")):
        rule_ir = read_json(path)
        unit = rule_ir["issue_tag"]
        compiled = (COMPILED / f"property_{unit}_v1_candidate.scl").read_text(
            encoding="utf-8")
        unit_reports = []
        for scenario in scenarios_for(rule_ir, unit):
            expected = scenario.pop("expected_nonempty")
            queries = tuple(expected)
            try:
                results = run_scenario(
                    rule_ir=rule_ir, compiled_source=compiled, scenario=scenario,
                    query_relations=queries, scli_path=scli_path,
                    work_dir=WORK_ROOT / unit)
            except ScallopFactValidationError as exc:
                failures.append(f"{unit}:{scenario['scenario_id']} 사실 검증 실패: {exc}")
                continue
            observed = {relation: result["nonempty"] for relation, result in results.items()}
            ok = observed == expected
            if not ok:
                failures.append(f"{unit}:{scenario['scenario_id']} 기대 {expected} / 관측 {observed}")
            unit_reports.append({"scenario_id": scenario["scenario_id"],
                                 "expected_nonempty": expected,
                                 "observed_nonempty": observed, "passed": ok})
        passed = sum(1 for item in unit_reports if item["passed"])
        print(f"  {unit:36s} 시나리오 {len(unit_reports)} / 통과 {passed}")
        for item in unit_reports:
            if not item["passed"]:
                print(f"       ✗ {item['scenario_id']}: 기대 {item['expected_nonempty']}")
                print(f"         관측 {item['observed_nonempty']}")
        reports.append({"unit": unit, "scenarios": unit_reports,
                        "passed": passed, "total": len(unit_reports)})

    total = sum(item["total"] for item in reports)
    passed = sum(item["passed"] for item in reports)
    REPORT.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime": {"scli": str(scli_path.relative_to(ROOT)),
                    "version": runtime_version(scli_path), "sha256": SCLI_SHA256},
        "model_output_executed_directly": False,
        "method": "사기 골든과 같은 축을 카드에서 결정론적으로 유도",
        "counts": {"units": len(reports), "scenarios": total, "passed": passed},
        "units": reports,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# 재산죄 RuleIR Scallop 런타임 결과", "",
             f"단위 {len(reports)} / 시나리오 {total} / 통과 **{passed}**", "",
             "| 단위 | 시나리오 | 통과 |", "|---|---:|---:|"]
    lines += [f"| `{item['unit']}` | {item['total']} | {item['passed']} |"
              for item in reports]
    HUMAN_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n단위 {len(reports)} / 시나리오 {total} / 통과 {passed}")
    if failures:
        for line in failures[:12]:
            print(f"  ✗ {line}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
