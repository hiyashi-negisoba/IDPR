# IDPR Data

Raw legal texts are not committed. Keep source, license, transformation notes,
and filtering decisions here.

Known local sources for development:

- Bar exam essay material: `/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay`
- Commentary chunks: `/home/jaehoonjeong/data/sp_qwen/data/serve/commentary_chunks`

Inventory artifacts:

- `data/inventory/kcl_criminal_v1_draft.jsonl`: KCL essay 형사법 61개 설문 분해 및 태깅 초안
- `data/inventory/kcl_criminal_v1_review.md`: 사람 검수용 요약표
- `data/inventory/kcl_criminal_v1_tag_counts.md`: 고유 issue tag 집합과 문항별 출현 빈도

Commentary bundle artifacts:

- `data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl`: 165개 issue tag별 commentary metadata target manifest
- `data/commentary/kcl_criminal_v1_commentary_chunks.jsonl`: `(law_id, article_no)` metadata 기준으로 전량 수집하고 `comment_id`로 중복 제거한 commentary chunks
- `data/commentary/kcl_criminal_v1_commentary_review.md`: 사람 검수용 tag-target 요약표
- `data/commentary/kcl_criminal_v1_commentary_pool.json`: 원천 hash, 포함·제외 규칙, 102개 target과 3,108개 selected chunk의 재현 명세
- `data/commentary/kcl_criminal_v1_non_mapped_audit.md`: 기존 비-mapped 33개 tag의 전수 육안 검토와 필요한 추가 corpus

Fraud rule-generation artifacts:

- `data/rulegen/fraud/fraud_commentary_index.json`: 형법 제347조 127개 chunk의 section별 index
- `data/rulegen/fraud/fraud_rulegen_requests.jsonl`: API pass-1용 13개 metadata-bounded request
- `data/rulegen/fraud/fraud_norm_card_set_exemplar.json`: 출처와 검수 상태가 붙은 8개 NormCard 모범 초안
- `data/rulegen/fraud/fraud_rule_ir_exemplar.json`: 출처 검증 가능한 사기죄 RuleIR 모범 초안
- `rules/exemplars/fraud_v1_candidate.scl`: RuleIR에서 결정론적으로 컴파일한 Scallop 초안

Regeneration:

```bash
/data5/jaehoonjeong/miniconda3/bin/python scripts/build_kcl_criminal_inventory.py
/data5/jaehoonjeong/miniconda3/bin/python scripts/build_kcl_criminal_commentary_bundle.py
/data5/jaehoonjeong/miniconda3/bin/python scripts/build_fraud_rulegen_exemplar.py
```
