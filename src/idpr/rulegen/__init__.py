"""Rule draft helpers."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
RULE_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")
CONTRACT_ROOT = Path(__file__).resolve().parents[3] / "docs/contracts"


@dataclass(frozen=True, slots=True)
class RuleDraft:
    rule_id: str
    source_ref: str
    body: str


class RuleIRValidationError(ValueError):
    """Raised when model-produced rule IR is not safe to compile."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid RuleIR:\n- " + "\n- ".join(errors))


class RuleIRGenerationContractError(ValueError):
    """Raised when a valid RuleIR does not implement the approved generation contract."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid full RuleIR generation:\n- " + "\n- ".join(errors))


class NormCandidateValidationError(ValueError):
    """Raised when one raw API extraction batch fails provenance checks."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid NormCandidateBatch:\n- " + "\n- ".join(errors))


class NormCardValidationError(ValueError):
    """Raised when normalized cards are not reviewable or source-grounded."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid NormCardSet:\n- " + "\n- ".join(errors))


class RulegenCritiqueValidationError(ValueError):
    """Raised when a critic exceeds its contract or returns inconsistent findings."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid RulegenCritiqueReport:\n- " + "\n- ".join(errors))


class NormCandidatePatchValidationError(ValueError):
    """Raised when an adjudicated candidate patch is unsafe or inconsistent."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("Invalid NormCandidatePatch:\n- " + "\n- ".join(errors))


def write_rule_draft(draft: RuleDraft, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{draft.rule_id}.scl"
    output_path.write_text(
        "\n".join(
            [
                f"// rule_id: {draft.rule_id}",
                "// status: draft",
                "// legal_review: pending",
                f"// source_ref: {draft.source_ref}",
                "",
                draft.body.rstrip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output_path


def validate_norm_candidate_batch(
    payload: Mapping[str, Any],
    request: Mapping[str, Any],
) -> None:
    """Validate one extraction response against the exact request commentary."""

    errors = _schema_errors(payload, "norm_candidate_batch.schema.json")
    if errors:
        raise NormCandidateValidationError(errors)
    if payload.get("request_id") != request.get("request_id"):
        errors.append("request_id does not match the extraction request")
    if payload.get("status") != "draft":
        errors.append("status must remain draft")

    commentary_by_id = {
        row["comment_id"]: row for row in request.get("commentary_chunks", [])
    }
    allowed_comment_ids = set(commentary_by_id)
    candidate_ids: set[str] = set()
    for index, candidate in enumerate(payload.get("candidates", [])):
        candidate_id = candidate.get("candidate_id", "")
        label = f"candidates[{index}]"
        if not RULE_ID.fullmatch(candidate_id):
            errors.append(f"{label}.candidate_id is not valid")
        elif candidate_id in candidate_ids:
            errors.append(f"duplicate candidate_id {candidate_id}")
        candidate_ids.add(candidate_id)
        if candidate.get("norm_kind") == "variant" and not candidate.get(
            "review_required", False
        ):
            errors.append(f"variant candidate {candidate_id} must require review")
        if (
            candidate.get("norm_kind") == "exception"
            and candidate.get("polarity") != "exception"
        ):
            errors.append(
                f"exception candidate {candidate_id} must have exception polarity"
            )
        refs = candidate.get("source_refs", [])
        if not refs:
            errors.append(f"candidate {candidate_id} has no source_refs")
        _validate_source_refs(
            refs,
            f"candidate {candidate_id}",
            allowed_comment_ids,
            commentary_by_id,
            errors,
        )

    if errors:
        raise NormCandidateValidationError(errors)


def repair_ocr_interrupted_candidate_quotes(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    *,
    minimum_fragment_length: int = 8,
    minimum_coverage: float = 0.85,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Split only high-confidence non-verbatim quotes around OCR interruptions."""

    repaired = copy.deepcopy(dict(payload))
    repair_records: list[dict[str, Any]] = []
    for candidate in repaired.get("candidates", []):
        replacement_refs: list[dict[str, Any]] = []
        for ref in candidate.get("source_refs", []):
            comment_id = ref.get("comment_id", "")
            quote = ref.get("quote", "")
            commentary = commentary_by_id.get(comment_id)
            source_text = commentary.get("document_text", "") if commentary else ""
            if not quote:
                replacement_refs.append(ref)
                continue

            if quote in source_text:
                if len(quote) <= 300:
                    replacement_refs.append(ref)
                    continue
                fragments = _split_exact_quote(quote)
                replacement_refs.extend(
                    {
                        "comment_id": comment_id,
                        "section_path": ref.get("section_path", ""),
                        "quote": fragment,
                    }
                    for fragment in fragments
                )
                repair_records.append(
                    {
                        "candidate_id": candidate.get("candidate_id", ""),
                        "comment_id": comment_id,
                        "original_quote": quote,
                        "replacement_quotes": fragments,
                    }
                )
                continue

            fragments = _ocr_quote_fragments(
                quote,
                source_text,
                minimum_fragment_length=minimum_fragment_length,
                minimum_coverage=minimum_coverage,
            )
            if not fragments:
                adjacent_refs = _adjacent_chunk_quote_refs(
                    quote,
                    ref.get("section_path", ""),
                    comment_id,
                    commentary_by_id,
                    minimum_fragment_length=minimum_fragment_length,
                    minimum_coverage=minimum_coverage,
                )
                if not adjacent_refs:
                    replacement_refs.append(ref)
                    continue
                replacement_refs.extend(adjacent_refs)
                repair_records.append(
                    {
                        "candidate_id": candidate.get("candidate_id", ""),
                        "comment_id": comment_id,
                        "original_quote": quote,
                        "replacement_refs": adjacent_refs,
                    }
                )
                continue

            replacement_refs.extend(
                {
                    "comment_id": comment_id,
                    "section_path": ref.get("section_path", ""),
                    "quote": fragment,
                }
                for fragment in fragments
            )
            repair_records.append(
                {
                    "candidate_id": candidate.get("candidate_id", ""),
                    "comment_id": comment_id,
                    "original_quote": quote,
                    "replacement_quotes": fragments,
                }
            )
        candidate["source_refs"] = replacement_refs
    return repaired, repair_records


def _split_exact_quote(quote: str, *, max_length: int = 300) -> list[str]:
    return [
        quote[start : start + max_length].strip()
        for start in range(0, len(quote), max_length)
        if quote[start : start + max_length].strip()
    ]


def _adjacent_chunk_quote_refs(
    quote: str,
    section_path: str,
    comment_id: str,
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    *,
    minimum_fragment_length: int,
    minimum_coverage: float,
) -> list[dict[str, Any]]:
    rows = list(commentary_by_id.items())
    current_index = next(
        (index for index, (row_id, _) in enumerate(rows) if row_id == comment_id),
        None,
    )
    if current_index is None:
        return []

    matches: list[tuple[int, int, str, str, str]] = []
    lower = max(0, current_index - 1)
    upper = min(len(rows), current_index + 2)
    for row_index in range(lower, upper):
        row_id, row = rows[row_index]
        if row.get("section_path") != section_path:
            continue
        source_text = row.get("document_text", "")
        matcher = SequenceMatcher(None, quote, source_text, autojunk=False)
        blocks = [
            block
            for block in matcher.get_matching_blocks()
            if block.size >= minimum_fragment_length
        ]
        if not blocks:
            continue
        block = max(blocks, key=lambda item: item.size)
        matches.append(
            (
                block.a,
                row_index,
                row_id,
                row.get("section_path", ""),
                source_text[block.b : block.b + block.size].strip(),
            )
        )

    matches.sort(key=lambda item: item[0])
    if len(matches) < 2:
        return []
    row_indexes = [item[1] for item in matches]
    if row_indexes != sorted(row_indexes):
        return []
    covered = sum(len(item[4]) for item in matches)
    if covered / len(quote) < minimum_coverage:
        return []
    return [
        {
            "comment_id": row_id,
            "section_path": row_section,
            "quote": fragment,
        }
        for _, _, row_id, row_section, fragment in matches
    ]


def apply_norm_candidate_patch(
    payload: Mapping[str, Any],
    patch: Mapping[str, Any],
    request: Mapping[str, Any],
    *,
    expected_target_id: str,
) -> dict[str, Any]:
    """Apply a minimal adjudicated patch and revalidate the complete batch."""

    errors = _schema_errors(patch, "norm_candidate_patch.schema.json")
    if patch.get("target_id") != expected_target_id:
        errors.append("target_id does not match the patch request")
    existing_ids = {
        candidate.get("candidate_id", "")
        for candidate in payload.get("candidates", [])
    }
    remove_ids = set(patch.get("remove_candidate_ids", []))
    unknown_removals = sorted(remove_ids - existing_ids)
    if unknown_removals:
        errors.append(f"remove_candidate_ids contains unknown IDs: {unknown_removals}")

    retained_ids = existing_ids - remove_ids
    add_ids = [
        candidate.get("candidate_id", "")
        for candidate in patch.get("add_candidates", [])
    ]
    duplicate_adds = sorted(
        candidate_id
        for candidate_id in set(add_ids)
        if add_ids.count(candidate_id) > 1 or candidate_id in retained_ids
    )
    if duplicate_adds:
        errors.append(f"add_candidates contains duplicate IDs: {duplicate_adds}")

    existing_questions = set(payload.get("unresolved_questions", []))
    duplicate_questions = sorted(
        existing_questions & set(patch.get("append_unresolved_questions", []))
    )
    if duplicate_questions:
        errors.append(
            f"append_unresolved_questions already contains: {duplicate_questions}"
        )
    if errors:
        raise NormCandidatePatchValidationError(errors)

    result = copy.deepcopy(dict(payload))
    result["candidates"] = [
        candidate
        for candidate in result.get("candidates", [])
        if candidate.get("candidate_id") not in remove_ids
    ] + copy.deepcopy(list(patch.get("add_candidates", [])))
    result["unresolved_questions"] = list(
        result.get("unresolved_questions", [])
    ) + list(patch.get("append_unresolved_questions", []))
    try:
        validate_norm_candidate_batch(result, request)
    except NormCandidateValidationError as exc:
        raise NormCandidatePatchValidationError(exc.errors) from exc
    return result


def _ocr_quote_fragments(
    quote: str,
    source_text: str,
    *,
    minimum_fragment_length: int,
    minimum_coverage: float,
) -> list[str]:
    if not source_text or len(quote) < minimum_fragment_length * 2:
        return []
    matcher = SequenceMatcher(None, quote, source_text, autojunk=False)
    blocks = [
        block
        for block in matcher.get_matching_blocks()
        if block.size >= minimum_fragment_length
    ]
    if not blocks:
        return []
    covered = sum(block.size for block in blocks)
    if covered / len(quote) < minimum_coverage:
        return []
    fragments = [
        source_text[block.b : block.b + block.size].strip() for block in blocks
    ]
    fragments = [fragment for fragment in fragments if fragment]
    if not fragments or any(fragment not in source_text for fragment in fragments):
        return []
    return fragments


def validate_norm_card_set(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    request_comment_ids: Mapping[str, set[str]] | None = None,
    allowed_source_refs: set[tuple[str, str, str]] | None = None,
    allowed_candidates: Mapping[
        tuple[str, str], Mapping[str, Any]
    ] | None = None,
) -> None:
    """Validate normalized cards before any model is allowed to emit RuleIR."""

    errors = _schema_errors(payload, "norm_card_set.schema.json")
    if errors:
        raise NormCardValidationError(errors)
    if payload.get("status") != "draft":
        errors.append("status must remain draft")
    legal_review = payload.get("legal_review")
    construction = payload.get("construction")
    if legal_review == "complete":
        if construction != "reviewed_aggregate":
            errors.append(
                "legal_review=complete is allowed only for reviewed_aggregate"
            )
        if any(card.get("review_required", False) for card in payload.get("cards", [])):
            errors.append(
                "legal_review=complete forbids cards with review_required=true"
            )
        if payload.get("legal_review_questions"):
            errors.append(
                "legal_review=complete requires an empty legal_review_questions list"
            )
    elif legal_review != "pending":
        errors.append("legal_review must be pending or complete")
    elif construction == "reviewed_aggregate":
        errors.append("reviewed_aggregate must have legal_review=complete")

    source_scope = payload.get("source_scope", {})
    allowed_comment_ids = set(source_scope.get("comment_ids", []))
    for comment_id in sorted(allowed_comment_ids):
        if comment_id not in commentary_by_id:
            errors.append(f"source_scope contains unknown comment_id {comment_id}")

    card_ids: set[str] = set()
    covered_candidate_refs: set[tuple[str, str]] = set()
    for index, card in enumerate(payload.get("cards", [])):
        card_id = card.get("id", "")
        label = f"cards[{index}]"
        if not RULE_ID.fullmatch(card_id):
            errors.append(f"{label}.id is not valid")
        elif card_id in card_ids:
            errors.append(f"duplicate norm card id {card_id}")
        card_ids.add(card_id)

        candidate_refs = card.get("candidate_refs", [])
        linked_candidates: list[Mapping[str, Any]] = []
        for candidate_ref in candidate_refs:
            candidate_key = (
                candidate_ref.get("request_id", ""),
                candidate_ref.get("candidate_id", ""),
            )
            covered_candidate_refs.add(candidate_key)
            if allowed_candidates is None:
                continue
            candidate = allowed_candidates.get(candidate_key)
            if candidate is None:
                errors.append(
                    f"norm card {card_id} links an unknown candidate {candidate_key}"
                )
            else:
                linked_candidates.append(candidate)

        formalization = card.get("formalization")
        doctrinal_status = card.get("doctrinal_status")
        review_required = card.get("review_required", False)
        variant_group = card.get("variant_group")
        if formalization == "policy_variant" and not variant_group:
            errors.append(f"policy variant {card_id} has no variant_group")
        if formalization == "policy_variant" and not review_required:
            errors.append(f"policy variant {card_id} must require review")
        if doctrinal_status == "disputed" and not review_required:
            errors.append(f"disputed norm card {card_id} must require review")
        if card.get("norm_kind") == "standard" and formalization not in {
            "standard_input",
            "policy_variant",
            "context_only",
        }:
            errors.append(f"standard norm card {card_id} has invalid formalization")

        refs = card.get("source_refs", [])
        if not refs:
            errors.append(f"norm card {card_id} has no source_refs")
        _validate_source_refs(
            refs,
            f"norm card {card_id}",
            allowed_comment_ids,
            commentary_by_id,
            errors,
        )
        if allowed_source_refs is not None:
            for ref in refs:
                source_key = (
                    ref.get("comment_id", ""),
                    ref.get("section_path", ""),
                    ref.get("quote", ""),
                )
                if source_key not in allowed_source_refs:
                    errors.append(
                        f"norm card {card_id} source is outside validated candidates"
                    )
        if allowed_candidates is not None:
            linked_norm_kinds = {
                candidate.get("norm_kind") for candidate in linked_candidates
            }
            linked_polarities = {
                candidate.get("polarity") for candidate in linked_candidates
            }
            if len(linked_norm_kinds) > 1:
                errors.append(
                    f"norm card {card_id} merges candidates with different norm_kind"
                )
            elif linked_norm_kinds and card.get("norm_kind") not in linked_norm_kinds:
                errors.append(
                    f"norm card {card_id} changes its candidates' norm_kind"
                )
            if len(linked_polarities) > 1:
                errors.append(
                    f"norm card {card_id} merges candidates with different polarity"
                )
            elif linked_polarities and card.get("polarity") not in linked_polarities:
                errors.append(
                    f"norm card {card_id} changes its candidates' polarity"
                )
            linked_source_refs = {
                (
                    ref.get("comment_id", ""),
                    ref.get("section_path", ""),
                    ref.get("quote", ""),
                )
                for candidate in linked_candidates
                for ref in candidate.get("source_refs", [])
            }
            for ref in refs:
                source_key = (
                    ref.get("comment_id", ""),
                    ref.get("section_path", ""),
                    ref.get("quote", ""),
                )
                if source_key not in linked_source_refs:
                    errors.append(
                        f"norm card {card_id} source is outside linked candidates"
                    )

        request_ids = card.get("request_ids", [])
        if not request_ids:
            errors.append(f"norm card {card_id} has no request_ids")
        if request_comment_ids is not None:
            unknown_requests = sorted(set(request_ids) - set(request_comment_ids))
            if unknown_requests:
                errors.append(
                    f"norm card {card_id} has unknown request_ids: {unknown_requests}"
                )
            request_scope = set().union(
                *(request_comment_ids.get(request_id, set()) for request_id in request_ids)
            )
            for ref in refs:
                if ref.get("comment_id") not in request_scope:
                    errors.append(
                        f"norm card {card_id} source is outside its request_ids: "
                        f"{ref.get('comment_id', '')}"
                    )
        linked_request_ids = {
            candidate_ref.get("request_id", "")
            for candidate_ref in candidate_refs
        }
        if not linked_request_ids.issubset(set(request_ids)):
            errors.append(
                f"norm card {card_id} request_ids omit a linked candidate request"
            )

    if allowed_candidates is not None:
        missing_candidates = sorted(
            set(allowed_candidates) - covered_candidate_refs
        )
        if missing_candidates:
            errors.append(
                f"NormCardSet omits {len(missing_candidates)} validated candidates"
            )

    if errors:
        raise NormCardValidationError(errors)


def validate_rulegen_critique(
    payload: Mapping[str, Any],
    *,
    expected_stage: str,
    expected_target_id: str,
    allowed_source_refs: list[Mapping[str, Any]] | None = None,
    commentary_by_id: Mapping[str, Mapping[str, Any]] | None = None,
    allowed_comment_ids: set[str] | None = None,
) -> None:
    """Validate a Sol critique without granting it authority to rewrite artifacts."""

    errors = _schema_errors(payload, "rulegen_critique_report.schema.json")
    if errors:
        raise RulegenCritiqueValidationError(errors)
    if payload.get("status") != "draft":
        errors.append("status must remain draft")
    if payload.get("stage") != expected_stage:
        errors.append("stage does not match the critic request")
    if payload.get("target_id") != expected_target_id:
        errors.append("target_id does not match the critic request")

    findings = payload.get("findings", [])
    verdict = payload.get("verdict")
    if verdict == "pass" and findings:
        errors.append("pass verdict cannot contain findings")
    if verdict in {"revise", "reject"} and not findings:
        errors.append(f"{verdict} verdict must contain at least one finding")

    allowed_ref_keys = (
        {_critic_source_ref_key(ref) for ref in allowed_source_refs}
        if allowed_source_refs is not None
        else None
    )
    finding_ids: set[str] = set()
    hard_finding = False
    for index, finding in enumerate(findings):
        finding_id = finding.get("finding_id", "")
        label = f"findings[{index}]"
        if not RULE_ID.fullmatch(finding_id):
            errors.append(f"{label}.finding_id is not valid")
        elif finding_id in finding_ids:
            errors.append(f"duplicate finding_id {finding_id}")
        finding_ids.add(finding_id)
        hard_finding = hard_finding or finding.get("severity") == "hard"
        finding_refs = finding.get("source_refs", [])
        if commentary_by_id is not None and allowed_comment_ids is not None:
            _validate_critic_source_refs(
                finding_refs,
                f"finding {finding_id}",
                allowed_comment_ids,
                commentary_by_id,
                errors,
            )
        elif allowed_ref_keys is not None:
            for ref in finding_refs:
                if _critic_source_ref_key(ref) not in allowed_ref_keys:
                    errors.append(
                        f"finding {finding_id} cites a source outside critic scope"
                    )

    if hard_finding and verdict == "pass":
        errors.append("hard finding forbids pass verdict")
    if hard_finding and not payload.get("review_required", False):
        errors.append("hard finding requires review_required=true")

    if errors:
        raise RulegenCritiqueValidationError(errors)


def validate_rule_ir(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    norm_card_set: Mapping[str, Any],
) -> None:
    """Validate NormCard provenance, predicate closure, and Datalog safety."""

    errors = _schema_errors(payload, "rule_ir.schema.json")
    if errors:
        raise RuleIRValidationError(errors)
    if payload.get("status") != "draft":
        errors.append("status must remain draft")
    if payload.get("legal_review") != "pending":
        errors.append("legal_review must remain pending")

    source_scope = payload.get("source_scope", {})
    allowed_comment_ids = set(source_scope.get("comment_ids", []))
    for comment_id in sorted(allowed_comment_ids):
        if comment_id not in commentary_by_id:
            errors.append(f"source_scope contains unknown comment_id {comment_id}")

    try:
        validate_norm_card_set(norm_card_set, commentary_by_id)
    except NormCardValidationError as exc:
        errors.extend(f"norm_card_set: {error}" for error in exc.errors)
    norm_card_defs = {
        card.get("id", ""): card for card in norm_card_set.get("cards", [])
    }
    norm_card_scope = payload.get("norm_card_scope", {})
    if norm_card_scope.get("card_set_id") != norm_card_set.get("card_set_id"):
        errors.append("norm_card_scope.card_set_id does not match NormCardSet")
    allowed_norm_card_ids = set(norm_card_scope.get("card_ids", []))
    unknown_scope_cards = sorted(allowed_norm_card_ids - set(norm_card_defs))
    if unknown_scope_cards:
        errors.append(f"norm_card_scope contains unknown cards: {unknown_scope_cards}")
    if payload.get("issue_tag") != norm_card_set.get("issue_tag"):
        errors.append("RuleIR issue_tag does not match NormCardSet")

    predicates = payload.get("predicates", [])
    predicate_defs: dict[str, Mapping[str, Any]] = {}
    for index, predicate in enumerate(predicates):
        predicate_id = predicate.get("id", "")
        label = f"predicates[{index}]"
        if not IDENTIFIER.fullmatch(predicate_id):
            errors.append(f"{label}.id is not a valid Scallop identifier")
            continue
        if predicate_id in predicate_defs:
            errors.append(f"duplicate predicate id {predicate_id}")
            continue
        predicate_defs[predicate_id] = predicate
        if predicate.get("kind") == "standard" and predicate.get("role") == "derived":
            errors.append(f"standard predicate {predicate_id} cannot be model-derived")
        refs = predicate.get("source_refs", [])
        if predicate.get("origin") == "commentary" and not refs:
            errors.append(f"commentary predicate {predicate_id} has no source_refs")
        norm_card_ids = predicate.get("norm_card_ids", [])
        if predicate.get("origin") == "commentary" and not norm_card_ids:
            errors.append(f"commentary predicate {predicate_id} has no norm_card_ids")
        if predicate.get("origin") == "system" and (refs or norm_card_ids):
            errors.append(
                f"system predicate {predicate_id} cannot claim commentary provenance"
            )
        _validate_source_refs(
            refs,
            f"predicate {predicate_id}",
            allowed_comment_ids,
            commentary_by_id,
            errors,
        )
        _validate_norm_card_links(
            refs,
            norm_card_ids,
            f"predicate {predicate_id}",
            allowed_norm_card_ids,
            norm_card_defs,
            errors,
        )

    rule_ids: set[str] = set()
    for index, rule in enumerate(payload.get("rules", [])):
        rule_id = rule.get("id", "")
        label = f"rules[{index}]"
        if not RULE_ID.fullmatch(rule_id):
            errors.append(f"{label}.id is not valid")
        elif rule_id in rule_ids:
            errors.append(f"duplicate rule id {rule_id}")
        rule_ids.add(rule_id)

        head = rule.get("head", {})
        body = rule.get("body", [])
        _validate_atom(head, f"{label}.head", predicate_defs, errors)
        for atom_index, atom in enumerate(body):
            _validate_atom(atom, f"{label}.body[{atom_index}]", predicate_defs, errors)
        head_predicate = predicate_defs.get(head.get("predicate"))
        if head_predicate and head_predicate.get("role") != "derived":
            errors.append(f"{label}.head must use a derived predicate")

        positive_variables = {
            argument["value"]
            for atom in body
            if not atom.get("negated", False)
            for argument in atom.get("arguments", [])
            if argument.get("kind") == "variable"
        }
        head_variables = {
            argument["value"]
            for argument in head.get("arguments", [])
            if argument.get("kind") == "variable"
        }
        if not head_variables <= positive_variables:
            unsafe = sorted(head_variables - positive_variables)
            errors.append(f"{label} has unsafe head variables: {unsafe}")
        for atom_index, atom in enumerate(body):
            if not atom.get("negated", False):
                continue
            negated_variables = {
                argument["value"]
                for argument in atom.get("arguments", [])
                if argument.get("kind") == "variable"
            }
            if not negated_variables <= positive_variables:
                unsafe = sorted(negated_variables - positive_variables)
                errors.append(
                    f"{label}.body[{atom_index}] has unsafe negated variables: {unsafe}"
                )
        _validate_variable_types(label, head, body, predicate_defs, errors)
        _validate_source_refs(
            rule.get("source_refs", []),
            f"rule {rule_id}",
            allowed_comment_ids,
            commentary_by_id,
            errors,
        )
        _validate_norm_card_links(
            rule.get("source_refs", []),
            rule.get("norm_card_ids", []),
            f"rule {rule_id}",
            allowed_norm_card_ids,
            norm_card_defs,
            errors,
        )

    if errors:
        raise RuleIRValidationError(errors)


def compile_rule_ir(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    norm_card_set: Mapping[str, Any],
) -> str:
    """Compile validated RuleIR into deterministic, discrete Scallop source."""

    validate_rule_ir(payload, commentary_by_id, norm_card_set)
    lines = [
        f"// rule_set_id: {payload['rule_set_id']}",
        "// status: draft",
        "// legal_review: pending",
        "// generated_from: validated RuleIR; model output is never executed directly",
        "",
    ]
    for predicate in payload["predicates"]:
        source_ids = ", ".join(
            source["comment_id"] for source in predicate["source_refs"]
        )
        lines.append(f"// {predicate['id']}: {predicate['definition']}")
        lines.append(f"// sources: {source_ids or 'system contract'}")
        lines.append(
            "// norm_cards: "
            + (", ".join(predicate["norm_card_ids"]) or "system contract")
        )
        types = ", ".join(argument["type"] for argument in predicate["arguments"])
        lines.append(f"type {predicate['id']}({types})")
        lines.append("")

    for rule in payload["rules"]:
        source_ids = ", ".join(source["comment_id"] for source in rule["source_refs"])
        lines.append(f"// rule_id: {rule['id']}")
        lines.append(f"// sources: {source_ids}")
        lines.append(f"// norm_cards: {', '.join(rule['norm_card_ids'])}")
        lines.append(
            f"rel {_compile_atom(rule['head'])} = "
            + " and\n  ".join(_compile_atom(atom) for atom in rule["body"])
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


FULL_RULE_IR_OUTPUT_SIGNATURES = {
    "fraud_established": (
        "case_id",
        "defendant_id",
        "deceived_person_id",
        "disposer_id",
        "property_owner_id",
        "subject_id",
        "beneficiary_id",
    ),
    "fraud_not_established": ("case_id", "defendant_id", "issue_id"),
    "fraud_undetermined": ("case_id", "defendant_id", "issue_id"),
    "fraud_conflict": ("case_id", "defendant_id", "issue_id"),
}
STANDARD_ASSESSMENT_STATUSES = {"satisfied", "not_satisfied", "unknown"}


def validate_full_rule_ir_generation(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    norm_card_set: Mapping[str, Any],
) -> None:
    """Validate complete core coverage, explicit unknowns, and evidence gating."""

    validate_rule_ir(payload, commentary_by_id, norm_card_set)
    errors: list[str] = []
    card_defs = {
        card.get("id", ""): card for card in norm_card_set.get("cards", [])
    }
    expected_card_ids = set(card_defs)
    actual_scope_ids = set(payload.get("norm_card_scope", {}).get("card_ids", []))
    if actual_scope_ids != expected_card_ids:
        errors.append(
            "norm_card_scope.card_ids must exactly equal the approved aggregate card set"
        )

    expected_comment_ids = {
        ref.get("comment_id", "")
        for card in card_defs.values()
        for ref in card.get("source_refs", [])
    }
    actual_comment_ids = set(payload.get("source_scope", {}).get("comment_ids", []))
    if actual_comment_ids != expected_comment_ids:
        errors.append(
            "source_scope.comment_ids must exactly equal the approved cards' sources"
        )

    predicates = payload.get("predicates", [])
    predicate_defs = {predicate.get("id", ""): predicate for predicate in predicates}
    rules = payload.get("rules", [])
    predicate_card_ids = {
        card_id
        for predicate in predicates
        for card_id in predicate.get("norm_card_ids", [])
    }
    rule_card_ids = {
        card_id for rule in rules for card_id in rule.get("norm_card_ids", [])
    }
    referenced_card_ids = predicate_card_ids | rule_card_ids
    missing_cards = sorted(expected_card_ids - referenced_card_ids)
    if missing_cards:
        errors.append(f"RuleIR omits approved cards: {missing_cards}")

    standard_card_ids = {
        card_id
        for card_id, card in card_defs.items()
        if card.get("formalization") == "standard_input"
    }
    standard_predicate_card_ids = {
        card_id
        for predicate in predicates
        if predicate.get("kind") == "standard" and predicate.get("role") == "input"
        for card_id in predicate.get("norm_card_ids", [])
    }
    missing_standard_cards = sorted(standard_card_ids - standard_predicate_card_ids)
    if missing_standard_cards:
        errors.append(
            "standard_input cards without an input standard predicate: "
            f"{missing_standard_cards}"
        )

    deterministic_card_ids = {
        card_id
        for card_id, card in card_defs.items()
        if card.get("formalization") == "deterministic_rule"
    }
    missing_deterministic_cards = sorted(deterministic_card_ids - rule_card_ids)
    if missing_deterministic_cards:
        errors.append(
            "deterministic_rule cards without an implementing rule: "
            f"{missing_deterministic_cards}"
        )

    provable = predicate_defs.get("provable")
    expected_provable = {
        "arguments": [
            {"name": "case_id", "type": "String"},
            {"name": "assessment_id", "type": "String"},
        ],
        "kind": "rule",
        "role": "input",
        "origin": "system",
        "source_refs": [],
        "norm_card_ids": [],
    }
    if provable is None or any(
        provable.get(key) != value for key, value in expected_provable.items()
    ):
        errors.append(
            "provable must be a system input with (case_id, assessment_id)"
        )

    if "active_policy" in predicate_defs:
        errors.append("active_policy is forbidden because all fraud policies are resolved")

    commentary_inputs: set[str] = set()
    unexpected_system_predicates: list[str] = []
    for predicate in predicates:
        predicate_id = predicate.get("id", "")
        arguments = predicate.get("arguments", [])
        if predicate.get("origin") == "system" and predicate_id != "provable":
            unexpected_system_predicates.append(predicate_id)
        if predicate_id != "provable":
            if not arguments or arguments[0] != {
                "name": "case_id",
                "type": "String",
            }:
                errors.append(f"predicate {predicate_id} must start with case_id: String")
        if predicate.get("kind") == "standard" and predicate.get("role") != "input":
            errors.append(f"standard predicate {predicate_id} must be an input")
        if predicate.get("origin") != "commentary" or predicate.get("role") != "input":
            continue
        commentary_inputs.add(predicate_id)
        if len(arguments) < 3:
            errors.append(
                f"commentary input {predicate_id} needs case, assessment, and status"
            )
            continue
        if arguments[1] != {"name": "assessment_id", "type": "String"}:
            errors.append(
                f"commentary input {predicate_id} must have assessment_id second"
            )
        if arguments[-1] != {"name": "status", "type": "String"}:
            errors.append(f"commentary input {predicate_id} must end with status")
    if unexpected_system_predicates:
        errors.append(
            "provable is the only allowed system predicate: "
            f"{sorted(unexpected_system_predicates)}"
        )

    consumed_commentary_inputs: set[str] = set()
    rule_head_predicates: set[str] = set()
    for rule_index, rule in enumerate(rules):
        head = rule.get("head", {})
        head_predicate = head.get("predicate", "")
        rule_head_predicates.add(head_predicate)
        body = rule.get("body", [])
        if any(atom.get("negated", False) for atom in body):
            errors.append(f"rules[{rule_index}] uses forbidden open-world negation")
        head_arguments = head.get("arguments", [])
        expected_case = head_arguments[0] if head_arguments else None
        if not expected_case or expected_case.get("kind") != "variable":
            errors.append(f"rules[{rule_index}] head must start with a case variable")
        if head_predicate == "fraud_established":
            if (
                len(head_arguments) < 4
                or head_arguments[2].get("kind") != "variable"
                or head_arguments[2] != head_arguments[3]
            ):
                errors.append(
                    f"rules[{rule_index}] must use one variable for deceived person "
                    "and disposer"
                )
        for atom_index, atom in enumerate(body):
            arguments = atom.get("arguments", [])
            if not arguments or arguments[0] != expected_case:
                errors.append(
                    f"rules[{rule_index}].body[{atom_index}] does not use the head case"
                )
        for atom_index, atom in enumerate(body):
            predicate_id = atom.get("predicate", "")
            if predicate_id not in commentary_inputs:
                continue
            consumed_commentary_inputs.add(predicate_id)
            arguments = atom.get("arguments", [])
            status = arguments[-1] if arguments else {}
            if status.get("kind") != "string" or (
                status.get("value") not in STANDARD_ASSESSMENT_STATUSES
            ):
                errors.append(
                    f"rules[{rule_index}].body[{atom_index}] must match one explicit status"
                )
            evidence_key = arguments[:2]
            paired = any(
                candidate.get("predicate") == "provable"
                and candidate.get("arguments", []) == evidence_key
                and not candidate.get("negated", False)
                for candidate in body
            )
            if not paired:
                errors.append(
                    f"rules[{rule_index}].body[{atom_index}] bypasses provable"
                )

    unconsumed_commentary_inputs = sorted(
        commentary_inputs - consumed_commentary_inputs
    )
    if unconsumed_commentary_inputs:
        errors.append(
            "commentary inputs are declared but never consumed: "
            f"{unconsumed_commentary_inputs}"
        )

    for predicate_id, argument_names in FULL_RULE_IR_OUTPUT_SIGNATURES.items():
        predicate = predicate_defs.get(predicate_id)
        if predicate is None:
            errors.append(f"missing required output predicate {predicate_id}")
            continue
        actual_names = tuple(
            argument.get("name") for argument in predicate.get("arguments", [])
        )
        actual_types = {
            argument.get("type") for argument in predicate.get("arguments", [])
        }
        if actual_names != argument_names or actual_types != {"String"}:
            errors.append(f"output predicate {predicate_id} has the wrong signature")
        if predicate.get("role") != "derived" or predicate.get("kind") != "rule":
            errors.append(f"output predicate {predicate_id} must be a derived rule")
        if predicate_id not in rule_head_predicates:
            errors.append(f"output predicate {predicate_id} has no implementing rule")

    if errors:
        raise RuleIRGenerationContractError(errors)


def render_rule_ir_natural_language_scaffold(payload: Mapping[str, Any]) -> str:
    """Render a complete mechanical explanation for later agent legal synthesis."""

    predicate_defs = {
        predicate["id"]: predicate for predicate in payload.get("predicates", [])
    }
    lines = [
        "# 사기죄 전체 RuleIR 자연어 설명 초안",
        "",
        "> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 "
        "성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.",
        "",
        "## 전체 구조",
        "",
        f"- rule_set_id: `{payload.get('rule_set_id', '')}`",
        f"- predicate: {len(payload.get('predicates', []))}개",
        f"- rule: {len(payload.get('rules', []))}개",
        f"- NormCard: {len(payload.get('norm_card_scope', {}).get('card_ids', []))}개",
        "",
        "## Predicate",
        "",
    ]
    for predicate in payload.get("predicates", []):
        signature = ", ".join(
            f"{argument['name']}: {argument['type']}"
            for argument in predicate["arguments"]
        )
        lines.extend(
            [
                f"### `{predicate['id']}({signature})`",
                "",
                predicate["definition"],
                "",
                f"- 종류/역할: `{predicate['kind']}` / `{predicate['role']}`",
                "- 연결 NormCard: "
                + (", ".join(f"`{card_id}`" for card_id in predicate["norm_card_ids"])
                   or "system contract"),
                "",
            ]
        )
    lines.extend(["## Rules", ""])
    for rule in payload.get("rules", []):
        head = rule["head"]
        head_definition = predicate_defs[head["predicate"]]["definition"]
        body_definitions = [
            predicate_defs[atom["predicate"]]["definition"] for atom in rule["body"]
        ]
        lines.extend(
            [
                f"### `{rule['id']}`",
                "",
                f"이 규칙은 **{head_definition}**을 도출한다.",
                "",
                "필요한 전제:",
                "",
                *(f"- {definition}" for definition in body_definitions),
                "",
                "연결 NormCard: "
                + ", ".join(f"`{card_id}`" for card_id in rule["norm_card_ids"]),
                "",
                f"검토 메모: {rule['review_notes']}",
                "",
            ]
        )
    lines.extend(
        [
            "## 에이전트 추가 설명 필요",
            "",
            "- 구성요건별 satisfied/not_satisfied/unknown 전파 경로",
            "- negative·exception 카드가 불성립 경로에 들어가는 방식",
            "- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별",
            "- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식",
            "- 차용금 사기 기준과 일반 사기 기준의 관계",
            "- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식",
            "- RAG로 제외된 구체 유형을 언제 검색해야 하는지",
            "",
        ]
    )
    return "\n".join(lines)


def _validate_norm_card_links(
    refs: list[Mapping[str, Any]],
    norm_card_ids: list[str],
    label: str,
    allowed_norm_card_ids: set[str],
    norm_card_defs: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    linked_refs: set[tuple[str, str, str]] = set()
    for norm_card_id in norm_card_ids:
        if norm_card_id not in allowed_norm_card_ids:
            errors.append(f"{label} references out-of-scope norm card {norm_card_id}")
            continue
        norm_card = norm_card_defs.get(norm_card_id)
        if norm_card is None:
            errors.append(f"{label} references unknown norm card {norm_card_id}")
            continue
        linked_refs.update(_source_ref_key(ref) for ref in norm_card.get("source_refs", []))

    for ref in refs:
        if _source_ref_key(ref) not in linked_refs:
            errors.append(
                f"{label} source_ref is not backed by its norm cards: "
                f"{ref.get('comment_id', '')}"
            )


def _source_ref_key(source: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(source.get("comment_id", "")),
        str(source.get("section_path", "")),
        str(source.get("quote", "")),
    )


def _critic_source_ref_key(source: Mapping[str, Any]) -> tuple[str, str]:
    return (
        str(source.get("comment_id", "")),
        str(source.get("section_path", "")),
    )


@lru_cache(maxsize=None)
def _contract_validator(schema_name: str) -> Draft202012Validator:
    schema = json.loads((CONTRACT_ROOT / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _schema_errors(payload: Mapping[str, Any], schema_name: str) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        _contract_validator(schema_name).iter_errors(payload),
        key=lambda item: list(item.absolute_path),
    ):
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        errors.append(f"{path}: {error.message}")
    return errors


def _validate_source_refs(
    refs: list[Mapping[str, Any]],
    label: str,
    allowed_comment_ids: set[str],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    for index, source in enumerate(refs):
        comment_id = source.get("comment_id", "")
        source_label = f"{label}.source_refs[{index}]"
        if comment_id not in allowed_comment_ids:
            errors.append(f"{source_label} is outside source_scope: {comment_id}")
            continue
        commentary = commentary_by_id.get(comment_id)
        if commentary is None:
            errors.append(f"{source_label} references unknown commentary: {comment_id}")
            continue
        if source.get("section_path") != commentary.get("section_path"):
            errors.append(f"{source_label} section_path does not match commentary metadata")
        quote = source.get("quote", "")
        if not quote or quote not in commentary.get("document_text", ""):
            errors.append(f"{source_label} quote is not an exact commentary substring")


def _validate_critic_source_refs(
    refs: list[Mapping[str, Any]],
    label: str,
    allowed_comment_ids: set[str],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    for index, source in enumerate(refs):
        comment_id = source.get("comment_id", "")
        source_label = f"{label}.source_refs[{index}]"
        if comment_id not in allowed_comment_ids:
            errors.append(f"{source_label} is outside source_scope: {comment_id}")
            continue
        commentary = commentary_by_id.get(comment_id)
        if commentary is None:
            errors.append(f"{source_label} references unknown commentary: {comment_id}")
            continue
        if source.get("section_path") != commentary.get("section_path"):
            errors.append(f"{source_label} section_path does not match commentary metadata")


def _validate_atom(
    atom: Mapping[str, Any],
    label: str,
    predicate_defs: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    predicate_id = atom.get("predicate", "")
    predicate = predicate_defs.get(predicate_id)
    if predicate is None:
        errors.append(f"{label} references undeclared predicate {predicate_id}")
        return
    arguments = atom.get("arguments", [])
    expected_arguments = predicate.get("arguments", [])
    if len(arguments) != len(expected_arguments):
        errors.append(
            f"{label} arity {len(arguments)} does not match {predicate_id} "
            f"arity {len(expected_arguments)}"
        )
        return
    for index, (argument, expected) in enumerate(zip(arguments, expected_arguments, strict=True)):
        kind = argument.get("kind")
        value = argument.get("value")
        if kind == "variable" and not (
            isinstance(value, str) and IDENTIFIER.fullmatch(value)
        ):
            errors.append(f"{label}.arguments[{index}] has an invalid variable")
        elif kind == "string" and not isinstance(value, str):
            errors.append(f"{label}.arguments[{index}] must contain a string")
        elif kind == "boolean" and not isinstance(value, bool):
            errors.append(f"{label}.arguments[{index}] must contain a boolean")
        if kind == "string" and expected.get("type") != "String":
            errors.append(f"{label}.arguments[{index}] string type mismatch")
        if kind == "boolean" and expected.get("type") != "bool":
            errors.append(f"{label}.arguments[{index}] boolean type mismatch")


def _validate_variable_types(
    label: str,
    head: Mapping[str, Any],
    body: list[Mapping[str, Any]],
    predicate_defs: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    variable_types: dict[str, str] = {}
    for atom in [head, *body]:
        predicate = predicate_defs.get(atom.get("predicate"))
        if predicate is None:
            continue
        for argument, expected in zip(
            atom.get("arguments", []), predicate.get("arguments", []), strict=False
        ):
            if argument.get("kind") != "variable":
                continue
            variable = argument.get("value")
            expected_type = expected.get("type")
            prior = variable_types.setdefault(variable, expected_type)
            if prior != expected_type:
                errors.append(
                    f"{label} variable {variable} has conflicting types {prior}/{expected_type}"
                )


def _compile_atom(atom: Mapping[str, Any]) -> str:
    arguments = ", ".join(_compile_argument(argument) for argument in atom["arguments"])
    compiled = f"{atom['predicate']}({arguments})"
    return f"~{compiled}" if atom.get("negated", False) else compiled


def _compile_argument(argument: Mapping[str, Any]) -> str:
    kind = argument["kind"]
    value = argument["value"]
    if kind == "variable":
        return value
    if kind == "string":
        return json.dumps(value, ensure_ascii=False)
    if kind == "boolean":
        return "true" if value else "false"
    raise ValueError(f"Unsupported RuleIR argument kind: {kind}")
