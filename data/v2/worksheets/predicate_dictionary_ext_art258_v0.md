# Predicate 사전 확장 — art258 중상해·존속중상해 (258의2 supporting dependency) v0

## 범위와 Gate① 위치

258은 `data/rulebase/article_catalog.json`의 evaluation/population 80개 조문에는 들지
않는다. 그러나 258의2가 이미 확정한 QUALIFY 4갈래 중 중상해·존속중상해 두 갈래의
base offense이므로, **supporting dependency로서 이번 Gate①의 effective 1-pass 범위에는
포함된다.** 이 문서는 그 dependency가 258의2를 완전하게 조립하는 데 필요한 최소
predicate만 저작한다. 258의 주변 법리·사례·독자 평가 population을 추가하지 않는다.

카드 및 원본 주석 chunk는 현 코퍼스에 없다(`art2582_2` 카드가 258을 base offense로
열거할 뿐이다). 따라서 art339와 같은 카드 없는 예외로, [국가법령정보센터의 현행
형법 제258조](https://www.law.go.kr/LSW/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1031011353)
원문을 직접 source로 삼는다. 원문은 제1항의 생명위험, 제2항의 불구 또는 불치·난치
질병, 제3항의 자기 또는 배우자의 직계존속 가중을 정한다.

## 기존 확정 predicate 재사용

258은 독립적인 상해 유형을 새로 만들지 않고 257 상해의 가중 유형이다. 따라서 아래
기존 id의 canonical_meaning을 재정의하거나 복제하지 않는다.

| id | 258에서의 역할 | 선행 출처 |
|---|---|---|
| `offense.injury[257]` | 중상해의 base offense; 257의 자연인·타인 객체, 상해 결과, 고의 및 기존 completion 구조를 그대로 상속 | 배치⑨ |
| `legal_element.natural_person_victim_status` | base offense 안에서 이미 충족되는 객체 요건 | 250/257 |
| `legal_element.injury_result` | base offense의 상해 결과; 중상해는 그 결과의 법정 가중 형태 | 257 |
| `legal_element.intent` | 중상해의 기본 상해 고의 | 13조/257 |
| `legal_element.lineal_ascendant_of_self_or_spouse_status` | 제258조 제3항의 가중 신분 | 250/257 |
| `legal_element.awareness_of_lineal_ascendant_status` | 제258조 제3항의 행위자 인식 요건 | 250 |

`ground_fact.violence_used`의 명칭은 Master B-8의 기존 2-pass 확인사항이다. 258이
`offense.injury[257]`를 그대로 참조하므로 그 항목을 재개하거나 새 conduct predicate를
만들지 않는다.

## 신규 predicate 1건 — 중상해 결과

| id | type | canonical_meaning | 직접 근거 |
|---|---|---|---|
| `legal_element.serious_injury_result` | legal_element | 257의 상해로 인해 피해자에게 **생명에 대한 위험**이 발생했거나, **불구** 또는 **불치나 난치의 질병**에 이르렀다는 제258조상 중상해 결과가 인정된다 | 형법 제258조 제1·2항 |

이는 단순한 관찰 사실이 아니라 제258조의 세 법정 결과 유형 중 하나에 포섭되는지를
판단하는 법적 결과 요건이므로 `ground_fact`가 아니라 `legal_element`다. 단일 id가
제1항과 제2항의 `ANY`를 내부 legal assessment로 포괄한다. `life_endangerment`,
`disability`, `incurable_disease`, `hardly_curable_disease`를 별도 predicate로 나누면
258의2의 base qualification에 불필요한 세부 법리를 새로 population하게 되므로 하지
않는다.

## 최소 조립 경로

```text
offense.aggravated_injury[258(1)-(2)]
  = QUALIFY(
      base = offense.injury[257],
      additions.result = legal_element.serious_injury_result
    )

offense.aggravated_ancestral_injury[258(3)]
  = QUALIFY(
      base = offense.aggravated_injury[258(1)-(2)],
      additions.subject = legal_element.lineal_ascendant_of_self_or_spouse_status,
      additions.mental = legal_element.awareness_of_lineal_ascendant_status
    )

258의2 = QUALIFY(
  base ∈ {offense.injury[257], offense.ancestral_injury[257],
          offense.aggravated_injury[258(1)-(2)],
          offense.aggravated_ancestral_injury[258(3)]},
  additions = ANY(legal_element.group_or_multiple_force,
                  legal_element.dangerous_object_carriage)
)
```

위 표기는 1-pass vocabulary와 dependency 경로를 동결하는 목적이다. 실제 YAML
`DerivedOffenseDef`/`QualifierDef` 조립은 Gate① 승인 뒤 2-pass에서 한다. 258의 미수,
상습범, 특별법·양형 및 258 자체의 evaluation population은 이 supporting dependency
범위에 넣지 않는다.

## Self-check

- **재사용 우선**: 257의 객체·상해·고의와 250/257의 존속 status·인식은 모두 기존 id를
  그대로 쓴다. 신규 predicate는 법문이 새로 요구하는 중상해 결과 하나뿐이다.
- **층위**: 258은 base offense 위에 결과·신분을 더하는 `QUALIFY`이며, relation이나
  doctrine을 Elements leaf처럼 추가하지 않는다.
- **source coverage**: 원문 직접 저작이라는 예외를 명시했고, 코퍼스에 없는 카드·주석을
  있는 것처럼 가정하지 않았다.
- **scope**: 258의2를 완성하기 위한 두 base variant까지만 추가한다. 80개 evaluation
  coverage는 변하지 않는다.

## Gate① 반영 결과

258의2가 참조하는 네 base branch가 모두 predicate vocabulary 수준에서 닫혔다. 258은
80개 평가 population 밖의 supporting dependency로 유지하되, Gate① 밖으로 미루지
않는다. 신규 스키마·DSL primitive는 없다.
