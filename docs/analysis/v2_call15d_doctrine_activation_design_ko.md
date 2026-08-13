# 검수 요청: Call 1.5-D doctrine activation 설계

2026-08-13. **설계는 검수 완료됐다.** 카드 A~E의 답변과 반영 결과가 각 카드 아래에 있다.
반영된 cue 카탈로그는 `data/v2/doctrine_raising_cues.yaml` v2(cue 14개)이고, 프롬프트 전문은
[v2_call15d_prompt_review_ko.md](v2_call15d_prompt_review_ko.md)에서 별도 검수 중이다.
모델은 아직 부르지 않았다.

## 0. 왜 이 경로가 필요한가

active doctrine은 26문항 전부에서 0이다. Scallop 결함이 아니라 dead loop다 -- closure가 13개
doctrine을 모든 사건에 후보로 열지만, 활성화는 leaf가 non-UNKNOWN이어야 하고, **그 32개 leaf를
planner가 한 번도 target으로 만든 적이 없다.** 확인했다: 현재 Call 2 truth에 저 32개 중
**0개**가 있고, planner의 `selected_predicate_refs`에도 **0개**가 있다.

그렇다고 32개를 87개 instance에 전부 여는 것은 답이 아니다. 그것만으로 target이 2,784개가
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
    {"cue_id": "cue.actor_transient_intoxication_stated",
     "factual_cue": "행위자가 그 행위 당시 음주, 약물 복용 등으로 일시적으로 ..."}
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

## 3. cue -> doctrine -> leaf 표 (검수 반영 후: 14 cue / 13 doctrine / 32 unique leaf)

| cue | scope | doctrine | stage | leaf 수 |
| --- | --- | --- | --- | --- |
| `actor_age_stated` | actor | `juvenile_defeat` | culpability | 1 |
| `actor_persistent_mental_disorder_stated` | actor | `insanity_defeat` | culpability | 3 |
| `actor_transient_intoxication_stated` | episode | `insanity_defeat` | culpability | 3 |
| `actor_hearing_or_speech_impairment_stated` | actor | `deaf_mute_mandatory_reduction` | culpability | 1 |
| `coercion_against_actor_stated` | episode | `coerced_act_defeat` | culpability | 3 |
| `actor_belief_of_permission_stated` | episode | `mistake_of_law_defeat` | culpability | 2 |
| `legal_or_occupational_basis_stated` | episode | `justifiable_act_defeat` | unlawfulness | 3 |
| `prior_force_by_other_stated` | episode | `self_defense` | unlawfulness | 3 |
| `imminent_danger_stated` | episode | `necessity_defeat` | unlawfulness | 4 |
| `competing_duty_stated` | episode | `conflict_of_duties_defeat` | unlawfulness | 2 |
| `claim_enforcement_obstacle_stated` | episode | `self_help_defeat` | unlawfulness | 3 |
| `victim_permission_stated` | episode | `victim_consent_defeat` | unlawfulness | 4 |
| `victim_permission_unobtainable_stated` | episode | `presumed_consent_defeat` | unlawfulness | 4 |
| `justifying_premise_belief_mismatch_stated` | episode | `mistaken_justifying_circumstance` | culpability | 2 |

leaf 32개 중 `ground_fact`는 2개(`actor_age_under_14_at_act_time`, `coerced_act_performed`)이고
나머지 30개는 `legal_element`다. 두 consent doctrine이 leaf 2개를, 위전착과 법률의 착오가
`justifiable_ground_for_mistake` 하나를 공유한다.

**재사용 가능한 leaf는 0개다.** 32개 전부가 새 neural target이다.

## 4. KCL-26 예상 수

| 단위 | 수 |
| --- | --- |
| factual episode (전체 / instance 보유) | 43 / 38 |
| Call 1.5-D 물리 요청 | 43 (episode당 1회, cue 14개 동시) |
| episode-actor 쌍 | 55 |
| top-level instance | 87 |
| provenance를 가진 전체 instance (참가 후보 포함) | 132 |
| doctrine leaf (unique) | 32 |

증분 target 계산식:

```
targets = Σ_{raised (doctrine, actor, episode)} leaves(doctrine) × instances(actor, episode)
```

- `instances(actor, episode)` 중앙값 2, 평균 2.4, 최대 13.
- 따라서 **raised 1건의 한계비용은 leaf 수 × 약 2** -- 정당방위(leaf 3)면 약 6 target.
- 상한: 14개 cue가 모든 episode·actor에서 TRUE면 87 × 32 = **2,784** (현재 534의 5배).
- 참가 후보 instance까지 열면 132 × 32 = 4,224. -- 카드 C에서 v1 범위 밖으로 결정했다.
- **재검수 게이트 `Δtarget ≤ 300`** (카드 E).

체감 예상은 문항당 raised 1~2건 수준(26문항 × 1.5 × 평균 leaf 2.8 × 2 ≈ **220 target 내외**,
534 -> 약 750)이지만, **이 숫자는 추정이므로 그대로 승인 근거로 쓰지 않는다.** Call 1.5-D를
먼저 돌려 raised 목록을 확정한 뒤 exact target 목록과 수를 다시 보고하고, 그때 Call 2 실행
승인을 받는다.

## 5. E2E lowering 경로

```text
data/v2/doctrine_raising_cues.yaml  (승인된 cue 카탈로그)
  -> Call 1.5-D  (episode당 1요청, cue 14개, 법리명 없음, scope도 숨김)
  -> DoctrineCueAssessment(cue_id, truth, subject_actor_ids, source_quote)
  -> [host] authored cue->doctrine 매핑과 scope만 적용
  -> RaisedDoctrine(case, actor, target_episode, doctrine_ref,
                    source_episode, projected, raised_by_cue_id, source_quote)
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

1. `src/idpr/v2/doctrine_cues.py` -- cue 카탈로그 파서와 출력 계약 검증. **구현 완료.**
2. `src/idpr/v2/runtime/doctrine_raising.py` -- cue assessment -> RaisedDoctrine 매핑.
   법리 내용을 모르고 표와 scope만 읽는다. **구현 완료.**
3. planner의 target 확장 -- 이번에 만든 `policy_probe_targets`와 같은 자리, 같은 방식
   (`opened_by` 표시, 이미 있는 target과 dedup). **Call 1.5-D 실행 후 착수.**

1~2의 회귀는 `tests/test_doctrine_cues.py` 14개가 지킨다. 특히
`test_every_authored_doctrine_has_a_raising_path`는 새 doctrine을 저작하고 cue를 잊으면
실패한다 -- 이번에 닫은 dead loop가 다시 열리지 않게 하는 잠금이다.

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

> comment: **조건부 승인.** 12개 cue를 factual raising gate로 두는 구조와 나머지 문구의 방향은
> 승인합니다. 다만 `competing_duty_stated`와 `legal_or_occupational_basis_stated`는 현재 문구가
> 너무 넓으므로 좁혀서 승인합니다. `competing_duty_stated`는 단순히 다른 요구가 있었다는
> 사실이 아니라 **행위자에게 같은 시점에 이행이 요구되는 둘 이상의 구체적 의무가 함께
> 서술되어 있는 경우**로 한정하십시오. 법적 의미의 '의무 충돌' 여부는 leaf가 판단합니다.
> `legal_or_occupational_basis_stated`는 공무원·직업인의 등장 자체가 아니라 **문제된 행위가
> 특정 법령, 직무상 권한·명령 또는 업무상 절차에 근거하여 행해졌다고 연결하여 서술된
> 경우**로 한정하십시오. `actor_age_stated`처럼 다소 넓더라도 leaf 1개로 안전하게 닫히는
> cue는 그대로 두어도 됩니다.

### 반영

두 문구를 좁혔다. 원칙은 "cue precision을 높이려 법적 판단을 집어넣지 않되, 단순 등장만으로
TRUE가 되는 lexical cue도 피한다"이며 카탈로그 주석에 명시했다.

- `competing_duty_stated` -> "행위자에게 같은 시점에 이행이 요구되는 둘 이상의 구체적 의무가
  함께 서술되어 있다"
- `legal_or_occupational_basis_stated` -> "문제된 행위가 특정 법령, 직무상 권한이나 명령, 또는
  업무상 절차에 근거하여 행해졌다고 연결하여 서술되어 있다"

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

> comment: **(가)의 취지는 승인하지만 현재 3개 actor-scope 분류는 수정 필요.** `age`와
> `hearing/speech impairment`는 actor scope로 두는 것이 맞습니다. 그러나 현재
> `actor_mental_condition_stated`는 정신질환뿐 아니라 **음주·약물 복용 상태까지 한 cue에
> 포함**하므로 actor scope로 전 사건에 전파하면 안 됩니다. 일시적 만취·약물 상태가 뒤의 별도
> 범행까지 번질 수 있습니다. 따라서 최소한 **지속적 정신상태/장애(actor scope)**와 **음주·약물
> 등 일시적 상태(episode scope)**로 분리하는 것을 권고합니다. 그 외 상황 cue 9개는 episode
> scope로 둡니다. 또한 actor-scope cue를 다른 episode에 투영할 때는 원래 cue가 관찰된
> `source_episode_id`와 실제 doctrine을 평가하는 `target_episode_id`를 분리하여 provenance를
> 보존하십시오.

### 반영 -- 이번 검수에서 가장 중요한 수정

제안대로였다면 "甲이 episode 1에서 술에 취했다"가 episode 7 범행의 insanity probe까지 열었다.
초과에서 닫은 episode scope 문제를 반대 방향으로 다시 만드는 것이었다.

`cue.actor_mental_condition_stated`를 두 cue로 분리했다. cue 수는 12 -> 13이 되고(D의 신설까지
14), 둘 다 `doctrine.insanity_defeat`를 열되 미치는 범위만 다르다.

| cue | scope |
| --- | --- |
| `cue.actor_persistent_mental_disorder_stated` | `actor` |
| `cue.actor_transient_intoxication_stated` | `episode` |

최종 actor scope는 age / persistent mental disorder / hearing-speech impairment 셋뿐이고
테스트가 그 집합을 정확히 고정한다. `RaisedDoctrine`은 `source_episode_id`와
`target_episode_id`를 따로 들고 `projected` 여부를 기록한다.

---

### 카드 C. 참가 후보 instance에도 doctrine leaf를 열 것인가

top-level instance는 87개, 참가 후보까지 포함하면 132개다. 교사자도 심신장애일 수 있으므로
법리상 열려야 하지만, 참가 후보 대부분은 link로 성립하지 않는다(현재 49 후보 -> link 4).

- (가) v1은 top-level 87개에만 연다. 파생 가담자 instance의 doctrine은 unresolved marker로
  남긴다. -- 권고(비용 45개 instance 분 절약).
- (나) 132개 전부에 연다.

> comment: **현재 v1은 (가) 승인.** 참가 후보 45개 전체에 doctrine leaf를 선제적으로 열지는
> 마십시오. 아직 participation link가 확정되지 않은 candidate에 31개 doctrine frontier를
> 확장하는 것은 비용 대비 의미가 없습니다. 다만 이를 최종 의미론으로 고정하지는 않습니다.
> 향후 **실제로 participation link가 확정되어 derivative participant instance가 생성된
> 경우에만**, 이미 얻은 actor/episode cue를 재사용하여 그 확정 instance에 doctrine leaf를 후속
> materialize하는 경로가 맞습니다. 현재는 해당 경우를 typed unresolved/deferred marker로
> 보존하십시오.

### 반영

v1은 top-level 87개에만 연다. 최종 구조는 `132개 전부`가 아니라
`participation candidate 45개 -> link 확정된 소수 instance -> doctrine leaf`이며, cue assessment는
actor/episode 단위로 보존되므로 재요청 없이 재사용할 수 있다. link가 확정됐는데 leaf가 없는
경우는 deferred marker로 남긴다.

---

### 카드 D. `doctrine.mistaken_justifying_circumstance`에 cue가 없다

registry에는 doctrine이 13개인데 cue는 12개 doctrine만 연다. 지난 세션에 저작한 위전착
(오상방위 등, culpability, leaf 2개)에 단서가 없어 **구조적으로 영원히 raised되지 않는다.**
이것이 정확히 이번에 닫으려는 dead loop와 같은 모양이다.

- (가) 이번에 cue를 함께 저작한다. 초안: "행위자가 자기를 향한 위해나 위험이 있다고 믿을
  만한 사정이 사건 사실에 적혀 있다".
- (나) 이번 범위에서 제외하고 `representation_gaps.yaml`에 명시적으로 남긴다.

> comment: **(가) 승인. 이번에 함께 닫아야 합니다.** 13개 doctrine 중 하나만 영구적으로 raising
> path가 없는 상태를 의도적으로 남길 이유가 없습니다. 다만 제시한 초안 "자기를 향한 위해나
> 위험이 있다고 믿을 만한 사정"은 실제 정당방위·긴급피난 사안까지 넓게 잡을 수 있으므로
> 수정하십시오. 권고 factual cue는 **"행위자가 공격·위험·승낙 등 자신의 행위를 허용할 수 있는
> 사실이 존재한다고 인식하였으나, 실제 사실관계에는 그 전제가 없거나 불분명하다는 서술이
> 있다"** 정도입니다. 모델은 그 불일치가 적혀 있는지만 탐지하고, 그것이 위법성조각사유의
> 전제사실 착오인지 및 정당한 이유가 있는지는 기존 doctrine leaf가 판단하게 하십시오.

### 반영

권고 문구 그대로 `cue.justifying_premise_belief_mismatch_stated`(scope `episode`)를 신설했다.
법리명은 cue에 넣지 않는 원칙을 유지했다. 이제 registry의 13개 doctrine 전부가 raising path를
가지며, `test_every_authored_doctrine_has_a_raising_path`가 그것을 회귀로 고정한다 -- 새 doctrine을
저작하고 cue를 잊으면 테스트가 실패한다.

---

### 카드 E. Call 2 증분 실행 게이트

권고안: Call 1.5-D 실행(모델 호출 43회, 입력 총 9천 자 수준으로 매우 저렴) -> raised 목록과
exact target 목록·수 보고 -> 승인 -> Call 2 증분 실행. 상한을 함께 정해 두는 것이 좋다면
"증분 target이 N개를 넘으면 실행 전 재검수" 형태로 N을 정해 주시면 그대로 건다.

> comment: **Call 1.5-D 43회 실행은 승인. Call 2는 아직 실행하지 않습니다.** Call 1.5-D 결과로
> 실제 raised set과 exact 증분 target을 산출한 뒤 다시 검수하십시오. 증분 Call 2 target의 재검수
> gate는 **N=300**으로 두는 것을 권고합니다. `Δtarget ≤ 300`이면 exact 목록 audit 후 실행
> 가능하고, `Δtarget > 300`이면 실행 전에 cue별 발화 수와 폭증 원인을 다시 검수합니다. 현재
> 추정치 약 220에 충분한 여유를 주면서도, broad cue 하나가 비정상적으로 많은 doctrine을 여는
> 경우를 잡을 수 있는 수준입니다.

### 반영

`Δtarget ≤ 300` 게이트를 채택했다. 컴퓨팅 비용만의 문제가 아니라 semantic safety gate다 --
300을 크게 넘으면 "KCL-26에서 방어법리 cue가 이렇게 많이 raised되는 게 맞나"를 먼저 의심해야
한다. Call 1.5-D 실행 자체는 승인됐으나, cue 카탈로그가 12 -> 14로 바뀌었으므로 프롬프트 전문
검수(카드 F)를 통과한 뒤에 돌린다. 지금 돌리면 artifact를 다시 버린다.

---

## 7. 이번 작업에서 하지 않는 것

- participation prompt/model tuning, live Call 2 재실행 (§33 관련) -- freeze.
- optional excess foreseeability probe -- 열지 않는다.
- co_principal unreachable mode -- schema를 좁히지 않고 marker로 보존한다.
- 흡수 조건 assessment 채널 -- Call 1.5-D가 닫힌 뒤로 미룬다.
