# Pre-change measurements — implement entry (P1, T001)

- Date: 2026-11-25
- run_id: `r20261125T022857Z-06dd`
- Stage: `implement`, package P1 (T001–T009)
- Capture directory: repository root `/storage/project/cloud-native-ai/spec-kit`
- Interpreter for Python checks: `/usr/local/bin/python3` (Python 3.11.11, pytest 8.4.2, typer 0.19.2)

Every reading below is a fresh execution on this worktree at the moment named; nothing is inherited
from prose. Where a plan/tasks-stage prose value differs, the difference is classified in
§ Baseline deltas.

## 1. Worktree identity

```console
$ git rev-parse --short HEAD
113d2c650
$ git status --short
(no output — clean)
$ git branch --show-current
105-runtime-store-layout
```

Provenance: `113d2c650` is the analyze-gate checkpoint commit on top of the dispatch base
`1b38f0e60`; the tree is clean.

## 2. Store inventory baseline

```console
$ git ls-tree -d 23938f22e:.specify/memory
040000 tree a2f1ecaf2066518465c828ebcadc1af8cdf0d101	coaching
040000 tree c0807237e7de9d6bdab02105f49470e6e606352c	evidence
040000 tree c4c9f61cfde1adeede6178203b0c30f4c7965f68	exec-quant
040000 tree ccfc6a5f93f1ad75444bd3f0dbf73f6282c767d5	feedback
040000 tree d0da05a5a93d5bacb46f704068890d8d8f0813b9	housekeeping
040000 tree 7e5597c0a36d3b1561884bee334fea2dc305d22e	knowledge
040000 tree c94744f56159061469ada558d7d260a8414ff915	renumber
040000 tree 7fdea5528286614d6e4656664c8cf4e3813dd26c	retention
040000 tree 53136a3d83060c8297574cec2fd845f16293c6dd	session
040000 tree 4d927e0b07ba91c7767c9e6eec779893fe973bc8	todo
040000 tree c96de145f3e73741d87fdf964d57883cc70708fe	tools
040000 tree 6d9f54c01c7b13bf3a7d82cf23551c81516d015c	trigger
$ git ls-tree -d 23938f22e:.specify/memory | wc -l
12
```

Reading: **12** baseline children — `coaching evidence exec-quant feedback housekeeping knowledge
renumber retention session todo tools trigger`. Matches the closed-inventory premise.

```console
$ git ls-files .specify/memory | wc -l
2992
```

Reading: **2,992** tracked paths under the live `.specify/memory/` at `113d2c650` (the plan/research
recorded 2,963 at `23938f22e` and 2,971 at plan time — both are earlier, dated readings; records
written by later stages account for the growth, not a defect).

## 3. Test live-reference carrier count

```console
$ grep -rl '\.specify/memory' tests/ | wc -l
92
```

Reading: **92** test files carry the retired-root literal at entry. Per rule L-3 / R-2.5 this is a
measurement, not a contract; classification happens in T029.

## 4. Mirror and command-copy baseline

```console
$ /usr/local/bin/python3 scripts/python/sync-mirrors.py --check
... (full output retained at .specify/specs/105-runtime-store-layout/test-evidence/sync-mirrors-baseline.txt, 459 lines)
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
rc = 2
$ grep -c '^DIFF ' .specify/specs/105-runtime-store-layout/test-evidence/sync-mirrors-baseline.txt
444
$ /usr/local/bin/python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
rc = 0
```

Readings: `sync-mirrors --check` rc **2** with **444** DIFF members, 0 MISS / 0 ORPHAN;
`regen-command-copies --check` rc **0**.

## 5. Full-suite name-level baseline (implement Step 0)

```console
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    --names-out .specify/specs/105-runtime-store-layout/test-evidence/implement-baseline-failed.txt
... full stdout/stderr retained at
    .specify/specs/105-runtime-store-layout/test-evidence/implement-baseline-run.txt
# test runner: mode=parallel workers=auto dist=load passes=2 tier=fast excluded_slow=7
==== 748 failed, 9469 passed, 4 skipped, 1536 warnings in 73.69s (0:01:13) =====
# failed-name list written: .../implement-baseline-failed.txt (748 entries) passes=2
```

Readings: **748 failed / 9,469 passed / 4 skipped** on the fast tier; the failed-name list holds
**748** sorted, de-duplicated test ids at
`.specify/specs/105-runtime-store-layout/test-evidence/implement-baseline-failed.txt`. This list is
the `comm -13` comparison base for GATE-5. The pre-existing failures are dominated by the mirror-drift
contract tests (same root cause as §4) plus environment/state facts already present at entry; they are
named, never claimed green.

## 6. Clause-coverage baseline (Step 0 + T001 row)

```console
$ /usr/local/bin/python3 .specify/scripts/python/account-clause-coverage.py \
    --spec-dir .specify/specs/105-runtime-store-layout --freeze > /tmp/accc-freeze-105.txt
rc = 0
$ wc -l /tmp/accc-freeze-105.txt
787 /tmp/accc-freeze-105.txt
$ diff /tmp/accc-freeze-105.txt .specify/specs/105-runtime-store-layout/coverage-baseline.txt | wc -l
4
```

The only difference between the re-captured freeze document and the frozen
`coverage-baseline.txt` is the `base-sha` header token (`113d2c650309` now vs `464ef0f045c4` frozen)
— the sorted UNCOVERED name list is identical (787 lines, 322 files = 214 parsed + 108 named). The
`--freeze` mode prints only and never writes; the frozen file was not modified.

Live coverage reading at entry:

```console
$ /usr/local/bin/python3 .specify/scripts/python/account-clause-coverage.py \
    --spec-dir .specify/specs/105-runtime-store-layout
claimed clauses 8, scanned files 326, clause universe 2418, FR universe 27
[clause-uncovered] pass (785) — 785 uncovered, 0 beyond the frozen baseline
[fr-uncovered] fail (21) — 6 of 27 FRs cited from citation groups
[clause-unparsable] fail (111) — 111 files yield no clause id; 1 declares a positive form
[coverage-baseline-delta] pass (0)
```

Readings: `claimed clauses 8`; `clause-uncovered` beyond baseline **0**; `coverage-baseline-delta`
**0**; `fr-uncovered` **21** (the md-none structural fact recorded in DoD-3 — reported, not a pass
criterion).

## Baseline deltas (classified before any drift verdict)

| Frozen / recorded value | Fresh reading | Class | Note |
|---|---|---|---|
| Plan `sync-mirrors --check` prose: 450 DIFF | 444 DIFF (same at the baseline artifact's own capture commit `647c13cd9`) | pre-existing measurement-time difference | The pinned artifact `test-evidence/sync-mirrors-baseline.txt` carries 444 members and is the comparison base for `test_mirror_member_set`; the prose 450 is a dated reading. No member is added or lost by this package's start. |
| Plan/research tracked paths: 2,963 (`23938f22e`) / 2,971 (plan time) | 2,992 at `113d2c650` | attributable to this feature line's own stage commits | Records written by requirements/clarify/plan/tasks/analyze stages under `.specify/memory/` between those commits. |
| Tasks measured premise `tests/` carriers: 92 | 92 | none | No change. |
| `coverage-baseline.txt` `base-sha: 464ef0f045c4` | re-captured header `base-sha: 113d2c650309` | attributable to this feature line's own commits | Name list identical; the frozen file is not rewritten. |

No `undecidable` class was needed.

## Pointers

- Full-suite baseline: `test-evidence/implement-baseline-run.txt`, `test-evidence/implement-baseline-failed.txt`
- Mirror baseline: `test-evidence/sync-mirrors-baseline.txt`
- Comparison form (owner): `.specify/skills/internal/implement-feature/SKILL.md` § Test runs
