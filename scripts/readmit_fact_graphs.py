"""Re-admit saved call-1 outputs after an admission-logic change, without the model.

``run_call1_fact_graphs.py`` keeps the raw payload whenever anything was dropped, so a
change to what the host admits can be applied to an existing run instead of paying for
another GPU pass. The model output is byte-identical to what the run produced; only the
host's decision about which facts to accept is recomputed.

This is not a way to relax the gate until the numbers improve. The admitted set is written
with its drop counts, and those counts are what the report publishes as extraction quality.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.neural.fact_graph import FactGraphError, admit_fact_graph

DEFAULT_PATH = PROJECT_ROOT / "data" / "eval" / "fact_graphs.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    question_text = {
        json.loads(line)["sub_question_id"]: json.loads(line)["question_text"]
        for line in args.inventory.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }

    rows = [
        json.loads(line)
        for line in args.path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    admitted = failed = 0
    drops: Counter[str] = Counter()
    out_rows: list[dict] = []
    for row in rows:
        case_id = row["sub_question_id"]
        raw = row.get("rejected_payload") or row.get("fact_graph")
        if raw is None:
            out_rows.append(row)
            failed += 1
            continue
        fresh: dict = {"sub_question_id": case_id}
        if "usage" in row:
            fresh["usage"] = row["usage"]
        try:
            admission = admit_fact_graph(
                raw, case_id=case_id, question_text=question_text[case_id]
            )
        except FactGraphError as error:
            fresh["error"] = f"FactGraphError: {error}"
            fresh["errors"] = error.errors
            fresh["rejected_payload"] = raw
            failed += 1
        else:
            fresh["fact_graph"] = admission.payload
            fresh["admission"] = admission.as_dict()
            if admission.dropped_total:
                fresh["rejected_payload"] = raw
            drops.update(admission.dropped)
            admitted += 1
        out_rows.append(fresh)

    target = args.out or args.path
    target.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in out_rows) + "\n",
        encoding="utf-8",
    )
    print(f"admitted={admitted} failed={failed} of {len(rows)}")
    print(f"dropped={dict(drops)}")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
