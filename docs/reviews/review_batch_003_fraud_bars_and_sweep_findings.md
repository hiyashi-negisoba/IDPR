# 검수 배치 003 — 사기 룰베이스 BAR 23장과 26문항 실행이 드러낸 것

작성: 2026-08-05 · 브랜치 `antigravity-0804` · 근거: 배치 실행 `219401` (26문항 전량)

답변: 각 `판정:` 줄에 **O** / **X** / 다른 지시. 의견은 `> comment:`.

---

## 이 배치가 생긴 이유

26문항을 돌려 보니 전체 실행에서 **`not_established`(불성립)를 만든 카드가 단 6장**이었습니다.
그 6장 중 하나가 방화죄의 `art164_sec2_1.residence_without_actual_presence` —
*"주거로 사용되는 건조물은 방화 당시 사람이 실제 현존할 필요가 없다"* 였습니다.
상해죄에서 잡았던 것과 **똑같은 극성 역전**이고, 검수 002 D-06에서 지목하신 바로 그 법리인데
배제 목록이 아니라 활성 `bar` 자리에 남아 있었습니다. 이미 `requirement_waived`로 고쳤습니다.

나머지 셋은 전부 **사기죄**에서 나왔습니다. 사기 룰베이스는 배치 001(재산죄 역할표 138장)에도
배치 002(장물죄 146장)에도 들어간 적이 없습니다. 별도 캠페인이라 `BAR_CARD_IDS` 라는
독립 목록으로 관리되고, **전수 검수를 받은 적이 없습니다.**

| 실행에서 불성립을 만든 카드 | 횟수 | 유닛 |
|---|---|---|
| `deception.fraud.definition.deception-target-human` | 3 | 사기 |
| `deception.fraud.causal-link.no-disposition-no-deception` | 2 | 사기 |
| `deception.fraud.element.deception-must-create-false-belief` | 2 | 사기 |
| `art164_sec2_1.residence_factual_use` | 1 | 방화 |
| `art164_sec2_1.residence_without_actual_presence` | 1 | 방화 **(수정 완료)** |
| `art136_sec2_4.active_conduct_requirement` | 1 | 공무집행방해 |

---

# G. 사기 BAR 23장

23장 모두 `polarity=negative` 이고, 문언도 대체로 "성립하지 않는다"로 끝납니다. 극성 자체는
문제가 아닙니다. 대신 **다른 세 가지 오배치**가 보입니다.

## G-01 "미수"를 "불성립"으로 컴파일하는 3장

세 카드는 사기죄가 **미수**라고 말하는데, `bar`에 앉아 사기죄 전체를 불성립시킵니다.
사기미수는 제352조로 처벌되는 범죄이므로 불성립과 같지 않습니다.

| 카드 | 명제 |
|---|---|
| `fraud_general_object.causation_required` | 인과관계가 인정되지 않으면 사기죄는 **기수로** 성립하지 않는다 |
| `fraud_general_object.deception_error_causation` | 다른 동기로 교부한 경우 **사기미수죄만** 성립한다 |
| `fraud_stages_participation.no_causation_attempt` | 인과관계가 인정되지 않으면 사기죄는 **미수이다** |

- 제안: 세 장 모두 `bar`에서 빼고, 기수 트랙만 저지하고 미수 트랙은 살리는 자리로 옮깁니다.
  현재 사기 조립기에 트랙 구분이 없으므로 당장은 **`post_outcome`(기수 부정·미수 성립)** 으로
  두고, 트랙 도입 시 기수 전용 `bar`로 옮기는 것을 권고합니다.
- 판정: 

## G-02 다른 죄로 넘어가는데 `boundary`가 아닌 3장

세 카드는 "사기죄가 아니라 **절도죄/횡령죄**" 라고 명시합니다. 검수 002에서 확립한 대로
이것은 `boundary`(불성립 + 후속 죄명)이지 단순 `bar`가 아닙니다. 지금은 후속 죄명이
컴파일 과정에서 사라져 답안이 "사기 불성립"에서 멈춥니다.

| 카드 | 넘어가는 죄 |
|---|---|
| `fraud_mistake.no_capacity_theft` | 절도죄 |
| `fraud_mistake.trick_theft_directness` | 절도죄 |
| `general_object.fraud.standard.own-possession-other-property-embezzlement` | 횡령죄 |

- 제안: `boundary` + `refers_to` = 절도 / 절도 / 횡령.
- 판정: 

## G-03 실행에서 실제로 발화한 3장 — 문언이 "기준"인지 "결론"인지

이 셋이 26문항에서 사기죄를 실제로 무너뜨렸습니다. 셋 다 조건부 부정문이라, 카드가
`satisfied` 라는 것이 **"이 법리가 옳다"** 인지 **"이 사안이 그 조건에 해당한다"** 인지가
문언만으로는 갈리지 않습니다. 검수 002 D-01과 같은 구조입니다.

| 카드 | 명제 | 발화 |
|---|---|---|
| `deception.fraud.definition.deception-target-human` | 인식능력이 없는 사람은 기망의 상대방이 될 수 없고, 기계는 기망 대상이 될 수 없다 | 3회 |
| `deception.fraud.element.deception-must-create-false-belief` | 진실과 합치하지 않는 관념을 발생시킨 행위가 아니면 기망이 아니다 | 2회 |
| `deception.fraud.causal-link.no-disposition-no-deception` | 착오에 기하여 처분행위를 하게 한 행위가 아니면 기망이 아니다 | 2회 |

특히 첫 번째는 `norm_kind=definition` 입니다. **기망 상대방의 정의**이지 이 사안에서
상대방이 기계였다는 인정이 아닙니다. 세 사건 모두 사람 상대 기망 사안인데 발화했습니다.

- 제안: `deception-target-human` 은 `assessment_standard` 로 이관(기망 상대방 적격의
  판단기준). 나머지 둘은 사기죄의 **필수 구성요건을 뒤집어 쓴 것**이므로, 카드를 부정형
  bar가 아니라 **긍정형 필수 component**("기망은 상대방에게 허위 관념을 발생시켜야 한다",
  "착오에 기한 처분행위가 있어야 한다")로 다시 쓰는 편이 정확합니다.
- 판정: 

## G-04 나머지 14장

아래는 현행 `bar` 유지가 타당해 보입니다. 이견이 있는 카드만 `> comment:` 에 ID로 적어 주세요.

```
deception.fraud.causal-link.loan-purpose-not-sole-trigger
deception.fraud.element.transaction-purpose-no-impairment
deception.fraud.standard.advertising-tolerable-exaggeration
deception.fraud.standard.easily-detectable-lie
deception.fraud.standard.loan-lender-anticipated-risk
deception.fraud.standard.loan-subsequent-default
deception.fraud.standard.vague-opinion-not-deception
fraud_intent.no_disposition_inducement_intent
fraud_mistake.no_thought_no_error
fraud_mistake.omission_not_all_nonclaims
fraud_mistake.property_limited_disposition
general_object.fraud.standard.own-property-not-object
general_object.fraud.standard.public-interest-only-no-fraud
special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime
```

다만 `fraud_mistake.no_thought_no_error`("어떠한 생각도 갖지 않는 경우에는 착오가 인정되지
않는다")와 `fraud_mistake.property_limited_disposition`("처분행위는 재산상 처분행위에
한정되므로…")은 `norm_kind=definition` 이라 G-03과 같은 위험이 있습니다.

- 판정: 

---

# H. 26문항 실행이 드러낸 구조적 사실

## H-01 카드 평가의 85%가 `unknown`

실행된 17개 유닛에서 모델이 평가한 카드 1,253장의 분포입니다.

| 평가 | 장수 | 비율 |
|---|---|---|
| `unknown` | 1,071 | 85.5% |
| `satisfied` | 173 | 13.8% |
| `not_satisfied` | 9 | 0.7% |

성립 결론이 난 유닛은 예외 없이 `satisfied` 비율이 높습니다(방화 17/34, 사문서위조 13/44,
횡령 16/64). 미확정으로 끝난 유닛은 3~7장만 satisfied 입니다(살인 4/141, 절도 3/66).

즉 **미확정의 원인은 규칙이 아니라 평가 단계**입니다. 유닛당 카드가 141장(살인)까지 가는데
전량 평가를 요구하니, 모델이 사안과 무관한 카드까지 훑다가 정작 필요한 요건 카드에서
`unknown`을 냅니다.

- 제안: 이 문제는 카드 보강이 아니라 **평가 단계 설계**로 풀어야 합니다. 다만 전량 평가는
  의도된 설계(top-k 금지)라 임의로 바꿀 수 없어, 별도 논의 항목으로 올립니다.
- 판정: 

## H-02 미확정 유닛이 채우지 못한 요건

| 요건 | 횟수 |
|---|---|
| `theft_*` (절도 고의·점유·불법영득의사) | 각 2 |
| `homicide_attempt_elements` / `voluntary_desistance` | 각 2 |
| 횡령 실행행위·고의·기수 | 각 1 |
| 상해 상해행위 / 존속관계 | 각 1 |
| 주거침입 실행착수 / 범인은닉 3요건 / 준강간 항거불능 | 각 1 |

- 판정: 

## H-03 15문항이 법률과 무관하게 중단됐던 것 — 이미 수정

26문항 중 15문항이 답안을 내지 못했습니다. 원인은 전부 Stage 1 계약 위반이었습니다.

| 원인 | 건수 |
|---|---|
| 이 죄가 받지 않는 당사자 역할을 지정 | 8 |
| 인용문이 지문에 없음 | 8 |
| 적재되지 않은 쟁점이 다른 쟁점에 의존 | 6 |
| 필요한 당사자 역할 누락 | 4 |

쟁점 하나의 결함이 **사건 전체를 폐기**하고 있었습니다. 나머지 5~6개 쟁점은 멀쩡했습니다.
결함 있는 쟁점만 강등해 "규칙 추론이 판정하지 않은 쟁점"으로 답안에 넘기도록 고쳤습니다.

- 판정: 

---

# I. `polarity=exception` 141장 — 게이트 현황 (검수 002 F-03 후속)

승인하신 activation gate를 만들었습니다(`scripts/audit_exception_polarity_cards.py` →
`data/rulegen/exception_polarity_gate.json`).

| 항목 | 수 |
|---|---|
| `polarity=exception` 전체 | 141 |
| 그 중 성립을 막는 자리(bar/boundary/waiver) | 88 |
| 영향받는 유닛 | 25 |

말씀하신 2번 조치("자동 컴파일되는 경우 실행 차단")를 그대로 켜면 **36개 유닛 중 25개가
멈춥니다.** 그래서 기구는 만들되 `enforce: false` 로 두고 감사 경고로만 노출하고 있습니다.

- 제안: 극성 복구 배치가 88장을 훑을 때까지 `enforce: false` 유지. 복구된 카드부터
  `approved` 에 넣어 하나씩 풀고, 전량 처리 후 `enforce: true`.
- 판정: 
