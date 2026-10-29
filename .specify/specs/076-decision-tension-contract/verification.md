# Verification Log — 076-decision-tension-contract

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=75216750
baseline_date=2026-10-29
baseline_branch=076-decision-tension-contract

# Full-suite baseline captured at implement start (E2 slot 1): 6514 passed / 39 failed / 7 skipped.
baseline_suite_failed=39
baseline_suite_failed_names=.specify/specs/076-decision-tension-contract/baseline-failed.txt
baseline_targeted_guard_passed=71

# -- /speckit.implement results --

implementation_date=2026-10-29
# Tree this segment (part 4/4) builds on: the P3 commit. This segment's own commit hash is reported
# in the implement wrap-up report; verification.md is written before that commit exists, so no
# self-referential hash is invented here.
segment_base_commit=3c1a288c
post_change_commit=3c1a288c

# P3 (T014–T020) measured the targeted set only; P4 (T021–T027) adds the guard slices, the mirror
# closeout, the zero-new-mechanism set difference and the quickstart runs. The closure full run
# belongs after review and is NOT pre-spent here.
post_change_targeted_set_passed=131
post_change_targeted_set_failed=0
post_change_remaining_open_tasks=0

# -- Evidence records (bind every `pass` claim to archived evidence) --

sample_id=SC-001_validator_twelve_runs
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/quickstart-s1-s5.txt
evidence_sha256=6069fb3be560b8adb542bc6020f47a8ade4b187d69aa1cfcfa7f6f9b6b22e8e8
verdict=pass

sample_id=SC-002_analyze_snapshot_set
evidence_path=.specify/specs/076-decision-tension-contract/notes/analyze-sc003/S3-section-missing.md
evidence_sha256=4f78b18354170efa6c6dbac0ccfb7bf440fe6ff409426fbff99d3a06855a1092
verdict=pass

sample_id=SC-003_gating_triple
evidence_path=.specify/specs/076-decision-tension-contract/notes/analyze-sc003/D-2-section-removed.md
evidence_sha256=d3590e0791e6ff24380eb16775ec8607652e8e8257ee2ffcf373e21d68e123c0
verdict=pass

sample_id=SC-004_quartet_eleven_runs
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/quickstart-s1-s5.txt
evidence_sha256=6069fb3be560b8adb542bc6020f47a8ade4b187d69aa1cfcfa7f6f9b6b22e8e8
verdict=pass

sample_id=SC-005_zero_new_mechanism
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/zero-new-mechanism.txt
evidence_sha256=3f182e8d77448a09206303c8d52117b749851f839d4610d3a26a485c34063d64
verdict=pass

sample_id=SC-006_adr_traceability
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/green-sc006-adr-traceability.txt
evidence_sha256=5df2910456c753b74d22ab214b4bc70f1771f6e1eac008f5bcf52a7328ed996e
verdict=pass

sample_id=SC-007_terminology_counts
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/terminology-counts-after.txt
evidence_sha256=c32042ce947719612bb2a8f886e985ea22ca5589c2a7c2fd0660f39337d0677b
verdict=pass

sample_id=SC-008_closed_set_delta
evidence_path=.specify/specs/076-decision-tension-contract/test-evidence/closed-set-delta.txt
evidence_sha256=1f1b7c67a859cde5c12f1be68fd58132f48d9c7d703e4d43d0e0ab5aa1d04425
verdict=pass

# -- Success Criteria evaluation --
# Vocabulary is the one owned by .specify/templates/verification-log-template.md
# (pass | fail | partial | deferred | unknown).

SC-001_status=pass
SC-001_value=12/12 runs as declared (1 compliant exit 0 on a fixture AND on the feature's own plan.md; 11 inverse inputs exit 1, each hitting exactly one declared label, total findings 1 per run)
SC-001_note=evidence test-evidence/quickstart-s1-s5.txt § S1 + § S2; the compliant run also covered the real plan (`scanned: 275 lines, 2 record(s)`)

SC-002_status=pass
SC-002_value=HIGH counts 0 / 1 / 1 / 1 across the four fixtures; the missing-section fixture is reported, not skipped
SC-002_note=snapshots notes/analyze-sc003/S3-{compliant,section-missing,record-incomplete,cost-unmapped}.md; channel is a detection pass rendering the program verdict under its HIGH-or-0 mapping — the /speckit.analyze narrative layer was not produced by a full skill run and no SC depends on it

SC-003_status=pass
SC-003_value=three snapshots 0 / 1 / 0 (compliant N/A → 0, section removed → 1, compliant record → 0)
SC-003_note=notes/analyze-sc003/D-{1,2,3}-*.md re-rendered by the `-k "d1 or d2 or d3"` run (3 passed); the bare-`N/A` case stays an additional assertion outside the triple

SC-004_status=pass
SC-004_value=11 runs: 1 accepted (exit 0) + 6 reason codes rejected once each (6/6) + 4 additional `missing-field` samples; exit codes 0/1/2 all covered; double-`red:` pinpoint accepted on the first split
SC-004_note=evidence test-evidence/quickstart-s1-s5.txt § S4; reason codes come from the closed set, never from a seventh value

SC-005_status=pass
SC-005_value=allowed-delta set = {} (empty); new mechanism count = 0 — command names 27 = 27 (added [], removed []), dependencies byte-identical, process/scheduler/scorer carriers 0 = 0, both new validators import stdlib only
SC-005_note=test-evidence/zero-new-mechanism.txt (complete capture + re-derivable collector); test-evidence/scope-set-difference.txt is the pointer slot named by tasks.md T022

SC-006_status=pass
SC-006_value=ADR `## Alternatives` carries the `tension_id` slot (T-NNN, plan.md, no field copied, 无承重张力记录 + verdict required); fixture record's cost resolves; an unresolvable `tension_id` is reported as a broken link through `index_records`
SC-006_note=test-evidence/green-sc006-adr-traceability.txt — scenario E is the ONE declared call surface; no command was added and the analyze channel never scans docs/decisions/

SC-007_status=pass
SC-007_value=five aliases × three trees = 0 hits (same as the pre-change baseline: all five were 0); A3 alias list still present with all five terms; owner `shared/guidelines/decision-tension.md` is inside the scanned surface and carries 0 (it is not whitelisted)
SC-007_note=test-evidence/terminology-counts-after.txt; whitelist is exactly two places, both outside the trees (§ Assumptions A3 and .specify/memory/features/076.md § 附)

SC-008_status=pass
SC-008_value=deleted or rewritten lines outside the declared allowed delta set = 0 (detection-and-severity.md: 1 removed = the count heading, 37 added = count heading + new channel section; critique-and-self-critique.md: 0 removed, 18 added = the quartet subsection); item counts: rejection forms 4→4, boundary declarations 6→6, consumer-list rows 4→4, pass sections A–G→A–G+I, DO-NOT-FLAG 6→6, severity domain 4→4
SC-008_note=test-evidence/closed-set-delta.txt (enumeration) + scenario G in the contract suite (drift guard: rewriting any baseline line or leaking an alias turns it red, see test-evidence/t021-scenario-fg-guards.txt)

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=T021 landed the two post-implementation guard slices (F terminology, G closed-set delta) and both were proven to go red under mutation before being declared green (test-evidence/t021-scenario-fg-guards.txt). T022's set difference is empty on all three inventories. T023 re-measured terminology at 0. T024 ran sync-mirrors --write then --check (all six pairs ok, all seven FR-025 pairs plus templates/instructions-template.md byte-identical) and actually ran scripts/bash/generate-instructions.sh under CWS_LIB_BASH_HOME: live .specify/instructions.md sha256 unchanged (41fd81a0…), reconcile reported 「live instructions already carry all template sections」, and the section table shows Task Complexity Rubric live 894 B vs template 1208 B — the measured proof that an existing section is never rewritten, so the T005 template pointer rides in only on that section's next whole-section convergence. T026 executed quickstart S1–S5 green with real exit codes. No deviation from the plan-owned artifacts: git diff --stat on plan.md / requirements.md / research.md / data-model.md / contracts/ / quickstart.md / feature-ref.md is empty.
