# Predicate 사전 확장 — 배치 ③ 총칙 위법성조각사유 (제20·22·23·24조) v1

[predicate_dictionary_ext_batch03_v0.md](predicate_dictionary_ext_batch03_v0.md)에 대한 사용자
검수 3건 반영. v0는 그대로 둔다. 20·24조가 바뀌고, 22·23조는 "과잉" doctrine의 stage
분류만 정정된다.

---

## 정정 1 — 제20조: `act_pursuant_to_law_or_business`를 두 leaf로 분리

**v0 오류**: 하나의 predicate 안에 이미 "법령에 의한 행위 OR 업무로 인한 행위"라는 OR가
숨어 있었다 — compositional DSL 취지에 안 맞고, `ANY`가 이미 있으니 굳이 leaf 안에서
암묵적으로 결합할 이유가 없다.

**v1(수정)**:

```text
legal_element.act_pursuant_to_law            법령에 의한 행위에 해당한다
legal_element.act_due_to_legitimate_business 정당한 업무로 인한 행위에 해당한다
legal_element.act_not_against_social_norms   (v0 그대로) 사회상규에 위배되지 아니하는 행위

doctrine.justifiable_act_defeat.requires =
    ANY(act_pursuant_to_law, act_due_to_legitimate_business,
        act_not_against_social_norms)
```

세 predicate가 각자 자기 `legal_standard`/provenance를 독립적으로 갖는다(Ⅱ절 법령행위
사례군과 Ⅲ절 업무행위 사례군이 서로 다른 근거를 갖고 있었으므로 애초에 분리돼 있어야
맞다). 신규 primitive 없음 — 기존 `ANY`만으로 표현.

---

## 정정 2 — 제22·23조: "과잉" doctrine은 Unlawfulness DEFEAT가 아니다

**v0 오류**: `doctrine.excessive_necessity`/`doctrine.excessive_self_help`를 마치
`necessity_defeat`/`self_help_defeat`와 같은 Unlawfulness 축 DEFEAT doctrine인 것처럼
같은 절에 나열했다. 구조적으로 틀렸다 — 과잉피난·과잉자구행위는 애초에 상당성 요건을
못 채워 Unlawfulness가 **defeat되지 않은** 상태이고, 그 다음 단계(21조
`excessive_defense`가 이미 쓰는 것과 같은 MODIFY/EXEMPT downstream 효과)로 넘어가는
doctrine이다.

**v1(수정)** — stage를 정정:

```text
doctrine.necessity_defeat            stage = unlawfulness (DEFEAT)   — 변경 없음
doctrine.self_help_defeat            stage = unlawfulness (DEFEAT)   — 변경 없음

doctrine.excessive_necessity         stage = culpability 또는 punishability
                                      (21조 excessive_defense와 동일한 downstream
                                      MODIFY/EXEMPT 패턴 재사용 — 신규 설계 아님)
doctrine.excessive_self_help         stage = culpability 또는 punishability
                                      (excessive_necessity와 같은 downstream이되
                                      MODIFY만 있고 EXEMPT 변형 없음 — v0의 "21조
                                      2항만 준용, 3항 미준용" 확인은 그대로 유지)
```

**정확한 stage(culpability vs punishability)는 아직 확정된 적이 없다** — 21조
`excessive_defense`도 predicate 사전 v0-v2 단계에서는 "정황에 따라 형 감면·불벌"이라고만
서술됐을 뿐, 실제 `DoctrineDef.stage`를 배정하는 건 2패스 실제 저작(`data/v2/definitions/`)
때다. 이번 정정의 의미는 "22·23조의 과잉 doctrine을 Unlawfulness DEFEAT로 잘못
분류하지 않는다"까지이고, culpability/punishability 중 어느 쪽인지는 21조
`excessive_defense`를 2패스에서 저작할 때 **셋이 함께** 정한다(21조도 아직 미정이므로
22·23조가 21조를 따라갈 것이 아니라 셋을 동시에 결정).

**22조 의무의 충돌(`conflict_of_duties_defeat`)은 정정 대상이 아니다.** 이건
`bundle.omission_bundle`(Elements)이 성립한 뒷단에서 실제로 Unlawfulness를 DEFEAT하는
doctrine이 맞다 — v0가 "2패스 확인사항"으로 낮춰 적었던 것을 정정한다: **자연스럽게
연결되고 별도 architecture 검토가 필요 없다.**

---

## 정정 3 — 제24조: 추정적 승낙에서 `consent_not_against_social_norms` canonical_meaning 불일치

**v0 오류**: `doctrine.presumed_consent_defeat`가 24조의
`legal_element.consent_not_against_social_norms`("그 승낙 및 승낙에 의한 행위가
사회상규에 반하지 않는다")를 그대로 재사용했는데, 추정적 승낙에는 **현실적 승낙 자체가
없다** — "그 승낙"이 가리킬 대상이 없어 canonical_meaning이 실제로는 안 맞는 predicate를
빌려 쓴 것이다.

**v1(수정)** — canonical_meaning을 현실적/추정적 승낙 양쪽을 포괄하도록 일반화하고
id도 그에 맞춘다:

```text
legal_element.consent_based_act_not_against_social_norms
    현실적 또는 추정적 승낙을 기초로 한 법익침해가 윤리적·도덕적으로 사회상규에
    반하지 아니한다

doctrine.victim_consent_defeat.requires =
    ALL(valid_consent_by_disposer, harm_caused_pursuant_to_consent,
        NOT(statutory_bar_on_consent),
        consent_based_act_not_against_social_norms)

doctrine.presumed_consent_defeat.requires =
    ALL(presumed_consent, actual_consent_unobtainable,
        NOT(statutory_bar_on_consent),
        consent_based_act_not_against_social_norms)
```

`statutory_bar_on_consent`는 v0 그대로 양쪽에서 재사용한다 — "법률상 승낙 자체에 효과를
안 주는 특별규정이 있는가"는 승낙이 현실적이든 추정적이든 같은 질문이라 canonical_meaning
불일치가 없다(사용자 확인).

---

## 배치③ v1 요약

정정 3건 전부 반영. 20조는 predicate 3개(분리), 22·23조는 doctrine stage 재분류(신규
predicate 없음), 24조는 predicate 1개 명칭·의미 통일. 신규 스키마·DSL primitive는
여전히 없음 — 21조 `excessive_defense`의 downstream 패턴을 그대로 재사용한다.
