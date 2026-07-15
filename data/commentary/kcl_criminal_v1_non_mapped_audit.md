# KCL commentary 비-mapped 33개 육안 검토

2026-07-15 기준 기존 `mapped`가 아니었던 33개 issue tag를 원천 PDF,
`docs.parquet`의 `(law_id, article_no)` metadata, 문항의 issue tag 조합으로 전수 검토했습니다.
KCL `rubric_summary`와 의미검색 점수는 mapping 근거로 사용하지 않았습니다.

## 결과

- 검토: 33/33
- 원천 PDF fallback 또는 오매핑 정정으로 완전 확보: 5
- 개별 범죄 조문만 확보, 총칙/특별법 gap 유지: 21
- 현재 corpus에서 확보 불가: 7

| tag | 이전 상태 | 검토 결론 | 현재 상태 | metadata targets | 판단 및 남은 자료 |
|---|---|---|---|---|---|
| `accidental_defense` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제257조 (33) | 상해죄 제257조 주석은 확보할 수 있으나 우연방위 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 위법성론 주석 |
| `attempt` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제299조 (14)<br>형법각칙 제300조 (2) | 준강간 제299조와 미수범 제300조는 확보되지만 불능미수 일반론은 총칙 쟁점입니다.<br>필요: 형법총칙 미수론 주석 |
| `attempted_murder` | mapped_with_corpus_gap | fully_available_after_raw_fallback | mapped | 형법각칙 제250조 (143)<br>형법각칙 제254조 (1) | 살인 제250조와 미수범 제254조 원천 PDF를 모두 확보했습니다. |
| `causation` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제268조 (113)<br>형법각칙 제337조 (19)<br>형법각칙 제338조 (8) | 과실치사상·강도치사상 조문 주석은 있으나 인과관계 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 인과관계 주석 |
| `commencement_of_execution` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제334조 (7)<br>형법각칙 제342조 (1) | 특수강도 및 절도·강도 미수범 주석은 있으나 실행의 착수 일반론은 총칙 쟁점입니다.<br>필요: 형법총칙 미수론 주석 |
| `cyber_defamation_false_fact` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 정보통신망을 통한 허위사실 명예훼손의 근거 특별법이 현재 corpus 밖입니다.<br>필요: 정보통신망법 또는 관련 특별법 주석 |
| `forced_indecent_act_indirect_principal` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제298조 (20) | 강제추행 제298조 주석은 있으나 간접정범 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 정범·공범론 주석 |
| `habitual_offense` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 문항의 상습성은 아동·청소년성보호법상 쟁점으로 해당 특별법이 corpus 밖입니다.<br>필요: 아동·청소년성보호법 주석 |
| `indirect_principal` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제227조 (25) | 허위공문서작성 제227조 주석은 있으나 간접정범 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 정범·공범론 주석 |
| `instigator_liability` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제250조 (143) | 살인 제250조 주석은 있으나 객체의 착오가 교사범에 미치는 효과는 총칙 쟁점입니다.<br>필요: 형법총칙 공범론·착오론 주석 |
| `joint_principal` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제129조 (31)<br>형법각칙 제164조 (24)<br>형법각칙 제250조 (143)<br>형법각칙 제254조 (1)<br>형법각칙 제331조 (12)<br>형법각칙 제335조 (20)<br>형법각칙 제337조 (19) | 각 문항의 뇌물·방화·살인·절도·준강도 조문은 확보되나 공동정범 일반론이 없습니다.<br>필요: 형법총칙 공동정범 주석 |
| `joint_principal_mistake` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제331조 (12)<br>형법각칙 제342조 (1) | 특수절도와 미수범 조문은 확보되나 공동정범의 착오 일반론이 없습니다.<br>필요: 형법총칙 공동정범·착오론 주석 |
| `joint_theft_impossible_attempt` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제331조 (12)<br>형법각칙 제342조 (1) | 특수절도와 미수범 조문은 확보되나 불능미수·공동정범 일반론이 없습니다.<br>필요: 형법총칙 미수론·공동정범 주석 |
| `justification_consent` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제329조 (43) | 절도 제329조 주석은 있으나 피해자 승낙의 위법성조각 구조는 총칙 쟁점입니다.<br>필요: 형법총칙 피해자 승낙 주석 |
| `mistake_of_circumstance` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제299조 (14)<br>형법각칙 제300조 (2) | 준강간 및 미수범 조문은 확보되나 반전된 구성요건적 착오 일반론은 총칙 쟁점입니다.<br>필요: 형법총칙 착오론 주석 |
| `mistake_of_consent` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제329조 (43) | 절도 제329조 주석은 있으나 양해·승낙의 착오 효과는 총칙 자료가 필요합니다.<br>필요: 형법총칙 착오론·피해자 승낙 주석 |
| `mistake_of_legality` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제136조 (64) | 공무집행방해 제136조 주석은 있으나 적법성의 체계적 지위에 따른 착오는 총칙 쟁점입니다.<br>필요: 형법총칙 고의·위법성의 착오 주석 |
| `mistake_of_object` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제250조 (143)<br>형법각칙 제257조 (33) | 살인·상해 조문 주석은 확보되나 객체의 착오 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 구성요건적 착오 주석 |
| `murder_attempt` | mapped_with_corpus_gap | fully_available_after_raw_fallback | mapped | 형법각칙 제250조 (143)<br>형법각칙 제254조 (1) | 살인 제250조와 미수범 제254조 원천 PDF를 모두 확보했습니다. |
| `non_retroactivity` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 행위시법·신법 적용 쟁점은 형법총칙이고 대상 특별법 주석도 현재 corpus 밖입니다.<br>필요: 형법총칙 죄형법정주의 및 아동·청소년성보호법 주석 |
| `objective_attribution` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제268조 (113)<br>형법각칙 제337조 (19)<br>형법각칙 제338조 (8) | 과실치사상·강도치사상 조문은 확보되나 객관적 귀속 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 객관적 귀속 주석 |
| `offense_subject_to_complaint` | mapped_with_corpus_gap | fully_available_after_mapping_correction | mapped | 형법각칙 제323조 (27)<br>형법각칙 제328조 (26)<br>형사소송법 제223조 (27)<br>형사소송법 제230조 (7)<br>형사소송법 제232조 (22)<br>형사소송법 제327조 (23) | 권리행사방해·친족상도례와 고소·공소기각 절차 조문으로 정정했습니다. |
| `police_stop_questioning` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 불심검문 근거인 경찰관직무집행법 주석이 현재 corpus 밖입니다.<br>필요: 경찰관직무집행법 주석 |
| `purpose_to_defame` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 비방 목적은 정보통신망 명예훼손 특별구성요건으로 해당 특별법이 corpus 밖입니다.<br>필요: 정보통신망법 또는 관련 특별법 주석 |
| `quasi_rape_impossible_attempt` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제299조 (14)<br>형법각칙 제300조 (2) | 준강간 제299조와 미수범 제300조는 확보되나 불능미수 일반론은 총칙 쟁점입니다.<br>필요: 형법총칙 불능미수 주석 |
| `relative_property_crime_exception` | mapped_with_corpus_gap | fully_available_after_mapping_correction | mapped | 형법각칙 제328조 (26)<br>형법각칙 제344조 (1) | 절도 사안에 맞춰 제328조와 제344조로 축소했고 제344조는 원천 PDF로 보완했습니다. |
| `secret_recording` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형사소송법 제310조의2 (50)<br>형사소송법 제313조 (19) | 전문증거 관련 형사소송법 주석은 있으나 녹음 적법성의 특별법 근거가 없습니다.<br>필요: 통신비밀보호법 주석 |
| `sexual_image_threat` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 촬영물 이용 협박의 근거 특별법이 현재 corpus 밖입니다.<br>필요: 성폭력처벌법 주석 |
| `special_robbery_attempt` | mapped_with_corpus_gap | fully_available_after_raw_fallback | mapped | 형법각칙 제334조 (7)<br>형법각칙 제342조 (1) | 특수강도 제334조와 미수범 제342조 원천 PDF를 모두 확보했습니다. |
| `special_theft_joint_principal` | mapped_with_corpus_gap | partial_context_only | mapped_with_corpus_gap | 형법각칙 제331조 (12) | 특수절도 제331조 주석은 있으나 공동정범 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 공동정범 주석 |
| `status_offense_accomplice` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제127조 (21) | 공무상비밀누설 제127조 주석은 있으나 신분범 공범 일반론은 총칙 자료가 필요합니다.<br>필요: 형법총칙 신분범·공범 주석 |
| `use_of_force_stop` | unavailable_in_current_commentary | unavailable | unavailable_in_current_commentary | 없음 | 정지·유형력 행사의 근거인 경찰관직무집행법 주석이 현재 corpus 밖입니다.<br>필요: 경찰관직무집행법 주석 |
| `voluntary_abandonment` | unavailable_in_current_commentary | partial_context_only | mapped_with_corpus_gap | 형법각칙 제250조 (143)<br>형법각칙 제254조 (1)<br>형법각칙 제297조 (28)<br>형법각칙 제300조 (2) | 살인·강간 및 해당 미수 처벌 조문은 확보되나 중지미수 일반론은 총칙 쟁점입니다.<br>필요: 형법총칙 중지미수 주석 |
