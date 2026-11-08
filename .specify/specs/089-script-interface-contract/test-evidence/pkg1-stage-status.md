# Package 1 stage status — 089-script-interface-contract (T001–T011)

**Scope**: Phase 1 Setup (T001–T005) + Phase 2 Foundational (T006–T011). One dispatch, 11 rows.
**Tree**: `/cws_data/cloud-native-ai/spec-kit`, branch `089-script-interface-contract`, base `9add95eb`.
**Run**: 2026-11-06, implement stage, package 1 of ~6.

---

## 1. Per-task completion

| Task | Status | Artifact | Verification |
|---|---|---|---|
| T001 | done | `notes/premises.md` | 13 generation-time premises re-probed; every one `agrees`, no anomaly |
| T002 | done | `notes/pre-change-measurements.md` + `test-evidence/T002-pre-change-measurements.txt` | 26 commands captured with readings and exit codes (119 lines) |
| T003 | done | `test-evidence/baseline-failed.txt` (34 names) + `test-evidence/baseline-full-suite-2026-11-06.{raw,meta}.txt` | full suite `--names-out`, exit 1, 592 s wall; **34 failed / 7464 passed / 3 skipped in 589.34 s** |
| T004 | done | `test-evidence/T004-coverage-refreeze.txt` | re-freeze exit 0; **573 names, `diff` empty**; header differs only in `base-sha` |
| T005 | done | `test-evidence/T005-sandbox-probe.txt` | worktree add 405 ms / remove 73 ms; `git worktree list` back to **1** entry; isolation sha256 PASS |
| T006 | done | `shared/definitions/script-interface-definitions.md` (header + 8 `##` sections) | 5 owned items listed at the top, `## Declared Exceptions` present exactly once |
| T007 | done | same file, `## 1.` + `## 2.` | four labels as a closed set in one table row; 7-step classification list, both readable by grep |
| T008 | done | same file, `## Declared Exceptions` | table `path` / `skill` / `unsatisfied clause` / `handling`, empty state = literal `none` |
| T009 | done | same file, `## 投影声明形态与消费方` | two kinds (`python-version-bridge`, `bash-version-guard`), anchors named, marker line + self-sufficiency rule |
| T010 | done | `shared/definitions/framework-map.md` | new row "Script interface contract" in the definition index |
| T011 | done | `scripts/python/script_interface_cli.py` + `tests/unit/test_script_interface_cli.py` | **24 passed in 0.27 s**; `--version` / `--help` / `--emit-rule` / unknown-option exit 2 all measured |

## 2. Commands and readings (this package's own checks)

| # | Command | Reading |
|---|---|---|
| 1 | `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/unit/test_script_interface_cli.py -q` | `24 passed in 0.27s`, exit 0 |
| 2 | `SPECKIT_PYTHON=/usr/bin/python3 bash scripts/bash/run-tests.sh --names-out …/baseline-failed.txt` | exit **1**, 592 s, `34 failed, 7464 passed, 3 skipped in 589.34s` |
| 3 | `grep -c script_interface_cli …/baseline-failed.txt` | **0** — the new unit test is not among the baseline failures |
| 4 | `/usr/bin/python3 -m pytest -q --collect-only` | `7527 tests collected in 1.93s`, exit 0 |
| 5 | `/usr/bin/python3 -m pytest -m contract -q --collect-only` | `4305/7527 tests collected (3222 deselected) in 1.90s` |
| 6 | `/usr/bin/python3 scripts/python/account-clause-coverage.py .specify/specs/089-script-interface-contract` | exit 0, `status: ok`, claimed clauses 38, FR 31/31 cited, 0 beyond baseline |
| 7 | `/usr/bin/python3 scripts/python/sync-mirrors.py --check` | exit **0**; `ok shared/ == .specify/shared/ (95 files)`, `ok scripts/ == .specify/scripts/ (122 files)`, all six pairs ok |
| 8 | `cmp shared/definitions/script-interface-definitions.md .specify/shared/definitions/script-interface-definitions.md` | byte-identical |
| 9 | `cmp shared/definitions/framework-map.md .specify/shared/definitions/framework-map.md` | byte-identical |
| 10 | `git worktree list` after T005 | **1** entry |
| 11 | `/usr/bin/python3 scripts/python/script_interface_cli.py --version` | `script_interface_cli.py 0.0.22`, exit 0 |
| 12 | `/usr/bin/python3 scripts/python/script_interface_cli.py --help` | usage + options + `-h/--help/--emit-rule/--version`, exit 0 |
| 13 | `/usr/bin/python3 scripts/python/script_interface_cli.py --emit-rule` | 8 keys exactly (`labels`, `flag_forms`, `separator`, `version_line`, `version_source`, `exempt_basis`, `findings`, `exceptions`), exit 0 |
| 14 | `/usr/bin/python3 scripts/python/script_interface_cli.py --bogus` | `error: unrecognized arguments: --bogus`, exit **2** |

## 3. Mirror state (honest boundary of this package)

This package edits **framework sources only** (`shared/`, `scripts/`) and projects them, as the dispatch brief
requires; it does not touch `.specify/templates/`, `.specify/memory/` or `.specify/instructions.md`.

`sync-mirrors.py --check` exits **0** with every pair `ok`. Three paths were projected by this package, each
byte-identical to its source (`cmp` exit 0):

- `.specify/shared/definitions/script-interface-definitions.md` (new; `shared` pair now 95 files)
- `.specify/shared/definitions/framework-map.md` (edited)
- `.specify/scripts/python/script_interface_cli.py` (new; `scripts` pair now 122 files)

**Known, deliberate residue**: `scripts/bash/script-interface.sh` and `scripts/python/script-interface-check.py`
are named in `feature-ref.md` § 2 as surfaces #5 and #3. Neither exists yet: T055 (bash guard body) and T032
(checker engine) are rows of later packages, and packages 2–6 create them. No stale copy exists under
`.specify/` for either path — `--check` reports no `MISS` on the `scripts` pair, i.e. the mirror tree carries
exactly the 122 sources it has.

## 4. Baseline failures are pre-existing, not introduced

The 34 baseline failures were captured at `9add95eb`, immediately **before** T001 created any file, and
immediately after T011 landed. `grep -c script_interface_cli baseline-failed.txt` = **0**, so no failure is
attributable to this package. The failure groups are: `test_loop_state_engine.py` (8), `test_admission_check.py`
(3), `test_lifecycle_detach_reattach.py` (3), `test_ssh_utils_skill.py` (2), and 18 individual contract tests.
The implement-entry baseline is therefore `baseline-failed.txt` itself; closure GATE-1 compares against it with
`comm -13`.

## 5. Deferred / not done in this package

- **No contract test** for the owner page: `tests/contract/test_script_interface_contract.py` is created by T012
  (later package), per `tasks.md` § Notes (one shared file, sequenced by `[blockedBy:]`). The red-first evidence
  file `notes/red-first-evidence.md` § "Why the owner page has no red-first row in this package" states the
  ordering.
- **No `.specify/templates/`, constitution, or `instructions.md` edit**: Phase 3 (US4, T020–T024) owns those.
- **No driver gate, no state-spine write, no second checker**: per C-32 and the dispatch brief.

## 6. Assumptions taken (unattended run — recorded, not asked)

1. **`.specify/.tmp/` parent was removed after T005.** `rmdir .specify/.tmp/086-sandbox` and the earlier
   `mktemp -d` scratch were cleaned. The bare `.specify/.tmp/` directory is recreated on demand by whichever
   later row needs it; it is git-ignored (`.specify/.gitignore:30`).
2. **The `/tmp` mount is `noexec` on this host.** T005 and every later sandbox row therefore use
   `.specify/.tmp/` (or `/var/tmp` for a real `git clone`). Recorded in `notes/premises.md` § 3.
3. **The 34 baseline failures are accepted as the implement-entry state.** They predate this package (measured
   at `9add95eb` on a tree where no 086 file had been written yet) and none of them touches a path this package
   creates. The closure comparison (`comm -13 baseline-failed.txt final-failed.txt`) is the only legal reading,
   and it is exact: any *new* failure is this feature's responsibility.
4. **The task-total ceiling check is not this package's object.** `decomposition-check.py --mode tasks` was
   measured at 87 rows at the tasks stage; this package added no row, so the reading is unchanged.

## 7. Anomalies surfaced (not repaired in place)

- `ANOMALY A-1` — **`tasks.md` § Environment Prerequisites' `contract`-collection reading has moved.**
  The tasks stage recorded `4303/7501 tests collected (3198 deselected) in 1.92s` at base `780652a4`;
  re-probed at implement entry the same command reads **`4305/7527 tests collected (3222 deselected) in 1.90s`**
  (`test-evidence/T003-collect-only.txt`). Both numbers moved, and part of the delta is this package's own unit
  test file (24 tests, none `contract`-marked). The *premise* the prerequisite exists for — "`contract`-marked
  collection is available" — holds, and no row in this feature pins either count, so nothing downstream is
  falsified. Surfaced rather than edited: the prerequisites block is `tasks.md`'s statement of a measurement it
  took at its own base commit, and rewriting another stage's dated reading is a judgement call this package does
  not own. The reading to use at closure is the one re-measured there, not either of these.
- `ANOMALY A-2` — **`T003`'s evidence first landed as a 7,543-line raw `--collect-only` dump.** It proved
  collection but violated the summary-first discipline (a full node-id listing is machine data, not a digest).
  Repaired in passing in the commit that followed: the file is now a 19-line record of the two counts and exit
  codes, with a note pointing at the full-suite capture for the real verdict. Disclosed because a raw dump had
  already been committed once.
