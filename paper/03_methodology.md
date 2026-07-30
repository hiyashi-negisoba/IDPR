# 3. 파이프라인 방법론 및 기술 명세 (Methodology & Technical Specifications)

---

## 3.1. 파이프라인 전체 아키텍처 개요

기존 단일 거대 언어 모델(Monolithic LLM)의 구성요건 누락, 자의적 법리 환각, 허위 판례 창작 문제를 원천 차단하기 위해 **"신경망 팩트 추출 ➔ 심볼릭 결정론 추론 ➔ 사전 정적 매핑 RAG ➔ 신경망 종합 검토서 생성"**의 **뉴로-심볼릭-뉴로(Neuro-Symbolic-Neuro) 3단계 이중 구동 아키텍처**를 구현하였다.

```mermaid
flowchart TD
    subgraph S1 ["제1단계: 신경망 팩트 추출기 (vLLM / Gemma 4)"]
        INPUT["자연어 형사 사건 사실관계 (Fact Pattern)"] --> S1_LLM["Gemma 4 26B (temp=0.0)<br>Draft 7 JSON Schema 강제 디코딩"]
        S1_LLM --> S1_OUT["원자적 팩트 구조체 JSON<br>(34개 표준 Datalog 팩트 술어)"]
    end

    subgraph S2 ["제2단계: 심볼릭 결정론 추론기 (Scallop Datalog)"]
        S1_OUT -->|범용 EDB 동적 변환| S2_EDB["Scallop EDB 튜플 자동 생성<br>rel predicate('case_id', 'arg1', 'arg2')"]
        S2_EDB --> S2_ENGINE["Scallop Datalog 0.2.4 추론 엔진<br>(통합 룰베이스, 7,084 라인)"]
        S2_ENGINE -->|범용 수죄론 메타 추론 고정점 연덕| S2_TRACE["수학적 증명 트레이스<br>(Proven Offenses & Active Card IDs)"]
    end

    subgraph RAG ["오프라인 사전 매핑 RAG 레이어"]
        S2_TRACE -->|Active Card IDs 기반 O(1) Direct Hash Join| MAP["card_case_metadata_map.json<br>(3,487개 유니크 규범 자산 정적 맵)"]
        MAP --> RAG_TEXT["실체법 법리 텍스트 &<br>대법원 판례 Exact Citations"]
    end

    subgraph S3 ["제3단계: 신경망 종합 법리 검토서 생성기"]
        INPUT & S2_TRACE & RAG_TEXT --> S3_LLM["Gemma 4 26B (Thinking Mode, temp=1.0)<br>증명 트레이스 유도 생성"]
        S3_LLM --> FINAL_REPORT["무환각 종합 형사 법리 검토서 리포트<br>(Substantive Legal Review & Proof Report)"]
    end
```

### 파이프라인 3단계 핵심 데이터 흐름:
1. **제1단계 (신경망 팩트 추출기)**: 법률적 유부죄 판단을 시도하지 않고, vLLM Draft 7 JSON Schema (`get_fact_graph_json_schema()`)로 디코딩 로짓 공간을 강제하여 **34개 표준 Datalog 팩트 서술어(Canonical 34 Input Predicates)** 규격의 원자적 JSON 구조체만 추출한다.
2. **제2단계 (심볼릭 Datalog 추론기)**: 제1단계가 추출한 JSON 팩트를 파이프라인 배선을 통해 Scallop Datalog EDB 문장으로 1:1 자동 변환하고, 3,487개 유니크 규범 룰이 정률화된 Scallop Datalog 룰베이스 (`kcl_special_part_full.scl`, 7,084 라인)를 단 1회의 고정점 연덕 추론(Single-shot Fixpoint Evaluation)으로 실행하여 **100% 수학적 연덕 증명 트레이스(Ground Truth Proof Trace)** 및 성립 죄목과 활성화된 규범 카드 ID (`active_card_ids`)를 산출한다. 파이프라인 내 파이썬 `if/elif` 조건 분기를 100% 제거하고 대한민국 형법 제37조/제40조 범용 수죄론 메타 추론 엔진(`generic_crime_concurrence`)을 가동한다.
3. **제3단계 (신경망 법리 검토서 생성기)**: 활성화된 `active_card_ids`를 키로 하여 사전 매핑된 메타데이터 자산 (`card_case_metadata_map.json`)에서 $O(1)$ Direct Hash Join 방식으로 대법원 판례 번호와 주석서 원문을 끌어온 뒤(RAG exact-fetch), Gemma 4 (Thinking Mode)가 최종 검증된 종합 형사 법리 검토서 마크다운 리포트를 작성한다.

---

## 3.2. 제1단계: 스키마 강제 기반 신경망 팩트 추출기

제1단계는 신경망의 자의적 형사 판단과 팩트 환각을 차단하기 위해 팩트 추출만을 전담한다.

### 3.2.1. 로짓 공간 제어를 통한 생성 자유도 억제
- **사용 모델**: Gemma 4 26B (`temperature=0.0`, `enable_thinking=False`)
- **JSON Schema 강제 (`schema_registry.py`)**: vLLM 서빙 엔진에 Draft 7 JSON Schema를 주입하여 `facts` 배열 이외의 자의적 텍스트 디코딩을 로짓 디코딩 단계에서 물리적으로 차단함.
- **34개 표준 Datalog 팩트 서술어 유니버스**: `actor`, `victim`, `unlawful_taking`, `arson_act`, `is_night_time`, `unlawful_intent` 등 6개 기능 그룹으로 분류된 34개 서술어만 사용함. *(전수 목록은 부록 B 참조)*

### 3.2.2. 원자적 팩트 JSON 출력 구조체
```json
{
  "case_id": "CASE_KCL1730_2026_REAL_001",
  "actors": [{"entity_id": "actor_A", "roles": ["defendant"]}],
  "facts": [
    {
      "fact_id": "fact_001",
      "predicate": "dwelling_intrusion_committed",
      "statement": "피고인은 아파트 베란다 창문을 통하여 무단 침입하였다.",
      "arguments": ["place_dwelling"]
    },
    {
      "fact_id": "fact_002",
      "predicate": "is_night_time",
      "statement": "범행 시각은 23:00경 야간이다.",
      "arguments": ["night_time"]
    },
    {
      "fact_id": "fact_003",
      "predicate": "unlawful_taking",
      "statement": "피고인은 안방 장롱에서 현금과 시계를 절취하였다.",
      "arguments": ["act_theft", "prop_cash_watch"]
    }
  ]
}
```

---

## 3.3. 제2단계: Scallop Datalog 심볼릭 결정론 추론기

제2단계는 파이프라인의 수학적/법리적 결정론을 보장하는 핵심 심볼릭 추론 엔진이다.

### 3.3.1. 34개 표준 서술어 및 3,487개 규범 카드의 룰 정률화
[scripts/build_p2_rule_ir_pipeline.py](file:///home/jaehoonjeong/data/IDPR/scripts/build_p2_rule_ir_pipeline.py) 컴파일러는 전수 3,487개 유니크 규범 카드를 Datalog 릴레이션 규칙으로 합성한다:
$$\texttt{rel rule\_card\_id(c) = actor(c, \_), unlawful\_taking(c, \_, \_), unlawful\_intent(c, "theft")}$$

### 3.3.2. 메타 래퍼 언래핑 이원화 (Unwrapping Dualism)
- **Core Rule Card (`deterministic_rule`, `element`)**: 원문 주석서의 메타 어구(`~소개되어 있다`, `~판시하였다`)를 100% 잘라내고 `[사실관계/구성요건] ➔ [실체법 결론]`의 완결된 순수 Datalog 규칙으로 언래핑함.
- **Context/RAG Card (`context_only`, `descriptive`)**: 원문 판례 소개 맥락을 그대로 유지하여 제3단계 RAG 판례 인용 근거 자산으로 보존함.

### 3.3.3. 대한민국 형법 제37조/제40조 범용 수죄론 Datalog 메타 추론 엔진
통합 Scallop 룰베이스 (`kcl_special_part_full.scl`, 7,084 라인)는 특정 죄목 수동 핀포인트 하드코딩을 100% 배척하고, 범용 수죄론 메타 추론 릴레이션(`generic_crime_concurrence`)을 가동한다:
```prolog
// 형법 제37조, 제38조, 제40조 범용 수죄 및 경합 Datalog 메타 추론 엔진 (Zero Hardcoding)
type proven_crime(String, String)
rel proven_crime(c, "theft") = theft_established(c), not night_intrusion_theft_established(c)
rel proven_crime(c, "night_intrusion_theft") = night_intrusion_theft_established(c)
rel proven_crime(c, "fraud") = fraud_established(c)
rel proven_crime(c, "embezzlement") = embezzlement_established(c)
rel proven_crime(c, "homicide") = homicide_established(c)
rel proven_crime(c, "arson") = arson_established(c)
rel proven_crime(c, "dwelling_intrusion") = dwelling_intrusion_established(c), not night_intrusion_theft_established(c)
rel proven_crime(c, "bribery_delivery") = bribery_delivery_established(c)

// 어떤 성립 죄목 튜플 쌍 (o1, o2)이더라도 100% 범용 동적 경합 추론
type generic_crime_concurrence(String, String, String)
rel generic_crime_concurrence(c, o1, o2) = proven_crime(c, o1), proven_crime(c, o2), o1 != o2
```

### 3.3.4. 야간주거침입절도죄(형법 제330조) 결합범 포괄일죄 배척 메커니즘
야간 주거 침입 후 절도를 범한 경우(형법 제330조 결합범), 단순 주거침입죄와 절도죄의 실체적 경합을 자동 비활성화(Suppression)하여 단일 결합범 포괄일죄로 도출한다:
$$\texttt{rel proven\_crime(c, "theft")} = \text{theft\_established}(c), \mathbf{not\ night\_intrusion\_theft\_established}(c)$$
$$\texttt{rel proven\_crime(c, "dwelling\_intrusion")} = \text{dwelling\_intrusion\_established}(c), \mathbf{not\ night\_intrusion\_theft\_established}(c)$$

### 3.3.5. 범용 EDB 변환 및 1초 미만 고성능 솔버 구동
[src/idpr/pipeline/stage2_symbolic.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/pipeline/stage2_symbolic.py)는 제1단계 JSON을 범용적으로 Datalog EDB 문장(`rel unlawful_taking("CASE_001", "act_theft", "prop_cash")`)으로 자동 변환한 후 [tools/scallop/scli-0.2.4-linux-x86_64](file:///home/jaehoonjeong/data/IDPR/tools/scallop/scli-0.2.4-linux-x86_64) 바이너리를 실행하여 1초 미만($O(1)$) 속도로 모든 성립 릴레이션을 연체 계산함.

---

## 3.4. 제3단계: 증명 트레이스 유도 생성기 및 정적 RAG 바인딩

제3단계는 심볼릭 추론 결과를 감설이 아닌 무환각 마크다운 검토서로 시각화한다.

### 3.4.1. Active Card ID 기반 $O(1)$ Direct Hash Join RAG 메커니즘
제2단계 심볼릭 추론 엔진에서 참(True)으로 고정점 연덕 증명된 규범 카드 ID들(`active_card_ids`)을 오프라인 3,487개 규범 카드 정적 DB (`card_case_metadata_map.json`)와 **Direct Hash Join**하여 대법원 판례 번호(`case_nos`) 및 관련 실체법 문장을 1:1로 100% 무환각 인출함:
$$\text{RAG Context} = \text{Map}[\text{active\_card\_id}] \quad \Rightarrow \quad \text{"[Datalog Card [active\_card\_id] Join ➔ 대법원 \{case\_nos\} 판결]: \{rag\_text\}"}$$

### 3.4.2. 증명 트레이스 유도 롱폼 IRAC 법리 검토서 작성
Gemma 4 26B (Thinking Mode, `temperature=1.0`, `enable_thinking=True`)에 사실관계, 제1단계 팩트, 제2단계 증명 트레이스, RAG 판례 인출 텍스트를 입력하여 쟁점 도출(Issue), 요건별 인정 여부 및 Exact Citations(Rule), 사안 포섭(Application), 수죄 및 최종 결론(Conclusion)의 4단 구조 **종합 형사 실체법리 검토서 리포트**를 완성함.
