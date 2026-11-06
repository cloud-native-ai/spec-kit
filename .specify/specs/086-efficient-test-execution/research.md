# Phase 0 Research — Feature 086 Efficient Test Execution (Concurrent by Default)

Standalone research artifact: the pass carries a measured baseline (eight rows), ten decisions, and a
re-measure list for the implementation stages. Every number below was produced by a command run in this
repository on 2026-11-06; nothing is recalled.

## 1. Measured Baseline

| ID | Fact | Value | Command / source (verbatim) |
|----|------|-------|------------------------------|
| B-1 | Full suite, serial, post-pull tree | 7475 passed / **19 failed** / 7 skipped in **1031.48 s** (0:17:11), exit 1 | `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/baseline-failed.txt -q`; header line `# test runner: .venv/bin/python -m pytest -q`; 19 name lines in the list |
| B-2 | Full suite, parallel, same tree, same runner, same `--names-out` | 7474 passed / **20 failed** / 7 skipped in **201.87 s** (0:03:21), exit 1 | `bash scripts/bash/run-tests.sh -n auto --names-out .specify/.tmp/086/parallel-failed.txt -q`; header line `# test runner: .venv/bin/python -m pytest -n auto -q`; 20 name lines |
| B-3 | Speedup | **5.1×** (1031.48 / 201.87) | Derived from B-1 and B-2 |
| B-4 | New failure names in parallel vs serial | **1**: `tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest` | `comm -13 .specify/.tmp/086/baseline-failed.txt .specify/.tmp/086/parallel-failed.txt` (re-run during the plan stage, output exactly one line) |
| B-5 | Failure names recovered in parallel | **0** | `comm -23 .specify/.tmp/086/baseline-failed.txt .specify/.tmp/086/parallel-failed.txt` (empty) |
| B-6 | Host measurement environment | CPython **3.14.6**, pytest **9.2.0**, pytest-xdist **3.8.0**, macOS **arm64**, **18** logical CPUs | `.venv/bin/python --version`; `.venv/bin/python -m pytest --version`; `.venv/bin/python -m pip show pytest-xdist`; `python3 -c "import os; print(os.cpu_count())"` → `18`; `uname -m` → `arm64` |
| B-7 | Mirror drift before any edit | **zero** on all six pairs | `python3 scripts/python/sync-mirrors.py --check` → `templates` 22 ok, `skills/external` 415 ok, `skills/internal` 138 ok, `agents` 16 ok, `scripts` 121 ok, `shared` 94 ok |
| B-8 | Governance surface sizes before the change | live constitution v1.16.0 with **19** principles; template 18; MUST-include **11**; double-landing watchlist **6**; instructions live **33,357 B / 33 sections**, template **28,930 B / 32 sections**; budget literal `INSTRUCTIONS_BUDGET_BYTES=34816` in `scripts/bash/generate-instructions.sh:53` | `grep -nE '^### [IVXLC0-9]+\. ' .specify/memory/constitution.md` (19 hits); `grep -cE '^## ' .specify/instructions.md` → 33; `grep -cE '^## ' templates/instructions-template.md` → 32; `wc -c` on both files; `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh`; watchlist length read from `DOUBLE_LANDING_WATCHLIST` in `tests/contract/test_constitution_double_landing.py` |
| B-9 | Gate scan at plan time | `total 27`, `violations 0`; frozen baseline file records `confirmationGates.total = 23` | `python3 .specify/scripts/python/scan-confirmation-gates.py --root . --json > .specify/.tmp/086/gate-scan-baseline.json`; `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` |

## 2. Decisions

### R-1 — Default mode is decided inside the runner, from an interpreter probe

**Question**: how does the runner know whether a parallel engine is available, without paying for a full
import on every invocation?

**Decision**: the runner probes once, with the interpreter it already resolved:
`"$PY" -c 'import xdist'`. Success → parallel default. Failure → serial + one named stderr line.

**Why**: `resolve_python` already shells out once (`-m pytest --version`), so a second `-c` probe adds a
comparable cost (tens of milliseconds) and gives an unambiguous, testable predicate. Probing via
`pytest --help | grep xdist` would couple the runner to plugin help text; probing via
`pip show pytest-xdist` would fail under `uv`-managed environments whose metadata layout differs.

**Rejected**: (a) assume parallel and let pytest fail — violates FR-006's "no error exit, no empty run";
(b) require the caller to opt in — violates FR-001's default-parallel requirement.

### R-2 — Worker resolution order is flag > env > auto, validated strictly

**Decision**: `--workers N|auto` (flag) beats `SPECKIT_TEST_WORKERS` (env), which beats the literal `auto`.
A non-numeric, zero, or negative value exits with a named error (`error: --workers expects a positive
integer or "auto"`) instead of falling back to 1 (FR-003).

**Why**: a silent fallback to 1 converts a configuration typo into a 5× slower run that looks healthy;
that is exactly the failure mode this feature exists to remove.

**Rejected**: clamping (`max(1, N)`) — hides the typo; ignoring the env var — breaks the documented
contract and the `quickstart.md` S-2 precedence scenario.

### R-3 — Two-pass mode carries the serial exceptions; one combined list, one combined exit code

**Decision**: in parallel mode the runner runs `pytest -m "not serial" -n <workers>` and then
`pytest -m serial -n0`, captures both stdouts, writes **one** sorted, de-duplicated `--names-out` list and
exits non-zero if either pass failed. A serial pass that collects **zero** tests is success (pytest's
exit code 5 is normalized to 0 **for that pass only**). In serial mode a single all-tests pass runs.

**Why**: FR-011 and A14 require the exception set to be enumerable and the run to stay one run. Splitting
the suite is the only way to keep both properties: the `serial` marker is the enumeration, and combining
the outputs keeps `comm -13` comparable with a serial baseline. Normalizing exit 5 only for the empty
serial pass prevents a spurious failure on a tree where nothing is marked `serial`.

**Rejected**: (a) `--deselect <nodeid>` per exception — unenumerable once the set grows, and it splits the
list over command lines rather than over a marker; (b) `--maxprocesses` tricks — do not express exclusion;
(c) `-p no:xdist` for the serial pass — works, but `-n0` is the documented, version-stable form and is
already how the runner's own tests express "one process".

### R-4 — Nested-run guard keys on `PYTEST_XDIST_WORKER`

**Decision**: if `PYTEST_XDIST_WORKER` is set in the environment, the runner goes serial and prints the
contract's mode line in its `nested` form — `# test runner: mode=serial reason=nested` (contract C-002), with
the worker id carried on the adjacent note line rather than folded into the mode line, so the mode line stays
one machine-readable shape across all three reasons (`data-model.md` E-5). Exit code unchanged.

**Evidence** (EP-005): `xdist/remote.py:417` sets the variable before collection and no cleanup path
deletes it, so a test that shells out to the runner sees it. Without this guard, every subprocess-using
test (167 files) that calls a pytest-running script would fork a second worker pool — the "process
explosion" failure mode.

**Rejected**: detecting nesting by walking the process tree (parent process name) — Linux/macOS
differences, fragile, and it would also fire for unrelated parent processes.

### R-5 — Caller-supplied worker count is never duplicated

**Decision**: scan the caller's arguments for `-n`, `--numprocesses`, `-n<value>`, `-n=<value>`; on a hit,
add nothing (no `-n`, no `--dist`). The caller's own scheduling wins.

**Why**: two `-n` flags on one pytest command line have undefined last-wins behavior that changes between
xdist versions; FR-004 forbids the duplication and US3-4 makes it observable in the printed command.

**Rejected**: overriding the caller with the computed default — silently ignores caller intent.

### R-6 — The stderr header keeps describing the command actually executed

**Decision**: the existing `# test runner: <interpreter> -m pytest <args>` line is preserved verbatim as
the **command** line, and the resolved mode is stated in a second, named line
(`# test runner: mode=parallel workers=<N> dist=load` / `mode=serial reason=<explicit|nested|no-xdist>`).

**Why**: FR-005/US3-5 requires the header to be truthful; a header that printed `-n auto` while the
runner had silently fallen back would be the exact false claim `quickstart.md` S-3 is designed to catch.

**Rejected**: mutating the existing header to include the mode — breaks `tests/integration/
test_sdd_loop_efficiency_regression.py`'s header expectations and any downstream log parser.

### R-7 — The watch-target self-test gets the marker, not a timeout bump

**Decision**: register a `serial` pytest marker; apply it to
`tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`; the runner's two-pass
mode excludes it from the parallel pass and re-runs it serially.

**Why**: the failure is parallel-load-specific (28 s unloaded vs >60 s under `-n auto`), so a timeout bump
would carry the *new* timeout value as a silent policy decision made under unknown load. The marker form
is enumerable (`pytest -m serial --collect-only -q`), reviewable, and reversible. A14 reserves the timeout
fallback for the case where the marker form cannot preserve the list or the exit code — it can.

**Rejected**: `pytest.mark.skipif(os.environ.get("PYTEST_XDIST_WORKER"))` — a host-dependent skip that
disappears from the exit code (FR-010 forbids skip); `pytest.mark.xfail` — asserts nothing.

### R-8 — The gate-scan criterion is "no increase", not "equals 23"

**Decision**: the implementation guard reads "the audit gate total does not increase over the value
measured before the change" (27 at plan time, EP-008), and the pre-existing 4-gate drift between the live
scan (27) and the frozen baseline file (23) is recorded as a known-bad fact rather than repaired here.

**Why**: `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` and
`test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` are **already failing on the serial
baseline** (both names appear in `.specify/.tmp/086/baseline-failed.txt`). Making this feature's criterion
an equality against 23 would (a) require repairing an unrelated feature's frozen baseline inside 086 and
(b) pre-write an expected result that does not hold at the start. Both are outside this feature's declared
boundary (§ Boundary and Ownership of requirements.md).

**Consequence for implement**: the new principle text and the new guideline MUST word their MUSTs so they
add zero gate hits; that is a design constraint, checked by diffing the scan against the stored baseline
JSON. It is **not** a promise to move the total to 23.

### R-9 — Work-package watcher test id corrected

**Question**: the dispatch brief labels the serial-exception test as "test_c24".

**Finding**: the live id is `tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`
(`tests/contract/test_sdd_loop_driver_skill.py:537`), and the Phase 0 name diff (B-4) names `test_c22`. The
literal is grounded in code, so code wins.

**Decision**: use `test_c22_watch_target_hook_selftest` everywhere; this is recorded as an in-passing
correction, not a scope change (the same test, the same disposition).

### R-10 — Tool-reuse gate result: no new tool record

**Lookup**: scanned `.specify/memory/tools/` (10 records: `build-summary-input.py`, `derive-utils.py`,
`evidence-utils.py`, `feedback-utils.py`, `goal-utils.py`, `interview-utils.py`, `refresh-tools.sh`,
`sanitize-utils.py`, `sync-mirrors.py`, `trigger-utils.py`).

**Decision**: the reusable actions this feature needs already have owners and are reused, not re-derived —
`sync-mirrors.py` (mirror regeneration), `generate-instructions.sh` (live instructions generation),
`scan-confirmation-gates.py` (gate measurement), `pre-analyze-check.py` / `decomposition-check.py` /
`overlap-check.py` (stage gates), `audit-test-budget.py` (ledger parsing, being extended in place). The
runner's mode resolution is a new capability with no existing record; per the gate's step 3 that is a
normal miss, and the code is written as part of WP-A1 rather than promoted to a Tool record speculatively.
No Tool record is created by this feature.

**Same-author disclosure** (`shared/workflow/objective-analysis-gate.md`): the gate fires — the artifacts
scored by this plan were authored in the same run. The fresh-context subagent dispatch was attempted from
the plan stage and was unavailable in this carrier (the executor has no subagent dispatch surface), so the
scoring was performed as a **direct bounded read** and is marked as such: every Constitution Check row and
every Post-Generation Quality Gate item in this artifact set is `(detected: direct read, subagent
unavailable)`. Validation therefore rests on the mechanical gates actually run (`validate-decision-tensions.py`,
`pre-analyze-check.py --stage plan`, `decomposition-check.py --mode plan`,
`doc-consistency-check.py --action structure`, the two mirror readings), not on a second reader.

## 3. Re-measure List (consumed by `/speckit.tasks` and `/speckit.implement`)

These are the facts this research asserts that a later stage MUST re-measure rather than inherit:

| # | Fact asserted here | Re-measure with |
|---|--------------------|-----------------|
| 1 | Serial baseline name list has 19 entries (B-1) | `wc -l .specify/.tmp/086/baseline-failed.txt` before any comparison |
| 2 | Parallel name list has 20 entries, one new name (B-2, B-4) | `comm -13` / `comm -23` against the *fresh* closure-slot serial baseline, not against `.specify/.tmp/086/*` (A9) |
| 3 | xdist 3.8.0 / pytest 9.2.0 on Python 3.14.6, 18 logical CPUs (B-6) | `.venv/bin/python -m pytest --version`; `pip show pytest-xdist`; `os.cpu_count()` — record verbatim into `test-evidence/` |
| 4 | Zero mirror drift before the edit (B-7) | `python3 scripts/python/sync-mirrors.py --check` before the first mirror write |
| 5 | Live constitution 19 principles / template 18 / MUST-include 11 / watchlist 6 (B-8) | the same greps the guards use, before editing |
| 6 | Instructions live 33 sections / 33,357 B; template 32 sections / 28,930 B; budget 34,816 B (B-8) | `grep -cE '^## '` on both files, `wc -c` on both, `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` |
| 7 | Gate total 27 live vs 23 frozen, both guard tests already red (B-9, R-8) | `scan-confirmation-gates.py --root . --json`; and confirm both guard names are still in the baseline failed-name list |
| 8 | The watch-target test id is `test_c22_watch_target_hook_selftest` (R-9) | `grep -n "def test_c2[0-9]_watch" tests/contract/test_sdd_loop_driver_skill.py` |
| 9 | Per-worker `basetemp` and `PYTEST_XDIST_WORKER` lifetime (EP-004, EP-005) | a throwaway parallel run collecting `os.environ.get("PYTEST_XDIST_WORKER")` and `str(tmp_path)` from two tests, asserting distinct values |

## 4. Alternatives Considered and Not Adopted

| Alternative | Why not |
|-------------|---------|
| `pytest-parallel` / `pytest-forked` / `pytest-xprocess` | Not installed, not maintained at the same cadence, and xdist is the de-facto engine the framework's own docs and 067's research already name |
| `--dist loadscope` / `loadfile` as the default | Both reduce parallel spread for this suite's shape (many small files, few heavy ones); A13 requires same-command evidence before a switch. Recorded as a tuning experiment in `quickstart.md` S-5 |
| A CI-only parallel path (serial locally) | Satisfies nobody: the user's complaint is local developer wall-clock |
| Project-level `addopts` (T-001 antithesis) | Rejected for the reasons in `plan.md` T-001 |
| Making the `serial` marker a `conftest.py` autouse skip | Skips are forbidden by FR-010; the marker must be visible as an *exclusion from the parallel pass*, not as a silent skip |
| Raising the global instructions budget pre-emptively | R-4/R-5 measure first; the budget moves only if the measured size exceeds it (clarify ruling 3) |
