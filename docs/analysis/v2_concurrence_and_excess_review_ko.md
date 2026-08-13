# 검수: 경합 규칙 승인과 초과의 사실 단위

2026-08-13. 최종 책임 뷰를 파이프라인에 관통시키면서 **검수 없이 결정할 수 없는 것 두 가지**가
남았었다. **두 카드 모두 검수 완료되어 반영됐다** -- 아래 각 카드의 "검수 결과"를 보라.
구현·산출물은 `experiments/v2_call15_directscope_26_causal/final_responsibility_v10/audit.md`에 있다.

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

> comment: (가) 그대로 승인하지 말고, 조건을 한 단계 좁힌 뒤 approved로 올리는 게 맞습니다.
> 대법원은 타인의 인장을 위조해 그 인장으로 사문서를 위조한 경우 원칙적으로 인장위조가
> 사문서위조에 흡수된다고 봅니다. 다만 후속 판례는 문서의 구성부분이 되는 인영 위조만
> 흡수되고, 인과(도장 자체)를 별도로 제작한 행위는 독립한 사인위조죄라고 명확히 구별합니다.
> 따라서 현재 condition만으로는 너무 넓습니다. rule 자체는 승인하되 condition을 "해당 문서의
> 구성부분이 된 인영의 위조"로 좁혀야 합니다. (다)는 반대합니다.

### 검수 결과 -- 반영 완료

조건을 `condition.forged_seal_impression_is_a_constituent_part_of_the_document`로 좁히고
`status: approved`로 올렸다. 넓은 조건(`..._was_means_of_document_forgery`)은 폐기했다.
`offense.seal_forgery_or_misuse`가 인영 위조와 인과 제작을 모두 담으므로 그 구별은 조건이 진다.

조건 assessment 채널은 아직 없어 후보는 UNKNOWN(unresolved)으로 남는다. KCL-26에서는
`r12_p2_q1_da`의 두 위조죄가 성립하지 않아 후보 자체가 열리지 않았다.

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

> comment: (가) 승인. 초과의 연결 단위는 factual episode가 아니라 이미 확정된
> participation/derivative link로 바꾸는 게 맞습니다. 교사범은 교사행위와 정범 실행이 시간적으로
> 분리되는 것이 정상이고, 판례도 핵심을 "교사행위로 정범이 범죄 실행을 결의하고 실제
> 실행했는가"라는 연결관계에서 찾습니다. 다만 단순히 "같은 사건의 정범이 저지른 모든 죄"까지
> 넓히면 안 되고 해당 derivative link의 principal realization에서 이어지는 실행 범위로 제한해야
> 합니다. r11_p1_q1의 폭행치상 family 미저작은 그대로 representation gap으로 남기는 것도 맞습니다.

### 검수 결과 -- 반영 완료

`plan_accessory_excess_candidates`의 join을 교체했다. 후보 universe는 확정된 derivative link의
principal이며, 세 join으로 제한한다.

1. linked principal과 **같은 행위자**가 실현한 죄 -- 사건 안의 다른 사람이 저지른 죄는 제외.
2. linked principal realization의 **episode 이후** -- 그 실행보다 앞선 죄는 초과일 수 없다.
3. **교사 대상과 다른** offense ref.

2번을 위해 planner가 `factual_episode_order`를 함께 나른다. episode id가 사실상 순번이더라도
그 우연에 기대지 않는다.

`r11_p1_q1`이 발화한다 -- 甲 `offense.theft` -> 乙 `offense.injury`,
`qualitative / no_liability_for_excess`. host 분류와 전용 Scallop relation의 parity도 통과했다.
폭행치상 미저작은 `gap.assault_offense_family`로 그대로 남겼다.

---

## 카드 ③. 초과 효과를 누가 소비하는가 (후속 검수, 반영 완료)

> comment: **1번부터 정해야 하고, 이건 Call 3에 맡기면 안 됩니다.** `no_liability_for_excess`는
> 서술 문제가 아니라 가담자의 책임 범위를 제한하는 substantive symbolic conclusion이니까
> final responsibility 단계가 소비해야 합니다. 초과하여 실현된 offense에 대해서는 가담자
> liability를 생성·유지하지 않고, 원래 교사·방조한 offense에 대한 liability는 그대로 유지하며,
> excess finding 자체는 provenance로 기록합니다. 전체 liability result를 FALSE로 덮어쓰는 것도
> 아니고 Call 3에 메모만 넘기는 것도 아니고, **해당 excess offense로의 attribution edge만
> 차단하는 효과**입니다. `unresolved`일 때는 무책임으로 접으면 안 되고 반대로 중한 죄
> liability를 세워서도 안 됩니다. Call 3는 나중에 이 typed 결과를 보고 설명만 해야 합니다.

### 검수 결과 -- 반영 완료

`plan_excess_attributions`가 각 초과 판정을 하나의 귀속 결정으로 바꾼다.

| effect | 귀속 결정 |
| --- | --- |
| `liable_for_instigated_scope` | `NOT_ATTRIBUTABLE_BY_EXCESS` |
| `liable_for_aggravated_result` | `attributed` |
| `no_liability_for_excess` | `NOT_ATTRIBUTABLE_BY_EXCESS` |
| `unresolved` | `UNRESOLVED_EXCESS_ATTRIBUTION` |

차단은 그 excess offense의 가담자 instance 하나에만 미친다. 뷰가 `final_instances`와
`attribution_withheld_instances`를 따로 내며, 원래 교사한 죄의 liability는 건드리지 않는다.
순서도 바꿨다 -- 초과가 경합보다 먼저 돈다. 귀속이 차단된 죄는 애초에 그 가담자의 죄가 아니므로
흡수하거나 흡수당하는 자리에 서면 안 된다.

`r11_p1_q1`에서 甲의 `offense.injury` 귀속은 `NOT_ATTRIBUTABLE_BY_EXCESS`이고
`blocked_instance`는 `None`이다 -- 甲의 상해 참가가 애초에 성립하지 않아 차단할 instance가
없었다. "생성되지 않음"과 "생성 후 제거"를 구분해 기록한다.
