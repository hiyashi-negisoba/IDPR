#!/usr/bin/env python3
"""Reconcile a Call 3 answer's final-conclusion section against its own body.

`run_v2_call3.py` writes one request, one whole answer, never rewritten -- that
invariant stays true for the *original* generation. This is a separate, explicit,
audited stage that runs strictly after it: it reads an existing `answers.jsonl`, asks a
second, narrowly-scoped completion to rewrite only the final-conclusion section so it
matches decisions (absorption, doctrine choice, resolved/unresolved state) the body
already made, and splices that section back in. Every edit is recorded -- the original
body is never sent to the model for rewriting, only the conclusion boundary moves.

This exists because body/conclusion drift (body says A absorbs B, conclusion lists both;
body picks a doctrine, conclusion contradicts it) was independently measured by an LLM
judge's `consistency` score and traced to the single long generation re-deriving the
conclusion from memory under nonzero temperature, rather than restating a decision
already made. A short, focused second pass with only the body in context is far less
prone to that drift than asking the same long generation to stay self-consistent to its
own earlier text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.neural.vllm_client import VLLMClient, VLLMClientError
from idpr.prompts import load_prompt, prompt_path
from idpr.v2.runtime.answer_plan import (
    assert_no_internal_markers,
    missing_final_conclusions,
)

PROMPTS = ("v2_call3_conclusion_align", "v2_call3_conclusion_align_user")

# 답안 후반부의 결론 절 경계. audit_v2_answer_form.py의 FINAL_BLOCK과 같은 패턴 --
# 감사와 정합화가 같은 절을 가리켜야 한다.
FINAL_BLOCK = re.compile(r"(?:\[?최종\s*(?:결론|요약|죄책)\]?|III?\.\s*죄수|결론\s*$)", re.M)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_conclusion(answer: str) -> tuple[str, str]:
    """본문과 결론 절을 가른다. 결론 절 헤딩을 못 찾으면 뒤 1/4을 결론으로 본다."""
    half = len(answer) // 2
    for match in FINAL_BLOCK.finditer(answer):
        if match.start() >= half:
            return answer[: match.start()], answer[match.start() :]
    cut = int(len(answer) * 0.75)
    return answer[:cut], answer[cut:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--answer-plans", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--case-id-file", type=Path)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()

    system_prompt = load_prompt(PROMPTS[0])
    user_template = load_prompt(PROMPTS[1])
    client = VLLMClient(base_url=args.base_url, model=args.model)

    answers = [
        json.loads(line)
        for line in args.answers.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    plans = {
        json.loads(line)["sub_question_id"]: json.loads(line)
        for line in args.answer_plans.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    if args.case_id_file:
        wanted = {
            line.strip()
            for line in args.case_id_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        answers = [row for row in answers if row["sub_question_id"] in wanted]

    args.out.mkdir(parents=True, exist_ok=True)
    out_path = args.out / "answers.jsonl"
    written = 0
    errors: list[dict[str, str]] = []
    changed_count = 0
    conclusion_missing_case_count = 0
    conclusion_missing_count = 0

    with out_path.open("w", encoding="utf-8") as handle:
        for row in answers:
            case_id = row["sub_question_id"]
            plan = plans[case_id]
            original_answer = row["answer"]
            required_final_conclusions = plan.get("required_final_conclusions", "")
            body, original_conclusion = split_conclusion(original_answer)

            user_content = (
                user_template.replace("{{BODY}}", body)
                .replace("{{ORIGINAL_CONCLUSION}}", original_conclusion)
                .replace(
                    "{{REQUIRED_FINAL_CONCLUSIONS}}", required_final_conclusions
                )
            )
            started = time.monotonic()
            try:
                new_conclusion = client.complete_text(
                    system_prompt=system_prompt,
                    user_template=user_content,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
            except VLLMClientError as error:
                errors.append({"case_id": case_id, "error": str(error)})
                continue

            aligned_answer = body.rstrip() + "\n\n" + new_conclusion.strip() + "\n"
            assert_no_internal_markers(aligned_answer)
            missing = missing_final_conclusions(
                aligned_answer, required_final_conclusions
            )
            conclusion_missing_case_count += bool(missing)
            conclusion_missing_count += len(missing)
            changed = new_conclusion.strip() != original_conclusion.strip()
            changed_count += changed

            handle.write(
                json.dumps(
                    {
                        "sub_question_id": case_id,
                        "answer": aligned_answer,
                        "original_answer": original_answer,
                        "original_conclusion": original_conclusion,
                        "aligned_conclusion": new_conclusion,
                        "changed": changed,
                        "missing_required_final_conclusion_count": len(missing),
                        "elapsed_seconds": round(time.monotonic() - started, 1),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            written += 1
            print(f"{case_id}: changed={changed}", flush=True)

    manifest = {
        "answers": str(args.answers),
        "answer_plans": str(args.answer_plans),
        "model": args.model,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "prompt_fingerprints": {name: _sha256(prompt_path(name)) for name in PROMPTS},
        "cases_requested": len(answers),
        "cases_written": written,
        "cases_changed": changed_count,
        "errors": errors,
        "required_final_conclusion_audit": {
            "missing_case_count": conclusion_missing_case_count,
            "missing_conclusion_count": conclusion_missing_count,
        },
    }
    (args.out / "answers.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)
    if conclusion_missing_count:
        print(
            f"required final conclusions missing in {conclusion_missing_case_count} case(s)",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
