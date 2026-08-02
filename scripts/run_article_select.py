"""Call 1.5 over the KCL inventory: article selection from the full 51-article catalog.

Written to disk as an artifact for the same reason call 1 is: the measurement half runs on
CPU and must be re-runnable without paying for the model again, and a recall miss has to be
readable afterwards -- the model's per-article ``reason`` is the record of why it picked
what it picked.

Input whitelist is enforced, not documented: the payload carries ``question_text``,
``question_prompt`` and the host's article catalog, and ``assert_no_leaked_fields`` gates
it before the request goes out.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.neural.article_select import (
    ArticleSelectError,
    article_select_schema,
    expand_attempt_articles,
    load_catalog,
    selection_payload,
    validate_selection,
)
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt

DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
SYSTEM_PROMPT = "article_select"
USER_PROMPT = "article_select_user"


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
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=0, help="0 = every question")
    args = parser.parse_args()

    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt = load_prompt(SYSTEM_PROMPT)
    user_template = load_prompt(USER_PROMPT)
    catalog = load_catalog()
    schema = article_select_schema(catalog)

    records = load_inventory(args.inventory)
    if args.limit:
        records = records[: args.limit]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    ok = failed = 0
    total_tokens = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for index, record in enumerate(records, start=1):
            case_id = record["sub_question_id"]
            question_prompt = record.get("question_prompt", "")
            payload = selection_payload(
                case_id=case_id,
                question_text=scoped_question_text(
                    record["question_text"], question_prompt
                ),
                question_prompt=question_prompt,
                catalog=catalog,
            )
            assert_no_leaked_fields(payload)

            row: dict = {"sub_question_id": case_id}
            output = None
            try:
                output, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="article_selection",
                    schema=schema,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                    user_template=user_template,
                )
                selected, entries = validate_selection(output, catalog=catalog)
                expanded = expand_attempt_articles(selected)
                row["selected"] = list(selected)
                row["articles"] = list(expanded)
                # Reported separately so the deterministic half of the recall is visible.
                row["attempt_expansion"] = [a for a in expanded if a not in set(selected)]
                row["entries"] = list(entries)
                row["usage"] = metadata.get("usage", {})
                total_tokens += int(metadata.get("usage", {}).get("total_tokens", 0) or 0)
                ok += 1
            except ArticleSelectError as error:
                # Recorded, not raised: one malformed response must not cost the other 60.
                row["error"] = f"{type(error).__name__}: {error}"
                row["errors"] = error.errors
                row["rejected_payload"] = output
                failed += 1
            except VLLMClientError as error:
                row["error"] = f"{type(error).__name__}: {error}"
                failed += 1
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            handle.flush()
            count = len(row.get("articles", ()))
            status = "FAIL" if "error" in row else f"ok ({count} articles)"
            print(f"[{index}/{len(records)}] {case_id} {status}")

    print(f"ok={ok} failed={failed} total_tokens={total_tokens}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
