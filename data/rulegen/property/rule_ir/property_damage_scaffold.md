# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.property_damage.full.v1_candidate`
- predicate: 177개
- rule: 276개
- NormCard: 53개

## Predicate

### `provable(case_id: String, assessment_id: String)`

해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `case_assessment_complete(case_id: String, defendant_id: String)`

라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `distinct_entity(case_id: String, left_entity_id: String, right_entity_id: String)`

두 역할에 배정된 entity가 서로 다른 사람임

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `property_damage_case_roles(case_id: String, defendant_id: String, owner_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art366_alternative_use_property(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.alternative_use_property`

### `satisfied_art366_alternative_use_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`

### `not_satisfied_satisfied_art366_alternative_use_property(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`

### `assess_art366_cloud_provider_delete_record(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.cloud_provider_delete_record`

### `satisfied_art366_cloud_provider_delete_record(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.cloud_provider_delete_record`

### `not_satisfied_satisfied_art366_cloud_provider_delete_record(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.cloud_provider_delete_record`

### `assess_art366_corpse_exclusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.corpse_exclusion`

### `satisfied_art366_corpse_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.corpse_exclusion`

### `not_satisfied_satisfied_art366_corpse_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.corpse_exclusion`

### `assess_art366_document_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.document_definition`

### `satisfied_art366_document_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.document_definition`

### `not_satisfied_satisfied_art366_document_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.document_definition`

### `assess_art366_electronic_record_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.electronic_record_definition`

### `satisfied_art366_electronic_record_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_definition`

### `not_satisfied_satisfied_art366_electronic_record_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_definition`

### `assess_art366_electronic_record_durability(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.electronic_record_durability`

### `satisfied_art366_electronic_record_durability(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_durability`

### `not_satisfied_satisfied_art366_electronic_record_durability(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_durability`

### `assess_art366_electronic_record_erasure(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.electronic_record_erasure`

### `satisfied_art366_electronic_record_erasure(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_erasure`

### `not_satisfied_satisfied_art366_electronic_record_erasure(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.electronic_record_erasure`

### `assess_art366_fact_certification_private_document(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.fact_certification_private_document`

### `satisfied_art366_fact_certification_private_document(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.fact_certification_private_document`

### `not_satisfied_satisfied_art366_fact_certification_private_document(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.fact_certification_private_document`

### `assess_art366_medium_damage_property_damage(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.medium_damage_property_damage`

### `satisfied_art366_medium_damage_property_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.medium_damage_property_damage`

### `not_satisfied_satisfied_art366_medium_damage_property_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.medium_damage_property_damage`

### `assess_art366_no_utility_property_exclusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.no_utility_property_exclusion`

### `satisfied_art366_no_utility_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.no_utility_property_exclusion`

### `not_satisfied_satisfied_art366_no_utility_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.no_utility_property_exclusion`

### `assess_art366_object_manageable_energy(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.object_manageable_energy`

### `satisfied_art366_object_manageable_energy(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.object_manageable_energy`

### `not_satisfied_satisfied_art366_object_manageable_energy(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.object_manageable_energy`

### `assess_art366_other_person_ownership(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.other_person_ownership`

### `satisfied_art366_other_person_ownership(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.other_person_ownership`

### `not_satisfied_satisfied_art366_other_person_ownership(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.other_person_ownership`

### `assess_art366_ownerless_property_exclusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.ownerless_property_exclusion`

### `satisfied_art366_ownerless_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.ownerless_property_exclusion`

### `not_satisfied_satisfied_art366_ownerless_property_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.ownerless_property_exclusion`

### `assess_art366_property_object_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.property_object_definition`

### `satisfied_art366_property_object_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.property_object_definition`

### `not_satisfied_satisfied_art366_property_object_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.property_object_definition`

### `assess_art366_public_building_affirmative_view(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.public_building_affirmative_view`

### `satisfied_art366_public_building_affirmative_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_building_affirmative_view`

### `not_satisfied_satisfied_art366_public_building_affirmative_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_building_affirmative_view`

### `assess_art366_public_document_used_by_office(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.public_document_used_by_office`

### `satisfied_art366_public_document_used_by_office(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_document_used_by_office`

### `not_satisfied_satisfied_art366_public_document_used_by_office(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_document_used_by_office`

### `assess_art366_public_interest_building_non_destruction(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.public_interest_building_non_destruction`

### `satisfied_art366_public_interest_building_non_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_interest_building_non_destruction`

### `not_satisfied_satisfied_art366_public_interest_building_non_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_interest_building_non_destruction`

### `assess_art366_record_medium_information_combination(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.record_medium_information_combination`

### `satisfied_art366_record_medium_information_combination(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.record_medium_information_combination`

### `not_satisfied_satisfied_art366_record_medium_information_combination(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.record_medium_information_combination`

### `assess_art366_separated_human_material(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.separated_human_material`

### `satisfied_art366_separated_human_material(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.separated_human_material`

### `not_satisfied_satisfied_art366_separated_human_material(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.separated_human_material`

### `assess_art366_shared_property_damage(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.shared_property_damage`

### `satisfied_art366_shared_property_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.shared_property_damage`

### `not_satisfied_satisfied_art366_shared_property_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.shared_property_damage`

### `assess_art366_special_medium_record_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.special_medium_record_definition`

### `satisfied_art366_special_medium_record_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.special_medium_record_definition`

### `not_satisfied_satisfied_art366_special_medium_record_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.special_medium_record_definition`

### `assess_art366_special_medium_record_limited_view(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366.special_medium_record_limited_view`

### `satisfied_art366_special_medium_record_limited_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.special_medium_record_limited_view`

### `not_satisfied_satisfied_art366_special_medium_record_limited_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.special_medium_record_limited_view`

### `assess_art366_transmitting_or_processing_information_exclusion(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

### `satisfied_art366_transmitting_or_processing_information_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

### `not_satisfied_satisfied_art366_transmitting_or_processing_information_exclusion(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

### `assess_art366_sec3_2_concealment_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.concealment_definition`

### `satisfied_art366_sec3_2_concealment_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_definition`

### `not_satisfied_satisfied_art366_sec3_2_concealment_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_definition`

### `assess_art366_sec3_2_concealment_no_possession_required(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

### `satisfied_art366_sec3_2_concealment_no_possession_required(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

### `not_satisfied_satisfied_art366_sec3_2_concealment_no_possession_required(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

### `assess_art366_sec3_2_concealment_temporary_and_return_intent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

### `satisfied_art366_sec3_2_concealment_temporary_and_return_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

### `not_satisfied_satisfied_art366_sec3_2_concealment_temporary_and_return_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

### `assess_art366_sec3_2_destruction_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.destruction_definition`

### `satisfied_art366_sec3_2_destruction_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.destruction_definition`

### `not_satisfied_satisfied_art366_sec3_2_destruction_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.destruction_definition`

### `assess_art366_sec3_2_destruction_no_irreparable_damage(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

### `satisfied_art366_sec3_2_destruction_no_irreparable_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

### `not_satisfied_satisfied_art366_sec3_2_destruction_no_irreparable_damage(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

### `assess_art366_sec3_2_document_margin_removal(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.document_margin_removal`

### `satisfied_art366_sec3_2_document_margin_removal(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_margin_removal`

### `not_satisfied_satisfied_art366_sec3_2_document_margin_removal(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_margin_removal`

### `assess_art366_sec3_2_document_removal_against_owner_intent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

### `satisfied_art366_sec3_2_document_removal_against_owner_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

### `not_satisfied_satisfied_art366_sec3_2_document_removal_against_owner_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

### `assess_art366_sec3_2_document_removal_without_owner_intent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

### `satisfied_art366_sec3_2_document_removal_without_owner_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

### `not_satisfied_satisfied_art366_sec3_2_document_removal_without_owner_intent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

### `assess_art366_sec3_2_electronic_file_metadata_concealment(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

### `satisfied_art366_sec3_2_electronic_file_metadata_concealment(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

### `not_satisfied_satisfied_art366_sec3_2_electronic_file_metadata_concealment(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

### `assess_art366_sec3_2_electronic_record_other_methods_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

### `satisfied_art366_sec3_2_electronic_record_other_methods_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

### `not_satisfied_satisfied_art366_sec3_2_electronic_record_other_methods_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

### `assess_art366_sec3_2_electronic_record_power_cutoff_exception(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

### `satisfied_art366_sec3_2_electronic_record_power_cutoff_exception(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

### `not_satisfied_satisfied_art366_sec3_2_electronic_record_power_cutoff_exception(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

### `assess_art366_sec3_2_emotional_use_majority_position(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

### `satisfied_art366_sec3_2_emotional_use_majority_position(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

### `not_satisfied_satisfied_art366_sec3_2_emotional_use_majority_position(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

### `assess_art366_sec3_2_mere_functional_interference_not_destruction(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

### `satisfied_art366_sec3_2_mere_functional_interference_not_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

### `not_satisfied_satisfied_art366_sec3_2_mere_functional_interference_not_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

### `assess_art366_sec3_2_movement_no_objective_use_value(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

### `satisfied_art366_sec3_2_movement_no_objective_use_value(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

### `not_satisfied_satisfied_art366_sec3_2_movement_no_objective_use_value(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

### `assess_art366_sec3_2_movement_objective_use_value(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.movement_objective_use_value`

### `satisfied_art366_sec3_2_movement_objective_use_value(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.movement_objective_use_value`

### `not_satisfied_satisfied_art366_sec3_2_movement_objective_use_value(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.movement_objective_use_value`

### `assess_art366_sec3_2_other_method_efficiency_harm_definition(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

### `satisfied_art366_sec3_2_other_method_efficiency_harm_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

### `not_satisfied_satisfied_art366_sec3_2_other_method_efficiency_harm_definition(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

### `assess_art366_sec3_2_other_method_temporary_unusable(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

### `satisfied_art366_sec3_2_other_method_temporary_unusable(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

### `not_satisfied_satisfied_art366_sec3_2_other_method_temporary_unusable(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

### `assess_art366_sec3_2_preservation_state_change_view(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.preservation_state_change_view`

### `satisfied_art366_sec3_2_preservation_state_change_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.preservation_state_change_view`

### `not_satisfied_satisfied_art366_sec3_2_preservation_state_change_view(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.preservation_state_change_view`

### `assess_art366_sec3_2_road_graffiti_totality(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.road_graffiti_totality`

### `satisfied_art366_sec3_2_road_graffiti_totality(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.road_graffiti_totality`

### `not_satisfied_satisfied_art366_sec3_2_road_graffiti_totality(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.road_graffiti_totality`

### `assess_art366_sec3_2_wall_graffiti_functional_efficiency_limit(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

### `satisfied_art366_sec3_2_wall_graffiti_functional_efficiency_limit(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

### `not_satisfied_satisfied_art366_sec3_2_wall_graffiti_functional_efficiency_limit(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

### `assess_art366_sec3_2_wall_graffiti_totality(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

### `satisfied_art366_sec3_2_wall_graffiti_totality(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

### `not_satisfied_satisfied_art366_sec3_2_wall_graffiti_totality(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

### `assess_art366_sec3_3_completion_efficiency_injury(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

### `satisfied_art366_sec3_3_completion_efficiency_injury(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

### `not_satisfied_satisfied_art366_sec3_3_completion_efficiency_injury(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

### `assess_art366_sec4_1_intent_absence(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec4_1.intent_absence`

### `satisfied_art366_sec4_1_intent_absence(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_absence`

### `not_satisfied_satisfied_art366_sec4_1_intent_absence(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_absence`

### `assess_art366_sec4_1_intent_awareness(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec4_1.intent_awareness`

### `satisfied_art366_sec4_1_intent_awareness(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_awareness`

### `not_satisfied_satisfied_art366_sec4_1_intent_awareness(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_awareness`

### `assess_art366_sec4_1_intent_conditional_sufficiency(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

### `satisfied_art366_sec4_1_intent_conditional_sufficiency(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

### `not_satisfied_satisfied_art366_sec4_1_intent_conditional_sufficiency(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

### `assess_art366_sec5_2_immediate_self_recovery_assessment(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

### `satisfied_art366_sec5_2_immediate_self_recovery_assessment(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

### `not_satisfied_satisfied_art366_sec5_2_immediate_self_recovery_assessment(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

### `assess_art366_sec5_2_justifiable_act_requirements(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

### `satisfied_art366_sec5_2_justifiable_act_requirements(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

### `not_satisfied_satisfied_art366_sec5_2_justifiable_act_requirements(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

### `assess_art366_sec5_2_possession_protection_destruction(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec5_2.possession_protection_destruction`

### `satisfied_art366_sec5_2_possession_protection_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.possession_protection_destruction`

### `not_satisfied_satisfied_art366_sec5_2_possession_protection_destruction(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.possession_protection_destruction`

### `assess_art366_sec5_2_socially_acceptable_act(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec5_2.socially_acceptable_act`

### `satisfied_art366_sec5_2_socially_acceptable_act(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.socially_acceptable_act`

### `not_satisfied_satisfied_art366_sec5_2_socially_acceptable_act(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_2.socially_acceptable_act`

### `assess_art366_sec5_5_presumed_consent(case_id: String, assessment_id: String, defendant_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art366_sec5_5.presumed_consent`

### `satisfied_art366_sec5_5_presumed_consent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_5.presumed_consent`

### `not_satisfied_satisfied_art366_sec5_5_presumed_consent(case_id: String, defendant_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec5_5.presumed_consent`

### `property_damage_object_satisfied(case_id: String, defendant_id: String, owner_id: String)`

객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`

### `property_damage_conduct_satisfied(case_id: String, defendant_id: String, owner_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`

### `property_damage_intent_satisfied(case_id: String, defendant_id: String, owner_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

### `property_damage_completion_satisfied(case_id: String, defendant_id: String, owner_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

### `property_damage_elements_satisfied(case_id: String, defendant_id: String, owner_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

### `property_damage_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.corpse_exclusion`, `art366.no_utility_property_exclusion`, `art366.ownerless_property_exclusion`, `art366.public_document_used_by_office`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec4_1.intent_absence`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

### `property_damage_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.corpse_exclusion`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.no_utility_property_exclusion`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.ownerless_property_exclusion`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_document_used_by_office`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_absence`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

### `property_damage_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.corpse_exclusion`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.no_utility_property_exclusion`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.ownerless_property_exclusion`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_document_used_by_office`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_absence`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

### `property_damage_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.corpse_exclusion`, `art366.no_utility_property_exclusion`, `art366.ownerless_property_exclusion`, `art366.public_document_used_by_office`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec4_1.intent_absence`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

### `property_damage_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.corpse_exclusion`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.no_utility_property_exclusion`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.ownerless_property_exclusion`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_document_used_by_office`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_absence`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

### `property_damage_established(case_id: String, defendant_id: String, owner_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

### `property_damage_boundary_shift(case_id: String, defendant_id: String, issue_id: String)`

이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_document_used_by_office`

### `property_damage_refers_to_crime(case_id: String, defendant_id: String, crime_name: String)`

이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.public_document_used_by_office`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

## Rules

### `property_damage.art366.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.alternative_use_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.alternative_use_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.alternative_use_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.alternative_use_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.cloud_provider_delete_record`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.cloud_provider_delete_record`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.cloud_provider_delete_record`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.cloud_provider_delete_record`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.corpse_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.corpse_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.corpse_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.corpse_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.document_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.document_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.document_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.document_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_durability`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_durability`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_durability`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_durability`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_erasure`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_erasure`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_erasure`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.electronic_record_erasure`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.fact_certification_private_document`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.fact_certification_private_document`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.fact_certification_private_document`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.fact_certification_private_document`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.medium_damage_property_damage`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.medium_damage_property_damage`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.medium_damage_property_damage`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.medium_damage_property_damage`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.no_utility_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.no_utility_property_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.no_utility_property_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.no_utility_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.object_manageable_energy`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.object_manageable_energy`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.object_manageable_energy`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.object_manageable_energy`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.other_person_ownership`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.other_person_ownership`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.other_person_ownership`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.other_person_ownership`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.ownerless_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.ownerless_property_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.ownerless_property_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.ownerless_property_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.property_object_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.property_object_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.property_object_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.property_object_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_building_affirmative_view`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_building_affirmative_view`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_building_affirmative_view`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.015.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_building_affirmative_view`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.016.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_interest_building_non_destruction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_interest_building_non_destruction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_interest_building_non_destruction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.017.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.public_interest_building_non_destruction`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.record_medium_information_combination`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.record_medium_information_combination`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.record_medium_information_combination`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.018.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.record_medium_information_combination`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.separated_human_material`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.separated_human_material`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.separated_human_material`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.019.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.separated_human_material`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.shared_property_damage`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.shared_property_damage`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.shared_property_damage`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.020.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.shared_property_damage`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.021.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_limited_view`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_limited_view`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_limited_view`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.022.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.special_medium_record_limited_view`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366.card.023.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.024.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.025.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.026.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.027.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.028.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_margin_removal`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_margin_removal`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_margin_removal`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.029.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_margin_removal`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.030.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.031.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.032.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.033.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.034.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.035.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.036.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.037.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_objective_use_value`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_objective_use_value`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_objective_use_value`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.038.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.movement_objective_use_value`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.039.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.040.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.preservation_state_change_view`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.preservation_state_change_view`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.preservation_state_change_view`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.041.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.preservation_state_change_view`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.042.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.road_graffiti_totality`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.042.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.road_graffiti_totality`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.042.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.road_graffiti_totality`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.042.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.road_graffiti_totality`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.043.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.043.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.043.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.043.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.044.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_2.card.044.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_2.card.044.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_2.card.044.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec3_3.card.045.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec3_3.card.045.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec3_3.card.045.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec3_3.card.045.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.046.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_absence`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.046.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_absence`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec4_1.card.046.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_absence`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec4_1.card.046.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_absence`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.047.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_awareness`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.047.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_awareness`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec4_1.card.047.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_awareness`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec4_1.card.047.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_awareness`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.048.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec4_1.card.048.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec4_1.card.048.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec4_1.card.048.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.049.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.049.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec5_2.card.049.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec5_2.card.049.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.050.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.050.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec5_2.card.050.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec5_2.card.050.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.051.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.possession_protection_destruction`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.051.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.possession_protection_destruction`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec5_2.card.051.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.possession_protection_destruction`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec5_2.card.051.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.possession_protection_destruction`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.052.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.socially_acceptable_act`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec5_2.card.052.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.socially_acceptable_act`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec5_2.card.052.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.socially_acceptable_act`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec5_2.card.052.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_2.socially_acceptable_act`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366_sec5_5.card.053.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_5.presumed_consent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `property_damage.art366_sec5_5.card.053.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_5.presumed_consent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `property_damage.art366_sec5_5.card.053.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_5.presumed_consent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `property_damage.art366_sec5_5.card.053.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art366_sec5_5.presumed_consent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `property_damage.art366.component.property_damage_object_satisfied.01`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.

연결 NormCard: `art366.alternative_use_property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.02`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.

연결 NormCard: `art366.cloud_provider_delete_record`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.03`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.

연결 NormCard: `art366.document_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.04`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.

연결 NormCard: `art366.electronic_record_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.05`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.

연결 NormCard: `art366.electronic_record_durability`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.06`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.

연결 NormCard: `art366.electronic_record_erasure`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.07`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.

연결 NormCard: `art366.fact_certification_private_document`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.08`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.

연결 NormCard: `art366.medium_damage_property_damage`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.09`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.

연결 NormCard: `art366.object_manageable_energy`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.10`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.

연결 NormCard: `art366.other_person_ownership`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.11`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.

연결 NormCard: `art366.property_object_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.12`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.

연결 NormCard: `art366.public_building_affirmative_view`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.13`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.

연결 NormCard: `art366.public_interest_building_non_destruction`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.14`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.

연결 NormCard: `art366.record_medium_information_combination`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.15`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.

연결 NormCard: `art366.separated_human_material`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.16`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.

연결 NormCard: `art366.shared_property_damage`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.17`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.

연결 NormCard: `art366.special_medium_record_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.component.property_damage_object_satisfied.18`

이 규칙은 **객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.

연결 NormCard: `art366.special_medium_record_limited_view`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.

연결 NormCard: `art366_sec3_2.concealment_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.

연결 NormCard: `art366_sec3_2.concealment_no_possession_required`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.

연결 NormCard: `art366_sec3_2.concealment_temporary_and_return_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.

연결 NormCard: `art366_sec3_2.destruction_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.

연결 NormCard: `art366_sec3_2.destruction_no_irreparable_damage`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.

연결 NormCard: `art366_sec3_2.document_margin_removal`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.

연결 NormCard: `art366_sec3_2.document_removal_against_owner_intent`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.08`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.

연결 NormCard: `art366_sec3_2.electronic_file_metadata_concealment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.09`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.

연결 NormCard: `art366_sec3_2.electronic_record_other_methods_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.10`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.

연결 NormCard: `art366_sec3_2.emotional_use_majority_position`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.11`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.

연결 NormCard: `art366_sec3_2.movement_objective_use_value`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.12`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.

연결 NormCard: `art366_sec3_2.other_method_efficiency_harm_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.13`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.

연결 NormCard: `art366_sec3_2.other_method_temporary_unusable`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.14`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.

연결 NormCard: `art366_sec3_2.preservation_state_change_view`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.15`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

연결 NormCard: `art366_sec3_2.road_graffiti_totality`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.16`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.

연결 NormCard: `art366_sec3_2.wall_graffiti_functional_efficiency_limit`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_2.component.property_damage_conduct_satisfied.17`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

연결 NormCard: `art366_sec3_2.wall_graffiti_totality`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec4_1.component.property_damage_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.

연결 NormCard: `art366_sec4_1.intent_awareness`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec4_1.component.property_damage_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.

연결 NormCard: `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366_sec3_3.component.property_damage_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `property_damage.art366.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 해부용 사체를 포함한 사체는 제366조의 범행객체인 재물에 해당하지 않는다.

연결 NormCard: `art366.corpse_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 주관적으로나 객관적으로 이용가치 또는 효용이 전혀 없는 물건은 재물성이 인정되지 않을 수 있다.

연결 NormCard: `art366.no_utility_property_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.

연결 NormCard: `art366.ownerless_property_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 네트워크에서 패킷 형태로 전송 중인 정보나 컴퓨터의 레지스터·캐시·주기억장치 등에 저장되어 처리 중인 정보 또는 중간결과값은 제366조의 범행객체가 아니다.

연결 NormCard: `art366.transmitting_or_processing_information_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec3_2.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 문서의 종래 사용상태가 처음부터 소유자 의사에 반하거나 무관한 특별한 사정이 있고, 그 상태를 제거·변경하였을 뿐 새로 문서 사용에 지장을 초래하지 않으면 기타 방법에 의한 문서손괴죄는 성립하지 않는다.

연결 NormCard: `art366_sec3_2.document_removal_without_owner_intent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec3_2.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 정보처리장치에 연결된 기록매체의 전원 차단은 저장된 기록 자체에 손상이 발생하는 예외적 경우가 아니라면 전자기록손괴죄가 별도로 성립하지 않는다.

연결 NormCard: `art366_sec3_2.electronic_record_power_cutoff_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec3_2.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 물건에 변형이나 손상을 가하지 않고 단순히 본래 기능만 훼손한 경우에는 손괴가 되지 않는다.

연결 NormCard: `art366_sec3_2.mere_functional_interference_not_destruction`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec3_2.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소유자가 우연히 놓아두거나 방치한 물건을 다른 곳으로 옮겨 즉시 본래 용법대로 사용할 수 없게 한 것만으로는 객관적 이용가치·효용이 인정되지 않아 기타 방법에 의한 효용침해를 인정할 수 없다.

연결 NormCard: `art366_sec3_2.movement_no_objective_use_value`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec4_1.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 범행객체가 타인 소유임을 알지 못하거나 자기 행위로 재물 등의 효용이 침해될 결과를 예견하지 못한 경우에는 고의가 없어 죄가 성립하지 않는다.

연결 NormCard: `art366_sec4_1.intent_absence`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec5_2.bar.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다.

연결 NormCard: `art366_sec5_2.immediate_self_recovery_assessment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec5_2.bar.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다.

연결 NormCard: `art366_sec5_2.justifiable_act_requirements`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec5_2.bar.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다.

연결 NormCard: `art366_sec5_2.possession_protection_destruction`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec5_2.bar.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다.

연결 NormCard: `art366_sec5_2.socially_acceptable_act`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.art366_sec5_5.bar.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 추정적 승낙은 현실적 승낙이 없더라도 행위 당시의 모든 객관적 사정에 비추어 피해자가 행위 내용을 알았다면 당연히 승낙하였을 것으로 예견되는 경우를 말한다.

연결 NormCard: `art366_sec5_5.presumed_consent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `property_damage.component.l0.mandatory_negative.01`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 본래의 효용가치를 상실하였더라도 다른 용도에 사용할 수 있는 물건은 재물손괴죄의 객체가 될 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 서비스약정이나 이용약관이 전자기록 변경·삭제 권한을 부여하지 않았는데 인터넷서비스제공자가 고객 동의 없이 고객이 생성·저장한 전자기록을 변경·삭제하여 복구 불능으로 만든 경우 전자기록 등 특수매체기록 손괴죄가 성립할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 형법상 문서는 문자 또는 이를 대신할 가독적 부호로 계속적으로 물체상에 기재된 의사 또는 관념의 표시인 원본 또는 사회적 기능과 신용성을 동일시할 수 있는 기계적 복사본으로서, 법률상 또는 사회생활상 주요 사항의 증거가 될 수 있는 것이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 전자기록은 일정한 물질적 매체에 전자적 또는 자기적 방식으로 저장된 기록을 말한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록은 기록으로서 본질에 맞는 어느 정도의 영속성을 갖추어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 매체에 전자적으로 기록된 유용한 정보나 자료를 무단 소거하여 기록 상태를 효용 감소 방향으로 변경한 경우 전자기록손괴죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 현행 형법상 문서손괴죄의 문서에는 권리의무에 관한 문서뿐 아니라 사실증명에 관한 문서도 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 기록 내용과 별개로 매체 자체를 파손하여 이용가치가 감소한 경우에는 전자기록손괴죄가 아니라 재물손괴죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등죄의 객체는 타인 소유물이며, 법인 또는 단체의 대표자가 관리·처분 권한을 갖더라도 법인이나 단체 소유물은 대표자에게 타인의 소유이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴죄의 재물은 물건의 종류·성격·경제적 가치 또는 교환가치 유무와 관계없이 널리 재산권의 목적이 될 수 있는 일체의 물건이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공용건조물에 대하여 파괴에 이르지 않는 효용침해행위를 한 경우에도 공용건조물은 제366조 건조물손괴죄의 객체에 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 타인 소유의 공익건조물을 손상시킨 행위가 파괴의 정도에 이르지 않은 경우에는 제366조의 객체가 될 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 범행객체인 전자기록 등 특수매체기록은 정보 자체나 정보보존 매체 자체가 아니라, 저장 또는 기록 매체에 정보가 기록되어 매체와 정보가 불가분적으로 결합된 상태를 의미한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 이식용 또는 실험용으로 인체에서 분리된 장기와 배아 등 인체구성물은 재물로서 손괴죄의 범행객체가 된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공유는 타인의 소유로 취급되므로, 공유자 한 사람이 다른 공유자가 점유하는 재물을 임의로 손상하면 재물손괴등죄가 성립할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 전자적·자기적 방식 및 그 밖의 기술적 방식으로 특수매체에 저장된 기록을 말하며, 전자기록은 그 예시에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 특수매체기록은 문서 이외의 특수한 방법과 매체에 기록되어 컴퓨터 등 정보처리장치에 사용되는 기록으로 한정하여 해석한다.

연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`

검토 메모: 구성요건 L0에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `property_damage.component.l1.mandatory_negative.02`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 물리적 유형적 훼손이 아니라 객체의 소재를 무형적으로 불명하게 하는 행위로서 손괴와 구별된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 은닉은 반드시 객체를 범인의 점유 또는 지배 아래 둘 것을 요구하지 않으며, 피해자 점유 장소 안에서 문서를 숨겨 발견을 곤란하게 한 경우도 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 은닉죄는 재물이나 문서를 이용할 수 없는 상태에 두면 족하고, 이용 방해 기간의 일시성·영속성이나 장래 반환 의사는 묻지 않는다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 재물 또는 문서의 전부 또는 일부에 직접 유형력을 행사해 물질적·물리적으로 훼손하여 원래 효용을 멸실 또는 감손시키는 행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 손괴는 중요한 부분의 훼손이나 물건 자체의 소멸을 요구하지 않으며, 본래 사용목적에 제공할 수 없는 상태가 되면 족하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 문서 본문 식별에 영향이 없더라도 여백 제거로 문서 이용의 불편 또는 완전한 외관을 갖춘 문서로서의 효용 저하가 생기면 손괴에 해당한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 소유자의 의사에 따라 게시 중인 문서를 소유자 의사에 반하여 떼어내 종래 이용상태를 변경하고 그 상태에 따른 이용을 일시적으로 불가능하게 하면 문서손괴죄가 성립할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 전자기록이 저장된 매체에서 파일의 명칭·속성·위치·기록방식 등에 관한 메타데이터를 임의 변경하여 정보의 식별 또는 접근을 곤란하게 하면 은닉에 해당할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 전자기록 등 특수매체기록에 대한 기타 방법의 효용침해행위에는 새 프로그램 입력으로 기존 정보를 사용할 수 없게 하거나, 기록을 추가·삭제하거나 다른 정보와 연결하여 정보 내용을 변경하는 경우 등이 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 감정상 물건을 본래의 용법에 따라 사용할 수 없게 한 경우도 기타 방법에 의한 효용침해행위에 해당하여 재물손괴죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 물건을 설치·부착된 장소나 물건에서 이동·분리한 경우, 그 장소 또는 물건과 범행객체 사이에 객관적으로 구성적 또는 결합적 관계가 있고 설치·부착으로 얻는 이용가치·효용이 인정되면 기타 방법에 의한 손괴죄가 성립할 근거가 된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해는 손괴·은닉 이외의 방법으로 물건의 이용가치 또는 효용을 해하는 것으로, 본래 용법에 따라 사용할 수 없게 하는 모든 경우를 포함한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 기타 방법에 의한 효용침해에는 물건을 본래 사용목적에 제공할 수 없게 하는 경우뿐 아니라 일시적으로 이용할 수 없게 하는 경우도 포함된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 유형력을 행사하여 소유자의 이익에 반하게 물건의 보존상태를 변경하고 일시적으로 본래 기능을 다할 수 없게 한 경우에도 손괴가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 포장도로 낙서가 도로 효용을 해하는지는 도로 용도·기능, 노면표시 기능 및 통행·안전 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 벽면 낙서는 그로 인하여 건조물의 미관 등 기능적 효용이 현저하게 침해되거나 감소된 경우에 한하여 재물손괴죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 건조물 벽면 낙서·게시물 부착·오물 투척이 건조물 효용을 해하는지는 건조물 용도와 기능, 채광·통풍·조망 영향, 미관 훼손 정도, 이용자 불쾌감·저항감, 원상회복 난이도·비용, 목적·계속성 및 당시 상황을 종합하여 사회통념에 따라 판단한다.

연결 NormCard: `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `property_damage.component.l3.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴등에는 손괴·은닉·기타 방법으로 타인 소유 재물·문서 또는 타인 지배관리 하 전자기록 등의 이용가치 전부 또는 일부를 침해한다는 인식, 즉 고의가 필요하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 재물손괴의 고의는 계획적 손괴 의도나 적극적 희망까지 필요하지 않고, 소유자 의사에 반하여 재물 효용을 상실하게 한다는 인식으로 충분하며 미필적 고의만으로도 충분하다.

연결 NormCard: `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 구성요건 L3에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `property_damage.component.l4.mandatory_negative.04`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 재물 등의 이용가치 또는 효용의 감소나 훼손 상태가 발생하면 기수에 이른다.

연결 NormCard: `art366_sec3_3.completion.efficiency_injury`

검토 메모: 구성요건 L4에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `property_damage.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `property_damage.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art366.corpse_exclusion`, `art366.no_utility_property_exclusion`, `art366.ownerless_property_exclusion`, `art366.public_document_used_by_office`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec4_1.intent_absence`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `property_damage.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.corpse_exclusion`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.no_utility_property_exclusion`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.ownerless_property_exclusion`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_document_used_by_office`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366.transmitting_or_processing_information_exclusion`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.document_removal_without_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.electronic_record_power_cutoff_exception`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.mere_functional_interference_not_destruction`, `art366_sec3_2.movement_no_objective_use_value`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_absence`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`, `art366_sec5_2.immediate_self_recovery_assessment`, `art366_sec5_2.justifiable_act_requirements`, `art366_sec5_2.possession_protection_destruction`, `art366_sec5_2.socially_acceptable_act`, `art366_sec5_5.presumed_consent`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `property_damage.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `property_damage.art366.boundary_shift.001`

이 규칙은 **이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다.

### `property_damage.art366.refers_to_crime.001`

이 규칙은 **이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공문서라도 공무소에서 사용하는 공용서류에 해당하지 않는 한 제366조의 범행객체가 되지만, 공용서류 해당 여부가 객체성 판단의 요건이 된다.

연결 NormCard: `art366.public_document_used_by_office`

검토 메모: 이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다.

### `property_damage.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art366.alternative_use_property`, `art366.cloud_provider_delete_record`, `art366.document_definition`, `art366.electronic_record_definition`, `art366.electronic_record_durability`, `art366.electronic_record_erasure`, `art366.fact_certification_private_document`, `art366.medium_damage_property_damage`, `art366.object_manageable_energy`, `art366.other_person_ownership`, `art366.property_object_definition`, `art366.public_building_affirmative_view`, `art366.public_interest_building_non_destruction`, `art366.record_medium_information_combination`, `art366.separated_human_material`, `art366.shared_property_damage`, `art366.special_medium_record_definition`, `art366.special_medium_record_limited_view`, `art366_sec3_2.concealment_definition`, `art366_sec3_2.concealment_no_possession_required`, `art366_sec3_2.concealment_temporary_and_return_intent`, `art366_sec3_2.destruction_definition`, `art366_sec3_2.destruction_no_irreparable_damage`, `art366_sec3_2.document_margin_removal`, `art366_sec3_2.document_removal_against_owner_intent`, `art366_sec3_2.electronic_file_metadata_concealment`, `art366_sec3_2.electronic_record_other_methods_definition`, `art366_sec3_2.emotional_use_majority_position`, `art366_sec3_2.movement_objective_use_value`, `art366_sec3_2.other_method_efficiency_harm_definition`, `art366_sec3_2.other_method_temporary_unusable`, `art366_sec3_2.preservation_state_change_view`, `art366_sec3_2.road_graffiti_totality`, `art366_sec3_2.wall_graffiti_functional_efficiency_limit`, `art366_sec3_2.wall_graffiti_totality`, `art366_sec3_3.completion.efficiency_injury`, `art366_sec4_1.intent_awareness`, `art366_sec4_1.intent_conditional_sufficiency`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
