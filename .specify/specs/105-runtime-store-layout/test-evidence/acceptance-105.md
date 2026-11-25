# Acceptance evidence — 105 runtime-store-layout (T038)

- Date: 2026-11-25
- Run: `r20261125T022857Z-06dd`, implement package P5
- Path labels follow `requirements.md` § Success Criteria: SC-001…SC-005 and SC-009 are **final**;
  SC-006…SC-008 are **supporting** (reported against their measured baselines, never as a final gate).
- One command per reading; each cited run went through `scripts/bash/run-tests.sh` (the only test
  entry). Full logs: `test-evidence/t038-sc-suite.txt` (41 passed), `test-evidence/t038-smoke.txt`
  (10 passed). SC-009's row is appended by T043.

## SC-001 — inventory closed, retired root absent (**final**, `pass`)

- Measurement:
  - `git ls-tree -d 23938f22e:.specify/memory | wc -l` → **12** (frozen baseline children).
  - declaration stores → **14** (`specify_cli.store_layout()['stores']`), equal to the requirements
    Store Inventory's 14 store targets.
  - `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_runtime_store_layout.py -q`
    → **7 passed in 6.58s** (includes `test_inventory_is_closed`,
    `test_declaration_equals_inventory_and_consumer_sets`, `test_repo_has_no_retired_root`).
  - `test ! -e .specify/memory` → exit **0**; `git ls-files` under the 14 new roots → **3007** tracked
    paths (the T033 dogfood receipt recorded 2999 at move time; the difference is post-dogfood records,
    including the two dogfood receipts and this package's S-7 re-check receipt).
- Evidence pointers: `test-evidence/t038-sc-suite.txt`, `test-evidence/dogfood.txt`,
  `notes/quickstart-run.md` § S-0/S-7.

## SC-002 — temporary memory under the new roots (**final**, `pass`)

- Measurement: `… run-tests.sh tests/integration/test_memory_preservation.py -q` →
  **5 passed in 6.49s** (session and knowledge record→recall round trips, upsert-by-slug, prune
  bounds, reindex, `run-determination --action determine` persisted under `.specify/session/` and
  retrievable via `--action history`, schema keys equal to the pre-migration form).
- Evidence pointers: `test-evidence/t020-us3-readings.txt`, `notes/red-first-evidence.md` § T020.

## SC-003 — dispatch injection paths unchanged (**final**, `pass`)

- Measurement: `… run-tests.sh tests/integration/test_dispatch_injection_paths.py -q` →
  **7 passed in 6.49s** (seven downlink fields / four injections / five uplink elements; every
  injected memory reference resolves under `.specify/session/` or `.specify/knowledge/`; the
  reverse-token fixture proves a token written only to feedback/exec-quant is never recalled; no
  second injection source, no new payload field).
- Evidence pointers: `test-evidence/t018-red-run.txt` (red side),
  `test-evidence/t020-us3-readings.txt` (green side).

## SC-004 — migration safety: three shapes plus the failure surfaces (**final**, `pass`)

- Measurement:
  - `… run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py -q` →
    **5 passed in 9.76s** — legacy dry-run plans every store and writes nothing (tree digest + `git
    status` empty), `--apply` relocates byte-identically (`diff -r`), the container disappears, dual
    content refuses naming both roots and the repair entry with both trees unchanged, and the rerun is
    `clean` with one receipt per run.
  - `… run-tests.sh tests/integration/test_store_layout_migration_us3_us6.py -q` →
    **4 passed in 9.64s** — residue (exit 3, every path listed, zero deletion), symlink (refuse,
    named path, link untouched), readonly (refuse `permission-denied` on uid 1001, no partial
    success), partial (resume moves only the remainder; one archive record per object; interrupted
    receipt byte-identical).
- Evidence pointers: `test-evidence/t016-us2-readings.txt`, `notes/red-first-evidence.md`
  § T016 / T035, `test-evidence/mutation-drill.md` § D5/D6, `test-evidence/dogfood.txt`.

## SC-005 — fresh initialization (**final**, `pass`)

- Measurement: `… run-tests.sh tests/integration/test_init_new_layout.py -q` →
  **1 passed in 7.36s** — after `specify init` on an empty directory: `.specify/session/` and
  `.specify/knowledge/` exist, `.specify/memory/` does not, other stores are lazy, the core-asset
  list is the two memory tiers, and the anchors stay at `.specify/`.
- Evidence pointers: `test-evidence/init-tree-t009.txt`,
  `notes/red-first-evidence.md` § T006/T009.

## SC-006 — live-reference containment (**supporting**, `pass` on its measured baseline)

- Measurement: `… run-tests.sh tests/contract/test_store_layout_live_refs.py -q` →
  **4 passed in 6.22s** — the measured old-root occurrence file sets equal the declared four-file
  allowlist in both directions for all three product classes; allowlisted files keep only their
  allowed lines; the test-side declaration is pinned to the contract table; the tests-class literal
  set is confined to the declared legacy/guard files (this package's US6 module derives the retired
  path from the declaration, so it adds no literal carrier).
- Evidence pointers: `test-evidence/t032-guard-run.txt`,
  `test-evidence/mutation-drill.md` § D1–D4.

## SC-007 — mirrors and command copies (**supporting**, `pass` on its measured baseline)

- Measurement:
  - `… run-tests.sh tests/contract/test_runtime_store_layout.py::test_mirror_member_set -q` (part of
    the 7-passed module run) — no NEW drift member relative to the 450-DIFF baseline file.
  - `/usr/local/bin/python3 scripts/python/sync-mirrors.py --check` → exit **0**:
    `ok scripts/ == .specify/scripts/ (132 files, byte-identical)` and
    `ok shared/ == .specify/shared/ (116 files, byte-identical)`.
  - `/usr/local/bin/python3 scripts/python/regen-command-copies.py --check` → exit **0**,
    `OK: all per-tool command copies match the source templates.`
  - The literal `python3 scripts/python/sync-mirrors.py --check` exits 2 in this environment because
    the profile interpreter lacks `typer` (platform fact, recorded in P4 R-10); under the pinned
    interpreter the reading above is the measured one.
- Evidence pointers: `notes/quickstart-run.md` § S-7, `test-evidence/p4-sync-mirrors-check.txt`,
  `test-evidence/sync-mirrors-baseline.txt`.

## SC-008 — tools domain tracked/ignored split (**supporting**, `pass` on its measured baseline)

- Measurement:
  - `… run-tests.sh tests/contract/test_tools_domain.py -q` → **4 passed in 6.44s**;
    `… run-tests.sh tests/contract/test_specify_gitignore_template.py -q` → **4 passed in 6.23s** —
    `*.json` inventories ignored, `*.md` records tracked, same-basename record + inventory coexist,
    template and installed copy byte-identical with the narrowed rules, claude/codex templates
    release every declared store root.
  - Live probe on this repository:
    `git check-ignore -v .specify/tools/system.json .specify/sanitize/findings.json .specify/trigger/telemetry.jsonl`
    → `.specify/.gitignore:16:tools/*.json`, `:23:sanitize/`, `:27:trigger/telemetry.jsonl`;
    `git ls-files .specify/tools` → 10 tracked records, zero JSON inventories.
- Evidence pointers: `test-evidence/t024-us4-readings.txt`, `notes/red-first-evidence.md` § T024.

## SC-009 — backward-incompatible change closure (**final**, `pass`; appended by T043)

- Inventory closure guard: `tests/contract/test_runtime_store_layout.py::test_backward_incompatible_inventory_is_closed`
  → **1 passed** (in the 10-passed fresh run `test-evidence/t043-sc009-run.txt`). The guard asserts, on
  the current plan: 18 contiguous rows BC01…BC18; the cited Store Inventory set `{1…15, 17}` exactly
  once each (14 relocations + container + `draft`); every behavior inside the closed class set with
  every `migrate:refuse:` token present in M-5; every evidence pointer resolving to an existing test
  path, evidence file, task id, or contract heading (with `同 BC01` resolved transitively); and zero
  forbidden behavior words in the Behavior cell (U-03 scope: BC12's change cell legitimately names
  `todo/`, and the test pins that fact).
- Red ability (T042 drills, `notes/red-first-evidence.md` § T042): deleting the BC13 row →
  `1 failed` (`the inventory must be a contiguous, duplicate-free BC01…BCNN set`); replacing BC01's
  behavior with `manual` → `1 failed` (`BC01: behavior 'manual' is outside the closed class set`);
  both restored with checksum equality and green re-run; `git diff -- plan.md` empty.
- `migrate:relocate` rows demonstrated (BC01…BC14): `test-evidence/t016-us2-readings.txt` — legacy
  dry-run `planned` with **zero writes** (`tree_unchanged=True`, `git_status_empty=True`,
  `receipt_store_created=False`), `--apply` `applied` with `diff_r_rc=[0]` per store and
  `storeLayout stores=14 resolved=14 refused=0 container=removed`; rerun `clean` with zero moves.
- Refusal rows demonstrated: BC16 (`draft/`) and the container pass — T035 residue fixture exits **3**
  `blocked`, every residue path listed, zero deletion (BC15/BC16); dual content exits **3** with both
  roots and the repair entry named (M-8 dual row); symlink and readonly refusals in the same module
  (fresh run above: 10 passed).
- Compatibility rows: BC17 (`no-workspace-object`) — fresh-init fixture green (SC-005); BC18
  (`compatibility-bridge`) — the two 097 dimension-pin tests assert the five-token prefix plus the
  six-token set (`tests/contract/test_migrate_engine_contract.py`, `tests/unit/test_migrate_planner.py`);
  v1 receipts remain resume inputs by construction (M-6).
- Smoke record: the feature's single smoke record in `test-evidence/verification-input.md`
  (`smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …`,
  `smoke_exit_code=0`, `smoke_evidence_path=…/t038-smoke.txt`) covers the main flow; T043 cites it
  rather than adding a second record.
- No fabricated readings: every number above is from the captured runs named inline.
