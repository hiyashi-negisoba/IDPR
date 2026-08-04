# 살인 RuleIR 제안 07 — 존속살해와 예비·음모 (Ⅱ.*, 제255조, 43장)

track 어휘는 제안 01·03을 따른다. `parricide`는 `base`를 상속한다.

## 초안 — 존속살해의 성격 (Ⅱ.1, Ⅱ.5, 3장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 3 | approve | component | ancestral_relation / mandatory_all | parricide | 자기 또는 배우자의 직계존속을 살해함으로써 성립 |
| 4 | context_only | context_only | - | - | 부진정신분범이라는 성격 규정. 효과는 #240·#241이 담고 있다 |
| 193 | context_only | context_only | - | - | #4와 같은 성격 규정 |

## 초안 — 직계존속의 범위 (Ⅱ.6, 14장)

정의(필수)와 인정 경로(택일)를 분리한다. 상해의 `ancestral_relation`에서 쓴 구조와 같다.

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 202 | approve | component | ancestral_relation / mandatory_all | parricide | 객체는 자기 또는 배우자의 직계존속 |
| 198 | approve | component | ancestral_relation / mandatory_all | parricide | 부모·조부모·증조부모·외조부모 등이 포함된다 |
| 204 | approve | component | ancestral_relation_timing / mandatory_all | parricide | 신분관계는 살해행위의 착수 당시 존재하면 충분 |
| 194 | approve | component | ancestral_relation_basis / alternative_any | parricide | 입양으로 형성되는 법정혈족관계 |
| 196 | approve | component | ancestral_relation_basis / alternative_any | parricide | 친생자 출생신고도 입양 요건을 갖추면 입양의 효력 |
| 201 | approve | component | ancestral_relation_basis / alternative_any | parricide | 혼인외 출생자와 생모는 출생으로 법률상 친족관계 |
| 238 | approve | component | ancestral_relation_basis / alternative_any | parricide | 결정 C 선택. 일반양자가 실부모를 살해하면 존속살해 |
| 195 | approve | bar | ancestral_relation / not_applicable | parricide | 입양요건을 갖추지 않으면 직계존비속이 아니다 |
| 197 | approve | bar | ancestral_relation / not_applicable | parricide | 백부모·숙부모 등 방계혈족은 제외 |
| 199 | approve | bar | ancestral_relation / not_applicable | parricide | 엄격해석. 등록부 기재만으로는 법률상 친자관계가 생기지 않는다 |
| 200 | approve | bar | ancestral_relation / not_applicable | parricide | 인지 전 혼인외 출생자와 생부 사이에는 관계가 없다 |
| 203 | approve | bar | ancestral_relation / not_applicable | parricide | 배우자는 법률상 배우자만을 뜻한다 |
| 205 | approve | bar | ancestral_relation / not_applicable | parricide | 계부모는 직계존속이 아니다 |
| 239 | approve | bar | ancestral_relation / not_applicable | parricide | 결정 C 선택. 사망한 배우자의 직계존속은 포함되지 않는다 |

#199와 #205는 상해의 #61(등록부 기재)·#60(법률상 개념)과 같은 법리다. 두 unit이 같은
규칙을 각자 갖는 것은 중복이 아니라 각 조문의 provenance다.

## 초안 — 존속살해의 고의 (Ⅱ.8, 2장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 206 | approve | component | ancestral_intent / mandatory_all | parricide | 자기 또는 배우자의 직계존속을 살해한다는 고의 |
| 207 | approve | bar | ancestral_intent / not_applicable | parricide | 신분을 인식하지 못하면 보통살인죄의 죄책에 그친다 |

#207이 `bar`이면 존속살해 track만 저지되고 `base`는 그대로 성립한다. "존속살해가 아니라
보통살인"이라는 결론이 track 구조로 표현된다 — 중지미수에서 쓴 것과 같은 방식이다.

## 초안 — 죄수와 비신분자 공범 (Ⅱ.9, Ⅱ.10, 6장)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 192 | approve | post_outcome | concurrence / not_applicable | parricide | - | 존속살해가 성립하면 보통살인죄는 특별관계로 별도 성립하지 않음 |
| 237 | approve | post_outcome | concurrence / not_applicable | parricide | arson_of_occupied_structure | 전문가 재정. 현주건조물방화치사와 존속살해는 상상적 경합 |
| 208 | approve | post_outcome | nonstatus_liability / not_applicable | complicity | - | 비신분자는 어느 견해에 의하든 보통살인죄로 처벌 |
| 240 | approve | post_outcome | nonstatus_liability / not_applicable | complicity | - | 결정 C 선택. 존속살해 공동정범이나 제33조 단서로 보통살인 처벌 |
| 241 | approve | post_outcome | nonstatus_liability / not_applicable | complicity | - | 결정 C 선택. 신분자는 존속살해 교사·방조, 비신분자는 보통살인 정범 |
| 209 | rewrite | post_outcome | nonstatus_liability / not_applicable | complicity | - | 메타 래퍼 제거. 실자와 함께 남편을 살해한 처는 존속살해 공동정범 |

#237은 어제 방화 unit의 전문가 재정과 짝을 이룬다. 방화 쪽에서 `..._imaginary_concurrence`를
선택했고(대법원 1996. 4. 26. 선고 96도485), 여기서 살인 쪽 진술이 같은 결론을 담는다.
두 unit의 경계가 일치한다.

## 초안 — 예비·음모 (제255조, 19장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 214 | approve | component | preparation_conduct / alternative_any | preparation | 실행 착수에 이르지 않은 일체의 준비행위 |
| 215 | approve | component | preparation_conduct / alternative_any | preparation | 의사·계획을 넘어 실행을 가능·용이하게 하는 준비행위 |
| 216 | rewrite | component | preparation_conduct / alternative_any | preparation | 메타 래퍼 제거. 물적인 것에 한정되지 않으나 실질적 기여를 요함 |
| 213 | rewrite | component | preparation_conduct / alternative_any | preparation | 메타 래퍼 제거. 살인을 위해 사람을 고용하고 대가를 약속한 경우 |
| 219 | approve | component | conspiracy_agreement / mandatory_all | preparation | 음모는 2인 이상 사이의 범죄실행 합의 |
| 218 | approve | bar | conspiracy_agreement / not_applicable | preparation | 합의에 이르지 않은 의사 표명·교환만으로는 음모가 아니다 |
| 221 | approve | component | murder_purpose / alternative_any | preparation | 살인죄·존속살해죄·위계위력살인죄를 범할 목적 |
| 220 | approve | component | murder_purpose / alternative_any | preparation | 사태 발생과 연관된 조건부 목적도 목적이 된다 |
| 223 | approve | component | preparation_intent / mandatory_all | preparation | 목적 외에 살인의 준비에 관한 고의가 필요 |
| 224 | approve | component | target_specificity / mandatory_all | preparation | 시기가 미정이어도 살해 대상자는 구체적으로 확정되어야 함 |
| 225 | rewrite | bar | target_specificity / not_applicable | preparation | 메타 래퍼 제거. 살해대상이 결정되지 않으면 예비죄가 아니다 |
| 222 | approve | bar | preparation_conduct / not_applicable | preparation | 인터넷 살인예고 게시만으로는 예비·음모가 아니다 |
| 217 | approve | bar | preparation_conduct / not_applicable | preparation | 낫을 들고 접근하면 착수에 이르러 예비가 아니라 미수 |
| 228 | approve | post_outcome | concurrence / not_applicable | preparation | 미수·기수에 이르면 예비·음모는 흡수된다 |
| 229 | approve | post_outcome | offense_count / not_applicable | preparation | 하나의 살인을 위한 여러 예비행위는 하나의 예비죄 |
| 227 | rewrite | component | preparation_complicity / mandatory_all | complicity | 메타 래퍼 제거. 예비행위를 공동으로 하면 예비죄의 공동정범 |
| 226 | rewrite | bar | preparation_complicity / not_applicable | complicity | 메타 래퍼 제거. 예비죄에 대한 종범은 성립하지 않는다 |
| 242 | rewrite | post_outcome | preparation_desistance_mitigation / not_applicable | preparation | 결정 C #20의 기존 선택을 계승해 긍정설 규칙으로 언래핑. 성립 배제가 아니라 감면 문제 |

#217은 `attempt`와 `preparation`의 경계다. 착수가 인정되면 예비가 아니라 미수이므로
preparation track을 저지한다. 제안 03의 #15(흉기를 들고 접근하면 착수)와 같은 사실관계를
반대편에서 진술한 카드이고, 두 track이 서로를 배제하는 관계가 이렇게 표현된다.

### #242의 기존 결정 C 복원

remediated 카드는 "부정설과 긍정설의 대립이 있다"는 메타문장으로 뭉개졌지만, 권위 있는
결정 C 문서는 선택지 (2)를 "예비·음모 단계에서도 자발적으로 실행 착수를 포기한 경우
중지미수의 혜택을 부여할 수 있다"는 긍정설로 제시하고 사용자가 이를 선택했다. 따라서
재질문하지 않고 그 문장으로 언래핑한다. 다만 이는 예비·음모죄의 성립을 없애는 규칙이
아니라 감면에 관한 규칙이므로 `bar`가 아니라 `post_outcome`으로 보존한다.

## Human decision H-H07

1. 위 43장 초안을 일괄 승인하는가?
2. 직계존속을 `ancestral_relation`(정의·차단) / `ancestral_relation_basis`(인정 경로) /
   `ancestral_relation_timing`(시점)으로 나누는 데 동의하는가?
3. #207(신분 불인식)을 `bar`로 두어 존속살해 track만 저지하고 보통살인은 그대로 성립하게
   하는 구조에 동의하는가?
4. #242를 기존 결정 C의 긍정설 선택에 따라 감면 `post_outcome` 규칙으로 복원하는 데
   동의하는가?
