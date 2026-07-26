# 재산죄 10단위 — 죄종별 성립요건 조건식

component 재분해를 마친 뒤의 최종 구조다. `established`는 모든 단위에서 공통이다:

```
<unit>_established =
    <unit>_elements_satisfied
    ∧ case_assessment_complete
    ∧ ¬<unit>_has_negative   (bar 카드 충족 또는 필수요건 명시적 not_satisfied)
    ∧ ¬<unit>_has_conflict   (같은 쟁점에 satisfied·not_satisfied 동시 증명,
                              또는 대안 트랙 두 개가 동시에 충족되는 경우)
```

아래는 단위마다 달라지는 `elements_satisfied`(component AND/OR 구조)와
bar·waiver·boundary·가중 플래그 개수다. component 이름 옆 숫자는 그 요건을
인정하는 카드(대안적 인정경로) 개수 — 그 안은 전부 OR다.

## 절도(야간주거침입·특수·상습 포함) (`theft`, art329, art330, art331, art332, art342)

```
theft_elements_satisfied = object_ownership ∧ object_possession ∧ conduct ∧ intent ∧ appropriation_intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object_ownership | 5 |
| object_possession | 14 |
| conduct | 2 |
| intent | 3 |
| appropriation_intent | 4 |
| completion | 2 |

역할 분포: bar 13 / waiver 1 / boundary 2 / 가중 attempt(1)·habitual(9)·nighttime_residential(7)·special(9)

규칙 309개 / 술어 154개

---

## 강도류 (`robbery`, art333, art334, art335, art337, art338, art343)

```
robbery_elements_satisfied =
           [conduct ∧ causation ∧ intent ∧ completion ∧ object_property ∧ completion_property]  ← 'property' 트랙
           OR [conduct ∧ causation ∧ intent ∧ completion ∧ object_benefit ∧ completion_benefit]  ← 'benefit' 트랙
```

| component | 인정경로 카드 수 |
|---|---:|
| object_property | 1 |
| object_benefit | 5 |
| conduct | 9 |
| causation | 4 |
| intent | 2 |
| completion | 4 |
| completion_property | 2 |
| completion_benefit | 1 |

역할 분포: bar 16 / waiver 7 / boundary 4 / 가중 death(10)·injury(7)·preparation(6)·quasi(26)·special(7)

규칙 441개 / 술어 222개

---

## 공갈 (`extortion`, art350)

```
extortion_elements_satisfied = object ∧ conduct ∧ causation ∧ intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 5 |
| conduct | 17 |
| causation | 1 |
| intent | 2 |
| completion | 4 |

역할 분포: bar 7 / waiver 2 / boundary 3

규칙 204개 / 술어 102개

---

## 배임수증재 (`breach_of_trust_bribe`, art357)

```
breach_of_trust_bribe_elements_satisfied = object ∧ conduct ∧ intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 12 |
| conduct | 12 |
| intent | 2 |
| completion | 3 |

역할 분포: bar 9 / waiver 3 / boundary 0

규칙 198개 / 술어 99개

---

## 점유이탈물횡령 (`lost_property_embezzlement`, art360)

```
lost_property_embezzlement_elements_satisfied = object ∧ conduct ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 4 |
| conduct | 3 |
| completion | 1 |

역할 분포: bar 2 / waiver 0 / boundary 4

규칙 77개 / 술어 45개

---

## 재물손괴 (`property_damage`, art366)

```
property_damage_elements_satisfied = object ∧ conduct ∧ intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 18 |
| conduct | 17 |
| intent | 2 |
| completion | 1 |

역할 분포: bar 15 / waiver 0 / boundary 0

규칙 255개 / 술어 122개

---

## 권리행사방해 (`interference_with_exercise_of_right`, art323)

```
interference_with_exercise_of_right_elements_satisfied = object_ownership ∧ object_possession ∧ conduct ∧ intent
```

| component | 인정경로 카드 수 |
|---|---:|
| object_ownership | 3 |
| object_possession | 12 |
| conduct | 5 |
| intent | 2 |

역할 분포: bar 7 / waiver 2 / boundary 0

규칙 154개 / 술어 81개

---

## 횡령·업무상횡령 (`embezzlement`, art355, art356)

```
embezzlement_elements_satisfied = object_ownership ∧ custody ∧ conduct ∧ intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object_ownership | 5 |
| custody | 2 |
| conduct | 16 |
| intent | 18 |
| completion | 1 |

역할 분포: bar 17 / waiver 2 / boundary 0 / 가중 occupational(4)

규칙 304개 / 술어 147개

---

## 배임·업무상배임 (`breach_of_trust`, art355, art356)

```
breach_of_trust_elements_satisfied = object ∧ conduct ∧ intent ∧ appropriation_intent ∧ completion
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 6 |
| conduct | 7 |
| intent | 5 |
| appropriation_intent | 4 |
| completion | 2 |

역할 분포: bar 9 / waiver 0 / boundary 0 / 가중 occupational(3)

규칙 173개 / 술어 90개

---

## 업무자 가중신분(공유) (`occupational_status`, art356)

```
occupational_status_elements_satisfied = object
```

| component | 인정경로 카드 수 |
|---|---:|
| object | 9 |

역할 분포: bar 1 / waiver 0 / boundary 0

규칙 53개 / 술어 32개

---
