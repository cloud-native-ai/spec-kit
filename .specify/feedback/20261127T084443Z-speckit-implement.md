---
id: "20261127T084443Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "r20261127T071500Z-111a"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-11-27T08:44:43Z"
summary: "Implement P1 (T001–T010 + T007A) for 111-general-best-practices: the docs-only five-document module under shared/best-practices (manifest with the closed four-category table, three placeholder owner f"
---

## Review
Implement P1 (T001–T010 + T007A) for 111-general-best-practices: the docs-only five-document module under shared/best-practices (manifest with the closed four-category table, three placeholder owner files, the Git clone seed entry), a red-first six-leg contract guard executed only through scripts/bash/run-tests.sh, the T007A mirror fan-out, and the manifest-owned 逐步积累机制 section (marker+stem in --review, identity convention, promotion procedure and generality criterion, 来源 shape, knowledge-promotion pointer, red line). US1 guard selection 4/4 green and US2 leg (d) green, both rc 0 with 0 failed names; red-first captured as 6 errors on the missing module before any content landed; entry baseline frozen with 223 pre-existing names. Run Determination reads artifact_correctness regressed by exactly one name — test_mirror_file_byte_identical[shared/best-practices/README.md->.specify/shared/best-practices/README.md] — which is the documented A-24 transient (T009 edits the source after T007A; T012/T013 converge the mirror in P2), not a defect of this package artifacts. Token consumption not evaluated (source unavailable); elapsed 415 s measured, not comparable (first record for this unit in this line). In-passing repairs: two evidence headers aligned to measured mtimes; raw *.log captures are git-ignored and referenced as local captures. T011–T019 remain open for P2; no push.

## Optimization Points
- A planned-pending red (a known transient scheduled to converge in a later task row) has no representation in run-determination: declaring it honestly forces artifact_correctness=regressed and trigger_feedback=true, which a stage checkpoint can misread as a package defect; a planned_pending value/red-source would keep the record honest without the false regression signal.
- The runner echoes a caller -k expression unquoted in its mode line, which reads like shell splitting even though the ARGS array preserves the single argument; quoting it in the echo would remove the ambiguity.
