# Call 2 초literal 판정 후보와 prompt-policy 승인안

2026-08-14. residual UNKNOWN 232개 중 occurrence/episode/full-case 세 arm에서 모두 UNKNOWN이었던
93개를 다시 검수했다. 목표는 UNKNOWN을 일괄 제거하는 것이 아니라, **명시된 사실에 통상적인
언어·법적 포섭을 적용하면 방향이 정해지는데도 "직접 적혀 있지 않다"는 이유로 멈춘 target**만
C 후보로 올리는 것이다.

활성 `prompts/v2_call2_grounding*.md`는 변경하지 않았다. 아래 문언은 실행 전 승인용 초안이다.

## 정본 packet

- candidate review: `diagnostics/overliteral_candidate_review_26_v1.json`
- downstream impact: `diagnostics/overliteral_downstream_impact_26_v1.json`
- candidate sha: `76005b7584acc14b4557f5520973238787f6676cd4486c199617447680c6a1eb`
- impact sha: `b98fa78de644722321348bb23c9b27b83b80c45c1fc728caf8568c2c848a28d2`

## 93개에서 C로 올린 범위

| tier | 수 | 계약 |
| --- | ---: | --- |
| `C_HIGH` | **10** | 원문이 predicate 방향을 거의 직접 고정 |
| `C_PROBABLE` | **7** | 통상적인 법적 추론 한 단계가 더 필요 |
| C로 승인하지 않음 | **76** | placement/role, 정의 오류, 부재 기반 부정, 인과·점유 등 실제 법적 검토가 섞임 |

counterfactual truth는 TRUE 10 / FALSE 7이다. 이는 gold patch가 아니라 revised policy가 17개를
전부 의도한 방향으로 해소한다는 **상한 측정**이다.

`C_HIGH`의 대표는 다음과 같다.

- `RU-059`: 피해자는 협박을 받고 신고했으며 재산 처분을 하지 않았다.
  `property_disposition=FALSE`.
- `RU-095`: 진정문서를 바꾼 것이 아니라 새 허위 평가서를 작성했다.
  `alteration_of_genuine_document=FALSE`.
- `RU-114`: 현관문을 열고 들어가 침실에서 자는 사람을 살해했다.
  `dwelling_or_managed_premises_object=TRUE`.
- `RU-191`: 전달받은 3천만 원 중 2천만 원을 임의 소비했다.
  `self_benefit_purpose=TRUE`.
- `RU-192/193`: B가 자기 돈 3천만 원을 수술비라는 말에 속아 빌려줬다.
  `disposition_authority/property_disposition=TRUE`.
- `RU-209`: 피해자를 넘어뜨린 뒤 발로 밟아 6주 골절상을 냈다.
  `injury_intent=TRUE`.

반대로 다음은 C 수치에 넣지 않았다.

- 흉기나 수단결함이 언급되지 않았다는 이유만으로 FALSE를 만드는 경우
- 다른 actor의 실행행위를 participant에게 복사해야만 풀리는 경우
- 사자의 점유, 다단계 인과관계, 강도 폭행 정도처럼 법적 논증이 필요한 경우
- 이미 고친 giver/recipient bribe predicate identity 오류
- 잘못 열린 offense candidate를 prompt로 억지 판정하는 경우

즉 revised policy가 허용할 것은 **명시 사실의 통상적 포섭**이지 closed-world 추론이나 법적
논쟁의 은폐가 아니다.

## downstream upper bound

동결된 guard-aware Call 2에 participation truth를 동일하게 병합하고 candidate truth만 바꿨다.
기존 mode 충돌 `r12_p2_q1_ga`는 양 arm에서 동일하게 typed quarantine했다. 현재 registry를 두
arm에 똑같이 사용했으므로 production lineage가 아니라 delta 진단이다.

| | `C_HIGH` 10 | `C_HIGH + C_PROBABLE` 17 |
| --- | ---: | ---: |
| symbolic output 변화 | 5문항 | 7문항 |
| final responsibility 변화 | **0** | **0** |

realization-link blocker 2개를 양쪽에 똑같이 채운 뒤 AnswerPlan을 비교하면 24개 공통 문항 중
analysis가 바뀌는 문항은 8개다. required-final conclusion이 바뀌는 것은 **2문항**이다.

1. `r14_p1_q2` 丙 증뢰물전달죄: 미확정 -> 불성립
   (`self_benefit_purpose=TRUE`가 자기이득 목적 수수를 배제)
2. `r14_p2_q1` 乙 강도치상죄: 미확정 -> 불성립
   (`injury_intent=TRUE`가 결과적 가중범 대신 고의 상해 route를 남김)

따라서 C는 final-responsibility set 전체를 바꾸는 큰 트랙은 아니지만, 두 required conclusion의
"미확정"을 정당한 불성립으로 바꿀 수 있는 essay-quality 영향이 있다. 반면 17개를 gold로
채워도 나머지 결론 대부분은 다른 UNKNOWN 때문에 그대로다. 이 결과로 full 452-target prompt
재실행을 바로 승인하지 않는다.

## 활성 prompt 최소 변경안

현재 문언의 핵심 충돌은 다음 둘이다.

```text
occurrence 문자열 ... 에서 직접 확인되거나 필연적으로 도출되는 사실만 사용한다.
문항의 다른 부분, 일반적인 사건 추측, 상식으로 보충한 사실은 사용하지 않는다.
```

아래 세 bullet로 최소 교체하는 안을 제안한다.

```text
- occurrence 문자열 또는 명시된 question assumption에 적힌 사실과, 그 사실에
  canonical_meaning/legal_standard를 적용한 통상적인 언어적·법적 포섭만 사용한다.
  원문에 predicate의 법적 명칭이나 결론어가 그대로 없다는 이유만으로 UNKNOWN을 반환하지 않는다.
- 금지되는 보충은 원문에 없는 사건, 행위, actor, 대상, 관계 또는 동기를 새로 만드는 것이다.
  다른 문항 부분·다른 occurrence·일반적 사건 추측은 계속 사용하지 않는다.
- FALSE는 명시 사실이 predicate를 적극적으로 배제하거나 서술된 경과와 양립할 수 없을 때만
  반환한다. 단순히 언급이 없다는 이유로 FALSE를 만들지 않으며, 필요한 사실이 빠졌거나
  합리적인 법적 견해가 갈리면 UNKNOWN을 유지한다.
```

GroundFact의 `직접 뒷받침/직접 부정` 규칙은 그대로 둔다. 이번 수정의 주된 대상은
LegalElement 포섭이며, actor-local GroundFact·source-binding 계약을 느슨하게 하지 않는다.

## 승인 뒤 실행 계약

1. production prompt를 먼저 교체하지 않는다.
2. exact 17 target만 동일 evidence·동일 batching으로 control/current와 candidate/revised 두 arm 실행.
3. C_HIGH에서 intended direction과 반대되는 TRUE<->FALSE가 하나라도 생기면 기각한다.
4. C 외 residual target을 추가 표본 검수하여 closed-world FALSE와 D 소거가 없는지 확인한다.
5. 통과해도 full Call 2는 아직 돌리지 않고 D dispute route와 함께 final lineage에서 한 번만 실행한다.

## 실행 후 판정

승인된 exact-target 진단을 B_SAFE episode subset과 합쳐 49-target 2×2로 실행했다. 정본은
`docs/analysis/v2_call2_uncertainty_factorial_49_run_review_ko.md`다.

- candidate prompt는 occurrence-scope C 17개를 하나도 바꾸지 못했다.
- mixed evidence에서도 C intended agreement는 1/17 -> 2/17에 그쳤다.
- B target에서 TRUE -> UNKNOWN 1, TRUE -> FALSE 1 부작용이 있었다.

따라서 이 문서의 prompt 수정안은 **기각**한다. production prompt는 변경하지 않는다. 반면 현행
prompt + attribution-safe episode evidence는 B 32개 중 25개를 의도한 known 값으로 복구했고
반대 known 값은 0이었다. 후속 소유권은 prompt가 아니라 actor-aware realization carrier다.

## 후속 검증에서 발견한 review-label 오류와 추가 기각

후속 typed-context 및 quote-validated deliberative 진단에서 B packet의 `counterfactual_truth`를
원문·rubric과 다시 대조한 결과 최소 두 라벨이 잘못되었음을 확인했다.

- `RU-049 for_the_offenders_benefit`: 丙이 乙에게 도피자금 1천만 원을 건넸고 rubric도 이를
  범인도피죄의 적극적 도피 원조로 요구한다. 기존 packet의 FALSE가 아니라 TRUE 방향이다.
- `RU-093 solicitation_received`: 甲이 丙에게 제3자 乙 지원을 먼저 요구한 사실이다. 甲이
  청탁을 *받은* 사실로 보는 기존 packet TRUE는 predicate 방향과 맞지 않는다.

따라서 위의 `25/32`, `반대 known 0`은 당시 packet에 대한 재현 수치일 뿐 법적 정답 정확도로
사용하지 않는다. B 32 target whitelist의 production 채택은 철회한다.

현행 계약을 유지하고 typed context 설명만 추가한 최소 prompt의 232-target paired 결과도
occurrence TRUE/FALSE/UNKNOWN 39/13/180, context 63/9/160이었다. UNKNOWN 25개가 known으로
이동했지만 FALSE->TRUE 직접 역전 2개와 검수상 잘못된 `foreseeability=FALSE`가 남았다.

exact evidence quote, 포섭 basis, 한 문장 application을 강제한 49-target deliberative 진단은
TRUE/FALSE/UNKNOWN 22/4/23, packet agreement 21/49, opposite-known 5였다. quote provenance를
검증해도 모델의 predicate 경계 혼동은 사라지지 않았다. 따라서 긴 rationale이나 단순 prompt
완화도 production 해법으로 채택하지 않는다.

후속 production 소유권은 다음 둘이다.

1. predicate definition에 다른 법적 층위와 혼동하면 안 되는 `semantic_exclusions`를 저작한다.
2. evidence 확대는 case whitelist가 아니라 definition-level `evidence_scope`가 허용한 predicate의
   초기 UNKNOWN에만 적용한다. 기존 known truth는 fallback이 덮어쓰지 못한다.
# 2026-08-14 인간 전문가 승인: 불법영득의사와 동의 착오의 분리

`legal_element.unlawful_appropriation_intent`는 권리자를 배제하고 재물을 경제적 용법에 따라
이용·처분하려는 **의사 자체**를 뜻한다. 처분권자의 동의가 있다고 착오했더라도 이 경제적
이용·처분 의사는 TRUE로 평가하고, 동의 착오가 범죄 성립에 미치는 효과는 기존
mistake/doctrine route에서 별도로 처리한다. 따라서 동의 착오만을 근거로 이 predicate를
FALSE로 내리는 것은 인접 법효과의 오귀속이다.

## semantic-boundary 49-target 승인 게이트: production fallback 기각

위 경계와 기존 검수 correction을 넣은 quote-validated deliberative 진단을 동일 49 target에
적용했다. 32개까지 진행된 partial artifact에서 `RU-095 alteration_of_genuine_document`는
FALSE로 교정되고 `RU-049 for_the_offenders_benefit`는 사실관계에 맞는 TRUE를 유지했다.
그러나 `RU-093 solicitation_received`에서 세 번 연속 반환한 evidence quote가 허용된 typed
carrier의 exact substring이 아니어서 host validator가 실행을 중단했다.

- artifact: `diagnostics/deliberative_grounding_49_semantic_boundaries_v2.json`
- 완료: 32/49, TRUE 13 / FALSE 3 / UNKNOWN 16
- 종료 사유: `RU-093` exact-quote validation 3회 실패
- 판정: **typed UNKNOWN fallback은 production에 채택하지 않는다.**

Definition Layer의 `semantic_exclusions`는 predicate 의미 경계로 유지하되 사건 truth를 제공하지
않는다. `evidence_scope`와 typed context builder는 실험·준비 인프라로 남기며, 활성 Call 2의
UNKNOWN을 덮어쓰는 경로에는 아직 연결하지 않는다. host merge 계약은 이미 known인 TRUE/FALSE를
fallback이 덮어쓰는 것을 오류로 거부한다.
