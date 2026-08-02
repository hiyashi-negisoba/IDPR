#!/usr/bin/env python3
"""Experiment: reconcile frozen Call 1.5 and retrieval candidates before Call 2.

The runner consumes an existing L0 artifact so retrieval rank is held constant across
prompt variants.  It emits both the model audit rows and a normal issue-first L0 file;
the production candidate builder and symbolic pipeline are reused without modification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.candidates import candidate_issues
from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.issue_pipeline import issue_candidate_row
from idpr.neural.article_reconcile import (
    ArticleReconcileError,
    reconciliation_payload,
    reconciliation_schema,
    validate_reconciliation,
)
from idpr.neural.article_select import attempt_article_map, load_catalog
from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2


def _rows(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _candidate_evidence(
    row: dict,
    *,
    selection_entries: dict[str, str],
    issue_by_id: dict,
    cards_by_id: dict,
    catalog_by_key: dict[str, dict[str, str]],
) -> list[dict]:
    model_articles = set(row.get("from_model", ()))
    attempt_articles = set(row.get("from_attempt_expansion", ()))
    retrieval: dict[str, tuple[int, object]] = {}
    for rank, issue_id in enumerate(row.get("retrieved_issue_ids", ()), start=1):
        issue = issue_by_id[issue_id]
        retrieval.setdefault(issue.article, (rank, issue))

    evidence: list[dict] = []
    for article in row["articles"]:
        if article in attempt_articles:
            continue
        entry = catalog_by_key[article]
        channels = []
        if article in model_articles:
            channels.append("model")
        if article in retrieval:
            channels.append("retrieval")
        candidate: dict = {
            "article": article,
            "label": entry["label"],
            "offense": entry["offense"],
            "admission_channels": channels,
        }
        if article in selection_entries:
            candidate["model_reason"] = selection_entries[article]
        if article in retrieval:
            rank, issue = retrieval[article]
            candidate["retrieval_rank"] = rank
            candidate["retrieved_issue"] = issue.title
            candidate["retrieved_rules"] = [
                cards_by_id[card_id].proposition
                for card_id in issue.retrieval_card_ids[:2]
            ]
        evidence.append(candidate)
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--l0-out", type=Path, required=True)
    parser.add_argument("--system-prompt", default="article_reconcile")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()

    inventory = {row["sub_question_id"]: row for row in _rows(args.inventory)}
    selections = {
        row["sub_question_id"]: {
            entry["article"]: entry["reason"] for entry in row.get("entries", ())
        }
        for row in _rows(args.selection)
    }
    candidate_rows = _rows(args.candidates)
    expected = set(inventory)
    actual = {row["sub_question_id"] for row in candidate_rows}
    if actual != expected:
        raise ValueError(f"candidate case ids differ: missing={expected-actual}, extra={actual-expected}")

    corpus = card_corpus()
    cards_by_id = corpus.by_id
    issues, _ = compile_issue_catalog_v2(corpus)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    catalog_by_key = {entry["key"]: entry for entry in load_catalog()}
    attempt_map = attempt_article_map()
    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)
    system_prompt = load_prompt(args.system_prompt)
    user_template = load_prompt("article_reconcile_user")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.l0_out.parent.mkdir(parents=True, exist_ok=True)
    audit_rows: list[dict] = []
    l0_rows: list[dict] = []
    for index, row in enumerate(candidate_rows, start=1):
        case_id = row["sub_question_id"]
        record = inventory[case_id]
        evidence = _candidate_evidence(
            row,
            selection_entries=selections.get(case_id, {}),
            issue_by_id=issue_by_id,
            cards_by_id=cards_by_id,
            catalog_by_key=catalog_by_key,
        )
        allowed = [candidate["article"] for candidate in evidence]
        payload = reconciliation_payload(
            case_id=case_id,
            question_text=scoped_question_text(
                record["question_text"], record.get("question_prompt", "")
            ),
            question_prompt=record.get("question_prompt", ""),
            candidates=evidence,
        )
        assert_no_leaked_fields(payload)
        output = None
        try:
            output, metadata = client.complete_json(
                system_prompt=system_prompt,
                payload=payload,
                schema_name="article_reconciliation",
                schema=reconciliation_schema(allowed),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=user_template,
            )
            kept, entries = validate_reconciliation(output, allowed_articles=allowed)
        except (ArticleReconcileError, VLLMClientError) as error:
            raise RuntimeError(f"{case_id}: reconciliation failed: {error}") from error

        kept_set = set(kept)
        model_kept = [article for article in row.get("from_model", ()) if article in kept_set]
        retrieved_issue_ids = [
            issue_id
            for issue_id in row.get("retrieved_issue_ids", ())
            if issue_by_id[issue_id].article in kept_set
        ]
        retrieval_kept = [issue_by_id[issue_id].article for issue_id in retrieved_issue_ids]
        scope = candidate_issues(
            selected=model_kept,
            retrieved=retrieval_kept,
            corpus=corpus,
            attempt_map=attempt_map,
        )
        audit_rows.append(
            {
                "sub_question_id": case_id,
                "policy": args.system_prompt,
                "candidate_articles": allowed,
                "selected": list(kept),
                "removed": [article for article in allowed if article not in kept_set],
                "entries": list(entries),
                "usage": metadata.get("usage", {}),
            }
        )
        l0_rows.append(
            issue_candidate_row(
                case_id,
                scope,
                retrieved_issue_ids=retrieved_issue_ids,
            )
        )
        print(
            f"[{index}/{len(candidate_rows)}] {case_id}: "
            f"{len(allowed)} -> {len(scope.articles)} articles / "
            f"{len(scope.initial_issues)} initial issues"
        )

    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in audit_rows),
        encoding="utf-8",
    )
    args.l0_out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in l0_rows),
        encoding="utf-8",
    )
    print(f"wrote {args.out}")
    print(f"wrote {args.l0_out}")


if __name__ == "__main__":
    main()
