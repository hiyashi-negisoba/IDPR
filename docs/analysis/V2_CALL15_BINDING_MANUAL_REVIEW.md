# Call 1.5 full-case v4 manual binding review

기준 artifact: `experiments/v2_call15_fullcase_26_v4/issue_bindings.jsonl`.

이 문서는 production 모델과 분리된 offline 감사다. KCL rubric, DefinitionRef gold,
GoldOccurrence는 Call 1.5 또는 Call 2 입력으로 사용하지 않았다. 동일 Gemma의 self-judge 결과도
사용하지 않았다.

## 판정 요약

- Call 1 frozen closure recall: 74/86. Call 1은 변경하지 않았다.
- Call 1.5 v4 contract-valid cases: 26/26.
- bindings: 74.
- question factual scope 밖 quote: 0.
- 명시적 gold seed direct-binding recall: 50/57 (87.7%), 실제 누락 7.
- closure reachability proxy 기준 보존: 65/74 (87.8%). 이것은 top-level 보존이 아니다.
- Call 1의 closure-only gold survivor 17개에 대한 host-derived top-level binding은 모두 미구현이다.
- DefinitionRef 기반 extraneous proxy: 15/74. 수동 확정 실제 과잉은 5/74.
- question_prompt가 요구한 actor 밖 binding: 1.

현재 v4는 Call 2 production 입력으로 승인하지 않는다.

## 명시 seed 누락 7

| case | seed | 수동 판정 |
|---|---|---|
| `kcl_criminal_r10_p1_q1_ga` | `offense.dwelling_intrusion` | 甲이 A를 따라 공동주택 엘리베이터·계단으로 들어간 직접 rubric issue. 실제 누락. |
| `kcl_criminal_r10_p1_q3_ga` | `offense.dereliction_of_duty` | 경찰관 丙이 乙을 입건하지 않은 행위. 실제 누락. |
| `kcl_criminal_r11_p2_q1_na` | `offense.deceptive_obstruction_of_official_duty` | 허위 시험평가서로 결재권자를 오인시킨 episode. 실제 누락. |
| `kcl_criminal_r13_p2_q1` | `offense.deceptive_obstruction_of_official_duty` | 甲의 P2 상대 허위진술. 실제 누락. |
| `kcl_criminal_r13_p2_q1` | `offense.harboring_or_escape` | 甲의 허위진술과 乙의 지시를 검토하는 rubric 대안. 실제 누락. |
| `kcl_criminal_r13_p2_q1` | `offense.obstruction_of_official_duty` | 甲이 검거 중인 P1에게 칼을 휘둘러 상해를 가한 동일 episode. 실제 누락. |
| `kcl_criminal_r14_p2_q1` | `derived_offense.quasi_robbery` | 절도 직후 체포면탈 목적 폭행 episode. closure proxy가 theft binding으로 덮어 숨긴 direct-binding 누락. |

## Call 1.5 누락으로 세면 안 되는 host-derived binding 17

Call 1의 74개 gold survivor 중 17개는 명시 seed가 아니라 closure-only candidate다. 기존
audit은 그중 closure reachability에서도 빠진 3개만 세어 host-derived pending을 과소계상했다.
planner가 closure candidate를 목록에 기록하는 것과 top-level binding을 생성하는 것은 다르다.
현재 host-derived top-level binding 생성은 17개 모두에 대해 미구현이다.

특히 아래 세 건은 robbery/theft와 injury fragment가 별도 binding으로 존재하므로
same-episode compatibility를 확인한 별도 liability target이 필요하다.

- `kcl_criminal_r11_p1_q1`
- `kcl_criminal_r13_p1_q1`
- `kcl_criminal_r14_p2_q1`

## extraneous proxy 15의 수동 재분류

### 실제 과잉 5

| case / binding | 이유 |
|---|---|
| `r10_p1_q1_ga/binding:001` extortion / 甲 | 협박과 성적 행위만 있고 재산 처분 episode가 없다. |
| `r11_p2_q1_ga/binding:002` third-party bribery / 乙 | rubric은 甲·乙의 수뢰 공동정범과 丙의 공여를 다룬다. 乙을 제3자뇌물 actor로 둔 binding은 지지되지 않는다. |
| `r11_p2_q1_da/binding:001` rape / 丙 | 원문·rubric은 준강간 불능미수 episode다. 강간의 coercive episode가 없다. |
| `r12_p2_q1_na/binding:002` ancestral homicide / 乙 | A는 甲의 양부이지 乙의 직계존속이 아니고, 질문 actor도 乙이다. |
| `r14_p1_q3/binding:002` property damage / 乙 | 질문은 甲의 죄책만 요구한다. 乙의 실행은 甲 binding의 context여야 한다. |

### proxy 오탐 10

다음은 rubric gold ref에 직접 포함되지 않아 proxy가 extraneous로 표시했지만 factual binding은
유지할 이유가 있다.

- `r10_p1_q1_ga` injury / 甲: rape-causing-injury의 result context가 되는 실제 injury episode.
- `r10_p1_q2` homicide / 甲, 乙: 사망 결과와 각 폭행 사이의 대안적 attribution 후보.
- `r10_p2_q2` dwelling intrusion / 乙: 주택 창문을 열고 들어간 명시적 episode.
- `r10_p2_q3` negligent homicide / 乙: 특별법 치사 문항을 closed catalog가 받는 factual episode.
- `r12_p1_q1` use of forged private document / 甲: 게시물 첨부라는 사용 후보이며, 선행 문서의
  위조 여부는 Call 2에서 부정될 수 있다.
- `r12_p2_q1_da` deceptive obstruction / 甲: 허위 위임장을 주민센터 직원에게 제출한 episode.
- `r13_p1_q1` injury / 甲: robbery-causing-injury host-derived binding의 component.
- `r14_p2_q1` injury / 乙: quasi-robbery injury 결합의 component.
- `r14_p2_q2` homicide / 乙: 피해자 사망과 robbery conduct 사이 causal attribution 후보.

위 목록에서 `r10_p1_q2` homicide는 actor별 두 binding이므로 총 10 bindings이다.

## actor/grouping proxy 검토

- GoldOccurrence actor conflict 2개는 모두 `r11_p2_q1_ga`의 丙→乙 급부 문장이다. 문장
  행위자는 丙이지만 rubric은 수령자 乙의 수뢰 공동정범도 검토한다. 따라서 두 건을 곧바로
  actor 오류로 세면 안 된다.
- 다만 bribery-taking / 乙 binding은 甲과 乙의 공모 문장을 context로 포함하지 않아 source-span
  sufficiency가 부족하다.
- mixed occurrence 4개는 허위공문서 episode 2개와 권리행사방해 episode 2개다. 모두 actor의
  행위와 다른 participant의 실행을 action/context로 묶은 정상적인 cross-participant episode다.
  GoldOccurrence 분할 때문에 생긴 proxy 오탐이다.

## 다음 acceptance 조건

1. question_prompt에서 source-derived candidate actor set을 만들고 actor 밖 top-level binding을
   host가 거부한다.
2. 명시 seed recall과 closure-derived host binding을 서로 다른 지표로 유지한다.
3. 누락 7을 회복하되 수동 확정 extraneous 5가 늘지 않아야 한다.
4. robbery/injury의 compatible binding에서 별도 host-derived binding 3개를 생성한다.
5. 그 뒤에만 binding-scoped Call 2 전체를 실행한다.
