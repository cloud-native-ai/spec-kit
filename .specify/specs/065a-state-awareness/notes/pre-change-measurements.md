# Pre-Change Measurements — 065a implement baseline (T001)

**Captured**: 2026-10-22, first edit of this implement run (implement-feature Step 0/T001).
**Provenance**: no `<spec-dir>/baseline-*` files existed before this run — this file IS the
first capture (skill §Step 0: a missing baseline is first capture, never zero drift).
`coverage-baseline.txt` was already frozen at tasks stage (header verified below); T002
re-runs the freeze command and verifies the header shape.

## 1. Mirror drift baseline

```
$ python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
scope --only: skills/external/sdd-loop-driver
ok    skills/external/ == .specify/skills/ (26 files)
SYNC_EXIT=0
```

Judgement rule (per tasks.md §Environment Prerequisites): "no NEW drift relative to this
baseline", not absolute-zero. Baseline drift set = empty.

## 2. Watcher self-test baseline

```
$ bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
ok stream-derive-failure
ok stream-detached-survives
SELF-TEST: 38 passed, 0 failed
WATCH_EXIT=0
```

## 3. Pytest pre-run result (Registry engine + skill contract)

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh --names-out .specify/specs/065a-state-awareness/baseline-failed.txt \
  -q tests/unit/test_line_registry_engine.py tests/contract/test_sdd_loop_driver_skill.py
48 passed in 31.22s
# failed-name list written: .specify/specs/065a-state-awareness/baseline-failed.txt (0 entries)
```

Interpreter probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version`
→ `pytest 9.1.1` (matches §Environment Prerequisites 2026-10-21; NOT a probe failure).

## 4. Working-tree snapshot of delivery paths

```
$ git status --short -- skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver \
    docs/reference/skills/sdd-loop-driver.md tests/contract/test_sdd_loop_driver_skill.py
(empty — exit 0, no output)
```

**Premise update (falsified by measurement, disclosed per implement-feature Step 5)**:
tasks.md § Path Conventions and T020/T022 state the delivery paths "已含外部同步产生的
未提交改动". At capture time the tree is CLEAN for all four paths — those external-sync
changes were committed before this dispatch (see `git log`: c7082866… and earlier).
Consequence: the "preserve uncommitted external changes, incremental only" constraint is
satisfied vacuously; implementation still edits incrementally and never rewrites those
files wholesale. Premise re-referenced: "tree clean at T001" is the new recorded baseline.

## 5. Frozen coverage-baseline header (verified, T002's frozen side)

```
$ head -2 .specify/specs/065a-state-awareness/coverage-baseline.txt
# coverage-baseline: frozen UNCOVERED clause names, codepoint-sorted, one per line; ...
# frozen-from: .specify/specs/*/contracts/* excluding 065a-state-awareness | ... | base-sha: 095c291ae2ab | files: 164 (parsed 81 + named 83)
```

## 6. Failed-name baseline (skill-owner form)

`baseline-failed.txt` next to this file: 0 entries (baseline is green). Regression
comparison form: `LC_ALL=C comm -13 .specify/specs/065a-state-awareness/baseline-failed.txt
<current-failed.txt>`; zero output = zero NEW failures (name-level, not count-level).
