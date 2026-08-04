# RuleIR core-normalized KCL E2E smoke — job 218989

## 실행 사실

- 코드 커밋: `0016591ee963b9ca4a298b62582e4e8bbe3b82db`
- Slurm: `218989`, `COMPLETED`, exit `0:0`, 3분 38초
- 모델 환경: 기존 `inv_ass_env`, Gemma 4 26B A4B, vLLM guidance
- 사전 감사: pass, API 호출 0, 미지원 guidance schema key 0
- 대상: `kcl_criminal_r14_p1_q2`, `kcl_criminal_r12_p1_q2`
- 두 사례 모두 역할 배정, 핵심 predicate 평가, 실제 Scallop, 최종 writer까지 완주했다.

## 확인된 개선

- 범용 FactGraph 및 카드별 3상태 질문을 새 경로에서 제거했다.
- 전체 등록 unit의 모델 경계는 카드 predicate 1,652개에서 핵심 component 245개로 줄었다.
- 실제 사례에서 뇌물공여 7개, 횡령 5개, 절도 6개만 모델이 평가했다.
- 이전 스모크의 과도한 `unknown`은 재현되지 않았다. 각 묶음은 모두 완결된 상태를 반환했다.
- NormCard와 source reference는 predicate-conditioned context로만 사용됐고 predicate 집합을 바꾸지 않았다.
- 실제 core Scallop derivation과 host-injected conclusion이 최종 writer까지 유지됐다.
- 두 번째 사례에서 절도 각칙 symbolic section과 미지원 총칙 model-only section이 표시상 분리됐다.

## 합격하지 못한 부분

### r14

- 명백한 차용금 용도 기망 사실이 있는데 `fraud` issue가 누락됐다.
- `bribe_giving`이 두 issue로 중복 선택됐지만 두 역할 배정 모두 피고인을 乙로 잡았다. 두 번째
  issue가 丙의 죄책을 겨냥했다면 issue 선택 결과가 주체를 보존하지 못한 것이다.
- 두 뇌물 issue 모두 `delivery_giver`, `delivery_recipient`, `offering` 세 track을 전부 선택하여
  동일 사실로 여섯 symbolic section이 중복 생성됐다.
- 횡령 역할 배정은 `entrustor=B`, `owner=B`로 두었다. 乙이 B로부터 소비대차로 차용한 금원을
  丙에게 전달 위탁한 구조에서 이 배정과 답안 서술은 법적으로 부정확하다.
- 따라서 `bribe_giving established`, `embezzlement established`라는 Scallop 출력은 실행
  자체는 진짜지만 잘못된 issue/role/track 입력 위의 derivation이다.

### r12

- 절도 core 6개는 모두 satisfied로 평가되어 `theft_established`가 실제로 도출됐다.
- 총칙 issue의 `reported_label`이 쟁점명이 아니라 그대로 `unsupported`였다.
- 각칙 predicate 평가는 피해자 동의에 관한 착오를 두고도 절도 고의를 satisfied로 처리했다.
- model-only 총칙 답안은 실제 동의 유무와 동의에 관한 착오의 법적 효과를 혼동한다. 각칙
  symbolic 결론과 전체 죄책 결론도 통합되지 않아 답안 내부 긴장이 남는다.
- writer의 application 문자열 안에 JSON 조각처럼 보이는 ```,`heading`...`` 문구가 끼었다.

## 일반화된 다음 교정 경계

이번 사례의 정답을 하드코딩하지 않는다. 다음 교정은 모든 사례에 적용되는 계약만 대상으로 한다.

1. issue 선택 결과에 정확한 `subject_quote`를 의무화하여 행위자별 issue를 다음 단계까지 보존한다.
2. 역할 배정은 `subject_quote`의 주체를 `defendant_id`로 강제하고, 같은 주체·unit의 중복 issue를
   명시적으로 검증한다.
3. track 선택은 해당 피고인의 행위에 적용되는 track만 허용하고, 선택 이유와 원문 근거를
   검증한다.
4. role은 단순 entity slot이 아니라 선택된 core predicate가 요구하는 법적 관계로 배정하며,
   소유·위탁·처분 같은 법적 관계에는 predicate-conditioned authority를 제공한다.
5. 미지원 총칙은 symbolic으로 위장하지 않되, 각칙 baseline과 전체 죄책의 관계를 명시하는 별도
   합성 계약이 필요하다.

이 스모크는 최소 predicate 경계와 실제 Scallop 폐회로를 입증했지만, KCL 답안 정확성 기준으로는
실패다.
