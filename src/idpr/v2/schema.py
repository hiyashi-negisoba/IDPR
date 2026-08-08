"""JSON Schema loading and structural validation for the IDPR v2.1.0 Definition Layer."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_DIR = PROJECT_ROOT / "docs/contracts/v2"

KIND_TO_SCHEMA_FILE: Mapping[str, str] = {
    "ground_fact": "ground_fact_def.schema.json",
    "legal_element": "legal_element_def.schema.json",
    "primitive": "primitive_def.schema.json",
    "element_bundle": "element_bundle_def.schema.json",
    "exported_component": "exported_component_def.schema.json",
    "offense": "offense_def.schema.json",
    "derived_offense": "derived_offense_def.schema.json",
    "doctrine": "doctrine_def.schema.json",
    "qualifier": "qualifier_def.schema.json",
    "relation": "relation_def.schema.json",
    "completion_policy": "completion_policy_def.schema.json",
    "participation_policy": "participation_policy_def.schema.json",
}


@lru_cache(maxsize=None)
def load_schema_documents(schema_dir: Path = SCHEMA_DIR) -> dict[str, dict[str, Any]]:
    """Every docs/contracts/v2/*.schema.json document (including common.schema.json), keyed by
    its $id."""
    documents: dict[str, dict[str, Any]] = {}
    for path in schema_dir.glob("*.schema.json"):
        contents = json.loads(path.read_text())
        documents[contents["$id"]] = contents
    return documents


@lru_cache(maxsize=None)
def load_kind_schemas(schema_dir: Path = SCHEMA_DIR) -> dict[str, dict[str, Any]]:
    return {
        kind: json.loads((schema_dir / filename).read_text())
        for kind, filename in KIND_TO_SCHEMA_FILE.items()
    }


@lru_cache(maxsize=None)
def build_schema_registry(schema_dir: Path = SCHEMA_DIR) -> Registry:
    """A referencing.Registry so cross-file $refs (e.g. .../v2/common#/$defs/id) resolve against
    local schema documents -- no network access, absolute-URI $ids map to local resources."""
    documents = load_schema_documents(schema_dir)
    resources = [
        (schema_id, Resource.from_contents(document, default_specification=DRAFT202012))
        for schema_id, document in documents.items()
    ]
    return Registry().with_resources(resources)


def validator_for(kind: str, schema_dir: Path = SCHEMA_DIR) -> Draft202012Validator:
    schema = load_kind_schemas(schema_dir)[kind]
    registry = build_schema_registry(schema_dir)
    return Draft202012Validator(schema, registry=registry)


def schema_errors(kind: str, payload: Mapping[str, Any], schema_dir: Path = SCHEMA_DIR) -> list[str]:
    """['path.to.field: message', ...] -- same convention as src/idpr/rulegen/native_host.py's and
    src/idpr/legacy/fraud_generation.py's existing _schema_errors helpers."""
    validator = validator_for(kind, schema_dir)
    errors = sorted(validator.iter_errors(payload), key=str)
    messages = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path) or "$"
        messages.append(f"{path}: {error.message}")
    return messages
