# KBL causal reasoning → Call 2

Source: `lbox/kbl`, file `reasoning/kbl_causal_reasoning_qa_v0.1.json`, pinned by the prepare script.
The adapter evaluates only the authored `legal_element.result_causation` atomic proposition.

`cause` and `effect` are serialized with the benchmark's charged facts, defendant claim, and
accepted evidence into one external evidence carrier. The gold letter is converted from the
meaning of the selected A/B option, so option-order reversal cannot change label semantics.
No offense selection, participation, completion, planner, Scallop execution, or final liability
judgment is performed.

Primary metrics are accuracy, macro F1 over labels observed in gold, and UNKNOWN rate. For KBL,
the gold labels are TRUE/FALSE, so this macro F1 is the ordinary binary macro F1 and has a ceiling
of 1.0. Fixed three-way macro F1 over TRUE/FALSE/UNKNOWN is retained only as a diagnostic, along
with per-class precision/recall/F1, coverage, selective accuracy, and the full confusion matrix.
