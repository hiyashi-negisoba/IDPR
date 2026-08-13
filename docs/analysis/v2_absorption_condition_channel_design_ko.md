# 검수 요청: 흡수 조건 assessment 채널 설계

2026-08-13. 프롬프트는 아직 쓰지 않았고 모델도 부르지 않았다. 이 문서 승인 후에 프롬프트 전문을
따로 올린다.

승인된 흡수 규칙은 하나다(`data/v2/concurrence_rules.yaml`).

```yaml
rule_id: absorption.seal_forgery_by_private_document_forgery
first_offense_ref:  offense.seal_forgery_or_misuse      # 흡수되는 쪽
second_offense_ref: offense.private_document_forgery    # 흡수하는 쪽
condition_ref: condition.forged_seal_impression_is_a_constituent_part_of_the_document
```

조건을 물을 곳이 없어 후보가 열려도 UNKNOWN이다. 이 문서는 그 채널을 연다.

## 1. pair identity

조건은 단일 instance의 predicate가 아니라 **두 instance 사이의 관계**다. 따라서 Article 263과
같은 pair-scoped carrier로 만들고 ordinary predicate Call 2에 얹지 않는다.

```python
ConcurrenceConditionPair(
    pair_id="concurrence-pair:0001",
    rule_id="absorption.seal_forgery_by_private_document_forgery",
    condition_ref="condition.forged_seal_impression_is_a_constituent_part_of_the_document",
    absorbed=OffenseInstanceKey(case, 甲, offense.seal_forgery_or_misuse, binding:004),
    absorbing=OffenseInstanceKey(case, 甲, offense.private_document_forgery, binding:002),
    factual_episode_id="factual_episode:001",
)
```

`left/right`가 아니라 `absorbed/absorbing`으로 이름 붙인다. 흡수는 방향이 있고, 그 방향은
authored rule의 `first/second`가 이미 정했다. 모델에게는 방향을 묻지 않는다.

## 2. candidate opening -- host가 하는 것은 여기까지

1. **승인된 rule**이 있을 것 (`status: approved`).
2. rule의 두 offense ref에 각각 **계획된 top-level instance**가 존재할 것.
3. **같은 factual episode**일 것.
4. **같은 행위자**일 것. -- 아래 카드 A.

host는 여기서 멈춘다. same episode + 두 죄 존재만으로 조건을 TRUE로 만들지 않는다. "그 인영이
바로 그 문서의 구성부분이 되었는가"만 모델이 판단한다.

**평가 시점과 해소 시점의 후보가 다르다는 점이 중요하다.** 조건 assessment는 Call 2 시점이라
*계획된* instance로 후보를 열고, 실제 흡수는 최종 책임 단계에서 *성립한* instance에만 적용된다.
따라서 assessment 후보 ⊇ 해소 후보이며, 조건이 TRUE여도 한쪽이 성립하지 않으면 흡수는 발화하지
않는다. 이번 KCL-26이 정확히 그 상태다(아래 6번).

## 3. 모델 payload

```json
{
  "case_id": "kcl_criminal_r12_p2_q1_da",
  "pair_id": "concurrence-pair:0001",
  "condition_statement": "위조된 인영이 그 문서의 구성부분이 되었는가",
  "legal_standard": "…(아래 카드 B에서 저작)…",
  "actor_id": "甲",
  "factual_episode_id": "factual_episode:001",
  "episode_text": "甲은 A를 살해한 직후 병실에 보관되어 있던 A의 인감도장을 가지고 나온 다음 …",
  "first_conduct": {"evidence_quote": "A의 인감도장을 가지고 나온"},
  "second_conduct": {"evidence_quote": "‘A가 甲에게 인감증명서 발급을 위임한다’는 취지의 A명의 위임장 1장을 작성"}
}
```

- 죄명·조문·`absorption`·`흡수` 같은 낱말은 넣지 않는다. Call 1.5-D에서와 같은 경계다.
  두 행위를 `first_conduct`/`second_conduct`로만 제시한다.
- `episode_text`는 Call 1.5-D에서 확정한 canonical whitespace form을 쓴다. prompt와
  exact-substring 검증이 같은 문자열을 본다.
- evidence quote는 Call 1.5가 이미 결박한 actor-action fragment 그대로다. host가 새로 고르지
  않는다.

## 4. 출력 -- 좁은 relation assessment

```json
{
  "pair_id": "concurrence-pair:0001",
  "truth": "TRUE | FALSE | UNKNOWN",
  "supporting_quotes": ["A명의 위임장 1장을 작성"]
}
```

계약(hard-fail, repair 없음): `pair_id` const 고정, truth 3치, TRUE일 때 `supporting_quotes`가
비지 않고 각 인용이 canonical `episode_text`의 exact substring일 것. 위반 시 그 pair는 reject하고
UNKNOWN으로 남긴다 -- 근거 없는 흡수는 흡수하지 않는 것보다 나쁘다.

## 5. 결과 lowering -- 기존 런타임을 그대로 쓴다

`resolve_concurrence`의 `condition_truths`에 `(rule_id, first, second) -> truth`로 넣으면 끝이고
새 심볼릭 코드는 없다.

| truth | 효과 |
| --- | --- |
| TRUE | 흡수 발화. 인장위조 instance가 `absorbed_instances`로 가고 `final_instances`에서 빠진다 |
| FALSE | 효과 없음. 두 죄 모두 유지 |
| UNKNOWN | 두 죄 모두 유지 + `unresolved_concurrence_candidates`에 기록 (현재 동작과 동일) |

복수 parent나 cycle은 지금처럼 host가 고르지 않고 unresolved로 보존한다.

## 6. KCL-26 실제 수

| 항목 | 수 |
| --- | --- |
| 승인된 rule | 1 |
| 열리는 pair 후보 (계획 instance 기준) | **1** |
| 신규 neural 요청 | **1** (pair 전용) |
| ordinary predicate target 증분 | **0** |

유일한 후보는 `r12_p2_q1_da` 甲, `binding:002`(사문서위조) ← `binding:004`(인장위조), 둘 다
`factual_episode:001`이다.

**최종 liability 변화는 0일 가능성이 매우 높다.** 그 문항에서 현재 성립한 것은 위조사문서행사죄와
위계공무집행방해죄뿐이고 두 위조죄는 모두 elements에서 멈춘다. 조건이 TRUE로 나와도 해소 단계에서
흡수할 대상이 성립하지 않는다. **발화 수를 만들려고 조건이나 candidate gate를 넓히지 않는다.**
여기서 확인할 것은 live path가 구조적으로 닫히는지뿐이다.

## 7. 병합: additive delta인가, 별도 carrier인가

**별도 carrier가 맞다.** `merge_v2_call2_additive_delta.py`의 키는
`(actor, offense_ref, occurrence_id, predicate_ref)`이고 pair는 그 키 공간에 없다. 억지로 넣으면
한 instance의 predicate로 위장하게 되어 방향(어느 쪽이 흡수되는지)이 사라진다.

그래서 Article 263과 같은 형태로 간다: Call 2 row에 `concurrence_condition_assessments` 블록을
추가하고, 병합은 append-only 계약을 그대로 물려받은 얇은 스크립트가 한다.

- pair_id는 baseline에 없던 것만 추가한다.
- 이미 있는 pair_id는 덮어쓰지 않는다.
- 각 assessment에 `source_run` provenance를 남긴다.
- 두 run의 model/prompt fingerprint를 비교한다.

즉 계약은 공유하고 키 공간만 다르다.

---

## 카드 A. pair에 **같은 행위자** 요건을 넣을 것인가

현재 `plan_concurrence_candidates`는 case + episode + exact offense ref만 본다. **행위자를 보지
않는다.** 특별관계 흡수(`plan_specialty_candidates`)에는 행위자 일치 요건이 있지만 authored
absorption에는 없다.

한 episode에 甲의 사문서위조와 乙의 인장위조가 함께 있으면 지금 규칙으로는 甲의 문서위조가 乙의
인장위조를 삼킨다. KCL-26에서는 둘 다 甲이라 이번에는 드러나지 않는다.

- (가) `ConcurrenceRule`에 `actor_constraint: same`을 저작하고 이 규칙에 붙인다. -- 권고.
- (나) 모든 absorption에 행위자 일치를 강제한다. (규칙별 저작 없이 일괄)
- (다) 현행 유지.

> comment:

---

## 카드 B. 조건의 canonical meaning / legal standard를 어떻게 저작하는가

모델에게 조건 문장 하나만 주면 "인영"과 "구성부분"을 스스로 해석한다. `condition_ref`에 대응하는
설명을 저작해 payload에 함께 실어야 한다. 초안:

> 어떤 사람의 인장을 눌러 찍은 자국(인영)이 그 문서의 일부로 들어가, 그 문서가 그 사람 명의로
> 작성된 것처럼 보이게 하는 데 쓰였는지를 본다. 도장 자체를 따로 만들어 두었을 뿐 그 문서에
> 찍히지 않았다면 해당하지 않는다.

법리명("흡수", "법조경합")은 넣지 않는다.

> comment:

---

## 카드 C. 이 사안은 **위조가 아니라 부정사용**이다

`offense.seal_forgery_or_misuse`는 두 형태를 담는다(`forgery_without_authority` 또는
`improper_use_of_genuine_seal`). 그런데 `r12_p2_q1_da`의 사실은 **A의 진짜 인감도장을 가지고 나와**
위임장에 쓴 것이므로 위조가 아니라 부정사용이다.

승인된 조건은 "**위조된** 인영이 그 문서의 구성부분이 되었는가"로 좁혀져 있으므로, 이 사안에서는
조건이 FALSE로 나오는 것이 문언상 맞다. 그러면 유일한 후보가 FALSE로 닫히고 채널은 구조만 확인된다.

- (가) 그대로 둔다. 조건이 제 일을 한 것이므로 FALSE가 정답이다. -- 권고.
- (나) 조건을 "위조 또는 부정사용된 인영"으로 넓힌다. 부정사용 인영이 문서의 구성부분이 된
      경우도 흡수로 보는 견해가 있다면 별도 규칙으로 저작하는 편이 낫다.

여기서 (나)를 택하는 것은 **발화 수를 만들려고 조건을 넓히는 것**에 해당할 수 있으므로, 법리적
근거가 있을 때만 택해야 한다.

> comment:

---

## 다음 단계 (승인 후)

1. `ConcurrenceConditionPair` + 계약/검증 (`runtime/concurrence_condition.py`).
2. planner가 pair 후보를 열고 plan에 직렬화.
3. 프롬프트 전문 검수 -> 설치.
4. 1 pair 실행 -> 별도 carrier 병합 -> `resolve_concurrence` -> 최종 책임 뷰 확인.
