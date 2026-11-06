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

## Scope note

This file is T015/T037 input only. The C-044/C-045 mutation legs (M-16/M-17/M-19) and the closure
diff (C-047, T055) are carried by their own rows; no mutation leg is claimed here.
