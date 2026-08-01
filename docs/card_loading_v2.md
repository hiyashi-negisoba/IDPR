# 카드 적재 v2 — 쟁점 중심 계층

## 결론

일반법리는 이미 RuleIR 카드에 있었다. 문제는 slot 단위 역할 상속 때문에 일반법리와
판례상 세부기준·구체 사안이 모두 독립적인 `core` 질문으로 적재된 것이었다. 원본 카드를
다시 쓰지 않고 런타임 적재 단위를 다음처럼 바꾼다.

```text
L0 후보 조문
  └─ 법적 쟁점(issue)
       ├─ anchor: 기존 카드 중 일반법리 1~4장, 항상 문맥으로 적재
       └─ detail: 세부기준·판례 사안, 첫 판정이 unknown일 때 최대 2장 검색
```

모델은 카드별 status가 아니라 쟁점별 status 하나만 출력한다. anchor와 detail은 별도
질문이 아니며, detail의 사실 전제가 사건과 맞을 때만 일반법리를 구체화한다.

## 전수 적재 계약

- 전체 원본 카드 1,848장은 정확히 한 issue에 배치한다. 누락과 중복을 모두 오류로 본다.
- 판례 사안형 카드 629장은 anchor가 될 수 없다.
- L0의 조문 합집합과 미수 조문 확장은 그대로 유지한다.
- 기존 `candidate_articles()`는 Phase 2 재현용이고, Phase 3는
  `candidate_issues()`를 사용한다.
- 첫 호출은 `assess_issue`만 판정한다. `guard`, `stage`, `concurrence`,
  `participation`, `support`는 각 런타임 경로에 보존한다.
- 첫 판정이 `unknown`인 issue에만 `retrieve_issue_cards()`를 실행한다. 검색 후보는 그
  issue의 `retrieval_card_ids`로 제한되어 다른 죄나 다른 요소의 카드가 섞일 수 없다.
- 검색 쿼리는 구체적 `missing_facts`와 가장 가까운 허용 사실을 결합한다. 긴 사건의 모든
  에피소드가 각기 무관 판례를 끌어오는 것을 막는다.

## 현재 전수 결과

생성 자산은 `data/rulebase/issue_catalog_v2.json`이다. 현재 51개 조문의 1,848장을
372개 issue로 구조화했고, 첫 호출의 기본 평가 issue는 159개다. 334개 일반법리 카드가
anchor이고, 1,246장은 필요 시 검색 후보, 214장은 symbolic 조건, 54장은 설명용이다.

남은 review flag 19개는 일반화할 비판례 anchor가 없는 deferred issue다. 기본 평가
issue에는 review flag가 없다. 이들은 판례 사안을 보편 법리로 승격하지 않고 조회 전용으로
남겨 둔 보수적 결과다.

## 스모크에서 달라진 점

기존 4조문 스모크는 193개 카드 status를 요구했다. v2 첫 호출은 같은 범위를 14개 쟁점,
24개 anchor로 표현하며 84개 세부카드는 처음부터 싣지 않는다. 첫 호출에서 unknown이 된
주거침입 쟁점에만 공동현관·출입통제·사실상 평온 기준을 쟁점당 최대 2장 붙여 재판정한다.

## 심볼릭 연결

issue status를 기존 카드 단위 Scallop gate에 끼워 맞추지 않는다. 런타임은
`issue_status(case, issue, status)`를 별도 사실로 적재하고, `issue_offense`와
`issue_function`으로 요소 지지·반증 및 조각 사유에 연결한다. anchor와 detail 카드에는
부모 issue의 status를 복제하지 않는다.

기존 `card_status` 규칙은 Phase 1 골든과 Phase 2 재현을 위해 병존한다. 죄수 조건이
`relation_condition` issue에 속하면 `condition_issue`를 통해 그 issue 판정을 읽는다.
stage·participation의 독자적인 결론 규칙은 법리 매핑 전에는 범죄 성립 게이트에 추가하지
않는다.

## L0 검색과의 연결

판례 사안 카드는 최초 평가에서 제외하지만 검색 인덱스에서는 유용한 사건 어휘를 제공한다.
운영 검색은 모든 member card를 신호로 사용한 뒤 card→issue→article로 점수를 집계한다.
top-18 article은 recall 때문에 유지하고, 선택된 조문은 initial issue와 anchor로만
확장한다. anchor-only issue 검색과 issue top-k 직행의 전수 실측은
docs/2026-08-02_issue_normalization.md에 기록했다.
