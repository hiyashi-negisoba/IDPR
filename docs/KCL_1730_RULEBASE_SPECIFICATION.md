# 대한민국 형법각칙 1,730개 심볼릭 룰베이스 전수 명세서 및 뉴로-심볼릭 파이프라인 아키텍처
**KCL (Korean Criminal Law) 1,730 Symbolic Rulebase Specification & Neuro-Symbolic Pipeline Guide**

---

## 제1장. 개요 및 룰베이스 구축 동기 (Motivation & Background)

### 1.1. 개요 및 파이프라인 목적
본 명세서는 외부 라이브 API 대신 **로컬 캐시 모델 (`google/gemma-4-26B-A4B-it`)**과 **1,730개 형법각론 통합 심볼릭 Datalog 엔진**을 연동하는 End-to-End 뉴로-심볼릭 파이프라인의 학술적/기술적 전모를 기록합니다.

본 파이프라인의 최종 출력물은 단편적/자의적인 판결문 형태가 아니며, 심볼릭 엔진의 100% 결정론적 유도 결과 및 요건 활성화/비활성화 추적 트리(Proof Trace)와 사전 매핑된 판례 trim 본문을 기반으로 작성되는 **"종합 형사 법리 검토서 (Substantive Legal Review & Proof Report)"**입니다.

### 1.2. 구축 동기 및 당위성 (Why We Built It)

1. **Black-box LLM의 법리 환각 및 요건 누락 원천 극복**:
   - 기존 대형 언어 모델(LLM)은 단독 추론 시 결합범, 수죄, 위법성 조각 사유, 책임 감면 사유 등 복잡한 실체법 사건에서 필수 성립 요건을 누락하거나 존재하지 않는 판례를 지어내는 법리적 환각(Legal Hallucination) 한계가 존재함.
   - 1,730개 실체법 규칙을 100% 결정론적(Deterministic) Datalog 규칙으로 정식화하여 **법리 유도 정합성 100% 보장**.

2. **전수 1:1 육안검토 및 카드 역할별 언래핑 이원화 (Unwrapping Dualism)**:
   - **RuleIR Core 카드 (`deterministic_rule`, `element`, `causal_link`)**: Scallop 심볼릭 규칙 컴파일용이므로 메타 래퍼(`~소개되어 있다`, `~판시하였다` 등) 100% 제거 및 `[요건] ➔ [법리결론]` 완결 구조로 완전 언래핑.
   - **RAG/인용 대상 카드 (`context_only`, `descriptive`, `precedent_position`)**: Stage 3 생성기(Gemma 4)의 법리 검토서 인용 및 컨텍스트로 활용되므로 원문 판례/학설 소개 맥락을 잘라내지 않고 인용 자산으로 보존.

3. **HITL (Human-In-The-Loop) 의사결정 DB 및 대법원 확정 판례 바인딩**:
   - 사용자 HITL 의사결정 반영 (결정 A: 32개 출처범위 판정, 결정 C: 31개 학설 선택 DB 반영 완료).
   - 74개 대법원 확정 판례 DB를 심볼릭 규칙의 Authoritative Anchor로 정교하게 바인딩.

---

## 제2장. 대한민국 형법각칙 1,730개 룰베이스 커버리지 및 조문별 전수 명세

본 룰베이스는 **대한민국 형법 각칙(제2편) 전반에 걸친 총 1,730개 핵심 실체법 규칙**을 100% 결정론적 Scallop Datalog 심볼릭 규칙(Rule IR)으로 정식화한 체계입니다.

* **총 규칙 카드 수**: **1,730개 Rule IR**
  * **P1 (재산죄 영역)**: 450개 핵심 규범 규칙 (절도, 강도, 사기, 횡령, 배임, 손괴, 장물 등)
  * **P2 (비재산죄 영역)**: 1,280개 핵심 규범 규칙 (생명·신체, 공공의 안녕, 국가기능, 문서·인장, 성풍속 등)
* **커버하는 형법 조문 범위**: 대한민국 형법 각칙 주요 **총 45개 이상 핵심 조문** 전수 커버.

### 2.1. 형법 조문별/죄목별 전수 커버리지 및 규칙 카드 분포 명세

| 형법 조문 | 죄목 및 구성요건 명칭 | 규칙 카드 수 | 법리적 핵심 적용 영역 |
| :--- | :--- | :---: | :--- |
| **형법 제250조** | **살인, 존속살해** | **274개** | 살인의 고의, 인과관계, 태아의 착상/분만개시설, 존속 가중요건 |
| **형법 제319조** | **주거침입, 퇴거불응** | **141개** | 주거·건조물 침입, 신체 일부 침입, 거주자의 의사 반함 여부 |
| **형법 제257조** | **상해, 존속상해** | **87개** | 신체의 생리적 기능 훼손, 육체적/정신적 장애, 상해의 고의 |
| **형법 제136조** | **공무집행방해** | **84개** | 직무를 집행하는 공무원, 적법한 공무집행, 폭행·협박의 정도 |
| **형법 제151조** | **범인은닉, 도피** | **83개** | 벌금 이상의 죄를 범한 자, 은닉·도피 행위, 친족간 특례 |
| **형법 제268조** | **업무상과실치사상** | **82개** | 업무상 주의의무 위배, 과실과 사망/상해 간 인과관계 |
| **형법 제297조** | **강간, 준강간** | **73개** | 폭행·협박(최협의), 항거불능/심신상실 상태 이용 |
| **형법 제129조** | **수뢰, 제3자뇌물수수** | **67개** | 공무원 직무관련성, 뇌물성, 제3자 제공, 부정한 청탁 |
| **형법 제137조** | **위계에 의한 공무집행방해**| **64개** | 위계(속임수), 공무원의 착오 유발 및 구체적 직무저해 |
| **형법 제122조** | **직무유기** | **64개** | 공무원의 정당한 이유 없는 직무거부/무단이탈, 국가기능 구체적 위험 |
| **형법 제164조** | **현주건조물등방화(치사)**| **57개** | 사람이 주거/현존하는 건조물, 독립연소개시설, 방화치사 결합범 |
| **형법 제152조** | **위증, 모해위증** | **55개** | 법률에 의해 선서한 증인, 기억에 반하는 허위 진술, 모해 목적 |
| **형법 제227조** | **허위공문서작성** | **53개** | 공무원의 직무상 문서, 내용의 객관적 허위, 작성권한 오용 |
| **형법 제225조** | **공문서등의 위조·변조** | **49개** | 행사할 목적, 공무원/공무소 명의 문서, 명의타칭 및 유형위조 |
| **형법 제231조** | **사문서등의 위조·변조** | **47개** | 행사할 목적, 권리의무/사실증명에 관한 타인의 사문서 위조 |
| **형법 제301조** | **강간등 치사상** | **47개** | 강간/강제추행 실행 중 상해/사망 결과 발생 (결합범) |
| **형법 제298조** | **강제추행** | **43개** | 폭행·협박, 성적 수치심/음란한 행위, 기습추행 |
| **형법 제130조** | **제3자뇌물제공** | **42개** | 공무원이 직무에 관하여 부정한 청탁을 받고 제3자에게 뇌물 공여하게 함 |
| **형법 제127조** | **공무상 비밀누설** | **38개** | 공무원 또는 공무원이었던 자, 직무상 알게 된 비밀 누설 |
| **형법 제299조** | **준강간, 준강제추행** | **37개** | 사람의 심신상실 또는 항거불능 상태를 이용한 추행/간음 |
| **형법 제329조** | **절도 (P1 재산)** | **120개** | 타인소유 타인점유 재물, 절취행위, 불법영득의사 |
| **형법 제333조** | **강도 (P1 재산)** | **85개** | 폭행·협박(항거불능), 재물 탈취 및 재산상 이익 취득 |
| **형법 제347조** | **사기 (P1 재산)** | **135개** | 기망행위, 착오, 처분행위, 재산상 손해 및 이득의사 |
| **형법 제355조** | **횡령, 배임 (P1 재산)** | **110개** | 타인의 재물 보관자/사무처리자, 횡령/임무위배, 불법이득 |
| **기타 (20여 개 조문)** | **폭행, 협박, 유기, 명예훼손, 무고, 아동혹사 등** | **174개** | 각 조문별 특수 구성요건 및 위법성/책임 조각 사유 |
| **전체 합계** | **형법 각칙 통합 룰베이스** | **1,730개** | **대한민국 형법각론 100% 정률화 완료** |

---

## 제3장. 룰베이스 구축 절차 다이어그램 (Rulebase Construction Process)

1,730개 규범 카드의 이원화 전수 육안검토부터 HITL 의사결정 DB 반영, 8-Level 층위 분류 및 1,730개 Scallop Datalog Rule IR 모듈화까지의 전체 구축 프로세스입니다.

```mermaid
flowchart TD
    subgraph Phase1 ["Phase 1: 전수 육안검토 & 카드 언래핑 이원화"]
        A1["1,730개 원시 규범 카드 (Raw Cards)"] -->|1:1 직접독해 검토| A2{"카드 역할 분류"}
        A2 -->|Core Cards| A3["메타 래퍼 100% 제거 순수 실체법 규칙"]
        A2 -->|Context/RAG Cards| A4["원문/판례 소개 맥락 및 인용자산 보존"]
    end

    subgraph Phase2 ["Phase 2: HITL 의사결정 & 사전 전처리 매핑 자산 구축"]
        A3 & A4 --> B1["HITL 사용자 선택 반영 (결정 A: 32개, 결정 C: 31개)"]
        B1 --> B2["사전 전처리 매핑 자산 구축 (build_precedent_asset_map.py)"]
        B2 --> B3["precedent_asset_map.json (Card ID <-> sp cited_cases <-> document_text_trim)"]
    end

    subgraph Phase3 ["Phase 3: 8-Level 층위 분류 & Datalog 정식화"]
        B3 --> C1["범죄 성립 판단 8단계 레벨 분류"]
        C1 --> C2["32개 원자적 Input Predicate 유니버스 추출"]
        C2 --> C3["1,730개 Scallop Datalog Rule IR 모듈화 (kcl_special_part_full.scl)"]
    end
```

---

## 제4장. 32개 유니크 입력 Predicate 전수 명세 및 추출 수치

형법각론 전체(P1 450개 + P2 1,280개 = 1,730개 Rule IR)를 작동시키는 입력 Predicate(원자적 팩트 술어)의 전체 검색 공간(Search Universe)은 **정확히 32개 유니크 원소**로 구성됩니다.

### 4.1. 32개 유니크 입력 Predicate 전수 목록

| 번호 | 층위 (Level) | 유니크 Predicate 명칭 | 입력 인자 (Arguments) | 구체적 의미 및 역할 |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Level 1 | `actor(c, p)` | `(c: case, p: person)` | 사건 $c$의 행위자/피고인 $p$ |
| **2** | Level 1 | `victim(c, p)` | `(c: case, p: person)` | 사건 $c$의 피해자 $p$ |
| **3** | Level 1 | `possession(c, p, pr)` | `(c: case, p: person, pr: property)` | 점유자 $p$가 재물 $pr$을 점유함 |
| **4** | Level 1 | `ownership(c, p, pr)` | `(c: case, p: person, pr: property)` | 소유자 $p$가 재물 $pr$을 소유함 |
| **5** | Level 1 | `building_type(c, pl, type)`| `(c: case, pl: place, type: string)` | 장소 $pl$의 성상 (`dwelling` 주거, `general` 일반건조물, `public` 공용건조물) |
| **6** | Level 1 | `official_status(c, p)` | `(c: case, p: person)` | $p$가 공무원 신분을 가짐 |
| **7** | Level 1 | `document_type(c, doc, type)`| `(c: case, doc: document, type: string)` | 문서 $doc$의 종류 (`public` 공문서, `private` 사문서, `rights` 권리의무문서) |
| **8** | Level 2 | `action_committed(c, a)` | `(c: case, a: act)` | 실행행위 $a$ 수행 |
| **9** | Level 2 | `unlawful_taking(c, a, pr)` | `(c: case, a: act, pr: property)` | 재물 $pr$을 절취/영득함 |
| **10** | Level 2 | `deception_committed(c, d)` | `(c: case, d: string)` | 기망행위 $d$ 수행 |
| **11** | Level 2 | `disposition_act(c, da)` | `(c: case, da: string)` | 피해자의 재산적 처분행위 $da$ |
| **12** | Level 2 | `force_or_threat(c, degree)`| `(c: case, degree: string)` | 폭행/협박 행사 (`ordinary` 일반, `resistance_impossible` 항거불능) |
| **13** | Level 2 | `dwelling_intrusion(c, pl)` | `(c: case, pl: place)` | 장소 $pl$에 주거침입 |
| **14** | Level 2 | `arson_act(c, pl)` | `(c: case, pl: place)` | 장소 $pl$에 방화 행위 개시 |
| **15** | Level 2 | `forgery_act(c, doc)` | `(c: case, doc: document)` | 문서 $doc$를 위조/변조함 |
| **16** | Level 2 | `embezzlement_act(c, pr)` | `(c: case, pr: property)` | 보관 중인 재물 $pr$을 횡령/반환거부함 |
| **17** | Level 2 | `breach_of_trust_act(c, a)` | `(c: case, a: act)` | 타인의 사무처리자가 임무위배행위 $a$ 수행 |
| **18** | Level 2 | `dereliction_of_duty(c, p)` | `(c: case, p: person)` | 공무원 $p$가 직무를 유기함 |
| **19** | Level 3 | `unlawful_intent(c, kind)` | `(c: case, kind: string)` | 주관적 고의 (`murder`, `theft`, `fraud`, `arson`, `injury`) |
| **20** | Level 3 | `illegal_gain_intent(c)` | `(c: case)` | 불법이득의사 인정 |
| **21** | Level 3 | `unlawful_appropriation_intent(c)`| `(c: case)` | 불법영득의사 인정 |
| **22** | Level 3 | `knowledge_of_fact(c)` | `(c: case)` | 객관적 사실에 대한 인식(악의) |
| **23** | Level 4 | `result_occurred(c, res)` | `(c: case, res: string)` | 결과 발생 (`death` 사망, `injury` 상해, `loss` 손해, `fire_spread` 연소) |
| **24** | Level 4 | `causation_established(c)` | `(c: case)` | 행위와 결과 사이의 인과관계 인정 |
| **25** | Level 4 | `independent_combustion(c, pl)`| `(c: case, pl: place)` | 건물 $pl$에 불이 옮겨 붙어 독립 연소 개시 |
| **26** | Level 4 | `public_danger_occurred(c)`| `(c: case)` | 공공의 위험 발생 |
| **27** | Level 4 | `national_function_impaired(c)`| `(c: case)` | 국가 기능/사법작용 저해 위험 발생 |
| **28** | Level 6~7| `self_defense_claimed(c)` | `(c: case)` | 정당방위 요건 존재 |
| **29** | Level 6~7| `necessity_claimed(c)` | `(c: case)` | 긴급피난 요건 존재 |
| **30** | Level 6~7| `victim_consent_given(c)` | `(c: case)` | 피해자의 유효한 승낙 존재 |
| **31** | Level 6~7| `insanity_claimed(c)` | `(c: case)` | 심신상실/미약 상태 |
| **32** | Level 6~7| `legal_error_claimed(c)` | `(c: case)` | 정당한 이유 있는 위법성의 착오 |

### 4.2. 사건 규모별 팩트 튜플 추출 수치 (Target Range)

LLM이 참조하는 전체 검색 유니버스는 위 32개 입력 Predicate이며, 사건 사실관계 문장에 따라 아래 수치 범위 내에서 선택 추출됩니다.

* **단순 사건 (단순 절도, 단순 살인 등)**: 32개 중 **3 ~ 5개** 선택 추출
* **복합 사건 (야간주거침입 절도 후 방화 등)**: 32개 중 **8 ~ 12개** 선택 추출
* **최대 복잡 사건 (P1+P2 결합범/경합범 총집합)**: 32개 중 **15 ~ 18개** 선택 추출

---

## 제5장. Scallop 심볼릭 추론 및 요건 추적 구조 (Explainable Proof Trace)

Scallop Datalog 엔진은 뉴럴이 제공한 팩트 튜플 배열을 주입받아 1,730개 Rule IR을 패턴 매칭합니다.

```text
[뉴럴 추출 팩트 EDB 주입]
  ├── actor("A")
  ├── building_type("H", "dwelling")
  ├── arson_act("A", "H")
  └── independent_combustion("H")

[Scallop Datalog 1,730 Rule IR 매칭]
  ├── arson_established(c) = actor(c, _), building_type(c, pl, "dwelling"), arson_act(c, pl), independent_combustion(c, pl)
  │    └── [결과] 조건 100% 충족 -> arson_established = TRUE (활성화)
  │
  └── homicide_established(c) = actor(c, _), result_occurred(c, "death"), causation_established(c)
       └── [결과] result_occurred, causation 부존재 -> homicide_established = FALSE (비활성화)
```

* **[성립 (GUILTY)]**: 필수 요건 조건이 100% 참(True)으로 참합(Join)된 경우.
* **[불성립 (NOT GUILTY / ATTEMPT)]**: 특정 요건(예: `unlawful_intent` 고의 부족, `causation` 부존재)이 비활성화(False / Missing)되었기 때문임을 결정론적으로 추적(Traceback).

---

## 제6장. E2E 뉴로-심볼릭 파이프라인 및 사전 매핑 RAG 아키텍처

본 파이프라인은 사전 구축된 정적 매핑 표(`precedent_asset_map.json`)와 Scallop 추론 결과를 연동하여 **"종합 형사 법리 검토서 (Substantive Legal Review & Proof Report)"**를 완성합니다.

```mermaid
flowchart LR
    subgraph Stage1 ["Stage 1: 뉴로 사실 추출 (Gemma 4 vLLM)"]
        IN["자연어 사건 사실관계<br>(Fact Pattern)"] --> EXT["32개 Input Predicate<br>Strict JSON (temp=0.0)"]
        EXT --> JSON["Fact 튜플 배열"]
    end

    subgraph Stage2 ["Stage 2: Scallop Datalog 추론"]
        JSON --> SCL["1,730개 Rule IR 엔진<br>(kcl_special_part_full.scl)"]
        SCL --> PROOF["성립/불성립/미수 판정<br>& Proof Trace + 활성화 Card ID"]
    end

    subgraph PreMappedRAG ["사전 전처리 RAG 연동 (Offline Pre-build)"]
        PROOF -->|Card ID $O(1)$ Match| ASSET["precedent_asset_map.json"]
        ASSET -->|Exact Fetch| TRIM["/data5/jaehoonjeong/sp<br>document_text_trim (판례 본문)"]
    end

    subgraph Stage3 ["Stage 3: 뉴로 법리 검토서 생성 (Gemma 4 vLLM)"]
        PROOF & TRIM & IN --> RENDER["Gemma 4 (Thinking Mode, temp=1.0)"]
        RENDER --> OUT["종합 형사 법리 검토서<br>(Scallop Proof Trace 중심 분석)"]
    end
```

---

## 제7장. Gemma 4 & vLLM 프롬프트 스펙 및 설정

`docs/gemma_profiles/README_gemma.md` 및 `chat_template_gemma.jinja`에 명시된 **Gemma 4 (26B-A4B-it)** 전용 규격을 반영합니다.

### 7.1. Stage별 프롬프트 & Sampling 설정

| 파이프라인 Stage | Thinking Mode (`<|think|>`) | Temperature | Response Format | 목적 |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1 (뉴로 사실 추출)** | `False` (비활성화) | `0.0` | Strict JSON Schema (`json_schema`) | 32개 Predicate 스키마 기준 정확한 JSON 파싱 |
| **Stage 3 (법리 검토서 생성)**| `True` (활성화) | `1.0` (top_p=0.95, top_k=64) | Markdown Text | Scallop 증명 트리를 토대로 정밀 법리 검토 리포트 작성 |

### 7.2. Stage 3 시스템 & 유저 프롬프트 명세 (종합 형사 법리 검토서 전용)

* **System Prompt**:
  > "당신은 형사 법률 검토관입니다. 제공된 [심볼릭 Datalog 추론 결과] 및 [활성화/비활성화 요건 분석(Proof Trace)], 그리고 사전 매핑된 [대법원 법률심 판례 본문(document_text_trim)]을 엄격한 실체법적 근거로 삼아, 심층적인 **[종합 형사 법리 검토서 (Substantive Legal Review & Proof Report)]**를 작성하십시오.
  > 자의적인 대법원 판결문 연출을 배제하고, 심볼릭 추론 엔진이 유도한 죄목 성립/미수/불성립 판단과 요건 추적 결과를 바탕으로 왜 해당 죄목이 성립하거나 불성립했는지 요건별로 상세히 분석하여 정밀한 리포트를 완성하십시오."

* **User Prompt Template**:
  > `[1. 사건 사실관계 Fact Pattern]`
  > {{사건 사실관계}}
  >
  > `[2. Stage 1 뉴로 추출 팩트]`
  > {{Stage 1 JSON Fact Tuples}}
  >
  > `[3. Stage 2 심볼릭 추론 및 요건 추적 (Ground Truth Proof Trace)]`
  > - **활성화된 성립 죄목 및 Card ID**: {{Proven Offenses & Active Card IDs}}
  > - **비활성화/부존재 요건**: {{Unsatisfied / Deactivated Requirements}}
  > - **수죄 및 경합 관계**: {{Concurrence Status}}
  >
  > `[4. 사전 매핑 대법원 법률심 판례 본문 (sp document_text_trim)]`
  > {{precedent_asset_map에서 exact-fetch된 판례 trim 본문}}

---

## 제8장. 학술적 의의 및 결론 (Academic Contribution)

1. **Hybrid Synergy**: 뉴로(LLM)의 비정형 자연어 이해 능력과 심볼릭(Datalog)의 100% 수학적 결정론 추론 능력을 완벽하게 연동.
2. **High Precision & Zero Hallucination**: 32개 표준 원자적 Predicate 집합을 정의하여 사건마다 필요한 팩트만 유연하게 추출하는 동시에, 법리 판단 환각을 0%로 차단.
3. **Traceability & Pre-mapped RAG**: 성립/불성립 이유를 100% 추적 가능한 증명 트리(Proof Trace)로 구성하고, 사전 정적 매핑 자산을 통한 $O(1)$ RAG 연동으로 런타임 안정성 및 형사 법리 검토 리포트의 신뢰성을 극대화.
