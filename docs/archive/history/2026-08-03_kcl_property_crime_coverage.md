# KCL 59문항에서 재산죄만으로 어디까지 가는가

산출: `scripts/report_kcl_property_crime_share.py`
결과: `experiments/results/phase3_kcl_property_share/final_59.json`

분류 근거는 KCL parquet의 `rubrics` 컬럼에서 뽑은 gold 죄명이다. 이 저장소의 issue_tags나
검색 결과가 아니라 벤치마크가 요구하는 죄명이며, 죄명→조문 표는 2026-07-31 법률 검수를 마친
`data/eval/rubric_crime_article_map.json`이다. 조문→장 구분은
`data/eval/criminal_code_property_chapters.json`에 데이터로 두었다.

## 1. 가장 큰 사실: 절반은 각칙 죄명 자체가 없다

| 구분 | 문항 | 비고 |
|---|---:|---|
| gold 죄명 없음 | **30** | 루브릭이 죄명을 하나도 지목하지 않음 |
| 재산죄만 | 8 | |
| 재산죄 + 비재산죄 혼합 | 8 | |
| 비재산죄만 | 13 | |
| 합계 | 59 | |

59문항 중 **30문항은 각칙 rule base가 재산죄든 비재산죄든 애초에 답을 만들지 못한다.** 이들은
코퍼스 밖 죄명이 있는 것도 아니고(`out_of_corpus_crimes` 전부 비어 있음) 죄명 자체가 없다.
따라서 어떤 형법각칙 RuleIR로도 도달 가능한 상한은 **29/59**다.

채점 가능한 29문항만 놓고 보면 재산죄만 27.6%, 혼합 27.6%, 비재산죄만 44.8%다.

## 2. 재산죄만 완성하면 8/59

재산죄 11개 unit은 이미 RuleIR과 compiled SCL이 있다. 그 자산만으로 gold 조문을 100% 덮는
문항은 **8개**다. 혼합 8문항은 부분적으로만 닿고, 나머지 43문항은 닿지 않는다.

## 3. 방화는 평가 기여가 0이다

`art164`는 59문항 중 **딱 한 문항**(`kcl_criminal_r14_p1_q1`)에만 등장한다. 그리고 그 문항은
살인·주거침입·상해도 함께 요구하므로, **방화 unit을 아무리 완성해도 단독으로는 새로 커버되는
문항이 0개다.**

오늘 방화 47장을 검수해 승인 원장까지 만든 작업은 계약과 파이프라인을 검증한 값어치는 있지만,
평가 점수에는 기여하지 않는다. 이건 작업이 잘못됐다는 뜻이 아니라, 파일럿을 커버리지 기준이
아니라 구조 기준으로 골랐기 때문에 생긴 결과다.

## 4. 비재산 unit을 추가할 때의 실제 이득

기여 큰 순서로 넣었을 때 완전히 커버되는 문항 수다. 시작점은 재산죄만의 8문항이다.

| 추가 unit | 카드 | 누적 커버 |
|---|---:|---:|
| intentional_bodily_injury (257·258-2·259·263) | 100 | 11/59 |
| homicide (250·254·255) | 229 | 14/59 |
| obstruction_of_official_duty (136) | 54 | 16/59 |
| dwelling_intrusion (319) | 102 | 18/59 |
| harboring_offender (151) | 58 | 19/59 |
| quasi_sexual_offense (299) | 25 | 20/59 |
| **arson_of_occupied_structure (164)** | **47** | **21/59** |
| private_document_forgery (231) | 44 | 22/59 |
| use_of_forged_private_document (234) | 22 | 23/59 |
| bribe_receipt + bribe_giving (129·133) | 81 | 25/59 |
| dereliction_of_duty (122) | 49 | 26/59 |
| 문서·인장·위증·공무상비밀 나머지 6개 | 231 | 29/59 |

상위 5개 unit(543장)을 넣으면 8 → 19문항으로 두 배 이상이 된다. 18개 비재산 unit을 전부
완성해도 상한은 29문항이다.

단일 unit만으로 문항이 완성되는 경우는 다음과 같다. 이들이 투자 대비 효율이 가장 높다.

- `intentional_bodily_injury` 단독으로 완성: 3문항
- `homicide` 단독으로 완성: 3문항
- `harboring_offender`, `dwelling_intrusion`, `obstruction_of_official_duty`,
  `quasi_sexual_offense`, `private_document_forgery` 각 1문항

## 5. 판단에 필요한 정리

- 재산죄만으로 논문을 쓰면 커버리지 주장은 **8/59**이고, 채점 가능 29문항 기준 27.6%다.
- 여기서 커버리지를 늘리는 가장 싼 경로는 방화가 아니라 **상해 → 살인 → 공무집행방해 →
  주거침입 → 범인은닉**이다.
- 30문항은 어떤 각칙 확장으로도 닿지 않으므로, 커버리지 지표를 59 분모로 보고하면 영원히
  절반을 넘지 못한다. 분모를 29(채점 가능 문항)로 잡을지 59로 잡을지는 논문 서술의 문제이며
  숨기지 말고 명시해야 한다.
