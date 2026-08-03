직전 출력은 호스트의 증거·구조 admission 계약을 통과하지 못했다. 아래 host_errors와
previous_output을 참고하되, case_text만 사실의 출처로 사용하여 완전한 FactGraph JSON을
처음부터 다시 출력하라.

- 모든 source_quote는 case_text에 존재하는 정확한 연속 부분문자열이어야 한다.
- acts, results, roles, relations, holdings, transfers가 참조하는 모든 entity와 act 순번은
  새 출력 내부에 실제로 존재해야 한다.
- 설문 범위를 벗어난 행위·쟁점은 만들지 말고, 원문에 근거 없는 항목은 삭제한다.
- host_errors를 설명하지 말고 JSON 객체만 출력한다.
