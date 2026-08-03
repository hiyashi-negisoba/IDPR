"""Call 1 over the KCL inventory: facts plus proposed offences, one call per question.

Runs against a job-local vLLM server. The output is an artifact rather than an in-memory
step so the retrieval half can be re-run and re-measured without paying for the model
again -- and so a fact graph can be read by a human when a recall number looks wrong.

Input whitelist is enforced here, not documented here: the payload is built from
``question_text`` and ``question_prompt`` only, and ``assert_no_leaked_fields`` gates it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.neural.fact_graph import (
    FactGraphError,
    admit_fact_graph,
    fact_graph_schema,
)
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt

DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
SYSTEM_PROMPT = "fact_graph_extract"
USER_PROMPT = "fact_graph_extract_user"
REPAIR_PROMPT = "fact_graph_contract_repair"


def load_inventory(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def restore_previous_graph(
    failed_row: dict, *, previous_row: dict | None
) -> dict:
    """Keep a previously admitted graph when regeneration fails, with provenance."""
    if not previous_row or "fact_graph" not in previous_row:
        return failed_row
    restored = {
        "sub_question_id": failed_row["sub_question_id"],
        "fact_graph": previous_row["fact_graph"],
        "admission": previous_row.get("admission", {}),
        "usage": previous_row.get("usage", {}),
        "fallback": {
            "kind": "previous_valid_fact_graph",
            "regeneration_error": failed_row.get(
                "error", "unknown regeneration error"
            )[:1000],
            "regeneration_errors": failed_row.get("errors", []),
            "regeneration_usage": failed_row.get("usage", {}),
        },
    }
    return restored


def select_records_for_run(
    records: list[dict],
    *,
    requested_case_ids: list[str],
    retry_rows: list[dict],
    limit: int,
) -> tuple[list[dict], dict[str, dict]]:
    """Select an explicit subset or the failed rows from a previous Call-1 artifact."""

    indexed = {str(record["sub_question_id"]): record for record in records}
    if len(indexed) != len(records):
        raise ValueError("inventory contains duplicate sub_question_id values")
    retry_index = {str(row["sub_question_id"]): row for row in retry_rows}
    if len(retry_index) != len(retry_rows):
        raise ValueError("retry artifact contains duplicate sub_question_id values")
    if requested_case_ids and retry_rows:
        raise ValueError("--case-id and --retry-failures-from are mutually exclusive")
    if requested_case_ids:
        unknown = sorted(set(requested_case_ids) - set(indexed))
        if unknown:
            raise ValueError(f"unknown --case-id values: {unknown}")
        wanted = set(requested_case_ids)
        selected = [record for record in records if record["sub_question_id"] in wanted]
    elif retry_rows:
        unknown = sorted(set(retry_index) - set(indexed))
        if unknown:
            raise ValueError(f"retry artifact has unknown cases: {unknown}")
        failed = {
            case_id
            for case_id, row in retry_index.items()
            if not isinstance(row.get("fact_graph"), dict)
        }
        selected = [record for record in records if record["sub_question_id"] in failed]
        if not selected:
            raise ValueError("retry artifact has no failed fact graphs")
    else:
        selected = records
    if limit:
        selected = selected[:limit]
    return selected, retry_index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--fallback-fact-graphs",
        type=Path,
        help="reuse a previously valid graph when regeneration fails",
    )
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=0, help="0 = every question")
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument(
        "--retry-failures-from",
        type=Path,
        help="run only rows without an admitted fact_graph in this prior artifact",
    )
    parser.add_argument(
        "--contract-attempts",
        type=int,
        default=1,
        help="bounded attempts per selected case, including the first request",
    )
    args = parser.parse_args()
    if args.contract_attempts < 1:
        parser.error("--contract-attempts must be positive")

    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt = load_prompt(SYSTEM_PROMPT)
    user_template = load_prompt(USER_PROMPT)
    repair_prompt = load_prompt(REPAIR_PROMPT)
    schema = fact_graph_schema()

    records = load_inventory(args.inventory)
    retry_rows = (
        load_inventory(args.retry_failures_from)
        if args.retry_failures_from and args.retry_failures_from.is_file()
        else []
    )
    records, retry_index = select_records_for_run(
        records,
        requested_case_ids=args.case_id,
        retry_rows=retry_rows,
        limit=args.limit,
    )
    fallback_rows = {
        row["sub_question_id"]: row
        for row in (
            load_inventory(args.fallback_fact_graphs)
            if args.fallback_fact_graphs and args.fallback_fact_graphs.is_file()
            else []
        )
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    ok = reused = failed = 0
    total_tokens = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for index, record in enumerate(records, start=1):
            case_id = record["sub_question_id"]
            question_prompt = record.get("question_prompt", "")
            payload = {
                "case_id": case_id,
                "case_text": scoped_question_text(
                    record["question_text"], question_prompt
                ),
                "question_prompt": question_prompt,
            }
            assert_no_leaked_fields(payload)

            row: dict = {"sub_question_id": case_id}
            previous_failure = retry_index.get(case_id, {})
            rejected_output = previous_failure.get("rejected_payload")
            host_errors = list(previous_failure.get("errors", []))
            attempts: list[dict] = []
            for attempt in range(1, args.contract_attempts + 1):
                active_payload = dict(payload)
                if rejected_output is not None or host_errors:
                    active_payload["contract_repair"] = {
                        "instruction": repair_prompt,
                        "host_errors": host_errors,
                        "previous_output": rejected_output,
                    }
                output = None
                try:
                    output, metadata = client.complete_json(
                        system_prompt=system_prompt,
                        payload=active_payload,
                        schema_name="fact_graph",
                        schema=schema,
                        max_tokens=args.max_tokens,
                        temperature=args.temperature,
                        user_template=user_template,
                    )
                    usage = metadata.get("usage", {})
                    total_tokens += int(usage.get("total_tokens", 0) or 0)
                    admission = admit_fact_graph(
                        output, case_id=case_id, question_text=record["question_text"]
                    )
                except FactGraphError as error:
                    attempts.append(
                        {"attempt": attempt, "usage": usage, "errors": error.errors}
                    )
                    rejected_output = output
                    host_errors = list(error.errors)
                    if attempt == args.contract_attempts:
                        row["error"] = f"{type(error).__name__}: {error}"
                        row["errors"] = error.errors
                        row["rejected_payload"] = output
                except VLLMClientError as error:
                    attempts.append({"attempt": attempt, "errors": [str(error)]})
                    host_errors = [str(error)]
                    if attempt == args.contract_attempts:
                        row["error"] = f"{type(error).__name__}: {error}"
                else:
                    attempts.append({"attempt": attempt, "usage": usage, "errors": []})
                    row["usage"] = usage
                    row["fact_graph"] = admission.payload
                    row["admission"] = admission.as_dict()
                    if admission.dropped_total:
                        # Never silent: extraction quality is a reported number.
                        row["rejected_payload"] = output
                    if previous_failure:
                        row["repair"] = {
                            "kind": "host_contract_repair",
                            "source_errors": previous_failure.get("errors", []),
                        }
                    ok += 1
                    break
            row["contract_attempts"] = attempts
            if "error" in row:
                row = restore_previous_graph(row, previous_row=fallback_rows.get(case_id))
                if "fallback" in row:
                    reused += 1
                else:
                    failed += 1
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            if "fallback" in row:
                status = "fallback"
            elif "error" in row:
                status = "FAIL"
            else:
                drops = row["admission"]["dropped_total"]
                status = "ok" if not drops else f"ok (-{drops})"
            print(f"[{index}/{len(records)}] {case_id} {status}")

    print(f"ok={ok} fallback={reused} failed={failed} total_tokens={total_tokens}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
