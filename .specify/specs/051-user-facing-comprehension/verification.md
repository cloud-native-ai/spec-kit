# Verification Log — 051-user-facing-comprehension

<!--
  Populated by /speckit.implement. This run was **MVP-scoped by user decision**:
  Phase 1 Setup + Phase 2 US1 only (13 of 63 tasks). US2–US5 were not started, so most
  Success Criteria are honestly `deferred` rather than `pass`. The feature's lifecycle
  status therefore stays **Planned** — the Pre-Status-Flip Gate was NOT run, because no
  status flip is being claimed.
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=925badb60860fdbbb8a5fade24cecb01627fbc6f
baseline_commit_superseded=710c7179fc1896d85b5d7d0c8ad52719af18f558
baseline_commit_superseded_reason=orphaned by the rebase onto gitlab/master; not an ancestor of HEAD, so it no longer delimits this feature's changes
baseline_date=2026-09-18
baseline_branch=051-user-facing-comprehension

# Baseline counters. Source of record: notes/pre-change-measurements.md (frozen by T001),
# which carries the command that re-derives each value.
baseline_truth_doc_count=0
baseline_guideline_count=11
baseline_template_h2_count=17
baseline_live_h2_count=18
baseline_template_guideline_pointers=7
baseline_live_guideline_pointers=8
baseline_reader_baseline_declaration_files=3
baseline_rule_sources_carrying_pointer=0
baseline_gate_total=23
baseline_gate_destructive=13
baseline_gate_governance_kept=10
baseline_contract_failed=26
baseline_blocking_patterns=17

# -- /speckit.implement results --

implementation_date=2026-09-18
post_change_commit=8e634e8cae263c923abc514e2181df89addd9c35
post_change_commit_note=82d95e2d (the US1 phase commit as originally recorded) was orphaned by the rebase; the rebased tree is what every gate below was re-validated against
post_change_scope=Phase 1 Setup (T001-T002) + Phase 2 US1 (T003-T013); 13 of 63 tasks closed
post_change_tasks_closed=13
post_change_tasks_open=50

post_change_truth_doc_count=1
post_change_guideline_count=12
post_change_template_h2_count=18
post_change_live_h2_count=19
post_change_template_guideline_pointers=8
post_change_live_guideline_pointers=9
post_change_reader_baseline_declaration_files=2
post_change_rule_sources_carrying_pointer=0
post_change_gate_total=23
post_change_gate_destructive=13
post_change_gate_governance_kept=10
post_change_contract_failed=26
post_change_blocking_patterns=17

# -- Success Criteria evaluation --

SC-001_status=deferred
SC-001_value=0 of 13 governance-kept gates carry a wording obligation
SC-001_note=The judging instrument now exists (truth doc's mechanical criteria, T006), but the gate-prompt side is US2 (T017 et al.) and the criterion is a human sampling review, not a file assertion.
SC-001_deferred_reason=US2 not in this run's MVP scope; unblocks when T017-T020 land and a reviewer outside this feature samples the 13 prompts.

SC-002_status=deferred
SC-002_value=rule defined (blacklist item 1); surface-wide count not yet measured or enforced
SC-002_note=The blacklist now makes "engine call form where a user-facing path exists" decidable, which is the precondition this SC needed; convergence of the 38 dispersed wordings is US4/US5.
SC-002_deferred_reason=Enforcement lands with the US2/US4/US5 pointer and convergence tasks; measuring now would report a not-yet-done state as a failure.

SC-003_status=partial
SC-003_value=truth docs = 1 (target 1) PASS; content-form restatements = not yet converged (target 0)
SC-003_note=First half measured and guarded: discipline-doc C-1/C-2/C-3 green, `ls -1 shared/guidelines/*.md | wc -l` = 12 with exactly one comprehension doc, C-3 drill-proven to catch a rename. Second half is DoD-9's single-source scan, which US5 builds.
SC-003_deferred_reason=Restatement count stays above 0 until T041/T046/T047 converge the dispersed wordings.

SC-004_status=deferred
SC-004_value=0 of 8 rule-source files carry the pointer (GATE-8 measured 0/8)
SC-004_note=The 11-class closed enumeration and the canonical one-line pointer form both landed in T006, so the eight insertions are now mechanical; the insertions themselves are US2/US4/US5.
SC-004_deferred_reason=T017/T025/T036/T041-T049 not in MVP scope.

SC-005_status=deferred
SC-005_value=charter double-landing not attempted; plan-template.md diff = 0 lines (constraint already satisfied)
SC-005_note=US3 owns both landing points. The zero-change constraint on plan-template.md is already guarded and green (gate-neutrality C-6, GATE-4 = 0).
SC-005_deferred_reason=US3 not in MVP scope.

SC-006_status=deferred
SC-006_value=judging instrument present; agreement rate not measured (needs >=20 messages, 2 independent reviewers)
SC-006_note=discipline-doc C-13 green: five verdict questions across both sides plus the explicit goal form ("two independent reviewers reach the same verdict"). The double-blind test itself is a human activity.
SC-006_deferred_reason=Requires two reviewers who did not build this feature; cannot be self-administered by the implementing agent.

SC-007_status=deferred
SC-007_value=suggestion-line form unchanged (proactive-trigger.md untouched this run)
SC-007_note=The truth doc's ceiling section now references the single-line constraint by path rather than restating it (C-12 green), which is what prevents inflation. The before/after length sampling belongs with T042.
SC-007_deferred_reason=US4 not in MVP scope; no sampling baseline captured yet.

SC-008_status=pass
SC-008_value=2 of 2 named conflicts adjudicated; blank surface classes = 0
SC-008_note=discipline-doc C-12 green. Both of FR-012's named conflicts (floor vs single-line, floor vs summary-first) carry an explicit adjudication order, plus the accepted cost of clarify R2-Q3=A written as "length unbounded, form bounded".

SC-009_status=partial
SC-009_value=3 of 5 surfaces guarded (truth doc, mirror parity, ambient section); 2 pending (charter template, charter command MUST-include list)
SC-009_note=34 contract cases in CI. Neutrality assertions are green on both new surfaces (discipline-doc C-15, ambient C-9). The single-source-scan assertion is DoD-9's, built by US5. Mutation-style effectiveness was demonstrated for two clauses rather than assumed — see notes/red-first-evidence.md.

SC-010_status=partial
SC-010_value=0 leaks in the truth doc and the ambient section; charter template and command template not yet touched by this feature
SC-010_note=discipline-doc C-15 and ambient-section C-9 both green against the four forbidden proprietary names. The remaining two surfaces are US3's; they cannot leak from this feature until US3 edits them.

SC-011_status=pass
SC-011_value=0 new executables outside tests/contract (GATE-9 = 0)
SC-011_note=gate-neutrality C-5 green in CI. No jargon lint, wording scorer, maturity report generator, tracking ledger or registry was added; the two new .py files are both under tests/contract/.

SC-012_status=pass
SC-012_value=gate total 23 -> 23; destructive 13 -> 13; governance_kept 10 -> 10; violations 0
SC-012_note=Achieved by design avoidance, not by widening the scanner: every line added inside scan scope was verified to carry 0 BLOCKING_RE hits. gate-neutrality C-2/C-3 green; `git diff BASE_SHA -- scripts/python/scan-confirmation-gates.py` = 0 files (GATE-4).

SC-013_status=deferred
SC-013_value=0 assertions cover confirmation-gates.md:68's wording rule
SC-013_note=US2 generalizes that clause and adds its assertion.
SC-013_deferred_reason=US2 not in MVP scope.

SC-014_status=deferred
SC-014_value=naming half landed; promotion not done; independent blacklist copies still 1
SC-014_note=discipline-doc C-10 is green on the naming requirement — blacklist item 2 declares reporting-playbook.md §1.7 as its instance source, states the promotion obligation and forbids a second independent blacklist. The enumeration itself is promoted by T046.
SC-014_deferred_reason=US5 (T046) not in MVP scope; C-10's full green point is T054 by design.

SC-015_status=deferred
SC-015_value=watchlist guard not built; 0 principles under double-landing guard
SC-015_note=US3 owns both the charter principle and the command's MUST-include entry, plus the mutation-tested watchlist guard.
SC-015_deferred_reason=US3 not in MVP scope.

SC-016_status=deferred
SC-016_value=0 regressions to date (full contract suite failure set == frozen baseline, comm -13 empty)
SC-016_note=The precondition holds — the regression net is empty after US1 — but the two moves it protects have not happened yet, so there is nothing to regress.
SC-016_deferred_reason=The moves are T041 (US4) and T046 (US5).

SC-017_status=pass
SC-017_value=dangling pointers = 0 across both instruction surfaces; 9 runtime targets resolve, 0 MISSING
SC-017_note=ambient-section C-11 traverses every guideline pointer on BOTH surfaces (template 8, live 9) and asserts both halves of the delivery window — the runtime copy a reader opens and the framework source that regenerates it. C-11(b)'s remainder assertion accounts for the 3 guidelines no surface points at, in subset semantics, so deleting any pointer fails while adding one does not. The ambient section carries FR-038's recovery route in normative prose. Drill-proven in both directions: removing either copy makes the clause fail naming the missing half. The drill also found that the first version of C-11 checked only the source tree and therefore passed with the runtime copy absent — recorded in notes/red-first-evidence.md's amendment.

SC-018_status=partial
SC-018_value=1 global baseline + 2 registered class overrides = 3 (<= 3) under by-class counting; 4 under by-line counting
SC-018_note=discipline-doc C-13 (exactly one global baseline), C-18(a) (2 registered override entries, cap 2) and C-18(b) (no unregistered declaration anywhere in shared/, templates/, skills/) are all green. C-18(b) went green because the unregistered fourth site — templates/commands/requirements.md:82, class 7's command-side twin — was converged by deleting the copy, per the one-source-of-truth repair direction. That copy had already drifted from its owner (it dropped "not developers"), which is the concrete cost the SC exists to prevent. **Open user decision, not silently resolved**: SC-018 says "at most 2 class-level override 处", and 处 reads as either class or line. By class (what C-18(a) implements) the total is 3 and the criterion holds; by line it is 4 and SC-018 would need restating as <=4 or the two requirements-guidelines.md sites merged. Recorded in the 第五轮 Clarifications block as awaiting user confirmation.
SC-018_deferred_reason=Not deferred work but an unresolved counting interpretation; the implemented reading is documented and the alternative's cost is stated rather than absorbed.

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=No task was marked [~]. The 50 open rows are US2-US5 scope that this MVP run deliberately did not start, not deferrals of attempted work.

# -- Completion Gate re-validation (run against the current tree, not trusted from task state) --

gate_1_new_test_failures_vs_baseline=PASS (comm -13 empty; 26 == frozen baseline)
gate_2_mirror_and_regen=PASS (scoped --check EXIT=0; regen --check EXIT=0; no new drift lines vs the frozen set)
gate_3_gate_budget=PASS (total 23, violations 0)
gate_4_scanner_and_zero_change_surfaces=PASS (0 files changed vs BASE_SHA)
gate_5_unclosed_task_rows=FAIL (50 open — US2-US5, outside this run's user-chosen MVP scope)
gate_6_validate_tasks=PASS (exit 0, 0 errors, 0 warnings)
gate_7_sc_status_lines=PASS (18 lines, this file)
gate_2_3_no_new_drift_lines=PASS (drift baseline re-frozen: the draw-diagram lines were committed and mirrored away; the single remaining line is upstream's own improve-skills source/mirror divergence, verified present in gitlab/master itself)
gate_8_eight_pointer_files=FAIL (0 of 8 — the insertions are US2/US4/US5 tasks)
gate_9_no_new_executables=PASS (0)

# 6 of 9 gates pass. The 3 that fail are the two that measure unbuilt US2-US5 work
# (GATE-5, GATE-8) and nothing else. GATE-7 passes only because this file now exists.
# The feature is NOT complete and its status MUST NOT flip to Implemented.

# -- Free-form notes --

post_change_rebase=rebased onto gitlab/master (925badb6) then master fast-forwarded; 33 commits on top of upstream, 0 behind; 6 index.json conflicts resolved by feedback-utils.py --action reindex, 1 additive table-row conflict in skills/draw-diagram/SKILL.md resolved by keeping both rows; nothing pushed
notes=MVP scope (Setup + US1) chosen by the user, phase-boundary commits pre-authorized. Three defects were found in this feature's own tests during the run, each by executing a check rather than reading it: (1) gate-neutrality C-5/C-6 derived their change set from `git diff <sha>`, which cannot see untracked files — so during the run window they were blind to exactly the artifacts they exist to judge; (2) discipline-doc C-3 compared two literals inside the test file and never looked at the tree, leaving "MUST NOT be renamed" unasserted; (3) ambient-section C-11 resolved pointers against the framework source tree while readers resolve the runtime copy, so SC-017's own drill passed with the runtime copy deleted. All three were the same shape as the two blind checks found earlier in this feature (the `--stat` piping form and `git diff HEAD`'s vacuity under CI): a command that returns an answer which is not about the proposition. C-3 and C-11 were then drill-proven able to fail. One cross-phase dependency was mis-sequenced in tasks.md — C-18(b)'s green point is T012 (US1) but the work that satisfies it was assigned to T043 (US5) — so the affected half of T043 was front-loaded into US1 and both rows were annotated with the falsified premise rather than the schedule being quietly overridden. Left untouched and reported as an upstream deviation: skills/draw-diagram/SKILL.md (modified) and skills/draw-diagram/references/self-deploy-render-service.md (untracked) belong to another unit's in-flight work and are the sole cause of 3 of the 26 baseline failures.
