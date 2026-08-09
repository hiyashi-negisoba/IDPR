# Predicate 사전 확장 — 배치 ⑥ 총칙 누범 (제35·36조) — architecture-compatibility 검수 v0

[predicate_dictionary_ext_batch05_v3.md](predicate_dictionary_ext_batch05_v3.md)의 연장이자
**총칙 predicate 사전 확장의 마지막 배치**. 마스터플랜이 "35-36조는 architecture-
compatibility 검수 대상(Punishability의 기존 `MODIFY` effect로 표현 가능한지)"이라고
지정했다. 결론: **35조는 표현 가능(architecture gap 아님), 36조는 애초에 이 트랙의
predicate 대상이 아니다**(순수 절차 조문).

---

## 제35조 누범 — Punishability MODIFY로 표현 가능, architecture gap 아님

배치②(negligence_bundle)의 원칙(여러 종류의 사실을 한 leaf에 합치지 않는다)을 적용해
전범 요건을 쪼갠다 — 실효/사면/복권마다 판정 기준이 다른 촘촘한 판례군이 있어(Ⅰ.1) 한
predicate로 뭉치면 그 예외 판단들이 뭉개진다.

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `ground_fact.prior_sentence_of_imprisonment_or_greater` | 전범에서 금고 이상의 형(유기징역·유기금고, 사형·무기형이 감형된 경우 포함)을 선고받았다 | Ⅰ.1 |
| `legal_element.prior_sentence_still_effective` | 그 형 선고의 효력이 실효·일반사면 등으로 상실되지 않았다(복권·특별사면은 효력을 상실시키지 않으므로 유효 유지) | Ⅰ.1 |
| `ground_fact.prior_sentence_execution_completed_or_exempted` | 전범의 형 집행이 종료되었거나 면제되었다(집행유예·선고유예·가석방 기간 중은 해당 없음, 가석방 기간 경과·집행유예 취소 후 복역종료는 해당) | Ⅰ.1 |
| `legal_element.subsequent_offense_within_recidivism_period` | 후범(금고 이상에 해당하는 선고형의 죄, 실행의 착수시 기준)이 전범의 형 집행종료·면제 후 3년 이내에 행해졌다 | Ⅰ.2 |
| `doctrine.recidivism_modify` | 위 요건이 모두 갖춰지면 형을 가중한다(Punishability stage, MODIFY, 장기의 2배까지, **필요적**) | Ⅱ.1, Ⅱ.2 |

```text
doctrine.recidivism_modify
    stage = punishability
    requires = ALL(
        prior_sentence_of_imprisonment_or_greater,
        prior_sentence_still_effective,
        prior_sentence_execution_completed_or_exempted,
        subsequent_offense_within_recidivism_period
    )
    effect = MODIFY(aggravated)
    punishability_note = "필요적 가중, 법정형 장기의 2배까지(특별법상 단기까지
        가중되는 경우는 별도)" — 배치①의 "임의적/필요적은 punishability_note
        자유텍스트로 구분" 패턴 재사용, 신규 필드 불필요.
```

**"후범이 금고 이상에 해당하는 죄"는 별도 predicate가 아니다.** 이건 그 offense_ref
자체의 법정형 속성(이미 정의에 내재)이지 사건마다 달라지는 사실이 아니다 —
`subsequent_offense_within_recidivism_period`의 canonical_meaning에 조건절로만 남기고
독립 leaf로 만들지 않는다.

**architecture 판정 — gap 아님.** 전과 사실은 "이 사건과 다른 사건의 결과를 참조"하는
게 아니라, **이 사건의 피고인에 대한 배경 사실**(다른 case-time fact와 동일한 층위)일
뿐이다 — 배치⑤가 발견한 "cross-actor/cross-offense symbolic dependency" 문제와는
성격이 다르다(다른 actor의 살아있는 evaluation을 참조하는 게 아니라, 그냥 이 actor에
대한 과거사실 ground_fact/legal_element). `DoctrineDef.stage=punishability`와 기존
`MODIFY` effect로 충분히 표현된다 — 마스터플랜의 "검수 필요"가 긍정적으로 해소됐다.

---

## 제36조 판결선고 후의 누범발각 — 이 트랙의 predicate 대상 아님

**신규 predicate 없음, HOLD도 아니고 범위 밖으로 명시 분류한다.** 36조는 "재판 확정
**후**에 누범 사실이 발각된 경우, 형사소송법 절차(검사가 최종 판결법원에 재판 청구,
법원 결정, 즉시항고 불가·보통항고만 가능)에 따라 **이미 선고된 형을 다시 정하는**"
순수 절차 조문이다(워크시트 Ⅲ). 이건:

```text
35조 recidivism_modify
    "이 사건" 평가 중에 형을 정하는 문제 → resolve_liability의 Punishability
    stage에서 다룬다.

36조
    "이미 끝난 사건"의 형을 재판 확정 후 절차로 다시 정하는 문제 → resolve_liability가
    평가하는 단일 사건-시점 파이프라인 밖의 별도 사법절차. IDPR v2.2.0의 stage 대수
    (Elements/Unlawfulness/Culpability/Punishability)가 다루는 "이 행위가 유죄인가,
    형이 얼마인가" 판단이 아니라 "이미 내려진 판단을 절차적으로 수정하는" 별도
    메커니즘이다.
```

마스터플랜이 형사소송법(001671, 5,373 chunk) 전체를 범위 밖으로 확정한 것과 같은
이유("절차법 stage 대수 부재") — 36조는 형법전 안에 있지만 성격상 그 형사소송법
범위와 같다. Band A-hold(1-8조, Applicability/Jurisdiction stage 부재)와도 다르다 —
"대응하는 stage가 아직 없어서 보류"가 아니라 **애초에 이 파이프라인이 다루는 종류의
질문이 아니라서 대상이 아니다**. 재검토가 필요해지면(예: 재심·형집행 관련 확장이
생기면) 그때 별도 트랙.

---

## 배치⑥ 요약 — 총칙 트랙 종료

35조 1개 doctrine(`recidivism_modify`, 5 predicate) 확정, architecture gap 아님으로
판정 — 마스터플랜의 우려가 긍정적으로 해소된 유일한 "검수 필요" 조문이다(33/34조는
실제 gap이 있었던 것과 대조). 36조는 범위 밖으로 명시 분류. **이걸로 총칙 26개
Band A-core 조문(9-34) + Band B의 35-36조 전체 predicate 후보 제시가 끝났다** — 남은
건 각칙 배치⑦-⑫(44개 조문) + art339 직접 저작이다.
