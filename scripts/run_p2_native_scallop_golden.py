"""P2 RuleIR-native unit의 Scallop 런타임 골든 시나리오 (API 0회).

사기·재산죄 골든과 같은 축을 검증한다. 다만 시나리오를 규칙 id에서 되짚지 않고 승인 원장의
per-card placement에서 직접 유도한다 — role·join·track이 이미 데이터에 있기 때문이다.

  1 <track>_established        track과 그 상속 track의 요건을 최소로 충족 + 완결 → 성립
  2 <track>_incomplete_blocked 같은 사실에서 완결 게이트만 빼면 → 성립 차단(요건은 충족)
  3 <track>_bar_blocks         bar·boundary 카드 하나가 충족되면 → 불성립 사유 발생·성립 차단
  4 <track>_conflict_blocks    같은 카드에 satisfied·not_satisfied가 모두 증명되면 → 충돌·차단
  5 <track>_unknown_blocks     필수 카드가 unknown이면 → 미확정으로 보존(부정으로 접지 않음)

가중 track은 상속한 base의 요건까지 모두 채워야 성립해야 한다. 2·5번이 그 상속이 실제로
걸려 있는지를 확인한다: base 쪽 카드 하나만 빠져도 가중 track이 성립하면 안 된다.

`scli`가 없으면 실행하지 않는다(`scripts/install_scallop_runtime.sh`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
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
from scripts.build_p2_native_rule_ir import OUT_DIR, UnitAssembler, read_json  # noqa: E402

LEDGER_DIR = ROOT / "data/rulegen/p2/native_review"
COMPILED = ROOT / "rules/generated"
REPORT_DIR = ROOT / "data/rulegen/p2"
WORK_ROOT = ROOT / ".cache/scallop/p2_native_golden"
DEFAULT_SCLI = ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
SCLI_SHA256 = "8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a"


class UnitScenarios:
    """One compiled unit's golden scenarios, derived from its decision ledger."""

    def __init__(self, unit_id: str) -> None:
        self.unit_id = unit_id
        self.rule_ir = read_json(OUT_DIR / f"{unit_id}_rule_ir_candidate.json")
        self.assembler = UnitAssembler(unit_id, None)
        # Use the execution ledger after approved rewrites/split parts have been
        # materialized.  The persisted decision ledger deliberately retains the
        # source card ids, while RuleIR addresses each split part independently.
        self.ledger = self.assembler.ledger
        self.compiled = (COMPILED / f"p2_{unit_id}_v1_candidate.scl").read_text(
            encoding="utf-8")
        self.parent = {item["track_id"]: item.get("inherits_from")
                       for item in self.ledger["tracks"]}
        role_predicate = next(
            item for item in self.rule_ir["predicates"]
            if item["id"].endswith("_case_roles"))
        self.actor_fields = [argument["name"] for argument in role_predicate["arguments"]]
        compiled_cards = set(self.rule_ir["norm_card_scope"]["card_ids"])
        self.rows = [row for row in self.ledger["placements"]
                     if row["card_id"] in compiled_cards]
        # 어떤 track이 실제로 컴파일되었는지는 RuleIR이 말한다. 원장에는 컴파일 범위 밖의
        # track에 놓인 경계 카드도 남아 있으므로 placement만 보고 track을 세면 안 된다.
        compiled_tracks = {
            item["id"][len(f"{unit_id}_"):-len("_elements_satisfied")]
            for item in self.rule_ir["predicates"]
            if item["id"].startswith(f"{unit_id}_")
            and item["id"].endswith("_elements_satisfied")
        }
        self.tracks = [track for track in self.parent if track in compiled_tracks]

    def lineage(self, track: str) -> list[str]:
        """The track plus every track it inherits from, innermost last."""
        chain, cursor = [], track
        while cursor and cursor not in chain:
            chain.append(cursor)
            cursor = self.parent.get(cursor)
        return chain

    def minimal_cards(self, track: str) -> list[str]:
        """The smallest card set that satisfies every component in the track's lineage."""
        by_component: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in self.rows:
            if row["role"] == "component" and self.assembler.placement_applies_to_track(row, track):
                by_component[(row["track_id"], row["component_id"])].append(row)
        cards: list[str] = []
        for key in sorted(by_component):
            rows = sorted(by_component[key], key=lambda row: row["card_id"])
            joins = {row["component_join"] for row in rows}
            if joins == {"alternative_any"}:
                cards.append(rows[0]["card_id"])
            else:
                cards.extend(row["card_id"] for row in rows)
        return list(dict.fromkeys(cards))

    def mandatory_card(self, track: str) -> str:
        """A card the track genuinely cannot do without — for the unknown/conflict axes.

        결합 요건 카드가 있으면 그것을 쓴다. 없으면 최소 집합의 첫 카드를 쓴다 — 최소 집합은
        택일 component마다 대표 카드를 하나씩만 담으므로, 그 하나가 빠지면 요건이 실제로
        무너진다.
        """
        for row in sorted(self.rows, key=lambda row: row["card_id"]):
            if (row["role"] == "component"
                    and row["component_join"] == "mandatory_all"
                    and self.assembler.placement_applies_to_track(row, track)):
                return row["card_id"]
        minimal = self.minimal_cards(track)
        if not minimal:
            raise SystemExit(f"{self.unit_id}/{track}: 구성요건 카드가 없어 축을 세울 수 없다")
        return minimal[0]

    def bar_card(self, track: str) -> str | None:
        for row in sorted(self.rows, key=lambda row: row["card_id"]):
            if (row["role"] in ("bar", "boundary")
                    and self.assembler.placement_applies_to_track(row, track)):
                return row["card_id"]
        return None

    def scenario(self, scenario_id: str, entries: list[tuple[str, str]],
                 *, close: bool = True) -> dict[str, Any]:
        actors = {field: ("case" if field == "case_id" else field.replace("_id", ""))
                  for field in self.actor_fields}
        return {
            "scenario_id": scenario_id,
            **{field: (scenario_id if field == "case_id" else actors[field])
               for field in self.actor_fields},
            "selected_card_ids": list(dict.fromkeys(card_id for card_id, _ in entries)),
            "assessments": [{
                "card_id": card_id, "status": status, "provable": True,
                "assessment_id": f"{scenario_id}.assessment.{index:03d}",
            } for index, (card_id, status) in enumerate(entries, 1)],
            "distinct_entities": [],
            "close_case": close,
        }

    def build(self) -> list[dict[str, Any]]:
        unit = self.unit_id
        out: list[dict[str, Any]] = []
        for track in self.tracks:
            elements = f"{unit}_{track}_elements_satisfied"
            established = f"{unit}_{track}_established"
            base = [(card_id, "satisfied") for card_id in self.minimal_cards(track)]
            mandatory = self.mandatory_card(track)
            no_report = {f"{unit}_not_established": False,
                         f"{unit}_undetermined": False,
                         f"{unit}_conflict": False}
            out.append({
                **self.scenario(f"{track}.established", base),
                "track": track,
                "expected_nonempty": {elements: True, established: True, **no_report}})
            out.append({
                **self.scenario(f"{track}.incomplete_blocked", base, close=False),
                "track": track,
                "expected_nonempty": {elements: True, established: False, **no_report}})
            # 구성요건 카드의 충돌은 충돌로만 보고한다. `not_established`는 bar·boundary가
            # 충족되었을 때만 나오며, 평가가 엇갈렸다는 사실이 곧 불성립 사유는 아니다.
            out.append({
                **self.scenario(f"{track}.conflict_blocks",
                                base + [(mandatory, "not_satisfied")]),
                "track": track,
                "expected_nonempty": {elements: True, established: False,
                                      f"{unit}_not_established": False,
                                      f"{unit}_undetermined": False,
                                      f"{unit}_conflict": True}})
            out.append({
                **self.scenario(
                    f"{track}.unknown_blocks",
                    [(card_id, status) for card_id, status in base
                     if card_id != mandatory] + [(mandatory, "unknown")]),
                "track": track,
                "expected_nonempty": {elements: False, established: False,
                                      f"{unit}_not_established": False,
                                      f"{unit}_undetermined": True,
                                      f"{unit}_conflict": False}})
            bar = self.bar_card(track)
            if bar:
                out.append({
                    **self.scenario(f"{track}.bar_blocks", base + [(bar, "satisfied")]),
                    "track": track,
                    "expected_nonempty": {elements: True, established: False,
                                          f"{unit}_not_established": True,
                                          f"{unit}_undetermined": False,
                                          f"{unit}_conflict": False}})
        return out


def run_unit(unit_id: str, scli_path: Path) -> tuple[dict[str, Any], list[str]]:
    unit = UnitScenarios(unit_id)
    failures: list[str] = []
    reports: list[dict[str, Any]] = []
    for scenario in unit.build():
        expected = scenario.pop("expected_nonempty")
        track = scenario.pop("track")
        try:
            results = run_scenario(
                rule_ir=unit.rule_ir, compiled_source=unit.compiled, scenario=scenario,
                query_relations=tuple(expected), scli_path=scli_path,
                work_dir=WORK_ROOT / unit_id)
        except ScallopFactValidationError as exc:
            failures.append(f"{unit_id}:{scenario['scenario_id']} 사실 검증 실패: {exc}")
            continue
        observed = {relation: result["nonempty"] for relation, result in results.items()}
        passed = observed == expected
        if not passed:
            failures.append(
                f"{unit_id}:{scenario['scenario_id']} 기대 {expected} / 관측 {observed}")
        reports.append({"scenario_id": scenario["scenario_id"], "track": track,
                        "expected_nonempty": expected, "observed_nonempty": observed,
                        "passed": passed})
    return {
        "unit": unit_id,
        "tracks": unit.tracks,
        "scenarios": reports,
        "passed": sum(1 for item in reports if item["passed"]),
        "total": len(reports),
    }, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", action="append", default=[],
                        help="생략하면 컴파일된 P2 native unit을 모두 돈다")
    args = parser.parse_args()

    scli_path = Path(os.environ.get("SCALLOP_SCLI", DEFAULT_SCLI))
    if not scli_path.is_file():
        raise SystemExit("Scallop 런타임이 없다 — scripts/install_scallop_runtime.sh")
    actual = sha256_file(scli_path)
    if actual != SCLI_SHA256:
        raise SystemExit(f"scli 체크섬 불일치: {actual}")

    units = args.unit or sorted(
        path.name[: -len("_rule_ir_candidate.json")]
        for path in OUT_DIR.glob("*_rule_ir_candidate.json"))

    reports, failures = [], []
    for unit_id in units:
        report, unit_failures = run_unit(unit_id, scli_path)
        failures.extend(unit_failures)
        reports.append(report)
        print(f"  {unit_id:34s} 시나리오 {report['total']:3d} / 통과 {report['passed']:3d}")
        for item in report["scenarios"]:
            if not item["passed"]:
                print(f"       ✗ {item['scenario_id']}")
                print(f"         기대 {item['expected_nonempty']}")
                print(f"         관측 {item['observed_nonempty']}")

    total = sum(item["total"] for item in reports)
    passed = sum(item["passed"] for item in reports)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "p2_native_scallop_runtime_report.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runtime": {"scli": str(scli_path.relative_to(ROOT)),
                    "version": runtime_version(scli_path), "sha256": SCLI_SHA256},
        "model_output_executed_directly": False,
        "method": "승인 원장의 per-card placement에서 결정론적으로 유도한 시나리오",
        "counts": {"units": len(reports), "scenarios": total, "passed": passed},
        "units": reports,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# P2 RuleIR-native Scallop 런타임 결과", "",
             f"unit {len(reports)} / 시나리오 {total} / 통과 **{passed}**", "",
             "| unit | track | 시나리오 | 통과 |", "|---|---|---:|---:|"]
    lines += [f"| `{item['unit']}` | {', '.join(item['tracks'])} | "
              f"{item['total']} | {item['passed']} |" for item in reports]
    (REPORT_DIR / "p2_native_scallop_runtime_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nunit {len(reports)} / 시나리오 {total} / 통과 {passed}")
    if failures:
        for line in failures[:12]:
            print(f"  ✗ {line}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
