# 살인 RuleIR 제안 06 — 죄수·양형·증거 (Ⅰ.20~Ⅰ.22, Ⅰ.5~Ⅰ.9, 59장)

59장 중 **43장이 `context_only`**다. 양형 25장과 증거 16장은 성립 결론을 바꾸지 않는다.
버리는 게 아니라 이 unit의 심볼릭 결론에 넣지 않는다는 뜻이며, 카드는 그대로 남는다.

## 초안 — 죄수 (Ⅰ.20, 16장)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 132 | approve | post_outcome | offense_count / not_applicable | base | - | 살인죄의 죄수는 피해자 수에 따라 결정된다 |
| 126 | approve | post_outcome | offense_count / not_applicable | base | - | 접착된 다수 살해는 실체적 경합 |
| 141 | approve | post_outcome | offense_count / not_applicable | base | - | 1행위 다수 살해는 상상적 경합 |
| 140 | rewrite | post_outcome | offense_count / not_applicable | base | - | 메타 래퍼 제거. 순차 총격도 피해자 수에 따라 각 살인죄 |
| 139 | rewrite | post_outcome | offense_count / not_applicable | base | - | 메타 래퍼 제거. 접착 행위라도 피해자별 살의가 있으면 경합범 |
| 137 | rewrite | post_outcome | offense_count / not_applicable | base | - | 메타 래퍼 제거. 범의 갱신 없는 예비~기수는 포괄하여 1죄 |
| 138 | approve | post_outcome | concurrence / not_applicable | base | - | 동일인에 대한 예비·미수·기수 및 상해·살인은 법조경합 |
| 128 | approve | post_outcome | concurrence / not_applicable | base | property_damage | 의복 손괴는 불가벌적 수반행위로 흡수 |
| 129 | approve | post_outcome | concurrence / not_applicable | base | corpse_abandonment | 사체를 옮겨 유기하면 사체유기죄가 별도로 성립 |
| 130 | approve | post_outcome | concurrence / not_applicable | base | - | 사체를 현장에 그대로 두고 도주하면 사체은닉죄 불성립 |
| 127 | approve | boundary | offense_scope / not_applicable | base | arson_of_occupied_structure | 살해 목적 현주건조물방화 사망은 방화치사죄로 의율 |
| 131 | approve | boundary | offense_scope / not_applicable | base | robbery | 채무 면탈 살해라도 이익 지배 이전이 없으면 살인죄만 성립 |
| 134 | approve | boundary | offense_scope / not_applicable | base | robbery | 선행 범죄 완료 후의 살해는 결합범이 아니라 실체적 경합 |
| 136 | approve | boundary | offense_scope / not_applicable | base | robbery | 은폐 목적 살해는 보복목적 살인이 아니라 강도살인 |
| 133 | context_only | context_only | - | - | - | 특정범죄가중법·성폭력처벌법 사이의 경합이며 특별법 영역 |
| 135 | context_only | context_only | - | - | - | 보복목적 판단 기준이며 특정범죄가중법 영역 |

#127은 어제 방화 unit에서 반대 방향으로 이미 판정했다. 방화 쪽 결정 C와 전문가 재정은
보통살인 목적 방화치사를 **법조경합(방화치사죄만)**으로 확정했고, 이 카드는 같은 결론을
살인 쪽에서 진술한다. 두 unit의 경계가 일치한다.

## 초안 — 양형 (Ⅰ.21, 25장)

Ⅰ.21에서 성립에 쓰이는 카드는 #142 하나뿐이다. 나머지 24장은 형의 선택·산정 문제다.

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 142 | approve | component | attempt_punishability / mandatory_all | attempt | 살인미수범 처벌. 제안 03의 #211과 같은 요건의 provenance |

| # | decision | 이유 |
|---:|---|---|
| 143 | context_only | 사체 훼손·암매장 사안의 사형 양정. 양형 |
| 144 | context_only | 어린이 2명 유인·살해 사안의 사형 양정. 양형 |
| 145 | context_only | 사형은 특별한 사정과 철저한 심리를 거쳐야 한다는 사형 선택 기준 |
| 146 | context_only | 사형 선고 시 특별한 사정을 명시해야 한다는 판시 방법 |
| 147 | context_only | 사형 심사 시 전문의견 등 깊이 있는 심리 요구. 심리 절차 |
| 148 | context_only | 죄책이 심히 중대하고 극형이 불가피할 것이라는 사형 요건 |
| 149 | context_only | 외국 무죄판결의 미결구금은 제7조 산입 대상이 아님. 형 집행 |
| 150 | context_only | 계획성·동기·피해자 관계 등을 양형에 반영하는 일반론 |
| 151 | context_only | 부정기형을 정기형으로 파기할 때의 불이익변경 기준. 형 산정 |
| 152 | context_only | 소년법 19세 미만 판단은 사실심 선고 시 기준. 형 산정 |
| 153 | context_only | 우발적 살인과 계획범행의 수괴 책임 차이. 양형 |
| 154 | context_only | 범죄수익 몰수·추징 대상. 부수처분 |
| 155 | context_only | 재범 위험성의 종합 판단과 판결시 기준. 부착명령 |
| 156 | context_only | 재범 위험성은 상당한 개연성을 의미한다는 정의. 부착명령 |
| 157 | context_only | 보통살인죄의 법정형. 이 unit은 형을 산출하지 않는다 |
| 158 | context_only | 조직적·잔혹한 다수범행 주범의 사형 양정. 양형 |
| 159 | context_only | 계획된 2명 살해 사안의 사형 양정. 양형 |
| 160 | context_only | 주도자 사형·나머지 무기징역의 형평. 양형 |
| 161 | context_only | 미필적 고의·피해자 1명 등을 고려하지 않은 사형 선택의 위법. 양형 |
| 162 | context_only | 무기징역 집행 중 재차 무기징역 선고의 의미. 양형 |
| 163 | context_only | 연속 범행의 계획성과 우발성을 나누어 심리하라는 요구. 양형 |
| 164 | context_only | 우발적·일회적 범행과 뉘우침은 사형 선택의 양형사정 |
| 165 | context_only | 치료감호의 재범 위험성만으로 부착명령 위험성을 단정 금지 |
| 233 | context_only | 결정 C 선택(사형 정당화 특별사정의 전원합의체 다수의견). 양형 기준 |

#157(법정형)만 성립과 무관하지 않아 보일 수 있으나, 이 unit은 형을 내지 않는다.
#211·#142처럼 처벌 근거를 요건으로 쓰는 경우와 달리 #157은 형량 자체다.

## 초안 — 증거와 사실인정 (Ⅰ.5~Ⅰ.9, 16장) — 전부 `context_only`

| # | 절 | decision | 이유 |
|---:|---|---|---|
| 178 | Ⅰ.5 | context_only | 간접증거만으로 유죄 인정이 가능하나 신중한 판단이 필요하다는 증명 법리 |
| 1 | Ⅰ.6 | context_only | 부검소견에 의지하려면 다른 사인을 배제하는 논증이 필요하다는 증명 법리 |
| 2 | Ⅰ.6 | context_only | 교살 혐의 사건의 심리미진 파기환송. 사실심리 |
| 179 | Ⅰ.7 | context_only | 농약 사이다 사건의 간접증거 종합. 사실인정 |
| 180 | Ⅰ.7 | context_only | 청산가리 캡슐 사안에서 다른 섭취 경로를 배제할 수 없는 경우. 증명 |
| 181 | Ⅰ.7 | context_only | 피해자 진술의 신빙성 평가. 증명력 |
| 182 | Ⅰ.8 | context_only | 사망시간 추정의 종합적 증명력. 증명력 |
| 183 | Ⅰ.8 | context_only | 직접증거와 간접증거의 종합. 증명 방법 |
| 184 | Ⅰ.8 | context_only | 보험금 수령만으로 살해 동기를 인정하지 말라는 사실인정 지침 |
| 185 | Ⅰ.8 | context_only | 금전적 동기가 수긍되기 위한 사정. 사실인정 |
| 186 | Ⅰ.8 | context_only | 동기가 미약해도 객관적 증거가 충분하면 유죄. 증명 |
| 187 | Ⅰ.8 | context_only | 과학적 증거방법의 구속력 요건. 증거법 |
| 188 | Ⅰ.8 | context_only | 제3자 열쇠 소지 시 정황증거의 증명력 감소. 증명력 |
| 189 | Ⅰ.9 | context_only | 시신이 없어도 간접증거 종합으로 유죄 인정 가능. 증명 |
| 190 | Ⅰ.9 | context_only | 시신 없고 연결 정황이 부족하면 책임 인정 곤란. 증명 |
| 191 | Ⅰ.9 | context_only | 시신 없는 살인의 유죄 인정 요소 정리. 증명 |

전부 **어떻게 증명할 것인가**이지 **무엇이 살인죄인가**가 아니다. 상해에서 상해진단서
증명력 2장(#2·#18)을 같은 이유로 `context_only`로 둔 것과 같다.

다만 규모가 다르다. 살인 주석은 증명에 16장을 쓴다. 실제 살인 사건의 쟁점이 대개
성립요건이 아니라 증명에 있다는 뜻이고, **KCL 문항도 그 비중을 따라갈 가능성이 있다.**
그 경우 이 unit의 심볼릭 결론이 답할 수 있는 범위가 좁아진다. 판단 근거로 적어 둔다.

## 초안 — 특정강력범죄법 (Ⅰ.22, 2장)

| # | decision | 이유 |
|---:|---|---|
| 166 | context_only | 누범 가중은 처단형 문제이며 특별법 영역 |
| 167 | context_only | 피의자 신상정보 공개 요건이며 성립과 무관 |

## Human decision H-H06

1. 위 59장 초안을 일괄 승인하는가?
2. 양형 24장·증거 16장·특별법 2장을 `context_only`로 두는 데 동의하는가?
3. #142(살인미수범 처벌)만 Ⅰ.21에서 건져 `attempt` track에 두는 데 동의하는가?
4. #157(보통살인죄 법정형)을 `context_only`로 두는 데 동의하는가? 이 unit은 형을 내지 않는다.
