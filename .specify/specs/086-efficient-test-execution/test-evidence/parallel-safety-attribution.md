# 086 T015 / T037 — Parallel failure-name attribution

Owner of the proposition: `tasks.md` T015 + T037 and
`contracts/dogfood-and-preservation.contract.md` C-045/C-046/C-047. The measurement itself is
`test-evidence/parallel-safety.txt` (T014); this file carries only the per-name disposition.

Referent: `test-evidence/baseline-failed.txt` — the T050 implementation-start baseline (19 names,
serial, taken before any source edit; never re-taken).

## Measurement read

- Post-change default-parallel run: `test-evidence/parallel-safety.txt` — 19 failed names,
  parallel pass 206.12 s, `comm -13` empty, `comm -23` empty.
- T016 arms (`test-evidence/scheduling-experiment.txt`): `-n auto --dist load` and
  `-n 8 --dist loadfile` also produce the same 19 names; `comm -3` empty; new names vs baseline 0.
- `test-evidence/parallel-safety.txt` itself carries the run's `--names-out` list at
  `.specify/.tmp/086/us1-parallel.txt` (scratch; the durable record is the evidence file).

## Three-way disposition (C-045)

**New failure names introduced by the parallel default: 0.** There is nothing to dispose of:

| disposition | count | names |
|---|---|---|
| root-cause fix | 0 | — |
| named serial exception | 0 new | the single declared exception (`test_c22_watch_target_hook_selftest`) is not a new failure name: it passes in the serial pass; see `test-evidence/serial-exceptions.txt` |
| pre-existing baseline failure | 0 new | the 19 parallel names are exactly the 19 T050 baseline names |
| **unattributed** | **0** | — |

The pre-existing determination is made against `test-evidence/baseline-failed.txt`, not against memory
or a count. Names absent from the parallel run but present in the baseline (`comm -23`): **empty** —
nothing is claimed as this feature's fix.

## Pre-emptive weakening check (C-046 / T037 second branch)

No test that already passed in parallel was weakened. The previously known hazards were handled
without touching their propositions:

- `tests/contract/test_sync_mirrors_only.py` and the smoke/mirror probes were left unchanged; they
  remained green under the parallel default in every full run (T014, T016 arms). No sandbox move was
  needed because no failure appeared.
- `test_c22_watch_target_hook_selftest` is the one declared serial exception, registered by marker
  (not skipped/xfailed/re-timed); its body and timeout are unchanged.
- Whole-worktree `git status` assertions (`test_closure_acceptance_check.py`,
  `test_humanize_command_surface.py`) were left un-scoped: the parallel evidence shows no failure, so
  narrowing them pre-emptively would have weakened a proposition that still holds.

## C-046 — no pre-emptive weakening (T055 green point)

`contracts/dogfood-and-preservation.contract.md` C-046: a test that passes in parallel today MUST NOT
be rewritten pre-emptively, and a fix MUST preserve the proposition the assertion makes. The three
named families, read on this tree:

| assertion family | file | proposition it makes | changed by this feature? |
|---|---|---|---|
| the mirror probe | `tests/contract/test_sync_mirrors_only.py` | every mirrored pair is byte-identical and `--check` exits 0 | **no** — no hunk touches it (`git diff --name-only $(git merge-base HEAD master)..HEAD -- tests/contract/test_sync_mirrors_only.py` is empty) |
| the smoke evidence | `tests/integration/test_acceptance_smoke.py` (`smoke_command`/`smoke_exit_code`/`smoke_evidence_path` shape) | a feature's smoke record is one command, exit 0, and an existing non-empty evidence path | **no** — no hunk touches it |
| the whole-worktree `git status` assertions | `tests/contract/test_closure_acceptance_check.py`, `tests/contract/test_humanize_command_surface.py` | a run writes only its declared outputs; the working tree it leaves behind has no undeclared delta | **no** — neither file is in the feature's diff |

All three stayed green in every full run this feature performed (T014 `test-evidence/parallel-safety.txt`,
the T016 arms `test-evidence/scheduling-experiment.txt`, and the closure slot
`test-evidence/closure-diff.txt`): none of them appears in the 19 baseline names, and the closure run
added no name. Because no failure appeared, no fix was needed, and therefore **nothing was scoped,
sandboxed or narrowed** — the strongest form of the proposition: the assertions are bit-for-bit what they
were before this feature started.

Verified mechanically:

```
$ git diff --name-only $(git merge-base HEAD master)..HEAD -- \
    tests/contract/test_sync_mirrors_only.py \
    tests/integration/test_acceptance_smoke.py \
    tests/contract/test_closure_acceptance_check.py tests/contract/test_humanize_command_surface.py
(no output)
```

The one whole-worktree `git status` proposition this feature *did* touch is its own new evidence file
`test-evidence/worktree-clean.txt` (T044), which records the bracketed run's delta rather than relaxing
anyone else's assertion.

## C-047 — the closure name diff (T055 green point)

Read off the two runs that already happened, never re-measured here:

| side | file | count |
|---|---|---|
| baseline (T050, slot 1) | `test-evidence/baseline-failed.txt` | 19 |
| closure (T047, slot 2, the clean `slot-2-closure` execution) | `test-evidence/final-failed.txt` | 19 |

```
$ comm -13 <(sort -u test-evidence/baseline-failed.txt) <(sort -u test-evidence/final-failed.txt)
(no output)                                                     -> added names: 0

$ comm -23 <(sort -u test-evidence/baseline-failed.txt) <(sort -u test-evidence/final-failed.txt)
(no output)                                                     -> dropped names: 0
```

Added names are **0** after attribution. Dropped names are **0**, recorded verbatim (empty) and claimed
as nothing — this feature does not assert it fixed any pre-existing failure. The two-way comparison, the
commands, both wall clocks and the contaminated `in-slot-rerun-attempt` that triggered the clean
re-execution are in `test-evidence/closure-diff.txt`.

## Mutation legs (doctored copies, never a tracked-file edit)

Housing: every doctored copy below lives under
`/Users/liuqiming.lqm/tmp/spec-kit/086/mutations-c2/sandbox` — a detached `git worktree` of this branch at
`93e61050`, sitting **outside the repo root** in the sanctioned cross-repository temp root
(`shared/guidelines/temp-directory-discipline.md` § 1). This is the correction to the previous attempt's
defect: that attempt's sandbox sat at `.specify/.tmp/086/mutations/sandbox/` *inside* the repo and
contaminated the closure run's two whole-tree Markdown scans (`closure-diff.txt` § The contaminated
execution). Every leg was restored with `git checkout --` and `git status --porcelain` in the sandbox
read **0 entries** after each restore. No tracked file in this worktree was touched to produce any leg.

### Leg M-16 — a byte changed outside the `SC-010_*` lines (C-050's mechanical half)

Mutation: `SC-010_unblock=` renamed to `SC-010_UNBLOCK=` — a line of 085 `verification.md` that is
**outside** the carve-out's four admissible prefixes, so it is exactly the mutation C-041's mechanical
check exists to catch.

```
$ git diff -U0 -- .specify/specs/085-sdd-temporary-goal-team/verification.md \
    | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' \
    | grep -cvE '^[+-]SC-010_(status|value|note|blocked_at)='
2
$ git diff -U0 -- .specify/specs/085-sdd-temporary-goal-team/verification.md | grep -E '^[+-]SC-010_[Uu]'
-SC-010_unblock=Run one small feature through the driver with the temporary team and record the stage agents' run report/checkpoints.
+SC-010_UNBLOCK=Run one small feature through the driver with the temporary team and record the stage agents' run report/checkpoints.
```

**RED as required**: 2 added/removed lines, neither matching `^SC-010_(status|value|note|blocked_at)=`, so
the GATE-5 second half fails. The same command over the **tracked** tree returns **0** — the carve-out
holds on the real tree.

A negative probe taken first is recorded because it sharpens the leg: renaming the *value* of
`SC-010_value` (`live SDD run` → `LIVE SDD run`) is **green** under this check — the line still matches
the prefix — which is correct, since C-041 admits any edit *to* those four lines. The first version of
this leg mutated the value and was therefore not a discriminating M-16; it was discarded and re-aimed at
a line the carve-out does not admit.

### Leg M-17 — skew rather than mark (skip form), re-applied (C-044)

Mutation: `@pytest.mark.serial` on `tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest`
replaced with `@pytest.mark.skip(reason="M-17 skip leg")` in the sandbox copy.

```
control (marker form, unmutated):
$ env -u PYTHONPATH SPECKIT_PYTHON=<venv>/python bash scripts/bash/run-tests.sh -q tests/contract/test_sdd_loop_driver_skill.py
# test runner exceptions: 1 declared serial test(s)
# test runner: mode=parallel workers=auto dist=load passes=2
24 passed in 1.31s
1 passed, 24 deselected in 28.43s

mutated (skip form):
# test runner: mode=parallel workers=auto dist=load passes=1     <- no exception line
24 passed, 1 skipped in 1.18s
```

The three-way-disposition check (a skipped or xfailed test is **not** one of root-cause fix / named
serial exception / pre-existing baseline failure):

```
control:  decorators on test_c22_watch_target_hook_selftest: ['serial']   GREEN: no skip/xfail; the exception is the registered marker form
mutated:  decorators on test_c22_watch_target_hook_selftest: ['skip']     RED: the watch-target self-test is SKIPPED/XFAILED — not one of the three admissible dispositions
```

**RED as required, and the marker-form control is GREEN** — the pair is what makes the leg
discriminating rather than a check that only ever says "red". The skip copy also loses the exception
line entirely (`passes=1`) and adds a `skipped` to the run's count: the test leaves the *evidence*
instead of moving out of the parallel pass, which is the difference C-044 exists to forbid.

The heavier form of this leg (marker removal under whole-suite parallel load, where the unmarked test
times out and lands in the failure-name list) is in `test-evidence/serial-exceptions.txt` § Leg F; the
skip form here is the one C-044 names as inadmissible on its own terms.

### Leg M-18 — claiming `pass` on a partial checkpoint chain (C-050)

Mutation, in the sandbox copy only, in two coordinated parts:

1. `.specify/specs/086-efficient-test-execution/checkpoints/04-…` through `11-…` removed, leaving
   **only** `01-requirements.md`, `02-clarify.md`, `03-plan.md` — the partial chain M-18 names.
2. `.specify/specs/085-sdd-temporary-goal-team/verification.md` doctored to claim completion:
   `SC-010_status=partial` → `SC-010_status=pass`, `SC-010_blocked_at=` emptied, `SC-010_note=` rewritten
   to assert a full 8-stage run, and the four now-inapplicable ladder rows deleted — so the row carries
   no textual hint that the chain is short.

The evidence-chain check (does the claim match what is on disk?):

```
mutated:
claimed=pass checkpoints=['clarify', 'plan', 'requirements'] missing=['tasks', 'checklist', 'analyze', 'implement', 'review']
RED: SC-010_status=pass with a partial chain; missing stages: tasks, checklist, analyze, implement, review   EXIT=1

control (unmutated):
CONTROL claimed=partial checkpoints=11 missing=['review']
GREEN: the claim matches the chain                                                                             EXIT=0
```

**RED as required**, and the control shows the check is not merely "everything is red": the real tree's
`partial` claim with 11 checkpoints and `review` still outstanding reads GREEN, because a `partial` claim
with a named gap is exactly what C-050 permits.

A negative probe on the first attempt is recorded for the same reason as M-16: with the checkpoints
unchanged and only `verification.md` doctored, the checker **passes**, because the live chain is
complete — which is why the M-18 mutation must also shorten the chain. That is stated in the leg's own
name ("only the requirements/clarify/plan checkpoints exist") and was honoured in the second attempt.

### Leg M-19 — `effective` reported from the declared 24 (C-049) — carried by T042

`test-evidence/serial-exceptions.txt` § 5 carries the M-19 leg; this file does not restate it.

## Scope note

This file is T015/T037 input, and since T055 it also carries C-046, C-047 and legs M-16/M-17/M-18. The
C-044/C-045 legs (M-17's marker-removal form, M-19) stay in `test-evidence/serial-exceptions.txt`, which is
their owner; the closure comparison's raw runs stay in `test-evidence/closure-diff.txt`. No mutation leg
edits a tracked file, and no leg's result is claimed as a test's green point beyond the clause it names.
