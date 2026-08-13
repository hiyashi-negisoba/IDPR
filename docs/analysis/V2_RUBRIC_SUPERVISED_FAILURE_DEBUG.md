# V2 rubric-supervised downstream failure debug

기준 artifact: 2026-08-12 diagnostic v3. 이 문서는 KCL rubric을 runtime 입력이나
few-shot으로 사용하지 않는다. rubric은 기대 issue/outcome의 **오프라인 supervision**이며,
최종 결론으로 모든 predicate truth를 역산하지 않는다. LLM judge도 사용하지 않았다.

## 결론

현재 병목을 단순히 `participation` 또는 `Call 3` 문제로 볼 수 없다. rubric에서 요구하는
issue를 현재 proof path에 겹쳐 보면 실패는 다음 순서로 누적된다.

```text
Call 1 / catalog reachability gap
  -> occurrence-local Call 2가 감당할 수 없는 predicate
  -> 명시 사실에 대한 Gemma TRUE/FALSE 오류와 대량 UNKNOWN
  -> completion / indirect-perpetration / doctrine authoring gap
  -> participation reject 또는 잘못된 accepted link
  -> 잘못된 truth와 authored coverage 한계의 Scallop 전파
  -> answer-facing 정보가 제거된 Call 3 payload
```

Scallop parity/runtime 자체가 입력 truth와 다른 결론을 낸 증거는 없다. 그러나 현재
Scallop 입력과 authored semantic coverage가 rubric의 법적 판단을 충분히 표현하지 못하므로,
17건의 성공 실행을 의미 성공으로 승인할 수 없다.

## 재현 가능한 evidence packet

`scripts/build_v2_rubric_supervision_debug.py`가 다음 자료를 case ID로 exact join한다.

- KCL `rubric_summary` 735개 atom
- reviewed Call 1 DefinitionRef gold
- diagnostic Call 2 truth와 participation local truth
- Scallop liability traces
- Call 3 생성 여부와 내부 marker

출력:

- `experiments/v2_restart_rebuild/rubric_supervision_debug_v1/evidence_packet.json`
- `experiments/v2_restart_rebuild/rubric_supervision_debug_v1/evidence_packet.md`

이 packet은 결론성 rubric atom 222개를 별도로 표시하지만, 그것을 leaf predicate gold라고
주장하지 않는다.

## 2026-08-12 normalization delta

이 진단 뒤 다음 경계까지 구현·검증했다. 아래 aggregate 수치는 여전히 diagnostic v3의
historical baseline이며 새 real-Gemma/full 결과가 아니다.

- Article 263은 transport bug가 아니었음을 `tests/test_article263_handoff.py`로 회귀 고정했다.
- `QUESTION_ASSUMPTION`을 GOLD occurrence와 섞지 않는 typed carrier와 KCL 2개 전제를
  `data/v2/question_assumptions.jsonl`에 추가했다.
- KCL completion slice 8개(homicide, ancestral homicide, rape, quasi rape, theft,
  special theft, injury, robbery)를 기존 card/stage/worksheet 근거로 production policy에
  추가했다. 전체 policy는 4개에서 12개가 됐다.
- 변경 registry로 planner core를 dry-run하면 top-level 815, assessment 849, relation 423은
  유지되고 predicate target은 5,182에서 5,838로 증가한다. 추가분은 해당 offense의
  completion 조건에 필요한 predicate다. registry hash가 바뀌었으므로 이전 Call 1
  manifest를 수동 수정해 새 artifact를 쓰지는 않았다.
- 간접정범은 Python runtime의 differentiated dependency path가 이미 있으나 production
  grounding target과 Scallop lowering이 없다. instigator/aider intent를 대신 쓰면 의미가
  달라지므로 typed utilization relation을 연결하기 전까지 production HOLD다.
- reviewed explicit evidence 8개만 담은
  `data/eval/v2_call2_decisive_predicate_partial_gold.jsonl`과 audit script를 추가했다.
  최초 diagnostic v3 대조의 semantic error 3개 중 준강간 1개는 request에 명시적 부정 문장이
  빠졌던 것으로 재분류했다. 따라서 historical ownership은 semantic error 2, model undercall
  4, evidence-scope missing 2이다. 누락 문장은 같은 GOLD occurrence source에 복원했고 다음
  real-Gemma run에서 처음으로 모델 의미 gate가 된다.
  같은 occurrence의 predicate가 offense context별로 달라진 candidate variation은 118개,
  그중 ground fact variation은 33개다. intent처럼 offense-sensitive한 항목이 있으므로
  118개 전부를 오류라고 보지는 않는다.
- Call 1 lineage ownership을 full registry hash에서 실제 neural input인 router catalog
  fingerprint로 분리했다. 기존 manifest는 ordered `catalog_definition_ids` exact match인 경우만
  legacy mode로 재사용하며, 새 manifest는 표시명·kind·statutory refs까지 hash한다.
- GroundFact는 동일 `(case, actor, occurrence, predicate)`마다 한 번만 평가하고 모든 소비
  offense instance에 host가 동일 truth를 투영하도록 바꿨다. LegalElement는 계속
  offense-instance local이다. 새 planner에서 semantic target 5,838개는 유지되지만 neural
  predicate request target은 4,998개로 840개 줄었다. diagnostic v3의 ground-fact contextual
  variation 33개는 다음 run에서 구조적으로 생성될 수 없다.
- KCL issue tag -> 주석서 -> card 경로를 offline audit했다. 26-case의 80개 tag 중 77개는
  commentary target, 75개는 candidate card가 있지만 explicit symbolic bridge는 0개다.
  `exception`/`defeater` card를 곧바로 doctrine으로 발화하지 않고 typed requires/effect/stage/
  instance binding을 authoring해야 한다. 결과는
  `experiments/v2_restart_rebuild/doctrine_card_bridge_audit_v1/`에 있다.
- 새 real-Gemma focused gate는 준강간 evidence 복원과 Article 263 pair-level relation
  evidence를 통과했다. 사문서위조의 `forgery_without_authority`는 같은 seed에서도 TRUE/FALSE가
  오가므로 known model instability로 동결했고 host repair나 case-specific prompt를 넣지 않았다.
- 새 diagnostic full은 exact audit 0 error, predicate 5,838 / neural predicate 4,998 / relation
  423 / participation 5,859이며 8 cases가 participation compile에서 reject됐다. partial gold는
  4 MATCH / 3 MODEL_UNDERCALL / 1 MODEL_SEMANTIC_ERROR였지만, 남은 Article 263 error가 pair-level
  evidence 미운반임을 밝혀 typed carrier를 추가했다. 해당 case-only v7 재실행은 세 조건 모두
  TRUE, audit 0 error다.
- source-local factual participant를 liable actor와 별도 namespace로 고정했다.
  `FactualParticipantKey(case_id, fpart:*)`에는 offense/role/mode/truth가 없고, KCL 간접정범
  supervision 6건의 exact source span만 `data/v2/gold_factual_participants.jsonl`에 기록한다.
  label이 기존 GOLD actor와 같아도 자동 병합하지 않으며 planner top-level universe도 늘리지
  않는다. 반면 production registry에는 아직 offense별 indirect-capability metadata가 없으므로
  card 문자열 검색으로 utilization 후보를 켜거나 모든 offense를 곱하는 구현은 HOLD다.
- decisive partial gold를 15개로 확장했다. 새 3개는 완결된 occurrence가 각각 밀침·상해,
  장래 거짓말 지시, 강도·사망만 진술하는데 `vaginal_intercourse_conduct`,
  `false_testimony_conduct`, `vaginal_intercourse_conduct`를 TRUE로 낸 명시적 false positive다.
  v6 historical artifact 대조는 MATCH 4 / MODEL_UNDERCALL 7 / MODEL_SEMANTIC_ERROR 4다.
  ground-fact contextual variation은 host projection으로 0이므로 이 세 건은 context variation이
  아니라 단일 neural ground-fact 오판이다.

## 1. aggregate failure localization

| boundary | observed evidence | diagnosis |
|---|---:|---|
| rubric supervision | 26 cases, 735 atoms, conclusion-like 222 | answer issue가 단일 offense 성립보다 훨씬 풍부함 |
| reviewed issue refs | 86 total, 74 planned/assessed | 12 refs(14.0%)는 Call 2 전에 도달 불가 |
| all Call 2 truths | TRUE 528 / FALSE 48 / UNKNOWN 4,612 | UNKNOWN 88.9% |
| reached gold-ref truths | TRUE 187 / FALSE 8 / UNKNOWN 985 | 관련 ref 안에서도 UNKNOWN 83.5%; 74 ref 중 16 ref는 전부 UNKNOWN |
| participation | 17 succeeded / 9 rejected | 9건은 downstream 차단 |
| positive participation | instigation 64 / aiding 64 / co 47 | co TRUE 47개는 전부 rejected case에만 존재 |
| Scallop | unresolved Elements 181 / completion unresolved 9 / fail 15 / established 8 | 213 trace 중 성립 8개 |
| doctrine | active rows 0 | rubric의 학설·특수 doctrine branch가 symbolic result에 없음 |
| Call 3 | 17 generated / 9 skipped | 6개 답안에 내부 marker 노출 |

## 2. Call 1 및 catalog reachability

86개 reviewed DefinitionRef 중 12개가 top-level planner universe에 없었다.

| case | missing reviewed ref |
|---|---|
| `r10_p2_q2` | `offense.breach_of_trust` |
| `r11_p2_q1_na` | `offense.dereliction_of_duty` |
| `r12_p1_q3` | `offense.theft` |
| `r12_p1_q4` | `offense.deceptive_obstruction_of_official_duty`, `offense.official_secret_disclosure` |
| `r12_p2_q1_da` | fraud, false/public-document alternatives, lost-property embezzlement 4 refs |
| `r13_p2_q1` | fraud, use-of-forged-private-document 2 refs |
| `r14_p1_q1` | `offense.dwelling_intrusion` |

이 수치는 실제 rubric issue 누락의 하한이다. reviewed DefinitionRef gold 자체가 closed catalog
밖의 다음 issue를 의도적으로 제외했기 때문이다.

- 장물보관
- 교통사고처리특례법상 치사
- 배임수재
- 통신비밀보호법
- 신용카드부정사용
- 일부 성폭력처벌법 및 폭처법 형태
- 보통폭행과 과실치상 일부

또한 negative issue도 답안의 issue이므로, 최종 불성립이라는 이유만으로 router에서 제거할
수 없다. `r14_p2_q4`의 공무집행방해 불성립과 폭행 성립이 대표적이다.

## 3. Call 2 predicate failure ownership

### 3.1 확인된 모델 의미 불안정

다음은 diagnostic request의 evidence scope가 충분하고 rubric과 원문이 같은 방향을 가리키는데
truth가 틀렸거나 반복 실행에서 안정되지 않았다.

1. `r12_p1_q1` 사문서위조
   - 원문: B가 부탁을 받고 B 명의 사실확인서를 작성·교부했다.
   - rubric: 허위 내용이어도 명의자가 작성했으므로 문서죄 불성립.
   - diagnostic v3 및 첫 focused run 2회: `forgery_without_authority=TRUE`.
   - 새 full 및 세 번째 focused run: `FALSE`.
   - 동일 seed/temperature에서도 결과가 달라 stable semantic pass로 승인하지 않는다.
     reviewed general standard 이상으로 prompt를 보강하거나 host repair하지 않는다.

### 3.2 evidence carrier/scope 오류

모델이 아니라 request가 필요한 증거를 받지 못한 사례가 확인됐다.

- `r11_p2_q1_da`: 전체 문제에는 “실제로 C는 반항이 불가능할 정도로 취하지 않았다”가
  있지만 diagnostic GOLD occurrence는 앞 문장인 “술에 취해 누워 있는 C”에서 끝났다.
  따라서 당시 `mental_incapacity...=TRUE`는 모델 semantic error로 확정할 수 없다. 누락
  문장을 동일 occurrence source에 복원했으며 다음 run부터 FALSE를 요구한다.
- `r10_p1_q2`: Article 263 pair binding은 있었지만 shared result/causal-uncertainty 문장이
  payload에 없었다. pair-level factual source/span을 typed carrier로 추가했다. 다만 underlying
  `injury_result`는 여전히 occurrence-local request에서 UNKNOWN이라, 세 Article 263 truth가
  TRUE여도 현재 completion gate는 unresolved다. 이는 Scallop parity 문제가 아니라 result
  evidence의 carrier ownership이 아직 맞지 않는 별도 blocker다.
- `r14_p2_q4`: question prompt가 “P의 직무집행은 적법하다고 전제”하지만 predicate request는
  GOLD occurrence source만 본다. 따라서 `lawful_performance_of_duty=UNKNOWN`이다.
- `r10_p1_q3_ga`: 뇌물 전달 목적과 불법원인급여 법리는 丁 occurrence 하나에 완결되지
  않는다. 그런데 `custody_of_anothers_property=TRUE`를 occurrence-local 판단으로 받았다.
- 간접정범, 신분범, 교사의 착오, 불법원인급여, 대향범은 한 occurrence의 단항 predicate로
  환원되지 않는다.

따라서 Call 2 evidence는 최소한 다음을 구분해야 한다.

```text
LOCAL_OCCURRENCE
QUESTION_ASSUMPTION
MULTI_OCCURRENCE_RELATION
PARTICIPATION_DEPENDENCY
DOCTRINAL_PROJECTION
```

현재는 뒤 네 종류 상당수가 첫 번째 request에 섞여 있다.

### 3.3 모델 undercall과 불필요한 candidate의 결합

rubric-relevant ref 안에서도 truth의 83.5%가 UNKNOWN이다. 일부는 정당한 UNKNOWN이지만
다음과 같은 명시 사실도 UNKNOWN으로 남았다.

- `r12_p1_q4`: 적법하게 선서하고 허위 증언한 丙에 대해 oath와 false testimony는 TRUE지만
  법정 절차 predicate가 UNKNOWN이어서 위증이 막힘.
- `r14_p2_q2`: 칼을 들이대 가방을 빼앗고 피해자가 사망한 사실에서 taking/death/weapon은
  일부 TRUE지만 robbery object, intent, aggravated-result attribution이 UNKNOWN이어서
  rubric의 특수강도치사 결론이 막힘.
- `r11_p2_q1_na`: 허위 시험평가서를 작성하여 결재권자의 도장을 받은 사실에서 공문서 객체만
  TRUE이고 작성권한·허위작성·행사목적·위계행위가 UNKNOWN이다.

반대로 5,859 participation target과 5,182 predicate target의 광범위한 candidate universe는
명백히 무관한 actor/offense 조합까지 모델에 노출한다. undercall과 false positive가 동시에
발생한 이유다.

## 4. RuleIR / completion / participation coverage

### 4.1 diagnostic v3 당시 completion coverage는 구조적으로 부족했음

26개 rubric 중 13개 case, 92개 atom이 미수·중지미수·불능미수·예비를 요구한다. 그러나
production `completion_policies.yaml`에는 다음 네 offense policy만 있다.

- dwelling intrusion
- robbery rape
- special robbery rape
- quasi-robbery rape

따라서 다음 핵심 결론은 현재 Scallop이 표현할 수 없다.

- 준강간 불능미수
- 살인 장애미수·중지미수
- 존속살해 교사불능미수
- 절도·특수절도 불능미수
- 강도예비
- 상해불능미수
- 살인예비 및 예비방조의 불성립

`r11_p2_q1_da`와 `r13_p1_q3`에서 completion이 답안 기대와 어긋난 것은 prompt 문제가 아니라
authored completion universe의 coverage gap이 우선했다. normalization delta에서 KCL
base-offense slice를 12개 policy로 확장했지만 새 predicate truth를 아직 재수집하지 않았으므로
diagnostic v3의 의미 결과가 개선됐다고 주장하지 않는다.

### 4.2 간접정범 production grounding과 이론 branch가 Scallop IR에 없음

rubric은 6개 case, 43개 atom에서 간접정범을 요구한다. 현재 participation form은 direct,
co-principal, instigator, aider뿐이다. 다음은 표현되지 않는다.

- 피해자를 도구로 한 강제추행 간접정범
- 작성권자를 도구로 한 허위공문서작성 간접정범
- 카드 사용자를 도구로 한 사기 간접정범
- 규범적 행위지배에 따른 권리행사방해 간접정범

Python runtime에는 피이용자의 Elements/Unlawfulness/Culpability/Punishability 실패와 다른
과실범 결과를 구분하는 `resolve_indirect_principal_liability()`가 이미 있다. 그러나 이를
호출할 production grounding relation과 Scallop lowering이 없다. 더 선행하는 identity gap도
있다. 강제추행 사례의 피해자 A와 허위공문서 사례의 결재권자는 현재 GOLD의 liable
`actor_id`도, `OffenseInstanceKey`도 아니다. 따라서 간접정범 endpoint를 기존 liability
instance로 제한하면 phantom principal을 만들게 된다. source-local factual participant
identity와 그 participant의 typed outcome을 먼저 정의해야 한다.

또한 11개 case가 학설 분기를 요구하지만 Scallop active doctrine row는 0이다. Call 2가 가진
12개 candidate doctrine도 모두 일반 위법성·책임 조각 계열이고, rubric의 다음 branch는
authored universe에 없다.

- 양해/승낙 이론
- 불법원인급여와 장물성
- 우연방위
- 중지미수 자의성
- 결과적 가중범의 미수
- 적법성 착오
- 공동정범 초과와 교사의 착오

주석서·card metadata의 재사용성은 높다. KCL-26 issue tag 80개 중 77개가 commentary
target, 75개가 article-matched candidate card를 가진다. 다만 이는 설명 근거 retrieval
coverage다. 현재 tag/card와 `DoctrineDef` 사이 explicit bridge는 0개이고, 특히 총칙 corpus
gap이 표시된 tag가 21개다. production에서는 KCL tag를 fact로 넣지 않으며, card function이
`exception`/`defeater`라는 이유만으로 host가 branch를 켜지 않는다. 각 branch에 stable id,
typed requires, effect/stage, offense-instance binding, source card provenance를 authoring해야
Scallop active doctrine으로 내릴 수 있다.

### 4.3 위조사문서행사 정의가 선행 위조를 요구하지 않음

`offense.use_of_forged_private_document`는 현재 `private_document_object`와
`utterance_conduct`만 요구한다. 객체가 실제 위조문서라는 obligation 또는 선행 forgery
realization dependency가 없다. 이 때문에 `r12_p1_q1`에서 기본 위조 판단과 별개로 행사죄가
성립할 수 있었다. 이는 Call 2가 아니라 authored RuleIR defect다.

### 4.4 participation full failure

- 9 cases rejected: cycle 2, multiple derivative 4, overlapping co 1, co/derivative conflict 2.
- TRUE co-principal group 47개가 모두 rejected case 안에 있어 co route는 full에서 한 번도
  end-to-end 검증되지 않았다.
- succeeded case의 accepted derivative 11개에도 `r12_p1_q4`의 “丙 위증행위 -> 甲의
  범인도피 방조”처럼 의미상 잘못된 link가 있다.
- rejected case는 occurrence fragment 중복뿐 아니라 역방향 edge와 무관 offense 전이가
  섞여 있다.

따라서 structural compiler는 정상적으로 hard-fail했지만, successful compile을 semantic
acceptance로 볼 수 없다.

## 5. Scallop 및 downstream handoff

### 5.1 Article 263 transport는 보존됨

Call 2 artifact에는 `r10_p1_q2`의 Article263 pair와 세 predicate truth가 존재한다. 그러나
별도 `article263_assessments` 필드를 Scallop runner가 직접 읽지 않는다는 사실만으로
handoff 누락이라고 판단한 초기 진단은 틀렸다. `run_v2_call2_pilot.py`가
`add_article263_truths()`를 호출한 뒤 양쪽 injury instance의 세 truth를 `case_truths`에
투영하고, Scallop runner는 그 `case_truths`를 읽는다. 실제 diagnostic artifact에도 6개
projected row가 존재한다. 따라서 transport defect는 없고,
`causal_origin_unascertained=FALSE`라는 의미 오판이 실제 blocker다.

### 5.2 성립 8개의 rubric-supervised 질적 판정

| classification | symbolic establishment |
|---|---|
| rubric과 정합 | `r10_p2_q1` 횡령, `r12_p2_q1_da` 위조사문서행사, `r14_p1_q1` 현주건조물방화 |
| rubric과 충돌 | `r10_p1_q3_ga` 횡령, `r11_p2_q1_da` 준강간 기수, `r12_p1_q1` 사문서위조·행사 2개 |
| 조건부 branch를 단일 결론으로 평탄화 | `r12_p1_q2` 절도 |

Scallop이 틀린 truth를 repair하지 않은 것은 계약상 맞다. 그러나 현재 8개 성립 중
answer-facing으로 그대로 승인할 수 있는 것은 3개뿐이다.

### 5.3 Call 3 handoff

Call 3는 17/26만 생성했다. payload는 213 trace를 answer issue로 축약하지 않고 전달하며,
participation route, principal, completion form의 법적 이름, decisive obligation, doctrine,
branch, fired rule을 제거한다. 그 결과:

- established 준강간을 writer가 판단 유보로 뒤집음
- 잘못 established된 횡령·문서죄는 확정적으로 서술
- unresolved를 불성립으로 바꾸거나 여러 instance를 합침
- 6개 case에서 내부 marker가 노출됨

이는 Call 3 prompt 이전의 answer-facing handoff defect다.

### 5.4 normalization diagnostic v6/v7 Scallop 결과

새 v6 diagnostic full은 18 cases를 실행하고 participation-rejected 8 cases를 repair 없이
skip했다. CaseTruths는 TRUE 597 / FALSE 31 / UNKNOWN 5,216이고 active doctrine은 여전히 0이다.
Scallop은 10 instance를 established로 냈으며 runtime/parity error는 관찰되지 않았다.

- rubric과 직접 정합하는 것은 `r10_p2_q1` 횡령, `r11_p2_q1_na` 위계공무집행방해,
  `r14_p1_q1` 현주건조물방화 3개다.
- `r10_p1_q1_ga` 강제추행은 offense 결론은 맞지만 direct realization로 평탄화되어 필요한
  indirect-principal route가 없다. 같은 case의 standalone injury는 answer-facing
  overgeneration이다.
- `r10_p1_q3_ga`의 丁·丙 `bribe_giving` 2개는 전달자/수뢰자의 법적 역할을 잘못 평탄화했다.
- `r12_p1_q1` 위조사문서행사는 base forgery dependency가 없어 여전히 잘못 성립했다.
- `r14_p2_q2` special injury는 특수강도치사 대신 잘못 성립한 offense다.
- `r14_p2_q4` 공무집행방해는 적법성 요소는 전달됐지만 사실의 착오 branch가 없어서 rubric의
  불성립 결론과 반대로 established됐다.

따라서 Scallop은 입력 truth와 authored rules를 정확히 전파하고 있지만, successful execution
18건이나 established 10개를 의미 성공으로 승인할 수 없다. v7 Article 263 carrier는 세
predicate를 TRUE로 고쳤으나 underlying injury completion의 `injury_result=UNKNOWN` 때문에
liability는 여전히 unresolved다.

### 5.5 Article 263 shared-result v8

v7 뒤에도 unresolved였던 이유를 두 경계로 추가 분해했다.

1. dedicated pair request는 법정의제 세 truth만 평가하여, 같은 relation evidence에 명시된
   underlying `injury_result`를 occurrence-local UNKNOWN으로 남겼다.
2. Scallop backend의 dedicated Article 263 parity program은 이미 존재했지만 E2E runner가
   이를 호출하지 않고 generic chain만 실행했다.

기존 Article 263 physical request에 `shared_result_truths` 한 항목을 추가했다. 법정의제 세
truth와 별도 필드이며 새 neural call/stage가 아니다. pair-level known truth는 같은 predicate의
occurrence-local UNKNOWN만 refine할 수 있고 known TRUE/FALSE 충돌은 계속 hard-fail한다.
E2E runner는 두 injury endpoint를 기존 dedicated backend로 보내고 결과를 generic result에
덮어쓴다. backend 자체도 단일 target 실행 시 case-wide truth를 target-instance view로 scope한다.

실제 `call2_article263_shared_result_v8` 결과는 세 statutory truth와 `injury_result`가 모두
TRUE이고 exact audit errors 0이다. Scallop에서는 두 endpoint 모두 completion `completed`,
`StatutoryDeemingObligation=TRUE`까지 도달했다. 남은 unresolved는 양쪽의 `intent=UNKNOWN`이다.
focused real-Gemma에서도 `natural_person_victim_status=TRUE`는 통과했으나 반복적인 복부 가격의
상해 고의는 두 actor 모두 UNKNOWN이었다. predicate definition/evidence가 충분하므로 이를
known model undercall로 동결하고 partial gold `dp:009`~`dp:012`에 기록했다. host repair나 추가
prompt tuning은 하지 않는다.

### 5.6 source-local participant identity와 추가 Call 2 false positive

피이용자는 현재 GOLD liable actor에 없는 A·B·C·결재권자와, 이미 actor로 존재하는 乙·丙이
섞여 있었다. 이들을 `GoldOccurrence`에 추가하면 participant마다 모든 routed offense가
top-level instance로 생성되어 phantom principal과 후보 폭증이 재발한다. 따라서 별도
`FactualParticipantKey`와 exact-span carrier만 만들었고, label 일치에 의한 actor 병합 및
ordinary liability output 투입을 금지했다.

이 identity만으로 utilization production grounding을 열 수는 없다. 현재 registry는 어느
offense가 간접정범 relation 후보인지 typed하게 표시하지 않으며, 관련 정보는 card 서술에만
있다. card 문구를 host가 검색해 후보를 활성화하면 설명 metadata가 법적 판단으로 변한다.
명시적 offense-level capability authoring 전에는 typed utilization relation/Scallop lowering을
HOLD한다.

동시에 partial gold `dp:013`~`dp:015`는 명시적 행위와 canonical predicate 의미가 정면으로
충돌하는 false positive를 확인했다. 이는 evidence scope나 Scallop propagation 문제가 아니라
Call 2의 semantic error다. case별 반례 prompt, few-shot, host truth repair는 추가하지 않는다.

## 6. case-level primary ownership matrix

| case | primary confirmed blockers |
|---|---|
| `r10_p1_q1_ga` | indirect-perpetration 부재, 성범죄/침입 completion coverage, predicate undercall |
| `r10_p1_q2` | Article263 truth 오류, 결과 적용/학설 branch 부재; transport는 정상 |
| `r10_p1_q3_ga` | cross-occurrence doctrine scope, false embezzlement establishment, accepted participation 의미 오류 |
| `r10_p2_q1` | 장물보관 catalog gap, 상해불능미수 coverage, relevant predicates UNKNOWN |
| `r10_p2_q2` | breach-of-trust seed miss, robbery preparation coverage, participation reverse-edge cycle |
| `r10_p2_q3` | traffic special law outside catalog, causal-theory branch 부재 |
| `r11_p1_q1` | realization fragmentation, co/derivative 중복, 무관 offense participation, attempt/초과 coverage |
| `r11_p2_q1_ga` | bribery co-principal/necessary-participant 표현과 local participation 충돌 |
| `r11_p2_q1_na` | indirect perpetration 부재, public-document predicates undercall, dereliction issue miss |
| `r11_p2_q1_da` | 명시적 부정 truth 오류, impossible-attempt policy 부재 |
| `r12_p1_q1` | forgery legal predicate 오류, forged-document dependency가 없는 RuleIR |
| `r12_p1_q2` | 양해/승낙 conditional branch 부재; 단일 establishment로 평탄화 |
| `r12_p1_q3` | theft issue miss, 배임수재 catalog gap, 업무상배임 predicate undercall |
| `r12_p1_q4` | positive official-secret issue miss, perjury undercall, false accepted harboring link |
| `r12_p2_q1_ga` | homicide/theft occurrence fragmentation, participation reject, mistake/attempt coverage |
| `r12_p2_q1_na` | preparation/aiding-of-preparation form 부재 |
| `r12_p2_q1_da` | 4/8 reviewed refs miss, base forgery undercall, use/base dependency 불일치 |
| `r13_p1_q1` | co-principal realization fragmentation, impossible-attempt coverage, overlapping co groups |
| `r13_p1_q3` | homicide attempt/abandonment policy 부재, explicit conduct/intent undercall |
| `r13_p2_q1` | fraud/document refs miss, false participation across unrelated card/use/violence occurrences |
| `r14_p1_q1` | dwelling-intrusion miss, homicide attempt policies, derivative requirement UNKNOWN |
| `r14_p1_q2` | fraud/bribe occurrence overconnection, co/derivative conflict, illegal-cause doctrine scope |
| `r14_p1_q3` | factual action direction과 legal dependency 방향 혼동, indirect-perpetration 표현 부재 |
| `r14_p2_q1` | theft/violence realization fragmentation, co/derivative ambiguity, theory branch 부재 |
| `r14_p2_q2` | result-attribution/robbery predicates undercall, causation theory branch 부재 |
| `r14_p2_q4` | question assumption이 Call2 evidence에서 누락, assault outside catalog, negative outcome branch 부재 |

## 7. 수정 전 확정해야 할 순서

이 문서는 planner를 설계하지 않는다. 다음 구현은 아래 실패를 순서대로 분리한 후 시작해야
한다.

1. **Evidence transport:** Article263 transport는 정상임을 회귀 고정하고, question
   assumption을 evidence carrier에 포함할 계약을 정의한다.
2. **Authored coverage:** KCL-26에 필요한 completion form, indirect perpetration, special
   doctrine/branch, forged-document dependency 중 무엇을 현 V2 scope에 포함할지 결정한다.
3. **Call2 supervision:** rubric + GOLD occurrence로 명시적으로 판정 가능한 decisive
   predicate만 partial gold로 만들고, 모델 오류와 scope 오류를 분리한다.
4. **Participation:** realization identity와 group-local unresolved semantics를 별도 계약으로
   다룬다. 현재 rejected 결과를 repair하지 않는다.
5. 그 다음에만 rubric-supervised issue planner와 AnswerPlan을 설계한다.

prompt에 case별 반례나 few-shot을 추가하는 것은 위 어느 failure class도 근본적으로 해결하지
못하므로 계속 금지한다.

## 8. 2026-08-12 indirect-principal structural lowering delta

5.6에서 HOLD했던 capability authoring과 utilization 경로를 구현했다. 이 delta는 앞선
historical diagnosis를 지우지 않고, 그중 indirect-principal 부재가 해소된 구조적 범위만
기록한다.

- exact offense의 explicit `indirect_principal_capability.legally_possible: true`만 static
  candidate scope로 사용한다. metadata 부재는 unauthored/out-of-scope이고 derived offense는
  base metadata를 상속하지 않는다. card prose, rubric tag, statute, participation mode fallback은
  모두 금지했다.
- factual relation은 offense-free
  `(case, utilizer actor, occurrence) -> source-local factual participant` direction이다. model
  output은 사실적 지시·야기·이용의 `TRUE/FALSE/UNKNOWN`뿐이며 legal effect는 없다.
- host compiler는 relation과 exact participant/offense의 내부
  `UtilizedParticipantOutcome`을 결합한다. missing/duplicate/wrong identity/capability는
  hard-fail하고 UNKNOWN은 보존한다. utilized participant가 exact offense에 liable하면 dependency는
  FALSE, 구성요건·위법성·책임·가벌성 단계의 defeat 또는 다른 과실범 outcome이면 TRUE다.
- indirect-principal runtime은 compiled dependency를 직접 소비하며 instigator/aider policy나
  intent predicate를 재사용하지 않는다.
- Scallop은 전용 `v2_indirect_principal_dependency_truth` relation과 program으로 lower한다.
  `v2_derivative_link` 경로는 사용하지 않고 host/Scallop exact row 및 truth parity를 검증한다.

planner dry-run은 factual utilization target 10개, audit errors 0이다. target은
`r10_p1_q1_ga`, `r11_p2_q1_na`, `r12_p1_q1`, `r12_p2_q1_da`, `r14_p1_q3`에 각 2개다.
`r13_p2_q1`은 Step 7 closure가 `derived_offense.fraud`를 만들지 않아 0개이며 이는 capability
fallback으로 고칠 대상이 아니다.

남은 생산 경계는 `UtilizedParticipantOutcome`이다. production에서는 participant를 ordinary
liability output으로 바꾸거나 rubric 결론/one-shot legal-stage 질문으로 outcome을 채우지 않는다.
predicate-level truth를 participant identity와 exact offense에 binding해 내부 stage outcome을
계산하는 producer가 필요하다. 따라서 real-Gemma full Call 2와 IssuePlanner/Call3는 계속
보류한다. 구현 회귀는 full local suite `130 passed, 13 skipped`로 통과했다.

### 8.1 production outcome producer closure

위의 남은 경계를 participant전용 predicate carrier와 deterministic producer로 닫았다.
핵심 불변식은 factual participant를 `OffenseInstanceKey`/ordinary liability result로 승격하지
않는 것이다. model은 exact offense의 요청된 predicate truth만 내고 host가 Elements와
active unlawfulness/culpability/punishability stage를 계산한다. missing relation은 UNKNOWN,
different-negligence는 explicit truth만 허용한다. participant completion 계약이 없는
completion-bearing offense는 fail-closed한다.

planner exact frontier는 outcome 5개 / participant predicate 26개이다. Call 2 runner와 exact audit,
deterministic dependency compiler, dedicated Scallop parity handoff까지 연결했다. factual evidence의
지시어 단편 5개는 새 법적 label 없이 완전한 출처 문장으로 확장했고,
`false_public_document_creation`은 명시적 intent 구성요건을 추가했다. planner audit은
errors 0이며 final assessment 5840 / neural request 5000이다.

새 live semantic gate는 인식 없는 공정증서 작성자 intent FALSE, 자기 명의 사문서
작성자의 타인 명의권한 FALSE, 비소유 乙의 권리행사방해 subject FALSE 세 건을 고정했다.
다만 endpoint env가 없고 새 prompt 승인도 필요하므로 real-Gemma 결과는 아직 없다.
로컬 검증은 `137 passed, 16 skipped`, focused `46 passed`, Ruff/compile 통과다.
IssuePlanner/Call3/judge는 live gate와 full Call 2 이후까지 계속 HOLD한다.

### 8.2 job 221593 full-production observation

축약·재서술 3-case 테스트를 승인 게이트로 사용하지 않고, production gold span과
현재 planner 전체를 job 221593의 Gemma에 실행했다. exact audit은 errors 0이지만
participation compile reject 8개를 계속 수집한 `DEGRADED_DIAGNOSTIC`이다. 6,184 requests,
9,489,400 total tokens이며 participant frontier 5/26을 포함한다.

participant predicate는 TRUE 7 / UNKNOWN 19, outcome 5개 전부 unresolved이다. 즉 새
typed producer/host dependency transport는 exact correspondence를 지켰지만, Gemma가 fixed participant의
명시적 부정 요건을 충분히 FALSE로 낮추지 못했다. factual utilization은 TRUE 8 / FALSE 2다.
partial-gold은 MATCH 5 / undercall 6 / semantic error 4이므로 전체 재실행만으로 의미 오류가
해소되지 않았다.

다음 분석은 이 artifact의 8 participation reject과 5 participant unresolved를 원본 문항·actual
payload 단위로 분리한다. IssuePlanner/Call3/judge는 계속 HOLD한다.
