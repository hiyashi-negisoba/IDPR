# Predicate 사전 확장 — 배치 ⑤ 총칙 공범과 신분·간접정범 (제33·34조) — architecture-compatibility 검수 v0

[predicate_dictionary_ext_batch04_v2.md](predicate_dictionary_ext_batch04_v2.md)의 연장. 마스터
플랜(mossy-doodling-breeze.md)이 "현재 6C runtime이 직접 지원하는지 검수가 먼저 필요"라고
지정한 조문이다 — 이번 배치는 predicate 후보 제시보다 **6C `src/idpr/v2/runtime/
participation.py`를 직접 읽고 구조 적합성을 판정하는 작업**이 핵심이다. 결론을 먼저
말하면: **33조 본문은 이미 지원되고, 33조 단서와 34조(간접정범) 본체는 진짜
architecture gap이다.** 후자는 이번 배치에서 내가 결정하지 않고 선택지만 제시한다.

---

## 제33조 본문(구성적 신분/진정신분범) — architecture gap 아님, 이미 지원됨

**공동정범 경로**: `apply_attribution()`이 `attributable_slots`가 가리키는 leaf predicate를
공동정범 사이에서 `fold_any`로 병합한다. 진정신분범의 신분 predicate(예: 수뢰죄의
"공무원 지위")를 그 offense의 `attributable_slots`에 포함시키기만 하면, 비신분자
공동정범도 신분자 쪽의 TRUE가 `fold_any`로 전이되어 신분범의 공동정범 죄책을 진다 —
33조 본문이 정확히 요구하는 결과("공무원 아닌 자는 공무원과 공동정범의 죄책을 지게
된다", 워크시트 Ⅰ)를 **기존 메커니즘이 이미 만들어낸다**.

**교사·방조 경로**: `resolve_derivative_liability`의 Elements =
`principal_realization_truth(principal) AND requires`다. 신분자가 정범으로 그 신분범을
실현했다면(`principal.realization is not None` → TRUE) 비신분자 교사·방조자의 파생책임은
정범의 신분 여부를 다시 묻지 않는다 — 애초에 신분 문제가 재발생하지 않는 구조다. 33조
본문이 "비신분자도 신분범의 교사범·종범이 된다"고 하는 것과 정확히 일치.

**신규 predicate 없음.** 33조 본문이 만드는 건 predicate가 아니라 **저작 시 주의사항**이다
— 진정신분범 offense를 2패스에서 저작할 때 그 신분 predicate(공무원·업무자·재물보관자 등,
이미 각칙 카드에 있는 predicate들)를 `attributable_slots`에 반드시 포함시켜야 33조 본문이
실제로 작동한다. 빠뜨리면 axis 관련 검증으로 못 잡는 조용한 결함이 될 수 있다는 점만
기록.

---

## 제33조 특수문제(Ⅲ.3) — architecture gap 아님

**의무범(행위자관련적 신분범)**: 비신분자가 가공해도 공동정범이 성립하지 않는다는
판례(공직선거법 기부행위제한위반죄 등) — 그 offense의 신분 predicate를
`attributable_slots`에 **넣지 않으면** 자동으로 이 결론이 나온다. 별도 배제 규칙 불필요.

**자수범**: 간접정범·공동정범이 아예 성립할 수 없는 범죄 유형(강간죄, 위증죄 등 논란) —
그 offense의 `participation_policy`에서 `co_principal` mode를 저작하지 않으면 된다.
배치④에서 이미 확인한 "mode는 offense 단위로 선택적 부여"(예비죄 종범 불성립 논의) 패턴
그대로.

---

## 제33조 단서(가감적 신분/부진정신분범, 책임개별화) — **architecture-compatibility 검토 필요**

워크시트 Ⅵ.1의 예: 아들(직계비속, 신분자)이 어머니(비신분자, 남편에 대해서는 신분 없음)로
하여금 자기 아버지(=아들의 직계존속)를 살해하도록 교사한 경우, 판례·다수설은 **아들은
존속살해죄 교사범**의 죄책을 진다고 본다 — 정범(어머니)이 실현한 건 보통살인(어머니에게는
존속살해의 신분이 없으므로)인데, 교사자(아들)는 **자신의 신분**을 기준으로 더 무거운
죄(존속살해교사)를 진다.

**이게 기존 `resolve_derivative_liability`와 충돌한다.** 현재 구조는 교사자의 파생책임을
`principal_realization_truth(principal)` — **정범이 실제로 실현한 그 offense**(위 예에서는
보통살인)에 고정한다. 정범이 보통살인을 실현했다면 교사자도 "그 offense"에 대한 교사
파생책임만 얻을 수 있고, **정범이 실현하지 않은 다른(더 무거운) offense에 대한 교사
책임을 별도로 얻는 경로가 없다.** 즉 "각 참가자가 자기 고유의 가중/감경 신분에 따라
서로 다른 DerivedOffenseDef를 각자 평가받는다"는 33조 단서(책임개별화)의 요구를 지금
구조가 표현할 수 있는지가 불확실하다.

**신규 predicate는 필요 없다** — 존속살해의 "직계비속" 신분 predicate는 이미 있다(각칙
카드). 문제는 predicate가 아니라 **`resolve_derivative_liability`가 교사자를 어느
offense/DerivedOffenseDef에 대해 평가할지를 정범이 아니라 교사자 자신의 신분으로 정할 수
있는가**라는 runtime 구조 질문이다. 2패스에서 실제로 시도해보고, 안 되면 architecture
issue로 승격 — 이번 배치에서 미리 해법을 확정하지 않는다.

---

## 제34조 간접정범 — **확인된 architecture gap. 새 participation mode가 없다**

`participation_policy_def.schema.json`을 직접 확인했다: `modes`는
`additionalProperties: false`로 **`co_principal`/`instigator`/`aider` 세 키만
허용한다**(`principal`은 정책 자체가 없는 기본값). 간접정범에 대응하는 5번째 mode가
스키마에 없다.

**왜 기존 `instigator`/`aider`로도 안 되는가 — 정확히 반대 방향의 요구다.**
`principal_realization_truth`는 `principal.realization is not None`일 때만 TRUE를
반환한다(정범이 실제로 그 죄를 성립시켰을 때). 그런데 34조의 간접정범은 **피이용자가
"어느 행위로 인하여 처벌되지 아니하는 자 또는 과실범으로 처벌되는 자"일 때만** 성립한다
— 책임무능력, 고의 없음, 위법성조각, 목적·신분 결여 등으로 피이용자 자신의 죄책이
**성립하지 않을 때** 이용자가 정범으로 처벌된다. 피이용자를 `resolve_derivative_liability`의
`principal` 자리에 넣으면 `principal_realization_truth`가 FALSE(elements/unlawfulness
gate가 fails)를 반환하고, 그러면 이용자의 파생책임도 `AND`로 묶여 FALSE가 된다 —
**정확히 34조가 요구하는 것과 반대의 결과**가 나온다. 기존 instigator/aider 파생책임
로직은 "정범이 성공해야 공범도 성립"인데, 간접정범은 "피이용자가 실패해야(불처벌)
이용자가 성립"이다.

**신규 predicate 후보(구조와 무관하게 필요)**:

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.instrumentalization_of_agent` | 이용자가 처벌되지 아니하는 자 또는 과실범으로 처벌되는 자를 도구로 이용하여 범죄행위의 결과를 발생하게 하는 이용행위(교사 또는 방조 형태)를 하였다 | Ⅱ.2 |
| `legal_element.agent_unpunished_or_negligent` | 피이용자의 행위가 구성요건해당성·위법성·책임 중 어느 하나가 없어 불처벌이거나, 과실범으로만 처벌된다 | Ⅱ.1 |

**구조 선택지 — 이번 배치에서 결정하지 않고 제시만 한다**:

```text
(a) 새 participation mode "indirect_principal" 신설
    participation_policy_def.schema.json에 4번째 mode 추가, `attribution_mode`도
    `derivative_mode`도 아닌 제3의 basis(피이용자 실패를 조건으로 하는 역방향 파생)가
    필요 — 스키마 변경.

(b) 간접정범을 participation mode가 아니라 이용자 자신의 offense Elements로 흡수
    (mode = 그냥 principal, 별도 참가 모드 불필요)
    `legal_element.instrumentalization_of_agent`를 이용자 자신의 conduct predicate로
    저작해 이용자를 direct principal처럼 평가한다 — 34조 다수설(정범설)과 부합.
    다만 34조 1항이 "교사 또는 방조의 예에 의하여 처벌한다"고 명시(방조 형태면 필요적
    감경)하므로, 처벌 단계에서 이 conduct predicate가 교사/방조 중 어느 형태였는지에
    따라 다른 MODIFY effect를 걸어야 한다 — Punishability MODIFY로 흡수 가능한지 확인
    필요(35-36조 누범과 유사한 "MODIFY로 흡수 가능한가" 성격의 검토, 배치⑥에서 같은
    패턴 재확인 예정).

(c) 피이용자 쪽에 새로운 3치 판정 함수 추가
    `principal_realization_truth`의 반대 방향("피이용자가 확정적으로 불처벌인가")을
    읽는 별도 함수를 만들고, 이를 조건으로 하는 새 derivative mode 유형 추가 — (a)의
    변형.
```

**신규 스키마 변경 여부는 이번 배치에서 결정하지 않는다.** (b)가 스키마 변경 없이 표현
가능하다는 점에서 매력적이지만, "정범 개념을 교사·방조 형(처벌수위)으로 처벌한다"는
34조 1항의 명문 규정을 Punishability MODIFY 하나로 정확히 흡수할 수 있는지는 2패스에서
직접 저작해봐야 확인된다.

---

## 제34조 2항(특수교사·방조, 지휘·감독자 가중) — 34조 1항 구조에 종속

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.supervisory_relationship` | 이용자가 자기의 지휘·감독을 받는 자임을 인식하고 그 자를 교사 또는 방조하였다 | Ⅳ.2 |

처벌효과("교사인 때 형의 장기·다액 1/2 가중, 방조인 때 정범의 형")는 34조 1항이 위
(a)/(b)/(c) 중 어느 구조로 확정되는지에 종속된다 — 이번 배치에서는 predicate 후보만
제시하고 downstream 구조는 34조 1항이 결정된 뒤 함께 정리.

**자수범은 34조에도 동일 원칙**: 자수범 offense는 간접정범 mode/predicate 자체를 그
offense에 저작하지 않는다(33조와 같은 "선택적 부여" 패턴).

---

## 배치⑤ 요약 — 이번 트랙에서 가장 중요한 발견

33조 본문·특수문제는 architecture gap이 아니라는 게 확인됐고(신규 predicate 없음,
저작 시 주의사항만), **33조 단서(책임개별화)와 34조(간접정범) 본체는 6C 코드를 직접
읽고 확인한 실제 architecture gap**이다 — 계획서가 "검수 필요" 그룹으로 지정한 게
정확했다는 게 이번에 실증됐다. 두 곳 다 이번 배치에서 predicate 후보(신규 스키마
불필요한 것들)만 제시하고, 구조 결정(특히 34조의 새 participation mode 신설 여부)은
사용자 판단을 기다린다.
