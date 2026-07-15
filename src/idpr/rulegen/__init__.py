"""Rule draft helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")
RULE_ID = re.compile(r"^[a-z][a-z0-9_.-]*$")


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


def validate_rule_ir(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
) -> None:
    """Validate provenance, predicate closure, arity, and Datalog variable safety."""

    errors: list[str] = []
    if payload.get("status") != "draft":
        errors.append("status must remain draft")
    if payload.get("legal_review") != "pending":
        errors.append("legal_review must remain pending")

    source_scope = payload.get("source_scope", {})
    allowed_comment_ids = set(source_scope.get("comment_ids", []))
    for comment_id in sorted(allowed_comment_ids):
        if comment_id not in commentary_by_id:
            errors.append(f"source_scope contains unknown comment_id {comment_id}")

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
        _validate_source_refs(
            refs,
            f"predicate {predicate_id}",
            allowed_comment_ids,
            commentary_by_id,
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

    if errors:
        raise RuleIRValidationError(errors)


def compile_rule_ir(
    payload: Mapping[str, Any],
    commentary_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    """Compile validated RuleIR into deterministic, discrete Scallop source."""

    validate_rule_ir(payload, commentary_by_id)
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
        types = ", ".join(argument["type"] for argument in predicate["arguments"])
        lines.append(f"type {predicate['id']}({types})")
        lines.append("")

    for rule in payload["rules"]:
        source_ids = ", ".join(source["comment_id"] for source in rule["source_refs"])
        lines.append(f"// rule_id: {rule['id']}")
        lines.append(f"// sources: {source_ids}")
        lines.append(
            f"rel {_compile_atom(rule['head'])} = "
            + " and\n  ".join(_compile_atom(atom) for atom in rule["body"])
        )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
