"""Narrow broad V2 retrieval to grounded, standalone special-part articles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.rulebase.cards import card_corpus
from idpr.special_part import (
    SpecialPartPlanError,
    PLANNER_VERSION,
    planned_candidate_row,
    planner_payload,
    planner_schema,
    validate_plan,
)


DEFAULT_BROAD_CANDIDATES = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data/eval/special_part_candidates.jsonl"


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--broad-candidates", type=Path, default=DEFAULT_BROAD_CANDIDATES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    args.work_dir = args.work_dir or args.out.parent / "planner_cases"
    args.work_dir.mkdir(parents=True, exist_ok=True)

    inventory_rows = _rows(args.inventory)
    inventory = {str(row["sub_question_id"]): row for row in inventory_rows}
    broad = {str(row["sub_question_id"]): row for row in _rows(args.broad_candidates)}
    case_ids = [str(row["sub_question_id"]) for row in inventory_rows]
    if args.case_id:
        unknown = sorted(set(args.case_id) - set(case_ids))
        if unknown:
            parser.error(f"unknown --case-id values: {unknown}")
        wanted = set(args.case_id)
        case_ids = [case_id for case_id in case_ids if case_id in wanted]
    if args.limit is not None:
        case_ids = case_ids[: args.limit]
    missing = sorted(set(case_ids) - set(broad))
    if missing:
        raise ValueError(f"broad candidate artifact is missing cases: {missing}")

    client = VLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=args.timeout_seconds,
    )
    system_prompt = load_prompt("special_part_plan")
    user_prompt = load_prompt("special_part_plan_user")
    corpus = card_corpus()
    output_rows: list[dict[str, Any]] = []
    for index, case_id in enumerate(case_ids, start=1):
        cache_path = args.work_dir / f"{case_id}.json"
        if cache_path.is_file() and not args.overwrite:
            try:
                cached = json.loads(cache_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                cached = {}
            if (
                cached.get("sub_question_id") == case_id
                and cached.get("pipeline_mode") == "special_part_light"
                and cached.get("planner_version") == PLANNER_VERSION
            ):
                output_rows.append(cached)
                print(
                    f"[{index}/{len(case_ids)}] {case_id} cache "
                    f"{len(cached.get('broad_articles', ()))}->"
                    f"{len(cached.get('articles', ()))} articles",
                    flush=True,
                )
                continue
        case = inventory[case_id]
        question_prompt = str(case.get("question_prompt", ""))
        question_text = scoped_question_text(str(case.get("question_text", "")), question_prompt)
        payload, candidate_articles = planner_payload(
            case_id=case_id,
            question_text=question_text,
            question_prompt=question_prompt,
            broad_articles=tuple(broad[case_id].get("articles", ())),
            corpus=corpus,
        )
        assert_no_leaked_fields(payload)
        if not candidate_articles:
            row = planned_candidate_row(
                case_id=case_id,
                selected_articles=(),
                entries=(),
                scope_note="검색 후보 중 독립 평가 가능한 각칙 구성요건 조문이 없음",
                broad_articles=tuple(broad[case_id].get("articles", ())),
                planner_route="direct_legal_analysis",
                corpus=corpus,
            )
        else:
            correction_errors: list[str] = []
            for attempt in range(1, 3):
                request = dict(payload)
                if correction_errors:
                    request["contract_correction"] = {
                        "errors": correction_errors,
                        "instruction": "source_quote는 case_text의 연속 문구를 정확히 복사하여 전체 JSON을 다시 출력하라.",
                    }
                model_output, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    user_template=user_prompt,
                    payload=request,
                    schema_name="special_part_plan",
                    schema=planner_schema(candidate_articles),
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
                try:
                    selected, entries = validate_plan(
                        model_output,
                        candidate_articles=candidate_articles,
                        question_text=question_text,
                    )
                except SpecialPartPlanError as error:
                    if attempt == 2:
                        raise
                    correction_errors = error.errors
                    continue
                row = planned_candidate_row(
                    case_id=case_id,
                    selected_articles=selected,
                    entries=entries,
                    scope_note=str(model_output["scope_note"]),
                    broad_articles=tuple(broad[case_id].get("articles", ())),
                    usage=metadata.get("usage", {}),
                    planner_route=str(model_output["route"]),
                    corpus=corpus,
                )
                break
        temporary_case = cache_path.with_suffix(cache_path.suffix + ".tmp")
        temporary_case.write_text(
            json.dumps(row, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_case.replace(cache_path)
        output_rows.append(row)
        print(
            f"[{index}/{len(case_ids)}] {case_id} {row['scope_status']} "
            f"{len(row['broad_articles'])}->{len(row['articles'])} articles",
            flush=True,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output_rows),
        encoding="utf-8",
    )
    temporary.replace(args.out)
    print(f"wrote {len(output_rows)} plans to {args.out}")


if __name__ == "__main__":
    main()
