# Test-Slimming Scope Facts — provenance for 067 requirements update (2026-10-22)

Dated record. Input to `.specify/specs/067-loop-efficiency-hardening/requirements.md` (User Story 5 / FR-011…FR-021 / SC-006…SC-010). Not a runtime guarantee. This file records how each scoped fact was obtained and discloses one counting discrepancy. No test was executed for this record; no pass/fail is claimed anywhere in it.

## Verified facts (all measured 2026-10-22, by the requirements-stage executor)

| Fact | Value | Source command / file (as run) |
|---|---|---|
| Canonical full-suite entry | `scripts/bash/run-tests.sh` | file exists; `bash scripts/bash/run-tests.sh --help` prints `# test runner: python -m pytest --help` |
| Interpreter resolved on this host | Python 3.14.6 + pytest 9.1.1 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python --version` and `-m pytest --version`; that venv's `python` is what the runner resolves on PATH |
| Bare `python3 -m pytest` unavailable | confirmed | `python3 -m pytest --version` → `No module named pytest` (CommandLineTools Python 3.9.6) |
| Test file count | 298 | `find tests -name 'test_*.py' -type f | wc -l` |
| Case count | 4553 (contract 3428 / unit 734 / integration 391) | driver inventory, 2026-10-22 dispatch brief; counting command not attached; to be cross-checked against the completed baseline log. Sum check: 3428+734+391 = 4553. |
| Marker registration | only `contract` and `integration` markers declared; unit = unmarked layer | `pyproject.toml` `[tool.pytest.ini_options] markers` |
| 063 targeted-set speed record | 144 cases in 123.64s (~0.86 s/case) | `.specify/specs/063-sdd-loop-efficiency/review.md` (GATE-1 re-run note) and `test-evidence/review.jsonl` stage-status row |
| CI test workflow | none | `ls .github/workflows/` → not found |
| Baseline run in flight | driver-owned, background | `bash scripts/bash/run-tests.sh -q --durations=50` → `notes/baseline-full-2026-10-22.log`; unfinished at spec-update time, not read as evidence, not committed by this part |

## Slow-pattern counting discrepancy (disclosed, not resolved by guessing)

Driver brief (2026-10-22) gave: ~234 test files containing subprocess/CliRunner, 25 containing copytree, 9 containing time.sleep (counting command not recorded). Reproducible counts run for this record (2026-10-22, file counts under `tests/`):

- `grep -rlE "subprocess|CliRunner" tests --include='test_*.py' | wc -l` → 110 (all `.py` under tests/: 116)
- `grep -rl "copytree" tests --include='test_*.py' | wc -l` → 12 (all `.py`: 13)
- `grep -rl "time\.sleep" tests --include='test_*.py' | wc -l` → 6 (all `.py`: 8)

Classification: repair-in-passing (Fast Fail Discipline) — the requirement text records both figures with attribution; both orders of magnitude support the same conclusion (suite cost dominated by per-test subprocess cold starts and workspace copies), so no downstream premise is falsified. The driver's wider figures most likely come from a broader counting command; if the driver's exact command surfaces, update the two rows in one place (here + the spec's 现状锚点 line) — do not leave them diverging silently.

## Scope boundary of this part (P1-requirements-test-scope)

- Allowed files touched: `requirements.md` (in place) + this notes file. Nothing else.
- The baseline log and `state-spine.md` are excluded from the part commit by instruction.
- Open items (parallel dev-only dependency admission, cold/warm cache timing basis, tiering boundary, host口径) are recorded in the spec's Assumptions section for clarify; this part does not decide them.
