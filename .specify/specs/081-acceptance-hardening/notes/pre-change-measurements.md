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

## PM-4 Contract-clause coverage lane — `pending (written by T023)`

Recorded here because T023 names this note as its landing point. Measured before the freeze (2026-11-03):
`status=baseline-missing`, `claimed clauses 0`, `[fr-uncovered] fail (25) — 0 of 25 FRs cited from citation
groups`. T023 freezes the exemption baseline and appends the read-only accounting verdict below; the FR lane
has no baseline by design, so freezing it does not make it green, and no empty or hand-edited baseline may
stand in for the real state.

- `account-clause-coverage.py --spec …` verdict: pending
- frozen baseline file (`coverage-baseline.txt`) name count: pending
