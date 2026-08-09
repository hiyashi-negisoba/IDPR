# Predicate 사전 확장 — 배치 ④ 총칙 미수론 나머지 (제28·29조) v1

[predicate_dictionary_ext_batch04_v0.md](predicate_dictionary_ext_batch04_v0.md)에 대한 사용자
검수 5건 반영. v0는 그대로 둔다. 29조 절은 변경 없음(v0 그대로 "신규 predicate 없음"),
28조 절이 전부 다시 정리된다.

---

## 정정 1 — `PREPARATION`/`CONSPIRACY`를 별도 state로 두면 overlap 발생

**v0 오류**: 두 state를 따로 두면 같은 occurrence에서 `preparatory_conduct`와
`conspiracy_agreement`가 **동시에 TRUE**일 수 있고(물적 준비 + 합의가 함께 있는 경우가
실제로 흔함), 그러면 Gate①의 상태 도출 규칙(`|T|>=2 → unresolved`)에 걸려 예비·음모가
멀쩡히 성립한 사건도 `unresolved`가 된다. "서로 다른 leaf라서 겹치지 않는다"는 v0의
주장 자체가 틀렸다 — leaf가 다르다는 사실은 상호배타성을 보장하지 않는다.

**v1(수정)** — 28조의 법률효과(예비·음모 모두 "벌하지 아니한다"는 원칙과 처벌 시 동일한
효과)가 같으므로, state를 하나로 묶는다:

```text
PREPARATION_OR_CONSPIRACY
    when = ALL(
        ANY(preparatory_conduct, conspiracy_agreement),
        NOT(commencement_of_execution)
    )
    punishable = (offense별, 법률에 특별한 규정이 있는 죄만 true)
```

`NOT(commencement_of_execution)`을 `when`에 명시적으로 넣은 것도 이번 수정의 일부다 —
`ATTEMPTED`(25조, pilot)와의 상호배타성을 "occurrence_id가 알아서 해결해준다"는
암묵적 가정이 아니라 **`when` 조건 자체에서 명시적으로 보장**한다(정정 4 참고). 신규
primitive는 여전히 필요 없다 — `ANY`/`ALL`/`NOT` 기존 구조로 충분.

---

## 정정 2 — `preparatory_conduct`에 목적(주관 요건)을 숨기지 않는다

**v0 오류**: canonical_meaning에 "목적한 범죄를 **실현하기 위한**"을 넣어 객관적
준비행위와 주관적 목적을 한 predicate에 합쳤다 — 배치②가 확정한 "mental은 별도
predicate로 다룬다"(intent/negligence를 conduct에 섞지 않는다)는 원칙과 어긋난다.

**v1(수정)**:

```text
legal_element.preparatory_conduct              물적 준비행위를 하였다(목적 서술 제거)
legal_element.conspiracy_agreement             (v0 그대로, 이미 "합의" 자체가 행위이지
                                                목적이 아니므로 손대지 않음)
legal_element.purpose_to_commit_target_offense (신규) 그 준비행위·합의가 특정 범죄를
                                                실현하려는 목적/고의로 이루어졌다

PREPARATION_OR_CONSPIRACY.when = ALL(
    purpose_to_commit_target_offense,
    ANY(preparatory_conduct, conspiracy_agreement),
    NOT(commencement_of_execution)
)
```

목적범구조긍정설/부정설 대립(이 목적이 13조 `intent`와 같은 것인지 별도
초과주관요소인지)은 여전히 predicate 구조에 영향을 주지 않는다 — `purpose_to_commit_
target_offense`라는 하나의 leaf로 양쪽 학설을 수용하고, 실제로 13조 `intent`와
동일하게 취급할지는 2패스 저작 시 결정(v0의 "학설 대립이 구조에 영향 없음" 판단은
predicate를 분리한 지금도 유지된다).

---

## 정정 3 — 예비죄 종범 불성립을 "기존 구조가 자동 해결"이라고 단정하지 않는다

**v0 오류**: "그 offense/state에 `aider` mode를 저작하지 않으면 된다"고 확정했는데,
현재 `ParticipationPolicyDef`는 **offense 단위**로 mode를 저작하지 **Completion
state별로 mode를 껐다 켰다 하는 구조가 아니다**. 같은 offense가 `COMPLETED`/
`ATTEMPTED`에서는 방조가 가능하고 `PREPARATION_OR_CONSPIRACY`에서는 불가능해야 하는데,
이건 "offense에 aider mode를 아예 안 붙인다"로는 표현이 안 된다(붙이면 전체 state에서
방조가 가능해지고, 안 붙이면 기수·미수에서도 방조가 막혀버린다).

**v1(수정)** — 확정에서 확인사항으로 낮춘다:

```text
예비죄 종범 불성립(판례 확립)
    → Completion state별로 participation mode 가용성이 달라져야 하는 요구인데,
      현재 6C 구조(offense 단위 ParticipationPolicyDef)가 이를 자연히 지원하는지
      확정되지 않았다 — 2패스에서 실제 예비·음모 처벌 죄(내란·외환·방화·강도 등)를
      저작하며 확인한다. 확인 결과 표현 불가로 판정되면 그때 architecture-
      compatibility issue로 승격한다(33/34/35-36/19조-263조 특례와 같은 그룹).

31조 2항(교사받은 자 불착수 시 예비·음모에 준한 처벌) 연결도 같은 이유로 확정 보류,
    2패스에서 함께 확인.
```

**예비죄 공동정범 긍정(v0의 항목 1)은 정정 대상이 아니다** — 이건 "새 participation
mode가 필요한가"라는 다른 질문이고, `co_principal`은 이미 존재하는 mode라 그 결론
(신규 mode 불필요)은 유지된다. state별 가용성 문제는 아직 제기되지 않았다(공동정범을
예비·음모 단계에서 막아야 한다는 법리가 없기 때문).

---

## 정정 4 — 죄수(예비의 미수 흡수)를 `occurrence_id`로 설명하지 않는다

**v0 오류**: "예비가 미수에 흡수된다"는 법률효과를 `occurrence_id`(사실관계 identity
보존)가 처리하는 것처럼 적었는데, `occurrence_id`는 같은 사건·행위를 식별할 뿐 흡수
로직 자체를 담당하지 않는다.

**v1(수정)**: 정정 1에서 `PREPARATION_OR_CONSPIRACY.when`에 넣은
`NOT(commencement_of_execution)`이 흡수관계를 담당하는 실제 메커니즘이다 — 착수가
일어나는 순간 이 state의 `when`이 FALSE가 되어 더 이상 도출되지 않고
`ATTEMPTED`/`COMPLETED`만 남는다. `occurrence_id`는 그 준비행위와 실행행위가 같은
사건의 연속임을 식별하는 identity 문제일 뿐, 이 흡수 자체의 근거가 아니다.

---

## 정정 5 — 자수 특례를 단일 MODIFY로 뭉치지 않는다

**v0 오류**: "MODIFY effect: … 감경 또는 면제"라고 하나로 적어 MODIFY(감경)와
EXEMPT(면제)를 섞었다 — 배치③이 21-23조에서 이미 정리한 원칙(MODIFY/EXEMPT를
분리하고, 어느 조합인지는 21조의 확정된 downstream 구조를 그대로 재사용)을 여기서도
따라야 한다.

**v1(수정)**:

```text
legal_element.voluntary_surrender_before_execution   (변경 없음)

자수 특례의 구체적 형 효과("감경 또는 면제")는 21-23조 downstream 패턴과 같은 구조
(MODIFY 계열과 EXEMPT 계열을 분리)로 표현하되, 실제 어느 offense(내란·외환·폭발물
사용·방화·통화위조 예비음모)에 어떤 조합으로 적용되는지는 조문마다 다를 수 있어
2패스 저작 시 개별 확인 — 이번 배치에서는 predicate 하나만 확정하고 downstream 구조는
21-23조가 확정된 뒤 함께 정리한다.
```

---

## 배치④ v1 요약

`PREPARATION_OR_CONSPIRACY` 단일 state(신규 predicate 3개: preparatory_conduct/
conspiracy_agreement/purpose_to_commit_target_offense) + `voluntary_surrender_
before_execution`(자수, downstream 구조는 21-23조와 함께 결정)로 확정. 종범 불성립·
31조 연결은 2패스 확인사항으로 이월(architecture-compatibility 승격 가능성 열어둠).
29조는 v0 그대로. 여전히 스키마 변경 없음.
