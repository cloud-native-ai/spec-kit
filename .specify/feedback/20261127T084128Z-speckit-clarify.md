---
id: "20261127T084128Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "r20261127T081500Z-112a"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "112-decision-batch-panel"
feature_id: "112"
partial: false
created: "2026-11-27T08:41:28Z"
summary: "Clarify stage of 112-decision-batch-panel (run r20261127T081500Z-112a), mode A on requirements.md: five unattended adjudications integrated as A-21…A-25 plus a new Clarifications session (Q rows 11→16"
---

## Review
Clarify stage of 112-decision-batch-panel (run r20261127T081500Z-112a), mode A on requirements.md: five unattended adjudications integrated as A-21…A-25 plus a new Clarifications session (Q rows 11→16). Outcomes: (1) candidacy vs qualification split — incomplete blocks stay candidates and present as incomplete, only carrier-level unreadability refuses; (2) deterministic register-row-to-block linkage via origin token plus literal identity comparison; (3) class gate narrowed — declared ai-autonomous excluded, unknown class incomplete (class-missing) and never settled, class conflict excluded with named disclosure; (4) record preconditions — drift revalidation, batch id minted only after checks, rejected attempts and replies write nothing, explicit authorization level; (5) response definition plus verbatim reply layer in the batch record. Also corrected the open-row baseline from the hand-listed 8 to the predicate-derived 17. Validator green before and after (408→437 lines, 55 definition rows, 15 strings, 0/0); workspace guard clean pre/post commit. Artifact commit 8b7591f63. No register/spine edits, no push, no main-tree writes.

## Optimization Points
- 1. token-efficiency — the requirements-stage open-row baseline was a hand-typed list (8) while the recorded predicate yields 17; counts in a closed-set claim must be predicate-derived, never transcribed. [fast-fail] 2. process — FR-011/A-13 said class-missing candidates are excluded while A-16/FR-010 said block-less rows present as incomplete; the contradiction was resolved at clarify, but a requirements-stage cross-check of the class gate against the incomplete rule would have caught it earlier. 3. process — US3 said objections are preserved verbatim while FR-033 allowed key points only; clarify now records a verbatim reply block in the batch record and keeps rationale as summary.
