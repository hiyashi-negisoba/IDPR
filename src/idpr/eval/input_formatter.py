"""
input_formatter.py
Preprocesses KCL benchmark items (kcl_criminal_v1_draft.jsonl) into structured inputs
tailored specifically for each baseline (Vanilla, CoT, Standard RAG, LegalChainReasoner, LePREC, ACAL, FOL Solver).

Fairness invariant
------------------
Only the fields in ``ALLOWED_INPUT_FIELDS`` may be derived from a benchmark record and
handed to a method. Everything else in the inventory record is annotation produced for
grading or coverage planning -- notably ``rubric_summary`` (the grading checklist),
``issue_tags`` (which name the very issues the rubric asks about), ``rubric_count``,
``legal_area``, ``covered``/``coverage_*`` and the review notes. Passing any of those to a
method under evaluation leaks the answer key.

``assert_no_leaked_fields`` enforces this and is exercised by the test suite, so a future
formatter cannot quietly reintroduce a leak.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

#: The only benchmark fields any method may see. ``sub_question_id`` is a join key, not
#: content -- it is echoed back in the output record so results can be matched to cases.
ALLOWED_INPUT_FIELDS = frozenset({"sub_question_id", "question_text", "question_prompt"})

#: Inventory fields that would leak grading or planning annotation into a prompt.
LEAKING_FIELDS = frozenset({
    "rubric_summary",
    "rubric_count",
    "issue_tags",
    "legal_area",
    "norm_types",
    "covered",
    "coverage_candidate",
    "coverage_notes",
    "coverage_review_status",
    "notes",
    "review_notes",
    "review_status",
    "source",
    "supporting_precedents",
})


class InputLeakageError(AssertionError):
    """Raised when a formatted input carries grading or planning annotation."""


_SCOPE_REFERENCE = re.compile(r"(?:사실관계\s*)?\((\d+)\)")
_STANDALONE_SCOPE = re.compile(
    r"사실관계\s*\((\d+)\)\s*(?:과|와)\s*관련하여,?"
)
_NUMBERED_FACT = re.compile(r"(?m)^\s*\((\d+)\)\s*")


def scoped_question_text(question_text: str, question_prompt: str) -> str:
    """Return the fact blocks explicitly named by the question prompt.

    The parser uses source labels only; it does not inspect rubrics or infer legal
    relevance. If a requested label cannot be resolved, the original text is returned.
    """
    references = tuple(
        dict.fromkeys(int(value) for value in _SCOPE_REFERENCE.findall(question_prompt))
    )
    if not references:
        return question_text

    parts = [part.strip() for part in re.split(r"\n\s*\n", question_text) if part.strip()]
    for index, part in enumerate(parts):
        match = _STANDALONE_SCOPE.fullmatch(part)
        if match and int(match.group(1)) in references:
            narrative = [
                line.strip()
                for preceding in parts[:index]
                for line in preceding.splitlines()
                if line.strip()
            ]
            if narrative and max(references) <= len(narrative):
                selected = [narrative[number - 1] for number in references]
                return "\n\n".join([*selected, *parts[index:]])

    if len(parts) < 2:
        return question_text
    fact_body = "\n\n".join(parts[:-1])
    markers = list(_NUMBERED_FACT.finditer(fact_body))
    if not markers:
        return question_text
    blocks = {
        int(marker.group(1)): fact_body[
            marker.start() : (
                markers[position + 1].start()
                if position + 1 < len(markers)
                else len(fact_body)
            )
        ].strip()
        for position, marker in enumerate(markers)
    }
    if not all(reference in blocks for reference in references):
        return question_text
    return "\n\n".join([*(blocks[reference] for reference in references), parts[-1]])


def assert_no_leaked_fields(formatted_input: Dict[str, Any]) -> None:
    """Fail loudly if a formatted input carries answer-key annotation.

    Checks both the top-level keys and any nested string content, so a leak cannot hide
    inside a rendered prompt fragment.
    """
    leaked = sorted(LEAKING_FIELDS & set(formatted_input))
    if leaked:
        raise InputLeakageError(
            f"formatted input leaks grading/planning annotation: {leaked}"
        )


class BaselineInputFormatter:
    """Formatter to adapt KCL raw benchmark records into baseline-specific input schemas."""

    @staticmethod
    def extract_facts(case_data: Dict[str, Any]) -> List[str]:
        """Splits full question_text into discrete factual sentence units."""
        raw_text = case_data.get("question_text", "")
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        sentences = []
        for line in lines:
            for part in line.split(". "):
                part = part.strip()
                if part:
                    if not part.endswith("."):
                        part += "."
                    sentences.append(part)
        return sentences

    @classmethod
    def _core(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """The whitelisted core every baseline is entitled to: the question and nothing else."""
        return {
            "sub_question_id": case_data.get("sub_question_id"),
            "question_text": case_data.get("question_text", ""),
            "question_prompt": case_data.get("question_prompt", ""),
        }

    @classmethod
    def format_vanilla(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for Vanilla Zero-shot LLM."""
        return cls._core(case_data)

    @classmethod
    def format_cot(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for Chain-of-Thought (CoT) Prompting."""
        formatted = cls._core(case_data)
        formatted["cot_steps"] = [
            "1. Issue Identification (쟁점 도출)",
            "2. Substantive Element Analysis (구성요건 검토)",
            "3. Defense Rejection (위법성·책임 조각 및 항변 배척)",
            "4. Final Offense & Concurrence Verdict (죄책 및 죄수 결론)",
        ]
        return formatted

    @classmethod
    def format_standard_rag(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for Standard RAG. The baseline runs its own BM25 retrieval over
        the precedent corpus, so no retrieved context is injected here."""
        return cls._core(case_data)

    @classmethod
    def format_legal_chain(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for LegalChainReasoner sub-agent chain."""
        formatted = cls._core(case_data)
        formatted["fact_sentences"] = cls.extract_facts(case_data)
        return formatted

    @classmethod
    def format_leprec(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for LePREC Legal Factor Classification.

        The full fact pattern is supplied. An earlier revision truncated this to the first
        10 sentences, which dropped 590 of 1,187 sentences across the 61-question set (48
        questions affected) and left LePREC arguing from half a fact pattern.
        """
        formatted = cls._core(case_data)
        formatted["fact_sentences"] = cls.extract_facts(case_data)
        return formatted

    @classmethod
    def format_acal(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for ACAL QBAF Formal Argumentation Framework."""
        formatted = cls._core(case_data)
        formatted["fact_pattern"] = case_data.get("question_text", "")
        return formatted

    @classmethod
    def format_fol_solver(cls, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats input for FOL Autoformalizer + Theorem Prover."""
        facts = cls.extract_facts(case_data)
        formatted = cls._core(case_data)
        formatted["fact_units"] = facts
        formatted["autoformalization_target"] = (
            f"Autoformalize {len(facts)} facts into First-Order Predicates."
        )
        return formatted
