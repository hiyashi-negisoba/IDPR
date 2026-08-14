# KCL-26 답안 품질을 가로막는 전체 장애물 감사

2026-08-14. 이 문서는 아직 실행하지 않은 LLM judge 점수를 추정하지 않는다. 현재 N/P/baseline
답안과 735개 KCL rubric atom을 **생성 후에만** 대조하여, 답안이 손해 볼 수밖에 없는 구조적
하한을 찾는다. rubric 내용·개수·점수는 Call 1~3 입력으로 사용하지 않았다.

재현 artifact는 `diagnostics/kcl_quality_barriers_v1.json`, builder는
`scripts/analyze_v2_kcl_quality_barriers.py`다. crime-name과 dispute marker 검사는 의미 채점이
아닌 lexical lower bound다.

## 결론부터

현재 답안이 나쁜 이유를 "문체"나 "Gemma가 약해서" 하나로 설명할 수 없다. 더 앞단에서
**검토 대상 누락 → UNKNOWN 과다 → 법적 쟁점 route 부재 → authored 조문/법리의 writer 전달
누락**이 연쇄적으로 발생한다. P에 카드를 추가해도 이 구조를 통과하지 못하므로, P가 baseline보다
자동으로 좋아질 이유가 없다.

반대로 아직 실제 judge를 돌리지 않았으므로 "우리 답안은 낮은 점수를 받았다"고 확정할 수도
없다. 지금 말할 수 있는 것은 현재 P가 KCL 채점 요소를 명시적으로 누락하는 강한 증거가 있고,
그 상태로 judge를 돌리는 것은 시스템보다 plumbing 결함을 재는 평가가 된다는 것이다.

## P0 — 법적 결론의 입력 자체가 불완전하다

### 1. Call 2 residual UNKNOWN

guard-aware scheduling 뒤 실제로 묻는 452 target 중 TRUE 201 / FALSE 19 / UNKNOWN 232,
UNKNOWN 비율은 **51.3%**다. 그 결과 AnswerPlan 106개 결론 anchor 중 78개가 미확정으로,
미확정 비율은 **73.6%**다. dead branch는 이미 79/531을 제거하고 counterfactual 26/26 동일로
닫았지만, 남은 한 문장 evidence 문제는 결론 문구에 직접 도달한다.

actor-aware paired 실험은 context만으로 UNKNOWN 24개를 known으로 바꿨다. 이것은 원인 확인이다.
다만 known 4개 후퇴와 reviewed 반대값 1개가 있어 predicate-specific evidence scope 없이 전면
채택할 수 없다. 상세는 `v2_call2_actor_aware_232_run_review_ko.md`다.

### 2. offense/binding universe 누락

- reviewed gold DefinitionRef 86개 중 direct top-level 50개(58.1%), structural reach 65개(75.6%)
- explicit gold seed 57개 중 50개(87.7%); 주거침입·범인도피·강도·사문서위조·위계공무집행방해·
  살인/존속살해 7개가 seed 단계에서 누락
- gold occurrence action span 48/67(71.6%)
- extraneous binding proxy 12/78(15.4%)

Call 2가 잘 판정해도 universe에 올라오지 않은 죄와 행위는 답안에 들어갈 수 없다. 이는
UNKNOWN prompt보다 우선하는 recall 문제다.

### 3. participation universe 누락

수동 검수 positive participation target 23개 중 현재 universe에 올바른 형태로 존재하는 것은
13개(56.5%)이고 **10개가 질문조차 되지 않는다**. 공범 형태와 정범 종속성이 KCL 결론에서 큰
비중을 가지므로 writer가 복구할 수 없는 P0 누락이다.

## P1 — 법적 논증을 답안으로 운반하지 못한다

### 4. 진짜 법적 쟁점의 discussion route가 사실상 비어 있다

rubric상 견해 대립 서술을 요구하는 atom은 45개, 해당 case는 20/26이다. 단순 marker 하한에서
견해 대립 표현이 있는 답안은 P **2/20**, N 4/20, baseline 9/20에 불과하다.

이 차이는 Call 2 truth 정확도로 해결되지 않는다. 현재 runtime active doctrine은 self-defense
1건뿐이고, `AnswerPlan.contested_points` schema는 있지만 builder가 어떤 registry도 주입하지 않아
실행상 항상 비어 있다. 사자의 점유처럼 모델이 TRUE라고 단정해도 논점을 논해야 하므로,
`authored doctrine/reviewed card -> contested_points -> Call 3 discussion obligation`을 truth와
독립적으로 구현해야 한다.

### 5. 조문 citation이 plan에서 답안으로 사라진다

rubric이 조문을 명시적으로 요구한 38 atom에 대한 문자열 하한은 P **7/38(18.4%)**, N
14/38(36.8%), baseline 11/38(28.9%)다. P의 AnswerPlan에는 다수 governing provision이 있었지만
writer가 이를 선택적으로 누락했다. 즉 retrieval 카드의 장점 이전에 기본 조문 transport가
깨졌다.

이를 막기 위해 이번 변경에서 AnswerPlan의 authored governing provision만 deduplicate한
`required_authorities` closed list를 추가했다. 기존 26개 P plan을 재구성하면 25개 case,
총 201개 citation anchor가 생긴다. 이는 새 법리를 주입하지 않고 이미 분석에 있는 조문을
Call 3가 빠뜨리지 못하게 하는 장치다. Call 3 artifact와 manifest에는 누락 조문 수를 별도로
기록하며 답안을 host가 고치지는 않는다. final N/P 재생성 때 실제 citation recall을 다시 검증한다.

### 6. card grounding coverage가 충분하지 않다

카드 대상 560개 중 143개는 검색 근거 자체가 없다. 원인은 derived offense article 미매핑 49,
episode quote 부재 94다. 검색한 417개 중 카드가 붙은 target은 288개다. P가 N보다 나아지려면
카드 품질뿐 아니라 **카드가 필요한 target까지 도달하는 bridge와 factual quote**가 먼저 있어야
한다.

## P2 — architecture gap과 writer noise

### 7. 전역 engineering gap이 모든 사건 prompt에 반복된다

현재 네 개 representation gap이 각각 26개 전 사건의 `open_points`에 들어가 총 104회 반복된다.
그와 별개로 `UNRESOLVED_MISTAKE_BINDING`은 25/26 case에 발생한다. 이는 사건별 법적 쟁점이
아니라 시스템 구현 한계를 writer에게 전역 노이즈로 전달하는 것이다.

폭행·장물 offense family, intended/result object binding, 위법성조각사유 전제사실 착오는 실제
coverage gap이므로 숨기면 안 된다. 다만 case applicability가 저작되기 전에는 답안 prompt가
아니라 audit manifest에 남겨야 한다. 전역 gap 문자열을 법적 쟁점 대용으로 쓰는 현재 경로는
제거 대상이다.

### 8. 죄명/파생죄 coverage 하한

단순 crime-name lexical 검사는 215개 후보 언급 중 P 74(34.4%), N 70(32.6%), baseline
78(36.3%)다. 일반어·별칭·흡수 관계 때문에 이 숫자를 recall로 직접 쓰면 안 된다. 그러나 P가
baseline보다 더 많은 논점을 언급한다고 볼 증거도 없다. 위 offense seed, derived mapping,
participation 누락을 고친 뒤 semantic issue-coverage audit로 다시 재야 한다.

## 실행 우선순위와 중단 기준

```text
P0  actor-aware predicate evidence scope 승인
    + 누락 offense/participation의 downstream-impact 기준 보강
P1  authored dispute registry -> AnswerPlan contested_points
    + required_authorities writer transport 검증
P1  derived article / episode quote card bridge 보강
P2  global representation gap을 case-scoped audit로 격리
    ↓
final Call 2 한 번
    ↓
Scallop -> AnswerPlan -> N/P 한 번
    ↓
baseline 포함 blind judge
```

모든 구조적 빈틈을 완벽히 메우는 것이 목표가 아니다. 각 수정은 다음 중 하나를 실제로 바꿀
때만 production에 채택한다.

1. final responsibility
2. required final conclusion
3. authored dispute/citation discussion obligation
4. KCL semantic issue coverage

이 네 출력에 영향이 없는 결함은 limitation으로 남긴다. judge는 위 P0/P1 transport를 닫은 뒤
돌려야 최종 시스템을 평가한다.
