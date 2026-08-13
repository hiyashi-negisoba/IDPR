# Participation factual-interaction 정상화 제안

## 1. 목적

현재 binding-scoped planner는 Call 2의 Cartesian을 제거했지만 participation target도 0이 됐다.
기존 `participation_local_targets()`는 동일 사건에서 **같은 offense instance를 이미 가진 actor들**을
전부 조합한다. 이 방식은 두 가지 상반된 실패를 만든다.

1. occurrence-aware 전체 universe에서는 5,859개 target과 무관 offense false link를 만든다.
2. binding-scoped universe에서는 교사자·방조자에게 동일 offense direct binding이 없는 경우
   올바른 participation target을 하나도 만들지 못한다.

목표는 participation의 법적 결론을 앞당기는 것이 아니라, 사건 원문에 명시된 사람 사이의
상호작용만 좁게 결박하여 기존 legal participation Call 2가 평가할 후보를 여는 것이다.

## 2. 파이프라인 위치

이 단계는 새로운 법적 추론 Call이 아니라 Call 1.5의 factual binding family에 속한다.
개념적 순서는 다음과 같다.

```text
Call 1 selected legal seeds
  -> Call 1.5 offense/actor factual bindings
  -> Call 1.5-P offense-free factual interactions
  -> host evidence-scoped participation candidate compiler
  -> existing legal participation Call 2
  -> deterministic dependency compiler
  -> Scallop
```

Call 1.5-P는 공범 유형이나 죄명을 판단하지 않는다. 기존 Call 1, Call 1.5 및 Call 2 prompt는
변경하지 않는다.

## 3. Call 1.5-P의 유일한 역할

> 한 factual episode 안에서 한 사람이 다른 사람에게 무엇을 요청·전달·제공했거나,
> 여러 사람이 어떤 행동을 함께 계획·분담했다는 명시적 사실을 exact quote로 결박한다.

입력은 한 번에 factual episode 하나다. 26문항 전체, 모든 seed, 모든 offense를 한 요청에
넣지 않는다.

입력 범위:

- normalized factual episode text
- 그 episode에 실제 등장하는 participant label
- 질문에서 책임을 묻는 actor label

입력 금지:

- offense id와 legal seed
- 구성요건 checklist
- rubric/gold conclusion
- participation mode와 최종 책임

## 4. 제안 출력 계약

```json
{
  "interactions": [
    {
      "interaction_type": "request_or_instruction",
      "source_actor_id": "甲",
      "target_actor_ids": ["乙"],
      "evidence_quotes": ["甲은 乙에게 ... 하라고 부탁하였다"]
    }
  ]
}
```

허용할 factual type은 다음 세 개로 제한한다.

| type | 사실 의미 | 법적 의미가 아님 |
|---|---|---|
| `request_or_instruction` | 특정 행동을 부탁·권유·지시·제안한 명시적 의사소통 | 교사범 성립 아님 |
| `means_information_or_assistance` | 수단·정보·자원·현장 도움을 제공한 명시적 사실 | 방조범 성립 아님 |
| `agreement_or_coordinated_conduct` | 공동 계획, 역할 분담 또는 함께 행동한 명시적 사실 | 공동정범 성립 아님 |

`source_actor_id`와 `target_actor_ids`는 factual direction만 뜻한다. 법적 정범, 교사자,
방조자, 피해자, 도구의 지위를 뜻하지 않는다.

한 episode에 여러 독립 상호작용이 있으면 여러 행을 허용한다. 상호작용이 명시되지 않으면
빈 배열이 유효하다.

## 5. 모델 금지사항

Call 1.5-P는 다음을 출력하거나 추론해서는 안 된다.

- offense ref 또는 적용 조문
- `instigator`, `aider`, `co_principal`, `indirect_principal`
- 범의 형성 시점, 고의, 기능적 행위지배 등 법적 predicate truth
- 정범의 범죄 성립이나 종속성
- 공범의 착오·초과, 신분, completion, 죄수
- DAG edge 또는 최종 liability

특히 “요청이 상대방의 범의를 유발했다”거나 “도움이 실행을 용이하게 했다”는 법적·인과적
평가를 Call 1.5-P가 하지 않는다. 원문에 요청 또는 제공 사실이 있는지만 결박한다.

## 6. Host validation

Host는 의미를 보충하지 않고 다음만 검사한다.

1. 모든 quote가 해당 normalized episode의 exact substring인지 확인한다.
2. actor id가 해당 episode participant universe 안에 있는지 확인한다.
3. source와 target의 self-link, 빈 target, 중복 interaction을 거부한다.
4. quote span과 `TARGET_FACT`/dependency-context provenance를 함께 기록한다.
5. 안정적인 `finteraction:*` identity를 부여한다.

모델이 선택하지 않은 interaction을 host가 텍스트 규칙으로 합성하지 않는다.

## 7. Participation candidate materialization gate

Factual interaction 하나만으로 법적 participation target을 만들지 않는다. 다음 교집합이
있을 때만 기존 legal participation Call 2 후보를 연다.

```text
validated factual interaction
  + 명시적으로 지목된 target actor의 offense binding
  + 질문의 Call 1 candidate offense universe
  -> one bounded legal participation probe
```

### 7.1 Directed interaction

`request_or_instruction` 또는 `means_information_or_assistance`의 target actor가 현재 질문의
normalized factual scope 안에 offense binding을 가지고 있을 때만 후보를 만든다. 지시·도움과
후속 실행은 시간상 서로 다른 factual episode일 수 있으므로 directed interaction에는 episode
동일성을 강제하지 않는다. 대신 모델이 명시적으로 지목한 target actor만 허용한다.

- source actor용 participation-only instance를 별도 identity로 만든다.
- principal instance는 target actor의 실제 binding identity를 그대로 쓴다.
- source interaction quote와 principal action quote를 모두 evidence carrier에 넣는다.
- 기존 legal participation Call 2가 exact offense에 대해 `instigation`, `aiding`을 각각
  TRUE/FALSE/UNKNOWN으로 판단한다.

`request_or_instruction`을 곧바로 instigation TRUE로, `means_information_or_assistance`를
aiding TRUE로 바꾸지 않는다. factual type은 후보 gate일 뿐이다.

### 7.2 Coordinated interaction

`agreement_or_coordinated_conduct`가 있고 참여자 중 적어도 한 명에게 현재 normalized factual
scope의 offense binding이 있을 때만 exact-offense co-principal probe를 연다. 합의·역할분담과
후속 실행은 서로 다른 factual episode일 수 있으므로, 모델이 명시적으로 묶은 participant
집합을 actor gate로 삼는다. direct binding이 없는 다른 참여자는 participation-only member
identity로 들어갈 수 있다. legal Call 2가 공동실행과 공동계획 여부를 판단한다.

### 7.3 Context-only principal

principal action이 질문의 dependency context에만 있더라도 source actor의 interaction quote가
`TARGET_FACT`에 있으면 participation 후보를 열 수 있다. 이때 principal binding은
`DEPENDENCY_ONLY_INSTANCE`로 평가해 종속성 근거로만 쓰고 최종 liability view에는 노출하지
않는다. 이는 `CONTEXT_ONLY_BINDING`을 다시 직접 책임으로 승격시키는 것이 아니다.

## 8. 의도적으로 보류할 범위

### 8.1 Cross-offense derivative

형법 제33조 단서처럼 principal offense와 accessory target offense가 다른 route는 runtime core에
존재하지만 caller가 두 offense의 대응을 선택해야 한다. factual interaction만으로 이 대응을
host가 추론하면 안 된다.

첫 구현에서는 다음만 허용한다.

- 동일 offense derivative candidate
- authored compatibility가 명시된 cross-offense pair

현재 authored compatibility가 없는 pair는 `UNRESOLVED_CROSS_OFFENSE_PARTICIPATION`으로
보존한다. 모든 Call 1 seed를 principal binding과 곱하지 않는다.

### 8.2 Indirect principal

피이용자에 의한 실행과 교사·방조는 identity와 법적 효과가 다르다. factual interaction
artifact는 향후 evidence로 재사용할 수 있지만 ordinary participation target으로 변환하지
않는다. indirect-principal producer는 별도 단계로 유지한다.

### 8.3 Article 263

공동정범의 예에 의한 형법 제263조 후보는 이미 별도 factual pair gate가 있다. 이를 generic
co-principal interaction으로 중복 생성하지 않는다.

## 9. 기대되는 복구 범위와 정직한 한계

현재 rubric과 canonical binding을 대조하면 다음 유형은 이 구조로 후보를 열 수 있다.

- 정범의 direct binding은 있으나 교사자·방조자 direct binding이 없는 사건
- 한 participant만 exact offense binding이 있고 다른 participant는 공동 계획·분담 사실만
  결박된 공동정범 사건
- dependency context의 정범 행위와 target fact의 공범 행위를 연결해야 하는 사건

반면 다음은 이 단계만으로 해결되지 않는다.

- 정범 offense binding 자체가 누락된 사건
- cross-offense pair의 authored compatibility가 없는 사건
- indirect principal, 공범의 착오·초과, 신분, completion, absorption 문제
- interaction이 원문에 암시적일 뿐 exact evidence quote를 잡을 수 없는 사건

따라서 participation recall 100%가 목적이 아니다. 모델 한계 외에 현재 candidate contract가
막고 있는 true link를, 최소 후보로 복구하는 것이 목적이다.

## 10. 평가 지표

26문항 전수 실행 후 다음을 함께 보고한다.

1. factual interaction 수와 contract-valid rate
2. rubric-relevant participation case candidate recall
3. generated legal participation probe 수
4. true-link / false-link / UNKNOWN 분포
5. unsupported 또는 extraneous interaction rate
6. participation compiler reject 수와 원인
7. Scallop derivative/co-principal instance 수
8. 새 establishment의 rubric 질적 정합성
9. Call 2 총 physical request 증가량

과거 5,859 participation target은 비교 baseline이다. 새 producer가 수십~수백 개로 다시
팽창하면 실패로 본다. 목표는 interaction과 실제 principal binding의 교집합에 비례하는 작은
후보 집합이다.

## 11. 구현 승인 경계

승인 전에는 다음을 하지 않는다.

- 새 Call 1.5-P prompt 작성 또는 live 호출
- 기존 Call 1/1.5/2 prompt 수정
- participation candidate를 production planner에 합치기

승인 후에도 먼저 schema, exact-quote validator, dry-run candidate compiler와 synthetic test를
구현한다. 그 결과로 예상 후보 수를 확인한 뒤 job 222907에서 26문항 factual interaction을
실행하고, 마지막에만 기존 legal participation Call 2와 Scallop을 재실행한다.
