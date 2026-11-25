# Verification inputs — 105-runtime-store-layout (T039)

- Date: 2026-11-25
- Run: `r20261125T022857Z-06dd`, implement package P5
- This file is the **input block** for `verification.md`; the spec side materializes that file.
  The key=value block below is the record (the closure checker parses `SC-NNN_status=` lines);
  prose above it is orientation only. SC-009's final pass row is appended by T043.
- Status vocabulary: the closed set owned by `templates/verification-log-template.md`
  (`pass | fail | partial | blocked | deferred | unknown`).
- Path labels: SC-001…SC-005 and SC-009 are `final`; SC-006…SC-008 are `supporting`
  (`requirements.md` § Success Criteria). Supporting readings are reported against their measured
  baselines and do not masquerade as a final gate.

SC-001_status=pass
SC-001_value=baseline_children=12 declared_stores=14 tracked_new_roots=3007 retired_root_absent=yes
SC-001_note=final path. `test_runtime_store_layout.py` 7 passed (inventory/declaration/framework map/no retired root); `test ! -e .specify/memory` exit 0; evidence test-evidence/t038-sc-suite.txt, test-evidence/dogfood.txt, notes/quickstart-run.md § S-0/S-7.
SC-002_status=pass
SC-002_value=tests/integration/test_memory_preservation.py=5 passed
SC-002_note=final path. session/knowledge record→recall, upsert-by-slug, prune bounds, reindex, determination persisted under .specify/session and retrievable by --action history; evidence test-evidence/t020-us3-readings.txt.
SC-003_status=pass
SC-003_value=tests/integration/test_dispatch_injection_paths.py=7 passed
SC-003_note=final path. Seven downlink fields / four injections / five uplink elements on the two memory tiers; reverse-token fixture proves feedback/exec-quant records are never recalled; no new payload field or second source; evidence test-evidence/t018-red-run.txt, t020-us3-readings.txt.
SC-004_status=pass
SC-004_value=us1_us2=5 passed us3_us6=4 passed
SC-004_note=final path. Dry-run zero writes, byte-identical relocation, dual refusal naming both roots, idempotent rerun, plus residue/symlink/readonly/partial failure surfaces (D5/D6 mutation drills); evidence test-evidence/t016-us2-readings.txt, mutation-drill.md, notes/red-first-evidence.md § T035.
SC-005_status=pass
SC-005_value=tests/integration/test_init_new_layout.py=1 passed
SC-005_note=final path. Fresh init seeds .specify/session and .specify/knowledge, never creates .specify/memory, other stores lazy, anchors at .specify/; evidence test-evidence/init-tree-t009.txt.
SC-006_status=pass
SC-006_value=tests/contract/test_store_layout_live_refs.py=4 passed
SC-006_note=supporting path (measured baseline, not a final gate). Measured old-root file sets equal the declared four-file allowlist both directions across the three product classes; allowlisted lines confined; tests-class literals confined to the declared legacy/guard set; evidence test-evidence/t032-guard-run.txt, mutation-drill.md § D1–D4.
SC-007_status=pass
SC-007_value=sync-mirrors rc=0 (scripts 132 files, shared 116 files byte-identical) regen-copies rc=0 no_new_drift_member=yes
SC-007_note=supporting path (measured baseline). `test_mirror_member_set` green; interpreter-pinned readings in notes/quickstart-run.md § S-7 (the literal profile-`python3` form exits 2 for lack of typer — recorded platform fact, P4 R-10); evidence test-evidence/p4-sync-mirrors-check.txt, sync-mirrors-baseline.txt.
SC-008_status=pass
SC-008_value=tools_domain=4 passed gitignore_template=4 passed tracked_records=10 ignored_inventories=all
SC-008_note=supporting path (measured baseline). tools/*.json ignored, *.md tracked, same-basename coexistence, template == installed copy byte-identical, claude/codex templates release every store root; live `git check-ignore` reading in test-evidence/non-goals-audit.md § 4 (ignore matrix) and t024-us4-readings.txt.
smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py tests/integration/test_store_layout_migration_us3_us6.py tests/integration/test_init_new_layout.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t038-smoke.txt
deferred_tasks=

- The single smoke record above is the feature's end-to-end main flow (old-layout upgrade, the four
  failure surfaces, and fresh initialization). It is written exactly once; T043's SC-009 row cites
  this record instead of adding a second `smoke_command=`.
SC-009_status=pass
SC-009_value=guard=1 passed rows=18 cited_rows=17 drills=2 red migration_apply=applied(14 resolved) residue/dual=blocked
SC-009_note=final path (row appended by T043). Guard `test_backward_incompatible_inventory_is_closed` green; T042 delete-row and forbidden-word drills red/green with checksum restore; every migrate:relocate row demonstrated by T016 (dry-run zero-write + apply byte-identical) and the refusal rows by T035 (residue/dual/symlink/readonly); evidence test-evidence/t043-sc009-run.txt, t016-us2-readings.txt, notes/red-first-evidence.md § T042, test-evidence/acceptance-105.md § SC-009. Smoke record: the single triple written at T039 above applies.
