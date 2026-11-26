# Implement Stage Integration Record — spec 106 (T001–T037)

Stage integrator closing execution for line `background-silent-failure` (run
`r20261125T113505Z-106a`, stage `implement`, attempt 1). Date: 2026-11-26.
Branch `106-background-silent-failure`.

## Integration order and package commits

Packages were verified in order P1 → P2 → P3 → P4; each verdict covers its task rows,
not a commit range, so the ranges below are the actual linear chain
(`git log --first-parent 907426e1c..HEAD`).

| Package | Rows | Commit range (actual) | Verdict file | Verdict |
|---|---|---|---|---|
| P1 | T001–T008 | `ef807eead..94c2be428` | `.specify/state/wp/background-silent-failure-implement-p1-a1.verdict.json` | pass |
| P2 | T009–T018 | `621b97965..813986be5` | `.specify/state/wp/background-silent-failure-implement-p2-a1.verdict.json` | pass |
| P3 | T019–T027 | `a31c307df..3f07db062` | `.specify/state/wp/background-silent-failure-implement-p3-a1.verdict.json` | pass |
| P4 | T028–T037 | `53b530096..0b59b17ad` | `.specify/state/wp/background-silent-failure-implement-p4-a1.verdict.json` | pass |

Range corrections (disclosed, no verdict contradiction): the dispatch input carried P3 as
`3f07db062..bc1883c8c` and P4 as `53b530096..6bc7a1bdd`. The P3 range is reversed
(`bc1883c8c` is the T026 commit inside P3; the tip is `3f07db062`), and the P4 tip
extends two commits past `6bc7a1bdd` (`1f0e9dee5` T034/T035, `0b59b17ad` T036/T037).
The P4 verdict's own evidence_refs verify `git log 3f07db062..HEAD` through
`0b59b17ad`, so both rows' verdicts are the authority and the table above uses the
chain actually on disk.

## Coverage

Every task row T001–T037 has exactly one passing package check (`result: "pass"` in the
four verdicts above); no row is missing, duplicated or contradictory.

- P1: T001–T008 — 8 rows, pass.
- P2: T009–T018 — 10 rows, pass.
- P3: T019–T027 — 9 rows, pass.
- P4: T028–T037 — 10 rows, pass.
- **Coverage: 37/37.**

## Task table closure

- 37 `- [ ]` rows flipped to the project task-state sigil `- [X]` (task text unchanged).
- `grep -cE '^- \[[ >]\]' tasks.md` = **0** (GATE-8 re-run; T037's recorded hand-off
  reading of 37 was an ownership deferral — the crew seat cannot write the task table —
  discharged by this integrator seat).
- `python3 .specify/scripts/python/validate-tasks.py .specify/specs/106-background-silent-failure/tasks.md`
  → `PASS: … — 0 error(s), 0 warning(s)`, rc 0 (re-run after the flip).
- Closed rows: 37; `[~]` rows: 0.

## Test readings

**Implement-start baseline (test-budget E2 slot seq 1, spine fence).** Full suite via the
sole runner `scripts/bash/run-tests.sh --full --names-out …/baseline-failed.txt`:
rc 1, **10049 passed / 218 failed** (218 unique failed nodeids in
`baseline-failed.txt`), full capture `test-evidence/implement-baseline-full.txt`.
No closure full-suite slot was spent (the budget fence holds one baseline slot; the
targeted batteries below are the stage's regression evidence).

**Targeted suites, green per package verdict (re-run by the independent verifier):**

| Package | Selection | Reading |
|---|---|---|
| P1 | `test_settlement_contract_definitions.py` + `test_settlement_engine.py` | 42 passed in 6.44s |
| P1 | `test_role_edge_engine.py` (report/query schema unchanged) | 25 passed in 6.32s |
| P2 | `test_settlement_carriers.py -k "test_c2_"` | 7 passed in 6.30s |
| P2 | `test_settlement_carriers.py` (US2 turn-green) | 21 passed in 6.29s |
| P2 | `test_settlement_engine.py` (supporting re-run) | 23 passed in 6.40s |
| P3 | `test_settlement_engine.py` + `preservation` + `scope` + `carriers` | 71 passed in 22.42s |
| P4 | `test_settlement_migration.py` (US5 turn-green) | 8 passed in 6.28s |
| P4 | settlement battery (engine 25 + carriers 30 + preservation 6 + scope 10 + migration 8) | 81 passed in 23.48s |
| P4 | smoke pair `test_settlement_engine.py` + `test_settlement_carriers.py` | 57 passed in 6.45s |
| P4 | SC-001 selection `-k "silent or zombie or pid_reuse or live"` | 16 passed |
| P4 | SC-002 selection `-k "unrecorded or unbacked or out_of_set or two_runs"` | 5 passed |

Other closure readings (from the P4 verdict): `validate-tasks` PASS 0/0;
`pre-analyze-check --stage tasks` decision=pass errors=0 advisories=2 (both recorded and
adjudicated in `test-evidence/final-gate.txt`); `sync-mirrors.py --check` rc 0 (output
identical to `test-evidence/mirror-check-baseline.txt`); `regen-command-copies.py --check`
rc 0; `scan-confirmation-gates.py --root . --json` total 30 vs frozen baseline 31, zero
new per-file hits on touched files; `account-clause-coverage.py` 34 claimed clauses,
0 uncovered beyond the frozen baseline.

## Residual observations (all disclosed by the package verdicts; none contradicts a verdict)

1. **T028 red-first premise** — the planned red could not reproduce because the T007
   commit `eabebe7bf` already shipped `version_bearing`/`legacy` in the engine. No source
   was rolled back to fabricate a red; red capability is evidenced by T021/T025/T032.
   The verdict is pass with the anomaly disclosed.
2. **T037 GATE-8 ownership deferral** — the crew seat could not satisfy `grep = 0` on the
   task table (task-table writes belong to the integrator). Discharged above; the
   re-run reading (0) is this record's.
3. **T033 in-passing correction** — the C1 attempt reader now consumes the live
   `pid=<n> start=<ticks>` line first (bare-integer fallback kept), mirrored and pinned by
   `test_c1_reads_the_drivers_pid_line_format` and
   `test_c1_pid_line_start_token_detects_pid_reuse` (both green).
4. **T026 meta-mutation method** — the second-value-table guard was proven red by
   injecting a table into the real declaration file with backup-and-restore; the
   byte-identical restore (sha256 `1406c61c…`) is recorded in `test-evidence/mutation-drill.md`.
5. **`verification.md` writeback** — T035 forbids the crew (and this seat) to write it;
   the spec-side `verification.md` remains the driver's post-input duty.
6. **No push / no merge** — U0 boundary; merging belongs to U6.

## Scope of this closing execution

Changed only: the task table state sigil (37 rows) and this record. No implementation
content, no evidence file was rewritten, no part commit was rewritten or squashed, no
spine or registry write, no push.
