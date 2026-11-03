# Verification Log — 081-acceptance-hardening

baseline_commit=cb841d90
baseline_date=2026-11-02
baseline_branch=081-acceptance-hardening
implementation_date=2026-11-03
post_change_commit=8ce0f006

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

SC-005_status=deferred
SC-005_value=the runtime-stack table and the two plan tables exist; the in-scope/inherited carrier checks are 081b
SC-005_note=this criterion is supporting; its measurement carrier is `tests/contract/test_acceptance_premises.py` (081b)
SC-005_blocked_at=081b owns the premise/inherited tests and the four deterministic findings
SC-005_reduced_measurement=the runtime-stack table and the two plan tables were read by the checker; the owner doc sections exist
SC-005_reduced_measurement_run=yes
SC-005_why_reduced_insufficient=the carrier-existence and in-scope-obligation assertions are not in 081a
SC-005_unblock=081b lands `test_acceptance_premises.py` and the four findings

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
SC-009_value=mirror/regen `--check` exit 0; five frozen-pin guards pass; clean full-suite 39 failed / 7023 passed / 7 skipped with `head − baseline` empty; the coverage lane is `uncovered` (17 clauses beyond the frozen baseline) and the schema-ownership guard is 081d work
SC-009_note=the set-level full-suite invariant is now clean; the remaining gaps are the coverage lane and the 081d schema-ownership guard
SC-009_blocked_at=coverage lane status `uncovered`; `tests/contract/test_acceptance_schema_ownership.py` is 081d work
SC-009_reduced_measurement=clean full-suite id-level diff: head 39 = baseline 39, 0 new, 0 fixed; five frozen-pin guards pass; mirror/regen 0
SC-009_reduced_measurement_run=yes
SC-009_why_reduced_insufficient=the coverage lane and the schema-ownership guard are not measured in 081a
SC-009_unblock=081d lands the schema-ownership guard; the coverage lane verdict is tracked as a separate gap (T023)

# -- Deferred tasks --

deferred_tasks=T024
deferred_reason_summary=T024 (the `manage-features` vocabulary owner) is deferred to 081d because WC-14 freezes the C-5 verification suite.

# -- Acceptance summary (copied from the checker; never recomputed here) --

final_path_pass=0
final_path_blocked=1
final_path_deferred=0
final_path_partial=1
final_path_fail=0
final_path_unknown=0
final_path_total=2
acceptance_verdict=block
final_path_source=test-evidence/closure-verdict.json (produced by `closure-acceptance-check.py --json-out`; this block is a copy, not a second count)

# -- Notes --

notes=The slice is deliberately Blocked: SC-001's three call sites are 1/3 in 081a, and the feature must not be called Implemented. The baseline is the plan-stage capture (39 failed / 6970 passed / 7 skipped); the closure-repair head runs are recorded under test-evidence/closure-repair-run*.txt. The one mirror-parity delta is attributed to test-order isolation in the existing 078 suite, not to a 081 behaviour change; it is disclosed here rather than counted as a pass. Provenance of the acceptance summary above: it is copied from test-evidence/closure-verdict.json (produced by the checker with --json-out), never recomputed by hand. Two notes carry the disclosures this log only points at: notes/driver-completions.md (the three stages the loop driver completed after the stage subagent hit its 120-turn limit, with commits) and notes/known-items.md (F12 recorded, F13 fixed, F14 deferred to 081d).
