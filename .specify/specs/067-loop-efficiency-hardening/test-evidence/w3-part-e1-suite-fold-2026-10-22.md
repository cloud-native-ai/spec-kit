# Part E1 — Mirror-Parity Suite + Fold Batches 1–2 (T019–T021) — 2026-10-22

Dated record for implement part E1 of spec 067 (plan §Implementation Slicing E,
W3 main piece + W1 fold batches 1–2). Every number below is measured from the
commands listed in § Command log; nothing here claims an unexecuted run.

## T019 — Shared parametrized mirror-parity suite

- File: `tests/contract/test_mirror_parity_suite.py` (new).
- Table source = the engine: importlib-loads `scripts/python/sync-mirrors.py`
  and derives every param from `MIRROR_PAIRS` + `iter_files` (house loading
  pattern: `tests/contract/helpers_prompt_assets.py`); no pair restated
  (One Source of Truth / Tool Reuse).
- Parametrization: 6 pairs → **717 per-file byte-identity params** (id carries
  `source→mirror`, FR-020) + **6 pair-level extras params** at exact engine
  strictness (strict `scripts` pair fails on ORPHANs; lenient pairs note-only —
  not tightened). Total 723 tests.
- Scope note: `templates/commands` per-tool copies are not a `MIRROR_PAIRS`
  entry (engine CLI delegates to `regen-command-copies.py`) — outside this
  pair-table suite by design.
- Honesty note: suite run 1 failed 717/717 — a suite-side defect (compared the
  source ROOT instead of `src/rel`); fixed in the same working session before
  any fold landed. Run 1 is recorded here rather than silently dropped.

### Suite run 2 (authoritative; verbatim counts)

`bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py -q --durations=0`
→ exit 1, **202 failed / 521 passed** (1.35 s). Expected red: current real
mirror drift, SC-008 relative-semantics input; sync fix owned by T023 (not
executed in this part — no mirror was synced).

Failure-set equivalence (mechanical check): suite failing params ↔ engine
`python3 scripts/python/sync-mirrors.py --check` DIFF lines = **202 = 202, sets
equal** (engine exit 2). Per-pair failing params:

| pair | failing file params |
|---|---|
| agents → .specify/agents/templates | 2 |
| scripts → .specify/scripts | 26 |
| shared → .specify/shared | 37 |
| skills/external → .specify/skills | 62 |
| skills/internal → .specify/skills/internal | 75 |
| templates → .specify/templates | 0 (green) |

All 6 pair-extras params pass (no ORPHANs).

## Candidate scan — actual criteria and counts (wide 口径)

- Wide criteria (plan-probes P-5 regex) applied to test-function definition
  lines under `tests/contract/`: `byte_identical|byte-identical|mirror.*identical|mirror parity|byte_equivalent`
  → **36 candidate test functions in 33 files**.
- P-5's "44" is explained: it counted regex-matching LINES (comments, assert
  messages, helper defs such as `assert_dirs_byte_equivalent`), not distinct
  test functions; the def-line scan yields 36.
- The narrow list `mirror-parity-candidates-2026-10-22.txt` (36 entries)
  matches the same 36 functions 1:1 (one stale line number:
  `test_proactive_trigger_section.py` 447 → 460, shifted by part-D edits).
- Per-function inspection (逐函数核对): 35 foldable — 32 pure byte-identity
  functions (whole-function fold) + 3 with extra assertions beyond byte
  compare (`test_summarize_project_prompt_assets.py::test_mirror_is_byte_equivalent`
  — tree file-set equality; `test_trigger_seed_derivation.py::test_c1_…` —
  seed JSON validity; `test_user_facing_comprehension_section.py::test_c2_…` —
  heading-once + pointer pins) → extra-assertion cases are batch-3 (T022)
  material, untouched in this part. 1 wide hit excluded:
  `test_feedback_probe_cli.py::test_map_is_deterministic_byte_identical` —
  engine-map output determinism in a tmp workspace, no mirror involved; kept
  untouched.

## Batch split (file-path dictionary order over the 36 candidates)

- Batch 1 (T020) = candidates 1–11 → **11 pure folds** (candidate 12 = the
  excluded determinism test).
- Batch 2 (T021) = candidates 13–24 → **12 pure folds**.
- Batch 3 (T022, next part) = candidates 25–36 (incl. the 3 extra-assertion
  cases and the `*aggregate*` self-improvement/token-efficiency families).

## T020/T021 — folds landed

- 23 functions removed across 20 files (batch 1: 10 files; batch 2: 10 files;
  `test_progress_reporting.py` and `test_evidence_step_conformance.py` carried
  two removals each — 11 + 12 functions total).
- Ledger: rows 46–68 appended to `test-evidence/test-consolidation-ledger.md`
  — **23 case-merge rows = 23 removed functions**; each row cites the exact
  suite param id(s) (verified to exist in the suite, generated mechanically
  from the engine table). Commit column = `pending` at first commit, backfilled
  after.
- No partial fold and no assertion-literal weakening landed in this part; pin
  strength (LED-07 / FR-018): removed tests' byte assertions are carried by
  suite byte compares (≥ the two removed `read_text`-equality compares); the
  `sdd-loop-driver` fold is covered by a 28-param superset of its 15 pinned
  files; sibling `test_c18_mirror_pair_no_drift` (not a candidate) keeps the
  same loop in file.

## Dependent-pin repair (fast-fail correction, disclosed)

- Targeted run 1 (suite + 20 touched files): 216 failed / 1214 passed. 202 =
  suite drift; 13 non-suite failures all IN the in-stage baseline
  (`baseline-failures-2026-10-22-implement-start.txt`); 1 NEW name:
  `test_sdd_loop_driver_skill.py::test_c16_contract_test_file_complete`.
- Cause: c16 pins "one test function per clause C-1..C-19" in that file — a
  wiring pin dependent on the removed `test_c12_` name, invisible to the
  name-based candidate scan.
- Repair (one reading consistent with recorded intent; local; reversible):
  C-12 arm re-anchored to the consolidation face — original literal kept as
  first arm, added arm requires `skills/external/sdd-loop-driver/` parity
  params in the suite. Strength preserved-or-increased; ledger row 69
  (`retained`) records it; row 67 cross-references.
- Re-check: suite + `test_sdd_loop_driver_skill.py` → **202 failed / 546
  passed, 0 non-suite failures**.

## Baseline traceability

- Baseline failures in the 20 touched files: 30. Absent from the targeted run:
  exactly the 17 folded ids that were baseline reds — their drift is carried by
  the suite's red params (failure set == engine DIFF set, proven above). No
  baseline failure went green by removal; no count-pin improved silently.
- Final targeted state: only the 202 known-drift suite params fail; every
  failure maps to a `sync-mirrors.py --check` DIFF line.

## Command log (all runs in this part)

1. `python3 scripts/python/sync-mirrors.py --check` (read-only) → exit 2, 202 DIFF / 0 MISS / 0 ORPHAN; templates ok (22 files).
2. `bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py -q --durations=0` (run 1, suite bug) → 717 failed / 6 passed.
3. Same command (run 2, after fix) → 202 failed / 521 passed.
4. `--collect-only -q` batch-1 files → 304 collected.
5. `--collect-only -q` batch-2 files → 403 collected.
6. Targeted: suite + 20 touched files `-q --durations=0` → 216 failed / 1214 passed (51.22 s).
7. Re-check: suite + `test_sdd_loop_driver_skill.py` → 202 failed / 546 passed (26.03 s).

Not run: full suite (slots owned by T007/T034); any `--write` sync (T023);
batch-3 folds (T022).

## Residual risks

- Suite red on 202 params until T023 syncs — expected, in-register.
- `templates/commands` per-tool copies remain unpinned by this suite (engine
  delegation surface, unchanged semantics).
- pytest deprecation warning (`TestCE3Doctor` class-scoped fixture,
  test_evidence_utils_cli.py) pre-existing, untouched.

## Commits

- Part E1 artifact commit: pending (backfilled below after commit).
- Ledger commit-hash backfill commit: pending.
