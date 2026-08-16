# KBL causal reasoning → Call 2

Source: `lbox/kbl`, file `reasoning/kbl_causal_reasoning_qa_v0.1.json`, pinned by the prepare script.
The adapter evaluates only the authored `legal_element.result_causation` atomic proposition.

`cause` and `effect` are serialized with the benchmark's charged facts, defendant claim, and
accepted evidence into one external evidence carrier. The gold letter is converted from the
meaning of the selected A/B option, so option-order reversal cannot change label semantics.
No offense selection, participation, completion, planner, Scallop execution, or final liability
judgment is performed.

Metrics are accuracy, fixed three-way macro F1, observed-gold macro F1, per-class
precision/recall/F1, UNKNOWN rate, coverage, selective accuracy, and the full
TRUE/FALSE/UNKNOWN confusion matrix.
