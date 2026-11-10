# Spec Audit — `.specify/archive/specs/066-loop-state-awareness-a/` (batch 8)

**Date**: 2026-11-10
**Mode**: read-only audit of the MAIN tree `/storage/project/cloud-native-ai/spec-kit` (working tree as-is, including uncommitted changes)
**Subject**: archived spec `066-loop-state-awareness-a` (Feature 065 slice A) vs the current implementation
**Output**: this file only — no spec, source or test file was modified; no commit was made.

## Scope

All 13 artifacts in the archive were read and scanned for repository-path references:

`requirements.md`, `plan.md`, `tasks.md`, `research.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`,
`contracts/{awareness-rules,compatibility-and-tests,snapshot-cli,snapshot-schema}.md`,
`notes/{historical,parent-fr-mapping}.md`, `checklists/*` (links), `test-evidence/*`.

**Counting rule**: one reference = one distinct normalized path target per literal form.
Trailing slashes normalized; brace (`skills/external/.../{A,B,C,D}`) and elided (`skills/.../references/...`) forms expanded/folded to their resolved targets; non-path command-output fragments (`docs/mirror`) dropped. Spec-internal artifacts are counted relative to the archived spec directory. A target named once relatively and once by its stale pre-archive absolute path counts as two literals because the two resolve differently (alive vs dead).

## Counts

| Class | Total | Alive | Archived-elsewhere | Dead |
|---|---:|---:|---:|---:|
| A — prefixed/external repo paths | 53 | 51 | 0 | 2 |
| B — stale pre-archive absolute self-paths `.specify/specs/066-loop-state-awareness-a/…` | 12 | 0 | 0 | 12 |
| C — spec-relative artifacts (resolved inside the archive) | 28 | 20 | 0 | 8 |
| **Total** | **93** | **71** | **0** | **22** |

`archived-elsewhere` is zero: the only relocated objects referenced by 066 are the spec's own files, and the audit rule counts their stale pre-archive paths as dead (their archive-resident counterparts are named in the broken list).

Alive highlights (all verified on disk): the whole `skills/external/sdd-loop-driver/` source tree, its `.specify/skills/sdd-loop-driver/` mirror, `docs/reference/skills/sdd-loop-driver.md`, `scripts/python/sync-mirrors.py`, `.specify/scripts/python/{clause_extract,account-clause-coverage,validate-tasks}.py`, `.specify/shared/guidelines/user-facing-comprehension.md`, `.specify/skills/internal/implement-feature/SKILL.md`, the parent spec `.specify/specs/065-loop-interruption-recovery/` (incl. `requirements.md`, `state-spine.md`, `notes/decomposition-gate.md`, `notes/plan-blocked-review.md`), the ledger target `.specify/specs/065a-state-awareness/`, `tests/unit/test_loop_state_engine.py`, `tests/contract/test_sdd_loop_driver_{skill,efficiency}.py`, `tests/unit/test_{line_registry_engine,decomposition_check}.py`, `templates/`, `src/`, `pyproject.toml`.

## Broken references

### B1 — Stale pre-archive absolute self-paths (12, all dead)

The spec now lives at `.specify/archive/specs/066-loop-state-awareness-a/`; every literal below resolves to nothing. 35 occurrence lines across 6 artifacts (`requirements.md` 1, `plan.md` 2, `research.md` 1, `tasks.md` 29, `notes/parent-fr-mapping.md` 1, `checklists/requirements.md` 1).

| Anchor (representative) | Literal | Now resolves to |
|---|---|---|
| `plan.md:79`, `requirements.md:8`, `tasks.md:7` | `.specify/specs/066-loop-state-awareness-a` (dir) | absent; dir is `.specify/archive/specs/066-loop-state-awareness-a/` |
| `plan.md:7`, `research.md:18`, `notes/parent-fr-mapping.md:5`, `checklists/requirements.md:46` | `.specify/specs/066-loop-state-awareness-a/requirements.md` | absent; exists at `.specify/archive/specs/066-loop-state-awareness-a/requirements.md` |
| `tasks.md:31`, `tasks.md:36` | `.specify/specs/066-loop-state-awareness-a/tasks.md` | absent; exists at archive path |
| `tasks.md:75` | `.specify/specs/066-loop-state-awareness-a/contracts/*.md` | absent; 4 contract files exist at archive path |
| `tasks.md:79` | `.specify/specs/066-loop-state-awareness-a/contracts/compatibility-and-tests.md` | absent; exists at archive path |
| `tasks.md:173` | `.specify/specs/066-loop-state-awareness-a/coverage-baseline.txt` | absent; absent in the archive too (T002 never executed) |
| `tasks.md:172` | `.specify/specs/066-loop-state-awareness-a/notes/` | absent as a live path; `notes/` exists at archive path |
| `tasks.md:258` | `.specify/specs/066-loop-state-awareness-a/notes/mutation-drills.md` | absent; absent in the archive too (T030 never executed) |
| `tasks.md:257` | `.specify/specs/066-loop-state-awareness-a/notes/quickstart-run.md` | absent; absent in the archive too (T029 never executed) |
| `tasks.md:185`, `tasks.md:225`, `tasks.md:239` | `.specify/specs/066-loop-state-awareness-a/notes/red-first-evidence.md` | absent; absent in the archive too |
| `tasks.md:65` | `.specify/specs/066-loop-state-awareness-a/test-evidence/` | absent as a live path; `test-evidence/` exists at archive path |
| `tasks.md:18`, `tasks.md:37`, `tasks.md:259`–`261` | `.specify/specs/066-loop-state-awareness-a/verification.md` | absent; absent in the archive too (DoD-6/GATE-7 never satisfied) |

### B2 — Missing test suites (2, dead)

| Anchor | Literal | Now resolves to |
|---|---|---|
| `plan.md:106`, `tasks.md:206` | `tests/contract/test_sdd_loop_driver_state_awareness.py` | absent; no renamed copy. Nearest successor is `tests/contract/test_loop_state_contract.py` (065a, 751 lines), which does not carry 066's clause set or watcher-SHA anchor |
| `plan.md:107`, `tasks.md:207` | `tests/integration/test_loop_state_snapshot_matrix.py` | absent; no successor with that role |

Also cited at `plan.md:123`, `tasks.md:21`, `tasks.md:33`, `tasks.md:225`, `feature-ref.md:31–32`, `research.md:191–192`, `quickstart.md:45`.

### B3 — Missing spec-relative artifacts and broken links (8, dead)

| Anchor | Literal | Now resolves to |
|---|---|---|
| `tasks.md:18`, `tasks.md:23`, `tasks.md:37` | `verification.md` (slice evidence file) | absent; never created (DoD Status stayed `pending`, all tasks `- [ ]`) |
| `tasks.md:65`, `tasks.md:173`, `tasks.md:336` | `coverage-baseline.txt` | absent; never created |
| `tasks.md:172`, `tasks.md:173` | `notes/pre-change-measurements.md` | absent; never created |
| `tasks.md:185`, `tasks.md:203`, `tasks.md:225`, `tasks.md:239` | `notes/red-first-evidence.md` | absent; never created |
| `tasks.md:23`, `tasks.md:257` | `notes/quickstart-run.md` | absent; never created |
| `tasks.md:23`, `tasks.md:258` | `notes/mutation-drills.md` | absent; never created |
| `requirements.md:10` | `brief-065a.md` (slice brief) | no file of this name anywhere in the repo |
| `checklists/2026-10-21-state-awareness.md:5` | `[Feature 065](…)](../../../memory/features/065.md)` | resolves to `.specify/archive/memory/features/065.md` (absent) — the archive move broke the relative link; the live object is `.specify/memory/features/065.md` |

## Ledger-target check

Ledger row (`CONSOLIDATION-LEDGER.md:16`):
`| 066-loop-state-awareness-a | archive | superseded by 065a (banner-archived 2026-10-22) | review-G6 |`

- **Verdict `archive` — accurate**: the spec directory is present under `.specify/archive/specs/066-loop-state-awareness-a/`.
- **Target `065a` resolves**: `.specify/specs/065a-state-awareness/` exists with `requirements.md`, `plan.md`, `tasks.md`, `verification.md`, `review.md`.
- **Banner date matches**: `requirements.md:3`, `plan.md:3`, `feature-ref.md:3` and `notes/historical.md:3` all record "archived/Archived 2026-10-22"; `notes/historical.md` names `065a-state-awareness` as the active execution basis.
- **Registry row resolves**: `.specify/memory/features.md:74` carries Feature 065 (status `Planned`), and `.specify/memory/features/065.md` exists (Last Updated 2026-10-22, records 065a as active basis and 066 as the retained parallel attempt).
- **Provenance note**: the cited `review-G6` artifact was written to `.specify/.tmp/sdd-loop/tmp/spec-consolidation/review-G6.md`, which no longer exists (temp cleanup); the only surviving trace is `.specify/history/.work/a3821ef3-4cfd-45e6-b8fe-5671936e2f18.txt`. The row itself is accurate; its provenance is not persisted.
- **Content nuance inside the archive**: `plan.md:218` § Slice Identity Note still says "066 supersedes 065a as the execution basis" — the reverse of the final decision recorded in the ledger and in the archive banner. The banner supersedes the note; no ledger error.

## Missing guards

1. `tests/contract/test_sdd_loop_driver_state_awareness.py` — missing (066's clause suite: CLI/SNP/RUL/CMP assertions, watcher SHA anchor, map/doc parity, docs/mirror assertions).
2. `tests/integration/test_loop_state_snapshot_matrix.py` — missing (named-fixture matrix, real watcher/git/probe, no-write proof).
3. **Watcher SHA-256 anchor is absent and its pinned value is stale**: 066 pins `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4` (`contracts/compatibility-and-tests.md:5`), but the current `skills/external/sdd-loop-driver/scripts/watch-target.sh` hashes to `955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479`. No test in `tests/` pins the old value (the string survives only in the archive and in the `rename-anchors` worktree copy).
4. Evidence files promised by DoD/GATE never produced: `verification.md`, `coverage-baseline.txt`, `notes/red-first-evidence.md`, `notes/mutation-drills.md`, `notes/quickstart-run.md`, `notes/pre-change-measurements.md`.
5. Guards that **did** survive: `tests/contract/test_sdd_loop_driver_skill.py:376-386` keeps `references/state-awareness.md` and `scripts/loop-state.py` in `MIRROR_FILES`; `tests/unit/test_loop_state_engine.py` and `tests/contract/test_loop_state_contract.py` exist under the 065a numbering.

## Spot checks (three implementation claims)

1. **File claim — PASS (as the 065a object)**. `skills/external/sdd-loop-driver/scripts/loop-state.py` exists (3,262 lines) and implements `snapshot`, `--probe` and `--self-test`; `recover` / `check-spine` are recognized with a refusal owner map (`REFUSAL_OWNER = {"recover": "065c", "check-spine": "065b"}`, line 62). The docstring attributes the implementation to Feature 065 / Slice 065a, not 066. Source and mirror are byte-identical (`cmp` on `loop-state.py` and `state-awareness.md`).
2. **Symbol/command claim — MISMATCH**. 066 CLI-02 (`contracts/snapshot-cli.md:6`) requires `recover`/`check-spine` to return `{schema_version:1, applied:false, result:"refused", steps:[], reason:"action-not-available-in-slice"}` with exit 2. The current engine returns `result:"failed"`, `reason:"not-implemented-in-065a"`, plus `owner`/`message`, and exits 1 (`loop-state.py:2114-2131`, `loop-state.py:3119-3121`, `EXIT_REFUSED = 1` at line 56). 066 itself is internally inconsistent here: CLI-05 reserves exit 1 for these refusals while CLI-02 demands exit 2.
3. **Behaviour surface — MISMATCH**. 066 FR-009/FR-012 claims slice A detects all eight interruption forms, including `heartbeat-stalled` and `lifecycle-spine-violation`. The current engine keeps the eight-value closed vocabulary (`loop-state.py:74-78`) but emits only six (`FORMS_065A`, `loop-state.py:83-86`); the two remaining forms are explicitly deferred to 065b in the owner reference (`references/state-awareness.md:55-66`). This is consistent with the 065a/065b split, not with 066's claim.

## Rename-pending flags (`memory/` → `.specify/` root, branch `rename-anchors`)

Audited against the current tree; these **alive-today** references will move when that branch lands:

| Reference (anchor) | Current target | Future target on `rename-anchors` |
|---|---|---|
| `.specify/memory/constitution.md` (`plan.md:49`) | alive | `.specify/constitution.md` |
| `.specify/memory/features.md` (`tasks.md:164`, `notes/historical.md:13`) | alive | `.specify/features.md` |
| `.specify/memory/features/065.md` (`tasks.md:164`, `notes/historical.md:13`) | alive | `.specify/features/065-loop-interruption-recovery.md` (detail files gain the slug suffix) |
| `.specify/memory/features*` (`tasks.md:66`) | alive | `.specify/features*` |

Stable under the rename (verified in the worktree): `.specify/memory/{tools,feedback,session,exec-quant,evidence}/`, `.specify/scripts/`, `.specify/shared/`, `.specify/skills/`, `.specify/specs/`, `.specify/archive/`. The broken relative link in B3 stays broken either way (`….specify/archive/memory/features/065.md` does not exist).

## Verdict

**BROKEN** — 22 dead references (12 stale pre-archive self-paths, 2 missing test suites, 8 missing spec-relative artifacts/links), the named watcher-SHA guard is absent and its pinned value is stale, and two of the three implementation claims examined do not hold in the current tree (refusal envelope shape/exit code; eight-form detection). All failures trace to the documented 2026-10-22 decision to archive 066 unimplemented in favour of 065a, which is itself `Planned` with a test waiver — the archived spec is therefore a historical record, not an executable contract.

ANOMALY: none — every broken item is explained by the documented archive-without-implementation decision or by the 065a supersession; no unexplained drift was found outside those two causes.

SPEC-AUDIT-8-DONE
