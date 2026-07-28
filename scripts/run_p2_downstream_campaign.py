"""Unattended P2(비재산 형법각칙) rulegen downstream: merge → normcard critic.

`run_property_campaign.py`(P1)와 동일한 오케스트레이터 패턴을 P2 31개 조문에 그대로
적용한다 — 조문 하나씩, 싼 것(chunks 적은 것)부터, idempotent, 러닝 예산 상한으로 자동
중단. P2는 candidate+critic 추출이 이미 `launch_rulegen_campaign.sh --confirm`으로
완료돼 있으므로(`.cache/llm/runs/campaign/<slug>/campaign_<slug>/terra/`) 이 스크립트는
추출을 재실행하지 않고 다운스트림(merge+normcard critic)만 수행한다.

RuleIR 생성은 P1과 동일하게 제외 — 죄명별 인간 게이트(벌크 HITL) 대상.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
MANIFEST = PROJECT_ROOT / "data/rulegen/campaign/kcl_substantive_campaign_manifest.json"
EXTRACT_ROOT = PROJECT_ROOT / ".cache/llm/runs/campaign"  # launch_rulegen_campaign.sh 산출 위치
DS_ROOT = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
LOG = PROJECT_ROOT / "logs/p2_downstream_campaign_status.log"

RATES = {"terra": (2.5, 15.0), "sol": (5.0, 30.0)}  # per 1M (in, out)


def usage_usd(run_dir: Path) -> float:
    total = 0.0
    if not run_dir.exists():
        return total
    for path in run_dir.rglob("*usage*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("cached"):
                continue
            role = d.get("role")
            if role not in RATES:
                continue
            u = d["usage"]
            ri, ro = RATES[role]
            total += u.get("prompt_tokens", 0) * ri / 1e6
            total += u.get("completion_tokens", 0) * ro / 1e6
    return total


def candidate_total(cand_dir: Path) -> int:
    if not cand_dir.exists():
        return 0
    n = 0
    for p in cand_dir.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        n += len(d.get("candidates", []))
    return n


def log(msg: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def run(cmd: list[str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as fh:
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT)
    return proc.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-usd", type=float, default=40.0, help="러닝 예산 상한")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--execute", action="store_true", help="미설정 시 계획만 출력(무지출)")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--summary", type=Path,
                        default=PROJECT_ROOT / "data/rulegen/campaign/p2_downstream_run_summary.json")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    targets = list(manifest["targets"])  # 매니페스트 = 이미 P2(비재산)만
    if not targets:
        raise SystemExit("매니페스트에 대상 조문이 없다")
    targets.sort(key=lambda t: t["chunks"])  # cheapest first

    plan_ch = sum(t["chunks"] for t in targets)
    log(f"=== P2 downstream campaign: {len(targets)} 조문 / {plan_ch} chunks "
        f"| downstream~${plan_ch*0.0377:.1f} | cap ${args.max_usd} ===")

    if not args.execute:
        for t in targets:
            log(f"  plan {t['article_no']:>8} {t['chunks']:>4}ch  {t['article_title'][:16]}")
        log("(dry-run — --execute 로 실행)")
        return

    spent = 0.0
    done: list[dict] = []
    for t in targets:
        slug = t["issue_tag"]
        article = t["article_no"]
        requests = PROJECT_ROOT / t["requests_path"]
        cand_dir = EXTRACT_ROOT / slug / f"campaign_{slug}" / "terra"

        if spent >= args.max_usd:
            log(f"!! 예산 상한 ${args.max_usd} 도달 (누적 ${spent:.2f}) — {article} 전에 중단")
            break

        n_cand = candidate_total(cand_dir)
        log(f">> {article} ({t['article_title'][:16]}) {t['chunks']}ch  후보 {n_cand}개  누적 ${spent:.2f}")
        if n_cand == 0:
            log(f"   후보 0개 — 추출이 안 됐거나 스텁 조문, downstream skip")
            done.append({"article": article, "slug": slug, "downstream_usd": 0.0, "downstream_rc": None})
            spent = sum(d["downstream_usd"] for d in done)
            continue

        ds_dir = DS_ROOT / slug / slug
        if (ds_dir / "critic_run.json").exists():
            log(f"   [downstream skip] 이미 완료 — 재사용")
            rc = 0
        else:
            rc = run(
                [PY, "scripts/run_rulegen_downstream.py",
                 "--crime-slug", slug, "--article-slug", slug, "--article", article,
                 "--law-id", "001692",
                 "--requests", str(requests),
                 "--candidates-dir", str(cand_dir),
                 "--run-id", slug, "--stage", "all",
                 "--concurrency", str(args.concurrency),
                 "--execute"],
                PROJECT_ROOT / f"logs/p2_{slug}_downstream.log",
            )
        ds_usd = usage_usd(ds_dir)
        log(f"   [downstream rc={rc}] ${ds_usd:.2f}  (rc=2는 일부 검증실패=정상 품질이슈)")
        done.append({"article": article, "slug": slug, "downstream_usd": ds_usd, "downstream_rc": rc})
        spent = sum(d["downstream_usd"] for d in done)

    total = sum(d["downstream_usd"] for d in done)
    log(f"=== 완료: {len(done)} 조문 처리 | 실지출 ${total:.2f} ===")
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest": args.manifest.name,
        "articles_done": len(done),
        "total_usd": round(total, 2),
        "per_article": done,
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"summary → {args.summary.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
