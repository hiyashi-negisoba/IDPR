# Predicate 사전 확장 — art339 강도강간 (카드 없음, 51개 조문 중 유일한 예외) v4

[predicate_dictionary_ext_art339_v3.md](predicate_dictionary_ext_art339_v3.md)에 대한
사용자 검수 2건을 반영한다. v3은 그대로 둔다 — 이력 추적용. v3의 D-1·D-2(active HOLD로
격상) 판단 자체는 맞다 — 이번 정정은 그 주변 서술 두 곳만 좁힌다.

---

## 정정 8 — 335조 F-5-1은 배치⑫에서 이미 해소·HOLD 해제됐다, 재언급 삭제

**v3 오류**: 정정7 본문과 재분류 D-2 항목·최종 상태 문단에서 335조 F-5-1을 "같은
계열의 HOLD"로 세 차례 인용했다. 그러나 `predicate_dictionary_ext_batch12_v1.md`
정정6이 이미 F-5-1을 **해제**했다 — 335는 `compose(offense, offense)`가 아니라
base_offense(329절도) 위에 목적·폭행협박 predicate를 얹은 단일 offense 구조이고,
`335.COMPLETED.when = taking_conduct`(329 predicate를 335 자신의 completion 판정
기준으로 직접 재사용)로 별도 링크 메커니즘 없이 저작이 끝났다. 339는 애초에 그 구조가
아니다 — `kind: offense` component 두 개(robbery_part, rape_part)를 진짜로 COMPOSE하는
첫 사례라서 335의 (이미 닫힌) 패턴과 계열 자체가 다르다. 닫힌 HOLD를 다시 "관련 항목"으로
불러오면 335를 다시 미확정처럼 보이게 만드는 부작용이 있다.

**v4(정정) — F-5-1·335 언급을 전부 삭제, "337·338의 기존 구조 선택 확인사항"으로만
표기.**

---

## 정정 9 — "2-pass 착수 전 반드시 해소"는 범위가 너무 넓다

**v3 오류**: D-1·D-2를 "2-pass 착수 전 반드시 해소"라고 썼다 — 이렇게 읽으면 다른
조문(총칙·이미 확정된 각칙 배치들)의 2-pass 실제 조립까지 339의 컴파일러 gap 해소를
기다려야 하는 것처럼 보인다. 그러나 확인된 건 "**339를 지금 형태로 조립할 수 없다**"는
것이지 다른 죄종의 2-pass를 막는 전제조건이 아니다.

**v4(정정) — 범위를 339 자신으로 좁힌다.**

```text
D-1·D-2는 art339의 2-pass 실제 assembly(derived_offense.robbery_rape·completion_
policy.robbery_rape의 실제 YAML 저작)를 확정하기 전에 반드시 해소해야 한다. 다른
조문의 2-pass 착수 조건이 아니다.
```

해소 방식(component-scoped 네임스페이스를 compile.py/completion.py에 신설할지, 이
COMPOSE 패턴 자체를 다른 방식으로 재설계할지)도 **지금 설계하지 않는다** — 339의
2-pass 착수 시점에 기존 구조로 우회 가능한지부터 먼저 확인하고 그때 결정한다.

---

## 최종 상태 (v4)

```text
art339 predicate vocabulary      확정
robbery-side candidate refs      확정 (333/334/335, 336은 coverage 참조만)
rape component = offense.rape[297]   확정 (component ref, 297조 predicate 수동 나열 안 함)
occasion_identity(강도의 기회)    확정 (G절 재사용)

art339 CompletionPolicy          ACTIVE HOLD — 339 자신의 2-pass assembly 확정 전
                                  반드시 해소, 다른 조문 2-pass의 전제조건 아님

  D-1. component별 commencement_of_execution 구별 불가 → 실제 발동 확인
  D-2. component별 slot suspension 불가(robbery 미수+rape 기수 표현 불가) → 실제 발동 확인

  generic element-leaf dedup 메커니즘(정정5) → 존재 확인, 339 Elements 자체에서는
  현재 미발동(mental 등 슬롯에서 robbery_part·rape_part가 겹치는 id를 안 씀)

(기존, 정정2 유지) robbery-side COMPOSE 구조(component ref 여러 개 vs 공통 base 재사용)
  — 337·338의 기존 구조 선택 확인사항과 함께 검토.
```

신규 predicate 0건 유지. D-1·D-2는 predicate가 아니라 컴파일러/런타임 설계 문제이므로
predicate 사전으로는 닫을 수 없다는 판단도 유지 — 다만 해소 시점·방식은 339의 2-pass
착수 시로 이월하고 지금 확정하지 않는다.
