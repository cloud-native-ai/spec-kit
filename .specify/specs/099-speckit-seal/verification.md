# Verification Log — 099-speckit-seal

baseline_commit=5e233678a
baseline_date=2026-11-11
baseline_branch=099-speckit-seal
implementation_date=2026-11-11
post_change_commit=5e233678a (P8b 收口；P9 的证据与状态包由承载本文件的提交落盘)

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/integration/test_seal_074_round.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/099-speckit-seal/notes/quickstart-run.md

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-003_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=clean single-spec fixture seals (exit 0, seal.outcome=sealed, 3 writes: registry row + detail + seal.md 1729 B); the rerun is already-sealed with 0 writes and no second receipt; the status pair flips to Sealed in the same batch; removing Sealed from one surface turns the drift guard red naming that surface
SC-001_note=carriers tests/contract/test_seal_seal.py (success, idempotence, status pair) + tests/contract/test_sealed_status_domain.py; live reading in notes/quickstart-run.md § S-4; P8b targeted suite 130 passed on the seal contract+integration set

SC-002_status=pass
SC-002_value=eight refusal classes each named with the closed code and zero writes with the status faces unchanged: from-status-invalid 1, p0-unresolved 1, closure-refused 1, closure-input-defect 2, conflict-open 1, slice-unclosed 1 (also names merge-incomplete), state-drift 2, dirty-spec-tree 1; the three-minus-one fixture is refused (closure-refused, exit 1)
SC-002_note=carrier tests/contract/test_seal_seal.py (REFUSALS table + three-minus-one); live re-execution 9/9 in notes/quickstart-run.md § S-5 (seal.md absent every time)

SC-003_status=pass
SC-003_value=two merge-apply runs produce byte-identical products and manifest (sha256 list diff empty, exit 0); the successful rerun is idempotent with zero writes; the order-by-return-time mutation turns tests/integration/test_seal_merge_determinism.py red
SC-003_note=live reading notes/quickstart-run.md § S-3 (run1/run2 sha equal; second run idempotent=true writes=[]); carriers tests/integration/test_seal_merge_determinism.py + tests/contract/test_seal_merge_apply.py green

SC-004_status=pass
SC-004_value=merged parent checks: id_continuity=pass, open_rows=0, duplicate_ids=0, dangling_refs=0; the id maps cover every slice entry; the 074 round rerun's validate-tasks reports 0 error (2 warnings, pre-existing slice-row kinds) with 0 open rows
SC-004_note=fixture reading notes/quickstart-run.md § S-3; round reading test-evidence/074-merge-checks-rerun-20261111.txt + test-evidence/074-merge-apply-rerun-20261111.txt; carrier tests/contract/test_seal_merge_apply.py

SC-005_status=pass
SC-005_value=same-number-different-meaning pairs are detected as conflicts with both literals side by side and resolved through declared mappings (074a local STR-010 -> parent STR-011; 074b local STR-004..007 -> STR-007..010); factory-doc local-ID references are detected and rewritten to parent IDs; the silent-renumbering mutation turns the carrier red
SC-005_note=round reading test-evidence/074-merge-plan-rerun-20261111.json/.txt (factory_doc_refs resolved, id_maps STR 17); carriers tests/contract/test_seal_merge_plan.py + tests/contract/test_seal_merge_apply.py

SC-006_status=pass
SC-006_value=the 074 round executed end to end and the terminal state is the named refusal: seal exit 2, sole engine condition closure-input-defect (B2); FR-027(a)/(b)/(c)/(e) resolved, FR-027(d) blocked (074b P0 F1 carries only a driver-recorded waiver); extra blockers B1 resolved, B2 blocked, B3 resolved, B4 resolved; the blocked-state rerun reproduces the refusal byte-identically; parent tasks.md open rows = 0 (57 pre-split rows superseded per C-022)
SC-006_note=round record test-evidence/074-round-20261110.txt; repair+rerun test-evidence/074-round-rerun-20261111.txt + test-evidence/p8b-dispositions-20261111.md; live rerun form notes/quickstart-run.md § S-7/S-8; carrier tests/integration/test_seal_074_round.py (5 passed)

SC-007_status=pass
SC-007_value=archive admission has one owner: Sealed -> exit 0 pointer seal.md; non-Sealed -> exit 1 reason not-sealed pointer /speckit.seal; legacy Completed without a C-044 ruling -> exit 1 legacy-completed-unruled; state-drift -> exit 2; copying the criterion into a second implementation turns the single-owner guard red
SC-007_note=live three-target reading notes/quickstart-run.md § S-6; carrier tests/contract/test_seal_archive_gate.py (incl. the static single-owner scan) green

SC-008_status=pass
SC-008_value=one schema owner for the status domain (shared/workflow/acceptance-hardening.md § Feature Status); every consumer recognizes Sealed and the drift guard names any surface that drops it; the engine action table carries no move/delete/archive/push/scheduler; no second state machine, registry, ledger, scheduler or parallel spec tree is added
SC-008_note=test-evidence/boundaries-audit.txt; carriers tests/contract/test_seal_boundaries.py + tests/contract/test_seal_archive_gate.py + tests/contract/test_sealed_status_domain.py green

SC-009_status=pass
SC-009_value=two concurrent seals on different specs write disjoint paths (no shared mutable aggregate); the review and slice measurement files stay byte-identical across a seal (hash comparison); an uncommitted change under the parent spec tree is refused as dirty-spec-tree naming the path
SC-009_note=carrier tests/contract/test_seal_concurrency_and_readonly.py green; the tree-level read-only reading is also in notes/quickstart-run.md § S-7 (git status over the three 074 trees empty after the rerun)

# -- Deferred tasks --

deferred_tasks=T041,T050
deferred_reason_summary=T041: the merged-074 post-checks were deferred in P8 on the merge engine's B3/B4 output defects (validate-tasks 43 errors); the root cause was repaired and the round rerun in P8b, and the row keeps the historical deferral record. T050: the coverage-lane zero-delta is unattainable under merge-back C-022 — this spec's 45/45 clauses are claimed, while the 074 round's mandated supersede rendering turns the parent's 67 pre-split green claims into quoted records, leaving those five parent contract files uncovered beyond the frozen baseline (67 named and attributed in test-evidence/coverage-final.txt); deferred to the user (accept the named residual, allowed by SC-006, or re-open the C-022 vs clause-claim conflict).

# -- Acceptance summary (copied from the checker; never recomputed here) --

final_path_pass=6
final_path_blocked=0
final_path_deferred=0
final_path_partial=0
final_path_fail=0
final_path_unknown=0
final_path_total=6
acceptance_verdict=accept
final_path_source=test-evidence/closure-verdict-099-preflip.json (claimed status Planned, verdict accept, 6/6 final pass) + test-evidence/closure-verdict-099.json (post-flip, claimed status Implemented, re-judged); both are the checker's own --json payloads, copied, not recomputed

# -- Notes --

notes=T045: full-suite GATE-1 reading is test-evidence/final-suite.txt — definitive serial run 268 failed / 8415 passed / 2 skipped, comm -13 against the 280-entry implementation-entry baseline is EMPTY (0 new), 12 baseline reds now pass; the default parallel form's 14 beyond-baseline names are each attributed there (8 feature-caused pin drifts repaired with dated stale-pin updates, 6 parallel-interference names under the documented nested-worktree self-location trap). T046: both mirror checks exit 0 with zero new drift (test-evidence/final-mirror-checks.txt). T047: quickstart S-1…S-9 executed with real commands/outputs/exit codes (notes/quickstart-run.md). T050: coverage lane reading test-evidence/coverage-final.txt (45/45 own clauses claimed; 67 residual names attributed to the round's C-022 consequence; deferred). The feature flip to Implemented happened after the pre-flip closure verdict and was re-judged after the flip; both payloads are recorded in test-evidence/closure-verdict-099.json (post-flip) and test-evidence/closure-verdict-099-preflip.json.
