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

from idpr.eval.input_formatter import assert_no_leaked_fields
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


def load_inventory(path: Path) -> list[dict]:
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
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=0, help="0 = every question")
    args = parser.parse_args()

    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt = load_prompt(SYSTEM_PROMPT)
    user_template = load_prompt(USER_PROMPT)
    schema = fact_graph_schema()

    records = load_inventory(args.inventory)
    if args.limit:
        records = records[: args.limit]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    ok = failed = 0
    total_tokens = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for index, record in enumerate(records, start=1):
            case_id = record["sub_question_id"]
            payload = {
                "case_id": case_id,
                "case_text": record["question_text"],
                "question_prompt": record.get("question_prompt", ""),
            }
            assert_no_leaked_fields(payload)

            row: dict = {"sub_question_id": case_id}
            try:
                output, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="fact_graph",
                    schema=schema,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    user_template=user_template,
                )
                admission = admit_fact_graph(
                    output, case_id=case_id, question_text=record["question_text"]
                )
                row["fact_graph"] = admission.payload
                row["admission"] = admission.as_dict()
                if admission.dropped_total:
                    # Never silent: extraction quality is a reported number.
                    row["rejected_payload"] = output
                row["usage"] = metadata.get("usage", {})
                total_tokens += int(metadata.get("usage", {}).get("total_tokens", 0) or 0)
                ok += 1
            except FactGraphError as error:
                # Recorded, not raised: one malformed graph must not cost the other 60.
                # The rejected payload is kept: without it a contract violation cannot be
                # told apart from a hallucination without paying for the GPU run again.
                row["error"] = f"{type(error).__name__}: {error}"
                row["errors"] = error.errors
                row["rejected_payload"] = output
                failed += 1
            except VLLMClientError as error:
                row["error"] = f"{type(error).__name__}: {error}"
                failed += 1
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            if "error" in row:
                status = "FAIL"
            else:
                drops = row["admission"]["dropped_total"]
                status = "ok" if not drops else f"ok (-{drops})"
            print(f"[{index}/{len(records)}] {case_id} {status}")

    print(f"ok={ok} failed={failed} total_tokens={total_tokens}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
