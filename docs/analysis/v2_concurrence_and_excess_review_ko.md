# 검수: 경합 규칙 승인과 초과의 사실 단위

2026-08-13. 최종 책임 뷰를 파이프라인에 관통시키면서 **검수 없이 결정할 수 없는 것 두 가지**가
남았다. 아래 두 카드에 `> comment:`로 답해 주시면 그대로 반영한다. 구현·산출물은
`experiments/v2_call15_directscope_26_causal/final_responsibility_v10/audit.md`에 있다.

---

## 카드 ①. 인장위조죄가 사문서위조죄에 흡수된다는 규칙을 승인할 것인가

**명제.** 행사할 목적으로 타인의 인장을 위조하고 그 인장으로 타인의 사문서를 위조한 경우,
인장위조죄(형법 제239조)는 사문서위조죄(형법 제231조)에 흡수되어 별도로 성립하지 않는다.

**v2 저작 형태** (`data/v2/concurrence_rules.yaml`)

```yaml
rule_id: absorption.seal_forgery_by_private_document_forgery
kind: absorption
first_offense_ref:  offense.seal_forgery_or_misuse      # 흡수되는 쪽
second_offense_ref: offense.private_document_forgery    # 흡수하는 쪽
occurrence_constraint: same_episode
condition_ref: condition.seal_forgery_was_means_of_document_forgery
```

**확인된 사실.** legacy `data/rulebase/concurrence.yaml`의 `absorbed_by[4]`를 그대로 옮긴 것이고,
조문↔DefinitionRef 매핑은 감사에서 EXACT_ONE_TO_ONE이었다. KCL-26에서 두 죄가 같은 factual
episode에 함께 결박된 문항은 `r12_p2_q1_da` 하나이며 binding:002(사문서위조)와
binding:004(인장위조)가 모두 `factual_episode:001`이다. 다만 그 문항에서 현재 성립한 것은 甲의
위조사문서행사죄뿐이므로, 승인하더라도 이번 run의 결론은 바뀌지 않는다.

**남는 문제.** 조건(`인장위조가 그 사문서위조의 수단이었는가`)을 판정할 채널이 아직 없다.
조건이 없으면 후보는 UNKNOWN으로 남아 두 죄가 **모두 유지되되 unresolved로 표시**된다. 그것이
현재 동작이며, 조건 없이 흡수를 발화시키지는 않는다.

**선택지**

- (가) 규칙을 `approved`로 올린다. 조건 채널이 붙기 전까지는 unresolved 후보로만 보인다.
- (나) `awaiting_legal_review`로 둔다. 후보 자체가 열리지 않는다. (현재 상태)
- (다) 규칙을 승인하면서 조건을 없애고 same-episode + 두 죄 성립만으로 흡수한다.
      -- 위조에 쓰지 않은 인장위조까지 삼킬 수 있으므로 권하지 않는다.

> comment:

---

## 카드 ②. 공범의 초과에서 "같은 사실"의 단위는 무엇인가

**드러난 것.** `plan_accessory_excess_candidates`는 가담자와 정범이 **같은 factual episode**에
있을 것을 요구한다(2026-08-13 저작). 그런데 교사는 본래 실행보다 앞선 episode에서 일어난다.
`r11_p1_q1`이 정확히 그 형태다.

| | episode |
| --- | --- |
| 甲의 절도 교사 | `factual_episode:001` |
| 乙의 절도 실현 | `factual_episode:004` |
| 乙의 상해 실현 | `factual_episode:005` |

그래서 KCL-26 전체에서 초과 후보가 **0개** 열린다. 판단이 "초과 아님"인 것이 아니라 후보가
닿지 않는 것이다. `excess_policies.yaml`에는 이미 절도→상해가 질적 초과 pair로 저작되어 있어,
후보만 열리면 이 문항은 `qualitative / no_liability_for_excess`로 판정된다.

현재는 규칙을 바꾸지 않고 `UNRESOLVED_EXCESS_EPISODE_SCOPE` marker만 남겼다.

**선택지**

- (가) 초과의 사실 단위를 episode가 아니라 **참가 링크**로 바꾼다. 즉 가담자와 이미 확정된
      derivative link로 묶인 정범이 같은 사건에서 실현한 다른 죄를 후보로 연다. 링크 자체가
      "이 교사가 이 실행으로 이어졌다"는 상류 판단이므로, episode 일치를 다시 요구하는 것은
      같은 것을 두 번 묻는 셈이다. -- 이쪽을 권한다.
- (나) episode 요건을 유지하되, 정범의 실현 episode를 기준으로 삼는다(가담 episode가 아니라).
      `r11_p1_q1`이면 ep004 기준이 되어 ep005의 상해는 여전히 빠진다.
- (다) 현행 유지. 초과는 같은 episode 안에서 정범이 다른 죄를 실현한 경우로만 좁힌다.
      KCL-26에서는 계속 0이고 marker로만 보인다.

**주의.** (가)를 택하더라도 `r11_p1_q1`의 rubric 정답(폭행치상)은 여전히 나오지 않는다.
폭행죄 family가 v2에 없어 v2는 乙을 `offense.injury`로 결박했기 때문이다
(`representation_gaps.yaml`의 `gap.assault_offense_family`). 다만 절도→상해 pair가 저작되어
있으므로 질적 초과라는 **분류**는 나온다.

> comment:
