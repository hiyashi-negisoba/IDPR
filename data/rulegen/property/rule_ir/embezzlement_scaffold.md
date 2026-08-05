# 사기죄 전체 RuleIR 자연어 설명 초안

> 이 파일은 구조를 빠짐없이 펼친 기계적 초안이다. 에이전트가 법률적 연결과 성립·불성립·unknown 경로를 다시 서술한 뒤 사용자에게 제시해야 한다.

## 전체 구조

- rule_set_id: `kr.property.embezzlement.full.v1_candidate`
- predicate: 211개
- rule: 331개
- NormCard: 64개

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

### `embezzlement_case_roles(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다

- 종류/역할: `rule` / `input`
- 연결 NormCard: system contract

### `assess_art355_embezzlement_document_embodied_right(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`

### `satisfied_art355_embezzlement_document_embodied_right(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`

### `not_satisfied_satisfied_art355_embezzlement_document_embodied_right(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`

### `assess_art355_embezzlement_object_excludes_property_interest(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

### `satisfied_art355_embezzlement_object_excludes_property_interest(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

### `not_satisfied_satisfied_art355_embezzlement_object_excludes_property_interest(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

### `assess_art355_embezzlement_object_identification(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement.object-identification`

### `satisfied_art355_embezzlement_object_identification(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-identification`

### `not_satisfied_satisfied_art355_embezzlement_object_identification(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-identification`

### `assess_art355_embezzlement_object_other_property(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355.embezzlement.object-other-property`

### `satisfied_art355_embezzlement_object_other_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-other-property`

### `not_satisfied_satisfied_art355_embezzlement_object_other_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-other-property`

### `assess_art355_embezzlement_other_person(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement.other-person`

### `satisfied_art355_embezzlement_other_person(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.other-person`

### `not_satisfied_satisfied_art355_embezzlement_other_person(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.other-person`

### `assess_art355_embezzlement_custody(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement_custody`

### `satisfied_art355_embezzlement_custody(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_custody`

### `not_satisfied_satisfied_art355_embezzlement_custody(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_custody`

### `assess_art355_embezzlement_illegal_name_trust(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement_illegal_name_trust`

### `satisfied_art355_embezzlement_illegal_name_trust(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_illegal_name_trust`

### `not_satisfied_satisfied_art355_embezzlement_illegal_name_trust(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_illegal_name_trust`

### `assess_art355_embezzlement_protectable_entrustment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355.embezzlement_protectable_entrustment`

### `satisfied_art355_embezzlement_protectable_entrustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_protectable_entrustment`

### `not_satisfied_satisfied_art355_embezzlement_protectable_entrustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_protectable_entrustment`

### `assess_art355_sec1_1_simple_embezzlement(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_1.simple_embezzlement`

### `satisfied_art355_sec1_1_simple_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_1.simple_embezzlement`

### `not_satisfied_satisfied_art355_sec1_1_simple_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_1.simple_embezzlement`

### `assess_art355_sec1_2_embezzlement_illegal_appropriation_exclusion(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

### `satisfied_art355_sec1_2_embezzlement_illegal_appropriation_exclusion(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

### `not_satisfied_satisfied_art355_sec1_2_embezzlement_illegal_appropriation_exclusion(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

### `assess_art355_sec1_2_embezzlement_illegal_appropriation_theory(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

### `satisfied_art355_sec1_2_embezzlement_illegal_appropriation_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

### `not_satisfied_satisfied_art355_sec1_2_embezzlement_illegal_appropriation_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

### `assess_art355_sec2_1_embezzlement_object_property(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355_sec2_1.embezzlement_object_property`

### `satisfied_art355_sec2_1_embezzlement_object_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec2_1.embezzlement_object_property`

### `not_satisfied_satisfied_art355_sec2_1_embezzlement_object_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec2_1.embezzlement_object_property`

### `assess_art355_sec3_3_authority_excess_theory(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.authority_excess_theory`

### `satisfied_art355_sec3_3_authority_excess_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.authority_excess_theory`

### `not_satisfied_satisfied_art355_sec3_3_authority_excess_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.authority_excess_theory`

### `assess_art355_sec3_3_company_funds_advance_loan(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

### `satisfied_art355_sec3_3_company_funds_advance_loan(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

### `not_satisfied_satisfied_art355_sec3_3_company_funds_advance_loan(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

### `assess_art355_sec3_3_company_funds_private_use(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.company_funds_private_use`

### `satisfied_art355_sec3_3_company_funds_private_use(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.company_funds_private_use`

### `not_satisfied_satisfied_art355_sec3_3_company_funds_private_use(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.company_funds_private_use`

### `assess_art355_sec3_3_completion_expression_theory(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.completion_expression_theory`

### `satisfied_art355_sec3_3_completion_expression_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.completion_expression_theory`

### `not_satisfied_satisfied_art355_sec3_3_completion_expression_theory(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.completion_expression_theory`

### `assess_art355_sec3_3_coownership_whole_property(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.coownership_whole_property`

### `satisfied_art355_sec3_3_coownership_whole_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.coownership_whole_property`

### `not_satisfied_satisfied_art355_sec3_3_coownership_whole_property(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.coownership_whole_property`

### `assess_art355_sec3_3_deceptive_means_no_fraud(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

### `satisfied_art355_sec3_3_deceptive_means_no_fraud(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

### `not_satisfied_satisfied_art355_sec3_3_deceptive_means_no_fraud(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

### `assess_art355_sec3_3_embezzlement_act(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.embezzlement_act`

### `satisfied_art355_sec3_3_embezzlement_act(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.embezzlement_act`

### `not_satisfied_satisfied_art355_sec3_3_embezzlement_act(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.embezzlement_act`

### `assess_art355_sec3_3_invalid_disposition_majority(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

### `satisfied_art355_sec3_3_invalid_disposition_majority(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

### `not_satisfied_satisfied_art355_sec3_3_invalid_disposition_majority(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

### `assess_art355_sec3_3_legal_disposition(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.legal_disposition`

### `satisfied_art355_sec3_3_legal_disposition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.legal_disposition`

### `not_satisfied_satisfied_art355_sec3_3_legal_disposition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.legal_disposition`

### `assess_art355_sec3_3_money_fungibles_consumed_amount(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

### `satisfied_art355_sec3_3_money_fungibles_consumed_amount(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

### `not_satisfied_satisfied_art355_sec3_3_money_fungibles_consumed_amount(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

### `assess_art355_sec3_3_no_property_damage_element(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.no_property_damage_element`

### `satisfied_art355_sec3_3_no_property_damage_element(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.no_property_damage_element`

### `not_satisfied_satisfied_art355_sec3_3_no_property_damage_element(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.no_property_damage_element`

### `assess_art355_sec3_3_objective_manifestation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.objective_manifestation`

### `satisfied_art355_sec3_3_objective_manifestation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.objective_manifestation`

### `not_satisfied_satisfied_art355_sec3_3_objective_manifestation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.objective_manifestation`

### `assess_art355_sec3_3_omission_embezzlement(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.omission_embezzlement`

### `satisfied_art355_sec3_3_omission_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.omission_embezzlement`

### `not_satisfied_satisfied_art355_sec3_3_omission_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.omission_embezzlement`

### `assess_art355_sec3_3_partnership_joint_property_whole_amount(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

### `satisfied_art355_sec3_3_partnership_joint_property_whole_amount(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

### `not_satisfied_satisfied_art355_sec3_3_partnership_joint_property_whole_amount(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

### `assess_art355_sec3_3_purpose_limited_money_setoff(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

### `satisfied_art355_sec3_3_purpose_limited_money_setoff(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

### `not_satisfied_satisfied_art355_sec3_3_purpose_limited_money_setoff(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

### `assess_art355_sec3_3_refusal_equivalent_to_embezzlement(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

### `satisfied_art355_sec3_3_refusal_equivalent_to_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

### `not_satisfied_satisfied_art355_sec3_3_refusal_equivalent_to_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

### `assess_art355_sec3_3_refusal_to_return(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.refusal_to_return`

### `satisfied_art355_sec3_3_refusal_to_return(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.refusal_to_return`

### `not_satisfied_satisfied_art355_sec3_3_refusal_to_return(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.refusal_to_return`

### `assess_art355_sec3_3_simple_destruction_exception(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec3_3.simple_destruction_exception`

### `satisfied_art355_sec3_3_simple_destruction_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.simple_destruction_exception`

### `not_satisfied_satisfied_art355_sec3_3_simple_destruction_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.simple_destruction_exception`

### `assess_art355_sec4_1_discretionary_funds_no_presumption(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

### `satisfied_art355_sec4_1_discretionary_funds_no_presumption(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

### `not_satisfied_satisfied_art355_sec4_1_discretionary_funds_no_presumption(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

### `assess_art355_sec4_1_embezzlement_intent_objective_elements(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

### `satisfied_art355_sec4_1_embezzlement_intent_objective_elements(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

### `not_satisfied_satisfied_art355_sec4_1_embezzlement_intent_objective_elements(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

### `assess_art355_sec4_1_eventual_intent_elements(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.eventual_intent_elements`

### `satisfied_art355_sec4_1_eventual_intent_elements(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.eventual_intent_elements`

### `not_satisfied_satisfied_art355_sec4_1_eventual_intent_elements(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.eventual_intent_elements`

### `assess_art355_sec4_1_eventual_intent_inference(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.eventual_intent_inference`

### `satisfied_art355_sec4_1_eventual_intent_inference(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.eventual_intent_inference`

### `not_satisfied_satisfied_art355_sec4_1_eventual_intent_inference(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.eventual_intent_inference`

### `assess_art355_sec4_1_explained_fund_use_no_inference(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

### `satisfied_art355_sec4_1_explained_fund_use_no_inference(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

### `not_satisfied_satisfied_art355_sec4_1_explained_fund_use_no_inference(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

### `assess_art355_sec4_1_illegal_appropriation_intent_definition(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

### `satisfied_art355_sec4_1_illegal_appropriation_intent_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

### `not_satisfied_satisfied_art355_sec4_1_illegal_appropriation_intent_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

### `assess_art355_sec4_1_illegal_appropriation_intent_ownerlike_disposition(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

### `satisfied_art355_sec4_1_illegal_appropriation_intent_ownerlike_disposition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

### `not_satisfied_satisfied_art355_sec4_1_illegal_appropriation_intent_ownerlike_disposition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

### `assess_art355_sec4_1_justified_refusal_exception(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.justified_refusal_exception`

### `satisfied_art355_sec4_1_justified_refusal_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.justified_refusal_exception`

### `not_satisfied_satisfied_art355_sec4_1_justified_refusal_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.justified_refusal_exception`

### `assess_art355_sec4_1_repayment_intent_no_exclusion(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

### `satisfied_art355_sec4_1_repayment_intent_no_exclusion(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

### `not_satisfied_satisfied_art355_sec4_1_repayment_intent_no_exclusion(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

### `assess_art355_sec4_1_representative_corporate_debt_payment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

### `satisfied_art355_sec4_1_representative_corporate_debt_payment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

### `not_satisfied_satisfied_art355_sec4_1_representative_corporate_debt_payment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

### `assess_art355_sec4_1_temporary_company_fund_objective_assessment_view(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

### `satisfied_art355_sec4_1_temporary_company_fund_objective_assessment_view(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

### `not_satisfied_satisfied_art355_sec4_1_temporary_company_fund_objective_assessment_view(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

### `assess_art355_sec4_2_embezzlement_illicit_appropriation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

### `satisfied_art355_sec4_2_embezzlement_illicit_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

### `not_satisfied_satisfied_art355_sec4_2_embezzlement_illicit_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

### `assess_art355_sec4_2_mere_destruction_not_appropriation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

### `satisfied_art355_sec4_2_mere_destruction_not_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

### `not_satisfied_satisfied_art355_sec4_2_mere_destruction_not_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

### `assess_art355_sec4_2_owner_benefit_disposition_no_appropriation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

### `satisfied_art355_sec4_2_owner_benefit_disposition_no_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

### `not_satisfied_satisfied_art355_sec4_2_owner_benefit_disposition_no_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

### `assess_art355_sec4_2_restricted_funds_off_purpose_embezzlement(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

### `satisfied_art355_sec4_2_restricted_funds_off_purpose_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

### `not_satisfied_satisfied_art355_sec4_2_restricted_funds_off_purpose_embezzlement(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

### `assess_art355_sec4_2_temporary_use_against_entrustment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

### `satisfied_art355_sec4_2_temporary_use_against_entrustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

### `not_satisfied_satisfied_art355_sec4_2_temporary_use_against_entrustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

### `assess_art355_sec4_2_third_party_appropriation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355_sec4_2.third_party_appropriation`

### `satisfied_art355_sec4_2_third_party_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.third_party_appropriation`

### `not_satisfied_satisfied_art355_sec4_2_third_party_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_2.third_party_appropriation`

### `assess_art355_sec4_3_accounting_only_adjustment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

### `satisfied_art355_sec4_3_accounting_only_adjustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

### `not_satisfied_satisfied_art355_sec4_3_accounting_only_adjustment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

### `assess_art355_sec4_3_budget_diversion_restricted(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

### `satisfied_art355_sec4_3_budget_diversion_restricted(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

### `not_satisfied_satisfied_art355_sec4_3_budget_diversion_restricted(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

### `assess_art355_sec4_3_business_expense_personal_or_excessive(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

### `satisfied_art355_sec4_3_business_expense_personal_or_excessive(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

### `not_satisfied_satisfied_art355_sec4_3_business_expense_personal_or_excessive(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

### `assess_art355_sec4_3_fake_capital_no_real_increase(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

### `satisfied_art355_sec4_3_fake_capital_no_real_increase(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

### `not_satisfied_satisfied_art355_sec4_3_fake_capital_no_real_increase(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

### `assess_art355_sec4_3_fake_capital_real_increase_assessment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

### `satisfied_art355_sec4_3_fake_capital_real_increase_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

### `not_satisfied_satisfied_art355_sec4_3_fake_capital_real_increase_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

### `assess_art355_sec4_3_objectively_not_grossly_improper_expenditure(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

### `satisfied_art355_sec4_3_objectively_not_grossly_improper_expenditure(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

### `not_satisfied_satisfied_art355_sec4_3_objectively_not_grossly_improper_expenditure(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

### `assess_art355_sec4_3_organization_representative_litigation_exception(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

### `satisfied_art355_sec4_3_organization_representative_litigation_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

### `not_satisfied_satisfied_art355_sec4_3_organization_representative_litigation_exception(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

### `assess_art355_sec4_3_restricted_budget_assessment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

### `satisfied_art355_sec4_3_restricted_budget_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

### `not_satisfied_satisfied_art355_sec4_3_restricted_budget_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

### `assess_art355_sec4_3_slush_fund_concealment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.slush_fund_concealment`

### `satisfied_art355_sec4_3_slush_fund_concealment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_concealment`

### `not_satisfied_satisfied_art355_sec4_3_slush_fund_concealment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_concealment`

### `assess_art355_sec4_3_slush_fund_definition(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art355_sec4_3.slush_fund_definition`

### `satisfied_art355_sec4_3_slush_fund_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_definition`

### `not_satisfied_satisfied_art355_sec4_3_slush_fund_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_definition`

### `assess_art355_sec4_3_slush_fund_formation_personal_appropriation(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

### `satisfied_art355_sec4_3_slush_fund_formation_personal_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

### `not_satisfied_satisfied_art355_sec4_3_slush_fund_formation_personal_appropriation(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

### `assess_art355_sec4_3_slush_fund_purpose_assessment(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

### `satisfied_art355_sec4_3_slush_fund_purpose_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

### `not_satisfied_satisfied_art355_sec4_3_slush_fund_purpose_assessment(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

### `assess_art355_sec5_retention_lien_no_illicit_intent(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

### `satisfied_art355_sec5_retention_lien_no_illicit_intent(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

### `not_satisfied_satisfied_art355_sec5_retention_lien_no_illicit_intent(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

### `assess_art356_business_possession_definition(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art356.business_possession_definition`

### `satisfied_art356_business_possession_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.business_possession_definition`

### `not_satisfied_satisfied_art356_business_possession_definition(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.business_possession_definition`

### `assess_art356_business_possession_origins(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.

- 종류/역할: `rule` / `input`
- 연결 NormCard: `art356.business_possession_origins`

### `satisfied_art356_business_possession_origins(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.business_possession_origins`

### `not_satisfied_satisfied_art356_business_possession_origins(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.business_possession_origins`

### `assess_art356_possession_business_nexus(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356.possession_business_nexus`

### `satisfied_art356_possession_business_nexus(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.possession_business_nexus`

### `not_satisfied_satisfied_art356_possession_business_nexus(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.possession_business_nexus`

### `assess_art356_sec2_2_unrelated_possession(case_id: String, assessment_id: String, defendant_id: String, entrustor_id: String, owner_id: String, status: String)`

이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `standard` / `input`
- 연결 NormCard: `art356_sec2_2.unrelated_possession`

### `satisfied_art356_sec2_2_unrelated_possession(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 충족됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.unrelated_possession`

### `not_satisfied_satisfied_art356_sec2_2_unrelated_possession(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

증명 가능한 평가에서 다음 조건이 부인됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356_sec2_2.unrelated_possession`

### `embezzlement_object_ownership_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

객체 요건 중 타인 소유가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355_sec2_1.embezzlement_object_property`

### `embezzlement_custody_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

객체 요건 중 행위자의 보관자 지위(위탁관계)가 인정됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`

### `embezzlement_conduct_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

실행행위 요건이 충족됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_1.simple_embezzlement`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_3.restricted_budget_assessment`

### `embezzlement_intent_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

주관적 요건이 충족됨 — 고의

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

### `embezzlement_completion_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.completion_expression_theory`

### `embezzlement_elements_satisfied(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

### `embezzlement_not_established(case_id: String, defendant_id: String, issue_id: String)`

명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement_illegal_name_trust`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.slush_fund_concealment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356_sec2_2.unrelated_possession`

### `embezzlement_undetermined(case_id: String, defendant_id: String, issue_id: String)`

관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_illegal_name_trust`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.deceptive_means_no_fraud`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.no_property_damage_element`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_concealment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356.business_possession_definition`, `art356.business_possession_origins`, `art356.possession_business_nexus`, `art356_sec2_2.unrelated_possession`

### `embezzlement_conflict(case_id: String, defendant_id: String, issue_id: String)`

같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_illegal_name_trust`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.deceptive_means_no_fraud`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.no_property_damage_element`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_concealment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356.business_possession_definition`, `art356.business_possession_origins`, `art356.possession_business_nexus`, `art356_sec2_2.unrelated_possession`

### `embezzlement_has_negative(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement_illegal_name_trust`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.slush_fund_concealment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356_sec2_2.unrelated_possession`

### `embezzlement_has_conflict(case_id: String, defendant_id: String)`

해당 피고인에 관해 하나 이상의 상충 평가가 존재함

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_illegal_name_trust`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.deceptive_means_no_fraud`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.no_property_damage_element`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_concealment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356.business_possession_definition`, `art356.business_possession_origins`, `art356.possession_business_nexus`, `art356_sec2_2.unrelated_possession`

### `embezzlement_established(case_id: String, defendant_id: String, entrustor_id: String, owner_id: String)`

완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

### `embezzlement_requirement_waived(case_id: String, defendant_id: String, issue_id: String, value: String)`

이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`, `art355_sec3_3.no_property_damage_element`

### `embezzlement_aggravation(case_id: String, defendant_id: String, kind: String)`

가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art356.business_possession_definition`, `art356.business_possession_origins`, `art356.possession_business_nexus`, `art356_sec2_2.unrelated_possession`

### `property_crime_established(case_id: String, crime_id: String, defendant_id: String, owner_id: String, possessor_id: String)`

재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지

- 종류/역할: `rule` / `derived`
- 연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

## Rules

### `embezzlement.art355.card.001.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.document-embodied-right`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.001.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.document-embodied-right`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.001.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.document-embodied-right`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.001.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.document-embodied-right`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.002.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.002.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.002.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.002.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.003.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-identification`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.003.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-identification`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.003.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-identification`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.003.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-identification`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.004.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-other-property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.004.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-other-property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.004.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-other-property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.004.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.object-other-property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.005.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.other-person`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.005.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.other-person`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.005.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.other-person`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.005.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement.other-person`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.006.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_custody`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.006.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_custody`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.006.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_custody`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.006.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_custody`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.007.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_illegal_name_trust`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.007.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_illegal_name_trust`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.007.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_illegal_name_trust`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.007.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_illegal_name_trust`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.card.008.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_protectable_entrustment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355.card.008.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_protectable_entrustment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355.card.008.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_protectable_entrustment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355.card.008.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355.embezzlement_protectable_entrustment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec1_1.card.009.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.simple_embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec1_1.card.009.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.simple_embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec1_1.card.009.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.simple_embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec1_1.card.009.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_1.simple_embezzlement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec1_2.card.010.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec1_2.card.010.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec1_2.card.010.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec1_2.card.010.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec1_2.card.011.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec1_2.card.011.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec1_2.card.011.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec1_2.card.011.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec2_1.card.012.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec2_1.embezzlement_object_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec2_1.card.012.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec2_1.embezzlement_object_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec2_1.card.012.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec2_1.embezzlement_object_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec2_1.card.012.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec2_1.embezzlement_object_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.013.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.authority_excess_theory`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.013.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.authority_excess_theory`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.013.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.authority_excess_theory`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.013.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.authority_excess_theory`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.014.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.014.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.014.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.014.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.015.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_private_use`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.015.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_private_use`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.015.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_private_use`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.015.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.company_funds_private_use`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.016.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.016.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.016.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.016.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.017.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.coownership_whole_property`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.017.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.coownership_whole_property`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.017.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.coownership_whole_property`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.017.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.coownership_whole_property`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.018.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.018.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.018.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.018.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.019.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.embezzlement_act`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.019.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.embezzlement_act`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.019.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.embezzlement_act`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.019.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.embezzlement_act`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.020.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.020.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.020.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.020.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.021.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.legal_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.021.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.legal_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.021.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.legal_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.021.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.legal_disposition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.022.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.022.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.022.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.022.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.023.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.no_property_damage_element`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.023.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.no_property_damage_element`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.023.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.no_property_damage_element`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.023.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.no_property_damage_element`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.024.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.objective_manifestation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.024.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.objective_manifestation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.024.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.objective_manifestation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.024.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.objective_manifestation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.025.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.omission_embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.025.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.omission_embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.025.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.omission_embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.025.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.omission_embezzlement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.026.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.026.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.026.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.026.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.027.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.027.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.027.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.027.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.028.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.028.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.028.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.028.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.029.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_to_return`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.029.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_to_return`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.029.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_to_return`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.029.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.refusal_to_return`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.030.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.simple_destruction_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec3_3.card.030.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.simple_destruction_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec3_3.card.030.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.simple_destruction_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec3_3.card.030.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec3_3.simple_destruction_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.031.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.031.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.031.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.031.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.032.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.032.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.032.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.032.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.033.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_elements`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.033.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_elements`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.033.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_elements`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.033.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_elements`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.034.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_inference`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.034.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_inference`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.034.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_inference`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.034.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.eventual_intent_inference`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.035.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.035.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.035.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.035.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.036.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.036.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.036.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.036.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.037.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.037.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.037.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.037.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.038.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.justified_refusal_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.038.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.justified_refusal_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.038.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.justified_refusal_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.038.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.justified_refusal_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.039.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.039.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.039.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.039.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.040.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.040.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.040.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.040.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.041.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_1.card.041.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_1.card.041.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_1.card.041.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.042.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.042.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.042.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.042.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.043.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.043.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.043.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.043.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.044.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.044.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.044.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.044.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.045.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.045.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.045.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.045.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.046.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.046.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.046.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.046.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.047.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_2.card.047.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_2.card.047.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_2.card.047.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_2.third_party_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.048.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.048.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.048.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.048.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.049.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.049.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.049.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.049.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.050.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.050.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.050.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.050.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.051.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.051.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.051.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.051.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.052.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.052.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.052.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.052.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.053.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.053.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.053.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.053.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.054.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.054.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.054.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.054.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.055.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.055.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.055.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.055.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.056.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_concealment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.056.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_concealment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.056.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_concealment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.056.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_concealment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.057.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.057.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.057.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.057.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.058.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.058.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.058.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.058.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.059.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec4_3.card.059.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec4_3.card.059.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec4_3.card.059.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355_sec5.card.060.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art355_sec5.card.060.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art355_sec5.card.060.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art355_sec5.card.060.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art356.card.061.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_definition`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art356.card.061.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_definition`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art356.card.061.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_definition`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art356.card.061.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_definition`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art356.card.062.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_origins`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art356.card.062.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_origins`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art356.card.062.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_origins`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art356.card.062.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.business_possession_origins`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art356.card.063.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.possession_business_nexus`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art356.card.063.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.possession_business_nexus`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art356.card.063.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.possession_business_nexus`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art356.card.063.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356.possession_business_nexus`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art356_sec2_2.card.064.satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 충족됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.

### `embezzlement.art356_sec2_2.card.064.undetermined`

이 규칙은 **관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.

### `embezzlement.art356_sec2_2.card.064.conflict`

이 규칙은 **같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음
- 이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.

### `embezzlement.art356_sec2_2.card.064.not_satisfied`

이 규칙은 **증명 가능한 평가에서 다음 조건이 부인됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.**을 도출한다.

필요한 전제:

- 이 카드의 사건별 적용 평가: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.
- 해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다.

### `embezzlement.art355.component.embezzlement_object_ownership_satisfied.01`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.

연결 NormCard: `art355.embezzlement.document-embodied-right`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.component.embezzlement_object_ownership_satisfied.02`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.

연결 NormCard: `art355.embezzlement.object-identification`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.component.embezzlement_object_ownership_satisfied.03`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.

연결 NormCard: `art355.embezzlement.object-other-property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.component.embezzlement_object_ownership_satisfied.04`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.

연결 NormCard: `art355.embezzlement.other-person`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec2_1.component.embezzlement_object_ownership_satisfied.05`

이 규칙은 **객체 요건 중 타인 소유가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.

연결 NormCard: `art355_sec2_1.embezzlement_object_property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.component.embezzlement_custody_satisfied.01`

이 규칙은 **객체 요건 중 행위자의 보관자 지위(위탁관계)가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.

연결 NormCard: `art355.embezzlement_custody`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.component.embezzlement_custody_satisfied.02`

이 규칙은 **객체 요건 중 행위자의 보관자 지위(위탁관계)가 인정됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.

연결 NormCard: `art355.embezzlement_protectable_entrustment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec1_1.component.embezzlement_conduct_satisfied.01`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.

연결 NormCard: `art355_sec1_1.simple_embezzlement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.02`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.

연결 NormCard: `art355_sec3_3.authority_excess_theory`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.03`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.

연결 NormCard: `art355_sec3_3.company_funds_advance_loan`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.04`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.

연결 NormCard: `art355_sec3_3.company_funds_private_use`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.05`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.

연결 NormCard: `art355_sec3_3.coownership_whole_property`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.06`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.

연결 NormCard: `art355_sec3_3.embezzlement_act`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.07`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.

연결 NormCard: `art355_sec3_3.invalid_disposition_majority`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.08`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.

연결 NormCard: `art355_sec3_3.legal_disposition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.09`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.

연결 NormCard: `art355_sec3_3.money_fungibles_consumed_amount`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.10`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.

연결 NormCard: `art355_sec3_3.objective_manifestation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.11`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.

연결 NormCard: `art355_sec3_3.omission_embezzlement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.12`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.

연결 NormCard: `art355_sec3_3.partnership_joint_property_whole_amount`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.13`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.

연결 NormCard: `art355_sec3_3.purpose_limited_money_setoff`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.14`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.

연결 NormCard: `art355_sec3_3.refusal_equivalent_to_embezzlement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_conduct_satisfied.15`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.

연결 NormCard: `art355_sec3_3.refusal_to_return`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_conduct_satisfied.16`

이 규칙은 **실행행위 요건이 충족됨**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.

연결 NormCard: `art355_sec4_3.restricted_budget_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec1_2.component.embezzlement_intent_satisfied.01`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.02`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.

연결 NormCard: `art355_sec4_1.embezzlement_intent_objective_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.03`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.

연결 NormCard: `art355_sec4_1.eventual_intent_elements`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.04`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.

연결 NormCard: `art355_sec4_1.eventual_intent_inference`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.05`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.06`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.

연결 NormCard: `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.07`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.

연결 NormCard: `art355_sec4_1.repayment_intent_no_exclusion`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_1.component.embezzlement_intent_satisfied.08`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.

연결 NormCard: `art355_sec4_1.temporary_company_fund_objective_assessment_view`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_2.component.embezzlement_intent_satisfied.09`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.

연결 NormCard: `art355_sec4_2.embezzlement_illicit_appropriation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_2.component.embezzlement_intent_satisfied.10`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.

연결 NormCard: `art355_sec4_2.restricted_funds_off_purpose_embezzlement`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_2.component.embezzlement_intent_satisfied.11`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.

연결 NormCard: `art355_sec4_2.temporary_use_against_entrustment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_2.component.embezzlement_intent_satisfied.12`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.

연결 NormCard: `art355_sec4_2.third_party_appropriation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.13`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.

연결 NormCard: `art355_sec4_3.budget_diversion_restricted`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.14`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.

연결 NormCard: `art355_sec4_3.business_expense_personal_or_excessive`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.15`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.

연결 NormCard: `art355_sec4_3.fake_capital_real_increase_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.16`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.

연결 NormCard: `art355_sec4_3.slush_fund_definition`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.17`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.

연결 NormCard: `art355_sec4_3.slush_fund_formation_personal_appropriation`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec4_3.component.embezzlement_intent_satisfied.18`

이 규칙은 **주관적 요건이 충족됨 — 고의**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.

연결 NormCard: `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355_sec3_3.component.embezzlement_completion_satisfied.01`

이 규칙은 **단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.

### `embezzlement.art355.bar.001`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 재물이 아닌 권리·재산상 이익 및 기업비밀·기업정보 자체는 횡령죄의 객체가 될 수 없다.

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355.bar.002`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 부동산실명법 위반의 중간생략등기형 또는 2자간 등기명의신탁에서 무효인 명의신탁약정에 기초한 관계는 형법상 보호할 가치 있는 위탁관계가 아니므로, 명의수탁자의 임의 처분에 대하여 명의신탁자 관계의 횡령죄는 성립하지 않는다.

연결 NormCard: `art355.embezzlement_illegal_name_trust`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec1_2.bar.003`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다.

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec3_3.bar.004`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 보관물을 손괴한 행위는 그 자체로는 불법영득의사의 표현이 아니므로 횡령죄를 구성하지 않는다.

연결 NormCard: `art355_sec3_3.simple_destruction_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_1.bar.005`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다.

연결 NormCard: `art355_sec4_1.discretionary_funds_no_presumption`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_1.bar.006`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다.

연결 NormCard: `art355_sec4_1.explained_fund_use_no_inference`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_1.bar.007`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다.

연결 NormCard: `art355_sec4_1.justified_refusal_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_1.bar.008`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다.

연결 NormCard: `art355_sec4_1.representative_corporate_debt_payment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_2.bar.009`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 단순한 손괴의 의사만으로는 횡령죄의 불법영득의사를 구성하지 않는다.

연결 NormCard: `art355_sec4_2.mere_destruction_not_appropriation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_2.bar.010`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 보관자가 자기 또는 제3자의 이익이 아니라 소유자의 이익을 위하여 처분한 경우에는 특별한 사정이 없는 한 불법영득의사가 인정되지 않는다.

연결 NormCard: `art355_sec4_2.owner_benefit_disposition_no_appropriation`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_3.bar.011`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다.

연결 NormCard: `art355_sec4_3.accounting_only_adjustment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_3.bar.012`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다.

연결 NormCard: `art355_sec4_3.fake_capital_no_real_increase`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_3.bar.013`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다.

연결 NormCard: `art355_sec4_3.objectively_not_grossly_improper_expenditure`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_3.bar.014`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다.

연결 NormCard: `art355_sec4_3.organization_representative_litigation_exception`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec4_3.bar.015`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다.

연결 NormCard: `art355_sec4_3.slush_fund_concealment`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art355_sec5.bar.016`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다.

연결 NormCard: `art355_sec5.retention_lien_no_illicit_intent`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.art356_sec2_2.bar.017`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.

### `embezzlement.component.l0o.mandatory_negative.01`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 권리가 화체된 문서 또는 유가증권은 재물일 수 있으나, 주식 그 자체 또는 전자외상매출채권처럼 재물이 아닌 권리는 횡령죄의 객체가 될 수 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 여러 재물이 횡령 객체가 될 수 있는 경우에는 소유관계와 성상, 위탁관계, 보관·처분 방법 및 행위자의 영득 의사 등 제반 사정을 종합하여 객체를 확정한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 객체는 행위자가 보관하는 타인의 재물이며, 횡령 대상 재물은 타인의 소유이어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 타인은 행위자 이외의 자연인, 법인, 법인격 없는 단체 또는 조합 등을 포함하며, 타인 소유 여부는 원칙적으로 민사실체법 및 외국적 요소가 있는 경우 국제사법상 준거법에 따라 결정한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 재물을 객체로 하고, 자기 점유 아래의 타인 재물을 대상으로 하는 재물죄이다.

연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355_sec2_1.embezzlement_object_property`

검토 메모: 구성요건 L0o에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `embezzlement.component.l0c.mandatory_negative.02`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관은 위탁관계에 의하여 맡겨진 타인의 재물에 대한 점유 또는 소지를 뜻하며, 사실상 지배뿐 아니라 법률상 지배·처분이 가능한 상태를 포함한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 보관에는 보관자와 소유자 사이의 법률상 또는 사실상의 위탁관계가 필요하고, 그 관계는 형법상 보호할 가치 있는 신임에 의한 것인지 관계·경위 및 형사법적 보호 필요성을 고려하여 규범적으로 판단한다.

연결 NormCard: `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`

검토 메모: 구성요건 L0c에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `embezzlement.component.l1.mandatory_negative.03`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 단순 또는 위탁물 횡령죄는 위탁관계에 의하여 타인의 재물을 보관하는 사람이 그 재물을 횡령하거나 반환을 거부하는 범죄이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 위탁 신뢰관계를 배신하여 권한을 초월한 처분으로 재물을 영득하는 행위가 횡령행위이며, 경제적으로 처벌할 필요가 있는 중요한 배신적 처분에 한하여 배신적 영득이 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 대표이사 등이 회사 자금을 가지급금 등의 명목으로 인출·사용하면서 이자나 변제기 약정 및 적법한 이사회 결의가 없으면, 통상 용인 범위를 벗어난 사적 대여·처분으로서 횡령죄를 구성한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공유자가 공유물을 보관하다 횡령한 경우, 분할 전에는 지분비율과 무관하게 공유물 전부에 대하여 횡령죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 횡령 또는 반환거부 행위는 불법영득의 의사를 실현하는 일체의 행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 보관자가 소유자의 동의 없이 보관물을 담보로 제공하는 등 처분행위에 무효 또는 취소사유가 있더라도, 불법영득의사가 표현된 이상 횡령죄 성립에 영향이 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 금전 등 대체물의 횡령죄는 실제 소비 등 처분한 수액에 관하여 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 단순한 내심의 불법영득 의사만으로는 성립하지 않고, 그 의사가 외부에서 인식될 수 있는 객관적 행위가 있어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 부작위로도 영득의사가 표현될 수 있으므로 부작위에 의한 횡령이 가능하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 동업자 사이 손익분배 정산 전 동업재산을 보관하던 동업자가 임의 횡령한 경우, 지분비율과 무관하게 횡령금액 전부에 대한 죄책을 부담한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 용도·목적 특정 위탁금은 특별한 상계정산 약정 없이 수탁자의 위탁자에 대한 채권에 상계충당할 수 없고, 반대채권이 있다는 사정만으로 반환거부의 정당한 사유가 되지 않는다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 반환거부가 횡령죄를 구성하려면 단순한 반환거부만으로는 부족하고, 반환거부 이유와 주관적 의사를 종합하여 횡령행위와 같다고 볼 정도여야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 반환의 거부란 보관물에 관하여 소유권자의 권리를 배제하는 의사표시를 하는 행위이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다.

연결 NormCard: `art355_sec1_1.simple_embezzlement`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_3.restricted_budget_assessment`

검토 메모: 구성요건 L1에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `embezzlement.component.l3.mandatory_negative.04`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득의사는 보관자가 소유자를 대신하여 보관 중인 타인의 재물을 이용·처분하려는 의사이며, 경제적 용법에 따른 이용·처분이나 경제적 이득 취득 의사를 필요로 하지 않는다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 용도가 엄격히 제한된 자금을 위탁받아 제한된 용도 외 목적으로 사용하면, 결과적으로 위탁자를 위한 면이 있더라도 사용행위 자체로 불법영득의사가 실현되어 횡령죄가 성립한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 보관물을 일시 사용한 경우라도 사용행위의 객관적 태양·시간·사회경제적 의미에 비추어 소유자의 위탁취지에 반하면, 행위자가 단순 일시사용 목적이었다고 하더라도 횡령죄 성립을 긍정할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄의 불법영득은 보관자 자신이 영득하는 경우뿐 아니라 제3자를 위하여 영득하는 경우도 포함한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다.
- 증명 가능한 평가에서 다음 조건이 부인됨: 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다.

연결 NormCard: `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 구성요건 L3에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `embezzlement.component.l4.mandatory_negative.05`

이 규칙은 **명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 부인됨: 횡령죄는 불법영득의사가 객관적으로 외부에 표현된 때 기수에 이른다.

연결 NormCard: `art355_sec3_3.completion_expression_theory`

검토 메모: 구성요건 L4에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다.

### `embezzlement.core.outcome.elements_satisfied`

이 규칙은 **구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)**을 도출한다.

필요한 전제:

- 객체 요건 중 타인 소유가 인정됨
- 객체 요건 중 행위자의 보관자 지위(위탁관계)가 인정됨
- 실행행위 요건이 충족됨
- 주관적 요건이 충족됨 — 고의
- 단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름

연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다.

### `embezzlement.core.outcome.has_negative`

이 규칙은 **해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함**을 도출한다.

필요한 전제:

- 명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함

연결 NormCard: `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement_illegal_name_trust`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.slush_fund_concealment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356_sec2_2.unrelated_possession`

검토 메모: 명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `embezzlement.core.outcome.has_conflict`

이 규칙은 **해당 피고인에 관해 하나 이상의 상충 평가가 존재함**을 도출한다.

필요한 전제:

- 같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨

연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-excludes-property-interest`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_illegal_name_trust`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_exclusion`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.deceptive_means_no_fraud`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.no_property_damage_element`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec3_3.simple_destruction_exception`, `art355_sec4_1.discretionary_funds_no_presumption`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.explained_fund_use_no_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.justified_refusal_exception`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.representative_corporate_debt_payment`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.mere_destruction_not_appropriation`, `art355_sec4_2.owner_benefit_disposition_no_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.accounting_only_adjustment`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_no_real_increase`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.objectively_not_grossly_improper_expenditure`, `art355_sec4_3.organization_representative_litigation_exception`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_concealment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`, `art355_sec5.retention_lien_no_illicit_intent`, `art356.business_possession_definition`, `art356.business_possession_origins`, `art356.possession_business_nexus`, `art356_sec2_2.unrelated_possession`

검토 메모: 카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.

### `embezzlement.core.outcome.established`

이 규칙은 **완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립**을 도출한다.

필요한 전제:

- 구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)
- 라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 최종 결론 층에서만 부정을 쓴다
- 해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함
- 해당 피고인에 관해 하나 이상의 상충 평가가 존재함

연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다.

### `embezzlement.art355_sec3_3.requirement_waived.001`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령을 실현하기 위해 기망수단을 사용하더라도 재물 이전과 피해자의 재산적 처분행위가 없으므로 횡령죄만 성립하고 사기죄는 별도로 성립하지 않는다.

연결 NormCard: `art355_sec3_3.deceptive_means_no_fraud`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `embezzlement.art355_sec3_3.requirement_waived.002`

이 규칙은 **이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다**을 도출한다.

필요한 전제:

- 증명 가능한 평가에서 다음 조건이 충족됨: 횡령죄의 성립에 재산상 손해의 발생은 구성요건적 요건으로 필요하지 않다.

연결 NormCard: `art355_sec3_3.no_property_damage_element`

검토 메모: 요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다.

### `embezzlement.aggravation.occupational.001`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다.

연결 NormCard: `art356.business_possession_definition`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `embezzlement.aggravation.occupational.002`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다.

연결 NormCard: `art356.business_possession_origins`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `embezzlement.aggravation.occupational.003`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다.

연결 NormCard: `art356.possession_business_nexus`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `embezzlement.aggravation.occupational.004`

이 규칙은 **가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립
- 증명 가능한 평가에서 다음 조건이 충족됨: 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다.

연결 NormCard: `art356_sec2_2.unrelated_possession`

검토 메모: 기본범이 성립한 위에 occupational 가중요건이 충족되면 플래그를 켠다.

### `embezzlement.core.outcome.bridge`

이 규칙은 **재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지**을 도출한다.

필요한 전제:

- 완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립

연결 NormCard: `art355.embezzlement.document-embodied-right`, `art355.embezzlement.object-identification`, `art355.embezzlement.object-other-property`, `art355.embezzlement.other-person`, `art355.embezzlement_custody`, `art355.embezzlement_protectable_entrustment`, `art355_sec1_1.simple_embezzlement`, `art355_sec1_2.embezzlement_illegal_appropriation_theory`, `art355_sec2_1.embezzlement_object_property`, `art355_sec3_3.authority_excess_theory`, `art355_sec3_3.company_funds_advance_loan`, `art355_sec3_3.company_funds_private_use`, `art355_sec3_3.completion_expression_theory`, `art355_sec3_3.coownership_whole_property`, `art355_sec3_3.embezzlement_act`, `art355_sec3_3.invalid_disposition_majority`, `art355_sec3_3.legal_disposition`, `art355_sec3_3.money_fungibles_consumed_amount`, `art355_sec3_3.objective_manifestation`, `art355_sec3_3.omission_embezzlement`, `art355_sec3_3.partnership_joint_property_whole_amount`, `art355_sec3_3.purpose_limited_money_setoff`, `art355_sec3_3.refusal_equivalent_to_embezzlement`, `art355_sec3_3.refusal_to_return`, `art355_sec4_1.embezzlement_intent_objective_elements`, `art355_sec4_1.eventual_intent_elements`, `art355_sec4_1.eventual_intent_inference`, `art355_sec4_1.illegal_appropriation_intent_definition`, `art355_sec4_1.illegal_appropriation_intent_ownerlike_disposition`, `art355_sec4_1.repayment_intent_no_exclusion`, `art355_sec4_1.temporary_company_fund_objective_assessment_view`, `art355_sec4_2.embezzlement_illicit_appropriation`, `art355_sec4_2.restricted_funds_off_purpose_embezzlement`, `art355_sec4_2.temporary_use_against_entrustment`, `art355_sec4_2.third_party_appropriation`, `art355_sec4_3.budget_diversion_restricted`, `art355_sec4_3.business_expense_personal_or_excessive`, `art355_sec4_3.fake_capital_real_increase_assessment`, `art355_sec4_3.restricted_budget_assessment`, `art355_sec4_3.slush_fund_definition`, `art355_sec4_3.slush_fund_formation_personal_appropriation`, `art355_sec4_3.slush_fund_purpose_assessment`

검토 메모: 성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다.

## 에이전트 추가 설명 필요

- 구성요건별 satisfied/not_satisfied/unknown 전파 경로
- negative·exception 카드가 불성립 경로에 들어가는 방식
- 삼각사기에서 피기망자·처분자·재산소유자·수익자 역할 구별
- 역할 슬롯은 분리하되 동일 인물이 여러 역할을 맡을 때 같은 ID를 쓰는 방식
- 차용금 사기 기준과 일반 사기 기준의 관계
- 동시에 상반된 assessment가 있을 때 conflict가 도출되는 방식
- RAG로 제외된 구체 유형을 언제 검색해야 하는지
