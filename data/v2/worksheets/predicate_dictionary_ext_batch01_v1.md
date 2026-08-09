# Predicate 사전 확장 — 배치 ① 총칙 책임능력·책임조각 (제9·11·12·16조) v1

[predicate_dictionary_ext_batch01_v0.md](predicate_dictionary_ext_batch01_v0.md)에 대한 사용자
검수 3건 반영. v0는 그대로 둔다 — 이력 추적용. 9·11·16조는 v0 그대로 유지(수정 없음),
12조와 **10조 참고 블록**이 이번에 바뀐다.

---

## 정정 1·2 — 12조: `coerced_act_performed`는 raw factual linkage만, self-induced는 긍정형 predicate + `NOT()` gating

**v0 오류**: `ground_fact.coerced_act_performed`의 canonical_meaning에 "구성요건에 해당하고
위법한"이라는 평가적 수식을 넣었고(→ 검수 필요 1의 causal_nexus relation 논쟁까지 만들어냄),
`coercion_not_self_induced`처럼 부정형으로 predicate 자체를 이름 지었다.

**v1(수정)**:

```text
ground_fact.coerced_act_performed
    행위자가 그 강제상태 하에서 특정 행위를 하였다
    (구성요건해당성·위법성은 그 offense 자체의 Elements/Unlawfulness가 이미 판단한다 —
    이 predicate은 "강제상태와 행위 사이의 raw factual linkage"만 담는다. 별도
    RelationDef/causal_nexus 재사용 불필요 — v0 검수 필요 1 해소.)

legal_element.self_induced_coercion
    행위자가 그 강제상태를 유책하게 자초하였다
    (긍정형으로 저작 — "not self induced"처럼 부정을 predicate 이름에 박지 않는다)

doctrine.coerced_act_defeat.requires =
    ALL(
        irresistible_coercion,
        coerced_act_performed,
        NOT(self_induced_coercion)
    )
```

부정은 predicate 자체가 아니라 `ElementExpression`(`NOT(...)`)이 담당한다 — v2가 이미
`result_not_occurred`를 삭제하면서 세운 것과 같은 원칙(부정형 predicate을 만들지 않는다)을
12조에도 그대로 적용. v0의 "검수 필요 2"(별도 exception doctrine vs 흡수)는 **흡수(위
`requires` gating)로 확정** — 별도 doctrine을 만들지 않는다.

---

## 정정 3 — 10조 참고 블록도 같은 패턴으로 소급 정정

**v0가 인용한 10조 구조(pilot v2, Gate ① 통과분)**가 이번 정정과 같은 문제를 갖고
있었다: `doctrine.actio_libera_in_causa_exception`을 "심신장애 DEFEAT/MODIFY를 다시
무력화하는" **별도 exception doctrine**으로 만들어뒀다(v0 top 참고 블록, pilot v2
Gate① "그대로 유지" 절 6번의 미해결 검수 포인트이기도 했다 — "심신장애 DEFEAT/MODIFY를
다시 무력화하는 exception의 exception이라 DoctrineDef 하나로 표현 가능한지 구조검토
필요"). 12조에서 같은 문제를 `requires` gating으로 정리했으므로, **10조도 소급해서
같은 패턴으로 정리한다** — `data/v2/definitions/`에 아직 아무것도 저작되지 않았으므로
(2패스 조립 전) 되돌릴 대상이 없고, predicate 사전 원본만 고치면 된다.

```text
legal_element.self_induced_disorder
    행위자가 그 심신장애 상태를 유책하게(자의로) 자초하였다

doctrine.insanity_defeat.requires =
    ALL(
        NOT(discrimination_capacity), -- 또는 변별·제어능력 결여의 실제 표현식
        NOT(control_capacity),
        NOT(self_induced_disorder)
    )

doctrine.diminished_capacity_modify.requires =
    ALL(
        (변별·제어능력 미약을 나타내는 조건),
        NOT(self_induced_disorder)
    )

-- doctrine.actio_libera_in_causa_exception 삭제(별도 exception doctrine 폐기)
```

**이건 이미 Gate①을 통과한 15개 pilot의 predicate 사전 내용을 바꾸는 것**이라 명시적으로
표시한다 — `predicate_dictionary_draft_v2.md` 자체는 이력 보존을 위해 손대지 않고, 이
배치01 문서가 "10조 ALIC 구조는 이 문서(batch01 v1) 기준으로 대체됐다"는 최신 판단을
담는다. 2패스 실제 저작 시 10조는 이 v1 블록을 따른다.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 여전히 기존 `LegalElementDef`/`DoctrineDef.requires`(`ALL`/`NOT`)로 전부
표현된다 — 오히려 이번 정정으로 primitive가 하나(`actio_libera_in_causa_exception`류
별도 exception doctrine 패턴) 줄었다.

---

## 배치① 최종 상태 (9·11·12·16조 + 10조 참고 정정)

9·11·16조는 v0 그대로, 12조는 위 정정 반영, 10조는 위 소급 정정 반영. 이 네 조문 +
10조 참고 블록으로 배치①을 마감한다.
