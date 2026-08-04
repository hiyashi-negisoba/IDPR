# P2 학설선택 구조화 감사

- authoritative source: `data/rulegen/p2/결정C_학설선택.md`
- source SHA-256: `db57f382c45eec76070324e7d029a9bd16de32a21eec874263d979fecb482ad9`
- decision groups: 31
- valid groups: 31
- invalid groups: 0
- legacy option order reconciliations: 3
- expert overrides: 2
- card-catalog mismatch groups: 2
- selected cards absent from current RuleIR units: 30

유효한 기존 선택은 후속 검수 패킷에서 자동 계승한다. 범위를 벗어난 번호는 추정하지 않는다.
선택 카드가 RuleIR unit에 없다는 것은 선택이 폐기됐다는 뜻이 아니라, Markdown 선택과 카드 승격이
아직 연결되지 않았다는 뜻이다.

## 기존 응답 불일치

없음.

## 법률전문가 재정으로 대체된 선택

- #5 `art164_sec3_6.intentional_fire_death_murder_concurrence`
  - 원래 선택: `art164_sec3_6.intentional_fire_death_murder_concurrence_affirmative`
  - 재정 선택: `art164_sec3_6.intentional_fire_death_murder_concurrence_negative`
  - 사안: 보통 사람을 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우
  - 결론: 현주건조물방화치사죄만 성립하고 살인죄는 여기에 흡수된다. 살인죄와의 상상적 경합을 인정하지 않는다.
  - 근거: 보통살인죄의 법정형(사형·무기 또는 5년 이상의 징역)이 현주건조물방화치사죄의 법정형(사형·무기 또는 7년 이상의 징역)보다 무겁지 않으므로 법조경합에 해당한다.
  - 대체 이유: 결정C_학설선택.md에서 선택된 긍정설은 학설의 시각이며 대법원 판례의 입장이 아니다
  - 판례 인용 상태: 사건번호 미확인 — 1차 판례 색인 대조 필요
- #15 `art250_sec2_10.arson_death_parricide_concurrence`
  - 원래 선택: `art250_sec2_10.arson_death_parricide_specialty_precedent`
  - 재정 선택: `art250_sec2_10.arson_death_parricide_imaginary_concurrence`
  - 사안: 직계존속을 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우
  - 결론: 존속살해죄와 현주건조물방화치사죄의 상상적 경합이 성립하고 중한 존속살해죄로 처단한다.
  - 근거: 존속살해죄는 형법 제256조의 자격정지 병과 규정 등으로 현주건조물방화치사죄보다 실질적으로 중하게 처벌할 수 있는 규정을 두고 있으므로 법조경합이 아니라 상상적 경합에 해당한다.
  - 대체 이유: 결정C_학설선택.md가 선택한 서울고등법원 2010노252 판결은 하급심 판단이며 대법원은 상상적 경합을 유지한다
  - 판례 인용 상태: 제공됨 — 판결 원문 대조는 미완

## 축약 전 선택지 순서로 복원

- #13 `art250_sec1_3.death_onset` raw=`(3)` → `art250_sec1_3.pulse_cessation_organ_removal`
- #16 `art250_sec2_6.adoptee_biological_parent_offense` raw=`(3)` → `art250_sec2_6.adoption_type_determines_offense`
- #28 `art301_sec4_6.pregnancy_injury` raw=`(3)` → `art301_sec4_6.unwanted_pregnancy_not_injury_holding`

## 카드 카탈로그 불일치

- #24 `art259_sec1_1.second_act_liability`: remediated card missing: art259_sec1_1.second_act.concurrence_view (선택 카드가 존재하면 기존 선택 자체는 계승)
- #30 `art319_sec2_1.dwelling_concept`: remediated card missing: art319_sec2_1.common_area_classification (선택 카드가 존재하면 기존 선택 자체는 계승)

## RuleIR 미연결 선택 카드

- `art152_sec1_6.perjury_evidence_destruction_special_relation`
- `art164_sec2_1.post_killing_arson_precedent`
- `art164_sec2_1.completion_independent_combustion_variant`
- `art164_sec3_2.attempted_basic_arson_included`
- `art164_sec3_6.intentional_fire_death_murder_concurrence_negative`
- `art227_sec3_2.assistant_indirect_perpetration_affirmative`
- `art250_sec1_11.indirect_perpetration_attempt_use_act`
- `art250_sec1_17.direct_active_euthanasia_negative`
- `art250_sec1_19.excessive_execution_death_precedent`
- `art250_sec1_21.death_penalty_special_circumstances_majority`
- `art250_sec1_3.birth_labor_theory`
- `art250_sec1_3.pulse_cessation_organ_removal`
- `art250_sec1_3.organ_transplant_law_limited_effect`
- `art250_sec2_10.arson_death_parricide_imaginary_concurrence`
- `art250_sec2_6.adoption_type_determines_offense`
- `art250_sec2_6.deceased_spouse_lineal_ascendant_ordinary_murder`
- `art250_sec2_9.nonstatus_accomplice_parricide_coprincipal_punished_ordinary`
- `art250_sec2_9.status_instigator_parricide_accomplice`
- `art255_sec4.preparation_desistance_doctrinal_variants`
- `art257_sec1_2.prenatal_injury_postnatal_result_negative`
- `art257.pregnancy_not_injury`
- `art257.drug_intangible_method`
- `art259_sec1_1.second_act.single_offense_holding`
- `art268.illicit_work_excluded`
- `art298_sec3_2.indecent_act_no_body_part_distinction`
- `art299_sec7.changed_circumstances_rape_only`
- `art301_sec4_6.unwanted_pregnancy_not_injury_holding`
- `art301_sec7.special_rape_injury_completed`
- `art319_sec2_1.dwelling_concept_sleeping`
- `art319_sec5_2.private_arrest_home_entry_affirmative`
