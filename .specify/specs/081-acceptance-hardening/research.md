# Phase 0 Research — 081 Stricter Acceptance & Artifact Review

**Owner of the schema this feature introduces**: `shared/workflow/acceptance-hardening.md` (requirements [[STR-017]]). This file records **measurements and rejected alternatives**, not schema — it never becomes a second definition point.

Every fact below was measured on the working tree of branch `081-acceptance-hardening` on 2026-11-03 unless a different date is written on the row.

## R1 — Test-runner preflight (D8)

| Observation | Command actually run | Result |
|---|---|---|
| Project interpreter | `.venv/bin/python --version` | `Python 3.14.6` |
| pytest present but unusable | `.venv/bin/python -m pytest --version` | died at import: `ModuleNotFoundError: No module named 'pygments'` |
| System interpreter | `python3 --version` | `Python 3.9.6` — unusable: `tests/conftest.py` uses PEP 604/585 annotations (`list[Path]`, `Path \| None`) at import time |
| Homebrew interpreter | `/opt/homebrew/bin/python3.13 -m pytest --version` | `No module named pytest` |
| `uv` | `command -v uv` | absent |
| pip index | `pip install` output | `http://yum.tbsite.net/pypi/simple/` (internal mirror, reachable) |

**Repair (chosen route: repair the existing `.venv`, not a new interpreter).** Six distributions were missing relative to what the test tree imports; installing them from the internal mirror made the canonical runner work with zero configuration change:

| Distribution | Installed version | Why it was needed |
|---|---|---|
| `pygments` | 2.21.0 | `_pytest._io.terminalwriter` imports it — without it `pytest` cannot even print its version |
| `PyYAML` | 6.0.3 | `skills/internal/create-team/scripts/build-summary-input.py` imports `yaml`; pytest collected that path and hit `SystemExit(2)` |
| `httpx` | 0.28.1 (+ `anyio` 4.16.0, `certifi`, `h11`, `httpcore`, `idna`, `typing_extensions`) | `src/specify_cli/__init__.py` imports `httpx` at module scope; 106 test modules import the package |
| `rich` | 15.0.0 | `src/specify_cli` console rendering |
| `platformdirs` | 4.14.3 | `src/specify_cli` path resolution |
| `readchar` | 4.2.2 | `src/specify_cli` interactive selection |

**Post-repair verification** (`bash scripts/bash/run-tests.sh` resolves `.venv/bin/python` first, so no env var is needed):

- `.venv/bin/python -m pytest --collect-only -q` → `7016 tests collected in 0.99s`, **0 collection errors** (before the repair: `3116 tests collected, 33 errors`, then `6123 collected / 106 errors` as each missing module was installed — the progression itself proves the gap was dependency-only, not code).
- `bash scripts/bash/run-tests.sh --names-out <spec-dir>/baseline-failed.txt -q` → the failing-test-id set used as the FR-023 baseline. The run takes minutes; its artifact is `baseline-failed.txt` in this spec directory and its console tail is archived under `test-evidence/`.

**Pins (RS-002 / RS-003), taken verbatim from the same session — no version is invented**:

- `pytest 9.2.0` on `CPython 3.14.6`
- `git version 2.54.0 (Apple Git-157)`

`pyproject.toml` declares only `requires-python = ">=3.8"` and an empty-ish `[tool.pytest.ini_options]` block — the repository has never pinned a pytest or git version, which is exactly why requirements FR-023 makes the first measured run the pin.

**Rejected alternatives**: (a) a fresh virtualenv — fixes nothing the repair does not, and adds an install step to every future run; (b) system `python3.9` — structurally impossible, `tests/conftest.py` is not importable there; (c) `uv` — not installed and not declared anywhere in the repo; (d) "record the baseline as `blocked`" — unavailable, because the runner was repairable in-session.

## R2 — `specify init` precondition in a development checkout (D7)

`specify init` is one of the three things 081's own smoke must cover (requirements FR-005). Measured behaviour in this checkout:

```
.venv/bin/specify init demo --ai claude --script sh --no-git --ignore-agent-tools
  error Check for local templates: not found
  Error: Local templates not found. GitHub download is no longer supported.
```

Root cause is a three-line function, not an install problem:

- `src/specify_cli/__init__.py` § `get_resource_path()` returns `MODULE_DIR` **only** if `MODULE_DIR/templates` exists, then returns `None`.
- `MODULE_DIR` is `Path(__file__).parent` → in this checkout `src/specify_cli/`, which carries no `templates/` directory.
- Its own docstring says *"Checks MODULE_DIR first (installed package), then repo root (local dev)"* — the documented second branch does not exist in the code (Principle VIII: code is the fact; here the fact contradicts the stated intent).
- The same file already reaches repo-root assets in three other places (`generate_commands` "Fallback to repo templates if available (helps in local dev when package templates lag)", the root-file copy loop, and the `claudeignore`/`codexignore` fallbacks), so the missing branch is an inconsistency rather than a design decision.

**Chosen enabler (in scope, minimal)**: give `get_resource_path()` the repo-root fallback its docstring declares — installed-package layout keeps priority, so a pip-installed CLI behaves exactly as before (`MODULE_DIR.parent.parent` is `site-packages`, which has no `templates/`). Consequence: the smoke's `specify init` exercises the **working tree** (the point of the check) instead of a stale installed copy.

**Rejected alternatives**: (a) run the smoke through the installed copy in `.venv/lib/.../site-packages/specify_cli` — it was installed 2026-10-30 and would vouch for code this feature did not write; (b) have the smoke build and install a wheel first — deterministic only if `hatchling` and its build isolation are available offline, and it pushes a build-tool dependency into the one command that must stay minimal; (c) mark 081's smoke `blocked` — the honest consequence if no enabler existed, but the enabler is four lines and one contract test.

## R3 — Existing guards this feature must change deliberately (not break silently)

Measured by reading the guards; each row is a pin that 081 changes **on purpose**, and each carries the reason the change is legitimate rather than a regression.

| Guard | What it pins today | Why 081 must change it |
|---|---|---|
| `tests/contract/test_review_code_composition.py` | `exactly two segments`; the marker list `[("1","process segment"),("2","code segment")]`; `### 2.1` | `/speckit.review` becomes four segments + one deterministic check (requirements FR-013) — the pinned sentence is the exact text the requirement rewrites |
| `tests/contract/test_review_feedback_boundary.py` | C-58 "the unit census is three" + the three unit ids | the artifact/implementation segments are carried by a new runtime-reachable skill, which completes its own closing record → census becomes four; the rule "the command MUST NOT suppress a skill's wrap-up" is what forces it |
| `tests/contract/test_skill_layer_visibility_guards.py` | `len(seen) == 15`, `len(internal_nested) == 37`, the `INTERNAL_SKILLS` roster | the new internal skill makes 38; the roster is the drift detector for the split |
| `tests/contract/test_expression_compatibility.py` | `FROZEN_SKILLS`, layer-qualified, 52 units | same new skill → 53 units |
| `tests/contract/test_migration_distribution.py` | `SKILL_BASELINE`, 52 units | same new skill → 53 units |
| `tests/contract/test_measurement_instruments.py` | `skill:review-sdd-process` in the instrument list | a second review-side skill becomes a measurement instrument |
| `tests/contract/test_requirements_checker.py` | the checker's five-label set extracted from `validate-requirements.py`'s docstring | the `Path` marker needs an early deterministic verdict (R4) → a sixth label |

## R4 — Where the `Path` marker is judged

The closed reason set of the closure checker (requirements FR-006, [[STR-008]]…[[STR-014]]) contains **no** reason for a missing or malformed `Path` marker, and adding one would reopen the closed set. A malformed marker therefore cannot be a `block` reason; it is an **input defect**:

- `scripts/python/validate-requirements.py` gains a `path-marker` check (its existing five labels stay unchanged in meaning), judged at the requirements-stage gate — early, where the author can still see the line number.
- `scripts/python/closure-acceptance-check.py` treats a spec whose SC definition lines do not carry exactly one legal marker as an **input error (exit 2)**, consistent with requirements § Edge Cases ("特性文件缺失 … MUST 以退出码 2 表示输入错误").

Both parsers tolerate the marker per Assumptions A4: `validate-requirements.py`'s `DEFINITION_RE` and `pre-analyze-check.py`'s `SC_DEF` anchor only the line prefix, so a trailing `**Path**: final` does not break either.

## R5 — Mirror / regeneration baseline (measured before any edit)

```
python3 scripts/python/regen-command-copies.py --check   → OK: all per-tool command copies match the source templates. (exit 0)
python3 scripts/python/sync-mirrors.py --check           → ok for all six pairs (exit 0)
    templates/ 22 files · skills/external/ 408 · skills/internal/ 136 · agents/ 3 · scripts/ 118 · shared/ 61
```

Baseline drift is **zero** on this branch, so the plan states the close criterion as an absolute `--check` exit 0 for the pairs this feature touches, and it says so as a measured fact rather than a pre-written expectation. Note the `scripts` pair is `STRICT` (an extra file in `.specify/scripts` fails `--check`), which is why the new engine lands in `scripts/python/` and its mirror in `.specify/scripts/python/`.

## R6 — Driver closure/merge landing points (D6/FR-017)

- `skills/external/sdd-loop-driver/scripts/integrate-lines.py` already executes `rebase → quality gate → merge --ff-only → integration-record → archive-runtime → worktree remove`, with the gate supplied as `--gate-cmd`. Today the gate is optional and a gate failure records `integration-record --result failed --reason quality-gate`.
- `line-registry.py`: `STATE_VALUES = {active, waiting, stalled, completed, orphaned, stale, closed}` (line 46); `ACTIVE_STATES = {active, waiting}`; `HOLDING_STATES = {active, completed}`; `merge_ready=True` requires `state == "completed"` (line 707); the terminal guard set `{closed, stale, orphaned}` appears at lines 1447/1949/2139/2249/2266; `promote-waiting` requires `state == "waiting"`; `deregister --reason stale-cleanup` writes `stale_from_state`; the "not revivable" guard for entering `active` admits only `{waiting, stalled}` (line 764).
- Consequence recorded for the implement stage: A6 item 6 ("recovery is `update --state active`") is only satisfiable if that same guard admits `blocked` — the plan therefore names `blocked` as an allowed predecessor for `active` **and** keeps it out of the terminal set. This is the one place where the eight dispositions in requirements A6 touch the same line from both sides.

## R7 — Where the four deterministic findings run (FR-012)

`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` is already the U4 gate for requirements/plan/tasks (`shared/workflow/expression-gates.md` rows `G-req-clarity` / `G-plan-fact` / `G-tasks-fact`). The four new findings land in that same script and those same gate rows; no new gate registry row is created, which is what "MUST NOT create a second parallel gate system" requires. The script's existing shape gives the extension its natural home: a per-stage check function plus a `findings` entry with `check`/`severity`/`path`/`line`/`message`, and `--waive CHECK:REL_PATH:LINE` already provides the waiver form.

## R8 — Inherited-blocker extraction: what actually exists today

The dependency set for 081 is derived, not assumed:

| Candidate | In the dependency set? | Basis |
|---|---|---|
| Feature 071 (Review × Code-Review composition) | **yes** | 081 rewrites the composition sentence and the gate carriers that 071 owns; 071's detail is `Ready for Review` |
| Feature 077 (feature-level class + document-stage gates) | **yes** | 081's four findings ride the same gate rows 077 registers; 081's plan-stage class read is 077's |
| Feature 062 ← spec 080 (humanize) | **no** | 081 touches no run-output surface; no shared owner document |
| Feature 072/073/074/076 | **no** | no shared owner document or gate row |

Measured inherited records (the FR-011 input — `grep` over each dependency's `verification.md` and `tasks.md`):

- `071/verification.md`: `SC-001_status=partial`, `SC-006_status=partial`, `deferred_tasks=` (empty), zero `[~]` rows in `tasks.md`.
- `077/verification.md`: `SC-002_status=partial`, `SC-005_status=partial`, `SC-008_status=partial`, `deferred_tasks=` (empty), zero `[~]` rows in `tasks.md`.
- No feature detail in `.specify/memory/features/` carries a `## Deferred` section; the extraction therefore reads the two carriers that do exist (`verification.md` status rows and `deferred_tasks=`), which is what the checker implements.

## R9 — Where review's report structure can grow without renumbering

`templates/review-template.md` already exposes `### 2.1 Code Segment (Verdict and Pointers)`, and two owner documents plus at least one guard cite that literal (`templates/commands/review.md`, `templates/feature-details-template.md` § gate item 8, `test_review_code_composition.py`). Adding the two new segments **after** `2.1` as `### 2.2` / `### 2.3` and the deterministic check as `### 2.4` keeps every existing citation valid; renumbering would touch two owners and several guards for no semantic gain. The template states that subsection numbers are stable slots, not execution order (the execution order is owned by `templates/commands/review.md`).
