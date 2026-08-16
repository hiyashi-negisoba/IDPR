#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.prompts import prompt_path
from idpr.v2.benchmarks.external_data import (
    definitions_fingerprint,
    prepare_kbl_rows,
    prepare_lbox_rows,
)
from idpr.v2.registry import load_definitions

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_OUT_ROOT = ROOT / "experiments/external/materialized"
LBOX_DATASET = "lbox/lbox_open"
LBOX_CONFIG = "statute_classification_plus"
LBOX_REVISION = "10429acf7e13d7ef2ea4187ffbd685490289a82c"
KBL_DATASET = "lbox/kbl"
KBL_DATA_FILE = "reasoning/kbl_causal_reasoning_qa_v0.1.json"
KBL_REVISION = "695653ba87affa2c3113896013179c81fc16786a"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    output = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: row must be an object")
        output.append(value)
    return output


def _load_lbox_local(path: Path) -> dict[str, list[dict[str, Any]]]:
    output = {}
    for split in ("train", "valid", "test"):
        source = path / f"{split}.jsonl"
        if not source.is_file():
            raise ValueError(f"missing LBOX split: {source}")
        output[split] = _read_jsonl(source)
    return output


def _load_kbl_local(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    value = json.loads(text)
    if isinstance(value, list) and all(isinstance(row, dict) for row in value):
        return list(value)
    raise ValueError(f"{path}: expected one JSON array of objects")


def _download(url: str, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.stat().st_size:
        return path
    request = urllib.request.Request(url, headers={"User-Agent": "idpr-v2-external-eval"})
    with urllib.request.urlopen(request, timeout=1200) as response:
        path.write_bytes(response.read())
    return path


def _hf_resolve_url(dataset: str, revision: str, path: str) -> str:
    return f"https://huggingface.co/datasets/{dataset}/resolve/{revision}/{path}?download=true"


def _load_lbox_hf(revision: str, cache_dir: Path) -> dict[str, list[dict[str, Any]]]:
    output = {}
    for split in ("train", "valid", "test"):
        relative = f"{LBOX_CONFIG}/{split}.jsonl"
        source = _download(
            _hf_resolve_url(LBOX_DATASET, revision, relative),
            cache_dir / "lbox_call1" / f"{split}.jsonl",
        )
        output[split] = _read_jsonl(source)
    return output


def _load_kbl_hf(revision: str, cache_dir: Path) -> list[dict[str, Any]]:
    source = _download(
        _hf_resolve_url(KBL_DATASET, revision, KBL_DATA_FILE),
        cache_dir / "kbl_call2" / Path(KBL_DATA_FILE).name,
    )
    return _load_kbl_local(source)


def _source_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _materialize(
    out_dir: Path,
    prepared: dict[str, Any],
    *,
    source: dict[str, Any],
    definitions_dir: Path,
    prompt_names: tuple[str, ...],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    gold_path = out_dir / "gold.jsonl"
    inputs_path = out_dir / "model_inputs.jsonl"
    excluded_path = out_dir / "excluded.jsonl"
    _write_jsonl(gold_path, prepared["gold_rows"])
    _write_jsonl(inputs_path, prepared["model_inputs"])
    _write_jsonl(excluded_path, prepared["excluded_rows"])
    manifest = {
        "benchmark": prepared["benchmark"],
        "source": source,
        "definitions_dir": str(definitions_dir),
        "definitions_fingerprint": definitions_fingerprint(definitions_dir),
        "coverage": prepared["coverage"],
        "summary": prepared["summary"],
        "prompts": {name: _file_hash(prompt_path(name)) for name in prompt_names},
        "artifacts": {
            "gold": {"path": str(gold_path), "sha256": _file_hash(gold_path)},
            "model_inputs": {
                "path": str(inputs_path),
                "sha256": _file_hash(inputs_path),
            },
            "excluded": {
                "path": str(excluded_path),
                "sha256": _file_hash(excluded_path),
            },
        },
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"{prepared['benchmark']}: source={prepared['summary']['source_N']} "
        f"covered={prepared['summary']['fully_covered_N']} "
        f"excluded={prepared['summary']['excluded_N']}"
    )
    print(f"wrote {manifest_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmark",
        choices=("all", "lbox_call1", "kbl_call2"),
        default="all",
    )
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out-root", type=Path, default=DEFAULT_OUT_ROOT)
    parser.add_argument("--lbox-source-dir", type=Path)
    parser.add_argument("--kbl-source", type=Path)
    parser.add_argument("--lbox-revision", default=LBOX_REVISION)
    parser.add_argument("--kbl-revision", default=KBL_REVISION)
    args = parser.parse_args()

    registry = load_definitions(args.definitions_dir)
    if args.benchmark in {"all", "lbox_call1"}:
        if args.lbox_source_dir is not None:
            lbox_rows = _load_lbox_local(args.lbox_source_dir)
            source = {
                "dataset": LBOX_DATASET,
                "config": LBOX_CONFIG,
                "mode": "local",
                "path": str(args.lbox_source_dir),
                "content_sha256": _source_hash(lbox_rows),
            }
        else:
            lbox_rows = _load_lbox_hf(args.lbox_revision, args.out_root / "_source_cache")
            source = {
                "dataset": LBOX_DATASET,
                "config": LBOX_CONFIG,
                "mode": "huggingface",
                "revision": args.lbox_revision,
                "splits": ["train", "valid", "test"],
                "content_sha256": _source_hash(lbox_rows),
            }
        prepared = prepare_lbox_rows(registry, lbox_rows)
        _materialize(
            args.out_root / "lbox_call1",
            prepared,
            source=source,
            definitions_dir=args.definitions_dir,
            prompt_names=("v2_call1_router", "v2_call1_router_user"),
        )

    if args.benchmark in {"all", "kbl_call2"}:
        if args.kbl_source is not None:
            kbl_rows = _load_kbl_local(args.kbl_source)
            source = {
                "dataset": KBL_DATASET,
                "data_file": KBL_DATA_FILE,
                "mode": "local",
                "path": str(args.kbl_source),
                "content_sha256": _source_hash(kbl_rows),
            }
        else:
            kbl_rows = _load_kbl_hf(args.kbl_revision, args.out_root / "_source_cache")
            source = {
                "dataset": KBL_DATASET,
                "data_file": KBL_DATA_FILE,
                "mode": "huggingface",
                "revision": args.kbl_revision,
                "content_sha256": _source_hash(kbl_rows),
            }
        prepared = prepare_kbl_rows(registry, kbl_rows)
        _materialize(
            args.out_root / "kbl_call2",
            prepared,
            source=source,
            definitions_dir=args.definitions_dir,
            prompt_names=("v2_call2_grounding", "v2_call2_grounding_user"),
        )


if __name__ == "__main__":
    main()
