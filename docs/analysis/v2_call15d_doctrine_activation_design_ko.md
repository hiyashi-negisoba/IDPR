# 검수 요청: Call 1.5-D doctrine activation 설계

2026-08-13. 프롬프트는 아직 작성하지 않았고 모델도 부르지 않았다. 이 문서는 **설계 검수용**이며,
승인 후에 (1) Call 1.5-D 프롬프트 전문을 별도로 올려 승인받고, (2) 실행 후 Call 2 증분 target
목록을 다시 보고한 뒤에야 Call 2를 돌린다.

## 0. 왜 이 경로가 필요한가

active doctrine은 26문항 전부에서 0이다. Scallop 결함이 아니라 dead loop다 -- closure가 13개
doctrine을 모든 사건에 후보로 열지만, 활성화는 leaf가 non-UNKNOWN이어야 하고, **그 31개 leaf를
planner가 한 번도 target으로 만든 적이 없다.** 확인했다: 현재 Call 2 truth에 저 31개 중
**0개**가 있고, planner의 `selected_predicate_refs`에도 **0개**가 있다.

그렇다고 31개를 87개 instance에 전부 여는 것은 답이 아니다. 그것만으로 target이 2,697개가
되어 현재 534개의 5배가 된다. 그래서 "무엇이 제기되었는가"를 먼저 사실 층에서 좁힌다.

## 1. 경계 (설계 제약)

- Call 1.5-D는 **법리명을 예측하지 않는다.** 모델 입력에 doctrine id, 조문 번호, 법리 이름이
  들어가지 않는다. 저작된 `factual_cue` 문장만 보고 "원문에 이런 사실이 적혀 있는가"에 답한다.
- **cue 부재는 doctrine FALSE가 아니다.** not raised이고, 그 단계는 지금처럼 preserved다.
- host는 raw text를 읽고 doctrine을 추론하지 않는다. `doctrine_raising_cues.yaml`의 저작된
  매핑만 쓴다.
- doctrine이 raised된 뒤에만 그 doctrine의 leaf를 Call 2 target으로 연다.
- rubric/gold는 runtime 입력도 activation source도 아니다.

## 2. Call 1.5-D 입출력 schema

### 단위

**요청 하나 = factual episode 하나.** KCL-26에는 episode가 43개(그중 instance를 가진 것이 38개)
있고 전체 episode 본문이 9,076자, 중앙값 182자다. 즉 요청당 입력이 매우 작다.

### 입력 payload (모델에게 가는 것)

```json
{
  "factual_episode_id": "factual_episode:001",
  "episode_text": "(1) 甲은 따로 살고 있는 사촌형 A로부터 ... 훔쳐 달라 ...",
  "actor_labels": ["甲", "乙", "A"],
  "cues": [
    {"cue_id": "cue.actor_age_stated",
     "factual_cue": "행위자의 나이 또는 출생 시점이 사건 사실에 적혀 있다"},
    {"cue_id": "cue.actor_mental_condition_stated",
     "factual_cue": "행위자의 정신질환, 정신적 장애, 음주 또는 약물 복용 상태가 ..."}
  ]
}
```

`actor_labels`는 Call 1.5가 이미 결박한 그 episode의 participant 목록이다. 모델이 새 인물을
만들지 못하게 하는 닫힌 집합이다. doctrine id도 조문도 없다.

### 출력 schema

```json
{
  "factual_episode_id": "factual_episode:001",
  "cue_assessments": [
    {"cue_id": "cue.coercion_against_actor_stated",
     "truth": "TRUE",
     "subject_actor_ids": ["乙"],
     "source_quote": "丙에게 범행을 함께할 것을 제안하여"}
  ]
}
```

host가 강제하는 계약(위반 시 hard-fail, repair 없음):

1. `cue_id`가 요청에 담긴 cue 집합과 **정확히 일치**(누락·추가·중복 금지).
2. `truth ∈ {TRUE, FALSE, UNKNOWN}`. TRUE가 아니면 not raised. UNKNOWN을 FALSE로 바꾸지 않고
   raw로 보존한다.
3. `subject_actor_ids ⊆ actor_labels`. 비어 있으면 not raised로 처리한다 -- 누구에 대한
   사실인지 모르는 채로 doctrine을 열면 甲의 심신장애가 乙의 죄책을 흔든다.
4. `source_quote`는 `episode_text`의 **exact substring**이어야 한다. TRUE인데 인용이 본문에
   없으면 그 cue는 reject하고 not raised로 남긴다.

## 3. cue -> doctrine -> leaf 표 (12 cue / 12 doctrine / 31 unique leaf)

| cue | doctrine | stage | leaf 수 |
| --- | --- | --- | --- |
| `actor_age_stated` | `juvenile_defeat` | culpability | 1 |
| `actor_mental_condition_stated` | `insanity_defeat` | culpability | 3 |
| `actor_hearing_or_speech_impairment_stated` | `deaf_mute_mandatory_reduction` | culpability | 1 |
| `coercion_against_actor_stated` | `coerced_act_defeat` | culpability | 3 |
| `actor_belief_of_permission_stated` | `mistake_of_law_defeat` | culpability | 2 |
| `legal_or_occupational_basis_stated` | `justifiable_act_defeat` | unlawfulness | 3 |
| `prior_force_by_other_stated` | `self_defense` | unlawfulness | 3 |
| `imminent_danger_stated` | `necessity_defeat` | unlawfulness | 4 |
| `competing_duty_stated` | `conflict_of_duties_defeat` | unlawfulness | 2 |
| `claim_enforcement_obstacle_stated` | `self_help_defeat` | unlawfulness | 3 |
| `victim_permission_stated` | `victim_consent_defeat` | unlawfulness | 4 |
| `victim_permission_unobtainable_stated` | `presumed_consent_defeat` | unlawfulness | 4 |

leaf 31개 중 `ground_fact`는 2개(`actor_age_under_14_at_act_time`, `coerced_act_performed`)이고
나머지 29개는 `legal_element`다. 두 consent doctrine이 leaf 2개를 공유한다.

**재사용 가능한 leaf는 0개다.** 31개 전부가 새 neural target이다.

## 4. KCL-26 예상 수

| 단위 | 수 |
| --- | --- |
| factual episode (전체 / instance 보유) | 43 / 38 |
| Call 1.5-D 물리 요청 | 43 (episode당 1회, cue 12개 동시) |
| episode-actor 쌍 | 55 |
| top-level instance | 87 |
| provenance를 가진 전체 instance (참가 후보 포함) | 132 |
| doctrine leaf (unique) | 31 |

증분 target 계산식:

```
targets = Σ_{raised (doctrine, actor, episode)} leaves(doctrine) × instances(actor, episode)
```

- `instances(actor, episode)` 중앙값 2, 평균 2.4, 최대 13.
- 따라서 **raised 1건의 한계비용은 leaf 수 × 약 2** -- 정당방위(leaf 3)면 약 6 target.
- 상한: 12개 cue가 모든 episode·actor에서 TRUE면 87 × 31 = **2,697** (현재 534의 5배).
- 참가 후보 instance까지 열면 132 × 31 = 4,092.

체감 예상은 문항당 raised 1~2건 수준(26문항 × 1.5 × 평균 leaf 2.8 × 2 ≈ **220 target 내외**,
534 -> 약 750)이지만, **이 숫자는 추정이므로 그대로 승인 근거로 쓰지 않는다.** Call 1.5-D를
먼저 돌려 raised 목록을 확정한 뒤 exact target 목록과 수를 다시 보고하고, 그때 Call 2 실행
승인을 받는다.

## 5. E2E lowering 경로

```text
data/v2/doctrine_raising_cues.yaml  (승인된 cue 카탈로그)
  -> Call 1.5-D  (episode당 1요청, cue 12개, 법리명 없음)
  -> DoctrineCueAssessment(cue_id, truth, subject_actor_ids, source_quote)
  -> [host] authored cue->doctrine 매핑만 적용
  -> RaisedDoctrine(case, episode, actor, doctrine_ref, raised_by_cue_ids)
  -> [planner] raised doctrine의 leaf만 target으로 materialize
       · candidate_doctrine_refs: 13 -> raised 집합으로 축소
       · ground_fact leaf는 기존 occurrence-level projection 재사용
       · legal_element leaf는 instance-local
       · opened_by="doctrine_raising_cue" 로 표시
  -> Call 2 (기존 프롬프트 그대로, target만 증분)
  -> raised_active_doctrines(...)        [기존 런타임, 수정 없음]
  -> resolve_stage effects / Scallop     [기존 경로, 수정 없음]
```

새로 만드는 코드는 세 곳뿐이다.

1. `src/idpr/v2/doctrine_cues.py` -- cue 카탈로그 파서와 출력 계약 검증.
2. `src/idpr/v2/runtime/doctrine_raising.py` -- cue assessment -> RaisedDoctrine 매핑.
   법리 내용을 모르고 표만 읽는다.
3. planner의 target 확장 -- 이번에 만든 `policy_probe_targets`와 같은 자리, 같은 방식
   (`opened_by` 표시, 이미 있는 target과 dedup).

기존 `doctrine_activation.raised_active_doctrines`와 Scallop stage effect는 **바꾸지 않는다.**
지금도 "leaf가 하나라도 non-UNKNOWN일 때만 활성화"를 요구하고 있고, 그 조건을 만족시킬
truth가 없었을 뿐이다.

## 6. 검수 카드

아래에 `> comment:`로 답해 주시면 그대로 반영한다.

---

### 카드 A. cue 12개 문구를 승인하는가

`doctrine_raising_cues.yaml`은 지금 `status: awaiting_legal_review`다. 이 파일이 승인되지 않으면
아래 전부가 진행되지 않는다. 저작 경계는 "현상적 사실만, 법적 평가 금지"이고, 예컨대
`prior_force_by_other_stated`는 "부당한 침해"가 아니라 "상대방이 먼저 유형력을 행사하였다"로
쓰여 있다. 그 평가는 leaf predicate가 Call 2에서 한다.

특히 보실 것:

- `cue.competing_duty_stated`("같은 시점에 이행해야 할 다른 의무나 요구가 함께 있었다")는
  넓다. 의무의 충돌이 아닌 단순한 사정까지 걸릴 수 있다.
- `cue.legal_or_occupational_basis_stated`("법령·직무·업무에 따라 이루어졌다")도 공무원이
  등장하는 문항 대부분에서 TRUE가 날 가능성이 있다.
- `cue.actor_age_stated`는 나이가 적혀 있기만 하면 열린다. 성인임이 명백해도 leaf
  `actor_age_under_14_at_act_time`이 FALSE로 닫히므로 결론은 안전하지만 target 1개를 쓴다.

> comment:

---

### 카드 B. cue의 적용 범위: 행위자 속성 vs 상황

지금 표에는 범위 구분이 없다. 그런데 두 종류가 섞여 있다.

- **행위자 속성**: 나이, 정신상태, 청각·언어 장애. 사건 앞머리에 한 번 적히고 그 행위자의
  모든 episode에 미친다.
- **상황**: 선행 폭력, 급박한 위험, 피해자 승낙, 직무 근거 등. 그 episode의 사실이다.

초과에서 배운 것과 같은 문제다 -- episode 일치를 일률 요구하면 앞머리에 적힌 나이가 뒤 episode의
죄에 닿지 않는다. 제안은 cue마다 `scope: actor | episode`를 저작하는 것이다.

| 제안 scope | cue |
| --- | --- |
| `actor` (그 행위자의 사건 전체) | age, mental condition, hearing/speech impairment |
| `episode` (그 episode의 그 행위자) | 나머지 9개 |

- (가) 위 표대로 `scope`를 저작한다. -- 권고.
- (나) 전부 `episode`로 둔다. 앞머리 서술이 뒤 episode에 닿지 않는다.
- (다) 전부 `actor`로 둔다. 한 episode의 정당방위 상황이 사건 전체로 번진다.

> comment:

---

### 카드 C. 참가 후보 instance에도 doctrine leaf를 열 것인가

top-level instance는 87개, 참가 후보까지 포함하면 132개다. 교사자도 심신장애일 수 있으므로
법리상 열려야 하지만, 참가 후보 대부분은 link로 성립하지 않는다(현재 49 후보 -> link 4).

- (가) v1은 top-level 87개에만 연다. 파생 가담자 instance의 doctrine은 unresolved marker로
  남긴다. -- 권고(비용 45개 instance 분 절약).
- (나) 132개 전부에 연다.

> comment:

---

### 카드 D. `doctrine.mistaken_justifying_circumstance`에 cue가 없다

registry에는 doctrine이 13개인데 cue는 12개 doctrine만 연다. 지난 세션에 저작한 위전착
(오상방위 등, culpability, leaf 2개)에 단서가 없어 **구조적으로 영원히 raised되지 않는다.**
이것이 정확히 이번에 닫으려는 dead loop와 같은 모양이다.

- (가) 이번에 cue를 함께 저작한다. 초안: "행위자가 자기를 향한 위해나 위험이 있다고 믿을
  만한 사정이 사건 사실에 적혀 있다".
- (나) 이번 범위에서 제외하고 `representation_gaps.yaml`에 명시적으로 남긴다.

> comment:

---

### 카드 E. Call 2 증분 실행 게이트

권고안: Call 1.5-D 실행(모델 호출 43회, 입력 총 9천 자 수준으로 매우 저렴) -> raised 목록과
exact target 목록·수 보고 -> 승인 -> Call 2 증분 실행. 상한을 함께 정해 두는 것이 좋다면
"증분 target이 N개를 넘으면 실행 전 재검수" 형태로 N을 정해 주시면 그대로 건다.

> comment:

---

## 7. 이번 작업에서 하지 않는 것

- participation prompt/model tuning, live Call 2 재실행 (§33 관련) -- freeze.
- optional excess foreseeability probe -- 열지 않는다.
- co_principal unreachable mode -- schema를 좁히지 않고 marker로 보존한다.
- 흡수 조건 assessment 채널 -- Call 1.5-D가 닫힌 뒤로 미룬다.
