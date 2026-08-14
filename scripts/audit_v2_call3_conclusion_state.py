#!/usr/bin/env python3
"""Compare the state each closing sentence asserts against the state the plan required.

Completeness asks whether the anchor was mentioned at all.  This asks the F1/F2 question:
the plan said `주어진 사실만으로는 성부를 확정하기 어렵다` and the answer said `성립하지
않는다` (F1), or the plan said `성립하지 않는다` and the answer softened it to a reservation
(F2).

The match is lexical -- an anchor is located in the closing section by its offence name,
and the state is read from the keywords in the sentence that names it.  That is enough to
*flag* a divergence for a human, not to decide one: an anchor whose offence name never
appears verbatim, or whose sentence carries no state keyword, is reported as `unmatched`
rather than as a pass or a failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.runtime.answer_plan import (
    _normalize_offense_text,
    extract_final_conclusion_section,
    offense_label_variants,
)

_REQUIRED_LINE = re.compile(r"^\s*·\s*(?P<actor>\S+)\s*—\s*(?P<offense>[^:]+?)\s*:\s*(?P<state>.+)$")
_SENTENCE_SPLIT = re.compile(r"(?<=[.。])\s*|\n+")
_ACTOR = re.compile(r"[甲乙丙丁戊己庚辛]")

# Ordered: the first match wins, so the negative form is tested before the positive one
# it contains as a substring.
_STATE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("불성립", re.compile(r"성립하지\s*(?:않|아니)|성립되지\s*않|불성립|처벌(?:되지|할)\s*(?:않|수\s*없)")),
    (
        "미확정",
        # `확정하기 어렵다` and the nominalized `성부 확정 어려움` are the same holding.
        # `어렵` alone does not cover `어려움`/`어려운`: the ㅂ-irregular changes the stem,
        # so the two forms share only `어려` as a literal prefix.
        re.compile(r"(?:확정|단정|판단)(?:하기)?\s*(?:어렵|어려|곤란)|확정할\s*수\s*없|불분명"),
    ),
    # Never a bare `성립`: it is a prefix of `성립하지 않는다`, so `과실치사죄가 성립하지
    # 않는다` would read as an affirmative at the earlier offset.
    (
        "성립",
        re.compile(
            r"성립(?:한다|된다|하며|하고|하는|함|하나)|죄책을\s*진다|"
            # `공무집행방해죄의 기수범으로 처벌된다` asserts the offence just as plainly.
            r"처벌(?:된다|한다|받는다)|기수범으로"
        ),
    ),
]


def _state_of(text: str) -> str | None:
    positions: list[tuple[int, str]] = []
    for label, pattern in _STATE_PATTERNS:
        match = pattern.search(text)
        if match:
            positions.append((match.start(), label))
    if not positions:
        return None
    # The state governing the anchor is the one asserted first in the sentence.
    return min(positions)[1]


def _plan_state(raw: str) -> str | None:
    return _state_of(raw)


def _required_anchors(plan: dict[str, Any]) -> list[dict[str, str]]:
    anchors: list[dict[str, str]] = []
    for line in str(plan.get("required_final_conclusions") or "").splitlines():
        match = _REQUIRED_LINE.match(line)
        if not match:
            continue
        offense = re.sub(r"\s*\(.*?\)\s*$", "", match.group("offense")).strip()
        anchors.append(
            {
                "actor": match.group("actor"),
                "offense": offense,
                "plan_state": _plan_state(match.group("state")) or "unknown",
                "plan_line": line.strip(),
            }
        )
    return anchors


#: What a writer may insert inside an offence name without renaming the crime: whitespace,
#: and the particles that turn `위계공무집행방해죄` into `위계에 의한 공무집행방해죄`.
_NAME_FILLER = r"(?:\s|에\s*의(?:한|하여))*"


def _offense_pattern(name: str) -> re.Pattern[str]:
    return re.compile(_NAME_FILLER.join(re.escape(char) for char in name))


def _offense_spans(sentence: str, offense: str) -> list[tuple[int, int]]:
    """Spans of whole-name mentions of one offence, in the sentence as written.

    Two things have to hold at once.  The name must flex -- the answer may write
    `위계에 의한 공무집행방해죄` for `위계공무집행방해죄` -- and it must still be a whole
    name, because `강도상해죄` contains `상해죄` and a closing section that lists both would
    otherwise hand the shorter anchor the wrong carrier.  Stripping the text's whitespace
    to make the first work destroys the boundary the second needs (`강간죄 및 상해죄` becomes
    `강간죄및상해죄`), so the flexing belongs in the pattern, not in the text.
    """
    spans = []
    for name in offense_label_variants(offense):
        for match in _offense_pattern(name).finditer(sentence):
            before = sentence[match.start() - 1] if match.start() else ""
            if not re.match(r"[가-힣]", before):
                spans.append((match.start(), match.end()))
    return sorted(set(spans))


def _mentions_offense(sentence: str, offense: str) -> bool:
    return bool(_offense_spans(sentence, offense))


def _state_for_offense(sentence: str, offense: str) -> str | None:
    """The state this sentence asserts of this offence: the first one stated at or after it.

    One sentence disposes of several crimes in more than one shape.  Each can carry its own
    predicate (`존속살해죄는 성립하지 않는다, 주거침입죄는 확정하기 어렵다`); several can
    share one (`수뢰죄, 직무유기죄, 횡령죄는 모두 ... 확정하기 어렵다`); and a sentence can
    hold both at once (`준강도죄, 특수절도죄는 ... 어렵고, 상해죄는 기수가 된다`).

    Reading forward from the offence's own mention to the first state keyword handles all
    three: a shared predicate is the first one the earlier crimes reach, and a crime with
    its own predicate reaches that one before any later group's.  Cutting the clause at the
    next crime name instead loses the shared predicate, and falling back to the sentence's
    tail picks up the *last* group's predicate for crimes in the first.
    """
    spans = _offense_spans(sentence, offense)
    if not spans:
        return None
    return _state_of(sentence[spans[0][0] :])


def _attributed_sentences(text: str) -> list[tuple[str | None, str]]:
    """Sentences paired with the actor that governs them.

    Answers group conclusions under an actor heading (`1. 乙의 죄책`) and then omit the
    actor from each item, so a sentence carries the last actor named at or before it.
    """
    out: list[tuple[str | None, str]] = []
    current: str | None = None
    for part in _SENTENCE_SPLIT.split(text):
        sentence = part.strip()
        if not sentence:
            continue
        actors = _ACTOR.findall(sentence)
        if actors:
            current = actors[0]
        out.append((current, sentence))
    return out


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[str(row["sub_question_id"])] = row
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    answers = _rows(args.answers)
    plans = _rows(args.answer_plans)

    findings: list[dict[str, Any]] = []
    for case_id, answer_row in answers.items():
        plan = plans[case_id]
        closing = extract_final_conclusion_section(str(answer_row["answer"]))
        sentences = _attributed_sentences(closing)

        required = _required_anchors(plan)
        # Two anchors can share an actor and an offence and differ only in state (two
        # instances of the same crime).  The closing text names them identically, so they
        # are decided together as a group: the states the answer asserts must cover the
        # states the plan required.
        groups: dict[tuple[str, str], list[dict[str, str]]] = {}
        for anchor in required:
            groups.setdefault((anchor["actor"], anchor["offense"]), []).append(anchor)

        anchors: list[dict[str, Any]] = []
        for (actor, offense), group in groups.items():
            named = [(a, s) for a, s in sentences if _mentions_offense(s, offense)]
            carriers = [s for a, s in named if a == actor]
            if not carriers:
                carriers = [s for _, s in named]
            answer_states = {
                state
                for sentence in carriers
                if (state := _state_for_offense(sentence, offense))
            }
            plan_states = {anchor["plan_state"] for anchor in group}

            if not answer_states:
                verdict = "unmatched"
            elif answer_states == plan_states:
                verdict = "agrees"
            elif len(group) > 1 or len(answer_states) > 1:
                verdict = "ambiguous"
            else:
                verdict = "diverges"

            for anchor in group:
                anchors.append(
                    {
                        **anchor,
                        "instances": len(group),
                        "plan_states": sorted(plan_states),
                        "answer_state": sorted(answer_states) or None,
                        "verdict": verdict,
                    }
                )

        findings.append(
            {
                "case_id": case_id,
                "anchors": anchors,
                "counts": {
                    verdict: sum(1 for a in anchors if a["verdict"] == verdict)
                    for verdict in ("agrees", "diverges", "ambiguous", "unmatched")
                },
            }
        )

    summary = {
        "answers": str(args.answers),
        "cases": len(findings),
        "anchors": sum(len(f["anchors"]) for f in findings),
        **{
            verdict: sum(f["counts"][verdict] for f in findings)
            for verdict in ("agrees", "diverges", "ambiguous", "unmatched")
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for finding in findings:
        for anchor in finding["anchors"]:
            if anchor["verdict"] in {"diverges", "ambiguous"}:
                print(
                    f"  {finding['case_id']}: {anchor['actor']} {anchor['offense']} "
                    f"plan={anchor['plan_state']} answer={anchor['answer_state']} "
                    f"({anchor['verdict']})"
                )


if __name__ == "__main__":
    main()
