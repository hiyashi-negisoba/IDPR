"""Free, mechanical scan for assessment_rationale/status self-contradiction.

No API calls. This is a regression check for the assess-prompt fix (docs/handoff/
CURRENT.md, B-bucket bar-card over-firing): does a predicate's own
assessment_rationale argue against its definition while status still claims
satisfied? Restricted to predicates whose card_role can defeat a track
(bar/boundary/waiver) plus, for the property/fraud units where card_role never
reaches the assess call (kind == "standard"), a lower-precision fallback.

This is a candidate generator, not a verdict: negation-proximity regex over
Korean prose has real false-positive/false-negative rates (see the narrow
hallucination precedent in docs/handoff/CURRENT.md). Read the flagged
(unit, predicate_id, rationale) rows before trusting a count.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

from idpr.rulegen.registry import PredicateIRMissing, build_registry


ROOT = Path(__file__).resolve().parents[1]
BLOCKING_ROLES = {"bar", "boundary", "waiver"}
SATISFIED_STATUSES = {"explicitly_supported", "inferentially_supported"}
# The 11 static units in rule_ir_registry_manifest.json's "units" list — the
# older property/fraud pipeline whose RuleIR predicates were never given a
# card_role (only the 25 p2-native units, built by build_p2_native_rule_ir.py,
# carry it). Kept as an explicit set rather than inferred from card_role
# presence so a unit with zero blocking predicates in a given run still gets
# tagged correctly.
FRAUD_PROPERTY_UNITS = {
    "fraud", "theft", "robbery", "extortion", "embezzlement",
    "breach_of_trust", "breach_of_trust_bribe", "lost_property_embezzlement",
    "property_damage", "interference_with_exercise_of_right",
    "occupational_status",
}


def _pipeline_group(unit_id: str) -> str:
    return "fraud_property" if unit_id in FRAUD_PROPERTY_UNITS else "p2_native"

# Negation markers that, when they appear as the grammatical head of a clause
# discussing the predicate's own subject matter, tend to mean "this narrow
# condition is NOT met" — the opposite of what a satisfied status asserts.
NEGATION_MARKERS = (
    "아니다", "아니라", "아니며", "아니므로", "아니고", "아니라면", "아니었다면",
    "볼 수 없다", "보기 어렵다", "인정되지 않는다", "인정할 수 없다",
    "해당하지 않는다", "해당한다고 보기 어렵다",
    "충족되지 않는다", "충족한다고 보기 어렵다",
    "성립하지 않는다", "성립한다고 보기 어렵다",
)
_STOPWORDS = {
    "이", "가", "은", "는", "을", "를", "의", "에", "에서", "으로", "로",
    "와", "과", "도", "만", "라", "이라", "하다", "있다", "없다", "것",
    "수", "그", "이런", "그런", "등", "및", "또는", "때문", "경우",
}
# Legal prose mixes digits into otherwise-Hangul terms (제3자, 제1항) — a
# Hangul-only token regex would silently drop exactly the terms most likely to
# matter for overlap, so digits are allowed inside a token as long as it has
# at least two Hangul characters.
_TOKEN_RE = re.compile(r"[가-힣0-9]*[가-힣][가-힣0-9]*[가-힣][가-힣0-9]*")


def _content_tokens(text: str) -> set[str]:
    return {tok for tok in _TOKEN_RE.findall(text) if tok not in _STOPWORDS}


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def _looks_contradictory(rationale: str, definition: str) -> str | None:
    """Return the offending sentence if a negation clause overlaps the definition."""

    def_tokens = _content_tokens(definition)
    if not def_tokens:
        return None
    for sentence in _sentences(rationale):
        if not any(marker in sentence for marker in NEGATION_MARKERS):
            continue
        overlap = _content_tokens(sentence) & def_tokens
        if len(overlap) >= 1:
            return sentence
    return None


def _load_role_maps(root: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """unit_id -> predicate_id -> {"card_role":..., "definition":..., "kind":...}."""

    registry = build_registry(root)
    maps: dict[str, dict[str, dict[str, Any]]] = {}
    for unit_id, entry in registry.items():
        if isinstance(entry, PredicateIRMissing):
            continue
        maps[unit_id] = {
            predicate["id"]: {
                "card_role": predicate.get("card_role"),
                "definition": str(predicate.get("definition", "")),
                "kind": predicate.get("kind"),
            }
            for predicate in entry.commentary_inputs
        }
    return maps


def _iter_case_dirs(run_dir: Path) -> Iterable[Path]:
    for path in sorted(run_dir.iterdir()):
        if path.is_dir() and (path / "03_native_report.json").is_file():
            yield path


def analyze(run_dir: Path, root: Path = ROOT) -> dict[str, Any]:
    role_maps = _load_role_maps(root)
    rows: list[dict[str, Any]] = []
    verdict_mismatches: list[dict[str, Any]] = []

    for case_dir in _iter_case_dirs(run_dir):
        case_id = case_dir.name
        report = json.loads((case_dir / "03_native_report.json").read_text(encoding="utf-8"))
        trust_by_issue = {
            directive["issue_id"]: directive.get("trust_status", "unknown")
            for directive in report.get("generation_contract", {}).get("conclusion_directives", [])
        }
        unit_by_issue = {
            directive["issue_id"]: directive.get("unit_id", "unknown")
            for directive in report.get("generation_contract", {}).get("conclusion_directives", [])
        }

        consistency_path = case_dir / "06_verdict_consistency.json"
        if consistency_path.is_file():
            contradictions = json.loads(consistency_path.read_text(encoding="utf-8")).get(
                "contradictions", []
            )
            for item in contradictions:
                verdict_mismatches.append({"case_id": case_id, **item})

        for assessment_path in sorted(case_dir.glob("02_assessment_*.json")):
            payload = json.loads(assessment_path.read_text(encoding="utf-8"))
            issue_id = payload.get("issue_id", "")
            unit_id = payload.get("unit_id") or unit_by_issue.get(issue_id, "unknown")
            trust_status = trust_by_issue.get(issue_id, "unknown")
            role_map = role_maps.get(unit_id, {})
            for predicate_id, item in payload.get("assessments", {}).items():
                status = item.get("status")
                if status not in SATISFIED_STATUSES:
                    continue
                meta = role_map.get(predicate_id, {})
                card_role = meta.get("card_role")
                kind = meta.get("kind")
                definition = meta.get("definition", "")
                # Two populations worth checking: p2-native blocking predicates
                # (card_role present and known-dangerous), and property/fraud
                # "standard" 3-state predicates (card_role never reaches them —
                # out of this session's B-bucket scope, tracked separately,
                # lower confidence).
                if card_role in BLOCKING_ROLES:
                    population = "blocking"
                elif card_role is None and kind == "standard":
                    population = "fraud_standard"
                else:
                    continue
                # Old runs (pre this session's A fix) named this field
                # inference_rationale; only accept it as a fallback so a
                # before/after comparison applies the identical contradiction
                # rule to both, absorbing nothing but the rename.
                rationale = item.get("assessment_rationale") or item.get("inference_rationale", "")
                offending = _looks_contradictory(rationale, definition)
                if offending is None:
                    continue
                rows.append(
                    {
                        "case_id": case_id,
                        "unit_id": unit_id,
                        "pipeline": _pipeline_group(unit_id),
                        "issue_id": issue_id,
                        "trust_status": trust_status,
                        "predicate_id": predicate_id,
                        "population": population,
                        "card_role": card_role,
                        "status": status,
                        "definition": definition,
                        "rationale": rationale,
                        "offending_sentence": offending,
                    }
                )

    by_trust: dict[str, int] = {}
    by_unit: dict[str, int] = {}
    by_pipeline: dict[str, int] = {}
    for row in rows:
        by_trust[row["trust_status"]] = by_trust.get(row["trust_status"], 0) + 1
        by_unit[row["unit_id"]] = by_unit.get(row["unit_id"], 0) + 1
        by_pipeline[row["pipeline"]] = by_pipeline.get(row["pipeline"], 0) + 1

    return {
        "run_dir": str(run_dir),
        # These are heuristic_candidates, not a confirmed contradiction count —
        # a negation-proximity regex over Korean prose has real false-positive/
        # false-negative rates. Manually read "candidates" before quoting a
        # rate anywhere; report confirmed_contradictions / heuristic_false_positives
        # separately once read.
        "heuristic_candidates": len(rows),
        "by_trust_status": dict(sorted(by_trust.items(), key=lambda kv: -kv[1])),
        "by_unit": dict(sorted(by_unit.items(), key=lambda kv: -kv[1])),
        "by_pipeline": dict(sorted(by_pipeline.items(), key=lambda kv: -kv[1])),
        "symbolic_writer_inconsistencies": len(verdict_mismatches),
        "verdict_mismatches": verdict_mismatches,
        "candidates": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--json-out", type=Path, default=None)
    args = parser.parse_args()

    report = analyze(args.run_dir)
    summary = {k: v for k, v in report.items() if k != "candidates"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"full candidates written to {args.json_out}")


if __name__ == "__main__":
    main()
