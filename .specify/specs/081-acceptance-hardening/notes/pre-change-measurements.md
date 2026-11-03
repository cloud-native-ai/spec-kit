# Pre-Change Measurements — Feature 081, slice 081a (implement start, T001)

**Captured**: 2026-11-03, at the first implement-stage edit (implement part 1, T001), HEAD `f9f6d4f3`,
branch `081-acceptance-hardening`. This note is the **frozen pre-change side** the later rows measure
against. It is deliberately **pointer-first**: the two expensive readings were taken once at plan stage and
are **not re-derived here** — re-running the full suite to re-collect a baseline would contaminate the very
comparison the baseline exists for.

## PM-1 Test baseline — by pointer, not re-run

| Reading | Frozen value | Where it physically lives |
|---|---|---|
| Failed / passed / skipped | `39 failed, 6970 passed, 7 skipped` | `test-evidence/plan-baseline-run.txt` (plan-stage console transcript, last line) |
| Failed test **id set** | 39 ids, one per line | `baseline-failed.txt` (same directory as `tasks.md`) |
| Collection size | `7016 tests collected` | `test-evidence/plan-runner-pins.txt` |

Owner of the comparison rule: `tasks.md` DoD-6 / GATE-7 — the comparison unit is the failing test **id set**,
never a count and never a byte diff. T022 runs the **head** side once at slice close; the baseline side above
is never re-collected (FR-023).

## PM-2 Runner pins — by pointer, plus the validity rule

`test-evidence/plan-runner-pins.txt` records, measured 2026-11-03:

| Pin | Recorded value | Consumer |
|---|---|---|
| `pytest --version` | `pytest 9.2.0` | RS-002 |
| `python --version` | `Python 3.14.6` | RS-002 |
| `git --version` | `git version 2.54.0 (Apple Git-157)` | RS-003 |

**Validity rule** (owner: `requirements.md` FR-023; `contracts/artifact-schemas.contract.md` AS-07): a pin
that is a transcript of one run is valid only while re-reading it reproduces it. Every baseline-difference
comparison MUST re-read both `--version`s first; a mismatch against the file above makes **that comparison
invalid** (input error, exit 2) and MUST NOT be read as new failures. A rebuilt `.venv` or another machine
means re-collecting the baseline, not reusing this one.

## PM-3 Mirror and per-tool-copy parity at implement start

Measured in this part, on the tree as it stood before any 081a source edit:

```text
$ python3 scripts/python/sync-mirrors.py --check
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (408 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (118 files)
ok    shared/ == .specify/shared/ (61 files)
(exit 0)

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
(exit 0)
```

Both `exit 0` with **zero drift**, so GATE-2 / DoD-4 may legitimately read as an absolute `exit 0` later:
the criterion is reachable because it holds now, not because it is assumed. The two file counts this part
moves are `shared/` (61 → 62, the T005 owner doc) and `scripts/` (118 → 119, the T006 checker).

## PM-4 Contract-clause coverage lane — **frozen and accounted at T023 (2026-11-03)**

Recorded here because T023 names this note as its landing point. Measured before the freeze (2026-11-03):
`status=baseline-missing`, `claimed clauses 0`, `[fr-uncovered] fail (25) — 0 of 25 FRs cited from citation
groups`.

### PM-4.1 The freeze (`--freeze`, exit 0)

```text
$ python3 scripts/python/account-clause-coverage.py .specify/specs/081-acceptance-hardening --freeze \
    > .specify/specs/081-acceptance-hardening/coverage-baseline.txt
EXIT=0
```

| Reading | Value |
|---|---|
| baseline file | `.specify/specs/081-acceptance-hardening/coverage-baseline.txt` |
| frozen name count | **495** names (497 lines = 2 header comment lines + 495 names) |
| sha256 | `5dcd61379e5e9f80c886b500f2e4eb02e3049621c281f76fe61952936dd95169` |
| frozen face | `.specify/specs/*/contracts/*` **excluding** `081-acceptance-hardening` — the accountant excludes the accounted spec so its own items can be *claimed* but never *exempted by its own baseline* |
| base sha recorded in the header | `da5e4480fe92` (the part-3 commit this tree derives from) |

The frozen set is repo-wide pre-existing debt (495 unclaimed clause names across 144 parsed contract files in
other specs), not this slice's own gaps. It was frozen from the **first** full-tree accounting run, not from a
green one — green would require the baseline while the baseline requires a run (the circularity `C-21` names).

### PM-4.2 The read-only accounting (exit 1 — an honest `uncovered`, not a green)

```text
$ python3 scripts/python/account-clause-coverage.py --spec .specify/specs/081-acceptance-hardening
spec-dir: .specify/specs/081-acceptance-hardening
corpus:   .specify/specs/*/contracts/*
scanned 248 files: parsed 145 + named-unparseable 103 == 248  [relational sentinel OK]
clause universe: 1516 distinct names over 145 parsed files (1540 ids extracted)
claimed clauses (this feature): 0
baseline: …/coverage-baseline.txt (495 names) ; baseline-internal existing uncovered: 495
FR uncovered: 25
  [clause-uncovered] fail (512) — 512 uncovered, 17 beyond the frozen baseline
  [fr-uncovered] fail (25) — 0 of 25 FRs cited from citation groups
  [clause-unparsable] warn (103) — 103 files yield no clause id under the owner's forms; 0 declare a
                                     positive form, so this is not read as zero-and-covered
  [coverage-baseline-delta] fail (17) — baseline holds 495 names; 495 uncovered items are baseline-internal
42 error(s), 0 warning(s)
status: uncovered
EXIT=1
```

- `account-clause-coverage.py --spec …` verdict: **`status: uncovered`, exit 1** — `[clause-uncovered] fail`,
  `[fr-uncovered] fail`, `[coverage-baseline-delta] fail`, `[clause-unparsable] warn`
- frozen baseline file (`coverage-baseline.txt`) name count: **495**

### PM-4.3 Why the two lanes stay red, stated per lane (no papering over)

- **Clause lane, 17 beyond baseline.** The live face includes this spec's own five contract files (the freeze
  face excludes them by design), and this feature's task rows carry **zero** `[green: <contract>#<clause>]`
  declarations, so the delta is exactly 17 names — all of them `closure-acceptance-check.contract.md#C-01` …
  `#C-17` (measured by `LC_ALL=C comm -13` against the frozen file, names not counts). This is a real,
  owned gap: the citation-group form for 081's contracts is the separate obligation T023's row names, and it
  belongs to the rows that implement those clauses. It is **not** repairable by widening or hand-editing the
  baseline — an exemption the spec grants itself is exactly what the freeze face excludes.
- **FR lane, 25 uncovered.** `[fr-uncovered] fail (25) — 0 of 25 FRs cited from citation groups`. This lane has
  **no baseline by design** (`research.md` A-7): FRs are claimed from contract citation groups, never from task
  rows, so freezing cannot move it and an empty or hand-edited baseline must not be substituted for the
  measurement. It reads the same before and after the freeze, which is the expected, not the surprising, outcome.
- **Anti-vacuity companion present**: `claimed clauses 0`, `scanned files 248`, `clause universe 1516`,
  `FR universe 25` — so "empty because right" is distinguishable from "empty because blind".

None of the three legs above is a substitute for the other, and none was made green by this part's work.

