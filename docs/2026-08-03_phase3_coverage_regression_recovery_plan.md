# Phase 3 Coverage 회귀 진단 및 복구 계획

> **전략 개정 안내 (2026-08-03):** 이 문서의 회귀 진단과 실행 기록은 보존하되,
> P2 이후의 총칙·절차법 확장 전략은 더 이상 현재 결정이 아니다. 최신 범위와 구현 전략은
> `2026-08-03_phase3_special_part_strategy_revision.md`를 따른다.

## 문서 목적

이 문서는 기존 `2026-08-03_phase3_final_handover.md`를 수정하거나 대체하지 않는다.
동일 날짜에 추가로 확인된 **IDPR 최종 59문항 Coverage 회귀**를 기록하고, 검색·카드 전달·
심볼릭 판정·답안 가시성 및 평가기의 개선 방향을 별도 버전으로 고정한다.

핵심 결론은 다음과 같다.

1. GPT-5.6으로 별도 채점한 개발 스모크 답안과 최종 59문항 답안은 같은 Gemma 백본을
   사용했지만, **동일한 생성 파이프라인 버전의 출력이 아니다.**
2. 별도 채점된 답안은 `phase3_answer_visibility_e2e_v2`, 코드 `4d48b2e`의 출력과
   글자 단위로 일치한다.
3. 최종 59문항은 이후의 `phase3_final_design_e2e_v4`, 코드 `2c7a317` 계열을 사용했다.
4. 동일 KCL 스모크에서 v2의 가시 법률 section 5개가 v4에서는 2개로 줄었다. 따라서
   스모크 성능과 최종 59문항 성능의 차이는 judge 변경만으로 설명할 수 없으며, 생성
   파이프라인의 Coverage 회귀가 실제로 존재한다.
5. 검색 자체의 recall 저하도 일부 있지만, 더 구조적인 문제는 **후보의 작은 변동이나
   `unknown` 판정이 최종 답안의 완전한 쟁점 삭제로 증폭되는 구조**다.

---

## 1. 확인된 버전 불일치

### 1.1 GPT-5.6이 채점한 개발 스모크

대상 문항은 `kcl_criminal_r10_p1_q1_ga`이다. 사용자가 별도로 GPT-5.6에 전달한 답안은
아래 산출물과 정확히 일치한다.

- 산출물: `experiments/results/phase3_answer_visibility_e2e_v2/idpr_nsn_outputs.jsonl`
- 테스트 코드: `4d48b2e289f0e27c1212ef18af1bf5bbb12b9a03`
- 답안 길이: 3,341자
- 가시 법률 section: 5개
  - 제298조 강제추행
  - 제297조 강간
  - 제257조 상해·존속상해
  - 제319조 주거침입·퇴거불응
  - 제301조 강간등 상해·치상

### 1.2 최종 파이프라인의 동일 스모크

최종 설계 v4에서 동일 문항을 다시 생성한 산출물은 다음과 같다.

- 산출물: `experiments/results/phase3_final_design_e2e_v4/idpr_nsn_outputs.jsonl`
- 테스트 코드: `2c7a317a430c4a4669ad1755fafe19f4f3f97488`
- 답안 길이: 645자
- 가시 법률 section: 2개
  - 제257조 상해·존속상해
  - 제297조 강간

v4에서는 스모크의 핵심 개선점이었던 제298조 강제추행 간접정범과 제301조 강간치상이
답안에서 사라졌다. 기존 handover에도 v2의 가시 section 5개가 최종 설계에서 2개로
감소했다고 기록되어 있으나, 당시 E2E 통과 조건은 루브릭 Coverage가 아니라 구조·배선·
계약 정합성이었다.

### 1.3 검색 후보의 실제 변화

두 실행의 모델 article selection은 동일했다. 차이는 L0 retrieval 합집합에서 발생했다.

| 버전 | 핵심 retrieval 후보 | 결과 |
|---|---|---|
| v2 | `art298`, `art319`, `art297`, `art301` 포함 | 강제추행·강간·주거침입·강간치상 논증 노출 |
| v4 | `art319`, `art297`은 남았으나 `art298`, `art301` 탈락; `art263`, `art268` 유입 | 핵심 쟁점 두 개가 Call 2 이전에 소실 |

FactGraph가 생성한 검색어가 v2의 4개에서 v4의 3개로 조금 달라진 것만으로 top-k 후보가
바뀌었다. 이는 현재 검색 경로가 질문의 핵심 쟁점을 안정적으로 보호하지 못하고 있음을
보여준다.

---

## 2. 최종 59문항 Coverage가 낮아진 직접 원인

### 2.1 judge의 엄격성만으로 설명되지 않는다

현재 완료된 실체법 IDPR 23문항에는 총 614개 루브릭 항목이 있다.

| 판정 상태 | 항목 수 | 비율 |
|---|---:|---:|
| `met` | 75 | 12.2% |
| 관련 구절은 있으나 `not_met` | 62 | 10.1% |
| 대응 내용 자체가 없는 `not_met` | 477 | 77.7% |

관련 구절이 있는 62개를 전부 부분 충족 0.5점으로 인정해도 micro Coverage 상한은 약
17.3%다. Gemini의 raw macro Coverage는 약 10.8%, 인용 safeguard 적용 후 점수는 약
8.5%로, safeguard가 설명하는 차이는 약 2.3%p뿐이다.

따라서 judge 교체는 일부 판정을 개선할 수 있지만, 현재 Coverage 저하의 주원인은 답안에
루브릭 내용이 실제로 존재하지 않는 것이다.

### 2.2 후보가 답안까지 살아남지 못한다

실체법 24문항의 Call 3 요청을 집계하면 다음과 같다.

- 문항당 평균 `required_sections`: 2.5개
- 문항당 평균 `suppressed_sections`: 8.1개
- suppression 사유
  - `no_positive_element_support`: 164개
  - `missing_required_base_offense`: 16개
  - `explicit_element_refutation_dominates`: 10개
  - `insufficient_material_grounding`: 5개

현재 `src/idpr/generation/issue_answer.py`의 visibility 정책은 긍정 근거가 없거나 물적
grounding이 부족한 후보를 최종 답안에서 숨긴다. 그러나 사례형 시험에서 “성립하지 않는
쟁점”과 “사실이 부족해 결론이 부정되는 쟁점”도 검토 대상이다. 현 구조는 다음 두 개념을
잘못 결합한다.

- 답안에서 **논해야 하는 관련성**
- 최종적으로 **성립한다고 결론낼 수 있는지**

그 결과 `not_satisfied` 또는 `unknown`이어야 할 논증이 “불성립 논증”으로 나타나는 대신
답안에서 완전히 삭제된다.

### 2.3 질문 초점보다 전체 사실관계의 신호가 우선한다

명확한 사례는 `kcl_criminal_r10_p2_q3`이다.

- 질문: 교통사고처리특례법위반(치사), 주의의무 위반과 합법적 대체행위·인과관계
- article selector: `art267`을 정확히 선택
- Call 2: 질문에 “충분한 측면 간격을 유지하지 않았다”는 사실이 있음에도 과실 여부를
  `rule_gap`으로 처리
- Scallop/visibility: `art267`을 숨기고, 같은 사실관계 블록 앞부분의 야간 주거침입 사실을
  근거로 `art330`을 노출
- 최종 답안: 교통사고가 아니라 야간주거침입절도만 검토
- Coverage: `0/15`

현재 scoping은 문제에서 참조한 번호의 사실 블록을 골라내지만, 그 블록 안에서 최종 질문이
묻는 행위·인물·법률관계를 다시 우선순위화하지 않는다. 따라서 배경 사실의 범죄가 질문의
직접 대상보다 강한 symbolic signal을 얻을 수 있다.

### 2.4 총칙·횡단 법리가 죄명 article에 종속되어 있다

현재 답안 계획의 기본 단위는 개별 범죄 article이다. 다음과 같은 횡단 쟁점은 특정 article의
카드에 우연히 포함되거나 검색되어야만 답안에 나타난다.

- 공동정범·교사범·방조범
- 신분과 공범
- 비신분자를 이용한 간접정범
- 사실의 착오·방법의 착오·교사의 착오
- 인과관계·객관적 귀속
- 미수·중지미수
- 죄수·흡수·상상적/실체적 경합
- 결과적 가중범과 기본범의 관계
- 특별법 구성요건

예를 들어 `kcl_criminal_r12_p1_q4`는 `art127`, `art152` section은 받았지만 甲의 교사,
乙의 위증교사, 대향범 및 형법 제33조 쟁점을 전달받지 못해 `8/39`에 그쳤다.
`kcl_criminal_r14_p1_q3`도 `art323`은 받았지만 비신분자를 이용한 간접정범의 학설·판례를
받지 못해 `5/20`에 그쳤다.

### 2.5 Call 3에는 복구 권한이 없다

Call 3 프롬프트는 다음을 강제한다.

- `required_sections`의 수와 순서를 그대로 유지
- 각 section의 issue 수와 순서를 그대로 유지
- 제공된 법리만 사용
- 새로운 쟁점 발굴 금지
- suppressed section은 모델 입력에서 제거

이 제약은 hallucination 방지에는 유리하지만, 상류의 단 한 번의 누락도 복구할 수 없게 한다.
현재는 검색·판정·가시성의 오류가 모두 최종 답안 누락으로 직결되는 단방향 구조다.

---

## 3. 유지할 설계와 수정할 설계

### 3.1 유지할 것

- 문제·답안·rubric의 해시 및 manifest 기록
- 답안 생성 시 rubric 비공개 원칙
- provenance ID와 원문 근거 검증
- `unknown_reason`의 typed contract
- 모델이 임의의 판례번호·조문·사실을 추가하지 못하게 하는 법리 경계
- Call 3의 구조화 출력과 heading/section 결박
- 모델 선택과 retrieval의 합집합 원칙

### 3.2 수정할 것

- fixed top-k 안에서 모든 후보가 경쟁하는 구조
- 후보 출처가 Call 2/Call 3로 가면서 사라지는 구조
- `no positive support = hidden` 규칙
- 기본범 gap이 있으면 결과적 가중범 논의 자체를 숨기는 규칙
- 질문 초점과 무관한 배경 범죄가 최종 section으로 승격되는 구조
- 총칙·횡단 법리를 개별 죄명 카드에만 종속시키는 구조
- 구조 검증만 통과하면 Coverage 회귀도 허용하는 E2E gate

---

## 4. 목표 구조

### 4.1 관련성과 결론 상태 분리

후보마다 다음 두 축을 별도로 관리한다.

```text
relevance: must_discuss | optional | irrelevant
verdict: established | not_established | unknown | attempt_review
```

`must_discuss`이면 verdict와 무관하게 답안에 노출한다. `not_established`는 불성립 논증,
`unknown`은 필요한 추가 사실과 결론 한계를 작성한다. verdict는 visibility가 아니라 결론의
강도를 결정해야 한다.

### 4.2 후보 provenance를 끝까지 보존

각 article/issue에 출처를 부여하고 Call 3까지 유지한다.

- `question_selected`: 질문 문언이 직접 요구
- `model_selected`: Call 1.5 article selector가 선택
- `fact_issue_candidate`: FactGraph가 명시적으로 제안
- `retrieval_selected`: semantic retrieval로 추가
- `general_part_selected`: 총칙 lane에서 추가
- `attempt_expansion`: 미수 처벌조항 확장

보존 우선순위는 `question_selected > model_selected/fact_issue_candidate >
general_part_selected > retrieval_selected`로 둔다. 질문 직접 후보는 retrieval top-k에 의해
퇴출되지 않아야 한다.

### 4.3 보호 슬롯형 후보 예산

하나의 top-k에서 전 후보를 경쟁시키지 않는다. 후보 예산을 lane별로 분리한다.

1. 질문 직접 선택: 전부 보호
2. 모델·FactGraph 명시 후보: 전부 또는 별도 상한 내 보호
3. 총칙·횡단 쟁점: 별도 lane
4. semantic retrieval: 남은 예산에서 보강
5. attempt/base/result expansion: 보호 후보에 종속하여 추가

단순히 전역 `top-k=18`로 복귀하는 것은 우선 해결책이 아니다. 핵심 후보 보호 없이 k만
늘리면 Call 2 토큰과 무관 쟁점이 다시 증가한다.

### 4.4 article 검색 후 issue-level 카드 선택

현재는 article 하나가 입장하면 큰 hierarchy와 다수 카드가 Call 2에 함께 들어가 모델을
압박한다. 최종 59문항의 L0는 문항당 article median 13개, initial issue median 43개,
anchor rule median 54개였다.

개선안은 다음과 같다.

1. 질문 초점으로 must-discuss article/issue 결정
2. 각 article의 core element 카드는 항상 제공
3. 질문과 직접 관련된 doctrine/detail 카드만 issue-level로 재검색
4. negative/exception 카드도 결론 가능성에 따라 함께 제공
5. 나머지 context 카드는 Call 2의 필수 판정 대상에서 제외

이 방식은 핵심 article을 삭제하지 않으면서 토큰과 판단 복잡도를 줄인다.

### 4.5 총칙·횡단 쟁점 lane 신설

FactGraph와 question prompt에서 다음 신호를 독립적으로 추출한다.

- 복수 행위자와 역할 분담 → 공동정범·교사·방조
- 신분자/비신분자 → 신분과 공범·간접정범
- 의도한 객체와 실제 객체 불일치 → 착오
- 기본범 미수 + 중한 결과 → 결과적 가중범의 기수/미수
- 복수 범죄·흡수 가능성 → 죄수관계
- 조건부 인과관계·합법적 대체행위 → 인과관계/객관적 귀속

이 lane의 결과는 개별 offense section 안의 공통 analysis 또는 별도의 총칙 analysis로
전달한다.

### 4.6 질문 초점 객체 도입

각 문항에 rubric을 보지 않고 다음 focus를 만든다.

- 질문이 요구하는 행위자
- 질문이 직접 지칭한 사실관계 번호
- 질문에서 추가·변형된 행위
- 요구된 판단 유형: 죄책, 증거능력, 절차 적법성, 인과관계 등

Call 2와 visibility는 focus와 무관한 배경 사실의 offense를 `optional` 또는 `irrelevant`로
낮춰야 한다. 반대로 focus와 직접 연결된 article은 일부 요소가 unknown이어도
`must_discuss`로 남긴다.

---

## 5. 구현 우선순위

### P0 — 회귀를 재현하고 관측 가능하게 만들기

1. v2와 v4의 동일 스모크 산출물을 영구 regression fixture로 보존한다.
2. 단계별 candidate lifecycle report를 생성한다.
   - selected source
   - retrieval rank
   - Call 2 status
   - Scallop directive
   - visibility decision
   - Call 3 포함 여부
3. `must_discuss` 후보가 어느 단계에서든 사라지면 테스트를 실패시킨다.
4. E2E gate에 section/issue family 보존 검사를 추가한다.
5. 구조 성공과 법적 Coverage 회귀 검사를 별도 결과로 기록한다.

### P1 — 최소 복구 패치

1. `l0_candidates.jsonl`의 `from_model`, `from_retrieval`, `from_attempt_expansion`을
   reasoning packet과 Call 3 request까지 전달한다.
2. 질문 직접 후보와 모델 선택 후보를 `must_discuss`로 지정한다.
3. `must_discuss`에는 `_presentation()`의 hidden 반환을 금지한다.
4. `no_positive_element_support`는 hidden 사유가 아니라 `not_established/unknown` 결론
   사유로 사용한다.
5. `missing_required_base_offense`인 결과적 가중범은 삭제하지 않고 기본범과 함께
   “선행 기본범 성립 여부 및 관계”를 검토하는 compact section으로 남긴다.
6. 질문 focus와 무관한 retrieval-only 후보만 기존 material gate로 숨긴다.

이 단계에서는 Call 3의 자유로운 쟁점 추가를 허용하지 않는다. 상류 계획의 recall을
복구하면서 기존 hallucination 방지 경계를 유지한다.

### P2 — 검색·카드 전달 재설계

1. 전역 top-k를 보호 슬롯형 candidate budget으로 변경한다.
2. article-level admission 뒤 issue-level detail retrieval을 수행한다.
3. 총칙·특별법 lane을 별도로 추가한다.
4. 질문 focus와 fact relevance를 Call 2 evidence binding에 반영한다.
5. 검색어의 작은 변화에 대한 stability test를 추가한다.
   - 동의어·문장순서 변화에도 핵심 article 생존
   - 비핵심 후보 순위 변화가 must-discuss 후보를 밀어내지 않음

### P3 — 결론 조립 개선

1. 호스트 결론은 유지하되 `relevance`와 `verdict`를 함께 사용한다.
2. section 전체를 `미확정`으로 덮기 전에 쟁점별 satisfied/not_satisfied/unknown을 반영한다.
3. attempt/result-aggravated/base-offense 관계를 하나의 일관된 결론 상태로 표현한다.
4. overall conclusion이 본문 쟁점별 소결을 기계적으로 뒤집지 않는지 검증한다.

### P4 — 평가기 재설계

생성 파이프라인 복구와 별개로 현재 judge도 다음과 같이 수정한다.

- Coverage: `full / partial / absent = 1 / 0.5 / 0`
- Precision: `gold_aligned_correct`는 비어 있지 않은 `rubric_indices`를 필수로 함
- Coverage와 Precision 판정을 별도 호출 또는 별도 검증 단계로 분리
- 동일 개발 스모크에서 기존 GPT-5.6 항목별 판정과 calibration
- 완료되지 않은 method/case 수가 다른 중간 평균은 최종 비교로 사용하지 않음

---

## 6. 하지 말아야 할 조치

- 최종 59문항의 rubric을 생성 프롬프트에 넣어 직접 맞추기
- 현재 결과를 덮어쓰거나 기존 59개 산출물을 수정하기
- Coverage를 올리기 위해 Call 3에 자유로운 법률지식 보완 권한 부여하기
- 전역 top-k만 무작정 확대하기
- 개별 holdout 문항·죄명에 대한 blacklist/whitelist 하드코딩
- 현재 Gemini 점수를 그대로 최종 성능으로 보고하기
- v2 전체 코드를 검토 없이 단순 checkout하여 이후의 provenance·contract 개선까지 제거하기

---

## 7. 검증 및 재실험 원칙

### 7.1 개발 단계

1. 기존 두 개발 스모크만으로 P0/P1을 구현한다.
2. 동일 입력을 여러 번 실행하여 must-discuss 후보 생존 여부를 확인한다.
3. v2 대비 다음을 동시에 만족해야 한다.
   - 핵심 issue family 보존
   - 무관 section 감소 또는 비증가
   - 잘못된 기수·성립 결론 감소
   - provenance/contract 위반 0
4. 답안 문자열 자체를 고정하지 않고 candidate/issue lifecycle을 회귀 조건으로 사용한다.

### 7.2 최종 59문항의 지위

현재 `experiments/results/phase3_final_59`는 삭제하거나 덮어쓰지 않는다. 이 산출물은
“v4의 question-focus 및 visibility 회귀를 발견한 진단 실행”으로 보존한다.

이미 59문항 결과와 rubric별 실패를 관찰했으므로, 이를 보고 조정한 파이프라인을 같은
59문항에서 다시 평가하면 원래 의미의 봉인 holdout은 아니다. 선택지는 다음 두 가지다.

1. 권장: 현재 59개를 진단/개발 세트로 전환하고 새로운 holdout을 봉인한다.
2. 불가피한 경우: 수정 전·후 결과를 모두 보존하고 “일반 구현 결함 수정 후 재실행”으로
   명시하되, 오염 가능성과 변경 SHA를 함께 보고한다.

### 7.3 최소 acceptance criteria

- 질문 직접/모델 선택 `must_discuss` 후보의 Call 3 생존율 100%
- hidden 후보 중 `must_discuss` 0개
- 동일 개발 스모크에서 v2의 핵심 `art298`, `art297`, `art301` issue family 보존
- 질문이 교통사고 인과관계를 묻는데 야간주거침입만 출력하는 유형의 focus inversion 0개
- required/suppressed lifecycle audit 누락 0개
- Call 3 provenance 및 schema 위반 0개
- 개발 스모크 Coverage가 v2보다 낮아지지 않으면서 hallucination/명백한 법리 오류가
  악화되지 않을 것

---

## 8. 수정 대상 파일

우선 검토 대상은 다음과 같다.

- `src/idpr/eval/input_formatter.py`
  - fact block scoping 이후 question focus 표현 추가
- `scripts/run_article_select.py`
  - question-selected 후보와 근거를 보호 provenance로 저장
- `scripts/run_l0_candidates.py`
  - 보호 슬롯형 후보 합집합과 lane별 예산
- `src/idpr/neural/issue_assessment.py`
  - focus-aware evidence binding 및 횡단 쟁점 입력
- `src/idpr/generation/issue_answer.py`
  - relevance/verdict 분리, must-discuss visibility, 결과적 가중범 보존
- `prompts/issue_assess.md`
  - 질문 직접 대상과 배경 사실 구분
- `prompts/issue_long_form_generate.md`
  - must-discuss의 negative/unknown 논증 명시
- `data/rulebase/issue_catalog_v2.json`
  - 총칙·횡단 쟁점의 독립 라우팅 검토
- `scripts/verify_phase3_final_design_e2e.py`
  - 구조 계약 외 issue-family Coverage 회귀 gate 추가

---

## 최종 결정 요약

현재 문제는 “Gemma 백본이 전체 문항에서 갑자기 약해졌다”가 아니다. v2 이후 검색어·후보
구성이 조금 달라졌고, 이후 단계가 그 작은 변화를 복구하지 못하도록 지나치게 강하게
결박되었다. 또한 `unknown/not_satisfied` 쟁점을 답안에서 논증하는 대신 삭제한 결과,
사례형 시험의 Coverage가 구조적으로 붕괴했다.

복구 목표는 v2의 모든 동작을 되돌리는 것이 아니라 다음 세 가지를 동시에 달성하는 것이다.

1. 질문이 요구하는 쟁점은 결론과 무관하게 반드시 살아남는다.
2. 검색·카드 입력은 핵심 후보를 보호하면서 issue 수준으로 압축한다.
3. 최종 작성기는 여전히 제공된 검수 법리와 사실만 사용한다.

이 경계에서 P0/P1을 먼저 구현·검증한 뒤 P2/P3로 확장한다.

---

## 9. V5 구현 기록 (2026-08-03)

V5의 평가·설계 우선순위는 **Coverage → logical consistency → Precision**으로 둔다.
Gemini 2.5 Flash의 hallucination 점수는 현재 신뢰 가능한 acceptance gate로 사용하지 않는다.
대신 생성 파이프라인의 provenance, 제공 법리 경계, 호스트 결론 계약은 그대로 유지한다.

### 9.1 구현 완료: P0/P1

- 질문 문언의 조문·완전 죄명을 결정론적으로 추출하는 `question_selected` lane 추가
- `question_selected`, `model_selected`, `fact_issue_candidate`, `retrieval_selected`,
  `attempt_expansion` provenance를 L0부터 Call 3까지 보존
- 질문 후보와 독립적으로 평가 가능한 모델·FactGraph 명시 후보를 `must_discuss`로 지정
- 미수 처벌조항처럼 자체 구성요건 없이 기본범에 붙는 후보는 `relation_support`로 보존하고
  standalone 범죄 section으로 강제하지 않음
- `must_discuss` 후보는 근거 부족·반대 사실·기본범 gap이 있어도 삭제하지 않고 compact
  negative/unknown 검토로 유지
- `relevance`와 `verdict`를 분리하고, 최종 결론은 기존 호스트 symbolic contract가 통제
- 모든 후보의 Call 2 상태, symbolic directive, verdict, visibility 및 Call 3 포함 여부를
  기록하는 `candidate_lifecycle` 추가
- 숨겨진 `must_discuss`가 하나라도 있으면 생성 및 E2E 검증 실패
- FactGraph의 grounded `after` 및 act→result 관계를 합친 복합 검색어 추가
- KCL 핵심 `art298`, `art297`, `art301`과 사용자 smoke의 `art347` 생존을 검사하는 V5
  acceptance gate 추가

단위·계약 테스트는 환경 의존성으로 수집할 수 없는 기존 `rank_bm25` 테스트 1개를 제외한
전체에서 548개가 통과했고, 최종 변경 후 관련 회귀 묶음 105개가 다시 통과했다.

### 9.2 실행 중인 검증

- 최초 V5 job `218666`은 새 lifecycle gate가 `art300`, `art342`의 relation-support와
  standalone offense를 구별하지 못한 것을 탐지하여 Call 3 전에 실패
- 보완 후 V5 2문항 Slurm E2E 재실행: job `218672`
- 출력: `experiments/results/phase3_v5_e2e_218672`
- 고정 환경: 기존 성공 잡과 같은 `inv_ass_env`, Gemma 4 26B A4B 스냅샷,
  RTX PRO 6000
- 제출 전 소스·입력 해시를 wrapper에 고정하여, 대기 중 파일 변경이나 계산 노드의
  `git` 부재가 재현성을 깨지 못하게 함
- E2E 완료 조건: 기존 schema/provenance 계약 + lifecycle audit + 핵심 issue family 생존
  + relevance/verdict/conclusion 일관성

### 9.3 다음 단계

job `218672`는 두 답안을 모두 생성했으나, 마지막 manifest verifier가 계산 노드에서
`git`을 찾지 못해 scheduler 상태는 failed로 종료되었다. 산출물을 읽기 전용으로 다시
검증한 결과 lifecycle audit과 conclusion consistency는 통과했지만, KCL 핵심
`art298`, `art301`이 L0와 Call 3에 도달하지 못하여 V5 acceptance는 실패했다. 이후 전략은
`2026-08-03_phase3_special_part_strategy_revision.md`를 따른다.
그 뒤 P2의 보호 슬롯·issue-level retrieval·총칙 lane을 한꺼번에 넣지 않고, lifecycle에서
확인된 병목 순서대로 작은 패치와 동일 2문항 gate를 반복한다. V5 전체 59문항 재생성은
이 smoke gate 통과 전에는 제출하지 않는다.
