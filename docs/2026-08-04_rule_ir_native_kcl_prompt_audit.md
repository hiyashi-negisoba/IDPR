# Lean RuleIR-native KCL 프롬프트 감사

- 상태: **pass**
- 모델/API 호출: 0
- 신경망 단계: closed issue selection → full predicate assessment → section prose

## 프롬프트 고정값

| stage | system SHA-256 | user SHA-256 | 계약 문구 |
|---|---|---|---|
| `issue_select` | `a4955e7bdca52a92ac0359d3fcc83bc9c5c94e829b5d72b664f034c7aa679f8c` | `c1aff928ddba42c5fe7b6327f2525214445bda94c6326180da8327eedbfa49fb` | pass |
| `predicate_assess` | `fb4cc49f7b1026b97f2b2a6aae0a47b8003e499190687bc231ed61e58dd50bef` | `f360b2d08bcf062dcac97696b5849d7c9635bbd04f25eb59252e67f2b79568b2` | pass |
| `section_write` | `47d5449f672ffd16f39335c811430083af2f957903ebd75f841cf1074d1fac09` | `40b07561e956cbd1dcbca8018061aa28d2d60fc970812f91dc7ae3e5f0cb155b` | pass |

## 불변식

- 초기 검색과 generic FactGraph가 없다.
- 선택 enum은 등록 RuleIR 36개와 `unsupported`뿐이다.
- 선택 unit의 모든 predicate와 역할이 schema required field다.
- 미지원 쟁점은 `predicate_ir_missing`이며 모델 결론을 받지 않는다.
- writer는 section별 Markdown만 쓰고 결론은 호스트가 붙인다.
