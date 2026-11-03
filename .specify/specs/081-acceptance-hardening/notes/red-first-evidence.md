# Red-First Evidence — Feature 081, slice 081a (implement stage)

**Opened**: 2026-11-03 at implement part 1 (T001), HEAD `f9f6d4f3`, branch `081-acceptance-hardening`.
**Owner of the obligation**: `tasks.md` § Definition of Done **DoD-2** and `## Format` § Tests Mode note —
each of the four 081a contract modules is authored *before* the row implementing its subject closes, and its
failing run is recorded here with **command line, real output, exit code and failing count**.

**Status of this file**: the four sections in § 1 are *scaffolding opened by T001 and filled by their own rows* —
T007, T008, T009, T010 write the red run; T011–T016 write the red→green transition. § 2 is filled once, at slice
close, by T022. **No section may be read as covered while it still reads `pending`**: nothing here is a claim
until it carries a real command, a real exit code and a real failing count.

## 1. The four 081a contract modules

| # | Test module | Contract clauses it pins | Red run written by | Subject that must be able to break |
|---|---|---|---|---|
| 1 | `tests/contract/test_closure_acceptance_check.py` | `contracts/closure-acceptance-check.contract.md` C-01…C-09, C-13…C-16 | T007 | `scripts/python/closure-acceptance-check.py` — verdict, closed reason set, exit-code tri-state, `final_path` counts, the seven fixtures |
| 2 | `tests/contract/test_requirements_checker.py` (extension) | `contracts/artifact-schemas.contract.md` AS-01…AS-04 | T008 | the sixth `path-marker` check label in `scripts/python/validate-requirements.py` |
| 3 | `tests/contract/test_acceptance_state_machine.py` | `contracts/state-vocabulary.contract.md` SV-03…SV-11 | T009 | `templates/feature-details-template.md` § Canonical Status State Machine and `templates/verification-log-template.md` |
| 4 | `tests/contract/test_gate_wiring_081.py` | `contracts/gate-wiring.contract.md` GW-01, GW-04 | T010 | the implement call site in `skills/internal/implement-feature/SKILL.md` Step 9 and `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate |

### 1.1 `tests/contract/test_closure_acceptance_check.py` — **red, written by T007; green expected at T015**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_closure_acceptance_check.py -q`
- Real output: `11 failed, 5 passed in 0.65s`; failures are the verdict/fixture assertions that require the full checker (`positive`, `negative`, `ladder-mutation`, `smoke-mutation`, `execution-without-final`, `mixed-path`, `expr-supporting-only`, human output, counts, waive grammar)
- Exit status / failing count: exit 1 / 11 failed
- Why red is correct now: T006 landed only the CLI surface; T015 completes the verdict logic.

### 1.2 `tests/contract/test_requirements_checker.py` — `path-marker` cases — **green after T011**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_requirements_checker.py -q`
- Real output: `40 passed in 1.82s`
- Exit status / failing count: exit 0 / 0 failed

### 1.3 `tests/contract/test_acceptance_state_machine.py` — **green after T012/T013**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_state_machine.py -q`
- Real output: `14 passed in 0.07s`
- Exit status / failing count: exit 0 / 0 failed

### 1.4 `tests/contract/test_gate_wiring_081.py` — **red, written by T010; green expected at T016**

- Command line: `bash scripts/bash/run-tests.sh tests/contract/test_gate_wiring_081.py -q`
- Real output: `7 failed, 1 passed in 0.05s`; failures are the Step-9/pre-status-flip invocation and block/accept assertions that require T016 wiring
- Exit status / failing count: exit 1 / 7 failed
- Why red is correct now: the implement call site is wired in T016; T010 authors the assertion first.

### 1.5 Absence check recorded at T001 (the state a red run requires)

```text
$ for f in tests/contract/test_closure_acceptance_check.py \
           tests/contract/test_requirements_checker.py \
           tests/contract/test_acceptance_state_machine.py \
           tests/contract/test_gate_wiring_081.py \
           tests/integration/test_acceptance_smoke.py; do
    if [ -f "$f" ]; then echo "PRESENT $f"; else echo "ABSENT  $f"; fi
  done
ABSENT  tests/contract/test_closure_acceptance_check.py
PRESENT tests/contract/test_requirements_checker.py
ABSENT  tests/contract/test_acceptance_state_machine.py
ABSENT  tests/contract/test_gate_wiring_081.py
ABSENT  tests/integration/test_acceptance_smoke.py
```

`test_requirements_checker.py` is the one **extension** module (five labels exist today, the sixth `path-marker`
label does not), so its red run is a new failing case inside an existing file rather than an absent file.

## 2. Slice-close set-level comparison (GATE-7 / DoD-6) — **measured 2026-11-03; the comparison FAILED (T022 not closed)**

Owner of the comparison rule: `tasks.md` DoD-6 / GATE-7 — the comparison unit is the failing test **id set**,
never a count and never a byte diff. The baseline side is the plan-stage capture and was **not** re-collected
(FR-023); only the head side was measured here.

### 2.1 Pin re-read (the comparison's validity precondition, FR-023)

```text
$ .venv/bin/python -m pytest --version   →  pytest 9.2.0
$ .venv/bin/python --version            →  Python 3.14.6
$ git --version                         →  git version 2.54.0 (Apple Git-157)
```

Both pins match `test-evidence/plan-runner-pins.txt` line for line, so this comparison is **valid** (not the
exit-2 input-error case): the difference below is a real difference about the tree, not a different runner.

### 2.2 The head run

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/.tmp/081a-head-failed.txt -q
43 failed, 7018 passed, 7 skipped, 4 warnings in 602.58s (0:10:02)
# failed-name list written: .specify/.tmp/081a-head-failed.txt (      43 entries)
EXIT=1
```

- exit status of the full-suite run: **1** (failures present — expected; the baseline run also exited 1)
- head failed id set: 43 entries, `.specify/.tmp/081a-head-failed.txt` (temporary, `FR-025`, not committed)
- baseline side, by pointer: 39 entries, `baseline-failed.txt` (`test-evidence/plan-baseline-run.txt` carries
  the `39 failed, 6970 passed, 7 skipped` console transcript)

### 2.3 The two set differences

```text
$ comm -23 <(sort .specify/.tmp/081a-head-failed.txt) <(sort baseline-failed.txt)   # head − baseline
tests/contract/test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes
tests/contract/test_humanize_command_surface.py::test_wc13_stage_class_pin_remeasured
tests/contract/test_stage_class_wiring.py::test_stripping_the_card_restores_the_baseline_bytes[implement]
tests/contract/test_stage_class_wiring.py::test_stripping_the_card_restores_the_baseline_bytes[tasks]

$ comm -13 <(sort .specify/.tmp/081a-head-failed.txt) <(sort baseline-failed.txt)   # baseline − head
(empty)
```

- `head 失败集 − 基线失败集`: **4 ids — NOT empty.** The DoD-6 / GATE-7 invariant (`head − baseline` empty)
  does **not** hold on this tree, so T022's own criterion is unmet and the row stays open.
- `基线失败集 − head 失败集`: **empty** — this slice fixed none of the 39 pre-existing failures (nothing to
  enumerate row by row; the "fixed items" list is legitimately zero-length, not silently dropped).

### 2.4 What the four ids are (measured, not inferred)

All four are **frozen-pin guards** — no behavioural regression; each fires because an 081a edit moved a byte
that another feature froze on purpose:

| New id | Failing assertion | What moved it |
|---|---|---|
| `test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes` | `drifted: ['skills/internal/manage-features/SKILL.md']` — the C-5 non-wiring complement is byte-frozen | **T024** (this part): `Blocked` added to that skill's status vocabulary |
| `test_stage_class_wiring.py::…[tasks]` | `tasks: stripping the wiring card no longer restores the frozen baseline` | **T014** (part 3): the upgraded GATE-4 sentence in `templates/commands/tasks.md` |
| `test_stage_class_wiring.py::…[implement]` | the same assertion for `implement` | **T016** (part 3): the checker invocation + `Blocked` landing rule in `templates/commands/implement.md` |
| `test_humanize_command_surface.py::test_wc13_stage_class_pin_remeasured` | `tasks: stripping the wiring card no longer restores the frozen baseline` (it re-runs the same strip leg) | the same two templates |

Three of the four predate this part (they were already red on `da5e4480`, the part-3 commit); one is T024's.
Re-measuring these pins is a **decision that belongs to the pins' owning features** — `test_expression_compatibility`
C-5 says in its own failure text that "the slice may only touch W1-W4 and the feedback-step pointer", and
`test_stage_class_wiring`'s baselines are 077's frozen bytes. That authority is not recorded in any 081a row, so
this note **records** the difference and does not move a pin, an assertion or the baseline to make it disappear
(FR-023's "zeros new failures" is a finding to be earned, never a number to be arranged).

**Consequence for the slice**: with `head − baseline` non-empty, T022 cannot close, therefore `tasks.md` is not
zero-open, therefore the `Planned → Blocked` transition licensed by `shared/workflow/acceptance-hardening.md`
§ Feature Status ("the tasks are closed and at least one `final`-path criterion is not `pass`") is **not yet
licensed**. T020 therefore did not run in this part; the feature stays `Planned` until the four pins are
dispositioned by their owners and T022 is re-run.

### 2.5 Final closure-repair disposition (supersedes 2.2–2.4; the authoritative current result)

The four frozen-pin failures above were dispositioned without weakening any assertion:

- The 081 GATE-4 and closure-verdict lines were moved **inside** the existing 077 stage-class wiring card in
  `templates/commands/{tasks,implement}.md`, so stripping the card restores the frozen baseline byte for byte.
- T024 was **deferred to 081d** because WC-14 freezes `tests/contract/test_expression_compatibility.py`, so the
  C-5 allowlist entry for the `manage-features` edit cannot land in 081a; `manage-features` and C-5 were restored
  to the baseline. The feature-details owner remains the 081a status-vocabulary carrier.
- Five frozen-pin guards now pass (`test_c5_non_wiring…`, the two `test_stage_class_wiring` card strips,
  `test_wc13_stage_class_pin_remeasured`, `test_wc14_frozen_surfaces_unchanged`).

A second full-suite closure-repair run on the restored tree measured:

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/.tmp/081a-head-failed.txt -q
40 failed, 7021 passed, 7 skipped, 4 warnings in 616.02s (0:10:16)
EXIT=1
```

- `head 失败集 − 基线失败集`: **1 id** — `tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/external/coaching-skills/references/prompt-templates.md->.specify/skills/coaching-skills/references/prompt-templates.md]`.
  It is a **concurrent-writer artifact**, not an 081 defect: commit `90de4d7f` (coaching-skills) landed at
  11:19:54 while this run was in flight and changed both the source and its mirror. The parity test observed a
  transient mismatch; the same test passes in isolation (`1 passed`) and the final files are byte-identical
  (`sha256 77a9f635…` on both; `sync-mirrors.py --check` exit 0). This run is therefore **invalid as a clean head
  set**; a fresh full-suite run on the stable tree is the authoritative T022 measurement.
- `基线失败集 − head 失败集`: **0** (no pre-existing failure was fixed; nothing to enumerate).
- Pin re-read still matches `plan-runner-pins.txt`: `pytest 9.2.0`, `Python 3.14.6`, `git 2.54.0`.

Because the acceptance unit is the full-suite id-level set, the one flake is **recorded, not erased**: T022 is
`[~]` deferred (unblock: fix the 078 mirror-parity test isolation, then rerun the full suite and close T022), and
T024 is `[~]` deferred to 081d. `tasks.md` is now zero-open (22 closed / 2 deferred), `verification.md` records
SC-001 `blocked` and SC-002 `partial`, and the closure checker returns `block` / exit 1 /
`zero-final-path-pass`. The feature is therefore **`Blocked`**, never `Implemented`; this is the strict-acceptance
outcome the feature is built to produce.

### 2.6 Clean full-suite closure — authoritative T022 measurement (2026-11-03)

After the concurrent `90de4d7f` landed and the tree was stable, the full suite was rerun once:

```text
$ bash scripts/bash/run-tests.sh --names-out .specify/.tmp/081a-head-failed-clean.txt -q
39 failed, 7023 passed, 7 skipped, 4 warnings in 699.18s (0:11:39)
EXIT=1
```

- `head 失败集 − 基线失败集`: **empty** (0 new).
- `基线失败集 − head 失败集`: **empty** (0 fixed).
- pins re-read: `pytest 9.2.0`, `Python 3.14.6`, `git 2.54.0` (match `plan-runner-pins.txt`).
- T022 closes; T024 remains deferred to 081d. The earlier run2 mirror-parity failure is attributed to the
  concurrent commit, not to 081; the clean set is the T022 evidence.

### 2.7 Review-fix re-disposition of § 2.5's pin repair (2026-11-03, supersedes 2.5 only)

§ 2.5 repaired the two `test_stage_class_wiring` pins by moving the 081 GATE-4 and closure-verdict lines
**inside** the 077 class-read card, so that stripping the card restored the frozen `c1cd4600` bytes. The
review rejected that repair, correctly: it made one document (the 077 wiring card) own two unrelated
obligations, and it hid a real framework line inside a feature-specific block.

Re-dispositioned the other way, which is the way this test's own comment prescribes:

- the closure-verdict bullet is back in `templates/commands/implement.md` § **Feature Integration** (where the
  `Planned → Implemented` transition is owned) and the upgraded GATE-4 bullet back in
  `templates/commands/tasks.md` § **Outputs** — their semantic homes;
- `BASELINE_SHA256`'s `tasks` / `implement` rows were **re-measured with this module's own
  `strip_wiring` + `_sha256_text`** and carry a dated reason, so the guard still asserts what it was built to
  assert — *stripping the card restores the pinned bytes* — against the post-081 baseline instead of against
  a byte-equality that only held while the line hid inside the card;
- `tests/contract/test_gate_wiring_081.py` gained the command-surface assertion that was missing (deleting
  the bullet turns it red), which is what let the misplacement survive review in the first place.

Five frozen-pin guards re-verified green after the re-disposition: the two card strips, `test_wc13`'s strip
leg, `test_wc14_frozen_surfaces_unchanged`, and `test_c5_non_wiring_files_keep_their_frozen_hashes`.


