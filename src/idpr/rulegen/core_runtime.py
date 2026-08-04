"""Small Scallop runtime over RuleIR-projected core component assessments."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

from idpr.neural.core_contract import selected_track_closure
from idpr.rulegen.native_host import DEFAULT_SCLI
from idpr.rulegen.scallop_runtime import ScallopRuntimeError


class CoreRuntimeError(ValueError):
    pass


def _fact(predicate: str, values: Sequence[str]) -> str:
    return f"rel {predicate}({', '.join(json.dumps(x, ensure_ascii=False) for x in values)})"


def _nonempty(output: str, relation: str) -> bool:
    match = re.search(rf"(?ms)^\s*{re.escape(relation)}\s*:\s*\{{(.*?)\}}\s*$", output)
    if match is None:
        raise ScallopRuntimeError(f"cannot parse core relation {relation}")
    return bool(match.group(1).strip())


def render_core_program(
    *,
    profile: Mapping[str, Any],
    case_id: str,
    role_values: Mapping[str, str],
    selected_tracks: Sequence[str],
    assessments: Mapping[str, Mapping[str, Any]],
) -> tuple[str, tuple[str, ...]]:
    unit_id = str(profile["unit_id"])
    role_args = [item["name"] for item in profile["role_contract"]["arguments"]]
    expected = set(role_args)
    if set(role_values) != expected or role_values.get("case_id") != case_id:
        raise CoreRuntimeError(
            f"{unit_id}: role tuple mismatch; expected={role_args}, got={sorted(role_values)}"
        )
    active_tracks = selected_track_closure(profile, selected_tracks)
    tracks = {item["track_id"]: item for item in profile["tracks"]}
    needed = {
        predicate_id
        for track_id in active_tracks
        for path in tracks[track_id]["paths"]
        for predicate_id in path["components"]
    }
    if set(assessments) != needed:
        raise CoreRuntimeError(
            f"{unit_id}: assessment set mismatch; missing={sorted(needed-set(assessments))}, "
            f"extra={sorted(set(assessments)-needed)}"
        )
    statuses = {predicate_id: item.get("status") for predicate_id, item in assessments.items()}
    invalid = {key: value for key, value in statuses.items() if value not in {
        "satisfied", "not_satisfied", "unknown"
    }}
    if invalid:
        raise CoreRuntimeError(f"{unit_id}: invalid assessment statuses {invalid}")

    role_predicate = profile["role_contract"]["predicate"]
    role_types = ", ".join("String" for _ in role_args)
    arguments = ", ".join(role_args)
    case_var, defendant_var = role_args[:2]
    negative_relation = f"{unit_id}_not_established"
    unknown_relation = f"{unit_id}_undetermined"
    conflict_relation = f"{unit_id}_conflict"
    lines = [
        f"type {role_predicate}({role_types})",
        "type core_component_assessment(String, String, String, String)",
        "type core_case_complete(String, String)",
        f"type {negative_relation}(String, String, String)",
        f"type {unknown_relation}(String, String, String)",
        f"type {conflict_relation}(String, String, String)",
    ]
    for track_id in active_tracks:
        elements = tracks[track_id]["elements_relation"]
        established = elements.removesuffix("elements_satisfied") + "established"
        lines.extend([f"type {elements}({role_types})", f"type {established}({role_types})"])

    for predicate_id in sorted(needed):
        lines.append(
            f'rel {negative_relation}({case_var}, {defendant_var}, "{predicate_id}") = '
            f'core_component_assessment({case_var}, {defendant_var}, "{predicate_id}", "not_satisfied")'
        )
        lines.append(
            f'rel {unknown_relation}({case_var}, {defendant_var}, "{predicate_id}") = '
            f'core_component_assessment({case_var}, {defendant_var}, "{predicate_id}", "unknown")'
        )

    for track_id in active_tracks:
        track = tracks[track_id]
        for path in track["paths"]:
            atoms = [f"{role_predicate}({arguments})"]
            atoms.extend(
                f'core_component_assessment({case_var}, {defendant_var}, "{component}", "satisfied")'
                for component in path["components"]
            )
            atoms.extend(f"{dependency}({arguments})" for dependency in path["depends_on_elements"])
            lines.append(
                f"rel {track['elements_relation']}({arguments}) = " + " and\n  ".join(atoms)
            )
        established = track["elements_relation"].removesuffix("elements_satisfied") + "established"
        lines.append(
            f"rel {established}({arguments}) = {track['elements_relation']}({arguments}) and\n  "
            f"core_case_complete({case_var}, {defendant_var})"
        )

    role_fact_values = [str(role_values[name]) for name in role_args]
    lines.append(_fact(role_predicate, role_fact_values))
    for predicate_id, status in sorted(statuses.items()):
        lines.append(_fact(
            "core_component_assessment",
            [case_id, str(role_values["defendant_id"]), predicate_id, str(status)],
        ))
    lines.append(_fact("core_case_complete", [case_id, str(role_values["defendant_id"])]))
    queries = tuple(dict.fromkeys([
        *(tracks[track_id]["elements_relation"] for track_id in active_tracks),
        *(
            tracks[track_id]["elements_relation"].removesuffix("elements_satisfied")
            + "established"
            for track_id in active_tracks
        ),
        negative_relation,
        unknown_relation,
        conflict_relation,
    ]))
    return "\n\n".join(lines) + "\n", queries


def execute_core_unit(
    *,
    profile: Mapping[str, Any],
    case_id: str,
    role_values: Mapping[str, str],
    selected_tracks: Sequence[str],
    assessments: Mapping[str, Mapping[str, Any]],
    work_dir: Path,
    scli_path: Path = DEFAULT_SCLI,
) -> dict[str, Any]:
    program, queries = render_core_program(
        profile=profile,
        case_id=case_id,
        role_values=role_values,
        selected_tracks=selected_tracks,
        assessments=assessments,
    )
    work_dir.mkdir(parents=True, exist_ok=True)
    path = work_dir / f"{case_id}.{profile['unit_id']}.core.scl"
    path.write_text(program, encoding="utf-8")
    completed = subprocess.run(
        [str(scli_path), "--output-all", str(path)],
        check=False, capture_output=True, text=True, timeout=120,
    )
    if completed.returncode != 0:
        raise ScallopRuntimeError(completed.stderr.strip() or completed.stdout.strip())
    observed = {relation: _nonempty(completed.stdout, relation) for relation in queries}
    tracks = {item["track_id"]: item for item in profile["tracks"]}
    outcomes = {}
    for track_id in selected_tracks:
        track = tracks[track_id]
        established = track["elements_relation"].removesuffix("elements_satisfied") + "established"
        relevant = {
            component
            for dependency_track in selected_track_closure(profile, [track_id])
            for path in tracks[dependency_track]["paths"]
            for component in path["components"]
        }
        states = {assessments[item]["status"] for item in relevant}
        if observed[established]:
            status = "established"
        elif "not_satisfied" in states:
            status = "not_established"
        elif "unknown" in states:
            status = "undetermined"
        else:
            status = "no_derived_outcome"
        outcomes[track_id] = {
            "symbolic_conclusion": status,
            "elements_relation": track["elements_relation"],
            "established_relation": established,
        }
    return {
        "status": "executed",
        "runtime": "scallop_scli_core_projection",
        "unit_id": profile["unit_id"],
        "selected_tracks": list(selected_tracks),
        "track_outcomes": outcomes,
        "query_results": observed,
        "program_path": str(path),
    }
