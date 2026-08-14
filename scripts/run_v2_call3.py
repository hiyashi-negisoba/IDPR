#!/usr/bin/env python3
"""Write one integrated IRAC answer per question.

One request, one whole answer.  The host does not assemble sections, append conclusions,
or edit a sentence of what comes back -- it stores the answer as written and records what
was sent.  Any consistency checking belongs to a later offline audit, never to a rewrite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.runtime.answer_plan import (
    assert_no_internal_markers,
    assert_no_rubric_fields,
    missing_required_authorities,
)

PROMPTS = ("v2_call3_irac", "v2_call3_irac_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--case-id-file", type=Path)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    system_prompt = load_prompt(PROMPTS[0])
    user_template = load_prompt(PROMPTS[1])
    client = VLLMClient(base_url=args.base_url, model=args.model)

    plans = [
        json.loads(line)
        for line in args.answer_plans.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if args.case_id_file:
        wanted = {
            line.strip()
            for line in args.case_id_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        plans = [plan for plan in plans if plan["sub_question_id"] in wanted]

    args.out.mkdir(parents=True, exist_ok=True)
    answers_path = args.out / "answers.jsonl"
    written = 0
    errors: list[dict[str, str]] = []
    authority_missing_case_count = 0
    authority_missing_count = 0

    with answers_path.open("w", encoding="utf-8") as handle:
        for plan in plans:
            case_id = plan["sub_question_id"]
            # The locks are re-checked at the boundary rather than trusted from upstream:
            # this is the last point before the material leaves us.
            assert_no_internal_markers(plan["analysis"])
            assert_no_rubric_fields(plan)
            required_final_conclusions = plan.get("required_final_conclusions", "")
            required_authorities = plan.get("required_authorities", "")
            if required_final_conclusions:
                assert_no_internal_markers(required_final_conclusions)
            if required_authorities:
                assert_no_internal_markers(required_authorities)
            user_content = (
                user_template.replace("{{CASE_TEXT}}", plan["case_text"])
                .replace("{{QUESTION}}", plan["question"])
                .replace("{{ANALYSIS}}", plan["analysis"])
                .replace("{{OPEN_POINTS}}", plan["open_points"])
                .replace("{{REQUIRED_AUTHORITIES}}", required_authorities)
                .replace("{{REQUIRED_FINAL_CONCLUSIONS}}", required_final_conclusions)
            )
            started = time.monotonic()
            try:
                answer = client.complete_text(
                    system_prompt=system_prompt,
                    user_template=user_content,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
            except VLLMClientError as error:
                errors.append({"case_id": case_id, "error": str(error)})
                continue
            missing_authorities = missing_required_authorities(
                answer, required_authorities
            )
            authority_missing_case_count += bool(missing_authorities)
            authority_missing_count += len(missing_authorities)
            handle.write(
                json.dumps(
                    {
                        "sub_question_id": case_id,
                        "answer": answer,
                        "answer_chars": len(answer),
                        "prompt_chars": len(system_prompt) + len(user_content),
                        "missing_required_authorities": list(missing_authorities),
                        "missing_required_authority_count": len(missing_authorities),
                        "elapsed_seconds": round(time.monotonic() - started, 1),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            written += 1
            print(f"{case_id}: {len(answer)} chars", flush=True)

    manifest = {
        "answer_plans": str(args.answer_plans),
        "model": args.model,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "prompt_fingerprints": {
            name: _sha256(prompt_path(name)) for name in PROMPTS
        },
        "cases_requested": len(plans),
        "cases_written": written,
        "errors": errors,
        "host_post_edit": False,
        "required_authority_audit": {
            "missing_case_count": authority_missing_case_count,
            "missing_authority_count": authority_missing_count,
            "answer_rewritten": False,
        },
    }
    (args.out / "answers.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
