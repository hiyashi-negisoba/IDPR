# v2 stagewise evaluation protocol

## 목적

KCL end-task 채점과 내부 단계 평가는 분리한다. KCL 점수는 최종 답안의 품질을 평가하고, stagewise 평가는 frozen artifact를 이용해 각 인터페이스가 어디까지 정보를 보존했는지 측정한다.

이 프로토콜의 offline audit은 모델을 다시 호출하지 않는다. 최종 시스템 버전을 고른 뒤 그 버전의 artifact set을 한 번 freeze하고, 같은 artifact set에 대해서만 stagewise 지표를 산출한다.

## 실행 순서

1. `frozen_B`와 fixed candidate의 KCL 결과를 비교해 최종 시스템 버전을 하나 선택한다.
2. 선택한 버전으로 26문항 artifact를 일관된 run root에 재생성하고 freeze한다.
3. freeze된 Call 1 / Call 1.5 / planner / Call 2 / Scallop / AnswerPlan / Call 3 artifact를 stagewise runner에 한꺼번에 넘긴다.
4. stagewise runner가 기존 감사 스크립트를 호출하고 하나의 summary를 만든다.
5. KCL main-table 수치와 stagewise 수치를 섞지 않는다.

Call 2를 다시 샘플링한 결과와 기존 Call 2 artifact의 결과를 같은 stagewise 표에 섞지 않는다. 재실행이 필요하면 artifact set 전체에 별도 run id를 부여한다.

## 단계별 지표 계약

| Stage | Primary metric | Supervision | 해석 |
|---|---|---|---|
| Call 1 | closed-catalog DefinitionRef recall after DSL closure | `v2_call1_definition_gold_draft.json` | 정답 법적 후보가 router+closure를 통과했는가 |
| Call 1.5 | explicit-gold-seed binding recall | DefinitionRef gold + reviewed factual spans | Call 1이 연 직접 seed를 actor/episode/evidence에 결박했는가 |
| Call 2 | exact truth match | reviewed decisive-predicate partial gold | 고정된 proposition의 TRUE/FALSE/UNKNOWN 판정이 맞는가 |
| Symbolic runtime | execution / unresolved diagnostics | frozen Scallop + final-responsibility artifact | typed symbolic chain이 정상 실행되었고 unresolved가 어디 남았는가 |
| Call 3 | required-final-conclusion completeness and state agreement | AnswerPlan | symbolic/typed 결론이 최종 자연어 답안에 보존되었는가 |

Symbolic runtime에 대해서는 독립적인 structured conclusion gold가 없는 상태에서 `symbolic conclusion accuracy`라고 부르지 않는다. 현재 자동 산출치는 실행 및 unresolved 진단이다. 별도의 conclusion gold를 확정하면 그때 정확도를 추가한다.

Call 3의 plan-faithfulness 지표도 KCL rubric quality를 대신하지 않는다. KCL rubric score는 main result이고, Call 3 stagewise 지표는 이미 정해진 결론을 자연어화하면서 훼손했는지 보는 인터페이스 진단이다.

## 실행

먼저 path wiring만 확인한다.

```bash
python scripts/run_v2_stagewise_eval.py \
  --call1 "$CALL1" \
  --call15 "$CALL15" \
  --plan "$PLAN" \
  --call2 "$CALL2" \
  --scallop "$SCALLOP" \
  --answer-plans "$ANSWER_PLANS" \
  --answers "$ANSWERS" \
  --out-dir "$STAGEWISE_OUT" \
  --dry-run
```

그 다음 같은 명령에서 `--dry-run`만 제거한다.

산출물:

- `stagewise_manifest.json`: 입력 artifact 경로와 SHA-256
- `call1_report.json`, `call1_audit.json`
- `call15_audit.json`, `call15_audit.md`
- `call2_partial_gold_audit.json`
- `call3_conclusion_completeness.json`
- `call3_conclusion_state.json`
- `stagewise_summary.json`, `stagewise_summary.md`

## 논문 배치

Results의 독자 질문을 다음 순서로 고정한다.

1. **Main Results on KCL** — 전체 시스템이 최종 법률 답안에서 실제로 좋아졌는가?
2. **Stagewise Evaluation** — 그 성능이 어느 단계에서 확보되고 어느 단계에서 손실되는가?
   - Call 1 routing
   - Call 1.5 binding
   - Call 2 atomic assessment
   - symbolic / typed reasoning
   - Call 3 realization faithfulness
3. **Process/generalization benchmark** — 별도 benchmark를 넣는 경우 KCL과 stagewise 분석 뒤에 둔다.
4. **Error Analysis** — 앞의 수치로 드러난 병목을 사례 단위로 설명한다.

즉 본문 흐름은 `end-task headline → internal mechanism → transfer/process evidence → failure analysis`로 둔다. Call 3의 KCL rubric score를 stagewise에서 다시 반복하지 않고, stagewise에서는 AnswerPlan-to-text faithfulness만 보고한다.
