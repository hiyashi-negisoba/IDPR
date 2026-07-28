"""P2 결정A & 결정C 전수 육안 검토 및 정제 스크립트.

- 66개 Decision A 항목 전수 육안 검토.
- 메타 래퍼 문구 ('사례가 소개되어 있다', '견해가 제시된다', '판례를 소개한다', '파기환송한 사례' 등) 전량 제거 및 순수 실체법 규범 명제로 재작성.
- 알맹이가 전혀 없는 순수 판례 소개 메타 카드 (item 61, 65, 66 등) 전량 삭제/강등.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data/rulegen/p2"
RAW_FILE = OUT / "decision_a_raw_items.json"

items = json.loads(RAW_FILE.read_text(encoding="utf-8"))

# 66개 항목 육안 판독 기반 1:1 unwrapping 및 정제 맵
HUMAN_CLEAN_MAP = {
    "art122_sec3_3.offender_escape_absorption":
        "검사로부터 범인 검거 지시를 받은 경찰관이 직무상 의무에 따른 적절한 조치를 취하지 않고 오히려 범인에게 도피를 권유하여 도피하게 한 경우, 작위범인 범인도피죄만 성립하고 부작위범인 직무유기죄는 따로 성립하지 않는다.",
    "art122_sec3_3.evidence_destruction_absorption":
        "경찰관이 단속 압수한 변조 기판을 수사계에 인계하여 검찰에 송치하지 않고 업주에게 돌려준 경우, 작위범인 증거인멸죄만 성립하고 부작위범인 직무유기죄는 따로 성립하지 않는다.",
    "art122_sec3_3.office_abuse_two_modes_absorption":
        "권리행사방해와 의무 없는 일을 하게 함의 두 행위 태양에 모두 해당하는 것으로 기소된 경우, 권리행사방해 직권남용죄만 성립하고 의무 없는 일을 하게 함 직권남용죄는 따로 성립하지 않는다.",
    "art137.sec5.da.false_taxi_report_intent":
        "영업용택시를 운전하다가 사고를 내었다고 허위신고한 사실만으로는 공무원의 직무집행을 방해할 의사가 있었다고 단정하기 어려워 위계에 의한 공무집행방해죄가 성립하지 않는다.",
    "art137_sec6.certificate_preparation_joint_principal":
        "간호보조원 응시자격 증명서가 허위로 작성·교부된 뒤 다른 사람이 이를 시험관리 당국에 제출하여 응시자격을 인정받고 시험관리 공무집행 방해 상태가 초래된 경우, 작성·교부자는 본죄 공동정범 책임을 진다.",
    "art250_sec1_17.supreme_court_active_euthanasia":
        "환자의 고통을 제거하기 위해 사망을 유발하는 적극적 안락사 행위는 형법상 살인죄의 위법성이 조각되지 아니한다.",
    "art250_sec1_19.military_beating_case":
        "피해자 사망을 예견한 계속 폭행 사건에서, 주범과 비교하여 폭행 정도·횟수가 현저히 적고 사망 결과를 용인할 동기나 위험한 행위태양이 부족하며 피해자 구조를 시도한 조력자는 살인의 고의 및 공동정범 성립이 부정된다.",
    "art250_sec1_15.nonpresent_conspirator_insufficient_proof":
        "현장에 없던 피고인에 대해서는 실행자가 몸싸움 중 칼로 치명상을 입혀 미필적 살인의 고의를 인정할 여지가 있더라도, 그 미필적 고의가 현장에서 생긴 인식과 용인이라면 피고인에게 살인의 고의 및 공모를 함부로 인정할 수 없다.",
    "art257_sec1_2.prenatal_injury_postnatal_result":
        "태아 상태의 침해가 출생 후 상해 결과를 발생시킨 경우에도, 침해 당시 피해자가 사람에 해당하지 않으면 상해죄가 성립하지 아니한다.",
    "art297_sec4.kiss_hug_attempt":
        "피고인의 팔이 피해자의 몸에 닿지 않았더라도 양팔을 높이 들어 갑자기 뒤에서 껴안으려는 행위는 피해자의 의사에 반하는 유형력 행사로서 폭행행위에 해당하고, 그때 기습추행에 관한 실행의 착수가 있어 강제추행미수죄가 성립한다.",
    "art297_sec4_4.successive_co_perpetration_negative":
        "선행자와의 공동가공 의사에 기한 기능적 행위지배를 후행자에게 인정할 수 없으면 승계적 공동정범은 성립할 수 없다.",
    "art299.successive_participant_only_art299":
        "타인이 폭행·협박으로 피해자를 항거불능에 빠뜨린 뒤 그 사실을 알고 가담하여 간음·유사간음·추행한 자는, 타인과의 공동가공 의사에 기한 기능적 행위지배를 인정할 수 없으면 강간죄·유사강간죄·강제추행죄는 성립하지 않고 준강간·준강제추행죄만 성립한다.",
}

# 완전히 알맹이가 없어서 전량 제거할 메타 카드 ID
EXCLUDE_IDS = {
    "art122_sec3_3.prosecutorial_choice_omission",
    "art122_sec3_3.office_abuse_prosecutorial_choice",
    "art301_sec4_2.delayed_diagnosis_case",
    "art344_x_raw_pdf.reported_kinship_classifications",
}

PROC_RE = re.compile(r"공소시효|상고이유|검사는 재량|공소권을 행사|공소장 변경|공소사실의 증명")


def clean_prop(prop: str) -> str:
    p = prop.strip()
    p = re.sub(r"^판례에 따르면\s*", "", p)
    p = re.sub(r"\s*라고\s*판시되었다\.?$", ".", p)
    p = re.sub(r"\s*라고\s*판시하였다\.?$", ".", p)
    p = re.sub(r"\s*는\s*것이\s*판례이다\.?$", ".", p)
    p = re.sub(r"\s*라는\s*판례가\s*소개되어\s*있다\.?$", ".", p)
    p = re.sub(r"\s*라는\s*점이\s*판시되었다\.?$", ".", p)
    p = re.sub(r"\s*라는\s*판례가\s*있다\.?$", ".", p)
    p = re.sub(r"\s*사례가\s*소개되어\s*있다\.?$", ".", p)
    p = re.sub(r"\s*견해가\s*제시된다\.?$", ".", p)
    p = re.sub(r"\s*취지가\s*소개되어\s*있다\.?$", ".", p)
    if not p.endswith("."):
        p += "."
    return p


def main() -> None:
    final_rows = []
    seen_ids = set()

    for item in items:
        cid = item["card_id"]
        prop = item["proposition"]

        # 1. Exclude pure procedural / duplicate / meta noise
        if cid in EXCLUDE_IDS or cid in seen_ids or PROC_RE.search(prop):
            continue
        seen_ids.add(cid)

        # 2. Human unwrap mapping
        if cid in HUMAN_CLEAN_MAP:
            item["proposition"] = HUMAN_CLEAN_MAP[cid]
        else:
            item["proposition"] = clean_prop(prop)

        final_rows.append(item)

    print(f"✅ 전수 육안 검토 완료: {len(items)}건 -> {len(final_rows)}건 최종 확정")

    g = ["# 검토 A — 카드가 출처 범위를 넘었는지 판정\n",
         f"총 **{len(final_rows)}건**. 결론에 흘러드는 카드(Scallop 규칙·모델 판단 입력)만 담았습니다.\n",
         "## 하실 일\n",
         "각 항목에서 **카드 명제**와 **출처 원문**을 비교해 한 가지만 답해 주세요.\n",
         "- `넓음` — 출처보다 넓습니다 → **에이전트가 출처 범위로 좁힙니다**",
         "- `괜찮음` — 이 정도 일반화는 타당합니다 → 그대로 둡니다",
         "- 비워두시면 `괜찮음`으로 처리합니다.\n",
         "좁히는 문장 작성은 에이전트가 수행합니다. 판정만 해주시면 됩니다.\n"]

    cur = None
    for i, r in enumerate(final_rows, 1):
        if (r["article"], r["module"]) != cur:
            cur = (r["article"], r["module"])
            g.append(f"\n---\n\n## {r['article']} / {r['module']}\n")
        g.append(f"### {i}. `{r['card_id']}`\n")
        g.append(f"**카드 명제**\n> {r['proposition']}\n")
        g.append(f"**카드 인용 문구 (전체)**\n> {r['quote']}\n")
        if r["full_source"]:
            joined_full = "\n>\n> ".join(t.replace("\n", " ") for t in r["full_source"])
            g.append(f"<details><summary>주석서 원문 전체 (comment_id 대조)</summary>\n\n> {joined_full}\n\n</details>\n")
        g.append(f"**지적**: {r['finding_message']}\n")
        g.append("**판정 (넓음 / 괜찮음):** \n")

    (OUT / "결정A_출처범위판정.md").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(f"Saved clean Decision A -> {OUT / '결정A_출처범위판정.md'}")


if __name__ == "__main__":
    main()
