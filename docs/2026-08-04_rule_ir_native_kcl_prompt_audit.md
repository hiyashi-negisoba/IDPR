# RuleIR-native KCL E2E 사전 프롬프트 감사

- 상태: **pass**
- 모델/API 호출: 0
- 대상 문항: `kcl_criminal_r14_p1_q2`, `kcl_criminal_r12_p1_q2`

## 프롬프트 고정값

| stage | system SHA-256 | user SHA-256 | 계약 문구 |
|---|---|---|---|
| `fact_extract` | `e5bc96e1dba3071421ca933825377811b2ff93a69f90a1d4cd329bfc084d59ad` | `41a2a3481a3b7df474032e22fb8003f0da86212570fbed8f3e2c937f90b269fe` | pass |
| `issue_select` | `d1eb7136a6a2ceb9a07e8a6e4e5ca835413c81b585ee1cf6f031bb5ee574e797` | `c1aff928ddba42c5fe7b6327f2525214445bda94c6326180da8327eedbfa49fb` | pass |
| `predicate_assess` | `01b688fc4f258461e07f2ee3251926059311c1fb6745aca09424e30febfa7c25` | `95521d613973fc509e421c34ea0239a3494eaaebe60bc7bd1531bc8ac02b81c2` | pass |
| `hybrid_generate` | `1809cbebdc41d933c99004a43c362098aa6ce5c22f89a9d2a41c882820a26bee` | `4bcaee37a132f7675c7792d1732087fa02607b2a893df13a4dba223278bce371` | pass |

## 확인된 불변식

- 모델 입력은 `sub_question_id`, `question_text`, `question_prompt`에서만 유도한다.
- FactGraph의 `issue_candidates`와 `retrieval_queries`는 schema에서 빈 배열로 고정한다.
- 죄종 선택 enum은 등록 RuleIR 36개와 `unsupported` 하나뿐이다.
- 선택된 unit의 predicate는 schema의 required field로 전량 강제한다.
- 지원 각칙의 결론 필드는 생성 모델 schema에 주지 않는다.
- 미지원 총칙은 `model_only_general_part_experiment`로 명시하며 symbolic으로 부르지 않는다.
- 절차법·증거법·수사·공판·상소 쟁점은 이번 실험 답안에서 제외한다.

## 남은 실험상 위험

- Unsupported general-part sections use model-only legal knowledge and are not symbolic.
- FactGraph vocabulary may omit legally material mental-state detail; omissions must remain unknown.
- The audit proves prompt/data contracts, not model compliance or answer correctness.
