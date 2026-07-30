# 요건 스켈레톤 검수 요청 — `slot_core` / `slot_presumed`

RuleIR 카드에는 '이 카드가 어느 죄의 어느 요건인가'가 없습니다. 주석서 목차
(`section_title`)와 `norm_kind` 두 신호로 자동 도출했고, 아래는 **자동 판정이
닿지 않은 항목만** 추린 것입니다.

- 전체 슬롯 **402** / 조문 **51**
- 자동 분류: `core` 161, `context` 91, `presumed` 51, `stage` 38, `concurrence` 35, `defeater` 17, `participation` 9
- 검수 대상 **40건** (blocking 22, advisory 18)

## 판정이 필요한 이유

`slot_core`는 **적극적 충족을 요구**하고 `slot_presumed`는 **반증이 있을 때만**
죄의 성립을 막습니다. 모든 요건에 적극적 충족을 요구하면, 시험 답안이 자명한
주체·객체를 논하지 않으므로 그 슬롯이 영구히 `unknown`이 되어 어떤 죄도
성립하지 않습니다. 그래서 이 구분이 파이프라인의 동작 여부를 좌우합니다.

역할별 의미:

| 역할 | 죄 성립에 미치는 효과 |
|---|---|
| `core` | 충족되지 않으면 죄 불성립 (행위·고의·인과관계 등) |
| `presumed` | 반증되지 않으면 충족으로 취급 (주체·객체) |
| `stage` | 기수/미수 판단에만 사용 |
| `defeater` | 충족되면 죄 성립을 저지 (위법성·책임) |
| `concurrence` | 죄수 관계 판단 재료 |
| `context` | 성립 판단에 미사용 (의의·판례 예시) |
| `participation` | 총칙 공범 영역 — 현재 규칙 없음 |

## blocking — 역할을 특정하지 못한 슬롯

자동 판정이 제목에서 역할을 읽어내지 못했습니다. `제안 역할`은 `norm_kind`만으로
둔 잠정값이니 맞는지 봐 주세요.

| 조문 | 슬롯 | 주석서 제목 | 카드 | 제안 역할 | 사유 |
|---|---|---|---:|---|---|
| art129 | `art129_sec1` | 단순수뢰죄 | 1 | `core` | title matched no bucket |
| art250 | `art250_sec1_9` | 이른바 ‘시신 없는 살인’ | 3 | `core` | title matched no bucket |
| art301 | `art301_sec4_5` | 수면 또는 의식불명의 상태, 외상 후 스트레스 장애 등 | 4 | `context` | commentary parse artifact, not a heading |
| art328 | `art328_sec6_3` | (예컨대 산 | 2 | `context` | commentary parse artifact, not a heading |
| art335 | `art335_sec3_3` | 범죄의 흔적 인멸 | 1 | `context` | title matched no bucket |
| art335 | `art335_sec7_1` | (형법 제342조) | 2 | `context` | commentary parse artifact, not a heading |
| art337 | `art337_sec3_2` | (형법 제257조) | 4 | `context` | commentary parse artifact, not a heading |
| art343 | `art343_sec2` | 요건 | 1 | `context` | title matched no bucket |
| art343 | `art343_sec2_1` | 주관적 요소 | 1 | `context` | title matched no bucket |
| art343 | `art343_sec2_2` | 객관적 요소 | 1 | `core` | title matched no bucket |
| art350 | `art350_sec4_1` | 공갈 | 4 | `core` | title matched no bucket |
| art350 | `art350_sec6_2` | 대가를 지급한 경우 | 2 | `context` | title matched no bucket |
| art350 | `art350_sec8_1` | 공갈자의 수령할 권리와 불법이득의사 | 1 | `context` | title matched no bucket |
| art350 | `art350_sec8_2` | 채권자의 변제 수령 | 6 | `core` | title matched no bucket |
| art355 | `art355_sec1_2` | 횡령죄의 본질 | 3 | `context` | title matched no bucket |
| art355 | `art355_sec4_1` | 총설 | 18 | `core` | title matched no bucket |
| art355 | `art355_sec4_3` | 구체적 검토 | 12 | `core` | title matched no bucket |
| art356 | `art356` | 업무상 보관 | 5 | `core` | title matched no bucket |
| art356 | `art356_sec2_2` | 업무의 내용 | 3 | `context` | title matched no bucket |
| art357 | `art357_sec1_3` | 배임죄와의 구별 | 2 | `core` | title matched no bucket |
| art357 | `art357_sec1_4` | 뇌물죄와의 구별 | 1 | `core` | title matched no bucket |
| art357 | `art357_sec4` | 배임증재죄 | 4 | `core` | title matched no bucket |

## advisory — 역할은 맞을 듯하나 편성이 이상한 슬롯

`norm_kind: element` 카드가 죄수·위법성·공범 절에 편성되어 있습니다. 제목 기준
역할을 그대로 썼으니 반대 판단이 필요하면 알려 주세요.

| 조문 | 슬롯 | 주석서 제목 | 카드 | 적용 역할 |
|---|---|---|---:|---|
| art129 | `art129_sec1_5` | 죄수 | 4 | `concurrence` |
| art151 | `art151_sec2_6` | 죄수 및 다른 죄와의 관계 | 5 | `concurrence` |
| art152 | `art152_sec1_5` | 죄수 | 4 | `concurrence` |
| art164 | `art164_sec3_5` | 공범 | 2 | `participation` |
| art250 | `art250_sec1_18` | 책임 | 11 | `defeater` |
| art250 | `art250_sec1_19` | 공범 | 23 | `participation` |
| art250 | `art250_sec1_20` | 죄수 및 다른 죄와의 관계 | 16 | `concurrence` |
| art255 | `art255_sec6` | 죄수 등 | 2 | `concurrence` |
| art257 | `art257_sec1_6` | 위법성 | 14 | `defeater` |
| art259 | `art259_sec2_3` | 죄수, 타죄와의 관계 | 2 | `concurrence` |
| art297 | `art297_sec10` | 피해자 행위의 위법성 조각 | 3 | `defeater` |
| art297 | `art297_sec7` | 죄수 | 3 | `concurrence` |
| art298 | `art298_sec6` | 죄수 | 2 | `concurrence` |
| art299 | `art299_sec7` | 죄수 | 1 | `concurrence` |
| art301 | `art301_sec6` | 공동정범 | 2 | `participation` |
| art329 | `art329_sec6` | 위법성·책임성의 문제 | 2 | `defeater` |
| art355 | `art355_sec5` | 위법성조각사유 관련 | 1 | `defeater` |
| art366 | `art366_sec5_2` | 정당행위 | 4 | `defeater` |

## 참고 — `core` 슬롯이 없는 조문

`art254`, `art300`, `art328`, `art342`, `art344`

미수범 규정(제254·300·342조)과 친족상도례(제328·344조)는 고유 구성요건이 없는
조문이므로 `core` 슬롯이 없는 것이 정상입니다. 이 목록에 다른 조문이 나타나면
스켈레톤 누락입니다.
