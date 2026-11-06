# Dev Setup

1. Clone the repo and create a virtualenv (Python ≥ 3.11 recommended for dev; runtime supports ≥ 3.8):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   ```
   The `dev` extra (declared in `pyproject.toml` → `[project.optional-dependencies]`) installs `pytest` and
   `pytest-xdist`. Nothing in it reaches the CLI's runtime dependency set — `pip install specify-cli` never
   pulls the test tooling. On Python 3.8 the extra installs `pytest` only, because `pytest-xdist` 3.x needs
   ≥ 3.9; the runner then falls back to a serial run and says so (see step 2).
2. Run the test suite and record the baseline (pre-existing failures exist long-term):
   ```bash
   .specify/scripts/bash/run-tests.sh
   ```
   The runner's **default is parallel** (`-n auto --dist load`), so no parallel argument is needed. Its stderr
   tells you what actually ran — `# test runner: mode=parallel workers=<n> dist=load` or
   `# test runner: mode=serial reason=<explicit|nested|no-xdist>`.
   - Full serial pass: `.specify/scripts/bash/run-tests.sh --serial`
   - Worker count: `--workers 8` or `--workers auto`. Precedence is **flag > `SPECKIT_TEST_WORKERS` > `auto`**,
     so `SPECKIT_TEST_WORKERS=8 .specify/scripts/bash/run-tests.sh` works for a whole shell session. A value
     that is neither a positive integer nor `auto` exits non-zero with a named error rather than silently
     running one worker.
   - Parallel engine absent (e.g. Python 3.8, or `pytest-xdist` not installed): the run still completes
     serially and the mode line carries `reason=no-xdist` — never an error, never an empty run.
   - A run started inside a parallel worker (`PYTEST_XDIST_WORKER` set) stays serial with `reason=nested`, so
     no second worker pool is forked.
   - A test that is not parallel-safe is declared with the registered `@pytest.mark.serial` marker; the
     parallel pass excludes it and a serial pass re-runs it, so one `--names-out` list and one exit code still
     cover everything. Enumerate the declared exceptions with
     `pytest -m serial --collect-only -q`.
   - `--names-out <file>` writes the sorted, de-duplicated failure-name list for `comm`-based comparison
     against a recorded baseline.
   The reasoning, the isolation preconditions and the rules for declaring a serial exception are owned by
   `.specify/shared/guidelines/test-execution-efficiency.md` — read it before adding a marker or changing the
   default.
3. Editing command templates? Source of truth is `templates/commands/`; afterwards run:
   ```bash
   python3 scripts/python/regen-command-copies.py --check
   ```
4. Editing skill or shared docs? Mirror-sync map lives in `.specify/instructions.md` (`AGENTS.md`).
