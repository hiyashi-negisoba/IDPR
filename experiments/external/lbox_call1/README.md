# LBOX Open → Call 1

Source: `lbox/lbox_open`, config `statute_classification_plus`, pinned by the prepare script.
All `train`, `valid`, and `test` rows form the source pool because this is a frozen zero-shot
external evaluation; no benchmark split is used for training or tuning.

The adapter exposes only `facts` plus the fixed generic routing question to production Call 1.
`casename` and `statutes` are scorer-side normalization fields and never enter the model payload.
A case enters the main evaluation only when every gold statute resolves uniquely to a directly
authored offense in the current production registry. The manifest, not the raw source count, is
the authority for the final evaluation N.

Primary metrics are raw DefinitionRef survival, closure DefinitionRef survival, closure recovery,
and case-level full hit. Micro precision/recall/F1 are secondary because external statute labels
need not enumerate every legally plausible candidate exposed by the high-recall router.
