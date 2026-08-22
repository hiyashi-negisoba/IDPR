from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import KIND_TO_EXAMPLE_FILE, DefinitionRegistry
from idpr.v2.routing import router_catalog, router_catalog_fingerprint, router_request_payload
from idpr.v2.runtime.grounding import AssessmentTarget, call2_request_payload, predicate_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey

LBOX_QUESTION_PROMPT = "제시된 사실관계에서 검토할 수 있는 범죄를 식별하시오."
KBL_CAUSATION_REF = "legal_element.result_causation"
KBL_EXTERNAL_ACTOR = "external:kbl:target"
KBL_EXTERNAL_OFFENSE = "external:kbl:result_causation"


def _text(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a non-empty string")
    return value


def _strings(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{where} must be a sequence of strings")
    values = tuple(_text(item, f"{where}[]").strip() for item in value)
    return tuple(dict.fromkeys(values))


def normalize_statute(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def _name_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[\s·ㆍ,，/()（）\-]+", "", value)
    return value[:-1] if value.endswith("죄") else value


def definitions_fingerprint(definitions_dir: Path) -> str:
    digest = hashlib.sha256()
    for filename in sorted(set(KIND_TO_EXAMPLE_FILE.values())):
        path = definitions_dir / filename
        digest.update(filename.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def direct_statute_map(registry: DefinitionRegistry) -> dict[str, tuple[str, ...]]:
    mapped: dict[str, list[str]] = {}
    for entry in registry.by_kind.get("offense", ()):
        identity = entry.payload.get("identity")
        if not isinstance(identity, Mapping):
            continue
        refs = identity.get("statutory_refs")
        if not isinstance(refs, Sequence) or isinstance(refs, str):
            continue
        for ref in refs:
            if isinstance(ref, str) and ref.strip():
                mapped.setdefault(normalize_statute(ref), []).append(entry.id)
    return {key: tuple(sorted(set(values))) for key, values in sorted(mapped.items())}


def statute_map_fingerprint(registry: DefinitionRegistry) -> str:
    encoded = json.dumps(
        direct_statute_map(registry),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _offense_name(registry: DefinitionRegistry, ref: str) -> str | None:
    entry = registry.get(ref)
    identity = entry.payload.get("identity") if entry and entry.kind == "offense" else None
    if not isinstance(identity, Mapping):
        return None
    name = identity.get("name")
    return name if isinstance(name, str) and name.strip() else None


def resolve_lbox_statute(
    registry: DefinitionRegistry,
    *,
    statute: str,
    casename: str,
    mapping: Mapping[str, Sequence[str]] | None = None,
) -> tuple[str | None, str]:
    statute_mapping = mapping or direct_statute_map(registry)
    candidates = tuple(statute_mapping.get(normalize_statute(statute), ()))
    if not candidates:
        return None, "uncovered_statute"
    if len(candidates) == 1:
        return candidates[0], "resolved"
    case_key = _name_key(casename)
    matches = []
    for ref in candidates:
        name = _offense_name(registry, ref)
        if name and _name_key(name) in case_key:
            matches.append(ref)
    if len(matches) == 1:
        return matches[0], "resolved_by_casename"
    return None, "ambiguous_statute_mapping"


def _summary(counts: Counter[str], excluded: list[dict[str, Any]], keys) -> dict[str, Any]:
    result = {key: counts.get(key, 0) for key in keys}
    result["excluded_N"] = len(excluded)
    result["excluded_reason_counts"] = dict(
        sorted(
            (key.removeprefix("excluded_"), value)
            for key, value in counts.items()
            if key.startswith("excluded_")
        )
    )
    return result


def prepare_lbox_rows(registry, rows_by_split):
    catalog = router_catalog(registry)
    mapping = direct_statute_map(registry)
    gold, inputs, excluded = [], [], []
    counts: Counter[str] = Counter()
    seen = set()
    for split in sorted(rows_by_split):
        for index, row in enumerate(rows_by_split[split]):
            counts["source_N"] += 1
            try:
                source_id = str(row.get("id", "")).strip()
                if not source_id:
                    raise ValueError("id is missing")
                case_id = f"lbox:{split}:{source_id}"
                if case_id in seen:
                    raise ValueError("duplicate split/id")
                seen.add(case_id)
                casetype = _text(row.get("casetype"), "casetype")
                casename = _text(row.get("casename"), "casename")
                facts = _text(row.get("facts"), "facts")
                statutes = _strings(row.get("statutes"), "statutes")
                if not statutes:
                    raise ValueError("statutes must not be empty")
                counts["schema_valid_N"] += 1
                if casetype != "criminal":
                    excluded.append({"id": case_id, "reason": "non_criminal_case"})
                    counts["excluded_non_criminal_case"] += 1
                    continue
                refs, mapping_rows, failure = [], [], None
                for statute in statutes:
                    ref, status = resolve_lbox_statute(
                        registry, statute=statute, casename=casename, mapping=mapping
                    )
                    mapping_rows.append(
                        {"statute": statute, "definition_ref": ref, "status": status}
                    )
                    if ref is None:
                        failure = status
                        break
                    refs.append(ref)
                if failure:
                    excluded.append(
                        {
                            "id": case_id,
                            "reason": failure,
                            "casename": casename,
                            "statutes": list(statutes),
                            "mapping": mapping_rows,
                        }
                    )
                    counts[f"excluded_{failure}"] += 1
                    continue
                counts["normalizable_N"] += 1
                refs = list(dict.fromkeys(refs))
                gold.append(
                    {
                        "id": case_id,
                        "gold_definition_refs": refs,
                        "gold_statutes": list(statutes),
                    }
                )
                inputs.append(
                    {
                        "id": case_id,
                        "source": {"dataset_id": source_id, "split": split},
                        "payload": router_request_payload(
                            question_prompt=LBOX_QUESTION_PROMPT,
                            case_text=facts,
                            catalog=catalog,
                        ),
                    }
                )
                counts["fully_covered_N"] += 1
            except ValueError as error:
                excluded.append(
                    {
                        "id": f"lbox:{split}:row-{index}",
                        "reason": "malformed_row",
                        "detail": str(error),
                    }
                )
                counts["excluded_malformed_row"] += 1
    return {
        "benchmark": "lbox_call1",
        "summary": _summary(
            counts,
            excluded,
            ("source_N", "schema_valid_N", "normalizable_N", "fully_covered_N"),
        ),
        "gold_rows": gold,
        "model_inputs": inputs,
        "excluded_rows": excluded,
        "coverage": {
            "router_catalog_fingerprint": router_catalog_fingerprint(catalog),
            "statute_map_fingerprint": statute_map_fingerprint(registry),
            "catalog_definition_ids": [entry.definition_id for entry in catalog],
        },
    }


def _kbl_truth(row: Mapping[str, Any]) -> str:
    label = _text(row.get("label"), "label").strip()
    if label not in {"A", "B"}:
        raise ValueError("label must be A or B")
    options = {key: re.sub(r"\s+", "", _text(row.get(key), key)) for key in ("A", "B")}
    if set(options.values()) != {"인과관계있음", "인과관계없음"}:
        raise ValueError("A/B must encode causation present/absent")
    return "TRUE" if options[label] == "인과관계있음" else "FALSE"


def _kbl_evidence(row: Mapping[str, Any]) -> str:
    pairs = (
        ("판단대상 원인", "cause"),
        ("판단대상 결과", "effect"),
        ("검사의 공소사실", "facts_charged"),
        ("피고인의 주장", "defendant_claim"),
        ("증거", "facts_accepted"),
    )
    values = (
        value
        for title, key in pairs
        for value in (f"[{title}]", _text(row.get(key), key))
    )
    return "\n".join(values)


def prepare_kbl_rows(registry, rows):
    available = registry.kind_of(KBL_CAUSATION_REF) == "legal_element"
    predicates = predicate_definitions(registry, (KBL_CAUSATION_REF,)) if available else ()
    gold, inputs, excluded = [], [], []
    counts: Counter[str] = Counter()
    seen = set()
    for index, row in enumerate(rows):
        counts["source_N"] += 1
        try:
            source_id = str(row.get("doc-id", "")).strip()
            if not source_id:
                raise ValueError("doc-id is missing")
            case_id = f"kbl:{source_id}"
            if case_id in seen:
                raise ValueError("duplicate doc-id")
            seen.add(case_id)
            truth = _kbl_truth(row)
            evidence = _kbl_evidence(row)
            counts["normalizable_N"] += 1
            if not available:
                excluded.append(
                    {"id": case_id, "reason": "result_causation_not_in_registry"}
                )
                counts["excluded_result_causation_not_in_registry"] += 1
                continue
            occurrence_id = f"external:kbl:occurrence:{source_id}"
            occurrence = GoldOccurrence(
                occurrence_id, KBL_EXTERNAL_ACTOR, evidence, 0, len(evidence)
            )
            target = AssessmentTarget(
                OffenseInstanceKey(
                    case_id,
                    KBL_EXTERNAL_ACTOR,
                    KBL_EXTERNAL_OFFENSE,
                    occurrence_id,
                ),
                KBL_CAUSATION_REF,
            )
            gold.append({"id": case_id, "label": truth})
            inputs.append(
                {
                    "id": case_id,
                    "source": {"dataset_id": source_id},
                    "target": target.as_dict(),
                    "payload": call2_request_payload(
                        evidence_occurrence=occurrence,
                        predicates=predicates,
                        targets=(target,),
                    ),
                }
            )
            counts["fully_covered_N"] += 1
        except ValueError as error:
            excluded.append(
                {
                    "id": f"kbl:row-{index}",
                    "reason": "malformed_row",
                    "detail": str(error),
                }
            )
            counts["excluded_malformed_row"] += 1
    return {
        "benchmark": "kbl_call2",
        "summary": _summary(
            counts, excluded, ("source_N", "normalizable_N", "fully_covered_N")
        ),
        "gold_rows": gold,
        "model_inputs": inputs,
        "excluded_rows": excluded,
        "coverage": {
            "predicate_ref": KBL_CAUSATION_REF,
            "predicate_available": available,
            "instance_namespace": {
                "actor_id": KBL_EXTERNAL_ACTOR,
                "offense_ref": KBL_EXTERNAL_OFFENSE,
                "symbolic_runtime": False,
            },
        },
    }


__all__ = [
    "KBL_CAUSATION_REF",
    "KBL_EXTERNAL_OFFENSE",
    "definitions_fingerprint",
    "prepare_kbl_rows",
    "prepare_lbox_rows",
    "resolve_lbox_statute",
]
