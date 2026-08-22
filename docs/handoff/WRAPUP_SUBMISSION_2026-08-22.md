# 제출 후 갈무리 (2026-08-22)

논문 제출 완료 시점의 레포 상태 기록. **2026-08-17 11:35 이후 레포에 변경 없음** —
그 뒤 작업(논문 저작)은 레포 밖에서 이뤄졌다. 이 문서는 다음 연구(ICLR) 착수 전에
"지금 손에 있는 것 / 열려 있는 것"을 한 장으로 고정한다.

---

## 1. 최종 수치

### 1.1 KCL-26 LLM judge — P vs N (`phase3_judge_sonnet_pn_v2_aligned`, 8/16 20:23)

symbolic plan을 준 조건(P)과 안 준 조건(N)의 짝지은 비교. Sonnet judge, 26문항.

| metric | N | **P** | Δ(P−N) | 95% CI (paired bootstrap, 10k) |
|---|---:|---:|---:|---|
| precision | 0.514 | **0.584** | **+0.070** | [0.0021, 0.1424] ✅ |
| coverage | 0.168 | **0.191** | +0.023 | [−0.0002, 0.0460] ~경계 |
| hallucination(raw) | −3.27 | **−2.69** | +0.577 | [−0.192, 1.308] n.s. |
| consistency | 0.808 | 0.750 | −0.058 | [−0.154, 0.029] n.s. |

**유의한 축은 precision 하나다.** coverage는 하한이 0에 걸쳐 있고, hallucination·consistency는
n.s.다. consistency는 오히려 P가 낮다(유보 표현이 늘어난 대가로 읽힌다).

pool 대비 위치(같은 judge run, n=26):

| method | precision | coverage | consistency | halluc.(raw) |
|---|---:|---:|---:|---:|
| **v2 IDPR-P** | **0.584** | 0.191 | 0.750 | **−2.69** |
| idpr_nsn_lean_61_routing_fix (v1) | 0.582 | 0.209 | 0.731 | −3.23 |
| chain_of_thought | 0.522 | **0.211** | 0.827 | −3.65 |
| v2 IDPR-N | 0.514 | 0.168 | 0.808 | −3.27 |
| standard_rag | 0.503 | 0.149 | 0.884 | −3.31 |
| vanilla_zero_shot | 0.478 | 0.151 | 0.854 | −3.71 |
| legal_chain_reasoner | 0.476 | 0.166 | **0.933** | −3.54 |
| acal | 0.456 | 0.168 | 0.856 | −3.23 |
| leprec | 0.435 | 0.140 | 0.837 | −3.23 |
| fol_autoformalizer_solver | 0.394 | 0.101 | 0.750 | −4.20 |

precision·hallucination 1위, coverage는 CoT에 진다. consistency는 하위권.

> 참고: 직전 판정 run `phase3_judge_sonnet_pn_defeated_by_state_fix`(8/16 17:57)에서는
> P 0.525 / N 0.538로 **P가 오히려 낮았다.** aligned run이 정본이지만, 두 run의 차이가
> 어디서 왔는지는 문서화돼 있지 않다 — 다음 연구에서 P 우위를 주장하려면 먼저 확인할 것.

### 1.2 외부 벤치마크 — LBOX Call 1 / KBL Call 2 (baseline 7종 **전부 완료**)

`docs/analysis/v2_external_benchmark_lbox_kbl_results_ko.md`(브랜치
`feature/kbl-binary-mode`)는 "진행 중"으로 멈춘 living draft다. **아래가 최종값**이다
(`experiments/external/runs/baselines/*/scores/`).

**LBOX Call 1** (죄명 추출, N=300 subset · ours는 3375 전체도 병기)

| method | recall | case full-hit | precision | F1 |
|---|---:|---:|---:|---:|
| **ours (raw, 300)** | **0.994** | **0.993** | 0.431 | 0.601 |
| ours (raw, 3375 전체) | 0.952 | 0.943 | 0.456 | 0.617 |
| leprec | 0.971 | 0.967 | **0.743** | **0.842** |
| standard_rag | 0.971 | 0.967 | 0.423 | 0.590 |
| legal_chain_reasoner | 0.977 | 0.973 | 0.655 | 0.784 |
| chain_of_thought | 0.968 | 0.963 | 0.648 | 0.776 |
| vanilla_zero_shot | 0.962 | 0.957 | 0.638 | 0.767 |
| acal | 0.956 | 0.950 | 0.399 | 0.563 |
| fol_autoformalizer_solver | 0.898 | 0.900 | 0.762 | 0.824 |

**recall은 우리가 1위(0.994), precision/F1은 하위권.** 라우터가 넓게 열고 하류가 거르는
설계의 직접 반영이다. 단 baseline의 "recall"은 자유서술 텍스트에 죄명이 등장했는지의
substring 매칭이라 개념이 동일하지 않다(§한계).

**KBL Call 2** (인과관계 TRUE/FALSE, N=93)

| method | accuracy | macro-F1 | coverage | unknown |
|---|---:|---:|---:|---:|
| **ours (전체 93, UNKNOWN=오답)** | 0.581 | 0.489 | 0.656 | 0.344 |
| **ours (UNKNOWN 제외 61건)** | **0.885** | 0.650 | 1.0 | 0.0 |
| standard_rag | 0.860 | **0.844** | 1.0 | 0.0 |
| vanilla_zero_shot | 0.860 | 0.844 | 1.0 | 0.0 |
| leprec | 0.849 | 0.833 | 1.0 | 0.0 |
| legal_chain_reasoner | 0.849 | 0.833 | 1.0 | 0.0 |
| fol_autoformalizer_solver | 0.839 | 0.823 | 1.0 | 0.0 |
| chain_of_thought | 0.828 | 0.803 | 1.0 | 0.0 |
| acal | 0.817 | 0.796 | 1.0 | 0.0 |

**이 벤치마크의 진짜 발견은 클래스 비대칭이다.** ours의 per-class:

```
TRUE  (n=65): precision 0.912  recall 0.800  f1 0.852
FALSE (n=28): precision 0.500  recall 0.071  f1 0.125   <- 28건 중 21건이 UNKNOWN
```

즉 **UNKNOWN은 균등한 기권이 아니라 거의 전부 부정 사례에서 나온다.** 폐쇄세계 grounding이
"근거 없음"과 "부정 사실"을 구분하지 못한다는 것이 수치로 잡힌 지점이고, 이게 미완의
`prompts/v2_call2_grounding_binary*.md`(미추적, 미승인)를 만들게 한 동기다.

---

## 2. 코드/브랜치 상태 — 정리 완료 (2026-08-22)

제출 후 갈라져 있던 작업을 한 줄기로 되돌렸다.

| 항목 | 처리 |
|---|---|
| detached HEAD (`3b7f85c`) | `deadline_v2_0808` 브랜치로 복귀 |
| `feature/kbl-binary-mode` 미병합 20커밋 | **머지**(no-ff). conflict 없음 |
| `stash@{0}` (KBL binary mode 작업) | 브랜치 `wip/kbl-binary-grounding`으로 보존 |
| `stash@{1}` (브랜치 전환 전 WIP) | 브랜치 `wip/pre-external-switch`으로 보존 |
| 미추적 프롬프트 2개 | `prompts/candidates/v2_call2_grounding_binary{,_user}_draft.md`로 이동. **미승인 초안이며 어디에도 배선되지 않았다** |
| 외부 벤치마크 결과 문서 | "진행 중" 칸을 최종값으로 채움 |

머지로 들어온 것:

- **외부 벤치마크 harness** — LBOX/KBL 재현 경로 일체(`src/idpr/v2/benchmarks/`,
  `scripts/{prepare,run,evaluate,score}_v2_external_benchmark*.py`)
- **Scallop semantic integrity 패치 6건** — participation principal identity, 초과귀속
  identity, 최종책임 handoff, 일반경합 cycle 거부, completion policy 보존을 Scallop
  emitter에 반영. **논문 수치 생성 이후의 런타임 수정이라 이 코드로 다시 돌린 실험은 없다.**

검증: 머지 트리 기준 pytest는 **conflict 없이 통과**하며, 실패는 아래 2건뿐이다(의도된
회귀 가드 — `voluntary_cessation` 정의 변경 vs 커밋된 plan artifact 괴리, Call 1부터
재실행하면 해소). 임시 워크트리에서 추가로 실패하는 7건은 워크트리에 없는 파일
(`tools/scallop/scli`, 동결 artifact) 때문이지 머지 탓이 아님을 대조로 확인했다.

```
test_carrier_contract.py::test_the_produced_plan_satisfies_the_contract_for_every_producer
test_evidence_scope_carrier_contract.py::test_every_predicate_is_carried_at_its_authored_scope
```

이어서 정리한 것:

- `origin/deadline_v2_0808` 푸시, **`main`을 같은 커밋으로 전진**(이전 187커밋 뒤) 후 푸시.
  다음 연구는 `main`에서 시작하면 된다
- 머지로 흡수된 로컬 브랜치 3개 삭제(`feature/kbl-binary-mode`, `agent/*` 2개)
- vLLM 서비스용 워크트리 3개 제거(473MB 회수) + 사라진 `/tmp` 워크트리 등록 정리.
  현재 워크트리는 `/data5/jaehoonjeong/IDPR` 하나뿐이다
- `wip/*` 두 브랜치를 origin에 백업한 뒤 중복된 stash 2건 삭제. **stash는 비어 있고
  미완 작업은 브랜치로만 남는다**

최종 검증: **`625 passed, 2 failed`**(위 가드 2건). 머지로 들어온 테스트 25개는 전부 통과.

## 3. 미해결 결함 (다음 연구의 출발점)

`docs/analysis/v2_qualitative_cot_vs_idpr_ko.md` §4의 우선순위 + 이후 추적 결과.

1. **라우터 degenerate repetition** — Call 1이 후보 4개에서 멈추고 나머지 슬롯을 같은 죄명
   반복으로 채운다(`assault ×17`). 예산을 distinct로 옮기는 레버는 §9에서 **효과 없음으로
   반증**됐고 사례 1건을 깨서 원상 복구했다. 남은 레버는 디코딩 설정 또는 재요청(recovery)
   이며 둘 다 승인 게이트. 피해는 국소적(2/26)이나 그중 하나가 최대 배점 문항이다.
2. **completion UNKNOWN** — "범행을 단념"이 원문에 명시돼 있는데 completion이 UNKNOWN.
   evidence scope를 행위자 에피소드 폭으로 넓히는 수정은 `voluntary_cessation` 하나만
   적용했고, 유보 상위 6건 중 나머지 5건은 **폭 결함이 아님이 정적 대조로 확인**됐다
   (`r11_p2_q1_ga`는 trailing gap 0). 원인이 남아 있다.
3. **Call 1.5 이중 binding** — 같은 (episode, actor, offense)에 binding 2개가 6/92 그룹.
   그중 3건은 CHAINED(A의 focal이 B의 supporting). 결정론적 병합 규칙은 설계돼 있으나
   "체인의 끝이 실행행위"라는 법적 판단이 뇌물 계열에도 성립하는지 미확인이라 미구현.
   **이걸 고쳐도 답안 죄명 중복 7건 중 2건만 설명된다.**
4. **판례 카드 소비 경로 부재** — 카드 396장을 payload에 실었는데 답안 판례 인용은
   1.1회로 CoT(1.8회)보다 적다. 루브릭이 판례 인용을 직접 배점하므로 채점에 바로 걸린다.
   자산이 아니라 소비 경로의 문제.
5. **죄수(경합)를 심볼릭이 결정하지 못한다** — 저작된 흡수 규칙이 2개뿐이라 26문항에서
   pair 1건, 그마저 UNKNOWN. 답안이 죄수를 명시한 17건은 **전부 프롬프트가 자유롭게 쓴 것**
   이고 dev 케이스에선 루브릭 정반대였다. 구조가 이기는 축으로 주장할 수 없다.
6. **`defeated_by_state`가 Scallop에 미연결** — 중지미수 흡수 규칙이 컴파일러에 없고
   검증기도 같은 결함을 복제해 못 잡는다. 미해결.
7. **규칙베이스 커버리지** — rubric 죄명 173건 중 저작X가 60건(34.7%). 라우터만 조여도
   상한이 26%다. 빠진 것: 협박·강요·제3자뇌물교부/취득·뇌물수수·장물·합동절도·
   주거침입강간(치상/중지미수)·체포·수뢰후부정처사.

---

## 4. 방법론적으로 확정된 제약 (재발 방지)

- **sealed-59**: dev 2건(`r10_p1_q1_ga`, `r14_p1_q2`... 정확히는 `kcl_criminal_r10_p1_q1_ga`,
  `kcl_criminal_r14_p1_q2`)만 열람 가능. 나머지 24건은 형식 스캔만.
- **자동 죄명 커버리지 지표는 우열 판단에 쓰지 않는다.** 같은 질문에 네 번 다른 답을 냈고,
  §1의 실질적 실패(중지미수 부정, 죄수 오답, occurrence 이중계상, 결론 회피) 중 죄명
  목록으로 보이는 것은 하나도 없다.
- **CoT와의 직접 비교는 스코핑이 다르다** — CoT는 제1문 전문을 받고 프롬프트 한 줄로
  스코핑하며, 우리는 host가 잘라 준 입력을 받는다. 우리 강점으로 세지 않기로 했다.
- **Call 2 수정은 국소적이지 않다** — 프롬프트·payload·carrier 변경은 shard 전체를
  최대 10.8% 오염시킨다(노이즈 바닥 0.3%).
