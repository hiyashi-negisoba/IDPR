# Predicate 사전 확장 — 배치 ① 총칙 책임능력·책임조각 (제9·11·12·16조) v0

[predicate_dictionary_draft_v2.md](predicate_dictionary_draft_v2.md)(15개 조문 pilot, Gate ① 통과)의
연장. 이 배치는 10조(심신장애, 이미 v0-v2에서 저작 완료)와 같은 Culpability 축 조문 중
나머지 4개(9·11·12·16조)를 다룬다. 형식은 pilot과 동일: `id(가칭)` / `canonical_meaning` /
근거(section_path), 조문별 "검수 필요" 절에 구조적 쟁점을 남긴다.

10조 predicate(참고, 그대로 재사용 가능한 패턴):

```text
ground_fact.mental_disorder_at_act_time        행위 당시 정신적 장애 상태
legal_element.discrimination_capacity          사물 변별능력
legal_element.control_capacity                 변별에 따른 행위 제어능력
doctrine.insanity_defeat                        변별·제어능력 모두 없으면 책임조각(DEFEAT)
doctrine.diminished_capacity_modify             변별·제어능력 미약이면 감경(MODIFY, 임의적)
doctrine.actio_libera_in_causa_exception        자의로 심신장애를 야기한 경우 책임감면 배제
```

---

## 제9조 형사미성년자 (Culpability)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `ground_fact.actor_age_under_14_at_act_time` | 행위 당시 행위자가 만 14세에 이르지 아니하였다 | Ⅱ.1 |
| `doctrine.juvenile_defeat` | 형사미성년자(만 14세 미만)는 벌하지 아니한다(DEFEAT) | Ⅱ.1 |

**검수 필요 1 — 나이 판정을 ground_fact 하나로 접어도 되는가.** 10조의 구조(raw fact +
포섭판단 legal_element 2개)와 달리 9조는 "만 14세 이상/미만"이 산술 비교라 별도
포섭판단(legal_element)이 필요 없다고 보고 `ground_fact` 하나로 접었다. 다만 워크시트
Ⅱ.1이 "만 14세에 이르렀는지 여부에 대한 판단은 사실인정의 문제"라고 명시하면서도
주민등록·가족관계등록이 절대적 근거가 아니고 증언·감정으로 확정해야 할 수도 있다고
적어, 사실인정 자체가 다툼의 대상이 될 수 있음을 보여준다 — 그래도 이건 "증거로 사실을
확정하는" 문제이지 "확정된 사실을 규범 기준에 포섭하는" 문제가 아니므로 ground_fact
유지가 맞다고 보지만, 이번 15개 pilot에는 없던 새 패턴(산술 임계값 predicate)이라 확인
받는다.

**검수 필요 2 — 포괄일죄/경합범 중 일부 기간만 미성년인 경우.** Ⅱ.1이 "포괄일죄나
경합범 중 일부가 형사미성년 상황에서 행해진 경우 그 부분만 처벌 불가"라고 명시하는데,
이건 occurrence 단위 판단(하나의 offense instance마다 별도 age 판정)을 요구하는 것으로
읽힌다 — v2.2.0 런타임의 `occurrence_id` 분리 설계와 자연히 맞아떨어지므로 별도 predicate
불필요, 저작 시 "actor_age_under_14"를 case가 아니라 occurrence 단위로 평가한다는 점만
확인.

---

## 제11조 농아자 (Culpability, 필요적 감경)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.deaf_mute_status` | 행위자가 청각기능과 언어기능을 동시에 구비하지 못한 사람(농아자)에 해당한다 | Ⅱ.1 |
| `doctrine.deaf_mute_mandatory_reduction` | 농아자의 행위이면 형을 필요적으로 감경한다(MODIFY) | Ⅱ.2 |

**검수 필요 — ground_fact가 아니라 legal_element로 분류한 근거.** 10조의
`mental_disorder_at_act_time`은 ground_fact였지만, 11조의 "농아자 해당 여부"는
워크시트 Ⅱ.1이 경계 사례를 다룬다(청각장애만 있고 발음기능 장애가 없으면 미적용,
약간의 청각장애+지능저하만으로는 미적용, 뇌졸중 후유증 언어장애만으로는 불인정) —
"청각+언어기능을 동시에 결여"라는 법적 정의에 raw fact를 포섭하는 판단이 필요해
legal_element로 분류했다. v2 typing pass 기준("이름이 아니라 canonical_meaning으로")과
일관되는지 확인 바람.

**검수 필요 — 임의적 감경(10조) vs 필요적 감경(11조) 표현.** v2가 이미 확정한 패턴은
"Culpability: MODIFY → diminished + punishability_note 자유텍스트(임의적/필요적 구분은
텍스트로)"였다(Gate ① "그대로 유지" 절 5번). 11조는 이 패턴을 그대로 따르되
punishability_note에 "필요적 감경"이라고만 적으면 되는지, 아니면 MODIFY effect 자체에
mandatory/discretionary 구분 필드가 필요한지 — 이번 배치에서 실제 사례가 2건(10·11조)이
됐으니 재확인.

---

## 제12조 강요된 행위 (Culpability, 기대가능성 부존재 DEFEAT)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.irresistible_coercion` | 저항할 수 없는 폭력이나 방어할 방법이 없는 협박(자기 또는 친족의 생명·신체에 대한 위해)에 의한 강제상태가 있었다 | Ⅱ.1 |
| `ground_fact.coerced_act_performed` | 그 강제상태 하에서 행위자가 구성요건에 해당하고 위법한 특정 행위를 하였다 | Ⅱ.1 |
| `legal_element.coercion_not_self_induced` | 그 강제상태를 행위자가 유책하게 자초한 것이 아니다 | Ⅱ.1 |
| `doctrine.coerced_act_defeat` | 강요된 행위에 해당하면 기대가능성이 없어 책임이 조각된다(DEFEAT) | Ⅱ.1 |

**검수 필요 1 — 강요와 피강요 행위 사이 "인과관계"를 별도 relation으로 뽑을지.**
워크시트가 "강요의 수단인 폭력·협박과 피강요자의 행위 사이에는 인과관계가 존재하여야
한다"고 명시한다. Step 5가 이미 `causal_nexus`라는 RelationDef 이름을 결과범
행위-결과 인과관계에 쓰고 있는데, 같은 이름을 여기(강요-행위 인과)에 재사용할지
아니면 위 표처럼 `coerced_act_performed`의 canonical_meaning 안에 "그 강제상태
하에서"를 넣어 별도 relation 없이 흡수할지 — 33/34/35-36조처럼 architecture-compatibility
검수가 필요한 수준은 아니라고 보지만(간단한 흡수로 해결 가능), 확인 바람.

**검수 필요 2 — 자초강제(self-induced coercion) 배제가 10조 ALIC과 같은 구조인가.**
워크시트가 "자초강제인 경우 강요된 행위로 볼 수 없다는 게 다수설이나, 유책성이 경미하면
항상 배제하는 게 타당하지 않다는 반론도 있다"고 학설 대립을 명시한다 — 10조의
`actio_libera_in_causa_exception`(자의로 심신장애를 야기하면 책임감면 배제)과 정확히
같은 형태의 "자초 배제" 구조다. 위 표에서는 `coercion_not_self_induced`를 doctrine의
`requires` 안에 긍정조건으로 넣었는데(10조는 별도 doctrine으로 뺐음 — ALIC exception
doctrine), 이 배치 두 조문(10·12조)에 같은 패턴이 반복되므로 **구조를 통일할지 결정
필요**: (a) 이번처럼 `requires`에 부정 조건 predicate로 흡수 vs (b) 10조처럼 별도
"self-inducement exception" doctrine으로 분리. v0의 10조 "검수 필요" 항목(둘 다 같은
질문을 미해결로 남겨뒀던 것)이 이번에 실제 반복사례로 나타난 것 — v1/v2가 HOLD로
미룬 항목이 아니라 이번에 결정이 필요하다.

---

## 제16조 법률의 착오 (Culpability, 정당한 이유 있는 경우 DEFEAT)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.awareness_of_illegality_lacking` | 행위자가 자기 행위의 위법성(사회정의·조리에 반한다는 점)을 인식하지 못하였다 | Ⅱ.1 |
| `legal_element.justifiable_ground_for_mistake` | 그 위법성 불인식에 정당한 이유가 있다(심사숙고·조회 의무를 다했음에도 회피 불가능하였다) | Ⅲ.1-Ⅲ.3 |
| `doctrine.mistake_of_law_defeat` | 위 두 요건이 모두 갖춰지면 책임이 조각된다(DEFEAT) | Ⅰ.1 |

**검수 필요 1 — "법률의 부지"와 경계를 predicate 서술에 명시해야 한다.** 판례가
반복적으로 "법률의 부지(단순히 몰랐다)는 16조의 법률의 착오가 아니다"라고 선을 긋는다
(워크시트 Ⅱ.2에 인용판례 다수). `awareness_of_illegality_lacking`의
canonical_meaning이 "단순 부지"까지 포함하는 것으로 오독되면 안 되고, "일반적으로
범죄가 되는 줄 알면서도 자신의 특수한 경우는 법령상 허용된다고 적극적으로 그릇
인식한 경우"로 좁혀야 한다 — 2패스 실제 저작(`legal_standard` 본문)에서 이 경계를
정확히 옮기는 게 중요하다는 메모.

**검수 필요 2 — 오상방위·오상과잉방위(21조 HOLD)와의 관계, 이번에도 HOLD 유지.**
v2의 pilot 검수에서 오상방위·오상과잉방위(21조 Ⅴ.2, Ⅴ.3 — 침해상황이 없는데 있다고
오인)를 "MistakeDef/variant state/신규 effect 없음, 반례 확인 시에만 architecture
issue로 승격"이라며 HOLD해뒀다. 16조 워크시트(Ⅱ.2 마지막 문단)를 직접 열람해보니
"위법성조각사유의 객관적 전제사실에 대한 착오도 엄격책임설에 따르면 간접적
위법성의 착오에 해당한다"는 학설 대립이 그대로 있다 — 즉 오상방위를 16조
`mistake_of_law_defeat`로 흡수할지, 별도 처리할지가 여전히 학설이 갈리는 지점이라는
게 원천 자료로도 확인된다. **이번 배치에서도 HOLD를 유지**하는 게 맞다고 보되(강학상
정리되지 않은 논점을 predicate 사전이 임의로 정리하면 안 된다는 v2의 원칙과 일관),
16조 doctrine이 이제 실제로 존재하므로 HOLD 해제 시 참조할 자리는 마련됐다는 점만
기록.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 9·11·12·16조 전부 기존 v2.2 DSL(`GroundFactDef`/`LegalElementDef`/
`DoctrineDef.requires`/MODIFY·DEFEAT effect)로 표현된다. 12조의 "검수 필요 2"가
구조 선택(흡수 vs 별도 exception doctrine) 문제이긴 하지만 두 선택지 다 기존
primitive 안에서 해결된다 — 신규 effect나 필드는 필요 없다.
