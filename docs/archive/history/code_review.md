# 🔬 IDPR 코드베이스 전수 코드리뷰 (탈탈 털기)

> [!CAUTION]
> 이 리뷰는 실제 파일을 전수 열어 독해한 결과입니다. 추측이 아닌 실측 기반입니다.

---

## 0. 프로젝트 개관 — 문서 vs 코드 괴리 요약

| 항목 | 명세서 (KCL_1730_RULEBASE_SPECIFICATION.md) | 실제 코드 | 괴리 |
|---|---|---|---|
| Input Predicates | §4.1에 "32개" 기재, §제목에 "33개" 기재 | `schema_registry.py`: 33개 정의 | **문서 내 불일치** (32 vs 33, 본문은 32, 표 제목은 33) |
| Rule Cards | "1,730개" | `kcl_special_part_full.scl`: `rel` 3,527줄, `type` 3,538줄 → 룰 개수 ≈ 3,527 | 문서 숫자와 실제 `rel` 라인 수 불일치 (카드 vs 컴파일된 룰의 차이인지 정의 불명) |
| 3-Layer Engine | 문서에 미기술 | SCL 파일 하단에 Layer 1~3 존재 | **핵심 아키텍처가 문서에 없음** |
| Stage 2 Dry-run | 문서에 미기술 | `stage1_extractor.py` L62~167에 키워드 매칭 dry-run | 문서와 무관한 레거시 코드 잔존 |
| RAG Asset | `precedent_asset_map.json` | Stage 3에서 `card_case_metadata_map.json` 사용 | **문서와 실제 파일명 불일치** |

---

## 1. 🚨 [CRITICAL] Stage 1 Dry-Run: 키워드 매칭 코드 전면 잔존

**파일**: [stage1_extractor.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/pipeline/stage1_extractor.py#L62-L167)

```python
# L66~67: 텍스트 키워드 매칭으로 dry-run 팩트 생성
txt = (case_text + " " + case_data.get("title", "")).lower()

if "뇌물" in txt or "편취" in txt or "전달" in txt or "bribery" in txt:
    # ... 하드코딩된 팩트 리스트
if "침입" in txt or "베란다" in txt or "아파트" in txt or "dwelling" in txt:
    # ... 하드코딩된 팩트 리스트
if "절취" in txt or "장롱" in txt or "챙겨" in txt or "theft" in txt:
    # ...
if "불" in txt or "라이터" in txt or "소파" in txt or "arson" in txt:
    # ...
```

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **CRITICAL** | AGENTS.md Rule 9를 정면 위반하는 **텍스트 키워드 매칭**. `"장롱"`, `"베란다"`, `"챙겨"` 같은 특정 테스트케이스 전용 어구로 범죄 유형을 판별 |
| 2 | **CRITICAL** | AGENTS.md Rule 11 위반: 특정 뇌물/사기/절도/방화 시나리오에 대한 **하드코딩된 팩트 리터럴**이 100줄 이상 박혀 있음 |
| 3 | **HIGH** | 이 코드가 있는 한 `client=None` dry-run 모드에서 E2E 테스트를 돌리면 **LLM이 추출하는 것이 아니라 파이썬 if문이 추론을 결정**하므로, 테스트 자체가 의미 없음 |
| 4 | **HIGH** | `"불" in txt`은 `"불법"`, `"불가"` 등 모든 한국어 단어에 매칭됨 → false positive 폭발 |

### 해결 방향
- Dry-run 모드는 **`case_data["facts"]`에 사전 제공된 팩트만 passthrough** 하거나 에러를 발생시켜야 함
- 현재 L55~60의 "pre-supplied facts passthrough" 분기가 이미 존재하므로, L62~167의 키워드 매칭 코드 전체를 **즉시 삭제**하고, pre-supplied facts가 없으면 `RuntimeError("vLLM client required for fact extraction")` 발생

---

## 2. 🚨 [CRITICAL] SCL 룰베이스: 동일 body의 대량 중복 규칙

**파일**: [kcl_special_part_full.scl](file:///home/jaehoonjeong/data/IDPR/data/rulegen/kcl_special_part_full.scl)

SCL 파일 head를 보면:

```scl
// 사기(fraud) 관련 Rule들 — 이름만 다르고 body가 동일
rel rule_fraud_elements_chain(c) = actor(c, _), deception_committed(c, _), disposition_committed(c, _), unlawful_intent(c, "fraud")
rel rule_fraud_deception(c) = actor(c, _), deception_committed(c, _), disposition_committed(c, _), unlawful_intent(c, "fraud")
rel rule_fraud_mistake(c) = actor(c, _), deception_committed(c, _), disposition_committed(c, _), unlawful_intent(c, "fraud")
rel rule_fraud_disposition(c) = actor(c, _), deception_committed(c, _), disposition_committed(c, _), unlawful_intent(c, "fraud")
// ... 이 패턴이 수십 개 반복
```

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **CRITICAL** | `rule_fraud_*` 이름만 다른 동일 body 규칙이 최소 수십 개. 이것은 "카드 ID를 보존하면서 컴파일"한 결과로 보이지만, **Datalog 엔진 관점에서 rule body가 동일하면 결정론적 차이가 없음** — 즉, 사실상 중복 |
| 2 | **HIGH** | `rule_fraud_mistake`의 body가 `actor, deception_committed, disposition_committed, unlawful_intent(c, "fraud")`인데, "착오" 요건을 별도로 표현하지 않음. **법리적으로 사기죄의 개별 구성요건 단계(기망→착오→처분→재산적 손해)를 체계적으로 분해하지 못하고 있음** |
| 3 | **HIGH** | 방화 관련도 동일: `rule_art164_sec*` 모든 rule의 body가 `actor, arson_act, independent_combustion, unlawful_intent(c, "arson")`으로 동일 |
| 4 | **MEDIUM** | 7,120줄 중 실질적으로 의미 있는 **distinct rule body는 Layer 1~3의 약 20개 미만**일 가능성이 높음. 나머지 3,000+개 규칙은 "카드 추적용 tag" 역할에 불과 |

### 근본 원인
룰 카드 → SCL 컴파일 과정에서, 카드의 법리적 세부 차이(예: "기망의 의미", "묵시적 기망 인정 여부", "불작위에 의한 기망")를 **구성요건 레벨의 Predicate로 분해하지 않고**, 같은 body에 다른 tag만 붙여 컴파일함

### 해결 방향
- 법리적으로 구별되는 카드는 **구별되는 Predicate를 도입**해야 함 (예: `deception_type(c, "implicit")`, `deception_type(c, "omission")`)
- 순수 해설/컨텍스트 카드는 SCL에 컴파일하지 말고 **RAG metadata로만 유지**
- 이렇게 하면 SCL 룰베이스가 7,120줄 → 수백 줄로 축소되면서 정밀도는 올라감

---

## 3. 🚨 [CRITICAL] Stage 2: Scallop 출력 파서의 취약한 정규식 파싱

**파일**: [stage2_symbolic.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/pipeline/stage2_symbolic.py#L118-L176)

```python
# L119~127: stdout을 줄 단위로 파싱
for line in scallop_output_raw.splitlines():
    line = line.strip()
    if ":" in line and "{" in line and "}" in line:
        rel_name, tuples_part = line.split(":", 1)
        # ...
        if rel_name == "element_satisfied":
            # ...
        elif rel_name == "is_absorbed":
            # ...
        elif rel_name in ("final_substantive_offense", "proven_crime"):
            # ...
```

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **CRITICAL** | `line.split(":", 1)`은 relation 이름에 `:`가 포함되거나, tuple 값에 `:`가 포함되면 **파싱 실패** |
| 2 | **HIGH** | `if ":" in line and "{" in line and "}" in line` — Scallop 출력 포맷에 대한 임의 가정. Scallop 버전 업데이트 시 **무조건 깨짐** |
| 3 | **HIGH** | L129~148: `element_satisfied`, `is_absorbed`, `final_substantive_offense` 등의 relation 이름이 **파이썬 if/elif 체인으로 하드코딩**되어 있음 |
| 4 | **HIGH** | L160~176: "Fallback for active legacy crime queries" — 추가적인 하드코딩 fallback 경로가 존재 |
| 5 | **MEDIUM** | `scallop_output_raw[:500]`으로 출력 자르기 — 디버깅/감사 시 증거 유실 |

### 해결 방향
- Scallop `--query` 플래그를 사용하면 **개별 relation별 결과만 깔끔하게 출력**됨. `scallop_runtime.py`의 [run_scenario](file:///home/jaehoonjeong/data/IDPR/src/idpr/rulegen/scallop_runtime.py#L198-L239)에서 이미 이 방식으로 구현되어 있음!
- Stage 2는 `scallop_runtime.py`의 접근 방식을 **그대로 재활용**해야 함
- 관계명 하드코딩을 제거하고, query relations를 설정 파일 또는 SCL 파일 하단의 `query` 선언에서 **동적으로 추출**

---

## 4. 🔴 [HIGH] 두 개의 완전히 분리된 아키텍처가 병존

현재 `src/idpr/` 아래에 **서로 모르는 두 개의 독립적 아키텍처**가 존재합니다:

### 아키텍처 A: "KCL 1730 범용 파이프라인" (최근 구축)

| 모듈 | 역할 |
|---|---|
| `pipeline/schema_registry.py` | 33개 Predicate 스키마 |
| `pipeline/stage1_extractor.py` | 뉴로 팩트 추출 |
| `pipeline/stage2_symbolic.py` | Scallop Datalog 추론 |
| `pipeline/stage3_reporter.py` | 법리 검토서 생성 |
| `pipeline/e2e_runner.py` | E2E 오케스트레이터 |

### 아키텍처 B: "사기죄 전용 정밀 파이프라인" (선행 구축, 더 정교)

| 모듈 | 역할 |
|---|---|
| `neural/__init__.py` (618줄) | 사기죄 전용 계약 검증, role anchoring, assessment bundle |
| `fraud_planning.py` (413줄) | 사기죄 compositional reasoning plan |
| `reasoning/__init__.py` (183줄) | 사기죄 전용 Python deterministic reasoning |
| `llm/__init__.py` (398줄) | SKI-ML Gateway 클라이언트 + 캐시 |
| `rulegen/scallop_runtime.py` (280줄) | 사기죄 전용 Scallop fact rendering + query |

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **HIGH** | 두 아키텍처 간 **공유 코드 0%**. 같은 Scallop 실행을 완전히 다른 방식으로 두 번 구현 |
| 2 | **HIGH** | `neural/vllm_client.py`(아키텍처 A)와 `llm/__init__.py`(아키텍처 B)가 **같은 일을 하는 두 개의 LLM 클라이언트** |
| 3 | **HIGH** | `reasoning/__init__.py`(아키텍처 B)는 **Python 하드코딩 사기죄 추론 로직** — Scallop을 안 쓰는 별도의 심볼릭 경로 |
| 4 | **MEDIUM** | 아키텍처 B의 `fraud_planning.py`는 잘 설계된 "core + profile" 조합형 플래닝인데, 아키텍처 A는 이걸 전혀 활용하지 않음 |

### 해결 방향
- 아키텍처 B의 **정밀한 계약 검증 + profile 기반 플래닝**을 아키텍처 A에 통합
- LLM 클라이언트를 하나로 통일 (vLLM 로컬 + 외부 API 모두 지원)
- `reasoning/__init__.py`의 Python 하드코딩 추론은 Scallop으로 완전 이관 후 삭제

---

## 5. 🔴 [HIGH] Stage 3 RAG: $O(N)$ fallback alias matching

**파일**: [stage3_reporter.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/pipeline/stage3_reporter.py#L38-L43)

```python
# L38~43: "O(1) Exact-Fetch"라고 주석이 써있으나 실제는 O(N)
if not entry:
    for key, val in self.card_case_map.items():
        if cid in key or key in cid or key.split(".")[0] in cid:
            entry = val
            break
```

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **HIGH** | `card_case_metadata_map.json`은 **2.6MB**. 매 card ID마다 전체 dict를 순회하면 $O(N \times M)$ |
| 2 | **HIGH** | `key.split(".")[0] in cid` — 부분 문자열 매칭으로 **false positive** 발생 가능 |
| 3 | **MEDIUM** | 명세서에서 강조하는 "사전 정적 매핑 자산을 통한 $O(1)$ RAG 연동"과 **코드가 불일치** |

### 해결 방향
- Card ID 정규화 규칙을 확립하고, 정확한 key로만 조회
- Alias가 필요하면 **빌드 타임에 alias→canonical 역색인**을 사전 구축

---

## 6. 🔴 [HIGH] SCL 3-Layer Engine의 확장성 병목

**파일**: [kcl_special_part_full.scl](file:///home/jaehoonjeong/data/IDPR/data/rulegen/kcl_special_part_full.scl) 하단 Layer 1~3

### 현재 구조

```scl
// Layer 1: 개별 범죄 성립 규칙 — 죄목별로 하나씩 수기 작성
rel theft_established(c) = actor(c, _), unlawful_taking(c, _, _), unlawful_intent(c, "theft")
rel fraud_established(c) = actor(c, _), deception_committed(c, _), disposition_committed(c, _), unlawful_intent(c, "fraud")
// ... 10개

// Layer 2: 흡수 관계 — 쌍별로 수기 작성
rel absorbed_by("theft", "night_intrusion_theft")
rel absorbed_by("dwelling_intrusion", "night_intrusion_theft")
// ... 9개

// Layer 3: 경합 — generic하지만 특정 쌍 별도 query도 존재
rel bribery_fraud_concurrence(c) = generic_crime_concurrence(c, "bribery_delivery", "fraud")
```

### 문제점

| # | 심각도 | 내용 |
|---|---|---|
| 1 | **HIGH** | Layer 1에 **살인, 절도, 사기, 방화 등 10개 죄목만** 있음. 명세서의 "45개 이상 조문"과 대비하면 **커버리지 ~22%** |
| 2 | **HIGH** | **상해죄(`injury_established`)가 Layer 1에 없음**. 그런데 Layer 2 `absorbed_by`에서 `"injury"`가 `"robbery_injury"`에 흡수된다고 선언 → Scallop은 이를 항상 false로 평가 → **준강도치상 판단 시 상해 흡수가 작동하지 않음** |
| 3 | **HIGH** | `causation_established` 팩트가 `homicide_established`의 body에 **포함되어 있지 않음** — 인과관계 없이 살인이 성립 가능한 구조적 결함 |
| 4 | **HIGH** | Layer 2 `absorbed_by` 관계가 **9개 쌍만 수기 나열**. 실제 형법의 흡수 관계(예: 강간치상→강간+상해, 방화치사→방화+살인, 특수절도→야간주거침입절도 등)가 대부분 누락 |
| 5 | **MEDIUM** | 명세서 표에 위증, 무고, 직무유기, 공무집행방해 등 대다수 죄목의 Layer 1 `*_established` 규칙이 **존재하지 않음** |

### 해결 방향
- Layer 1의 `*_established` 규칙을 **카드 컴파일 파이프라인에서 자동 생성**되도록 해야 함
- Layer 2 `absorbed_by`를 별도 JSON/YAML 정의 파일로 분리하고 빌드 시 SCL에 컴파일
- 새 죄목 추가 시 "코드 파일을 직접 편집"할 필요 없이 **정의 파일 + 빌드 스크립트** 만으로 완료되는 구조

---

## 7. 🟡 [MEDIUM] VLLMClient 코드 품질 이슈

**파일**: [vllm_client.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/neural/vllm_client.py)

| 줄 | 이슈 |
|---|---|
| L101~104 | **동일한 체크가 두 번 연속**: `if not isinstance(output, dict):` 가 2줄 연속 |
| L1~244 전체 | `complete_json`과 `complete_text`의 HTTP 호출 코드가 **90% 중복** (request 구성, urlopen, error handling) |
| L126~130 | `complete_text`에서 `{{INPUT_JSON}}` 템플릿 치환 로직이 `build_chat_request`과 **중복 구현** |
| - | 타임아웃 1200초(20분) — 합리적 기본값인지 검토 필요 |

---

## 8. 🟡 [MEDIUM] 테스트의 의미론적 약점

**파일**: [test_e2e_pipeline.py](file:///home/jaehoonjeong/data/IDPR/tests/test_e2e_pipeline.py)

```python
def test_e2e_official_case_1_realistic_property_nonproperty(runner):
    result = runner.run_e2e(TEST_CASE_1)
    proven = [off["offense"] for off in result["symbolic_results"]["proven_offenses"]]
    assert any("dwelling_intrusion" in p for p in proven)
    assert any("theft" in p for p in proven)
    assert any("arson" in p for p in proven)
```

### 문제점

| # | 내용 |
|---|---|
| 1 | `runner`에 `client=None` → Stage 1은 **키워드 매칭 dry-run**을 사용. 따라서 이 테스트는 "LLM이 올바른 팩트를 추출하는지"가 아니라 "파이썬 if문이 키워드를 감지하는지"를 테스트 |
| 2 | Stage 2도 실제 Scallop 바이너리가 없으면 테스트가 깨지는 구조 → CI 환경에서의 실행 가능성 미보장 |
| 3 | `TEST_CASE_1`, `TEST_CASE_2`가 `scripts/` 모듈에서 import됨 → 테스트 데이터가 실행 스크립트에 종속 |

---

## 9. 🟡 [MEDIUM] `scripts/` 폴더의 스크립트 폭발

`scripts/` 디렉토리에 **85개의 파이썬 스크립트**가 flat하게 존재합니다.

- `build_*` 계열: 28개
- `run_*` 계열: 15개
- `apply_*` 계열: 9개
- `audit_*` 계열: 6개
- `finalize_*` 계열: 4개
- `draft_*` 계열: 3개
- 기타: 20개

### 문제점

| # | 내용 |
|---|---|
| 1 | 어떤 스크립트가 현행(live)이고 어떤 것이 레거시인지 **판단 불가능** |
| 2 | `build_fraud_full_rule_ir_candidate.py` **107,455 bytes**(~3,000줄) — 한 파일에 모든 빌드 로직 |
| 3 | 스크립트 간 의존 관계 파악 불가 → 빌드 순서 오류 위험 |

### 해결 방향
- 현행 파이프라인에 필요한 스크립트만 `scripts/active/`로 분리
- 나머지는 `scripts/archive/` 또는 삭제
- Makefile 또는 `doit`/`invoke` 기반 빌드 오케스트레이션 도입

---

## 10. 🟡 [MEDIUM] 아키텍처 B 내부의 사기죄 하드코딩

**파일**: [reasoning/__init__.py](file:///home/jaehoonjeong/data/IDPR/src/idpr/reasoning/__init__.py#L104-L163)

```python
def derive_fraud(inputs: FraudInputs) -> Derivation:
    required = {
        "deception": Fact("deception", (inputs.defendant, inputs.victim)),
        "mistake_caused": Fact("mistake_caused", (inputs.victim,)),
        "disposition_by_deceived": Fact(
            "disposition_by_deceived",
            (inputs.victim, inputs.property_id),
        ),
    }
```

- **사기죄 전용** 하드코딩된 Python 추론 로직
- Scallop과 **완전히 독립적**으로 동작하는 별도의 심볼릭 레이어
- `fraud_planning.py`의 `FRAUD_ROLES` 5-tuple도 사기죄 전용

---

## 11. 📊 법률 추론 시 예상되는 실제 병목

### 11.1. Predicate 표현력 부족

현재 33개 Predicate는 **존재/부존재 이진(binary)** 팩트만 표현 가능합니다:

```
actor(c, p)           → "행위자가 존재한다" (O/X)
force_or_threat(c, d) → "폭행/협박이 존재한다" (O/X)
```

실제 형사법 추론에 필요한 **정도(degree), 시간적 순서, 조건적 관계**를 표현 불가능:

| 필요한 표현 | 현재 커버 여부 |
|---|---|
| 협박의 정도 (최협의/광의/일반) | ❌ `force_or_threat(c, "violence")` 하나뿐 |
| 기망과 처분행위의 인과관계 | ❌ `causation_established`는 있으나 기망→착오→처분 체인 미표현 |
| 고의의 시점 (사전/사후/미필적 고의) | ❌ `unlawful_intent(c, "fraud")`만 존재 |
| 재산적 손해의 정량적 크기 | ❌ |
| 공동정범 vs 교사범 vs 방조범 | ❌ |
| 미수/예비/음모 단계 | ❌ |
| 결합범의 내부 시간 순서 | ❌ |

### 11.2. Stage 1→2 간 정보 유실

Stage 1이 추출한 `statement` (자연어 설명)은 Stage 2에서 **완전히 무시**됩니다:

```python
# stage2_symbolic.py L56~70
pred = str(fact.get("predicate") ...).strip()
raw_args = fact.get("arguments") or []
# statement는 읽지 않음 → 정보 유실
```

LLM이 `statement`에 담은 세밀한 법리 정보(예: "묵시적 기망에 해당", "미필적 고의")가 Scallop에 전달되지 않습니다.

### 11.3. 위법성 조각 사유의 처리 부재

33개 Predicate에 `consent_given`, `self_defense_claimed`, `necessity_claimed`, `insanity_claimed` 4개가 정의되어 있으나:
- Layer 1~3 SCL에서 이들을 **소비하는 규칙이 0개**
- 즉, LLM이 정당방위 팩트를 추출해도 **Scallop이 이를 무시**

---

## 12. 최종 요약: "규칙+카드만 추가하면 알아서 동작하는 코드"로 가는 로드맵

현재 상태를 한 문장으로 요약하면:

> **"사기죄에 대해 정교하게 설계된 파이프라인(B)과, 범용을 표방하지만 실질적으로 10개 죄목만 커버하고 키워드 매칭이 잔존하는 파이프라인(A)이 서로를 모른 채 공존하는 상태"**

### 해결 우선순위

| 순위 | 작업 | 예상 효과 |
|---|---|---|
| 🥇 | Stage 1 dry-run 키워드 매칭 **전면 삭제** | Rule 9/11 준수, 테스트 신뢰성 회복 |
| 🥈 | Stage 2 Scallop 파서를 `scallop_runtime.py` 방식으로 **통일** | 하드코딩 제거, Scallop 버전 독립성 |
| 🥉 | SCL Layer 1 `*_established` 규칙을 **빌드 스크립트에서 자동 생성** | 새 죄목 추가 시 SCL 수동 편집 불필요 |
| 4 | 아키텍처 A와 B **통합** (LLM client, Scallop runtime 공유) | 코드 중복 50% 이상 제거 |
| 5 | SCL 중복 body 규칙 정리 (카드 tag → metadata, 실질 구별 → Predicate 분화) | SCL 7,000줄 → 수백 줄, 정밀도 향상 |
| 6 | `absorbed_by` + Layer 1 룰 정의를 **외부 YAML/JSON**으로 분리 | 규칙 추가 = 설정 파일 편집 + `make build` |
| 7 | 위법성 조각 사유 처리 규칙 구현 | 정당방위/긴급피난이 작동하는 진짜 추론 |

---

## 13. 🚨 [추가 실측 — 2026-07-30] 비재산죄 확장 이후에도 §2/§6 문제가 그대로임을 실사례로 재확인

이 섹션은 §2("동일 body 대량 중복")와 §6("Layer 1 확장성 병목")에서 이미 지적된 문제가, 그 이후 진행된 **비재산죄(성범죄·주거침입·뇌물·직무유기 등) rulegen 확장 작업 이후에도 전혀 개선되지 않았음**을 실제 스모크 테스트 케이스(`kcl_criminal_r10_p1_q1_ga`, 변호사시험 10회 형사법 제1문)로 검증한 기록입니다.

### 13.1. Rule body 중복도 전수 census (§2 point 4의 "추정"을 실측으로 확정)

```bash
grep "^rel rule_" data/rulegen/kcl_special_part_full.scl \
  | sed 's/^rel rule_[a-zA-Z0-9_]*(c) = //' | sort | uniq -c | sort -rn
```

| 규칙 본문(body) 패턴 | 개수 | 비율 |
|---|---:|---:|
| `actor(c,_), action_committed(c,_)` | 1,592 | 45.6% |
| `actor, deception_committed, disposition_committed, "fraud"` | 693 | 19.9% |
| `actor, legal_custody, "embezzlement"` | 355 | 10.2% |
| `actor, action_committed, result_occurred("death"), "murder"` | 324 | 9.3% |
| `actor, unlawful_taking, "theft"` | 207 | 5.9% |
| `actor, dwelling_intrusion_committed` | 151 | 4.3% |
| `actor, bribery_delivery_committed` | 105 | 3.0% |
| `actor, arson_act, independent_combustion, "arson"` | 60 | 1.7% |
| **합계** | **3,487** | **100.0%** |

`rel rule_*(...)` 로 시작하는 전체 relation 3,487개(§0 표의 "3,527"과 근사) 중 **distinct body는 정확히 8종뿐**이며, 이 8종이 전체의 100%를 남김없이 채웁니다. 즉 §2에서 "distinct rule body는 Layer 1~3의 약 20개 미만일 가능성이 높다"고 추정한 것보다 실제로는 더 심각합니다 — **개별 rule body 다양성이 사실상 0**입니다. `강제추행 간접정범`, `주거침입죄 위요지`, `강간치상 예견가능성` 같은 이름이 붙은 700개 이상의 art297/298/301/319 규칙들도 전부 위 8종 중 하나(대부분 `actor, action_committed`만으로 무조건 참)를 그대로 복사한 것이며, 이름이 시사하는 법리적 조건(강제성 정도, 신체 접촉 여부, 공용부분 해당성 등)을 **전혀 검증하지 않습니다**.

### 13.2. 비재산죄 확장이 §6 "Layer 1 = 10개 죄목"을 하나도 늘리지 못했음

`rule_artXXX_*` 이름에서 조문 번호를 추출하면 현재 SCL에 **50개 조문**이 존재합니다:

```
122 127 129 130 133 136 137 151 152 164 225 227 231 234 239 250 254 255
257 259 263 267 268 297 298 299 300 301 319 323 328 329 330 331 332 333
334 335 337 338 342 343 344 350 355 356 357 360 366
```

그런데 §6에서 지적한 **최종 결론 레이어(`element_satisfied` → `final_substantive_offense` → `proven_crime`)의 하드코딩된 10개 카테고리**는 지금도 그대로입니다 (`kcl_special_part_full.scl:7027-7069`):

```
theft, night_intrusion_theft, quasi_robbery, robbery_injury,
fraud, embezzlement, homicide, arson, dwelling_intrusion, bribery_delivery
```

즉 성범죄(art297/298/299/300/301), 상해·폭행·과실치사상(art254/255/257/259/263/267/268), 문서위조(art225/227/231/234/239), 직무유기·범인도피·증거인멸(art122/127/129/130/136/137/151/152), 공갈·손괴(art350/366) 등 **최근 확장으로 새로 생긴 조문 그룹 전부가 Layer 1에 단 하나도 연결되어 있지 않습니다.** 확장 작업으로 SCL 파일은 5,091줄 → 7,120줄로 늘었지만(`git log`상 `ca85b49` → `dd3036b`), Layer 1이 그대로인 이상 **이 확장이 최종 파이프라인 출력에 미치는 실질적 효과는 0%**입니다. §6 point 1의 "커버리지 ~22%"라는 수치는 확장 이전 스냅샷 기준이었는데, 확장 이후에도 분모(조문 수)만 커졌을 뿐 분자(Layer 1 연결 조문 수)는 그대로라서 **실질 커버리지는 오히려 더 낮아졌습니다** (10/50 ≈ 20%, 확장 전보다 소폭 하락).

### 13.3. 실사례 검증: 이 스모크 케이스를 지금 돌리면 나올 결과를 예측

`kcl_criminal_r10_p1_q1_ga`(강제추행 간접정범 + 주거침입강간치상 + 뇌물공여 등 6개 이상 죄책이 쟁점인 사례, rubric 36개)를 현재 파이프라인에 그대로 태우면, Stage 1이 사실관계를 완벽히 추출한다고 가정해도 Stage 2의 Layer 1에는 이 사건과 맞아떨어지는 카테고리가 `dwelling_intrusion`(주거침입)과 `bribery_delivery`(뇌물공여) 단 둘뿐입니다. 나머지 핵심 쟁점 — **강제추행 간접정범, 강간(미수), 강간치상, B에 대한 폭행/상해** — 은 Layer 1에 대응 카테고리 자체가 없어 `element_satisfied`에 절대 나타날 수 없습니다.

결과적으로 지금 파이프라인이 이 문항에서 낼 수 있는 최선의 결과는 "주거침입 + 뇌물공여" 2개 죄명뿐이며, 이는 [baseline_smoke_test_r10_p1_q1_ga.md](baseline_smoke_test_r10_p1_q1_ga.md)에서 비교한 7개 베이스라인 중 가장 부실했던 것(ACAL, 버그로 사실관계 자체를 인식 못해 0개)보다는 낫지만, 나머지 6개 베이스라인(각 3~5개 죄명 언급) 전부보다 못한 결과입니다. "비재산죄로 확장했다"는 사실만으로는 베이스라인 대비 우위를 전혀 보장하지 못하며, §6 해결 방향(Layer 1 자동 생성)을 실행하지 않는 한 이번 확장분(art297/298/301/319 등)은 rulegen 예산만 소모하고 출력에는 기여하지 않는 죽은 코드로 남습니다.

### 13.4. 우선순위 갱신 제안

§12 표의 🥉 항목("SCL Layer 1 `*_established` 규칙을 빌드 스크립트에서 자동 생성")이 원래 3순위였는데, 비재산죄 확장이 이미 진행되어 죽은 규칙이 700개 이상 누적된 지금 시점에는 **이걸 가장 먼저 해결하지 않으면 향후 rulegen 캠페인이 늘어날수록 죽은 코드만 비례해서 늘어나는 구조**입니다. Layer 1을 개별 크라임마다 수기 작성하는 대신, "각 조문 그룹의 대표 `_established` 관계를 rule card 메타데이터(예: 카드가 속한 죄명 태그)로부터 빌드 시점에 자동 생성"하는 방식으로 바꾸는 것을 다음 작업으로 제안합니다.

