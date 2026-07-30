"""Run the compiled rulebase through the pinned native Scallop CLI.

Two things are deliberate here.

*Card statuses are rendered by the host, not by the model.* Call 2 returns JSON that the
host validates and then writes out as facts. A model that emitted Datalog text directly
would be writing code into the program -- the injection path the previous architecture had.

*Every requested relation must appear in the output.* ``scli`` 0.2.4 prints only declared
queries, and an undeclared relation is silently absent rather than an error -- that is how
the previous rulebase's 3,487 rules came to contribute nothing while appearing to run. The
program declares its queries, one invocation prints all of them, and a relation missing
from the output raises instead of reading as an empty result.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Iterable, Mapping, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"

VALID_STATUSES = frozenset({"satisfied", "not_satisfied", "unknown"})

_CASE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
_TUPLE_RE = re.compile(r"\(([^)]*)\)")
_ELEMENT_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


class ScallopError(RuntimeError):
    """Raised when the runtime cannot evaluate a program or parse its output."""


class StatusFactError(ValueError):
    """Raised before a malformed assessment can reach the program text."""


def render_card_statuses(
    case_id: str, statuses: Iterable[tuple[str, str]]
) -> str:
    """Render call 2's assessments as ``card_status`` facts.

    ``case_id`` is pattern-checked and card ids are emitted as quoted literals, so no
    model output reaches the program as syntax.
    """
    if not _CASE_ID_RE.fullmatch(case_id):
        raise StatusFactError(f"case_id must be a safe identifier, got {case_id!r}")
    rows: list[str] = []
    for card_id, status in statuses:
        if status not in VALID_STATUSES:
            raise StatusFactError(
                f"{card_id}: status {status!r} is not one of {sorted(VALID_STATUSES)}"
            )
        if '"' in card_id or "\\" in card_id:
            raise StatusFactError(f"card id is not a bare identifier: {card_id!r}")
        rows.append(f'  ("{case_id}", "{card_id}", "{status}"),')
    if not rows:
        return ""
    return "\n".join(["", "rel card_status = {", *sorted(rows), "}", ""])


def parse_query_output(output: str, relation: str) -> tuple[tuple[str, ...], ...]:
    """``foo: {("a", "b"), ("c", "d")}`` -> ``(("a","b"), ("c","d"))``.

    Raises when the relation is absent. An absent relation and an empty one look the same
    to a caller that defaults, and the difference is "the rule never ran" versus "the rule
    ran and concluded nothing".
    """
    match = re.search(
        rf"(?ms)^\s*{re.escape(relation)}\s*:\s*\{{(.*?)\}}\s*$", output
    )
    if match is None:
        raise ScallopError(
            f"{relation} is missing from the scli output; is it declared as a query? "
            f"got: {output!r}"
        )
    body = match.group(1).strip()
    if not body:
        return ()
    return tuple(
        tuple(_ELEMENT_RE.findall(inner)) for inner in _TUPLE_RE.findall(body)
    )


def run_program(
    program: str,
    query_relations: Sequence[str],
    work_dir: Path,
    *,
    name: str = "program",
    scli_path: Path | None = None,
    timeout: int = 300,
) -> Mapping[str, tuple[tuple[str, ...], ...]]:
    """Evaluate one program and return each requested relation's tuples.

    One invocation, because the program declares its queries and scli prints them all;
    running ``--query`` once per relation re-evaluates the whole program each time.
    """
    scli_path = scli_path or DEFAULT_SCLI
    if not scli_path.is_file():
        raise ScallopError(f"scli not found at {scli_path}")

    undeclared = sorted(
        relation
        for relation in query_relations
        if not re.search(rf"^query\s+{re.escape(relation)}\s*$", program, re.MULTILINE)
    )
    if undeclared:
        raise ScallopError(
            f"relations requested but not declared as queries: {undeclared}"
        )

    work_dir.mkdir(parents=True, exist_ok=True)
    program_path = work_dir / f"{name}.scl"
    program_path.write_text(program, encoding="utf-8")

    completed = subprocess.run(
        [str(scli_path), str(program_path)],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise ScallopError(
            f"scli failed on {name}: "
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )
    return {
        relation: parse_query_output(completed.stdout, relation)
        for relation in query_relations
    }


def runtime_version(scli_path: Path | None = None) -> str:
    completed = subprocess.run(
        [str(scli_path or DEFAULT_SCLI), "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return completed.stdout.strip()
