# 검토 A — 카드가 출처 범위를 넘었는지 판정

총 **59건**. 결론에 흘러드는 카드(Scallop 규칙·모델 판단 입력)만 담았습니다.

## 하실 일

각 항목에서 **카드 명제**와 **출처 원문**을 비교해 한 가지만 답해 주세요.

- `넓음` — 출처보다 넓습니다 → **제가 출처 범위로 좁히겠습니다**
- `괜찮음` — 이 정도 일반화는 타당합니다 → 그대로 둡니다
- 비워두시면 `괜찮음`으로 처리합니다.

좁히는 문장 작성은 제가 합니다. 판정만 해주시면 됩니다.


---

## art328 / sec1_1

### 1. `art328_sec1_1.article1_application_suspension`

**카드 명제**
> 헌법불합치결정에 따라 개선입법 시한인 2025년 12월 31일까지 형법 제328조 제1항을 적용하여 형 면제 판결을 선고할 수 없다.

**출처 원문**
> 위 헌법불합치결정에서는 2025. 12. 31.까지 개선 입법을 요구하면서 위 시한 까지의 적용을 중지하였는바, 이에 따라 재판절차에서도 위 개선 입법 시한까지 형법 제328조 제1항의 친족상도례 규정을 적용할 수 없게 되었다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The source states that Article 328(1) cannot be applied in judicial proceedings until the legislative deadline, but the card narrows this into an inability to render a sentence-exemption judgment. That specific procedural consequence is not stated in the bounded commentary and requires statutory or other supporting material.

</details>

**판정 (넓음 / 괜찮음):** 이건 그냥 너무 trivial한 카드야 필요없어.


---

## art328 / sec1_3

### 2. `art328_sec1_3.nonkinship_proof_burden`

**카드 명제**
> 친족상도례 적용 여부에서 친족관계가 없다는 점의 증명책임은 검사에게 있다.

**출처 원문**
> 하고 그 증명책임은 검사에게 있다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

제공된 문서가 문장 중간인 '하고 그 증명책임은 검사에게 있다'에서 시작하므로, 증명책임의 대상이 곧 '친족관계가 없다는 점'이라고 이 범위만으로 확정할 수 없다. review_notes의 불확정성 표시만으로는 단정적인 proposition과 deterministic_rule 형식화를 보완하지 못한다.

</details>

**판정 (넓음 / 괜찮음):** 지금 출처원문이 잘렸어. 다만 명제자체는 맞음


---

## art328 / sec3_2

### 3. `art328_sec3_2.full_adoption_ends_pre_adoption_kinship`

**카드 명제**
> 친양자 입양이 확정되면 입양 전 친족관계가 종료한다.

**출처 원문**
> 친양자의 입양 전의 친족관계는 친양자 입양이 확정된 때에는 종료한다

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

출처는 입양 전 친족관계의 종료를 민법 제908조의3 제2항 '본문'의 효과로 한정하고 있어 단서 또는 예외의 존재 가능성을 표시한다. 카드는 이 한정을 제거하여 친양자 입양 확정 시 언제나 친족관계가 종료하는 것으로 정리했다.

</details>

**판정 (넓음 / 괜찮음):**


---

## art328 / sec6_3

### 4. `art328_sec6_3.disabled_victim_abuse_crimes_no_application`

**카드 명제**
> 2022년 1월 28일 이후 범하여진 장애인 피해 재산범죄 중 장애인복지법상 장애인학대관련범죄에 해당하는 제355조, 제356조 및 제357조의 횡령·배임 관련 범죄에는 친족상도례가 적용되지 않는다.

**출처 원문**
> 따라서 2022. 1. 28. 이후 범하여진 장애인이 피 해자인 재산범죄 중 장애인복지법 제2조 제4항 제11호 및 제12호에 따른 장애인 학대관련범죄

**지적**: 카드 명제와 출처 규범이 어긋난다는 지적입니다.

<details><summary>상세</summary>

이 카드는 연결된 후보가 포함한 장애인학대관련범죄의 전체 열거 범위 중 제347조, 제347조의2, 제348조, 제350조, 제350조의2 및 제352조에 해당하는 사기·공갈 관련 범죄를 누락하고 제355조부터 제357조까지로 축소하였다. 전체 commentary chunk는 사기·공갈 관련 열거와 횡령·배임 관련 열거 모두에 친족상도례가 적용되지 않는다고 명시하므로, 현재 카드는 후보를 완전하게 구현하지 않는다.

</details>

**판정 (넓음 / 괜찮음):** 출처가 끊김. 이렇게 엉망이었어?

### 5. `art328_sec6_3.disabled_victim_abuse_crimes_no_application`

**카드 명제**
> 2022년 1월 28일 이후 범하여진 장애인 피해 재산범죄 중 장애인복지법상 장애인학대관련범죄에 해당하는 제355조, 제356조 및 제357조의 횡령·배임 관련 범죄에는 친족상도례가 적용되지 않는다.

**출처 원문**
> 따라서 2022. 1. 28. 이후 범하여진 장애인이 피 해자인 재산범죄 중 장애인복지법 제2조 제4항 제11호 및 제12호에 따른 장애인 학대관련범죄

**지적**: 카드가 출처에 없는 내용까지 담았다는 지적입니다.

<details><summary>상세</summary>

제공된 인용이 제355조·제356조·제357조 외의 범위를 뒷받침하지 않는다는 메모는 bounded commentary chunk 전체를 고려하지 않은 판단이다. 같은 chunk의 본문에는 제347조, 제347조의2, 제348조, 제350조, 제350조의2 및 제352조가 명시되어 있다.

</details>

**판정 (넓음 / 괜찮음):** 동일한게 지금 두번 들어가있음


---

## art329 / sec2

### 6. `art329_sec2.theft_object_anothers_property_in_possession`

**카드 명제**
> 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다.

**출처 원문**
> 여기서 말하는 타인의 재물은 타인 소유의 재물로서 타인의 점유 아래 있는 것을 뜻한다.

**지적**: 카드가 출처에 없는 내용까지 담았다는 지적입니다.

<details><summary>상세</summary>

임치 포장물·용기 내용물, 점유보조자의 사실상 지배 기준 및 이에 관한 미해결 견해 대립은 제공된 commentary chunk에 나타나지 않는다. 이 한정된 출처만으로는 그러한 구체적 쟁점이나 견해 대립을 카드에 귀속시킬 수 없다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec2_2

### 7. `art329_sec2_2.abandoned_license_plate`

**카드 명제**
> 자동차 등록번호판이 손으로 떼어낼 수 있을 정도로 관리상태가 불량하고 소유자가 소유권을 포기하였거나 점유 의사로 사실상 지배하였다고 볼 수 없는 경우, 그 등록번호판은 절도죄의 객체가 될 수 없다.

**출처 원문**
> 그 당시 그 소유권을 포기한 것이거나 적어도 점유할 의사로 사실상 지배하 고 있었다고는 볼 수 없으므로 그 등록번호판을 절도죄의 객체라고 할 수 없

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The card turns a fact-specific abandoned-vehicle outcome into a broader rule keyed mainly to a readily removable license plate and lack of control or intent. The source outcome also rests on prolonged nonpayment and attachment history, long-term abandonment, the owner's fugitive status, broken windows, flat tires, and overall poor management.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec3_3

### 8. `art329_sec3_3.completion.control_and_disposal`

**카드 명제**
> 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다.

**출처 원문**
> 타인의 재물을 자기의 실력적 지배 아래에 둠으로 써 배타적으로 자유로이 처분할 수 있는 상태가 되면 족하므로 영구적으로 안 전하게 그 물건의 경제적 가치를 보전하여 이를 이용 처분할 수 있는 상태에까 지 두어야 하는 것은 아니다.

**지적**: 카드 명제와 출처 규범이 어긋난다는 지적입니다.

<details><summary>상세</summary>

연결된 후보는 절도 기수에 완전한 경계망 이탈이 필요하지 않다는 부정적 한계도 포함하지만, 카드 명제는 이를 누락하였다. 이는 후보가 제시한 기수 기준의 범위를 불완전하게 옮긴 것이다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec8_10

### 9. `art329_sec8_10.trade_secret_cd_misuse_separate_offense`

**카드 명제**
> 부정한 이익을 얻을 목적으로 타인의 영업비밀이 담긴 CD를 절취하여 그 영업비밀을 부정사용한 경우, 절도죄와 별도로 부정경쟁방지 및 영업비밀보호에 관한 법률 위반죄가 성립한다.

**출처 원문**
> 부정한 이익을 얻을 목적으로 타인의 영업비밀이 담긴 CD를 절취해 그 영업비밀을 부정사용한 경우, 절도죄와 별도로 부정경쟁방지 및 영업비밀보호에 관한 법률 제18조 제2항 위반죄가 성립한다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The source identifies the separate offense specifically as a violation of Article 18(2), but the proposition broadens this to an unspecified violation of the entire Unfair Competition Prevention and Trade Secret Protection Act.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec8_4

### 10. `art329_sec8_4.stolen_document_forgery_not_subsequent_act`

**카드 명제**
> 절취물에 관한 문서위조행위는 절도의 불가벌적 사후행위로 볼 수 없다.

**출처 원문**
> 문서위조행위를 절도의 불가벌적 사후행 위라고 볼 수는 없다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

‘절취물에 관한 문서위조행위’라는 표현은 모든 절취물 관련 문서위조로 범위를 넓힌다. 출처는 절취한 어음 용지나 차용증서 등에 위조 인장을 찍어 타인 명의 문서를 위조한 구체적 경우에 관하여 불가벌적 사후행위가 아니라고 설명한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec8_5

### 11. `art329_sec8_5.kill_then_theft_real_concurrence`

**카드 명제**
> 절도의 범의 없이 살인한 후 재물을 절취한 경우, 사자의 점유 계속을 인정할 타당성이 있으면 절도죄가 성립하고 살인죄와 절도죄는 실체적 경합범이다.

**출처 원문**
> 절도의 범 의 없이 살인을 한 후 재물을 절취한 경우에는 이미 앞서 사자의 점유(☞ 제329 조 Ⅱ. 2. 라. 주석 참조)에 관하여 설명한 바와 같이 사자의 점유 계속을 인정할만 한 타당성이 있는 한 단순한 점유이탈물횡령이 아니라 절도죄가 성립하므로 살 인과 절도의 실체적 경합범이다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

검토 메모는 '절취 당시 절도의 범의 부재'를 평가하도록 하지만, 출처와 proposition의 요건은 살인 당시 절도의 범의가 없었다는 것이다. 이후 재물을 절취하는 단계의 범의 부재로 바꾸면 시간적 요건이 왜곡되고 절도죄 성립 설명과도 충돌한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art329 / sec8_8

### 12. `art329_sec8_8.theft_fraud_real_concurrence`

**카드 명제**
> 절도죄와 사기죄가 수단 또는 결과의 견련관계에 있는 경우에도 실체적 경합범이다.

**출처 원문**
> 이 경우에 절도죄와 사기죄는 서로 수단 또는 결과의 견련관계에 있으나 실체적 경합범이다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition states generally that theft and fraud are in substantive concurrence whenever they have an instrumental or result relationship. The source says "이 경우에," limiting that conclusion to the preceding stolen-property fraud situations. The review note recognizes this limitation, but the proposition itself does not.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art331 / sec3_3

### 13. `art331_sec3_3.absentee_conspirator_group_theft`

**카드 명제**
> 3명 이상이 합동절도를 공모하고 적어도 2명이 범행현장에서 시간적·장소적으로 협동하여 실행행위를 분담한 경우, 현장 공모자가 실행정범의 행위를 자기 의사 실현수단으로 삼았다고 평가할 만한 정범성 표지를 갖추면 합동절도의 공동정범을 인정할 수 있다.

**출처 원문**
> 3명 이상의 범인이 합동절도의 범행을 공모한 후 적어도 2명 이상의 범인이 범행현 장에서 시간적·장소적으로 협동관계를 이루면서 실행행위를 분담하여 범행을 한 경우에는 공동정범의 일반 이론에 비추어 단순한 공모자에게도 합동절도의 공동정범을 인정할 수 있다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The proposition conditions liability on a '현장 공모자' possessing the required indicia, but the source addresses the 공모자 who is not at the scene and distinguishes that person from the two or more on-scene perpetrators. '현장 공모자' materially changes the actor covered by the reported precedent standard.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art331 / sec4_1

### 14. `art331_sec4_1.joint_methods-inclusive-single-offense`

**카드 명제**
> 제331조 제1항과 제2항의 범행 방법을 함께 사용하여 특수절도죄를 저지른 경우에는 특수절도의 포괄일죄가 성립한다.

**출처 원문**
> 형법 제331조 제1항과 제2항의 범행 방법을 함께 사용하여 특수절도죄를 저지른 경우, 예컨대 흉기를 휴대하고 야간에 문이나 담 그 밖의 건조물 일부를 손괴한 후 건조물 등에 침입하여 절취행위를 하거나 또는 2인 이상이 합동하여 흉기를 휴대하고 위와 같은 절취행위를 한 경우 등에서는 특수절도의 포괄일죄가 성립 한다고 보아야 한다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The bounded commentary states the inclusive-single-offense treatment for combined methods, but it does not identify that treatment as an exception to another norm. The classification as "exception" therefore requires review or additional support.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art334 / sec1

### 15. `art334_sec1.nighttime_robbery_damage_irrelevant`

**카드 명제**
> 손괴행위 수반 여부와 관계없이 야간 강도행위는 제334조 제1항의 특수강도죄로 처단된다.

**출처 원문**
> 손괴행위가 수반된 것이든 아니든 야간 강도행위는 모두 본항의 특수강도죄로 처단되게 된다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

‘야간 강도행위’를 모든 야간 강도행위로 읽히게 표현했으나, 출처는 제334조 제1항의 야간주거침입강도와 그에 대응하는 손괴 후 야간주거침입절도 규정의 부재를 논하는 문맥이다. 현재 명제는 주거침입 등 제1항의 장소적·행위적 범위와 무관한 야간 강도까지 포괄할 수 있다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art335 / sec3

### 16. `art335_sec3.special_purpose`

**카드 명제**
> 준강도죄는 재물탈환 항거, 체포 면탈 또는 범죄 흔적 인멸 중 하나의 목적을 가지고 폭행·협박을 하여야 하는 목적범이다.

**출처 원문**
> 준강도죄는 아래 중 하나의 목적을 가지고 폭행·협박을 하여야 성립하므로, 이 른바 목적범에 해당한다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The bounded commentary states only that violence or intimidation must be committed for one of the purposes listed elsewhere below. It does not identify those purposes as resistance to recovery of property, evasion of arrest, or destruction of traces of the crime. The card therefore asserts details not supported by the available commentary chunk.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art335 / sec6_1

### 17. `art335_sec6_1.days_later_no_opportunity`

**카드 명제**
> 범행 수일 후 재물탈환 방지 또는 체포 면탈 목적으로 폭행을 한 경우에는 준강도죄가 성립될 수 없다.

**출처 원문**
> 범행 수일 후 피해자에게 발각되어 재물탈환을 방지할 목적으로 폭행을 가 한다거나 또는 절도범이 범행 수일 후 체포하러 온 경찰관에 대하여 체포를 면 하고자 폭행을 가한 경우에는 준강도죄가 성립될 수 없다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition turns two fact-specific examples into a broader categorical rule covering any violence committed several days later for recovery prevention or arrest evasion. The source separately describes violence after discovery by the victim to prevent recovery and violence against a police officer who came to arrest the thief, and introduces them as examples.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art337 / sec5

### 18. `art337_sec5.co-offender-unforeseeable-violence`

**카드 명제**
> 절도 공모자가 다른 공모자의 체포면탈 목적 폭행을 전혀 예기할 수 없었던 경우, 그 공모자에게 준강도상해죄의 공동책임을 물을 수 없다는 판례가 소개된다.

**출처 원문**
> 피고인은 위 갑의 폭행행위를 전연 예기할 수 없었다고 보이므로 피고인에게 준강도상해죄의 공동책임을 지울 수 없다고 한 것도 있는바

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

소개된 판례는 피고인이 인기척의 정체가 확인되기 전에 도주하여 상당한 거리를 벗어난 것으로 추정된 구체적 사정에 기초해 폭행을 전혀 예견할 수 없었다고 판단한다. 현재 명제는 이 사실상 한계를 제거하여 모든 예견 불가능 사례에 적용되는 일반 판례 법리처럼 넓혔다.

</details>

**판정 (넓음 / 괜찮음):** 

### 19. `art337_sec5.withdrawal-before-execution-functional-control`

**카드 명제**
> 공모자가 공모로 담당한 기능적 행위지배를 해소하고 실행에 미친 영향력을 제거하지 않으면 공모관계 이탈을 인정할 수 없다는 판례가 소개된다.

**출처 원문**
> 공모관계에서의 이탈은 공모에 의 하여 담당한 기능적 행위지배를 해소하는 것을 필요로 하므로 공모자가 공모에 주도적으로 참여하여 다른 공모자의 실행에 영향을 미친 때에는 범행을 저지하 기 위하여 적극적으로 노력하는 등 실행에 미친 영향력을 제거하지 아니하는 한 공모관계에서 이탈하였다고 할 수 없다고 판시

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

현재 명제는 모든 공모자가 기능적 행위지배 해소와 실행 영향력 제거를 모두 해야 하는 것처럼 표현한다. 출처는 기능적 행위지배 해소를 일반적으로 언급한 뒤, 공모를 주도하여 다른 공모자의 실행에 영향을 미친 경우에 적극적 노력 등으로 그 영향력을 제거해야 한다고 한정한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art337 / sec6_1

### 20. `art337_sec6_1.quasi_robbery_injury_single_offense`

**카드 명제**
> 포괄하여 준강도상해죄의 일죄가 성립하고 별도로 준강도죄가 성립하지 않는다고 판시한 소개된 판례가 있다.

**출처 원문**
> 포괄하여 준강도상해죄의 일죄가 성립하고 별도로 준강도죄가 성립하는 것은 아니라고 판시한 것이 있다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

판례 결과만 기재하고 그 결과를 한정하는 사실관계, 즉 절도범이 체포를 면탈하려고 추격자 A에게 상해를 가한 후 계속 도주하면서 다른 추격자 B를 협박한 경우라는 요건을 누락하였다. 현재 문언은 모든 준강도상해죄와 준강도죄의 관계에 적용되는 일반 판례 규범처럼 읽힌다.

</details>

**판정 (넓음 / 괜찮음):** 

### 21. `art337_sec6_1.inn_manager_injury_guests_real_concurrence`

**카드 명제**
> 시간적으로 접착된 상황에서 동일한 방법으로 이루어진 행위라도 포괄하여 하나의 강도상해죄를 구성하지 않고 강도상해죄와 강도죄의 실체적 경합범 관계에 있다고 한 소개된 판례가 있다.

**출처 원문**
> 피고인의 위와 같은 행 위는 비록 시간적으로 접착된 상황에서 동일한 방법으로 이루어지기는 하였으 나 포괄하여 1개의 강도상해죄를 구성하는 것이 아니라 강도상해죄와 강도죄의 실체적 경합범의 관계에 있다고 한다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

소개된 판례의 결론을 여관 관리인에 대한 상해·강취 후 각 객실 투숙객에게 별도로 강취한 사실관계에서 분리하여, 시간적으로 접착되고 방법이 동일한 모든 행위에 적용되는 일반 명제로 표현하였다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art338 / sec2

### 22. `art338_sec2.debt_evasion_robbery`

**카드 명제**
> 채권자에게 상속인이 없거나 채권 행사가 불가능한 경우, 또는 채무자에게 불리한 채무 경개가 요구되어 채무가중을 피하려는 상황에서 채권자를 살해하여 채무를 면탈하거나 채무가중을 피하면 재산적 이익지배의 취득이 있어 강도에 해당하고 강도살인죄를 구성한다.

**출처 원문**
> 채권자에게 상속인이 없거나 상속인이 있더라도 그 채권의 존재를 알 수 없 어 그 행사 가능성이 없는 때 또는 살해 직전에 채권자가 채무자에게 불리한 채 무 내용의 경개를 요구함으로써 채무자의 지위가 더욱 불리하게 될 상황에 있 었다든가 하는 경우에는 채권자를 살해함으로써 채무를 면탈하거나 또는 채무 가중의 불이익을 면하는 등 재산적 이익지배의 취득이 있다고 볼 수 있는 것이 므로 이는 강도에 해당한다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

‘채권 행사가 불가능한 경우’라는 표현은 출전보다 넓다. 출전은 상속인이 있더라도 그 상속인이 채권의 존재를 알 수 없어 행사 가능성이 없는 경우를 제시하며, 모든 원인의 채권 행사 불가능성을 일반적으로 포함하지 않는다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art338 / sec3

### 23. `art338_sec3.delayed_death_no_effect`

**카드 명제**
> 살해행위가 강도의 기회에 가해진 이상 사망 결과가 즉시 발생하지 않고 시간적 간격을 두고 발생하여도 강도살인·치사죄 성립에는 영향이 없다.

**출처 원문**
> 살해행위가 강도의 기회에 가해진 이상 사망의 결과가 그 즉시 발생하지 않고 약간의 시간적 간격을 두고 발생한 경우

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition treats any temporal interval before death as irrelevant. The source's general statement is limited to a slight temporal interval, while the longer six-hour and 50-kilometer example depends on additional facts, including implementation of the original plan to conceal the crime. The deterministic formulation therefore exceeds the stated general norm.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art338 / sec7

### 24. `art338_sec7.specific_violent_crime`

**카드 명제**
> 강도살인·치사죄와 그 미수죄는 특정강력범죄의 처벌에 관한 특례법 제2조 제1항 제5호의 특정강력범죄에 해당한다.

**출처 원문**
> 강도살인, 치사죄와 그 미수죄는 특정강력범죄의 처벌에 관한 특례법 제2조 제1항 제5호의 ‘특정강력범죄’에 해당

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The description that classification is confirmed '열거적으로' suggests an exhaustive classification rule. The source establishes only that the named offenses and attempts qualify; it does not state that the list is exhaustive.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art343 / sec2_2

### 25. `art343_sec2_2.conspiracy_concrete_agreement`

**카드 명제**
> 2인 이상이 범행 실행을 구체적으로 상호 합의한 경우 음모의 요건을 충족한다.

**출처 원문**
> 2인 이상이 위와 같은 범행의 실행을 구체적으로 상호 합의한 경우에는 음모의 요건을 충족한다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

‘범행 실행’이라는 표현은 강도 실행을 논하는 출처 문맥보다 넓다. 이 카드의 요건이 모든 범죄의 음모에 일반적으로 적용되는 것처럼 읽힐 수 있다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art344 / x_raw_pdf

### 26. `art344_x_raw_pdf.reported_kinship_classifications`

**카드 명제**
> 주석은 범인이 피해자의 부의 외사촌 동생인 경우, 피해자가 범인의 친할머니의 동생인 경우 및 피해자와 외사촌남매간인 경우에 관한 판례를 소개한다.

**출처 원문**
> 범인이 피해자의  부의 외사촌 동생(즉 피해자가 범인의  고종사촌 형수)인          
                                                                    
           경우 및 피해자가  범인의 친할머니의  동생이라든지   피해자와  외사촌남매간이라

**지적**: 카드 명제와 출처 규범이 어긋난다는 지적입니다.

<details><summary>상세</summary>

The card does not faithfully preserve its linked candidate. It omits both the reported conclusion that the listed relationships fall within Article 328 kinship and the fourth listed relationship, where the victim is the offender's paternal aunt. The full bounded commentary text expressly supplies both points.

</details>

**판정 (넓음 / 괜찮음):** 

### 27. `art344_x_raw_pdf.reported_kinship_classifications`

**카드 명제**
> 주석은 범인이 피해자의 부의 외사촌 동생인 경우, 피해자가 범인의 친할머니의 동생인 경우 및 피해자와 외사촌남매간인 경우에 관한 판례를 소개한다.

**출처 원문**
> 범인이 피해자의  부의 외사촌 동생(즉 피해자가 범인의  고종사촌 형수)인          
                                                                    
           경우 및 피해자가  범인의 친할머니의  동생이라든지   피해자와  외사촌남매간이라

**지적**: 카드가 출처에 없는 내용까지 담았다는 지적입니다.

<details><summary>상세</summary>

The note treats the provenance excerpt's mid-sentence ending as if the remainder of the bounded source were unavailable. The supplied full commentary chunk states the conclusion and includes the additional paternal-aunt category. Primary-precedent verification may remain a review issue, but recovery of these details does not require consulting material outside the bounded chunk.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art350 / sec10_2

### 28. `art350_sec10_2.public_official_no_duty_execution`

**카드 명제**
> 공무원이 직무집행 의사 없이 또는 직무처리에 대한 대가관계 없이 타인을 공갈하여 재물을 교부하게 한 경우, 재물교부자는 공갈죄 피해자이고 뇌물공여죄는 성립하지 않는다는 판례 입장이 소개되어 있다.

**출처 원문**
> 공무원이 직무집행의 의사 없이 또는 직무처리와 대가적 관계없이 타인 을 공갈하여 재물을 교부하게 한 경우에는 공갈죄만 성립하고, 이러한 경우 재 물의 교부자가 공무원의 해악의 고지로 인하여 외포의 결과 금품을 제공한 것 이라면 그는 공갈죄의 피해자가 되어 뇌물공여죄가 성립하지 않는다

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition categorically treats the property provider as an extortion victim for every case involving absence of an intent to perform official duties or a quid pro quo. The reported precedent additionally conditions that conclusion on the provider having supplied the property because the official's threatened harm produced fear.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art350 / sec10_7

### 29. `art350_sec10_7.cash_card_continuing_extortion`

**카드 명제**
> 피해자로부터 현금카드를 교부받은 행위와 그 카드로 현금자동지급기에서 예금을 여러 번 인출한 행위가 피해자의 예금을 갈취하려는 단일하고 계속된 범의 아래의 일련의 행위이면, 포괄하여 하나의 공갈죄만 성립하고 별도 절도죄는 성립하지 않는다.

**출처 원문**
> 피고인이 피해자로부터 현금카드를 교부받은 행위와 이 를 사용하여 현금자동지급기에서 예금을 여러 번 인출한 행위는 모두 피해자의 예금을 갈취하고자 하는 피고인의 단일하고 계속된 범의 아래에서 이루어진 일 련의 행위로서 포괄하여 하나의 공갈죄만 성립하고, 이와 별도로 절도죄가 성립 하지는 않는다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The statement that the cited material does not mention non-establishment of 컴퓨터등 사용사기죄 is contradicted by the full bounded commentary text, which expressly says that the offense likewise does not arise.

</details>

**판정 (넓음 / 괜찮음):** 

### 30. `art350_sec10_7.cash_card_continuing_extortion`

**카드 명제**
> 피해자로부터 현금카드를 교부받은 행위와 그 카드로 현금자동지급기에서 예금을 여러 번 인출한 행위가 피해자의 예금을 갈취하려는 단일하고 계속된 범의 아래의 일련의 행위이면, 포괄하여 하나의 공갈죄만 성립하고 별도 절도죄는 성립하지 않는다.

**출처 원문**
> 피고인이 피해자로부터 현금카드를 교부받은 행위와 이 를 사용하여 현금자동지급기에서 예금을 여러 번 인출한 행위는 모두 피해자의 예금을 갈취하고자 하는 피고인의 단일하고 계속된 범의 아래에서 이루어진 일 련의 행위로서 포괄하여 하나의 공갈죄만 성립하고, 이와 별도로 절도죄가 성립 하지는 않는다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition applies to any receipt of a victim's cash card followed by withdrawals under a continuing extortion intent, while the reported precedent concerns a card obtained by threatening the account holder and relies on the resulting defective consent remaining uncancelled and the absence of a stop-payment request. Omitting those circumstances broadens the precedent beyond the supplied source.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art350 / sec5_3

### 31. `art350_sec5_3.delivery_tacit_acquiescence`

**카드 명제**
> 상대방이 외포에 따라 묵인하는 동안 공갈자가 직접 재물을 탈취한 경우에도 공갈죄가 성립할 수 있다.

**출처 원문**
> 묵인하고 있는 동안에 공갈자가 직접 재물을 탈취한 때에도 공갈죄가 성립한다고 보고 있다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

The referenced commentary chunk concerns third-party receipt and does not support the card's proposition about direct taking during fear-induced acquiescence. The excerpt is also only a sentence fragment from an unrelated proposition.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art350 / sec8_2

### 32. `art350_sec8_2.extortion_loss_despite_payment_duty`

**카드 명제**
> 상대방에게 교부·이전 의무가 있더라도 공갈로 인한 외포가 없었다면 교부·이전하지 않았을 재물 또는 재산상 이익을 외포로 교부·이전한 경우, 그 범위에서 재산상 손해가 발생하여 공갈죄의 정형성이 인정된다.

**출처 원문**
> 공갈을 당하여 외포하지 않았더라면 교부 또는 이전하지 않았을 재물 또는 재산상의 이익을 공갈을 당하여 외포하게 됨으로써 재물을 교부하거나 재산상의 이익을 이전하였다면

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

The proposition states without qualification that the extortion offense's typicality is established, but the commentary says it is only prima facie established ("일응 인정된다"). Omitting that qualification makes the card broader and more conclusive than its source.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec3_1

### 33. `art355.breach_transfer_security_pre_settlement_registration`

**카드 명제**
> 가등기담보법 시행 후 약한 의미의 양도담보에서 채권자가 정산절차 전에 제3자에게 가등기를 설정한 행위에 배임죄 성립을 인정한 원심을 수긍한 대법원 판결이 소개되어 있다.

**출처 원문**
> 채권자가 부동산에 관하여 정산절차를 거치기 이전 에 제3자에게 가등기를 설정한 행위에 대하여 배임죄의 성립을 인정한 원심을 수긍한 대법원 판결이 있고

**지적**: 카드가 출처에 없는 내용까지 담았다는 지적입니다.

<details><summary>상세</summary>

카드는 해당 판결을 '가등기담보법 시행 후'의 법 적용 사례로 제시하지만, 같은 출처는 그 사안이 차용물 반환에 관한 재산권 이전예약에 해당하지 않아 가등기담보법이 적용되는 사안은 아닌 것으로 보인다고 명시한다. 현재 명제는 판결의 적용 법률과 일반화 가능성을 반대로 표시한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec3_2

### 34. `art355.breach.confidential-information`

**카드 명제**
> 비밀유지의무를 부담하는 직원이 영업비밀 또는 영업상 주요 자산을 경쟁업체 유출 또는 자기 이익 이용 목적으로 무단 반출하면 반출 시 업무상배임죄가 기수에 이른다. 적법 반출 자료도 퇴사 시 반환·폐기 의무를 위반하면 퇴사 시 기수가 될 수 있다. 다만 특별한 사정이 없는 한 퇴사 후에는 타인의 사무처리자 지위가 없어 별도 업무상배임이 성립하지 않는다.

**출처 원문**
> 경쟁업체에 유출하거나 스스로의 이익을 위하여 이용할 목적으로 무단으로 반출하였다면 유출 또는 반출 시에 업무상배임죄의 기수가 된다.

**지적**: 카드 명제와 출처 규범이 어긋난다는 지적입니다.

<details><summary>상세</summary>

Three of the four linked candidates—art355.element.omission-legal-duty, art355.causal-link.omission-new-loss-risk, and art355.standard.omission-attempt-risk-concretized—are absent from the supplied validated candidate batches. Only art355.causal-link-auditor-reporting-omission-new-harm is bounded, and that candidate alone does not provenance-link every general clause in the merged card.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec3_3

### 35. `art355_sec3_3.legal_disposition`

**카드 명제**
> 횡령의 법률적 처분행위는 청약 또는 계약 체결로 충분하며, 매각·증여·교환 등이 전형적 처분행위이다.

**출처 원문**
> 법률적 처분행위는 청약 또는 계약의 체결로서 충분하고

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

청약 또는 계약 체결로 충분하다는 명제는 법률적 처분행위 해당 여부에 관한 것이며, 원문은 기수 성립 여부가 견해에 따라 달라진다고 명시한다. 현재 proposition은 그 유보를 누락하여 청약 또는 계약 체결만으로 횡령죄가 기수에 이른다는 의미로 읽힐 수 있고, 별도로 보존된 기수시기 경쟁 견해 및 부동산 등기 기준과 충돌한다.

</details>

**판정 (넓음 / 괜찮음):** 

### 36. `art355_sec3_3.private_school_tuition_restricted_use`

**카드 명제**
> 용도가 엄격히 제한된 사립학교 교비회계 자금을 제한된 용도 외 목적으로 사용하면, 개인적 목적이 아니거나 결과적으로 위탁자를 위한 면이 있어도 불법영득의사가 실현되어 횡령죄가 성립한다.

**출처 원문**
> 이와 같이 용도가 엄격히 제한된 자금을 위탁받아 집행하 면서 그 제한된 용도 이외의 목적으로 자금을 사용하는 것은 그 사용이 개인적인 목 적에서 비롯된 경우는 물론 결과적으로 자금을 위탁한 본인을 위하는 면이 있더라도 그 사용행위 자체로서 불법영득의 의사를 실현한 것이 되어 횡령죄가 성립

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

원문 판례 기준은 회사 운영자나 대표 등이 내부 절차를 거쳐 고문을 위촉하고 급여를 지급한 경우를 전제로 한다. 현재 proposition은 그 전제를 누락하여 내부 절차를 거치지 않은 지급에도 동일한 엄격한 인정 기준이 적용되는 것으로 범위를 확장한다.

</details>

**판정 (넓음 / 괜찮음):** 

### 37. `art355_sec3_3.company_funds_private_use`

**카드 명제**
> 대표이사가 적법한 절차 없이 회사 자금을 회사 업무와 무관한 사적 용도로 임의 지출하면, 주주총회 또는 이사회 결의 여부와 관계없이 횡령죄를 면할 수 없다.

**출처 원문**
> 주식회사의 자금을 회사의 업무와 무관하게 주주나 대표이사의 개인 채무 변제 등과 같은 사적인 용도로 임의 지출하 였다면 그 지출에 관하여 주주총회나 이사회의 결의가 있었는지 여부와는 관계없이 횡령죄의 죄책을 면할 수 없다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

현재 proposition은 `적법한 절차 없이`를 횡령 성립 조건처럼 배치하지만, 인용된 판례 명제는 회사 업무와 무관한 사적 용도의 임의 지출이면 주주총회나 이사회 결의 유무와 관계없이 죄책을 면할 수 없다는 것이다. 따라서 절차 흠결은 이 명제의 필수조건이 아니다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec5_2

### 38. `art355_sec5_2.real_estate_transfer_exception`

**카드 명제**
> 판례는 부동산 양도계약의 소유권이전의무에 대하여 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무성을 인정한다.

**출처 원문**
> 결국 판례는 부동산 양도계약에 따른 소유권이전의무에 대해서만 중도금 지급 관행 등 거래 현실의 특수성을 고려하여 예외적으로 타인의 사무로 인정하고

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

부동산 양도계약의 소유권이전의무를 예외적으로 타인의 사무로 인정한다고만 서술하여 적용 단계를 넓혔다. 제공된 판례 설명은 계약금만 지급된 단계가 아니라 중도금 지급 등 계약이 본격적으로 이행되고 계약이 취소·해제되지 않은 단계에서 매도인의 지위를 인정한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec5_3

### 39. `art355_sec5_3.performance_to_first_purchaser`

**카드 명제**
> 매도인이 부동산을 이중매도하였더라도 제1매수인에게 소유권이전의무를 이행한 행위는 제2매수인에 대한 관계에서 배임죄가 성립하지 않는다.

**출처 원문**
> 매도인이 부동산을 이중으로 매도하고 제1매수인에게 소유권이전의무를 이행하 였다고 하여 제2매수인에 대한 관계에서 배임죄가 성립하는 것은 아니다.

**지적**: 카드가 출처에 없는 내용까지 담았다는 지적입니다.

<details><summary>상세</summary>

The card references candidate_id "art355.exception.performance-to-first-purchaser", but no candidate with that ID appears in the supplied validated_candidates. Although the card proposition is supported by the commentary, its asserted candidate-stage provenance is invalid.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec7_10

### 40. `art355_sec7_10.cooperative_election_occupational_breach_concurrence`

**카드 명제**
> 중소기업협동조합법상 선거운동을 위한 재산상 이익 제공죄와 조합 법인카드 결제로 조합에 손해를 가한 업무상배임죄는 구성요건·행위태양·보호법익이 달라 실체적 경합 관계에 있다.

**출처 원문**
> 각 범죄의 구성 요건 및 행위의 태양과 보호법익을 달리하고 있어 상상적 경합 관계에 있다고 볼 수 없고, 실체적 경합 관계에 있다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

출처는 중소기업중앙회장 선거에서 특정 후보자를 당선시킬 목적으로 선거인들에게 숙식을 제공하고 그 비용을 조합 법인카드로 결제한 사안의 판단이다. 현재 명제는 이를 중소기업협동조합법상 선거운동을 위한 재산상 이익 제공죄 전반과 법인카드 결제에 의한 업무상배임죄 전반에 적용되는 범죄 관계로 표현하여 사안 범위를 넓힌다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec7_12

### 41. `art355_sec7_12.speculative_transaction_company_property_assessment`

**카드 명제**
> 회사 임원 등의 회사재산 처분이 투기행위를 하기 위한 것인지는 회사 목적·주된 영업, 자산규모, 거래 경위, 목적물 특성, 시세변동 폭, 거래 방법·기간·규모·횟수, 자금 조성경위, 거래관행 및 경제상황을 종합 고려하여 판단한다.

**출처 원문**
> 당해 회사의 목적과 주된 영업내용, 회사의 자산 규모, 당해 거래에 이

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

출처는 제반 사정을 종합적으로 고려한다고 규정하지만, ‘어느 하나의 부재만으로 투기행위가 부정되는 것은 아니다’라는 별도의 명제를 명시하지 않는다. 종합평가 방식에서 추론할 수 있더라도 출처에 직접 제시된 법리처럼 단정하면 범위가 넓어진다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec7_8

### 42. `art355_sec7_8.loan_kickback_internal_distribution`

**카드 명제**
> 금융기관 임직원과 대출 상대방이 부실대출을 공모하고 대출금 일부를 되돌려 받기로 하여 약정 금품을 수수한 경우, 그 수수는 업무상배임 공동정범 사이의 내부적 이익분배에 불과하여 별도의 특정경제범죄가중처벌등에관한법률위반(수재등)죄는 성립하지 않는다.

**출처 원문**
> 금융기관의 임직원이 대출 상대방과 공모하여 임무에 위배하여 대출 상대방에

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

명제는 원문이 전제한 금융기관 임직원의 임무위배 및 담보부동산의 담보가치를 훨씬 초과하는 대출이라는 구체적 조건을 단순한 '부실대출'로 축약하여, 별도 수재등죄가 성립하지 않는 범위를 원문보다 넓힌다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec7_9

### 43. `art355_sec7_9.imaginary_concurrence_fine`

**카드 명제**
> 상상적 경합에서 가장 중한 죄의 형으로 처벌하되 다른 법조의 최하한보다 가볍게 처단할 수 없으며, 업무상배임죄와 영업비밀 국외누설죄의 상상적 경합에서는 중한 업무상배임죄의 형으로 처벌하면서 영업비밀보호법상 벌금형을 병과할 수 있다.

**출처 원문**
> 형법 제40조가 규정하는 1개의 행위가 수개의 죄에 해당하는 경우에 ‘가장 중한 죄에 정한 형으로 처벌한다.’라고 함은, 수개의 죄명 중 가장 중한 형을 규정한 법조에 의하여 처단한다는 취지와 함께 다른 법조의 최하한의 형보다 가볍게 처단할 수 없다는 취지 즉, 각 법조의 상한과 하한을 모두 중한 형의 범위 내에

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

벌금형 병과 가능성을 현재의 일반적인 '영업비밀보호법상' 결론처럼 표현했으나, 출처는 구 부정경쟁방지 및 영업비밀보호에 관한 법률이 해당 범죄에 징역형과 벌금형을 병과할 수 있도록 규정했다는 조건 아래의 판례 결론이다. 역사적 법률과 병과 규정이라는 조건이 누락되어 명제가 출처보다 넓다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec8

### 44. `art355_sec8.transaction_counterparty_illegality`

**카드 명제**
> 정범의 행위가 배임행위임을 알고 거래에 임하여 외견상 방조행위로 평가될 수 있는 행위가 있더라도, 범죄를 구성할 정도의 위법성이 없다고 볼 수 있다.

**출처 원문**
> 비록 정범의 행위가 배임행위에 해당한다는 점을 알고 거래에 임하였다는 사정이 있어 외견상 방조행위로 평가될 수 있는 행위

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

위법성 부정 결론을 해당 거래상대방의 관여가 교사 또는 배임 전 과정 관여 등 적극 가담의 정도에 이르지 않고, 계약이 반사회적 법률행위로 무효가 되지 않으며, 법질서 전체의 관점에서 사회적 상당성을 갖춘 경우라는 원문의 누적 조건 없이 제시하였다. 현재 문언은 배임 인식과 외견상 방조행위만 있으면 일반적으로 위법성이 부정될 수 있는 것처럼 범위를 넓힌다.

</details>

**판정 (넓음 / 괜찮음):** 

### 45. `art355_sec8.transaction_counterparty_illegality`

**카드 명제**
> 정범의 행위가 배임행위임을 알고 거래에 임하여 외견상 방조행위로 평가될 수 있는 행위가 있더라도, 범죄를 구성할 정도의 위법성이 없다고 볼 수 있다.

**출처 원문**
> 비록 정범의 행위가 배임행위에 해당한다는 점을 알고 거래에 임하였다는 사정이 있어 외견상 방조행위로 평가될 수 있는 행위

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

review_notes는 위법성 부정의 구체적 판단조건이 제공된 범위에서 확정되지 않는다고 하지만, 참조된 commentary chunk의 전체 문언에는 적극 가담의 정도, 반사회적 법률행위로서의 무효 여부, 사회적 상당성이 명시되어 있다. 추가적인 사실평가가 필요하다는 점과 출처에 조건이 없다는 점을 구별해야 한다.

</details>

**판정 (넓음 / 괜찮음):** 

### 46. `art355_sec8.insufficient_collusion_loan_request`

**카드 명제**
> 배임행위에 편승한 것으로 볼 수 있어도 배임행위의 전 과정에 관여하거나 적극 가담한 것으로 볼 수 없다면, 배임행위의 공동정범으로 처벌할 수 없다.

**출처 원문**
> 피고인 甲이 피고인 ⼄ 등의 배임행위에 편승했다고 볼 수는 있어도 배임행위의 전 과정에 관여하거나 이에 적극 가담한 것으로는 볼 수 없

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

특정 부실대출 사안에서 대출 부탁, 친분에 따른 실행, 대가 제공·약속 정황의 부재 등을 종합하여 적극 가담을 부정한 판례 사례를, 단순히 편승은 있으나 전 과정 관여나 적극 가담이 없으면 언제나 공동정범 처벌이 불가능하다는 일반 규범으로 바꾸었다. 이는 연결된 candidate의 사실적 한정도 제거한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec8_2

### 47. `art355_sec8_2.unspecified_embezzlement_indictment_invalidity`

**카드 명제**
> 약 2년간 회사 자금을 수시로 수표 인출하여 합계 금원을 횡령하였다는 공소사실이 시기·종기, 범행횟수, 자금 및 횡령 명목을 특정하지 않아 포괄일죄 여부와 방어권 행사가 불가능한 경우, 공소사실 불특정으로 공소제기 절차가 무효가 된다.

**출처 원문**
> 사실은 기본적 사실관계가 동일하여 포괄일죄에 해당하는지 여부조차 판단하기 어려

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

출처는 특정 공소사실에 관하여 공소기각 판단을 정당하다고 본 사례를 보고한다. 현재 proposition은 사건의 결론을 일반적인 조건부 무효 규칙처럼 표현하여 사례별 결함의 정도와 방어권 판단을 넘어 일반화될 수 있다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec9

### 48. `art355_sec9.victim_change_defense_rights`

**카드 명제**
> 배임 공소사실의 피해자를 공소장 기재와 달리 다른 상속인들로 인정하면 피고인의 방어방법이 달라져 실질적 불이익 우려가 있는 경우, 법원이 직권으로 피해자를 변경하여 배임죄 성립을 인정할 필요가 없다.

**출처 원문**
> 공소사실과 달리 B의 상속인들을 피해자로 인정할 경우 그에 대응할 피

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

판례가 직권 피해자 변경을 하지 않은 원심을 정당하다고 본 근거에는 방어권 행사의 실질적 불이익 우려뿐 아니라, 직권으로 실제 피해자를 인정하지 않은 것이 현저하게 정의와 형평에 반하지 않는다는 판단도 포함된다. 현재 명제는 후자의 조건을 누락하여, 방어상 불이익 우려만 있으면 일반적으로 직권 변경의 필요가 없다는 더 넓은 규범으로 표현한다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art355 / sec9_1

### 49. `art355_sec9_1.protectable_entrustment_denied`

**카드 명제**
> 판례는 횡령죄로 보호할 만한 가치가 있는 위탁관계가 인정되지 않는 경우 횡령죄가 성립하지 않는다고 판단하고 있다.

**출처 원문**
> 판례는 횡 령죄로 보호할 만한 가치가 있는 위탁관계가 인정되지 않는다고 보아 횡령죄가 성립되지 않는다고 판단하고 있다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

원문과 후보는 사기피해금이 송금된 계좌명의인과 접근매체 양수인 사이의 특정 관계에서 보호할 가치 있는 위탁관계를 부정한 판례를 다루지만, 카드 명제는 관계와 사실 맥락을 삭제하여 보호할 가치 있는 위탁관계가 없는 모든 경우에 관한 일반 명제로 확대되었다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art357 / sec3_2

### 50. `art357_sec3_2.tv_producer_stock_opportunity`

**카드 명제**
> 방송국 가요프로그램 담당 프로듀서가 연예기획사 운영자로부터 소속 연예인 출연 또는 뮤직비디오 방영 청탁을 받고 시세차익이 예상되는 주식 매수기회를 제공받아 주식을 매수한 경우 배임수재죄가 성립한다.

**출처 원문**
> 방송국 예능담당 프로듀서가 연예기획사 운영자로부터 상당한 시세차 익이 예상되는 주식의 매수기회를 제공받음으로써 그가 제작하는 예능프로그램 등에 소속 연예인을 출연시키거나 뮤직비디오를 방영해 달라는 청탁을 받고 주식을 매수 함으로써 재산상 이익을 취득하였다면 배임수재죄가 성립한다.

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

성립 결론을 서술하는 출처 사례의 행위자는 방송국 예능담당 프로듀서인데, 카드가 이를 가요프로그램 담당 프로듀서로 바꾸었다. 같은 문단의 가요프로그램 담당 프로듀서에 관한 문장은 타인의 사무를 처리하는 자의 지위를 설명할 뿐, 해당 주식 매수 사례의 행위자 표시가 아니다.

</details>

**판정 (넓음 / 괜찮음):** 

### 51. `art357_sec3_2.implied_improper_solicitation_inference`

**카드 명제**
> 부정한 청탁의 존재가 명시적으로 증명되지 않아도, 통상 범위를 넘는 금액 수수와 객관적 사실관계 또는 정황에 비추어 묵시적 부정한 청탁을 추인할 수 있다.

**출처 원문**
> 부정한 청탁의 존재가 명시적으로 증명되지 않았더라 도 통상적인 범위를 넘어서는 금액 수수가 있었던 사안에서 객관적으로 인정되 는 사실관계나 정황에 비추어 묵시적으로 부정한 청탁이 있었다고 추인하여 본 죄를 인정한 경우가 많다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

출처는 재판실무에서 일정한 사안에 관해 묵시적 청탁을 추인하여 범죄를 인정한 경우가 많다는 경향을 보고한다. 카드는 이를 일반적으로 추인할 수 있다는 규범적 허용 기준으로 바꾸어 출처의 기술적·경향적 한계를 제거하였다.

</details>

**판정 (넓음 / 괜찮음):** 

### 52. `art357_sec3_2.self_rights_protection_not_improper`

**카드 명제**
> 자신의 권리를 확보하기 위한 행위는 부정한 청탁에 해당하지 않을 수 있다.

**출처 원문**
> 피고인이 자기의 권리를 확보하기 위한 행위로서 부정한 청탁이 라고 할 수 없다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

출처의 결론은 자신의 소유라고 믿은 부동산의 처분, 손해배상 우려, 종중 가처분의 부당성 지적과 비용 지급 및 취하라는 구체적 사안에 관한 것이다. 카드는 이를 모든 자기 권리 확보 행위에 적용될 수 있는 일반 명제로 확장하였다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art366 / sec1

### 53. `art366.object_manageable_energy`

**카드 명제**
> 재물손괴등죄의 범행객체는 유체물인 재물이며, 순수한 유체물이 아니더라도 관리 가능한 동력은 범행객체에 포함된다.

**출처 원문**
> 범행객체 가 유체물에 한정되는 재물죄로서 강도, 사기, 공갈 등 이욕죄와 구별된다. 순수 한 유체물이 아니지만 ‘관리 가능한 동력’도 범행객체에 포함된다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

명제는 재물손괴등죄의 범행객체 전체가 유체물인 재물인 것처럼 표현한다. 그러나 같은 출처는 타인의 재물뿐 아니라 문서와 전자기록 등 특수매체기록도 조항의 객체로 제시한다. 유체물 한정 설명은 재물이라는 객체 유형의 성격에 관한 설명으로 한정되어야 하며, 죄 전체의 객체 범위를 배타적으로 규정하는 명제로 확장할 수 없다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art366 / sec3_1

### 54. `art366.ownerless_property_exclusion`

**카드 명제**
> 현재 누구의 소유에도 속하지 않는 무주물은 타인성이 인정되지 않아 재물손괴등죄의 범행객체가 될 수 없다.

**출처 원문**
> 현재 어느 누구의 소유에도 속하지 않는 물건 인 무주물인 경우도 마찬가지로 타인성이 인정될 수 없으므로 범행객체가 될 수 없다.

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

무주물은 범행객체가 될 수 없다는 명제를 보존하면서도, 출처가 바로 이어서 민법상 무주의 부동산은 국가 소유로 의제되어 예외적으로 타인성이 인정될 수 있다고 명시한 예외를 카드에 반영하지 않았다. 현재 카드는 관련 예외 없이 무주물 전반에 적용되는 규칙으로 읽힐 수 있다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art366 / sec4_1

### 55. `art366_sec4_1.intent_destruction_protective_measures`

**카드 명제**
> 임대인이 가재도구의 비를 막고 타인의 개봉을 방지하려는 조치를 하였다면, 그 조치에 과실이 있어 침수로 효용이 해하여졌더라도 손괴의 고의는 인정되기 어렵다.

**출처 원문**
> 그 조치가 미흡한 점에 과실이 있음은 별론으로 하

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

보고된 사례의 행위자는 임대인이 아니라 임대인의 모인 피고인이고, 가재도구를 옥상으로 옮긴 뒤 구체적인 방수·개봉방지 조치를 한 사실관계이다. 현재 명제는 행위자를 임대인으로 바꾸고 구체적 사례를 일반적인 조건문처럼 확장한다.

</details>

**판정 (넓음 / 괜찮음):** 

### 56. `art366_sec4_1.intent_concealment_relocation`

**카드 명제**
> 영업방해를 위해 타인이 설치하려는 철조망을 원래 위치에서 떨어진 자기 토지로 옮긴 경우, 재물은닉의 범의는 인정되지 않는다.

**출처 원문**
> 재물은닉의 범의가 있다고 할 수 없다고 한 사례

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

원문은 타인이 영업을 방해하기 위해 설치하려던 철조망을 영업자인 피고인이 자기 소유의 다른 토지로 옮긴 사례이다. 현재 명제의 '영업방해를 위해 … 옮긴 경우'는 피고인의 이동 목적이 영업방해였던 것으로 읽혀 행위 목적의 주체와 의미를 뒤바꾼다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art366 / sec5_3

### 57. `art366_sec5_3.emergency_evacuation_proportionality`

**카드 명제**
> 긴급피난의 상당성 판단에서는 피난행위가 위난에 처한 법익을 보호하기 위한 유일한 수단이어야 하고, 피해자에게 가장 경미한 손해를 주는 방법을 택해야 하며, 보전되는 이익이 침해되는 이익보다 우월해야 한다.

**출처 원문**
> 피난행위는 위난에 처한 법익을 보호하기 위한 유일한 수단

**지적**: 카드 명제와 출처 규범이 어긋난다는 지적입니다.

<details><summary>상세</summary>

연결된 후보는 상당성 요건으로 사회윤리·법질서 전체의 정신에 적합한 수단일 것을 포함하고, 전체 commentary chunk도 이를 명시한다. 그러나 카드는 유일수단성·최소침해·이익우월성만 남겨 후보의 네 번째 요건을 누락했으며, review_notes의 '제공된 인용문이 뒷받침하지 않는 추가 요소'라는 설명도 전체 bounded source와 맞지 않는다.

</details>

**판정 (넓음 / 괜찮음):** 

### 58. `art366_sec5_3.chainsaw_dog_injury_not_emergency_or_excess`

**카드 명제**
> 다른 방법으로 개들을 쫓아 자신의 개를 보호할 수 있었고 현재의 공격 위험도 인정되지 않는 경우, 기계톱으로 상대방 개를 상해한 행위는 긴급피난 또는 과잉피난에 해당하지 않는다.

**출처 원문**
> 피난행위의 상당

**지적**: 출처가 이 명제를 지지하지 않는다는 지적입니다.

<details><summary>상세</summary>

'현재의 공격 위험도 인정되지 않는 경우'라는 표현은 공격 위험 일반이 부정된 것처럼 확장한다. 출처가 명시하는 사실은 피해자의 개들이 당시 피고인을 공격하지 않았고 평소 공격적 성향이 있다고 볼 자료도 없었다는 점이다. 반면 피고인은 그 개들이 자신의 진돗개를 공격하려 한다고 생각한 사안이므로, 출처는 진돗개에 대한 현재 공격 위험까지 포괄적으로 부정하지 않는다.

</details>

**판정 (넓음 / 괜찮음):** 


---

## art366 / sec6

### 59. `art366_sec6.mistake_of_law_exception`

**카드 명제**
> 손괴행위가 법에 따라 죄가 되지 않는다고 오인하였고 그 오인에 정당한 사유가 있으면 법률의 착오로 책임이 조각된다.

**출처 원문**
> 자신의 손괴행위가 법에 의하여 죄가 되지 아니하는 것으로 오인한 경우 그 오

**지적**: 출처는 특정 사실관계에 한정해 말하는데 카드가 일반 법리처럼 넓혔다는 지적입니다.

<details><summary>상세</summary>

예외 명제는 단순한 법률의 부지가 아니라, 일반적으로 범죄가 되는 행위가 자신의 특수한 경우에는 법령상 허용된다고 오인한 경우여야 한다는 명시적 제한을 누락한다. 현재 문구는 죄가 되지 않는다는 모든 정당한 오인을 포괄하는 것처럼 읽혀 출전보다 넓다.

</details>

**판정 (넓음 / 괜찮음):** 

