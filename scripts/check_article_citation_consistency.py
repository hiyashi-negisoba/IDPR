#!/usr/bin/env python3
"""Flag 형법 article citations in an IDPR answer that fall outside the
routed unit(s)' registered article scope.

Motivation: docs/handoff/CURRENT.md's narrow-hallucination breakdown found
6/26 IDPR cases with a ``statutory_error`` incident and speculated that most
were simple citation-number typos catchable by cross-referencing each
RuleIR unit's own registered articles (no new judge/API call needed). This
script builds that mechanical check and reports, case by case, whether the
speculation holds — some of the 7 known incidents turn out to be a wrong
subsection or a missing-unit/wrong-track problem rather than a bare typo,
which this article-number-level check cannot catch.

Article scope per unit is read from each unit's own
``*_rule_ir_candidate.json`` -> ``source_scope.target_paths`` (entries like
``commentary://001692/art331``), not guessed or hardcoded.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CITATION_RE = re.compile(r"제\s*(\d+)\s*조(?:의\s*(\d+))?")


def _rule_ir_candidate_paths() -> list[Path]:
    return sorted(ROOT.glob("data/rulegen/*/rule_ir/*_rule_ir_candidate.json"))


def load_unit_article_scope() -> dict[str, set[str]]:
    """unit_id -> set of bare article numbers registered in its source scope."""
    scope: dict[str, set[str]] = {}
    for path in _rule_ir_candidate_paths():
        unit_id = path.name[: -len("_rule_ir_candidate.json")]
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        target_paths = (data.get("source_scope") or {}).get("target_paths") or []
        articles = set()
        for target in target_paths:
            m = re.search(r"art(\d+)(?:_(\d+))?", target)
            if m:
                articles.add(m.group(1))
        if articles:
            scope[unit_id] = articles
    return scope


def units_for_case(run_dir: Path, case_id: str) -> list[str]:
    report = json.loads((run_dir / case_id / "03_native_report.json").read_text(encoding="utf-8"))
    gc = report["generation_contract"]
    units = {c["unit_id"] for c in gc["conclusion_directives"]}
    units |= {s.get("unit_id") for s in gc.get("skipped_directives", []) if s.get("unit_id")}
    units.discard("unsupported")
    return sorted(units)


def extract_citations(answer_text: str) -> list[tuple[str, str]]:
    """Return (article_number, full_match) pairs, e.g. ('164', '제164조')."""
    return [(m.group(1), m.group(0)) for m in CITATION_RE.finditer(answer_text)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, default=ROOT / "experiments/results/rule_ir_native_lean_61_routing_fix")
    parser.add_argument("--case-list", type=Path, default=ROOT / ".cache/phase3_substantive_law_case_lists/curated_26.txt")
    args = parser.parse_args()

    scope = load_unit_article_scope()
    # 형법총칙 (arts 1-86: complicity/attempt/sentencing/concurrence) applies
    # regardless of which offense unit was routed and must never be flagged.
    # Corpus-wide-registered is not a safe filter on its own -- e.g. art302
    # (미성년자·심신미약자 간음) is a real 각칙 offense article but happens to be
    # registered by no unit yet, so relying on "seen somewhere in our units"
    # would silently miss it. Anything above the 총칙/각칙 boundary is a real
    # specific-offense article and is fair game to flag.
    GENERAL_PART_MAX_ARTICLE = 86
    case_ids = [l.strip() for l in args.case_list.read_text(encoding="utf-8").splitlines() if l.strip()]

    total_flagged = 0
    total_cases_with_flags = 0
    for case_id in case_ids:
        case_dir = args.run_dir / case_id
        answer_path = case_dir / "05_answer.md"
        if not answer_path.exists():
            continue
        units = units_for_case(args.run_dir, case_id)
        allowed = set()
        for u in units:
            allowed |= scope.get(u, set())
        answer = answer_path.read_text(encoding="utf-8")
        citations = extract_citations(answer)
        flagged = sorted({
            (num, full) for num, full in citations
            if num not in allowed and int(num) > GENERAL_PART_MAX_ARTICLE
        })
        if flagged:
            total_cases_with_flags += 1
            total_flagged += len(flagged)
            print(f"=== {case_id} (units: {', '.join(units)}) ===")
            print(f"  allowed articles: {sorted(allowed, key=int)}")
            for num, full in flagged:
                print(f"  FLAGGED: {full} (제{num}조 not in any routed unit's scope)")
            print()

    print(f"cases with >=1 out-of-scope citation: {total_cases_with_flags}/{len(case_ids)}")
    print(f"total flagged citation mentions: {total_flagged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
