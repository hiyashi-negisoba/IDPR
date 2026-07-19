# 범죄사실 작성례 기반 사기죄 M5 확장 인벤토리

## 목적과 자료 단위

경찰청 국가수사본부의 `범죄사실 작성방법 및 죄종별 작성례(총론, 경제범죄)` 중 사기 부분을
개선 M5의 복수 사례 실험 후보로 검토했다. PDF를 다시 임의 파싱하지 않고 다음 검수 완료
인덱스를 기준으로 삼는다.

- 인덱스: `/data5/jaehoonjeong/sp/data/processed/manuals/manual_crimefacts_economic_v2`
- 기준 파일: `leaf_raw.jsonl`, `chunks.jsonl`, `manifest.json`
- 사기 범주: `manual_crimefacts_economic::path::016`, 물리면 55~81
- 규모: 21개 leaf. 한 leaf 안에 여러 번호 작성례가 있을 수 있으므로 사건 ID는
  `leaf_id + case_ordinal`로 만든다.

원문 작성례에는 이미 “기망”, “의사나 능력이 없었다”, 적용법조와 결론이 들어 있다. 따라서
그대로 사용하면 label leakage가 생긴다. 이 자료는 우선 **positive pipeline conformance**와
프로파일 coverage 시험에 사용하고, 사실추출·법적 판단 정확도의 주 평가자료로 사용하지 않는다.
성능평가에는 결론 문구가 없는 KCL 원문과 별도의 negative·unknown 대조사례가 필요하다.

## 21개 leaf 분류

| Leaf | 작성례 유형 | 현재 필요한 경로 | 판정 |
|---|---|---|---|
| 046 | 차용사기 | `profile.loan`, 재물·이익 | 1순위. 기존 용도기망 plan을 변제의사·능력형으로 확장 |
| 047 | 변제기일연장 | `profile.loan`, `object.property_benefit` | 1순위. 금전 교부 없는 재산상 이익 시험 |
| 048 | 취업사기 | 공통 core, 장래 이행의사 standard | ordinary plan과 RAG 필요 |
| 049 | 선불금사기 | 공통 core, 장래 이행의사, 일부 광고 | ordinary/advertising plan 필요 |
| 050 | 무전취식 | `profile.implicit_deception`, 재산상 이익 | 1순위. 말 없는 기망과 서비스 이익 시험 |
| 051 | 무임승차 | `profile.implicit_deception`, 재산상 이익 | 050과 같은 축의 반복사례 |
| 052 | 계약금사기 | 공통 core, 장래 이행의사 | ordinary contract plan 필요 |
| 053 | 어음수표사기 | 공통 core, 지급의사·능력, 재산상 이익 | instrument 관련 RAG 필요 |
| 054 | 카드 관련 사기 | 법인 피해, 카드 발급·사용, 일부 제347조의2 | 혼합 leaf. 사례별 죄명 분리 후 사용 |
| 055 | 부동산 관련 사기 | 공통 core + 광고·부작위 가능성 | 지엽 규칙은 RAG, 7개 작성례를 분리 |
| 056 | 물품매매사기 | 공통 core, 대금지급의사 | ordinary purchase plan 후보 |
| 057 | 소송사기 | 삼각구조, 권리행사, 소송 단계 | 전용 litigation profile을 RuleIR로 승격한 뒤 사용 |
| 058 | 투자사기 | 광고, 다수 피해자, 제3자 취득 가능성 | advertising/investment plan 필요 |
| 059 | 대출사기 | 제347조의2와 제347조 사례가 혼재 | 제2 작성례만 현재 제347조 후보 |
| 060 | 보험사기 | 보험사기방지특별법 | 현재 제347조 rule set 밖, future work |
| 061 | 휴대폰 개통 등 사기 | 재물 교부, 장래 지급의사 | ordinary plan 후보 |
| 062 | 중고차 매매 사기 | 광고, 다단계 기망, 공모 | advertising + multi-actor 확장 뒤 사용 |
| 063 | 기타사기 | 제1 작성례는 삼각사기, 제2는 제347조의2 | 제1 작성례를 구조 모듈 시험에 우선 사용 |
| 064 | 특경법 제3조 중 사기 | 제347조 core + 가중처벌·유사수신 경합 | 결론 범위를 확장할 때 사용 |
| 065 | 편의시설부정이용죄 | 형법 제348조의2 | 현재 제347조 범위 밖 |
| 066 | 부당이득 | 형법 제349조 | 현재 제347조 범위 밖 |

2026-07-19 일반화 작업에서 `ordinary`를 포함한 6개 실행 plan을 registry로 만들고,
사건별 역할·거래·질문 template에서 IRAC 단위를 컴파일하도록 교체했다. 아래 첫 확장 배치의
1~5는 같은 M5 러너에 연결되는 상태다. 표의 나머지 “후보”는 여전히 전용 프로파일·카드의
법률 검토가 끝난 뒤 추가해야 한다.

## 첫 확장 배치

| 순서 | 사건 ID | 선택 이유 | 새로 검증하는 경계 |
|---:|---|---|---|
| 1 | `leaf::046/case::1` | 전형적인 무자력 차용 | 용도기망이 아닌 변제의사·능력형 loan plan |
| 2 | `leaf::047/case::1` | 변제기 연장으로 이자 상당 이익 취득 | 재물 교부 없는 재산상 이익 adapter |
| 3 | `leaf::050/case::1` | 대금 지급 의사 없이 주문 | 묵시적 기망 + 서비스 이익 |
| 4 | `leaf::052/case::1` | 공급 의사·능력 없이 계약금 수령 | ordinary 장래 이행의사와 단순 채무불이행 경계 |
| 5 | `leaf::063/case::1` | 경비원을 속여 제3자 택배 수령 | 피기망자·처분자와 재산 피해자 분리 |
| 6 | `leaf::057/case::2` | 허위 청구 후 반소로 미수 | 소송사기 삼각구조와 실행착수·미수 |

1~5는 기존 15개 실행 모듈을 넓게 시험한다. 6은 관련 NormCard가 현재 retrieval-only에
남아 있으므로, 사람이 litigation core를 선별해 새 프로파일로 승인한 뒤 실행한다. 이 순서면
공통 core가 먼저 안정된 다음 특수 소송 규칙으로 넘어갈 수 있다.

## 구현 현황

1. 완료: `allowed_profiles`·`required_profiles`·`reasoning_plan_id` 사건 계약을 도입했다.
2. 완료: 6개 프로파일별 카드계획과 공통 core를 JSON registry로 분리했다.
3. 완료: 역할·거래·계획 template 기반 typed IRAC unit builder로 교체했다.
4. 완료: RAG query를 계획별 template으로 교체했다.
5. 완료: 첫 5건에 원문 전문 대신 `leaf_id`, 순번, 물리면, 원문 segment hash를 기록했다.
6. 부분 완료: 결론형 문구를 제거한 5개 challenge input을 만들었다. 사람 gold와 의도적으로
   조작한 negative 대조사례는 실제 neural 평가 전에 추가해야 한다.

## 다음 neural 실행의 종료 기준

- 첫 5개 비소송 사례가 같은 M5 코드 경로에서 실행된다.
- 모든 사건에서 FactGraph, 카드평가, Scallop, IRACPlan, host-compiled 답안이 계약을 통과한다.
- 사례별 활성 프로파일과 비활성 프로파일이 사람 검수표에 보인다.
- 정적 위반뿐 아니라 사람 gold 기준의 구성요건 적용 오류와 false-positive를 기록한다.
- warm latency를 FactGraph, assessment, Scallop, IRAC application으로 분해한다.
- 소송사기는 전용 core 카드의 사람 승인이 끝나기 전에는 실행 성공 수에 포함하지 않는다.
