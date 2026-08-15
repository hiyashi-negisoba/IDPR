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
    assert_no_rubric_fields,
    missing_final_conclusions,
    missing_required_authorities,
)

PROMPTS = ("v2_call3_irac", "v2_call3_irac_user")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_SECTION = re.compile(
    r"\n?<(?P<tag>[A-Z_]+)>\s*\n(?P<body>.*?)\n?</(?P=tag)>\n?", re.DOTALL
)


def _drop_empty_sections(content: str) -> str:
    """내용이 없는 `<TAG>` 절을 통째로 뺀다.

    빈 절을 "없음" 같은 문자열로 채우면 두 가지가 섞인다 -- 정말로 없다는 판단과, 우리가
    알지 못한다는 사실이다. 둘을 구별할 수 없는 곳에서는 말하지 않는 편이 정확하다.
    """
    return _SECTION.sub(
        lambda match: "" if not match.group("body").strip() else match.group(0),
        content,
    )


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
    conclusion_missing_case_count = 0
    conclusion_missing_count = 0

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
            # 빈 절은 통째로 뺀다. "다루지 않은 영역으로 특정된 것은 없다"처럼 비어 있음을
            # 내용으로 바꿔 적으면 분석의 완결성을 host가 선언하는 것이 되고, 우리는 그것을
            # 알 수 없다 -- Call 1이 죄명을 놓친 문항에서도 그 문장이 나갔다.
            user_content = _drop_empty_sections(user_content)
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
            # 프롬프트가 요구한 최종 결론이 실제로 마지막 절에 있는지. 답안은 그대로 두고
            # 어긋남만 기록한다 -- rewrite loop를 만들면 답안이 모델의 것이 아니게 된다.
            missing_conclusions = missing_final_conclusions(
                answer, required_final_conclusions
            )
            conclusion_missing_case_count += bool(missing_conclusions)
            conclusion_missing_count += len(missing_conclusions)
            handle.write(
                json.dumps(
                    {
                        "sub_question_id": case_id,
                        "answer": answer,
                        "answer_chars": len(answer),
                        "prompt_chars": len(system_prompt) + len(user_content),
                        "missing_required_authorities": list(missing_authorities),
                        "missing_required_authority_count": len(missing_authorities),
                        "missing_required_final_conclusions": [
                            {
                                "actor": value.actor,
                                "offense_label": value.offense_label,
                                "state": value.state,
                            }
                            for value in missing_conclusions
                        ],
                        "missing_required_final_conclusion_count": len(
                            missing_conclusions
                        ),
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
        "required_final_conclusion_audit": {
            "missing_case_count": conclusion_missing_case_count,
            "missing_conclusion_count": conclusion_missing_count,
            "answer_rewritten": False,
        },
    }
    (args.out / "answers.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if errors:
        sys.exit(1)
    if conclusion_missing_count:
        # 답안은 이미 저장됐다. 여기서 종료 상태를 실패로 두는 것은 체인이 그 사실을 모른 채
        # 다음 단계로 넘어가지 않게 하기 위한 것이고, 답안을 고치는 것과는 다른 일이다.
        print(
            f"required final conclusions missing in {conclusion_missing_case_count} case(s)",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
