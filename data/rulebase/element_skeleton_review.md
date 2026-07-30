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

## 무엇을 답해 주시면 되는지

각 항목마다 역할 하나만 골라 주세요: `core` / `presumed` / `stage` / `defeater` / `concurrence` / `context`.
제안 역할이 맞으면 넘어가셔도 됩니다. 판단 기준은 **'이 명제들이 검사가
증명해야 하는 요건을 말하는가'** 입니다.

- 요건을 말한다 → 그 요건이 통상 다투어지면 `core`, 자명하면 `presumed`
- 미수·기수 시기를 말한다 → `stage`
- 성립을 저지하는 사유를 말한다 → `defeater`
- 다른 죄와의 관계를 말한다 → `concurrence`
- 요건이 아니라 의의·판례 예시·처벌 규정이다 → `context`

---

## 분류 예시 — 자동 분류가 판정한 실제 슬롯

아래는 검수 대상이 **아닌**, 자동 분류가 확정한 슬롯들입니다. 각 역할이 실제로
어떤 카드 묶음에 붙는지 보시고 같은 기준으로 판정해 주세요.

### `core` 예시 — art297 · `art297_sec6` — 고의

- 왜 `core`인가: 카드가 모두 '이것이 있어야 죄가 된다'를 말합니다. 고의는 사안마다 다투어지므로 검사가 적극적으로 증명해야 하는 요건입니다.
- 심볼릭에서의 효과: 이 슬롯이 `satisfied`가 되지 않으면 해당 죄는 성립하지 않습니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | standard_input | 강간죄에는 폭행·협박으로 피해자를 강간한다는 인식과 의사가 필요하고, 미필적 고의로도 충분하다. |
| 2 | exception | negative | standard_input | 피해자 승낙이 없음에도 승낙이 있다고 오인한 경우 강간죄의 고의가 조각된다. |

### `presumed` 예시 — art335 · `art335_sec2` — 주체

- 왜 `presumed`인가: 요건이기는 하나 사안에서 거의 다투어지지 않습니다. 카드도 '주체는 절도범이다'라는 확인과, 그에 해당하지 않는 경우를 짚는 예외로 구성되어 있습니다.
- 심볼릭에서의 효과: 답안이 언급하지 않아도 통과하고, 카드가 `not_satisfied`로 명시 반증될 때만 죄의 성립을 막습니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 준강도의 주체는 절도범이며, 절도의 실행에 착수한 이상 절도 기수인지 미수인지는 묻지 않는다. |
| 2 | exception | exception | deterministic_rule | 절취행위에 착수하지 않은 단순한 절도 예비단계에서 폭행·협박을 하였더라도 준강도죄에 해당하지 않는다. |
| 3 | exception | exception | deterministic_rule | 절도죄의 객체인 재물이 아닌 재산상 이익을 취득하려고 폭행·협박을 한 경우에는 준강도죄가 성립할 수 없다. |

### `stage` 예시 — art329 · `art329_sec3_3` — 기수시기

- 왜 `stage`인가: 요건의 충족 여부가 아니라 **언제 기수가 되는가**를 말합니다.
- 심볼릭에서의 효과: 성립 게이트에는 들어가지 않고 기수/미수 판정에만 쓰입니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | standard_input | 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다. |
| 2 | standard | positive | standard_input | 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다. |

### `defeater` 예시 — art297 · `art297_sec5` — 피해자의 승낙

- 왜 `defeater`인가: 충족되면 죄의 성립을 **저지**하는 사유입니다. 요건과 방향이 반대입니다.
- 심볼릭에서의 효과: `satisfied`가 되면 다른 요건이 모두 충족되어도 죄가 성립하지 않습니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | exception | exception | standard_input | 피해자 본인의 성관계 승낙은 구성요건 해당성을 조각하며, 친권자 등의 승낙은 강간죄 성립에 영향을 주지 않는다. |
| 2 | exception | negative | standard_input | 피해자가 사전에 성관계를 승낙했더라도 동의를 번복하면 승낙이 있다고 볼 수 없다. |
| 3 | standard | positive | standard_input | 성관계 승낙 여부는 행위 경위와 태양, 피해자 연령, 범행 당시 정황 등을 종합해 성적 자유 또는 성적 자기결정권 침해 여부를 기준으로 구체적·개별적으로 판단한다. |
| 4 | standard | negative | standard_input | 피해자가 범행 무렵까지 피고인과 전화·문자 연락을 하고 호감을 보인 정황만으로 성관계 승낙 또는 묵인을 인정할 수는 없다. |

### `concurrence` 예시 — art319 · `art319_sec6_1` — 죄수

- 왜 `concurrence`인가: 계속범·포괄일죄처럼 **다른 죄 또는 다른 행위와의 관계**를 말합니다.
- 심볼릭에서의 효과: 성립 판단에는 쓰이지 않고, 죄수 정의(`absorbed_by`)의 초안 재료가 됩니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | deterministic_rule | 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이다. |
| 2 | exception | negative | deterministic_rule | 주거침입죄 기수 후 퇴거요구에 불응하더라도 별도로 퇴거불응죄는 성립하지 않는다. |
| 3 | standard | positive | standard_input | 주거침입 후 잠시 나왔다가 다시 들어간 경우 포괄일죄가 된다. |
| 4 | standard | positive | standard_input | 무단침입으로 유죄판결이 확정된 뒤에도 퇴거하지 않고 계속 거주하면, 판결확정 이후의 침입행위 및 위법상태 계속으로 별도의 주거침입죄가 된다. |

### `participation` 예시 — art297 · `art297_sec4_4` — 공동정범

- 왜 `participation`인가: 공범·신분 등 형법총칙 영역입니다. 총칙 주석서를 적재하지 않았으므로 대응 규칙이 없습니다.
- 심볼릭에서의 효과: 성립 판단에 쓰이지 않습니다. 서술 재료로만 남습니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | negative | standard_input | 선행자와의 공동가공 의사에 기한 기능적 행위지배를 후행자에게 인정할 수 없으면 승계적 공동정범은 성립할 수 없다는 대법원 취지가 소개되어 있다. |
| 2 | standard | positive | standard_input | 선행자의 행위를 이용하여 피해자를 간음한 후행자에게는 준강간죄가 성립할 여지가 있다. |

### `context` 예시 — art250 · `art250_sec1_1` — 의의

- 왜 `context`인가: 죄의 정의·연혁·판례 예시입니다. 증명의 대상이 아닙니다.
- 심볼릭에서의 효과: 성립 판단에 쓰이지 않고 Rule 문단 서술에만 쓰입니다.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | deterministic_rule | 살인죄는 고의로 사람을 살해하여 사람의 생명을 끊는 범죄이다. |
| 2 | definition | positive | deterministic_rule | 살인 피해자가 보통의 사람인 경우 보통살인죄가 된다. |

### 경계 사례 — 제목과 내용이 어긋난 슬롯

art329 · `art329_sec3_1` — 개념: 제목이 '개념'이라 **`context`**로 분류됐지만, 카드는 절취의 성립 범위를 정하고 있어
행위 요건(`core`)에 가깝습니다. 이런 슬롯은 검수 대기열에 올라오지 않으므로,
눈에 띄면 슬롯 ID만 알려 주세요.

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 기망이 점유침탈의 방법에 불과하여 기망으로 재물의 교부 또는 점유 이전이 있었다고 보기 어려운 경우에는 사기죄가 아니라 절도죄가 성립한다. |
| 2 | definition | positive | standard_input | 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다. |

---

## blocking — 역할을 특정하지 못한 슬롯

제목에서 역할을 읽어내지 못했습니다. `제안 역할`은 `norm_kind`만으로 둔 잠정값입니다.

### B1. art129 · `art129_sec1` — 단순수뢰죄

- 제안 역할: **`core`**  |  카드 1장 (standard_input 0)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 수뢰죄는 공무원 또는 중재인이 직무에 관하여 뇌물을 수수·요구 또는 약속한 때 성립한다. |
> comment: context (만약 수뢰죄에서 구성요건 다루는 카드가 없다면 core)
### B2. art250 · `art250_sec1_9` — 이른바 ‘시신 없는 살인’

- 제안 역할: **`core`**  |  카드 3장 (standard_input 3)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 살인죄처럼 법정형이 무거운 범죄도 직접증거 없이 간접증거만으로 유죄를 인정할 수 있고, 시체가 발견되지 않아도 관련 간접증거를 상호 관련하에 종합적으로 고찰하여 살인 공소사실을 인정할 수 있다. |
| 2 | element | positive | standard_input | 시신 없는 살인사건에서 유죄를 인정하려면 피해자의 사망, 피고인의 살의, 피고인 행위에 의한 피해자 사망이 요구된다고 판례 입장을 정리할 수 있다. |
| 3 | standard | negative | standard_input | 시신이 없고 사망 경위·살해방법·피고인의 구체적 행동 및 원인행위가 불명하며, 피고인 행위와 사망을 직접 연결할 객관적 흔적이나 의미 있는 정황적 접점이 부족하고 다른 사망 가능성을 배제할 수 없는 사안에서는 살인죄 책임을 인정하기 어렵다는 대법원 판단이 소개되어 있다. |
> comment: 1, 2, 3 context
### B3. art301 · `art301_sec4_5` — 수면 또는 의식불명의 상태, 외상 후 스트레스 장애 등

- 제안 역할: **`context`**  |  카드 4장 (standard_input 4)  |  사유: commentary parse artifact, not a heading

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | standard_input | 외부 상처가 없더라도 육체적·정신적 생리기능 훼손, 예컨대 보행불능·수면장애·식욕감퇴 등의 기능장애가 발생하면 상해로 인정될 수 있다. |
| 2 | definition | positive | standard_input | 심각한 외상 후 나타나는 외상 후 스트레스 장애도 상해로 인정될 수 있다. |
| 3 | standard | positive | standard_input | 수면유도 약물로 피해자가 일시적 수면 또는 의식불명 상태가 되고 건강상태가 불량하게 변경되거나 생활기능 장애가 초래되면, 외부 상처가 없거나 자연 회복하더라도 상해에 해당한다. |
| 4 | standard | positive | standard_input | 성범죄 후 외상 후 스트레스 장애의 상해 여부 및 인과관계는 피해자가 필연적으로 겪는 정도의 증상인지, 의사 진단·소견, 범행 내용, 구체적 증상, 치료 내용과 경과, 기존 정신과 치료 전력 등을 고려하여 판단한다. |
> comment: all context
### B4. art328 · `art328_sec6_3` — (예컨대 산

- 제안 역할: **`context`**  |  카드 2장 (standard_input 0)  |  사유: commentary parse artifact, not a heading

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | exception | exception | deterministic_rule | 2022년 1월 28일 이후 범하여진 장애인 피해 재산범죄 중 장애인복지법상 장애인학대관련범죄에 해당하는 제355조, 제356조 및 제357조의 횡령·배임 관련 범죄에는 친족상도례가 적용되지 않는다. |
| 2 | exception | exception | deterministic_rule | 재산범죄를 가중처벌하는 특별법에서도 형법상 재산범죄의 성질이 유지되는 경우, 친족상도례 배제의 명시적 규정이 없으면 친족상도례가 적용된다. |
> comment: all context
### B5. art335 · `art335_sec3_3` — 범죄의 흔적 인멸

- 제안 역할: **`context`**  |  카드 1장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | standard_input | 범죄 흔적 인멸은 절도범이 검거될 때 범행의 증명자료가 되는 증거를 소멸시키는 것을 말하며, 범행 목격자 또는 증거물 인멸에 장애가 되는 사람에게 죄증을 무효화할 목적으로 폭행·협박하는 경우를 포함한다. |
> comment: core - 준강도에 대하여 한정되는 카드지?
### B6. art335 · `art335_sec7_1` — (형법 제342조)

- 제안 역할: **`context`**  |  카드 2장 (standard_input 2)  |  사유: commentary parse artifact, not a heading

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | variant | positive | standard_input | 준강도의 기수·미수는 절취행위가 기수에 이르렀는지를 기준으로 정한다. |
| 2 | standard | positive | standard_input | 대법원은 준강도의 기수 여부를 절도행위의 기수 여부를 기준으로 판단하여야 한다고 하여 준강도미수를 인정하는 입장으로 변경하였다. |
> comment: 1번 stage, 2번 context
### B7. art337 · `art337_sec3_2` — (형법 제257조)

- 제안 역할: **`context`**  |  카드 4장 (standard_input 4)  |  사유: commentary parse artifact, not a heading

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 상해 여부는 피해자의 신체 완전성 훼손 또는 생리적 기능 장애를 객관적·일률적으로 판단하지 않고, 연령·성별·체격 등 신체상·정신상의 구체적 상태를 기준으로 판단한다. |
| 2 | definition | positive | standard_input | 강도상해·치상죄의 상해는 피해자의 건강상태가 불량하게 변경되고 생활기능에 장애가 초래된 경우를 말하며, 특히 중할 것을 요구하지 않는다. |
| 3 | exception | exception | standard_input | 추적을 벗어난 뒤 현장에서 상당히 떨어진 지점에서 체포면탈 목적으로 상해를 가하거나, 범행 종료 후 상당 기간이 지나 새로 범의를 일으켜 범행한 경우에는 강도의 기회에 한 행위로 보기 어렵다. |
| 4 | exception | exception | standard_input | 치료가 필요 없이 자연치유되고 일상생활에 아무 지장이 없는 극히 경미한 상처는 강도상해·치상죄의 상해에 해당하지 않는다. |
> comment: all context
### B8. art343 · `art343_sec2` — 요건

- 제안 역할: **`context`**  |  카드 1장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | standard_input | 예비는 범죄의 의사로 이를 실현하기 위하여 하는 모든 준비행위로서, 아직 실행에 착수하기 전 단계의 행위이다. |
> comment: core
### B9. art343 · `art343_sec2_1` — 주관적 요소

- 제안 역할: **`context`**  |  카드 1장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | variant | positive | standard_input | 행위자에게 미필적으로라도 강도를 할 목적이 인정되면 강도예비·음모죄가 성립한다. |
> comment: core
### B10. art343 · `art343_sec2_2` — 객관적 요소

- 제안 역할: **`core`**  |  카드 1장 (standard_input 0)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 흉기 준비, 가옥침입 준비, 침입방법 또는 재물 반출방법의 기획·입안은 강도예비에 해당한다. |
> comment: core
### B11. art350 · `art350_sec4_1` — 공갈

- 제안 역할: **`core`**  |  카드 4장 (standard_input 3)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 공갈행위에는 협박을 수단으로 하는 경우뿐 아니라 폭행을 수단으로 하는 경우도 포함된다. |
| 2 | standard | positive | standard_input | 공갈수단이 사람을 외포하게 하기에 족한지는 객관적으로 판단한다. |
| 3 | standard | negative | standard_input | 객관적으로 사람을 외포시키기에 부족한 행위는 상대방이 현실로 외포심을 일으켰더라도 공갈이 아니므로 공갈죄가 성립하지 않고 절도죄가 성립할 여지가 있다. |
| 4 | standard | negative | standard_input | 협박이나 폭행이 상대방의 반항을 억압할 정도에 이르면 공갈죄가 아니라 강도죄가 성립한다. |
> comment: 1번 core, 2번 context, 3, 4번 concurrence
### B12. art350 · `art350_sec6_2` — 대가를 지급한 경우

- 제안 역할: **`context`**  |  카드 2장 (standard_input 2)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 공갈로 인해 교부하지 않았을 재물 또는 처분하지 않았을 재산상 이익을 교부·처분하게 된 경우, 상당한 대가를 지급하였더라도 공갈죄가 성립한다. |
| 2 | causal_link | negative | standard_input | 폭행·협박을 당한 상대방이 객관적으로 상당한 대가에 주관적으로도 만족하여 재물을 교부한 경우에는 해악의 고지와 처분행위 사이의 인과관계가 부정되어 공갈죄 미수가 성립한다. |
> comment: 1번 core, 2번 stage
### B13. art350 · `art350_sec8_1` — 공갈자의 수령할 권리와 불법이득의사

- 제안 역할: **`context`**  |  카드 1장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 정당한 권리를 실현하기 위하여 해악을 고지한 경우에도 그 수단·방법이 사회통념상 허용되는 범위를 넘으면 공갈죄의 실행에 착수한 것이며, 그 판단은 목적과 수단을 전체적으로 종합하여 한다. |
> comment: context
### B14. art350 · `art350_sec8_2` — 채권자의 변제 수령

- 제안 역할: **`core`**  |  카드 6장 (standard_input 6)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | causal_link | positive | standard_input | 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다. |
| 2 | element | positive | standard_input | 재물 또는 재산상 이익을 취득할 권리가 없는 자가 외관상 권리가 있는 것처럼 보이더라도 공갈한 경우에는 권리행사 문제가 아니라 공갈죄가 당연히 성립한다. |
| 3 | standard | positive | standard_input | 권리실현 수단이 사회통념상 허용되는 정도나 범위를 넘는지는 추구 목적과 선택 수단 등 주관적·객관적 측면을 종합하여 판단한다. |
| 4 | exception | exception | standard_input | 채권 실행 또는 손해배상 합의금 수령 등을 위하여 사회통념상 허용 범위의 위협적 언사를 한 경우 공갈죄가 성립하지 않으며, 수반된 협박행위도 별도의 협박죄를 구성하지 않는다. |
| 5 | standard | positive | standard_input | 권리행사에 수반된 공갈행위의 위법성 조각 여부는 권리행사와 수단행위를 전체적으로 관찰하여, 그 공갈행위가 권리행사의 수단으로 사회통념상 용인될 수 있는지에 따라 판단한다. |
| 6 | standard | positive | standard_input | 정당한 권리자가 재물 또는 재산상 이익을 취득하더라도, 권리실행의 수단방법이 사회통념상 허용되는 범위를 넘으면 공갈죄 성립이 방해되지 않는다. |
> comment: 1,2번 core, 3번 context, 4번 defeater, 5번 defeater-context, 6번 coree
### B15. art355 · `art355_sec1_2` — 횡령죄의 본질

- 제안 역할: **`context`**  |  카드 3장 (standard_input 3)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | variant | positive | standard_input | 배임죄의 본질은 신의성실의무에 위반하여 타인의 신뢰를 배반하고 재산을 침해하는 데 있다. |
| 2 | exception | exception | standard_input | 일시사용·손괴·은닉의 의사로 재물을 처분하거나 위탁자를 위한 의사로 권한을 넘은 경우에는 불법영득의사가 없어 횡령죄가 성립하지 않는다. |
| 3 | variant | positive | standard_input | 횡령의 본질은 위탁받은 타인의 재물을 불법하게 영득하는 데 있으므로, 횡령죄가 성립하려면 보관 재물을 자기 소유물처럼 사용·수익·처분하려는 불법영득의 의사가 있어야 한다. |
> comment: 1번 context, 2번 defeater, 3번 core
### B16. art355 · `art355_sec4_1` — 총설

- 제안 역할: **`core`**  |  카드 18장 (standard_input 18)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | standard_input | 배임의 고의에는 타인의 사무처리자로서 임무위배행위를 하고, 그로 인해 자기 또는 제3자가 이익을 취득하며, 본인에게 손해를 가한다는 점에 관한 인식 또는 의사가 필요하다. |
| 2 | definition | positive | standard_input | 배임의 범의는 본인 손해 발생 또는 발생 염려 및 자기 또는 제3자의 재산상 이득에 대한 인식으로 충분하며, 본인에게 손해를 가할 의사나 이득을 얻을 목적은 필요하지 않고 미필적 고의로도 충분하다. |
| 3 | standard | positive | standard_input | 경영상 판단에서 배임의 고의는 판단 경위·동기, 사업 내용, 경제상황, 손실 및 이익 발생 개연성 등을 고려하여 자기 또는 제3자의 이익 취득 및 본인 손해에 대한 인식 아래 한 의도적 행위가 인정되는 경우에 한하여 인정된다. |
| 4 | exception | exception | standard_input | 경영상 판단에서 위와 같은 인식 없이 본인에게 손해가 발생한 결과만으로 배임 책임을 묻거나, 단순한 주의의무 위반 과실만을 이유로 책임을 물을 수 없다. |
| 5 | element | positive | standard_input | 매도인이 주장하는 해제사유가 적법하지 않고, 이를 적법한 해제사유로 믿지 않았거나 그 믿음에 정당한 이유가 없으면 배임의 범의가 인정된다. |
| 6 | exception | exception | standard_input | 임무에 위배한다는 인식이 없으면 배임죄가 성립할 수 없다. |
| 7 | standard | positive | standard_input | 구체적 상황상 법령·계약 또는 신의성실 원칙에 따라 역할·지위에서 당연히 기대되는 행위를 하지 않거나 하지 않아야 할 행위를 하여 자기 또는 제3자의 재산상 이익을 취득시키고 본인에게 손해를 가하면, 그에 관한 고의 또는 불법이득의 의사가 인정된다. |
| 8 | standard | negative | standard_input | 용도가 추상적으로 정해졌더라도 보관자에게 사용처·시기 등에 광범위한 재량이 있고 사후보고나 증빙제출도 요구되지 않는 보관금은, 사용처 설명 또는 증빙 부재만으로 불법영득의사를 추단할 수 없다. |
| 9 | element | positive | standard_input | 횡령죄의 주관적 구성요건으로 행위자 신분 및 보관 중인 타인 재물을 횡령하거나 반환 거부한다는 객관적 구성요건에 대한 고의가 필요하고, 그 인식은 미필적으로도 족하다. |
| 10 | element | positive | standard_input | 미필적 고의는 범죄사실 발생 가능성의 인식과 그 발생 위험을 용인하는 내심의 의사를 필요로 한다. |
| 11 | standard | positive | standard_input | 미필적 고의의 용인 여부는 행위자 진술만이 아니라 외부 행위형태와 구체적 사정을 기초로 일반인의 평가를 고려하여 심리상태를 추인해 판단한다. |
| 12 | standard | negative | standard_input | 엄격한 용도 외 사용 사안이 아니고 피고인이 돈의 행방·사용처에 합리적 설명 및 부합 자료를 제시하면, 특별한 사정이 없는 한 불법영득의사에 의한 횡령을 인정할 수 없다. |
| 13 | definition | positive | standard_input | 횡령죄에서 불법영득의 의사란 타인 재물 보관자가 위탁 취지에 반하여 자기 또는 제3자의 이익을 위하여 권한 없이 재물을 자기 소유물처럼 사실상 또는 법률상 처분하려는 의사이다. |
| 14 | definition | positive | standard_input | 횡령죄의 불법영득의사는 타인의 재물을 보관하는 자가 보관취지에 반하여 정당한 권원 없이 스스로 소유권자처럼 사실상 또는 법률상 처분하려는 의사를 말한다. |
| 15 | exception | exception | standard_input | 반환거부에 동시이행항변권·유치권·상계권 행사 등의 정당한 이유가 있으면 불법영득의사가 인정되지 않는다. |
| 16 | standard | positive | standard_input | 소유자로서 처분하려는 의사가 있으면 사후 반환·변상·전보 의사가 있어도 불법영득의사를 인정할 수 있다. |
| 17 | standard | negative | standard_input | 회사에 개인채권을 가진 대표이사가 회사 보관금으로 자신의 회사 상대 채권을 변제하더라도, 이는 대표이사 권한 내 회사채무 이행행위로 유효하여 불법영득의사가 인정되지 않는다. |
| 18 | variant | positive | standard_input | 회사 관리 자금의 일시 유용은 유용금액의 규모·정도, 시간적 간격 및 상환능력을 객관적으로 평가하여 판단하며, 가벌성이 없다고 볼 정도가 아니면 불법영득의사가 인정된다. |
> comment: 1, 2, 3번 core, 4번 defeater, 5번 core, 6번 defeater, 7번 core, 8번 context, 9번 core, 10, 11번 context, 12번 defeater, 13, 14번 context, 15번 defeater, 16번 core, 17, 18번 context
### B17. art355 · `art355_sec4_3` — 구체적 검토

- 제안 역할: **`core`**  |  카드 12장 (standard_input 10)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | negative | standard_input | 법인을 위한 경비 지출을 정리하기 위한 허위 직원채용·허위급여 처리, 영업실적을 가장하기 위한 변칙 장부정리, 부외부채 변제를 위한 장부상 급여 인상 등 장부상 정리에 불과한 경우에는 불법영득의사가 인정되지 않는다. |
| 2 | standard | positive | standard_input | 공공단체 예산의 항목유용 자체가 위법한 목적을 가지거나 용도가 엄격히 제한된 경우에는, 그 지출이 공공단체를 위한 것이더라도 불법영득의사를 부정할 수 없다. |
| 3 | element | positive | deterministic_rule | 판공비 등을 불법영득의사로 횡령하였다고 인정하려면 업무와 무관한 개인적 이익을 위한 지출 또는 업무 관련 지출이더라도 합리적 범위를 넘는 과다 지출이 증명되어야 한다. |
| 4 | standard | negative | standard_input | 등기를 위한 가장납입으로 회사 자본이 실질적으로 증가하지 않고 납입·인출 전 과정에서 자본금 변동이 없는 경우에는 불법영득의사를 인정하기 어려워 업무상횡령죄가 성립하지 않는다. |
| 5 | standard | positive | standard_input | 가장납입 주금이 회사에 귀속되어 회사 자본이 실질적으로 증가하였는지는 주금 납입 경위와 납입금의 보관·인출 형태 및 경위 등 제반 사정을 종합하여 판단한다. |
| 6 | standard | negative | standard_input | 지출목적에 관한 행위자의 주관적 판단이 객관적으로 심히 부당하지 않다고 사회통념상 인정될 수 있는 경우 불법영득의사가 부정된다. |
| 7 | exception | exception | standard_input | 단체 대표자 개인이 당사자인 민·형사사건의 변호사 비용은 원칙적으로 단체 비용으로 지출할 수 없지만, 분쟁의 실질적 이해관계가 단체에 있고 단체 업무와 깊이 관련되며 단체 이익을 위하여 소송수행 또는 고소대응의 특별한 필요성이 있는 경우에는 예외적으로 지출할 수 있다. |
| 8 | standard | positive | standard_input | 횡령된 예산이 용도가 엄격히 제한된 예산인지는 예산의 근거와 성격, 사용 관행 및 관련 규정을 종합하여 판단한다. |
| 9 | standard | negative | standard_input | 비자금이 장부상 일반자금 속에 은닉되어 있거나 회사 재산인 비자금을 차명계좌에 입금·관리하였더라도, 그것만으로 불법영득의사를 인정할 수 없다. |
| 10 | definition | positive | deterministic_rule | 비자금은 법인 회계장부에서 처리되는 공적 자금이 아니라, 법인 운영자 또는 관리자가 변칙회계 등을 통해 법인회계로부터 분리하여 별도로 관리하는 법인 자금이다. |
| 11 | standard | positive | standard_input | 법인과 무관하거나 개인적으로 착복할 목적임이 명백한 상태에서 법인 회계로부터 분리하거나 변칙회계로 인출·차명보관하여 비자금을 조성한 경우, 그 조성행위 자체로 불법영득의사를 실현한 것으로 인정할 수 있다. |
| 12 | standard | positive | standard_input | 비자금 조성행위자에게 법인 자금을 빼내어 착복할 목적이 있었는지는 법인의 성격, 비자금 조성 동기·방법·규모·기간, 보관방법 및 실제 사용용도 등을 종합하여 판단한다. |
> comment: all context
### B18. art356 · `art356` — 업무상 보관

- 제안 역할: **`core`**  |  카드 5장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | definition | positive | deterministic_rule | 업무상횡령죄의 업무상 보관은 업무자가 업무 수행으로 타인의 재물을 보관하는 것으로, 재물 보관에 관한 위탁신임관계가 보관자의 업무상 지위와 결부되어 성립하는 경우를 말한다. |
| 2 | variant | positive | deterministic_rule | 업무상 보관은 업무상 지위에 따라 당연히 재물을 보관하게 된 경우와 업무자에 대한 위탁자의 구체적 위탁행위로 재물을 보관하게 된 경우 모두에 성립한다. |
| 3 | causal_link | positive | standard_input | 업무상횡령죄의 객체가 되려면 업무상 보관하는 타인의 재물이어야 하며, 재물 점유와 업무 사이에 상호관련성이 있어야 한다. |
| 4 | element | positive | deterministic_rule | 업무상 횡령 또는 배임죄에는 단순 횡령ㆍ배임죄의 보관자 또는 사무처리자 신분에 더하여 업무자 신분이 요구된다. |
| 5 | definition | positive | deterministic_rule | 업무상 횡령과 배임죄는 행위자가 보관하는 타인의 물건 또는 처리하는 타인의 사무가 업무상 임무와 연결된 경우 이를 가중처벌하는 범죄이다. |
> comment: 1, 2, 3, 4번 core, 5번 context
### B19. art356 · `art356_sec2_2` — 업무의 내용

- 제안 역할: **`context`**  |  카드 3장 (standard_input 2)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | exception | negative | standard_input | 일정한 업무에 종사하더라도 그 업무와 무관하게 타인의 재물을 보관하게 된 경우에는 업무상횡령죄가 성립하지 않는다. |
| 2 | exception | exception | deterministic_rule | 업무 내용 자체가 위법하지 않다면 면허ㆍ인가 미취득과 같은 행정절차상 불법이 있더라도 현재 반복ㆍ계속하여 행하여지는 사무는 업무에 해당한다. |
| 3 | standard | negative | standard_input | 사회질서에 반하거나 강행법규에 위반되는 등 법이 절대적으로 금지하는 행위는 업무 의사로 반복하더라도 업무가 되지 못한다. |
> comment: 1번 defeater, 2번 core, 3번 defeater
### B20. art357 · `art357_sec1_3` — 배임죄와의 구별

- 제안 역할: **`core`**  |  카드 2장 (standard_input 1)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | exception | exception | deterministic_rule | 배임수재죄에서는 임무위배행위 또는 재산상 손해를 가하는 것이 필요하지 않다. |
| 2 | element | positive | standard_input | 배임수재죄는 부정한 청탁과 재물 또는 재산상 이익의 취득을 요한다. |
> comment: all core
### B21. art357 · `art357_sec1_4` — 뇌물죄와의 구별

- 제안 역할: **`core`**  |  카드 1장 (standard_input 0)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 배임수재죄는 재물 또는 재산상의 이익을 현실적으로 취득해야 성립한다. |
> comment: all core
### B22. art357 · `art357_sec4` — 배임증재죄

- 제안 역할: **`core`**  |  카드 4장 (standard_input 2)  |  사유: title matched no bucket

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | negative | standard_input | 수재자에게는 부정한 청탁이라도 증재자 입장에서는 부정한 청탁으로 볼 수 없는 사정이 있으면 배임증재죄가 성립하지 않을 수 있으며, 정당한 업무·더 큰 손실 회피·권리 확보 등으로 사회상규나 신의칙에 위배되지 않는 경우가 예시된다. |
| 2 | element | positive | deterministic_rule | 배임증재죄는 재물 등을 현실적으로 공여해야 기수이고, 공여 의사표시 또는 약속만으로는 미수이다. |
| 3 | definition | positive | standard_input | 배임증재죄는 타인의 사무처리자에게 그 임무에 관한 부정한 청탁을 하고 재물 또는 재산상 이익을 공여하여 성립하며, 비신분범이다. |
| 4 | element | negative | deterministic_rule | 배임증재죄의 공여는 타인의 사무처리자에게 할 것을 요하므로, 사무처리자가 아닌 자에게 교부한 경우에는 성립하지 않는다. |
> comment: 1번 defeater, 2번 stage, 3번 core, 4번 defeater
---

## advisory — 역할은 맞을 듯하나 편성이 이상한 슬롯

`norm_kind: element` 카드가 죄수·위법성·공범 절에 편성되어 있습니다. 제목 기준
역할을 그대로 적용했으니, 반대 판단이 필요한 것만 지적해 주세요.

### A1. art129 · `art129_sec1_5` — 죄수

- 적용 역할: **`concurrence`**  |  카드 4장 (standard_input 4)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 단일하고 계속적 범의로 이루어지고 동일 법익을 침해한 반복 수뢰행위는 포괄일죄로 처벌하며, 그러한 범의의 단일성과 계속성을 인정할 수 없으면 각 범행은 별죄로서 경합범이 된다. |
| 2 | standard | positive | standard_input | 단일하고 계속된 범의 아래 동종 범행을 일정 기간 반복하고 피해법익도 동일하다면, 수수일자 사이에 상당한 기간이 있어도 포괄일죄가 될 수 있다. |
| 3 | standard | negative | standard_input | 서로 다른 감정평가법인이 각자의 이해관계에 따라 다른 일시·장소에서 제공한 뇌물을 그때그때 수수한 사안에서는 단일하고 계속된 범의 아래 5회 수수하였다고 보기 어려워 포괄일죄가 아니다. |
| 4 | element | negative | standard_input | 공무원이 재직 중 직무 관련 뇌물수수를 약속하고 퇴직 후 이를 수수한 경우, 약속과 수수가 시간적으로 근접·연속되어도 뇌물수수죄는 성립하지 않는다. |
> comment: 4번은 context같기도해
### A2. art151 · `art151_sec2_6` — 죄수 및 다른 죄와의 관계

- 적용 역할: **`concurrence`**  |  카드 5장 (standard_input 4)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | negative | standard_input | 범인을 알고 적절한 조치를 취할 직무상 의무가 있는 사람이 범인을 도피하게 하여 직무를 유기한 경우, 원칙적으로 범인도피죄만 성립하고 직무유기죄는 별도로 성립하지 않는다는 판례가 소개되어 있다. |
| 2 | standard | negative | standard_input | 범인이 아닌 피의자가 수사기관에서 자신이 범죄를 저지른 것처럼 허위 자백한 경우, 위계에 의한 공무집행방해죄는 성립하지 않는다는 판례 법리가 소개되어 있다. |
| 3 | standard | negative | standard_input | 참고인이 수사기관에서 허위 진술을 한 경우에도, 피의자의 허위 자백에 관한 법리가 마찬가지로 적용된다고 소개되어 있다. |
| 4 | element | positive | standard_input | 허위 진술에 그치지 않고 적극적으로 조작한 허위 증거를 제출하여, 수사기관이 충실히 수사해도 그 허위성을 발견하지 못할 정도에 이르면 위계에 의한 공무집행방해죄가 성립한다. |
| 5 | exception | negative | deterministic_rule | 범인은닉죄와 군형법상 이탈자비호죄의 구성요건을 모두 충족하는 행위는 특별관계에 따라 군형법상 이탈자비호죄만 성립한다. |
> comment: 2, 3번은 context
### A3. art152 · `art152_sec1_5` — 죄수

- 적용 역할: **`concurrence`**  |  카드 4장 (standard_input 3)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 하나의 사건에서 한 번 선서한 증인이 같은 기일에 여러 사실에 관하여 기억에 반하는 허위진술을 계속한 경우 포괄하여 1개의 위증죄가 성립하고, 각 허위진술별 경합범이 되지 않는다. |
| 2 | standard | negative | standard_input | 포괄일죄 관계의 위증 일부에 관하여 확정판결이 있으면, 종전 공소사실과 다른 허위진술 부분이라도 그 기판력이 미쳐 후속 위증죄 부분은 면소되어야 한다. |
| 3 | standard | positive | standard_input | 같은 사건·같은 심급에서 서로 다른 변론기일에 허위진술하더라도 최초 선서의 효력이 유지된 상태에서 증언하였다면 1개의 위증죄만 성립한다. |
| 4 | element | positive | deterministic_rule | 하나의 사건에서 여러 사람에게 각각 개별적으로 위증을 교사한 경우 위증교사죄는 경합범이 된다. |

### A4. art164 · `art164_sec3_5` — 공범

- 적용 역할: **`participation`**  |  카드 2장 (standard_input 2)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 현존건조물방화치상죄와 같은 부진정결과적가중범에서 집단 방화 과정 중 일부가 고의로 살상을 가하여도 다른 집단원에게 사상 결과의 예견가능성이 있으면 다른 집단원도 치사상의 책임을 면할 수 없다. |
| 2 | element | positive | standard_input | 현주건조물등방화치사상죄의 교사범 또는 방조범은 기본범죄의 교사·방조 외에 중한 결과에 대한 예견가능성이 인정되어야 한다. |
 
### A5. art250 · `art250_sec1_18` — 책임

- 적용 역할: **`defeater`**  |  카드 11장 (standard_input 11)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | standard_input | 살인죄 성립을 위해 행위자에게 책임능력이 있어야 하며, 책임능력 판단의 기준 시점은 범행 당시이다. |
| 2 | definition | positive | standard_input | 심신장애는 정신병 또는 비정상적 정신상태와 같은 정신적 장애라는 생물학적 요소와, 그 장애로 사물변별능력 및 행위통제능력이 결여되거나 감소한 심리학적 요소를 모두 요구한다. |
| 3 | exception | negative | standard_input | 정신적 장애가 있더라도 범행 당시 정상적인 사물변별능력이나 행위통제능력이 있으면 심신장애로 볼 수 없다. |
| 4 | standard | positive | standard_input | 충동조절장애·인격장애·소아기호증 등의 비정상적 정신상태는 병적인 경우 심신장애에 해당할 수 있으나, 성격적 결함인 경우에는 심신상실이나 심신미약에 해당하지 않는다. |
| 5 | exception | negative | standard_input | 원칙적으로 충동조절장애와 같은 성격적 결함은 형의 감면사유인 심신장애에 해당하지 않는다. |
| 6 | exception | exception | standard_input | 충동조절장애와 같은 성격적 결함이라도 매우 심각하여 본래 의미의 정신병자와 동등하다고 평가할 수 있으면, 그로 인한 범행은 심신장애로 인한 범행으로 본다. |
| 7 | standard | positive | standard_input | 심신장애의 유무와 정도는 법률적 판단이므로 법원은 전문감정 의견에 반드시 기속되지 않으며, 정신질환의 종류·정도, 범행 경위와 전후 행동 등 제반 사정을 종합하여 독자적으로 판단할 수 있다. |
| 8 | standard | negative | standard_input | 심신장애가 의심되는데도 정신감정을 하지 않고 규범적 요소에만 기초하여 심신장애 주장을 배척하는 것은 위법하다. |
| 9 | exception | negative | standard_input | 범행을 예견하고도 자의로 심신장애를 야기한 뒤 살인을 저지른 경우에는 형법 제10조 제3항에 따라 심신장애로 인한 감경을 할 수 없다. |
| 10 | standard | negative | standard_input | 필로폰 투약으로 인한 환각 상태에서 타인의 생명에 위해를 가할 수 있음을 예견하고도 스스로 심신미약 상태를 야기하여 살인을 저지른 경우에는 심신장애 감경을 할 수 없다. |
| 11 | exception | negative | standard_input | 저항할 수 없는 폭력 또는 자기·친족의 생명·신체에 대한 위해를 방어할 능력이 없는 협박으로 강요된 행위 등 적법행위의 기대가능성이 없는 경우에는 행위자의 책임을 물을 수 없다. |

### A6. art250 · `art250_sec1_19` — 공범

- 적용 역할: **`participation`**  |  카드 23장 (standard_input 21)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | standard_input | 살인 공동정범은 공동가공의 의사와 공동의사에 기한 기능적 행위지배를 통한 범죄 실행이라는 주관적·객관적 요건을 충족해야 한다. |
| 2 | element | negative | standard_input | 공동가공의 의사는 타인의 범행을 인식하면서 이를 제지하지 않고 용인하는 것만으로는 부족하고, 공동의 의사로 특정 범죄행위를 하기 위한 일체성과 상호 이용의 관계를 내용으로 해야 한다. |
| 3 | element | positive | standard_input | 구성요건행위를 직접 분담하지 않은 공모자도 전체 범죄에서의 지위·역할 및 범죄경과에 대한 지배·장악력 등에 비추어 본질적 기여를 통한 기능적 행위지배가 인정되면 공모공동정범이 될 수 있다. |
| 4 | definition | positive | standard_input | 공모는 일정한 법정 형식을 요구하지 않고, 2인 이상이 범죄에 공동가공하여 실현하려는 의사의 결합이 있으면 성립하며, 전체 모의 과정이 없어도 순차적 또는 암묵적 의사 결합으로 성립할 수 있다. |
| 5 | causal_link | positive | standard_input | 공모가 이루어진 경우 실행행위에 직접 관여하지 않은 사람도 다른 공모자의 행위에 대하여 공동정범으로서 형사책임을 진다. |
| 6 | exception | exception | standard_input | 살인 공모에 가담했더라도 다른 공모자가 실행에 착수하기 전에 공모관계에서 이탈하면 이후 다른 공모자의 살인행위에 대해 공동정범 책임을 지지 않으며, 이탈 의사는 반드시 명시적일 필요가 없다. |
| 7 | element | negative | standard_input | 공모에 주도적으로 참여하여 다른 공모자의 실행에 영향을 미친 사람은 범행 저지를 위한 적극적 노력 등으로 자신의 영향력을 제거하지 않으면 공모관계에서 이탈했다고 볼 수 없다. |
| 8 | exception | exception | standard_input | 여러 명이 가벼운 상해 또는 폭행의 범의로 범행하던 중 1인이 살인의 결과를 발생시킨 경우, 나머지 사람들이 살인을 전혀 예측하지 못했다면 그들에게 살인죄 책임을 물을 수 없다. |
| 9 | element | positive | standard_input | 강도살인죄 공동정범의 성립에는 강도 부분뿐 아니라 살인 부분에 관한 고의의 공동이 필요하다. |
| 10 | standard | negative | standard_input | 피해자 사망을 예견한 계속 폭행 사건에서, 주범과 비교하여 폭행 정도·횟수가 현저히 적고 사망 결과를 용인할 동기나 위험한 행위태양이 부족하며 피해자 구조를 시도한 B·C·D에 대해서는 살인의 고의 및 공동정범 법리 오해를 이유로 살인죄 인정 원심을 파기환송한 사례가 소개되어 있다. |
| 11 | standard | negative | standard_input | 실제 살인을 실행하지 않은 A에 대하여 공범 B 진술의 신빙성이 부족하고 대화에 구체적 범행공모를 인정할 증거가 부족한 인천 초등생 살해사건에서, A가 살인 실행 가능성을 진지하게 인식하고 지시·공모했다고 보기 어렵다는 원심 판단을 대법원이 수긍한 사례가 소개되어 있다. |
| 12 | standard | negative | standard_input | 사전 공모에 따른 행위에 관하여 공모자가 총을 버리고 도망간 사정만으로는 공모관계에서 이탈하였다고 볼 수 없다. |
| 13 | element | positive | standard_input | 살인의사가 없던 사람을 교사하여 살인을 결의하게 하고 피교사자가 살인죄를 범한 경우 살인교사죄가 성립한다. |
| 14 | exception | exception | deterministic_rule | 피교사자가 살인을 승낙하지 않았거나 승낙하였더라도 실행의 착수에 이르지 않은 경우, 교사자는 살인예비·음모죄에 준하여 처벌된다. |
| 15 | exception | exception | deterministic_rule | 살인을 교사하였으나 피교사자가 상해행위만 한 경우 교사자는 상해죄의 교사범이 되는 동시에 교사의 미수에 해당하며, 상상적 경합으로 더 무거운 살인예비·음모죄로 처벌한다. |
| 16 | standard | positive | standard_input | 살인의 교사 사실은 범죄사실을 구성하므로 이를 인정하려면 엄격한 증명이 요구된다. |
| 17 | standard | positive | standard_input | 피고인이 교사사실을 부인하면 교사사실과 상당한 관련성이 있는 간접사실을 증명하는 방법으로 이를 증명할 수 있고, 관련 간접사실인지는 경험칙에 바탕을 둔 합리적 판단으로 정한다. |
| 18 | element | positive | standard_input | 살인죄 정범이 범행한다는 점을 알면서 그 실행행위를 용이하게 하는 행위를 한 사람은 살인방조범으로 처벌된다. |
| 19 | element | positive | standard_input | 살인방조범이 성립하려면 방조자가 정범의 살인 실행행위를 방조한다는 고의와 정범 행위가 구성요건에 해당한다는 점에 관한 정범의 고의가 있어야 한다. |
| 20 | standard | positive | standard_input | 살인방조에서 정범의 고의는 정범이 실현할 범죄의 구체적 내용을 인식할 필요 없이 미필적 인식 또는 예견으로 충분하다. |
| 21 | definition | positive | standard_input | 살인방조행위에는 물질적 방조뿐 아니라 정범의 범행결의를 강화하는 정신적 방조도 포함되며, 실행착수 전 장래 실행행위를 예상하여 이를 용이하게 한 경우도 방조범이 성립한다. |
| 22 | standard | positive | standard_input | 공동정범으로 기소된 범죄사실도 공소사실 동일성 범위에서 더 가벼운 방조사실이 인정되고 피고인의 방어에 실질적 불이익이 없다면, 공소장 변경 없이 직권으로 인정할 수 있다. |
| 23 | standard | positive | standard_input | 공동정범의 공동가공의사와 기능적 행위지배가 인정되기 어려운 부모라도, 다른 부모의 구타로 자녀가 사망할 위험을 예견하면서 보호·양육의무를 이행하지 않고 구타를 제지하지 않아 살인을 용이하게 한 경우 살인방조 책임이 인정될 수 있다. |

### A7. art250 · `art250_sec1_20` — 죄수 및 다른 죄와의 관계

- 적용 역할: **`concurrence`**  |  카드 16장 (standard_input 12)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 살인죄의 죄수는 피해자 수에 따라 결정된다. |
| 2 | standard | positive | standard_input | 1개의 행위로 여러 사람을 살해한 경우 여러 개의 살인죄가 성립하고 상상적 경합 관계가 된다. |
| 3 | standard | positive | standard_input | 동일 장소에서 동일 방법으로 시간적으로 접착하여 여러 사람을 살해한 경우 여러 살인죄의 실체적 경합범이 된다. |
| 4 | standard | positive | standard_input | 단일 범의 아래 동일 장소·방법으로 시간적으로 접착된 상황에서 각 피해자의 머리에 실탄을 순차 발사하여 살해한 경우에도 피해자 수에 따라 각 살인죄를 구성한다는 판례가 소개되어 있다. |
| 5 | standard | negative | standard_input | 여러 피해자를 차례로 쇠망치로 강타해 살해한 경우 피해법익이 다르고 각 피해자에 대한 살해의사가 각각 성립하면, 동일 장소·방법으로 시간적으로 접착된 행위라도 포괄적 1죄가 아니며 경합범으로 처단한다는 판례가 소개되어 있다. |
| 6 | exception | exception | deterministic_rule | 동일인에 대한 살인예비·살인미수·살인기수 및 동일인에 대한 상해·살인은 법조경합 관계이므로 하나의 살인죄만 성립한다. |
| 7 | exception | exception | standard_input | 동일인을 살해하려는 동일한 의사발동에서 나온 예비행위 또는 공격행위가 범의 갱신 없이 살인기수에 이른 경우, 시간·장소·방법의 동일 여부와 무관하게 포괄하여 단순한 1개의 살인기수죄로 처단한다는 판례가 소개되어 있다. |
| 8 | exception | exception | deterministic_rule | 살인행위에 따른 의복 손괴는 불가벌적 수반행위로서 재물손괴죄가 살인죄에 흡수된다. |
| 9 | exception | exception | deterministic_rule | 사람을 살해한 뒤 사체를 다른 장소로 옮겨 유기한 경우 사체유기죄가 별도로 성립하며, 이를 불가벌적 사후행위로 볼 수 없다. |
| 10 | exception | negative | standard_input | 살해 목적 수행 중 사체 발견을 어렵게 하려는 의사로 인적 드문 장소로 피해자를 유인하거나 끌고 가 살해한 뒤 사체를 그대로 두고 도주한 경우, 사체 발견이 현저히 곤란해졌더라도 별도 사체은닉죄는 성립하지 않는다. |
| 11 | standard | positive | standard_input | 사람을 살해할 목적으로 현주건조물에 방화하여 사망하게 한 경우 현주건조물방화치사죄로 의율하며 살인죄와 상상적 경합으로 의율하지 않는다. |
| 12 | standard | positive | standard_input | 살인죄가 강도살인죄나 강간살인죄 등 결합범의 일부가 되려면 살인행위가 강도 또는 강간 등의 기회에 이루어져야 하며, 선행 범죄가 완료된 뒤 살해하면 별도 살인죄와 선행 강도죄 또는 강간죄는 실체적 경합관계이다. |
| 13 | exception | negative | standard_input | 채무가 명백하고 채권자의 상속인이 존재하며 채권 확인 방법도 확보된 경우, 채무 면탈 의사로 채권자를 살해하여도 재산상 이익 지배가 이전되었다고 보기 어려워 강도살인죄는 성립하지 않고 살인죄만 성립한다. |
| 14 | standard | positive | standard_input | 피고인의 자백 없이 보복 목적의 존재를 판단할 때에는 피해자와의 관계, 수사단서 제공에 대한 반응, 불이익 내용과 정도, 범행 경위·수단·방법·태양, 전후 정황 등 객관적 사정을 종합 고려해야 한다. |
| 15 | exception | negative | standard_input | 강도범행 후 범행 은폐 목적으로 피해자를 살해한 경우 보복목적 살인이 아니라 강도살인죄가 성립한다. |
| 16 | standard | positive | standard_input | 미성년자 피해자를 약취한 후 강간 목적으로 가혹행위와 상해를 가하고 강간 및 살인미수를 한 경우, 약취 미성년자 상해 관련 특정범죄가중처벌법위반죄와 강간 및 살인미수 관련 성폭력처벌법위반죄는 상해 결과가 후행 행위 과정에서 발생했더라도 실체적 경합관계이다. |

### A8. art255 · `art255_sec6` — 죄수 등

- 적용 역할: **`concurrence`**  |  카드 2장 (standard_input 0)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 하나의 살인범죄 실행을 위한 여러 예비행위는 상호 보완되어 전체로 하나의 준비행위가 되므로 하나의 살인예비죄가 성립한다. |
| 2 | exception | negative | deterministic_rule | 살인예비·음모가 살인미수 또는 살인기수 단계에 이르면 예비·음모죄는 미수 또는 기수죄에 흡수되어 별도로 성립하지 않는다. |

### A9. art257 · `art257_sec1_6` — 위법성

- 적용 역할: **`defeater`**  |  카드 14장 (standard_input 13)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | negative | standard_input | 방어행위가 아닌 상해는 정당방위가 될 수 없고, 서로 싸워 상대방에게 상해를 가한 경우에는 위법성이 조각되지 않는다. |
| 2 | standard | exception | standard_input | 외관상 상호 싸움처럼 보여도 일방의 위법한 공격에 대항한 유형력 행사가 새로운 적극적 공격으로 평가되지 않고 사회관념상 상당하면 위법성이 조각될 수 있다. |
| 3 | element | negative | deterministic_rule | 자상행위는 상해죄의 구성요건에 해당하지 않으므로 타인이 자상에 관여하는 방조·교사 행위도 범죄가 되지 않는다. |
| 4 | standard | exception | standard_input | 복싱·레슬링·유도 등 상해가 예견되는 운동경기에서 규칙을 지켜 경기한 경우 그에 수반된 상해는 승낙에 의해 위법성이 조각될 수 있다. |
| 5 | standard | exception | standard_input | 운전 미숙 또는 음주 사실을 알면서 동승하는 등 운전 위험을 감수하고 동승한 경우 과실상해에 대한 승낙으로 위법성이 조각될 수 있다. |
| 6 | standard | negative | standard_input | 정확하거나 충분한 설명 없이 받은 수술 승낙은 수술의 위법성을 조각할 유효한 승낙이 될 수 없다는 대법원 사례가 소개되어 있다. |
| 7 | standard | negative | standard_input | 징계행위가 교육목적상 필요·적절하고 사회통념상 용인될 정도여야 하므로, 피징계자를 상해에 이르게 한 징계는 원칙적으로 상해죄의 위법성을 조각할 수 없다. |
| 8 | standard | exception | standard_input | 친권자의 체벌은 자녀 보호·교양을 위해 불가피한 경우 극히 제한된 범위에서 사회상규에 반하지 않는 행위로만 허용될 수 있다는 견해가 제시된다. |
| 9 | standard | positive | standard_input | 야간에 술에 취하여 신병들에게 행패를 부리는 피해자를 소대장이 제지하는 과정에서 군대 질서 유지 목적으로 한 경미한 폭행은 사회상규에 위배되지 않는 행위로 위법성이 조각될 수 있다. |
| 10 | standard | negative | standard_input | 상관이 훈련 중 부하 방위병을 감금·구타한 행위가 훈육권 또는 징계권 범위를 넘으면 위법하다. |
| 11 | standard | negative | standard_input | 상사 계급자가 얼차려 결정권자가 아니고 부대 지침상 허용되지 않은 얼차려를 지시한 경우, 그 지시행위는 정당행위에 해당하지 않는다. |
| 12 | standard | positive | standard_input | 개정 전 시행령 적용 사안에서 교사의 폭행·욕설 지도행위는 교육상 필요와 불가피성, 그리고 방법·정도의 객관적 타당성을 모두 갖춘 경우에만 법령에 의한 정당행위가 될 수 있다. |
| 13 | standard | positive | standard_input | 초·중등교육법 시행 전 사안에서 교사의 교육목적 달성을 위한 체벌은 방법과 정도가 사회상규에 벗어나지 않으면 정당행위에 해당할 수 있다. |
| 14 | standard | negative | standard_input | 초·중등교육법 시행 전 사안에서도 교사의 체벌이 상해에 이른 경우 일반적으로 용인되는 교육업무상의 정당행위를 벗어나 위법하다. |

### A10. art259 · `art259_sec2_3` — 죄수, 타죄와의 관계

- 적용 역할: **`concurrence`**  |  카드 2장 (standard_input 0)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 두 사람에게 각각 칼을 휘둘러 한 사람을 사망에 이르게 하고 다른 사람에게 상처를 입힌 경우 상해치사죄와 상해죄의 경합범이 된다. |
| 2 | exception | negative | deterministic_rule | 강도행위 중 상해의 고의로 사람을 상해하여 사망하게 한 경우 강도치사죄만 성립하고 별도로 상해치사죄를 구성하지 않는다. |

### A11. art297 · `art297_sec10` — 피해자 행위의 위법성 조각

- 적용 역할: **`defeater`**  |  카드 3장 (standard_input 3)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | standard_input | 피해자가 행위자의 폭행·협박에 의한 강간에 대항하여 방어 또는 적극적 반격행위를 한 경우, 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것이고 상당한 이유가 있으면 정당방위로 위법성이 조각된다. |
| 2 | standard | positive | standard_input | 심야에 귀가 중인 피해자가 공동으로 강간하려는 행위자에게 끌려가 폭행·추행을 당하던 중 정조와 신체를 지키려 혀를 깨물어 혀 절단상을 입힌 경우 정당방위가 인정된 판례가 소개되어 있다. |
| 3 | standard | negative | standard_input | 계속 성관계를 강요받던 피해자가 남자 친구와 사전 공모하여 범행을 준비하고, 술에 취해 잠든 의붓아버지를 식칼로 살해한 경우 사회통념상 상당성이 결여되어 정당방위가 인정되지 않은 판례가 소개되어 있다. |

### A12. art297 · `art297_sec7` — 죄수

- 적용 역할: **`concurrence`**  |  카드 3장 (standard_input 1)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 동일한 폭행·협박으로 피해자의 항거불가능 또는 현저한 곤란 상태가 계속되는 상황에서 수회 간음한 경우, 시간적·장소적 근접성과 범의의 단일성·계속성이 인정되면 포괄 일죄가 성립한다. |
| 2 | element | positive | deterministic_rule | 항거불능 상태가 종료된 후 다시 폭행·협박을 가하여 간음한 경우 별개의 강간죄가 성립한다. |
| 3 | element | positive | deterministic_rule | 피해자가 여러 명이면 동일한 장소에서 동일한 폭행·협박에 의한 경우에도 각 피해자에 따라 수개의 강간죄가 성립한다. |

### A13. art298 · `art298_sec6` — 죄수

- 적용 역할: **`concurrence`**  |  카드 2장 (standard_input 1)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 원칙적으로 각 추행행위마다 하나의 범죄가 성립하지만, 각 행위가 시간적·장소적으로 가깝고 범의의 단일성과 계속성이 인정되면 포괄일죄가 성립한다. |
| 2 | element | positive | deterministic_rule | 피해자가 여러 명이면 동일 장소에서 동일한 폭행·협박에 의한 경우라도 피해자별로 수개의 죄가 성립한다. |

### A14. art299 · `art299_sec7` — 죄수

- 적용 역할: **`concurrence`**  |  카드 1장 (standard_input 0)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | positive | deterministic_rule | 본죄는 원칙적으로 각 간음행위, 유사간음행위, 추행행위마다 하나의 범죄가 성립한다. |

### A15. art301 · `art301_sec6` — 공동정범

- 적용 역할: **`participation`**  |  카드 2장 (standard_input 1)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | exception | exception | deterministic_rule | 강간 등을 공모한 공범이 다른 공범자의 실행착수 전, 즉 폭행·협박 전 공범관계에서 이탈한 경우 다른 공범자의 행위에 대해 공동정범 책임을 지지 않는다. |
| 2 | element | negative | standard_input | 고의범인 강간 등 상해죄에서 공모자에게도 상해에 대한 고의가 필요하므로, 그 고의를 인정하기 어려우면 공동정범으로 처벌할 수 없다. |

### A16. art329 · `art329_sec6` — 위법성·책임성의 문제

- 적용 역할: **`defeater`**  |  카드 2장 (standard_input 2)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | negative | standard_input | 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다. |
| 2 | variant | negative | standard_input | 피해자의 승낙이 있는 경우에는 절취에 해당하지 않아 절도죄의 구성요건해당성이 인정되지 않는다. |

### A17. art355 · `art355_sec5` — 위법성조각사유 관련

- 적용 역할: **`defeater`**  |  카드 1장 (standard_input 1)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | element | negative | standard_input | 유치권이나 동시이행 항변권 행사로 반환을 거부하는 경우에는 불법영득의사가 인정되지 않아 구성요건해당성이 없다. |

### A18. art366 · `art366_sec5_2` — 정당행위

- 적용 역할: **`defeater`**  |  카드 4장 (standard_input 4)

| # | norm_kind | polarity | formalization | 명제 |
|---:|---|---|---|---|
| 1 | standard | positive | standard_input | 부동산 자력탈환권의 행사가 직시에 이루어졌는지는 물리적 시간뿐 아니라 침탈자의 점유 확립, 법적 안정·평화 침해 및 권리남용 여부를 함께 살펴 판단한다. |
| 2 | element | positive | standard_input | 정당행위는 동기·목적의 정당성, 수단·방법의 상당성, 법익균형성, 긴급성 및 보충성 등의 요건을 갖춘 경우에 인정된다. |
| 3 | standard | positive | standard_input | 부당한 점유침탈을 배제하고 위험발생을 방지하기 위해 자물쇠나 전기선을 절단한 경우, 침해가 과도하지 않아 사회통념상 현저히 타당성을 잃지 않으면 정당행위가 된다. |
| 4 | definition | positive | standard_input | 사회상규에 위배되지 아니하는 행위란 법질서 전체의 정신, 사회윤리 또는 사회통념에 비추어 용인될 수 있는 행위이다. |
> comment: 1, 4번 context

## 참고 — `core` 슬롯이 없는 조문

`art254`, `art300`, `art328`, `art342`, `art344`

미수범 규정(제254·300·342조)과 친족상도례(제328·344조)는 고유 구성요건이 없는
조문이므로 `core` 슬롯이 없는 것이 정상입니다. 이 목록에 다른 조문이 나타나면
스켈레톤 누락입니다.
