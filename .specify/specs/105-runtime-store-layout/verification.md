# Verification Log — 105-runtime-store-layout

baseline_commit=113d2c650
baseline_date=2026-11-25
baseline_branch=105-runtime-store-layout
implementation_date=2026-11-25
post_change_commit=1e6dc208c (P5R; this file and the task-table closure land in the spec-side commit that follows it)

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py tests/integration/test_store_layout_migration_us3_us6.py tests/integration/test_init_new_layout.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t038-smoke.txt

# -- Evidence records (bind every `pass` claim to archived evidence) --

sample_id=SC-001
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t038-sc-suite.txt
evidence_sha256=3c7308d622ca7096457eb100389a3eaf29d9440ede0fac62d231f7d0d66467c9
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t020-us3-readings.txt
evidence_sha256=abca1857e97080c40cedeea1feba60b2d920132f189b978306ffa889e57cfd42
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t020-us3-readings.txt
evidence_sha256=abca1857e97080c40cedeea1feba60b2d920132f189b978306ffa889e57cfd42
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t016-us2-readings.txt
evidence_sha256=c071f1d20587d4fa23b95732a18795f74c452769ebde8a469a304671e95aad29
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/init-tree-t009.txt
evidence_sha256=7d8a41b8810639c99dab333e1b64ed1d2a75b0e9505a5ede1311517e1c1ededd
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t032-guard-run.txt
evidence_sha256=a59f601291695e27867b8f8791c07379e451ac71f7b6b63c151aa0beaef9a595
verdict=pass

sample_id=SC-007
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/p4-sync-mirrors-check.txt
evidence_sha256=c1b68141e082a3d5fd41589e30e7a297073c70cf0692ceaf03368000dc29a2fc
verdict=pass

sample_id=SC-008
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t024-us4-readings.txt
evidence_sha256=be38259fbe6005dd4b5acf126696769e7f15829fa750e4210f4bd3d9534ec1ae
verdict=pass

sample_id=SC-009
evidence_path=.specify/specs/105-runtime-store-layout/test-evidence/t043-sc009-run.txt
evidence_sha256=7f4b3f9128504f8ed18f5d4b7a3f9280b5887f51cf37e09ccee168f6405f2b12
verdict=pass

# -- Success Criteria evaluation --

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
SC-004_value=us1_us2=6 passed us3_us6=4 passed third_apply_after_resume=clean
SC-004_note=final path. Dry-run zero writes, byte-identical relocation, dual refusal naming both roots, idempotent rerun, plus residue/symlink/readonly/partial failure surfaces (D5/D6 mutation drills) and the P5R resume-supersession regression; evidence test-evidence/t016-us2-readings.txt, p5r-resume-idempotence.txt, mutation-drill.md, notes/red-first-evidence.md § T035/P5R.

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

SC-009_status=pass
SC-009_value=guard=1 passed rows=18 cited_rows=17 drills=2 red migration_apply=applied(14 resolved) residue/dual=blocked
SC-009_note=final path. Guard `test_backward_incompatible_inventory_is_closed` green; T042 delete-row and forbidden-word drills red/green with checksum restore; every migrate:relocate row demonstrated by T016 (dry-run zero-write + apply byte-identical) and the refusal rows by T035 (residue/dual/symlink/readonly); evidence test-evidence/t043-sc009-run.txt, t016-us2-readings.txt, notes/red-first-evidence.md § T042, test-evidence/acceptance-105.md § SC-009. The single smoke triple above applies.

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-001_joint_acceptance=pass
RS-002_joint_acceptance=pass
RS-003_joint_acceptance=pass
RS-004_joint_acceptance=pass
RS-005_joint_acceptance=pass
RS-006_joint_acceptance=pass

deferred_tasks=

notes=Implement packages P1–P5 plus bounded P5R; full fast tier 218 failed / 10040 passed / 0 setup errors with `comm -13` NEW=0 against the 748-name entry baseline (530 repaired; the 218 remaining are named pre-existing reds). Mirrors: `/usr/local/bin/python3 sync-mirrors.py --check` rc 0 / 0 drift members; `regen-command-copies.py --check` rc 0. Retired root absent; 12 stores relocated with receipt v2. P5R closes the crash→resume→third-apply idempotence gap read-only.
