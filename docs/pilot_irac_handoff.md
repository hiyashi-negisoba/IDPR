# Pilot rubric 기준 Scallop → Call 3 IRAC 인계

## 결론

Call 3에 rubric이나 모범답을 넣지 않는다. 대신 pilot의 36개 rubric이 채점하는
답안 구조를 호스트 계약으로 보존한다.

    이슈별 Call 2 판정
      → Scallop의 요건·조각·미수·흡수·경합 결과
      → 사람이 읽는 semantic directive
      → 죄명별 IRAC section

원시 `offense_established`, `element_unaddressed` 튜플은 모델에 노출하지 않는다.
대신 `성립 후 흡수`, `미수 검토`, `요건 미확정` 같은 작성 지시로 번역한다.

## Rubric에서 보존할 것

- 죄명별 쟁점 제시와 검토 순서
- 일반법리와 판례상 하위 판단기준
- 제공된 사실·반대사실의 구체적 포섭과 개별 소결
- 실행의 착수·중지미수·결과적 가중범의 기수 여부
- 간접정범·공범과 특별관계·흡수·상상적/실체적 경합
- 개별 죄명 검토 뒤의 최종 죄수 결론

이 구조를 각 죄명 section의 하나의 `Issue / Rule / Application / Conclusion`으로 명시한다.
내부적으로는 issue별 analysis를 유지하되, 최종 마크다운에서는 Issue와 Rule을 죄명 단위로
모으고 Application 안에서 각 쟁점의 포섭과 소결을 전개한다. 쟁점별로 완전한 IRAC를
반복하지 않아 사례형 답안의 자연스러운 흐름을 보존한다.
Call 3 모델은 여기까지의 산문만 담당하고, 죄명별 Conclusion과 종합 Conclusion은
symbolic directive로부터 호스트가 생성한다. 따라서 작성 모듈이 미수 검토를 미수 성립으로
앞당기거나 미확정 죄명을 확정할 수 없다.
`unknown`은 사실을 만들어 채우지 않고 부족한 사실과 결론의 한계를 쓴다.
핵심 요건에 `element_unaddressed`가 있으면 원시 `offense_established`가 함께 있어도
Call 3 결론은 `undetermined`가 우선한다.

## Call 3에서 버릴 것

- rubric 문언·배점·채점 키워드와 모범답 결론
- 원시 Scallop relation 배열과 내부 ID를 답안 문장에 노출하는 것
- 사안과 무관한 조문의 세부 판례 목록
- 입력에 없는 판례번호·학설·사실의 보충

## Pilot에서 실제로 살릴 카드

초기 4개 조문(제297·301·298·319조)의 14개 구성요건 issue를 우선 판정한다.
그 후 살아 있는 죄명에 한해 stage·participation·concurrence·guard issue를 두 번째
패스에서 판정한다. 초기 실험에서는 16개 후속 issue가 선택됐다.

작성 시에는 status를 바꾸지 않고 초기 요건과 법적으로 유의미한 후속 issue에서
관련 detail을 최대 2장씩 검색한다. 초기 요건 unknown은 답안에 반드시 남기지만,
근거 없는 deferred 공범·죄수·guard unknown은 산문에서 뺈다. 이로써 피해자를 도구로
삼은 강제추행 간접정범, 미수에
그친 강간의 폭행으로 상해가 발생한 경우, 상해의 인과관계·예견가능성,
공동주택 공용부의 객체성과 평온 침해 기준을 IRAC에 보존한다.

## 현재 corpus gap

- 제276조 체포죄가 51개 조문 corpus에 없다.
- 성폭력처벌법상 `주거침입강간치상`이 독립된 죄명·조문 노드로 없다.
  현재는 제297·301·319조를 조합해 구성요건을 일부 보존하지만 특별법상
  결합범의 최종 죄명과 특별관계를 심볼릭하게 완전 표현하지 못한다.
- 중지미수의 자의성·중지행위, 간접정범의 일반론은 형법총칙 corpus 공백이다.
  각칙 카드가 해당 사안을 일부 보완하지만 보편적 Rule IR을 대체하지는 못한다.

따라서 pilot은 IRAC 배선과 이슈 선택을 검증하기에는 유효하지만, corpus 밖의
죄명까지 포함한 36개 rubric 전항목 재현 실험으로 보고하면 안 된다.
