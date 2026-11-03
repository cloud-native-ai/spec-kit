# Verification Log — 081-acceptance-hardening

baseline_commit=cb841d90
baseline_date=2026-11-02
baseline_branch=081-acceptance-hardening
implementation_date=2026-11-03
post_change_commit=4c07fdc9

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-004_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=blocked
SC-001_value=the implement call site blocks the negative fixture (`block`, exit 1, `zero-final-path-pass`); the review and driver call sites are 081c/081d work
SC-001_note=1 of 3 required call sites is wired; SC-001 is a final-path criterion and therefore not pass
SC-001_blocked_at=SC-001 requires all three call sites; 081a wires only the implement site
SC-001_reduced_measurement=implement call-site contract test and the negative fixture both return block/exit 1 with `zero-final-path-pass`; T016 wiring green
SC-001_reduced_measurement_run=yes
SC-001_why_reduced_insufficient=one call site cannot prove the review or driver closure/merge gates
SC-001_unblock=wire the review site in 081c and the driver closure/merge site in 081d, then rerun all three sites

SC-002_status=partial
SC-002_value=positive fixture accepts with exit 0 and `smoke-mutation` blocks with `status-claims-implemented-but-blocked`; the `Implemented → Ready for Review` leg needs 081c
SC-002_note=the positive path and the smoke hard condition are green; the fourth gate condition is a review-stage measurement
SC-002_blocked_at=the `Implemented → Ready for Review` half is only measurable at the review site (081c)
SC-002_reduced_measurement=positive fixture `accept` + smoke hard condition + `smoke-mutation` block
SC-002_reduced_measurement_run=yes
SC-002_why_reduced_insufficient=the positive path alone does not exercise the review-site fourth condition
SC-002_unblock=081c review-site wiring, then rerun the positive/negative pair at that site

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

SC-005_status=partial
SC-005_value=ownership and premises are first-class: the four findings fire 4/4 through both producers (`pre-analyze-check.py` and `closure-acceptance-check.py`); `RS-004`'s three `in-scope` duties are 3/3 (`FR-005` defined, quoted by this file's T011 row at line level, joint-acceptance row present); both plan tables account for 8/8 records — 7 settled in this slice + 1 disclosed `inherited-later`
SC-005_note=the two plan tables' records: the three zero-row sources carry no disposition because there is no row to dispose; the five extracted `partial` rows are all dispositioned; of the three `inherited` rows, IB-006 (`task:T005+test:tests/contract/test_acceptance_premises.py`) and IB-007 (`task:T012+test:tests/contract/test_acceptance_premises.py`) resolve in this slice, and IB-004 reads `inherited-later` (`test:tests/contract/test_acceptance_review_composition.py`, `Carrier slice=081c`). `inherited-later` is a disclosed legal reading — neither an undisposed blocker nor a resolved carrier — which is why this row reads `partial`, not `pass`
SC-005_blocked_at=IB-004's carrier module belongs to slice 081c, so its carrier measurement cannot resolve in 081b
SC-005_reduced_measurement=`tests/contract/test_acceptance_premises.py` (the slice's single carrier) asserts the four findings through both producers, the three `in-scope` duties at their own stages, the carrier forms/eligibility/slice readings, the join key and the extraction; the 081b test set also keeps the frozen guards green
SC-005_reduced_measurement_run=yes
SC-005_why_reduced_insufficient=the inherited carrier for IB-004 is the 081c review-composition module; a supporting criterion naming that carrier cannot claim the full carrier measurement in 081b
SC-005_unblock=081c lands `tests/contract/test_acceptance_review_composition.py` and completes IB-004's carrier to `task:<T-ID>+test:<path>`; 081d re-reads the row at line closure

SC-006_status=deferred
SC-006_value=the review composition and ARC contract exists; the four-segment review and artifact/implementation measurements are 081c
SC-006_note=this criterion is supporting; its carrier is 081c
SC-006_blocked_at=081c owns `review-feature-quality`, the review command rewrite and the ARC measurement
SC-006_reduced_measurement=review-composition contract and the owner doc § Review Composition
SC-006_reduced_measurement_run=yes
SC-006_why_reduced_insufficient=no real review run exists to measure the four segments and the three counts
SC-006_unblock=081c lands the review composition and runs a review

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
final_path_source=test-evidence/closure-verdict-081b.json (byte-identical copy of `.specify/.tmp/081b-closure-verdict.json`, produced by `closure-acceptance-check.py --json-out`; this block is a copy, not a second count)

# -- Notes --

notes=081a closed as Blocked (SC-001's three call sites were 1/3); 081b lands US2 and keeps the feature Blocked — SC-005 is now `partial` with the 7/8-settled + 1-`inherited-later` reading, and the verdict remains `zero-final-path-pass` because no closure call site was added. The slice's close record is `test-evidence/tasks-081b-slice-tests.txt` (89 passed, exit 0); the feature-level baseline comparison is 081d's. Historical 081a note: the slice is deliberately Blocked: SC-001's three call sites are 1/3 in 081a, and the feature must not be called Implemented. The baseline is the plan-stage capture (39 failed / 6970 passed / 7 skipped); the closure-repair head runs are recorded under test-evidence/closure-repair-run*.txt. The one mirror-parity delta is attributed to test-order isolation in the existing 078 suite, not to a 081 behaviour change; it is disclosed here rather than counted as a pass. Provenance of the acceptance summary above: it is copied from test-evidence/closure-verdict.json (produced by the checker with --json-out), never recomputed by hand. Two notes carry the disclosures this log only points at: notes/driver-completions.md (the three stages the loop driver completed after the stage subagent hit its 120-turn limit, with commits) and notes/known-items.md (F12 recorded, F13 fixed, F14 deferred to 081d).
