# 재산죄 RuleIR 레벨(페이즈) 구조

작성일: 2026-07-26 · 상태: **조립·런타임 검증 완료** · 입력: 검토완료 core **480장** / 죄명 단위 11개
기계 판독본: `data/rulegen/property/rule_ir_phase_map.json` (`scripts/build_rule_ir_phase_map.py`, API 0회)

사용자 요청: 커버 중인 재산죄 일체에 대해 조문별 RuleIR 레벨 구조를 정리한다(기본범 → 가중범 식).
추측으로 그리지 않고 **core 480장을 레벨에 배정해** 각 레벨이 실제로 어떤 카드로 채워지는지, 어디가
비어 있는지 확인했다.

---

## 1. 레벨 정의

판단이 흘러가는 순서다. 아래 레벨은 위 레벨의 **결론을 입력으로** 받는다.

| 레벨 | 이름 | 내용 | 카드 |
|---|---|---|---:|
| **L0** | 적격·객체 | 재물성·재산상 이익·타인성·점유·주체 신분 — 무엇에 대한 누구의 죄인가 | 123 |
| **L1** | 실행행위 | 절취·강취·폭행협박·처분·손괴·취거·임무위배·청탁 | 120 |
| **L2** | 인과·귀속 | 행위와 결과의 연결, 외포·처분행위의 매개, 결과 귀속 | 3 |
| **L3** | 주관 | 고의·불법영득의사·불법이득의사·목적·인식 | 70 |
| **L4** | 단계 | 실행의 착수·기수시기·미수 | 30 |
| **L5** | 가중 | 가중유형 플래그 요건(야간·흉기·합동·상습·업무자·상해·사망·예비·준강도) | 99 |
| **L6** | 위법성·책임 | 정당행위·피해자의 승낙·권리행사 | 10 |
| **L7** | 처벌·소추 | 친족상도례(형 면제·친고죄) — **A4 절차 레이어로 이월** | 25 |

**왜 이 순서인가.** RuleIR 계약이 부정을 `case_assessment_complete` 게이트 이후 최종 스트라텀에서만
허용한다. 위법성 조각(L6)은 본질적으로 부정으로 쓰이므로(`조각되지 않았다면 성립`) 요건 층과 같은
스트라텀에 둘 수 없다. 그래서 성립을 두 단계로 나눈다.

```
<unit>_elements_satisfied(case_id, ...) :- L0 ∧ L1 ∧ L2 ∧ L3 ∧ L4 component.    // 부정 없음
<unit>_not_established(case_id, defendant_id, issue_id)                          // BAR 카드(L6 포함)
    :- satisfied_<bar card>(...).                                               //  + 필수요건 not_satisfied
<unit>_has_negative(case_id, defendant_id) :- <unit>_not_established(..., _).    // 2항 요약
<unit>_has_conflict(case_id, defendant_id) :- <unit>_conflict(..., _).
<unit>_established(case_id, ...)                                                // 유일한 부정 사용 규칙
    :- <unit>_elements_satisfied(...), case_assessment_complete(case_id, defendant_id),
       not <unit>_has_negative(...), not <unit>_has_conflict(...).
<unit>_aggravation(case_id, defendant_id, kind) :- <unit>_established(...), L5 요건.
```

**정정(2026-07-26)**: 처음에 `established :- ..., not justified`로 적었는데 계약 위반이다. 계약은
부정을 쓰는 규칙을 **하나만** 허용하고 그것이 정확히 `has_negative`·`has_conflict` 두 요약만
부정해야 한다. 따라서 **L6 위법성·책임 카드는 `justified`가 아니라 `has_negative`로 흘러간다**
(BAR 카드와 같은 경로). 이 구조는 사기 RuleIR과 동일하며, 실제 조립·런타임으로 검증됐다.

L7은 `charge`가 정해진 뒤에 붙는다 — 성립·죄명과 층이 다르다(§4).

레벨별 술어 이름은 다음 규약으로 고정한다: `eligible_object`/`standing`(L0) ·
`conduct_*`(L1) · `caused_by`(L2) · `intent_*`(L3) · `stage(case_id, defendant_id, kind)`(L4,
kind ∈ preparation | attempt | completed) · `<unit>_aggravation(kind)`(L5) · `justified`(L6) ·
`punishment_exempt`/`prosecution_requires_complaint`(L7).

## 2. 조문 19개의 역할

| 조문 | 죄명 | 역할 | 단위 | 카드 |
|---|---|---|---|---:|
| 제329조 | 절도 | **기본범** | `theft` | 40 |
| 제330조 | 야간주거침입절도 | 가중유형 → `nighttime_residential` | `theft` | 7 |
| 제331조 | 특수절도 | 가중유형 → `special` | `theft` | 9 |
| 제332조 | 상습절도 | 가중유형 → `habitual` | `theft` | 9 |
| 제342조 | 미수범 | 미수 처벌근거(단위 간 공유) | `theft` | 1 |
| 제333조 | 강도 | **기본범** | `robbery` | 42 |
| 제334조 | 특수강도 | 가중유형 → `special` | `robbery` | 7 |
| 제335조 | 준강도 | 특별유형 → `quasi` | `robbery` | 26 |
| 제337조 | 강도상해·치상 | 가중유형 → `injury` | `robbery` | 7 |
| 제338조 | 강도살인·치사 | 가중유형 → `death` | `robbery` | 10 |
| 제343조 | 강도 예비·음모 | 예비 단계 → `preparation` | `robbery` | 6 |
| 제350조 | 공갈 | **기본범** | `extortion` | 41 |
| 제355조 ① | 횡령 | **기본범** | `embezzlement` | 60 |
| 제355조 ② | 배임 | **기본범** | `breach_of_trust` | 33 |
| 제356조 | 업무상 횡령·배임 | 가중신분 → `occupational` (공유 모듈) | `occupational_status` 외 | 17 |
| 제357조 | 배임수증재 | **기본범** | `breach_of_trust_bribe` | 41 |
| 제360조 | 점유이탈물횡령 | **기본범**(별개 죄명) | `lost_property_embezzlement` | 14 |
| 제366조 | 재물손괴 | **기본범** | `property_damage` | 53 |
| 제323조 | 권리행사방해 | **기본범** | `interference_with_exercise_of_right` | 32 |
| 제328조 | 친족간의 범행과 고소 | 처벌·소추 수정요소(공유 모듈) | `relative_property_crime_exception` | 25 |

기본범 8 + 가중/특별유형 8 + 공유 수정요소 2 + 미수 처벌근거 1 = 19조문.
**가중유형 조문에서 온 카드는 전부 L5**로 배정했다 — 그 조문 자체가 가중유형을 정하기 때문이다.
제356조 17장 중 업무 개념 10장은 공유 모듈(`occupational_status`)이 되고, 업무상 보관 4장과
업무상 사무처리 3장은 각각 횡령·배임 단위의 L5로 들어간다.

## 3. 단위 × 레벨 행렬

| 단위 | L0 | L1 | L2 | L3 | L4 | L5 | L6 | L7 | 합 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `theft` | 23 | 2 | · | 11 | 2 | 26 | 2 | · | 66 |
| `robbery` | 2 | 16 | 1 | 9 | 13 | 56 | 1 | · | 98 |
| `extortion` | 6 | 23 | 2 | 3 | 6 | · | 1 | · | 41 |
| `embezzlement` | 12 | 20 | · | 26 | 1 | 4 | 1 | · | 64 |
| `breach_of_trust` | 9 | 10 | · | 12 | 2 | 3 | · | · | 36 |
| `breach_of_trust_bribe` | 17 | 17 | · | 3 | 4 | · | · | · | 41 |
| `property_damage` | 22 | 22 | · | 3 | 1 | · | 5 | · | 53 |
| `interference_with_exercise_of_right` | 23 | 6 | · | 3 | · | · | · | · | 32 |
| `lost_property_embezzlement` | 9 | 4 | · | · | 1 | · | · | · | 14 |
| `occupational_status` (공유) | · | · | · | · | · | 10 | · | · | 10 |
| `relative_property_crime_exception` (공유) | · | · | · | · | · | · | · | 25 | 25 |
| **합** | **123** | **120** | **3** | **70** | **30** | **99** | **10** | **25** | **480** |

죄명마다 무게중심이 다른 것이 그대로 드러난다.

- **절도(`theft`)는 L0가 23장**으로 압도적이다. 제329조 주석서의 본체가 Ⅱ. 타인의 재물(소유·점유)
  이고(40장 중 23장), 절취 행위 자체는 정의 두 장으로 끝난다. 절도 사건의 다툼이 대부분 "누구의 점유였나"에
  걸린다는 실무 감각과 일치한다.
- **강도(`robbery`)는 L5가 56장**이다. 기본조문 42장보다 가중·특별유형이 많다 — 준강도 26장이
  주도한다. 강도는 기본범 판단보다 유형 분기가 규칙 부담이 크다.
- **횡령(`embezzlement`)은 L3가 26장**으로 가장 두껍다. 불법영득의사가 사실상 이 죄의 승부처다.
- **손괴(`property_damage`)는 L0·L1이 22:22**로 균형이고 L6가 5장이다(효용 침해와 정당행위).
- **권리행사방해는 L0가 23/32**다. "자기의 물건이면서 타인의 점유·권리의 목적"이라는 객체 요건이
  이 죄의 거의 전부다.

## 4. 빈 레벨이 뜻하는 것

빈 칸은 규칙이 없다는 사실이고, 논문 coverage tier에 그대로 보고한다.

| 빈 레벨 | 단위 | 해석 |
|---|---|---|
| **L2 전반 (3장뿐)** | theft·embezzlement·breach_of_trust·bribe·damage·권리행사방해 | 재산죄 주석서는 인과관계를 독립 절로 두지 않고 행위 서술에 녹인다. 인과관계·객관적 귀속 일반론은 **형법총칙 주석서가 필요**하고 코퍼스에 없다 — KCL 태그 `causation`·`objective_attribution`이 이미 uncovered로 기록돼 있다. |
| L3 | `lost_property_embezzlement` | 점유이탈물횡령의 불법영득의사는 횡령 카드로 대체 판단해야 한다. 제360조 주석서가 얇다(9 chunks). |
| L4 | `interference_with_exercise_of_right` | 권리행사방해의 착수·기수 규칙이 없다. 미수 처벌조항(제322조)도 커버 밖이다. |
| L6 | bribe·breach_of_trust·점유이탈물횡령·권리행사방해 | 위법성 조각 논의가 그 죄 주석서에 독립 절로 없다. `justified` 술어는 두되 규칙이 비므로 항상 거짓이 된다. |
| L5 | `extortion` | 특수공갈(제350조의2)이 KCL 커버 밖이라 공갈은 가중유형이 없다. |
| L0·L1 | 공유 모듈 2개 | 정상이다 — 수정요소는 자기 객체·행위를 갖지 않고 기본범의 결론을 받는다. |

## 5. 배정 방법과 한계

두 단계로 배정했다.

1. **조문 역할**: 가중유형 조문(제330·331·332·334·335·337·338·342·343·356조) → L5,
   제328조 → L7.
2. **기본조문 카드**: ① 명제가 기수·미수·착수를 직접 정하면 L4(주석서가 기수시기 규칙을 '행위' 절
   안에 적어 두는 경우가 있어 절 제목만 보면 실행행위로 흘러간다), ② 그 외에는 **주석서 절 제목**을
   1차 신호로 쓰고, ③ 절 제목이 일반적일 때(총설·개설·의의·구체적 검토)만 명제 문언으로 배정한다.

절 제목을 1차 신호로 쓴 이유는 실측이다. 명제 문언만으로 배정한 첫 시도는 480장 중 166장이 L0로
쏠렸다 — 객체 명사(재물·점유)가 행위 카드에도 들어 있기 때문이다. 카드결함 감사에서도 절 제목이
명제 문언보다 강한 신호였다(같은 교훈의 두 번째 확인).

**한계**: 문언 배정분은 휴리스틱이다. L0/L1 경계(객체 요건인가 행위 요건인가)와 L2/L4 경계(인과가
기수·미수를 정하는 카드)가 특히 애매하다. 레벨은 규칙 생성 시 스트라텀 순서를 정하는 데 쓰이고
카드의 법적 의미를 바꾸지 않으므로, 경계 카드가 한 층 옆으로 가도 결론은 같다 — 다만 어느 층에서
부정을 쓰는지에는 영향이 있으므로 L6 배정 10장은 생성 후 비평에서 다시 확인한다.

## 6. RuleIR 생성에 어떻게 쓰이는가

- **스트라텀 순서**를 이 레벨로 고정한다. 레벨은 조립기(`scripts/build_property_rule_ir.py`)에서
  component 구성으로 그대로 쓰인다 — 사기가 손으로 쓴 `COMPONENT_SOURCES`(11 component) 자리에
  이 레벨 맵이 들어간다(L0→object, L1→conduct, L2→causation, L3→intent, L4→completion).
- **부정 사용 지점**이 L6·L7과 최종 결론 스트라텀으로 한정된다(계약과 일치).
- **가중 플래그**가 L5에서만 켜지므로 기본범 요건과 섞이지 않는다(preflight 4항목).
- **빈 레벨**은 생성 시 그 술어를 만들지 않는다. 규칙 없는 술어를 두면 `undetermined`가 아니라
  `not_established`로 잘못 흐른다.

관련: `rulegen_rule_ir_units.md`(단위 설계·§3.1 가중 플래그) ·
`data/rulegen/property/RuleIR_preflight_10항목.md`(승인 게이트) · `idpr_remaining_work.md` A3
