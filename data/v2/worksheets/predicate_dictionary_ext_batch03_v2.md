# Predicate 사전 확장 — 배치 ③ 총칙 위법성조각사유 (제20·22·23·24조) v2

[predicate_dictionary_ext_batch03_v1.md](predicate_dictionary_ext_batch03_v1.md)에 대한 사용자
검수 1건 반영 — "과잉" doctrine의 stage 표기만 정정. 20·22조 의무의 충돌·24조는 v1
그대로.

---

## 정정 — "과잉" doctrine에 `stage = culpability 또는 punishability`라는 모호한 표기를 쓰지 않는다

**v1 오류**: `DoctrineDef.stage`는 저작 시 **하나의 구체적인 stage로 확정**돼야 하는
필드인데("또는"으로 두 후보를 남겨두는 건 스키마가 허용하지 않는 상태를 predicate
사전에 적어놓은 것과 같다), `MODIFY`와 `EXEMPT`도 서로 다른 stage effect다 — 하나의
doctrine에 애매한 stage를 붙일 수 없다.

**v2(수정)** — stage를 확정하는 대신, "21조 `excessive_defense`가 실제로 어떻게
구조화되는지"에 종속시킨다:

```text
doctrine.excessive_necessity (22조)
    Unlawfulness DEFEAT 아님 — 21조 excessive_defense와 동일한 downstream 구조를
    그대로 따른다. 21조가 MODIFY 효과와 EXEMPT 효과를 하나의 DoctrineDef 안에서
    표현하는지, 아니면 별도 두 DoctrineDef(예: excessive_defense_modify /
    excessive_defense_exempt)로 나누는지에 따라 excessive_necessity도 같은 개수·
    같은 stage로 복제한다 — 21조 2항(형 감면)·3항(야간·공포 등 불벌) 둘 다 준용하므로
    구조 전체를 복제.

doctrine.excessive_self_help (23조)
    Unlawfulness DEFEAT 아님 — 21조 구조 중 **MODIFY 계열만** 복제(형의 임의적 감면).
    21조 3항(EXEMPT 계열)에 대응하는 부분은 준용되지 않으므로 복제하지 않는다.
```

즉 이번 predicate 사전 단계에서 22·23조가 새로 stage를 정하는 게 아니라, **21조가
확정될 때 나오는 구체적 DoctrineDef 구조(개수·stage·effect)를 그대로 복제하는 관계**라는
점만 기록한다. 21조 자체의 stage 확정은 2패스에서 21·22·23조를 함께 저작할 때
이뤄진다(v1의 판단 유지).

---

## 배치③ v2 요약 — 마감

20조 3-way `ANY` 분해, 22조 의무의 충돌 Unlawfulness DEFEAT 확정, 24조
`consent_based_act_not_against_social_norms` 일반화, `statutory_bar_on_consent` 공용은
전부 v1대로 확정. 이번 정정으로 "과잉" doctrine의 stage 모호 표기만 없앴다. 신규
스키마·DSL primitive 없음. 배치③ 종료.
