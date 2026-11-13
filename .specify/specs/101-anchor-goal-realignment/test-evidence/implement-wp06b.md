# Implement — WP-06b (GATE-1 closure repair)

**Date**: 2026-11-12
**Unit**: `skill:implement-feature` / `r20261112T064607Z-b101`
**Entry state**: `43e38095a` (checkpoint 20); the in-territory edits described here were
committed during the gap as `101cce5e4` ("update test case"), so HEAD at the final-suite
run already contained them.
**Verdict**: **35 of 37 new failure ids closed in-territory; 2 remain blocked on an
out-of-territory engine enumeration defect.** GATE-1 therefore still FAILs on exactly
those two ids; nothing was weakened, no guard was deleted, no out-of-territory source was
edited.

## 1. Final suite (the single closure-repair rerun)

| | Reading |
|---|---|
| Command | `bash scripts/bash/run-tests.sh --full --names-out .specify/specs/101-anchor-goal-realignment/test-evidence/final-suite-2026-11-12.txt` |
| Exit | 1 |
| Pass 1 | **193 failed / 8972 passed / 3 skipped** (9168 collected, 56.23 s), passes=2 tier=full |
| Pass 2 | 1 passed / 9168 deselected (the declared serial test) |
| Failure-id names | 193 entries written to `final-suite-2026-11-12.txt` |
| Full output | `final-suite-2026-11-12.log` (untracked console log of the same run) |
| E2 baseline | `suite-baseline-entry.txt` — 192 ids |
| `comm -13` (new) | **3** at run time (see § 2 for the disposition of each) |
| `comm -23` (fixed) | 2 — `test_criterion_subject.py::test_c3_the_section_is_an_addition_and_no_existing_form_was_rewritten`, `test_goal_migration_path.py::test_migration_preserves_the_resolved_objective` |

## 2. The 37 → 2 accounting

All edits are to live tests / live owners inside the declared write territory. Where a
test pinned a dated fact (a SHA-256, a command count, a summary path), the pin was moved
to the new live fact with the evidence recorded in the test's own rationale.

| Group (module) | Ids | What changed | Status |
|---|---|---|---|
| `tests/contract/test_criterion_subject.py` | 11 | Owner moved to `shared/definitions/anchor-definitions.md`; real subject `.specify/anchoring/draw-two-layer-structure/anchor.md`; the `PREEXISTING_SECTIONS` table re-derived from the Anchor doc's 9 H2 headings; the `[subjects: <glob>]` contract, literal count and exit-code facts kept intact | closed |
| `tests/contract/test_temp_goal_contract.py` | 6 | Retargeted to `088-speckit-visualization` as an **action-level Goal** (`.specify/goals/<slug>/goal.md`), with the layer-separation and retired-`--scope spec` (exit 2) subjects preserved | closed |
| `tests/contract/test_parallel_lines.py` (3) + `tests/integration/test_parallel_lines.py` (1) | 4 | Seeds write `anchor.md` / `anchor_slug:`; payloads assert `anchor_slug`; the T048 legacy team intentionally keeps `goal_slug` as the recorded legacy-readability case | closed |
| `tests/contract/test_temp_team_schema.py` | 2 | Retargeted to `086-efficient-test-execution`: `binding:`/`owner: human`/`origin`/`anchor_slug`, `goal_slug` absent, `lifecycle_state`/`isolation`/`requested`/`effective`; `run-checks` verdict carries `anchor_slug` | closed |
| `tests/contract/test_stage_class_wiring.py` | 2 | `clarify` → `1126d90a…b771058`, `checklist` → `9bcce326…7f3b794d`; provenance measured with the module's own `strip_wiring` + `_sha256_text`: the only delta is the machine-owned banner fingerprint `4682b9e3…` → `2845f564…` recompiled by WP-03 (5a091f693), and swapping the banner back restores the old pins byte-for-byte. The five other drifting rows are pre-existing baseline reds and were left untouched | closed |
| `tests/integration/test_archive_migration_real_data.py` | 1 | Live target `.specify/anchoring/<slug>/anchor.md` | closed |
| `tests/contract/test_migrate_distribution_assembly.py` | 1 | `COMMAND_BASELINE` 31 → 32 with a dated rationale; cross-checked against `test_migration_distribution.py` (already lists `anchor`, asserts 32) | closed |
| `tests/contract/test_git_workflow_observe.py` (live-surface gap) | 1 | Added probe Object row `skill-manage-anchor-wrapup | skill-wrapup | skill:manage-anchor | wrap-up` to `shared/definitions/probe-definitions.md` (+ mirror via `sync-mirrors.py --write`); `probe-utils.py probes --validate --reconcile` = 0 gaps (129 objects / 86 embeds); `compile-embeds` wrote 0, 85 unchanged | closed |
| `tests/contract/test_docs_step_injection.py` (live-surface gap) | 2 | `anchor` added to `COMPLEX_COMMANDS` (its registered wrap-up face carries the `h-docs-sync-eval` line) and removed from `DOCS_STEP_EXCLUDED` | closed |
| `tests/contract/test_binding_model.py` (live-surface gap) | 1 | The teams landing point is now asserted only for `run-team` / `improve-team`; `manage-goal` asserts `.specify/teams/<slug>` absent and `.specify/goals/<goal-slug>/goal.md` present, cites the Goal owner, and names `migrate-archive` + `/speckit.anchor` as the Anchor-side refusal | closed |
| `tests/contract/test_summary_trigger.py` (live-surface gap) | 2 | Pointer moved to `.specify/anchoring/<anchor-slug>/summary/`; the test additionally asserts the retired `.specify/goal/` form is absent | closed |
| `tests/contract/test_decision_tension_contract.py` (workspace residue) | 1 | `pointer_base` skips ancestors named `.specify`, so the pre-existing untracked `.specify/.specify/` self-match no longer hijacks path resolution; the artifact was **not** deleted | closed |
| `tests/contract/test_isomorphism_map.py` (workspace residue) | 1 | `REPO_ROOT/.specify/.tmp` added to `SCAN_SKIP_PATHS` as the sanctioned agent-scratch root (mid-run sandboxes are not document surfaces) | closed |
| `tests/contract/test_resident_backfill.py` | 2 | Test aligned to the new model (`anchor.md`, sensor glob `*/anchor.md`, incomplete fixture and mutation victim renamed) — and the aligned subject then **fails on the engine**, see § 3 | **blocked** |

**Suite-time new id outside the 37** (self-inflicted, repaired after the run):
`tests/contract/test_inprocess_conversion_contract.py::test_c001_every_covered_file_classifies_all_of_its_sites`
went red because the rewritten temp-goal module collapsed four classified subprocess call
sites into one `_run` helper (and dropped the name
`test_goal_engine_validates_the_archive_definition` that the 098 census carries as a keep
row). Repair, inside `tests/**`: the helper was removed, calls were inlined into their
owning tests, and the test name was restored. Re-verified by
`bash scripts/bash/run-tests.sh tests/contract/test_temp_goal_contract.py tests/contract/test_inprocess_conversion_contract.py -q`
→ **16 passed, 1 failed**, the single failure being the pre-existing baseline id
`test_c006_the_full_tree_scan_names_its_uncovered_files`. No second full suite was run:
the assignment's closure-repair rerun was already spent, and the repair is proven by the
targeted module pair.

## 3. Residual: 2 blocked ids — out-of-territory engine defect

- **Failing ids**: `tests/contract/test_resident_backfill.py::test_every_archive_resident_carries_a_binding_after_backfill`,
  `tests/contract/test_resident_backfill.py::test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding`.
- **Defect**: `scripts/python/goal-utils.py:2528 _resident_definitions` enumerates archive
  residents with `(repo_root / ARCHIVE_DIRNAME).glob("*/goal.md")` — the retired filename —
  while every other path in the engine resolves `definition_filename("anchor")` →
  `anchor.md` (`_path_for_kind`, `binding_payload`), and the sibling
  `_anchor_layer_contains` (line 186) documents the intended either-filename rule
  (`("anchor.md", "goal.md")`). Consequence: an `anchor.md` resident is invisible to
  `backfill-bindings`, so C-112's "every unbound archive resident gets a binding" claim is
  violated.
- **Live proof**: `.specify/anchoring/visualization-skill-selection/anchor.md` carries no
  `binding:` block, and `goal-utils.py backfill-bindings --dry-run --json` plans **zero**
  `kind: "goal"` rows (it lists teams only). Captured in
  `anomaly-resident-backfill-wp06b-2026-11-12.txt`.
- **Fix** (2 lines, not applied): enumerate
  `definition_filename("anchor")` in addition to the legacy `goal.md` (dedupe by slug),
  mirroring `_anchor_layer_contains`. Out of this package's write territory
  (`tests/**`, `shared/definitions/probe-definitions.md` + compile,
  `shared/definitions/anchor-definitions.md`, the summary literal owner, the spec's
  coverage baseline / verification / registry / detail / evidence / task checkboxes).
- **Not weakened**: the aligned test keeps the same subject (every archive resident is
  bound after one backfill; a second backfill writes nothing and refuses an incomplete
  heading). Deleting or relaxing it would hide a real product gap.

## 4. T004 coverage baseline (frozen)

- **Command**: `python scripts/python/account-clause-coverage.py --freeze --spec-dir .specify/specs/101-anchor-goal-realignment --corpus-root .specify/specs`
  → rc 0, redirected to `coverage-baseline.txt` (675 lines: header + 673 frozen names;
  base-sha `b9f6a0edb`; 309 files = 201 parsed + 108 named).
- **Correction disclosed**: the task text says `--corpus-root` points at the repo root, but
  the engine iterates `<corpus-root>/*/contracts/` non-recursively; the repo root contains
  no such directories and the run aborts with "no contract files found". The corpus of spec
  dirs is `.specify/specs` (the engine's own default and its documented semantic), and that
  is the value used.
- **Live accounting against it**: `python scripts/python/account-clause-coverage.py --spec-dir .specify/specs/101-anchor-goal-realignment --corpus-root .specify/specs`
  → rc 1. 722 uncovered clause names, of which **673 are baseline-internal** and **49 are
  beyond the baseline — all 49 are this feature's own contract clauses**
  (`101-.../contracts/*.md#C-1…C-49`) with no `[green:]` claim surface in `tasks.md`
  (claimed clauses 0). Uncovered FRs 48. **No other spec gained an uncovered clause
  relative to the frozen baseline** — the FR-071 comparison is now measurable and shows no
  regression outside this feature's own unclaimed clauses.

## 5. Guard and delivery readings

| Reading | Value | Evidence |
|---|---|---|
| Mirror check | ok — shared/ == .specify/shared/ (114 files byte-identical), all five projections ok | run 2026-11-12 in this package (rc 0) |
| Command-copy check | ok — all per-tool command copies match source templates | rc 0 |
| Residue scan C1–C7 | **all 0** (`{"C1":0,"C2":0,"C3":0,"C4":0,"C5":0,"C6":0,"C7":0}`) | module `tests/contract/test_live_semantic_residue.py` via its own `declaration`/`scan_tree` on the live tree |
| Feature smoke | rc 0 — **43 passed in 12.85 s** | `final-smoke-wp06b-2026-11-12.txt` |
| Touched-module record | **11 failed / 274 passed** — all 11 reds are baseline ids except the 2 blocked resident ids (`comm -13` against `suite-baseline-entry.txt`) | `implement-wp06b-targeted-tests.txt` |

## 6. Wrap-up engines (`skill:implement-feature`, `r20261112T064607Z-b101`)

All three ran and each reported **duplicate** for this (unit, run) — duplicates count as
satisfied, no second row written:

| Engine | Reading | Evidence |
|---|---|---|
| `run-determination.py --action determine --complexity complex --json` | rc 0, `duplicate: true` | `wrap-up-determine-wp06b-2026-11-12.json` |
| `exec-quant.py --action collect --unit-type skill` | rc 0, `duplicate record ...; no second row written` | `wrap-up-execquant-wp06b-2026-11-12.json` |
| `feedback-utils.py --action record --unit-type skill` | rc 0, `id 20261112T121643Z-skill-implement-feature`, `duplicate: true`, `count_since_submission` 485, `should_prompt` true | `wrap-up-feedback-wp06b-2026-11-12.json` |

## 7. Disclosed observations (not smoothed over)

- **One suite run, one post-suite repair.** The final suite was executed after all
  in-territory alignments, but before the census-shape repair of § 2's last paragraph;
  that repair is verified by a targeted module pair only. The suite-time new set is
  therefore 3 ids, not 2.
- **The 2 blocked ids are a decision, not a correction** (fast-fail): the fix belongs to
  `scripts/python/goal-utils.py`, outside the declared write territory; the run reports
  path + evidence and stops.
- **Working tree at wrap-up**: only `coverage-baseline.txt` was untracked at suite time;
  the touched test/owner edits are committed as `101cce5e4`. `.specify/.specify/` was not
  deleted; `.specify/.tmp` was excluded as the sanctioned scratch root; `smoke-081.txt`
  was committed by that same in-gap commit and was not reverted.
- **12 live `team.md` `forbidden_paths`** still list `.specify/goal/**` — the recorded
  classification residual, unchanged.
- **SC-008 build limb** remains `not-evaluated` (EP-006 pre-existing Hugo failure).
