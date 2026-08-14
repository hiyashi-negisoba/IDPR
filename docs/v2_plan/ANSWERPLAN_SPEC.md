# AnswerPlan 확정 스키마 — rubric 역설계

2026-08-13. `data/v2/v2_call3_prompt.md` §22 초안 스키마를 KCL rubric이 실제로 채점하는
항목 유형에 맞춰 확정한 것이다. 짝 문서는 `docs/analysis/v2_call3_prompt_review_ko.md`
(Call 3 프롬프트 전문 검수)다.

AnswerPlan은 **새로운 판단을 만들지 않는다.** Scallop/`FinalResponsibilityView`/
`LiabilityEvaluation`이 이미 산출한 것을 손실 없이 투영하고, 각 항목에 그 항목을 서술하는 데
필요한 규범 근거를 붙이는 것이 전부다. 이 문서에서 "계산"이라고 부르는 것은 전부 결정론적
재배열이다.

---

## 0. rubric 관측 사실 (설계의 근거)

KCL-26 실체법 문항의 rubric 735항목을 **유형 집계**한 결과다. 사건 내용 열람은 승인된
dev case 2건(`r10_p1_q1_ga`, `r14_p1_q2`)으로 한정했고, sealed-24는 항목 수·배점·어미
패턴 같은 case-agnostic 통계만 사용했다.

| rubric 항목 유형 | 항목 수 | 비중 |
|---|---:|---:|
| 결론 ("~죄책을 진다고 결론 내리는지") | 172 | 23.4% |
| 언급 (죄수·불성립·부수쟁점) | 153 | 20.8% |
| 판례 법리 인용 요구 | 115 | 15.6% |
| 법리 설명(rule statement) | 109 | 14.8% |
| 쟁점 제기 ("~의 성부를 논하고 있는지") | 71 | 9.7% |
| 조문 적시 | 65 | 8.8% |
| 죄수(경합·흡수·특별관계·불가벌) | 58 | 7.9% |
| 학설 대립 | 40 | 5.4% |

문항당 항목 13~55개(평균 28.3), 배점 10~55점(평균 22.1).

**이 통계는 프롬프트·스키마 설계의 근거로만 쓴다.** 문항별 수치는 AnswerPlan에도 프롬프트에도
들어가지 않는다(§2.1, 계약 §4-8).

판례 요구 115항목 중 **사건번호를 요구하는 것은 2개뿐**이고 113개는 판시 법리의 내용만
요구한다. 이 사실이 §5의 근거 채널 선택을 결정한다.

---

## 1. 초안 §22 대비 델타

| # | 델타 | rubric 근거 |
|---|---|---|
| D1 | `legal_standard` + `governing_provision`을 decisive finding에 동봉 | 법리 설명 14.8% + 조문 적시 8.8% |
| D2 | 판례 법리 문장(`rule_statements`)을 별도 슬롯으로 신설 | 판례 인용 15.6% |
| D3 | 흡수·특별관계 쌍의 **양쪽**을 보존하고 "불성립으로 논하라"를 명시 | 죄수 7.9%, 어미 `...지 않는다고 결론 내리는지` 21건 |
| D4 | issue 간 **선결 의존 순서**를 실어 보냄 | dev rubric의 "본죄 성부 검토에 앞서 …를 먼저 살피는지" |
| D5 | `contested_points` — 학설 대립 지점. 출처는 authored/reviewed 자산으로 잠근다 | 학설 대립 5.4% |
| D6 | 분량은 plan 자체의 쟁점 수로만 조절 (rubric 수치는 plan에 넣지 않는다) | 항목 13~55개의 편차 |
| D7 | 죄명마다 명시적 결론 문장을 요구(통합 논증은 유지) | 결론 23.4%, 어미가 죄명 단위 |

초안에서 **삭제하지 않는 것**: §7 final_state anchor, §9 participation route 필수 보존,
§13 UNKNOWN≠FALSE, §18 host 무개입, §20 내부 표현 노출 금지. 전부 유지한다.

---

## 2. 확정 스키마

```text
AnswerPlan
├── case_id
├── case_text                      # 사건 원문 전문 (초안 §4)
├── question                       # 원 질문 전문 (초안 §5)
│                                   # D6. 분량 필드는 두지 않는다. §4-8 / §2.1 참조.
│
├── discussion_order[]             # D4. anchored_issue id의 선결 의존 위상정렬
│
├── anchored_issues[]
│   ├── issue_id                   # 사람에게는 노출되지 않는 내부 키
│   ├── actor
│   ├── offense_label              # 자연어 죄명 ("주거침입강간치상죄")
│   ├── governing_provision        # D1. "형법 제319조 제1항" 등
│   ├── episode_facts              # 해당 factual episode 서술 + exact quote
│   ├── final_state                # ESTABLISHED | NOT_ESTABLISHED | UNRESOLVED
│   │                              # | NOT_ATTRIBUTABLE | ABSORBED | SUPERSEDED
│   ├── completion                 # {state, why}  (초안 §8)
│   ├── participation              # {mode, principal_actor, principal_offense,
│   │                              #  principal_realization, relation}  (초안 §9, 필수)
│   ├── stage_results              # elements / unlawfulness / culpability / punishability
│   ├── decisive
│   │   ├── stage                  # LiabilityEvaluation.decisive_stage
│   │   ├── satisfied[]            # {statement, legal_standard, governing_provision,
│   │   │                          #  rule_statements[], supporting_quote}
│   │   ├── failed[]               # 동형
│   │   └── blocking[]             # UNKNOWN. 동형. 여기에 "확정하기 어렵다"가 붙는다
│   ├── doctrines[]                # {label, stage, effect, outcome}
│   │                              # raised-but-inactive와 active를 구별해 표시 (초안 §10)
│   ├── contested_points[]         # D5. {label, positions[], adopted, why_adopted, origin}
│   │                              #     origin ∈ {authored_doctrine, reviewed_card}
│   │                              #     rubric 유래 금지. §2.2 / §4-9
│   └── provenance
│
├── final_responsibility
│   ├── retained[]                 # 최종 죄책 집합
│   ├── absorbed[]                 # D3. {absorbed_offense, absorbing_offense, relation,
│   │                              #      condition_statement, legal_standard}
│   ├── imaginative_pairs[]        # 상상적 경합
│   ├── substantive_concurrence    # 실체적 경합 최종 결론
│   ├── excess_attributions[]      # 초과로 귀속이 차단된 것
│   └── status_redirections[]      # 제33조 단서
│
└── open_issues[]
    ├── known_representation_gaps  # data/v2/representation_gaps.yaml
    └── unmapped_instances         # UNMAPPED_DERIVED_ARTICLE 등, 근거 없이 서술될 영역
```

### 2.1 분량 필드를 두지 않는 이유

초안 검토 단계에서는 `target_scale = {rubric_item_count, score}`를 두려 했다. **철회한다.**
rubric 문면을 감추더라도 "이 문항은 항목 37개에 30점"은 문항별 gold annotation을 생성 단계에
주는 것이고, reviewer가 oracle signal로 공격할 수 있다. rubric 통계는 **프롬프트 설계 근거로만**
남기고(§0) plan에는 어떤 형태로도 싣지 않는다.

분량 조절은 두 경로로 충분하다.

1. plan 자체가 이미 분량의 대리 변수다 — `anchored_issues` 수 + `contested_points` 수 +
   `final_responsibility.absorbed` 수 + `open_issues` 수. 별도 필드로 계산해 넘길 필요도 없이
   payload를 읽으면 드러난다.
2. 프롬프트가 이미 그렇게 지시한다 — "분량은 `analysis`와 `open_points`가 담은 쟁점의 수에
   맞춘다."

### 2.2 `contested_points`의 출처

`contested_points`는 **production knowledge에서만 온다.** 허용되는 출처는 둘이다.

- `origin: authored_doctrine` — `data/v2/definitions/doctrines.yaml` 등 authored DSL이
  이미 갈래를 표현하고 있고 런타임이 그중 하나를 택한 경우. `adopted`는 런타임이 택한 갈래,
  `why_adopted`는 authored `legal_standard`다.
- `origin: reviewed_card` — reviewed 카드 코퍼스에 대립하는 명제가 실려 있는 경우
  (`doctrinal_status`, `variant_group`이 이미 이 관계를 들고 있다). §5.5의 회수 경로로만
  들어오고 `card_id`를 동반한다.

**rubric에서 생성하거나 보완하지 않는다.** 특정 문항의 rubric에 "미수설·기수설 대립을 언급하는지"가
있다는 이유로 그 대립을 plan에 채워 넣으면, 그 5.4% 배점은 우리 지식이 아니라 채점표를 되받아
쓴 것이 된다. 대립을 표현할 자산이 없으면 그 항목은 **비워 둔다** — 카드 A가 "`analysis`가 견해
대립을 제시한 쟁점은"이라고 조건절로 쓰인 이유가 이것이다. plan이 비어 있으면 모델은 자기 기억으로
학설 대립을 만들어내지 않는다.

**이건 output skeleton이 아니다.** 초안 §22의 경고를 그대로 유지한다 — Call 3가 이 배열
순서대로 문단을 뽑는 게 아니라, 사건 reasoning state를 손실 없이 전달하는 input
representation일 뿐이다. 유일한 예외가 `discussion_order`이고, 그것도 "이 순서를 지키라"가
아니라 "이 선후관계를 깨지 말라"는 제약이다.

---

## 3. 런타임 → AnswerPlan 투영표

새로 계산할 것이 거의 없다는 것을 보이기 위한 표다.

| AnswerPlan 필드 | 출처 | 비고 |
|---|---|---|
| `anchored_issues[].final_state` | `LiabilityResult` + `FinalResponsibilityView` | 후자가 우선 (초안 §11) |
| `decisive.stage` | `LiabilityEvaluation.decisive_stage` | 그대로 |
| `decisive.satisfied/failed/blocking` | `LiabilityEvaluation.decisive_obligation` + `ObligationOutcome` | truth로 3분할 |
| `.legal_standard` | 해당 predicate의 authored `legal_standard` | 164개 저작 완료 |
| `.governing_provision` | authored `authority_refs[].citation` (`statute_text`) | 148개 |
| `doctrines[]` | `AppliedEffect` + `RaisedDoctrine` | active/raised 구별 |
| `participation` | `ParticipationDependencyObligation` + participation grounding | 필수, 누락 시 hard-fail |
| `completion` | `CompletionRequirementObligation` + completion policy | |
| `final_responsibility.absorbed[]` | `ConcurrenceResolution.absorbed_instances` | |
| `.condition_statement` / `.legal_standard` | `ConcurrenceRule` 동명 필드 | 이미 규칙이 지고 있다 |
| `excess_attributions[]` | `ExcessAttribution` | |
| `status_redirections[]` | `FinalResponsibilityView.status_redirections` | 제33조 단서 |
| `open_issues` | `data/v2/representation_gaps.yaml` + `UnresolvedFinding` | |
| `contested_points[]` | authored `doctrines.yaml` 갈래 / reviewed 카드 `variant_group` | **rubric 유래 금지** (§2.2) |
| `rule_statements[]` | **§5의 근거 채널** | 유일한 신규 조립 |

`contested_points`와 `rule_statements` 둘만 런타임 산출물의 직접 투영이 아니다. 전자는
authored/reviewed 자산의 조회, 후자는 §5.5의 검색 회수다. 그 밖의 모든 필드는 결정론적 재배열이다.

---

## 4. 계약

AnswerPlan 빌더가 지켜야 하는 것. 전부 테스트로 고정한다.

1. **참가 route 필수.** `participation.mode`가 있는 instance에 `principal_actor`가 없으면
   hard-fail. 초안 §9의 요구를 계약으로 승격한다.
2. **흡수 쌍 양방향 보존.** `absorbed[]`의 각 항목은 흡수되는 죄와 흡수하는 죄를 **둘 다**
   이름으로 들고 있어야 한다. 한쪽만 있으면 hard-fail. rubric이 "~는 흡수관계로 별도로
   성립하지 않음을 언급하는지"를 채점하므로, 흡수된 죄가 plan에서 사라지면 그 배점을 잃는다.
3. **UNKNOWN 보존.** `blocking[]`이 비어 있지 않은 issue의 `final_state`는 절대
   `NOT_ESTABLISHED`가 될 수 없다.
4. **lineage guard 계승.** E2E와 동일하게 참가 병합 plan만 받는다
   (`require_participation_plan_lineage`).
5. **내부 식별자 비노출.** 직렬화 단계에서 `binding:*`, `factual_episode:*`, `offense.*`,
   `legal_element.*`, `UNKNOWN`, `stage=`, `source_run=` 문자열이 payload에 남으면 hard-fail.
   자연어 라벨로 치환된 것만 나간다. (초안 §20)
6. **근거 무결성.** `rule_statements[]`의 각 문장은 카드 코퍼스에 존재하는 명제의 정확한
   복사여야 하고 `card_id`를 동반한다. 요약·합성 금지.
7. **gold precedent 차단.** 빌더는 데이터셋의 `supporting_precedents` 컬럼을 읽지 않는다.
   §5.1의 배제 결정을 코드 수준에서 고정한다.
8. **rubric 수치 차단.** plan의 어떤 필드도 `rubrics` / `score` 컬럼에서 파생되지 않는다.
   문항별 항목 수·배점을 담은 필드를 두지 않는다(§2.1).
9. **`contested_points` 출처 잠금.** 모든 항목은 `origin ∈ {authored_doctrine, reviewed_card}`를
   갖고 그 출처 id(`doctrine_ref` 또는 `card_id`)를 동반해야 한다. **evaluation rubric에서
   생성하거나 보완하지 않는다.** origin 없는 항목이 들어오면 hard-fail한다(§2.2).

10. **카드는 truth를 바꾸지 않는다.** 회수된 카드를 주입한 plan은 주입하지 않은 plan과
    issue 집합·`final_state`·`decisive` 3분할·`required_final_conclusions`가 **완전히 동일**해야
    한다. 카드는 `rule_statements[]`에만 나타난다. 이것이 §5.3이 Call 2 카드 A/B를 부결한
    사유가 Call 3에서 재발하지 않음을 코드 수준에서 보증하는 방식이다. 빌더 테스트가
    N plan과 P plan을 실제로 비교해서 지킨다.

계약 7·8·9는 하나의 원칙이다 — **평가 자료는 설계 근거로만 쓰고 산출물에 흘려보내지 않는다.**
세 항목 모두 빌더 테스트로 고정하고, 위반 시 plan 생성이 실패하도록 한다.

---

## 5. 판례 근거 채널 — 우리 카드 코퍼스 (production)

### 5.1 데이터셋 gold precedent는 쓰지 않는다 (배제 확정)

2026-08-13 결정. 어떤 조건에서도 쓰지 않는다 — production 경로에서도, ablation 조건에서도.

배제 사유 둘:

1. **oracle이다.** `supporting_precedents`는 그 문항의 정답 판례이고, 판시사항 항목이
   사건의 결론을 그대로 담고 있는 경우가 있다(dev case에서 확인). rubric의 판례 항목을
   정답지에서 받아쓰는 구조가 된다.
2. **용량이 안 맞는다.** 문항당 평균 8.4건(총 219건), 건당 평균 6,080자(최대 92,129자)로
   **문항당 평균 5만 자**다. 선별 없이 넣을 수 없고, 선별하려면 결국 §5.5의 검색기가
   필요하다 — 즉 gold를 쓰더라도 카드 경로의 기계를 그대로 다시 만들어야 한다.

AnswerPlan 빌더는 이 컬럼을 읽지 않는다. 테스트로 고정한다(§4-7).

### 5.2 왜 카드 코퍼스로 충분한가

| 사실 | 값 |
|---|---|
| 카드 코퍼스 | 1,848장 / reviewed issue 383개 |
| `authority_basis: commentary_reported_precedent` | **638장 (34.5%)** |
| 사건번호를 담은 카드 | 10장 |
| **rubric 판례 항목 중 사건번호를 요구하는 것** | **115개 중 2개** |

rubric은 판시 **법리의 내용**을 요구하지 번호를 요구하지 않는다. 638장의 판례 유래 명제는
정확히 그 형태다. 반대로 v2 authored definition의 `authority_refs`는 165개 중 판례근거가
12개뿐이므로, `legal_standard`만으로는 이 15.6% 배점을 채울 수 없다. 카드가 그 공백을 메운다.

### 5.3 왜 이 용법은 부결된 A/B와 다른가

`experiments/v2_call15_directscope_26_causal/card_call2_ab_v1/`은 카드를 **Call 2의 truth
채널**로 쓰는 실험이었고 순증분 UNKNOWN −3/88, decisive gold 개선 0/3으로 부결됐다. 부결
사유는 전부 truth를 바꾸는 것의 리스크였다 — occurrence identity 혼합 1건, evidence
provenance 불충분 2건.

Call 3는 truth를 만들지 않는다. `card_issue_join_v1/audit.md`가 이 용법을 이미 지목해 뒀다:

> `support_issue`: Rule/IRAC 설명과 근거 보강용이며 symbolic effect는 없다.

따라서 카드는 **서술 근거로만** 들어가고, 카드 명제가 anchored conclusion과 충돌하면 언제나
anchor가 이긴다(프롬프트 검수 문서 카드 E).

### 5.4 타이밍 — Scallop 이후, AnswerPlan 조립 시점

Call 2 앞이 아니다. 근거 셋:

1. Call 2 앞에서 하면 truth 채널이 되고, 그건 §5.3에서 부결됐다.
2. Scallop 이후에는 **답안에 실제로 등장할 issue가 확정**된다. join audit 기준 26문항의
   issue candidate는 213개지만, final responsibility로 좁히면 그 일부만 남는다.
3. 검색 scope는 established에 한정하지 않는다. rubric이 흡수·불성립도 서술을 요구하므로
   **`final_responsibility` 전 항목 + `decisive.blocking`까지** 포함한다.

### 5.5 회수 절차

검색 unit은 `(offense_instance, decisive/blocking predicate)`이고, 회수 결과도 **그 쌍에
키가 걸린다.** instance 단위로 붙이면 같은 죄 안에서 어느 요건 때문에 성립·불성립·미확정인지가
사라지고, 그 구별이 이 채널의 존재 이유다.

부착 대상은 `satisfied`에 한정하지 않는다 -- **`failed`와 `blocking`에도 붙인다.** 불성립·미확정을
서술하려면 그 요건이 왜 필요한지에 대한 법리가 오히려 더 중요하다.

3단 폴백:

1. **결박.** `data/v2/card_target_issue_bridge.yaml`에 route가 있으면 그 issue로 확정한다
   (52 routes / 40 predicate / 21 offense, 검수 완료). 검색 점수로 parent issue를 고르지
   않는다는 기존 계약을 그대로 계승한다.
2. **조문 family 내 검색.** route가 없으면 그 instance의 authored 조문 identity로 issue
   family를 제한한 뒤, 해당 occurrence의 exact factual quote를 질의로 BM25 + embeddinggemma-300m
   RRF → bge-reranker-v2-m3 재정렬. 활성 issue 아래에서 **detail card 최대 2장**.
3. **근거 없음.** 위 둘 다 실패하면 카드 없이 `legal_standard` + `governing_provision`만
   보낸다. 카드를 억지로 붙이지 않는다.

`element_issue` 외에 `stage_issue`(실행착수·기수·중지미수), `participation_issue`(교사·방조·
공동정범), `guard_issue`(위법성·책임조각), `concurrence_issue`(경합·흡수)를 각각 해당
AnswerPlan 슬롯의 근거로 회수한다. join audit의 selected issue function 분포
(element 133 / support 27 / concurrence 21 / guard 18 / stage 8 / participation 6)가 이
슬롯 매핑과 그대로 대응한다.

### 5.6 알려진 한계 — 명시하고 봉합하지 않는다

KCL-26의 87 instance 중 16개가 `UNMAPPED_DERIVED_ARTICLE`이다(특수절도 5, 상해치사 2,
사기 2, 강도치상 2, 준강도 2, 강간치상 1, 강도상해 1, 강도치사 1). 이 instance들에는 카드가
붙지 않고 `legal_standard`만 간다. **base 조문 상속으로 임시 보완하지 않는다** — join
audit의 기존 결정을 그대로 유지한다. 대신 `open_issues.unmapped_instances`에 기록해
Call 3가 자기 법학지식으로 서술하도록 둔다.

---

## 6. 근거 채널 ablation (논문용)

gold를 배제해도 단일 변수 실험은 그대로 성립한다. AnswerPlan의 근거 슬롯만 끄고 켠다.

| 조건 | `rule_statements[]` 출처 |
|---|---|
| **P (production)** | 저작된 `authority_refs` 전부 + §5.5의 카드 회수 |
| **N (floor)** | 저작된 `authority_refs` 전부(조문 148 / 판례 12). **카드 회수 없음** |

rubric type-2(판례 인용, 15.6%) 점수의 P−N 차이가 곧 **카드 코퍼스가 서술 근거로 기여하는
몫**이다. 두 조건의 symbolic anchor가 동일하므로 결론 정확도 축은 움직이지 않고 서술 축만
분리해서 측정된다. 추가 저작이나 외부 자산 없이 지금 자산으로 나온다.

**N을 "근거 없음"으로 적지 않는 이유.** authored `authority_refs`는 조문 근거와 판례 근거를 한
리스트에 담고 있고, `governing_provision`은 그중 `statute_text`를, precedent 항목은 같은
리스트의 나머지를 투영한 것이다. 판례 근거 12개 중 8개는 케이스노트 항목 참조이고 사건번호가
붙은 인용은 둘뿐이며, 26문항 plan에 실제로 나타난 것은 5건이다. 이 12개를 N에서 떼어낼 수는
없다 -- `legal_element.coercion_sufficiency_for_forcible_indecency`의 `canonical_meaning`이
`낮은 기준(2018도13877 전합)`이어서, 인용을 빼면 더 깨끗한 floor가 아니라 뜻을 잃은 predicate가
된다. 저작 자산을 양쪽에 동일하게 깔고 **카드 채널만 켜고 끄는 것**이 단일 변수다.

그러므로 P−N을 "규칙베이스 전체의 서술 근거 기여"로 서술하지 않는다. 저작된 12개 판례 근거도
규칙베이스 자산이므로, 그 문장은 N에 이미 깔린 몫을 카드 채널의 공로로 돌리는 것이 된다. 이
어긋남의 방향은 안전한 쪽이다 -- N이 그만큼 강한 floor이므로 P−N은 과소추정이다.

---

## 7. 구현 순서

1. `src/idpr/v2/runtime/answer_plan.py` — §3 투영 + §4 계약. 신규 모델 호출 0.
2. `scripts/build_v2_answer_plan.py` — 정본 artifact(`final_responsibility_v10` /
   `doctrine_e2e_v11` / `absorption_e2e_v12`)를 읽어 26문항 plan 생성.
3. §5.5 근거 회수를 `answer_plan.py`에 연결. 기존 `idpr.retrieval` 재사용.
4. 프롬프트 승인 후 `scripts/run_v2_call3.py`.
5. dev case 2건으로 먼저 관통 확인 → 26문항 full E2E.

1~3은 API 호출이 없고 승인 게이트에 걸리지 않는다. 4가 프롬프트 승인 게이트다.
