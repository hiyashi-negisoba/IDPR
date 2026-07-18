from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.neural import ModelCacheError, audit_local_model_snapshot  # noqa: E402


DEFAULT_SNAPSHOT = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/"
    "models--google--gemma-4-26B-A4B-it/snapshots/"
    "01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--json-out", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = audit_local_model_snapshot(args.snapshot)
    except ModelCacheError as exc:
        print(f"Gemma 4 cache preflight failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
