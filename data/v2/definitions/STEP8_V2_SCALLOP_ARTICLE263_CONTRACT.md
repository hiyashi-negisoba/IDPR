# Step 8 — v2 Scallop Article 263 backend-completion 계약

상태: **freeze 완료** (2026-08-11)

## 목적

generic Step 5 liability-chain을 변경하지 않고, Step 7이 이미 선택한 Article 263
statutory-deeming 경로의 runtime 평가를 Scallop backend로 이행한다.

```text
Step 7 surviving Article 263 probe (caller-owned, 재판정 금지)
  -> Step 3 completion / 기존 직접 Elements obligation (Scallop)
  -> Article 263 statutory-deeming ALL truth (Scallop)
  -> combined Elements fold (기존 StatutoryDeemingObligation 포함)
  -> non-speculative stage tail (Scallop)
  -> 기존 LiabilityEvaluation / LiabilityResult
```

## 고정 입력·출력 경계

- 입력 target은 `statutory_deeming` constraint를 가진 이미 컴파일된 offense와 기존
  `OffenseInstanceKey`다. 현재 production의 유일한 opt-in은 `offense.injury`다.
- Step 7이 probe를 surviving candidate로 선택하는 일, Call 2 factual v0, Call 3,
  Definition Layer, 모델 호출은 범위 밖이다.
- 출력은 기존 `LiabilityEvaluation`과 조건부 `LiabilityResult`뿐이다. 새 offense
  identity, binding carrier, participation mode, legal abstraction을 만들지 않는다.

## Scallop truth 및 adapter

statutory truth는 checked `statutory_deeming.requires`의 세 Article 19 leaves와 기존
`legal_element.injury_result`를 `ALL`로 fold한다. 별도 query의 정확한 key set은
authorised target마다 한 행이며 truth는 `TRUE | FALSE | UNKNOWN`이다.

adapter는 completion이 실제로 Elements를 허용한 경우에만 다음 기존 provenance를
추가한다.

```text
ObligationOutcome(
  StatutoryDeemingObligation(underlying_instance=target),
  statutory_truth,
)
```

최종 Elements truth는 기존 Step 5 direct obligation truth들과 statutory truth의
`fold_all`이다. FALSE obligation이 하나면 기존 `decisive_obligation` 규칙에 따라
statutory obligation이 기록되고, 여러 FALSE면 `None`이다.

## 비가설적 stage 규칙

- completion 중단이면 Elements 및 뒤 stage는 `not_reached`이며 statutory provenance를
  결과에 붙이지 않는다.
- combined Elements가 `FALSE` 또는 `UNKNOWN`이면 doctrine stage를 호출하지 않고 모두
  `not_reached`로 복원한다.
- combined Elements가 `TRUE`일 때만 Unlawfulness -> Culpability -> Punishability를
  이전 Scallop gate가 `passes`인 경우에만 순서대로 실행한다.

## 금지 사항

- `apply_attribution()` 또는 source actor truth merge 금지
- `offense_ref=263` 생성 금지
- Python `resolve_article_263_deemed_liability()` 또는
  `pipeline.resolve_liability()`를 backend runtime oracle로 호출 금지
- generic Step 5, frozen Step 1–4 public contract, Step 7 probe producer 변경 금지

## 완료 조건

Article 263 TRUE/FALSE/UNKNOWN statutory truth, completion stop, doctrine-stage stop 및
typed conclusion/provenance가 기존 dedicated Python runtime과 field-by-field parity를
보인다. backend 경로는 Python statutory/pipeline resolver를 monkeypatch해도 실행되어야
한다.

## Acceptance evidence

`tests/test_v2_scallop_backend_step5.py`는 다음을 dedicated Python runtime과
field-by-field 비교한다.

- statutory truth `TRUE | FALSE | UNKNOWN`
- synthetic completion `unresolved` stop: Elements 이하 `not_reached`, statutory
  provenance 없음 (production Definition Layer 변경 없음)
- active `doctrine.self_defense`의 Unlawfulness defeat 및
  `doctrine.juvenile_defeat`의 Culpability defeat: 이후 stage `not_reached`
- Python `resolve_article_263_deemed_liability()`와
  `pipeline.resolve_liability()`를 금지한 backend 실행
