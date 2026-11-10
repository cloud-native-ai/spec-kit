# Phase 0 Research — 098 Suite Speed Optimizations

**Feature**: `098-suite-speed-optimizations` → Feature 086 Efficient Test Execution (Concurrent by Default)
**Date**: 2026-11-10
**Method**: read-only probes plus targeted runner invocations; every command and its complete output is recorded under `test-evidence/`. No full-suite run was performed in this phase (two-slot budget discipline).

## B. Measurements taken in this phase

| id | measurement | evidence |
|----|-------------|----------|
| B-1 | Interpreter/pytest/xdist: `python 3.11.11`, `pytest 8.4.2`, `xdist 3.8.0`; full-tree collection `8543 tests collected`; `-m slow` collects nothing today and exits 5 | `test-evidence/plan-baseline-probe.txt` |
| B-2 | Existing runner contract suite is green BEFORE any change: `40 passed in 13.90s`, exit 0 (`--workers 4`) | `test-evidence/runner-contract-pretest.txt` |
| B-3 | `tests/contract/test_client_metrics.py`: `16 passed in 6.62s` with 8 × `time.sleep(1.1)`; the file runs across 2 xdist workers, so fixed sleeps cost ~4.4 s of wall time per worker pair | `test-evidence/targeted-pretest-baseline.txt` |
| B-4 | Corpus pair `test_coverage_receipt.py + test_clause_coverage.py`: `2 failed, 62 passed in 31.92s`. The two failures (`test_c5_gate_budget_is_unchanged_by_the_owner_document`, `test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census`) are PRE-EXISTING baseline failures, not caused by this spec (098 adds no YAML contract; the pin says `re-derive notes/clause-form-census.md`) | `test-evidence/targeted-pretest-baseline.txt` |
| B-5 | Writing an evidence file under `.specify/specs` WHILE a corpus-scanning test runs flips `test_c20`'s before/after md5 and reddens it (3 failed incl. `test_c20`); the same run is green when output is written outside the corpus (2 pre-existing failures, 62 passed) | `test-evidence/corpus-write-hazard.txt` vs `test-evidence/targeted-pretest-baseline.txt` |
| B-6 | Session-scoped fixtures build once per xdist worker: 3 tests on 2 workers produced exactly 2 builds (`built-gw0`, `built-gw1`) | `test-evidence/session-fixture-probe.txt` |
| B-7 | Real-corpus consumers: `test_clause_coverage.py` runs `account()` over the real `.specify/specs` in 5 tests (c10, c20, c26, c27, `form_exit_code_table`) plus c4's glob and c6's grep; `test_coverage_receipt.py` reads only a 071 requirements glob plus three template files. Mutation tests in both files operate exclusively on `tmp_path` corpora | Explore census (2026-11-10) |
| B-8 | Sleep scope: `test_client_metrics.py` 8; `test_sdd_loop_efficiency_runner.py` 1 (0.2 s polling interval with a 30 s deadline — already deadline-bounded); `test_session_kill_reattach.py` 2; `test_line_envelope_contract.py` 2; `test_feedback_probe_cli.py` 1; `test_store_state_protocol.py` 2. A shared `wait_until(predicate, timeout, interval)` helper already exists at `tests/fixtures/line_fixtures.py:396` | `plan-baseline-probe.txt` + Explore |
| B-9 | Subprocess census: 498 source lines / 495 real calls / 228 files; targets: ~265 Python-engine invocations, 119 git, 36 bash, ~63 computed argv. Existing in-process precedents: `tests/script_api.py` (CliRunner) and `importlib.util.spec_from_file_location` in 109 test files. Fixture-layer `run_engine`/`run_cli` helpers carry `cwd=`/`env=` and stay subprocess | Explore census (estimates labelled) |
| B-10 | Two-slot budget owner is `.specify/skills/sdd-loop-driver/references/efficiency-model.md` §2 (rows `:91`/`:92`); restatements in `stage-prompts.md:165`/`:206`. `audit-test-budget.py` ignores any token starting with `-` that is not a value flag, so `--full` classifies as a flag and the command remains a full-suite run with no parser change | Explore + source read |

## Probe transcripts

The per-worker session-fixture probe (B-6) and version probes are reproduced in
`test-evidence/plan-baseline-probe.txt`; the session probe source and marker files lived under
`.specify/.tmp/098-probe/` (git-ignored scratch, sanctioned root).

## R. Decisions

### R-1 — Tier semantics and runner composition

- Two tiers, values `fast` and `full`; no second runner and no second selection source (FR-001).
- `fast` is the default when the caller supplies no `-m` and does not request `--full`.
- Composition with the existing serial two-pass model:

| state | parallel pass | serial pass | tier field |
|-------|---------------|-------------|------------|
| fast, no serial members | `-m "not slow"` | — | `tier=fast excluded_slow=N` |
| fast, serial members | `-m "not serial and not slow"` | `-n0 -m "serial and not slow"` | same |
| full, no serial members | (no marker args) | — | `tier=full excluded_slow=0` |
| full, serial members | `-m "not serial"` | `-n0 -m serial` | same |
| caller `-m` (either tier request) | unchanged from 086 | unchanged | `tier=caller excluded_slow=0` |

- `--serial` changes only the execution shape; the tier applies to its single pass (`-n0 -m "not slow"` in fast, `-n0` in full, caller `-m` untouched).

### R-2 — Exclusion count and disclosure

The excluded count is produced by marker enumeration over the caller's selection, exactly as C-011 enumerates `serial`: `pytest --collect-only -q -m slow <caller args>` with `-q/--quiet` normalised away. The collect exits 5 when no member matches, which is treated as zero. The count is never a hardcoded constant. Cost: one extra collection per default-tier run (measured 1.7–11 s cold, ~2 s warm); accepted because the wall-clock ratio target (SC-004) is measured over the full run and the collection is two orders of magnitude cheaper.

### R-3 — Empty selection after exclusion

The named error fires only when the fast tier actually caused the emptiness: a primary pass exits 5 AND the enumerated slow count is greater than zero. The runner then prints `# test runner: error=empty-selection-after-tier-exclusion tier=fast excluded_slow=<n>` and exits 2. When the caller's selection was already empty (slow count 0), pytest's exit 5 is preserved unchanged (C-012 compatibility).

### R-4 — Slow membership registry and guard

Membership is measured, not declared in the requirements: the registry is
`test-evidence/slow-members.md`, a pipe table with the fixed columns `test_id | category | reason | date`.
`category` is closed: `process-boundary` (spawns, waits for, or terminates an external process/queue) or
`corpus-scan` (traverses the whole corpus or multiple spec directories). The guard derives both sides —
the registry rows and `pytest --collect-only -q -m slow` — and asserts exact one-to-one correspondence.
Candidate pools (final membership measured at implement): detached/stage-runner integration tests
(`test_sdd_loop_efficiency_runner.py`, `test_session_kill_reattach.py`) and real-corpus contract tests
(`test_clause_coverage.py` c10/c20/c26/c27/form_exit_code_table).

### R-5 — Session scan cache

- Key: `(session, worker, managed surface)`. Managed surfaces in this slice: `framework-specs-corpus`
  (the `account()` payload over `.specify/specs`) and `framework-root-inputs` (the 071 requirements path
  and the three template texts read by `test_coverage_receipt.py`).
- Carrier: a session-scoped fixture FACTORY in `tests/conftest.py`, cached per `(root, variant)`; the real
  root is the session default, `tmp_path` roots are used by mutation drills. Build count is recorded on the
  fixture value; consumers receive a `copy.deepcopy` so no in-place mutation can leak across tests.
- In-process build: the fixture loads `scripts/python/account-clause-coverage.py` with
  `importlib.util.spec_from_file_location` (existing house pattern) and wraps `_corpus_files` with a
  traversal counter. The five real-corpus tests consume the payload; the CLI/exit-code case
  (`form_exit_code_table`) stays subprocess because its subject is the process contract.
- Mutation drills use tmp corpora and therefore never touch the real corpus; `test_c20`'s byte-identity
  check stays a separate subprocess test (it is the detector for real-corpus writes).

### R-6 — Injected clock for ordering

`scripts/python/feedback-utils.py` reads time only through `now_iso()` and `timestamp_id()` (B-4 source
read: `:125`, `:129`; call sites `:879`, `:881`, `:1056`, `:2071`, `:2075`, `:2089`, `:2168`, `:2293`,
`:2366`). The feature adds one optional global option, `--now <ISO-8601-Z>`, documented in `--help` as a
test-only deterministic clock; when present the two helpers return the injected value (with the same
one-second granularity), when absent behaviour is byte-identical to today. Tests also control file mtimes
explicitly with `os.utime` where the closure rule compares owner-file mtime against entry `created`.
Decision tension T-002 records the rejected alternative (test-side entry rewriting) and its tradeoff.

### R-7 — Event waits

`tests/fixtures/line_fixtures.py::wait_until` is the single wait helper; it takes a predicate, a deadline,
and an interval. The feature lowers its defaults to `timeout=30`, `interval<=0.2` at the call sites that
adopt it, and every adoption asserts the return value with a named failure message. Timeout never maps to
`skip`/`xfail`/retry. Exemption registry (real-time semantics, not synchronization):
`tests/unit/test_line_registry_engine.py` (generated flock holder must outlive a 0.2 s lock timeout) and
`tests/unit/test_concurrency_check_engine.py` (synthetic task duration for a wall-clock comparison).
Polling intervals inside fixture writers are not test synchronization and are out of scope.

### R-8 — In-process conversion classification

Boundary classes (keep, closed set): `cli-contract`, `signal-timeout-interrupt`, `git-external`,
`process-isolation-subject`, `other-interpreter`, `global-state-unrecoverable`, plus `copy-topology`
(calls whose subject is a projected/mirrored copy or a separately installed tree). Converted rows carry the
equivalence route. Fixture helpers (`tests/fixtures/*`) that set `cwd=`/`env=` are retained as
`global-state-unrecoverable`; conversion targets are test-local wrappers that invoke engines with explicit
paths/`--workspace-root` and assert JSON or file effects. The manifest is generated by a deterministic AST
scan at implement; the guard re-scans and requires every discovered call site to be classified.

### R-9 — Two-slot budget surfaces

Three restatements of the slot commands gain `--full` in the same change (owner + two stage-prompt rows),
then the skill mirror is regenerated (`skills/external` → `.specify/skills`). The audit parser needs no
change (B-10). The slot count, timing and order are unchanged.

### R-10 — Same-author verification

The plan artifacts are authored in this session; the Constitution Check and Post-Generation Quality Gate
verdicts are delegated to fresh-context read-only subagents per
`.specify/shared/workflow/objective-analysis-gate.md`, with the same-author condition named in each brief.

## Re-measure list (implement must re-measure, never inherit)

1. Slow membership candidate durations and final membership (B-7 pools).
2. Exclusion-enumeration cost under the real tree after tier injection.
3. Client-metrics wall time before/after at the same worker count.
4. Corpus-pair build count and wall time before/after.
5. Conversion census after the manifest scan (the B-9 numbers are estimates by category).

## Risks carried into the plan

- Writing any file under `.specify/specs` while a full run is in flight reddens `test_c20` (B-5); the
  driver's `--names-out` is written after the passes, but stage evidence must land outside the corpus or
  after the run completes.
- Two pre-existing baseline failures (B-4) mean every full run will name them; comparisons are by name.
- `--now` widens a shipped engine's CLI surface; the contract pins default-off byte equality and `--help`
  documentation.
