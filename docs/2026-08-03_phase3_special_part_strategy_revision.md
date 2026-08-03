# Phase 3 형법 각칙 중심 전략 개정안

## 0. 문서 지위

이 문서는 `2026-08-03_phase3_coverage_regression_recovery_plan.md`에서 확인된 Coverage
회귀를 바탕으로 목표 범위와 구현 전략을 다시 결정한다. 기존 문서의 실험 기록과 원인
분석은 유효하지만, 총칙·절차법 lane을 즉시 확장하고 V5 예외 로직을 계속 추가하는 계획은
이 문서로 대체한다.

현재 결정은 다음 한 문장으로 요약된다.

> **V2를 운영 기준선으로 두고, 목표를 형법 각칙의 article-local 구성요건 분석으로
> 축소하며, provenance와 검증 계약만 유지한 단순 파이프라인을 다시 만든다.**

여기서 목표는 엄밀한 의미의 “실체법 전체”가 아니다. 형법 총칙도 실체법에 포함되므로,
연구 범위는 **형법 각칙·개별 범죄 구성요건 분석**이라고 표현한다.

---

## 1. 전략을 바꾸는 이유

### 1.1 현재 rulebase의 실제 범위

현재 article catalog는 51개 article로 구성되어 있고 대부분 형법 각칙이다. 총칙 규정은
독립된 체계로 들어 있지 않으며, 제254조·제300조·제342조와 같은 개별 미수 처벌조항만
일부 포함되어 있다. 공동정범·교사·방조·간접정범·착오·신분·죄수관계는 특정 각칙 카드
아래에 부분적으로 존재할 뿐, 형사법 전체를 일관되게 라우팅할 수 있는 총칙 ontology가
아니다. 형사절차·증거법도 독립된 rulebase가 없다.

이 상태에서 형사법 전체 Coverage를 host logic으로 복구하려 하면 다음 예외가 계속 생긴다.

- 미수 처벌조항을 독립 죄명으로 볼지 기본범 support로 볼지
- 결과적 가중범과 기본범의 기수·미수 관계를 어떻게 연결할지
- 공동정범·교사·방조·간접정범을 어느 각칙 section에 붙일지
- 흡수·상상적 경합·실체적 경합을 어떤 article 사이에서 계산할지
- 절차법 문항을 각칙 중심 FactGraph와 카드로 어떻게 표현할지

이는 구현 세부 오류가 아니라 목표 범위와 지식 기반이 맞지 않는 구조적 문제다.

### 1.2 V2·V3·V4의 실제 계보

버전 번호는 일관된 semantic version이 아니었다.

- `phase3_answer_visibility_e2e_v2`, 코드 `4d48b2e`
  - KCL smoke에서 5개 section, 3,341자 답안
  - 제298조·제297조·제301조 등 핵심 각칙 후보가 답안까지 생존
- `phase3_final_design_e2e_v2`
  - retrieval 모델 인증 오류로 L0 전에 실패한 실행 폴더
- `phase3_final_design_e2e_v3`
  - 위 실패의 재시도
  - KCL 한 문항 생성 후 취소
  - KCL 답안은 658자, 제257조·제297조 두 section
- `phase3_final_design_e2e_v4`
  - V3와 동일한 L0 후보 및 사실상 동일한 KCL 답안
  - KCL 답안은 646자, 동일한 두 section

따라서 “V3 설계”가 별도로 존재했다고 보기 어렵다. 실질적으로는 좋은 Coverage를 보인
answer-visibility V2와, stage/property reasoning을 합친 final-design V3/V4 계열의 비교다.

### 1.3 FOL solver baseline과의 복잡도 비교

현재 FOL baseline은 모델이 생성한 논리식을 host가 Z3로 실행하여 결론을 계산하는 실제
solver pipeline이 아니다. Gemma에게 한 번의 호출로 FOL, Z3 예시 코드, 최종 답안을 모두
작성하게 하고 그 텍스트를 그대로 저장한다. 코드에서는 Z3 설치 여부만 기록한다.

따라서 baseline의 단순성과 IDPR의 복잡성을 직접 비교하면 안 된다. 다만 IDPR도 불완전한
법률 ontology로 죄명 발견, 총칙 연결, 최종 verdict, section visibility까지 모두
결정론적으로 통제하려 한 것은 과도했다.

IDPR이 유지해야 할 차별점은 “형사법 전체의 완전한 symbolic solver”가 아니라 다음이다.

- 검색된 법리의 provenance
- 사실 인용의 grounding
- article별 구성요건의 구조화된 판정
- 답안 누락과 결론 충돌의 검증 가능성

---

## 2. 새로운 연구 범위

### 2.1 포함 범위

다음은 주 평가 대상이다.

1. 사실관계에서 관련 개별 범죄 article을 발견하는 능력
2. 각 article의 객관적·주관적 구성요건 제시
3. 해당 article 카드에 포함된 판례 기준 제시
4. 구성요건별 사실 포섭
5. 개별 기수범의 성립·불성립·사실 부족 결론
6. 결과범 article 자체에 포함된 인과관계·예견가능성 검토
7. 독립된 범죄 section 내부의 논리적 일관성

판단 경계는 **article-locality**다. 하나의 article package 안에서 구성요건과 법리를
완결할 수 있으면 포함한다.

### 2.2 제외 범위

다음은 현재 주 성능 목표에서 제외한다.

- 미수·중지미수·불능미수
- 공동정범·교사범·방조범·간접정범
- 신분과 공범
- 사실의 착오·방법의 착오 및 공범의 착오
- 정당방위 등 위법성 조각과 책임 조각의 일반론
- 흡수·상상적 경합·실체적 경합 등 죄수관계
- 기본범과 결과적 가중범 사이의 기수·미수 관계
- 형사소송법, 수사법, 증거법, 공판절차

범위 밖 법리를 맞추기 위한 host-side 예외, article hardcoding 또는 prompt 임시 규칙을
추가하지 않는다.

### 2.3 경계 사례

- 강간 기수의 폭행·협박과 간음 요건: 포함
- 강간미수 및 중지미수: 제외
- 강제추행의 폭행·협박·추행 요건: 포함
- 피해자를 도구로 한 간접정범: 제외
- 사기죄의 기망·착오·처분행위·재산상 손해: 포함
- 사기와 횡령의 죄수관계: 제외
- 강간치상 article 자체의 상해와 인과관계: 포함 가능
- 기본범이 미수인데 강간치상이 기수인지: 제외

이 경계를 구현 중 편의에 따라 움직이지 않는다. 변경이 필요하면 먼저 문서와 평가 태그를
수정하고 새 실험 버전으로 분리한다.

---

## 3. 단순화된 목표 파이프라인

```text
전체 문제와 질문
  → broad article retrieval
  → grounded issue planner
  → 선택 article의 core element 카드 로딩
  → article별 요소 판정
  → 독립 범죄별 답안 작성
  → provenance·누락·결론 충돌 감사
```

### 3.1 Broad article retrieval

- 전체 사실관계와 최종 질문을 함께 사용한다.
- 모델 article proposal과 semantic retrieval의 합집합을 planner 입력으로 사용한다.
- retrieval pool은 넓게 유지하되 그 자체를 답안 section 목록으로 간주하지 않는다.
- 총칙 article expansion과 attempt mapping은 수행하지 않는다.
- 특정 개발 문항의 gold article을 보호하는 whitelist를 두지 않는다.

### 3.2 Grounded issue planner

planner는 question, fact quote, 검색된 article label과 짧은 core rule을 보고 실제로 논할
개별 범죄를 고른다. 각 선택에는 반드시 다음이 있어야 한다.

- closed catalog article ID
- 관련 행위자
- 원문 fact quote
- 논해야 하는 이유

planner가 고른 article은 최종 답안까지 생존한다. 이후 symbolic visibility가 다시 삭제하지
않는다. retrieval-only 후보는 planner가 선택하지 않으면 답안 후보가 아니다. 이 구조는
복잡한 `must_discuss` 출처 우선순위보다 단순하다.

### 3.3 Article-local element assessment

선택된 각 article에 대해 core element issue를 모두 제공한다.

```text
status: satisfied | not_satisfied | unknown
```

- `satisfied`: 입력 사실이 해당 요소를 적극 지지
- `not_satisfied`: 입력 사실이 요소와 명시적으로 충돌
- `unknown`: 필요한 사실이 기록에 없음

판정마다 fact quote 또는 fact ID와 rule card ID를 결박한다. 총칙 관계나 다른 article의
성립 여부를 요소 판정에 끌어오지 않는다.

### 3.4 Answer generation

- planner가 선택한 article 수와 section 수를 동일하게 유지한다.
- 각 section은 해당 article의 요소 판정만 사용한다.
- 요소가 충족되면 성립, 반대 사실이면 불성립, 사실 부족이면 판단 제한을 쓴다.
- 전체 결론은 독립 범죄별 결론을 나열한다.
- 죄수관계는 작성하지 않는다.
- 제공되지 않은 총칙·절차법을 모델의 일반지식으로 보완하지 않는다.

### 3.5 Host validation과 Scallop의 역할

host가 반드시 검증할 것은 다음뿐이다.

- 선택된 article이 전부 답안에 존재하는가
- 인용한 fact/rule ID가 실제 입력에 존재하는가
- 판정과 section 결론이 충돌하지 않는가
- section별 결론과 overall conclusion이 충돌하지 않는가
- 모델이 새로운 article, 판례번호, 사실을 추가하지 않았는가

Scallop은 필요하면 다음과 같은 좁은 consistency checker로만 사용한다.

- `satisfied` 요소 집합과 성립 결론의 형식적 정합성
- `not_satisfied` 핵심 요소와 성립 결론의 충돌
- 동일 article의 상반된 결론

Scallop이 issue spotting, 미수 연결, 공범 관계, 죄수관계, section visibility를 결정하지
않는다. 단순 host validator로 충분하면 Scallop을 실행 경로에서 제거할 수도 있다.

---

## 4. V2와 V5에서 가져올 것

### 4.1 V2에서 유지

- 넓은 retrieval과 모델 proposal의 합집합
- article core element를 충분히 전달하는 방식
- 불확정 후보도 성급하게 삭제하지 않는 답안 가시성
- 긴 형식의 article별 법리·포섭 서술

### 4.2 이후 버전에서 선별 이식

- 원문·artifact hash와 manifest
- fact/rule provenance
- typed `unknown_reason`
- 구조화 출력과 schema validation
- candidate/section lifecycle audit
- host-controlled conclusion consistency

### 4.3 이식하지 않을 것

- `must_discuss` 출처별 다단계 예외
- 미수 처벌 article의 자동 expansion
- 기본범 gap에 따른 결과적 가중범 visibility 예외
- stage/property/general-part relation을 모두 묶은 symbolic verdict
- smoke article ID를 직접 검사하는 최종 성능 gate
- 총칙·절차법 Coverage를 host logic으로 보충하는 규칙

V5 job은 진단과 lifecycle 검증 실험으로 보존하며 생산 후보로 자동 승격하지 않는다.

### 4.4 V5 job 218672의 최종 진단

job `218672`는 두 smoke 답안 생성을 완료했다. Slurm 상태가 failed인 직접 원인은 마지막
manifest verifier가 계산 노드에서 `git`을 다시 호출한 환경 오류다. 생성 산출물 자체는
완전하며 읽기 전용 재검증 결과는 다음과 같다.

- lifecycle audit: passed
- `must_discuss` 생존율: 6/6, 100%
- relevance/verdict/conclusion 구조 정합성: passed
- KCL 핵심 issue family retrieval: failed
- KCL 핵심 issue family Call 3 도달: failed
- 사용자 사기 smoke의 제347조 Call 3 도달: passed

KCL 답안에는 제257조, 제334조, 제335조, 제337조, 제319조, 제259조, 제297조가 나타났지만
핵심 제298조 강제추행과 제301조 강간등 상해·치상은 L0에서부터 없었다. 특수강도·준강도·
강도상해가 model-selected `must_discuss`로 살아남아 오히려 관련성이 낮은 section을 늘렸다.
답안 내부의 표면적 결론 충돌은 없었으나, 핵심 rubric Coverage는 회복되지 않았다.

사용자 사기 smoke는 제347조 사기의 구성요건과 포섭을 충실히 작성하고 성립 결론도
일관되게 유지했다. 반면 제355조 횡령 검토와 죄수관계는 빠졌고, 일부 문장에서 “丙의
기망으로 甲이 교부”해야 할 주체 관계가 “甲의 기망에 의해 丙이 교부받음”으로 뒤집혔다.

이 결과는 후보 출처별 visibility 예외를 추가하는 방식이 Coverage를 안정적으로 해결하지
못한다는 근거다. V5에 추가 예외를 더하지 않고 article-local 단순 전략으로 전환한다.

---

## 5. 평가 전략

### 5.1 원본 루브릭을 결과에 맞게 수정하지 않는다

생성 결과를 본 뒤 루브릭을 삭제하거나 문구를 바꾸지 않는다. 대신 실험 실행 전에 원본
루브릭 항목을 다음과 같이 범위 태깅한다.

```text
in_scope_special_part
out_of_scope_general_part
out_of_scope_procedure
ambiguous_scope
```

태깅 기준과 결과는 별도 파일로 봉인하고 모든 baseline에 동일하게 적용한다. 이 태깅은
정답을 생성 모델에 제공하기 위한 것이 아니라 연구 주장의 분모를 명시하기 위한 것이다.

### 5.2 주 지표

우선순위는 다음과 같다.

1. in-scope Coverage
2. in-scope logical consistency
3. in-scope Precision

Gemini 2.5 Flash의 hallucination 점수는 주 acceptance gate로 사용하지 않는다. 대신 존재하지
않는 판례·조문·fact/rule ID는 deterministic validation으로 차단하고 별도 incident count로
보고한다.

### 5.3 함께 보고할 보조 지표

- 원본 전체 루브릭 Coverage
- 총 루브릭 중 in-scope 비율
- 범위 밖 루브릭을 포함했을 때의 이론적 Coverage ceiling
- 문항별 선택 article 수
- 선택 article의 최종 section 생존율
- section 내부 및 overall conclusion 충돌 수

전체 원본 Coverage가 낮더라도 범위 제한 때문에 생긴 부분과 in-scope 실패를 분리해서
보고한다.

### 5.4 개발세트

현재 KCL smoke는 간접정범·중지미수·결과적 가중범·죄수관계 비중이 높아 새 목표의 단일
acceptance case로 부적절하다. 이 문항은 역사적 회귀 진단용으로만 보존한다.

새 개발세트는 결과를 보기 전에 8~12문항으로 고정한다.

- 단순 개인적 법익범
- 재산범죄
- 공공적 법익범
- 결과범과 인과관계
- 복수의 독립 각칙 범죄가 있는 사례
- 성립하지 않는 각칙 후보를 명시적으로 배척해야 하는 사례

총칙·절차법이 주된 문항은 개발 acceptance에서 제외하되 전체 원본 평가에는 남겨 둔다.

---

## 6. 실행 계획

### P0 — 현재 실행 보존과 기준선 확정

1. V2 59문항 generation job을 완료한다.
2. dependency로 연결된 V2 Gemini 평가를 완료한다.
3. Gemini 점수 외에 답안 길이, section 수, lifecycle, 원본 Coverage를 보존한다.
4. V5 2문항 job은 진단 산출물로만 보존한다.
5. V2와 V4/V5 산출물을 덮어쓰지 않는다.

### P1 — 범위 봉인

1. 각칙/총칙/절차법 rubric tagging 지침을 작성한다.
2. 59문항 루브릭을 태깅하고 파일 hash를 봉인한다.
3. 각칙 중심 개발 8~12문항을 고정한다.
4. 평가 주 지표와 보조 지표를 manifest에 명시한다.

### P2 — 단순 프로토타입

1. V2 기준 코드에서 별도 branch/worktree를 만든다.
2. broad retrieval 산출물은 유지한다.
3. grounded issue planner를 하나의 명시적 stage로 만든다.
4. planner-selected article을 Call 3까지 그대로 유지한다.
5. article-local element assessment만 실행한다.
6. 총칙 expansion과 cross-offense symbolic relation을 제거한다.
7. provenance와 consistency validator를 이식한다.

### P3 — 개발 평가

1. 고정 개발세트에서 V2와 단순 프로토타입을 비교한다.
2. 문항별 article plan을 먼저 감사한다.
3. in-scope Coverage와 consistency를 측정한다.
4. 개별 smoke article이 아니라 집계 지표로 통과 여부를 결정한다.
5. 통과하지 못하면 prompt나 retrieval을 한 축씩만 변경한다.

### P4 — 최종 실행

다음 조건을 만족한 뒤에만 전체 실행을 제출한다.

- 개발세트 planner-selected article 생존율 100%
- 구조·provenance 위반 0
- 명백한 section/overall conclusion 충돌 0
- V2 대비 in-scope Coverage 비열화 없음
- 문항별 불필요 section 수가 사전 상한 이내
- 실행 코드, 모델, 환경, 입력 및 rubric-scope tag hash 고정

---

## 7. 중단 기준

다음 상황에서는 예외를 추가하지 않고 설계 단계로 되돌아간다.

- 특정 문항의 특정 article을 살리기 위한 코드 분기 필요
- 총칙 article을 각칙 section으로 넣기 위한 새로운 special case 필요
- retrieval 후보와 답안 후보의 차이를 설명하기 위해 출처별 visibility 예외가 증가
- 하나의 수정이 다른 범죄군의 후보 수 또는 결론을 크게 변경
- Scallop relation이 실제 답안의 법적 결론보다 pipeline bookkeeping에 더 많이 사용

---

## 8. 논문 및 보고 문구

현재 범위에서 피해야 할 표현:

- 한국 형사법 전체를 포괄하는 symbolic solver
- 실체법 및 절차법 전 영역 Coverage
- 총칙·각칙을 통합한 완전한 죄책 판정

권장 표현:

> 본 시스템은 한국 형법 각칙의 개별 범죄 구성요건 분석을 대상으로, 검색된 규범 카드와
> 사건 사실을 provenance ID로 결박하여 article별 법리 제시, 사실 포섭 및 성립 여부를
> 생성하고 그 누락과 논리적 충돌을 검증한다. 형법 총칙의 횡단 법리와 형사절차법은 현재
> 주 평가 범위에서 제외하며, 원본 전체 루브릭 성능과 범위 조건부 성능을 함께 보고한다.

FOL baseline도 실제 host-side Z3 execution이 없는 현재 구현을 그대로 사용할 경우
`FOL-style prompted reasoning`으로 기술한다. 실제 solver baseline으로 주장하려면 생성된
논리 프로그램의 파싱·실행·결론 결박을 별도로 구현해야 한다.

---

## 최종 결정

1. V2는 폐기하지 않고 현재 운영 기준선으로 사용한다.
2. V5 예외 패치는 더 확장하지 않는다.
3. 총칙·절차법 Coverage를 현재 파이프라인에서 억지로 복구하지 않는다.
4. 목표를 article-local 형법 각칙 분석으로 축소한다.
5. 다음 구현은 V2의 단순한 흐름에 provenance와 consistency validation만 이식한다.
6. 성능 판단은 단일 smoke가 아니라 사전에 고정한 각칙 중심 개발세트에서 수행한다.
7. 원본 전체 루브릭과 범위 조건부 루브릭 결과를 모두 투명하게 보고한다.
