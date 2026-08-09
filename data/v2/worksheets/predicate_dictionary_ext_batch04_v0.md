# Predicate 사전 확장 — 배치 ④ 총칙 미수론 나머지 (제28·29조) v0

[predicate_dictionary_ext_batch03_v2.md](predicate_dictionary_ext_batch03_v2.md)의 연장. 25-27조
(미수·중지·불능미수)는 이미 15개 조문 pilot에서 CompletionPolicy로 저작 완료됐다 — 이
배치는 그 축의 나머지 두 조문(예비·음모, 미수범 처벌의 일반원칙)이다. **결론부터
말하면 이번 배치는 신규 predicate가 거의 필요 없다** — 28·29조 대부분이 pilot v2가
이미 확정해둔 CompletionPolicy 패턴(state별 `when`/`punishable`)의 근거를 제공할
뿐이고, 학설 대립(발현형태설/독립구성요건설/이분설, 목적범구조긍정설/부정설)은
predicate 구조에 영향을 주지 않는다.

---

## 제28조 예비·음모

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.preparatory_conduct` | 목적한 범죄를 실현하기 위한 물적 준비행위를 하였다(예비) | Ⅲ.1 |
| `legal_element.conspiracy_agreement` | 2인 이상의 자 사이에 특정 범죄의 실행을 위한 합의가 성립하였고 그 합의에 실질적인 위험성이 인정된다(음모) | Ⅲ.1 |
| `legal_element.voluntary_surrender_before_execution` | 예비·음모한 목적범죄를 실행에 이르기 전에 자수하였다 | Ⅵ.1 |

**CompletionPolicy state로 편입** — 25-27조와 같은 패턴:

```text
PREPARATION   when = preparatory_conduct        punishable = (offense별, 법률에 특별한
                                                   규정이 있는 죄만 true — 28조 원칙)
CONSPIRACY    when = conspiracy_agreement        punishable = (offense별, 동일 원칙)

MODIFY effect: voluntary_surrender_before_execution → 형의 감경 또는 면제(자수 특례,
    내란·외환·폭발물사용·방화·통화위조 예비음모 등 조문별로 규정된 죄에만 적용)
```

신규 CompletionPolicy state 2개(`PREPARATION`/`CONSPIRACY`) 추가지만, 이건 **7차
addendum의 `states`가 이미 지원하는 구조**(`when`/`punishable`/`requires`)를 그대로
쓰는 것이라 스키마 변경이 아니다 — pilot v2가 25-27조에서 `ATTEMPTED`/
`ABANDONED_ATTEMPT`/`IMPOSSIBLE_ATTEMPT_*`를 만든 것과 같은 작업.

**신규 predicate가 아닌 것들(전부 기존 구조로 자동 커버됨) — 확인만 하고 넘어감**:

1. **예비죄의 공동정범(긍정, Ⅳ.3)**: 6C `co_principal` mode를 그대로 쓴다 — 새 mode
   불필요. 예비·음모 자체가 offense-like completion state일 뿐 participation 구조가
   달라지지 않는다.
2. **예비죄의 종범 불성립(판례 확립, Ⅳ.3)**: `participation_policy_def`에서 그
   offense/state에 `aider` mode를 아예 저작하지 않으면 된다 — "방조 불성립"을 표현할
   특수 constraint가 필요한 게 아니라, 애초에 mode를 선택적으로만 부여하는 기존
   구조가 자연히 이 결론을 낸다.
3. **예비죄의 중지범 특례 불인정(판례 확립, Ⅵ.2)**: `PREPARATION`의 `when`과
   `ABANDONED_ATTEMPT`(26조, 이미 pilot에서 저작)의 `when`은 서로 다른 leaf 조건이라
   같은 occurrence가 두 state를 동시에 도출할 수 없다 — v2 Gate①의 상태 도출 규칙
   (`|T|==1`)이 이미 이 결론을 구조적으로 보장한다. 별도 배제 규칙 불필요.
4. **예비·음모의 죄수(Ⅴ)**: 여러 준비행위가 하나의 예비/음모로 포괄되고, 실행착수
   시 예비는 흡수되어 미수/기수만 남는다 — 이것도 offense instance/occurrence 단위
   설계(Step 6A의 `occurrence_id`)로 이미 커버되는 사실관계 확정 문제이지 predicate
   설계 문제가 아니다.
5. **목적범구조긍정설/부정설(Ⅲ.1)**: "…죄를 범할 목적"이 별도 초과주관적 요소인지,
   그냥 그 목적범죄에 대한 `legal_element.intent`(13조, 배치②)와 같은 것인지의
   대립인데, `preparatory_conduct`/`conspiracy_agreement`의 canonical_meaning에
   "목적한 범죄를 실현하기 위한"이 이미 포함돼 있어 predicate 하나로 양쪽 학설을
   다 수용한다(20조 ANY 사례와 같이, 학설 대립이 구조에 영향을 안 주는 경우).

**검수 필요 — 31조(교사, pilot 완료)와의 연결.** 워크시트 Ⅵ.1이 "교사를 받은 자가
승낙하고 실행에 착수하지 아니한 때에는 교사자·피교사자를 음모 또는 예비에 준하여
처벌한다(31조 2항)"를 언급한다 — 이미 저작된 31조 교사 predicate가 이 조건(피교사자
불착수)을 표현할 수 있는지는 2패스에서 31조를 다시 열 때 확인해야 한다. 이번 배치가
새로 만들 predicate는 아니고 cross-reference로만 남긴다.

---

## 제29조 미수범의 처벌

**신규 predicate 없음.** 29조는 "미수범은 각 본조(각칙 개별 조문)에 규정이 있어야
처벌된다"는 원칙 선언인데, 이건 pilot v2의 "수정1"(`CompletionPolicy`의 `punishable`은
state별 bool, offense마다 저작 시점에 값을 매긴다)이 이미 정확히 구현하고 있는
원칙이다 — 29조가 그 근거 조문일 뿐 새로 표현할 게 없다. 확인만 하고 종료.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** `PREPARATION`/`CONSPIRACY`는 기존 `states` 구조의 신규 인스턴스일 뿐이고,
나머지는 기존 구조가 이미 답을 갖고 있음을 확인하는 배치였다. 지금까지 배치 중 가장
가벼운 배치.
