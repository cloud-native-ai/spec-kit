# Verification Log — 081-acceptance-hardening

baseline_commit=cb841d90
baseline_date=2026-11-02
baseline_branch=081-acceptance-hardening
implementation_date=2026-11-03
post_change_commit=dc72c941

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-004_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=blocked
SC-001_value=the implement and review call sites are wired (2/3): the implement site blocks the negative fixture, and the review site names `closure-acceptance-check.py` and treats `block` as a non-pass; the driver closure/merge site is 081d work
SC-001_note=1 of 3 required call sites is wired; SC-001 is a final-path criterion and therefore not pass
SC-001_blocked_at=SC-001 requires all three call sites; 081c wires the review site, leaving the driver closure/merge site
SC-001_reduced_measurement=implement call-site contract test and the negative fixture both return block/exit 1 with `zero-final-path-pass`; T016 wiring green
SC-001_reduced_measurement_run=yes
SC-001_why_reduced_insufficient=one call site cannot prove the review or driver closure/merge gates
SC-001_unblock=wire the driver closure/merge site in 081d, then rerun all three sites

SC-002_status=partial
SC-002_value=the composition is wired and the negative pair is measured: `review-implemented-blocked` blocks (`zero-final-path-pass`, `F-ACCEPTANCE`); the positive R4R half is NOT measured, because SC-002 requires **all three** named readings — (i) implement site accepting `positive`, (ii) a **recorded review-composition run** over `review-implemented-clean` (four segments executed on that fixture, its `review.md` or an equivalent four-segment transcript, the ARC record, command / exit code / evidence path), (iii) `smoke-mutation` refusing with `status-claims-implemented-but-blocked` — and (ii) is the one that is absent. Measured today: (i) and (iii) hold at the fixture boundary; (ii) does not exist as a run
SC-002_note=the bar is the recorded four-segment composition run, not the checker payload: a checker invocation on a fixture is the *input* the artifact segment consumes, and it is recorded below as the reduced measurement exactly because it is not the bar. 081d's T004 owns producing the reading; if it cannot be produced, this row stays `partial` and the feature stays `Blocked` (tasks.md § Status consequence)
SC-002_blocked_at=no recorded review-composition run over `review-implemented-clean`: no four-segment transcript (or fixture-local `review.md`) plus ARC record exists with its command, exit code and evidence path
SC-002_reduced_measurement=`review-implemented-clean` checker invocation (accept/exit 0/all four conditions true at the payload level) + `review-implemented-blocked` block/exit 1/`zero-final-path-pass` + 081c T004 leg (i) + 081a's implement-site and `smoke-mutation` readings
SC-002_reduced_measurement_run=yes
SC-002_why_reduced_insufficient=a checker invocation on a fixture is not the review site's four-segment run: it judges the fourth condition without executing the process, artifact, implementation and code segments over the fixture, so it carries none of their findings and no produced `review.md`. Re-taking the same invocation cannot upgrade this row
SC-002_unblock=run the composed `/speckit.review` over `review-implemented-clean` so all four segments execute on that fixture, and record the four-segment transcript (or the fixture-local `review.md`) with the ARC record, the command, the exit code and the evidence path; then SC-002 can pass — that same recorded run is the produced `review.md` SC-006's unblock names, so one run serves both readings

SC-003_status=partial
SC-003_value=feature-details owner states four `Blocked` transitions and the fourth Ready-for-Review condition; `manage-features` (T024, deferred) and the feature-index-template vocabulary are 081d work
SC-003_note=1 of 3 vocabulary owners is in place (feature-details only); `manage-features` and `feature-index-template` are 081d. Known window, owned by 081d: the registry row reads `Blocked` while `manage-features` does not yet admit it — un-deferring T024 here was blocked by WC-14 (`tests/contract/test_expression_compatibility.py` is frozen), so the window is recorded, not papered over
SC-003_blocked_at=two of the three vocabulary owners are deferred: `manage-features` (T024) and feature-index-template are 081d
SC-003_reduced_measurement=feature-details owner contract test (14 passed) and the state-machine contract test
SC-003_reduced_measurement_run=yes
SC-003_why_reduced_insufficient=one owner cannot prove that the registry tool and the index template admit `Blocked`
SC-003_unblock=081d adds `Blocked` to `manage-features`' vocabulary and to the feature-index template's closed vocabulary

SC-004_status=pass
SC-004_value=the six-value vocabulary, five `SC-NNN_` ladder fields, illegal-row trigger and the exactly-one smoke record are asserted by the state-machine contract test
SC-004_note=the ladder-mutation fixture is asserted by the checker contract test

SC-005_status=pass
SC-005_value=ownership and premises are first-class: the four findings fire 4/4 through both producers; `RS-004`'s three `in-scope` duties are 3/3; both plan tables account for 8/8 records with **all three inherited carriers resolving in the live 081c `tasks.md`** — IB-004 → `task:T004+test:tests/contract/test_acceptance_review_composition.py`, IB-006 → `task:T012+test:tests/contract/test_acceptance_premises.py`, IB-007 → `task:T012+test:tests/contract/test_acceptance_premises.py`; no `inherited-later` remains
SC-005_note=081b's dated reading was 7/8 settled + 1 `inherited-later`; 081c completed IB-004's carrier and re-pointed IB-006 to the live T012, so the closure payload now reports zero `inherited-blocker-undisposed` rows (T012 evidence) and the carrier reading is complete
SC-005_blocked_at=
SC-005_reduced_measurement=`tests/contract/test_acceptance_premises.py` 28 passed + zero `inherited-blocker-undisposed` in the 081c closure payload + the 081c guard suite 211 passed
SC-005_reduced_measurement_run=yes
SC-005_why_reduced_insufficient=
SC-005_unblock=

SC-006_status=partial
SC-006_value=the composition is structurally measurable and measured: four segment headings in the fixed order, four report slots, five fields per segment, the seven-key `final_path` copy (7/7) and the four-unit census; a real review run's `review.md` has not been produced
SC-006_note=the structural half is asserted by `tests/contract/test_acceptance_review_composition.py` (32 tests) and the guard suite (211 passed); the run half is review-stage evidence
SC-006_blocked_at=no real review run has produced a `review.md`
SC-006_reduced_measurement=T004 legs (a)–(k) + the fixture-level ARC payloads + the guard suite
SC-006_reduced_measurement_run=yes
SC-006_why_reduced_insufficient=structure is not a run: the segments and the copied record are asserted on templates, not on a produced `review.md`
SC-006_unblock=run `/speckit.review` on `review-implemented-clean` and measure the produced `review.md`

SC-007_status=deferred
SC-007_value=the `--audit-existing` surface exists; the zero-write audit over existing features is 081d
SC-007_note=this criterion is supporting; its carrier is 081d
SC-007_blocked_at=081d owns the audit mode and its zero-write test
SC-007_reduced_measurement=the CLI surface exposes `--audit-existing` and returns an explicit not-implemented input error rather than a fabricated verdict
SC-007_reduced_measurement_run=yes
SC-007_why_reduced_insufficient=the zero-write report over real features has not been produced
SC-007_unblock=081d implements the audit mode and its zero-write test

SC-008_status=partial
SC-008_value=the smoke record exists and was run twice with exit 0/0; the final `081d` claim over the final tree is still open
SC-008_note=the smoke command covers `specify init`, the positive/negative checker and `regen-command-copies.py --check`
SC-008_blocked_at=the final claim is over the 081d tree, not the 081a tree
SC-008_reduced_measurement=two identical exit-0 smoke runs on 081a; `smoke-081.txt` records all three sub-checks
SC-008_reduced_measurement_run=yes
SC-008_why_reduced_insufficient=later slices edit the same sources and must rerun the smoke on the final tree
SC-008_unblock=081d reruns the smoke on the final tree and records the triple

SC-009_status=partial
SC-009_value=mirror/regen `--check` exit 0; five frozen-pin guards pass; final post-review-fix full-suite 39 failed / 7025 passed / 7 skipped with `head − baseline` empty; the coverage lane is `uncovered` (17 clauses beyond the frozen baseline) and the schema-ownership guard is 081d work
SC-009_note=the set-level full-suite invariant is now clean; the remaining gaps are the coverage lane and the 081d schema-ownership guard
SC-009_blocked_at=coverage lane status `uncovered`; `tests/contract/test_acceptance_schema_ownership.py` is 081d work
SC-009_reduced_measurement=clean full-suite id-level diff: head 39 = baseline 39, 0 new, 0 fixed; five frozen-pin guards pass; mirror/regen 0
SC-009_reduced_measurement_run=yes
SC-009_why_reduced_insufficient=the coverage lane and the schema-ownership guard are not measured in 081a
SC-009_unblock=081d lands the schema-ownership guard; the coverage lane verdict is tracked as a separate gap (T023)

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=Slice 081b has no `[~]` task row. 081a's T024 (`manage-features` vocabulary owner) was archived with `tasks-081a.md` and remains 081d's; it is not a row of this slice and MUST NOT be extracted as a live locator.

# -- Acceptance summary (copied from the checker; never recomputed here) --

final_path_pass=0
final_path_blocked=1
final_path_deferred=0
final_path_partial=1
final_path_fail=0
final_path_unknown=0
final_path_total=2
acceptance_verdict=block
final_path_source=test-evidence/closure-verdict-081c.json (byte-identical copy of `.specify/.tmp/081c-closure-verdict.json`, produced by `closure-acceptance-check.py --json-out`; this block is a copy, not a second count)

# -- Notes --

notes=081c lands US3 (review composition + ARC): 17/17 tasks; the review call site is wired, so SC-001 is blocked at 2/3 call sites (driver closure/merge is 081d's) and SC-002 remains partial because no real review command run over `review-implemented-clean` was recorded. SC-005 is now `pass` (all three inherited carriers resolve); SC-006 is `partial` (structure measured, no produced `review.md`). Close set `214 passed` exit 0 (`test-evidence/tasks-081c-slice-tests.txt`); smoke 0/0; mirrors/regen 0. The feature remains Blocked. Historical 081a/081b notes are preserved in `notes/red-first-evidence.md` and `notes/red-first-evidence-081b.md`. The baseline is the plan-stage capture (39 failed / 6970 passed / 7 skipped); the closure-repair head runs are recorded under test-evidence/closure-repair-run*.txt. The one mirror-parity delta is attributed to test-order isolation in the existing 078 suite, not to a 081 behaviour change; it is disclosed here rather than counted as a pass. Provenance of the acceptance summary above: it is copied from test-evidence/closure-verdict-081c.json (byte-identical to `.specify/.tmp/081c-closure-verdict.json`, produced by the checker with --json-out), never recomputed by hand. This slice's known items are F15–F24 in `notes/known-items-081c.md`; no driver-completion record exists for 081c (081a's record is `notes/driver-completions.md`, kept as history).
