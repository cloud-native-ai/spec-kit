# ARC — Acceptance Reality Check — 093-concurrency-by-default

**Seat**: RV093-3 (ARC) · **Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-review` · **Branch**: `093-review` @ `46bcb8716` · **Date**: 2026-11-09
**Mode**: read-only. The only write is this file. No commit, no subagent dispatch, no repair.

## 1. Closure battery — measured vs claimed

Command (verbatim as mandated; the JSON payload was captured with the same inputs plus `--json`):

```
python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/093-concurrency-by-default --feature-registry .specify/memory/features.md
```

Exit status **1**. Measured against the WP5 record (`test-evidence/wp5-closure-reading.json`):

| Field | Claimed (WP5 record) | ARC re-measure | Match |
|---|---|---|---|
| `verdict` | `block` | `block` | yes |
| `final_path` | pass=5 blocked=1 deferred=0 partial=0 fail=0 unknown=0 total=6 | identical | yes |
| `claimed_status` | `Planned` | `Planned` (source: this worktree's `.specify/memory/features.md`) | yes |
| `reason` | `final-path-not-pass: SC-006` | identical, sole reason; `waived: []` | yes |
| `flow_class` | `execution` | `execution` | yes |
| `tasks` | open=159, closed=0, in_progress=0, deferred=0 | identical | yes |
| `smoke` | 1 record, `smoke_exit_code=0`, evidence path exists | identical (`wp5-acceptance-final.txt`, non-empty) | yes |
| `completion_conditions` | no_open_rows=false, status_row_per_criterion=true, every_final_path_pass=false, smoke_record_pass=true | identical | yes |

**Reproduced, not refuted.** The expected reading `verdict: block` with the single reason `final-path-not-pass: SC-006` is exact; the six `final`-path criteria decompose as SC-001…SC-005 `pass` and SC-006 `blocked`, so pass=5 / blocked=1 / total=6 follows mechanically from `requirements.md` (`**Path**` markers) and `verification.md` (`SC-NNN_status=` rows).

## 2. Gate re-runs

| Gate | Command | Recorded reading | ARC re-run |
|---|---|---|---|
| Closure battery | §1 | `block`, one reason SC-006, exit 1 | `block`, one reason SC-006, exit 1 |
| `validate-requirements` | `python3 scripts/python/validate-requirements.py …/requirements.md` and the `.specify/scripts/python/` copy | `wp5-validate-requirements.txt`: status ok, 345 lines / 48 definitions / 11 shared strings, **0 error / 0 warning** | identical: six checks pass, 345 / 48 / 11, **0/0**, exit 0 |
| `validate-tasks` | `python3 scripts/python/validate-tasks.py …/tasks.md` and the `.specify/scripts/python/` copy | `wp5-validate-tasks.txt`: PASS, **0 error / 0 warning**, 159 rows | identical: PASS, **0/0**, exit 0 |
| Task set | `grep -c '^- \[.\] T[0-9]' tasks.md` + closure payload | 159 rows, all `- [ ]` (open=159, closed=0) | 159 rows; 159 open / 0 closed / 0 in-progress / 0 deferred |
| Acceptance smoke | the 11-module `smoke_command` quoted in `verification.md` | `wp5-acceptance-final.txt`: 96 passed / 0 skipped in 7.14 s | **96 passed / 0 skipped in 7.13 s** |
| SC-002 pair | the two test ids cited by the SC-002 row | green | 3 passed together with SC-011 (below) |
| SC-006 live read | `…::test_this_features_coordination_report_is_decidable_or_not_evaluated` | 1 passed (`wp5-t110-t112-coordination-coverage.txt`) | 1 passed |
| Full suite (GATE-1) | `bash scripts/bash/run-tests.sh -q` | 207 failed / 8256 passed / 2 skipped, 0 NEW 093-caused | **not re-run** by ARC — outside the three-chain scope; the recorded GATE-1 name-level comparison stands as recorded |

**The mandate's `0/0 vs 0/1` premise does not match the evidence.** Both `wp5-validate-requirements.txt` and `wp5-validate-tasks.txt` record **0 error(s) / 0 warning(s)**, and both re-runs reproduce 0/0. There is no 0-error/1-warning reading in the wp5 validate pair; the only 0/1-shaped readings in `test-evidence/` belong to `account-clause-coverage` runs (657 errors / 1 warning), a different validator. Premise corrected, not confirmed — no 0/1 reading was fabricated to match it.

## 3. Success-criterion evidence chains

### 3.1 SC-002 — final path, claimed `pass` → **supported**

- **Claim**: `verification.md` § Success criteria row SC-002 and machine row `SC-002_status=pass`, citing `tests/contract/test_concurrency_serial_reason.py::test_default_concurrency_fixture_reads_effective_two` and `tests/contract/test_concurrency_high_order.py::test_reverting_analyze_to_off_turns_the_judgement_red`.
- **Artifact**: `test_concurrency_serial_reason.py:187-207` builds a two-unit record with intervals `[1000,1010)` and `[1005,1020)`, runs the engine's `reading` action and asserts `effective == 2`; `test_concurrency_high_order.py:212-233` mutates `decomposition-coverage.yaml` (`analyze: on → off`) and asserts an `analyze-default` finding.
- **Recompute**: both tests re-run green. By hand: under the fact's half-open interval and settle-before-dispatch tie-break (`shared/declarations/facts/effective-concurrency.yaml:27-29`; `scripts/python/concurrency-check.py:843-861`), the two intervals overlap from 1005 to 1010 → peak = 2. The claim `effective >= 2` is arithmetically forced by the fixture, and reverting the stage default to serial reds the judgement as claimed.
- **Caveat**: this is a record-level fixture — it proves the reading arithmetic and the default-on mutation, not an actual dispatch. Real dispatch is exactly what SC-006 owns.
- **Verdict**: supported.

### 3.2 SC-006 — final path, claimed `blocked` / `not_evaluated` → **supported as blocked**

- **Claim**: `verification.md` SC-006 row + five-field ladder (`blocked_at`, `reduced_measurement` with `..._run=yes`, `why_reduced_insufficient`, `unblock`), citing `notes/coordination-report.md`, `notes/serial-baseline.md` and `test-evidence/wp5-t110-t112-coordination-coverage.txt`.
- **Artifact**: the report records a real (non-fixture) implement run with six dispatched units and per-unit verdicts, declared-order integration `WP1 → WP2 → WP3 → WP4 → enginefix → WP5`, `duration: not_evaluated`, `effective: not_evaluated` with reason `mechanism-not-yet-landed`.
- **Recompute**:
  - The fact's `missing_interval_rule` (`effective-concurrency.yaml:29`) says any dispatched unit without an interval makes `effective` the literal `not_evaluated`. The report records no per-unit dispatch/settle epochs, so the rule yields `not_evaluated` — the value is the rule's output, not a fig leaf; the report explicitly refuses to reconstruct epochs from commit timestamps (an inference, not a measurement). Not `0`, not an estimate → no fabricated number.
  - 091 comparison: I re-read `.specify/state/091-auto-git-closeout.md` lines 57 and 186 — `62/62` tasks confirmed. The `1 agent` reading rests on 091's single implement checkpoint (`checkpoints/09-implement.md`). The `116 minutes` value has **no duration field in 091's spine**; it travels as the 093 spec's own dated citation (`requirements.md` line 19 / line 179; `features/093.md` line 5), and `serial-baseline.md` discloses exactly that chain. Weaker provenance than the task count, but disclosed, not fabricated.
  - The live test only asserts that a `coordination*.md` file contains the literal `not_evaluated` (`test_concurrency_real_run_evidence.py:242-247`); the report-shape judge (`_judge_report`) runs on synthetic dicts only. So the green live test evidences presence, not full report shape — the shape judgement is mine above.
- **Verdict**: supported as `blocked`: SC-006 is genuinely unmet (no real run with `effective >= 2`), and the missing quantity is honestly `not_evaluated`.

### 3.3 SC-011 — supporting path, claimed `pass` → **supported (textual guard)**

- **Claim**: `verification.md` SC-011 row + `SC-011_status=pass`, citing `tests/contract/test_concurrency_high_order.py::test_anti_nesting_chain_is_depth_two_with_its_three_prohibitions`.
- **Artifact**: `.specify/shared/definitions/subagent-definitions.md:170` states the permitted chain as **depth 2** (team orchestrator → invoking member → stage executor) and the three prohibitions verbatim; the test (`test_concurrency_high_order.py:130-145`) asserts the judge is empty on the real text, then replaces `MUST NOT start or host any SDD run` with `MAY carry the driver` and asserts it reds.
- **Recompute**: test re-run green; I read the source text and confirmed all four literal anchors (`depth 2` + the three prohibition sentences) are present, and that the mutation removes one of them.
- **Caveat**: this is a string-presence guard, not a semantic proof that no stage executor can start an SDD run. Acceptable on a `supporting` path; it should not be cited as enforcement evidence.
- **Verdict**: supported.

## 4. Registry judgement — `.specify/memory/features.md` row 093

**Measured**: the registry row (line 102) carries Status **`Planned`**; the checker resolved `claimed_status: Planned` from this worktree's registry. The row does not overclaim completion.

**Is `Planned` legal?** Yes as a *claim*, no as the *owed landing* — two different questions:

- The ARC owner (`shared/workflow/acceptance-hardening.md:674-676`) explicitly pairs `agree` when the checker's verdict is `block` and the claim is already `Blocked` **or `Planned`**; only `Implemented` / `Ready for Review` claims against a `block` are `refused`. `Planned` therefore does not exceed its evidence and triggers no `status-claims-implemented-but-blocked` reason.
- The transition owner (`templates/feature-details-template.md:73-75, 94`) and `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate (line 40 ff.) are stricter: `/speckit.implement` MUST land `Blocked` when the four conjunctive conditions do not hold, and on a closure `block` the gate says record the emitted reasons in `verification.md`, **land `Blocked`**, and MUST NOT write `Implemented`. Precedent is 088, whose implement stage landed `Planned → Blocked` on the same closure shape and whose review kept `Blocked`.

**What the close-out must record**:

1. Flip the 093 registry Status cell `Planned → Blocked` (Feature Details and Spec Path unchanged), and write the closure reason + date into the `Last Updated` cell (`final-path-not-pass: SC-006`; `not_evaluated`, no real concurrent run).
2. Keep the closure reasons in `verification.md` (already present) and keep `deferred_tasks=` consistent.
3. Reflect the task state honestly: `tasks.md` holds **159 `- [ ]` rows**, and **T098 is genuinely open by design** (F-093-003: the coordinator-dispatch verdict awaits its owner; `notes/implement-wp1.md` row T098 says so). The WP5 disclosure's phrasing ("state sigils are flipped by the integration owner") is true for the package rows but must not be read as "all 159 are done"; the close-out must name T098 as an open row (or record an owner ruling).
4. Do not write `Implemented` / `Ready for Review`; per U6 the line closes `blocked`, never `completed`.

**One further defect to record, not repair**: `verification.md:24-25` says SC-006 "requires an explicit user waiver for `Implemented → Ready for Review`". The waiver clause belongs to the `Implemented → Ready for Review` gate, but that gate is unreachable while the feature is not `Implemented`; `Blocked → Ready for Review` is illegal, and `Blocked → Implemented` requires the blocker lifted **and** every `final`-path criterion `pass` ("both, not either"). A waiver alone therefore does not create a legal exit from the blocked state; the normal resolution is a future run that actually dispatches and records intervals.

## 5. Terminal state (driver U6)

- **U6 rule**: the closure/merge step runs `closure-acceptance-check.py`; `block` marks the line `blocked` — the line is not, and must not become, `completed` (`skills/external/sdd-loop-driver/SKILL.md:90`).
- **Is `blocked` honest here?** Yes. SC-006 is unmet on measured evidence (no real run with `effective >= 2`); the only real run was a serial fold with no interval record; and condition (1) of `Planned → Implemented` independently fails with 159 open rows. Nothing in the tree records a per-unit dispatch/settle interval pair for any real run — the driver spine carries stage-level timestamps only, and no line-registry or fork-interval record exists in this worktree. The three-fork review wave is tracked at stage granularity, not per-fork intervals.
- **Is SC-006 resolvable before close-out?** Not from the data recorded so far. It becomes resolvable only by a run that (a) dispatches ≥ 2 units concurrently, (b) records `dispatched_at` / `settled_at` per unit, and (c) records per-unit verdicts, integration order and duration — the current review wave records none of these. A user waiver alone is not a legal exit (§4). No repair was performed; this is the report.

## 6. Carried residuals

| Residual | State | Owner / next reading |
|---|---|---|
| SC-006 `blocked` (final) | open | the next real run with recorded intervals; re-read `verification.md` SC-006 row |
| SC-007 `partial` (supporting) | open | add team territory-binding and loop per-stage fixture rows (ladder already present) |
| SC-010 `partial` (supporting) | open | 161 frozen-baseline + 44 master-inherited + 2 trigger-order reds outside this feature's write domain; whole-suite-green not claimed |
| T098 open | open by design | F-093-003 — coordinator-dispatch verdict value awaits its owner |
| 159 task sigils unflipped | open | integration owner flips per reality; T098 stays open unless ruled |
| F-093-002 | open | `overlap-check.py` path-prefix defect (framework, not repaired in 093) |
| F-093-020 | open | FR-035 fork mechanism vs current dispatch text — convergence owed in implementation/review |
| `verification.md:24-25` waiver sentence | imprecise | should be aligned with the state machine at close-out (§4) |
| 116-minute 091 figure | weaker provenance | spec-carried citation, no 091 duration field; disclosed in `serial-baseline.md` |
| Live-report test strength | caveat | literal-presence check; report shape judged only on synthetic dicts |
| Full suite (GATE-1) | not re-run by ARC | recorded reading 207F/8256P/2S, 0 NEW 093-caused, stands as recorded |
| Mandate `0/1` validator reading | premise mismatch | both wp5 validate files record 0/0; no 0/1 reading exists (§2) |

## 7. ARC verdict

**ACCEPT sustained.** The recorded acceptance state is independently reproducible to the field: `verdict: block`, `final_path: pass=5 blocked=1 total=6`, claimed `Planned`, single reason `final-path-not-pass: SC-006`; the 159-row task set and both validator 0/0 readings are confirmed; and the three sampled evidence chains (SC-002 pass, SC-006 blocked/`not_evaluated`, SC-011 pass) each hold on recomputation. The `Planned` claim is legal under the ARC `agree` pairing, but it is not the landing the workflow owes: the close-out must flip the registry to `Blocked` (§4), record T098 as a genuinely open row, and close the line `blocked` per U6. Nothing was repaired in this review.

ANOMALY: the claimed state lags the measured state — the registry still reads `Planned` while the closure verdict is `block` (legal as an ARC `agree` pairing but not the `Blocked` landing the state machine and Pre-Status-Flip Gate require), T098 is a genuinely open row rather than an unflipped sigil, and `verification.md` cites a waiver remedy at an `Implemented → Ready for Review` gate that is unreachable from `Blocked`; additionally the mandate's `0/1` validator reading does not exist — both `wp5-validate-*` files record 0/0 — and no repair was performed.

RV093-3-DONE
