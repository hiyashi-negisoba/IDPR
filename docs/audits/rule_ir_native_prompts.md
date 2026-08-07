# Lean RuleIR-native KCL 프롬프트 감사

- 상태: **pass**
- 모델/API 호출: 0
- 신경망 단계: closed issue selection → full predicate assessment → section prose

## 프롬프트 고정값

| stage | system SHA-256 | user SHA-256 | 계약 문구 |
|---|---|---|---|
| `issue_select` | `884f90a226bc77145f7ed4f7f64160e8d0a2ff49b7526f24a571efbfe0749895` | `c1aff928ddba42c5fe7b6327f2525214445bda94c6326180da8327eedbfa49fb` | pass |
| `predicate_assess` | `718f715f6e2d29c44ec86ca6a29bbfa9c16ccda72e45a91d6ce91093d8f909ef` | `f360b2d08bcf062dcac97696b5849d7c9635bbd04f25eb59252e67f2b79568b2` | pass |
| `section_write` | `5a5d00fe629de13f351ec7c92069c56acdb739462b4076ef5eef75a11e80be98` | `e7a3ca08b2fe519973b176dd058135041dda95fa8cef5cdbefbcb807348a1680` | pass |

## 불변식

- 초기 검색과 generic FactGraph가 없다.
- 선택 enum은 등록 RuleIR 36개와 `unsupported`뿐이다.
- 선택 unit의 모든 predicate와 역할이 schema required field다.
- 미지원 쟁점은 `predicate_ir_missing`이며 모델 결론을 받지 않는다.
- writer는 section별 Markdown만 쓰고 결론은 호스트가 붙인다.
