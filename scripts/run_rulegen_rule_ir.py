"""죄명-불문 RuleIR 생성 + sol 비평 — 단위별 1콜 (preflight 승인 게이트).

사기 러너(`run_fraud_full_rule_ir_generation.py`)는 제347조 경로·역할·출력 술어를 하드코딩하고
있어 재산죄 11단위에 쓸 수 없다. 이 드라이버는 그 구조를 단위-파라미터화한 것으로, 계약·프롬프트·
검증기는 그대로 재사용한다.

단위별 생성 요청은 preflight에서 승인받은 것으로 조립한다.
  · 카드      `data/rulegen/property/rule_ir_units/<unit>.json` (검토완료 core)
  · 역할·가중  preflight의 ACTOR_ROLES / AGGRAVATION
  · 스트라텀   `rule_ir_phase_map.json`의 레벨 배정 (L0~L7)
  · 계약      증거 게이트·부정 제한·브리지 술어(`rulegen_rule_ir_phases.md` §1)

게이트가 셋이다. ① preflight 10항목이 전부 `approve`여야 한다. ② 카드셋이 NormCardSet 계약을
통과해야 한다. ③ 이미 만들어진 후보를 덮어쓰지 않는다(단위별 skip → 재제출 안전).

친족상도례(`relative_property_crime_exception`)는 생성하지 않는다 — 처벌·소추 층이라 A4 절차
레이어에서 쓰기로 한 사용자 결정이다. 브리지 술어를 배출하는 쪽(죄명 단위)만 만든다.

기본은 dry-run이고 실제 지출은 `--execute`에서만 일어난다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.llm import (  # noqa: E402
    GatewayConfig,
    JSONCompletionJob,
    LLMGateway,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    NormCardValidationError,
    RuleIRGenerationContractError,
    RuleIRGenerationProfile,
    RuleIRValidationError,
    render_rule_ir_natural_language_scaffold,
    validate_full_rule_ir_generation,
    validate_norm_card_set,
)

from scripts.build_property_core_norm_card_sets import commentary_index  # noqa: E402
from scripts.build_property_rule_ir_preflight import (  # noqa: E402
    ACTOR_ROLES,
    AGGRAVATION,
    SHARED_MODULES,
)

PROP = ROOT / "data/rulegen/property"
UNITS = PROP / "rule_ir_units"
UNIT_MANIFEST = PROP / "rule_ir_unit_manifest.json"
PHASE_MAP = PROP / "rule_ir_phase_map.json"
PREFLIGHT = PROP / "rule_ir_prep_review_queue.json"
OUT_DIR = PROP / "rule_ir"
PROMPT = ROOT / "prompts/rulegen_merge_rule_ir.md"
RULE_IR_SCHEMA = ROOT / "docs/contracts/rule_ir.schema.json"
FEWSHOT = ROOT / "data/rulegen/fraud/fraud_rule_ir_generation_fewshot.json"
CRITIC_PROMPT = ROOT / "prompts/rulegen_critic.md"
RUN_ROOT = ROOT / ".cache/llm/runs/property_rule_ir"
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9_.-]+$")
TERRA_MAX_TOKENS = 64_000
SOL_MAX_TOKENS = 32_000
RATES = {"terra": (2.5, 15.0), "sol": (5.0, 30.0)}  # per 1M (in, out)
# 친족상도례는 A4 절차 레이어에서 쓴다 — 이번 생성 대상이 아니다.
DEFERRED_UNITS = ("relative_property_crime_exception",)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def preflight_gate() -> list[str]:
    queue = read_json(PREFLIGHT)
    errors: list[str] = []
    if len(queue["items"]) != 10:
        errors.append(f"preflight 항목이 10개가 아니다: {len(queue['items'])}")
    pending = [entry["review_id"] for entry in queue["items"]
               if entry["human_review"].get("decision") != "approve"
               or entry["human_review"].get("status") != "completed"]
    if pending:
        errors.append(f"승인되지 않은 preflight 항목: {pending}")
    return errors


def spent_usd(run_dir: Path) -> float:
    """지금까지의 실지출 — usage 매니페스트에서 캐시 제외 합산(preflight 10항목의 상한 집행)."""

    total = 0.0
    for path in run_dir.rglob("*usage*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("cached") or row.get("role") not in RATES:
                continue
            rate_in, rate_out = RATES[row["role"]]
            usage = row["usage"]
            total += usage.get("prompt_tokens", 0) * rate_in / 1e6
            total += usage.get("completion_tokens", 0) * rate_out / 1e6
    return total


def levels_for(unit: str, phase_rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    """단위의 카드를 레벨별로 묶는다 — 스트라텀 순서를 요청에 실어 준다."""

    grouped: dict[str, list[str]] = {}
    for row in phase_rows:
        if row["unit"] == unit:
            grouped.setdefault(row["level"], []).append(row["card_id"])
    return {level: sorted(cards) for level, cards in sorted(grouped.items())}


def build_request(unit: str, card_set: dict[str, Any],
                  phase_rows: list[dict[str, Any]]) -> dict[str, Any]:
    roles = ACTOR_ROLES[unit]
    shared = unit in SHARED_MODULES
    aggravation = [{"kind": kind, "article": article, "precondition": condition}
                   for kind, article, condition in AGGRAVATION.get(unit, [])]
    # 계약이 요구하는 출력 술어는 정확히 이 네 개다(`RuleIRGenerationProfile.for_crime`).
    # elements_met·aggravation은 그 위에 얹는 보조 술어라 required가 아니다.
    issue_shape = ["case_id", "defendant_id", "issue_id"]
    outputs = [
        {"id": f"{unit}_established", "arguments": ["case_id", *roles],
         "role": "derived",
         "meaning": "요건 충족 + 종결 게이트 통과 + 소극·충돌 요약이 모두 부정된 최종 결론."},
        {"id": f"{unit}_not_established", "arguments": issue_shape, "role": "derived",
         "meaning": "요건이 확정적으로 결여됐다."},
        {"id": f"{unit}_undetermined", "arguments": issue_shape, "role": "derived",
         "meaning": "판단에 필요한 사실이 미확정이다 — 불성립과 구별한다."},
        {"id": f"{unit}_conflict", "arguments": issue_shape, "role": "derived",
         "meaning": "규칙이 서로 다른 결론을 낸다."},
    ]
    helper_outputs = [
        {"id": f"{unit}_elements_met", "arguments": ["case_id", *roles],
         "meaning": "L0~L4 요건 충족(부정을 쓰지 않는 스트라텀)."},
        {"id": f"{unit}_has_negative", "arguments": ["case_id", "defendant_id"],
         "meaning": ("불성립 근거의 닫힌 요약. **L6 위법성·책임 카드는 여기로 들어온다** — "
                     "위법성 조각을 따로 부정하면 최종 스트라텀 밖에서 부정을 쓰게 되어 계약 위반이다.")},
        {"id": f"{unit}_has_conflict", "arguments": ["case_id", "defendant_id"],
         "meaning": "충돌 근거의 닫힌 요약."},
    ]
    if aggravation:
        helper_outputs.append({
            "id": f"{unit}_aggravation", "arguments": ["case_id", "defendant_id", "kind"],
            "meaning": "가중유형 플래그. 열거된 kind만 생성한다. 꺼지면 기본범으로 남는다.",
            "allowed_kinds": [entry["kind"] for entry in aggravation],
        })

    contract: dict[str, Any] = {
        "generation_unit": "single_complete_rule_ir",
        "case_isolation": "Every non-system predicate starts with case_id: String.",
        "active_policy_allowed": False,
        "negation_allowed": "final_outcome_stratum_only_after_closed_case_gate",
        "system_input_predicates": [
            {"id": "provable", "arguments": ["case_id", "assessment_id"],
             "origin": "system", "role": "input", "kind": "rule",
             "note": "commentary에서 온 모든 입력은 이 게이트를 통과해야 한다."},
            {"id": "case_assessment_complete", "arguments": ["case_id", "defendant_id"],
             "origin": "system", "role": "input", "kind": "rule",
             "note": "이 게이트 뒤 최종 결론 규칙에서만 부정을 쓴다."},
            {"id": "distinct_entity",
             "arguments": ["case_id", "left_entity_id", "right_entity_id"],
             "origin": "system", "role": "input", "kind": "rule"},
            {"id": f"{unit}_case_roles", "arguments": ["case_id", *roles],
             "origin": "system", "role": "input", "kind": "rule",
             "note": "행위자 역할 배정. 슬롯이 달라도 같은 사람일 수 있다."},
        ],
        "system_inputs_are_exhaustive": True,
        "standard_assessment": {
            "input_prefix": ["case_id", "assessment_id"],
            "input_suffix": ["status"],
            "statuses": ["satisfied", "not_satisfied", "unknown"],
            "missing_is_false": False,
            "note": ("standard_input 카드마다 "
                     "`(case_id, assessment_id, ..., status)` 형태의 입력 술어를 하나 만든다. "
                     "규칙 본문에서 status는 명시적 문자열 하나로 고정한다."),
        },
        "actor_roles": list(roles),
        "role_identity": {
            "same_entity_id_may_fill_multiple_roles": True,
            "separate_slots_imply_distinct_people": False,
            "note": ("강도·공갈은 폭행·협박의 상대방이 소유자·점유자와 다를 수 있다. 서로 다른 "
                     "사람이어야 하는 곳에서만 distinct_entity를 쓴다."),
        },
        "required_output_predicates": outputs,
        "helper_predicates": helper_outputs,
        "final_outcome_rule": {
            "id": f"{unit}.core.outcome.established",
            "head": f"{unit}_established",
            "must_negate_exactly": [f"{unit}_has_negative", f"{unit}_has_conflict"],
            "must_include_positive": "case_assessment_complete",
            "note": ("부정을 쓰는 규칙은 이것 하나뿐이다. 다른 규칙에서 부정을 쓰면 계약 위반이다."),
        },
        "stratum_order": {
            "levels": ["L0 적격·객체", "L1 실행행위", "L2 인과·귀속", "L3 주관",
                       "L4 단계(착수·기수)", "L5 가중", "L6 위법성·책임"],
            "cards_by_level": levels_for(unit, phase_rows),
            "composition": [
                f"{unit}_elements_met :- L0 ∧ L1 ∧ L2 ∧ L3 ∧ stage=completed (부정 없음)",
                f"{unit}_has_negative :- L6 위법성·책임 카드 및 불성립 근거 (부정 없음)",
                f"{unit}_established :- {unit}_elements_met, case_assessment_complete, "
                f"not {unit}_has_negative, not {unit}_has_conflict",
                (f"{unit}_aggravation(kind) :- {unit}_established, L5 요건" if aggravation
                 else "이 단위에는 가중유형이 없다 — aggravation 술어를 만들지 않는다"),
            ],
            "empty_levels_instruction": ("카드가 없는 레벨의 술어는 만들지 않는다. 규칙 없는 술어를 "
                                         "두면 미확정이 아니라 불성립으로 잘못 흐른다."),
        },
        "bridge_predicate": {
            "id": "property_crime_established",
            "arguments": ["case_id", "crime_id", "defendant_id", "owner_id", "possessor_id"],
            "purpose": ("공유 수정요소(친족상도례·업무자 신분)가 받는 이음새. 받는 쪽 규칙은 이번 "
                        "생성 범위가 아니다."),
            "emit": not shared,
            "note": "시스템 입력이 아니라 파생 술어로 만든다.",
        },
        "aggravation_flags": aggravation,
        "hard_requirements": [
            "norm_card_scope.card_ids는 승인 카드 집합과 정확히 같아야 한다.",
            "source_scope.comment_ids는 승인 카드의 출처 집합과 정확히 같아야 한다.",
            "모든 승인 카드가 최소 하나의 술어 또는 규칙에 인용돼야 한다.",
            "deterministic_rule 카드는 각각 그것을 구현하는 규칙이 있어야 한다.",
            "standard_input 카드는 각각 대응하는 입력 standard 술어가 있어야 한다.",
            "술어·규칙의 source_refs는 그 술어·규칙이 인용한 카드의 출처 안에서만 고른다.",
            "규칙 머리의 모든 변수는 본문에서 결박돼야 한다(unsafe head variable 금지).",
            "규칙 본문의 모든 원자는 머리와 같은 case 변수로 시작해야 한다.",
            f"식별자에 'fraud'를 쓰지 않는다 — 이 단위는 {unit}이고, 구조 예시의 이름을 옮기면 "
            "계약 위반이다.",
        ],
    }

    return {
        "version": "1.0.0",
        "stage": "rule_ir",
        "request_id": f"property.{unit}.rule_ir.full.v1",
        "target": {"issue_tag": unit,
                   "rule_set_id": f"kr.property.{unit}.full.v1_candidate",
                   "status": "draft", "legal_review": "pending"},
        "architecture_contract": contract,
        "coverage_contract": {
            "cards": len(card_set["cards"]),
            "card_ids": sorted(card["id"] for card in card_set["cards"]),
            "instruction": ("승인된 카드 전부가 최소 하나의 술어 또는 규칙에 인용돼야 한다. "
                            "카드에 없는 요건을 새로 만들지 않는다."),
        },
        "bounded_source_material": {"approved_norm_card_set": card_set},
        "excluded_context": {
            "instruction": ("구체 사안·죄수·공범총칙·타법률·판단지침형·증명소송법으로 강등된 카드를 "
                            "규칙으로 되살리지 않는다."),
            "audit_path": "data/rulegen/property/core_norm_card_set_ledger.json",
        },
        "review_workflow": [
            "local_schema_provenance_and_generation_contract_validation",
            "agent_rule_ir_review",
            "agent_long_form_natural_language_explanation",
            "human_review",
            "sol_critic",
            "human_re_review",
            "scallop_compile_and_runtime_tests",
        ],
    }


def system_prompt() -> str:
    prompt = PROMPT.read_text(encoding="utf-8").rstrip()
    schema = RULE_IR_SCHEMA.read_text(encoding="utf-8").rstrip()
    fewshot = FEWSHOT.read_text(encoding="utf-8").rstrip()
    return (
        f"{prompt}\n\nExact output JSON Schema:\n```json\n{schema}\n```\n\n"
        "Partial structural example only:\n"
        "This two-card fraud example teaches status, evidence-gate, provenance, and actor "
        "signature structure. It is not a statement of the current crime's doctrine. Do not copy "
        "its IDs, card count, source scope, or conclusions. The approved aggregate in the current "
        "request is the only substantive generation scope.\n"
        f"```json\n{fewshot}\n```\n"
    )


def critic_system_prompt() -> str:
    prompt = CRITIC_PROMPT.read_text(encoding="utf-8").rstrip()
    schema = RULE_IR_SCHEMA.read_text(encoding="utf-8").rstrip()
    return f"{prompt}\n\nRuleIR JSON Schema under review:\n```json\n{schema}\n```\n"


def unit_targets(args: argparse.Namespace) -> list[str]:
    manifest = read_json(UNIT_MANIFEST)
    tags = [unit["issue_tag"] for unit in manifest["units"]
            if unit["issue_tag"] not in DEFERRED_UNITS]
    if args.units:
        wanted = [tag.strip() for tag in args.units.split(",") if tag.strip()]
        unknown = sorted(set(wanted) - set(tags))
        if unknown:
            raise SystemExit(f"알 수 없는 단위(또는 이월 단위): {unknown}")
        return wanted
    return tags


async def generate(unit: str, request: dict[str, Any], card_set: dict[str, Any],
                   commentary: dict[str, Any], gateway: LLMGateway,
                   run_dir: Path) -> dict[str, Any]:
    job = JSONCompletionJob(
        request_id=request["request_id"], role="terra",
        system_prompt=system_prompt(), payload=request,
        max_tokens=TERRA_MAX_TOKENS, reasoning_effort="low",
    )
    result = await gateway.complete_json(job)
    write_usage_manifest(run_dir / "terra_usage.jsonl", [result])
    write_json(run_dir / "terra" / f"{unit}.json", result.output)

    errors: list[str] = []
    try:
        validate_full_rule_ir_generation(
            result.output, commentary, card_set,
            RuleIRGenerationProfile.for_crime(unit, ACTOR_ROLES[unit]))
    except (RuleIRValidationError, RuleIRGenerationContractError) as exc:
        errors = list(exc.errors)
        gateway.discard_cache(result)

    if not errors:
        write_json(OUT_DIR / f"{unit}_rule_ir_candidate.json", result.output)
        (OUT_DIR / f"{unit}_scaffold.md").write_text(
            render_rule_ir_natural_language_scaffold(result.output), encoding="utf-8")
    return {"unit": unit, "valid": not errors, "validation_errors": errors,
            "api_calls": int(not result.cached), "cached": result.cached,
            "usage": result.usage,
            "rules": len(result.output.get("rules", [])),
            "predicates": len(result.output.get("predicates", []))}


async def critique(unit: str, candidate: dict[str, Any], card_set: dict[str, Any],
                   gateway: LLMGateway, run_dir: Path) -> dict[str, Any]:
    payload = {"stage": "rule_ir_critique", "issue_tag": unit,
               "rule_ir": candidate,
               "approved_norm_card_set": card_set,
               "instruction": ("규칙별로 카드 근거·스트라텀 배치·부정 사용·가중 플래그 전제조건을 "
                               "점검한다. 카드에 없는 요건이 들어왔는지, 빈 레벨의 술어를 만들었는지 "
                               "확인한다.")}
    job = JSONCompletionJob(
        request_id=f"property.{unit}.rule_ir.sol_critic.v1", role="sol",
        system_prompt=critic_system_prompt(), payload=payload,
        max_tokens=SOL_MAX_TOKENS, reasoning_effort="low",
    )
    result = await gateway.complete_json(job)
    write_usage_manifest(run_dir / "sol_usage.jsonl", [result])
    write_json(run_dir / "sol" / f"{unit}.json", result.output)
    return {"unit": unit, "api_calls": int(not result.cached), "cached": result.cached,
            "usage": result.usage, "verdict": result.output.get("verdict"),
            "findings": len(result.output.get("findings", []))}


async def run(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    phase_rows = read_json(PHASE_MAP)["rows"]
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    generated: list[dict[str, Any]] = []
    critiqued: list[dict[str, Any]] = []

    for unit in unit_targets(args):
        spent = spent_usd(run_dir)
        if spent >= args.max_usd:
            print(f"!! 예산 상한 ${args.max_usd} 도달(누적 ${spent:.2f}) — {unit} 전에 중단")
            break
        card_set = read_json(UNITS / f"{unit}.json")
        commentary: dict[str, Any] = {}
        for article in next(entry["articles"] for entry in read_json(UNIT_MANIFEST)["units"]
                            if entry["issue_tag"] == unit):
            chunks, _ = commentary_index(article)
            commentary.update(chunks)

        try:
            validate_norm_card_set(card_set, commentary)
        except NormCardValidationError as exc:
            raise SystemExit(f"{unit} 카드셋이 계약을 통과하지 못한다: {exc}") from exc

        candidate_path = OUT_DIR / f"{unit}_rule_ir_candidate.json"
        if candidate_path.exists():
            print(f"  [{unit}] 후보 이미 존재 — skip")
            generated.append({"unit": unit, "valid": True, "skipped": True})
        else:
            summary = await generate(unit, build_request(unit, card_set, phase_rows),
                                     card_set, commentary, gateway, run_dir)
            state = "valid" if summary["valid"] else f"invalid({len(summary['validation_errors'])})"
            print(f"  [{unit}] 생성 {state} / 규칙 {summary.get('rules')} "
                  f"/ 술어 {summary.get('predicates')}")
            for line in summary["validation_errors"][:5]:
                print(f"       - {line}")
            generated.append(summary)

        if args.stage in ("critic", "all") and candidate_path.exists():
            critic_path = run_dir / "sol" / f"{unit}.json"
            if critic_path.exists():
                print(f"  [{unit}] 비평 이미 존재 — skip")
            else:
                verdict = await critique(unit, read_json(candidate_path), card_set,
                                         gateway, run_dir)
                print(f"  [{unit}] 비평 {verdict['verdict']} / 지적 {verdict['findings']}")
                critiqued.append(verdict)

    summary = {
        "version": "1.0.0", "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "units": len(generated),
        "valid": sum(1 for entry in generated if entry["valid"]),
        "api_calls": sum(entry.get("api_calls", 0) for entry in generated)
        + sum(entry.get("api_calls", 0) for entry in critiqued),
        "spent_usd": round(spent_usd(run_dir), 2),
        "max_usd": args.max_usd,
        "generation": generated, "critique": critiqued,
        "deferred_units": list(DEFERRED_UNITS),
        "next_gate": "agent_rule_by_rule_review_then_human_review",
    }
    write_json(run_dir / "run.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="미설정 시 계획만 출력(무지출)")
    parser.add_argument("--units", default="", help="쉼표목록(기본: 이월 제외 전 단위)")
    parser.add_argument("--stage", choices=["generate", "critic", "all"], default="all")
    parser.add_argument("--max-usd", type=float, default=6.0,
                        help="러닝 예산 상한(초과 시 다음 단위 전 중단) — preflight 10항목")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    args = parser.parse_args()
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id에 안전하지 않은 문자가 있다")

    gate_errors = preflight_gate()
    if gate_errors:
        raise SystemExit("preflight 게이트 통과 실패:\n- " + "\n- ".join(gate_errors))

    targets = unit_targets(args)
    manifest = read_json(UNIT_MANIFEST)
    cards = {unit["issue_tag"]: unit["cards"] for unit in manifest["units"]}
    total = sum(cards[tag] for tag in targets)
    print(f"=== RuleIR 생성: 단위 {len(targets)} / 카드 {total} / stage={args.stage} ===")
    for tag in targets:
        print(f"  plan {tag:36s} {cards[tag]:4d}장")
    print(f"  이월(생성 안 함): {', '.join(DEFERRED_UNITS)}")
    print(f"  추정 $4.52 (terra $1.35 + sol $3.17, 사기 실측 2.96자/토큰 기준) / "
          f"상한 ${args.max_usd}")

    if not args.execute:
        print("(dry-run — --execute 로 실행)")
        return

    load_dotenv(args.env_file, override=False)
    config = GatewayConfig.from_env(require_api_key=True, require_models=False)
    config.model_for_role("terra")
    config = replace(config, max_concurrency=1, max_retries=0,
                     timeout_seconds=max(config.timeout_seconds, 900.0))
    summary = asyncio.run(run(args, config))
    print(f"\n=== 완료: 단위 {summary['units']} / 계약통과 {summary['valid']} "
          f"/ API {summary['api_calls']}콜 / 실지출 ${summary['spent_usd']} ===")
    if summary["valid"] != summary["units"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
