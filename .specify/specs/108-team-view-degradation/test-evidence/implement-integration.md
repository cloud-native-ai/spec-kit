# Implement integration — 108-team-view-degradation

Stage `implement` of line `team-view-degradation` (run id `r20261126T071500Z-108a`), single
closing execution by the SDD Stage Integrator. Branch `108-team-view-degradation`, worktree
`.specify/.tmp/sdd-loop/worktrees/team-view-degradation`. Stage base `005437f72` — the
DoD-2 `implement_start_commit=` recorded in `test-evidence/implement-entry-readings.txt`;
the program fidelity baseline stays `54c6efa8c` (DoD-6, a different referent).

## Integration order

P1 → P2 → P3 → P4, serial in one shared worktree (the decomposition's declared write-alone
order; the packages ran as `implement-p1`…`implement-p4`). Verified outputs were aggregated
in that order; **no contradiction was found between package outputs**. Part commits are not
rewritten: this integration adds one closing commit on top of `31994cc90`.

Part commits as dispatched (endpoints inclusive):

- P1 `c55521f3c..74ae2e076` (T001–T005)
- P2 `83bb3bdea..33303ba94` (T006–T012)
- P3 `2db7c8ca9..3477f63f1` (T013–T018)
- P4 `0588a2114..31994cc90` (T019–T029)

## Coverage — 29/29

Program-checked over the effective package verdicts (not eyeballed): every row T001–T029 is
covered by exactly one check row, every effective check result is `pass` — zero missing,
zero duplicate, zero non-pass, and the four ranges are contiguous and disjoint. Verdicts
are runtime state under `/storage/project/cloud-native-ai/spec-kit/.specify/state/wp/`
(cited, not committed):

| Package | Task range | Check rows | Effective verdict |
|---------|-----------|------------|-------------------|
| P1 (a2) | T001–T005 | 5 | pass |
| P2 (a1) | T006–T012 | 7 | pass |
| P3 (a1) | T013–T018 | 6 | pass |
| P4 (a1) | T019–T029 | 11 | pass |

- `team-view-degradation-implement-p1-a2.verdict.json` — pass, verified 2026-11-26T09:59:01Z.
  Supersedes `…-p1-a1.verdict.json` (fail, 09:56:35Z): the a1 attempt's single blocking
  defect was T005's E2 baseline row missing the `trigger` field; the field was repaired
  (`"trigger":"scheduled"`) before the a2 verification, which re-checked all five rows
  pass. The a1 verdict stays on disk as history.
- `team-view-degradation-implement-p2-a1.verdict.json` — pass, 10:10:59Z.
- `team-view-degradation-implement-p3-a1.verdict.json` — pass, 10:23:50Z.
- `team-view-degradation-implement-p4-a1.verdict.json` — pass, 12:32:38Z.

The substance behind each verdict is this spec's committed evidence: `notes/` (red-first
slots, per-story green records, quickstart run) and `test-evidence/` (red captures,
targeted set, shape guard, mirror checks, verification input).

## Task-table closure

All 29 rows flipped `- [ ]` → `- [X]` by this integration with task text untouched —
mechanically verified: normalizing `- [X]` back to `- [ ]` reproduces the pre-edit file
byte-for-byte (29 changed lines, equal line counts). `validate-tasks.py` returns
`PASS … 0 error(s), 0 warning(s)`; the GATE-8 pattern `^- \[[ >]\]` counts 0.

## Test readings

**Stage-start baseline (the line's single baseline slot).** One full suite at implement
entry through the single runner, 2026-11-26T09:50:12Z: **221 failed / 10191 passed**
(10190 from the main parallel pass + 1 from the serial second pass), 3 skipped, rc 1. The
221 failed node ids are frozen in `baseline-failed.txt` (221 lines, all node ids); the full
output is `test-evidence/implement-baseline.log`; the spine E2 row seq 1 carries
`trigger: scheduled`, `passed: 10191`, `failed: 221`. TB-03 forbids a second full suite
inside `implement` — none was run; the wrap-up accounting reads the recorded targeted set.

**Red-first (every new-behavior test was red before its subject landed).** Captures:
`us1-red-unit.txt` (AttributeError on the absent grammar/classifier entry),
`us1-red-integration.txt` (6 failed in 6.31s), `us2-red-degraded.txt` (7 failed + 1
guard-pass), `us2-red-states.txt` (3 failed), `us3-red-contract.txt` (1 failed, 17 passed —
`test_three_surfaces_cite_the_owner` red until T021–T023). The two T020 guards are the
declared migration/regression exception: their claims (byte fidelity, zero-write snapshots)
become meaningful only after the engine amendment, and they were authored after it.

**Green readings (all through `scripts/bash/run-tests.sh` with
`SPECKIT_PYTHON=/usr/local/bin/python3`):**

- US1 (T012): 12 passed (6 unit recognition + 6 integration) in 6.59s — SC-001 production
  replica latest = parsed maximum at 5/5 classification with exit 5; SC-002 corpus replica
  13/13 recognized at exit 0.
- US2 (T018): 17 passed in 6.80s — the integration file then held 6 US1 nodes + 11 US2
  nodes. SC-003: six named states on one degraded view at exit 5, 9/9 members,
  `/speckit.team modify` ≥ 1, zero fabricated values; the unreadable-latest node exits 0.
- US3 (T025): 37 passed in 6.85s (18 contract + 19 integration, including the 2 T020
  guards). SC-004: healthy-fidelity stdout diff lines = 0, equal exits, both goal variants.
  SC-005: reason set `{engine-degraded, report-recognition-uncertain}`, 2/2 exit-5 mapping,
  observed exits ⊆ `{0,2,3,4,5}`, `-h`/`--help`/`--version` zero-write. SC-006: overview
  equality 2/2 and a single recognition entry (one `classify_runs`, one compiled grammar).
  SC-007: three-scenario snapshots — additions / modifications / deletions = 0 / 0 / 0.
  Label closure: 20 owner-table members ↔ 17 program constants, both directions.
- Targeted set (T027, SC-008): the seven files named by quickstart.md § Run the targeted
  set — **149 passed, 0 failed, 0 skipped** in 7.01s, rc 0. The failed-name list
  `targeted-current-failed.txt` holds 0 entries; `comm -13 baseline-failed.txt
  targeted-current-failed.txt` reads **0 new failure names**. Composition: 43 new nodes
  (6 unit + 18 contract + 19 integration) + the 106 inherited team-view nodes. This is the
  only suite execution of this integration; a `--collect-only` pass (43 collected) was used
  to verify the node arithmetic — never a re-run.
- Shape guard (T028): `git diff --stat 54c6efa8c..HEAD -- skills/internal/create-team/SKILL.md
  skills/internal/create-team/references/create-mode.md` is empty; the two pinned nodes pass;
  the corpus replica still recognizes 13/13 and compact names stay run reports.
- Quickstart (T026): S-0…S-7 executed as written (S-0 route a live; S-1…S-7 route b through
  their named pinning tests); every scenario's exit matches its spec — 0 for healthy and
  read-only scenarios, 5 for the residue-only and degraded scenarios; record
  `notes/quickstart-run.md`, teardown included.
- Mirror / copy convergence (T024): `sync-mirrors.py --write` synced 1 file; `--check` rc 0
  with zero DIFF (no NEW drift against `sync-mirrors-baseline.txt`);
  `regen-command-copies.py --check` rc 0; the two mirror pairs verify byte-identical
  (`cmp`).

**DoD-2 comparison units (measured in the P4 verdict, re-cited here).**
`git diff 005437f72..HEAD -- pyproject.toml` empty (dependency unit 1); the import-root
audit passes (unit 2); T020's three scenario snapshots count zero (storage unit 1); the
changed-path complement is addressed under residual 2 below (storage unit 2).

## Closing commit contents

The closed task table, this record, and six stage-evidence JSONL files that were untracked
at integration start — the five `<stage>.jsonl` stage-status rows (clarify / plan / tasks /
checklist / analyze) plus `analyze-incremental-r4.jsonl`. They were created during the
stage's E3 evidence reconciliation, live inside the declared surface
(`.specify/specs/108-team-view-degradation/test-evidence/**`), and are committed here as
records so no driver-audit evidence is lost with the worktree. No implementation content
changed; no part commit was rewritten.

## Disclosures and residuals

1. **P1 retry (a1 → a2).** The a1 fail was the single missing `trigger` field on the E2
   baseline row — a record-schema defect, not a deliverable defect; a2 re-verified the same
   five rows and passed. Recorded here because both verdict files remain as history.
2. **Declared-surface gap for `tasks.md`.** DoD-2's declared change surface lists the 8
   delivery files, `{notes,test-evidence,writeback}/**`, `checkpoints/**`,
   `coverage-baseline.txt` and the handoff record-store groups — it does not name
   `tasks.md`, yet DoD-1, GATE-8 and this dispatch mandate the task-table closure. The
   closing commit therefore adds exactly one path outside the literal surface:
   `.specify/specs/108-team-view-degradation/tasks.md` (untouched anywhere in
   `005437f72..31994cc90` before this commit; checkbox lines only). The GATE-6 changed-path
   difference over `<BASELINE>..HEAD` will contain that one path; it is the stage contract's
   own closure duty, disclosed for U4 adjudication rather than edited around (editing DoD
   text or skipping the closure would each invent intent the artifacts do not record).
3. **Writeback ledger gap (T019–T029).** `writeback/` holds T001–T018 (18 files) but no
   T019–T029 records, while handoff.md § Writeback prescribes one record per completed
   task. The P4 verdict passed T019–T029 on committed evidence; the missing 11 writeback
   files are surfaced, not backfilled (backfilling would require inventing run ids and
   authorship the integrator seat does not hold).
4. **E3 stage-evidence naming.** The five `<stage>.jsonl` stage-status rows were created
   during the P1 a1→a2 reconciliation to satisfy the test-budget audit's `<stage>.jsonl`
   naming; `review.jsonl` is still absent because the review stage has not run — the P1-a2
   verdict already records this as a driver closure-gate item, outside the implement
   deliverable.
5. **Reading reconciliations (totals unaffected).** Two part-era notes carry narrative
   count slips that contradict their own parentheticals: `targeted-set.txt` says "72 new"
   nodes while its enumeration and the measured collection are 43 new (6+18+19) + 106
   inherited = 149; `notes/us2-green.txt` says "7 US1 + 10 US2" while the file then held 6
   US1 + 11 US2 nodes = 17. The measured totals (149, 17) are consistent everywhere; the
   dated notes were left untouched as records, and this record carries the reconciled
   readings.
6. **Test-side correction at T018** (as disclosed in `notes/us2-green.txt`): two assertion
   prefixes in `test_undeclared_pattern_and_zero_line_ledger_states` were tightened after
   the red capture; both target lines that existed at red time, and the recorded red cause
   (the absent `适用性不可判定` state) is unchanged. No product rule was touched.
7. **Quickstart name correspondence and S-0 re-reading** (as disclosed in
   `notes/quickstart-run.md`): S-7's parenthetical node name is executed as its
   tasks.md-pinned equivalent `test_label_closure_both_directions` (the plan-owned
   quickstart was left unedited); S-0's baseline-blob sha256 equality no longer holds after
   the amendment — the fidelity claim is S-1's machine diff, not a hash equality.
8. **No anomaly inside the packages themselves**: the four effective verdicts passed with
   per-check evidence pointers, and no package output contradicts another. Residuals 2 and
   3 are stage-boundary facts this integration is the first seat positioned to observe.