# 다음 세션 안내 — ICLR 트랙

기준 2026-08-22 · 브랜치 `deadline_v2_0808` (= `main`, origin 푸시됨)
검증 기준선 `625 passed, 2 failed` (conda **base**)

## 한 줄 상태

**논문 제출과 레포 정리는 끝났다. ICLR 트랙은 계획이 확정 단계이고 실행은 0이다.**
이번 세션에서 만든 것은 문서 둘뿐이다 — 코드 변경 없음, GPU·API 사용 없음.

## 읽는 순서

1. `docs/handoff/WRAPUP_SUBMISSION_2026-08-22.md` — 제출 시점 상태·최종 수치·미해결 결함 7건
2. **`docs/research/ICLR_TRACK_PLAN.md`** — 이 트랙의 정본. 아래 요약은 이걸 대체하지 않는다
3. `docs/analysis/v2_qualitative_cot_vs_idpr_ko.md` — 우리 시스템의 실패 성격 (필요할 때)

`START_HERE.md`와 `NEXT_SESSION.md`는 데드라인 기준 문서라 **만료**다.

---

## 확정된 것 — 되묻지 말 것

사용자가 여러 턴에 걸쳐 결정한 것들이다. 다시 열지 말고, 바꾸려면 근거를 갖고 제안하라.

| | 결정 |
|---|---|
| **학습** | **하지 않는다.** test-time 조향만. 신뢰도 파라미터 학습은 마지막 절 확장으로만 언급 |
| **조향의 뜻** | 점수를 손으로 미는 것이 아니라, 지목된 체인에 대해 **모델이 논증을 다시 쓰게 하는 것**. 공격본 / 방어본 두 개 |
| **판정** | 숫자 둘. 이동량 `D = Σ|s'−s|`, 접지율 `G = 원문 확인 전제 / 내세운 전제`. **LLM judge를 새로 부르지 않는다** — G는 기존 Call 2 재사용 |
| **법리 판단** | 우리가 재지 않는다. gold(`crime_type`)가 채점한다 |
| **단위** | predicate가 아니라 **chain**. (중간에 predicate로 접었다가 되돌린 이력이 있다) |
| **코어 죄명** | 재산죄(사기·횡령·업무상횡령) = 구성요건 훈련장 / 폭력죄(폭행·상해·재물손괴) = 위법성 훈련장. 특수상해·야간건조물침입절도는 **제외**(무죄가 거의 없다) |
| **책임 조각** | 주장에 넣지 않는다(커버 슬라이스 전체 63건). 정성 관찰만 |
| **양형** | 주 타깃 아님. "공유된 원자 판단 위의 두 번째 head"로만, 일반 언어로만 서술 |
| **DCDE** | EMNLP 2026 main accept. **인용 대상이자 직접 붙는 baseline** |
| **반사실 데이터** | `new_fact` 말고 **원본/중립 버전**을 쓴다 |

## 열린 결정 — 사용자 답을 받아야 한다

1. 부 테스트베드 확정 (주장 검증 계열 중 무엇)
2. 무죄 범주 불균형을 macro로 볼지 support 가중으로 볼지
3. 논증본에서 전제를 뽑아 요건 형태로 만드는 단계 — 별도 호출인가, 논증 생성 시 함께 구조화인가

---

## 절대 하지 말 것

- **Phase 1 게이트 전에 파일럿·배관 착수 금지.** 게이트는 "gold 결론을 손으로 넣었을 때
  우리 사다리가 `crime_type` 4치를 재현하는가"이고 **모델 없이** 돈다. 여기가 안 되면
  scallopy 전환도 logprob 수집도 전부 헛돈다
- **용어를 뭉뚱그리지 말 것.** 계획서 §2.0이 `s` / `v` / `Δs`를 기호로 못 박아 뒀다.
  "점수"라고만 쓰면 다음 세션으로 오류가 전파된다 (이번 세션에서 실제로 그랬고 사용자가 잡았다)
- 승인 게이트: 활성 프롬프트·정의 전문은 사용자 승인 후 설치, 유료 API 호출은 비용 추정과 함께
- 긴 작업·GPU 작업은 길이 무관 **항상 sbatch**, `IDPR_HF_HOME` 필수, job 백그라운드 폴링 금지
- pytest는 conda **base** (`/data5/jaehoonjeong/miniconda3/bin/python`)

---

## 사실 확인 — 추측하지 말고 여기를 볼 것

**Scallop 실행은 CLI subprocess다.** `src/idpr/rulebase/scallop.py:212`가 `scli-0.2.4` 바이너리를
부른다. 프로덕션은 unit provenance이고, 확률 경로(`run_probabilistic_program`, 260행)는
`topkproofs/minmaxprob/addmultprob`만 지원하며 주석에 experimental이라 적혀 있다.
**미분 가능 경로가 없다** — gradient를 쓰려면 scallopy(torch) 전환이 필요하다.

**요건 점수는 지금 존재하지 않는다.** 레포 어디에도 logprob 수집이 없고, 호스트가 검증한 뒤
`satisfied / not_satisfied / unknown` 3치 라벨로 렌더한다.

**데이터 위치**

```
DCDE            /data5/jaehoonjeong/DCDE/data/GOLD/natural_innocent.json      3,412건 (한국어 실판결)
                /data5/jaehoonjeong/DCDE/data/GOLD/natural_guilty_only.json   1,291건
                crime_type: 0=유죄 · 1=구성요건불성립 · 2=위법성조각 · 3=책임조각
                (2/3의 의미는 DCDE `scripts/post_process.py`의 JUST/CULP 키워드 주석에서 확인)
LBOX LJP        HF 캐시 lbox_open/legal_judgement_prediction/criminal          8,400/1,050/1,050
저작 죄명 69개   data/v2/definitions/{offenses,derived_offenses}.yaml
```

**이번 세션에서 계산해 둔 수치**(다시 재지 말 것, 재현 필요하면 위 경로에서)

- DCDE 커버율: 무죄 65.8% · 유죄 77.8%
- 죄명 × 무죄단계 교차표: 계획서 §5.1
- LBOX 총칙 감경 발동률 0.1~0.3%, 자유형 개월수 분산의 71.2%가 죄종 내부

---

## 이번 세션이 한 일

1. 제출 시점 상태 갈무리 → `WRAPUP_SUBMISSION_2026-08-22.md`
2. 레포 정리 — 머지(외부 벤치마크 harness + Scallop semantic integrity 패치 6건), main 전진,
   stash → `wip/*` 브랜치 백업, 워크트리 3개 제거
3. ICLR 트랙 계획 수립 → `ICLR_TRACK_PLAN.md`

**주의:** 논문 수치는 semantic integrity 패치가 머지되기 **전** 코드로 생성됐다. 재실행하면
달라질 수 있다.
