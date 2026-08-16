#!/usr/bin/env python3
"""UNKNOWN predicate 중 더 넓은 증거가 이미 있었던 것을 정적으로 가려낸다.

`voluntary_cessation_or_prevention`에서 확인된 결함의 일반형을 찾는다: predicate가
`offense_realization` 폭으로 요청됐는데, **같은 instance의 actor_episode carrier가
더 넓은 span을 이미 가지고 있던** 경우다. 그 폭 차이 안에 답이 있었다면 UNKNOWN은
모델 성능이 아니라 carrier 설정의 결과다.

이것은 스크리닝이지 증명이 아니다. 폭이 넓다는 것은 답이 거기 있었다는 뜻이 아니다.
사건 텍스트를 읽지 않으므로(sealed-59) 원문 대조는 하지 않는다.

출력은 predicate_ref와 카운트뿐이고 사건 사실이나 인용문을 싣지 않는다.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
LEGAL_ELEMENTS = REPO / "data" / "v2" / "definitions" / "legal_elements.yaml"
GROUND_FACTS = REPO / "data" / "v2" / "definitions" / "ground_facts.yaml"

ACTOR_EPISODE = "actor_episode"
DEFAULT_SCOPE = "offense_realization"


def _authored_scopes() -> dict[str, str]:
    """정의에 적힌 evidence_scope. 없으면 기본값이 적용된다."""
    scopes: dict[str, str] = {}
    for path in (LEGAL_ELEMENTS, GROUND_FACTS):
        for entry in yaml.safe_load(path.read_text(encoding="utf-8")) or ():
            if isinstance(entry, dict) and "id" in entry:
                scopes[entry["id"]] = entry.get("evidence_scope", DEFAULT_SCOPE)
    return scopes


def _instance_id(key: dict) -> tuple:
    return (
        key.get("case_id"),
        key.get("actor_id"),
        key.get("offense_ref"),
        key.get("occurrence_id"),
    )


def _load(path: Path) -> dict[str, dict]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            rows[rec["sub_question_id"]] = rec
    return rows


def _bounds(span: dict | None) -> tuple[int, int] | None:
    if not isinstance(span, dict):
        return None
    try:
        return int(span["start"]), int(span["end"])
    except (KeyError, TypeError, ValueError):
        return None


def _width(span: dict | None) -> int:
    bounds = _bounds(span)
    return -1 if bounds is None else bounds[1] - bounds[0]


def audit_case(plan: dict, call2: dict, scopes: dict[str, str]) -> list[dict]:
    spans = {
        occ["occurrence_id"]: occ.get("source_span")
        for occ in plan.get("occurrences", ())
    }

    used: dict[tuple, str] = {}
    widest_episode: dict[tuple, tuple[str, int]] = {}
    for carrier in plan.get("assessment_carriers", ()):
        instance = _instance_id(carrier["instance_key"])
        used[(instance, carrier["predicate_ref"])] = carrier["carrier_id"]
        if carrier.get("carrier_kind") != ACTOR_EPISODE:
            continue
        width = _width(spans.get(carrier["carrier_id"]))
        current = widest_episode.get(instance)
        if current is None or width > current[1]:
            widest_episode[instance] = (carrier["carrier_id"], width)

    findings = []
    for assessment in call2.get("assessments", ()):
        if assessment.get("truth") != "UNKNOWN":
            continue
        predicate = assessment.get("predicate_ref")
        instance = _instance_id(assessment.get("instance_key", {}))
        carrier_id = used.get((instance, predicate))
        if carrier_id is None:
            continue
        used_bounds = _bounds(spans.get(carrier_id))
        episode = widest_episode.get(instance)
        if used_bounds is None or episode is None or episode[1] <= _width(
            spans.get(carrier_id)
        ):
            continue
        episode_bounds = _bounds(spans.get(episode[0]))
        if episode_bounds is None:
            continue
        # 중지·결과처럼 실행행위 **뒤**에 오는 사실은 trailing 폭에서만 답할 수 있다.
        # leading 폭만 넓은 것은 배경·경위가 더 실린 것이고 다른 결함이다.
        trailing = episode_bounds[1] - used_bounds[1]
        leading = used_bounds[0] - episode_bounds[0]
        findings.append(
            {
                "case_id": plan["sub_question_id"],
                "predicate_ref": predicate,
                "authored_scope": scopes.get(predicate, DEFAULT_SCOPE),
                "used_width": used_bounds[1] - used_bounds[0],
                "episode_width": episode[1],
                "trailing_gap": trailing,
                "leading_gap": leading,
            }
        )
    return findings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--plan",
        type=Path,
        default=REPO
        / "experiments/v2_unknown_reduction_26/plan_concurrence/evaluation_instance_plan.jsonl",
    )
    ap.add_argument(
        "--call2",
        type=Path,
        default=REPO
        / "experiments/v2_unknown_reduction_26/call2/grounding_output_with_article151.jsonl",
    )
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    scopes = _authored_scopes()
    plans = _load(args.plan)
    call2 = _load(args.call2)

    findings: list[dict] = []
    for case_id, plan in sorted(plans.items()):
        if case_id in call2:
            findings.extend(audit_case(plan, call2[case_id], scopes))

    trailing = [
        f
        for f in findings
        if f["authored_scope"] == DEFAULT_SCOPE and f["trailing_gap"] > 0
    ]
    report = {
        "note": (
            "UNKNOWN 중 같은 instance의 actor_episode carrier가 더 넓었던 것. "
            "스크리닝이며 원문 대조가 아니다."
        ),
        "total_findings": len(findings),
        "cases_affected": len({f["case_id"] for f in findings}),
        "by_case": dict(Counter(f["case_id"] for f in findings).most_common()),
        "trailing_note": (
            "실행행위 뒤 텍스트가 요청에서 빠진 realization-scoped UNKNOWN. "
            "voluntary_cessation_or_prevention이 확인된 사례이고 나머지는 후보다."
        ),
        "trailing_total": len(trailing),
        "trailing_cases": len({f["case_id"] for f in trailing}),
        "trailing_by_predicate": dict(
            Counter(f["predicate_ref"] for f in trailing).most_common()
        ),
        "trailing_by_case": dict(
            Counter(f["case_id"] for f in trailing).most_common()
        ),
        "findings": findings,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {k: v for k, v in report.items() if k != "findings"},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
