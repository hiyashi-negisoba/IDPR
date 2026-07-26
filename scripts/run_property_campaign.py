"""Unattended P1 property-crime rulegen bulk: candidate → merge → normcard critic.

Runs the substantive rulegen pipeline for the property-crime (재산범) subset of
the KCL campaign manifest, one 조문 at a time, cheapest (fewest chunks) first so
a broken pipeline fails cheap. RuleIR generation is intentionally excluded — it
is gated behind a per-crime human NormCard review (bulk HITL) and cannot run for
a fresh crime.

Safety for unattended runs:
- Articles processed smallest-first.
- Per-article failures are tolerated (logged, campaign continues).
- A running USD cap (--max-usd) aborts the campaign before the next article if
  measured spend exceeds it.
- Every stage reuses approved prompts; terra(reasoning) gets reasoning_effort=low.
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
EXTRACT_ROOT = PROJECT_ROOT / ".cache/llm/runs/campaign_prop"
DS_ROOT = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
LOG = PROJECT_ROOT / "logs/property_campaign_status.log"

RATES = {"terra": (2.5, 15.0), "sol": (5.0, 30.0)}  # per 1M (in, out)

# 형법 재산범죄 조문 (절도·강도·공갈·횡령·배임·손괴·권리행사방해·친족상도례).
# 사기(347)·장물(362)은 이미 완료라 매니페스트에서 제외돼 있음.
PROPERTY_ARTICLES = {
    323, 328, 329, 331, 334, 335, 337, 338,
    342, 343, 344, 350, 355, 356, 357, 360, 366,
}


def art_num(article_no: str) -> int:
    digits = re.sub(r"[^0-9]", "", article_no or "")
    return int(digits) if digits else 0


def usage_usd(run_dir: Path) -> float:
    """Sum non-cached spend across every *_usage.jsonl under run_dir."""
    total = 0.0
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


def candidate_count(cand_dir: Path) -> int:
    """Number of candidate batch files present (for extraction idempotency)."""
    if not cand_dir.exists():
        return 0
    return sum(1 for _ in cand_dir.glob("*.json"))


def candidate_total(cand_dir: Path) -> int:
    """Total candidates across batch files; 0 means nothing extractable (stub 조문)."""
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
    parser.add_argument("--max-usd", type=float, default=55.0, help="러닝 예산 상한(초과 시 다음 조문 전 중단)")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--execute", action="store_true", help="미설정 시 계획만 출력(무지출)")
    parser.add_argument("--manifest", type=Path, default=MANIFEST,
                        help="캠페인 매니페스트(기본: KCL 실체 캠페인). 보강 조문은 "
                             "kcl_supplement_manifest.json")
    parser.add_argument("--articles", default="",
                        help="처리할 조문 번호 콤마목록(기본: 재산범 전체). 예: 330,332,333")
    parser.add_argument("--summary", type=Path,
                        default=PROJECT_ROOT / "data/rulegen/campaign/property_campaign_run_summary.json",
                        help="실행 요약 산출 경로(매니페스트별로 덮어쓰지 않게 분리)")
    args = parser.parse_args()

    wanted = ({int(x) for x in args.articles.replace(" ", "").split(",") if x}
              or PROPERTY_ARTICLES)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    targets = [t for t in manifest["targets"] if art_num(t["article_no"]) in wanted]
    if not targets:
        raise SystemExit(f"{args.manifest.name}에 대상 조문이 없다: {sorted(wanted)}")
    targets.sort(key=lambda t: t["chunks"])  # cheapest first

    plan_ch = sum(t["chunks"] for t in targets)
    plan_ext = sum(t["est_extraction_critic_usd"] for t in targets)
    log(f"=== property campaign: {len(targets)} 조문 / {plan_ch} chunks "
        f"| extract+critic~${plan_ext:.1f} + downstream~${plan_ch*0.0377:.1f} "
        f"= ~${plan_ext + plan_ch*0.0377:.1f} | cap ${args.max_usd} ===")

    if not args.execute:
        for t in targets:
            log(f"  plan {t['article_no']:>8} {t['chunks']:>4}ch {t['batches']:>2}b  {t['article_title'][:16]}")
        log("(dry-run — --execute 로 실행)")
        return

    spent = 0.0
    done: list[dict] = []
    for t in targets:
        slug = t["issue_tag"]  # e.g. "art329"
        article = t["article_no"]
        requests = PROJECT_ROOT / t["requests_path"]
        batches = t["batches"]
        ext_dir = EXTRACT_ROOT / slug
        cand_dir = ext_dir / "terra"

        if spent >= args.max_usd:
            log(f"!! 예산 상한 ${args.max_usd} 도달 (누적 ${spent:.2f}) — {article} 전에 중단")
            break

        log(f">> {article} ({t['article_title'][:16]}) {t['chunks']}ch/{batches}b  누적 ${spent:.2f}")

        # 1) 추출 + 후보 critic. rc=2(all_valid=false)는 정상 — 첫-패스 추출은 거의 항상
        # 검증 플래그가 있고 후보 파일은 그래도 기록된다(장물도 동일). 다운스트림 게이트는
        # rc가 아니라 '후보 존재'로만 판단한다. 이미 추출된 조문은 재지출 없이 재사용.
        if candidate_count(cand_dir) >= batches:
            log(f"   [extract skip] 후보 {candidate_count(cand_dir)}개 이미 존재 — 재사용")
            rc = 0
        else:
            rc = run(
                [PY, "scripts/run_fraud_rulegen_pilot.py",
                 "--requests", str(requests),
                 "--run-root", str(EXTRACT_ROOT),
                 "--run-id", slug,
                 "--start", "1", "--limit", str(batches),
                 "--concurrency", str(args.concurrency),
                 "--terra-max-tokens", "16000", "--terra-reasoning-effort", "low",
                 "--with-critic", "--execute"],
                PROJECT_ROOT / f"logs/prop_{slug}_extract.log",
            )
        ext_usd = usage_usd(ext_dir)
        n_cand = candidate_total(cand_dir)
        log(f"   [extract rc={rc}] ${ext_usd:.2f}  후보 {n_cand}개 (rc=2는 검증플래그, 정상)")
        if n_cand == 0:
            log(f"   후보 0개 — 다운스트림 skip (스텁/주석부재 조문)")
            done.append({"article": article, "slug": slug, "extract_usd": ext_usd,
                         "downstream_usd": 0.0, "extract_rc": rc, "downstream_rc": None})
            spent = sum(d["extract_usd"] + d["downstream_usd"] for d in done)
            continue

        # 2) 다운스트림 merge + normcard critic (죄명-불문 드라이버). 이미 완료된
        # 조문(critic_run.json 존재)은 재실행하지 않는다 — 재실행은 캐시 히트라
        # 실비 매니페스트를 cached=true로 덮어써 $0 오계상시킨다.
        ds_dir = DS_ROOT / slug / slug
        if (ds_dir / "critic_run.json").exists():
            log(f"   [downstream skip] 이미 완료 — 재사용")
            rc2 = 0
        else:
            rc2 = run(
                [PY, "scripts/run_rulegen_downstream.py",
                 "--crime-slug", slug, "--article-slug", slug, "--article", article,
                 "--law-id", "001692",
                 "--requests", str(requests),
                 "--candidates-dir", str(cand_dir),
                 "--run-id", slug, "--stage", "all",
                 "--concurrency", str(args.concurrency),
                 "--execute"],
                PROJECT_ROOT / f"logs/prop_{slug}_downstream.log",
            )
        ds_usd = usage_usd(ds_dir)
        log(f"   [downstream rc={rc2}] ${ds_usd:.2f}  (rc2=0 이면 all_valid, 2 이면 일부 검증실패=정상 품질이슈)")
        done.append({"article": article, "slug": slug, "extract_usd": ext_usd,
                     "downstream_usd": ds_usd, "extract_rc": rc, "downstream_rc": rc2})
        spent = sum(d["extract_usd"] + d["downstream_usd"] for d in done)

    total = sum(d["extract_usd"] + d["downstream_usd"] for d in done)
    log(f"=== 완료: {len(done)} 조문 처리 | 실지출 ${total:.2f} ===")
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest": args.manifest.name,
        "articles_done": len(done),
        "total_usd": round(total, 2),
        "per_article": done,
    }
    out = args.summary
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"summary → {out.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
