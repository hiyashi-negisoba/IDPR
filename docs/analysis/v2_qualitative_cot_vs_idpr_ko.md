# CoT vs IDPR-B 질적 비교 (2026-08-16)

`START_HERE.md` §4-1의 "사람이 직접 읽는 질적 비교". 자동 죄명 지표를 대체하는 것이
아니라, 그 지표가 **구조적으로 볼 수 없는 것**을 기록한다(§6).

- 답안: `experiments/v2_unknown_reduction_26/frozen_B/answers.jsonl` (sha256 8e057342…)
- 비교군: `experiments/results/cot_26_8192/chain_of_thought_outputs.jsonl`
- 형식 스캔 산출물: `experiments/v2_unknown_reduction_26/answer_form_scan/report.json`
- 재현: `python3 scripts/audit_v2_answer_form.py --out <경로>`

## 0. sealed-59 준수

§7 정책상 **답안 본문을 사람이 읽은 것은 dev 2건 중 `r10_p1_q1_ga` 한 건뿐**이다.
나머지 25건은 스크립트가 카운트만 냈고 본문은 출력하지 않았다. §2의 모든 수치는
substantive 정오 판정을 포함하지 않는다 -- 유보 표현, 죄명 중복, 조문 쌍, 죄수 표현,
분량·구조 다섯 축의 형식 통계다.

---

## 1. dev 케이스 정독 -- `kcl_criminal_r10_p1_q1_ga`

변시 10회 형사법 제1문 1.(가). 루브릭 36항목으로 26문항 중 가장 무거운 축이다.

### 사실관계 (1)

① 甲이 영상통화 중 A를 협박(신체사진 유포 고지)해 A로 하여금 스스로 가슴·음부를
만지게 함 → ② A의 아파트 1층 현관에 숨어 있다가 엘리베이터에 따라 타 얼굴을 주먹으로
2회 구타, 5층에서 계단으로 끌고 가 청테이프로 양손을 결박한 후 간음하려다 A의 애원에
**뉘우치고 범행을 단념** → ③ 끌려가던 중 뿌리치다 넘어져 발목 골절(3주).

루브릭 정답: **강제추행죄의 간접정범**(피해자를 도구로) + **성폭법위반 주거침입강간치상죄**,
양자 실체적 경합.

### 축별 수기 채점

| 축 | 항목수 | CoT | IDPR-B |
|---|---:|---:|---:|
| 강제추행 간접정범 (자수범 부정·피해자 도구·추행 정의·흡수) | 8 | 0 | 0 |
| 주거침입 (위요지·공용 엘리베이터/계단·기수시기) | 6 | 0 | 0 |
| 주거침입강간 실행착수 / 중지미수 (자의성·착수미수) | 10 | ~1.5 | 2 |
| 결과적 가중범 치상 (인과·예견가능성·기수설 대립) | 9 | ~1 | ~2.5 |
| 체포죄 · 상상적 경합 · 최종 죄수 | 3 | 0 | 0 |
| **계** | **36** | **≈2.5 (7%)** | **≈4.5 (12%)** |

이 격차는 노이즈 폭이다. **우열이 아니라 실패의 종류가 다른 것**이 이 정독의 산출물이다.

### 공통 실패 -- 배점의 절반

**주거침입을 양쪽 다 열지 않았다.** "A가 거주하는 아파트 1층 현관 … 엘리베이터를 타자
따라 들어가 … 5층에서 내린 다음 계단으로"가 원문에 그대로 있다. 이 죄 하나가 안 열려서
무너지는 항목이 14개(루브릭 2·3·13·14·15·16·17·18·19·20·26·27·33·34)로 **배점 39%**다.
우리 쪽 원인은 §6에서 **라우터 miss로 확정**됐다 -- `offense.dwelling_intrusion`은 저작돼
있고 라우터 카탈로그에도 있으며 이전 run에서는 이 문항에 실제로 결박됐다. 규칙베이스
공백이 아니다.

**에피소드 ①도 양쪽 다 실패.** 8항목짜리 축인데 CoT는 강요죄/성폭법 촬영물이용강요로
갈음했고, 우리 답안은 **이 사실관계를 언급조차 하지 않는다**. 원인은 §6에서 특정했다 --
Call 1 라우팅 miss다. 하류 탈락이 아니다.

### CoT의 실패 성격 -- 자신 있게 틀린다

- **범위 이탈**: 3대 쟁점 중 하나를 B의 사망·상해치사에 쓴다. 사실관계 (2)다. 다만 CoT는
  제1문 전문을 `question_text`로 받고 스코핑을 프롬프트 한 줄에만 의존한다
  (`src/idpr/baselines/cot.py:37`). 우리는 host가 잘라 준 입력을 받는다 --
  **공정한 비교 축이 아니므로 우리 강점으로 세지 않는다.**
- **법리를 정면으로 뒤집음**: "스스로 중단하였다 하더라도 이미 성립한 미수죄의 성립에는
  영향이 없습니다". 중지미수(제26조 필요적 감면)를 부정한다. 루브릭 최대 클러스터를
  반대로 밟았고, 그걸 "항변 배척" 절에 넣어 형식만 보면 잘 쓴 답안처럼 보인다.
- **조문 오인**: 강간상해에 제301조의2(강간등 살인·치사)를 붙였다.
- 결론이 "강간상해**미수**" -- 판례 기수설과 반대다(루브릭 30~32 정반대).

### IDPR-B의 실패 성격 -- 못 짚고 흐린다

- **조문은 전부 정확**하다. 제260①·제297·제257①·제301·제262·제13·제25①. CoT의
  제301조의2 같은 오인이 없다. 심볼릭 앵커가 값을 하는 지점이다.
- **결론 회피 3곳**: "미수 여부는 확정할 수 없다"(2회), "고의 여부에 따라 성부가 결정된다",
  "현재 사실관계만으로는 확정하기 어렵다". 그런데 원문에 **"범행을 단념하였다"**가 명시돼
  있다. 미수인지 몰라서가 아니라, completion이 UNKNOWN으로 올라온 것을 프롬프트가
  "성기 삽입 여부가 명시되지 않아"라는 산문으로 번역했다. **저작된 rape completion policy가
  있는데도** 이렇게 나온다.
- **죄수가 새어나온다**: 최종 결론에 강간죄가 2건("얼굴 때린 행위"와 "간음하려 한 행위")
  별개 항목으로 선다. planner의 occurrence 분할이 그대로 답안 항목이 됐다. 하나의 강간
  실행행위다.
- **명시적 죄수 오답 1건**: "강간죄가 성립하는 경우 폭행죄는 흡수되는 것이 아니라 실체적
  경합". 루브릭 27의 정반대다. 저작된 흡수 규칙이 2개뿐(§5)이라 심볼릭이 안 짚어 주니
  프롬프트가 자유롭게 틀렸다.
- **강간치상은 검토하고 불성립으로 닫는다.** 상당인과관계·예견가능성이라는 옳은 축을
  잡고 판례 기준을 대고 "이동 과정의 이례적 사고"라며 부정한다. 루브릭은 인정이다(28·29).
  논증은 방어 가능한 수준인데 결론이 반대 -- 우리 쪽 최선의 실패다.

---

## 2. 26문항 형식 스캔 -- substantive 정오 판정 없음

`scripts/audit_v2_answer_form.py`. 다섯 축만 본다.

| 축 | IDPR-B | CoT |
|---|---:|---:|
| 평균 분량(자) | 2,260 | 2,494 |
| 유보 표현 밀도(/1k자) | **0.80** | **0.02** |
| 유보 표현이 있는 사례 | **10 / 26** | 1 / 26 |
| 유보로 닫은 최종 결론 항목 | **10 / 43** | 0 / 42 |
| 죄명 중복 사례 | 7 / 26 (11건) | 4 / 26 (5건) |
| 조문 쌍 검사 통과 / 검사 | 66 / 67 | 41 / 43 |
| 조문 불일치 | 1 | 2 |
| 죄수 관계를 명시한 사례 | **17 / 26** | 13 / 26 |
| 평균 절 헤딩 | 12.6 | 13.2 |
| 평균 조문 인용 | **5.2** | 3.8 |
| 평균 판례 언급 | 1.1 | **1.8** |
| 평균 등장 죄명 종수 | 5.2 | 4.5 |
| 결론 열거가 없는 사례 | 8 / 26 | 9 / 26 |

### 유보율 -- 우리만의 문제이고, 소수 사례에 몰려 있다

CoT는 사실상 0이다(26건 중 1건, 1회). 우리는 10건에서 나오고 결론 항목의 23%가 유보로
닫힌다. 분포가 균등하지 않다 -- **16건은 유보가 아예 없고**, 상위 6건이 대부분을 차지한다:

```
r10_p1_q1_ga  11회 (4.50/1k)   r10_p1_q2     5회 (2.14/1k)
r13_p1_q3      6회 (3.42/1k)   r10_p1_q3_ga  6회 (1.92/1k)
r11_p2_q1_ga   6회 (2.23/1k)   r10_p2_q1     5회 (1.87/1k)
```

dev 케이스에서 확인된 대로 이것은 스타일이 아니라 **UNKNOWN의 산문 표면화**다. 유보가
몰린 사례는 앞단 UNKNOWN이 몰린 사례일 가능성이 높고, 그 대조가 우선순위 ②의 진입점이다.

### occurrence 중복 -- 우리 쪽 패턴이 더 구조적이다

건수는 7 대 4로 비슷해 보이지만 형태가 다르다. 우리 쪽 중복은 **같은 죄명이 3항목까지**
가고(`r11_p1_q1` 특수절도죄 3), 재산죄 계열에 몰린다:

```
r11_p1_q1   특수절도죄 3, 장물취득죄 2
r14_p2_q1   준강도죄 2, 절도죄 2, 특수절도죄 2
r13_p2_q1   장물취득죄 2, 절도죄 2
r10_p1_q1_ga 강간죄 2          (dev: Call 1.5 이중 binding으로 특정, §6)
r11_p2_q1_ga 제3자뇌물제공죄 2
r12_p1_q4   위증죄 2
r14_p1_q1   현주건조물방화죄 2
```

한 문항에서 세 죄명이 동시에 이중계상되는 `r14_p2_q1` 같은 형태는 문체가 아니라
**planner가 나눈 occurrence가 답안 열거로 그대로 나오는 것**이다. 다만 행위자가 여러 명인
문항에서는 같은 죄명이 정당하게 두 번 설 수 있으므로(甲의 절도, 乙의 절도), 이 카운트만으로는
누수를 확정하지 못한다. 확정에는 결론 항목의 행위자 축 대조가 필요하다 -- 우선순위 ③.

### 조문 오류 -- 양쪽 다 낮고, 이 축은 정밀도만 있다

| | 내용 |
|---|---|
| IDPR-B | `r11_p2_q1_na` 공무집행방해죄에 제137조(위계공무집행방해) 인용 |
| CoT | `r11_p2_q1_ga` 뇌물수수죄에 제130조(제3자뇌물제공) / `r14_p2_q2` 강도죄에 제334조(특수강도) |

**이 축의 재현율은 낮다.** 대조표(`data/eval/rubric_crime_article_map.json`, 124종)에 있는
죄명만 검사하므로, dev 케이스에서 사람이 잡은 CoT의 실제 오류(`강간상해(제301조의2)`)를
스캔은 못 잡았다 -- `강간상해죄`가 대조표에 없다. 따라서 위 표는 **하한**이다.
"우리가 조문에 강하다"는 dev 케이스 정독이 근거이고, 이 스캔은 그것을 반증하지 않는
수준의 증거다.

### 죄수 단정 -- 우리가 더 자주 단정하지만, 근거가 없다

17 대 13으로 우리가 더 자주 죄수를 명시한다. 그러나 dev 케이스에서 그 단정 하나가
루브릭 정반대였고, 저작된 흡수 규칙은 2개뿐이다(§5: 26문항에서 pair 1건, 그마저 UNKNOWN).
즉 **심볼릭이 죄수를 결정하는 사례는 사실상 0이고, 17건 전부 프롬프트가 자유롭게 쓴 것**이다.
"죄수는 프롬프트가 진다"는 §5의 기록이 여기서 다시 확인된다. 명시 빈도를 강점으로 읽으면
안 된다.

내역: 실체적경합 14 / 흡수 7 / 상상적경합 2 (CoT: 실체적경합 13 / 흡수 2 / 법조경합 1 /
상상적경합 1). 우리 쪽 죄수 무언급 9건, CoT 13건.

### 논증 밀도/구조

절 구조(12.6 vs 13.2)와 분량(2,260 vs 2,494)은 사실상 동률이다. 갈리는 두 축:

- **조문 인용은 우리가 37% 많다**(5.2 vs 3.8). 심볼릭에서 조문 identity를 받아 오는 구조의
  직접 효과로 보인다.
- **판례 언급은 CoT가 64% 많다**(1.8 vs 1.1). 루브릭 36항목 중 "판례의 입장을 인용하여
  설명하는지"를 요구하는 항목이 dev 케이스에서만 9개다. **이 축은 CoT가 앞선다.**
  우리는 판례 카드 396장을 가지고도 진다 -- 회수한 카드가 답안의 판례 인용으로 이어지지
  않는다. 카드가 없어서가 아니라 소비 경로가 없어서다.

---

## 3. 이 비교에서 나온 판단

1. **자동 죄명 지표가 왜 못 쓰는지 확인됐다.** §1의 실패 중 죄명 목록으로 보이는 것은
   하나도 없다 -- 중지미수 부정, 죄수 오답, occurrence 이중계상, 결론 회피 전부.
2. **질적 차이는 있고 방향이 일정하다.** CoT는 넓게 짚고 자신 있게 틀리고, 우리는 좁게
   짚고 흐리게 답한다. 루브릭이 "논리적으로 적용하는지"를 묻는 형태라 부분점수는 우리 쪽에
   여지가 더 있으나, dev 1건의 7% vs 12%로는 아무것도 결론짓지 못한다.
3. **CoT가 앞서는 축을 하나 찾았다**: 판례 인용 빈도(1.8 vs 1.1). **판례 카드 396장을 가진
   쪽이 진다.** 루브릭이 판례 인용을 항목으로 직접 배점하므로 채점에 바로 걸리는
   병목이고, 자산이 아니라 소비 경로의 문제다.

## 4. 우선순위 (§6 추적 후 개정)

1. **라우터 슬롯 낭비** -- 원래 ①(episode:001 소실)과 ④(router recall)는 같은 결함이었다.
   §6이 특정했다. 여기가 1순위다.
2. **completion UNKNOWN** -- "범행을 단념"이 명시된 사실인데 completion이 UNKNOWN인 원인.
   저작된 rape policy가 있으므로 policy 부재가 아니라 결박/평가 경로 문제다.
   유보 상위 6개 사례가 진입점이다.
3. **occurrence 누수** -- planner의 occurrence 분할이 최종 결론 열거로 나오는 것을 차단한다.
   확정에는 결론 항목의 행위자 축 대조가 선행한다(§2 중복 절). §6에서 dev 케이스의
   누수 지점은 planner가 아니라 **Call 1.5**로 특정됐다.
4. **판례 인용 소비 경로** -- 카드 396장이 답안에 도달하지 않는다(§3-3). 채점에 직접 걸린다.

## 5. 이 문서가 근거로 쓰이지 않는 것

- 26문항 정확도. §1은 1건이고 §2는 형식만이다.
- CoT와의 우열. 스코핑 조건이 다르고(§1), dev 표본이 1건이다.
- 조문 오류율의 절대값. §2의 해당 축은 하한이다.

---

## 6. 우선순위 ① 추적 결과 -- 라우터가 슬롯을 중복으로 태운다

### 결론

`factual_episode:001`은 하류에서 떨어진 것이 아니다. **Call 1이 해당 죄명을 아예 부르지
않았다.** episode:001을 여는 죄는 `offense.forcible_indecency`인데, 정본 run의 Call 1
seed 4개(`extortion`, `rape`, `injury`, `assault`)에 없다.

그리고 그 자리를 무엇이 차지했는지가 확인된다. Call 1의 raw 출력이다:

```
raw_seeds  = [extortion, rape, injury, assault, assault, assault,
              assault, assault, assault, assault]   <- 10개, 캡 포화
normalized = [extortion, rape, injury, assault]     <- 4개
```

**10슬롯 중 6개를 `offense.assault` 중복으로 태웠다.** `MAX_SEEDS_PER_CASE = 10`은 호스트
절단이 아니라 구조화 출력 스키마의 `maxItems`이므로(`src/idpr/v2/routing.py:20,127`),
모델이 스스로 캡까지 채우면서 내용 대신 반복을 넣은 것이다. 정규화는 계약 검증 **뒤**에
오므로(`normalize_router_seeds`, 같은 파일 258행) 중복을 걷어내도 잃은 슬롯은 돌아오지 않는다.

### 왜 이번 run에서 생겼나

라우터 카탈로그가 63 -> 69로 늘었고, **늘어난 6개가 정확히 이것들이다**:

```
assault, assault_causing_death, assault_causing_injury, special_assault
stolen_property_acquisition, stolen_property_custody
```

`representation_gaps.yaml`의 폭행죄 family와 장물죄 family 공백을 메운 결과다. 그리고
r10_p1_q1_ga에서 슬롯을 태운 죄명이 바로 그 신규 `offense.assault`다. temperature는 0.0이고
모델 스냅샷도 동일하므로 샘플링 노이즈가 아니다 -- **카탈로그 확장이 라우터 출력을
결정론적으로 바꿨다.**

### 범위 -- 국소적이고, 공백 메우기 자체는 이득이다

전역으로는 개선이다. 오해하면 안 된다.

| | 이전 run | 정본 run |
|---|---:|---:|
| Call 1 raw seed 총계 | -- | 131 |
| 중복 제거 후 seed 총계 | 116 | 116 |
| binding 총계 | 78 | **98** |
| 신규 6개 죄의 결박 | -- | 12 (assault 7 / assault_causing_injury 3 / stolen_property_acquisition 2) |

중복이 발생한 사례는 4/26이고 태운 슬롯은 15개(raw의 11.5%)다. 그중 **캡에 포화하면서
동시에 중복을 태운 사례가 2건**이고, 그 2건이 피해 전부다:

```
r10_p1_q1_ga  10슬롯 중 6개를 assault 중복  -> forcible_indecency, dwelling_intrusion 탈락
r10_p1_q2     10슬롯 중 6개를 assault 중복
r13_p2_q1     10슬롯 중 2개 (quasi_forcible_indecency)
r14_p1_q1      4슬롯 중 1개 (arson_of_occupied_structure)
```

`offense.dwelling_intrusion`은 전역 결박이 3 -> 4로 오히려 늘었다. 무너진 것은 이 한
문항에서다. 반면 `offense.forcible_indecency`는 **26문항 전체 결박이 1 -> 0**이 됐고,
그 1건이 r10_p1_q1_ga였다.

### 규칙베이스 공백이 아니다

두 죄 모두 저작돼 있고 라우터 카탈로그 69개에 들어 있다. 따라서 이 사례에서 §4-3의
"저작X 60건"은 원인이 아니다. **순수한 라우터 recall 결함**이다.

### 아직 하지 않은 것

수정은 Call 1의 출력 계약 또는 프롬프트를 건드리므로 **승인 게이트**에 걸린다(§7).
설치하지 않았고, 진단만 기록한다. 선택지는 세 갈래이고 성격이 다르다.

1. **캡을 distinct 기준으로 옮긴다** -- 스키마의 `maxItems`를 그대로 두되 중복이 예산을
   먹지 않게 한다. 계약 변경이고, 모델이 캡을 채우려는 성향 자체는 안 고친다.
2. **중복 발생 시 recovery 요청** -- 이미 부른 ref를 제외하고 남은 예산만큼 재요청한다.
   호스트 로직이지만 새 요청 payload이므로 프롬프트 승인이 필요하다. 4/26에만 발동한다.
3. **아무것도 안 한다** -- 전역 binding은 78 -> 98로 개선됐고 피해는 2문항이다.

세 번째를 배제하지 않는다. 다만 피해 2건 중 하나가 루브릭 36항목짜리 최대 문항이고
거기서 배점 22%가 날아갔다는 것은 기록해 둔다.

### 부수 확인 -- occurrence 누수의 발생 지점

우선순위 ③과 관련해 dev 케이스의 강간죄 이중계상 지점이 특정됐다. planner가 아니라
**Call 1.5**다. 단일 seed `offense.rape`에 대해 같은 `factual_episode:002`, 같은 행위자 甲으로
binding이 두 개(`binding:001`, `binding:002`) 나왔다. 하나의 강간 실행행위이므로 답안의
"강간죄 2건"은 이 이중 binding이 끝까지 흘러간 결과다. ③의 수정 지점은 Call 1.5의
동일 episode/동일 actor/동일 offense 중복 binding이다.

---

## 7. 우선순위 ② 추적 결과 -- 중지 사실이 요청에 실리지 않는다

### 결론

모델 undercall이 아니다. **자의적 중지를 묻는 요청에 중지 문장이 들어 있지 않다.**

`completion_policy.rape`에는 `abandoned_attempt`(중지미수)가 이미 저작돼 있고 leaf 세 개를
요구한다. Call 2가 답한 값은 이렇다.

```
legal_element.commencement_of_execution      TRUE
ground_fact.vaginal_intercourse_conduct      FALSE
legal_element.voluntary_cessation_or_prevention  UNKNOWN   <- 여기서 멈춘다
```

앞의 둘만으로 `attempted`가 성립하지만 `attempted`는 `defeated_by_state:
[abandoned_attempt]`이므로, 중지 여부가 UNKNOWN인 한 두 상태를 가를 수 없다. 답안의
"미수 여부는 확정할 수 없다"는 이 unresolved가 산문으로 나온 것이다.

### 증거는 있는데 폭이 다르다

`voluntary_cessation_or_prevention` 요청이 실제로 본 텍스트다:

```
carrier:realization:甲:factual_action:002:003:factual_action:002:002   span 257-349
  "A가 엘리베이터를 타자 따라 들어가 주먹으로 A의 얼굴을 2회 때리고
   5층에서 내린 다음 계단으로 끌고 가 미리 준비한 청테이프로 A의 양손을 묶어 반항을 억압한 후"
```

**"A가 그만두라고 애원하자 자신의 행동을 뉘우치고 범행을 단념하였다"(span 363-400)가 없다.**
이 텍스트만 보면 UNKNOWN이 맞는 답이다.

같은 instance의 actor_episode 폭 carrier에는 그 문장이 들어 있다:

```
carrier:actor_episode:甲:factual_action:002:003:factual_action:002:002   span 215-469
  ... A를 간음하려 하였으나
      A가 그만두라고 애원하자 자신의 행동을 뉘우치고 범행을 단념하였다. ...
```

Call 1.5는 이 문장을 `binding:002`의 `context_fragments`로 정확히 잡아 두었다. 소실이
아니라 **배분 문제**다. 같은 사건에서 predicate마다 폭이 갈린다:

| 폭 | predicate |
|---|---|
| `same_actor_episode` | intent, vaginal_intercourse_conduct, natural_person_victim_status, means_or_object_defect |
| `offense_realization` (기본값) | commencement_of_execution, coercive_conduct, **voluntary_cessation_or_prevention**, dangerousness |

### 원인

`data/v2/definitions/legal_elements.yaml:335`의 정의에 `evidence_scope` 필드가 **없어서**
기본값 `offense_realization`으로 떨어진다.

중지는 정의상 "하려던 것을 그만둔 것"이라 실행행위 조각(`factual_action`) 안에 있을 수
없다. 항상 그 다음 문장에 온다. 즉 이 leaf는 realization 폭에서는 **구조적으로 답할 수
없고**, 지금까지 UNKNOWN이 나온 것은 모델이 아니라 폭 설정의 결과다.

이것은 [[evidence-scope-lever-conditions]]가 듣는 조건과 정확히 일치한다 -- 사실이 같은
행위자 에피소드 안의 **다른 행위**에 있고, 법적 평가가 아니라 사실이다.

### 제안하는 수정 (정의 변경, 승인 대기)

`legal_element.intent`(57a8271), `offense.dwelling_intrusion`(4acf973)과 같은 형태의 한 줄이다.

```yaml
- id: legal_element.voluntary_cessation_or_prevention
  arguments: [{name: actor, type: entity}, {name: act, type: entity}]
  canonical_meaning: "자의에 의한 중지·결과방지(중지범)"
  legal_standard: "행위자가 외부 장애가 아닌 자의로 실행을 중지하거나 결과 발생을 방지하였는지 여부"
  evidence_scope: same_actor_episode          # <- 추가
  authority_refs: [{authority_basis: statute_text, citation: "형법 제26조"}]
```

같은 이유가 걸리는 이웃 leaf가 하나 더 있다. `legal_element.dangerousness`(불능미수의
위험성, 제27조)도 realization 폭인데, 수단·대상의 착오는 실행행위 조각 밖의 사정으로
드러나는 경우가 많다. 다만 KCL-26에서 실제로 결정적인 문항이 확인되지 않았으므로 함께
바꾸지 않고 별도 판단으로 남긴다.

### 확인하지 않은 것

이 수정이 실제로 TRUE를 끌어내는지는 Call 2 재실행 전까지 알 수 없다. 폭을 넓히면
모델이 답할 수 있게 될 뿐이고, 답이 맞는지는 별개다. 유보 상위 6개 사례 중 나머지
5건이 같은 원인인지도 아직 대조하지 않았다.

---

## 8. 우선순위 ② 정적 대조와 ③ 원인 -- 2026-08-16 후속

### ②-1. 유보 상위 나머지 5건은 같은 결함이 아니다

`scripts/audit_v2_unknown_evidence_scope.py`로 정적 대조했다. UNKNOWN 중 같은 instance의
actor_episode carrier가 더 넓었던 것을 찾고, 그중 **실행행위 뒤 텍스트가 빠진 것**만
(`trailing_gap > 0`) 따로 센다. 중지처럼 뒤에 오는 사실은 trailing 폭에서만 답할 수 있다.

전체로는 79건/19사건, trailing만으로 좁혀도 60건/15사건이 걸린다. **이 스크리닝은 판별력이
없다** -- 26문항 중 15개에서 뜨므로 "떴다"는 것이 결함의 증거가 되지 못한다. 후보 목록이다.

유보 상위 6건의 내역은 이렇다.

| 사례 | trailing 건수 | predicate (최대 gap) |
|---|---:|---|
| `r10_p1_q1_ga` | 5 | voluntary_cessation ×2, coercion_induced_causation ×2, coercion_sufficiency (+120자) |
| `r10_p1_q3_ga` | 8 | concealment_or_escape_conduct, act_directed_at_another_offender 등 (+234자) |
| `r13_p1_q3` | 3 | injury_result ×2, aggravated_result_attribution (+98자) |
| `r10_p1_q2` | 3 | injury_result ×2, aggravated_result_attribution (+9자) |
| `r10_p2_q1` | 2 | disposition_authority, property_disposition (+19자) |
| `r11_p2_q1_ga` | **0** | -- |

읽을 것 셋.

1. **`r11_p2_q1_ga`는 trailing 결함이 하나도 없다.** 유보가 6회인데 폭 문제가 아니다.
   원인이 다르고 별도 추적이 필요하다.
2. **`r10_p1_q2`(+9자)와 `r10_p2_q1`(+19자)의 gap은 무의미하게 작다.** 폭을 넓혀도 새로
   들어올 문장이 없다. 이 둘도 폭 결함으로 보기 어렵다.
3. **구조적 형제는 결과 predicate 하나뿐이다.** `injury_result`(4)와
   `aggravated_result_attribution`(3)은 중지와 같은 이유로 실행행위 뒤에 온다 -- 중한 결과는
   정의상 행위 다음이다. `r13_p1_q3`의 +98자는 실질적인 폭이다. 그러나 **원문 대조 없이는
   근거가 아니므로 이번에 바꾸지 않는다.** `dangerousness`와 같은 취급이다.

따라서 이번 수정은 `voluntary_cessation_or_prevention` 하나로 끝낸다. 26문항 중 이 predicate가
UNKNOWN인 곳은 `r10_p1_q1_ga`, `r11_p2_q1_da`, `r12_p2_q1_ga` 세 사건이다.

### ②-2. 회귀 가드가 붉게 켜졌다 (의도된 것)

정의를 바꾼 뒤 `test_carrier_contract`와 `test_evidence_scope_carrier_contract` 2건이 실패한다.
커밋된 plan artifact가 옛 정의 아래 생성돼 이 predicate를 realization 폭으로 나르기 때문이다.
가드가 artifact/정의 괴리를 정확히 보고한 것이고, **Call 1부터의 재실행으로 해소된다.**
그 전까지 전체 스위트는 `600 passed, 2 failed`다.

### ③. Call 1.5 이중 binding의 원인

같은 `(사건, episode, actor, offense)`에 binding이 둘 이상인 그룹은 **6개 / 92개 그룹**이고
초과 binding은 6개(전체 98개의 6.1%), 영향 사건은 5/26이다. 호스트에는 병합·중복제거 로직이
없다 -- `issue_binding.py`는 identity 정합성만 검증한다.

```
r10_p1_q1_ga  ep:002  rape                    focal 002:003 / 002:004   CHAINED
r10_p1_q3_ga  ep:001  bribe_delivery_receipt  focal 001:003 / 001:005   CHAINED
r14_p1_q2     ep:002  bribe_delivery_receipt  focal 002:003 / 002:005   CHAINED
r10_p1_q2     ep:001  assault                 focal 001:001 / 001:002
r11_p2_q1_ga  ep:001  bribe_giving            focal 001:004 / 001:005
r11_p2_q1_ga  ep:001  bribe_delivery_receipt  focal 001:004 / 001:005
```

**절반(3건)이 CHAINED다** -- 한 binding의 focal action이 다른 binding의 supporting action에
들어 있다. dev 케이스가 그 형태다.

```
binding:001  focal 002:003 "…계단으로 끌고 가 청테이프로 A의 양손을 묶어 반항을 억압한 후"
             supporting 002:002 "…엘리베이터를 타자 따라 들어가 주먹으로 A의 얼굴을 2회 때리고"
binding:002  focal 002:004 "A를 간음하려 하였으나"
             supporting 002:003  (= binding:001의 focal)
```

강간의 폭행과 간음 시도를 **두 개의 강간 realization**으로 연 것이다. 하나의 실행행위다.
답안의 "강간죄 2건"이 여기서 나온다.

나머지 3건은 focal이 서로 겹치지 않는다. 뇌물을 두 차례 준 경우처럼 실제로 두 죄일 수
있으므로 같은 결함으로 묶지 않는다.

### ③의 범위 -- 답안 중복의 일부만 설명한다

§2에서 답안에 죄명 중복이 있던 사건은 7개인데, binding 이중화가 있는 사건은 5개이고
**겹치는 것은 `r10_p1_q1_ga`와 `r11_p2_q1_ga` 둘뿐이다.** `r11_p1_q1`(특수절도죄 3),
`r14_p2_q1`(3종 ×2), `r13_p2_q1`, `r12_p1_q4`, `r14_p1_q1`의 중복은 binding 단계에서 오지
않는다. 행위자가 여럿이거나 파생죄 쌍일 수 있다. **③을 고쳐도 답안 중복의 대부분은 남는다.**

### ③에 대한 판단 요청

CHAINED 3건에 대한 결정론적 병합 규칙은 이렇게 쓸 수 있다: 같은
`(episode, actor, offense)` 안에서 A의 focal이 B의 supporting에 있으면 하나의 realization으로
보고, **어느 binding의 supporting에도 focal로 등장하지 않는 것**(체인의 끝)을 남기고 나머지
action을 supporting으로 흡수한다. 호스트 코드이고 모델을 부르지 않는다.

다만 "체인의 끝이 그 죄의 실행행위다"는 것은 법적 판단이다. 강간에서는 맞지만
(간음 행위가 실행행위이고 폭행은 수단), 뇌물 계열 2건에도 같은 방향인지는 확인이 필요하다.
그래서 구현하지 않고 남긴다.
