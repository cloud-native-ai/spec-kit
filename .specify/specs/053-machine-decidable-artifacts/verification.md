# Verification Log — 053-machine-decidable-artifacts

<!--
  Populated by /speckit.implement at T049 (2026-10-04). Shape owned by
  .specify/templates/verification-log-template.md, including the SC status vocabulary
  {pass | fail | partial | deferred | unknown} — no row below narrows it.
  Every number in this file was re-derived by a command during this run; none is quoted
  from an upstream artifact (DoD-9's re-freeze rule).
-->

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=ad190d46de960efd70e61a4719a16561a89b7e9d
baseline_date=2026-10-02
baseline_branch=053-machine-decidable-artifacts

baseline_failed_test_names=65
baseline_failed_names_md5=02177c0e6e5961c880f73d932007df92
baseline_passed_tests=2927
baseline_gate_total=23
baseline_gate_violations=0
baseline_blocking_patterns=17
baseline_mirror_diff_scripts_python=1
baseline_mirror_diff_templates=2
baseline_mirror_diff_skills=30
baseline_mirror_diff_whole_tree=33
baseline_corpus_files_excl_053=110
baseline_corpus_clause_ids_excl_053=507
baseline_goal_utils_actions=9
baseline_goal_utils_exit_constants=4
baseline_validate_tasks_labels=6
baseline_green_claims_on_own_tasks=0
baseline_owner_doc_for_clause_syntax=absent
baseline_run_checks_action=absent
baseline_subject_reference_form=absent

# -- /speckit.implement results --

implementation_date=2026-10-04
post_change_commit=ec30d14f7d7dde719eea5f036d5e7edf790f3920

post_change_failed_test_names=65
post_change_passed_tests=3165
post_change_new_failures_vs_baseline=0
post_change_fixed_vs_baseline=0
post_change_gate_total=23
post_change_gate_violations=0
post_change_blocking_patterns=17
post_change_mirror_diff_scripts_python=1
post_change_mirror_diff_templates=2
post_change_mirror_diff_skills=30
post_change_mirror_diff_whole_tree=33
post_change_corpus_files_all=117
post_change_corpus_files_parsed=64
post_change_corpus_files_named_unparseable=53
post_change_corpus_clause_ids_all=689
post_change_corpus_clause_names_distinct=665
post_change_corpus_clause_ids_collapsed=24
post_change_goal_utils_actions=10
post_change_goal_utils_exit_constants=5
post_change_validate_tasks_labels=10
post_change_green_claims_on_own_tasks=182
post_change_own_contract_clauses=182
post_change_own_uncovered_clauses=0
post_change_coverage_baseline_names=483
post_change_uncovered_beyond_baseline=0
post_change_fr_universe=48
post_change_fr_uncovered=0
post_change_new_scripts=3
post_change_contract_suites=6
post_change_contract_tests_in_feature_suites=190

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=4/4 classes named exactly, zero cross-masking; 3 real specs exit 0; 5th label also sampled
SC-001_note=b1 delete FR-030 row -> exit 1 {id-contiguous}; b2 move SC-002 after SC-005 -> exit 1 {doc-order}; b3 [[STR-005]]->[[STR-999]] -> exit 1 {ref-resolvable}; b4 plant [NEEDS CLARIFICATION: probe] -> exit 1 {marker-count} (count reported 1); b5 double FR-001 row -> exit 1 {dup-id}; positive control (unmodified spec) exit 0; residue 0. Copies built in mktemp -d, never under .specify/specs/ (checker-form C-17). Evidence: notes/quickstart-run.md 场景 3.

SC-002_status=pass
SC-002_value=transitional awk blocks 0; "Until that validator ships" 0; validate-requirements.py mentioned 2x
SC-002_note=anti-vacuity companion present: the file is non-empty and its document-order-invariant subsection still exists, so "0 because removed" is distinguishable from "0 because the section was lost". The two tests that used to assert the copy's PRESENCE as their pass condition were rewritten in the same commit (D-9); the old assertion string "the interim extraction block is gone" now has 0 hits and "shares one implementation" 1. tests/contract/test_clarify_semantic_completeness.py -> 13 passed. Evidence: notes/quickstart-run.md 场景 2.

SC-003_status=pass
SC-003_value=both directions measured: consistent order 0 WARN; inverted order 1 WARN naming clause, both rows and both phases
SC-003_note=The operative condition is clause-ordinal inversion against the monotonic row order (C-12 as amended 2026-10-04); FR-017's prose under-determines it and only this reading satisfies both halves of C-12's criterion. A third sample pins that the comparison uses `order` and not the heading's phase number (## Phase 9 before ## Phase 2 still warns once). Evidence: notes/red-first-evidence.md T019/T020/T022 and notes/quickstart-run.md 场景 5.

SC-004_status=pass
SC-004_value=dangling exit 1; cross-phase-only exit 0; both collision classes exit 0; no third tier added
SC-004_note=Both dangling sub-cases sampled separately (contract file absent; file present but clause id absent, message names file and id) plus the md-none case, where a file that exists but declares no machine-decidable clause form is an ERROR rather than a silent pass. Existing tiers untouched: test_c5_exit_code_table's four original assertions are unchanged and two green tiers were appended.

SC-005_status=pass
SC-005_value=3-clause contract with 2 claims -> exactly 1 UNCOVERED line, STR-009 prefix; after the 3rd claim -> empty set, exit 0, companion non-zero
SC-005_note=Comparison is by sorted NAME list, never by count; the baseline file and the live list are both codepoint-sorted and the idiom runs under LC_ALL=C (measured defect: glibc collation ignores #/. so under en_US.UTF-8 comm reported 665 where the true delta was 182 — see notes/quickstart-run.md 场景 7). test_c24 runs comm with BOTH sides non-empty, because with an empty baseline comm echoes all of file 2 whatever the ordering and the first version of that test passed for that weak reason.

SC-006_status=pass
SC-006_value=scanned 117 files: parsed 64 + named-unparseable 53 == 117 (relational sentinel OK)
SC-006_note=The sentinel is relational, printed by the script every run, and no total is a literal in its source (asserted). Owner document exists, declares all six forms with their criterion regexes, is referenced by the accountant, and carries the canonical pointer to user-facing-comprehension.md in pointer form. Collapsibility measured both ways: default run prints 0 NAMED: lines, --list-named prints 53. Re-deriving this run also corrected the census owner's per-form id column (md-bold-closed 312 -> 311), which had contradicted its own corrected total. Evidence: notes/quickstart-run.md 场景 6.

SC-007_status=partial
SC-007_value=5 checks with all fields in one call; blocked run exit 5; missing slug exit 3 with checksum unchanged; but the "real team with a terminal goal" sample does not exist
SC-007_note=Marked partial honestly rather than pass. Three of the four legs are met on real or copied-real data: the field set is exact (C-9's set-equality), the REAL bound team with its genuinely `dropped` T-001 gives verdict target-terminal / blocked true / exit 5, and a nonexistent slug exits 3 with the byte checksum of .specify/goal/ + .specify/teams/ identical before and after (md5 dad5e7c5f584e0efe82e533b965d3485 both sides). The unmet leg is the criterion's own wording: it asks for a REAL team whose goal is already terminal, and the repository holds exactly one goal, whose status is `active` — so no real sample exists. Per C-28's contingency that tier was constructed in a throwaway copy of the real tree (status planted `achieved`) and recorded as constructed, never fabricated. Also corrected: the criterion says the two exit codes land in the blocked tier and the INPUT-ERROR tier, but a nonexistent slug is `not found` (3) in this binary — every existing action maps that condition to 3 via GoalNotFound, and C-17/C-19 forbid giving one condition two codes. The measured pair is 5 and 3. Unblocking a full pass: create or point at a real terminal-state goal; nothing in the implementation would change.

SC-008_status=pass
SC-008_value=exactly one check not-evaluated, the other four evaluated, array length still 5
SC-008_note=Two independent samples. (a) precondition failure: a local-form reference gives cross-goal no prefix to compare, so it reports not-evaluated while the other four are evaluated and the run exits 0 — the reported verdict is never `ok` for a check that did not run. (b) exception: monkeypatching one of the five check functions to raise leaves that one not-evaluated WITH its reason in `message` and the other four still reported, which is only possible because each check is its own guarded function rather than a branch in one short-circuiting call.

SC-009_status=pass
SC-009_value=derived set 7 -> 6 -> 7 members across a removal and an addition; enumeration text byte-identical throughout
SC-009_note=Demonstrated on a copy of the REAL skills tree (seven real draw-* skills), not a synthetic stand-in, with both criteria in one goal definition so the difference is visible in one output. After removing skills/draw-d3js the enumeration still asserted a member that no longer existed; after adding skills/draw-xyz it still omitted one that did — and it still said "Seven" both times. That is the churn the real goal's own ## History records having happened. Residue 0; the real tree was only read. Evidence: notes/quickstart-run.md 场景 10.

SC-010_status=pass
SC-010_value=1 goal definition scanned (>= 1 companion satisfied), name-level delta empty, no ERROR entries, real definition still validates
SC-010_note=The corpus really is one definition, so the anti-vacuity companion C-12 demands is asserted in the same test rather than assumed from an empty delta: at least one definition scanned, no parse ERROR, and the real goal's criteria derive an EMPTY subject set (state `absent`), which is what "pure enumeration parses exactly as before" means mechanically. Pre-existing goal suites re-run green in the same phase: test_goal_definition.py, tests/unit/test_goal_utils.py, test_goal_targets_engine.py (41 passed), test_goal_targets_check.py, test_goal_migration.py — 165 passed across the US5 batch.

SC-011_status=pass
SC-011_value=25 counter-samples over 21 newly added check units across 5 subjects; 4 mutation drills; residue 0 everywhere
SC-011_note=Per-subject pairs are in the GATE-9 section below, both sides derived by command in the same run. Every drill was restored by exact reverse substitution and re-verified (git diff empty, or a finally-block restore plus a re-run asserting the clean state). Drill residue measured by 场景 12's A/B/C probes: A=0, B=0, C positive control 1 then 0 — C is mandatory, because without it A's 0 is indistinguishable from a pattern that matches nothing.

SC-012_status=pass
SC-012_value=gate total 23 / violations 0; repo proper names in the three templates landing points 0/0/0; new test failures vs the frozen name-level baseline 0
SC-012_note=All three legs measured this run, per file rather than as a merged count. Integer headroom is still zero (cap 93 * 0.25 = 23.25, total 23), and the budget was met by wording design alone: the scanner, its mirror, both cap baselines and all three pin sites have an EMPTY git diff across the window, asserted by test_c7. The neutrality suite was mutation-drilled twice to prove it can go red (see below). Name-level comparison used LC_ALL=C comm -13 with both side counts printed.

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=none — all 49 tasks closed [X]; no row was deferred, so no exhaustive-requirement or unavailable-resource reason applies

# -- Free-form notes --

notes=Run spanned 2026-10-02..2026-10-04 across 8 phases and 6 phase-boundary commits (eac5f393 Phases 1-2, 14ac648b Phase 3, 26bd2feb deviation disclosure, 145b6944 Phase 4, 58cfa226 Phase 5, 4873f07d Phase 6, 1bc04378 Phase 7, ec30d14f Phase 8 T044-T048; this log lands in a following wrap-up commit). Consecutive gate rejections this run: 0 (the counter has run scope and resets each run; no gate was re-validated more than once as failing). GATE-4 read 1 open row at re-validation time because T049 was still open while this file was being written; it flips to 0 in the same edit that closes T049.

notes_gate_revalidation=All ten gates re-run against the current tree rather than trusted from the all-tasks-done state. GATE-1 baseline 65 / current 65 / new 0 / fixed 0. GATE-2 per pair by its own criterion — relative for the three pre-dirty pairs (scripts/python 1 DIFF = the recorded trigger-utils.py, templates 2, skills 30, whole tree 33, reconciling exactly) and absolute for shared/definitions, shared/guidelines, shared/constants, templates/tasks-template.md, templates/commands and the three skills/create-team files (all EXIT=0). GATE-3 regen --check EXIT=0. GATE-6 total 23 / violations 0 and `git diff ad190d46..HEAD -- scripts/python/scan-confirmation-gates.py` empty (0 lines). GATE-7 validate-tasks EXIT=0 with zero green-* findings, and 182 clauses / 182 claims / 182 distinct / 0 uncovered / 0 outside the corpus, all re-derived this run. GATE-8 relational sentinel holds (64 + 53 == 117), LC_ALL=C comm -13 delta 0 with empty stderr, paired companion claimed 182 > 0, FR lane 48/48 with 0 uncovered, status ok, exit 0. GATE-9 below. GATE-10 three real specs exit 0 each and five broken copies exit 1 each naming exactly its own label.

notes_gate9_per_subject=Both sides derived by command in the same run; the denominator is the NEW subset per subject (owner: data-model.md § 标签集 for the enumeration, each module's docstring for its full label set), never the full docstring count and never a typed total. (1) validate-requirements.py — units 5 (id-contiguous, doc-order, ref-resolvable, marker-count, dup-id from its docstring), counter-samples 5 (b1..b5 above), 5 >= 5 OK. (2) validate-tasks.py — units 4 NEW (green-dangling, green-cross-phase, green-clause-collision, green-path-divergence; its docstring holds 10 but 6 predate this feature, so the floor is 4), counter-samples 5 (one per label plus green-path-divergence's paired negative that C-27 owes), 5 >= 4 OK. (3) account-clause-coverage.py — units 4 (clause-uncovered, fr-uncovered, clause-unparsable, coverage-baseline-delta), counter-samples 6 (3-clause/2-claimed uncovered; delete one (FR-003) from a citation group; stream-style yaml named not guessed-zero; prose-only md named; baseline file removed -> non-zero naming the path; empty corpus -> exit 2 rather than a vacuous green), 6 >= 4 OK. (4) goal-utils.py run-checks — no label set, so keyed action+tier per SC-011: units 5 (exit tiers 0/2/3/4/5), counter-samples 5 (real bound team no target -> 0; reference matching neither grammar -> 2; nonexistent slug -> 3; goal status planted `finished` -> 4; real dropped Target -> 5 and a planted `achieved` goal -> 5 with no --target at all), plus the C-16 injection drill, 5 >= 5 OK. (5) goal-utils.py criterion-subject derivation — units 3 new verdict-vocabulary items (SUBJECT MISSING:, SUBJECT EMPTY:, SUBJECT CONFLICT:), counter-samples 4 (one per prefix plus the positive control that the same criterion without the brace enumeration validates clean at exit 0), 4 >= 3 OK. Totals: 21 units, 25 counter-samples, every subject at or above its floor, and no subject used its full docstring count as the denominator.

notes_mutation_drills=Four drills on guards of negative propositions, each restored by exact reverse substitution and re-verified. (a) Phase 8 neutrality, template leg: planted the literal `spec-kit` on templates/tasks-template.md's file-paths bullet -> 1 test red naming the file and line; restored with \cp -f from a backup, needle count 0 and the original line count 1, suite back to 20 passed, `git diff` EMPTY. (b) Phase 8 neutrality, budget leg: appended "wait for user confirmation before writing" to shared/definitions/contract-clause-definitions.md -> scanner total moved 23 to 24 and 3 tests red; restored the same way, scanner back to 23, suite 20 passed, `git diff` EMPTY. (c) Phase 5 FR lane: replaced one citation group's `(FR-003)` with prose in a fixture -> FR-003 appeared in fr-uncovered and the exit went non-zero; restored in a finally block and the same run re-asserted the clean state. (d) Phase 4 mention rule: an unclosed backtick run was pinned as the complement of the code-span exclusion, so "mentions are not claims" cannot be satisfied by a parser that never parses claims. Drill residue: 场景 12's A and B probes both 0, with the C positive control run first (1 then 0).

notes_premises_falsified=Seven premises inherited from upstream artifacts were falsified by execution and written back rather than worked around, which is the discipline this feature exists to make mechanical. (1) The clause-form census id total 508 -> 507, because only line-initial markers and table FIRST cells declare clauses; the census now derives id counts from clause_extract.py. (2) quickstart 场景 3's first broken copy deleted FR-023, which two other rows cite in prose, so it cross-masked ref-resolvable; switched to FR-030 (20 FR ids measured to have zero non-definition mentions). (3) T022's "exit 0 today is IMPOSSIBLE" — measured PASS with 0 errors and 0 warnings, and the row's reasoning was backwards; annotated on the row. (4) quickstart 场景 5 put counter-samples under <spec-dir>/notes/samples/, contradicting checker-form C-17; changed to mktemp -d. (5) FR-020 named only fenced blocks while FR-009's mention rule also covers inline code spans — T018's row had to NAME the tag to define it, and the first implementation parsed that mention as a claim on a file literally named `<contract>`, so this feature's own tasks.md failed its own GATE-7; FR-020, C-8 and a Session 2026-10-04 clarification were amended and both directions pinned. (6) The census's per-form id column summed to 508 while its own corrected total said 507; md-bold-closed is 311, not 312, and the row was struck through with the arithmetic shown. (7) E-4 defined `test_paths` as every write target while naming the field test_paths, and FR-018(b)/C-16/the origin prose all say test path — implementing E-4's wording produced 3 false green-path-divergence findings on this feature's own tasks.md the moment T045 landed its claims, because three rows append to one evidence log; narrowed to test paths with a positive control, and both artifacts corrected.

notes_escalations=Three items escalated rather than fixed in passing, each because the fix sits outside FR-022..FR-048's declared scope and would change something this feature does not own. A-7 (registered at analyze, disclosure added at US3): whether the FR lane gets its own cross-repository baseline; the implementation took the reading every downstream artifact already presupposes (FR universe = the one spec dir's requirements.md), which does not foreclose adding a cross-repo view later. A-8 (new, US3): the owner's yaml-openapi form names a clause by its HTTP method key, and 8 corpus files declare one method under several paths, so 24 of 689 extracted ids share a name and a name-set collapses them; the accountant now prints both numbers with the cause, the owner document records the non-uniqueness, and choosing a qualified id form is left to the syntax owner. A-9 (new, US4): goal-utils.py's shared parent parser does NOT make --json/--repo-root position-independent — argparse lets a subparser's default clobber the top-level value, so `--json list` silently emits the human form; fixing it would change flag precedence for all ten actions, so the false source comment and the false Tool-record line were corrected, C-11's falsified premise annotated, and both directions pinned. Two repo-state findings were also surfaced and deliberately not fixed: `.specify/teams/viz-skill-arena` declares goal_slug `visualization-skill-selection` whose definition does not exist (a dangling binding nothing enumerated before run-checks existed), and 18 of 44 specs carry pre-existing requirements-side debt that the new checker now reports — both recorded rather than repaired, since FR-027's philosophy is not to require retrofitting existing specs.

notes_deviation=One process deviation, disclosed and committed as its own record (26bd2feb): gate-check.py ran BEFORE the first edit for Phases 1 and 2 but only AFTER the edits for Phase 3. The retroactive verdict was `allow` for all six paths with EXIT=0, so nothing was written that the gate would have blocked; the ordering was still wrong. Phases 4-8 ran the gate before their first edit and each phase's verdict is echoed in that phase's first progress report (Phase 4: 5/5 allow; Phase 5: 6/6 allow; Phase 6: 11/11 allow; Phase 7: 8/8 allow; Phase 8: 4/4 allow).

notes_self_hosting=Feature 053 passes the tooling it exists to build, which is DoD-7 and the plan's dogfooding obligation. Its own 182 contract clauses sit permanently OUTSIDE coverage-baseline.txt because the baseline面 excludes this feature's spec dir, so they could only ever be claimed, never exempted — and all 182 are claimed by the seven rows that pin them (T007/T008/T017/T024/T030/T038/T044), each contract's full set on one row so every clause is claimed exactly once. validate-tasks.py exits 0 on this tasks.md with zero green-* findings; the accountant reports status ok with 0 uncovered beyond baseline and its paired companion at 182. Self-hosting found four of the seven falsified premises above, including the one where this feature's own definition row broke this feature's own gate — the strongest available evidence that the proposition it argues for is true.

notes_red_first_scope=Six of the seven pinning suites were proven red before their subject existed, with the failing output pasted into notes/red-first-evidence.md (T004 clause_extract, T007/T008 US1, T017 US2, T024 US3, T030 US4, T038 US5). The seventh, tests/contract/test_neutrality_budget.py (T044), has NO red-first phase by construction: every one of its 19 clauses is a negative proposition about artifacts that had already landed in Phases 1-7 (nothing was added, the budget did not move, no machinery appeared), so there is no subject whose absence could make it red. DoD-2's red-first obligation is therefore vacuous for that suite rather than unmet, and it was discharged the only way a green-on-arrival guard can be: a mutation drill proving it CAN go red, run twice and recorded in notes_mutation_drills= above (a planted repo proper name turned 1 test red; a planted blocking phrase moved the scanner 23 -> 24 and turned 3 red), each restored by exact reverse substitution with `git diff` verified empty. The same reasoning is why each of its tests carries a positive control or a scanned-population sentinel.

notes_dod8_closure=DoD-8 named four landing points but only two had task rows: T034 owned docs/reference/commands/team.md and T035 the Tool record, while docs/reference/commands/requirements.md and docs/reference/commands/tasks.md belonged to no row. Both were found stale on the DoD sweep and closed in the wrap-up pass — the requirements reference described no validation step at all (so US1's new stop-on-ERROR behaviour was undocumented for readers of docs/), and the tasks reference enumerated the validator's rule list and had drifted from it by exactly the four green-* checks US2 added. DoD-8's row in tasks.md carries the annotation; the row was NOT marked met on the strength of the two files it named, which is the folding-a-void-row-silently failure the flip gate forbids.
