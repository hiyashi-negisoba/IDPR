"""Call 1.5 over the KCL inventory: fact-linked routing from the normalized catalog.

Written to disk as an artifact for the same reason call 1 is: the measurement half runs on
CPU and must be re-runnable without paying for the model again, and a recall miss has to be
readable afterwards -- the model's per-article ``reason`` is the record of why it picked
what it picked.

Input whitelist is enforced, not documented: the payload carries ``question_text``,
``question_prompt``, Call 1's grounded issue hints and the host's article catalog.
``assert_no_leaked_fields`` gates it before the request goes out.
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
    selectable_catalog,
    selection_payload,
    validate_selection,
)
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt

DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"
SYSTEM_PROMPT = "article_select"
USER_PROMPT = "article_select_user"


def load_inventory(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def retrieval_articles(row: dict) -> list[str]:
    """Read the untouched ranked lane, including legacy artifacts losslessly when possible."""
    if "retrieved_articles" in row:
        return list(dict.fromkeys(row["retrieved_articles"]))
    if row.get("retrieved_issue_ids"):
        return list(
            dict.fromkeys(issue_id.split(".", 1)[0] for issue_id in row["retrieved_issue_ids"])
        )
    return list(dict.fromkeys(row.get("from_retrieval", ())))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument(
        "--retrieval-candidates",
        type=Path,
        help="optional prior retrieval artifact whose from_retrieval list is reranked",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=0, help="0 = every question")
    args = parser.parse_args()

    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt = load_prompt(SYSTEM_PROMPT)
    user_template = load_prompt(USER_PROMPT)
    # The source catalog covers the whole corpus. Generic attempt provisions are removed
    # from the model enum and restored from the selected base offences after validation.
    catalog = selectable_catalog(load_catalog())
    selectable_keys = {entry["key"] for entry in catalog}

    records = load_inventory(args.inventory)
    fact_graphs = {
        row["sub_question_id"]: row["fact_graph"]
        for row in load_inventory(args.fact_graphs)
    }
    retrieval_candidates = {
        row["sub_question_id"]: retrieval_articles(row)
        for row in (
            load_inventory(args.retrieval_candidates)
            if args.retrieval_candidates
            else []
        )
    }
    if args.limit:
        records = records[: args.limit]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    ok = failed = 0
    total_tokens = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for index, record in enumerate(records, start=1):
            case_id = record["sub_question_id"]
            if case_id not in fact_graphs:
                raise ValueError(f"fact graph artifact is missing {case_id}")
            question_prompt = record.get("question_prompt", "")
            retrieval_hints = tuple(
                article
                for article in dict.fromkeys(retrieval_candidates.get(case_id, ()))
                if article in selectable_keys
            )
            payload = selection_payload(
                case_id=case_id,
                question_text=scoped_question_text(
                    record["question_text"], question_prompt
                ),
                question_prompt=question_prompt,
                issue_hints=fact_graphs[case_id].get("issue_candidates", ()),
                retrieval_hints=retrieval_hints,
                catalog=catalog,
            )
            assert_no_leaked_fields(payload)
            schema = article_select_schema(
                catalog, retrieval_hints=retrieval_hints
            )

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
                selected, entries = validate_selection(
                    output, catalog=catalog, retrieval_hints=retrieval_hints
                )
                expanded = expand_attempt_articles(selected)
                row["question_domain"] = output["question_domain"]
                row["model_selected"] = [
                    entry["article"]
                    for entry in output["selected"]
                    if entry["article"] != "no_substantive_offense"
                ]
                row["candidate_decisions"] = [
                    {"article": article, **dict(decision)}
                    for article, decision in zip(
                        retrieval_hints,
                        output["candidate_decisions"],
                        strict=True,
                    )
                ]
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
