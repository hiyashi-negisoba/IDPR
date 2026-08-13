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
_COUNTERFACTUAL_REPLACEMENT = re.compile(
    r"밑줄친\s*부분을\s*<u>\s*(.*?)\s*</u>\s*로\s*바꿀\s*경우",
    re.DOTALL,
)
_UNDERLINED_TEXT = re.compile(r"<u>.*?</u>", re.DOTALL)
_DIRECT_SCOPE_PREFIX = re.compile(
    r"^(?:(?:사실관계\s*)?\(\d+\)\s*(?:과|와)\s*관련하여,?|"
    r"(?:사실관계\s*|위\s*사례\s*)?\(\d+\)"
    r"(?:\s*(?:과|와)\s*\(\d+\))*\s*에서)\s*"
)
_RESPONSIBILITY_ACTOR = re.compile(r"[甲乙丙丁戊己庚辛壬癸]")


def _direct_question_prompt(question_prompt: str) -> str:
    replacement = _COUNTERFACTUAL_REPLACEMENT.search(question_prompt)
    if replacement:
        return question_prompt[replacement.end() :].strip()
    return _DIRECT_SCOPE_PREFIX.sub("", question_prompt, count=1).strip()


def _apply_counterfactual_replacement(scope: str, question_prompt: str) -> str:
    """Turn an explicitly authored fact replacement into a direct fact question."""
    match = _COUNTERFACTUAL_REPLACEMENT.search(question_prompt)
    if not match:
        return scope

    replacement = match.group(1).strip()
    for opening, closing in (("'", "'"), ('"', '"'), ("‘", "’"), ("“", "”")):
        if replacement.startswith(opening) and replacement.endswith(closing):
            replacement = replacement[len(opening) : -len(closing)].strip()
            break

    normalized = _UNDERLINED_TEXT.sub(f"<u>{replacement}</u>", scope, count=1)
    return normalized


def _compose_scope(facts: List[str], question_prompt: str) -> str:
    direct_prompt = _direct_question_prompt(question_prompt)
    scope = "\n\n".join([*facts, direct_prompt] if direct_prompt else facts)
    return _apply_counterfactual_replacement(scope, question_prompt)


def _expand_explicit_fact_dependencies(
    blocks: Dict[int, str], references: tuple[int, ...]
) -> tuple[int, ...]:
    """Include numbered facts explicitly presupposed by a selected fact block."""
    selected = set(references)
    changed = True
    while changed:
        changed = False
        for number in tuple(selected):
            block = blocks.get(number, "")
            dependencies = {
                int(value) for value in _SCOPE_REFERENCE.findall(block)
                if int(value) != number
            }
            if (
                number > 1
                and re.match(rf"^\s*\({number}\)\s*다음\s*날", block)
                and "위 범행" in block
            ):
                dependencies.add(number - 1)
            for dependency in dependencies:
                if dependency in blocks and dependency not in selected:
                    selected.add(dependency)
                    changed = True
    return tuple(sorted(selected))


def scoped_question_text(question_text: str, question_prompt: str) -> str:
    """Return the fact blocks explicitly named by the question prompt.

    The parser uses source labels only; it does not inspect rubrics or infer legal
    relevance. If a requested label cannot be resolved, the original text is returned.
    """
    references = tuple(
        dict.fromkeys(int(value) for value in _SCOPE_REFERENCE.findall(question_prompt))
    )
    parts = [part.strip() for part in re.split(r"\n\s*\n", question_text) if part.strip()]
    if not references:
        if question_text.rstrip().endswith(question_prompt.strip()):
            fact_body = question_text.rstrip()[: -len(question_prompt.strip())].strip()
            markers = list(_NUMBERED_FACT.finditer(fact_body))
            actors = tuple(dict.fromkeys(_RESPONSIBILITY_ACTOR.findall(question_prompt)))
            if markers and actors:
                blocks = [
                    fact_body[
                        marker.start() : (
                            markers[position + 1].start()
                            if position + 1 < len(markers)
                            else len(fact_body)
                        )
                    ].strip()
                    for position, marker in enumerate(markers)
                ]
                selected = [block for block in blocks if any(actor in block for actor in actors)]
                if selected:
                    return _compose_scope(selected, question_prompt)
            return _compose_scope([fact_body], question_prompt)
        return _apply_counterfactual_replacement(question_text, question_prompt)

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
                return _compose_scope(selected, question_prompt)

    leading_scope = _STANDALONE_SCOPE.match(question_prompt)
    if leading_scope and len(parts) >= 2:
        narrative = [
            line.strip()
            for preceding in parts[:-1]
            for line in preceding.splitlines()
            if line.strip()
        ]
        if narrative and max(references) <= len(narrative):
            selected = [narrative[number - 1] for number in references]
            return _compose_scope(selected, question_prompt)

    if len(parts) < 2:
        return _apply_counterfactual_replacement(question_text, question_prompt)
    fact_body = "\n\n".join(parts[:-1])
    markers = list(_NUMBERED_FACT.finditer(fact_body))
    if not markers:
        return _apply_counterfactual_replacement(question_text, question_prompt)
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
        return _apply_counterfactual_replacement(question_text, question_prompt)
    expanded = _expand_explicit_fact_dependencies(blocks, references)
    return _compose_scope([blocks[reference] for reference in expanded], question_prompt)


def target_fact_source_spans(
    question_text: str, question_prompt: str
) -> tuple[tuple[int, int], ...] | None:
    """Locate only the numbered facts explicitly selected by the question.

    Dependency closure remains available as factual context, but is deliberately
    excluded here so an earlier episode cannot silently become an independent
    liability target. ``None`` means no safe numbered boundary was recoverable.
    """
    references = tuple(
        dict.fromkeys(int(value) for value in _SCOPE_REFERENCE.findall(question_prompt))
    )
    if not references:
        return None
    stripped = question_text.rstrip()
    prompt = question_prompt.strip()
    fact_end = len(stripped) - len(prompt) if stripped.endswith(prompt) else len(question_text)
    markers = list(_NUMBERED_FACT.finditer(question_text[:fact_end]))
    if not markers:
        return None
    spans = {
        int(marker.group(1)): (
            marker.start(),
            markers[position + 1].start()
            if position + 1 < len(markers)
            else fact_end,
        )
        for position, marker in enumerate(markers)
    }
    if not all(reference in spans for reference in references):
        return None
    selected = tuple(spans[reference] for reference in references)
    prompt_start = stripped.rfind(prompt)
    if prompt_start >= 0:
        # The prompt may itself author a new hypothesis or replacement fact.  It is
        # target evidence, whereas dependency-closure blocks remain context-only.
        selected = (*selected, (prompt_start, prompt_start + len(prompt)))
    return selected


def assert_no_leaked_fields(formatted_input: Dict[str, Any]) -> None:
    """Fail loudly if a formatted input carries answer-key annotation.

    Checks both the top-level keys and any nested string content, so a leak cannot hide
    inside a rendered prompt fragment.
    """
    def keys(value: Any) -> set[str]:
        if isinstance(value, dict):
            return set(value) | {
                nested
                for child in value.values()
                for nested in keys(child)
            }
        if isinstance(value, (list, tuple)):
            return {nested for child in value for nested in keys(child)}
        return set()

    leaked = sorted(LEAKING_FIELDS & keys(formatted_input))
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
