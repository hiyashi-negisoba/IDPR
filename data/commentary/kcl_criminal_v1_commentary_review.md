# KCL 형사법 issue tag commentary bundle

이 파일은 의미검색이나 reranker 점수를 쓰지 않고, `issue_tags`를 조문 metadata에
직접 매핑한 뒤 해당 `(law_id, article_no)` chunk를 전량 수집한 검수본입니다.

## Summary

- Tags: 165
- Unique commentary chunks: 3108
- Mapped: 137
- Mapped with corpus gap: 21
- Unavailable in current commentary: 7
- Target missing in docs: 0
- Raw PDF fallback chunks: 5
- Previously non-mapped tags manually audited: 33/33
- Pool specification: `kcl_criminal_v1_commentary_pool.json`
- Exception audit: `kcl_criminal_v1_non_mapped_audit.md`

## Tag targets

| tag | status | chunks | targets / reason | sub_questions |
|---|---|---:|---|---|
| `accidental_defense` | mapped_with_corpus_gap | 33 | 형법각칙 제257조 상해, 존속상해 (33)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r10_p2_q1` |
| `accomplice_of_preparation` | mapped | 8 | 형법각칙 제255조 예비, 음모 (8) | `kcl_criminal_r12_p2_q1_na` |
| `aggravated_result` | mapped | 27 | 형법각칙 제337조 강도상해, 치상 (19)<br>형법각칙 제338조 강도살인·치사 (8) | `kcl_criminal_r14_p2_q2` |
| `amendment_of_indictment` | mapped | 59 | 형사소송법 제298조 공소장의 변경 (59) | `kcl_criminal_r13_p2_q5` |
| `appeal_interest` | mapped | 36 | 형사소송법 제327조 공소기각의 판결 (23)<br>형사소송법 제328조 공소기각의 결정 (10)<br>형사소송법 제363조 공소기각의 결정 (3) | `kcl_criminal_r10_p2_q5` |
| `appeal_reason_statement` | mapped | 34 | 형사소송법 제32조 변호인선임의 효력 (13)<br>형사소송법 제36조 변호인의 독립소송행위권 (3)<br>형사소송법 제361조의3 항소이유서와 답변서 (18) | `kcl_criminal_r10_p2_q6` |
| `appeal_reason_statement_period` | mapped | 117 | 형사소송법 제361조의3 항소이유서와 답변서 (18)<br>형사소송법 제361조의4 항소기각의 결정 (17)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r10_p1_q3_da` |
| `appellate_disposition` | mapped | 112 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r13_p2_q3` |
| `appellate_fact_finding` | mapped | 131 | 형사소송법 제307조 증거재판주의 (49)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r14_p2_q7` |
| `appellate_scope` | mapped | 112 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r12_p1_q6` |
| `appellate_sentencing` | mapped | 37 | 형사소송법 제368조 불이익변경의 금지 (37) | `kcl_criminal_r11_p2_q3` |
| `appellate_trial_scope` | mapped | 117 | 형사소송법 제361조의3 항소이유서와 답변서 (18)<br>형사소송법 제361조의4 항소기각의 결정 (17)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r10_p1_q3_da` |
| `arrest_method` | mapped | 107 | 형사소송법 제200조의2 영장에 의한 체포 (37)<br>형사소송법 제200조의3 긴급체포 (23)<br>형사소송법 제211조 현행범인과 준현행범인 (11)<br>형사소송법 제212조 현행범인의 체포 (36) | `kcl_criminal_r13_p1_q2` |
| `arrest_scene_search` | mapped | 124 | 형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제216조 영장에 의하지 아니한 강제처분 (39)<br>형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r12_p2_q2` |
| `arson` | mapped | 24 | 형법각칙 제164조 현주건조물 등 방화 (24) | `kcl_criminal_r14_p1_q1` |
| `attempt` | mapped_with_corpus_gap | 16 | 형법각칙 제299조 준강간, 준강제추행 (14)<br>형법각칙 제300조 미수범 (2)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r11_p2_q1_da` |
| `attempted_murder` | mapped | 144 | 형법각칙 제250조 살인, 존속살해 (143)<br>형법각칙 제254조 미수범 (1) | `kcl_criminal_r14_p1_q1` |
| `bail_revocation` | mapped | 37 | 형사소송법 제102조 보석조건의 변경과 취소 등 (19)<br>형사소송법 제402조 항고 (18) | `kcl_criminal_r13_p2_q4` |
| `breach_of_trust` | mapped | 362 | 형법각칙 제355조 횡령, 배임 (352)<br>형법각칙 제356조 업무상의 횡령과 배임 (10) | `kcl_criminal_r10_p2_q2` |
| `breach_of_trust_bribe` | mapped | 34 | 형법각칙 제357조 배임수증재 (34) | `kcl_criminal_r12_p1_q3` |
| `bribe_delivery` | mapped | 8 | 형법각칙 제133조 뇌물공여 등 (8) | `kcl_criminal_r10_p1_q3_ga`, `kcl_criminal_r14_p1_q2` |
| `bribe_giving` | mapped | 8 | 형법각칙 제133조 뇌물공여 등 (8) | `kcl_criminal_r11_p2_q1_ga` |
| `bribery` | mapped | 31 | 형법각칙 제129조 수뢰, 사전수뢰 (31) | `kcl_criminal_r10_p1_q3_ga`, `kcl_criminal_r11_p2_q1_ga`, `kcl_criminal_r14_p1_q2` |
| `causation` | mapped_with_corpus_gap | 140 | 형법각칙 제268조 업무상과실·중과실 치사상 (113)<br>형법각칙 제337조 강도상해, 치상 (19)<br>형법각칙 제338조 강도살인·치사 (8)<br>gap: 인과관계 일반론은 형법총칙 영역입니다. | `kcl_criminal_r10_p2_q3`, `kcl_criminal_r14_p2_q2` |
| `causation_uncertainty` | mapped | 12 | 형법각칙 제263조 동시범 (12) | `kcl_criminal_r10_p1_q2` |
| `co_defendant_statement` | mapped | 59 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r10_p1_q3_na`, `kcl_criminal_r14_p2_q3` |
| `co_offender_suspension` | mapped | 51 | 형사소송법 제249조 공소시효의 기간 (27)<br>형사소송법 제253조 시효의 정지와 효력 (24) | `kcl_criminal_r11_p2_q2` |
| `commencement_of_execution` | mapped_with_corpus_gap | 8 | 형법각칙 제334조 특수강도 (7)<br>형법각칙 제342조 미수범 (1)<br>gap: 실행의 착수 일반론은 형법총칙 영역입니다. | `kcl_criminal_r10_p2_q2` |
| `complaint_before_investigation` | mapped | 57 | 형사소송법 제223조 고소권자 (27)<br>형사소송법 제230조 고소기간 (7)<br>형사소송법 제200조의3 긴급체포 (23) | `kcl_criminal_r14_p1_q4_1` |
| `complaint_cure_after_indictment` | mapped | 145 | 형사소송법 제223조 고소권자 (27)<br>형사소송법 제230조 고소기간 (7)<br>형사소송법 제254조 공소제기의 방식과 공소장 (88)<br>형사소송법 제327조 공소기각의 판결 (23) | `kcl_criminal_r14_p1_q4_2` |
| `complaint_withdrawal` | mapped | 22 | 형사소송법 제232조 고소의 취소 (22) | `kcl_criminal_r11_p1_q2_na` |
| `concurrent_crimes` | mapped | 112 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r13_p2_q3`, `kcl_criminal_r14_p1_q5_1` |
| `conflicting_co_offender_judgment` | mapped | 62 | 형사소송법 제420조 재심이유 (58)<br>형사소송법 제435조 재심개시의 결정 (4) | `kcl_criminal_r11_p1_q4` |
| `copy_identity` | mapped | 203 | 형사소송법 제106조 압수 (150)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제129조 압수목록의 교부 (4)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_ga` |
| `counterpart_offense` | mapped | 51 | 형사소송법 제249조 공소시효의 기간 (27)<br>형사소송법 제253조 시효의 정지와 효력 (24) | `kcl_criminal_r11_p2_q2` |
| `credit_card_crime` | mapped | 170 | 형법각칙 제329조 절도 (43)<br>형법각칙 제347조 사기 (127) | `kcl_criminal_r13_p2_q1` |
| `cyber_defamation_false_fact` | unavailable_in_current_commentary | 0 | 특별법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r12_p1_q1` |
| `damage` | mapped | 48 | 형법각칙 제366조 재물손괴등 (48) | `kcl_criminal_r14_p1_q3` |
| `defendant_statement_hearsay_exception` | mapped | 78 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제313조 진술서 등 (19)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r10_p1_q1_ra` |
| `defense_counsel_appointment` | mapped | 34 | 형사소송법 제32조 변호인선임의 효력 (13)<br>형사소송법 제36조 변호인의 독립소송행위권 (3)<br>형사소송법 제361조의3 항소이유서와 답변서 (18) | `kcl_criminal_r10_p2_q6` |
| `dereliction_of_duty` | mapped | 25 | 형법각칙 제122조 직무유기 (25) | `kcl_criminal_r10_p1_q3_ga`, `kcl_criminal_r11_p2_q1_na` |
| `digital_evidence_admissibility` | mapped | 203 | 형사소송법 제106조 압수 (150)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제129조 압수목록의 교부 (4)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_ga` |
| `direct_examination_principle` | mapped | 131 | 형사소송법 제307조 증거재판주의 (49)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r14_p2_q7` |
| `discovery_noncompliance` | mapped | 34 | 형사소송법 제266조의3 증거서류 등의 열람·등사 (20)<br>형사소송법 제266조의4 법원의 열람·등사 결정 (5)<br>형사소송법 제266조의5 증거개시 관련 조치 (9) | `kcl_criminal_r11_p2_q5` |
| `dismissal_judgment` | mapped | 36 | 형사소송법 제327조 공소기각의 판결 (23)<br>형사소송법 제328조 공소기각의 결정 (10)<br>형사소송법 제363조 공소기각의 결정 (3) | `kcl_criminal_r10_p2_q5` |
| `document_offense` | mapped | 26 | 형법각칙 제231조 사문서등의 위조변조 (20)<br>형법각칙 제234조 위조사문서등의 행사 (6) | `kcl_criminal_r12_p1_q1` |
| `electronic_evidence` | mapped | 266 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r13_p2_q2`, `kcl_criminal_r14_p2_q5` |
| `electronic_evidence_admissibility` | mapped | 263 | 형사소송법 제106조 압수 (150)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r13_p1_q4_1` |
| `embezzlement` | mapped | 362 | 형법각칙 제355조 횡령, 배임 (352)<br>형법각칙 제356조 업무상의 횡령과 배임 (10) | `kcl_criminal_r10_p2_q1`, `kcl_criminal_r14_p1_q2` |
| `emergency_arrest` | mapped | 23 | 형사소송법 제200조의3 긴급체포 (23) | `kcl_criminal_r14_p1_q4_1` |
| `emergency_arrest_search_seizure` | mapped | 71 | 형사소송법 제200조의3 긴급체포 (23)<br>형사소송법 제216조 영장에 의하지 아니한 강제처분 (39)<br>형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r10_p1_q1_da`, `kcl_criminal_r12_p2_q2`, `kcl_criminal_r13_p1_q4_1` |
| `evidence_admissibility` | mapped | 89 | 형사소송법 제307조 증거재판주의 (49)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r10_p1_q1_na` |
| `evidence_discovery` | mapped | 34 | 형사소송법 제266조의3 증거서류 등의 열람·등사 (20)<br>형사소송법 제266조의4 법원의 열람·등사 결정 (5)<br>형사소송법 제266조의5 증거개시 관련 조치 (9) | `kcl_criminal_r11_p2_q5` |
| `execution_stay` | mapped | 37 | 형사소송법 제102조 보석조건의 변경과 취소 등 (19)<br>형사소송법 제402조 항고 (18) | `kcl_criminal_r13_p2_q4` |
| `expert_report_admissibility` | mapped | 50 | 형사소송법 제313조 진술서 등 (19)<br>형사소송법 제314조 증거능력에 대한 예외 (22)<br>형사소송법 제315조 당연히 증거능력이 있는 서류 (9) | `kcl_criminal_r12_p2_q3` |
| `extortion` | mapped | 47 | 형법각칙 제350조 공갈 (47) | `kcl_criminal_r11_p1_q1` |
| `false_public_document` | mapped | 42 | 형법각칙 제225조 공문서등의 위조변조 (17)<br>형법각칙 제227조 허위공문서작성등 (25) | `kcl_criminal_r11_p2_q1_na` |
| `forced_indecent_act_indirect_principal` | mapped_with_corpus_gap | 20 | 형법각칙 제298조 강제추행 (20)<br>gap: 간접정범은 형법총칙 영역입니다. | `kcl_criminal_r10_p1_q1_ga` |
| `forensic_participation_right` | mapped | 203 | 형사소송법 제106조 압수 (150)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제129조 압수목록의 교부 (4)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_ga` |
| `formal_judgment` | mapped | 36 | 형사소송법 제327조 공소기각의 판결 (23)<br>형사소송법 제328조 공소기각의 결정 (10)<br>형사소송법 제363조 공소기각의 결정 (3) | `kcl_criminal_r10_p2_q5` |
| `fraud` | mapped | 127 | 형법각칙 제347조 사기 (127) | `kcl_criminal_r10_p2_q1`, `kcl_criminal_r12_p2_q1_da`, `kcl_criminal_r14_p1_q2` |
| `habitual_offense` | unavailable_in_current_commentary | 0 | 특별법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r13_p2_q5` |
| `harboring_offender` | mapped | 38 | 형법각칙 제151조 범인은닉과 친족간의 특례 (38) | `kcl_criminal_r10_p2_q2`, `kcl_criminal_r12_p1_q4`, `kcl_criminal_r13_p2_q1` |
| `hearsay_exception` | mapped | 158 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제313조 진술서 등 (19)<br>형사소송법 제314조 증거능력에 대한 예외 (22)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r12_p1_q5_na`, `kcl_criminal_r13_p1_q4_1`, `kcl_criminal_r14_p2_q6` |
| `hearsay_statement` | mapped | 59 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r10_p1_q3_na`, `kcl_criminal_r14_p2_q3` |
| `hearsay_vs_original_evidence` | mapped | 59 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r12_p1_q5_ga` |
| `identity_of_facts` | mapped | 59 | 형사소송법 제298조 공소장의 변경 (59) | `kcl_criminal_r13_p2_q5` |
| `illegal_evidence` | mapped | 122 | 형사소송법 제308조의2 위법수집증거의 배제 (40)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r12_p2_q4` |
| `imaginative_concurrence` | mapped | 112 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r12_p1_q6` |
| `impeachment_evidence` | mapped | 32 | 형사소송법 제318조의2 증명력을 다투기 위한 증거 (32) | `kcl_criminal_r13_p1_q4_2` |
| `improper_use_of_seal` | mapped | 7 | 형법각칙 제239조 사인등의 위조, 부정사용 (7) | `kcl_criminal_r12_p2_q1_da` |
| `independent_concurrent_acts` | mapped | 12 | 형법각칙 제263조 동시범 (12) | `kcl_criminal_r10_p1_q2` |
| `indirect_principal` | mapped_with_corpus_gap | 25 | 형법각칙 제227조 허위공문서작성등 (25)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r11_p2_q1_na` |
| `information_property` | mapped | 405 | 형법각칙 제329조 절도 (43)<br>형법각칙 제355조 횡령, 배임 (352)<br>형법각칙 제356조 업무상의 횡령과 배임 (10) | `kcl_criminal_r12_p1_q3` |
| `injury_resulting_death` | mapped | 7 | 형법각칙 제259조 상해치사 (7) | `kcl_criminal_r10_p1_q2` |
| `inspection_report_photo` | mapped | 68 | 형사소송법 제49조 검증 등의 조서 (3)<br>형사소송법 제139조 검증 (7)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58) | `kcl_criminal_r12_p2_q3` |
| `instigator_liability` | mapped_with_corpus_gap | 143 | 형법각칙 제250조 살인, 존속살해 (143)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r12_p2_q1_ga` |
| `interference_with_exercise_of_right` | mapped | 27 | 형법각칙 제323조 권리행사방해 (27) | `kcl_criminal_r14_p1_q3` |
| `investigator_testimony` | mapped | 67 | 형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r13_p1_q4_2` |
| `joint_principal` | mapped_with_corpus_gap | 250 | 형법각칙 제129조 수뢰, 사전수뢰 (31)<br>형법각칙 제164조 현주건조물 등 방화 (24)<br>형법각칙 제250조 살인, 존속살해 (143)<br>형법각칙 제254조 미수범 (1)<br>형법각칙 제331조 특수절도 (12)<br>형법각칙 제335조 준강도 (20)<br>형법각칙 제337조 강도상해, 치상 (19)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r11_p2_q1_ga`, `kcl_criminal_r13_p1_q3`, `kcl_criminal_r14_p1_q1`, `kcl_criminal_r14_p2_q1` |
| `joint_principal_mistake` | mapped_with_corpus_gap | 13 | 형법각칙 제331조 특수절도 (12)<br>형법각칙 제342조 미수범 (1)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r13_p1_q1` |
| `joint_residential_intrusion` | mapped | 65 | 형법각칙 제319조 주거침입, 퇴거불응 (65) | `kcl_criminal_r13_p1_q1` |
| `joint_theft_impossible_attempt` | mapped_with_corpus_gap | 13 | 형법각칙 제331조 특수절도 (12)<br>형법각칙 제342조 미수범 (1)<br>gap: 불능미수와 공동정범은 형법총칙 영역입니다. | `kcl_criminal_r13_p1_q1` |
| `justification_consent` | mapped_with_corpus_gap | 43 | 형법각칙 제329조 절도 (43)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r12_p1_q2` |
| `legality_of_official_act` | mapped | 64 | 형법각칙 제136조 공무집행방해 (64) | `kcl_criminal_r14_p2_q4` |
| `mistake_of_circumstance` | mapped_with_corpus_gap | 16 | 형법각칙 제299조 준강간, 준강제추행 (14)<br>형법각칙 제300조 미수범 (2)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r11_p2_q1_da` |
| `mistake_of_consent` | mapped_with_corpus_gap | 43 | 형법각칙 제329조 절도 (43)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r12_p1_q2` |
| `mistake_of_legality` | mapped_with_corpus_gap | 64 | 형법각칙 제136조 공무집행방해 (64)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r14_p2_q4` |
| `mistake_of_object` | mapped_with_corpus_gap | 176 | 형법각칙 제250조 살인, 존속살해 (143)<br>형법각칙 제257조 상해, 존속상해 (33)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r10_p2_q1`, `kcl_criminal_r12_p2_q1_ga` |
| `multiple_hearsay` | mapped | 130 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제314조 증거능력에 대한 예외 (22) | `kcl_criminal_r12_p1_q5_na` |
| `murder` | mapped | 143 | 형법각칙 제250조 살인, 존속살해 (143) | `kcl_criminal_r12_p2_q1_ga` |
| `murder_attempt` | mapped | 144 | 형법각칙 제250조 살인, 존속살해 (143)<br>형법각칙 제254조 미수범 (1) | `kcl_criminal_r13_p1_q3` |
| `murder_preparation` | mapped | 8 | 형법각칙 제255조 예비, 음모 (8) | `kcl_criminal_r12_p2_q1_na` |
| `negligence` | mapped | 119 | 형법각칙 제267조 과실치사 (6)<br>형법각칙 제268조 업무상과실·중과실 치사상 (113) | `kcl_criminal_r10_p2_q3` |
| `new_evidence` | mapped | 62 | 형사소송법 제420조 재심이유 (58)<br>형사소송법 제435조 재심개시의 결정 (4) | `kcl_criminal_r11_p1_q4` |
| `non_retroactivity` | unavailable_in_current_commentary | 0 | 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r13_p2_q5` |
| `objective_attribution` | mapped_with_corpus_gap | 140 | 형법각칙 제268조 업무상과실·중과실 치사상 (113)<br>형법각칙 제337조 강도상해, 치상 (19)<br>형법각칙 제338조 강도살인·치사 (8)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r10_p2_q3`, `kcl_criminal_r14_p2_q2` |
| `obstruction_by_fraud` | mapped | 34 | 형법각칙 제137조 위계에 의한 공무집행방해 (34) | `kcl_criminal_r11_p2_q1_na`, `kcl_criminal_r12_p1_q4`, `kcl_criminal_r13_p2_q1` |
| `obstruction_of_official_duties` | mapped | 64 | 형법각칙 제136조 공무집행방해 (64) | `kcl_criminal_r14_p2_q4` |
| `occupational_breach_of_trust` | mapped | 10 | 형법각칙 제356조 업무상의 횡령과 배임 (10) | `kcl_criminal_r12_p1_q3` |
| `offense_subject_to_complaint` | mapped | 132 | 형법각칙 제323조 권리행사방해 (27)<br>형법각칙 제328조 친족간의 범행과 고소 (26)<br>형사소송법 제223조 고소권자 (27)<br>형사소송법 제230조 고소기간 (7)<br>형사소송법 제232조 고소의 취소 (22)<br>형사소송법 제327조 공소기각의 판결 (23) | `kcl_criminal_r14_p1_q4_1`, `kcl_criminal_r14_p1_q4_2` |
| `official_bribe_receipt` | mapped | 31 | 형법각칙 제129조 수뢰, 사전수뢰 (31) | `kcl_criminal_r10_p1_q3_ga` |
| `official_secret_disclosure` | mapped | 21 | 형법각칙 제127조 공무상 비밀의 누설 (21) | `kcl_criminal_r12_p1_q4` |
| `ordinary_appeal` | mapped | 37 | 형사소송법 제102조 보석조건의 변경과 취소 등 (19)<br>형사소송법 제402조 항고 (18) | `kcl_criminal_r13_p2_q4` |
| `partial_appeal` | mapped | 112 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r12_p1_q6`, `kcl_criminal_r13_p2_q3`, `kcl_criminal_r14_p1_q5_1` |
| `participation_right` | mapped | 275 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_na` |
| `perjury` | mapped | 43 | 형법각칙 제152조 위증, 모해위증 (43) | `kcl_criminal_r12_p1_q4` |
| `police_interrogation_record` | mapped | 67 | 형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제316조 전문의 진술 (9) | `kcl_criminal_r13_p1_q4_2` |
| `police_statement_record` | mapped | 130 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제314조 증거능력에 대한 예외 (22) | `kcl_criminal_r12_p1_q5_na` |
| `police_stop_questioning` | unavailable_in_current_commentary | 0 | 경찰관직무집행법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r13_p1_q2` |
| `post_seizure_warrant` | mapped | 9 | 형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r10_p1_q1_da` |
| `post_warrant_cure` | mapped | 122 | 형사소송법 제308조의2 위법수집증거의 배제 (40)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r12_p2_q4` |
| `private_document_forgery` | mapped | 20 | 형법각칙 제231조 사문서등의 위조변조 (20) | `kcl_criminal_r12_p2_q1_da` |
| `procedural_cure` | mapped | 34 | 형사소송법 제32조 변호인선임의 효력 (13)<br>형사소송법 제36조 변호인의 독립소송행위권 (3)<br>형사소송법 제361조의3 항소이유서와 답변서 (18) | `kcl_criminal_r10_p2_q6` |
| `prohibition_disadvantageous_change` | mapped | 37 | 형사소송법 제368조 불이익변경의 금지 (37) | `kcl_criminal_r11_p2_q3`, `kcl_criminal_r14_p1_q5_2` |
| `property_possession` | mapped | 27 | 형법각칙 제323조 권리행사방해 (27) | `kcl_criminal_r14_p1_q3` |
| `prosecutor_appeal` | mapped | 34 | 형사소송법 제266조의3 증거서류 등의 열람·등사 (20)<br>형사소송법 제266조의4 법원의 열람·등사 결정 (5)<br>형사소송법 제266조의5 증거개시 관련 조치 (9) | `kcl_criminal_r11_p2_q5` |
| `purpose_to_defame` | unavailable_in_current_commentary | 0 | 특별법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r12_p1_q1` |
| `quasi_rape_impossible_attempt` | mapped_with_corpus_gap | 16 | 형법각칙 제299조 준강간, 준강제추행 (14)<br>형법각칙 제300조 미수범 (2)<br>gap: 불능미수 일반론은 형법총칙 영역입니다. | `kcl_criminal_r11_p2_q1_da` |
| `quasi_robbery_injury` | mapped | 39 | 형법각칙 제335조 준강도 (20)<br>형법각칙 제337조 강도상해, 치상 (19) | `kcl_criminal_r11_p1_q1`, `kcl_criminal_r13_p1_q1`, `kcl_criminal_r14_p2_q1` |
| `recording_admissibility` | mapped | 69 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제313조 진술서 등 (19) | `kcl_criminal_r10_p1_q1_ra` |
| `reenactment_photo` | mapped | 68 | 형사소송법 제49조 검증 등의 조서 (3)<br>형사소송법 제139조 검증 (7)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58) | `kcl_criminal_r12_p2_q3` |
| `relative_property_crime_exception` | mapped | 27 | 형법각칙 제328조 친족간의 범행과 고소 (26)<br>형법각칙 제344조 친족간의 범행 (1) | `kcl_criminal_r11_p1_q2_na`, `kcl_criminal_r13_p1_q1` |
| `remand_scope` | mapped | 35 | 형사소송법 제342조 일부상소 (30)<br>형사소송법 제397조 파기환송 (5) | `kcl_criminal_r14_p1_q5_1` |
| `remand_sentencing` | mapped | 42 | 형사소송법 제368조 불이익변경의 금지 (37)<br>형사소송법 제397조 파기환송 (5) | `kcl_criminal_r14_p1_q5_2` |
| `remote_cloud_search_seizure` | mapped | 226 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73) | `kcl_criminal_r14_p2_q5` |
| `residential_intrusion` | mapped | 65 | 형법각칙 제319조 주거침입, 퇴거불응 (65) | `kcl_criminal_r10_p1_q1_ga`, `kcl_criminal_r14_p1_q1` |
| `residential_intrusion_rape_injury` | mapped | 117 | 형법각칙 제297조 강간 (28)<br>형법각칙 제301조 강간 등 상해·치상 (24)<br>형법각칙 제319조 주거침입, 퇴거불응 (65) | `kcl_criminal_r10_p1_q1_ga` |
| `retrial` | mapped | 62 | 형사소송법 제420조 재심이유 (58)<br>형사소송법 제435조 재심개시의 결정 (4) | `kcl_criminal_r11_p1_q4` |
| `robbery_preparation` | mapped | 10 | 형법각칙 제343조 예비, 음모 (10) | `kcl_criminal_r10_p2_q2` |
| `search_warrant` | mapped | 124 | 형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제216조 영장에 의하지 아니한 강제처분 (39)<br>형사소송법 제217조 영장에 의하지 아니하는 강제처분 (9) | `kcl_criminal_r12_p2_q2` |
| `secret_recording` | mapped_with_corpus_gap | 69 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제313조 진술서 등 (19)<br>gap: 통신비밀보호법 쟁점은 현재 corpus 밖입니다. | `kcl_criminal_r13_p1_q3`, `kcl_criminal_r13_p1_q4_1` |
| `secret_recording_by_conversation_party` | mapped | 69 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제313조 진술서 등 (19) | `kcl_criminal_r10_p1_q1_ra` |
| `seizure_record_photo_admissibility` | mapped | 92 | 형사소송법 제49조 검증 등의 조서 (3)<br>형사소송법 제307조 증거재판주의 (49)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r10_p1_q1_da` |
| `separate_warrant` | mapped | 275 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_na` |
| `sexual_image_threat` | unavailable_in_current_commentary | 0 | 특별법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r11_p1_q1` |
| `special_injury` | mapped | 3 | 형법각칙 제258조의2 특수상해 (3) | `kcl_criminal_r13_p2_q1` |
| `special_robbery` | mapped | 7 | 형법각칙 제334조 특수강도 (7) | `kcl_criminal_r14_p2_q2` |
| `special_robbery_attempt` | mapped | 8 | 형법각칙 제334조 특수강도 (7)<br>형법각칙 제342조 미수범 (1) | `kcl_criminal_r10_p2_q2` |
| `special_theft` | mapped | 12 | 형법각칙 제331조 특수절도 (12) | `kcl_criminal_r11_p1_q2_na`, `kcl_criminal_r13_p2_q1` |
| `special_theft_joint_principal` | mapped_with_corpus_gap | 12 | 형법각칙 제331조 특수절도 (12)<br>gap: 공동정범 일반론은 형법총칙 영역입니다. | `kcl_criminal_r11_p1_q1`, `kcl_criminal_r14_p2_q1` |
| `status_offense_accomplice` | mapped_with_corpus_gap | 21 | 형법각칙 제127조 공무상 비밀의 누설 (21)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r12_p1_q4` |
| `statute_of_limitations` | mapped | 51 | 형사소송법 제249조 공소시효의 기간 (27)<br>형사소송법 제253조 시효의 정지와 효력 (24) | `kcl_criminal_r11_p2_q2` |
| `stolen_property` | mapped | 59 | 형법각칙 제362조 장물의 취득, 알선 등 (59) | `kcl_criminal_r10_p2_q1`, `kcl_criminal_r11_p1_q1` |
| `tablet_imaging` | mapped | 232 | 형사소송법 제106조 압수 (150)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제215조 압수, 수색, 검증 (73) | `kcl_criminal_r14_p2_q5` |
| `theft` | mapped | 43 | 형법각칙 제329조 절도 (43) | `kcl_criminal_r12_p1_q2` |
| `theft_from_deceased` | mapped | 52 | 형법각칙 제329조 절도 (43)<br>형법각칙 제360조 점유이탈물횡령 (9) | `kcl_criminal_r12_p2_q1_da` |
| `theft_vs_fraud` | mapped | 170 | 형법각칙 제329조 절도 (43)<br>형법각칙 제347조 사기 (127) | `kcl_criminal_r13_p2_q1` |
| `third_party_receipt` | mapped | 15 | 형법각칙 제130조 제삼자뇌물제공 (15) | `kcl_criminal_r11_p2_q1_ga` |
| `third_party_voluntary_submission` | mapped | 14 | 형사소송법 제108조 임의 제출물 등의 압수 (5)<br>형사소송법 제218조 영장에 의하지 아니한 압수 (9) | `kcl_criminal_r12_p2_q4` |
| `traffic_accident_death` | mapped | 119 | 형법각칙 제267조 과실치사 (6)<br>형법각칙 제268조 업무상과실·중과실 치사상 (113) | `kcl_criminal_r10_p2_q3` |
| `trial_centered_principle` | mapped | 131 | 형사소송법 제307조 증거재판주의 (49)<br>형사소송법 제364조 항소법원의 심판 (82) | `kcl_criminal_r14_p2_q7` |
| `unrelated_electronic_evidence` | mapped | 275 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제121조 영장집행과 당사자의 참여 (3)<br>형사소송법 제122조 영장집행과 참여권자에의 통지 (6)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r11_p1_q3_na`, `kcl_criminal_r12_p2_q4`, `kcl_criminal_r13_p2_q2` |
| `use_deception` | mapped | 127 | 형법각칙 제347조 사기 (127) | `kcl_criminal_r14_p1_q2` |
| `use_of_force_stop` | unavailable_in_current_commentary | 0 | 경찰관직무집행법 주석서가 현재 commentary corpus에 없습니다. | `kcl_criminal_r13_p1_q2` |
| `victim_consent` | mapped | 43 | 형법각칙 제329조 절도 (43) | `kcl_criminal_r12_p1_q2` |
| `video_recording_authenticity` | mapped | 90 | 형사소송법 제221조 제3자의 출석요구 등 (23)<br>형사소송법 제244조의2 피의자진술의 영상녹화 (9)<br>형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58) | `kcl_criminal_r14_p2_q6` |
| `voluntary_abandonment` | mapped_with_corpus_gap | 174 | 형법각칙 제250조 살인, 존속살해 (143)<br>형법각칙 제254조 미수범 (1)<br>형법각칙 제297조 강간 (28)<br>형법각칙 제300조 미수범 (2)<br>gap: 핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다. | `kcl_criminal_r10_p1_q1_ga`, `kcl_criminal_r13_p1_q3` |
| `voluntary_submission` | mapped | 14 | 형사소송법 제108조 임의 제출물 등의 압수 (5)<br>형사소송법 제218조 영장에 의하지 아니한 압수 (9) | `kcl_criminal_r10_p1_q1_na` |
| `warrant_relevance` | mapped | 266 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r13_p2_q2` |
| `warrant_scope` | mapped | 266 | 형사소송법 제106조 압수 (150)<br>형사소송법 제113조 압수·수색영장 (3)<br>형사소송법 제215조 압수, 수색, 검증 (73)<br>형사소송법 제308조의2 위법수집증거의 배제 (40) | `kcl_criminal_r14_p2_q5` |
| `warrantless_seizure` | mapped | 14 | 형사소송법 제108조 임의 제출물 등의 압수 (5)<br>형사소송법 제218조 영장에 의하지 아니한 압수 (9) | `kcl_criminal_r10_p1_q1_na` |
| `withdrawal_from_preparation` | mapped | 8 | 형법각칙 제255조 예비, 음모 (8) | `kcl_criminal_r12_p2_q1_na` |
| `witness_statement_record` | mapped | 80 | 형사소송법 제312조 검사 또는 사법경찰관의 조서 등 (58)<br>형사소송법 제314조 증거능력에 대한 예외 (22) | `kcl_criminal_r14_p2_q6` |
| `witness_testimony_admissibility` | mapped | 84 | 형사소송법 제310조의2 전문증거와 증거능력 (50)<br>형사소송법 제316조 전문의 진술 (9)<br>형사소송법 제161조의2 증인신문의 방식 (25) | `kcl_criminal_r10_p1_q3_na`, `kcl_criminal_r12_p1_q5_ga`, `kcl_criminal_r14_p2_q3` |
