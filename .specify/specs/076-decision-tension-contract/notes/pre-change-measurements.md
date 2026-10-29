# Pre-Change Measurements — 076-decision-tension-contract

**Purpose**: freeze the three plan-stage baselines this feature's implementation is judged
against, BEFORE any source edit. Each row keeps the command, the date it was measured, the
observed value, and the evidence file that holds the verbatim output. These are dated records
(`2026-10-29`); they are not restated as current reality elsewhere — the owner of each value is
the evidence file named in the row.

**Baseline commit**: `ac63fe8c` (Feature 076 registration) — the referent for the two closed-set
claims and for the zero-new-machinery set difference.

## 1. Mirror drift baseline (six pairs, all `ok`)

- **Command** (both, run from the repo root):
  ```
  python3 scripts/python/sync-mirrors.py --check
  python3 scripts/python/regen-command-copies.py --check
  ```
- **Date**: 2026-10-29 (plan stage)
- **Observed**:
  ```
  ok    templates/ == .specify/templates/ (22 files)
  ok    skills/external/ == .specify/skills/ (406 files)
  ok    skills/internal/ == .specify/skills/internal/ (136 files)
  ok    agents/ == .specify/agents/templates/ (3 files)
  ok    scripts/ == .specify/scripts/ (115 files)
  ok    shared/ == .specify/shared/ (59 files)
  EXIT=0
  ```
  `regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.`
- **Evidence file**: `test-evidence/sync-mirrors-check.txt`
- **Criterion this baseline serves**: 「no NEW drift relative to this measurement」, never a bare
  exit code (FR-025 / `contracts/mirrors-and-scope.md` C-3).

## 2. Terminology baseline (five internal aliases, each 0 in the three distribution trees)

- **Command** (one run per alias):
  ```
  grep -rF --include=*.md -- '<alias>' shared templates skills | wc -l
  ```
- **Date**: 2026-10-29 (plan stage)
- **Observed**:

  | Alias | Count |
  |-------|-------|
  | 矛盾论 | 0 |
  | 主要矛盾 | 0 |
  | 矛盾的主要方面 | 0 |
  | 对抗性矛盾 | 0 |
  | 矛盾转化条件 | 0 |

  Positive control: the A3 alias list still exists in `requirements.md` (1 line).
- **Evidence file**: `test-evidence/terminology-aliases-baseline.txt`
- **Criterion this baseline serves**: SC-007「改动前后计数相同」(FR-024).

## 3. Targeted contract-test baseline (70 passed, five existing guard suites)

- **Command**:
  ```
  $SPECKIT_PYTHON -m pytest -q \
    tests/contract/test_closed_set_claims.py \
    tests/contract/test_self_improvement_conformance.py \
    tests/contract/test_validation_carrier_contract.py \
    tests/contract/test_user_facing_comprehension_doc.py \
    tests/contract/test_validate_tasks_parallel_safety.py
  ```
- **Date**: 2026-10-29 (plan stage)
- **Observed**: `......................................................................   [100%]` /
  `70 passed in 0.59s` / `EXIT=0`
- **Evidence file**: `test-evidence/targeted-tests-baseline.txt`
- **Criterion this baseline serves**: GATE-5「五个既有守护套件的失败名集合无新增」.

## 4. Interpreter fact (recorded, not hidden)

- The repo's own `.venv/bin/python -m pytest --version` reports `No module named pytest`
  (Python 3.14.6, pytest absent).
- `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python` → `pytest 9.1.1`
  (2026-10-29). Every pytest run of this feature uses that interpreter, matching the plan-stage
  targeted baseline.

## 5. Implementation-start full-suite baseline

- **Observed**: `6514 passed / 39 failed`; the 39 pre-existing failure names are frozen in
  `baseline-failed.txt` and MUST NOT be repaired, masked, or counted as regressions of this
  feature.
