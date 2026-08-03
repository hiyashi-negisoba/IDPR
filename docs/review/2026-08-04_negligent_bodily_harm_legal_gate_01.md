# 과실치사·업무상과실치사상 RuleIR 일괄 법률검수 게이트 01

대상은 현재 카드 자산의 제267조·제268조 85장 전부다. 카드별 판정은 다음 세 문서에
있으며 고유 카드 85/85, 누락 0, 중복 0이다.

- `p2/negligent_bodily_harm_proposal_01.md`: 제267조·고의경계·결정 C 17장
- `p2/negligent_bodily_harm_proposal_02.md`: 업무상과실 39장
- `p2/negligent_bodily_harm_proposal_03.md`: 중과실·죄수 29장

승인 전에는 승인 원장, RuleIR 또는 SCL에 편입하지 않는다.

## G-N01 — 카드별 판정

85장 표의 `decision / role / component / join / track / refers_to`를 일괄 승인하는가?
수정할 카드 번호만 제시해도 된다.

## G-N02 — 세 track과 역할 tuple

다음 구조를 승인하는가?

| track | 의미 | 상속 |
|---|---|---|
| `ordinary` | 제267조 과실치사 | - |
| `occupational` | 제268조 업무상과실치사상 | `ordinary`의 `absence_of_intent`, `pre_person_exclusion` placement만 선택 상속 |
| `gross` | 제268조 중과실치사상 | 위 공통 placement와 `occupational::general_requirements`, 죄수 placement만 선택 상속 |

- 역할 tuple: `negligent_bodily_harm_case_roles(case_id, defendant_id, victim_id)`
- `gross`는 `occupational`의 자식이 아니다. 중과실에는 업무자 지위가 필요하지 않으므로
  `business_status`나 업무상 `duty_breach`를 상속하지 않는다.

## G-N03 — 제268조 공통 일반요건

#25를 다음처럼 언래핑하여 업무상과실과 중과실이 공유하는 `general_requirements`로 쓰는
것을 승인하는가?

> 형법 제268조의 죄가 성립하려면 과실, 행위자 이외의 다른 사람의 사망 또는 신체상 상해
> 결과, 그리고 과실과 결과 사이의 인과관계가 충족되어야 한다.

원문은 제268조 해설에서 “본죄”라고 표현한다. `occupational`은 여기에 업무성·업무상
주의의무·상당인과관계를 추가하고, `gross`는 중과실 정도를 추가한다.

## G-N04 — 차단규칙의 범위

다음을 승인하는가?

- 갑작스러운 버스 바퀴 진입 #7은 발견·회피 불가능 부분만 `duty_breach` bar
- 신뢰원칙 #39는 특별사정 없는 숙련 철도작업자에 대한 신뢰 부분만 bar
- 허용된 위험 #23·#28·#35, 수평적 의료분업 #26은 `occupational`만 차단
- 중과실 부정사례 #58·#62·#65·#67·#69는 `gross`만 차단
- 불법업무 배제 #85는 결정 C에 따라 `occupational::business_status`만 차단하고,
  일반 과실치상은 현재 범위 밖이므로 `predicate_ir_missing`

## G-N05 — 고의경계와 죄수의 보존

다음을 승인하는가?

- #2 고의부재와 #84 현실적 회피노력을 실행 component로 두어 세 track이 공유
- 살인·상해 고의를 한 문장에 묶은 #83은 하나의 boundary로 만들지 않고 라우터
  `context_only`로 보존. 실제 고의 죄명은 등록된 살인·고의상해 unit이 별도 평가
- #13·#14·#31·#50·#70~82는 `post_outcome`; outcome bridge 전에는 미컴파일
- 외부 교통·산업안전·중대재해·제266조 참조는 가짜 fallback 없이
  `predicate_ir_missing`

## 응답 형식

전부 동의하면 `G-N01~N05 승인`으로 충분하다. 수정이 있으면
`G-N04: #39 context_only`처럼 게이트와 카드 번호만 적어도 된다.
