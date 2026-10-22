# Research — 067-loop-efficiency-hardening, test-suite slimming (Phase 0)

**Date**: 2026-10-22 · **Stage**: plan (P3-plan-test-slimming) · **Scope**: User Story 5
design inputs (FR-011…FR-021, SC-006…SC-010). Full-run facts are dated records from
`test-evidence/baseline-full-2026-10-22.md`; probe evidence produced this stage is in
`test-evidence/plan-probes-2026-10-22.md` (P-1…P-5). No full-suite run happened in this
stage; no pass/fail is claimed for unexecuted tests.

## B. Evidence base

- **B-1 Baseline (authoritative, dated)**: complete run 750 s wall / 748.56 s pytest;
  83 failed / 4467 passed / 1 skipped; 4553 collected (contract 3428 / unit 734 /
  integration 391). Slowest 50 = 298.2 s (≈40% of wall): admission_check 18,
  worktree queue 6, proactive trigger 4, trigger telemetry 3, workspace isolation 3,
  plus one 28.21 s self-test. Failure set: 83 names, 50 with mirror/parity/sync/drift/
  distribution markers, 33 others (gate-total pins, exec-quant, 3 loop-state cases).
- **B-2 Host cost structure (probe, this stage)**: plain spawn ~10 ms, `git` CLI ~29 ms,
  interpreter start ~55 ms — too small to explain 3–9 s tests. The dominant unit cost on
  this host is the global git `core.hooksPath` security scanner: ≈0.9 s per fixture
  commit (0.96 s with hooks vs 0.077 s with hooks disabled). 52 commit call sites across
  30+ test files (plus engine scripts committing inside fixture repos) put that tax on
  every slow-test family. Admission-check probe: call phase 2.93–9.62 s with ≈2.6 s CPU
  for the whole probe — waiting, not computing.
- **B-3 Suite shape**: 298 test files; per-case cost is dominated by per-test subprocess
  cold starts (110 files match subprocess/CliRunner) and per-test workspace copies
  (12 files match copytree), per the reproducible counts in
  `notes/test-slimming-scope-2026-10-22.md`. An in-process engine import pattern
  (`importlib.util.spec_from_file_location`) already exists in 5+ unit/contract files.
- **B-4 Mirror-test landscape**: 44 pure byte-identity/parity test functions across ~40
  contract files; the pair inventory is owned by `scripts/python/sync-mirrors.py`
  (`MIRROR_PAIRS` table, `compare_pair`, `--check` exit 2). Roughly 50 of the 83 baseline
  failures are mirror-marker tests — i.e. the drift they detect is real, pre-existing,
  and mechanically repairable by the sync engine, not by touching the tests.
- **B-5 Existing runner contract**: `scripts/bash/run-tests.sh` resolves the interpreter,
  passes args through to pytest, supports `--names-out` (sorted FAILED name list), exit
  code = pytest's result. Any pytest arg (including an optional parallel flag) passes
  through unchanged; default path is serial.

## R. Decisions (each: choice, rationale, rejected alternatives)

- **R-1 Fixture-commit hook neutralization (biggest cross-cutting win, lowest risk)**.
  Tests build throwaway fixture repos; no assertion exercises the host security scanner.
  A single autouse fixture (tests-side conftest) points `GIT_CONFIG_GLOBAL` /
  `GIT_CONFIG_SYSTEM` at empty temp files for the test process, so every git subprocess
  (tests and engine scripts alike) skips the ~0.9 s/commit hook tax. Rejected: per-call
  `-c core.hooksPath=` edits in 30+ files (diff noise, easily missed on new tests);
  disabling hooks host-wide (out of scope, host policy). Risk: some test may depend on
  global git config; the implement-baseline slot run is the verification point, and the
  fixture can scope the env override narrowly if a conflict appears.
- **R-2 In-process engine invocation for engine-loop tests** (trigger telemetry's 60+
  engine subprocess calls; admission-check's per-test script runs). Import the engine
  module via the existing importlib pattern and call its action/entry function directly,
  keeping 1–2 subprocess cases per engine to pin the CLI contract (exit codes, argv
  surface). Rejected: converting everything (loses the real-CLI pin); keeping
  subprocesses (the loop tests' cost scales with spawn count). Risk: in-process global
  state leaks between actions — mitigated by per-case module reload or explicit reset,
  preserving FR-016 isolation semantics.
- **R-3 Module-scoped fixture repos where tests do not mutate shared state**; where they
  do, per-test clones of a module-scoped base repo (clone after the base commit, before
  any mutation). Workspace-copy fixtures should use platform clone/copy-on-write where
  available (APFS `clonefile` with a plain-`copy` fallback), which is behavior-neutral.
  Rejected: session-scope for mutating fixtures (cross-test pollution, FR-016 violation).
- **R-4 Table-driven consolidation of matrix-shaped tests** (e.g. admission boundary
  rows — the file already has one parametrized case — extended to sibling shape cases;
  proactive-trigger per-tool-key loops already dict-driven internally). Each merged case
  keeps per-row assertions and row-encoding parametrize ids (FR-014/FR-020).
- **R-5 One shared parametrized mirror-parity suite, table derived from the engine**:
  import `sync-mirrors.py`'s pair inventory and assert `compare_pair`-equivalent byte
  identity per pair, with parametrize ids carrying the pair path (node id stays
  locatable). Per-file byte-identity-only test functions are then removed file-by-file,
  each with a ledger row (FR-015) pointing at the suite id. Tests that assert MORE than
  byte identity (section sets, counts, wiring) keep their extra assertions where they
  live; only the redundant byte-compare collapses. Pin strength rises (all engine pairs
  covered, none missable) — FR-018 satisfied; the 50 baseline-failing mirror tests keep
  failing in the suite until the drift is synced, exactly matching the relative-baseline
  semantics of SC-008.
- **R-6 Baseline failure triage is bounded and two-class**: (class 1, deterministic
  repair) mirror/sync/drift/distribution markers — repair by running the sync engine
  (`--write` scoped to drifted pairs), never by editing tests; the sync itself is the
  "fix", and any pair whose source is mid-flight from another feature is registered as
  pre-existing debt instead of being synced blind. (class 2, case-level) gate-total pins,
  exec-quant, loop-state — each name gets a triage row: stale-pin-with-owner-fact (fix
  pin to the owner's current value, rationale recorded per FR-018), real regression (fix
  mechanism), or explicit pre-existing debt (dated record under test-evidence/ per
  SC-008). Deleting a failing test is never a disposition (FR-015/SC-008).
- **R-7 Parallel execution: admissible, NOT adopted in this spec's fixed measurement
  command.** Rationale: (a) R-1…R-4 are required regardless and the top-50 concentration
  arithmetic (750 s − ~200–250 s hook/spawn recovery − ~30 s collection/file-merge
  recovery − remaining single-test fixes) projects the serial post-slimming run into the
  ~450–550 s band, under the 600 s budget but with honest uncertainty; (b) parallel
  safety across 298 files cannot be verified without full-suite runs this stage is
  forbidden to make, and FR-017(b) isolation repairs would land on the critical path
  unbounded; (c) clarify admitted xdist as optional — FR-017's default branch is
  "reach the budget by equivalent means"; (d) adopting parallel would also charge an
  extra serial-availability proof (FR-017(c)) to a slot. Contingency, pinned now: if the
  post-consolidation serial measurement at the closure slot exceeds 600 s, the
  requirements Edge Case applies — record the dated evidence and take an explicit scope
  revision / clarify escalation for a parallel fixed command; a silent command change or
  a quiet subset run is forbidden. Serial fallback proof obligation (FR-017(c)) therefore
  does not arise in this spec.
- **R-8 Measurement command pinned exactly as the clarify protocol defines it** (cold
  cache → fixed runner command → wrapper epoch wall clock → dated evidence record); no
  plan-stage change to the protocol file. See `contracts/measurement.md`.
- **R-9 Ledger audit join stays a deterministic inline procedure, not new machinery**:
  regenerate the post id list with the same collect method, `comm -23` against the
  baseline list, join each missing id against ledger rows (case rows by full node id,
  file rows by declared prefix expansion) with a small inline script text fixed in
  `contracts/consolidation-ledger.md`. Constitution IX: no new repo script, no new
  tracking system.
- **R-10 Out-of-scope-but-recorded**: the 28.21 s watch-target self-test pays real-time
  sleeps inside a script this spec must not modify (delivery surface, FR-021). It stays
  as fixed cost; a script-side `--self-test` scale knob is recorded as a candidate for a
  future spec, not implemented here.

## Open questions carried to tasks/implement

- Exact per-file split between R-2 (in-process) and R-3 (fixture reuse) for the mid-tier
  slow files — decided per file at tasks time with the hypotheses table in plan.md §W2
  as the input; each conversion keeps a subprocess-level CLI-pin case.
- Which of the 33 non-mirror baseline failures are stale pins vs real regressions —
  triaged name-by-name at implement start against owner facts (R-6 class 2 procedure).
